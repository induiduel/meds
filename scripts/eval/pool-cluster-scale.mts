// Ölçek: N sentetik öge ile analiz + kümeleme süresi ve olay döngüsünün en uzun kilitlenmesi.
// Çalıştır: N=2000 npx tsx scripts/eval/pool-cluster-scale.mts
import { questionToItems } from '../../src/services/poolClusterService.ts';
import { createRecallEngine } from '../../src/services/recall/engine.ts';
import { clusterRecall } from '../../src/services/recall/cluster.ts';
const root = new URL('../../', import.meta.url).pathname;
const eng = await createRecallEngine(root);
const N = Number(process.env.N || 2000);
const words = 'amiloid kongo kırmızısı elma yeşili kazeöz nekroz tüberküloz granülom sifiliz şankr treponema down sendromu trizomi ense saydamlığı siklosporin kalsinörin takrolimus nötrofil vazodilatasyon ödem tromboz emboli infarkt hipertrofi atrofi metaplazi displazi apoptoz karyoreksis piknoz'.split(' ');
const rnd = (k: number) => Array.from({ length: k }, () => words[Math.floor(Math.random() * words.length)]).join(' ');
const disc = ['Tıbbi Patoloji', 'Tıbbi Genetik', 'Enfeksiyon Hastalıkları', 'Tıbbi Farmakoloji'];
const qs = Array.from({ length: N }, (_, i) => ({ id: `x${i}`, committeeId: `donem3-kurul${1 + (i % 2)}`, discipline: disc[i % 4], questionNumber: i % 3 ? 0 : 1 + (i % 100), isUnassignedNumber: !!(i % 3), fragments: [{ text: rnd(8), type: 'stem' }], options: [], createdAt: '' }));
const t0 = performance.now();
const items = qs.map((q) => questionToItems(q as any, eng)!.recall);
const t1 = performance.now();
let maxLag = 0;
let last = performance.now();
const mon = setInterval(() => { const now = performance.now(); maxLag = Math.max(maxLag, now - last - 5); last = now; }, 5);
const groups = await clusterRecall(items, eng);
const t2 = performance.now();
clearInterval(mon);
console.log(`N=${N}: analiz ${(t1 - t0).toFixed(0)} ms, kümeleme ${(t2 - t1).toFixed(0)} ms, küme ${groups.filter((g) => g.members.length > 1).length}, en uzun olay döngüsü kilidi ${maxLag.toFixed(0)} ms`);
process.exit(0);
