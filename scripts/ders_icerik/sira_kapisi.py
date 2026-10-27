#!/usr/bin/env python3
"""Sıralı tablo kapısı (H105): Sıra/Adım/Aşama sütunlu tablolarda numaralar 1'den kesintisiz olmalı.
Kullanım: python3 scripts/ders_icerik/sira_kapisi.py [dosya.json ...]  (varsayılan: src/data/ders_icerik/*.json)"""
import glob, json, re, sys
SIRA = re.compile(r'^(sıra|adım|aşama|#|no)$', re.I)
hata = 0
for p in sys.argv[1:] or sorted(glob.glob('src/data/ders_icerik/*.json')):
    for t in json.load(open(p)).get('tablolar', []):
        if not t.get('h') or not SIRA.match(t['h'][0].strip()): continue
        nums = [r[0].strip() for r in t['r']]
        if not all(n.isdigit() for n in nums): continue
        if [int(n) for n in nums] != list(range(1, len(nums) + 1)):
            hata += 1; print(f"HATA {p}: «{t['t']}» sıra {nums}")
print(f"{hata} HATA"); sys.exit(1 if hata else 0)
