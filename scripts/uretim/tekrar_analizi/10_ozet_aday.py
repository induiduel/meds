"""Cevap–ders özeti sözcüksel ön eleme: soru (kök + doğru şık) önermesinin özet penceresindeki IDF ağırlıklı kapsanması.
Çıktı ozet_cevap/aday.jsonl (her soru için en iyi 3 pencere)."""
import json, re, math, unicodedata, collections
R = {json.loads(l)['id']: json.loads(l) for l in open('sorular_ozet.jsonl')}
OZ = json.load(open('/home/indu/medsor/meds/src/data/lectureSummariesCatalog.json'))
OK = json.load(open('/home/indu/medsor/meds_temp/kurul_ders_konu/v2/ozet_konu.json'))
FOLD = str.maketrans("çğıöşüâîû", "cgiosuaiu")
STOP = set('ve ile bir bu da de icin olan olarak gibi daha en cok ya veya hangisi hangisidir asagidakilerden asagidaki '
           'degildir dogrudur yanlistir yer almaz olmaz hangileri ise ki ne nedir ait gore sonra once kadar arasinda tum her '
           'ilgili olarak edilen eden olur olup oldugu olmayan bulunan neden nedeniyle durum hasta hastada yasinda yas'.split())
def toks(s):
    s = str(s or '').replace('İ', 'i').replace('I', 'ı').lower().translate(FOLD)
    s = unicodedata.normalize('NFKD', s); s = ''.join(c for c in s if not unicodedata.combining(c))
    out = []
    for w in re.findall(r'[a-z0-9]+', s):
        if w in STOP or (len(w) < 3 and not w.isdigit()): continue
        out.append(w[:6] if not w.isdigit() else w)     # Türkçe ek toleransı: 6 harflik kök
    return out
# özet pencereleri
konu2oz = collections.defaultdict(list)
for oid, v in OK.items():
    k = v.get('konu')
    if k: konu2oz[(int(k[0]), k[1], k[2])].append(oid)
ozmap = {o['id']: o for o in OZ}
WIN = {}
df = collections.Counter()
for o in OZ:
    lines = [l.strip() for l in o['content'].split('\n')]
    lines = [l for l in lines if l and not l.startswith('<sub>') and len(l) > 3]
    units = []
    for i, l in enumerate(lines):
        units.append((i, i, l))
        if i + 1 < len(lines): units.append((i, i + 1, l + ' ' + lines[i + 1]))
    WIN[o['id']] = [(a, b, t, set(toks(t))) for a, b, t in units]
    for w in set(toks(o['content'])): df[w] += 1
N = len(OZ)
idf = lambda w: math.log((N + 1) / (df.get(w, 0) + 1)) + 1
def goster(r):
    vs = {v['v']: v for v in r['variants']}
    v = vs.get('site') or vs.get('kok') or r['variants'][0]
    return v
out = open('ozet_cevap/aday.jsonl', 'w'); C = collections.Counter()
for i, r in R.items():
    m = r.get('mufredat') or {}
    v = goster(r)
    ans = str(r.get('answer') or '').upper()
    dogru = next((t for k, t in v['opts'] if k.upper() == ans), '')
    if not m.get('konu') or not dogru: C['eksik'] += 1; continue
    oz = konu2oz.get((int(m.get('kurul') or 0), m.get('ders'), m.get('konu')), [])
    if not oz: C['ozet_yok'] += 1; continue
    ot = toks(dogru); st = [w for w in toks(v['stem']) if w not in ot]
    if not ot: C['sik_bos'] += 1; continue
    W = {w: idf(w) for w in set(ot + st)}
    tot_o = sum(W[w] for w in set(ot)); tot_s = sum(W[w] for w in set(st)) or 1
    best = []
    for oid in oz:
        for a, b, t, ts in WIN[oid]:
            co = sum(W[w] for w in set(ot) if w in ts) / tot_o
            if co < 0.34: continue
            cs = sum(W[w] for w in set(st) if w in ts) / tot_s
            sk = 0.6 * co + 0.4 * cs       # benzerlik: doğru şık ağırlıklı, kök destekli
            best.append((round(sk, 3), round(co, 3), round(cs, 3), oid, a, b, t[:700]))
    best.sort(reverse=True)
    rec = {'id': i, 'ozetler': oz, 'kok': v['stem'][:600], 'dogru': dogru[:300], 'cevap': ans,
           'adaylar': [dict(zip(('benzerlik', 'sik_kapsama', 'kok_kapsama', 'ozet', 'satir_bas', 'satir_son', 'metin'), x)) for x in best[:3]]}
    out.write(json.dumps(rec, ensure_ascii=False) + '\n')
    b0 = best[0][0] if best else 0
    C['>=0.60' if b0 >= 0.6 else ('0.45-0.60' if b0 >= 0.45 else '<0.45')] += 1
print(C)
