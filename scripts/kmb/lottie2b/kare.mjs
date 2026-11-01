#!/usr/bin/env node
/**
 * Herhangi bir Lottie JSON'undan kare(ler) alır (lottie-web canvas, başsız Chrome).
 *   node scripts/kmb/lottie2b/kare.mjs <dosya.json> [--t=0.5,3,7] [--out=klasör] [--w=800]
 * Çıktı: <out>/<ad>-<t>.png (zemin beyaz). Oynatıcının HTML etiket katmanı çizilmez (onun için kare_onizle.mjs).
 */
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const MEDS = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const args = process.argv.slice(2);
const opt = Object.fromEntries(args.filter((a) => a.startsWith('--')).map((a) => { const [k, ...v] = a.slice(2).split('='); return [k, v.length ? v.join('=') : '1']; }));
const dosyalar = args.filter((a) => !a.startsWith('--'));
const OUT = opt.out || path.join(process.env.TMPDIR || '/tmp', 'kmb-kare2b'); fs.mkdirSync(OUT, { recursive: true });
const W = Number(opt.w || 800), H = Math.round(W * 5 / 8);
const TS = (opt.t || '0.5').split(',').map(Number);
const PORT = 9550 + Math.floor(Math.random() * 40);
const dir = path.join(OUT, `.chrome-${PORT}`);
const chrome = spawn('/opt/google/chrome/chrome', ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${dir}`, '--no-first-run', '--disable-extensions', '--mute-audio', '--hide-scrollbars', '--allow-file-access-from-files', `--window-size=${W + 20},${H + 20}`], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
process.on('exit', () => { try { chrome.kill('SIGKILL'); } catch {} try { fs.rmSync(dir, { recursive: true, force: true }); } catch {} });
for (let i = 0; i < 60; i++) { try { await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json(); break; } catch { await sleep(200); } }
const tgt = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: 'PUT' })).json();
const ws = new WebSocket(tgt.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener('open', r));
let id = 0; const pend = new Map();
ws.addEventListener('message', (m) => { const d = JSON.parse(m.data); if (d.id && pend.has(d.id)) { const p = pend.get(d.id); pend.delete(d.id); d.error ? p.rej(new Error(JSON.stringify(d.error))) : p.res(d.result); } else if (d.method === 'Runtime.exceptionThrown') console.error('sayfa hatası:', d.params.exceptionDetails?.exception?.description?.slice(0, 300)); });
const send = (method, params = {}) => new Promise((res, rej) => { const i = ++id; pend.set(i, { res, rej }); ws.send(JSON.stringify({ id: i, method, params })); });
const ev = async (expr) => { const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true }); if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description); return r.result?.value; };
await send('Page.enable'); await send('Runtime.enable');
await send('Emulation.setDeviceMetricsOverride', { width: W + 20, height: H + 20, deviceScaleFactor: 1, mobile: false });
const sayfa = path.join(OUT, '.kare.html');
fs.writeFileSync(sayfa, `<!doctype html><meta charset="utf-8"><style>body{margin:0;background:#fff}#k{width:${W}px;height:${H}px}</style><body><div id="k"></div>
<script src="file://${path.join(MEDS, 'node_modules/lottie-web/build/player/lottie_canvas.min.js')}"></script><script>
let a=null;async function yukle(v){if(a)a.destroy();const k=document.getElementById('k');k.innerHTML='';a=lottie.loadAnimation({container:k,renderer:'canvas',loop:false,autoplay:false,animationData:v,rendererSettings:{clearCanvas:true,preserveAspectRatio:'xMidYMid meet'}});
 await new Promise(r=>{if(a.isLoaded)r();else a.addEventListener('DOMLoaded',r);});return a.totalFrames;}
function git(t){a.goToAndStop(Math.min(a.totalFrames-1,Math.round(t*30)),true);return a.currentFrame;}
</script>`);
await send('Page.navigate', { url: 'file://' + sayfa }); await sleep(800);
for (const f of dosyalar) {
  const veri = fs.readFileSync(f, 'utf8');
  const ad = path.basename(f, '.json');
  const n = await ev(`yukle(${veri})`);
  for (const t of TS) {
    await ev(`git(${t})`); await sleep(120);
    const shot = await send('Page.captureScreenshot', { format: 'png', clip: { x: 0, y: 0, width: W, height: H, scale: 1 } });
    const dosya = path.join(OUT, `${ad}-${t}.png`);
    fs.writeFileSync(dosya, Buffer.from(shot.data, 'base64'));
    console.log(`${ad} t=${t} (${n} kare) → ${dosya}`);
  }
}
ws.close();
process.exit(0);
