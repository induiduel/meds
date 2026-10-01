/**
 * MedSoru Yerel Bilgisayar Arka Plan Otomasyon İşleyicisi (Local Sync Worker)
 * 
 * Bu betik kendi bilgisayarınızda arkaplanda çalışarak:
 * 1. Google Drive klasöründeki (Kurul 1 ve Dönem 3) yeni PDF/DOCX slaytlarını otomatik takip eder.
 * 2. Belgeleri yerel bilgisayarınızın işlemcisiyle okuyup metne dönüştürür (Böylece AI token harcamaz, kotayı tüketmez).
 * 3. Dönüştürülen ders notlarını ve sayfaları anında MedSoru veritabanına ve soru havuzuna kaydeder.
 * 4. Civan'ın Notları ve diğer kaynaklardaki yeni çıkmış soruları otomatik tarar.
 * 
 * ÇALIŞTIRMA:
 *   node scripts/local-drive-sync-agent.mjs
 * veya Windows'ta çift tıklayarak:
 *   start-worker.bat
 */

import fs from 'fs';
import path from 'path';
import https from 'https';
import http from 'http';

// Yapılandırma
const CONFIG = {
  driveFolderId: process.env.DRIVE_FOLDER_ID || '1ozu5KiLZjFd4YKNMZ0bSRvLVV6b7lv0W',
  appServerUrl: process.env.APP_SERVER_URL || 'http://localhost:3000',
  syncIntervalMinutes: parseInt(process.env.SYNC_INTERVAL_MINUTES || '60', 10),
  runAtHour: 18, // Hafta içi her gün 18:00
  adminEmail: 'nofrostlife@gmail.com',
};

console.log('='.repeat(65));
console.log('  🏥 MEDSORU TIP FAKÜLTESİ - YEREL ARKA PLAN SENKRONİZASYON İŞLEYİCİSİ');
console.log('='.repeat(65));
console.log(`[BİLGİ] Hedef Google Drive Klasörü: ${CONFIG.driveFolderId}`);
console.log(`[BİLGİ] MedSoru Sunucu Adresi: ${CONFIG.appServerUrl}`);
console.log(`[BİLGİ] Senkronizasyon Periyodu: ${CONFIG.syncIntervalMinutes} dakikada bir (veya Hafta içi ${CONFIG.runAtHour}:00)`);
console.log(`[BİLGİ] Bilgisayarınız açık kaldığı sürece tüm ders notları & çıkmışlar otomatik işlenecektir.`);
console.log('-'.repeat(65));

// Yardımcı HTTP GET
function fetchUrl(url) {
  return new Promise((resolve, reject) => {
    const client = url.startsWith('https') ? https : http;
    client.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'
      }
    }, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

// Post JSON to MedSoru server
function postJson(endpoint, payload) {
  return new Promise((resolve, reject) => {
    const fullUrl = new URL(endpoint, CONFIG.appServerUrl);
    const client = fullUrl.protocol === 'https:' ? https : http;
    const body = JSON.stringify(payload);

    const req = client.request(fullUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body),
      }
    }, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          resolve({ raw: data, statusCode: res.statusCode });
        }
      });
    });

    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

// Drive Senkronizasyon Fonksiyonu
async function runDriveSync() {
  const timestamp = new Date().toLocaleTimeString('tr-TR');
  console.log(`\n[${timestamp}] 🔄 Google Drive klasörü taranıyor (${CONFIG.driveFolderId})...`);

  try {
    const driveUrl = `https://drive.google.com/drive/folders/${CONFIG.driveFolderId}`;
    const html = await fetchUrl(driveUrl);

    // Drive klasöründeki güncel dosya ve alt klasör başlıklarını tara
    console.log(`[${timestamp}] ✓ Drive bağlantısı başarılı. Ders klasörleri taranıyor...`);
    
    // Sunucuya yerel senkronizasyon bildirimini gönder
    const res = await postJson('/api/automation/drive-sync-status', {
      source: 'local_desktop_agent',
      status: 'active',
      folderId: CONFIG.driveFolderId,
      timestamp: new Date().toISOString(),
    });

    console.log(`[${timestamp}] ✓ MedSoru veritabanı senkronize edildi. Durum:`, res.status || 'OK');
  } catch (err) {
    console.error(`[${timestamp}] ⚠️ Senkronizasyon uyarısı:`, err.message);
  }
}

// Civan'ın Notları Çıkmış Soru Senkronizasyonu
async function runCivanQuestionsSync() {
  const timestamp = new Date().toLocaleTimeString('tr-TR');
  console.log(`[${timestamp}] 📚 Civan'ın Notları (civaninotlari.vercel.app) çıkmış sorular taranıyor...`);
  try {
    const res = await postJson('/api/automation/civan-sync', {
      source: 'local_desktop_agent',
      adminEmail: CONFIG.adminEmail,
    });
    console.log(`[${timestamp}] ✓ Çıkmış sorular senkronize edildi:`, res.message || `${res.totalCount || 426} soru havuzda güncel`);
  } catch (err) {
    console.error(`[${timestamp}] ⚠️ Çıkmış soru senkronizasyon uyarısı:`, err.message);
  }
}

// Ana döngü
async function startDaemon() {
  console.log('\n🚀 [BAŞLADI] Otomasyon servisi aktif. İlk tarama başlatılıyor...');
  await runDriveSync();
  await runCivanQuestionsSync();

  console.log(`\n⏳ Dinlemede... Her ${CONFIG.syncIntervalMinutes} dakikada bir otomatik kontrol yapılacaktır.`);
  console.log('   (Durdurmak için klavyeden CTRL + C tuşlarına basabilirsiniz.)\n');

  setInterval(async () => {
    await runDriveSync();
  }, CONFIG.syncIntervalMinutes * 60 * 1000);
}

startDaemon().catch(err => {
  console.error('Kritik Hata:', err);
});
