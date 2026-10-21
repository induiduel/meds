#!/usr/bin/env python3
"""Çıkmış şık açıklamalarını kopyalara yayar (çözücü = tek kaynak; önce sik_uygula.py).

- Son Prova (src/data/son_prova/k*/sorular/<brans>.json): çözücü sorusunun kopyası olan çıkmışlarda siklar/ipucu/cozum metni
  ve klip özetleri (çözücü kliplerini çalar) çözücüden alınır.
- Sesli sınav asistanı: aynı kök + aynı seçenek + aynı cevaplı çıkmışta yardim[H] (5 şık) ve yanlis[H] (yanlış şıklar) =
  çözücünün şık açıklaması; hem seslendirme girdisi (meds_temp/.../asistan/cikti) hem yayın (src/data/<brans>_asistan) metni.
  Eşleşmeyen çıkmışlar meds_temp/cikmis_paket/asistan/eslesmeyen.json'a yazılır (yazar + denetçi hattı, sonra
  asistan_uygula.py). Asistan sesleri sonra asistan_ses.py ile, yayın klip özetleri asistan_uygula.py --ozet ile.

Kullanım: python3 meds/scripts/cikmis_paket/kopya_esitle.py
"""
import glob, json, re
from pathlib import Path

MEDS = Path(__file__).resolve().parents[2]
T = MEDS.parent / 'meds_temp'
BRANSLAR = ['patoloji', 'enfeksiyon', 'genetik', 'uroloji', 'halksagligi', 'kadindogum', 'farmakoloji']
n = lambda t: re.sub(r'\W+', '', t.lower())


def tam_dir(b):
    return T / ('patoloji_ornek26/cozucu/cikti_tam' if b == 'patoloji' else f'spot_cozucu/{b}/cikti_tam')


def asistan_girdi(b):
    return T / ('patoloji_onem/asistan2/cikti' if b == 'patoloji' else f'spot_cozucu/{b}/asistan/cikti')


# ---- Son Prova
sp_say = 0
for f in sorted(glob.glob(str(MEDS / 'src/data/son_prova/k*/sorular/*.json'))):
    d = json.load(open(f)); degisti = False
    for k, q in d.items():
        b, r = k.split('/'); kod, no = r.split('#')
        p = MEDS / 'src/data' / f'{b}_cozucu' / f'{kod}.json'
        if q.get('tur') != 'cikmis' or not p.exists():
            continue
        c = json.loads(p.read_text())
        cq = next((x for x in c['sorular'] if x['no'] == int(no)), None)
        if not cq or n(cq['soru']) != n(q['soru']) or cq['dogru'] != q['dogru']:
            continue
        yeni = {'siklar': cq['siklar'], 'ipucu': cq['ipucu'], 'cozum': cq['cozum']}
        kl = dict(q.get('klip') or {})
        for ad, kk in [('i', f'i-{no}'), ('c', f'c-{no}'), ('d', f'd-{no}')] + [(f's{h}', f's-{no}-{h}') for h in 'ABCDE']:
            if kk in c['klip']:
                kl[ad] = c['klip'][kk]['v']
        if any(q.get(a) != v for a, v in yeni.items()) or kl != q.get('klip'):
            q.update(yeni); q['klip'] = kl; degisti = True; sp_say += 1
    if degisti:
        Path(f).write_text(json.dumps(d, ensure_ascii=False, indent=1 if open(f).read(2) == '{\n' else None))
print('Son Prova güncellenen soru:', sp_say)

# ---- Asistan
eslesmeyen, as_say = [], 0
for b in BRANSLAR:
    m = {}
    for f in glob.glob(str(tam_dir(b) / '*.json')):
        for q in json.load(open(f))['sorular']:
            if q.get('tur') == 'cikmis':
                m.setdefault(n(q['soru']), q)
    for f in sorted(glob.glob(str(MEDS / 'src/data' / f'{b}_asistan' / '*.json'))):
        if f.endswith('index.json'):
            continue
        yay = json.load(open(f))
        gp = asistan_girdi(b) / f"{yay['kod']}.json"
        gir = json.loads(gp.read_text())
        gs = {s['anahtar']: s for bo in gir['bolumler'] for nk in bo['noktalar'] for s in (nk.get('sorular') or [])}
        degisti = False
        for p in yay.get('noktalar', []):
            for s in p['sorular']:
                if s.get('tur') != 'cikmis':
                    continue
                q = m.get(n(s['kok']))
                if (not q or q['dogru'] != s['dogru']
                        or {h: n(v) for h, v in q['secenekler'].items()} != {h: n(v) for h, v in s['secenekler'].items()}):
                    eslesmeyen.append({'id': f"{b}/{yay['kod']}/{s['k']}", 'ders': yay['baslik'], 'nokta': p['baslik'],
                                       'nokta_cumleler': p.get('cumleler'), 'soru': s['kok'], 'secenekler': s['secenekler'],
                                       'dogru': s['dogru'], 'mevcut_yardim': s['yardim'], 'mevcut_yanlis': s['yanlis'],
                                       'dogruMetin': s.get('dogruMetin')})
                    continue
                g = gs[s['k']]
                g['yardim'] = {h: q['siklar'][h] for h in 'ABCDE'}
                g['yanlis'] = {h: q['siklar'][h] for h in g['yanlis']}
                s['yardim'] = {h: q['siklar'][h]['metin'] for h in 'ABCDE'}
                s['yanlis'] = {h: q['siklar'][h]['metin'] for h in s['yanlis']}
                degisti = True; as_say += 1
        if degisti:
            gp.write_text(json.dumps(gir, ensure_ascii=False, indent=1))
            Path(f).write_text(json.dumps(yay, ensure_ascii=False, separators=(',', ':')) if not open(f).read(2) == '{\n'
                               else json.dumps(yay, ensure_ascii=False, indent=1))
print('Asistan eşitlenen çıkmış:', as_say, '· eşleşmeyen:', len(eslesmeyen))
(T / 'cikmis_paket/asistan').mkdir(parents=True, exist_ok=True)
(T / 'cikmis_paket/asistan/eslesmeyen.json').write_text(json.dumps(eslesmeyen, ensure_ascii=False, indent=1))
