/** Anlama sınaması: niyet doğruluğu (A: elle, B: şablon+gürültü) + varlık yakalama. Çalıştır: npx tsx scripts/asistan/anlama_sinama.mts [-v] */
import fs from 'node:fs';
import { anla } from '../../src/services/asistan/anlama';
import { getQueryIntel } from '../../src/services/queryIntel/server';
import { fold } from '../../src/services/queryIntel/core';

const verbose = process.argv.includes('-v');
for (let i = 0; i < 120 && !getQueryIntel(); i++) await new Promise(r => setTimeout(r, 500));
if (!getQueryIntel()) { console.error('queryIntel paketi yüklenemedi'); process.exit(2); }
const satirlar = fs.readFileSync(new URL('./sinama/' + (process.argv.find(a => a.endsWith('.jsonl')) || 'anlama.jsonl'), import.meta.url), 'utf-8').trim().split('\n').map(l => JSON.parse(l));
const sayac: Record<string, { ok: number; n: number }> = { A: { ok: 0, n: 0 }, B: { ok: 0, n: 0 } };
const varlik = { ok: 0, n: 0 };
const niyetHata: Record<string, number> = {};
const hatalar: string[] = [];
for (const s of satirlar) {
  const a = anla(s.q);
  const dogru = a.ana === s.niyet || a.ikincil.includes(s.niyet);
  const tam = a.ana === s.niyet;
  sayac[s.grup].n++; if (tam) sayac[s.grup].ok++;
  if (!tam) { niyetHata[`${s.niyet}→${a.ana}`] = (niyetHata[`${s.niyet}→${a.ana}`] || 0) + 1; hatalar.push(`[${s.grup}] "${s.q}" beklenen=${s.niyet} bulunan=${a.ana}${dogru ? ' (ikincilde var)' : ''} varlik=${a.varliklar.map(v => v.label).join('|')}`); }
  if (s.varlik) {
    varlik.n++;
    const hedef = fold(s.varlik).split(' ')[0].slice(0, 5);
    if (a.varliklar.some(v => fold(v.label + ' ' + v.matched).includes(hedef))) varlik.ok++;
    else if (verbose) hatalar.push(`[varlık] "${s.q}" beklenen=${s.varlik} bulunan=${a.varliklar.map(v => v.label).join('|') || '-'}`);
  }
}
const pct = (o: { ok: number; n: number }) => `${o.ok}/${o.n} = %${(100 * o.ok / o.n).toFixed(1)}`;
console.log(`Niyet A (elle): ${pct(sayac.A)}\nNiyet B (şablon): ${pct(sayac.B)}\nVarlık yakalama: ${pct(varlik)}`);
console.log('En sık karışmalar:', Object.entries(niyetHata).sort((x, y) => y[1] - x[1]).slice(0, 12).map(([k, v]) => `${k}×${v}`).join('  '));
if (verbose) console.log(hatalar.join('\n'));
process.exit(0);
