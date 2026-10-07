-- MedSoru RAG: çok dilli e5-small (384 boyut, CPU, ücretsiz) vektörleri + karma arama fonksiyonu.
-- Yerel: docker exec -i supabase-db psql -U postgres < bu_dosya.sql · Bulut: Supabase Dashboard → SQL Editor → Run.
CREATE EXTENSION IF NOT EXISTS vector;

ALTER TABLE public.rag_chunks ADD COLUMN IF NOT EXISTS embedding_e5 vector(384);
ALTER TABLE public.rag_chunks ADD COLUMN IF NOT EXISTS content_hash TEXT;
ALTER TABLE public.rag_chunks ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ DEFAULT NOW();

CREATE INDEX IF NOT EXISTS idx_rag_chunks_e5_hnsw
  ON public.rag_chunks USING hnsw (embedding_e5 vector_cosine_ops) WITH (m = 16, ef_construction = 64);
CREATE INDEX IF NOT EXISTS idx_rag_chunks_type ON public.rag_chunks (document_type);
CREATE INDEX IF NOT EXISTS idx_rag_chunks_committee ON public.rag_chunks (committee_id);

-- Anlamsal arama (sorgu vektörü "query: " önekiyle e5-small ile üretilir).
-- filter_types boşsa tüm türler; kaynak (grounding) aramaları için: past_question, lecture_slide, summary, transcript.
CREATE OR REPLACE FUNCTION public.match_rag_chunks_e5(
  query_embedding vector(384),
  match_count INT DEFAULT 10,
  filter_types TEXT[] DEFAULT NULL,
  filter_committee TEXT DEFAULT NULL
) RETURNS TABLE (id TEXT, document_id TEXT, document_type TEXT, committee_id TEXT, discipline TEXT, title TEXT,
                 page_number INT, content TEXT, metadata JSONB, similarity FLOAT)
LANGUAGE sql STABLE AS $$
  SELECT rc.id, rc.document_id, rc.document_type, rc.committee_id, rc.discipline, rc.title, rc.page_number, rc.content,
         rc.metadata, 1 - (rc.embedding_e5 <=> query_embedding) AS similarity
  FROM public.rag_chunks rc
  WHERE rc.embedding_e5 IS NOT NULL
    AND (filter_types IS NULL OR rc.document_type = ANY (filter_types))
    AND (filter_committee IS NULL OR rc.committee_id = filter_committee)
  ORDER BY rc.embedding_e5 <=> query_embedding
  LIMIT match_count;
$$;
NOTIFY pgrst, 'reload schema';
