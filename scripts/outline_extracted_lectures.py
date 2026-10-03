# -*- coding: utf-8 -*-
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

files = [
    'data/extracted_lectures/1_halk_sağlığıtarihçesi.txt',
    'data/extracted_lectures/4_enfeksiyon_hastalıklarında_temel_kavramlar_ve_genel_özellikler.txt',
    'data/extracted_lectures/5_enfeksiyon_hastalıklarının_genel_epidemiyolojik_özellikleri.txt',
    'data/extracted_lectures/4_üriner_sistem_enfeksiyonlarının_epidemiyoloji,_etyoloji_ve_semptomatolojisi.txt',
    'data/extracted_lectures/5_üriner_sistemin_spesifik_enfeksiyonları.txt',
    'data/extracted_lectures/2026-27_d3_ders_programı.txt'
]

for f in files:
    if os.path.exists(f):
        txt = open(f, encoding='utf-8').read()
        lines = [l.strip() for l in txt.split('\n') if l.strip()]
        print('='*70)
        print(f"{f} ({len(lines)} satır, {len(txt)} karakter)")
        print('Öne Çıkan Başlıklar / Satırlar:')
        for l in lines[:25]:
            if len(l) > 3 and not l.isdigit():
                print(f"  • {l[:95]}")
