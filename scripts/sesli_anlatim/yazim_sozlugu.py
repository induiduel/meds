#!/usr/bin/env python3
"""Sesli ders ekran yazımı sözlüğü — konuşma metni okunuşla yazılır, ekranda doğru yazım gösterilir (kullanıcı, 2026-10-22).

  kisaltma: okunuş → yazım   "beta ha ce ge" → "β-hCG", "de ne a" → "DNA" (büyük/küçük harf ders kaynağındaki en sık biçim)
  acilim:   açılım → kısaltma "plazminojen aktivatörü" → "t-PA": ekranda açılımın ardına "(t-PA)" eklenir (kaynakta
            "… (t-PA)" biçiminde geçen ve konuşma metinlerinde kullanılan açılımlar)

Ses ve saklanan metin değişmez; dönüşüm ekranda (src/services/sayiYazim.ts → ekranYazimi) yapılır.
Kullanım: yazim_sozlugu.py   (src/data/sesli_anlatim/yazim_sozlugu.json üretir)
"""
from __future__ import annotations

import collections
import glob
import json
import re
from pathlib import Path

import okunus as O

MEDS = Path(__file__).resolve().parents[2]
CIKTI = MEDS / "src/data/sesli_anlatim/yazim_sozlugu.json"
YUNAN = {"alfa": "α", "beta": "β", "gama": "γ", "gamma": "γ", "delta": "δ", "epsilon": "ε", "kappa": "κ", "lambda": "λ"}


# kaynakta "(…)" biçiminde geçmeyen ama yaygın açılımlar (kullanıcı örnekleri, 2026-10-22)
EL_ACILIM = {"doku plazminojen aktivatörü": "t-PA", "glikoprotein ib": "Gp Ib", "glikoprotein iib/iiia": "Gp IIb/IIIa",
             "von willebrand faktörü": "vWF", "insan koryonik gonadotropini": "hCG"}


# okunuşu kaynaktan türetilemeyen yazımlar (çok sözcüklü / sayı üslü; k1-51 V2, 2026-10-23)
EL_KISALTMA = {"ce re pe": "CRP", "pe ha": "pH", "ha ı ve": "HIV", "e koli": "E. coli", "hepatit be": "hepatit B",
               "pe fimbriya": "P fimbriya", "tamm horsfall": "Tamm-Horsfall",
               "on üzeri beş": "10⁵", "on üzeri dört": "10⁴", "on üzeri üç": "10³",
               # patoloji V2 okunuşları (2026-10-23)
               "anka": "ANCA", "pe i ka üç ce a": "PIK3CA", "ka ras": "KRAS", "i ge a": "IgA", "i ge ge": "IgG",
               "i ge e": "IgE", "i ge em": "IgM", "pe i üç ka": "PI3K", "pe i üç kinaz": "PI3 kinaz",
               "e er": "ER", "pe er": "PR", "a ef pe": "AFP", "pe de el bir": "PD-L1",
               "pe em el ra ra": "PML-RARA", "e em el dört alk": "EML4-ALK", "pe de ge ef": "PDGF", "be ce ar abl": "BCR-ABL",
               "be ce er abl": "BCR-ABL", "ef se epsilon": "Fcε", "se te el a": "CTLA", "en a pe ku i": "NAPQI", "e te es": "ETS",
               "be ka": "BK", "a le amiloid": "AL amiloid", "a a amiloid": "AA amiloid", "a le ve a a": "AL ve AA",
               "pe de bir": "PD-1", "se te el a dört": "CTLA-4", "se te el a dörde": "CTLA-4'e", "se te el a dörttür": "CTLA-4'tür",
               "ce te el a dört": "CTLA-4", "ce de kırka": "CD40'a", "ce a on dokuz dokuz": "CA 19-9", "te em pe ar es es iki": "TMPRSS2"}


ELE = {"germinal vezikül varlığı", "tetanoz bağışıklaması", "fingolimod hidroklorür", "nitrik oksit sentaz", "glatiramer asetat"}


def kaynak_metni() -> str:
    return "\n".join(open(f, encoding="utf-8", errors="ignore").read()
                     for f in glob.glob(str(O.KAYNAK / "**/*.md"), recursive=True))


def main():
    kaynak = kaynak_metni()
    biçim: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    for t in re.findall(r"[α-ωA-Za-zÇĞİÖŞÜçğıöşü0-9]+(?:-[A-Za-z0-9]+)*", kaynak):
        if sum(c.isupper() for c in t) >= 1 and re.search(r"[A-Za-z]", t):
            biçim[re.sub(r"[^A-Za-z]", "", t).upper()][t] += 1
    metinler = [open(f, encoding="utf-8").read() for f in sorted(glob.glob(str(MEDS / "data/sesli_anlatim/metin/*.md")))]

    kisa: dict[str, str] = {}
    for m in metinler:
        kayit: list = []
        # FONETIK_TTS'siz yalnız hece dizisi: okunus.duzelt FONETIK uyguladığı için _en_iyi'yi doğrudan yürüt
        K = O.kume()
        es = list(O.SOZ.finditer(m))
        i = 0
        while i < len(es):
            bul = O._en_iyi(m, es, i, K)
            if bul:
                sonraki = O._en_iyi(m, es, i + 1, K) if i + 1 < len(es) else None
                if sonraki and (sonraki[0] > bul[0] or (sonraki[0] == bul[0] and bul[1][0] in O.BAGLAC and (bul[1][0] != "ve" or len(bul[1]) < 4))):
                    bul = None
            if not bul:
                i += 1
                continue
            j, heceler, ek = bul
            anahtar = "".join(O.HARF[h] for h in heceler)
            adaylar = biçim.get(anahtar)
            if adaylar and len(heceler) >= 2 and not (len(heceler) == 2 and set(heceler) & {"o", "e", "a", "de"}):
                # rakamlı biçim ("TP53") okunuşun ardındaki sayıyı da içerir: harf kısmı alınır, rakam sayı geçişinden gelir
                # ve ekranda "bitisik" listesiyle birleşir ("te pe elli üç" → "TP 53" → "TP53"; eskiden "TP53 53")
                yazim = adaylar.most_common(1)[0][0]
                if re.search(r"\d$", yazim):
                    alt = [t for t, _ in adaylar.most_common() if re.fullmatch(r"[A-Za-z]+", t) and sum(c.isupper() for c in t) >= 2]
                    yazim = alt[0] if alt else re.sub(r"-?\d+$", "", yazim)
                okun = " ".join(heceler)
                # önceki sözcük Yunan harfiyse ("beta ha ce ge") ve kaynakta "β-hCG" geçiyorsa birlikte
                once = O.tr_lower(es[i - 1].group(0)) if i else ""
                if once in YUNAN:
                    yb = [t for t in adaylar if t.startswith(YUNAN[once])]
                    if not yb and f"{YUNAN[once]}-{yazim}" in kaynak:
                        yb = [f"{YUNAN[once]}-{yazim}"]
                    if yb:
                        kisa[f"{once} {okun}"] = yb[0] if "-" in yb[0] or yb[0][1:2] == "-" else yb[0]
                kisa.setdefault(okun, yazim)
            i = j

    # açılım (KISALTMA)
    toplam = O.tr_lower("\n".join(metinler))
    acilim: dict[str, str] = {}
    for m in re.finditer(r"((?:[A-Za-zÇĞİÖŞÜçğıöşü\-]+ ){1,6}?[A-Za-zÇĞİÖŞÜçğıöşü\-]+)\s*\(([A-Za-zα-ω][A-Za-z0-9α-ω\-]{1,11})\)", kaynak):
        ab = m.group(2)
        buyuk = [c for c in ab if c.isupper()]
        if len(buyuk) < 2 and not (len(buyuk) == 1 and len(ab) <= 3):
            continue
        sozler = m.group(1).split()
        for n in range(min(6, len(sozler)), 0, -1):
            ifade = O.tr_lower(" ".join(sozler[-n:]))
            ilk = {w[0].upper() for w in ifade.split()}
            harf = {O.tr_lower(c) for c in ab if c.isalpha()} | {"ç" if c == "C" else c for c in []}
            bas = ifade.split()[0]
            # baştaki sözcük kısaltmanın bir harfiyle başlamalı ("kısmında dikkat …", "ya da germinal …" elenir)
            if bas[0] not in harf and not (bas[0] in "çşğıöü" and {"ç": "c", "ş": "s", "ğ": "g", "ı": "i", "ö": "o", "ü": "u"}[bas[0]] in harf):
                continue
            if bas in {"ve", "ya", "da", "de", "en", "ile", "veya"}:
                continue
            eksik = len(set(buyuk)) - sum(c in ilk for c in set(buyuk))
            if len(ifade) < 8 or eksik > (1 if len(set(buyuk)) >= 4 else 0) or ifade.split()[0][0].upper() != buyuk[0].replace("İ", "I"):
                continue
            if re.search(rf"(?<![a-zçğıöşü]){re.escape(ifade)}", toplam):
                acilim.setdefault(ifade, ab)
                break

    for k in [k for k, v in acilim.items() if re.search(r"\d", v) or k in ELE]:
        del acilim[k]
    acilim.update(EL_ACILIM)
    kisa.update(EL_KISALTMA)
    CIKTI.parent.mkdir(parents=True, exist_ok=True)
    # rakamla bitişik yazılan kısaltmalar (TP53, HER2, BRCA1, C3, CD4, Ki-67): ekranda "TP 53" → "TP53"
    # aynı kısaltmanın en sık biçimi seçilir ("BCL-2" mi "BCL2" mi kaynaktaki sıklığa göre)
    bsay = collections.Counter(t for t in re.findall(r"(?<![A-Za-z0-9])[A-Za-z]{1,6}-?\d{1,3}[a-z]?(?![A-Za-z0-9])", kaynak)
                               if sum(c.isupper() for c in t) >= 1)
    enc: dict[str, str] = {}
    for t, _ in bsay.most_common():
        enc.setdefault(t.replace("-", "").upper(), t)
    bitisik = sorted(enc.values())
    veri = {"yunan": YUNAN, "harf": O.HARF, "bitisik": bitisik,
            "kisaltma": sorted(kisa.items(), key=lambda x: -len(x[0])),
            "acilim": sorted(acilim.items(), key=lambda x: -len(x[0]))}
    CIKTI.write_text(json.dumps(veri, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(len(kisa), "kısaltma,", len(acilim), "açılım →", CIKTI)


if __name__ == "__main__":
    main()
