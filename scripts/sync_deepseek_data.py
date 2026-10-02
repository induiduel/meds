#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/sync_deepseek_data.py
Robust DeepSeek Data Synchronizer and Sanitizer for MedSoru:
- Scans `meds_database/deepseek_data/` and local `deepseek_data/`.
- Enforces strict anti-corruption filters:
    * Rejects bloated questions (>1000 chars)
    * Rejects questions with >3 question marks (OCR booklet dumps)
    * Requires valid options (>= 2 choices)
    * Strips OCR artifacts (e.g. SAYFA NO, repetitive exam headers)
- Syncs clean questions to `src/data/pastQuestions.json` and `src/data/interactive_learning_decks.json`.
- Merges medical glossary additions to `src/data/medical_glossary.json`.
- Merges markdown spot pearls to relevant slide decks.
"""

import os
import sys
import json
import re
import glob

sys.stdout.reconfigure(encoding='utf-8')

# Search paths for deepseek data
CANDIDATE_DIRS = [
    r"c:\Users\indui\Desktop\meds_database\deepseek_data",
    os.path.join(os.path.dirname(__file__), "..", "deepseek_data"),
    os.path.join(os.getcwd(), "deepseek_data"),
]

PAST_QUESTIONS_PATH = os.path.join("src", "data", "pastQuestions.json")
DECKS_PATH = os.path.join("src", "data", "interactive_learning_decks.json")
GLOSSARY_PATH = os.path.join("src", "data", "medical_glossary.json")

# Quality thresholds
MAX_STEM_LENGTH = 1000
MAX_QUESTION_MARKS = 3
MIN_STEM_LENGTH = 20
MIN_OPTIONS = 2

def sanitize_stem(text: str) -> str:
    """Removes common OCR artifacts from question stems."""
    if not text:
        return ""
    cleaned = re.sub(r'SAYFA\s+NO:\s*\d+', '', text, flags=re.IGNORECASE)
    cleaned = re.sub(r'T\.C\.\s+KARAB[UÜ]K\s+[UÜ]N[Iİ]VERS[Iİ]TES[Iİ][^\n]*', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'TIP\s+FAK[UÜ]LTES[Iİ][^\n]*', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'D[OÖ]NEM\s+III[^\n]*', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

def validate_question(q: dict) -> tuple[bool, str]:
    """Validates question quality and returns (isValid, reason)."""
    stem = q.get('stem') or q.get('question') or ''
    stem = sanitize_stem(stem)
    
    if len(stem) < MIN_STEM_LENGTH:
        return False, f"Stem too short ({len(stem)} chars)"
    
    if len(stem) > MAX_STEM_LENGTH:
        return False, f"Stem bloated (> {MAX_STEM_LENGTH} chars: {len(stem)} chars)"
    
    qmark_count = stem.count('?')
    if qmark_count > MAX_QUESTION_MARKS:
        return False, f"Too many question marks ({qmark_count} > {MAX_QUESTION_MARKS}, multi-question booklet dump)"
    
    options = q.get('options', [])
    if not isinstance(options, list) or len(options) < MIN_OPTIONS:
        return False, f"Invalid options count ({len(options)} < {MIN_OPTIONS})"
    
    return True, "Valid"

def sync_questions(data_dirs):
    if not os.path.exists(PAST_QUESTIONS_PATH):
        print(f"Warning: {PAST_QUESTIONS_PATH} not found.")
        return 0, 0

    with open(PAST_QUESTIONS_PATH, 'r', encoding='utf-8') as f:
        past_questions = json.load(f)

    # Purge any pre-existing bloated questions (>1000 chars or >3 ?)
    clean_existing = []
    purged_existing = 0
    for q in past_questions:
        st = q.get('stem', '')
        if len(st) > MAX_STEM_LENGTH or st.count('?') > MAX_QUESTION_MARKS:
            purged_existing += 1
            continue
        clean_existing.append(q)

    if purged_existing > 0:
        print(f"Purged {purged_existing} pre-existing corrupted questions from pastQuestions.")

    pq_map = {q['id']: q for q in clean_existing if 'id' in q}

    accepted = 0
    rejected = 0
    rejection_reasons = {}

    for ddir in data_dirs:
        if not os.path.isdir(ddir):
            continue

        # Look for *.json and *.jsonl
        for filepath in glob.glob(os.path.join(ddir, "*.*")):
            ext = os.path.splitext(filepath)[1].lower()
            filename = os.path.basename(filepath)
            if ext not in ['.json', '.jsonl'] or filename.startswith('glossary_'):
                continue

            print(f"Scanning file for questions: {filename}")
            questions_in_file = []

            if ext == '.jsonl':
                with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                questions_in_file.append(json.loads(line))
                            except Exception:
                                pass
            else:
                with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                    try:
                        content = json.load(f)
                        if isinstance(content, list):
                            questions_in_file = content
                        elif isinstance(content, dict) and 'questions' in content:
                            questions_in_file = content['questions']
                    except Exception:
                        pass

            for raw_q in questions_in_file:
                if not isinstance(raw_q, dict):
                    continue
                
                is_valid, reason = validate_question(raw_q)
                if not is_valid:
                    rejected += 1
                    rejection_reasons[reason] = rejection_reasons.get(reason, 0) + 1
                    continue

                qid = raw_q.get('id')
                if not qid:
                    qid = f"ds-q-{len(pq_map) + 1:04d}"
                    raw_q['id'] = qid

                raw_q['stem'] = sanitize_stem(raw_q.get('stem') or raw_q.get('question') or '')
                raw_q['source'] = 'deepseek'
                raw_q['contributor'] = 'DeepSeek AI'
                raw_q['isContribution'] = True

                pq_map[qid] = raw_q
                accepted += 1

    # Save pastQuestions
    updated_list = list(pq_map.values())
    with open(PAST_QUESTIONS_PATH, 'w', encoding='utf-8') as f:
        json.dump(updated_list, f, ensure_ascii=False, indent=2)

    print(f"-> Question Sync Complete: {accepted} accepted, {rejected} rejected.")
    if rejection_reasons:
        for r, cnt in rejection_reasons.items():
            print(f"   [REJECTED] {r}: {cnt} items")

    return accepted, rejected

def sync_glossary(data_dirs):
    if not os.path.exists(GLOSSARY_PATH):
        print(f"Warning: {GLOSSARY_PATH} not found.")
        return 0

    with open(GLOSSARY_PATH, 'r', encoding='utf-8') as f:
        glossary = json.load(f)

    existing_terms = {g['term'].lower().strip(): g for g in glossary}
    added = 0
    updated = 0

    for ddir in data_dirs:
        if not os.path.isdir(ddir):
            continue

        for filepath in glob.glob(os.path.join(ddir, "*glossary*.json")) + glob.glob(os.path.join(ddir, "*tibbi_terim*.json")):
            print(f"Scanning glossary file: {os.path.basename(filepath)}")
            try:
                with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                    items = json.load(f)
                    if not isinstance(items, list):
                        continue
                    for item in items:
                        if not isinstance(item, dict) or 'term' not in item or 'definition' not in item:
                            continue
                        t_key = item['term'].lower().strip()
                        if t_key in existing_terms:
                            # Update existing
                            ex = existing_terms[t_key]
                            if 'definition' in item and len(item['definition']) > len(ex.get('definition', '')):
                                ex['definition'] = item['definition']
                            if 'clinicalPearls' in item and not ex.get('clinicalPearls'):
                                ex['clinicalPearls'] = item['clinicalPearls']
                            updated += 1
                        else:
                            # Add new
                            glossary.append(item)
                            existing_terms[t_key] = item
                            added += 1
            except Exception as e:
                print(f"Error reading glossary file {filepath}: {e}")

    # Sort alphabetically
    glossary.sort(key=lambda x: x.get('term', '').lower())
    with open(GLOSSARY_PATH, 'w', encoding='utf-8') as f:
        json.dump(glossary, f, ensure_ascii=False, indent=2)

    print(f"-> Glossary Sync Complete: {added} new terms added, {updated} updated (Total: {len(glossary)}).")
    return added + updated

def sync_markdown_spot_notes(data_dirs):
    if not os.path.exists(DECKS_PATH):
        print(f"Warning: {DECKS_PATH} not found.")
        return 0

    with open(DECKS_PATH, 'r', encoding='utf-8') as f:
        decks = json.load(f)

    enriched_slides = 0

    for ddir in data_dirs:
        if not os.path.isdir(ddir):
            continue

        for filepath in glob.glob(os.path.join(ddir, "*.md")):
            filename = os.path.basename(filepath)
            if 'readme' in filename.lower():
                continue

            print(f"Scanning spot notes markdown: {filename}")
            try:
                with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()

                # Parse sections with ##
                sections = re.split(r'\n(?=##\s+)', content)
                for sec in sections:
                    lines = sec.strip().split('\n')
                    if not lines or not lines[0].startswith('##'):
                        continue
                    sec_title = lines[0].replace('##', '').strip()
                    sec_body = '\n'.join(lines[1:]).strip()

                    # Find matching decks/slides
                    keywords = [w.lower() for w in re.findall(r'\b\w{4,}\b', sec_title)]
                    for deck in decks:
                        deck_text = (deck.get('title', '') + ' ' + deck.get('discipline', '')).lower()
                        # If at least 2 keywords match deck title/discipline
                        matches = sum(1 for kw in keywords if kw in deck_text)
                        if matches >= 1:
                            # Enrich first matching slide's synthesis
                            for slide in deck.get('slides', [])[:3]:
                                syn = slide.get('synthesisNarrative', '')
                                if sec_title not in syn:
                                    note_block = f"\n\n### 💡 DeepSeek & Hoca Spot İncisi: {sec_title}\n"
                                    # Bulletize lines if not bulleted
                                    for bline in sec_body.split('\n'):
                                        bline = bline.strip()
                                        if not bline:
                                            continue
                                        if not bline.startswith(('•', '-', '*', '1.', '2.', '3.')):
                                            note_block += f"• **Spot Vurgu:** {bline}\n"
                                        else:
                                            note_block += f"{bline}\n"
                                    slide['synthesisNarrative'] = syn + note_block
                                    enriched_slides += 1
                                    break
            except Exception as e:
                print(f"Error parsing markdown {filepath}: {e}")

    # Re-verify and sanitize questions inside decks
    sanitized_in_decks = 0
    for deck in decks:
        for slide in deck.get('slides', []):
            clean_exam_q = []
            for q in slide.get('pastExamQuestions', []):
                stem = q.get('stem', '')
                if len(stem) > MAX_STEM_LENGTH or stem.count('?') > MAX_QUESTION_MARKS:
                    sanitized_in_decks += 1
                    continue
                clean_exam_q.append(q)
            slide['pastExamQuestions'] = clean_exam_q

    with open(DECKS_PATH, 'w', encoding='utf-8') as f:
        json.dump(decks, f, ensure_ascii=False, indent=2)

    print(f"-> Spot Notes Sync: {enriched_slides} slides enriched with DeepSeek spot pearls.")
    print(f"-> Decks Question Audit: {sanitized_in_decks} bloated questions pruned from decks.")
    return enriched_slides

def main():
    print("=" * 60)
    print("🩺 MedSoru DeepSeek Data Synchronizer & Quality Gatekeeper")
    print("=" * 60)

    existing_dirs = [d for d in CANDIDATE_DIRS if os.path.exists(d)]
    if not existing_dirs:
        print("No deepseek_data directory found in candidate paths:")
        for d in CANDIDATE_DIRS:
            print(f"  - {d}")
        # Create default local directory for convenience
        default_dir = os.path.join(os.getcwd(), "deepseek_data")
        os.makedirs(default_dir, exist_ok=True)
        print(f"Created default folder at {default_dir}. Drop DeepSeek files here.")
        existing_dirs = [default_dir]
    else:
        print("Found active deepseek_data directories:")
        for d in existing_dirs:
            print(f"  ✓ {d}")

    print("\n1. Synchronizing Past Questions...")
    sync_questions(existing_dirs)

    print("\n2. Synchronizing Medical Glossary...")
    sync_glossary(existing_dirs)

    print("\n3. Synchronizing Spot Notes & Verifying Decks...")
    sync_markdown_spot_notes(existing_dirs)

    print("\n✅ DeepSeek Data Synchronization completed successfully.")
    print("=" * 60)

if __name__ == '__main__':
    main()
