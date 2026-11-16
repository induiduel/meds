import sys, os, json, re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from meds.scripts.apply_generated_deck import apply_deck
from meds.scripts.generate_deck_core import sanitize_deck
from meds.scripts.generate_deck_util import make_slide
from meds.scripts.auto_build_5_decks import create_100_slide_deck

def build_curriculum_deck(meta, concepts):
    deck_id = meta["id"]
    print(f"Compiling curriculum deck {deck_id} (100 slides, 30 flashcards)...")
    
    sections = []
    # concepts is a list of 10 section dictionaries. Each has "title" and "subtopics" (list of 10 items)
    assert len(concepts) == 10, f"Expected 10 sections, got {len(concepts)}"
    
    for sec_idx, sec in enumerate(concepts):
        sec_num = sec_idx + 1
        sec_title = sec["title"]
        subtopics = sec["subtopics"]
        assert len(subtopics) == 10, f"Expected 10 subtopics in section {sec_num}, got {len(subtopics)}"
        
        topics_data = []
        for top_idx, st in enumerate(subtopics):
            slide_idx = sec_idx * 10 + top_idx + 1
            is_cp = (slide_idx % 10 == 0)
            
            top_title = st["title"] if not is_cp else f"[TEKRAR SAYFASI - CHECKPOINT {sec_num}] {sec_title}"
            subtitle = st["subtitle"]
            focus = st.get("focus", meta["discipline"])
            lead = st["lead"]
            bullets = st["bullets"]
            alert_type = "IMPORTANT" if is_cp else "NOTE"
            alert_text = st["alert"]
            summaries = st["summaries"]
            
            # Interactive elements
            cloze_s = st["cloze"][0]
            cloze_t = st["cloze"][1]
            cloze_h = st["cloze"][2]
            
            tbl_title = st["table"]["title"]
            tbl_headers = st["table"]["headers"]
            tbl_rows = st["table"]["rows"]
            
            chain_title = st["chain"]["title"]
            chain_steps = st["chain"]["steps"]
            
            rec_q = st["recall"]["q"]
            rec_a = st["recall"]["a"]
            
            spot_topic = st["spot"]["topic"]
            spot_items = st["spot"]["items"]
            
            quiz_q = st["quiz"]["q"]
            quiz_opts = st["quiz"]["opts"]
            
            topics_data.append({
                "title": top_title,
                "subtitle": subtitle,
                "focus": focus,
                "lead": lead,
                "bullets": bullets,
                "alert_type": alert_type,
                "alert_text": alert_text,
                "summaries": summaries,
                "cloze_s": cloze_s,
                "cloze_t": cloze_t,
                "cloze_h": cloze_h,
                "tbl_title": tbl_title,
                "tbl_headers": tbl_headers,
                "tbl_rows": tbl_rows,
                "chain_title": chain_title,
                "chain_steps": chain_steps,
                "rec_q": rec_q,
                "rec_a": rec_a,
                "spot_topic": spot_topic,
                "spot_items": spot_items,
                "quiz_q": quiz_q,
                "quiz_opts": quiz_opts
            })
            
        sections.append({
            "section_title": sec_title,
            "topics": topics_data
        })
        
    deck = create_100_slide_deck(
        deck_id=meta["id"],
        title=meta["title"],
        short_title=meta["shortTitle"],
        desc=meta["description"],
        discipline=meta["discipline"],
        source_pdf=meta["sourcePdf"],
        overview=meta["overview"],
        pearls=meta["pearls"],
        outcomes=meta["outcomes"],
        flashcards=meta["flashcards"],
        outline_10_sections=sections
    )
    
    return deck

print("Curriculum compiler engine ready.")
