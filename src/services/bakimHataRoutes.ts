/**
 * AB17 + AB18 sunucu tarafı.
 *  - Bakım kipi (varsayılan KAPALI): ortam değişkeni MEDS_BAKIM=1 (MEDS_BAKIM_SURE="15 dk" isteğe bağlı) ya da yönetici ucu
 *    POST /api/admin/bakim {acik:boolean, sure?:string}. Açıkken öğrenci /api/* istekleri 503 + {bakim:true, sure} alır;
 *    /api/health, /api/admin/*, /api/bakim ve istemci hata bildirimi dışarıda kalır (yönetici kipi kapatabilsin).
 *    Bellekteki bayrak sunucu yeniden başlayınca ortam değişkenine döner.
 *  - İstemci hata bildirimi: POST /api/istemci-hata → data/istemci_hatalari.jsonl (IP başına dakikada 5, dosya 5 MB tavan).
 *    Yönetici okur: GET /api/admin/istemci-hata?n=100.
 */
import type express from 'express';
import fs from 'fs';
import path from 'path';

type Mw = (req: express.Request, res: express.Response, next: express.NextFunction) => void;

export type BakimDenetleyici = {
  durum: () => { bakim: boolean; sure?: string };
  /** Bakımı aç/kapa (site-ayar kalıcılığı bunu açılışta çağırır) */
  ayarla: (acik: boolean, sure?: string) => void;
  /** POST /api/admin/bakim sonrası çağrılır (yonetim16/siteAyar kalıcı yazar) */
  onDegisti?: (d: { bakim: boolean; sure?: string }) => void;
};

export function registerBakimHataRoutes(app: express.Express, opts: { dataDir: string; requireAdmin: Mw }): BakimDenetleyici {
  let bakim = process.env.MEDS_BAKIM === '1';
  let sure: string | undefined = process.env.MEDS_BAKIM_SURE || undefined;
  const durum = () => ({ bakim, ...(bakim && sure ? { sure } : {}) });

  app.use((req, res, next) => {
    if (!bakim || !req.path.startsWith('/api/')) return next();
    if (/^\/api\/(health|admin\/|bakim$|istemci-hata$)/.test(req.path)) return next();
    if ((req as any).adminAuth) return next();
    res.status(503).set('Retry-After', '120').json(durum());
  });

  const ctl: BakimDenetleyici = {
    durum,
    ayarla: (acik, s) => { bakim = acik; sure = acik && s ? String(s).slice(0, 40) : undefined; },
  };

  app.get('/api/bakim', (_req, res) => {
    res.set('Cache-Control', 'no-store');
    res.status(bakim ? 503 : 200).json(durum());
  });

  app.post('/api/admin/bakim', opts.requireAdmin, (req, res) => {
    bakim = req.body?.acik === true;
    sure = typeof req.body?.sure === 'string' && req.body.sure.trim() ? String(req.body.sure).slice(0, 40) : undefined;
    console.log(`[bakim] ${bakim ? 'AÇIK' : 'kapalı'}${sure ? ` (${sure})` : ''}`);
    try { ctl.onDegisti?.(durum()); } catch (e: any) { console.warn('[bakim] kalıcı yazılamadı:', e?.message); }
    res.json(durum());
  });

  const dosya = path.join(opts.dataDir, 'istemci_hatalari.jsonl');
  const sayac = new Map<string, { n: number; t: number }>();
  app.post('/api/istemci-hata', (req, res) => {
    const ip = String(req.headers['cf-connecting-ip'] || req.ip || '');
    const now = Date.now();
    const s = sayac.get(ip);
    if (s && now - s.t < 60_000 && s.n >= 5) return res.status(429).json({ ok: false });
    sayac.set(ip, s && now - s.t < 60_000 ? { n: s.n + 1, t: s.t } : { n: 1, t: now });
    if (sayac.size > 5000) sayac.clear();
    const b = req.body || {};
    const kayit = {
      at: new Date(now).toISOString(),
      mesaj: String(b.mesaj || '').slice(0, 2000),
      yigin: String(b.yigin || '').slice(0, 6000),
      bilesen: String(b.bilesen || '').slice(0, 4000),
      adres: String(b.adres || '').slice(0, 500),
      surum: String(b.surum || '').slice(0, 80),
      ua: String(req.headers['user-agent'] || '').slice(0, 300),
    };
    try {
      if (fs.existsSync(dosya) && fs.statSync(dosya).size > 5 * 1024 * 1024) fs.renameSync(dosya, dosya + '.1');
      fs.appendFileSync(dosya, JSON.stringify(kayit) + '\n');
      res.json({ ok: true });
    } catch {
      res.status(500).json({ ok: false });
    }
  });

  app.get('/api/admin/istemci-hata', opts.requireAdmin, (req, res) => {
    const n = Math.min(500, Math.max(1, Number(req.query.n) || 100));
    try {
      const satir = fs.existsSync(dosya) ? fs.readFileSync(dosya, 'utf8').trim().split('\n').filter(Boolean) : [];
      res.json({ kayitlar: satir.slice(-n).reverse().map((l) => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean) });
    } catch (e: any) { res.status(500).json({ error: e?.message }); }
  });
  return ctl;
}
