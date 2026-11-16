"""Semantik Veri Modeli — yapılandırma.

Yalnızca OKUR (eski veriye ve v2 çıktısına dokunmaz): müfredat, ders notları, özetler, CORE parçaları,
ICD/sözlük kaynakları. Tüm çıktı bu klasörün `data/` altına yazılır. GPU yok, ücretsiz (CPU).
"""
from __future__ import annotations

import os

os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("OMP_NUM_THREADS", "8")
from pathlib import Path

PROJECT_ROOT = Path(os.environ.get("MEDS_PROJECT_ROOT", "/home/indu/medsor"))
MEDS_DIR = PROJECT_ROOT / "meds"
DB = Path(os.environ.get("MEDS_DATABASE_DIR", PROJECT_ROOT / "meds_database"))
CORE = Path(os.environ.get("MEDS_CORE_DIR", PROJECT_ROOT / "meds_database_core"))
DB2 = PROJECT_ROOT / "meds_database_v2"

# Salt okunur kaynaklar
CURRICULUM = MEDS_DIR / "curriculum" / "kbu_tip_donem3_curriculum.json"
TAXONOMY = DB / "taxonomy" / "donem3_ders_programi.json"
CLEAN_NOTES = DB / "derived" / "clean_notes"
SUMMARIES = MEDS_DIR / "src" / "data" / "summaries"
ICD_TSV = DB2 / "reference" / "icd10.tsv"
THESAURUS = DB2 / "evidence_thesaurus" / "kanitli_sozluk.json"
CONCEPT_IDS = DB2 / "concept_ids" / "kavramlar.json"

# CORE (v2 çıktısı) — indeks için
CORE_CHUNKS = CORE / "chunks"
CORE_VECTORS = CORE / "vectors" / "e5.npy"
CORE_VECTOR_IDS = CORE / "vectors" / "e5_ids.jsonl"
CORE_SOURCES = CORE / "sources"
CORE_QUESTIONS = CORE / "questions"

# Çıktı (bu klasör)
BASE = Path(__file__).resolve().parent
OUT = BASE / "data"
OUT.mkdir(parents=True, exist_ok=True)

EMBED_MODEL = os.environ.get("MEDS_SEM_EMBED", "intfloat/multilingual-e5-small")
RERANK_MODEL = os.environ.get("MEDS_SEM_RERANK", "cross-encoder/mmarco-mMiniLMv2-L6-H384-v1")
CHUNK_MIN_WORDS = 60
CHUNK_MAX_WORDS = 250
TOP_K = 25
RERANK_K = 5

TAX_PATH = OUT / "taxonomy.json"
LEXICON_PATH = OUT / "lexicon.json"
ICD_PATH = OUT / "icd.json"
META_PATH = OUT / "chunks_meta.jsonl"
INDEX_PATH = OUT / "index.faiss"
REPORT_PATH = OUT / "eval_report.json"
