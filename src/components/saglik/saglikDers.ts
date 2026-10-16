import { createContext, useContext } from 'react';

/**
 * "Ders slaytında geçiyor" işaretleri — Sağlık Bakanlığı sekmesinde sayfadaki bilgi ders slaytında ya da çıkmış soruda
 * da geçiyorsa işaretlenir:
 *  - ayni:   aynı sayı + aynı yıl + ortak ad sözcükleri (ör. Türkiye TDH 2025 = 1,42)
 *  - farkli: aynı gösterge ve yıl için slaytta BAŞKA bir değer yazıyor (ör. sayfada revize 1,63, slaytta 1,69)
 *  - terim:  slaytta (ve çoğunlukla çıkmış soruda) geçen kavram/kurum/kısaltma (ör. KETEM, Umumi Hıfzıssıhha Kanunu)
 * Dizin: src/data/saglik/ders_eslesme.json (scripts/saglik/ders_eslesme.py) — tembel yüklenir.
 */

export interface DersCumle {
  d: string; s: number; b: string; t: string; y: string[];
  /** Çıkmış soru ise: soru id, sınav yılı, kurul */
  q?: string; qy?: string; qk?: number;
}
export interface DersTerim { t: string; k: string[]; s: number[]; q: number[]; n: number; nq: number; a?: string }
export interface DersDizin {
  desteler: Record<string, string>;
  cumleler: DersCumle[];
  /** kanonik sayı → [cümle no, başlangıç, bitiş, sayının kendi yılı (yoksa 0)] */
  dizin: Record<string, number[][]>;
  terimler?: DersTerim[];
}
export type EslesmeTur = 'ayni' | 'farkli' | 'terim';
export interface DersEslesme {
  tur: EslesmeTur;
  cumle: DersCumle;
  deste: string;
  /** Sayfa metnindeki aralık */
  bas: number; son: number; ham: string;
  /** Slayt cümlesindeki vurgulanacak aralık */
  sa: number; sb: number;
  /** farkli: slayttaki değer ve yıl */
  slaytDeger?: string; yil?: number;
  terim?: DersTerim;
}

export const DersCtx = createContext<DersDizin | null>(null);
export const useDersDizin = () => useContext(DersCtx);

let yuk: Promise<DersDizin> | null = null;
/** Dosyada başlıklar ayrı listede (cümlede numara) ve boş yıl listesi yazılmaz; yüklerken geri açılır */
export const dersDiziniYukle = () => (yuk ||= import('../../data/saglik/ders_eslesme.json').then((m) => {
  const ham = (m.default || m) as unknown as DersDizin & { basliklar?: string[] };
  const bl = ham.basliklar || [];
  for (const c of ham.cumleler as (DersCumle & { b: string | number })[]) {
    if (typeof c.b === 'number') c.b = bl[c.b] || '';
    if (!c.y) c.y = [];
  }
  return ham as DersDizin;
}));

// Slayttaki ve sayfadaki sayılar aynı biçimde okunur (Python betiğindeki SAYI ile aynı)
const SAYI = /(%\s?)?(\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+(?:[.,]\d+)?)(\s?%|\s?‰)?/g;
const YIL = /\b(19[5-9]\d|20[0-4]\d)\b/g;
const ONCE_YIL = /(19[5-9]\d|20[0-4]\d)[\s'’:=a-zA-ZçğıöşüÇĞİÖŞÜ()]{0,16}$/;
const SONRA_YIL = /^[\s'’a-zA-ZçğıöşüÇĞİÖŞÜ%‰]{0,8}\(\s*(19[5-9]\d|20[0-4]\d)\b/;
/** Birim paydaları ("100.000 canlı doğumda") değer sayılmaz */
const PAYDA = new Set(['100', '1000', '10000', '100000']);

export function kanonik(ham: string): string | null {
  let s = ham.trim();
  if (/^\d{1,3}(?:\.\d{3})+(?:,\d+)?$/.test(s)) s = s.replace(/\./g, '').replace(',', '.');
  else s = s.replace(',', '.');
  const f = Number(s);
  if (!isFinite(f)) return null;
  return String(+f.toFixed(6));
}

const anlamli = (ham: string, kan: string, yuzde: boolean) => {
  if (yuzde || ham.includes(',') || kan.includes('.')) return true;
  const n = Number(kan);
  if (/^\d{4}$/.test(ham) && n >= 1950 && n <= 2049) return false;
  return n >= 10;
};

/** Sayıya bitişik yıl ("2013'te 2,10", "2025: 1,42", "1,42 (2025)"); yoksa 0 — Python kendi_yili ile aynı */
export function kendiYili(t: string, a: number, b: number): number {
  const on = t.slice(Math.max(0, a - 22), a);
  const m = ONCE_YIL.exec(on);
  if (m && !/\d/.test(on.slice(m.index + m[1].length))) return Number(m[1]);
  const s = SONRA_YIL.exec(t.slice(b, b + 24));
  return s ? Number(s[1]) : 0;
}

const katla = (s: string) => s.toLocaleLowerCase('tr-TR')
  .replace(/ı/g, 'i').replace(/ş/g, 's').replace(/ç/g, 'c').replace(/ğ/g, 'g').replace(/ö/g, 'o').replace(/ü/g, 'u').replace(/â/g, 'a').replace(/î/g, 'i');

// Her göstergede geçen genel sözcükler eşleşme sayılmaz
const GENEL = new Set([
  'orani', 'oran', 'hizi', 'sayis', 'sayi', 'yilin', 'yilda', 'yili', 'turki', 'topla', 'olara', 'icin', 'veya', 'gore', 'deger', 'binde',
  'yuzde', 'kisi', 'kisib', 'ortal', 'genel', 'yeni', 'daha', 'kadar', 'olan', 'olup', 'ise', 'iken', 'sonra', 'once', 'ilk', 'son',
  'bu', 'bir', 'her', 'gibi', 'ile', 'olarak', 'veri', 'veril', 'yaklas', 'yakla', 'tum', 'tumu', 'artis', 'azal', 'duzey', 'dusus',
  'karab', 'ilin', 'ilce', 'merke', 'sagli', 'bakan', 'kaynak', 'tablo',
]);
const kokler = (s: string): Set<string> => {
  const out = new Set<string>();
  for (const w of katla(s).split(/[^a-z]+/)) {
    if (w.length < 4) continue;
    const k = w.slice(0, 5);
    if (!GENEL.has(k) && !GENEL.has(w)) out.add(k);
  }
  return out;
};
/** Göstergenin tam adı (genel sözcükler dahil — "Toplam" / "Genel" doğurganlık ayrılsın); yalnız bağlaçlar atılır */
const tamKokler = (s: string): string[] => [...new Set(katla(s.split(' · ')[0]).split(/[^a-z]+/)
  .filter((w) => w.length >= 3 && !['icin', 'veya', 'ile', 'olan', 'yas', 'karabuk', 'turkiye'].includes(w)).map((w) => w.slice(0, 5)))];
/** Ad kısaltması: "Toplam doğurganlık hızı" → "TDH" */
const kisaltmasi = (ad: string) => ad.split(/\s+/).filter((w) => /^\p{L}/u.test(w) && w.length > 2).map((w) => w[0].toLocaleUpperCase('tr-TR')).join('');

/** Cümle başına kök kümeleri bir kez hesaplanır (aynı cümle sayfadaki onlarca değerle karşılaştırılır) */
interface CumleKok { t: Set<string>; tb: Set<string>; tam: Set<string> }
const kokOnbellek = new WeakMap<DersCumle, CumleKok>();
function cumleKok(c: DersCumle): CumleKok {
  let k = kokOnbellek.get(c);
  if (!k) {
    const t = kokler(c.t);
    k = { t, tb: new Set([...t, ...kokler(c.b)]), tam: new Set(katla(`${c.b} ${c.t}`).split(/[^a-z]+/).map((w) => w.slice(0, 5))) };
    kokOnbellek.set(c, k);
  }
  return k;
}

/** Kök ağırlığı (IDF): slayt cümlelerinin çoğunda geçen kök ("hafta", "doğum") az, nadir kök ("sosyalleştirme") çok sayılır */
const idfOnbellek = new WeakMap<DersDizin, Map<string, number>>();
function idfTablosu(dz: DersDizin): Map<string, number> {
  let t = idfOnbellek.get(dz);
  if (t) return t;
  const df = new Map<string, number>();
  for (const c of dz.cumleler) for (const k of kokler(`${c.b} ${c.t}`)) df.set(k, (df.get(k) || 0) + 1);
  const N = dz.cumleler.length || 1;
  t = new Map([...df].map(([k, n]) => [k, Math.log(N / n)]));
  idfOnbellek.set(dz, t);
  return t;
}
/** Yıl → o yıla bitişik slayt sayıları (farklı değer araması) */
const yilOnbellek = new WeakMap<DersDizin, Map<number, [number, number, number, string][]>>();
function yilDizini(dz: DersDizin) {
  let t = yilOnbellek.get(dz);
  if (t) return t;
  t = new Map();
  for (const [kan, l] of Object.entries(dz.dizin)) {
    for (const [no, a, b, y] of l) if (y) (t.get(y) || t.set(y, []).get(y)!).push([no, a, b, kan]);
  }
  yilOnbellek.set(dz, t);
  return t;
}
/** Güçlü sayı (ondalık, yüzde, ≥ 1000) için gereken ortak kök ağırlığı; zayıf sayı (sıradan tam sayı) için daha yüksek */
const ESIK_GUCLU = 5;
const ESIK_ZAYIF = 11;
const ESIK_YILLI = 2;

const slaytYuzdeMi = (t: string, a: number, b: number) => t[a - 1] === '%' || t[a - 2] === '%' || /^\s?%/.test(t.slice(b, b + 2));
/** Sayının hemen önündeki (≤ 40 harf) son yer etiketi: il (Karabük) mü Türkiye mi */
const yerEtiketi = (t: string, i: number): 'il' | 'tr' | '' => {
  const on = t.slice(Math.max(0, i - 40), i);
  const tr = Math.max(on.lastIndexOf('Türkiye'), on.search(/\bTR\b/));
  const il = on.lastIndexOf('Karabük');
  return il < 0 && tr < 0 ? '' : il > tr ? 'il' : 'tr';
};
/** Anlamlı hane sayısı: "1.42" → 3, "2.1" → 2, "249614" → 6 */
const anlamliHane = (kan: string) => kan.replace(/^[0.]+/, '').replace('.', '').replace(/0+$/, '').length || 1;
const ondalikMi = (ham: string) => /[.,]\d{1,2}$/.test(ham) && !/^\d{1,3}(?:\.\d{3})+$/.test(ham);

export interface EslesmeSecenek {
  /** Değerin adı (gösterge kutusu / satır adı, tablo sütunu) — "farklı değer" yalnız adı bilinen değerde aranır */
  ad?: string;
  /** İl sayfası: yıllı ve "Türkiye" etiketsiz değerler ilin kendi verisidir, Türkiye geneli slayt bilgisine bağlanmaz */
  yerel?: boolean;
}

/**
 * Metindeki sayıların ders slaytında / çıkmış soruda geçtiği cümleleri bulur.
 * `baglam`: değerin adı ya da üst madde (ör. "Bebek ölüm hızı 2025") — anahtar kelime ve yıl buradan da okunur.
 */
export function dersEslesmeleri(dz: DersDizin | null, metin: string, baglam = '', sec: EslesmeSecenek = {}): DersEslesme[] {
  if (!dz || !metin) return [];
  const duz = metin.replace(/\*\*|==/g, '');
  const tum = `${baglam} ${duz}`;
  const yillar = new Set(tum.match(YIL) || []);
  const baglamYillari = [...new Set(baglam.match(YIL) || [])];
  // Değerin adı: verilen bağlam ya da metnin "Ad: değer" biçimindeki ad kısmı
  // Değerin önündeki kısa ad ("Toplam doğurganlık hızı 1,42 kadın başına çocuk" → "Toplam doğurganlık hızı")
  const onAd = (/^\s*([^\d:%]{3,70}?)\s*:?\s*%?\d/.exec(duz)?.[1] ?? '').trim();
  const onAdUygun = onAd.split(/\s+/).length <= 7 ? onAd : '';
  const adMetni = baglam || (/^([^:]{3,80}):/.exec(duz)?.[1] ?? onAdUygun);
  const ad = kokler(adMetni);
  const gerek = ad.size ? Math.min(2, ad.size) : 2;
  const aranan = ad.size ? ad : kokler(tum);
  if (!aranan.size) return [];
  const idf = idfTablosu(dz);
  const tumK = kokler(tum);
  const out: DersEslesme[] = [];
  const gor = new Set<number>();
  // Hangi sayılar değer? "Ad: **34** ASM, **90** AHB" → kalın sayılar; "**2025**: 7,8 binde (…)" → iki noktadan
  // sonraki ilk sayı (birimdeki "15-49 yaş", parantezdeki fark değer sayılmaz). Ad yoksa metindeki ilk sayı.
  const iki = duz.indexOf(':');
  const kalin = [...metin.matchAll(/\*\*([^*]+)\*\*/g)].map((x) => x[1]).filter((x) => /\d/.test(x) && !/^\s*(19|20)\d\d\s*$/.test(x));
  const adaylar = [...duz.matchAll(SAYI)].filter((m) => {
    if ((m.index ?? 0) < iki) return false;
    if (kalin.length) return kalin.some((k) => k.includes(m[2]));
    return true;
  });
  // Kalın sayılar ya da metnin ilk sayısı "birincil" değerdir (bağlamın adı ve yılı ona aittir); serbest metindeki öteki
  // sayılar ("… yenilenme düzeyinin (2,1) altında") yalnız kendi çevresiyle (± 70 harf) ve kendi yılıyla eşleşir
  const degerler = kalin.length ? adaylar : adaylar.filter((m) => !/^(19|20)\d\d$/.test(m[2]));
  // "Farklı değer" için göstergenin tam adı ve kısaltması
  const adTam = sec.ad || onAdUygun;
  const tamAd = adTam ? tamKokler(adTam) : [];
  const adKisa = adTam ? kisaltmasi(adTam.split(' · ')[0]) : '';
  const kisaRe = adKisa.length >= 3 ? new RegExp(`(^|[^\\p{L}])${adKisa}([^\\p{L}]|$)`, 'u') : null;
  const adiTasir = (c: DersCumle) => {
    if (!tamAd.length) return false;
    if (kisaRe?.test(c.t)) return true;
    const k = cumleKok(c).tam;
    return tamAd.every((x) => k.has(x));
  };
  degerler.forEach((m, sira0) => {
    const birincil = kalin.length > 0 || sira0 === 0;
    const ham = m[2];
    // Sayı bir sözcüğün parçası olmasın (ör. "PM10")
    const once = duz[(m.index ?? 0) - 1];
    if (once && /[\p{L}\d.,/]/u.test(once) && !m[1]) return;
    const kan = kanonik(ham);
    if (!kan || PAYDA.has(kan) || !anlamli(ham, kan, !!(m[1] || m[3]))) return;
    const yuzde = !!(m[1] || m[3]);
    const i0 = m.index ?? 0;
    const bas = i0 + (m[1]?.length || 0);
    const son = bas + ham.length;
    // Değerin kendi yılı: bitişik yıl, yoksa bağlamdaki tek yıl (gösterge yılı, "Yıl yıl" listesinde üst madde)
    const kendi = kendiYili(duz, bas, son);
    const vYil = kendi || (birincil && yillar.size === 1 ? Number([...yillar][0]) : birincil && baglamYillari.length === 1 ? Number(baglamYillari[0]) : 0);
    const cevre = birincil ? '' : duz.slice(Math.max(0, i0 - 70), i0 + m[0].length + 70);
    const yillarM = birincil ? yillar : new Set(kendi ? [String(kendi)] : []);
    const arananM = birincil ? aranan : kokler(`${adMetni} ${cevre}`);
    const gerekM = birincil ? gerek : 2;
    // İl sayfasında yıllı değer "Türkiye" diye etiketli değilse ilin kendi verisidir
    const etiket = yerEtiketi(duz, i0);
    const yerelDeger = etiket === 'il' || (!!sec.yerel && !!vYil && etiket !== 'tr');
    // Slayttaki sayı da aynı yere ait olmalı (soru: "Türkiye: 1,51 — Karabük: 1,14")
    const yerUyar = (c: DersCumle, a: number) => {
      const se = yerEtiketi(c.t, a);
      return yerelDeger ? se === 'il' : se !== 'il';
    };
    const sonra = duz.slice(i0 + m[0].length, i0 + m[0].length + 3);
    const sira = /^\.\s*[\p{Ll}\d]/u.test(sonra) || /^\.\s*$/.test(sonra);
    const aralik = /^\s?[-–]\s?\d/.test(sonra) || /\d\s?[-–]\s?$/.test(duz.slice(Math.max(0, i0 - 3), i0));
    const zayif = (!yuzde && !ham.includes(',') && Number(kan) < 1000) || sira || aralik;
    // Zayıf sayıda yalnız sayının yakınındaki sözcükler (± 50 harf) ve ad sayılır; uzun metinde tesadüfi ortaklık olmasın
    const yakinK = zayif ? kokler(`${adMetni} ${duz.slice(Math.max(0, i0 - 50), i0 + m[0].length + 50)}`) : birincil ? tumK : arananM;
    const say = (k: Set<string>) => { let n = 0; for (const x of arananM) if (k.has(x)) n++; return n; };
    const agirlik = (k: Set<string>) => { let w = 0; for (const x of yakinK) if (k.has(x)) w += idf.get(x) ?? 0; return w; };
    let buldu = false;
    for (const [no, a, b, sy] of dz.dizin[kan] || []) {
      if (gor.has(no)) continue;
      const c = dz.cumleler[no];
      if (!c) continue;
      // Yüzde ile yüzde olmayan aynı sayı eşleşmez ("%81" ≠ "81 yıl"); slayttaki sayı bir aralığın ucuysa da ("7.7-9.7")
      if (slaytYuzdeMi(c.t, a, b) !== yuzde) continue;
      if (/^\s?[-–]\s?\d/.test(c.t.slice(b, b + 3)) || /\d\s?[-–]\s?$/.test(c.t.slice(Math.max(0, a - 3), a))) continue;
      if (!yerUyar(c, a)) continue;
      // Yıl: iki tarafın da kendi yılı varsa aynı olmalı; sayfadaki değerin yılı slaytın cümlesinde/başlığında geçmeli
      let yilUyar = !yillarM.size;
      if (vYil && sy) { if (vYil !== sy) continue; yilUyar = true; }
      else if (vYil) {
        if (c.y.length && !c.y.includes(String(vYil))) continue;
        yilUyar = c.y.includes(String(vYil));
        // Yılsız slayt cümlesi (genel bilgi): yalnız tesadüfe kapalı sayıda (≥ 3 anlamlı hane) ve gösterge adı geçiyorsa
        if (!c.y.length && (!adiTasir(c) || zayif || anlamliHane(kan) < 3)) continue;
      } else if (sy) {
        // Yılsız değer (eşik, norm: "yenilenme düzeyi 2,1") bir yılın istatistiğine ("2013: 2,1") bağlanmaz; yılı
        // yazılmayan güncel gösterge ("Canlı doğum sayısı 895.374") yalnız tesadüfe kapalı sayıda ve adı geçiyorsa
        if (anlamliHane(kan) < 3 || !adiTasir(c)) continue;
      } else if (yillarM.size && c.y.length) {
        if (!c.y.some((y) => yillarM.has(y))) continue;
        yilUyar = true;
      }
      const ck = cumleKok(c);
      const cumleK = ck.t;
      // Yıl uyuşuyorsa slayt başlığı da sayılır; yoksa ad cümlenin kendisinde geçmeli
      const bakilan = yilUyar ? ck.tb : cumleK;
      const tamUyar = adiTasir(c);
      if (!tamUyar && say(bakilan) < gerekM) continue;
      // Ortak sözcüklerin ağırlığı: sıradan tam sayı ("24 saat", "10. hafta") tesadüfe açık → çok daha yüksek eşik
      // Yıl da uyuşuyorsa (güçlü kanıt) eşik düşer
      const esik = zayif ? ESIK_ZAYIF : yilUyar ? ESIK_YILLI : ESIK_GUCLU;
      if (!(tamUyar && !zayif) && agirlik(zayif ? cumleK : bakilan) < esik) continue;
      gor.add(no);
      buldu = true;
      out.push({ tur: 'ayni', cumle: c, deste: c.q ? 'Çıkmış soru' : dz.desteler[c.d] || c.d, bas, son, ham, sa: a, sb: b });
    }
    // Aynı gösterge + aynı yıl için slaytta başka değer: ölçek aynı (oran 0,75–1,33), ikisi de ondalık ya da ikisi de büyük sayı
    if (!buldu && vYil && tamAd.length && !yerelDeger && !zayif) {
      const deger = Number(kan);
      let enIyi: DersEslesme | null = null;
      let fark = Infinity;
      for (const [no, a, b, skan] of yilDizini(dz).get(vYil) || []) {
        if (skan === kan || gor.has(no)) continue;
        const c = dz.cumleler[no];
        if (!c || c.q) continue;
        const sd = Number(skan);
        const oran = sd / deger;
        if (!(oran >= 0.75 && oran <= 1.33)) continue;
        const sham = c.t.slice(a, b);
        if (ondalikMi(sham) !== ondalikMi(ham) || slaytYuzdeMi(c.t, a, b) !== yuzde) continue;
        if (!adiTasir(c) || !yerUyar(c, a)) continue;
        const f = Math.abs(Math.log(oran));
        if (f < fark) { fark = f; enIyi = { tur: 'farkli', cumle: c, deste: dz.desteler[c.d] || c.d, bas, son, ham, sa: a, sb: b, slaytDeger: sham, yil: vYil }; }
      }
      if (enIyi) { gor.add(dz.cumleler.indexOf(enIyi.cumle)); out.push(enIyi); }
    }
  });
  return out;
}

/* ---------------------------------------------------------------------------------------------------------------
 * Terimler — Python ders_eslesme.py'deki terim_katla / terim_koku / eslesir ile aynı kurallar
 * --------------------------------------------------------------------------------------------------------------- */

const terimKatla = (s: string) => s.replace(/İ/g, 'i').replace(/I/g, 'ı').toLowerCase()
  .replace(/ı/g, 'i').replace(/ş/g, 's').replace(/ç/g, 'c').replace(/ğ/g, 'k').replace(/ö/g, 'o').replace(/ü/g, 'u')
  .replace(/[âà]/g, 'a').replace(/î/g, 'i').replace(/û/g, 'u');
const terimKoku = (w: string) => (w.length <= 4 ? w : w.slice(0, Math.max(4, Math.ceil(w.length * 0.75))));
const esler = (sayfa: string, terim: string, tek = false) => {
  // Tek sözcüklü terimde sözcüğün tamamı aranır ("servisit" ≠ "servisi")
  if (tek && terim.length > 4) return sayfa.startsWith(terim) && sayfa.length <= terim.length + 6;
  if (terim.length <= 4) return sayfa === terim || (terim.length >= 3 && sayfa.startsWith(terim) && sayfa.length - terim.length <= 4);
  return sayfa.startsWith(terimKoku(terim)) && sayfa.length <= terim.length + 6;
};
interface Sozcuk { w: string; f: string; a: number; b: number }
const SOZCUK = /[A-Za-zÇĞİÖŞÜçğıöşüÂâÎîÛû]+(?:['’][A-Za-zÇĞİÖŞÜçğıöşüÂâÎîÛû]+)?/g;
/** Aralarında yalnız boşluk/tire olan sözcük dizileri (noktalama diziyi böler) */
function ardisik(s: string): Sozcuk[][] {
  const out: Sozcuk[][] = [];
  let cur: Sozcuk[] = [];
  let son = -1;
  for (const m of s.matchAll(SOZCUK)) {
    const w = m[0].split(/['’]/)[0];
    const x = { w, f: terimKatla(w), a: m.index ?? 0, b: (m.index ?? 0) + w.length };
    if (cur.length) {
      const ara = s.slice(son, x.a);
      if (!/^[\s-]*$/.test(ara) && !/^['’]\S*\s*$/.test(ara)) { out.push(cur); cur = []; }
    }
    cur.push(x);
    son = x.b;
  }
  if (cur.length) out.push(cur);
  return out;
}

const terimOnbellek = new WeakMap<DersDizin, Map<string, DersTerim[]>>();
function terimKovasi(dz: DersDizin) {
  let t = terimOnbellek.get(dz);
  if (t) return t;
  t = new Map();
  // Dizin uzun terimleri önce yazar → kovada da uzun önce (en uzun eşleşme kazanır)
  for (const x of dz.terimler || []) {
    const k = x.a ? terimKatla(x.a).slice(0, 3) : x.k[0].slice(0, 3);
    (t.get(k) || t.set(k, []).get(k)!).push(x);
  }
  terimOnbellek.set(dz, t);
  return t;
}

function diziEslesmesi(dz: Sozcuk[], i: number, x: DersTerim): number {
  if (x.a) return dz[i].w === x.a ? 1 : 0;
  if (i + x.k.length > dz.length) return 0;
  for (let j = 0; j < x.k.length; j++) if (!esler(dz[i + j].f, x.k[j], x.k.length === 1)) return 0;
  return x.k.length;
}

/** Metinde geçen terimler: [başlangıç, bitiş, terim] (çakışmasız, en uzun eşleşme) */
export function terimleriBul(dz: DersDizin | null, metin: string): [number, number, DersTerim][] {
  if (!dz?.terimler?.length || !metin) return [];
  const kova = terimKovasi(dz);
  const out: [number, number, DersTerim][] = [];
  for (const d of ardisik(metin)) {
    for (let i = 0; i < d.length;) {
      let n = 0;
      let bulunan: DersTerim | null = null;
      for (const x of kova.get(d[i].f.slice(0, 3)) || []) {
        const k = diziEslesmesi(d, i, x);
        if (k > n) { n = k; bulunan = x; }
      }
      if (bulunan) { out.push([d[i].a, d[i + n - 1].b, bulunan]); i += n; } else i++;
    }
  }
  return out;
}

/** Terimin slayt/soru cümlesindeki aralığı (balonda vurgulamak için) */
export function terimAraligi(t: string, x: DersTerim): [number, number] | null {
  for (const d of ardisik(t)) for (let i = 0; i < d.length; i++) {
    const n = diziEslesmesi(d, i, x);
    if (n) return [d[i].a, d[i + n - 1].b];
  }
  return null;
}
