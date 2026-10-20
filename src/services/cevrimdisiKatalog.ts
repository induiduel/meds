/**
 * Çevrimdışı paket kataloğu (istemci: src/services/cevrimdisi/).
 *   GET /api/cevrimdisi/katalog      — tüm paketlerin özeti: kimlik, modül, grup, başlık, bayt, dosya sayısı, sürüm (dosya listesi yok; küçük).
 *   GET /api/cevrimdisi/paket/:id    — tek paketin dosyaları [{u, v, b}] (u: kök göreli adres, v: sürüm, b: bayt).
 * Kaynaklar: dist/cevrimdisi-manifest.json (derleme parçaları; scripts/vite/cevrimdisiManifest.ts), src/data/* (klip adları,
 * sürüm özetleri) ve data/* (ses dosyaları, boyut). Paket sürümü dosya adres+sürümlerinin özeti: içerik ya da ses değişince değişir,
 * istemci "güncelleme var" gösterir ve yalnız değişen dosyaları indirir. Sesli dersler (canlı ders) burada değil; istemci kendi
 * kataloğundan (/api/canli-ders) ekler. Çıkmış/soru havuzu veritabanı IndexedDB'ye ayrıca iner (offlineDatabaseService).
 */
import crypto from 'crypto';
import fs from 'fs';
import path from 'path';
import type { Express, Request, Response } from 'express';
import { resolveDeckPdfs } from './lecturePdfLocator';

export interface PDosya { u: string; v?: string; b: number }
export interface Paket {
  id: string;
  modul: string;
  grup: string;
  baslik: string;
  alt?: string;
  sira: number;
  bayt: number;
  n: number;
  surum: string;
  /** Uygulama paketi gibi çevrimdışı modda her zaman cihazda tutulanlar */
  zorunlu?: boolean;
  /** İsteğe bağlı ağır parçalar (istemci "sesleri / PDF'leri de indir" seçimine göre atlar): bayt + dosya sayısı */
  ek?: { ses?: { b: number; n: number }; pdf?: { b: number; n: number } };
  /** Bu paket indirilince birlikte inmesi gereken paketler (ör. TBG kampı → sesli dersi); istemci kuyruğa kendisi ekler */
  bagimli?: string[];
  /** Tür başına sürüm: sessiz indirilen paket yalnız ses değişince "güncelleme var" göstermesin */
  surumT?: { veri: string; ses?: string; pdf?: string };
}

/** Dosya türü (istemci paketMotoru.dosyaTuru ile aynı kural) */
export const dosyaTuru = (u: string): 'ses' | 'pdf' | 'veri' =>
  /\.mp3($|\?)/i.test(u) || /^\/api\/(cozucu-ses|patoloji-asistan\/ses|patoloji-cozucu\/ses|patoloji-cozucu-alt\/ses|ogren-ses|kamp\/ses)\//.test(u) ? 'ses'
    : u.startsWith('/api/lecture-pdf/') || u.startsWith('/vendor/pdfjs/') ? 'pdf' : 'veri';

/** PDF.js'in çizim için istediği yardımcı dosyalar (yazı tipi, wasm, renk profili); server.ts /vendor/pdfjs'ten sunar */
const PDFJS_YARDIMCI = [
  ...['FoxitDingbats.pfb', 'FoxitFixed.pfb', 'FoxitFixedBold.pfb', 'FoxitFixedBoldItalic.pfb', 'FoxitFixedItalic.pfb', 'FoxitSerif.pfb',
    'FoxitSerifBold.pfb', 'FoxitSerifBoldItalic.pfb', 'FoxitSerifItalic.pfb', 'FoxitSymbol.pfb', 'LiberationSans-Bold.ttf',
    'LiberationSans-BoldItalic.ttf', 'LiberationSans-Italic.ttf', 'LiberationSans-Regular.ttf'].map((f) => `standard_fonts/${f}`),
  'wasm/openjpeg.wasm', 'wasm/openjpeg_nowasm_fallback.js', 'wasm/qcms_bg.wasm', 'iccs/CGATS001Compat-v2-micro.icc',
];

const KOK = process.cwd();
const DIST = path.join(KOK, 'dist');
const SRC_DATA = path.join(KOK, 'src', 'data');
const DATA = path.join(KOK, 'data');

const BRANS: Record<string, string> = {
  patoloji: 'Patoloji', enfeksiyon: 'Enfeksiyon', uroloji: 'Üroloji', genetik: 'Genetik',
  halksagligi: 'Halk Sağlığı', kadindogum: 'Kadın Doğum', farmakoloji: 'Farmakoloji',
};
const ASISTAN_ONEK: Record<string, string> = { e: 'enfeksiyon', u: 'uroloji', g: 'genetik', h: 'halksagligi', k: 'kadindogum', f: 'farmakoloji' };

const jsonOku = (p: string): any => {
  try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch { return null; }
};
const boyut = (p: string) => {
  try { return fs.statSync(p).size; } catch { return 0; }
};
const ozet = (s: string) => crypto.createHash('sha1').update(s).digest('hex').slice(0, 12);

interface Manifest { olusturma: string; kod: string[]; veri: Record<string, string[]> }

let onbellek: { anahtar: string; paketler: Map<string, { p: Paket; dosyalar: PDosya[] }> } | null = null;

function kur(): Map<string, { p: Paket; dosyalar: PDosya[] }> {
  const mYol = path.join(DIST, 'cevrimdisi-manifest.json');
  let anahtar = '';
  try { anahtar = String(fs.statSync(mYol).mtimeMs); } catch { /* derleme yok */ }
  // Ses/veri klasörleri değişince de yeniden kurulsun: 5 dk'lık zaman dilimi anahtara katılır
  anahtar += `|${Math.floor(Date.now() / 300_000)}`;
  if (onbellek && onbellek.anahtar === anahtar) return onbellek.paketler;

  const m: Manifest = jsonOku(mYol) || { olusturma: '', kod: [], veri: {} };
  const out = new Map<string, { p: Paket; dosyalar: PDosya[] }>();
  const kullanilan = new Set<string>();
  const parca = (u: string): PDosya => ({ u: `/${u}`, b: boyut(path.join(DIST, u)) });
  /** src/data altındaki JSON'un derleme parçaları */
  const veri = (rel: string): PDosya[] => {
    const fs_ = m.veri[`src/data/${rel}`];
    if (!fs_) return [];
    fs_.forEach((f) => kullanilan.add(f));
    return fs_.map(parca);
  };
  const ekle = (p: Omit<Paket, 'bayt' | 'n' | 'surum'>, dosyalar: PDosya[]) => {
    const tekil = new Map<string, PDosya>();
    for (const d of dosyalar) if (d.b > 0 || d.u.startsWith('/api/')) tekil.set(d.u, d);
    const ds = [...tekil.values()];
    if (!ds.length && !p.bagimli?.length) return;
    const tur: Record<'ses' | 'pdf' | 'veri', PDosya[]> = { ses: [], pdf: [], veri: [] };
    for (const d of ds) tur[dosyaTuru(d.u)].push(d);
    const sur = (xs: PDosya[]) => ozet(xs.map((d) => `${d.u}@${d.v || ''}`).sort().join('|'));
    const ek: Paket['ek'] = {};
    const surumT: NonNullable<Paket['surumT']> = { veri: sur(tur.veri) };
    for (const t of ['ses', 'pdf'] as const) {
      if (!tur[t].length || p.modul === 'uygulama') continue;
      ek[t] = { b: tur[t].reduce((a, d) => a + d.b, 0), n: tur[t].length };
      surumT[t] = sur(tur[t]);
    }
    out.set(p.id, {
      p: { ...p, bayt: ds.reduce((a, d) => a + d.b, 0), n: ds.length, surum: sur(ds), ...(Object.keys(ek).length ? { ek, surumT } : {}) },
      dosyalar: ds,
    });
  };
  const ses = (u: string, dosya: string, v?: string): PDosya => ({ u, v, b: boyut(dosya) });

  for (const [b, bAd] of Object.entries(BRANS)) {
    // Soru çözücü: set başına (ders JSON + dizin + Öğren eşlemesi + klipler + ortak klipler)
    const cDizin = jsonOku(path.join(SRC_DATA, `${b}_cozucu`, 'index.json'));
    if (cDizin?.dersler) {
      const ortak = Object.entries<any>(cDizin.ortak || {}).map(([k, x]) =>
        ses(`/api/cozucu-ses/${b}/ema/ortak/${k}.mp3`, path.join(DATA, `${b}_cozucu`, 'ses', 'ortak', `${k}.mp3`), x.v));
      cDizin.dersler.forEach((d: any, i: number) => {
        const ders = jsonOku(path.join(SRC_DATA, `${b}_cozucu`, `${d.kod}.json`));
        if (!ders) return;
        const klasor = ders.klasor || d.kod;
        const klipler = Object.entries<any>(ders.klip || {}).map(([k, x]) =>
          ses(`/api/cozucu-ses/${b}/ema/${klasor}/${k}.mp3`, path.join(DATA, `${b}_cozucu`, 'ses', klasor, `${k}.mp3`), x.v));
        const set = d.setSay > 1 ? ` · Set ${d.set}/${d.setSay}` : '';
        ekle({ id: `cozucu:${b}:${d.kod}`, modul: 'cozucu', grup: bAd, baslik: `Ders ${d.no} · ${d.baslik}`, alt: `${d.soru} soru${set}`, sira: i },
          [...veri(`${b}_cozucu/${d.kod}.json`), ...veri(`${b}_cozucu/index.json`), ...veri(`cozucu_ogren/${b}.json`), ...klipler, ...ortak]);
      });
    }
    // En önemliler + sesli sınav asistanı: ders başına
    const oDizin = jsonOku(path.join(SRC_DATA, `${b}_onem`, 'index.json'));
    if (oDizin?.dersler) {
      oDizin.dersler.forEach((d: any, i: number) => {
        const asistan = jsonOku(path.join(SRC_DATA, `${b}_asistan`, `${d.kod}.json`));
        const aBrans = ASISTAN_ONEK[d.kod[0]] || 'patoloji';
        const klipler = Object.entries<any>(asistan?.klip || {}).map(([k, x]) =>
          ses(`/api/patoloji-asistan/ses/${d.kod}/${k}.mp3`, path.join(DATA, `${aBrans}_asistan`, 'ses', d.kod, `${k}.mp3`), x.v));
        ekle({ id: `onem:${b}:${d.kod}`, modul: 'onem', grup: bAd, baslik: `Ders ${d.no} · ${d.baslik}`, alt: `${d.madde} madde${asistan ? ' · sesli asistan' : ''}`, sira: i },
          [...veri(`${b}_onem/${d.kod}.json`), ...veri(`${b}_onem/index.json`), ...veri(`${b}_asistan/${d.kod}.json`), ...veri(`${b}_asistan/index.json`),
            ...veri(`cozucu_ogren/${b}.json`), ...klipler]);
      });
    }
  }

  // Alternatif çözücü (patoloji)
  const aDizin = jsonOku(path.join(SRC_DATA, 'patoloji_cozucu_alt', 'index.json'));
  (aDizin?.dersler || []).forEach((d: any, i: number) => {
    const ders = jsonOku(path.join(SRC_DATA, 'patoloji_cozucu_alt', `${d.kod}.json`));
    const klipler = (ders?.sorular || []).filter((s: any) => s.mp3).map((s: any) =>
      ses(`/api/patoloji-cozucu-alt/ses/${d.kod}/${s.mp3}`, path.join(DATA, 'patoloji_cozucu_alt', 'ses', d.kod, s.mp3), s.h));
    ekle({ id: `alt:${d.kod}`, modul: 'alt', grup: 'Patoloji', baslik: `Ders ${d.no} · ${d.baslik}`, alt: `${d.soru} soru`, sira: i },
      [...veri(`patoloji_cozucu_alt/${d.kod}.json`), ...veri('patoloji_cozucu_alt/index.json'), ...klipler]);
  });

  // Etkileşimli dersler: deste + EMA sesleri + ders PDF'leri
  const katalog: any[] = jsonOku(path.join(SRC_DATA, 'decks', 'catalog.json')) || [];
  katalog.forEach((d: any, i: number) => {
    const id = d.id;
    const safe = String(id).replace(/[^a-zA-Z0-9_-]+/g, '_');
    const kayit = jsonOku(path.join(DATA, 'ogren_ses', id, 'kayit.json')) || {};
    const sesler = Object.keys(kayit).filter((k) => /^\d+$/.test(k)).map((k) =>
      ses(`/api/ogren-ses/${encodeURIComponent(id)}/${k}.mp3`, path.join(DATA, 'ogren_ses', id, `${k}.mp3`), kayit[k]?.h));
    let pdfler: PDosya[] = [];
    try {
      pdfler = resolveDeckPdfs(id).map((f, j) => (f.full ? { u: `/api/lecture-pdf/deck/${encodeURIComponent(id)}/${j}?v=${f.size || 0}`, b: f.size } : null))
        .filter(Boolean) as PDosya[];
    } catch { /* eşleme yok */ }
    if (pdfler.length) {
      // Görüntüleyici önce eşlemeyi (dosya listesi + slayt→sayfa) ve PDF'li deste listesini ister; PDF.js yardımcıları da gerekir
      const nm = process.env.MEDS_NODE_MODULES || path.join(KOK, 'node_modules');
      pdfler.push({ u: `/api/lecture-pdf/deck/${encodeURIComponent(id)}`, b: 4_000 }, { u: '/api/lecture-pdf/decks', b: 60_000 },
        ...PDFJS_YARDIMCI.map((f) => ({ u: `/vendor/pdfjs/${f}`, b: boyut(path.join(nm, 'pdfjs-dist', f)) })));
    }
    const grup = String(d.discipline || 'Diğer').split('/')[0].trim();
    ekle({ id: `ogren:${id}`, modul: 'ogren', grup, baslik: d.shortTitle || d.title, alt: `${d.slideCount} adım${sesler.length ? ' · sesli' : ''}${pdfler.length ? ' · PDF' : ''}`, sira: i },
      [...veri(`decks/items/${safe}.json`), ...sesler, ...pdfler]);
  });

  // Kurul kampları: kurul × branş (kamp JSON parçası + EMA klipleri; data/kamp/ses/k<N>/<brans>/)
  for (const k of Object.keys(m.veri).filter((x) => /^src\/data\/kamp\/k\d+\/[a-z0-9]+\.json$/.test(x)).sort()) {
    const [, kurul, brans] = k.match(/kamp\/k(\d+)\/([a-z0-9]+)\.json$/)!;
    const kamp = jsonOku(path.join(KOK, k));
    const klipler = Object.values<string>(kamp?.ses || {}).filter((d) => /^[a-z0-9-]{1,60}\.mp3$/.test(d)).map((d) =>
      ses(`/api/kamp/ses/${kurul}/${brans}/${d}`, path.join(DATA, 'kamp', 'ses', `k${kurul}`, brans, d)));
    ekle({ id: `kamp:${kurul}:${brans}`, modul: 'veri', grup: 'Kurul kampı', baslik: `Kurul ${kurul} · ${kamp?.baslik || brans}`,
      alt: `${(kamp?.anlatim || []).length} anlatım · ${(kamp?.deneme || []).length} deneme sorusu`, sira: Number(kurul) },
    [...veri(k.slice('src/data/'.length)), ...klipler]);
  }
  // TBG sınav kampı (/genetik-check-up): kalıp tabloları uygulama kodunda; Ders 7 sesli asistanı (g07) klipleri burada,
  // anlatımın kendisi sesli ders (k1-70) olarak bağımlı paketle iner
  const g07 = jsonOku(path.join(SRC_DATA, 'genetik_asistan', 'g07.json'));
  if (g07) {
    ekle({ id: 'sayfa:tbg-kampi', modul: 'veri', grup: 'Kurul kampı', baslik: 'TBG Sınav Kampı', alt: 'Sesli ders, soru çözerek anlatım, kalıp kartları', sira: 0,
      bagimli: ['sesli:k1-70-tbg-sinav-kampi'] },
    Object.entries<any>(g07.klip || {}).map(([k, x]) => ses(`/api/patoloji-asistan/ses/g07/${k}.mp3`, path.join(DATA, 'genetik_asistan', 'ses', 'g07', `${k}.mp3`), x.v)));
  }
  // Son Prova (/son-prova): part başına veri (dizin + branş soruları) + aşama/check-up sorularının EMA klipleri; sesli özetin
  // kendisi (ses + kırpılmış PDF) bağımlı sesli ders paketiyle iner. Kurul başına genel check-up + deneme paketi (deneme sessiz).
  for (const k of Object.keys(m.veri).filter((x) => /^src\/data\/son_prova\/k\d+\/index\.json$/.test(x)).sort()) {
    const kurul = Number(k.match(/k(\d+)\/index/)![1]);
    const ix = jsonOku(path.join(KOK, k));
    if (!ix?.dersler) continue;
    const klipler = (refs: string[]) => refs.flatMap((ref) => {
      const [brans, kalan] = ref.split('/');
      const no = kalan.split('#')[1];
      const q = jsonOku(path.join(SRC_DATA, 'son_prova', `k${kurul}`, 'sorular', `${brans}.json`))?.[ref];
      if (!q?.klip || !q.kl) return [];
      return Object.entries<string>(q.klip).map(([t, v]) => {
        const ad = t.startsWith('s') && t.length === 2 ? `s-${no}-${t[1]}` : `${t}-${no}`;
        return ses(`/api/cozucu-ses/${brans}/ema/${q.kl}/${ad}.mp3`, path.join(DATA, `${brans}_cozucu`, 'ses', q.kl, `${ad}.mp3`), v);
      });
    });
    const dVeri = (b?: string) => [...veri(`son_prova/k${kurul}/index.json`), ...(b ? veri(`son_prova/k${kurul}/sorular/${b}.json`) : [])];
    let sira = 0;
    for (const d of ix.dersler) {
      for (const p of d.partlar) {
        const refs = p.asamalar.flatMap((a: any) => [...a.sorular, ...a.checkup]);
        ekle({ id: `sonprova:${p.key}`, modul: 'veri', grup: `Son Prova · Kurul ${kurul}`, baslik: `${d.ad}${d.partlar.length > 1 ? ` · Part ${p.no}` : ''}`,
          alt: `${p.asamalar.length} aşama · ${refs.length} soru · sesli özet ${p.tahminiDk} dk`, sira: sira++, bagimli: [`sesli:${p.key}`] },
        [...dVeri(d.brans), ...klipler(refs)]);
      }
    }
    ekle({ id: `sonprova:k${kurul}:deneme`, modul: 'veri', grup: `Son Prova · Kurul ${kurul}`, baslik: 'Genel check-up ve denemeler',
      alt: `${ix.denemeler.length} deneme · ${ix.dersler.length} dersin genel check-up'ı`, sira: 99 },
    [...dVeri(), ...ix.dersler.flatMap((d: any) => [...veri(`son_prova/k${kurul}/sorular/${d.brans}.json`), ...klipler(d.genel)])]);
  }
  // Olası sorular: yayımlanmış kurul setleri (data/olasi_sorular/k<N>.json) + özet listesi
  const olasi = [1, 2, 3, 4, 5, 6].filter((k) => boyut(path.join(DATA, 'olasi_sorular', `k${k}.json`)) > 0);
  if (olasi.length) {
    ekle({ id: 'veri:olasi', modul: 'veri', grup: 'Başvuru', baslik: 'Olası sorular', alt: `Kurul ${olasi.join(', ')} olası soru setleri`, sira: 0 },
      [{ u: '/api/olasi-sorular', b: 2_000 }, ...olasi.map((k) => ({ u: `/api/olasi-sorular/${k}`, b: boyut(path.join(DATA, 'olasi_sorular', `k${k}.json`)) }))]);
  }

  // Başvuru verileri (tek paket halinde)
  const grupVeri = (id: string, baslik: string, alt: string, onekler: RegExp) => {
    const ks = Object.keys(m.veri).filter((k) => onekler.test(k));
    ekle({ id, modul: 'veri', grup: 'Başvuru', baslik, alt, sira: 0 }, ks.flatMap((k) => veri(k.slice('src/data/'.length))));
  };
  grupVeri('veri:sozluk', 'Sözlük, hastalıklar ve kavramlar', 'Sözlük, hastalık kartları, tıp ansiklopedisi',
    /^src\/data\/(diseases|disease_lessons|medical_encyclopedia|medicalConcepts5000)\.json$/);
  grupVeri('veri:ozet', 'Ders özetleri', 'Tüm kurulların ders özetleri', /^src\/data\/(summaries\/|summaries_meta\.json)/);
  grupVeri('veri:spot', 'Sınav spotları ve ezber kartları', 'Spot listesi, kazanım eşlemesi, kartlar',
    /^src\/data\/(exam_spots_k1(_kazanim)?\.json|decks\/flashcards\.json|kazanimlar\/byDeck\.json)$/);
  grupVeri('veri:kazanim', 'Kazanım soruları', 'Sınav çalışmasındaki kazanım soru bankası', /^src\/data\/kazanimlar\/(questions|lite)\//);
  grupVeri('veri:sinav', 'Sınav çalışması', 'Kurul 1 kazanım başına çalışma soruları', /^src\/data\/sinav_calisma\//);
  grupVeri('veri:ornek', 'Örnek sorular', 'Kurul 1 kazanım temelli örnek sorular', /^src\/data\/ornek_sorular\//);
  grupVeri('veri:saglik', 'Sağlık Bakanlığı', 'Resmî veriler ve ders bağlantıları', /^src\/data\/saglik\//);
  ekle({ id: 'veri:notlar', modul: 'veri', grup: 'Başvuru', baslik: 'Ders notları', alt: 'Amfi ders notlarının metinleri', sira: 0 },
    [{ u: '/api/lecture-notes', b: 2_100_000 }]);

  // Uygulama: tüm kod + paketlere girmeyen küçük ortak veri parçaları (yazım yardımcısı modeli hariç; çevrimiçi özellik)
  const kalanVeri = new Set<string>();
  for (const [k, fs_] of Object.entries(m.veri)) {
    if (/composer_model/.test(k)) continue;
    fs_.forEach((f) => { if (!kullanilan.has(f)) kalanVeri.add(f); });
  }
  // Paketlenmemiş kalan büyük veri dosyaları (≥1 MB) uygulama paketini şişirmesin: ayrı "diğer" paketi
  const kucuk: string[] = [];
  const buyuk: string[] = [];
  for (const f of kalanVeri) (boyut(path.join(DIST, f)) >= 1_000_000 ? buyuk : kucuk).push(f);
  // Dizinler (branş/ders listeleri, Öğren eşlemeleri): liste ekranları (spotlar, çözücü, sınav çalışması, istatistik) tüm
  // branşlarınkini birlikte yükler; yalnız bir branşın paketi inmiş cihazda da internetsiz açılsınlar diye uygulamaya girer (~0,3 MB)
  const dizinler = Object.entries(m.veri).filter(([k]) => /^src\/data\/[^/]+\/(k\d+\/)?index\.json$|^src\/data\/cozucu_ogren\//.test(k)).flatMap(([, fs_]) => fs_);
  // Uygulama simgeleri ve PWA tanımı (her sayfa ister; internetsiz kurulu uygulamada simge/başlık eksik kalmasın)
  const simgeler = ['/manifest.json', '/favicon.ico', '/favicon.png', '/favicon.svg', '/apple-touch-icon.png', '/ses/sessiz.mp3',
    ...['icon-144x144.png', 'icon-192x192.png', 'icon-512x512.png', 'maskable-icon-192x192.png', 'maskable-icon-512x512.png'].map((f) => `/icons/${f}`)]
    .map((u) => ({ u, b: boyut(path.join(DIST, u)) }));
  // Sesli dersin motivasyon/mola klipleri (public/ses/motivasyon, ~3 MB): sesli ders internetsiz de konuşur
  try {
    for (const f of fs.readdirSync(path.join(DIST, 'ses', 'motivasyon')).filter((x) => x.endsWith('.mp3'))) {
      simgeler.push({ u: `/ses/motivasyon/${f}`, b: boyut(path.join(DIST, 'ses', 'motivasyon', f)) });
    }
  } catch { /* klasör yok */ }
  // Google yazı tipleri: CSS adresi index.html'den; içindeki woff2 dosyalarını istemci indirir (CSS tarayıcıya göre değişir)
  let html = '';
  try { html = fs.readFileSync(path.join(DIST, 'index.html'), 'utf8'); } catch { /* derleme yok */ }
  const yaziTipi = [...new Set(html.match(/https:\/\/fonts\.googleapis\.com\/css2\?[^"'\s]+/g) || [])].map((u) => ({ u: u.replace(/&amp;/g, '&'), b: 250_000 }));
  ekle({ id: 'uygulama', modul: 'uygulama', grup: 'Uygulama', baslik: 'Uygulama dosyaları', alt: 'Tüm sayfaların kodu, görünüm ve yazı tipleri', sira: 0, zorunlu: true },
    [...m.kod.filter((f) => !/composer_model/.test(f)).map(parca), ...kucuk.map(parca), ...dizinler.map(parca), ...simgeler, ...yaziTipi,
      { u: '/index.html', b: boyut(path.join(DIST, 'index.html')), v: m.olusturma }]);
  if (buyuk.length) ekle({ id: 'veri:diger', modul: 'veri', grup: 'Başvuru', baslik: 'Diğer içerik', alt: 'Kalan büyük veri dosyaları', sira: 9 }, buyuk.map(parca));

  onbellek = { anahtar, paketler: out };
  return out;
}

export function registerCevrimdisiKatalogRoutes(app: Express) {
  app.get('/api/cevrimdisi/katalog', (_req: Request, res: Response) => {
    try {
      const ps = kur();
      const paketler = [...ps.values()].map((x) => x.p);
      res.setHeader('Cache-Control', 'no-cache');
      res.json({ surum: ozet(paketler.map((p) => `${p.id}@${p.surum}`).join('|')), olusturma: new Date().toISOString(), paketler });
    } catch (e: any) {
      res.status(500).json({ error: e?.message || 'katalog kurulamadı' });
    }
  });
  app.get('/api/cevrimdisi/paket/:id', (req: Request, res: Response) => {
    const x = kur().get(String(req.params.id));
    if (!x) return res.status(404).json({ error: 'paket yok' });
    res.setHeader('Cache-Control', 'no-cache');
    res.json({ ...x.p, dosyalar: x.dosyalar });
  });
}
