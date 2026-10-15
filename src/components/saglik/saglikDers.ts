import { createContext, useContext } from 'react';

/**
 * "Ders slaytında geçiyor" işareti: sayfadaki bir değer ders slaytındaki bir cümlede de geçiyorsa (aynı sayı + ortak
 * anahtar kelime + yıl uyumu) değerin sağ üstüne "!" konur ve sayı vurgulanır.
 * Dizin: src/data/saglik/ders_eslesme.json (scripts/saglik/ders_eslesme.py) — tembel yüklenir.
 */

export interface DersCumle { d: string; s: number; b: string; t: string; y: string[] }
export interface DersDizin { desteler: Record<string, string>; cumleler: DersCumle[]; dizin: Record<string, [number, number, number][]> }
export interface DersEslesme { cumle: DersCumle; deste: string; bas: number; son: number; ham: string }

export const DersCtx = createContext<DersDizin | null>(null);
export const useDersDizin = () => useContext(DersCtx);

let yuk: Promise<DersDizin> | null = null;
export const dersDiziniYukle = () => (yuk ||= import('../../data/saglik/ders_eslesme.json').then((m) => (m.default || m) as unknown as DersDizin));

// Slayttaki ve sayfadaki sayılar aynı biçimde okunur (Python betiğindeki SAYI ile aynı)
const SAYI = /(%\s?)?(\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+(?:[.,]\d+)?)(\s?%|\s?‰)?/g;
const YIL = /\b(19[5-9]\d|20[0-4]\d)\b/g;
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
/** Güçlü sayı (ondalık, yüzde, ≥ 1000) için gereken ortak kök ağırlığı; zayıf sayı (sıradan tam sayı) için daha yüksek */
const ESIK_GUCLU = 5;
const ESIK_ZAYIF = 11;
const ESIK_YILLI = 2;

/**
 * Metindeki sayıların ders slaytında geçtiği cümleleri bulur.
 * `baglam`: değerin adı ya da üst madde (ör. "Bebek ölüm hızı") — anahtar kelime eşleşmesi buradan da yapılır.
 */
export function dersEslesmeleri(dz: DersDizin | null, metin: string, baglam = ''): DersEslesme[] {
  if (!dz || !metin) return [];
  const duz = metin.replace(/\*\*|==/g, '');
  const tum = `${baglam} ${duz}`;
  const yillar = new Set(tum.match(YIL) || []);
  // Değerin adı: verilen bağlam ya da metnin "Ad: değer" biçimindeki ad kısmı
  const adMetni = baglam || (/^([^:]{3,80}):/.exec(duz)?.[1] ?? '');
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
  const degerler = kalin.length ? adaylar : adaylar.filter((m) => !/^(19|20)\d\d$/.test(m[2])).slice(0, 1);
  for (const m of degerler) {
    const ham = m[2];
    // Sayı bir sözcüğün parçası olmasın (ör. "PM10")
    const once = duz[(m.index ?? 0) - 1];
    if (once && /[\p{L}\d.,/]/u.test(once) && !m[1]) continue;
    const kan = kanonik(ham);
    if (!kan || PAYDA.has(kan) || !anlamli(ham, kan, !!(m[1] || m[3]))) continue;
    const yuzde = !!(m[1] || m[3]);
    const i0 = m.index ?? 0;
    const sonra = duz.slice(i0 + m[0].length, i0 + m[0].length + 3);
    const sira = /^\.\s*[\p{Ll}\d]/u.test(sonra) || /^\.\s*$/.test(sonra);
    const aralik = /^\s?[-–]\s?\d/.test(sonra) || /\d\s?[-–]\s?$/.test(duz.slice(Math.max(0, i0 - 3), i0));
    const zayif = (!yuzde && !ham.includes(',') && Number(kan) < 1000) || sira || aralik;
    // Zayıf sayıda yalnız sayının yakınındaki sözcükler (± 50 harf) ve ad sayılır; uzun metinde tesadüfi ortaklık olmasın
    const yakinK = zayif ? kokler(`${adMetni} ${duz.slice(Math.max(0, i0 - 50), i0 + m[0].length + 50)}`) : tumK;
    for (const [no, a, b] of dz.dizin[kan] || []) {
      if (gor.has(no)) continue;
      const c = dz.cumleler[no];
      if (!c) continue;
      // Yüzde ile yüzde olmayan aynı sayı eşleşmez ("%81" ≠ "81 yıl")
      const slaytYuzde = c.t[a - 1] === '%' || c.t[a - 2] === '%' || /^\s?%/.test(c.t.slice(b, b + 2));
      if (slaytYuzde !== yuzde) continue;
      // Değerin yılı varsa slaytın cümlesinde ya da başlığında aynı yıl geçmeli (yılsız genel bilgiye bağlanmaz)
      if (yillar.size && !c.y.some((y) => yillar.has(y))) continue;
      const say = (k: Set<string>) => { let n = 0; for (const x of aranan) if (k.has(x)) n++; return n; };
      const agirlik = (k: Set<string>) => { let w = 0; for (const x of yakinK) if (k.has(x)) w += idf.get(x) ?? 0; return w; };
      const cumleK = kokler(c.t);
      // Yıl uyuşuyorsa slayt başlığı da sayılır; yoksa ad cümlenin kendisinde geçmeli
      const bakilan = yillar.size ? new Set([...cumleK, ...kokler(c.b)]) : cumleK;
      if (say(bakilan) < gerek) continue;
      // Ortak sözcüklerin ağırlığı: sıradan tam sayı ("24 saat", "10. hafta") tesadüfe açık → çok daha yüksek eşik
      // Yıl da uyuşuyorsa (güçlü kanıt) eşik düşer
      const esik = zayif ? ESIK_ZAYIF : yillar.size ? ESIK_YILLI : ESIK_GUCLU;
      if (agirlik(zayif ? cumleK : bakilan) < esik) continue;
      gor.add(no);
      const bas = (m.index ?? 0) + (m[1]?.length || 0);
      out.push({ cumle: c, deste: dz.desteler[c.d] || c.d, bas, son: bas + ham.length, ham });
    }
  }
  return out;
}

/** Slayt cümlesinde vurgulanacak aralık: aynı kanonik sayıyı taşıyan ilk konum */
export function cumleAraligi(dz: DersDizin, e: DersEslesme): [number, number] | null {
  const kan = kanonik(e.ham);
  const no = dz.cumleler.indexOf(e.cumle);
  const r = kan ? (dz.dizin[kan] || []).find(([n]) => n === no) : undefined;
  return r ? [r[1], r[2]] : null;
}
