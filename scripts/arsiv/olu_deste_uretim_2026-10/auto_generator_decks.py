import sys, os, json, re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from meds.scripts.apply_generated_deck import apply_deck
from meds.scripts.generate_deck_core import sanitize_deck
from meds.scripts.generate_deck_util import make_slide

def build_deck_from_spec(deck_spec):
    deck_id = deck_spec["id"]
    print(f"Building deck: {deck_id}...")
    
    slides = []
    topics = deck_spec["slide_topics"] # exactly 100 topic dictionaries
    assert len(topics) == 100, f"Expected 100 topics, got {len(topics)}"
    
    for idx, t in enumerate(topics):
        s_num = idx + 1
        is_checkpoint = (s_num % 10 == 0)
        
        # Build narrative
        lead = t["lead"]
        bullets = t["bullets"] # list of (header, desc)
        alert_t = t.get("alert_type", "NOTE" if not is_checkpoint else "IMPORTANT")
        alert_text = t["alert_text"]
        summaries = t["summaries"]
        
        # Interactive elements (4-6 per slide)
        interactives = []
        
        # 1. Cloze masking
        interactives.append({
            "type": "cloze_masking",
            "sentence": t["cloze_sentence"],
            "maskedTerm": t["cloze_term"],
            "hint": t["cloze_hint"]
        })
        
        # 2. Interactive table
        interactives.append({
            "type": "interactive_table",
            "tableTitle": t["table_title"],
            "tableHeaders": t["table_headers"],
            "tableRows": t["table_rows"]
        })
        
        # 3. Causal chain
        interactives.append({
            "type": "causal_chain",
            "chainTitle": t["chain_title"],
            "steps": t["chain_steps"]
        })
        
        # 4. Active recall
        interactives.append({
            "type": "active_recall",
            "question": t["recall_q"],
            "answer": t["recall_a"]
        })
        
        # 5. Spot the lie
        interactives.append({
            "type": "spot_the_lie",
            "topic": f"Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: {t['spot_topic']}",
            "items": t["spot_items"]
        })
        
        # 6. Micro quiz
        interactives.append({
            "type": "micro_quiz",
            "question": t["quiz_q"],
            "microQuizOptions": t["quiz_opts"]
        })
        
        slide_obj = make_slide(
            slide_num=s_num,
            title=t["title"],
            subtitle=t["subtitle"],
            clinical_focus=t["clinical_focus"],
            lead_paragraph=lead,
            bullet_tuples=bullets,
            alert_type=alert_t,
            alert_text=alert_text,
            bullet_summaries=summaries,
            interactive_items=interactives
        )
        if is_checkpoint:
            slide_obj["isCheckpoint"] = True
            
        slides.append(slide_obj)
        
    deck = {
        "id": deck_id,
        "deckId": deck_id,
        "title": deck_spec["title"],
        "shortTitle": deck_spec["shortTitle"],
        "description": deck_spec["description"],
        "courseCode": deck_spec.get("courseCode", "TIP 310"),
        "curriculumPeriod": deck_spec.get("curriculumPeriod", "Dönem 3 · Kurul 1"),
        "committee": deck_spec.get("committee", "Kurul 1 (Ürogenital ve Obstetrik Kurulu)"),
        "discipline": deck_spec["discipline"],
        "date": deck_spec.get("date", "08.10.2026"),
        "instructor": deck_spec.get("instructor", "Fakülte Öğretim Üyesi"),
        "sourcePdf": deck_spec["sourcePdf"],
        "overview": deck_spec["overview"],
        "highYieldPearls": deck_spec["highYieldPearls"],
        "isNew": True,
        "version": "2.0",
        "learningOutcomes": deck_spec["learningOutcomes"],
        "flashcards": deck_spec["flashcards"],
        "slides": slides
    }
    
    deck = sanitize_deck(deck)
    return deck

print("build_deck_from_spec defined successfully.")
