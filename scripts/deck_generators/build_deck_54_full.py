# -*- coding: utf-8 -*-
import sys, os, json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.deck54.sec1 import get_sec1_slides
from meds.scripts.deck_generators.deck54.sec2 import get_sec2_slides
from meds.scripts.deck_generators.deck54.sec3 import get_sec3_slides
from meds.scripts.deck_generators.deck54.sec4 import get_sec4_slides
from meds.scripts.deck_generators.deck54.sec5 import get_sec5_slides
from meds.scripts.deck_generators.deck54.sec6 import get_sec6_slides
from meds.scripts.deck_generators.deck54.sec7 import get_sec7_slides
from meds.scripts.deck_generators.deck54.sec8 import get_sec8_slides
from meds.scripts.deck_generators.deck54.sec9 import get_sec9_slides
from meds.scripts.deck_generators.deck54.sec10 import get_sec10_slides
from meds.scripts.deck_generators.deck54.deck_54_flashcards import get_deck_54_flashcards
from meds.scripts.apply_generated_deck import apply_deck

DECK_ID = "k1p-k1-54-uterus-duz-kas-ve-trofoblastik-tumorleri"

def build_deck():
    print(f"Building complete deck for {DECK_ID}...")
    slides = []
    slides.extend(get_sec1_slides())
    slides.extend(get_sec2_slides())
    slides.extend(get_sec3_slides())
    slides.extend(get_sec4_slides())
    slides.extend(get_sec5_slides())
    slides.extend(get_sec6_slides())
    slides.extend(get_sec7_slides())
    slides.extend(get_sec8_slides())
    slides.extend(get_sec9_slides())
    slides.extend(get_sec10_slides())

    print(f"Total slides gathered: {len(slides)}")
    assert len(slides) == 100, f"Expected 100 slides, got {len(slides)}"

    # Ensure sequential slideNumber 1 to 100 and validate checkpoint flag
    for idx, s in enumerate(slides):
        s["slideNumber"] = idx + 1
        if idx + 1 in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
            s["isCheckpoint"] = True

    flashcards = get_deck_54_flashcards()
    print(f"Total flashcards gathered: {len(flashcards)}")
    assert len(flashcards) == 30, f"Expected 30 flashcards, got {len(flashcards)}"

    deck = {
        "id": DECK_ID,
        "deckId": DECK_ID,
        "title": "Uterus Düz Kas ve Trofoblastik Tümörleri",
        "shortTitle": "Uterus Düz Kas ve Trofoblastik Tümörleri",
        "discipline": "Tıbbi Patoloji",
        "committee": "Kurul 1 - Ürogenital ve Obstetrik Kurulu",
        "description": "Myometrium düz kas tümörleri (leiomyom, varyantlar, leiomyosarkom), gestasyonel trofoblastik neoplaziler (komplet mol, parsiyel mol, invaziv mol, koryokarsinom, PSTT), plasenta anatomisi, asendan korioamnionit, funisit, transplasental villit (TORCH, sifiliz, listeria), ektopik gebelik, preeklampsi/eklampsi ve plasental yapışma anomalileri (akreta, inkreta, perkreta).",
        "courseCode": "k1p",
        "curriculumCategory": "Dönem 3 Kurul 1",
        "category": "Kurul 1 · 2026-2027 ders paketi",
        "programDate": "2026-10-09",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "themeColor": "rose",
        "sourcePdf": "meds_database_v2/ders_notlari_k1/notlar/54_uterus_duz_kas_ve_trofoblastik_tumorleri.md",
        "slides": slides,
        "flashcards": flashcards,
        "slideCount": len(slides),
        "totalSlides": len(slides),
        "slidesCount": len(slides),
        "flashcardsCount": len(flashcards),
        "cardCount": len(flashcards),
        "questionCount": 0
    }

    return deck

if __name__ == '__main__':
    deck = build_deck()
    apply_deck(deck)
    print(f"Deck 54 ({DECK_ID}) built and applied successfully.")
