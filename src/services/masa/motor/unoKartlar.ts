/**
 * Uno desteleri ve kart puanları (mod başına). Saf veri + kurucu; motor (sunucu), sınama ve kural sayfası aynı tabloyu okur.
 * Kaynak: Mattel yönerge sayfaları (Flip GDR44, All Wild HHL33, No Mercy HVW18, Attack/Extreme GXY81, Teams HXT58, Flex HMY99,
 * Deluxe HGL63, Express, Liar's JLH43). Yönergede sayısı yazmayan kartlarda (No Mercy renkli aksiyonlar, Flex dağılımı) toplamı
 * tutturan en yaygın döküm kullanılır; `UNO_DESTE_DOKUM` kural sayfasında aynen gösterilir.
 */
import type { Rng, UnoDeger, UnoKart, UnoMod, UnoRenk, UnoYuz } from '../tipler';

const RENKLER: readonly UnoRenk[] = ['k', 's', 'y', 'm'];
const SAYI = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] as const;
const sayiMi = (d: UnoDeger) => d.length === 1;

/** Bir deste satırı: renk başına (renkli: true) ya da toplam adet */
export interface DesteSatir { deger: UnoDeger; adet: number; renkli: boolean; ek?: Partial<UnoYuz>; ad?: string }

const klasik108: DesteSatir[] = [
  { deger: '0', adet: 1, renkli: true },
  ...SAYI.slice(1).map((v) => ({ deger: v as UnoDeger, adet: 2, renkli: true })),
  { deger: 'pas', adet: 2, renkli: true }, { deger: 'yon', adet: 2, renkli: true }, { deger: '+2', adet: 2, renkli: true },
  { deger: 'joker', adet: 4, renkli: false }, { deger: '+4', adet: 4, renkli: false },
];
const birDokuz = (adet: number, ek?: Partial<UnoYuz>): DesteSatir[] => SAYI.slice(1).map((v) => ({ deger: v as UnoDeger, adet, renkli: true, ek }));

/** Flip: açık ve koyu yüz dökümleri ayrı; kartlar rastgele eşlenir */
export const FLIP_ACIK: DesteSatir[] = [
  ...birDokuz(2),
  { deger: '+1', adet: 2, renkli: true }, { deger: 'yon', adet: 2, renkli: true }, { deger: 'pas', adet: 2, renkli: true }, { deger: 'flip', adet: 2, renkli: true },
  { deger: 'joker', adet: 4, renkli: false }, { deger: 'joker+2', adet: 4, renkli: false },
];
export const FLIP_KOYU: DesteSatir[] = [
  ...birDokuz(2, { t: 'k' }),
  { deger: '+5', adet: 2, renkli: true, ek: { t: 'k' } }, { deger: 'yon', adet: 2, renkli: true, ek: { t: 'k' } },
  { deger: 'pasHerkes', adet: 2, renkli: true, ek: { t: 'k' } }, { deger: 'flip', adet: 2, renkli: true, ek: { t: 'k' } },
  { deger: 'joker', adet: 4, renkli: false, ek: { t: 'k' } }, { deger: 'jokerRenk', adet: 4, renkli: false, ek: { t: 'k' } },
];

export const UNO_DESTE_DOKUM: Record<UnoMod, DesteSatir[]> = {
  klasik: klasik108, yigma: klasik108, yediSifir: klasik108, cekCek: klasik108, atlama: klasik108, hizli: klasik108,
  deluxe: [...klasik108.slice(0, -2), { deger: 'joker', adet: 8, renkli: false }, { deger: '+4', adet: 4, renkli: false }],
  express: [
    ...SAYI.map((v) => ({ deger: v as UnoDeger, adet: 1, renkli: true })),
    { deger: '+1', adet: 1, renkli: true }, { deger: 'yon', adet: 1, renkli: true }, { deger: 'pas', adet: 1, renkli: true },
    { deger: 'joker', adet: 2, renkli: false }, { deger: 'joker+2', adet: 2, renkli: false },
  ],
  flip: FLIP_ACIK,
  hepsiJoker: [
    { deger: 'joker', adet: 54, renkli: false }, { deger: 'jokerYon', adet: 14, renkli: false }, { deger: 'jokerPas', adet: 14, renkli: false },
    { deger: 'jokerPas2', adet: 6, renkli: false }, { deger: 'joker+2', adet: 10, renkli: false }, { deger: '+4', adet: 6, renkli: false },
    { deger: 'jokerHedef2', adet: 4, renkli: false }, { deger: 'jokerTakas', adet: 4, renkli: false },
  ],
  noMercy: [
    ...SAYI.map((v) => ({ deger: v as UnoDeger, adet: 2, renkli: true })),
    { deger: 'pas', adet: 3, renkli: true }, { deger: 'yon', adet: 3, renkli: true }, { deger: 'hepsiAt', adet: 3, renkli: true },
    { deger: 'pasHerkes', adet: 2, renkli: true }, { deger: '+2', adet: 3, renkli: true }, { deger: 'r+4', adet: 2, renkli: true },
    { deger: 'jokerYon4', adet: 8, renkli: false }, { deger: '+6', adet: 4, renkli: false }, { deger: '+10', adet: 4, renkli: false }, { deger: 'rulet', adet: 8, renkli: false },
  ],
  extreme: [
    ...birDokuz(2),
    { deger: 'yon', adet: 1, renkli: true }, { deger: 'pas', adet: 2, renkli: true }, { deger: 'hepsiAt', adet: 2, renkli: true },
    { deger: 'vur1', adet: 1, renkli: true }, { deger: 'vur2', adet: 2, renkli: true },
    { deger: 'joker', adet: 4, renkli: false }, { deger: 'jokerVur', adet: 4, renkli: false },
  ],
  takim: [
    ...(['1', '2', '3', '4', '5'] as const).flatMap((v): DesteSatir[] => [{ deger: v, adet: 1, renkli: true }, { deger: v, adet: 1, renkli: true, ek: { ps: 1 }, ad: 'paslaşma simgeli' }]),
    ...(['6', '7', '8', '9'] as const).map((v): DesteSatir => ({ deger: v, adet: 2, renkli: true })),
    { deger: '+2', adet: 2, renkli: true }, { deger: 'yon', adet: 2, renkli: true }, { deger: 'pas', adet: 2, renkli: true },
    { deger: 'joker', adet: 4, renkli: false }, { deger: 'jokerTakim', adet: 8, renkli: false }, { deger: 'jokerTakim4', adet: 4, renkli: false },
  ],
  // Flex: flex rengi kurucuda atanır (aşağıda); 4 ve 8'in düz kopyaları güç kartını çevirir
  flex: [
    ...(['1', '2', '3', '4', '5', '6', '7', '8'] as const).flatMap((v): DesteSatir[] => [
      { deger: v, adet: 1, renkli: true, ek: v === '4' || v === '8' ? { cv: 1 } : undefined },
      { deger: v, adet: 1, renkli: true, ek: { fx: 'j' }, ad: 'flex' },
    ]),
    ...(['+2', 'pas', 'yon'] as const).flatMap((v): DesteSatir[] => [{ deger: v, adet: 1, renkli: true }, { deger: v, adet: 1, renkli: true, ek: { fx: 'j' }, ad: 'flex' }]),
    { deger: 'fxHerkes', adet: 4, renkli: false, ek: { fx: 'j' } }, { deger: 'fxHedef2', adet: 4, renkli: false, ek: { fx: 'j' } },
    { deger: 'fx+4', adet: 2, renkli: false, ek: { fx: 'j' } }, { deger: 'jokerCevir', adet: 6, renkli: false },
  ],
  yalanci: [
    ...SAYI.flatMap((v): DesteSatir[] => [{ deger: v, adet: 1, renkli: true }, { deger: v, adet: 1, renkli: true, ek: { yl: 1 }, ad: 'yalancı' }]),
    { deger: '+2', adet: 2, renkli: true, ek: { yl: 1 } }, { deger: 'yon', adet: 2, renkli: true, ek: { yl: 1 } }, { deger: 'pas', adet: 2, renkli: true, ek: { yl: 1 } },
    { deger: '+4', adet: 2, renkli: false, ek: { yl: 1 } }, { deger: 'jokerMeydan', adet: 6, renkli: false },
  ],
  dostlar: [
    ...klasik108,
    { deger: 'kitty', adet: 2, renkli: false }, { deger: 'batman', adet: 2, renkli: false }, { deger: 'kuromi', adet: 2, renkli: false }, { deger: 'pony', adet: 2, renkli: false },
  ],
};

/** Flex kartının ikinci rengi: kendi renginden farklı, sayıya/simgeye göre sabit */
export function flexRenk(renk: UnoRenk, deger: UnoDeger): UnoRenk {
  const kay = deger === '+2' ? 1 : deger === 'pas' ? 2 : deger === 'yon' ? 3 : (Number(deger) % 3) + 1;
  return RENKLER[(RENKLER.indexOf(renk) + kay) % 4];
}

function yuzler(dokum: DesteSatir[]): UnoYuz[] {
  const out: UnoYuz[] = [];
  for (const s of dokum) {
    if (s.renkli) for (const r of RENKLER) for (let i = 0; i < s.adet; i++) out.push({ renk: r, deger: s.deger, ...s.ek, ...(s.ek?.fx ? { fx: flexRenk(r, s.deger) } : {}) });
    else for (let i = 0; i < s.adet; i++) out.push({ renk: null, deger: s.deger, ...s.ek });
  }
  return out;
}

/** Karılmamış deste; kimlik = dizin. Flip'te her karta rastgele bir koyu yüz eşlenir (`rng` yalnız bunun için). */
export function unoDesteKur(mod: UnoMod, rng?: Rng): UnoKart[] {
  const on = yuzler(UNO_DESTE_DOKUM[mod] ?? klasik108);
  if (mod !== 'flip') return on.map((y, id) => ({ id, ...y }));
  const arka = yuzler(FLIP_KOYU);
  const r = rng ?? (() => 0.5);
  for (let i = arka.length - 1; i > 0; i--) { const x = Math.floor(r() * (i + 1)); const j = x >= 0 && x <= i ? x : 0; [arka[i], arka[j]] = [arka[j], arka[i]]; }
  return on.map((y, id) => ({ id, ...y, arka: arka[id] }));
}

/** Joker çekme / renkli çekme kartlarının çektirdiği kart sayısı (0 = çekme kartı değil) */
export const CEKME: Partial<Record<UnoDeger, number>> = { '+1': 1, '+2': 2, 'r+4': 4, '+4': 4, '+5': 5, 'joker+2': 2, jokerYon4: 4, '+6': 6, '+10': 10, jokerTakim4: 2, 'fx+4': 4 };
/** Extreme: vur kartlarının basış sayısı */
export const VURUS: Partial<Record<UnoDeger, number>> = { vur1: 1, vur2: 2, jokerVur: 2 };

/** El sonu puan değeri (mod başına resmî tablo) */
export function kartPuani(kart: UnoYuz, mod: UnoMod = 'klasik'): number {
  const d = kart.deger;
  if (sayiMi(d)) return Number(d);
  if (mod === 'flip') return d === '+1' ? 10 : d === 'pasHerkes' ? 30 : d === 'joker' ? 40 : d === 'joker+2' ? 50 : d === 'jokerRenk' ? 60 : 20;
  if (mod === 'hepsiJoker') return d === 'joker' ? 20 : 50;
  if (mod === 'extreme') return kart.renk === null ? 50 : d === 'hepsiAt' ? 30 : d === 'vur2' ? 40 : 20;
  return kart.renk === null ? 50 : 20;
}
