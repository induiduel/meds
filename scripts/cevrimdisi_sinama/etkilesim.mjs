// Aşama D: internetsiz etkileşim sınaması (sinama.mjs'nin indirdiği profil üzerinde). Her senaryo bir adresi açar, ekranda
// bir eylem yapar (oynat, şık seç, PDF aç) ve sonucu ölçer: ses gerçekten çalıyor mu (currentTime ilerliyor, hata yok),
// PDF sayfası çiziliyor mu, cevap geri bildirimi geliyor mu. Kullanım: node etkilesim.mjs  (SADECE=ad,ad)
import fs from 'node:fs';
import { tarayici, sleep, ag } from './cdp.mjs';
const BASE = 'http://localhost:3100';
const OUT = process.env.OUT || '/tmp/claude-1000/cevrimdisi-sinama';
const PROFIL = process.env.PROFIL || '/tmp/claude-1000/cevrimdisi-profil';
const paketler = JSON.parse(fs.readFileSync(`${OUT}/paketler.json`, 'utf8'));
const pk = (onek) => paketler.find((x) => x.startsWith(onek))?.split(':');
const [, cBrans, cKod] = pk('cozucu:') || [];
const [, oBrans, oKod] = pk('onem:') || [];
const [, aKod] = pk('alt:') || [];
const deste = pk('ogren:')?.[1];
const sesli = pk('sesli:')?.slice(1).join(':');
const t = await tarayici({ profil: PROFIL });
await t.send('Fetch.enable', { patterns: [{ urlPattern: '*/api/ai-test/durum*' }] });
t.on((m, p) => { if (m === 'Fetch.requestPaused') t.send('Fetch.fulfillRequest', { requestId: p.requestId, responseCode: 200, responseHeaders: [{ name: 'Content-Type', value: 'application/json' }], body: Buffer.from('{"ok":true}').toString('base64') }).catch(() => {}); });
// Ortam: oluşturulan her medya öğesi kaydedilir; başarım penceresi gizlenir
await t.send('Page.addScriptToEvaluateOnNewDocument', { source: `(()=>{window.__medya=[];const op=HTMLMediaElement.prototype.play;HTMLMediaElement.prototype.play=function(){if(!window.__medya.includes(this))window.__medya.push(this);return op.call(this)};const OA=window.Audio;window.Audio=function(s){const a=new OA(s);window.__medya.push(a);return a};window.Audio.prototype=OA.prototype;document.addEventListener('DOMContentLoaded',()=>{const s=document.createElement('style');s.textContent='.bs-giris{display:none!important}';document.head.appendChild(s)})})()` });
const hatalar = [];
t.on((m, p) => {
  if (m === 'Runtime.exceptionThrown') hatalar.push('İSTİSNA ' + (p.exceptionDetails?.exception?.description || '').slice(0, 200));
  if (m === 'Runtime.consoleAPICalled' && p.type === 'error') hatalar.push('KONSOL ' + p.args.map((a) => a.value ?? a.description ?? '').join(' ').slice(0, 200));
});
// Önce (çevrimiçi) güncellemeler iner: yeni derleme sonrası uygulama paketi ve değişen paketler
if (process.env.GUNCELLE !== '0') {
  await ag(false);
  await t.send('Page.navigate', { url: BASE + '/' }); await sleep(6000);
  const M = 'window.__medsorCevrimdisi';
  for (let i = 0; i < 40 && !(await t.ev(`!!${M}`)); i++) await sleep(500);
  await t.ev(`${M}.katalogYenile(true)`);
  const g = await t.ev(`(()=>{const s=${M}.durumAl();const ids=Object.keys(s.kayitlar).filter(id=>${M}.paketDurumu(id)==='guncelleme');${M}.kuyrugaEkle(ids,true);return ids})()`);
  console.log('Güncellenen:', g.join(' ') || '—');
  for (let i = 0; i < 300; i++) { await sleep(2000); if (await t.ev(`(()=>{const s=${M}.durumAl();return !s.kuyruk.length&&!s.aktif})()`)) break; }
  await t.send('Page.reload'); await sleep(5000);
}
await ag(true);
const tikla = (re) => `(()=>{const re=${re};const b=[...document.querySelectorAll('button,[role=button],a')].filter(e=>e.offsetParent!==null).find(e=>re.test((e.getAttribute('aria-label')||'')+' '+(e.title||'')+' '+e.textContent));if(b){b.click();return (b.getAttribute('aria-label')||b.textContent||'').trim().slice(0,60)}return null})()`;
const medya = `(()=>{const m=(window.__medya||[]).concat([...document.querySelectorAll('audio,video')]);return m.map(a=>({src:(a.currentSrc||a.src||'').replace(location.origin,'').slice(0,90),t:+a.currentTime.toFixed(2),p:a.paused,hata:a.error&&a.error.code,rs:a.readyState}))})()`;
const SENARYO = {
  'yazi-tipi': { u: '/bugun', adim: async () => t.ev(`(async()=>{const c=await caches.open('medsor-paket-v1');const ks=(await c.keys()).map(r=>r.url);
    const css=ks.find(u=>u.startsWith('https://fonts.googleapis.com/'));const woff=ks.filter(u=>u.startsWith('https://fonts.gstatic.com/')).length;
    await document.fonts.ready;return {css:!!css,woff,geist:document.fonts.check('16px Geist'),literata:document.fonts.check('16px Literata')}})()`),
    ok: (r) => r.css && r.woff >= 4 && r.geist },
  'motivasyon-klip': { u: '/bugun', adim: async () => t.ev(`(async()=>{const a=new Audio('/ses/motivasyon/basla-ilk-01.mp3');a.muted=true;try{await a.play()}catch(e){return {hata:String(e)}}await new Promise(r=>setTimeout(r,1500));return {t:a.currentTime,hata:a.error&&a.error.code}})()`),
    ok: (r) => r.t > 0.3 && !r.hata },
  'ogren-ders': { u: `/ogren/${deste}`, adim: async () => {
    const once = await t.ev(`document.body.innerText.length`);
    const ileri = await t.ev(tikla(`/sonraki|ileri|devam/i`)); await sleep(1500);
    return { once, ileri, sonra: await t.ev(`document.body.innerText.length`) };
  }, ok: (r) => r.once > 1500 },
  'ogren-ses': { u: `/ogren/${deste}`, adim: async () => { const b = await t.ev(tikla(`/dinle|sesli|oynat|seslendir/i`)); await sleep(4000); return { b, m: await t.ev(medya) }; },
    ok: (r) => r.m.some((x) => x.t > 0.5 && !x.hata) },
  'ogren-pdf': { u: `/ogren/${deste}?pdf=1`, bekle: 9000, adim: async () => ({ tuval: await t.ev(`[...document.querySelectorAll('canvas')].filter(c=>c.width>100).length`), yazi: await t.ev(`(document.body.innerText.match(/PDF[^\\n]{0,80}/)||[''])[0]`) }), ok: (r) => r.tuval > 0 },
  'cozucu-ses': { u: `/soru-cozucu?brans=${cBrans}&ders=${cKod}&coz=1`, bekle: 8000, adim: async () => { const b = await t.ev(tikla(`/başlat|oynat|dinle|çöz/i`)); await sleep(5000); return { b, m: await t.ev(medya) }; },
    ok: (r) => r.m.some((x) => x.t > 0.5 && !x.hata) },
  'asistan-ses': { u: `/en-onemliler?brans=${oBrans}&ders=${oKod}&asistan=1`, bekle: 8000, adim: async () => { const b = await t.ev(tikla(`/başlat|oynat|dinle/i`)); await sleep(5000); return { b, m: await t.ev(medya) }; },
    ok: (r) => r.m.some((x) => x.t > 0.5 && !x.hata) },
  'onem-liste': { u: `/en-onemliler?brans=${oBrans}&ders=${oKod}`, adim: async () => ({ n: await t.ev(`document.body.innerText.length`) }), ok: (r) => r.n > 2500 },
  'alt-ses': { u: `/alternatif-cozucu?ders=${aKod}&coz=1`, bekle: 8000, adim: async () => { const b = await t.ev(tikla(`/başlat|oynat|dinle/i`)); await sleep(5000); return { b, m: await t.ev(medya) }; },
    ok: (r) => r.m.some((x) => x.t > 0.5 && !x.hata) },
  'sesli-ders': { u: `/canliders/${sesli}`, bekle: 8000, adim: async () => { const b = await t.ev(`(()=>{const e=[...document.querySelectorAll('[aria-label="Oynat"]')].find(x=>x.offsetParent);if(e){e.click();return 'Oynat'}return null})()`); await sleep(5000); return { b, m: await t.ev(medya) }; },
    ok: (r) => r.m.some((x) => x.t > 0.5 && !x.hata) },
  'cikmis-cevap': { u: `/cikmis`, adim: async () => {
    const r = await t.ev(`(()=>{const s=[...document.querySelectorAll('button')].find(b=>/^\\s*A\\b/.test(b.textContent)&&b.offsetParent);if(!s)return null;const once=document.body.innerText.length;s.click();return once})()`);
    await sleep(1500); return { once: r, sonra: await t.ev(`document.body.innerText.length`), dogru: await t.ev(`/Doğru|Yanlış|doğru cevap/i.test(document.body.innerText)`) };
  }, ok: (r) => r.once && r.dogru },
  'arama': { u: `/ara/apoptoz`, adim: async () => ({ metin: await t.ev(`document.body.innerText.replace(/\\s+/g,' ').slice(0,300)`), n: await t.ev(`document.body.innerText.length`) }), ok: (r) => r.n > 1500 },
  'test-olustur': { u: `/test`, adim: async () => {
    const b = await t.ev(tikla(`/testi oluştur/i`));
    let soru = false, durum = '';
    for (let i = 0; i < 30 && !soru; i++) { await sleep(1000); durum = await t.ev(`(document.querySelector('.tb b')||{}).textContent||''`); soru = await t.ev(`/Soru\\s*1\\b|1\\s*\\/\\s*\\d+/.test(document.body.innerText) && !document.querySelector('.tb')`); }
    return { b, soru, durum };
  }, ok: (r) => r.soru },
};
const sadece = process.env.SADECE?.split(',');
const rapor = [];
for (const [ad, s] of Object.entries(SENARYO)) {
  if (sadece && !sadece.includes(ad)) continue;
  hatalar.length = 0;
  await t.send('Page.navigate', { url: BASE + s.u });
  await sleep(s.bekle || 6000);
  let r; try { r = await s.adim(); } catch (e) { r = { istisna: String(e).slice(0, 200) }; }
  const ok = (() => { try { return !!s.ok(r); } catch { return false; } })();
  const sh = await t.send('Page.captureScreenshot', { format: 'jpeg', quality: 55 });
  fs.writeFileSync(`${OUT}/etk_${ad}.jpg`, Buffer.from(sh.data, 'base64'));
  rapor.push({ ad, ok, r, hatalar: [...new Set(hatalar)].slice(0, 8) });
  console.log(ok ? '✓' : '✗', ad, JSON.stringify(r).slice(0, 400), hatalar.length ? `hata=${hatalar.length}` : '');
}
fs.writeFileSync(`${OUT}/etkilesim.json`, JSON.stringify(rapor, null, 1));
await ag(false); t.kapat(); process.exit(0);
