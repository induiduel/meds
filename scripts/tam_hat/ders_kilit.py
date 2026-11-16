#!/usr/bin/env python3
"""Ders bazlı kilit — aynı dersi iki oturumun aynı anda işleyip birbirinin işini ezmesini önler
(kullanıcı kararı 2026-11-16: 6. partide dört ders iki oturumda işlendi, biri diğerinin 60 soruluk setini ezdi).

Kilit dosyası: meds/data/ders_kilit/<key>.json {oturum, host, pid, baslama, son_canli, asama}.
Aynı makinedeki oturumlar dosya sistemini paylaşır; kilit onları kapsar. Kilit bayatsa (sahip süreç ölü ya da
>KADER_SN sessiz) kendiliğinden kırılır.

  ders_kilit.py al  <key> [--asama E0] [--oturum ID]   → kilidi al; başkası tutuyorsa çıkış 1 (kimin tuttuğunu yazar)
  ders_kilit.py canli <key> [--oturum ID]              → son_canli'yi tazele (uzun işlerde bayatlamayı önler)
  ders_kilit.py birak <key> [--oturum ID]              → kilidi bırak (yalnız sahibi)
  ders_kilit.py durum [<key>]                          → kilit(ler) durumu
Oturum kimliği: --oturum ya da MEDS_OTURUM ortam değişkeni; yoksa host:pid türetilir.
"""
from __future__ import annotations

import argparse
import json
import os
import socket
import sys
import time
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
KILIT_DIR = KOK / "data" / "ders_kilit"
KADER_SN = 6 * 3600  # 6 saat sessiz kalan kilit bayat sayılır


def _oturum(verilen: str | None) -> str:
    return verilen or os.environ.get("MEDS_OTURUM") or f"{socket.gethostname()}:{os.getppid()}"


def _canli_mi(k: dict) -> bool:
    """Kilit hâlâ geçerli mi: yeterince taze ve (aynı hosttaysa) süreç yaşıyor mu."""
    if time.time() - k.get("son_canli", 0) > KADER_SN:
        return False
    if k.get("host") == socket.gethostname() and k.get("pid"):
        try:
            os.kill(int(k["pid"]), 0)        # süreç yaşıyor → kilit canlı
        except ProcessLookupError:
            return False                      # süreç yok → bayat
        except (PermissionError, ValueError):
            return True                       # süreç var (başka kullanıcı) ya da pid okunamadı → canlı say
    return True


def _oku(p: Path) -> dict | None:
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def al(key: str, asama: str, oturum: str) -> int:
    KILIT_DIR.mkdir(parents=True, exist_ok=True)
    p = KILIT_DIR / f"{key}.json"
    mevcut = _oku(p)
    if mevcut and mevcut.get("oturum") != oturum and _canli_mi(mevcut):
        yas = round((time.time() - mevcut.get("son_canli", 0)) / 60)
        print(f"KİLİTLİ: {key} başka oturumda ({mevcut.get('oturum')}, {yas} dk önce, aşama {mevcut.get('asama')}). "
              f"Bırakması beklenir ya da bayatlar (>{KADER_SN // 3600} saat).", file=sys.stderr)
        return 1
    t = time.time()
    p.write_text(json.dumps({"oturum": oturum, "host": socket.gethostname(), "pid": os.getppid(),
                             "baslama": (mevcut or {}).get("baslama", t) if mevcut and mevcut.get("oturum") == oturum else t,
                             "son_canli": t, "asama": asama}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"kilit alındı: {key} (oturum {oturum}, aşama {asama})")
    return 0


def canli(key: str, oturum: str) -> int:
    p = KILIT_DIR / f"{key}.json"
    k = _oku(p)
    if not k or k.get("oturum") != oturum:
        print(f"UYARI: {key} kilidi sende değil; tazelenmedi", file=sys.stderr)
        return 1
    k["son_canli"] = time.time()
    p.write_text(json.dumps(k, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


def birak(key: str, oturum: str) -> int:
    p = KILIT_DIR / f"{key}.json"
    k = _oku(p)
    if k and k.get("oturum") not in (oturum, None):
        print(f"UYARI: {key} kilidi başka oturumda ({k.get('oturum')}); bırakılmadı", file=sys.stderr)
        return 1
    p.unlink(missing_ok=True)
    print(f"kilit bırakıldı: {key}")
    return 0


def durum(key: str | None) -> int:
    if not KILIT_DIR.exists():
        print("kilit yok")
        return 0
    for p in sorted(KILIT_DIR.glob("*.json")):
        if key and p.stem != key:
            continue
        k = _oku(p) or {}
        yas = round((time.time() - k.get("son_canli", 0)) / 60)
        print(f"  {p.stem}: {k.get('oturum')} · aşama {k.get('asama')} · {yas} dk · {'canlı' if _canli_mi(k) else 'BAYAT'}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("eylem", choices=("al", "canli", "birak", "durum"))
    ap.add_argument("key", nargs="?")
    ap.add_argument("--asama", default="?")
    ap.add_argument("--oturum")
    a = ap.parse_args()
    oturum = _oturum(a.oturum)
    if a.eylem == "durum":
        return durum(a.key)
    if not a.key:
        ap.error("key gerekli")
    return {"al": lambda: al(a.key, a.asama, oturum),
            "canli": lambda: canli(a.key, oturum),
            "birak": lambda: birak(a.key, oturum)}[a.eylem]()


if __name__ == "__main__":
    sys.exit(main())
