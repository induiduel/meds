#!/usr/bin/env python3
"""Doğrulanmış sınav spotlarını site verisine yazar.

Girdi: meds_temp/sinav_spotlari/spotlar/*.jsonl (dogrula.py 0 HATA olmalı)
Çıktı: meds_database_v2/sinav_spotlari_k1/spotlar.json (arşiv) + meds/src/data/exam_spots_k1.json (site)
Kullanım: python3 meds/scripts/sinav_spotlari/birlestir.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SPOT_DIR = ROOT / "meds_temp/sinav_spotlari/spotlar"
INDEX = ROOT / "meds_database_v2/ders_notlari_k1/index.json"
ARSIV = ROOT / "meds_database_v2/sinav_spotlari_k1/spotlar.json"
SITE = ROOT / "meds/src/data/exam_spots_k1.json"
ALAN = ("id", "kategori", "onem", "baslik", "spot", "maddeler", "soru", "cevap", "tuzak", "karsilastir", "etiketler")


def main() -> int:
    r = subprocess.run([sys.executable, str(Path(__file__).parent / "dogrula.py")], capture_output=True, text=True)
    print(r.stdout.splitlines()[0] if r.stdout else r.stderr)
    if r.returncode != 0:
        print("Doğrulama HATA verdi; birleştirme yapılmadı.")
        return 1
    dersler = {d["sira"]: d for d in json.loads(INDEX.read_text())}
    out_d, spots = [], []
    for f in sorted(SPOT_DIR.glob("*.jsonl")):
        satir = [json.loads(l) for l in f.read_text().splitlines() if l.strip()]
        if not satir:
            continue
        no = satir[0]["ders_no"]
        d = dersler.get(no, {})
        out_d.append({"no": no, "id": d.get("id"), "baslik": d.get("title"), "disiplin": d.get("ders"),
                      "hoca": d.get("ogretim_uyesi"), "tarih": d.get("program_tarihi"), "sayi": len(satir)})
        for s in satir:
            o = {k: s[k] for k in ALAN if s.get(k) not in (None, "", [])}
            o["ders"] = no
            o["kaynak"] = [{"satir": q.get("satir"), "alinti": q.get("alinti")} for q in s.get("kaynak") or []]
            spots.append(o)
    data = {"surum": 1, "kurul": 1, "uretildi": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "kaynak": "meds_database_v2/ders_notlari_k1/notlar", "dersler": out_d, "spotlar": spots}
    ARSIV.parent.mkdir(parents=True, exist_ok=True)
    ARSIV.write_text(json.dumps(data, ensure_ascii=False, indent=1))
    SITE.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    print(f"{len(out_d)} ders, {len(spots)} spot → {SITE.relative_to(ROOT)} ({SITE.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
