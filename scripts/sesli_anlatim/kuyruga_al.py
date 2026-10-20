#!/usr/bin/env python3
"""Hazır ve denetimden geçmiş konuşma metinlerini yayına alır ve seslendirme kuyruğuna sırayla ekler.

- meds_temp/sesli_anlatim/metinler/<key>.md → (metin_denetle 0 HATA ise) data/sesli_anlatim/metin/<key>.md
- data/sesli_anlatim/dersler.json liste.json'dan yazılır.
- Sıra korunur: her ses grubunda (emel, aoede) metni henüz hazır olmayan ilk dersten sonrası kuyruğa alınmaz.
- Kuyruğa ekleme sunucunun /api/sesli-anlatim/uret ucuyla (varsayılan http://127.0.0.1:3000).

Kullanım: kuyruga_al.py [--izle SANİYE] [--sunucu URL] [--kuru]
"""
import argparse, json, shutil, subprocess, sys, time, urllib.request
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
ROOT = MEDS.parent
TEMP = ROOT / 'meds_temp' / 'sesli_anlatim'
DATA = MEDS / 'data' / 'sesli_anlatim'
DENETLE = MEDS / 'scripts' / 'sesli_anlatim' / 'metin_denetle.py'
SAG = {'emel': ('edge-emel', 'Emel')}  # varsayılan ses her derste Emel
ALTERNATIF = ('gemini-ucretsiz', 'Aoede')  # kullanıcı isteği: ücretsiz anahtarlarla sırayla Aoede alternatifi (ücretli asla)


def _panel_secret():
    """Oracle'a (--sunucu) giderken yönetici doğrulaması: MEDS_PANEL_SECRET (ortam ya da meds/.env). Yazdırılmaz."""
    import os
    if os.environ.get('MEDS_PANEL_SECRET'):
        return os.environ['MEDS_PANEL_SECRET'].strip()
    env = MEDS / '.env'
    for satir in env.read_text(encoding='utf-8').splitlines() if env.exists() else []:
        if satir.startswith('MEDS_PANEL_SECRET='):
            return satir.split('=', 1)[1].strip().strip('"')
    return ''


def istek(url, veri=None):
    h = {'Content-Type': 'application/json', 'x-admin-email': 'nofrostlife@gmail.com'}
    if _panel_secret():
        h['x-panel-secret'] = _panel_secret()
    req = urllib.request.Request(url, data=json.dumps(veri).encode() if veri is not None else None,
                                 headers=h,
                                 method='POST' if veri is not None else 'GET')
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def tur(args):
    liste = json.load(open(TEMP / 'liste.json'))
    DATA.joinpath('metin').mkdir(parents=True, exist_ok=True)
    dersler = [{'key': x['key'], 'no': x['no'], 'baslik': x['baslik'], 'sira': x['sira'], 'ses': x['ses']} for x in liste]
    hedef = DATA / 'dersler.json'
    # listede olmayan dersleri koru: ders işçisi yayını (/api/sesli-anlatim/ders-ekle) yeni dersleri buraya ekler (2026-10-16)
    if hedef.exists():
        anahtarlar = {x['key'] for x in dersler}
        dersler += [x for x in json.load(open(hedef)) if x.get('key') not in anahtarlar]
    if not hedef.exists() or json.load(open(hedef)) != dersler:
        if not args.kuru:
            json.dump(dersler, open(hedef, 'w'), ensure_ascii=False, indent=1)
    try:
        durum = istek(f'{args.sunucu}/api/sesli-anlatim')
    except Exception as e:
        print('sunucuya ulaşılamadı:', e)
        return
    by = {d['key']: d for d in durum['dersler']}
    durdu = set()
    eklenen = 0
    for x in liste:
        grup = x['ses']
        if grup in durdu:
            continue
        kaynak = TEMP / 'metinler' / f"{x['key']}.md"
        yayin = DATA / 'metin' / f"{x['key']}.md"
        # .ok işareti: metni yazan ajan başarıyla bitti (yarım/kesik metin yayına alınmaz)
        if not kaynak.exists() or not kaynak.with_suffix('.md.ok').exists():
            durdu.add(grup)
            continue
        if subprocess.run([sys.executable, str(DENETLE), str(kaynak)], capture_output=True).returncode != 0:
            print('denetim geçmedi, sıra burada bekliyor:', x['key'])
            durdu.add(grup)
            continue
        if not yayin.exists() or yayin.read_text() != kaynak.read_text():
            if not args.kuru:
                shutil.copyfile(kaynak, yayin)
            print('metin yayına alındı:', x['key'])
        d = by.get(x['key']) or {}
        # önce varsayılan Emel, ardından ücretsiz Aoede alternatifi (her biri bir kez)
        for sag, ses in (SAG[grup], ALTERNATIF):
            var = any(v['saglayici'] == sag and v['ses'] == ses for v in d.get('varyantlar') or [])
            sirada = any(j['saglayici'] == sag and j['ses'] == ses for j in d.get('isler') or [])
            if var or sirada:
                continue
            if args.kuru:
                print('kuyruğa alınacak:', x['key'], sag, ses)
                continue
            r = istek(f'{args.sunucu}/api/sesli-anlatim/uret', {'key': x['key'], 'saglayici': sag, 'ses': ses})
            print('kuyruğa alındı:', x['sira'], x['key'], sag, ses, r.get('is', {}).get('id'))
            eklenen += 1
    return eklenen


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--izle', type=int, default=0)
    ap.add_argument('--sunucu', default='http://127.0.0.1:3000')
    ap.add_argument('--kuru', action='store_true')
    a = ap.parse_args()
    while True:
        tur(a)
        if not a.izle:
            break
        time.sleep(a.izle)
