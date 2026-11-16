import sys, os, json, re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from meds.scripts.apply_generated_deck import apply_deck
from meds.scripts.generate_deck_core import sanitize_deck
from meds.scripts.generate_deck_util import make_slide

print("Starting generation process for Kurul 1 Decks 49, 50, 51, 52, 53...")
