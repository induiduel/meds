#!/usr/bin/env python3
"""
Retrofit and normalize all past decks (12-41) to ensure full interactiveElements coverage,
canonical schema compliance, and zero validation errors.
"""

import json, os, sys, copy, re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DECKS_PATH = os.path.join(ROOT_DIR, 'src', 'data', 'interactive_learning_decks.json')
ITEMS_DIR = os.path.join(ROOT_DIR, 'src', 'data', 'decks', 'items')
PACKAGES_DIR = os.path.join(os.path.dirname(ROOT_DIR), 'packages')

sys.path.insert(0, os.path.join(ROOT_DIR, 'scripts'))
from validate_learning_decks import check_deck, leaks
import enrichment_definitions as ed

def clean_hint(hint, answer):
    if not leaks(hint, answer):
        return hint
    candidates = [
        'Kritik kavram', 'Klinik parametre', 'Temel bulgu',
        'Patofizyolojik mekanizma', 'Ayırıcı kriter', 'Hedef molekül',
        'Önemli gösterge', 'Değerlendirme faktörü', 'Belirteç'
    ]
    for c in candidates:
        if not leaks(c, answer):
            return c
    return 'Kriter'

def sanitize_element(el):
    t = el.get('type')
    if t == 'micro_quiz':
        if 'microQuizOptions' not in el and 'options' in el:
            el['microQuizOptions'] = el['options']
        if 'options' not in el and 'microQuizOptions' in el:
            el['options'] = el['microQuizOptions']
    elif t == 'branching_logic':
        if 'options' not in el and 'choices' in el:
            opts = []
            for ch in el['choices']:
                is_corr = ch.get('isCorrect')
                if is_corr is None:
                    outcome = (ch.get('outcome') or ch.get('feedback') or ch.get('explanation') or '').strip().lower()
                    is_corr = outcome.startswith('doğru') or outcome.startswith('dogru')
                opts.append({
                    'text': ch.get('text', ''),
                    'isCorrect': bool(is_corr),
                    'feedback': ch.get('feedback') or ch.get('explanation') or ch.get('outcome') or 'Açıklama'
                })
            true_count = sum(1 for o in opts if o['isCorrect'])
            if true_count == 0 and opts:
                opts[0]['isCorrect'] = True
            elif true_count > 1:
                first = True
                for o in opts:
                    if o['isCorrect']:
                        if not first:
                            o['isCorrect'] = False
                        first = False
            el['options'] = opts
        q_text = el.get('initialQuestion') or el.get('question')
        if q_text:
            if not el.get('scenario'):
                el['scenario'] = q_text
            elif q_text not in el['scenario']:
                el['scenario'] = f"{el['scenario']} - {q_text}"
        for opt in el.get('options', []):
            if 'feedback' not in opt and 'explanation' in opt:
                opt['feedback'] = opt['explanation']
            elif 'feedback' not in opt and 'outcome' in opt:
                opt['feedback'] = opt['outcome']
    elif t == 'before_after_slider':
        if 'leftTitle' not in el and 'beforeTitle' in el:
            el['leftTitle'] = el.get('beforeTitle') or 'Önceki Durum'
            el['rightTitle'] = el.get('afterTitle') or 'Sonraki Durum'
            el['leftPoints'] = [el.get('beforeText', '')]
            el['rightPoints'] = [el.get('afterText', '')]
        elif 'leftPoints' in el and 'rightPoints' in el:
            lp = el['leftPoints'] if isinstance(el['leftPoints'], list) else [el['leftPoints']]
            rp = el['rightPoints'] if isinstance(el['rightPoints'], list) else [el['rightPoints']]
            el['leftPoints'] = lp
            el['rightPoints'] = rp
    elif t == 'cloze_masking':
        sen, term = el.get('sentence', ''), el.get('maskedTerm', '')
        if el.get('hint') and leaks(el['hint'], term):
            el['hint'] = clean_hint(el['hint'], term)
    elif t == 'interactive_table':
        for r in el.get('tableRows', []):
            cells = r.get('cells') if isinstance(r, dict) else r
            for c in cells or []:
                if isinstance(c, dict) and c.get('isMasked') and c.get('hint') and leaks(c['hint'], c.get('text', '')):
                    c['hint'] = clean_hint(c['hint'], c.get('text', ''))
    return el

def main():
    print(f"Loading decks from {SRC_DECKS_PATH}...")
    with open(SRC_DECKS_PATH, 'r', encoding='utf-8') as f:
        decks = json.load(f)

    modified_deck_ids = set()

    for d in decks:
        did = d.get('id', '')
        if not did.startswith('k1p-k1-'):
            continue
        try:
            num = int(did.split('-')[2])
        except ValueError:
            continue

        if 12 <= num <= 36:
            for s in d['slides']:
                if 'elements' in s:
                    s['interactiveElements'] = [sanitize_element(copy.deepcopy(x)) for x in s['elements']]
                elif 'interaction' in s:
                    s['interactiveElements'] = [sanitize_element(copy.deepcopy(s['interaction']))]
            modified_deck_ids.add(did)

        elif num in [37, 38, 39]:
            enrich_dict = {37: ed.D37_ENRICHMENTS, 38: ed.D38_ENRICHMENTS, 39: ed.D39_ENRICHMENTS}[num]
            for s in d['slides']:
                snum = s['slideNumber']
                elems = []
                if 'microQuiz' in s:
                    mq = s['microQuiz']
                    elems.append(sanitize_element({
                        'type': 'micro_quiz',
                        'question': mq.get('question', ''),
                        'options': mq.get('options', []),
                        'microQuizOptions': mq.get('options', [])
                    }))
                if snum in enrich_dict:
                    for el in enrich_dict[snum]:
                        elems.append(sanitize_element(copy.deepcopy(el)))
                s['interactiveElements'] = elems
            modified_deck_ids.add(did)

        elif num == 40:
            for s in d['slides']:
                snum = s['slideNumber']
                if snum in ed.D40_ENRICHMENTS:
                    elems = s.get('interactiveElements', [])
                    for el in ed.D40_ENRICHMENTS[snum]:
                        elems.append(sanitize_element(copy.deepcopy(el)))
                    s['interactiveElements'] = elems
            modified_deck_ids.add(did)

        elif num == 41:
            for s in d['slides']:
                snum = s['slideNumber']
                if snum in ed.D41_ENRICHMENTS:
                    elems = s.get('interactiveElements', [])
                    for el in ed.D41_ENRICHMENTS[snum]:
                        elems.append(sanitize_element(copy.deepcopy(el)))
                    s['interactiveElements'] = elems
            modified_deck_ids.add(did)

    # Validate all decks
    print(f"Validating all {len(decks)} decks before saving...")
    total_errors = 0
    for d in decks:
        out = []
        check_deck(d, out)
        errors = [x for x in out if x[0] == 'HATA']
        if errors:
            total_errors += len(errors)
            print(f"ERROR in {d['id']}:")
            for e in errors:
                print("  ", e)

    if total_errors > 0:
        print(f"ABORTING: {total_errors} validation errors encountered.")
        sys.exit(1)

    print("ALL DECKS VALIDATED SUCCESSFULLY (0 ERRORS)!")
    print(f"Writing updated decks to {SRC_DECKS_PATH}...")
    with open(SRC_DECKS_PATH, 'w', encoding='utf-8') as f:
        json.dump(decks, f, ensure_ascii=False, indent=2)

    print(f"Syncing {len(modified_deck_ids)} modified decks to items/ and packages/...")
    for did in modified_deck_ids:
        deck_obj = next(x for x in decks if x['id'] == did)
        item_path = os.path.join(ITEMS_DIR, f"{did}.json")
        if os.path.exists(os.path.dirname(item_path)):
            with open(item_path, 'w', encoding='utf-8') as f:
                json.dump(deck_obj, f, ensure_ascii=False, indent=2)

        pkg_deck_path = os.path.join(PACKAGES_DIR, did, 'deck.json')
        if os.path.exists(os.path.dirname(pkg_deck_path)):
            with open(pkg_deck_path, 'w', encoding='utf-8') as f:
                json.dump(deck_obj, f, ensure_ascii=False, indent=2)

    print("Sync complete.")

if __name__ == '__main__':
    main()
