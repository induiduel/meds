// Canlı ders (/canliders): herkese açık, yalnız okuma uçları.
//   GET /api/canli-ders                     — sesi olan dersler (sıra ile)
//   GET /api/canli-ders/:key                — bölüm/paragraf metni + varyantlar (zamanlama) + PDF hizalaması
//   GET /api/canli-ders/ses/:key/:vid.mp3   — MP3 (Range/206; ?indir=1 → ek olarak indir)
// Veri: data/sesli_anlatim/ (sesliAnlatim.ts) + hizalama/<key>.json (scripts/sesli_anlatim/pdf_hizala.py).
import type { Express, Request, Response } from 'express';
import fs from 'fs';
import path from 'path';
import { metinParagraflari } from './sesliAnlatim';

const KOK = path.join(process.cwd(), 'data', 'sesli_anlatim');
const P = {
  dersler: path.join(KOK, 'dersler.json'),
  kayit: path.join(KOK, 'kayit.json'),
  metin: (k: string) => path.join(KOK, 'metin', `${k}.md`),
  ses: (k: string, v: string) => path.join(KOK, 'ses', k, `${v}.mp3`),
  hizalama: (k: string) => path.join(KOK, 'hizalama', `${k}.json`),
};

interface Ders { key: string; no: number; baslik: string; sira: number }
interface KayitVaryant {
  id: string;
  saglayici: string;
  ses: string;
  etiket: string;
  sureSn: number;
  bayt: number;
  zamanlama?: [number, number][];
}

const oku = <T,>(p: string, bos: T): T => {
  try {
    return JSON.parse(fs.readFileSync(p, 'utf8'));
  } catch {
    return bos;
  }
};
const anahtarGecerli = (k: unknown): k is string => typeof k === 'string' && /^k1-\d+-[a-z0-9-]+$/.test(k);
const vidGecerli = (v: unknown): v is string => typeof v === 'string' && /^[a-z0-9-]+$/.test(v);

const dersler = () => oku<Ders[]>(P.dersler, []);
/** Kayıtlı ve dosyası diskte olan varyantlar (ilki varsayılan). */
function varyantlar(key: string): KayitVaryant[] {
  const k = oku<Record<string, KayitVaryant[]>>(P.kayit, {});
  return (k[key] || []).filter((v) => vidGecerli(v.id) && fs.existsSync(P.ses(key, v.id)));
}
/** surum: dosyanın değiştirilme zamanı — ses onarılınca/yeniden üretilince adres değişsin (aynı bayt boyutu olsa bile). */
const surum = (key: string, vid: string) => {
  try {
    return Math.round(fs.statSync(P.ses(key, vid)).mtimeMs);
  } catch {
    return 0;
  }
};
const ozet = (key: string) => (v: KayitVaryant) => ({ id: v.id, etiket: v.etiket, saglayici: v.saglayici, ses: v.ses, sureSn: v.sureSn, bayt: v.bayt, surum: surum(key, v.id) });

export function registerCanliDersRoutes(app: Express) {
  app.get('/api/canli-ders', (_req: Request, res: Response) => {
    const out = dersler()
      .slice()
      .sort((a, b) => a.sira - b.sira)
      .map((d) => {
        const vs = varyantlar(d.key);
        if (!vs.length) return null;
        return {
          key: d.key,
          no: d.no,
          baslik: d.baslik,
          sira: d.sira,
          varsayilan: ozet(d.key)(vs[0]),
          varyantlar: vs.map(ozet(d.key)),
          pdf: fs.existsSync(P.hizalama(d.key)),
        };
      })
      .filter(Boolean);
    // Express res.json zayıf ETag üretir ve If-None-Match'te 304 döner.
    res.setHeader('Cache-Control', 'public, max-age=60');
    res.json({ dersler: out });
  });

  app.get('/api/canli-ders/ses/:key/:dosya', (req: Request, res: Response) => {
    const key = req.params.key;
    const vid = String(req.params.dosya || '').replace(/\.mp3$/, '');
    if (!anahtarGecerli(key) || !vidGecerli(vid)) return res.status(400).json({ error: 'geçersiz istek' });
    const v = varyantlar(key).find((x) => x.id === vid);
    if (!v) return res.status(404).json({ error: 'ses yok' });
    const d = dersler().find((x) => x.key === key);
    if (req.query.indir) {
      const ad = `${String(d?.no ?? '').padStart(2, '0')} - ${d?.baslik || key} - ${v.etiket || vid}.mp3`.replace(/[\\/:*?"<>|\u0000-\u001f]/g, '-');
      const ascii = ad
        .replace(/[ğĞüÜşŞıİöÖçÇ·]/g, (c) => ({ ğ: 'g', Ğ: 'G', ü: 'u', Ü: 'U', ş: 's', Ş: 'S', ı: 'i', İ: 'I', ö: 'o', Ö: 'O', ç: 'c', Ç: 'C', '·': '-' })[c]!)
        .normalize('NFKD')
        .replace(/[^\x20-\x7e]/g, '')
        .replace(/["\\]/g, '');
      const utf8 = encodeURIComponent(ad).replace(/['()*]/g, (c) => `%${c.charCodeAt(0).toString(16).toUpperCase()}`);
      res.setHeader('Content-Disposition', `attachment; filename="${ascii}"; filename*=UTF-8''${utf8}`);
    }
    // sendFile: Range → 206/416, ETag/Last-Modified, Accept-Ranges
    res.sendFile(P.ses(key, vid), {
      headers: { 'Content-Type': 'audio/mpeg', 'Cache-Control': 'public, max-age=86400' },
      cacheControl: false,
      dotfiles: 'deny',
    }, (err: any) => {
      if (err && !res.headersSent) res.status(err.status || 500).end();
    });
  });

  app.get('/api/canli-ders/:key', (req: Request, res: Response) => {
    const key = req.params.key;
    if (!anahtarGecerli(key)) return res.status(400).json({ error: 'geçersiz ders' });
    const d = dersler().find((x) => x.key === key);
    if (!d || !fs.existsSync(P.metin(key))) return res.status(404).json({ error: 'ders yok' });
    const vs = varyantlar(key);
    if (!vs.length) return res.status(404).json({ error: 'bu dersin sesi henüz yok' });
    const pars = metinParagraflari(fs.readFileSync(P.metin(key), 'utf8'));
    const bolumler: { baslik: string; paragraflar: { i: number; metin: string }[] }[] = [];
    pars.forEach((p, i) => {
      if (p.bolumBasi || !bolumler.length) bolumler.push({ baslik: p.bolumBaslik, paragraflar: [] });
      bolumler[bolumler.length - 1].paragraflar.push({ i, metin: p.t });
    });
    const hz = oku<any>(P.hizalama(key), null);
    const pdf = hz && Array.isArray(hz.paragraflar) && hz.paragraflar.length === pars.length
      ? { deckId: hz.deckId, dosyalar: hz.dosyalar, paragraflar: hz.paragraflar }
      : null;
    res.setHeader('Cache-Control', 'public, max-age=60');
    res.json({
      key,
      no: d.no,
      baslik: d.baslik,
      bolumler,
      varyantlar: vs.map((v) => ({
        ...ozet(key)(v),
        zamanlama: Array.isArray(v.zamanlama) && v.zamanlama.length === pars.length ? v.zamanlama : null,
      })),
      pdf,
    });
  });
}
