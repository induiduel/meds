// Soru havuzu motoru ölçümü (gerçek çıkmış sorulardan üretilmiş öğrenci hatırlamaları; LLM yok).
//   npx tsx scripts/eval/recall-engine.mts                 # test kümesi (k4–k6), banka hedef soruları İÇERMEZ (yeni sınav)
//   npx tsx scripts/eval/recall-engine.mts --bank include  # banka hedefleri içerir (öğrenciler eski bir soruyu hatırlıyor)
//   npx tsx scripts/eval/recall-engine.mts --split dev     # geliştirme kümesi (k1–k3)
//   npx tsx scripts/eval/recall-engine.mts --fit           # çift modelini dev'de öğren, eşiği seç, test'te ölç
//   npx tsx scripts/eval/recall-engine.mts --kitle          # ek: eski kitle kaynak veri setlerinde gruplama
//   npx tsx scripts/eval/recall-engine.mts --dump-bank f    # çıkmış eşleşme puanlarını yaz (BANK_MATCH ayarı için)
// Eski motorun (kume-v2, 2026-10-12) aynı verideki sonucu: test F1 %37,5 · ARI 0,371; dev F1 %43,7 · ARI 0,430.
// Veri: scripts/eval/datasets/hatirlama/{hedef,hatirlama}_k*.json
import fs from 'fs';
import { createRecallEngine } from '../../src/services/recall/engine.ts';
import { clusterRecall, assignToGroup, draftCluster, setBankMatch, pairFeatures, PAIR_FEATURES, PAIR_WEIGHTS, setPairWeights, LINK_PROB, setLinkProb, type RecallItem } from '../../src/services/recall/cluster.ts';
import { splitRecall } from '../../src/services/recall/normalize.ts';
import { fitPairModel } from '../../src/services/recall/fit.ts';
import { fold } from '../../src/services/questionIntake.ts';

const root = new URL('../../', import.meta.url).pathname;
const DS = `${root}scripts/eval/datasets/hatirlama`;
const arg = (k: string, d?: string) => { const i = process.argv.indexOf(`--${k}`); return i > 0 ? (process.argv[i + 1] && !process.argv[i + 1].startsWith('--') ? process.argv[i + 1] : 'true') : d; };
const bankMode = arg('bank', 'exclude');
const FIT = arg('fit') === 'true';
const DROP = (arg('drop', '') || '').split(',').filter(Boolean); // --drop nbr,anchor: özelliği devre dışı bırak
const VERBOSE = arg('verbose') === 'true';


type Target = { id: string; committeeId: string; discipline: string; topic: string; stem: string; options: { key: string; text: string }[]; correctAnswer: string; group: string; questionNumber?: number };
type Msg = { mid: string; metin: string; soru_idler: string[]; tur: string; iddia_harf: string | null; iddia_dogru: boolean | null; no: number | null };
const targets = new Map<string, Target>();
const msgsByK = new Map<number, (Msg & { committeeId: string })[]>();
for (let k = 1; k <= 6; k++) {
  const f = `${DS}/hatirlama_k${k}.json`;
  if (!fs.existsSync(f)) continue;
  for (const t of JSON.parse(fs.readFileSync(`${DS}/hedef_k${k}.json`, 'utf8')) as Target[]) targets.set(t.id, t);
  msgsByK.set(k, (JSON.parse(fs.readFileSync(f, 'utf8')) as Msg[]).map((m) => ({ ...m, committeeId: `donem3-kurul${k}` })));
}
const splitOf = (s: string) => (s === 'dev' ? [1, 2, 3] : s === 'all' ? [1, 2, 3, 4, 5, 6] : [4, 5, 6]).filter((k) => msgsByK.has(k));

if (arg('dump-bank')) setBankMatch(() => true);
const t0 = performance.now();
const engine = await createRecallEngine(root, { excludeIds: bankMode === 'include' ? new Set() : new Set(targets.keys()) });
console.log(`motor ${engine.version} · banka ${engine.bankSize} (${bankMode === 'include' ? 'hedefler dahil' : 'hedefler hariç'}) · sözlük ${engine.lexicon.size} · terim ${engine.terms.size} · kurulum ${(performance.now() - t0).toFixed(0)} ms`);

/** Mesajı birimlere böler (çok sorulu mesaj) ve analiz eder. */
function itemsFor(ks: number[], split = true) {
  const items: (RecallItem & { gold: string[]; msg: Msg })[] = [];
  for (const k of ks) for (const m of msgsByK.get(k)!) {
    const parts = split ? splitRecall(m.metin) : [m.metin];
    parts.forEach((p, i) => {
      const a = engine.analyze(p, { committeeId: m.committeeId });
      items.push({ key: `${m.mid}#${i}`, committeeId: m.committeeId, createdAt: m.mid, number: a.number, text: p, a, gold: m.soru_idler, msg: m });
    });
  }
  return items;
}

// ---------------------------------------------------------------- metrikler
function clusterMetrics(items: { key: string; gold: string[]; a: any }[], groups: { members: { key: string }[] }[]) {
  const cl = new Map<string, number>();
  groups.forEach((g, i) => g.members.forEach((m) => cl.set(m.key, i)));
  const real = items.filter((x) => x.gold.length && !x.a.isNoise);
  let tp = 0, fp = 0, fn = 0;
  for (let i = 0; i < real.length; i++) for (let j = 0; j < i; j++) {
    const a = real[i], b = real[j];
    if (a.key.split('#')[0] === b.key.split('#')[0]) continue; // aynı mesajın parçaları
    const same = a.gold.some((g) => b.gold.includes(g));
    const tog = cl.has(a.key) && cl.get(a.key) === cl.get(b.key);
    if (same && tog) tp++; else if (!same && tog) fp++; else if (same && !tog) fn++;
  }
  const P = tp / Math.max(1, tp + fp), R = tp / Math.max(1, tp + fn), F = (2 * P * R) / Math.max(1e-9, P + R);
  // B-küp (birincil etiket)
  let bp = 0, br = 0;
  for (const x of real) {
    const c = cl.get(x.key);
    const mates = real.filter((y) => cl.get(y.key) === c);
    const goldMates = real.filter((y) => y.gold[0] === x.gold[0]);
    bp += mates.filter((y) => y.gold[0] === x.gold[0]).length / mates.length;
    br += goldMates.filter((y) => cl.get(y.key) === c).length / goldMates.length;
  }
  bp /= real.length; br /= real.length;
  const bF = (2 * bp * br) / Math.max(1e-9, bp + br);
  // ARI (birincil etiket, tekiller kendi kümesi)
  const lab = real.map((x) => x.gold[0]);
  const pred = real.map((x, i) => (cl.has(x.key) ? `c${cl.get(x.key)}` : `s${i}`));
  const ari = adjustedRand(lab, pred);
  const goldQs = new Set(real.map((x) => x.gold[0])).size;
  const multi = groups.filter((g) => g.members.length >= 2).length;
  return { P, R, F, bP: bp, bR: br, bF, ari, goldQs, multi, singles: groups.filter((g) => g.members.length === 1).length };
}
function adjustedRand(a: string[], b: string[]) {
  const n = a.length, c2 = (x: number) => (x * (x - 1)) / 2;
  const ct = new Map<string, number>(), ra = new Map<string, number>(), rb = new Map<string, number>();
  for (let i = 0; i < n; i++) {
    ct.set(`${a[i]}\u0000${b[i]}`, (ct.get(`${a[i]}\u0000${b[i]}`) || 0) + 1);
    ra.set(a[i], (ra.get(a[i]) || 0) + 1); rb.set(b[i], (rb.get(b[i]) || 0) + 1);
  }
  let sij = 0; for (const v of ct.values()) sij += c2(v);
  let sa = 0; for (const v of ra.values()) sa += c2(v);
  let sb = 0; for (const v of rb.values()) sb += c2(v);
  const exp = (sa * sb) / c2(n), max = (sa + sb) / 2;
  return (sij - exp) / Math.max(1e-9, max - exp);
}
const stemsOf = (s: string) => new Set(fold(s).split(' ').filter((w) => w.length >= 4).map((w) => w.slice(0, 5)));
const tokenF1 = (a: string, b: string) => {
  const A = stemsOf(a), B = stemsOf(b);
  const i = [...A].filter((x) => B.has(x)).length;
  if (!i) return 0;
  const p = i / A.size, r = i / B.size;
  return (2 * p * r) / (p + r);
};
const pct = (x: number) => `${(x * 100).toFixed(1)}%`;

// ---------------------------------------------------------------- çift modeli öğrenme (dev)
if (FIT) {
  const dev = itemsFor(splitOf(arg('train', 'dev')!)).filter((x) => !x.a.isNoise && x.gold.length);
  const X: number[][] = [], Y: number[] = [];
  for (let i = 0; i < dev.length; i++) for (let j = 0; j < i; j++) {
    const a = dev[i], b = dev[j];
    if (a.committeeId !== b.committeeId || a.key.split('#')[0] === b.key.split('#')[0]) continue;
    const f = pairFeatures(a, b, engine);
    X.push(PAIR_FEATURES.map((k) => (DROP.includes(k) && k !== 'opt' ? 0 : (f as any)[k])));
    Y.push(a.gold.some((g) => b.gold.includes(g)) ? 1 : 0);
  }
  if (arg('dump-pairs')) { fs.writeFileSync(arg('dump-pairs')!, JSON.stringify({ features: PAIR_FEATURES, X, Y })); console.log('çiftler yazıldı'); process.exit(0); }
  const pos = Y.filter(Boolean).length;
  const learned = fitPairModel(X, Y, { l2: Number(arg('l2', '0.5')), fixed: DROP.includes('opt') ? { opt: PAIR_WEIGHTS.opt } : {} });
  // Dengeli eğitim olasılığı kaydırır: yanlış birleşme pahalı olduğundan eşik dev'de F0.5'e göre seçilir
  setPairWeights(learned);
  console.log(`dev çiftleri ${X.length} (pozitif ${pos}) · öğrenilen ağırlıklar:`, JSON.stringify(learned));
  let bestThr = LINK_PROB, bestF = -1;
  for (const thr of [0.4, 0.5, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9]) {
    const groups = await clusterRecall(dev, engine, { linkProb: thr });
    if (arg('quiet')) { const m = clusterMetrics(dev, groups); const f05 = (1.25 * m.P * m.R) / Math.max(1e-9, 0.25 * m.P + m.R); if (f05 > bestF) { bestF = f05; bestThr = thr; } continue; }
    const m = clusterMetrics(dev, groups);
    // Yanlış birleşme (P) daha pahalı: F0.5
    const f05 = (1.25 * m.P * m.R) / Math.max(1e-9, 0.25 * m.P + m.R);
    console.log(`  eşik ${thr}: P ${pct(m.P)} R ${pct(m.R)} F1 ${pct(m.F)} F0.5 ${pct(f05)} B³ ${pct(m.bF)} küme ${m.multi}/${m.goldQs}`);
    if (f05 > bestF) { bestF = f05; bestThr = thr; }
  }
  setLinkProb(bestThr);
  console.log(`seçilen eşik ${bestThr}`);
}

// ---------------------------------------------------------------- ölçüm
const split = arg('split', 'test')!;
const items = itemsFor(splitOf(split));
const t1 = performance.now();
let groups = await clusterRecall(items, engine);
let clusterMs = performance.now() - t1;
// --incremental f: ilk f oranı toplu kümelenir, kalanlar geliş sırasıyla tek tek mevcut kümelere atanır (sunucudaki artımlı yol)
if (arg('incremental')) {
  const f = Number(arg('incremental')) || 0.3;
  const order = [...items].sort((a, b) => (a.createdAt < b.createdAt ? -1 : 1));
  const cut = Math.floor(order.length * f);
  const t2 = performance.now();
  const gs: { members: RecallItem[]; cohesion: number }[] = cut ? await clusterRecall(order.slice(0, cut), engine) : [];
  for (const it of order.slice(cut)) {
    if (it.a.isNoise) continue;
    const hit = assignToGroup(it, gs, engine, { linkProb: Number(arg('assign-p', '0.6')), cap: Number(arg('cap', '12')) });
    if (hit) hit.group.members.push(it); else gs.push({ members: [it], cohesion: 1 });
  }
  clusterMs = performance.now() - t2;
  groups = gs;
  console.log(`(artımlı: ilk %${Math.round(f * 100)} toplu, ${order.length - cut} öge tek tek atandı)`);
}

// Gürültü
const noiseGold = items.filter((x) => !x.gold.length), noisePred = items.filter((x) => x.a.isNoise);
const noiseTP = noisePred.filter((x) => !x.gold.length).length;
// Ders / konu (tek sorulu, gürültüsüz)
const single = items.filter((x) => x.gold.length === 1 && !x.a.isNoise);
let dersHit = 0, ders2 = 0, konuHit = 0, dersConf = 0, dersConfHit = 0;
for (const x of single) {
  const t = targets.get(x.gold[0])!;
  if (x.a.ders[0]?.name === t.discipline) dersHit++;
  if (x.a.ders.slice(0, 2).some((d) => d.name === t.discipline)) ders2++;
  if (x.a.konu?.name === t.topic) konuHit++;
  if ((x.a.ders[0]?.p || 0) >= 0.75) { dersConf++; if (x.a.ders[0].name === t.discipline) dersConfHit++; }
}
// Terim kesinliği: çıkarılan terim hedef sorunun metninde (katlanmış kök) geçiyor mu
let termN = 0, termOk = 0;
for (const x of single) {
  const t = targets.get(x.gold[0])!;
  const gold = stemsOf(`${t.stem} ${t.options.map((o) => o.text).join(' ')}`);
  for (const term of x.a.terms) { termN++; if ([...stemsOf(term)].some((s) => gold.has(s))) termOk++; }
}
// İddia/no çıkarımı
const claimMsgs = items.filter((x) => x.msg.iddia_harf && x.gold.length === 1);
const claimHit = claimMsgs.filter((x) => x.a.claimedLetter === x.msg.iddia_harf).length;
const claimFalse = items.filter((x) => !x.msg.iddia_harf && x.a.claimedLetter).length;
const noMsgs = items.filter((x) => x.msg.no);
const noHit = noMsgs.filter((x) => x.number === x.msg.no).length;

const met = clusterMetrics(items, groups);
// Taslak
let dN = 0, dF1 = 0, bankN = 0, bankHit = 0, bankSame = 0, ansN = 0, ansHit = 0, dersClHit = 0;
for (const g of groups) {
  if (g.members.length < 2) continue;
  const golds = new Map<string, number>();
  for (const m of g.members as any[]) for (const id of m.gold) golds.set(id, (golds.get(id) || 0) + 1);
  const top = [...golds].sort((a, b) => b[1] - a[1])[0];
  if (!top) continue;
  const t = targets.get(top[0])!;
  const d = draftCluster(g.members, engine);
  dN++;
  dF1 += tokenF1(d.stem, t.stem);
  if (d.discipline?.name === t.discipline) dersClHit++;
  if (d.bankMatch) { bankN++; if (d.bankMatch.id === t.id) bankHit++; else if (tokenF1(d.bankMatch.stem, t.stem) >= 0.6) bankSame++; }
  if (arg('dump-bank') && d.bankMatch) fs.appendFileSync(arg('dump-bank')!, JSON.stringify({ mode: bankMode, ok: d.bankMatch.id === t.id, score: d.bankMatch.score, margin: d.bankMatch.margin, support: d.bankMatch.support, n: g.members.length }) + '\n');
  const av = Object.entries(d.answerVotes).sort((a, b) => b[1] - a[1]);
  if (av.length && av[0][1] >= 2) { ansN++; if (av[0][0] === t.correctAnswer) ansHit++; }
  if (VERBOSE) console.log(`\n■ ${g.members.length} üye · altın ${t.id} (${top[1]}/${g.members.length}) · ${d.discipline?.name}\n  ALTIN: ${t.stem.slice(0, 140)}\n  TASLAK: ${d.stem.slice(0, 140)}\n  BANKA: ${d.bankMatch ? `${d.bankMatch.id === t.id ? '✓' : '✗'} ${d.bankMatch.stem.slice(0, 100)}` : '-'}`);
}

console.log(`\n=== ${split} (${splitOf(split).map((k) => `k${k}`).join(',')}) · ${items.length} birim / ${new Set(items.map((x) => x.msg.mid)).size} mesaj ===`);
console.log(`Gürültü ayıklama: kesinlik ${pct(noiseTP / Math.max(1, noisePred.length))} · duyarlılık ${pct(noiseTP / Math.max(1, noiseGold.length))} (${noisePred.length} işaretlendi / ${noiseGold.length} gerçek)`);
console.log(`Ders: top1 ${pct(dersHit / single.length)} · top2 ${pct(ders2 / single.length)} · güvenli (p≥0.75) ${pct(dersConf / single.length)} kapsama, ${pct(dersConfHit / Math.max(1, dersConf))} isabet · konu top1 ${pct(konuHit / single.length)}`);
console.log(`Terim kesinliği ${pct(termOk / Math.max(1, termN))} (${termN} terim, birim başına ${(termN / single.length).toFixed(2)})`);
console.log(`Cevap iddiası harfi: ${pct(claimHit / Math.max(1, claimMsgs.length))} (${claimMsgs.length}) · yanlış iddia çıkarımı ${claimFalse} · soru no: ${pct(noHit / Math.max(1, noMsgs.length))} (${noMsgs.length})`);
console.log(`Gruplama: ${met.goldQs} gerçek soru → ${met.multi} küme + ${met.singles} tekil · çift P ${pct(met.P)} R ${pct(met.R)} F1 ${pct(met.F)} · B³ P ${pct(met.bP)} R ${pct(met.bR)} F1 ${pct(met.bF)} · ARI ${met.ari.toFixed(3)} · ${clusterMs.toFixed(0)} ms`);
console.log(`Taslak (${dN} küme): medoid kök benzerliği (kök F1) ${pct(dF1 / Math.max(1, dN))} · küme dersi ${pct(dersClHit / Math.max(1, dN))} · çıkmış eşleşmesi önerilen ${bankN} (${bankMode === 'include' ? `doğru ${pct(bankHit / Math.max(1, bankN))} (+${bankSame} başka yılın aynı sorusu), kapsama ${pct(bankHit / Math.max(1, dN))}` : `hedef bankada yok; ${bankSame} tanesi başka yılın aynı sorusu (kök F1 ≥ 0.6), ${bankN - bankSame} yanlış`}) · oy çoğunluğu cevabı ${pct(ansHit / Math.max(1, ansN))} (${ansN} küme)`);

// ---------------------------------------------------------------- ek: kitle kaynak veri setleri (kurul/ders yok; yalnız gruplama)
if (arg('kitle') === 'true') {
  for (const f of ['synthetic_10q_500v', 'challenging_14q_650v']) {
    const d = JSON.parse(fs.readFileSync(`${root}scripts/eval/datasets/kitle_kaynak/${f}.json`, 'utf8'));
    const its: (RecallItem & { gold: string[]; a: any })[] = [];
    d.forEach((x: any) => x.varyasyonlar.forEach((v: any, i: number) => {
      const a = engine.analyze(v.metin, { committeeId: 'kitle' });
      its.push({ key: `${x.soru_id}-${i}`, committeeId: 'kitle', createdAt: '', number: a.number, text: v.metin, a, gold: [String(x.soru_id)] });
    }));
    const gs = await clusterRecall(its, engine);
    const m = clusterMetrics(its, gs);
    console.log(`Kitle ${f}: ${its.length} mesaj · ${m.goldQs} soru → ${m.multi} küme · çift P ${pct(m.P)} R ${pct(m.R)} F1 ${pct(m.F)} · ARI ${m.ari.toFixed(3)}`);
  }
}
