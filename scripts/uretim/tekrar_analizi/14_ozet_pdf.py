"""Ders özeti → kaynak slayt (PDF/PPTX) bağı. Kurul 1: Öğren destesi (2026-27 Drive PDF'i, deckPdfSources). Kurul 2–6: geçen yılın
(2025-26) slaytları (meds_database/sources, gecen_yil_d3/kurul N/…) dosya adı eşleşmesiyle (token_sort ≥ 85)."""
import json, glob, re, unicodedata, collections
from rapidfuzz import fuzz
ROOT = '/home/indu/medsor'
def f(s):
    s = str(s).replace('İ', 'i').replace('I', 'ı').lower().translate(str.maketrans('çğıöşü', 'cgiosu'))
    s = unicodedata.normalize('NFKD', s); s = ''.join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r'\.(md|pdf|pptx|txt)$', '', s); s = re.sub(r'\b(d3|3 sinif|donem 3|otomatik kaydedilme)\b', ' ', s)
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()
src = [json.load(open(p)) for p in glob.glob(f'{ROOT}/meds_database/sources/*.json')]
src = [d for d in src if 'gecen_yil_d3/kurul' in str(d.get('path'))]
PDF = json.load(open(f'{ROOT}/meds/src/data/deckPdfSources.json'))['decks']
OZ = json.load(open(f'{ROOT}/meds/src/data/lectureSummariesCatalog.json'))
out = {}; st = collections.Counter()
for o in OZ:
    if o['id'].startswith('k1-'):
        d = PDF.get('k1p-' + o['id'])
        if d and d.get('files'):
            out[o['id']] = [{'ad': x.get('name'), 'yol': x.get('path'), 'driveId': x.get('fileId'), 'sayfa': x.get('pages'), 'yil': '2026-2027', 'yontem': 'deste'} for x in d['files']]
            st['k1_deste'] += 1
        else: st['k1_yok'] += 1
        continue
    k = o['kurul']; a = f(o['fileName'])
    best = max(((fuzz.token_sort_ratio(a, f(d.get('name'))), d) for d in src if f'kurul {k}/' in str(d.get('path'))), default=(0, None), key=lambda x: x[0])
    if best[1] is not None and best[0] >= 85 and len(a) >= 5:
        d = best[1]
        out[o['id']] = [{'ad': d.get('name'), 'yol': d.get('path'), 'driveId': d.get('drive_id'), 'sayfa': d.get('pages'), 'yil': '2025-2026',
                         'yontem': f'dosya_adi_{round(best[0])}', 'kaynakId': d.get('source_id')}]
        st['k2_6_eslesti'] += 1
    else: st['k2_6_yok'] += 1
json.dump(out, open('ozet_cevap/ozet_pdf.json', 'w'), ensure_ascii=False, indent=1)
print(dict(st))
