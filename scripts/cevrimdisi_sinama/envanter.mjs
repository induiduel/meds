// Aşama A: çevrimiçi envanter. Her rota açılır, sayfanın istediği aynı-köken adresler kaydedilir; çevrimdışı kataloğun
// (tüm paketlerin dosya listesi) kapsamadığı adresler rota başına raporlanır. Kullanım: node envanter.mjs [OUT=envanter.json]
import fs from 'node:fs';
import { tarayici, sleep, SEED } from './cdp.mjs';
const BASE = process.env.BASE || 'http://localhost:3100';
const OUT = process.env.OUT || new URL('./envanter.json', import.meta.url).pathname;
const kat = await (await fetch('http://localhost:3000/api/cevrimdisi/katalog')).json();
const kapsam = new Map();
async function kapsamKur() { kapsam.clear(); const kat = await (await fetch('http://localhost:3000/api/cevrimdisi/katalog')).json();
for (const p of kat.paketler) {
  const x = await (await fetch(`http://localhost:3000/api/cevrimdisi/paket/${encodeURIComponent(p.id)}`)).json();
  for (const d of x.dosyalar || []) kapsam.set(d.u.split('?')[0], p.id), kapsam.set(d.u, p.id);
} }
const ilkDeste = kat.paketler.find((p) => p.modul === 'ogren').id.slice(6);
const cd = await (await fetch('http://localhost:3000/api/canli-ders')).json().catch(() => null);
const cdKey = (cd?.dersler || cd || [])[0]?.key;
const ROTALAR = (process.env.ROTALAR || ['/', '/bugun', '/ogren', `/ogren/${ilkDeste}`, '/sorular', '/cikmis', '/calis', '/test', '/sinav-calisma', '/kartlar',
  '/sozluk', '/hastaliklar', '/notlar', '/ozetler', '/spotlar', '/en-onemliler', '/soru-cozucu', '/alternatif-cozucu', '/kazanimlar', '/ornek-sorular',
  '/saglik', '/canliders', cdKey && `/canliders/${cdKey}`, '/kamp', '/patoloji-check-up', '/genetik-check-up', '/olasi-sorular', '/gecmis-kurullar',
  '/istatistik', '/bitirdiklerim', '/ayarlar', '/siralama', '/harita', '/muzik', '/ses-kayitlari', '/kitapcik', '/guncellemeler', '/asistan', '/ara/apoptoz',
  '/cevrimdisi'].filter(Boolean).join(',')).split(',');
const t = await tarayici({ temiz: true });
let istekler = [];
t.on((m, p) => { if (m === 'Network.requestWillBeSent') istekler.push({ u: p.request.url, tur: p.type, y: p.request.method }); });
await t.send('Page.navigate', { url: BASE + '/favicon.ico' }); await sleep(700); await t.ev(SEED);
const rapor = {}; const ham = {};
for (const r of ROTALAR) {
  istekler = [];
  await t.send('Page.navigate', { url: BASE + r });
  await sleep(Number(process.env.BEKLE || 6000));
  // Sayfayı sonuna dek kaydır (tembel yüklenen parçalar da istensin)
  await t.ev(`(async()=>{for(let i=0;i<6;i++){scrollBy(0,innerHeight);document.querySelectorAll('main,[class*=scroll]').forEach(e=>e.scrollBy?.(0,2000));await new Promise(r=>setTimeout(r,400))}})()`).catch(() => {});
  await sleep(1500);
  const ayni = [...new Map(istekler.filter((x) => x.u.startsWith(BASE) && x.y === 'GET').map((x) => [x.u.slice(BASE.length), x])).values()];
  ham[r] = ayni.map((x) => ({ ...x, u: x.u.slice(BASE.length) }));
  const eksik = ayni.map((x) => ({ ...x, u: x.u.slice(BASE.length) })).filter((x) => !kapsam.has(x.u) && !kapsam.has(x.u.split('?')[0]) && x.tur !== 'Document');
  rapor[r] = { n: ayni.length, eksik: eksik.map((x) => `${x.tur} ${x.u}`) };
  console.log(r, ayni.length, 'eksik:', eksik.length);
}
await kapsamKur(); for (const r of Object.keys(ham)) rapor[r].eksik = ham[r].filter((x) => !kapsam.has(x.u) && !kapsam.has(x.u.split('?')[0]) && x.tur !== 'Document').map((x) => `${x.tur} ${x.u}`);
fs.writeFileSync(OUT.replace('.json', '_ham.json'), JSON.stringify(ham));
fs.writeFileSync(OUT, JSON.stringify(rapor, null, 1));
t.kapat(); process.exit(0);
