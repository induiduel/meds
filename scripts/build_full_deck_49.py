import sys, os, json, re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from meds.scripts.apply_generated_deck import apply_deck
from meds.scripts.auto_build_5_decks import create_100_slide_deck
from meds.scripts.build_deck_49_generator import get_deck_49_flashcards

DECK_ID = "k1p-k1-49-invaziv-serviks-kanseri-ve-endometriyozis"

print("Building complete Deck 49...")
