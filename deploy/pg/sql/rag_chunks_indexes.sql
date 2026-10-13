-- rag_chunks indeksleri (idempotent). 2026-10-13: Oracle'da tam döküm geri yüklemesi (sync-vectors.sh --clean)
-- sonrası tabloda hiç indeks kalmamıştı → her vektör araması 81k satırı sırayla tarıyordu (~1,7 sn, zaman aşımı 1,5 sn).
-- Kullanım (iki makinede): docker exec -i meds-pg psql -U meds -d meds < deploy/pg/sql/rag_chunks_indexes.sql
SET maintenance_work_mem = '768MB';
-- paralel kurulum Docker'ın 64 MB /dev/shm'sine sığmıyor ("No space left on device")
SET max_parallel_maintenance_workers = 0;

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conrelid = 'public.rag_chunks'::regclass AND contype = 'p') THEN
    -- yinelenen kimlik varsa en yenisi kalır
    DELETE FROM public.rag_chunks a USING public.rag_chunks b
      WHERE a.id = b.id AND a.ctid < b.ctid;
    ALTER TABLE public.rag_chunks ADD CONSTRAINT rag_chunks_pkey PRIMARY KEY (id);
  END IF;
END $$;

CREATE INDEX IF NOT EXISTS idx_rag_chunks_committee ON public.rag_chunks (committee_id);
CREATE INDEX IF NOT EXISTS idx_rag_chunks_discipline ON public.rag_chunks (discipline);
CREATE INDEX IF NOT EXISTS idx_rag_chunks_doc_id ON public.rag_chunks (document_id);
CREATE INDEX IF NOT EXISTS idx_rag_chunks_type ON public.rag_chunks (document_type);
CREATE INDEX IF NOT EXISTS idx_rag_chunks_type_doc ON public.rag_chunks (document_type, document_id);
CREATE INDEX IF NOT EXISTS idx_rag_chunks_fts ON public.rag_chunks USING gin (to_tsvector('simple'::regconfig, content));
CREATE INDEX IF NOT EXISTS idx_rag_chunks_bge_m3_hnsw ON public.rag_chunks
  USING hnsw (embedding_bge_m3 vector_cosine_ops) WITH (m = 16, ef_construction = 64);
-- e5 (384) yedek yol: bge servisi yokken kullanılır; küçük (≈110 MB) HNSW
CREATE INDEX IF NOT EXISTS idx_rag_chunks_e5_hnsw ON public.rag_chunks
  USING hnsw (embedding_e5 vector_cosine_ops) WITH (m = 16, ef_construction = 64);
ANALYZE public.rag_chunks;
