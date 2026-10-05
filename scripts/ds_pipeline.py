"""
Dönem 3 - Çıkmış soru + ders notu eşleştirme ve düzeltme hattı.
Adım 1: Deterministik normalizasyon + ders notu kataloğu + iş birimi (batch) üretimi.
"""
import json, os, re, glob, sys, hashlib, unicodedata
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8')

BASE = ((__import__('os').environ.get('MEDS_DATABASE_DIR') or __import__('os').path.expanduser('~/meds_database')))
RS = os.path.join(BASE, "redakte_sorular")
RZ = os.path.join(BASE, "redakte_ozet")
WORK = (__import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__))) + "/.meds_ds/work")
os.makedirs(WORK, exist_ok=True)

# ----------------------------------------------------------------------------
# MÜFREDAT HARİTASI (database_json/*/committee.json dosyalarından türetildi)
# ----------------------------------------------------------------------------
COMMITTEE = {}
for cj in glob.glob(os.path.join(BASE, "database_json", "*", "committee.json")):
    c = json.load(open(cj, encoding='utf-8'))
    COMMITTEE[c['committeeId']] = c

EXAM_SETS = {
    "donem3-kurul1": (1, "TIP 310 Ürogenital ve Obstetrik Kurulu"),
    "donem3-kurul2": (2, "TIP 320 Nöropsikiyatri Kurulu"),
    "donem3-kurul3": (3, "TIP 330 Gastrointestinal Sistem Kurulu"),
    "donem3-kurul4": (4, "TIP 340 Dolaşım, Solunum ve Tümör Kurulu"),
    "donem3-kurul5": (5, "TIP 350 Endokrin, Kas-İskelet ve Cilt Kurulu"),
    "donem3-kurul6": (6, "TIP 360 Hematoloji ve Onkoloji Kurulu"),
    "donem3-final": ("final", "TIP 300 Yıl Sonu Genel Final Sınavı"),
    "donem3-butunleme": ("butunleme", "TIP 300 Yıl Sonu Bütünleme Sınavı"),
}

# ----------------------------------------------------------------------------
# 1) METİN TEMİZLEME YARDIMCILARI
# ----------------------------------------------------------------------------
HTML_ENTITIES = {
    '&apos;': "'", '&#39;': "'", '&quot;': '"', '&#34;': '"', '&amp;': '&',
    '&lt;': '<', '&gt;': '>', '&nbsp;': ' ', '&hellip;': '…', '&ndash;': '–',
    '&mdash;': '—', '&rsquo;': "'", '&lsquo;': "'", '&ldquo;': '"', '&rdquo;': '"',
    '&deg;': '°', '&plusmn;': '±', '&micro;': 'µ', '&sup2;': '²', '&sup3;': '³',
    '&frac12;': '½', '&times;': '×', '&divide;': '÷', '&ge;': '≥', '&le;': '≤',
    '&alpha;': 'α', '&beta;': 'β', '&gamma;': 'γ', '&Delta;': 'Δ',
}

def decode_entities(s: str) -> str:
    if not s:
        return ""
    # ondalık / onaltılık sayısal entity'ler
    s = re.sub(r'&#x([0-9A-Fa-f]+);', lambda m: chr(int(m.group(1), 16)), s)
    s = re.sub(r'&#(\d+);', lambda m: chr(int(m.group(1))), s)
    for k, v in HTML_ENTITIES.items():
        s = s.replace(k, v)
    return s

# UTF-8'in Latin-1/CP1252 olarak yanlış çözülmesinden doğan bozukluklar
MOJIBAKE_MAP = {
    'Ã¼': 'ü', 'Ã¶': 'ö', 'Ã§': 'ç', 'Ã±': 'ñ', 'Ã¢': 'â', 'Ã®': 'î', 'Ã´': 'ô',
    'Ã¤': 'ä', 'Ã«': 'ë', 'Ã¯': 'ï', 'Ã–': 'Ö', 'Ãœ': 'Ü', 'Ã‡': 'Ç', 'Ã‰': 'É',
    'Ä±': 'ı', 'Ä°': 'İ', 'ÄŸ': 'ğ', 'Äž': 'Ğ', 'ÅŸ': 'ş', 'Åž': 'Ş',
    'Å“': 'œ', 'â€“': '–', 'â€”': '—', 'â€™': "'", 'â€œ': '"', 'â€\x9d': '"',
    'â€': '"', 'Â°': '°', 'Â±': '±', 'Âµ': 'µ', 'Â²': '²', 'Â³': '³',
    'Â½': '½', 'Â': '', 'â‚': '₺', 'Å¸': 'ş',
    'Ã¾': 'þ', 'Ã°': 'ð',
    'Å¸': 'ş', 'ÅŸ': 'ş', 'Åž': 'Ş', 'Å¡': 'š', 'Å¾': 'ž',
}
# uzun anahtarlar önce uygulanmalı
MOJIBAKE_KEYS = sorted(MOJIBAKE_MAP, key=len, reverse=True)

def _fix_orphan_a(s: str) -> str:
    """'Åş' -> 'ş', 'A±' -> 'ı' gibi tek başına kalmış bozuk kalıntılar."""
    s = s.replace('Å\u015f', 'ş').replace('Å\u015e', 'Ş')
    s = re.sub(r'(?<![A-Za-zÇĞİÖŞÜçğıöşü])A±', 'ı', s)
    s = re.sub(r'(?<![A-Za-zÇĞİÖŞÜçğıöşü])A°', 'İ', s)
    return s

def fix_mojibake(s: str) -> str:
    if not s:
        return ""
    for k in MOJIBAKE_KEYS:
        s = s.replace(k, MOJIBAKE_MAP[k])
    s = _fix_orphan_a(s)
    # kalan tek tük bozukluklar: cp1252/latin-1 çift kodlama denemesi
    if re.search(r'[ÃÄÅÂ][\x80-\xbf]', s):
        try:
            s = s.encode('latin-1', errors='strict').decode('utf-8', errors='strict')
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass
    return s

TURKISH_UPPER = {'i': 'İ', 'ı': 'I'}
def tr_title(s: str) -> str:
    return s

def normalize_ws(s: str) -> str:
    if not s:
        return ""
    s = s.replace('\u00ad', '').replace('\ufeff', '').replace('\x00', '')
    s = s.replace('\r\n', '\n').replace('\r', '\n')
    s = re.sub(r'[ \t]+', ' ', s)
    s = re.sub(r' *\n *', '\n', s)
    s = re.sub(r'\n{3,}', '\n\n', s)
    return s.strip()

TURKISH_LETTERS = set('ğüşıöçĞÜŞİÖÇâîûÂÎÛ')

def clean_text(s: str, keep_newlines=False) -> str:
    """Tam temizlik: entity + mojibake + whitespace + kontrol karakterleri."""
    if not s:
        return ""
    s = decode_entities(s)
    s = fix_mojibake(s)
    s = unicodedata.normalize('NFC', s)
    s = ''.join(ch for ch in s if ch == '\n' or ch == '\t' or unicodedata.category(ch)[0] != 'C')
    s = normalize_ws(s)
    if not keep_newlines:
        s = re.sub(r'\s*\n\s*', ' ', s)
    s = re.sub(r'\s{2,}', ' ', s)
    return s.strip()

# ----------------------------------------------------------------------------
# 2) hamSoru GÜRÜLTÜ TEMİZLEME (OCR/site artefaktları)
# ----------------------------------------------------------------------------
NOISE_PATTERNS = [
    r'\s*Enfeksiyon Hastalıkları\s*·\s*Dönem 3\s*[–-]\s*Kurul\s*\d+\s*·\s*\d+\s*/\s*\d+\s*$',
    r'\s*[A-ZÇĞİÖŞÜa-zçğıöşü ]+\s*·\s*Dönem 3\s*[–-]\s*Kurul\s*\d+\s*·\s*\d+\s*/\s*\d+\s*$',
    r'\s*\d{2}/\d{2}/\d{4}\s+sinav\.karabuk\.edu\.tr.*$',
    r'\s*https?://\S+.*$',
    r'\s*Sıra No\s+Cevap\s+.*$',
    r'\s*Sıra No\s+Ders\s*/\s*Ünite\s*/\s*Konu.*$',
    r'\s*\[D3 [^\]]*\]\s*',
    r'\s*\[25-26 dosyası\]\s*',
    r'\s*Not:\s*Aynı soru[^\n]*$',
    r'\s*\(Cevap anahtarı:\s*[A-E]\)\s*$',
    r'\s*\(Doğru cevap:\s*\d+\)\s*$',
    r'\s*Doğru cevap:\s*[A-E]\.?\s*$',
    r'\s*Cevap:\s*[A-E]\.?\s*$',
]
EMBED_SOURCE_RE = re.compile(r'\[([A-Za-zÇĞİÖŞÜçğıöşü0-9 _\-\.]+?)\]\s*(?=[A-ZÇĞİÖŞÜ])')

def strip_ham_noise(s: str) -> str:
    if not s:
        return ""
    t = decode_entities(s)
    t = fix_mojibake(t)
    t = t.replace('\n', ' ')
    for p in NOISE_PATTERNS:
        t = re.sub(p, ' ', t, flags=re.MULTILINE)
    t = re.sub(r'\s{2,}', ' ', t)
    t = re.sub(r'^\s*\d{1,3}\s*[\.\)\-]\s*', '', t)          # baştaki soru numarası
    t = re.sub(r'\s*\d+\s*/\s*\d+\s*$', '', t)                # "13/43"
    return t.strip(' -–—·|')

# ----------------------------------------------------------------------------
# 3) DERS NOTU KATALOĞU
# ----------------------------------------------------------------------------
def build_lecture_catalog():
    manifest = json.load(open(os.path.join(BASE, "redakte_ozet_manifest.json"), encoding='utf-8'))
    cat = []
    for key, m in manifest.items():
        p = m.get('output_path')
        if not p or not os.path.exists(p):
            continue
        txt = open(p, encoding='utf-8', errors='replace').read()
        title = clean_text(m.get('title') or os.path.basename(p))
        disc = clean_text(m.get('discipline') or '')
        # ilk anlamlı paragraftan kısa konu imzası
        body = re.sub(r'^.*?Öğrenci / Çalışma Grubu:.*?$', '', txt, count=1, flags=re.M | re.S)
        # başlıkları çıkar: konu imzası olarak kullan
        heads = [clean_text(h) for h in re.findall(r'^##\s+(?!#)(.+)$', txt, flags=re.M)]
        heads = [h for h in heads if h and not h.startswith(('⚡', '🎯', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.'))][:14]
        if not heads:
            heads = [clean_text(h) for h in re.findall(r'^###\s+(?!#)(.+)$', txt, flags=re.M)][:14]
        cat.append({
            "lectureId": "lec-" + hashlib.md5(p.encode('utf-8')).hexdigest()[:10],
            "kurul": m.get('kurul'),
            "discipline": disc,
            "title": title,
            "path": p,
            "chars": len(txt),
            "headings": heads,
            "text": txt,
        })
    return cat

# ----------------------------------------------------------------------------
# 4) SORU YÜKLEME + DEDUP + DETERMİNİSTİK NORMALİZASYON
# ----------------------------------------------------------------------------
def load_questions():
    qs = {}
    dupes = []
    for f in sorted(glob.glob(os.path.join(RS, "*.json"))):
        b = os.path.basename(f)
        if "raporu" in b or "tum_redakte" in b:
            continue
        try:
            d = json.load(open(f, encoding='utf-8'))
        except Exception as e:
            print("LOAD-ERR", b, e)
            continue
        if not isinstance(d, list):
            continue
        for q in d:
            if q.get('id') in qs:
                dupes.append((q.get('id'), b))
                continue
            q['_src'] = b
            qs[q['id']] = q
    return qs, dupes

def normalize_question(q):
    doc = dict(q)
    doc['discipline'] = clean_text(q.get('discipline') or '')
    doc['topic'] = clean_text(q.get('topic') or '')
    doc['stem'] = clean_text(q.get('stem') or '')
    doc['explanation'] = clean_text(q.get('explanation') or '')
    doc['hamSoru'] = strip_ham_noise(q.get('hamSoru') or '')
    doc['sourceFile'] = clean_text(q.get('sourceFile') or '')
    doc['examYear'] = clean_text(q.get('examYear') or '')
    opts = []
    for o in (q.get('options') or []):
        if not isinstance(o, dict):
            continue
        opts.append({
            "key": (o.get('key') or '').strip().upper()[:1],
            "text": clean_text(o.get('text') or ''),
            "isCorrect": bool(o.get('isCorrect')),
        })
    # eksik şık anahtarlarını sırayla tamamla
    for i, o in enumerate(opts):
        if not o['key']:
            o['key'] = "ABCDE"[i] if i < 5 else str(i + 1)
    doc['options'] = opts
    return doc

def audit(doc):
    """Deterministik kalite bayrakları."""
    flags = []
    opts = doc['options']
    if not doc['stem']:
        flags.append('bos_kok')
    if len(doc['stem']) < 25:
        flags.append('cok_kisa_kok')
    if len(opts) != 5:
        flags.append(f'sik_sayisi_{len(opts)}')
    if any(not o['text'] for o in opts):
        flags.append('bos_sik')
    ncorrect = sum(1 for o in opts if o['isCorrect'])
    if ncorrect == 0:
        flags.append('dogru_sik_yok')
    elif ncorrect > 1:
        flags.append('coklu_dogru_sik')
    ca = (doc.get('correctAnswer') or '').strip().upper()[:1]
    keys = [o['key'] for o in opts]
    if ca not in keys:
        flags.append('cevap_anahtari_uyumsuz')
    else:
        marked = [o['key'] for o in opts if o['isCorrect']]
        if marked and marked != [ca]:
            flags.append('isaretli_cevap_celiskisi')
    if not doc['explanation']:
        flags.append('aciklama_yok')
    elif len(doc['explanation']) < 60:
        flags.append('aciklama_cok_kisa')
    if not doc['topic']:
        flags.append('konu_yok')
    if doc['discipline'] not in (COMMITTEE.get(doc['committeeId'], {}).get('disciplines') or []):
        flags.append('mufredat_disiplin_uyumsuz')
    # şık metinleri arasında neredeyse tekrar
    seen = Counter(re.sub(r'\W+', '', o['text'].lower()) for o in opts if o['text'])
    if any(v > 1 for v in seen.values()):
        flags.append('tekrarli_sik')
    return flags

def main():
    print("### DERS NOTU KATALOĞU ###")
    cat = build_lecture_catalog()
    print("ders notu:", len(cat), "toplam karakter:", sum(c['chars'] for c in cat))
    json.dump([{k: v for k, v in c.items() if k != 'text'} for c in cat],
              open(os.path.join(WORK, "lecture_catalog.json"), "w", encoding='utf-8'),
              ensure_ascii=False, indent=1)

    print("\n### SORULAR ###")
    qs, dupes = load_questions()
    print("unique soru:", len(qs), "| atlanan tekrar id:", len(dupes))
    docs = [normalize_question(q) for q in qs.values()]
    for d in docs:
        d['qualityFlags'] = audit(d)
    json.dump(docs, open(os.path.join(WORK, "questions_normalized.json"), "w", encoding='utf-8'),
              ensure_ascii=False, indent=1)

    print("\n### KALİTE BAYRAKLARI ###")
    c = Counter(f for d in docs for f in d['qualityFlags'])
    for k, v in c.most_common():
        print(f"  {k}: {v}")
    print("temiz soru (bayraksız):", sum(1 for d in docs if not d['qualityFlags']))

    print("\n### EXAM SET x DISCIPLINE DAĞILIMI ###")
    grid = defaultdict(Counter)
    for d in docs:
        grid[d['committeeId']][d['discipline']] += 1
    for cid in sorted(grid, key=lambda x: str(EXAM_SETS.get(x, ('', ''))[0])):
        print(f"\n-- {cid} ({sum(grid[cid].values())} soru)")
        for disc, n in grid[cid].most_common():
            print(f"     {n:4}  {disc}")

    # mojibake kontrolü
    left = [d['id'] for d in docs if re.search(r'[ÃÄÅÂ]', d['stem'] + d['explanation'] + d['topic'])]
    print("\nkalan mojibake şüphesi:", len(left), left[:5])
    for x in left[:6]:
        d = [y for y in docs if y['id'] == x][0]
        for f in ('stem', 'topic', 'explanation', 'discipline'):
            if re.search(r'[ÃÄÅÂ]', d[f] or ''):
                m = re.search(r'.{45}[ÃÄÅÂ].{45}', d[f], re.S)
                print(f"  {x} [{f}]: {m.group(0) if m else d[f][:120]!r}")

if __name__ == "__main__":
    main()
