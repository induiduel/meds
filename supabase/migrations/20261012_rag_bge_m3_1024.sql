-- MedSoru RAG: BGE-M3 (1024 boyut) test kolonu + arama fonksiyonu.
-- TEST aşaması: uygulanmadan önce kullanıcı onayı gerekir. Prod embedding_e5 (384) korunur.
-- Uygulama: yerel -> docker exec -i supabase-db psql -U postgres < bu_dosya.sql ; bulut -> SQL Editor.
CREATE EXTENSION IF NOT EXISTS vector;

ALTER TABLE public.rag_chunks ADD COLUMN IF NOT EXISTS embedding_bge_m3 vector(1024);
ALTER TABLE public.rag_chunks ADD COLUMN IF NOT EXISTS content_hash_bge_m3 TEXT;

CREATE INDEX IF NOT EXISTS idx_rag_chunks_bge_m3_hnsw
  ON public.rag_chunks USING hnsw (embedding_bge_m3 vector_cosine_ops) WITH (m = 16, ef_construction = 64);

CREATE OR REPLACE FUNCTION public.match_rag_chunks_bge_m3(
  query_embedding vector(1024),
  match_count INT DEFAULT 10,
  filter_types TEXT[] DEFAULT NULL,
  filter_committee TEXT DEFAULT NULL
) RETURNS TABLE (id TEXT, document_id TEXT, document_type TEXT, committee_id TEXT, discipline TEXT, title TEXT,
                 page_number INT, content TEXT, metadata JSONB, similarity FLOAT)
LANGUAGE sql STABLE AS $$
  SELECT rc.id, rc.document_id, rc.document_type, rc.committee_id, rc.discipline, rc.title, rc.page_number, rc.content,
         rc.metadata, 1 - (rc.embedding_bge_m3 <=> query_embedding) AS similarity
  FROM public.rag_chunks rc
  WHERE rc.embedding_bge_m3 IS NOT NULL
    AND (filter_types IS NULL OR rc.document_type = ANY (filter_types))
    AND (filter_committee IS NULL OR rc.committee_id = filter_committee)
  ORDER BY rc.embedding_bge_m3 <=> query_embedding
  LIMIT match_count;
$$;

NOTIFY pgrst, 'reload schema';
