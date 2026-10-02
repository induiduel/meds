import rawGlossary from './medical_glossary.json';
import rawEncyclopedia from './medical_encyclopedia.json';

/**
 * Universal reader and synthesizer for medical terms:
 * - Unifies medical_glossary.json (both string definitions and structured objects)
 * - Merges medical_encyclopedia.json (rich pathology, pharmacology, and clinical diseases)
 * Ensures every medical term, drug, disease, bacterium and virus has a live, interactive floating toast card!
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

// 2. Process medical_encyclopedia.json (Enrich and fill empty definitions)
if (Array.isArray(rawEncyclopedia)) {
  for (const enc of rawEncyclopedia as any[]) {
    if (!enc || !enc.title) continue;
    const term = String(enc.title).trim();
    const normKey = term.toLowerCase();

    // Summary as main definition
    const definition = String(enc.summary || '').trim();
    if (!definition) continue;

    // Clinical Pearls from clinicalSignificance or highYieldFacts
    const pearlsArr: string[] = [];
    if (Array.isArray(enc.clinicalSignificance)) {
      pearlsArr.push(...enc.clinicalSignificance);
    }
    if (Array.isArray(enc.highYieldFacts)) {
      pearlsArr.push(...enc.highYieldFacts);
    }
    const clinicalPearls = pearlsArr.slice(0, 3).join(' • ').trim() || undefined;

    // Aliases from relatedTerms or clean term without parentheses
    const aliases: string[] = [];
    if (Array.isArray(enc.relatedTerms)) {
      aliases.push(...enc.relatedTerms.map((t: string) => t.replace(/-/g, ' ')));
    }
    const parenMatch = term.match(/^(.+?)\s*\((.+?)\)$/);
    if (parenMatch) {
      aliases.push(parenMatch[1].trim());
      aliases.push(parenMatch[2].trim());
    }

    const existing = termMap.get(normKey);
    if (existing) {
      // Merge: prefer longer definition and combine pearls
      if (!existing.definition || definition.length > existing.definition.length) {
        existing.definition = definition;
      }
      if (!existing.clinicalPearls && clinicalPearls) {
        existing.clinicalPearls = clinicalPearls;
      }
      if (aliases.length > 0) {
        const mergedAliases = Array.from(new Set([...(existing.aliases || []), ...aliases]));
        existing.aliases = mergedAliases;
      }
    } else {
      const rawCat = String(enc.category || enc.discipline || 'Tıbbi Patoloji');
      const category = CATEGORY_LABELS[rawCat.toLowerCase()] || rawCat;

      termMap.set(normKey, {
        term,
        aliases: aliases.length > 0 ? aliases : undefined,
        category,
        definition,
        clinicalPearls,
        badgeColor: BADGE_BY_CATEGORY[rawCat.toLowerCase()] || 'rose',
        discipline: enc.discipline || undefined,
      });
    }
  }
}

export const GLOSSARY: GlossaryEntry[] = Array.from(termMap.values());
