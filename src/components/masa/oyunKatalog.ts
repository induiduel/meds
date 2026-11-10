/** Oyun kataloğu: kategoriler ve sıra. Merkez kartları, kural sekmeleri ve "Nasıl oynanır" kısayolları buradan dizilir. */
import { type OyunTur, type UnoMod } from '../../services/masa/tipler';

export interface Kategori { id: string; ad: string; alt: string; turler: OyunTur[] }

/** Sıra: en çok oynanandan az bilinene; her kategoride ilk oyun o ailenin en tanıdığı */
export const KATEGORILER: Kategori[] = [
  { id: 'okey', ad: 'Okey', alt: 'Istakalı klasikler: per aç, taş işle ya da çek-at.', turler: ['yedili', 'takim', 'duz', 'yuzbir'] },
  { id: 'acik', ad: 'Açık masa', alt: 'Taş atılmaz; okey taşları masada dizilir, yeniden kurulur.', turler: ['kastet', 'remi', 'domino'] },
  { id: 'kart', ad: 'Kart oyunları', alt: 'Uno destesi ve 52’lik iskambil.', turler: ['uno', 'pisti'] },
  { id: 'tahta', ad: 'Tahta oyunları', alt: 'İki kişilik; arkadaşınla ya da bota karşı.', turler: ['go', 'cizgi', 'xox'] },
];
export const OYUN_SIRA: OyunTur[] = KATEGORILER.flatMap((k) => k.turler);
export const kategoriAdi = (tur: OyunTur) => KATEGORILER.find((k) => k.turler.includes(tur))?.ad || 'Oyun';

export const OYUN_CUMLE: Record<OyunTur, string> = {
  yedili: 'Yedi taşla başla, per aç, masadaki perlere işle; elini ilk bitiren kazanır.',
  takim: 'Yedili’nin eşli hâli: karşındaki ortağınla aynı perlere işle, birlikte bitir.',
  duz: 'Çek, at, elini perlere ya da yedi çifte ayırıp son taşla bitir: herkesin bildiği okey.',
  yuzbir: 'Okeyli klasik: 101 sayıyla ya da beş çiftle aç, taşlarını erit, son taşını at.',
  kastet: 'Taş atmadan açtıkça aç; masadaki taşları elindekilerle yeniden dizdiğin ortak masa okeyi.',
  remi: 'Elinden 30 ile aç, sonra masadaki bütün perleri yeniden kur; ilk bitiren kazanır.',
  domino: 'Okey taşlarıyla domino: rengi ya da sayısı tutan taşı zincire ekle, ardışık koyup ek hamle kazan.',
  uno: 'Rengi ya da sayıyı tuttur, kartlarını bitir. Resmî kurallar ya da Yığma, 7-0, Atlama gibi modlar.',
  pisti: 'Yerdeki kartı eşle, Vale ile topla, tek karta pişti yap: klasik Pişti 2 ya da 4 kişiyle.',
  go: 'Ahşap tahtada alan kapma: taşlarla çevir, grupları al. 9×9, 13×13, 19×19; handikap ve süre.',
  cizgi: 'Zar at, çizgini kare kare rakibin kalesine sür. Yüz yüze gelince iki zarla kapışma.',
  xox: 'Klasik üçlü dizi; 4×4’ten 6×6’ya büyük tahtalarda dörtlü, beşli dizi.',
};

export const oyuncuYazi = ([enAz, enCok]: readonly [number, number]) => (enAz === enCok ? `${enAz} oyuncu` : `${enAz}–${enCok} oyuncu`);

/** Uno mod kartlarındaki kısa tanıtım (uzun açıklama: tipler.ts UNO_MODLAR) */
export const UNO_MOD_KISA: Record<UnoMod, string> = {
  klasik: 'Resmî kurallar',
  yigma: '+2 ve +4 birikir',
  yediSifir: '7 ve 0 el değiştirir',
  atlama: 'Tıpkısıyla araya gir',
  hizli: '5 kartla kısa el',
  cekCek: 'Uyan gelene dek çek',
};
