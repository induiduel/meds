#!/usr/bin/env python3
"""Kurul 3 arşivi parti işçisi: ders listesini sırayla hazırla → metin → kapılar (yayın YAPMAZ).

Yayın (EMA GPU ses + PDF takibi + .medspak) ayrı süreçte, `k3_kuyruk.py` ile yürür: GPU'ya aynı anda tek iş
girer, birden çok parti süreci GPU kilidinde kuyruğa takılıp metin üretimini durdurmaz (2026-11-17 düzeltmesi).

  env -u INVOCATION_ID MEDS_LLM_ELLE=1 python3 scripts/uretim/arsiv_25_26/k3_parti.py [--baslangic N] [--adet K]
      [--ders key1,key2] [--kuru] [--yayin]   # --kuru: yalnız sırayı yaz · --yayin: bitince kuyruğu çalıştır
Durum: meds_database_25_26/kurul3_durum.json  {key: {asama, tarih, hata}}  (k3_durum.py, flock'lu)
"""
from __future__ import annotations
import sys as _sys
from pathlib import Path as _Path
_d = _Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in _sys.path:
    _sys.path.append(str(_d))
import kok as _kok  # noqa: E402

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

MEDS = _kok.MEDS
DB = MEDS.parent / "meds_database_25_26"
DURUM = DB / "kurul3_durum.json"
PY = str(MEDS / ".venv-ocr" / "bin" / "python")
BURASI = Path(__file__).resolve().parent


def durum_oku() -> dict:
    import k3_durum as D
    return D.oku()


def durum_yaz(d: dict) -> None:
    import k3_durum as D
    with D.kilit():
        D.yaz(d)


def durum_guncelle(key: str, **alanlar) -> None:
    import k3_durum as D
    D.guncelle(key, **alanlar)


def calistir(komut: list[str], ad: str, env_ek: dict | None = None) -> tuple[int, str]:
    import os
    t = time.time()
    env = dict(os.environ)
    env.pop("INVOCATION_ID", None)
    env.update(env_ek or {})
    r = subprocess.run(komut, capture_output=True, text=True, cwd=MEDS, env=env)
    cikti = ((r.stdout or "") + (r.stderr or "")).strip()
    print(f"    {ad}: çıkış {r.returncode} · {time.time() - t:.0f} sn", flush=True)
    if r.returncode != 0:
        for x in cikti.splitlines()[-12:]:
            print("      " + x[:160], flush=True)
    return r.returncode, cikti


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--baslangic", type=int, default=0)
    ap.add_argument("--adet", type=int, default=6)
    ap.add_argument("--ders")
    ap.add_argument("--kuru", action="store_true")
    ap.add_argument("--yayin", action="store_true", help="bitince yayın kuyruğunu başlat")
    a = ap.parse_args()
    tablo = json.loads((DB / "kurul3_eslesme.json").read_text(encoding="utf-8"))
    d = durum_oku()
    if a.ders:
        anahtarlar = [x.strip() for x in a.ders.split(",") if x.strip()]
    else:
        # bitmemiş dersler: sayfa sayısı küçükten büyüğe (hızlı kazanç + boru hattı doğrulaması)
        anahtarlar = sorted(tablo, key=lambda k: (d.get(k, {}).get("asama") in ("tamam", "Metin kapıları 0 HATA", "yayin"),
                                                 tablo[k]["sayfa"]))
        anahtarlar = [k for k in anahtarlar if d.get(k, {}).get("asama") != "tamam"]
        anahtarlar = anahtarlar[a.baslangic:a.baslangic + a.adet]
    if a.kuru:
        for k in anahtarlar:
            print(k, tablo[k]["sayfa"], "sayfa", tablo[k]["baslik"][:60])
        return 0
    print(f"parti: {len(anahtarlar)} ders", flush=True)
    for k in anahtarlar:
        e = tablo[k]
        print(f"\n=== {k} · {e['sayfa']} sayfa · {e['baslik']}", flush=True)
        durum_guncelle(k, asama="hazirlik")
        rc, _ = calistir([PY, str(BURASI / "k3_ders.py"), "hazirla", k], "hazırlık")
        if rc != 0:
            durum_guncelle(k, asama="hata:hazirlik")
            continue
        durum_guncelle(k, asama="metin")
        rc, cikti = calistir([PY, str(BURASI / "k3_uret.py"), k], "metin")
        durum_guncelle(k, asama="Metin kapıları 0 HATA" if rc == 0 else "hata:metin",
                       **({"son": cikti.splitlines()[-1][:200]} if cikti else {}))
    d = durum_oku()
    tamam = [k for k, v in d.items() if v.get("asama") == "tamam"]
    print(f"\nparti bitti · toplam tamam {len(tamam)}/{len(tablo)}")
    for k, v in d.items():
        if v.get("asama", "").startswith("hata"):
            print(f"  HATA {k}: {v['asama']}")
    if a.yayin:
        print("\nyayın kuyruğu başlıyor…", flush=True)
        calistir([PY, str(BURASI / "k3_kuyruk.py")], "kuyruk")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
