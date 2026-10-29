#!/usr/bin/env python3
"""Müfredat sözlüğünde terim ara (tanım cümlesi türü için tek geçerli kaynak). LLM yok.

  python3 scripts/tam_hat/dis_ajan/sozluk_ara.py <terim> [<terim> …]
Kaynak: src/data/medical_glossary.json (+ terim_yardimcisi_sozluk.json). Çıktıdaki anahtar, `uretim` kaydındaki "sozluk" alanına AYNEN yazılır.
Bulunmayan terim için tanım cümlesi yazılamaz (kaynak dışı bilgi yasağı).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ortak import katla  # noqa: E402

KOK = Path(__file__).resolve().parents[3]
KAYNAK = [KOK / "src/data/medical_glossary.json", KOK / "src/data/terim_yardimcisi_sozluk.json"]


def yukle_hepsi() -> dict:
    out = {}
    for f in KAYNAK:
        try:
            for k, v in json.loads(f.read_text("utf8")).items():
                out.setdefault(k, v)
        except Exception:  # noqa: BLE001
            pass
    return out


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    sozluk = yukle_hepsi()
    kat = {katla(k): k for k in sozluk}
    for t in sys.argv[1:]:
        ft = katla(t)
        tam = [kat[k] for k in kat if k == ft]
        iceren = [kat[k] for k in kat if ft in k and k != ft][:8]
        print(f"== {t}")
        if not tam and not iceren:
            print("   BULUNAMADI: bu terim için tanım cümlesi yazamazsın.")
        for k in tam + iceren:
            v = sozluk[k]
            print(f"   sozluk={k!r}\n   tanım: {str(v.get('definition', ''))[:300]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
