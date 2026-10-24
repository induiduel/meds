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
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Frame, KeepTogether, NextPageTemplate, PageBreak,
                                PageTemplate, Paragraph, Spacer, Table, TableStyle)

sys.path.insert(0, str(Path(__file__).parent))
from sorular import DERSLER, S  # noqa: E402

KOK = Path(__file__).resolve().parents[2]
CIKTI = KOK / "data" / "cikmis_2627" / "kurul1_2627.pdf"

FONT = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", FONT + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", FONT + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVI", FONT + "DejaVuSans-Oblique.ttf"))

H = colors.HexColor
MUREKKEP, GRI, SOLUK, CIZGI, ZEMIN = H("#1c1917"), H("#57534e"), H("#a8a29e"), H("#e7e5e4"), H("#fafaf9")
# Ders renkleri: (koyu vurgu, açık zemin)
RENK = {
    "Tıbbi Genetik": (H("#6d28d9"), H("#f5f3ff")),
    "Enfeksiyon Hastalıkları": (H("#b91c1c"), H("#fef2f2")),
    "Patoloji": (H("#be185d"), H("#fdf2f8")),
    "Halk Sağlığı": (H("#047857"), H("#ecfdf5")),
    "Üroloji": (H("#0369a1"), H("#f0f9ff")),
    "Kadın Hastalıkları ve Doğum": (H("#c2410c"), H("#fff7ed")),
    "Farmakoloji": (H("#4d7c0f"), H("#f7fee7")),
}
ETIKET = {"tahmini": (H("#78716c"), "YERİ TAHMİNİ"), "kismi": (H("#b45309"), "KISMİ"), "uretildi": (H("#1d4ed8"), "ŞIKLAR ÜRETİLDİ"),
          "tartisma": (H("#b91c1c"), "TARTIŞMALI")}
URETILDI = "ders notundan üretildi"

SAYFA_G, SAYFA_Y = A4
KENAR, ARA = 13 * mm, 7 * mm
SUTUN = (SAYFA_G - 2 * KENAR - ARA) / 2
UST_ILK, UST, ALT = 82 * mm, 16 * mm, 15 * mm


def st(ad, **k):
    k.setdefault("fontName", "DV"); k.setdefault("textColor", MUREKKEP)
    return ParagraphStyle(ad, **k)


st_kok = st("kok", fontName="DVB", fontSize=8.6, leading=11.6)
st_sik = st("sik", fontSize=8.3, leading=10.8, leftIndent=11, firstLineIndent=-11, textColor=H("#292524"))
st_not = st("not", fontSize=7.3, leading=9.6, textColor=H("#44403c"))
st_eksik = st("eksik", fontName="DVI", fontSize=7.8, leading=10, textColor=SOLUK)
st_ders = st("ders", fontName="DVB", fontSize=10.5, leading=13, textColor=colors.white)
st_ders_alt = st("dersalt", fontSize=7.5, leading=9, textColor=colors.white)
st_h = st("h", fontName="DVB", fontSize=14, leading=18)
st_kucuk = st("kucuk", fontSize=7.5, leading=10, textColor=GRI)


def p(metin, stil):
    return Paragraph(escape(metin).replace("\n", "<br/>"), stil)


def rozetler(turler):
    return " ".join(f'<font name="DVB" size="6.3" color="{ETIKET[t][0].hexval()}">[{ETIKET[t][1]}]</font>' for t in turler)


def ders_basligi(ad, bas, son, n):
    koyu, _ = RENK[ad]
    t = Table([[p(ad, st_ders), p(f"Soru {bas}–{son}\n{n}/{son - bas + 1} toplandı", st_ders_alt)]],
              colWidths=[SUTUN * 0.62, SUTUN * 0.38])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), koyu), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("ALIGN", (1, 0), (1, 0), "RIGHT"), ("LEFTPADDING", (0, 0), (-1, -1), 7),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 0), (-1, -1), 5),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 5), ("ROUNDEDCORNERS", [3, 3, 3, 3])]))
    return t


def soru_karti(ders, no, kok, siklar, cevap, notu, kesin):
    koyu, acik = RENK[ders]
    turler = ([] if kesin else ["tahmini"]) + ([] if siklar else ["kismi"]) + \
             (["uretildi"] if notu and URETILDI in notu else []) + \
             (["tartisma"] if notu and ("Tartışmalı" in notu or "tartışmalı" in notu) else [])
    baslik = f'<font name="DVB" color="{koyu.hexval()}">{no}.</font> {escape(kok).replace(chr(10), "<br/>")}'
    if turler:
        baslik += "<br/>" + rozetler(turler)
    icerik = [Paragraph(baslik, st_kok), Spacer(1, 1.6 * mm)]
    if siklar:
        icerik += [Paragraph(f'<font name="DVB" color="{koyu.hexval()}">{"ABCDE"[j]})</font> {escape(s)}', st_sik)
                   for j, s in enumerate(siklar)]
    else:
        metin = "Şıklar toplanmadı."
        if cevap != "?":
            metin += f' <font name="DVB">Hatırlanan cevap:</font> {escape(cevap)}'
        icerik.append(Paragraph(metin, st_sik))
    satirlar = [[icerik]]
    if notu:
        not_t = Table([[Paragraph(f'<font name="DVB" color="{koyu.hexval()}">Not</font>  {escape(notu)}', st_not)]],
                      colWidths=[SUTUN - 14])
        not_t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), acik), ("LEFTPADDING", (0, 0), (-1, -1), 5),
                                   ("RIGHTPADDING", (0, 0), (-1, -1), 5), ("TOPPADDING", (0, 0), (-1, -1), 3),
                                   ("BOTTOMPADDING", (0, 0), (-1, -1), 3), ("ROUNDEDCORNERS", [2, 2, 2, 2])]))
        satirlar.append([not_t])
    t = Table(satirlar, colWidths=[SUTUN])
    t.setStyle(TableStyle([("LINEBEFORE", (0, 0), (0, -1), 2, koyu), ("LEFTPADDING", (0, 0), (-1, -1), 7),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 4), ("TOPPADDING", (0, 0), (-1, -1), 2),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    return KeepTogether([t, Spacer(1, 3.2 * mm)])


def eksik_satiri(nolar):
    aralik = f"{nolar[0]}–{nolar[-1]}" if len(nolar) > 1 else str(nolar[0])
    t = Table([[p(f"{aralik}  ·  toplanmadı", st_eksik)]], colWidths=[SUTUN])
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.5, CIZGI, None, (2, 2)), ("LEFTPADDING", (0, 0), (-1, -1), 7),
                           ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    return [t, Spacer(1, 3.2 * mm)]


def yerlestir():
    """Ders → [(no, soru|None, kesin)] — grupta numarası yazılanlar yerinde, kalanlar boş numaralara sırayla."""
    sonuc = {}
    for ad, bas, son in DERSLER:
        sorular = S[ad]
        yer = {q[0]: (q, True) for q in sorular if q[0]}
        bos = [n for n in range(bas, son + 1) if n not in yer]
        for q, n in zip([q for q in sorular if not q[0]], bos):
            yer[n] = (q, False)
        sonuc[ad] = [(n, *yer.get(n, (None, False))) for n in range(bas, son + 1)]
    return sonuc


def anahtar_tablosu(ad, kayitlar):
    koyu, acik = RENK[ad]
    hucre = []
    for no, q, _ in kayitlar:
        if q is None:
            cv = "—"
        elif q[2]:
            cv = q[3] + ("*" if URETILDI in q[4] else "")
        else:
            cv = "kısmi"
        hucre.append((str(no), cv))
    sutun = 10
    satirlar = []
    for i in range(0, len(hucre), sutun):
        parca = hucre[i:i + sutun] + [("", "")] * (sutun - len(hucre[i:i + sutun]))
        satirlar += [[a for a, _ in parca], [b for _, b in parca]]
    gen = (SAYFA_G - 2 * KENAR) / sutun
    t = Table(satirlar, colWidths=[gen] * sutun, rowHeights=[5.2 * mm, 6.2 * mm] * (len(satirlar) // 2))
    stil = [("FONTNAME", (0, 0), (-1, -1), "DV"), ("FONTSIZE", (0, 0), (-1, -1), 7.5), ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("GRID", (0, 0), (-1, -1), 0.4, CIZGI)]
    for r in range(0, len(satirlar), 2):
        stil += [("BACKGROUND", (0, r), (-1, r), acik), ("TEXTCOLOR", (0, r), (-1, r), koyu),
                 ("FONTNAME", (0, r + 1), (-1, r + 1), "DVB"), ("FONTSIZE", (0, r + 1), (-1, r + 1), 8.5)]
    t.setStyle(TableStyle(stil))
    return t


def main():
    yer = yerlestir()
    toplanan = sum(len(S[a]) for a, _, _ in DERSLER)
    kismi = sum(1 for a, _, _ in DERSLER for q in S[a] if not q[2] or URETILDI in q[4])

    def ilk_sayfa(c, d):
        c.saveState()
        c.setFillColor(MUREKKEP); c.rect(0, SAYFA_Y - 52 * mm, SAYFA_G, 52 * mm, stroke=0, fill=1)
        x = KENAR
        for ad, _, _ in DERSLER:  # ders renk şeridi
            w = (SAYFA_G - 2 * KENAR) / len(DERSLER)
            c.setFillColor(RENK[ad][0]); c.rect(x, SAYFA_Y - 52 * mm, w, 1.6 * mm, stroke=0, fill=1); x += w
        c.setFillColor(SOLUK); c.setFont("DVB", 7.5)
        c.drawString(KENAR, SAYFA_Y - 13 * mm, "MeDSor  ·  DÖNEM 3  ·  KURUL 1  ·  ÖĞRENCİ DERLEMESİ")
        c.setFillColor(colors.white); c.setFont("DVB", 20)
        c.drawString(KENAR, SAYFA_Y - 24 * mm, "Çıkmış Sorular 2026–2027")
        c.setFont("DV", 8.3); c.setFillColor(H("#d6d3d1"))
        c.drawString(KENAR, SAYFA_Y - 31 * mm, "Derleme PDF'i ve “Konu çalışma grubu” tartışması")
        c.drawString(KENAR, SAYFA_Y - 35.5 * mm, "(23.10 10:00 – 24.10 15:25) birleştirildi.")
        c.setFillColor(SOLUK); c.setFont("DV", 7.3)
        c.drawString(KENAR, SAYFA_Y - 45 * mm, "Sınav sırası:  Genetik 1–12 · Enfeksiyon 13–34 · Patoloji 35–68 · Halk Sağlığı 69–78 · "
                                               "Üroloji 79–90 · Kadın Doğum 91–96 · Farmakoloji 97–100")
        # sayılar
        kutular = [(f"{toplanan}", "toplanan / 100"), (f"{100 - toplanan}", "toplanmadı"), (f"{kismi}", "kısmi / üretilmiş")]
        kx = SAYFA_G - KENAR - 3 * 21 * mm
        for deger, ad in kutular:
            c.setFillColor(colors.white); c.setFont("DVB", 19); c.drawCentredString(kx + 10.5 * mm, SAYFA_Y - 30 * mm, deger)
            c.setFillColor(SOLUK); c.setFont("DV", 6.6); c.drawCentredString(kx + 10.5 * mm, SAYFA_Y - 35 * mm, ad)
            kx += 21 * mm
        # işaret açıklaması
        y = SAYFA_Y - 60 * mm
        c.setFillColor(ZEMIN); c.roundRect(KENAR, y - 14.5 * mm, SAYFA_G - 2 * KENAR, 16.5 * mm, 2 * mm, stroke=0, fill=1)
        aciklama = [("tahmini", "Grupta numarası yazılmadı; dersin boş numarasına kondu."),
                    ("kismi", "Yalnız konu ya da doğru cevap hatırlanıyor, şıklar yok."),
                    ("uretildi", "Eksik şıklar ders notundan, hocanın soru üslubuyla üretildi."),
                    ("tartisma", "Cevap öğrenciler arasında kesinleşmedi; nota bakın.")]
        yy = y - 1.5 * mm
        for tur, metin in aciklama:
            renk, ad = ETIKET[tur]
            c.setFillColor(renk); c.setFont("DVB", 6.5); c.drawString(KENAR + 4 * mm, yy - 1 * mm, f"[{ad}]")
            c.setFillColor(GRI); c.setFont("DV", 7); c.drawString(KENAR + 30 * mm, yy - 1 * mm, metin)
            yy -= 3.6 * mm
        alt_bilgi(c, d)
        c.restoreState()

    def alt_bilgi(c, d):
        c.setStrokeColor(CIZGI); c.setLineWidth(0.5); c.line(KENAR, 10.5 * mm, SAYFA_G - KENAR, 10.5 * mm)
        c.setFillColor(SOLUK); c.setFont("DV", 6.8)
        c.drawString(KENAR, 7 * mm, "Kurul 1 · 2026–2027 çıkmış sorular · öğrencilerin hatırladıklarından derlenmiştir, resmî değildir")
        c.drawRightString(SAYFA_G - KENAR, 7 * mm, f"{d.page}")

    def diger_sayfa(c, d):
        c.saveState()
        c.setFillColor(MUREKKEP); c.setFont("DVB", 7)
        c.drawString(KENAR, SAYFA_Y - 9 * mm, "ÇIKMIŞ SORULAR 2026–2027")
        c.setFillColor(SOLUK); c.setFont("DV", 7); c.drawRightString(SAYFA_G - KENAR, SAYFA_Y - 9 * mm, "Dönem 3 · Kurul 1")
        c.setStrokeColor(CIZGI); c.setLineWidth(0.5); c.line(KENAR, SAYFA_Y - 11 * mm, SAYFA_G - KENAR, SAYFA_Y - 11 * mm)
        alt_bilgi(c, d)
        c.restoreState()

    def sutunlar(ust):
        y = ALT; h = SAYFA_Y - ust - ALT
        return [Frame(KENAR, y, SUTUN, h, 0, 0, 0, 0), Frame(KENAR + SUTUN + ARA, y, SUTUN, h, 0, 0, 0, 0)]

    doc = BaseDocTemplate(str(CIKTI), pagesize=A4, title="Kurul 1 2026-2027 Çıkmış Sorular", author="MeDSor")
    doc.addPageTemplates([
        PageTemplate("ilk", sutunlar(UST_ILK), onPage=ilk_sayfa),
        PageTemplate("iki", sutunlar(UST), onPage=diger_sayfa),
        PageTemplate("tek", [Frame(KENAR, ALT, SAYFA_G - 2 * KENAR, SAYFA_Y - UST - ALT, 0, 0, 0, 0)], onPage=diger_sayfa),
    ])

    hikaye = [NextPageTemplate("iki")]
    for ad, bas, son in DERSLER:
        hikaye += [CondPageBreak(45 * mm), ders_basligi(ad, bas, son, len(S[ad])), Spacer(1, 3 * mm)]
        eksik = []
        for no, q, kesin in yer[ad]:
            if q is None:
                eksik.append(no); continue
            if eksik:
                hikaye += eksik_satiri(eksik); eksik = []
            _, kok, siklar, cevap, notu = q
            hikaye.append(soru_karti(ad, no, kok, siklar, cevap, notu, kesin))
        if eksik:
            hikaye += eksik_satiri(eksik)
        hikaye.append(Spacer(1, 2 * mm))

    hikaye += [NextPageTemplate("tek"), PageBreak(), p("Cevap anahtarı", st_h), Spacer(1, 1.5 * mm),
               p("“*”: şıklar ders notundan üretildi. “kısmi”: şıklar toplanmadı. “—”: soru toplanmadı. "
                 "Numaraları tahmini olan soruların yeri ders içinde değişebilir.", st_kucuk), Spacer(1, 5 * mm)]
    for ad, bas, son in DERSLER:
        koyu, _ = RENK[ad]
        hikaye += [KeepTogether([Paragraph(f'<font color="{koyu.hexval()}">■</font>  <font name="DVB">{ad}</font>'
                                           f'  <font color="{GRI.hexval()}" size="7.5">{bas}–{son}</font>',
                                           st("ah", fontSize=9.5, leading=13)),
                                 Spacer(1, 1.5 * mm), anahtar_tablosu(ad, yer[ad]), Spacer(1, 5 * mm)])]

    CIKTI.parent.mkdir(parents=True, exist_ok=True)
    doc.build(hikaye)
    print(CIKTI, toplanan, kismi)


if __name__ == "__main__":
    main()
