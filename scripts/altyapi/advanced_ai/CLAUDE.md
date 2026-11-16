# scripts/altyapi/advanced_ai/ — RAG vektör hattı

Vector pipeline (2026-10-13): `scripts/altyapi/advanced_ai/rag_vektor_hatti.py` is the only writer of `rag_chunks`
(`rag_vector_build.py` is a compat wrapper). It reads `data/local_rag_chunks.jsonl` (old `.json` if missing; `scripts/rag_parca_deposu.py`), embeds only new/changed chunks
through the CPU services (no in-process model), writes meds-pg with COPY, deletes rows no longer in the source, and
with `--oracle` sends only the diff (id + hashes + vector fingerprint) to Oracle over ssh (gzip). `--denetle` finds and
repairs bge vectors stored under the wrong chunk. Cron every 3 h on the device. Never restore `rag_chunks` with a full
dump without re-running `deploy/pg/sql/rag_chunks_indexes.sql` (Oracle lost every index that way → 1.7 s queries).
SQL functions live in `deploy/pg/sql/rag_vektor_islevleri.sql` (dynamic plpgsql so HNSW is used with/without filters).
`GET /api/rag/related` (`src/services/ragRelatedRoutes.ts`) uses stored vectors (no embed call): `mod=ilgili` lecture
material, `benzer` similar questions, `kopya` near-duplicates; `GET /api/rag/vectors/health` shows coverage.
