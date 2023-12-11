# Imposter Imposition
A free imposition tool written in Python

## About the current state
I just started this project for my personal needs, since I wasn't able to find a functional, free 
imposition tool that fitted my needs.
Currently, I only fully implemented the 4 pages per page / 
8 pages per sheet mode and tested it with a DIN A6 PDF imposed onto DIN A4 sheets.

Any help is appreciated, just create a pull request and describe your changes.
(Also please comment your code as I did before)


## Requirements
To run the program in its current state you will need the following requirements:

* Python 3.12
* Pillow 10.1.0
* ReportLab 4.0.7
* pdf2img 0.1.2
* pypdf 3.17.2

## How to run

In main.py:

* Change the input pdf path (currently `"I:\Dokumente\Medikamentenkarten\Medikamentenkarten_vollständig.pdf"`)
* Change the output pdf path (currently `"Medikamentenkarten_vollständig_imposed.pdf"`)
* (Optional) Change the final page and print sheet format (Currently `S4x4(PaperFormats.DIN.A6, PaperFormats.DIN.A4)` )