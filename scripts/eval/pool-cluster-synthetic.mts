// Kümeleme doğruluğu: aynı soruyu farklı sözlerle hatırlayan parçalar bir araya gelmeli, aynı konudan farklı
// sorular ve ilgisiz parçalar ayrı kalmalı. LLM yok. Çalıştır: npx tsx scripts/eval/pool-cluster-synthetic.mts
import { questionToItems } from '../../src/services/poolClusterService.ts';
import { createRecallEngine } from '../../src/services/recall/engine.ts';
import { clusterRecall, pairFeatures, pairProb } from '../../src/services/recall/cluster.ts';
const root = new URL('../../', import.meta.url).pathname;
const eng = await createRecallEngine(root);
type S = { g: string; d: string; t: string; o?: [string, string][]; n?: number };
const P = 'Tıbbi Patoloji', G = 'Tıbbi Genetik', E = 'Enfeksiyon Hastalıkları', F = 'Tıbbi Farmakoloji';
const data: S[] = [
  // amiloid boyama sorusu
  { g: 'amiloid-boya', d: P, t: 'amiloid birikimi hangi boya ile gösterilir kongo kırmızısı polarize ışıkta elma yeşili' },
  { g: 'amiloid-boya', d: P, t: 'elma yeşili çift kırılım veren birikim sorusu vardı, kongo kırmızısı', o: [['B', 'Kongo kırmızısı']] },
  { g: 'amiloid-boya', d: P, t: 'amiloidoz boyası', o: [['B', 'Kongo kırmızısı'], ['A', 'PAS']] },
  // aynı konu farklı soru: amiloid tipi
  { g: 'amiloid-tip', d: P, t: 'kronik inflamasyonda görülen sekonder amiloidozda biriken protein AA amiloid serum amiloid A' },
  { g: 'amiloid-tip', d: P, t: 'romatoid artritli hastada AA tipi amiloid birikimi hangi proteinden köken alır' },
  // nekroz tipi (tbc)
  { g: 'kazeoz', d: P, t: 'tüberkülozda görülen nekroz tipi kazeöz nekroz', o: [['A', 'Koagülatif nekroz'], ['C', 'Kazeöz nekroz']] },
  { g: 'kazeoz', d: P, t: 'tbc granülomunda ortadaki peynirimsi nekroz hangisiydi', o: [['C', 'Kazeöz nekroz']] },
  // down
  { g: 'down-nt', d: G, t: 'birinci trimester taramada ense saydamlığı artışı ve burun kemiği yokluğu down sendromu trizomi 21' },
  { g: 'down-nt', d: G, t: 'ense kalınlığı artmış fetüs, en olası kromozom anomalisi trizomi 21' },
  // sifiliz
  { g: 'sifiliz', d: E, t: 'primer sifilizde ağrısız şankr, etken treponema pallidum' },
  { g: 'sifiliz', d: E, t: 'ağrısız genital ülser sert şankr sifiliz sorusu', o: [['D', 'Treponema pallidum']] },
  // gonore (aynı ders farklı soru)
  { g: 'gonore', d: E, t: 'gonore tedavisinde seftriakson ve klamidya için doksisiklin' },
  // farmakoloji
  { g: 'kalsinorin', d: F, t: 'siklosporin etki mekanizması kalsinörin inhibisyonu takrolimus' },
  { g: 'kalsinorin', d: F, t: 'takrolimus ve siklosporin hangi enzimi inhibe eder kalsinörin' },
  // aynı ilaç, farklı soru (yan etki) — kalsinörin kümesine girmemeli
  { g: 'siklo-yanetki', d: F, t: 'siklosporinin en önemli yan etkisi nefrotoksisite ve hipertansiyon, diş eti hiperplazisi' },
  // farklı ders aynı kelime: ayrı kalmalı
  { g: 'down-pato', d: P, t: 'down sendromlu çocukta görülen lösemi tipi akut megakaryoblastik' },
  // tek kelimelik kısa hatıra
  { g: 'sifiliz', d: E, t: 'sifiliz' },
  // numaralı ayrı sorular: aynı konu olsa da birleşmemeli
  { g: 'n12', d: P, t: 'akut inflamasyonda nötrofil göçü', n: 12 },
  { g: 'n13', d: P, t: 'akut inflamasyonda vazodilatasyon nötrofil', n: 13 },
  // numaralı + numarasız aynı soru: birleşmeli
  { g: 'n12', d: P, t: 'nötrofil göçü akut inflamasyon sorusu 12 mi neydi' },
];
const qs = data.map((x, i) => ({
  id: `s${i}-${x.g}`, committeeId: 'donem3-kurul1', discipline: x.d, topic: `${x.d} Hatırlanan Soru`,
  questionNumber: x.n || 0, isUnassignedNumber: !x.n, fragments: [{ text: x.t, type: 'stem' }],
  options: (x.o || []).map(([k, t]) => ({ key: k, text: t })), createdAt: `2026-10-12T00:00:${String(i).padStart(2, '0')}Z`,
}));
const items = qs.map((q) => questionToItems(q as any, eng)!.recall);
const t0 = performance.now();
const groups = (await clusterRecall(items, eng)).filter((g) => g.members.length > 1);
const ms = performance.now() - t0;
const label = (k: string) => k.split('-').slice(1).join('-');
let tp = 0, fp = 0, fn = 0;
const clusterOf = new Map<string, number>();
groups.forEach((g, i) => g.members.forEach((m: any) => clusterOf.set(m.key, i)));
for (let i = 0; i < items.length; i++) for (let j = 0; j < i; j++) {
  const same = label(items[i].key) === label(items[j].key);
  const together = clusterOf.has(items[i].key) && clusterOf.get(items[i].key) === clusterOf.get(items[j].key);
  if (same && together) tp++; else if (!same && together) fp++; else if (same && !together) fn++;
}
for (const g of groups) console.log(`■ uyum ${g.cohesion.toFixed(2)}: ${g.members.map((m: any) => label(m.key)).join(', ')}`);
const prec = tp / Math.max(1, tp + fp), rec = tp / Math.max(1, tp + fn);
console.log(`çift kesinlik ${(prec * 100).toFixed(0)}% · duyarlılık ${(rec * 100).toFixed(0)}% · yanlış birleşme ${fp} · ${ms.toFixed(1)} ms`);
if (process.env.DEBUG) {
  for (let i = 0; i < items.length; i++) for (let j = 0; j < i; j++) {
    const p = pairProb(pairFeatures(items[i], items[j], eng));
    if (p > 0.3 || label(items[i].key) === label(items[j].key)) console.log(`${p.toFixed(2)} ${label(items[i].key)} ~ ${label(items[j].key)}  [${items[i].a.terms.join(',')}] [${items[j].a.terms.join(',')}]`);
  }
}
// Bilinen hata (hatirlama-v1): "siklosporin mekanizması" ↔ "siklosporin yan etkisi" birleşiyor (tek ilaç adı + benzer
// sözcükler). Asıl ölçüm scripts/eval/recall-engine.mts; bu betik yalnız gözle kontrol, kesinlik %80'in altına inerse hata verir.
process.exit(prec < 0.8 ? 1 : 0);
