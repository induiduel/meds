// Ortak başsız Chrome + CDP yardımcısı (çevrimdışı sınamaları). Kalıcı profil: PROFIL klasörü (SW + önbellekler korunur).
import { spawn } from 'node:child_process';
import fs from 'node:fs';
export const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
export async function tarayici({ profil, temiz = false } = {}) {
  const PORT = 9800 + Math.floor(Math.random() * 150);
  const dir = profil || `${process.env.HOME}/.cache/medsor-cevrimdisi/chrome-${PORT}`;
  if (temiz) fs.rmSync(dir, { recursive: true, force: true });
  const chrome = spawn('/opt/google/chrome/chrome', ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${dir}`, '--no-first-run',
    '--disable-extensions', '--mute-audio', '--autoplay-policy=no-user-gesture-required', '--window-size=1280,900'], { stdio: 'ignore' });
  process.on('exit', () => { try { chrome.kill('SIGKILL'); } catch {} if (!profil) try { fs.rmSync(dir, { recursive: true, force: true }); } catch {} });
  for (let i = 0; i < 60; i++) { try { await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json(); break; } catch { await sleep(200); } }
  const tgt = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: 'PUT' })).json();
  const ws = new WebSocket(tgt.webSocketDebuggerUrl);
  await new Promise((r) => ws.addEventListener('open', r));
  let id = 0; const pend = new Map(); const dinleyici = new Set();
  ws.addEventListener('message', (m) => {
    const d = JSON.parse(m.data);
    if (d.id && pend.has(d.id)) { const p = pend.get(d.id); pend.delete(d.id); d.error ? p.rej(new Error(JSON.stringify(d.error))) : p.res(d.result); }
    else if (d.method) for (const f of dinleyici) f(d.method, d.params);
  });
  const send = (method, params = {}) => new Promise((res, rej) => { const i = ++id; pend.set(i, { res, rej }); ws.send(JSON.stringify({ id: i, method, params })); });
  const ev = async (expr, t = 120000) => {
    const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true, timeout: t });
    if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description || r.exceptionDetails.text);
    return r.result?.value;
  };
  await send('Page.enable'); await send('Runtime.enable'); await send('Network.enable'); await send('Log.enable');
  return { send, ev, on: (f) => { dinleyici.add(f); return () => dinleyici.delete(f); }, kapat: () => { try { chrome.kill('SIGKILL'); } catch {} } };
}
export const SEED = `(() => { const now = new Date().toISOString(); const s = (k, v) => localStorage.setItem(k, v);
  s('medsoru_user_registered','1'); s('medsoru_giris_uyarisi_v1', JSON.stringify({surum:1,at:now}));
  ['medsoru_tour_v1','medsoru_canli_ders_tur_ders_v1','medsoru_canli_ders_tur_liste_v1','medsoru_canli_ders_tv_tanitim_v1','medsoru_learn_tour_lesson_v1','medsoru_learn_tour_library_v1','medsoru_splash_seen'].forEach(k => s(k, JSON.stringify({done:true,at:now,surum:9})));
})()`;
export const ag = async (kapat) => { await fetch(`http://127.0.0.1:3101/${kapat ? 'kapat' : 'ac'}`); };
