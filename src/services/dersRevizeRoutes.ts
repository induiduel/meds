/**
 * Revize Ders İşçisi (Yönetim → Yeni dersler → Revize): cihazda (Claude Code oturumu içinden) yeniden üretilen ders
 * taslakları. Taslaklar `<kök>/ders_isci/taslak/<is_id>/` altında, durum.json'da `revize: true` ile durur.
 *
 *   GET  /taslaklar                    → revize taslakları + yeni/eski sürüm karşılaştırması
 *   GET  /taslak/:id                   → rapor, denetim, karşılaştırma
 *   GET  /taslak/:id/dosya/:ad         → çıktı dosyası
 *   POST /taslak/:id/islem {islem}     ← degistir | ekle | kaldir | ikisini_tut
 *   POST /taslak/:id/yeniden           ← yayınlanamayan / kesilen / site derlemesi düşen taslağı yeniden gönder
 *   POST /yeniden                      ← bunların hepsini yeniden gönder
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
      yayinda: desteler().some((x) => x.revizeIsId === id),
      calisiyor: is?.id === id ? is : sira.some((x) => x.id === id) ? { asama: 'sırada', gunluk: '' } : null,
      zaman: durum.zaman || fs.statSync(d).mtimeMs / 1000,
    };
  };

  // Sıra bellekte durur: sunucu yayın sürerken yeniden başladıysa (ör. bellek taşması) onaylanıp yayınlanmamış taslaklar
  // sessizce kaybolmasın — "kesildi" diye işaretlenir, panelde "Yeniden gönder" çıkar.
  try {
    for (const id of fs.existsSync(taslakKok) ? fs.readdirSync(taslakKok).filter((x) => ID.test(x)) : []) {
      const d = path.join(taslakKok, id);
      const k = oku(path.join(d, 'karar.json'), null);
      if (!oku(path.join(d, 'durum.json'), {})?.revize || k?.karar !== 'onayla' || k?.islem === 'kaldir' || fs.existsSync(path.join(d, 'yayin.json'))) continue;
      fs.writeFileSync(
        path.join(d, 'yayin.json'),
        JSON.stringify({ durum: 'kesildi', kip: k.islem, hatalar: ['Sunucu yayın sırasında yeniden başladı; iş tamamlanmadı. "Yeniden gönder" ile tekrar dene.'] }, null, 1),
      );
    }
  } catch {}

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
    res.json({ taslaklar: liste, is, sira: sira.map((x) => x.id) });
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

  // Sıra: işlemler tek tek yayınlanır (yayinla.py aynı kaynak dosyalara yazar); site en sonda bir kez derlenir.
  const sira: { id: string; islem: string; kim: string }[] = [];
  const bekleyenIds = () => new Set([...(is ? [is.id] : []), ...sira.map((x) => x.id)]);

  /** İşlemin bu taslak için geçerli olup olmadığı; geçerliyse null. */
  const engel = (o: any, islem: string): string | null => {
    if (!o) return 'taslak yok';
    if (bekleyenIds().has(o.is_id)) return 'Bu taslak zaten sırada.';
    if (o.yayin?.durum === 'yayinlandi') return 'Bu revize zaten yayınlandı; aynı revize ikinci kez gönderilemez.';
    if (o.karar?.islem === 'kaldir' || o.durum === 'reddedildi') return 'Bu taslak kaldırıldı.';
    if (desteler().some((x) => x.revizeIsId === o.is_id)) return 'Bu revize zaten yayında; aynı revize ikinci kez gönderilemez.';
    if (islem === 'kaldir') return null;
    if (islem === 'ekle' && o.alternatif) return 'Yayında bir sürümü var: Yer değiştir ya da Her ikisini tut.';
    if ((islem === 'degistir' || islem === 'ikisini_tut') && !o.alternatif) return 'Yayında alternatif yok: Ekle.';
    if (o.denetim_hata) return `İşçi denetiminde ${o.denetim_hata} HATA var.`;
    return null;
  };

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

  let isliyor = false;
  const isle = async () => {
    if (isliyor) return;
    isliyor = true;
    const yayinlananlar: string[] = [];
    const derlenecek: string[] = [];
    while (sira.length) {
      const { id, islem } = sira.shift()!;
      const d = path.join(taslakKok, id);
      if (islem === 'derle') {
        derlenecek.push(id);
        continue;
      }
      is = { id, islem, asama: 'kaynaklara yazılıyor', basla: Date.now(), gunluk: '' };
      const kod = await calistir(python, ['scripts/ders_isci/yayinla.py', '--yerel', '--is', id], `kaynaklara yazılıyor (${sira.length} sırada)`);
      desteOnbellek = null;
      if (kod === 0) yayinlananlar.push(id);
      else if (!fs.existsSync(path.join(d, 'yayin.json')))
        fs.writeFileSync(path.join(d, 'yayin.json'), JSON.stringify({ durum: 'hata', kip: islem, hatalar: [is.gunluk.slice(-1500)] }, null, 1));
    }
    yayinlananlar.push(...derlenecek);
    if (yayinlananlar.length) {
      is = { id: yayinlananlar[yayinlananlar.length - 1], islem: 'derleme', asama: 'site derleniyor', basla: Date.now(), gunluk: '' };
      const b = await calistir('npx', ['vite', 'build'], 'site derleniyor');
      for (const id of yayinlananlar) {
        const yp = path.join(taslakKok, id, 'yayin.json');
        fs.writeFileSync(yp, JSON.stringify({ ...oku(yp, {}), site_derlendi: b === 0 }, null, 1));
      }
    }
    is = null;
    isliyor = false;
  };

  const sirayaAl = (id: string, islem: string, kim: string) => {
    const d = path.join(taslakKok, id);
    const zaman = Date.now() / 1000;
    if (islem === 'kaldir') {
      fs.writeFileSync(path.join(d, 'karar.json'), JSON.stringify({ karar: 'reddet', islem, kim, zaman }, null, 1));
      fs.writeFileSync(path.join(d, 'durum.json'), JSON.stringify({ ...oku(path.join(d, 'durum.json'), {}), durum: 'reddedildi', zaman }, null, 1));
      return;
    }
    fs.writeFileSync(path.join(d, 'karar.json'), JSON.stringify({ karar: 'onayla', islem, kim, zaman }, null, 1));
    try {
      fs.unlinkSync(path.join(d, 'yayin.json'));
    } catch {}
    sira.push({ id, islem, kim });
  };

  r.post('/taslak/:id/islem', express.json(), (req, res) => {
    const id = req.params.id;
    const islem = String(req.body?.islem || '');
    if (!ID.test(id) || !ISLEMLER.has(islem)) return res.status(400).json({ hata: 'geçersiz istek' });
    const e = engel(ozet(id), islem);
    if (e) return res.status(e === 'taslak yok' ? 404 : 409).json({ hata: e });
    sirayaAl(id, islem, String(req.headers['x-admin-email'] || ''));
    isle();
    res.json({ ok: true, durum: islem === 'kaldir' ? 'reddedildi' : 'sirada' });
  });

  /**
   * Yeniden gönderilebilir mi: yayın hatası / denetim hatası / sunucu yeniden başlarken kesilen yayın / site derlemesi düşen.
   * Dönüş: yapılacak iş ('yayinla' | 'derle' | 'onar') ya da engel metni.
   */
  const yenidenNe = (o: any): { is: 'yayinla' | 'derle' | 'onar' } | { engel: string } => {
    if (!o) return { engel: 'taslak yok' };
    if (bekleyenIds().has(o.is_id)) return { engel: 'Bu taslak zaten sırada.' };
    if (o.karar?.karar !== 'onayla' || o.karar?.islem === 'kaldir') return { engel: 'Bu taslak gönderilmemiş; önce bir işlem seç.' };
    // revize zaten destelerde: yayın aslında olmuş (ör. eşzamanlı ikinci gönderim "zaten yayında" diye düştü) → kaydı düzelt
    if (o.yayinda) return o.yayin?.durum === 'yayinlandi' && o.yayin?.site_derlendi === false ? { is: 'derle' } : o.yayin?.durum === 'yayinlandi' ? { engel: 'Bu revize sitede yayında.' } : { is: 'onar' };
    if (o.yayin?.durum === 'yayinlandi') return o.yayin.site_derlendi === false ? { is: 'derle' } : { engel: 'Bu revize sitede yayında.' };
    if (o.denetim_hata) return { engel: `İşçi denetiminde ${o.denetim_hata} HATA var; taslak yeniden üretilmeli.` };
    return { is: 'yayinla' };
  };

  const yenidenGonder = (o: any, kim: string): string | null => {
    const n = yenidenNe(o);
    if ('engel' in n) return n.engel;
    const d = path.join(taslakKok, o.is_id);
    const islem = o.karar?.islem || o.yayin?.kip || (o.alternatif ? 'ikisini_tut' : 'ekle');
    if (n.is === 'onar') {
      const deste = desteler().find((x) => x.revizeIsId === o.is_id);
      fs.writeFileSync(
        path.join(d, 'yayin.json'),
        JSON.stringify({ ...(o.yayin || {}), hatalar: undefined, durum: 'yayinlandi', kip: islem, deste_id: deste?.id, yayin_zamani: new Date().toISOString(), onarildi: true }, null, 1),
      );
      return null;
    }
    if (n.is === 'derle') {
      sira.push({ id: o.is_id, islem: 'derle', kim });
      return null;
    }
    try {
      fs.unlinkSync(path.join(d, 'yayin.json'));
    } catch {}
    fs.writeFileSync(path.join(d, 'karar.json'), JSON.stringify({ ...o.karar, kim: kim || o.karar?.kim, zaman: Date.now() / 1000, yeniden: true }, null, 1));
    sira.push({ id: o.is_id, islem, kim });
    return null;
  };

  r.post('/taslak/:id/yeniden', express.json(), (req, res) => {
    const id = req.params.id;
    if (!ID.test(id)) return res.status(400).json({ hata: 'geçersiz kimlik' });
    const o = ozet(id);
    const e = yenidenGonder(o, String(req.headers['x-admin-email'] || ''));
    if (e) return res.status(e === 'taslak yok' ? 404 : 409).json({ hata: e });
    isle();
    res.json({ ok: true });
  });

  r.post('/yeniden', express.json(), (req, res) => {
    const kim = String(req.headers['x-admin-email'] || '');
    const alinan: string[] = [];
    for (const id of fs.existsSync(taslakKok) ? fs.readdirSync(taslakKok).filter((x) => ID.test(x)) : []) {
      const o: any = ozet(id);
      if (!o || 'engel' in yenidenNe(o)) continue;
      if (!yenidenGonder(o, kim)) alinan.push(id);
    }
    if (alinan.length) isle();
    res.json({ ok: true, alinan });
  });

  /** Toplu gönderim: bekleyen tüm taslaklar — alternatifi olan "Her ikisini tut", olmayan "Ekle". */
  r.post('/toplu', express.json(), (req, res) => {
    const kim = String(req.headers['x-admin-email'] || '');
    const alinan: { id: string; islem: string }[] = [];
    const atlanan: { id: string; neden: string }[] = [];
    for (const id of fs.existsSync(taslakKok) ? fs.readdirSync(taslakKok).filter((x) => ID.test(x)) : []) {
      const o: any = ozet(id);
      if (!o || o.durum !== 'onay_bekliyor') continue;
      const islem = o.alternatif ? 'ikisini_tut' : 'ekle';
      const e = engel(o, islem);
      if (e) {
        atlanan.push({ id, neden: e });
        continue;
      }
      sirayaAl(id, islem, kim);
      alinan.push({ id, islem });
    }
    if (alinan.length) isle();
    res.json({ ok: true, alinan, atlanan });
  });

  return r;
}
