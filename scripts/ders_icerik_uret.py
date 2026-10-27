#!/usr/bin/env python3
# İçerik biçimi: docs/DERS_ICERIK_BICIMI.md (yeni v15 ekranının okunaklı gösterebileceği yapıda üret).
"""Ders içerik paketi: taslak (meds_temp/ogrenci_ders/<kod>/taslak) + önem listesi → src/data/ders_icerik/<key>.json.
Kullanım: ders_icerik_uret.py k2-05 k2-05-norolojik-muayene 2n03 k2noroloji_onem"""
import json, sys, os
kod, key, onem_kod, onem_dir = sys.argv[1:5]
R = os.path.join(os.path.dirname(__file__), '..')
T = os.path.join(R, '..', 'meds_temp', 'ogrenci_ders', kod, 'taslak')
J = lambda p: json.load(open(p, encoding='utf-8'))
deck = J(f'{T}/deck.json'); soz = J(f'{T}/sozluk.json')['yeni']; hast = J(f'{T}/hastaliklar.json')
out = {'key': key, 'baslik': deck.get('title'), 'ozet': deck.get('overview', '')}
out['terimler'] = [{'t': x['term'], 'a': x['definition'], 'i': x.get('pearl', ''), 'e': x.get('aliases', []), 's': (x.get('kanit') or {}).get('sayfa')} for x in soz]
ke = os.path.join(R, 'data/sesli_anlatim/kisaltma_elle', key + '.json')
out['kisaltmalar'] = []
if os.path.exists(ke):
    k = J(ke); k = k.get('kisaltmalar', k) if isinstance(k, dict) else k
    out['kisaltmalar'] = [{'k': a, 'acilim': b} for a, b in (k.items() if isinstance(k, dict) else [])]
AL = [('etiology', 'Etiyoloji'), ('physiology_pathophysiology', 'Fizyopatoloji'), ('morphology_pathology', 'Morfoloji'), ('symptoms_clinical', 'Klinik bulgular'),
      ('pathognomonic_features', 'Ayırt edici bulgu'), ('diagnostic_methods', 'Tanı'), ('imaging_findings', 'Görüntüleme'), ('treatment', 'Tedavi')]
out['hastaliklar'] = []
for h in hast:
    bol = [{'b': ad, 'm': h[f]} for f, ad in AL if h.get(f)]
    sy = sorted({x['sayfa'] for x in h.get('kanitlar', []) if x.get('sayfa')})
    out['hastaliklar'].append({'id': h['id'], 'ad': h['name'], 'latin': h.get('latinName', ''), 'kat': h.get('category', ''), 'bolumler': bol, 's': sy})
sp = []
for l in open(f'{T}/bilgi_havuzu.jsonl', encoding='utf-8'):
    r = json.loads(l)
    if r.get('tur') == 'spot': sp.append({'b': r.get('varlik', ''), 'm': r['bilgi'], 's': (r.get('kanit') or {}).get('sayfa')})
out['bilgiler'] = sp
try:
    on = J(os.path.join(R, 'src/data', onem_dir, onem_kod + '.json'))
    out['onemli'] = [{'p': m['puan'], 'b': m['baslik'], 'm': m['bilgi'], 'alt': m.get('alt', []), 'n': m.get('neden', ''), 's': [a['sayfa'] for a in m.get('alinti', [])]} for m in on['maddeler']]
except Exception as e: out['onemli'] = []
out['spotlar'] = [{'m': p, 'n': s['slideNumber'], 'bolum': s.get('bolum', '')} for s in deck['slides'] for p in s.get('spotPearls', [])]
tab = []; kart = []
for s in deck['slides']:
    for it in s.get('interactiveElements', []):
        if it['type'] == 'interactive_table':
            tab.append({'t': it['tableTitle'], 'h': it['tableHeaders'], 'r': [[c['text'] for c in row['cells']] for row in it['tableRows']], 'n': s['slideNumber']})
        elif it['type'] == 'venn_grid':
            ad = {'A': it['labelA'], 'B': it['labelB'], 'both': 'İkisi de', 'neither': 'İkisi de değil'}
            tab.append({'t': it['title'], 'h': ['Ölçüt', 'Hangisine ait', 'Gerekçe'], 'r': [[i['criterion'], ad.get(i['correct'], i['correct']), i.get('explanation', '')] for i in it['items']], 'n': s['slideNumber'], 'k': 'karsilastirma'})
    for f in s.get('flashcards', []): kart.append({'o': f['front'], 'a': f['back'], 'c': f.get('category', ''), 'n': s['slideNumber']})
out['tablolar'] = tab; out['kartlar'] = kart
p = os.path.join(R, 'src/data/ders_icerik', key + '.json')
json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(p, {k: len(v) for k, v in out.items() if isinstance(v, list)})
