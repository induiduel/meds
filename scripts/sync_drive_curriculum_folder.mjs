/**
 * scripts/sync_drive_curriculum_folder.mjs
 * 
 * Google Drive klasöründeki (1ozu5KiLZjFd4YKNMZ0bSRvLVV6b7lv0W) tüm ders notlarını:
 * 1. C:\Users\indui\Desktop\meds_database\ders_notlari_pdf ve kurul_ders_notlari\Kurul 1'e indirir.
 * 2. PDFParse ile doğrudan ayrıştırıp C:\Users\indui\Desktop\meds_database\ders_notlari_txt ve kurul_ders_notlari_txt'e kaydeder.
 * 3. Redakte özet motorunu (generate_redakte_ozet.py) tetikler.
 * 4. Varsa ses kayıtlarını kontrol eder.
 */

import fs from 'fs';
import path from 'path';
import https from 'https';
import { PDFParse } from 'pdf-parse';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');

const BASE_DB_DIR = 'C:\\Users\\indui\\Desktop\\meds_database';
const DERS_PDF_DIR = path.join(BASE_DB_DIR, 'ders_notlari_pdf');
const DERS_TXT_DIR = path.join(BASE_DB_DIR, 'ders_notlari_txt');
const K1_PDF_DIR = path.join(BASE_DB_DIR, 'kurul_ders_notlari', 'Kurul 1');
const K1_TXT_DIR = path.join(BASE_DB_DIR, 'kurul_ders_notlari_txt', 'Kurul 1');

[DERS_PDF_DIR, DERS_TXT_DIR, K1_PDF_DIR, K1_TXT_DIR].forEach(dir => {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
});

const TARGET_FOLDER_ID = '1ozu5KiLZjFd4YKNMZ0bSRvLVV6b7lv0W';

function sanitizeFileName(name) {
  return name.replace(/[\\/:*?"<>|]/g, '_').replace(/\s+/g, ' ').trim();
}

async function crawlDriveFolder(folderId, pathPrefix = '', visited = new Set()) {
  if (visited.has(folderId)) return [];
  visited.add(folderId);

  const url = `https://drive.google.com/drive/folders/${folderId}`;
  try {
    const res = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
      }
    });

    if (!res.ok) return [];
    const html = await res.text();
    const match = html.match(/window\['_DRIVE_ivd'\]\s*=\s*'([^']+)'/);
    if (!match) return [];

    const unescaped = match[1]
      .replace(/\\\\x([0-9a-fA-F]{2})/g, (_, hex) => String.fromCharCode(parseInt(hex, 16)))
      .replace(/\\x([0-9a-fA-F]{2})/g, (_, hex) => String.fromCharCode(parseInt(hex, 16)));

    const parsed = JSON.parse(unescaped);
    const discovered = [];

    function recurse(val) {
      if (!val) return;
      if (Array.isArray(val)) {
        if (typeof val[0] === 'string' && val[0].length >= 25 && typeof val[2] === 'string' && typeof val[3] === 'string') {
          const id = val[0];
          const name = val[2];
          const mime = val[3];
          const isFolder = mime.includes('folder');
          discovered.push({ id, name, mime, isFolder, parentFolderId: folderId, fullPath: pathPrefix ? `${pathPrefix}/${name}` : name });
        }
        val.forEach(recurse);
      }
    }
    recurse(parsed);

    const unique = [];
    const seen = new Set();
    for (const item of discovered) {
      if (!seen.has(item.id)) {
        seen.add(item.id);
        unique.push(item);
      }
    }

    let allFiles = [];
    for (const item of unique) {
      if (item.isFolder) {
        const subItems = await crawlDriveFolder(item.id, item.fullPath, visited);
        allFiles = allFiles.concat(subItems);
      } else {
        allFiles.push(item);
      }
    }

    return allFiles;
  } catch (err) {
    console.error(`[Crawl Hatası] ${folderId}:`, err.message);
    return [];
  }
}

function downloadDriveFile(fileId, destPath) {
  return new Promise((resolve, reject) => {
    if (fs.existsSync(destPath) && fs.statSync(destPath).size > 2048) {
      return resolve({ skipped: true, size: fs.statSync(destPath).size });
    }

    const initialUrl = `https://drive.usercontent.google.com/download?id=${fileId}&export=download&authuser=0&confirm=t`;

    function makeReq(url, redirectCount = 0) {
      if (redirectCount > 6) return reject(new Error('Çok fazla yönlendirme'));

      https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' } }, (res) => {
        if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
          return makeReq(res.headers.location, redirectCount + 1);
        }
        if (res.statusCode !== 200) {
          return reject(new Error(`HTTP Durumu: ${res.statusCode}`));
        }

        const fileStream = fs.createWriteStream(destPath);
        res.pipe(fileStream);
        fileStream.on('finish', () => {
          fileStream.close();
          const size = fs.existsSync(destPath) ? fs.statSync(destPath).size : 0;
          resolve({ skipped: false, size });
        });
      }).on('error', (err) => {
        if (fs.existsSync(destPath)) fs.unlinkSync(destPath);
        reject(err);
      });
    }

    makeReq(initialUrl);
  });
}

async function extractTextFromPdf(filePath) {
  const dataBuffer = fs.readFileSync(filePath);
  const parser = new PDFParse({ data: dataBuffer });
  const textRes = await parser.getText();
  const pages = (textRes.pages || []).map((p, idx) => ({
    pageNumber: idx + 1,
    content: (p?.text || '').trim(),
  }));
  return {
    totalPages: pages.length,
    fullText: pages.map(p => `--- [SAYFA ${p.pageNumber}] ---\n${p.content}`).join('\n\n')
  };
}

async function syncDriveCurriculum() {
  console.log('=' .repeat(80));
  console.log('🔄 GOOGLE DRIVE DERS NOTLARI SENKRONİZASYON & DENETİM BAŞLATILIYOR');
  console.log(`📁 Hedef Klasör: ${TARGET_FOLDER_ID}`);
  console.log('=' .repeat(80));

  console.log('\n[1/4] Drive klasör ağacı taranıyor...');
  const files = await crawlDriveFolder(TARGET_FOLDER_ID);
  console.log(`✓ Toplam ${files.length} dosya tespit edildi.`);

  const downloadedNew = [];
  const processedTxt = [];

  for (const file of files) {
    const isDoc = file.name.endsWith('.pdf') || file.name.endsWith('.pptx');
    if (!isDoc) continue;

    const safeName = sanitizeFileName(file.name);
    const destPdfPath1 = path.join(DERS_PDF_DIR, safeName);
    const destPdfPath2 = path.join(K1_PDF_DIR, safeName);
    const baseName = safeName.replace(/\.[^/.]+$/, "");
    const destTxtPath1 = path.join(DERS_TXT_DIR, `${baseName}.txt`);
    const destTxtPath2 = path.join(K1_TXT_DIR, `${baseName}.txt`);

    // Check if PDF exists
    const pdfExists = fs.existsSync(destPdfPath1) || fs.existsSync(destPdfPath2);
    const targetPdfPath = fs.existsSync(destPdfPath1) ? destPdfPath1 : destPdfPath2;

    if (!pdfExists) {
      console.log(`📥 İndiriliyor: ${file.name}`);
      try {
        const res = await downloadDriveFile(file.id, destPdfPath1);
        // Also copy to Kurul 1
        fs.copyFileSync(destPdfPath1, destPdfPath2);
        console.log(`   ✓ İndirildi: ${safeName} (${Math.round(res.size / 1024)} KB)`);
        downloadedNew.push(safeName);
      } catch (err) {
        console.error(`   ❌ İndirme hatası (${file.name}):`, err.message);
        continue;
      }
    }

    // Check if TXT exists
    const txtExists = fs.existsSync(destTxtPath1) && fs.existsSync(destTxtPath2);
    if (!txtExists && file.name.endsWith('.pdf')) {
      const srcPdf = fs.existsSync(destPdfPath1) ? destPdfPath1 : destPdfPath2;
      console.log(`⚙️ TXT'ye çevriliyor: ${safeName}`);
      try {
        const extracted = await extractTextFromPdf(srcPdf);
        fs.writeFileSync(destTxtPath1, extracted.fullText, 'utf8');
        fs.writeFileSync(destTxtPath2, extracted.fullText, 'utf8');
        console.log(`   ✓ Metin kaydedildi: ${baseName}.txt (${extracted.totalPages} sayfa)`);
        processedTxt.push(baseName);
      } catch (err) {
        console.error(`   ❌ Metin çıkarma hatası (${safeName}):`, err.message);
      }
    }
  }

  console.log('\n[2/4] İndirme ve TXT Çıkarım Özeti:');
  console.log(` - Yeni indirilen PDF sayısı: ${downloadedNew.length}`);
  console.log(` - Yeni oluşturulan TXT sayısı: ${processedTxt.length}`);

  // Step 3: Trigger Redakte Ozet Generation
  console.log('\n[3/4] Redakte Özet Doğrulaması ve Üretimi (generate_redakte_ozet.py)...');
  const redakteScript = path.join(BASE_DB_DIR, 'generate_redakte_ozet.py');
  if (fs.existsSync(redakteScript)) {
    try {
      execSync(`python "${redakteScript}" --kurul 1`, { stdio: 'inherit', cwd: BASE_DB_DIR });
      console.log('✓ Kurul 1 redakte özetleri güncellendi.');
    } catch (e) {
      console.error('⚠️ Redakte özet üretimi uyarıyla tamamlandı:', e.message);
    }
  }

  // Step 4: Check Audio Recordings
  console.log('\n[4/4] Ses Kayıtları ve Transkripsiyon Kontrolü...');
  const sesDir = path.join(BASE_DB_DIR, 'ses_kayitlari');
  const transDir = path.join(BASE_DB_DIR, 'transcriptions');
  const sesFiles = fs.existsSync(sesDir) ? fs.readdirSync(sesDir) : [];
  const transFiles = fs.existsSync(transDir) ? fs.readdirSync(transDir) : [];
  console.log(` - Mevcut ses kaydı sayısı: ${sesFiles.length}`);
  console.log(` - Mevcut transkripsiyon sayısı: ${transFiles.length}`);

  console.log('\n' + '=' .repeat(80));
  console.log('✅ DRIVE SENKRONİZASYON VE REDAKSİYON KONTROLÜ TAMAMLANDI.');
  console.log('=' .repeat(80));
}

syncDriveCurriculum();
