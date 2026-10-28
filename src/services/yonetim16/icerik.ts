/**
 * Yönetim v16 — İçerik uçları: Kurullar ve dersler, Öğrenme, Kaynaklar (server-only, 2026-10-28).
 * Belge: docs/YONETIM_V16_KIT.md §7.
 *
 *  GET  /api/admin/kurullar                 kurul takvimi (kurul_takvimi_ozet.json) + aktif kurul
 *  PUT  /api/admin/kurullar/:no             tek kurulun ad/kod/tarihleri  (no = 1–6 ya da "genel": final/bütünleme)
 *  GET  /api/admin/dersler                  ders kayıt defteri (dersler/kN.json birleşik) + katman özeti — sunucu sayfalı
 *  GET  /api/admin/dersler/:id              ders ayrıntısı: o derse bağlı her katman + görünürlük
 *  PUT  /api/admin/dersler/:id              tek dersin konu/hoca/tarih/saat/branş alanları (id ve kod kalıcıdır, kural 15)
 *  GET  /api/admin/branslar · PUT /api/admin/branslar/:harf   branş adı/kısa adı (harf ve slug kalıcıdır)
 *  GET  /api/admin/sesli-dersler[/:key]     sesli ders kayıtları + katman dosyaları
 *  GET  /api/admin/spot-cozucu              önem / asistan / çözücü envanteri (branş × ders)
 *  GET  /api/admin/ders-icerik[/:key]       ders içerik paketleri (src/data/ders_icerik)
 *  GET  /api/admin/sinav-dagilimi · PUT /api/admin/sinav-dagilimi/:kurul
 *  GET  /api/admin/k16/katalog/:varlik[/meta|/:id] · PUT /api/admin/k16/katalog/:varlik/:id
 *       dataCatalogService varlıkları + bu dosyadaki bağdaştırıcılar (spot, kisaltma, terim, saglik) v16 liste biçiminde
 *
 * Yazmalar: data/content katmanına (writableContent) + atomikJsonGuncelle (yedek katman DIŞINDA data/_yedek/<ad>)
 * + SSE content_changed. Denetim kaydı ara katmanda; hedef + fark burada bildirilir. Toplu yazma ucu YOK (kural 15).
 */
import type express from 'express';
import fs from 'fs';
import path from 'path';
import { listeSorgusu, diziSayfala, katla } from './sayfalama.ts';
import { atomikJsonGuncelle } from './atomikJson.ts';
import { denetimHedef, denetimFark } from './denetim.ts';
import { siteAyarOku } from './siteAyar.ts';
import { resolveContent, writableContent } from '../contentOverlay.ts';
import { katalogErisimi } from '../dataCatalogService.ts';

type Any = Record<string, any>;
type Deps = {
  rootDir: string;
  dataDir: string;
  requireAdmin: express.RequestHandler;
  broadcast: (ev: string, d: any) => void;
  getDecks: () => any[];
};

/* ---------- okuma önbelleği (mtime) ---------- */
const onbellek = new Map<string, { mtime: number; veri: any }>();
function oku<T = any>(file: string, bos: T): T {
  const f = resolveContent(file);
  try {
    const m = fs.statSync(f).mtimeMs;
    const c = onbellek.get(f);
    if (c && c.mtime === m) return c.veri;
    const veri = JSON.parse(fs.readFileSync(f, 'utf8'));
    onbellek.set(f, { mtime: m, veri });
    return veri;
  } catch {
    return bos;
  }
}
const varMi = (f: string) => { try { return fs.existsSync(f); } catch { return false; } };
const ls = (d: string) => { try { return fs.readdirSync(d); } catch { return [] as string[]; } };
const TARIH = /^\d{4}-\d{2}-\d{2}$/;
const kirp = (v: unknown, n = 300) => String(v ?? '').trim().slice(0, n);

export function registerIcerik16Routes(app: express.Express, d: Deps) {
  const SRC = path.join(d.rootDir, 'src', 'data');
  const SES = path.join(d.dataDir, 'sesli_anlatim');
  const YEDEK = (ad: string) => path.join(d.dataDir, '_yedek', ad);
  const TAKVIM = path.join(SRC, 'kurul_takvimi_ozet.json');
  const DERSLER = (k: number) => path.join(SRC, 'dersler', `k${k}.json`);
  const BRANSLAR = path.join(SRC, 'dersler', 'branslar.json');
  const DAGILIM = path.join(SRC, 'sinav_dagilimi.json');
  const PAKET = path.join(SRC, 'ders_icerik');
  const gor = () => siteAyarOku().gorunurluk || {};
  const kim = (req: express.Request) => String((req as any).adminAuth?.email || req.headers['x-admin-email'] || 'yönetici');

  /** src/data dosyasını katmanda kilitli günceller; katmanda kopya yoksa paketteki dosyadan başlar */
  async function katmanGuncelle<T>(file: string, ad: string, fn: (eski: T) => T): Promise<T> {
    const hedef = writableContent(file);
    // Katman kayıt düzeyinde farktır: başlangıç kaynak + fark birleşimi (yalnız kaynaktan başlamak önceki farkları silerdi)
    if (!varMi(hedef)) { const birlesik = resolveContent(file); if (varMi(birlesik)) fs.copyFileSync(birlesik, hedef); }
    const sonuc = await atomikJsonGuncelle<T>(hedef, (eski) => fn(eski as T), { yedek: 5, yedekKlasoru: YEDEK(ad) });
    onbellek.delete(hedef);
    return sonuc;
  }
  const yayinla = (entity: string, ids: string[] = []) => d.broadcast('content_changed', { entity, ids: ids.slice(0, 200), at: Date.now() });

  /* ================= Kurullar ================= */
  const aktifKurulNo = (kurullar: Any[]) => {
    const p = (n: number) => String(n).padStart(2, '0');
    const t = new Date();
    const gun = `${t.getFullYear()}-${p(t.getMonth() + 1)}-${p(t.getDate())}`;
    return (kurullar.find((k) => gun <= k.sinav) || kurullar[kurullar.length - 1])?.kurul;
  };

  app.get('/api/admin/kurullar', d.requireAdmin, (_req, res) => {
    const t = oku<Any>(TAKVIM, {});
    const kurullar: Any[] = t.kurullar || [];
    const g = gor();
    const dersSayisi = (k: number) => (oku<Any>(DERSLER(k), {}).dersler || []).length;
    res.json({
      egitimYili: t.egitimYili, donem: t.donem, final: t.final, butunleme: t.butunleme, kaynak: t.kaynak,
      katmanda: resolveContent(TAKVIM) !== TAKVIM,
      aktif: aktifKurulNo(kurullar),
      kurullar: kurullar.map((k) => ({ ...k, dersSayisi: dersSayisi(k.kurul), gorunurluk: g[`kurul:${k.kurul}`] || 'acik' })),
    });
  });

  app.put('/api/admin/kurullar/:no', d.requireAdmin, async (req, res) => {
    const no = String(req.params.no);
    const b = req.body || {};
    try {
      let once: Any = {}, sonra: Any = {};
      await katmanGuncelle<Any>(TAKVIM, 'kurul_takvimi_ozet', (t) => {
        if (no === 'genel') {
          once = { final: t.final, butunleme: t.butunleme };
          for (const k of ['final', 'butunleme']) if (k in b) { if (!TARIH.test(String(b[k]))) throw new Error(`${k} YYYY-AA-GG olmalı`); t[k] = String(b[k]); }
          sonra = { final: t.final, butunleme: t.butunleme };
          return t;
        }
        const k = (t.kurullar || []).find((x: Any) => String(x.kurul) === no);
        if (!k) throw new Error('Kurul bulunamadı');
        once = { ...k };
        for (const a of ['baslangic', 'sinav', 'bitis']) if (a in b) { if (!TARIH.test(String(b[a]))) throw new Error(`${a} YYYY-AA-GG olmalı`); k[a] = String(b[a]); }
        if ('ad' in b) { const v = kirp(b.ad, 120); if (!v) throw new Error('ad boş olamaz'); k.ad = v; }
        if ('kod' in b) k.kod = kirp(b.kod, 30);
        if (k.sinav < k.baslangic) throw new Error('Sınav tarihi başlangıçtan önce olamaz');
        if (k.bitis < k.sinav) throw new Error('Bitiş sınavdan önce olamaz');
        sonra = { ...k };
        return t;
      });
      denetimHedef(res, no === 'genel' ? 'kurul-takvimi' : `kurul:${no}`);
      denetimFark(res, once, sonra);
      yayinla('kurullar', [no]);
      res.json({ ok: true, kayit: sonra });
    } catch (e: any) {
      res.status(400).json({ error: e?.message || 'kaydedilemedi' });
    }
  });

  /* ================= Branşlar ================= */
  const branslar = (): Any[] => oku<Any>(BRANSLAR, {}).branslar || [];
  const bransHarf = (kod: string) => String(kod || '').replace(/^\d+/, '').charAt(0);
  const bransOf = (ders: Any) => branslar().find((b) => b.harf === bransHarf(ders.kod)) || branslar().find((b) => b.ad === ders.brans);

  app.get('/api/admin/branslar', d.requireAdmin, (_req, res) => {
    const say = new Map<string, number>();
    for (let k = 1; k <= 6; k++) for (const x of oku<Any>(DERSLER(k), {}).dersler || []) { const h = bransHarf(x.kod); say.set(h, (say.get(h) || 0) + 1); }
    res.json({ branslar: branslar().map((b) => ({ ...b, dersSayisi: say.get(b.harf) || 0 })), aciklama: oku<Any>(BRANSLAR, {}).aciklama });
  });

  app.put('/api/admin/branslar/:harf', d.requireAdmin, async (req, res) => {
    const harf = String(req.params.harf);
    try {
      let once: Any = {}, sonra: Any = {};
      await katmanGuncelle<Any>(BRANSLAR, 'branslar', (t) => {
        const b = (t.branslar || []).find((x: Any) => x.harf === harf);
        if (!b) throw new Error('Branş bulunamadı');
        once = { ...b };
        if ('ad' in req.body) { const v = kirp(req.body.ad, 80); if (!v) throw new Error('ad boş olamaz'); b.ad = v; }
        if ('kisa' in req.body) { const v = kirp(req.body.kisa, 40); if (!v) throw new Error('kısa ad boş olamaz'); b.kisa = v; }
        sonra = { ...b };
        return t;
      });
      denetimHedef(res, `brans:${harf}`);
      denetimFark(res, once, sonra);
      yayinla('branslar', [harf]);
      res.json({ ok: true, kayit: sonra });
    } catch (e: any) {
      res.status(400).json({ error: e?.message || 'kaydedilemedi' });
    }
  });

  /* ================= Katman dizinleri ================= */
  let katmanOnbellek: { at: number; v: ReturnType<typeof katmanDizini> } | null = null;
  function katmanDizini() {
    const paketler = new Map<string, Any>();
    for (const f of ls(PAKET)) if (f.endsWith('.json')) {
      const p = oku<Any>(path.join(PAKET, f), null as any);
      if (p?.key) paketler.set(p.key, p);
    }
    const sesliListe: Any[] = oku<Any[]>(path.join(SES, 'dersler.json'), []);
    const sesliKeys = new Set<string>(sesliListe.map((x) => x.key));
    for (const f of ls(path.join(SES, 'metin'))) if (f.endsWith('.md')) sesliKeys.add(f.slice(0, -3));
    const desteler = d.getDecks().map((x: Any) => ({ id: String(x.id), title: x.shortTitle || x.title, slideCount: x.slideCount ?? (x.slides || []).length }));
    // önem / asistan / çözücü: <önek>_<tür>/index.json
    const envanter: Any[] = [];
    for (const dir of ls(SRC)) {
      const m = dir.match(/^(.+)_(onem|asistan|cozucu)$/);
      if (!m) continue;
      const idx = oku<Any>(path.join(SRC, dir, 'index.json'), null as any);
      for (const x of idx?.dersler || []) envanter.push({ dizin: dir, onek: m[1], tur: m[2], kod: String(x.kod), no: x.no, baslik: x.baslik, madde: x.madde ?? x.soru ?? x.adim ?? 0, ses: x.ses, cikmis: x.cikmis });
    }
    return { paketler, sesliKeys, sesliListe, desteler, envanter };
  }
  const katmanlar = () => {
    if (!katmanOnbellek || Date.now() - katmanOnbellek.at > 30_000) katmanOnbellek = { at: Date.now(), v: katmanDizini() };
    return katmanOnbellek.v;
  };
  const onekBul = (ders: Any) => { const b = bransOf(ders); return b ? (Number(ders.kurul) === 1 ? b.slug : `k${ders.kurul}${b.slug}`) : ''; };
  const kodEs = (x: string, ders: Any) => x === ders.kod || x === String(ders.kod).replace(/^\d+[a-z]/, '');

  function dersKatman(ders: Any) {
    const K = katmanlar();
    const on = `${ders.id}-`;
    const paketKey = [...K.paketler.keys()].find((k) => k.startsWith(on) || k === ders.id);
    const sesli = [...K.sesliKeys].filter((k) => k.startsWith(on)).sort();
    const desteler = K.desteler.filter((x) => x.id.includes(on));
    const onek = onekBul(ders);
    const env = K.envanter.filter((x) => x.onek === onek && kodEs(x.kod, ders));
    return { paketKey, sesli, desteler, env, onek };
  }
  const ozetKatman = (ders: Any) => {
    const k = dersKatman(ders);
    const t = (tur: string) => k.env.filter((x) => x.tur === tur).reduce((a, x) => a + Number(x.madde || 0), 0);
    return {
      paket: !!k.paketKey, sesli: k.sesli.length, deste: k.desteler.length,
      onem: t('onem'), asistan: t('asistan'), cozucu: t('cozucu'),
    };
  };
  const tumDersler = (): Any[] => {
    const out: Any[] = [];
    for (let k = 1; k <= 6; k++) for (const x of oku<Any>(DERSLER(k), {}).dersler || []) out.push(x);
    return out;
  };
  const dersBul = (id: string): Any | undefined => {
    const m = id.match(/^k(\d)-/);
    return m ? (oku<Any>(DERSLER(Number(m[1])), {}).dersler || []).find((x: Any) => x.id === id) : undefined;
  };

  /* ================= Dersler ================= */
  app.get('/api/admin/dersler', d.requireAdmin, (req, res) => {
    const s = listeSorgusu(req, { varsayilanBoyut: 50 });
    const g = gor();
    const satirlar: Any[] = tumDersler().map((x) => ({ ...x, katman: ozetKatman(x), gorunurluk: g[`ders:${x.id}`] || 'acik' }));
    res.json(diziSayfala(satirlar, s, {
      araMetni: (x) => `${x.id} ${x.kod} ${x.konu} ${x.brans} ${x.ogretim_uyesi || ''}`,
      siralayicilar: { id: (x) => x.id, tarih: (x) => x.tarih || '', konu: (x) => katla(x.konu), brans: (x) => katla(x.brans) },
      suzgecler: {
        kurul: (x, v) => String(x.kurul) === v,
        brans: (x, v) => x.brans === v,
        gorunurluk: (x, v) => x.gorunurluk === v,
        katman: (x, v) => (v === 'eksik' ? !x.katman.paket && !x.katman.sesli && !x.katman.deste : v === 'paket' ? x.katman.paket : Number((x.katman as Any)[v]) > 0),
      },
      yuzler: { kurul: (x) => String(x.kurul), brans: (x) => x.brans, gorunurluk: (x) => x.gorunurluk },
      eslestir: (x) => ({ id: x.id, kod: x.kod, kurul: x.kurul, brans: x.brans, konu: x.konu, ogretim_uyesi: x.ogretim_uyesi, tarih: x.tarih, saat: x.saat, katman: x.katman, gorunurluk: x.gorunurluk }),
    }));
  });

  app.get('/api/admin/dersler/:id', d.requireAdmin, (req, res) => {
    const ders = dersBul(String(req.params.id));
    if (!ders) return res.status(404).json({ error: 'Ders bulunamadı' });
    const k = dersKatman(ders);
    const g = gor();
    const p = k.paketKey ? katmanlar().paketler.get(k.paketKey) : null;
    const sesKayit = oku<Any>(path.join(SES, 'kayit.json'), {});
    const sesliSatir = (key: string) => sesliOzet(key, sesKayit);
    const ornekDosya = path.join(SRC, 'ornek_sorular', `k${ders.kurul}`, `${k.paketKey || ders.ders_id_tam || ders.id}.json`);
    const ornek = oku<Any>(ornekDosya, null as any);
    const ornekSayi = ornek ? (ornek.kazanimlar || []).reduce((a: number, z: Any) => a + (z.sorular || []).length, 0) : 0;
    res.json({
      ders,
      brans: bransOf(ders) || null,
      gorunurluk: g[`ders:${ders.id}`] || 'acik',
      katmanlar: {
        paket: p ? { key: p.key, baslik: p.baslik, sayilar: paketSayilari(p), gorunurluk: g[`paket:${p.key}`] || 'acik' } : null,
        sesli: k.sesli.map((key) => ({ ...sesliSatir(key), gorunurluk: g[`sesli:${key}`] || 'acik' })),
        desteler: k.desteler.map((x) => ({ ...x, gorunurluk: g[`deste:${x.id}`] || 'acik' })),
        envanter: k.env.map((x) => ({ ...x, gorunurluk: g[`${x.tur}:${x.dizin}/${x.kod}`] || 'acik' })),
        ornek: ornekSayi ? { dosya: path.relative(SRC, ornekDosya), soru: ornekSayi } : null,
        cikmis: { konular: (ders.cikmis_konular || []).length, paket: p ? (p.cikmis || []).length : 0 },
        quiz: p ? (p.quiz || []).length : 0,
      },
    });
  });

  app.put('/api/admin/dersler/:id', d.requireAdmin, async (req, res) => {
    const id = String(req.params.id);
    const m = id.match(/^k(\d)-\d+$/);
    if (!m) return res.status(400).json({ error: 'Geçersiz ders kimliği' });
    const b = req.body || {};
    try {
      let once: Any = {}, sonra: Any = {};
      await katmanGuncelle<Any>(DERSLER(Number(m[1])), `dersler_k${m[1]}`, (t) => {
        const x = (t.dersler || []).find((y: Any) => y.id === id);
        if (!x) throw new Error('Ders bulunamadı');
        once = { konu: x.konu, ogretim_uyesi: x.ogretim_uyesi, tarih: x.tarih, saat: x.saat, brans: x.brans };
        if ('konu' in b) { const v = kirp(b.konu, 200); if (!v) throw new Error('konu boş olamaz'); x.konu = v; }
        if ('ogretim_uyesi' in b) x.ogretim_uyesi = kirp(b.ogretim_uyesi, 120);
        if ('tarih' in b) { if (b.tarih && !TARIH.test(String(b.tarih))) throw new Error('tarih YYYY-AA-GG olmalı'); x.tarih = String(b.tarih || ''); }
        if ('saat' in b) { if (b.saat && !/^\d{2}:\d{2}-\d{2}:\d{2}$/.test(String(b.saat))) throw new Error('saat SS:DD-SS:DD olmalı'); x.saat = String(b.saat || ''); }
        if ('brans' in b && b.brans !== x.brans) {
          const yeni = branslar().find((y) => y.ad === b.brans);
          if (!yeni) throw new Error('Bilinmeyen branş');
          // Kod kalıcıdır (kural 15): yalnız aynı harfi paylaşan yazıma geçilebilir
          if (yeni.harf !== bransHarf(x.kod)) throw new Error(`Ders kodu ${x.kod} "${yeni.harf}" harfli branşa taşınamaz; kimlik/kod kalıcıdır.`);
          x.brans = yeni.ad;
        }
        sonra = { konu: x.konu, ogretim_uyesi: x.ogretim_uyesi, tarih: x.tarih, saat: x.saat, brans: x.brans };
        return t;
      });
      denetimHedef(res, `ders:${id}`);
      denetimFark(res, once, sonra);
      yayinla('dersler', [id]);
      res.json({ ok: true, kayit: sonra });
    } catch (e: any) {
      res.status(400).json({ error: e?.message || 'kaydedilemedi' });
    }
  });

  /* ================= Sesli ders ================= */
  const SES_KATMAN = ['metin', 'cumle_zaman', 'kelime_zaman', 'isaret', 'cizim', 'terim', 'kisaltma', 'cikmis_konum', 'vurgu', 'v2'] as const;
  function sesliOzet(key: string, kayit: Any) {
    const liste = katmanlar().sesliListe;
    const kd = liste.find((x) => x.key === key);
    const varyant: Any[] = kayit[key] || [];
    const dosya: Record<string, boolean> = {};
    for (const k of SES_KATMAN) dosya[k] = varMi(path.join(SES, k, `${key}.${k === 'metin' ? 'md' : 'json'}`));
    const ses = varyant.find((v) => v.varsayilan) || varyant[varyant.length - 1];
    return {
      key, baslik: kd?.baslik || key, no: kd?.no, sira: kd?.sira, kayitli: !!kd, kurul: Number((key.match(/^k(\d)/) || [])[1]) || null,
      varyant: varyant.length, sureSn: ses?.sureSn || 0, saglayici: ses?.saglayici || '', olusturuldu: ses?.olusturuldu || '',
      dosya, eksik: SES_KATMAN.filter((k) => !dosya[k] && k !== 'v2' && k !== 'vurgu').length + (varyant.length ? 0 : 1),
    };
  }
  app.get('/api/admin/sesli-dersler', d.requireAdmin, (req, res) => {
    const s = listeSorgusu(req);
    const kayit = oku<Any>(path.join(SES, 'kayit.json'), {});
    const g = gor();
    const satirlar: Any[] = [...katmanlar().sesliKeys].map((k) => ({ ...sesliOzet(k, kayit), gorunurluk: g[`sesli:${k}`] || 'acik' }));
    res.json(diziSayfala(satirlar, s, {
      araMetni: (x) => `${x.key} ${x.baslik}`,
      siralayicilar: { key: (x) => x.key, sureSn: (x) => x.sureSn, olusturuldu: (x) => x.olusturuldu || '', eksik: (x) => x.eksik },
      suzgecler: {
        kurul: (x, v) => String(x.kurul) === v,
        durum: (x, v) => (v === 'tam' ? x.eksik === 0 : v === 'eksik' ? x.eksik > 0 : v === 'sessiz' ? !x.varyant : true),
        gorunurluk: (x, v) => x.gorunurluk === v,
      },
      yuzler: { kurul: (x) => String(x.kurul), durum: (x) => [x.eksik === 0 ? 'tam' : 'eksik', ...(x.varyant ? [] : ['sessiz'])], gorunurluk: (x) => x.gorunurluk },
    }));
  });
  app.get('/api/admin/sesli-dersler/:key', d.requireAdmin, (req, res) => {
    const key = String(req.params.key);
    if (!katmanlar().sesliKeys.has(key)) return res.status(404).json({ error: 'Sesli ders bulunamadı' });
    const kayit = oku<Any>(path.join(SES, 'kayit.json'), {});
    const varyantlar = (kayit[key] || []).map(({ zamanlama, klipler, ...v }: Any) => ({ ...v, zamanlamaSayisi: (zamanlama || []).length, klipSayisi: (klipler || []).length }));
    res.json({ ...sesliOzet(key, kayit), varyantlar, gorunurluk: gor()[`sesli:${key}`] || 'acik', ders: dersBul(key.slice(0, key.indexOf('-', 3)) || key) || null });
  });

  /* ================= Önem / asistan / çözücü ================= */
  app.get('/api/admin/spot-cozucu', d.requireAdmin, (req, res) => {
    const s = listeSorgusu(req);
    const g = gor();
    const satirlar: Any[] = katmanlar().envanter.map((x) => ({ ...x, id: `${x.dizin}/${x.kod}`, kurul: (x.onek.match(/^k(\d)/) || [, '1'])[1], gorunurluk: g[`${x.tur}:${x.dizin}/${x.kod}`] || 'acik' }));
    res.json(diziSayfala(satirlar, s, {
      araMetni: (x) => `${x.dizin} ${x.kod} ${x.baslik}`,
      siralayicilar: { kod: (x) => `${x.onek}/${x.kod}`, madde: (x) => Number(x.madde) || 0, baslik: (x) => katla(x.baslik) },
      suzgecler: { tur: (x, v) => x.tur === v, onek: (x, v) => x.onek === v, kurul: (x, v) => x.kurul === v, gorunurluk: (x, v) => x.gorunurluk === v },
      yuzler: { tur: (x) => x.tur, onek: (x) => x.onek, kurul: (x) => x.kurul, gorunurluk: (x) => x.gorunurluk },
    }));
  });

  /* ================= Ders içerik paketleri ================= */
  const paketSayilari = (p: Any) => Object.fromEntries(Object.entries(p).filter(([, v]) => Array.isArray(v)).map(([k, v]) => [k, (v as any[]).length]));
  app.get('/api/admin/ders-icerik', d.requireAdmin, (req, res) => {
    const s = listeSorgusu(req);
    const g = gor();
    const satirlar: Any[] = [...katmanlar().paketler.values()].map((p) => ({ key: p.key, baslik: p.baslik, kurul: (p.key.match(/^k(\d)/) || [])[1] || '', sayilar: paketSayilari(p), gorunurluk: g[`paket:${p.key}`] || 'acik' }));
    res.json(diziSayfala(satirlar, s, {
      araMetni: (x) => `${x.key} ${x.baslik}`,
      siralayicilar: { key: (x) => x.key, quiz: (x) => x.sayilar.quiz || 0, terimler: (x) => x.sayilar.terimler || 0 },
      suzgecler: { kurul: (x, v) => x.kurul === v, gorunurluk: (x, v) => x.gorunurluk === v },
      yuzler: { kurul: (x) => x.kurul, gorunurluk: (x) => x.gorunurluk },
    }));
  });
  app.get('/api/admin/ders-icerik/:key', d.requireAdmin, (req, res) => {
    const p = katmanlar().paketler.get(String(req.params.key));
    if (!p) return res.status(404).json({ error: 'Paket bulunamadı' });
    // Tam paket istemciye gitmez: her bölümden ilk 5 öge örnek
    const ornek = Object.fromEntries(Object.entries(p).map(([k, v]) => [k, Array.isArray(v) ? (v as any[]).slice(0, 5) : v]));
    res.json({ key: p.key, baslik: p.baslik, ozet: p.ozet, sayilar: paketSayilari(p), ornek, gorunurluk: gor()[`paket:${p.key}`] || 'acik' });
  });

  /* ================= Sınav dağılımı ================= */
  app.get('/api/admin/sinav-dagilimi', d.requireAdmin, (_req, res) => res.json(oku<Any>(DAGILIM, {})));
  app.put('/api/admin/sinav-dagilimi/:kurul', d.requireAdmin, async (req, res) => {
    const k = String(req.params.kurul);
    if (!/^[1-6]$/.test(k)) return res.status(400).json({ error: 'kurul 1–6' });
    const b = req.body || {};
    try {
      let once: Any = {}, sonra: Any = {};
      await katmanGuncelle<Any>(DAGILIM, 'sinav_dagilimi', (t) => {
        t.kurullar = t.kurullar || {};
        const x = { ...(t.kurullar[k] || {}) };
        once = JSON.parse(JSON.stringify(x));
        if ('toplam' in b) { const n = Number(b.toplam); if (!Number.isInteger(n) || n < 1 || n > 500) throw new Error('toplam 1–500'); x.toplam = n; }
        if ('hedef' in b) { const n = Number(b.hedef); if (!Number.isInteger(n) || n < 0 || n > 500) throw new Error('hedef 0–500'); x.hedef = n; }
        if ('tahmini' in b) x.tahmini = b.tahmini === true;
        if ('branslar' in b) {
          if (!b.branslar || typeof b.branslar !== 'object' || Array.isArray(b.branslar)) throw new Error('branslar nesne olmalı');
          const y: Record<string, number> = {};
          for (const [a, v] of Object.entries(b.branslar)) { if (!/^[a-z0-9]{2,30}$/.test(a)) throw new Error(`geçersiz branş: ${a}`); const n = Number(v); if (!Number.isInteger(n) || n < 0) throw new Error(`${a}: tam sayı olmalı`); y[a] = n; }
          x.branslar = y;
        }
        t.kurullar[k] = x;
        sonra = x;
        return t;
      });
      denetimHedef(res, `sinav-dagilimi:${k}`);
      denetimFark(res, once, sonra);
      yayinla('sinav_dagilimi', [k]);
      res.json({ ok: true, kayit: sonra });
    } catch (e: any) {
      res.status(400).json({ error: e?.message || 'kaydedilemedi' });
    }
  });

  /* ================= Katalog bağdaştırıcıları ================= */
  type Bagdastirici = {
    etiket: string; kaynak: string; yuzler: { anahtar: string; etiket: string }[];
    yukle: () => Any[]; kimlik: (x: Any) => string; baslik: (x: Any) => string; alt?: (x: Any) => string;
    yuz: (x: Any, k: string) => string | undefined; metin: (x: Any) => string;
    duzenlenebilir?: string[]; kaydet?: (id: string, yama: Any) => Promise<{ once: Any; sonra: Any }>;
  };
  const sozlukBag = (dosya: string, ad: string, etiket: string): Bagdastirici => ({
    etiket, kaynak: `src/data/${ad}.json`,
    yuzler: [{ anahtar: 'category', etiket: 'Tür' }, { anahtar: 'ders', etiket: 'Ders' }],
    yukle: () => Object.entries(oku<Any>(dosya, {})).map(([k, v]) => ({ ...(v as Any), _key: k })),
    kimlik: (x) => x._key, baslik: (x) => x.term || x._key, alt: (x) => kirp(x.definition, 110),
    yuz: (x, k) => (x[k] == null ? undefined : String(x[k])), metin: (x) => `${x._key} ${x.term || ''} ${x.definition || ''}`,
    duzenlenebilir: ['term', 'definition', 'category'],
    kaydet: async (id, yama) => {
      let once: Any = {}, sonra: Any = {};
      await katmanGuncelle<Any>(dosya, ad, (t) => {
        if (!(id in t)) throw new Error('Kayıt bulunamadı');
        once = { ...t[id] };
        for (const a of ['term', 'definition', 'category']) if (a in yama) { const v = kirp(yama[a], 2000); if (a !== 'category' && !v) throw new Error(`${a} boş olamaz`); t[id][a] = v; }
        sonra = { ...t[id] };
        return t;
      });
      return { once, sonra };
    },
  });
  const BAG: Record<string, Bagdastirici> = {
    spot: {
      etiket: 'Sınav spotları', kaynak: 'src/data/exam_spots_k1.json',
      yuzler: [{ anahtar: 'kategori', etiket: 'Kategori' }, { anahtar: 'onem', etiket: 'Önem' }, { anahtar: 'ders', etiket: 'Ders' }],
      yukle: () => {
        const v = oku<Any>(path.join(SRC, 'exam_spots_k1.json'), {});
        const dersAd = new Map((v.dersler || []).map((x: Any) => [x.id, x.baslik]));
        return (v.spotlar || []).map((x: Any) => ({ ...x, _ders: dersAd.get(x.ders_id || x.ders) || x.ders_id || x.ders || '' }));
      },
      kimlik: (x) => x.id, baslik: (x) => x.baslik || kirp(x.spot, 120), alt: (x) => [x._ders, x.kategori, x.onem ? `önem ${x.onem}` : ''].filter(Boolean).join(' · '),
      yuz: (x, k) => (k === 'ders' ? x._ders || undefined : x[k] == null ? undefined : String(x[k])), metin: (x) => `${x.id} ${x.baslik} ${x.spot} ${(x.maddeler || []).join(' ')}`,
    },
    kisaltma: sozlukBag(path.join(SRC, 'kisaltma_sozluk.json'), 'kisaltma_sozluk', 'Kısaltmalar'),
    terim: sozlukBag(path.join(SRC, 'terim_yardimcisi_sozluk.json'), 'terim_yardimcisi_sozluk', 'Terim yardımcısı'),
    saglik: {
      etiket: 'Sağlık Bakanlığı kaynakları', kaynak: 'src/data/saglik/kaynaklar.json',
      yuzler: [{ anahtar: 'kurum', etiket: 'Kurum' }, { anahtar: 'yil', etiket: 'Yıl' }],
      yukle: () => oku<Any>(path.join(SRC, 'saglik', 'kaynaklar.json'), {}).kaynaklar || [],
      kimlik: (x) => x.id, baslik: (x) => x.belge, alt: (x) => [x.kurum, x.yil].filter(Boolean).join(' · '),
      yuz: (x, k) => (x[k] == null ? undefined : String(x[k])), metin: (x) => `${x.id} ${x.belge} ${x.kurum} ${x.not || ''}`,
    },
  };
  // dataCatalogService varlığını aynı arayüze çevirir (tanımlar ve kayıt yolları değişmez)
  const katalogBag = (id: string): Bagdastirici | null => {
    const e = katalogErisimi?.varliklar.find((x: Any) => x.id === id);
    if (!e) return null;
    return {
      etiket: e.label, kaynak: e.source, yuzler: e.facets.map((f: Any) => ({ anahtar: f.key, etiket: f.label })),
      yukle: e.load, kimlik: e.key, baslik: e.title, alt: e.subtitle, yuz: (x, k) => { const v = e.facet(x, k); return Array.isArray(v) ? v[0] : v; }, metin: e.text,
      duzenlenebilir: e.save ? e.editable : [],
      kaydet: e.save ? async (rid, yama) => {
        const once = e.load().find((r: Any) => e.key(r) === rid);
        const onceK = once ? Object.fromEntries(e.editable.map((a: string) => [a, once[a]])) : {};
        const kayit = e.save(rid, yama);
        katalogErisimi?.onChange?.(e.id, [rid]);
        return { once: onceK, sonra: Object.fromEntries(e.editable.map((a: string) => [a, kayit?.[a]])) };
      } : undefined,
    };
  };
  const bagBul = (id: string) => BAG[id] || katalogBag(id);
  const GOR_ONEK: Record<string, string> = { decks: 'deste' };

  app.get('/api/admin/k16/katalog/:varlik/meta', d.requireAdmin, (req, res) => {
    const b = bagBul(String(req.params.varlik));
    if (!b) return res.status(404).json({ error: 'Bilinmeyen veri türü' });
    const rows = b.yukle();
    const yuzler: Record<string, { deger: string; n: number }[]> = {};
    for (const f of b.yuzler) {
      const m = new Map<string, number>();
      for (const x of rows) { const v = b.yuz(x, f.anahtar); if (v) m.set(v, (m.get(v) || 0) + 1); }
      yuzler[f.anahtar] = [...m].map(([deger, n]) => ({ deger, n })).sort((a, c) => c.n - a.n).slice(0, 40);
    }
    res.json({ etiket: b.etiket, kaynak: b.kaynak, toplam: rows.length, suzgecler: b.yuzler, yuzler, duzenlenebilir: b.duzenlenebilir || [] });
  });

  app.get('/api/admin/k16/katalog/:varlik', d.requireAdmin, (req, res) => {
    const id = String(req.params.varlik);
    const b = bagBul(id);
    if (!b) return res.status(404).json({ error: 'Bilinmeyen veri türü' });
    const s = listeSorgusu(req);
    const g = gor();
    const gk = GOR_ONEK[id];
    const ann = katalogErisimi?.annAll()[id] || {};
    const suzgecler: Record<string, (x: Any, v: string) => boolean> = {};
    for (const f of b.yuzler) suzgecler[f.anahtar] = (x, v) => b.yuz(x, f.anahtar) === v;
    if (gk) suzgecler.gorunurluk = (x, v) => (g[`${gk}:${b.kimlik(x)}`] || 'acik') === v;
    res.json(diziSayfala(b.yukle(), s, {
      araMetni: b.metin,
      siralayicilar: { baslik: (x) => katla(b.baslik(x) || '') },
      suzgecler,
      yuzler: Object.fromEntries(b.yuzler.map((f) => [f.anahtar, (x: Any) => b.yuz(x, f.anahtar)])),
      eslestir: (x) => ({ id: b.kimlik(x), baslik: b.baslik(x), alt: b.alt?.(x) || '', degerlendirme: ann[b.kimlik(x)]?.status || '', ...(gk ? { gorunurluk: g[`${gk}:${b.kimlik(x)}`] || 'acik' } : {}) }),
    }));
  });

  app.get('/api/admin/k16/katalog/:varlik/:id', d.requireAdmin, (req, res) => {
    const vid = String(req.params.varlik);
    const b = bagBul(vid);
    if (!b) return res.status(404).json({ error: 'Bilinmeyen veri türü' });
    const x = b.yukle().find((r) => b.kimlik(r) === req.params.id);
    if (!x) return res.status(404).json({ error: 'Kayıt bulunamadı' });
    const kayit = vid === 'decks'
      ? { ...x, slides: undefined, _adimlar: (x.slides || []).length }
      : x;
    const gk = GOR_ONEK[vid];
    res.json({ id: b.kimlik(x), baslik: b.baslik(x), kayit, duzenlenebilir: b.duzenlenebilir || [], ...(gk ? { gorunurlukAnahtari: `${gk}:${b.kimlik(x)}`, gorunurluk: gor()[`${gk}:${b.kimlik(x)}`] || 'acik' } : {}) });
  });

  app.put('/api/admin/k16/katalog/:varlik/:id', d.requireAdmin, async (req, res) => {
    const vid = String(req.params.varlik);
    const b = bagBul(vid);
    if (!b?.kaydet) return res.status(400).json({ error: 'Bu veri türü buradan düzenlenemez (salt okunur).' });
    const yama = Object.fromEntries(Object.entries(req.body?.yama || {}).filter(([k]) => (b.duzenlenebilir || []).includes(k)));
    if (!Object.keys(yama).length) return res.status(400).json({ error: 'Değişen düzenlenebilir alan yok' });
    try {
      const { once, sonra } = await b.kaydet(String(req.params.id), yama);
      denetimHedef(res, `${vid}:${req.params.id}`);
      denetimFark(res, once, sonra);
      if (BAG[vid]) yayinla(vid, [String(req.params.id)]);
      res.json({ ok: true, kayit: sonra, kim: kim(req) });
    } catch (e: any) {
      res.status(400).json({ error: e?.message || 'kaydedilemedi' });
    }
  });
}
