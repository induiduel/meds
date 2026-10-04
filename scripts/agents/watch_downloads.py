#!/usr/bin/env python3
"""
meds_downloads izleyicisi: yeni/değişen PDF ve PPTX dosyalarını fark eder ve
read_document.py ile temp1'e çevirir (PROJE_TANITIMI.md, 1. aşama).

  watch_downloads.py            # sürekli izle
  watch_downloads.py --once     # bir kez tara ve çık
  watch_downloads.py --vision   # OCR yetersizse yerel görsel modeli de kullan
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from read_document import DEFAULT_DOWNLOADS, DEFAULT_TEMP1, SUPPORTED, process_file  # noqa: E402

STABLE_SECONDS = 8  # indirme bitmemiş dosyayı okumamak için son değişiklikten bu kadar bekle


def scan(root: Path, seen: dict[Path, tuple[float, int]], vision: bool, docling: bool = False) -> int:
    done = 0
    for f in sorted(root.rglob("*")):
        if not f.is_file() or f.suffix.lower() not in SUPPORTED or f.name.startswith(("~$", ".")):
            continue
        if f.name.endswith((".crdownload", ".part", ".tmp")):
            continue
        st = f.stat()
        key = (st.st_mtime, st.st_size)
        if seen.get(f) == key:
            continue
        if time.time() - st.st_mtime < STABLE_SECONDS:
            continue  # hâlâ yazılıyor olabilir
        try:
            process_file(f, DEFAULT_TEMP1, root, force=False, use_ocr=True, use_vision=vision, use_docling=docling)
            seen[f] = key
            done += 1
        except Exception as e:
            print(f"✗ HATA {f.name}: {e}", file=sys.stderr)
            seen[f] = key  # aynı hatayı döngüde tekrarlama; dosya değişirse yeniden denenir
    return done


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--vision", action="store_true")
    ap.add_argument("--docling", action="store_true")
    ap.add_argument("--interval", type=int, default=15, help="tarama aralığı (sn)")
    ap.add_argument("--dir", type=Path, default=DEFAULT_DOWNLOADS)
    a = ap.parse_args()

    a.dir.mkdir(parents=True, exist_ok=True)
    seen: dict[Path, tuple[float, int]] = {}
    print(f"İzleniyor: {a.dir}  ->  {DEFAULT_TEMP1}")
    while True:
        scan(a.dir, seen, a.vision, a.docling)
        if a.once:
            break
        time.sleep(a.interval)


if __name__ == "__main__":
    main()
