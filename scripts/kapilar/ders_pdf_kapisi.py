#!/usr/bin/env python3
"""Sesli ders PDF kapısı (H-PDF, 2026-11-06).

Belirti: yeni Kurul 2 derslerinde (Polinöropati, Bazal Ganglionlar) görüntüleyici PDF'i açamayıp "Drive'da aç" yedeğine düşüyordu.
Kök neden: (1) destesiz yeni dersin `deckId`'si `lecturePdfLocator.ts::SANAL_DESTELER`'e eklenmemişti; (2) eklenen kayıt
`meds-web` yeniden başlatılmadan sunucuda görünmüyordu (tsx watch yok, AGENTS 12).
Kapı: her hizalama dosyasının deckId'si sunucunun /api/lecture-pdf/decks kataloğunda en az bir açılabilir PDF'le yer almalı.

Kullanım: python3 scripts/kapilar/ders_pdf_kapisi.py [--sunucu http://localhost:3000] [--onek k2-] [--atla k2-07-genel-anestezik-ilaclar]
"""
import argparse, json, pathlib, sys, urllib.request

import sys as _sys
from pathlib import Path as _Path
_d = _Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in _sys.path:
    _sys.path.append(str(_d))
import kok as _kok  # noqa: E402
KOK = _kok.MEDS
ap = argparse.ArgumentParser()
ap.add_argument('--sunucu', default='http://localhost:3000')
# --statik (H624): sunucu gerekmez — deckId SANAL_DESTELER/deckPdfSources'ta kayıtlı ve PDF drive_root'ta olmalı.
# dagit.sh bunu dağıtımdan ÖNCE zorunlu çalıştırır (kayıtsız ders canlıya çıkamaz).
ap.add_argument('--statik', action='store_true')
ap.add_argument('--kok', default=None, help='meds kökü (dagit.sh worktree)')
ap.add_argument('--onek', default='k2-')
# arşivde kalan, yayında olmayan eski sınama dersleri
ap.add_argument('--atla', nargs='*', default=['k2-07-genel-anestezik-ilaclar'])
a = ap.parse_args()

if a.kok:
    KOK = pathlib.Path(a.kok)

def statik_katalog():
    import re, unicodedata
    ts = (KOK / 'src/services/lecturePdfLocator.ts').read_text()
    blok = ts[ts.index('export const SANAL_DESTELER'):]
    blok = blok[:blok.index('\n};')]
    drive = KOK.parent / 'meds_downloads/drive_root'
    nfc = lambda x: unicodedata.normalize('NFC', x)
    var = {nfc(str(p.relative_to(drive))) for p in drive.rglob('*.pdf')} if drive.exists() else None
    kat = {}
    for m in re.finditer(r"\n  '([^']+)': \{(.*?)\n  \},", blok, re.S):
        yollar = re.findall(r"path: '([^']+)'", m.group(2))
        kat[m.group(1)] = [{'available': var is None or nfc(y) in var} for y in yollar] or [{'available': True}]
    js = json.loads((KOK / 'src/data/deckPdfSources.json').read_text()).get('decks', {})
    for k, v in js.items():
        kat.setdefault(k, [{'available': True}] if v.get('files') else [])
    return kat

katalog = statik_katalog() if a.statik else json.load(urllib.request.urlopen(f'{a.sunucu}/api/lecture-pdf/decks', timeout=30))['decks']
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
