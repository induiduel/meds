"""Öğren destelerini docs/OGREN_ETKILESIM_REHBERI.md kurallarına göre denetler.

Kullanım:
    python3 scripts/validate_learning_decks.py                 # src/data/interactive_learning_decks.json
    python3 scripts/validate_learning_decks.py yeni_deste.json  # tek dosya (deste ya da deste listesi)
    python3 scripts/validate_learning_decks.py --ozet           # yalnız kural başına sayılar
    python3 scripts/validate_learning_decks.py --duzelt         # kesik zincir basamaklarını tamamla, sızdıran ipuçlarını sil (dosyaya yazar)

Çıkış kodu: HATA varsa 1, yalnız UYARI varsa 0. Yeni deste eklemeden önce HATA sayısı 0 olmalı.
"""
import json, os, re, sys, collections

ROOT = os.path.join(os.path.dirname(__file__), '..')
DEFAULT = os.path.join(ROOT, 'src', 'data', 'interactive_learning_decks.json')
TRUNC = re.compile(r'(\.\.\.|…)\s*$')
OPT_KEY = re.compile(r'^[A-E]$')
TYPES = {
    'micro_quiz', 'interactive_table', 'cloze_masking', 'causal_chain',
    'branching_logic', 'before_after_slider', 'active_recall',
    'spot_the_lie', 'swipe_matching', 'feature_bidding', 'venn_grid'
}

def fold(s):
    return str(s or '').lower().replace('ı', 'i').replace('İ', 'i')

def stems(s, n=5):
    return {w[:n] for w in re.findall(r'[\wçğıöşü%.,]+', fold(s)) if len(w) >= 3 or re.search(r'\d', w)}

def leaks(hint, answer):
    h = fold(hint)
    return any((w[:5] if len(w) > 5 else w) in h for w in re.findall(r'[\wçğıöşü%.,-]+', fold(answer)) if len(w) >= 3 or re.search(r'\d', w))

def check_deck(d, out):
    did = d.get('id') or '?'
    def add(level, code, slide, msg):
        out.append((level, code, did, slide, msg))
    if not d.get('id') or not re.fullmatch(r'[A-Za-z0-9_-]+', d['id']):
        add('HATA', 'deste-id', 0, 'id yalnız harf, rakam, - ve _ içermeli')
    for k in ('title', 'slides'):
        if not d.get(k):
            add('HATA', 'deste-alan', 0, f'"{k}" eksik')
    if not d.get('discipline'):
        add('UYARI', 'deste-disiplin', 0, '"discipline" eksik (bölüm üst bilgisinde boş görünür)')
    slides = d.get('slides') or []
    nums = [s.get('slideNumber') for s in slides]
    if nums != list(range(1, len(slides) + 1)):
        add('UYARI', 'slayt-sira', 0, 'slideNumber 1\'den başlayıp kesintisiz artmalı')
    for s in slides:
        n = s.get('slideNumber')
        if not s.get('title'):
            add('HATA', 'slayt-baslik', n, 'title eksik')
        if TRUNC.search(str(s.get('title', ''))) or TRUNC.search(str(s.get('subtitle', ''))):
            add('HATA', 'kesik-metin', n, 'başlık/alt başlık "…" ile kesilmiş')
        cc = s.get('coreContent') if isinstance(s.get('coreContent'), dict) else {}
        if not (s.get('synthesisNarrative') or s.get('content') or cc.get('keyBullets')):
            add('HATA', 'anlatim-yok', n, 'synthesisNarrative/content ya da keyBullets gerekli')
        if s.get('isCheckpoint') and not str(s.get('title', '')).startswith('[TEKRAR SAYFASI'):
            add('UYARI', 'tekrar-baslik', n, 'tekrar sayfası başlığı "[TEKRAR SAYFASI - CHECKPOINT n] Ad" biçiminde olmalı')
        for t in s.get('medicalTerms') or []:
            if not (t.get('term') and t.get('explanation')):
                add('HATA', 'terim', n, 'medicalTerms öğesinde term/explanation eksik')
        for c in s.get('flashcards') or []:
            if not ((c.get('front') or c.get('question')) and (c.get('back') or c.get('answer'))):
                add('HATA', 'kart', n, 'kartta front/back eksik')
        for q in (s.get('relatedQuestions') or []) + ([s['practiceQuestion']] if isinstance(s.get('practiceQuestion'), dict) else []):
            stem = q.get('stem') or q.get('question') or ''
            opts = q.get('options') or []
            if len(stem) < 10 or len(opts) < 2:
                add('HATA', 'soru', n, 'soru kökü ya da şıklar eksik')
                continue
            keys = [o.get('key') if isinstance(o, dict) else str(o)[:1] for o in opts]
            raw = q.get('correctAnswer') if q.get('correctAnswer') is not None else q.get('answer')
            ans = '' if raw is None else str(raw)
            flagged = [o for o in opts if isinstance(o, dict) and o.get('isCorrect')]
            letter = str(q.get('answer') or '') if OPT_KEY.match(str(q.get('answer') or '')) else ans
            if len(flagged) == 1 or (OPT_KEY.match(letter) and letter in keys):
                pass
            elif (ans.isdigit() and int(ans) < len(opts)) or re.match(r'^[A-E][).]\s', ans):
                add('UYARI', 'soru-cevap-eski', n, f'correctAnswer eski biçimde ({ans[:20]!r}); yeni içerikte yalnız harf (A-E) kullanın')
            else:
                add('HATA', 'soru-cevap', n, f'correctAnswer tek harf (A-E) olmalı; şu an: {ans!r}')
        for e in s.get('interactiveElements') or []:
            t = e.get('type')
            if t not in TYPES:
                add('HATA', 'tur', n, f'bilinmeyen etkileşim türü: {t}')
                continue
            if t == 'micro_quiz':
                opts = e.get('microQuizOptions') or []
                if not (e.get('question') or e.get('sentence')) or len(opts) < 2:
                    add('HATA', 'mini-soru', n, 'question ve en az 2 microQuizOptions gerekli')
                if sum(1 for o in opts if o.get('isCorrect')) != 1:
                    add('HATA', 'mini-soru-dogru', n, 'tam olarak bir şıkta isCorrect: true olmalı')
                if any(not o.get('explanation') for o in opts):
                    add('UYARI', 'mini-soru-aciklama', n, 'her şıkta explanation olmalı (öğrenci tüm şıkları açıp okuyabiliyor)')
            elif t == 'branching_logic':
                opts = e.get('options') or []
                if not e.get('scenario') or len(opts) < 2 or sum(1 for o in opts if o.get('isCorrect')) != 1:
                    add('HATA', 'klinik-karar', n, 'scenario, ≥2 options ve tek isCorrect gerekli')
                if any(not o.get('feedback') for o in opts):
                    add('UYARI', 'klinik-karar-geri', n, 'her seçenekte feedback olmalı')
            elif t == 'cloze_masking':
                sen, term = e.get('sentence', ''), e.get('maskedTerm', '')
                if not term or fold(term) not in fold(sen):
                    add('HATA', 'bosluk-yok', n, 'maskedTerm cümlede birebir geçmeli')
                if e.get('hint') and leaks(e['hint'], term):
                    add('HATA', 'ipucu-sizinti', n, f'ipucu cevabı ele veriyor: {e["hint"]!r}')
            elif t == 'interactive_table':
                hdr = e.get('tableHeaders') or []
                rows = e.get('tableRows') or []
                if not hdr or not rows:
                    add('HATA', 'gizli-tablo', n, 'tableHeaders ve tableRows gerekli')
                for r in rows:
                    cells = r.get('cells') if isinstance(r, dict) else r
                    if len(cells or []) != len(hdr):
                        add('HATA', 'gizli-tablo-sutun', n, 'her satırda başlık sayısı kadar hücre olmalı')
                    for c in cells or []:
                        if isinstance(c, dict) and c.get('isMasked') and c.get('hint') and leaks(c['hint'], c.get('text', '')):
                            add('HATA', 'ipucu-sizinti', n, f'gizli hücre ipucu cevabı ele veriyor: {c["hint"]!r} → {c.get("text")!r}')
                if not any(isinstance(c, dict) and c.get('isMasked') for r in rows for c in ((r.get('cells') if isinstance(r, dict) else r) or [])):
                    add('UYARI', 'gizli-tablo-bos', n, 'hiç gizli hücre yok')
            elif t == 'causal_chain':
                steps = e.get('steps') or []
                if len(steps) < 2:
                    add('HATA', 'zincir', n, 'en az 2 basamak gerekli')
                for st in steps:
                    if TRUNC.search(str(st)):
                        add('HATA', 'kesik-metin', n, f'zincir basamağı kesilmiş: {str(st)[:70]!r}')
            elif t == 'before_after_slider':
                if not (e.get('leftTitle') and e.get('rightTitle') and e.get('leftPoints') and e.get('rightPoints')):
                    add('HATA', 'karsilastir', n, 'leftTitle/rightTitle/leftPoints/rightPoints gerekli')
                elif len(e['leftPoints']) != len(e['rightPoints']):
                    add('UYARI', 'karsilastir-satir', n, 'sol ve sağ madde sayıları eşit olmalı (satırlar karşılıklı eşleşir)')
            elif t == 'active_recall':
                if not (e.get('question') and e.get('answer')):
                    add('HATA', 'aktif-hatirlama', n, 'question ve answer gerekli')
                if TRUNC.search(str(e.get('question', ''))):
                    add('HATA', 'kesik-metin', n, 'aktif hatırlama sorusu kesilmiş')
            elif t == 'spot_the_lie':
                items = e.get('items') or []
                if not (e.get('topic') or e.get('question')) or len(items) < 3:
                    add('HATA', 'tuzak-avi', n, 'topic/question ve en az 3 items gerekli')
                lies = [i for i in items if isinstance(i, dict) and (i.get('isLie') or i.get('isTrap'))]
                if len(lies) != 1:
                    add('HATA', 'tuzak-avi-tek', n, 'tam olarak bir önermede isLie: true olmalı')
                for it in items:
                    if not isinstance(it, dict) or not it.get('text'):
                        add('HATA', 'tuzak-avi-madde', n, 'her önermede text alanı zorunludur')
                    elif TRUNC.search(str(it.get('text', ''))):
                        add('HATA', 'kesik-metin', n, 'önerme metni kesilmiş')
                    if isinstance(it, dict) and not it.get('explanation'):
                        add('UYARI', 'tuzak-avi-aciklama', n, 'her önermede explanation olması önerilir')
            elif t == 'swipe_matching':
                left_c = e.get('leftCategory')
                right_c = e.get('rightCategory')
                cards = e.get('cards') or []
                if not left_c or not right_c or len(cards) < 2:
                    add('HATA', 'hizli-esleme', n, 'leftCategory, rightCategory ve en az 2 cards gerekli')
                for c in cards:
                    if not isinstance(c, dict) or not c.get('text') or not c.get('category'):
                        add('HATA', 'hizli-esleme-kart', n, 'her kartta text ve category (left/right) zorunludur')
                    elif TRUNC.search(str(c.get('text', ''))):
                        add('HATA', 'kesik-metin', n, 'kart metni kesilmiş')
            elif t == 'feature_bidding':
                optA = e.get('optionA')
                optB = e.get('optionB')
                rounds = e.get('rounds') if isinstance(e.get('rounds'), list) else []
                if not optA or not optB:
                    add('HATA', 'puan-bahsi-secenek', n, 'optionA ve optionB zorunludur')
                if not rounds and not e.get('feature'):
                    add('HATA', 'puan-bahsi-ozellik', n, 'en az bir rounds ögesi veya feature/correct alanı gerekli')
                all_rounds = rounds if rounds else [e]
                for r in all_rounds:
                    if not isinstance(r, dict) or not r.get('feature') or not r.get('correct'):
                        add('HATA', 'puan-bahsi-tur', n, 'her turda feature ve correct (A/B) zorunludur')
                    elif str(r.get('correct')).upper() not in ('A', 'B'):
                        add('HATA', 'puan-bahsi-cevap', n, 'correct alanı A ya da B olmalıdır')
                    elif TRUNC.search(str(r.get('feature', ''))):
                        add('HATA', 'kesik-metin', n, 'özellik metni kesilmiş')
            elif t == 'venn_grid':
                labA = e.get('labelA')
                labB = e.get('labelB')
                items = e.get('items') or []
                if not labA or not labB or len(items) < 2:
                    add('HATA', 'capraz-tablo', n, 'labelA, labelB ve en az 2 items gerekli')
                for it in items:
                    if not isinstance(it, dict) or not it.get('criterion') or not it.get('correct'):
                        add('HATA', 'capraz-tablo-madde', n, 'her kriterde criterion ve correct (A/B/both/neither) zorunludur')
                    elif str(it.get('correct')).lower() not in ('a', 'b', 'both', 'neither', 'both_a_b'):
                        add('HATA', 'capraz-tablo-cevap', n, 'correct değeri A, B, both veya neither olmalıdır')
                    elif TRUNC.search(str(it.get('criterion', ''))):
                        add('HATA', 'kesik-metin', n, 'kriter metni kesilmiş')


def candidates(s):
    cc = s.get('coreContent') if isinstance(s.get('coreContent'), dict) else {}
    parts = [s.get('subtitle'), s.get('title')]
    for b in cc.get('keyBullets') or []:
        parts += [b.get('desc'), b.get('title')]
    parts += re.split(r'\n+|(?<=[.!?])\s+', str(s.get('synthesisNarrative') or s.get('content') or ''))
    out = []
    for x in parts:
        x = re.sub(r'^\s*[-•]\s*', '', re.sub(r'[*=#>]+', '', str(x or ''))).strip()
        if len(x) > 8:
            out.append(x)
    return out

def repair_truncated(text, cands):
    if not TRUNC.search(text):
        return text
    body = TRUNC.sub('', text)
    k = body.find(':')
    label, frag = (body[:k + 1] + ' ', body[k + 1:].strip()) if 0 < k < 48 else ('', body.strip())
    head = fold(frag)
    if len(head) < 8:
        return text
    for c in cands:
        if fold(c).startswith(head) and len(c) >= len(frag):
            return label + c
    return text

def fix_deck(d):
    """Kesik zincir basamaklarını aynı slayttan tamamlar, cevabı ele veren ipuçlarını siler. Değişiklik sayısını döndürür."""
    n = 0
    for s in d.get('slides') or []:
        els = s.get('interactiveElements') or []
        if isinstance(s.get('interactiveElement'), dict):
            els = els + [s['interactiveElement']]
        for e in els:
            if e.get('type') == 'causal_chain':
                new = [repair_truncated(x, candidates(s)) if isinstance(x, str) else x for x in e.get('steps') or []]
                if new != e.get('steps'):
                    n += sum(1 for a, b in zip(new, e['steps']) if a != b)
                    e['steps'] = new
            elif e.get('type') == 'cloze_masking' and e.get('hint') and leaks(e['hint'], e.get('maskedTerm', '')):
                e['hint'] = ''
                n += 1
            elif e.get('type') == 'interactive_table':
                for r in e.get('tableRows') or []:
                    for c in (r.get('cells') if isinstance(r, dict) else r) or []:
                        if isinstance(c, dict) and c.get('isMasked') and c.get('hint') and leaks(c['hint'], c.get('text', '')):
                            c['hint'] = ''
                            n += 1
    return n

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    summary = '--ozet' in sys.argv
    path = args[0] if args else DEFAULT
    data = json.load(open(path, encoding='utf8'))
    decks = data if isinstance(data, list) else [data]
    if '--duzelt' in sys.argv:
        fixed = sum(fix_deck(d) for d in decks)
        tmp = path + '.tmp'
        json.dump(data, open(tmp, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
        os.replace(tmp, path)
        print(f'{fixed} alan düzeltildi → {path}')
    out = []
    for d in decks:
        check_deck(d, out)
    errs = sum(1 for o in out if o[0] == 'HATA')
    warns = len(out) - errs
    by = collections.Counter((o[0], o[1]) for o in out)
    if not summary:
        for lvl, code, did, n, msg in out[:400]:
            print(f'{lvl:5} {code:20} {did} #{n}: {msg}')
        if len(out) > 400:
            print(f'… {len(out) - 400} satır daha')
    print('\nÖzet:')
    for (lvl, code), c in sorted(by.items()):
        print(f'  {lvl:5} {code:20} {c}')
    print(f'\n{len(decks)} deste · {errs} HATA · {warns} UYARI')
    sys.exit(1 if errs else 0)

if __name__ == '__main__':
    main()
