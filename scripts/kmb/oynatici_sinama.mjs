// KMB oynatıcı jest sınaması (H461): başsız Chrome'da gerçek dokunma/fare olaylarıyla 26 senaryo (tek/çift/üçlü dokunuş,
// basılı tutma, kaydırma, cümle menüsü, adım sonu sorusu, tam ekran ders videosu, fare tık/çift tık).
// Kullanım: AI_COOKIE=<meds_ai_test> [BASE=http://localhost:3000] [OUT=klasör] node meds/scripts/kmb/oynatici_sinama.mjs
import { spawn } from 'node:child_process';
import fs from 'node:fs';
const BASE = process.env.BASE || 'http://localhost:3000';
const PORT = 9800 + Math.floor(Math.random() * 100);
const dir = `/tmp/claude-1000/jest-chrome-${PORT}`;
const chrome = spawn('/opt/google/chrome/chrome', ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${dir}`, '--no-first-run', '--mute-audio', '--autoplay-policy=no-user-gesture-required'], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
process.on('exit', () => { try { chrome.kill('SIGKILL'); } catch {} try { fs.rmSync(dir, { recursive: true, force: true }); } catch {} });
for (let i = 0; i < 50; i++) { try { await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json(); break; } catch { await sleep(200); } }
const tgt = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: 'PUT' })).json();
const ws = new WebSocket(tgt.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener('open', r));
let id = 0; const pend = new Map(); const errs = [];
ws.addEventListener('message', (m) => { const d = JSON.parse(m.data); if (d.id && pend.has(d.id)) { const p = pend.get(d.id); pend.delete(d.id); d.error ? p.rej(new Error(JSON.stringify(d.error))) : p.res(d.result); } else if (d.method === 'Runtime.exceptionThrown') errs.push(d.params.exceptionDetails?.exception?.description?.slice(0, 200)); });
const send = (method, params = {}) => new Promise((res, rej) => { const i = ++id; pend.set(i, { res, rej }); ws.send(JSON.stringify({ id: i, method, params })); });
const ev = async (e) => (await send('Runtime.evaluate', { expression: e, awaitPromise: true, returnByValue: true })).result?.value;
await send('Page.enable'); await send('Runtime.enable'); await send('Network.enable');
await send('Network.setCookie', { name: 'meds_ai_test', value: process.env.AI_COOKIE, url: BASE, httpOnly: true, sameSite: 'Strict' });
const SEED = `(() => { const now = new Date().toISOString(); const s = (k, v) => localStorage.setItem(k, v);
  s('medsoru_user_registered','1'); s('medsoru_giris_uyarisi_v1', JSON.stringify({surum:1,at:now}));
  ['medsoru_tour_v1','medsoru_splash_seen'].forEach(k => s(k, JSON.stringify({done:true,at:now,surum:9}))); })()`;
await send('Page.navigate', { url: BASE + '/favicon.ico' }); await sleep(600); await ev(SEED);

const sonuc = []; const kontrol = (ad, ok, ayrinti = '') => { sonuc.push({ ad, ok: !!ok, ayrinti }); console.log(`${ok ? 'GEÇTİ' : 'KALDI'}  ${ad}${ayrinti ? '  · ' + ayrinti : ''}`); };
const durum = () => ev(`(() => { const l = document.querySelector('.kmb-ogret .kmb-lv'); return l ? { gizli: l.classList.contains('gizli'), calan: l.classList.contains('calan'), sure: l.querySelector('.kmb-lv-sure')?.textContent, rozet: !!l.querySelector('.kmb-lv-rozet'), kayma: !!l.querySelector('.kmb-lv-kayma'), menu: !!l.querySelector('.kmb-lv-menu'), tam: l.classList.contains('tam') } : null })()`);
const kutu = () => ev(`(() => { const r = document.querySelector('.kmb-ogret .kmb-lv-sahne').getBoundingClientRect(); return { x: r.left, y: r.top, w: r.width, h: r.height } })()`);
const sn = (s) => { const [m, x] = s.split(' / ')[0].split(':').map(Number); return m * 60 + x; };

// ———— tam ekran ders videosu (yatay telefon)
await send('Emulation.setDeviceMetricsOverride', { width: 812, height: 375, deviceScaleFactor: 2, mobile: true });
await send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
await send('Page.navigate', { url: BASE + '/dersler/kmb/uretral-kateter' }); await sleep(6000);
await ev(`[...document.querySelectorAll('.kmb-ogret .kmb-bag')].find(b => b.textContent.includes('Tüm ders'))?.click()`); await sleep(2500);
const dv = () => ev(`(() => { const d = document.querySelector('.kmb-dv'); const l = d?.querySelector('.kmb-lv'); return d ? { uyku: d.classList.contains('uyku'), gizli: l.classList.contains('gizli'), calan: l.classList.contains('calan'), sure: l.querySelector('.kmb-lv-sure')?.textContent } : null })()`);
const tk = await ev(`(() => { const r = document.querySelector('.kmb-dv .kmb-lv-sahne').getBoundingClientRect(); return { x: r.left, y: r.top, w: r.width, h: r.height } })()`);
const td = async (fx, fy) => { const x = tk.x + tk.w * fx, y = tk.y + tk.h * fy; await send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x, y }] }); await sleep(40); await send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }); };
let q = await dv(); kontrol('tam ekran ders videosu açıldı ve oynuyor', q && q.calan, JSON.stringify(q));
await send('Page.captureScreenshot', { format: 'jpeg', quality: 70 }).then((r) => fs.writeFileSync((process.env.OUT || '/tmp') + '/tam_acik.jpg', Buffer.from(r.data, 'base64')));
await sleep(3500); q = await dv(); kontrol('tam ekran: 3 sn sonra şerit ve denetimler birlikte gizlenir', q.uyku && q.gizli && q.calan, JSON.stringify(q));
await send('Page.captureScreenshot', { format: 'jpeg', quality: 70 }).then((r) => fs.writeFileSync((process.env.OUT || '/tmp') + '/tam_gizli.jpg', Buffer.from(r.data, 'base64')));
await td(0.5, 0.2); await sleep(450); q = await dv(); kontrol('tam ekran tek dokunuş: şerit+denetim açılır, oynama sürer, sarmaz', !q.uyku && !q.gizli && q.calan, JSON.stringify(q));
await td(0.9, 0.5); await sleep(450); q = await dv(); kontrol('tam ekran kenar tek dokunuş: gizler, sarmaz', q.uyku && q.gizli && q.calan, JSON.stringify(q));
const t1 = sn(q.sure); await td(0.9, 0.5); await sleep(120); await td(0.9, 0.5); await sleep(400); q = await dv();
kontrol('tam ekran kenar çift dokunuş: +10 sn', sn(q.sure) >= t1 + 9, t1 + ' → ' + q.sure);
await ev(`document.querySelector('.kmb-dv-dugmeler button[aria-label="Kapat"]')?.click()`); await sleep(500);

// ———— dokunmatik telefon
await send('Emulation.setDeviceMetricsOverride', { width: 375, height: 812, deviceScaleFactor: 2, mobile: true });
await send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
await send('Page.navigate', { url: BASE + '/dersler/kmb/uretral-kateter' }); await sleep(6000);
await ev(`document.querySelector('.kmb-ogret .kmb-lv')?.scrollIntoView({block:'center'})`); await sleep(500);
let k = await kutu();
const dokun = async (fx, fy = 0.4) => { const x = k.x + k.w * fx, y = k.y + k.h * fy; await send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x, y }] }); await sleep(40); await send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }); };
const sifirla = async () => { await ev(`(() => { const l = document.querySelector('.kmb-ogret .kmb-lv'); l.querySelector('.kmb-lv-dugmeler button[aria-label="Duraklat"]')?.click(); const i = l.querySelector('.kmb-lv-zaman input'); Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(i, '5'); i.dispatchEvent(new Event('input',{bubbles:true})); })()`); await sleep(400); };
let d = await durum();
kontrol('başlangıç: denetimler açık, oynamıyor', d && !d.gizli && !d.calan, JSON.stringify(d));
await dokun(0.5, 0.12); await sleep(450); d = await durum();
kontrol('tek dokunuş (orta) yalnız denetimleri gizler, oynatmaz', d.gizli && !d.calan, JSON.stringify(d));
await dokun(0.92); await sleep(450); d = await durum();
kontrol('tek dokunuş (sağ kenar) denetimleri geri açar, sarmaz', !d.gizli && !d.calan && d.sure.startsWith('0:00'), JSON.stringify(d));
await dokun(0.08); await sleep(450); d = await durum();
kontrol('tek dokunuş (sol kenar) yalnız gizler, sarmaz', d.gizli && d.sure.startsWith('0:00'), d.sure);
await sifirla();
await dokun(0.92); await sleep(120); await dokun(0.92); await sleep(450); d = await durum();
kontrol('çift dokunuş sağ: +10 sn (5→15)', sn(d.sure) === 15, d.sure);
await sifirla();
await dokun(0.92); await sleep(120); await dokun(0.92); await sleep(150); await dokun(0.92); await sleep(450); d = await durum();
kontrol('üçlü dokunuş sağ: +20 sn (5→25, seri)', sn(d.sure) === 25, d.sure);
await dokun(0.08); await sleep(120); await dokun(0.08); await sleep(450); d = await durum();
kontrol('çift dokunuş sol: −10 sn (25→15)', sn(d.sure) === 15, d.sure);
await dokun(0.5, 0.12); await sleep(120); await dokun(0.5, 0.12); await sleep(700); d = await durum();
kontrol('çift dokunuş orta: oynat', d.calan, JSON.stringify(d));
await sleep(3600); d = await durum();
kontrol('oynarken 3 sn sonra denetimler gizlenir', d.gizli && d.calan, JSON.stringify(d));
await dokun(0.5, 0.12); await sleep(450); d = await durum();
kontrol('oynarken tek dokunuş: denetimler açılır, oynama sürer', !d.gizli && d.calan, JSON.stringify(d));
// basılı tut → 2×
{ const x = k.x + k.w * 0.5, y = k.y + k.h * 0.12; await send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x, y }] }); await sleep(700); d = await durum(); kontrol('basılı tutma: 2× rozeti', d.rozet, JSON.stringify(d)); await send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }); await sleep(300); d = await durum(); kontrol('bırakınca 2× biter, oynamaya devam', !d.rozet && d.calan, JSON.stringify(d)); }
// yatay kaydırma → sar
{ const once = sn((await durum()).sure); const x = k.x + k.w * 0.6, y = k.y + k.h * 0.12;
  await send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x, y }] });
  for (let i = 1; i <= 8; i++) { await send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: x - i * 15, y }] }); await sleep(30); }
  d = await durum(); kontrol('yana kaydırırken hedef balonu', d.kayma, JSON.stringify(d));
  await send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }); await sleep(300); d = await durum();
  kontrol('sola kaydırma geri sarar', sn(d.sure) < once, `${once} → ${d.sure}`); }
// cümle menüsü
await ev(`document.querySelector('.kmb-ogret .kmb-lv-dugmeler [aria-label="Cümle listesi"]').click()`); await sleep(300); d = await durum();
kontrol('cümle menüsü açılır', d.menu, '');
await ev(`document.querySelectorAll('.kmb-ogret .kmb-lv-menu li button')[2].click()`); await sleep(1200); d = await durum();
kontrol('menüden 3. cümleye atlar', !d.menu && (await ev(`document.querySelector('.kmb-ogret .kmb-lv-baslik')?.textContent`))?.includes('Cümle 3'), d.sure);
await ev(`document.querySelector('.kmb-ogret .kmb-lv-dugmeler button[aria-label="Duraklat"]')?.click()`);

// adım sonu hızlı kontrol: soru çıkar, yanıtlanana dek sıradakine geçilmez
await ev(`document.querySelectorAll('.kmb-serit button')[9].click()`); await sleep(2500);
await ev(`(() => { const i = document.querySelector('.kmb-ogret .kmb-lv-zaman input'); Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(i, String(Number(i.max) - 0.8)); i.dispatchEvent(new Event('input',{bubbles:true})); document.querySelector('.kmb-ogret .kmb-lv-dugmeler button[aria-label="Oynat"]').click(); })()`);
await sleep(4500);
let hk = await ev(`({ soru: document.querySelector('.kmb-hizli h3')?.textContent, bekle: document.querySelector('.kmb-lv-son-bas')?.textContent, adim: document.querySelector('.kmb-ogret-baslik small')?.textContent })`);
kontrol('adım sonu sorusu çıkar ve geçiş bekler', hk.soru && /soruyu yanıtla/.test(hk.bekle || '') && /Adım 10/.test(hk.adim), JSON.stringify(hk));
await send('Page.captureScreenshot', { format: 'jpeg', quality: 70 }).then((r) => fs.writeFileSync((process.env.OUT || '/tmp') + '/hizli.jpg', Buffer.from(r.data, 'base64')));
await ev(`document.querySelector('.kmb-hizli .kmb-secenekler button').click()`); await sleep(300);
await ev(`[...document.querySelectorAll('.kmb-hizli button')].find(b => /Devam/.test(b.textContent))?.click()`); await sleep(3000);
hk = await ev(`({ son: document.querySelector('.kmb-ogret .kmb-lv-son')?.innerText, hizli: !!document.querySelector('.kmb-hizli'), oto: document.querySelector('.kmb-ogret-arac input')?.checked, adim: document.querySelector('.kmb-ogret-baslik small')?.textContent, kayit: Object.keys(JSON.parse(localStorage.getItem('medsoru_kmb_hata_02') || '{"s":{}}').s) })`);
kontrol('yanıtlayınca istatistiğe yazılır ve sıradaki adıma geçilir', /Adım 11/.test(hk.adim) && hk.kayit.includes('video'), JSON.stringify(hk));

// ———— fare (PC)
await send('Emulation.setTouchEmulationEnabled', { enabled: false });
await send('Emulation.setDeviceMetricsOverride', { width: 1366, height: 860, deviceScaleFactor: 1, mobile: false });
await send('Page.navigate', { url: BASE + '/dersler/kmb/uretral-kateter' }); await sleep(6000);
k = await kutu();
const tik = async (fx, n = 1) => { const x = k.x + k.w * fx, y = k.y + k.h * 0.12; await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y }); for (let i = 1; i <= n; i++) { await send('Input.dispatchMouseEvent', { type: 'mousePressed', x, y, button: 'left', clickCount: i }); await send('Input.dispatchMouseEvent', { type: 'mouseReleased', x, y, button: 'left', clickCount: i }); await sleep(60); } };
await tik(0.5); await sleep(400); d = await durum();
kontrol('fare tık: oynat', d.calan, JSON.stringify(d));
await tik(0.5); await sleep(400); d = await durum();
kontrol('fare tık: duraklat', !d.calan, JSON.stringify(d));
await tik(0.5, 2); await sleep(600); d = await durum();
kontrol('fare çift tık: tam ekran, oynatma durumu değişmez', !d.calan && d.tam, JSON.stringify(d));
console.log('HATALAR', JSON.stringify(errs));
const kalan = sonuc.filter((x) => !x.ok).length; console.log(`${sonuc.length - kalan}/${sonuc.length} geçti`);
process.exit(0);
