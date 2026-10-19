#!/usr/bin/env python3
"""Alternatif soru çözücü doğrulayıcı: metin + ses bütünlüğü."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
KOK = MEDS / "data/patoloji_cozucu_alt"
YASAK = ("pdf", "slayt", "ders notu", "talimat", "şıkkı")


def main() -> int:
    hata = 0
    toplam = 0
    for p in sorted((KOK / "metin").glob("*.json")):
        if p.name.startswith("tum_"):
            continue
        d = json.loads(p.read_text(encoding="utf-8"))
        kayit_p = KOK / "ses" / d["kod"] / "kayit.json"
        kayit = json.loads(kayit_p.read_text(encoding="utf-8")) if kayit_p.exists() else {}
        for q in d["sorular"]:
            toplam += 1
            ad = f"{d['kod']}/{q['no']}"
            if not q["metin"].strip() or not q["ses"].strip():
                print(f"HATA {ad}: boş metin/ses"); hata += 1
            if not 60 <= q["kelime"] <= 320:
                print(f"HATA {ad}: kelime {q['kelime']}"); hata += 1
            for k in YASAK:
                if k in q["metin"].lower():
                    print(f"HATA {ad}: yasak ifade '{k}'"); hata += 1
            if not re.search(r"\b[ABCDE]\b", q["metin"]):
                print(f"HATA {ad}: cevap harfi yok"); hata += 1
            mp3 = KOK / "ses" / d["kod"] / f"{q['no']}.mp3"
            if not mp3.exists() or mp3.stat().st_size < 5000:
                print(f"HATA {ad}: ses yok/küçük"); hata += 1
            elif not kayit.get(str(q["no"]), {}).get("sure", 0) > 5:
                print(f"HATA {ad}: süre kaydı yok"); hata += 1
            if re.search(r"\d", q["ses"]):
                print(f"HATA {ad}: ses metninde rakam"); hata += 1
    print(f"{toplam} soru denetlendi · {hata} HATA")
    return 1 if hata else 0


if __name__ == "__main__":
    sys.exit(main())
