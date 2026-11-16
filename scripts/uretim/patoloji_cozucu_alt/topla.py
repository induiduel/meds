#!/usr/bin/env python3
"""Alternatif soru çözücü dizini: metin + ses kayıtlarından index.json üretir."""
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
from pathlib import Path

MEDS = _kok.MEDS
KOK = MEDS / "data/patoloji_cozucu_alt"
KAYNAK_INDEX = MEDS / "src/data/patoloji_cozucu/index.json"


def main() -> None:
    no_by_kod = {
        d["kod"]: d.get("no", 999)
        for d in json.loads(KAYNAK_INDEX.read_text(encoding="utf-8"))["dersler"]
    }
    dersler = []
    for p in sorted((KOK / "metin").glob("*.json")):
        if p.name.startswith("tum_"):
            continue
        d = json.loads(p.read_text(encoding="utf-8"))
        kod = d["kod"]
        ders_no = d.get("no") or no_by_kod.get(kod) or int("".join(c for c in kod if c.isdigit()) or 999)
        ses_klasor = KOK / "ses" / kod
        kayit = json.loads((ses_klasor / "kayit.json").read_text(encoding="utf-8")) if (ses_klasor / "kayit.json").exists() else {}
        sure = round(sum(v.get("sure", 0) for v in kayit.values()), 1)
        dersler.append({
            "kod": kod,
            "no": ders_no,
            "baslik": d["baslik"],
            "soru": len(d["sorular"]),
            "ornek": sum(1 for s in d["sorular"] if s["tur"] == "ornek"),
            "cikmis": sum(1 for s in d["sorular"] if s["tur"] == "cikmis"),
            "ses": len(kayit),
            "sure": int(sure),
        })
        print(f"{kod} (Ders {ders_no}): {len(d['sorular'])} soru, {len(kayit)} ses, {sure:.0f} sn")

    dersler.sort(key=lambda x: (x["no"], x["kod"]))
    index = {"surum": "patoloji-cozucu-alt-2", "ses": "EMA Lightning", "dersler": dersler}
    (KOK / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    print("TOPLAM", sum(x["soru"] for x in dersler), "soru,", sum(x["sure"] for x in dersler), "sn ses")


if __name__ == "__main__":
    main()
