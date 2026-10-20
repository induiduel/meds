/**
 * Olası sorular + kurul takvimi + otomasyon hattı durumu.
 *
 *   GET  /api/kurul-takvimi                       — kurul tarihleri + aktif/arşiv (src/data/kurul_takvimi_ozet.json)
 *   GET  /api/olasi-sorular                       — hangi kurulların olası soru seti var (özet)
 *   GET  /api/olasi-sorular/:kurul                — yayımlanmış set (data/olasi_sorular/k<N>.json)
 *   POST /api/olasi-sorular/:kurul/:id/geri-bildirim  {karar: 'boyleydi'|'degildi'|'duzeltme', metin?, cevap?}
 *        → data/olasi_sorular/geri_bildirim_k<N>.jsonl (yalnız eklenir). topla.py bunu kanıt olarak okur.
 *   GET  /api/admin/hat                           — otomasyon/hat.json + meds_temp/hat/durum.json + hat.log sonu
 *
 * Set gece hattında üretilir (scripts/olasi_soru/gece.sh): kapı 0 HATA → data/olasi_sorular/k<N>.json → Oracle.
 */
import crypto from 'crypto';
import fs from 'fs';
import path from 'path';
import type { Express, Request, Response, RequestHandler } from 'express';
import { KURULLAR, aktifKurul, arsivKurullar, sonSinavKurul, sinavaKalanGun, bugun } from './kurulTakvimi';

const KARARLAR = new Set(['boyleydi', 'degildi', 'duzeltme']);

export function registerOlasiSoruRoutes(app: Express, opts: { rootDir: string; requireAdmin: RequestHandler }) {
  const VERI = path.join(opts.rootDir, 'data', 'olasi_sorular');
  const setYolu = (k: number) => path.join(VERI, `k${k}.json`);
  const kurulNo = (s: unknown) => {
    const n = Number(s);
    return Number.isInteger(n) && n >= 1 && n <= 6 ? n : 0;
  };

  app.get('/api/kurul-takvimi', (_req: Request, res: Response) => {
    const gun = bugun();
    res.set('Cache-Control', 'public, max-age=300');
    res.json({
      tarih: gun, kurullar: KURULLAR, aktif: aktifKurul(gun), arsiv: arsivKurullar(gun).map((k) => k.kurul),
      sonSinav: sonSinavKurul(gun)?.kurul ?? null, sinavaKalanGun: sinavaKalanGun(gun),
    });
  });

  app.get('/api/olasi-sorular', (_req: Request, res: Response) => {
    const out = KURULLAR.map((k) => {
      try {
        const d = JSON.parse(fs.readFileSync(setYolu(k.kurul), 'utf8'));
        return { kurul: k.kurul, ad: k.ad, soru: (d.sorular || []).length, uretildi: d.uretildi || null };
      } catch { return null; }
    }).filter(Boolean);
    res.json({ setler: out });
  });

  app.get('/api/olasi-sorular/:kurul', (req: Request, res: Response) => {
    const k = kurulNo(req.params.kurul);
    if (!k) return res.status(400).json({ error: 'geçersiz kurul' });
    fs.readFile(setYolu(k), 'utf8', (err, txt) => {
      if (err) return res.status(404).json({ error: 'Bu kurul için olası soru seti henüz üretilmedi.', kurul: k });
      res.set('Cache-Control', 'no-cache');
      res.type('application/json').send(txt);
    });
  });

  // Hız sınırı: IP başına saatte 30 geri bildirim (metin Claude sentezine kanıt olarak gider; doldurulmasın)
  const sayac = new Map<string, number[]>();
  app.post('/api/olasi-sorular/:kurul/:id/geri-bildirim', (req: Request, res: Response) => {
    const ip = String(req.headers['cf-connecting-ip'] || req.ip || '');
    const simdi = Date.now();
    const son = (sayac.get(ip) || []).filter((t) => simdi - t < 3600_000);
    if (son.length >= 30) return res.status(429).json({ error: 'Çok fazla geri bildirim; bir saat sonra yeniden deneyin.' });
    sayac.set(ip, [...son, simdi]);
    if (sayac.size > 5000) sayac.clear();
    const k = kurulNo(req.params.kurul);
    const id = String(req.params.id || '');
    const { karar, metin, cevap } = req.body || {};
    if (!k || !/^k[1-6]-os-(\d{3}|s-[\w-]{6})$/.test(id) || !KARARLAR.has(karar)) {
      return res.status(400).json({ error: 'geçersiz geri bildirim' });
    }
    const satir = {
      ts: new Date().toISOString(), kurul: k, id, karar,
      metin: String(metin || '').slice(0, 2000), cevap: String(cevap || '').slice(0, 2),
      uid: String(req.header('x-user-uid') || '').slice(0, 128),  // doğrulanmamış (istemci bildirir)
      ip: ip ? crypto.createHash('sha256').update(ip).digest('hex').slice(0, 12) : '',  // aynı kaynaktan çoklu oy ayıklama
    };
    fs.mkdirSync(VERI, { recursive: true });
    fs.appendFile(path.join(VERI, `geri_bildirim_k${k}.jsonl`), JSON.stringify(satir) + '\n', (err) => {
      if (err) return res.status(500).json({ error: 'kaydedilemedi' });
      res.json({ success: true });
    });
  });

  app.get('/api/admin/hat', opts.requireAdmin, (_req: Request, res: Response) => {
    const kok = path.resolve(opts.rootDir, '..');
    const oku = (p: string, yedek: any) => { try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch { return yedek; } };
    let log: string[] = [];
    try { log = fs.readFileSync(path.join(kok, 'meds_temp/hat/hat.log'), 'utf8').trim().split('\n').slice(-60); } catch { /* yok */ }
    res.json({
      defter: oku(path.join(opts.rootDir, 'otomasyon/hat.json'), null),
      durum: oku(path.join(kok, 'meds_temp/hat/durum.json'), {}),
      log,
    });
  });
}
