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
export const SANAL_DESTELER: Record<string, { title: string; decks: string[] }> = {
  'k1p-k1-70-tbg-sinav-kampi': {
    title: 'TBG Sınav Kampı',
    decks: [
      'k1p-k1-01-dismorfolojide-genetik-terminoloji-v2',
      'k1p-k1-10-kromozomal-hastaliklar-ve-genetik-danisma-v2',
      'k1p-k1-19-dogumsal-kadin-erkek-genital-gelisim-anomalileri-v2',
      'k1p-k1-31-urogenital-sistem-tumorlerinde-genetik-belirtecler-v2',
      'k1p-k1-35-prenatal-tani-yontemleri-v2',
      'k1p-k1-60-preimplantasyon-genetik-tani-pgt',
    ],
  },
};
function sanalDeste(deckId: string, decks: Record<string, DeckSourceEntry>): DeckSourceEntry | undefined {
  const s = SANAL_DESTELER[deckId];
  if (!s) return undefined;
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

export type DeckPdfPublic = { name: string; folder: string; size: number; pages?: number; fileId?: string; available: boolean };
export const toPublic = (f: ResolvedDeckPdf): DeckPdfPublic => ({ name: f.name, folder: f.folder, size: f.size, pages: f.pages, fileId: f.fileId, available: !!f.full });

/** Tüm desteler için diskte açılabilen PDF listesi (Öğren kataloğundaki PDF düğmeleri için). */
export function deckPdfAvailability(): Record<string, DeckPdfPublic[]> {
  const out: Record<string, DeckPdfPublic[]> = {};
  for (const id of [...Object.keys(deckSources().decks), ...Object.keys(SANAL_DESTELER)]) {
    const files = resolveDeckPdfs(id);
    if (files.some((f) => f.full)) out[id] = files.map(toPublic);
  }
  return out;
}
