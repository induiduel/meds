/**
 * Ders PDF'lerini diskte bulur ("PDF'ten aç" için). Server-only.
 *
 * Dosyalar iki yerde olabilir: `MEDS_DATABASE_DIR/ders_notlari_pdf` (düz klasör) ve Drive'dan inen
 * ham kaynaklar `MEDS_DOWNLOADS_DIR/drive_root/**` (kurul/ders alt klasörleri). Eski rota yalnız ilkine
 * baktığı için klasör boşken her PDF 404 dönüyordu. Ad karşılaştırması Unicode NFC + Türkçe küçük harf
 * ile yapılır (macOS/Drive'dan gelen NFD adlar da eşleşir). Dizin taraması 10 dk önbelleklenir.
 */
import fs from 'fs';
import path from 'path';

const CACHE_MS = 10 * 60 * 1000;
let cache: { at: number; files: Map<string, string> } | null = null;

const norm = (s: string) => s.normalize('NFC').toLocaleLowerCase('tr-TR').replace(/\.pdf$/i, '').replace(/\s+/g, ' ').trim();

function roots(): string[] {
  const db = process.env.MEDS_DATABASE_DIR || path.resolve(process.cwd(), '..', 'meds_database');
  const dl = process.env.MEDS_DOWNLOADS_DIR || path.resolve(process.cwd(), '..', 'meds_downloads');
  return [path.join(db, 'ders_notlari_pdf'), path.join(dl, 'drive_root'), dl];
}

function walk(dir: string, out: Map<string, string>, depth = 0) {
  if (depth > 6) return;
  let entries: fs.Dirent[];
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true });
  } catch {
    return;
  }
  for (const e of entries) {
    const full = path.join(dir, e.name);
    if (e.isDirectory()) walk(full, out, depth + 1);
    else if (e.isFile() && /\.pdf$/i.test(e.name)) {
      const key = norm(e.name);
      if (!out.has(key)) out.set(key, full);
    }
  }
}

function index(): Map<string, string> {
  if (cache && Date.now() - cache.at < CACHE_MS) return cache.files;
  const files = new Map<string, string>();
  for (const r of roots()) if (fs.existsSync(r)) walk(r, files);
  cache = { at: Date.now(), files };
  return files;
}

/** Dosya adına göre PDF'in tam yolunu döner; bulunamazsa null. */
export function findLecturePdf(requestedName: string): string | null {
  const target = norm(path.basename(String(requestedName || '')));
  if (!target) return null;
  const files = index();
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
