// Sesli ders · hazır ders videosu oynatıcısı (v15 › O01 Video ders, O02 Tam ekran, O03 Resim içinde resim).
// Videoları yönetici GPU kuyruğu üretir (dersVideoIs.ts → data/ders_video/cikti/<id>.mp4); burada yalnız OKUNUR.
// Öğrenciye giriş zorunlu; <video> başlık gönderemediği için akış 2 saatlik imzalı adresle verilir. LLM yok.
//   GET /api/ders-video/hazir              → { videolar: [{ id, key, cozunurluk, bayt, bitti }] } (ders başına en iyi çözünürlük)
//   GET /api/ders-video/:id/baglanti       → { url } (giriş gerekli)
//   GET /api/ders-video/:id/akis?s=&t=     → MP4 (Range, satır içi)
import type { Express } from 'express';
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { verifiedUid } from './adminAuth';

const KOK = path.join(process.cwd(), 'data', 'ders_video');
const KUYRUK = path.join(KOK, 'kuyruk.json');
const CIKTI = path.join(KOK, 'cikti');
const SIRA: Record<string, number> = { '1080p': 4, '2k': 3, '720p': 2, '4k': 1 }; // akış için 1080p en uygun
interface Is { id: string; key: string; cozunurluk: string; durum: string; bitti?: string; bayt?: number }

const dosya = (id: string) => path.join(CIKTI, `${id}.mp4`);
const imza = (id: string, son: number) =>
  crypto.createHmac('sha256', String(process.env.MEDS_PANEL_SECRET || 'yok')).update(`izle.${id}.${son}`).digest('hex').slice(0, 32);
function hazirlar(): Is[] {
  let isler: Is[] = [];
  try { isler = JSON.parse(fs.readFileSync(KUYRUK, 'utf8')).isler || []; } catch { return []; }
  const enIyi = new Map<string, Is>();
  for (const x of isler) {
    if (x.durum !== 'bitti' || !/^[A-Za-z0-9]+$/.test(x.id) || !fs.existsSync(dosya(x.id))) continue;
    const o = enIyi.get(x.key);
    if (!o || (SIRA[x.cozunurluk] || 0) > (SIRA[o.cozunurluk] || 0) || ((SIRA[x.cozunurluk] || 0) === (SIRA[o.cozunurluk] || 0) && String(x.bitti) > String(o.bitti))) enIyi.set(x.key, x);
  }
  return [...enIyi.values()];
}

export function registerDersVideoOynat(app: Express) {
  app.get('/api/ders-video/hazir', (req, res) => {
    if (!verifiedUid(req)) return res.json({ videolar: [], girisli: false });
    res.setHeader('Cache-Control', 'private, max-age=60');
    res.json({ girisli: true, videolar: hazirlar().map((x) => ({ id: x.id, key: x.key, cozunurluk: x.cozunurluk, bayt: x.bayt || 0, bitti: x.bitti || '' })) });
  });

  app.get('/api/ders-video/:id/baglanti', (req, res) => {
    if (!verifiedUid(req)) return res.status(401).json({ error: 'Videoyu izlemek için giriş yapmalısın.' });
    const x = hazirlar().find((v) => v.id === req.params.id);
    if (!x) return res.status(404).json({ error: 'Video hazır değil.' });
    const son = Date.now() + 2 * 3600_000;
    res.json({ url: `/api/ders-video/${x.id}/akis?s=${son}&t=${imza(x.id, son)}` });
  });

  app.get('/api/ders-video/:id/akis', (req, res) => {
    const id = String(req.params.id);
    const son = Number(req.query.s) || 0;
    const t = String(req.query.t || '');
    const beklenen = imza(id, son);
    if (!/^[A-Za-z0-9]+$/.test(id) || son < Date.now() || t.length !== beklenen.length || !crypto.timingSafeEqual(Buffer.from(t), Buffer.from(beklenen))) {
      return res.status(403).json({ error: 'Bağlantının süresi doldu.' });
    }
    if (!fs.existsSync(dosya(id))) return res.status(404).json({ error: 'Video yok.' });
    res.setHeader('Content-Type', 'video/mp4');
    res.setHeader('Cache-Control', 'private, max-age=7200');
    res.sendFile(dosya(id), { acceptRanges: true }, (err: any) => { if (err && !res.headersSent) res.status(500).end(); });
  });
}
