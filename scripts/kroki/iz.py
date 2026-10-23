"""Sayfa izi ve sayfa eşleme — slayt kayması (ICERIK_MOTORU_V3.md §2.2).

İz: `metin` = 64 bit SimHash (katlanmış sözcük 3'lüleri; az sözcükte 1'liler), `gorsel` = 64 bit pHash (32×32 gri,
2B DCT, sol üst 8×8, ortanca eşik). Hamming uzaklığı küçükse iki sayfa aynıdır.
Eşleme (eski L0 ↔ yeni PDF): aynı = metin ≤ 6 ve görsel ≤ 10 (metinsiz sayfada yalnız görsel ≤ 6); biri tutarsa
`degismis`; hiçbiri tutmazsa `yeni`. Her eski sayfa en çok bir yeni sayfaya; sıra korumaya öncelik (eşit uzaklıkta
beklenen kaymaya en yakın aday). Sonuç: {yeni_sayfa: {"eski": n|None, "tur": ayni|degismis|yeni, "metin": d, "gorsel": d}}.
"""
from __future__ import annotations

import hashlib

import numpy as np

from ortak import katla, sozcukler

METIN_ESIK, GORSEL_ESIK, METINSIZ_GORSEL_ESIK = 6, 10, 6


def simhash(metin: str) -> str | None:
    w = [katla(x) for x in sozcukler(metin) if len(x) >= 2]
    if len(w) < 3:
        return None                                   # metinsiz sayfa: yalnız görsel izle eşlenir
    oge = [" ".join(w[i:i + 3]) for i in range(len(w) - 2)] if len(w) >= 6 else w
    v = [0] * 64
    for o in oge:
        h = int.from_bytes(hashlib.md5(o.encode()).digest()[:8], "big")
        for i in range(64):
            v[i] += 1 if (h >> i) & 1 else -1
    deger = 0
    for i in range(64):
        if v[i] > 0:
            deger |= 1 << i
    return f"{deger:016x}"


def _dct2(a: np.ndarray) -> np.ndarray:
    from scipy.fft import dctn
    return dctn(a, norm="ortho")


def phash(gri32: np.ndarray) -> str:
    """gri32: 32×32 float gri görüntü."""
    d = _dct2(gri32.astype("float64"))[:8, :8].flatten()
    ort = np.median(d[1:])
    deger = 0
    for i, b in enumerate(d > ort):
        if b:
            deger |= 1 << i
    return f"{deger:016x}"


def sayfa_gri32(sayfa) -> np.ndarray:
    """PyMuPDF sayfası → 32×32 gri (alan ortalaması; küçük çizim + yeniden örnekleme)."""
    import cv2
    import pymupdf
    pm = sayfa.get_pixmap(matrix=pymupdf.Matrix(128 / max(sayfa.rect.width, 1), 128 / max(sayfa.rect.width, 1)),
                          colorspace=pymupdf.csGRAY, alpha=False)
    g = np.frombuffer(pm.samples, dtype=np.uint8).reshape(pm.height, pm.width)
    return cv2.resize(g, (32, 32), interpolation=cv2.INTER_AREA).astype("float64")


def hamming(a: str | None, b: str | None) -> int | None:
    if a is None or b is None:
        return None
    return bin(int(a, 16) ^ int(b, 16)).count("1")


def _kapsar(e: dict, y: dict, dg: int) -> bool:
    """Eski sayfanın sözcüklerinin ≥%80'i yeni sayfada ve görünüm yakın (dg ≤ 16): üzerine madde eklenmiş sayfa."""
    a, b = e.get("kume"), y.get("kume")
    return bool(a) and bool(b) and dg <= 16 and len(a & b) / len(a) >= 0.8


def kume(sozler) -> set[str]:
    return {katla(w) for w in sozler if len(w) >= 3}


def eslestir(eski: list[dict], yeni: list[dict]) -> dict[int, dict]:
    """eski/yeni: [{"sayfa": n, "iz": {"metin": h|None, "gorsel": h}, "kume"?: {sözcük}}]. Dönen: yeni sayfa no → kayıt."""
    adaylar = []
    for y in yeni:
        for e in eski:
            dm = hamming(y["iz"].get("metin"), e["iz"].get("metin"))
            dg = hamming(y["iz"]["gorsel"], e["iz"]["gorsel"])
            if dm is None and (y["iz"].get("metin") is None) != (e["iz"].get("metin") is None):
                continue                              # biri metinli biri metinsiz: aynı sayfa olamaz
            if dm is None:
                tur = "ayni" if dg <= METINSIZ_GORSEL_ESIK else None
            elif dm <= METIN_ESIK and dg <= GORSEL_ESIK:
                tur = "ayni"
            elif dm <= METIN_ESIK or (dg <= METINSIZ_GORSEL_ESIK and dm <= 16) or _kapsar(e, y, dg):
                tur = "degismis"
            else:
                tur = None
            if tur:
                adaylar.append(((0 if tur == "ayni" else 1), (dm if dm is not None else 0) + dg / 4,
                                y["sayfa"], e["sayfa"], tur, dm, dg))
    # açgözlü atama: önce "aynı", sonra en küçük uzaklık; eşitlikte sıra korunur (küçük sayfa farkı)
    adaylar.sort(key=lambda a: (a[0], a[1], abs(a[2] - a[3])))
    sonuc: dict[int, dict] = {}
    kullanilan: set[int] = set()
    for _, _, ys, es, tur, dm, dg in adaylar:
        if ys in sonuc or es in kullanilan:
            continue
        sonuc[ys] = {"eski": es, "tur": tur, "metin": dm, "gorsel": dg}
        kullanilan.add(es)
    for y in yeni:
        sonuc.setdefault(y["sayfa"], {"eski": None, "tur": "yeni", "metin": None, "gorsel": None})
    return dict(sorted(sonuc.items()))
