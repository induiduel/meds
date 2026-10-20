// Çevrimdışı sınama vekili: :3100 → :3000. Denetim :3101 (/kapat, /ac, /durum). Kapalıyken her bağlantı anında kesilir
// (tarayıcı ve SW gerçek ağ hatası görür). Ayrı köken olduğundan SW ve önbellekler canlı/yerel kullanımdan bağımsızdır.
import http from 'node:http';
const HEDEF = Number(process.env.HEDEF || 3000), PORT = Number(process.env.PORT || 3100);
let kapali = false; const soketler = new Set();
const s = http.createServer((req, res) => {
  if (kapali) { req.socket.destroy(); return; }
  const p = http.request({ host: '127.0.0.1', port: HEDEF, path: req.url, method: req.method, headers: req.headers }, (r) => { res.writeHead(r.statusCode, r.headers); r.pipe(res); });
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
console.log(`vekil :${PORT} → :${HEDEF}, denetim :${PORT + 1}`);
