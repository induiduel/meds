#!/usr/bin/env python3
"""Soru ekle yazım yardımcısı için yerel dil modeli üretir → src/data/composer_model.json

Kaynak: src/data/pastQuestions.json (soru kökleri + şıklar; sözlük için açıklamalar).
  --exclude-ids <dosya>  : simülasyon için test kümesindeki soruları dışarıda bırakır
  --out <yol>            : çıktı yolu
Model:
  ng   : bağlam (son 1-3 katlanmış kelime) → [[sonraki yüzey kelime, sayı], ...]
  vocab: katlanmış kelime → sayı | [yüzey biçim, sayı]  (tamamlama + yazım düzeltme)
  acc  : ASCII biçim → Türkçe karakterli biçim (yalnız belirsizlik yoksa)
"""
import json, re, sys, argparse, unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ap = argparse.ArgumentParser()
ap.add_argument('--exclude-ids')
ap.add_argument('--out', default=str(ROOT / 'src/data/composer_model.json'))
a = ap.parse_args()

excl = set(json.load(open(a.exclude_ids))) if a.exclude_ids else set()
qs = [q for q in json.load(open(ROOT / 'src/data/pastQuestions.json')) if q.get('id') not in excl]

LOW = str.maketrans({'I': 'ı', 'İ': 'i'})
ASC = str.maketrans('çğıöşüâîû', 'cgiosuaiu')

def low(s): return unicodedata.normalize('NFC', s.translate(LOW).lower()).replace('i̇', 'i')
def fold(w): return re.sub(r"[^\wçğıöşüâîû%/+-]", '', low(w))
def asc(w): return w.translate(ASC)

def clean_stem(s):
    s = re.sub(r'\s+', ' ', s or '').strip()
    s = re.sub(r'^\(?\d+[.)-]\s*', '', s)  # soru numarası
    return s

stems, texts = [], []
for q in qs:
    st = clean_stem(q.get('stem') or '')
    if len(st.split()) >= 3: stems.append(st)
    texts.append(st)
    # açıklamalar yalnız sözlüğe girer (geçerli çekimleri tanımak için; n-gram köklerden kurulur)
    for k in ('explanation', 'tibbi_aciklama'):
        if isinstance(q.get(k), str): texts.append(q[k])
    for o in (q.get('options') or []):
        texts.append(o.get('text', '') if isinstance(o, dict) else str(o))

# ---- sözcük dağarcığı
surf = defaultdict(Counter)
for t in texts:
    for w in t.split():
        f = fold(w)
        if len(f) < 2 or not re.search(r'[a-zçğıöşü]', f): continue
        sw = re.sub(r'^[^\w]+|[^\w%]+$', '', w)
        surf[f][sw if sw.isupper() and len(sw) <= 6 else low(sw)] += 1  # kısaltmalar (CRP, EKG) büyük kalır
vocab = {}
for f, c in surf.items():
    n = sum(c.values())
    if n >= 2:
        sw = c.most_common(1)[0][0]
        vocab[f] = n if sw == f else [sw, n]  # yüzey biçim anahtarla aynıysa yalnız sayı

# ---- Türkçe karakter geri kazanımı: yalnız ASCII biçimi kendi başına geçmiyorsa ve tek baskın aday varsa
byasc = defaultdict(list)
for f, v in vocab.items():
    n = v if isinstance(v, int) else v[1]
    if asc(f) != f: byasc[asc(f)].append((n, f))
acc = {}
for k, cands in byasc.items():
    if len(k) < 3: continue
    ov = vocab.get(k, 0)
    own = ov if isinstance(ov, int) else ov[1]
    cands.sort(reverse=True)
    n, best = cands[0]
    tot = sum(c for c, _ in cands)
    if n >= 2 and own * 4 <= n and n >= 0.85 * tot: acc[k] = best

# ---- n-gram (soru köklerinden)
ng = defaultdict(Counter)
for st in stems:
    ws = st.split()
    fs = ['^'] + [fold(w) for w in ws]
    out = ws
    for i, w in enumerate(out):
        j = i + 1  # fs indeksi
        for k in (1, 2, 3):
            if j - k < 0: break
            ctx = ' '.join(fs[j - k:j])
            ng[ctx][w] += 1
model_ng = {}
for ctx, c in ng.items():
    k = ctx.count(' ') + 1
    keep = [[w, n] for w, n in c.most_common(6) if n >= (2 if k > 1 else 3)]
    if keep: model_ng[ctx] = keep

json.dump({'v': 2, 'ng': model_ng, 'vocab': vocab, 'acc': acc}, open(a.out, 'w'), ensure_ascii=False, separators=(',', ':'))
print(f'kök={len(stems)} ng={len(model_ng)} vocab={len(vocab)} acc={len(acc)} → {a.out} ({Path(a.out).stat().st_size//1024} KB)')
