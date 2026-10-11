/**
 * Uçtan uca arama değerlendirmesi (searchEverything): hastalık profilleri üzerinden otomatik sorgu seti.
 * Her hastalık için: tam ad, yazım hatalı ad, aksansız ad, ad + niyet ("tedavisi"). Beklenen: o hastalığın kartı ilk 3'te.
 * Karşılaştırma: "…" (anlamlandırma kapalı, eski davranışa yakın) ile normal mod.
 *   MEDS_VECTOR_SEARCH=0 npx tsx scripts/search/eval-search.mts   (vektörsüz, deterministik ve hızlı)
 */
import dotenv from 'dotenv';
dotenv.config();
const fs = await import('fs');
const { searchEverything } = await import('../../src/services/ragService.ts');
const { getQueryIntel } = await import('../../src/services/queryIntel/server.ts');
const { fold } = await import('../../src/services/queryIntel/core.ts');
getQueryIntel();
await new Promise((r) => setTimeout(r, 2500));
if (!getQueryIntel()) throw new Error('paket yüklenemedi');

const diseases = JSON.parse(fs.readFileSync('src/data/diseases.json', 'utf-8')) as any[];
let seed = 3;
const rnd = () => ((seed = (seed * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff);
const N = Number(process.env.N || 120);
const pick = [...diseases].sort(() => rnd() - 0.5).slice(0, N);
const ALPHA = 'abcdefghiklmnoprstuvyz';
const typo = (s: string) => {
  const ws = s.split(' ');
  let li = 0;
  ws.forEach((w, i) => { if (w.length > ws[li].length) li = i; });
  const w = ws[li];
  if (w.length < 5) return s;
  const p = 1 + Math.floor(rnd() * (w.length - 2));
  const k = Math.floor(rnd() * 3);
  ws[li] = k === 0 ? w.slice(0, p) + w.slice(p + 1) : k === 1 ? w.slice(0, p) + w[p + 1] + w[p] + w.slice(p + 2) : w.slice(0, p) + ALPHA[Math.floor(rnd() * ALPHA.length)] + w.slice(p + 1);
  return ws.join(' ');
};
const clean = (n: string) => n.replace(/\s*\([^)]*\)/g, '').replace(/\s+/g, ' ').trim();
const sets: Record<string, Array<{ q: string; id: string }>> = { tam: [], hatali: [], aksansiz: [], niyet: [] };
for (const d of pick) {
  const n = clean(d.name);
  if (n.length < 4) continue;
  sets.tam.push({ q: n, id: d.id });
  sets.hatali.push({ q: typo(n), id: d.id });
  sets.aksansiz.push({ q: fold(n), id: d.id });
  sets.niyet.push({ q: `${n} tedavisi`, id: d.id });
}
// Kopya profiller (aynı yalın ad) aynı hedef sayılır: veri sorunu, sıralama hatası değil
const graph = JSON.parse(fs.readFileSync('data/knowledge/disease_graph.json', 'utf-8'));
const same = new Map<string, Set<string>>();
for (const g of graph.summary.duplicates || []) for (const id of g.ids) same.set(id, new Set(g.ids));
const rank = async (q: string, id: string) => {
  const r = await searchEverything(q, { limit: 10 });
  const ok = same.get(id) || new Set([id]);
  const i = r.results.findIndex((h) => h.documentType === 'disease' && ok.has(h.documentId));
  return i < 0 ? 99 : i;
};
for (const [name, items] of Object.entries(sets)) {
  for (const mode of ['eski', 'yeni'] as const) {
    let h1 = 0, h3 = 0, mrr = 0, ms = 0;
    for (const it of items) {
      const t = performance.now();
      const r = await rank(mode === 'eski' ? `"${it.q}"` : it.q, it.id);
      ms += performance.now() - t;
      if (r === 0) h1++;
      if (r < 3) h3++;
      if (r < 10) mrr += 1 / (r + 1);
    }
    const n = items.length;
    console.log(`${name.padEnd(9)} ${mode}: hit@1 %${((h1 / n) * 100).toFixed(1)} · hit@3 %${((h3 / n) * 100).toFixed(1)} · MRR ${(mrr / n).toFixed(3)} · ort ${(ms / n).toFixed(0)} ms (n=${n})`);
  }
}
process.exit(0);
