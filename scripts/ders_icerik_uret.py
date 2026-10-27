#!/usr/bin/env python3
"""Ders içerik paketi üretici: yayındaki kaynaklardan (deste, bilgi havuzu, terim/kısaltma katmanı, önem listesi,
varsa taslak) src/data/ders_icerik/<key>.json. Kaynak dışı veri yazılmaz; her kayıt kaynağı (slayt/sayfa) taşır.
Kullanım: python3 scripts/ders_icerik_uret.py <key> [<key> ...]   (key örn. k2-05-norolojik-muayene)
Paket biçimi ve sayfalar: docs/DERS_ICERIK_STANDARDI.md"""
import json, os, re, glob, sys
R = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
J = lambda p: json.load(open(p, encoding='utf-8'))
nz = lambda s: re.sub(r'\s+', ' ', re.sub(r'[^\wçğıöşü ]', ' ', (s or '').lower())).strip()
SIRA_ON = re.compile(r'^\s*(\d+|[a-zçğıöşü])[.)]\s+', re.I)
AL = [('etiology', 'Etiyoloji'), ('physiology_pathophysiology', 'Fizyopatoloji'), ('morphology_pathology', 'Morfoloji'), ('symptoms_clinical', 'Klinik bulgular'),
      ('pathognomonic_features', 'Ayırt edici bulgu'), ('diagnostic_methods', 'Tanı'), ('imaging_findings', 'Görüntüleme'), ('treatment', 'Tedavi')]
TUR_AD = {'spot': 'Temel bilgi', 'mekanizma': 'Mekanizma', 'tani': 'Tanı', 'tedavi': 'Tedavi', 'epidemiyoloji': 'Epidemiyoloji', 'ilac': 'İlaç', 'klinik': 'Klinik'}

def uret(key):
    kod = '-'.join(key.split('-')[:2])
    T = os.path.join(R, '..', 'meds_temp', 'ogrenci_ders', kod, 'taslak')
    dk = os.path.join(R, 'src/data/decks/items', f'k2p-{key}.json')
    deck = J(dk) if os.path.exists(dk) else {'slides': []}
    out = {'key': key, 'baslik': deck.get('title', ''), 'ozet': deck.get('overview', '')}
    # --- terimler (deste terimleri + PDF terim katmanı + taslak sözlük), kısaltmalar
    ter, gor = [], set()
    def ekle(t, a, i='', e=(), s=None):
        k = nz(t)
        if t and a and k not in gor: gor.add(k); ter.append({'t': t, 'a': a, 'i': i, 'e': list(e), 's': s})
    sz = os.path.join(T, 'sozluk.json')
    if os.path.exists(sz):
        for x in J(sz).get('yeni', []): ekle(x['term'], x['definition'], x.get('pearl', ''), x.get('aliases', []), (x.get('kanit') or {}).get('sayfa'))
    for s in deck['slides']:
        for m in s.get('medicalTerms', []): ekle(m['term'], m['explanation'], '', [], None)
    tj = os.path.join(R, 'data/sesli_anlatim/terim', key + '.json')
    if os.path.exists(tj):
        for dosya in J(tj)['d'].values():
            for sayfa, v in dosya.items():
                for x in v['t']:
                    if x.get('k') in ('terim', 'latince'): ekle(x['t'][:1].upper() + x['t'][1:], x['a'], '', [], int(sayfa))
    out['terimler'] = ter
    kis = {}
    kj = os.path.join(R, 'data/sesli_anlatim/kisaltma', key + '.json')
    if os.path.exists(kj):
        for dosya in J(kj)['d'].values():
            for v in dosya.values():
                for x in v['t']: kis[x['t']] = x.get('acilim') or x['a']
    ke = os.path.join(R, 'data/sesli_anlatim/kisaltma_elle', key + '.json')
    if os.path.exists(ke): kis.update(J(ke))
    out['kisaltmalar'] = [{'k': a, 'acilim': b} for a, b in kis.items()]
    # --- bilgi havuzu (kaynak: slayt sayfası + alıntı) → bilgiler + varlık kartları
    hp = os.path.join(T, 'bilgi_havuzu.jsonl')
    if not os.path.exists(hp): hp = os.path.join(R, '..', 'meds_database_v2', 'bilgi_havuzu', key + '.jsonl')
    havuz = [json.loads(l) for l in open(hp, encoding='utf-8')] if os.path.exists(hp) else []
    out['bilgiler'] = [{'b': r.get('varlik', ''), 'm': r['bilgi'], 's': (r.get('kanit') or {}).get('sayfa'), 'tur': r.get('tur')} for r in havuz if r.get('tur') == 'spot']
    hz = os.path.join(T, 'hastaliklar.json')
    hast = []
    if os.path.exists(hz):
        for h in J(hz):
            bol = [{'b': ad, 'm': [{'m': x} for x in h[f]]} for f, ad in AL if h.get(f)]
            if not bol: continue  # kaynakta alt başlığı olmayan kayıt boş kart olmasın
            hast.append({'id': h['id'], 'ad': h['name'], 'latin': h.get('latinName', ''), 'kat': h.get('category', ''), 'bolumler': bol, 's': sorted({x['sayfa'] for x in h.get('kanitlar', []) if x.get('sayfa')})})
    ids = {nz(h['ad']) for h in hast}
    gr = {}
    for r in havuz:
        if r.get('tur') == 'spot' and nz(r.get('varlik')) in ids: continue
        gr.setdefault(r.get('varlik', ''), []).append(r)
    for ad, rs in gr.items():
        if nz(ad) in ids: continue
        bol = {}
        for r in rs: bol.setdefault(TUR_AD.get(r.get('tur'), 'Bilgi'), []).append({'m': r['bilgi'], 's': (r.get('kanit') or {}).get('sayfa')})
        if len(rs) < 2 and rs[0].get('tur') == 'spot': continue  # tek spotluk varlık: Bilgi spotlarında zaten var
        hast.append({'id': re.sub(r'\W+', '-', nz(ad)), 'ad': ad, 'latin': '', 'kat': 'Havuz', 'bolumler': [{'b': b, 'm': m} for b, m in bol.items()], 's': sorted({x['s'] for m in bol.values() for x in m if x['s']})})
    out['hastaliklar'] = hast
    # --- önem listesi (başlık eşleşmesiyle)
    out['onemli'] = []
    for ix in glob.glob(os.path.join(R, 'src/data/k2*_onem/index.json')):
        for d in J(ix)['dersler']:
            if nz(d['baslik']) == nz(deck.get('title') or out['baslik']):
                m = J(os.path.join(os.path.dirname(ix), d['kod'] + '.json'))['maddeler']
                out['onemli'] = [{'p': x['puan'], 'b': x['baslik'], 'm': x['bilgi'], 'alt': x.get('alt', []), 'n': x.get('neden', ''), 's': [a['sayfa'] for a in x.get('alinti', [])], 'tur': x.get('tur', '')} for x in m]
    # --- deste: spot, tablo, karşılaştırma, sıralı liste, kart, mini quiz
    spot, tab, lis, kart, quiz = [], [], [], [], []
    for s in deck['slides']:
        n = s['slideNumber']; bl = s.get('bolum', '')
        for p in s.get('spotPearls', []): spot.append({'m': re.sub(r'^📌\s*\[SINAV SPOTU\]\s*', '', p), 'n': n, 'bolum': bl})
        for f in s.get('flashcards', []): kart.append({'o': f['front'], 'a': f['back'], 'c': f.get('category', ''), 'n': n})
        for it in s.get('interactiveElements', []):
            ty = it['type']
            if ty == 'interactive_table':
                tab.append({'t': it['tableTitle'], 'h': it['tableHeaders'], 'r': [[c['text'] for c in row['cells']] for row in it['tableRows']], 'n': n})
            elif ty == 'venn_grid':
                ad = {'A': it['labelA'], 'B': it['labelB'], 'both': 'İkisi de', 'neither': 'İkisi de değil'}
                tab.append({'t': it['title'], 'h': ['Ölçüt', 'Hangisine ait', 'Gerekçe'], 'r': [[i['criterion'], ad.get(i['correct'], i['correct']), i.get('explanation', '')] for i in it['items']], 'n': n, 'k': 'karsilastirma'})
            elif ty == 'before_after_slider':
                L, Rr = it['leftPoints'], it['rightPoints']
                tab.append({'t': f"{it['leftTitle']} ve {it['rightTitle']}", 'h': [it['leftTitle'], it['rightTitle']], 'r': [[L[i] if i < len(L) else '', Rr[i] if i < len(Rr) else ''] for i in range(max(len(L), len(Rr)))], 'n': n, 'k': 'karsilastirma'})
            elif ty == 'feature_bidding':
                ad = {'A': it['optionA'], 'B': it['optionB']}
                tab.append({'t': it['title'], 'h': ['Özellik', 'Hangisine ait', 'Gerekçe'], 'r': [[r['feature'], ad.get(r['correct'], r['correct']), r.get('explanation', '')] for r in it['rounds']], 'n': n, 'k': 'karsilastirma'})
            elif ty == 'swipe_matching':
                ad = {'left': it['leftCategory'], 'right': it['rightCategory']}
                tab.append({'t': it['title'], 'h': ['Öge', 'Sınıf', 'Gerekçe'], 'r': [[c['text'], ad.get(c['category'], c['category']), c.get('explanation', '')] for c in it['cards']], 'n': n, 'k': 'karsilastirma'})
            elif ty == 'causal_chain':
                lis.append({'t': it['chainTitle'], 'sira': 'numara', 'm': [{'m': SIRA_ON.sub('', x)} for x in it['steps']], 'n': n})
            elif ty == 'sequence_order':
                lis.append({'t': it['prompt'], 'sira': 'numara', 'm': [{'m': x} for x in it['steps']], 'n': n, 'a': it.get('explanation', '')})
            elif ty == 'micro_quiz':
                quiz.append({'q': it['question'], 'o': [{'k': o['key'], 't': o['text'], 'd': bool(o.get('isCorrect')), 'a': o.get('explanation', '')} for o in it['microQuizOptions']], 'n': n})
    out['spotlar'] = spot; out['tablolar'] = tab; out['listeler'] = lis; out['kartlar'] = kart; out['quiz'] = quiz
    # --- çıkmış soru konumları
    cj = os.path.join(R, 'data/sesli_anlatim/cikmis_konum', key + '.json')
    out['cikmis'] = len(J(cj)) if os.path.exists(cj) else 0
    p = os.path.join(R, 'src/data/ders_icerik', key + '.json')
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print(key, {k: len(v) for k, v in out.items() if isinstance(v, list)})
for k in sys.argv[1:]: uret(k)
