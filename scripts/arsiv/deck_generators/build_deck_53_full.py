# -*- coding: utf-8 -*-
import sys, os, json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.deck53.sec1 import get_sec1
from meds.scripts.deck_generators.deck53.sec2 import get_sec2
from meds.scripts.deck_generators.deck53.sec3 import get_sec3
from meds.scripts.deck_generators.deck53.sec4 import get_sec4
from meds.scripts.deck_generators.deck53.sec5 import get_sec5
from meds.scripts.deck_generators.deck53.sec6 import get_sec6
from meds.scripts.deck_generators.deck53.sec7 import get_sec7
from meds.scripts.deck_generators.deck53.sec8 import get_sec8
from meds.scripts.deck_generators.deck53.sec9 import get_sec9
from meds.scripts.deck_generators.deck53.sec10 import get_sec10
from meds.scripts.deck_generators.deck53.deck_53_flashcards import get_deck_53_flashcards
from meds.scripts.apply_generated_deck import apply_deck

DECK_ID = "k1p-k1-53-endometriyal-hiperplazi-ve-kanserleri"

def build_deck():
    print(f"Building complete deck for {DECK_ID}...")
    slides = []
    slides.extend(get_sec1())
    slides.extend(get_sec2())
    slides.extend(get_sec3())
    slides.extend(get_sec4())
    slides.extend(get_sec5())
    slides.extend(get_sec6())
    slides.extend(get_sec7())
    slides.extend(get_sec8())
    slides.extend(get_sec9())
    slides.extend(get_sec10())

    print(f"Total slides gathered: {len(slides)}")
    assert len(slides) == 100, f"Expected 100 slides, got {len(slides)}"

    # Ensure sequential slideNumber 1 to 100 and validate content
    for idx, s in enumerate(slides):
        s["slideNumber"] = idx + 1
        # Set isCheckpoint flag
        if idx + 1 in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
            s["isCheckpoint"] = True

    flashcards = get_deck_53_flashcards()
    print(f"Total flashcards gathered: {len(flashcards)}")
    assert len(flashcards) == 30, f"Expected 30 flashcards, got {len(flashcards)}"

    deck = {
        "id": DECK_ID,
        "title": "Endometriyal Hiperplazi ve Kanserleri",
        "shortTitle": "Endometriyal Hiperplazi ve Kanserleri",
        "discipline": "Tıbbi Patoloji",
        "committee": "Kurul 1 - Ürogenital ve Obstetrik Kurulu",
        "description": "Menstrual siklus hormonal düzeni, endometrial histoloji ve fazlar, epitelyal metaplaziler, AUK sınıflaması, düzensiz proliferatif endometrium, endometrial polip, hiperplazi sınıflaması ve kanser riski, endometrit tanı kriterleri, adenomyozis, endometriozis ve FIGO evrelemeli endometrium karsinomu.",
        "courseCode": "k1p",
        "curriculumCategory": "Dönem 3 Kurul 1",
        "category": "Kurul 1 · 2026-2027 ders paketi",
        "programDate": "2026-10-09",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "themeColor": "rose",
        "slides": slides,
        "flashcards": flashcards
    }

    return deck

if __name__ == '__main__':
    deck = build_deck()
    apply_deck(deck)
    print("Deck 53 built and applied successfully.")
