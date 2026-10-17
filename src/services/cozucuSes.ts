/**
 * Sesli soru çözücü (branş geneli) — ses klipleri.
 *   GET /api/cozucu-ses/:brans/:ses/:kod/:klip.mp3 — MP3 (Range/206). Adreste ?v=<metin özeti> olduğu için uzun önbellek.
 * Klasör: data/<brans>_cozucu/ses/<kod>/ (varsayılan ses, EMA) ya da data/<brans>_cozucu/ses_<ses>/<kod>/ (başka sesler).
 * Klipler bu bilgisayarda üretilir (patoloji: scripts/patoloji_cozucu/cozucu_ses.py; diğerleri: scripts/spot_cozucu/ses.py);
 * Oracle'a rsync ile taşınır. İçerik (metinler, zamanlamalar) ön yüz paketinde: src/data/<brans>_cozucu/.
 */
import path from 'path';
import type { Express, Request, Response } from 'express';

const BRANSLAR = new Set(['patoloji', 'enfeksiyon', 'uroloji']);
const VARSAYILAN_SES = 'ema';
const KOK = path.resolve(process.cwd(), 'data');

export function registerCozucuSesRoutes(app: Express) {
  app.get('/api/cozucu-ses/:brans/:ses/:kod/:dosya', (req: Request, res: Response) => {
    const brans = String(req.params.brans || '');
    const ses = String(req.params.ses || '');
    const kod = String(req.params.kod || '');
    const klip = String(req.params.dosya || '').replace(/\.mp3$/, '');
    if (!BRANSLAR.has(brans) || !/^[a-z0-9]{2,16}$/.test(ses) || !/^([a-z]?\d{2}[a-z]?|ortak)$/.test(kod) || !/^[a-zA-Z0-9-]{1,40}$/.test(klip)) {
      return res.status(400).json({ error: 'geçersiz istek' });
    }
    const klasor = ses === VARSAYILAN_SES ? 'ses' : `ses_${ses}`;
    res.sendFile(path.join(KOK, `${brans}_cozucu`, klasor, kod, `${klip}.mp3`), {
      headers: { 'Content-Type': 'audio/mpeg', 'Cache-Control': 'public, max-age=2592000, immutable' },
      cacheControl: false,
      dotfiles: 'deny',
    }, (err: any) => {
      if (err && !res.headersSent) res.status(err.status === 404 || err.code === 'ENOENT' ? 404 : 500).end();
    });
  });
}
