#!/usr/bin/env node
/**
 * KMB 3B sahne önizlemesi — başsız Chrome (WebGL/SwiftShader) ile /kmb?sahne=… adresinden yüksek çözünürlüklü kare alır.
 *   node scripts/kmb/sahne3b_onizle.mjs [sahne…] [--goster] [--etiket] [--odak=id] [--eylem='[...]'] [--w=1600] [--out=klasör]
 * Varsayılan: 3B'si olan tüm sahneler, gizli ögeler açık + etiketli. Sunucu 3000 çalışıyor olmalı; giriş ai-test çereziyle (.env MEDS_PANEL_SECRET).
 */
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const MEDS = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const args = process.argv.slice(2);
const opt = Object.fromEntries(args.filter((a) => a.startsWith('--')).map((a) => { const [k, ...v] = a.slice(2).split('='); return [k, v.length ? v.join('=') : '1']; }));
let sahneler = args.filter((a) => !a.startsWith('--'));
if (!sahneler.length) { sahneler = ['foley', 'yakin-mesane', 'erkek', 'yakin-uretra', 'mesane', 'kadin', 'yakin-kadin', 'yakin-el', 'yakin-erkek-jel', 'malzeme', 'foley-kesit', 'travma', 'pozisyon', 'maket']; }
const OUT = opt.out || path.join(process.env.TMPDIR || '/tmp', 'kmb_sahne3b'); fs.mkdirSync(OUT, { recursive: true });
const W = Number(opt.w || 1600), H = Math.round(W * 5 / 8);
const secret = (fs.readFileSync(path.join(MEDS, '.env'), 'utf8').match(/^MEDS_PANEL_SECRET=(.*)$/m) || [])[1]?.replace(/"/g, '').trim();
const PORT = 9700 + Math.floor(Math.random() * 150);
const dir = path.join(OUT, `.chrome-${PORT}`);
const chrome = spawn('/opt/google/chrome/chrome', ['--headless=new', '--disable-gpu-vsync', `--remote-debugging-port=${PORT}`, `--user-data-dir=${dir}`, '--no-first-run', '--disable-extensions', '--mute-audio', '--hide-scrollbars',
  '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', `--window-size=${W},${H + 40}`], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
process.on('exit', () => { try { chrome.kill('SIGKILL'); } catch {} try { fs.rmSync(dir, { recursive: true, force: true }); } catch {} });
for (let i = 0; i < 60; i++) { try { await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json(); break; } catch { await sleep(200); } }
const tgt = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: 'PUT' })).json();
const ws = new WebSocket(tgt.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener('open', r));
let id = 0; const pend = new Map();
ws.addEventListener('message', (m) => { const d = JSON.parse(m.data); if (d.id && pend.has(d.id)) { const p = pend.get(d.id); pend.delete(d.id); d.error ? p.rej(new Error(JSON.stringify(d.error))) : p.res(d.result); } else if (d.method === 'Runtime.exceptionThrown') console.error('sayfa hatası:', d.params.exceptionDetails?.exception?.description?.slice(0, 900)); });
const send = (method, params = {}) => new Promise((res, rej) => { const i = ++id; pend.set(i, { res, rej }); ws.send(JSON.stringify({ id: i, method, params })); });
await send('Page.enable'); await send('Runtime.enable'); await send('Network.enable');
await send('Emulation.setDeviceMetricsOverride', { width: W, height: H + 40, deviceScaleFactor: 1, mobile: false });
// giriş: ai-test çerezi
await send('Page.navigate', { url: 'http://localhost:3000/' }); await sleep(1500);
await send('Runtime.evaluate', { expression: `localStorage.setItem('medsoru_giris_uyarisi_v1', JSON.stringify({surum:1,at:new Date().toISOString()})); localStorage.setItem('medsoru_kmb_3b', ${opt.uc ? "'1'" : "'0'"}); fetch('/api/ai-test/oturum',{method:'POST',headers:{'x-panel-secret':${JSON.stringify(secret || '')}}}).then(r=>r.status)`, awaitPromise: true, returnByValue: true });
/** Tek kare: sahne + durum (eylem listesi) + odak → png */
async function kare(ad, sahne, eylem, odak, goster) {
  const q = new URLSearchParams({ sahne, w: String(W) });
  if (goster) { q.set('goster', '1'); q.set('etiket', '1'); }
  if (odak) q.set('odak', odak); if (eylem?.length) q.set('eylem', JSON.stringify(eylem));
  await send('Page.navigate', { url: `http://localhost:3000/kmb?${q}` });
  await sleep(Number(opt.bekle || 4000));
  const r = await send('Runtime.evaluate', { expression: `(()=>{const e=document.querySelector('.kmb-3b, .kmb-sahne');if(!e)return null;const b=e.getBoundingClientRect();return {x:b.left,y:b.top,w:b.width,h:b.height,uc:!!document.querySelector('.kmb-3b canvas')}})()`, returnByValue: true });
  const b = r.result?.value; if (!b) { console.error(ad, 'sahne bulunamadı'); return; }
  const shot = await send('Page.captureScreenshot', { format: 'png', clip: { x: b.x, y: b.y, width: b.w, height: b.h, scale: 1 } });
  const dosya = path.join(OUT, `${ad}.png`);
  fs.writeFileSync(dosya, Buffer.from(shot.data, 'base64'));
  console.log(`${ad}: ${b.uc ? '3B' : 'SVG'} → ${dosya}`);
}
if (opt.film || opt.hedef) {
  // Hedefler filmi vuruşları: 02.json hedefCalisma[].film — öğrencinin gördüğü gerçek durum (sahne değişince durum sıfırlanır, eylem birikir)
  const ders = JSON.parse(fs.readFileSync(path.join(MEDS, 'src/data/kmb/02.json'), 'utf8'));
  for (const k of ders.hedefCalisma) {
    if (opt.hedef && Number(opt.hedef) !== k.no) continue;
    let sahne = k.sahne, eylem = [];
    for (let i = 0; i < (k.film || []).length; i++) {
      const v = k.film[i];
      if (v.sahne && v.sahne !== sahne) { sahne = v.sahne; eylem = []; }
      eylem = [...eylem, ...(v.eylem || [])];
      if (sahneler.length && !sahneler.includes(sahne) && process.argv.slice(2).some((a) => !a.startsWith('--'))) continue;
      await kare(`h${String(k.no).padStart(2, '0')}-${i}-${sahne}`, sahne, eylem, v.odak, false);
    }
  }
} else {
  for (const sahne of sahneler) await kare(sahne + (opt.goster ? '-tum' : ''), sahne, opt.eylem ? JSON.parse(opt.eylem) : [], opt.odak, !!opt.goster);
}
process.exit(0);
