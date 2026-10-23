"""Tıbbi varlık çıkarıcı (betik; model yok) — PDF sayfası ile çıkmış sorusunu aynı dilde eşlemek için (§15.1).

Kaynaklar: `src/data/medical_glossary.json` (terim, kısaltma), `src/data/diseases.json` (ad, Latince ad).
Varlık biçimi: `t:<katlanmış terim>` (sözlük/hastalık), `k:<KISALTMA>` (2–6 büyük harf), `s:<sayı><birim>`.
Eşleme katlanmış sözcük n-gramlarıyla (1–5); 4 harften kısa terim yalnız büyük harfli kısaltma olarak sayılır.
"""
from __future__ import annotations

import re
from functools import lru_cache

from ortak import KOK, katla, oku, sozcukler

BIRIM = r"(?:mg/dl|mg/kg|mmhg|mmol|meq|mg|ml|µg|mcg|kg|cm|mm|µm|nm|iu|ü|%|gün|hafta|ay|yıl|yaş|saat|dk|dakika|sn|saniye)"
SAYI_BIRIM = re.compile(rf"(\d+(?:[.,]\d+)?)\s?({BIRIM})(?![a-zçğıöşü])", re.I)
YUZDE = re.compile(r"%\s?(\d+(?:[.,]\d+)?)")
KISALTMA = re.compile(r"(?<![A-Za-zÇĞİÖŞÜçğıöşü])([A-ZÇĞİÖŞÜ][A-ZÇĞİÖŞÜ0-9]{1,5})(?![A-Za-zÇĞİÖŞÜçğıöşü])")
GENEL = set("ve ile hücre doku organ tedavi tanı hasta klinik bulgu belirti neden sonuç tip grup sınıf durum hastalık "
            "risk faktör artış azalma etki yapı fonksiyon işlev".split())


def _ekle(sozluk: dict, ad: str):
    ana = re.sub(r"\(.*?\)", " ", ad or "")
    w = [katla(x) for x in sozcukler(ana)]
    if w and (len(w) > 1 or len(w[0]) >= 4) and " ".join(w) not in GENEL:
        sozluk[" ".join(w)] = " ".join(w)
    for ic in re.findall(r"\((.*?)\)", ad or ""):
        if re.fullmatch(r"[A-Za-z0-9-]{2,8}", ic.strip()) and any(ch.isupper() for ch in ic):
            sozluk.setdefault(f"#K#{ic.strip().upper()}", " ".join(w))   # kısaltma → ana terim


@lru_cache(maxsize=1)
def sozluk() -> tuple[dict, int]:
    s: dict[str, str] = {}
    g = oku(KOK / "src" / "data" / "medical_glossary.json", {}) or {}
    for k, v in g.items():
        _ekle(s, (v or {}).get("term") or k)
    for h in oku(KOK / "src" / "data" / "diseases.json", []) or []:
        _ekle(s, h.get("name", ""))
        if h.get("latinName"):
            _ekle(s, h["latinName"])
    uzun = max((len(k.split()) for k in s if not k.startswith("#K#")), default=1)
    return s, min(uzun, 5)


def cikar(metin: str) -> set[str]:
    s, n = sozluk()
    out: set[str] = set()
    w = [katla(x) for x in sozcukler(metin)]
    for i in range(len(w)):
        for k in range(1, n + 1):
            if i + k > len(w):
                break
            p = " ".join(w[i:i + k])
            if p in s:
                out.add(f"t:{s[p]}")
    for m in KISALTMA.finditer(metin or ""):
        ab = m.group(1)
        if ab.isdigit() or len(set(ab)) == 1:
            continue
        out.add(f"k:{ab.upper()}")
        if f"#K#{ab.upper()}" in s:
            out.add(f"t:{s['#K#' + ab.upper()]}")
    for m in SAYI_BIRIM.finditer(metin or ""):
        out.add(f"s:{m.group(1).replace(',', '.')}{katla(m.group(2))}")
    for m in YUZDE.finditer(metin or ""):
        out.add(f"s:{m.group(1).replace(',', '.')}%")
    return out
