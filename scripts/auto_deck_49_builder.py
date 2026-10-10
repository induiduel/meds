import sys, os, json, re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from meds.scripts.auto_build_5_decks_full import build_deck_from_spec_complete
from meds.scripts.auto_generator_5_decks_full import make_item
from meds.scripts.build_deck_49_generator import get_deck_49_flashcards

DECK_ID = "k1p-k1-49-invaziv-serviks-kanseri-ve-endometriyozis"

print("Building Deck 49...")
