-- ==============================================================================
-- MedSoru AI Etkileşimleri, Tartışmalar & Çok Modlu RAG Şeması
-- Supabase Dashboard > SQL Editor sekmesinde çalıştırın.
-- ==============================================================================

-- 1. AI Soru Etkileşimleri & Sohbet Kayıtları Tablosu
-- Her bir AI sohbeti, redaksiyon, açıklama ve kullanıcı sorusu burada saklanır.
CREATE TABLE IF NOT EXISTS public.ai_question_interactions (
  id TEXT PRIMARY KEY,
  question_id TEXT,                                      -- İlgili soru ID'si (örn: past-123 veya q-101)
  committee_id TEXT,                                     -- 'donem3-kurul1', 'donem3-kurul2', vb.
  discipline TEXT,                                       -- 'Tıbbi Patoloji', 'Tıbbi Farmakoloji', vb.
  topic TEXT,                                            -- Soru konusu veya başlığı
  interaction_type TEXT DEFAULT 'chat_qa',              -- 'chat_qa', 'refinement', 'redaction', 'mnemonic', 'trap_warning', 'user_comment'
  user_id TEXT,                                          -- Soruyu soran/işlem yapan öğrenci UID'si
  user_display_name TEXT,                                -- Öğrenci rumuzu / adı
  prompt TEXT NOT NULL,                                  -- Kullanıcının sorduğu soru veya AI talimatı
  response TEXT NOT NULL,                                -- Yapay zekanın verdiği yanıt/açıklama
  context_snapshot JSONB DEFAULT '{}'::jsonb,            -- Soru kökü, şıklar, doğru cevap ve slayt referansı
  metadata JSONB DEFAULT '{}'::jsonb,                    -- Model, sağlayıcı, token sayısı vb.
  upvotes INTEGER DEFAULT 0,                             -- Topluluk tarafından faydalı bulunma oyu
  rag_chunk_id TEXT,                                     -- rag_chunks tablosundaki karşılık gelen parça ID'si
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. İndeksler (Soruya ve komiteye göre anında çekebilmek için)
CREATE INDEX IF NOT EXISTS idx_ai_interactions_question ON public.ai_question_interactions (question_id);
CREATE INDEX IF NOT EXISTS idx_ai_interactions_committee ON public.ai_question_interactions (committee_id);
CREATE INDEX IF NOT EXISTS idx_ai_interactions_discipline ON public.ai_question_interactions (discipline);
CREATE INDEX IF NOT EXISTS idx_ai_interactions_type ON public.ai_question_interactions (interaction_type);
CREATE INDEX IF NOT EXISTS idx_ai_interactions_created ON public.ai_question_interactions (created_at DESC);

-- 3. Row Level Security (RLS)
ALTER TABLE public.ai_question_interactions ENABLE ROW LEVEL SECURITY;

DO $$ 
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'Allow public read ai_question_interactions') THEN
    CREATE POLICY "Allow public read ai_question_interactions" ON public.ai_question_interactions FOR SELECT USING (true);
    CREATE POLICY "Allow public insert ai_question_interactions" ON public.ai_question_interactions FOR INSERT WITH CHECK (true);
    CREATE POLICY "Allow public update ai_question_interactions" ON public.ai_question_interactions FOR UPDATE USING (true);
    CREATE POLICY "Allow public delete ai_question_interactions" ON public.ai_question_interactions FOR DELETE USING (true);
  END IF;
END $$;

-- 4. RAG Chunks tablosundaki ek belge türleri için destek
-- Belge türleri: 'lecture_slide', 'past_question', 'active_question', 'summary', 'transcript', 'user_contribution', 'ai_refinement', 'ai_qa'
CREATE INDEX IF NOT EXISTS idx_rag_chunks_type_doc ON public.rag_chunks (document_type, document_id);
