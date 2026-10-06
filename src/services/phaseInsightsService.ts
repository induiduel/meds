/**
 * Faz 5 / 6 / 6.5 / 8 analizlerini okur (server-only).
 * Kaynak: $MEDS_DATABASE_DIR/derived/phase_insights/insights.json
 * (scripts/advanced_ai/export_phase_insights.py üretir; faz zinciri her turda yeniler).
 * Dosya değişince (mtime) yeniden yüklenir. Faz 6 yapay zekâ üretimidir ve `dogrulanmadi: true` taşır.
 */
import fs from 'fs';
import path from 'path';

// dotenv sunucu açılışında yüklendiği için yol her okumada çözülür
const insightsFile = () =>
  path.join(
    process.env.MEDS_DATABASE_DIR || path.resolve(process.cwd(), '..', 'meds_database'),
    'derived',
    'phase_insights',
    'insights.json',
  );

type InsightsDb = { generated_at?: string; counts?: Record<string, number>; items: Record<string, any> };

let cache: InsightsDb | null = null;
let cacheMtime = 0;

function load(): InsightsDb | null {
  try {
    const stat = fs.statSync(insightsFile());
    if (!cache || stat.mtimeMs !== cacheMtime) {
      const parsed = JSON.parse(fs.readFileSync(insightsFile(), 'utf-8')) as InsightsDb;
      if (parsed && parsed.items && Object.keys(parsed.items).length > 0) {
        cache = parsed;
        cacheMtime = stat.mtimeMs;
      }
    }
  } catch {
    // dosya yoksa ya da yazılırken okunduysa önceki önbellek kullanılır
  }
  return cache;
}

// Faz 13 tıbbi varlıklar: $MEDS_DATABASE_DIR/derived/entities/soru_varliklar.jsonl (phase13_entities.py).
// Sitede yalnız kimlikli varlıklar (Wikidata/UMLS, WHO ICD-10, kanıtlı sözlük) gösterilir; kimliksiz GLiNER tahmini kanıt değildir.
const entitiesFile = () =>
  path.join(process.env.MEDS_DATABASE_DIR || path.resolve(process.cwd(), '..', 'meds_database'), 'derived', 'entities', 'soru_varliklar.jsonl');

type Entity = { ad: string; tur: string | null; kaynak: string; kimlik?: Record<string, string[]> };
let entCache: Map<string, Entity[]> | null = null;
let entMtime = 0;

function loadEntities(): Map<string, Entity[]> | null {
  try {
    const stat = fs.statSync(entitiesFile());
    if (!entCache || stat.mtimeMs !== entMtime) {
      const map = new Map<string, Entity[]>();
      for (const line of fs.readFileSync(entitiesFile(), 'utf-8').split('\n')) {
        if (!line.trim()) continue;
        try {
          const r = JSON.parse(line);
          const seen = new Set<string>();
          const list: Entity[] = [];
          for (const v of r.varliklar || []) {
            if (!v.kavram || !v.ad) continue;
            const key = String(v.ad).toLocaleLowerCase('tr-TR');
            if (seen.has(key)) continue;
            seen.add(key);
            list.push({ ad: v.ad, tur: v.tur || null, kaynak: v.kaynak, kimlik: v.kimlik || undefined });
          }
          if (list.length) map.set(String(r.soru_id), list);
        } catch {
          // yarım yazılmış satır
        }
      }
      if (map.size > 0) {
        entCache = map;
        entMtime = stat.mtimeMs;
      }
    }
  } catch {
    // dosya yok: önceki önbellek
  }
  return entCache;
}

export function getQuestionInsights(questionId: string): any | null {
  const db = load();
  const item = db?.items?.[questionId] || null;
  const ents = loadEntities()?.get(questionId);
  if (!ents) return item;
  return { ...(item || {}), varliklar: ents };
}

export function getInsightsSummary(): { generatedAt: string | null; counts: Record<string, number>; total: number } {
  const db = load();
  return {
    generatedAt: db?.generated_at || null,
    counts: db?.counts || {},
    total: db ? Object.keys(db.items).length : 0,
  };
}
