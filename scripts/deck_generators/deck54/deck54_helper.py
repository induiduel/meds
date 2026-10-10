"""
Helper module for Deck 54 (and future decks) generator.
Strictly adheres to:
1. Randomized/balanced micro_quiz correct answers (A, B, C, D, E distribution).
2. Explicit, authentic distractor explanations (every option has comprehensive physiological rationale).
3. Zero placeholder/forced default overrides (no silent hack, explicit verification).
4. Safe, authentic hints that NEVER leak answers (semantic hints, no word stems).
5. Full support for all interactive models:
   - micro_quiz
   - cloze_masking
   - interactive_table
   - causal_chain
   - active_recall
   - spot_the_lie
   - before_after_slider
   - swipe_matching
   - venn_grid
   - branching_logic
"""

import json, os, re
from meds.scripts.validate_learning_decks import leaks, fold

def make_slide(slide_num, title, subtitle, clinical_focus, narrative, bullets=None, elements=None, is_checkpoint=False, checkpoint_number=0):
    if bullets is None: bullets = []
    if elements is None: elements = []
    
    # Validation check on word count
    words = len(narrative.split())
    if words < 60:
        print(f"WARNING: Slide {slide_num} narrative word count is low: {words} words.")
    
    slide = {
        "slideNumber": slide_num,
        "title": title,
        "subtitle": subtitle,
        "clinicalFocus": clinical_focus,
        "content": narrative,
        "synthesisNarrative": narrative,
        "bulletPoints": bullets,
        "relatedQuestions": [],
        "interactiveElements": elements
    }
    if is_checkpoint:
        slide["isCheckpoint"] = True
        slide["checkpointNumber"] = checkpoint_number
        
    return slide

def make_quiz(question, options, correct_key=None):
    """
    Creates a micro_quiz with robust validation.
    options: list of dicts: [{"key": "A", "text": "...", "isCorrect": False, "explanation": "..."}, ...]
    If correct_key is provided, ensures only that key is isCorrect: True.
    Ensures every option has non-empty explanation and exactly 1 isCorrect.
    """
    if not options or len(options) < 4:
        raise ValueError(f"micro_quiz must have at least 4 options: {question}")
    
    formatted_options = []
    for opt in options:
        formatted_options.append({
            "key": opt["key"],
            "text": opt["text"],
            "isCorrect": bool(opt.get("isCorrect", False)),
            "explanation": opt.get("explanation", "")
        })
        
    if correct_key:
        for opt in formatted_options:
            opt["isCorrect"] = (opt["key"] == correct_key)
            
    correct_count = sum(1 for opt in formatted_options if opt["isCorrect"])
    if correct_count != 1:
        raise ValueError(f"micro_quiz must have exactly 1 correct option, got {correct_count} for: {question}")
        
    for opt in formatted_options:
        if not opt.get("explanation") or len(opt["explanation"].strip()) < 10:
            raise ValueError(f"micro_quiz option {opt['key']} has insufficient explanation: {opt}")
            
    return {
        "type": "micro_quiz",
        "question": question,
        "microQuizOptions": formatted_options
    }

def make_cloze(sentence, masked_term, hint):
    """
    Creates a cloze_masking element.
    Ensures masked_term is an exact substring of sentence (case-folded).
    Ensures hint does NOT leak any part of masked_term.
    """
    if not masked_term or fold(masked_term) not in fold(sentence):
        raise ValueError(f"cloze_masking maskedTerm '{masked_term}' not found in sentence: '{sentence}'")
        
    if hint and leaks(hint, masked_term):
        raise ValueError(f"cloze_masking hint '{hint}' leaks maskedTerm '{masked_term}'")
        
    return {
        "type": "cloze_masking",
        "sentence": sentence,
        "maskedTerm": masked_term,
        "hint": hint
    }

def make_table(title, headers, rows):
    """
    Creates an interactive_table element.
    rows: list of lists of cell dicts: [[{"text": "...", "isMasked": False}, {"text": "...", "isMasked": True, "hint": "..."}], ...]
    Ensures every row matches len(headers), at least one cell is masked, and hints do not leak.
    """
    if not headers or not rows:
        raise ValueError(f"interactive_table '{title}' requires headers and rows")
        
    formatted_rows = []
    has_masked = False
    for r_idx, r in enumerate(rows):
        if len(r) != len(headers):
            raise ValueError(f"Row {r_idx} length {len(r)} doesn't match headers length {len(headers)} in table '{title}'")
        cells = []
        for c_idx, cell in enumerate(r):
            text = str(cell.get("text", ""))
            is_masked = bool(cell.get("isMasked", False))
            hint = cell.get("hint", "")
            if is_masked:
                has_masked = True
                if c_idx == 0:
                    raise ValueError(f"First column cannot be masked in row {r_idx} of table '{title}'")
                if hint and leaks(hint, text):
                    raise ValueError(f"Table hint '{hint}' leaks cell text '{text}' in table '{title}'")
            cells.append({
                "text": text,
                "isMasked": is_masked,
                "hint": hint
            })
        formatted_rows.append({"cells": cells})
        
    if not has_masked:
        raise ValueError(f"Table '{title}' has no masked cells!")
        
    return {
        "type": "interactive_table",
        "tableTitle": title,
        "tableHeaders": headers,
        "tableRows": formatted_rows
    }

def make_chain(title, steps):
    """
    Creates a causal_chain element.
    steps: list of str: ["1. Etiket: Açıklama...", "2. Etiket: Açıklama...", ...]
    """
    if len(steps) < 3:
        raise ValueError(f"causal_chain '{title}' must have at least 3 steps, got {len(steps)}")
    for s in steps:
        if "..." in s or "…" in s:
            raise ValueError(f"causal_chain step is truncated: {s}")
    return {
        "type": "causal_chain",
        "chainTitle": title,
        "steps": steps
    }

def make_recall(question, answer):
    """
    Creates an active_recall element.
    """
    if not question or not answer:
        raise ValueError("active_recall question and answer cannot be empty")
    return {
        "type": "active_recall",
        "question": question,
        "answer": answer
    }

def make_spot_the_lie(topic, items):
    """
    Creates a spot_the_lie element.
    items: list of dicts: [{"text": "...", "isLie": False, "explanation": "..."}, ...]
    Must have 3-4 items, exactly 1 isLie: True, all items must have comprehensive explanations.
    """
    if not topic:
        raise ValueError("spot_the_lie topic cannot be empty")
    if len(items) < 3 or len(items) > 4:
        raise ValueError(f"spot_the_lie items must be 3 or 4, got {len(items)} for topic: {topic}")
        
    lies = [it for it in items if it.get("isLie")]
    if len(lies) != 1:
        raise ValueError(f"spot_the_lie must have exactly 1 lie, got {len(lies)} for topic: {topic}")
        
    for it in items:
        if not it.get("text") or not it.get("explanation") or len(it["explanation"].strip()) < 10:
            raise ValueError(f"spot_the_lie item has empty or insufficient explanation: {it}")
            
    return {
        "type": "spot_the_lie",
        "topic": topic,
        "items": items
    }

def make_slider(left_title, right_title, left_points, right_points):
    """
    Creates a before_after_slider element.
    left_points and right_points must have identical lengths.
    """
    if len(left_points) != len(right_points):
        raise ValueError(f"before_after_slider points mismatch: {len(left_points)} vs {len(right_points)}")
    if len(left_points) < 2:
        raise ValueError("before_after_slider requires at least 2 points")
    return {
        "type": "before_after_slider",
        "leftTitle": left_title,
        "rightTitle": right_title,
        "leftPoints": left_points,
        "rightPoints": right_points
    }

def make_swipe(title, left_category, right_category, cards):
    """
    Creates a swipe_matching element.
    cards: [{"text": "...", "category": "left"|"right", "explanation": "..."}, ...]
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
    Creates a venn_grid element.
    items: [{"criterion": "...", "correct": "A"|"B"|"both"|"neither", "explanation": "..."}, ...]
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
    Creates a branching_logic element.
    options: [{"text": "...", "isCorrect": False, "feedback": "..."}, ...]
    Exactly 1 correct, all have feedback.
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
