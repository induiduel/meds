"""Soru ↔ sınav ↔ kurul ↔ ders ↔ konu ↔ kazanım ↔ ders özeti ↔ Öğren destesi ↔ ders notu ↔ PDF ilişki dizini.

Girdiler: pastQuestions.json (sinavKimligi + checkSolve.mufredat), ozet_cevap/konu_ozet_haritasi.json (11_ozet_harita.py),
kazanım kataloğu (slayt → deckId, sayfa), deckPdfSources.json, ders_notlari_k1/index.json, birlestirmeler.json.
Çıktı: meds_database_v2/iliski/soru_iliskileri.json (soru başına) + konu_iliskileri.json (konu başına kaynak listesi).
`--yaz`: her soruya küçük `iliski` alanı {ozet, deste, dersNotu, pdf} yazılır (meds-web durdurulmuş olmalı).
"""
import json, collections, os, re, sys, shutil, datetime
ROOT = '/home/indu/medsor'
D = f'{ROOT}/meds/src/data'
OUT = f'{ROOT}/meds_database_v2/iliski'
PQ = f'{D}/pastQuestions.json'
YAZ = '--yaz' in sys.argv
Q = json.load(open(PQ))
H = json.load(open('ozet_cevap/konu_ozet_haritasi.json'))          # "kurul|ders|konu" -> [{id, kapsam}]
OZ = {o['id']: o for o in json.load(open(f'{D}/lectureSummariesCatalog.json'))}
PDF = json.load(open(f'{D}/deckPdfSources.json'))['decks']
DN = {x['id']: x for x in json.load(open(f'{ROOT}/meds_database_v2/ders_notlari_k1/index.json'))}
OPDF = json.load(open('ozet_cevap/ozet_pdf.json'))
MG = json.load(open(f'{ROOT}/meds_database_v2/soru_birlestirme/birlestirmeler.json'))['gruplar']
asil_of = {u: g['asil'] for g in MG if g.get('durum') != 'ayrildi' for u in g['uyeler']}

# konu -> desteler (kazanım slaytlarındaki deckId) + kazanım -> slayt sayfaları
konu_deste = collections.defaultdict(collections.Counter); kz_slayt = {}
for k in range(1, 7):
    c = json.load(open(f'{D}/kazanimlar/k{k}.json'))
    for de in c['dersler']:
        for ko in de['konular']:
            key = f"{k}|{de['ders']}|{ko['konu']}"
            for z in ko['kazanimlar']:
                sl = [s for s in z.get('slaytlar') or [] if s.get('deckId')]
                for s in sl: konu_deste[key][s['deckId']] += 1
                kz_slayt[z['id']] = [{'deste': s['deckId'], 'sayfa': s.get('sayfa'), 'alinti': (s.get('alinti') or '')[:80]} for s in sl[:4]]
def desteler_of(ozetler, key):
    out = []
    for o in ozetler:                         # Kurul 1: özet kimliği = ders notu = deste (k1p-<id>, V2: k1p-k1-NN-…-v2)
        m = re.match(r'^(k1-\d\d)-', o['id'])
        if m:
            for d in PDF:
                if d == 'k1p-' + o['id'] or (d.startswith('k1p-' + m.group(1) + '-') and d.endswith('-v2')): out.append(d)
    for d, _ in konu_deste[key].most_common():
        if d in PDF and d not in out: out.append(d)
        elif d not in PDF and 'k1p-' + d in PDF and 'k1p-' + d not in out: out.append('k1p-' + d)
    return out
def pdf_of(deste):
    f = (PDF.get(deste) or {}).get('files') or []
    return [{'ad': x.get('name'), 'yol': x.get('path'), 'sayfa_sayisi': x.get('pages'), 'driveId': x.get('fileId')} for x in f]

S = {}; K = {}; st = collections.Counter()
for q in Q:
    m = (q.get('checkSolve') or {}).get('mufredat') or {}
    sk = q.get('sinavKimligi') or {}
    rec = {'soru': q['id'], 'gorunen': asil_of.get(q['id'], q['id']),
           'sinav': {k: sk.get(k) for k in ('yil', 'sinav', 'etiket', 'kesinlik')},
           'kurul': m.get('kurul'), 'ders': m.get('ders'), 'konu': m.get('konu'),
           'kazanim': {'id': m.get('kazanimId'), 'metin': m.get('kazanim')} if m.get('kazanimId') else None}
    key = f"{m.get('kurul')}|{m.get('ders')}|{m.get('konu')}"
    oz = H.get(key, []) if m.get('konu') else []
    rec['ozetler'] = [{'id': o['id'], 'baslik': OZ[o['id']]['title'], 'kapsam': o.get('kapsam', 'tam')} for o in oz if o['id'] in OZ]
    ds = desteler_of(rec['ozetler'], key) if m.get('konu') else []
    rec['desteler'] = [{'id': d, 'baslik': PDF[d].get('title')} for d in ds]
    rec['dersNotlari'] = [{'id': o['id'], 'dosya': DN[o['id']]['dosya']} for o in rec['ozetler'] if o['id'] in DN]
    pdfs = []
    for d in ds:
        for p in pdf_of(d):
            if p['ad'] not in {x['ad'] for x in pdfs}: pdfs.append(dict(p, yil='2026-2027', kaynak='deste:' + d))
    for o in rec['ozetler']:
        for p in OPDF.get(o['id'], []):
            if p['ad'] not in {x['ad'] for x in pdfs}:
                pdfs.append({'ad': p['ad'], 'yol': p['yol'], 'sayfa_sayisi': p.get('sayfa'), 'driveId': p.get('driveId'), 'yil': p.get('yil'), 'kaynak': 'ozet:' + o['id']})
    rec['pdf'] = pdfs[:3]
    if rec['kazanim'] and kz_slayt.get(rec['kazanim']['id']): rec['kazanimSlaytlari'] = kz_slayt[rec['kazanim']['id']]
    S[q['id']] = rec
    for f in ('ozetler', 'desteler', 'dersNotlari', 'pdf'): st[f + ('_var' if rec[f] else '_yok')] += 1
    if m.get('konu'):
        k = K.setdefault(key, {'kurul': m.get('kurul'), 'ders': m.get('ders'), 'konu': m.get('konu'), 'ozetler': rec['ozetler'],
                               'desteler': rec['desteler'], 'dersNotlari': rec['dersNotlari'], 'pdf': rec['pdf'], 'sorular': [], 'gorunenSoru': 0})
        k['sorular'].append(q['id']); k['gorunenSoru'] += rec['gorunen'] == q['id']
os.makedirs(OUT, exist_ok=True)
json.dump(S, open(f'{OUT}/soru_iliskileri.json', 'w'), ensure_ascii=False)
json.dump(sorted(K.values(), key=lambda x: (x['kurul'] or 0, x['ders'] or '', x['konu'] or '')), open(f'{OUT}/konu_iliskileri.json', 'w'), ensure_ascii=False, indent=1)
print(dict(st)); print('konu', len(K), 'özetsiz konu', sum(1 for k in K.values() if not k['ozetler']))
if YAZ:
    ts = datetime.datetime.now().strftime('%Y%m%d%H%M'); os.makedirs(f'{ROOT}/yedek/iliski_{ts}', exist_ok=True)
    shutil.copy(PQ, f'{ROOT}/yedek/iliski_{ts}/pastQuestions.json')
    for q in Q:
        r = S[q['id']]
        q['iliski'] = {'ozet': [o['id'] for o in r['ozetler']], 'deste': [d['id'] for d in r['desteler']][:3],
                       'dersNotu': [d['id'] for d in r['dersNotlari']], 'pdf': [p['ad'] for p in r['pdf']], 'surum': 'iliski-v1'}
    json.dump(Q, open(PQ + '.tmp', 'w'), ensure_ascii=False); os.replace(PQ + '.tmp', PQ); shutil.copy(PQ, f'{ROOT}/meds/data/pastQuestions.json')
    print('YAZILDI')
