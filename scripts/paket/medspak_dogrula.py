#!/usr/bin/env python3
"""`.medspak` kapısı (R7, ICERIK_MOTORU_V3.md §6): her kimlik çözülür, türev veriler aynı metin sürümünden, boyut tavanı.

  - meta: surum, ders_id, deste_id, metin_hash zorunlu
  - deste var; cümlelerin slayt_adim'i destenin slideNumber'larından
  - cizim.cumle_id ve soru.bagli_cumle var olan cümleye
  - ses_parca.metin_hash == meta.metin_hash (sesli metin değişince eski ses pakete girmez); işaret ve çizim metin özeti
    birbirine eşit (aynı sürüm)
  - öğrenci indirmesinde (ekler=0) ek tablosu boş; dosya ≤ 150 MB
Kullanım: python3 scripts/paket/medspak_dogrula.py <paket.medspak> …   → "N HATA"
"""
from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

TAVAN_MB = 150


def denetle(yol: Path) -> list[str]:
    e = []
    db = sqlite3.connect(yol)
    meta = dict(db.execute("SELECT anahtar, deger FROM meta"))
    for k in ("surum", "ders_id", "deste_id", "metin_hash"):
        if not meta.get(k):
            e.append(f"meta.{k} yok")
    d = db.execute("SELECT json FROM deste WHERE id=?", (meta.get("deste_id"),)).fetchone()
    adimlar = {s.get("slideNumber") for s in json.loads(d[0]).get("slides", [])} if d else set()
    if not d:
        e.append(f"deste {meta.get('deste_id')} pakette yok")
    cum = {r[0]: r[1] for r in db.execute("SELECT id, slayt_adim FROM cumle")}
    if not cum:
        e.append("cümle yok")
    kotu = [c for c, a in cum.items() if a is not None and adimlar and a not in adimlar]
    if kotu:
        e.append(f"{len(kotu)} cümlenin slayt adımı destede yok (ör. {kotu[0]})")
    for (c,) in db.execute("SELECT DISTINCT cumle_id FROM cizim"):
        if c not in cum:
            e.append(f"çizim bilinmeyen cümleye: {c}")
    for (q, c) in db.execute("SELECT id, bagli_cumle FROM soru WHERE bagli_cumle IS NOT NULL"):
        if c not in cum:
            e.append(f"soru {q} bilinmeyen cümleye bağlı: {c}")
    for (v, h) in db.execute("SELECT varyant, metin_hash FROM ses_parca"):
        if h != meta.get("metin_hash"):
            e.append(f"ses {v}: metin özeti {h} ≠ paketin metni {meta.get('metin_hash')} (eski metnin sesi)")
    if db.execute("SELECT COUNT(*) FROM cizim").fetchone()[0] and meta.get("cizim_metin_hash") != meta.get("isaret_metin_hash"):
        e.append("çizim ve işaret farklı metin sürümünden")
    if meta.get("ekler") in ("0", 0) and db.execute("SELECT COUNT(*) FROM ek").fetchone()[0]:
        e.append("öğrenci paketinde ek (PDF/öğrenci notu/hoca kaydı) var")
    mb = yol.stat().st_size / 1048576
    if mb > TAVAN_MB:
        e.append(f"paket {mb:.0f} MB (tavan {TAVAN_MB})")
    db.close()
    return e


if __name__ == "__main__":
    toplam = 0
    for a in sys.argv[1:]:
        h = denetle(Path(a))
        for x in h:
            print("  HATA", x)
        print(f"{a}: {len(h)} HATA")
        toplam += len(h)
    sys.exit(1 if toplam else 0)
