/** Ders içerik paketi (scripts/ders_icerik_uret.py → src/data/ders_icerik/<key>.json): terim, hastalık, bilgi, tablo, kart, örnek soru. */
export interface DiTerim { t: string; a: string; i: string; e: string[]; s?: number }
export interface DiHastalik { id: string; ad: string; latin: string; kat: string; bolumler: { b: string; m: string[] }[]; s: number[] }
export interface DiTablo { t: string; h: string[]; r: string[][]; n: number; k?: string }
export interface DiOnemli { p: number; b: string; m: string; alt: string[]; n: string; s: number[] }
export interface DiPaket {
  key: string; baslik?: string; ozet?: string;
  terimler: DiTerim[]; kisaltmalar: { k: string; acilim: string }[]; hastaliklar: DiHastalik[];
  bilgiler: { b: string; m: string; s?: number }[]; onemli: DiOnemli[]; spotlar: { m: string; n: number; bolum: string }[];
  tablolar: DiTablo[]; kartlar: { o: string; a: string; c: string; n: number }[];
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

export type DiBolum = 'terimler' | 'hastaliklar' | 'bilgiler' | 'tablolar' | 'sorular' | 'kartlar';
export const DI_BOLUMLER: { id: DiBolum; ad: string }[] = [
  { id: 'terimler', ad: 'Terimler ve kısaltmalar' }, { id: 'hastaliklar', ad: 'Hastalıklar ve bulgular' },
  { id: 'bilgiler', ad: 'Bilgi spotları' }, { id: 'tablolar', ad: 'Tablolar ve karşılaştırmalar' },
  { id: 'sorular', ad: 'Örnek sorular' }, { id: 'kartlar', ad: 'Hatırlatma kartları' },
];
