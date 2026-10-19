/**
 * Patoloji alternatif sesli soru çözücü — EMA ses klipleri.
 *   GET /api/patoloji-cozucu-alt/ses/:kod/:dosya.mp3 — MP3 (Range/206).
 * Klipler meds/scripts/patoloji_cozucu_alt/seslendir.py ile üretilir → data/patoloji_cozucu_alt/ses/<kod>/<no>.mp3
 * Metinler ön yüz paketinde: src/data/patoloji_cozucu_alt/ (scripts/patoloji_cozucu_alt/paketle.py).
 */
import path from 'path';
import type { Express, Request, Response } from 'express';

const KOK = path.resolve(process.cwd(), 'data', 'patoloji_cozucu_alt', 'ses');

export function registerPatolojiCozucuAltRoutes(app: Express) {
  app.get('/api/patoloji-cozucu-alt/ses/:kod/:dosya', (req: Request, res: Response) => {
    const kod = String(req.params.kod || '');
    const dosya = String(req.params.dosya || '');
    if (!/^\d{2}[a-z]?$/.test(kod) || !/^\d{1,3}\.mp3$/.test(dosya)) return res.status(400).json({ error: 'geçersiz istek' });
    res.sendFile(path.join(KOK, kod, dosya), {
      headers: { 'Content-Type': 'audio/mpeg', 'Cache-Control': 'public, max-age=2592000, immutable' },
      cacheControl: false,
      dotfiles: 'deny',
    }, (err: any) => {
      if (err && !res.headersSent) res.status(err.status === 404 || err.code === 'ENOENT' ? 404 : 500).end();
    });
  });
}
