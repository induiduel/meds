#!/usr/bin/env node
/**
 * prepare-android-dist.mjs
 * dist/ içindeki yalnızca GÜNCEL derlemeye ait (reachable) JS/CSS parçalarını ve temel statik dosyaları
 * dist-android/ klasörüne kopyalar. Böylece Capacitor APK'sı 3.2 GB'lık eski derleme geçmişini taşımaz.
 */
import fs from 'node:fs';
import path from 'node:path';

const DIST = path.resolve('dist');
const OUT = path.resolve('dist-android');
const ASSETS = path.join(DIST, 'assets');
const OUT_ASSETS = path.join(OUT, 'assets');

if (!fs.existsSync(ASSETS)) {
  console.error('[prepare-android-dist] dist/assets bulunamadı. Önce vite build çalıştırın.');
  process.exit(1);
}

fs.rmSync(OUT, { recursive: true, force: true });
fs.mkdirSync(OUT_ASSETS, { recursive: true });

const all = new Set(fs.readdirSync(ASSETS));
const NAME_RE = /[\w.-]+\.(?:js|css|json|woff2?|ttf|png|jpe?g|svg|webp|gif|ico|wasm|mjs)/g;

const roots = fs.readdirSync(DIST)
  .filter((f) => /\.(html|js|json|ico|svg|png)$/.test(f))
  .map((f) => path.join(DIST, f));

for (const r of roots) {
  const base = path.basename(r);
  fs.copyFileSync(r, path.join(OUT, base));
}

for (const dirName of ['icons', 'fonts']) {
  const srcDir = path.join(DIST, dirName);
  if (fs.existsSync(srcDir)) {
    fs.cpSync(srcDir, path.join(OUT, dirName), { recursive: true });
  }
}

const reachable = new Set();
const queue = roots.filter((f) => /\.(html|js|json)$/.test(f));
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
      if (/\.(js|mjs|css|json)$/.test(name)) {
        queue.push(path.join(ASSETS, name));
      }
    }
  }
}

let totalBytes = 0;
for (const name of reachable) {
  const src = path.join(ASSETS, name);
  const dst = path.join(OUT_ASSETS, name);
  fs.copyFileSync(src, dst);
  totalBytes += fs.statSync(dst).size;
}

console.log(
  `[prepare-android-dist] ${reachable.size} güncel parça dist-android/ içine kopyalandı (${(totalBytes / 1e6).toFixed(1)} MB)`
);
