#!/usr/bin/env node
/**
 * Arayüz sınıflarını tasarım sistemine (v7 · Apple Sağlık) çevirir.
 *
 *  - Ham Tailwind renkleri (amber-50, rose-700, slate-500 …) → anlamsal tokenlar
 *    (warn-soft, bad-text, ink-3 …). Böylece her ekran aynı renk dilini konuşur ve
 *    koyu tema kendiliğinden uyar.
 *  - Rastgele piksel yazı boyutları (text-[13.5px]) → 10 basamaklı yazı ölçeği
 *    (text-2xs … text-4xl).
 *
 * `dark:` önekli sınıflara ve bilinçli renk kullanan dosyalara (kalem, fosforlu
 * kalem, özet okuyucu temaları) dokunmaz.
 *
 * Kullanım:  node scripts/design/normalize-ui-classes.mjs [--apply] [yol…]
 */
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '../..');
const args = process.argv.slice(2);
const APPLY = args.includes('--apply');
const targets = args.filter((a) => !a.startsWith('--'));

const EXCLUDE = [
  /src\/components\/annotation\//,
  /src\/components\/ui\/Highlighter\.tsx$/,
  /src\/components\/learn\/SlideDrawingCanvas\.tsx$/,
  /src\/components\/SummaryArtifactReader\.tsx$/,
  /src\/components\/summary\//,
  /src\/components\/pdf\//,
  /src\/components\/BookletView\.tsx$/,
];

const GROUP = {
  amber: 'warn', orange: 'warn', yellow: 'warn',
  rose: 'bad', red: 'bad', pink: 'bad',
  emerald: 'ok', green: 'ok', teal: 'ok', lime: 'ok',
  blue: 'accent', indigo: 'accent', sky: 'accent', cyan: 'accent',
  violet: 'ai', purple: 'ai', fuchsia: 'ai',
  slate: 'n', gray: 'n', zinc: 'n', neutral: 'n', stone: 'n',
};
const PAL = Object.keys(GROUP).join('|');
const PROPS = 'bg|text|border|border-[trblxy]|ring|outline|divide|from|via|to|fill|stroke|decoration|accent|caret|placeholder|shadow';
const RE = new RegExp(`(?<![\\w\\-\\[/])((?:[a-z0-9-]+:)*)(${PROPS})-(${PAL})-(50|100|200|300|400|500|600|700|800|900|950)(\\/\\d{1,3})?(?![\\w\\-])`, 'g');

const neutral = (prop, s) => {
  const surface = prop === 'bg' || prop === 'from' || prop === 'via' || prop === 'to';
  const line = /^(border|ring|outline|divide)/.test(prop);
  if (surface) return s <= 100 ? 'field' : s === 200 ? 'line' : s === 300 ? 'line-2' : s <= 500 ? 'ink-3' : s <= 700 ? 'ink-2' : 'ink';
  if (line) return s <= 200 ? 'line' : 'line-2';
  if (prop === 'shadow') return null;
  // metin, simge, imleç
  return s <= 300 ? 'ink-3' : s <= 500 ? 'ink-3' : s <= 700 ? 'ink-2' : 'ink';
};
const colored = (prop, g, s, alpha) => {
  const surface = prop === 'bg' || prop === 'from' || prop === 'via' || prop === 'to';
  const line = /^(border|ring|outline|divide)/.test(prop);
  if (prop === 'shadow') return null;
  if (surface) {
    if (s <= 100) return { c: `${g}-soft`, a: alpha };
    if (s <= 300) return { c: g, a: alpha || '/20' };
    return { c: g, a: alpha };
  }
  if (line) return s <= 300 ? { c: g, a: alpha || '/30' } : { c: g, a: alpha };
  // metin / simge
  if (s <= 200) return { c: `${g}-soft`, a: alpha };
  return { c: g === 'bad' ? 'bad-text' : g, a: alpha };
};

const TEXT_STEPS = [
  [11.25, '2xs'], [12.25, 'xs'], [13.25, 'sm'], [14.25, 'base'], [16.25, 'md'],
  [18.75, 'lg'], [21, 'xl'], [25, '2xl'], [31, '3xl'], [Infinity, '4xl'],
];
const RE_TEXT = /(?<![\w\-[/])((?:[a-z0-9-]+:)*)text-\[(\d+(?:\.\d+)?)px\](?![\w\-])/g;

const stats = { files: 0, color: 0, text: 0, byFile: [] };

function transform(src) {
  let nColor = 0;
  let nText = 0;
  let out = src.replace(RE, (m, variants, prop, pal, shade, alpha) => {
    if (/(^|:)dark:/.test(variants)) return m;
    const s = Number(shade);
    const g = GROUP[pal];
    let rep;
    if (g === 'n') {
      const c = neutral(prop, s);
      if (!c) return m;
      rep = `${variants}${prop}-${c}${alpha || ''}`;
    } else {
      const r = colored(prop, g, s, alpha);
      if (!r) return m;
      rep = `${variants}${prop}-${r.c}${r.a || ''}`;
    }
    if (rep !== m) nColor++;
    return rep;
  });
  out = out.replace(RE_TEXT, (m, variants, px) => {
    if (/(^|:)dark:/.test(variants)) return m;
    const v = Number(px);
    const step = TEXT_STEPS.find(([max]) => v <= max)[1];
    nText++;
    return `${variants}text-${step}`;
  });
  return { out, nColor, nText };
}

function walk(p, acc) {
  const st = fs.statSync(p);
  if (st.isDirectory()) for (const f of fs.readdirSync(p)) walk(path.join(p, f), acc);
  else if (/\.(tsx|ts)$/.test(p)) acc.push(p);
  return acc;
}

const roots = targets.length ? targets.map((t) => path.resolve(ROOT, t)) : [path.join(ROOT, 'src')];
const files = roots.flatMap((r) => walk(r, []));
for (const f of files) {
  const rel = path.relative(ROOT, f);
  if (EXCLUDE.some((re) => re.test(rel))) continue;
  const src = fs.readFileSync(f, 'utf8');
  const { out, nColor, nText } = transform(src);
  if (out === src) continue;
  stats.files++;
  stats.color += nColor;
  stats.text += nText;
  stats.byFile.push([nColor + nText, rel]);
  if (APPLY) fs.writeFileSync(f, out);
}
stats.byFile.sort((a, b) => b[0] - a[0]);
console.log(`${APPLY ? 'Uygulandı' : 'Deneme'}: ${stats.files} dosya · ${stats.color} renk · ${stats.text} yazı boyutu`);
for (const [n, f] of stats.byFile.slice(0, 15)) console.log(String(n).padStart(5), f);
