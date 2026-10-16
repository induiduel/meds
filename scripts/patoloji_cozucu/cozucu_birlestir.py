#!/usr/bin/env python3
"""Sesli soru çözücü: cikti (cozucu_dogrula.py 0 HATA) + EMA kayıtları → meds/src/data/patoloji_cozucu/{index,<kod>}.json.

Ön yüz yalnız `metin` biçimini gösterir; klipler /api/patoloji-cozucu/ses/<kod>/<klip>.mp3?v=<h> (cozucu_ses.py).
Ders sırası ve başlıkları önem listesinden (src/data/patoloji_onem/index.json). Hatalı ders atlanır ve raporlanır.
Kullanım: python3 meds/scripts/patoloji_cozucu/cozucu_birlestir.py
"""
import json, os, subprocess, sys
B = os.path.dirname(os.path.abspath(__file__))
A = '/home/indu/medsor/meds_temp/patoloji_ornek26/cozucu'
SES = '/home/indu/medsor/meds/data/patoloji_cozucu/ses'
OUT = '/home/indu/medsor/meds/src/data/patoloji_cozucu'
ONEM = json.load(open('/home/indu/medsor/meds/src/data/patoloji_onem/index.json'))['dersler']
os.makedirs(OUT, exist_ok=True)


def kayit(ad):
    p = f'{SES}/{ad}/kayit.json'
    return json.load(open(p)) if os.path.exists(p) else {}


dersler, hatali = [], []
for od in ONEM:
    kod = od['kod']; f = f'{A}/cikti/{kod}.json'
    if not os.path.exists(f): continue
    r = subprocess.run([sys.executable, f'{B}/cozucu_dogrula.py', f], capture_output=True, text=True)
    if r.returncode:
        hatali.append(kod); continue
    o = json.load(open(f)); kay = kayit(kod)
    sorular, gerek = [], []
    for q in o['sorular']:
        n = q['no']
        gerek += [f'q-{n}', f'i-{n}', f'c-{n}', f'd-{n}'] + [f's-{n}-{h}' for h in 'ABCDE']
        sorular.append({'no': n, 'soru': q['soru'], 'secenekler': q['secenekler'], 'dogru': q['dogru'],
                        'ipucu': q['ipucu']['metin'], 'siklar': {h: q['siklar'][h]['metin'] for h in 'ABCDE'},
                        'cozum': q['cozum']['metin'], 'sayfa': q['sayfa']})
    klip = {k: {'v': kay[k]['h'], 'sure': kay[k]['sure'], 'zaman': kay[k]['zaman']} for k in gerek if k in kay}
    d = {'kod': kod, 'no': od['no'], 'baslik': od['baslik'], 'sorular': sorular, 'klip': klip}
    json.dump(d, open(f'{OUT}/{kod}.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    dersler.append({'kod': kod, 'no': od['no'], 'baslik': od['baslik'], 'soru': len(sorular), 'ses': len(klip) == len(gerek)})
for f in os.listdir(OUT):
    if f != 'index.json' and f[:-5] not in {d['kod'] for d in dersler}: os.remove(f'{OUT}/{f}')
ok = kayit('ortak')
json.dump({'surum': 'patoloji-cozucu-v1', 'ses': 'EMA Lightning', 'ortak': {k: {'v': v['h'], 'sure': v['sure']} for k, v in ok.items()},
           'dersler': dersler}, open(f'{OUT}/index.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(dersler), 'ders ·', sum(d['soru'] for d in dersler), 'soru · sesli', sum(d['ses'] for d in dersler), '· hatalı', hatali)
