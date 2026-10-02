import rawGlossary from './medical_glossary.json';

/**
 * One reader for medical_glossary.json, whatever its current shape:
 * - an array of { term, definition, clinicalPearls, pronunciation, aliases, badgeColor }  (v1)
 * - an object keyed by term with { term, description, clinicalPearl, discipline, category } (v2)
 * Entries without any definition text are dropped so no empty card or popover is shown.
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
  genetik: 'Genetik',
  patoloji: 'Tıbbi patoloji',
  patojen: 'Mikrobiyoloji',
};

const BADGE_BY_CATEGORY: Record<string, string> = {
  hastalik: 'blue',
  ilac: 'teal',
  genetik: 'purple',
  patoloji: 'red',
  patojen: 'amber',
};

const toEntry = (x: any): GlossaryEntry | null => {
  if (!x || typeof x !== 'object' || !x.term) return null;
  const definition = String(x.definition || x.description || '').trim();
  if (!definition) return null;
  const rawCat = String(x.category || x.discipline || 'Diğer');
  const category = CATEGORY_LABELS[rawCat.toLocaleLowerCase('tr-TR')] || rawCat;
  return {
    term: String(x.term),
    aliases: Array.isArray(x.aliases) ? x.aliases : undefined,
    category,
    pronunciation: x.pronunciation || undefined,
    definition,
    clinicalPearls: String(x.clinicalPearls || x.clinicalPearl || '').trim() || undefined,
    badgeColor: x.badgeColor || BADGE_BY_CATEGORY[rawCat.toLocaleLowerCase('tr-TR')],
    discipline: x.discipline || undefined,
  };
};

const source: any[] = Array.isArray(rawGlossary) ? (rawGlossary as any[]) : Object.values(rawGlossary as Record<string, any>);

export const GLOSSARY: GlossaryEntry[] = source.map(toEntry).filter((e): e is GlossaryEntry => !!e);
