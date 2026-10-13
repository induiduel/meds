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

function optionOverlap(a: Analysis, b: Analysis): number {
  if (!a.options.length || !b.options.length) return 0;
  const ka = a.options.map((o) => fold(o.metin).split(' ').filter((x) => x.length >= 4).map((x) => x.slice(0, 5)));
  const kb = b.options.map((o) => fold(o.metin).split(' ').filter((x) => x.length >= 4).map((x) => x.slice(0, 5)));
  let hit = 0;
  for (const x of ka) if (x.length && kb.some((y) => y.some((t) => x.includes(t)))) hit++;
  return hit / Math.min(ka.length, kb.length);
}

/** Düzeltilmiş içerik sözcüklerinin 4'lü harf dizileri (kalan yazım farklarına dayanıklı). */
const grams = new WeakMap<Analysis, Map<string, number>>();
function charGrams(a: Analysis): Map<string, number> {
  let g = grams.get(a);
  if (g) return g;
  g = new Map();
  for (const w of a.words) {
    const t = `_${w}_`;
    for (let i = 0; i + 4 <= t.length; i++) { const k = t.slice(i, i + 4); g.set(k, (g.get(k) || 0) + 1); }
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
  const cos = dot(a.vec, b.vec);
  const contain = containment(sa, sb, eng.idf);
  let term = 0;
  if (a.terms.length && b.terms.length) {
    const tb = new Set(b.terms);
    const inter = a.terms.filter((t) => tb.has(t)).length;
    // Dice: tek ortak terim, terimleri çok olan iki hatırlamayı tam puanla eşlemesin (aynı ilacın farklı soruları)
    term = (2 * inter) / (a.terms.length + b.terms.length);
  }
  // Aynı çıkmış soruya güçlü yaslanma: iki hatırlamanın ilk 2 banka komşusu kesişiyor
  let anchor = 0;
  const ta = a.bank.slice(0, 2), tb2 = b.bank.slice(0, 2);
  for (const p of ta) for (const q of tb2) if (p.id === q.id) anchor = Math.max(anchor, Math.min(p.score, q.score));
  const opt = optionOverlap(a, b);
  const chr = dot(charGrams(a), charGrams(b));
  // Aynı numara ancak içerik de örtüşüyorsa kanıttır (farklı kaynaklardan aynı numaralı iki ayrı soru birleşmesin)
  const sameNo = x.number && y.number && x.number === y.number && (chr >= 0.2 || cos >= 0.15) ? 1 : 0;
  const diffNo = x.number && y.number && x.number !== y.number && !(x.numberAssigned && y.numberAssigned) ? 1 : 0;
  const da = x.discipline || (a.ders[0] && a.ders[0].p >= 0.75 ? a.ders[0].name : '');
  const db = y.discipline || (b.ders[0] && b.ders[0].p >= 0.75 ? b.ders[0].name : '');
  const dersConflict = da && db && da !== db ? 1 : 0;
  const short = Math.min(sa.size, sb.size) <= 2 ? 1 : 0;
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
export async function clusterRecall(items: RecallItem[], eng: RecallEngine, opts: { linkProb?: number } = {}) {
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
    const sim: Float32Array[] = Array.from({ length: n }, () => new Float32Array(n));
    for (let i = 0; i < n; i++) {
      for (let j = 0; j < i; j++) {
        const p = pairProb(pairFeatures(group[i], group[j], eng, cache));
        sim[i][j] = p; sim[j][i] = p;
      }
      await yieldIfBusy();
    }
    // Yuva numaraları farklı iki küme asla birleşmez (aynı sınavın iki ayrı sorusu)
    const slot = group.map((g) => (g.numberAssigned && g.number ? g.number : 0));
    for (let i = 0; i < n; i++) for (let j = 0; j < i; j++) if (slot[i] && slot[j] && slot[i] !== slot[j]) { sim[i][j] = -1; sim[j][i] = -1; }
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
      const v = best[ba];
      const na = members[ba].length, nb = members[bb].length;
      slot[ba] = slot[ba] || slot[bb];
      for (let c = 0; c < n; c++) {
        if (!alive[c] || c === ba || c === bb) continue;
        const s = sim[ba][c] < 0 || sim[bb][c] < 0 || (slot[ba] && slot[c] && slot[ba] !== slot[c])
          ? -1 : (na * sim[ba][c] + nb * sim[bb][c]) / (na + nb);
        sim[ba][c] = s; sim[c][ba] = s;
      }
      internal[ba] += internal[bb] + v * na * nb;
      members[ba] = members[ba].concat(members[bb]);
      alive[bb] = 0;
      rescan(ba);
      for (let c = 0; c < n; c++) {
        if (!alive[c] || c === ba) continue;
        if (bestJ[c] === ba || bestJ[c] === bb) rescan(c);
        else if (sim[c][ba] > best[c]) { best[c] = sim[c][ba]; bestJ[c] = ba; }
      }
      await yieldIfBusy();
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

/** Kümenin taslağı: medoid metin + oylar + ortak çıkmış soru adayı. Yapay zekâ yok; kanıt dışı bilgi eklemez. */
export function draftCluster(members: RecallItem[], eng: RecallEngine): RecallDraft {
  // Temsilci: kümenin ortak ögelerini (en az 2 üyede geçen kökler, IDF ağırlıklı) en çok kapsayan hatırlama;
  // eşitlikte daha bilgili/uzun olan. Cümle onun sözcükleriyle kurulur (bilgi eklenmez).
  const stemCount = new Map<string, number>();
  for (const m of members) for (const st of new Set(m.a.stems)) stemCount.set(st, (stemCount.get(st) || 0) + 1);
  const common = [...stemCount].filter(([, c]) => c >= 2 || members.length === 1);
  const commonW = common.reduce((t, [st]) => t + eng.idf(st), 0) || 1;
  let medoid = members[0], bestScore = -1;
  for (const m of members) {
    const own = new Set(m.a.stems);
    let cov = 0;
    for (const [st] of common) if (own.has(st)) cov += eng.idf(st);
    const score = cov / commonW + 0.1 * Math.min(1, m.a.words.length / 10) - (m.a.words.length > 40 ? 0.1 : 0);
    if (score > bestScore) { bestScore = score; medoid = m; }
  }
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
  return {
    stem: eng.cleanSentence(medoid.text) || medoid.a.clean,
    medoidKey: medoid.key,
    discipline: dTop ? { name: dTop[0], p: Math.round((dTop[1] / dTot) * 100) / 100 } : null,
    konu: [...konuVote].sort((a, b) => b[1] - a[1])[0]?.[0] || null,
    terms: [...termVote].sort((a, b) => b[1] - a[1]).map(([t]) => t).slice(0, 8),
    number: [...numVote].sort((a, b) => b[1] - a[1])[0]?.[0] ?? null,
    negativeLikely: members.filter((m) => m.a.negative >= 0.5).length >= Math.max(1, members.length * 0.3),
    answerVotes,
    answerTextVotes: textVotes.sort((a, b) => b.votes - a.votes),
    bankMatch,
  };
}

export type { Letter };
