#!/usr/bin/env python3
"""Hedef kilidi (dış ajan protokolü §12-10). LLM yok.

  hedef.py yaz   <W> ad=min:max [ad=min:max …]     # iş başında BİR KEZ; W/hedef.json imzalanır, sonra değiştirilemez
  hedef.py kontrol <W> ad=ölçülen [ad=ölçülen …]   # tolerans: ad 'anlatim' ile başlıyorsa ±%20, değilse ±%10 (yalnız sayısal hedef)
  hedef.py dogrula <W>                             # dosya imzası bozulmamış mı
  hedef.py say <metin.md>                          # anlatım kelime sayısı (# ve @@ satırları hariç) — hedef kontrolde bunu kullan
Tolerans yalnız SAYI içindir; tıbbi doğruluk, kaynak, üslup ve ileri sızıntıda tolerans yoktur.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def imza(h: dict) -> str:
    return hashlib.sha256(json.dumps(h, sort_keys=True).encode()).hexdigest()


def oku(W: Path) -> dict:
    d = json.loads((W / "hedef.json").read_text("utf8"))
    if imza(d["hedefler"]) != d["imza"]:
        raise SystemExit("HATA [HEDEF-01] hedef.json imzası bozuk: hedef sonradan değiştirilmiş. Yapılacak: değiştirme; kullanıcıya bildir.")
    return d


def main() -> int:
    if len(sys.argv) < 3 or sys.argv[1] not in ("yaz", "kontrol", "dogrula", "say"):
        print(__doc__)
        return 2
    mod, W = sys.argv[1], Path(sys.argv[2])
    if mod == "say":
        print(sum(len(l.split()) for l in W.read_text("utf8").splitlines() if not l.startswith(("# ", "@@ "))))
        return 0
    if mod == "yaz":
        if (W / "hedef.json").exists():
            print("HATA [HEDEF-02] hedef.json zaten var; hedef sonradan değiştirilemez. Yapılacak: mevcut hedefe uy.")
            return 1
        h = {}
        for x in sys.argv[3:]:
            ad, _, r = x.partition("=")
            lo, _, hi = r.partition(":")
            h[ad] = [float(lo), float(hi)]
        if not h:
            print("HATA hedef verilmedi (ad=min:max)")
            return 2
        (W / "hedef.json").write_text(json.dumps({"hedefler": h, "imza": imza(h)}, indent=1), "utf8")
        print("hedef.json yazıldı (kilitli):", h)
        return 0
    d = oku(W)
    if mod == "dogrula":
        print("GEÇTİ: hedef.json bozulmamış")
        return 0
    kotu = 0
    for x in sys.argv[3:]:
        ad, _, v = x.partition("=")
        v = float(v)
        lo, hi = d["hedefler"].get(ad, [None, None])
        if lo is None:
            print(f"HATA [HEDEF-03] '{ad}' için hedef tanımlı değil.")
            kotu += 1
            continue
        pay = 0.20 if ad.startswith("anlatim") else 0.10
        if lo <= v <= hi:
            print(f"GEÇTİ {ad}={v:g} (hedef {lo:g}–{hi:g})")
        elif lo * (1 - pay) <= v <= hi * (1 + pay):
            print(f"UYARI {ad}={v:g} hedef dışı ama ±%{int(pay*100)} toleransta. Yapılacak: yalnız sapan bölümü düzelt; rapora yaz.")
        else:
            print(f"HATA [HEDEF-04] {ad}={v:g} toleransın dışında ({lo:g}–{hi:g}, ±%{int(pay*100)}). Yapılacak: yalnız sapan bölümü düzelt.")
            kotu += 1
    return 1 if kotu else 0


if __name__ == "__main__":
    sys.exit(main())
