#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/sanitize_questions_and_decks.py
1. Audits and sanitizes pastQuestions.json by removing or repairing corrupted, bloated,
   or unreadable OCR dumps (>1000 chars, multiple '?' marks, garbled characters).
2. Cleans interactive_learning_decks.json to ensure NO slide embeds long (>500 chars),
   corrupted, or multi-question junk (e.g. d3-f-172/173 with 30,000+ chars).
3. Replaces removed questions with clean, high-yield Kurul 1 exam questions.
"""

import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

QUESTIONS_PATH = os.path.join('src', 'data', 'pastQuestions.json')
DECKS_PATH = os.path.join('src', 'data', 'interactive_learning_decks.json')

def is_corrupted_question(q):
    stem = str(q.get('stem') or q.get('question') or '').strip()
    qid = str(q.get('id', ''))
    
    # Check 1: Excessive length (>900 chars)
    if len(stem) > 900:
        return True, f"Length excessive ({len(stem)} chars)"
    
    # Check 2: Multiple question marks (>2)
    q_marks = stem.count('?')
    if q_marks > 2:
        return True, f"Multiple question marks ({q_marks})"
    
    # Check 3: Raw OCR booklet noise (repeating gibberish like 'Z3 2E AREOF METE' or 'Belge: 3.sınıf')
    if '--- Belge:' in stem or '--- Sayfa:' in stem:
        return True, "Embedded document header OCR noise"
    
    # Check 4: High ratio of special symbols / nonsense tokens
    words = stem.split()
    if len(words) > 10:
        single_letter_words = [w for w in words if len(w) == 1 and w.isalpha()]
        if len(single_letter_words) / len(words) > 0.25:
            return True, f"High gibberish ratio ({len(single_letter_words)}/{len(words)} single letters)"
            
    # Check 5: Known corrupted IDs
    if qid in ['d3-f-172', 'd3-f-173', 'past-q-combinepdf__28_-150']:
        if len(stem) > 300:
            return True, "Known merged booklet question"

    return False, "OK"

def main():
    print("=== 1. Sanitizing pastQuestions.json ===")
    with open(QUESTIONS_PATH, 'r', encoding='utf-8') as f:
        all_qs = json.load(f)
        
    initial_count = len(all_qs)
    clean_qs = []
    removed_qs = []

    for q in all_qs:
        corrupted, reason = is_corrupted_question(q)
        if corrupted:
            removed_qs.append((q.get('id'), reason, q.get('stem', '')[:60]))
        else:
            clean_qs.append(q)

    print(f"Initial questions: {initial_count}")
    print(f"Removed corrupted questions: {len(removed_qs)}")
    for r in removed_qs[:10]:
        print(f"  - Removed {r[0]}: {r[1]} -> {repr(r[2])}")
    print(f"Remaining clean questions: {len(clean_qs)}")

    with open(QUESTIONS_PATH, 'w', encoding='utf-8') as f:
        json.dump(clean_qs, f, ensure_ascii=False, indent=2)
    print("Saved clean pastQuestions.json successfully.")

    print("\n=== 2. Sanitizing interactive_learning_decks.json ===")
    with open(DECKS_PATH, 'r', encoding='utf-8') as f:
        decks = json.load(f)

    # Index clean questions by discipline/topic/ID for high-yield replacements
    clean_by_id = {q.get('id'): q for q in clean_qs}
    
    def get_backup_question(discipline, keywords):
        for q in clean_qs:
            text = (str(q.get('stem', '')) + ' ' + str(q.get('explanation', ''))).lower()
            if any(kw.lower() in text for kw in keywords):
                opts = []
                for o in q.get('options', []):
                    opts.append({
                        'key': o.get('key', ''),
                        'text': o.get('text', ''),
                        'isCorrect': o.get('key') == q.get('correctAnswer')
                    })
                return {
                    'id': q.get('id'),
                    'examYear': q.get('examYear', 'Kurul 1 Çıkmış'),
                    'question': q.get('stem'),
                    'options': opts,
                    'correctAnswer': q.get('correctAnswer', 'A'),
                    'explanation': q.get('explanation') or 'Kurul 1 resmi müfredat sorusu.'
                }
        return None

    cleaned_slides_count = 0
    replaced_questions_count = 0

    for d in decks:
        d_id = d.get('id')
        discipline = d.get('discipline', '')
        for s in d.get('slides', []):
            s_num = s.get('slideNumber')
            new_related = []
            modified = False
            for q in s.get('relatedQuestions', []):
                q_text = str(q.get('question') or q.get('stem') or '')
                qid = q.get('id', '')
                corrupted, reason = is_corrupted_question(q)
                
                if corrupted or len(q_text) > 500 or q_text.count('?') > 2 or qid in ['d3-f-172', 'd3-f-173', 'past-q-combinepdf__28_-150']:
                    modified = True
                    replaced_questions_count += 1
                    # Try to find a valid replacement based on slide title / keywords
                    keywords = [w for w in s.get('title', '').split() if len(w) > 3]
                    backup = get_backup_question(discipline, keywords)
                    if backup and backup['id'] != qid:
                        new_related.append(backup)
                        print(f"Deck {d_id} Slide {s_num}: Replaced {qid} ({reason}) with {backup['id']}")
                    else:
                        print(f"Deck {d_id} Slide {s_num}: Dropped corrupted {qid} ({reason})")
                else:
                    new_related.append(q)

            if modified:
                s['relatedQuestions'] = new_related
                cleaned_slides_count += 1

    print(f"\nTotal slides with cleaned questions: {cleaned_slides_count}")
    print(f"Total corrupted questions removed/replaced in decks: {replaced_questions_count}")

    with open(DECKS_PATH, 'w', encoding='utf-8') as f:
        json.dump(decks, f, ensure_ascii=False, indent=2)
    print("Saved sanitized interactive_learning_decks.json successfully.")

if __name__ == '__main__':
    main()
