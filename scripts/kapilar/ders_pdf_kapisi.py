#!/usr/bin/env python3
"""Sesli ders PDF kapısı (H-PDF, 2026-11-06).

Belirti: yeni Kurul 2 derslerinde (Polinöropati, Bazal Ganglionlar) görüntüleyici PDF'i açamayıp "Drive'da aç" yedeğine düşüyordu.
Kök neden: (1) destesiz yeni dersin `deckId`'si `lecturePdfLocator.ts::SANAL_DESTELER`'e eklenmemişti; (2) eklenen kayıt
`meds-web` yeniden başlatılmadan sunucuda görünmüyordu (tsx watch yok, AGENTS 12).
Kapı: her hizalama dosyasının deckId'si sunucunun /api/lecture-pdf/decks kataloğunda en az bir açılabilir PDF'le yer almalı.

Kullanım: python3 scripts/kapilar/ders_pdf_kapisi.py [--sunucu http://localhost:3000] [--onek k2-] [--atla k2-07-genel-anestezik-ilaclar]
"""
import argparse, json, pathlib, sys, urllib.request

KOK = pathlib.Path(__file__).resolve().parents[2]
ap = argparse.ArgumentParser()
ap.add_argument('--sunucu', default='http://localhost:3000')
ap.add_argument('--onek', default='k2-')
# arşivde kalan, yayında olmayan eski sınama dersleri
ap.add_argument('--atla', nargs='*', default=['k2-07-genel-anestezik-ilaclar'])
a = ap.parse_args()

katalog = json.load(urllib.request.urlopen(f'{a.sunucu}/api/lecture-pdf/decks', timeout=30))['decks']
hata = 0
for f in sorted((KOK / 'data/sesli_anlatim/hizalama').glob(f'{a.onek}*.json')):
    if f.stem in a.atla:
        continue
    deck = json.loads(f.read_text()).get('deckId') or f'k2p-{f.stem}'
    dosyalar = katalog.get(deck) or []
    if not any(d.get('available') for d in dosyalar):
        hata += 1
        print(f'HATA {f.stem}: deckId {deck} sunucuda açılabilir PDF yok '
              f'(SANAL_DESTELER kaydı / dosya yolu / meds-web yeniden başlatma)')
print(f'{hata} HATA')
sys.exit(1 if hata else 0)
