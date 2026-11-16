"""Revize v2 — yapılandırma. Girdi salt okunur; çıktı v2 deposunda."""
from __future__ import annotations

from pathlib import Path

from .. import config as v2

PROJECT_ROOT = v2.PROJECT_ROOT
REVIEWS = PROJECT_ROOT / "meds_database_v2" / "phase14_past_question_editor" / "reviews.jsonl"
CORE_DIR = v2.CORE_DIR                                            # meds_database_core
OUT = CORE_DIR / "revize_v2"
STATE = OUT / "_state"
VECTORS = OUT / "vectors"
QUESTIONS_OUT = OUT / "questions.jsonl"
CHANGES_OUT = OUT / "changes.jsonl"
QUARANTINE_OUT = OUT / "quarantine.jsonl"
REPORT_OUT = OUT / "report.json"

MAX_OPTION_LEN = 220          # gereksiz uzun şık eşiği
MIN_STEM_LEN = 18
SUPPORT_MIN = 0.35            # kanıt desteği eşiği
REVIZE_TAG = "v2"


def ensure_dirs() -> None:
    for d in (OUT, STATE, VECTORS):
        d.mkdir(parents=True, exist_ok=True)
