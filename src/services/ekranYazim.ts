/**
 * Sesli ders ekran yazımı (kullanıcı, 2026-10-22): konuşma metni okunuşla yazılır ("on dördüncü hafta", "beta ha ce ge",
 * "doku plazminojen aktivatörü"); ekranda slayttaki gibi gösterilir: "14. hafta", "β-hCG", "doku plazminojen aktivatörü
 * (t-PA)", "12+6 hafta", "20-24. hafta", "δ". Saklanan metin, ses ve cümle zamanı değişmez; konumlar eşlemeyle taşınır.
 * Sözlük: scripts/sesli_anlatim/yazim_sozlugu.py → src/data/sesli_anlatim/yazim_sozlugu.json.
 * Ses tarafının tersi: scripts/sesli_anlatim/okunus.py SAYI_TTS (ekrandaki rakam → okunuş).
 */
import sozluk from '../data/sesli_anlatim/yazim_sozlugu.json';
import { sayilariYazEslemeli } from './sayiYazim';

type Konum = (k: number, bitis?: boolean) => number;
type Fn = (...a: any[]) => string;

/** Bir regex geçişi + eski→yeni konum eşlemesi (dönüşen parçanın içine düşen konum başına/sonuna yapışır). */
function gecis(t: string, re: RegExp, fn: Fn): { yeni: string; f: Konum } {
  const d: [number, number, number, number][] = [];
  let kay = 0;
  const yeni = t.replace(re, (...a: any[]) => {
    const m = a[0] as string;
    const i = a.find((x, j) => j > 0 && typeof x === 'number') as number;
    const r = fn(...a);
    if (r !== m) {
      d.push([i, i + m.length, i + kay, i + kay + r.length]);
      kay += r.length - m.length;
    }
    return r;
  });
  const f: Konum = (k, bitis = false) => {
    let off = 0;
    for (const [os, oe, ns, ne] of d) {
      if (k < os || (k === os && !bitis)) break;
      if (k < oe || (k === oe && bitis && k === os)) return bitis ? ne : ns;
      off = ne - oe;
    }
    return k + off;
  };
  return { yeni, f };
}

const tr = (s: string) => s.toLocaleLowerCase('tr');
const esc = (s: string) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const L = '\\p{L}';
const ON = `(?<![${L}\\d])`;
const SON = `(?![${L}\\d])`;

/* ---------- sayılar ---------- */
const DEGER: Record<string, number> = {
  sıfır: 0, bir: 1, iki: 2, üç: 3, dört: 4, beş: 5, altı: 6, yedi: 7, sekiz: 8, dokuz: 9,
  on: 10, yirmi: 20, otuz: 30, kırk: 40, elli: 50, altmış: 60, yetmiş: 70, seksen: 80, doksan: 90,
  yüz: 100, bin: 1000, milyon: 1e6,
};
const SIRA: Record<string, number> = {
  birinci: 1, ikinci: 2, üçüncü: 3, dördüncü: 4, beşinci: 5, altıncı: 6, yedinci: 7, sekizinci: 8, dokuzuncu: 9,
  onuncu: 10, yirminci: 20, otuzuncu: 30, kırkıncı: 40, ellinci: 50, altmışıncı: 60, yetmişinci: 70, sekseninci: 80,
  doksanıncı: 90, yüzüncü: 100, bininci: 1000,
};
const buyukte = (ks: string[]) => ks.flatMap((k) => [k, k[0].toLocaleUpperCase('tr') + k.slice(1)]).sort((a, b) => b.length - a.length).join('|');
const KOK = buyukte(Object.keys(DEGER));
const SKOK = buyukte(Object.keys(SIRA));
const EK = "(?:y?[dt][ıiuü]r|y?[aeıiuü]|n?[dt][ae]n?|n?[ıiuü]n|s?[ıiuü](?:n[ae]|nd[ae]n?|n[ıiuü]n)?|y?l[ae]|l[ae]r[ıi]?|y?[ıiuü]n[ae]|l[ıiuü]k)?";
const DIZI = `(?:${KOK})(?:\\s+(?:${KOK}))*`;
const SDIZI = `(?:(?:${KOK})\\s+)*(?:${SKOK})`;

function deger(sozler: string[]): number {
  let toplam = 0, cur = 0;
  for (const w of sozler) {
    const v = DEGER[w] ?? SIRA[w];
    if (v === 100) cur = (cur || 1) * 100;
    else if (v >= 1000) { toplam += (cur || 1) * v; cur = 0; }
    else cur += v;
  }
  return toplam + cur;
}
const say = (s: string) => deger(tr(s).trim().split(/\s+/));
const ekli = (n: string, ek: string) => (ek ? `${n}'${ek}` : n);
// "bir" tek başına çoğunlukla belirsizlik sözcüğü ("bir kadın"); yalnız bu sözcüklerden sonra sayıdır
const BIR_ONU = /(?:trizomi|tip|evre|faktör|derece|grade|sınıf|kromozom|madde|hafta|gün|ay|yıl|kategori)\s*$/i;

const R_SIRA_ARALIK = new RegExp(`${ON}(${SDIZI})\\s+ile\\s+(${SDIZI})(${EK})${SON}`, 'gu');
const R_HAFTA_GUN = new RegExp(`${ON}(${DIZI})\\s+hafta\\s+artı\\s+(${DIZI})\\s+gün(${EK})${SON}`, 'gu');
const R_ARTI = new RegExp(`${ON}(${DIZI})\\s+artı\\s+(${DIZI})(${EK})${SON}`, 'gu');
const R_ARALIK = new RegExp(`${ON}(${DIZI})\\s+ile\\s+(${DIZI})(${EK})${SON}`, 'gu');
const R_SIRA = new RegExp(`${ON}(${SDIZI})(${EK})${SON}`, 'gu');
const R_SAYI = new RegExp(`${ON}(${DIZI})(${EK})${SON}`, 'gu');
const R_YUZDE_ILE = new RegExp(`%(\\d+(?:,\\d+)?)\\s+ile\\s+(${DIZI})(${EK})${SON}`, 'gu');
const BIRIM: Record<string, string> = {
  'mili ünite': 'mIU', 'ünite': 'U', 'miligram': 'mg', 'mikrogram': 'µg', 'nanogram': 'ng', 'gram': 'g', 'kilogram': 'kg',
  'mililitre': 'mL', 'desilitre': 'dL', 'litre': 'L', 'milimetre cıva': 'mmHg', 'milimetre': 'mm', 'santimetre': 'cm',
  'mikrometre': 'µm', 'milimol': 'mmol', 'miliosmol': 'mOsm', 'mikromol': 'µmol', 'nanomol': 'nmol', 'pikogram': 'pg',
};
const BIRIM_RE = Object.keys(BIRIM).sort((a, b) => b.length - a.length).map((k) => k.replace(' ', '\\s+')).join('|');
const birim = (s: string) => BIRIM[tr(s).replace(/\s+/g, ' ')] ?? s;
const R_TIRE = new RegExp(`(\\d+)\\s+tire\\s+(\\d+)${SON}`, 'gu');
const R_KARYO = new RegExp(`(?<![\\d,])(4[5-9]|69|92)\\s+([XY]{1,4})${SON}`, 'gu');
const R_KARYO_ARTI = new RegExp(`(\\d,[XY]{1,4})\\s+artı\\s+(\\d+)${SON}`, 'gu');
const R_ISARET = new RegExp(`${ON}(eksi|artı)\\s+(\\d+(?:,\\d+)?)${SON}`, 'giu');
// "mili ünite bölü mililitre" → "mIU/mL"; "miligram" yalnız rakamdan sonra → "200 mg" (düz "gram" sözcüğü rakamla bile yazıda kalır)
const R_BOLU = new RegExp(`${ON}(${BIRIM_RE})\\s+bölü\\s+(${BIRIM_RE})(${EK})${SON}`, 'giu');
const R_BIRIM = new RegExp(`(\\d)\\s+(${BIRIM_RE.replace('|gram|', '|')})(${EK})${SON}`, 'giu');
const GUN_HAFTA: Record<string, string> = { e: 'ya', de: 'da', den: 'dan', dür: 'dır', lük: 'lık', ün: 'ın', ü: 'ı' };

const tekSozluk = (dizi: string) => !/\s/.test(dizi.trim());
function sayiGec(dizi: string, ek: string, onu: string): string | null {
  const w = tr(dizi.trim());
  const ws = w.split(/\s+/);
  if (ws.some((x, i) => i && x === ws[i - 1])) return null; // "yüz yüze", "bir bir"
  if (tekSozluk(dizi)) {
    if (dizi[0] !== w[0] && w === 'bir') return null; // cümle başı "Bir"
    if (w === 'bir' && !BIR_ONU.test(onu)) return null;
    if (w === 'yüz' || w === 'bin') return null; // "yüz" = yüz (surat), "bin" fiil olabilir
    if (ek) return null; // "onu", "altında", "ikisi" — zamir/yer bildirebilir
    if (w === 'altı' && /(?:[ıiuü]n|n[ıiuü]n)\s*$/i.test(onu)) return null; // "miligramın altı"
  }
  return ekli(String(say(dizi)), ek);
}

/* ---------- sözlük geçişleri ---------- */
const KIS = (sozluk.kisaltma as [string, string][]);
const R_KIS = KIS.length
  ? new RegExp(`${ON}(${KIS.map(([o]) => o.split(' ').map(esc).join('\\s+')).join('|')})(${EK})${SON}`, 'giu')
  : null;
const KIS_HARITA = new Map(KIS.map(([o, y]) => [o, y]));
const ACI = (sozluk.acilim as [string, string][]);
// açılımın son sözcüğüne çekim eki gelebilir ("faktörüne"); kısaltma sözcüğün ardına parantezle eklenir
const R_ACI = ACI.length
  ? new RegExp(`${ON}(${ACI.map(([a]) => a.split(' ').map(esc).join('\\s+')).join('|')})(\\p{L}*)(?!\\s*\\()`, 'giu')
  : null;
const ACI_HARITA = new Map(ACI.map(([a, k]) => [a, k]));
const YUNAN = sozluk.yunan as Record<string, string>;
const R_YUNAN = new RegExp(`${ON}(${Object.keys(YUNAN).join('|')})${SON}`, 'giu');

function zincir(metin: string, adimlar: [RegExp | null, Fn][]): { metin: string; konum: Konum } {
  let t = metin;
  const fs: Konum[] = [];
  for (const [re, fn] of adimlar) {
    if (!re) continue;
    const g = gecis(t, re, fn);
    if (g.yeni !== t) { fs.push(g.f); t = g.yeni; }
  }
  return { metin: t, konum: (k, b) => fs.reduce((x, f) => f(x, b), k) };
}

function adimlar(): [RegExp | null, Fn][] {
  const goruldu = new Set<string>();
  const onu = (s: string, i: number) => s.slice(Math.max(0, i - 24), i);
  return [
    [R_KIS, (m: string, o: string, ek: string) => {
      const y = KIS_HARITA.get(tr(o).replace(/\s+/g, ' '));
      return y ? ekli(y, ek) : m;
    }],
    [R_ACI, (m: string, a: string, kuyruk: string) => {
      const k = ACI_HARITA.get(tr(a).replace(/\s+/g, ' '));
      if (!k || goruldu.has(k)) return m; // paragrafta ilk geçişte bir kez
      goruldu.add(k);
      return `${m} (${k})`;
    }],
    [R_YUNAN, (m: string, a: string) => YUNAN[tr(a)] ?? m],
    [R_SIRA_ARALIK, (_m: string, a: string, b: string, ek: string) => ekli(`${say(a)}-${say(b)}.`, ek)],
    [R_HAFTA_GUN, (_m: string, a: string, b: string, ek: string) => `${say(a)}+${say(b)} hafta${GUN_HAFTA[ek] ?? ek}`],
    [R_ARTI, (_m: string, a: string, b: string, ek: string) => ekli(`${say(a)}+${say(b)}`, ek)],
    [R_ARALIK, (m: string, a: string, b: string, ek: string, i: number, s: string) =>
      sayiGec(a, '', onu(s, i)) === null ? m : ekli(`${say(a)}-${say(b)}`, ek)],
    [R_SIRA, (_m: string, a: string, ek: string) => ekli(`${say(a)}.`, ek)],
    [R_YUZDE_ILE, (_m: string, n: string, b: string, ek: string) => ekli(`%${n}-${say(b)}`, ek)],
    [R_SAYI, (m: string, a: string, ek: string, i: number, s: string) => sayiGec(a, ek, onu(s, i)) ?? m],
    // rakamlar yerleştikten sonra işaretler ve birimler (okunuş değil yazım: "2-5", "47,XY,+18", "-3", "mIU/mL", "25 mm")
    [R_TIRE, (_m: string, a: string, b: string) => `${a}-${b}`],
    [R_KARYO, (_m: string, n: string, k: string) => `${n},${k}`],
    [R_KARYO_ARTI, (_m: string, k: string, n: string) => `${k},+${n}`],
    [R_ISARET, (_m: string, isaret: string, n: string) => `${tr(isaret) === 'eksi' ? '-' : '+'}${n}`],
    [R_BOLU, (_m: string, a: string, b: string, ek: string) => ekli(`${birim(a)}/${birim(b)}`, ek)],
    [R_BIRIM, (_m: string, n: string, b: string, ek: string) => ekli(`${n} ${birim(b)}`, ek)],
  ];
}

/** Ekran yazımı + eski konumu yeni metne çeviren işlev. Önce ondalık/yüzde (sayiYazim), sonra yukarıdaki geçişler. */
export function ekranYazimiEslemeli(metin: string): { metin: string; konum: Konum } {
  const a = sayilariYazEslemeli(metin);
  const b = zincir(a.metin, adimlar());
  // "%15 ile 20" → "%15-20"
  const c = gecis(b.metin, /(%\d+(?:,\d+)?) ile (\d+(?:,\d+)?)(?![\d,])/gu, (_m: string, x: string, y: string) => `${x}-${y}`);
  return { metin: c.yeni, konum: (k, bitis) => c.f(b.konum(a.konum(k, bitis), bitis), bitis) };
}
export const ekranYazimi = (metin: string) => ekranYazimiEslemeli(metin).metin;
