/**
 * Revize Ders İşçisi (Yönetim → Yeni dersler → Revize): cihazda (Claude Code oturumu içinden) yeniden üretilen ders
 * taslakları. Taslaklar `<kök>/ders_isci/taslak/<is_id>/` altında, durum.json'da `revize: true` ile durur.
 *
 *   GET  /taslaklar                    → revize taslakları + yeni/eski sürüm karşılaştırması
 *   GET  /taslak/:id                   → rapor, denetim, karşılaştırma
 *   GET  /taslak/:id/dosya/:ad         → çıktı dosyası
 *   POST /taslak/:id/islem {islem}     ← degistir | ekle | kaldir | ikisini_tut
 *
 * İşlem: karar.json yazılır, `yayinla.py --yerel --is <id>` (deste/not/soru/sözlük kanonik kaynaklara) ve ardından
 * `npx vite build` arka planda çalışır; ilerleme taslağın yayin.json'unda ve bu modüldeki iş durumunda görünür.
 * server.ts: app.use('/api/admin/ders-revize', requireAdmin, dersRevizeRouter(__dirname));
 */
import express from 'express';
import fs from 'fs';
import path from 'path';
import { spawn } from 'child_process';

const ID = /^[0-9]{8}-[0-9a-f]{10}(?:-\d+)?$/;
const DOSYALAR = new Set(['deck.json', 'ornek_sorular.json', 'sozluk.json', 'hastaliklar.json', 'bilgi_havuzu.jsonl',
  'cikmis_baglantilari.json', 'ders_notu.md', 'ders_paketi.json', 'rapor.md', 'denetim.json']);
const ISLEMLER = new Set(['degistir', 'ekle', 'kaldir', 'ikisini_tut']);

const oku = (p: string, vars: any = null) => {
  try {
    return JSON.parse(fs.readFileSync(p, 'utf8'));
  } catch {
    return vars;
  }
};

/** Bir destenin öğrenciye gösterilen ölçüleri (Öğren'deki sürüm diyaloğuyla aynı tanım: splitLearningDecks). */
export function desteOlcusu(d: any) {
  const slides: any[] = Array.isArray(d?.slides) ? d.slides : [];
  let etkilesim = 0;
  let kelime = 0;
  for (const s of slides) {
    const els = s.interactiveElements || s.elements || (s.interactiveElement ? [s.interactiveElement] : []);
    etkilesim += Array.isArray(els) ? els.length : 0;
    kelime += String(s.synthesisNarrative || s.content || '').split(/\s+/).filter(Boolean).length;
  }
  return { adim: slides.length, etkilesim, kelime, boyutKb: Math.round(Buffer.byteLength(JSON.stringify(d || {})) / 1024) };
}

export function dersRevizeRouter(appDir: string): express.Router {
  const kok = process.env.MEDS_ISCI_DIR || path.resolve(appDir, '..', 'ders_isci');
  const taslakKok = path.join(kok, 'taslak');
  const desteDosyasi = path.resolve(appDir, 'src', 'data', 'interactive_learning_decks.json');
  const python = fs.existsSync(path.resolve(appDir, '.venv-ocr', 'bin', 'python'))
    ? path.resolve(appDir, '.venv-ocr', 'bin', 'python')
    : 'python3';
  let is: { id: string; islem: string; asama: string; basla: number; gunluk: string } | null = null;

  let desteOnbellek: { mtime: number; liste: any[] } | null = null;
  const desteler = (): any[] => {
    try {
      const m = fs.statSync(desteDosyasi).mtimeMs;
      if (!desteOnbellek || desteOnbellek.mtime !== m) desteOnbellek = { mtime: m, liste: oku(desteDosyasi, []) };
      return desteOnbellek.liste;
    } catch {
      return [];
    }
  };

  const ozet = (id: string) => {
    const d = path.join(taslakKok, id);
    const durum = oku(path.join(d, 'durum.json'), {});
    if (!durum?.revize) return null;
    const b = oku(path.join(d, 'baglam.json'), {});
    const den = oku(path.join(d, 'denetim.json'), {});
    const yeni = oku(path.join(d, 'deck.json'), null);
    const desteId = b.deste_id || durum.deste_id;
    // yayındaki sürümler: aynı kimlik + aynı sürüm grubundakiler
    const yayindakiler = desteler()
      .filter((x) => x.id === desteId || x.versionGroup === desteId)
      .map((x) => ({ id: x.id, baslik: x.title, surum: x.versionLabel || 'V1', ...desteOlcusu(x) }));
    return {
      is_id: id,
      durum: durum.durum,
      ozet: durum.ozet || '',
      deste_id: desteId,
      ders_id: b.ders_id,
      ders: b.program?.ders,
      konu: b.program?.konu,
      pdf: b.pdf_adi,
      denetim_hata: den.hata,
      sayilar: den.sayilar || {},
      referans: (den.referansla_tamamlanan || []).length,
      yeni: yeni ? { baslik: yeni.title, ...desteOlcusu(yeni) } : null,
      yayindakiler,
      alternatif: yayindakiler.length > 0,
      karar: oku(path.join(d, 'karar.json'), null),
      yayin: oku(path.join(d, 'yayin.json'), null),
      calisiyor: is?.id === id ? is : null,
      zaman: durum.zaman || fs.statSync(d).mtimeMs / 1000,
    };
  };

  const r = express.Router();
  r.use((_req, res, next) => {
    res.setHeader('Cache-Control', 'no-store');
    next();
  });

  r.get('/taslaklar', (_req, res) => {
    if (!fs.existsSync(taslakKok)) return res.json({ taslaklar: [], is });
    const liste = fs
      .readdirSync(taslakKok)
      .filter((x) => ID.test(x))
      .map(ozet)
      .filter(Boolean)
      .sort((a: any, b: any) => (b.zaman || 0) - (a.zaman || 0));
    res.json({ taslaklar: liste, is });
  });

  r.get('/taslak/:id', (req, res) => {
    const id = req.params.id;
    if (!ID.test(id)) return res.status(400).json({ hata: 'geçersiz kimlik' });
    const o = ozet(id);
    if (!o) return res.status(404).json({ hata: 'taslak yok' });
    const d = path.join(taslakKok, id);
    let rapor = '';
    try {
      rapor = fs.readFileSync(path.join(d, 'rapor.md'), 'utf8');
    } catch {}
    res.json({ ...o, rapor, denetim: oku(path.join(d, 'denetim.json'), {}), dosyalar: fs.readdirSync(d).filter((f) => DOSYALAR.has(f)) });
  });

  r.get('/taslak/:id/dosya/:ad', (req, res) => {
    const { id, ad } = req.params;
    if (!ID.test(id) || !DOSYALAR.has(ad)) return res.status(404).json({ hata: 'yol yok' });
    const p = path.join(taslakKok, id, ad);
    if (!fs.existsSync(p)) return res.status(404).json({ hata: 'dosya yok' });
    res.type(ad.endsWith('.md') ? 'text/markdown; charset=utf-8' : ad.endsWith('.jsonl') ? 'text/plain; charset=utf-8' : 'application/json');
    res.send(fs.readFileSync(p));
  });

  r.post('/taslak/:id/islem', express.json(), (req, res) => {
    const id = req.params.id;
    const islem = String(req.body?.islem || '');
    if (!ID.test(id) || !ISLEMLER.has(islem)) return res.status(400).json({ hata: 'geçersiz istek' });
    const o: any = ozet(id);
    if (!o) return res.status(404).json({ hata: 'taslak yok' });
    if (is) return res.status(409).json({ hata: `Başka bir yayın sürüyor (${is.id}). Bitince yeniden dene.` });
    if (o.yayin?.durum === 'yayinlandi') return res.status(409).json({ hata: 'Bu taslak zaten yayınlandı.' });
    if (islem === 'ekle' && o.alternatif) return res.status(400).json({ hata: 'Yayında bir sürümü var: Yer değiştir ya da Her ikisini tut.' });
    if ((islem === 'degistir' || islem === 'ikisini_tut') && !o.alternatif) return res.status(400).json({ hata: 'Yayında alternatif yok: Ekle.' });
    if (o.denetim_hata) return res.status(400).json({ hata: `İşçi denetiminde ${o.denetim_hata} HATA var.` });

    const d = path.join(taslakKok, id);
    const kim = String(req.headers['x-admin-email'] || '');
    const zaman = Date.now() / 1000;
    if (islem === 'kaldir') {
      fs.writeFileSync(path.join(d, 'karar.json'), JSON.stringify({ karar: 'reddet', islem, kim, zaman }, null, 1));
      fs.writeFileSync(path.join(d, 'durum.json'), JSON.stringify({ ...oku(path.join(d, 'durum.json'), {}), durum: 'reddedildi', zaman }, null, 1));
      return res.json({ ok: true, durum: 'reddedildi' });
    }
    fs.writeFileSync(path.join(d, 'karar.json'), JSON.stringify({ karar: 'onayla', islem, kim, zaman }, null, 1));
    try {
      fs.unlinkSync(path.join(d, 'yayin.json'));
    } catch {}
    is = { id, islem, asama: 'yayınlanıyor', basla: Date.now(), gunluk: '' };
    const calistir = (cmd: string, args: string[], asama: string) =>
      new Promise<number>((coz) => {
        if (is) is.asama = asama;
        const p = spawn(cmd, args, { cwd: appDir, env: { ...process.env, CUDA_VISIBLE_DEVICES: '' } });
        const ekle = (b: Buffer) => {
          if (is) is.gunluk = (is.gunluk + b.toString()).slice(-4000);
        };
        p.stdout.on('data', ekle);
        p.stderr.on('data', ekle);
        p.on('close', (c) => coz(c ?? 1));
        p.on('error', () => coz(1));
      });
    (async () => {
      const kod = await calistir(python, ['scripts/ders_isci/yayinla.py', '--yerel', '--is', id], 'kaynaklara yazılıyor');
      if (kod === 0) {
        desteOnbellek = null;
        const b = await calistir('npx', ['vite', 'build'], 'site derleniyor');
        const y = oku(path.join(d, 'yayin.json'), {});
        fs.writeFileSync(path.join(d, 'yayin.json'), JSON.stringify({ ...y, site_derlendi: b === 0 }, null, 1));
      } else if (!fs.existsSync(path.join(d, 'yayin.json'))) {
        fs.writeFileSync(path.join(d, 'yayin.json'), JSON.stringify({ durum: 'hata', hatalar: [is?.gunluk.slice(-1500)] }, null, 1));
      }
      is = null;
    })();
    res.json({ ok: true, durum: 'basladi' });
  });

  return r;
}
