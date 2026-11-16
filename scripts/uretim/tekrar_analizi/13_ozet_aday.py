"""Cevap ↔ ders özeti sözcüksel adaylar (ters dizin).

Önerme = sitede görünen kök + doğru şık. Benzerlik (0–1) = 0,6 × doğru şık kapsaması + 0,4 × kök kapsaması
(IDF ağırlıklı, 6 harflik kök eşleşmesi; özet penceresi = 1 ya da ardışık 2 satır).
Arama alanı: sorunun konusuna bağlı özet(ler) (konu_ozet_haritasi.json) + aynı kurulun diğer özetleri (eşik aynı, `konu_disi` işaretli).
Yalnız görünen sorular (gizli kopyalar asıldan devralır). Çıktı: ozet_cevap/aday2.jsonl (soru başına en iyi 3 pencere).
"""
import json, re, math, unicodedata, collections
ROOT = '/home/indu/medsor'; D = f'{ROOT}/meds/src/data'
Q = json.load(open(f'{D}/pastQuestions.json'))
OZ = json.load(open(f'{D}/lectureSummariesCatalog.json'))
H = json.load(open('ozet_cevap/konu_ozet_haritasi.json'))
MG = json.load(open(f'{ROOT}/meds_database_v2/soru_birlestirme/birlestirmeler.json'))['gruplar']
gizli = {u for g in MG if g.get('durum') != 'ayrildi' for u in g['uyeler'] if u != g['asil']}
FOLD = str.maketrans("çğıöşüâîû", "cgiosuaiu")
STOP = set('ve ile bir bu da de icin olan olarak gibi daha en cok ya veya hangisi hangisidir asagidakilerden asagidaki '
           'degildir dogrudur yanlistir yer almaz olmaz hangileri ise ki ne nedir ait gore sonra once kadar arasinda tum her '
           'ilgili edilen eden olur olup oldugu olmayan bulunan neden nedeniyle durum hasta hastada yasinda yas ifade ifadeler '
           'verilen verilmistir soru sik asagida yukaridaki hangisinde hangisine hangisinin'.split())
def toks(s):
    s = str(s or '').replace('İ', 'i').replace('I', 'ı').lower().translate(FOLD)
    s = unicodedata.normalize('NFKD', s); s = ''.join(c for c in s if not unicodedata.combining(c))
    return [w if w.isdigit() else w[:6] for w in re.findall(r'[a-z0-9]+', s) if w not in STOP and (len(w) >= 3 or w.isdigit())]
W = []; inv = collections.defaultdict(set); df = collections.Counter(); kurul_of = {}
for o in OZ:
    kurul_of[o['id']] = int(o.get('kurul') or 0)
    lines = [l.strip() for l in o['content'].split('\n')]
    lines = [l for l in lines if len(l) > 3 and not l.startswith('<sub>')]
    for w in set(toks(o['content'])): df[w] += 1
    for i, l in enumerate(lines):
        for t in ([l] + ([l + '\n' + lines[i + 1]] if i + 1 < len(lines) else [])):
            n = len(W); ts = set(toks(t)); W.append((o['id'], i, t, ts))
            for w in ts: inv[w].add(n)
N = len(OZ)
idf = lambda w: math.log((N + 1) / (df.get(w, 0) + 1)) + 1
out = open('ozet_cevap/aday2.jsonl', 'w'); C = collections.Counter()
for q in Q:
    if q['id'] in gizli: continue
    rec = q.get('reconstruction') if isinstance(q.get('reconstruction'), dict) else {}
    stem = rec.get('stem') or q.get('stem') or ''
    opts = rec.get('options') or q.get('options') or []
    ans = str(rec.get('correctAnswer') or q.get('correctAnswer') or '').upper()
    dogru = next((o.get('text', '') for o in opts if isinstance(o, dict) and str(o.get('key', '')).upper() == ans), '')
    m = (q.get('checkSolve') or {}).get('mufredat') or {}
    if not dogru or not stem: C['eksik'] += 1; continue
    ot = set(toks(dogru)); st = set(toks(stem)) - ot
    if not ot: C['sik_bos'] += 1; continue
    w8 = {w: idf(w) for w in ot | st}; to = sum(w8[w] for w in ot); ts_ = sum(w8[w] for w in st) or 1
    konu_oz = {o['id'] for o in H.get(f"{m.get('kurul')}|{m.get('ders')}|{m.get('konu')}", [])}
    kurul = int(m.get('kurul') or 0)
    aday = set()
    for w in ot: aday |= inv.get(w, set())
    best = []
    for n in aday:
        oid, li, t, wt = W[n]
        if oid not in konu_oz and kurul_of[oid] != kurul: continue
        co = sum(w8[w] for w in ot if w in wt) / to
        if co < 0.5: continue
        cs = sum(w8[w] for w in st if w in wt) / ts_
        sk = 0.6 * co + 0.4 * cs
        if sk >= 0.45: best.append((round(sk, 3), round(co, 3), round(cs, 3), oid, li, t[:900], oid not in konu_oz))
    best.sort(key=lambda x: (-x[0], x[6]))
    # aynı satır tekrarlarını ayıkla
    seen = set(); top = []
    for b in best:
        if (b[3], b[4]) in seen: continue
        seen.add((b[3], b[4])); top.append(b)
        if len(top) == 3: break
    b0 = top[0][0] if top else 0
    C['>=0.60' if b0 >= 0.6 else ('0.45-0.60' if b0 >= 0.45 else 'yok')] += 1
    if top and top[0][6]: C['en_iyi_konu_disi'] += 1
    out.write(json.dumps({'id': q['id'], 'konu': [m.get('kurul'), m.get('ders'), m.get('konu')], 'konu_ozetleri': sorted(konu_oz),
                          'kok': stem[:700], 'dogru': dogru[:300], 'cevap': ans,
                          'olumsuz': bool(re.search(r'değildir|değil|yer almaz|beklenmez|görülmez|olmaz|yanlıştır|bulunmaz|kullanılmaz|söylenemez', stem, re.I)),
                          'adaylar': [dict(zip(('benzerlik', 'sik_kapsama', 'kok_kapsama', 'ozet', 'satir', 'metin', 'konu_disi'), b)) for b in top]},
                         ensure_ascii=False) + '\n')
print(dict(C))
