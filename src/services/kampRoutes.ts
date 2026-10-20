/**
 * Kurul kampı — hoca tüyoları + kamp içeriği (kullanıcı kararı 2026-10-20).
 *
 * Tüyo = hocanın derste söylediği sınav ipucu ("şunu mutlaka sorarım", "bu tabloyu bilin"). Kayıt yalnız EKLENİR
 * (data/kamp/tuyolar.jsonl, olay defteri); güncel durum olaylardan katlanır. Kamp içeriği gece otomasyon/kamp_zinciri.py
 * ile ders bilgi deposundan (PDF yeniden okunmaz) + ONAYLI tüyolardan üretilir → src/data/kamp/k<N>/<brans>.json.
 *
 *   POST /api/kamp/tuyo-oner            {kurul, brans, ders_id?, metin, ad?}  öğrenci önerisi (IP başına saatte 10) → durum "oneri"
 *   GET  /api/kamp/tuyolar?kurul=N      yalnız onaylı tüyolar (herkese açık; kamp sayfası + kamp zinciri)
 *   GET  /api/admin/kamp/tuyolar        tümü (öneri dahil)
 *   POST /api/admin/kamp/tuyo           {kurul, brans, ders_id?, metin, kaynak?} yönetici ekler → "onayli"
 *   POST /api/admin/kamp/tuyo/:id/karar {karar: "onayla"|"reddet", metin?}  (metin = düzeltilmiş hâli)
 *   GET  /api/kamp/ses/:kurul/:brans/:klip.mp3   kamp anlatımı/denemesi EMA klipleri (data/kamp/ses/k<N>/<brans>/)
 */
import crypto from 'crypto';
import fs from 'fs';
import path from 'path';
import type { Express, Request, RequestHandler, Response } from 'express';

interface Tuyo { id: string; kurul: number; brans: string; ders_id?: string; metin: string; kaynak?: string; durum: 'oneri' | 'onayli' | 'reddedildi'; zaman: string; kim?: string }

export function registerKampRoutes(app: Express, opts: { dataDir: string; requireAdmin: RequestHandler }) {
  const KLASOR = path.join(opts.dataDir, 'kamp');
  const DEFTER = path.join(KLASOR, 'tuyolar.jsonl');
  const yaz = (olay: Record<string, unknown>) => {
    fs.mkdirSync(KLASOR, { recursive: true });
    fs.appendFileSync(DEFTER, JSON.stringify({ ...olay, ts: new Date().toISOString() }) + '\n');
  };
  /** Olay defterini katla: ekle / karar olayları → güncel tüyolar */
  const tuyolar = (): Tuyo[] => {
    const m = new Map<string, Tuyo>();
    let satirlar: string[] = [];
    try { satirlar = fs.readFileSync(DEFTER, 'utf8').split('\n'); } catch { return []; }
    for (const s of satirlar) {
      if (!s.trim()) continue;
      let o: any;
      try { o = JSON.parse(s); } catch { continue; }
      if (o.olay === 'ekle') m.set(o.id, { id: o.id, kurul: o.kurul, brans: o.brans, ders_id: o.ders_id, metin: o.metin, kaynak: o.kaynak, durum: o.durum, zaman: o.ts, kim: o.kim });
      else if (o.olay === 'karar' && m.has(o.id)) {
        const t = m.get(o.id)!;
        t.durum = o.karar === 'onayla' ? 'onayli' : 'reddedildi';
        if (o.metin) t.metin = o.metin;
      }
    }
    return [...m.values()];
  };
  const dogrula = (b: any): string | null => {
    const kurul = Number(b?.kurul);
    if (!Number.isInteger(kurul) || kurul < 1 || kurul > 6) return 'kurul 1–6 olmalı';
    if (!/^[a-z0-9]{2,30}$/.test(String(b?.brans || ''))) return 'brans (slug) geçersiz';
    if (b?.ders_id && !/^k[1-6]-\d{2}$/.test(String(b.ders_id))) return 'ders_id k<N>-NN biçiminde olmalı';
    const metin = String(b?.metin || '').trim();
    if (metin.length < 8 || metin.length > 1500) return 'metin 8–1500 karakter olmalı';
    return null;
  };
  const yeniId = () => `t-${Date.now().toString(36)}-${crypto.randomBytes(3).toString('hex')}`;

  const sayac = new Map<string, number[]>();
  app.post('/api/kamp/tuyo-oner', (req: Request, res: Response) => {
    const ip = String(req.headers['cf-connecting-ip'] || req.ip || '');
    const simdi = Date.now();
    const son = (sayac.get(ip) || []).filter((t) => simdi - t < 3600_000);
    if (son.length >= 10) return res.status(429).json({ error: 'Çok fazla öneri; bir saat sonra yeniden deneyin.' });
    const h = dogrula(req.body);
    if (h) return res.status(400).json({ error: h });
    sayac.set(ip, [...son, simdi]);
    const id = yeniId();
    yaz({ olay: 'ekle', id, kurul: Number(req.body.kurul), brans: req.body.brans, ders_id: req.body.ders_id || undefined,
      metin: String(req.body.metin).trim(), kaynak: 'ogrenci', durum: 'oneri', kim: String(req.body.ad || '').slice(0, 60) });
    res.json({ success: true, id, durum: 'oneri' });
  });

  app.get('/api/kamp/tuyolar', (req: Request, res: Response) => {
    const k = Number(req.query.kurul) || 0;
    res.json({ tuyolar: tuyolar().filter((t) => t.durum === 'onayli' && (!k || t.kurul === k)).map(({ kim, ...t }) => t) });
  });
  app.get('/api/admin/kamp/tuyolar', opts.requireAdmin, (_req: Request, res: Response) => res.json({ tuyolar: tuyolar() }));
  app.post('/api/admin/kamp/tuyo', opts.requireAdmin, (req: Request, res: Response) => {
    const h = dogrula(req.body);
    if (h) return res.status(400).json({ error: h });
    const id = yeniId();
    yaz({ olay: 'ekle', id, kurul: Number(req.body.kurul), brans: req.body.brans, ders_id: req.body.ders_id || undefined,
      metin: String(req.body.metin).trim(), kaynak: String(req.body.kaynak || 'hoca (yönetici girdi)').slice(0, 120), durum: 'onayli', kim: 'yonetici' });
    res.json({ success: true, id, durum: 'onayli' });
  });
  app.post('/api/admin/kamp/tuyo/:id/karar', opts.requireAdmin, (req: Request, res: Response) => {
    const id = String(req.params.id || '');
    const karar = String(req.body?.karar || '');
    if (!['onayla', 'reddet'].includes(karar)) return res.status(400).json({ error: 'karar onayla|reddet' });
    if (!tuyolar().some((t) => t.id === id)) return res.status(404).json({ error: 'tüyo yok' });
    const metin = req.body?.metin ? String(req.body.metin).trim().slice(0, 1500) : undefined;
    yaz({ olay: 'karar', id, karar, ...(metin ? { metin } : {}) });
    res.json({ success: true });
  });

  app.get('/api/kamp/ses/:kurul/:brans/:dosya', (req: Request, res: Response) => {
    const k = String(req.params.kurul), b = String(req.params.brans), d = String(req.params.dosya);
    if (!/^[1-6]$/.test(k) || !/^[a-z0-9]{2,30}$/.test(b) || !/^[a-z0-9-]{1,60}\.mp3$/.test(d)) return res.status(400).end();
    res.sendFile(path.join(KLASOR, 'ses', `k${k}`, b, d), {
      headers: { 'Content-Type': 'audio/mpeg', 'Cache-Control': 'public, max-age=2592000, immutable' }, cacheControl: false, dotfiles: 'deny',
    }, (err: any) => { if (err && !res.headersSent) res.status(err.code === 'ENOENT' ? 404 : 500).end(); });
  });
}
