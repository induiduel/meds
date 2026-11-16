#!/usr/bin/env python3
"""Ortak betik günlüğü (yalnız stdlib; asla istisna fırlatmaz).

Kullanım (betikten):
    import gunluk
    gunluk.olay("veri_bakim", "bilgi", "arşivlendi", yol="data/x.bak", bayt=123)
    with gunluk.sure("veri_bakim", "rapor"):
        ...
Kayıt: <MEDS>/data/gunluk/betik-YYYY-MM.jsonl (tek satır JSON: zaman, seviye, kaynak, mesaj, ek, pid).
Sunucu aynı klasöre veri-YYYY-MM.jsonl yazar; CLI ikisini birlikte okur. uyari/hata stderr'e de yazılır.

CLI:
    python3 scripts/gunluk.py son [--n 30] [--seviye uyari] [--kaynak x]
    python3 scripts/gunluk.py ozet [--gun 7]
"""
from __future__ import annotations

import argparse
import contextlib
import json
import os
import sys
import time
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    _s = Path(__file__).resolve().parent
    while not (_s / "kok.py").exists() and _s != _s.parent:
        _s = _s.parent
    if str(_s) not in sys.path:
        sys.path.append(str(_s))
    import kok as _kok  # noqa: E402
    KLASOR: Path = _kok.MEDS / "data" / "gunluk"
except Exception:  # kök bulunamazsa bile günlük çökertmez
    KLASOR = Path.cwd() / "data" / "gunluk"

SEVIYELER = ("bilgi", "uyari", "hata")
_SIRA = {s: i for i, s in enumerate(SEVIYELER)}


def olay(kaynak: str, seviye: str, mesaj: str, **ek) -> None:
    """Tek satır JSON yazar. Hiçbir koşulda istisna fırlatmaz."""
    try:
        seviye = seviye if seviye in _SIRA else "bilgi"
        an = datetime.now(timezone.utc).astimezone()
        kayit = {"zaman": an.isoformat(timespec="seconds"), "seviye": seviye, "kaynak": str(kaynak),
                 "mesaj": str(mesaj), "ek": ek or {}, "pid": os.getpid()}
        satir = json.dumps(kayit, ensure_ascii=False, default=str)
        if seviye != "bilgi":
            try:
                print(f"[{seviye}] {kaynak}: {mesaj}", file=sys.stderr)
            except Exception:
                pass
        KLASOR.mkdir(parents=True, exist_ok=True)
        with open(KLASOR / f"betik-{an:%Y-%m}.jsonl", "a", encoding="utf-8") as f:
            f.write(satir + "\n")
    except Exception:
        pass


@contextlib.contextmanager
def sure(kaynak: str, ad: str, **ek):
    """Bloğun süresini ms olarak kaydeder; blok istisna verirse 'hata' düzeyinde yazar ve istisnayı geçirir."""
    t0 = time.perf_counter()
    try:
        yield
    except BaseException as e:
        olay(kaynak, "hata", f"{ad} başarısız: {type(e).__name__}: {e}",
             sure_ms=round((time.perf_counter() - t0) * 1000), ad=ad, **ek)
        raise
    olay(kaynak, "bilgi", f"{ad} bitti", sure_ms=round((time.perf_counter() - t0) * 1000), ad=ad, **ek)


def _kayitlar():
    if not KLASOR.is_dir():
        return
    for p in sorted(list(KLASOR.glob("betik-*.jsonl")) + list(KLASOR.glob("veri-*.jsonl"))):
        try:
            with open(p, encoding="utf-8", errors="replace") as f:
                for satir in f:
                    try:
                        k = json.loads(satir)
                        if isinstance(k, dict):
                            k["_dosya"] = p.name.split("-")[0]
                            yield k
                    except Exception:
                        continue
        except OSError:
            continue


def _zaman(k) -> datetime | None:
    try:
        z = datetime.fromisoformat(str(k.get("zaman", "")).replace("Z", "+00:00"))
        return z if z.tzinfo else z.replace(tzinfo=timezone.utc)
    except Exception:
        return None


def _son(a) -> int:
    esik = _SIRA.get(a.seviye, 0)
    sec = [k for k in _kayitlar()
           if _SIRA.get(k.get("seviye"), 0) >= esik and (not a.kaynak or a.kaynak in str(k.get("kaynak", "")))]
    sec.sort(key=lambda k: _zaman(k) or datetime.min.replace(tzinfo=timezone.utc))
    if not sec:
        print(f"(kayıt yok — {KLASOR})")
        return 0
    for k in sec[-a.n:]:
        z = str(k.get("zaman", ""))[:19].replace("T", " ")
        ek = k.get("ek") or {}
        eks = " ".join(f"{x}={v}" for x, v in list(ek.items())[:4]) if isinstance(ek, dict) else ""
        print(f"{z}  {k.get('seviye', '?'):5} {k['_dosya']:5} {str(k.get('kaynak', ''))[:18]:18} "
              f"{str(k.get('mesaj', ''))[:70]}  {eks[:60]}")
    return 0


def _ozet(a) -> int:
    sinir = datetime.now(timezone.utc) - timedelta(days=a.gun)
    say: Counter = Counter()
    for k in _kayitlar():
        z = _zaman(k)
        if z and z >= sinir:
            say[(str(k.get("kaynak", "?")), str(k.get("seviye", "?")))] += 1
    if not say:
        print(f"(son {a.gun} günde kayıt yok — {KLASOR})")
        return 0
    kaynaklar = sorted({k for k, _ in say})
    print(f"{'kaynak':28} {'bilgi':>7} {'uyari':>7} {'hata':>7}")
    for kn in kaynaklar:
        print(f"{kn[:28]:28} " + " ".join(f"{say[(kn, s)]:>7}" for s in SEVIYELER))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Ortak betik/sunucu günlüğü okuyucu")
    alt = ap.add_subparsers(dest="komut", required=True)
    s = alt.add_parser("son", help="son kayıtlar")
    s.add_argument("--n", type=int, default=30)
    s.add_argument("--seviye", choices=SEVIYELER, default="bilgi", help="bu düzey ve üstü")
    s.add_argument("--kaynak", default="")
    o = alt.add_parser("ozet", help="kaynak × seviye sayıları")
    o.add_argument("--gun", type=int, default=7)
    a = ap.parse_args(argv)
    return _son(a) if a.komut == "son" else _ozet(a)


if __name__ == "__main__":
    sys.exit(main())
