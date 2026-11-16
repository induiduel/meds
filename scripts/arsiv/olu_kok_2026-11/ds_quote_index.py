"""Tüm ders notları için global doğrulama indeksi + alıntı doğrulama."""
import json, os, re, sys, glob
from difflib import SequenceMatcher
sys.stdout.reconfigure(encoding='utf-8')
BASE = ((__import__('os').environ.get('MEDS_DATABASE_DIR') or __import__('os').path.expanduser('~/meds_database')))
RZ = os.path.join(BASE, "redakte_ozet")

def norm(s):
    s = (s or '').lower().replace('İ', 'i').replace('I', 'ı')
    s = re.sub(r'[^\wçğıöşü ]', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()

idx = []
for f in glob.glob(os.path.join(RZ, "Kurul *", "*", "*.md")):
    parts = os.path.relpath(f, RZ).split(os.sep)
    txt = open(f, encoding='utf-8', errors='replace').read()
    idx.append({
        "path": f, "kurul": parts[0], "discipline": parts[1],
        "title": os.path.basename(f)[:-3], "chars": len(txt), "norm": norm(txt),
    })
print("indekslenen ders notu:", len(idx), "| toplam karakter:", sum(x['chars'] for x in idx))

def verify_quote(quote, hint_discipline=None):
    nq = norm(quote)
    if len(nq) < 25:
        return None
    words = [w for w in nq.split() if len(w) > 4]
    if not words:
        return None
    cands = idx
    if hint_discipline:
        pref = [x for x in idx if hint_discipline.split('(')[0].strip() in x['discipline']]
        if pref:
            cands = pref + [x for x in idx if x not in pref]
    best = (0.0, None)
    for x in cands[:len(idx)]:
        hits = sum(1 for w in words if w in x['norm'])
        if hits < max(3, int(len(words) * 0.5)):
            continue
        # benzerlik penceresi
        for i in range(0, max(1, len(x['norm']) - 150), 50):
            r = SequenceMatcher(None, nq[:200], x['norm'][i:i + 230]).ratio()
            if r > best[0]:
                best = (r, x)
        if best[0] > 0.9:
            break
        if hint_discipline and best[1] and hint_discipline.split('(')[0].strip() in best[1]['discipline'] and best[0] > 0.6:
            break
    return best

if __name__ == "__main__":
    OUT = (__import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__))) + "/.meds_ds/out")
    BAT = (__import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__))) + "/.meds_ds/work/batches")
    stats = {"tam": 0, "id_yanlis": 0, "uydurma": 0, "kisa": 0}
    for f in sorted(glob.glob(os.path.join(OUT, "*.json"))):
        bid = os.path.basename(f)[:-5]
        b = json.load(open(os.path.join(BAT, bid + ".json"), encoding='utf-8'))
        paths = {c['lectureId']: c['path'] for c in b['lectureCandidates']}
        d = json.load(open(f, encoding='utf-8'))
        for q in d['questions']:
            for lm in (q.get('lectureMatches') or []):
                qq = lm.get('evidenceQuote') or ''
                if len(norm(qq)) < 25:
                    stats['kisa'] += 1
                    continue
                rat, lec = verify_quote(qq, q.get('discipline'))
                actual = paths.get(lm.get('lectureId'))
                if actual and lec and os.path.normcase(os.path.abspath(actual)) == os.path.normcase(os.path.abspath(lec['path'])):
                    stats['tam'] += 1
                elif lec and rat > 0.55:
                    stats['id_yanlis'] += 1
                    print(f"ID-DÜZELT {q['id']:12} verilen={lm.get('lectureId')} -> {os.path.basename(lec['path'])} ({rat:.2f})")
                else:
                    stats['uydurma'] += 1
                    print(f"UYDURMA?  {q['id']:12} lec={lm.get('lectureId')} oran={(rat if lec else 0):.2f} :: {qq[:130]}")
    print("\n### ALINTI DOĞRULAMA ###")
    for k, v in stats.items():
        print(f"  {k}: {v}")
