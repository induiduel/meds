/**
 * Ek modüller — EMA ses klipleri.
 *   GET /api/ek-modul/ses/:modul/:klip.mp3 — MP3 (Range/206). Adreste ?v=<metin özeti> olduğu için uzun önbellek.
 * Klasör: data/ek_moduller/ses/<modül>/ (git dışı). Klipler bu bilgisayarda scripts/ek_modul/ses.py ile (EMA, GPU) üretilir,
 * Oracle'a rsync ile taşınır. Klip dizini (özet + süre) ön yüz paketinde: src/data/ek_moduller/<modül>/klip.json.
 */
import path from 'path';
import type { Express, Request, Response } from 'express';

const KOK = path.resolve(process.cwd(), 'data', 'ek_moduller', 'ses');

export function registerEkModulSesRoutes(app: Express) {
  app.get('/api/ek-modul/ses/:modul/:dosya', (req: Request, res: Response) => {
    const modul = String(req.params.modul || '');
    const klip = String(req.params.dosya || '').replace(/\.mp3$/, '');
    if (!/^[a-z0-9-]{2,40}$/.test(modul) || !/^[a-z0-9-]{1,40}$/.test(klip)) return res.status(400).json({ error: 'geçersiz istek' });
    res.sendFile(path.join(KOK, modul, `${klip}.mp3`), {
      headers: { 'Content-Type': 'audio/mpeg', 'Cache-Control': 'public, max-age=2592000, immutable' },
      cacheControl: false,
      dotfiles: 'deny',
    }, (err: any) => {
      if (err && !res.headersSent) res.status(err.status === 404 || err.code === 'ENOENT' ? 404 : 500).end();
    });
  });
}
