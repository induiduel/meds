/**
 * Uno kart rehberi: her kartın o moddaki gerçek etkisi, modların kural anlatımı. Saf veri + işlev (React yok).
 * Metinler motorla birebirdir (services/masa/motor/uno.ts, unoKartlar.ts); kural değişirse önce motor, sonra burası güncellenir.
 * Kural sayfası (kurallar/UnoKurallar.tsx), lobi mod kataloğu ve oyun içi kart balonu aynı tabloyu okur.
 */
import type { UnoDeger, UnoMod, UnoRenk, UnoYuz } from '../../../services/masa/tipler';
import { UNO_KOYU_RENK_AD, UNO_RENK_AD, UNO_TAKAS_MODLAR } from '../../../services/masa/motor/unoAsistan';
import { FLIP_ACIK, FLIP_KOYU, UNO_DESTE_DOKUM, flexRenk, kartPuani, type DesteSatir } from '../../../services/masa/motor/unoKartlar';

export interface KartBilgi { ad: string; etki: string; puan: number; ipucu?: string }
export type KartGrup = 'sayi' | 'aksiyon' | 'joker' | 'ozel';
export interface ModKart {
  /** Örnek yüz (çizim için) */
  yuz: UnoYuz;
  /** Destedeki toplam adet (dört renk birlikte) */
  adet: number;
  bilgi: KartBilgi;
  grup: KartGrup;
  /** Flip: kartın hangi yüzünde */
  taraf?: 'acik' | 'koyu';
  /** Aynı satırda gösterilecek öbür örnekler (sayı özetlerinde) */
  ornekler?: UnoYuz[];
  /** Flex kartı: flex yüzünün etkisi (düz yüz `bilgi`de) */
  flexBilgi?: KartBilgi;
}

const RENKLER: readonly UnoRenk[] = ['k', 's', 'y', 'm'];
const sayiMi = (d: UnoDeger) => d.length === 1;
const kucuk = (s: string) => s.toLocaleLowerCase('tr');

/** Kartların kısa adları (ekranda görünen) */
export const KART_AD: Record<UnoDeger, string> = {
  '0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
  pas: 'Atlat', yon: 'Yön', '+2': '+2', joker: 'Joker', '+4': 'Joker +4',
  '+1': '+1', flip: 'Flip', 'joker+2': 'Joker +2', '+5': '+5', pasHerkes: 'Herkesi Atlat', jokerRenk: 'Joker Renk Çek',
  jokerYon: 'Joker Yön', jokerPas: 'Joker Atlat', jokerPas2: 'Joker İkili Atlat', jokerHedef2: 'Joker Hedefli +2', jokerTakas: 'Joker Zorunlu Takas',
  hepsiAt: 'Hepsini At', 'r+4': '+4', jokerYon4: 'Joker Yön +4', '+6': 'Joker +6', '+10': 'Joker +10', rulet: 'Joker Renk Ruleti',
  vur1: 'Vur 1', vur2: 'Vur 2', jokerVur: 'Joker Çifte Saldırı',
  jokerTakim: 'Joker Takım Oyunu', jokerTakim4: 'Joker Takıma +4',
  jokerCevir: 'Joker Güçleri Çevir', fxHerkes: 'Flex Joker Herkes Çeker', fxHedef2: 'Flex Joker Hedefli +2', 'fx+4': 'Flex Joker +4',
  jokerMeydan: 'Joker Meydan Okuma',
  kitty: 'Kedicik: Hediye Paketi', batman: 'Yarasa: Gece Siperi', kuromi: 'Yaramaz Tavşan: Şaka', pony: 'Gökkuşağı Tayı',
};

const renkAdi = (kart: UnoYuz, r: UnoRenk) => (kart.t === 'k' ? UNO_KOYU_RENK_AD : UNO_RENK_AD)[r];

/** Çekme kartlarının ortak anlatımı: klasik ailede hemen çekilir, biriktiren modlarda ceza birikir */
function cekEtki(mod: UnoMod, n: number, kosul: string): string {
  if (mod === 'noMercy') return `Sıradaki oyuncu ${n} kart çeker ve sırası geçer. Ceza birikir: sıradaki, elinde +${n} ya da daha büyük bir çekme kartı varsa (rengi tutmasa da) üstüne ekleyip toplamı bir sonrakine devreder; ekleyemeyen hepsini çeker.`;
  if (mod === 'yigma') return `Sıradaki oyuncu ${n} kart çeker ve sırası geçer. Ceza birikir: ${kosul}; ekleyemeyen biriken kartların hepsini çeker.`;
  if (mod === 'dostlar') return `Sıradaki oyuncu ${n} kart çeker ve sırası geçer. Ceza birikir: ${kosul}; Yarasa kartı biriken cezayı tümden siler. Ekleyemeyen hepsini çeker.`;
  return `Sıradaki oyuncu ${n} kart çeker ve sırası geçer. Üstüne başka çekme kartı eklenmez.`;
}

function etkiYaz(mod: UnoMod, kart: UnoYuz, flex: boolean): { etki: string; ipucu?: string } {
  const d = kart.deger;
  const takas = UNO_TAKAS_MODLAR.includes(mod);
  if (sayiMi(d)) {
    const ek: string[] = [];
    if (d === '7' && takas) ek.push('Oynayınca seçtiğin rakiple elini değiştirirsin. Son kartınsa takas yapılmaz, eli kazanırsın.');
    if (d === '0' && takas) ek.push('Oynanınca herkes elini oyun yönündeki oyuncuya verir. Son kartınsa devir yapılmaz, eli kazanırsın.');
    if (kart.cv) ek.push('Çevirme simgeli: oynayınca kendi güç kartın döner (yeşilse kırmızıya, kırmızıysa yeşile).');
    if (kart.ps) ek.push('Paslaşma simgeli: oynayınca sen ve ortağın birbirinize birer kart verirsiniz (ikinizin de kartı varsa).');
    if (kart.fx && kart.fx !== 'j') ek.push(`Flex kartı: güç kartın yeşilken flex rengi (${kucuk(UNO_RENK_AD[kart.fx])}) ortadaki renge uyuyorsa da oynanır. Geçerli renk yine kartın asıl rengi olur, güç kartın kırmızıya döner.`);
    if (kart.yl) ek.push('Yalancı kartı: her zaman kapalı oynanır ve ne olduğu söylenir; söylediğin kart ortadakine uymalıdır, doğru olması gerekmez.');
    const temel = mod === 'hepsiJoker' ? 'Her zaman oynanır; bu modda renk ve sayı tutturulmaz.' : 'Ortadaki kartla rengi ya da sayısı tutunca oynanır.';
    return { etki: [temel, ...ek].filter(Boolean).join(' '), ipucu: d === '7' && takas ? 'En az kartı olan rakibi seç; elin zaten en azsa 7’yi sona sakla.' : undefined };
  }
  const yl = kart.yl ? ' Yalancı kartıdır: kapalı oynanır, söylenen etki inanılırsa uygulanır.' : '';
  switch (d) {
    case 'pas':
      if (flex) return { etki: 'Flex yüzü: bütün rakipler atlanır, yeniden sen oynarsın. Güç kartın kırmızıya döner.' };
      return { etki: `Sıradaki oyuncu atlanır. İki kişilik oyunda yeniden sen oynarsın.${yl}` };
    case 'yon':
      if (flex) return { etki: 'Flex yüzü: yön döner ve yeni yöndeki ilk oyuncu atlanır. Güç kartın kırmızıya döner.' };
      return { etki: `Oyun yönü tersine döner. İki kişilik oyunda Atlat gibi çalışır: yeniden sen oynarsın.${yl}` };
    case '+2':
      if (flex) return { etki: 'Flex yüzü: bütün rakipler birer kart çeker, kimsenin sırası geçmez. Güç kartın kırmızıya döner.' };
      return { etki: cekEtki(mod, 2, 'sıradaki elinde +2 ya da +4 varsa üstüne ekler') + yl };
    case '+1': return { etki: 'Sıradaki oyuncu 1 kart çeker ve sırası geçer. Aynı renk ya da başka bir +1 üstüne oynanır.' };
    case '+5': return { etki: 'Koyu yüz: sıradaki oyuncu 5 kart çeker ve sırası geçer. Aynı renk ya da başka bir +5 üstüne oynanır.' };
    case 'r+4': return { etki: cekEtki(mod, 4, '') + ' Renkli bir karttır: ceza yokken yalnız rengi tutunca ya da başka bir +4 üstüne oynanır; itiraz edilmez.' };
    case 'joker':
      if (mod === 'hepsiJoker') return { etki: 'Düz joker: her zaman oynanır, başka etkisi yoktur.', ipucu: 'Elindeki en değersiz karttır (20 puan); aksiyon jokerlerini rakip azalınca kullan.' };
      return { etki: 'Her zaman oynanır; geçerli rengi sen seçersin.', ipucu: 'Elinde en çok bulunan rengi seç.' };
    case '+4':
      if (mod === 'hepsiJoker') return { etki: 'Sıradaki oyuncu 4 kart çeker ve sırası geçer. Koşulsuz oynanır, itiraz edilmez.' };
      if (mod === 'yalanci') return { etki: 'Her karta uyar; rengi sen seçersin, sıradaki 4 kart çeker ve sırası geçer. Yalancı kartıdır: kapalı oynanır. Klasik +4 itirazı yoktur, yalnız “Yalan!” denebilir.' };
      if (mod === 'yigma' || mod === 'dostlar') return { etki: `Rengi sen seçersin. ${cekEtki(mod, 4, '+4’ün üstüne yalnız +4 eklenir')} Bu modda +4’e itiraz yoktur.` };
      return { etki: 'Rengi sen seçersin; sıradaki 4 kart çeker ve sırası geçer. Kurala göre yalnız elinde ortadaki renkten kart yokken oynanır. Sıradaki itiraz edebilir: elinde o renkten kart vardıysa 4 kartı sen çekersin, yoktuysa itiraz eden 6 kart çeker.', ipucu: 'Elinde ortadaki renkten kart varken oynarsan itirazda yakalanırsın.' };
    case 'joker+2':
      if (mod === 'hepsiJoker') return { etki: 'Sıradaki oyuncu 2 kart çeker ve sırası geçer. İtiraz edilmez, üstüne eklenmez.' };
      return { etki: 'Rengi sen seçersin; sıradaki 2 kart çeker ve sırası geçer. Kurala göre yalnız elinde ortadaki renkten kart yokken oynanır. Sıradaki itiraz edebilir: haklıysa 2 kartı sen çekersin, haksızsa o 4 kart çeker.' };
    case 'jokerRenk': return { etki: 'Koyu yüz: bir renk seçersin; sıradaki oyuncu o renkten kart gelene dek çeker, hepsini alır ve sırası geçer. İtiraz edilebilir: elinde ortadaki renkten kart vardıysa o renk gelene dek sen çekersin; yoktuysa itiraz eden, renk gelene dek çektiklerine 2 kart daha ekler.' };
    case 'flip': return { etki: 'Her şey ters döner: atık yığını, çekme destesi ve bütün eller öbür yüzüne çevrilir. Yeni üst kart, atığın en altındaki kartın öbür yüzüdür; joker çıkarsa rengi Flip’i oynayan seçer. Aynı renk ya da başka bir Flip üstüne oynanır.', ipucu: 'Rakiplerin elindeki kartların öbür yüzünü görürsün: çevirmeden önce bak.' };
    case 'pasHerkes': return { etki: 'Bütün rakipler atlanır, yeniden sen oynarsın.' };
    case 'jokerYon': return { etki: 'Oyun yönü tersine döner. İki kişilik oyunda yeniden sen oynarsın.' };
    case 'jokerPas': return { etki: 'Sıradaki oyuncu atlanır.' };
    case 'jokerPas2': return { etki: 'Sıradaki iki oyuncu atlanır. İki ya da üç kişilik oyunda sıra yeniden sana gelir.' };
    case 'jokerHedef2': return { etki: 'Seçtiğin rakip 2 kart çeker; sırası atlanmaz, oyun olağan sıradaki oyuncuyla sürer.', ipucu: 'En az kartı kalan rakibe oyna.' };
    case 'jokerTakas': return { etki: 'Seçtiğin rakiple elini değiştirmek zorundasın. Son kartın buysa takas yine yapılır: boş eli alan rakip eli kazanır.', ipucu: 'Son kartın olarak kalmasın; rakibin eli seninkinden azken oyna.' };
    case 'hepsiAt': return { etki: `Kartla birlikte elindeki aynı renkten bütün kartları atarsın; Hepsini At en üstte kalır. Aynı renk ya da başka bir Hepsini At üstüne oynanır. Elin boşalırsa eli kazanırsın.`, ipucu: 'Elinde o renkten çok kart biriktiğinde oyna.' };
    case 'jokerYon4': return { etki: 'Yön tersine döner; yeni yöndeki sıradaki oyuncu 4 kart çeker, rengi sen seçersin. Ceza birikir (+4 ya da daha büyüğü eklenir). İki kişilik oyunda ceza sana döner: üstüne çekme kartı ekleyerek rakibine yollayabilirsin, ekleyemezsen sen çekersin.' };
    case '+6': return { etki: 'Rengi sen seçersin; sıradaki 6 kart çeker ve sırası geçer. Ceza birikir: üstüne yalnız +6 ya da +10 eklenir. İtiraz edilmez.' };
    case '+10': return { etki: 'Rengi sen seçersin; sıradaki 10 kart çeker ve sırası geçer. Ceza birikir: üstüne yalnız başka bir +10 eklenir. İtiraz edilmez.' };
    case 'rulet': return { etki: 'Rengi sıradaki oyuncu seçer; sonra desteden o renk gelene dek kart açılır, açılan bütün kartları alır ve sırası geçer. Biriken cezanın üstüne oynanmaz, üstüne de ceza eklenmez.' };
    case 'vur1': return { etki: 'Sıradaki oyuncu fırlatıcıya 1 kez basar ve sırası geçer. Vurulan, elinde herhangi bir Vur kartı varsa (rengi tutmasa da) üstüne ekleyip basışları bir sonrakine devreder.' };
    case 'vur2': return { etki: 'Sıradaki oyuncu fırlatıcıya 2 kez basar ve sırası geçer. Vurulan, elinde herhangi bir Vur kartı varsa (rengi tutmasa da) üstüne ekleyip basışları bir sonrakine devreder.' };
    case 'jokerVur': return { etki: 'Bir renk ve bir rakip seçersin: seçtiğin rakip fırlatıcıya 2 kez basar, oyun ondan sonraki oyuncuyla sürer. Bir vuruşun üstüne de eklenir; o zaman biriken basışları seçtiğin rakibe yollarsın.' };
    case 'jokerTakim': return { etki: 'Rengi seçersin; sıra doğrudan ortağına atlar. Ortağın uyan bir kartını oynamak zorundadır. Oynayacak kartı yoksa sen 2 kart çekersin ve sıra ortağından sonraki oyuncuya geçer.', ipucu: 'Ortağının elinde olduğunu bildiğin rengi seç (el başında ona verdiğin kartı hatırla).' };
    case 'jokerTakim4': return { etki: 'Rengi seçersin; sıradaki oyuncu 2 kart çeker ve sırası geçer, onun ortağı da 2 kart çeker (eli bitmiş olsa bile; böylece oyuna döner).' };
    case 'jokerCevir': return { etki: 'Rengi seçersin; herkesin güç kartı döner (yeşiller kırmızı, kırmızılar yeşil olur). Bunun sonunda herkes kırmızı kalırsa hepsi yeniden yeşile döner.' };
    case 'fxHerkes': return { etki: flex ? 'Flex yüzü: rengi seçersin, bütün rakipler 2’şer kart çeker; kimsenin sırası geçmez. Güç kartın kırmızıya döner.' : 'Düz yüzü: olağan joker, rengi seçersin.' };
    case 'fxHedef2': return { etki: flex ? 'Flex yüzü: rengi seçersin, seçtiğin rakip 2 kart çeker; sırası atlanmaz. Güç kartın kırmızıya döner.' : 'Düz yüzü: olağan joker, rengi seçersin.' };
    case 'fx+4': return { etki: flex ? 'Flex yüzü: rengi seçersin, seçtiğin rakip 4 kart çeker; oyun olağan sıradakiyle sürer, itiraz edilmez. Güç kartın kırmızıya döner.' : 'Düz yüzü: Joker +4. Sıradaki 4 çeker ve sırası geçer ya da itiraz eder: elinde ortadaki renkten kart ya da başka joker vardıysa 4 kartı sen çekersin, yoktuysa itiraz eden 6 kart çeker.' };
    case 'jokerMeydan': return { etki: 'Açık oynanır; bir renk seçersin. Bütün rakipler o renkten olduğunu öne sürerek birer kartı kapalı koyar. Sonra dilediğin oyuncuyu tek tek sorgularsın: kartı o renkten değilse geri alır ve 1 kart çeker; doğru renk çıkınca sorgu biter. Sorgulanmayan ve doğru çıkan kartlar jokerin altına girer.', ipucu: 'Elinde az kalan rakibi önce sorgula: kapalı kartla elini bitirebilir.' };
    case 'kitty': return { etki: 'Rengi ve bir rakibi seçersin; ona elinden seçtiğin 2 kartı hediye edersin (elinde en az 1 kart kalır). Biriken cezanın üstüne oynanmaz.', ipucu: 'En pahalı kartlarını ver: jokerler 50 puandır.' };
    case 'batman': return { etki: 'Sana ceza birikmişse üstüne oynarsın: biriken bütün çekme cezası silinir, rengi seçersin ve sıra geçer. Ceza yokken oynarsan bütün rakipler atlanır, yeniden sen oynarsın.', ipucu: 'Büyük bir ceza gelene dek elinde tut.' };
    case 'kuromi': return { etki: 'Rengi seçersin; bütün rakipler birer kart çeker, kimsenin sırası geçmez. Biriken cezanın üstüne oynanmaz.' };
    case 'pony': return { etki: 'Bir renk seçersin; elindeki o renkten bütün kartları atarsın, geçerli renk o olur. Elin boşalırsa eli kazanırsın. Biriken cezanın üstüne oynanmaz.', ipucu: 'Elinde en çok bulunan rengi seç.' };
    default: return { etki: 'Özel kart.' };
  }
}

/** Kartın o moddaki adı, etkisi ve puanı. `flex`: Flex kartının flex yüzü anlatılsın. */
export function kartBilgi(mod: UnoMod, kart: UnoYuz, flex = false): KartBilgi {
  const on = `${kart.fx && kart.renk ? 'Flex ' : ''}${kart.yl && kart.renk ? 'Yalancı ' : ''}${kart.renk ? renkAdi(kart, kart.renk) + ' ' : ''}`;
  const { etki, ipucu } = etkiYaz(mod, kart, flex);
  return { ad: `${on}${KART_AD[kart.deger]}`, etki, puan: kartPuani(kart, mod), ipucu };
}

/* ------------------------------------------------------------------ mod desteleri ------------------------------------------------------------------ */

const grupBul = (d: UnoDeger, renkli: boolean): KartGrup =>
  sayiMi(d) ? 'sayi' : ['kitty', 'batman', 'kuromi', 'pony'].includes(d) ? 'ozel' : renkli ? 'aksiyon' : 'joker';

function satirlar(mod: UnoMod, dokum: DesteSatir[], taraf?: 'acik' | 'koyu'): ModKart[] {
  const out: ModKart[] = [];
  const takas = UNO_TAKAS_MODLAR.includes(mod);
  let ri = 0;
  const yuzKur = (s: DesteSatir, r: UnoRenk): UnoYuz => ({ renk: s.renkli ? r : null, deger: s.deger, ...s.ek, ...(s.ek?.fx && s.renkli ? { fx: flexRenk(r, s.deger) } : {}) });
  // Sayı kartları: aynı bayraklı ve özel etkisi olmayanlar tek satırda özetlenir
  const sayiGrup = new Map<string, DesteSatir[]>();
  for (const s of dokum) {
    if (!sayiMi(s.deger)) continue;
    const ozel = takas && (s.deger === '7' || s.deger === '0') ? s.deger : '';
    const anahtar = `${ozel}|${s.ek?.yl ? 'yl' : ''}${s.ek?.ps ? 'ps' : ''}${s.ek?.cv ? 'cv' : ''}${s.ek?.fx ? 'fx' : ''}`;
    sayiGrup.set(anahtar, [...(sayiGrup.get(anahtar) ?? []), s]);
  }
  for (const liste of sayiGrup.values()) {
    const degerler = [...new Set(liste.map((s) => s.deger))].sort();
    const adet = liste.reduce((t, s) => t + s.adet * 4, 0);
    const ilk = liste[0];
    const ornekler = degerler.slice(0, 4).map((v, i) => yuzKur({ ...ilk, deger: v }, RENKLER[(ri + i) % 4]));
    const yuz = ornekler[0];
    ri++;
    const b = kartBilgi(mod, yuz);
    const aralik = degerler.length === 1 ? degerler[0] : degerler.length === Number(degerler[degerler.length - 1]) - Number(degerler[0]) + 1 ? `${degerler[0]}–${degerler[degerler.length - 1]}` : degerler.join(', ');
    const sifat = ilk.ek?.yl ? 'Yalancı sayı kartları' : ilk.ek?.ps ? 'Paslaşma simgeli sayılar' : ilk.ek?.cv ? 'Çevirme simgeli sayılar' : ilk.ek?.fx ? 'Flex sayı kartları' : 'Sayı kartları';
    const ad = degerler.length === 1 ? `${ilk.ek?.yl ? 'Yalancı ' : ''}${degerler[0]} (dört renk)` : `${sifat} ${aralik}`;
    out.push({ yuz, adet, grup: 'sayi', taraf, ornekler: degerler.length > 1 ? ornekler : undefined, bilgi: { ...b, ad, puan: degerler.length === 1 ? b.puan : -1 } });
  }
  for (const s of dokum) {
    if (sayiMi(s.deger)) continue;
    const r = RENKLER[ri++ % 4];
    const yuz = yuzKur(s, r);
    const b = kartBilgi(mod, yuz);
    const ad = `${s.ek?.fx && s.renkli ? 'Flex ' : ''}${s.ek?.yl && s.renkli ? 'Yalancı ' : ''}${KART_AD[s.deger]}`;
    const kart: ModKart = { yuz, adet: s.adet * (s.renkli ? 4 : 1), grup: grupBul(s.deger, s.renkli), taraf, bilgi: { ...b, ad } };
    if (s.ek?.fx) {
      const fb = kartBilgi(mod, yuz, true);
      kart.flexBilgi = { ...fb, ad };
      if (!s.renkli) kart.bilgi = { ...kartBilgi(mod, yuz, false), ad };
    }
    out.push(kart);
  }
  return out;
}

/** Modun bütün kart türleri, adetleriyle (toplam = deste; Flip'te açık + koyu yüz ayrı ayrı 112) */
export function modKartlari(mod: UnoMod): ModKart[] {
  if (mod === 'flip') return [...satirlar(mod, FLIP_ACIK, 'acik'), ...satirlar(mod, FLIP_KOYU, 'koyu')];
  return satirlar(mod, UNO_DESTE_DOKUM[mod]);
}

/* ------------------------------------------------------------------ mod anlatımları ------------------------------------------------------------------ */

export interface ModRehber {
  slogan: string;
  ozet: string;
  nasil: string[];
  ozelKurallar: { baslik: string; metin: string }[];
  puan: [string, string][];
  ipuclari: string[];
  kaynakNotu?: string;
}

const PUAN_KLASIK: [string, string][] = [['Sayı kartı (0–9)', 'Üstündeki sayı'], ['Atlat, Yön, +2', '20'], ['Joker, Joker +4', '50']];
const UNO_DEMEK = { baslik: 'UNO demek', metin: 'Sondan bir önceki kartını oynarken UNO dersin. Unutursan, sıradaki oyuncu hamle yapana dek herhangi bir rakip seni yakalayabilir: 2 kart çekersin. Yakalanmadan önce fark edip UNO dersen kurtulursun.' };
const ILK_KART_KLASIK = { baslik: 'İlk kart', metin: 'Ortaya açılan ilk kart +4 ise desteye geri konur, yenisi açılır. Joker açılırsa ilk oyuncu rengi seçer. Atlat açılırsa ilk oyuncunun sırası geçer; Yön açılırsa sıra ters döner; +2 açılırsa ilk oyuncu 2 kart çeker ve sırası geçer.' };
const DENGELI = { baslik: 'Dengeli dağıtım', metin: 'Deste rastgele karılır; yalnız bir ele 2’den çok joker (en çok bir +4) ya da 3’ten çok aksiyon kartı düşerse fazlası destedeki rastgele bir sayı kartıyla değiştirilir. Elinde 3 joker olan oyuncu desteden dördüncüsünü çekmez.' };
const ITIRAZ4 = { baslik: '+4 ve itiraz', metin: '+4 kurala göre yalnız elinde ortadaki renkten kart yokken oynanır. Sıradaki oyuncu kabul eder (4 çeker, sırası geçer) ya da itiraz eder: oynayanın elinde o renkten kart vardıysa 4 kartı oynayan çeker ve itiraz eden olağan oynar; yoktuysa itiraz eden 6 kart çeker ve sırası geçer.' };
const hedefNot = (p: number) => `Maç, lobide seçilen el sayısı dolunca ya da bir oyuncu ${p} puana ulaşınca biter.`;

export const MOD_REHBER: Record<UnoMod, ModRehber> = {
  klasik: {
    slogan: 'Herkesin bildiği Uno, resmî kurallarıyla.',
    ozet: '108 kart, herkese 7 kart. Rengi, sayıyı ya da simgeyi tutturan kartı atarsın; elini ilk bitiren kazanır.',
    nasil: [
      'Ortadaki kartla rengi, sayısı ya da simgesi aynı olan kartı atarsın. Joker her zaman oynanır.',
      'Oynayacak kartın yoksa (ya da oynamak istemiyorsan) desteden 1 kart çekersin. Çektiğin kart uyuyorsa hemen oynayabilirsin; o tur başka kart oynayamazsın. Uymuyorsa sırayı geçersin.',
      'Deste biterse ortadaki kartlar (en üstteki hariç) karılıp yeni deste olur.',
      'Tek kartın kalınca UNO dersin. Son kartını oynayan eli kazanır.',
    ],
    ozelKurallar: [
      ILK_KART_KLASIK, ITIRAZ4,
      { baslik: 'Üst üste ekleme yok', metin: '+2 ve +4 üst üste eklenmez: kart çeken oyuncu karşılık veremez. Son kart +2 ya da +4 ise sıradaki oyuncu yine çeker ve o kartlar da puana sayılır.' },
      UNO_DEMEK, DENGELI,
    ],
    puan: PUAN_KLASIK,
    ipuclari: ['Yüksek sayıları ve aksiyon kartlarını erken at: elde kalan her kart eksi puandır.', 'Jokerleri sona sakla; +4’ü elinde ortadaki renk varken oynama.', 'Bir rakibin 1–2 kartı kaldıysa +2 ve Atlat ile onu durdur.'],
  },
  deluxe: {
    slogan: 'Puan defterli büyük kutu: 112 kart, 500 puana kadar.',
    ozet: 'Deluxe kutunun 112’lik destesi: klasik destenin aynısı, yalnız Joker sayısı 4 yerine 8. Kurallar klasikle aynıdır.',
    nasil: [
      'Herkese 7 kart dağıtılır. Rengi, sayıyı ya da simgeyi tutturan kartı atarsın; joker her zaman oynanır.',
      'Oynayamıyorsan 1 kart çekersin; çektiğin kart uyuyorsa hemen oynayabilirsin, uymuyorsa sırayı geçersin.',
      'Her elin sonunda puanlar deftere yazılır. ' + hedefNot(500),
    ],
    ozelKurallar: [ILK_KART_KLASIK, ITIRAZ4, UNO_DEMEK, DENGELI],
    puan: PUAN_KLASIK,
    ipuclari: ['Destede iki kat joker var: renk değişimi sık olur, tek renge yığılma.', '500 puana giden yolda büyük eller belirleyicidir: rakiplerin elinde joker bırakarak bitirmeye çalış.'],
    kaynakNotu: 'Deste dökümü Mattel’in Deluxe yönergesindeki (HGL63) listeye göredir: 76 sayı, 24 aksiyon, 8 Joker, 4 Joker +4.',
  },
  express: {
    slogan: 'Cep boyu Uno: yarım deste, beşer kart, hızlı eller.',
    ozet: '56 kart ve herkese 5 kart. +2’nin yerini +1, Joker +4’ün yerini Joker +2 alır; her sayıdan renk başına tek kart vardır.',
    nasil: [
      'Herkese 5 kart dağıtılır. Rengi, sayıyı ya da simgeyi tutturan kartı atarsın.',
      'Oynayamıyorsan 1 kart çekersin; çektiğin kart uyuyorsa hemen oynayabilirsin.',
      'Tek kartın kalınca UNO dersin; yakalanırsan 2 kart çekersin.',
      hedefNot(250),
    ],
    ozelKurallar: [
      { baslik: 'İlk kart', metin: 'Joker +2 açılırsa desteye geri konur. Joker açılırsa ilk oyuncu rengi seçer; Atlat ilk oyuncuyu atlatır, Yön sırayı ters çevirir, +1 açılırsa ilk oyuncu 1 kart çeker ve sırası geçer.' },
      { baslik: 'Joker +2 ve itiraz', metin: 'Joker +2 kurala göre yalnız elinde ortadaki renkten kart yokken oynanır. Sıradaki kabul eder (2 çeker) ya da itiraz eder: haklıysa 2 kartı oynayan çeker, haksızsa itiraz eden 4 kart çeker ve sırası geçer.' },
      UNO_DEMEK,
    ],
    puan: [['Sayı kartı (0–9)', 'Üstündeki sayı'], ['+1, Yön, Atlat', '20'], ['Joker, Joker +2', '50']],
    ipuclari: ['Deste küçük: hangi kartların çıktığını takip etmek kolaydır.', 'Beş kartla el çabuk biter; UNO demeyi unutma.'],
    kaynakNotu: 'Döküm (40 sayı, 4 +1, 4 Yön, 4 Atlat, 2 Joker, 2 Joker +2) UNO Express yönergesinin yaygın dökümüne göredir. En çok 6 oyuncu.',
  },
  flip: {
    slogan: 'Her kartın iki yüzü var: bir Flip, bütün oyunu tersine çevirir.',
    ozet: '112 çift yüzlü kart. Oyun açık yüzle başlar; Flip kartı oynanınca atık, deste ve bütün eller koyu yüze döner. Koyu yüz daha serttir: +5, Herkesi Atlat ve Joker Renk Çek.',
    nasil: [
      'Herkese 7 kart dağıtılır, oyun açık yüzle başlar. Rengi, sayıyı ya da simgeyi tutturan kartı atarsın.',
      'Rakiplerinin elindeki kartların öbür yüzünü görürsün; onlar da seninkileri görür. Destenin üstündeki kartın öbür yüzü de açıktır.',
      'Oynayamıyorsan 1 kart çekersin; çektiğin kart uyuyorsa hemen oynayabilirsin.',
      'Flip oynanınca her şey çevrilir ve oyun yeni yüzün renkleriyle (pembe, turuncu, turkuaz, mor) sürer; bir sonraki Flip’e dek öyle kalır.',
      'El bitince puan, o an etkin olan yüze göre hesaplanır. ' + hedefNot(500),
    ],
    ozelKurallar: [
      { baslik: 'Flip nasıl çevirir', metin: 'Atık yığını ters çevrilir: Flip kartı en alta gider, yeni üst kart yığının eski en alt kartının öbür yüzüdür ve geçerli rengi o belirler. Bu kartın etkisi uygulanmaz; joker çıkarsa rengi Flip’i oynayan seçer. Deste ve bütün eller de çevrilir.' },
      { baslik: 'İlk kart', metin: 'Her el açık yüzle başlar. İlk kart Flip ya da Joker +2 çıkarsa desteye geri konur, yenisi açılır. +1 açılırsa ilk oyuncu 1 kart çeker ve sırası geçer.' },
      { baslik: 'Joker +2 itirazı (açık yüz)', metin: 'Yalnız elinde ortadaki renkten kart yokken oynanır. Sıradaki kabul eder (2 çeker) ya da itiraz eder: haklıysa 2 kartı oynayan çeker, haksızsa itiraz eden 4 kart çeker.' },
      { baslik: 'Joker Renk Çek itirazı (koyu yüz)', metin: 'Sıradaki kabul ederse seçilen renk gelene dek çeker. İtiraz ederse: oynayanın elinde ortadaki renkten kart vardıysa o renk gelene dek oynayan çeker; yoktuysa itiraz eden renk gelene dek çeker, üstüne 2 kart daha alır.' },
      { baslik: 'Üst üste ekleme yok', metin: '+1, +5 ve joker çekme kartlarının üstüne ekleme yapılmaz.' },
      UNO_DEMEK,
    ],
    puan: [['Sayı kartı (1–9)', 'Üstündeki sayı'], ['+1', '10'], ['+5, Yön, Atlat, Flip', '20'], ['Herkesi Atlat', '30'], ['Joker', '40'], ['Joker +2', '50'], ['Joker Renk Çek', '60']],
    ipuclari: ['Çevirmeden önce rakiplerin öbür yüzlerine bak: koyu yüzde kimin eli güçlenecek?', 'Koyu yüzde elin kötüyse Flip’i sakla; açık yüze dönüş biletindir.', 'Joker Renk Çek için destede az kalan rengi seç: rakip daha çok kart çeker.'],
    kaynakNotu: 'Açık ve koyu yüzlerin hangi kartta eşleştiği resmî yönergede yazmaz; her elde rastgele eşlenir. Destede 0 yoktur.',
  },
  hepsiJoker: {
    slogan: 'Renk yok, sayı yok: her kart joker, her kart oynanır.',
    ozet: 'All Wild: 112 kartın hepsi jokerdir. Eşleştirme derdi yoktur; oyunu Atlat, Yön, çekme, hedefli çekme ve el takası kartlarının zamanlaması belirler.',
    nasil: [
      'Herkese 7 kart dağıtılır. Sıran gelince dilediğin kartı atarsın: renk ya da sayı tutturmak gerekmez.',
      'Aksiyon jokeri oynadıysan etkisi uygulanır; düz jokerin etkisi yoktur.',
      'İstersen kart oynamak yerine desteden 1 kart çekebilirsin; o tur yalnız çektiğin kartı oynayabilir ya da sırayı geçebilirsin.',
      'Tek kartın kalınca UNO dersin; yakalanırsan 2 kart çekersin. ' + hedefNot(500),
    ],
    ozelKurallar: [
      { baslik: 'İlk kart', metin: 'Ortaya açılan ilk kartın etkisi yok sayılır; hangi kart çıkarsa çıksın ilk oyuncu olağan oynar.' },
      { baslik: 'İtiraz ve ekleme yok', metin: 'Joker +4 ve Joker +2 koşulsuz oynanır, itiraz edilmez; üstlerine çekme kartı eklenmez.' },
      { baslik: 'Hedefli +2', metin: 'Seçtiğin rakip 2 kart çeker ama sırası atlanmaz; oyun olağan sıradaki oyuncuyla sürer.' },
      { baslik: 'Zorunlu Takas', metin: 'Bir rakip seçip elini onunla değiştirmek zorundasın. Son kartın Zorunlu Takas ise takas yine yapılır ve boş eli alan rakip eli kazanır.' },
      { baslik: 'İki kişilik oyun', metin: 'Joker Yön, Joker Atlat ve Joker İkili Atlat’tan sonra yeniden sen oynarsın.' },
      UNO_DEMEK,
    ],
    puan: [['Düz Joker', '20'], ['Bütün aksiyon jokerleri', '50']],
    ipuclari: ['Düz jokerleri önce at, aksiyonları rakip 1–2 karta düşünce kullan.', 'Zorunlu Takas’ı elinde son kart olarak bırakma: boş elini rakibe verirsin.', 'Elin kalabalıksa Zorunlu Takas’ı en az kartlı rakibe oyna.'],
    kaynakNotu: 'Kart adetleri (54 Joker, 14 Yön, 14 Atlat, 6 İkili Atlat, 10 +2, 6 +4, 4 Hedefli +2, 4 Zorunlu Takas) resmî yönergede yazmaz; toplamı 112 eden yaygın döküm kullanılır.',
  },
  noMercy: {
    slogan: 'Acımak yok: +10’lar birikir, 25 karta ulaşan elenir.',
    ozet: 'Show ’Em No Mercy: 168 kartlık en sert Uno. Düz joker yoktur; +6, +10, Renk Ruleti ve Hepsini At vardır. Çekme kartları birikir, uyan kart gelene dek çekilir.',
    nasil: [
      'Herkese 7 kart dağıtılır; ilk kart sayı olana dek açılır. Rengi, sayıyı ya da simgeyi tutturan kartı atarsın.',
      'Oynayacak kartın yoksa uyan bir kart gelene dek çekersin ve gelen kartı oynamak zorundasın. Elinde oynanabilir kart varken kart çekemezsin.',
      'Sana çekme kartı oynandıysa eşit ya da daha büyük bir çekme kartıyla karşılık verirsin; veremezsen biriken kartların hepsini çeker, sıranı kaybedersin.',
      'Elindeki kart sayısı 25’e ulaşırsa elenirsin. Son kartını oynayan ya da masada tek kalan eli kazanır.',
      hedefNot(1000),
    ],
    ozelKurallar: [
      { baslik: 'Biriktirme', metin: 'Çekme kartları: +2, +4 (renkli), Joker Yön +4, Joker +6, Joker +10. Üstüne yalnız eşit ya da daha büyük değerli bir çekme kartı eklenir (ör. +4’ün üstüne +2 olmaz, +6 olur); renk tutması gerekmez. Renk Ruleti cezanın üstüne eklenmez.' },
      { baslik: '25 kart: elenme', metin: 'Bir oyuncunun eli 25 karta ulaştığı an elenir; çekme o anda durur. Kartları kenara ayrılır ve deste yeniden karılınca oyuna döner. Elenen oyuncu eli izler.' },
      { baslik: '7 takas, 0 devir', metin: '7 oynayan, seçtiği bir rakiple elini değiştirir. 0 oynanınca oyundaki herkes elini oyun yönündeki oyuncuya verir. Son kartın 7 ya da 0 ise etki uygulanmaz, eli kazanırsın.' },
      { baslik: 'Renk Ruleti', metin: 'Rengi sıradaki oyuncu seçer; desteden o renk gelene dek kart açılır (jokerler sayılmaz), açılanların hepsini alır ve sırası geçer.' },
      { baslik: 'Joker Yön +4, iki kişilik oyunda', metin: 'Yön dönünce sıra yine sana gelir ve 4 kartlık ceza senin önünde durur: üstüne bir çekme kartı ekleyerek rakibine yollayabilirsin, ekleyemezsen sen çekersin.' },
      { baslik: 'İtiraz yok', metin: 'Bu modda hiçbir karta itiraz edilmez.' },
      UNO_DEMEK,
    ],
    puan: [['Sayı kartı (0–9)', 'Üstündeki sayı'], ['Renkli aksiyonlar (Atlat, Yön, +2, +4, Hepsini At, Herkesi Atlat)', '20'], ['Jokerler (Yön +4, +6, +10, Renk Ruleti)', '50'], ['Elenen her oyuncu', 'Kazanana +250, elenene −250']],
    ipuclari: ['Büyük çekme kartlarını (+6, +10) savunma için sakla: sana gelen cezayı ancak onlarla devredersin.', 'Hepsini At’ı o renkten kart biriktirince oyna; tek hamlede elin erir.', '7’yi en az kartlı rakibe oyna; elin azsa 7 elinde yük olur.', 'Elin 20 karta yaklaştıysa önce kart azalt: bir +6 seni eler.'],
    kaynakNotu: 'Renkli kartların adedi resmî yönergede yazmaz. Burada renk başına 36 kart kullanılır: 0–9 ikişer, Atlat 3, Yön 3, Hepsini At 3, Herkesi Atlat 2, +2 üçer, +4 ikişer. Jokerler: 8 Yön +4, 4 +6, 4 +10, 8 Renk Ruleti.',
  },
  extreme: {
    slogan: 'Deste fırlatıcıda: düğmeye bas, şansına ne fırlarsa.',
    ozet: 'Uno Attack / Extreme: kart çekmek yerine fırlatıcının düğmesine basılır. Bazen hiç kart çıkmaz, bazen bir avuç kart eline fırlar. Vur kartları rakibi düğmeye bastırır.',
    nasil: [
      'Herkese 7 kart dağıtılır, destenin kalanı fırlatıcıya konur. Rengi, sayıyı ya da simgeyi tutturan kartı atarsın.',
      'Oynayacak kartın yoksa (ya da oynamak istemiyorsan) fırlatıcıya bir kez basarsın. Bastığın an sıran biter: fırlayan kartlar o tur oynanmaz.',
      'Vur kartı oynanan oyuncu yazan sayı kadar basar ve sırası geçer; elinde Vur kartı varsa üstüne ekleyip basışları devredebilir.',
      'Tek kartın kalınca UNO dersin; yakalanırsan fırlatıcıya 2 kez basarsın. ' + hedefNot(500),
    ],
    ozelKurallar: [
      { baslik: 'Fırlatıcı nasıl çalışır', metin: 'Her basışta kart fırlama olasılığı %24’ten başlar ve boş geçen her basışla 17 puan artar (en çok %90). Kart fırladığında 2 ile 8 arasında kart gelir ve olasılık başa döner. Birden çok basman gerekiyorsa kart fırladığı anda kalan basışlardan vazgeçilmiş sayılır.' },
      { baslik: 'Üst üste vuruş', metin: 'Sana Vur 1, Vur 2 ya da Çifte Saldırı oynandıysa elindeki herhangi bir Vur kartını rengine bakmadan üstüne ekleyebilirsin: basışlar birikir ve bir sonraki oyuncuya (Çifte Saldırı’da seçtiğin rakibe) geçer. Ekleyemeyen biriken basışların hepsini yapar.' },
      { baslik: 'Vuruştan sonra sıra', metin: 'Tek vuruşta oyun, vurulan oyuncudan sonrakiyle sürer. Üst üste vuruşta oyun, ilk Vur kartını oynayandan sonraki oyuncuyla sürer (o oyuncu az önce basan kişiyse bir sonrakiyle).' },
      { baslik: 'Hepsini At', metin: 'Kartla birlikte elindeki o renkten bütün kartları atarsın. Başka renkten bir Hepsini At’ın üstüne de oynanır.' },
      { baslik: 'İlk kart', metin: 'Joker Çifte Saldırı açılırsa desteye geri konur. Vur 1 ya da Vur 2 açılırsa ilk oyuncu o kadar basar ve sırası geçer. Joker açılırsa ilk oyuncu rengi seçer.' },
      { baslik: 'Son kart', metin: 'Son kartın bir Vur kartıysa hedef yine basar; fırlayan kartlar puana sayılır.' },
    ],
    puan: [['Sayı kartı (1–9)', 'Üstündeki sayı'], ['Yön, Atlat, Vur 1', '20'], ['Hepsini At', '30'], ['Vur 2', '40'], ['Joker, Joker Çifte Saldırı', '50']],
    ipuclari: ['Birkaç boş basıştan sonra fırlatıcı “dolmuştur”: o sırada rakibi bastırmak için Vur kartı oyna.', 'Vur kartlarından birini savunma için elinde tut.', 'Çifte Saldırı’yı en az kartlı rakibe yolla.'],
    kaynakNotu: 'Deste, güncel Attack/Extreme yönergesine (GXY81) göredir: 72 sayı (1–9), 4 Yön, 8 Atlat, 8 Hepsini At, 4 Vur 1, 8 Vur 2, 4 Joker, 4 Çifte Saldırı. Gerçek fırlatıcı mekaniktir; buradaki olasılık modeli ona benzetilmiştir.',
  },
  flex: {
    slogan: 'Güç kartın yeşilse kartı esnet: ikinci renk, ikinci etki.',
    ozet: 'Flex kartlarının köşesinde ikinci bir renk, aksiyonlarında daha güçlü bir ikinci etki vardır. Bu flex yüzünü yalnız güç kartın yeşilken kullanırsın; kullanınca güç kartın kırmızıya döner.',
    nasil: [
      'Herkese 7 kart ve yeşil yüzü açık bir güç kartı verilir. İlk kart sayı olana dek açılır.',
      'Kartlar olağan biçimde (rengi, sayısı ya da simgesi tutunca) oynanır. Oynayamıyorsan 1 kart çekersin; uyuyorsa hemen oynayabilirsin.',
      'Güç kartın yeşilse bir Flex kartını flex yüzüyle oynayabilirsin: flex rengi ortadaki renge uyuyorsa ya da kart zaten uyuyorsa. Flex aksiyonlarda ve flex jokerlerde ikinci etki devreye girer.',
      'Flex yüzünü kullandığında güç kartın kırmızıya döner; kırmızıyken flex yüzü kullanılmaz.',
      hedefNot(500),
    ],
    ozelKurallar: [
      { baslik: 'Geçerli renk', metin: 'Bir kartı flex rengiyle oynasan da oyun, kartın ortadaki asıl rengiyle sürer; flex rengi yalnız kartı oynayabilmeni sağlar.' },
      { baslik: 'Güç kartı ne zaman döner', metin: 'Çevirme simgeli sayıyı (düz 4 ve 8) oynayınca kendi güç kartın döner: yeşilse kırmızı, kırmızıysa yeşil olur. Joker Güçleri Çevir herkesin güç kartını döndürür. Herkesin güç kartı aynı anda kırmızı kalırsa hepsi yeniden yeşile döner.' },
      { baslik: 'Flex aksiyonlar', metin: 'Flex +2: bütün rakipler birer kart çeker, kimse atlanmaz. Flex Atlat: bütün rakipler atlanır. Flex Yön: yön döner ve yeni yöndeki ilk oyuncu atlanır. Düz yüzleri olağan +2, Atlat ve Yön’dür.' },
      { baslik: 'Flex jokerler', metin: 'Düz yüzleri olağan jokerdir. Flex yüzleri: Herkes Çeker (bütün rakipler 2’şer kart), Hedefli +2 (seçtiğin rakip 2 kart, sırası atlanmaz), Flex +4 (seçtiğin rakip 4 kart, itirazsız).' },
      { baslik: 'Flex Joker +4 itirazı (düz yüz)', metin: 'Düz yüzüyle oynanırsa Joker +4’tür ve yalnız elinde ortadaki renkten kart yokken kurala uygundur; itirazda öbür jokerler de o renkten sayılır. Haklı itirazda 4 kartı oynayan çeker, haksız itirazda itiraz eden 6 kart çeker.' },
      UNO_DEMEK,
    ],
    puan: [['Sayı kartı (1–8)', 'Üstündeki sayı'], ['+2, Atlat, Yön (düz ve flex)', '20'], ['Bütün jokerler', '50']],
    ipuclari: ['Gücünü sıradan bir sayı için harcama; rakip 1–2 karta düşünce flex aksiyon için sakla.', 'Güç kartın kırmızıysa çevirme simgeli 4 ya da 8 ile yeniden yeşile çevir.', 'Rakiplerin güç kartlarına bak: yeşil olan seni her an hedefleyebilir.'],
    kaynakNotu: 'Resmî yönerge yalnız “8’i güç kartı 112 kart” der; dağılım yazmaz. Burada 104 kart kullanılır: her renkte 1–8’in bir düz bir flex kopyası (64), +2/Atlat/Yön’ün bir düz bir flex kopyası (24), 4 Herkes Çeker, 4 Hedefli +2, 2 Flex +4, 6 Güçleri Çevir. Çevirme simgesi düz 4 ve 8’dedir; flex renkleri sabit bir düzene göre atanır.',
  },
  takim: {
    slogan: 'Karşındaki oyuncu ortağın: birlikte bitirin.',
    ozet: 'Uno Teams: ikişerli takımlar. Ortaklar birbirine kart verir, Takım Oyunu jokeriyle sırayı birbirine atlatır. Takım, iki ortağın da eli bitince kazanır.',
    nasil: [
      '4, 6 ya da 8 oyuncuyla oynanır; tam karşında oturan oyuncu ortağındır. Herkese 7 kart dağıtılır, ilk kart sayı olana dek açılır.',
      'Oyun başlamadan herkes ortağına 1 kart verir; kartlar aynı anda el değiştirir.',
      'Kartlar olağan biçimde oynanır. Oynayamıyorsan 1 kart çekersin; uyuyorsa hemen oynayabilirsin.',
      'Elin bitince ortağın kartlarının yarısını sana verir ve oynamayı sürdürürsün. Ortağının tek kartı kaldıysa oyundan çıkar, onu beklersin.',
      'Son kart oynandığında iki ortağın da eli boşsa takım eli kazanır. ' + hedefNot(500),
    ],
    ozelKurallar: [
      { baslik: 'Paslaşma simgesi', metin: 'Her renkte 1–5 sayılarının birer kopyasında paslaşma simgesi vardır. Bu kartı oynayınca sen ve ortağın birbirinize birer kart verirsiniz (ikinizin de elinde kart varsa); kartlar aynı anda el değiştirir, oyun bu sırada bekler.' },
      { baslik: 'Takım Oyunu jokeri', metin: 'Rengi seçersin ve sıra doğrudan ortağına atlar; aradaki rakipler oynayamaz. Ortağın uyan bir kartını oynamak zorundadır, oyun ondan sonra sürer. Ortağının uyan kartı yoksa (ya da eli bitmişse) jokeri oynayan 2 kart çeker ve sıra ortağından sonraki oyuncuya geçer.' },
      { baslik: 'Takıma +4', metin: 'Sıradaki oyuncu 2 kart çeker ve sırası geçer; onun ortağı da 2 kart çeker. Ortak eli bitmiş bekliyorsa bu kartlarla oyuna döner.' },
      { baslik: 'Eli biten oyuncu', metin: 'Ortağı kartlarının yarısını verir (tek sayıda büyük parça ortakta kalır: 9 karttan 4’ü verilir). Verilecek kartları ortak tek tek seçer. Ortağın yalnız 1 kartı varsa bir şey verilmez; eli biten oyundan çıkar ve sırası atlanır. Beklerken ortağı herhangi bir nedenle kart çekerse yine yarısını verir ve oyuncu oyuna döner.' },
      { baslik: 'UNO', metin: 'Tek kartı kalan oyuncu UNO der; onun yerine ortağı da diyebilir. Rakipler yakalarsa 2 kart çeker. Ortaklar birbirini yakalayamaz.' },
      { baslik: 'Puan', metin: 'Kazanan takımın iki oyuncusu da rakiplerin elinde kalan kartların toplamını alır; kaybedenler kendi ellerindeki kartların değeri kadar eksi alır.' },
    ],
    puan: [['Sayı kartı (1–9)', 'Üstündeki sayı'], ['Atlat, Yön, +2', '20'], ['Joker, Takım Oyunu, Takıma +4', '50']],
    ipuclari: ['El başında ortağına, elinde çok bulunan renkten bir kart ver: Takım Oyunu’nda o rengi seçersin.', 'Jokerlerini ortağına verme; değersiz sayıları ver.', 'Ortağın çıktıysa kart çekmek onu oyuna geri sokar: bunu rakip için de hesaba kat.', 'Eller uzundur: bir takımın bitirmesi için iki elin de erimesi gerekir.'],
    kaynakNotu: 'Kart adetleri resmî yönergede yazmaz; toplamı 112 eden yaygın döküm kullanılır (72 sayı, 8 +2, 8 Yön, 8 Atlat, 4 Joker, 8 Takım Oyunu, 4 Takıma +4; 20 kartta paslaşma simgesi).',
  },
  yalanci: {
    slogan: 'Kartı kapat, bir şey söyle: inanan oynar, inanmayan “Yalan!” der.',
    ozet: 'Liar’s Uno: destenin yarıdan çoğu “yalancı kartı”dır ve kapalı oynanır. Oynarken kartın ne olduğunu söylersin; doğru olması gerekmez, yalnız ortadaki karta uyan bir şey söylemelisin.',
    nasil: [
      'Herkese 7 kart dağıtılır; ilk kart sayı olana dek açılır. Köşesinde beyaz daire olan kartlar yalancı kartıdır.',
      'Düz kartlar açık oynanır ve ortadaki karta uymalıdır (renk, sayı ya da simge).',
      'Yalancı kartı her zaman kapalı oynanır: bir renk ve değer söylersin. Söylediğin kart ortadakine uymalıdır (aynı renk, aynı değer ya da +4); elindeki kartın gerçekten o olması gerekmez.',
      'Sıradaki oyuncu ya inanır (kart söylendiği gibi sayılır, etkisi uygulanır) ya da “Yalan!” der. Öbür oyuncular da sıradaki karar verene dek “Yalan!” diyebilir.',
      'Oynayacak düz kartın ve yalancı kartın yoksa 1 kart çekersin; istersen kart oynamak yerine de çekebilirsin. ' + hedefNot(500),
    ],
    ozelKurallar: [
      { baslik: '“Yalan!” denince', metin: 'Kart açılır. Söylenen doğruysa kart geçerli olur, etkisi uygulanır ve “Yalan!” diyen 1 kart çeker. Yalansa oynayan kartını geri alır, 1 kart çeker ve sırası geçer; ortadaki kart değişmez.' },
      { baslik: 'İnanılınca', metin: 'Kart kapalı kalır ve söylenen kart sayılır: söylenen +2 ise sıradaki 2 çeker, Atlat ise atlanır, +4 ise 4 çeker ve renk söylenen renk olur. Sonraki oyuncu söylenen karta göre oynar.' },
      { baslik: 'Düz kartı kapalı oynamak', metin: 'Kural dışıdır: yakalanan kartını geri alır ve 6 kart çeker. Bu masada düz kartlar her zaman açık oynatılır; ceza yalnız kuralı tamamlamak için vardır.' },
      { baslik: 'Son kart', metin: 'Son kartını kapalı oynadıysan, inanılırsa eli kazanırsın. “Yalan!” denir ve yalan çıkarsa kartı geri alıp 1 kart çekersin, oyun sürer.' },
      { baslik: '7 takas, 0 devir', metin: '7 oynayan (ya da 7 dediğine inanılan) seçtiği rakiple elini değiştirir; 0’da herkes elini oyun yönündeki oyuncuya verir. 7 ya da 0’a “Yalan!” denip doğru çıkarsa ceza kartı el değişiminden sonra çekilir.' },
      { baslik: 'Joker Meydan Okuma', metin: 'Açık oynanır, bir renk seçilir. Bütün rakipler o renkten olduğunu öne sürerek birer kartı kapalı koyar. Jokeri oynayan dilediği oyuncuyu sırayla sorgular: kartı o renkten değilse geri alır ve 1 kart çeker; doğru renk çıkınca sorgu biter. Sorgulanmayan ve doğru çıkan kartlar jokerin altına girer; böylece elini bitiren eli kazanır (birden çok kişi birlikte kazanabilir). Oyun seçilen renkle, jokeri oynayandan sonraki oyuncuyla sürer.' },
      { baslik: 'Joker +4', metin: 'Yalancı kartıdır, kapalı oynanır ve her karta uyar. Klasik +4 itirazı yoktur; yalnız “Yalan!” denebilir. Üst üste ekleme yapılmaz.' },
      { baslik: 'UNO', metin: 'Tek kartın kalınca UNO dersin; yakalanırsan 2 kart çekersin. Meydan Okuma’da kapalı kart koyarak tek karta düşen oyuncu UNO demiş sayılır.' },
    ],
    puan: [['Sayı kartı (0–9)', 'Üstündeki sayı'], ['Atlat, Yön, +2', '20'], ['Joker +4, Joker Meydan Okuma', '50'], ['Elde kalan kartlar', 'Gerçek değeriyle sayılır']],
    ipuclari: ['Her renk ve sayının yalnız bir yalancı kopyası vardır: söylenen kart senin elindeyse yalan kesindir.', 'Uyan yalancı kartın varsa doğruyu söyle; rakibin boşuna “Yalan!” demesi sana kart kazandırır.', 'Rakibin son kartını kapalı oynuyorsa çoğu zaman “Yalan!” demeye değer.', 'Meydan Okuma’da doğru renkten kartın yoksa en pahalı kartını koy.'],
    kaynakNotu: 'Kart adetleri (40 düz sayı, 40 yalancı sayı, 8 +2, 8 Yön, 8 Atlat, 2 Joker +4, 6 Meydan Okuma) resmî yönergede yazmaz; toplamı 112 eden yaygın döküm kullanılır.',
  },
  yigma: {
    slogan: '+2’ye +2, +4’e +4: ceza büyür, biri hepsini çeker.',
    ozet: 'Klasik deste ve kurallar; tek fark çekme kartlarının üst üste eklenebilmesi.',
    nasil: [
      'Herkese 7 kart dağıtılır; kartlar klasikteki gibi oynanır.',
      'Sana +2 oynandıysa üstüne +2 ya da +4, +4 oynandıysa üstüne yalnız +4 ekleyebilirsin: ceza birikir ve sıradakine geçer (ör. +2, +2, +4 = 8 kart).',
      'Ekleyecek kartı olmayan (ya da eklemek istemeyen) biriken kartların hepsini çeker ve sırası geçer.',
    ],
    ozelKurallar: [
      { baslik: 'İtiraz yok', metin: 'Bu modda +4’e itiraz edilmez; +4 her zaman oynanabilir.' },
      { baslik: 'Son kart', metin: 'Son kartın +2 ya da +4 ise sıradaki, o ana dek birikenle birlikte hemen çeker; kartlar puana sayılır.' },
      ILK_KART_KLASIK, UNO_DEMEK, DENGELI,
    ],
    puan: PUAN_KLASIK,
    ipuclari: ['Bir +2’yi savunma için sakla: sana gelen cezayı devredersin.', '+4 her cezanın üstüne eklenir; en değerli savunma kartındır.'],
  },
  yediSifir: {
    slogan: '7 atan elini değiştirir, 0 atılınca eller döner.',
    ozet: 'Klasik deste ve kurallar; 7 ve 0 kartları elleri yer değiştirir.',
    nasil: [
      'Herkese 7 kart dağıtılır; kartlar klasikteki gibi oynanır.',
      '7 oynayınca bir rakip seçer, elini onunla değiştirirsin.',
      '0 oynanınca herkes elini oyun yönündeki oyuncuya verir.',
    ],
    ozelKurallar: [
      { baslik: 'Takas ve UNO', metin: 'Takas ya da devir sonunda tek karta düşen oyuncu da UNO demelidir; demezse yakalanabilir.' },
      { baslik: 'Son kart', metin: 'Son kartın 7 ya da 0 ise takas ya da devir yapılmaz, eli kazanırsın.' },
      ILK_KART_KLASIK, ITIRAZ4, UNO_DEMEK, DENGELI,
    ],
    puan: PUAN_KLASIK,
    ipuclari: ['7’yi en az kartlı rakibe oyna.', 'Elin azsa 7 ve 0’ı elinde tutma: başkası oynarsa güzel elin gider.'],
  },
  atlama: {
    slogan: 'Tıpkısı elindeyse sıranı bekleme: araya gir.',
    ozet: 'Klasik deste ve kurallar; ortadaki kartın tıpkısını sıra beklemeden atabilirsin.',
    nasil: [
      'Herkese 7 kart dağıtılır; kartlar klasikteki gibi oynanır.',
      'Ortadaki kartın tıpkısı (aynı renk ve aynı sayı ya da simge) elindeyse sıra kimde olursa olsun hemen atabilirsin.',
      'Sıra atlayan oyuncuya geçer ve ondan devam eder; aradaki oyuncular sırasını kaybeder.',
    ],
    ozelKurallar: [
      { baslik: 'Neyle atlanmaz', metin: 'Joker ve +4 ile atlanmaz. Bir karar beklenirken (renk seçimi, +4 itirazı) atlama yapılmaz.' },
      { baslik: 'Etki', metin: 'Atlayarak oynanan kartın etkisi (Atlat, Yön, +2) atlayan oyuncudan sayılır.' },
      ILK_KART_KLASIK, ITIRAZ4, UNO_DEMEK, DENGELI,
    ],
    puan: PUAN_KLASIK,
    ipuclari: ['Elindeki çift kartları hatırla: biri ortaya düşünce öbürüyle araya girersin.', 'Hızlı davranan kazanır; ortadaki kartı sürekli izle.'],
  },
  hizli: {
    slogan: 'Beş kart, kısa el, hemen rövanş.',
    ozet: 'Klasik deste ve kurallar; herkese 7 yerine 5 kart dağıtılır.',
    nasil: ['Herkese 5 kart dağıtılır.', 'Kartlar klasikteki gibi oynanır: rengi, sayıyı ya da simgeyi tuttur; oynayamıyorsan 1 kart çek.', 'Eller kısa sürer; UNO demeyi unutma.'],
    ozelKurallar: [ILK_KART_KLASIK, ITIRAZ4, UNO_DEMEK, DENGELI],
    puan: PUAN_KLASIK,
    ipuclari: ['Az kartla her aksiyon kartı belirleyicidir: Atlat ve +2’yi rakibin tek kartı kalınca kullan.'],
  },
  cekCek: {
    slogan: 'Uyan kart gelene dek çek.',
    ozet: 'Klasik deste ve kurallar; oynayamayan tek kart değil, uyan kart gelene dek çeker.',
    nasil: ['Herkese 7 kart dağıtılır; kartlar klasikteki gibi oynanır.', 'Oynayacak kartın yoksa uyan bir kart gelene dek çekmeye devam edersin.', 'Gelen kartı hemen oynayabilir ya da sırayı geçebilirsin.'],
    ozelKurallar: [ILK_KART_KLASIK, ITIRAZ4, UNO_DEMEK, DENGELI],
    puan: PUAN_KLASIK,
    ipuclari: ['Renk değiştirerek rakibi uzun çekişe sok: destede az kalan rengi seç.', 'Elin kabarabilir; yüksek kartları erken at.'],
  },
  dostlar: {
    slogan: 'Dört sevimli dost, dört özel güç.',
    ozet: 'Klasik 108 kart + 8 karakter kartı. Kedicik hediye verir, Yarasa cezayı siper eder, Yaramaz Tavşan herkese kart çektirir, Gökkuşağı Tayı bir rengin tamamını attırır. +2 ve +4 birikir.',
    nasil: [
      'Herkese 7 kart dağıtılır; kartlar klasikteki gibi oynanır.',
      'Karakter kartları jokerdir: her zaman oynanır, rengi sen seçersin ve kartın özel gücü uygulanır.',
      '+2 ve +4 üst üste eklenir (Yığma kuralı); ekleyemeyen biriken kartların hepsini çeker.',
      'Tek kartın kalınca UNO dersin; son kartını oynayan eli kazanır.',
    ],
    ozelKurallar: [
      { baslik: 'Kedicik: Hediye Paketi', metin: 'Rengi ve bir rakibi seçersin; ona elinden seçtiğin 2 kartı verirsin. Elinde en az 1 kart kalır: 2 kartın varsa 1, tek kartın varsa hiç kart verilmez.' },
      { baslik: 'Yarasa: Gece Siperi', metin: 'Sana ceza birikmişse üstüne oynarsın: ceza tümden silinir, rengi seçersin, sıra olağan ilerler. Ceza yokken oynarsan bütün rakipler atlanır ve yeniden sen oynarsın.' },
      { baslik: 'Yaramaz Tavşan: Şaka', metin: 'Rengi seçersin; bütün rakipler birer kart çeker. Kimsenin sırası geçmez.' },
      { baslik: 'Gökkuşağı Tayı', metin: 'Bir renk seçersin; elindeki o renkten bütün kartlar atılır ve geçerli renk o olur. Elin boşalırsa eli kazanırsın.' },
      { baslik: 'Biriktirme', metin: '+2’nin üstüne +2 ya da +4, +4’ün üstüne yalnız +4 eklenir. Biriken cezanın üstüne karakter kartlarından yalnız Yarasa oynanır. Bu modda +4’e itiraz yoktur.' },
      { baslik: 'İlk kart', metin: 'İlk kart +4 ya da karakter kartı çıkarsa desteye geri konur, yenisi açılır.' },
      UNO_DEMEK, DENGELI,
    ],
    puan: [...PUAN_KLASIK, ['Karakter kartları', '50']],
    ipuclari: ['Yarasa’yı büyük bir ceza gelene dek sakla.', 'Gökkuşağı Tayı’nı elinde en çok bulunan renkle oyna.', 'Kedicik’le jokerlerini değil, elindeki en pahalı fazlalıkları ver; ama jokerler 50 puandır, el bitmek üzereyse onları da gönder.'],
    kaynakNotu: 'Bu mod MeDSor’a özeldir; resmî bir kutu oyunu değildir.',
  },
};
