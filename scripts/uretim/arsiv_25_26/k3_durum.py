#!/usr/bin/env python3
"""Kurul 3 arşiv durum defteri — çok süreçli güvenli okuma/yazma (flock).

Neden: metin işçileri paralel çalışırken (birden çok k3_parti süreci) ve yayın kuyruğu ayrı süreçte
durum dosyasını yazıyor. Kilit olmadan oku-değiştir-yaz yarışıyor, bir işçinin yazdığı "tamam" kayboluyordu.

  k3_durum.py oku | yaz '<json>' | sil <key> | liste
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

import contextlib
import fcntl
import json
import os
import sys
from pathlib import Path

MEDS = _kok.MEDS
DB = MEDS.parent / "meds_database_25_26"
DURUM = DB / "kurul3_durum.json"
KILIT = DB / "kurul3_durum.lock"


@contextlib.contextmanager
def kilit():
    DB.mkdir(parents=True, exist_ok=True)
    f = open(KILIT, "a+", encoding="utf-8")
    try:
        fcntl.flock(f, fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(f, fcntl.LOCK_UN)
        f.close()


def oku() -> dict:
    try:
        return json.loads(DURUM.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def yaz(d: dict) -> None:
    """Kilidi ÇAĞIRAN almış olmalı (guncelle içinden kullanılır)."""
    g = DURUM.with_suffix(f".{os.getpid()}.tmp.json")
    g.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    g.replace(DURUM)


def guncelle(key: str, **alanlar) -> dict:
    """Tek anahtarı kilitle oku-değiştir-yaz; dosyanın geri kalanına dokunmaz."""
    with kilit():
        d = oku()
        d[key] = {**alanlar, "tarih": alanlar.get("tarih") or _simdi()}
        yaz(d)
        return d[key]


def _simdi() -> str:
    import time
    return time.strftime("%Y-%m-%d %H:%M")


def main() -> int:
    a = sys.argv[1:]
    if not a:
        print(json.dumps(oku(), ensure_ascii=False, indent=1))
        return 0
    if a[0] == "oku":
        print(json.dumps(oku().get(a[1]) if len(a) > 1 else oku(), ensure_ascii=False, indent=1))
    elif a[0] == "yaz":
        with kilit():
            yaz(json.loads(a[1]))
    elif a[0] == "sil" and len(a) > 1:
        with kilit():
            d = oku()
            d.pop(a[1], None)
            yaz(d)
    else:
        print(__doc__, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
