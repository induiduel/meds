/**
 * Anlamsal (vektör) arama + karma sıralama (server-only).
 *
 * Sorgu meds-embed servisinde (127.0.0.1:8091, e5-small, CPU) vektöre çevrilir; meds-pg'deki
 * public.match_rag_chunks_e5 / _bge_m3 fonksiyonu en yakın parçaları döndürür (scripts/advanced_ai/rag_vector_build.py yazar).
 * BM25 (localRagEngine) sonuçlarıyla Reciprocal Rank Fusion ile birleştirilir. Servis ya da veritabanı yanıt vermezse
 * sessizce yalnız BM25 kullanılır (arama asla bozulmaz).
 *
 * VARSAYILAN KAPALI (açmak: MEDS_VECTOR_SEARCH=1). retrieval-eval (2026-10-07): BM25 kısmi kök hit@5 96 / ek değişmiş 92 /
 * konu 44; karma w=0.8 → 94/93/41, w=0.3 → 95/93/43. Öğrenci parçası sorgularında BM25 daha iyi; vektör yalnız
 * anlamca benzer (eş anlamlı) aramalarda yarar, onu ölçen bir test eklenince yeniden değerlendirilmeli.
 */
import { pgDb } from './pgDb';

const EMBED_URL = process.env.MEDS_EMBED_URL || process.env.MEDS_EMBED_BGE_URL || 'http://127.0.0.1:8094/embed';
const TIMEOUT_MS = Number(process.env.MEDS_VECTOR_TIMEOUT_MS || 1500);
const RRF_K = 60;
const VECTOR_WEIGHT = Number(process.env.MEDS_VECTOR_WEIGHT || 0.8);

/**
 * Halk dili → tıbbi terim eşanlamlısı (yalnız VEKTÖR sorgusuna eklenir; BM25 aynen kalır).
 * Amaç: "kansızlık/alyuvar" gibi günlük dilin dense aramada kaybolmaması.
 */
const MEDICAL_SYNONYMS: Array<[string, string]> = [
  ['kırmızı küre', 'eritrosit'],
  ['beyaz küre', 'lökosit'],
  ['kan pulcuğu', 'trombosit'],
  ['kansızlık', 'anemi'],
  ['alyuvar', 'eritrosit'],
  ['akyuvar', 'lökosit'],
  ['yüksek tansiyon', 'hipertansiyon'],
  ['düşük tansiyon', 'hipotansiyon'],
  ['şeker hastalığı', 'diyabet diabetes mellitus'],
  ['kalp krizi', 'miyokard enfarktüsü'],
  ['nefes darlığı', 'dispne'],
  ['sarılık', 'ikter hiperbilirubinemi'],
  ['ishal', 'diyare'],
  ['kabızlık', 'konstipasyon'],
  ['çarpıntı', 'palpitasyon'],
  ['kaşıntı', 'pruritus'],
  ['böbrek yetmezliği', 'renal yetmezlik'],
  ['karaciğer yağlanması', 'hepatosteatoz'],
];

export function expandMedicalQuery(query: string): string {
  const q = query.toLowerCase();
  const add: string[] = [];
  for (const [halk, tip] of MEDICAL_SYNONYMS) {
    if (q.includes(halk) && !q.includes(tip.split(' ')[0])) add.push(tip);
  }
  return add.length ? `${query} ${add.join(' ')}`.slice(0, 1500) : query;
}

type Row = Record<string, any> & { id: string };

// Aynı sorgu (ör. öneri + arama, sayfa yenileme) embed servisine yeniden gitmesin
const queryVecCache = new Map<string, number[]>();

let downUntil = 0; // servis düşükse bir süre denenmez (her aramada zaman aşımı beklenmesin)

async function withTimeout<T>(p: (signal: AbortSignal) => Promise<T>): Promise<T> {
  const ctl = new AbortController();
  let t: ReturnType<typeof setTimeout> | undefined;
  // Postgres sorgusu sinyali dinlemez; yarış ile arama süresi yine TIMEOUT_MS ile sınırlanır.
  const timeout = new Promise<never>((_, reject) => {
    t = setTimeout(() => {
      ctl.abort();
      reject(new Error('timeout'));
    }, TIMEOUT_MS);
  });
  try {
    return await Promise.race([p(ctl.signal), timeout]);
  } finally {
    clearTimeout(t);
  }
}

export function vectorSearchEnabled(): boolean {
  const flag = process.env.MEDS_VECTOR_SEARCH;
  const enabled = flag !== undefined ? flag === '1' : Boolean(process.env.MEDS_EMBED_URL);
  return enabled && Date.now() > downUntil;
}

/** Sorguya anlamsal olarak en yakın parçalar (meds-pg pgvector). Hata/kapalıysa boş liste. */
export async function semanticSearch(query: string, opts: { documentTypes?: string[]; committeeId?: string; limit?: number } = {}): Promise<Row[]> {
  if (!vectorSearchEnabled() || !query.trim()) return [];
  try {
    const vecQuery = expandMedicalQuery(query).slice(0, 1500);
    let vec = queryVecCache.get(vecQuery);
    if (vec) {
      queryVecCache.delete(vecQuery);
      queryVecCache.set(vecQuery, vec);
    } else {
      vec = await withTimeout(async (signal) => {
        const r = await fetch(EMBED_URL, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ texts: [vecQuery] }), signal });
        if (!r.ok) throw new Error(`embed ${r.status}`);
        return (await r.json()).vectors?.[0] as number[];
      });
      if (Array.isArray(vec)) {
        queryVecCache.set(vecQuery, vec);
        if (queryVecCache.size > 500) queryVecCache.delete(queryVecCache.keys().next().value as string);
      }
    }
    if (!Array.isArray(vec) || (vec.length !== 384 && vec.length !== 1024)) return [];
    // bge-m3 (1024) test kolonu; 384 varsayılan yol aynen korunur.
    const rpcFn = vec.length === 1024 ? 'match_rag_chunks_bge_m3' : 'match_rag_chunks_e5';
    // Yassı skor gürültü filtresi: çok düşük güvenli vektör kuyruğu RRF'ye girmez.
    // Not: mutlak eşik tek başına yetmez (serotonin≈troponin gibi 0.56'lık karışmalar
    // paraphrase kazançlarının 0.47'sinden yüksek olabilir); eşik 0.45 = yalnız kuyruk keser.
    const MIN_SIM = vec.length === 1024
      ? Number(process.env.MEDS_VECTOR_MIN_SIM_BGE || 0.45)
      : Number(process.env.MEDS_VECTOR_MIN_SIM_E5 || 0.8);
    const rows = await withTimeout(async () => {
      const { data, error } = await pgDb.rpc(rpcFn, {
        query_embedding: vec,
        match_count: opts.limit || 40,
        filter_types: opts.documentTypes?.length ? opts.documentTypes : null,
        filter_committee: opts.committeeId || null,
      });
      if (error) throw new Error(`rpc ${error.message}`);
      return ((data || []) as Row[]).filter((rw) => (Number(rw.similarity) || 0) >= MIN_SIM);
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

/**
 * Saklanan vektörden anlamsal olarak ilişkili parçalar (embed servisi gerekmez; meds-pg related_rag_chunks).
 * Çok işlevli: soru → ilgili slayt/özet/deste, benzer çıkmış soru, kopya adayı (similarity ≥ ~0.95).
 * Aynı belgeden en çok `perDocument` parça döner (tek destenin 10 slaytı listeyi doldurmasın). Hata → boş liste.
 */
const relatedCache = new Map<string, { at: number; rows: Row[] }>();
const RELATED_TTL_MS = 10 * 60_000;

export async function relatedChunks(
  sourceChunkId: string,
  opts: { documentTypes?: string[]; committeeId?: string; limit?: number; minSim?: number; perDocument?: number } = {},
): Promise<Row[]> {
  if (!sourceChunkId) return [];
  const limit = Math.min(Math.max(opts.limit || 8, 1), 30);
  const perDoc = Math.max(opts.perDocument ?? 2, 1);
  const key = JSON.stringify([sourceChunkId, opts.documentTypes || null, opts.committeeId || null, limit, opts.minSim ?? null, perDoc]);
  const hit = relatedCache.get(key);
  if (hit && Date.now() - hit.at < RELATED_TTL_MS) return hit.rows;
  try {
    const { data, error } = await pgDb.rpc('related_rag_chunks', {
      source_id: sourceChunkId,
      match_count: limit * 4,
      filter_types: opts.documentTypes?.length ? opts.documentTypes : null,
      filter_committee: opts.committeeId || null,
      exclude_same_document: true,
    });
    if (error) throw new Error(error.message);
    const minSim = opts.minSim ?? 0.5;
    const perDocCount = new Map<string, number>();
    const rows: Row[] = [];
    for (const r of (data || []) as Row[]) {
      if ((Number(r.similarity) || 0) < minSim) continue;
      const d = `${r.document_type}:${r.document_id}`;
      const n = perDocCount.get(d) || 0;
      if (n >= perDoc) continue;
      perDocCount.set(d, n + 1);
      rows.push(r);
      if (rows.length >= limit) break;
    }
    relatedCache.set(key, { at: Date.now(), rows });
    if (relatedCache.size > 2000) relatedCache.delete(relatedCache.keys().next().value as string);
    return rows;
  } catch (err: any) {
    console.warn('[vectorSearch] related_rag_chunks:', err?.message || err);
    return [];
  }
}

/** Belge kimliğinden (ör. çıkmış soru id'si) o belgenin ilk parçasının kimliği. */
export async function chunkIdForDocument(documentType: string, documentId: string): Promise<string | null> {
  try {
    const r = await pgDb.query(
      'select id from rag_chunks where document_type = $1 and document_id = $2 order by page_number nulls first, id limit 1',
      [documentType, documentId],
    );
    return r.rows[0]?.id || null;
  } catch {
    return null;
  }
}
