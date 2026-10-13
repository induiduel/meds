/**
 * Çift modelinin öğrenilmesi ve öğrenilmiş ağırlıkların yüklenmesi.
 *
 * - `fitPairModel`: işaret kısıtlı (benzerlik ≥ 0, ceza ≤ 0), sınıf dengeli, L2'li lojistik; standartlaştırılmış
 *   özelliklerle Adam. Örnek ağırlığı verilebilir (öğrenci kararları sentetik çiftlerden daha değerlidir).
 * - Öğrenilmiş ağırlıklar `data/recall_weights.json`'da durur (scripts/recall/learn.mts yazar; yalnız sınama setinde
 *   gerileme yoksa). Sunucu motoru kurarken `loadLearnedWeights` ile okur; dosya yoksa/uyumsuzsa kod içi ağırlıklar.
 */
import fs from 'fs';
import path from 'path';
import { PAIR_FEATURES, PAIR_WEIGHTS, setPairWeights, setLinkProb } from './cluster.ts';

export type PairWeights = typeof PAIR_WEIGHTS;
const SIGN: Record<string, number> = { cos: 1, contain: 1, chr: 1, term: 1, anchor: 1, opt: 1, sameNo: 1, diffNo: -1, dersConflict: -1 };

export function fitPairModel(X: number[][], Y: number[], o: { l2?: number; epochs?: number; sampleWeight?: number[]; fixed?: Partial<PairWeights> } = {}): PairWeights {
  const D = PAIR_FEATURES.length;
  const l2 = o.l2 ?? 0.5, epochs = o.epochs ?? 1500;
  const fixedIdx = new Map<number, number>();
  for (const [k, v] of Object.entries(o.fixed || {})) fixedIdx.set(PAIR_FEATURES.indexOf(k as any), v as number);
  const mu = new Array(D).fill(0), sd = new Array(D).fill(1);
  for (let k = 1; k < D; k++) {
    let m = 0; for (const x of X) m += x[k]; m /= X.length || 1;
    let v = 0; for (const x of X) v += (x[k] - m) ** 2; v = Math.sqrt(v / (X.length || 1)) || 1;
    mu[k] = m; sd[k] = v;
  }
  const Z = X.map((x) => x.map((v, k) => (k ? (fixedIdx.has(k) ? 0 : (v - mu[k]) / sd[k]) : 1)));
  // Sabit tutulan özelliklerin katkısı ofset olarak eklenir
  const off = X.map((x) => { let t = 0; for (const [k, w] of fixedIdx) t += w * x[k]; return t; });
  const pos = Y.reduce((a, b) => a + b, 0);
  const wPos = (Y.length - pos) / Math.max(1, pos);
  const sw = o.sampleWeight || Y.map(() => 1);
  const norm = sw.reduce((a, b) => a + b, 0) || 1; // örnek ağırlığı yoksa çift sayısı (eski ölçekle aynı)
  const wz = new Array(D).fill(0), m1 = new Array(D).fill(0), m2 = new Array(D).fill(0);
  const b1 = 0.9, b2 = 0.999, lr = 0.05;
  for (let ep = 1; ep <= epochs; ep++) {
    const g = new Array(D).fill(0);
    for (let i = 0; i < Z.length; i++) {
      let z = off[i];
      for (let k = 0; k < D; k++) z += Z[i][k] * wz[k];
      const p = 1 / (1 + Math.exp(-z));
      const w = (Y[i] ? wPos : 1) * sw[i];
      for (let k = 0; k < D; k++) g[k] += w * (p - Y[i]) * Z[i][k];
    }
    for (let k = 0; k < D; k++) {
      if (fixedIdx.has(k)) continue;
      const gk = g[k] / norm + (k ? l2 * wz[k] : 0);
      m1[k] = b1 * m1[k] + (1 - b1) * gk; m2[k] = b2 * m2[k] + (1 - b2) * gk * gk;
      wz[k] -= (lr * (m1[k] / (1 - b1 ** ep))) / (Math.sqrt(m2[k] / (1 - b2 ** ep)) + 1e-8);
      const sg = SIGN[PAIR_FEATURES[k]];
      if (sg && wz[k] * sg < 0) wz[k] = 0;
    }
  }
  const w = wz.map((v, k) => (k ? (fixedIdx.has(k) ? fixedIdx.get(k)! : v / sd[k]) : v));
  w[0] = wz[0] - wz.slice(1).reduce((s, v, k) => s + (fixedIdx.has(k + 1) ? 0 : (v * mu[k + 1]) / sd[k + 1]), 0);
  return Object.fromEntries(PAIR_FEATURES.map((k, i) => [k, Math.round(w[i] * 100) / 100])) as PairWeights;
}

export const LEARNED_FILE = 'data/recall_weights.json';
export interface LearnedWeights { features: string[]; weights: PairWeights; linkProb: number; fittedAt: string; feedbackPairs: number; metrics?: Record<string, number> }

/** Öğrenilmiş ağırlıkları uygular (özellik listesi aynıysa). Uygulandıysa dosya içeriğini döndürür. */
export function loadLearnedWeights(rootDir: string): LearnedWeights | null {
  try {
    const j = JSON.parse(fs.readFileSync(path.join(rootDir, LEARNED_FILE), 'utf8')) as LearnedWeights;
    if (JSON.stringify(j.features) !== JSON.stringify(PAIR_FEATURES) || !j.weights || !(j.linkProb > 0 && j.linkProb < 1)) return null;
    setPairWeights(j.weights);
    setLinkProb(j.linkProb);
    return j;
  } catch {
    return null;
  }
}
