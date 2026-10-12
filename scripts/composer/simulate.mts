/**
 * Soru ekle yazım yardımcısı simülasyonu (metin tamamlama + yazım düzeltme).
 * Kullanım: npm run composer:sim  (= npx tsx scripts/composer/simulate.mts [--verbose] [--seed 42])
 *   --test/--model verilmezse %10 test kümesi ayrılır ve model kalan %90'dan geçici olarak derlenir.
 *   GHOST_MIN=0.4 → hayalet eşiğini dener; NO_SOURCES=1 → sunucu kaynakları yokken ölçer.
 * Test kökleri modele hiç girmez (dışarıda bırakılmış %10); kaynaklar sunucudaki
 * /api/past-exams/similar gibi eğitim köklerinden kelime örtüşmesiyle seçilir.
 */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { smartComposerService } from '../../src/services/smartComposerService.ts';

const arg = (k: string) => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : undefined; };
const verbose = process.argv.includes('--verbose');
const all: any[] = JSON.parse(fs.readFileSync('src/data/pastQuestions.json', 'utf8'));
let testPath = arg('--test'), modelPath = arg('--model');
if (!testPath) {
  // sabit tohumla %10 test kümesi; model yalnız kalan %90'dan derlenir (sızıntı yok)
  let s0 = Number(arg('--seed') || 42); const r0 = () => ((s0 = (s0 * 16807) % 2147483647) / 2147483647);
  const ids = all.filter((q) => (q.stem || '').split(/\s+/).length >= 6).map((q) => q.id);
  const t = ids.filter(() => r0() < 0.1);
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'composer-sim-'));
  testPath = path.join(dir, 'test.json'); modelPath = path.join(dir, 'model.json');
  fs.writeFileSync(testPath, JSON.stringify(t));
  execFileSync('python3', ['scripts/composer/build_composer_model.py', '--exclude-ids', testPath, '--out', modelPath], { stdio: 'inherit' });
}
const testIds = new Set<string>(JSON.parse(fs.readFileSync(testPath, 'utf8')));
const svc: any = smartComposerService;
if (process.env.GHOST_MIN) svc.ghostMin = Number(process.env.GHOST_MIN);
if (modelPath && svc.setModel) svc.setModel(JSON.parse(fs.readFileSync(modelPath, 'utf8')));

const clean = (s: string) => (s || '').replace(/\s+/g, ' ').trim().replace(/^\(?\d+[.)-]\s*/, '');
const low = (s: string) => s.toLocaleLowerCase('tr-TR');
const fw = (w: string) => low(w).replace(/[^\p{L}\p{N}%]/gu, '');
const train = all.filter((q) => !testIds.has(q.id)).map((q) => clean(q.stem)).filter((s) => s.split(' ').length >= 3);
const test = all.filter((q) => testIds.has(q.id)).map((q) => clean(q.stem)).filter((s) => s.split(' ').length >= 6);

// basit benzer kök bulucu (sunucu benzeri)
const trainSets = train.map((s) => new Set(s.split(' ').map(fw).filter((w) => w.length > 3)));
function similar(q: string, extra?: string): string[] {
  const qs = q.split(' ').map(fw).filter((w) => w.length > 3);
  const sc = trainSets.map((S, i) => [qs.reduce((a, w) => a + (S.has(w) ? 1 : 0), 0), i] as [number, number]);
  sc.sort((a, b) => b[0] - a[0]);
  const out = sc.slice(0, 5).filter((x) => x[0] > 0).map((x) => train[x[1]]);
  if (process.env.NO_SOURCES) return [];
  return extra ? [extra, ...out.slice(0, 4)] : out;
}

let seed = 7; const rnd = () => ((seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648);
const CLOSERS = /hangisi|hangileri|nedir|değildir|yanlıştır|doğrudur|aşağıdaki/i;

// ---------- 1) TAMAMLAMA ----------
type C = { kind: string; typed: string; truth: string; sources: string[] };
const comp: C[] = [];
const pick = test.slice().sort(() => rnd() - 0.5);
for (let n = 0; n < 120; n++) {
  const st = pick[n % pick.length]; const ws = st.split(' ');
  const cut = 2 + Math.floor(rnd() * (ws.length - 3));
  const mid = n % 3 === 0 && ws[cut].length > 4;
  let typed = ws.slice(0, cut).join(' ') + ' ';
  let truth = ws.slice(cut).join(' ');
  if (mid) { const k = 2 + Math.floor(rnd() * (ws[cut].length - 3)); typed = typed + ws[cut].slice(0, k); truth = ws[cut].slice(k) + ' ' + ws.slice(cut + 1).join(' '); }
  const kind = n < 20 ? 'havuzda' : mid ? 'kelime-ortası' : 'kelime-sonu';
  comp.push({ kind, typed, truth, sources: similar(typed, n < 20 ? st : undefined) });
}

function scoreComp(c: C, ghost: string) {
  const g = ghost; if (!g.trim()) return { offered: 0, firstOk: 0, words: 0, wrong: 0, premature: 0 };
  // kelime ortasıysa ilk parça birebir eşleşmeli
  const gt = (c.typed + g).slice(c.typed.length);
  const tw = c.truth.split(' ').filter(Boolean).map(fw), gw = gt.trim().split(' ').filter(Boolean).map(fw);
  const midOk = /\S$/.test(c.typed) ? c.truth.startsWith(gt.split(' ')[0]) || (gt.startsWith(' ') && c.truth.startsWith(' ')) : true;
  let m = 0; while (m < gw.length && m < tw.length && gw[m] === tw[m]) m++;
  const firstOk = m > 0 && midOk ? 1 : 0;
  const premature = CLOSERS.test(gt) && !CLOSERS.test(c.truth) ? 1 : 0;
  return { offered: 1, firstOk, words: firstOk ? m : 0, wrong: firstOk ? 0 : 1, premature };
}

const res: Record<string, any> = {};
let tms = 0;
for (const c of comp) {
  const t0 = performance.now();
  const r = smartComposerService.getAssist(c.typed, c.sources);
  tms = Math.max(tms, performance.now() - t0);
  const s = scoreComp(c, r.ghost);
  const b = (res[c.kind] ||= { n: 0, offered: 0, firstOk: 0, words: 0, wrong: 0, premature: 0 });
  b.n++; for (const k of ['offered', 'firstOk', 'words', 'wrong', 'premature']) b[k] += (s as any)[k];
  if (verbose && s.wrong) console.log(`✗ [${c.kind}/${r.options[0]?.category}] «${c.typed}» → «${r.ghost}» | doğru: «${c.truth.slice(0, 50)}»`);
}

// ---------- 2) YAZIM DÜZELTME ----------
const ASC: Record<string, string> = { ç: 'c', ğ: 'g', ı: 'i', ö: 'o', ş: 's', ü: 'u', Ç: 'C', Ğ: 'G', İ: 'I', Ö: 'O', Ş: 'S', Ü: 'U' };
const strip = (s: string) => s.replace(/[çğıöşüÇĞİÖŞÜ]/g, (ch) => ASC[ch]);
function typo(w: string): string {
  const i = 1 + Math.floor(rnd() * (w.length - 2)); const r = rnd();
  if (r < 0.35) return w.slice(0, i) + w.slice(i + 1);                       // harf düşmesi
  if (r < 0.7) return w.slice(0, i) + w[i + 1] + w[i] + w.slice(i + 2);       // yer değiştirme
  return w.slice(0, i) + w[i] + w.slice(i);                                   // harf çiftleme
}
type S = { kind: string; input: string; truth: string };
const sp: S[] = [];
const pk2 = test.slice().sort(() => rnd() - 0.5);
for (let n = 0; n < 70; n++) {
  const st = pk2[n]; let input = st; let kind = 'temiz';
  if (n < 25) { input = strip(st); kind = 'aksansız'; }
  else if (n < 50) {
    kind = 'harf-hatası';
    const ws = st.split(' '); const idx = ws.map((w, i) => [w, i] as [string, number]).filter(([w]) => /^\p{L}{7,}$/u.test(w));
    if (!idx.length) { n--; continue; }
    const [w, i] = idx[Math.floor(rnd() * idx.length)]; ws[i] = typo(w); input = ws.join(' ');
  }
  sp.push({ kind, input: input + ' ', truth: st + ' ' });
}
const sres: Record<string, any> = {};
for (const s of sp) {
  const r = smartComposerService.getSpellingCorrection(s.input);
  const out = r ? r.text : s.input;
  const iw = s.input.split(' '), ow = out.split(' '), tw = s.truth.split(' ');
  let need = 0, fixed = 0, broke = 0;
  for (let i = 0; i < tw.length; i++) {
    const wasWrong = low(iw[i] ?? '') !== low(tw[i]);
    const nowOk = low(ow[i] ?? '') === low(tw[i]);
    if (wasWrong) { need++; if (nowOk) fixed++; } else if (!nowOk) broke++;
  }
  const b = (sres[s.kind] ||= { n: 0, need: 0, fixed: 0, broke: 0 });
  b.n++; b.need += need; b.fixed += fixed; b.broke += broke;
  if (verbose && (broke || fixed < need)) console.log(`✎ [${s.kind}] «${s.input.trim()}» → «${out.trim()}»`);
}

console.log(`\nTAMAMLAMA (${comp.length} senaryo, en uzun ${tms.toFixed(1)} ms)`);
for (const [k, b] of Object.entries(res)) console.log(`  ${k.padEnd(14)} n=${b.n} öneri=%${(100 * b.offered / b.n).toFixed(0)} isabet=%${(100 * b.firstOk / b.n).toFixed(0)} yanlış=%${(100 * b.wrong / b.n).toFixed(0)} erken-kapatma=${b.premature} ort.doğru-kelime=${(b.words / Math.max(1, b.firstOk)).toFixed(1)}`);
console.log(`YAZIM (${sp.length} senaryo)`);
for (const [k, b] of Object.entries(sres)) console.log(`  ${k.padEnd(14)} n=${b.n} düzeltilmesi-gereken=${b.need} düzeltilen=${b.fixed} (%${(100 * b.fixed / Math.max(1, b.need)).toFixed(0)}) bozulan-doğru-kelime=${b.broke}`);
const T = Object.values(res).reduce((a: any, b: any) => ({ n: a.n + b.n, ok: a.ok + b.firstOk, wr: a.wr + b.wrong }), { n: 0, ok: 0, wr: 0 });
const W = Object.values(sres).reduce((a: any, b: any) => ({ need: a.need + b.need, fixed: a.fixed + b.fixed, broke: a.broke + b.broke }), { need: 0, fixed: 0, broke: 0 });
console.log(`ÖZET toplam=${comp.length + sp.length} tamamlama-isabet=%${(100 * T.ok / T.n).toFixed(1)} tamamlama-yanlış=%${(100 * T.wr / T.n).toFixed(1)} düzeltme-geri-çağırma=%${(100 * W.fixed / W.need).toFixed(1)} bozma=${W.broke}`);
