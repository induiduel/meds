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
      let q: any = pgDb.from(table);
      if (action === 'select') q = q.select(b.columns || '*', { count: b.count, head: b.head });
      else if (action === 'insert') q = q.insert(b.rows || []);
      else if (action === 'upsert') q = q.upsert(b.rows || [], { onConflict: b.onConflict });
      else if (action === 'update') q = q.update(b.patch || {});
      else if (action === 'delete') {
        // Filtresiz toplu silme engellenir
        if (!b.filters?.length) return res.status(400).json({ data: null, count: null, error: { message: 'Filtresiz silme yapılamaz.' } });
        q = q.delete();
      } else return res.status(400).json({ data: null, count: null, error: { message: 'Geçersiz işlem.' } });

      if (action === 'update' && !b.filters?.length) {
        return res.status(400).json({ data: null, count: null, error: { message: 'Filtresiz güncelleme yapılamaz.' } });
      }
      for (const [op, col, val] of b.filters || []) {
        if (!FILTER_OPS.has(op)) return res.status(400).json({ data: null, count: null, error: { message: `Geçersiz filtre: ${op}` } });
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
      res.status(result.error ? 400 : 200).json(result);
    } catch (e: any) {
      res.status(400).json({ data: null, count: null, error: { message: e?.message || String(e) } });
    }
  });
}
