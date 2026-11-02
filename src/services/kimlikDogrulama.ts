/**
 * Sunucu tarafı kimlik doğrulaması — MeDSor'un kendi kimlik sistemi (2026-11-02, Firebase Auth kaldırıldı).
 *
 * Google/Firebase projesi askıya alınınca (Consumer 'projects/990828780858' has been suspended) giriş tamamen
 * durmuştu. Artık hesaplar ve oturumlar Oracle meds-pg'de (yerelKimlik.ts), erişim jetonu burada HMAC-SHA256 ile
 * imzalanır ve yine burada doğrulanır: hiçbir istekte dış servise gidilmez.
 *
 * İstemci `Authorization: Bearer <erişim jetonu>` yollar (EventSource için `?idToken=`). Jeton yükü:
 * { uid, email, auth_time (sn), iat, exp, typ: 'erisim' }. Gizli anahtar MEDS_AUTH_SECRET (≥32 karakter) ya da
 * ilk açılışta üretilip `data/.kimlik_anahtari` (0600) dosyasına yazılan anahtardır; anahtar değişirse tüm erişim
 * jetonları geçersizleşir, istemci yenileme jetonuyla yenisini alır.
 */
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { fileURLToPath } from 'url';
import type express from 'express';

export type VerifiedUser = { uid: string; email: string };

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');

let anahtar: Buffer | null = null;
function gizliAnahtar(): Buffer {
  if (anahtar) return anahtar;
  const env = String(process.env.MEDS_AUTH_SECRET || '').trim();
  if (env.length >= 32) return (anahtar = Buffer.from(env, 'utf8'));
  const dosya = path.join(ROOT, 'data', '.kimlik_anahtari');
  try {
    const v = fs.readFileSync(dosya, 'utf8').trim();
    if (v.length >= 32) return (anahtar = Buffer.from(v, 'utf8'));
  } catch { /* ilk açılış */ }
  const yeni = crypto.randomBytes(48).toString('base64url');
  fs.mkdirSync(path.dirname(dosya), { recursive: true });
  fs.writeFileSync(dosya, yeni, { mode: 0o600 });
  return (anahtar = Buffer.from(yeni, 'utf8'));
}

const b64 = (o: unknown) => Buffer.from(JSON.stringify(o)).toString('base64url');
const BASLIK = b64({ alg: 'HS256', typ: 'JWT' });

/** Erişim jetonunun ömrü (sn). İstemci süresi dolmadan yenileme jetonuyla yeniler. */
export const ERISIM_OMRU_SN = 60 * 60;

export function erisimJetonuUret(u: { uid: string; email: string; authTime: number }): { token: string; exp: number } {
  const iat = Math.floor(Date.now() / 1000);
  const exp = iat + ERISIM_OMRU_SN;
  const govde = `${BASLIK}.${b64({ uid: u.uid, email: u.email, auth_time: u.authTime, iat, exp, typ: 'erisim' })}`;
  const imza = crypto.createHmac('sha256', gizliAnahtar()).update(govde).digest('base64url');
  return { token: `${govde}.${imza}`, exp };
}

function jetonYuku(token: string): any | null {
  const p = String(token || '').split('.');
  if (p.length !== 3) return null;
  try {
    return JSON.parse(Buffer.from(p[1], 'base64url').toString('utf8'));
  } catch {
    return null;
  }
}

/** İmza + süre + tür denetimi; geçerliyse kullanıcı, değilse null. Ağ isteği yok. */
export function erisimJetonuDogrula(token: string): VerifiedUser | null {
  const p = String(token || '').split('.');
  if (p.length !== 3 || p[0] !== BASLIK) return null;
  const beklenen = crypto.createHmac('sha256', gizliAnahtar()).update(`${p[0]}.${p[1]}`).digest();
  let gelen: Buffer;
  try { gelen = Buffer.from(p[2], 'base64url'); } catch { return null; }
  if (gelen.length !== beklenen.length || !crypto.timingSafeEqual(gelen, beklenen)) return null;
  const y = jetonYuku(token);
  if (!y || y.typ !== 'erisim' || !y.uid || Number(y.exp) * 1000 < Date.now()) return null;
  return { uid: String(y.uid), email: String(y.email || '').toLowerCase() };
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
  const user = erisimJetonuDogrula(token);
  if (!user) return { user: null, invalid: true };
  // Yönetici "oturumları sonlandır" dediyse: o andan önce açılmış girişin jetonları (yenilense de auth_time aynı kalır) reddedilir
  if (oturumIptali) {
    const iptal = oturumIptali(user.uid);
    if (iptal && jetonGirisZamani(token) * 1000 < iptal) return { user: null, invalid: true, revoked: true };
  }
  return { user };
}

/** Jetonun giriş zamanı (auth_time, sn). İmza ayrıca doğrulanır; burada yalnız yük okunur. */
export function jetonGirisZamani(token: string): number {
  const y = jetonYuku(token);
  return Number(y?.auth_time || y?.iat) || 0;
}

/** uid → oturum sonlandırma zamanı (ms) ya da null. userAdminRoutes kurar (users.json `sessionsRevokedAt`). */
let oturumIptali: ((uid: string) => number | null) | null = null;
export function oturumIptaliKur(fn: (uid: string) => number | null) {
  oturumIptali = fn;
}
export function oturumIptalZamani(uid: string): number | null {
  return oturumIptali ? oturumIptali(uid) : null;
}

/** Hesaba bağlı not defterinin sunucu tarafı kodu (istemci bilmez; yalnız doğrulanmış jetondan türetilir). */
export const accountNotesCode = (uid: string) => `acct:${uid}`;
