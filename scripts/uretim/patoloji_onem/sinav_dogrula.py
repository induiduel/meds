import json, os, sys, glob
W = os.path.dirname(os.path.abspath(__file__))
SRC = {}
for f in glob.glob(f'{W}/partiler/*.json'):
    for d in json.load(open(f)): SRC[d['kod']] = d
te = 0
for p in sys.argv[1:]:
    o = json.load(open(p)); k = o.get('kod'); e = []
    s = SRC.get(k)
    if not s: print('HATA', p, 'kod girdide yok'); te += 1; continue
    ids = {m['id'] for m in s['maddeler']}; M = o.get('maddeler') or {}
    if set(M) != ids: e.append(f'maddeler eksik/fazla: eksik {sorted(ids - set(M))[:5]} fazla {sorted(set(M) - ids)[:5]}')
    for i, v in M.items():
        if v.get('kaynak') not in ('metin', 'tablo', 'sekil'): e.append(f'{i}: kaynak geçersiz')
        if not isinstance(v.get('klinik'), bool): e.append(f'{i}: klinik true/false olmalı')
    A = o.get('adaylar') or []
    lo, hi = (5, 7) if k == '15' else (3, 5)
    if not lo <= len(A) <= hi: e.append(f'adaylar {len(A)} ({lo}–{hi})')
    if [a.get('sira') for a in A] != list(range(1, len(A) + 1)): e.append('sira 1..n sıralı olmalı')
    for a in A:
        v = M.get(a.get('id'))
        if not v: e.append(f"aday {a.get('id')} madde değil"); continue
        if v.get('kaynak') != 'metin' or v.get('klinik'): e.append(f"aday {a['id']} sınava uygun değil (tablo/şekil/klinik)")
        g = str(a.get('gerekce') or '')
        if len(g.split()) < 6: e.append(f"aday {a['id']}: gerekce kısa")
        if any(w in g.lower() for w in ('aday', 'ipucu', 'talimat')): e.append(f"aday {a['id']}: gerekce iç terim içeriyor")
    if len({a.get('id') for a in A}) != len(A): e.append('aday tekrar')
    for x in e: print('HATA', k, x)
    te += len(e)
print(te, 'HATA'); sys.exit(1 if te else 0)
