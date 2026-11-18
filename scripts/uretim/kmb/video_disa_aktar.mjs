// KMB videolarını tek parça MP4 olarak dışa aktarır (2026-11-18, kullanıcı isteği):
//   ders    = "Tüm ders · tam ekran" (DersVideo: adım videoları art arda, EMA o-<adım> sesleri)
//   basamak = "Basamak filmi (KMB rehberi)" (HedefFilmi tur=basamak: rehber basamakları, p-<no> sesleri)
// Yöntem: yerel sitede (3000) başsız Chrome gerçek oynatıcıyı açar ve gerçek zamanlı oynatır; görüntü CDP screencast
// kareleri (zaman damgalı), ses ise sayfadaki her <audio> oynatma aralığının (kaynak, duvar saati, ortam saati) kaydından
// ffmpeg ile yeniden kurulur (başsız Chrome sesi yakalanamaz). Bitiş: oynatıcı body[data-kmb-bitti] yazar.
// Yalnız anlatım: denetimler, şeritler, hoca sorusu/düşünme payı ve bitiş ekranı videoya girmez (window.__kmbKayit).
// Video sitede ne görünüyorsa odur (aynı bileşenler) — ayrı bir çizim kopyası yok, sapma olmaz. Süre ≈ video süresi.
//
// Kullanım: node meds/scripts/uretim/kmb/video_disa_aktar.mjs <kod|slug> [ders|basamak|ikisi]   (varsayılan ikisi, paralel)
//   OUT=klasör (varsayılan data/kmb_cozucu/ses_video/<kod>: site /api/kmb-video/<kod>/<tur>.mp4 ile indirir, ses_esitle.sh Oracle'a taşır)  GEN=1280 YUK=720  SITE=http://localhost:3000  FPS=30
// Çıktı: OUT/ders.mp4, OUT/basamak.mp4 (H.264 + AAC, yuv420p, faststart) + src/data/kmb/video.json künyesi (indir düğmesi
//   yalnız künyede olan videoda görünür; künye ön yüz paketinde → yayın için vite build + dagit.sh).
// LLM/API kullanmaz (kural 20 dışı); GPU kullanmaz (libx264, CPU).
import { spawn, spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const MEDS = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const KOK = path.resolve(MEDS, '..');
const SITE = process.env.SITE || 'http://localhost:3000';
const GEN = +(process.env.GEN || 1280), YUK = +(process.env.YUK || 720), FPS = +(process.env.FPS || 30);
let OUT;
const [istek, turArg = 'ikisi'] = process.argv.slice(2);
if (!istek || !['ders', 'basamak', 'ikisi'].includes(turArg)) {
  console.error('Kullanım: video_disa_aktar.mjs <kod|slug> [ders|basamak|ikisi]'); process.exit(2);
}
const dersler = JSON.parse(fs.readFileSync(path.join(MEDS, 'src/data/kmb/index.json'), 'utf8'));
const dersBul = () => {
  for (const f of fs.readdirSync(path.join(MEDS, 'src/data/kmb')).filter((x) => /^\d+\.json$/.test(x))) {
    const d = JSON.parse(fs.readFileSync(path.join(MEDS, 'src/data/kmb', f), 'utf8'));
    if (d.kod === istek || d.slug === istek || d.kod === istek.padStart(2, '0')) return d;
  }
  return null;
};
const ders = dersBul();
if (!ders) { console.error(`KMB dersi yok: ${istek} (var: ${JSON.stringify(dersler).slice(0, 200)})`); process.exit(2); }
const turler = turArg === 'ikisi' ? ['ders', 'basamak'] : [turArg];
if (turler.includes('basamak') && !ders.rehberBasamaklari?.length) { console.error(`${ders.kod}: rehber basamağı yok`); process.exit(2); }
const sir = (fs.readFileSync(path.join(MEDS, '.env'), 'utf8').match(/^MEDS_PANEL_SECRET=(.*)$/m) || [])[1]?.trim().replace(/^["']|["']$/g, '');
if (!sir) { console.error('.env MEDS_PANEL_SECRET yok (yapay zekâ test girişi gerekir)'); process.exit(2); }
OUT = path.resolve(process.env.OUT || path.join(MEDS, 'data/kmb_cozucu/ses_video', ders.kod));
fs.mkdirSync(OUT, { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const DUGME = { ders: 'Tüm ders · tam ekran', basamak: 'Basamak filmi (KMB rehberi)' };

async function kaydet(tur) {
  const ad = `${ders.kod}-${ders.slug}-${tur}`;
  // çalışma klasörü (kareler, Chrome profili) meds_temp'te: OUT ses_esitle.sh ile Oracle'a eşitlenir, oraya çöp gitmesin (H639)
  const is = path.join(KOK, 'meds_temp/kmb_video', `.${ad}`);
  fs.rmSync(is, { recursive: true, force: true }); fs.mkdirSync(path.join(is, 'kare'), { recursive: true });
  const log = (...a) => console.log(`[${tur}]`, ...a);
  const PORT = 9300 + Math.floor(Math.random() * 600);
  const chrome = spawn('/opt/google/chrome/chrome', ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${path.join(is, 'profil')}`,
    '--no-first-run', '--disable-extensions', '--mute-audio', '--hide-scrollbars', '--autoplay-policy=no-user-gesture-required',
    `--window-size=${GEN},${YUK}`, `--screen-info={${GEN}x${YUK}}`, /* ekran 800×600 kalırsa screencast karesi kesik gelir */ '--disable-background-timer-throttling', '--disable-renderer-backgrounding'], { stdio: 'ignore' });
  const kapat = () => { try { chrome.kill('SIGKILL'); } catch { /* */ } };
  process.on('exit', kapat);
  try {
    for (let i = 0; i < 75; i++) { try { await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json(); break; } catch { await sleep(200); } }
    // açılıştaki sekme --window-size ile açılır (/json/new ile açılan sekme 800×600 kalıyordu → kare kesik)
    let tgt = null;
    for (let i = 0; i < 50 && !tgt; i++) { tgt = (await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json()).find((x) => x.type === 'page') || null; if (!tgt) await sleep(100); }
    if (!tgt) tgt = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: 'PUT' })).json();
    const ws = new WebSocket(tgt.webSocketDebuggerUrl);
    await new Promise((r) => ws.addEventListener('open', r));
    let id = 0; const pend = new Map(); const kareler = [];
    const send = (method, params = {}) => new Promise((res, rej) => { const i = ++id; pend.set(i, { res, rej }); ws.send(JSON.stringify({ id: i, method, params })); });
    ws.addEventListener('message', (m) => {
      const d = JSON.parse(m.data);
      if (d.id && pend.has(d.id)) { const p = pend.get(d.id); pend.delete(d.id); d.error ? p.rej(new Error(JSON.stringify(d.error))) : p.res(d.result); return; }
      if (d.method === 'Page.screencastFrame') {
        const { data, metadata, sessionId } = d.params;
        const f = path.join(is, 'kare', `${String(kareler.length).padStart(6, '0')}.jpg`);
        fs.writeFileSync(f, Buffer.from(data, 'base64'));
        kareler.push({ f, t: metadata.timestamp * 1000 });
        send('Page.screencastFrameAck', { sessionId }).catch(() => {});
      } else if (d.method === 'Runtime.exceptionThrown') log('sayfa hatası:', d.params.exceptionDetails?.exception?.description?.slice(0, 200));
    });
    const ev = async (expr) => { const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true }); if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description || r.exceptionDetails.text); return r.result?.value; };
    await send('Page.enable'); await send('Runtime.enable');
    // başsız pencere 800×600 açılır; screencast pencereyi çeker → pencereyi GEN×YUK yap, sayfa düzeni de aynı boyutta olsun
    // (yalnız Emulation düzeni büyütür, kare 800×600'de kesik kalır: sağ/alt ve altyazı videoya girmiyordu)
    try { const { windowId } = await send('Browser.getWindowForTarget'); await send('Browser.setWindowBounds', { windowId, bounds: { width: GEN, height: YUK } }); } catch (e) { log('pencere boyutu:', e.message); }
    await send('Emulation.setDeviceMetricsOverride', { width: GEN, height: YUK, deviceScaleFactor: 1, mobile: false, screenWidth: GEN, screenHeight: YUK });
    // ses kaydedici: her <audio> öğesinin oynadığı aralıklar → window.__sesAralik [{src, w0, m0, w1, m1, hiz}] (w = epoch ms)
    await send('Page.addScriptToEvaluateOnNewDocument', { source: `(() => {
      // yalnız anlatım (kullanıcı kararı 2026-11-18): soru/düşünme atlanır (HedefFilmi), denetim/şerit/menü/bitiş ekranı gizlenir
      window.__kmbKayit = true;
      document.addEventListener('DOMContentLoaded', () => { const st = document.createElement('style'); st.textContent =
        '.kmb-dv-ust,.kmb-hf-dugmeler,.kmb-hf-serit,.kmb-hf-denetim,.kmb-hf-ray,.kmb-hf-son,.kmb-hf-yukleniyor,.kmb-hf-soru,' +
        '.kmb-lv-cubuk,.kmb-lv-orta,.kmb-lv-jest-ipucu,.kmb-lv-ince,.kmb-lv-menu,.kmb-lv-son,.kmb-lv-isik,.kmb-lv-onizle,.kmb-lv-ust' +
        '{display:none!important} .kmb-dv *,.kmb-hf *{cursor:none!important}'; document.head.appendChild(st); });
      // oynatıcı sesi blob: adresinden çalar (sesOnYukle): blob'u sakla, kayıt sonunda sayfa içinden okunur
      const B = new Map(), co = URL.createObjectURL; URL.createObjectURL = function (b) { const u = co.call(URL, b); if (b instanceof Blob) B.set(u, b); return u; };
      URL.revokeObjectURL = () => {}; // kayıt boyunca blob'lar düşmesin
      window.__blobAl = async (u) => { const b = B.get(u); if (!b) return null; const x = new Uint8Array(await b.arrayBuffer()); let s = '';
        for (let i = 0; i < x.length; i += 32768) s += String.fromCharCode(...x.subarray(i, i + 32768)); return btoa(s); };
      const L = window.__sesAralik = []; const acik = new WeakMap(); const sim = () => performance.timeOrigin + performance.now();
      const kapa = (a) => { const s = acik.get(a); if (!s) return; s.w1 = sim(); s.m1 = a.currentTime; L.push(s); acik.delete(a); };
      const ac = (a) => { kapa(a); if (!a.paused && a.currentSrc) acik.set(a, { src: a.currentSrc, w0: sim(), m0: a.currentTime, hiz: a.playbackRate }); };
      const bag = (a) => { if (a.__sk) return; a.__sk = 1;
        a.addEventListener('playing', () => ac(a)); a.addEventListener('seeked', () => ac(a)); a.addEventListener('ratechange', () => ac(a));
        ['pause', 'ended', 'emptied', 'waiting', 'seeking'].forEach((e) => a.addEventListener(e, () => kapa(a))); };
      const p = HTMLMediaElement.prototype.play; HTMLMediaElement.prototype.play = function () { bag(this); return p.apply(this, arguments); };
      window.__sesKapat = () => document.querySelectorAll('audio,video').forEach(kapa);
      const eskiA = window.Audio; window.Audio = function (...x) { const o = new eskiA(...x); bag(o); window.__tumSes = (window.__tumSes || []); window.__tumSes.push(o); return o; };
      window.Audio.prototype = eskiA.prototype;
      window.__sesKapat = () => (window.__tumSes || []).concat([...document.querySelectorAll('audio,video')]).forEach(kapa);
    })();` });
    // giriş: yapay zekâ test çerezi (anahtar yalnız başlıkta, URL'de değil)
    await send('Page.navigate', { url: `${SITE}/api/health` }); await sleep(800);
    const giris = await ev(`fetch('/api/ai-test/oturum',{method:'POST',headers:{'x-panel-secret':${JSON.stringify(sir)}}}).then(r=>r.status)`);
    if (giris !== 200) throw new Error(`test girişi başarısız (${giris})`);
    // giriş bilgilendirmesi (GirisUyarisi) bu başsız profilde kabul edilmiş sayılsın — yoksa pencere oynatıcıyı örter
    await ev(`localStorage.setItem('medsoru_giris_uyarisi_v1', JSON.stringify({surum: 99, at: new Date().toISOString()}))`);
    await send('Page.navigate', { url: `${SITE}/dersler/kmb/${ders.slug}` });
    let dugme = false;
    for (let i = 0; i < 100 && !dugme; i++) {
      await sleep(300);
      dugme = await ev(`(() => { const b = [...document.querySelectorAll('button')].find((x) => x.textContent.trim().startsWith(${JSON.stringify(DUGME[tur])}) && x.offsetParent);
        if (!b) return false; b.scrollIntoView({block:'center'}); const r = b.getBoundingClientRect(); const x = r.x + r.width / 2, y = r.y + r.height / 2;
        const ust = document.elementFromPoint(x, y); if (!ust || !(b === ust || b.contains(ust))) { document.querySelector('.bs-k-perde')?.click(); return false; } // üstünde kutlama/pencere var: kutlamayı kapat, yeniden dene
        window.__dg = [x, y]; return true; })()`);
    }
    if (!dugme) { const g = await send('Page.captureScreenshot', { format: 'png' }); fs.writeFileSync(path.join(OUT, `${ad}-hata.png`), Buffer.from(g.data, 'base64'));
      log('engelleyen:', await ev(`(() => { const b = [...document.querySelectorAll('button')].find((x) => x.textContent.trim().startsWith(${JSON.stringify(DUGME[tur])})); if (!b) return 'düğme yok'; const r = b.getBoundingClientRect(); const u = document.elementFromPoint(r.x + r.width / 2, r.y + r.height / 2); return u ? u.outerHTML.slice(0, 200) : 'nokta dışı ' + JSON.stringify(r); })()`)); }
    if (!dugme) throw new Error(`"${DUGME[tur]}" düğmesi bulunamadı (${SITE}/dersler/kmb/${ders.slug})`);
    await sleep(1500); // ses verisi (ses_<kod>.json) yüklensin
    const [x, y] = await ev('window.__dg');
    await send('Page.startScreencast', { format: 'jpeg', quality: 88, maxWidth: GEN, maxHeight: YUK, everyNthFrame: 1 });
    await sleep(300);
    const t0 = await ev('performance.timeOrigin + performance.now()');
    for (const type of ['mousePressed', 'mouseReleased']) await send('Input.dispatchMouseEvent', { type, x, y, button: 'left', clickCount: 1 });
    // fare imleci/denetimler kendiliğinden gizlensin diye imleci köşeye çek
    await sleep(400); await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: GEN - 1, y: YUK - 1 });
    log('oynatılıyor (gerçek zamanlı)…');
    let son = 0, bitti = false;
    while (!bitti) {
      await sleep(2000);
      bitti = await ev(`document.body.dataset.kmbBitti === ${JSON.stringify(tur)}`);
      const s = Math.round((Date.now() - t0) / 1000);
      if (s - son >= 30) { son = s; log(`${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')} · ${kareler.length} kare · ${(await ev('window.__sesAralik.length'))} ses aralığı`); }
      if (s > 60 && !(await ev('window.__sesAralik.length + (window.__tumSes || []).filter((a) => !a.paused).length'))) throw new Error('60 sn içinde ses başlamadı (oynatıcı açılmadı?)');
      if (s > 4 * 3600) throw new Error('4 saati aştı, bitiş işareti gelmedi');
    }
    await sleep(1200); // son kare
    await ev('window.__sesKapat()');
    const t1 = await ev('performance.timeOrigin + performance.now()');
    await send('Page.stopScreencast');
    const aralik = (await ev('window.__sesAralik')).filter((a) => a.w1 > a.w0 + 20);
    if (!kareler.length) throw new Error('hiç kare gelmedi');
    log(`kayıt bitti: ${((t1 - t0) / 1000).toFixed(1)} sn, ${kareler.length} kare, ${aralik.length} ses aralığı`);

    // görüntü: concat listesi (her kare bir sonrakine dek ekranda)
    const kl = [];
    const ilk = kareler.findIndex((k) => k.t >= t0); const bas = Math.max(0, ilk === -1 ? 0 : ilk - 1);
    const K = kareler.slice(bas);
    for (let i = 0; i < K.length; i++) {
      const a = Math.max(K[i].t, t0), b = i + 1 < K.length ? K[i + 1].t : t1;
      if (b - a <= 0) continue;
      kl.push(`file '${K[i].f}'`, `duration ${((b - a) / 1000).toFixed(4)}`);
    }
    kl.push(`file '${K[K.length - 1].f}'`);
    fs.writeFileSync(path.join(is, 'kareler.txt'), kl.join('\n') + '\n');
    // ses: her aralık kendi kaynağından [m0, m1] kesilir, w0 - t0 gecikmeyle yerleştirilir, hepsi karıştırılır
    const girdiler = [], filtre = [];
    const sesDosya = new Map();
    for (const a of aralik) {
      let yer = sesDosya.get(a.src);
      if (!yer) {
        yer = path.join(is, `ses${sesDosya.size}.mp3`);
        if (a.src.startsWith('blob:')) {
          const b64 = await ev(`window.__blobAl(${JSON.stringify(a.src)})`); if (!b64) throw new Error(`ses blob'u okunamadı ${a.src}`);
          fs.writeFileSync(yer, Buffer.from(b64, 'base64'));
        } else {
          const r = await fetch(new URL(a.src, SITE)); if (!r.ok) throw new Error(`ses indirilemedi ${a.src} (${r.status})`);
          fs.writeFileSync(yer, Buffer.from(await r.arrayBuffer()));
        }
        sesDosya.set(a.src, yer);
      }
      const n = girdiler.length / 2;
      girdiler.push('-i', yer);
      const gec = Math.max(0, Math.round(a.w0 - t0));
      const hiz = a.hiz && Math.abs(a.hiz - 1) > 0.01 ? `,atempo=${a.hiz}` : '';
      filtre.push(`[${n + 1}:a]atrim=start=${a.m0.toFixed(3)}:end=${a.m1.toFixed(3)},asetpts=PTS-STARTPTS${hiz},aresample=48000,aformat=channel_layouts=stereo,adelay=${gec}|${gec}[s${n}]`);
    }
    ws.close(); kapat();
    const cikis = path.join(OUT, `${tur}.mp4`);
    const arg = ['-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', path.join(is, 'kareler.txt'), ...girdiler];
    if (aralik.length) {
      filtre.push(`${aralik.map((_, i) => `[s${i}]`).join('')}amix=inputs=${aralik.length}:normalize=0:dropout_transition=0[ses]`);
      fs.writeFileSync(path.join(is, 'filtre.txt'), filtre.join(';\n'));
      arg.push('-filter_complex_script', path.join(is, 'filtre.txt'), '-map', '0:v', '-map', '[ses]', '-c:a', 'aac', '-b:a', '160k');
    }
    arg.push('-vf', `fps=${FPS},scale=${GEN}:${YUK}:force_original_aspect_ratio=decrease,pad=${GEN}:${YUK}:(ow-iw)/2:(oh-ih)/2:color=black,format=yuv420p`,
      '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-t', ((t1 - t0) / 1000).toFixed(3), '-movflags', '+faststart', cikis);
    log('ffmpeg birleştiriyor…');
    const r = spawnSync('ffmpeg', arg, { stdio: ['ignore', 'inherit', 'inherit'] });
    if (r.status !== 0) throw new Error(`ffmpeg çıkış ${r.status}`);
    fs.rmSync(is, { recursive: true, force: true });
    const mb = (fs.statSync(cikis).size / 1048576).toFixed(1);
    // künye: indir düğmesi + önbellek kırıcı (v = boyut+zaman özeti)
    const KY = path.join(MEDS, 'src/data/kmb/video.json');
    const ky = fs.existsSync(KY) ? JSON.parse(fs.readFileSync(KY, 'utf8')) : {};
    const st = fs.statSync(cikis);
    (ky[ders.kod] ||= {})[tur] = { mb: +mb, sn: Math.round((t1 - t0) / 1000), v: (st.size ^ Math.round(st.mtimeMs)).toString(36).replace('-', ''), tarih: new Date().toISOString().slice(0, 10) };
    fs.writeFileSync(KY, JSON.stringify(ky, null, 1) + '\n');
    log(`HAZIR: ${cikis} (${mb} MB, ${((t1 - t0) / 60000).toFixed(1)} dk) · künye src/data/kmb/video.json`);
    return cikis;
  } finally { kapat(); }
}

const sonuc = await Promise.allSettled(turler.map(kaydet));
let hata = 0;
sonuc.forEach((s, i) => { if (s.status === 'rejected') { hata++; console.error(`[${turler[i]}] HATA:`, s.reason?.message || s.reason); } });
process.exit(hata ? 1 : 0);
