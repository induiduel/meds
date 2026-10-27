/**
 * Ders programı düzeni: yönetici/moderatörün derslerin yerini (tarih + saat) değiştirmesi.
 * Resmî kayıt (src/data/dersler/kN.json) değişmez; fark `data/ders_programi_duzen.json` dosyasında tutulur:
 * { "<kurul>": { "<ders kimliği>": { tarih, saat } } }. Okuma herkese açık, yazma yalnız yönetici/moderatör.
 */
import fs from 'fs';
import path from 'path';
import type express from 'express';

interface Yer { tarih: string; saat?: string }
type Duzen = Record<string, Record<string, Yer>>;

const TARIH = /^\d{4}-\d{2}-\d{2}$/;

export function registerDersProgramiDuzenRoutes(
  app: express.Express,
  deps: { dataDir: string; yazmaYetkisi: express.RequestHandler },
) {
  const dosya = path.join(deps.dataDir, 'ders_programi_duzen.json');
  const oku = (): Duzen => {
    try { return JSON.parse(fs.readFileSync(dosya, 'utf8')) as Duzen; } catch { return {}; }
  };

  app.get('/api/ders-programi/duzen', (req, res) => {
    const k = String(req.query.kurul || '');
    res.setHeader('Cache-Control', 'no-cache');
    res.json({ success: true, duzen: k ? oku()[k] || {} : oku() });
  });

  app.put('/api/ders-programi/duzen', deps.yazmaYetkisi, (req, res) => {
    const kurul = String(req.body?.kurul || '');
    const degisimler = req.body?.degisimler;
    if (!/^[1-6]$/.test(kurul) || !Array.isArray(degisimler) || !degisimler.length || degisimler.length > 50) {
      return res.status(400).json({ success: false, error: 'Geçersiz istek.' });
    }
    const temiz: Record<string, Yer> = {};
    for (const d of degisimler) {
      const id = String(d?.id || '');
      const tarih = String(d?.tarih || '');
      const saat = d?.saat == null ? undefined : String(d.saat).slice(0, 20);
      if (!/^k\d+-[\w-]+$/.test(id) || !TARIH.test(tarih)) return res.status(400).json({ success: false, error: 'Geçersiz ders kaydı.' });
      temiz[id] = { tarih, ...(saat ? { saat } : {}) };
    }
    const tum = oku();
    tum[kurul] = { ...(tum[kurul] || {}), ...temiz };
    fs.mkdirSync(deps.dataDir, { recursive: true });
    fs.writeFileSync(dosya + '.tmp', JSON.stringify(tum, null, 1));
    fs.renameSync(dosya + '.tmp', dosya);
    res.json({ success: true, duzen: tum[kurul] });
  });

  /** Düzeni sıfırla (kurulun tamamı) */
  app.delete('/api/ders-programi/duzen', deps.yazmaYetkisi, (req, res) => {
    const kurul = String(req.query.kurul || '');
    const tum = oku();
    delete tum[kurul];
    fs.writeFileSync(dosya, JSON.stringify(tum, null, 1));
    res.json({ success: true });
  });
}
