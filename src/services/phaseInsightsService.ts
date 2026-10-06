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

export function getQuestionInsights(questionId: string): any | null {
  const db = load();
  return db?.items?.[questionId] || null;
}

export function getInsightsSummary(): { generatedAt: string | null; counts: Record<string, number>; total: number } {
  const db = load();
  return {
    generatedAt: db?.generated_at || null,
    counts: db?.counts || {},
    total: db ? Object.keys(db.items).length : 0,
  };
}
