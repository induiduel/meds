"""Kurul 1 2026-2027 çıkmış sorularını ders notlarıyla eşleştirir → data/cikmis_2627/kurul1_2627.json

Kullanım: python3 scripts/cikmis_2627/eslestir.py   (sonra uret.py PDF'i bu JSON'dan üretir)
Ders notları: meds_database_v2/ders_notlari_k1 (index.json + notlar/*.md). Eşleşme önce sorunun kendi dersindeki
notlarda aranır; ELLE sözlüğü otomatik eşleşmeyi geçersiz kılar.
"""
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sorular import DERSLER, S, grup_pdf_disi, sik_isareti  # noqa: E402

KOK = Path(__file__).resolve().parents[2]
NOTLAR = KOK.parent / "meds_database_v2" / "ders_notlari_k1"
CIKTI = KOK / "data" / "cikmis_2627" / "kurul1_2627.json"

# Sınavdaki ders adı → ders notu dizinindeki ders adı
DERS_ESLE = {"Patoloji": "Tıbbi Patoloji", "Farmakoloji": "Tıbbi Farmakoloji"}
# Otomatik eşleşmenin yanıldığı sorular: kökte geçen parça → ders notu sırası
# (ders notundaki terim ve geçmiş yılların çıkmış sorularındaki konu etiketiyle doğrulandı)
ELLE = {
    "minör anomali": 1, "ense saydamlığı": 35, "Alfa-Fetoprotein": 31, "akılcı antibiyotik": 21,
    "anneden doğan": 57, "Akut prostatit": 34, "Kronik enflamasyonun morfolojik": 13, "Diyabetik nefropatinin": 41,
    "Minimal Değişim": 37, "Akut piyelonefrit tanısında": 42, "Endokrin organ tümörlerinde": 28,
    "Herpes Simplex": 46, "Endometriyum hiperplazisini": 53, "Anne sütü ve bebek beslenmesi": 22,
    "tüm gebelere rutin önerilen": 23, "Terminde ve 2,5 kg": 22, "prerenal proteinüri": 51,
}


def elle(kok):
    return next((v for k, v in ELLE.items() if k in kok), None)


def yerlestir(sorular, bas, son, sira):
    """Numarası bilinenler yerinde; bilinmeyenler ders notu sırasına göre boş numaralara.

    Sınavda bir dersin soruları ders notlarının işleniş sırasını izliyor (ör. patolojide 35 → not 02 … 68 → not 66).
    Her bilinmeyen soru, notu sırası en az kendisininki kadar olan ilk bilinen sorudan önceki boş numaraya konur.
    """
    yer = {q[0]: (q, True) for q in sorular if q[0]}
    bilinen = sorted((n, sira(q)) for n, (q, _) in yer.items())
    onceki = bas - 1
    for q in sorted((q for q in sorular if not q[0]), key=sira):
        bos = [n for n in range(onceki + 1, son + 1) if n not in yer]
        sinir = next((n for n, s in bilinen if n > onceki and s >= sira(q)), son + 1)
        uygun = [n for n in bos if n < sinir] or bos or [n for n in range(bas, son + 1) if n not in yer]
        yer[uygun[0]] = (q, False)
        onceki = uygun[0]
    return yer


DUR = set("ve ile bir bu için olan olarak aşağıdakilerden hangisi hangisidir değildir doğrudur yanlıştır en daha "
          "ilgili ifadelerden durumlardan gibi veya ise de da ki çok az sonra önce olur olması".split())


def katla(s):
    s = s.lower().translate(str.maketrans("çğıöşüâîû", "cgiosuaiu"))
    return [w[:5] for w in re.findall(r"[a-z0-9]+", s) if len(w) > 2 and w not in DUR]


def main():
    dizin = json.loads((NOTLAR / "index.json").read_text())
    notlar = []
    for d in dizin:
        satirlar = (NOTLAR / d["dosya"]).read_text().splitlines()
        notlar.append({**d, "satirlar": satirlar, "kokler": Counter(katla(" ".join(satirlar)))})
    df = Counter(k for n in notlar for k in n["kokler"])
    idf = {k: math.log(len(notlar) / v) for k, v in df.items()}

    def puanla(n, sorgu):
        return sum(idf.get(k, 0) * min(n["kokler"][k], 3) ** 0.5 for k in set(sorgu) if k in n["kokler"])

    def kanit(n, sorgu, adet=2):
        s = set(sorgu)
        aday = []
        for i, sat in enumerate(n["satirlar"]):
            if len(sat) < 25 or sat.startswith("#"):
                continue
            p = sum(idf.get(k, 0) for k in set(katla(sat)) & s)
            aday.append((p, i))
        aday.sort(reverse=True)
        return [{"satir": i + 1, "metin": n["satirlar"][i].strip()[:400], "puan": round(p, 1)} for p, i in aday[:adet] if p > 0]

    def esle(ad, kok, siklar, cevap):
        dogru = siklar["ABCDE".index(cevap)] if siklar and cevap in "ABCDE" else cevap
        sorgu = katla(kok) * 2 + katla(dogru) * 2 + katla(" ".join(siklar))
        hedef = DERS_ESLE.get(ad, ad)
        adaylar = sorted(((puanla(n, sorgu) * (1.0 if n["ders"] == hedef else 0.55), n) for n in notlar),
                         key=lambda x: -x[0])
        secilen = next(n for n in notlar if n["sira"] == elle(kok)) if elle(kok) else adaylar[0][1]
        return secilen, adaylar, sorgu

    kayitlar = []
    for ad, bas, son in DERSLER:
        esler = {id(q): esle(ad, q[1], q[2], q[3]) for q in S[ad]}
        yer = yerlestir(S[ad], bas, son, lambda q: esler[id(q)][0]["sira"])
        for no in range(bas, son + 1):
            if no not in yer:
                kayitlar.append({"kurul": 1, "yil": "2026-2027", "sinav_no": no, "ders": ad, "durum": "toplanmadi"})
                continue
            (_, kok, siklar, cevap, notu), kesin = yer[no]
            secilen, adaylar, sorgu = esler[id(yer[no][0])]
            uretildi = bool(notu and "ders notundan üretildi" in notu)
            kayitlar.append({
                "kurul": 1, "yil": "2026-2027", "sinav_no": no, "sinav_no_kesin": kesin, "ders": ad,
                "konu": secilen["title"], "ders_notu_id": secilen["id"], "ders_notu_sira": secilen["sira"],
                "ogretim_uyesi": secilen["ogretim_uyesi"],
                "durum": "kismi" if not siklar else ("siklar_uretildi" if uretildi else "tam"),
                "tartismali": bool(notu and "artışmalı" in notu),
                "kok": kok, "siklar": siklar, "cevap": cevap, "not": notu,
                "grup_pdfinde": not grup_pdf_disi(kok), "grup_pdf_disi_dayanak": grup_pdf_disi(kok),
                "sik_isaretleri": {"uretildi": list(sik_isareti(kok).get("uretildi", "")),
                                   "supheli": list(sik_isareti(kok).get("supheli", ""))},
                "eslesme": {
                    "yontem": "elle" if elle(kok) else "otomatik",
                    "puan": round(adaylar[0][0], 1),
                    "ikinci_aday": {"id": adaylar[1][1]["id"], "puan": round(adaylar[1][0], 1)},
                    "kanit": kanit(secilen, sorgu),
                },
                "kaynak": "derleme PDF'i + Konu çalışma grubu (WhatsApp, 23.10 10:00 – 24.10 15:25)",
            })
    CIKTI.parent.mkdir(parents=True, exist_ok=True)
    CIKTI.write_text(json.dumps({"kurul": 1, "yil": "2026-2027", "dersler": [list(d) for d in DERSLER],
                                 "sorular": kayitlar}, ensure_ascii=False, indent=1))
    print(CIKTI, len([k for k in kayitlar if k["durum"] != "toplanmadi"]))


if __name__ == "__main__":
    main()
