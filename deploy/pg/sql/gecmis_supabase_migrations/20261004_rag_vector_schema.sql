-- ==============================================================================
-- MedSoru RAG (Retrieval-Augmented Generation) & pgvector Şeması
-- Supabase Dashboard > SQL Editor sekmesine yapıştırıp "Run" butonuna basarak çalıştırın.
-- ==============================================================================

-- 1. pgvector Eklentisini Etkinleştir
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. RAG Parçacıkları (Chunks) Tablosu
-- Slayt sayfaları, çıkmış sorular, ses transkriptleri ve özetler burada saklanır.
CREATE TABLE IF NOT EXISTS public.rag_chunks (
  id TEXT PRIMARY KEY,
  document_id TEXT NOT NULL,                         -- Orijinal not, soru veya transkript ID'si
  document_type TEXT NOT NULL,                       -- 'lecture_slide', 'past_question', 'transcript', 'summary'
  committee_id TEXT,                                 -- 'donem3-kurul1', 'donem3-kurul2', vb.
  discipline TEXT,                                   -- 'Tıbbi Patoloji', 'Tıbbi Farmakoloji', vb.
  title TEXT,                                        -- Not başlığı veya soru konusu
  page_number INTEGER,                               -- Slayt/Sayfa no (sorularda NULL veya soru no)
  content TEXT NOT NULL,                             -- Metin içeriği (arama yapılan asıl veri)
  content_tsv tsvector GENERATED ALWAYS AS (to_tsvector('simple', content)) STORED,
  metadata JSONB DEFAULT '{}'::jsonb,                -- Ek bilgiler (şıklar, doğru cevap, öğretim üyesi vb.)
  embedding vector(1024),                            -- BGE-M3 1024 boyutlu yerel dense vektör
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Hızlı Filtreleme ve Vektör İndeksleri
CREATE INDEX IF NOT EXISTS idx_rag_chunks_committee ON public.rag_chunks (committee_id);
CREATE INDEX IF NOT EXISTS idx_rag_chunks_discipline ON public.rag_chunks (discipline);
CREATE INDEX IF NOT EXISTS idx_rag_chunks_type ON public.rag_chunks (document_type);
CREATE INDEX IF NOT EXISTS idx_rag_chunks_doc_id ON public.rag_chunks (document_id);
CREATE INDEX IF NOT EXISTS idx_rag_chunks_type_doc ON public.rag_chunks (document_type, document_id);

-- Tam Metin Arama (Full-Text Search) Simple GIN İndeksi (Tıbbi terimleri bozmaz)
CREATE INDEX IF NOT EXISTS idx_rag_chunks_tsv ON public.rag_chunks USING gin (content_tsv);

-- HNSW Vektör Benzerlik İndeksi (IVFFlat yerine dinamik, yüksek hızlı ve sıfır-reindex gerektiren HNSW)
CREATE INDEX IF NOT EXISTS idx_rag_chunks_hnsw 
  ON public.rag_chunks USING hnsw (embedding vector_cosine_ops) 
  WITH (m = 16, ef_construction = 64);

-- 4. Temel Vektör Benzerlik Araması Fonksiyonu (match_rag_chunks)
CREATE OR REPLACE FUNCTION match_rag_chunks (
  query_embedding vector(768),
  match_threshold float DEFAULT 0.35,
  match_count int DEFAULT 5,
  filter_committee text DEFAULT NULL,
  filter_discipline text DEFAULT NULL,
  filter_doc_type text DEFAULT NULL
)
RETURNS TABLE (
  id text,
  document_id text,
  document_type text,
  committee_id text,
  discipline text,
  title text,
  page_number int,
  content text,
  metadata jsonb,
  similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    rc.id,
    rc.document_id,
    rc.document_type,
    rc.committee_id,
    rc.discipline,
    rc.title,
    rc.page_number,
    rc.content,
    rc.metadata,
    (1 - (rc.embedding <=> query_embedding))::float AS similarity
  FROM public.rag_chunks rc
  WHERE
    (filter_committee IS NULL OR rc.committee_id = filter_committee)
    AND (filter_discipline IS NULL OR rc.discipline ILIKE '%' || filter_discipline || '%')
    AND (filter_doc_type IS NULL OR rc.document_type = filter_doc_type)
    AND (rc.embedding IS NOT NULL)
    AND (1 - (rc.embedding <=> query_embedding)) >= match_threshold
  ORDER BY rc.embedding <=> query_embedding ASC
  LIMIT match_count;
END;
$$;

-- 5. Hibrit Arama Fonksiyonu (Vektör + Anahtar Kelime FTS)
-- Tıbbi terimleri (ilaç, sendrom, gen adları) tam yakalamak için kosinüs benzerliği ile metin eşleşmesini birleştirir.
CREATE OR REPLACE FUNCTION hybrid_match_rag_chunks (
  query_text text,
  query_embedding vector(768),
  match_count int DEFAULT 5,
  filter_committee text DEFAULT NULL,
  filter_discipline text DEFAULT NULL,
  filter_doc_type text DEFAULT NULL
)
RETURNS TABLE (
  id text,
  document_id text,
  document_type text,
  committee_id text,
  discipline text,
  title text,
  page_number int,
  content text,
  metadata jsonb,
  similarity float,
  fts_rank float,
  combined_score float
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  WITH vector_search AS (
    SELECT
      rc.id,
      (1 - (rc.embedding <=> query_embedding))::float AS sim
    FROM public.rag_chunks rc
    WHERE
      (filter_committee IS NULL OR rc.committee_id = filter_committee)
      AND (filter_discipline IS NULL OR rc.discipline ILIKE '%' || filter_discipline || '%')
      AND (filter_doc_type IS NULL OR rc.document_type = filter_doc_type)
      AND rc.embedding IS NOT NULL
    ORDER BY rc.embedding <=> query_embedding ASC
    LIMIT (match_count * 3)
  ),
  text_search AS (
    SELECT
      rc.id,
      ts_rank_cd(to_tsvector('simple', rc.content), plainto_tsquery('simple', query_text))::float AS trank
    FROM public.rag_chunks rc
    WHERE
      (filter_committee IS NULL OR rc.committee_id = filter_committee)
      AND (filter_discipline IS NULL OR rc.discipline ILIKE '%' || filter_discipline || '%')
      AND (filter_doc_type IS NULL OR rc.document_type = filter_doc_type)
      AND to_tsvector('simple', rc.content) @@ plainto_tsquery('simple', query_text)
    ORDER BY trank DESC
    LIMIT (match_count * 3)
  )
  SELECT
    rc.id,
    rc.document_id,
    rc.document_type,
    rc.committee_id,
    rc.discipline,
    rc.title,
    rc.page_number,
    rc.content,
    rc.metadata,
    COALESCE(vs.sim, 0.0)::float AS similarity,
    COALESCE(ts.trank, 0.0)::float AS fts_rank,
    (COALESCE(vs.sim, 0.0) * 0.7 + COALESCE(ts.trank, 0.0) * 0.3)::float AS combined_score
  FROM public.rag_chunks rc
  LEFT JOIN vector_search vs ON rc.id = vs.id
  LEFT JOIN text_search ts ON rc.id = ts.id
  WHERE vs.id IS NOT NULL OR ts.id IS NOT NULL
  ORDER BY combined_score DESC
  LIMIT match_count;
END;
$$;

-- 6. Row Level Security (RLS) Politikaları
ALTER TABLE public.rag_chunks ENABLE ROW LEVEL SECURITY;

DO $$ 
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'Allow public read rag_chunks') THEN
    CREATE POLICY "Allow public read rag_chunks" ON public.rag_chunks FOR SELECT USING (true);
    CREATE POLICY "Allow public insert rag_chunks" ON public.rag_chunks FOR INSERT WITH CHECK (true);
    CREATE POLICY "Allow public update rag_chunks" ON public.rag_chunks FOR UPDATE USING (true);
    CREATE POLICY "Allow public delete rag_chunks" ON public.rag_chunks FOR DELETE USING (true);
  END IF;
END $$;
