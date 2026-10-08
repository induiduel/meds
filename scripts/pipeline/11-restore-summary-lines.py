"""Ders özetlerinde tek cümleye yapıştırılmış slayt satırlarını kaynaktan geri kurar.

Özet üretilirken slayttaki satır sonları silinmiş; "Skrotal ağrı … ağrılı ejakülasyon ateş yüksekliği → torsiyon …
chlamidya trachomatis …" gibi ayrı bilgiler tek cümle olmuş. Bu betik her maddeyi temp2'deki (düzeltilmiş, ham kaynakla
teyitli) slayt metninde arar ve kaynakta yeni satırın başladığı yerlerden alt maddelere böler.
Metin değişmez: yalnızca satır/madde sınırı eklenir ve yeni satırın ilk harfi büyütülür. Kaynakta bulunamayan
madde olduğu gibi kalır.

PDF satır sarmalamaları (cümle ortasında alt satıra geçme) kesilmez: yeni satır küçük harfle başlıyorsa ya da
önceki satırda kapanmamış parantez varsa sarmalama sayılır.

Girdi : $MEDS_TEMP_DIR/temp2/**/*.md   (varsayılan: ../meds_temp)
Çıktı : data/lectureSummariesCatalog.json, src/data/lectureSummariesCatalog.json, src/data/summaries/kurul*.json
        (yalnızca `content` alanı). Yazmadan önce özgün dosyalar $MEDS_TEMP_DIR/ozet_satir_yedek/<zaman>/ altına kopyalanır.
Çalıştır: python3 scripts/pipeline/11-restore-summary-lines.py          # deneme: istatistik + örnek
          python3 scripts/pipeline/11-restore-summary-lines.py --yaz    # dosyalara yaz
"""
import argparse, bisect, glob, json, os, re, shutil, time
from collections import Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
TEMP_DIR = os.environ.get('MEDS_TEMP_DIR') or os.path.abspath(os.path.join(ROOT, '..', 'meds_temp'))
TARGETS = [os.path.join(ROOT, 'data', 'lectureSummariesCatalog.json'),
           os.path.join(ROOT, 'src', 'data', 'lectureSummariesCatalog.json')] + \
          sorted(glob.glob(os.path.join(ROOT, 'src', 'data', 'summaries', 'kurul*.json')))

TR = str.maketrans({'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u', 'â': 'a', 'î': 'i', 'û': 'u'})
MIN_MATCH = 20      # en kısa güvenilir eşleşme (katlanmış harf)
GRAM, STEP = 20, 10  # kaynak dosya seçimi için parça dizini
MIN_SEG = 4          # bundan kısa parça öncekine eklenir


def fold_map(s):
    """Türkçe katlanmış, yalnız harf/rakam metin + her harfin özgün konumu."""
    out, idx = [], []
    for i, ch in enumerate(s):
        c = 'i' if ch in 'İI' else ch.lower().translate(TR)
        for cc in c:
            if cc.isascii() and cc.isalnum():
                out.append(cc); idx.append(i)
    return ''.join(out), idx


def is_real_break(prev, cur):
    """Kaynakta `cur` satırı yeni bir bilgi mi, yoksa `prev`in PDF sarmalaması mı?"""
    if prev is None:
        return True
    if prev.count('(') > prev.count(')'):
        return False
    # Sayfa genişliğini dolduran, noktalamayla bitmeyen satır alt satıra sarmalanmıştır
    if len(prev) >= 80 and prev[-1] not in '.:;!?)':
        return False
    first = cur.lstrip()[:1]
    return bool(first) and not first.islower()


def load_sources():
    files = []
    for f in glob.glob(os.path.join(TEMP_DIR, 'temp2', '**', '*.md'), recursive=True):
        parts, starts, real = [], [], []
        pos, prev = 0, None
        for line in open(f, encoding='utf-8', errors='ignore'):
            line = line.strip()
            if not line:
                continue
            if line.startswith('## Sayfa'):
                prev = None  # sayfa başı her zaman yeni bilgi
                continue
            fl, _ = fold_map(line)
            if not fl:
                continue
            starts.append(pos); real.append(is_real_break(prev, line))
            parts.append(fl); pos += len(fl); prev = line
        if parts:
            files.append((''.join(parts), starts, real))
    gidx = {}
    for i, (big, _, _) in enumerate(files):
        for j in range(0, len(big) - GRAM, STEP):
            gidx.setdefault(big[j:j + GRAM], set()).add(i)
    return files, gidx


def pick_sources(files, gidx, texts, k=3):
    votes = Counter()
    for t in texts:
        fb, _ = fold_map(t)
        for j in range(len(fb) - GRAM):
            for fi in gidx.get(fb[j:j + GRAM], ()):
                votes[fi] += 1
    return [files[i] for i, _ in votes.most_common(k)]


def cut_after(text, idx, j):
    """Katlanmış j. harften önceki harfin hemen arkası; satır sonu noktalaması önceki satırda kalır."""
    p = idx[j - 1] + 1
    while p < len(text) and text[p] in ' .,;:)!?':
        p += 1
    return p


def cuts_for(text, sources):
    """Özgün metinde kesilecek konumlar (yeni bilginin başladığı karakter)."""
    fb, idx = fold_map(text)
    cuts, i = set(), 0
    while len(fb) - i >= MIN_MATCH:
        best, where = 0, None
        for src in sources:
            big = src[0]
            lo, hi = max(MIN_MATCH, best + 1), len(fb) - i
            while lo <= hi:
                mid = (lo + hi) // 2
                if big.find(fb[i:i + mid]) >= 0:
                    best, where = mid, src; lo = mid + 1
                else:
                    hi = mid - 1
        if best < MIN_MATCH:
            i += 1
            continue
        big, starts, real = where
        at = big.find(fb[i:i + best])
        k = bisect.bisect_right(starts, at)
        while k < len(starts) and starts[k] < at + best:
            off = starts[k] - at
            if off > 0 and real[k]:
                cuts.add(cut_after(text, idx, i + off))
            k += 1
        # Kaynakta ardışık olmayan iki parça yan yana getirilmiş: o da ayrı bilgi
        if i > 0:
            cuts.add(cut_after(text, idx, i))
        i += best
    return sorted(cuts)


def upper_first(s):
    if not s:
        return s
    if s[0] == 'i':
        return 'İ' + s[1:]
    if s[0] == 'ı':
        return 'I' + s[1:]
    return s[0].upper() + s[1:]


NUM_TAIL = re.compile(r'^(.*?)\s+(\(?\d{1,2}[.)])$')


def segments(text, cuts):
    segs, last = [], 0
    for c in cuts + [len(text)]:
        seg = text[last:c].strip()
        last = c
        if not seg:
            continue
        if segs and len(re.sub(r'\W', '', seg)) < MIN_SEG:
            segs[-1] += ' ' + seg
        else:
            segs.append(seg)
    # Tek başına kalmış "1." bir sonraki satırın numarasıdır
    k = 0
    while k < len(segs) - 1:
        if re.fullmatch(r'\(?\d{1,2}[.)]', segs[k]):
            segs[k + 1] = f'{segs[k]} {segs[k + 1]}'
            del segs[k]
        else:
            k += 1
    # "Temas izolasyonu 2." → numara bir sonraki satırın başına
    for k in range(len(segs) - 1):
        m = NUM_TAIL.match(segs[k])
        if m and m.group(1):
            segs[k] = m.group(1)
            segs[k + 1] = f'{m.group(2)} {segs[k + 1]}'
    return [upper_first(s) for s in segs]


HEADER = re.compile(r'^[A-ZÇĞİÖŞÜ][\wÇĞİÖŞÜçğıöşü-]*(?:\s+[A-ZÇĞİÖŞÜ][\wÇĞİÖŞÜçğıöşü-]*){0,5}$')


def restore(content, files, gidx, stats):
    lines = content.split('\n')
    bullets = [re.sub(r'^\s*[-*]\s+', '', l).replace('**', '') for l in lines if re.match(r'^\s*[-*]\s+', l)]
    sources = pick_sources(files, gidx, [b for b in bullets if len(b) >= 60])
    if not sources:
        return content
    out = []
    for n, line in enumerate(lines):
        m = re.match(r'^(\s*)([-*])\s+(.*)$', line)
        if not m:
            out.append(line); continue
        indent, body = m.group(1), m.group(3)
        bold = body.startswith('**') and body.rstrip().endswith('**')
        plain = body.replace('**', '').replace('i\u0307', 'i').strip()
        nxt = lines[n + 1] if n + 1 < len(lines) else ''
        has_children = not indent and bool(re.match(r'^\s{2,}[-*]\s+', nxt))
        # Alt maddeli başlık satırı ("**… kimlere uygulanır?:**") etiket olarak kalır
        if (has_children and bold) or len(plain) < 40:
            out.append(line); continue
        segs = segments(plain, cuts_for(plain, sources))
        if len(segs) < 2:
            out.append(line); continue
        stats['madde'] += 1; stats['yeni_satir'] += len(segs) - 1
        if indent:
            out.extend(f'{indent}- {s}' for s in segs)
            continue
        # Üst madde: slayt başlığı + ilk bilgi tek satır, kalanlar alt madde
        head = segs.pop(0)
        if HEADER.match(head.rstrip(':')) and segs and len(segs[0]) <= 60 and not re.match(r'^\(?\d', segs[0]):
            head = f'{head} {segs.pop(0)}'
        out.append(f'- **{head}**' if bold else f'- {head}')
        out.extend(f'  - {s}' for s in segs)
    return '\n'.join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--yaz', action='store_true', help='Dosyalara yaz (yoksa yalnızca deneme)')
    ap.add_argument('--ornek', default='sum-k1-cinsel_yolla_bula_an_hastal_klarda_tedavi_md', help='Denemede gösterilecek özet')
    args = ap.parse_args()

    files, gidx = load_sources()
    print(f'temp2 kaynak: {len(files)} dosya')
    base = json.load(open(TARGETS[1], encoding='utf-8'))
    stats = Counter()
    new_content = {}
    t0 = time.time()
    for s in base:
        c = s.get('content') or ''
        r = restore(c, files, gidx, stats)
        if r != c:
            new_content[s['id']] = (c, r)
    print(f'{len(new_content)} özet, {stats["madde"]} madde bölündü, {stats["yeni_satir"]} yeni satır ({time.time() - t0:.0f} sn)')

    if args.ornek in new_content:
        old, new = new_content[args.ornek]
        ol, nl = old.split('\n'), new.split('\n')
        shown = 0
        for l in nl:
            if l not in ol and shown < 40:
                print('  +', l[:160]); shown += 1

    if not args.yaz:
        print('Deneme: dosyalara yazılmadı (--yaz ile yaz).')
        return
    backup = os.path.join(TEMP_DIR, 'ozet_satir_yedek', time.strftime('%Y%m%d-%H%M%S'))
    os.makedirs(backup, exist_ok=True)
    for path in TARGETS:
        rel = os.path.relpath(path, ROOT)
        dst = os.path.join(backup, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(path, dst)
        raw = open(path, encoding='utf-8').read()
        data = json.loads(raw)
        # Dosyanın kendi biçimini koru (girintili mi tek satır mı)
        indent = 2 if raw[:200].count('\n') > 1 else None
        seps = (',', ':') if '":"' in raw[:300] else None
        changed = 0
        for s in data:
            pair = new_content.get(s.get('id'))
            # Yalnızca içerik hâlâ beklenen özgün metinse değiştir (başka düzenlemeleri ezme)
            if pair and s.get('content') == pair[0]:
                s['content'] = pair[1]; changed += 1
        tmp = path + '.tmp'
        with open(tmp, 'w', encoding='utf-8') as fh:
            json.dump(data, fh, ensure_ascii=False, indent=indent, separators=seps)
        os.replace(tmp, path)
        print(f'  {rel}: {changed} özet güncellendi')
    print(f'Yedek: {backup}')


if __name__ == '__main__':
    main()
