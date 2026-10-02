"""
Adım 4: Batch çıktılarını birleştir, doğrula, onar ve tek JSONL dosyası üret.
"""
import json, os, re, sys, glob, hashlib
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8')
from ds_quote_index import norm, idx

def build_lookup():
    """Hızlı kelime erişimi için ders notu kelime kümeleri."""
    lut = []
    for x in idx:
        lut.append((x, set(x['norm'].split())))
    return lut

LUT = build_lookup()
from difflib import SequenceMatcher

def verify_quote_fast(quote, hint_discipline=None, topk=12, thresh=0.5):
    nq = norm(quote)
    words = [w for w in nq.split() if len(w) > 4]
    if not words or len(nq) < 40:
        return None, 0.0
    scored = []
    for x, ws in LUT:
        hits = sum(1 for w in words if w in ws)
        if hits < max(3, int(len(words) * 0.5)):
            continue
        bonus = 30 if hint_discipline and hint_discipline.split('(')[0].strip() in x['discipline'] else 0
        scored.append((hits + bonus, x))
    if not scored:
        return None, 0.0
    scored.sort(key=lambda t: -t[0])
    best = (0.0, None)
    for _s, x in scored[:topk]:
        # hızlı kontrol: alıntının ilk 12 kelimesi geçiyor mu
        probe = ' '.join(words[:12])
        if probe in x['norm']:
            return x, 1.0
        for i in range(0, max(1, len(x['norm']) - 150), 45):
            r = SequenceMatcher(None, nq[:200], x['norm'][i:i + 230]).ratio()
            if r > best[0]:
                best = (r, x)
            if r > 0.9:
                return x, r
    return best[1], best[0]

BASE = r"C:\Users\indui\Desktop\meds_database"
WORK = r"C:\Users\indui\Desktop\meds\.meds_ds\work"
OUT = r"C:\Users\indui\Desktop\meds\.meds_ds\out"
BAT = os.path.join(WORK, "batches")

ALLOWED = {
    "answerStatus": {"dogrulandi", "duzeltildi", "dogrulanamadi", "belirsiz"},
    "evidenceStatus": {"kanitli", "kismi_kanit", "not_yok"},
    "coverage": {"guclu", "orta", "zayif", "yok"},
    "curriculumFit": {"uyumlu", "kismen_uyumlu", "uyumsuz"},
    "status": {"onaylandi", "inceleme_gerekli", "kullanilamaz"},
}

MOJI = re.compile(r'[ÃÄÅÂ]|&apos;|&quot;|&#\d+;')

def clean(s):
    if not s:
        return ""
    s = s.replace('&apos;', "'").replace('&quot;', '"').replace('&#39;', "'")
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

def build():
    base = json.load(open(os.path.join(WORK, "questions_matched.json"), encoding='utf-8'))
    BASEMAP = {q['id']: q for q in base}
    print("temel soru:", len(BASEMAP))

    files = sorted(glob.glob(os.path.join(OUT, "*.json"))) + \
            sorted(glob.glob(os.path.join(WORK, "out_retry", "*.json")))
    print("batch çıktısı:", len(files))

    records = {}
    issues = Counter()
    dup_group = {}
    for f in files:
        bid = os.path.basename(f)[:-5]
        try:
            d = json.load(open(f, encoding='utf-8'))
        except Exception as e:
            issues['bozuk_json'] += 1
            print("BOZUK JSON:", bid, e)
            continue
        bpath = os.path.join(BAT, bid + ".json")
        if not os.path.exists(bpath):
            bpath = os.path.join(WORK, "batches_retry", bid + ".json")
        b = json.load(open(bpath, encoding='utf-8'))
        src = {q['id']: q for q in b['questions']}
        cand_ids = {c['lectureId'] for c in b['lectureCandidates']}
        got = set()
        for q in d.get('questions') or []:
            qid = q.get('id')
            if not qid or qid not in src:
                issues['bilinmeyen_id'] += 1
                continue
            got.add(qid)
            orig = src[qid]
            # --- alan doğrulama ve onarım ---
            opts = q.get('options') or []
            opts = [{"key": (o.get('key') or '').strip().upper()[:1], "text": clean(o.get('text') or ''),
                     "isCorrect": bool(o.get('isCorrect'))} for o in opts if isinstance(o, dict)]
            if [o['key'] for o in opts] != ['A', 'B', 'C', 'D', 'E']:
                issues['sik_anahtar_onarildi'] += 1
                for i, o in enumerate(opts):
                    if i < 5 and o['key'] not in 'ABCDE':
                        o['key'] = 'ABCDE'[i]
            corr = [o['key'] for o in opts if o['isCorrect']]
            ca = (q.get('correctAnswer') or '').strip().upper()[:1]
            if len(corr) != 1 or (corr and ca != corr[0]):
                issues['cevap_onarildi'] += 1
                if len(corr) == 1:
                    ca = corr[0]
                elif ca in [o['key'] for o in opts]:
                    for o in opts:
                        o['isCorrect'] = (o['key'] == ca)
                    corr = [ca]
            if len(opts) != 5 or len(corr) != 1:
                issues['sik_yapisi_bozuk'] += 1
            st = q.get('status') if q.get('status') in ALLOWED['status'] else 'inceleme_gerekli'
            an = q.get('answerStatus') if q.get('answerStatus') in ALLOWED['answerStatus'] else 'dogrulanamadi'
            ev = q.get('evidenceStatus') if q.get('evidenceStatus') in ALLOWED['evidenceStatus'] else 'not_yok'
            cf = q.get('curriculumFit') if q.get('curriculumFit') in ALLOWED['curriculumFit'] else 'kismen_uyumlu'

            # --- ders notu eşleşmelerini doğrula (uydurma ID/alıntı temizliği) ---
            lm_out = []
            for lm in (q.get('lectureMatches') or []):
                lid = lm.get('lectureId')
                if lid not in cand_ids:
                    issues['uydurma_lectureid_silindi'] += 1
                    continue
                quote = clean(lm.get('evidenceQuote') or '')
                nq = norm(quote)
                if len(nq.split()) < 8:
                    issues['kisa_alinti_silindi'] += 1
                    continue
                lec, rat = verify_quote_fast(quote, q.get('discipline') or orig.get('discipline'))
                if not lec or rat < 0.5:
                    issues['dogrulanmayan_alinti_silindi'] += 1
                    continue
                lm_out.append({"lectureId": lid, "matchType": clean(lm.get('matchType') or 'konu_eslesmesi'),
                               "coverage": lm.get('coverage') if lm.get('coverage') in ALLOWED['coverage'] else 'orta',
                               "evidenceQuote": quote})
            if not lm_out and ev == 'kanitli':
                issues['kanitsiz_kanitli_not_yoka_cevrildi'] += 1
                ev = 'not_yok'
            if lm_out and ev == 'not_yok':
                ev = 'kismi_kanit'

            exp = clean(q.get('explanation') or '')
            if len(exp) < 250:
                issues['kisa_aciklama'] += 1
            if not clean(q.get('stem') or ''):
                issues['bos_kok'] += 1
            if MOJI.search((q.get('stem') or '') + exp + (q.get('topic') or '')):
                issues['mojibake_kaldi'] += 1

            disc = clean(q.get('discipline') or orig['discipline'])
            topic = clean(q.get('topic') or orig['topic'])
            rec = {
                "id": qid,
                "committeeId": orig['committeeId'],
                "folderKey": orig['folderKey'],
                "donem": orig['donem'],
                "kurul": orig['kurul'],
                "examSet": orig['committeeId'],
                "examYear": orig['examYear'],
                "questionNumber": orig.get('questionNumber'),
                "discipline": disc,
                "topic": topic,
                "stem": clean(q.get('stem') or ''),
                "options": opts,
                "correctAnswer": ca,
                "explanation": exp,
                "evidenceText": clean(q.get('evidenceText') or ''),
                "lectureMatches": lm_out,
                "source": {
                    "file": orig.get('sourceFile') or '',
                    "rawStem": orig.get('hamSoru') or '',
                },
                "verification": {
                    "answerStatus": an,
                    "evidenceStatus": ev,
                    "confidence": round(float(q.get('confidence') or 0.0), 2)
                    if isinstance(q.get('confidence'), (int, float)) else 0.0,
                    "curriculumFit": cf,
                    "status": st,
                    "qualityScore": int(q.get('qualityScore') or 0)
                    if isinstance(q.get('qualityScore'), (int, float)) else 0,
                    "changes": [c for c in (q.get('changes') or []) if isinstance(c, str)],
                    "needsReview": bool(q.get('needsReview')) or st != 'onaylandi',
                    "reviewReason": clean(q.get('reviewReason') or ''),
                },
                "duplicateOf": q.get('duplicateOf') or None,
            }
            # RAG için türetilmiş alanlar
            rec["optionsText"] = " ".join(f"{o['key']}) {o['text']}" for o in opts)
            rec["lectureRefs"] = [{"lectureId": m["lectureId"],
                                   "title": os.path.basename(
                                       next((c['path'] for c in b['lectureCandidates']
                                             if c['lectureId'] == m["lectureId"]), ""))[:-3],
                                   "coverage": m["coverage"]} for m in lm_out]
            rec["embeddingText"] = (f"{rec['discipline']} - {rec['topic']}. {rec['stem']} "
                                    f"{rec['optionsText']} Doğru cevap: {ca}. {exp} "
                                    f"{rec['evidenceText']}").strip()
            if q.get('duplicateOf'):
                dup_group[qid] = q['duplicateOf']
            records[qid] = rec

        missing = set(src) - got
        if missing:
            issues['eksik_soru'] += len(missing)
            print(f"EKSİK {bid}: {sorted(missing)[:6]}")

    # batch çıktısı olmayan / eksik kalan sorular için temel kayıt üret
    for qid, orig in BASEMAP.items():
        if qid in records:
            continue
        issues['temel_kayittan_tamamlandi'] += 1
        rec = {
            "id": qid, "committeeId": orig['committeeId'], "folderKey": orig['folderKey'],
            "donem": orig['donem'], "kurul": orig['kurul'], "examSet": orig['committeeId'],
            "examYear": orig['examYear'], "questionNumber": orig.get('questionNumber'),
            "discipline": clean(orig['discipline']), "topic": clean(orig['topic']),
            "stem": clean(orig['stem']), "options": orig['options'],
            "correctAnswer": (orig.get('correctAnswer') or '').strip().upper()[:1],
            "explanation": clean(orig['explanation']), "evidenceText": "",
            "lectureMatches": [],
            "source": {"file": orig.get('sourceFile') or '', "rawStem": orig.get('hamSoru') or ''},
            "verification": {"answerStatus": "dogrulanamadi", "evidenceStatus": "not_yok",
                             "confidence": 0.5, "curriculumFit": "kismen_uyumlu",
                             "status": "inceleme_gerekli", "qualityScore": 50,
                             "changes": [], "needsReview": True,
                             "reviewReason": "AI doğrulaması bu soru için tamamlanamadı."},
            "duplicateOf": None,
        }
        rec["optionsText"] = " ".join(f"{o['key']}) {o['text']}" for o in rec['options'])
        rec["lectureRefs"] = []
        rec["embeddingText"] = (f"{rec['discipline']} - {rec['topic']}. {rec['stem']} "
                                f"{rec['optionsText']} Doğru cevap: {rec['correctAnswer']}. "
                                f"{rec['explanation']}").strip()
        records[qid] = rec

    print("\n### BİRLEŞTİRME SORUNLARI ###")
    for k, v in issues.most_common():
        print(f"  {k}: {v}")

    return records, BASEMAP

def finalize(records, BASEMAP, outpath):
    rows = list(records.values())
    # sıralama: dönem/kurul sırası, branş, soru no
    order = {"donem3-kurul1": 1, "donem3-kurul2": 2, "donem3-kurul3": 3, "donem3-kurul4": 4,
             "donem3-kurul5": 5, "donem3-kurul6": 6, "donem3-final": 7, "donem3-butunleme": 8}
    rows.sort(key=lambda r: (order.get(r['committeeId'], 99), r['discipline'],
                             r.get('questionNumber') or 0, r['id']))
    with open(outpath, "w", encoding='utf-8', newline='\n') as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False, separators=(',', ':')) + "\n")
    return rows

if __name__ == "__main__":
    recs, base = build()
    out = os.path.join(WORK, "meds_donem3_sorulari_duzeltilmis.jsonl")
    rows = finalize(recs, base, out)
    size = os.path.getsize(out)
    print(f"\n### ÇIKTI ###\n{out}\n{len(rows)} kayıt | {size/1e6:.2f} MB")

    st = Counter(r['verification']['status'] for r in rows)
    an = Counter(r['verification']['answerStatus'] for r in rows)
    ev = Counter(r['verification']['evidenceStatus'] for r in rows)
    cf = Counter(r['verification']['curriculumFit'] for r in rows)
    disc = Counter(r['discipline'] for r in rows)
    print("\nstatus:", st.most_common())
    print("answerStatus:", an.most_common())
    print("evidenceStatus:", ev.most_common())
    print("curriculumFit:", cf.most_common())
    print("kanıtlı soru:", sum(1 for r in rows if r['lectureMatches']))
    print("ortalama kalite:", round(sum(r['verification']['qualityScore'] for r in rows) / len(rows), 1))
    print("ortalama açıklama uzunluğu:", round(sum(len(r['explanation']) for r in rows) / len(rows)))
    print("\nbranş dağılımı:")
    for k, v in disc.most_common():
        print(f"  {v:4}  {k}")

    # --- son kalite kontrolü ---
    print("\n### SON KALİTE KONTROLÜ ###")
    prob = Counter()
    for r in rows:
        o = r['options']
        if len(o) != 5 or [x['key'] for x in o] != list('ABCDE'):
            prob['sik_yapisi'] += 1
        if sum(1 for x in o if x['isCorrect']) != 1:
            prob['dogru_sik_sayisi'] += 1
        if r['correctAnswer'] not in [x['key'] for x in o]:
            prob['cevap_uyumsuz'] += 1
        if len(r['stem']) < 20:
            prob['kisa_kok'] += 1
        if len(r['explanation']) < 250:
            prob['kisa_aciklama'] += 1
        if MOJI.search(r['stem'] + r['explanation'] + r['topic'] + r['optionsText']):
            prob['mojibake'] += 1
        if not r['embeddingText']:
            prob['bos_embedding'] += 1
        for m in r['lectureMatches']:
            if not m['evidenceQuote'] or len(m['evidenceQuote'].split()) < 8:
                prob['zayif_alinti'] += 1
    print("sorun:" if prob else "sorun yok:", dict(prob) if prob else "")
    ids = [r['id'] for r in rows]
    print("tekil id:", len(set(ids)), "/", len(ids))
    print("kanıtlı soru:", sum(1 for r in rows if r['lectureMatches']),
          "| eşleşme sayısı:", sum(len(r['lectureMatches']) for r in rows))
    print("onaylı+inceleme+kullanılamaz:",
          f"{st.get('onaylandi',0)} / {st.get('inceleme_gerekli',0)} / {st.get('kullanilamaz',0)}")
    print("ortalama embedding uzunluğu:", round(sum(len(r['embeddingText']) for r in rows) / len(rows)))
    print("dosya boyutu: %.2f MB" % (size / 1e6))
