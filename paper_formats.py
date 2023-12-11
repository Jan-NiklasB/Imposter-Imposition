from reportlab.lib import pagesizes


class PaperFormats:
    class DIN:
        A0 = [841.0, 1189.0, pagesizes.A0]
        A1 = [594.0, 841.0, pagesizes.A1]
        A2 = [420.0, 594.0, pagesizes.A2]
        A3 = [297.0, 420.0, pagesizes.A3]
        A4 = [210.0, 297.0, pagesizes.A4]
        A5 = [148.0, 210.0, pagesizes.A5]
        A6 = [105.0, 148.0, pagesizes.A6]
        A7 = [74.0, 105.0, pagesizes.A7]
        A8 = [52.0, 74.0, pagesizes.A8]
        A9 = [37.0, 52.0, pagesizes.A9]
        A10 = [26.0, 37.0, pagesizes.A10]

    class US:
        Invoice = [140.0, 216.0]
        Executive = [184.0, 267.0]
        Legal = [216.0, 356.0, pagesizes.LEGAL]

        class ANSI:
            A = [216.0, 279.0, pagesizes.LETTER]
            B = [279.0, 432.0, pagesizes.LEDGER]
            C = [432.0, 559.0]
            D = [559.0, 864.0]
            E = [864.0, 1118.0]
            F = [711.0, 1016.0]
