/**
 * Sunucu tarafı Firebase kimlik doğrulaması (firebase-admin olmadan).
 * İstemci `Authorization: Bearer <Firebase ID token>` yollar; jeton Identity Toolkit `accounts:lookup` ile
 * doğrulanır ve uid/e-posta oradan alınır. Sonuç 10 dk önbellekte tutulur (her istekte Google'a gidilmez).
 * Web API anahtarı firebase-applet-config.json'dan okunur (herkese açık anahtardır).
 */
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { fileURLToPath } from 'url';
import type express from 'express';

export type VerifiedUser = { uid: string; email: string };

let apiKey: string | undefined;
function getApiKey(): string | undefined {
  if (apiKey !== undefined) return apiKey || undefined;
  try {
    const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
    apiKey = String(JSON.parse(fs.readFileSync(path.join(root, 'firebase-applet-config.json'), 'utf8')).apiKey || '');
  } catch {
    apiKey = '';
  }
  return apiKey || undefined;
}

const cache = new Map<string, VerifiedUser & { exp: number }>();

export async function verifyFirebaseIdToken(token: string): Promise<VerifiedUser | null> {
  const key = getApiKey();
  if (!token || !key) return null;
  const h = crypto.createHash('sha256').update(token).digest('hex');
  const hit = cache.get(h);
  if (hit && hit.exp > Date.now()) return { uid: hit.uid, email: hit.email };
  try {
    const r = await fetch(`https://identitytoolkit.googleapis.com/v1/accounts:lookup?key=${encodeURIComponent(key)}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ idToken: token }),
      signal: AbortSignal.timeout(5000),
    });
    if (!r.ok) return null;
    const u = (await r.json())?.users?.[0];
    if (!u?.localId) return null;
    const out = { uid: String(u.localId), email: String(u.email || '').toLowerCase() };
    if (cache.size > 2000) cache.clear();
    cache.set(h, { ...out, exp: Date.now() + 10 * 60 * 1000 });
    return out;
  } catch {
    return null;
  }
}

/** İstekteki Bearer jetonu (yoksa boş). */
export function bearerToken(req: express.Request): string {
  const auth = String(req.headers.authorization || '');
  return auth.toLowerCase().startsWith('bearer ') ? auth.slice(7).trim() : '';
}

/**
 * Jeton yoksa { user: null }; jeton var ama geçersizse { invalid: true } (istemci yeniden giriş yapmalı).
 */
export async function requestUser(req: express.Request): Promise<{ user: VerifiedUser | null; invalid?: boolean; revoked?: boolean }> {
  const token = bearerToken(req);
  if (!token) return { user: null };
  const user = await verifyFirebaseIdToken(token);
  if (!user) return { user: null, invalid: true };
  // Yönetici "oturumları sonlandır" dediyse: o andan önce açılmış girişin jetonları (yenilense de auth_time aynı kalır) reddedilir
  if (oturumIptali) {
    const iptal = oturumIptali(user.uid);
    if (iptal && jetonGirisZamani(token) * 1000 < iptal) return { user: null, invalid: true, revoked: true };
  }
  return { user };
}

/** Jetonun giriş zamanı (auth_time, sn). Jeton zaten Google'da doğrulandı; burada yalnız yük okunur. */
export function jetonGirisZamani(token: string): number {
  try {
    const yuk = JSON.parse(Buffer.from(token.split('.')[1] || '', 'base64url').toString('utf8'));
    return Number(yuk.auth_time || yuk.iat) || 0;
  } catch {
    return 0;
  }
}

/** uid → oturum sonlandırma zamanı (ms) ya da null. userAdminRoutes kurar (users.json `sessionsRevokedAt`). */
let oturumIptali: ((uid: string) => number | null) | null = null;
export function oturumIptaliKur(fn: (uid: string) => number | null) {
  oturumIptali = fn;
}

/** Hesaba bağlı not defterinin sunucu tarafı kodu (istemci bilmez; yalnız doğrulanmış jetondan türetilir). */
export const accountNotesCode = (uid: string) => `acct:${uid}`;
