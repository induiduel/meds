#!/usr/bin/env python3
"""Sesli sınav asistanı çıkmış şık açıklamalarını uygular ve seslendirir.

1. meds_temp/cikmis_paket/asistan/cikti*.json (yazar + denetçi, sik_dogrula.py 0 HATA; `sorun` olanlar atlanır):
   yardim[H] (5 şık) ve yanlis[H] (yanlış şıklar) hem seslendirme girdisine (asistan/cikti/<kod>.json) hem yayına yazılır.
2. Değişen derslerde asistan_ses.py klasor() ile yalnız metni değişen klipler (y-*, h-*) EMA ile üretilir.
3. Yayın dosyalarının (src/data/<brans>_asistan/<kod>.json) klip özetleri kayit.json'dan güncellenir.
   (asistan_birlestir.py K1 derslerini K2 kapısıyla reddedip sildiği için kullanılmaz.)
Önce kopya_esitle.py çalışmış olmalı (eşleşen çıkmışlar). Kullanım: bash meds/scripts/cikmis_paket/asistan_uygula.sh
"""
import glob, json, sys
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
T = MEDS.parent / 'meds_temp'
sys.path.insert(0, str(MEDS / 'scripts/spot_cozucu'))
import ses as SC  # noqa: E402
import asistan_ses as AS  # noqa: E402


def girdi_dir(b):
    return T / ('patoloji_onem/asistan2/cikti' if b == 'patoloji' else f'spot_cozucu/{b}/asistan/cikti')


cikti = {}
for f in sorted(glob.glob(str(T / 'cikmis_paket/asistan/cikti*.json'))):
    cikti.update({k: v for k, v in json.load(open(f)).items() if not v.get('sorun')})
dersler = {}
for k, v in cikti.items():
    b, kod, s = k.split('/')
    dersler.setdefault((b, kod), {})[s] = v['siklar']
# kopya_esitle.py'nin değiştirdiği dersler de seslendirilir (hepsi; değişmeyen klip yeniden üretilmez)
for b in ['patoloji', 'enfeksiyon', 'genetik', 'uroloji', 'halksagligi', 'kadindogum', 'farmakoloji']:
    for f in glob.glob(str(girdi_dir(b) / '*.json')):
        dersler.setdefault((b, Path(f).stem), {})
print(len(cikti), 'yazılmış soru,', len(dersler), 'ders')

S = SC.Ema()
for (b, kod), sorular in sorted(dersler.items()):
    yp = MEDS / 'src/data' / f'{b}_asistan' / f'{kod}.json'
    gp = girdi_dir(b) / f'{kod}.json'
    if not yp.exists() or not gp.exists():
        continue
    yay, gir = json.loads(yp.read_text()), json.loads(gp.read_text())
    gs = {s['anahtar']: s for bo in gir['bolumler'] for nk in bo['noktalar'] for s in (nk.get('sorular') or [])}
    ys = {s['k']: s for p in yay.get('noktalar', []) for s in p['sorular']}
    for a, sk in sorular.items():
        g, y = gs[a], ys[a]
        g['yardim'] = {h: sk[h] for h in 'ABCDE'}
        g['yanlis'] = {h: sk[h] for h in g['yanlis']}
        y['yardim'] = {h: sk[h]['metin'] for h in 'ABCDE'}
        y['yanlis'] = {h: sk[h]['metin'] for h in y['yanlis']}
    if sorular:
        gp.write_text(json.dumps(gir, ensure_ascii=False, indent=1))
    kok = MEDS / 'data' / f'{b}_asistan' / 'ses'
    SC.klasor(S, kok, kod, AS.klipler(gir, S), 48)
    kay = json.loads((kok / kod / 'kayit.json').read_text())
    for ad in list(yay.get('klip', {})):
        if ad in kay:
            yay['klip'][ad] = {**yay['klip'][ad], 'v': kay[ad]['h'], 'sure': kay[ad]['sure'], 'zaman': kay[ad]['zaman']}
    tek = yp.read_text()[:2] != '{\n'
    yp.write_text(json.dumps(yay, ensure_ascii=False, separators=(',', ':')) if tek else json.dumps(yay, ensure_ascii=False, indent=1))
print('bitti')
