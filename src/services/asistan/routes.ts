/** Tıp Asistanı uç noktası: POST /api/asistan/sor {soru} → Cevap. Sunucu kodu değişince `systemctl --user restart meds-web`. */
import type express from 'express';
import { cevapla, cevapsizKaydet } from './cevap';

const SON = new Map<string, number[]>();
function sinir(ip: string): boolean {
  const now = Date.now(), l = (SON.get(ip) || []).filter(t => now - t < 60_000);
  if (l.length >= 40) { SON.set(ip, l); return false; }
  l.push(now); SON.set(ip, l);
  if (SON.size > 5000) SON.clear();
  return true;
}

export function registerAsistanRoutes(app: express.Express) {
  app.post('/api/asistan/sor', async (req, res) => {
    // proje durduruldu (2026-10-29): MEDS_ASISTAN=1 olmadan uç yok sayılır
    if (process.env.MEDS_ASISTAN !== '1') return res.status(404).json({ error: 'yok' });
    const soru = String(req.body?.soru ?? '').trim().slice(0, 400);
    if (!soru) return res.status(400).json({ error: 'soru boş' });
    if (!sinir(String(req.headers['cf-connecting-ip'] || req.ip || ''))) return res.status(429).json({ error: 'Çok sık soruyorsun, biraz bekle.' });
    try {
      const c = await cevapla(soru);
      cevapsizKaydet(soru, c);
      res.json(c);
    } catch (e: any) {
      res.status(500).json({ error: 'Asistan şu an cevap veremiyor.', detay: String(e?.message || e).slice(0, 200) });
    }
  });
}
