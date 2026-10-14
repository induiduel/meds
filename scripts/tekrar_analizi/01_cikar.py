"""Her çıkmış soru için metin sürümleri + sınav ipuçları → sorular_ozet.jsonl (salt okuma)."""
import json, os, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
qs = json.load(open('/home/indu/medsor/meds/data/pastQuestions.json'))
SRC = '/home/indu/medsor/meds_database/sources'
_sn = {}
def sname(sf):
    if sf is None: return None
    sf = str(sf)
    if sf in _sn: return _sn[sf]
    p = f'{SRC}/{sf}.json'
    v = sf
    if re.fullmatch(r'[0-9a-f]{12}', sf) and os.path.exists(p):
        d = json.load(open(p)); v = d.get('path') or d.get('name') or sf
    _sn[sf] = v; return v
def opts(o):
    if isinstance(o, dict): o = [{'key': k, 'text': v} for k, v in o.items()]
    out = []
    for x in o or []:
        if isinstance(x, dict): out.append((str(x.get('key') or x.get('label') or ''), str(x.get('text') or '')))
        else: out.append(('', str(x)))
    return out
out = open(f'{ROOT}/sorular_ozet.jsonl', 'w')
for q in qs:
    variants = []
    for name, d in [('orijinal', q.get('checkSolveOriginal')), ('p14', q.get('phase14Original')), ('eski', q.get('eskiSurum')),
                    ('ham', q.get('rawQuestion')), ('site', q.get('reconstruction')), ('kok', {'stem': q.get('stem'), 'options': q.get('options')})]:
        if isinstance(d, dict) and (d.get('stem') or d.get('options')):
            variants.append({'v': name, 'stem': str(d.get('stem') or ''), 'opts': opts(d.get('options'))})
    if q.get('rawStem'): variants.append({'v': 'rawStem', 'stem': q['rawStem'], 'opts': []})
    cs = q.get('checkSolve') or {}
    rec = {
        'id': q['id'], 'sourceFile': q.get('sourceFile'), 'kaynak': sname(q.get('sourceFile')),
        'examYear': q.get('examYear'), 'committeeId': q.get('committeeId'), 'originalCommitteeId': q.get('originalCommitteeId'),
        'sourceNote': q.get('sourceNote'), 'booklet': q.get('booklet'), 'questionNumber': q.get('questionNumber'),
        'evidence': q.get('evidence'), 'splitFrom': q.get('splitFrom'), 'status': q.get('status'),
        'csStatus': cs.get('status'), 'discipline': q.get('discipline'), 'topic': q.get('topic'),
        'kazanim': (q.get('kazanim') or {}).get('id'), 'mufredat': cs.get('mufredat'),
        'answer': q.get('correctAnswer'), 'tags': q.get('tags'), 'yilDuzeltmesi': q.get('yilDuzeltmesi'),
        'variants': variants, 'mergedQuestionIds': q.get('mergedQuestionIds'),
        'examOccurrences': q.get('examOccurrences'),
    }
    out.write(json.dumps(rec, ensure_ascii=False) + '\n')
print(len(qs))
