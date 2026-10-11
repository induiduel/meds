// styles/appearance.css'teki 6 paletin metin/zemin çiftlerini WCAG oranıyla ölçer. Kullanım: node scripts/design/check-contrast.mjs
import { readFileSync } from 'node:fs';
const css = readFileSync(new URL('../../src/styles/appearance.css', import.meta.url), 'utf8');
const lum = (h) => { const n = parseInt(h.slice(1), 16); return [n >> 16, (n >> 8) & 255, n & 255].map((c) => { c /= 255; return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4; }).reduce((a, c, i) => a + c * [0.2126, 0.7152, 0.0722][i], 0); };
const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };
const re = /html\.ui-v7\[data-mode="(\w+)"\]\[data-palette="(\w)"\] \{([^}]*)\}/g;
const pairs = [['ink', 'white'], ['ink', 'canvas'], ['ink-2', 'white'], ['ink-3', 'white'], ['ink-3', 'canvas'], ['accent', 'white'], ['accent', 'canvas'], ['on-accent', 'accent'], ['accent', 'accent-soft'], ['ok', 'white'], ['ok', 'ok-soft'], ['warn', 'white'], ['warn', 'warn-soft'], ['bad-text', 'white'], ['bad-text', 'bad-soft'], ['ai', 'ai-soft'], ['ink-3', 'field'], ['on-solid', 'ok'], ['on-solid', 'bad'], ['on-solid', 'accent'], ['on-solid', 'warn']];
let fails = 0;
for (const m of css.matchAll(re)) {
  const v = Object.fromEntries([...m[3].matchAll(/--color-([\w-]+):\s*(#[0-9A-Fa-f]{6})/g)].map((x) => [x[1], x[2]]));
  const out = pairs.map(([f, b]) => { const r = ratio(v[f], v[b]); if (r < 4.5) fails++; return `${r < 4.5 ? '✗' : ' '} ${f}/${b} ${r.toFixed(2)}`; });
  console.log(`${m[1]}·${m[2]}\n  ` + out.join('\n  '));
}
console.log(fails ? `\n${fails} çift 4.5:1 altında` : '\nTüm çiftler ≥4.5:1');
process.exit(fails ? 1 : 0);
