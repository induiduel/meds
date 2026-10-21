// Dağıtım öncesi: server.ts'ten ulaşılan her göreli import dosyası ağaçta var mı?
// (Commit'lenmemiş dosyaya import → canlı açılışta ERR_MODULE_NOT_FOUND, 2026-10-21 kesintisi.)
// Kullanım: node import_denetimi.mjs <kök> [giriş...]   → eksik varsa çıkış 1
import fs from 'node:fs';
import path from 'node:path';

const kok = path.resolve(process.argv[2] || '.');
const girisler = process.argv.slice(3).length ? process.argv.slice(3) : ['server.ts'];
const UZANTI = ['', '.ts', '.tsx', '.mts', '.js', '.mjs', '.jsx', '.json'];
const KALIP = /(?:import|export)\s[^'"]*?from\s*['"]([^'"]+)['"]|import\s*['"]([^'"]+)['"]|import\(\s*['"]([^'"]+)['"]\s*\)/g;

function coz(taban, hedef) {
  const ham = hedef.startsWith('@/') ? path.join(kok, hedef.slice(2)) : path.resolve(path.dirname(taban), hedef);
  const adaylar = [];
  for (const u of UZANTI) adaylar.push(ham + u);
  // TS'de './x.js' yazılıp x.ts bulunabilir
  if (/\.(m?js|jsx)$/.test(ham)) for (const u of ['.ts', '.tsx', '.mts']) adaylar.push(ham.replace(/\.(m?js|jsx)$/, u));
  for (const u of UZANTI.slice(1)) adaylar.push(path.join(ham, 'index' + u));
  return adaylar.find((a) => fs.existsSync(a) && fs.statSync(a).isFile());
}

const gorulen = new Set();
const eksik = [];
const kuyruk = girisler.map((g) => path.join(kok, g));
while (kuyruk.length) {
  const dosya = kuyruk.pop();
  if (gorulen.has(dosya)) continue;
  gorulen.add(dosya);
  if (!/\.(m?[jt]sx?)$/.test(dosya)) continue;
  const metin = fs.readFileSync(dosya, 'utf8').replace(/\/\*[\s\S]*?\*\//g, '').replace(/^\s*\/\/.*$/gm, '');
  for (const m of metin.matchAll(KALIP)) {
    const hedef = m[1] || m[2] || m[3];
    if (!hedef.startsWith('.') && !hedef.startsWith('@/')) continue;
    const bulunan = coz(dosya, hedef);
    if (bulunan) kuyruk.push(bulunan);
    else eksik.push(`${path.relative(kok, dosya)} → ${hedef}`);
  }
}
if (eksik.length) {
  console.error(`DURDU: ${eksik.length} import commit'li ağaçta yok (commit'lenmemiş dosya?):`);
  for (const e of eksik) console.error('  · ' + e);
  process.exit(1);
}
console.log(`    import denetimi: ${gorulen.size} dosya, eksik yok`);
