/**
 * adminAuth.ts — yönetici yetkisinin doğrulanması (2026-10-20 güvenlik düzeltmesi).
 *
 * Eski model: `x-admin-email` (ya da body.adminEmail/requestedBy, query.adminEmail) yönetici e-postasına eşitse
 * internetteki herkes yönetici sayılıyordu. Yeni model, /api/* isteklerinde erken bir ara katmanla
 * `req.adminAuth = { ok, via }` hesaplar; yönetici yalnız şunlardan biriyle doğrulanır:
 *   (a) `x-panel-secret` = MEDS_PANEL_SECRET (sabit zamanlı karşılaştırma) — betikler, Oracle konteynerleri,
 *   (b) gerçek loopback (vekil başlığı yok: cf-connecting-ip / x-forwarded-for / x-real-ip) — cihazdaki betikler/panel,
 *   (c) `Authorization: Bearer <Firebase ID jetonu>` ve e-postası yönetici e-postası — tarayıcıdaki yönetici.
 *
 * Geçiş anahtarı MEDS_ADMIN_AUTH:
 *   - 'strict' (varsayılan, 2026-10-24): yalnız doğrulanmış istek yönetici sayılır; eski iddia yine günlüğe yazılır.
 *   - 'log': acil geri dönüş — doğrulanmamış ama eski e-posta iddiası geçen istek kabul edilir, günlüğe yazılır.
 *
 * Ayrıca: yerel panel (localhost, "Canlı" hedef) istekleri aynı kökene `x-panel-proxy: oracle` (EventSource için
 * `?panelProxy=oracle`) ile gelir; yalnız gerçek loopback isteği Oracle'a gizli anahtarla akış olarak iletilir.
 */
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { Readable } from 'stream';
import type express from 'express';
import { requestUser, bearerToken } from './firebaseIdentity';
import { isLoopback } from './peopleInsights';

export type AdminAuthVia = 'token' | 'secret' | 'loopback' | null;
export type AdminAuthState = { ok: boolean; via: AdminAuthVia };

declare module 'express-serve-static-core' {
  interface Request {
    adminAuth?: AdminAuthState;
    /** Ara katmanın doğruladığı Firebase kullanıcısı (geçerli Bearer jetonu varsa; yönetici olmasa da). */
    verifiedUser?: { uid: string; email: string } | null;
  }
}

const lc = (v: unknown) => String(v || '').trim().toLowerCase();

export function panelSecretOk(req: express.Request): boolean {
  const expected = String(process.env.MEDS_PANEL_SECRET || '').trim();
  const supplied = String(req.headers['x-panel-secret'] || '');
  if (expected.length < 24 || supplied.length !== expected.length) return false;
  return crypto.timingSafeEqual(Buffer.from(supplied), Buffer.from(expected));
}

/** Varsayılan 'strict' (2026-10-24); eski e-posta iddiasını geçici kabul için yalnız MEDS_ADMIN_AUTH=log. */
export function adminAuthMode(): 'log' | 'strict' {
  return lc(process.env.MEDS_ADMIN_AUTH) === 'log' ? 'log' : 'strict';
}

/** Doğrulanmış Firebase uid'i (ara katman hesaplar); yoksa ''. İstemcinin yolladığı uid/e-posta/ad kimlik sayılmaz. */
export function verifiedUid(req: express.Request): string {
  return String(req.verifiedUser?.uid || '');
}
export function verifiedEmail(req: express.Request): string {
  return lc(req.verifiedUser?.email);
}

/** /api/* için yönetici doğrulamasını önceden hesaplar (isRequestAdmin senkron kalsın diye). */
export function adminAuthMiddleware(adminEmail: string): express.RequestHandler {
  return (req, _res, next) => {
    if (!req.path.startsWith('/api/')) return next();
    if (panelSecretOk(req)) req.adminAuth = { ok: true, via: 'secret' };
    else if (isLoopback(req)) req.adminAuth = { ok: true, via: 'loopback' };
    else req.adminAuth = { ok: false, via: null };
    // EventSource başlık yollayamaz: yalnız canlı olay akışında jeton sorgu parametresiyle gelebilir
    const qTok = req.path === '/api/realtime/events' ? String((req.query as any)?.idToken || '') : '';
    if (qTok && !req.headers.authorization) req.headers.authorization = `Bearer ${qTok}`;
    if (!bearerToken(req)) return next();
    // firebaseIdentity jeton doğrulamasını jeton özetine göre 10 dk önbellekte tutar (her istekte Google'a gidilmez)
    requestUser(req)
      .then((who) => {
        req.verifiedUser = who.user || null;
        if (!req.adminAuth?.ok && who.user && lc(who.user.email) === lc(adminEmail)) req.adminAuth = { ok: true, via: 'token' };
      })
      .catch(() => {})
      .finally(() => next());
  };
}

/* ---------------- eski iddia (geçiş dönemi) ---------------- */

function legacyClaim(req: express.Request, adminEmail: string): string | null {
  const admin = lc(adminEmail);
  const fields: [string, unknown][] = [
    ['header:x-admin-email', req.headers['x-admin-email']],
    ['body:adminEmail', (req.body as any)?.adminEmail],
    ['body:requestedBy', (req.body as any)?.requestedBy],
    ['query:adminEmail', (req.query as any)?.adminEmail],
  ];
  // Eski davranış: ilk dolu alan karar verirdi
  const first = fields.find(([, v]) => typeof v === 'string' && v);
  if (first && lc(first[1]) === admin) return first[0];
  // Eski "loopback" (vekil başlığına bakmadan req.ip): tünel/Caddy arkasındaki dış istekler de geçiyordu
  const ip = String(req.ip || req.socket?.remoteAddress || '');
  const oldLoopback = ip.includes('127.0.0.1') || ip.includes('::1') || ip.includes('localhost');
  if (oldLoopback && (!first || lc(first[1]) === admin)) return 'loopback-proxied';
  return null;
}

let logPath = '';
const lastLogged = new Map<string, number>();

function logLegacy(req: express.Request, field: string) {
  if (!logPath) return;
  const ip = String(req.socket?.remoteAddress || '');
  const key = `${req.path}|${ip}|${req.headers['cf-connecting-ip'] || ''}`;
  const now = Date.now();
  if ((lastLogged.get(key) || 0) > now - 60_000) return;
  if (lastLogged.size > 5000) lastLogged.clear();
  lastLogged.set(key, now);
  const line = {
    time: new Date(now).toISOString(),
    method: req.method,
    path: req.path,
    ip,
    xff: req.headers['x-forwarded-for'] || undefined,
    cf: req.headers['cf-connecting-ip'] || undefined,
    ua: String(req.headers['user-agent'] || '').slice(0, 200),
    field,
    mode: adminAuthMode(),
  };
  fs.promises.appendFile(logPath, JSON.stringify(line) + '\n').catch(() => {});
}

export function configureAdminAuthLog(dataDir: string) {
  logPath = path.join(dataDir, 'admin_auth_log.jsonl');
}

/** isRequestAdmin'in yeni gövdesi: doğrulanmış → true; yalnız eski iddia → 'log' kipinde günlüğe yaz + true, 'strict'te false. */
export function isRequestAdminVerified(req: express.Request, adminEmail: string): boolean {
  if (req.adminAuth?.ok) return true;
  // Ara katmandan geçmemiş istek (ör. /api dışı): eşzamanlı olarak hesaplanabilenler
  if (!req.adminAuth && (panelSecretOk(req) || isLoopback(req))) return true;
  const field = legacyClaim(req, adminEmail);
  if (!field) return false;
  logLegacy(req, field);
  return adminAuthMode() !== 'strict';
}

/* ---------------- yerel panel → Oracle vekili ---------------- */

const HOP = new Set(['host', 'connection', 'keep-alive', 'transfer-encoding', 'upgrade', 'content-length', 'accept-encoding', 'x-panel-proxy', 'proxy-connection', 'te', 'trailer']);
const RES_SKIP = new Set(['content-encoding', 'content-length', 'transfer-encoding', 'connection', 'keep-alive']);

/**
 * Yalnız gerçek loopback + `x-panel-proxy: oracle` (ya da `?panelProxy=oracle`) taşıyan /api/* isteklerini Oracle'a
 * gizli anahtarla iletir; gövde ve yanıt akış olarak geçer (SSE dahil). express.json ve compression'dan ÖNCE kaydedilir.
 */
export function panelOracleProxyMiddleware(): express.RequestHandler {
  return async (req, res, next) => {
    if (!req.path.startsWith('/api/')) return next();
    const flagged = req.headers['x-panel-proxy'] === 'oracle' || (req.query as any)?.panelProxy === 'oracle';
    if (!flagged || !isLoopback(req)) return next();
    const secret = String(process.env.MEDS_PANEL_SECRET || '').trim();
    if (!secret) return void res.status(503).json({ error: 'MEDS_PANEL_SECRET tanımlı değil; canlıya yerelden ulaşılamıyor.' });
    const base = String(process.env.MEDS_ORACLE_API_URL || 'https://api.nofrostlife.com.tr').replace(/\/$/, '');
    const u = new URL(req.originalUrl, 'http://yerel');
    u.searchParams.delete('panelProxy');
    const headers = new Headers();
    for (const [k, v] of Object.entries(req.headers)) {
      if (v == null || HOP.has(k.toLowerCase())) continue;
      headers.set(k, Array.isArray(v) ? v.join(', ') : String(v));
    }
    headers.set('x-panel-secret', secret);
    const ac = new AbortController();
    res.on('close', () => { if (!res.writableEnded) ac.abort(); });
    const hasBody = !['GET', 'HEAD'].includes(req.method);
    try {
      const r = await fetch(`${base}${u.pathname}${u.search}`, {
        method: req.method,
        headers,
        body: hasBody ? (Readable.toWeb(req) as any) : undefined,
        // @ts-expect-error Node fetch akış gövdesi için gerekli
        duplex: hasBody ? 'half' : undefined,
        redirect: 'manual',
        signal: ac.signal,
      });
      res.status(r.status);
      r.headers.forEach((v, k) => { if (!RES_SKIP.has(k.toLowerCase())) res.setHeader(k, v); });
      if (!r.body) return void res.end();
      res.flushHeaders();
      const body = Readable.fromWeb(r.body as any);
      body.on('error', () => { try { res.end(); } catch { /* */ } });
      body.pipe(res);
    } catch (e: any) {
      if (ac.signal.aborted) return;
      if (!res.headersSent) res.status(502).json({ error: `Oracle'a ulaşılamadı: ${e?.message || e}` });
      else res.end();
    }
  };
}
