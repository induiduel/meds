/** Ders içerik paketi (scripts/ders_icerik_uret.py → src/data/ders_icerik/<key>.json): terim, hastalık, bilgi, tablo, kart, örnek soru. */
/** adim: ait olduğu Öğren slayt numarası (0 = eşlenemedi → PDF'te 'Ek'); scripts/ders_icerik_adim.py yazar. */
export interface DiAdim { adim?: number }
export interface DiTerim extends DiAdim { t: string; a: string; i: string; e: string[]; s?: number }
export interface DiHastalik extends DiAdim { id: string; ad: string; latin: string; kat: string; bolumler: { b: string; m: { m: string; s?: number | null }[] }[]; s: number[] }
export interface DiTablo extends DiAdim { t: string; h: string[]; r: string[][]; n: number; k?: string }
export interface DiOnemli extends DiAdim { p: number; b: string; m: string; alt: string[]; n: string; s: number[]; tur?: string }
/** sira: numara (1,2,3) | alfa (a,b,c) | azalan (büyükten küçüğe) | madde (sırasız) */
export interface DiListe extends DiAdim { t: string; sira: 'numara' | 'alfa' | 'azalan' | 'madde'; m: { m: string; alt?: { m: string }[] }[]; n: number; a?: string }
export interface DiQuiz extends DiAdim { q: string; o: { k: string; t: string; d: boolean; a: string }[]; n: number }
export interface DiPaket {
  key: string; baslik?: string; ozet?: string;
  terimler: DiTerim[]; kisaltmalar: (DiAdim & { k: string; acilim: string })[]; hastaliklar: DiHastalik[];
  bilgiler: (DiAdim & { b: string; m: string; s?: number })[]; onemli: DiOnemli[]; spotlar: (DiAdim & { m: string; n: number; bolum: string })[];
  tablolar: DiTablo[]; listeler: DiListe[]; quiz: DiQuiz[]; cikmis?: number; kartlar: (DiAdim & { o: string; a: string; c: string; n: number })[];
}
export interface DiSoru { id: string; kazanim: number; zorluk: string; soru: string; secenekler: Record<string, string>; dogru: string; aciklama: string }

const PAKETLER = import.meta.glob('../../data/ders_icerik/*.json') as Record<string, () => Promise<{ default: DiPaket }>>;
const SORULAR = import.meta.glob('../../data/ornek_sorular/*/*.json') as Record<string, () => Promise<{ default: { kazanimlar: { no: number; metin: string; sorular: DiSoru[] }[] } }>>;
const anahtar = (key: string) => key.replace(/-v\d+$/, '');
const bul = <T,>(m: Record<string, T>, key: string) => Object.entries(m).find(([p]) => p.endsWith(`/${anahtar(key)}.json`))?.[1];

export const dersIcerikVar = (key: string) => !!bul(PAKETLER, key);
export const dersIcerikGetir = async (key: string) => (await bul(PAKETLER, key)?.())?.default || null;
export const dersSorulariGetir = async (key: string): Promise<{ no: number; metin: string; sorular: DiSoru[] }[]> =>
  (await bul(SORULAR, key)?.())?.default.kazanimlar || [];

export type DiBolum = 'terimler' | 'hastaliklar' | 'bilgiler' | 'listeler' | 'tablolar' | 'sorular' | 'quiz' | 'kartlar';
export const DI_BOLUMLER: { id: DiBolum; ad: string }[] = [
  { id: 'terimler', ad: 'Terimler ve kısaltmalar' }, { id: 'hastaliklar', ad: 'Hastalıklar ve kavramlar' },
  { id: 'bilgiler', ad: 'Bilgi spotları' }, { id: 'listeler', ad: 'Sıralamalar ve listeler' }, { id: 'tablolar', ad: 'Tablolar ve karşılaştırmalar' },
  { id: 'sorular', ad: 'Örnek sorular' }, { id: 'quiz', ad: 'Mini sorular' }, { id: 'kartlar', ad: 'Hatırlatma kartları' },
];

/** PDF için ders slaytları (Öğren destesi; anlatım metni + sırası). */
export interface DiSlayt { slideNumber: number; title: string; subtitle?: string; badge?: string; bolum?: string; synthesisNarrative?: string; content?: string; isCheckpoint?: boolean; isGameFinale?: boolean; pdfSayfalari?: number[] }
const DESTELER = import.meta.glob('../../data/decks/items/*.json', { import: 'default' }) as Record<string, () => Promise<{ slides: DiSlayt[]; title?: string }>>;
export const dersSlaytlariGetir = async (key: string) => (await Object.entries(DESTELER).find(([p]) => p.endsWith(`/k2p-${anahtar(key)}.json`))?.[1]?.()) || null;
