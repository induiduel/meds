#!/usr/bin/env python3
"""Kurul 2 arşivinde ses dosyası mevcut ve güncel olan dersleri lazer metin takibi %98-100 ile paketleyen otomasyon."""

from __future__ import annotations
import json
import os
import subprocess
import sys
from pathlib import Path

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")

MEDS = Path(__file__).resolve().parents[2]
ROOT = MEDS.parent
SA_KOK = MEDS / "data" / "arsiv_25_26" / "sesli_anlatim"
DB_25_26 = ROOT / "meds_database_25_26"

sys.path.insert(0, str(MEDS / "scripts" / "arsiv_25_26"))
import uygula_lazer_takip as ULT

HEDEFLER = [
    "y25-k2-06-agri-yollari-ve-mekanizmalari",
    "y25-k2-07-genel-anestezik-ilaclar",
    "y25-k2-09-sss-ilaclari",
    "y25-k2-10-bas-agrisina-yaklasim",
    "y25-k2-12-kafa-travmalari",
    "y25-k2-13-spinal-travmalar",
    "y25-k2-14-beyin-tumorleri",
    "y25-k2-15-sizofrenik-bozukluklar",
    "y25-k2-16-norolojik-rehabilitasyona-giris",
    "y25-k2-17-periferik-noropati",
    "y25-k2-18-bazal-gangliyonlar",
    "y25-k2-20-psikiyatrik-tedaviler",
    "y25-k2-21-sedatif-ve-hipnotik-ilaclar",
    "y25-k2-55-panik-bozukluk",
    "y25-k2-58-alkoller",
    "y25-k2-59-psikiyatrik-hastaliklar-ve-genetik-analizi",
    "y25-k2-60-miyorelaksan-ilaclar",
]


def main():
    print(f"Toplam {len(HEDEFLER)} derste lazer takip zenginleştirme ve .medspak üretimi başlatılıyor...\n")
    basarili = []
    hatali = []

    for i, key in enumerate(HEDEFLER, 1):
        print(f"\n{'='*70}\n[{i}/{len(HEDEFLER)}] İŞLENİYOR: {key}\n{'='*70}")
        try:
            # 1. Lazer zenginleştirme (capa, v2, taslak)
            l_cnt, tot_cnt, pct_l, pct_w = ULT.zenginlestir_ders(key)
            print(f"[{key}] ULT: {l_cnt}/{tot_cnt} ({pct_l}%) satır | {pct_w}% kelime")

            # 2. Arşiv yayınla (var olan sesi kullanır)
            cmd = [
                sys.executable,
                str(MEDS / "scripts" / "arsiv_25_26" / "arsiv_yayinla.py"),
                "--key", key,
            ]
            r = subprocess.run(cmd, cwd=MEDS)
            if r.returncode != 0:
                print(f"HATA: arsiv_yayinla başarısız (kod {r.returncode})", file=sys.stderr)
                hatali.append((key, f"arsiv_yayinla kod {r.returncode}"))
                continue

            # 3. Doğrula
            medspak_yol = DB_25_26 / "medspak" / "kurul2" / f"{key}.medspak"
            r_dogrula = subprocess.run(
                [sys.executable, str(MEDS / "scripts" / "paket" / "medspak_dogrula.py"), str(medspak_yol)],
                capture_output=True,
                text=True,
            )
            if r_dogrula.returncode != 0 or "0 HATA" not in r_dogrula.stdout:
                print(f"HATA: medspak_dogrula başarısız: {r_dogrula.stdout} {r_dogrula.stderr}", file=sys.stderr)
                hatali.append((key, "medspak_dogrula"))
                continue

            print(f"[{key}] TAMAMLANDI ✔ (0 HATA, {pct_l}% satır takip)")
            basarili.append((key, pct_l, pct_w))
        except Exception as e:
            print(f"HATA [{key}]: {e}", file=sys.stderr)
            hatali.append((key, str(e)))

    print("\n" + "=" * 70)
    print(f"ÖZET: {len(basarili)} BAŞARILI, {len(hatali)} HATALI")
    for k, pl, pw in basarili:
        print(f"  ✔ {k:50s} : {pl}% satır | {pw}% kelime")
    for k, err in hatali:
        print(f"  ❌ {k:50s} : {err}")


if __name__ == "__main__":
    main()
