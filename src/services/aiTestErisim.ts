/**
 * Yapay zekâ test erişimi: site hesapsız açılamaz (App.tsx zorunlu giriş kapısı). Yalnız test eden ajanlar
 * MEDS_PANEL_SECRET'i `x-panel-secret` başlığıyla göndererek 12 saatlik, HttpOnly, imzalı bir çerez alır;
 * kapı bu çerezi /api/ai-test/durum ile sorar. Gizli anahtar istemciye/adrese hiç girmez, çerez JS'ten okunamaz.
 *   await fetch('/api/ai-test/oturum', { method: 'POST', headers: { 'x-panel-secret': '<.env MEDS_PANEL_SECRET>' } })
 *   Çıkış: POST /api/ai-test/cikis
 */
import type express from 'express';
import crypto from 'crypto';
import { panelSecretOk } from './adminAuth';

const CEREZ = 'meds_ai_test';
const SURE_MS = 12 * 60 * 60 * 1000;

const imza = (bitis: number) =>
  crypto.createHmac('sha256', String(process.env.MEDS_PANEL_SECRET || '')).update(`ai-test:${bitis}`).digest('base64url');

function cerezOku(req: express.Request): string {
  const ham = String(req.headers.cookie || '');
  for (const p of ham.split(';')) {
    const i = p.indexOf('=');
    if (i > 0 && p.slice(0, i).trim() === CEREZ) return decodeURIComponent(p.slice(i + 1).trim());
  }
  return '';
}

export function aiTestGecerli(req: express.Request): boolean {
  if (String(process.env.MEDS_PANEL_SECRET || '').trim().length < 24) return false;
  const [b, s] = cerezOku(req).split('.');
  const bitis = Number(b);
  if (!bitis || !s || bitis < Date.now()) return false;
  const beklenen = imza(bitis);
  return s.length === beklenen.length && crypto.timingSafeEqual(Buffer.from(s), Buffer.from(beklenen));
}

export function registerAiTestRoutes(app: express.Express) {
  app.post('/api/ai-test/oturum', (req, res) => {
    if (!panelSecretOk(req)) return void res.status(403).json({ ok: false });
    const bitis = Date.now() + SURE_MS;
    const guvenli = req.secure || String(req.headers['x-forwarded-proto'] || '').includes('https');
    res.setHeader('Set-Cookie', `${CEREZ}=${bitis}.${imza(bitis)}; Path=/; Max-Age=${SURE_MS / 1000}; HttpOnly; SameSite=Strict${guvenli ? '; Secure' : ''}`);
    res.json({ ok: true, bitis });
  });
  app.get('/api/ai-test/durum', (req, res) => {
    res.setHeader('Cache-Control', 'no-store');
    res.json({ ok: aiTestGecerli(req) });
  });
  app.post('/api/ai-test/cikis', (_req, res) => {
    res.setHeader('Set-Cookie', `${CEREZ}=; Path=/; Max-Age=0; HttpOnly; SameSite=Strict`);
    res.json({ ok: true });
  });
}
