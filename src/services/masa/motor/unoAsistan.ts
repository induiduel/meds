/**
 * Uno — saf yardımcılar. Motor (sunucu) ve istemci (ipucu, el dizilişi, erişilebilirlik adı) aynı işlevleri kullanır.
 * Yan etki yok; yalnız `tipler.ts` türleri.
 */
import type { UnoDeger, UnoGorunum, UnoHamle, UnoKart, UnoMod, UnoRenk, UnoYuz } from '../tipler';
import { CEKME, kartPuani } from './unoKartlar';

export const UNO_RENKLER: readonly UnoRenk[] = ['k', 's', 'y', 'm'];
export const UNO_DEGERLER: readonly UnoDeger[] = [
  '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'pas', 'pasHerkes', 'yon', '+1', '+2', 'r+4', '+5', 'vur1', 'vur2', 'hepsiAt', 'flip',
  'joker', 'jokerYon', 'jokerPas', 'jokerPas2', 'joker+2', '+4', 'jokerYon4', '+6', '+10', 'jokerRenk', 'rulet', 'jokerHedef2', 'jokerTakas', 'jokerVur',
  'jokerTakim', 'jokerTakim4', 'jokerCevir', 'fxHerkes', 'fxHedef2', 'fx+4', 'jokerMeydan', 'kitty', 'batman', 'kuromi', 'pony',
];

export const UNO_RENK_AD: Record<UnoRenk, string> = { k: 'Kırmızı', s: 'Sarı', y: 'Yeşil', m: 'Mavi' };
/** Flip koyu yüz renk adları */
export const UNO_KOYU_RENK_AD: Record<UnoRenk, string> = { k: 'Pembe', s: 'Turuncu', y: 'Turkuaz', m: 'Mor' };
export const UNO_DEGER_AD: Record<UnoDeger, string> = {
  '0': 'Sıfır', '1': 'Bir', '2': 'İki', '3': 'Üç', '4': 'Dört', '5': 'Beş', '6': 'Altı', '7': 'Yedi', '8': 'Sekiz', '9': 'Dokuz',
  pas: 'Atlat', yon: 'Yön değiştir', '+2': 'İki çek', joker: 'Joker', '+4': 'Joker dört çek',
  '+1': 'Bir çek', flip: 'Flip', 'joker+2': 'Joker iki çek', '+5': 'Beş çek', pasHerkes: 'Herkesi atlat', jokerRenk: 'Joker renk gelene dek çek',
  jokerYon: 'Joker yön', jokerPas: 'Joker atlat', jokerPas2: 'Joker ikili atlat', jokerHedef2: 'Joker hedefli iki çek', jokerTakas: 'Joker zorunlu takas',
  hepsiAt: 'Hepsini at', 'r+4': 'Dört çek', jokerYon4: 'Joker yön ve dört çek', '+6': 'Joker altı çek', '+10': 'Joker on çek', rulet: 'Joker renk ruleti',
  vur1: 'Bir vur', vur2: 'İki vur', jokerVur: 'Joker çifte saldırı',
  jokerTakim: 'Joker takım oyunu', jokerTakim4: 'Joker takıma dört çek',
  jokerCevir: 'Joker güçleri çevir', fxHerkes: 'Flex joker herkes çeker', fxHedef2: 'Flex joker hedefli iki çek', 'fx+4': 'Flex joker dört çek',
  jokerMeydan: 'Joker yalancı meydan okuması',
  kitty: 'Kedicik hediye paketi', batman: 'Yarasa gece siperi', kuromi: 'Yaramaz tavşan şakası', pony: 'Gökkuşağı tayı',
};

export const sayiKartiMi = (k: UnoYuz): boolean => k.deger.length === 1;
/** 7 = takas, 0 = devir olan modlar */
export const UNO_TAKAS_MODLAR: readonly UnoMod[] = ['yediSifir', 'noMercy', 'yalanci'];
/** Yalancı modunda kapalı oynarken söylenebilecek değerler */
export const UNO_BEYAN_DEGERLER: readonly UnoDeger[] = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+2', 'yon', 'pas', '+4'];

/** Hedef (rakip) seçilen kart mı. 7: takas modlarında; hedef verilmezse motor en az kartlı rakibi seçer. */
export function hedefGerek(mod: UnoMod, deger: UnoDeger, flex: boolean): boolean {
  return deger === 'jokerHedef2' || deger === 'jokerTakas' || deger === 'jokerVur' || deger === 'kitty'
    || (flex && (deger === 'fxHedef2' || deger === 'fx+4')) || (deger === '7' && UNO_TAKAS_MODLAR.includes(mod));
}
/** Oynarken renk seçilen kart mı (Hepsi Joker'de renk yok; Renk Ruleti'nde rengi sıradaki seçer) */
export const renkGerek = (mod: UnoMod, kart: UnoYuz): boolean => kart.renk === null && mod !== 'hepsiJoker' && kart.deger !== 'rulet';

/** Aktif renk, üstteki kartla aynı değer/simge ya da joker (her zaman). */
export function oynanabilirMi(kart: UnoYuz, ust: UnoYuz, aktifRenk: UnoRenk): boolean {
  return kart.renk === null || kart.renk === aktifRenk || kart.deger === ust.deger;
}

/** El sonu puan değeri (mod başına resmî tablo; klasik: sayı = yüz değeri, renkli aksiyon 20, joker 50) */
export const kartDegeri = (kart: UnoYuz, mod: UnoMod = 'klasik'): number => kartPuani(kart, mod);

/** Sıralı kart kimlikleri: renk (k,s,y,m) → değer; jokerler sonda */
export function elSirala(el: UnoKart[]): number[] {
  const anahtar = (k: UnoKart) => (k.renk === null ? 4 : UNO_RENKLER.indexOf(k.renk)) * 100 + UNO_DEGERLER.indexOf(k.deger);
  return [...el].sort((a, b) => anahtar(a) - anahtar(b) || a.id - b.id).map((k) => k.id);
}

/** Belirlenimci [0,1) karma (FNV-1a): botun yakalama kararı aynı durumda hep aynı çıkar */
export function karma(s: string): number {
  let h = 0x811c9dc5;
  for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 0x01000193); }
  return (h >>> 0) / 4294967296;
}

type Oneri = { hamle: UnoHamle; aciklama: string };
const kucuk = (s: string) => s.toLocaleLowerCase('tr');

/** Zarar veren hedefli kartlar ve takas için rakip: en az kartlı (takımda ortak hariç) */
function hedefSec(g: UnoGorunum, ben: string): string | undefined {
  const benim = g.oyuncular.find((o) => o.id === ben);
  return g.oyuncular
    .filter((o) => o.id !== ben && !o.elendi && !o.cikti && (benim?.takim === undefined || o.takim !== benim.takim))
    .sort((a, b) => a.kartSayisi - b.kartSayisi)[0]?.id;
}

/**
 * Yalnız sıra hamlesi (oyna / çek / pas) ve sırası gelenin kararları. Bot ve asistan aynı mantığı kullanır; sıra `ben`de değilse null.
 * `blof` (0–1): Yalancı modunda botun blöf zarı; verilmezse (asistan) blöf önerilmez.
 */
export function siraOnerisi(g: UnoGorunum, ben: string, blof?: number): Oneri | null {
  if (g.bitti) return null;
  const mod = g.mod;
  const sayim: Record<UnoRenk, number> = { k: 0, s: 0, y: 0, m: 0 };
  for (const k of g.elim) if (k.renk) sayim[k.renk]++;
  const enCok = (): UnoRenk => { let r: UnoRenk = g.aktifRenk; for (const x of UNO_RENKLER) if (sayim[x] > sayim[r]) r = x; return r; };
  const renkAd = (r: UnoRenk) => kucuk((g.taraf === 'k' ? UNO_KOYU_RENK_AD : UNO_RENK_AD)[r]);
  const b = g.bekle;
  if (g.ver) {
    const sirali = [...g.elim].sort((x, y) => kartPuani(y, mod) - kartPuani(x, mod) || x.id - y.id);
    const kart = g.ver.neden === 'hediye' ? sirali[0] : sirali[sirali.length - 1];
    return kart ? { hamle: { t: 'ver', kart: kart.id }, aciklama: g.ver.neden === 'hediye' ? 'Hediye: en pahalı kartını ver, elin hafiflesin.' : 'Ortağına en değersiz kartını ver; jokerlerini kendine sakla.' } : null;
  }
  if (b) {
    if ((b.tur === 'renk' || b.tur === 'rulet') && b.kim === ben) {
      const renk = enCok();
      return { hamle: { t: 'renk', renk }, aciklama: b.tur === 'rulet' ? `Renk Ruleti: seçtiğin renk gelene dek kart açılır. Elinde en çok ${renkAd(renk)} var, onu seç.` : `Elinde en çok ${renkAd(renk)} var, onu seç.` };
    }
    if (b.tur === 'itiraz' && b.hedef === ben) {
      return { hamle: { t: 'kabul' }, aciklama: b.kart === 'jokerRenk'
        ? 'Kabul edersen seçilen renk gelene dek çekersin. İtiraz edersen: oynayanın elinde önceki renkten kart varsa o çeker, yoksa sen 2 kart fazlasını çekersin.'
        : `Kabul edersen ${b.kart === 'joker+2' ? 2 : 4} çekersin. İtiraz edersen: oynayanın elinde önceki renkten kart varsa o çeker, yoksa sen 2 kart fazlasını çekersin.` };
    }
    if (b.tur === 'yalan' && b.karar === ben) return { hamle: { t: 'inan' }, aciklama: 'Emin değilsen inan. “Yalan!” dersen: kart söylenen gibiyse sen 1 kart çekersin, değilse o kartı geri alıp 1 kart çeker.' };
    if (b.tur === 'meydan' && b.asama === 'koy' && b.koymayan.includes(ben)) {
      const dogru = g.elim.filter((k) => k.renk === b.renk).sort((x, y) => kartPuani(y, mod) - kartPuani(x, mod))[0];
      const kart = dogru ?? [...g.elim].sort((x, y) => kartPuani(y, mod) - kartPuani(x, mod))[0];
      return kart ? { hamle: { t: 'koy', kart: kart.id }, aciklama: dogru ? `Elinde ${renkAd(b.renk)} var: onu kapalı koy, sorgulansan da kurtulursun.` : `Elinde ${renkAd(b.renk)} yok: en pahalı kartını kapalı koy ve sorgulanmamayı um.` } : null;
    }
    if (b.tur === 'meydan' && b.asama === 'sorgu' && b.oynayan === ben) return { hamle: { t: 'yeter' }, aciklama: 'Şüphelendiğin oyuncuyu sorgula; yalancıysa kartını geri alır. Doğru renk çıkarsa sorgu biter.' };
    return null;
  }
  if (g.sira !== ben) return null;

  const benim = g.oyuncular.find((o) => o.id === ben);
  const rakipler = g.oyuncular.filter((o) => o.id !== ben && !o.elendi && !o.cikti && (benim?.takim === undefined || o.takim !== benim.takim));
  const tehdit = rakipler.some((o) => o.kartSayisi <= 2);
  const enAz = Math.min(99, ...rakipler.map((o) => o.kartSayisi));
  const ustDeger = g.ust.deger;
  const gercekUyar = (k: UnoKart) => k.renk === null || k.renk === g.aktifRenk || k.deger === ustDeger || mod === 'hepsiJoker' || !!g.yigin;
  // Joker çekme kartı yalnız elde aktif renkten kart yokken dürüstçe oynanır (itirazda yakalanmamak için)
  const renkVar = g.elim.some((k) => k.renk === g.aktifRenk);
  const itirazli = (k: UnoKart) => (k.deger === '+4' && ['klasik', 'deluxe', 'hizli', 'cekCek', 'atlama', 'yediSifir'].includes(mod))
    || ((k.deger === 'joker+2' || k.deger === 'jokerRenk') && (mod === 'flip' || mod === 'express')) || (k.deger === 'fx+4' && mod === 'flex');
  const oynanir = g.elim.filter((k) => g.oynanabilir.includes(k.id));
  // Yalancı: doğru söylenebilecek kartlar (yalancı kartı gerçekten uyuyorsa) + açık oynanan düz kartlar
  let uygun = oynanir.filter((k) => (mod === 'yalanci' ? gercekUyar(k) : true) && (!itirazli(k) || !renkVar || !!g.yigin));
  if (!uygun.length && g.zorunlu) uygun = oynanir;
  if (!uygun.length && g.takimOyun) uygun = oynanir;

  const hamleKur = (kart: UnoKart): Extract<UnoHamle, { t: 'oyna' }> => {
    const h: Extract<UnoHamle, { t: 'oyna' }> = { t: 'oyna', kart: kart.id };
    const yalnizFlex = !!g.yalnizFlex?.includes(kart.id);
    const flexOlur = !!g.flex?.includes(kart.id);
    // Flex yüzü: yalnız öyle uyuyorsa ya da bir rakibi durdurmak gerekiyorsa
    if (yalnizFlex || (flexOlur && tehdit && !sayiKartiMi(kart))) h.flex = true;
    if (renkGerek(mod, kart)) {
      // En çok kartın olan renk; eşitlikte geçerli renk korunur (Gökkuşağı Tayı: o rengin hepsi atılır)
      h.renk = enCok();
    }
    if (hedefGerek(mod, kart.deger, !!h.flex)) h.hedef = hedefSec(g, ben);
    if (mod === 'yalanci' && kart.yl) { h.kapali = true; h.beyan = { renk: kart.renk ?? h.renk ?? g.aktifRenk, deger: kart.deger }; }
    if (g.elim.length === 2) h.uno = true;
    return h;
  };

  if (!uygun.length) {
    // Yalancı: bot uymayan yalancı kartını kapalı oynayıp blöf yapabilir
    const yalanci = mod === 'yalanci' && blof !== undefined ? oynanir.filter((k) => k.yl) : [];
    if (yalanci.length && blof! < 0.45) {
      const kart = yalanci.reduce((en, k) => (kartPuani(k, mod) > kartPuani(en, mod) ? k : en));
      const sayilar = UNO_BEYAN_DEGERLER.slice(0, 10);
      const h: UnoHamle = { t: 'oyna', kart: kart.id, kapali: true, beyan: { renk: g.aktifRenk, deger: sayilar[Math.floor(blof! * 1000) % 10] } };
      if (g.elim.length === 2) h.uno = true;
      return { hamle: h, aciklama: 'Blöf.' };
    }
    if (g.yigin && !g.cektiBuTur) {
      return { hamle: { t: 'cek' }, aciklama: g.firlatici ? `Ekleyecek Vur kartın yok: fırlatıcıya ${g.yigin} kez bas.` : `Ekleyecek kartın yok: biriken ${g.yigin} kartı çek.` };
    }
    return g.cektiBuTur
      ? { hamle: { t: 'pas' }, aciklama: 'Çektiğin kart uymuyor: sırayı geç.' }
      : { hamle: { t: 'cek' }, aciklama: g.firlatici ? 'Oynanabilir kartın yok: fırlatıcıya bas.' : mod === 'noMercy' ? 'Oynanabilir kartın yok: uyan kart gelene dek çekersin.' : 'Oynanabilir kartın yok: desteden çek.' };
  }

  const zarar = (d: UnoDeger) => ['+1', '+2', 'r+4', '+5', 'joker+2', '+4', 'jokerYon4', '+6', '+10', 'jokerRenk', 'rulet', 'jokerHedef2', 'vur1', 'vur2', 'jokerVur', 'jokerTakim4', 'fxHedef2', 'fx+4', 'fxHerkes', 'kuromi'].includes(d);
  const atlatir = (d: UnoDeger) => ['pas', 'pasHerkes', 'jokerPas', 'jokerPas2', 'batman'].includes(d);
  const takasIyi = enAz < g.elim.length - 1;
  const puan = (k: UnoKart): number => {
    const d = k.deger;
    if (d === 'jokerTakas' || (d === '7' && UNO_TAKAS_MODLAR.includes(mod))) return g.elim.length === 1 ? -500 : takasIyi ? 950 : d === '7' ? 120 : 5;
    if (g.yigin) return 2000 - kartPuani(k, mod) - (CEKME[d] ?? 0) * 10; // cezaya en küçük kartla karşılık ver
    if (tehdit && zarar(d)) return 1000 + (CEKME[d] ?? 2);
    if (tehdit && atlatir(d)) return 800;
    if (d === 'hepsiAt' && k.renk) return 600 + sayim[k.renk] * 60;
    if (d === 'pony') { const n = Math.max(...UNO_RENKLER.map((r) => sayim[r])); return n >= 2 ? 620 + n * 60 : 60; }
    if (d === 'kitty') return g.elim.length > 2 ? 640 : 70;
    if (mod === 'hepsiJoker') return d === 'joker' ? 600 : 300;
    if (k.renk === null) return d === 'joker' ? 100 : 50; // jokerler sona saklanır
    return (sayiKartiMi(k) ? 500 + Number(d) : 300) + sayim[k.renk] * 10;
  };
  const kart = uygun.reduce((en, k) => (puan(k) > puan(en) || (puan(k) === puan(en) && k.id < en.id) ? k : en));
  const hamle = hamleKur(kart);
  const ad = `${k_ad(kart, g)}`;
  const p = puan(kart);
  const neden = g.yigin ? 'biriken cezayı sıradakine devret'
    : p >= 800 && p < 2000 && tehdit ? 'bir rakibin az kartı kaldı, onu durdur'
      : (kart.deger === 'jokerTakas' || kart.deger === '7') && takasIyi ? 'en az kartı olan rakiple elini değiştir'
        : kart.deger === 'hepsiAt' ? 'bu renkteki bütün kartlarından kurtul'
          : kart.renk === null && hamle.renk ? `${renkAd(hamle.renk)} rengi seç (elinde en çok o var)`
            : kart.renk === null ? 'her zaman oynanır'
              : sayiKartiMi(kart) ? 'elinde en çok bulunan renkten en yüksek sayı'
                : 'sayı kartın uymuyor, aksiyon kartını kullan';
  return { hamle, aciklama: `${ad}: ${neden}.${hamle.flex ? ' Flex yüzüyle oyna.' : ''}${hamle.kapali ? ' Kapalı oyna ve doğruyu söyle.' : ''}${hamle.uno ? ' Oynarken UNO de.' : ''}` };
}
const k_ad = (kart: UnoKart, g: UnoGorunum): string => `${kart.renk ? (g.taraf === 'k' ? UNO_KOYU_RENK_AD : UNO_RENK_AD)[kart.renk] + ' ' : ''}${UNO_DEGER_AD[kart.deger]}`;

/** Asistan ipucu: önce UNO / yakalama fırsatı, sonra sıra hamlesi (bot mantığıyla aynı). */
export function oneri(g: UnoGorunum, ben: string): Oneri | null {
  if (g.bitti || !g.oyuncular.some((o) => o.id === ben)) return null;
  if (g.yakalanabilir.includes(ben)) return { hamle: { t: 'uno' }, aciklama: 'Tek kartın kaldı: yakalanmadan UNO de.' };
  const benim = g.oyuncular.find((o) => o.id === ben);
  const hedef = g.yakalanabilir.find((id) => id !== ben && (benim?.takim === undefined || g.oyuncular.find((o) => o.id === id)?.takim !== benim.takim));
  if (hedef) return { hamle: { t: 'yakala', hedef }, aciklama: g.firlatici ? 'UNO demeyen oyuncuyu yakala: fırlatıcıya 2 kez basar.' : 'UNO demeyen oyuncuyu yakala: 2 kart çeker.' };
  return siraOnerisi(g, ben);
}
