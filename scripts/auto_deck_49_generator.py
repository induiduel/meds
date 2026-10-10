import sys, os, json, re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from meds.scripts.generate_complete_5_decks import build_and_save_deck
from meds.scripts.build_deck_49_generator import get_deck_49_flashcards

DECK_ID = "k1p-k1-49-invaziv-serviks-kanseri-ve-endometriyozis"

print("Building complete 100 slides for Deck 49...")
