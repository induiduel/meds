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
import { cikmisOrnekMi as kaynakBulunamadi } from './questionQuarantine';
import { registerCanliDersAra } from './canliDersAra';

const KOK = path.join(process.cwd(), 'data', 'sesli_anlatim');
const ARSIV_KOK = path.join(process.cwd(), 'data', 'arsiv_25_26', 'sesli_anlatim');
const GUNLUK_KOK = path.join(process.cwd(), 'data', 'sesli_anlatim', 'gunluk');
const ARSIV_GUNLUK_KOK = path.join(process.cwd(), 'data', 'arsiv_25_26', 'gunluk');
const ARSIV_DECKS_KOK = path.join(process.cwd(), 'data', 'arsiv_25_26', 'decks');
const MEDSPAK_25_26 = fs.existsSync('/home/ubuntu/medsor/meds_database_25_26/medspak')
  ? '/home/ubuntu/medsor/meds_database_25_26/medspak'
  : path.resolve(process.cwd(), '..', 'meds_database_25_26', 'medspak');
const MEDSPAK_EXPORT = path.resolve(process.cwd(), '..', 'meds_export', 'medspak');

const arsivMi = (k: string) => /^y25-k\d+-\d+-[a-z0-9-]+$/.test(k);
const kokSec = (k: string) => (arsivMi(k) ? ARSIV_KOK : KOK);

const P = {
  dersler: path.join(KOK, 'dersler.json'),
  arsivDersler: path.join(ARSIV_KOK, 'dersler.json'),
  kayit: (arsiv = false) => path.join(arsiv ? ARSIV_KOK : KOK, 'kayit.json'),
  metin: (k: string) => path.join(kokSec(k), 'metin', `${k}.md`),
  ses: (k: string, v: string) => path.join(kokSec(k), 'ses', k, `${v}.mp3`),
  hizalama: (k: string) => path.join(kokSec(k), 'hizalama', `${k}.json`),
  vurgu: (k: string) => path.join(kokSec(k), 'vurgu', `${k}.json`),
  cumle: (k: string) => path.join(kokSec(k), 'cumle_zaman', `${k}.json`),
  kelime: (k: string) => path.join(kokSec(k), 'kelime_zaman', `${k}.json`),
  isaret: (k: string) => path.join(kokSec(k), 'isaret', `${k}.json`),
  cizim: (k: string) => path.join(kokSec(k), 'cizim', `${k}.json`),
  v2: (k: string) => path.join(kokSec(k), 'v2', `${k}.json`),
  cikmisKonum: (k: string) => path.join(kokSec(k), 'cikmis_konum', `${k}.json`),
  terim: (k: string) => path.join(kokSec(k), 'terim', `${k}.json`),
  kisaltma: (k: string) => path.join(kokSec(k), 'kisaltma', `${k}.json`),
  ogrenciNot: (fileId: string) => path.join(KOK, 'ogrenci_not', `${fileId.replace(/[^\w-]/g, '')}.json`),
  gunluk: (k: string) => path.join(arsivMi(k) ? ARSIV_GUNLUK_KOK : GUNLUK_KOK, `${k}.json`),
};

interface Ders {
  key: string;
  no: number;
  kurulNo?: number;
  kurul?: number;
  brans?: string;
  hoca?: string;
  donem?: '2025-2026' | '2026-2027';
  desteId?: string;
  sayfaSayisi?: number;
  baslik: string;
  sira: number;
}
interface KayitVaryant {
  id: string;
  saglayici: string;
  ses: string;
  etiket: string;
  sureSn: number;
  bayt: number;
  zamanlama?: [number, number][];
  /** klipli derste paragraf klip özetleri (sesliAnlatim.ts klipKaydet); kelime_zaman.py klip önbelleği için */
  klipler?: string[];
}

const oku = <T,>(p: string, bos: T): T => {
  try {
    return JSON.parse(fs.readFileSync(p, 'utf8'));
  } catch {
    return bos;
  }
};
const anahtarGecerli = (k: unknown): k is string => typeof k === 'string' && /^(?:y25-)?k\d+-\d+-[a-z0-9-]+$/.test(k);
const vidGecerli = (v: unknown): v is string => typeof v === 'string' && /^[a-z0-9-]+$/.test(v);

/*
 * Sınama (test) verisi (kullanıcı kararı 2026-10-27): data/sinama.json'daki kurala uyan dersler gerçek (güncel) derslerle aynı
 * listede gösterilmez; ayrı bölümde ('donem=sinama') ve 'SINAMA — test verisi' etiketiyle sunulur. Betikler listeyi
 * `?sinama=1` ile (güncel + sınama) okur. Kural: { etiket, brans: [...], kurulMin, anahtarlar: [...] }.
 */
type SinamaKonfig = { etiket?: string; brans?: string[]; kurulMin?: number; anahtarlar?: string[] };
const sinamaKonfig = (): SinamaKonfig => oku<SinamaKonfig>(path.join(process.cwd(), 'data', 'sinama.json'), {});
const sinamaEtiketi = (): string => sinamaKonfig().etiket || 'SINAMA — test verisi';
const sinamaMi = (d: Ders): boolean => {
  if (arsivMi(d.key) || d.donem === '2025-2026') return false;
  const c = sinamaKonfig();
  if (c.anahtarlar?.includes(d.key)) return true;
  if (!c.brans?.length) return false;
  const b = bransBilgisi(d);
  return c.brans.includes(b.brans) && b.kurul >= (c.kurulMin ?? 1);
};
const dersler = (donem?: string, sinamaDahil = false): Ders[] => {
  if (donem === '2025-2026') return oku<Ders[]>(P.arsivDersler, []);
  if (donem === 'hepsi') return [...oku<Ders[]>(P.dersler, []), ...oku<Ders[]>(P.arsivDersler, [])];
  const guncel = oku<Ders[]>(P.dersler, []);
  if (donem === 'sinama') return guncel.filter(sinamaMi);
  return sinamaDahil ? guncel : guncel.filter((d) => !sinamaMi(d));
};
const dersBul = (key: string): Ders | undefined =>
  (arsivMi(key) ? oku<Ders[]>(P.arsivDersler, []) : oku<Ders[]>(P.dersler, [])).find((x) => x.key === key);

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
  const kurul = d.kurul || Number(/^(?:y25-)?k(\d+)-/.exec(d.key)?.[1]) || 0;
  if (arsivMi(d.key) && d.brans) {
    return { brans: d.brans, bransNo: d.no, kurul };
  }
  const sp = /^k\d+-\d+-son-prova-([a-z-]+?)(?:-(\d+))?$/.exec(d.key);
  const modul = MODUL_DERS[d.key] || (sp ? [SON_PROVA_BRANS[sp[1]] || slugBrans(sp[1]) || 'Son Prova', `Son Prova${sp[2] ? ` ${sp[2]}` : ''}`] as [string, string] : undefined);
  if (modul) return { brans: modul[0], bransNo: modul[1], kurul };
  // Blok özet (k1-95-blok-ozet-patoloji-1): birkaç dersi tek sesli derste anlatır; liste sayfasında ayrı sekme
  const bo = /^k\d+-\d+-blok-ozet-([a-z-]+?)(?:-(\d+))?(?:-v(\d+))?$/.exec(d.key);
  if (bo) return { brans: SON_PROVA_BRANS[bo[1]] || slugBrans(bo[1]) || 'Blok özet', bransNo: `Blok özet${bo[2] ? ` ${bo[2]}` : ''}${bo[3] ? ` · V${bo[3]}` : ''}`, kurul };
  // Kurul 2+: branş ve branş içi numara YALNIZ ders kayıt defterinden (kod "2n07" → 7). Drive dosya adındaki "33)"
  // numarası çakışabiliyor (Kurul 1: Meme Kanseri ile Memenin Benign ikisi de 33) — KURUL2_YAPILMAYACAK_HATALAR H16.
  const dk = /^(?:y25-)?k([2-6])-(\d{2})/.exec(d.key);
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
  return y ? { brans: y[0], bransNo: y[1], kurul } : { brans: d.brans || 'Diğer', bransNo: d.no, kurul };
}
/** Kayıtlı ve dosyası diskte olan varyantlar (ilki varsayılan). */
function varyantlar(key: string): KayitVaryant[] {
  const k = oku<Record<string, KayitVaryant[]>>(P.kayit(arsivMi(key)), {});
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

function medspakYoluBul(key: string): string | null {
  const m = /^(?:y25-)?k(\d+)-/.exec(key);
  const kurul = m ? Number(m[1]) : 2;
  const adaylar = [
    path.join(MEDSPAK_25_26, `kurul${kurul}`, `${key}.medspak`),
    path.join(MEDSPAK_EXPORT, `kurul${kurul}`, `${key}.medspak`),
    path.join(MEDSPAK_EXPORT, `${key}.medspak`),
  ];
  for (const a of adaylar) {
    if (fs.existsSync(a)) return a;
  }
  return null;
}

/** Paketin boyutu + sürümü (mtime): çevrimdışı merkezi bununla "güncelleme var" kararını verir */
function medspakBilgi(key: string): { medspakBayt?: number; medspakSurum?: string } {
  const y = medspakYoluBul(key);
  if (!y) return {};
  try {
    const st = fs.statSync(y);
    return { medspakBayt: st.size, medspakSurum: `${Math.round(st.mtimeMs)}-${st.size}` };
  } catch { return {}; }
}

export function registerCanliDersRoutes(app: Express) {
  app.get('/api/canli-ders', (req: Request, res: Response) => {
    const donem = String(req.query.donem || '2026-2027');
    const out = dersler(donem, req.query.sinama === '1')
      // Son Prova partları listede kalır (zamanlama betikleri ve çevrimdışı paketler bu listeyi okur); sesli ders ekranı onları süzer
      .filter((d) => !LISTEDE_GIZLI.has(d.key))
      .sort((a, b) => (a.kurul || 1) - (b.kurul || 1) || a.sira - b.sira)
      .map((d) => {
        const vs = varyantlar(d.key);
        if (!vs.length) return null;
        const b = bransBilgisi(d);
        const isArsiv = arsivMi(d.key) || d.donem === '2025-2026';
        const sinama = sinamaMi(d);
        return {
          key: d.key,
          donem: isArsiv ? '2025-2026' : '2026-2027',
          arsiv: isArsiv,
          ...(sinama ? { sinama: true, sinamaEtiket: sinamaEtiketi() } : {}),
          // no: branş içi numara (Tıbbi Patoloji 16); kurulNo: kurul genelindeki sıra
          no: b.bransNo,
          kurulNo: d.kurulNo ?? d.no,
          brans: b.brans,
          hoca: d.hoca,
          parca: b.parca,
          listeNo: b.listeNo,
          kurul: b.kurul,
          baslik: d.baslik,
          sira: d.sira,
          desteId: d.desteId || (isArsiv ? `k${b.kurul}p-${d.key}` : undefined),
          varsayilan: ozet(d.key)(vs[0]),
          varyantlar: vs.map(ozet(d.key)),
          pdf: fs.existsSync(P.hizalama(d.key)),
          gunlukVar: fs.existsSync(P.gunluk(d.key)),
          medspakVar: Boolean(medspakYoluBul(d.key)),
          ...medspakBilgi(d.key),
        };
      })
      .filter(Boolean);
    // Express res.json zayıf ETag üretir ve If-None-Match'te 304 döner.
    res.setHeader('Cache-Control', out.length ? 'public, max-age=30' : 'no-store');
    res.json({ donem, dersler: out });
  });

  app.get('/api/canli-ders/ses/:key/:dosya', (req: Request, res: Response) => {
    const key = req.params.key;
    const vid = String(req.params.dosya || '').replace(/\.mp3$/, '');
    if (!anahtarGecerli(key) || !vidGecerli(vid)) return res.status(400).json({ error: 'geçersiz istek' });
    const v = varyantlar(key).find((x) => x.id === vid);
    if (!v) return res.status(404).json({ error: 'ses yok' });
    const d = dersBul(key);
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

  app.get('/api/canli-ders/:key/gunluk', (req: Request, res: Response) => {
    const key = req.params.key;
    if (!anahtarGecerli(key)) return res.status(400).json({ error: 'geçersiz ders' });
    const d = dersBul(key);
    const g = oku<any>(P.gunluk(key), null);
    if (g) return res.json(g);
    return res.json({
      key,
      donem: arsivMi(key) ? '2025-2026' : '2026-2027',
      kurul: d?.kurul || Number(/^(?:y25-)?k(\d+)-/.exec(key)?.[1]) || 1,
      brans: d?.brans || '',
      baslik: d?.baslik || key,
      kayitlar: [],
    });
  });

  app.get('/api/canli-ders/:key/medspak', (req: Request, res: Response) => {
    const key = req.params.key;
    if (!anahtarGecerli(key)) return res.status(400).json({ error: 'geçersiz ders' });
    const yol = medspakYoluBul(key);
    if (!yol) return res.status(404).json({ error: 'medspak bulunamadı' });
    res.setHeader('Content-Disposition', `attachment; filename="${key}.medspak"`);
    res.sendFile(yol, { headers: { 'Content-Type': 'application/vnd.sqlite3' } });
  });

  // Çıkmış soru → sesli ders konum dizini (tasarım C03 "Derste 04:18"): bütün güncel derslerin cikmis_konum dosyaları
  // birleştirilir; metni değişmiş dersin eşleşmesi alınmaz (metinHash), cümle başlangıcı cumle_zaman'dan (EMA varyantı
  // öncelikli). 10 dk bellekte; dosya yoksa boş dizin. Yanıt: { q: { [soruId]: { k, b, p, c, t? } } }
  let dizinOnbellek: { at: number; q: Record<string, { k: string; b: string; p: number; c: number; t?: number }> } | null = null;
  app.get('/api/canli-ders/cikmis-dizin', (_req: Request, res: Response) => {
    if (!dizinOnbellek || Date.now() - dizinOnbellek.at > 600_000) {
      const q: Record<string, { k: string; b: string; p: number; c: number; t?: number }> = {};
      const klasor = path.join(KOK, 'cikmis_konum');
      let dosyalar: string[] = [];
      try { dosyalar = fs.readdirSync(klasor).filter((f) => f.endsWith('.json')); } catch { /* yok */ }
      for (const f of dosyalar) {
        const key = f.replace(/\.json$/, '');
        try {
          const d = dersBul(key);
          if (!d || !fs.existsSync(P.metin(key))) continue;
          const ck = oku<any>(P.cikmisKonum(key), null);
          if (!ck || !Array.isArray(ck.q) || !ck.q.length) continue;
          const pars = metinParagraflari(fs.readFileSync(P.metin(key), 'utf8'));
          const h = crypto.createHash('sha1').update(pars.map((x) => x.t).join('\n')).digest('hex');
          if (ck.metinHash !== h) continue;
          const cz = oku<any>(P.cumle(key), null);
          const vz = cz && cz.metinHash === h && cz.varyantlar ? (Object.entries(cz.varyantlar).find(([v]) => /ema/i.test(v)) || Object.entries(cz.varyantlar)[0])?.[1] as any : null;
          for (const x of ck.q) {
            const id = String(x?.id || '');
            if (!id || kaynakBulunamadi(id) || (q[id] && (q[id] as any).skor >= (x.skor || 0))) continue;
            const t = vz?.p?.[String(x.p)]?.[x.c];
            q[id] = { k: key, b: d.baslik, p: x.p, c: x.c, ...(Number.isFinite(t) ? { t: Math.floor(t) } : {}), ...({ skor: x.skor || 0 } as any) };
          }
        } catch { /* bozuk dosya atlanır */ }
      }
      for (const v of Object.values(q)) delete (v as any).skor;
      dizinOnbellek = { at: Date.now(), q };
    }
    res.setHeader('Cache-Control', 'public, max-age=600');
    res.json({ q: dizinOnbellek.q });
  });

  // Sesli derste geçen yerler (A05): :key'den önce kayıtlı olmalı
  registerCanliDersAra(app, {
    dersler: () => dersler('2026-2027').filter((d) => !LISTEDE_GIZLI.has(d.key)),
    metinYolu: P.metin, cumleYolu: P.cumle, sesVar: (k) => varyantlar(k).length > 0,
  });

  app.get('/api/canli-ders/:key', (req: Request, res: Response) => {
    const key = req.params.key;
    if (!anahtarGecerli(key)) return res.status(400).json({ error: 'geçersiz ders' });
    const d = dersBul(key);
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
    const isArsiv = arsivMi(key) || d.donem === '2025-2026';
    const desteId = d.desteId || hz?.deckId || (isArsiv ? `k${b.kurul}p-${key}` : `k${b.kurul}p-${key}`);
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
    res.setHeader('Cache-Control', 'public, max-age=30');
    res.json({
      key,
      donem: isArsiv ? '2025-2026' : '2026-2027',
      arsiv: isArsiv,
      ...(sinamaMi(d) ? { sinama: true, sinamaEtiket: sinamaEtiketi() } : {}),
      desteId,
      gunlukVar: fs.existsSync(P.gunluk(key)),
      medspakVar: Boolean(medspakYoluBul(key)),
      no: b.bransNo,
      kurulNo: d.kurulNo ?? d.no,
      brans: b.brans,
      hoca: d.hoca,
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
        ...(Array.isArray(v.klipler) && v.klipler.length === pars.length ? { klipler: v.klipler } : {}),
      })),
      pdf,
      // önemli cümle/terim aralıkları (scripts/sesli_anlatim/vurgu_uret.py): { "<i>": [[bas, son, "c"|"t", onem]] }
      vurgu: oku<any>(P.vurgu(key), null)?.p || null,
      // okunan cümlenin slayttaki satır/kelime/resim kutuları (scripts/sesli_anlatim/pdf_isaret.py); metin değiştiyse gönderilmez
      isaret: (() => {
        const is = oku<any>(P.isaret(key), null);
        if (!is || !pdf) return null;
        const h = crypto.createHash('sha1').update(pars.map((p) => p.t).join('\n')).digest('hex');
        if (is.metinHash !== h) return null;
        // canlı çizim (R6, scripts/cizim/cizim_uret.py): aynı metin sürümünden komutlar cümle işaretine `z` olarak eklenir
        const cz = oku<any>(P.cizim(key), null);
        if (cz?.metinHash !== h || !cz?.p) return is.c;
        const c: Record<string, any[]> = {};
        for (const [pi, cs] of Object.entries<any[]>(is.c || {})) {
          c[pi] = (cs || []).map((x: any, ci: number) => {
            const z = cz.p?.[pi]?.[String(ci)];
            if (!z?.length) return x;
            return { ...(x || { s: z[0].s, t: 'sayfa', l: [], w: [], d: 0 }), z };
          });
        }
        return c;
      })(),
      // Kurul 2+ sesli metin v2 (konusma_v2.py): cümle başına ekran maddesi, düzey, vurgu türleri, çıkmış, slayt adımı.
      // Paragraf, cümle sesleri birleşince metindeki paragrafla aynıysa gönderilir (metin değiştiyse o paragraf yok sayılır).
      v2: (() => {
        const v = oku<any>(P.v2(key), null);
        const vp = Array.isArray(v?.bolumler) ? v.bolumler.flatMap((b: any) => (Array.isArray(b?.paragraflar) ? b.paragraflar : [])) : [];
        if (vp.length !== pars.length) return null;
        const sade = (t: string) => String(t || '').replace(/\s+/g, ' ').trim();
        const out: Record<string, any[]> = {};
        vp.forEach((p: any, i: number) => {
          const cs = Array.isArray(p?.cumleler) ? p.cumleler : [];
          if (!cs.length || sade(cs.map((c: any) => c.ses).join(' ')) !== sade(pars[i].t)) return;
          if (!cs.some((c: any) => (c.ekran && sade(c.ekran) !== sade(c.ses)) || c.vurgu?.length || c.cikmis?.length || c.slayt_adim != null)) return;
          out[String(i)] = cs.map((c: any) => ({
            e: String(c.ekran || ''),
            d: Number(c.duzey) || 0,
            v: (Array.isArray(c.vurgu) ? c.vurgu : []).filter((x: any) => x?.metin && x?.tur).map((x: any) => [String(x.metin), String(x.tur)]),
            c: Array.isArray(c.cikmis) ? c.cikmis.map(String) : [],
            // slayt_adim şemada adım KİMLİĞİ ("k2-07-d-s05", konusma_v2.py) → destenin slideNumber'ı (eski sayı biçimi de kabul)
            a: Number.isFinite(c.slayt_adim) ? c.slayt_adim : (/-s(\d+)$/.exec(String(c.slayt_adim || '')) ? Number(/-s(\d+)$/.exec(String(c.slayt_adim))![1]) : null),
            s: c.spot ?? null,
          }));
        });
        return Object.keys(out).length ? { deste: desteId, p: out } : null;
      })(),
      // çıkmış soru → dayandığı cümle (scripts/sesli_anlatim/cikmis_konum.py); PDF yeri ön yüzde isaret[p][c]'den
      cikmisKonum: (() => {
        const ck = oku<any>(P.cikmisKonum(key), null);
        if (!ck || !Array.isArray(ck.q) || !ck.q.length) return null;
        const h = crypto.createHash('sha1').update(pars.map((p) => p.t).join('\n')).digest('hex');
        // H84: özgün kaynağı bulunamayan (karantinadaki) çıkmış soru listede gösterilmez
        const q = ck.metinHash === h ? ck.q.filter((x: any) => !kaynakBulunamadi(String(x?.id))) : null;
        return q && q.length ? q : null;
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
      // PDF terim yardımcısı (scripts/sesli_anlatim/terim_sozlugu.py): { "<dosya>": { "<sayfa>": { bos, t: [{ t, a, k, f?, b }] } } }
      // PDF'e bağlıdır (metin değişse de geçerli)
      terim: (() => {
        const t = oku<any>(P.terim(key), null);
        return t?.d && Object.keys(t.d).length ? t.d : null;
      })(),
      // PDF kısaltma yardımcısı (scripts/sesli_anlatim/kisaltma_sozlugu.py): ayrı katman, terimlerle aynı kutup yapısı
      // { "<dosya>": { "<sayfa>": { bos, t: [{ t, acilim, a, k: "kisaltma", b }] } } }
      kisaltma: (() => {
        const t = oku<any>(P.kisaltma(key), null);
        return t?.d && Object.keys(t.d).length ? t.d : null;
      })(),
    });
  });
}
