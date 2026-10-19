#!/usr/bin/env python3
"""Alternatif soru çözücü — ön yüz paketi.

Girdi : meds/data/patoloji_cozucu_alt/{metin,ses}
Çıktı : meds/src/data/patoloji_cozucu_alt/index.json ve <kod>.json
        (uygulama bunları import.meta.glob ile paketler; ses /api/patoloji-cozucu-alt/ses/<kod>/<no>.mp3)
"""
from __future__ import annotations

import json
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
KOK = MEDS / "data/patoloji_cozucu_alt"
HEDEF = MEDS / "src/data/patoloji_cozucu_alt"
KAYNAK_INDEX = MEDS / "src/data/patoloji_cozucu/index.json"


def main() -> None:
    HEDEF.mkdir(parents=True, exist_ok=True)
    no_by_kod = {d["kod"]: d.get("no") for d in json.loads(KAYNAK_INDEX.read_text(encoding="utf-8"))["dersler"]}
    dersler = []
    for p in sorted((KOK / "metin").glob("*.json")):
        if p.name.startswith("tum_"):
            continue
        d = json.loads(p.read_text(encoding="utf-8"))
        kod = d["kod"]
        kayit_p = KOK / "ses" / kod / "kayit.json"
        kayit = json.loads(kayit_p.read_text(encoding="utf-8")) if kayit_p.exists() else {}
        sorular = []
        for s in d["sorular"]:
            k = kayit.get(str(s["no"]), {})
            sorular.append({
                "no": s["no"], "tur": s["tur"], "soru": s["soru"],
                "secenekler": s["secenekler"], "dogru": s["dogru"],
                "giris": s["giris"], "aciklamalar": s["aciklamalar"], "ozet": s["ozet"],
                "mp3": f"{s['no']}.mp3", "h": k.get("h", ""), "sure": k.get("sure", 0),
            })
        ders = {
            "kod": kod, "no": no_by_kod.get(kod) or int("".join(c for c in kod if c.isdigit()) or 0),
            "baslik": d["baslik"], "sorular": sorular,
        }
        (HEDEF / f"{kod}.json").write_text(json.dumps(ders, ensure_ascii=False), encoding="utf-8")
        dersler.append({
            "kod": kod, "no": ders["no"], "baslik": d["baslik"], "soru": len(sorular),
            "ornek": sum(1 for s in sorular if s["tur"] == "ornek"),
            "cikmis": sum(1 for s in sorular if s["tur"] == "cikmis"),
            "sure": round(sum(s["sure"] for s in sorular)),
        })
    index = {"surum": "patoloji-cozucu-alt-1", "dersler": dersler}
    (HEDEF / "index.json").write_text(json.dumps(index, ensure_ascii=False), encoding="utf-8")
    print(f"{len(dersler)} ders, {sum(d['soru'] for d in dersler)} soru → {HEDEF}")


if __name__ == "__main__":
    main()
