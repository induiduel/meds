#!/usr/bin/env python3
"""Her sınav spotunu kendi dersinin en yakın kazanımına eşler (Sınav spotları → Kazanım süzgeci).

Girdi: meds/src/data/exam_spots_k1.json + meds/src/data/kazanimlar/byDeck.json ("k1p-<ders id>")
Çıktı: meds/src/data/exam_spots_k1_kazanim.json → {"dersler": {"<no>": ["kazanım", ...]}, "spotlar": {"<spot id>": idx}}
Vektörleme yalnız CPU servisiyle (meds-embed-bge, scripts/altyapi/agents/lib.py::embed); GPU/LLM yok.
birlestir.py spotları yeniden ürettikten sonra bu betik de çalıştırılır.
Kullanım: CUDA_VISIBLE_DEVICES="" python3 meds/scripts/uretim/sinav_spotlari/kazanim_esle.py
"""
from __future__ import annotations
# Konum-bağımsız kök (2026-11-16): sabit parents[N] yerine scripts/kok.py (dosya taşınsa da doğru).
import sys as _sys
from pathlib import Path as _Path
_d = _Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in _sys.path:
    _sys.path.append(str(_d))
import kok as _kok  # noqa: E402

import json
import os
import sys
from pathlib import Path

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")
ROOT = _kok.PROJE
sys.path.insert(0, str(ROOT / "meds/scripts/altyapi/agents"))
from lib import embed  # noqa: E402

SPOT = ROOT / "meds/src/data/exam_spots_k1.json"
KAZ = ROOT / "meds/src/data/kazanimlar/byDeck.json"
CIKTI = ROOT / "meds/src/data/exam_spots_k1_kazanim.json"


def main() -> int:
    veri = json.loads(SPOT.read_text())
    kaz = json.loads(KAZ.read_text())
    out_d: dict[str, list[str]] = {}
    out_s: dict[str, int] = {}
    for d in veri["dersler"]:
        liste = [k["m"].strip() for k in kaz.get(f"k1p-{d['id']}", []) if k.get("m")]
        spotlar = [s for s in veri["spotlar"] if s["ders"] == d["no"]]
        if not liste or not spotlar:
            continue
        out_d[str(d["no"])] = liste
        kv = embed(liste, model="bge-m3")
        sv = embed([" ".join(filter(None, [s["baslik"], s["spot"].replace("**", ""), s.get("soru", ""), *(s.get("etiketler") or [])])) for s in spotlar], model="bge-m3")
        best = (sv @ kv.T).argmax(axis=1)
        for s, i in zip(spotlar, best):
            out_s[s["id"]] = int(i)
        print(f"ders {d['no']:>2}: {len(spotlar)} spot → {len(liste)} kazanım")
    CIKTI.write_text(json.dumps({"dersler": out_d, "spotlar": out_s}, ensure_ascii=False, separators=(",", ":")))
    print(f"{len(out_s)} / {len(veri['spotlar'])} spot eşlendi → {CIKTI.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
