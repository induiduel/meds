#!/usr/bin/env python3
"""Her sınav spotunu kendi dersinin en yakın kazanımına eşler (Sınav spotları → Kazanım süzgeci).

Girdi: meds/src/data/exam_spots_k1.json + meds/src/data/kazanimlar/byDeck.json ("k1p-<ders id>")
Çıktı: meds/src/data/exam_spots_k1_kazanim.json → {"dersler": {"<no>": ["kazanım", ...]}, "spotlar": {"<spot id>": idx}}
Vektörleme yalnız CPU servisiyle (meds-embed-bge, scripts/agents/lib.py::embed); GPU/LLM yok.
birlestir.py spotları yeniden ürettikten sonra bu betik de çalıştırılır.
Kullanım: CUDA_VISIBLE_DEVICES="" python3 meds/scripts/sinav_spotlari/kazanim_esle.py
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "meds/scripts/agents"))
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
