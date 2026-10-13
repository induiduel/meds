/**
 * Tarayıcı → sunucu → meds-pg sorgu kapısı (POST /api/db/query).
 *
 * Supabase döneminde tarayıcı veritabanına anonim anahtarla doğrudan bağlanıyordu (her tabloya yazabiliyordu).
 * Artık istemcideki `getSupabaseClient()` aynı zincir biçimini (from/select/eq/order/range...) JSON olarak bu uca
 * yollar; sunucu tablo/işlem beyaz listesi ve yönetici denetimiyle `pgDb` üzerinde çalıştırır.
 * Tanımlayıcılar pgDb içinde doğrulanır, değerler parametre olarak gider (SQL enjeksiyonu yok).
 */
import type express from 'express';
import { pgDb } from './pgDb';

const PUBLIC_READ = new Set(['committees', 'questions', 'past_questions', 'lecture_notes', 'practice_questions']);
const ADMIN_READ = new Set([...PUBLIC_READ, 'users', 'past_question_reports', 'system_status', 'answer_votes', 'ai_question_interactions']);
const ADMIN_WRITE = new Set(['committees', 'questions', 'past_questions', 'lecture_notes', 'past_question_reports', 'system_status', 'users']);
const MAX_ROWS = 1000;
const FILTER_OPS = new Set(['eq', 'neq', 'gt', 'gte', 'lt', 'lte', 'like', 'ilike', 'in', 'is', 'not']);

type Body = {
  table: string;
  action: 'select' | 'insert' | 'upsert' | 'update' | 'delete';
  columns?: string;
  count?: 'exact';
  head?: boolean;
  filters?: [string, string, any][];
  order?: [string, boolean][];
  range?: [number, number];
  limit?: number;
  single?: 'one' | 'maybe';
  rows?: any[];
  patch?: Record<string, any>;
  onConflict?: string;
};

const CACHEABLE_READ = new Set(['committees', 'questions', 'past_questions', 'lecture_notes', 'practice_questions', 'system_status']);
const SELECT_CACHE_TTL_MS = 15_000;
const MAX_CACHE_ENTRIES = 250;

type CacheEntry = { expiresAt: number; payload: any };
const selectCache = new Map<string, CacheEntry>();
const inflightSelects = new Map<string, Promise<any>>();

export function invalidateDbQueryCache(table?: string) {
  if (!table) {
    selectCache.clear();
    return;
  }
  const prefix = `${table}:`;
  for (const key of selectCache.keys()) {
    if (key.startsWith(prefix)) selectCache.delete(key);
  }
}

export function registerDbQueryRoute(app: express.Express, isRequestAdmin: (req: express.Request) => boolean) {
  app.post('/api/db/query', async (req, res) => {
    const b = (req.body || {}) as Body;
    const admin = isRequestAdmin(req);
    const action = b.action || 'select';
    const table = String(b.table || '');

    const allowed = action === 'select' ? (admin ? ADMIN_READ : PUBLIC_READ).has(table) : admin && ADMIN_WRITE.has(table);
    if (!allowed) {
      return res.status(403).json({ data: null, count: null, error: { message: 'Bu tabloya erişim yetkiniz yok.', code: '42501' } });
    }

    try {
      if (action !== 'select') {
        invalidateDbQueryCache(table);
      }

      const canCache = action === 'select' && CACHEABLE_READ.has(table);
      const cacheKey = canCache
        ? `${table}:${b.columns || '*'}:${b.count || ''}:${b.head ? 1 : 0}:${JSON.stringify(b.filters || [])}:${JSON.stringify(b.order || [])}:${JSON.stringify(b.range || [])}:${b.limit ?? ''}:${b.single || ''}`
        : '';

      if (canCache) {
        const hit = selectCache.get(cacheKey);
        if (hit && hit.expiresAt > Date.now()) {
          return res.status(200).json(hit.payload);
        }
        const pending = inflightSelects.get(cacheKey);
        if (pending) {
          const shared = await pending;
          return res.status(shared.error ? 400 : 200).json(shared);
        }
      }

      const runQuery = async () => {
        let q: any = pgDb.from(table);
        if (action === 'select') q = q.select(b.columns || '*', { count: b.count, head: b.head });
        else if (action === 'insert') q = q.insert(b.rows || []);
        else if (action === 'upsert') q = q.upsert(b.rows || [], { onConflict: b.onConflict });
        else if (action === 'update') q = q.update(b.patch || {});
        else if (action === 'delete') {
          if (!b.filters?.length) return { __badRequest: true, payload: { data: null, count: null, error: { message: 'Filtresiz silme yapılamaz.' } } };
          q = q.delete();
        } else return { __badRequest: true, payload: { data: null, count: null, error: { message: 'Geçersiz işlem.' } } };

        if (action === 'update' && !b.filters?.length) {
          return { __badRequest: true, payload: { data: null, count: null, error: { message: 'Filtresiz güncelleme yapılamaz.' } } };
        }
        for (const [op, col, val] of b.filters || []) {
          if (!FILTER_OPS.has(op)) return { __badRequest: true, payload: { data: null, count: null, error: { message: `Geçersiz filtre: ${op}` } } };
          q = op === 'not' ? q.not(col, val?.[0], val?.[1]) : q[op](col, val);
        }
        if (action === 'select') {
          for (const [col, asc] of b.order || []) q = q.order(col, { ascending: asc });
          const from = Math.max(0, Number(b.range?.[0] ?? 0));
          const to = b.range ? Number(b.range[1]) : from + Math.min(Number(b.limit ?? MAX_ROWS), MAX_ROWS) - 1;
          q = q.range(from, Math.min(to, from + MAX_ROWS - 1));
          if (b.single === 'one') q = q.single();
          else if (b.single === 'maybe') q = q.maybeSingle();
        }
        const result = await q;
        return { __badRequest: false, payload: result };
      };

      if (canCache) {
        const p = runQuery().then((r) => r.payload);
        inflightSelects.set(cacheKey, p);
        try {
          const result = await p;
          if (!result?.error) {
            if (selectCache.size >= MAX_CACHE_ENTRIES) {
              const oldest = selectCache.keys().next().value;
              if (oldest) selectCache.delete(oldest);
            }
            selectCache.set(cacheKey, { expiresAt: Date.now() + SELECT_CACHE_TTL_MS, payload: result });
          }
          return res.status(result?.error ? 400 : 200).json(result);
        } finally {
          inflightSelects.delete(cacheKey);
        }
      }

      const out = await runQuery();
      if (out.__badRequest) return res.status(400).json(out.payload);
      res.status(out.payload.error ? 400 : 200).json(out.payload);
    } catch (e: any) {
      res.status(400).json({ data: null, count: null, error: { message: e?.message || String(e) } });
    }
  });
}
