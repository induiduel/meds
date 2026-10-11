// Havuz kümelemesini gerçek data/questions.json üzerinde (yapay zekâsız) dener; küme üyelerini ve süreyi yazar.
// Çalıştır: npx tsx scripts/eval/pool-cluster-check.mts
import fs from 'fs';
import { questionToItem, clusterItems, buildProposal, matchTerms } from '../../src/services/poolClusterService.ts';
const root = new URL('../../', import.meta.url).pathname;
const d = JSON.parse(fs.readFileSync(root + 'data/questions.json', 'utf8'));
const qs: any[] = Array.isArray(d) ? d : d.questions;
const mod: any = await import('../../src/services/poolClusterService.ts');
// terim dizinini servis üzerinden yükle
const idx = await (mod as any).__loadTermIndexForTest?.(root);
const t0 = Date.now();
const items = qs.map((q) => questionToItem(q, idx)).filter(Boolean) as any[];
const t1 = Date.now();
const groups = await clusterItems(items);
const t2 = Date.now();
console.log(`öge ${items.length}, terimli öge ${items.filter((i) => i.terms.length).length}, küme ${groups.length}, özellik ${t1 - t0} ms, kümeleme ${t2 - t1} ms`);
for (const g of groups) {
  const p = buildProposal(g.members, g.cohesion);
  console.log(`\n■ ${p.clusterTitle} | ${p.committeeId} ${p.discipline} | no=${p.questionNumber ?? '-'} | uyum ${p.cohesion} | ortak: ${p.sharedTerms.join(', ')}`);
  for (const m of g.members) console.log(`   - ${m.key.slice(0, 48)} no=${m.number ?? '-'} [${m.terms.slice(0, 5).join(', ')}] ${m.text.replace(/\s+/g, ' ').slice(0, 90)}`);
}
