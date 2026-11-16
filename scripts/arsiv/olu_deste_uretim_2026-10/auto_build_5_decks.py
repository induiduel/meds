import sys, os, json, re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from meds.scripts.apply_generated_deck import apply_deck
from meds.scripts.generate_deck_core import sanitize_deck
from meds.scripts.generate_deck_util import make_slide

# Generic builder for high-quality, syllabus-faithful, 100-slide medical decks
def create_100_slide_deck(deck_id, title, short_title, desc, discipline, source_pdf, overview, pearls, outcomes, flashcards, outline_10_sections):
    slides = []
    
    for sec_idx, sec in enumerate(outline_10_sections):
        sec_num = sec_idx + 1
        sec_title = sec["section_title"]
        topics = sec["topics"] # 10 topics per section = 100 slides total
        assert len(topics) == 10, f"Section {sec_num} must have 10 topics"
        
        for top_idx, t in enumerate(topics):
            slide_num = sec_idx * 10 + top_idx + 1
            is_checkpoint = (slide_num % 10 == 0)
            
            s_title = t["title"] if not is_checkpoint else f"[TEKRAR SAYFASI - CHECKPOINT {sec_num}] {sec_title}"
            s_sub = t["subtitle"]
            s_focus = t.get("focus", "Klinik ve Patolojik Özellikler")
            
            lead = t["lead"]
            bullets = t["bullets"]
            alert_type = t.get("alert_type", "IMPORTANT" if is_checkpoint else "NOTE")
            alert_text = t["alert_text"]
            summaries = t["summaries"]
            
            interactives = [
                {
                    "type": "cloze_masking",
                    "sentence": t["cloze_s"],
                    "maskedTerm": t["cloze_t"],
                    "hint": t["cloze_h"]
                },
                {
                    "type": "interactive_table",
                    "tableTitle": t["tbl_title"],
                    "tableHeaders": t["tbl_headers"],
                    "tableRows": t["tbl_rows"]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": t["chain_title"],
                    "steps": t["chain_steps"]
                },
                {
                    "type": "active_recall",
                    "question": t["rec_q"],
                    "answer": t["rec_a"]
                },
                {
                    "type": "spot_the_lie",
                    "topic": f"Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: {t['spot_topic']}",
                    "items": t["spot_items"]
                },
                {
                    "type": "micro_quiz",
                    "question": t["quiz_q"],
                    "microQuizOptions": t["quiz_opts"]
                }
            ]
            
            slide_obj = make_slide(
                slide_num=slide_num,
                title=s_title,
                subtitle=s_sub,
                clinical_focus=s_focus,
                lead_paragraph=lead,
                bullet_tuples=bullets,
                alert_type=alert_type,
                alert_text=alert_text,
                bullet_summaries=summaries,
                interactive_items=interactives
            )
            if is_checkpoint:
                slide_obj["isCheckpoint"] = True
            slides.append(slide_obj)
            
    assert len(slides) == 100, f"Expected 100 slides, got {len(slides)}"
    assert len(flashcards) == 30, f"Expected 30 flashcards, got {len(flashcards)}"
    
    deck = {
        "id": deck_id,
        "deckId": deck_id,
        "title": title,
        "shortTitle": short_title,
        "description": desc,
        "courseCode": "TIP 310",
        "curriculumPeriod": "Dönem 3 · Kurul 1",
        "committee": "Kurul 1 (Ürogenital ve Obstetrik Kurulu)",
        "discipline": discipline,
        "date": "08.10.2026",
        "instructor": "Dönem 3 Kurul 1 Öğretim Üyeleri",
        "sourcePdf": source_pdf,
        "overview": overview,
        "highYieldPearls": pearls,
        "isNew": True,
        "version": "2.0",
        "learningOutcomes": outcomes,
        "flashcards": flashcards,
        "slides": slides
    }
    
    deck = sanitize_deck(deck)
    return deck

print("create_100_slide_deck defined successfully.")
