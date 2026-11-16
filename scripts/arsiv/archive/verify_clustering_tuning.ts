import {
  calculateDraftCompatibility,
  clusterDraftsForCommittee,
  clearBlockedPairs,
  pairKey,
  CLUSTER_PRESETS,
} from '../src/services/draftClusteringService';

const mk = (over: Record<string, unknown> = {}) => ({
  id: `t-${Math.random().toString(36).slice(2, 7)}`,
  committeeId: 'donem3-kurul1',
  questionNumber: 0,
  discipline: 'Belirtilmedi',
  topic: '',
  status: 'gathering',
  fragments: [],
  options: [],
  tags: [],
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
  ...over,
} as any);

const frag = (text: string, author = 'Ogrenci') => ({ id: `f-${Math.random()}`, author, text, type: 'stem', timestamp: new Date().toISOString(), upvotes: 1 });

// 1. Aynı kavram, farklı soru (zayıf kanıt) -> auto_merge OLMAMALI
const downA = mk({ questionNumber: 12, discipline: 'Tıbbi Genetik', fragments: [frag('Down sendromunda fetal ultrasonda ense kalınlığı artışı ve kalp anomalisi görülür.')], options: [{ key: 'A', text: 'Trizomi 21', upvotes: 1 }] });
const downB = mk({ questionNumber: 34, discipline: 'Tıbbi Genetik', fragments: [frag('Down sendromlu hastada Alzheimer erken başlar, lösemi riski artmıştır.')], options: [{ key: 'A', text: 'APP geni', upvotes: 1 }] });
const r1 = calculateDraftCompatibility(downA, downB);
console.log('TEST1 kavram-tekeli:', r1.score, r1.recommendation, '|', r1.reasons.slice(0, 2).join(' / ').slice(0, 120));
console.log(r1.recommendation === 'auto_merge' ? '  FAIL: otomatik birleşmemeli' : '  OK');

// 2. Güçlü eşleşme (aynı no + ortak şıklar) -> auto_merge OLMALI
const s1 = mk({ questionNumber: 14, discipline: 'Farmakoloji', fragments: [frag('Hipertansiyon hastasında ACE inhibitörü sonrası inatçı kuru öksürük gelişti.')], options: [{ key: 'A', text: 'Bradikinin birikimi', upvotes: 3 }, { key: 'B', text: 'Renin artışı', upvotes: 1 }] });
const s2 = mk({ questionNumber: 14, discipline: 'Farmakoloji', fragments: [frag('ACE inhibitörü kullanan hastada gece uyandıran kuru öksürük, bradikinin yıkımı engellenir.')], options: [{ key: 'A', text: 'Bradikinin birikimi', upvotes: 2 }, { key: 'B', text: 'Renin artışı', upvotes: 1 }] });
const r2 = calculateDraftCompatibility(s1, s2);
console.log('TEST2 guclu-eslesme:', r2.score, r2.recommendation);
console.log(r2.recommendation === 'auto_merge' ? '  OK' : '  FAIL: otomatik birleşmeli');

// 3. İki kısa taslak (ders aynı, kanıt yok) -> distinct OLMALI
const k1 = mk({ discipline: 'Patoloji', fragments: [frag('Hocam MI sordu.')], options: [] });
const k2 = mk({ discipline: 'Patoloji', fragments: [frag('Bence nekroz vardı.')], options: [] });
const r3 = calculateDraftCompatibility(k1, k2);
console.log('TEST3 kisa-taslak:', r3.score, r3.recommendation);
console.log(r3.recommendation === 'distinct' ? '  OK' : '  FAIL: ayrık olmalı');

// 4. Engellenmiş çift -> kümelenmemeli (gerçek yol: tuning.blocked ile)
clearBlockedPairs();
const blocked = new Set([pairKey(s1.id, s2.id)]);
const sumBlocked = clusterDraftsForCommittee([s1, s2] as any, 'donem3-kurul1', { ...CLUSTER_PRESETS.balanced, blocked });
const together = sumBlocked.clusters.some((c) => {
  const ids = [c.anchorQuestion.id, ...c.satelliteDrafts.map((s) => s.question.id)];
  return ids.includes(s1.id) && ids.includes(s2.id);
});
console.log('TEST4 engelli-cift kumede-birlikte:', together);
console.log(!together ? '  OK' : '  FAIL');
clearBlockedPairs();

// 5. Hassasiyet: sıkı modda TEST2 skoru auto eşiğin altında mı üstünde mi raporla
const r5 = calculateDraftCompatibility(s1, s2, { ...CLUSTER_PRESETS.strict });
console.log('TEST5 siki-mod skoru:', r5.score, r5.recommendation, '(esik 80)');

// 6. Kümeleme: 3 Down-vari + 2 ACE -> ACE kümesi hazır, Down'lar daginik/in incelemede olmalı
const d3 = mk({ questionNumber: 45, discipline: 'Tıbbi Genetik', fragments: [frag('Down sendromunda atrioventriküler septal defekt en sık kalp anomalisidir.')], options: [] });
const sum = clusterDraftsForCommittee([downA, downB, d3, s1, s2] as any, 'donem3-kurul1');
console.log('TEST6 kumeler:', sum.clusters.map((c) => `${c.status}%${c.overallConfidence}[${c.satelliteDrafts.length + 1}]`).join(' '), 'muglak=', sum.vagueDraftsCount);
const aceCluster = sum.clusters.find((c) => [c.anchorQuestion.id, ...c.satelliteDrafts.map((s) => s.question.id)].includes(s1.id));
console.log(aceCluster && aceCluster.status === 'ready_to_merge' ? '  OK: ACE hazır küme' : '  BILGI: ACE küme durumu=' + aceCluster?.status);
process.exit(0);
