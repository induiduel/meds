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

// Yönetim konsolundan elle düzeltmeler: $MEDS_DATABASE_DIR/derived/manual_overrides/faz_duzeltmeleri.json
// Faz çıktıları değiştirilmez; düzeltme okuma sırasında uygulanır ve faz zinciri yeniden üretse de kalır.
const dbDir = () => process.env.MEDS_DATABASE_DIR || path.resolve(process.cwd(), '..', 'meds_database');
const overridesFile = () => path.join(dbDir(), 'derived', 'manual_overrides', 'faz_duzeltmeleri.json');

export type PhaseOverride = {
  gizle?: string[]; // gizlenecek bölümler: slayt | faz6 | kisaltmalar | terimler | mufredat | varliklar
  slaytlar?: { kaynak: string; sayfa: number; alinti?: string }[];
  kazanim?: { kurul?: number; ders?: string; konu?: string; kazanim?: string };
  kisaltmalar?: Record<string, string>;
  not?: string;
  guncelleyen?: string;
  guncelleme?: string;
};

function readOverrides(): Record<string, PhaseOverride> {
  try {
    return JSON.parse(fs.readFileSync(overridesFile(), 'utf-8')) || {};
  } catch {
    return {};
  }
}

export function getPhaseOverride(questionId: string): PhaseOverride | null {
  return readOverrides()[questionId] || null;
}

export function savePhaseOverride(questionId: string, ov: PhaseOverride | null, by: string): PhaseOverride | null {
  const all = readOverrides();
  if (!ov) delete all[questionId];
  else all[questionId] = { ...ov, guncelleyen: by, guncelleme: new Date().toISOString() };
  fs.mkdirSync(path.dirname(overridesFile()), { recursive: true });
  const tmp = overridesFile() + '.tmp';
  fs.writeFileSync(tmp, JSON.stringify(all, null, 1));
  fs.renameSync(tmp, overridesFile());
  return all[questionId] || null;
}

function applyOverride(item: any, ov: PhaseOverride): any {
  const out = { ...item, elle_duzeltildi: true };
  if (ov.slaytlar?.length) out.slayt = { guven: 'elle', slaytlar: ov.slaytlar };
  if (ov.kazanim) out.mufredat = { guven: 'elle', dogrulama: 'elle', kazanimlar: [ov.kazanim] };
  if (ov.kisaltmalar) out.faz6_5 = { ...(out.faz6_5 || { terimler: [], esanlamlilar: {} }), kisaltmalar: ov.kisaltmalar };
  for (const g of ov.gizle || []) {
    if (g === 'slayt') delete out.slayt;
    if (g === 'faz6') delete out.faz6;
    if (g === 'mufredat') { delete out.mufredat; delete out.faz8; }
    if (g === 'varliklar') delete out.varliklar;
    if (g === 'kisaltmalar' && out.faz6_5) out.faz6_5 = { ...out.faz6_5, kisaltmalar: {} };
    if (g === 'terimler') {
      if (out.faz6_5) out.faz6_5 = { ...out.faz6_5, terimler: [], esanlamlilar: {} };
      if (out.faz5) out.faz5 = { ...out.faz5, terimler: [] };
    }
  }
  return out;
}

/** Düzeltmesiz ham faz verisi (yönetim konsolu karşılaştırması için). */
export function getRawQuestionInsights(questionId: string): any | null {
  const item = load()?.items?.[questionId] || null;
  const ents = loadEntities()?.get(questionId);
  return ents ? { ...(item || {}), varliklar: ents } : item;
}

export function getQuestionInsights(questionId: string): any | null {
  const raw = getRawQuestionInsights(questionId);
  const ov = getPhaseOverride(questionId);
  if (!ov) return raw;
  return applyOverride(raw || {}, ov);
}

/** Soru bazında tüm türetilmiş kayıtlar (Öğren, müfredat, karantina, tüm Faz 13 varlıkları). */
export function getQuestionDerivedRecords(questionId: string): Record<string, any> {
  const rd = (rel: string) => {
    try {
      return JSON.parse(fs.readFileSync(path.join(dbDir(), 'derived', rel), 'utf-8'));
    } catch {
      return null;
    }
  };
  const learn = rd('learn_links.json')?.baglantilar?.[questionId] || null;
  const muf = rd('curriculum_links/soru_mufredat.json')?.sorular?.[questionId] || null;
  const kar = rd('quarantine/karantina.json');
  const karantina = kar ? (kar.sorular || kar.karantina || kar)[questionId] || null : null;
  let varliklarTum: any[] = [];
  try {
    const line = fs
      .readFileSync(entitiesFile(), 'utf-8')
      .split('\n')
      .find((l) => l.includes(`"soru_id": "${questionId}"`));
    if (line) varliklarTum = JSON.parse(line).varliklar || [];
  } catch {
    // yok
  }
  return { ogren: learn, mufredat_sinav_basligi: muf, karantina, varliklar_tum: varliklarTum };
}

export function getInsightsSummary(): { generatedAt: string | null; counts: Record<string, number>; total: number } {
  const db = load();
  return {
    generatedAt: db?.generated_at || null,
    counts: db?.counts || {},
    total: db ? Object.keys(db.items).length : 0,
  };
}
