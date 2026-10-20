// Aşama C: gerçek internetsiz sınama. Temiz profil → vekil (:3100) üzerinden açılış → seçilen paketler uygulamanın kendi
// motoruyla (window.__medsorCevrimdisi) iner → vekil kapatılır (gerçek ağ hatası) → her rota açılır; konsol hatası,
// düşen istek, hata metni, boş ekran ve "cihazında yok" ekranı kaydedilir. Ekran görüntüleri OUT klasörüne.
// Kullanım: node sinama.mjs   (PAKETLER=id,id  ROTALAR=/a,/b  ATLA_INDIR=1 → profil korunur, indirme atlanır)
import fs from 'node:fs';
import { tarayici, sleep, SEED, ag } from './cdp.mjs';
const BASE = 'http://localhost:3100';
const OUT = process.env.OUT || '/tmp/claude-1000/cevrimdisi-sinama';
const PROFIL = process.env.PROFIL || '/tmp/claude-1000/cevrimdisi-profil';
fs.mkdirSync(OUT, { recursive: true });
const gizli = (fs.readFileSync(new URL('../../.env', import.meta.url), 'utf8').match(/^MEDS_PANEL_SECRET=(.*)$/m) || [])[1]?.trim().replace(/^"|"$/g, '');
await ag(false);
const t = await tarayici({ profil: PROFIL, temiz: !process.env.ATLA_INDIR });
// Giriş kapısı: yapay zekâ test erişimi çevrimiçiyken çerezle; internetsizken durum sorusu sınama aracınca yanıtlanır
await t.send('Fetch.enable', { patterns: [{ urlPattern: '*/api/ai-test/durum*' }] });
t.on((m, p) => { if (m === 'Fetch.requestPaused') t.send('Fetch.fulfillRequest', { requestId: p.requestId, responseCode: 200, responseHeaders: [{ name: 'Content-Type', value: 'application/json' }], body: Buffer.from('{"ok":true}').toString('base64') }).catch(() => {}); });
const hatalar = []; const dusen = [];
t.on((m, p) => {
  if (m === 'Runtime.exceptionThrown') hatalar.push('İSTİSNA ' + (p.exceptionDetails?.exception?.description || p.exceptionDetails?.text || '').slice(0, 300));
  if (m === 'Runtime.consoleAPICalled' && p.type === 'error') hatalar.push('KONSOL ' + p.args.map((a) => a.value ?? a.description ?? '').join(' ').slice(0, 300));
  if (m === 'Network.requestWillBeSent') istek.set(p.requestId, p.request.url);
  if (m === 'Network.loadingFailed' && !p.canceled) dusen.push(`${p.type} ${(istek.get(p.requestId) || '').replace(BASE, '')} ${p.errorText}`);
  if (m === 'Network.responseReceived' && p.response.status >= 400 && p.response.url.startsWith(BASE)) dusen.push(`${p.type} ${p.response.url.replace(BASE, '')} HTTP ${p.response.status}`);
});
const istek = new Map();
// Test hesabının başarım "dönemin?" penceresi her ekranı örtüyor: sınamada gizlenir (yalnız bu araçta)
await t.send('Page.addScriptToEvaluateOnNewDocument', { source: `document.addEventListener('DOMContentLoaded',()=>{const s=document.createElement('style');s.textContent='.bs-giris{display:none!important}';document.head.appendChild(s)})` });
if (process.env.IZLE) await t.send('Page.addScriptToEvaluateOnNewDocument', { source: `(()=>{const od=Cache.prototype.delete;Cache.prototype.delete=function(r,o){const u=typeof r==='string'?r:r&&r.url;if(String(u).includes('index.html'))console.error('SILME index', u, new Error().stack);return od.call(this,r,o)};const cd=CacheStorage.prototype.delete;CacheStorage.prototype.delete=function(n){console.error('SILME önbellek', n, new Error().stack);return cd.call(this,n)};const op=Cache.prototype.put;Cache.prototype.put=function(r,x){const u=typeof r==='string'?r:r&&r.url;if(String(u).includes('index.html'))console.error('YAZMA index', u, x&&x.status);return op.call(this,r,x)}})()` });
await t.send('Page.navigate', { url: BASE + '/favicon.ico' }); await sleep(800);
await t.ev(SEED);
if (gizli) await t.ev(`fetch('/api/ai-test/oturum',{method:'POST',headers:{'x-panel-secret':${JSON.stringify(gizli)}}}).then(r=>r.status)`);
await t.send('Page.navigate', { url: BASE + '/' }); await sleep(5000);
await t.ev(`navigator.serviceWorker.ready.then(()=>1)`);
await t.send('Page.reload'); await sleep(5000);
// Başarım "dönemin?" penceresi (test hesabında profil yok) sınamayı örtmesin
await t.ev(`(async()=>{for(let i=0;i<20;i++){const k=document.querySelector('.bs-giris');if(k){const b=[...k.querySelectorAll('button')].find(x=>/^\\s*3/.test(x.textContent));b&&b.click();await new Promise(r=>setTimeout(r,400));const kurul=[...k.querySelectorAll('button')].find(x=>/Kurul\\s*1|^\\s*1\\s*$/.test(x.textContent)&&!/Dönem/.test(x.textContent));kurul&&kurul.click();await new Promise(r=>setTimeout(r,300));k.querySelector('.bs-dk-kaydet')?.click();await new Promise(r=>setTimeout(r,1500));return 'profil'}await new Promise(r=>setTimeout(r,500))}return 'pencere yok'})()`).then((x) => console.log('Başarım:', x)).catch(() => {});
console.log('SW denetiminde:', await t.ev('!!navigator.serviceWorker.controller'));
const M = 'window.__medsorCevrimdisi';
for (let i = 0; i < 40 && !(await t.ev(`!!${M}`)); i++) await sleep(500);
await t.ev(`${M}.katalogYenile(true)`);
const kat = await t.ev(`${M}.durumAl().katalog.map(p=>({id:p.id,modul:p.modul,bayt:p.bayt}))`);
const ilk = (m) => kat.find((p) => p.modul === m)?.id;
const PAKETLER = (process.env.PAKETLER || [...kat.filter((p) => p.modul === 'veri').map((p) => p.id), 'db:sorular', 'ogren:deck-urinary-obstruction',
  ilk('cozucu'), ilk('onem'), ilk('alt'), ilk('sesli'), kat.find((p) => p.id === 'sayfa:tbg-kampi')?.id].filter(Boolean).join(',')).split(',');
fs.writeFileSync(`${OUT}/paketler.json`, JSON.stringify(PAKETLER));
if (!process.env.ATLA_INDIR) {
  console.log('İndiriliyor:', PAKETLER.join(' '));
  await t.ev(`${M}.cevrimdisiModuAc(${JSON.stringify(PAKETLER)}, {ses:true,pdf:true})`);
  const t0 = Date.now();
  for (;;) {
    await sleep(3000);
    const d = await t.ev(`(()=>{const s=${M}.durumAl();return {k:s.kuyruk.length,a:s.aktif&&s.aktif.id,d:${JSON.stringify(['uygulama', ...PAKETLER])}.map(id=>id+':'+${M}.paketDurumu(id))}})()`);
    if (!d.k && !d.a) { console.log(d.d.join(' ')); break; }
    if (Date.now() - t0 > 20 * 60_000) { console.log('ZAMAN AŞIMI', d); break; }
  }
}
const kayit = await t.ev(`Object.fromEntries(Object.entries(${M}.durumAl().kayitlar).map(([k,v])=>[k,v.yarim?'YARIM':'tamam']))`);
console.log('Cihazdaki paketler:', JSON.stringify(kayit));

await ag(true);
await sleep(500);
const deste = PAKETLER.find((x) => x.startsWith('ogren:'))?.slice(6);
const sesli = PAKETLER.find((x) => x.startsWith('sesli:'))?.slice(6);
const ROTALAR = (process.env.ROTALAR || ['/', '/bugun', '/ogren', deste && `/ogren/${deste}`, '/sorular', '/cikmis', '/calis', '/test', '/sinav-calisma', '/kartlar',
  '/sozluk', '/hastaliklar', '/notlar', '/ozetler', '/spotlar', '/en-onemliler', '/soru-cozucu', '/alternatif-cozucu', '/kazanimlar', '/ornek-sorular',
  '/saglik', '/canliders', sesli && `/canliders/${sesli}`, '/kamp', '/patoloji-check-up', '/genetik-check-up', '/olasi-sorular', '/gecmis-kurullar',
  '/istatistik', '/bitirdiklerim', '/ayarlar', '/harita', '/ara/apoptoz', '/cevrimdisi'].filter(Boolean).join(',')).split(',');
const HATA_RE = /(yüklenemedi|yuklenemedi|bir hata|hata oluştu|başarısız|Failed to fetch|bağlantı kurulamadı|cihazında yok|NetworkError|Something went wrong)/i;
const rapor = [];
for (const r of ROTALAR) {
  hatalar.length = 0; dusen.length = 0;
  await t.send('Page.navigate', { url: BASE + r });
  await sleep(Number(process.env.BEKLE || 7000));
  const g = await t.ev(`(()=>{const tx=document.body.innerText||'';return {uzun:tx.replace(/\\s+/g,' ').trim().length, yok:!!document.querySelector('.cv-yok'), cevrimdisiHtml:document.title.includes('Çevrimdışı Mod'), metin:tx.replace(/\\s+/g,' ').slice(0,4000)}})()`).then(async (g) => ({ ...g, kabukVar: await t.ev(`caches.open('medsor-paket-v1').then(c=>c.match(location.origin+'/index.html')).then(x=>!!x)`), motor: await t.ev(`(()=>{const s=window.__medsorCevrimdisi&&window.__medsorCevrimdisi.durumAl();return s?JSON.stringify({a:s.aktif,k:s.kuyruk,h:s.hatalar,u:window.__medsorCevrimdisi.paketDurumu('uygulama')}):'yok'})()`).catch(()=>'?') })).catch((e) => ({ hata: String(e) }));
  const sh = await t.send('Page.captureScreenshot', { format: 'jpeg', quality: 55 });
  fs.writeFileSync(`${OUT}/${r.replace(/[^a-z0-9]+/gi, '_') || 'kok'}.jpg`, Buffer.from(sh.data, 'base64'));
  const hataMetni = (g.metin || '').match(new RegExp(`.{0,60}${HATA_RE.source}.{0,60}`, 'i'))?.[0];
  const sonuc = { r, uzun: g.uzun, yok: g.yok, kabuk: g.cevrimdisiHtml, hataMetni, hatalar: [...new Set(hatalar)].slice(0, 12), dusen: [...new Set(dusen)].slice(0, 25) };
  rapor.push(sonuc);
  const kotu = g.yok || g.cevrimdisiHtml || hataMetni || (g.uzun || 0) < 200 || hatalar.length;
  if (process.env.MOTOR) console.log('   motor', g.motor);
  console.log(kotu ? '✗' : '✓', r, g.kabukVar ? '' : 'KABUK-YOK', `metin=${g.uzun}`, g.yok ? 'CİHAZDA-YOK' : '', hataMetni ? `«${hataMetni}»` : '', `hata=${hatalar.length} düşen=${dusen.length}`);
}
fs.writeFileSync(`${OUT}/rapor.json`, JSON.stringify(rapor, null, 1));
await ag(false);
t.kapat(); process.exit(0);
