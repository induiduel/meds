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
}

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
    if (!ds.length) return;
    out.set(p.id, {
      p: { ...p, bayt: ds.reduce((a, d) => a + d.b, 0), n: ds.length, surum: ozet(ds.map((d) => `${d.u}@${d.v || ''}`).sort().join('|')) },
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
    const grup = String(d.discipline || 'Diğer').split('/')[0].trim();
    ekle({ id: `ogren:${id}`, modul: 'ogren', grup, baslik: d.shortTitle || d.title, alt: `${d.slideCount} adım${sesler.length ? ' · sesli' : ''}${pdfler.length ? ' · PDF' : ''}`, sira: i },
      [...veri(`decks/items/${safe}.json`), ...sesler, ...pdfler]);
  });

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
  ekle({ id: 'uygulama', modul: 'uygulama', grup: 'Uygulama', baslik: 'Uygulama dosyaları', alt: 'Tüm sayfaların kodu, görünüm ve yazı tipleri', sira: 0, zorunlu: true },
    [...m.kod.filter((f) => !/composer_model/.test(f)).map(parca), ...kucuk.map(parca),
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
