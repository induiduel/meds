# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 24: Emboli, Enfarktüs ve Şok
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Yardımcı Fonksiyonlar ve İnteraktif Eleman Üreteçleri
"""

import re

def normalize_text(text):
    text = text.lower()
    text = text.replace('i̇', 'i').replace('ı', 'i').replace('ş', 's').replace('ğ', 'g').replace('ü', 'u').replace('ö', 'o').replace('ç', 'c')
    return re.sub(r'[^a-z0-9]', ' ', text)

def has_stem_leak(hint, answer):
    if not hint or not answer:
        return False
    # Sayı kontrolü
    for d in re.findall(r"\b\d+\b", answer):
        if re.search(r"\b" + re.escape(d) + r"\b", hint):
            return True
    # 4 harfli kök kontrolü
    h_words = normalize_text(hint).split()
    a_words = normalize_text(answer).split()
    stop_words = {"ve", "veya", "ile", "icin", "olan", "bir", "bu", "su", "da", "de", "ise", "en", "cok", "daha", "kadar"}
    h_stems = {w[:4] for w in h_words if len(w) >= 4 and w not in stop_words}
    a_stems = {w[:4] for w in a_words if len(w) >= 4 and w not in stop_words}
    overlap = h_stems.intersection(a_stems)
    return len(overlap) > 0

def make_cloze(sentence, maskedTerm, hint):
    assert maskedTerm in sentence, f"HATA: Maskelenen terim ('{maskedTerm}') cümle içinde bulunamadı: '{sentence}'"
    assert not hint.endswith("...") and not hint.endswith("…"), f"HATA: İpucu üç nokta ile bitemez: '{hint}'"
    return {
        "type": "cloze_masking",
        "sentence": sentence,
        "maskedTerm": maskedTerm,
        "hint": hint
    }

def make_micro_quiz(question, options_dict, correct_key=None, explanations_dict=None):
    single_exp = ""
    if isinstance(explanations_dict, str):
        single_exp = explanations_dict
        explanations_dict = {}
    elif explanations_dict is None:
        explanations_dict = {}
        
    options = []
    if isinstance(options_dict, list):
        for opt in options_dict:
            if isinstance(opt, dict):
                k = opt.get("key", "")
                text = opt.get("text", "")
                is_corr = opt.get("isCorrect", (k == correct_key) if correct_key else False)
                exp = opt.get("explanation", "")
                if not exp:
                    if is_corr and single_exp:
                        exp = single_exp
                    else:
                        exp = explanations_dict.get(k, f"{k} seçeneği {'doğrudur' if is_corr else 'yanlıştır'}.")
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
                if is_corr and single_exp:
                    exp = single_exp
                else:
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

def make_table(*args, **kwargs):
    title = kwargs.get("title", "")
    hidden_coords = kwargs.get("hidden_coords", None)
    hints = kwargs.get("hints", None)
    
    if len(args) == 2:
        headers, raw_rows = args
    elif len(args) == 3:
        title, headers, raw_rows = args
    elif len(args) == 4:
        title, headers, raw_rows, hidden_coords = args
    elif len(args) == 5:
        title, headers, raw_rows, hidden_coords, hints = args
    else:
        raise ValueError(f"make_table invalid args: {len(args)}")

    table_rows = []
    hint_idx = 0
    for r_idx, r in enumerate(raw_rows):
        assert len(r) == len(headers), f"HATA: Tablo satırındaki hücre sayısı ({len(r)}) başlık sayısına ({len(headers)}) eşit olmalıdır!"
        cells = []
        for c_idx, cell_item in enumerate(r):
            if isinstance(cell_item, dict):
                text = cell_item.get("text", "")
                is_masked = cell_item.get("isMasked", False)
                hint = cell_item.get("hint", "")
            else:
                text = str(cell_item)
                is_masked = False
                hint = ""
                if hidden_coords and (r_idx, c_idx) in hidden_coords:
                    is_masked = True
                    if hints and hint_idx < len(hints):
                        hint = hints[hint_idx]
                        hint_idx += 1
            cells.append({
                "text": text,
                "isMasked": is_masked,
                "hint": hint
            })
        table_rows.append({"cells": cells})
    
    res = {
        "type": "interactive_table",
        "headers": headers,
        "rows": table_rows,
        "tableHeaders": headers,
        "tableRows": table_rows
    }
    if title:
        res["title"] = title
    return res

def make_before_after(title, *args, **kwargs):
    if len(args) == 2:
        before_label = "Önceki / Riskli Durum"
        before_desc = args[0]
        after_label = "Sonraki / Hedef Durum"
        after_desc = args[1]
    elif len(args) >= 4:
        before_label = args[0]
        before_desc = args[1]
        after_label = args[2]
        after_desc = args[3]
    else:
        raise ValueError("make_before_after requires (title, before_desc, after_desc) or (title, before_label, before_desc, after_label, after_desc)")

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
        if "feedback" not in o and "explanation" in o:
            o["feedback"] = o["explanation"]

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
