/**
 * Yönetim v16 › Site › Sürüm (salt okunur, server-only, 2026-10-28).
 *  GET /api/admin/site/surum → { not: guncelleme_notu.json, derleme: dist/surum.json, dagitim: dist/dagitim.json, gecmis: surum_gunlugu.json (son 50) }
 */
import type express from 'express';
import fs from 'fs';
import path from 'path';

const oku = (f: string) => { try { return JSON.parse(fs.readFileSync(f, 'utf8')); } catch { return null; } };

export function registerSiteSurumRoutes(app: express.Express, d: { rootDir: string; requireAdmin: express.RequestHandler }) {
  app.get('/api/admin/site/surum', d.requireAdmin, (req, res) => {
    const n = Math.max(1, Math.min(200, Number(req.query.n) || 50));
    const gunluk = oku(path.join(d.rootDir, 'src', 'data', 'surum_gunlugu.json'));
    res.json({
      not: oku(path.join(d.rootDir, 'guncelleme_notu.json')),
      derleme: oku(path.join(d.rootDir, 'dist', 'surum.json')),
      dagitim: oku(path.join(d.rootDir, 'dist', 'dagitim.json')),
      gecmis: Array.isArray(gunluk?.surumler) ? gunluk.surumler.slice(0, n) : [],
      gecmisUretildi: gunluk?.uretildi || null,
    });
  });
}
