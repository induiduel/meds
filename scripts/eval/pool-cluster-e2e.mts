// Uçtan uca (gerçek ücretsiz Gemini, geçici klasör; gerçek veriye dokunmaz): girdi → ayrıştırma → soruya geri yazma → kümeleme → AI birleştirme.
// Çalıştır: npx tsx scripts/eval/pool-cluster-e2e.mts
import dotenv from 'dotenv';
dotenv.config({ path: '/home/indu/medsor/meds/.env', quiet: true } as any);
process.env.MEDS_INTAKE_GROQ_FALLBACK = '0';
import fs from 'fs';
const { createQuestionIntake, applyIntakeToQuestion } = await import('../../src/services/questionIntake.ts');
const { createPoolClusterService } = await import('../../src/services/poolClusterService.ts');
const dir = fs.mkdtempSync('/tmp/claude-1000/-home-indu-medsor/981ed072-f2aa-4b06-8d5d-743f9f966cb0/scratchpad/e2e-');
const root = '/home/indu/medsor/meds';
const db: any[] = [
  { id: 'qA', committeeId: 'donem3-kurul1', questionNumber: 0, isUnassignedNumber: true, discipline: 'Tıbbi Patoloji', topic: 'Tıbbi Patoloji Hatırlanan Soru', fragments: [{ type: 'stem', text: 'amiloid birikimi elma yeşili b şıkkı kongo muydu' }], options: [], createdAt: '2026-10-12T00:00:01Z' },
  { id: 'qB', committeeId: 'donem3-kurul1', questionNumber: 0, isUnassignedNumber: true, discipline: 'Belirtilmedi', topic: 'Soru #0', fragments: [{ type: 'stem', text: 'polarize ışıkta elma yeşili çift kırılım veren madde, kongo kırmızısı ile boyanır' }], options: [{ key: 'B', text: 'Kongo kırmızısı' }], createdAt: '2026-10-12T00:00:02Z' },
];
const qi = createQuestionIntake(dir, root, {
  getQuestions: () => db,
  writeback: (raw: any, parse: any, units: any) => { const i = db.findIndex((q) => q.id === raw.questionId); if (i < 0) return 'retry'; db[i] = applyIntakeToQuestion(db[i], raw, parse, units); return 'ok'; },
});
const file = dir + '/clusters.json';
const pc = createPoolClusterService({ rootDir: root, file, getQuestions: () => db, getOrphanUnits: () => qi.orphanUnits() });
qi.submit({ committeeId: 'donem3-kurul1', questionId: 'qA', source: 't', rawText: db[0].fragments[0].text + '. bi de 30 da down sendromu trizomi 21 sorusu vardı ense saydamlığı' });
qi.submit({ committeeId: 'donem3-kurul1', questionId: 'qB', source: 't', rawText: db[1].fragments[0].text, formOptions: [{ key: 'B', text: 'Kongo kırmızısı' }] });
qi.submit({ committeeId: 'donem3-kurul1', source: 't', rawText: 'down sendromlu fetüste birinci trimester ense kalınlığı artmıştı trizomi 21' });
for (let i = 0; i < 90; i++) {
  await new Promise((r) => setTimeout(r, 2000));
  const pending = db.filter((q) => !q.intake).length;
  if (!pending && qi.orphanUnits().length >= 2) break;
}
console.log('geri yazma:', db.map((q) => [q.id, q.discipline, q.topic, q.intake?.ozet?.varliklar?.slice(0, 4)]));
console.log('sahipsiz birimler:', qi.orphanUnits().map((o: any) => [o.unit.soru_no, o.unit.ders_tahmini, o.unit.metin_parcasi.slice(0, 50)]));
process.env.MEDS_INTAKE_GROQ_FALLBACK = '0';
await pc.runNow();
for (const c of pc.list()) console.log(`■ ${c.clusterTitle} | no=${c.questionNumber} | üyeler: ${[...c.sourceQuestionIds, ...c.sourceIntakeUnits].join(', ')} | şıklar: ${c.mergedOptions.map((o: any) => `${o.key}:${o.text}`).join(' ')}`);
console.log('durum', pc.status());
// AI birleştirmesini bekle
for (let i = 0; i < 40 && pc.status().aiQueue > 0; i++) await new Promise((r) => setTimeout(r, 3000));
for (const c of pc.list()) console.log(`AI ${c.aiMerged}: ${c.mergedStem}\n   ${c.mergedOptions.map((o: any) => `${o.key}:${o.text}[${o.source}]`).join(' ')} | öneri ${c.aiAnswerSuggestion} | kaynak ${c.sources?.length}`);
process.exit(0);
