/**
 * Uno — saf yardımcılar. Motor (sunucu) ve istemci (ipucu, el dizilişi, erişilebilirlik adı) aynı işlevleri kullanır.
 * Yan etki yok; yalnız `tipler.ts` türleri.
 */
import type { UnoDeger, UnoGorunum, UnoHamle, UnoKart, UnoRenk } from '../tipler';

export const UNO_RENKLER: readonly UnoRenk[] = ['k', 's', 'y', 'm'];
export const UNO_DEGERLER: readonly UnoDeger[] = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'pas', 'yon', '+2', 'joker', '+4'];

export const UNO_RENK_AD: Record<UnoRenk, string> = { k: 'Kırmızı', s: 'Sarı', y: 'Yeşil', m: 'Mavi' };
export const UNO_DEGER_AD: Record<UnoDeger, string> = {
  '0': 'Sıfır', '1': 'Bir', '2': 'İki', '3': 'Üç', '4': 'Dört', '5': 'Beş', '6': 'Altı', '7': 'Yedi', '8': 'Sekiz', '9': 'Dokuz',
  pas: 'Atlat', yon: 'Yön değiştir', '+2': 'İki çek', joker: 'Joker', '+4': 'Dört çek',
};

export const sayiKartiMi = (k: UnoKart): boolean => k.deger.length === 1;

/** Aktif renk, üstteki kartla aynı değer/simge ya da joker/+4 (her zaman). */
export function oynanabilirMi(kart: UnoKart, ust: UnoKart, aktifRenk: UnoRenk): boolean {
  return kart.renk === null || kart.renk === aktifRenk || kart.deger === ust.deger;
}

/** El sonu puan değeri: sayı = yüz değeri, pas/yon/+2 = 20, joker/+4 = 50 */
export function kartDegeri(kart: UnoKart): number {
  if (kart.renk === null) return 50;
  return sayiKartiMi(kart) ? Number(kart.deger) : 20;
}

/** Sıralı kart kimlikleri: renk (k,s,y,m) → değer; joker ve +4 sonda */
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

/** Yalnız sıra hamlesi (oyna / çek / pas). Bot ve asistan aynı mantığı kullanır; sıra `ben`de değilse null. */
export function siraOnerisi(g: UnoGorunum, ben: string): Oneri | null {
  if (g.bitti || g.sira !== ben) return null;
  const sayim: Record<UnoRenk, number> = { k: 0, s: 0, y: 0, m: 0 };
  for (const k of g.elim) if (k.renk) sayim[k.renk]++;
  const enCok = (): UnoRenk => { let r: UnoRenk = g.aktifRenk; for (const x of UNO_RENKLER) if (sayim[x] > sayim[r]) r = x; return r; };
  if (g.renkSec) { const renk = enCok(); return { hamle: { t: 'renk', renk }, aciklama: `İlk kart joker: elinde en çok ${UNO_RENK_AD[renk].toLocaleLowerCase('tr')} var, onu seç.` }; }
  if (g.dortBekle?.hedef === ben) return { hamle: { t: 'kabul' }, aciklama: '+4 sana oynandı. Kabul edersen 4 çekersin. İtiraz edersen: oynayanın elinde önceki renkten kart varsa o 4 çeker, yoksa sen 6 çekersin.' };
  // +4 yalnız elde aktif renkten kart yokken dürüstçe oynanır (itirazda yakalanmamak için)
  const renkVar = g.elim.some((k) => k.renk === g.aktifRenk);
  const uygun = g.elim.filter((k) => g.oynanabilir.includes(k.id) && (k.deger !== '+4' || !renkVar || !!g.yigin));
  if (!uygun.length) {
    if (g.yigin && !g.cektiBuTur) return { hamle: { t: 'cek' }, aciklama: `Ekleyecek kartın yok: biriken ${g.yigin} kartı çek.` };
    return g.cektiBuTur
      ? { hamle: { t: 'pas' }, aciklama: 'Çektiğin kart uymuyor: sırayı geç.' }
      : { hamle: { t: 'cek' }, aciklama: 'Oynanabilir kartın yok: desteden çek.' };
  }
  const tehdit = g.oyuncular.some((o) => o.id !== ben && o.kartSayisi <= 2);
  const puan = (k: UnoKart): number => {
    if (tehdit && k.deger === '+2') return 1000;
    if (tehdit && k.deger === '+4') return 900;
    if (tehdit && k.deger === 'pas') return 800;
    if (k.renk === null) return k.deger === 'joker' ? 100 : 50; // jokerler sona saklanır
    return (sayiKartiMi(k) ? 500 + Number(k.deger) : 300) + sayim[k.renk] * 10;
  };
  const kart = uygun.reduce((en, k) => (puan(k) > puan(en) || (puan(k) === puan(en) && k.id < en.id) ? k : en));
  const hamle: UnoHamle = { t: 'oyna', kart: kart.id };
  if (kart.renk === null) {
    // En çok kartın olan renk; eşitlikte geçerli renk korunur
    let renk = g.aktifRenk;
    for (const r of UNO_RENKLER) if (sayim[r] > sayim[renk]) renk = r;
    hamle.renk = renk;
  }
  if (g.elim.length === 2) hamle.uno = true;
  const ad = `${kart.renk ? UNO_RENK_AD[kart.renk] + ' ' : ''}${UNO_DEGER_AD[kart.deger]}`;
  const neden = puan(kart) >= 800 ? 'bir rakibin az kartı kaldı, onu durdur'
    : kart.renk === null ? `başka kartın uymuyor; ${UNO_RENK_AD[hamle.renk!].toLocaleLowerCase('tr')} rengi seç (elinde en çok o var)`
    : sayiKartiMi(kart) ? 'elinde en çok bulunan renkten en yüksek sayı'
    : 'sayı kartın uymuyor, aksiyon kartını kullan';
  return { hamle, aciklama: `${ad}: ${neden}.${hamle.uno ? ' Oynarken UNO de.' : ''}` };
}

/** Asistan ipucu: önce UNO / yakalama fırsatı, sonra sıra hamlesi (bot mantığıyla aynı). */
export function oneri(g: UnoGorunum, ben: string): Oneri | null {
  if (g.bitti || !g.oyuncular.some((o) => o.id === ben)) return null;
  if (g.yakalanabilir.includes(ben)) return { hamle: { t: 'uno' }, aciklama: 'Tek kartın kaldı: yakalanmadan UNO de.' };
  const hedef = g.yakalanabilir.find((id) => id !== ben);
  if (hedef) return { hamle: { t: 'yakala', hedef }, aciklama: 'UNO demeyen oyuncuyu yakala: 2 kart çeker.' };
  return siraOnerisi(g, ben);
}
