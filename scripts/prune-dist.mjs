#!/usr/bin/env node
// dist/assets birikimini temizler (vite emptyOutDir:false → her derleme yeni hash'li parçalar bırakır).
// Korunan: güncel derlemeden erişilebilen dosyalar + son KEEP_BUILDS derlemenin kayıtlı kümesi
//          + son --keep-hours saat içinde yazılmış dosyalar (eski SW istemcileri için tampon).
// Kullanım: node scripts/prune-dist.mjs [--apply] [--dir dist] [--keep-builds 2] [--keep-hours 24]
//           --apply olmadan yalnız rapor verir.
import fs from 'node:fs';
import path from 'node:path';

const args = process.argv.slice(2);
const opt = (name, def) => {
  const i = args.indexOf(name);
  return i >= 0 ? args[i + 1] : def;
};
const APPLY = args.includes('--apply');
const DIST = path.resolve(opt('--dir', 'dist'));
const KEEP_BUILDS = Number(opt('--keep-builds', 2));
const KEEP_HOURS = Number(opt('--keep-hours', 24));
const ASSETS = path.join(DIST, 'assets');
const LEDGER = path.join(DIST, '.builds');

if (!fs.existsSync(ASSETS)) {
  console.error(`[prune-dist] ${ASSETS} yok`);
  process.exit(1);
}

const all = new Set(fs.readdirSync(ASSETS));
const NAME_RE = /[\w.-]+\.(?:js|css|json|woff2?|ttf|png|jpe?g|svg|webp|gif|ico|wasm|mjs|map)/g;

// Kök dosyalardan (html, sw.js, manifest) başlayıp assets içindeki referansları izle.
const roots = fs.readdirSync(DIST)
  .filter((f) => /\.(html|js|json)$/.test(f))
  .map((f) => path.join(DIST, f));
const reachable = new Set();
const queue = [...roots];
while (queue.length) {
  const file = queue.pop();
  let text;
  try {
    text = fs.readFileSync(file, 'utf8');
  } catch {
    continue;
  }
  for (const m of text.matchAll(NAME_RE)) {
    const name = m[0];
    if (all.has(name) && !reachable.has(name)) {
      reachable.add(name);
      if (/\.(js|mjs|css|json)$/.test(name)) queue.push(path.join(ASSETS, name));
    }
  }
}
if (reachable.size === 0) {
  console.error('[prune-dist] güncel derlemeden hiç parça bulunamadı — güvenlik için durdu');
  process.exit(1);
}

// Derleme defteri: her çalıştırmada güncel küme kaydedilir, son KEEP_BUILDS küme korunur.
fs.mkdirSync(LEDGER, { recursive: true });
const entry = [...reachable].find((n) => n.startsWith('entry-index-')) || `build-${Date.now()}`;
const ledgerFile = path.join(LEDGER, `${entry}.txt`);
if (!fs.existsSync(ledgerFile)) fs.writeFileSync(ledgerFile, [...reachable].sort().join('\n'));
const ledgers = fs.readdirSync(LEDGER)
  .map((f) => ({ f, t: fs.statSync(path.join(LEDGER, f)).mtimeMs }))
  .sort((a, b) => b.t - a.t);
const keep = new Set(reachable);
for (const { f } of ledgers.slice(0, KEEP_BUILDS)) {
  for (const n of fs.readFileSync(path.join(LEDGER, f), 'utf8').split('\n')) if (n) keep.add(n);
}
if (APPLY) for (const { f } of ledgers.slice(KEEP_BUILDS)) fs.rmSync(path.join(LEDGER, f), { force: true });

const cutoff = Date.now() - KEEP_HOURS * 3600_000;
let delCount = 0;
let delBytes = 0;
let keptRecent = 0;
for (const name of all) {
  if (keep.has(name)) continue;
  const p = path.join(ASSETS, name);
  const st = fs.statSync(p);
  if (st.mtimeMs > cutoff) {
    keptRecent++;
    continue;
  }
  delCount++;
  delBytes += st.size;
  if (APPLY) fs.rmSync(p, { force: true });
}

const mb = (b) => (b / 1e6).toFixed(1) + 'MB';
console.log(
  `[prune-dist] toplam ${all.size} · güncel ${reachable.size} · korunan ${keep.size}` +
    ` · son ${KEEP_HOURS}s tamponu ${keptRecent} · ${APPLY ? 'silinen' : 'silinecek'} ${delCount} (${mb(delBytes)})`,
);
