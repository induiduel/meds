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
from sorular import DERSLER, S  # noqa: E402

KOK = Path(__file__).resolve().parents[2]
NOTLAR = KOK.parent / "meds_database_v2" / "ders_notlari_k1"
CIKTI = KOK / "data" / "cikmis_2627" / "kurul1_2627.json"

# Sınavdaki ders adı → ders notu dizinindeki ders adı
DERS_ESLE = {"Patoloji": "Tıbbi Patoloji", "Farmakoloji": "Tıbbi Farmakoloji"}
# Otomatik eşleşmenin yanıldığı sorular: sınav no → ders notu sırası
ELLE = {1: 1, 4: 35, 8: 31, 22: 21, 42: 13, 50: 41, 52: 59, 54: 37, 57: 42, 58: 28, 60: 46, 63: 53, 69: 22, 72: 23, 74: 22,
        81: 51}

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

    kayitlar = []
    for ad, bas, son in DERSLER:
        sorular = S[ad]
        yer = {q[0]: (q, True) for q in sorular if q[0]}
        bos = [n for n in range(bas, son + 1) if n not in yer]
        for q, n in zip([q for q in sorular if not q[0]], bos):
            yer[n] = (q, False)
        hedef = DERS_ESLE.get(ad, ad)
        for no in range(bas, son + 1):
            if no not in yer:
                kayitlar.append({"kurul": 1, "yil": "2026-2027", "sinav_no": no, "ders": ad, "durum": "toplanmadi"})
                continue
            (_, kok, siklar, cevap, notu), kesin = yer[no]
            dogru = siklar["ABCDE".index(cevap)] if siklar and cevap in "ABCDE" else cevap
            sorgu = katla(kok) * 2 + katla(dogru) * 2 + katla(" ".join(siklar))
            adaylar = sorted(((puanla(n, sorgu) * (1.0 if n["ders"] == hedef else 0.55), n) for n in notlar),
                             key=lambda x: -x[0])
            secilen = next(n for n in notlar if n["sira"] == ELLE[no]) if no in ELLE else adaylar[0][1]
            uretildi = bool(notu and "ders notundan üretildi" in notu)
            kayitlar.append({
                "kurul": 1, "yil": "2026-2027", "sinav_no": no, "sinav_no_kesin": kesin, "ders": ad,
                "konu": secilen["title"], "ders_notu_id": secilen["id"], "ogretim_uyesi": secilen["ogretim_uyesi"],
                "durum": "kismi" if not siklar else ("siklar_uretildi" if uretildi else "tam"),
                "tartismali": bool(notu and "artışmalı" in notu),
                "kok": kok, "siklar": siklar, "cevap": cevap, "not": notu,
                "eslesme": {
                    "yontem": "elle" if no in ELLE else "otomatik",
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
