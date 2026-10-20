// Sayfa × boyut taraması: ekran görüntüsü + yatay taşma / küçük dokunma hedefi / adsız düğme / konsol hatası (raw CDP, başsız Chrome)
// Kullanım: node scripts/perf/sayfa_tarama.mjs   (BASE=http://localhost:3000, OUT=klasör, ROUTES=/a,/b, VPS=375x812m,1440x900, WAIT=ms, FULL=1, SEED="s('anahtar','değer');")
// Çıktı: OUT/<boyut>_<rota>.jpg + OUT/report.json. Turlar/giriş uyarısı localStorage ile atlanır. 'm' ekli boyut = dokunmatik telefon.
// Not: ::after ile büyütülmüş dokunma alanlarını ve satırı kaplayan bağlantıları göremez; 'small' listesini gözle süz.
import { spawn } from 'node:child_process';
import fs from 'node:fs';

const BASE = process.env.BASE || 'http://localhost:3000';
const OUT = process.env.OUT || `${process.env.TMPDIR || '/tmp'}/medsor-sayfa-tarama`;
const ROUTES = (process.env.ROUTES || '/bugun,/ogren,/sinav-calisma,/cikmis,/sorular,/kartlar,/test,/canliders,/notlar,/sozluk,/hastaliklar,/saglik,/spotlar,/spotlar?gorunum=onem,/spotlar?gorunum=cozucu,/kazanimlar,/ozetler,/calis,/ornek-sorular,/istatistik,/ayarlar,/siralama,/harita,/muzik,/').split(',');
const VPS = (process.env.VPS || '375x812m,820x1180m,1440x900').split(',').map((s) => { const m = s.match(/(\d+)x(\d+)(m?)/); return { w: +m[1], h: +m[2], mobile: !!m[3], tag: s }; });
const FULL = process.env.FULL === '1';
fs.mkdirSync(OUT, { recursive: true });
const PORT = 9400 + Math.floor(Math.random() * 400);
const dir = `/tmp/claude-1000/sweep-chrome-${PORT}`;
const chrome = spawn('/opt/google/chrome/chrome', ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${dir}`, '--no-first-run', '--disable-extensions', '--mute-audio', '--hide-scrollbars'], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
process.on('exit', () => { try { chrome.kill('SIGKILL'); } catch {} try { fs.rmSync(dir, { recursive: true, force: true }); } catch {} });
for (let i = 0; i < 50; i++) { try { await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json(); break; } catch { await sleep(200); } }
const tgt = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: 'PUT' })).json();
const ws = new WebSocket(tgt.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener('open', r));
let id = 0; const pend = new Map(); const errs = [];
ws.addEventListener('message', (m) => {
  const d = JSON.parse(m.data);
  if (d.id && pend.has(d.id)) { const p = pend.get(d.id); pend.delete(d.id); d.error ? p.rej(new Error(JSON.stringify(d.error))) : p.res(d.result); }
  else if (d.method === 'Runtime.exceptionThrown') errs.push(d.params.exceptionDetails?.exception?.description?.slice(0, 200) || 'exception');
  else if (d.method === 'Runtime.consoleAPICalled' && d.params.type === 'error') errs.push(d.params.args.map((a) => a.value ?? a.description ?? '').join(' ').slice(0, 200));
});
const send = (method, params = {}) => new Promise((res, rej) => { const i = ++id; pend.set(i, { res, rej }); ws.send(JSON.stringify({ id: i, method, params })); });
const ev = async (expr) => { const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true }); return r.result?.value; };
await send('Page.enable'); await send('Runtime.enable');
// Zorunlu giriş: AI_COOKIE=<meds_ai_test değeri> (POST /api/ai-test/oturum, x-panel-secret) ile test oturumu
if (process.env.AI_COOKIE) { await send('Network.enable'); await send('Network.setCookie', { name: 'meds_ai_test', value: process.env.AI_COOKIE, url: BASE, httpOnly: true, sameSite: 'Strict' }); }

const SEED = `(() => { const now = new Date().toISOString();
  const s = (k, v) => localStorage.setItem(k, v);
  s('medsoru_user_registered','1'); s('medsoru_giris_uyarisi_v1', JSON.stringify({surum:1,at:now}));
  ['medsoru_tour_v1','medsoru_canli_ders_tur_ders_v1','medsoru_canli_ders_tur_liste_v1','medsoru_canli_ders_tv_tanitim_v1','medsoru_learn_tour_lesson_v1','medsoru_learn_tour_library_v1','medsoru_splash_seen'].forEach(k => s(k, JSON.stringify({done:true,at:now,surum:9})));
  ${process.env.SEED || ''}
})()`;

await send('Page.navigate', { url: BASE + '/favicon.ico' }); await sleep(800);
await ev(SEED);
const report = [];
const AUDIT = `(() => {
  const vw = innerWidth, out = [];
  const docOver = document.documentElement.scrollWidth - vw;
  const offenders = [];
  for (const el of document.querySelectorAll('body *')) {
    const r = el.getBoundingClientRect(); if (!r.width || !r.height) continue;
    if (r.right > vw + 2 || r.left < -2) {
      const cs = getComputedStyle(el); if (cs.position === 'fixed' && cs.visibility === 'hidden') continue;
      let p = el.parentElement, clipped = false;
      while (p && p !== document.body) { const o = getComputedStyle(p).overflowX; if (o !== 'visible') { clipped = true; break; } p = p.parentElement; }
      if (!clipped) offenders.push((el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\\s+/).slice(0,2).join('.') : el.tagName) + '@' + Math.round(r.right));
    }
  }
  const small = [], unnamed = [];
  for (const el of document.querySelectorAll('button, a[href], [role=button], [role=tab], input, select')) {
    const r = el.getBoundingClientRect(); if (!r.width || !r.height) continue;
    if (getComputedStyle(el).visibility === 'hidden') continue;
    if ((r.width < 24 || r.height < 24) && el.type !== 'checkbox' && el.type !== 'radio') small.push((el.getAttribute('aria-label') || el.textContent || el.className || el.tagName).toString().trim().slice(0, 30) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height));
    const name = (el.getAttribute('aria-label') || el.getAttribute('title') || el.textContent || el.getAttribute('aria-labelledby') || el.getAttribute('placeholder') || (el.labels && el.labels[0] && el.labels[0].textContent) || '').trim();
    if (!name && el.type !== 'hidden') unnamed.push((typeof el.className === 'string' ? el.className.slice(0, 40) : el.tagName));
  }
  const fonts = {}; for (const el of document.querySelectorAll('main *, .sh-main *')) { if (!el.childNodes.length || el.children.length) continue; const f = getComputedStyle(el).fontFamily.split(',')[0].replace(/"/g,''); fonts[f] = (fonts[f]||0)+1; }
  const imgs = [...document.querySelectorAll('img:not([alt])')].length;
  return { docOver, offenders: [...new Set(offenders)].slice(0, 12), small: [...new Set(small)].slice(0, 15), smallN: small.length, unnamed: [...new Set(unnamed)].slice(0, 10), unnamedN: unnamed.length, imgs, fonts, h: document.documentElement.scrollHeight };
})()`;

for (const vp of VPS) {
  await send('Emulation.setDeviceMetricsOverride', { width: vp.w, height: vp.h, deviceScaleFactor: 1, mobile: vp.mobile });
  await send('Emulation.setTouchEmulationEnabled', { enabled: vp.mobile });
  for (const route of ROUTES) {
    errs.length = 0;
    await send('Page.navigate', { url: BASE + route });
    await sleep(+(process.env.WAIT || 3500));
    // açık kalan tur/diyalogları kapat
    await ev(`document.querySelectorAll('[aria-label="Kapat"],[aria-label="Turu kapat"],[aria-label="Atla"]').forEach(b => { if (b.closest('[class*=tur],[class*=tour]')) b.click(); }); 1`);
    await sleep(300);
    const a = await ev(AUDIT);
    const name = `${vp.tag}_${route.replace(/[/?=&]+/g, '_').replace(/^_|_$/g, '') || 'root'}`;
    const shot = await send('Page.captureScreenshot', { format: 'jpeg', quality: 60, captureBeyondViewport: FULL, ...(FULL ? { clip: { x: 0, y: 0, width: vp.w, height: Math.min(a?.h || vp.h, 4000), scale: 1 } } : {}) });
    fs.writeFileSync(`${OUT}/${name}.jpg`, Buffer.from(shot.data, 'base64'));
    report.push({ name, ...a, errs: [...new Set(errs)].slice(0, 5) });
    console.log(name, JSON.stringify({ over: a?.docOver, off: a?.offenders, smallN: a?.smallN, unnamedN: a?.unnamedN, errs: errs.length }));
  }
}
fs.writeFileSync(`${OUT}/report.json`, JSON.stringify(report, null, 1));
process.exit(0);
