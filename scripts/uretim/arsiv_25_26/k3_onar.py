#!/usr/bin/env python3
"""Kurul 3 arşivi onarım işçisi: kapı hatası olan derslerde YALNIZ eksik sayfaları yeniden üretir.

Neden: üretim turu bitince kapsam kapısı birkaç sayfayı "anlatılmamış" bulabiliyor (görsel/şema sayfaları,
modelin boş yanıtı). Tüm dersi yeniden üretmek token israfıdır; burada kapının sayfaları çıkarılıp yalnız onlar
k3_uret.py --sayfa ile üretilir. LLM çağrısı olduğu için kural 20: elle komut (`MEDS_LLM_ELLE=1`).

  env -u INVOCATION_ID MEDS_LLM_ELLE=1 python3 scripts/uretim/arsiv_25_26/k3_onar.py [--adet N] [--ders k1,k2]
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
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import k3_durum as D

MEDS = _kok.MEDS
DB = MEDS.parent / "meds_database_25_26"
PY = str(MEDS / ".venv-ocr" / "bin" / "python")
BURASI = Path(__file__).resolve().parent


def kapilar(key: str) -> tuple[int, str]:
    env = dict(os.environ)
    env.pop("INVOCATION_ID", None)
    r = subprocess.run([PY, str(BURASI / "k3_yayinla.py"), key, "--kapi"],
                       capture_output=True, text=True, cwd=MEDS, env=env)
    return r.returncode, ((r.stdout or "") + (r.stderr or "")).strip()


def eksik_sayfalar(cikti: str) -> list[int]:
    """Kapsam satırlarından sayfa numaraları: 'KAPSAM s.9: anlatılmamış…' ya da 'kapsam: s.9: …'."""
    out = []
    for m in re.finditer(r"s\.(\d+):\s*(anlatılmamış|görselli sayfa)", cikti):
        n = int(m.group(1))
        if n not in out:
            out.append(n)
    return sorted(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--adet", type=int, default=99)
    ap.add_argument("--ders")
    a = ap.parse_args()
    tablo = json.loads((DB / "kurul3_eslesme.json").read_text(encoding="utf-8"))
    d = D.oku()
    if a.ders:
        liste = [x.strip() for x in a.ders.split(",") if x.strip()]
    else:
        liste = [k for k, v in d.items() if str(v.get("asama", "")).startswith("hata:metin")]
        liste.sort(key=lambda k: tablo[k]["sayfa"])
    islenen = 0
    for k in liste:
        if islenen >= a.adet:
            break
        print(f"\n=== onarım {k} · {tablo[k]['baslik']}", flush=True)
        rc, cikti = kapilar(k)
        if rc == 0:
            D.guncelle(k, asama="Metin kapıları 0 HATA", son="onarım: kapılar 0 HATA")
            print("   kapılar zaten 0 HATA", flush=True)
            islenen += 1
            continue
        eksik = eksik_sayfalar(cikti)
        if not eksik:
            # kapsam dışı hata (metin biçimi vb.): önce biçim yenilemesi
            print("   sayfa eksiği yok → biçim yenilemesi", flush=True)
            env = dict(os.environ)
            env.pop("INVOCATION_ID", None)
            subprocess.run([PY, str(BURASI / "k3_uret.py"), k, "--tsv-yenile"], cwd=MEDS, env=env)
            rc2, cikti2 = kapilar(k)
            D.guncelle(k, **({"asama": "Metin kapıları 0 HATA", "son": "onarım: biçim yenilendi"} if rc2 == 0
                             else {"asama": "hata:metin", "son": cikti2.splitlines()[-1][:200] if cikti2 else ""}))
            islenen += 1
            continue
        print(f"   eksik sayfalar: {eksik}", flush=True)
        env = dict(os.environ)
        env.pop("INVOCATION_ID", None)
        t = time.time()
        r = subprocess.run([PY, str(BURASI / "k3_uret.py"), k, "--sayfa", ",".join(map(str, eksik)),
                            "--parca-sayfa", "1"], cwd=MEDS, env=env, capture_output=True, text=True)
        cik = ((r.stdout or "") + (r.stderr or "")).strip()
        for x in cik.splitlines()[-6:]:
            print("     " + x[:160], flush=True)
        print(f"   üretim {time.time() - t:.0f} sn · çıkış {r.returncode}", flush=True)
        D.guncelle(k, **({"asama": "Metin kapıları 0 HATA", "son": f"onarım: {len(eksik)} sayfa"}
                         if r.returncode == 0 else
                         {"asama": "hata:metin", "son": cik.splitlines()[-1][:200] if cik else ""}))
        islenen += 1
    print(f"\nonarım bitti · işlenen {islenen}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
