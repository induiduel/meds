"""Kurul 1 2026-2027 çıkmış soruları PDF'i → data/cikmis_2627/kurul1_2627.pdf

Kullanım: python3 scripts/cikmis_2627/uret.py
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
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Frame, Image, KeepTogether, NextPageTemplate, PageBreak,
                                PageTemplate, Paragraph, Spacer, Table, TableStyle)

sys.path.insert(0, str(Path(__file__).parent))
from sorular import DERSLER, S, grup_pdf_disi, sik_isareti  # noqa: E402

KOK = Path(__file__).resolve().parents[2]
CIKTI = KOK / "data" / "cikmis_2627" / "kurul1_2627.pdf"
ESLESME = KOK / "data" / "cikmis_2627" / "kurul1_2627.json"  # eslestir.py üretir
KTG = KOK / "data" / "cikmis_2627" / "ktg.jpeg"

FONT = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", FONT + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", FONT + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVI", FONT + "DejaVuSans-Oblique.ttf"))

H = colors.HexColor
MUREKKEP, GRI, SOLUK, CIZGI, ZEMIN = H("#1c1917"), H("#57534e"), H("#a8a29e"), H("#e7e5e4"), H("#fafaf9")
# Renk yalnız durumu gösterir; ders başlıkları ve sorular siyah-beyazdır.
DURUM = {
    "emin": (H("#15803d"), "CEVAP DOĞRULANDI"),
    "tartisma": (H("#b91c1c"), "TARTIŞMALI"),
    "eksik": (H("#b91c1c"), "ŞIK EKSİK"),
    "eklendi": (H("#1d4ed8"), "SONRADAN EKLENDİ"),
    "uretildi": (H("#1d4ed8"), "ŞIKLAR ÜRETİLDİ"),
    "tahmini": (H("#b45309"), "YERİ TAHMİNİ"),
    "kismi": (H("#78716c"), "HATIRLANMADI"),
}
URETILDI = "ders notundan üretildi"

SAYFA_G, SAYFA_Y = A4
KENAR, ARA = 13 * mm, 7 * mm
SUTUN = (SAYFA_G - 2 * KENAR - ARA) / 2
UST_ILK, UST, ALT = 82 * mm, 16 * mm, 15 * mm


def st(ad, **k):
    k.setdefault("fontName", "DV"); k.setdefault("textColor", MUREKKEP)
    return ParagraphStyle(ad, **k)


st_konu = st("konu", fontSize=6.6, leading=8.6, textColor=GRI, spaceAfter=2)
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
    return " ".join(f'<font name="DVB" size="6.3" color="{DURUM[t][0].hexval()}">[{DURUM[t][1]}]</font>' for t in turler)


def durumlar(siklar, notu, kesin):
    n = notu or ""
    t = ([] if kesin else ["tahmini"]) + ([] if siklar else ["kismi"])
    t += ["uretildi"] if URETILDI in n else (["eklendi"] if "24.10 eklendi" in n else [])
    t += ["eksik"] if "Şık eksik" in n or "hatırlanmadı" in n.split(".")[0] else []
    t += ["tartisma"] if "artışmalı" in n else []
    if siklar and not {"tartisma", "eksik", "uretildi", "eklendi"} & set(t):
        t.append("emin")
    return t


def ana_renk(t):
    """Kart kenarı ve cevap rengi: en önemli durumun rengi."""
    for k in ("tartisma", "eksik", "uretildi", "eklendi", "emin", "kismi"):
        if k in t:
            return DURUM[k][0]
    return MUREKKEP


def ders_basligi(ad, bas, son, n):
    t = Table([[p(ad, st_ders), p(f"Soru {bas}–{son}\n{n}/{son - bas + 1} toplandı", st_ders_alt)]],
              colWidths=[SUTUN * 0.62, SUTUN * 0.38])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), MUREKKEP), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("ALIGN", (1, 0), (1, 0), "RIGHT"), ("LEFTPADDING", (0, 0), (-1, -1), 7),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 0), (-1, -1), 5),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 5), ("ROUNDEDCORNERS", [3, 3, 3, 3])]))
    return t


def soru_karti(ders, no, kok, siklar, cevap, notu, kesin, konu=None):
    turler = durumlar(siklar, notu, kesin)
    renk = ana_renk(turler)
    baslik = f'<font name="DVB">{no}.</font> {escape(kok).replace(chr(10), "<br/>")}' + "<br/>" + rozetler(turler)
    icerik = []
    if konu:
        icerik.append(Paragraph(f'<font name="DVB">KURUL 1</font>  ·  {escape(ders)}  ·  {escape(konu)}', st_konu))
    icerik += [Paragraph(baslik, st_kok), Spacer(1, 1.6 * mm)]
    if "NST trasesi" in kok and KTG.exists():
        en = SUTUN - 14
        icerik += [Image(str(KTG), width=en, height=en * 336 / 644), Spacer(1, 1.6 * mm)]
    if siklar:
        isaret = sik_isareti(kok)
        for j, s in enumerate(siklar):
            harf, metin = "ABCDE"[j], escape(s)
            for tur in ("supheli", "uretildi"):
                if harf in isaret.get(tur, ""):
                    r = DURUM["tartisma" if tur == "supheli" else "uretildi"][0].hexval()
                    metin = f'<u><font color="{r}">{metin}</font></u>'
                    break
            icerik.append(Paragraph(f'<font name="DVB">{harf})</font> {metin}', st_sik))
        dogru = f'{cevap}) {siklar["ABCDE".index(cevap)]}' if cevap in "ABCDE" else cevap
    else:
        icerik.append(Paragraph("Şıklar toplanmadı.", st_sik))
        dogru = cevap if cevap != "?" else "belirlenemedi"
    icerik += [Spacer(1, 1.4 * mm), Paragraph(f'<font name="DVB" color="{renk.hexval()}">Tahmini cevap:</font> '
                                              f'<font color="{renk.hexval()}">{escape(dogru)}</font>', st_sik)]
    satirlar = [[icerik]]
    if notu:
        not_t = Table([[Paragraph(f'<font name="DVB">Not</font>  {escape(notu)}', st_not)]], colWidths=[SUTUN - 14])
        not_t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), ZEMIN), ("LEFTPADDING", (0, 0), (-1, -1), 5),
                                   ("RIGHTPADDING", (0, 0), (-1, -1), 5), ("TOPPADDING", (0, 0), (-1, -1), 3),
                                   ("BOTTOMPADDING", (0, 0), (-1, -1), 3), ("ROUNDEDCORNERS", [2, 2, 2, 2])]))
        satirlar.append([not_t])
    t = Table(satirlar, colWidths=[SUTUN])
    t.setStyle(TableStyle([("LINEBEFORE", (0, 0), (0, -1), 2, renk), ("LEFTPADDING", (0, 0), (-1, -1), 7),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 4), ("TOPPADDING", (0, 0), (-1, -1), 2),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    return KeepTogether([t, Spacer(1, 3.2 * mm)])


def eksik_satiri(nolar):
    aralik = f"{nolar[0]}–{nolar[-1]}" if len(nolar) > 1 else str(nolar[0])
    t = Table([[Paragraph(f"{aralik}  ·  toplanmadı  " + rozetler(["kismi"]), st_eksik)]], colWidths=[SUTUN])
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
    hucre = []
    for no, q, kesin in kayitlar:
        if q is None:
            hucre.append((str(no), "—", DURUM["kismi"][0]))
            continue
        _, _, siklar, cevap, notu = q
        cv = cevap if siklar else ("kısmi" if cevap == "?" else "metin")
        hucre.append((str(no), cv, ana_renk(durumlar(siklar, notu, kesin))))
    sutun = 10
    satirlar, renkler = [], []
    for i in range(0, len(hucre), sutun):
        parca = hucre[i:i + sutun] + [("", "", MUREKKEP)] * (sutun - len(hucre[i:i + sutun]))
        satirlar += [[a for a, _, _ in parca], [b for _, b, _ in parca]]
        renkler.append([c for _, _, c in parca])
    gen = (SAYFA_G - 2 * KENAR) / sutun
    t = Table(satirlar, colWidths=[gen] * sutun, rowHeights=[5.2 * mm, 6.2 * mm] * (len(satirlar) // 2))
    stil = [("FONTNAME", (0, 0), (-1, -1), "DV"), ("FONTSIZE", (0, 0), (-1, -1), 7.5), ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("GRID", (0, 0), (-1, -1), 0.4, CIZGI)]
    for r in range(0, len(satirlar), 2):
        stil += [("BACKGROUND", (0, r), (-1, r), ZEMIN), ("TEXTCOLOR", (0, r), (-1, r), GRI),
                 ("FONTNAME", (0, r + 1), (-1, r + 1), "DVB"), ("FONTSIZE", (0, r + 1), (-1, r + 1), 8.5)]
        for c, renk in enumerate(renkler[r // 2]):
            stil.append(("TEXTCOLOR", (c, r + 1), (c, r + 1), renk))
    t.setStyle(TableStyle(stil))
    return t


def istatistik_bolumu(yer):
    tam_gen = SAYFA_G - 2 * KENAR
    bolum = [PageBreak(), p("Grubun PDF'inde olmayan sorular", st_h), Spacer(1, 1.5 * mm),
             p("Grubun cevap anahtarlı PDF'i (24.10 16:31, 78 soru) ile karşılaştırıldı. Aşağıdaki sorular yalnız bu "
               "derlemede var; dayanakları yanlarında yazılı.", st_kucuk), Spacer(1, 3 * mm)]
    satirlar = [["No", "Ders", "Soru", "Dayanak"]]
    for ad, _, _ in DERSLER:
        for no, q, _ in yer[ad]:
            if q and grup_pdf_disi(q[1]):
                satirlar.append([str(no), p(ad, st_not), p(q[1].split("\n")[0], st_not), p(grup_pdf_disi(q[1]), st_not)])
    t = Table(satirlar, colWidths=[10 * mm, 30 * mm, tam_gen - 105 * mm, 65 * mm], repeatRows=1)
    t.setStyle(TableStyle([("FONTNAME", (0, 0), (-1, 0), "DVB"), ("FONTSIZE", (0, 0), (-1, -1), 7.5),
                           ("BACKGROUND", (0, 0), (-1, 0), ZEMIN), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LINEBELOW", (0, 0), (-1, -1), 0.4, CIZGI), ("TOPPADDING", (0, 0), (-1, -1), 3),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    bolum += [t, Spacer(1, 8 * mm), p("İstatistikler", st_h), Spacer(1, 1.5 * mm),
              p("“Numarası kesin”: grupta sınavdaki numarasıyla yazılan sorular; bunların sınavda o numarada olduğu kesindir. "
                "“Grup PDF'inde”: grubun son PDF'inde de yer alan sorular. “Tam”: kök ve şıklar hatırlandı, cevap "
                "tartışmasız.", st_kucuk), Spacer(1, 3 * mm)]
    basliklar = ["Ders", "Sınavda", "Topla-\nnan", "Numarası\nkesin", "Grup\nPDF'inde", "Yalnız\nbizde", "Tam",
                 "Şıkları\nüretilen", "Tartış-\nmalı", "Toplan-\nmadı"]
    satirlar, toplam = [basliklar], [0] * 9
    for ad, bas, son in DERSLER:
        kay = [(q, kesin) for _, q, kesin in yer[ad] if q]
        durum = [durumlar(q[2], q[4], kesin) for q, kesin in kay]
        say = [son - bas + 1, len(kay), sum(k for _, k in kay), sum(not grup_pdf_disi(q[1]) for q, _ in kay),
               sum(bool(grup_pdf_disi(q[1])) for q, _ in kay), sum("emin" in d for d in durum),
               sum("uretildi" in d for d in durum), sum("tartisma" in d for d in durum), son - bas + 1 - len(kay)]
        toplam = [a + b for a, b in zip(toplam, say)]
        satirlar.append([ad] + [str(x) for x in say])
    satirlar.append(["Toplam"] + [str(x) for x in toplam])
    satirlar[0] = [p(x, st("ib", fontName="DVB", fontSize=6.6, leading=8.2, alignment=1 if i else 0))
                   for i, x in enumerate(basliklar)]
    t = Table(satirlar, colWidths=[40 * mm] + [(tam_gen - 40 * mm) / 9] * 9)
    t.setStyle(TableStyle([("FONTNAME", (0, 0), (-1, -1), "DV"), ("FONTSIZE", (0, 0), (-1, -1), 7.3),
                           ("FONTNAME", (0, 0), (-1, 0), "DVB"), ("FONTNAME", (0, -1), (-1, -1), "DVB"),
                           ("BACKGROUND", (0, 0), (-1, 0), ZEMIN), ("BACKGROUND", (0, -1), (-1, -1), ZEMIN),
                           ("ALIGN", (1, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("GRID", (0, 0), (-1, -1), 0.4, CIZGI), ("TOPPADDING", (0, 0), (-1, -1), 4),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                           ("TEXTCOLOR", (3, 1), (3, -1), DURUM["emin"][0]), ("TEXTCOLOR", (6, 1), (6, -1), DURUM["emin"][0]),
                           ("TEXTCOLOR", (5, 1), (5, -1), DURUM["eklendi"][0]), ("TEXTCOLOR", (7, 1), (7, -1), DURUM["uretildi"][0]),
                           ("TEXTCOLOR", (8, 1), (8, -1), DURUM["tartisma"][0]), ("TEXTCOLOR", (9, 1), (9, -1), DURUM["kismi"][0])]))
    bolum.append(t)
    return bolum


def main():
    yer = yerlestir()
    konular = {k["sinav_no"]: k["konu"] for k in json.loads(ESLESME.read_text())["sorular"] if k.get("konu")}
    toplanan = sum(len(S[a]) for a, _, _ in DERSLER)
    kismi = sum(1 for a, _, _ in DERSLER for q in S[a] if not q[2] or URETILDI in q[4])

    def ilk_sayfa(c, d):
        c.saveState()
        c.setFillColor(MUREKKEP); c.rect(0, SAYFA_Y - 52 * mm, SAYFA_G, 52 * mm, stroke=0, fill=1)
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
        kutular = [(f"{toplanan}", "toplanan / 100"), (f"{100 - toplanan}", "toplanmadı"), (f"{kismi}", "şıkları üretilen")]
        kx = SAYFA_G - KENAR - 3 * 21 * mm
        for deger, ad in kutular:
            c.setFillColor(colors.white); c.setFont("DVB", 19); c.drawCentredString(kx + 10.5 * mm, SAYFA_Y - 30 * mm, deger)
            c.setFillColor(SOLUK); c.setFont("DV", 6.6); c.drawCentredString(kx + 10.5 * mm, SAYFA_Y - 35 * mm, ad)
            kx += 21 * mm
        # işaret açıklaması
        y = SAYFA_Y - 60 * mm
        c.setFillColor(ZEMIN); c.roundRect(KENAR, y - 14.5 * mm, SAYFA_G - 2 * KENAR, 16.5 * mm, 2 * mm, stroke=0, fill=1)
        aciklama = [("emin", "Cevap ders notuyla uyumlu, tartışma yok."),
                    ("tartisma", "Cevap öğrenciler arasında kesinleşmedi; nota bakın."),
                    ("eksik", "Sorunun bazı şıkları hatırlanmadı."),
                    ("eklendi", "Soru derleme PDF'inden sonra gruptan eklendi."),
                    ("uretildi", "Eksik şıklar ders notundan üretildi."),
                    ("tahmini", "Numara yazılmadı, boş numaraya kondu."),
                    ("kismi", "Soru hatırlanmadı.")]
        for i, (tur, metin) in enumerate(aciklama):
            renk, ad = DURUM[tur]
            xx = KENAR + 4 * mm + (i // 4) * (SAYFA_G - 2 * KENAR) / 2
            yy = y - 2.5 * mm - (i % 4) * 3.4 * mm
            c.setFillColor(renk); c.setFont("DVB", 6.3); c.drawString(xx, yy, f"[{ad}]")
            c.setFillColor(GRI); c.setFont("DV", 6.6); c.drawString(xx + 30 * mm, yy, metin)
        xx, yy = KENAR + 4 * mm + (SAYFA_G - 2 * KENAR) / 2, y - 2.5 * mm - 3 * 3.4 * mm
        for renk, ornek, metin in [(DURUM["uretildi"][0], "Şık", "eklenen şık"), (DURUM["tartisma"][0], "Şık", "şüpheli şık")]:
            c.setFillColor(renk); c.setFont("DV", 6.6); c.drawString(xx, yy, ornek)
            w = c.stringWidth(ornek, "DV", 6.6); c.setStrokeColor(renk); c.setLineWidth(0.5); c.line(xx, yy - 0.8, xx + w, yy - 0.8)
            c.setFillColor(GRI); c.drawString(xx + w + 1.5 * mm, yy, metin)
            xx += 30 * mm
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
            hikaye.append(soru_karti(ad, no, kok, siklar, cevap, notu, kesin, konular.get(no)))
        if eksik:
            hikaye += eksik_satiri(eksik)
        hikaye.append(Spacer(1, 2 * mm))

    hikaye += [NextPageTemplate("tek"), PageBreak(), p("Cevap anahtarı", st_h), Spacer(1, 1.5 * mm),
               p("Cevap rengi durumu gösterir: yeşil doğrulandı, kırmızı tartışmalı / şık eksik, mavi sonradan eklendi / "
                 "şıklar üretildi, gri toplanmadı. “metin”: şık yok, cevap soru kartında. Numaraları tahmini olan "
                 "soruların yeri ders içinde değişebilir.", st_kucuk), Spacer(1, 5 * mm)]
    for ad, bas, son in DERSLER:
        hikaye += [KeepTogether([Paragraph(f'<font name="DVB">{ad}</font>'
                                           f'  <font color="{GRI.hexval()}" size="7.5">{bas}–{son}</font>',
                                           st("ah", fontSize=9.5, leading=13)),
                                 Spacer(1, 1.5 * mm), anahtar_tablosu(ad, yer[ad]), Spacer(1, 5 * mm)])]

    hikaye += istatistik_bolumu(yer)

    CIKTI.parent.mkdir(parents=True, exist_ok=True)
    doc.build(hikaye)
    print(CIKTI, toplanan, kismi)


if __name__ == "__main__":
    main()
