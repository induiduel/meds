"""Eksik/kalitesiz kalan sorular için tamamlayıcı (retry) batch üretir."""
import json, os, re, glob, sys, hashlib
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r"C:\Users\indui\Desktop\meds\scripts")
import ds_batches as B

W = r"C:\Users\indui\Desktop\meds\.meds_ds\work"
R = r"C:\Users\indui\Desktop\meds\.meds_ds"
O = r"C:\Users\indui\Desktop\meds\.meds_ds\out"
O2 = r"C:\Users\indui\Desktop\meds\.meds_ds\out_retry"
RB = os.path.join(W, "batches_retry")

LIGHT = B.LIGHT

def main():
    base = json.load(open(os.path.join(W, "questions_matched.json"), encoding='utf-8'))
    BASEMAP = {q['id']: q for q in base}
    have = {}
    for f in glob.glob(os.path.join(O, "*.json")) + glob.glob(os.path.join(O2, "*.json")):
        try:
            d = json.load(open(f, encoding='utf-8'))
        except Exception:
            continue
        for q in (d.get('questions') or []):
            if q.get('id'):
                have[q['id']] = q
    missing = [qid for qid in BASEMAP if qid not in have]
    print("tamamlanan soru:", len(have), "| eksik:", len(missing))
    if not missing:
        print("EKSİK YOK")
        return

    # eksikleri committee+discipline ile grupla (chunk 4)
    groups = defaultdict(list)
    for qid in missing:
        d = BASEMAP[qid]
        groups[(d['committeeId'], d['discipline'])].append(d)
    order = {cid: str(v[0]) for cid, v in B.EXAM_SETS.items()}
    n = 0
    for (cid, disc), items in sorted(groups.items(), key=lambda kv: (order.get(kv[0][0], ''), kv[0][1])):
        items.sort(key=lambda x: str(x.get('questionNumber') or ''))
        for i in range(0, len(items), 4):
            chunk = items[i:i + 4]
            agg = {}
            for d in chunk:
                for c in d['lectureCandidates']:
                    a = agg.setdefault(c['lectureId'], {"best": 0.0, "hits": 0, "c": c})
                    a['best'] = max(a['best'], c['matchScore'])
                    a['hits'] += 1
            pick = sorted(agg.values(), key=lambda x: -(x['best'] + x['hits'] * 12))[:7]
            common = {}
            for p in pick:
                c = p['c']
                common[c['lectureId']] = {
                    "lectureId": c['lectureId'], "path": c['path'], "title": c['title'],
                    "discipline": c['discipline'], "kurul": c['kurul'], "chars": c['chars'],
                    "evidence": B.build_evidence(B.CATALOG_BY_ID[c['lectureId']],
                                                 [B.toks(d['stem']) | B.toks(d['topic']) for d in chunk]),
                }
            bid = "retry_" + hashlib.md5((",".join(d['id'] for d in chunk)).encode()).hexdigest()[:12]
            qs_out = []
            for d in chunk:
                q = {k: d[k] for k in LIGHT}
                q['lectureMatches'] = [
                    {"lectureId": c['lectureId'], "matchScore": c['matchScore'],
                     "sameDiscipline": c['sameDiscipline'], "sections": c['sections']}
                    for c in d['lectureCandidates'] if c['lectureId'] in common
                ]
                qs_out.append(q)
            batch = {
                "batchId": bid, "committeeId": cid, "kurul": chunk[0]['kurul'],
                "committeeName": B.EXAM_SETS.get(cid, ('', ''))[1], "discipline": disc,
                "canonicalDiscipline": B.canonical_discipline(disc, cid),
                "curriculumDisciplines": B.COMMITTEE.get(cid, {}).get('disciplines', []),
                "questionCount": len(chunk), "lectureCandidates": list(common.values()),
                "questions": qs_out,
            }
            json.dump(batch, open(os.path.join(RB, bid + ".json"), "w", encoding='utf-8'),
                      ensure_ascii=False, indent=1)
            n += 1
    print("retry batch sayısı:", n)

if __name__ == "__main__":
    main()
