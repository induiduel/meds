#!/usr/bin/env python3
"""Soru çözücü — kısaltma okunuşu: harf adı dizilerini ünlüsü uzatılmış harf adlarına çevirir ("de ne a" → "dee nee aa").

Neden (2026-10-17, ölçüm): EMA birleşik yazılan diziyi kelime gibi okuyor ("denea" → konuşma tanımada "deneye"); ayrık "de ne a"da
son harf sonraki sözcüğe yapışıyor ("ahsarı"). Ünlüsü uzatılmış harf adlarında (dee nee aa, aa cee tee haa, tee pee elli üç)
Whisper-medium ACTH, BRCA1, DCIS, ER/PR, IgG, MHC, TNF, TP53, VHL'yi harf harf doğru tanıdı. Kullanıcının istediği okunuş: "DeNeAA".

Dizi tespiti okunus.py'nin kuralıyla (hece dizisinin harfleri gerçek bir kısaltma olmalı; "ve/de/ne" bağlaçları korunur); kısaltma
kümesi = ders kaynaklarındaki kısaltmalar ∪ aynı sorunun ekrandaki metninde geçen kısaltmalar. Yalnız seslendirmeye giden metne uygulanır.
Kullanım: kisaltma_ses.py "metin"  |  python3 -c 'import kisaltma_ses as k; print(k.uzat(s, k.metin_kisaltmalari(m)))'
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "sesli_anlatim"))
import okunus as O  # noqa: E402

# harf → uzun okunuş (Türkçe harf adı, ünlü iki kez)
UZUN = {"A": "aa", "B": "bee", "C": "cee", "Ç": "çee", "D": "dee", "E": "ee", "F": "fee", "G": "gee", "H": "haa", "I": "ıı",
        "J": "jee", "K": "kaa", "L": "lee", "M": "mee", "N": "nee", "O": "oo", "Ö": "öö", "P": "pee", "R": "ree", "S": "see",
        "Ş": "şee", "T": "tee", "U": "uu", "Ü": "üü", "V": "vee", "Y": "yee", "Z": "zee", "Q": "kuu", "X": "iks"}
_I = {"i": "ii", "i̇": "ii", "ı": "ıı"}  # HARF "i"→"I" verir; okunuşta i/ı ayrımı korunur


def metin_kisaltmalari(*metinler: str) -> set[str]:
    """Ekrandaki metinde geçen kısaltmalar (CD4 → CD, IgG → IGG, BRCA1 → BRCA, HER2 → HER)."""
    k = set()
    for m in metinler:
        for w in re.findall(r"[A-Za-zÇĞİÖŞÜçğıöşü]+", m or ""):
            if 2 <= len(w) <= 8 and sum(c.isupper() for c in w) >= 2:
                k.add(w.upper().replace("İ", "I"))
    return k


def _uzun(hece: str) -> str:
    h = O.tr_lower(hece)
    return _I.get(h) or UZUN.get(O.HARF[h], h)


def uzat(metin: str, ek_kume: set[str] | None = None) -> str:
    K = O.kume() | (ek_kume or set())
    es = list(O.SOZ.finditer(metin))
    out, son, i = [], 0, 0
    while i < len(es):
        bul = O._en_iyi(metin, es, i, K)
        if bul:
            sonraki = O._en_iyi(metin, es, i + 1, K) if i + 1 < len(es) else None
            if sonraki and (sonraki[0] > bul[0] or (sonraki[0] == bul[0] and bul[1][0] in O.BAGLAC and (bul[1][0] != "ve" or len(bul[1]) < 4))):
                bul = None
        if bul:
            j, heceler, ek = bul
            s = " ".join(_uzun(h) for h in heceler)
            if es[i].group(0)[:1].isupper():
                s = s[:1].upper() + s[1:]
            ek = ek.lstrip("'’")
            bas, bit = es[i].start(), es[j - 1].end()
            out.append(metin[son:bas] + s + (" " + ek if ek else ""))
            son, i = bit, j
        else:
            i += 1
    out.append(metin[son:])
    return "".join(out)


if __name__ == "__main__":
    print(uzat(" ".join(sys.argv[1:]), metin_kisaltmalari(" ".join(sys.argv[1:]).upper())))
