#!/usr/bin/env python3
"""Deste deposu parçalı arka uç sınaması (VERI_MODELI Faz 3). Monolite DOKUNMAZ: geçici kopyada çalışır.

Aynı işlem dizisi (oku → bir desteyi düzenle → yeni deste ekle → sil) önce monolit kopyasında, sonra parçalı
dizinde uygulanır; parçaların birleşimi monolit kopyasıyla bayt bayt aynı olmalı. Süreler de ölçülür.
    python3 scripts/sinama_deste_parcali.py
"""
from __future__ import annotations

import hashlib
import importlib
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path as _P

_s = _P(__file__).resolve()
while not (_s / "kok.py").exists() and _s != _s.parent:
    _s = _s.parent
sys.path.insert(0, str(_s))
from kok import PROJE  # noqa: E402,F401

import deste_deposu as _dd0  # noqa: E402

KAYNAK = _dd0.YOL


def depo(dosya: _P, parca: _P | None):
    os.environ["DESTE_DOSYASI"] = str(dosya)
    if parca:
        os.environ["MEDS_DESTE_PARCALI"] = "1"
        os.environ["MEDS_DESTE_PARCA_DIZIN"] = str(parca)
    else:
        os.environ.pop("MEDS_DESTE_PARCALI", None)
        os.environ.pop("MEDS_DESTE_PARCA_DIZIN", None)
    return importlib.reload(_dd0)


def sure(f):
    t = time.perf_counter()
    r = f()
    return r, (time.perf_counter() - t) * 1000


def senaryo(dd, olcum: dict, ad: str):
    ilk = dd.hepsi()
    hedef = ilk[len(ilk) // 2]["id"]
    sil_id = ilk[3]["id"]
    d, olcum[f"{ad}_oku_ms"] = sure(lambda: dd.oku(hedef))
    assert d and d["id"] == hedef
    d["title"] = d["title"] + " (sınama)"
    _, olcum[f"{ad}_duzenle_ms"] = sure(lambda: dd.guncelle(d))
    assert dd.guncelle({"id": "sinama-yeni-deste", "deckId": "sinama-yeni-deck", "title": "Yeni", "slides": []}) is False
    assert dd.oku("sinama-yeni-deck")["id"] == "sinama-yeni-deste"  # deckId ile arama
    with dd.duzenle() as liste:  # toplu düzenleme yolu
        liste[0]["sinama"] = True
    assert dd.sil(sil_id) is True and dd.sil("yok-boyle-deste") is False


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="deste_parcali_") as td:
        t = _P(td)
        mono = t / "mono.json"
        shutil.copyfile(KAYNAK, mono)
        parca_mono = t / "p_kaynak.json"
        shutil.copyfile(KAYNAK, parca_mono)  # parçalı modda kilit dosyası bunun yanında
        parca = t / "desteler"
        olcum: dict = {}

        dd = depo(mono, None)
        senaryo(dd, olcum, "monolit")

        dd = depo(parca_mono, None)
        dd.parcali_yaz(dd.hepsi(), parca)
        dd = depo(parca_mono, parca)
        senaryo(dd, olcum, "parcali")
        assert parca_mono.read_bytes() == KAYNAK.read_bytes(), "parçalı kipte monolit kopyasına yazıldı!"

        a = mono.read_bytes()
        b = dd.birlestir_bayt(dd.parca_baytlari(parca))
        ha, hb = hashlib.sha256(a).hexdigest(), hashlib.sha256(b).hexdigest()
        print(f"monolit sonucu  sha256 {ha} ({len(a):,} bayt)")
        print(f"parçalı birleşim sha256 {hb} ({len(b):,} bayt)")
        for k, v in olcum.items():
            print(f"  {k:22s} {v:9.1f} ms")
        depo(KAYNAK, None)
        if a != b:
            print("SONUÇ: FARK VAR")
            return 1
        print("SONUÇ: bayt bayt aynı")
        return 0


if __name__ == "__main__":
    sys.exit(main())
