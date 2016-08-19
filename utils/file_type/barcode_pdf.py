#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @date    160815 - completed

"""
Created barcode and output to PDF file.

Require Libraries:
(* is primary library)

  - Pillow==3.3.0
  - (*)reportlab==3.3.0
"""
from reportlab.graphics.barcode import code128
from reportlab.graphics.barcode import code39
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def pdf_exporter():
    # font
    pdfmetrics.registerFont(TTFont('STHeiti', 'STHeiti Light.ttc'))
    pdfmetrics.registerFont(TTFont('STHeitiM', 'STHeiti Medium.ttc'))

    mypdf = canvas.Canvas(filename='my_pdf.pdf')

    # output
    mypdf.setFont('STHeiti', 32)
    mypdf.drawString(100, 550, "Have a nice day!")
    mypdf.drawString(50, 600, "繁體謝謝，简体谢谢")

    # barcode
    mypdf.setFont('STHeiti', 1.5)
    barcode = code128.Code128("123456789", barHeight=50, barWidth=1.2)
    barcode.drawOn(mypdf, 50, 300)
    mypdf.setFont('STHeiti', 16)
    mypdf.drawString(80, 280, "Barcode 128")

    barcode2 = code39.Extended39(
        "123456789", barWidth=0.6 * mm, barHeight=15 * mm)
    barcode2.drawOn(mypdf, 50, 400)

    mypdf.setFont('STHeiti', 16)
    mypdf.drawString(80, 380, "Barcode 39-E")
    mypdf.showPage()
    mypdf.save()

if __name__ == '__main__':
    pdf_exporter()
