# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 19: Doğumsal Kadın/Erkek Genital Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)
İnteraktif Öğrenme Destesi Yardımcı Fonksiyonları.
Tüm interaktif öge kurallarına tam uyumludur.
"""

def make_cloze(sentence, masked_term, hint):
    assert masked_term in sentence, f"HATA: '{masked_term}' cümlede birebir bulunamadı: '{sentence}'"
    return {
        "type": "cloze_masking",
        "sentence": sentence,
        "maskedTerm": masked_term,
        "hint": hint
    }

def make_micro_quiz(question, options_dict, correct_key=None, explanations_dict=None):
    if explanations_dict is None:
        explanations_dict = {}
    options = []
    if isinstance(options_dict, list):
        for opt in options_dict:
            if isinstance(opt, dict):
                k = opt.get("key", "")
                text = opt.get("text", "")
                is_corr = opt.get("isCorrect", (k == correct_key) if correct_key else False)
                exp = opt.get("explanation", explanations_dict.get(k, f"{k} seçeneği {'doğrudur' if is_corr else 'yanlıştır'}."))
                options.append({
                    "key": k,
                    "text": text,
                    "isCorrect": is_corr,
                    "explanation": exp
                })
    elif isinstance(options_dict, dict):
        for k, v in options_dict.items():
            is_corr = (k == correct_key)
            exp = explanations_dict.get(k, "")
            if not exp:
                exp = f"{k} seçeneği {'doğrudur' if is_corr else 'yanlıştır'}."
            options.append({
                "key": k,
                "text": v,
                "isCorrect": is_corr,
                "explanation": exp
            })
    return {
        "type": "micro_quiz",
        "question": question,
        "options": options,
        "microQuizOptions": options
    }

def make_table(headers, rows):
    table_rows = []
    for r in rows:
        assert len(r) == len(headers), f"HATA: Tablo satırındaki hücre sayısı ({len(r)}) başlık sayısına ({len(headers)}) eşit olmalıdır!"
        cells = []
        for cell_item in r:
            if isinstance(cell_item, dict):
                text = cell_item.get("text", "")
                is_masked = cell_item.get("isMasked", False)
                hint = cell_item.get("hint", "")
            else:
                text = str(cell_item)
                is_masked = False
                hint = ""
            cells.append({
                "text": text,
                "isMasked": is_masked,
                "hint": hint
            })
        table_rows.append({"cells": cells})
    return {
        "type": "interactive_table",
        "headers": headers,
        "rows": table_rows
    }

def make_before_after(title, before_label, before_desc, after_label, after_desc):
    left_points = [before_desc] if isinstance(before_desc, str) else list(before_desc)
    right_points = [after_desc] if isinstance(after_desc, str) else list(after_desc)
    assert len(left_points) == len(right_points), f"HATA: Sol ({len(left_points)}) ve sağ ({len(right_points)}) madde sayıları eşit olmalıdır!"
    return {
        "type": "before_after_slider",
        "title": title,
        "leftTitle": before_label,
        "rightTitle": after_label,
        "leftPoints": left_points,
        "rightPoints": right_points,
        "beforeState": {
            "label": before_label,
            "description": left_points[0] if left_points else ""
        },
        "afterState": {
            "label": after_label,
            "description": right_points[0] if right_points else ""
        }
    }

def make_causal_chain(title, steps):
    assert 3 <= len(steps) <= 6, f"HATA: Mekanizma zinciri 3-6 basamak olmalıdır, gelen: {len(steps)}"
    for s in steps:
        assert not s.endswith("...") and not s.endswith("…"), f"HATA: Zincir adımı üç nokta ile bitemez: '{s}'"
    return {
        "type": "causal_chain",
        "title": title,
        "steps": steps
    }

def make_active_recall(question, answer, clue=""):
    return {
        "type": "active_recall",
        "question": question,
        "answer": answer,
        "clue": clue
    }

def make_branching_logic(scenario, *args):
    if len(args) == 1:
        options = args[0]
    elif len(args) == 2:
        question, options = args
        scenario = f"{scenario}\n\n**Soru:** {question}"
    else:
        raise ValueError("make_branching_logic expects (scenario, options) or (scenario, question, options)")

    assert len(options) >= 2, f"HATA: Dallanan mantık en az 2 seçenek içermelidir: {len(options)}"
    correct_count = sum(1 for o in options if o.get("isCorrect") or o.get("isOptimal"))
    assert correct_count == 1, f"HATA: Dallanan mantıkta tam 1 doğru seçenek olmalıdır! Bulunan: {correct_count}"
    
    for o in options:
        if "isCorrect" in o and "isOptimal" not in o:
            o["isOptimal"] = o["isCorrect"]
        elif "isOptimal" in o and "isCorrect" not in o:
            o["isCorrect"] = o["isOptimal"]

    return {
        "type": "branching_logic",
        "scenario": scenario,
        "options": options,
        "branchingOptions": options
    }

def make_flashcard(id_str, front, back, hint, category):
    return {
        "id": id_str,
        "front": front,
        "back": back,
        "hint": hint,
        "category": category
    }

# Aliases
make_quiz = make_micro_quiz
make_slider = make_before_after
make_chain = make_causal_chain
make_recall = make_active_recall
make_branching = make_branching_logic
