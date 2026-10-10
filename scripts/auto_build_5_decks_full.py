import sys, os, json, re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from meds.scripts.apply_generated_deck import apply_deck
from meds.scripts.generate_deck_core import sanitize_deck
from meds.scripts.generate_deck_util import make_slide
from meds.scripts.auto_build_5_decks import create_100_slide_deck

def build_deck_from_spec_complete(deck_spec):
    deck_id = deck_spec["id"]
    print(f"\n==========================================")
    print(f"Building: {deck_id} (100 slides, 30 flashcards)...")
    print(f"Title: {deck_spec['title']}")
    print(f"==========================================")
    
    sections = []
    for s_idx, sec in enumerate(deck_spec["sections"]):
        sec_num = s_idx + 1
        sec_title = sec["title"]
        items = sec["items"]
        assert len(items) == 10, f"Section {sec_num} must have 10 items, got {len(items)}"
        
        topics = []
        for top_idx, it in enumerate(items):
            slide_idx = s_idx * 10 + top_idx + 1
            is_cp = (slide_idx % 10 == 0)
            
            title = it["title"] if not is_cp else f"[TEKRAR SAYFASI - CHECKPOINT {sec_num}] {sec_title}"
            subtitle = it["subtitle"]
            focus = it.get("focus", deck_spec["discipline"])
            lead = it["lead"]
            bullets = it["bullets"]
            alert = it["alert"]
            summaries = it["summaries"]
            
            topics.append({
                "title": title,
                "subtitle": subtitle,
                "focus": focus,
                "lead": lead,
                "bullets": bullets,
                "alert_type": "IMPORTANT" if is_cp else "NOTE",
                "alert_text": alert,
                "summaries": summaries,
                "cloze_s": it["cloze"][0],
                "cloze_t": it["cloze"][1],
                "cloze_h": it["cloze"][2],
                "tbl_title": it["table"]["title"],
                "tbl_headers": it["table"]["headers"],
                "tbl_rows": it["table"]["rows"],
                "chain_title": it["chain"]["title"],
                "chain_steps": it["chain"]["steps"],
                "rec_q": it["recall"]["q"],
                "rec_a": it["recall"]["a"],
                "spot_topic": it["spot"]["topic"],
                "spot_items": it["spot"]["items"],
                "quiz_q": it["quiz"]["q"],
                "quiz_opts": it["quiz"]["opts"]
            })
            
        sections.append({
            "section_title": sec_title,
            "topics": topics
        })
        
    deck = create_100_slide_deck(
        deck_id=deck_id,
        title=deck_spec["title"],
        short_title=deck_spec["shortTitle"],
        desc=deck_spec["description"],
        discipline=deck_spec["discipline"],
        source_pdf=deck_spec["sourcePdf"],
        overview=deck_spec["overview"],
        pearls=deck_spec["pearls"],
        outcomes=deck_spec["outcomes"],
        flashcards=deck_spec["flashcards"],
        outline_10_sections=sections
    )
    apply_deck(deck)
    print(f"Applied {deck_id} successfully!")
    return deck

print("build_deck_from_spec_complete ready.")
