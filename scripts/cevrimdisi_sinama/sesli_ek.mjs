// Aşama E: sesli dersin EK katmanları internetsiz çalışıyor mu (2026-11-09, canliDersCevrimdisiEk.ts + sw.js).
// Çevrimiçi: ders uygulamanın kendi indiricisiyle (CevrimdisiDugme → cdCevrimdisiIndir) iner → vekil kapanır → ders sayfası
// açılır; cihazdaki kopyadan ayrıntı, ses (Range/206), ara soru klibi, ders analizi klibi, çıkmış sorunun tam verisi, terim
// sesi, Lottie dosyası doğrulanır. Kullanım: DERS=<key> node sesli_ek.mjs  (ATLA_INDIR=1 profil korunur)
import fs from 'node:fs';
import { tarayici, sleep, SEED, ag } from './cdp.mjs';
const BASE = 'http://localhost:3100';
const DERS = process.env.DERS;
if (!DERS) { console.error('DERS=<sesli ders anahtarı> gerekli'); process.exit(2); }
const PROFIL = process.env.PROFIL || `${process.env.HOME}/.cache/medsor-cevrimdisi/profil-sesli-ek`;
const gizli = (fs.readFileSync(new URL('../../.env', import.meta.url), 'utf8').match(/^MEDS_PANEL_SECRET=(.*)$/m) || [])[1]?.trim().replace(/^"|"$/g, '');
await ag(false);
const t = await tarayici({ profil: PROFIL, temiz: !process.env.ATLA_INDIR });
await t.send('Fetch.enable', { patterns: [{ urlPattern: '*/api/ai-test/durum*' }] });
t.on((m, p) => { if (m === 'Fetch.requestPaused') t.send('Fetch.fulfillRequest', { requestId: p.requestId, responseCode: 200, responseHeaders: [{ name: 'Content-Type', value: 'application/json' }], body: Buffer.from('{"ok":true}').toString('base64') }).catch(() => {}); });
const hatalar = [];
t.on((m, p) => {
  if (m === 'Runtime.exceptionThrown') hatalar.push('İSTİSNA ' + (p.exceptionDetails?.exception?.description || p.exceptionDetails?.text || '').slice(0, 300));
  if (m === 'Runtime.consoleAPICalled' && p.type === 'error') hatalar.push('KONSOL ' + p.args.map((a) => a.value ?? a.description ?? '').join(' ').slice(0, 300));
});
await t.send('Page.addScriptToEvaluateOnNewDocument', { source: `document.addEventListener('DOMContentLoaded',()=>{const s=document.createElement('style');s.textContent='.bs-giris{display:none!important}';document.head.appendChild(s)})` });
await t.send('Page.navigate', { url: BASE + '/favicon.ico' }); await sleep(800);
await t.ev(SEED);
if (gizli) await t.ev(`fetch('/api/ai-test/oturum',{method:'POST',headers:{'x-panel-secret':${JSON.stringify(gizli)}}}).then(r=>r.status)`);
await t.send('Page.navigate', { url: BASE + '/' }); await sleep(5000);
await t.ev(`navigator.serviceWorker.ready.then(()=>1)`);
await t.send('Page.reload'); await sleep(4000);
console.log('SW denetiminde:', await t.ev('!!navigator.serviceWorker.controller'));

const M = 'window.__medsorCevrimdisi';
for (let i = 0; i < 40 && !(await t.ev(`!!${M}`)); i++) await sleep(500);
if (!process.env.ATLA_INDIR) {
  // Uygulama paketi + sesli ders (katalog motoru sesli paketini canliDersCevrimdisi.ts'e devreder)
  await t.ev(`${M}.katalogYenile(true)`);
  await t.ev(`${M}.cevrimdisiModuAc(${JSON.stringify([`sesli:${DERS}`])}, {ses:true,pdf:true})`);
  const t0 = Date.now();
  for (;;) {
    await sleep(3000);
    const d = await t.ev(`(()=>{const s=${M}.durumAl();return {k:s.kuyruk.length,a:s.aktif&&s.aktif.id,d:['uygulama','sesli:${DERS}'].map(id=>id+':'+${M}.paketDurumu(id)),h:s.hatalar}})()`);
    if (!d.k && !d.a) { console.log('İndirme:', d.d.join(' '), d.h && Object.keys(d.h).length ? JSON.stringify(d.h) : ''); break; }
    if (Date.now() - t0 > Number(process.env.SURE_DK || 15) * 60_000) { console.log('ZAMAN AŞIMI', d); break; }
  }
}
const kayit = await t.ev(`JSON.parse(localStorage.getItem('medsoru_canli_ders_cevrimdisi_v1')||'{}')[${JSON.stringify(DERS)}]`);
console.log('Kayıt:', kayit ? `${kayit.sesler?.length} ses, ${kayit.pdfler?.length} PDF, ${kayit.resimler?.length} resim, ${kayit.ekler?.length} ek (eksik ${kayit.ekEksik}), ${(kayit.bayt / 1e6).toFixed(1)} MB` : 'YOK');
const ekler = kayit?.ekler || [];
const sinif = (re) => ekler.filter((u) => re.test(u)).length;
console.log('  ek dağılımı: hocaara', sinif(/cozucu-ses\/k\dhocaara/), 'analiz', sinif(/dersanaliz/), 'çıkmış', sinif(/past-exams\/tek/), 'terim', sinif(/terim-ses/), 'lottie', sinif(/ara_resim.*json/), 'örnek', sinif(/content\/ornek/), 'günlük', sinif(/\/gunluk$/));

// ---- İNTERNETSİZ ----
await ag(true); await sleep(500);
hatalar.length = 0;
await t.send('Page.navigate', { url: BASE + `/canliders/${DERS}` }); await sleep(8000);
const sayfa = await t.ev(`(()=>{const tx=(document.body.innerText||'').replace(/\\s+/g,' ');return {uzun:tx.length,yok:!!document.querySelector('.cv-yok'),baslik:document.title,hata:(tx.match(/.{0,50}(yüklenemedi|alınamadı|bir hata|cihazında yok|Failed to fetch).{0,50}/i)||[])[0]}})()`);
console.log(sayfa.yok || sayfa.hata ? '✗' : '✓', 'ders sayfası', JSON.stringify(sayfa));
const oynat = await t.ev(`(()=>{const e=[...document.querySelectorAll('[aria-label="Oynat"]')].find(x=>x.offsetParent);if(e){e.click();return 'Oynat'}return null})()`);
await sleep(5000);
const medya = await t.ev(`(()=>[...document.querySelectorAll('audio,video')].map(a=>({src:(a.currentSrc||a.src||'').replace(location.origin,'').slice(0,80),t:+a.currentTime.toFixed(2),p:a.paused,hata:a.error&&a.error.code,rs:a.readyState})))()`);
const dersSesi = medya.find((m) => m.src.includes('/api/canli-ders/ses/'));
console.log(dersSesi && dersSesi.t > 1 && !dersSesi.hata ? '✓' : '✗', 'ders sesi', oynat, JSON.stringify(medya));

// Ek dosyaları doğrudan iste (SW yanıtı): durum, X-From-Cache, Range/206
const ornek = (re) => ekler.find((u) => re.test(u));
const sorgulu = async (u, range) => t.ev(`fetch(${JSON.stringify(u)}${range ? ",{headers:{Range:'bytes=0-99'}}" : ''}).then(async r=>({s:r.status,c:r.headers.get('X-From-Cache'),l:r.headers.get('Content-Length'),ct:r.headers.get('Content-Type')})).catch(e=>({hata:String(e)}))`);
const denemeler = [
  ['ayrıntı JSON', `/api/canli-ders/${encodeURIComponent(DERS)}`, false, (r) => r.s === 200],
  ['ara soru klibi (Range)', ornek(/cozucu-ses\/k\dhocaara/), true, (r) => r.s === 206],
  ['ders analizi klibi', ornek(/dersanaliz/), false, (r) => r.s === 200],
  ['çıkmış soru verisi', ornek(/past-exams\/tek/), false, (r) => r.s === 200 && r.c === '1'],
  ['terim sesi', ornek(/terim-ses/), false, (r) => r.s === 200],
  ['Lottie', ornek(/ara_resim.*json/), false, (r) => r.s === 200],
].filter(([, u]) => u);
let kotu = 0;
for (const [ad, u, range, ok] of denemeler) {
  // Ses klipleri önbellekte sorgusuz; sayfanın istediği gibi ?v=<sürüm> ile de sorulur
  const istek = /cozucu-ses|dersanaliz/.test(u) ? `${u}?v=${encodeURIComponent((await t.ev(`caches.open('medsoru-canli-ders-offline').then(c=>c.match(${JSON.stringify(u)})).then(r=>r&&r.headers.get('X-Cd-Surum'))`)) || '')}` : u;
  const r = await sorgulu(istek, range);
  const iyi = ok(r);
  if (!iyi) kotu++;
  console.log(iyi ? '✓' : '✗', ad, istek.replace(BASE, '').slice(0, 90), JSON.stringify(r));
}
// Ara soru sayfasını ünlemle aç ve ses çalsın
const unlem = await t.ev(`(()=>{const b=[...document.querySelectorAll('button')].find(x=>x.offsetParent&&/sorabileceği|ara soru|Hoca/i.test((x.getAttribute('aria-label')||'')+' '+(x.title||'')));if(b){b.click();return (b.getAttribute('aria-label')||b.title)}return null})()`);
await sleep(6000);
const medya2 = await t.ev(`(()=>(window.__medya||[]).concat([...document.querySelectorAll('audio')]).map(a=>({src:(a.currentSrc||a.src||'').replace(location.origin,'').slice(0,80),t:+a.currentTime.toFixed(2),hata:a.error&&a.error.code})))()`);
console.log(unlem ? 'ara soru düğmesi:' : 'ara soru düğmesi yok', unlem, JSON.stringify(medya2));
const sh = await t.send('Page.captureScreenshot', { format: 'jpeg', quality: 60 });
const OUT = process.env.OUT || `${process.env.HOME}/.cache/medsor-cevrimdisi/cikti`;
fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(`${OUT}/sesli_ek.jpg`, Buffer.from(sh.data, 'base64'));
console.log('Konsol hataları:', hatalar.length ? [...new Set(hatalar)].slice(0, 10).join('\n  ') : '—');
await ag(false);
t.kapat();
process.exit(kotu || sayfa.yok || !dersSesi ? 1 : 0);
