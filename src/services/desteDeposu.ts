/**
 * Öğren desteleri tek deposu (sunucu tarafı) — `scripts/deste_deposu.py`'nin eşi.
 *
 * `interactive_learning_decks.json` yolu yalnız burada tanımlıdır. Okuma canlı içerik katmanından
 * (`resolveContent`) yapılır ve mtime ile önbelleğe alınır; yazım katmana (`writableContent`) atomik
 * yapılır, `markContentChanged('decks', ids)` yayınlanır ve önbellek geçersiz kılınır.
 */
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { fileURLToPath } from 'url';
import { resolveContent, writableContent, markContentChanged } from './contentOverlay.ts';

const __filename = fileURLToPath(import.meta.url);
const ROOT_DIR = path.resolve(path.dirname(__filename), '..', '..'); // meds/

export const INTERACTIVE_DECKS_FILE = path.resolve(ROOT_DIR, 'src', 'data', 'interactive_learning_decks.json');

export interface DesteOnbellegi {
  file: string;
  mtime: number;
  data: any[];
  compactJsonStr: string;
  compactEtag: string;
  fullJsonStr: string;
  fullEtag: string;
}

let decksCache: DesteOnbellegi | null = null;

/** Son önbellek (ETag'li hazır JSON dizgeleri için); `desteleriOku()` çağrısından sonra günceldir. */
export function desteOnbellegi(): DesteOnbellegi | null {
  return decksCache;
}

/**
 * Deste listesini okur (katman öncelikli, mtime önbellekli). Dönen dizi önbellekle paylaşılır — DEĞİŞTİRME.
 * Değiştirip geri yazacaksan `{ kopya: true }` ver: dosyadan taze ayrıştırılmış bağımsız liste döner.
 */
export function desteleriOku(secenek: { kopya?: boolean } = {}): any[] {
  if (secenek.kopya) {
    try {
      const file = resolveContent(INTERACTIVE_DECKS_FILE);
      if (!fs.existsSync(file)) return [];
      const data = JSON.parse(fs.readFileSync(file, 'utf-8'));
      return Array.isArray(data) ? data : [];
    } catch (e) {
      console.error('Error reading interactive_learning_decks.json:', e);
      return [];
    }
  }
  try {
    const file = resolveContent(INTERACTIVE_DECKS_FILE);
    if (fs.existsSync(file)) {
      const mtime = fs.statSync(file).mtimeMs;
      if (decksCache && decksCache.file === file && decksCache.mtime === mtime) return decksCache.data;
      const data = JSON.parse(fs.readFileSync(file, 'utf-8'));
      const list = Array.isArray(data) ? data : [];
      const compactList = list.map((d: any) => ({
        id: d.id,
        title: d.title,
        description: d.description,
        committee: d.committee || d.committeeId,
        discipline: d.discipline,
        slideCount: d.slides?.length || 0,
        flashcardCount: d.flashcards?.length || 0,
        updatedAt: d.updatedAt,
      }));
      const compactJsonStr = JSON.stringify({ total: compactList.length, decks: compactList });
      const compactEtag = `"${crypto.createHash('md5').update(compactJsonStr).digest('hex')}"`;
      const fullJsonStr = JSON.stringify({ total: list.length, decks: list });
      const fullEtag = `"${crypto.createHash('md5').update(fullJsonStr).digest('hex')}"`;
      decksCache = { file, mtime, data: list, compactJsonStr, compactEtag, fullJsonStr, fullEtag };
      return list;
    }
  } catch (e) {
    console.error('Error reading interactive_learning_decks.json:', e);
  }
  return decksCache?.data || [];
}

/** Tek deste: tam id, `k1p-<id>` ya da id içeren ilk eşleşme (server.ts /api/decks/:id kuralı). */
export function desteOku(id: string, list: any[] = desteleriOku()): any | null {
  return list.find((d) => d.id === id || d.id === `k1p-${id}` || d.id.includes(id)) || null;
}

/** Katman etkin mi (deste dosyası katmandan mı geliyor)? */
export function desteKatmandaMi(): boolean {
  return resolveContent(INTERACTIVE_DECKS_FILE) !== INTERACTIVE_DECKS_FILE;
}

/** Listeyi katmana atomik yazar (JSON.stringify girinti 2), değişimi yayınlar, önbelleği geçersiz kılar. */
export function desteleriYaz(list: any[], degisenIdler: string[]): void {
  const filePath = writableContent(INTERACTIVE_DECKS_FILE);
  const dir = path.dirname(filePath);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  const tempPath = `${filePath}.tmp_${Date.now()}_${Math.random().toString(36).slice(2, 6)}`;
  fs.writeFileSync(tempPath, JSON.stringify(list, null, 2), 'utf-8');
  fs.renameSync(tempPath, filePath);
  decksCache = null;
  markContentChanged('decks', degisenIdler.map(String));
}
