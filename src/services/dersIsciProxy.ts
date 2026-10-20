/**
 * Ders işçisi onay ekranı vekili: /api/admin/ders-isci/* → işçinin iç API'si (compose iç ağı, dışarıya kapalı).
 * Yalnız yönetici. İşçi yoksa (ör. cihazda geliştirme) 503 döner; ekran bunu "işçiye ulaşılamıyor" diye gösterir.
 * server.ts: app.use('/api/admin/ders-isci', requireAdmin, dersIsciRouter());
 */
import express from 'express';

const ISCI_URL = (process.env.MEDS_ISCI_URL || 'http://meds-ders-isci:8095').replace(/\/$/, '');
const ID = '[0-9]{8}-[0-9a-f]{10}(?:-\\d+)?';
const IZINLI_GET = new RegExp(`^/(saglik|taslaklar|checklist|kuyruk|zamanlama|olaylar|ayarlar|taslak/${ID}(?:/dosya/[a-z_]+\\.(?:json|jsonl|md))?)$`);
// Yazan uçlar: karar, yeniden gönder, eşiği yok say, kuyruk eylemleri, ayarlar, Drive taraması, elle kuyruğa alma
const IZINLI_POST = new RegExp(`^/(taslak/${ID}/(?:karar|yeniden|esik-atla)|kuyruk/${ID}/(?:simdi|one-al|sona-at|kaldir|yeniden-dene)|ayarlar|tara|pdf/kuyruga)$`);

export function dersIsciRouter(): express.Router {
  const r = express.Router();
  r.use(async (req, res) => {
    const yol = req.path.replace(/\/$/, '') || '/';
    const izin = req.method === 'GET' ? IZINLI_GET : req.method === 'POST' ? IZINLI_POST : null;
    if (!izin) return res.status(405).json({ hata: 'yöntem yok' });
    if (!izin.test(yol)) return res.status(404).json({ hata: 'yol yok' });
    try {
      const ctrl = new AbortController();
      const t = setTimeout(() => ctrl.abort(), 20000);
      const body =
        req.method === 'POST'
          ? JSON.stringify({ ...(req.body || {}), kim: String(req.headers['x-admin-email'] || req.body?.kim || '') })
          : undefined;
      const yanit = await fetch(ISCI_URL + yol, {
        method: req.method,
        headers: body ? { 'Content-Type': 'application/json' } : undefined,
        body,
        signal: ctrl.signal,
      });
      clearTimeout(t);
      res.status(yanit.status);
      res.setHeader('Content-Type', yanit.headers.get('content-type') || 'application/json');
      res.setHeader('Cache-Control', 'no-store');
      return res.send(Buffer.from(await yanit.arrayBuffer()));
    } catch (e: any) {
      // İşçi yalnız Oracle'daki compose ağında çalışır; cihazdaki sunucu ona ulaşamaz (beklenen durum).
      const yerel = !process.env.MEDS_ISCI_URL;
      return res.status(503).json({
        hata: yerel
          ? 'Ders işçisi yalnız Oracle sunucusunda çalışır; bu yerel sunucudan erişilemez. Panel başlığından hedefi "Canlı" yapıp sayfayı yenileyin.'
          : 'Ders işçisine ulaşılamıyor (işçi kapalı ya da yeniden başlıyor olabilir).',
        yerel,
        ayrinti: String(e?.message || e),
      });
    }
  });
  return r;
}
