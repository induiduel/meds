#!/usr/bin/env python3
"""Kurul 3 arşivi GPU yayın kuyruğu: metni ve kapıları bitmiş dersleri sırayla yayınlar (EMA GPU).

EMA kilidi (`/tmp/claude-1000/cozucu_ses.lock`) başka bir iş tarafından tutuluyorsa **bekler** (MEDS_SES_KILIT_BEKLE=1),
kilit boşalınca ilk dersi üretir. Tek süreç, sıralı: GPU'ya aynı anda tek iş.
Her ders yayınlandıktan sonra **canlıya dağıtılır** (kullanıcı talimatı 2026-11-17) ve kuyruk devam eder.

  nohup python3 scripts/uretim/arsiv_25_26/k3_kuyruk.py [--dagit-yok] > /tmp/k3_kuyruk.log 2>&1 &
Kriter: meds_database_25_26/kurul3_durum.json → asama in ("Metin kapıları 0 HATA", "bekliyor_gpu", "yayin")
"""
from __future__ import annotations
import sys as _sys
from pathlib import Path as _Path
_d = _Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in _sys.path:
    _sys.path.insert(0, str(_d))
import kok as _kok  # noqa: E402

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import k3_durum as D

MEDS = _kok.MEDS
DB = MEDS.parent / "meds_database_25_26"
DURUM = DB / "kurul3_durum.json"
PY = str(MEDS / ".venv-ocr" / "bin" / "python")
BURASI = Path(__file__).resolve().parent
HAZIR = ("Metin kapıları 0 HATA", "bekliyor_gpu", "yayin")


def oku() -> dict:
    return D.oku()


def yaz(d: dict) -> None:
    with D.kilit():
        D.yaz(d)


def main() -> int:
    tablo = json.loads((DB / "kurul3_eslesme.json").read_text(encoding="utf-8"))
    dagit = "--dagit-yok" not in sys.argv
    tukendi = set()
    while True:
        d = oku()
        sira = [k for k in tablo if k not in tukendi and d.get(k, {}).get("asama") in HAZIR]
        if not sira:
            print("kuyruk boş — çıkılıyor", flush=True)
            return 0
        k = sira[0]
        print(f"\n=== yayın {k} · {tablo[k]['baslik']}", flush=True)
        D.guncelle(k, asama="yayin")
        env = dict(os.environ)
        env.pop("INVOCATION_ID", None)
        env["MEDS_SES_KILIT_BEKLE"] = "1"
        r = subprocess.run([PY, str(BURASI / "k3_yayinla.py"), k], cwd=MEDS, env=env, capture_output=True, text=True)
        cikti = ((r.stdout or "") + (r.stderr or "")).strip()
        for x in cikti.splitlines()[-8:]:
            print("   " + x[:170], flush=True)
        D.guncelle(k, asama={0: "tamam", 75: "bekliyor_gpu"}.get(r.returncode, "hata:yayin"),
                   **({"son": cikti.splitlines()[-1][:200]} if cikti else {}))
        if r.returncode == 0 and dagit:
            # kullanıcı talimatı 2026-11-17: her ders bitince canlıya dağıt, sonra devam et
            print(f"   → canlıya dağıtılıyor: {k}", flush=True)
            rd = subprocess.run([PY, str(BURASI / "k3_dagit.py"), k], cwd=MEDS, env=env, capture_output=True, text=True)
            for x in ((rd.stdout or "") + (rd.stderr or "")).strip().splitlines()[-6:]:
                print("     " + x[:170], flush=True)
            if rd.returncode == 0:
                D.guncelle(k, asama="tamam", dagitim=time.strftime("%Y-%m-%d %H:%M"))
        if r.returncode != 0:
            tukendi.add(k)
        time.sleep(2)


if __name__ == "__main__":
    raise SystemExit(main())
