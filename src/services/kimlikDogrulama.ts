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

/**
 * Medya jetonu (2026-11-24): <audio>/<img>/PDF/arka plan indirmesi Authorization taşıyamaz. Bunlar için ayrı,
 * typ 'medya' jetonu sunucu yanıtında HttpOnly çereze yazılır (JS okuyamaz, yalnız API alanı). Bearer yolu bunu
 * REDDEDER (erisimJetonuDogrula typ 'erisim' ister) ve kapı onu yalnız GET/HEAD'de kabul eder: sızsa bile yazma yapılamaz.
 */
export const MEDYA_CEREZI = 'medsor_medya';
export const MEDYA_OMRU_SN = 2 * 60 * 60;
export function medyaJetonuUret(u: { uid: string; email: string; authTime: number }): { token: string; exp: number } {
  const iat = Math.floor(Date.now() / 1000);
  const exp = iat + MEDYA_OMRU_SN;
  const govde = `${BASLIK}.${b64({ uid: u.uid, email: u.email, auth_time: u.authTime, iat, exp, typ: 'medya' })}`;
  const imza = crypto.createHmac('sha256', gizliAnahtar()).update(govde).digest('base64url');
  return { token: `${govde}.${imza}`, exp };
}

/** İmza + süre + tür denetimi; geçerliyse kullanıcı, değilse null. Ağ isteği yok. */
export function erisimJetonuDogrula(token: string, tur: 'erisim' | 'medya' = 'erisim'): VerifiedUser | null {
  const p = String(token || '').split('.');
  if (p.length !== 3 || p[0] !== BASLIK) return null;
  const beklenen = crypto.createHmac('sha256', gizliAnahtar()).update(`${p[0]}.${p[1]}`).digest();
  let gelen: Buffer;
  try { gelen = Buffer.from(p[2], 'base64url'); } catch { return null; }
  if (gelen.length !== beklenen.length || !crypto.timingSafeEqual(gelen, beklenen)) return null;
  const y = jetonYuku(token);
  if (!y || y.typ !== tur || !y.uid || Number(y.exp) * 1000 < Date.now()) return null;
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
export function cerezJetonu(req: express.Request): string {
  const m = new RegExp(`(?:^|;\\s*)${MEDYA_CEREZI}=([^;]+)`).exec(String(req.headers.cookie || ''));
  try { return m ? decodeURIComponent(m[1]) : ''; } catch { return ''; }
}

/**
 * Jeton yoksa { user: null }; jeton var ama geçersizse { invalid: true } (istemci yeniden giriş yapmalı).
 * cerezli: başlık yoksa HttpOnly medya çerezi — YALNIZ GET/HEAD ve yalnız typ 'medya' (bkz. medyaJetonuUret).
 */
export async function requestUser(req: express.Request, cerezli = false): Promise<{ user: VerifiedUser | null; invalid?: boolean; revoked?: boolean }> {
  const okuma = req.method === 'GET' || req.method === 'HEAD';
  const bearer = bearerToken(req);
  const token = bearer || (cerezli && okuma ? cerezJetonu(req) : '');
  const tur = bearer ? 'erisim' : 'medya';
  if (!token) return { user: null };
  const user = erisimJetonuDogrula(token, tur);
  // Bozuk/eski medya çerezi istemciyi çıkışa zorlamasın: yalnız Bearer geçersizse invalid
  if (!user) return tur === 'erisim' ? { user: null, invalid: true } : { user: null };
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

/**
 * POST /api/kimlik/medya-cerezi (Bearer erişim jetonuyla): HttpOnly medya çerezini bu API alanına yazar.
 * DELETE aynı adres: çerezi siler (çıkış). Domain yok → yalnız isteğin geldiği API host'u.
 */
export function registerMedyaCerezi(app: express.Express) {
  const ozellik = (req: express.Request, maxAge: number) => {
    const https = req.secure || String(req.headers['x-forwarded-proto'] || '').includes('https') || !!req.headers['cf-connecting-ip'];
    return `Path=/api; Max-Age=${maxAge}; HttpOnly; SameSite=Lax${https ? '; Secure' : ''}`;
  };
  app.post('/api/kimlik/medya-cerezi', async (req, res) => {
    const who = await requestUser(req);
    if (!who.user) return res.status(401).json({ ok: false });
    const { token, exp } = medyaJetonuUret({ uid: who.user.uid, email: who.user.email, authTime: jetonGirisZamani(bearerToken(req)) });
    res.setHeader('Set-Cookie', `${MEDYA_CEREZI}=${encodeURIComponent(token)}; ${ozellik(req, MEDYA_OMRU_SN)}`);
    res.setHeader('Cache-Control', 'no-store');
    return res.json({ ok: true, exp });
  });
  app.delete('/api/kimlik/medya-cerezi', (req, res) => {
    res.setHeader('Set-Cookie', `${MEDYA_CEREZI}=; ${ozellik(req, 0)}`);
    return res.json({ ok: true });
  });
}
