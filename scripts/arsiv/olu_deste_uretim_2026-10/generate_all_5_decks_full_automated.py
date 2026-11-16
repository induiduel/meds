import sys, os, json, re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from meds.scripts.apply_generated_deck import apply_deck
from meds.scripts.generate_deck_core import sanitize_deck
from meds.scripts.generate_deck_util import make_slide
from meds.scripts.auto_build_5_decks import create_100_slide_deck

def build_deck_from_lesson_data(meta, lesson_sections):
    deck_id = meta["id"]
    print(f"\n==========================================")
    print(f"Building 100 Slides for {deck_id}...")
    print(f"Title: {meta['title']}")
    print(f"==========================================")
    
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
        outline_10_sections=lesson_sections
    )
    
    apply_deck(deck)
    print(f"Deck {deck_id} applied successfully!")
    return deck

print("Automated framework ready.")
