#!/usr/bin/env python3
"""Gece görev politikası (R4) — `aktif` görevleri bekleyen hedeflerde bütçe tavanıyla koşar ve uygular.

Şimdilik: `kanit_bagla` — Kurul 2+ (aktif kurul ve önceki K2+ kurullar) derslerinin `kanit.json`'undaki olası/bağsız
soruları 6'lık partilerle modele seçtirir, kapıdan geçeni uygular (l1/kanit_model.json + kanit.json + tekrar listesi).
Kurul 1 yalnız `--k1` ile (kendi l1 dosyaları; içerik verisi değil). Görevin `mod` alanı `golge` ise hiç koşmaz.
Tavan: `--parti` (varsayılan 20/gece). Kota/bütçe biterse kalan sonraki geceye (çıkış 4); yanıt yoksa 5.

Kullanım: python3 meds/otomasyon/llm/gece.py [--parti 20] [--k1] [--ders kN-NN]
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from llm import cekirdek as c  # noqa: E402
from llm import yonlendir  # noqa: E402


def aktif_kurul() -> int:
    r = subprocess.run([sys.executable, str(c.KOK / "scripts" / "takvim" / "aktif_kurul.py")], capture_output=True, text=True)
    return int(r.stdout.strip() or 1)


def kanit_bagla(parti_tavan: int, k1: bool, tek: str | None) -> int:
    from llm.gorevler import kanit_bagla as KB
    if c.kayit("kanit_bagla").get("mod") == "golge":
        print("kanit_bagla gölge kipinde — gece uygulanmaz"); return 0
    aktif = aktif_kurul()
    dersler = sorted(p.parent.parent.name for p in (c.DB2 / "ders_bilgi").glob("k*-*/l1/kanit.json"))
    if tek:
        dersler = [tek]
    else:
        dersler = [d for d in dersler if (2 <= int(d[1]) <= max(aktif, 2)) or (k1 and d.startswith("k1-"))]
    yapilan, son_kod = 0, 0
    for ders in dersler:
        while yapilan < parti_tavan:
            if not KB.bekleyenler(ders):
                break
            try:
                is_id = c.is_ac("kanit_bagla", f"{ders}/parti/0", KB.hazirla(f"{ders}/parti/0", {}))
            except SystemExit as e:
                print(f"  {ders}: {e}"); break
            kod = yonlendir.calistir(is_id, None, None, log=lambda m: print("   " + m))
            yapilan += 1
            _, pj = c.paket(is_id)
            if kod == 0:
                cik = c.oku(c.is_klasoru(is_id) / "cikti.json")
                KB.uygula(cik, pj["meta"])
                dusen = c.durum(is_id).get("kismi") or []
                if dusen:
                    KB.denemeyi_say(ders, [pj["meta"]["sorular"][Q]["id"] for Q in dusen])
                c.durum_yaz(is_id, durum="uygulandi", uygulandi=c.simdi())
                continue
            if kod == 1:
                KB.denemeyi_say(ders, [ms["id"] for ms in pj["meta"]["sorular"].values()])
            son_kod = kod
            if kod in (4, 5):
                print(f"  {ders}: kota/bütçe (kod {kod}) — kalan sonraki gece"); return kod
            # kapıdan geçemeyen parti: deneme sayıldı; tavanı aşan sorular `model_cozemedi` listesine düşer (elle)
            print(f"  {ders}: parti kapıdan geçmedi (kod {kod}) — deneme sayıldı"); continue
    print(f"kanit_bagla gece: {yapilan} parti")
    return son_kod if son_kod not in (1,) else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--parti", type=int, default=20)
    ap.add_argument("--k1", action="store_true")
    ap.add_argument("--ders")
    a = ap.parse_args()
    return kanit_bagla(a.parti, a.k1, a.ders)


if __name__ == "__main__":
    sys.exit(main())
