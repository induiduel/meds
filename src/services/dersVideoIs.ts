// Sesli ders · yerel GPU video iş kuyruğu (yalnız yönetici). Öğrenciler videoyu kendi cihazında üretir (cdVideo.ts);
// yönetici isterse iş burada kuyruğa girer, yerel bilgisayardaki işçi (scripts/ders_video/video_isci.py) alır, NVENC ile
// üretip MP4'ü Oracle'a rsync'ler ve durumu bildirir. GPU kuralları: AGENTS.md §10 beşinci istisna (meds-gpuguard + saat kilidi).
//   POST   /api/canli-ders/video-is              { key, vid, cozunurluk }  → iş ekler
//   GET    /api/canli-ders/video-is              → son işler + işçi son görülme
//   DELETE /api/canli-ders/video-is/:id          → iptal (işçi bir sonraki bildiriminde durur)
//   GET    /api/canli-ders/video-is/:id/baglanti → 10 dk geçerli imzalı indirme adresi
//   GET    /api/canli-ders/video-is/:id/indir?t= → MP4 (Range)
//   İşçi (x-panel-secret): POST /api/canli-ders/video-is/al · POST /api/canli-ders/video-is/:id/durum
import type { Express, Request, Response, NextFunction } from 'express';
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { isStrongAdmin } from './peopleInsights';

const KOK = path.join(process.cwd(), 'data', 'ders_video');
const KUYRUK = path.join(KOK, 'kuyruk.json');
const CIKTI = path.join(KOK, 'cikti');
const COZ = new Set(['720p', '1080p', '2k', '4k']);
const SON_IS = 40;

type Durum = 'bekliyor' | 'calisiyor' | 'bitti' | 'hata' | 'iptal';
interface Is {
  id: string; key: string; vid: string; cozunurluk: string; durum: Durum;
  istendi: string; basladi?: string; bitti?: string; oran?: number; mesaj?: string; bayt?: number; kodlayici?: string;
}
interface Kuyruk { isler: Is[]; isci?: { gorulme: string; gpu?: string } }

const oku = (): Kuyruk => { try { return JSON.parse(fs.readFileSync(KUYRUK, 'utf8')); } catch { return { isler: [] }; } };
const yaz = (k: Kuyruk) => {
  fs.mkdirSync(KOK, { recursive: true });
  const tmp = `${KUYRUK}.tmp`;
  fs.writeFileSync(tmp, JSON.stringify(k, null, 1));
  fs.renameSync(tmp, KUYRUK);
};
const imza = (id: string, son: number) =>
  crypto.createHmac('sha256', String(process.env.MEDS_PANEL_SECRET || 'yok')).update(`${id}.${son}`).digest('hex').slice(0, 32);
const dosya = (id: string) => path.join(CIKTI, `${id}.mp4`);
const guvenli = (s: unknown, re: RegExp) => (typeof s === 'string' && re.test(s) ? s : null);

export function registerDersVideoIsRoutes(app: Express, adminEmail: string) {
  const guclu = async (req: Request, res: Response, next: NextFunction) => {
    if (await isStrongAdmin(req, adminEmail)) return next();
    res.status(403).json({ error: 'Bu işlem yalnız yönetici içindir.' });
  };

  app.post('/api/canli-ders/video-is', guclu, (req, res) => {
    const key = guvenli(req.body?.key, /^[a-z0-9-]{3,120}$/);
    const vid = guvenli(req.body?.vid, /^[A-Za-z0-9._-]{1,120}$/);
    const coz = String(req.body?.cozunurluk || '');
    if (!key || !vid || !COZ.has(coz)) return res.status(400).json({ error: 'Ders, ses ya da çözünürlük geçersiz.' });
    const k = oku();
    const var_ = k.isler.find((x) => x.key === key && x.vid === vid && x.cozunurluk === coz && (x.durum === 'bekliyor' || x.durum === 'calisiyor'));
    if (var_) return res.json({ ok: true, is: var_, zatenVar: true });
    const is: Is = { id: `v${Date.now().toString(36)}${crypto.randomBytes(3).toString('hex')}`, key, vid, cozunurluk: coz, durum: 'bekliyor', istendi: new Date().toISOString() };
    k.isler.push(is);
    // eski bitmiş işler ve dosyaları temizlenir (son SON_IS iş kalır)
    while (k.isler.length > SON_IS) { const e = k.isler.shift()!; try { fs.unlinkSync(dosya(e.id)); } catch { /* yok */ } }
    yaz(k);
    res.json({ ok: true, is });
  });

  app.get('/api/canli-ders/video-is', guclu, (_req, res) => {
    res.setHeader('Cache-Control', 'no-store');
    const k = oku();
    res.json({ isler: [...k.isler].reverse(), isci: k.isci || null });
  });

  app.delete('/api/canli-ders/video-is/:id', guclu, (req, res) => {
    const k = oku();
    const is = k.isler.find((x) => x.id === req.params.id);
    if (!is) return res.status(404).json({ error: 'İş yok.' });
    if (is.durum === 'bekliyor' || is.durum === 'calisiyor') { is.durum = 'iptal'; is.bitti = new Date().toISOString(); }
    else { k.isler = k.isler.filter((x) => x !== is); try { fs.unlinkSync(dosya(is.id)); } catch { /* yok */ } }
    yaz(k);
    res.json({ ok: true });
  });

  app.get('/api/canli-ders/video-is/:id/baglanti', guclu, (req, res) => {
    const is = oku().isler.find((x) => x.id === req.params.id);
    if (!is || is.durum !== 'bitti' || !fs.existsSync(dosya(is.id))) return res.status(404).json({ error: 'Video hazır değil.' });
    const son = Date.now() + 10 * 60_000;
    res.json({ url: `/api/canli-ders/video-is/${is.id}/indir?s=${son}&t=${imza(is.id, son)}` });
  });

  app.get('/api/canli-ders/video-is/:id/indir', (req, res) => {
    const id = String(req.params.id);
    const son = Number(req.query.s) || 0;
    const t = String(req.query.t || '');
    const beklenen = imza(id, son);
    if (son < Date.now() || t.length !== beklenen.length || !crypto.timingSafeEqual(Buffer.from(t), Buffer.from(beklenen))) {
      return res.status(403).json({ error: 'Bağlantının süresi doldu.' });
    }
    const is = oku().isler.find((x) => x.id === id);
    if (!is || !fs.existsSync(dosya(id))) return res.status(404).json({ error: 'Video yok.' });
    const ad = `${is.key} (${is.cozunurluk} 60fps).mp4`;
    res.setHeader('Content-Disposition', `attachment; filename*=UTF-8''${encodeURIComponent(ad)}`);
    res.setHeader('Cache-Control', 'private, no-store');
    res.sendFile(dosya(id), { acceptRanges: true }, (err: any) => { if (err && !res.headersSent) res.status(500).end(); });
  });

  // ——— işçi ———
  app.post('/api/canli-ders/video-is/al', guclu, (req, res) => {
    const k = oku();
    k.isci = { gorulme: new Date().toISOString(), gpu: String(req.body?.gpu || '').slice(0, 120) };
    const is = req.body?.hazir === false ? undefined : k.isler.find((x) => x.durum === 'bekliyor');
    if (is) { is.durum = 'calisiyor'; is.basladi = new Date().toISOString(); is.oran = 0; }
    yaz(k);
    res.json({ is: is || null });
  });

  app.post('/api/canli-ders/video-is/:id/durum', guclu, (req, res) => {
    const k = oku();
    const is = k.isler.find((x) => x.id === req.params.id);
    if (!is) return res.status(404).json({ error: 'İş yok.' });
    k.isci = { ...(k.isci || {}), gorulme: new Date().toISOString() };
    if (is.durum === 'iptal') { yaz(k); return res.json({ iptal: true }); }
    const d = String(req.body?.durum || '');
    if (d === 'calisiyor' || d === 'bitti' || d === 'hata') is.durum = d;
    if (typeof req.body?.oran === 'number') is.oran = Math.max(0, Math.min(1, req.body.oran));
    if (typeof req.body?.mesaj === 'string') is.mesaj = req.body.mesaj.slice(0, 300);
    if (typeof req.body?.kodlayici === 'string') is.kodlayici = req.body.kodlayici.slice(0, 40);
    if (d === 'bitti') {
      if (!fs.existsSync(dosya(is.id))) { is.durum = 'hata'; is.mesaj = 'Video dosyası sunucuya ulaşmadı.'; }
      else is.bayt = fs.statSync(dosya(is.id)).size;
    }
    if (d === 'bitti' || d === 'hata') is.bitti = new Date().toISOString();
    yaz(k);
    res.json({ ok: true, iptal: false });
  });
}
