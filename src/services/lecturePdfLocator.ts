/**
 * Ders PDF'lerini diskte bulur (Öğren ekranındaki PDF görüntüleyici ve "PDF'te aç" için). Server-only.
 *
 * Dosyalar iki yerde olabilir: `MEDS_DATABASE_DIR/ders_notlari_pdf` (düz klasör) ve Drive'dan inen
 * ham kaynaklar `MEDS_DOWNLOADS_DIR/drive_root/**` (kurul/ders alt klasörleri). Ad karşılaştırması Unicode NFC +
 * Türkçe küçük harf ile yapılır (Drive'dan gelen NFD adlar da eşleşir). Dizin taraması 10 dk önbelleklenir.
 *
 * Deste → PDF eşlemesi `src/data/deckPdfSources.json` dosyasındadır (`scripts/build_deck_pdf_sources.py` üretir;
 * drive_root'a göre göreli yol, içerikle doğrulanmış). Dosyada olmayan desteye PDF gösterilmez (tahmin yok).
 */
import fs from 'fs';
import path from 'path';

const CACHE_MS = 10 * 60 * 1000;

interface PdfIndex {
  at: number;
  /** ad anahtarı → tam yol (ilk bulunan) */
  byName: Map<string, string>;
  /** drive_root'a göre NFC göreli yol → tam yol */
  byRel: Map<string, string>;
  /** drive_root altındaki ders PDF'leri */
  driveFiles: { rel: string; full: string }[];
}
let cache: PdfIndex | null = null;

const norm = (s: string) => s.normalize('NFC').toLocaleLowerCase('tr-TR').replace(/\.pdf$/i, '').replace(/\s+/g, ' ').trim();

/** Türkçe karakterleri katlar: "Glomerüler" → "glomeruler". */
const fold = (s: string) =>
  s
    .normalize('NFC')
    .replace(/İ/g, 'i')
    .replace(/I/g, 'ı')
    .toLowerCase()
    .replace(/ı/g, 'i')
    .normalize('NFKD')
    .replace(/[̀-ͯ]/g, '');

/** Numara öneki, boşluk ve noktalama farklarını yok sayan ad anahtarı ("1) Patolojiye Giriş" = "1)Patolojiye Giriş"). */
const nameKey = (s: string) =>
  fold(path.basename(s))
    .replace(/\.pdf$/, '')
    .replace(/^\s*\d+\s*\)\s*/, '')
    .replace(/_?20\d\d$/, '')
    .replace(/[^a-z0-9]+/g, '');

function dirs() {
  const db = process.env.MEDS_DATABASE_DIR || path.resolve(process.cwd(), '..', 'meds_database');
  const dl = process.env.MEDS_DOWNLOADS_DIR || path.resolve(process.cwd(), '..', 'meds_downloads');
  return { notes: path.join(db, 'ders_notlari_pdf'), drive: path.join(dl, 'drive_root'), downloads: dl };
}

function walk(dir: string, visit: (full: string, name: string) => void, depth = 0) {
  if (depth > 6) return;
  let entries: fs.Dirent[];
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true });
  } catch {
    return;
  }
  for (const e of entries) {
    const full = path.join(dir, e.name);
    if (e.isDirectory()) walk(full, visit, depth + 1);
    else if (e.isFile() && /\.pdf$/i.test(e.name)) visit(full, e.name);
  }
}

function index(): PdfIndex {
  if (cache && Date.now() - cache.at < CACHE_MS) return cache;
  const { notes, drive, downloads } = dirs();
  const byName = new Map<string, string>();
  const byRel = new Map<string, string>();
  const driveFiles: PdfIndex['driveFiles'] = [];
  const addName = (full: string, name: string) => {
    const k = norm(name);
    if (!byName.has(k)) byName.set(k, full);
  };
  walk(notes, addName);
  walk(drive, (full, name) => {
    addName(full, name);
    const rel = path.relative(drive, full).normalize('NFC');
    byRel.set(rel, full);
    driveFiles.push({ rel, full });
  });
  walk(downloads, addName); // çıkmış soru PDF'leri vb. (yalnız ada göre)
  cache = { at: Date.now(), byName, byRel, driveFiles };
  return cache;
}

/** Dosya adına göre PDF'in tam yolunu döner; bulunamazsa null. */
export function findLecturePdf(requestedName: string): string | null {
  const target = norm(path.basename(String(requestedName || '')));
  if (!target) return null;
  const files = index().byName;
  const exact = files.get(target);
  if (exact && fs.existsSync(exact)) return exact;
  // Numara öneki ("1)") ya da küçük ad farkları: içerme eşleşmesi, en kısa fark kazanır.
  let best: { p: string; diff: number } | null = null;
  for (const [key, p] of files) {
    if (key.includes(target) || target.includes(key)) {
      const diff = Math.abs(key.length - target.length);
      if (!best || diff < best.diff) best = { p, diff };
    }
  }
  return best && fs.existsSync(best.p) ? best.p : null;
}

/* ------------------------------------------------------------------ deste → PDF */

interface SourceFile {
  path: string;
  name: string;
  fileId?: string;
  pages?: number;
}
export interface DeckSourceEntry {
  title: string;
  files: SourceFile[];
  /** slaytNo → [başlangıç, bitiş, dosyaIndeksi?] */
  slides?: Record<string, number[]>;
  /** PDF yoksa: ders programındaki tarih */
  missing?: { tarih?: string };
}
interface SourcesFile {
  generatedAt?: string;
  decks: Record<string, DeckSourceEntry>;
}
const sourceCache = new Map<string, { mtime: number; data: SourcesFile }>();

/**
 * Eşleme dosyası: derlemeyle gelen `src/data/deckPdfSources.json` ve Oracle'da ders işçisinin her Drive taramasından
 * sonra yazdığı `MEDS_DOWNLOADS_DIR/_deck_pdf_sources.json`; `generatedAt`'i yeni olan kullanılır.
 */
function deckSources(): SourcesFile {
  const { downloads } = dirs();
  const candidates = [path.join(downloads, '_deck_pdf_sources.json'), path.resolve(process.cwd(), 'src', 'data', 'deckPdfSources.json')];
  let best: SourcesFile | null = null;
  for (const p of candidates) {
    try {
      const m = fs.statSync(p).mtimeMs;
      let c = sourceCache.get(p);
      if (!c || c.mtime !== m) {
        c = { mtime: m, data: JSON.parse(fs.readFileSync(p, 'utf8')) };
        sourceCache.set(p, c);
      }
      if (!best || String(c.data.generatedAt || '') > String(best.generatedAt || '')) best = c.data;
    } catch {
      /* dosya yok / yarım yazılmış */
    }
  }
  return best || { decks: {} };
}

/**
 * Sanal desteler: birden çok dersin PDF'lerini tek destede birleştirir (sıra = dosya indeksi). TBG Sınav Kampı sesli dersi
 * altı genetik dersinin slaytlarını tek görüntüleyicide açar (data/sesli_anlatim/hizalama/k1-70-tbg-sinav-kampi.json).
 */
export const SANAL_DESTELER: Record<string, { title: string; decks: string[]; files?: SourceFile[] }> = {
  // Sesli ders V2 (2026-10-23): Öğren destesi k1p-k1-65 eski birleşik PDF'e (33) Memenin Benign) bağlı; sınav odaklı sesli
  // özet asıl ders PDF'iyle anlatıldı ve hizalandı.
  'k1p-k1-65-meme-kanseri-ve-molekuler-tipleri-sesli-v2': {
    title: 'Meme Kanseri ve Moleküler Tipleri',
    decks: [],
    files: [{ path: 'Kurul 1/Tıbbi Patoloji/35) Meme Kanseri ve Moleküler Tipleri.pdf', name: '35) Meme Kanseri ve Moleküler Tipleri.pdf', pages: 67, fileId: '1xtoC_Gck7KgK4YCeRMCSQqVZ8vB9Wl2g' } as SourceFile],
  },
  // 2026-27 Kurul 2 (2026-10-27): işçisiz, elle üretilen sesli ders; Öğren destesi henüz yok, bu yılın okul PDF'i doğrudan bağlı.
  'k2p-k2-01-norolojik-hastaya-yaklasim': {
    title: 'Nörolojik Hastaya Yaklaşım',
    decks: [],
    files: [{ path: 'Kurul 2/Nöroloji/1)Nörolojik hastaya yaklaşım.pdf', name: '1)Nörolojik hastaya yaklaşım.pdf', pages: 9, fileId: '1W9hP005FeexiyGBlCyKGRGcIKKg9W-jm' } as SourceFile],
  },
  // 2026-11-03 Beyin ve Sinir Cerrahisi: derse Zeynep hoca girdi, sınav asıl hoca Sinan Apaydın'ın slaytlarından; bağlı PDF onun
  // Drive klasöründen (1c8b1CPiZaNx2ZlxxdHWITUw15dNIT0jx). Spinal travmalar 2026-11-03'te k2-12'den ayrı derse (k2-64) bölündü.
  'k2p-k2-12-kafa-ve-omurilik-yaralanmalari': {
    title: 'Kafa ve Omurilik Yaralanmaları',
    decks: [],
    files: [{ path: 'Kurul 2/Beyin ve Sinir Cerrahisi/1)Kafa ve Omurilik Yaralanmaları.pdf', name: '1)Kafa ve Omurilik Yaralanmaları.pdf', pages: 76, fileId: '1ran23mdEnl_4p9CxbiYQwLustck52Agk' } as SourceFile],
  },
  'k2p-k2-13-medulla-spinalis-lezyonlari': {
    title: 'Medulla Spinalis Lezyonları: Omurga Tümörleri',
    decks: [],
    files: [{ path: 'Kurul 2/Beyin ve Sinir Cerrahisi/2)Omurga Tümörleri.pdf', name: '2)Omurga Tümörleri.pdf', pages: 20, fileId: '1KagKsjrTCiYoy7JE7qOfSJYMKMv7ntqk' } as SourceFile],
  },
  'k2p-k2-14-intrakraniyal-kitlelerde-belirti-ve-bulgular': {
    title: 'İntrakraniyal Kitlelerde Belirti ve Bulgular',
    decks: [],
    files: [{ path: 'Kurul 2/Beyin ve Sinir Cerrahisi/3)Beyin Tümörleri.pdf', name: '3)Beyin Tümörleri.pdf', pages: 68, fileId: '1NoH24LBMQUz4IZjglxCXgHo5PT6XeujF' } as SourceFile],
  },
  'k2p-k2-64-spinal-travmalar': {
    title: 'Spinal Travmalar',
    decks: [],
    files: [{ path: 'Kurul 2/Beyin ve Sinir Cerrahisi/4)Spinal Travmalar.pdf', name: '4)Spinal Travmalar.pdf', pages: 57, fileId: '1qOQ4DYspVXBXoyxahYyNzsfvwWT4LDgf' } as SourceFile],
  },
  // 2026-11-04 Kurul 2, 3. parti (Öğren askıda, destesiz): okul PDF'i doğrudan bağlı. k2-07'nin bu yılki PDF'i okul Drive'ında henüz
  // yok (kullanıcı yerelden paylaştı) → fileId yok; eski 2023-24 dersi (k2p-k2-07-genel-anestezik-ilaclar, SINAMA) arşivde kalır.
  'k2p-k2-07-genel-anestezik-ilaclarin-farmakolojisi': {
    title: 'Genel Anestezik İlaçların Farmakolojisi',
    decks: [],
    files: [{ path: 'Kurul 2/Tıbbi Farmakoloji /2)Genel Anestezik İlaçların Farmakolojisi.pdf', name: '2)Genel Anestezik İlaçların Farmakolojisi.pdf', pages: 60 } as SourceFile],
  },
  'k2p-k2-15-sizofrenik-bozukluklar': {
    title: 'Şizofreni ve Diğer Psikotik Bozukluklar',
    decks: [],
    files: [{ path: 'Kurul 2/Psikiyatri /2)Şizofreni ve Diğer Psikotik Bozukluklar.pdf', name: '2)Şizofreni ve Diğer Psikotik Bozukluklar.pdf', pages: 49, fileId: '12rnNztA96t0UgWWLiLRvKp52XCw3FDKz' } as SourceFile],
  },
  'k2p-k2-16-norolojik-rehabilitasyona-giris-ve-genel-ilkeler': {
    title: 'Nörolojik Rehabilitasyona Giriş ve Genel İlkeler',
    decks: [],
    files: [{ path: 'Kurul 2/FTR/1)Nörolojik rehabilitasyona giriş ve genel ilkeler.pdf', name: '1)Nörolojik rehabilitasyona giriş ve genel ilkeler.pdf', pages: 43, fileId: '1lj1IYdYpYjhq602-179jVlQ3vh6DpDDh' } as SourceFile],
  },
  // 2026-11-06 Kurul 2, 5. parti (Öğren askıda, destesiz): okul PDF'i doğrudan bağlı.
  'k2p-k2-19-bipolar-bozukluk': {
    title: 'Bipolar Duygudurum Bozukluğu',
    decks: [],
    files: [{ path: 'Kurul 2/Psikiyatri /3)Bipolar Duygudurum Boz..pdf', name: '3)Bipolar Duygudurum Boz..pdf', pages: 44, fileId: '1HIwUJUNM8We6Ca3ktASvsQLJu_WQ29AH' } as SourceFile],
  },
  'k2p-k2-20-psikiyatrik-bozukluklarda-uygulanan-tedaviler': {
    title: 'Psikiyatrik Bozukluklarda Uygulanan Tedaviler',
    decks: [],
    files: [{ path: 'Kurul 2/Psikiyatri /6)Psikiyatride Tedaviler.pdf', name: '6)Psikiyatride Tedaviler.pdf', pages: 32, fileId: '1i-HGVkF67IhZQzntDD4Ebbnm-DUIbJm2' } as SourceFile],
  },
  'k2p-k2-21-sedatif-ve-hipnotik-ilaclar': {
    title: 'Sedatif ve Hipnotik İlaçlar',
    decks: [],
    files: [{ path: 'Kurul 2/Tıbbi Farmakoloji /3)Sedatif ve Hipnotik İlaçlar.pdf', name: '3)Sedatif ve Hipnotik İlaçlar.pdf', pages: 55, fileId: '19yvtKOAtgBQpWEdbSIKaPBtEeSq4MoF4' } as SourceFile],
  },
  // 2026-11-06 H?: k2-17/k2-18 sesli dersleri kayıtsızdı → görüntüleyici "Drive'da aç" yedeğine düşüyordu.
  'k2p-k2-17-periferik-noropati': {
    title: 'Periferik Nöropati',
    decks: [],
    files: [{ path: 'Kurul 2/Nöroloji/5)POLİNÖROPATİLER.pdf', name: '5)POLİNÖROPATİLER.pdf', pages: 23, fileId: '1lrl3iqDXRocQPW3oesoWzLePPhMfclsQ' } as SourceFile],
  },
  'k2p-k2-18-bazal-gangliyonlar-ve-ekstrapiramidal-sistem': {
    title: 'Bazal Gangliyonlar ve Ekstrapiramidal Sistem',
    decks: [],
    files: [{ path: 'Kurul 2/Nöroloji/6)Bazal Ganglionlar.pdf', name: '6)Bazal Ganglionlar.pdf', pages: 20, fileId: '1-O48d9vY81Z--Kx3COklUtyn4kRwNTC5' } as SourceFile],
  },
  'k2p-k2-37-okb-ve-iliskili-bozukluklar': {
    title: 'OKB ve İlişkili Diğer Bozukluklar',
    decks: [],
    files: [{ path: 'Kurul 2/Psikiyatri /4)OKB.pdf', name: '4)OKB.pdf', pages: 23, fileId: '1Naxqd5sF5saLsUVpq6HvT6LME3Daq2MV' } as SourceFile],
  },
  // 2026-11-09 6. parti (k2-22, k2-23, k2-24, k2-58): deste yok, PDF sanal desteyle bağlanır.
  'k2p-k2-22-psikosomatik-bozukluklar': {
    title: 'Psikosomatik Bozukluklar',
    decks: [],
    files: [{ path: 'Kurul 2/Psikiyatri /7)Psikosomatik Hastalıklar.pdf', name: '7)Psikosomatik Hastalıklar.pdf', pages: 51, fileId: '1aHOgFatMfF77svtBsLRuZKMMXbEt5kk1' } as SourceFile],
  },
  'k2p-k2-23-cinsel-kimlik-bozukluklari': {
    title: 'Cinsel Kimlik ve İşlev Bozuklukları',
    decks: [],
    files: [{ path: 'Kurul 2/Psikiyatri /8)Cinsel Kimlik ve İşlev Bozuklukları.pdf', name: '8)Cinsel Kimlik ve İşlev Bozuklukları.pdf', pages: 44, fileId: '1gK3h7HLvGvuHNjBc6VmC6p_701rEl52X' } as SourceFile],
  },
  'k2p-k2-24-epilepsi': {
    title: 'Epilepsi',
    decks: [],
    files: [{ path: 'Kurul 2/Nöroloji/7)Epilepsi.pdf', name: '7)Epilepsi.pdf', pages: 51, fileId: '1hM273583cLORxhcCSW8ySEEH66tOkws_' } as SourceFile],
  },
  'k2p-k2-58-alkoller': {
    title: 'Alkoller',
    decks: [],
    files: [{ path: 'Kurul 2/Tıbbi Farmakoloji /4)Alkoller.pdf', name: '4)Alkoller.pdf', pages: 53, fileId: '1MZQ1Xlesc_NQbQJZFwYtKbDsf7d16_LQ' } as SourceFile],
  },
  // 2026-11-10 7. parti (k2-26, k2-27): deste yok.
  'k2p-k2-26-norolojik-hastaliklar': {
    title: 'Nörolojik Hastalıklar ve Genetiği',
    decks: [],
    files: [{ path: 'Kurul 2/Tıbbi Genetik/2)Nörolojik Hastalıklar ve Genetiği.pdf', name: '2)Nörolojik Hastalıklar ve Genetiği.pdf', pages: 98, fileId: '1cpBFefnLEa1Y4gouNh_1nMscR-5EuaAH' } as SourceFile],
  },
  'k2p-k2-27-aile-hekimliginde-periyodik-muayeneler-1': {
    title: 'Periyodik Sağlık Muayeneleri',
    decks: [],
    files: [{ path: 'Kurul 2/Aile Hekimliği /1)PERİYODİK MUAYENELER.pdf', name: '1)PERİYODİK MUAYENELER.pdf', pages: 135, fileId: '1ct_laG60bexcgGkR8L4ekjbdgkUWSvnM' } as SourceFile],
  },
  // 2026-11-10 8. parti (k2-28): deste yok.
  'k2p-k2-28-sik-gorulen-norolojik-hastaliklar-ve-rehabilitasyo': {
    title: 'Sık Görülen Nörolojik Hastalıklarda Rehabilitasyon',
    decks: [],
    files: [{ path: 'Kurul 2/FTR/2)NÖROLOJİK HASTALIKLARDA REHABİLİTASYON.pdf', name: '2)NÖROLOJİK HASTALIKLARDA REHABİLİTASYON.pdf', pages: 46, fileId: '1zGxWg8ORUzrkGZIECiMg6bV6u42op6W2' } as SourceFile],
  },
  // 2026-11-12 9. parti (k2-29, k2-30, k2-31): deste yok.
  'k2p-k2-29-santral-sinir-sistemi-enfeksiyonlari': {
    title: 'Santral Sinir Sistemi Enfeksiyonları',
    decks: [],
    files: [{ path: 'Kurul 2/Tıbbi Patoloji/3)Santral Sinir Sistemi Enfeksiyonları.pdf', name: '3)Santral Sinir Sistemi Enfeksiyonları.pdf', pages: 57, fileId: '10NYEyjYvB8k8Qt_1zHA55wcUoA4gA0Xl' } as SourceFile],
  },
  'k2p-k2-30-norodejeneratif-hastaliklar': {
    title: 'Nörodejeneratif Hastalıklar',
    decks: [],
    files: [{ path: 'Kurul 2/Tıbbi Patoloji/4)Nörodejeneratif Hastalıklar.pdf', name: '4)Nörodejeneratif Hastalıklar.pdf', pages: 67, fileId: '1P7PYS5R2fJOJ44tIL0tqYj0VHT5EqKke' } as SourceFile],
  },
  'k2p-k2-31-medulla-spinalis-hastaliklari': {
    title: 'Medulla Spinalis Hastalıkları',
    decks: [],
    files: [{ path: 'Kurul 2/Nöroloji/8)Medulla Spinalis Hastalıkları.pdf', name: '8)Medulla Spinalis Hastalıkları.pdf', pages: 46, fileId: '1ISKIIXBm01K1ohrRtdoOJrHxqrVknPwf' } as SourceFile],
  },
  'k2p-k2-38-travma-ve-stres-baglantili-bozukluklar': {
    title: 'Travma ve Stres Bağlantılı Bozukluklar',
    decks: [],
    files: [{ path: 'Kurul 2/Psikiyatri /5)TSSB.pdf', name: '5)TSSB.pdf', pages: 28, fileId: '1C8cwvudGGlO19JebFMKyf9cLIG7Tq2jK' } as SourceFile],
  },
  'k1p-k1-70-tbg-sinav-kampi': {
    title: 'TBG Sınav Kampı',
    decks: [
      'k1p-k1-01-dismorfolojide-genetik-terminoloji-v2',
      'k1p-k1-10-kromozomal-hastaliklar-ve-genetik-danisma-v2',
      'k1p-k1-19-dogumsal-kadin-erkek-genital-gelisim-anomalileri-v2',
      'k1p-k1-31-urogenital-sistem-tumorlerinde-genetik-belirtecler-v2',
      'k1p-k1-35-prenatal-tani-yontemleri-v2',
      'k1p-k1-60-preimplantasyon-genetik-tani-pgt',
      // PDF çıkmış entegrasyonu (2026-10-21): abortus ve kalıtsal böbrek hastalıkları slaytları
      'k1p-k1-61-abortus-v2',
      'k1p-k1-44-vaskuler-ve-kistik-bobrek-hastaliklari-v2',
      'k1p-k1-27-uriner-sistem-tas-hastaliklari-fizyopatolojisi-v2',
      'k1p-k1-38-glomeruler-hastaliklar-nefritik-sendrom-v2',
      'k1p-k1-45-bobrek-tumorleri-v2',
    ],
  },
};
function sanalDeste(deckId: string, decks: Record<string, DeckSourceEntry>): DeckSourceEntry | undefined {
  const s = SANAL_DESTELER[deckId];
  if (!s) return undefined;
  if (s.files) return { title: s.title, files: s.files } as DeckSourceEntry;
  const files = s.decks.map((id) => decks[id]?.files?.[0]).filter((f): f is SourceFile => !!f);
  return files.length === s.decks.length ? { title: s.title, files } as DeckSourceEntry : undefined;
}

export function deckSourceEntry(deckId: string): DeckSourceEntry | undefined {
  const decks = deckSources().decks;
  return decks[deckId] || sanalDeste(deckId, decks);
}

export interface ResolvedDeckPdf {
  name: string;
  /** Üst klasör (ör. "Üroloji"): aynı adlı iki PDF'i ayırt etmek için */
  folder: string;
  /** Diskte yoksa null (sıra korunur: slaytlardaki dosya indeksi bu diziye bakar) */
  full: string | null;
  size: number;
  mtimeMs: number;
  fileId?: string;
  pages?: number;
}

/** Yalnız drive_root içinde: önce birebir göreli yol, sonra aynı ad anahtarı (Drive'da yeniden adlandırma). */
function resolveFile(f: SourceFile): string | null {
  const idx = index();
  const hit = idx.byRel.get(f.path.normalize('NFC'));
  if (hit && fs.existsSync(hit)) return hit;
  const k = nameKey(f.name);
  const same = idx.driveFiles.filter((d) => nameKey(d.rel) === k && path.dirname(d.rel) === path.dirname(f.path.normalize('NFC')));
  const pool = same.length ? same : idx.driveFiles.filter((d) => nameKey(d.rel) === k);
  return pool.length === 1 && fs.existsSync(pool[0].full) ? pool[0].full : null;
}

/**
 * Destenin PDF'leri, eşleme dosyasındaki sırayla (ilk eleman ana kaynak). İçerikle doğrulanmamış eşleşme yoktur:
 * eşleme dosyasında olmayan deste için boş döner (başlığa göre tahmin yapılmaz).
 */
export function resolveDeckPdfs(deckId: string): ResolvedDeckPdf[] {
  const arsiv = arsivPdf(deckId);
  if (arsiv) return [arsiv];
  const ozet = ozetPdf(deckId);
  if (ozet) return [ozet];
  const entry = deckSourceEntry(deckId);
  return (entry?.files || []).map((f) => {
    const full = resolveFile(f);
    let size = 0;
    let mtimeMs = 0;
    if (full) {
      try {
        const st = fs.statSync(full);
        size = st.size;
        mtimeMs = st.mtimeMs;
      } catch {
        /* yarışta silindi */
      }
    }
    return {
      name: f.name,
      folder: path.basename(path.dirname(f.path)).normalize('NFC').trim(),
      full: full && size ? full : null,
      size,
      mtimeMs,
      fileId: f.fileId,
      pages: f.pages,
    };
  });
}

/*
 * Son Prova özet PDF'leri (scripts/son_prova/pdf_kirp.mjs): partın konuşma metninde atıf yapılan slayt sayfaları,
 * kaynak derslerin PDF'lerinden kırpılıp tek PDF'te birleştirilir → data/son_prova/pdf/<partKey>.pdf (+ .json: ad, sayfa).
 * Deste kimliği "k<kurul>p-<partKey>" (ör. k1p-k1-81-son-prova-patoloji-1); eşleme dosyasına girmez.
 */
const OZET_DECK_RE = /^k\d+p-(k\d+-\d+-(?:son-prova|blok-ozet)-[a-z0-9-]+)$/; // blok özet (Patoloji 16–20 …) aynı hattan
const ARSIV_DECK_RE = /^k(\d+)p-(y25-k\d+-\d+-[a-z0-9-]+)$/;
const arsivPdfDir = () => fs.existsSync('/home/ubuntu/medsor/meds_database_25_26/pdf')
  ? '/home/ubuntu/medsor/meds_database_25_26/pdf'
  : path.resolve(process.cwd(), '..', 'meds_database_25_26', 'pdf');
const arsivHizalamaDir = () => path.resolve(process.cwd(), 'data', 'arsiv_25_26', 'sesli_anlatim', 'hizalama');
function arsivPdf(deckId: string): ResolvedDeckPdf | null {
  const m = ARSIV_DECK_RE.exec(deckId);
  if (!m) return null;
  const [, kurul, key] = m;
  const full = path.join(arsivPdfDir(), `kurul${kurul}`, `${key}.pdf`);
  let meta: { name?: string; pages?: number; fileId?: string } = {};
  try {
    const hz = JSON.parse(fs.readFileSync(path.join(arsivHizalamaDir(), `${key}.json`), 'utf8'));
    const f = hz?.dosyalar?.[0];
    if (f) meta = { name: f.name, pages: f.pages, fileId: f.fileId };
  } catch { /* yok */ }
  let size = 0;
  let mtimeMs = 0;
  try { const st = fs.statSync(full); size = st.size; mtimeMs = st.mtimeMs; } catch { /* henüz üretilmedi */ }
  return { name: meta.name || `${key}.pdf`, folder: `2025-2026 Kurul ${kurul}`, full: size ? full : null, size, mtimeMs, pages: meta.pages, fileId: meta.fileId };
}
const arsivDesteleri = (): string[] => {
  try {
    const out: string[] = [];
    for (let k = 2; k <= 6; k++) {
      const dir = path.join(arsivPdfDir(), `kurul${k}`);
      if (!fs.existsSync(dir)) continue;
      for (const f of fs.readdirSync(dir)) {
        if (/\.pdf$/.test(f)) out.push(`k${k}p-${f.replace(/\.pdf$/, '')}`);
      }
    }
    return out;
  } catch { return []; }
};
const ozetDir = () => path.resolve(process.cwd(), 'data', 'son_prova', 'pdf');
function ozetPdf(deckId: string): ResolvedDeckPdf | null {
  const m = OZET_DECK_RE.exec(deckId);
  if (!m) return null;
  const full = path.join(ozetDir(), `${m[1]}.pdf`);
  let meta: { name?: string; pages?: number } = {};
  try { meta = JSON.parse(fs.readFileSync(path.join(ozetDir(), `${m[1]}.json`), 'utf8')); } catch { /* yok */ }
  let size = 0;
  let mtimeMs = 0;
  try { const st = fs.statSync(full); size = st.size; mtimeMs = st.mtimeMs; } catch { /* henüz üretilmedi */ }
  return { name: meta.name || `${m[1]}.pdf`, folder: 'Son Prova', full: size ? full : null, size, mtimeMs, pages: meta.pages };
}
const ozetDesteleri = (): string[] => {
  try {
    return fs.readdirSync(ozetDir()).filter((f) => /\.pdf$/.test(f)).map((f) => {
      const key = f.replace(/\.pdf$/, '');
      return `k${/^k(\d+)-/.exec(key)?.[1] || '1'}p-${key}`;
    });
  } catch { return []; }
};

export type DeckPdfPublic = { name: string; folder: string; size: number; pages?: number; fileId?: string; available: boolean };
export const toPublic = (f: ResolvedDeckPdf): DeckPdfPublic => ({ name: f.name, folder: f.folder, size: f.size, pages: f.pages, fileId: f.fileId, available: !!f.full });

/** Tüm desteler için diskte açılabilen PDF listesi (Öğren kataloğundaki PDF düğmeleri için). */
export function deckPdfAvailability(): Record<string, DeckPdfPublic[]> {
  const out: Record<string, DeckPdfPublic[]> = {};
  for (const id of [...Object.keys(deckSources().decks), ...Object.keys(SANAL_DESTELER), ...ozetDesteleri(), ...arsivDesteleri()]) {
    const files = resolveDeckPdfs(id);
    if (files.some((f) => f.full)) out[id] = files.map(toPublic);
  }
  return out;
}
