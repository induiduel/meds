// Başsız Chrome + CDP ile yazma/arama başarım ölçümü (2026-10-15 başarım turu).
// Kullanım: node scripts/perf/yazma_olcum.mjs <compose|palette|page:/yol[:seçici]> [cpu yavaşlatma=4] [taban=http://localhost:3000]
// Ortam: TEXT (yazılacak metin), GAP (tuş arası ms), TAIL, PROF=1 (JS profili), TRACE=1|2|3 (iz / geçersizleştirme),
//        DETAIL=1 (en uzun kareler), CSS (deneysel stil enjekte et).
// Ölçüt: long-animation-frame sayısı ve blockSum = kullanıcının hissettiği donma. Gerçek tuş olayları (Input.dispatchKeyEvent).
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';

const SCN = process.argv[2] || 'compose';
const RATE = Number(process.argv[3] || 4);
const BASE = process.argv[4] || 'http://localhost:3000';
const PROFILE = process.env.PROF === '1';
const PORT = 9333 + Math.floor(Math.random() * 500);
const dir = `${os.tmpdir()}/medsor-perf-chrome-${PORT}`;

const chrome = spawn('/opt/google/chrome/chrome', [
  '--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${dir}`, '--window-size=1280,800',
  '--no-first-run', '--no-default-browser-check', '--disable-extensions', '--mute-audio', '--disable-gpu',
], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const cleanup = () => { try { chrome.kill('SIGKILL'); } catch {} try { fs.rmSync(dir, { recursive: true, force: true }); } catch {} };
process.on('exit', cleanup);

let ver;
for (let i = 0; i < 50; i++) { try { ver = await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json(); break; } catch { await sleep(200); } }
const tgt = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: 'PUT' })).json();
const ws = new WebSocket(tgt.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener('open', r));
let id = 0; const pend = new Map(); const listeners = [];
ws.addEventListener('message', (m) => {
  const d = JSON.parse(m.data);
  if (d.id && pend.has(d.id)) { const p = pend.get(d.id); pend.delete(d.id); d.error ? p.rej(new Error(JSON.stringify(d.error))) : p.res(d.result); }
  else if (d.method) listeners.forEach((l) => l(d));
});
const send = (method, params = {}) => new Promise((res, rej) => { const i = ++id; pend.set(i, { res, rej }); ws.send(JSON.stringify({ id: i, method, params })); });
const ev = async (expr) => { const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true }); if (r.exceptionDetails) throw new Error(JSON.stringify(r.exceptionDetails).slice(0, 400)); return r.result.value; };

await send('Page.enable'); await send('Runtime.enable');
await send('Emulation.setDeviceMetricsOverride', { width: 1280, height: 800, deviceScaleFactor: 1, mobile: false });
const go = async (path) => { await send('Page.navigate', { url: BASE + path }); await sleep(1500); for (let i = 0; i < 40; i++) { if (await ev(`!!document.querySelector('.sh-main, main') && !document.getElementById('app-splash')`).catch(() => false)) break; await sleep(250); } await sleep(2500); };

const installObs = () => ev(`(() => { window.__loaf = []; new PerformanceObserver((l) => { for (const e of l.getEntries()) window.__loaf.push({ d: e.duration, b: e.blockingDuration, sl: e.styleAndLayoutStart ? e.startTime + e.duration - e.styleAndLayoutStart : 0, r: e.renderStart ? e.startTime + e.duration - e.renderStart : 0, s: (e.scripts || []).map((s) => ({ inv: s.invoker, f: (s.sourceURL || '').split('/').pop() + ':' + (s.sourceFunctionName || '') + '@' + s.sourceCharPosition, d: s.duration, fl: s.forcedStyleAndLayoutDuration })) }); }).observe({ type: 'long-animation-frame' }); return 1; })()`);
const typeText = async (text, gap = 110) => { for (const ch of text) { await send('Input.dispatchKeyEvent', { type: 'keyDown', key: ch, text: ch, unmodifiedText: ch }); await send('Input.dispatchKeyEvent', { type: 'keyUp', key: ch }); await sleep(gap); } };
const report = async (label, t0) => {
  const L = await ev('window.__loaf');
  const sum = (a, f) => Math.round(a.reduce((x, y) => x + f(y), 0));
  const scripts = new Map();
  for (const e of L) for (const s of e.s) scripts.set(s.f + ' [' + s.inv + ']', (scripts.get(s.f + ' [' + s.inv + ']') || 0) + s.d);
  const out = {
    label, cpu: RATE, wallMs: Date.now() - t0, loafN: L.length, loafSum: sum(L, (e) => e.d), blockSum: sum(L, (e) => e.b), styleLayoutSum: sum(L, (e) => e.sl),
    scriptSum: sum(L, (e) => e.s.reduce((x, s) => x + s.d, 0)), forcedSL: sum(L, (e) => e.s.reduce((x, s) => x + (s.fl || 0), 0)),
    worst: L.map((e) => Math.round(e.d)).sort((a, b) => b - a).slice(0, 6),
    topScripts: [...scripts].sort((a, b) => b[1] - a[1]).slice(0, 8).map(([k, v]) => Math.round(v) + 'ms ' + k),
  };
  console.log(JSON.stringify(out, null, 1)); if (process.env.DETAIL) console.log(JSON.stringify(L.sort((a,b)=>b.d-a.d).slice(0,6).map(e=>({d:Math.round(e.d),b:Math.round(e.b),render:Math.round(e.r),sl:Math.round(e.sl),scr:e.s.map(s=>s.inv+' '+s.f+' '+Math.round(s.d))}))));
};
const trace = async (fn) => {
  const evs = []; let done;
  const fin = new Promise((r) => (done = r));
  listeners.push((d) => { if (d.method === 'Tracing.dataCollected') evs.push(...d.params.value); if (d.method === 'Tracing.tracingComplete') done(); });
  await send('Tracing.start', { categories: 'devtools.timeline,disabled-by-default-devtools.timeline,disabled-by-default-devtools.timeline.invalidationTracking,v8.execute,blink.user_timing', transferMode: 'ReportEvents' });
  await fn();
  await send('Tracing.end'); await fin;
  const main = evs.filter((e) => e.name === 'RunTask' && e.dur > 40000);
  // her uzun görevin içindeki olayları adlarına göre topla (yalnız ana iş parçacığı: görevle aynı tid)
  const agg = new Map();
  for (const t of main) {
    const kids = evs.filter((e) => e.tid === t.tid && e.pid === t.pid && e.ts >= t.ts && e.ts <= t.ts + t.dur && e !== t);
    for (const k of kids) { const key = k.name + (k.args?.data?.type ? ':' + k.args.data.type : '') + (k.args?.data?.url ? ' ' + String(k.args.data.url).split('/').pop() : ''); agg.set(key, (agg.get(key) || 0) + (k.dur || 0) / 1000); }
    if (process.env.TRACE === '2' && t === main.sort((a,b)=>b.dur-a.dur)[0]) console.log('KIDS', JSON.stringify(kids.slice(0,80).map((k)=>[k.name,k.ph,Math.round((k.dur||0)/1000),Math.round((k.ts-t.ts)/1000), k.args?.data?.url?String(k.args.data.url).split('/').pop():(k.args?.data?.type||'')])));
  }
  if (process.env.TRACE === '3') {
    const ult = evs.filter((e) => e.name === 'UpdateLayoutTree' && e.dur > 5000).map((e) => ({ ms: Math.round(e.dur / 1000), n: e.args?.elementCount ?? e.args?.data?.elementCount }));
    console.log('ULT', JSON.stringify(ult.slice(0, 12)));
    const lay = evs.filter((e) => e.name === 'Layout' && e.dur > 5000).map((e) => ({ ms: Math.round(e.dur / 1000), dirty: e.args?.beginData?.dirtyObjects, total: e.args?.beginData?.totalObjects }));
    console.log('LAYOUT', JSON.stringify(lay.slice(0, 12)));
    const ia = new Map();
    for (const e of evs) {
      if (!/Invalidat/.test(e.name)) continue;
      const d = e.args?.data || {};
      const k = [e.name, d.reason || d.changedClass || d.changedAttribute || d.changedPseudo || d.changedId || '', d.nodeName || '', String(d.extraData || (Array.isArray(d.selectors) ? d.selectors.map((x) => x.selector).join(';') : '') || '').slice(0, 140)].join(' | ');
      ia.set(k, (ia.get(k) || 0) + 1);
    }
    console.log('INVALIDATIONS', JSON.stringify([...ia].sort((a, b) => b[1] - a[1]).slice(0, 30), null, 1));
  }
  console.log('LONG TASKS', main.length, main.map((t) => Math.round(t.dur / 1000)).sort((a, b) => b - a).slice(0, 8));
  console.log('INSIDE (ms, nested sums):', JSON.stringify([...agg].sort((a, b) => b[1] - a[1]).slice(0, 25).map(([k, v]) => Math.round(v) + ' ' + k), null, 1));
};
const prof = async (fn) => {
  if (process.env.TRACE) return trace(fn);
  if (!PROFILE) return fn();
  await send('Profiler.enable'); await send('Profiler.setSamplingInterval', { interval: 200 }); await send('Profiler.start');
  await fn();
  const { profile } = await send('Profiler.stop');
  const byId = new Map(profile.nodes.map((n) => [n.id, n]));
  const self = new Map(); const dt = profile.timeDeltas; const total = new Map();
  profile.samples.forEach((sid, i) => { const n = byId.get(sid); const cf = n.callFrame; const k = `${cf.functionName || '(anon)'} ${cf.url.split('/').pop()}:${cf.lineNumber}:${cf.columnNumber}`; self.set(k, (self.get(k) || 0) + (dt[i] || 0)); });
  const top = [...self].filter(([k]) => !k.startsWith('(idle)') && !k.startsWith('(program)')).sort((a, b) => b[1] - a[1]).slice(0, 25).map(([k, v]) => (v / 1000).toFixed(0) + 'ms ' + k);
  console.log('PROFILE self:', JSON.stringify(top, null, 1));
  console.log('(program)/(gc):', [...self].filter(([k]) => /^\((program|garbage)/.test(k)).map(([k, v]) => k.split(' ')[0] + ' ' + (v / 1000).toFixed(0) + 'ms').join(', '));
};

try {
  await send('Emulation.setCPUThrottlingRate', { rate: 1 });
  if (SCN === 'compose') {
    await go('/');
    await ev(`document.querySelector('textarea').click(), document.querySelector('textarea').focus(), 1`); await sleep(1200);
    await ev(`(document.activeElement.tagName === 'TEXTAREA' ? 1 : document.querySelector('textarea').focus(), 1)`);
  } else if (SCN === 'palette') {
    await go('/');
    await ev(`document.querySelector('.s12-rail-search, .sh-side-search').click(), 1`); await sleep(1000);
  } else if (SCN.startsWith('page:')) {
    const [, path, sel] = SCN.split(':');
    await go(path); await sleep(2000);
    const ok = await ev(`(() => { const el = document.querySelector(${JSON.stringify(sel || 'main input[type="search"], main input[data-page-search], .cx-dock input, main input')}); if (!el) return 'yok'; el.scrollIntoView({block:'center'}); el.click(); el.focus(); return el.outerHTML.slice(0, 160); })()`);
    console.log('input:', ok); await sleep(800);
  }
  const text = process.env.TEXT || 'kolesistit tedavisinde ilk tercih';
  await send('Emulation.setCPUThrottlingRate', { rate: RATE });
  if (process.env.CSS) { await ev(`(() => { const s = document.createElement('style'); s.textContent = ${JSON.stringify(process.env.CSS)}; document.head.appendChild(s); return 1; })()`); await sleep(500); }
  await installObs(); await sleep(300);
  const t0 = Date.now();
  await prof(async () => { await typeText(text, Number(process.env.GAP || 110)); await sleep(Number(process.env.TAIL || 2500)); });
  await report(SCN, t0);
  console.log('dom:', await ev('document.getElementsByTagName("*").length'));
} catch (e) { console.error('HATA', e.message); }
cleanup(); process.exit(0);
