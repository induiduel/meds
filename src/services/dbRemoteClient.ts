/**
 * Tarayıcı tarafı veritabanı istemcisi: Supabase istemcisinin kullanılan zincir biçimini
 * (from/select/eq/in/order/range/limit/single/upsert/update/delete) taklit eder; sorguyu JSON olarak
 * sunucudaki POST /api/db/query kapısına yollar. Tarayıcı veritabanına ve anahtara hiç dokunmaz.
 * Yetki sunucuda: herkes yalnız genel tabloları okur, yazma yönetici ister.
 */
import { defaultApiBaseForThisHost } from '../config/deployment';
import { getLocalAdminSession } from './auth';

export type RemoteResult<T = any> = { data: T | null; error: { message: string; code?: string } | null; count: number | null };

function apiBase(): string {
  try {
    const custom = (typeof localStorage !== 'undefined' && localStorage.getItem('medsoru_custom_api_url')) || '';
    if (custom && !custom.includes('github.')) return custom.replace(/\/+$/, '');
  } catch (_) {}
  try {
    return defaultApiBaseForThisHost() || '';
  } catch (_) {
    return '';
  }
}

export function liveRequestHeaders(): Record<string, string> {
  const h: Record<string, string> = { 'Content-Type': 'application/json' };
  try {
    const admin = getLocalAdminSession();
    if (admin?.email) h['x-admin-email'] = admin.email;
  } catch (_) {}
  return h;
}

class RemoteQuery<T = any> implements PromiseLike<RemoteResult<T>> {
  private body: Record<string, any>;
  constructor(table: string) {
    this.body = { table, action: 'select', filters: [], order: [] };
  }
  select(columns = '*', opts?: { count?: 'exact'; head?: boolean }) {
    if (this.body.action === 'select') {
      this.body.columns = columns;
      if (opts?.count) this.body.count = opts.count;
      if (opts?.head) this.body.head = true;
    }
    return this;
  }
  insert(rows: any) {
    Object.assign(this.body, { action: 'insert', rows: Array.isArray(rows) ? rows : [rows] });
    return this;
  }
  upsert(rows: any, opts?: { onConflict?: string }) {
    Object.assign(this.body, { action: 'upsert', rows: Array.isArray(rows) ? rows : [rows], onConflict: opts?.onConflict });
    return this;
  }
  update(patch: Record<string, any>) {
    Object.assign(this.body, { action: 'update', patch });
    return this;
  }
  delete() {
    this.body.action = 'delete';
    return this;
  }
  private f(op: string, col: string, val: any) {
    this.body.filters.push([op, col, val]);
    return this;
  }
  eq(c: string, v: any) { return this.f('eq', c, v); }
  neq(c: string, v: any) { return this.f('neq', c, v); }
  gt(c: string, v: any) { return this.f('gt', c, v); }
  gte(c: string, v: any) { return this.f('gte', c, v); }
  lt(c: string, v: any) { return this.f('lt', c, v); }
  lte(c: string, v: any) { return this.f('lte', c, v); }
  like(c: string, v: string) { return this.f('like', c, v); }
  ilike(c: string, v: string) { return this.f('ilike', c, v); }
  in(c: string, v: any[]) { return this.f('in', c, v); }
  is(c: string, v: null | boolean) { return this.f('is', c, v); }
  not(c: string, op: string, v: any) { return this.f('not', c, [op, v]); }
  order(col: string, opts?: { ascending?: boolean }) {
    this.body.order.push([col, opts?.ascending !== false]);
    return this;
  }
  limit(n: number) {
    this.body.limit = n;
    return this;
  }
  range(from: number, to: number) {
    this.body.range = [from, to];
    return this;
  }
  single() {
    this.body.single = 'one';
    return this;
  }
  maybeSingle() {
    this.body.single = 'maybe';
    return this;
  }
  private async run(): Promise<RemoteResult<T>> {
    try {
      const res = await fetch(`${apiBase()}/api/db/query`, {
        method: 'POST',
        headers: liveRequestHeaders(),
        body: JSON.stringify(this.body),
      });
      const json = await res.json().catch(() => null);
      if (json && typeof json === 'object' && 'data' in json) return json as RemoteResult<T>;
      return { data: null, count: null, error: { message: `Sunucu yanıtı ${res.status}` } };
    } catch (e: any) {
      return { data: null, count: null, error: { message: e?.message || 'Ağ hatası' } };
    }
  }
  then<R1 = RemoteResult<T>, R2 = never>(
    ok?: ((v: RemoteResult<T>) => R1 | PromiseLike<R1>) | null,
    fail?: ((e: any) => R2 | PromiseLike<R2>) | null
  ): PromiseLike<R1 | R2> {
    return this.run().then(ok, fail);
  }
}

export const dbRemoteClient = {
  from<T = any>(table: string) {
    return new RemoteQuery<T>(table);
  },
};
export type DbRemoteClient = typeof dbRemoteClient;

/** Sunucu üzerinden canlı yayın (POST /api/live/broadcast). Gönderen kendi mesajını almaz. */
export async function postLiveBroadcast(event: string, payload: any, senderId?: string | null): Promise<boolean> {
  try {
    const headers = liveRequestHeaders();
    if (senderId) headers['x-live-client'] = senderId;
    const res = await fetch(`${apiBase()}/api/live/broadcast`, { method: 'POST', headers, body: JSON.stringify({ event, payload }) });
    return res.ok;
  } catch (_) {
    return false;
  }
}

/** NOTIFY → LISTEN → SSE gidiş-dönüş testini başlatır (yanıt SSE 'pong' olayıyla gelir). */
export async function postLivePing(senderId?: string | null): Promise<{ id: string; dbLatencyMs: number } | null> {
  try {
    const headers = liveRequestHeaders();
    if (senderId) headers['x-live-client'] = senderId;
    const res = await fetch(`${apiBase()}/api/live/ping`, { method: 'POST', headers });
    if (!res.ok) return null;
    const j = await res.json();
    return j?.id ? { id: j.id, dbLatencyMs: j.dbLatencyMs } : null;
  } catch (_) {
    return null;
  }
}

export function dbApiBase(): string {
  return apiBase();
}
