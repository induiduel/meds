// Sayfa açılışı / sayfaya dönüş başarım ölçümü (başsız Chrome + CDP).
// Kullanım: node scripts/perf/yukleme_olcum.mjs /cikmis /kartlar /cikmis RELOAD /cikmis
//   RELOAD = sayfayı baştan yükle (IndexedDB dolu, gerçek dönüş ziyareti).
// Ortam: RATE (CPU yavaşlatma, 4), BASE (http://localhost:3000), PROF=1 (JS öz-süre profili).
// Ölçüt: readyMs (içerik görünene kadar), long-animation-frame toplamı (donma), en büyük ağ istekleri.
// Gezinme SPA içidir (history.pushState + popstate), kullanıcının sayfalar arası geçişi gibi.
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';

const PATHS = process.argv.slice(2);
const RATE = Number(process.env.RATE || 4);
const BASE = process.env.BASE || 'http://localhost:3000';
const PORT = 9333 + Math.floor(Math.random() * 500);
const dir = `${os.tmpdir()}/medsor-perf-load-${PORT}`;
const chrome = spawn('/opt/google/chrome/chrome', ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${dir}`, '--window-size=1280,800',
  '--no-first-run', '--no-default-browser-check', '--disable-extensions', '--mute-audio', '--disable-gpu'], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
process.on('exit', () => { try { chrome.kill('SIGKILL'); } catch {} try { fs.rmSync(dir, { recursive: true, force: true }); } catch {} });

for (let i = 0; i < 50; i++) { try { await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json(); break; } catch { await sleep(200); } }
const tgt = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: 'PUT' })).json();
const ws = new WebSocket(tgt.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener('open', r));
let id = 0; const pend = new Map(); const L = [];
ws.addEventListener('message', (m) => {
  const d = JSON.parse(m.data);
  if (d.id && pend.has(d.id)) { const p = pend.get(d.id); pend.delete(d.id); d.error ? p.rej(new Error(JSON.stringify(d.error))) : p.res(d.result); }
  else if (d.method) L.forEach((l) => l(d));
});
const send = (method, params = {}) => new Promise((res, rej) => { const i = ++id; pend.set(i, { res, rej }); ws.send(JSON.stringify({ id: i, method, params })); });
const ev = async (e) => (await send('Runtime.evaluate', { expression: e, awaitPromise: true, returnByValue: true })).result.value;
await send('Page.enable'); await send('Runtime.enable'); await send('Network.enable');
const req = new Map();
L.push((d) => {
  if (d.method === 'Network.requestWillBeSent') req.set(d.params.requestId, { url: d.params.request.url, t0: d.params.timestamp });
  if (d.method === 'Network.loadingFinished') { const r = req.get(d.params.requestId); if (r) { r.bytes = d.params.encodedDataLength; r.t1 = d.params.timestamp; } }
});

const home = async () => { await send('Emulation.setCPUThrottlingRate', { rate: 1 }); await send('Page.navigate', { url: BASE + '/' }); await sleep(8000); await send('Emulation.setCPUThrottlingRate', { rate: RATE }); };
await home();
for (const p of PATHS) {
  req.clear();
  if (p === 'RELOAD') { await home(); console.log('--- yeniden yüklendi (IndexedDB dolu)'); continue; }
  await ev(`(() => { window.__loaf = []; new PerformanceObserver((l) => { for (const e of l.getEntries()) window.__loaf.push(e.duration); }).observe({ type: 'long-animation-frame' }); return 1; })()`);
  if (process.env.PROF) { await send('Profiler.enable'); await send('Profiler.setSamplingInterval', { interval: 500 }); await send('Profiler.start'); }
  const t0 = Date.now();
  await ev(`(() => { history.pushState({}, '', ${JSON.stringify(p)}); dispatchEvent(new PopStateEvent('popstate')); return 1; })()`);
  let ready = -1;
  for (let i = 0; i < 120; i++) {
    await sleep(250);
    if (await ev(`(() => { const t = document.querySelector('main')?.innerText || ''; return t.length > 400 && !/Yükleniyor/.test(t.slice(0, 300)); })()`)) { ready = Date.now() - t0; break; }
  }
  await sleep(4000);
  if (process.env.PROF) {
    const { profile } = await send('Profiler.stop');
    const byId = new Map(profile.nodes.map((n) => [n.id, n])); const t = new Map(); const self = new Map();
    profile.samples.forEach((s, i) => t.set(s, (t.get(s) || 0) + (profile.timeDeltas[i] || 0)));
    for (const [nid, us] of t) { const cf = byId.get(nid).callFrame; const k = `${cf.functionName || '(anon)'} ${cf.url.split('/').pop()}:${cf.lineNumber}:${cf.columnNumber}`; self.set(k, (self.get(k) || 0) + us); }
    console.log('PROFILE', p, JSON.stringify([...self].sort((a, b) => b[1] - a[1]).slice(0, 15).map(([k, v]) => (v / 1000).toFixed(0) + 'ms ' + k), null, 1));
  }
  const loaf = await ev('window.__loaf');
  const net = [...req.values()].filter((r) => r.bytes).sort((a, b) => b.bytes - a.bytes).slice(0, 4)
    .map((r) => `${(r.bytes / 1024).toFixed(0)}KB ${((r.t1 - r.t0) * 1000).toFixed(0)}ms ${r.url.replace(BASE, '').slice(0, 80)}`);
  console.log(JSON.stringify({ path: p, cpu: RATE, readyMs: ready, loafN: loaf.length, loafSum: Math.round(loaf.reduce((a, b) => a + b, 0)),
    worst: loaf.map(Math.round).sort((a, b) => b - a).slice(0, 5), net }));
}
process.exit(0);
