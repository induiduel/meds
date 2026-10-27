#!/usr/bin/env python3
"""Ders başına çıkmış soru üslubu: konuya en yakın çıkmışlardan az sayıda, kalıpça çeşitli örnek seçer (LLM yok).

  python3 scripts/tam_hat/soru_uslup_ornek.py <ders klasörü> [--n 8]

Girdi: <klasör>/cikmis_aday.json (hazirlik.py üretir: sitenin BM25 + bge-m3 araması; `kez` = kaç sayfa parçasında çıktı).
Çıktı: <klasör>/soru_uslubu.json
  ornekler       : n çıkmış (kök + şıklar), her kalıptan en az biri varsa o kalıp temsil edilir
  kalip_payi     : çıkmış adaylarda kalıp payları (olumsuz kök, vaka, öncüllü, doğrudan) — soru_uslup.py bununla kıyaslar
  kok_kelime_ort : çıkmış köklerin ortalama kelime sayısı
Yazar alt ajanı soru yazmadan önce yalnız bu dosyayı okur (bütün çıkmış bankası değil); örnek sayısı bilerek küçük tutulur.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

KALIPLAR = ("olumsuz", "vaka", "onculu", "dogrudan")


def kalip(kok: str) -> str:
    k = kok.lower()
    if re.search(r"\b(i{1,3}|iv)\.\s|ifadelerden|öncül|hangileri", k):
        return "onculu"
    if re.search(r"\d+\s*yaşında|yaşındaki|başvur|kliniğe|acile", k):
        return "vaka"
    if re.search(r"değildir|yanlıştır|yoktur|beklenmez|olamaz|söylenemez|dışında|bulunmaz|görülmez|yanlış olan", k):
        return "olumsuz"
    return "dogrudan"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("klasor", type=Path)
    ap.add_argument("--n", type=int, default=8)
    a = ap.parse_args()
    aday = json.loads((a.klasor / "cikmis_aday.json").read_text())
    aday = [x for x in aday if len(x.get("secenekler") or []) >= 4 and len((x.get("kok") or "").split()) >= 5]
    if not aday:
        print("HATA: kullanılabilir çıkmış aday yok (önce hazirlik.py)", file=sys.stderr)
        return 1
    aday.sort(key=lambda x: (-(x.get("kez") or 0), -(x.get("puan") or 0)))
    pay = {k: 0 for k in KALIPLAR}
    for x in aday:
        x["kalip"] = kalip(x["kok"])
        pay[x["kalip"]] += 1
    secilen: list[dict] = []
    for k in KALIPLAR:  # önce her kalıbın en yakın örneği
        ilk = next((x for x in aday if x["kalip"] == k), None)
        if ilk:
            secilen.append(ilk)
    for x in aday:  # kalan yerler yakınlık sırasıyla
        if len(secilen) >= a.n:
            break
        if x not in secilen:
            secilen.append(x)
    cikti = {
        "kaynak": "cikmis_aday.json",
        "aday_sayisi": len(aday),
        "kalip_payi": {k: round(v / len(aday), 2) for k, v in pay.items()},
        "kok_kelime_ort": round(sum(len(x["kok"].split()) for x in aday) / len(aday), 1),
        "ornekler": [{"kalip": x["kalip"], "kok": x["kok"], "secenekler": x["secenekler"]} for x in secilen[:a.n]],
    }
    (a.klasor / "soru_uslubu.json").write_text(json.dumps(cikti, ensure_ascii=False, indent=1))
    print(f"{len(cikti['ornekler'])} örnek · kalıp payı {cikti['kalip_payi']} · kök ort. {cikti['kok_kelime_ort']} kelime")
    return 0


if __name__ == "__main__":
    sys.exit(main())
