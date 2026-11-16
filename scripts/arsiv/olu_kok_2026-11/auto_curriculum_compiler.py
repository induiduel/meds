import sys, os, json, re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from meds.scripts.apply_generated_deck import apply_deck
from meds.scripts.generate_deck_core import sanitize_deck
from meds.scripts.generate_deck_util import make_slide
from meds.scripts.auto_build_5_decks import create_100_slide_deck

def build_complete_deck(deck_id, title, short_title, desc, discipline, source_pdf, overview, pearls, outcomes, flashcards, sections_data):
    print(f"\n==========================================")
    print(f"Compiling: {deck_id} (100 slides, 30 flashcards)...")
    print(f"Title: {title}")
    print(f"==========================================")
    
    deck = create_100_slide_deck(
        deck_id=deck_id,
        title=title,
        short_title=short_title,
        desc=desc,
        discipline=discipline,
        source_pdf=source_pdf,
        overview=overview,
        pearls=pearls,
        outcomes=outcomes,
        flashcards=flashcards,
        outline_10_sections=sections_data
    )
    apply_deck(deck)
    print(f"Applied {deck_id} successfully!")
    return deck

print("build_complete_deck ready.")
