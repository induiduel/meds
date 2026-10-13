/**
 * Soru havuzu motoru, aşama 4–5: aynı soruyu anlatan hatırlamaları gruplama ve kanıta dayalı taslak.
 *
 * Çift benzerliği öğrenilmiş küçük bir lojistik modeldir (PAIR_WEIGHTS; `npm run eval:recall -- --fit` ile
 * sınama setinin geliştirme yarısında yeniden öğrenilir, diğer yarısında ölçülür). Özellikler:
 * TF-IDF kosinüs (düzeltilmiş kökler, banka IDF'i), ağırlıklı kapsama (kısa hatırlama uzun olanın içinde),
 * tıbbi terim örtüşmesi, aynı çıkmış soruya yaslanma, şık örtüşmesi, soru no aynı/farklı, ders çelişkisi.
 * Kümeleme ortalama bağlantılıdır (zincirleme yok); farklı soru numarası kesin engel değil cezadır
 * (öğrenciler numarayı ±1 yanlış hatırlıyor).
 */
import { dot, type Analysis, type RecallEngine, type Vec } from './engine.ts';
import { fold, type Letter } from './normalize.ts';

export interface RecallItem {
  key: string;
  committeeId: string;
  createdAt: string;
  /** Formdan ya da kayıttan gelen ders (öğrencinin seçtiği); boşsa sınıflayıcı. */
  discipline?: string | null;
  number: number | null;
  /** Numara öğrencinin seçtiği soru yuvasından mı (güvenilir) yoksa metinden mi çıkarıldı (±1 yanlış olabilir). */
  numberAssigned?: boolean;
  /** Öğrencinin ham metni (taslak cümle bundan kurulur). */
  text: string;
  a: Analysis;
}

export const PAIR_FEATURES = ['bias', 'cos', 'contain', 'chr', 'term', 'anchor', 'opt', 'sameNo', 'diffNo', 'dersConflict', 'short'] as const;
/**
 * Öğrenilmiş ağırlıklar: `npx tsx scripts/eval/recall-engine.mts --fit --l2 0.5 --drop opt` (geliştirme kümesi k1–k3,
 * sınıf dengeli, işaret kısıtlı lojistik; 2026-10-13). `opt` öğrenilmedi (sınama setinde şık nadir): elle 1.0 —
 * formdaki harfli şıklar aynı soruyu güçlü biçimde gösterir.
 */
export let PAIR_WEIGHTS: Record<(typeof PAIR_FEATURES)[number], number> = {
  bias: -0.99, cos: 2.22, contain: 1.77, chr: 3, term: 0.84, anchor: 5.92, opt: 1.0, sameNo: 1.9, diffNo: -0.27, dersConflict: -0.35, short: 0.19,
};
export const setPairWeights = (w: typeof PAIR_WEIGHTS) => { PAIR_WEIGHTS = w; };
/** Ortalama bağlantı eşiği (olasılık). */
export let LINK_PROB = 0.6;
export const setLinkProb = (p: number) => { LINK_PROB = p; };
/**
 * Belirsizlik payı: numarasız bir hatırlama, numaraları farklı (yani kesin ayrı) iki soruya eşiği geçip bu paydan
 * yakın olasılıkla uyuyorsa hiçbirine bağlanmaz. Canlı örnek: "geri dönüşümlü hücre hasarı" parçası #6'ya 0,94,
 * #7'ye 0,96 → #7'ye yanlış birleşmişti. Hangisi olduğu kanıtla ayrışana kadar tekil kalır.
 */
export const AMBIG_GAP = 0.1;

/** Numarasız ögenin, farklı yuvalardaki adaylar arasında kararsız olup olmadığı (yuva → en yüksek olasılık). */
function ambiguousAcrossSlots(bySlot: Map<number, number>, thr: number): boolean {
  const top = [...bySlot.values()].filter((p) => p >= thr).sort((a, b) => b - a);
  return top.length >= 2 && top[0] - top[1] < AMBIG_GAP;
}

const sumW = (stems: Set<string>, idf: (s: string) => number) => { let s = 0; for (const t of stems) s += idf(t); return s; };

/** Kısa hatırlamanın içerik kökleri uzun olanda ne ölçüde geçiyor (IDF ağırlıklı); ≥2 ortak kök gerekir. */
function containment(a: Set<string>, b: Set<string>, idf: (s: string) => number): number {
  if (!a.size || !b.size) return 0;
  const [s, l] = a.size <= b.size ? [a, b] : [b, a];
  let inter = 0, n = 0;
  for (const t of s) if (l.has(t)) { inter += idf(t); n++; }
  if (!n) return 0;
  return (inter / Math.max(1e-9, sumW(s, idf))) * Math.min(1, n / 2);
}

const GENERIC_OPT_STEM = new Set([
  'hucre', 'hasta', 'hastal', 'sendr', 'etki', 'etkis', 'test', 'testi', 'grubu', 'merke', 'tipi', 'oran', 'orani',
  'sente', 'inhib', 'aktiv', 'azali', 'artar', 'yukse', 'dusuk', 'pozit', 'negat', 'birin', 'ikinc', 'ucunc', 'basam',
]);

/** Genel soru/klinik çerçeve kökleri: tek başına iki sorunun aynı özel konuyu sorduğunu kanıtlamaz ("... gösteren test", "... bulguları"). */
const GENERIC_FRAME_STEM = new Set([
  'hasta', 'hastal', 'olgul', 'bulun', 'goste', 'ortay', 'konan', 'koyan', 'test', 'testi', 'yapan', 'neden', 'etken',
  'tedav', 'tani', 'tanis', 'bulgu', 'belir', 'klini', 'tablo', 'ozell', 'ifade', 'onerm', 'oncul', 'ilacl', 'grubu',
  'kulla', 'gorul', 'gelis', 'olust', 'veril', 'uygun', 'dogru', 'yanli', 'degil', 'bekle', 'riski', 'yukse', 'en',
]);

const GENERIC_BRIDGE_STEM = new Set([
  ...GENERIC_FRAME_STEM,
  'otodo', 'otore', 'domin', 'reses', 'mutas', 'genet', 'kalit', 'sendr', 'serum', 'dokud', 'emili', 'orani', 'duzey',
  'karac', 'bobre', 'bagir', 'mide', 'akcig', 'beyin', 'siste', 'metab', 'enzim', 'resep', 'inhib', 'antag', 'agoni',
  'polip', 'adeno', 'karsi', 'neopl', 'tumor', 'lezyo', 'infek', 'infla', 'bakte', 'virus', 'oral', 'paren', 'amino',
  'ototo', 'kohor', 'kesit',
]);

/**
 * Bankada olmayan (yeni) sorularda, yalnız kavram/hastalık/ilaç adını içeren kısa cevap/konu hatırlaması ile
 * o kavramın tanımını/mekanizmasını anlatan soru kökü arasında tıbbi sözlük/ders notu üzerinden köprü kurar.
 */
function conceptBridgeScore(a: Analysis, b: Analysis, eng: RecallEngine): number {
  const checkDir = (shortA: Analysis, longB: Analysis): number => {
    if (shortA.role === 'options' || longB.role === 'options' || longB.role === 'claim') return 0;
    if (shortA.negative >= 0.5 || longB.negative >= 0.5 || shortA.isRoman || longB.isRoman) return 0;
    const sa = [...new Set(shortA.stems.filter((s) => !GENERIC_BRIDGE_STEM.has(s) && !/^\d+$/.test(s)))];
    if (sa.length < 1 || sa.length > 2) return 0;
    const sb = new Set((longB.stemStems.length ? longB.stemStems : longB.stems).filter((s) => !GENERIC_BRIDGE_STEM.has(s) && !/^\d+$/.test(s)));
    if (sb.size < 2) return 0;
    let best = 0;
    for (const h of sa) {
      if (sb.has(h) || eng.idf(h) < 4.5) continue;
      const defs = eng.conceptDefs(h);
      if (!defs) continue;
      let hits = 0, idfSum = 0;
      for (const t of sb) {
        if (eng.idf(t) >= 3.5 && defs.has(t)) { hits++; idfSum += eng.idf(t); }
      }
      if ((hits >= 2 && idfSum >= 9.0) || (hits >= 3 && idfSum >= 11.0)) {
        best = Math.max(best, Math.min(0.54, 0.32 + 0.02 * idfSum));
      }
    }
    return best;
  };
  return Math.max(checkDir(a, b), checkDir(b, a));
}

function optionOverlap(a: Analysis, b: Analysis): number {
  if (!a.options.length || !b.options.length) return 0;
  const toks = (s: string) =>
    fold(s)
      .split(' ')
      .filter((x) => x.length >= 4 && !GENERIC_OPT_STEM.has(x.slice(0, 5)))
      .map((x) => x.slice(0, 5))
      .filter((x) => !/^(yalni|hepsi|hicbi|birli|dogru|yanli)$/.test(x));
  const ka = a.options.map((o) => toks(o.metin)).filter((x) => x.length > 0);
  const kb = b.options.map((o) => toks(o.metin)).filter((x) => x.length > 0);
  if (!ka.length || !kb.length) return 0;
  let hit = 0;
  for (const x of ka) if (kb.some((y) => y.some((t) => x.includes(t)))) hit++;
  // İki tam şık listesi (≥3 şık) yalnız tek bir ortak çeldirici paylaşıyorsa bu aynı soru kanıtı değildir
  if (ka.length >= 3 && kb.length >= 3 && hit < 2) return 0;
  return hit / Math.min(ka.length, kb.length);
}

/**
 * Düzeltilmiş içerik sözcüklerinin 4'lü harf dizileri (kalan yazım farklarına dayanıklı).
 * Her sözcük kendi içinde normalize edilir ki 13 harfli tek bir ortak sözcük ("aminoglikozid") kısa farklı sözcükleri boğmasın.
 */
const grams = new WeakMap<Analysis, Map<string, number>>();
function charGrams(a: Analysis): Map<string, number> {
  const cached = grams.get(a);
  if (cached) return cached;
  const g = new Map<string, number>();
  for (const w of a.words) {
    const t = `_${w}_`;
    const len = Math.max(1, t.length - 3);
    const wNorm = 1 / Math.sqrt(len);
    for (let i = 0; i + 4 <= t.length; i++) {
      const k = t.slice(i, i + 4);
      g.set(k, (g.get(k) || 0) + wNorm);
    }
  }
  let n = 0;
  for (const v of g.values()) n += v * v;
  n = Math.sqrt(n) || 1;
  for (const [k, v] of g) g.set(k, v / n);
  grams.set(a, g);
  return g;
}

export function pairFeatures(x: RecallItem, y: RecallItem, eng: RecallEngine, cache?: WeakMap<Analysis, Set<string>>) {
  const a = x.a, b = y.a;
  const sa = cache?.get(a) || new Set(a.stems);
  const sb = cache?.get(b) || new Set(b.stems);
  let nShared = 0;
  for (const t of sa) if (sb.has(t)) nShared++;
  const minSize = Math.min(sa.size, sb.size);

  let cos = dot(a.vec, b.vec);
  let contain = containment(sa, sb, eng.idf);
  let term = 0;
  if (a.terms.length && b.terms.length) {
    const tb = new Set(b.terms);
    const inter = a.terms.filter((t) => tb.has(t)).length;
    // Dice: tek ortak terim, terimleri çok olan iki hatırlamayı tam puanla eşlemesin (aynı ilacın farklı soruları)
    term = (2 * inter) / (a.terms.length + b.terms.length);
  }
  // Aynı çıkmış soruya güçlü yaslanma (bankadaki sorunun kök + şıkları üzerinden kök ↔ şık köprüsü kurar)
  let anchor = 0;
  const ta = a.bank.slice(0, 2), tb2 = b.bank.slice(0, 2);
  for (const p of ta) for (const q of tb2) {
    if (p.id === q.id && p.score >= 0.35 && q.score >= 0.35) anchor = Math.max(anchor, Math.min(p.score, q.score));
  }
  if (anchor < 0.4 && nShared === 0) {
    anchor = Math.max(anchor, conceptBridgeScore(a, b, eng));
  }
  const opt = optionOverlap(a, b);
  let chr = dot(charGrams(a), charGrams(b));
  // Odak yüklem ayrımı: yaygın/orta sıklıktaki tek bir konu kökünü (IDF < 5.2) paylaşıp her iki tarafta ≥2 farklı
  // spesifik kök taşıyan iki ayrı soru kökü ("Kolera toksini mekanizması" vs "Kolera kliniği") yanlış birleşmesin
  if (nShared === 1 && minSize >= 3 && anchor === 0 && opt === 0) {
    let sharedIdf = 0, diffA = 0, diffB = 0;
    for (const t of sa) {
      if (sb.has(t)) sharedIdf = eng.idf(t);
      else if (!GENERIC_FRAME_STEM.has(t) && !/^\d+$/.test(t)) diffA++;
    }
    for (const t of sb) if (!sa.has(t) && !GENERIC_FRAME_STEM.has(t) && !/^\d+$/.test(t)) diffB++;
    if (sharedIdf < 5.2 && diffA >= 2 && diffB >= 2) {
      cos *= 0.65;
      contain *= 0.55;
      chr *= 0.7;
    }
  }
  // Aynı numara ancak içerik de örtüşüyorsa kanıttır (farklı kaynaklardan aynı numaralı iki ayrı soru birleşmesin)
  const sameNo = x.number && y.number && x.number === y.number && (chr >= 0.2 || cos >= 0.15) ? 1 : 0;
  const diffNo = x.number && y.number && x.number !== y.number && !(x.numberAssigned && y.numberAssigned) ? 1 : 0;
  const da = x.discipline || (a.ders[0] && a.ders[0].p >= 0.75 ? a.ders[0].name : '');
  const db = y.discipline || (b.ders[0] && b.ders[0].p >= 0.75 ? b.ders[0].name : '');
  const dersConflict = da && db && da !== db ? 1 : 0;
  // Kısa parça desteği: tek kök tam örtüştüğünde veya 2 köklü parçanın her iki kökü de karşıda bulunduğunda
  const short = (minSize === 1 && contain >= 0.45) || (minSize === 2 && nShared >= 2 && contain >= 0.45) ? 1 : 0;
  return { bias: 1, cos, contain, chr, term, anchor, opt, sameNo, diffNo, dersConflict, short };
}

export function pairProb(f: ReturnType<typeof pairFeatures>): number {
  let z = 0;
  for (const k of PAIR_FEATURES) z += PAIR_WEIGHTS[k] * (f as any)[k];
  return 1 / (1 + Math.exp(-z));
}

let sliceStart = Date.now();
async function yieldIfBusy() {
  if (Date.now() - sliceStart < 8) return;
  await new Promise((r) => setImmediate(r));
  sliceStart = Date.now();
}

/** Ortalama bağlantılı kümeleme (kurul içinde). Tekil kalanlar da döner (members.length === 1). */
/** Yöneticinin "farklı soru" diye ayırdığı çiftler (anahtar çifti, sıralı "a|b"); bu çiftler asla aynı kümeye girmez. */
export const pairKey = (a: string, b: string) => (a < b ? `${a}|${b}` : `${b}|${a}`);

const BROAD_TOPIC_STEM = new Set(['tumor', 'sendr', 'biyop', 'lezyo', 'turu', 'tipi']);

export async function clusterRecall(items: RecallItem[], eng: RecallEngine, opts: { linkProb?: number; cannotLink?: Set<string> } = {}) {
  const thr = opts.linkProb ?? LINK_PROB;
  sliceStart = Date.now();
  const byCommittee = new Map<string, RecallItem[]>();
  for (const it of items) {
    if (it.a.isNoise) continue;
    (byCommittee.get(it.committeeId) || byCommittee.set(it.committeeId, []).get(it.committeeId)!).push(it);
  }
  const cache = new WeakMap<Analysis, Set<string>>();
  for (const it of items) cache.set(it.a, new Set(it.a.stems));
  const out: { members: RecallItem[]; cohesion: number }[] = [];
  for (const group of byCommittee.values()) {
    const n = group.length;
    // Aday çiftler ters dizinle: ortak kök, terim ya da ilk 2 çıkmış soru komşusu olmayan çift hesaplanmaz.
    // Hesaplanmayan çift = "ortak hiçbir şeyi yok" taban olasılığı (0 değil; 0 ortalama bağlantıyı yapay biçimde düşürür)
    const base = Math.fround(1 / (1 + Math.exp(-PAIR_WEIGHTS.bias)));
    const sim: Float32Array[] = Array.from({ length: n }, () => new Float32Array(n).fill(base));
    const rawSim: Float32Array[] = Array.from({ length: n }, () => new Float32Array(n).fill(base));
    const post = new Map<string, number[]>();
    const keysOf = (it: RecallItem) => new Set([
      ...it.a.stems.map((s) => `s:${s}`),
      ...it.a.terms.map((t) => `t:${t}`),
      ...it.a.bank.slice(0, 2).filter((b) => b.score >= 0.4).map((b) => `b:${b.id}`),
    ]);
    const keySets = group.map(keysOf);
    keySets.forEach((ks, i) => { for (const k of ks) (post.get(k) || post.set(k, []).get(k)!).push(i); });
    // Kısa kavram/cevap uyduları için kavram tanım köklerini de aday aramasına ekle (ters dizini şişirmeden)
    const queryKeySets = group.map((it, i) => {
      const qks = new Set(keySets[i]);
      if (it.a.role !== 'options' && it.a.stems.length <= 3 && it.a.negative < 0.5 && !it.a.isRoman) {
        for (const h of it.a.stems) {
          if (eng.idf(h) < 4.5 || GENERIC_BRIDGE_STEM.has(h)) continue;
          const defs = eng.conceptDefs(h);
          if (defs) for (const d of defs) if (post.has(`s:${d}`)) qks.add(`s:${d}`);
        }
      }
      return qks;
    });
    const maxDf = Math.max(20, Math.ceil(n * 0.2));
    const seen = new Uint8Array(n);
    for (let i = 0; i < n; i++) {
      seen.fill(0);
      for (const k of queryKeySets[i]) {
        const list = post.get(k)!;
        if (!list || (list.length > maxDf && !k.startsWith('b:'))) continue;
        for (const j of list) {
          if (j === i || seen[j]) continue;
          seen[j] = 1;
          if (rawSim[i][j] !== base) continue;
          const p = pairProb(pairFeatures(group[i], group[j], eng, cache));
          sim[i][j] = p; sim[j][i] = p;
          rawSim[i][j] = p; rawSim[j][i] = p;
        }
      }
      await yieldIfBusy();
    }
    // Yuva numaraları farklı olanlar veya metinden çıkarılan soru numaraları ≥2 farkla çelişenler (±1 hatırlama hatası hariç) asla birleşmez
    const slot = group.map((g) => (g.numberAssigned && g.number ? g.number : 0));
    const qno = group.map((g) => g.number || 0);
    for (let i = 0; i < n; i++) for (let j = 0; j < i; j++) {
      if ((slot[i] && slot[j] && slot[i] !== slot[j]) || (qno[i] && qno[j] && Math.abs(qno[i] - qno[j]) >= 2)) {
        sim[i][j] = -1; sim[j][i] = -1;
        rawSim[i][j] = -1; rawSim[j][i] = -1;
      }
    }
    // Yönetici ayırması: kesin engel (yuva çelişkisi gibi birleşmeyle de yayılır)
    if (opts.cannotLink?.size) {
      for (let i = 0; i < n; i++) for (let j = 0; j < i; j++) if (opts.cannotLink.has(pairKey(group[i].key, group[j].key))) {
        sim[i][j] = -1; sim[j][i] = -1;
        rawSim[i][j] = -1; rawSim[j][i] = -1;
      }
    }
    // Numarasız öge iki ayrı numaralı soruya neredeyse eşit uyuyorsa numaralı sorulara bağlanmaz (bkz. AMBIG_GAP)
    for (let i = 0; i < n; i++) {
      if (slot[i]) continue;
      const bySlot = new Map<number, number>();
      for (let j = 0; j < n; j++) if (slot[j] && sim[i][j] > (bySlot.get(slot[j]) ?? -1)) bySlot.set(slot[j], sim[i][j]);
      if (!ambiguousAcrossSlots(bySlot, thr)) continue;
      for (let j = 0; j < n; j++) if (slot[j] && sim[i][j] > base) { sim[i][j] = base; sim[j][i] = base; }
    }
    const isCoreItem = (idx: number) => {
      const r = group[idx].a.role;
      if (r !== 'stem' && r !== 'mixed') return false;
      const specStems = [...new Set(group[idx].a.stemStems.filter((s) => !/^\d+$/.test(s) && !GENERIC_FRAME_STEM.has(s)))];
      if (specStems.length >= 3) return true;
      if (specStems.length === 2 && !specStems.some((s) => BROAD_TOPIC_STEM.has(s))) return true;
      return false;
    };
    const qnoCompatible = (ma: number[], mb: number[]) => {
      for (const i of ma) if (qno[i]) for (const j of mb) if (qno[j] && Math.abs(qno[i] - qno[j]) >= 2) return false;
      return true;
    };
    const optCompatible = (ma: number[], mb: number[]) => {
      for (const i of ma) if (group[i].a.options.length >= 3) {
        for (const j of mb) if (group[j].a.options.length >= 3 && optionOverlap(group[i].a, group[j].a) === 0) return false;
      }
      return true;
    };
    // İki küme arasındaki bağlantı puanı:
    // - Her iki kümede de çekirdek soru kökü varsa: uydu (şık/iddia) üyelerinin kök-kök benzerliğini seyreltmesini önlemek için
    //   çekirdek üyeler arası ortalama (coreAvg), en güçlü çekirdek köprüsü (coreMax) ve tüm çiftler ortalaması (allAvg) birlikte değerlendirilir.
    const groupSim = (aIdx: number, bIdx: number, ma: number[], mb: number[]): number => {
      if (slot[aIdx] && slot[bIdx] && slot[aIdx] !== slot[bIdx]) return -1;
      if (!qnoCompatible(ma, mb) || !optCompatible(ma, mb)) return -1;
      let allSum = 0;
      for (const i of ma) for (const j of mb) {
        if (sim[i][j] < 0) return -1;
        allSum += rawSim[i][j];
      }
      const allAvg = allSum / (ma.length * mb.length);
      const ca = ma.filter(isCoreItem), cb = mb.filter(isCoreItem);
      if (ca.length > 0 && cb.length > 0) {
        let coreSum = 0, coreMax = -1, coreMin = 2;
        for (const i of ca) for (const j of cb) {
          const r = rawSim[i][j];
          coreSum += r;
          if (r > coreMax) coreMax = r;
          if (r < coreMin) coreMin = r;
        }
        const coreAvg = coreSum / (ca.length * cb.length);
        if (coreAvg < thr * 0.78 && coreMax < thr * 0.92) return -1;
        return Math.max(allAvg, coreAvg, coreMin >= 0.40 && coreAvg >= thr * 0.65 ? coreMax * 0.85 : 0);
      }
      return allAvg;
    };

    const alive = new Uint8Array(n).fill(1);
    const members = group.map((_, i) => [i]);
    const internal = new Float64Array(n);
    const best = new Float32Array(n).fill(-1);
    const bestJ = new Int32Array(n).fill(-1);
    const rescan = (i: number) => {
      best[i] = -1; bestJ[i] = -1;
      for (let j = 0; j < n; j++) if (j !== i && alive[j] && sim[i][j] > best[i]) { best[i] = sim[i][j]; bestJ[i] = j; }
    };
    for (let i = 0; i < n; i++) rescan(i);
    for (;;) {
      let ba = -1;
      for (let i = 0; i < n; i++) if (alive[i] && bestJ[i] >= 0 && (ba < 0 || best[i] > best[ba])) ba = i;
      if (ba < 0 || best[ba] < thr) break;
      const bb = bestJ[ba];
      if (!qnoCompatible(members[ba], members[bb]) || !optCompatible(members[ba], members[bb])) {
        sim[ba][bb] = -1; sim[bb][ba] = -1;
        rescan(ba);
        if (bestJ[bb] === ba) rescan(bb);
        continue;
      }
      const v = best[ba];
      const na = members[ba].length, nb = members[bb].length;
      slot[ba] = slot[ba] || slot[bb];
      const merged = members[ba].concat(members[bb]);
      internal[ba] += internal[bb] + v * na * nb;
      members[ba] = merged;
      alive[bb] = 0;
      for (let c = 0; c < n; c++) {
        if (!alive[c] || c === ba) continue;
        const s = sim[ba][c] < 0 || sim[bb][c] < 0 ? -1 : groupSim(ba, c, merged, members[c]);
        sim[ba][c] = s; sim[c][ba] = s;
      }
      rescan(ba);
      for (let c = 0; c < n; c++) {
        if (!alive[c] || c === ba) continue;
        if (bestJ[c] === ba || bestJ[c] === bb) rescan(c);
        else if (sim[c][ba] > best[c]) { best[c] = sim[c][ba]; bestJ[c] = ba; }
      }
      await yieldIfBusy();
    }

    // Aşama 2 (Köprü-Uydu Bağlama): Şık listesi ('options'), cevap iddiası ('claim') veya tek kavram içeren uydu kümeleri,
    // kurulda en güçlü köprü bağlantısına sahip çekirdek kümeye (tartışmasız ise) eklenir.
    for (let pass = 0; pass < 2; pass++) {
      let changed = false;
      for (let s = 0; s < n; s++) {
        if (!alive[s] || members[s].some(isCoreItem)) continue;
        let bestC = -1, bestP = -1, secondP = -1;
        for (let c = 0; c < n; c++) {
          if (!alive[c] || c === s || !members[c].some(isCoreItem)) continue;
          if (slot[s] && slot[c] && slot[s] !== slot[c]) continue;
          if (!qnoCompatible(members[s], members[c]) || !optCompatible(members[s], members[c])) continue;
          let blocked = false, maxPair = -1;
          for (const si of members[s]) {
            for (const ci of members[c]) {
              if (rawSim[si][ci] < 0) { blocked = true; break; }
              if (rawSim[si][ci] > maxPair) maxPair = rawSim[si][ci];
            }
            if (blocked) break;
          }
          if (blocked) continue;
          if (maxPair > bestP) { secondP = bestP; bestP = maxPair; bestC = c; }
          else if (maxPair > secondP) { secondP = maxPair; }
        }
        const gapOk = bestP - Math.max(base, secondP) >= AMBIG_GAP || (bestP >= 0.85 && bestP - Math.max(base, secondP) >= 0.06);
        if (bestC >= 0 && bestP >= thr && gapOk) {
          const na = members[bestC].length, nb = members[s].length;
          slot[bestC] = slot[bestC] || slot[s];
          internal[bestC] += internal[s] + bestP * na * nb;
          members[bestC] = members[bestC].concat(members[s]);
          alive[s] = 0;
          changed = true;
        }
      }
      if (!changed) break;
    }

    // Romen rakamlı öncül/şık uydusu ("24 I ve III B"): soru numarası bilinen bir Romen çekirdek kümesiyle eşleşiyorsa bağlanır.
    for (let s = 0; s < n; s++) {
      if (!alive[s] || members[s].some(isCoreItem)) continue;
      if (!members[s].every((i) => group[i].a.stems.length === 0 && group[i].a.isRoman)) continue;
      const sQno = members[s].map((i) => qno[i]).find((q) => q > 0) || 0;
      if (!sQno) continue;
      const romanCores: number[] = [];
      for (let c = 0; c < n; c++) {
        if (!alive[c] || c === s || !members[c].some(isCoreItem)) continue;
        if (!members[c].some((i) => group[i].a.isRoman && qno[i] === sQno)) continue;
        if (slot[s] && slot[c] && slot[s] !== slot[c]) continue;
        if (!qnoCompatible(members[s], members[c])) continue;
        romanCores.push(c);
      }
      if (romanCores.length === 1) {
        const c = romanCores[0];
        const na = members[c].length, nb = members[s].length;
        slot[c] = slot[c] || slot[s];
        internal[c] += internal[s] + thr * na * nb;
        members[c] = members[c].concat(members[s]);
        alive[s] = 0;
      }
    }

    for (let i = 0; i < n; i++) {
      if (!alive[i]) continue;
      const m = members[i].length;
      out.push({ members: members[i].map((k) => group[k]), cohesion: m > 1 ? internal[i] / ((m * (m - 1)) / 2) : 1 });
    }
  }
  return out;
}

// ---------------------------------------------------------------- taslak

export interface RecallDraft {
  /** Okunur, temizlenmiş, en temsilî hatırlama (medoid) — öğrenci sözcükleri, sohbetsiz. */
  stem: string;
  /** Medoid hatırlamanın anahtarı. */
  medoidKey: string;
  discipline: { name: string; p: number } | null;
  konu: string | null;
  terms: string[];
  number: number | null;
  negativeLikely: boolean;
  answerVotes: Record<string, number>;
  /** Harfi bilinmeyen cevap iddiaları ("cevap nistatin olmalı") metinle oylanır. */
  answerTextVotes: { text: string; votes: number }[];
  /** Aynı kuruldaki en benzer doğrulanmış çıkmış soru (öğrenciler eski bir soruyu hatırlıyor olabilir). */
  bankMatch: { id: string; score: number; margin: number; support: number; stem: string; options: { key: string; text: string }[]; correctAnswer: string } | null;
}

/** Çıkmış soru önerisi kuralı (scripts/eval/recall-engine.mts --dump-bank ile iki senaryoda ayarlanır). */
export let BANK_MATCH = (s1: number, margin: number, support: number) => s1 >= 0.4 && margin >= 0.12 && support >= 0.3;
export const setBankMatch = (f: typeof BANK_MATCH) => { BANK_MATCH = f; };

/** Kümenin soru kökünü öğrenci parçalarından sentezler: şık/iddia uydularını eler, en kapsayıcı soru kökünü seçer ve soru kalıbını tamamlar. */
function synthesizeClusterStem(members: RecallItem[], eng: RecallEngine, negativeLikely: boolean): { medoid: RecallItem; stem: string } {
  const corePool = members.filter((m) => (m.a.role === 'stem' || m.a.role === 'mixed') && m.a.stemStems.length >= 2);
  const nonOptPool = corePool.length ? corePool : members.filter((m) => m.a.role !== 'options' && m.a.stems.length >= 1);
  const pool = nonOptPool.length ? nonOptPool : members;

  // Kök konsensüsü yalnız adayların soru kökü köklerinden (stemStems) hesaplanır ki şık dökümleri medoid seçimini saptırmasın
  const stemCount = new Map<string, number>();
  for (const m of pool) {
    const sts = m.a.stemStems.length ? m.a.stemStems : m.a.stems;
    for (const st of new Set(sts)) stemCount.set(st, (stemCount.get(st) || 0) + 1);
  }
  const common = [...stemCount].filter(([, c]) => c >= 2 || pool.length === 1);
  const commonW = common.reduce((t, [st]) => t + eng.idf(st), 0) || 1;
  const hasLongerStem = pool.some((m) => (m.a.stemWords.length || m.a.words.length) >= 4);

  let medoid = pool[0], bestScore = -1e9;
  for (const m of pool) {
    const sts = m.a.stemStems.length ? m.a.stemStems : m.a.stems;
    const wLen = m.a.stemWords.length || m.a.words.length;
    const own = new Set(sts);
    let cov = 0, extra = 0;
    for (const [st] of common) if (own.has(st)) cov += eng.idf(st);
    for (const st of own) if ((stemCount.get(st) || 0) < 2) extra += eng.idf(st);
    const cleaned = eng.cleanSentence(m.text);
    const hasInterrog = /\b(hangisi|hangisidir|hangileri|hangisinde|hangi|nedir|değildir|yanlıştır|beklenmez|almaz)\b/i.test(cleaned);
    let score =
      cov / commonW +
      0.03 * Math.min(8, extra) +
      (hasInterrog ? 0.22 : 0) +
      0.15 * Math.min(1, wLen / 7) -
      (wLen > 32 ? 0.15 : 0) -
      (hasLongerStem && wLen <= 2 ? 0.35 : 0);
    if (score > bestScore) { bestScore = score; medoid = m; }
  }

  let stem = eng.cleanSentence(medoid.text) || medoid.a.clean;
  if (medoid.a.role !== 'options' && stem) {
    const hasRoman = members.filter((m) => /\bI\b.*\bII\b|\b(?:dörtlü|üçlü|dortlu|uclu)\s+(?:önerme|öncül|onerme|oncul)\b/i.test(m.text)).length >= 1 &&
      /\bI\b|\böncül|\bönerme|\bifadeler/i.test(medoid.text);
    if (hasRoman && !/\bhangileri\b/i.test(stem)) {
      stem = `${stem.replace(/[?.!,\s]+$/, '')} ile ilgili aşağıdaki ifadelerden hangileri doğrudur?`;
    } else if (negativeLikely && !/\b(değildir|yanlıştır|beklenmez|almaz|yapmaz|olmaz|bulunmaz|görülmez|içermez)\b/i.test(stem)) {
      stem = `${stem.replace(/[?.!,\s]+$/, '')} ile ilgili aşağıdakilerden hangisi yanlıştır?`;
    } else if (!/\b(hangisi|hangisidir|hangileri|hangisinde|hangi|nedir|değildir|yanlıştır|beklenmez|almaz|verilir|yapılmalıdır)\b/i.test(stem) && !/\?$/.test(stem)) {
      stem = `${stem.replace(/[?.!,\s]+$/, '')} aşağıdakilerden hangisidir?`;
    }
    if (/^Hangisi\s+/u.test(stem)) {
      stem = `Aşağıdakilerden h${stem.slice(1)}`;
    }
  }
  return { medoid, stem };
}

/** Kümenin taslağı: medoid metin + oylar + ortak çıkmış soru adayı. Yapay zekâ yok; kanıt dışı bilgi eklemez. */
export function draftCluster(members: RecallItem[], eng: RecallEngine): RecallDraft {
  const negativeLikely = members.filter((m) => m.a.negative >= 0.5).length >= Math.max(1, members.length * 0.3);
  const { medoid, stem } = synthesizeClusterStem(members, eng, negativeLikely);
  const dersVote = new Map<string, number>();
  for (const m of members) {
    if (m.discipline) dersVote.set(m.discipline, (dersVote.get(m.discipline) || 0) + 1);
    else for (const d of m.a.ders.slice(0, 2)) dersVote.set(d.name, (dersVote.get(d.name) || 0) + d.p);
  }
  const dTot = [...dersVote.values()].reduce((a, b) => a + b, 0) || 1;
  const dTop = [...dersVote].sort((a, b) => b[1] - a[1])[0];
  const konuVote = new Map<string, number>();
  for (const m of members) if (m.a.konu && (!dTop || m.a.ders[0]?.name === dTop[0])) konuVote.set(m.a.konu.name, (konuVote.get(m.a.konu.name) || 0) + m.a.konu.p);
  const termVote = new Map<string, number>();
  for (const m of members) for (const t of new Set(m.a.terms)) termVote.set(t, (termVote.get(t) || 0) + 1);
  const numVote = new Map<number, number>();
  for (const m of members) if (m.number) numVote.set(m.number, (numVote.get(m.number) || 0) + 1);
  const answerVotes: Record<string, number> = {};
  for (const m of members) if (m.a.claimedLetter) answerVotes[m.a.claimedLetter] = (answerVotes[m.a.claimedLetter] || 0) + 1;
  const textVotes: { text: string; votes: number }[] = [];
  for (const m of members) {
    const t = m.a.claimedText;
    if (!t) continue;
    const g = textVotes.find((x) => fold(x.text).slice(0, 6) === fold(t).slice(0, 6));
    if (g) g.votes++; else textVotes.push({ text: t, votes: 1 });
  }
  // Çıkmış soru adayı: küme merkezinin (üye vektörleri toplamı) bankadaki en yakın sorusu. Öneri ancak birinci aday
  // ikinciden belirgin ayrışıyorsa yapılır (aynı konudaki komşu sorular arasında kararsızlık = eşleşme yok).
  const centroid: Vec = new Map();
  for (const m of members) for (const [k, v] of m.a.vec) centroid.set(k, (centroid.get(k) || 0) + v);
  let nrm = 0; for (const v of centroid.values()) nrm += v * v; nrm = Math.sqrt(nrm) || 1;
  for (const [k, v] of centroid) centroid.set(k, v / nrm);
  const hits = eng.searchBank(centroid, members[0].committeeId, 3);
  let bankMatch: RecallDraft['bankMatch'] = null;
  if (hits[0]) {
    const s1 = hits[0].score, s2 = hits[1]?.score || 0;
    const support = members.filter((m) => m.a.bank.slice(0, 3).some((b) => b.id === hits[0].id)).length / members.length;
    if (BANK_MATCH(s1, s1 - s2, support)) {
      const d = eng.bankDoc(hits[0].id);
      if (d) bankMatch = { id: d.id, score: s1, margin: Math.round((s1 - s2) * 1000) / 1000, support: Math.round(support * 100) / 100, stem: d.stem, options: d.options, correctAnswer: d.correctAnswer };
    }
  }
  // Metinle yazılan cevap iddiaları ("sefepim dedim") kümedeki harfli şıklardan biriyle tekil eşleşiyorsa harf oyuna da yansıtılır
  const knownLettered: { key: string; folded: string }[] = [];
  for (const m of members) for (const o of m.a.options) if (o.harf && o.metin) knownLettered.push({ key: o.harf, folded: fold(o.metin) });
  if (bankMatch?.options) for (const o of bankMatch.options) if (/^[A-E]$/.test(o.key) && o.text) knownLettered.push({ key: o.key, folded: fold(o.text) });
  if (knownLettered.length && textVotes.length) {
    for (const tv of textVotes) {
      const tf = fold(tv.text).trim();
      if (tf.length < 4) continue;
      const matchedKeys = new Set<string>();
      for (const kl of knownLettered) if (kl.folded.includes(tf) || tf.includes(kl.folded)) matchedKeys.add(kl.key);
      if (matchedKeys.size === 1) {
        const L = [...matchedKeys][0];
        answerVotes[L] = (answerVotes[L] || 0) + tv.votes;
      }
    }
  }
  return {
    stem,
    medoidKey: medoid.key,
    discipline: dTop ? { name: dTop[0], p: Math.round((dTop[1] / dTot) * 100) / 100 } : null,
    konu: [...konuVote].sort((a, b) => b[1] - a[1])[0]?.[0] || null,
    terms: [...termVote].sort((a, b) => b[1] - a[1]).map(([t]) => t).slice(0, 8),
    number: [...numVote].sort((a, b) => b[1] - a[1])[0]?.[0] ?? null,
    negativeLikely,
    answerVotes,
    answerTextVotes: textVotes.sort((a, b) => b.votes - a.votes),
    bankMatch,
  };
}

export type { Letter };

/**
 * Artımlı kümeleme: yeni hatırlamayı mevcut kümelere ortalama bağlantıyla atar (kümenin en çok `cap` üyesiyle;
 * en yenileri). En iyi küme eşiği geçmezse null → kendi tekil kümesini açar. Maliyet: küme × cap, havuz boyundan bağımsız
 * değil ama O(n) (toplu hesap O(n²)). Yuva numarası çelişen kümeye atanmaz.
 */
export function assignToGroup<G extends { members: RecallItem[] }>(item: RecallItem, groups: Iterable<G>, eng: RecallEngine, opts: { linkProb?: number; cap?: number; cannotLink?: Set<string> } = {}): { group: G; prob: number } | null {
  const thr = opts.linkProb ?? LINK_PROB;
  const cap = opts.cap ?? 12;
  if (item.a.isNoise) return null;
  let best: { group: G; prob: number } | null = null;
  const bySlot = new Map<number, number>();
  for (const g of groups) {
    const ms = g.members;
    if (!ms.length || ms[0].committeeId !== item.committeeId) continue;
    if (item.numberAssigned && item.number && ms.some((m) => m.numberAssigned && m.number && m.number !== item.number)) continue;
    if (item.number && ms.some((m) => m.number && Math.abs(m.number - item.number!) >= 2)) continue;
    if (opts.cannotLink?.size && ms.some((m) => opts.cannotLink!.has(pairKey(item.key, m.key)))) continue;
    const sample = ms.length > cap ? ms.slice(-cap) : ms;
    // Ucuz ön eleme: hiçbir üyeyle ortak kök/terim yoksa geç
    const st = new Set(item.a.stems);
    if (!sample.some((m) => m.a.stems.some((s) => st.has(s)) || m.a.terms.some((t) => item.a.terms.includes(t)))) continue;
    let sum = 0;
    for (const m of sample) sum += pairProb(pairFeatures(item, m, eng));
    const p = sum / sample.length;
    const gs = ms.find((m) => m.numberAssigned && m.number)?.number;
    if (gs) bySlot.set(gs, Math.max(bySlot.get(gs) ?? -1, p));
    if (p >= thr && (!best || p > best.prob)) best = { group: g, prob: p };
  }
  // Numarasız öge iki ayrı numaralı soruya neredeyse eşit uyuyorsa hiçbirine atanmaz
  if (best && !(item.numberAssigned && item.number) && ambiguousAcrossSlots(bySlot, thr)) return null;
  return best;
}
