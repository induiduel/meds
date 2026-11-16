"""
Hücre İçi Birikimler ve Kalsifikasyonlar (Ders 7) İnteraktif Öğrenme Destesi Yardımcı Fonksiyonları.
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
    rows: [
      [ ("Açık Metin", False, ""), ("Gizli Metin", True, "İpucu") ]
    ]
    """
    table_rows = []
    for r in rows:
        cells = []
        for cell_tuple in r:
            text = cell_tuple[0]
            is_masked = cell_tuple[1]
            hint = cell_tuple[2] if len(cell_tuple) > 2 else ""
            cells.append({
                "text": text,
                "isMasked": is_masked,
                "hint": hint
            })
        table_rows.append({"cells": cells})
    return {
        "type": "interactive_table",
        "tableHeaders": headers,
        "tableRows": table_rows
    }

def make_before_after(title, before_label, before_desc, after_label, after_desc):
    """
    Karşılaştırma / Değişim kaydırıcısı (before_after_slider).
    Hem doğrulayıcı (leftTitle, rightTitle, leftPoints, rightPoints)
    hem de UI (beforeState, afterState) şemasını destekler.
    """
    left_points = [before_desc] if isinstance(before_desc, str) else list(before_desc)
    right_points = [after_desc] if isinstance(after_desc, str) else list(after_desc)
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
    """
    Mekanizma zinciri (causal_chain).
    steps: 3 ila 6 elemanlı liste. Her biri 'N. Başlık: Tam açıklama cümlesi' formatında.
    """
    assert 3 <= len(steps) <= 6, f"HATA: causal_chain basamak sayısı 3-6 arasında olmalıdır: {len(steps)}"
    return {
        "type": "causal_chain",
        "title": title,
        "steps": steps
    }

def make_active_recall(question, answer):
    """
    Aktif hatırlama (active_recall).
    """
    assert not answer.endswith("...") and not answer.endswith("…"), f"HATA: active_recall cevabı üç nokta ile bitemez: '{answer}'"
    return {
        "type": "active_recall",
        "question": question,
        "answer": answer
    }

def make_branching_logic(scenario, options):
    """
    Dallanan klinik karar senaryosu.
    options: [
        {"text": "...", "isCorrect": False, "feedback": "..."},
        {"text": "...", "isCorrect": True, "feedback": "..."}
    ]
    """
    correct_count = sum(1 for o in options if o.get("isCorrect"))
    assert correct_count == 1, f"HATA: branching_logic tam olarak 1 doğru cevap içermelidir: {correct_count}"
    assert len(options) >= 2, "HATA: branching_logic en az 2 seçenek içermelidir"
    return {
        "type": "branching_logic",
        "scenario": scenario,
        "options": options,
        "branchingOptions": options
    }

def make_flashcard(card_id, front, back, hint="", category="Hücre İçi Birikimler ve Kalsifikasyonlar"):
    return {
        "id": card_id,
        "front": front,
        "back": back,
        "hint": hint,
        "category": category
    }
