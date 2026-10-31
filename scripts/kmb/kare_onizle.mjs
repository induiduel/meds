// KMB Lottie kare önizleyici: her videonun her bölümünden (cümle) kare alır, oynatıcının HTML etiket katmanını
// (LottieVideo.tsx › Katman: kamera, kadraja sıkıştırma, çakışma itmesi, kmb.css kesme kuralı) taklit ederek çizer ve
// cümle metnini altına yazan temas sayfası (contact sheet) üretir. Başsız Chrome (raw CDP) + node_modules/lottie-web canvas.
// Kullanım: node meds/scripts/kmb/kare_onizle.mjs [ad…]     (ad yoksa adimlar.json'daki tüm adım videoları; "konu" = index.json)
//   OUT=klasör (varsayılan $TMPDIR/kmb-kare)  KARE=.12,.5,.92 (bölüm içi kesirler)  GEN=360 (kare genişliği, px)
// Çıktı: OUT/<ad>.jpg + OUT/rapor.json (otomatik bulgular: kesik etiket, altyazı bölgesine taşan / kadraja sıkışan /
//   üst üste binen etiket, boş kare). Bulgular ipucudur; asıl denetim kareye bakıp cümleyle karşılaştırmaktır.
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const MEDS = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const LOT = path.join(MEDS, 'src/data/kmb/lottie');
const OUT = process.env.OUT || `${process.env.TMPDIR || '/tmp'}/kmb-kare`;
const KARE = (process.env.KARE || '.12,.5,.92').split(',').map(Number);
const GEN = +(process.env.GEN || 400);  // 400 px ≈ telefon: etiket yazısı 10 px tabana oturur (en sıkışık durum)
fs.mkdirSync(OUT, { recursive: true });
const adim = JSON.parse(fs.readFileSync(path.join(LOT, 'adimlar.json'), 'utf8'));
const konu = JSON.parse(fs.readFileSync(path.join(LOT, 'index.json'), 'utf8'));
let istek = process.argv.slice(2);
if (istek.includes('konu')) istek = [...istek.filter((x) => x !== 'konu'), ...konu.map((v) => v.ad)];
const tum = [...adim, ...konu];
const secili = istek.length ? tum.filter((v) => istek.includes(v.ad) || istek.includes(v.adim)) : adim;

const PORT = 9800 + Math.floor(Math.random() * 150);
const dir = path.join(OUT, `.chrome-${PORT}`);
const chrome = spawn('/opt/google/chrome/chrome', ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${dir}`, '--no-first-run',
  '--disable-extensions', '--mute-audio', '--hide-scrollbars', '--allow-file-access-from-files'], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
process.on('exit', () => { try { chrome.kill('SIGKILL'); } catch {} try { fs.rmSync(dir, { recursive: true, force: true }); } catch {} });
for (let i = 0; i < 60; i++) { try { await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json(); break; } catch { await sleep(200); } }
const tgt = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: 'PUT' })).json();
const ws = new WebSocket(tgt.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener('open', r));
let id = 0; const pend = new Map();
ws.addEventListener('message', (m) => {
  const d = JSON.parse(m.data);
  if (d.id && pend.has(d.id)) { const p = pend.get(d.id); pend.delete(d.id); d.error ? p.rej(new Error(JSON.stringify(d.error))) : p.res(d.result); }
  else if (d.method === 'Runtime.exceptionThrown') console.error('sayfa hatası:', d.params.exceptionDetails?.exception?.description?.slice(0, 300));
});
const send = (method, params = {}) => new Promise((res, rej) => { const i = ++id; pend.set(i, { res, rej }); ws.send(JSON.stringify({ id: i, method, params })); });
const ev = async (expr) => { const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true }); if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description); return r.result?.value; };
await send('Page.enable'); await send('Runtime.enable');

// sayfa: lottie-web canvas + oynatıcı Katman() mantığının birebir kopyası
const sayfa = path.join(OUT, '.onizle.html');
fs.writeFileSync(sayfa, `<!doctype html><meta charset="utf-8"><style>
body{margin:0;background:#1b2330;font:13px system-ui,sans-serif;color:#eef2f7;width:${GEN * KARE.length + 80}px}
h1{font-size:16px;margin:10px 14px}.sat{display:flex;gap:8px;padding:6px 14px 10px;border-top:1px solid #33405a}
.hc{width:${GEN}px}.sahne{position:relative;width:${GEN}px;aspect-ratio:8/5;background:#fff;overflow:hidden;container-type:inline-size}
.sahne img{position:absolute;inset:0;width:100%;height:100%}.alt{position:absolute;left:0;right:0;top:76%;bottom:0;background:rgba(255,0,80,.07);border-top:1px dashed rgba(220,0,60,.6)}
.kmb-lv-etiket{position:absolute;transform:translate(-50%,-50%);padding:.3em .75em;border-radius:999px;background:#1f2a3a;color:#fff;font-size:clamp(10px,2cqi,20px);font-weight:600;white-space:nowrap;max-width:46cqi;overflow:hidden;text-overflow:ellipsis;box-shadow:0 2px 6px rgba(0,0,0,.2)}
.kmb-lv-etiket.bilgi{background:#2f6fd6}.kmb-lv-etiket.uyari{background:#c0392b}.kmb-lv-etiket.dogru{background:#2e9e5b}
.kmb-lv-etiket.kesik,.kmb-lv-etiket.sikis{outline:3px solid #ff00d4}
.kmb-lv-sayac{position:absolute;transform:translate(-50%,-50%);padding:.25em .6em;border-radius:8px;background:rgba(15,20,27,.85);color:#ffd866;font:700 clamp(11px,2.6cqi,30px) monospace}
.kt{font:11px monospace;opacity:.7;margin-top:2px}.met{width:${GEN * KARE.length + 16}px;font-size:13px;line-height:1.35;padding:0 14px}
.met b{color:#ffd866}.bul{color:#ff7ab8;font:11px monospace}
</style><body><div id="kok"></div><script src="file://${path.join(MEDS, 'node_modules/lottie-web/build/player/lottie_canvas.min.js')}"></script><script>
function kameraAn(v,t){const k=v.kamera;if(!k||!k.length)return[400,250,100];if(t<=k[0][0])return[k[0][1],k[0][2],k[0][3]];
 for(let i=0;i<k.length-1;i++){const a=k[i],b=k[i+1];if(t<=b[0]){const f=b[0]===a[0]?1:(t-a[0])/(b[0]-a[0]);const e=f*f*(3-2*f);return[a[1]+(b[1]-a[1])*e,a[2]+(b[2]-a[2])*e,a[3]+(b[3]-a[3])*e];}}
 const s=k[k.length-1];return[s[1],s[2],s[3]];}
const sik=(n,a,b)=>Math.min(b,Math.max(a,n));
function katman(v,t,kap,bul){const[cx,cy,z]=kameraAn(v,t);const k=z/100;const dolu=[];
 const yer=(x,y,ad)=>{const ham=[(400+(x-cx)*k)/8,(250+(y-cy)*k)/5];const l=sik(ham[0],12,88);let tp=sik(ham[1],8,72);
  for(let n=0;n<6&&dolu.some(([a,b])=>Math.abs(a-l)<26&&Math.abs(b-tp)<8);n++)tp=tp+8>72?tp-8*(n+1):tp+8;
  dolu.push([l,tp]);const sk=Math.abs(ham[0]-l)>3||ham[1]>72+3||ham[1]<8-3;if(sk)bul.push('kadraja sıkıştı: "'+ad+'" ham ('+ham[0].toFixed(0)+'%,'+ham[1].toFixed(0)+'%)');
  return[l,sik(tp,6,72),sk];};
 const els=[];
 for(const s of v.sayaclar.filter(s=>t>=s.bas)){const[l,tp]=yer(s.x,s.y,'sayaç');const f=Math.min(1,Math.max(0,(t-s.bas)/Math.max(.01,s.son-s.bas)));
  const e=document.createElement('span');e.className='kmb-lv-sayac';e.style.left=l+'%';e.style.top=tp+'%';e.textContent=(s.v1+(s.v2-s.v1)*f).toFixed(s.ondalik)+' '+s.birim;kap.appendChild(e);els.push(e);}
 for(const g of v.etiketler.filter(e=>t>=e.bas&&t<=e.son)){const[l,tp,sk]=yer(g.x,g.y,g.metin);const e=document.createElement('span');
  e.className='kmb-lv-etiket '+g.tur+(sk?' sikis':'');e.style.left=l+'%';e.style.top=tp+'%';e.textContent=g.metin;e.dataset.m=g.metin;kap.appendChild(e);els.push(e);}
 return els;}
function denetle(els,kap,bul){const K=kap.getBoundingClientRect();const r=els.map(e=>e.getBoundingClientRect());
 els.forEach((e,i)=>{if(e.scrollWidth>e.clientWidth+1){e.classList.add('kesik');bul.push('kesik etiket: "'+(e.dataset.m||e.textContent)+'"');}
  if(r[i].bottom>K.top+K.height*.76+1)bul.push('altyazı bölgesine taşıyor: "'+(e.dataset.m||e.textContent)+'"');
  if(r[i].left<K.left-1||r[i].right>K.right+1)bul.push('kadraj dışına taşıyor: "'+(e.dataset.m||e.textContent)+'"');
  for(let j=0;j<i;j++){const a=r[i],b=r[j];const ox=Math.min(a.right,b.right)-Math.max(a.left,b.left),oy=Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top);
   if(ox>4&&oy>4)bul.push('üst üste binen: "'+(e.dataset.m||e.textContent)+'" ↔ "'+(els[j].dataset.m||els[j].textContent)+'"');}});}
// oynatıcıda sahne zemini beyaz (kmb.css .kmb-lv-sahne); saydam alanlar beyaza basılır
function beyaz(cv){const c=document.createElement('canvas');c.width=cv.width;c.height=cv.height;const x=c.getContext('2d');x.fillStyle='#fff';x.fillRect(0,0,c.width,c.height);x.drawImage(cv,0,0);return c.toDataURL('image/jpeg',.85);}
function bosMu(cv){const c=document.createElement('canvas');c.width=40;c.height=25;const x=c.getContext('2d');x.drawImage(cv,0,0,40,25);
 const d=x.getImageData(0,0,40,25).data;let s=0,s2=0,n=d.length/4;for(let i=0;i<d.length;i+=4){const g=(d[i]+d[i+1]+d[i+2])/3;s+=g;s2+=g*g;}return Math.sqrt(s2/n-(s/n)**2)<6;}
async function isle(v,veri,KARE){const kok=document.getElementById('kok');kok.innerHTML='';const h=document.createElement('h1');h.textContent=v.ad+' — '+v.baslik+' ('+v.sure+' sn)';kok.appendChild(h);
 const kap=document.createElement('div');kap.style.cssText='position:absolute;left:-9999px;width:800px;height:500px';document.body.appendChild(kap);
 const a=lottie.loadAnimation({container:kap,renderer:'canvas',loop:false,autoplay:false,animationData:veri,rendererSettings:{clearCanvas:true}});
 await new Promise(r=>{if(a.isLoaded)r();else a.addEventListener('DOMLoaded',r);});const cv=kap.querySelector('canvas');const rapor=[];
 for(let i=0;i<v.bolumler.length;i++){const b=v.bolumler[i];const sat=document.createElement('div');sat.className='sat';sat.style.flexWrap='wrap';kok.appendChild(sat);const bul=[];
  for(const f of KARE){const t=b.bas+(b.son-b.bas)*f;a.goToAndStop(Math.min(a.totalFrames-1,Math.round(t*30)),true);
   const hc=document.createElement('div');hc.className='hc';const s=document.createElement('div');s.className='sahne';const im=new Image();im.src=beyaz(cv);
   s.appendChild(im);const al=document.createElement('div');al.className='alt';s.appendChild(al);hc.appendChild(s);sat.appendChild(hc);
   if(bosMu(cv))bul.push('boş kare @'+t.toFixed(1));
   const fb=[];const els=katman(v,t,s,fb);await new Promise(r=>requestAnimationFrame(r));denetle(els,s,fb);bul.push(...fb.map(x=>x+' @'+t.toFixed(1)));
   const kt=document.createElement('div');kt.className='kt';const kam=kameraAn(v,t);kt.textContent='t='+t.toFixed(2)+' sn · kamera '+kam.map(x=>x.toFixed(0)).join(',');hc.appendChild(kt);}
  const m=document.createElement('div');m.className='met';const uniq=[...new Set(bul)];m.innerHTML='<b>'+(i+1)+'.</b> '+b.metin.replace(/</g,'&lt;')+(uniq.length?'<div class="bul">⚑ '+uniq.join('<br>⚑ ').replace(/</g,'&lt;')+'</div>':'');
  sat.appendChild(m);rapor.push({cumle:i+1,bulgular:uniq});}
 a.destroy();kap.remove();await new Promise(r=>setTimeout(r,50));return{rapor,h:document.documentElement.scrollHeight};}
</script>`);
await send('Page.navigate', { url: 'file://' + sayfa });
await sleep(1200);
const rapor = {};
for (const v of secili) {
  const veri = fs.readFileSync(path.join(LOT, `${v.ad}.json`), 'utf8');
  const r = await ev(`isle(${JSON.stringify(v)}, ${veri}, ${JSON.stringify(KARE)})`);
  await send('Emulation.setDeviceMetricsOverride', { width: GEN * KARE.length + 80, height: Math.min(r.h, 16000), deviceScaleFactor: 1, mobile: false });
  await sleep(150);
  const shot = await send('Page.captureScreenshot', { format: 'jpeg', quality: 82, captureBeyondViewport: true, clip: { x: 0, y: 0, width: GEN * KARE.length + 80, height: Math.min(r.h, 16000), scale: 1 } });
  fs.writeFileSync(path.join(OUT, `${v.ad}.jpg`), Buffer.from(shot.data, 'base64'));
  rapor[v.ad] = r.rapor;
  const n = r.rapor.reduce((s, x) => s + x.bulgular.length, 0);
  console.log(`${v.ad}: ${r.rapor.length} bölüm, ${n} otomatik bulgu → ${path.join(OUT, v.ad + '.jpg')}`);
}
fs.writeFileSync(path.join(OUT, 'rapor.json'), JSON.stringify(rapor, null, 1));
ws.close();
process.exit(0);
