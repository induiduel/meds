-- ==============================================================================
-- MedSoru Faz 2/3: Gelişmiş Hibrit Arama & Tıbbi Bilgi Grafı (GraphRAG) Şeması
-- ==============================================================================

-- 1. Tıbbi Bilgi Grafı Düğümleri (Knowledge Graph Nodes)
CREATE TABLE IF NOT EXISTS public.medical_graph_nodes (
    id TEXT PRIMARY KEY,                             -- 'Hastalik:Pnömoni', 'Ilac:Seftriakson'
    node_type TEXT NOT NULL,                         -- 'Ders', 'Konu', 'Hastalik', 'Belirti', 'Ilac', 'Gen'
    name TEXT NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Tıbbi Bilgi Grafı İlişkileri (Knowledge Graph Edges)
CREATE TABLE IF NOT EXISTS public.medical_graph_edges (
    id BIGSERIAL PRIMARY KEY,
    source_node TEXT NOT NULL REFERENCES public.medical_graph_nodes(id) ON DELETE CASCADE,
    target_node TEXT NOT NULL REFERENCES public.medical_graph_nodes(id) ON DELETE CASCADE,
    relation TEXT NOT NULL,                          -- 'NEDEN_OLUR', 'TEDAVİ_EDER', 'SEMPTOMUDUR'
    weight FLOAT DEFAULT 1.0,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(source_node, target_node, relation)
);

CREATE INDEX IF NOT EXISTS idx_graph_edges_source ON public.medical_graph_edges(source_node);
CREATE INDEX IF NOT EXISTS idx_graph_edges_target ON public.medical_graph_edges(target_node);

-- 3. MemGPT Öğrenci Bellek Tablosu (Core Memory & Recall)
CREATE TABLE IF NOT EXISTS public.student_ai_memory (
    user_id TEXT PRIMARY KEY,
    profile JSONB NOT NULL DEFAULT '{"donem": 3, "weak_topics": [], "mastered_topics": []}'::jsonb,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Supabase Hibrit Arama Fonksiyonu: Reciprocal Rank Fusion (RRF)
-- RRF_Score(d) = 1 / (60 + rank_dense) + 1 / (60 + rank_fts)
CREATE OR REPLACE FUNCTION hybrid_search_chunks (
    query_text TEXT,
    query_embedding vector(1024),
    match_count INT DEFAULT 10,
    rrf_k INT DEFAULT 60
)
RETURNS TABLE (
    id TEXT,
    content TEXT,
    title TEXT,
    discipline TEXT,
    final_score FLOAT,
    fts_rank INT,
    dense_rank INT,
    dense_similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    WITH fts_ranked AS (
        SELECT 
            rc.id,
            ROW_NUMBER() OVER (ORDER BY ts_rank_cd(to_tsvector('simple', rc.content), plainto_tsquery('simple', query_text)) DESC)::INT AS rank_fts
        FROM public.rag_chunks rc
        WHERE to_tsvector('simple', rc.content) @@ plainto_tsquery('simple', query_text)
        LIMIT match_count * 3
    ),
    dense_ranked AS (
        SELECT 
            rc.id,
            (1 - (rc.embedding <=> query_embedding))::FLOAT AS similarity,
            ROW_NUMBER() OVER (ORDER BY rc.embedding <=> query_embedding ASC)::INT AS rank_dense
        FROM public.rag_chunks rc
        WHERE rc.embedding IS NOT NULL
        LIMIT match_count * 3
    )
    SELECT 
        rc.id,
        rc.content,
        rc.title,
        rc.discipline,
        (
            COALESCE(1.0 / (rrf_k + dr.rank_dense), 0.0) +
            COALESCE(1.0 / (rrf_k + fr.rank_fts), 0.0)
        )::FLOAT AS final_score,
        fr.rank_fts,
        dr.rank_dense,
        COALESCE(dr.similarity, 0.0)::FLOAT AS dense_similarity
    FROM public.rag_chunks rc
    LEFT JOIN fts_ranked fr ON rc.id = fr.id
    LEFT JOIN dense_ranked dr ON rc.id = dr.id
    WHERE fr.id IS NOT NULL OR dr.id IS NOT NULL
    ORDER BY final_score DESC
    LIMIT match_count;
END;
$$;
