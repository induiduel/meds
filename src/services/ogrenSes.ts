// İnteraktif Öğrenme Desteleri EMA Seslendirme Servisi
// GET /api/ogren-ses/:deckId/:dosya -> MP3 akışı (HTTP 206 Partial Content / Range destekli)
import type { Express, Request, Response } from 'express';
import fs from 'fs';
import path from 'path';

const DATA_DIR = path.resolve(process.cwd(), 'data', 'ogren_ses');

export function registerOgrenSesRoutes(app: Express) {
  app.get('/api/ogren-ses/:deckId/:dosya', (req: Request, res: Response) => {
    const deckId = String(req.params.deckId || '');
    const dosya = String(req.params.dosya || '');

    // Temel güvenlik ve format doğrulaması
    if (!/^[a-zA-Z0-9_-]+$/.test(deckId) || !/^[a-zA-Z0-9_.-]+$/.test(dosya)) {
      return res.status(400).json({ error: 'geçersiz istek' });
    }

    const dosyaAdi = dosya.endsWith('.mp3') || dosya.endsWith('.json') ? dosya : `${dosya}.mp3`;
    const dosyaYolu = path.join(DATA_DIR, deckId, dosyaAdi);

    if (!fs.existsSync(dosyaYolu)) {
      return res.status(404).json({ error: 'ses dosyası bulunamadı' });
    }

    const contentType = dosyaAdi.endsWith('.json') ? 'application/json' : 'audio/mpeg';

    res.sendFile(
      dosyaYolu,
      {
        headers: {
          'Content-Type': contentType,
          'Cache-Control': 'public, max-age=2592000, immutable',
        },
        cacheControl: false,
        dotfiles: 'deny',
      },
      (err: any) => {
        if (err && !res.headersSent) {
          res.status(err.status === 404 || err.code === 'ENOENT' ? 404 : 500).end();
        }
      }
    );
  });
}
