import json, os, glob, re, sys
sys.stdout.reconfigure(encoding='utf-8')
OUT = r"C:\Users\indui\Desktop\meds\.meds_ds\out"
BAT = r"C:\Users\indui\Desktop\meds\.meds_ds\work\batches"
CAT = {}
import glob as g
for f in g.glob(r"C:\Users\indui\Desktop\meds_database\redakte_ozet\Kurul *\*\*.md"):
    CAT[f] = open(f, encoding='utf-8', errors='replace').read()

def norm(s):
    return re.sub(r'\s+', ' ', re.sub(r'[^\wçğıöşüÇĞİÖŞÜ ]', ' ', (s or '').lower())).strip()

files = sorted(glob.glob(os.path.join(OUT, "*.json")))
print(f"{'soru':14}{'lecId':18}{'cov':8}{'evid':12}{'alıntı_bulundu':16}{'ilk40'}")
tot = found = miss = 0
for f in files:
    bid = os.path.basename(f)[:-5]
    b = json.load(open(os.path.join(BAT, bid + ".json"), encoding='utf-8'))
    paths = {c['lectureId']: c['path'] for c in b['lectureCandidates']}
    d = json.load(open(f, encoding='utf-8'))
    for q in d['questions']:
        for lm in (q.get('lectureMatches') or []):
            tot += 1
            lid = lm.get('lectureId')
            quote = lm.get('evidenceQuote') or ''
            p = paths.get(lid)
            txt = CAT.get(p, '') if p else ''
            # alıntıyı ders notunda ara (ilk 90 karakter üzerinden)
            probe = norm(quote)[:90]
            ok = False
            if probe and txt:
                nt = norm(txt)
                ok = probe in nt
                if not ok:
                    # kelime bazlı kısmi eşleşme
                    words = [w for w in probe.split() if len(w) > 4][:12]
                    if words:
                        hitn = sum(1 for w in words if w in nt)
                        ok = hitn >= max(3, int(len(words) * 0.6))
            found += ok
            miss += (not ok)
            if not ok:
                print(f"{q['id']:14}{(lid or '')[:16]:18}{(lm.get('coverage') or '')[:7]:8}{(q.get('evidenceStatus') or '')[:11]:12}{'YOK':16}{probe[:60]}")
print(f"\ntoplam eşleşme: {tot} | ders notunda bulundu: {found} | bulunamadı: {miss}")

# kanıt bulunamayanların coverage dağılımı
print("\n### kapsam dağılımı ###")
from collections import Counter
cc = Counter()
for f in files:
    d = json.load(open(f, encoding='utf-8'))
    for q in d['questions']:
        for lm in (q.get('lectureMatches') or []):
            cc[(lm.get('coverage'), q.get('evidenceStatus'))] += 1
for k, v in cc.most_common(): print("  ", k, v)

print("\n### 'kullanilamaz' ve 'inceleme_gerekli' örnekleri ###")
n = 0
for f in files:
    d = json.load(open(f, encoding='utf-8'))
    for q in d['questions']:
        if q.get('status') != 'onaylandi':
            print(f"\n[{q['id']}] status={q['status']} reason={q.get('reviewReason','')[:150]}")
            print("   stem:", q['stem'][:200])
            n += 1
            if n >= 5: break
    if n >= 5: break
