/**
 * Ders (branş) kimliği: Apple Sağlık'taki kategori renkleri gibi her ders kendi rengini taşır.
 * Renk değerleri styles/health.css'te `.d-<anahtar>` sınıflarıyla tanımlıdır
 * (--d dolgu, --d-ink metin, --d-soft zemin); burada yalnız ad → anahtar eşlemesi yapılır.
 */
export type DisciplineKey =
  | 'pat' | 'farm' | 'enf' | 'mikro' | 'halk' | 'ic' | 'gen' | 'cocuk' | 'kadin' | 'acil'
  | 'biyo' | 'ana' | 'fiz' | 'noro' | 'psik' | 'kardi' | 'cerr' | 'ftr' | 'uro' | 'onko' | 'diger';

const RULES: [RegExp, DisciplineKey, string][] = [
  [/patoloji/i, 'pat', 'Patoloji'],
  [/farmakoloji/i, 'farm', 'Farmakoloji'],
  [/mikrobiyoloji|parazit|viroloji|immünoloji|immunoloji/i, 'mikro', 'Mikrobiyoloji'],
  [/enfeksiyon/i, 'enf', 'Enfeksiyon'],
  [/halk sağlığı|halk sagligi|epidemiyoloji|biyoistatistik/i, 'halk', 'Halk Sağlığı'],
  [/kardiyoloji|kalp/i, 'kardi', 'Kardiyoloji'],
  [/onkoloji|hematoloji/i, 'onko', 'Onkoloji'],
  [/iç hastalık|ic hastalik|dahiliye|gastroenteroloji|nefroloji|endokrin/i, 'ic', 'İç Hastalıkları'],
  [/genetik|biyoloji/i, 'gen', 'Genetik'],
  [/çocuk|cocuk|pediatri/i, 'cocuk', 'Çocuk Sağlığı'],
  [/kadın|kadin|doğum|dogum|jinekoloji/i, 'kadin', 'Kadın Doğum'],
  [/acil/i, 'acil', 'Acil Tıp'],
  [/biyokimya/i, 'biyo', 'Biyokimya'],
  [/anatomi|histoloji|embriyoloji/i, 'ana', 'Anatomi'],
  [/fizyoloji/i, 'fiz', 'Fizyoloji'],
  [/nöroloji|noroloji|beyin/i, 'noro', 'Nöroloji'],
  [/psikiyatri|psikoloji/i, 'psik', 'Psikiyatri'],
  [/fiziksel tıp|ftr|rehabilitasyon/i, 'ftr', 'FTR'],
  [/üroloji|uroloji/i, 'uro', 'Üroloji'],
  [/cerrahi/i, 'cerr', 'Cerrahi'],
];

export function disciplineKey(name?: string | null): DisciplineKey {
  const s = String(name || '');
  for (const [re, key] of RULES) if (re.test(s)) return key;
  return 'diger';
}

/** Kısa görünen ad: "Tıbbi Patoloji Kurul Sorusu" → "Patoloji" */
export function disciplineLabel(name?: string | null): string {
  const s = String(name || '');
  for (const [re, , label] of RULES) if (re.test(s)) return label;
  return s.replace(/^tıbbi\s+/i, '').replace(/\s+(kurul|çıkmış)\s+sorusu$/i, '').trim() || 'Diğer';
}

/** `className` için: "d-pat" gibi; renkler CSS değişkeni olarak alt öğelere geçer */
export const disciplineClass = (name?: string | null) => `d-${disciplineKey(name)}`;

/**
 * Ders grupları (tıp eğitimindeki klasik ayrım). Listeler önce gruba, grup içinde soru sayısına göre dizilir.
 * Sıra = ekrandaki sıra.
 */
export const DISCIPLINE_GROUPS: { id: string; label: string; keys: DisciplineKey[] }[] = [
  { id: 'temel', label: 'Temel tıp', keys: ['pat', 'farm', 'mikro', 'biyo', 'gen', 'fiz', 'ana'] },
  { id: 'dahili', label: 'Dahili', keys: ['ic', 'enf', 'noro', 'kardi', 'onko', 'cocuk', 'psik', 'ftr', 'acil'] },
  { id: 'cerrahi', label: 'Cerrahi', keys: ['cerr', 'kadin', 'uro'] },
  { id: 'toplum', label: 'Toplum sağlığı', keys: ['halk'] },
  { id: 'diger', label: 'Diğer', keys: ['diger'] },
];
const GROUP_OF = new Map<DisciplineKey, number>(DISCIPLINE_GROUPS.flatMap((g, i) => g.keys.map((k) => [k, i] as [DisciplineKey, number])));
export const disciplineGroupIndex = (name?: string | null) => GROUP_OF.get(disciplineKey(name)) ?? DISCIPLINE_GROUPS.length - 1;

/** Ders adlarını gruplar; grup içinde `count` azalan, eşitse ada göre. Boş gruplar dönmez. */
export function groupDisciplines<T>(items: T[], name: (x: T) => string, count: (x: T) => number) {
  const buckets = DISCIPLINE_GROUPS.map((g) => ({ ...g, items: [] as T[] }));
  for (const it of items) buckets[disciplineGroupIndex(name(it))].items.push(it);
  for (const b of buckets) b.items.sort((a, c) => count(c) - count(a) || name(a).localeCompare(name(c), 'tr'));
  return buckets.filter((b) => b.items.length > 0);
}
