/**
 * 60 planı — kurul sınavından en az 60 almak için kişiye özel çalışma planı (Bitirdiklerim › Sınav planı).
 *
 * Girdi: aktif kurulun soru dağılımı (data/sinav_dagilimi.json), dersler (en önemliler + soru çözücü dizinleri, sesli
 * ders listesi; ders birimi = branş + branş içi numara), öğrencinin işaretleri ve çözdüğü soruların sonucu
 * (calismaTakip, en önemliler "öğrendim", soru çözücü ilerlemesi), çalışma hızı ve sınava kalan saat.
 *
 * Puan: branşta n soru, d doğru → d ≥ n/2 ise d; değilse 2d − n/2 (baraj: yarıdan eksik her doğru kadar eksi).
 *
 * Model:
 *  - Dersin branştaki payı w = 0,5·madde payı + 0,3·soru bankası payı + 0,2·ders süresi payı (kazanım, çıkmış sıklığı, ders uzunluğu).
 *  - Bilgi düzeyi k = 1 − (1 − 0,55·sesli)(1 − 0,45·önemliler)(1 − 0,40·soru); 12 günden eski çalışma %10 unutulur.
 *  - Doğru olasılığı p = 0,22 + 0,62·k (çalışılmamış konuda şıklardan eleme payı, çalışılmış konuda da hata payı var: en çok ~%75).
 *  - Öğrencinin soru çözücüdeki ilk deneme doğruları modeli branş bazında düzeltir (çok soru çözdükçe ağırlığı artar).
 *  - Branşta doğru sayısı beta-binom (tahmin belirsizliği + dikkat hatası); branş puanları birleştirilip P(puan ≥ 60) tam hesaplanır.
 * Plan: her ders için sıradaki adım (en önemliler asistanı → soru çözücü → sesli ders) adayı; amaç E[puan] + 30·P(≥60),
 * her turda "kazanç / süre"si en yüksek adım seçilir (baraj altı branşta her doğru 2 puan değerinde olduğu için kendiliğinden öne çıkar).
 * P(≥60) %90'a ulaşınca plan durur: kalan vakit dinlenme ve isteğe bağlı tekrar.
 */
import dagilim from '../../data/sinav_dagilimi.json';
import { navigateTo, pathFor } from '../../router';
import { bittiMi, type Hiz, type TakipModul, takipOku } from '../../services/calismaTakip';
import { aktifKurul } from '../../services/kurulTakvimi';
import { cdListeGetir, type CdListeDers } from '../canliDers/canliDersStore';
import { CD_SPOT_BRANS } from '../canliDers/canliDersKategori';
import { bransTanim, type Brans } from '../spots/brans';
import { cozucuDizinYukle, ilerlemeOku, ozet, type CDizinDers } from '../spots/cozucu/cozucuVeri';
import { dizinYukle as onemDizinYukle, ogrenilenler, type DizinDers } from '../spots/onem/onemVeri';
import { getAsistanSureGruplari } from '../spots/sure/spotsSureVeri';
import { cozucuyaGit, onemeGit } from '../spots/spotsYol';

export type AdimTur = 'onem' | 'cozucu' | 'sesli';
export type Asama = 'baraj' | 'puan' | 'pekistir';

interface KurulDagilim { toplam: number; hedef: number; branslar: Record<string, number> }
export const kurulDagilimi = (kurul: number): KurulDagilim | null =>
  ((dagilim as { kurullar: Record<string, KurulDagilim> }).kurullar[String(kurul)]) || null;

/* ── Ham veri ─────────────────────────────────────────────────────────── */

export interface PlanDers {
  anahtar: string;
  brans: Brans;
  no: number;
  ad: string;
  onem?: DizinDers & { sure: number; asistan: boolean };
  cozucu: CDizinDers[];
  sesli: CdListeDers[];
}
export interface PlanVeri { kurul: number; sinav: string; dagilim: KurulDagilim; dersler: PlanDers[] }

const SORU_SN = 75;
const MADDE_SN = 40;

export async function planVerisiYukle(): Promise<PlanVeri | null> {
  const k = aktifKurul();
  const dg = kurulDagilimi(k.kurul);
  if (!dg) return null;
  const branslar = Object.keys(dg.branslar) as Brans[];
  const asistanSure = new Map<string, number>();
  for (const g of getAsistanSureGruplari()) for (const d of g.dersler) asistanSure.set(`${g.brans}/${d.kod}`, d.sure);
  const [sesli, ...dz] = await Promise.all([
    cdListeGetir().catch(() => [] as CdListeDers[]),
    ...branslar.map((b) => Promise.all([onemDizinYukle(b).catch(() => null), cozucuDizinYukle(b).catch(() => null)])),
  ]);
  const dersler = new Map<string, PlanDers>();
  const al = (b: Brans, no: number, ad: string) => {
    const a = `${b}|${no}`;
    let d = dersler.get(a);
    if (!d) { d = { anahtar: a, brans: b, no, ad, cozucu: [], sesli: [] }; dersler.set(a, d); }
    return d;
  };
  branslar.forEach((b, i) => {
    const [o, c] = dz[i] as [{ dersler: DizinDers[] } | null, { dersler: CDizinDers[] } | null];
    for (const d of o?.dersler || []) {
      const as = asistanSure.get(`${b}/${d.kod}`);
      al(b, Number(d.no), d.baslik).onem = { ...d, sure: as || d.madde * MADDE_SN, asistan: !!as && bransTanim(b).asistan };
    }
    for (const d of c?.dersler || []) al(b, Number(d.no), d.baslik).cozucu.push(d);
  });
  // Sesli ders yalnız bilinen bir derse bağlanır (kamp / son prova bölümleri ayrı)
  for (const d of sesli as CdListeDers[]) {
    const b = d.brans ? CD_SPOT_BRANS[d.brans] : undefined;
    if (!b || (d.kurul && d.kurul !== k.kurul)) continue;
    const x = dersler.get(`${b}|${Number(d.no)}`);
    if (x) x.sesli.push(d);
  }
  return { kurul: k.kurul, sinav: k.sinav, dagilim: dg, dersler: [...dersler.values()] };
}

/* ── Durum ve olasılık ───────────────────────────────────────────────── */

interface Durum { sesli: number; onem: number; soru: number; eski: boolean }
const bilgi = (s: Durum) => {
  const k = 1 - (1 - 0.55 * s.sesli) * (1 - 0.45 * s.onem) * (1 - 0.40 * s.soru);
  return s.eski ? k * 0.9 : k;
};
const TABAN = 0.22;
const pOf = (s: Durum, kal: number) => TABAN + 0.62 * bilgi(s) * kal;

/* beta-binom: doğru sayısı dağılımı (n soru, ortalama p, yoğunluk c) */
const lgam = (x: number): number => {
  const g = [76.18009172947146, -86.50532032941677, 24.01409824083091, -1.231739572450155, 0.1208650973866179e-2, -0.5395239384953e-5];
  let y = x; const t = x + 5.5 - (x + 0.5) * Math.log(x + 5.5);
  let s = 1.000000000190015;
  for (const c of g) s += c / ++y;
  return -t + Math.log(2.5066282746310005 * s / x);
};
const YOGUNLUK = 25;
function betaBinom(n: number, p: number): number[] {
  const a = Math.max(1e-3, p * YOGUNLUK), b = Math.max(1e-3, (1 - p) * YOGUNLUK);
  const lb = lgam(a) + lgam(b) - lgam(a + b);
  const out: number[] = [];
  let top = 0;
  for (let d = 0; d <= n; d++) {
    const v = Math.exp(lgam(n + 1) - lgam(d + 1) - lgam(n - d + 1) + lgam(d + a) + lgam(n - d + b) - lgam(n + a + b) - lb);
    out.push(v); top += v;
  }
  return out.map((v) => v / top);
}
/** Branş puanı (yarım puan biriminde, 2·puan): d ≥ n/2 → 2d; değilse 4d − n */
const puan2 = (d: number, n: number) => (2 * d >= n ? 2 * d : 4 * d - n);
export const bransPuani = (d: number, n: number) => puan2(d, n) / 2;

/** Dağılım: { min, p[] } — puan2 = min + i */
interface Dag { min: number; p: number[] }
function bransDag(n: number, p: number): Dag {
  const bb = betaBinom(n, p);
  const min = puan2(0, n), max = puan2(n, n);
  const arr = new Array(max - min + 1).fill(0);
  bb.forEach((v, d) => { arr[puan2(d, n) - min] += v; });
  return { min, p: arr };
}
function birlestir(x: Dag, y: Dag): Dag {
  const p = new Array(x.p.length + y.p.length - 1).fill(0);
  for (let i = 0; i < x.p.length; i++) { const a = x.p[i]; if (a < 1e-12) continue; for (let j = 0; j < y.p.length; j++) p[i + j] += a * y.p[j]; }
  return { min: x.min + y.min, p };
}
const BIR: Dag = { min: 0, p: [1] };
const beklenen = (d: Dag) => d.p.reduce((s, v, i) => s + v * (d.min + i), 0) / 2;
const enAz = (d: Dag, hedef: number) => d.p.reduce((s, v, i) => s + (d.min + i >= hedef * 2 ? v : 0), 0);
/** Puanın %20 olasılıkla altında kalacağı değer (kötü gün) */
const yuzdelik = (d: Dag, q: number) => { let s = 0; for (let i = 0; i < d.p.length; i++) { s += d.p[i]; if (s >= q) return (d.min + i) / 2; } return (d.min + d.p.length - 1) / 2; };

/* ── Plan ────────────────────────────────────────────────────────────── */

export interface PlanAdim {
  ders: PlanDers;
  tur: AdimTur;
  sn: number;
  asama: Asama;
  /** adımın beklenen puan kazancı */
  kazanc: number;
  /** adımdan sonra P(≥60) */
  olasilik: number;
  baslik: string;
  ac: () => void;
  gun?: number;
}
export interface BransPlan {
  brans: Brans;
  ad: string;
  n: number;
  /** şu anki beklenen doğru / puan */
  dogru: number;
  puan: number;
  /** plan sonrası */
  planDogru: number;
  planPuan: number;
  calismaSn: number;
  soruSn: number;
  ders: number;
  biten: number;
  /** öğrencinin soru çözücüdeki ilk deneme doğru oranı (yeterli soru varsa) */
  isabet?: number;
  cozulen: number;
}
export interface PlanGun { gun: number; tarih: string; kapasiteSn: number; adimlar: PlanAdim[]; sn: number }
export interface PlanSonuc {
  kurul: number;
  sinav: string;
  hedef: number;
  simdi: { beklenen: number; olasilik: number; kotu: number };
  sonra: { beklenen: number; olasilik: number; kotu: number };
  /** sınava kadar plana ayrılabilecek süre (molalar düşülmüş) */
  butceSn: number;
  planSn: number;
  /** tüm kalan içeriğin süresi (hepsini bitirmek için) */
  hepsiSn: number;
  branslar: BransPlan[];
  adimlar: PlanAdim[];
  gunler: PlanGun[];
  /** plan bütçe yetmediği için %90'a ulaşamadı */
  yetersiz: boolean;
  /** hedef bugünkü durumla zaten güvende */
  guvende: boolean;
}

export interface PlanAyar { gunlukSaat: number }

const TR_GUN = ['Pazar', 'Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi'];
const gunStr = (d: Date) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;

/** Sınava kadar günler ve plana ayrılabilir süre. Sınav sabahı 09:30; gece 23:30 sonrası ve uyku planlanmaz;
 *  her saatin 10 dk'sı mola. */
export function gunKapasiteleri(sinav: string, gunlukSaat: number, simdi = new Date()) {
  const out: { tarih: string; ad: string; sn: number }[] = [];
  const sinavGun = new Date(`${sinav}T00:00:00`);
  for (let i = 0; i < 60; i++) {
    const g = new Date(simdi.getFullYear(), simdi.getMonth(), simdi.getDate() + i);
    if (g >= sinavGun) break;
    let sn = gunlukSaat * 3600;
    if (i === 0) {
      const gece = new Date(g.getFullYear(), g.getMonth(), g.getDate(), 23, 30).getTime();
      sn = Math.min(sn, Math.max(0, (gece - simdi.getTime()) / 1000) * 0.75);
    }
    sn *= 50 / 60;
    out.push({ tarih: gunStr(g), ad: i === 0 ? 'Bugün' : i === 1 ? 'Yarın' : TR_GUN[g.getDay()], sn: Math.round(sn) });
  }
  return out;
}

export function planHesapla(veri: PlanVeri, hiz: Partial<Record<TakipModul, Hiz>>, ayar: PlanAyar): PlanSonuc {
  const tk = takipOku();
  const il = ilerlemeOku();
  const ogr = ogrenilenler();
  const ogrSay = new Map<string, number>();
  ogr.forEach((id) => { const k = id.slice(0, id.lastIndexOf('-')); ogrSay.set(k, (ogrSay.get(k) || 0) + 1); });
  // sesli asistanı bitirmek en önemliler konusunu çalışmış sayılır
  const asistanBitti = new Set<string>();
  for (const g of getAsistanSureGruplari()) for (const d of g.dersler) if (d.tamamlandi) asistanBitti.add(`${g.brans}/${d.kod}`);
  const oran = (m: TakipModul) => hiz[m]?.oran ?? 1.1;
  const simdi = Date.now();
  const kayit = (m: TakipModul, id: string) => tk.k[`${m}:${id}`];

  // Ders durumları
  interface D { d: PlanDers; w: number; s: Durum; kal: { sesli: number; onem: number; cozucu: number }; dogru: number; cozulen: number }
  const branslar = Object.keys(veri.dagilim.branslar) as Brans[];
  const ders: Record<string, D[]> = {};
  let hepsiSn = 0;
  for (const b of branslar) {
    const L = veri.dersler.filter((d) => d.brans === b);
    const top = (f: (d: PlanDers) => number) => L.reduce((s, d) => s + f(d), 0);
    const madde = (d: PlanDers) => d.onem?.madde || 0;
    const soru = (d: PlanDers) => d.cozucu.reduce((s, c) => s + c.soru, 0);
    const sure = (d: PlanDers) => d.sesli.reduce((s, c) => s + (c.varsayilan?.sureSn || 0), 0) || d.onem?.sure || 0;
    const tm = top(madde), ts = top(soru), tu = top(sure);
    const agr = [[0.5, tm], [0.3, ts], [0.2, tu]].filter(([, t]) => t > 0);
    const ag = agr.reduce((s, [a]) => s + a, 0) || 1;
    ders[b] = L.map((d) => {
      const w = L.length && agr.length
        ? ((tm ? 0.5 * madde(d) / tm : 0) + (ts ? 0.3 * soru(d) / ts : 0) + (tu ? 0.2 * sure(d) / tu : 0)) / ag
        : 1 / Math.max(1, L.length);
      // sesli: bitirilen parça oranı; kalan süre
      let sesliBit = 0, sesliKalan = 0, son = 0;
      for (const c of d.sesli) {
        const k = kayit('sesli', c.key);
        const t = c.varsayilan?.sureSn || 0;
        if (k?.sonAt) son = Math.max(son, Date.parse(k.sonAt));
        if (bittiMi(k)) sesliBit++;
        else sesliKalan += Math.max(t * 0.15, t * oran('sesli') - (k?.durum === 'tekrar' ? 0 : k?.sn || 0));
      }
      // en önemliler
      let onemF = 0, onemKalan = 0;
      if (d.onem) {
        const k = kayit('onem', `${b}/${d.onem.kod}`);
        if (k?.sonAt) son = Math.max(son, Date.parse(k.sonAt));
        const n = ogrSay.get(d.onem.kod) || 0;
        onemF = bittiMi(k, (d.onem.madde > 0 && n >= d.onem.madde) || asistanBitti.has(`${b}/${d.onem.kod}`)) ? 1 : d.onem.madde ? Math.min(1, n / d.onem.madde) : 0;
        onemKalan = onemF >= 1 ? 0 : d.onem.sure * oran('onem') * (1 - onemF);
      }
      // soru çözücü
      let cozulen = 0, toplamSoru = 0, dogru = 0, cozKalan = 0;
      for (const c of d.cozucu) {
        const o = ozet(il[c.kod], c.soru);
        const k = kayit('cozucu', `${b}/${c.kod}`);
        if (k?.sonAt) son = Math.max(son, Date.parse(k.sonAt));
        const tamam = bittiMi(k, o.tamam);
        const coz = tamam ? c.soru : o.cozulen;
        cozulen += o.cozulen; dogru += o.d + 0.5 * o.d2; toplamSoru += c.soru;
        const sSn = (c.sure && c.soru ? c.sure / c.soru : SORU_SN) * oran('cozucu');
        cozKalan += Math.max(0, c.soru - coz) * sSn;
      }
      const s: Durum = {
        sesli: d.sesli.length ? sesliBit / d.sesli.length : 0,
        onem: onemF,
        soru: toplamSoru ? Math.min(1, cozulen / toplamSoru) : 0,
        eski: son > 0 && simdi - son > 12 * 86400_000,
      };
      const kal = { sesli: d.sesli.length && s.sesli < 1 ? sesliKalan : 0, onem: onemKalan, cozucu: cozKalan };
      hepsiSn += kal.sesli + kal.onem + kal.cozucu;
      return { d, w, s, kal, dogru, cozulen };
    });
  }

  // Kişisel düzeltme: branşta çözülen soruların ilk deneme isabeti / modelin o derslerdeki beklentisi
  const kalibre: Record<string, number> = {};
  const isabet: Record<string, number | undefined> = {};
  for (const b of branslar) {
    const L = ders[b];
    const n = L.reduce((s, x) => s + x.cozulen, 0);
    if (n < 10) { kalibre[b] = 1; continue; }
    const obs = L.reduce((s, x) => s + x.dogru, 0) / n;
    const mod = L.reduce((s, x) => s + x.cozulen * pOf(x.s, 1), 0) / n;
    isabet[b] = obs;
    const f = Math.max(0.75, Math.min(1.2, (obs + 0.03) / Math.max(0.3, mod)));
    const r = n / (n + 30);
    kalibre[b] = 1 + r * (f - 1);
  }
  const bransP = (b: Brans) => ders[b].reduce((s, x) => s + x.w * Math.min(0.92, pOf(x.s, kalibre[b])), 0);
  const dagOf = (b: Brans) => bransDag(veri.dagilim.branslar[b], bransP(b));
  const hedef = veri.dagilim.hedef;
  const J = (t: Dag) => beklenen(t) + 30 * enAz(t, hedef);
  const toplamDag = (L: Dag[]) => L.reduce(birlestir, BIR);

  const ilkDag = branslar.map(dagOf);
  const ilkTop = toplamDag(ilkDag);
  const simdiOz = { beklenen: beklenen(ilkTop), olasilik: enAz(ilkTop, hedef), kotu: yuzdelik(ilkTop, 0.2) };
  const ilkBrans = branslar.map((b, i) => ({ b, dogru: veri.dagilim.branslar[b] * bransP(b), puan: beklenen(ilkDag[i]) }));

  // Gün kapasiteleri
  const gunler = gunKapasiteleri(veri.sinav, ayar.gunlukSaat);
  const butceSn = gunler.reduce((s, g) => s + g.sn, 0);

  // Açgözlü seçim
  const adimlar: PlanAdim[] = [];
  let kalanButce = butceSn;
  let dag = ilkDag.slice();
  const HEDEF_P = 0.9;
  for (let tur = 0; tur < 400; tur++) {
    const top = toplamDag(dag);
    if (enAz(top, hedef) >= HEDEF_P || kalanButce < 300) break;
    const j0 = J(top);
    // her branş için diğerlerinin birleşimi
    const on: Dag[] = [BIR]; for (let i = 0; i < dag.length; i++) on.push(birlestir(on[i], dag[i]));
    const ar: Dag[] = [BIR]; for (let i = dag.length - 1; i >= 0; i--) ar.unshift(birlestir(dag[i], ar[0]));
    type Secim = { bi: number; x: D; tur: AdimTur; sn: number; oran: number; yeni: Dag };
    let en = null as Secim | null;
    branslar.forEach((b, bi) => {
      const dig = birlestir(on[bi], ar[bi + 1]);
      const eDig = beklenen(dig);
      // kuyruk[i] = P(diğerleri ≥ dig.min + i)
      const kuyruk = new Array(dig.p.length + 1).fill(0);
      for (let i = dig.p.length - 1; i >= 0; i--) kuyruk[i] = kuyruk[i + 1] + dig.p[i];
      const Jile = (y: Dag) => {
        let pr = 0;
        for (let i = 0; i < y.p.length; i++) {
          const k = hedef * 2 - (y.min + i) - dig.min;
          pr += y.p[i] * (k <= 0 ? 1 : k >= kuyruk.length ? 0 : kuyruk[k]);
        }
        return eDig + beklenen(y) + 30 * pr;
      };
      for (const x of ders[b]) {
        const adaylar: [AdimTur, number, Partial<Durum>][] = [];
        if (x.kal.onem > 0) adaylar.push(['onem', x.kal.onem, { onem: 1, eski: false }]);
        if (x.kal.sesli > 0) adaylar.push(['sesli', x.kal.sesli, { sesli: 1, eski: false }]);
        // soru çözmeye konu en az bir kez çalışıldıktan sonra geçilir
        if (x.kal.cozucu > 0 && (x.s.onem >= 0.6 || x.s.sesli >= 0.5)) adaylar.push(['cozucu', x.kal.cozucu, { soru: 1, eski: false }]);
        for (const [t, sn, deg] of adaylar) {
          if (sn > kalanButce + 600) continue;
          const eskiS = x.s;
          x.s = { ...eskiS, ...deg };
          const yeni = dagOf(b);
          x.s = eskiS;
          const o = (Jile(yeni) - j0) / (sn / 3600);
          if (!en || o > en.oran) en = { bi, x, tur: t, sn, oran: o, yeni };
        }
      }
    });
    const sec = en as Secim | null;
    if (!sec || sec.oran <= 0.05) break;
    const { bi, x, tur: t, sn, yeni } = sec;
    const b = branslar[bi];
    const n = veri.dagilim.branslar[b];
    const altta = n * bransP(b) < n / 2;
    const once = beklenen(dag[bi]);
    x.s = { ...x.s, ...(t === 'onem' ? { onem: 1 } : t === 'sesli' ? { sesli: 1 } : { soru: 1 }), eski: false };
    x.kal = { ...x.kal, [t]: 0 };
    dag[bi] = yeni;
    kalanButce -= sn;
    adimlar.push({
      ders: x.d, tur: t, sn: Math.round(sn),
      asama: altta ? 'baraj' : t === 'cozucu' ? 'pekistir' : 'puan',
      kazanc: beklenen(yeni) - once,
      olasilik: enAz(toplamDag(dag), hedef),
      baslik: x.d.ad,
      ac: adimAc(x.d, t),
    });
  }
  const sonTop = toplamDag(dag);
  const sonraOz = { beklenen: beklenen(sonTop), olasilik: enAz(sonTop, hedef), kotu: yuzdelik(sonTop, 0.2) };

  // Günlere yerleştir (sıra korunur; adım günün yarısından fazlası sığmıyorsa ertesi güne)
  const pg: PlanGun[] = gunler.map((g, i) => ({ gun: i, tarih: g.ad, kapasiteSn: g.sn, adimlar: [], sn: 0 }));
  let gi = 0;
  for (const a of adimlar) {
    while (gi < pg.length - 1 && pg[gi].kapasiteSn - pg[gi].sn < a.sn * 0.5) gi++;
    if (!pg.length) break;
    a.gun = gi; pg[gi].adimlar.push(a); pg[gi].sn += a.sn;
  }

  const bp: BransPlan[] = branslar.map((b, i) => {
    const n = veri.dagilim.branslar[b];
    const A = adimlar.filter((a) => a.ders.brans === b);
    return {
      brans: b, ad: bransTanim(b).ad, n,
      dogru: ilkBrans[i].dogru, puan: ilkBrans[i].puan,
      planDogru: n * bransP(b), planPuan: beklenen(dag[i]),
      calismaSn: A.filter((a) => a.tur !== 'cozucu').reduce((s, a) => s + a.sn, 0),
      soruSn: A.filter((a) => a.tur === 'cozucu').reduce((s, a) => s + a.sn, 0),
      ders: ders[b].length,
      biten: ders[b].filter((x) => bilgi(x.s) >= 0.7).length,
      isabet: isabet[b], cozulen: ders[b].reduce((s, x) => s + x.cozulen, 0),
    };
  });

  return {
    kurul: veri.kurul, sinav: veri.sinav, hedef,
    simdi: simdiOz, sonra: sonraOz,
    butceSn, planSn: adimlar.reduce((s, a) => s + a.sn, 0), hepsiSn: Math.round(hepsiSn),
    branslar: bp, adimlar, gunler: pg.filter((g) => g.adimlar.length || g.gun === 0),
    yetersiz: sonraOz.olasilik < HEDEF_P,
    guvende: simdiOz.olasilik >= HEDEF_P,
  };
}

function adimAc(d: PlanDers, t: AdimTur): () => void {
  if (t === 'sesli') {
    const il = d.sesli.find((c) => !bittiMi(takipOku().k[`sesli:${c.key}`])) || d.sesli[0];
    return () => navigateTo(pathFor('canli_ders', il.key));
  }
  if (t === 'onem' && d.onem) {
    const kod = d.onem.kod, asistan = d.onem.asistan;
    return () => onemeGit({ brans: d.brans, ders: kod, asistan: asistan ? '1' : null });
  }
  const il = ilerlemeOku();
  const c = d.cozucu.find((x) => !ozet(il[x.kod], x.soru).tamam) || d.cozucu[0];
  return () => cozucuyaGit({ brans: d.brans, ders: c?.kod, coz: '1' });
}

export const ADIM_AD: Record<AdimTur, string> = { onem: 'En önemliler', cozucu: 'Soru çöz', sesli: 'Sesli ders' };
export const ASAMA_AD: Record<Asama, string> = { baraj: 'Barajı geç', puan: 'Puan topla', pekistir: 'Soruyla pekiştir' };
