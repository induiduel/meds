/**
 * Ders işçisi onay ekranı vekili: /api/admin/ders-isci/* → işçinin iç API'si (compose iç ağı, dışarıya kapalı).
 * Yalnız yönetici. İşçi yoksa (ör. cihazda geliştirme) 503 döner; ekran bunu "işçiye ulaşılamıyor" diye gösterir.
 * server.ts: app.use('/api/admin/ders-isci', requireAdmin, dersIsciRouter());
 */
import express from 'express';

const ISCI_URL = (process.env.MEDS_ISCI_URL || 'http://meds-ders-isci:8095').replace(/\/$/, '');
const IZINLI = /^\/(saglik|taslaklar|checklist|kuyruk|zamanlama|taslak\/[0-9]{8}-[0-9a-f]{10}(?:-\d+)?(?:\/dosya\/[a-z_]+\.(?:json|jsonl|md)|\/karar|\/yeniden)?)$/;

export function dersIsciRouter(): express.Router {
  const r = express.Router();
  r.use(async (req, res) => {
    const yol = req.path.replace(/\/$/, '') || '/';
    if (!IZINLI.test(yol)) return res.status(404).json({ hata: 'yol yok' });
    if (req.method !== 'GET' && !(req.method === 'POST' && (yol.endsWith('/karar') || yol.endsWith('/yeniden')))) {
      return res.status(405).json({ hata: 'yöntem yok' });
    }
    try {
      const ctrl = new AbortController();
      const t = setTimeout(() => ctrl.abort(), 20000);
      const body =
        req.method === 'POST'
          ? JSON.stringify({ ...(req.body || {}), kim: String(req.headers['x-admin-email'] || req.body?.kim || '') })
          : undefined;
      const yanit = await fetch(ISCI_URL + yol, {
        method: req.method,
        headers: body ? { 'Content-Type': 'application/json' } : undefined,
        body,
        signal: ctrl.signal,
      });
      clearTimeout(t);
      res.status(yanit.status);
      res.setHeader('Content-Type', yanit.headers.get('content-type') || 'application/json');
      res.setHeader('Cache-Control', 'no-store');
      return res.send(Buffer.from(await yanit.arrayBuffer()));
    } catch (e: any) {
      return res.status(503).json({ hata: 'Ders işçisine ulaşılamıyor', ayrinti: String(e?.message || e) });
    }
  });
  return r;
}
