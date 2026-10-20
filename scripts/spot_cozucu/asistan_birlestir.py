"""Sesli sınav asistanı (branş geneli): plan + cikti (asistan_dogrula.py 0 HATA) + EMA kayıtları → meds/src/data/<brans>_asistan/{index,<kod>}.json.
Klipler /api/patoloji-asistan/ses/<kod>/<klip>.mp3 (sunucu kodun önekinden branş klasörünü bulur: e → enfeksiyon, u → uroloji).
Kullanım: python3 meds/scripts/spot_cozucu/asistan_birlestir.py <brans>
"""
import json, os, subprocess, sys
brans = sys.argv[1]
A = f'/home/indu/medsor/meds_temp/spot_cozucu/{brans}/asistan'
SES = f'/home/indu/medsor/meds/data/{brans}_asistan/ses'
OUT = f'/home/indu/medsor/meds/src/data/{brans}_asistan'
ONEM = f'/home/indu/medsor/meds/src/data/{brans}_onem/index.json'
sira = {d['kod']: i for i, d in enumerate(json.load(open(ONEM))['dersler'])}
os.makedirs(OUT, exist_ok=True)
dersler, hatali = [], []
# Kurul 2+ ders zinciri: yalnız bağımsız denetimi geçmiş kodlar (onayli.json yoksa davranış değişmez)
_onayli_p = f'/home/indu/medsor/meds_temp/spot_cozucu/{brans}/onayli.json'
ONAYLI = set(json.load(open(_onayli_p))) if os.path.exists(_onayli_p) else None
for f in sorted(os.listdir(f'{A}/cikti'), key=lambda x: sira.get(x[:-5], 999)):
    if not f.endswith('.json'): continue
    kod = f[:-5]
    if ONAYLI is not None and kod not in ONAYLI: continue
    r = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'asistan_dogrula.py'), f'{A}/cikti/{f}'], capture_output=True, text=True)
    if r.returncode:
        hatali.append(kod); continue
    o = json.load(open(f'{A}/cikti/{f}')); p = json.load(open(f'{A}/plan/{kod}.json'))
    PN = {n['id']: n for n in p['noktalar']}
    PS = {s['anahtar']: s for n in p['noktalar'] for s in n['sorular']}
    kp = f'{SES}/{kod}/kayit.json'
    kay = json.load(open(kp)) if os.path.exists(kp) else {}
    bolumler, noktalar, gerek = [], [], ['giris', 'kapanis']
    for bi, b in enumerate(o['bolumler'], 1):
        bolumler.append({'baslik': b['baslik'], 'neden': b['neden']['metin']}); gerek.append(f'b-{bi}')
        for n in b['noktalar']:
            pn = PN[n['id']]; gerek.append(f'a-{n["id"]}')
            sorular = []
            for s in n.get('sorular') or []:
                ps = PS[s['anahtar']]; k = s['anahtar']
                gerek += [f'q-{k}', f'd-{k}', f'h-{k}'] + [f'y-{k}-{h}' for h in s['yanlis']]
                sorular.append({'k': k, 'tur': ps['tur'], **({'sinav': ps['sinav']} if ps.get('sinav') else {}), 'kok': ps['kok'],
                                'secenekler': ps['secenekler'], 'dogru': ps['dogru'], 'dogruMetin': s['dogru']['metin'],
                                'yanlis': {h: v['metin'] for h, v in s['yanlis'].items()},
                                'yardim': {h: v['metin'] for h, v in sorted(s['yardim'].items())}})
            noktalar.append({'id': n['id'], 'bolum': bi - 1, 'puan': pn['puan'], 'aday': pn['aday'], 'kategori': pn['kategori'],
                             'baslik': n['baslik'], 'bilgi': pn['bilgi'], 'cumleler': [c['metin'] for c in n['cumleler']], 'sorular': sorular})
    klip = {k: {'v': v['h'], 'sure': v['sure'], 'zaman': v['zaman']} for k, v in kay.items() if k in set(gerek)}
    d = {'kod': kod, 'no': p['no'], 'baslik': p['baslik'], 
         'giris': [c['metin'] for c in o['giris']], 'kapanis': [c['metin'] for c in o['kapanis']],
         'bolumler': bolumler, 'noktalar': noktalar, 'klip': klip}
    json.dump(d, open(f'{OUT}/{kod}.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    sorular = [s for n in noktalar for s in n['sorular']]
    dersler.append({'kod': kod, 'no': p['no'], 'baslik': p['baslik'], 'bolum': len(bolumler), 'adim': len(noktalar), 'soru': len(sorular),
                    'cikmis': sum(1 for s in sorular if s['tur'] == 'cikmis'), 'ses': all(g in klip for g in gerek),
                    'sure': round(sum(v['sure'] for k, v in klip.items() if k[:2] in ('a-', 'b-') or k in ('giris', 'kapanis')))})
for f in os.listdir(OUT):
    if f != 'index.json' and f[:-5] not in {d['kod'] for d in dersler}: os.remove(f'{OUT}/{f}')
json.dump({'surum': f'{brans}-asistan-v1', 'brans': brans, 'ses': 'EMA Lightning', 'dersler': dersler}, open(f'{OUT}/index.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(dersler), 'ders ·', sum(d['adim'] for d in dersler), 'nokta ·', sum(d['soru'] for d in dersler), 'soru · sesli', sum(d['ses'] for d in dersler), '· hatalı', hatali)
