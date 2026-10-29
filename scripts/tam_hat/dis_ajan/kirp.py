#!/usr/bin/env python3
"""Sayfa görüntüsünden oranla kırpma (şekil/çizim okumada parçalara bakmak için). LLM yok.

  python3 scripts/tam_hat/dis_ajan/kirp.py <op/s-12.png> <x0> <y0> <x1> <y1> [--cikti dosya.png] [--buyut 2]
Koordinatlar 0–1 ORAN (sol-üst = 0,0). Örn. sayfanın üst yarısı: 0 0 1 0.5. Çıktı varsayılan: <W>/kirpik_<ad>_<x0>_<y0>.png.
Kırpığı aç ve oku; çizim koordinatını doğrulamak için de kullan (anlatılan şey kırpıkta duruyor mu?).
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image


def main() -> int:
    if len(sys.argv) < 6:
        print(__doc__)
        return 2
    yol = Path(sys.argv[1])
    x0, y0, x1, y1 = (float(v) for v in sys.argv[2:6])
    if not (0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1):
        print("HATA oranlar 0≤x0<x1≤1 ve 0≤y0<y1≤1 olmalı")
        return 1
    im = Image.open(yol)
    w, h = im.size
    k = im.crop((int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h)))
    b = int(sys.argv[sys.argv.index("--buyut") + 1]) if "--buyut" in sys.argv else 2
    k = k.resize((k.width * b, k.height * b), Image.LANCZOS)
    cikti = Path(sys.argv[sys.argv.index("--cikti") + 1]) if "--cikti" in sys.argv else yol.with_name(f"kirpik_{yol.stem}_{x0:g}_{y0:g}.png")
    k.save(cikti)
    print(f"kırpık yazıldı: {cikti} ({k.width}x{k.height})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
