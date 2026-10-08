"""MedSoru Core v2 — merkezi yapılandırma.

Tüm yollar ortam değişkenlerinden okunur (kodda gömülü mutlak yol yok). Varsayılanlar projenin
kardeş klasör düzenini (PROJE_TANITIMI.md) izler:

  meds_downloads/        ham Drive indirmeleri
  meds_temp/             ara çalışma alanı
  meds_database/         ESKİ veri deposu — v2 buradan yalnız OKUR (denetim), asla yazmaz
  meds_database_core/    YENİ izole çıktı deposu — v2 yalnız buraya yazar (MEDS_CORE_DIR)

`meds/.env` varsa yüklenir; mevcut ortam değişkenleri EZİLMEZ.
"""
from __future__ import annotations

import os
from pathlib import Path

__all__ = [
    "PROJECT_ROOT", "MEDS_DIR", "DOWNLOADS_DIR", "TEMP_DIR", "DATABASE_DIR", "SCHEMA_DIR",
    "CORE_DIR", "QUESTIONS_DIR", "CHUNKS_DIR", "SOURCES_DIR", "REPORTS_DIR", "STATE_DIR",
    "KATALOG_PATH", "PIPELINE_GENERATION",
    "load_dotenv", "ensure_core_dirs", "is_under_core", "describe",
]


def _p(key: str, default: Path) -> Path:
    raw = os.environ.get(key)
    return Path(raw).expanduser() if raw else default


def load_dotenv(path: Path | None = None) -> None:
    """Basit .env okuyucu: KEY=VALUE satırlarını ortama ekler, var olanları ezmez."""
    p = path or (MEDS_DIR / ".env")
    try:
        text = p.read_text(encoding="utf-8")
    except OSError:
        return
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        key = key.strip()
        val = val.split(" #", 1)[0].strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val


PROJECT_ROOT = _p("MEDS_PROJECT_ROOT", Path("/home/indu/medsor"))
MEDS_DIR = PROJECT_ROOT / "meds"

# .env'yi yolları hesaplamadan ÖNCE yükle (yol değişkenleri .env'den gelebilir).
load_dotenv(MEDS_DIR / ".env")

DOWNLOADS_DIR = _p("MEDS_DOWNLOADS_DIR", PROJECT_ROOT / "meds_downloads")
TEMP_DIR = _p("MEDS_TEMP_DIR", PROJECT_ROOT / "meds_temp")

# ESKİ veri: yalnız okunur.
DATABASE_DIR = _p("MEDS_DATABASE_DIR", PROJECT_ROOT / "meds_database")
SCHEMA_DIR = _p("MEDS_SCHEMA_DIR", DATABASE_DIR / "schema")

# YENİ izole çıktı: yalnız buraya yazılır.
CORE_DIR = _p("MEDS_CORE_DIR", PROJECT_ROOT / "meds_database_core")
QUESTIONS_DIR = CORE_DIR / "questions"
CHUNKS_DIR = CORE_DIR / "chunks"
SOURCES_DIR = CORE_DIR / "sources"
REPORTS_DIR = CORE_DIR / "reports"
CORE_REPORTS_DIR = REPORTS_DIR
STATE_DIR = CORE_DIR / "_state"
KATALOG_PATH = CORE_DIR / "KATALOG.json"
VECTORS_DIR = CORE_DIR / "vectors"
NOTES_DIR = CORE_DIR / "notes"
SUMMARIES_DIR = CORE_DIR / "summaries"
DERIVED_DIR = CORE_DIR / "derived"

# Müfredat / kazanım kaynakları (salt okunur).
TAXONOMY_PATH = _p("MEDS_TAXONOMY", DATABASE_DIR / "taxonomy" / "donem3_ders_programi.json")
CURRICULUM_PATH = _p("MEDS_CURRICULUM", MEDS_DIR / "curriculum" / "kbu_tip_donem3_curriculum.json")
# Faz 14 (eski sistem) inceleme çıktısı — entegrasyon için okunur.
FAZ14_REVIEWS = _p("MEDS_FAZ14_REVIEWS", PROJECT_ROOT / "meds_database_v2" / "phase14_past_question_editor" / "reviews.jsonl")

# Bu hattın ürettiği kayıtları ayırt eden nesil etiketi.
PIPELINE_GENERATION = os.environ.get("MEDS_V2_GENERATION", "v2_core")

# Serbest bulut zorunlu mu (faturalı anahtar kullanılmaz). Varsayılan: yalnız ücretsiz.
FREE_ONLY = os.environ.get("MEDS_FREE_ONLY", "1").lower() not in {"0", "false", "no", "off"}


def ensure_core_dirs() -> None:
    """Yeni çıktı deposunun dizinlerini (idempotent) oluşturur."""
    for d in (CORE_DIR, QUESTIONS_DIR, CHUNKS_DIR, SOURCES_DIR, REPORTS_DIR, STATE_DIR,
              VECTORS_DIR, NOTES_DIR, SUMMARIES_DIR, DERIVED_DIR):
        d.mkdir(parents=True, exist_ok=True)


def is_under_core(path: str | Path) -> bool:
    """Yol, izole CORE_DIR ağacının içinde mi?"""
    p = Path(path).resolve()
    core = CORE_DIR.resolve()
    return p == core or core in p.parents


def describe() -> dict[str, str]:
    """Tanı için okunur yol özeti."""
    return {
        "project_root": str(PROJECT_ROOT),
        "downloads": str(DOWNLOADS_DIR),
        "temp": str(TEMP_DIR),
        "database (salt-okunur)": str(DATABASE_DIR),
        "schema": str(SCHEMA_DIR),
        "core (yazılabilir)": str(CORE_DIR),
        "generation": PIPELINE_GENERATION,
        "free_only": str(FREE_ONLY),
    }
