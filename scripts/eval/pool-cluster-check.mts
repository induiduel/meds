// Havuz kümelemesini gerçek data/questions.json üzerinde (yapay zekâsız) dener; küme üyelerini, taslağı ve süreyi yazar.
// Çalıştır: npx tsx scripts/eval/pool-cluster-check.mts
import fs from 'fs';
import { questionToItems, buildProposal } from '../../src/services/poolClusterService.ts';
import { createRecallEngine } from '../../src/services/recall/engine.ts';
import { clusterRecall, draftCluster } from '../../src/services/recall/cluster.ts';
const root = new URL('../../', import.meta.url).pathname;
const d = JSON.parse(fs.readFileSync(root + 'data/questions.json', 'utf8'));
const qs: any[] = Array.isArray(d) ? d : d.questions;
const eng = await createRecallEngine(root);
const t0 = Date.now();
const pairs = qs.filter((q) => !q.isMerged).map((q) => questionToItems(q, eng)).filter(Boolean) as NonNullable<ReturnType<typeof questionToItems>>[];
const t1 = Date.now();
const groups = (await clusterRecall(pairs.map((p) => p.recall), eng)).filter((g) => g.members.length >= 2);
const t2 = Date.now();
const pool = new Map(pairs.map((p) => [p.recall.key, p.pool]));
console.log(`öge ${pairs.length}, gürültü ${pairs.filter((p) => p.recall.a.isNoise).length}, küme ${groups.length}, özellik ${t1 - t0} ms, kümeleme ${t2 - t1} ms`);
for (const g of groups) {
  const p = buildProposal(g.members.map((m) => pool.get(m.key)!), g.cohesion);
  const dr = draftCluster(g.members, eng);
  console.log(`\n■ ${p.clusterTitle} | ${p.committeeId} ${p.discipline} | no=${p.questionNumber ?? '-'} | uyum ${p.cohesion} | ortak: ${p.sharedTerms.join(', ')}`);
  console.log(`  taslak: ${dr.stem}${dr.bankMatch ? `\n  çıkmış: ${dr.bankMatch.stem.slice(0, 120)} (${dr.bankMatch.score})` : ''}`);
  for (const m of g.members) console.log(`   - ${m.key.slice(0, 48)} no=${m.number ?? '-'} [${m.a.terms.slice(0, 5).join(', ')}] ${m.text.replace(/\s+/g, ' ').slice(0, 90)}`);
}
