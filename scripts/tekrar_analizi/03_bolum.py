"""Her soruya kaynak-bölüm (segment) ata + kesin kopya kenarları + bölüm örtüşme matrisi."""
import json, re, collections
R = {json.loads(l)['id']: json.loads(l) for l in open('sorular_ozet.jsonl')}
# combinepdf (28) sayfa aralıkları → (bölüm, etiket)
CP = [(1,100,'cp-S0','?'),(101,139,'cp-K1a','K1 tarihsiz'),(140,178,'cp-K1b','K1 tarihsiz'),(179,235,'cp-K1c','2020-21 K1 #585310'),
      (236,254,'cp-K1d','2020-21 K1 #585245'),(255,289,'cp-K2z','2020-21 K2 #901009'),(290,337,'cp-K2a','2020-21 K2 #901070'),
      (338,373,'cp-K2b','K2 tarihsiz'),(374,421,'cp-K2c','2020-21 K2 #901070 (2.baskı)'),(422,473,'cp-K2d','2020-21 K2 #901035'),
      (474,523,'cp-K2e','2020-21 K2 #901005'),(524,575,'cp-K3a','2020-21 K3 #1222389'),(576,614,'cp-K3b','K3 tarihsiz'),
      (615,653,'cp-K3c','K3 tarihsiz'),(654,708,'cp-K3d','2020-21 K3 #1222370'),(709,757,'cp-K4a','2020-21 K4 #1255798'),
      (758,799,'cp-K4b','2020-21 K4 #1255882'),(800,842,'cp-K4c','2020-21 K4 #1255828'),(843,874,'cp-K4d','K4 tarihsiz'),
      (875,921,'cp-K5a','2020-21 K5 #1473066'),(922,955,'cp-K5b','K5 tarihsiz'),(956,993,'cp-K5c','K5 tarihsiz'),
      (994,1038,'cp-K5d','2020-21 K5 #1472982'),(1039,1090,'cp-K5e','2020-21 K5 #1473012'),(1091,1139,'cp-K5f','2020-21 K5 #1473047'),
      (1140,1189,'cp-K5g','2020-21 K5 #1472988'),(1190,1236,'cp-K5h','2020-21 K5 #1472989'),(1237,1274,'cp-K6a','K6 tarihsiz'),
      (1275,1323,'cp-K6b','2020-21 K6 #1671873'),(1324,1379,'cp-K6c','2020-21 K6 #1671854'),(1380,1431,'cp-K6d','2020-21 K6 #1671819'),
      (1432,1480,'cp-K6e','2020-21 K6 #1671796')]
def seg(r):
    i = r['id']
    m = re.match(r'^(k1-\d{4}-\d{4}(?:-[a-d])?)-q\d+$', i)
    if m: return 'D3K1pdf:' + m.group(1)
    if r['sourceFile'] == 'c4259dc9087e':
        ps = [int(x.group(1)) for e in (r.get('evidence') or []) for x in [re.search(r':p(\d+)', str(e))] if x]
        if ps:
            for a, b, s, _ in CP:
                if a <= ps[0] <= b: return s
        return 'cp-?'
    k = str(r.get('kaynak') or 'yok')
    k = re.sub(r'\.(pdf|txt|pptx|json|md|docx)(\.pdf)*$', '', k, flags=re.I)
    k = k.replace('%20', ' ')
    note = str(r.get('sourceNote') or '')
    if re.search(r'_Kurul\d_Cikmis_Sorular|_Donem3_Kurul1_Cikmis', k):   # ders bazlı derleme: notta yıl varsa bölüm
        y = re.search(r'(20\d\d)-(20\d\d)', note)
        return f'derleme:{k}:{y.group(0) if y else "?"}'
    return 'dosya:' + k
for r in R.values(): r['seg'] = seg(r)
json.dump({i: r['seg'] for i, r in R.items()}, open('bolum.json', 'w'), ensure_ascii=False)
segsize = collections.Counter(r['seg'] for r in R.values())
# kesin kopya kenarları
P = [json.loads(l) for l in open('ciftler.jsonl')]
def fold(s): 
    return s
num = lambda s: tuple(sorted(re.findall(r'\d+(?:[.,]\d+)?', re.sub(r'^\s*\d{1,3}\s*[\).\-]', '', s or ''))))
def vstem(r, v):
    for x in r['variants']:
        if x['v'] == v: return x['stem']
    return ''
E = []
for p in P:
    a, b = R[p['a']], R[p['b']]
    s, o, pt, ans = p['stem'], p['opt'], p['part'], p['ans']
    ne = num(vstem(a, p['va'])) == num(vstem(b, p['vb']))
    if (s >= 90 and (o is None or o >= 0.8) and ne) or (s >= 80 and o is not None and o >= 0.8 and (ans or 0) >= 90 and ne) \
       or (pt >= 95 and o is not None and o >= 0.8 and ne):
        E.append((p['a'], p['b']))
json.dump(E, open('kesin_kenarlar.json', 'w'))
print('kesin kenar', len(E))
# bölüm örtüşmesi: A'daki sorulardan B'de kopyası olanların sayısı
link = collections.defaultdict(lambda: collections.defaultdict(set))
for x, y in E:
    sx, sy = R[x]['seg'], R[y]['seg']
    link[sx][sy].add(x); link[sy][sx].add(y)
rows = []
for sa in link:
    for sb in link[sa]:
        if sa < sb or sa == sb:
            na, nb = len(link[sa][sb]), len(link[sb][sa])
            ov = max(na / segsize[sa], nb / segsize[sb])
            rows.append((round(ov, 2), sa, segsize[sa], na, sb, segsize[sb], nb))
rows.sort(reverse=True)
with open('bolum_ortusme.tsv', 'w') as f:
    for r in rows: f.write('\t'.join(map(str, r)) + '\n')
print(len(rows))
for r in rows[:120]: print(r)
