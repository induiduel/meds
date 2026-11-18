/**
 * Sesli soru çözücü (branş geneli) — ses klipleri.
 *   GET /api/cozucu-ses/:brans/:ses/:kod/:klip.mp3 — MP3 (Range/206). Adreste ?v=<metin özeti> olduğu için uzun önbellek.
 * Klasör: data/<brans>_cozucu/ses/<kod>/ (varsayılan ses, EMA) ya da data/<brans>_cozucu/ses_<ses>/<kod>/ (başka sesler).
 * Klipler bu bilgisayarda üretilir (patoloji: scripts/uretim/patoloji_cozucu/cozucu_ses.py; diğerleri: scripts/uretim/spot_cozucu/ses.py);
 * Oracle'a rsync ile taşınır. İçerik (metinler, zamanlamalar) ön yüz paketinde: src/data/<brans>_cozucu/.
 */
import path from 'path';
import type { Express, Request, Response } from 'express';

const BRANSLAR = new Set(['patoloji', 'enfeksiyon', 'uroloji', 'genetik', 'halksagligi', 'kadindogum', 'farmakoloji', 'kmb']);
/** Kurul 2+ branş klasörleri kurul öneklidir (k2noroloji); kodlar 2n03 (src/data/dersler/branslar.json). */
const bransGecerli = (b: string) => BRANSLAR.has(b) || /^k[2-6][a-z]{2,16}$/.test(b);
const VARSAYILAN_SES = 'ema';
const KOK = path.resolve(process.cwd(), 'data');

const KMB_VIDEO_AD: Record<string, string> = { ders: 'tum-ders', basamak: 'basamak-filmi' };

export function registerCozucuSesRoutes(app: Express) {
  // KMB tam ders / basamak filmi MP4 indirme (2026-11-18): data/kmb_cozucu/ses_video/<kod>/<tur>.mp4
  // (scripts/uretim/kmb/video_disa_aktar.mjs üretir, deploy/oracle/ses_esitle.sh taşır). ?ad=<slug> indirme adına girer.
  app.get('/api/kmb-video/:kod/:dosya', (req: Request, res: Response) => {
    const kod = String(req.params.kod || '');
    const tur = String(req.params.dosya || '').replace(/\.mp4$/, '');
    const slug = String(req.query.ad || '').replace(/[^a-z0-9-]/g, '').slice(0, 60);
    if (!/^\d{2}$/.test(kod) || !KMB_VIDEO_AD[tur]) return res.status(400).json({ error: 'geçersiz istek' });
    const ad = `medsor-kmb-${kod}${slug ? `-${slug}` : ''}-${KMB_VIDEO_AD[tur]}.mp4`;
    res.sendFile(path.join(KOK, 'kmb_cozucu', 'ses_video', kod, `${tur}.mp4`), {
      headers: { 'Content-Type': 'video/mp4', 'Content-Disposition': `attachment; filename="${ad}"`, 'Cache-Control': 'public, max-age=2592000, immutable' },
      cacheControl: false,
      dotfiles: 'deny',
    }, (err: any) => {
      if (err && !res.headersSent) res.status(err.status === 404 || err.code === 'ENOENT' ? 404 : 500).end();
    });
  });

  app.get('/api/cozucu-ses/:brans/:ses/:kod/:dosya', (req: Request, res: Response) => {
    const brans = String(req.params.brans || '');
    const ses = String(req.params.ses || '');
    const kod = String(req.params.kod || '');
    const klip = String(req.params.dosya || '').replace(/\.mp3$/, '');
    if (!bransGecerli(brans) || !/^[a-z0-9]{2,16}$/.test(ses) || !/^((\d[a-z]|[a-z])?\d{2}[a-z]?|ortak)$/.test(kod) || !/^[a-zA-Z0-9-]{1,40}$/.test(klip)) {
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
