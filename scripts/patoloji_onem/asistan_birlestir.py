"""Sesli sınav asistanı: plan + cikti (dogrula 0 HATA) + EMA kayıtları → meds/src/data/patoloji_asistan/{index,<kod>}.json.

Ön yüz yalnız `metin` biçimini gösterir; ses klip adresleri /api/patoloji-asistan/ses/<kod>/<klip>.mp3?v=<h>.
Kullanım: python3 meds/scripts/patoloji_onem/asistan_birlestir.py  (ses üretilmemiş derste klip zamanları boş kalır; ekran
metinle ve okuma süresiyle ilerler).
"""
import json, os, re, subprocess, sys
A = '/home/indu/medsor/meds_temp/patoloji_onem/asistan'
SES = '/home/indu/medsor/meds/data/patoloji_asistan/ses'
OUT = '/home/indu/medsor/meds/src/data/patoloji_asistan'
ONEM = '/home/indu/medsor/meds/src/data/patoloji_onem/index.json'
sira = {d['kod']: i for i, d in enumerate(json.load(open(ONEM))['dersler'])}
os.makedirs(OUT, exist_ok=True)
dersler, hatali = [], []
for f in sorted(os.listdir(f'{A}/cikti'), key=lambda x: sira.get(x[:-5], 999)):
    kod = f[:-5]
    r = subprocess.run([sys.executable, f'{A}/dogrula.py', f'{A}/cikti/{f}'], capture_output=True, text=True)
    if r.returncode:
        hatali.append(kod); continue
    o = json.load(open(f'{A}/cikti/{f}')); p = json.load(open(f'{A}/plan/{kod}.json'))
    kp = f'{SES}/{kod}/kayit.json'
    kay = json.load(open(kp)) if os.path.exists(kp) else {}
    klip = {k: {'v': v['h'], 'sure': v['sure'], 'zaman': v['zaman']} for k, v in kay.items()}
    adimlar = []
    for a, pa in zip(o['adimlar'], p['adimlar']):
        x = {'id': a['id'], 'puan': pa['puan'], 'aday': pa['aday'], 'kategori': pa['kategori'], 'baslik': a['baslik'],
             'bilgi': pa['bilgi'], 'cumleler': [c['metin'] for c in a['cumleler']]}
        if pa.get('soru'):
            s, ps = a['soru'], pa['soru']
            x['soru'] = {'tur': ps['tur'], **({'sinav': ps['sinav']} if ps.get('sinav') else {}), 'kok': ps['kok'], 'secenekler': ps['secenekler'],
                         'dogru': ps['dogru'], 'dogruMetin': s['dogru']['metin'], 'yanlis': {k: v['metin'] for k, v in s['yanlis'].items()}}
        adimlar.append(x)
    gerek = ['giris', 'kapanis'] + [f'a-{a["id"]}' for a in adimlar] + [f'{t}-{a["id"]}' for a in adimlar if a.get('soru') for t in 'qd'] + \
            [f'y-{a["id"]}-{h}' for a in adimlar if a.get('soru') for h in a['soru']['yanlis']]
    ses_hazir = all(g in klip for g in gerek)
    d = {'kod': kod, 'no': p['no'], 'baslik': p['baslik'], 'soruSayisi': p.get('soruSayisi', 1),
         'giris': [c['metin'] for c in o['giris']], 'kapanis': [c['metin'] for c in o['kapanis']], 'adimlar': adimlar,
         'klip': {k: v for k, v in klip.items() if k in gerek}}
    json.dump(d, open(f'{OUT}/{kod}.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    dersler.append({'kod': kod, 'no': p['no'], 'baslik': p['baslik'], 'adim': len(adimlar), 'soru': sum(1 for a in adimlar if a.get('soru')),
                    'ses': ses_hazir, 'sure': round(sum(v['sure'] for k, v in klip.items() if k in ('giris', 'kapanis') or k.startswith('a-')))})
for f in os.listdir(OUT):
    if f != 'index.json' and f[:-5] not in {d['kod'] for d in dersler}: os.remove(f'{OUT}/{f}')
json.dump({'surum': 'patoloji-asistan-v1', 'ses': 'EMA Lightning', 'dersler': dersler}, open(f'{OUT}/index.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(dersler), 'ders ·', sum(d['adim'] for d in dersler), 'adım ·', sum(d['soru'] for d in dersler), 'soru · sesli', sum(d['ses'] for d in dersler), '· hatalı', hatali)
