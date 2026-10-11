/**
 * Sorgu zekâsı değerlendirmesi: yapay yazım hataları (silme/ekleme/ikame/yer değiştirme/aksansız),
 * gerçekçi örnek sorgular, tamamlama ve gecikme ölçümü.
 *   npx tsx scripts/search/eval-query-intel.mts
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { QueryIntelEngine, decodeBins } from '../../src/services/queryIntel/engine.ts';
import { fold } from '../../src/services/queryIntel/core.ts';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
let t = performance.now();
const pack = JSON.parse(fs.readFileSync(path.join(root, 'data/search/query-intel.json'), 'utf-8'));
const bins = decodeBins(new Uint8Array(fs.readFileSync(path.join(root, 'data/search/query-intel.bin'))));
const eng = new QueryIntelEngine(pack, bins);
console.log(`yükleme ${(performance.now() - t).toFixed(0)} ms, heap ${(process.memoryUsage().heapUsed / 1e6).toFixed(0)} MB`);

// --- 1) yapay hata seti: sık tıbbi sözcükler (≥6 harf, df ≥ 30)
let seed = 7;
const rnd = () => ((seed = (seed * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff);
const pool = eng.words.map((w, i) => ({ w, i })).filter(({ w, i }) => w.length >= 6 && eng.freq[i] >= 30 && /^\p{Ll}+$/u.test(w));
const ALPHA = 'abcçdefgğhıijklmnoöprsştuüvyz';
const corrupt = (w: string): string => {
  const k = Math.floor(rnd() * 4);
  const p = 1 + Math.floor(rnd() * (w.length - 2));
  if (k === 0) return w.slice(0, p) + w.slice(p + 1);
  if (k === 1) return w.slice(0, p) + ALPHA[Math.floor(rnd() * ALPHA.length)] + w.slice(p);
  if (k === 2) return w.slice(0, p) + ALPHA[Math.floor(rnd() * ALPHA.length)] + w.slice(p + 1);
  return w.slice(0, p) + w[p + 1] + w[p] + w.slice(p + 2);
};
let ok = 0, wrong = 0, none = 0, n = 0;
let ms = 0;
for (let j = 0; j < Number(process.env.N || 600); j++) {
  const { w } = pool[Math.floor(rnd() * pool.length)];
  const typo = corrupt(w);
  if (fold(typo) === fold(w) || eng.idOf(fold(typo)) >= 0 && eng.freq[eng.idOf(fold(typo))] >= 4) continue; // gerçek sözcüğe dönüştü
  n++;
  const t0 = performance.now();
  const r = eng.correct(typo);
  ms += performance.now() - t0;
  if (!r.text) none++;
  else if (fold(r.text) === fold(w)) ok++;
  else wrong++;
}
console.log(`yazım (tek hata, ${n} sözcük): doğru %${((ok / n) * 100).toFixed(1)} · yanlış %${((wrong / n) * 100).toFixed(1)} · öneri yok %${((none / n) * 100).toFixed(1)} · ort ${(ms / n).toFixed(2)} ms`);

// aksansız yazım
let ok2 = 0, n2 = 0;
for (const { w } of pool.filter((x) => /[çğıöşü]/.test(x.w)).slice(0, 400)) {
  n2++;
  const r = eng.correct(fold(w));
  if (r.text === w) ok2++;
}
console.log(`aksansız → Türkçe (${n2}): doğru %${((ok2 / n2) * 100).toFixed(1)}`);

// --- 2) örnek sorgular
const show = (q: string) => {
  const t0 = performance.now();
  const a = eng.analyze(q);
  const c = eng.complete(q, 5);
  const g = eng.completeSentence(q);
  const dt = performance.now() - t0;
  console.log(`\n» "${q}"  [${dt.toFixed(2)} ms]`);
  if (a.corrected) console.log(`  düzeltme: ${a.corrected}  (${a.changes.map((x) => `${x.from}→${x.to} ${x.conf}`).join(', ')})`);
  if (a.concepts.length) console.log(`  kavram: ${a.concepts.map((x) => `${x.label} [${x.type}${x.ref ? ' ' + x.ref.kind + ':' + x.ref.id : ''}]${x.viaAlias ? ' (takma)' : ''}`).join(' | ')}`);
  if (a.intent) console.log(`  niyet: ${a.intent}`);
  if (a.rewrites.length) console.log(`  yeniden yazım: ${a.rewrites.join(' | ')}`);
  const sl = a.slots.filter((x) => x.alts.length);
  if (sl.length) console.log(`  yuvalar: ${sl.map((x) => `${x.w}≈{${x.alts.join(',')}}`).join(' ')}`);
  console.log(`  öneri: ${c.map((s) => `${s.kind}:${s.value}`).join(' | ')}`);
  if (g) console.log(`  hayalet: «${q}${g}»`);
};
for (const q of [
  'böbrek tümörü', 'böbrek tümörlerinde tedavi', 'böbreğin tümörleri', 'karaciğer tümörü', 'renal neoplazm', 'kansızlığı olan hasta', 'yüksek tansiyon tedavisi', 'kansızlık tedavisi', 'kansizlik', 'nefrotk sendrm', 'bobrek tumoru', 'hipotiroidi belirtileri', 'nefrotiksendrom',
  'wilms', 'VHL', 'renal hüc', 'glomerül', 'akut poststreptokokal', 'ttp', 'aşağıdakilerden ', 'en sık görülen ',
  'nefrotik sendromda en sık', 'trombosit', 'tromboz', 'diyabetik nefropati tanısı', 'IgA nefropatis', 'polikistik böbr',
]) show(q);

// --- 3) gecikme: 2000 rastgele önek
const prefixes: string[] = [];
for (let j = 0; j < 2000; j++) { const { w } = pool[Math.floor(rnd() * pool.length)]; prefixes.push(w.slice(0, 2 + Math.floor(rnd() * (w.length - 2)))); }
t = performance.now();
for (const p of prefixes) eng.complete(p, 8);
const per = (performance.now() - t) / prefixes.length;
t = performance.now();
for (const p of prefixes) eng.analyze(p + ' tedavisi');
console.log(`\ngecikme: complete ort ${per.toFixed(3)} ms · analyze ort ${((performance.now() - t) / prefixes.length).toFixed(3)} ms · heap ${(process.memoryUsage().heapUsed / 1e6).toFixed(0)} MB`);
