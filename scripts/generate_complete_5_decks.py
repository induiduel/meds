import sys, os, json, re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from meds.scripts.apply_generated_deck import apply_deck
from meds.scripts.generate_deck_core import sanitize_deck
from meds.scripts.generate_deck_util import make_slide

# Generic generator for creating a complete 100-slide deck with 30 flashcards
def build_and_save_deck(meta, section_generators):
    deck_id = meta["id"]
    print(f"\n>>> GENERATING DECK: {deck_id} (100 slides, 30 flashcards)...")
    slides = []
    
    for s_idx, sec in enumerate(section_generators):
        sec_num = s_idx + 1
        sec_title = sec["title"]
        items = sec["items"]
        assert len(items) == 10, f"Section {sec_num} ({sec_title}) must have 10 items, got {len(items)}"
        
        for top_idx, item in enumerate(items):
            slide_idx = s_idx * 10 + top_idx + 1
            is_cp = (slide_idx % 10 == 0)
            
            s_title = item["title"] if not is_cp else f"[TEKRAR SAYFASI - CHECKPOINT {sec_num}] {sec_title}"
            s_subtitle = item["subtitle"]
            s_focus = item.get("focus", meta["discipline"])
            s_lead = item["lead"]
            s_bullets = item["bullets"]
            s_alert_type = "IMPORTANT" if is_cp else "NOTE"
            s_alert_text = item["alert"]
            s_summaries = item["summaries"]
            
            interactives = [
                {
                    "type": "cloze_masking",
                    "sentence": item["cloze"][0],
                    "maskedTerm": item["cloze"][1],
                    "hint": item["cloze"][2]
                },
                {
                    "type": "interactive_table",
                    "tableTitle": item["table"]["title"],
                    "tableHeaders": item["table"]["headers"],
                    "tableRows": item["table"]["rows"]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": item["chain"]["title"],
                    "steps": item["chain"]["steps"]
                },
                {
                    "type": "active_recall",
                    "question": item["recall"]["q"],
                    "answer": item["recall"]["a"]
                },
                {
                    "type": "spot_the_lie",
                    "topic": f"Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: {item['spot']['topic']}",
                    "items": item["spot"]["items"]
                },
                {
                    "type": "micro_quiz",
                    "question": item["quiz"]["q"],
                    "microQuizOptions": item["quiz"]["opts"]
                }
            ]
            
            slide_obj = make_slide(
                slide_num=slide_idx,
                title=s_title,
                subtitle=s_subtitle,
                clinical_focus=s_focus,
                lead_paragraph=s_lead,
                bullet_tuples=s_bullets,
                alert_type=s_alert_type,
                alert_text=s_alert_text,
                bullet_summaries=s_summaries,
                interactive_items=interactives
            )
            if is_cp:
                slide_obj["isCheckpoint"] = True
                
            slides.append(slide_obj)
            
    assert len(slides) == 100, f"Expected 100 slides, got {len(slides)}"
    assert len(meta["flashcards"]) == 30, f"Expected 30 flashcards, got {len(meta['flashcards'])}"
    
    deck = {
        "id": deck_id,
        "deckId": deck_id,
        "title": meta["title"],
        "shortTitle": meta["shortTitle"],
        "description": meta["description"],
        "courseCode": "TIP 310",
        "curriculumPeriod": "Dönem 3 · Kurul 1",
        "committee": "Kurul 1 (Ürogenital ve Obstetrik Kurulu)",
        "discipline": meta["discipline"],
        "date": "08.10.2026",
        "instructor": meta.get("instructor", "Dönem 3 Kurul 1 Öğretim Üyesi"),
        "sourcePdf": meta["sourcePdf"],
        "overview": meta["overview"],
        "highYieldPearls": meta["pearls"],
        "isNew": True,
        "version": "2.0",
        "learningOutcomes": meta["outcomes"],
        "flashcards": meta["flashcards"],
        "slides": slides
    }
    
    deck = sanitize_deck(deck)
    apply_deck(deck)
    print(f"Deck {deck_id} saved and synced successfully!")
    return deck

print("build_and_save_deck loaded.")
