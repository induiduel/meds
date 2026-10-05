import fs from 'fs';
import path from 'path';
import https from 'https';

function downloadDriveBuffer(fileId) {
  return new Promise((resolve, reject) => {
    const url = `https://drive.usercontent.google.com/download?id=${fileId}&export=download&authuser=0&confirm=t`;
    function req(u, red = 0) {
      if (red > 5) return reject(new Error('Çok fazla yönlendirme'));
      https.get(u, { headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' } }, (res) => {
        if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
          return req(res.headers.location, red + 1);
        }
        if (res.statusCode !== 200) return reject(new Error(`HTTP Durumu: ${res.statusCode}`));
        const chunks = [];
        res.on('data', c => chunks.push(c));
        res.on('end', () => resolve(Buffer.concat(chunks)));
        res.on('error', reject);
      }).on('error', reject);
    }
    req(url);
  });
}

async function downloadAll() {
  const realSlides = JSON.parse(fs.readFileSync('data/real_drive_slides.json', 'utf8'));
  const destDir = `${process.env.MEDS_DATABASE_DIR || '/home/indu/Masaüstü/MedSoru Project/meds_database'}/ders_notlari_pdf`;
  if (!fs.existsSync(destDir)) fs.mkdirSync(destDir, { recursive: true });

  console.log(`İndirilecek toplam ders slaytı: ${realSlides.length}`);
  let done = 0;
  for (const s of realSlides) {
    const safeName = s.name.replace(/[\\/:*?"<>|]/g, '_').trim();
    const dest = path.join(destDir, safeName);
    if (fs.existsSync(dest) && fs.statSync(dest).size > 1024) {
      done++;
      console.log(`✓ [Mevcut] ${safeName}`);
      continue;
    }
    try {
      console.log(`📥 İndiriliyor: ${safeName} (${s.folderName})...`);
      const buf = await downloadDriveBuffer(s.id);
      fs.writeFileSync(dest, buf);
      done++;
      console.log(`   ✓ Kaydedildi: ${safeName} (${(buf.length / (1024 * 1024)).toFixed(2)} MB)`);
    } catch (e) {
      console.warn(`   ⚠️ İndirilemedi (${safeName}):`, e.message);
    }
  }
  console.log(`\n🎉 Tüm Ders Slaytları İndirildi: ${done} / ${realSlides.length}`);
}

downloadAll().catch(console.error);
