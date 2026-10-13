"""Öğren desteleri → Drive'daki ders PDF'leri ve slayt → (PDF, sayfa) eşlemesi; İÇERİKLE DOĞRULANMIŞ.

Çıktı: `src/data/deckPdfSources.json` (varsayılan) ya da `--cikti` (Oracle'da ders işçisi
`$MEDS_DOWNLOADS_DIR/_deck_pdf_sources.json` yazar; sunucu ikisinden yenisini kullanır).

Kural: doğru ders ↔ doğru PDF; şüpheli eşleşme gösterilmez.
  1. Drive kökündeki (drive_root) her ders PDF'inin her sayfası okunur (PyMuPDF). Her slaytın metni tüm sayfalarla
     TF-IDF kosinüsüyle karşılaştırılır (ters dizin; numpy gerekmez).
  2. Ad adayları (OVERRIDES → ders işçisi checklist'i → eski katalog → slayt `sourcePdf`) yalnız İÇERİK DESTEĞİ varsa
     kabul edilir: adayın kapsadığı slayt sayısı, en iyi PDF'inkinin en az yarısı olmalı. Yoksa içerik kazanır
     (raporda "ÇELİŞKİ").
  3. Ad adayı yoksa: en iyi PDF slaytların ≥%30'unu kapsamalı ve ikinciden ≥1,5 kat önde olmalı; değilse deste
     PDF'siz kalır (raporda "KANIT YOK" + ders programındaki tarih).
  4. Dersin ≥%12'sini (en az 3 slayt) kapsayan başka PDF'ler ek dosya olur (bir PDF birden çok ders, bir ders birden
     çok PDF içerebilir: ör. "26)Mesane…" = Mesane + CYBE patolojisi).
  5. Slayt → (dosya, sayfa aralığı): her adım önce en benzer dosyaya atanır; dosya başına sayfalar sıra korumalı
     bölütlenir (her içerik adımı ardışık bir bölüm; adım atlanabilir, hiçbir adıma benzemeyen sayfalar boşluk olur,
     metinsiz şekil sayfaları bölümüne katılır). Özet/tekrar/oyun/çıkmış adımları tüm PDF'i gösterir.

Çalıştırma:  .venv-ocr/bin/python scripts/build_deck_pdf_sources.py [--cikti yol] [--rapor yol] [--sessiz]
Çıkış kodu: 0 = tüm eşleşmeler doğrulandı; 3 = raporda ÇELİŞKİ var (çıktı yine yazılır, içerik kazanır);
2 = PDF'lerin hepsi okunamadı (çıktı YAZILMAZ).
"""
import argparse, datetime, json, math, os, re, sys, unicodedata
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.normpath(os.path.join(HERE, '..'))
ROOT = os.path.normpath(os.path.join(APP, '..'))
DECKS = os.path.join(APP, 'src', 'data', 'interactive_learning_decks.json')
LEGACY = os.path.join(APP, 'src', 'data', 'deckPdfCatalog.ts')
OUT = os.path.join(APP, 'src', 'data', 'deckPdfSources.json')
# Denetimde elle doğrulanmış adım aralıkları: {deste: {slideNumber: {"r": [baş, son, dosya], "t": başlık}}}.
# Yalnız adım başlığı hâlâ aynıysa ve dosya sayısı yetiyorsa uygulanır (deste değişince kendiliğinden düşer).
FIXES = os.path.join(HERE, 'deck_pdf_slide_duzeltme.json')
DL = os.environ.get('MEDS_DOWNLOADS_DIR') or os.path.join(ROOT, 'meds_downloads')
DRIVE = os.path.join(DL, 'drive_root')
ISCI = os.environ.get('MEDS_ISCI_DIR') or os.path.join(ROOT, 'ders_isci')
CHECKLIST = os.path.join(ISCI, 'checklist.json')

# Elle doğrulanmış adlar (drive_root'a göre yol). Bunlar da içerik denetiminden geçer.
OVERRIDES = {
    'k1p-k1-23-ana-cocuk-sagligi-duzeyinin-izlenmesi': ['Kurul 1/Halk Sağlığı/2)Ana çocuk sağ.izleme .pdf'],
    'k1p-k1-31-urogenital-sistem-tumorlerinde-genetik-belirtecler': ["Kurul 1/Tıbbi Genetik/4)'ÜROGENİTAL SİSTEM TÜMÖRLERİNDE GENETİK BELİRTEÇLER.'.pdf"],
    'k1p-k1-37-glomeruler-hastaliklar-nefrotik-sendrom': ['Kurul 1/Tıbbi Patoloji/21)Glomerüler Hastalıklar_ Nefrotik Sendrom.pdf'],
    'k1p-k1-38-glomeruler-hastaliklar-nefritik-sendrom': ['Kurul 1/Tıbbi Patoloji/22)Glomeruler Hastalıklar_ Nefritik Sendrom.pdf'],
    'k1p-k1-40-cinsel-yolla-bulasan-hastaliklarda-profilaksi-ve-korunma': ["Kurul 1/Enfeksiyon Hastalıkları/6)'Cinsel yolla bulaşan enfeksiyonlarda profilaksi ve korunma' .pdf"],
    'k1p-k1-46-mesane-hastaliklari-ve-tumorleri': ['Kurul 1/Tıbbi Patoloji/26)Mesane Hastalıkları ve Tümörleri.pdf'],
    'k1p-k1-50-sifilis': ['Kurul 1/Enfeksiyon Hastalıkları/7)Sifiliz .pdf'],
    'k1p-k1-53-endometriyal-hiperplazi-ve-kanserleri': ['Kurul 1/Tıbbi Patoloji/30)Endometrial Hiperplazi ve Kanserleri.pdf'],
    'k1p-k1-56-memenin-benign-hastaliklari': ['Kurul 1/Tıbbi Patoloji/33) Memenin Benign Hastalıkları.pdf'],
    'k1p-k1-58-enurezis-nokturna': ['Kurul 1/Üroloji/6)Enürezis.pdf'],
    'k1p-k1-61-abortus': ['Kurul 1/Kadın Hastalıkları ve Doğum/1)Abortus_2026.pdf'],
    'k1p-k1-62-uretral-akinti': ['Kurul 1/Enfeksiyon Hastalıkları/8)ÜRETRAL AKINTI.pdf'],
    'k1p-k1-67-gebelik-hastaliklari': ['Kurul 1/Tıbbi Patoloji/32)Gebelik Hastalıkları .pdf'],
    'learn-glomeruler-hastaliklar-nefritik': ['Kurul 1/Tıbbi Patoloji/22)Glomeruler Hastalıklar_ Nefritik Sendrom.pdf'],
    'learn-enfeksiyon-epidemiyoloji': ['Kurul 1/Halk Sağlığı/5)Enfeksiyon Hastalıklarının Genel Epidemiyolojik Özellikleri.pdf'],
    'learn-uriner-sistem-enfeksiyonlari-epidemiyoloji': ["Kurul 1/Üroloji/4)'Üriner Sistem Enfeksiyonlarının Epidemiyoloji, Etyoloji ve Semptomatolojisi'.pdf"],
}
# Ders içeriği değil, program belgesi: içerik denetimi uygulanmaz.
NO_CONTENT_CHECK = {'learn-donem3-kurul1-mufredat-rehberi': ['Ders Programı/2026-27 D3 ders programı.pdf']}

STRONG = 0.20          # slayt ↔ sayfa benzerliği bu eşiği geçerse "kapsıyor"
NAME_SUPPORT = 0.5     # ad adayı en iyi PDF'in kapsamının en az bu oranını kapsamalı
SOLO_SHARE = 0.30      # ad adayı yoksa: en iyi PDF slaytların en az bu oranını kapsamalı
SOLO_LEAD = 1.5        # ... ve ikinciden bu kat önde olmalı
EXTRA_SHARE = 0.12     # ek PDF eşiği (en az 3 slayt)
MAX_FILES = 3

STOP = {'ve', 'ile', 'icin', 'bir', 'olan', 'ders', 'yeni', 'mikro', 'tip', 'pdf', 'genel', 'kurul', 'notu', 'slayt',
        'sayfa', 'bolum', 'tekrar', 'checkpoint', 'ozet', 'olarak', 'veya', 'daha', 'gibi', 'kadar', 'sonra', 'once'}


def nfc(s):
    return unicodedata.normalize('NFC', str(s or ''))


def fold(s):
    s = nfc(s).replace('İ', 'i').replace('I', 'ı').lower().replace('ı', 'i')
    s = unicodedata.normalize('NFKD', s)
    return ''.join(ch for ch in s if not unicodedata.combining(ch))


def name_key(name):
    b = fold(os.path.basename(name))
    b = re.sub(r'\.pdf$', '', b)
    b = re.sub(r'^\s*\d+\s*\)\s*', '', b)
    b = re.sub(r'_?20\d\d$', '', b)
    return re.sub(r'[^a-z0-9]+', '', b)


def toks(s):
    return [w[:7] for w in re.findall(r'[a-z0-9]+', fold(s)) if len(w) >= 4 and w not in STOP and not w.isdigit()]


def slide_text(s):
    parts = [s.get('title', '')] * 3 + [s.get('subtitle', '')] * 2
    for k in ('coreContent', 'synthesisNarrative', 'content'):
        v = s.get(k)
        if isinstance(v, str):
            parts.append(v[:1500])
    for t in s.get('medicalTerms') or []:
        if isinstance(t, dict):
            parts.append(t.get('term', ''))
    return ' '.join(parts)


# ---------------------------------------------------------------- envanter ve PDF metni
def load_inventory(extra):
    """drive_root'a göre NFC göreli yol → {fileId, local}. Diskteki ad NFD olabilir."""
    inv = {}
    if os.path.isdir(DRIVE):
        for dp, _, fs in os.walk(DRIVE):
            for f in fs:
                if f.lower().endswith('.pdf'):
                    full = os.path.join(dp, f)
                    inv[nfc(os.path.relpath(full, DRIVE))] = {'fileId': None, 'local': full}
    for src in [os.path.join(DL, '_downloads.json')] + list(extra):
        if not os.path.exists(src):
            continue
        for fid, v in json.load(open(src)).items():
            p = nfc(v.get('path', ''))
            if v.get('status') != 'done' or not p.startswith('drive_root/') or not p.lower().endswith('.pdf'):
                continue
            e = inv.setdefault(p[len('drive_root/'):], {'fileId': None, 'local': None})
            e['fileId'] = e['fileId'] or fid
    return inv


def page_texts(path):
    try:
        import pymupdf
    except ImportError:
        import fitz as pymupdf
    with pymupdf.open(path) as doc:
        return [pg.get_text('text') for pg in doc]


class Corpus:
    """Tüm ders PDF sayfaları için TF-IDF + ters dizin."""

    def __init__(self, files):  # files: {rel: [sayfa metni]}
        self.files = list(files)
        self.pages = []  # (dosya_idx, sayfa_idx)
        self.page_len = []
        counts = []
        for fi, rel in enumerate(self.files):
            for pi, t in enumerate(files[rel]):
                self.pages.append((fi, pi))
                counts.append(Counter(toks(t)))
                self.page_len.append(sum(counts[-1].values()))
        n = len(counts)
        df = Counter(w for c in counts for w in c)
        self.idf = {w: math.log(n / d) for w, d in df.items()}
        self.inv = defaultdict(list)
        for k, c in enumerate(counts):
            for w, x in self._vec(c).items():
                self.inv[w].append((k, x))
        self.n_pages = {rel: len(files[rel]) for rel in self.files}

    def _vec(self, c):
        v = {w: (1 + math.log(f)) * self.idf[w] for w, f in c.items() if w in self.idf}
        n = math.sqrt(sum(x * x for x in v.values())) or 1
        return {w: x / n for w, x in v.items()}

    def score(self, text):
        """sayfa_kimliği → benzerlik (yalnız sıfırdan büyükler)."""
        sc = defaultdict(float)
        for w, x in self._vec(Counter(toks(text))).items():
            for k, y in self.inv.get(w, ()):
                sc[k] += x * y
        return sc


# ---------------------------------------------------------------- ad adayları
def load_legacy():
    if not os.path.exists(LEGACY):
        return {}
    t = open(LEGACY, encoding='utf-8').read()
    m = re.search(r'=\s*(\{.*\});\s*\n\s*export function', t, re.S)
    return json.loads(m.group(1)) if m else {}


def load_checklist():
    out, dates = {}, {}
    if os.path.exists(CHECKLIST):
        for k in json.load(open(CHECKLIST)).get('konular', []):
            did = k.get('deste_id')
            if did:
                out.setdefault(did, []).extend(nfc(p['pdf']) for p in (k.get('pdf_2627') or []) if p.get('pdf'))
                dates[did] = {'tarih': k.get('tarih')}
    return out, dates


def resolve_name(name, inv, by_key):
    name = nfc(name)
    if name in inv:
        return name
    hits = by_key.get(name_key(name)) or []
    # Tam dosya adı tutan önce (ör. "5)Üriner Sistem Enfeksiyonlari.pdf" ≠ Üroloji'deki "3)Üriner Sistem Enfeksiyonları.pdf")
    tam = [h for h in hits if os.path.basename(h) == os.path.basename(name)]
    return sorted(tam or hits, key=len)[0] if hits else None


def name_candidates(deck, inv, by_key, checklist, legacy):
    did, out = deck['id'], []

    def add(rel, src):
        if rel and rel not in [r for r, _ in out]:
            out.append((rel, src))

    for rel in OVERRIDES.get(did, []):
        add(resolve_name(rel, inv, by_key), 'elle')
    for rel in checklist.get(did, []):
        add(resolve_name(rel, inv, by_key), 'checklist')
    lg = legacy.get(did) or {}
    for n in (lg.get('localFileName'), lg.get('fileName')):
        if n:
            add(resolve_name(n, inv, by_key), 'eski_katalog')
    names = Counter(s['sourcePdf'].get('fileName') for s in deck.get('slides', [])
                    if isinstance(s.get('sourcePdf'), dict) and s['sourcePdf'].get('fileName'))
    for n, _ in names.most_common(2):
        add(resolve_name(n, inv, by_key), 'slayt_kaynagi')
    return out


# ---------------------------------------------------------------- hizalama
OVERVIEW_RE = re.compile(r'ozet|bilgi paketi|cikmis soru|tekrar sayfasi|checkpoint|oyun sayfasi|sinav spot')


def is_overview(s):
    """Tüm dersi özetleyen adımlar (PDF'te tek bölüme denk gelmez)."""
    return bool(s.get('isCheckpoint') or s.get('isGameFinale') or OVERVIEW_RE.search(fold(s.get('title', ''))))


def segment(rows, plen):
    """rows: içerik adımı × sayfa benzerliği; plen: sayfa başına sözcük sayısı.
    Sayfaları sırayla adımlara böler (her adım ardışık bir aralık; adım atlanabilir). Dönen: adım başına (ilk, son) sütun.
    Puan: sayfanın o adıma göreli benzerliği (sayfadaki en iyi adıma oranı; mutlak benzerlik düşükse indirimli).
    Hiçbir adıma benzemeyen sayfalar (başka ders, kaynakça) "boşluk" durumuna düşer; metinsiz sayfalar (şekil) bulunduğu
    bölüme katılır."""
    m, n = len(rows), len(rows[0])
    NEW, SKIP, GAP = 0.6, 0.8, 0.3
    z, gz = [], []
    for j in range(n):
        col = [rows[i][j] for i in range(m)]
        mx = max(col)
        if plen[j] < 15 or mx < 0.01:  # metinsiz: kimseye puan yok, bulunduğu yerde kalır
            z.append([0.0] * m)
            gz.append(0.0)
        else:
            w = min(1.0, mx / 0.15)
            z.append([c / mx * w for c in col])
            gz.append(GAP)
    NEG = -1e18
    # durumlar: 0..m-1 = adım i, m..2m-1 = adım i'den sonra boşluk; başta boşluk = adım -1 sonrası (sanal, i=-1)
    dp = [z[0][i] - SKIP * i for i in range(m)] + [NEG] * m
    pre = gz[0]  # ilk adımdan önceki boşluk
    backs = []
    for j in range(1, n):
        cur, bk = [NEG] * (2 * m), [0] * (2 * m)
        best_prev, arg_prev = pre - SKIP, -1  # i=0 için: baştaki boşluktan
        for i in range(m):
            if i > 0:
                c = max(dp[i - 1], dp[m + i - 1])
                a = i - 1 if dp[i - 1] >= dp[m + i - 1] else m + i - 1
                if c >= best_prev - SKIP:
                    best_prev, arg_prev = c, a
                else:
                    best_prev -= SKIP
            jump = best_prev - NEW + SKIP  # best_prev bir adım fazla cezalı tutuluyor
            stay = dp[i]
            if stay >= jump:
                cur[i], bk[i] = z[j][i] + stay, i
            else:
                cur[i], bk[i] = z[j][i] + jump, arg_prev
            g_stay, g_from = dp[m + i], dp[i]
            if g_stay >= g_from:
                cur[m + i], bk[m + i] = gz[j] + g_stay, m + i
            else:
                cur[m + i], bk[m + i] = gz[j] + g_from, i
        pre += gz[j]
        backs.append(bk)
        dp = cur
    st = max(range(2 * m), key=lambda k: dp[k] - SKIP * (m - 1 - (k % m)))
    owner = [st]
    for bk in reversed(backs):
        st = bk[st] if st >= 0 else -1  # -1: ilk adımdan önceki boşluk
        owner.append(st)
    owner.reverse()
    owner = [o if 0 <= o < m else None for o in owner]
    first, last = {}, {}
    for j, i in enumerate(owner):
        if i is None:
            continue
        first.setdefault(i, j)
        last[i] = j
    out = []
    for i in range(m):
        if i in first:
            out.append((first[i], last[i]))
        else:  # atlanan adım: komşu bölümler arasında en benzer sayfa
            lo = max([last[k] for k in last if k < i], default=0)
            hi = min([first[k] for k in first if k > i], default=n - 1)
            j = max(range(lo, hi + 1), key=lambda q: rows[i][q])
            out.append((j, j))
    return out


# ---------------------------------------------------------------- ana akış
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--envanter', action='append', default=[], help='ek _downloads.json')
    ap.add_argument('--cikti', default=OUT)
    ap.add_argument('--rapor', default=None, help='doğrulama raporu (md); varsayılan çıktının yanına')
    ap.add_argument('--sessiz', action='store_true')
    a = ap.parse_args()

    decks = json.load(open(DECKS))
    inv = load_inventory(a.envanter)
    by_key = defaultdict(list)
    for rel in inv:
        by_key[name_key(rel)].append(rel)
    checklist, dates = load_checklist()
    legacy = load_legacy()

    texts = {}
    for rel, e in sorted(inv.items()):
        if e.get('local') and not rel.startswith('Ders Program'):
            try:
                texts[rel] = page_texts(e['local'])
            except Exception as err:  # bozuk PDF
                print('  ! okunamadı:', rel, err, file=sys.stderr)
    # Koruma: okunamayan PDF varsa (PyMuPDF yok, bozuk dosya, yarım indirme) eksik eşleme YAZILMAZ; eski çıktı kalır.
    local = [rel for rel, e in inv.items() if e.get('local') and not rel.startswith('Ders Program')]
    if not texts or len(texts) < len(local):
        print(f'HATA: {len(local)} PDF\'ten {len(texts)} tanesi okunabildi; çıktı yazılmadı.', file=sys.stderr)
        return 2
    corpus = Corpus(texts)

    out, report, conflicts = {}, [], 0
    fixes = json.load(open(FIXES, encoding='utf-8')) if os.path.exists(FIXES) else {}
    n_fix = 0
    for deck in decks:
        did = deck['id']
        entry = {'title': deck.get('title', ''), 'files': []}
        if did in NO_CONTENT_CHECK:
            for rel in NO_CONTENT_CHECK[did]:
                r = resolve_name(rel, inv, by_key)
                if r:
                    f = {'path': r, 'name': os.path.basename(r)}
                    if inv[r].get('fileId'):
                        f['fileId'] = inv[r]['fileId']
                    entry['files'].append(f)
            entry['via'] = 'program_belgesi'
            out[did] = entry
            report.append((did, 'OK', 'program belgesi (içerik denetimi yok)', entry['files']))
            continue

        slides = deck.get('slides', [])
        body = [i for i, s in enumerate(slides) if not s.get('isCheckpoint')] or list(range(len(slides)))
        scores = [corpus.score(slide_text(s)) for s in slides]
        cover = Counter()
        for i in body:
            sc = scores[i]
            if sc:
                k = max(sc, key=sc.get)
                if sc[k] >= STRONG:
                    cover[corpus.files[corpus.pages[k][0]]] += 1
        n = len(body)
        ranked = cover.most_common()
        top_rel, top_c = ranked[0] if ranked else (None, 0)
        second_c = ranked[1][1] if len(ranked) > 1 else 0

        names = [(r, s) for r, s in name_candidates(deck, inv, by_key, checklist, legacy) if r]
        supported = [(r, s) for r, s in names if cover.get(r, 0) >= max(2, NAME_SUPPORT * top_c)]
        primary, status = None, 'OK'
        if supported:
            primary, src = max(supported, key=lambda x: cover.get(x[0], 0))
            entry['via'] = src
            note = f'ad ({src}) + içerik: {cover.get(primary, 0)}/{n} slayt'
            if primary != supported[0][0]:
                note += f' (ilk ad adayı {os.path.basename(supported[0][0])} yerine içerikçe güçlü olan)'
        elif top_rel and top_c >= max(3, SOLO_SHARE * n) and (names or top_c >= SOLO_LEAD * second_c):
            primary = top_rel
            entry['via'] = 'icerik'
            if names:
                status = 'ÇELİŞKİ'
                note = (f'ad adayı içerikle desteklenmiyor ({os.path.basename(names[0][0])}: {cover.get(names[0][0], 0)}/{n}); '
                        f'içerik kazandı: {top_c}/{n}')
            else:
                note = f'yalnız içerik: {top_c}/{n} slayt (ikinci {second_c})'
        else:
            status = 'KANIT YOK'
            d = dates.get(did) or {}
            note = (f'en iyi aday {os.path.basename(top_rel) if top_rel else "—"} yalnız {top_c}/{n} slayt'
                    + (f'; ad adayı {os.path.basename(names[0][0])} {cover.get(names[0][0], 0)}/{n}' if names else '')
                    + (f'; ders tarihi {d["tarih"]}' if d.get('tarih') else ''))
            if d.get('tarih'):
                entry['missing'] = {'tarih': d['tarih']}
        if status == 'ÇELİŞKİ':
            conflicts += 1

        files = []
        if primary:
            files.append(primary)
            for rel, c in ranked:
                if len(files) >= MAX_FILES:
                    break
                if rel not in files and c >= max(3, EXTRA_SHARE * n):
                    files.append(rel)
        for rel in files:
            f = {'path': rel, 'name': os.path.basename(rel), 'pages': corpus.n_pages.get(rel)}
            if inv.get(rel, {}).get('fileId'):
                f['fileId'] = inv[rel]['fileId']
            entry['files'].append(f)

        # Slayt → (dosya, sayfa aralığı): seçilen dosyaların sayfaları birleştirilip sıra korumalı bölütlenir;
        # her içerik adımı PDF'te ardışık bir bölüme (başlangıç–bitiş) denk gelir. Özet/tekrar/oyun adımları tüm dersi gösterir.
        if files:
            fidx = {corpus.files.index(r): j for j, r in enumerate(files)}
            cols = [k for k, (fi, _) in enumerate(corpus.pages) if fi in fidx]
            content = [i for i in body if not is_overview(slides[i])] or body
            # Önce her adımın dosyası (en benzer sayfanın dosyası; ana dosyaya hafif öncelik), sonra dosya başına bölütleme:
            # ders sırası dosyalar arasında gidip gelebilir, tek dosya içinde ise PDF sırası korunur.
            fcols = {j: [k for k in cols if fidx[corpus.pages[k][0]] == j] for j in range(len(files))}
            own = {}
            for i in content:
                best = [max((scores[i].get(k, 0.0) for k in fcols[j]), default=0.0) * (1.1 if j == 0 else 1.0)
                        for j in range(len(files))]
                if max(best) >= 0.08:
                    j = max(range(len(files)), key=lambda j: best[j])
                    # ek dosyaya ancak açık üstünlükle geçilir (zayıf benzerlik dersi başka dosyaya sıçratmasın)
                    own[i] = j if j == 0 or (best[j] >= STRONG and best[j] >= 1.3 * best[0]) else 0
            last = next((own[i] for i in content if i in own), 0)
            for i in content:  # eşleşmeyen adım önceki adımın dosyasında kalır
                last = own.setdefault(i, last)
            res, hit = {}, 0
            for j, fc in fcols.items():
                mine = [i for i in content if own[i] == j]
                if not mine:
                    continue
                rows = [[scores[i].get(k, 0.0) for k in fc] for i in mine]
                for i, row, (s0, s1) in zip(mine, rows, segment(rows, [corpus.page_len[k] for k in fc])):
                    # Bölüm kenarındaki ilgisiz sayfalar (kapak, başka konu) atılır
                    top = max(row[s0:s1 + 1])
                    while s0 < s1 and row[s0] < 0.3 * top:
                        s0 += 1
                    while s1 > s0 and row[s1] < 0.3 * top and corpus.page_len[fc[s1]] >= 15:
                        s1 -= 1
                    edge = i in (mine[0], mine[-1])
                    if j or edge:  # ek dosyada ve dosyanın ilk/son bölümünde kapsam taşabilir: en benzer sayfanın çevresiyle sınırla
                        pk = max(range(s0, s1 + 1), key=lambda q: row[q])
                        ok = lambda q: row[q] >= 0.4 * top or corpus.page_len[fc[q]] < 15
                        a0 = a1 = pk
                        while a0 > s0 and ok(a0 - 1):
                            a0 -= 1
                        while a1 < s1 and ok(a1 + 1):
                            a1 += 1
                        s0, s1 = a0, a1
                    res[str(slides[i].get('slideNumber', i + 1))] = [s0 + 1, s1 + 1] + ([j] if j else [])
                    if max(row[s0:s1 + 1]) >= STRONG:
                        hit += 1
            for i, s in enumerate(slides):
                res.setdefault(str(s.get('slideNumber', i + 1)), [1, corpus.n_pages[files[0]]])
            for k, fx in (fixes.get(did) or {}).items():
                s = next((s for s in slides if str(s.get('slideNumber')) == k), None)
                r = fx.get('r') or []
                if s and s.get('title', '') == fx.get('t') and len(r) >= 2 and (r[2] if len(r) > 2 else 0) < len(files):
                    res[k] = [r[0], r[1]] + ([r[2]] if len(r) > 2 and r[2] else [])
                    n_fix += 1
            res = {k: res[k] for k in sorted(res, key=lambda x: int(x) if x.isdigit() else 0)}
            entry['slides'] = res
            entry['check'] = {'slides': n, 'covered': sum(cover.get(r, 0) for r in files), 'aligned': hit}
        out[did] = entry
        report.append((did, status, note, entry['files']))

    gen = datetime.datetime.now().isoformat(timespec='seconds')
    os.makedirs(os.path.dirname(os.path.abspath(a.cikti)), exist_ok=True)
    tmp = a.cikti + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh:
        json.dump({'generatedAt': gen, 'pdfCount': len(texts), 'decks': out}, fh, ensure_ascii=False, separators=(',', ':'))
    os.replace(tmp, a.cikti)

    rp = a.rapor or os.path.splitext(a.cikti)[0] + '_rapor.md'
    c = Counter(s for _, s, _, _ in report)
    lines = [f'# Deste → PDF eşleşme raporu ({gen})', '',
             f"Drive ders PDF'i: {len(texts)} · deste: {len(report)} · " + ' · '.join(f'{k}: {v}' for k, v in c.items()), '']
    for st in ('ÇELİŞKİ', 'KANIT YOK', 'OK'):
        rows = [r for r in report if r[1] == st]
        if rows:
            lines += [f'## {st} ({len(rows)})', '']
            lines += [f'- `{did}` — {" + ".join(f["name"] for f in files) or "PDF yok"} — {note}' for did, _, note, files in rows]
            lines.append('')
    with open(rp, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines))
    if not a.sessiz:
        print('\n'.join(lines[:3]))
        for did, st, note, files in report:
            if st != 'OK' or len(files) > 1:
                print(f'{st:9} {did[:50]:50} {" + ".join(f["name"][:26] for f in files) or "—"} | {note}')
        print('Yazıldı:', a.cikti, '·', rp, '· elle düzeltilmiş adım:', n_fix)
    # Öğren kitaplığının "Ders programı" sırası da aynı checklist'ten tazelenir
    try:
        import subprocess
        subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build_deck_schedule.py')], check=False)
    except Exception as e:  # sıralama dosyası eşleşmeyi bozmasın
        print('Ders programı sırası yazılamadı:', e)
    return 3 if conflicts else 0


if __name__ == '__main__':
    sys.exit(main())
