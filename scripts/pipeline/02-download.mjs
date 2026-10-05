// Aşama 3: Drive dosyalarını meds_downloads altına indirir (artımlı, devam edilebilir, sıralı).
// Önce ücretsiz herkese açık indirme; başarısız olursa GOOGLE_SERVICE_ACCOUNT_FILE varsa Drive API (servis hesabı).
// Kullanım: node scripts/pipeline/02-download.mjs [--limit N] [--rate KBps] [--dry]
import fs from 'fs'; import path from 'path'; import crypto from 'crypto';
import { Readable } from 'stream'; import { pipeline } from 'stream/promises'; import { Transform } from 'stream';
import { DOWNLOADS_DIR } from './config.mjs';

const arg = (n, d) => { const i = process.argv.indexOf('--' + n); return i < 0 ? d : (process.argv[i + 1] ?? true); };
const LIMIT = Number(arg('limit', 0)), RATE = Number(arg('rate', 0)) * 1024, DRY = process.argv.includes('--dry');
const WANT = /\.(pdf|pptx|docx?)$/i;
const manifestPath = path.join(DOWNLOADS_DIR, '_manifest.json');
const statePath = path.join(DOWNLOADS_DIR, '_downloads.json');
const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
const state = fs.existsSync(statePath) ? JSON.parse(fs.readFileSync(statePath, 'utf8')) : {};
const save = () => fs.writeFileSync(statePath, JSON.stringify(state, null, 2));
const sleep = ms => new Promise(r => setTimeout(r, ms));
const safe = s => s.replace(/[\\:*?"<>|]/g, '_').split('/').map(x => x.trim()).filter(Boolean).join('/');

// --- servis hesabı (isteğe bağlı yedek) ---
let saTokenCache = null;
async function saToken() {
  const f = process.env.GOOGLE_SERVICE_ACCOUNT_FILE; if (!f || !fs.existsSync(f)) return null;
  if (saTokenCache && saTokenCache.exp > Date.now() + 60000) return saTokenCache.token;
  const sa = JSON.parse(fs.readFileSync(f, 'utf8')); const now = Math.floor(Date.now() / 1000);
  const b = o => Buffer.from(JSON.stringify(o)).toString('base64url');
  const unsigned = b({ alg: 'RS256', typ: 'JWT' }) + '.' + b({ iss: sa.client_email, scope: 'https://www.googleapis.com/auth/drive.readonly', aud: sa.token_uri, iat: now, exp: now + 3600 });
  const sig = crypto.sign('RSA-SHA256', Buffer.from(unsigned), sa.private_key).toString('base64url');
  const r = await fetch(sa.token_uri, { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ grant_type: 'urn:ietf:params:oauth:grant-type:jwt-bearer', assertion: unsigned + '.' + sig }) });
  const j = await r.json(); if (!j.access_token) return null;
  saTokenCache = { token: j.access_token, exp: Date.now() + 3500000 }; return saTokenCache.token;
}

async function open(id, method) {
  if (method === 'free') {
    const r = await fetch(`https://drive.usercontent.google.com/download?id=${id}&export=download&confirm=t`, { redirect: 'follow' });
    const ct = r.headers.get('content-type') || '';
    if (!r.ok || ct.includes('text/html')) return null; // kota/izin sayfası
    return r;
  }
  const t = await saToken(); if (!t) return null;
  const r = await fetch(`https://www.googleapis.com/drive/v3/files/${id}?alt=media`, { headers: { Authorization: `Bearer ${t}` } });
  return r.ok ? r : null;
}

function throttle(bps) {
  if (!bps) return new Transform({ transform(c, _, cb) { cb(null, c); } });
  let sent = 0; const t0 = Date.now();
  return new Transform({ async transform(c, _, cb) { sent += c.length;
    const wait = sent / bps * 1000 - (Date.now() - t0); if (wait > 0) await sleep(wait); cb(null, c); } });
}

const todo = manifest.items.filter(i => !i.is_folder && WANT.test(i.name) && state[i.drive_id]?.status !== 'done');
const all = manifest.items.filter(i => !i.is_folder && WANT.test(i.name));
console.log(`Hedef: ${all.length} dosya, kalan: ${todo.length}${DRY ? ' (dry-run)' : ''}`);
if (DRY) process.exit(0);

let n = 0, fail = 0, bytes = 0;
for (const it of todo) {
  if (LIMIT && n >= LIMIT) break; n++;
  const rel = path.join(it.root, safe(it.path)); const dest = path.join(DOWNLOADS_DIR, rel); const part = dest + '.part';
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  let ok = false, via = null;
  for (const method of ['free', 'service_account']) {
    for (let t = 0; t < 2 && !ok; t++) {
      try {
        const res = await open(it.drive_id, method); if (!res) break;
        const hash = crypto.createHash('sha256'); let size = 0;
        const counter = new Transform({ transform(c, _, cb) { hash.update(c); size += c.length; cb(null, c); } });
        await pipeline(Readable.fromWeb(res.body), throttle(RATE), counter, fs.createWriteStream(part));
        if (size < 1024) { fs.rmSync(part, { force: true }); break; }
        fs.renameSync(part, dest);
        state[it.drive_id] = { status: 'done', path: rel, size, sha256: hash.digest('hex'), via: method, at: new Date().toISOString() };
        bytes += size; ok = true; via = method;
      } catch (e) { fs.rmSync(part, { force: true }); await sleep(2000 * (t + 1)); }
    }
    if (ok) break;
  }
  if (!ok) { fail++; state[it.drive_id] = { status: 'failed', path: rel, at: new Date().toISOString() }; }
  console.log(`${ok ? 'OK ' : 'HATA'} [${n}/${todo.length}] ${via ?? ''} ${rel}`);
  save(); await sleep(1000);
}
console.log(`Bitti. indirilen: ${(bytes / 1048576).toFixed(1)} MB, hata: ${fail}`);
