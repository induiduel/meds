/**
 * Faz 12 temizlik katmanı (server-only): data/lecture_notes.json özgün kalır; temizlenmiş sayfa metinleri
 * $MEDS_DATABASE_DIR/derived/clean_notes/lecture_notes_overlay.json içinden okunup gösterimde uygulanır
 * (glif/madde işareti onarımı, OCR çöp satırları, URL/sayfa no, tekrarlayan üst-alt bilgi). Dosya değişince yeniden yüklenir.
 */
import fs from 'fs';
import path from 'path';

type Overlay = { zaman?: string; notlar: Record<string, Record<string, string>> };
let cache: Overlay | null = null;
let cacheMtime = 0;

const overlayFile = () =>
  path.join(
    process.env.MEDS_DATABASE_DIR || path.resolve(process.cwd(), '..', 'meds_database'),
    'derived',
    'clean_notes',
    'lecture_notes_overlay.json',
  );

function load(): Overlay | null {
  try {
    const stat = fs.statSync(overlayFile());
    if (!cache || stat.mtimeMs !== cacheMtime) {
      const parsed = JSON.parse(fs.readFileSync(overlayFile(), 'utf-8')) as Overlay;
      if (parsed?.notlar && Object.keys(parsed.notlar).length) {
        cache = parsed;
        cacheMtime = stat.mtimeMs;
      }
    }
  } catch {
    // katman yoksa özgün metin gösterilir
  }
  return cache;
}

/** Notun sayfalarına temiz metni uygular; değişen sayfa yoksa notu aynen döndürür. */
export function applyCleanOverlay<T extends { id?: string; pages?: Array<{ pageNumber?: number; content?: string }> }>(note: T): T {
  const pages = load()?.notlar?.[String(note.id)];
  if (!pages || !note.pages) return note;
  return {
    ...note,
    pages: note.pages.map((p) => {
      const clean = pages[String(p.pageNumber)];
      return clean !== undefined ? { ...p, content: clean, cleaned: true } : p;
    }),
  };
}
