"""Kurul 1 2026-2027 çıkmış soruları PDF'i → data/cikmis_2627/kurul1_2627.pdf

Kullanım: python3 scripts/cikmis_2627/eslestir.py && python3 scripts/cikmis_2627/uret.py
Soru yerleşimi, konu ve durum bilgisi eslestir.py'nin ürettiği JSON'dan okunur.
Sınav kitapçığı düzeni: iki eşit sütun, tek yazı ailesi, renk yalnız durum noktasında ve işaretli şıklarda.
Sunulduğu yer: GET /api/test/kurul1/2627
"""
import json
import sys
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Frame, Image, KeepTogether, NextPageTemplate,
                                PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle)

sys.path.insert(0, str(Path(__file__).parent))
from sorular import DERSLER  # noqa: E402

KOK = Path(__file__).resolve().parents[2]
CIKTI = KOK / "data" / "cikmis_2627" / "kurul1_2627.pdf"
ESLESME = KOK / "data" / "cikmis_2627" / "kurul1_2627.json"
KTG = KOK / "data" / "cikmis_2627" / "ktg.jpeg"

FONT = "/usr/share/fonts/truetype/dejavu/"
for ad, dosya in [("F", "DejaVuSans"), ("FB", "DejaVuSans-Bold"), ("FI", "DejaVuSans-Oblique")]:
    pdfmetrics.registerFont(TTFont(ad, FONT + dosya + ".ttf"))
pdfmetrics.registerFontFamily("F", normal="F", bold="FB", italic="FI", boldItalic="FB")

H = colors.HexColor
SIYAH, METIN, GRI, CIZGI = H("#111111"), H("#222222"), H("#6e6e6e"), H("#d9d9d9")
DURUM = {  # renk yalnız durum içindir
    "emin": (H("#1e7b3c"), "doğrulandı"),
    "tartisma": (H("#b3261e"), "tartışmalı"),
    "eksik": (H("#b3261e"), "şık eksik"),
    "eklendi": (H("#1f4fb3"), "sonradan eklendi"),
    "uretildi": (H("#1f4fb3"), "şıklar üretildi"),
    "tahmini": (H("#9a5b00"), "yeri tahmini"),
    "kismi": (GRI, "hatırlanmadı"),
}

SAYFA_G, SAYFA_Y = A4
KENAR, ARA = 15 * mm, 8 * mm
SUTUN = (SAYFA_G - 2 * KENAR - ARA) / 2
GEN = SAYFA_G - 2 * KENAR
UST, ALT, BASLIK_ILK = 17 * mm, 15 * mm, 47 * mm
GIRINTI = 7 * mm  # soru numarasının asılı girintisi; kök, şık ve cevap bu hizadan başlar

BOY, SATIR = 8.6, 11.6


def st(ad, **k):
    k.setdefault("fontName", "F"); k.setdefault("fontSize", BOY); k.setdefault("leading", SATIR)
    k.setdefault("textColor", METIN)
    return ParagraphStyle(ad, **k)


st_kok = st("kok", fontName="FB", leftIndent=GIRINTI, firstLineIndent=-GIRINTI)
st_sik = st("sik", leftIndent=GIRINTI + 4.5 * mm, firstLineIndent=-4.5 * mm)
st_konu = st("konu", fontSize=6.6, leading=8.6, textColor=GRI, leftIndent=GIRINTI)
st_cevap = st("cevap", fontSize=7.8, leading=10.4, leftIndent=GIRINTI)
st_ders = st("ders", fontName="FB", fontSize=9, leading=11, textColor=colors.white)
st_ders_sag = st("derssag", fontSize=7.2, leading=11, textColor=colors.white, alignment=2)
st_eksik = st("eksik", fontName="FI", fontSize=7.8, leading=10.4, textColor=GRI, leftIndent=GIRINTI, firstLineIndent=-GIRINTI)
st_h = st("h", fontName="FB", fontSize=11, leading=14, textColor=SIYAH)
st_kucuk = st("kucuk", fontSize=7.2, leading=9.8, textColor=GRI)
st_hucre = st("hucre", fontSize=7.4, leading=9.6)
st_hucre_b = st("hucreb", fontName="FB", fontSize=7.2, leading=9.2)
st_not_no = st("notno", fontName="FB", fontSize=7.4, leading=9.8)
st_not = st("not", fontSize=7.4, leading=9.8, textColor=H("#333333"))


def p(metin, stil):
    return Paragraph(escape(metin).replace("\n", "<br/>"), stil)


def durumlar(k):
    n, siklar = k.get("not") or "", k["siklar"]
    t = ([] if k["sinav_no_kesin"] else ["tahmini"]) + ([] if siklar else ["kismi"])
    t += ["uretildi"] if "ders notundan üretildi" in n else (["eklendi"] if "24.10 eklendi" in n else [])
    t += ["eksik"] if "Şık eksik" in n or "hatırlanmadı" in n.split(".")[0] else []
    t += ["tartisma"] if "artışmalı" in n else []
    if siklar and not {"tartisma", "eksik", "uretildi", "eklendi"} & set(t):
        t.append("emin")
    return t


def ana_durum(t):
    return next(k for k in ("tartisma", "eksik", "uretildi", "eklendi", "emin", "kismi") if k in t)


def nokta(renk):
    return f'<font color="{renk.hexval()}" size="9">●</font>'


def soru_blogu(k):
    t = durumlar(k)
    ana = ana_durum(t)
    parca = [p(f"{k['ders']} · {k['konu']}", st_konu), Spacer(1, 0.8 * mm),
             Paragraph(f"{k['sinav_no']}.<font name='F'> </font>" + escape(k["kok"]).replace("\n", "<br/>"), st_kok),
             Spacer(1, 1.2 * mm)]
    if "NST trasesi" in k["kok"] and KTG.exists():
        en = SUTUN - GIRINTI
        img = Image(str(KTG), width=en, height=en * 336 / 644)
        img.hAlign = "RIGHT"
        parca += [img, Spacer(1, 1.2 * mm)]
    isaret = k.get("sik_isaretleri", {})
    if k["siklar"]:
        for j, s in enumerate(k["siklar"]):
            harf, metin = "ABCDE"[j], escape(s)
            for tur, durum in (("supheli", "tartisma"), ("uretildi", "uretildi")):
                if harf in isaret.get(tur, []):
                    metin = f'<u><font color="{DURUM[durum][0].hexval()}">{metin}</font></u>'
                    break
            parca.append(Paragraph(f"{harf}) {metin}", st_sik))
        cevap = k["cevap"]
    else:
        parca.append(p("Şıklar toplanmadı.", st_eksik))
        cevap = k["cevap"] if k["cevap"] != "?" else "belirlenemedi"
    ek = [DURUM[x][1] for x in t if x not in ("emin", ana)]
    satir = f'{nokta(DURUM[ana][0])} <font name="FB">Cevap: {escape(cevap)}</font>' \
            f'<font color="{GRI.hexval()}"> {DURUM[ana][1]}{" · " + " · ".join(ek) if ek else ""}' \
            f'{" · not ↓" if k.get("not") else ""}</font>'
    parca += [Spacer(1, 1.2 * mm), Paragraph(satir, st_cevap), Spacer(1, 4.2 * mm)]
    return KeepTogether(parca)


def ders_basligi(ad, bas, son, n):
    t = Table([[p(ad.upper(), st_ders), p(f"Soru {bas}–{son} · {n}/{son - bas + 1}", st_ders_sag)]],
              colWidths=[SUTUN * 0.62, SUTUN * 0.38], rowHeights=[7 * mm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), SIYAH), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 2.5 * mm), ("RIGHTPADDING", (0, 0), (-1, -1), 2.5 * mm),
                           ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return [CondPageBreak(45 * mm), t, Spacer(1, 4 * mm)]


def tablo(satirlar, gen, ek=()):
    t = Table(satirlar, colWidths=gen, repeatRows=1)
    t.setStyle(TableStyle([("FONTNAME", (0, 0), (-1, -1), "F"), ("FONTSIZE", (0, 0), (-1, -1), 7.4),
                           ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LINEBELOW", (0, 0), (-1, 0), 0.8, SIYAH),
                           ("LINEBELOW", (0, 1), (-1, -1), 0.3, CIZGI), ("LEFTPADDING", (0, 0), (-1, -1), 2),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 2), ("TOPPADDING", (0, 0), (-1, -1), 3),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 3)] + list(ek)))
    return t


def main():
    kayitlar = json.loads(ESLESME.read_text())["sorular"]
    ders_kayit = {ad: [k for k in kayitlar if k["ders"] == ad] for ad, _, _ in DERSLER}
    toplanan = [k for k in kayitlar if k["durum"] != "toplanmadi"]
    kesin = sum(1 for k in toplanan if k["sinav_no_kesin"])

    def ilk(c, d):
        c.saveState()
        y = SAYFA_Y - 15 * mm
        c.setFillColor(SIYAH); c.setFont("FB", 15); c.drawString(KENAR, y - 5 * mm, "DÖNEM 3 KURUL 1 ÇIKMIŞ SORULAR")
        c.setFont("F", 8.5); c.setFillColor(METIN)
        c.drawRightString(SAYFA_G - KENAR, y - 5 * mm, "2026–2027 · Öğrenci derlemesi")
        c.setFillColor(GRI); c.setFont("F", 7.4)
        c.drawString(KENAR, y - 11 * mm, f"{len(toplanan)}/100 soru toplandı · {kesin} sorunun sınav numarası kesin · "
                                         f"{100 - len(toplanan)} soru toplanmadı · resmî değildir")
        c.setStrokeColor(SIYAH); c.setLineWidth(1); c.line(KENAR, y - 14 * mm, SAYFA_G - KENAR, y - 14 * mm)
        # durum açıklaması: tek satır, eşit aralıklı
        x, yy = KENAR, y - 19.5 * mm
        for tur in ("emin", "tartisma", "uretildi", "tahmini", "kismi"):
            renk, ad = DURUM[tur]
            c.setFillColor(renk); c.setFont("F", 9); c.drawString(x, yy, "●")
            c.setFillColor(METIN); c.setFont("F", 7.2); c.drawString(x + 3.6 * mm, yy + 0.3, ad)
            x += GEN / 5
        c.setFillColor(GRI); c.setFont("F", 6.8)
        c.drawString(KENAR, yy - 5 * mm, "Altı çizili mavi şık: sonradan eklendi ya da ders notundan üretildi.  "
                                          "Altı çizili kırmızı şık: şüpheli.  Notlar sondaki Notlar bölümünde.")
        c.setStrokeColor(CIZGI); c.setLineWidth(0.4); c.line(KENAR, yy - 8 * mm, SAYFA_G - KENAR, yy - 8 * mm)
        alt(c, d)
        c.restoreState()

    def alt(c, d):
        c.setStrokeColor(CIZGI); c.setLineWidth(0.4); c.line(KENAR, 10.5 * mm, SAYFA_G - KENAR, 10.5 * mm)
        c.setFillColor(GRI); c.setFont("F", 6.8)
        c.drawString(KENAR, 7 * mm, "Dönem 3 Kurul 1 · 2026–2027 çıkmış sorular")
        c.drawRightString(SAYFA_G - KENAR, 7 * mm, f"Sayfa {d.page}")

    def diger(c, d):
        c.saveState()
        c.setFillColor(SIYAH); c.setFont("FB", 7.4); c.drawString(KENAR, SAYFA_Y - 10 * mm, "DÖNEM 3 KURUL 1 ÇIKMIŞ SORULAR")
        c.setFillColor(GRI); c.setFont("F", 7.4); c.drawRightString(SAYFA_G - KENAR, SAYFA_Y - 10 * mm, "2026–2027")
        c.setStrokeColor(SIYAH); c.setLineWidth(0.8); c.line(KENAR, SAYFA_Y - 12 * mm, SAYFA_G - KENAR, SAYFA_Y - 12 * mm)
        if d.page > 1:
            c.setStrokeColor(CIZGI); c.setLineWidth(0.4)
            orta = KENAR + SUTUN + ARA / 2
            c.line(orta, ALT, orta, SAYFA_Y - UST)
        alt(c, d)
        c.restoreState()

    def iki_sutun(ust):
        h = SAYFA_Y - ust - ALT
        return [Frame(KENAR, ALT, SUTUN, h, 0, 0, 0, 0), Frame(KENAR + SUTUN + ARA, ALT, SUTUN, h, 0, 0, 0, 0)]

    def ilk_sayfa(c, d):
        ilk(c, d)
        c.saveState(); c.setStrokeColor(CIZGI); c.setLineWidth(0.4)
        orta = KENAR + SUTUN + ARA / 2
        c.line(orta, ALT, orta, SAYFA_Y - BASLIK_ILK); c.restoreState()

    doc = BaseDocTemplate(str(CIKTI), pagesize=A4, title="Dönem 3 Kurul 1 Çıkmış Sorular 2026-2027", author="MeDSor")
    doc.addPageTemplates([
        PageTemplate("ilk", iki_sutun(BASLIK_ILK), onPage=ilk_sayfa),
        PageTemplate("iki", iki_sutun(UST), onPage=diger),
        PageTemplate("tek", [Frame(KENAR, ALT, GEN, SAYFA_Y - UST - ALT, 0, 0, 0, 0)], onPage=diger),
    ])

    hikaye = [NextPageTemplate("iki")]
    for ad, bas, son in DERSLER:
        kay = ders_kayit[ad]
        hikaye += ders_basligi(ad, bas, son, sum(k["durum"] != "toplanmadi" for k in kay))
        eksik = []

        def eksik_yaz():
            if eksik:
                a = f"{eksik[0]}–{eksik[-1]}." if len(eksik) > 1 else f"{eksik[0]}."
                hikaye.extend([p(f"{a} Toplanmadı.", st_eksik), Spacer(1, 4.2 * mm)])
                eksik.clear()
        for k in kay:
            if k["durum"] == "toplanmadi":
                eksik.append(k["sinav_no"]); continue
            eksik_yaz()
            hikaye.append(soru_blogu(k))
        eksik_yaz()
        hikaye.append(Spacer(1, 2 * mm))

    # Cevap anahtarı
    hikaye += [NextPageTemplate("tek"), PageBreak(), p("CEVAP ANAHTARI", st_h), Spacer(1, 1.5 * mm),
               p("Harfin rengi durumu gösterir (ilk sayfadaki açıklama). “—”: toplanmadı. “m”: şık yok, cevap soruda.",
                 st_kucuk), Spacer(1, 4 * mm)]
    hucre = []
    for k in kayitlar:
        if k["durum"] == "toplanmadi":
            hucre.append((str(k["sinav_no"]), "—", GRI))
        else:
            hucre.append((str(k["sinav_no"]), k["cevap"] if k["siklar"] else "m", DURUM[ana_durum(durumlar(k))][0]))
    satirlar, stil = [], []
    for sat in range(25):  # 4 blok × (No, Cevap), dikey okunur
        satir = []
        for blok in range(4):
            no, cv, r = hucre[blok * 25 + sat]
            satir += [no, cv]
            stil.append(("TEXTCOLOR", (blok * 2 + 1, sat + 1), (blok * 2 + 1, sat + 1), r))
        satirlar.append(satir)
    at = Table([["No", "Cevap"] * 4] + satirlar, colWidths=[GEN / 8] * 8, rowHeights=[6 * mm] + [5.6 * mm] * 25)
    at.setStyle(TableStyle([("FONTNAME", (0, 0), (-1, -1), "F"), ("FONTSIZE", (0, 0), (-1, -1), 8),
                            ("FONTNAME", (0, 0), (-1, 0), "FB"), ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("GRID", (0, 0), (-1, -1), 0.3, CIZGI),
                            ("LINEBELOW", (0, 0), (-1, 0), 0.8, SIYAH), ("BACKGROUND", (0, 0), (-1, 0), H("#f2f2f2"))]
                           + [("FONTNAME", (c, 1), (c, -1), "FB") for c in (1, 3, 5, 7)] + stil))
    hikaye.append(at)

    # Notlar
    hikaye += [PageBreak(), p("NOTLAR", st_h), Spacer(1, 1.5 * mm),
               p("Soru kartında “not ↓” işareti olan soruların açıklamaları.", st_kucuk), Spacer(1, 4 * mm)]
    satir = [[p(str(k["sinav_no"]), st_not_no), p(k["not"], st_not)] for k in toplanan if k.get("not")]
    nt = Table(satir, colWidths=[10 * mm, GEN - 10 * mm])
    nt.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -1), 0.3, CIZGI),
                            ("LEFTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 3),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    hikaye.append(nt)

    # Karşılaştırma ve istatistik
    hikaye += [PageBreak(), p("GRUBUN PDF'İNDE OLMAYAN SORULAR", st_h), Spacer(1, 1.5 * mm),
               p("Grubun cevap anahtarlı PDF'i (24.10 16:31, 78 soru) ile karşılaştırıldı; aşağıdaki sorular yalnız bu "
                 "derlemede var.", st_kucuk), Spacer(1, 4 * mm)]
    satir = [[p("No", st_hucre_b), p("Ders", st_hucre_b), p("Soru", st_hucre_b), p("Dayanak", st_hucre_b)]]
    for k in toplanan:
        if not k["grup_pdfinde"]:
            satir.append([p(str(k["sinav_no"]), st_hucre), p(k["ders"], st_hucre), p(k["kok"].split("\n")[0], st_hucre),
                          p(k["grup_pdf_disi_dayanak"], st_hucre)])
    hikaye += [tablo(satir, [GEN * 0.06, GEN * 0.18, GEN * 0.46, GEN * 0.30]), Spacer(1, 9 * mm),
               p("İSTATİSTİKLER", st_h), Spacer(1, 1.5 * mm),
               p("Numara kesin: grupta sınavdaki numarasıyla yazılan sorular. Tam: kök ve şıklar hatırlandı, cevap "
                 "tartışmasız. Grup PDF'inde: grubun son PDF'inde de yer alan sorular.", st_kucuk), Spacer(1, 4 * mm)]
    bas_ = ["Ders", "Sınavda", "Toplanan", "Numara kesin", "Grup PDF'inde", "Yalnız bizde", "Tam", "Şıkları üretilen",
            "Tartışmalı", "Toplanmadı"]
    hs = st("hs", fontName="FB", fontSize=6.8, leading=8.6, alignment=1)
    satir, toplam = [[p(bas_[0], st_hucre_b)] + [p(b, hs) for b in bas_[1:]]], [0] * 9
    for ad, bas, son in DERSLER:
        kay = [k for k in ders_kayit[ad] if k["durum"] != "toplanmadi"]
        dz = [durumlar(k) for k in kay]
        say = [son - bas + 1, len(kay), sum(k["sinav_no_kesin"] for k in kay), sum(k["grup_pdfinde"] for k in kay),
               sum(not k["grup_pdfinde"] for k in kay), sum("emin" in d for d in dz), sum("uretildi" in d for d in dz),
               sum("tartisma" in d for d in dz), son - bas + 1 - len(kay)]
        toplam = [a + b for a, b in zip(toplam, say)]
        satir.append([p(ad, st_hucre)] + [str(x) for x in say])
    satir.append([p("<b>Toplam</b>", st_hucre)] + [str(x) for x in toplam])
    hikaye.append(tablo(satir, [GEN * 0.235] + [GEN * 0.085] * 9,
                        ek=[("ALIGN", (1, 0), (-1, -1), "CENTER"), ("FONTNAME", (1, -1), (-1, -1), "FB"),
                            ("LINEABOVE", (0, -1), (-1, -1), 0.8, SIYAH)]))

    CIKTI.parent.mkdir(parents=True, exist_ok=True)
    doc.build(hikaye)
    print(CIKTI, len(toplanan))


if __name__ == "__main__":
    main()
