#!/usr/bin/env python3
"""Takvime göre kurul durumu (tek doğruluk kaynağı: src/data/kurul_takvimi.json).

  aktif_kurul.py               → bugün çalışılan kurul (sınavı henüz geçmemiş ilk kurul)
  aktif_kurul.py --son-sinav   → sınavı en son yapılmış kurul (olası soru gece işi bunu kullanır)
  aktif_kurul.py --json        → tam durum
  --tarih YYYY-AA-GG           → başka bir gün için
Sunucu/ön yüz aynı kuralı src/services/kurulTakvimi.ts ile uygular.
"""
import argparse, datetime as dt, json
from pathlib import Path

T = Path(__file__).resolve().parents[2] / "src/data/kurul_takvimi.json"


def durum(gun):
    k = json.loads(T.read_text())["kurullar"]
    aktif = next((x for x in k if gun <= x["sinav"]), k[-1])
    son = max((x for x in k if x["sinav"] <= gun), key=lambda x: x["sinav"], default=None)
    return {"tarih": gun, "aktif": aktif["kurul"], "aktif_ad": aktif["ad"], "aktif_sinav": aktif["sinav"],
            "sinava_gun": (dt.date.fromisoformat(aktif["sinav"]) - dt.date.fromisoformat(gun)).days,
            "son_sinav": son["kurul"] if son else None, "arsiv": [x["kurul"] for x in k if x["sinav"] < gun]}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--tarih", default=dt.date.today().isoformat())
    ap.add_argument("--son-sinav", action="store_true"); ap.add_argument("--json", action="store_true")
    a = ap.parse_args(); d = durum(a.tarih)
    print(json.dumps(d, ensure_ascii=False) if a.json else (d["son_sinav"] or 0) if a.son_sinav else d["aktif"])
