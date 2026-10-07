"""Teslim edilen dosyanın kaynak 1279 soruya karşı kapsama ve kalite raporu."""
import json, os, re, sys
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding='utf-8')

W = (__import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__))) + "/.meds_ds/work")
TARGET = ((__import__('os').environ.get('MEDS_DATABASE_DIR') or __import__('os').path.expanduser('~/meds_database')) + "/deepseek_data/meds_donem3_sorulari_duzeltilmis.jsonl")
MOJI = re.compile(r'[ÃÄÅÂ]|&apos;|&quot;|&#\d+;')

base = json.load(open(os.path.join(W, "questions_matched.json"), encoding='utf-8'))
BASE = {q['id']: q for q in base}

rows = [json.loads(l) for l in open(TARGET, encoding='utf-8') if l.strip()]
have = {r['id']: r for r in rows}

print("=" * 78)
print("TESLİM RAPORU")
print("=" * 78)
print(f"hedef dosya        : {TARGET}")
print(f"boyut              : {os.path.getsize(TARGET)/1e6:.2f} MB")
print(f"kayıt              : {len(rows)}")
print(f"kaynak soru        : {len(BASE)}")
missing = [q for q in BASE if q not in have]
print(f"kapsama            : {len(rows)}/{len(BASE)}  (%{100*len(rows)//len(BASE)})")
print(f"eksik              : {len(missing)}")

ord_ = ['donem3-kurul1','donem3-kurul2','donem3-kurul3','donem3-kurul4',
        'donem3-kurul5','donem3-kurul6','donem3-final','donem3-butunleme']
tot = Counter(q['committeeId'] for q in BASE.values())
got = Counter(r['committeeId'] for r in rows)
print("\n--- Kurul bazında ---")
for c in ord_:
    t, g = tot.get(c, 0), got.get(c, 0)
    bar = "█" * int(20 * g / max(1, t))
    print(f"  {c:18} {g:4}/{t:<4} {bar:20} {'TAM' if g == t else 'EKSİK ' + str(t-g)}")

print("\n--- Doğrulama durumu ---")
st = Counter(r['verification']['status'] for r in rows)
an = Counter(r['verification']['answerStatus'] for r in rows)
ev = Counter(r['verification']['evidenceStatus'] for r in rows)
cf = Counter(r['verification']['curriculumFit'] for r in rows)
for k, v in st.most_common():
    print(f"  status {k:18} {v:5} (%{100*v//len(rows)})")
print()
for k, v in an.most_common():
    print(f"  cevap  {k:18} {v:5}")
print()
for k, v in ev.most_common():
    print(f"  kanıt  {k:18} {v:5}")
print()
for k, v in cf.most_common():
    print(f"  müfredat {k:16} {v:5}")

print("\n--- Ders notu eşleştirme ---")
n_lec = sum(1 for r in rows if r['lectureMatches'])
n_match = sum(len(r['lectureMatches']) for r in rows)
print(f"  kanıtlı soru       : {n_lec} (%{100*n_lec//len(rows)})")
print(f"  toplam eşleşme     : {n_match}")
print(f"  ortalama eşleşme   : {n_match/max(1,len(rows)):.2f}")
cov = Counter(m['coverage'] for r in rows for m in r['lectureMatches'])
for k, v in cov.most_common():
    print(f"  kapsam {k:12} {v:5}")

print("\n--- Değişiklik türleri ---")
ch = Counter(c for r in rows for c in r['verification']['changes'])
for k, v in ch.most_common():
    print(f"  {k:28} {v:5}")

print("\n--- Kalite ---")
el = sorted(len(r['explanation']) for r in rows)
print(f"  açıklama min/med/max : {el[0]}/{el[len(el)//2]}/{el[-1]}")
print(f"  açıklama <300        : {sum(1 for x in el if x < 300)}")
print(f"  ortalama kalite puanı: {sum(r['verification']['qualityScore'] for r in rows)/len(rows):.1f}")
print(f"  ortalama güven       : {sum(r['verification']['confidence'] for r in rows)/len(rows):.2f}")

print("\n--- Yapısal kontrol ---")
prob = Counter()
for r in rows:
    o = r['options']
    if len(o) != 5 or [x['key'] for x in o] != list('ABCDE'): prob['sik_yapisi'] += 1
    if sum(1 for x in o if x['isCorrect']) != 1: prob['dogru_sik'] += 1
    if r['correctAnswer'] not in [x['key'] for x in o]: prob['cevap_uyumsuz'] += 1
    if len(r['stem']) < 20: prob['kisa_kok'] += 1
    if MOJI.search(r['stem'] + r['explanation'] + r['topic'] + r['optionsText']): prob['mojibake'] += 1
    if not r['embeddingText']: prob['bos_embedding'] += 1
    if not r['discipline'] or not r['topic']: prob['alan_eksik'] += 1
    for m in r['lectureMatches']:
        if len((m.get('evidenceQuote') or '').split()) < 8: prob['zayif_alinti'] += 1
print("  sorunlar:", dict(prob) if prob else "yok")
print(f"  tekil id: {len(set(r['id'] for r in rows))}/{len(rows)}")

print("\n--- İnceleme gerektirenler (ilk 15) ---")
n = 0
for r in rows:
    if r['verification']['status'] != 'onaylandi':
        print(f"  [{r['id']}] {r['verification']['status']:18} {r['discipline'][:26]:28} {r['verification']['reviewReason'][:70]}")
        n += 1
        if n >= 15:
            break

if missing:
    print("\n--- Eksik sorular ---")
    mc = Counter(BASE[m]['committeeId'] for m in missing)
    print(" ", mc.most_common())
