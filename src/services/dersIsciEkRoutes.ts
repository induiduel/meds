/**
 * Ders işçisi onay kapısı — yöneticinin öğrenci notu / ders ses kaydı yüklemesi (2026-10-24).
 * Dosyalar doğrudan diske akar (belleğe alınmaz): data/ders_isci_ekler/<is_id>/{not,ses}/<ad>. İşçi konteyneri aynı klasörü
 * salt okunur görür (/app/data …; scripts/ders_isci/ayarlar.py EK_DIZIN) ve onayda iş kaydına yazar.
 * server.ts: app.use('/api/admin/ders-isci-ek', requireAdmin, dersIsciEkRouter());
 *   GET    /:isId                     → {not: [{ad, boyut}], ses: [...]}
 *   POST   /:isId?tur=not|ses&ad=<dosya adı>   (gövde: ham dosya)  → {ok, ad, boyut}
 *   DELETE /:isId?tur=not|ses&ad=<dosya adı>
 */
import express from 'express';
import fs from 'node:fs';
import path from 'node:path';

const KOK = path.resolve(process.cwd(), 'data', 'ders_isci_ekler');
const ID = /^[0-9]{8}-[0-9a-f]{10}(?:-\d+)?$/;
const SINIR: Record<string, number> = { not: 50 * 1024 * 1024, ses: 600 * 1024 * 1024 };
const UZANTI: Record<string, RegExp> = {
  not: /\.(pdf|png|jpe?g|webp|heic|txt|md|docx?)$/i,
  ses: /\.(mp3|m4a|aac|wav|ogg|opus|webm|mp4|amr|3gp)$/i,
};

function guvenliAd(ad: string): string {
  const temiz = path.basename(String(ad || '')).replace(/[^\p{L}\p{N}._ -]+/gu, '_').replace(/^\.+/, '').slice(0, 120);
  return temiz || `dosya-${Date.now()}`;
}

function liste(isId: string) {
  const out: Record<string, { ad: string; boyut: number }[]> = { not: [], ses: [] };
  for (const tur of Object.keys(out)) {
    const d = path.join(KOK, isId, tur);
    if (!fs.existsSync(d)) continue;
    out[tur] = fs.readdirSync(d).filter((f) => !f.endsWith('.yukleniyor'))
      .map((f) => ({ ad: f, boyut: fs.statSync(path.join(d, f)).size }));
  }
  return out;
}

export function dersIsciEkRouter(): express.Router {
  const r = express.Router();
  r.get('/:isId', (req, res) => {
    if (!ID.test(req.params.isId)) return res.status(400).json({ hata: 'geçersiz iş kimliği' });
    res.json(liste(req.params.isId));
  });
  r.post('/:isId', (req, res) => {
    const { isId } = req.params;
    const tur = String(req.query.tur || '');
    const ad = guvenliAd(String(req.query.ad || ''));
    if (!ID.test(isId)) return res.status(400).json({ hata: 'geçersiz iş kimliği' });
    if (!SINIR[tur]) return res.status(400).json({ hata: 'tur not|ses olmalı' });
    if (!UZANTI[tur].test(ad)) return res.status(400).json({ hata: `bu dosya türü ${tur} için kabul edilmiyor` });
    const boy = Number(req.headers['content-length'] || 0);
    if (boy > SINIR[tur]) return res.status(413).json({ hata: `dosya çok büyük (en çok ${SINIR[tur] / 1048576} MB)` });
    const d = path.join(KOK, isId, tur);
    fs.mkdirSync(d, { recursive: true });
    const hedef = path.join(d, ad);
    const gecici = `${hedef}.yukleniyor`;
    const yazici = fs.createWriteStream(gecici);
    let yazilan = 0;
    let bitti = false;
    const iptal = (kod: number, hata: string) => {
      if (bitti) return;
      bitti = true;
      yazici.destroy();
      fs.rmSync(gecici, { force: true });
      if (!res.headersSent) res.status(kod).json({ hata });
    };
    req.on('data', (parca: Buffer) => {
      yazilan += parca.length;
      if (yazilan > SINIR[tur]) { req.unpipe(yazici); iptal(413, 'dosya çok büyük'); req.resume(); }
    });
    req.on('aborted', () => iptal(499, 'yükleme kesildi'));
    yazici.on('error', (e) => iptal(500, `yazılamadı: ${e.message}`));
    yazici.on('finish', () => {
      if (bitti) return;
      bitti = true;
      if (!yazilan) { fs.rmSync(gecici, { force: true }); return res.status(400).json({ hata: 'boş dosya' }); }
      fs.renameSync(gecici, hedef);
      res.json({ ok: true, ad, boyut: yazilan, ekler: liste(isId) });
    });
    req.pipe(yazici);
  });
  r.delete('/:isId', (req, res) => {
    const { isId } = req.params;
    const tur = String(req.query.tur || '');
    if (!ID.test(isId) || !SINIR[tur]) return res.status(400).json({ hata: 'geçersiz istek' });
    fs.rmSync(path.join(KOK, isId, tur, guvenliAd(String(req.query.ad || ''))), { force: true });
    res.json({ ok: true, ekler: liste(isId) });
  });
  return r;
}
