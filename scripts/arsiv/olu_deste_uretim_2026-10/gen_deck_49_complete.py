import sys, os, json, re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from meds.scripts.apply_generated_deck import apply_deck
from meds.scripts.generate_deck_core import sanitize_deck

# We will generate all 100 slides and 30 flashcards for Deck 49: TIP 310 - İnvaziv Serviks Kanseri ve Endometriyozis
print("Generating 100 slides for Deck 49...")
