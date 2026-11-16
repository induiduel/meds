# -*- coding: utf-8 -*-
import sys, os, json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.apply_generated_deck import apply_deck

from meds.scripts.deck_generators.deck51.sec1 import get_sec1
from meds.scripts.deck_generators.deck51.sec2 import get_sec2
from meds.scripts.deck_generators.deck51.sec3 import get_sec3
from meds.scripts.deck_generators.deck51.sec4 import get_sec4
from meds.scripts.deck_generators.deck51.sec5 import get_sec5
from meds.scripts.deck_generators.deck51.sec6 import get_sec6
from meds.scripts.deck_generators.deck51.sec7 import get_sec7
from meds.scripts.deck_generators.deck51.sec8 import get_sec8
from meds.scripts.deck_generators.deck51.sec9 import get_sec9
from meds.scripts.deck_generators.deck51.sec10 import get_sec10
from meds.scripts.deck_generators.deck51.deck_51_flashcards import get_deck_51_flashcards

DECK_ID = "k1p-k1-51-uriner-sistem-enfeksiyonlari-laboratuvar-bulgulari"

if __name__ == "__main__":
    print(f"Building {DECK_ID} full...")
    all_slides = []
    all_slides.extend(get_sec1())
    all_slides.extend(get_sec2())
    all_slides.extend(get_sec3())
    all_slides.extend(get_sec4())
    all_slides.extend(get_sec5())
    all_slides.extend(get_sec6())
    all_slides.extend(get_sec7())
    all_slides.extend(get_sec8())
    all_slides.extend(get_sec9())
    all_slides.extend(get_sec10())

    flashcards = get_deck_51_flashcards()

    deck_path = f"/home/indu/medsor/meds/src/data/decks/items/{DECK_ID}.json"
    if os.path.exists(deck_path):
        with open(deck_path, "r", encoding="utf-8") as f:
            deck = json.load(f)
    else:
        deck = {
            "id": DECK_ID,
            "title": "Üriner Sistem Enfeksiyonları: Laboratuvar Bulguları ve Tedavi",
            "curriculumPeriod": "Dönem 3",
            "committee": "Kurul 1",
            "subject": "Üroloji / Enfeksiyon Hastalıkları",
            "author": "Doç. Dr. Özer Baran",
            "description": "Üriner sistem enfeksiyonlarının epidemiyolojisi, patogenezi, laboratuvar tanı kriterleri (nitrit, lökosit esteraz, mikroskopi) ve tedavi rejimleri."
        }

    deck["slides"] = all_slides
    deck["flashcards"] = flashcards
    deck["totalSlides"] = len(all_slides)
    deck["slideCount"] = len(all_slides)
    deck["flashcardCount"] = len(flashcards)

    apply_deck(deck)
    print(f"Successfully applied {len(all_slides)} slides and {len(flashcards)} flashcards to {DECK_ID}")
