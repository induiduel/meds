#!/usr/bin/env node
import { spawnSync } from 'child_process';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, '..');

// Parametreleri ayrıştır
const args = process.argv.slice(2);
const isOnce = args.includes('--once');
let intervalMinutes = 20;

for (const arg of args) {
  if (arg.startsWith('--interval=')) {
    const val = parseInt(arg.split('=')[1], 10);
    if (!isNaN(val) && val > 0) intervalMinutes = val;
  }
}

// Git binary yolunu güvenli şekilde tespit et
function findGitExecutable() {
  const possiblePaths = [
    'git',
    'C:\\Program Files\\Git\\cmd\\git.exe',
    'C:\\Program Files\\Git\\bin\\git.exe',
    path.join(process.env.LOCALAPPDATA || '', 'Programs\\Git\\cmd\\git.exe')
  ];

  for (const gitPath of possiblePaths) {
    try {
      const res = spawnSync(gitPath, ['--version'], { encoding: 'utf-8', stdio: 'pipe' });
      if (res.status === 0) {
        return gitPath;
      }
    } catch {
      // devam et
    }
  }
  return 'git';
}

const GIT_EXE = findGitExecutable();

function runGit(gitArgs, options = {}) {
  const res = spawnSync(GIT_EXE, gitArgs, {
    cwd: projectRoot,
    encoding: 'utf-8',
    ...options
  });
  return res;
}

function getTimestamp() {
  const now = new Date();
  const pad = (n) => String(n).padStart(2, '0');
  const yyyy = now.getFullYear();
  const mm = pad(now.getMonth() + 1);
  const dd = pad(now.getDate());
  const hh = pad(now.getHours());
  const min = pad(now.getMinutes());
  const ss = pad(now.getSeconds());
  return `${yyyy}-${mm}-${dd} ${hh}:${min}:${ss}`;
}

function getCurrentBranch() {
  const res = runGit(['rev-parse', '--abbrev-ref', 'HEAD']);
  if (res.status === 0 && res.stdout) {
    return res.stdout.trim();
  }
  return 'main';
}

function syncGitChanges() {
  const timestamp = getTimestamp();
  console.log(`\n---------------------------------------------------------`);
  console.log(`⏱️  [${timestamp}] Dosya değişiklikleri kontrol ediliyor...`);

  // 1. Değişiklik durumunu kontrol et
  const statusRes = runGit(['status', '--porcelain']);
  if (statusRes.status !== 0) {
    console.error(`❌ [${timestamp}] 'git status' çalıştırılamadı:`, statusRes.stderr);
    return false;
  }

  const rawChanges = statusRes.stdout.trim();
  if (!rawChanges) {
    console.log(`ℹ️  [${timestamp}] Herhangi bir dosya değişikliği tespit edilmedi.`);
    console.log(`😴 GitHub'a işlem yapılmadı (boş commit/push engellendi).`);
    return true;
  }

  // Değişen dosya detayları
  const lines = rawChanges.split('\n').map(l => l.trim()).filter(Boolean);
  console.log(`📝 [${timestamp}] ${lines.length} adet dosya değişikliği tespit edildi:`);
  lines.slice(0, 8).forEach(line => console.log(`   • ${line}`));
  if (lines.length > 8) {
    console.log(`   ... ve ${lines.length - 8} dosya daha`);
  }

  // 2. git add -A
  console.log(`➕ [${timestamp}] Dosyalar sahneleniyor (git add -A)...`);
  const addRes = runGit(['add', '-A']);
  if (addRes.status !== 0) {
    console.error(`❌ [${timestamp}] 'git add' hatası:`, addRes.stderr);
    return false;
  }

  // 3. git commit
  const commitMsg = `auto: sync changes [${timestamp}] (${lines.length} dosya güncellendi)`;
  console.log(`💾 [${timestamp}] Commit oluşturuluyor: "${commitMsg}"...`);
  const commitRes = runGit(['commit', '-m', commitMsg]);
  if (commitRes.status !== 0) {
    console.error(`❌ [${timestamp}] 'git commit' hatası:`, commitRes.stderr);
    return false;
  }

  // 4. Mevcut branch tespiti
  const branch = getCurrentBranch();

  // 5. Olası çakışmaları önlemek için git pull --rebase
  console.log(`🔄 [${timestamp}] Uzak depo kontrol ediliyor (git pull --rebase origin ${branch})...`);
  const pullRes = runGit(['pull', '--rebase', 'origin', branch]);
  if (pullRes.status !== 0) {
    console.warn(`⚠️ [${timestamp}] 'git pull --rebase' uyarısı (offline olabilir veya rebase gerekmiyor):`, pullRes.stderr || pullRes.stdout);
  }

  // 6. git push
  console.log(`🚀 [${timestamp}] GitHub'a aktarılıyor (git push origin ${branch})...`);
  const pushRes = runGit(['push', 'origin', branch]);
  if (pushRes.status !== 0) {
    console.error(`❌ [${timestamp}] 'git push' hatası:`, pushRes.stderr);
    console.warn(`⚠️ Değişiklikler yerel olarak commitlendi ancak GitHub'a pushlanamadı. Bir sonraki döngüde tekrar denenecek.`);
    return false;
  }

  console.log(`🎉 [${timestamp}] Başarıyla GitHub'a aktarıldı! (Branch: ${branch})`);
  return true;
}

// Ana çalışma döngüsü
console.log(`=========================================================`);
console.log(`🩺 MedSoru - Otomatik Git Senkronizasyon Servisi`);
console.log(`📂 İzlenen Dizin: ${projectRoot}`);
console.log(`⚙️  Git Binary   : ${GIT_EXE}`);
console.log(`⏰ Kontrol Süresi: Her ${intervalMinutes} dakikada bir`);
console.log(`=========================================================`);

if (isOnce) {
  syncGitChanges();
  process.exit(0);
} else {
  // İlk kontrolü hemen yap
  syncGitChanges();

  const intervalMs = intervalMinutes * 60 * 1000;
  console.log(`\n⏳ Bir sonraki kontrol ${intervalMinutes} dakika sonra yapılacak...`);

  setInterval(() => {
    try {
      syncGitChanges();
    } catch (err) {
      console.error(`❌ Beklenmeyen hata:`, err);
    }
    console.log(`\n⏳ Bir sonraki kontrol ${intervalMinutes} dakika sonra yapılacak...`);
  }, intervalMs);
}
