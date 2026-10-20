/**
 * Sesli sınav asistanı (Patoloji, Enfeksiyon, Üroloji) — EMA ses klipleri.
 *   GET /api/patoloji-asistan/ses/:kod/:klip.mp3  — MP3 (Range/206). Adreste ?v=<metin özeti> olduğu için uzun önbellek.
 * Klipler bu bilgisayarda EMA Lightning'le üretilir → data/<brans>_asistan/ses/<kod>/ (patoloji: scripts/patoloji_onem/asistan_ses.py,
 * diğerleri: scripts/spot_cozucu/asistan_ses.py). Branş ders kodunun önekinden: e → enfeksiyon, u → uroloji, rakam → patoloji.
 * İçerik (metinler, zamanlamalar) ön yüz paketinde: src/data/<brans>_asistan/<kod>.json.
 */
import path from 'path';
import type { Express, Request, Response } from 'express';
import branslar from '../data/dersler/branslar.json';

const KOK = path.resolve(process.cwd(), 'data');
const ONEK_BRANS: Record<string, string> = {
  e: 'enfeksiyon', u: 'uroloji', g: 'genetik', h: 'halksagligi', k: 'kadindogum', f: 'farmakoloji',
};
const HARF_SLUG: Record<string, string> = Object.fromEntries((branslar as any).branslar.map((b: any) => [b.harf, b.slug]));
/** Kurul 1: önek harfi (e07) ya da rakam (07 = patoloji). Kurul 2+: <kurul><harf><no> (2n03) → k2noroloji_asistan. */
const bransKlasor = (kod: string) => {
  const m = /^(\d)([a-z])\d{2}/.exec(kod);
  if (m && HARF_SLUG[m[2]]) return `k${m[1]}${HARF_SLUG[m[2]]}_asistan`;
  return `${ONEK_BRANS[kod[0]] || 'patoloji'}_asistan`;
};

export function registerPatolojiAsistanRoutes(app: Express) {
  app.get('/api/patoloji-asistan/ses/:kod/:dosya', (req: Request, res: Response) => {
    const kod = String(req.params.kod || '');
    const klip = String(req.params.dosya || '').replace(/\.mp3$/, '');
    if (!/^(\d[a-z]|[eughkf])?\d{2}[a-z]?$/.test(kod) || !/^[a-zA-Z0-9-]{1,40}$/.test(klip)) return res.status(400).json({ error: 'geçersiz istek' });
    res.sendFile(path.join(KOK, bransKlasor(kod), 'ses', kod, `${klip}.mp3`), {
      headers: { 'Content-Type': 'audio/mpeg', 'Cache-Control': 'public, max-age=2592000, immutable' },
      cacheControl: false,
      dotfiles: 'deny',
    }, (err: any) => {
      if (err && !res.headersSent) res.status(err.status === 404 || err.code === 'ENOENT' ? 404 : 500).end();
    });
  });
}
