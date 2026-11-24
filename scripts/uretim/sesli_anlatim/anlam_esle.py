#!/usr/bin/env python3
"""Anlatım ↔ slayt ANLAM eşlemesi (H655, 2026-11-24).

Kök neden: hocanın sesli anlatımı slaytı birebir okumaz, başka sözcüklerle anlatır. pdf_isaret.eslestir yalnız ortak
5 harf köke bakar; ortak kök azsa cümle "sayfa"/"kelime"ye düşer ya da tek yaygın kelime yüzünden yanlış maddeye gider.
Bu modül cümleyi ve slayt maddelerini bge-m3 ile vektörler (CPU servisi meds-embed-bge :8094, GPU YOK — kural 10) ve
kelime kanıtıyla birleştirir:  puan = kosinüs + 0,04 × min(ortak kök, 4)  (+0,03 atanan sayfa).

Ayrıca w_doldur: konuşulan HER içerik kelimesine slayt maddesinde bir kelime kutusu verir. Ortak kökler sabit çapa,
aradakiler iki çapa arasında sıra korunarak oranla dağıtılır → vurgu cümle boyunca kesintisiz ilerler, "geç kalmaz".
"""
from __future__ import annotations

import os

import json
import urllib.request

import numpy as np

URL = os.environ.get("MEDS_EMBED_BGE_URL", "http://127.0.0.1:8094/embed")
ESIK = 0.52        # tek başına kabul alt sınırı (bge-m3 Türkçe, ölçüm: alakasız madde ≈ 0,30–0,45)
FARK = 0.025       # birinci ile ikinci (komşu olmayan) aday arasında en az bu fark
GUCLU = 0.66       # bu ve üstü fark aranmadan kabul

_onbellek: dict[str, np.ndarray] = {}


def vektor(metinler: list[str]) -> np.ndarray:
    eksik = [m for m in dict.fromkeys(metinler) if m not in _onbellek]
    for i in range(0, len(eksik), 64):
        parca = eksik[i:i + 64]
        q = urllib.request.Request(URL, data=json.dumps({"texts": parca, "kind": "raw"}).encode(),
                                   headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(q, timeout=600) as r:
            vek = json.load(r)["vectors"]
        for m, v in zip(parca, vek):
            a = np.asarray(v, dtype="float32")
            _onbellek[m] = a / max(float(np.linalg.norm(a)), 1e-9)
    if len(_onbellek) > 60000:
        _onbellek.clear()
    return np.stack([_onbellek[m] for m in metinler]) if metinler else np.zeros((0, 1024), "float32")


def servis_var() -> bool:
    try:
        with urllib.request.urlopen(URL.rsplit("/", 1)[0] + "/health", timeout=3) as r:
            return r.status == 200
    except Exception:
        return False


def madde_metni(md: dict) -> str:
    return " ".join(md["metin"]).strip()


def w_doldur(tk: list[tuple[str, int, int]], kutular: list[tuple[str, tuple]], capalar: list[tuple[int, int]]):
    """tk: konuşma tokenleri (kök, b, e); kutular: maddedeki slayt kelimeleri okuma sırasıyla (kök, kutu);
    capalar: kesin (token i, kutu j) eşleri. Dönüş: [(i, j)] — her token için tek kutu, i ve j artan."""
    n, m = len(tk), len(kutular)
    if not n or not m:
        return []
    cs = sorted({i: j for i, j in capalar}.items())
    # sıra korunsun: azalan j'li çapalar atılır
    tem, son = [], -1
    for i, j in cs:
        if j > son:
            tem.append((i, j)); son = j
    noktalar = [(-1, -1.0)] + [(i, float(j)) for i, j in tem] + [(n, float(m))]
    out = []
    for (i0, j0), (i1, j1) in zip(noktalar, noktalar[1:]):
        if i0 >= 0:
            out.append((i0, int(j0)))
        ara = i1 - i0
        for i in range(i0 + 1, i1):
            j = j0 + (j1 - j0) * (i - i0) / ara
            out.append((i, int(min(m - 1, max(0, round(j - 0.5 if i1 == n else j))))))
    return out


def en_iyi_madde(cumle: str, adaylar: list[tuple[int, int, dict, set, int]], S: set[str], s0: int):
    """adaylar: (sayfa, madde no, madde, kök kümesi, kelime sayısı). Dönüş (sayfa, madde no, puan) | None."""
    adaylar = [a for a in adaylar if a[4] >= 2]
    if not adaylar:
        return None
    V = vektor([cumle] + [madde_metni(a[2]) for a in adaylar])
    kos = V[1:] @ V[0]
    puan = []
    for a, c in zip(adaylar, kos):
        ortak = len(a[3] & S)
        puan.append((float(c) + 0.04 * min(ortak, 4) + (0.03 if a[0] == s0 else 0.0), float(c), a))
    puan.sort(key=lambda x: -x[0])
    p1, c1, a1 = puan[0]
    if c1 < ESIK:
        return None
    ikinci = next((p for p, _, a in puan[1:] if not (a[0] == a1[0] and abs(a[1] - a1[1]) <= 1)), None)
    if c1 < GUCLU and ikinci is not None and p1 - ikinci < FARK:
        return None
    return a1[0], a1[1], p1
