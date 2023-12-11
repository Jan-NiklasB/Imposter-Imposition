import os
from pathlib import Path
import tempfile
from PIL import Image
from PIL.PpmImagePlugin import PpmImageFile
from pdf2image.exceptions import PDFInfoNotInstalledError, PDFPageCountError, PDFSyntaxError
from pdf2image import convert_from_path
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import pagesizes
from paper_formats import PaperFormats
from segmentations import _PageMap, S4x4
from pypdf import PdfWriter


def img_from_pdf(path_to_pdf: Path, tmp: tempfile.TemporaryDirectory, dpi: int = 600) -> list:
    """Creates images from each page of the given PDF file and saves them in the temp-folder

    :param path_to_pdf: Path object holding the path to the input PDF file
    :type path_to_pdf: Path
    :param tmp: TempDirectory object used to store the images
    :type tmp: tempfile.TempDirectory
    :param dpi: DPI of the resulting image
    :type dpi: int

    :returns: A list object with all images created from the PDF file
    :rtype: list
    """
    try:
        images_from_path = convert_from_path(path_to_pdf, dpi=dpi, output_folder=tmp.name)
        return images_from_path
    except PDFInfoNotInstalledError as e:
        print(e)
    except PDFPageCountError as e:
        print(e)
    except PDFSyntaxError as e:
        print(e)
    except Exception as e:
        print(e)


def rotate_img(img_obj: PpmImageFile):
    """Methode that rotates the saved image by 180 degrees

    :param img_obj: PIL PpmImageFile of the image to rotate
    :type img_obj: PpmImageFile
    """
    img = Image.open(img_obj.filename)
    img = img.rotate(180)
    img.save(img_obj.filename)


def create_single_page(page_nr: int, imgs: list[PpmImageFile], page_mapping: _PageMap.__subclasses__(), backside: bool,
                       output_landscape: bool, output_path: Path):
    """Methode that creates a single print page with the given parameters

    :param page_nr: Continuous page number
    :type page_nr: int
    :param imgs: A List of PpmImageFile-Objects in the sequence as given by page_mapping
    :type imgs: list[PpmImageFile]
    :param page_mapping: An instance of an _PageMap subclass (e.g. S2x2) that defines the rotation and mapping
    :type page_mapping: _PageMap.__subclasses__()
    :param backside: True if the side is the backside of a single print sheet
    :type backside: bool
    :param output_landscape: True if the print sheet is in landscape orientation in relation to the single page
    :type output_landscape: bool
    :param output_path: Path where the temporary separate pages get stored
    :type output_path: Path

    """
    if output_landscape:
        page = canvas.Canvas(str(output_path.joinpath(str(page_nr).zfill(4) + ".pdf")), pagesize=pagesizes.landscape(page_mapping.print_page_format[2]))
    else:
        page = canvas.Canvas(str(output_path.joinpath(str(page_nr).zfill(4) + ".pdf")), pagesize=pagesizes.portrait(page_mapping.print_page_format[2]))

    if backside:
        for i in range(0, len(imgs)):
            if page_mapping.rotation_back[i]:
                rotate_img(imgs[i])
            page.drawImage(imgs[i].filename, x=page_mapping.get_coords[i][0] * mm, y=page_mapping.get_coords[i][1] * mm,
                           width=page_mapping.final_page_format[0] * mm, height=page_mapping.final_page_format[1] * mm)

    else:
        for i in range(0, len(imgs)):
            if page_mapping.rotation_front[i]:
                rotate_img(imgs[i])
            page.drawImage(imgs[i].filename, x=page_mapping.get_coords[i][0] * mm, y=page_mapping.get_coords[i][1] * mm,
                           width=page_mapping.final_page_format[0] * mm, height=page_mapping.final_page_format[1] * mm)

    page.showPage()
    page.save()


def create_duplex_page(set_counter: int, imgs: list[PpmImageFile], page_mapping: _PageMap.__subclasses__(),
                       output_path: Path):
    """Methode that creates two pages (one duplex page pair)

    :param set_counter: Integer representing the current continous number of the image-set (one set = no. of images per duplex page)
    :type set_counter: int
    :param imgs: List holding the number of images needed for one duplex page
    :type imgs: list[PpmImageFile]
    :param page_mapping: _PageMap subclass instance holding the pagemap, rotation matrix etc.
    :type page_mapping: _PageMap.__subclasses__()
    :param output_path: Path object holding the path where the temporary page files get stored
    :type output_path: Path

    """
    if len(imgs) == len(page_mapping.mapping_front) * 2:
        imgs_front = []
        imgs_back = []
        for i in range(0, len(page_mapping.mapping_front)):
            imgs_front.append(imgs[page_mapping.mapping_front[i] - 1])
        for i in range(0, len(page_mapping.mapping_back)):
            imgs_back.append(imgs[page_mapping.mapping_back[i] - 1])
    else:
        imgs_front = []
        imgs_back = []
        n_of_imgs = len(imgs)
        empty_page = Image.new(mode="RGB", size=imgs[0].size, color=(255, 255, 255))
        empty_page.save("empty.ppm")
        empty_page = Image.open("empty.ppm")
        for i in range(0, len(page_mapping.mapping_front)):
            if page_mapping.mapping_front[i] > n_of_imgs:
                imgs_front.append(empty_page)
            else:
                imgs_front.append(imgs[page_mapping.mapping_front[i] - 1])
        for i in range(0, len(page_mapping.mapping_back)):
            if page_mapping.mapping_back[i] > n_of_imgs:
                imgs_back.append(empty_page)
            else:
                imgs_back.append(imgs[page_mapping.mapping_back[i] - 1])

    create_single_page(set_counter, imgs_front, page_mapping, False, False, output_path)
    create_single_page(set_counter + 1, imgs_back, page_mapping, True, False, output_path)


def create_book(imgs: list[PpmImageFile], page_mapping: _PageMap.__subclasses__(), output_path: Path):
    """Methode that creates all duplex pages from a given PDF file in a given page format

    :param imgs: List holding all pages as PpmImageFile
    :type imgs: list[PpmImageFile]
    :param page_mapping: Instance of a _PageMap subclass holding the pagemap, rotation matrix, input page format and
    print page format
    :type page_mapping: _PageMap.__subclasses__()
    :param output_path: Path object holding the path where the temporary page files get stored
    :type output_path: Path

    """
    pages_per_sheet = len(page_mapping.mapping_front) * 2
    i = 0
    img_sets = []
    img_set = []
    full_sets = int(len(imgs) / pages_per_sheet)
    additional_pages = len(imgs) % pages_per_sheet
    for s in range(0, full_sets, 1):
        img_set = []
        for p in range(s * pages_per_sheet, (s + 1) * pages_per_sheet):
            img_set.append(imgs[i])
            i = i + 1
        img_sets.append(img_set)
    img_set = []
    img_set = imgs[-additional_pages:]
    img_sets.append(img_set)
    set_counter = 1
    for ps in range(len(img_sets)):
        create_duplex_page(set_counter, img_sets[ps], page_mapping, output_path)
        set_counter = set_counter + 2


def merge_pages(output_path: Path):
    """Methode which merges all separate page files to one PDF file

    :param output_path: Path object holding the path where the merged PDF file is stored
    :type output_path: Path

    """
    merger = PdfWriter()
    filenames = os.listdir("./sites")
    for f in filenames:
        merger.append(Path.cwd().joinpath("sites").joinpath(f))
    merger.write(output_path)
    merger.close()


if __name__ == "__main__":
    temp = tempfile.TemporaryDirectory()
    pdf = Path("I:\Dokumente\Medikamentenkarten\Medikamentenkarten_vollständig.pdf")
    images = img_from_pdf(pdf, temp)
    create_book(images, S4x4(PaperFormats.DIN.A6, PaperFormats.DIN.A4), Path.cwd().joinpath("sites"))
    merge_pages(Path.cwd().joinpath("Medikamentenkarten_vollständig_imposed.pdf"))
    images.clear()
    images = None
    temp.cleanup()
    temp = None
    print("finished")
