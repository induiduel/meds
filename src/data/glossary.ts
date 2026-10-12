import rawGlossary from './medical_glossary.json';
import { safeJsonFetch } from '../services/api';
import { contentReady, isContentChanged, onContentChanged } from '../services/contentLive';

/**
 * Universal reader and synthesizer for medical terms:
 * - Unifies medical_glossary.json (both string definitions and structured objects)
 * - medical_glossary.json is curated by scripts/v2 (`study build --export`): every entry is checked
 *   against lecture notes (`dogrulama`, `kaynaklar`)
 * - medical_encyclopedia.json only contributes aliases to existing entries (it is unverified AI content)
 */
export interface GlossaryEntry {
  term: string;
  aliases?: string[];
  category: string;
  pronunciation?: string;
  definition: string;
  clinicalPearls?: string;
  badgeColor?: string;
  discipline?: string;
}

const CATEGORY_LABELS: Record<string, string> = {
  hastalik: 'Klinik hastalık',
  ilac: 'Farmakoloji',
  genetik: 'Genetik & Patoloji',
  patoloji: 'Tıbbi Patoloji',
  patojen: 'Mikrobiyoloji',
  bakteriyoloji: 'Bakteriyoloji',
  viroloji: 'Viroloji',
  terim: 'Tıbbi terim',
  protein: 'Protein & molekül',
  'halk-sagligi': 'Halk sağlığı',
  epidemiyoloji: 'Halk sağlığı',
  uroloji: 'Üroloji',
};

const BADGE_BY_CATEGORY: Record<string, string> = {
  hastalik: 'blue',
  ilac: 'teal',
  genetik: 'purple',
  patoloji: 'red',
  patojen: 'amber',
  bakteriyoloji: 'red',
  viroloji: 'rose',
};

// Map to deduplicate by normalized term
const termMap = new Map<string, GlossaryEntry>();

/** Ham sözlüğü (dizi ya da terim → tanım nesnesi) termMap'e işler */
function ingest(rawGlossary: unknown) {
  termMap.clear();
  // 1. Process medical_glossary.json
  if (Array.isArray(rawGlossary)) {
    for (const item of rawGlossary as any[]) {
      if (!item) continue;
      const term = String(item.term || '').trim();
      const definition = String(item.definition || item.description || '').trim();
      if (!term || !definition) continue;

      const rawCat = String(item.category || item.discipline || 'Tıbbi Patoloji');
      const category = CATEGORY_LABELS[rawCat.toLowerCase()] || rawCat;
      const normKey = term.toLowerCase();

      termMap.set(normKey, {
        term,
        aliases: Array.isArray(item.aliases) ? item.aliases : undefined,
        category,
        pronunciation: item.pronunciation || undefined,
        definition,
        clinicalPearls: String(item.clinicalPearls || item.clinicalPearl || '').trim() || undefined,
        badgeColor: item.badgeColor || BADGE_BY_CATEGORY[rawCat.toLowerCase()] || 'blue',
        discipline: item.discipline || undefined,
      });
    }
  } else if (rawGlossary && typeof rawGlossary === 'object') {
    for (const [key, val] of Object.entries(rawGlossary as Record<string, any>)) {
      if (!val) continue;

      // Case A: string definition (glossary[term] = "açıklama")
      if (typeof val === 'string') {
        const definition = val.trim();
        if (!definition) continue;
        const term = key.trim();
        const normKey = term.toLowerCase();

        termMap.set(normKey, {
          term,
          category: 'Tıbbi Patoloji',
          definition,
          badgeColor: 'teal',
        });
        continue;
      }

      // Case B: object definition ({ term, description, category, ... })
      if (typeof val === 'object') {
        const term = String(val.term || key).trim();
        const definition = String(val.definition || val.description || '').trim();
        if (!term) continue;

        const rawCat = String(val.category || val.discipline || 'Tıbbi Patoloji');
        const category = CATEGORY_LABELS[rawCat.toLowerCase()] || rawCat;
        const normKey = term.toLowerCase();

        // Only save if has definition or fallback
        if (definition) {
          termMap.set(normKey, {
            term,
            aliases: Array.isArray(val.aliases) ? val.aliases : undefined,
            category,
            pronunciation: val.pronunciation || undefined,
            definition,
            clinicalPearls: String(val.clinicalPearls || val.clinicalPearl || '').trim() || undefined,
            badgeColor: val.badgeColor || BADGE_BY_CATEGORY[rawCat.toLowerCase()] || 'purple',
            discipline: val.discipline || undefined,
          });
        }
      }
    }
  }
}
ingest(rawGlossary);

// Panelden değiştirilen sözlük canlı gelir: dizi yerinde güncellenir, dinleyenler `medsoru:glossary-changed` alır
export const GLOSSARY: GlossaryEntry[] = Array.from(termMap.values());

async function pullLiveGlossary() {
  const r = await safeJsonFetch<unknown>('/api/content/glossary', { cache: 'no-store' });
  if (!r.ok || !r.data || typeof r.data !== 'object') return;
  ingest(r.data);
  GLOSSARY.splice(0, GLOSSARY.length, ...termMap.values());
  encyclopediaEnhanced = false;
  if (typeof window !== 'undefined') window.dispatchEvent(new CustomEvent('medsoru:glossary-changed'));
}
// Modül grafiği yüklenince kaydol (contentLive ile içe aktarma döngüsü)
if (typeof window !== 'undefined') setTimeout(() => {
  void contentReady(8000).then(() => { if (isContentChanged('glossary')) void pullLiveGlossary(); });
  onContentChanged('glossary', () => void pullLiveGlossary());
}, 0);


// 2. medical_encyclopedia.json: yalnız takma ad zenginleştirmesi (boşta/istek üzerine dinamik yüklenir)
let encyclopediaEnhanced = false;
export async function enhanceGlossaryWithEncyclopedia(): Promise<GlossaryEntry[]> {
  if (encyclopediaEnhanced) return GLOSSARY;
  try {
    const rawModule = await import('./medical_encyclopedia.json');
    const rawEncyclopedia = rawModule.default || rawModule;
    if (Array.isArray(rawEncyclopedia)) {
      for (const enc of rawEncyclopedia as any[]) {
        if (!enc) continue;
        const term = String(enc.term || enc.title || '').trim();
        if (!term) continue;
        const normKey = term.toLowerCase();

        const definition = String(enc.definition || enc.description || enc.summary || '').trim();
        if (!definition) continue;

        const aliases: string[] = [];
        if (enc.latinName && typeof enc.latinName === 'string') {
          aliases.push(enc.latinName.trim());
        }
        if (Array.isArray(enc.aliases)) {
          aliases.push(...enc.aliases.map((a: string) => String(a).trim()));
        }
        const parenMatch = term.match(/^(.+?)\s*\((.+?)\)$/);
        if (parenMatch) {
          aliases.push(parenMatch[1].trim());
          aliases.push(parenMatch[2].trim());
        }

        const existing = termMap.get(normKey) || (parenMatch ? termMap.get(parenMatch[1].trim().toLowerCase()) : undefined);
        if (existing && aliases.length > 0) {
          const own = existing.term.toLowerCase();
          const mergedAliases = Array.from(new Set([...(existing.aliases || []), ...aliases])).filter(
            (a) => a && a.toLowerCase() !== own
          );
          existing.aliases = mergedAliases.length > 0 ? mergedAliases : undefined;
        }
      }
      encyclopediaEnhanced = true;
    }
  } catch {}
  return GLOSSARY;
}

