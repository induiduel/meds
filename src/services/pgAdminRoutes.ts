/**
 * Yönetim › Veritabanı gezgini: meds-pg'nin tüm tablolarını gör, ara, satır düzenle/ekle/sil, salt okunur SQL çalıştır.
 *
 * Güvenlik: kişisel veri (user_data, user_devices…) içerdiği için başlık e-postasına güvenmez — `isStrongAdmin`
 * (loopback, Firebase yönetici jetonu ya da MEDS_PANEL_SECRET). Yerel panel Oracle hedefindeyken istek yerel sunucuya
 * gelir (`x-panel-target: oracle`) ve gizli anahtarla Oracle'a iletilir (Kişiler ile aynı yol).
 * Tablo/sütun adları yalnız katalogdan gelen listeyle eşleşirse kullanılır; değerler her zaman parametredir.
 */
import type express from 'express';
import { pgDb } from './pgDb';
import { isLoopback, isStrongAdmin } from './peopleInsights';

type Col = { name: string; type: string; udt: string; nullable: boolean; def: string | null };
type Table = { name: string; rows: number; bytes: number; columns: Col[]; pk: string[] };

/** data/*.json'dan yansıyan tablolar: asıl kaynak JSON, burada yapılan düzeltme bir sonraki eşitlemede ezilebilir */
const MIRROR: Record<string, string> = {
  questions: 'data/db.json (Soru havuzu)',
  past_questions: 'data/pastQuestions.json (Çıkmış sorular)',
  practice_questions: 'örnek soru dosyaları',
  lecture_notes: 'ders notu dosyaları',
  committees: 'data/db.json (kurullar)',
  rag_chunks: 'data/local_rag_chunks.json (vektör hattı)',
};

const qi = (s: string) => `"${s.replace(/"/g, '""')}"`;
const LIMIT_MAX = 500;

export function registerPgAdminRoutes(app: express.Express, deps: { adminEmail: string; oracleApiUrl: string; isPgOnline: () => boolean }) {
  let cache: { at: number; tables: Table[] } | null = null;

  const loadTables = async (force = false): Promise<Table[]> => {
    if (!force && cache && Date.now() - cache.at < 30_000) return cache.tables;
    const t = await pgDb.query(
      `select c.relname as name, greatest(c.reltuples, 0)::bigint as est, coalesce(s.n_live_tup, 0)::bigint as live,
              pg_total_relation_size(c.oid)::bigint as bytes
         from pg_class c join pg_namespace n on n.oid = c.relnamespace
         left join pg_stat_user_tables s on s.relid = c.oid
        where n.nspname = 'public' and c.relkind in ('r', 'p')
        order by c.relname`,
    );
    const cols = await pgDb.query(
      `select table_name, column_name, data_type, udt_name, is_nullable = 'YES' as nullable, column_default, ordinal_position
         from information_schema.columns where table_schema = 'public' order by table_name, ordinal_position`,
    );
    const pks = await pgDb.query(
      `select tc.table_name, kcu.column_name from information_schema.table_constraints tc
         join information_schema.key_column_usage kcu on kcu.constraint_name = tc.constraint_name and kcu.table_schema = tc.table_schema
        where tc.table_schema = 'public' and tc.constraint_type = 'PRIMARY KEY' order by kcu.ordinal_position`,
    );
    const tables: Table[] = t.rows.map((r: any) => ({
      name: r.name,
      rows: Number(r.live) || Number(r.est) || 0,
      bytes: Number(r.bytes) || 0,
      columns: cols.rows
        .filter((c: any) => c.table_name === r.name)
        .map((c: any) => ({ name: c.column_name, type: c.data_type, udt: c.udt_name, nullable: !!c.nullable, def: c.column_default })),
      pk: pks.rows.filter((p: any) => p.table_name === r.name).map((p: any) => p.column_name),
    }));
    cache = { at: Date.now(), tables };
    return tables;
  };

  const tableOf = async (name: unknown) => {
    const t = (await loadTables()).find((x) => x.name === String(name || ''));
    if (!t) throw Object.assign(new Error('Tablo bulunamadı.'), { status: 404 });
    return t;
  };
  /** Sütun türüne göre parametre ifadesi: $n::tür (tür katalogdan gelir) */
  const castOf = (c: Col, n: number) => {
    if (c.udt === 'vector') return `$${n}::vector`;
    if (c.type === 'ARRAY') return `$${n}::${qi(c.udt.replace(/^_/, ''))}[]`;
    if (c.type === 'USER-DEFINED') return `$${n}::${qi(c.udt)}`;
    return `$${n}::${c.udt === 'bpchar' ? 'text' : qi(c.udt)}`;
  };
  const valueOf = (c: Col, v: unknown) => {
    if (v === null || v === undefined) return null;
    if (c.udt === 'json' || c.udt === 'jsonb') return typeof v === 'string' ? v : JSON.stringify(v);
    if (c.type === 'ARRAY' && Array.isArray(v)) return v;
    if (typeof v === 'object') return JSON.stringify(v);
    return v;
  };
  /** Satır seçimi: birincil anahtar varsa onunla, yoksa ctid ile */
  const whereOf = (t: Table, key: Record<string, unknown>, start: number) => {
    const values: unknown[] = [];
    if (t.pk.length) {
      const parts = t.pk.map((k) => {
        if (!(k in key)) throw Object.assign(new Error(`Anahtar alanı eksik: ${k}`), { status: 400 });
        values.push(key[k]);
        return `${qi(k)}::text = $${start + values.length}::text`;
      });
      return { sql: parts.join(' and '), values };
    }
    if (typeof key.ctid !== 'string' || !/^\(\d+,\d+\)$/.test(key.ctid)) throw Object.assign(new Error('Satır kimliği (ctid) geçersiz.'), { status: 400 });
    values.push(key.ctid);
    return { sql: `ctid = $${start + 1}::tid`, values };
  };

  const proxyToOracle = async (req: express.Request, res: express.Response) => {
    const secret = String(process.env.MEDS_PANEL_SECRET || '').trim();
    if (!secret) return res.status(503).json({ error: 'MEDS_PANEL_SECRET tanımlı değil; canlı veritabanına yerelden ulaşılamıyor.' });
    try {
      const r = await fetch(`${deps.oracleApiUrl.replace(/\/$/, '')}${req.originalUrl}`, {
        method: req.method,
        headers: { 'content-type': 'application/json', 'x-panel-secret': secret, 'x-admin-email': deps.adminEmail },
        body: req.method === 'GET' ? undefined : JSON.stringify(req.body || {}),
      });
      res.status(r.status).type(r.headers.get('content-type') || 'application/json').send(Buffer.from(await r.arrayBuffer()));
    } catch (e: any) {
      res.status(502).json({ error: `Oracle'a ulaşılamadı: ${e?.message || e}` });
    }
  };
  const guard = async (req: express.Request, res: express.Response): Promise<boolean> => {
    if (!(await isStrongAdmin(req, deps.adminEmail))) {
      res.status(403).json({ error: 'Veritabanına yalnız doğrulanmış yönetici oturumu erişebilir.' });
      return false;
    }
    if (req.headers['x-panel-target'] === 'oracle' && isLoopback(req)) {
      await proxyToOracle(req, res);
      return false;
    }
    if (!deps.isPgOnline()) {
      res.status(503).json({ error: 'meds-pg çevrimdışı.' });
      return false;
    }
    res.setHeader('Cache-Control', 'no-store');
    return true;
  };
  const fail = (res: express.Response, e: any) => res.status(e?.status || 500).json({ error: e?.message || String(e) });

  app.get('/api/admin/pg/tables', async (req, res) => {
    if (!(await guard(req, res))) return;
    try {
      const tables = await loadTables(req.query.yenile === '1');
      const size = await pgDb.query(`select pg_database_size(current_database())::bigint as b, version() as v`);
      res.json({ tables: tables.map((t) => ({ ...t, mirror: MIRROR[t.name] || null })), databaseBytes: Number(size.rows[0]?.b) || 0, version: String(size.rows[0]?.v || '').split(' on ')[0], at: new Date().toISOString() });
    } catch (e) {
      fail(res, e);
    }
  });

  app.get('/api/admin/pg/rows', async (req, res) => {
    if (!(await guard(req, res))) return;
    try {
      const t = await tableOf(req.query.table);
      const limit = Math.min(LIMIT_MAX, Math.max(1, Number(req.query.limit) || 50));
      const offset = Math.max(0, Number(req.query.offset) || 0);
      const vec = t.columns.filter((c) => c.udt === 'vector').map((c) => c.name);
      // Vektör sütunları satırda taşınmaz (1024 sayı); yerine boyutu gösterilir
      // Büyük metin/JSON (ör. user_data.data) listede kısaltılır; satır açılınca /row tam halini getirir
      const sel = t.columns.map((c) =>
        c.udt === 'vector'
          ? `case when ${qi(c.name)} is null then null else 'vektör · ' || vector_dims(${qi(c.name)}) end as ${qi(c.name)}`
          : ['json', 'jsonb', 'text', 'varchar'].includes(c.udt)
            ? `case when length(${qi(c.name)}::text) > 600 then left(${qi(c.name)}::text, 240) || ' … (' || length(${qi(c.name)}::text) || ' karakter)' else ${qi(c.name)}::text end as ${qi(c.name)}`
            : qi(c.name),
      );
      const values: unknown[] = [];
      let where = '';
      const q = String(req.query.q || '').trim();
      if (q) {
        values.push(`%${q}%`);
        const col = String(req.query.col || '');
        if (col && t.columns.some((c) => c.name === col)) where = `where ${qi(col)}::text ilike $1`;
        else where = `where (to_jsonb(t)${vec.map((v) => ` - '${v.replace(/'/g, "''")}'`).join('')})::text ilike $1`;
      }
      const ord = t.columns.find((c) => c.name === String(req.query.order || ''));
      const dir = req.query.dir === 'asc' ? 'asc' : 'desc';
      const order = ord ? `order by ${qi(ord.name)} ${dir} nulls last` : t.pk.length ? `order by ${t.pk.map(qi).join(', ')} ${dir}` : '';
      await pgDb.query('select 1');
      const rows = await pgDb.query(
        `select ctid::text as "__ctid", ${sel.join(', ')} from ${qi(t.name)} t ${where} ${order} limit ${limit} offset ${offset}`,
        values,
      );
      const count = q
        ? Number((await pgDb.query(`select count(*)::bigint as n from ${qi(t.name)} t ${where}`, values)).rows[0]?.n) || 0
        : t.rows;
      res.json({ table: t.name, rows: rows.rows, total: count, exact: !!q, limit, offset });
    } catch (e) {
      fail(res, e);
    }
  });

  // Tek satırın tam hali (düzenleme çekmecesi)
  app.get('/api/admin/pg/row', async (req, res) => {
    if (!(await guard(req, res))) return;
    try {
      const t = await tableOf(req.query.table);
      let key: Record<string, unknown> = {};
      try { key = JSON.parse(String(req.query.key || '{}')); } catch { /* boş */ }
      const w = whereOf(t, key, 0);
      const sel = t.columns.map((c) => (c.udt === 'vector' ? `case when ${qi(c.name)} is null then null else 'vektör · ' || vector_dims(${qi(c.name)}) end as ${qi(c.name)}` : qi(c.name)));
      const r = await pgDb.query(`select ctid::text as "__ctid", ${sel.join(', ')} from ${qi(t.name)} where ${w.sql} limit 2`, w.values);
      if (r.rows.length !== 1) return res.status(404).json({ error: 'Satır bulunamadı (silinmiş ya da anahtarı değişmiş olabilir).' });
      res.json({ row: r.rows[0] });
    } catch (e) {
      fail(res, e);
    }
  });

  app.patch('/api/admin/pg/row', async (req, res) => {
    if (!(await guard(req, res))) return;
    try {
      const t = await tableOf(req.body?.table);
      const set: Record<string, unknown> = req.body?.set && typeof req.body.set === 'object' ? req.body.set : {};
      const cols = Object.keys(set).map((k) => t.columns.find((c) => c.name === k)).filter((c): c is Col => !!c && c.udt !== 'vector');
      if (!cols.length) return res.status(400).json({ error: 'Değişecek sütun yok.' });
      const values: unknown[] = cols.map((c) => valueOf(c, set[c.name]));
      const w = whereOf(t, req.body?.key || {}, values.length);
      const r = await pgDb.query(
        `update ${qi(t.name)} set ${cols.map((c, i) => `${qi(c.name)} = ${castOf(c, i + 1)}`).join(', ')} where ${w.sql}`,
        [...values, ...w.values],
      );
      if (r.rowCount !== 1) return res.status(409).json({ error: `Güncelleme ${r.rowCount} satırı etkiledi (1 bekleniyordu).` });
      res.json({ success: true });
    } catch (e) {
      fail(res, e);
    }
  });

  app.post('/api/admin/pg/row', async (req, res) => {
    if (!(await guard(req, res))) return;
    try {
      const t = await tableOf(req.body?.table);
      const vals: Record<string, unknown> = req.body?.values && typeof req.body.values === 'object' ? req.body.values : {};
      const cols = Object.keys(vals).map((k) => t.columns.find((c) => c.name === k)).filter((c): c is Col => !!c && c.udt !== 'vector');
      if (!cols.length) return res.status(400).json({ error: 'En az bir alan gir.' });
      const r = await pgDb.query(
        `insert into ${qi(t.name)} (${cols.map((c) => qi(c.name)).join(', ')}) values (${cols.map((c, i) => castOf(c, i + 1)).join(', ')}) returning ctid::text as "__ctid"`,
        cols.map((c) => valueOf(c, vals[c.name])),
      );
      cache = null;
      res.json({ success: true, ctid: r.rows[0]?.__ctid || null });
    } catch (e) {
      fail(res, e);
    }
  });

  app.delete('/api/admin/pg/row', async (req, res) => {
    if (!(await guard(req, res))) return;
    try {
      const t = await tableOf(req.body?.table);
      const w = whereOf(t, req.body?.key || {}, 0);
      const r = await pgDb.query(`delete from ${qi(t.name)} where ${w.sql}`, w.values);
      if (r.rowCount !== 1) return res.status(409).json({ error: `Silme ${r.rowCount} satırı etkiledi (1 bekleniyordu).` });
      cache = null;
      res.json({ success: true });
    } catch (e) {
      fail(res, e);
    }
  });

  // Salt okunur SQL: READ ONLY işlem + 10 sn zaman aşımı + en çok 1000 satır
  app.post('/api/admin/pg/sql', async (req, res) => {
    if (!(await guard(req, res))) return;
    const sql = String(req.body?.sql || '').trim().replace(/;\s*$/, '');
    if (!sql) return res.status(400).json({ error: 'Sorgu boş.' });
    if (sql.includes(';')) return res.status(400).json({ error: 'Tek sorgu çalıştırılabilir (noktalı virgül yok).' });
    const { pgPool } = await import('./pgDb');
    const client = await pgPool.connect();
    const t0 = Date.now();
    try {
      await client.query('begin read only');
      await client.query(`set local statement_timeout = 10000`);
      const r = await client.query({ text: sql, rowMode: 'array' });
      await client.query('rollback');
      const fields = (r.fields || []).map((f: any) => f.name);
      res.json({ fields, rows: (r.rows || []).slice(0, 1000), total: r.rowCount ?? (r.rows || []).length, truncated: (r.rows || []).length > 1000, ms: Date.now() - t0 });
    } catch (e: any) {
      await client.query('rollback').catch(() => {});
      res.status(400).json({ error: e?.message || String(e) });
    } finally {
      client.release();
    }
  });
}
