// Palet kaydındaki (src/utils/palettes.ts) tüm paletlerin metin/zemin çiftlerini WCAG oranıyla ölçer.
// Kullanım: npx tsx scripts/design/check-contrast.mjs   (çıkış kodu 1 = en az bir çift eşik altında)
import { PALETTES, TOKEN_KEYS } from '../../src/utils/palettes.ts';

const lum = (h) => { const n = parseInt(h.slice(1), 16); return [n >> 16, (n >> 8) & 255, n & 255].map((c) => { c /= 255; return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4; }).reduce((a, c, i) => a + c * [0.2126, 0.7152, 0.0722][i], 0); };
const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };
// [ön plan, zemin, eşik] — eşik verilmezse 4.5 (normal metin). line-2 bir kenarlık: 1.5 yeter.
const PAIRS = [['ink', 'white'], ['ink', 'canvas'], ['ink-2', 'white'], ['ink-2', 'field'], ['ink-3', 'white'], ['ink-3', 'canvas'], ['ink-3', 'field'],
  ['accent', 'white'], ['accent', 'canvas'], ['accent', 'field'], ['on-accent', 'accent'], ['on-accent', 'accent-hover'], ['accent', 'accent-soft'],
  ['clinic', 'white'], ['clinic', 'clinic-soft'], ['ok', 'white'], ['ok', 'ok-soft'], ['warn', 'white'], ['warn', 'warn-soft'],
  ['bad-text', 'white'], ['bad-text', 'bad-soft'], ['ai', 'white'], ['ai', 'ai-soft'], ['brand', 'brand-soft', 3],
  ['on-solid', 'ok'], ['on-solid', 'bad'], ['on-solid', 'accent'], ['on-solid', 'warn'], ['on-solid', 'clinic'], ['line-2', 'white', 1.5]];

let fails = 0;
const ids = new Set();
for (const p of PALETTES) {
  const key = `${p.mode}/${p.id}`;
  if (ids.has(key)) { console.log(`✗ ${key} iki kez tanımlı`); fails++; }
  ids.add(key);
  const missing = TOKEN_KEYS.filter((k) => !/^#[0-9A-Fa-f]{6}$/.test(p.vars[k] || ''));
  if (missing.length) { console.log(`✗ ${key} eksik/geçersiz token: ${missing.join(', ')}`); fails += missing.length; continue; }
  const bad = [];
  for (const [f, b, min = 4.5] of PAIRS) { const r = ratio(p.vars[f], p.vars[b]); if (r < min) bad.push(`${f}/${b} ${r.toFixed(2)}<${min}`); }
  fails += bad.length;
  console.log(`${bad.length ? '✗' : '✓'} ${key.padEnd(8)} ${p.name.padEnd(14)} ${bad.join(', ')}`);
}
for (const m of ['light', 'sepia', 'dark']) { const n = PALETTES.filter((p) => p.mode === m).length; if (n !== 4) { console.log(`✗ ${m}: ${n} palet (4 olmalı)`); fails++; } }
console.log(fails ? `\n${fails} sorun` : `\n${PALETTES.length} palet × ${PAIRS.length} çift: tümü eşiğin üstünde`);
process.exit(fails ? 1 : 0);
