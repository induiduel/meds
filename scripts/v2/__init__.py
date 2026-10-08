"""MedSoru Core v2 — bağımsız veri denetim + ingest sistemi.

Eski `scripts/agents`, `scripts/advanced_ai` ve `scripts/pipeline` hattından bağımsız çalışır.
Yalnızca `meds_database/schema/*.json` sözleşmesini paylaşır; eski veriyi okur ama asla ezmez.
Çıktıyı yalnızca `MEDS_CORE_DIR` (varsayılan `meds_database_core/`) altına yazar.

Donanım kısıtı: GPU kullanan yerel AI yok. Yerel tarafta yalnız CPU-only yöntemler
(Tesseract/OCRmyPDF, kural/regex, BM25, CPU embedding); LLM gereken her yerde ücretsiz bulut.
"""

__version__ = "2.0.0.dev0"
