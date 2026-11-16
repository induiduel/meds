# -*- coding: utf-8 -*-
"""
build_hypersensitivity_deck.py
Generates the comprehensive 500% depth interactive learning deck for:
'learn-asiri-duyarlilik-ve-otoimmunite' (Prof. Dr. Hikmet Keleş / Robbins 11. Baskı)
Includes:
- 24 rich slides with synthesis narrative, multi-level structured spot pearls (red/blue),
  flashcards, core content cards, AI prompt suggestions.
- Authentic 5-choice practice study questions (isPracticeQuestion: True, examYear: 'Özgün Çalışma Testi').
- Deep encyclopedia & glossary terms with differential diagnosis, mechanism, and exam pearls.
- Appending study questions to chunked database (src/data/study_questions/).
- Updating learning_batch_queue.json.
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECK_ID = "learn-asiri-duyarlilik-ve-otoimmunite"
DECK_TITLE = "Aşırı Duyarlılık Reaksiyonları ve Otoimmünite Patolojisi"
SHORT_TITLE = "Aşırı Duyarlılık & Otoimmünite"
DISCIPLINE = "Tıbbi Patoloji"
COMMITTEE = "Dönem 3 Kurul 1"
INSTRUCTOR = "Prof. Dr. Hikmet Keleş"

print("Starting generation for:", DECK_TITLE)
