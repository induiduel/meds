#!/usr/bin/env python3
"""Sesli ders v2 cümlelerine geçmiş yıl öğrenci önem etiketi yazar (ekranda "Öğrenciler buraya çalıştı" rozeti).

  python3 scripts/ogrenci_onem/v2_etiketle.py <sesli ders anahtarı> [--ders k2-05] [--yaz]

Her A/B biriminin bilgileri (el notu, vurgulu satır, çıkmış önermesi) cümle düzeyinde aranır (kapi.kapsandi: vektör + kelime kökü);
birimin bilgisini taşıyan en iyi en çok 2 cümle `ogrenci: {"oncelik": "A|B", "birim": "<id>"}` alır. Önceki etiketler silinip yeniden
yazılır (kimlik ve metin değişmez; konusma_v2 şeması `ogrenci` alanını tanır). --yaz yoksa yalnız rapor.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agents"))
from kapi import kapsandi, kokler  # noqa: E402
from ortak import CIKTI, KOK, bilgiler, oku_json  # noqa: E402

BIRIM_BASINA = 2


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("key"); ap.add_argument("--ders"); ap.add_argument("--yaz", action="store_true")
    a = ap.parse_args()
    from lib import embed  # noqa: E402
    ders = a.ders or re.match(r"k\d+-\d+", a.key).group(0)
    on = oku_json(CIKTI / f"{ders}.json")
    p = KOK / f"data/sesli_anlatim/v2/{a.key}.json"
    v = oku_json(p)
    if not on or not v:
        sys.exit(f"veri yok: {ders} / {p}")
    cs = [c for b in v["bolumler"] for pr in b["paragraflar"] for c in pr["cumleler"]]
    # ses okunuşla ("Düşen"), ekran yazımla ("Duchenne") yazılır: ikisi de aday, ikisi de aynı cümleye döner
    metin = [c["ses"] for c in cs] + [c.get("ekran", "").replace("**", "") or c["ses"] for c in cs]
    CV = embed(metin, model="bge-m3")
    CK = [kokler(t) for t in metin]
    secim: dict[int, tuple[str, str, float]] = {}
    rapor = []
    for b in on["birimler"]:
        if b["oncelik"] not in ("A", "B"):
            continue
        bl = bilgiler(b, on)
        if not bl:
            continue
        BV = embed([x["metin"] for x in bl], model="bge-m3")
        puan: dict[int, float] = defaultdict(float)
        for x, bv in zip(bl, BV):
            ok, sk, cm = kapsandi(x["metin"], bv, metin, CV, CK, x.get("cevap", ""))
            if ok:
                j = metin.index(cm) % len(cs)
                puan[j] += sk + (0.5 if x["tur"] == "cikmis" else 0)
        en = sorted(puan.items(), key=lambda z: -z[1])[:BIRIM_BASINA]
        for j, sk in en:
            onceki = secim.get(j)
            if not onceki or (onceki[0] == "B" and b["oncelik"] == "A") or (onceki[0] == b["oncelik"] and sk > onceki[2]):
                secim[j] = (b["oncelik"], b["id"], sk)
        rapor.append(f"{b['oncelik']} {b['id']:14} {b['baslik'][:50]:50} → " + (", ".join(cs[j]["id"] for j, _ in en) or "ANLATIMDA YOK"))
    for c in cs:
        c.pop("ogrenci", None)
    for j, (o, bid, _) in secim.items():
        cs[j]["ogrenci"] = {"oncelik": o, "birim": bid}
    print("\n".join(rapor))
    print(f"{a.key}: {len(secim)} cümle etiketlendi (A {sum(1 for x in secim.values() if x[0] == 'A')}, B {sum(1 for x in secim.values() if x[0] == 'B')})")
    if a.yaz:  # dosyanın kendi biçimi korunur (v2 dosyaları sıkıştırılmış tek satır) → fark yalnız etiketler
        sik = "\n" not in p.read_text().strip()
        p.write_text(json.dumps(v, ensure_ascii=False, separators=(",", ":")) if sik else json.dumps(v, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
