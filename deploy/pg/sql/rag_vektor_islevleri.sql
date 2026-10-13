-- RAG vektör işlevleri (idempotent). İki makinede:
--   docker exec -i meds-pg psql -U meds -d meds < deploy/pg/sql/rag_vektor_islevleri.sql
--
-- 2026-10-13: match_rag_chunks_* işlevleri "(filter IS NULL OR …)" kalıbı yüzünden genel planda HNSW yerine paralel
-- sıralı tarama seçiyordu (Oracle: ~1 sn/sorgu; zaman aşımı 1,5 sn). Artık yalnız verilen süzgeçlerle dinamik sorgu
-- kurulur, her çağrı gerçek değerlerle planlanır ve HNSW indeksi kullanılır (~0,1 sn). İmzalar/dönüş tipleri aynı.
-- Süzgeçli aramada sonuç eksik kalmasın diye pgvector 0.8 yinelemeli tarama açık.
--
-- related_rag_chunks: saklanan vektörden "bununla ilgili ne var?" (embed servisi gerekmez). Kullanan: /api/rag/related.

CREATE OR REPLACE FUNCTION public._rag_vector_query(col text, qv text, match_count integer, filter_types text[],
                                                   filter_committee text, exclude_id text, exclude_doc text)
RETURNS TABLE(id text, document_id text, document_type text, committee_id text, discipline text, title text,
              page_number integer, content text, metadata jsonb, similarity double precision)
LANGUAGE plpgsql STABLE
SET hnsw.iterative_scan = 'relaxed_order'
SET hnsw.ef_search = 80
AS $$
DECLARE
  w text := format('rc.%I IS NOT NULL', col);
BEGIN
  IF col NOT IN ('embedding_bge_m3', 'embedding_e5') THEN RAISE EXCEPTION 'geçersiz kolon %', col; END IF;
  IF filter_types IS NOT NULL THEN w := w || ' AND rc.document_type = ANY ($3)'; END IF;
  IF filter_committee IS NOT NULL THEN w := w || ' AND rc.committee_id = $4'; END IF;
  IF exclude_id IS NOT NULL THEN w := w || ' AND rc.id <> $5'; END IF;
  IF exclude_doc IS NOT NULL THEN w := w || ' AND rc.document_id <> $6'; END IF;
  RETURN QUERY EXECUTE format(
    'SELECT * FROM (SELECT rc.id, rc.document_id, rc.document_type, rc.committee_id, rc.discipline, rc.title,
            rc.page_number, rc.content, rc.metadata, 1 - (rc.%1$I <=> $1::vector) AS similarity
       FROM public.rag_chunks rc WHERE %2$s ORDER BY rc.%1$I <=> $1::vector LIMIT $2) s
     ORDER BY s.similarity DESC', col, w)
  USING qv, match_count, filter_types, filter_committee, exclude_id, exclude_doc;
END $$;

CREATE OR REPLACE FUNCTION public.match_rag_chunks_bge_m3(query_embedding vector, match_count integer DEFAULT 10,
                                                         filter_types text[] DEFAULT NULL::text[], filter_committee text DEFAULT NULL::text)
RETURNS TABLE(id text, document_id text, document_type text, committee_id text, discipline text, title text,
              page_number integer, content text, metadata jsonb, similarity double precision)
LANGUAGE sql STABLE
AS $$
  SELECT * FROM public._rag_vector_query('embedding_bge_m3', query_embedding::text, match_count, filter_types, filter_committee, NULL, NULL);
$$;

CREATE OR REPLACE FUNCTION public.match_rag_chunks_e5(query_embedding vector, match_count integer DEFAULT 10,
                                                     filter_types text[] DEFAULT NULL::text[], filter_committee text DEFAULT NULL::text)
RETURNS TABLE(id text, document_id text, document_type text, committee_id text, discipline text, title text,
              page_number integer, content text, metadata jsonb, similarity double precision)
LANGUAGE sql STABLE
AS $$
  SELECT * FROM public._rag_vector_query('embedding_e5', query_embedding::text, match_count, filter_types, filter_committee, NULL, NULL);
$$;
-- önceki sürümün işlev düzeyindeki ayarı (artık iç işlevde)
ALTER FUNCTION public.match_rag_chunks_bge_m3(vector, integer, text[], text) RESET ALL;
ALTER FUNCTION public.match_rag_chunks_e5(vector, integer, text[], text) RESET ALL;

CREATE OR REPLACE FUNCTION public.related_rag_chunks(
  source_id text,
  match_count integer DEFAULT 10,
  filter_types text[] DEFAULT NULL,
  filter_committee text DEFAULT NULL,
  exclude_same_document boolean DEFAULT true
)
RETURNS TABLE(id text, document_id text, document_type text, committee_id text, discipline text, title text,
              page_number integer, content text, metadata jsonb, similarity double precision)
LANGUAGE plpgsql STABLE
AS $$
DECLARE
  vb text;
  ve text;
  src_doc text;
BEGIN
  SELECT rc.embedding_bge_m3::text, rc.embedding_e5::text, rc.document_id INTO vb, ve, src_doc
  FROM public.rag_chunks rc WHERE rc.id = source_id;
  IF vb IS NULL AND ve IS NULL THEN RETURN; END IF;
  RETURN QUERY SELECT * FROM public._rag_vector_query(
    CASE WHEN vb IS NOT NULL THEN 'embedding_bge_m3' ELSE 'embedding_e5' END, coalesce(vb, ve), match_count,
    filter_types, filter_committee, source_id, CASE WHEN exclude_same_document THEN src_doc END);
END $$;
