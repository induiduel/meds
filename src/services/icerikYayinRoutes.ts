/**
 * Otomatik hatların canlı içerik yayını. Yetki: `x-panel-secret` = MEDS_PANEL_SECRET (iki makinenin .env'i) ya da gerçek
 * loopback. x-admin-email başlığına GÜVENMEZ (bilinen zayıflık, CLAUDE.md "Known gaps").
 *   POST /api/admin/icerik/:entity/degisti  {ids: string[]}
 * Hat dosyayı önce data/content/<dosya> katmanına koyar (rsync), sonra bu uç değişen kimlikleri işaretler ve SSE
 * `content_changed` yayar; açık istemciler yalnız o veriyi yeniden çeker. Panel düzenlemesi olmayan türler (hastalıklar)
 * için kullanılır (ör. otomasyon/hastalik_zinciri.py). Dosya katmanda değilse 409: önce dosyayı koy.
 */
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import type { Express, Request, Response, NextFunction } from 'express';
import { CONTENT_FILES } from './contentOverlay';

function hatYetkisi(req: Request, res: Response, next: NextFunction) {
  const sir = process.env.MEDS_PANEL_SECRET || '';
  const gelen = String(req.header('x-panel-secret') || '');
  const sirOk = !!sir && gelen.length === sir.length && crypto.timingSafeEqual(Buffer.from(gelen), Buffer.from(sir));
  const ip = req.socket?.remoteAddress || '';
  const loopback = ip === '127.0.0.1' || ip === '::1' || ip === '::ffff:127.0.0.1';
  if (sirOk || loopback) return next();
  return res.status(403).json({ error: 'yetki yok' });
}

export function registerIcerikYayinRoutes(app: Express, opts: {
  dataDir: string; onChange: (entity: string, ids: string[]) => void;
}) {
  app.post('/api/admin/icerik/:entity/degisti', hatYetkisi, (req, res) => {
    const entity = String(req.params.entity || '');
    const dosya = CONTENT_FILES[entity];
    if (!dosya) return res.status(400).json({ error: 'bilinmeyen içerik türü' });
    if (!fs.existsSync(path.join(opts.dataDir, 'content', dosya))) {
      return res.status(409).json({ error: `katmanda ${dosya} yok; önce dosyayı data/content altına koyun` });
    }
    const ids = (Array.isArray(req.body?.ids) ? req.body.ids : []).map(String).filter((x: string) => /^[\w.-]{1,120}$/.test(x)).slice(0, 2000);
    if (!ids.length) return res.status(400).json({ error: 'ids boş' });
    opts.onChange(entity, ids);
    res.json({ success: true, entity, ids: ids.length });
  });
}
