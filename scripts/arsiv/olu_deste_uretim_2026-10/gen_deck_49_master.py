import sys, os, json, re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from meds.scripts.apply_generated_deck import apply_deck
from meds.scripts.generate_deck_core import sanitize_deck

DECK_ID = "k1p-k1-49-invaziv-serviks-kanseri-ve-endometriyozis"

print("Master script setup ready.")
