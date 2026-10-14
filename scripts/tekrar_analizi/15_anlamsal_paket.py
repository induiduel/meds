"""Sözcüksel benzerliği ≥ 0,60 olan (soru, özet penceresi) adaylarını anlamsal inceleme partilerine böler."""
import json
OZ = {o['id']: o for o in json.load(open('/home/indu/medsor/meds/src/data/lectureSummariesCatalog.json'))}
lines = {}
def satirlar(oid):
    if oid not in lines:
        L = [l.strip() for l in OZ[oid]['content'].split('\n')]
        lines[oid] = [l for l in L if len(l) > 3 and not l.startswith('<sub>')]
    return lines[oid]
items = []
for l in open('ozet_cevap/aday2.jsonl'):
    r = json.loads(l)
    ad = [a for a in r['adaylar'] if a['benzerlik'] >= 0.60][:2]
    if not ad: continue
    pas = []
    for a in ad:
        L = satirlar(a['ozet']); i = a['satir']
        baglam = '\n'.join(L[max(0, i - 1): i + 3])[:900]       # pencere + bir satır öncesi/sonrası
        pas.append({'ozet': a['ozet'], 'ozet_baslik': OZ[a['ozet']]['title'], 'satir': i, 'benzerlik': a['benzerlik'],
                    'konu_disi': a['konu_disi'], 'metin': baglam})
    items.append({'id': r['id'], 'kok': r['kok'], 'dogru_cevap': r['dogru'], 'olumsuz_kok': r['olumsuz'], 'pasajlar': pas})
N = 45
for k in range(0, len(items), N):
    json.dump({'parti': f'a{k // N + 1:03d}', 'sorular': items[k:k + N]}, open(f'ozet_cevap/parti/a{k // N + 1:03d}.json', 'w'), ensure_ascii=False, indent=1)
print(len(items), 'soru', (len(items) + N - 1) // N, 'parti')
