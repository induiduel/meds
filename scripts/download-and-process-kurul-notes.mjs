/**
 * scripts/download-and-process-kurul-notes.mjs
 * 
 * Google Drive'daki Kurul 1 - Kurul 6 tüm amfi ders notlarını:
 * 1. C:\Users\indui\Desktop\meds_database\kurul_ders_notlari\Kurul 1 .. 6 klasörlerine indirir.
 * 2. PDF, PPTX ve DOCX formatlarını saf metin olarak ayrıştırıp
 *    C:\Users\indui\Desktop\meds_database\kurul_ders_notlari_txt\Kurul 1 .. 6 klasörlerine .txt olarak kaydeder.
 * 3. Ayrıştırılan ders notlarını Firebase Firestore 'lecture_notes' koleksiyonuna ve data/lecture_notes.json'a aktarır.
 * 4. AI Redaksiyon subagent'ı için 6 kurulun tüm amfi müfredatını eksiksiz hazır hale getirir.
 */

import fs from 'fs';
import path from 'path';
import https from 'https';
import JSZip from 'jszip';
import mammoth from 'mammoth';
import { PDFParse } from 'pdf-parse';
import { initializeApp } from 'firebase/app';
import { getFirestore, doc, setDoc, writeBatch } from 'firebase/firestore';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');

const BASE_DB_DIR = 'C:\\Users\\indui\\Desktop\\meds_database';
const DOWNLOAD_BASE = path.join(BASE_DB_DIR, 'kurul_ders_notlari');
const TXT_BASE = path.join(BASE_DB_DIR, 'kurul_ders_notlari_txt');

const KURULS = [
  { name: 'Kurul 1', committeeId: 'donem3-kurul1', id: '1P4BQ83PsKezAkSyuDFmqPklD3djjrCxA' },
  { name: 'Kurul 2', committeeId: 'donem3-kurul2', id: '1SkXx2eRvojlPMkIawwFkFr9M_p7lcx_1' },
  { name: 'Kurul 3', committeeId: 'donem3-kurul3', id: '14kdfK-kz_Tt3A_SAWCXJD1TzOIjmUBv8' },
  { name: 'Kurul 4', committeeId: 'donem3-kurul4', id: '1F8BeGfX9WpK2xYOZaL6vPRFp_TqxKZUN' },
  { name: 'Kurul 5', committeeId: 'donem3-kurul5', id: '1FlVTQMgrLHTA3F_nwsY4eqHVZWb2Np8N' },
  { name: 'Kurul 6', committeeId: 'donem3-kurul6', id: '1ZQD6AIAf_CV3P5X3ColZw9kAnzgixI2k' }
];

// Firebase Başlatma
const cfg = JSON.parse(fs.readFileSync(path.join(ROOT_DIR, 'firebase-applet-config.json'), 'utf8'));
const app = initializeApp(cfg);
const db = cfg.firestoreDatabaseId ? getFirestore(app, cfg.firestoreDatabaseId) : getFirestore(app);

function cleanForFirestore(obj) {
  if (obj === null || obj === undefined) return null;
  if (Array.isArray(obj)) return obj.map(cleanForFirestore).filter(v => v !== undefined);
  if (typeof obj === 'object') {
    const res = {};
    for (const [k, v] of Object.entries(obj)) {
      if (v !== undefined) {
        res[k] = cleanForFirestore(v);
      }
    }
    return res;
  }
  return obj;
}

function sanitizeFileName(name) {
  return name.replace(/[\\/:*?"<>|]/g, '_').replace(/\s+/g, ' ').trim();
}

// Drive Klasörünü Recursive Tarama
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

// Drive Dosyası İndirme
function downloadDriveFile(fileId, destPath) {
  return new Promise((resolve, reject) => {
    if (fs.existsSync(destPath) && fs.statSync(destPath).size > 1024) {
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

// Metin Çıkarma Motorları
async function extractTextFromPdf(filePath) {
  const dataBuffer = fs.readFileSync(filePath);
  const parser = new PDFParse({ data: dataBuffer });
  const textRes = await parser.getText();
  const pages = (textRes.pages || []).map((p, idx) => ({
    pageNumber: idx + 1,
    content: (p?.text || '').trim(),
    keywords: extractKeywords(p?.text || '')
  }));
  return {
    totalPages: pages.length,
    pages,
    fullText: pages.map(p => `--- [SAYFA ${p.pageNumber}] ---\n${p.content}`).join('\n\n')
  };
}

async function extractTextFromPptx(filePath) {
  const data = fs.readFileSync(filePath);
  const zip = await JSZip.loadAsync(data);
  const slideFiles = Object.keys(zip.files).filter(f => f.startsWith('ppt/slides/slide') && f.endsWith('.xml'));
  slideFiles.sort((a, b) => {
    const numA = parseInt(a.replace(/[^0-9]/g, ''), 10);
    const numB = parseInt(b.replace(/[^0-9]/g, ''), 10);
    return numA - numB;
  });

  const pages = [];
  for (let idx = 0; idx < slideFiles.length; idx++) {
    const sf = slideFiles[idx];
    const xml = await zip.files[sf].async('text');
    const texts = (xml.match(/<a:t[^>]*>(.*?)<\/a:t>/g) || []).map(t => t.replace(/<[^>]+>/g, '').trim()).filter(Boolean);
    const content = texts.join(' ');
    pages.push({
      pageNumber: idx + 1,
      content,
      keywords: extractKeywords(content)
    });
  }

  return {
    totalPages: pages.length,
    pages,
    fullText: pages.map(p => `--- [SLAYT ${p.pageNumber}] ---\n${p.content}`).join('\n\n')
  };
}

async function extractTextFromDocx(filePath) {
  const result = await mammoth.extractRawText({ path: filePath });
  const content = result.value || '';
  const pages = [{
    pageNumber: 1,
    content,
    keywords: extractKeywords(content)
  }];
  return {
    totalPages: 1,
    pages,
    fullText: content
  };
}

function extractKeywords(text) {
  return Array.from(new Set(
    (text.toLowerCase().match(/\b[a-zçğıöşü]{5,20}\b/g) || [])
      .filter(w => !['bunun', 'kadar', 'olarak', 'neden', 'hangisi', 'ancak', 'ayrıca', 'genel', 'sayfa', 'dönem'].includes(w))
  )).slice(0, 15);
}

// Disiplin Tespiti (Klasör adından)
function detectDisciplineFromPath(fullPath) {
  const clean = fullPath.toLowerCase();
  if (clean.includes('patoloji')) return 'Tıbbi Patoloji';
  if (clean.includes('farma')) return 'Tıbbi Farmakoloji';
  if (clean.includes('genetik') || clean.includes('tbg')) return 'Tıbbi Genetik';
  if (clean.includes('enfeksiyon') || clean.includes('mikro')) return 'Enfeksiyon Hastalıkları';
  if (clean.includes('üroloji') || clean.includes('uroloji')) return 'Üroloji';
  if (clean.includes('halk')) return 'Halk Sağlığı';
  if (clean.includes('kadın') || clean.includes('doğum')) return 'Kadın Hastalıkları ve Doğum';
  if (clean.includes('nöro') || clean.includes('noro')) return 'Nöroloji';
  if (clean.includes('psikiyatri')) return 'Psikiyatri';
  if (clean.includes('aile')) return 'Aile Hekimliği';
  if (clean.includes('kardiyo')) return 'Kardiyoloji';
  if (clean.includes('göğüs')) return 'Göğüs Hastalıkları';
  if (clean.includes('ortopedi')) return 'Ortopedi ve Travmatoloji';
  if (clean.includes('acil')) return 'Acil Tıp';
  if (clean.includes('ftr')) return 'FTR';
  if (clean.includes('dahiliye') || clean.includes('iç hast')) return 'İç Hastalıkları';
  if (clean.includes('çocuk') || clean.includes('pediatri')) return 'Çocuk Sağlığı ve Hastalıkları';
  if (clean.includes('biyokimya')) return 'Tıbbi Biyokimya';
  return 'Tıbbi Patoloji';
}

async function main() {
  console.log('='.repeat(75));
  console.log('📚 KURUL 1 - 6 TÜM DERS NOTLARI İNDİRME VE TXT DÖNÜŞTÜRÜCÜ');
  console.log('='.repeat(75));

  const allRenderedNotes = [];

  for (const kurul of KURULS) {
    console.log(`\n===========================================================================`);
    console.log(`🔍 [${kurul.name}] Taranıyor (Folder ID: ${kurul.id})...`);
    console.log(`===========================================================================`);

    const kurulDownloadDir = path.join(DOWNLOAD_BASE, kurul.name);
    const kurulTxtDir = path.join(TXT_BASE, kurul.name);
    if (!fs.existsSync(kurulDownloadDir)) fs.mkdirSync(kurulDownloadDir, { recursive: true });
    if (!fs.existsSync(kurulTxtDir)) fs.mkdirSync(kurulTxtDir, { recursive: true });

    const files = await crawlDriveFolder(kurul.id);
    console.log(`   📂 ${files.length} dosya tespit edildi.`);

    let kurulSuccessCount = 0;

    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const safeName = sanitizeFileName(file.name);
      const ext = path.extname(safeName).toLowerCase();
      
      // Yalnızca doküman ve slayt formatlarını işle
      if (!['.pdf', '.pptx', '.ppt', '.docx', '.doc'].includes(ext)) {
        continue;
      }

      const destFile = path.join(kurulDownloadDir, safeName);
      const destTxt = path.join(kurulTxtDir, `${path.parse(safeName).name}.txt`);

      console.log(`\n[${i + 1}/${files.length}] ${file.name}`);

      // 1. İndir
      try {
        const dlRes = await downloadDriveFile(file.id, destFile);
        if (dlRes.skipped) {
          console.log(`   ⚡ Zaten mevcut: ${safeName} (${Math.round(dlRes.size / 1024)} KB)`);
        } else {
          console.log(`   ⬇️ İndirildi: ${safeName} (${Math.round(dlRes.size / 1024)} KB)`);
        }
      } catch (dlErr) {
        console.warn(`   ⚠️ İndirme hatası: ${dlErr.message}`);
        continue;
      }

      // 2. Metne Dönüştür
      let extracted = { totalPages: 0, pages: [], fullText: '' };
      try {
        if (ext === '.pdf') {
          extracted = await extractTextFromPdf(destFile);
        } else if (ext === '.pptx') {
          extracted = await extractTextFromPptx(destFile);
        } else if (ext === '.docx') {
          extracted = await extractTextFromDocx(destFile);
        }

        if (extracted.fullText && extracted.fullText.length > 50) {
          fs.writeFileSync(destTxt, extracted.fullText, 'utf8');
          console.log(`   💾 TXT kaydedildi: ${destTxt} (${extracted.totalPages} sayfa/slayt)`);

          const discipline = detectDisciplineFromPath(file.fullPath || file.name);
          const noteObj = {
            id: `knote-${kurul.committeeId}-${file.id.substring(0, 12)}`,
            title: path.parse(safeName).name,
            discipline,
            committeeId: kurul.committeeId,
            driveFileId: file.id,
            totalSlides: extracted.totalPages,
            renderedAt: new Date().toISOString(),
            sourcePath: destFile,
            pages: extracted.pages.map(p => ({
              pageNumber: p.pageNumber,
              content: p.content && p.content.length > 800 ? p.content.substring(0, 800) + '...' : p.content,
              keywords: p.keywords
            })).slice(0, 45) // Firestore 1MB koruması
          };

          allRenderedNotes.push(noteObj);
          kurulSuccessCount++;
        }
      } catch (extErr) {
        console.warn(`   ⚠️ Metin ayrıştırma hatası: ${extErr.message}`);
      }
    }

    console.log(`\n✅ ${kurul.name} tamamlandı: ${kurulSuccessCount} ders notu .txt formatına çevrildi.`);
  }

  console.log(`\n===========================================================================`);
  console.log(`🎉 TOPLAM ${allRenderedNotes.length} ADET DERS NOTU BAŞARIYLA AYRIŞTIRILDI!`);
  console.log(`===========================================================================`);

  // data/lecture_notes.json ve src/data/lecture_notes.json Güncelle
  const localNotesPath = path.join(ROOT_DIR, 'data', 'lecture_notes.json');
  const srcNotesPath = path.join(ROOT_DIR, 'src', 'data', 'lecture_notes.json');

  let existing = [];
  if (fs.existsSync(localNotesPath)) {
    try {
      existing = JSON.parse(fs.readFileSync(localNotesPath, 'utf8'));
    } catch (e) {}
  }

  const notesMap = new Map();
  existing.forEach(n => notesMap.set(n.id || n.title, n));
  allRenderedNotes.forEach(n => notesMap.set(n.id || n.title, n));
  const finalNotes = Array.from(notesMap.values());

  fs.writeFileSync(localNotesPath, JSON.stringify(finalNotes, null, 2), 'utf8');
  fs.writeFileSync(srcNotesPath, JSON.stringify(finalNotes, null, 2), 'utf8');
  console.log(`💾 Toplam Ders Notu Arşivi: ${finalNotes.length} (data ve src JSON dosyaları güncellendi).`);

  // Firebase Firestore Senkronizasyonu
  console.log('\n🌐 [Firebase] Yeni ders notları Firestore "lecture_notes" koleksiyonuna aktarılıyor...');
  let fbCount = 0;
  for (let i = 0; i < allRenderedNotes.length; i += 40) {
    const chunk = allRenderedNotes.slice(i, i + 40);
    const batch = writeBatch(db);
    chunk.forEach(note => {
      const cleanNote = cleanForFirestore(note);
      const docRef = doc(db, 'lecture_notes', note.id);
      batch.set(docRef, cleanNote, { merge: true });
    });
    try {
      await batch.commit();
      fbCount += chunk.length;
      process.stdout.write(`   ✓ ${fbCount}/${allRenderedNotes.length} not Firestore'a aktarıldı...\r`);
    } catch (fbErr) {
      console.warn(`   ⚠️ Firestore batch hatası:`, fbErr.message);
    }
  }

  console.log(`\n🎉 Tüm Kurul 1-6 ders notları başarıyla bilgisayara indirildi, .txt yapıldı ve Firebase'e yüklendi!`);
}

main().catch(console.error);
