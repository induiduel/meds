#!/usr/bin/env python3
"""
Müfredat bilgi paketi — Dönem 3 ders programı (Faz 8 ağacı): kurul → ders → konu.

Faz 14, örnek soru üretici ve site API'si (/api/curriculum/package) bu paketi kullanır. Kazanım metinleri ağaçta
çoğunlukla bozuk olduğu için pakete yalnız kurul/ders/konu (ve ders saati) girer.
Model istemine hep AYNI metin, istemin EN BAŞINDA verilir: Gemini aynı ön eki otomatik önbelleğe alır
(implicit caching) — ek ücret yok, önbellekten okunan kısım indirimli.

Kaynak: $MEDS_DATABASE_DIR/derived/curriculum_links/agac.json
Çıktı:  $MEDS_DATABASE_DIR/derived/curriculum_links/mufredat_paketi.json (ve .txt)
Kullanım: python3 curriculum_package.py   (paketi yeniden üretir ve özetini yazar)
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

ROOT = _kok.MEDS
DB = Path(os.environ.get("MEDS_DATABASE_DIR") or ROOT.parent / "meds_database")
TREE = DB / "derived" / "curriculum_links" / "agac.json"
OUT_JSON = DB / "derived" / "curriculum_links" / "mufredat_paketi.json"
OUT_TXT = OUT_JSON.with_suffix(".txt")


def build() -> dict:
    a = json.loads(TREE.read_text(encoding="utf-8"))
    kurullar = []
    for k in a.get("kurullar") or []:
        dersler = []
        for d in k.get("dersler") or []:
            konular = [c.get("ad") for c in d.get("konular") or [] if c.get("ad")]
            if konular:
                dersler.append({"ders": d.get("ad"), "saat": d.get("saat"), "konular": konular})
        kurullar.append({"kurul": k.get("kurul"), "kod": k.get("kod"), "ad": k.get("ad"), "dersler": dersler})
    return {"donem": 3, "kaynak": "Faz 8 müfredat ağacı (resmî 2026-27 ders programı)", "kurullar": kurullar}


def as_text(pkg: dict, kurul: int | None = None) -> str:
    """Model istemi için kısa düz metin. kurul verilirse yalnız o kurul."""
    lines = ["DÖNEM 3 MÜFREDAT PAKETİ (kurul → ders → konular). Kurul kodu: kurul N = TIP3N0."]
    for k in pkg["kurullar"]:
        if kurul is not None and k["kurul"] != kurul:
            continue
        lines.append(f"\n## Kurul {k['kurul']} ({k['kod']}) — {k['ad']}")
        for d in k["dersler"]:
            lines.append(f"- {d['ders']}: " + "; ".join(d["konular"]))
    return "\n".join(lines)


def load(rebuild: bool = False) -> dict:
    """Paketi döndür; ağaç paketten yeniyse (ya da yoksa) yeniden üretir."""
    if not rebuild and OUT_JSON.exists() and (not TREE.exists() or OUT_JSON.stat().st_mtime >= TREE.stat().st_mtime):
        return json.loads(OUT_JSON.read_text(encoding="utf-8"))
    pkg = build()
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    tmp = OUT_JSON.with_suffix(".tmp")
    tmp.write_text(json.dumps(pkg, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(OUT_JSON)
    OUT_TXT.write_text(as_text(pkg), encoding="utf-8")
    return pkg


def find_topic(pkg: dict, kurul: int | None, ders: str | None) -> list[str]:
    for k in pkg["kurullar"]:
        if kurul is not None and k["kurul"] != kurul:
            continue
        for d in k["dersler"]:
            if ders and d["ders"].lower() == ders.lower():
                return d["konular"]
    return []


if __name__ == "__main__":
    p = load(rebuild=True)
    t = as_text(p)
    print(json.dumps({"kurul": len(p["kurullar"]), "ders": sum(len(k["dersler"]) for k in p["kurullar"]),
                      "konu": sum(len(d["konular"]) for k in p["kurullar"] for d in k["dersler"]),
                      "metin_karakter": len(t), "yaklasik_token": len(t) // 3, "dosya": str(OUT_JSON)}, ensure_ascii=False))
    sys.exit(0)
