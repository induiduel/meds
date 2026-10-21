// Çevrimdışı sınama vekili: :3100 → :3000. Denetim :3101 (/kapat, /ac, /durum). Kapalıyken her bağlantı anında kesilir
// (tarayıcı ve SW gerçek ağ hatası görür). Ayrı köken olduğundan SW ve önbellekler canlı/yerel kullanımdan bağımsızdır.
import http from 'node:http';
import https from 'node:https';
// HEDEF: yerel port (3000) ya da canlı adres (HEDEF=https://nofrostlife.com.tr → canlı veriyle sınama)
const HEDEF = process.env.HEDEF || '3000', PORT = Number(process.env.PORT || 3100);
const uzak = /^https?:/.test(HEDEF) ? new URL(HEDEF) : null;
let kapali = false; const soketler = new Set();
const s = http.createServer((req, res) => {
  if (kapali) { req.socket.destroy(); return; }
  const mod = uzak?.protocol === 'https:' ? https : http;
  const hedef = uzak ? { host: uzak.hostname, port: uzak.port || (uzak.protocol === 'https:' ? 443 : 80), headers: { ...req.headers, host: uzak.host } }
    : { host: '127.0.0.1', port: Number(HEDEF), headers: req.headers };
  const p = mod.request({ ...hedef, path: req.url, method: req.method }, (r) => {
    // Canlının Domain'li çerezleri localhost'ta da tutulsun
    const h = { ...r.headers };
    if (uzak && h['set-cookie']) h['set-cookie'] = [].concat(h['set-cookie']).map((c) => c.replace(/;\s*Domain=[^;]+/i, ''));
    res.writeHead(r.statusCode, h); r.pipe(res);
  });
  p.on('error', () => { try { res.destroy(); } catch {} });
  req.pipe(p);
});
s.on('connection', (k) => { if (kapali) return k.destroy(); soketler.add(k); k.on('close', () => soketler.delete(k)); });
s.listen(PORT, '127.0.0.1');
http.createServer((req, res) => {
  if (req.url === '/kapat') { kapali = true; for (const k of soketler) k.destroy(); }
  if (req.url === '/ac') kapali = false;
  res.end(JSON.stringify({ kapali }));
}).listen(PORT + 1, '127.0.0.1');
console.log(`vekil :${PORT} → ${HEDEF}, denetim :${PORT + 1}`);
