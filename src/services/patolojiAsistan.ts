/**
 * Sesli sınav asistanı (Patoloji, Enfeksiyon, Üroloji) — EMA ses klipleri.
 *   GET /api/patoloji-asistan/ses/:kod/:klip.mp3  — MP3 (Range/206). Adreste ?v=<metin özeti> olduğu için uzun önbellek.
 * Klipler bu bilgisayarda EMA Lightning'le üretilir → data/<brans>_asistan/ses/<kod>/ (patoloji: scripts/patoloji_onem/asistan_ses.py,
 * diğerleri: scripts/spot_cozucu/asistan_ses.py). Branş ders kodunun önekinden: e → enfeksiyon, u → uroloji, rakam → patoloji.
 * İçerik (metinler, zamanlamalar) ön yüz paketinde: src/data/<brans>_asistan/<kod>.json.
 */
import path from 'path';
import type { Express, Request, Response } from 'express';

const KOK = path.resolve(process.cwd(), 'data');
const ONEK_BRANS: Record<string, string> = {
  e: 'enfeksiyon', u: 'uroloji', g: 'genetik', h: 'halksagligi', k: 'kadindogum', f: 'farmakoloji',
};
const bransKlasor = (kod: string) => `${ONEK_BRANS[kod[0]] || 'patoloji'}_asistan`;

export function registerPatolojiAsistanRoutes(app: Express) {
  app.get('/api/patoloji-asistan/ses/:kod/:dosya', (req: Request, res: Response) => {
    const kod = String(req.params.kod || '');
    const klip = String(req.params.dosya || '').replace(/\.mp3$/, '');
    if (!/^[eughkf]?\d{2}[a-z]?$/.test(kod) || !/^[a-zA-Z0-9-]{1,40}$/.test(klip)) return res.status(400).json({ error: 'geçersiz istek' });
    res.sendFile(path.join(KOK, bransKlasor(kod), 'ses', kod, `${klip}.mp3`), {
      headers: { 'Content-Type': 'audio/mpeg', 'Cache-Control': 'public, max-age=2592000, immutable' },
      cacheControl: false,
      dotfiles: 'deny',
    }, (err: any) => {
      if (err && !res.headersSent) res.status(err.status === 404 || err.code === 'ENOENT' ? 404 : 500).end();
    });
  });
}
