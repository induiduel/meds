"""Kurul 1 2026-2027 çıkmış soruları PDF'i → data/cikmis_2627/kurul1_2627.pdf

Kullanım: python3 scripts/cikmis_2627/uret.py
Sunulduğu yer: GET /api/test/kurul1/2627
"""
import sys
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

sys.path.insert(0, str(Path(__file__).parent))
from sorular import DERSLER, S  # noqa: E402

KOK = Path(__file__).resolve().parents[2]
CIKTI = KOK / "data" / "cikmis_2627" / "kurul1_2627.pdf"

FONT = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", FONT + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", FONT + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVI", FONT + "DejaVuSans-Oblique.ttf"))

st_baslik = ParagraphStyle("b", fontName="DVB", fontSize=15, leading=19)
st_alt = ParagraphStyle("a", fontName="DV", fontSize=8.5, leading=11.5, textColor=colors.HexColor("#444"))
st_ders = ParagraphStyle("d", fontName="DVB", fontSize=11, leading=14, textColor=colors.white)
st_kok = ParagraphStyle("k", fontName="DVB", fontSize=9, leading=12)
st_sik = ParagraphStyle("s", fontName="DV", fontSize=8.8, leading=11.5, leftIndent=8)
st_not = ParagraphStyle("n", fontName="DVI", fontSize=8, leading=10.5, leftIndent=8, textColor=colors.HexColor("#9a3412"))
st_eksik = ParagraphStyle("e", fontName="DVI", fontSize=8.8, leading=12, textColor=colors.HexColor("#777"))


def p(metin, stil):
    return Paragraph(escape(metin).replace("\n", "<br/>"), stil)


def ders_seridi(ad, bas, son, n):
    t = Table([[p(f"{ad}  ·  sınavda {bas}–{son}  ·  toplanan {n}/{son - bas + 1}", st_ders)]], colWidths=[180 * mm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#0f172a")),
                           ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    return t


def main():
    hikaye = [
        p("Dönem 3 Kurul 1 Çıkmış Sorular — 2026-2027", st_baslik), Spacer(1, 2 * mm),
        p("Öğrencilerin hatırladıklarından derlendi (24.10.2026). Sorular sınavdaki ders aralıklarına yerleştirildi; "
          "ders içindeki sıra kesin değildir, numaralar tahminidir. Toplanamayan sorular \"toplanmadı\" diye "
          "gösterilir. Cevaplar derleme anahtarıyla karşılaştırılıp kontrol edildi; farklılıklar soru altında not edildi.",
          st_alt), Spacer(1, 4 * mm),
    ]
    anahtar = []
    toplam = 0
    for ad, bas, son in DERSLER:
        sorular = S[ad]
        toplam += len(sorular)
        hikaye += [ders_seridi(ad, bas, son, len(sorular)), Spacer(1, 2.5 * mm)]
        for i, (kok, siklar, cevap, notu) in enumerate(sorular):
            no = bas + i
            blok = [p(f"{no}. {kok}", st_kok)]
            blok += [p(f"{'ABCDE'[j]}) {s}", st_sik) for j, s in enumerate(siklar)]
            if notu:
                blok.append(p("Not: " + notu, st_not))
            blok.append(Spacer(1, 3 * mm))
            hikaye.append(KeepTogether(blok))
            anahtar.append((no, cevap))
        eksik = list(range(bas + len(sorular), son + 1))
        if eksik:
            aralik = f"{eksik[0]}–{eksik[-1]}" if len(eksik) > 1 else str(eksik[0])
            hikaye += [p(f"{aralik}: toplanmadı ({len(eksik)} soru)", st_eksik), Spacer(1, 4 * mm)]
            anahtar += [(n, "—") for n in eksik]

    hikaye += [Spacer(1, 4 * mm), p("Cevap anahtarı (tahmini numaralarla)", st_baslik), Spacer(1, 2 * mm)]
    satirlar = []
    for r in range(25):
        satir = []
        for c in range(4):
            no, cv = anahtar[c * 25 + r]
            satir += [str(no), cv]
        satirlar.append(satir)
    t = Table([["No", "Cevap"] * 4] + satirlar, colWidths=[22 * mm, 23 * mm] * 4)
    t.setStyle(TableStyle([("FONTNAME", (0, 0), (-1, -1), "DV"), ("FONTNAME", (0, 0), (-1, 0), "DVB"),
                           ("FONTSIZE", (0, 0), (-1, -1), 8.5), ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                           ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0"))]))
    hikaye.append(t)
    hikaye += [Spacer(1, 3 * mm), p(f"Toplanan: {toplam}/100 · Toplanmayan: {100 - toplam}", st_alt)]

    def altbilgi(c, d):
        c.setFont("DV", 7.5)
        c.drawString(15 * mm, 10 * mm, "MeDSor · Kurul 1 2026-2027 çıkmış sorular (öğrenci derlemesi)")
        c.drawRightString(195 * mm, 10 * mm, f"Sayfa {d.page}")

    CIKTI.parent.mkdir(parents=True, exist_ok=True)
    SimpleDocTemplate(str(CIKTI), pagesize=A4, leftMargin=15 * mm, rightMargin=15 * mm, topMargin=14 * mm,
                      bottomMargin=16 * mm, title="Kurul 1 2026-2027 Çıkmış Sorular", author="MeDSor").build(
        hikaye, onFirstPage=altbilgi, onLaterPages=altbilgi)
    print(CIKTI, toplam)


if __name__ == "__main__":
    main()
