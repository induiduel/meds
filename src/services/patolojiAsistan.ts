/**
 * Patoloji sesli sınav asistanı — EMA ses klipleri.
 *   GET /api/patoloji-asistan/ses/:kod/:klip.mp3  — MP3 (Range/206). Adreste ?v=<metin özeti> olduğu için uzun önbellek.
 * Klipler scripts/patoloji_onem/asistan_ses.py ile bu bilgisayarda EMA Lightning'le üretilir → data/patoloji_asistan/ses/<kod>/.
 * İçerik (metinler, zamanlamalar) ön yüz paketinde: src/data/patoloji_asistan/<kod>.json.
 */
import path from 'path';
import type { Express, Request, Response } from 'express';

const KOK = path.resolve(process.cwd(), 'data', 'patoloji_asistan', 'ses');

export function registerPatolojiAsistanRoutes(app: Express) {
  app.get('/api/patoloji-asistan/ses/:kod/:dosya', (req: Request, res: Response) => {
    const kod = String(req.params.kod || '');
    const klip = String(req.params.dosya || '').replace(/\.mp3$/, '');
    if (!/^\d{2}[a-z]?$/.test(kod) || !/^[a-zA-Z0-9-]{1,40}$/.test(klip)) return res.status(400).json({ error: 'geçersiz istek' });
    res.sendFile(path.join(KOK, kod, `${klip}.mp3`), {
      headers: { 'Content-Type': 'audio/mpeg', 'Cache-Control': 'public, max-age=2592000, immutable' },
      cacheControl: false,
      dotfiles: 'deny',
    }, (err: any) => {
      if (err && !res.headersSent) res.status(err.status === 404 || err.code === 'ENOENT' ? 404 : 500).end();
    });
  });
}
