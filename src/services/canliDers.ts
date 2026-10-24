// Canlı ders (/canliders): herkese açık, yalnız okuma uçları.
//   GET /api/canli-ders                     — sesi olan dersler (sıra ile)
//   GET /api/canli-ders/:key                — bölüm/paragraf metni + varyantlar (zamanlama) + PDF hizalaması
//   GET /api/canli-ders/ses/:key/:vid.mp3   — MP3 (Range/206; ?indir=1 → ek olarak indir)
// Veri: data/sesli_anlatim/ (sesliAnlatim.ts) + hizalama/<key>.json (scripts/sesli_anlatim/pdf_hizala.py).
import type { Express, Request, Response } from 'express';
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { metinParagraflari } from './sesliAnlatim';

const KOK = path.join(process.cwd(), 'data', 'sesli_anlatim');
const P = {
  dersler: path.join(KOK, 'dersler.json'),
  kayit: path.join(KOK, 'kayit.json'),
  metin: (k: string) => path.join(KOK, 'metin', `${k}.md`),
  ses: (k: string, v: string) => path.join(KOK, 'ses', k, `${v}.mp3`),
  hizalama: (k: string) => path.join(KOK, 'hizalama', `${k}.json`),
  vurgu: (k: string) => path.join(KOK, 'vurgu', `${k}.json`),
  cumle: (k: string) => path.join(KOK, 'cumle_zaman', `${k}.json`),
  kelime: (k: string) => path.join(KOK, 'kelime_zaman', `${k}.json`),
  isaret: (k: string) => path.join(KOK, 'isaret', `${k}.json`),
  cikmisKonum: (k: string) => path.join(KOK, 'cikmis_konum', `${k}.json`),
  ogrenciNot: (fileId: string) => path.join(KOK, 'ogrenci_not', `${fileId.replace(/[^\w-]/g, '')}.json`),
};

interface Ders { key: string; no: number; baslik: string; sira: number }
interface KayitVaryant {
  id: string;
  saglayici: string;
  ses: string;
  etiket: string;
  sureSn: number;
  bayt: number;
  zamanlama?: [number, number][];
}

const oku = <T,>(p: string, bos: T): T => {
  try {
    return JSON.parse(fs.readFileSync(p, 'utf8'));
  } catch {
    return bos;
  }
};
const anahtarGecerli = (k: unknown): k is string => typeof k === 'string' && /^k\d+-\d+-[a-z0-9-]+$/.test(k);
const vidGecerli = (v: unknown): v is string => typeof v === 'string' && /^[a-z0-9-]+$/.test(v);

const dersler = () => oku<Ders[]>(P.dersler, []);

/*
 * Ders (branş) ve branş içi numara. Kaynak: dersin slayt PDF'inin Drive yolu (hizalama › dosyalar[0].path,
 * "Kurul 1/Tıbbi Patoloji/16)Tümör ….pdf" → Tıbbi Patoloji 16) — yeni dersler kendiliğinden yerine düşer.
 * BRANS_DUZELT: Drive numarası çakışan/hatalı ya da başka dersin PDF'ine hizalı dersler (her zaman).
 * BRANS_YEDEK: hizalaması (PDF'i) henüz olmayan dersler; Drive numaraları Oracle hizalamasıyla aynı.
 */
const BRANS_DUZELT: Record<string, [string, number, number?, number?]> = {
  // Drive: Böbrek ve Mesane ikisi de "26)", İnvaziv Serviks "39)" — patoloji önem listesiyle aynı numara
  'k1-46-mesane-hastaliklari-ve-tumorleri': ['Tıbbi Patoloji', 27],
  'k1-49-invaziv-serviks-kanseri-ve-endometriyozis': ['Tıbbi Patoloji', 29],
  // Drive: Meme Kanseri de "33)" (Memenin Benign ile çakışır). Numara = soru çözücü/önem/asistan numarası (34 Erkek
  // Genital, 35 Meme Kanseri; eşleşme numarayla yapılır). 4. öge listeNo: sesli ders listesi anlatım sırasıyla gitsin
  // (Meme önce). Kapı: scripts/sesli_anlatim/cozucu_eslesme_dogrula.py
  'k1-65-meme-kanseri-ve-molekuler-tipleri': ['Tıbbi Patoloji', 35, undefined, 34.5],
  'k1-66-erkek-genital-sistem-ve-prostat-hastaliklari': ['Tıbbi Patoloji', 34],
};
/** Listede gösterilmeyen dersler (adresle açılmaya devam eder). Uterus Düz Kas ve Trofoblastik: ayrı slaytı yok,
 *  30. PDF s.76–91 (Endometrial dersinin sonu) + 32. PDF s.35–64 (Gebelik Hastalıkları) tekrarı — kullanıcı kararı. */
const LISTEDE_GIZLI = new Set(['k1-54-uterus-duz-kas-ve-trofoblastik-tumorleri']);
const BRANS_YEDEK: Record<string, [string, number]> = {
  'k1-06-gebelik-ve-emzirme-doneminde-beslenme': ['Halk Sağlığı', 7],
  'k1-63-turkiye-de-saglik-hizmetleri': ['Halk Sağlığı', 6],
  'k1-47-bagisikligi-baskili-hastalarda-enfeksiyon': ['Enfeksiyon Hastalıkları', 11],
  'k1-57-intrauterin-enfeksiyonlar': ['Enfeksiyon Hastalıkları', 9],
  'k1-64-gebelik-terminolojisi-ve-kavramlari': ['Kadın Hastalıkları ve Doğum', 2],
  'k1-65-meme-kanseri-ve-molekuler-tipleri': ['Tıbbi Patoloji', 35],
  'k1-66-erkek-genital-sistem-ve-prostat-hastaliklari': ['Tıbbi Patoloji', 34],
};
const bransOnbellek = new Map<string, { mtime: number; v: { brans: string; bransNo: number } | null }>();
/** Modül dersleri (birden çok dersin özeti): branş içi numara yerine etiket. TBG Sınav Kampı → "Genetik · Sınav kampı". */
/** Son Prova partları (k<N>-8x-son-prova-<brans>[-<part>]): "Patoloji · Son Prova 2" */
const SON_PROVA_BRANS: Record<string, string> = {
  patoloji: 'Tıbbi Patoloji', enfeksiyon: 'Enfeksiyon Hastalıkları', genetik: 'Tıbbi Genetik', uroloji: 'Üroloji',
  'halk-sagligi': 'Halk Sağlığı', 'kadin-dogum': 'Kadın Hastalıkları ve Doğum', farmakoloji: 'Tıbbi Farmakoloji',
};
/** Kurul 2+ Son Prova anahtarları branş slug'ını branslar.json'dan taşır (otomasyon/son_prova_zinciri.py: k2-81-son-prova-noroloji) */
const slugBrans = (slug: string): string | undefined =>
  oku<{ branslar?: { slug: string; ad: string }[] }>(path.join(process.cwd(), 'src', 'data', 'dersler', 'branslar.json'), {}).branslar?.find((b) => b.slug === slug)?.ad;
const MODUL_DERS: Record<string, [string, string]> = { 'k1-70-tbg-sinav-kampi': ['Tıbbi Genetik', 'Sınav kampı'] };
function bransBilgisi(d: Ders): { brans: string; bransNo: number | string; kurul: number; parca?: number; listeNo?: number } {
  const kurul = Number(/^k(\d+)-/.exec(d.key)?.[1]) || 0;
  const sp = /^k\d+-\d+-son-prova-([a-z-]+?)(?:-(\d+))?$/.exec(d.key);
  const modul = MODUL_DERS[d.key] || (sp ? [SON_PROVA_BRANS[sp[1]] || slugBrans(sp[1]) || 'Son Prova', `Son Prova${sp[2] ? ` ${sp[2]}` : ''}`] as [string, string] : undefined);
  if (modul) return { brans: modul[0], bransNo: modul[1], kurul };
  // Blok özet (k1-95-blok-ozet-patoloji-1): birkaç dersi tek sesli derste anlatır; liste sayfasında ayrı sekme
  const bo = /^k\d+-\d+-blok-ozet-([a-z-]+?)(?:-(\d+))?(?:-v(\d+))?$/.exec(d.key);
  if (bo) return { brans: SON_PROVA_BRANS[bo[1]] || slugBrans(bo[1]) || 'Blok özet', bransNo: `Blok özet${bo[2] ? ` ${bo[2]}` : ''}${bo[3] ? ` · V${bo[3]}` : ''}`, kurul };
  // Kurul 2+: branş ve branş içi numara YALNIZ ders kayıt defterinden (kod "2n07" → 7). Drive dosya adındaki "33)"
  // numarası çakışabiliyor (Kurul 1: Meme Kanseri ile Memenin Benign ikisi de 33) — KURUL2_YAPILMAYACAK_HATALAR H16.
  const dk = /^k([2-6])-(\d{2})/.exec(d.key);
  if (dk) {
    const kd = oku<{ dersler?: { id: string; kod: string; brans: string }[] }>(path.join(process.cwd(), 'src', 'data', 'dersler', `k${dk[1]}.json`), {});
    const r = kd.dersler?.find((x) => x.id === `k${dk[1]}-${dk[2]}`);
    const no = Number(/(\d+)$/.exec(r?.kod || '')?.[1]);
    if (r && no) return { brans: r.brans, bransNo: no, kurul };
  }
  const elle = BRANS_DUZELT[d.key];
  if (elle) return { brans: elle[0], bransNo: elle[1], kurul, ...(elle[2] ? { parca: elle[2] } : {}), ...(elle[3] ? { listeNo: elle[3] } : {}) };
  const p = P.hizalama(d.key);
  let mtime = -1;
  try { mtime = fs.statSync(p).mtimeMs; } catch { /* PDF yok */ }
  let o = bransOnbellek.get(d.key);
  if (!o || o.mtime !== mtime) {
    const yol = String(oku<any>(p, null)?.dosyalar?.[0]?.path || '');
    const m = /^Kurul \d+\/([^/]+)\/\s*(\d+)\s*\)/.exec(yol);
    o = { mtime, v: m ? { brans: m[1].normalize('NFC').trim(), bransNo: Number(m[2]) } : null };
    bransOnbellek.set(d.key, o);
  }
  if (o.v) return { ...o.v, kurul };
  const y = BRANS_YEDEK[d.key];
  return y ? { brans: y[0], bransNo: y[1], kurul } : { brans: 'Diğer', bransNo: d.no, kurul };
}
/** Kayıtlı ve dosyası diskte olan varyantlar (ilki varsayılan). */
function varyantlar(key: string): KayitVaryant[] {
  const k = oku<Record<string, KayitVaryant[]>>(P.kayit, {});
  return (k[key] || []).filter((v) => vidGecerli(v.id) && fs.existsSync(P.ses(key, v.id)));
}
/** surum: dosyanın değiştirilme zamanı — ses onarılınca/yeniden üretilince adres değişsin (aynı bayt boyutu olsa bile). */
const surum = (key: string, vid: string) => {
  try {
    return Math.round(fs.statSync(P.ses(key, vid)).mtimeMs);
  } catch {
    return 0;
  }
};
const ozet = (key: string) => (v: KayitVaryant) => ({ id: v.id, etiket: v.etiket, saglayici: v.saglayici, ses: v.ses, sureSn: v.sureSn, bayt: v.bayt, surum: surum(key, v.id) });

export function registerCanliDersRoutes(app: Express) {
  app.get('/api/canli-ders', (_req: Request, res: Response) => {
    const out = dersler()
      // Son Prova partları listede kalır (zamanlama betikleri ve çevrimdışı paketler bu listeyi okur); sesli ders ekranı onları süzer
      .filter((d) => !LISTEDE_GIZLI.has(d.key))
      .sort((a, b) => a.sira - b.sira)
      .map((d) => {
        const vs = varyantlar(d.key);
        if (!vs.length) return null;
        const b = bransBilgisi(d);
        return {
          key: d.key,
          // no: branş içi numara (Tıbbi Patoloji 16); kurulNo: kurul genelindeki sıra
          no: b.bransNo,
          kurulNo: d.no,
          brans: b.brans,
          parca: b.parca,
          listeNo: b.listeNo,
          kurul: b.kurul,
          baslik: d.baslik,
          sira: d.sira,
          varsayilan: ozet(d.key)(vs[0]),
          varyantlar: vs.map(ozet(d.key)),
          pdf: fs.existsSync(P.hizalama(d.key)),
        };
      })
      .filter(Boolean);
    // Express res.json zayıf ETag üretir ve If-None-Match'te 304 döner.
    res.setHeader('Cache-Control', out.length ? 'public, max-age=60' : 'no-store');
    res.json({ dersler: out });
  });

  app.get('/api/canli-ders/ses/:key/:dosya', (req: Request, res: Response) => {
    const key = req.params.key;
    const vid = String(req.params.dosya || '').replace(/\.mp3$/, '');
    if (!anahtarGecerli(key) || !vidGecerli(vid)) return res.status(400).json({ error: 'geçersiz istek' });
    const v = varyantlar(key).find((x) => x.id === vid);
    if (!v) return res.status(404).json({ error: 'ses yok' });
    const d = dersler().find((x) => x.key === key);
    if (req.query.indir) {
      const b = d ? bransBilgisi(d) : null;
      const ad = `${b ? `${b.brans} ${String(b.bransNo).padStart(2, '0')}${b.parca ? ` Part ${b.parca}` : ''}` : ''} - ${d?.baslik || key} - ${v.etiket || vid}.mp3`.replace(/[\\/:*?"<>|\u0000-\u001f]/g, '-');
      const ascii = ad
        .replace(/[ğĞüÜşŞıİöÖçÇ·]/g, (c) => ({ ğ: 'g', Ğ: 'G', ü: 'u', Ü: 'U', ş: 's', Ş: 'S', ı: 'i', İ: 'I', ö: 'o', Ö: 'O', ç: 'c', Ç: 'C', '·': '-' })[c]!)
        .normalize('NFKD')
        .replace(/[^\x20-\x7e]/g, '')
        .replace(/["\\]/g, '');
      const utf8 = encodeURIComponent(ad).replace(/['()*]/g, (c) => `%${c.charCodeAt(0).toString(16).toUpperCase()}`);
      res.setHeader('Content-Disposition', `attachment; filename="${ascii}"; filename*=UTF-8''${utf8}`);
    }
    // sendFile: Range → 206/416, ETag/Last-Modified, Accept-Ranges
    res.sendFile(P.ses(key, vid), {
      headers: { 'Content-Type': 'audio/mpeg', 'Cache-Control': 'public, max-age=86400' },
      cacheControl: false,
      dotfiles: 'deny',
    }, (err: any) => {
      if (err && !res.headersSent) res.status(err.status || 500).end();
    });
  });

  app.get('/api/canli-ders/:key', (req: Request, res: Response) => {
    const key = req.params.key;
    if (!anahtarGecerli(key)) return res.status(400).json({ error: 'geçersiz ders' });
    const d = dersler().find((x) => x.key === key);
    if (!d || !fs.existsSync(P.metin(key))) return res.status(404).json({ error: 'ders yok' });
    const vs = varyantlar(key);
    if (!vs.length) return res.status(404).json({ error: 'bu dersin sesi henüz yok' });
    const pars = metinParagraflari(fs.readFileSync(P.metin(key), 'utf8'));
    const bolumler: { baslik: string; paragraflar: { i: number; metin: string }[] }[] = [];
    pars.forEach((p, i) => {
      if (p.bolumBasi || !bolumler.length) bolumler.push({ baslik: p.bolumBaslik, paragraflar: [] });
      bolumler[bolumler.length - 1].paragraflar.push({ i, metin: p.t });
    });
    const hz = oku<any>(P.hizalama(key), null);
    const pdf = hz && Array.isArray(hz.paragraflar) && hz.paragraflar.length === pars.length
      ? { deckId: hz.deckId, dosyalar: hz.dosyalar, paragraflar: hz.paragraflar, ...(Array.isArray(hz.sayfaKaynak) ? { sayfaKaynak: hz.sayfaKaynak } : {}) }
      : null;
    const b = bransBilgisi(d);
    // Cümle başlangıçları (scripts/sesli_anlatim/cumle_zaman.py): yalnız metin ve ses dosyası ölçüldüğü hâliyle duruyorsa
    const cz = oku<any>(P.cumle(key), null);
    const czHash = crypto.createHash('sha1').update(pars.map((p) => p.t).join('\n')).digest('hex');
    const czGecerli = cz && cz.metinHash === czHash;
    const cumleZaman = (vid: string) => {
      const e = czGecerli ? cz.varyantlar?.[vid] : null;
      if (!e || !e.p) return null;
      try { return fs.statSync(P.ses(key, vid)).size === e.bayt ? e.p : null; } catch { return null; }
    };
    // Kelime başlangıçları (scripts/sesli_anlatim/kelime_zaman.py): aynı koşul — metin ve ses dosyası ölçüldüğü hâliyle
    const kz = oku<any>(P.kelime(key), null);
    const kzGecerli = kz && czHash === kz.metinHash;
    const kelimeZaman = (vid: string) => {
      const e = kzGecerli ? kz.varyantlar?.[vid] : null;
      if (!e || !e.p) return null;
      try { return fs.statSync(P.ses(key, vid)).size === e.bayt ? e.p : null; } catch { return null; }
    };
    res.setHeader('Cache-Control', 'public, max-age=60');
    res.json({
      key,
      no: b.bransNo,
      kurulNo: d.no,
      brans: b.brans,
      parca: b.parca,
      kurul: b.kurul,
      sira: d.sira,
      baslik: d.baslik,
      bolumler,
      varyantlar: vs.map((v) => ({
        ...ozet(key)(v),
        zamanlama: Array.isArray(v.zamanlama) && v.zamanlama.length === pars.length ? v.zamanlama : null,
        cumleZaman: Array.isArray(v.zamanlama) && v.zamanlama.length === pars.length ? cumleZaman(v.id) : null,
        // cümle başına sesteki konuşma parçaları [a1,b1,a2,b2…] (duraklamalar çıkarılmış): kelime kelime takip
        cumleKonusma: Array.isArray(v.zamanlama) && v.zamanlama.length === pars.length && cumleZaman(v.id) ? cz.varyantlar[v.id].k || null : null,
        kelimeZaman: Array.isArray(v.zamanlama) && v.zamanlama.length === pars.length ? kelimeZaman(v.id) : null,
      })),
      pdf,
      // önemli cümle/terim aralıkları (scripts/sesli_anlatim/vurgu_uret.py): { "<i>": [[bas, son, "c"|"t", onem]] }
      vurgu: oku<any>(P.vurgu(key), null)?.p || null,
      // okunan cümlenin slayttaki satır/kelime/resim kutuları (scripts/sesli_anlatim/pdf_isaret.py); metin değiştiyse gönderilmez
      isaret: (() => {
        const is = oku<any>(P.isaret(key), null);
        if (!is || !pdf) return null;
        const h = crypto.createHash('sha1').update(pars.map((p) => p.t).join('\n')).digest('hex');
        return is.metinHash === h ? is.c : null;
      })(),
      // çıkmış soru → dayandığı cümle (scripts/sesli_anlatim/cikmis_konum.py); PDF yeri ön yüzde isaret[p][c]'den
      cikmisKonum: (() => {
        const ck = oku<any>(P.cikmisKonum(key), null);
        if (!ck || !Array.isArray(ck.q) || !ck.q.length) return null;
        const h = crypto.createHash('sha1').update(pars.map((p) => p.t).join('\n')).digest('hex');
        return ck.metinHash === h ? ck.q : null;
      })(),
      // öğrenci notunda işaretli (önemli) yerler, PDF dosyası başına (scripts/sesli_anlatim/ogrenci_not_isaret.py):
      // { "<dosya i>": { "<sayfa>": { l: [[x0,y0,x1,y1]], y: [x,y] } } } — kırmızı marker + sayfa başına bir yıldız
      ogrenciNot: (() => {
        if (!pdf || !Array.isArray(pdf.dosyalar)) return null;
        const out: Record<string, any> = {};
        pdf.dosyalar.forEach((f: any, i: number) => {
          const n = f?.fileId ? oku<any>(P.ogrenciNot(String(f.fileId)), null) : null;
          if (n?.s && Object.keys(n.s).length) out[String(i)] = n.s;
        });
        return Object.keys(out).length ? out : null;
      })(),
    });
  });
}
