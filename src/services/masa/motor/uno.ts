/**
 * Uno — saf kural motoru (2–8 oyuncu). Mod başına deste ve kurallar: UNO_MODLAR (tipler.ts) + unoKartlar.ts.
 *  - Klasik aile (klasik, deluxe, hizli, cekCek, atlama, yediSifir, express): resmî kurallar; joker çekme kartına itiraz edilir.
 *  - yigma / dostlar / noMercy: çekme kartları birikir (`yigin`); noMercy'de eşit ya da büyük değer eklenir, 25 kartta elenilir.
 *  - flip: çift yüzlü kart (`arka`), Flip kartı her şeyi çevirir · hepsiJoker: renk yok · extreme: deste fırlatıcıda, Vur kartları birikir
 *  - flex: güç kartı (`guc`) yeşilken flex yüzü · takim: karşılıklı ortaklar, kart verme (`ver`) · yalanci: kapalı kart + beyan (`bekle.yalan`)
 * Dengeli dağıtım (klasik aile): bir ele 2'den çok joker (en çok 1 +4) ya da 3'ten çok aksiyon düşerse fazlası sayı kartıyla değişir.
 * Durum düz JSON; `uygula` girdiyi değiştirmez. Gizlilik: el, öbür yüz ve kapalı kartın gerçeği yalnız `gorunum(bakan)` kurallarıyla gider.
 */
import type { Ceza, ElSatir, ElSonuc, Motor, OdaAyar, Olay, Rng, UnoBekle, UnoBeyan, UnoDeger, UnoGorunum, UnoKart, UnoMod, UnoRenk } from '../tipler';
import { UNO_MODLAR, unoModTanim } from '../tipler';
import { UNO_RENKLER, UNO_TAKAS_MODLAR as TAKAS, hedefGerek, karma, sayiKartiMi, siraOnerisi } from './unoAsistan';
import { CEKME, VURUS, kartPuani, unoDesteKur } from './unoKartlar';

/** Durumdaki kart: `by` = kapalı oynanırken söylenen kimlik (Yalancı) */
type K = UnoKart & { by?: UnoBeyan };

interface VerDurum { neden: 'takim' | 'sembol' | 'yari' | 'hediye'; kalan: { kim: string; kime: string; adet: number }[]; tampon: { kim: string; kime: string; kart: K }[] }
type Bekle =
  | { tur: 'renk'; kim: string; sonra: 'oyna' | 'gec' }
  | { tur: 'itiraz'; oynayan: string; hedef: string; haksiz: boolean; kart: UnoDeger }
  | { tur: 'rulet'; kim: string }
  | { tur: 'yalan'; oynayan: string; kart: number; beyan: UnoBeyan; karar: string; hedef?: string; duz: boolean }
  | { tur: 'meydan'; oynayan: string; renk: UnoRenk; asama: 'koy' | 'sorgu'; katilan: string[]; konan: Record<string, K>; sorgulanan: string[] };

export interface UnoDurum {
  tur: 'uno';
  elNo: number;
  /** Oturma sırasıyla oyuncu kimlikleri */
  oyuncular: string[];
  /** Sırası olanın `oyuncular` dizini */
  kim: number;
  yon: 1 | -1;
  eller: Record<string, K[]>;
  /** Son eleman en üstte */
  deste: K[];
  /** Son eleman en üstte; joker burada da renksiz durur (seçilen renk `aktifRenk`) */
  atik: K[];
  aktifRenk: UnoRenk;
  cektiBuTur: boolean;
  cekilen: number | null;
  unoDedi: string[];
  yakalanabilir: string[];
  cezalar: Record<string, Ceza[]>;
  sonuc: ElSonuc | null;
  mod?: UnoMod;
  /** Biriken çekme cezası (extreme: basış); yiginEn: son çekme kartının değeri (noMercy); yiginIlk/yiginAdet: extreme ilk vuran, vur kartı sayısı */
  yigin?: number;
  yiginEn?: number;
  yiginIlk?: string | null;
  yiginAdet?: number;
  /** Bekleyen karar; ver: bekleyen kart verme (ikisi de normal hamleleri durdurur) */
  bekle?: Bekle | null;
  ver?: VerDurum | null;
  /** flip: etkin yüz */
  taraf?: 'a' | 'k';
  /** noMercy: elenenler */
  elenen?: string[];
  /** extreme: fırlatıcı gerilimi (boş basışlarla artar) */
  gerilim?: number;
  /** flex: güç kartı yeşil mi */
  guc?: Record<string, boolean>;
  /** takim: Takım Oyunu jokerini oynayan (sıradaki ortak oynamak zorunda) */
  takimOyun?: string | null;
}

const MODLAR = UNO_MODLAR.map((m) => m.id);
const mod = (d: UnoDurum): UnoMod => d.mod ?? 'klasik';
/** Dengeli dağıtım ve çekiş koruması uygulanan modlar */
const DENGELI: UnoMod[] = ['klasik', 'yigma', 'yediSifir', 'cekCek', 'atlama', 'hizli', 'deluxe', 'dostlar'];
/** +4'e itiraz edilen modlar */
const DORT_ITIRAZ: UnoMod[] = ['klasik', 'deluxe', 'hizli', 'cekCek', 'atlama', 'yediSifir'];
const YIGAR: UnoMod[] = ['yigma', 'dostlar', 'noMercy'];
/** İlk açılan kart sayı olana dek yenilenen modlar (aksiyon yok sayılır) */
const ILK_SAYI: UnoMod[] = ['noMercy', 'takim', 'flex', 'yalanci'];
const MERCY = 25;
const UNO_CEZA = 2;
const BEYAN_DEGER: UnoDeger[] = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+2', 'yon', 'pas', '+4'];

const ELDE_EN_COK = { joker: 2, dort: 1, aksiyon: 3 };
const jokerMi = (k: UnoKart) => k.renk === null;
const aksiyonMu = (k: UnoKart) => k.renk !== null && !sayiKartiMi(k);

/** [0,n) tam sayı; bozuk rng'de 0 */
const rs = (rng: Rng, n: number): number => { const x = Math.floor(rng() * n); return x >= 0 && x < n ? x : 0; };
function kar<T>(a: T[], rng: Rng): T[] {
  for (let i = a.length - 1; i > 0; i--) { const j = rs(rng, i + 1); [a[i], a[j]] = [a[j], a[i]]; }
  return a;
}
const renkMi = (x: unknown): x is UnoRenk => typeof x === 'string' && (UNO_RENKLER as readonly string[]).includes(x);

/** 108 kart, kimlik 0–107 (karılmamış klasik deste) */
export const unoDeste = (): UnoKart[] => unoDesteKur('klasik');

/** Dağıtım dengesi: sınırı aşan kart destedeki rastgele bir sayı kartıyla yer değiştirir (deste karışık kalır) */
function dengele(el: K[], deste: K[], rng: Rng): void {
  for (let guvenlik = 0; guvenlik < 20; guvenlik++) {
    const j = el.filter(jokerMi), d4 = el.filter((k) => k.deger === '+4'), ak = el.filter(aksiyonMu);
    const fazla = d4.length > ELDE_EN_COK.dort ? d4[0] : j.length > ELDE_EN_COK.joker ? j[0] : ak.length > ELDE_EN_COK.aksiyon ? ak[0] : null;
    if (!fazla) return;
    const adaylar = deste.map((k, i) => (sayiKartiMi(k) ? i : -1)).filter((i) => i >= 0);
    if (!adaylar.length) return;
    const di = adaylar[rs(rng, adaylar.length)];
    const ei = el.indexOf(fazla);
    [el[ei], deste[di]] = [deste[di], el[ei]];
  }
}

/* ------------------------------------------------------------------ sıra ------------------------------------------------------------------ */

const ortak = (d: UnoDurum, id: string): string => { const n = d.oyuncular.length; return d.oyuncular[(d.oyuncular.indexOf(id) + n / 2) % n]; };
/** Sıra alan oyuncu mu: elenmemiş; takım modunda eli bitmiş (ortağını bekleyen) değil */
const oynuyor = (d: UnoDurum, id: string): boolean => !d.elenen?.includes(id) && !(mod(d) === 'takim' && d.eller[id].length === 0);
const aktifSayi = (d: UnoDurum): number => d.oyuncular.filter((id) => oynuyor(d, id)).length;
/** `nereden` dizininden oyun yönünde `adim` etkin oyuncu ileri (0 = aynı oyuncu) */
function ileri(d: UnoDurum, nereden: number, adim = 1): number {
  const n = d.oyuncular.length;
  let i = nereden;
  for (let a = 0; a < adim; a++) {
    for (let g = 0; g < n; g++) { i = (((i + d.yon) % n) + n) % n; if (oynuyor(d, d.oyuncular[i])) break; }
  }
  return i;
}
function gec(d: UnoDurum, adim: number, olaylar: Olay[], nereden = d.kim): void {
  d.kim = ileri(d, nereden, adim);
  d.cektiBuTur = false; d.cekilen = null;
  olaylar.push({ t: 'sira', o: d.oyuncular[d.kim] });
}

/* ------------------------------------------------------------------ çekme ------------------------------------------------------------------ */

/** Bu hamlede desteden kart alanlar (takım: elini bitirmiş ortağa yarı verme tetiklenir) */
let cekenler = new Set<string>();

/** Gizlilik: öbür yüz ve beyan dışarı gitmez */
const acik = (k: K): UnoKart => { const { arka: _a, by: _b, ...y } = k; return y; };
const ustGorunum = (k: K): UnoKart => (k.by ? { id: k.id, renk: k.by.renk, deger: k.by.deger, kp: 1 } : acik(k));
const ust = (d: UnoDurum): K => d.atik[d.atik.length - 1];
/** Eşleşmede geçerli üst değer (kapalı kartta söylenen) */
const ustDeger = (d: UnoDurum): UnoDeger => ust(d).by?.deger ?? ust(d).deger;

/** Tek kart al: deste biterse atık (üstteki hariç) karılıp deste olur; ikisi de boşsa null. */
function al(d: UnoDurum, kime: string, rng: Rng, olaylar: Olay[], sayac: { j: number }): K | null {
  if (!d.deste.length) {
    // Karar bekleyen kapalı kart geri alınabilir: altındaki gerçek üst kart da atıkta kalır
    const kalan = d.bekle?.tur === 'yalan' ? 2 : 1;
    if (d.atik.length <= kalan) return null;
    d.deste = kar(d.atik.splice(0, d.atik.length - kalan), rng);
    for (const k of d.deste) delete k.by;
    olaylar.push({ t: 'karildi', deste: d.deste.length });
  }
  let k = d.deste.pop()!;
  if (DENGELI.includes(mod(d)) && jokerMi(k) && d.eller[kime].filter(jokerMi).length + sayac.j >= 3) {
    const adaylar = d.deste.map((x, i) => (x.renk !== null ? i : -1)).filter((i) => i >= 0);
    if (adaylar.length) { const di = adaylar[rs(rng, adaylar.length)]; [k, d.deste[di]] = [d.deste[di], k]; }
  }
  if (jokerMi(k)) sayac.j++;
  d.eller[kime].push(k);
  cekenler.add(kime);
  return k;
}
function cekOlay(kime: string, kartlar: K[], neden: string, olaylar: Olay[]): void {
  olaylar.push({ t: 'cekti', o: kime, adet: kartlar.length, neden });
  if (kartlar.length) olaylar.push({ t: 'cektim', kime, kartlar: kartlar.map(acik) });
}
const dolu = (d: UnoDurum, id: string) => mod(d) === 'noMercy' && d.eller[id].length >= MERCY;

function cek(d: UnoDurum, kime: string, adet: number, neden: string, rng: Rng, olaylar: Olay[]): K[] {
  const kartlar: K[] = [];
  const sayac = { j: 0 };
  for (let i = 0; i < adet && !dolu(d, kime); i++) { const k = al(d, kime, rng, olaylar, sayac); if (!k) break; kartlar.push(k); }
  cekOlay(kime, kartlar, neden, olaylar);
  return kartlar;
}
/** `uygun` kart gelene dek çek (o kart dahil); deste biterse ya da el dolarsa durur */
function geleneCek(d: UnoDurum, kime: string, uygun: (k: K) => boolean, neden: string, rng: Rng, olaylar: Olay[]): K[] {
  const kartlar: K[] = [];
  const sayac = { j: 0 };
  for (let i = 0; i < 120 && !dolu(d, kime); i++) { const k = al(d, kime, rng, olaylar, sayac); if (!k) break; kartlar.push(k); if (uygun(k)) break; }
  cekOlay(kime, kartlar, neden, olaylar);
  return kartlar;
}
/** Extreme fırlatıcı: her basışta gerilime bağlı olasılıkla 2–8 kart fırlar; kart fırlayınca kalan basışlardan vazgeçilir. */
function firlat(d: UnoDurum, kime: string, basis: number, neden: string, rng: Rng, olaylar: Olay[]): number {
  let bos = 0;
  for (let b = 0; b < basis; b++) {
    const g = d.gerilim || 0;
    if (rng() < Math.min(0.9, 0.24 + 0.17 * g)) {
      d.gerilim = 0;
      const adet = 2 + Math.floor(rng() * rng() * 7);
      olaylar.push({ t: 'firlat', o: kime, adet, bos, neden });
      return cek(d, kime, adet, 'firlat', rng, olaylar).length;
    }
    d.gerilim = g + 1; bos++;
  }
  olaylar.push({ t: 'firlat', o: kime, adet: 0, bos, neden });
  return 0;
}

/* ------------------------------------------------------------------ eşleşme ------------------------------------------------------------------ */

/** Birikmiş cezanın üstüne eklenebilir mi */
function yiginUyar(d: UnoDurum, kart: K): boolean {
  const m = mod(d);
  if (m === 'extreme') return !!VURUS[kart.deger];
  if (m === 'noMercy') return kart.deger !== 'rulet' && (CEKME[kart.deger] ?? 0) >= (d.yiginEn || 1);
  if (m === 'dostlar' && kart.deger === 'batman') return true;
  return kart.deger === '+4' || (kart.deger === '+2' && ustDeger(d) === '+2');
}
const duzUyar = (d: UnoDurum, kart: K): boolean => kart.renk === null || kart.renk === d.aktifRenk || kart.deger === ustDeger(d);
/** Flex yüzüyle oynanabilir mi (güç yeşil, kart flex) */
const flexUyar = (d: UnoDurum, o: string, kart: K): boolean =>
  mod(d) === 'flex' && !!kart.fx && !!d.guc?.[o] && (kart.fx === 'j' || kart.fx === d.aktifRenk || duzUyar(d, kart));
/** Oynanabilirlik (mod ve biriken ceza dahil); Yalancı'da yalancı kartı her zaman kapalı oynanabilir */
function uyar(d: UnoDurum, o: string, kart: K): boolean {
  const m = mod(d);
  if (d.yigin) return yiginUyar(d, kart);
  if (m === 'hepsiJoker') return true;
  if (m === 'yalanci' && kart.yl) return true;
  return duzUyar(d, kart) || flexUyar(d, o, kart);
}
/** Atlama modu: ortadaki kartın tıpkısı (renkli) sıra beklemeden atılabilir */
const tipki = (d: UnoDurum, k: K) => { const u = ust(d); return mod(d) === 'atlama' && k.renk !== null && k.renk === u.renk && k.deger === u.deger && !d.yigin && !d.bekle; };
/* ------------------------------------------------------------------ el sonu ------------------------------------------------------------------ */

function elSonucu(d: UnoDurum, kazananlar: string[]): ElSonuc {
  const m = mod(d);
  const elenen = d.elenen ?? [];
  const deger = (id: string) => d.eller[id].reduce((t, k) => t + kartPuani(k, m), 0);
  const toplam = d.oyuncular.filter((id) => !kazananlar.includes(id) && !elenen.includes(id)).reduce((t, id) => t + deger(id), 0) + elenen.length * 250;
  const satirlar: ElSatir[] = d.oyuncular.map((id) => {
    const kazandi = kazananlar.includes(id);
    const kalan = d.eller[id].length;
    const cezalar = d.cezalar[id] ?? [];
    const cz = cezalar.length ? ` · ${cezalar.length} UNO cezası` : '';
    if (kazandi) return { id, puan: toplam, kalan, kazandi, cezalar, aciklama: `${kalan ? 'Kazandı' : 'Eli bitirdi'} (+${toplam})${cz}` };
    if (elenen.includes(id)) return { id, puan: -250, kalan: 0, kazandi, cezalar, aciklama: `25 karta ulaşıp elendi (−250)${cz}` };
    return { id, puan: 0 - deger(id), kalan, kazandi, cezalar, aciklama: `${kalan} kart (−${deger(id)})${cz}` };
  });
  return { neden: 'bitti', kazananlar, satirlar };
}
function bitir(d: UnoDurum, kazananlar: string[], olaylar: Olay[]): void {
  d.bekle = null; d.ver = null; d.yigin = 0;
  d.sonuc = elSonucu(d, kazananlar);
  olaylar.push({ t: 'elBitti', kazanan: kazananlar[0], kazananlar });
}

/* ------------------------------------------------------------------ el başı ------------------------------------------------------------------ */

function elBaslat(g: { oyuncular: { id: string }[]; elNo: number; baslayan: number; rng: Rng; ayar?: Partial<OdaAyar> }): UnoDurum {
  const oyuncular = g.oyuncular.map((o) => o.id);
  const n = oyuncular.length;
  if (n < 2 || n > 8 || new Set(oyuncular).size !== n) throw new Error('Uno 2–8 farklı oyuncuyla oynanır.');
  const m: UnoMod = MODLAR.includes(g.ayar?.unoMod as UnoMod) ? (g.ayar!.unoMod as UnoMod) : 'klasik';
  if (m === 'takim' && (n < 4 || n % 2)) throw new Error('Takım modu 4, 6 ya da 8 oyuncuyla oynanır.');
  const deste: K[] = kar(unoDesteKur(m, g.rng), g.rng);
  const elKart = unoModTanim(m).elKart;
  const eller: Record<string, K[]> = {};
  const cezalar: Record<string, Ceza[]> = {};
  for (const id of oyuncular) { eller[id] = deste.splice(deste.length - elKart, elKart); cezalar[id] = []; if (DENGELI.includes(m)) dengele(eller[id], deste, g.rng); }
  // İlk kart: geri konup yenilenenler (mod başına); kalan kartların etkisi ilk oyuncuya uygulanır
  const yenile = (k: K): boolean =>
    ILK_SAYI.includes(m) ? !sayiKartiMi(k)
      : m === 'hepsiJoker' ? false
        : ['+4', 'joker+2', 'flip', 'jokerVur', 'kitty', 'batman', 'kuromi', 'pony'].includes(k.deger);
  let ilk = deste.pop()!;
  for (let i = 0; yenile(ilk) && i < 400; i++) { deste.splice(rs(g.rng, deste.length), 0, ilk); ilk = deste.pop()!; }
  if (yenile(ilk)) { deste.push(ilk); ilk = deste.splice(deste.findIndex(sayiKartiMi), 1)[0]; } // bozuk rng güvencesi
  const b = Number.isInteger(g.baslayan) ? ((g.baslayan % n) + n) % n : 0;
  const d: UnoDurum = {
    tur: 'uno', elNo: g.elNo, oyuncular, kim: b, yon: 1, eller, deste, atik: [ilk], aktifRenk: ilk.renk ?? 'k',
    cektiBuTur: false, cekilen: null, unoDedi: [], yakalanabilir: [], cezalar, sonuc: null, mod: m, yigin: 0, yiginEn: 0, bekle: null, ver: null,
  };
  if (m === 'flip') d.taraf = 'a';
  if (m === 'noMercy') d.elenen = [];
  if (m === 'extreme') d.gerilim = 0;
  if (m === 'flex') d.guc = Object.fromEntries(oyuncular.map((id) => [id, true]));
  if (m === 'takim') d.ver = { neden: 'takim', kalan: oyuncular.map((id) => ({ kim: id, kime: ortak(d, id), adet: 1 })), tampon: [] };
  if (m === 'hepsiJoker') return d; // ilk kartın etkisi yok sayılır
  const bos: Olay[] = [];
  if (ilk.renk === null) d.bekle = { tur: 'renk', kim: oyuncular[b], sonra: 'oyna' };
  else if (ilk.deger === 'pas') d.kim = ileri(d, b);
  else if (ilk.deger === 'yon') { d.yon = -1; d.kim = ileri(d, b); } // dağıtan (ilk oyuncunun solundaki) başlar, sıra ters döner; 2 kişide atlat
  else if (ilk.deger === '+2' || ilk.deger === '+1') { cek(d, oyuncular[b], CEKME[ilk.deger]!, ilk.deger, g.rng, bos); d.kim = ileri(d, b); }
  else if (ilk.deger === 'vur1' || ilk.deger === 'vur2') { firlat(d, oyuncular[b], VURUS[ilk.deger]!, 'vur', g.rng, bos); d.kim = ileri(d, b); }
  return d;
}

/* ------------------------------------------------------------------ kart etkisi ------------------------------------------------------------------ */

interface Oyun {
  o: string; deger: UnoDeger;
  /** Kartın kendi rengi (joker: null) ve geçerli olacak renk */
  renkli: UnoRenk | null; renk: UnoRenk;
  hedef?: string; flex: boolean; haksiz: boolean; ps?: boolean; cv?: boolean;
}

/** Flip: atık, deste ve bütün eller ters döner; yeni üst kart eski en alttaki kartın öbür yüzüdür */
function cevir(d: UnoDurum): void {
  const dondur = (k: K): K => (k.arka ? { id: k.id, ...k.arka, arka: { renk: k.renk, deger: k.deger, ...(k.t ? { t: k.t } : {}) } } : k);
  d.atik = d.atik.map(dondur).reverse();
  d.deste = d.deste.map(dondur).reverse();
  for (const id of d.oyuncular) d.eller[id] = d.eller[id].map(dondur);
  d.taraf = d.taraf === 'k' ? 'a' : 'k';
}

/** En az kartlı etkin rakip (eşitlikte oyun yönünde en yakın) */
function enAzRakip(d: UnoDurum, o: string): string {
  const ben = d.oyuncular.indexOf(o), n = d.oyuncular.length;
  return d.oyuncular.filter((id) => id !== o && oynuyor(d, id))
    .map((id) => ({ id, n: d.eller[id].length, s: ((((d.oyuncular.indexOf(id) - ben) * d.yon) % n) + n) % n }))
    .sort((a, b) => a.n - b.n || a.s - b.s)[0]?.id ?? o;
}

/** Kart atığa konduktan sonra etkisini uygular; sırayı ilerletir ya da eli bitirir. */
function etki(d: UnoDurum, p: Oyun, rng: Rng, olaylar: Olay[]): void {
  const m = mod(d);
  const el = d.eller[p.o];
  const ben = d.oyuncular.indexOf(p.o);
  const D = p.deger;
  const N = aktifSayi(d) + (oynuyor(d, p.o) ? 0 : 1); // eli az önce biten (takım) oyuncu da sayılır
  d.kim = ben;
  d.takimOyun = null;
  let bitti = el.length === 0;
  let adim = 1;
  /** sabit: sıra elle atandı · dur: karar bekleniyor, sıra ilerlemez */
  let sabit = false, dur = false;
  let kazanan: string[] | null = null;
  const sonrakiId = () => d.oyuncular[ileri(d, ben)];
  const digerleri = () => d.oyuncular.filter((id) => id !== p.o && oynuyor(d, id));
  const atlat = () => { if (!bitti) olaylar.push({ t: 'atlandi', o: sonrakiId() }); };

  if (m === 'flex' && d.guc) {
    if (p.flex) { d.guc[p.o] = false; olaylar.push({ t: 'guc', o: p.o, acik: false }); }
    else if (p.cv) { d.guc[p.o] = !d.guc[p.o]; olaylar.push({ t: 'guc', o: p.o, acik: d.guc[p.o] }); }
    if (D === 'jokerCevir') { for (const id of d.oyuncular) d.guc[id] = !d.guc[id]; olaylar.push({ t: 'gucHepsi', o: p.o, cevir: true }); }
    if (d.oyuncular.every((id) => !d.guc![id])) { for (const id of d.oyuncular) d.guc[id] = true; olaylar.push({ t: 'gucHepsi', o: p.o }); }
  }

  if (D === 'yon' || D === 'jokerYon') {
    d.yon = d.yon === 1 ? -1 : 1;
    olaylar.push({ t: 'yon', yon: d.yon });
    if (p.flex || N === 2) { atlat(); adim = 2; }
  } else if (D === 'pas' || D === 'jokerPas') {
    if (p.flex) adim = 0; else { atlat(); adim = 2; }
  } else if (D === 'pasHerkes' || (D === 'batman' && !d.yigin)) {
    adim = 0;
    if (!bitti) olaylar.push({ t: 'herkesAtlandi', o: p.o });
  } else if (D === 'batman') {
    d.yigin = 0; d.yiginEn = 0;
    olaylar.push({ t: 'siper', o: p.o });
  } else if (D === 'jokerPas2') {
    atlat();
    adim = N === 2 ? 2 : 3;
  } else if (D === '+2' && p.flex) {
    for (const id of digerleri()) cek(d, id, 1, '+1', rng, olaylar);
  } else if (D === 'fxHerkes' && p.flex) {
    for (const id of digerleri()) cek(d, id, 2, '+2', rng, olaylar);
  } else if (D === 'kuromi') {
    for (const id of digerleri()) cek(d, id, 1, '+1', rng, olaylar);
  } else if ((D === 'jokerHedef2' || (D === 'fxHedef2' && p.flex)) && p.hedef) {
    cek(d, p.hedef, 2, '+2', rng, olaylar);
  } else if (D === 'fx+4' && p.flex && p.hedef) {
    cek(d, p.hedef, 4, '+4', rng, olaylar);
  } else if (D === 'jokerTakim4') {
    const s = sonrakiId();
    cek(d, s, 2, '+2', rng, olaylar);
    const so = ortak(d, s);
    if (so !== s) cek(d, so, 2, '+2', rng, olaylar);
    adim = 2;
  } else if (CEKME[D] && !(D === 'fx+4' && p.flex)) {
    const v = CEKME[D]!;
    if (D === 'jokerYon4') { d.yon = d.yon === 1 ? -1 : 1; olaylar.push({ t: 'yon', yon: d.yon }); }
    const itirazli = (D === '+4' && DORT_ITIRAZ.includes(m)) || (D === 'joker+2' && (m === 'flip' || m === 'express')) || (D === 'fx+4' && m === 'flex');
    if (YIGAR.includes(m) && !bitti) {
      d.yigin = (d.yigin || 0) + v; d.yiginEn = v;
      olaylar.push({ t: 'yigin', adet: d.yigin });
      if (D === 'jokerYon4' && N === 2) adim = 0; // iki kişide ceza oynayana döner; üstüne ekleyerek rakibe yollayabilir
    } else if (itirazli && !bitti) {
      d.bekle = { tur: 'itiraz', oynayan: p.o, hedef: sonrakiId(), haksiz: p.haksiz, kart: D };
    } else {
      adim = 2; // son kart olsa da sıradaki çeker (puan için)
      cek(d, sonrakiId(), v + (d.yigin || 0), D, rng, olaylar);
      d.yigin = 0; d.yiginEn = 0;
    }
  } else if (D === 'jokerRenk') {
    if (bitti) geleneCek(d, sonrakiId(), (k) => k.renk === p.renk, 'renkCek', rng, olaylar);
    else d.bekle = { tur: 'itiraz', oynayan: p.o, hedef: sonrakiId(), haksiz: p.haksiz, kart: D };
  } else if (D === 'rulet') {
    if (!bitti) d.bekle = { tur: 'rulet', kim: sonrakiId() };
  } else if (D === 'flip') {
    cevir(d);
    olaylar.push({ t: 'flip', taraf: d.taraf, ust: ustGorunum(ust(d)) });
    const u = ust(d);
    if (u.renk) d.aktifRenk = u.renk;
    else if (!bitti) { d.bekle = { tur: 'renk', kim: p.o, sonra: 'gec' }; dur = true; }
  } else if (D === 'hepsiAt' || D === 'pony') {
    const renk = D === 'pony' ? p.renk : p.renkli;
    const at = el.filter((k) => k.renk === renk);
    if (at.length) {
      d.eller[p.o] = el.filter((k) => k.renk !== renk);
      d.atik.splice(d.atik.length - 1, 0, ...at);
      olaylar.push({ t: 'attiHepsi', o: p.o, adet: at.length, kartlar: at.map(acik) });
      bitti = d.eller[p.o].length === 0;
    }
  } else if (VURUS[D]) {
    const v = VURUS[D]!;
    const hedef = D === 'jokerVur' && p.hedef ? p.hedef : sonrakiId();
    if (bitti) { firlat(d, hedef, v + (d.yigin || 0), 'vur', rng, olaylar); d.yigin = 0; }
    else {
      if (!d.yigin) { d.yiginIlk = p.o; d.yiginAdet = 0; }
      d.yigin = (d.yigin || 0) + v; d.yiginAdet = (d.yiginAdet || 0) + 1;
      olaylar.push({ t: 'yigin', adet: d.yigin, vur: true });
      d.kim = d.oyuncular.indexOf(hedef); sabit = true;
      d.cektiBuTur = false; d.cekilen = null;
      olaylar.push({ t: 'sira', o: hedef });
    }
  } else if (D === 'jokerTakas' || (D === '7' && TAKAS.includes(m) && !bitti)) {
    const hid = p.hedef && p.hedef !== p.o && oynuyor(d, p.hedef) ? p.hedef : enAzRakip(d, p.o);
    if (hid !== p.o) {
      [d.eller[p.o], d.eller[hid]] = [d.eller[hid], d.eller[p.o]];
      olaylar.push({ t: 'takas', o: p.o, hedef: hid });
      // Zorunlu Takas son kartsa takas yine yapılır: boş eli alan kazanır
      if (bitti) { kazanan = [hid]; bitti = false; }
    }
  } else if (D === '0' && TAKAS.includes(m) && !bitti) {
    const sira = d.oyuncular.filter((id) => oynuyor(d, id));
    const eski = sira.map((id) => d.eller[id]);
    const k = sira.length;
    sira.forEach((_, j) => { d.eller[sira[(((j + d.yon) % k) + k) % k]] = eski[j]; });
    olaylar.push({ t: 'devir', o: p.o, yon: d.yon });
  } else if (D === 'jokerTakim') {
    const o2 = ortak(d, p.o);
    olaylar.push({ t: 'takimOyun', o: p.o, hedef: o2 });
    const oi = d.oyuncular.indexOf(o2);
    if (d.eller[o2].some((k) => duzUyar(d, k))) {
      d.kim = oi; d.takimOyun = p.o; sabit = true;
      d.cektiBuTur = false; d.cekilen = null;
      olaylar.push({ t: 'sira', o: o2 });
    } else {
      // Ortak oynayamıyor: jokeri oynayan 2 çeker, sıra ortaktan sonrakine geçer
      cek(d, p.o, 2, 'takim', rng, olaylar);
      bitti = false;
      gec(d, 1, olaylar, oi); sabit = true;
    }
  } else if (D === 'kitty') {
    const adet = Math.min(2, el.length - 1);
    if (adet > 0 && p.hedef) d.ver = { neden: 'hediye', kalan: [{ kim: p.o, kime: p.hedef, adet }], tampon: [] };
  } else if (D === 'jokerMeydan') {
    const katilan = d.oyuncular.filter((id) => id !== p.o && oynuyor(d, id) && d.eller[id].length > 0);
    if (!bitti && katilan.length) {
      d.bekle = { tur: 'meydan', oynayan: p.o, renk: p.renk, asama: 'koy', katilan, konan: {}, sorgulanan: [] };
      olaylar.push({ t: 'meydan', o: p.o, renk: p.renk });
      dur = true;
    }
  }

  // Takım: paslaşma simgeli kart → oynayan ve ortağı birer kart verir (ikisinin de kartı varsa)
  if (m === 'takim' && p.ps && !d.ver) {
    const o2 = ortak(d, p.o);
    if (d.eller[p.o].length && d.eller[o2].length) d.ver = { neden: 'sembol', kalan: [{ kim: p.o, kime: o2, adet: 1 }, { kim: o2, kime: p.o, adet: 1 }], tampon: [] };
  }

  if (kazanan) return bitir(d, kazanan, olaylar);
  if (bitti && m !== 'takim') return bitir(d, [p.o], olaylar);
  if (sabit || dur) return;
  gec(d, adim, olaylar, ben);
}

/** Yalancı Meydan Okuması biter: kalan kapalı kartlar jokerin altına girer, eli biten(ler) kazanır */
function meydanBitir(d: UnoDurum, b: Extract<Bekle, { tur: 'meydan' }>, olaylar: Olay[]): void {
  const kalan = Object.keys(b.konan);
  d.atik.splice(d.atik.length - 1, 0, ...kalan.map((id) => b.konan[id]));
  d.aktifRenk = b.renk;
  d.bekle = null;
  olaylar.push({ t: 'meydanBitti', o: b.oynayan, kalan });
  const biten = kalan.filter((id) => d.eller[id].length === 0);
  if (biten.length) return bitir(d, biten, olaylar);
  for (const id of kalan) if (d.eller[id].length === 1 && !d.unoDedi.includes(id)) d.unoDedi.push(id);
  gec(d, 1, olaylar, d.oyuncular.indexOf(b.oynayan));
}

/** Hamle sonu: elenme (No Mercy), takımda el bitirme / yarı verme, UNO durumu */
function sonIslem(d: UnoDurum, onceEl: Record<string, number>, olaylar: Olay[], oynayan: string | null): void {
  const m = mod(d);
  if (!d.sonuc && m === 'noMercy') {
    for (const id of d.oyuncular) {
      if (d.eller[id].length < MERCY || d.elenen!.includes(id)) continue;
      // Elenenin kartları kenara ayrılır: atığın altına girer, deste yeniden karılınca oyuna döner
      d.atik.unshift(...d.eller[id].splice(0));
      d.elenen!.push(id);
      olaylar.push({ t: 'elendi', o: id });
    }
    const kalan = d.oyuncular.filter((id) => !d.elenen!.includes(id));
    if (kalan.length === 1) bitir(d, kalan, olaylar);
    else if (d.elenen!.includes(d.oyuncular[d.kim])) {
      if (d.bekle && 'kim' in d.bekle && d.elenen!.includes(d.bekle.kim)) d.bekle = null;
      d.yigin = 0; d.yiginEn = 0;
      gec(d, 1, olaylar);
    }
  }
  if (!d.sonuc && m === 'takim') {
    for (const id of d.oyuncular) {
      const o2 = ortak(d, id);
      if (d.eller[id].length) continue;
      if (d.ver?.kalan.some((x) => x.kime === id) ) continue;
      if (!d.eller[o2].length) {
        // İki ortağın da eli boş: eli son bitirenin takımı kazanır
        if (onceEl[id] > 0 || onceEl[o2] > 0) { bitir(d, [id, o2].sort((a, b) => d.oyuncular.indexOf(a) - d.oyuncular.indexOf(b)), olaylar); break; }
        continue;
      }
      const yeniBitti = onceEl[id] > 0;
      if (!yeniBitti && !cekenler.has(o2)) continue;
      const adet = Math.floor(d.eller[o2].length / 2);
      if (adet < 1) { if (yeniBitti) olaylar.push({ t: 'cikti', o: id }); continue; }
      // Ortak kartlarının yarısını verir (büyük parça kendisinde kalır); eli biten oyuna döner
      const giris = { kim: o2, kime: id, adet };
      if (d.ver) d.ver.kalan.push(giris); else d.ver = { neden: 'yari', kalan: [giris], tampon: [] };
      olaylar.push({ t: 'dondu', o: id, veren: o2, adet });
    }
    if (!d.sonuc && !oynuyor(d, d.oyuncular[d.kim]) && !d.bekle && aktifSayi(d) > 0) { d.takimOyun = null; gec(d, 1, olaylar); }
  }
  // Kart sayısı 1'den farklı olunca UNO durumu sıfırlanır
  const tek = (id: string) => d.eller[id].length === 1;
  // Bu hamlede (takas, devir, Hepsini At, kart verme…) tek karta düşen de UNO demelidir; oynarken "UNO" diyen oynayan demiş sayılır
  if (!d.sonuc) for (const id of d.oyuncular) {
    if (!tek(id) || onceEl[id] === 1 || d.unoDedi.includes(id) || d.yakalanabilir.includes(id)) continue;
    if (id === oynayan) { d.unoDedi.push(id); olaylar.push({ t: 'uno', o: id }); } else d.yakalanabilir.push(id);
  }
  d.unoDedi = d.unoDedi.filter(tek);
  d.yakalanabilir = d.yakalanabilir.filter(tek);
}

/* ------------------------------------------------------------------ hamle ------------------------------------------------------------------ */

function uygula(durum: unknown, oyuncu: string, hamle: unknown, rng: Rng): { durum: unknown; olaylar: Olay[] } | { hata: string } {
  try {
    const d = structuredClone(durum) as UnoDurum;
    if (!d || d.tur !== 'uno' || !Array.isArray(d.oyuncular)) return { hata: 'Oyun durumu okunamadı.' };
    if (d.sonuc) return { hata: 'El bitti.' };
    if (typeof oyuncu !== 'string' || !d.oyuncular.includes(oyuncu)) return { hata: 'Bu oyunda değilsin.' };
    if (!hamle || typeof hamle !== 'object') return { hata: 'Geçersiz hamle.' };
    if (d.elenen?.includes(oyuncu)) return { hata: '25 karta ulaşıp elendin: bu eli izliyorsun.' };
    const h = hamle as { t?: unknown; kart?: unknown; renk?: unknown; uno?: unknown; hedef?: unknown; flex?: unknown; kapali?: unknown; beyan?: unknown };
    const olaylar: Olay[] = [];
    const m = mod(d);
    const siraBende = d.oyuncular[d.kim] === oyuncu;
    const el = d.eller[oyuncu];
    const onceEl = Object.fromEntries(d.oyuncular.map((id) => [id, d.eller[id].length]));
    const b = d.bekle ?? null;
    cekenler = new Set();
    const hedefGecerli = (x: unknown): x is string => typeof x === 'string' && x !== oyuncu && d.oyuncular.includes(x) && oynuyor(d, x);

    if (h.t === 'oyna' || h.t === 'cek' || h.t === 'pas') {
      if (d.ver) return { hata: d.ver.kalan.some((x) => x.kim === oyuncu) ? 'Önce vereceğin kartı seç.' : 'Kart verilmesi bekleniyor.' };
      if (b) {
        return { hata: b.tur === 'renk' ? (b.kim === oyuncu ? 'Önce rengi seç.' : 'Renk seçilmesi bekleniyor.')
          : b.tur === 'itiraz' ? (b.hedef === oyuncu ? 'Joker çekme kartı sana oynandı: kabul et ya da itiraz et.' : 'İtiraz kararı bekleniyor.')
            : b.tur === 'rulet' ? (b.kim === oyuncu ? 'Renk Ruleti: önce bir renk seç.' : 'Renk Ruleti için renk seçilmesi bekleniyor.')
              : b.tur === 'yalan' ? 'Kapalı kart için karar bekleniyor: inan ya da yalan de.'
                : 'Meydan okuma sürüyor.' };
      }
    }

    if (h.t === 'renk') {
      if (!b || (b.tur !== 'renk' && b.tur !== 'rulet') || b.kim !== oyuncu) return { hata: 'Şu an renk seçilmez.' };
      if (!renkMi(h.renk)) return { hata: 'Geçersiz renk.' };
      const renk = h.renk;
      d.aktifRenk = renk; d.bekle = null;
      olaylar.push({ t: 'renk', renk, o: oyuncu });
      if (b.tur === 'rulet') {
        // Renk Ruleti: seçilen renk gelene dek açılan bütün kartlar alınır, sıra geçer
        const kartlar = geleneCek(d, oyuncu, (k) => k.renk === renk, 'rulet', rng, olaylar);
        olaylar.push({ t: 'rulet', o: oyuncu, renk, adet: kartlar.length });
        gec(d, 1, olaylar);
      } else if (b.sonra === 'gec') gec(d, 1, olaylar);
    } else if (h.t === 'kabul' || h.t === 'itiraz') {
      if (!b || b.tur !== 'itiraz' || b.hedef !== oyuncu) return { hata: 'İtiraz edilecek bir kart yok.' };
      d.bekle = null;
      const renkCek = b.kart === 'jokerRenk';
      const v = CEKME[b.kart] ?? 4;
      const renk = d.aktifRenk;
      const cektir = (kime: string, ek: number, neden: string) => {
        if (renkCek) { geleneCek(d, kime, (k) => k.renk === renk, neden, rng, olaylar); if (ek) cek(d, kime, ek, neden, rng, olaylar); }
        else cek(d, kime, v + ek, neden, rng, olaylar);
      };
      if (h.t === 'kabul') {
        cektir(oyuncu, 0, renkCek ? 'renkCek' : b.kart);
        gec(d, 1, olaylar);
      } else if (b.haksiz) {
        // İtiraz haklı: kartı kuralsız oynayan çeker, itiraz eden normal oynar
        olaylar.push({ t: 'itiraz', o: oyuncu, hedef: b.oynayan, hakli: true, adet: renkCek ? 0 : v });
        cektir(b.oynayan, 0, 'itiraz');
      } else {
        olaylar.push({ t: 'itiraz', o: oyuncu, hedef: b.oynayan, hakli: false, adet: renkCek ? 0 : v + 2 });
        cektir(oyuncu, 2, 'itiraz');
        gec(d, 1, olaylar);
      }
    } else if (h.t === 'uno') {
      // Takım modunda ortak da "UNO" diyebilir
      const kim = d.yakalanabilir.includes(oyuncu) ? oyuncu : m === 'takim' && d.yakalanabilir.includes(ortak(d, oyuncu)) ? ortak(d, oyuncu) : null;
      if (!kim) return { hata: 'UNO diyecek durumda değilsin.' };
      d.yakalanabilir = d.yakalanabilir.filter((x) => x !== kim);
      d.unoDedi.push(kim);
      olaylar.push({ t: 'uno', o: kim });
    } else if (h.t === 'yakala') {
      const hedef = h.hedef;
      if (typeof hedef !== 'string' || !d.oyuncular.includes(hedef)) return { hata: 'Yakalanacak oyuncu bulunamadı.' };
      if (hedef === oyuncu) return { hata: 'Kendini yakalayamazsın.' };
      if (m === 'takim' && ortak(d, oyuncu) === hedef) return { hata: 'Ortağını yakalayamazsın; onun yerine UNO diyebilirsin.' };
      if (!d.yakalanabilir.includes(hedef)) return { hata: 'Yakalanacak kimse yok.' };
      d.cezalar[hedef].push({ tur: 'uno', puan: 0, aciklama: 'UNO demedi' });
      olaylar.push({ t: 'yakalandi', o: hedef, yakalayan: oyuncu });
      if (m === 'extreme') firlat(d, hedef, 2, 'yakalandi', rng, olaylar);
      else cek(d, hedef, UNO_CEZA, 'yakalandi', rng, olaylar);
      d.yakalanabilir = d.yakalanabilir.filter((x) => x !== hedef); // deste boşsa kart gelmeyebilir; yine de bir kez yakalanır
    } else if (h.t === 'ver') {
      const v = d.ver;
      const g = v?.kalan.find((x) => x.kim === oyuncu);
      if (!v || !g) return { hata: 'Şu an kart vermen gerekmiyor.' };
      const i = typeof h.kart === 'number' ? el.findIndex((k) => k.id === h.kart) : -1;
      if (i < 0) return { hata: 'Bu kart elinde yok.' };
      v.tampon.push({ kim: oyuncu, kime: g.kime, kart: el.splice(i, 1)[0] });
      if (--g.adet <= 0) v.kalan = v.kalan.filter((x) => x !== g);
      olaylar.push({ t: 'verdi', o: oyuncu, hedef: g.kime, adet: 1, kalan: g.adet });
      if (!v.kalan.length) {
        // Hepsi verildi: kartlar aynı anda el değiştirir
        const alan = new Map<string, K[]>();
        for (const t of v.tampon) { d.eller[t.kime].push(t.kart); alan.set(t.kime, [...(alan.get(t.kime) ?? []), t.kart]); }
        for (const [kime, kartlar] of alan) olaylar.push({ t: 'aldim', kime, kartlar: kartlar.map(acik) });
        olaylar.push({ t: 'verildi', neden: v.neden, alanlar: [...alan.keys()] });
        d.ver = null;
      }
    } else if (h.t === 'inan' || h.t === 'yalan') {
      if (!b || b.tur !== 'yalan') return { hata: 'Karar verilecek kapalı kart yok.' };
      if (oyuncu === b.oynayan) return { hata: 'Kendi kartın için karar veremezsin.' };
      if (h.t === 'inan' && oyuncu !== b.karar) return { hata: 'Karta inanıp oyunu sürdürmek sıradaki oyuncunun kararı; sen yalnız “Yalan!” diyebilirsin.' };
      const kart = ust(d);
      const p: Oyun = { o: b.oynayan, deger: b.beyan.deger, renkli: b.beyan.deger === '+4' ? null : b.beyan.renk, renk: b.beyan.renk, hedef: b.hedef, flex: false, haksiz: false };
      d.bekle = null;
      d.kim = d.oyuncular.indexOf(b.oynayan);
      if (h.t === 'inan') {
        // Kart kapalı kalır, söylenen kart sayılır
        olaylar.push({ t: 'inandi', o: oyuncu, hedef: b.oynayan });
        d.aktifRenk = b.beyan.renk;
        etki(d, p, rng, olaylar);
      } else {
        const dogru = !b.duz && kart.deger === b.beyan.deger && (kart.renk === null || kart.renk === b.beyan.renk);
        if (dogru) {
          // Doğru söylemiş: kart açılır ve geçerli olur, “Yalan!” diyen 1 kart çeker (7/0'da el değişiminden sonra)
          delete kart.by;
          olaylar.push({ t: 'yalan', o: oyuncu, hedef: b.oynayan, hakli: false, kart: acik(kart) });
          d.aktifRenk = b.beyan.renk;
          const sonra = (b.beyan.deger === '7' || b.beyan.deger === '0') && d.eller[b.oynayan].length > 0;
          if (!sonra) cek(d, oyuncu, 1, 'yalan', rng, olaylar);
          etki(d, p, rng, olaylar);
          if (sonra && !d.sonuc) cek(d, oyuncu, 1, 'yalan', rng, olaylar);
        } else {
          // Yalan (ya da düz kartı kapalı oynamış): kartı geri alır, ceza çeker, sırası geçer
          d.atik.pop();
          delete kart.by;
          d.eller[b.oynayan].push(kart);
          olaylar.push({ t: 'yalan', o: oyuncu, hedef: b.oynayan, hakli: true, kart: acik(kart), duz: b.duz });
          cek(d, b.oynayan, b.duz ? 6 : 1, 'yalan', rng, olaylar);
          gec(d, 1, olaylar);
        }
      }
    } else if (h.t === 'koy') {
      if (!b || b.tur !== 'meydan' || b.asama !== 'koy' || !b.katilan.includes(oyuncu) || b.konan[oyuncu]) return { hata: 'Şu an kapalı kart koyman gerekmiyor.' };
      const i = typeof h.kart === 'number' ? el.findIndex((k) => k.id === h.kart) : -1;
      if (i < 0) return { hata: 'Bu kart elinde yok.' };
      b.konan[oyuncu] = el.splice(i, 1)[0];
      olaylar.push({ t: 'koydu', o: oyuncu });
      if (b.katilan.every((id) => b.konan[id])) { b.asama = 'sorgu'; olaylar.push({ t: 'sira', o: b.oynayan }); }
    } else if (h.t === 'sorgula' || h.t === 'yeter') {
      if (!b || b.tur !== 'meydan' || b.asama !== 'sorgu' || b.oynayan !== oyuncu) return { hata: 'Şu an sorgulayamazsın.' };
      if (h.t === 'yeter') meydanBitir(d, b, olaylar);
      else {
        const hedef = h.hedef;
        if (typeof hedef !== 'string' || !b.konan[hedef] || b.sorgulanan.includes(hedef)) return { hata: 'Bu oyuncu sorgulanamaz.' };
        const kart = b.konan[hedef];
        const dogru = kart.renk === b.renk;
        b.sorgulanan.push(hedef);
        olaylar.push({ t: 'sorgu', o: oyuncu, hedef, dogru, kart: acik(kart) });
        if (dogru) meydanBitir(d, b, olaylar);
        else {
          // Yalancı: kartını geri alır, 1 kart çeker
          delete b.konan[hedef];
          d.eller[hedef].push(kart);
          cek(d, hedef, 1, 'yalan', rng, olaylar);
          if (!Object.keys(b.konan).some((id) => !b.sorgulanan.includes(id))) meydanBitir(d, b, olaylar);
        }
      }
    } else if (h.t === 'cek') {
      if (!siraBende) return { hata: 'Sıra sende değil.' };
      if (d.cektiBuTur) return { hata: 'Bu turda zaten çektin.' };
      if (d.takimOyun && el.some((k) => duzUyar(d, k))) return { hata: 'Ortağın Takım Oyunu jokeri oynadı: uyan bir kartını oynamalısın.' };
      d.yakalanabilir = [];
      if (d.takimOyun) {
        // Araya kart verme girdi ve uyan kart kalmadı: jokeri oynayan 2 çeker, sıra geçer
        cek(d, d.takimOyun, 2, 'takim', rng, olaylar);
        d.takimOyun = null;
        gec(d, 1, olaylar);
      } else if (d.yigin) {
        // Biriken cezayı üstlenenin sırası geçer
        const adet = d.yigin;
        d.yigin = 0; d.yiginEn = 0;
        if (m === 'extreme') {
          firlat(d, oyuncu, adet, 'vur', rng, olaylar);
          // Tek vuruşta sıra vurulandan sonrakine; üst üste vuruşta ilk vurandan sonrakine geçer (o da vurulansa bir sonrakine)
          const ilk = d.yiginIlk ? d.oyuncular.indexOf(d.yiginIlk) : -1;
          let sira = (d.yiginAdet || 1) > 1 && ilk >= 0 ? ileri(d, ilk) : ileri(d, d.kim);
          if (sira === d.kim) sira = ileri(d, d.kim);
          d.yiginIlk = null; d.yiginAdet = 0;
          d.kim = sira; d.cektiBuTur = false; d.cekilen = null;
          olaylar.push({ t: 'sira', o: d.oyuncular[sira] });
        } else {
          cek(d, oyuncu, adet, 'yigin', rng, olaylar);
          gec(d, 1, olaylar);
        }
      } else if (m === 'extreme') {
        // Fırlatıcıya bir kez basılır; fırlayan kart bu tur oynanamaz
        firlat(d, oyuncu, 1, 'cek', rng, olaylar);
        gec(d, 1, olaylar);
      } else if (m === 'noMercy') {
        if (el.some((k) => uyar(d, oyuncu, k))) return { hata: 'Oynanabilir kartın var: No Mercy’de yalnız oynayacak kartın yokken çekersin.' };
        // Uyan kart gelene dek çekilir; gelen kart oynanmak zorundadır
        const kartlar = geleneCek(d, oyuncu, (k) => uyar(d, oyuncu, k), 'cek', rng, olaylar);
        const son = kartlar[kartlar.length - 1];
        if (son && uyar(d, oyuncu, son) && !dolu(d, oyuncu)) { d.cektiBuTur = true; d.cekilen = son.id; }
        else gec(d, 1, olaylar);
      } else {
        let kart = cek(d, oyuncu, 1, 'cek', rng, olaylar)[0];
        // Çek-çek: uyan kart gelene dek
        for (let i = 0; m === 'cekCek' && kart && !uyar(d, oyuncu, kart) && i < 40; i++) kart = cek(d, oyuncu, 1, 'cek', rng, olaylar)[0];
        d.cektiBuTur = true;
        d.cekilen = kart ? kart.id : null;
      }
    } else if (h.t === 'pas') {
      if (!siraBende) return { hata: 'Sıra sende değil.' };
      if (!d.cektiBuTur) return { hata: 'Önce kart çekmelisin.' };
      if (m === 'noMercy' && d.cekilen !== null && el.some((k) => k.id === d.cekilen && uyar(d, oyuncu, k))) return { hata: 'No Mercy: çektiğin uyan kartı oynamak zorundasın.' };
      olaylar.push({ t: 'pas', o: oyuncu });
      gec(d, 1, olaylar);
    } else if (h.t === 'oyna') {
      const i = typeof h.kart === 'number' ? el.findIndex((k) => k.id === h.kart) : -1;
      if (!siraBende && !(i >= 0 && tipki(d, el[i]))) return { hata: m === 'atlama' ? 'Sıra sende değil; sıra dışında yalnız ortadaki kartın tıpkısını atabilirsin.' : 'Sıra sende değil.' };
      if (i < 0) return { hata: 'Bu kart elinde yok.' };
      const kart = el[i];
      if (!siraBende) {
        // Atlama: sıra atlayan oyuncuya geçer, oynanan kartın etkisi ondan sayılır
        d.kim = d.oyuncular.indexOf(oyuncu);
        d.cektiBuTur = false; d.cekilen = null;
        olaylar.push({ t: 'atladi', o: oyuncu });
      }
      if (d.cektiBuTur && kart.id !== d.cekilen) return { hata: 'Çektikten sonra yalnız çektiğin kartı oynayabilirsin.' };
      const flex = h.flex === true;
      const kapali = m === 'yalanci' && (h.kapali === true || !!kart.yl);

      if (kapali) {
        // Yalancı: kart kapalı konur, ne olduğu söylenir; söylenen kart ortadakine uymalıdır
        const by = h.beyan as Partial<UnoBeyan> | undefined;
        if (!by || !renkMi(by.renk) || !BEYAN_DEGER.includes(by.deger as UnoDeger)) return { hata: 'Kapalı oynarken kartın ne olduğunu söylemelisin (renk ve değer).' };
        const beyan: UnoBeyan = { renk: by.renk, deger: by.deger as UnoDeger };
        if (!(beyan.deger === '+4' || beyan.renk === d.aktifRenk || beyan.deger === ustDeger(d))) return { hata: 'Söylediğin kart ortadakine uymalı: aynı renk, aynı değer ya da +4.' };
        d.yakalanabilir = [];
        el.splice(i, 1);
        kart.by = beyan;
        d.atik.push(kart);
        olaylar.push({ t: 'oynadi', o: oyuncu, kart: ustGorunum(kart), kapali: true });
        if (el.length === 1) {
          if (h.uno === true) { d.unoDedi.push(oyuncu); olaylar.push({ t: 'uno', o: oyuncu }); }
          else d.yakalanabilir.push(oyuncu);
        }
        const hedef = beyan.deger === '7' && hedefGecerli(h.hedef) ? h.hedef : undefined;
        d.bekle = { tur: 'yalan', oynayan: oyuncu, kart: kart.id, beyan, karar: d.oyuncular[ileri(d, d.kim)], hedef, duz: !kart.yl };
        d.cektiBuTur = false; d.cekilen = null;
        olaylar.push({ t: 'sira', o: d.bekle.karar });
      } else {
        if (flex && !flexUyar(d, oyuncu, kart)) return { hata: !kart.fx ? 'Bu kartın flex yüzü yok.' : !d.guc?.[oyuncu] ? 'Güç kartın kırmızı: flex yüzünü kullanamazsın.' : 'Bu kartın flex rengi de uymuyor.' };
        if (!flex && d.yigin && !yiginUyar(d, kart)) {
          return { hata: m === 'extreme' ? `Sana ${d.yigin} vuruş geldi: yalnız bir Vur kartı eklenir; ekleyemiyorsan fırlatıcıya bas.`
            : m === 'noMercy' ? `Biriken ${d.yigin} kartın üstüne yalnız +${d.yiginEn} ya da daha büyük bir çekme kartı eklenir; ekleyemiyorsan çek.`
              : `Biriken ${d.yigin} kartın üstüne yalnız ${ustDeger(d) === '+2' ? '+2 ya da +4' : '+4'}${m === 'dostlar' ? ' ya da Yarasa siperi' : ''} eklenir; ekleyemiyorsan çek.` };
        }
        if (d.yigin && flex) return { hata: 'Biriken cezanın üstüne flex yüzüyle oynanmaz.' };
        if (!flex && !d.yigin && !(m === 'hepsiJoker' || duzUyar(d, kart))) {
          return { hata: flexUyar(d, oyuncu, kart) ? 'Bu kart yalnız flex yüzüyle uyuyor.' : 'Bu kart şu an oynanamaz.' };
        }
        const renkGerek = kart.renk === null && m !== 'hepsiJoker' && kart.deger !== 'rulet';
        const renk = kart.renk ?? (renkGerek ? h.renk : d.aktifRenk);
        if (!renkMi(renk)) return { hata: 'Joker için renk seçmelisin.' };
        const hGerek = hedefGerek(m, kart.deger, flex);
        if (hGerek && kart.deger !== '7' && !hedefGecerli(h.hedef)) return { hata: 'Bu kart için bir rakip seçmelisin.' };
        const hedef = hGerek && hedefGecerli(h.hedef) ? h.hedef : undefined;

        d.yakalanabilir = [];
        // Joker çekme kartı yalnız elde geçerli renkten kart yokken kurala uygundur (itirazda bakılır; Flex'te öbür jokerler de sayılır)
        const haksiz = el.some((k) => k.id !== kart.id && (k.renk === d.aktifRenk || (m === 'flex' && k.renk === null)));
        el.splice(i, 1);
        d.atik.push(kart);
        if (m !== 'hepsiJoker') d.aktifRenk = renk;
        olaylar.push({ t: 'oynadi', o: oyuncu, kart: acik(kart), ...(kart.renk === null && renkGerek ? { renk } : {}), ...(flex ? { flex: true } : {}), ...(hedef ? { hedef } : {}) });
        if (kart.renk === null && renkGerek) olaylar.push({ t: 'renk', renk });
        if (el.length === 1) {
          if (h.uno === true) { d.unoDedi.push(oyuncu); olaylar.push({ t: 'uno', o: oyuncu }); }
          else d.yakalanabilir.push(oyuncu);
        }
        d.cektiBuTur = false; d.cekilen = null;
        etki(d, { o: oyuncu, deger: kart.deger, renkli: kart.renk, renk, hedef, flex, haksiz, ps: !!kart.ps, cv: !!kart.cv }, rng, olaylar);
      }
    } else return { hata: 'Geçersiz hamle.' };

    sonIslem(d, onceEl, olaylar, h.t === 'oyna' && h.uno === true ? oyuncu : null);
    return { durum: d, olaylar };
  } catch {
    return { hata: 'Hamle işlenemedi.' };
  }
}

/* ------------------------------------------------------------------ görünüm ------------------------------------------------------------------ */

function bekleGorunum(b: Bekle): UnoBekle {
  if (b.tur === 'renk') return { tur: 'renk', kim: b.kim };
  if (b.tur === 'itiraz') return { tur: 'itiraz', oynayan: b.oynayan, hedef: b.hedef, kart: b.kart };
  if (b.tur === 'rulet') return { tur: 'rulet', kim: b.kim };
  if (b.tur === 'yalan') return { tur: 'yalan', oynayan: b.oynayan, beyan: b.beyan, karar: b.karar };
  return { tur: 'meydan', oynayan: b.oynayan, renk: b.renk, asama: b.asama, koymayan: b.katilan.filter((id) => !b.konan[id] && !b.sorgulanan.includes(id)), konan: Object.keys(b.konan).filter((id) => !b.sorgulanan.includes(id)) };
}

function gorunum(durum: unknown, bakan: string | null): UnoGorunum {
  const d = durum as UnoDurum;
  const m = mod(d);
  const b = d.bekle ?? null;
  const sira = !b ? d.oyuncular[d.kim] : b.tur === 'renk' || b.tur === 'rulet' ? b.kim : b.tur === 'itiraz' ? b.hedef : b.tur === 'yalan' ? b.karar : b.oynayan;
  const oyuncu = bakan !== null && d.oyuncular.includes(bakan);
  const elim = oyuncu ? d.eller[bakan!] : [];
  const serbest = !d.sonuc && !b && !d.ver;
  const siraBende = serbest && bakan === d.oyuncular[d.kim];
  const oynanir = (k: K) => (!d.cektiBuTur || k.id === d.cekilen) && uyar(d, bakan!, k);
  const g: UnoGorunum = {
    tur: 'uno', elNo: d.elNo, sira, yon: d.yon,
    oyuncular: d.oyuncular.map((id) => ({
      id, kartSayisi: d.eller[id].length, unoDedi: d.unoDedi.includes(id),
      ...(d.elenen?.includes(id) ? { elendi: true } : {}),
      ...(m === 'takim' ? { takim: d.oyuncular.indexOf(id) % (d.oyuncular.length / 2), ...(d.eller[id].length === 0 ? { cikti: true } : {}) } : {}),
      ...(d.guc ? { guc: !!d.guc[id] } : {}),
      ...(m === 'flip' && id !== bakan ? { arka: d.eller[id].map((k) => k.arka!).filter(Boolean) } : {}),
    })),
    elim: elim.map(acik),
    ust: ustGorunum(ust(d)), aktifRenk: d.aktifRenk, deste: d.deste.length, atikSayisi: d.atik.length,
    cektiBuTur: d.cektiBuTur,
    oynanabilir: siraBende ? elim.filter(oynanir).map((k) => k.id)
      : serbest && oyuncu ? elim.filter((k) => tipki(d, k)).map((k) => k.id) : [],
    yakalanabilir: d.sonuc ? [] : [...d.yakalanabilir],
    bitti: !!d.sonuc,
    mod: m,
    yigin: d.yigin || 0,
    hedefPuan: unoModTanim(m).hedef,
  };
  if (b) {
    g.bekle = bekleGorunum(b);
    if (b.tur === 'itiraz') g.dortBekle = { oynayan: b.oynayan, hedef: b.hedef };
    if (b.tur === 'renk' && b.sonra === 'oyna') g.renkSec = true;
  }
  if (d.ver) {
    if (!b) g.bekle = { tur: 'ver', neden: d.ver.neden, kalan: d.ver.kalan.map((x) => ({ ...x })) };
    const benim = oyuncu ? d.ver.kalan.find((x) => x.kim === bakan) : undefined;
    if (benim) g.ver = { kime: benim.kime, adet: benim.adet, neden: d.ver.neden };
  }
  if (siraBende && d.cekilen !== null) g.cekilen = d.cekilen;
  if (m === 'flip') { g.taraf = d.taraf ?? 'a'; const du = d.deste[d.deste.length - 1]?.arka; if (du) g.desteUst = du; }
  if (m === 'hepsiJoker') g.renksiz = true;
  if (m === 'extreme') g.firlatici = true;
  if (m === 'flex' && siraBende && !d.yigin) {
    const fx = elim.filter((k) => (!d.cektiBuTur || k.id === d.cekilen) && flexUyar(d, bakan!, k));
    g.flex = fx.map((k) => k.id);
    g.yalnizFlex = fx.filter((k) => !duzUyar(d, k)).map((k) => k.id);
  }
  if (siraBende) {
    g.cekOlur = !d.cektiBuTur && !(d.takimOyun && elim.some((k) => duzUyar(d, k))) && !(m === 'noMercy' && !d.yigin && elim.some((k) => uyar(d, bakan!, k)));
    if (m === 'noMercy' && d.cektiBuTur && d.cekilen !== null && g.oynanabilir.includes(d.cekilen)) g.zorunlu = true;
    if (d.takimOyun) g.takimOyun = true;
  }
  return g;
}

/* ------------------------------------------------------------------ bot ------------------------------------------------------------------ */

function botHamle(durum: unknown, bot: string, _rng: Rng): unknown | null {
  const d = durum as UnoDurum;
  if (d.sonuc || !d.oyuncular.includes(bot) || d.elenen?.includes(bot)) return null;
  const m = mod(d);
  const el = d.eller[bot];
  const tur = d.atik.length + d.deste.length * 7 + el.length * 131;
  const zar = (ek: string) => karma(`${bot}|${tur}|${ek}`);
  if (d.yakalanabilir.includes(bot)) return { t: 'uno' }; // insandan devralınan el
  if (m === 'takim' && d.yakalanabilir.includes(ortak(d, bot)) && zar('ortakUno') < 0.7) return { t: 'uno' };
  // Yakalama kararı belirlenimci: aynı durumda yeniden sorulunca değişmez (≈ %50)
  const yakala = d.yakalanabilir.find((h) => h !== bot && !(m === 'takim' && ortak(d, bot) === h) && karma(`${bot}|${h}|${d.atik.length}`) < 0.5);
  if (yakala) return { t: 'yakala', hedef: yakala };

  if (d.ver) {
    const g = d.ver.kalan.find((x) => x.kim === bot);
    if (!g || !el.length) return null;
    // Rakibe hediye: en pahalı kart; ortağa: en değersiz sayı (jokerler kendisinde kalır)
    const sirali = [...el].sort((a, b) => kartPuani(b, m) - kartPuani(a, m) || a.id - b.id);
    return { t: 'ver', kart: (d.ver.neden === 'hediye' ? sirali[0] : sirali[sirali.length - 1]).id };
  }

  const sayim: Record<UnoRenk, number> = { k: 0, s: 0, y: 0, m: 0 };
  for (const k of el) if (k.renk) sayim[k.renk]++;
  const enCok = UNO_RENKLER.reduce((en, r) => (sayim[r] > sayim[en] ? r : en), d.aktifRenk);

  const b = d.bekle;
  if (b) {
    if ((b.tur === 'renk' || b.tur === 'rulet') && b.kim === bot) return { t: 'renk', renk: enCok };
    if (b.tur === 'itiraz' && b.hedef === bot) {
      // Oynayanın elinde çok kart varsa (renk tutma olasılığı yüksek) itiraz eder
      const n = d.eller[b.oynayan].length;
      return { t: zar('itiraz') < Math.min(0.6, n / 12) ? 'itiraz' : 'kabul' };
    }
    if (b.tur === 'yalan' && b.oynayan !== bot) {
      // Söylenen yalancı kartının tek kopyası kendi elindeyse yalan kesindir
      const kesin = el.some((k) => k.yl && k.deger === b.beyan.deger && (k.renk === null ? el.filter((x) => x.yl && x.deger === '+4').length >= 2 : k.renk === b.beyan.renk));
      const kalan = d.eller[b.oynayan].length;
      const olasilik = kesin ? 1 : (b.karar === bot ? 0.16 : 0.05) + (kalan <= 1 ? 0.3 : 0) + (b.beyan.deger === '+4' || b.beyan.deger === '+2' ? 0.1 : 0);
      if (zar('yalan') < olasilik) return { t: 'yalan' };
      return b.karar === bot ? { t: 'inan' } : null;
    }
    if (b.tur === 'meydan') {
      if (b.asama === 'koy' && b.katilan.includes(bot) && !b.konan[bot]) {
        const dogru = el.filter((k) => k.renk === b.renk).sort((x, y) => kartPuani(y, m) - kartPuani(x, m));
        const kart = dogru[0] ?? [...el].sort((x, y) => kartPuani(y, m) - kartPuani(x, m) || x.id - y.id)[0];
        return kart ? { t: 'koy', kart: kart.id } : null;
      }
      if (b.asama === 'sorgu' && b.oynayan === bot) {
        const aday = Object.keys(b.konan).filter((id) => !b.sorgulanan.includes(id)).sort((x, y) => d.eller[x].length - d.eller[y].length);
        return aday.length && karma(`${bot}|${d.atik.length}|${b.sorgulanan.length}|sorgu`) < 0.55 ? { t: 'sorgula', hedef: aday[0] } : { t: 'yeter' };
      }
    }
    return null;
  }

  // Atlama: sıra dışındaki bot tıpkı kartını (belirlenimci ≈ %60) hemen atar
  if (d.oyuncular[d.kim] !== bot) {
    const t = el.find((k) => tipki(d, k));
    if (t && karma(`${bot}|${d.atik.length}|atla`) < 0.6) return { t: 'oyna', kart: t.id, ...(el.length === 2 ? { uno: true } : {}) };
    return null;
  }
  return siraOnerisi(gorunum(d, bot), bot, zar('blof'))?.hamle ?? null;
}

export const unoMotor: Motor = {
  tur: 'uno',
  min: 2,
  max: 8,
  elBaslat,
  uygula,
  gorunum,
  botHamle,
  sonuc: (durum) => (durum as UnoDurum).sonuc,
};
