#!/usr/bin/env python3
"""Tek kapı girişi — hat aşamasının kanonik kapısını matris.json'dan çözüp çalıştırır. (kullanıcı kararı 2026-11-16)

Neden: tek-kapı birleşik betikler (anlatim_kapi, ornek_soru_kapi) çağrı sayısını azalttı ama kapı DOSYALARI hâlâ dağınık.
Bu dispatcher TEK giriş verir: ajan/işçi aşama adıyla çağırır, kapı komutunu kendisi bilmek zorunda kalmaz. Alttaki
doğrulayıcılar silinmez; bu matrisin yapı taşlarıdır — tek fark, artık buradan tek adla çağrılırlar.

  python3 scripts/kapilar/kos.py --liste
  python3 scripts/kapilar/kos.py anlatim dizin=<v3 dizin> sayfalar=<sayfalar.json> key=k2-49
  python3 scripts/kapilar/kos.py ornek_soru dosya=<...> uslup=<...> ders="<ders>" sayfalar=<...>

Aşamanın `gerekli` yer tutucuları ad=değer çiftleriyle verilir; eksikse çalıştırmadan listeyle durur. Kapının çıkış
kodu aynen döndürülür (0 = 0 HATA).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
MATRIS = Path(__file__).resolve().parent / "matris.json"


def _yukle() -> dict:
    return json.loads(MATRIS.read_text(encoding="utf-8"))["asamalar"]


def main() -> int:
    asamalar = _yukle()
    argv = sys.argv[1:]
    if not argv or argv[0] in ("--liste", "-l", "--help", "-h"):
        print("Aşamalar (tek kapı girişi · matris.json):")
        for ad, m in asamalar.items():
            yer = ", ".join(m["gerekli"])
            print(f"  {ad:<14} {Path(m['kapi']).name:<24} gerekli: {yer}")
        return 0
    asama, ciftler = argv[0], argv[1:]
    if asama not in asamalar:
        print(f"HATA: bilinmeyen aşama '{asama}' (geçerli: {', '.join(asamalar)})", file=sys.stderr)
        return 2
    m = asamalar[asama]
    deg: dict[str, str] = {}
    for c in ciftler:
        if "=" not in c:
            print(f"HATA: ad=değer bekleniyor, '{c}' değil", file=sys.stderr)
            return 2
        ad, _, v = c.partition("=")
        deg[ad] = v
    eksik = [g for g in m["gerekli"] if g not in deg]
    if eksik:
        print(f"HATA: eksik yer tutucu(lar): {', '.join(eksik)}  (gerekli: {', '.join(m['gerekli'])})", file=sys.stderr)
        return 2
    try:
        arg = [p.format(**deg) for p in m["arg"]]
    except KeyError as e:
        print(f"HATA: matriste tanımsız yer tutucu {e}", file=sys.stderr)
        return 2
    cmd = [sys.executable, m["kapi"], *arg]
    print(f"== kapı: {asama} → {' '.join(cmd[1:])}")
    return subprocess.run(cmd, cwd=KOK).returncode


if __name__ == "__main__":
    sys.exit(main())
