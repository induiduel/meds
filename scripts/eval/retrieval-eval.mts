// Retrieval eval: 300 seeded past questions -> simulated student queries -> is the same question in top 5?
// Run from repo root: npx tsx scripts/eval/retrieval-eval.mts   (STRIP=1 to drop Turkish characters)
import fs from 'fs';
import { searchLocalRag } from '../../src/services/localRagEngine.ts';
let seed = 42; const rnd = () => (seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648;
const strip = (s: string) => s.replace(/[ıİ]/g, 'i').replace(/[çÇ]/g, 'c').replace(/[ğĞ]/g, 'g').replace(/[öÖ]/g, 'o').replace(/[şŞ]/g, 's').replace(/[üÜ]/g, 'u');
const all = JSON.parse(fs.readFileSync('data/pastQuestions.json', 'utf-8'));
const pool = all.filter((q: any) => (q.stem || q.reconstruction?.stem || '').length > 60);
const picks: any[] = []; while (picks.length < 300) { const q = pool[Math.floor(rnd() * pool.length)]; if (!picks.includes(q)) picks.push(q); }
const norm = (s: string) => s.toLowerCase().replace(/\s+/g, ' ').slice(0, 80);
const variants: Record<string, (q: any) => string> = {
  'kısmi kök': (q) => {
    const words = (q.stem || q.reconstruction.stem).split(/\s+/).filter((w: string) => w.length >= 4);
    let kept = words.filter(() => rnd() < 0.5).slice(0, 8).join(' ');
    return `${process.env.STRIP ? strip(kept) : kept} sorusu çıktı`;
  },
  'ek değişmiş': (q) => {
    const sfx = ['in', 'de', 'ler', 'dan', 'ı', 'una', 'leri'];
    const words = (q.stem || q.reconstruction.stem).split(/\s+/).filter((w: string) => w.length >= 4);
    const kept = words.filter(() => rnd() < 0.5).slice(0, 8)
      .map((w: string) => w.length > 6 && rnd() < 0.6 ? w.slice(0, -2) + sfx[Math.floor(rnd() * sfx.length)] : w).join(' ');
    return `${kept} sorusu çıktı`;
  },
  'sadece konu': (q) => {
    const t = String(q.topic || '').split(/[–-]/).pop()!.trim();
    return process.env.STRIP ? strip(t) : t;
  },
};
for (const [name, mk] of Object.entries(variants)) {
  let hit1 = 0, hit5 = 0, mrr = 0, n = 0;
  for (const q of picks) {
    const query = mk(q); if (query.trim().length < 6) continue; n++;
    const r = await searchLocalRag(query, { limit: 5, documentTypes: ['past_question'] as any });
    const target = norm(q.stem || q.reconstruction.stem);
    const rank = r.findIndex(x => x.documentId === q.id || norm((x.content.match(/Soru Kökü:\n([\s\S]*?)\n/) || [])[1] || '') === target);
    if (r.some(x => (x.metadata?.topic || '') === q.topic)) (globalThis as any).same = ((globalThis as any).same || 0) + 1;
    if (rank === 0) hit1++; if (rank >= 0) { hit5++; mrr += 1 / (rank + 1); }
  }
  console.log(`${name.padEnd(12)} n=${n}  hit@1 ${(hit1 / n * 100).toFixed(0)}%  hit@5 ${(hit5 / n * 100).toFixed(0)}%  MRR ${(mrr / n).toFixed(2)}  aynı-konu@5 ${(((globalThis as any).same || 0) / n * 100).toFixed(0)}%`); (globalThis as any).same = 0;
}
process.exit(0);
