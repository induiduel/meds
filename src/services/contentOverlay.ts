/**
 * Canlı içerik katmanı (server-only).
 *
 * src/data altındaki paket verisi (sözlük, kartlar, hastalıklar, Öğren desteleri, örnek sorular) ön yüze
 * derlemede gömülür; Oracle'da da imajın içinde durur. Yönetim panelinden yapılan değişiklik oraya yazılırsa
 * hem ziyaretçiye yansımaz hem bir sonraki dağıtımda silinir.
 *
 * Bu yüzden panel değişiklikleri data/content/<src/data'ya göre yol> altına (kalıcı birim) yazılır ve
 * okuyan herkes (katalog, /api/decks, /api/content/*) önce buraya bakar. İstemci /api/content/manifest ile
 * hangi verinin paketten yeni olduğunu öğrenir, SSE `content_changed` ile anında tazelenir.
 *
 * Dağıtım: deploy/oracle/content-overlay-sync.sh önce katmanı yerel src/data'ya geri çeker (yerel dosya
 * son dağıtımdan beri değişmediyse), dağıtımdan sonra imajla birebir aynı olan katman dosyalarını siler.
 */
import fs from 'fs';
import path from 'path';

let SRC = '';
let DIR = '';
const IDS_FILE = () => path.join(DIR, '_ids.json');

/** Katmanı kullanan türler → src/data'ya göre dosya (örnek sorular klasördür) */
export const CONTENT_FILES: Record<string, string> = {
  glossary: 'medical_glossary.json',
  cards: 'question_cards.json',
  diseases: 'diseases.json',
  decks: 'interactive_learning_decks.json',
  ornek: 'ornek_sorular',
  summaries: 'lectureSummariesCatalog.json',
};

export function initContentOverlay(rootDir: string, dataDir: string) {
  SRC = path.join(rootDir, 'src', 'data');
  DIR = path.join(dataDir, 'content');
}

function relOf(file: string): string | null {
  if (!SRC) return null;
  const rel = path.relative(SRC, path.resolve(file));
  return rel && !rel.startsWith('..') && !path.isAbsolute(rel) ? rel : null;
}

/** Okuma yolu: katmanda değiştirilmiş kopya varsa o, yoksa paketteki dosya */
export function resolveContent(file: string): string {
  const rel = relOf(file);
  if (!rel) return file;
  const o = path.join(DIR, rel);
  return fs.existsSync(o) ? o : file;
}

/** Yazma yolu: src/data altındaki her dosya katmana yazılır */
export function writableContent(file: string): string {
  const rel = relOf(file);
  if (!rel) return file;
  const o = path.join(DIR, rel);
  fs.mkdirSync(path.dirname(o), { recursive: true });
  return o;
}

function readIds(): Record<string, Record<string, number>> {
  try { return JSON.parse(fs.readFileSync(IDS_FILE(), 'utf8')) || {}; } catch { return {}; }
}

/** Değişen kayıt kimliklerini not eder (istemci yalnız bu desteleri sunucudan çeker) */
export function markContentChanged(entity: string, ids: string[] = []) {
  if (!DIR || !CONTENT_FILES[entity] || !ids.length) return;
  const all = readIds();
  const now = Date.now();
  all[entity] = { ...(all[entity] || {}) };
  for (const id of ids) all[entity][id] = now;
  fs.mkdirSync(DIR, { recursive: true });
  fs.writeFileSync(IDS_FILE(), JSON.stringify(all, null, 2), 'utf8');
}

const mtimeOf = (p: string) => { try { return fs.statSync(p).mtimeMs; } catch { return 0; } };

/**
 * Paketten yeni olanlar. Katman dosyası dağıtımda silinince (imaj artık aynı) türü de listeden düşer.
 * decks: değişen deste kimlikleri; ornek: değişen ders dosyaları (k1/k1-01 gibi).
 */
export function contentManifest() {
  const out: Record<string, { at: number; ids?: string[] }> = {};
  const ids = readIds();
  let pruned = false;
  for (const [entity, rel] of Object.entries(CONTENT_FILES)) {
    const o = path.join(DIR, rel);
    if (!fs.existsSync(o)) {
      if (ids[entity]) { delete ids[entity]; pruned = true; }
      continue;
    }
    if (entity === 'ornek') {
      const files: string[] = [];
      for (const k of fs.readdirSync(o)) {
        const kd = path.join(o, k);
        if (fs.statSync(kd).isDirectory()) for (const f of fs.readdirSync(kd)) if (f.endsWith('.json')) files.push(`${k}/${f.replace(/\.json$/, '')}`);
      }
      if (files.length) out.ornek = { at: mtimeOf(o), ids: files };
      continue;
    }
    out[entity] = { at: mtimeOf(o), ids: entity === 'decks' ? Object.keys(ids.decks || {}) : undefined };
  }
  if (pruned) try { fs.writeFileSync(IDS_FILE(), JSON.stringify(ids, null, 2), 'utf8'); } catch { /* yoksay */ }
  return out;
}
