#!/usr/bin/env python3
"""Sesli soru çözücü: örnek sorular (cikti/, cozucu_dogrula.py) + benzer/çıkmış sorular (cikti2/, cozucu_dogrula2.py) + EMA kayıtları
→ meds_temp/.../cozucu/cikti_tam/<kod>.json (seslendirme girdisi) ve meds/src/data/patoloji_cozucu/{index,<kod>}.json (ön yüz).

Numaralar kalıcıdır (ilerleme ve klip adları buna bağlı): örnek 1..n (kaynak no), benzer n+1..2n, çıkmış 2n+1.. (cikti2 sırasıyla), canlı ders örnekleri
sonra (cikti3/, cozucu_dogrula3.py; ekranda 'Örnek soru · zorluk').
Ekranda sıra: ders akışı (ilk PDF sayfası), eşitlikte örnek → benzer → çıkmış. Hatalı ders atlanır ve raporlanır.
Kullanım: python3 meds/scripts/patoloji_cozucu/cozucu_birlestir.py
"""
import json, os, subprocess, sys
B = os.path.dirname(os.path.abspath(__file__))
A = '/home/indu/medsor/meds_temp/patoloji_ornek26/cozucu'
SES = '/home/indu/medsor/meds/data/patoloji_cozucu/ses'
OUT = '/home/indu/medsor/meds/src/data/patoloji_cozucu'
ONEM = json.load(open('/home/indu/medsor/meds/src/data/patoloji_onem/index.json'))['dersler']
TUR_SIRA = {'ornek': 0, 'benzer': 1, 'cikmis': 2}
os.makedirs(OUT, exist_ok=True); os.makedirs(f'{A}/cikti_tam', exist_ok=True)


def kayit(ad):
    p = f'{SES}/{ad}/kayit.json'
    return json.load(open(p)) if os.path.exists(p) else {}


def gecer(betik, f):
    return subprocess.run([sys.executable, f'{B}/{betik}', f], capture_output=True, text=True).returncode == 0


dersler, hatali = [], []
for od in ONEM:
    kod = od['kod']; f = f'{A}/cikti/{kod}.json'; f2 = f'{A}/cikti2/{kod}.json'
    if not os.path.exists(f): continue
    if not gecer('cozucu_dogrula.py', f) or (os.path.exists(f2) and not gecer('cozucu_dogrula2.py', f2)):
        hatali.append(kod); continue
    tam = [dict(q, tur='ornek') for q in json.load(open(f))['sorular']]
    n = len(tam)
    if os.path.exists(f2):
        o2 = json.load(open(f2))
        tam += [dict(q, no=n + i, tur='benzer') for i, q in enumerate(o2.get('yeni') or [], 1)]
        m = len(tam)
        tam += [dict(q, no=m + i, tur='cikmis') for i, q in enumerate(o2.get('cikmis') or [], 1)]
    f3 = f'{A}/cikti3/{kod}.json'  # 3. tur: canlı ders konularından örnek sorular (numaralar çıkmışlardan sonra)
    if os.path.exists(f3):
        if not gecer('cozucu_dogrula3.py', f3): hatali.append(kod); continue
        m = len(tam)
        tam += [dict(q, no=m + i, tur='ornek') for i, q in enumerate(json.load(open(f3)).get('yeni') or [], 1)]
    json.dump({'kod': kod, 'sorular': tam}, open(f'{A}/cikti_tam/{kod}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    kay = kayit(kod)
    sorular, gerek = [], []
    for q in sorted(tam, key=lambda q: (min(q['sayfa']), TUR_SIRA[q['tur']], q['no'])):
        no = q['no']
        gerek += [f'q-{no}', f'i-{no}', f'c-{no}', f'd-{no}'] + [f's-{no}-{h}' for h in 'ABCDE']
        sorular.append({'no': no, 'tur': q['tur'], **({'sinav': q['sinav']} if q.get('sinav') else {}),
                        **({'zorluk': q['zorluk']} if q.get('zorluk') else {}),
                        'soru': q['soru'], 'secenekler': q['secenekler'], 'dogru': q['dogru'],
                        'ipucu': q['ipucu']['metin'], 'siklar': {h: q['siklar'][h]['metin'] for h in 'ABCDE'},
                        'cozum': q['cozum']['metin'], 'sayfa': q['sayfa']})
    klip = {k: {'v': kay[k]['h'], 'sure': kay[k]['sure'], 'zaman': kay[k]['zaman']} for k in gerek if k in kay}
    d = {'kod': kod, 'no': od['no'], 'baslik': od['baslik'], 'sorular': sorular, 'klip': klip}
    json.dump(d, open(f'{OUT}/{kod}.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    say = {t: sum(q['tur'] == t for q in sorular) for t in TUR_SIRA}
    dersler.append({'kod': kod, 'no': od['no'], 'baslik': od['baslik'], 'soru': len(sorular), **say, 'ses': len(klip) == len(gerek)})
for f in os.listdir(OUT):
    if f != 'index.json' and f[:-5] not in {d['kod'] for d in dersler}: os.remove(f'{OUT}/{f}')
ok = kayit('ortak')
json.dump({'surum': 'patoloji-cozucu-v2', 'ses': 'EMA Lightning', 'ortak': {k: {'v': v['h'], 'sure': v['sure']} for k, v in ok.items()},
           'dersler': dersler}, open(f'{OUT}/index.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(dersler), 'ders ·', sum(d['soru'] for d in dersler), 'soru (örnek', sum(d['ornek'] for d in dersler), '· benzer',
      sum(d['benzer'] for d in dersler), '· çıkmış', sum(d['cikmis'] for d in dersler), ') · sesli', sum(d['ses'] for d in dersler), '· hatalı', hatali)
