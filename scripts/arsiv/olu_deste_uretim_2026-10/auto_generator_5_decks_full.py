import sys, os, json, re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from meds.scripts.auto_build_5_decks_full import build_deck_from_spec_complete

# Helper to construct high-quality, syllabus-faithful items
def make_item(title, subtitle, lead, b1_h, b1_t, b2_h, b2_t, b3_h, b3_t, alert, sum1, sum2, sum3,
              cloze_s, cloze_t, cloze_h,
              tbl_t, h1, h2, h3, r1_1, r1_2, r1_3, r1_m, r2_1, r2_2, r2_3, r2_m,
              ch_t, st1, st2, st3, st4,
              rec_q, rec_a,
              spot_top, lie_idx, t1, e1, t2, e2, t3, e3, t4, e4,
              q_text, optA, eA, optB, eB, optC, eC, optD, eD, correct_key):
    
    bullets = [(b1_h, b1_t), (b2_h, b2_t), (b3_h, b3_t)]
    summaries = [sum1, sum2, sum3]
    
    tbl_rows = [
        {"cells": [{"text": r1_1, "isMasked": False}, {"text": r1_2, "isMasked": (r1_m == 2), "hint": "Klinik değerlendirme kriteri"}, {"text": r1_3, "isMasked": (r1_m == 3), "hint": "Klinik değerlendirme kriteri"}]},
        {"cells": [{"text": r2_1, "isMasked": False}, {"text": r2_2, "isMasked": (r2_m == 2), "hint": "Klinik değerlendirme kriteri"}, {"text": r2_3, "isMasked": (r2_m == 3), "hint": "Klinik değerlendirme kriteri"}]}
    ]
    
    spot_items = [
        {"text": t1, "isLie": (lie_idx == 1), "explanation": e1},
        {"text": t2, "isLie": (lie_idx == 2), "explanation": e2},
        {"text": t3, "isLie": (lie_idx == 3), "explanation": e3},
        {"text": t4, "isLie": (lie_idx == 4), "explanation": e4}
    ]
    
    quiz_opts = [
        {"key": "A", "text": optA, "isCorrect": (correct_key == "A"), "explanation": eA},
        {"key": "B", "text": optB, "isCorrect": (correct_key == "B"), "explanation": eB},
        {"key": "C", "text": optC, "isCorrect": (correct_key == "C"), "explanation": eC},
        {"key": "D", "text": optD, "isCorrect": (correct_key == "D"), "explanation": eD}
    ]
    
    return {
        "title": title,
        "subtitle": subtitle,
        "lead": lead,
        "bullets": bullets,
        "alert": alert,
        "summaries": summaries,
        "cloze": [cloze_s, cloze_t, cloze_h],
        "table": {"title": tbl_t, "headers": [h1, h2, h3], "rows": tbl_rows},
        "chain": {"title": ch_t, "steps": [st1, st2, st3, st4]},
        "recall": {"q": rec_q, "a": rec_a},
        "spot": {"topic": spot_top, "items": spot_items},
        "quiz": {"q": q_text, "opts": quiz_opts}
    }

print("make_item definition complete.")
