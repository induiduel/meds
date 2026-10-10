import sys, os, json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from meds.scripts.deck_generators.deck49.sec1 import get_sec1
from meds.scripts.deck_generators.deck49.sanitize_sec1 import sanitize_elements
from meds.scripts.deck_generators.deck49.sec2 import get_sec2
from meds.scripts.deck_generators.deck49.sec3 import get_sec3
from meds.scripts.deck_generators.deck49.sec4 import get_sec4
from meds.scripts.deck_generators.deck49.sec5 import get_sec5
from meds.scripts.deck_generators.deck49.sec6 import get_sec6
from meds.scripts.deck_generators.deck49.sec7 import get_sec7
from meds.scripts.deck_generators.deck49.sec8 import get_sec8
from meds.scripts.deck_generators.deck49.sec9 import get_sec9
from meds.scripts.deck_generators.deck49.sec10 import get_sec10
from meds.scripts.build_deck_49_generator import get_deck_49_flashcards
from meds.scripts.apply_generated_deck import apply_deck

DECK_ID = "k1p-k1-49-invaziv-serviks-kanseri-ve-endometriyozis"

def build_deck():
    print(f"Building complete deck for {DECK_ID}...")
    slides = []
    slides.extend(sanitize_elements(get_sec1()))
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

    # Ensure sequential slideNumber 1 to 100
    for idx, s in enumerate(slides):
        s["slideNumber"] = idx + 1

    flashcards = get_deck_49_flashcards()
    print(f"Total flashcards gathered: {len(flashcards)}")
    assert len(flashcards) == 30, f"Expected 30 flashcards, got {len(flashcards)}"

    deck = {
        "id": DECK_ID,
        "title": "İnvaziv Serviks Kanseri ve Endometriyozis",
        "discipline": "Tıbbi Patoloji",
        "description": "Servisit etyolojisi, endoservikal polip, HPV virolojisi, E6/E7 onkogenezi, SIL/CIN doğal seyri, Pap smear ve HPV taramaları, aşılama ve invaziv karsinom patolojisi.",
        "courseCode": "k1p",
        "curriculumCategory": "Dönem 3 Kurul 1",
        "slides": slides,
        "flashcards": flashcards
    }

    return deck

if __name__ == '__main__':
    deck = build_deck()
    apply_deck(deck)
    print("Deck 49 built and applied successfully.")
