/**
 * scripts/start-hybrid-tunnel.mjs
 * 
 * Yerel bilgisayarınızdaki MedSoru sunucusunu (port 3000)
 * GitHub Pages (HTTPS) üzerinden güvenle erişilebilir kılmak için
 * ücretsiz bir tünel açar ve adresi doğrudan Firebase Firestore'a kaydeder.
 * 
 * Böylece:
 * 1. Firebase kotanız dolsa bile GitHub Pages üzerinden yerel PC'niz veritabanı olarak kullanılır.
 * 2. Port yönlendirme (port forwarding) yapmanıza gerek kalmaz.
 * 3. Mixed-content (HTTPS -> HTTP) sorunu tamamen ortadan kalkar.
 */

import { spawn } from 'child_process';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { initializeApp } from 'firebase/app';
import { getFirestore, doc, setDoc } from 'firebase/firestore';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');

// 1. Firebase Bağlantısı
const cfgPath = path.join(ROOT_DIR, 'firebase-applet-config.json');
let firestoreDb = null;
// Firebase veritabanı devre dışı (src/services/dbFlags.ts): yalnızca MEDS_FIREBASE_ENABLED=1 ise bağlanılır/yazılır
if (process.env.MEDS_FIREBASE_ENABLED === '1' && fs.existsSync(cfgPath)) {
  try {
    const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
    const app = initializeApp(cfg, 'hybrid-tunnel-worker');
    firestoreDb = cfg.firestoreDatabaseId ? getFirestore(app, cfg.firestoreDatabaseId) : getFirestore(app);
    console.log('🔥 [Hibrit Tünel] Firebase bağlantısı kuruldu.');
  } catch (e) {
    console.warn('⚠️ Firebase bağlantı hatası:', e.message);
  }
}

// 2. Tünel Başlatıcı (localtunnel)
console.log('🚀 [Hibrit Tünel] Port 3000 için ücretsiz güvenli HTTPS tüneli açılıyor...');

const tunnelProcess = spawn('npx', ['--yes', 'localtunnel', '--port', '3000'], {
  shell: true,
  stdio: ['ignore', 'pipe', 'pipe']
});

tunnelProcess.stdout.on('data', async (data) => {
  const output = data.toString();
  console.log(`[Tünel Çıktısı]: ${output.trim()}`);

  const match = output.match(/https:\/\/[a-zA-Z0-9-.]+\.loca\.lt/);
  if (match) {
    const tunnelUrl = match[0];
    console.log(`\n✨ [Tünel Aktif!] Harici Güvenli Adresiniz: ${tunnelUrl}`);

    if (firestoreDb) {
      try {
        await setDoc(doc(firestoreDb, 'system_status', 'local_server_config'), {
          isServerRunning: true,
          port: 3000,
          tunnelUrl,
          lastUpdated: new Date().toISOString(),
          status: 'online'
        }, { merge: true });
        console.log('💾 [Tünel] Adres Firestore "system_status/local_server_config" belgesine kaydedildi!');
        console.log('   GitHub Pages artık bu adres üzerinden yerel veritabanınıza bağlanabilir.');
      } catch (err) {
        console.warn('Firestore kayıt hatası:', err.message);
      }
    }
  }
});

tunnelProcess.stderr.on('data', (data) => {
  console.error(`[Tünel Hatası]: ${data.toString().trim()}`);
});

tunnelProcess.on('close', (code) => {
  console.log(`[Tünel Sonlandı] Çıkış kodu: ${code}`);
});

process.on('SIGINT', () => {
  tunnelProcess.kill();
  process.exit();
});
