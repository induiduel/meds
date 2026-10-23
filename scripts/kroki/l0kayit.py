"""L0 dosyasına sayfa düzeyi alan yazımı (roi, egri, ok) — tek yazıcı, dosya kilitli.

Bu alanlar `l0.py`'nin TASINAN listesindedir: PDF güncellenince "aynı" sayfalara taşınır, yeniden hesaplanmaz.
"""
from __future__ import annotations

import fcntl
from pathlib import Path

from ortak import DEPO, oku, yaz


def yol(ders: str) -> Path:
    return DEPO / ders / "l0" / "sayfalar.json"


def yukle(ders: str) -> dict:
    d = oku(yol(ders))
    if not d:
        raise SystemExit(f"{ders}: L0 yok — önce scripts/kroki/l0.py --ders {ders}")
    return d


def sayfa(ders: str, no: int) -> tuple[dict, dict]:
    d = yukle(ders)
    s = next((x for x in d["sayfalar"] if x["sayfa"] == no), None)
    if not s:
        raise SystemExit(f"{ders}: sayfa {no} yok ({d['sayfa_sayisi']} sayfa)")
    return d, s


def sayfa_yaz(ders: str, no: int, alan: str, deger) -> None:
    yaz_toplu(ders, {no: {alan: deger}})


def yaz_toplu(ders: str, alanlar: dict[int, dict]) -> None:
    """{sayfa: {alan: değer}} — tek okuma/yazma, dosya kilidiyle (aynı anda iki betik L0'ı ezmesin)."""
    p = yol(ders)
    with open(p.with_suffix(".kilit"), "w") as k:
        fcntl.flock(k, fcntl.LOCK_EX)
        d = yukle(ders)
        for s in d["sayfalar"]:
            for alan, deger in (alanlar.get(s["sayfa"]) or {}).items():
                if deger in (None, [], {}):
                    s.pop(alan, None)
                else:
                    s[alan] = deger
        yaz(p, d)
