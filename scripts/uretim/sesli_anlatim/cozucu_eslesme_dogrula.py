#!/usr/bin/env python3
"""Sesli ders ↔ soru çözücü / sesli asistan / önem listesi eşleşme kapısı.

Ön yüz eşleşmeyi yalnız `<branş>|<branş içi no>` ile kurar (CanliDersCozucuSoru.oneriBul, bitirdiklerimVeri
ilgiliCozulenler, sınav planı, konu eleme). Numara /api/canli-ders'ten gelir (src/services/canliDers.ts
bransBilgisi + BRANS_DUZELT). Bu betik her sesli dersin numarasıyla bulunan çözücü/asistan/önem dersinin başlığının
sesli ders başlığıyla örtüştüğünü doğrular (scripts/hat/oncelikli_dersler/analiz.py _baslik_sozcuk ile aynı yöntem).

Kullanım: python3 scripts/uretim/sesli_anlatim/cozucu_eslesme_dogrula.py [--url http://localhost:3000] [--json liste.json]
Çıkış: 0 HATA → 0, aksi 1.
"""
# Konum-bağımsız kök (2026-11-16): sabit parents[N] yerine scripts/kok.py (dosya taşınsa da doğru).
import sys as _sys
from pathlib import Path as _Path
_d = _Path(__file__).resolve().parent
while not (_d / "kok.py").exists() and _d != _d.parent:
    _d = _d.parent
if str(_d) not in _sys.path:
    _sys.path.append(str(_d))
import kok as _kok  # noqa: E402
import argparse
import json
import re
import sys
import unicodedata
import urllib.request
from pathlib import Path

KOK = _kok.MEDS
VERI = KOK / 'src' / 'data'
# canliDersKategori.ts CD_SPOT_BRANS ile aynı
BRANS = {
    'Tıbbi Patoloji': 'patoloji', 'Enfeksiyon Hastalıkları': 'enfeksiyon', 'Üroloji': 'uroloji',
    'Tıbbi Genetik': 'genetik', 'Halk Sağlığı': 'halksagligi', 'Kadın Hastalıkları ve Doğum': 'kadindogum',
    'Tıbbi Farmakoloji': 'farmakoloji',
}
TURLER = ('cozucu', 'asistan', 'onem')
# Başlıkta konu bildirmeyen sık sözcükler
BOS = {'hastaliklari', 'hastaliklar', 'giris', 'genel', 'temel', 'ozellikleri', 'kavramlari', 'patolojisi'}


def sozcukler(s: str) -> set[str]:
    s = unicodedata.normalize('NFC', s).replace('I', 'ı').replace('İ', 'i').lower()
    s = s.translate(str.maketrans('çğıöşüâîû', 'cgiosuaiu'))
    return {w for w in re.findall(r'\w{4,}', s)} - BOS


def ortusur(a: str, b: str) -> bool:
    A, B = sozcukler(a), sozcukler(b)
    if A & B:
        return True
    # kök örtüşmesi (meme/memenin, prostat/prostatik): ilk 5 harf
    return bool({w[:5] for w in A} & {w[:5] for w in B})


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--url', default='http://localhost:3000')
    ap.add_argument('--json', help='/api/canli-ders çıktısı dosyası (sunucu yerine)')
    a = ap.parse_args()
    if a.json:
        liste = json.loads(Path(a.json).read_text())['dersler']
    else:
        with urllib.request.urlopen(f'{a.url}/api/canli-ders?sinama=1', timeout=30) as r:
            liste = json.load(r)['dersler']

    dizin = {}
    for b in set(BRANS.values()):
        for t in TURLER:
            p = VERI / f'{b}_{t}' / 'index.json'
            if p.exists():
                dizin[(b, t)] = json.loads(p.read_text()).get('dersler', [])

    hata, uyari, tamam = [], [], 0
    goruldu: dict[tuple[str, int], str] = {}
    for d in liste:
        b = BRANS.get(d.get('brans') or '')
        if not b or '-son-prova-' in d['key'] or '-blok-ozet-' in d['key'] or '-sinav-kampi' in d['key']:
            continue
        try:
            no = int(d['no'])
        except (TypeError, ValueError):
            continue
        if (d.get('parca') or 1) == 1:
            if (b, no) in goruldu:
                hata.append(f"{d['key']}: {b}|{no} numarası {goruldu[(b, no)]} ile çakışıyor")
            goruldu[(b, no)] = d['key']
        for t in TURLER:
            L = dizin.get((b, t))
            if L is None:
                continue
            m = [x for x in L if int(x.get('no', -1)) == no]
            if not m:
                uyari.append(f"{d['key']} ({d['baslik']}): {b}_{t} içinde no {no} yok")
                continue
            if not ortusur(d['baslik'], m[0].get('baslik', '')):
                hata.append(f"{d['key']} «{d['baslik']}» → {b}_{t}/{m[0].get('kod')} «{m[0].get('baslik')}» (no {no}) başlık örtüşmüyor")
            else:
                tamam += 1
    for u in uyari:
        print('UYARI', u)
    for h in hata:
        print('HATA ', h)
    print(f'{tamam} eşleşme doğru, {len(uyari)} UYARI, {len(hata)} HATA')
    return 1 if hata else 0


if __name__ == '__main__':
    sys.exit(main())
