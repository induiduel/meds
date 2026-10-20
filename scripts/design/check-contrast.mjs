// Palet kaydındaki (src/utils/palettes.ts) tüm paletlerin metin/zemin çiftlerini WCAG oranıyla ölçer.
// Kullanım: npx tsx scripts/design/check-contrast.mjs   (çıkış kodu 1 = en az bir çift eşik altında)
import { PALETTES, TOKEN_KEYS } from '../../src/utils/palettes.ts';

const lum = (h) => { const n = parseInt(h.slice(1), 16); return [n >> 16, (n >> 8) & 255, n & 255].map((c) => { c /= 255; return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4; }).reduce((a, c, i) => a + c * [0.2126, 0.7152, 0.0722][i], 0); };
const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };
// [ön plan, zemin, eşik] — eşik verilmezse 4.5 (normal metin). line-2 bir kenarlık: 1.5 yeter.
const PAIRS = [['ink', 'white'], ['ink', 'canvas'], ['ink-2', 'white'], ['ink-2', 'field'], ['ink-3', 'white', 5], ['ink-3', 'canvas', 5], ['ink-3', 'field', 5],
  ['accent', 'white'], ['accent', 'canvas'], ['accent', 'field'], ['on-accent', 'accent'], ['on-accent', 'accent-hover'], ['accent', 'accent-soft'],
  ['clinic', 'white'], ['clinic', 'clinic-soft'], ['ok', 'white'], ['ok', 'ok-soft'], ['warn', 'white'], ['warn', 'warn-soft'],
  ['bad-text', 'white'], ['bad-text', 'bad-soft'], ['ai', 'white'], ['ai', 'ai-soft'], ['brand', 'brand-soft', 3],
  ['on-solid', 'ok'], ['on-solid', 'bad'], ['on-solid', 'accent'], ['on-solid', 'warn'], ['on-solid', 'clinic'], ['on-solid', 'ai'], ['on-solid', 'brand', 3], ['line-2', 'white', 1.5]];

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
// Tema başına en az 4 palet (v10: açıkta X serisiyle 7, koyuda 6); kimlikler tema içinde benzersiz olmalı
for (const m of ['light', 'sepia', 'dark']) { const ps = PALETTES.filter((p) => p.mode === m); if (ps.length < 4) { console.log(`✗ ${m}: ${ps.length} palet (en az 4)`); fails++; } if (new Set(ps.map((p) => p.id)).size !== ps.length) { console.log(`✗ ${m}: yinelenen palet kimliği`); fails++; } }
// Vurgu seçenekleri (OLED siyah, Gece mercanı …): her biri paletin zeminlerinde okunur olmalı
for (const p of PALETTES) for (const a of p.accents || []) {
  const v = p.vars; const bad = [];
  for (const [f, b] of [[a.accent, v.white], [a.accent, v.canvas], [a.accent, v.field], [a.on, a.accent], [a.on, a.hover], [a.accent, a.soft]]) { const r = ratio(f, b); if (r < 4.5) bad.push(`${f}/${b} ${r.toFixed(2)}`); }
  if (bad.length) { console.log(`✗ ${p.mode}/${p.id} vurgu ${a.id}: ${bad.join(', ')}`); fails += bad.length; }
}
// Ayırt edilebilirlik: aynı temadaki iki palet hem zemin hem vurgu bakımından neredeyse aynıysa (OKLab mesafesi) kopyadır
const oklab = (h) => { const n = parseInt(h.slice(1), 16); const [r, g, b] = [n >> 16, (n >> 8) & 255, n & 255].map((c) => { c /= 255; return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4; });
  const l = Math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b), m = Math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b), s = Math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b);
  return [0.2104542553 * l + 0.793617785 * m - 0.0040720468 * s, 1.9779984951 * l - 2.428592205 * m + 0.4505937099 * s, 0.0259040371 * l + 0.7827717662 * m - 0.808675766 * s]; };
const dist = (a, b) => { const [x, y] = [oklab(a), oklab(b)]; return Math.hypot(x[0] - y[0], x[1] - y[1], x[2] - y[2]); };
for (const m of ['light', 'sepia', 'dark']) { const ps = PALETTES.filter((p) => p.mode === m);
  for (let i = 0; i < ps.length; i++) for (let j = i + 1; j < ps.length; j++) { const da = dist(ps[i].vars.accent, ps[j].vars.accent), dc = dist(ps[i].vars.canvas, ps[j].vars.canvas);
    if (da < 0.08 && dc < 0.03) { console.log(`✗ ${m}: ${ps[i].name} ile ${ps[j].name} neredeyse aynı (vurgu Δ${da.toFixed(3)}, zemin Δ${dc.toFixed(3)})`); fails++; } } }
console.log(fails ? `\n${fails} sorun` : `\n${PALETTES.length} palet × ${PAIRS.length} çift: tümü eşiğin üstünde`);
process.exit(fails ? 1 : 0);
