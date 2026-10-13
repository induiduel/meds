// Sınav sırasından ders ön bilgisi (numberDersPrior) ölçümü: 15 gerçek sınav dökümünde her soru için öğrenci tarzı
// kısaltılmış/aksansız metin + soru no; aynı sınavın numaralı sorularının %20'si "havuzda biliniyor". Sorular bankadan
// çıkarılır. Yalnız metin ↔ metin + sınav sırası ders isabeti, ağırlık taraması.
//   npx tsx scripts/eval/recall-number-prior.mts
import fs from 'fs';
import { createRecallEngine, numberDersPrior, CLASSIFY } from '../../src/services/recall/engine.ts';
import { fold } from '../../src/services/recall/normalize.ts';

const root = new URL('../../', import.meta.url).pathname;
const past: any[] = JSON.parse(fs.readFileSync(`${root}data/pastQuestions.json`, 'utf8'));
const by = new Map<string, Map<number, any>>();
for (const q of past) {
  if (q.status !== 'verified' || !String(q.committeeId || '').startsWith('donem3-kurul') || !(q.questionNumber > 0 && q.questionNumber <= 200)) continue;
  const k = `${q.committeeId}|${q.sourceFile}|${q.examYear}`;
  if (!by.has(k)) by.set(k, new Map());
  if (!by.get(k)!.has(q.questionNumber)) by.get(k)!.set(q.questionNumber, q);
}
const exams = [...by.values()].map((m) => [...m.values()]).filter((qs) => qs.length >= 30 && new Set(qs.map((q) => q.discipline)).size >= 3);
const ids = new Set(exams.flat().map((q) => q.id));
const eng = await createRecallEngine(root, { pastQuestions: past, excludeIds: ids });
let seed = 7;
const rnd = () => ((seed = (seed * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff);
// Öğrenci tarzı: kökten 4–7 içerik sözcüğü, aksansız
const recall = (stem: string) => {
  const w = fold(stem).split(' ').filter((x) => x.length >= 4);
  const start = Math.floor(rnd() * Math.max(1, w.length - 6));
  return w.slice(start, start + 4 + Math.floor(rnd() * 4)).join(' ');
};
const cases = exams.flatMap((qs) => qs.map((q) => ({ q, text: recall(q.stem), known: qs.filter((t) => t !== q && rnd() < 0.2).map((t) => ({ number: t.questionNumber, ders: t.discipline })) })));
console.log(`${exams.length} sınav, ${cases.length} soru`);
for (const w of [0, 0.15, 0.3, 0.5, 0.8]) {
  CLASSIFY.numberPrior = w;
  let hit = 0, withPrior = 0, hitPrior = 0;
  for (const c of cases) {
    const prior = numberDersPrior(c.known, c.q.questionNumber);
    const a = eng.analyze(c.text, { committeeId: c.q.committeeId, dersPrior: prior });
    const ok = a.ders[0]?.name === c.q.discipline;
    if (ok) hit++;
    if (prior) { withPrior++; if (ok) hitPrior++; }
  }
  console.log(`ağırlık ${w}: ders isabeti ${(100 * hit / cases.length).toFixed(1)}% · ön bilgisi olanlarda ${(100 * hitPrior / Math.max(1, withPrior)).toFixed(1)}% (${withPrior})`);
}
process.exit(0);
