"""İnceleme partileri: sınırda çiftler + otomatik 'aynı' örneklemi → inceleme/parti/pNNN.json"""
import json, random, collections
R = {json.loads(l)['id']: json.loads(l) for l in open('sorular_ozet.jsonl')}
U = json.load(open('birim.json'))
P = [json.loads(l) for l in open('cift_karar.jsonl')]
par = {}
def f(x):
    while par.get(x, x) != x: x = par[x]
    return x
for p in P:
    if p['benzerlik'] == 'ayni' and p['karar'] == 'BIRLESTIR': par[f(p['a'])] = f(p['b'])
def goster(i):
    r = R[i]; u = U[i]
    vs = {v['v']: v for v in r['variants']}
    o = vs.get('orijinal') or vs.get('p14') or vs.get('ham') or vs.get('eski') or vs.get('kok') or r['variants'][0]
    s = vs.get('site') or vs.get('kok')
    d = {'id': i, 'kaynak': u['belge'], 'sinav': f"{u['yil'] or '?'} {u['sinav'] or '?'} ({u['kesinlik']})",
         'kok': o['stem'][:900], 'siklar': {k or str(n): t[:220] for n, (k, t) in enumerate(o['opts'])},
         'cevap': r.get('answer')}
    if s and s['stem'] and s['stem'][:200] != o['stem'][:200]:
        d['site_kok'] = s['stem'][:600]
        d['site_siklar'] = {k or str(n): t[:160] for n, (k, t) in enumerate(s['opts'])}
    return d
sec = []
for p in P:
    if p['benzerlik'] != 'ayni' and f(p['a']) != f(p['b']):
        oncelik = {'BIRLESTIR': 0, 'KORU': 1, 'BEKLET': 2}[p['karar']]
        sec.append((oncelik, 'sinir', p))
random.seed(7)
ayni = [p for p in P if p['benzerlik'] == 'ayni']
for p in random.sample(ayni, 120): sec.append((0, 'orneklem', p))
sec.sort(key=lambda x: (x[0], x[2]['a']))
N = 55; parti = []
for k in range(0, len(sec), N):
    items = [{'cift': j + k, 'tur': t, 'kural_karari': p['karar'], 'A': goster(p['a']), 'B': goster(p['b'])}
             for j, (_, t, p) in enumerate(sec[k:k + N])]
    pid = f'p{k // N + 1:03d}'
    json.dump({'parti': pid, 'ciftler': items}, open(f'inceleme/parti/{pid}.json', 'w'), ensure_ascii=False, indent=1)
    parti.append(pid)
print(len(sec), len(parti), collections.Counter((x[0], x[1]) for x in sec))
