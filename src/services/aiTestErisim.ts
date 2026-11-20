/**
 * Yapay zekâ test erişimi: site hesapsız açılamaz (App.tsx zorunlu giriş kapısı). Yalnız test eden ajanlar
 * MEDS_PANEL_SECRET'i `x-panel-secret` başlığıyla göndererek 12 saatlik, HttpOnly, imzalı bir çerez alır;
 * kapı bu çerezi /api/ai-test/durum ile sorar. Gizli anahtar istemciye/adrese hiç girmez, çerez JS'ten okunamaz.
 *   await fetch('/api/ai-test/oturum', { method: 'POST', headers: { 'x-panel-secret': '<.env MEDS_PANEL_SECRET>' } })
 *   Çıkış: POST /api/ai-test/cikis
 *   Tarayıcı ajanı için: /ai-giris sayfası (herkese açık bağlantı yok, noindex) — anahtar forma yazılır, POST gövdesiyle gider,
 *   adrese hiç girmez; doğruysa aynı çerez kurulur ve / adresine yönlenir.
 */
import express from 'express';
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

function cerezKur(req: express.Request, res: express.Response): number {
  const bitis = Date.now() + SURE_MS;
  const guvenli = req.secure || String(req.headers['x-forwarded-proto'] || '').includes('https');
  res.setHeader('Set-Cookie', `${CEREZ}=${bitis}.${imza(bitis)}; Path=/; Max-Age=${SURE_MS / 1000}; HttpOnly; SameSite=Strict${guvenli ? '; Secure' : ''}`);
  return bitis;
}

function anahtarDogru(aday: string): boolean {
  const gercek = String(process.env.MEDS_PANEL_SECRET || '').trim();
  if (gercek.length < 24) return false;
  const a = crypto.createHash('sha256').update(String(aday || '').trim()).digest();
  const b = crypto.createHash('sha256').update(gercek).digest();
  return crypto.timingSafeEqual(a, b);
}

const girisSayfasi = (hata: boolean) => `<!doctype html><html lang="tr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow">
<title>AI test girişi</title><style>body{font:16px system-ui;max-width:420px;margin:15vh auto;padding:0 16px}
input,button{font:inherit;width:100%;padding:10px;margin-top:8px;box-sizing:border-box}</style></head><body>
<h1>Yapay zekâ test girişi</h1><p>Yalnız site sınaması yapan ajanlar içindir.</p>
${hata ? '<p id="hata" style="color:#b00">Anahtar geçersiz.</p>' : ''}
<form method="post" action="/ai-giris" autocomplete="off">
<label for="anahtar">Test anahtarı</label><input id="anahtar" name="anahtar" type="password" required>
<button id="gir" type="submit">Misafir (AI test) olarak gir</button></form></body></html>`;

export function registerAiTestRoutes(app: express.Express) {
  app.post('/api/ai-test/oturum', (req, res) => {
    if (!panelSecretOk(req)) return void res.status(403).json({ ok: false });
    res.json({ ok: true, bitis: cerezKur(req, res) });
  });
  app.get('/ai-giris', (_req, res) => {
    res.setHeader('Cache-Control', 'no-store');
    res.setHeader('X-Robots-Tag', 'noindex, nofollow');
    res.type('html').send(girisSayfasi(false));
  });
  app.post('/ai-giris', express.urlencoded({ extended: false, limit: '2kb' }), (req, res) => {
    res.setHeader('Cache-Control', 'no-store');
    if (!anahtarDogru(String((req.body as any)?.anahtar || ''))) {
      // kaba deneme yavaşlatması
      return void setTimeout(() => res.status(403).type('html').send(girisSayfasi(true)), 1500);
    }
    cerezKur(req, res);
    res.redirect(303, '/');
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
