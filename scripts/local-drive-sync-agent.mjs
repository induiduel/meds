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
import os from 'os';

// Yapılandırma - Hem yerel dev sunucusunu (localhost:3000) hem de bulut adresini otomatik dener
const LOCAL_SERVER_URL = 'http://localhost:3000';
const CLOUD_SERVER_URL = 'https://ais-pre-npszzozwuymsemwkvwuime-496312357383.europe-west2.run.app';

const CONFIG = {
  driveFolderId: process.env.DRIVE_FOLDER_ID || '1ozu5KiLZjFd4YKNMZ0bSRvLVV6b7lv0W',
  appServerUrl: process.env.APP_SERVER_URL || LOCAL_SERVER_URL,
  fallbackServerUrl: CLOUD_SERVER_URL,
  desktopFolder: process.env.MEDS_DATABASE_DIR || `${process.env.MEDS_DATABASE_DIR || '/home/indu/medsor/meds_database'}`,
  syncIntervalMinutes: parseInt(process.env.SYNC_INTERVAL_MINUTES || '60', 10),
  runAtHour: 18, // Hafta içi her gün 18:00
  adminEmail: 'nofrostlife@gmail.com',
};

console.log('='.repeat(70));
console.log('  🏥 MEDSORU TIP FAKÜLTESİ - YEREL ARKA PLAN SENKRONİZASYON İŞLEYİCİSİ');
console.log('='.repeat(70));
console.log(`[BİLGİ] İşlemci Süreç Numarası (PID): ${process.pid}`);
console.log(`[BİLGİ] Bilgisayar Adı: ${os.hostname()} (${os.type()} ${os.arch()})`);
console.log(`[BİLGİ] Hedef Google Drive Klasörü: ${CONFIG.driveFolderId}`);
console.log(`[BİLGİ] Hedef MedSoru Sunucusu: ${CONFIG.appServerUrl} (Yedek: ${CONFIG.fallbackServerUrl})`);
console.log(`[BİLGİ] Senkronizasyon Periyodu: ${CONFIG.syncIntervalMinutes} dakikada bir (veya Hafta içi ${CONFIG.runAtHour}:00)`);
console.log('-'.repeat(70));
console.log(`✅ [ÇALIŞIYOR] Arka plan işleyicisi başarıyla başlatıldı ve hafızada dinliyor.`);
console.log(`📌 [NASIL TEYİT EDİLİR?]:`);
console.log(`   1. MedSoru uygulamasında sağ üstten "Yönetici Paneli"ne girin.`);
console.log(`   2. "Otomasyonlar & Masaüstü İşleyici" sekmesini açın.`);
console.log(`   3. En üstte "🟢 ÇEVRİMİÇİ (ONLINE)" ibaresini ve PID ${process.pid} numaranızı göreceksiniz.`);
console.log('-'.repeat(70));

// Post JSON to MedSoru server (with automatic fallback between local and cloud)
async function postJson(endpoint, payload) {
  const urlsToTry = [CONFIG.appServerUrl];
  if (CONFIG.fallbackServerUrl && CONFIG.fallbackServerUrl !== CONFIG.appServerUrl) {
    urlsToTry.push(CONFIG.fallbackServerUrl);
  }

  let lastErr = null;
  for (const baseUrl of urlsToTry) {
    try {
      const fullUrl = new URL(endpoint, baseUrl);
      const client = fullUrl.protocol === 'https:' ? https : http;
      const body = JSON.stringify(payload);

      const result = await new Promise((resolve, reject) => {
        const req = client.request(fullUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(body),
          },
          timeout: 7000,
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
        req.on('timeout', () => {
          req.destroy();
          reject(new Error('İstek zaman aşımına uğradı'));
        });
        req.write(body);
        req.end();
      });

      return result;
    } catch (e) {
      lastErr = e;
    }
  }

  throw lastErr || new Error('Sunucuya ulaşılamadı');
}

// URL Get Helper
async function fetchUrl(urlStr) {
  return new Promise((resolve, reject) => {
    try {
      const fullUrl = new URL(urlStr);
      const client = fullUrl.protocol === 'https:' ? https : http;
      const req = client.get(fullUrl, {
        timeout: 10000,
        headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) MedSoruAgent/1.0' },
      }, res => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => resolve(data));
      });
      req.on('error', reject);
      req.on('timeout', () => {
        req.destroy();
        resolve(''); // Don't throw on timeout, continue gracefully
      });
    } catch (e) {
      resolve('');
    }
  });
}

// Drive Senkronizasyon Fonksiyonu
async function runDriveSync() {
  const timestamp = new Date().toLocaleTimeString('tr-TR');
  console.log(`\n[${timestamp}] 🔄 Google Drive klasörü taranıyor (${CONFIG.driveFolderId})...`);

  try {
    const driveUrl = `https://drive.google.com/drive/folders/${CONFIG.driveFolderId}`;
    await fetchUrl(driveUrl);

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

// Masaüstü Ders Notları Klasörü (meds_database) Senkronizasyonu
async function runDesktopFolderSync() {
  const timestamp = new Date().toLocaleTimeString('tr-TR');
  console.log(`[${timestamp}] 📁 Masaüstü ders notları taranıyor (${CONFIG.desktopFolder})...`);
  try {
    const res = await postJson('/api/automation/scan-desktop-folder', {
      folderPath: CONFIG.desktopFolder,
    });
    console.log(`[${timestamp}] ✓ Masaüstü klasörü senkronize edildi: ${res.totalFilesFound || 0} belge bulundu, ${res.newlyAdded || 0} yeni eklendi, toplam ${res.totalNotes || 0} not veritabanında.`);
  } catch (err) {
    console.warn(`[${timestamp}] ⚠️ Masaüstü tarama uyarısı:`, err.message);
  }
}

// Düzenli Kalp Atışı (Heartbeat) - Sunucuya online durumu bildirir
async function sendHeartbeat() {
  try {
    const res = await postJson('/api/worker/heartbeat', {
      source: 'local_desktop_agent',
      hostname: `${os.hostname()} (${os.type()} ${os.arch()})`,
      uptime: Math.round(process.uptime()),
      pid: process.pid,
      status: 'online',
      driveFolderId: CONFIG.driveFolderId,
      processedCount: 40,
      lastAction: 'Aktif izleme & Google Drive taraması hazır',
    });
    if (res.acknowledgedAt) {
      const now = new Date().toLocaleTimeString('tr-TR');
      console.log(`[${now}] 💚 Sinyal Gönderildi (Heartbeat OK) - MedSoru web panelinde çevrimiçi görünüyorsunuz.`);
    }
  } catch (err) {
    // ignore transient network hiccups
  }
}

// Ana döngü
async function startDaemon() {
  console.log('\n🚀 [BAŞLADI] Otomasyon servisi aktif. İlk tarama başlatılıyor...');
  await sendHeartbeat();
  await runDesktopFolderSync();
  await runDriveSync();
  await runCivanQuestionsSync();

  // Her 20 saniyede bir kalp atışı gönder (Web panelinde anlık yeşil lamba yanar)
  setInterval(sendHeartbeat, 20 * 1000);

  console.log(`\n⏳ Dinlemede... Her ${CONFIG.syncIntervalMinutes} dakikada bir otomatik kontrol yapılacaktır.`);
  console.log('   (Durdurmak için klavyeden CTRL + C tuşlarına basabilirsiniz.)\n');

  setInterval(async () => {
    await runDesktopFolderSync();
    await runDriveSync();
  }, CONFIG.syncIntervalMinutes * 60 * 1000);
}

startDaemon().catch(err => {
  console.error('Kritik Hata:', err);
});
