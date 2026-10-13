// "Soru ekle" anlık eşleşme ölçümü: mesajlar sırayla gelir; her yeni mesaj için havuzdaki önceki kayıtlar arasından
// aynı soruyu anlatan taslak önerilir. Eski tarayıcı algoritması (draftClusteringService.findRealtimeMatchingDrafts +
// medicalPredictorService ders tahmini) ile yeni motor (recall/) aynı akışta karşılaştırılır.
//   npx tsx scripts/eval/recall-realtime.mts [--split test|dev|all]
import fs from 'fs';
import { createRecallEngine } from '../../src/services/recall/engine.ts';
import { pairFeatures, pairProb, type RecallItem } from '../../src/services/recall/cluster.ts';
import { findRealtimeMatchingDrafts, loadMedicalConcepts } from '../../src/services/draftClusteringService.ts';
import { predictCommitteeAndDiscipline } from '../../src/services/medicalPredictorService.ts';

const root = new URL('../../', import.meta.url).pathname;
const DS = `${root}scripts/eval/datasets/hatirlama`;
const split = (() => { const i = process.argv.indexOf('--split'); return i > 0 ? process.argv[i + 1] : 'test'; })();
const ks = split === 'dev' ? [1, 2, 3] : split === 'all' ? [1, 2, 3, 4, 5, 6] : [4, 5, 6];
const targets = new Map<string, any>();
for (let k = 1; k <= 6; k++) for (const t of JSON.parse(fs.readFileSync(`${DS}/hedef_k${k}.json`, 'utf8'))) targets.set(t.id, t);
await loadMedicalConcepts().catch(() => {});
const eng = await createRecallEngine(root, { excludeIds: new Set(targets.keys()) });
const MIN_P = 0.6;

const res = { old: { shown: 0, top1: 0, any: 0, possible: 0, falseAlarm: 0, ms: 0 }, neu: { shown: 0, top1: 0, any: 0, possible: 0, falseAlarm: 0, ms: 0 } };
const ders = { old: 0, neu: 0, n: 0 };
for (const k of ks) {
  const msgs = JSON.parse(fs.readFileSync(`${DS}/hatirlama_k${k}.json`, 'utf8')).filter((m: any) => m.soru_idler.length === 1);
  const cid = `donem3-kurul${k}`;
  const poolOld: any[] = [];
  const poolNew: (RecallItem & { gold: string })[] = [];
  for (const m of msgs) {
    const gold = m.soru_idler[0];
    const possible = poolNew.some((p) => p.gold === gold);
    // eski
    let t0 = performance.now();
    const om = findRealtimeMatchingDrafts({ committeeId: cid, discipline: 'Belirtilmedi', topic: 'Belirtilmedi Hatırlanan Soru', text: m.metin }, poolOld, 35, 4, false);
    res.old.ms += performance.now() - t0;
    // yeni
    t0 = performance.now();
    const a = eng.analyze(m.metin, { committeeId: cid });
    const me: RecallItem = { key: m.mid, committeeId: cid, createdAt: m.mid, number: a.number, text: m.metin, a };
    const nm = a.isNoise ? [] : poolNew.map((p) => ({ p, s: pairProb(pairFeatures(me, p, eng)) })).filter((x) => x.s >= MIN_P).sort((x, y) => y.s - x.s).slice(0, 4);
    res.neu.ms += performance.now() - t0;
    for (const [r, list] of [[res.old, om.map((x: any) => x.question.gold)], [res.neu, nm.map((x) => x.p.gold)]] as const) {
      if (possible) r.possible++;
      if (list.length) {
        r.shown++;
        if (list[0] === gold) r.top1++;
        if (list.includes(gold)) r.any++;
        else r.falseAlarm++;
      }
    }
    // ders tahmini
    const t = targets.get(gold);
    ders.n++;
    if (predictCommitteeAndDiscipline(m.metin, cid).predictedDiscipline?.discipline === t.discipline) ders.old++;
    if (a.ders[0]?.name === t.discipline) ders.neu++;
    poolOld.push({ id: m.mid, gold, committeeId: cid, questionNumber: 0, discipline: 'Belirtilmedi', topic: 'Belirtilmedi Hatırlanan Soru', status: 'gathering', fragments: [{ id: 'f', author: 'x', text: m.metin, type: 'stem', timestamp: '', upvotes: 0 }], options: [], tags: [], createdAt: m.mid, updatedAt: m.mid });
    poolNew.push({ ...me, gold });
  }
}
const pct = (a: number, b: number) => `${((100 * a) / Math.max(1, b)).toFixed(1)}%`;
for (const [name, r] of [['ESKİ (tarayıcı)', res.old], ['YENİ (motor)', res.neu]] as const) {
  console.log(`${name}: öneri gösterilen ${r.shown} · ilk öneri doğru ${pct(r.top1, r.shown)} · listede doğru var ${pct(r.any, r.shown)} · yanlış alarm ${r.falseAlarm} · havuzda eşi olanların yakalanması ${pct(r.any, r.possible)} (${r.possible}) · ${(r.ms / ders.n).toFixed(2)} ms/mesaj`);
}
console.log(`Ders tahmini: eski ${pct(ders.old, ders.n)} · yeni ${pct(ders.neu, ders.n)} (${ders.n} mesaj)`);
process.exit(0);
