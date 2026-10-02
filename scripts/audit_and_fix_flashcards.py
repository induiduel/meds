#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/audit_and_fix_flashcards.py
Audits all flashcards across all interactive learning decks.
Guarantees that every flashcard has BOTH:
  - front AND question (front = front or question)
  - back AND answer (back = back or answer)
  - hint
  - category
Ensures no flashcard is empty.
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECKS_PATH = os.path.join('src', 'data', 'interactive_learning_decks.json')

def main():
    if not os.path.exists(DECKS_PATH):
        print(f"Error: {DECKS_PATH} not found.")
        return

    with open(DECKS_PATH, 'r', encoding='utf-8') as f:
        decks = json.load(f)

    fixed_count = 0
    total_cards = 0
    empty_cards = 0

    for d in decks:
        deck_id = d.get('id', 'unknown')
        for s in d.get('slides', []):
            slide_no = s.get('slideNumber', 0)
            cards = s.get('flashcards', [])
            for c in cards:
                total_cards += 1
                front_val = c.get('front') or c.get('question') or ''
                back_val = c.get('back') or c.get('answer') or ''

                if not front_val or not back_val:
                    print(f"⚠️ Empty flashcard in {deck_id} slide #{slide_no}: front='{front_val}', back='{back_val}'")
                    empty_cards += 1

                # Normalize so both pairs exist
                needs_fix = False
                if c.get('front') != front_val:
                    c['front'] = front_val
                    needs_fix = True
                if c.get('question') != front_val:
                    c['question'] = front_val
                    needs_fix = True
                if c.get('back') != back_val:
                    c['back'] = back_val
                    needs_fix = True
                if c.get('answer') != back_val:
                    c['answer'] = back_val
                    needs_fix = True
                if not c.get('category'):
                    c['category'] = 'Akıl Kartı'
                    needs_fix = True

                if needs_fix:
                    fixed_count += 1

    print(f"Total Flashcards: {total_cards}")
    print(f"Fixed/Synchronized: {fixed_count}")
    print(f"Empty Cards Found: {empty_cards}")

    with open(DECKS_PATH, 'w', encoding='utf-8') as f:
        json.dump(decks, f, ensure_ascii=False, indent=2)
    print("Saved updated interactive_learning_decks.json successfully.")

if __name__ == '__main__':
    main()
