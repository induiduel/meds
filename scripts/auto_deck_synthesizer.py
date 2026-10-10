import sys, os, json, re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from meds.scripts.auto_curriculum_compiler import build_complete_deck

# Synthesizer builds 10 structured sections per deck
def synthesize_section(sec_idx, sec_title, slide_blueprints):
    assert len(slide_blueprints) == 10, f"Section {sec_title} must have 10 slides, got {len(slide_blueprints)}"
    sec_num = sec_idx + 1
    topics = []
    
    for top_idx, b in enumerate(slide_blueprints):
        slide_idx = sec_idx * 10 + top_idx + 1
        is_cp = (slide_idx % 10 == 0)
        
        title = b["title"] if not is_cp else f"[TEKRAR SAYFASI - CHECKPOINT {sec_num}] {sec_title}"
        subtitle = b["subtitle"]
        focus = b.get("focus", "Klinik Patoloji")
        lead = b["lead"]
        bullets = b["bullets"] # list of (header, text)
        alert = b["alert"]
        summaries = b["summaries"]
        
        # Interactives
        cloze_s, cloze_t, cloze_h = b["cloze"]
        tbl_t, tbl_h, tbl_rows = b["table"]
        ch_t, ch_steps = b["chain"]
        rec_q, rec_a = b["recall"]
        spot_top, spot_items = b["spot"]
        quiz_q, quiz_opts = b["quiz"]
        
        topics.append({
            "title": title,
            "subtitle": subtitle,
            "focus": focus,
            "lead": lead,
            "bullets": bullets,
            "alert_type": "IMPORTANT" if is_cp else "NOTE",
            "alert_text": alert,
            "summaries": summaries,
            "cloze_s": cloze_s,
            "cloze_t": cloze_t,
            "cloze_h": cloze_h,
            "tbl_title": tbl_t,
            "tbl_headers": tbl_h,
            "tbl_rows": tbl_rows,
            "chain_title": ch_t,
            "chain_steps": ch_steps,
            "rec_q": rec_q,
            "rec_a": rec_a,
            "spot_topic": spot_top,
            "spot_items": spot_items,
            "quiz_q": quiz_q,
            "quiz_opts": quiz_opts
        })
        
    return {
        "section_title": sec_title,
        "topics": topics
    }

print("Synthesizer ready.")
