#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helper constructors for Lesson 2 (Patolojiye Giriş) interactive elements.
Strictly conforms to meds/docs/OGREN_ETKILESIM_REHBERI.md and validate_learning_decks.py.
"""

def make_micro_quiz(question, options_dict, correct_key, explanations_dict):
    """
    question: Soru kökü
    options_dict: {'A': 'Metin', 'B': 'Metin', ...}
    correct_key: 'A' | 'B' | 'C' | 'D' | 'E'
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
        "microQuizOptions": options
    }

def make_interactive_table(title, headers, rows_data):
    """
    rows_data: list of rows where each row is a list of tuples:
    [
        [ ("Hücre", False), ("44", True, "22 çift"), ("Açıklama", False) ]
    ]
    or dicts: {"text": "...", "isMasked": True, "hint": "..."}
    """
    formatted_rows = []
    for row in rows_data:
        cells = []
        for cell in row:
            if isinstance(cell, tuple):
                text = cell[0]
                is_masked = cell[1] if len(cell) > 1 else False
                hint = cell[2] if len(cell) > 2 else ""
                cells.append({"text": str(text), "isMasked": is_masked, "hint": str(hint)})
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

def make_cloze(sentence, masked_term, hint=""):
    """
    sentence: Cümle (masked_term cümlede BİREBİR geçmelidir)
    masked_term: Gizlenecek terim
    hint: İpucu (cevabın hiçbir kelimesini içermez)
    """
    return {
        "type": "cloze_masking",
        "sentence": sentence,
        "maskedTerm": masked_term,
        "hint": hint
    }

def make_before_after(title, left_title, right_title, left_points, right_points):
    """
    Karşılaştırma kaydırıcısı / Ayırıcı tanı tablosu.
    left_points ve right_points eşit sayıda madde içermelidir.
    """
    return {
        "type": "before_after_slider",
        "title": title,
        "leftTitle": left_title,
        "rightTitle": right_title,
        "leftPoints": left_points,
        "rightPoints": right_points
    }

def make_causal_chain(title, steps):
    """
    Mekanizma basamakları zinciri.
    steps: ["1. Etiket: tam cümle", "2. Etiket: tam cümle", ...]
    """
    return {
        "type": "causal_chain",
        "chainTitle": title,
        "steps": steps
    }

def make_active_recall(question, answer):
    """
    question: Soru metni
    answer: Cevap metni
    """
    return {
        "type": "active_recall",
        "question": question,
        "answer": answer
    }

def make_branching_logic(scenario, options):
    """
    Dallanan klinik karar senaryosu.
    options: [{"text": "...", "isCorrect": True/False, "feedback": "..."}, ...]
    """
    return {
        "type": "branching_logic",
        "scenario": scenario,
        "options": options
    }

def make_flashcard(card_id, front, back, hint="", category="Klinik Patoloji"):
    """
    Akıl kartı constructor.
    """
    return {
        "id": card_id,
        "front": front,
        "back": back,
        "hint": hint,
        "category": category
    }
