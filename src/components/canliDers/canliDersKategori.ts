/**
 * Canlı ders listesi · konu kategorileri. Ders başlığından anahtar sözcükle belirlenir (yeni ders eklenince de
 * kendiliğinden yerine düşer). Kurallar SIRAYLA denenir: organ kategorileri tümörden önce gelir ("Böbrek Tümörleri"
 * böbrekte kalsın), tümör genetikten önce ("Tümör Genetiği"), beslenme gebelikten önce.
 */
import type { CdListeDers } from './canliDersStore';

export interface CdKategori { id: string; ad: string; kisa: string; alt: string; re: RegExp | null }

const fold = (s: string) =>
  s.toLocaleLowerCase('tr').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ı/g, 'i');

/** Dizilim = sayfadaki sıra (genel → sistemler → halk sağlığı) */
const KATEGORILER: CdKategori[] = [
  { id: 'hucre', ad: 'Hücre hasarı ve adaptasyon', kisa: 'Hücre', alt: 'Patolojiye giriş, nekroz, birikimler', re: /hucre|patolojiye giris|birikim|yaslanma/ },
  { id: 'enflamasyon', ad: 'Enflamasyon ve hemodinamik', kisa: 'Enflamasyon', alt: 'Enflamasyon, onarım, ödem, tromboz, şok', re: /enflamasyon|onarim|odem|tromboz|emboli/ },
  { id: 'immun', ad: 'İmmünoloji', kisa: 'İmmünoloji', alt: 'Aşırı duyarlılık, otoimmünite, immünofarmakoloji', re: /duyarlilik|immun/ },
  { id: 'tumor', ad: 'Tümör biyolojisi', kisa: 'Tümör', alt: 'Neoplazi, karsinojenez, evreleme', re: /tumor|karsinojen|neoplazi|kanser/ },
  { id: 'genetik', ad: 'Genetik, gebelik ve prenatal', kisa: 'Genetik · Gebelik', alt: 'Kromozom, prenatal tanı, gebelik', re: /gebelik|prenatal|preimplant|abortus|kromozom|dismorfoloji|genetik/ },
  { id: 'bobrek', ad: 'Böbrek ve üriner sistem', kisa: 'Böbrek', alt: 'Glomerüler, tübüler, taş, mesane', re: /bobrek|glomerul|tubul|obstruksiyon|urolit|mesane|enurez/ },
  { id: 'genital', ad: 'Genital sistem ve meme', kisa: 'Genital · Meme', alt: 'Kadın ve erkek genital, meme', re: /vulva|serviks|endometri|uterus|ovidukt|ovaryum|meme|erkek genital|prostat/ },
  { id: 'enfeksiyon', ad: 'Enfeksiyon ve mikrobiyoloji', kisa: 'Enfeksiyon', alt: 'ÜSE, CYBE, epidemiyoloji, direnç', re: /enfeksiyon|sifiliz|izolasyon|akinti|direnc|cinsel yolla/ },
  { id: 'halk', ad: 'Halk sağlığı ve beslenme', kisa: 'Halk sağlığı', alt: 'Beslenme, salgın, sağlık hizmetleri', re: /beslen|halk sagligi|saglik hizmet|salgin|ana cocuk/ },
  { id: 'diger', ad: 'Diğer dersler', kisa: 'Diğer', alt: '', re: null },
];

/** Eşleme sırası (dizilimden ayrı): önce dar/organ kuralları */
const SIRA = ['halk', 'bobrek', 'genital', 'tumor', 'enfeksiyon', 'genetik', 'immun', 'enflamasyon', 'hucre'];
const byId = new Map(KATEGORILER.map((k) => [k.id, k]));

export function cdKategori(baslik: string): CdKategori {
  const f = fold(baslik);
  for (const id of SIRA) {
    const k = byId.get(id)!;
    if (k.re!.test(f)) return k;
  }
  return byId.get('diger')!;
}

const noSayi = (d: CdListeDers) => Number(d.no) || 9999;

/** Boş kategoriler düşer; her grupta ders numarasına göre sıralı */
export function cdKategoriGrupla(ds: CdListeDers[]): { kat: CdKategori; dersler: CdListeDers[] }[] {
  const m = new Map<string, CdListeDers[]>();
  for (const d of ds) {
    const id = cdKategori(d.baslik).id;
    (m.get(id) || m.set(id, []).get(id)!).push(d);
  }
  return KATEGORILER.filter((k) => m.has(k.id)).map((k) => ({ kat: k, dersler: m.get(k.id)!.sort((a, b) => noSayi(a) - noSayi(b)) }));
}
