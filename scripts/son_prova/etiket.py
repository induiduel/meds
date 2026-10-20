#!/usr/bin/env python3
"""Özet PDF sayfa üstü etiketleri: kirp.json'daki her sayfa için tek satırlık etiket şeridi (reportlab, Liberation Sans).
pdf_kirp.mjs bu şeritleri kaynak slaytın üstüne eklenen boş banda yerleştirir (pdf-lib standart yazı tipleri Türkçe harf çizemez).
Kullanım: etiket.py kirp.json cikti.pdf
"""
import json
import sys
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

FONT = Path(__file__).resolve().parents[2] / "public/fonts"
pdfmetrics.registerFont(TTFont("LS", str(FONT / "LiberationSans-Regular.ttf")))
pdfmetrics.registerFont(TTFont("LSB", str(FONT / "LiberationSans-Bold.ttf")))
G, Y = 1000, 30  # şerit boyutu (pt); slayt genişliğine ölçeklenir


def main():
    k = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    c = canvas.Canvas(sys.argv[2], pagesize=(G, Y))
    for i, s in enumerate(k["sayfalar"], 1):
        c.setFillColor(HexColor("#EEF2F7"))
        c.rect(0, 0, G, Y, stroke=0, fill=1)
        c.setFillColor(HexColor("#1F3A5F"))
        c.rect(0, 0, 6, Y, stroke=0, fill=1)
        sag = f"{i} / {len(k['sayfalar'])}"
        c.setFont("LS", 13)
        c.setFillColor(HexColor("#5B6B7F"))
        c.drawRightString(G - 14, 10, sag)
        metin = s["etiket"]
        c.setFont("LSB", 14)
        c.setFillColor(HexColor("#1F2937"))
        while pdfmetrics.stringWidth(metin, "LSB", 14) > G - 120 and len(metin) > 10:
            metin = metin[:-2]
        if metin != s["etiket"]:
            metin = metin.rstrip() + "…"
        c.drawString(16, 10, metin)
        c.showPage()
    c.save()


if __name__ == "__main__":
    main()
