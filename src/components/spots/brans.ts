/**
 * Sınav spotları › "En önemliler" ve "Soru çözücü" görünümlerinin branşları. Her branşın verisi ayrı klasörde:
 *   src/data/<id>_onem/{index,<kod>}.json   (önem listesi; patoloji: scripts/patoloji_onem, diğerleri: scripts/spot_cozucu/birlestir.py)
 *   src/data/<id>_cozucu/{index,<kod>}.json (sesli soru çözücü; sesler data/<id>_cozucu/ses, ses_<ses> →/api/cozucu-ses/<id>/…)
 * Ders kodları branşlar arasında tekildir (patoloji "07", enfeksiyon "e07", üroloji "u03"); "öğrendim" ve çözücü ilerlemesi koda bağlı.
 */
import branslarVeri from '../../data/dersler/branslar.json';

/** Kurul 1 branşları sabit; Kurul 2+ branşları kurul önekli klasörlerden (k2noroloji) kendiliğinden gelir. */
export type Brans = 'patoloji' | 'enfeksiyon' | 'uroloji' | 'genetik' | 'halksagligi' | 'kadindogum' | 'farmakoloji' | `k${number}${string}`;

export interface BransTanim {
  id: Brans;
  /** kısa ad (sekme, başlık) */
  ad: string;
  /** Kurul 1 ders adı */
  tam: string;
  /** "Tüm …" süzgecinin adı */
  hepsi: string;
  /** önem listesinde arama örneği */
  araOrnek: string;
  /** soru çözücü sayfasının açıklaması (soru türleri) */
  cozucuNot: string;
  /** sesli sınav asistanı var mı (düğme yalnız src/data/<id>_asistan verisi varsa görünür) */
  asistan: boolean;
  /** hocanın sınav kuralı kutusu (tablo/şekil/klinik bulgudan soru yok; slayt başına soru) — yalnız patoloji */
  sinavKurali: boolean;
}

const KURUL1_BRANSLAR: BransTanim[] = [
  {
    id: 'patoloji', ad: 'Patoloji', tam: 'Tıbbi Patoloji', hepsi: 'Tüm patoloji', araOrnek: 'nefrotik, meme, tromboz',
    cozucuNot: '2026-27 örnek soruları, aynı üslupta orta-zor benzer sorular ve konunun çıkmış soruları',
    asistan: true, sinavKurali: true,
  },
  {
    id: 'enfeksiyon', ad: 'Enfeksiyon', tam: 'Enfeksiyon Hastalıkları', hepsi: 'Tüm enfeksiyon', araOrnek: 'sifiliz, izolasyon, direnç',
    cozucuNot: 'çıkmış sorular ve çıkmışların üslubunda örnek sorular (çoğu orta, kolay ve zor da var), karışık',
    asistan: true, sinavKurali: false,
  },
  {
    id: 'uroloji', ad: 'Üroloji', tam: 'Üroloji', hepsi: 'Tüm üroloji', araOrnek: 'taş, obstrüksiyon, enürezis',
    cozucuNot: 'çıkmış sorular ve çıkmışların üslubunda örnek sorular (çoğu orta, kolay ve zor da var), karışık',
    asistan: true, sinavKurali: false,
  },
  {
    id: 'genetik', ad: 'Genetik', tam: 'Tıbbi Genetik', hepsi: 'Tüm genetik', araOrnek: 'kromozom, prenatal, doku tipleme',
    cozucuNot: 'çıkmış sorular ve çıkmışların üslubunda örnek sorular (çoğu orta, kolay ve zor da var), karışık',
    asistan: true, sinavKurali: false,
  },
  {
    id: 'halksagligi', ad: 'Halk Sağlığı', tam: 'Halk Sağlığı', hepsi: 'Tüm halk sağlığı', araOrnek: 'anne sütü, salgın, bebek ölüm',
    cozucuNot: 'çıkmış sorular ve çıkmışların üslubunda örnek sorular (çoğu orta, kolay ve zor da var), karışık',
    asistan: true, sinavKurali: false,
  },
  {
    id: 'kadindogum', ad: 'Kadın Doğum', tam: 'Kadın Hastalıkları ve Doğum', hepsi: 'Tüm kadın doğum', araOrnek: 'abortus, servikal yetmezlik, düşük',
    cozucuNot: 'çıkmış sorular ve çıkmışların üslubunda örnek sorular (çoğu orta, kolay ve zor da var), karışık',
    asistan: true, sinavKurali: false,
  },
  {
    id: 'farmakoloji', ad: 'Farmakoloji', tam: 'Tıbbi Farmakoloji', hepsi: 'Tüm farmakoloji', araOrnek: 'siklosporin, takrolimus, immünsüpresif',
    cozucuNot: 'çıkmış sorular ve çıkmışların üslubunda örnek sorular (çoğu orta, kolay ve zor da var), karışık',
    asistan: true, sinavKurali: false,
  },
];

// Kurul 2+: src/data/k<N><slug>_onem|_cozucu klasörü oluştuğu anda sekme görünür (ders zinciri üretir).
const VERI_KLASORLERI = Object.keys({
  ...import.meta.glob('../../data/k[2-6]*_onem/index.json'),
  ...import.meta.glob('../../data/k[2-6]*_cozucu/index.json'),
});
const SLUG_AD: Record<string, { ad: string; kisa: string }> = {
  ...Object.fromEntries((branslarVeri as any).branslar.map((b: any) => [b.slug, { ad: b.ad, kisa: b.kisa }])),
  // Hocanın üslubunda sorular (scripts/patoloji_soru_isci): ayrı çözücü branşı, branslar.json'da yok
  patolojihoca: { ad: 'Tıbbi Patoloji · Hoca soruları', kisa: 'Patoloji Hoca' },
  // Sesli derste slayt arası "hocanın sorabileceği" sorular (scripts/hoca_ara_soru), tüm dersler
  hocaara: { ad: 'Hocanın sorabileceği sorular', kisa: 'Hoca sorabilir' },
};
const sonrakiKurullar: BransTanim[] = [...new Set(VERI_KLASORLERI.map((p) => /\/(k[2-6][a-z]+)_(onem|cozucu)\//.exec(p)?.[1]).filter(Boolean) as string[])]
  .sort()
  .map((id) => {
    const kurul = id[1];
    const t = SLUG_AD[id.slice(2)] || { ad: id.slice(2), kisa: id.slice(2) };
    return {
      id: id as Brans, ad: `${t.kisa} · K${kurul}`, tam: `Kurul ${kurul} ${t.ad}`, hepsi: `Tüm ${t.kisa.toLocaleLowerCase('tr')} (Kurul ${kurul})`,
      araOrnek: 'konu, terim, hastalık',
      cozucuNot: 'çıkmış sorular ve çıkmışların üslubunda örnek sorular (çoğu orta, kolay ve zor da var), karışık',
      asistan: true, sinavKurali: false,
    };
  });

export const BRANSLAR: BransTanim[] = [...KURUL1_BRANSLAR, ...sonrakiKurullar];

export const bransTanim = (b: Brans): BransTanim => BRANSLAR.find((x) => x.id === b) || BRANSLAR[0];
export const bransOku = (s: string | null | undefined): Brans => (BRANSLAR.some((x) => x.id === s) ? (s as Brans) : 'patoloji');
