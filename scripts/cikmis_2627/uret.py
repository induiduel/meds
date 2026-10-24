"""Kurul 1 2026-2027 çıkmış soruları PDF'i → data/cikmis_2627/kurul1_2627.pdf

Kullanım: python3 scripts/cikmis_2627/eslestir.py && python3 scripts/cikmis_2627/uret.py
Soru yerleşimi, konu ve durum bilgisi eslestir.py'nin ürettiği JSON'dan okunur.
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

NOTO = "/usr/share/fonts/truetype/noto/"
for ad, dosya in [("Serif", "NotoSerif-Regular"), ("SerifB", "NotoSerif-Bold"), ("SerifI", "NotoSerif-Italic"),
                  ("Display", "NotoSerifDisplay-Bold"), ("Sans", "NotoSans-Regular"), ("SansB", "NotoSans-Bold"),
                  ("SansI", "NotoSans-Italic")]:
    pdfmetrics.registerFont(TTFont(ad, NOTO + dosya + ".ttf"))
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="SerifB", italic="SerifI", boldItalic="SerifB")
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="SansB", italic="SansI", boldItalic="SansB")

H = colors.HexColor
MUREKKEP, METIN, GRI, SOLUK, CIZGI, KAGIT = (H("#1a1a1a"), H("#2b2b2b"), H("#6b6b6b"), H("#a3a3a3"),
                                            H("#e4e1dc"), H("#f7f5f1"))
# Renk yalnız durumu gösterir; ders başlıkları ve sorular siyah-beyazdır.
DURUM = {
    "emin": (H("#1f7a3f"), "cevap doğrulandı"),
    "tartisma": (H("#b42318"), "tartışmalı"),
    "eksik": (H("#b42318"), "şık eksik"),
    "eklendi": (H("#2551b3"), "sonradan eklendi"),
    "uretildi": (H("#2551b3"), "şıklar üretildi"),
    "tahmini": (H("#a15c07"), "yeri tahmini"),
    "kismi": (GRI, "hatırlanmadı"),
}

SAYFA_G, SAYFA_Y = A4
KENAR_SOL, KENAR_SAG, UST, ALT = 22 * mm, 20 * mm, 20 * mm, 18 * mm
OLUK = 17 * mm  # soru numarası sütunu
GEN = SAYFA_G - KENAR_SOL - KENAR_SAG
METIN_GEN = GEN - OLUK


def st(ad, **k):
    k.setdefault("fontName", "Serif"); k.setdefault("textColor", METIN)
    return ParagraphStyle(ad, **k)


st_kok = st("kok", fontSize=10.2, leading=14.6)
st_sik = st("sik", fontSize=9.8, leading=13.4, leftIndent=16, firstLineIndent=-16)
st_meta = st("meta", fontName="Sans", fontSize=7, leading=9.5, textColor=GRI)
st_no = st("no", fontName="Display", fontSize=17, leading=19, textColor=MUREKKEP)
st_rozet = st("rozet", fontName="SansB", fontSize=6, leading=8)
st_cevap = st("cevap", fontName="Sans", fontSize=8.6, leading=11.5, alignment=2)
st_not = st("not", fontName="Sans", fontSize=7.6, leading=10.6, textColor=H("#4a4a4a"))
st_eksik = st("eksik", fontName="SansI", fontSize=8.2, leading=11, textColor=SOLUK)
st_govde = st("govde", fontName="Sans", fontSize=8.6, leading=12.4, textColor=H("#3a3a3a"))
st_h1 = st("h1", fontName="Display", fontSize=24, leading=28, textColor=MUREKKEP)
st_ust = st("ust", fontName="SansB", fontSize=7, leading=9, textColor=GRI)
st_hucre = st("hucre", fontName="Sans", fontSize=7.8, leading=10.2)
st_hucre_b = st("hucreb", fontName="SansB", fontSize=7.2, leading=9.2, alignment=1)


def p(metin, stil):
    return Paragraph(escape(metin).replace("\n", "<br/>"), stil)


def cizgi(kalinlik=0.4, renk=CIZGI):
    return Table([[""]], colWidths=[GEN], rowHeights=[0.1], style=TableStyle([("LINEBELOW", (0, 0), (-1, -1), kalinlik, renk)]))


def durumlar(k):
    n, siklar = k.get("not") or "", k["siklar"]
    t = ([] if k["sinav_no_kesin"] else ["tahmini"]) + ([] if siklar else ["kismi"])
    t += ["uretildi"] if "ders notundan üretildi" in n else (["eklendi"] if "24.10 eklendi" in n else [])
    t += ["eksik"] if "Şık eksik" in n or "hatırlanmadı" in n.split(".")[0] else []
    t += ["tartisma"] if "artışmalı" in n else []
    if siklar and not {"tartisma", "eksik", "uretildi", "eklendi"} & set(t):
        t.append("emin")
    return t


def ana_renk(t):
    for k in ("tartisma", "eksik", "uretildi", "eklendi", "emin", "kismi"):
        if k in t:
            return DURUM[k][0]
    return MUREKKEP


def rozetler(turler):
    return "<br/>".join(f'<font color="{DURUM[t][0].hexval()}">{DURUM[t][1]}</font>' for t in turler)


def soru_blogu(k):
    turler = durumlar(k)
    renk = ana_renk(turler).hexval()
    sag = [p(f"{k['ders']}  ·  {k['konu']}", st_meta), Spacer(1, 1.2 * mm),
           Paragraph(escape(k["kok"]).replace("\n", "<br/>"), st_kok), Spacer(1, 2 * mm)]
    if "NST trasesi" in k["kok"] and KTG.exists():
        sag += [Image(str(KTG), width=METIN_GEN * 0.92, height=METIN_GEN * 0.92 * 336 / 644), Spacer(1, 2 * mm)]
    isaret = k.get("sik_isaretleri", {})
    if k["siklar"]:
        for j, s in enumerate(k["siklar"]):
            harf, metin = "ABCDE"[j], escape(s)
            if harf in isaret.get("supheli", []):
                metin = f'<u><font color="{DURUM["tartisma"][0].hexval()}">{metin}</font></u>'
            elif harf in isaret.get("uretildi", []):
                metin = f'<u><font color="{DURUM["uretildi"][0].hexval()}">{metin}</font></u>'
            sag.append(Paragraph(f'<font name="SansB" size="8.6" color="#6b6b6b">{harf}</font> {metin}', st_sik))
        cv = k["cevap"]
        dogru = f'{cv}) {k["siklar"]["ABCDE".index(cv)]}' if cv in "ABCDE" else cv
    else:
        sag.append(p("Şıklar toplanmadı.", st_eksik))
        dogru = k["cevap"] if k["cevap"] != "?" else "belirlenemedi"
    sag += [Spacer(1, 1.6 * mm),
            Paragraph(f'<font color="{renk}">Tahmini cevap  <font name="SansB">{escape(dogru)}</font></font>', st_cevap)]
    if k.get("not"):
        not_t = Table([[p(k["not"], st_not)]], colWidths=[METIN_GEN])
        not_t.setStyle(TableStyle([("LINEBEFORE", (0, 0), (0, 0), 0.8, CIZGI), ("LEFTPADDING", (0, 0), (-1, -1), 7),
                                   ("RIGHTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 1),
                                   ("BOTTOMPADDING", (0, 0), (-1, -1), 1)]))
        sag += [Spacer(1, 1.6 * mm), not_t]
    sol = [p(str(k["sinav_no"]), st_no), Spacer(1, 1 * mm), Paragraph(rozetler(turler), st_rozet)]
    t = Table([[sol, sag]], colWidths=[OLUK, METIN_GEN])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 0),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return KeepTogether([t, Spacer(1, 4.5 * mm), cizgi(), Spacer(1, 4.5 * mm)])


def eksik_blogu(nolar):
    aralik = f"{nolar[0]}–{nolar[-1]}" if len(nolar) > 1 else str(nolar[0])
    soru = "Bu numaradaki soru" if len(nolar) == 1 else f"Bu numaralardaki {len(nolar)} soru"
    t = Table([[p(aralik, st("ne", fontName="Display", fontSize=12, leading=14, textColor=SOLUK)),
                p(f"Toplanmadı. {soru} hiçbir kaynakta hatırlanmadı.", st_eksik)]], colWidths=[OLUK, METIN_GEN])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return [t, Spacer(1, 4.5 * mm), cizgi(), Spacer(1, 4.5 * mm)]


def ders_acilisi(ad, bas, son, kayit):
    n = sum(1 for k in kayit if k["durum"] != "toplanmadi")
    konular = []
    for k in kayit:
        if k.get("konu") and k["konu"] not in konular:
            konular.append(k["konu"])
    return [CondPageBreak(80 * mm), Spacer(1, 2 * mm), p(f"SORU {bas}–{son}  ·  {n}/{son - bas + 1} TOPLANDI", st_ust),
            Spacer(1, 1.5 * mm), p(ad, st_h1), Spacer(1, 2 * mm), p("Konular: " + " · ".join(konular), st_meta),
            Spacer(1, 3 * mm), cizgi(1.2, MUREKKEP), Spacer(1, 6 * mm)]


def tablo(satirlar, gen, hizala_sol=1, ek=()):
    t = Table(satirlar, colWidths=gen, repeatRows=1)
    t.setStyle(TableStyle([("FONTNAME", (0, 0), (-1, -1), "Sans"), ("FONTSIZE", (0, 0), (-1, -1), 7.8),
                           ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (hizala_sol, 0), (-1, -1), "CENTER"),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.8, MUREKKEP), ("LINEBELOW", (0, 1), (-1, -1), 0.4, CIZGI),
                           ("LEFTPADDING", (0, 0), (-1, -1), 3), ("TOPPADDING", (0, 0), (-1, -1), 4),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 4)] + list(ek)))
    return t


def main():
    kayitlar = json.loads(ESLESME.read_text())["sorular"]
    ders_kayit = {ad: [k for k in kayitlar if k["ders"] == ad] for ad, _, _ in DERSLER}
    toplanan = [k for k in kayitlar if k["durum"] != "toplanmadi"]
    kesin = sum(1 for k in toplanan if k["sinav_no_kesin"])
    uretilen = sum(1 for k in toplanan if "uretildi" in durumlar(k))

    def kapak(c, d):
        c.saveState()
        c.setFillColor(KAGIT); c.rect(0, 0, SAYFA_G, SAYFA_Y, stroke=0, fill=1)
        c.setFillColor(GRI); c.setFont("SansB", 7.5)
        c.drawString(KENAR_SOL, SAYFA_Y - 24 * mm, "MeDSor  ·  DÖNEM 3  ·  KURUL 1  ·  ÖĞRENCİ DERLEMESİ")
        c.setFillColor(MUREKKEP); c.setFont("Display", 40)
        c.drawString(KENAR_SOL, SAYFA_Y - 44 * mm, "Çıkmış Sorular")
        c.drawString(KENAR_SOL, SAYFA_Y - 60 * mm, "2026–2027")
        c.setFont("Serif", 10); c.setFillColor(METIN)
        c.drawString(KENAR_SOL, SAYFA_Y - 71 * mm, "Derleme PDF'leri, “Konu çalışma grubu” tartışması (23.10 10:00 – 24.10 16:31),")
        c.drawString(KENAR_SOL, SAYFA_Y - 76 * mm, "ders notları ve geçmiş yılların çıkmış soruları birleştirilerek hazırlandı.")
        x = KENAR_SOL
        for deger, ad in [(len(toplanan), "toplanan / 100"), (kesin, "numarası kesin"),
                          (uretilen, "şıkları üretilen"), (100 - len(toplanan), "toplanmadı")]:
            c.setFillColor(MUREKKEP); c.setFont("Display", 26); c.drawString(x, SAYFA_Y - 96 * mm, str(deger))
            c.setFillColor(GRI); c.setFont("Sans", 7.5); c.drawString(x, SAYFA_Y - 101 * mm, ad)
            x += 40 * mm
        c.setStrokeColor(MUREKKEP); c.setLineWidth(1.2)
        c.line(KENAR_SOL, SAYFA_Y - 110 * mm, SAYFA_G - KENAR_SAG, SAYFA_Y - 110 * mm)
        c.restoreState()

    def sayfa(c, d):
        c.saveState()
        c.setFillColor(GRI); c.setFont("SansB", 6.8)
        c.drawString(KENAR_SOL, SAYFA_Y - 11 * mm, "ÇIKMIŞ SORULAR 2026–2027")
        c.setFont("Sans", 6.8); c.drawRightString(SAYFA_G - KENAR_SAG, SAYFA_Y - 11 * mm, "Dönem 3 · Kurul 1")
        c.setFillColor(SOLUK)
        c.drawString(KENAR_SOL, 9 * mm, "Öğrencilerin hatırladıklarından derlenmiştir; resmî değildir.")
        c.setFillColor(MUREKKEP); c.setFont("Display", 9); c.drawRightString(SAYFA_G - KENAR_SAG, 9 * mm, str(d.page))
        c.restoreState()

    doc = BaseDocTemplate(str(CIKTI), pagesize=A4, title="Kurul 1 2026-2027 Çıkmış Sorular", author="MeDSor")
    doc.addPageTemplates([
        PageTemplate("kapak", [Frame(KENAR_SOL, ALT, GEN, SAYFA_Y - 118 * mm - ALT, 0, 0, 0, 0)], onPage=kapak),
        PageTemplate("govde", [Frame(KENAR_SOL, ALT, GEN, SAYFA_Y - UST - ALT, 0, 0, 0, 0)], onPage=sayfa)])

    # Kapak: içindekiler ve işaretler
    hikaye = [NextPageTemplate("govde"), p("İÇİNDEKİLER", st_ust), Spacer(1, 2 * mm)]
    satir = [[p("Ders", st_hucre_b), p("Sınavda", st_hucre_b), p("Toplanan", st_hucre_b),
              p("Numarası kesin", st_hucre_b), p("Toplanmadı", st_hucre_b)]]
    for ad, bas, son in DERSLER:
        kay = [k for k in ders_kayit[ad] if k["durum"] != "toplanmadi"]
        satir.append([p(f"{ad}  ({bas}–{son})", st_hucre), str(son - bas + 1), str(len(kay)),
                      str(sum(k["sinav_no_kesin"] for k in kay)), str(son - bas + 1 - len(kay))])
    hikaye += [tablo(satir, [GEN * 0.44] + [GEN * 0.14] * 4), Spacer(1, 8 * mm), p("İŞARETLER", st_ust),
               Spacer(1, 2 * mm)]
    isaret = [[Paragraph(f'<font color="{DURUM[t][0].hexval()}" name="SansB">{DURUM[t][1]}</font>', st_hucre),
               p(acik, st_hucre)] for t, acik in [
        ("emin", "Cevap ders notuyla uyumlu, öğrenciler arasında tartışma yok."),
        ("tartisma", "Cevap kesinleşmedi; gerekçe sorunun notunda."),
        ("eksik", "Sorunun bazı şıkları hatırlanmadı."),
        ("eklendi", "Soru ilk derlemeden sonra gruptan eklendi."),
        ("uretildi", "Eksik şıklar ders notundan, hocanın soru üslubuyla üretildi."),
        ("tahmini", "Numara grupta yazılmadı; ders notlarının işleniş sırasına göre boş numaraya kondu."),
        ("kismi", "Soru hatırlanmadı.")]]
    isaret += [[Paragraph(f'<u><font color="{DURUM["uretildi"][0].hexval()}">Altı çizili mavi şık</font></u>', st_hucre),
                p("Sonradan eklenen ya da üretilen şık.", st_hucre)],
               [Paragraph(f'<u><font color="{DURUM["tartisma"][0].hexval()}">Altı çizili kırmızı şık</font></u>', st_hucre),
                p("Öğrencilerin emin olmadığı ya da değiştirdiği şık.", st_hucre)]]
    it = Table(isaret, colWidths=[GEN * 0.3, GEN * 0.7])
    it.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.4, CIZGI), ("TOPPADDING", (0, 0), (-1, -1), 3.5),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5), ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    hikaye += [it, PageBreak()]

    for ad, bas, son in DERSLER:
        hikaye += ders_acilisi(ad, bas, son, ders_kayit[ad])
        eksik = []
        for k in ders_kayit[ad]:
            if k["durum"] == "toplanmadi":
                eksik.append(k["sinav_no"]); continue
            if eksik:
                hikaye += eksik_blogu(eksik); eksik = []
            hikaye.append(soru_blogu(k))
        if eksik:
            hikaye += eksik_blogu(eksik)

    # Ek 1: cevap anahtarı
    hikaye += [PageBreak(), p("EK 1", st_ust), Spacer(1, 1 * mm), p("Cevap anahtarı", st_h1), Spacer(1, 2 * mm),
               p("Harfin rengi durumu gösterir: yeşil doğrulandı, kırmızı tartışmalı ya da şık eksik, mavi sonradan "
                 "eklendi ya da şıkları üretildi, gri toplanmadı. “metin”: şık yok, cevap soru sayfasında.", st_govde),
               Spacer(1, 6 * mm)]
    hucreler = []
    for k in kayitlar:
        if k["durum"] == "toplanmadi":
            hucreler.append((str(k["sinav_no"]), "—", DURUM["kismi"][0]))
        else:
            hucreler.append((str(k["sinav_no"]), k["cevap"] if k["siklar"] else "metin", ana_renk(durumlar(k))))
    satirlar, stil = [], []
    for i in range(0, 100, 10):
        parca = hucreler[i:i + 10]
        satirlar += [[a for a, _, _ in parca], [b for _, b, _ in parca]]
        r0 = len(satirlar) - 2
        stil += [("TEXTCOLOR", (0, r0), (-1, r0), SOLUK), ("FONTSIZE", (0, r0), (-1, r0), 7),
                 ("FONTNAME", (0, r0 + 1), (-1, r0 + 1), "SansB"), ("FONTSIZE", (0, r0 + 1), (-1, r0 + 1), 10),
                 ("LINEBELOW", (0, r0 + 1), (-1, r0 + 1), 0.4, CIZGI)]
        stil += [("TEXTCOLOR", (c, r0 + 1), (c, r0 + 1), rr) for c, (_, _, rr) in enumerate(parca)]
    at = Table(satirlar, colWidths=[GEN / 10] * 10, rowHeights=[5 * mm, 8 * mm] * 10)
    at.setStyle(TableStyle([("FONTNAME", (0, 0), (-1, -1), "Sans"), ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                            ("VALIGN", (0, 0), (-1, -1), "MIDDLE")] + stil))
    hikaye.append(at)

    # Ek 2: grubun PDF'inde olmayanlar, Ek 3: istatistik
    hikaye += [PageBreak(), p("EK 2", st_ust), Spacer(1, 1 * mm), p("Grubun PDF'inde olmayan sorular", st_h1),
               Spacer(1, 2 * mm),
               p("Grubun cevap anahtarlı PDF'i (24.10 16:31, 78 soru) ile karşılaştırıldı. Aşağıdaki sorular yalnız bu "
                 "derlemede var.", st_govde), Spacer(1, 4 * mm)]
    satir = [[p("No", st_hucre_b), p("Ders", st_hucre_b), p("Soru", st_hucre_b), p("Dayanak", st_hucre_b)]]
    for k in toplanan:
        if not k["grup_pdfinde"]:
            satir.append([str(k["sinav_no"]), p(k["ders"], st_hucre), p(k["kok"].split("\n")[0], st_hucre),
                          p(k["grup_pdf_disi_dayanak"], st_hucre)])
    hikaye += [tablo(satir, [GEN * 0.07, GEN * 0.18, GEN * 0.45, GEN * 0.30], hizala_sol=99),
               Spacer(1, 10 * mm), p("EK 3", st_ust), Spacer(1, 1 * mm), p("İstatistikler", st_h1), Spacer(1, 2 * mm),
               p("“Numarası kesin”: grupta sınavdaki numarasıyla yazılan sorular. “Tam”: kök ve şıklar hatırlandı, cevap "
                 "tartışmasız. “Grup PDF'inde”: grubun son PDF'inde de yer alan sorular.", st_govde), Spacer(1, 4 * mm)]
    basliklar = ["Ders", "Sınavda", "Toplanan", "Numara\nkesin", "Grup\nPDF'inde", "Yalnız\nbizde", "Tam",
                 "Şıkları\nüretilen", "Tartış-\nmalı", "Toplan-\nmadı"]
    satir, toplam = [[p(b, st_hucre_b) for b in basliklar]], [0] * 9
    for ad, bas, son in DERSLER:
        kay = [k for k in ders_kayit[ad] if k["durum"] != "toplanmadi"]
        dz = [durumlar(k) for k in kay]
        say = [son - bas + 1, len(kay), sum(k["sinav_no_kesin"] for k in kay), sum(k["grup_pdfinde"] for k in kay),
               sum(not k["grup_pdfinde"] for k in kay), sum("emin" in d for d in dz), sum("uretildi" in d for d in dz),
               sum("tartisma" in d for d in dz), son - bas + 1 - len(kay)]
        toplam = [a + b for a, b in zip(toplam, say)]
        satir.append([p(ad, st_hucre)] + [str(x) for x in say])
    satir.append([p("<b>Toplam</b>", st_hucre)] + [str(x) for x in toplam])
    ek = [("TEXTCOLOR", (3, 1), (3, -1), DURUM["emin"][0]), ("TEXTCOLOR", (6, 1), (6, -1), DURUM["emin"][0]),
          ("TEXTCOLOR", (5, 1), (5, -1), DURUM["eklendi"][0]), ("TEXTCOLOR", (7, 1), (7, -1), DURUM["uretildi"][0]),
          ("TEXTCOLOR", (8, 1), (8, -1), DURUM["tartisma"][0]), ("TEXTCOLOR", (9, 1), (9, -1), GRI),
          ("FONTNAME", (1, -1), (-1, -1), "SansB"), ("LINEABOVE", (0, -1), (-1, -1), 0.8, MUREKKEP)]
    hikaye.append(tablo(satir, [GEN * 0.235] + [GEN * 0.085] * 9, ek=ek))

    CIKTI.parent.mkdir(parents=True, exist_ok=True)
    doc.build(hikaye)
    print(CIKTI, len(toplanan), uretilen)


if __name__ == "__main__":
    main()
