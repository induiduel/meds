#!/usr/bin/env python3
"""Yeni bir ders için 'hocanın soracağı yerler' tahmin girdisini üretir (LLM yok). meds/.venv-ocr/bin/python ile çalışır.

  tahmin_girdisi.py <ders_metni.md> --ders "Tıbbi Patoloji" --konu "Tiroid ve Paratiroid" --cikti <klasör>

Üretir: <klasör>/{not.md, profil.md, adaylar.md}. profil.md ilk satırı K (10–18; ders uzunluğuna göre) tahmin sayısını söyler.
Sonra yazar/alt ajan `docs/HOCA_TAHMIN_REHBERI.md`'ye göre K tahmin yazar; çıktı önem listesi 'kanit: profil' adaylarıdır
(çıkmışla eşleşmeyen yerleri tamamlar). Gömme servisi (bge-m3 :8094) açık olmalıdır. Ölçüm ve sınırlar: docs/HOCA_USLUBU/TEST_TURLARI.md.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tur_yonet  # noqa: E402
from algoritmalar import gecmis_gom, sinyaller  # noqa: E402
from ortak import CIKTI, slug  # noqa: E402
from sinama_ortak import DERS_ESLE  # noqa: E402
from satir_model import dosya_satirlari  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("metin", type=Path)
    ap.add_argument("--ders", required=True)
    ap.add_argument("--konu", default="")
    ap.add_argument("--cikti", type=Path, required=True)
    a = ap.parse_args()
    ders = DERS_ESLE.get(a.ders, a.ders)
    dd = dict(id="uret-" + slug(a.metin.stem), ders=ders, konu=a.konu or a.metin.stem, yol=a.metin, satirlar=dosya_satirlari(a.metin), sorular=[])
    Q, QE = gecmis_gom()
    idx = {}
    for j, q in enumerate(Q):
        idx.setdefault(q["ders"], []).append(j)
    k = dd["id"]
    sig = {k: sinyaller(dd, Q, QE, idx)}
    tur_yonet.PROFIL = CIKTI  # üretim profili (2026-27 dahil)
    ad = dict(genel_adaylar=tur_yonet.adaylar(sig, dd, k, n=20, tur_filtre=True))
    ad.update(tur_yonet.yapi_adaylari(dd))
    a.cikti.mkdir(parents=True, exist_ok=True)
    shutil.copy(a.metin, a.cikti / "not.md")
    (a.cikti / "adaylar.md").write_text(tur_yonet.adaylar_md(ad))
    (a.cikti / "profil.md").write_text(f"**Bu ders için tam {tur_yonet.hedef_k(dd)} tahmin yaz.**\n\n" + tur_yonet.profil_md(dd, k, sig, Q, QE))
    print(f"{a.cikti}: not.md, profil.md (K={tur_yonet.hedef_k(dd)}), adaylar.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
