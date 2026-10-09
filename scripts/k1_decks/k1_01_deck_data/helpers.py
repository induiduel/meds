#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helper constructors for rich interactive elements in Deck 1
"""

def make_micro_quiz(question, options_dict, correct_key, explanations_dict):
    """
    options_dict: {'A': 'Metin', 'B': 'Metin', 'C': 'Metin', 'D': 'Metin'}
    explanations_dict: {'A': 'Açıklama...', 'B': 'Açıklama...', ...}
    """
    options = []
    for k in sorted(options_dict.keys()):
        options.append({
            "key": k,
            "text": options_dict[k],
            "isCorrect": (k == correct_key),
            "explanation": explanations_dict.get(k, "Detaylı klinik açıklama.")
        })
    return {
        "type": "micro_quiz",
        "question": question,
        "sentence": question,
        "microQuizOptions": options
    }

def make_interactive_table(title, headers, rows_data):
    """
    rows_data: list of lists of tuples or dicts:
    [
        [ ("Otozom", False), ("44", True, "22 çift"), ("Otozomal genleri taşır", False) ],
        ...
    ]
    or list of cell dicts: {"text": "...", "isMasked": True, "hint": "..."}
    """
    formatted_rows = []
    for row in rows_data:
        cells = []
        for cell in row:
            if isinstance(cell, tuple):
                text = cell[0]
                is_masked = cell[1] if len(cell) > 1 else False
                hint = cell[2] if len(cell) > 2 else ""
                cells.append({"text": text, "isMasked": is_masked, "hint": hint})
            elif isinstance(cell, dict):
                cells.append(cell)
            else:
                cells.append({"text": str(cell), "isMasked": False})
        formatted_rows.append({"cells": cells})

    return {
        "type": "interactive_table",
        "tableTitle": title,
        "tableHeaders": headers,
        "tableRows": formatted_rows
    }

def make_cloze(sentence, masked_term, hint="", explanation=""):
    res = {
        "type": "cloze_masking",
        "sentence": sentence,
        "maskedTerm": masked_term,
        "hint": hint
    }
    if explanation:
        res["explanation"] = explanation
    return res

def make_before_after(*args, **kwargs):
    if len(args) == 5:
        title, left_title, right_title, left_points, right_points = args
        return {
            "type": "before_after_slider",
            "title": title,
            "leftTitle": left_title,
            "rightTitle": right_title,
            "leftPoints": left_points,
            "rightPoints": right_points
        }
    elif len(args) == 4:
        left_title, right_title, left_points, right_points = args
        return {
            "type": "before_after_slider",
            "leftTitle": left_title,
            "rightTitle": right_title,
            "leftPoints": left_points,
            "rightPoints": right_points
        }
    else:
        raise ValueError(f"make_before_after expects 4 or 5 positional arguments, got {len(args)}")

def make_causal_chain(title, steps):
    return {
        "type": "causal_chain",
        "chainTitle": title,
        "steps": steps
    }

def make_active_recall(*args, **kwargs):
    if len(args) == 3:
        title, question, answer = args
        return {
            "type": "active_recall",
            "title": title,
            "question": question,
            "answer": answer
        }
    elif len(args) == 2:
        question, answer = args
        return {
            "type": "active_recall",
            "question": question,
            "answer": answer
        }
    else:
        raise ValueError(f"make_active_recall expects 2 or 3 positional arguments, got {len(args)}")

def make_branching_logic(scenario, options_list):
    """
    options_list: list of dicts with keys 'text', 'isCorrect', 'feedback'
    """
    return {
        "type": "branching_logic",
        "scenario": scenario,
        "options": options_list
    }

def make_flashcard(card_id, front, back, hint="", category="Klinik Sentez"):
    return {
        "id": card_id,
        "front": front,
        "back": back,
        "hint": hint,
        "category": category,
        "difficulty": "medium",
        "mastered": False
    }
