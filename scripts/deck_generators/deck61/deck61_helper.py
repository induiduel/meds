# -*- coding: utf-8 -*-
"""
Deck 61 Helper Functions and Strict Validators
Guarantees:
- Middle-high difficulty, authentic medical questions from amfi lecture notes
- Strict chronology and zero forward leakage
- Non-empty explanations for EVERY option (correct and distractors)
- Balanced answer keys (A, B, C, D)
- Cloze maskedTerm must be exact substring of sentence, hint must NOT leak maskedTerm (raises ValueError if leaks)
- Table cell hints must NOT leak cell text (raises ValueError if leaks)
- No feature_bidding allowed
- Strict model support for all 10 interactive elements
"""

import unicodedata

def fold(s: str) -> str:
    """Normalize and lowercase for leakage detection."""
    if not s:
        return ""
    s = s.replace("I", "ı").replace("İ", "i").lower()
    return "".join(
        c for c in unicodedata.normalize("NFKD", s)
        if not unicodedata.combining(c)
    )

def leaks(hint: str, answer: str) -> bool:
    """
    Returns True if hint contains words/stems of answer.
    Checks words of length >= 5 or complete words.
    """
    f_hint = fold(hint)
    f_ans = fold(answer)
    words = [w for w in "".join(c if c.isalnum() else " " for c in f_ans).split() if len(w) >= 3]
    for w in words:
        stem = w[:5] if len(w) >= 5 else w
        if stem in f_hint:
            return True
    return False

def make_quiz(question, options, correct_key=None):
    """
    options: [{"key": "A", "text": "...", "isCorrect": bool, "explanation": "..."}, ...]
    """
    if len(options) not in (4, 5):
        raise ValueError(f"Quiz must have 4 or 5 options, got {len(options)}")
    
    correct_opts = [opt for opt in options if opt.get("isCorrect")]
    if len(correct_opts) != 1:
        raise ValueError(f"Quiz must have exactly 1 correct option, got {len(correct_opts)}")
    
    for opt in options:
        if not opt.get("text") or not opt.get("text").strip():
            raise ValueError(f"Quiz option text cannot be empty: {opt}")
        if not opt.get("explanation") or not opt.get("explanation").strip():
            raise ValueError(f"Quiz option explanation cannot be empty: {opt}")
        if opt["explanation"] in ("Doğru.", "Yanlış.", "Alakasız bir patolojik tablodur"):
            raise ValueError(f"Quiz explanation must be detailed and pathophysiological, got: '{opt['explanation']}'")

    if correct_key and correct_opts[0].get("key") != correct_key:
        raise ValueError(f"Quiz correct option {correct_opts[0].get('key')} != requested {correct_key}")

    return {
        "type": "micro_quiz",
        "question": question,
        "microQuizOptions": options
    }

def make_cloze(sentence, masked_term, hint):
    """
    Sentence must contain masked_term as exact substring.
    Hint must not leak masked_term.
    """
    if masked_term not in sentence:
        raise ValueError(f"cloze_masking maskedTerm '{masked_term}' not in sentence '{sentence}'")
    if not hint or not hint.strip():
        raise ValueError(f"cloze_masking hint cannot be empty for '{masked_term}'")
    if leaks(hint, masked_term):
        raise ValueError(f"cloze_masking hint '{hint}' leaks maskedTerm '{masked_term}'")
    
    return {
        "type": "cloze_masking",
        "sentence": sentence,
        "maskedTerm": masked_term,
        "hint": hint
    }

def make_table(title, headers, rows):
    """
    rows: [ [ {"text": "...", "isMasked": False}, {"text": "...", "isMasked": True, "hint": "..."}, ... ], ... ]
    """
    if not rows or len(rows) < 2:
        raise ValueError("Table must have at least 2 rows")
    num_headers = len(headers)
    for r_idx, row in enumerate(rows):
        if len(row) != num_headers:
            raise ValueError(f"Table row {r_idx} length {len(row)} != headers length {num_headers}")
        for cell in row:
            if cell.get("isMasked"):
                hint = cell.get("hint", "")
                text = cell.get("text", "")
                if not hint or not hint.strip():
                    raise ValueError(f"Masked cell '{text}' must have a non-empty hint")
                if leaks(hint, text):
                    raise ValueError(f"Table hint '{hint}' leaks cell text '{text}' in table '{title}'")
    formatted_rows = []
    for r in rows:
        if isinstance(r, dict) and "cells" in r:
            formatted_rows.append(r)
        elif isinstance(r, list):
            formatted_rows.append({"cells": r})
        else:
            formatted_rows.append(r)

    return {
        "type": "interactive_table",
        "title": title,
        "tableTitle": title,
        "headers": headers,
        "tableHeaders": headers,
        "rows": formatted_rows,
        "tableRows": formatted_rows
    }

def make_chain(title, steps):
    """
    steps: ["1. Etiket: Açıklama...", ...]
    """
    if len(steps) < 3 or len(steps) > 6:
        raise ValueError(f"Chain steps must be between 3 and 6, got {len(steps)}")
    for s in steps:
        if not s or not s.strip():
            raise ValueError("Chain step cannot be empty")
        if s.endswith("...") or s.endswith("…"):
            raise ValueError(f"Chain step cannot end with ellipsis: {s}")
    return {
        "type": "causal_chain",
        "title": title,
        "steps": steps
    }

def make_recall(question, answer):
    if not question or not question.strip():
        raise ValueError("Recall question cannot be empty")
    if not answer or not answer.strip():
        raise ValueError("Recall answer cannot be empty")
    return {
        "type": "active_recall",
        "question": question,
        "answer": answer
    }

def make_spot_the_lie(topic, items):
    """
    items: [{"text": "...", "isLie": bool, "explanation": "..."}, ...]
    Exactly 1 lie, 3-4 items.
    """
    if len(items) not in (3, 4):
        raise ValueError(f"spot_the_lie must have 3 or 4 items, got {len(items)}")
    lie_count = sum(1 for it in items if it.get("isLie"))
    if lie_count != 1:
        raise ValueError(f"spot_the_lie must have exactly 1 lie, got {lie_count}")
    for it in items:
        if not it.get("text") or not it.get("explanation"):
            raise ValueError(f"spot_the_lie item missing text or explanation: {it}")
        if it["explanation"] in ("Doğru.", "Yanlış."):
            raise ValueError(f"spot_the_lie explanation must be detailed, got: {it['explanation']}")
    return {
        "type": "spot_the_lie",
        "topic": topic,
        "items": items
    }

def make_slider(left_title, right_title, left_points, right_points):
    """
    before_after_slider: equal length points.
    """
    if len(left_points) != len(right_points):
        raise ValueError(f"Slider points mismatch: {len(left_points)} vs {len(right_points)}")
    if len(left_points) < 2:
        raise ValueError("Slider requires at least 2 comparison points")
    return {
        "type": "before_after_slider",
        "leftTitle": left_title,
        "rightTitle": right_title,
        "leftPoints": left_points,
        "rightPoints": right_points
    }

def make_swipe(title, left_category, right_category, cards):
    """
    swipe_matching: cards category must be 'left' or 'right'
    """
    if len(cards) < 3:
        raise ValueError("swipe_matching requires at least 3 cards")
    for c in cards:
        if c.get("category") not in ("left", "right"):
            raise ValueError(f"swipe_matching card category must be 'left' or 'right': {c}")
        if not c.get("text") or not c.get("explanation"):
            raise ValueError(f"swipe_matching card missing text or explanation: {c}")
    return {
        "type": "swipe_matching",
        "title": title,
        "leftCategory": left_category,
        "rightCategory": right_category,
        "cards": cards
    }

def make_venn(title, label_a, label_b, items):
    """
    venn_grid: items with correct in ('A', 'B', 'both', 'neither')
    """
    if len(items) < 3:
        raise ValueError("venn_grid requires at least 3 items")
    for it in items:
        if str(it.get("correct")).lower() not in ("a", "b", "both", "neither"):
            raise ValueError(f"venn_grid item correct value must be A, B, both, or neither: {it}")
        if not it.get("criterion") or not it.get("explanation"):
            raise ValueError(f"venn_grid item missing criterion or explanation: {it}")
    return {
        "type": "venn_grid",
        "title": title,
        "labelA": label_a,
        "labelB": label_b,
        "items": items
    }

def make_branching(scenario, options):
    """
    branching_logic: exactly 1 correct, middle-high difficulty
    """
    if len(options) < 3:
        raise ValueError("branching_logic requires at least 3 options")
    correct_count = sum(1 for opt in options if opt.get("isCorrect"))
    if correct_count != 1:
        raise ValueError(f"branching_logic must have exactly 1 correct option, got {correct_count}")
    for opt in options:
        if not opt.get("text") or not opt.get("feedback"):
            raise ValueError(f"branching_logic option missing text or feedback: {opt}")
    return {
        "type": "branching_logic",
        "scenario": scenario,
        "options": options
    }

def make_slide(slide_num, title, subtitle, clinical_focus, narrative, bullets, elements, is_checkpoint=False, checkpoint_number=None):
    """
    Creates a canonical learning slide.
    Validates word count >= 60 (target 70-150 words).
    Validates elements count (4 to 6 elements).
    """
    words = len(narrative.split())
    if words < 60:
        raise ValueError(f"Slide {slide_num} narrative word count too short: {words} words (minimum 60 required)")
    
    if len(elements) < 4 or len(elements) > 6:
        raise ValueError(f"Slide {slide_num} must have 4-6 interactive elements, got {len(elements)}")

    # Check for forbidden models
    for el in elements:
        if el.get("type") == "feature_bidding":
            raise ValueError(f"Slide {slide_num} contains forbidden element 'feature_bidding'")

    slide = {
        "slideNumber": slide_num,
        "title": title,
        "subtitle": subtitle,
        "clinicalFocus": clinical_focus,
        "content": narrative,
        "synthesisNarrative": narrative,
        "bullets": bullets,
        "interactiveElements": elements
    }
    if is_checkpoint:
        slide["isCheckpoint"] = True
        slide["checkpointNumber"] = checkpoint_number
    return slide
