#!/usr/bin/env python3
"""Patoloji hoca-üslubu soru kapısı (0 HATA gerekir). Kurallar: docs/PATOLOJI_HOCA_SORU_MANTIGI.md §4.

  python3 scripts/patoloji_soru_isci/dogrula.py <sorular.json> <paket.json> [--esik 60]

sorular.json: [{onem_id, kalip, kok, siklar[5], cevap "A".."E", aciklama{A..E}, kaynak{sayfa, metin}, celdirici_kaynak[sayfa,...]}]
HATA: her önem adayı (puan ≥ eşik) ≥2 soru ve ≥2 FARKLI kalıp; 5 şık, tek doğru, kök '?'; kökte slayt/ders/hoca göndermesi yok;
      kaynak alıntı PDF sözcüklerinde; ≥3 yanlış şık aynı dersin sözcüklerinden ve celdirici_kaynak ≥3 sayfa; her şık açıklaması ≥2 cümle ve
      geçiştirme kalıbı yok; doğru şık en uzun şık değil kuralı toplamda profil.json sınırında; şık uzunluk oranı.
UYARI (profil.json hedefleri): bileşik şık payı, üstünlük kökü payı, olumsuz kök payı, kök uzunluğu.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

AD = Path(__file__).parent
YASAK_KOK = re.compile(r"slayt|derste|hocan|bu bölümde|metne göre|sayfa \d", re.I)
GECISTIRME = re.compile(r"bu sorunun cevabı değil|olarak geçmez|yapmaz\.$|\bdeğildir\.$", re.I)
BILESIK = re.compile(r"[;+→]|\bile\b|\bve\b|:")
USTUN = re.compile(r"en tipik|en karakteristik|patognomonik|en olası|en doğru|en sık|en önemli", re.I)
OLUMSUZ = re.compile(r"(değildir|yanlıştır|beklenmez|görülmez|söylenemez|dışındadır|olamaz)\??$")

def tok(s: str) -> set[str]:
    s = s.lower().replace("İ", "i").replace("I", "ı"); return set(re.findall(r"[a-zçğıöşü0-9\-]{5,}", s))

def main() -> int:
    if len(sys.argv) < 3: print(__doc__); return 2
    sor = json.loads(Path(sys.argv[1]).read_text()); sor = sor["sorular"] if isinstance(sor, dict) else sor; paket = json.loads(Path(sys.argv[2]).read_text())
    esik = int(sys.argv[sys.argv.index("--esik") + 1]) if "--esik" in sys.argv else 60
    prof = json.loads((AD / "profil.json").read_text())["hedef"]
    soz = set(paket["sozcukler"]); hata, uyari = [], []
    H = lambda i, m: hata.append(f"[{i}] {m}")
    onem = {x["id"]: x for x in paket["onem_adaylari"]}
    per: dict[str, list[dict]] = {}
    for n, q in enumerate(sor, 1):
        k = f"{q.get('onem_id','?')}#{n}"
        per.setdefault(q.get("onem_id", "?"), []).append(q)
        if q.get("onem_id") not in onem: H(k, "onem_id pakette yok")
        s = q.get("siklar", [])
        if len(s) != 5 or len({x.strip().lower() for x in s}) != 5: H(k, "5 farklı şık gerekir"); continue
        if q.get("cevap") not in list("ABCDE"): H(k, "cevap A–E"); continue
        if not q["kok"].strip().endswith("?"): H(k, "kök '?' ile bitmeli")
        if YASAK_KOK.search(q["kok"]): H(k, "kökte slayt/ders/hoca göndermesi")
        if q.get("kalip") not in json.loads((AD / "profil.json").read_text())["kalip"]: H(k, "geçersiz kalıp")
        kay = q.get("kaynak") or {}
        if not kay.get("sayfa") or len(tok(kay.get("metin", "")) - soz) > 0 or not kay.get("metin"): H(k, "kaynak alıntı yok ya da PDF sözcüklerinde bulunmuyor")
        dogru = "ABCDE".index(q["cevap"]); yanlis = [x for i, x in enumerate(s) if i != dogru]
        dis = [x for x in yanlis if not (tok(x) & soz)]
        if len(dis) > 1: H(k, f"{len(dis)} yanlış şıkta dersin hiçbir sözcüğü yok (çeldirici komşu kavramdan olmalı): {dis[:2]}")
        if len(set(q.get("celdirici_kaynak", []))) < 3: H(k, "celdirici_kaynak ≥3 farklı sayfa")
        uz = [len(x) for x in s]
        if max(uz) / max(min(uz), 1) > prof["sik_uzunluk_orani_max"] * 1.5: H(k, "şık uzunlukları çok farklı (ipucu)")
        ac = q.get("aciklama") or {}
        for h in "ABCDE":
            t = (ac.get(h) or "").strip()
            if len(re.findall(r"[.!?](\s|$)", t)) < 2: H(k, f"{h} açıklaması en az 2 cümle olmalı")
            if GECISTIRME.search(t): H(k, f"{h} açıklaması geçiştirme kalıbı")
    sab = {}
    for n, q in enumerate(sor):
        for h, t in (q.get("aciklama") or {}).items():
            c = [x for x in re.split(r"(?<=[.!?])\s+", t.strip()) if x]
            if c:
                w = re.findall(r"\w+", c[-1].lower()); sab.setdefault(" ".join(w[:3] + ["…"] + w[-2:]), []).append(f"{n}{h}")
    for k_, v in sab.items():
        if len(v) > 4: hata.append(f"[genel] açıklama sonunda aynı kalıp cümle {len(v)} kez ({k_}): şıka özgü yaz")
    for oid, x in onem.items():
        if x["puan"] < esik: continue
        qs = per.get(oid, [])
        if len(qs) < 2: H(oid, f"önem puanı {x['puan']}: en az 2 soru gerekir (var {len(qs)})")
        elif len({q.get('kalip') for q in qs}) < 2: H(oid, "iki soru FARKLI kalıpta olmalı")
        if x.get("tur") == "ad" and not any(q.get("kalip") == "ters_ad" for q in qs): H(oid, "ad/eponim noktası: olgu verilip adı soran 'ters_ad' sorusu gerekir")
    n = max(len(sor), 1)
    bil = sum(sum(bool(BILESIK.search(x)) for x in q["siklar"]) / 5 for q in sor if len(q.get("siklar", [])) == 5) / n
    ust = sum(bool(USTUN.search(q["kok"])) for q in sor) / n
    neg = sum(bool(OLUMSUZ.search(q["kok"].strip())) for q in sor) / n
    uzn = sum(max(range(5), key=lambda i: len(q["siklar"][i])) == "ABCDE".index(q["cevap"]) for q in sor if len(q.get("siklar", [])) == 5 and q.get("cevap") in list("ABCDE")) / n
    if uzn > prof["dogru_en_uzun_payi_max"]: H("genel", f"doğru şık en uzun payı %{uzn*100:.0f} > %{prof['dogru_en_uzun_payi_max']*100:.0f} (ipucu sızıntısı)")
    lo, hi = prof["bilesik_sik_payi"]
    if not lo <= bil <= hi + .15: uyari.append(f"bileşik şık payı %{bil*100:.0f} (hedef %{lo*100:.0f}–{hi*100:.0f})")
    lo, hi = prof["ustunluk_kok_payi"]
    if not lo - .1 <= ust <= hi + .15: uyari.append(f"'en tipik/en olası' kök payı %{ust*100:.0f} (hedef %{lo*100:.0f}–{hi*100:.0f})")
    if neg > prof["olumsuz_kok_payi_max"]: uyari.append(f"olumsuz kök payı %{neg*100:.0f} (üst sınır %{prof['olumsuz_kok_payi_max']*100:.0f})")
    kw = [len(q["kok"].split()) for q in sor]
    if kw and not prof["kok_kelime"][0] <= sum(kw) / len(kw) <= prof["kok_kelime"][1]: uyari.append(f"kök ort. {sum(kw)/len(kw):.1f} kelime (hedef {prof['kok_kelime']})")
    for m in hata: print("HATA", m)
    for m in uyari: print("UYARI", m)
    print(f"{len(sor)} soru, {len(hata)} HATA, {len(uyari)} UYARI")
    return 1 if hata else 0

if __name__ == "__main__":
    sys.exit(main())
