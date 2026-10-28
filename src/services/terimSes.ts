// Terim / kısaltma / bilgi paketi hazır sesleri (EMA GPU, scripts/sesli_anlatim/terim_ses_uret.py)
// GET /api/terim-ses?b=<başlık>&g=<tanım>  -> MP3 (Range destekli) ya da 404. Anahtar, betikteki anahtar() ile birebir aynıdır:
// sha1("terim-1|" + nokta(temizle(başlık)) + "|" + nokta(temizle(tanım)))[:12]; dosya data/terim_ses/<h2>/<h>.mp3
import type { Express, Request, Response } from 'express';
import crypto from 'crypto';
import fs from 'fs';
import path from 'path';

const DIR = path.resolve(process.cwd(), 'data', 'terim_ses');
const SURUM = 'terim-1';
const temizle = (s: string) => s.replace(/\*\*|__|`/g, '').replace(/\s+/g, ' ').trim();
const nokta = (s: string) => (!s || '.!?'.includes(s[s.length - 1]) ? s : s + '.');

export function terimSesAnahtar(baslik: string, govde: string): string {
  return crypto.createHash('sha1').update(`${SURUM}|${nokta(temizle(baslik))}|${nokta(temizle(govde))}`).digest('hex').slice(0, 12);
}

export function registerTerimSesRoutes(app: Express) {
  app.get('/api/terim-ses', (req: Request, res: Response) => {
    const b = String(req.query.b || '');
    const g = String(req.query.g || '');
    if (!b || !g || b.length > 300 || g.length > 2000) return res.status(400).json({ error: 'geçersiz istek' });
    const h = terimSesAnahtar(b, g);
    const yol = path.join(DIR, h.slice(0, 2), `${h}.mp3`);
    if (!fs.existsSync(yol)) return res.status(404).json({ error: 'ses yok' });
    res.sendFile(yol, { headers: { 'Content-Type': 'audio/mpeg', 'Cache-Control': 'public, max-age=2592000, immutable' }, cacheControl: false, dotfiles: 'deny' },
      (err: any) => { if (err && !res.headersSent) res.status(err.code === 'ENOENT' ? 404 : 500).end(); });
  });
}
