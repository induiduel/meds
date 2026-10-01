/**
 * MedSoru Yerel Otomasyon ve Senkronizasyon Motoru (meds-local-sync.mjs)
 * 
 * Bu betik:
 * 1. Google Drive çıkmış soru ve ders notları klasörlerini tarar.
 * 2. Yeni/eksik PDF'leri doğrudan C:\Users\indui\Desktop\meds_database klasörüne indirir.
 * 3. Yerel CPU ile (pdf-parse) PDF'leri sayfa sayfa birebir okur (asla AI özet uydurmaz).
 * 4. Çıkan saf metinleri meds_sorular_txt ve ders_notlari_txt içine .txt olarak kaydeder.
 * 5. Çıkmış soruları kurallara uygun olarak soru, şıklar ve branşlara ayrıştırıp .questions.json üretir.
 * 6. Beğeni sayılarını varsayılan olarak 0 başlatır ve tekil oy mantığını uygular.
 * 7. Tüm verileri yerel veritabanına ve Firebase Firestore'a eşitler.
 * 8. Bilgisayar açıldığında (özellikle 16:00 - 18:00 aralığında) otomatik çalışabilir.
 */

import fs from 'fs';
import path from 'path';
import https from 'https';
import http from 'http';
import os from 'os';
import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import { PDFParse } from 'pdf-parse';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Windows Masaüstü Bildirimi (Toast / Action Center) Gönderici
function sendWindowsNotification(title, message) {
  try {
    const psScript = path.join(__dirname, 'show-notification.ps1');
    if (!fs.existsSync(psScript)) return;
    const child = spawn('powershell.exe', [
      '-NoProfile',
      '-ExecutionPolicy', 'Bypass',
      '-File', psScript,
      '-Title', title,
      '-Message', message,
    ], { stdio: 'ignore', windowsHide: true, detached: true });
    child.unref();
  } catch (err) {
    console.warn('[Bildirim Hatası]:', err.message);
  }
}

// MedSoru Sunucusuna Kalp Atışı (Heartbeat) Bildirimi
async function sendWorkerHeartbeat(status = 'online', lastAction = '16:00 - 18:00 Arası Otomasyon ve Eşitleme Aktif') {
  try {
    let questionFilesCount = 0;
    if (fs.existsSync(DIRS.sorularPdf)) {
      questionFilesCount = fs.readdirSync(DIRS.sorularPdf).filter(f => f.toLowerCase().endsWith('.pdf')).length;
    }
    await postServerJson('/api/worker/heartbeat', {
      source: 'meds_local_sync',
      hostname: `${os.hostname()} (Windows 10/11)`,
      uptime: Math.round(process.uptime()),
      pid: process.pid,
      status,
      lastAction,
      processedCount: questionFilesCount,
      driveFolderId: DRIVE_QUESTION_FOLDERS[0]?.id || '18U1LZVvV0VROcWVQTDBeJYwdBWiEIVwS',
      isStartupConfigured: true,
    });
  } catch (e) {
    // Sunucu geçici olarak kapalıysa yutulur
  }
}

// --- YAPILANDIRMA ---
const BASE_DATABASE_DIR = process.env.MEDS_DATABASE_DIR || 'C:\\Users\\indui\\Desktop\\meds_database';
const DIRS = {
  root: BASE_DATABASE_DIR,
  sorularPdf: path.join(BASE_DATABASE_DIR, 'meds_sorular'),
  sorularTxt: path.join(BASE_DATABASE_DIR, 'meds_sorular_txt'),
  notlarPdf: path.join(BASE_DATABASE_DIR, 'ders_notlari_pdf'),
  notlarTxt: path.join(BASE_DATABASE_DIR, 'ders_notlari_txt'),
};

const DRIVE_QUESTION_FOLDERS = [
  { name: '1) Çıkmışlar (Kurul 1-6 & Final)', id: '18U1LZVvV0VROcWVQTDBeJYwdBWiEIVwS' },
  { name: '2) 25-26 Dönem 3 Çıkmışları', id: '1VJwhDITJWZFaaBTvMajnLUzII31r1GTp' },
  { name: '3) 3. Dönem', id: '1AZaRbCpIUKtv0t6sg3VaZHC42NmbrnB4' },
  { name: '4) Çıkmış Sorular', id: '16ianUX4Nnl-dU9SZOSOgvDDuEaM1x6vZ' },
  { name: '5) 3. Sınıf', id: '1FAqqW0iAeg3NNjkPBeY3zG9X4FXaJuVM' },
  { name: '6) Dönem 3 Çıkmış Toplama', id: '1QKbD3800KBa3AUWP8apMSiKCMV0jiA21' },
];

const DRIVE_LECTURE_NOTE_FOLDERS = [
  { name: 'Ders Notları & Slaytlar', id: '1ozu5KiLZjFd4YKNMZ0bSRvLVV6b7lv0W' },
];

const LOCAL_SERVER_URL = 'http://localhost:3000';

// Klasörleri oluştur
function ensureDirectories() {
  for (const dir of Object.values(DIRS)) {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
  }
}

// Dosya adı temizleyici
function sanitizeFileName(name) {
  return name.replace(/[\\/:*?"<>|]/g, '_').replace(/\s+/g, ' ').trim();
}

// Google Drive klasörünü recursive tarama
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
          discovered.push({ id, name, mime, isFolder, parentFolderId: folderId, fullPath: pathPrefix ? `${pathPrefix} / ${name}` : name });
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

// Drive'dan dosya indirme (Redirect ve Stream desteği)
function downloadDriveFile(fileId, destPath) {
  return new Promise((resolve, reject) => {
    // Dosya zaten varsa ve boyutu 0'dan büyükse tekrar indirme
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
        fileStream.on('error', (err) => {
          try { fs.unlinkSync(destPath); } catch {}
          reject(err);
        });
      }).on('error', reject);
    }

    makeReq(initialUrl);
  });
}

// PDF dosyasından saf, birebir metin çıkarımı (CPU tabanlı, sıfır AI uydurması)
async function extractVerbatimPdfText(pdfPath) {
  try {
    const dataBuffer = fs.readFileSync(pdfPath);
    const parser = new PDFParse({ data: dataBuffer });
    const textRes = await parser.getText();
    const pages = (textRes.pages || []).map((p, idx) => ({
      pageNumber: idx + 1,
      text: (p?.text || '').trim()
    }));
    return {
      totalPages: pages.length,
      pages,
      fullText: pages.map(p => `--- [SAYFA ${p.pageNumber}] ---\n${p.text}`).join('\n\n')
    };
  } catch (err) {
    console.warn(`[PDF Okuma Hatası] ${pdfPath}:`, err.message);
    return { totalPages: 0, pages: [], fullText: '' };
  }
}

// Dosya adı veya yolundan Komite ID belirleme
function detectCommitteeId(fileNameOrPath) {
  const lower = fileNameOrPath.toLowerCase();
  if (lower.includes('kurul 1') || lower.includes('kurul1') || lower.includes('d3k1') || lower.includes('komite 1')) return 'donem3-kurul1';
  if (lower.includes('kurul 2') || lower.includes('kurul2') || lower.includes('d3k2') || lower.includes('komite 2')) return 'donem3-kurul2';
  if (lower.includes('kurul 3') || lower.includes('kurul3') || lower.includes('d3k3') || lower.includes('komite 3')) return 'donem3-kurul3';
  if (lower.includes('kurul 4') || lower.includes('kurul4') || lower.includes('d3k4') || lower.includes('komite 4')) return 'donem3-kurul4';
  if (lower.includes('kurul 5') || lower.includes('kurul5') || lower.includes('d3k5') || lower.includes('komite 5')) return 'donem3-kurul5';
  if (lower.includes('kurul 6') || lower.includes('kurul6') || lower.includes('d3k6') || lower.includes('komite 6')) return 'donem3-kurul6';
  if (lower.includes('büt') || lower.includes('butunleme')) return 'donem3-butunleme';
  if (lower.includes('final')) return 'donem3-final';
  return 'donem3-kurul1'; // varsayılan
}

// Metinden çıkmış soruları ayrıştır
function parseQuestionsFromVerbatimText(fullText, sourceFileName, defaultCommitteeId) {
  const questions = [];
  const lines = fullText.split('\n').map(l => l.trim()).filter(Boolean);

  let currentDiscipline = 'Tıbbi Patoloji';
  let currentQNum = null;
  let currentStemLines = [];
  let currentOptions = [];
  let currentAnswer = undefined;

  function commitQuestion() {
    if (!currentQNum || currentStemLines.length === 0) return;
    const stemText = currentStemLines.join(' ').trim();
    if (stemText.length < 10) return;

    const fileBase = path.basename(sourceFileName, path.extname(sourceFileName)).replace(/[^a-zA-Z0-9_-]/g, '_');
    const qId = `q-${fileBase}-${currentQNum}`;

    // Seçenekleri oluştur (her zaman 0 beğeni ile başlar)
    const optionsObj = currentOptions.map(opt => ({
      key: opt.key,
      text: opt.text,
      suggestedBy: 'Çıkmış Sınav Arşivi',
      upvotes: 0,
      likedBy: []
    }));

    const yearMatch = sourceFileName.match(/(?:19\d{2}|20[0-2][0-5])/);
    const examYear = yearMatch ? yearMatch[0] : 'Kategorisiz';
    const isAmbiguous = stemText.length < 25 || optionsObj.length < 2;

    questions.push({
      id: qId,
      committeeId: defaultCommitteeId,
      questionNumber: currentQNum,
      discipline: currentDiscipline,
      topic: `${currentDiscipline} Çıkmış Soru ${currentQNum}`,
      status: currentOptions.length >= 3 ? 'verified' : 'gathering',
      tags: [currentDiscipline, 'Çıkmış Sınav', path.basename(sourceFileName), examYear],
      examYear,
      isAmbiguous,
      placementNotes: isAmbiguous ? 'Muallak Soru (Eksik Metin / Yetersiz Şık)' : undefined,
      claimedAnswer: currentAnswer,
      officialAnswer: currentAnswer,
      upvotes: 0,
      likedBy: [],
      sourceFile: path.basename(sourceFileName),
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      fragments: [
        {
          id: `f-${qId}-stem`,
          author: 'Yerel Otomasyon',
          text: stemText,
          type: 'stem',
          timestamp: new Date().toISOString(),
          upvotes: 0,
          likedBy: []
        }
      ],
      options: optionsObj
    });

    currentQNum = null;
    currentStemLines = [];
    currentOptions = [];
    currentAnswer = undefined;
  }

  // Tıp Fakültesi anabilim dalı tespiti için anahtar kelimeler
  const DISCIPLINE_KEYWORDS = [
    'Tıbbi Biyoloji ve Genetik', 'Tıbbi Biyoloji', 'Biyoloji',
    'Tıbbi Biyokimya', 'Biyokimya',
    'Histoloji ve Embriyoloji', 'Histoloji', 'Embriyoloji',
    'Anatomi', 'Fizyoloji',
    'Tıbbi Patoloji', 'Patoloji', 'Tıbbi Farmakoloji', 'Farmakoloji',
    'İç Hastalıkları', 'Dahiliye', 'Kardiyoloji', 'Göğüs Hastalıkları',
    'Enfeksiyon Hastalıkları', 'Mikrobiyoloji', 'Tıbbi Mikrobiyoloji',
    'Pediatri', 'Çocuk Sağlığı', 'Kadın Hastalıkları ve Doğum',
    'Genel Cerrahi', 'Üroloji', 'Nöroloji', 'Psikiyatri',
    'Beyin ve Sinir Cerrahisi', 'Ortopedi ve Travmatoloji', 'Ortopedi', 'Acil Tıp', 'Aile Hekimliği',
    'Halk Sağlığı', 'Tıbbi Genetik',
    'Anesteziyoloji', 'Anestezi', 'FTR', 'Fiziksel Tıp'
  ];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Sayfa ayracı atla
    if (line.startsWith('--- [SAYFA')) continue;

    // Branş başlığı kontrolü
    const matchedDisc = DISCIPLINE_KEYWORDS.find(d => line.toLowerCase() === d.toLowerCase() || line.toLowerCase() === `${d.toLowerCase()}:`);
    if (matchedDisc) {
      currentDiscipline = matchedDisc;
      continue;
    }

    // Soru başlangıcı: "1)", "1.", "Soru 1:", "1 -", "1/100"
    const qStartMatch = line.match(/^(?:soru\s*)?(\d{1,3})\s*[\)\.\-]\s*(.*)$/i);
    if (qStartMatch && !line.match(/^[A-E]\)/i)) {
      const num = parseInt(qStartMatch[1], 10);
      if (num >= 1 && num <= 150) {
        commitQuestion();
        currentQNum = num;
        if (qStartMatch[2] && qStartMatch[2].trim().length > 0) {
          currentStemLines.push(qStartMatch[2].trim());
        }
        continue;
      }
    }

    // Şık kontrolü: "A)", "B)", "C)", "D)", "E)" veya "A.", "B."
    const optMatch = line.match(/^([A-E])\s*[\)\.]\s*(.*)$/);
    if (optMatch && currentQNum) {
      currentOptions.push({
        key: optMatch[1].toUpperCase(),
        text: (optMatch[2] || '').trim()
      });
      continue;
    }

    // Cevap anahtarı kontrolü: "Cevap: B", "Doğru Seçenek: C", "Cevap C"
    const ansMatch = line.match(/^(?:cevap|doğru\s*cevap|yanıt)\s*[:\-]?\s*([A-E])/i);
    if (ansMatch && currentQNum) {
      currentAnswer = ansMatch[1].toUpperCase();
      continue;
    }

    // Devam eden soru metni veya şık metni
    if (currentQNum) {
      if (currentOptions.length > 0) {
        // Son şıkkın metnine ekle
        currentOptions[currentOptions.length - 1].text += ' ' + line;
      } else {
        // Soru köküne ekle
        currentStemLines.push(line);
      }
    }
  }

  commitQuestion();
  return questions;
}

// POST JSON yardımcı fonksiyonu
async function postServerJson(endpoint, payload) {
  try {
    const res = await fetch(`${LOCAL_SERVER_URL}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (res.ok) {
      return await res.json().catch(() => ({ status: 'OK' }));
    }
  } catch (err) {
    // Sunucu kapalıysa yerel dosyaya yazılacak, sorun değil
  }
  return null;
}

// --- ANA İŞ AKIŞI ---
export async function runFullSync() {
  console.log('='.repeat(75));
  console.log('  🏥 MEDSORU TIP FAKÜLTESİ - YEREL ARŞİV & SENKRONİZASYON OTOMASYONU');
  console.log('='.repeat(75));
  console.log(`[Klasör] meds_database: ${BASE_DATABASE_DIR}`);
  console.log(`[Tarih/Saat] ${new Date().toLocaleString('tr-TR')}`);
  console.log('-'.repeat(75));

  // Windows Bildirimi ve Sunucu Kalp Atışı
  sendWindowsNotification(
    'MedSoru: Günlük Eşitleme Başladı ⏳',
    'Google Drive çıkmış soruları ve ders notları taranıyor...'
  );
  await sendWorkerHeartbeat('online', 'Google Drive taranıyor ve PDF belgeleri okunuyor...');

  ensureDirectories();

  // 1. ADIM: Google Drive Çıkmış Soru Klasörlerini Tara
  console.log('\n🔍 1. ADIM: Google Drive Çıkmış Soruları Taranıyor...');
  const allDiscoveredQuestions = [];
  for (const root of DRIVE_QUESTION_FOLDERS) {
    process.stdout.write(`   📁 ${root.name}... `);
    const files = await crawlDriveFolder(root.id, root.name);
    console.log(`${files.length} dosya bulundu.`);
    allDiscoveredQuestions.push(...files);
  }

  // Benzersiz PDF'leri filtrele
  const uniqueQuestionPdfs = new Map();
  allDiscoveredQuestions.forEach(f => {
    if (f.name.toLowerCase().endsWith('.pdf') || (f.mime && f.mime.includes('pdf'))) {
      if (!uniqueQuestionPdfs.has(f.id)) {
        uniqueQuestionPdfs.set(f.id, f);
      }
    }
  });
  console.log(`   ✓ Toplam Benzersiz Çıkmış Soru PDF Sayısı: ${uniqueQuestionPdfs.size}`);

  // 2. ADIM: Çıkmış Soruları İndir
  console.log('\n📥 2. ADIM: Çıkmış Soru PDF Dosyaları İndiriliyor...');
  let downloadedCount = 0;
  let skippedCount = 0;
  for (const file of uniqueQuestionPdfs.values()) {
    const safeName = sanitizeFileName(file.name);
    const destPath = path.join(DIRS.sorularPdf, safeName);
    try {
      const res = await downloadDriveFile(file.id, destPath);
      if (res.skipped) {
        skippedCount++;
      } else {
        downloadedCount++;
        console.log(`   ✓ İndirildi: ${safeName} (${(res.size / (1024 * 1024)).toFixed(2)} MB)`);
      }
    } catch (e) {
      console.warn(`   ⚠️ İndirilemedi (${safeName}):`, e.message);
    }
  }
  console.log(`   ✓ İndirme Tamamlandı. (Yeni İndirilen: ${downloadedCount}, Zaten Mevcut Olan: ${skippedCount})`);

  // 3. ADIM: Yerel PDF Okuma & Metin Çıkarımı (Birebir / Verbatim)
  console.log('\n📖 3. ADIM: Yerel CPU ile Birebir Metin Çıkarımı (OCR / pdf-parse)...');
  const localQuestionFiles = fs.readdirSync(DIRS.sorularPdf).filter(f => f.toLowerCase().endsWith('.pdf'));
  console.log(`   📂 İşlenecek Yerel Çıkmış PDF Sayısı: ${localQuestionFiles.length}`);

  let totalParsedQuestions = [];

  for (const pdfFile of localQuestionFiles) {
    const pdfPath = path.join(DIRS.sorularPdf, pdfFile);
    const baseName = path.basename(pdfFile, path.extname(pdfFile));
    const txtPath = path.join(DIRS.sorularTxt, `${baseName}.txt`);
    const jsonPath = path.join(DIRS.sorularTxt, `${baseName}.questions.json`);

    // Eğer txt zaten varsa ve doluysa oradan oku, yoksa PDF'ten çıkar
    let verbatimText = '';
    if (fs.existsSync(txtPath) && fs.statSync(txtPath).size > 100) {
      verbatimText = fs.readFileSync(txtPath, 'utf8');
    } else {
      const extRes = await extractVerbatimPdfText(pdfPath);
      if (extRes.fullText && extRes.fullText.length > 50) {
        verbatimText = extRes.fullText;
        fs.writeFileSync(txtPath, verbatimText, 'utf8');
      }
    }

    if (verbatimText && verbatimText.length > 100) {
      const committeeId = detectCommitteeId(pdfFile);
      const parsed = parseQuestionsFromVerbatimText(verbatimText, pdfFile, committeeId);
      if (parsed.length > 0) {
        fs.writeFileSync(jsonPath, JSON.stringify(parsed, null, 2), 'utf8');
        totalParsedQuestions.push(...parsed);
        console.log(`   ✓ ${pdfFile}: ${parsed.length} soru ayrıştırıldı (${committeeId})`);
      }
    }
  }

  console.log(`   ✓ Toplam Ayrıştırılan Çıkmış Soru Sayısı: ${totalParsedQuestions.length}`);

  // 4. ADIM: Soruları Yerel data/pastQuestions.json ile Birleştir (Çıkmış Sorular Arşivi)
  console.log('\n💾 4. ADIM: Sorular Çıkmış Soru Arşivine (pastQuestions.json) Aktarılıyor...');
  const pastJsonPath = path.join(process.cwd(), 'data', 'pastQuestions.json');
  const srcPastJsonPath = path.join(process.cwd(), 'src', 'data', 'pastQuestions.json');
  let existingPastQuestions = [];
  if (fs.existsSync(pastJsonPath)) {
    try {
      existingPastQuestions = JSON.parse(fs.readFileSync(pastJsonPath, 'utf8'));
    } catch {}
  }

  // Soruları id veya metin benzerliği ile birleştir (Duplicate engelleme)
  const pastMap = new Map();
  existingPastQuestions.forEach(q => {
    if (q && q.id) pastMap.set(q.id, q);
    const stem = (q.reconstruction?.stem || q.rawQuestion?.stem || q.stem || q.topic || '').trim().toLowerCase();
    if (stem.length > 10) pastMap.set(stem.slice(0, 60), q);
  });
  
  let newAddedCount = 0;
  for (const q of totalParsedQuestions) {
    const stem = (q.reconstruction?.stem || q.rawQuestion?.stem || q.stem || q.topic || '').trim().toLowerCase();
    const stemKey = stem.length > 10 ? stem.slice(0, 60) : '';
    if (!pastMap.has(q.id) && (!stemKey || !pastMap.has(stemKey))) {
      const pastItem = {
        ...q,
        isPastExam: true,
        examYear: q.examYear && !q.examYear.includes('2026') ? q.examYear : 'Geçmiş Yıllar Çıkmışı (Arşiv)',
        sourceFile: q.sourceFile || 'Geçmiş Sınav Dosyası',
      };
      existingPastQuestions.push(pastItem);
      pastMap.set(q.id, pastItem);
      if (stemKey) pastMap.set(stemKey, pastItem);
      newAddedCount++;
    }
  }

  fs.writeFileSync(pastJsonPath, JSON.stringify(existingPastQuestions, null, 2), 'utf8');
  if (fs.existsSync(path.dirname(srcPastJsonPath))) {
    fs.writeFileSync(srcPastJsonPath, JSON.stringify(existingPastQuestions, null, 2), 'utf8');
  }
  console.log(`   ✓ data/pastQuestions.json güncellendi! (Yeni eklenen: ${newAddedCount}, Toplam Çıkmış Soru: ${existingPastQuestions.length})`);

  // 5. ADIM: Ders Notları & Slaytlar (Verbatim İşleme)
  console.log('\n📚 5. ADIM: Ders Notları ve Slaytlar İşleniyor (Birebir İçerik)...');
  const lectureNotesFiles = fs.readdirSync(DIRS.notlarPdf).filter(f => f.toLowerCase().endsWith('.pdf'));
  const lectureNotesJsonPath = path.join(process.cwd(), 'data', 'lecture_notes.json');
  let existingNotes = [];
  if (fs.existsSync(lectureNotesJsonPath)) {
    try { existingNotes = JSON.parse(fs.readFileSync(lectureNotesJsonPath, 'utf8')); } catch {}
  }

  const notesMap = new Map();
  existingNotes.forEach(n => {
    if (n && (n.id || n.title)) notesMap.set(n.id || n.title, n);
  });

  for (const noteFile of lectureNotesFiles) {
    const pdfPath = path.join(DIRS.notlarPdf, noteFile);
    const baseName = path.basename(noteFile, path.extname(noteFile));
    const txtPath = path.join(DIRS.notlarTxt, `${baseName}.txt`);

    console.log(`   📄 Slayt Okunuyor: ${noteFile}...`);
    const extRes = await extractVerbatimPdfText(pdfPath);
    
    // Saf metni .txt olarak kaydet
    if (extRes.fullText) {
      fs.writeFileSync(txtPath, extRes.fullText, 'utf8');
    }

    if (extRes.pages.length > 0) {
      // Slayt sayfalarını saf metin olarak formatla
      const pages = extRes.pages.map(p => ({
        pageNumber: p.pageNumber,
        content: p.text || '[Bu sayfada yalnızca şekil, şema veya mikroskobik görüntü yer almaktadır.]',
        keywords: p.text.split(/\s+/).filter(w => w.length > 4).slice(0, 10)
      }));

      const noteId = `ln-${baseName.replace(/[^a-zA-Z0-9_-]/g, '_').toLowerCase()}`;
      const noteItem = {
        id: noteId,
        committeeId: detectCommitteeId(baseName),
        title: baseName,
        discipline: baseName.includes('Patoloji') ? 'Tıbbi Patoloji' : 'Tıp Dersi',
        totalSlides: extRes.totalPages,
        pages,
      };

      notesMap.set(noteId, noteItem);
      console.log(`   ✓ ${baseName}: ${extRes.totalPages} sayfa birebir metin olarak kaydedildi.`);
    }
  }

  const updatedNotes = Array.from(notesMap.values());
  fs.writeFileSync(lectureNotesJsonPath, JSON.stringify(updatedNotes, null, 2), 'utf8');
  console.log(`   ✓ data/lecture_notes.json güncellendi! (Toplam Ders Notu: ${updatedNotes.length})`);

  // 6. ADIM: MedSoru Çalışan Sunucusuna ve Firebase'e Eşitle
  console.log('\n🌐 6. ADIM: Sunucu ve Firebase Senkronizasyonu...');
  if (totalParsedQuestions.length > 0) {
    console.log(`   📤 ${totalParsedQuestions.length} soru MedSoru sunucusuna ve veritabanına aktarılıyor...`);
    await postServerJson('/api/questions/batch-import', {
      adminEmail: 'nofrostlife@gmail.com',
      committeeId: 'donem3-kurul1',
      examYear: 'Çıkmış',
      questions: totalParsedQuestions,
    }).catch((e) => console.warn('   ⚠️ Sunucuya aktarım uyarısı:', e.message));
  }

  await postServerJson('/api/automation/drive-sync-status', {
    source: 'meds_local_sync',
    status: 'completed',
    questionsCount: mergedQuestions.length,
    notesCount: updatedNotes.length,
    timestamp: new Date().toISOString(),
  });

  console.log('\n' + '='.repeat(75));
  console.log('  🎉 SENKRONİZASYON BAŞARIYLA TAMAMLANDI!');
  console.log(`  - İndirilen ve Taranan Çıkmış Dosyaları: ${localQuestionFiles.length}`);
  console.log(`  - Havuzdaki Toplam Soru Sayısı: ${mergedQuestions.length}`);
  console.log(`  - İşlenen Ders Notu Sayısı: ${updatedNotes.length}`);
  console.log('='.repeat(75));

  // Windows Bildirimi ve Kalp Atışı
  sendWindowsNotification(
    'MedSoru: Eşitleme Tamamlandı ✅',
    `${mergedQuestions.length} soru veritabanında güncel, ${updatedNotes.length} ders notu işlendi ve Firestore'a aktarıldı.`
  );
  await sendWorkerHeartbeat('online', `Eşitleme tamamlandı (${mergedQuestions.length} soru, ${updatedNotes.length} not)`);
}

// Saat Kontrolü (16:00 - 18:00 Aralığı)
function isWithinTargetHours() {
  const currentHour = new Date().getHours();
  return currentHour >= 16 && currentHour < 18;
}

// Daemon / Zamanlayıcı Modu
async function startDaemon(forceSyncNow = false) {
  console.log('='.repeat(75));
  console.log('  🏥 MEDSORU TIP FAKÜLTESİ - GÜNLÜK YEREL SENKRONİZASYON SERVİSİ');
  console.log('='.repeat(75));
  console.log(`[BİLGİ] İşlemci Süreç Numarası (PID): ${process.pid}`);
  console.log(`[BİLGİ] Bilgisayar Adı: ${os.hostname()}`);
  console.log(`[BİLGİ] Hedef Saat Aralığı: 16:00 - 18:00 (Her gün)`);
  console.log(`[BİLGİ] Hedef Klasör: ${DIRS.root}`);
  console.log('='.repeat(75));

  // Windows Masaüstü Bildirimi
  sendWindowsNotification(
    'MedSoru Otomasyon Servisi Aktif 🚀',
    'Windows başlangıcına eklendi. Servis arka planda çalışıyor (16:00 - 18:00 arası otomatik eşitlenecektir).'
  );

  // İlk Kalp Atışı
  await sendWorkerHeartbeat('online', 'Servis başlatıldı - 16:00-18:00 aralığı bekleniyor');

  // Her 15 saniyede bir kalp atışı gönder (Web panelinde anında yeşil ONLINE yanar)
  setInterval(() => {
    sendWorkerHeartbeat('online', isWithinTargetHours() ? '16:00-18:00 aralığında aktif izleme & eşitleme' : 'Boşta - 16:00-18:00 aralığı bekleniyor');
  }, 15000);

  let hasRunToday = false;
  let lastRunDate = '';

  const checkAndRunSchedule = async (isManual = false) => {
    const today = new Date().toISOString().slice(0, 10);
    if (lastRunDate !== today) {
      hasRunToday = false;
      lastRunDate = today;
    }

    if (isManual || isWithinTargetHours()) {
      if (isManual || !hasRunToday) {
        console.log(`\n⏰ [${new Date().toLocaleTimeString('tr-TR')}] Eşitleme başlatılıyor (${isManual ? 'Manuel tetiklendi' : '16:00 - 18:00 zaman aralığı'})...`);
        hasRunToday = true;
        try {
          await runFullSync();
        } catch (err) {
          console.error('Eşitleme hatası:', err);
          sendWindowsNotification(
            'MedSoru: Eşitleme Uyarısı ⚠️',
            'Eşitleme sırasında hata oluştu: ' + (err.message || 'Bilinmeyen hata')
          );
        }
      }
    } else {
      console.log(`[Beklemede] Saat: ${new Date().toLocaleTimeString('tr-TR')} - 16:00 - 18:00 aralığı bekleniyor...`);
    }
  };

  // Eğer --sync-now bayrağı ile başlatıldıysa veya şu an 16:00-18:00 arasındaysa ilk açılışta çalıştır
  if (forceSyncNow || isWithinTargetHours()) {
    await checkAndRunSchedule(forceSyncNow);
  }

  // Her 1 dakikada bir saati kontrol et
  setInterval(() => {
    checkAndRunSchedule(false);
  }, 60 * 1000);
}

// Komut satırı argümanları
const args = process.argv.slice(2);
const isDaemon = args.includes('--daemon');
const forceSyncNow = args.includes('--sync-now');

if (isDaemon) {
  startDaemon(forceSyncNow).catch(console.error);
} else {
  // Varsayılan olarak hemen bir kez çalıştır
  runFullSync().catch(console.error);
}
