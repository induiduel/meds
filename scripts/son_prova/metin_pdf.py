#!/usr/bin/env python3
"""PDF'i diskte olmayan ders için slayt metni sayfaları (pdf_metin "=== SAYFA N ===" → N. sayfa).
Özet PDF'te o dersin slaytı yerine bu sayfalar gösterilir; sayfa numaraları korunur, üstte açık not bulunur.
Kullanım: metin_pdf.py <pdf_metin.md> <cikti.pdf> <ders adı>
"""
import re
import sys
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

FONT = Path(__file__).resolve().parents[2] / "public/fonts"
pdfmetrics.registerFont(TTFont("LS", str(FONT / "LiberationSans-Regular.ttf")))
pdfmetrics.registerFont(TTFont("LSB", str(FONT / "LiberationSans-Bold.ttf")))
G, Y = 960, 540


def satirlar(metin: str, font: str, boy: float, gen: float) -> list[str]:
    out = []
    for ham in metin.splitlines():
        ham = ham.rstrip()
        if not ham.strip():
            continue
        s = ""
        for w in ham.split(" "):
            t = (s + " " + w).strip() if s else w
            if pdfmetrics.stringWidth(t, font, boy) > gen and s:
                out.append(s)
                s = w
            else:
                s = t
        out.append(s)
    return out


def main():
    md, cikti, ad = sys.argv[1], sys.argv[2], sys.argv[3]
    parca = re.split(r"^=== SAYFA (\d+) ===\s*$", Path(md).read_text(encoding="utf-8"), flags=re.M)
    sayfa = {int(parca[i]): parca[i + 1] for i in range(1, len(parca) - 1, 2)}
    son = max(sayfa) if sayfa else 1
    c = canvas.Canvas(cikti, pagesize=(G, Y))
    for n in range(1, son + 1):
        c.setFillColor(HexColor("#FFFFFF")); c.rect(0, 0, G, Y, stroke=0, fill=1)
        c.setFillColor(HexColor("#FFF7E6")); c.rect(0, Y - 34, G, 34, stroke=0, fill=1)
        c.setFillColor(HexColor("#8A5A00")); c.setFont("LS", 12)
        c.drawString(20, Y - 22, f"{ad} · slayt {n} — slayt metni (bu dersin PDF dosyası paylaşılmadığı için yazı olarak gösterilir)")
        boy = 17
        ls = satirlar(sayfa.get(n, ""), "LS", boy, G - 80)
        while len(ls) * boy * 1.35 > Y - 80 and boy > 9:
            boy -= 1
            ls = satirlar(sayfa.get(n, ""), "LS", boy, G - 80)
        y = Y - 70
        for i, s in enumerate(ls):
            c.setFont("LSB" if i == 0 else "LS", boy + (3 if i == 0 else 0))
            c.setFillColor(HexColor("#111827"))
            c.drawString(40, y, s)
            y -= boy * 1.35 + (6 if i == 0 else 0)
        c.showPage()
    c.save()


if __name__ == "__main__":
    main()
