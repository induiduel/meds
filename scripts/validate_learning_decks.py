"""Öğren destelerini docs/OGREN_ETKILESIM_REHBERI.md kurallarına göre denetler.

Kullanım:
    python3 scripts/validate_learning_decks.py                 # src/data/interactive_learning_decks.json
    python3 scripts/validate_learning_decks.py yeni_deste.json  # tek dosya (deste ya da deste listesi)
    python3 scripts/validate_learning_decks.py --ozet           # yalnız kural başına sayılar
    python3 scripts/validate_learning_decks.py --duzelt         # kesik zincir basamaklarını tamamla, sızdıran ipuçlarını sil (dosyaya yazar)
    python3 scripts/validate_learning_decks.py deck.json --oyun-zorunlu  # yeni ders: son slayt "ders sonu oyunları" olmalı (§5.14)
    python3 scripts/validate_learning_decks.py deck.json --oyun-zorunlu --kurul2  # Kurul 2+: Türkçe üslup ve şık açıklama kapıları HATA
    python3 scripts/validate_learning_decks.py --uslup          # eski destelerde üslup/şık açıklama ihlallerini UYARI olarak göster

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
# Ders sonu oyunları (rehber §5.14): yalnız destenin SON slaytında, "[OYUN SAYFASI] …" başlıklı oyun sayfasında
GAME_TYPES = {'sequence_order', 'estimate_slider', 'perturbation', 'fix_the_text'}
GAME_RE = re.compile(r'^\[OYUN SAYFASI\]', re.I)
DIRS = {'up', 'down', 'same', 'artar', 'azalır', 'azalir', 'değişmez', 'degismez'}
OYUN_ZORUNLU = '--oyun-zorunlu' in sys.argv
# Kurul 2 hata defteri (docs/KURUL2_YAPILMAYACAK_HATALAR.md): --kurul2 ile HATA; Kurul 1 desteleri toplu düzeltilmez, --uslup ile UYARI.
# --oyun-zorunlu'ya bağlanmadı: Kurul 1 ders işçisi (ders_isci/denetle.py) o bayrakla çalışıyor.
KAPI_SEVIYE = 'HATA' if '--kurul2' in sys.argv else ('UYARI' if '--uslup' in sys.argv else None)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from turkce_uslup import denetle_yapi as uslup_yapi  # noqa: E402  (docs/TURKCE_USLUP_STANDARDI.md)
from sik_aciklama import denetle as sik_denetle  # noqa: E402  (docs/SIK_ACIKLAMA_STANDARDI.md)

def is_game_slide(s):
    return bool(s.get('isGameFinale')) or bool(GAME_RE.match(str(s.get('title', ''))))

def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None

def check_game(e, n, add):
    t = e.get('type')
    if t == 'sequence_order':
        steps = [str(x.get('text') if isinstance(x, dict) else x).strip() for x in (e.get('steps') or [])]
        if not e.get('prompt') or not 3 <= len(steps) <= 8:
            add('HATA', 'sirala', n, 'prompt ve 3–8 steps (doğru sırada) gerekli')
        if len({fold(x) for x in steps}) != len(steps) or any(not x for x in steps):
            add('HATA', 'sirala-tekrar', n, 'basamaklar boş olamaz ve birbirinden farklı olmalı')
        if any(TRUNC.search(x) for x in steps):
            add('HATA', 'kesik-metin', n, 'sıralama basamağı kesilmiş')
        if not e.get('explanation'):
            add('UYARI', 'sirala-aciklama', n, 'explanation (sıranın gerekçesi) önerilir')
    elif t == 'estimate_slider':
        rounds = e.get('items') if isinstance(e.get('items'), list) and e.get('items') else [e]
        for r in rounds:
            lo, hi, ans, tol = num(r.get('min')), num(r.get('max')), num(r.get('answer')), num(r.get('tolerance', 0))
            if not r.get('prompt') or None in (lo, hi, ans, tol):
                add('HATA', 'tahmin', n, 'her turda prompt, min, max, answer, tolerance (sayı) gerekli')
                continue
            if not lo < hi or not lo <= ans <= hi:
                add('HATA', 'tahmin-aralik', n, f'min < max ve min ≤ answer ≤ max olmalı ({lo}, {hi}, {ans})')
            if tol < 0 or tol * 2 >= hi - lo:
                add('HATA', 'tahmin-tolerans', n, 'tolerance ≥ 0 ve aralığın yarısından küçük olmalı (yoksa her tahmin doğru)')
            if r.get('step') is not None and (num(r.get('step')) or 0) <= 0:
                add('HATA', 'tahmin-adim', n, 'step pozitif sayı olmalı')
            if not r.get('explanation'):
                add('UYARI', 'tahmin-aciklama', n, 'her turda explanation önerilir')
    elif t == 'perturbation':
        ps = e.get('parameters') or []
        if not e.get('scenario') or len(ps) < 3:
            add('HATA', 'ne-degisir', n, 'scenario (müdahale) ve en az 3 parameters gerekli')
        dirs = set()
        for p in ps:
            c = fold(p.get('correct') if isinstance(p, dict) else '')
            if not isinstance(p, dict) or not p.get('name') or c not in DIRS:
                add('HATA', 'ne-degisir-param', n, 'her parametrede name ve correct (up/down/same) gerekli')
                continue
            dirs.add({'artar': 'up', 'azalır': 'down', 'azalir': 'down', 'değişmez': 'same', 'degismez': 'same'}.get(c, c))
            if not p.get('explanation'):
                add('UYARI', 'ne-degisir-aciklama', n, 'her parametrede fizyopatolojik explanation önerilir')
        if len(ps) >= 3 and len(dirs) < 2:
            add('HATA', 'ne-degisir-tek-yon', n, 'tüm parametreler aynı yönde olamaz (en az 2 farklı yön)')
    elif t == 'fix_the_text':
        text = str(e.get('text') or '')
        errs = e.get('errors') or []
        if len(text.split()) < 15 or not 1 <= len(errs) <= 3:
            add('HATA', 'hata-duzelt', n, 'text (≥15 kelime) ve 1–3 errors gerekli')
        seen = []
        for er in errs:
            if not isinstance(er, dict) or not er.get('wrong') or not er.get('correct'):
                add('HATA', 'hata-duzelt-madde', n, 'her hatada wrong ve correct gerekli')
                continue
            w, c = str(er['wrong']), str(er['correct'])
            at = fold(text).find(fold(w))
            if at < 0:
                add('HATA', 'hata-duzelt-yok', n, f'yanlış ifade metinde geçmiyor: {w!r}')
            elif any(a < at + len(w) and at < b for a, b in seen):
                add('HATA', 'hata-duzelt-cakisma', n, f'yanlış ifadeler metinde çakışıyor: {w!r}')
            else:
                seen.append((at, at + len(w)))
            if fold(w) == fold(c):
                add('HATA', 'hata-duzelt-ayni', n, f'wrong ile correct aynı: {w!r}')
            others = [o for o in er.get('options') or [] if fold(o) != fold(c)]
            if len(others) < 1:
                add('HATA', 'hata-duzelt-secenek', n, 'options en az 1 çeldirici içermeli (doğru cevap otomatik eklenir)')
            if not er.get('explanation'):
                add('UYARI', 'hata-duzelt-aciklama', n, 'her hatada explanation önerilir')

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
    games = [i for i, s in enumerate(slides) if is_game_slide(s)]
    if len(games) > 1:
        add('HATA', 'oyun-sayfasi-tek', 0, 'destede en fazla 1 oyun sayfası olabilir')
    if games and games[-1] != len(slides) - 1:
        add('HATA', 'oyun-sayfasi-yer', slides[games[-1]].get('slideNumber'), 'oyun sayfası destenin SON slaytı olmalı')
    if OYUN_ZORUNLU and not games:
        add('HATA', 'oyun-sayfasi-yok', 0, 'yeni derste son slayt "[OYUN SAYFASI] Ders sonu oyunları" olmalı (rehber §5.14)')
    nums = [s.get('slideNumber') for s in slides]
    if nums != list(range(1, len(slides) + 1)):
        add('UYARI', 'slayt-sira', 0, 'slideNumber 1\'den başlayıp kesintisiz artmalı')
    for s in slides:
        n = s.get('slideNumber')
        if KAPI_SEVIYE:
            for h in uslup_yapi(s, f'slayt{n}'):
                add(KAPI_SEVIYE, 'turkce-uslup', n, h)
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
        # Ekranla aynı kaynak sırası (lesson/lessonModel.ts buildSteps): interactiveElements > elements > interactiveElement
        shown = s.get('interactiveElements') or s.get('elements') or ([s['interactiveElement']] if isinstance(s.get('interactiveElement'), dict) else [])
        game_slide = is_game_slide(s)
        if game_slide:
            gt = [e.get('type') for e in shown if isinstance(e, dict)]
            if not 4 <= len(gt) <= 6 or any(t not in GAME_TYPES for t in gt):
                add('HATA', 'oyun-sayfasi-oge', n, 'oyun sayfasında 4–6 öge olmalı ve hepsi oyun türü olmalı (sequence_order, estimate_slider, perturbation, fix_the_text)')
            elif len(set(gt)) < 4:
                add('UYARI', 'oyun-sayfasi-cesit', n, f'dört oyun türünün hepsi kullanılmalı (şu an {len(set(gt))})')
        for e in shown:
            if not isinstance(e, dict) or not e.get('type'):
                continue
            t = e.get('type')
            if t in GAME_TYPES:
                if not game_slide:
                    add('HATA', 'oyun-yeri', n, f'{t} yalnız son slayttaki oyun sayfasında kullanılır')
                check_game(e, n, add)
                continue
            if t not in TYPES:
                add('HATA', 'tur', n, f'bilinmeyen etkileşim türü: {t}')
                continue
            if t == 'micro_quiz':
                opts = e.get('microQuizOptions') or e.get('options') or []
                if not (e.get('question') or e.get('sentence')) or len(opts) < 2:
                    add('HATA', 'mini-soru', n, 'question ve en az 2 microQuizOptions gerekli')
                if sum(1 for o in opts if o.get('isCorrect')) != 1:
                    add('HATA', 'mini-soru-dogru', n, 'tam olarak bir şıkta isCorrect: true olmalı')
                if any(not o.get('explanation') for o in opts):
                    add('UYARI', 'mini-soru-aciklama', n, 'her şıkta explanation olmalı (öğrenci tüm şıkları açıp okuyabiliyor)')
                if KAPI_SEVIYE:
                    for i, o in enumerate(opts):
                        for h in sik_denetle(o.get('explanation', ''), f'mini-soru şık {i + 1}', enaz=15, encok=55, cumle=(1, 3)):
                            add(KAPI_SEVIYE, 'sik-aciklama', n, h)
            elif t == 'branching_logic':
                # Ekran options | choices | branchingOptions okur (LessonBlocks IxBody)
                opts = next((x for x in (e.get('options'), e.get('choices'), e.get('branchingOptions')) if isinstance(x, list) and x), [])
                if not e.get('scenario') or len(opts) < 2 or sum(1 for o in opts if o.get('isCorrect') or o.get('correct')) != 1:
                    add('HATA', 'klinik-karar', n, 'scenario, ≥2 seçenek (options/choices) ve tek isCorrect gerekli')
                if any(not (o.get('feedback') or o.get('explanation')) for o in opts):
                    add('UYARI', 'klinik-karar-geri', n, 'her seçenekte feedback olmalı')
                if KAPI_SEVIYE:
                    for i, o in enumerate(opts):
                        for h in sik_denetle(o.get('feedback') or o.get('explanation') or '', f'klinik karar seçenek {i + 1}', enaz=15, encok=60, cumle=(1, 3)):
                            add(KAPI_SEVIYE, 'sik-aciklama', n, h)
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
                    # İsteğe bağlı alt zincir: {"text": "2. …", "substeps": ["2a. …", "2b. …"]} (rehber §5.5)
                    txt = st.get('text') if isinstance(st, dict) else st
                    if isinstance(st, dict) and not str(txt or '').strip():
                        add('HATA', 'zincir', n, 'nesne biçimli basamakta "text" gerekli')
                    if TRUNC.search(str(txt)):
                        add('HATA', 'kesik-metin', n, f'zincir basamağı kesilmiş: {str(txt)[:70]!r}')
                    subs = st.get('substeps') if isinstance(st, dict) else None
                    if subs is not None:
                        if not isinstance(subs, list) or not 2 <= len(subs) <= 6 or any(not str(x).strip() for x in subs):
                            add('HATA', 'alt-zincir', n, 'substeps 2–6 dolu basamak olmalı')
                        elif any(TRUNC.search(str(x)) for x in subs):
                            add('HATA', 'kesik-metin', n, 'alt zincir basamağı kesilmiş')
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
