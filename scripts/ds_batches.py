"""
Adım 2 (v2): Soru -> ders notu aday eşleştirmesi + AI doğrulama iş birimleri.
- Final/Bütünleme sınavları kümülatif olduğundan TÜM kurul ders notlarına bakar.
- Her aday için en ilgili bölüm (heading) ve kanıt pasajı çıkarılır.
"""
import json, os, re, sys, glob, hashlib
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r"C:\Users\indui\Desktop\meds\scripts")
from ds_pipeline import (BASE, RS, WORK, RZ, COMMITTEE, EXAM_SETS,
                         clean_text, build_lecture_catalog)

BATCHDIR = os.path.join(WORK, "batches")
os.makedirs(BATCHDIR, exist_ok=True)

TR_STOP = set("""ve ile için bir bu da de mi ne ki en çok daha göre kadar sonra önce
olan olarak olduğu hangisidir hangisi aşağıdakilerden aşağıdaki değildir yapılır
hastalığı hastalık hastada hasta tanı tedavi klinik bulgu bulguları etken etkisi
tipi türü şekli nedeni nedir doğru yanlış hangileri aşağıdakilerden hangisi
aşağıdakilerden hangisinin değildir biri biriyle ilgili olan olduğu""".split())

def toks(s):
    s = (s or '').lower().replace('İ', 'i').replace('I', 'ı')
    return set(w for w in re.findall(r'[a-zçğıöşü]{4,}', s) if w not in TR_STOP)

CATALOG = build_lecture_catalog()
CATALOG_BY_ID = {}
for _c in CATALOG:
    _prep_needed = True
    CATALOG_BY_ID[_c['lectureId']] = _c

def _split_sections(txt):
    """(heading, govde) listesi döndürür."""
    parts = re.split(r'^(#{2,3}\s+.+)$', txt, flags=re.M)
    out = []
    for i in range(1, len(parts), 2):
        h = clean_text(parts[i].lstrip('#').strip())
        body = parts[i + 1] if i + 1 < len(parts) else ''
        out.append((h, body))
    return out

def _is_question_section(h):
    """Ders notundaki 'çıkmış soru' bloklarını ayıkla: kanıt yalnızca anlatımdan gelsin."""
    return bool(re.match(r'^\s*(Soru|Question)\s*\d*\s*[:.\-]', h)) or 'ÇIKMIŞ' in h.upper()

def _prep(c):
    if '_tokens' in c:
        return c
    # anlatım gövdesi: hem 'çıkmış sorular' hem 'spot bilgiler' bölümü hariç
    body = re.split(r'##\s*🎯', c['text'])[0]
    body = re.split(r'##\s*⚡', body)[0]
    c['_tokens'] = toks(body)
    c['_headtokens'] = toks(' '.join(c['headings']))
    c['_title_tokens'] = toks(c['title'])
    c['_sections'] = [(h, b) for h, b in _split_sections(c['text']) if not _is_question_section(h)]
    teaching = re.split(r'##\s*(?:🎯|⚡)', c['text'])[0]
    c['_sec_tokens'] = [(h, toks(h + ' ' + b[:4000]), b) for h, b in _split_sections(teaching)
                        if not _is_question_section(h)]
    return c

def snippet_for(q_tokens, c, width=900, maxn=2):
    """Sorunun anahtar kelimeleriyle en örtüşen bölümden kanıt pasajı."""
    return _sections_for(q_tokens, c, width=width, maxn=maxn)

def _sections_for(q_tokens, c, width=1600, maxn=3):
    scored = []
    for h, st, body in c.get('_sec_tokens', []):
        ov = len(q_tokens & st)
        if ov:
            scored.append((ov, h, body))
    scored.sort(key=lambda x: -x[0])
    out = []
    for ov, h, body in scored[:maxn]:
        clean_body = clean_text(body, keep_newlines=True)
        paras = [p.strip() for p in re.split(r'\n\s*\n|\n(?=- )', clean_body) if len(p.strip()) > 80]
        if not paras:
            paras = [clean_body[:width]]
        paras.sort(key=lambda p: -len(q_tokens & toks(p)))
        picked, total = [], 0
        for p in paras:
            if total >= width:
                break
            chunk = re.sub(r'\s+', ' ', p)[:width - total]
            picked.append(chunk)
            total += len(chunk)
        out.append({"heading": h[:160], "excerpt": ' '.join(picked)[:width], "termOverlap": ov})
    return out

def build_evidence(c, q_tokens_list, cap=14000):
    """Bir ders notu için batch'teki tüm soruları kapsayan kanıt paketi."""
    merged_tokens = set()
    for t in q_tokens_list:
        merged_tokens |= t
    heads = _sections_for(merged_tokens, c, width=1500, maxn=5)
    # hiç örtüşme yoksa ders notunun en bilgi yoğun ilk bölümlerini ver
    if not heads:
        heads = [{"heading": h, "excerpt": re.sub(r'\s+', ' ', clean_text(b, keep_newlines=True))[:900],
                  "termOverlap": 0} for h, _st, b in c.get('_sec_tokens', [])[:3]]
    out, total = [], 0
    for h in heads:
        if total >= cap:
            break
        e = h['excerpt'][:cap - total]
        out.append({"heading": h['heading'], "excerpt": e, "termOverlap": h['termOverlap']})
        total += len(e)
    return out

def match_lectures(q, topn=5, min_overlap=2):
    qt = toks(q['stem']) | toks(q['topic']) | toks(q['explanation'][:1200])
    if not qt:
        return []
    q_disc = re.sub(r'\s*\(.*?\)', '', q['discipline']).strip()
    scored = []
    for c in CATALOG:
        _prep(c)
        ov = len(qt & c['_tokens'])
        head_ov = len(qt & c['_headtokens'])
        title_ov = len(qt & c['_title_tokens'])
        same_disc = 1 if (q_disc and (q_disc in c['discipline'] or c['discipline'] in q_disc)) else 0
        # gürültü filtresi: anlamlı örtüşme şartı
        if ov < min_overlap and head_ov == 0 and title_ov == 0:
            continue
        # kümülatif sınavlarda (final/bütünleme) kurul serbest, aksi halde aynı kurul öncelikli
        kurul_bonus = 0.0
        if str(c['kurul']) == str(q['kurul']):
            kurul_bonus = 20.0
        elif q['committeeId'] in ('donem3-final', 'donem3-butunleme'):
            kurul_bonus = 0.0
        else:
            kurul_bonus = -25.0
        score = ov * 1.0 + head_ov * 5.0 + title_ov * 8.0 + same_disc * 22.0 + kurul_bonus
        if score <= 0:
            continue
        scored.append((score, ov, head_ov, same_disc, c))
    scored.sort(key=lambda x: -x[0])

    out = []
    seen_disc = Counter()
    for s, ov, ho, sd, c in scored:
        # aynı ders notundan en fazla 3, aynı branştan en fazla 3 aday
        if seen_disc[c['discipline']] >= 3:
            continue
        seen_disc[c['discipline']] += 1
        out.append({
            "lectureId": c['lectureId'], "path": c['path'], "title": c['title'],
            "discipline": c['discipline'], "kurul": c['kurul'], "chars": c['chars'],
            "matchScore": round(s, 1), "termOverlap": ov, "headingOverlap": ho,
            "sameDiscipline": bool(sd),
            "sections": snippet_for(qt, c),
        })
        if len(out) >= topn:
            break
    return out

def canonical_discipline(disc, committee_id):
    """Müfredattaki kanonik branş adına eşle (parantezli alt uzmanlıkları koru)."""
    canon = COMMITTEE.get(committee_id, {}).get('disciplines', [])
    base = re.sub(r'\s*\(.*?\)', '', disc).strip()
    aliases = {
        'Pediatri': 'Çocuk Sağlığı ve Hastalıkları',
        'Kadın Doğum': 'Kadın Hastalıkları ve Doğum',
        'FTR': 'Fiziksel Tıp ve Rehabilitasyon',
        'Tıbbi Biyokimya': 'Tıbbi Biyokimya',
        'Tıbbi Biyoloji ve Genetik': 'Tıbbi Genetik',
    }
    b = aliases.get(base, base)
    for c in canon:
        if b and (b in c or c in b):
            return c
    for c in canon:
        if disc and (disc in c or c in disc):
            return c
    return disc

LIGHT = ["id", "committeeId", "folderKey", "donem", "kurul", "discipline", "topic",
         "questionNumber", "examYear", "sourceFile", "stem", "options", "correctAnswer",
         "explanation", "hamSoru", "qualityFlags"]

def main():
    docs = json.load(open(os.path.join(WORK, "questions_normalized.json"), encoding='utf-8'))
    print("soru:", len(docs))

    nomatch = []
    for d in docs:
        d['lectureCandidates'] = match_lectures(d)
        if not d['lectureCandidates']:
            nomatch.append(d)
    print("aday ders notu bulunamayan soru:", len(nomatch))
    if nomatch:
        print("  kurul:", Counter(str(d['kurul']) for d in nomatch).most_common())
        print("  branş:", Counter(d['discipline'] for d in nomatch).most_common(12))
        for d in nomatch[:6]:
            print(f"   - [{d['id']}] {d['discipline']} | {d['topic']} | {d['stem'][:90]}")

    json.dump(docs, open(os.path.join(WORK, "questions_matched.json"), "w", encoding='utf-8'),
              ensure_ascii=False, indent=1)

    groups = defaultdict(list)
    for d in docs:
        groups[(d['committeeId'], d['discipline'])].append(d)

    order = {cid: str(v[0]) for cid, v in EXAM_SETS.items()}
    batches = []
    for (cid, disc), items in sorted(groups.items(), key=lambda kv: (order.get(kv[0][0], ''), kv[0][1])):
        items.sort(key=lambda x: str(x.get('questionNumber') or ''))
        CH = 14
        for i in range(0, len(items), CH):
            chunk = items[i:i + CH]
            agg = {}
            for d in chunk:
                for c in d['lectureCandidates']:
                    a = agg.setdefault(c['lectureId'], {"best": 0.0, "hits": 0, "c": c})
                    a['best'] = max(a['best'], c['matchScore'])
                    a['hits'] += 1
            pick = sorted(agg.values(), key=lambda x: -(x['best'] + x['hits'] * 12))[:9]
            common = {}
            for p in pick:
                c = p['c']
                common[c['lectureId']] = {
                    "lectureId": c['lectureId'], "path": c['path'], "title": c['title'],
                    "discipline": c['discipline'], "kurul": c['kurul'], "chars": c['chars'],
                    "evidence": build_evidence(CATALOG_BY_ID[c['lectureId']],
                                               [toks(d['stem']) | toks(d['topic']) for d in chunk]),
                }
            bid = f"{cid}__{hashlib.md5(disc.encode()).hexdigest()[:6]}__{i//CH+1:02d}"
            qs_out = []
            for d in chunk:
                q = {k: d[k] for k in LIGHT}
                q['lectureMatches'] = [
                    {"lectureId": c['lectureId'], "matchScore": c['matchScore'],
                     "sameDiscipline": c['sameDiscipline'], "sections": c['sections']}
                    for c in d['lectureCandidates'] if c['lectureId'] in common
                ]
                qs_out.append(q)
            batches.append({
                "batchId": bid, "committeeId": cid, "kurul": chunk[0]['kurul'],
                "committeeName": EXAM_SETS.get(cid, ('', ''))[1],
                "discipline": disc,
                "canonicalDiscipline": canonical_discipline(disc, cid),
                "curriculumDisciplines": COMMITTEE.get(cid, {}).get('disciplines', []),
                "questionCount": len(chunk),
                "lectureCandidates": list(common.values()),
                "questions": qs_out,
            })

    for b in batches:
        json.dump(b, open(os.path.join(BATCHDIR, b['batchId'] + ".json"), "w", encoding='utf-8'),
                  ensure_ascii=False, indent=1)
    json.dump(batches, open(os.path.join(WORK, "batches_index.json"), "w", encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print("\nbatch sayısı:", len(batches))
    print(Counter(b['committeeId'] for b in batches).most_common())
    # boyut kontrolü
    sizes = [(os.path.getsize(os.path.join(BATCHDIR, b['batchId'] + '.json')), b['batchId']) for b in batches]
    sizes.sort()
    print("en küçük batch dosyaları (byte):", sizes[:2])
    print("en büyük batch dosyaları (byte):", sizes[-2:])

    b = batches[0]
    print(f"\n### ÖRNEK BATCH {b['batchId']} | {b['discipline']} | {b['questionCount']} soru")
    for c in b['lectureCandidates']:
        print(f"   CAND {c['discipline'][:26]:28} {c['title'][:58]}")
        for s in c['evidence'][:1]:
            print(f"        § {s['heading'][:80]} | {s['excerpt'][:170]}")

if __name__ == "__main__":
    main()
