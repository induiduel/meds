// Başsız Chrome ile sayfa sayfa konsol hatası / yakalanmamış istisna / başarısız istek taraması.
// Kullanım: node scripts/perf/konsol_tarama.mjs [/yol ...]   (BASE=http://localhost:3000)
import { spawn } from 'node:child_process'; import fs from 'node:fs'; import os from 'node:os';
const BASE = process.env.BASE || 'http://localhost:3000';
const PATHS = process.argv.slice(2).length ? process.argv.slice(2) : ['/', '/cikmis', '/sozluk', '/spotlar', '/hastaliklar', '/kartlar', '/ozetler', '/ogren', '/calis', '/saglik', '/ara'];
const PORT = 9333 + Math.floor(Math.random() * 500); const dir = `${os.tmpdir()}/medsor-konsol-${PORT}`;
const chrome = spawn('/opt/google/chrome/chrome', ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${dir}`, '--window-size=1280,800', '--no-first-run', '--disable-extensions', '--mute-audio', '--disable-gpu'], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
process.on('exit', () => { try { chrome.kill('SIGKILL'); } catch {} try { fs.rmSync(dir, { recursive: true, force: true }); } catch {} });
for (let i = 0; i < 50; i++) { try { await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json(); break; } catch { await sleep(200); } }
const tgt = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: 'PUT' })).json();
const ws = new WebSocket(tgt.webSocketDebuggerUrl); await new Promise((r) => ws.addEventListener('open', r));
let id = 0; const pend = new Map(); let cur = '/'; const out = {};
const add = (m) => { (out[cur] ||= new Set()).add(m.slice(0, 300)); };
ws.addEventListener('message', (m) => {
  const d = JSON.parse(m.data);
  if (d.id && pend.has(d.id)) { pend.get(d.id)(d.result); pend.delete(d.id); return; }
  if (d.method === 'Runtime.exceptionThrown') add('İSTİSNA ' + (d.params.exceptionDetails.exception?.description || d.params.exceptionDetails.text));
  if (d.method === 'Runtime.consoleAPICalled' && d.params.type === 'error') add('console.error ' + d.params.args.map((a) => a.value ?? a.description ?? '').join(' '));
  if (d.method === 'Log.entryAdded' && d.params.entry.level === 'error') add('log ' + d.params.entry.text + ' ' + (d.params.entry.url || ''));
  if (d.method === 'Network.responseReceived' && d.params.response.status >= 400) add(`HTTP ${d.params.response.status} ${d.params.response.url.replace(BASE, '')}`);
});
const send = (method, params = {}) => new Promise((res) => { const i = ++id; pend.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
await send('Page.enable'); await send('Runtime.enable'); await send('Log.enable'); await send('Network.enable');
for (const p of PATHS) { cur = p; await send('Page.navigate', { url: BASE + p }); await sleep(7000); }
for (const p of PATHS) console.log(p, out[p] ? [...out[p]] : 'temiz');
process.exit(0);
