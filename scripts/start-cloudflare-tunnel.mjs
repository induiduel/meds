/**
 * scripts/start-cloudflare-tunnel.mjs
 * 
 * MedSoru Sunucusunu (port 3000) ve Cloudflare Quick Tunnel'ı
 * eşzamanlı olarak başlatır. Domain gerektirmeden anında
 * güvenli bir https://*.trycloudflare.com adresi üretir.
 */

import { spawn, execSync } from 'child_process';
import fs from 'fs';
import path from 'path';
import http from 'http';
import { fileURLToPath } from 'url';
import { initializeApp } from 'firebase/app';
import { getFirestore, doc, setDoc } from 'firebase/firestore';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');
const DESKTOP_DIR = path.resolve(process.env.USERPROFILE || process.env.HOME, 'Desktop');

let serverProcess = null;
let tunnelProcess = null;

// Firebase Bağlantısı (Varsa Firestore'a tünel adresini otomatik kaydeder)
const cfgPath = path.join(ROOT_DIR, 'firebase-applet-config.json');
let firestoreDb = null;
if (fs.existsSync(cfgPath)) {
  try {
    const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
    const app = initializeApp(cfg, 'cloudflare-tunnel-worker');
    firestoreDb = cfg.firestoreDatabaseId ? getFirestore(app, cfg.firestoreDatabaseId) : getFirestore(app);
  } catch (e) {
    // Firebase opsiyoneldir, hata vermesine gerek yok
  }
}

// 1. Port 3000 kontrol fonksiyonu
function checkPort3000() {
  return new Promise((resolve) => {
    const req = http.get('http://127.0.0.1:3000/api/health', (res) => {
      resolve(res.statusCode === 200);
    });
    req.on('error', () => resolve(false));
    req.setTimeout(1000, () => {
      req.destroy();
      resolve(false);
    });
  });
}

// 2. Cloudflared ikilisini bul veya indir
function getCloudflaredPath() {
  const localExe = path.join(ROOT_DIR, 'cloudflared.exe');
  if (fs.existsSync(localExe)) {
    return localExe;
  }
  // Sistem PATH'inde var mı kontrol et
  try {
    const whereOut = execSync('where cloudflared', { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }).trim();
    if (whereOut) {
      return 'cloudflared';
    }
  } catch (e) {}

  console.log('⬇️ cloudflared.exe bulunamadı, indiriliyor (yaklaşık 30 MB)...');
  try {
    execSync(`curl.exe -L -o "${localExe}" "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"`, {
      stdio: 'inherit'
    });
    return localExe;
  } catch (err) {
    throw new Error('cloudflared.exe indirilemedi: ' + err.message);
  }
}

async function main() {
  console.log('========================================================');
  console.log('       MEDSORU & CLOUDFLARE QUICK TUNNEL BAŞLATICI      ');
  console.log('========================================================\n');

  // Adım 1: Sunucu Durumu Kontrolü
  const isAlreadyRunning = await checkPort3000();
  if (isAlreadyRunning) {
    console.log('✅ MedSoru sunucusu halihazırda port 3000 üzerinde aktif.');
  } else {
    console.log('🚀 MedSoru sunucusu başlatılıyor (npx tsx server.ts)...');
    serverProcess = spawn('npx', ['tsx', 'server.ts'], {
      cwd: ROOT_DIR,
      shell: true,
      stdio: 'inherit',
    });

    serverProcess.on('exit', (code) => {
      if (code !== 0 && code !== null) {
        console.error(`⚠️ MedSoru sunucusu kapandı (kod: ${code})`);
      }
    });

    // Sunucu ayağa kalkana kadar bekle (maksimum 45 saniye)
    console.log('⏳ Sunucunun hazır olması bekleniyor...');
    let ready = false;
    for (let i = 0; i < 90; i++) {
      await new Promise((r) => setTimeout(r, 500));
      ready = await checkPort3000();
      if (ready) break;
    }

    if (!ready) {
      console.error('❌ Sunucu 45 saniye içinde başlatılamadı!');
      cleanupAndExit(1);
      return;
    }
    console.log('✅ MedSoru sunucusu başarıyla hazırlandı (http://localhost:3000).');
  }

  // Adım 2: Cloudflared Yolunu Al
  const cloudflaredExe = getCloudflaredPath();

  // Adım 3: Cloudflare Quick Tunnel Başlat
  console.log('\n🌐 Cloudflare Quick Tunnel başlatılıyor (Domain gerektirmez)...');
  tunnelProcess = spawn(cloudflaredExe, ['tunnel', '--url', 'http://localhost:3000'], {
    cwd: ROOT_DIR,
    shell: false,
    stdio: ['ignore', 'pipe', 'pipe'],
  });

  let tunnelDetected = false;

  const handleTunnelOutput = async (data) => {
    const text = data.toString();
    process.stdout.write(text);

    if (!tunnelDetected) {
      const match = text.match(/https:\/\/[a-zA-Z0-9-]+\.trycloudflare\.com/);
      if (match && !match[0].includes('api.trycloudflare.com')) {
        tunnelDetected = true;
        const tunnelUrl = match[0];

        console.log('\n' + '='.repeat(70));
        console.log('🎉 TEBRİKLER! CLOUDFLARE QUICK TUNNEL AKTİF EDİLDİ');
        console.log('='.repeat(70));
        console.log(`\n  👉 Dış Dünya (HTTPS) Adresiniz : ${tunnelUrl}`);
        console.log(`  👉 Yerel Makine Adresiniz     : http://localhost:3000\n`);
        console.log('='.repeat(70));
        console.log('💡 Bu adresi tarayıcınızda açabilir veya cep telefonunuzdan');
        console.log('   herhangi bir şifre / port yönlendirme olmadan erişebilirsiniz.');
        console.log('----------------------------------------------------------------------\n');

        // URL'yi yerel dosyaya kaydet
        try {
          const tunnelInfoPath = path.join(ROOT_DIR, 'data', 'active_tunnel.txt');
          fs.writeFileSync(tunnelInfoPath, tunnelUrl, 'utf8');
        } catch (e) {}

        // Masaüstüne doğrudan kısayol (.url) oluştur
        try {
          const desktopUrlPath = path.join(DESKTOP_DIR, 'MedSoru_Tünel_Giriş.url');
          fs.writeFileSync(desktopUrlPath, `[InternetShortcut]\nURL=${tunnelUrl}\n`, 'utf8');
          console.log('📌 Masaüstünüze doğrudan tıklayıp açabileceğiniz "MedSoru_Tünel_Giriş.url" kısayolu eklendi.');
        } catch (e) {}

        // Firestore'a kaydet (GitHub Pages senkronizasyonu için)
        if (firestoreDb) {
          try {
            await setDoc(doc(firestoreDb, 'system_status', 'local_server_config'), {
              isServerRunning: true,
              port: 3000,
              tunnelUrl,
              provider: 'cloudflare_quick_tunnel',
              lastUpdated: new Date().toISOString(),
              status: 'online',
            }, { merge: true });
            console.log('🔥 [Firestore] Tünel adresi senkronize edildi (GitHub Pages üzerinden erişim hazır).');
          } catch (err) {
            // sessizce geç
          }
        }

        console.log('\n[Çıkmak ve tüneli durdurmak için konsolda Ctrl + C tuşlarına basınız]\n');
      }
    }
  };

  tunnelProcess.stdout.on('data', handleTunnelOutput);
  tunnelProcess.stderr.on('data', handleTunnelOutput);

  tunnelProcess.on('exit', (code) => {
    console.log(`\n⚠️ Cloudflare Tunnel durduruldu (kod: ${code})`);
    cleanupAndExit(code || 0);
  });
}

function cleanupAndExit(code = 0) {
  if (tunnelProcess && !tunnelProcess.killed) {
    try {
      if (process.platform === 'win32') {
        execSync(`taskkill /pid ${tunnelProcess.pid} /T /F`, { stdio: 'ignore' });
      } else {
        tunnelProcess.kill('SIGINT');
      }
    } catch (e) {}
  }
  if (serverProcess && !serverProcess.killed) {
    try {
      if (process.platform === 'win32') {
        execSync(`taskkill /pid ${serverProcess.pid} /T /F`, { stdio: 'ignore' });
      } else {
        serverProcess.kill('SIGINT');
      }
    } catch (e) {}
  }
  process.exit(code);
}

process.on('SIGINT', () => {
  console.log('\n🛑 Kapatılıyor...');
  cleanupAndExit(0);
});

process.on('SIGTERM', () => {
  cleanupAndExit(0);
});

main().catch((err) => {
  console.error('Beklenmeyen hata:', err);
  cleanupAndExit(1);
});
