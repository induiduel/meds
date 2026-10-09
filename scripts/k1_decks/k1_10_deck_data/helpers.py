"""
Kromozomal Hastalıklar ve Genetik Danışma (Kurul 1 - Ders 10)
İnteraktif Öğrenme Destesi Yardımcı Fonksiyonları.
Tüm interaktif öge kurallarına (OGREN_ETKILESIM_REHBERI ve validate_learning_decks.py) tam uyumludur.
"""

def make_cloze(sentence, masked_term, hint):
    """
    Boşluk doldurma (cloze_masking).
    maskedTerm cümlede birebir geçmelidir.
    hint asla maskedTerm kelimelerini veya sayılarını sızdırmamalıdır.
    """
    assert masked_term in sentence, f"HATA: '{masked_term}' cümlede birebir bulunamadı: '{sentence}'"
    return {
        "type": "cloze_masking",
        "sentence": sentence,
        "maskedTerm": masked_term,
        "hint": hint
    }

def make_micro_quiz(question, options_dict, correct_key, explanations_dict):
    """
    Mikro soru (micro_quiz).
    options_dict: {"A": "...", "B": "...", "C": "...", "D": "...", "E": "..."}
    correct_key: "B"
    explanations_dict: {"A": "...", "B": "...", ...}
    """
    options = []
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
    """
    İnteraktif maskeli tablo (interactive_table).
    rows:
      1) [ {"cells": ["c1", "c2", ...], "hiddenIndex": 1, "hint": "..."} ]
      2) [ [ ("c1", False, ""), ("c2", True, "hint"), ... ] ]
      3) [ [ {"text": "c1", "isMasked": False}, {"text": "c2", "isMasked": True, "hint": "..."}, ... ] ]
    """
    table_rows = []
    for r in rows:
        cells = []
        if isinstance(r, dict) and "cells" in r:
            raw_cells = r["cells"]
            if len(raw_cells) < len(headers):
                raw_cells = list(raw_cells) + ["—"] * (len(headers) - len(raw_cells))
            elif len(raw_cells) > len(headers):
                raw_cells = list(raw_cells)[:len(headers)]
            
            hidden_idx = r.get("hiddenIndex", 1)
            row_hint = r.get("hint", "")
            for idx, c_text in enumerate(raw_cells):
                is_m = (idx == hidden_idx)
                cells.append({
                    "text": str(c_text),
                    "isMasked": is_m,
                    "hint": row_hint if is_m else ""
                })
        elif isinstance(r, (list, tuple)):
            for cell_item in r:
                if isinstance(cell_item, dict):
                    cells.append(cell_item)
                elif isinstance(cell_item, (list, tuple)):
                    text = cell_item[0]
                    is_m = cell_item[1] if len(cell_item) > 1 else False
                    hint = cell_item[2] if len(cell_item) > 2 else ""
                    cells.append({
                        "text": str(text),
                        "isMasked": is_m,
                        "hint": hint if is_m else ""
                    })
                else:
                    cells.append({
                        "text": str(cell_item),
                        "isMasked": False,
                        "hint": ""
                    })
            if len(cells) < len(headers):
                cells = list(cells) + [{"text": "—", "isMasked": False, "hint": ""}] * (len(headers) - len(cells))
            elif len(cells) > len(headers):
                cells = list(cells)[:len(headers)]
        
        table_rows.append({"cells": cells})

    return {
        "type": "interactive_table",
        "tableHeaders": headers,
        "tableRows": table_rows
    }

def make_before_after(*args):
    """
    Karşılaştırma / Değişim kaydırıcısı (before_after_slider).
    Kabul eder:
      make_before_after(title, before_label, before_desc, after_label, after_desc)
      make_before_after(before_label, before_desc, after_label, after_desc)
    """
    if len(args) == 5:
        title, before_label, before_desc, after_label, after_desc = args
    elif len(args) == 4:
        title = "Karşılaştırma Analizi"
        before_label, before_desc, after_label, after_desc = args
    else:
        raise ValueError(f"make_before_after 4 veya 5 argüman almalıdır, verilen: {len(args)}")

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
        "beforeLabel": before_label,
        "afterLabel": after_label,
        "beforePoints": left_points,
        "afterPoints": right_points,
        "beforeState": {
            "label": before_label,
            "description": left_points[0] if left_points else ""
        },
        "afterState": {
            "label": after_label,
            "description": right_points[0] if right_points else ""
        }
    }

make_slider = make_before_after

def make_causal_chain(title, steps):
    """
    Mekanizma zinciri (causal_chain).
    steps: 3 ila 6 elemanlı liste. Her biri 'N. Başlık: Tam açıklama cümlesi' formatında.
    """
    assert 3 <= len(steps) <= 6, f"HATA: causal_chain basamak sayısı 3-6 arasında olmalıdır: {len(steps)}"
    for s in steps:
        assert not s.endswith("...") and not s.endswith("…"), f"HATA: Zincir basamağı üç nokta ile bitemez: '{s}'"
    return {
        "type": "causal_chain",
        "title": title,
        "steps": steps
    }

def make_active_recall(question, answer, hint=None):
    """
    Aktif hatırlama (active_recall).
    """
    assert not answer.endswith("...") and not answer.endswith("…"), f"HATA: active_recall cevabı üç nokta ile bitemez: '{answer}'"
    assert not question.endswith("...") and not question.endswith("…"), f"HATA: active_recall sorusu üç nokta ile bitemez: '{question}'"
    item = {
        "type": "active_recall",
        "question": question,
        "answer": answer
    }
    if hint:
        item["hint"] = hint
    return item

def make_branching_logic(scenario, options):
    """
    Dallanan klinik karar senaryosu.
    """
    for o in options:
        if "isCorrect" in o and "isOptimal" not in o:
            o["isOptimal"] = o["isCorrect"]
        elif "isOptimal" in o and "isCorrect" not in o:
            o["isCorrect"] = o["isOptimal"]
    correct_count = sum(1 for o in options if o.get("isCorrect"))
    assert correct_count == 1, f"HATA: branching_logic tam olarak 1 doğru cevap içermelidir: {correct_count}"
    assert len(options) >= 2, "HATA: branching_logic en az 2 seçenek içermelidir"
    return {
        "type": "branching_logic",
        "scenario": scenario,
        "options": options,
        "branchingOptions": options
    }

def make_flashcard(card_id, front, back, hint="", category="Kromozomal Hastalıklar"):
    return {
        "id": card_id,
        "front": front,
        "back": back,
        "hint": hint,
        "category": category
    }
