import sys, os, json, re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from meds.scripts.generate_complete_5_decks import build_and_save_deck

print("Executing all 5 decks now...")
