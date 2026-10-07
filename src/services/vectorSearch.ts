/**
 * Anlamsal (vektör) arama + karma sıralama (server-only).
 *
 * Sorgu meds-embed servisinde (127.0.0.1:8091, e5-small, CPU) vektöre çevrilir; yerel Supabase'deki
 * public.match_rag_chunks_e5 fonksiyonu en yakın parçaları döndürür (scripts/advanced_ai/rag_vector_build.py yazar).
 * BM25 (localRagEngine) sonuçlarıyla Reciprocal Rank Fusion ile birleştirilir. Servis ya da veritabanı yanıt vermezse
 * sessizce yalnız BM25 kullanılır (arama asla bozulmaz).
 *
 * VARSAYILAN KAPALI (açmak: MEDS_VECTOR_SEARCH=1). retrieval-eval (2026-10-07): BM25 kısmi kök hit@5 96 / ek değişmiş 92 /
 * konu 44; karma w=0.8 → 94/93/41, w=0.3 → 95/93/43. Öğrenci parçası sorgularında BM25 daha iyi; vektör yalnız
 * anlamca benzer (eş anlamlı) aramalarda yarar, onu ölçen bir test eklenince yeniden değerlendirilmeli.
 */
const EMBED_URL = process.env.MEDS_EMBED_URL || 'http://127.0.0.1:8091/embed';
const TIMEOUT_MS = Number(process.env.MEDS_VECTOR_TIMEOUT_MS || 1500);
const RRF_K = 60;
const VECTOR_WEIGHT = Number(process.env.MEDS_VECTOR_WEIGHT || 0.8);

type Row = Record<string, any> & { id: string };

let downUntil = 0; // servis düşükse bir süre denenmez (her aramada zaman aşımı beklenmesin)

function supabaseTarget() {
  const url = (process.env.LOCAL_SUPABASE_URL || process.env.SUPABASE_URL || 'http://127.0.0.1:8000').replace(/\/+$/, '');
  const key = process.env.LOCAL_SUPABASE_KEY || process.env.SUPABASE_SECRET_KEY || '';
  return { url, key };
}

async function withTimeout<T>(p: (signal: AbortSignal) => Promise<T>): Promise<T> {
  const ctl = new AbortController();
  const t = setTimeout(() => ctl.abort(), TIMEOUT_MS);
  try {
    return await p(ctl.signal);
  } finally {
    clearTimeout(t);
  }
}

export function vectorSearchEnabled(): boolean {
  return process.env.MEDS_VECTOR_SEARCH === '1' && Date.now() > downUntil;
}

/** Sorguya anlamsal olarak en yakın parçalar (yerel Supabase). Hata/kapalıysa boş liste. */
export async function semanticSearch(query: string, opts: { documentTypes?: string[]; committeeId?: string; limit?: number } = {}): Promise<Row[]> {
  if (!vectorSearchEnabled() || !query.trim()) return [];
  const { url, key } = supabaseTarget();
  if (!key) return [];
  try {
    const vec = await withTimeout(async (signal) => {
      const r = await fetch(EMBED_URL, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ texts: [query.slice(0, 1500)] }), signal });
      if (!r.ok) throw new Error(`embed ${r.status}`);
      return (await r.json()).vectors?.[0] as number[];
    });
    if (!Array.isArray(vec) || vec.length !== 384) return [];
    const rows = await withTimeout(async (signal) => {
      const r = await fetch(`${url}/rest/v1/rpc/match_rag_chunks_e5`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', apikey: key, Authorization: `Bearer ${key}` },
        body: JSON.stringify({
          query_embedding: `[${vec.join(',')}]`,
          match_count: opts.limit || 40,
          filter_types: opts.documentTypes?.length ? opts.documentTypes : null,
          filter_committee: opts.committeeId || null,
        }),
        signal,
      });
      if (!r.ok) throw new Error(`rpc ${r.status}`);
      return (await r.json()) as Row[];
    });
    return rows || [];
  } catch {
    downUntil = Date.now() + 60_000; // 1 dk yalnız BM25
    return [];
  }
}

/**
 * BM25 sonuçlarını anlamsal sonuçlarla Reciprocal Rank Fusion ile birleştirir.
 * toItem: vektör satırını BM25 sonuç biçimine çevirir (yalnız vektörün bulduğu parçalar için).
 */
export function fuseRRF<T extends { id: string }>(bm25: T[], vector: Row[], toItem: (r: Row) => T, limit: number): T[] {
  const score = new Map<string, number>();
  const item = new Map<string, T>();
  bm25.forEach((r, i) => {
    score.set(r.id, (score.get(r.id) || 0) + 1 / (RRF_K + i + 1));
    item.set(r.id, r);
  });
  vector.forEach((r, i) => {
    score.set(r.id, (score.get(r.id) || 0) + VECTOR_WEIGHT / (RRF_K + i + 1));
    if (!item.has(r.id)) item.set(r.id, toItem(r));
  });
  return [...score.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, limit)
    .map(([id]) => item.get(id)!)
    .filter(Boolean);
}
