#!/usr/bin/env node
/**
 * KMB 2B sahnelerini SVG olarak dışa aktarır (Lottie 2B hattının tek kaynağı: components/kmb/sahneler*.tsx).
 *   node scripts/kmb/lottie2b/svg_disa.mjs [sahne…]      → scripts/kmb/lottie2b/svg/<sahne>.svg + bbox.json
 * Başsız Chrome ile /kmb?sahne=<ad>&goster=1 (tüm ögeler görünür) açılır; svg.kmb-sahne'nin işaretlemesi ve her
 * `[data-id]` ögesinin getBBox kutusu alınır. Sunucu 3000 çalışıyor olmalı (dist güncel: `npx vite build`).
 */
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const MEDS = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const OUT = path.join(MEDS, 'scripts/kmb/lottie2b/svg');
fs.mkdirSync(OUT, { recursive: true });
const TUM = ['foley', 'mesane', 'erkek', 'travma', 'malzeme', 'pozisyon', 'kadin', 'yakin-mesane', 'yakin-uretra', 'yakin-kadin', 'yakin-el', 'yakin-erkek-jel', 'foley-kesit', 'maket'];
const sahneler = process.argv.slice(2).filter((a) => !a.startsWith('--'));
const secili = sahneler.length ? sahneler : TUM;
const secret = (fs.readFileSync(path.join(MEDS, '.env'), 'utf8').match(/^MEDS_PANEL_SECRET=(.*)$/m) || [])[1]?.replace(/"/g, '').trim();
const PORT = 9600 + Math.floor(Math.random() * 90);
const dir = path.join(process.env.TMPDIR || '/tmp', `kmb-svg-${PORT}`);
const chrome = spawn('/opt/google/chrome/chrome', ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${dir}`, '--no-first-run', '--disable-extensions', '--mute-audio', '--hide-scrollbars', '--window-size=1000,700'], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
process.on('exit', () => { try { chrome.kill('SIGKILL'); } catch {} try { fs.rmSync(dir, { recursive: true, force: true }); } catch {} });
for (let i = 0; i < 60; i++) { try { await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json(); break; } catch { await sleep(200); } }
const tgt = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: 'PUT' })).json();
const ws = new WebSocket(tgt.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener('open', r));
let id = 0; const pend = new Map();
ws.addEventListener('message', (m) => { const d = JSON.parse(m.data); if (d.id && pend.has(d.id)) { const p = pend.get(d.id); pend.delete(d.id); d.error ? p.rej(new Error(JSON.stringify(d.error))) : p.res(d.result); } });
const send = (method, params = {}) => new Promise((res, rej) => { const i = ++id; pend.set(i, { res, rej }); ws.send(JSON.stringify({ id: i, method, params })); });
const ev = async (expr) => { const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true }); if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description); return r.result?.value; };
await send('Page.enable'); await send('Runtime.enable');
await send('Page.navigate', { url: 'http://localhost:3000/' }); await sleep(1500);
await ev(`localStorage.setItem('medsoru_giris_uyarisi_v1', JSON.stringify({surum:1,at:new Date().toISOString()})); localStorage.setItem('medsoru_kmb_3b','0'); fetch('/api/ai-test/oturum',{method:'POST',headers:{'x-panel-secret':${JSON.stringify(secret || '')}}}).then(r=>r.status)`);
const bbox = fs.existsSync(path.join(OUT, 'bbox.json')) ? JSON.parse(fs.readFileSync(path.join(OUT, 'bbox.json'), 'utf8')) : {};
for (const s of secili) {
  await send('Page.navigate', { url: `http://localhost:3000/kmb?sahne=${s}&goster=1&w=800` });
  await sleep(3500);
  const r = await ev(`(()=>{const svg=document.querySelector('svg.kmb-sahne');if(!svg)return null;const b={};
    for(const g of svg.querySelectorAll('[data-id]')){const x=g.getBBox();b[g.dataset.id]=[+x.x.toFixed(1),+x.y.toFixed(1),+x.width.toFixed(1),+x.height.toFixed(1)];}
    return {svg:svg.outerHTML,b};})()`);
  if (!r) { console.error(`${s}: sahne bulunamadı`); continue; }
  fs.writeFileSync(path.join(OUT, `${s}.svg`), r.svg + '\n');
  bbox[s] = r.b;
  console.log(`${s}: ${(r.svg.length / 1024).toFixed(0)} KB, ${Object.keys(r.b).length} öge`);
}
fs.writeFileSync(path.join(OUT, 'bbox.json'), JSON.stringify(bbox, null, 1) + '\n');
ws.close();
process.exit(0);
