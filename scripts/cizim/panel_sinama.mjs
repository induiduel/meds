// Canlı çizim panel/etiket sınaması (docs/CIZIM_KURALLARI.md §9; kullanıcı 2026-10-24 "her seferinde aynı hatalar").
// Dersin bütün panel ve etiketleri gerçek CizimLayer + pdfDoc.css ile başsız Chrome'da 366 / 567 / 1100 px sayfa
// genişliğinde çizilir; taşma, iç taşma, ayrılan yükseklik aşımı, yatay zincirde satıra kırılma, kelime ortasından kırılma,
// kesik yazı, panel içi üst üste binme ve 7 px altı yazı sayılır. Hata varsa çıkış 1 (ders zinciri yayını durdurur).
// Kullanım: node scripts/cizim/panel_sinama.mjs <ders-anahtarı>
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const key = process.argv[2];
if (!key) { console.error('kullanım: panel_sinama.mjs <ders>'); process.exit(2); }
const HERE = path.dirname(fileURLToPath(import.meta.url));
const MEDS = path.resolve(HERE, '..', '..');
const DIR = fs.mkdtempSync('/tmp/claude-1000/panel-sinama-');
const n = execFileSync(path.join(MEDS, '.venv-ocr/bin/python'), [path.join(HERE, 'sinama/hazirla.py'), key, DIR], { encoding: 'utf8' }).trim().split('\n').pop();
execFileSync(path.join(MEDS, 'node_modules/.bin/esbuild'), [path.join(HERE, 'sinama/giris.tsx'), '--bundle', `--outfile=${DIR}/giris.js`, '--jsx=automatic', '--log-level=error'], { env: { ...process.env, NODE_PATH: path.join(MEDS, 'node_modules') } });
const DENETIM = fs.readFileSync(path.join(HERE, 'sinama/denetim.js'), 'utf8');

const tip = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.png': 'image/png' };
const sunucu = http.createServer((q, s) => { const f = path.join(DIR, decodeURIComponent(new URL(q.url, 'http://x').pathname).replace(/^\/$/, '/index.html')); fs.readFile(f, (e, d) => { if (e) { s.writeHead(404); s.end(); return; } s.writeHead(200, { 'content-type': tip[path.extname(f)] || 'application/octet-stream' }); s.end(d); }); }).listen(0);
const WEB = `http://127.0.0.1:${sunucu.address().port}`;
const PORT = 9800 + Math.floor(Math.random() * 150);
const prof = `${DIR}/chrome`;
const chrome = spawn('/opt/google/chrome/chrome', ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${prof}`, '--no-first-run', '--disable-extensions', '--hide-scrollbars', '--window-size=1300,1000'], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const bitir = (kod) => { try { chrome.kill('SIGKILL'); } catch {} sunucu.close(); try { fs.rmSync(DIR, { recursive: true, force: true }); } catch {} process.exit(kod); };
for (let i = 0; i < 60; i++) { try { await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json(); break; } catch { await sleep(200); } }
const tgt = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: 'PUT' })).json();
const ws = new WebSocket(tgt.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener('open', r));
let id = 0; const pend = new Map();
ws.addEventListener('message', (m) => { const d = JSON.parse(m.data); if (d.id && pend.has(d.id)) { const p = pend.get(d.id); pend.delete(d.id); d.error ? p.rej(new Error(JSON.stringify(d.error))) : p.res(d.result); } });
const send = (method, params = {}) => new Promise((res, rej) => { const i = ++id; pend.set(i, { res, rej }); ws.send(JSON.stringify({ id: i, method, params })); });
const ev = async (expr) => (await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true })).result?.value;
await send('Page.enable'); await send('Runtime.enable');
let toplam = 0;
for (const w of [366, 567, 1100]) {
  await send('Emulation.setDeviceMetricsOverride', { width: w + 40, height: 1000, deviceScaleFactor: 1, mobile: false });
  await send('Page.navigate', { url: `${WEB}/?w=${w}&t=1` });
  for (let i = 0; i < 50 && !(await ev('!!window.__hazir')); i++) await sleep(200);
  await sleep(1200);
  const hatalar = (await ev(DENETIM)) || [];
  toplam += hatalar.length;
  console.log(`${w} px: ${hatalar.length} hata`);
  for (const h of hatalar) console.log('  - ' + h);
}
console.log(`${key}: ${n} öğe × 3 genişlik → ${toplam} hata`);
bitir(toplam ? 1 : 0);
