// Öğrenci kararlarından çift modelini yeniden öğrenir (sunucu haftada bir, ≥20 yeni kararla çalıştırır).
//   npx tsx scripts/recall/learn.mts            # yalnız rapor
//   npx tsx scripts/recall/learn.mts --write    # kapıdan geçerse data/recall_weights.json yazar
// Eğitim: sınama setinin geliştirme yarısı (k1–k3, sentetik çiftler) + öğrenci kararlarının %75'i (3 kat ağırlık).
// Kapı: (1) kararların ayrılmış %25'inde doğruluk düşmemeli, (2) test kümesinde (k4–k6) gruplama F1 en çok 1 puan düşebilir.
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { createRecallEngine, type RecallEngine } from '../../src/services/recall/engine.ts';
import { clusterRecall, pairFeatures, pairProb, PAIR_FEATURES, PAIR_WEIGHTS, LINK_PROB, setPairWeights, setLinkProb, type RecallItem } from '../../src/services/recall/cluster.ts';
import { splitRecall } from '../../src/services/recall/normalize.ts';
import { fitPairModel, loadLearnedWeights, LEARNED_FILE, type LearnedWeights } from '../../src/services/recall/fit.ts';
import { readFeedback, latestDecisions } from '../../src/services/recall/feedback.ts';
import { questionToItems, knownNumbered } from '../../src/services/poolClusterService.ts';

process.env.CUDA_VISIBLE_DEVICES = '';
const root = new URL('../../', import.meta.url).pathname;
const WRITE = process.argv.includes('--write');
// --data <klasör>: kararlar ve havuz başka klasörden (deneme); yazım da oraya
const di = process.argv.indexOf('--data');
const DATA = di > 0 ? process.argv[di + 1] : path.join(root, 'data');
const MIN = 20;
const DS = `${root}scripts/eval/datasets/hatirlama`;

const fb = latestDecisions(readFeedback(DATA));
if (fb.length < MIN) { console.log(`öğrenci kararı ${fb.length} < ${MIN}: öğrenme yapılmadı`); process.exit(0); }

const targets = new Set<string>();
for (let k = 1; k <= 6; k++) for (const t of JSON.parse(fs.readFileSync(`${DS}/hedef_k${k}.json`, 'utf8'))) targets.add(t.id);
const eng = await createRecallEngine(root, { excludeIds: targets });
const current: { weights: typeof PAIR_WEIGHTS; link: number } = { weights: { ...(loadLearnedWeights(root)?.weights || PAIR_WEIGHTS) }, link: LINK_PROB };

type Item = RecallItem & { gold: string[]; mid: string };
function itemsFor(ks: number[]): Item[] {
  const out: Item[] = [];
  for (const k of ks) for (const m of JSON.parse(fs.readFileSync(`${DS}/hatirlama_k${k}.json`, 'utf8'))) {
    splitRecall(m.metin).forEach((p, i) => {
      const a = eng.analyze(p, { committeeId: `donem3-kurul${k}` });
      out.push({ key: `${m.mid}#${i}`, mid: m.mid, committeeId: `donem3-kurul${k}`, createdAt: m.mid, number: a.number, text: p, a, gold: m.soru_idler });
    });
  }
  return out;
}
const vec = (f: any) => PAIR_FEATURES.map((k) => f[k]);

// Sentetik çiftler (dev)
const dev = itemsFor([1, 2, 3]).filter((x) => !x.a.isNoise && x.gold.length);
const X: number[][] = [], Y: number[] = [], W: number[] = [];
for (let i = 0; i < dev.length; i++) for (let j = 0; j < i; j++) {
  const a = dev[i], b = dev[j];
  if (a.committeeId !== b.committeeId || a.mid === b.mid) continue;
  X.push(vec(pairFeatures(a, b, eng))); Y.push(a.gold.some((g) => b.gold.includes(g)) ? 1 : 0); W.push(1);
}

// Öğrenci kararları: yazılan metin ↔ önerilen havuz kaydı (bugünkü hâli)
const qdb = JSON.parse(fs.readFileSync(path.join(DATA, 'questions.json'), 'utf8'));
const questions: any[] = Array.isArray(qdb) ? qdb : qdb.questions || [];
const byId = new Map(questions.map((q) => [String(q.id), q]));
const fbPairs: { f: number[]; y: number; holdout: boolean }[] = [];
for (const d of fb) {
  const q = byId.get(d.questionId);
  if (!q) continue;
  const known = knownNumbered(questions, d.committeeId, q.id);
  const other = questionToItems(q, eng as RecallEngine, known)?.recall;
  if (!other) continue;
  const a = eng.analyze(d.text, { committeeId: d.committeeId });
  const me: RecallItem = { key: 'yeni', committeeId: d.committeeId, createdAt: d.at, number: a.number, text: d.text, a };
  const holdout = parseInt(crypto.createHash('sha1').update(d.text + d.questionId).digest('hex').slice(0, 2), 16) < 64; // ~%25
  fbPairs.push({ f: vec(pairFeatures(me, other, eng)), y: d.decision === 'ayni' ? 1 : 0, holdout });
}
for (const p of fbPairs) if (!p.holdout) { X.push(p.f); Y.push(p.y); W.push(3); }
const train = fbPairs.filter((p) => !p.holdout).length, hold = fbPairs.filter((p) => p.holdout);
console.log(`öğrenci kararı ${fb.length} (eşleşen ${fbPairs.length}: eğitim ${train}, ayrılan ${hold.length}) · sentetik çift ${X.length - train}`);

// Şık örtüşmesi ancak iki tarafında da şık olan yeterli karar (≥50) varsa öğrenilir; yoksa mevcut değer korunur
const optIdx = PAIR_FEATURES.indexOf('opt');
const withOpt = fbPairs.filter((p) => !p.holdout && p.f[optIdx] > 0).length;
const fitted = fitPairModel(X, Y, { l2: 0.5, sampleWeight: W, fixed: withOpt < 50 ? { opt: current.weights.opt } : {} });

// Eşik: dev kümelemede F0.5 (yanlış birleşme pahalı)
async function clusterF(items: Item[]) {
  const gs = await clusterRecall(items, eng);
  const cl = new Map<string, number>(); gs.forEach((g, i) => g.members.forEach((m) => cl.set(m.key, i)));
  let tp = 0, fp = 0, fn = 0;
  for (let i = 0; i < items.length; i++) for (let j = 0; j < i; j++) {
    const a = items[i], b = items[j];
    if (a.mid === b.mid || a.a.isNoise || b.a.isNoise || !a.gold.length || !b.gold.length) continue;
    const same = a.gold.some((g) => b.gold.includes(g)), tog = cl.get(a.key) === cl.get(b.key);
    if (same && tog) tp++; else if (!same && tog) fp++; else if (same) fn++;
  }
  const P = tp / Math.max(1, tp + fp), R = tp / Math.max(1, tp + fn);
  return { F1: (2 * P * R) / Math.max(1e-9, P + R), F05: (1.25 * P * R) / Math.max(1e-9, 0.25 * P + R) };
}
setPairWeights(fitted);
let link = 0.6, best = -1;
for (const t of [0.5, 0.55, 0.6, 0.65, 0.7, 0.75]) { setLinkProb(t); const m = await clusterF(dev); if (m.F05 > best) { best = m.F05; link = t; } }

const acc = (w: typeof PAIR_WEIGHTS, thr: number) => {
  if (!hold.length) return NaN;
  setPairWeights(w);
  let ok = 0;
  for (const p of hold) { const z = PAIR_FEATURES.reduce((s, k, i) => s + (w as any)[k] * p.f[i], 0); ok += (1 / (1 + Math.exp(-z)) >= thr ? 1 : 0) === p.y ? 1 : 0; }
  return ok / hold.length;
};
const test = itemsFor([4, 5, 6]);
setPairWeights(current.weights); setLinkProb(current.link);
const before = { test: (await clusterF(test)).F1, hold: acc(current.weights, current.link) };
setPairWeights(fitted); setLinkProb(link);
const after = { test: (await clusterF(test)).F1, hold: acc(fitted, link) };
const pct = (x: number) => (Number.isNaN(x) ? '—' : `${(100 * x).toFixed(1)}%`);
console.log(`test F1 ${pct(before.test)} → ${pct(after.test)} · ayrılan kararlarda doğruluk ${pct(before.hold)} → ${pct(after.hold)} · eşik ${current.link} → ${link}`);
console.log('ağırlıklar:', JSON.stringify(fitted));

const pass = after.test >= before.test - 0.01 && (Number.isNaN(after.hold) || after.hold >= before.hold);
if (!pass) { console.log('KAPI: geçmedi, ağırlıklar yazılmadı'); process.exit(2); }
if (WRITE) {
  const out: LearnedWeights = { features: [...PAIR_FEATURES], weights: fitted, linkProb: link, fittedAt: new Date().toISOString(), feedbackPairs: fbPairs.length, metrics: { testF1Before: before.test, testF1After: after.test, holdoutBefore: before.hold, holdoutAfter: after.hold } };
  const f = path.join(DATA, path.basename(LEARNED_FILE));
  fs.writeFileSync(`${f}.tmp`, JSON.stringify(out, null, 2));
  fs.renameSync(`${f}.tmp`, f);
  console.log(`KAPI: geçti, ${f} yazıldı`);
} else console.log('KAPI: geçti (yazmak için --write)');
process.exit(0);
