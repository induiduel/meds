#!/usr/bin/env python3
"""Patoloji ders PDF'inden önem adayları + çeldirici havuzu çıkarır (LLM yok; hocanın soru mantığı: docs/PATOLOJI_HOCA_SORU_MANTIGI.md).

  meds/.venv-ocr/bin/python -I scripts/patoloji_soru_isci/hazirla.py <ders.pdf> <cikti_klasoru> [--n 12]

Çıktı <klasör>/paket.json:
  onem_adaylari : [{id, sayfa, metin, tur, puan, gerekce[], kirmizi, kalin}]  (puan büyükten küçüğe; sarı dolgu YAPI ETİKETİ olarak kullanılır (etiket altı satır +14); başlık puana girmez)
  ifade_havuzu  : {sayfa: [kısa kırmızı/kalın ifadeler]}  → çeldirici kaynağı (yalnız aynı dersin komşu kavramları)
  sozcukler     : dersin anlamlı sözcük kümesi (dogrula.py çeldirici denetimi)
Biçim yalnız EK kanıttır (kırmızı +8, kalın +6); asıl puan içerik türünden gelir (ad/ayırıcı/mekanizma/sonuç/en-üstünlük).
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
import pymupdf

TUR = [
  ("ad", re.compile(r"\((?:[A-ZÇĞİÖŞÜ][a-zçğıöşü’']+[–\-][A-ZÇĞİÖŞÜ][a-zçğıöşü’']+(?:\s(?:sendromu|hastalığı|tümörü))?|(?:[A-ZÇĞİÖŞÜ][a-zçğıöşü’']+\s){1,2}(?:sendromu|hastalığı|tümörü|nodülleri|cisimcikleri|lezyonu|fenomeni))\)"), 26),
  ("en_ustunluk", re.compile(r"en sık|en önemli|en tipik|karakteristik|patognomonik|tanı koydurucu|ayırt edici|klasik|tipik", re.I), 22),
  ("ayirici", re.compile(r"ayırt|aksine|yerine|farklı olarak|\byok\b|kaybı|yalnız|sadece|karşın|buna karşı", re.I), 20),
  ("mekanizma", re.compile(r"→|sonra|ardından|aktivasyon|salınım|basamak|sırasıyla", re.I), 18),
  ("sonuc", re.compile(r"sonucu|neden olur|gelişir|ile sonuçlan|zemin|artar|azalır|yol açar|çözünmez", re.I), 16),
  ("siniflama", re.compile(r"alt tip|tipleri|türleri|sınıflama|evre|derece|grup", re.I), 12),
]

ETIKET = re.compile(r"ancak|istisna|sonuç|not\b|çözünmezse|örnek|dikkat|önemli|klinik|tanı|ayırıcı|tipleri|alt tip", re.I)

def tok(s: str) -> set[str]:
    s = s.lower().replace("İ", "i").replace("I", "ı")
    return set(re.findall(r"[a-zçğıöşü0-9\-]{5,}", s))

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("pdf", type=Path); ap.add_argument("cikti", type=Path); ap.add_argument("--n", type=int, default=12)
    a = ap.parse_args()
    doc = pymupdf.open(a.pdf)
    satirlar, havuz, sozcuk = [], {}, set()
    onceki_etiket = False
    for p in doc:
        hl = [d["rect"] for d in p.get_drawings() if d.get("fill") and d["fill"][0] > .95 and d["fill"][1] > .95 and d["fill"][2] < .2 and d["rect"].height < 45]
        for b in p.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                sp = [s for s in l["spans"] if s["text"].strip()]
                if not sp: continue
                t = "".join(s["text"] for s in sp).strip(); n = sum(len(s["text"]) for s in sp)
                boy = max(s["size"] for s in sp)
                kir = sum(len(s["text"]) for s in sp if s["color"] == 0xFF0000) / n
                kal = sum(len(s["text"]) for s in sp if s["flags"] & 16 or "Bold" in s["font"]) / n
                sozcuk |= tok(t)
                r = pymupdf.Rect(l["bbox"]); sari = any(not (r & h).is_empty for h in hl)
                ct = t.lstrip("–•- ").strip()
                etiket = (sari or boy >= 24) and (ct.endswith(":") or len(ct.split()) <= 3) and bool(ETIKET.search(ct))
                if boy >= 24 or n < 12:
                    onceki_etiket = onceki_etiket or etiket; continue   # başlık ve kırıntı satırlar
                satirlar.append((p.number + 1, ct, kir, kal, sari, onceki_etiket)); onceki_etiket = False
                if kir >= 0.5 or kal >= 0.5:
                    k = re.sub(r"\s+", " ", t.lstrip("–•- ")).strip(" .:;")
                    if 1 <= len(k.split()) <= 8: havuz.setdefault(str(p.number + 1), []).append(k)
    aday = []
    tumtok = [(i, tok(x[1])) for i, x in enumerate(satirlar)]
    for si, (sayfa, t, kir, kal, sari, etk) in enumerate(satirlar):
        puan, ger, tur = 30, [], None
        for ad, rx, w in TUR:
            if rx.search(t):
                puan += w; ger.append(ad); tur = tur or ad
        isaret = bool(re.search(r"\*\*\*|ipucu|\b[A-ZÇĞİÖŞÜ]{3,}\b", t))
        mine = tumtok[si][1]
        tekrar = len(mine) >= 3 and sum(1 for j, o in tumtok if j != si and len(mine & o) / len(mine | o) >= 0.5) >= 1
        if not ger and not (etk or isaret or tekrar): continue
        if etk: puan += 14; ger.append("etiket_altı")
        if isaret: puan += 22; ger.append("açık_işaret")
        if tekrar: puan += 16; ger.append("tekrar")
        if kir >= 0.5: puan += 8; ger.append("kırmızı")
        if kal >= 0.3: puan += 10; ger.append("kalın")
        if kir >= 0.5 and kal >= 0.3 and sari: puan += 10; ger.append("üç_biçim")
        tur = tur or ("etiket_dali" if etk else "tekrar" if tekrar else "isaret")
        if "ad" in ger:
            puan += 6  # ad parantezde, olgu kırmızı: olgu verilip ad sorulur (§2.4)
        aday.append(dict(sayfa=sayfa, metin=t, tur=tur, puan=min(puan, 100), gerekce=ger, kirmizi=round(kir, 2), kalin=round(kal, 2)))
    # genişlik kuralı: sayfa başına en fazla 2 aday, toplam --n
    aday.sort(key=lambda x: -x["puan"]); secilen, sayac = [], {}
    for x in aday:
        if sayac.get(x["sayfa"], 0) >= 2: continue
        sayac[x["sayfa"]] = sayac.get(x["sayfa"], 0) + 1; secilen.append(x)
        if len(secilen) >= a.n: break
    # tek geçen ad/eponim bonusu (§2.4)
    tum = "\n".join(x[1] for x in satirlar)
    for i, x in enumerate(secilen, 1):
        x["id"] = f"o{i:02d}"
        m = TUR[0][1].search(x["metin"])
        if m and tum.count(m.group(0)) == 1: x["puan"] = min(100, x["puan"] + 14); x["gerekce"].append("tek geçen ad")
    secilen.sort(key=lambda x: -x["puan"])
    a.cikti.mkdir(parents=True, exist_ok=True)
    (a.cikti / "paket.json").write_text(json.dumps(dict(pdf=a.pdf.name, sayfa_sayisi=len(doc), onem_adaylari=secilen, ifade_havuzu=havuz, sozcukler=sorted(sozcuk)), ensure_ascii=False, indent=1))
    print(f"{a.pdf.name}: {len(secilen)} önem adayı, havuz {sum(map(len, havuz.values()))} ifade → {a.cikti/'paket.json'}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
