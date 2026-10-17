/**
 * Sunucu tarafı Postgres erişimi (meds-pg: Postgres + pgvector). Supabase'in yerini alır.
 *
 * - Tek havuz (`pg.Pool`), yalnız sunucu sürecinde kullanılır; tarayıcı veritabanına hiç bağlanmaz.
 * - `pgDb.from(table)`: eski Supabase çağrılarının kullandığı sorgu biçiminin (select/eq/in/order/
 *   range/upsert/update/delete...) yalnız projede geçen alt kümesi. Dönüş `{ data, error, count }`.
 * - jsonb sütunları sütun türüne bakılarak JSON'a çevrilir (node-pg JS dizisini PG dizisi sanar).
 * - `pgListen`: LISTEN/NOTIFY için ayrı, kendini yeniden bağlayan istemci (canlı yayın kaynağı).
 */
import pg from 'pg';
import dotenv from 'dotenv';

// ESM içe aktarmaları server.ts'teki dotenv.config()'ten önce çalışır; adres burada okunmalı.
dotenv.config();

const DATABASE_URL = process.env.DATABASE_URL || 'postgres://meds@127.0.0.1:54330/meds';

export const pgPool = new pg.Pool({
  connectionString: DATABASE_URL,
  max: Number(process.env.PG_POOL_MAX || 10),
  idleTimeoutMillis: 30_000,
  connectionTimeoutMillis: 5_000,
  statement_timeout: 30_000,
  application_name: 'meds-app',
});
pgPool.on('error', (err) => console.warn('[pgDb] havuz hatası:', err.message));

export type PgResult<T = any> = { data: T | null; error: { message: string; code?: string } | null; count: number | null };

const IDENT = /^[a-z_][a-z0-9_]*$/;
function ident(name: string): string {
  if (!IDENT.test(name)) throw new Error(`Geçersiz tanımlayıcı: ${name}`);
  return `"${name}"`;
}

// Sütun türü önbelleği: jsonb/json sütunlarına giden değerler JSON.stringify edilir.
const columnTypes = new Map<string, Promise<Map<string, string>>>();
function getColumnTypes(table: string): Promise<Map<string, string>> {
  let p = columnTypes.get(table);
  if (!p) {
    p = pgPool
      .query(
        `select column_name, udt_name from information_schema.columns where table_schema = 'public' and table_name = $1`,
        [table]
      )
      .then((r) => new Map(r.rows.map((row: any) => [row.column_name, row.udt_name])))
      .catch((e) => {
        columnTypes.delete(table);
        throw e;
      });
    columnTypes.set(table, p);
  }
  return p;
}

function toParam(value: any, udt: string | undefined): any {
  if (value === undefined) return null;
  if (value === null) return null;
  if (udt === 'jsonb' || udt === 'json') return JSON.stringify(value);
  if (udt === 'vector' && Array.isArray(value)) return `[${value.join(',')}]`;
  return value;
}

type Filter = { sql: (p: (v: any) => string) => string };
type Mode = 'select' | 'insert' | 'upsert' | 'update' | 'delete';

class QueryBuilder<T = any> implements PromiseLike<PgResult<T>> {
  private mode: Mode = 'select';
  private columns = '*';
  private countMode: 'exact' | null = null;
  private headOnly = false;
  private filters: Filter[] = [];
  private orders: string[] = [];
  private limitN: number | null = null;
  private offsetN: number | null = null;
  private singleMode: 'one' | 'maybe' | null = null;
  private rows: any[] = [];
  private patch: Record<string, any> = {};
  private conflict: string | null = null;
  private ignoreDuplicates = false;
  private skipUnchanged: string | null = null;
  private returning = false;

  constructor(private table: string) {
    ident(table);
  }

  select(columns = '*', opts?: { count?: 'exact'; head?: boolean }) {
    if (this.mode === 'select') {
      this.columns = columns;
      if (opts?.count) this.countMode = 'exact';
      if (opts?.head) this.headOnly = true;
    } else {
      this.returning = true;
      this.columns = columns;
    }
    return this;
  }
  insert(rows: any | any[]) {
    this.mode = 'insert';
    this.rows = Array.isArray(rows) ? rows : [rows];
    return this;
  }
  /** `skipUnchangedColumn`: o sütun değişmemişse satır güncellenmez (gereksiz NOTIFY/WAL yok). */
  upsert(rows: any | any[], opts?: { onConflict?: string; ignoreDuplicates?: boolean; skipUnchangedColumn?: string }) {
    this.mode = 'upsert';
    this.skipUnchanged = opts?.skipUnchangedColumn || null;
    this.rows = Array.isArray(rows) ? rows : [rows];
    this.conflict = opts?.onConflict || null;
    this.ignoreDuplicates = Boolean(opts?.ignoreDuplicates);
    return this;
  }
  update(patch: Record<string, any>) {
    this.mode = 'update';
    this.patch = patch;
    return this;
  }
  delete() {
    this.mode = 'delete';
    return this;
  }

  private op(col: string, sqlOp: string, value: any) {
    ident(col);
    this.filters.push({ sql: (p) => `"${col}" ${sqlOp} ${p(value)}` });
    return this;
  }
  eq(col: string, v: any) { return this.op(col, '=', v); }
  neq(col: string, v: any) { return this.op(col, '<>', v); }
  gt(col: string, v: any) { return this.op(col, '>', v); }
  gte(col: string, v: any) { return this.op(col, '>=', v); }
  lt(col: string, v: any) { return this.op(col, '<', v); }
  lte(col: string, v: any) { return this.op(col, '<=', v); }
  like(col: string, v: string) { return this.op(col, 'like', v); }
  ilike(col: string, v: string) { return this.op(col, 'ilike', v); }
  is(col: string, v: null | boolean) {
    ident(col);
    const lit = v === null ? 'null' : v ? 'true' : 'false';
    this.filters.push({ sql: () => `"${col}" is ${lit}` });
    return this;
  }
  in(col: string, values: any[]) {
    ident(col);
    this.filters.push({ sql: (p) => `"${col}" = any(${p(values)})` });
    return this;
  }
  not(col: string, operator: string, v: any) {
    ident(col);
    if (operator === 'is' && v === null) this.filters.push({ sql: () => `"${col}" is not null` });
    else this.filters.push({ sql: (p) => `not ("${col}" = ${p(v)})` });
    return this;
  }
  order(col: string, opts?: { ascending?: boolean; nullsFirst?: boolean }) {
    ident(col);
    const dir = opts?.ascending === false ? 'desc' : 'asc';
    const nulls = opts?.nullsFirst === undefined ? '' : opts.nullsFirst ? ' nulls first' : ' nulls last';
    this.orders.push(`"${col}" ${dir}${nulls}`);
    return this;
  }
  limit(n: number) {
    this.limitN = Math.max(0, Math.floor(n));
    return this;
  }
  range(from: number, to: number) {
    this.offsetN = Math.max(0, Math.floor(from));
    this.limitN = Math.max(0, Math.floor(to) - this.offsetN + 1);
    return this;
  }
  maybeSingle() {
    this.singleMode = 'maybe';
    return this;
  }
  // `.single()` Supabase'te satır yoksa hata döner; aynı davranış korunur.
  single() {
    this.singleMode = 'one';
    return this;
  }

  private selectList(): string {
    if (this.columns.trim() === '*') return '*';
    return this.columns
      .split(',')
      .map((c) => c.trim())
      .filter(Boolean)
      .map((c) => ident(c))
      .join(', ');
  }

  private async build(): Promise<{ text: string; values: any[]; countText?: string; countValues?: any[] }> {
    const values: any[] = [];
    const types = this.mode === 'select' || this.mode === 'delete' ? null : await getColumnTypes(this.table);
    const p = (v: any) => {
      values.push(v);
      return `$${values.length}`;
    };
    const where = () => (this.filters.length ? ` where ${this.filters.map((f) => f.sql(p)).join(' and ')}` : '');
    const ret = this.returning ? ` returning ${this.selectList()}` : '';
    const t = ident(this.table);

    if (this.mode === 'select') {
      const w = where();
      const filterValues = values.slice();
      let text = `select ${this.selectList()} from ${t}${w}`;
      if (this.orders.length) text += ` order by ${this.orders.join(', ')}`;
      if (this.limitN !== null) text += ` limit ${this.limitN}`;
      if (this.offsetN !== null) text += ` offset ${this.offsetN}`;
      const countText = this.countMode ? `select count(*)::int as n from ${t}${w}` : undefined;
      return { text, values, countText, countValues: filterValues };
    }
    if (this.mode === 'delete') {
      return { text: `delete from ${t}${where()}${ret}`, values };
    }
    if (this.mode === 'update') {
      const sets = Object.entries(this.patch)
        .filter(([, v]) => v !== undefined)
        .map(([k, v]) => `${ident(k)} = ${p(toParam(v, types!.get(k)))}`);
      if (!sets.length) throw new Error('Boş güncelleme');
      return { text: `update ${t} set ${sets.join(', ')}${where()}${ret}`, values };
    }
    // insert / upsert: satırlardaki tüm anahtarların birleşimi (eksik olanlar default/null)
    const cols = Array.from(
      new Set(this.rows.flatMap((r) => Object.keys(r).filter((k) => r[k] !== undefined && types!.has(k))))
    );
    if (!cols.length || !this.rows.length) throw new Error('Boş ekleme');
    const tuples = this.rows.map(
      (r) => `(${cols.map((c) => (c in r && r[c] !== undefined ? p(toParam(r[c], types!.get(c))) : 'default')).join(', ')})`
    );
    let text = `insert into ${t} (${cols.map(ident).join(', ')}) values ${tuples.join(', ')}`;
    if (this.mode === 'upsert') {
      const keys = (this.conflict || (types!.has('id') ? 'id' : 'uid')).split(',').map((s) => s.trim());
      keys.forEach(ident);
      const updatable = cols.filter((c) => !keys.includes(c));
      if (this.ignoreDuplicates || !updatable.length) text += ` on conflict (${keys.map(ident).join(', ')}) do nothing`;
      else
        text += ` on conflict (${keys.map(ident).join(', ')}) do update set ${updatable
          .map((c) => `${ident(c)} = excluded.${ident(c)}`)
          .join(', ')}${
          this.skipUnchanged ? ` where ${t}.${ident(this.skipUnchanged)} is distinct from excluded.${ident(this.skipUnchanged)}` : ''
        }`;
    }
    return { text: text + ret, values };
  }

  async execute(): Promise<PgResult<T>> {
    try {
      // Aynı satır tek ifadede iki kez upsert edilirse PG hata verir; son kopya kazanır.
      if (this.mode === 'upsert' && this.rows.length > 1) {
        const key = (this.conflict || 'id').split(',').map((s) => s.trim());
        const seen = new Map<string, any>();
        for (const r of this.rows) seen.set(key.map((k) => String(r[k])).join('\u0001'), r);
        this.rows = Array.from(seen.values());
      }
      const q = await this.build();
      let count: number | null = null;
      if (q.countText) {
        const c = await pgPool.query(q.countText, q.countValues);
        count = c.rows[0]?.n ?? 0;
      }
      if (this.mode === 'select' && this.headOnly) return { data: null, error: null, count };
      const r = await pgPool.query(q.text, q.values);
      const rows = this.mode === 'select' || this.returning ? r.rows : null;
      if (this.singleMode) {
        if (!rows || rows.length === 0) {
          return this.singleMode === 'maybe'
            ? { data: null, error: null, count }
            : { data: null, error: { message: 'Satır bulunamadı', code: 'PGRST116' }, count };
        }
        return { data: rows[0] as any, error: null, count };
      }
      return { data: rows as any, error: null, count: count ?? (this.mode === 'select' ? null : r.rowCount) };
    } catch (e: any) {
      return { data: null, error: { message: e?.message || String(e), code: e?.code }, count: null };
    }
  }

  then<R1 = PgResult<T>, R2 = never>(
    onfulfilled?: ((value: PgResult<T>) => R1 | PromiseLike<R1>) | null,
    onrejected?: ((reason: any) => R2 | PromiseLike<R2>) | null
  ): PromiseLike<R1 | R2> {
    return this.execute().then(onfulfilled, onrejected);
  }
}

export const pgDb = {
  from<T = any>(table: string) {
    return new QueryBuilder<T>(table);
  },
  /** Adlandırılmış argümanlarla SQL fonksiyonu çağırır: select * from fn(a => $1, ...) */
  async rpc<T = any>(fn: string, args: Record<string, any> = {}): Promise<PgResult<T>> {
    try {
      ident(fn);
      const names = Object.keys(args);
      const values = names.map((n) => {
        const v = args[n];
        if (Array.isArray(v) && v.every((x) => typeof x === 'number')) return `[${v.join(',')}]`;
        if (v && typeof v === 'object' && !Array.isArray(v)) return JSON.stringify(v);
        return v;
      });
      const argSql = names.map((n, i) => `${ident(n)} => $${i + 1}`).join(', ');
      const r = await pgPool.query(`select * from ${ident(fn)}(${argSql})`, values);
      return { data: r.rows as any, error: null, count: r.rowCount };
    } catch (e: any) {
      return { data: null, error: { message: e?.message || String(e), code: e?.code }, count: null };
    }
  },
  query: (text: string, values?: any[]) => pgPool.query(text, values),
};

export async function pgHealth(): Promise<{ ok: boolean; latencyMs: number; error?: string }> {
  const t = Date.now();
  try {
    await pgPool.query('select 1');
    return { ok: true, latencyMs: Date.now() - t };
  } catch (e: any) {
    return { ok: false, latencyMs: Date.now() - t, error: e?.message };
  }
}

/**
 * LISTEN/NOTIFY aboneliği. Bağlantı koparsa üstel bekleme ile yeniden bağlanır ve
 * `onReconnect` çağrılır (kopukluk sırasında kaçan değişiklikleri telafi etmek için).
 */
export function pgListen(
  channel: string,
  onMessage: (payload: string) => void,
  hooks: { onStatus?: (s: 'connecting' | 'connected' | 'error') => void; onReconnect?: () => void } = {}
): () => void {
  ident(channel);
  let client: pg.Client | null = null;
  let stopped = false;
  let attempt = 0;
  let everConnected = false;
  let timer: ReturnType<typeof setTimeout> | null = null;
  let keepAlive: ReturnType<typeof setInterval> | null = null;

  const schedule = () => {
    if (stopped || timer) return;
    const delay = Math.min(60_000, 1000 * 2 ** Math.min(attempt++, 6));
    timer = setTimeout(() => {
      timer = null;
      void connect();
    }, delay);
  };

  const connect = async () => {
    hooks.onStatus?.('connecting');
    const c = new pg.Client({ connectionString: DATABASE_URL, application_name: 'meds-app-listen', keepAlive: true });
    client = c;
    const fail = (err?: any) => {
      if (client !== c) return;
      client = null;
      if (keepAlive) clearInterval(keepAlive);
      keepAlive = null;
      if (err && (attempt <= 2 || attempt % 10 === 0)) {
        console.warn(`[pgListen:${channel}] bağlantı koptu (deneme ${attempt}):`, err?.message || err);
      }
      hooks.onStatus?.('error');
      c.end().catch(() => {});
      schedule();
    };
    c.on('error', fail);
    c.on('end', () => fail());
    c.on('notification', (msg) => {
      if (msg.channel === channel && msg.payload != null) {
        try {
          onMessage(msg.payload);
        } catch (e) {
          console.warn(`[pgListen:${channel}] işleyici hatası:`, e);
        }
      }
    });
    try {
      await c.connect();
      await c.query(`listen ${ident(channel)}`);
      attempt = 0;
      hooks.onStatus?.('connected');
      // Sessiz kopmaları (NAT/firewall) yakalamak için dakikada bir yoklama
      keepAlive = setInterval(() => {
        c.query('select 1').catch(fail);
      }, 60_000);
      if (everConnected) hooks.onReconnect?.();
      everConnected = true;
    } catch (e) {
      fail(e);
    }
  };

  void connect();
  return () => {
    stopped = true;
    if (timer) clearTimeout(timer);
    if (keepAlive) clearInterval(keepAlive);
    client?.end().catch(() => {});
    client = null;
  };
}
