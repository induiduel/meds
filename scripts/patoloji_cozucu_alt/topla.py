#!/usr/bin/env python3
"""Alternatif soru çözücü dizini: metin + ses kayıtlarından index.json üretir."""
from __future__ import annotations

import json
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
KOK = MEDS / "data/patoloji_cozucu_alt"


def main() -> None:
    dersler = []
    for p in sorted((KOK / "metin").glob("*.json")):
        if p.name.startswith("tum_"):
            continue
        d = json.loads(p.read_text(encoding="utf-8"))
        ses_klasor = KOK / "ses" / d["kod"]
        kayit = json.loads((ses_klasor / "kayit.json").read_text(encoding="utf-8")) if (ses_klasor / "kayit.json").exists() else {}
        sure = round(sum(v.get("sure", 0) for v in kayit.values()), 1)
        dersler.append({
            "kod": d["kod"], "baslik": d["baslik"], "soru": len(d["sorular"]),
            "ornek": sum(1 for s in d["sorular"] if s["tur"] == "ornek"),
            "cikmis": sum(1 for s in d["sorular"] if s["tur"] == "cikmis"),
            "ses": len(kayit), "sure": int(sure),
        })
        print(f"{d['kod']}: {len(d['sorular'])} soru, {len(kayit)} ses, {sure:.0f} sn")
    index = {"surum": "patoloji-cozucu-alt-1", "ses": "EMA Lightning", "dersler": dersler}
    (KOK / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    print("TOPLAM", sum(x["soru"] for x in dersler), "soru,", sum(x["sure"] for x in dersler), "sn ses")


if __name__ == "__main__":
    main()
