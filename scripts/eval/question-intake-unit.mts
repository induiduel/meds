// Soru girişi ayrıştırıcısının kod denetimleri (LLM yok). Çalıştır: npx tsx scripts/eval/question-intake-unit.mts
import { letteredOptions, maskPersonal, normalizationOk, sameTerm, evidenceOk, fold, capConfidence, splitUnits, applyIntakeToQuestion } from '../../src/services/questionIntake.ts';
let fail = 0;
const eq = (name: string, got: any, want: any) => { const ok = JSON.stringify(got) === JSON.stringify(want); if (!ok) { fail++; console.log('✗', name, '\n   got ', JSON.stringify(got), '\n   want', JSON.stringify(want)); } else console.log('✓', name); };
eq('harfli şıklar', letteredOptions('A) koagulatif nekroz C) kazeoz nekroz gerisini hatirlamiyom').map(o => [o.harf, o.metin]), [['A', 'koagulatif nekroz'], ['C', 'kazeoz nekroz']]);
eq('satır şıkları', letteredOptions('kök\nA) E. coli\nD) Proteus').map(o => [o.harf, o.metin]), [['A', 'E. coli'], ['D', 'Proteus']]);
eq('hepatit b. kısaltma şık değil', letteredOptions('hepatit b. sorusu vardı').length, 0);
eq('cümle içi harf yok', letteredOptions('vitamin a eksikliği ve d vitamini').length, 0);
eq('telefon+ad maskesi', maskPersonal('ben Ayşe 0555 123 45 67, mail a@b.com', 'Ayşe Yılmaz'), 'ben [KİŞİSEL] [KİŞİSEL], mail [KİŞİSEL]');
eq('soru no maskelenmez', maskPersonal('12 de sifiliz, 30 da down'), '12 de sifiliz, 30 da down');
eq('ceftriakson~seftriakson', sameTerm(fold('seftriakson'), fold('ceftriakson')), true);
eq('metoprolol≠metoklopramid', sameTerm('metoprolol', 'metoklopramid'), false);
eq('propranolol≠metoprolol', normalizationOk('Metoprolol', 'propranolol'), false);
eq('sefazolin≠seftriakson', normalizationOk('Seftriakson', 'sefazolin'), false);
eq('kongo→Kongo kırmızısı', normalizationOk('Kongo kırmızısı', 'kongo muydu'), true);
eq('zn→Ziehl-Neelsen', normalizationOk('Ziehl-Neelsen boyası', 'zn boyasi'), true);
eq('kongo→Prusya mavisi reddi', normalizationOk('Prusya mavisi', 'kongo'), false);
const c = fold('abi kongo muydu neydi ben onu isaretledim'); const ct = new Set(c.split(' '));
eq('kanıt var', evidenceOk('kongo muydu', c, ct), true);
eq('uydurma kanıt', evidenceOk('kongo kirmizisi', c, ct), false);
eq('tek harf kanıt değil', evidenceOk('b', c, ct), false);
eq('tereddüt sınırı', capConfidence(0.9, 'kongo muydu neydi', ''), 0.5);
eq('eminim sınırı', capConfidence(1, 'kesin E', ''), 0.8);
// Birim ayırma ve soru kaydına geri yazma
const U = (no: number | null, ders = 'Tıbbi Patoloji', konu: string | null = 'Hücre Hasarı ve Nekroz - I'): any => ({
  metin_parcasi: '', ders_tahmini: ders, ders_guveni: 0.9, ikincil_ders: null, karisma_notu: null, kurul_disi_suphesi: false,
  konu_tahmini: konu, soru_no: no, soru_tipi: 'mekanizma', uzman: 'patoloji', soru_odagi: null, soru_koku_bulgulari: [],
  hatirlanan_siklar: [{ harf: 'B', metin: 'Kazeöz nekroz', kanit: 'b', guven: 0.5 }], iddia_edilen_cevap: null,
  olumsuz_soru_koku_ihtimali: 0.9, olumsuz_gerekce: '', tibbi_varliklar: [{ ad: 'Kazeöz nekroz', tip: 'bulgu' }], eksikler: [], model: 't',
});
const P = (units: any[]): any => ({ girdiId: 'g1', createdAt: '2026-10-12T00:00:00Z', promptVersion: 'v', status: 'ayristirildi', cacheKey: '', maskedText: '', enjeksiyon_suphesi: false, units, models: [], validationErrors: [] });
const R = (o: any = {}): any => ({ id: 'g1', createdAt: '', committeeId: 'donem3-kurul1', source: 't', rawText: 'x', questionId: 'q1', ...o });
eq('numaralı: başka numaralı birim ayrılır', splitUnits(R({ questionNumber: 12 }), P([U(null), U(30)])), { attached: [0], orphan: [1] });
eq('numarasız: ilk birim bağlanır', splitUnits(R(), P([U(null), U(30)])), { attached: [0], orphan: [1] });
eq('soru kimliği yoksa hepsi ayrı', splitUnits(R({ questionId: undefined }), P([U(null)])), { attached: [], orphan: [0] });
eq('tek birim, numarası farklı da olsa numarasız soruya bağlanır', splitUnits(R(), P([U(30)])), { attached: [0], orphan: [] });
const q0 = { id: 'q1', discipline: 'Belirtilmedi', topic: 'Tıbbi Patoloji Hatırlanan Soru', tags: ['x'], fragments: [{ text: 'öğrenci metni' }] };
const q1 = applyIntakeToQuestion(q0, R(), P([U(null)]), [U(null)]);
eq('genel ders ve konu doldurulur', [q1.discipline, q1.topic], ['Tıbbi Patoloji', 'Hücre Hasarı ve Nekroz - I']);
eq('öğrenci parçası değişmez', q1.fragments, q0.fragments);
eq('olumsuz kök etiketi', q1.tags.includes('olumsuz-kok-olasi'), true);
const q2 = applyIntakeToQuestion({ ...q0, discipline: 'Tıbbi Genetik' }, R(), P([U(null)]), [U(null)]);
eq('seçilmiş ders ezilmez, uyuşmazlık işaretlenir', [q2.discipline, q2.tags.includes('ders-uyusmazligi')], ['Tıbbi Genetik', true]);
const q3 = applyIntakeToQuestion(q1, R(), P([U(null)]), [U(null)]);
eq('aynı girdi iki kez yazılınca çoğalmaz', q3.intake.girdiler.length, 1);
console.log(fail ? `${fail} HATA` : 'hepsi geçti');
process.exit(fail ? 1 : 0);
