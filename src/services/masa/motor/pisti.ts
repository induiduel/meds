/**
 * Pişti — saf kural motoru (52 kartlık Fransız destesi, 2 ya da 4 oyuncu; 4'te karşılıklı ortaklar, puan takım toplamı).
 * Başta yere 4 kart (3 kapalı + üstte açık; üst Vale ise yer kartları desteye karılıp yeniden açılır), herkese 4 kart; eller
 * bitince desteden yeniden 4'er, deste bitince el biter. Aynı değer ya da Vale yeri alır; yerde tek kart varken aynı değerle
 * almak pişti (10), tek Vale'ye Vale pişti 20. El sonunda yerde kalan son alana gider.
 * Puan: As 1, Vale 1, ♣2 = 2, ♦10 = 3, en çok kart +3 (eşitlikte kimse), pişti 10/20.
 * Durum düz JSON; `uygula` girdiyi değiştirmez. Gizlilik: el yalnız `gorunum(bakan)` ve `kime`li olaylarla sahibine gider;
 * deste ve yerdeki kapalı kartlar hiçbir görünümde yoktur.
 */
import type { ElSatir, ElSonuc, Motor, OdaAyar, Olay, Rng, Takim } from '../tipler';

/** maca ♠, kupa ♥, karo ♦, sinek ♣ */
export type PistiRenk = 'maca' | 'kupa' | 'karo' | 'sinek';
/** d: 1 = As, 2–10, 11 = Vale, 12 = Kız, 13 = Papaz */
export interface PistiKart { id: number; renk: PistiRenk; d: number }
export type PistiHamle = { t: 'oyna'; kart: number };

export interface PistiOyuncuGorunum {
  id: string;
  takim: Takim;
  kartSayisi: number;
  /** Aldığı kart sayısı */
  aldigi: number;
  pisti: number;
  /** Pişti puanı (Vale piştisi 20) */
  pistiPuan: number;
}

export interface PistiGorunum {
  tur: 'pisti';
  elNo: number;
  sira: string;
  oyuncular: PistiOyuncuGorunum[];
  /** Bakanın eli (izleyicide boş) */
  elim: PistiKart[];
  /** Yerdeki kart sayısı (kapalılar dahil) ve en üstteki açık kart */
  yerSayisi: number;
  ust: PistiKart | null;
  /** Yerin altında hâlâ duran kapalı kart sayısı (başta 3) */
  kapali: number;
  deste: number;
  /** Son yeri alan (el sonunda kalan kartlar ona gider) */
  sonAlan: string | null;
  /** 4 oyunculu eşli oyun */
  esli: boolean;
  bitti: boolean;
}

export interface PistiDurum {
  tur: 'pisti';
  elNo: number;
  oyuncular: string[];
  takimlar: Record<string, Takim>;
  kim: number;
  eller: Record<string, PistiKart[]>;
  /** Son eleman en üstte */
  deste: PistiKart[];
  /** Son eleman en üstte; ilk `kapali` kart kapalıdır */
  yer: PistiKart[];
  kapali: number;
  alinan: Record<string, PistiKart[]>;
  pisti: Record<string, number>;
  pistiPuan: Record<string, number>;
  sonAlan: string | null;
  sonuc: ElSonuc | null;
}

export const PISTI_RENKLER: readonly PistiRenk[] = ['maca', 'kupa', 'karo', 'sinek'];
export const PISTI_RENK_SIMGE: Record<PistiRenk, string> = { maca: '♠', kupa: '♥', karo: '♦', sinek: '♣' };
export const PISTI_RENK_AD: Record<PistiRenk, string> = { maca: 'Maça', kupa: 'Kupa', karo: 'Karo', sinek: 'Sinek' };
export const VALE = 11;
const EL = 4;

export const degerYazi = (d: number): string => (d === 1 ? 'A' : d === 11 ? 'J' : d === 12 ? 'Q' : d === 13 ? 'K' : String(d));
export const degerAd = (d: number): string => (d === 1 ? 'As' : d === 11 ? 'Vale' : d === 12 ? 'Kız' : d === 13 ? 'Papaz' : String(d));
export const kartAd = (k: PistiKart): string => `${PISTI_RENK_AD[k.renk]} ${degerAd(k.d)}`;

/** 52 kart, kimlik 0–51 (karılmamış): renk = id / 13, değer = id % 13 + 1 */
export function pistiDeste(): PistiKart[] {
  return Array.from({ length: 52 }, (_, id) => ({ id, renk: PISTI_RENKLER[Math.floor(id / 13)], d: (id % 13) + 1 }));
}

/** Kartın el sonu puanı (pişti ve çoğunluk hariç) */
export function kartPuani(k: PistiKart): number {
  if (k.renk === 'sinek' && k.d === 2) return 2;
  if (k.renk === 'karo' && k.d === 10) return 3;
  return k.d === 1 || k.d === VALE ? 1 : 0;
}

/** Atılan kart yeri alır mı (yer boşken hiçbir kart almaz) */
export const aliyorMu = (kart: PistiKart, ust: PistiKart | null): boolean => !!ust && (kart.d === ust.d || kart.d === VALE);

const rs = (rng: Rng, n: number): number => { const x = Math.floor(rng() * n); return x >= 0 && x < n ? x : 0; };
function kar<T>(a: T[], rng: Rng): T[] {
  for (let i = a.length - 1; i > 0; i--) { const j = rs(rng, i + 1); [a[i], a[j]] = [a[j], a[i]]; }
  return a;
}
const kopya = (d: PistiDurum): PistiDurum => JSON.parse(JSON.stringify(d));

/** Takım dizisi: verilmişse o, yoksa i%2 (A,B,A,B → karşılıklı ortaklar) */
export function takimlarKur(oyuncular: { id: string; takim?: Takim }[]): Record<string, Takim> {
  const t: Record<string, Takim> = {};
  oyuncular.forEach((o, i) => { t[o.id] = o.takim === 'A' || o.takim === 'B' ? o.takim : i % 2 === 0 ? 'A' : 'B'; });
  return t;
}

/** Puan dökümü: oyuncu (2 kişi) ya da takım (4 kişi) başına */
interface Doküm { kart: number; as: number; vale: number; sinek2: boolean; karo10: boolean; pisti: number; pistiPuan: number; temel: number }
function dokum(d: PistiDurum, kimler: string[]): Doküm {
  const kartlar = kimler.flatMap((id) => d.alinan[id]);
  const r: Doküm = { kart: kartlar.length, as: 0, vale: 0, sinek2: false, karo10: false, pisti: 0, pistiPuan: 0, temel: 0 };
  for (const k of kartlar) {
    if (k.d === 1) r.as++;
    if (k.d === VALE) r.vale++;
    if (k.renk === 'sinek' && k.d === 2) r.sinek2 = true;
    if (k.renk === 'karo' && k.d === 10) r.karo10 = true;
    r.temel += kartPuani(k);
  }
  for (const id of kimler) { r.pisti += d.pisti[id]; r.pistiPuan += d.pistiPuan[id]; }
  return r;
}

function elSonucu(d: PistiDurum): ElSonuc {
  const esli = d.oyuncular.length === 4;
  // Puan birimleri: eşlide takım, değilse oyuncu
  const birimler: string[][] = esli
    ? (['A', 'B'] as Takim[]).map((t) => d.oyuncular.filter((id) => d.takimlar[id] === t))
    : d.oyuncular.map((id) => [id]);
  const dk = birimler.map((b) => dokum(d, b));
  const enCok = Math.max(...dk.map((x) => x.kart));
  const cogunluk = dk.filter((x) => x.kart === enCok).length === 1 ? dk.findIndex((x) => x.kart === enCok) : -1;
  const puan = dk.map((x, i) => x.temel + x.pistiPuan + (i === cogunluk ? 3 : 0));
  const enIyi = Math.max(...puan);
  const aciklama = (x: Doküm, i: number): string => {
    const p: string[] = [`${x.kart} kart`];
    if (x.pisti) p.push(`${x.pisti} pişti (${x.pistiPuan})`);
    if (x.as) p.push(`${x.as} as`);
    if (x.vale) p.push(`${x.vale} vale`);
    if (x.sinek2) p.push('♣2 (+2)');
    if (x.karo10) p.push('♦10 (+3)');
    if (i === cogunluk) p.push('en çok kart +3');
    return p.join(' · ');
  };
  const satirlar: ElSatir[] = d.oyuncular.map((id) => {
    const bi = birimler.findIndex((b) => b.includes(id));
    const kazandi = puan[bi] === enIyi;
    const ek = esli ? ` (takım ${d.takimlar[id]})` : '';
    return { id, puan: puan[bi], kalan: d.eller[id].length, kazandi, cezalar: [], aciklama: aciklama(dk[bi], bi) + ek };
  });
  const kazananlar = satirlar.filter((s) => s.kazandi).map((s) => s.id);
  const s: ElSonuc = { neden: 'deste', kazananlar, satirlar };
  if (esli) {
    const kt = (['A', 'B'] as Takim[]).filter((_, i) => puan[i] === enIyi);
    if (kt.length === 1) s.kazananTakim = kt[0];
  }
  return s;
}

function dagit(d: PistiDurum, olaylar: Olay[]): void {
  for (const id of d.oyuncular) {
    d.eller[id] = d.deste.splice(d.deste.length - EL, EL);
    olaylar.push({ t: 'cektim', kime: id, kartlar: d.eller[id] });
  }
  olaylar.push({ t: 'dagit', deste: d.deste.length });
}

function elBaslat(g: { oyuncular: { id: string; takim?: Takim }[]; elNo: number; baslayan: number; rng: Rng; ayar?: Partial<OdaAyar> }): PistiDurum {
  const oyuncular = g.oyuncular.map((o) => o.id);
  const n = oyuncular.length;
  if ((n !== 2 && n !== 4) || new Set(oyuncular).size !== n) throw new Error('Pişti 2 ya da 4 farklı oyuncuyla oynanır.');
  let deste = kar(pistiDeste(), g.rng);
  let yer = deste.splice(deste.length - 4, 4);
  // Üst açık kart Vale ise yer kartları desteye karılıp yeniden açılır
  for (let i = 0; yer[3].d === VALE && i < 100; i++) { deste = kar([...deste, ...yer], g.rng); yer = deste.splice(deste.length - 4, 4); }
  if (yer[3].d === VALE) { const j = deste.findIndex((k) => k.d !== VALE); [yer[3], deste[j]] = [deste[j], yer[3]]; } // bozuk rng güvencesi
  const d: PistiDurum = {
    tur: 'pisti', elNo: g.elNo, oyuncular, takimlar: takimlarKur(g.oyuncular),
    kim: Number.isInteger(g.baslayan) ? ((g.baslayan % n) + n) % n : 0,
    eller: {}, deste, yer, kapali: 3,
    alinan: Object.fromEntries(oyuncular.map((id) => [id, []])),
    pisti: Object.fromEntries(oyuncular.map((id) => [id, 0])),
    pistiPuan: Object.fromEntries(oyuncular.map((id) => [id, 0])),
    sonAlan: null, sonuc: null,
  };
  dagit(d, []);
  return d;
}

function uygula(durum: unknown, oyuncu: string, hamle: unknown, _rng: Rng): { durum: unknown; olaylar: Olay[] } | { hata: string } {
  const d0 = durum as PistiDurum;
  if (d0.sonuc) return { hata: 'El bitti.' };
  if (!d0.oyuncular.includes(oyuncu)) return { hata: 'Bu masada oyuncu değilsin.' };
  if (d0.oyuncular[d0.kim] !== oyuncu) return { hata: 'Sıra sende değil.' };
  const h = hamle as Partial<PistiHamle> | null;
  if (!h || h.t !== 'oyna' || typeof h.kart !== 'number') return { hata: 'Geçersiz hamle.' };
  const ki = d0.eller[oyuncu].findIndex((k) => k.id === h.kart);
  if (ki < 0) return { hata: 'Bu kart elinde yok.' };

  const d = kopya(d0);
  const olaylar: Olay[] = [];
  const [kart] = d.eller[oyuncu].splice(ki, 1);
  const ust = d.yer.length ? d.yer[d.yer.length - 1] : null;
  olaylar.push({ t: 'oynadi', o: oyuncu, kart });
  if (aliyorMu(kart, ust)) {
    const pisti = d.yer.length === 1 && kart.d === ust!.d;
    const adet = d.yer.length + 1;
    d.alinan[oyuncu].push(...d.yer, kart);
    d.yer = [];
    d.kapali = 0;
    d.sonAlan = oyuncu;
    if (pisti) {
      const p = kart.d === VALE ? 20 : 10;
      d.pisti[oyuncu]++;
      d.pistiPuan[oyuncu] += p;
      olaylar.push({ t: 'pisti', o: oyuncu, puan: p, vale: kart.d === VALE });
    }
    olaylar.push({ t: 'aldi', o: oyuncu, adet, pisti });
  } else {
    d.yer.push(kart);
  }

  d.kim = (d.kim + 1) % d.oyuncular.length;
  if (d.oyuncular.every((id) => d.eller[id].length === 0)) {
    if (d.deste.length >= EL * d.oyuncular.length) dagit(d, olaylar);
    else {
      // El sonu: yerde kalan son alana
      if (d.yer.length && d.sonAlan) {
        olaylar.push({ t: 'aldi', o: d.sonAlan, adet: d.yer.length, pisti: false, sonKalan: true });
        d.alinan[d.sonAlan].push(...d.yer);
        d.yer = [];
        d.kapali = 0;
      }
      d.sonuc = elSonucu(d);
      olaylar.push({ t: 'elBitti' });
      return { durum: d, olaylar };
    }
  }
  olaylar.push({ t: 'sira', o: d.oyuncular[d.kim] });
  return { durum: d, olaylar };
}

function gorunum(durum: unknown, bakan: string | null): PistiGorunum {
  const d = durum as PistiDurum;
  return {
    tur: 'pisti', elNo: d.elNo, sira: d.oyuncular[d.kim],
    oyuncular: d.oyuncular.map((id) => ({
      id, takim: d.takimlar[id], kartSayisi: d.eller[id].length, aldigi: d.alinan[id].length, pisti: d.pisti[id], pistiPuan: d.pistiPuan[id],
    })),
    elim: bakan && d.eller[bakan] ? d.eller[bakan].map((k) => ({ ...k })) : [],
    yerSayisi: d.yer.length,
    ust: d.yer.length > d.kapali ? { ...d.yer[d.yer.length - 1] } : null,
    kapali: d.kapali,
    deste: d.deste.length,
    sonAlan: d.sonAlan,
    esli: d.oyuncular.length === 4,
    bitti: !!d.sonuc,
  };
}

/* ------------------------------------------------------------------ bot + asistan ------------------------------------------------------------------ */

export interface PistiOneri { kart: number; neden: string }

/**
 * Belirlenimci öneri: (1) üst kartla aynı değer (pişti fırsatı önce), (2) yer doluysa ve değerliyse Vale ile al,
 * (3) en az değerli kartı at (Vale saklanır; yalnız Vale kaldıysa Vale). Yer boşken Vale atılmaz (başka kart varsa).
 */
export function pistiOneri(el: PistiKart[], ust: PistiKart | null, yerSayisi: number): PistiOneri | null {
  if (!el.length) return null;
  const eslesen = ust ? el.filter((k) => k.d === ust.d) : [];
  if (eslesen.length) {
    const k = eslesen.sort((a, b) => kartPuani(b) - kartPuani(a) || a.id - b.id)[0];
    return { kart: k.id, neden: yerSayisi === 1 ? `Yerde tek ${degerAd(ust!.d)} var: ${kartAd(k)} ile pişti yaparsın (${ust!.d === VALE ? 20 : 10} puan).` : `${kartAd(k)} üstteki ${degerAd(ust!.d)} ile eşleşir; yerdeki ${yerSayisi} kartı alırsın.` };
  }
  const valeler = el.filter((k) => k.d === VALE);
  const digerleri = el.filter((k) => k.d !== VALE);
  // Vale ile alma: yerde değerli kart ya da büyük yığın varsa (ya da elde Vale'den başka kart yoksa)
  if (ust && valeler.length && (yerSayisi >= 4 || !digerleri.length)) {
    return { kart: valeler[0].id, neden: `Yerde ${yerSayisi} kart birikti; Vale ile hepsini alırsın.` };
  }
  if (!digerleri.length) return { kart: valeler[0].id, neden: 'Elinde yalnız Vale kaldı.' };
  // En az değerli: puansız, rakibe pişti vermeyecek (yer boşken tek kart pişti riski taşır), küçük değer
  const risk = (k: PistiKart) => kartPuani(k) * 10 + (k.d >= 12 ? 1 : 0);
  const k = [...digerleri].sort((a, b) => risk(a) - risk(b) || a.d - b.d || a.id - b.id)[0];
  return { kart: k.id, neden: valeler.length ? `Eşleşen kartın yok; Vale'yi büyük yığın için sakla, ${kartAd(k)} gibi değersiz bir kart at.` : `Eşleşen kartın yok; en değersiz kartın ${kartAd(k)}.` };
}

function botHamle(durum: unknown, bot: string, _rng: Rng): PistiHamle | null {
  const d = durum as PistiDurum;
  if (d.sonuc || d.oyuncular[d.kim] !== bot) return null;
  const ust = d.yer.length ? d.yer[d.yer.length - 1] : null;
  const o = pistiOneri(d.eller[bot], ust, d.yer.length);
  return o ? { t: 'oyna', kart: o.kart } : null;
}

export const pistiMotor: Motor = {
  tur: 'pisti' as any,
  min: 2,
  max: 4,
  elBaslat,
  uygula,
  gorunum: gorunum as unknown as Motor['gorunum'],
  botHamle,
  sonuc: (durum) => (durum as PistiDurum).sonuc,
};
