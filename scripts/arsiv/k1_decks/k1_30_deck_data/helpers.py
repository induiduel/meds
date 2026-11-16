# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 30: İleri Tümör Genetiği ve Metabolizması
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Yardımcı Fonksiyonlar ve Şablon Üreticiler.
"""

def make_cloze(sentence, masked_term, hint=""):
    assert masked_term in sentence, f"HATA: '{masked_term}' hedef cümlede yer almıyor: {sentence}"
    return {
        "type": "cloze_masking",
        "sentence": sentence,
        "maskedTerm": masked_term,
        "hint": hint
    }

def make_micro_quiz(question, options, explanation=""):
    assert len(options) in (4, 5), f"HATA: Şık sayısı 4 veya 5 olmalı, bulunan: {len(options)}"
    correct_count = sum(1 for o in options if o.get("isCorrect"))
    assert correct_count == 1, f"HATA: Tam olarak 1 doğru şık olmalı, bulunan: {correct_count}"
    for idx, opt in enumerate(options):
        assert opt.get("explanation"), f"HATA: {idx}. seçeneğin açıklaması boş olamaz!"
    return {
        "type": "micro_quiz",
        "question": question,
        "options": options,
        "explanation": explanation
    }

def make_table(title, headers, rows):
    assert len(headers) >= 2, "HATA: En az 2 başlık olmalı"
    assert len(rows) >= 2, "HATA: En az 2 satır olmalı"
    for r in rows:
        assert len(r.get("cells", [])) == len(headers), "HATA: Hücre sayısı başlık sayısına eşit olmalı"
        assert r.get("hiddenIndex") is not None, "HATA: hiddenIndex belirtilmeli"
        assert r.get("hint"), "HATA: İpucu belirtilmeli"
    return {
        "type": "interactive_table",
        "title": title,
        "headers": headers,
        "rows": rows
    }

def make_before_after(title, before_title, before_text, after_title, after_text, clinical_significance):
    return {
        "type": "before_after_slider",
        "title": title,
        "beforeTitle": before_title,
        "beforeText": before_text,
        "afterTitle": after_title,
        "afterText": after_text,
        "clinicalSignificance": clinical_significance
    }

def make_causal_chain(title, steps):
    assert 3 <= len(steps) <= 6, f"HATA: Basamak sayısı 3-6 olmalı, bulunan: {len(steps)}"
    for s in steps:
        assert ":" in s, f"HATA: Basamak 'N. Etiket: Açıklama' biçiminde olmalı: {s}"
    return {
        "type": "causal_chain",
        "title": title,
        "steps": steps
    }

def make_active_recall(question, answer, hint=""):
    return {
        "type": "active_recall",
        "question": question,
        "answer": answer,
        "hint": hint
    }

def make_branching_logic(scenario, question, choices):
    assert len(choices) >= 2, "HATA: En az 2 seçenek olmalı"
    correct_count = sum(1 for c in choices if c.get("isCorrect"))
    assert correct_count == 1, "HATA: Tam olarak 1 doğru seçenek olmalı"
    for c in choices:
        assert c.get("explanation"), "HATA: Her seçeneğin gerekçesi olmalı"
    return {
        "type": "branching_logic",
        "scenario": scenario,
        "question": question,
        "choices": choices
    }
