# -*- coding: utf-8 -*-
"""
Deck 61 Full Builder: k1p-k1-61-abortus
Amfi dersi: TIP 310 · Abortus · Dr. Öğr. Üyesi Hilal Ezgi Türkmen · Dönem 3 Kurul 1
"""

import sys, os, json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from meds.scripts.deck_generators.deck61.sec1 import get_sec1_slides
from meds.scripts.deck_generators.deck61.sec2 import get_sec2_slides
from meds.scripts.deck_generators.deck61.sec3 import get_sec3_slides
from meds.scripts.deck_generators.deck61.sec4 import get_sec4_slides
from meds.scripts.deck_generators.deck61.sec5 import get_sec5_slides
from meds.scripts.deck_generators.deck61.sec6 import get_sec6_slides
from meds.scripts.deck_generators.deck61.sec7 import get_sec7_slides
from meds.scripts.deck_generators.deck61.sec8 import get_sec8_slides
from meds.scripts.deck_generators.deck61.sec9 import get_sec9_slides
from meds.scripts.deck_generators.deck61.sec10 import get_sec10_slides
from meds.scripts.deck_generators.deck61.deck_61_flashcards import get_deck_61_flashcards
from meds.scripts.apply_generated_deck import apply_deck

DECK_ID = "k1p-k1-61-abortus"

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

    flashcards = get_deck_61_flashcards()
    print(f"Total flashcards gathered: {len(flashcards)}")
    assert len(flashcards) == 30, f"Expected 30 flashcards, got {len(flashcards)}"

    deck = {
        "id": DECK_ID,
        "deckId": DECK_ID,
        "title": "Abortus",
        "shortTitle": "Abortus",
        "discipline": "Kadın Hastalıkları ve Doğum",
        "committee": "Kurul 1 - Ürogenital ve Obstetrik Kurulu",
        "description": "Erken ve geç abortus tanımı (<20 hafta, <500 g), fetal genetik anomaliler (45,X0, trizomi 16, trizomi 1/3/19 yokluğu), maternal etiyolojiler, klinik tipler (imminens, insipiens, inkomplet, komplet, missed abortus USG kriterleri, septik abortus ve yönetimi), ilk trimester kanamalı hastaya yaklaşım, ultrasonik gebelik yaşı/canlılık tayini (hCG >2000 eşiği, CRL formülü), yönetim seçenekleri (bekleme, misoprostol, mifepriston, cerrahi aspirasyon, Rh Anti-D profilaksisi) ve tekrarlayan gebelik kaybı (ASRM, ESHRE, RCOG tanımları, kabul edilen etiyolojiler, önerilen testler).",
        "courseCode": "k1p",
        "curriculumCategory": "Dönem 3 Kurul 1",
        "category": "Kurul 1 · 2026-2027 ders paketi",
        "programDate": "2026-10-15",
        "instructor": "Dr. Öğr. Üyesi Hilal Ezgi Türkmen",
        "themeColor": "pink",
        "sourcePdf": "meds_database_v2/ders_notlari_k1/notlar/61_abortus.md",
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
    print(f"Deck 61 ({DECK_ID}) built and applied successfully.")
