// Aşama 2: Drive envanteri (yalnızca metadata, dosya indirmez). Çıktı: meds_downloads/_manifest.json
import fs from 'fs'; import path from 'path'; import crypto from 'crypto';
import { DOWNLOADS_DIR, DRIVE_ROOTS } from './config.mjs';
const UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/122 Safari/537.36';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const visited = new Set(); const items = [];

async function list(folderId) {
  for (let t = 0; t < 3; t++) {
    try {
      const res = await fetch(`https://drive.google.com/drive/folders/${folderId}`, { headers: { 'User-Agent': UA, 'Accept-Language': 'tr-TR,tr;q=0.9' } });
      if (!res.ok) { await sleep(1500 * (t + 1)); continue; }
      const m = (await res.text()).match(/window\['_DRIVE_ivd'\]\s*=\s*'([^']+)'/);
      if (!m) return [];
      const un = m[1].replace(/\\\\x([0-9a-fA-F]{2})/g, (_, h) => String.fromCharCode(parseInt(h, 16)))
                     .replace(/\\x([0-9a-fA-F]{2})/g, (_, h) => String.fromCharCode(parseInt(h, 16)));
      const out = []; const seen = new Set();
      (function rec(v) {
        if (!Array.isArray(v)) return;
        if (typeof v[0] === 'string' && v[0].length >= 25 && typeof v[2] === 'string' && typeof v[3] === 'string' && !seen.has(v[0])) {
          seen.add(v[0]); out.push({ id: v[0], name: v[2], mime: v[3] });
        }
        v.forEach(rec);
      })(JSON.parse(un));
      return out.filter(o => o.id !== folderId);
    } catch (e) { await sleep(1500 * (t + 1)); }
  }
  console.warn('[HATA] listelenemedi:', folderId); return [];
}

async function crawl(folderId, relPath, rootKey) {
  if (visited.has(folderId)) return; visited.add(folderId);
  for (const it of await list(folderId)) {
    const isFolder = it.mime.includes('folder');
    const p = relPath ? `${relPath}/${it.name}` : it.name;
    items.push({ source_id: crypto.createHash('sha1').update(it.id).digest('hex').slice(0, 12),
      drive_id: it.id, name: it.name, mime: it.mime, is_folder: isFolder, path: p, root: rootKey });
    if (isFolder) { await sleep(300); await crawl(it.id, p, rootKey); }
  }
}

for (const r of DRIVE_ROOTS) { console.log('>>', r.name); await crawl(r.id, '', r.key); }
const files = items.filter(i => !i.is_folder);
const byMime = {}; for (const f of files) byMime[f.mime] = (byMime[f.mime] || 0) + 1;
fs.mkdirSync(DOWNLOADS_DIR, { recursive: true });
fs.writeFileSync(path.join(DOWNLOADS_DIR, '_manifest.json'), JSON.stringify({
  generated_at: new Date().toISOString(), folders: items.length - files.length, files: files.length, by_mime: byMime, items }, null, 2));
console.log(`Klasör: ${items.length - files.length}  Dosya: ${files.length}`, byMime);
