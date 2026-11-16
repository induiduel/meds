"""Kopya aday çiftleri: TF-IDF karakter n-gram ile aday üret, rapidfuzz ile sürümler arası ayrıntılı puanla → ciftler.jsonl"""
import json, re, unicodedata, numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from rapidfuzz import fuzz
R = [json.loads(l) for l in open('sorular_ozet.jsonl')]
FOLD = str.maketrans("çğıöşüâîûÇĞİÖŞÜ", "cgiosuaiucgiosu")
def fold(s):
    s = str(s or '').replace('İ', 'i').replace('I', 'ı').lower().translate(FOLD)
    s = unicodedata.normalize('NFKD', s); s = ''.join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r'^\s*(soru\s*)?\d{1,3}\s*[\).\-:]\s*', ' ', s)          # soru numarası
    s = re.sub(r'https?://\S+|sinav\.\S+|\d{1,2}[./]\d{1,2}[./]\d{2,4}', ' ', s)
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()
def otext(t):
    t = re.sub(r'^\s*[a-eA-E]\s*[\).\-:]\s*', '', str(t or ''))
    return fold(t)
for r in R:
    vs = []
    for v in r['variants']:
        st = fold(v['stem']); op = [otext(t) for _, t in v['opts'] if otext(t)]
        if st or op: vs.append((v['v'], st, op, v['opts']))
    r['_v'] = vs
    prim = vs[0] if vs else ('', '', [], [])
    r['_doc'] = prim[1] + ' || ' + ' | '.join(sorted(prim[2]))
docs = [r['_doc'] for r in R]
vec = TfidfVectorizer(analyzer='char_wb', ngram_range=(3, 5), min_df=2, sublinear_tf=True)
X = vec.fit_transform(docs)
stems = [' '.join({v[1] for v in r['_v']}) for r in R]
Xs = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=1, sublinear_tf=True).fit_transform(stems)
pairs = set()
B = 500
for i0 in range(0, len(R), B):
    S = (X[i0:i0 + B] @ X.T).toarray(); S2 = (Xs[i0:i0 + B] @ Xs.T).toarray()
    for a in range(S.shape[0]):
        i = i0 + a
        for j in np.where((S[a] >= 0.45) | (S2[a] >= 0.55))[0]:
            if j > i: pairs.add((i, int(j)))
print('aday', len(pairs))
def opt_match(A, Bo):
    if not A or not Bo: return None
    used = set(); tot = 0; hit = 0
    for a in A:
        best, bj = 0, -1
        for j, b in enumerate(Bo):
            if j in used: continue
            s = fuzz.ratio(a, b)
            if s > best: best, bj = s, j
        if bj >= 0 and best >= 80: used.add(bj); hit += 1
    return hit / max(len(A), len(Bo))
def correct_text(r):
    # yalnız sitede görünen sürümün cevabına göre doğru şık metni
    for v in r['variants']:
        if v['v'] in ('site', 'kok'):
            for k, t in v['opts']:
                if k.upper() == str(r.get('answer') or '').upper(): return otext(t)
    return ''
out = open('ciftler.jsonl', 'w'); n = 0
for i, j in sorted(pairs):
    a, b = R[i], R[j]
    best = (0, None, None); bpart = 0; om = None
    for va in a['_v']:
        for vb in b['_v']:
            if not va[1] or not vb[1]: continue
            s = fuzz.ratio(va[1], vb[1])
            if s > best[0]: best = (s, va[0], vb[0])
            if min(len(va[1]), len(vb[1])) >= 35:
                bpart = max(bpart, fuzz.partial_ratio(va[1], vb[1]))
            m = opt_match(va[2], vb[2])
            if m is not None: om = m if om is None else max(om, m)
    ca, cb = correct_text(a), correct_text(b)
    ans = None if not ca or not cb else round(fuzz.ratio(ca, cb))
    stoks = min(len(a['_v'][0][1].split()) if a['_v'] else 0, len(b['_v'][0][1].split()) if b['_v'] else 0)
    if best[0] < 60 and bpart < 85 and (om or 0) < 0.6: continue
    out.write(json.dumps({'a': a['id'], 'b': b['id'], 'stem': round(best[0], 1), 'part': round(bpart, 1), 'opt': om,
                          'ans': ans, 'stoks': stoks, 'va': best[1], 'vb': best[2]}, ensure_ascii=False) + '\n'); n += 1
print('yazılan', n)
