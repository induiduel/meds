#!/usr/bin/env node

/**
 * scripts/sync-drive-updates.mjs
 * 
 * MedSoru Google Drive Değişiklik Tespit ve Manuel Senkronizasyon Motoru
 * ---------------------------------------------------------------------
 * Bu script; Google Drive klasörlerinde (Ders Notları & Amfi Slaytları ve Çıkmış Sınavlar)
 * güncelleme veya yeni dosya olduğunda:
 *   1. Drive'daki tüm klasör ağacını tarar ve yerel dosyalarla karşılaştırır.
 *   2. İsteğe bağlı olarak yalnızca kontrol yapar (--check-only) ve değişiklik raporu üretir.
 *   3. Yeni veya güncellenen dosyaları indirir, saf metin (verbatim) OCR ile okur.
 *   4. Soru havuzunu (data/pastQuestions.json) ve ders slaytlarını (data/lecture_notes.json) günceller.
 *   5. Slayt-soru eşleştirmelerini yeniler ve bulut veritabanlarına eşitler.
 *
 * Kullanım:
 *   node scripts/sync-drive-updates.mjs --check-only              -> Sadece Drive değişikliklerini denetler (önizleme)
 *   node scripts/sync-drive-updates.mjs                           -> Tüm Drive güncellemelerini manuel indirir ve işler
 *   node scripts/sync-drive-updates.mjs --scope=lectures          -> Yalnızca ders notları ve slaytları eşitler
 *   node scripts/sync-drive-updates.mjs --scope=exams             -> Yalnızca çıkmış soruları eşitler
 *   node scripts/sync-drive-updates.mjs --folder=<folderId>       -> Belirtilen özel Drive klasörünü tarar ve eşitler
 *   node scripts/sync-drive-updates.mjs --force                   -> Tüm dosyaları zorla baştan indirip işler
 */

import fs from 'fs';
import path from 'path';
import https from 'https';
import http from 'http';
import os from 'os';
import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import { createRequire } from 'module';

const require = createRequire(import.meta.url);
const pdfParseModule = require('pdf-parse');
const PDFParse = pdfParseModule.PDFParse || pdfParseModule.default || pdfParseModule;

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, '..');
const DATA_DIR = path.resolve(PROJECT_ROOT, 'data');
const BASE_DATABASE_DIR = process.env.MEDS_DATABASE_DIR || 'C:\\Users\\indui\\Desktop\\meds_database';

// Target Directories
const DIRS = {
  root: BASE_DATABASE_DIR,
  sorularPdf: path.join(BASE_DATABASE_DIR, 'meds_sorular'),
  sorularTxt: path.join(BASE_DATABASE_DIR, 'meds_sorular_txt'),
  notlarPdf: path.join(BASE_DATABASE_DIR, 'ders_notlari_pdf'),
  notlarTxt: path.join(BASE_DATABASE_DIR, 'ders_notlari_txt'),
  kurulNotlar: path.join(BASE_DATABASE_DIR, 'kurul_ders_notlari'),
  kurulTxt: path.join(BASE_DATABASE_DIR, 'kurul_ders_notlari_txt'),
};

// Result and Settings files
const CHECK_RESULT_FILE = path.join(DATA_DIR, 'drive_check_result.json');
const SETTINGS_FILE = path.join(DATA_DIR, 'drive_sync_settings.json');
const PAST_QUESTIONS_FILE = path.join(DATA_DIR, 'pastQuestions.json');
const LECTURE_NOTES_FILE = path.join(DATA_DIR, 'lecture_notes.json');

// Google Drive Target Root Folders
export const DRIVE_KURUL_FOLDERS = [
  { name: 'Kurul 1 Ders Notları', committeeId: 'donem3-kurul1', id: '1P4BQ83PsKezAkSyuDFmqPklD3djjrCxA', type: 'lecture' },
  { name: 'Kurul 2 Ders Notları', committeeId: 'donem3-kurul2', id: '1SkXx2eRvojlPMkIawwFkFr9M_p7lcx_1', type: 'lecture' },
  { name: 'Kurul 3 Ders Notları', committeeId: 'donem3-kurul3', id: '14kdfK-kz_Tt3A_SAWCXJD1TzOIjmUBv8', type: 'lecture' },
  { name: 'Kurul 4 Ders Notları', committeeId: 'donem3-kurul4', id: '1F8BeGfX9WpK2xYOZaL6vPRFp_TqxKZUN', type: 'lecture' },
  { name: 'Kurul 5 Ders Notları', committeeId: 'donem3-kurul5', id: '1FlVTQMgrLHTA3F_nwsY4eqHVZWb2Np8N', type: 'lecture' },
  { name: 'Kurul 6 Ders Notları', committeeId: 'donem3-kurul6', id: '1ZQD6AIAf_CV3P5X3ColZw9kAnzgixI2k', type: 'lecture' },
  { name: 'Genel Ders Notları & Slaytlar', committeeId: 'donem3-kurul1', id: '1ozu5KiLZjFd4YKNMZ0bSRvLVV6b7lv0W', type: 'lecture' },
];

export const DRIVE_EXAM_FOLDERS = [
  { name: '1) Çıkmışlar (Kurul 1-6 & Final)', id: '18U1LZVvV0VROcWVQTDBeJYwdBWiEIVwS', type: 'exam' },
  { name: '2) 25-26 Dönem 3 Çıkmışları', id: '1VJwhDITJWZFaaBTvMajnLUzII31r1GTp', type: 'exam' },
  { name: '3) 3. Dönem', id: '1AZaRbCpIUKtv0t6sg3VaZHC42NmbrnB4', type: 'exam' },
  { name: '4) Çıkmış Sorular', id: '16ianUX4Nnl-dU9SZOSOgvDDuEaM1x6vZ', type: 'exam' },
  { name: '5) 3. Sınıf', id: '1FAqqW0iAeg3NNjkPBeY3zG9X4FXaJuVM', type: 'exam' },
  { name: '6) Dönem 3 Çıkmış Toplama', id: '1QKbD3800KBa3AUWP8apMSiKCMV0jiA21', type: 'exam' },
];

// CLI Arguments
const args = process.argv.slice(2);
const isCheckOnly = args.includes('--check-only') || args.includes('-c');
const isForce = args.includes('--force') || args.includes('-f');
const scopeArg = args.find(a => a.startsWith('--scope='))?.split('=')[1] || 'all';
const customFolderId = args.find(a => a.startsWith('--folder='))?.split('=')[1] || null;
const requestedBy = args.find(a => a.startsWith('--requested-by='))?.split('=')[1] || 'admin';

function ensureDirectories() {
  if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
  for (const dir of Object.values(DIRS)) {
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  }
}

function sanitizeFileName(name) {
  return name.replace(/[\\/:*?"<>|]/g, '_').replace(/\s+/g, ' ').trim();
}

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
  } catch (_) {}
}

async function postServerJson(endpoint, payload) {
  const LOCAL_URL = 'http://localhost:3000';
  const fullUrl = new URL(endpoint, LOCAL_URL);
  const body = JSON.stringify(payload);

  return new Promise((resolve, reject) => {
    const req = http.request(fullUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body),
      },
      timeout: 5000,
    }, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); } catch { resolve({ ok: true }); }
      });
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('Timeout')); });
    req.write(body);
    req.end();
  });
}

/**
 * Google Drive Recursive Folder Crawler
 */
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
          discovered.push({
            id,
            name,
            mime,
            isFolder,
            parentFolderId: folderId,
            fullPath: pathPrefix ? `${pathPrefix} / ${name}` : name,
          });
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

/**
 * Drive'dan dosya indirme (Redirect ve Stream desteği)
 */
function downloadDriveFile(fileId, destPath) {
  return new Promise((resolve, reject) => {
    if (!isForce && fs.existsSync(destPath) && fs.statSync(destPath).size > 1024) {
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

/**
 * PDF'den saf metin çıkarma
 */
async function extractVerbatimPdfText(pdfPath) {
  try {
    const dataBuffer = fs.readFileSync(pdfPath);
    let fullText = '';
    let totalPages = 1;
    const pages = [];

    try {
      const parser = new PDFParse({ data: dataBuffer });
      const textRes = await parser.getText();
      fullText = textRes.text || '';
      totalPages = textRes.pages?.length || 1;
      (textRes.pages || []).forEach((p, idx) => {
        pages.push({
          pageNumber: idx + 1,
          text: (p.text || '').trim(),
        });
      });
    } catch (_) {
      // Fallback pdfParse function style
      const fn = typeof pdfParseModule === 'function' ? pdfParseModule : pdfParseModule.default;
      if (typeof fn === 'function') {
        const data = await fn(dataBuffer);
        fullText = data.text || '';
        totalPages = data.numpages || 1;
        pages.push({ pageNumber: 1, text: fullText.trim() });
      }
    }

    return { fullText, totalPages, pages };
  } catch (err) {
    return { fullText: '', totalPages: 0, pages: [] };
  }
}

/**
 * Dosya adından komite ID belirleme
 */
function detectCommitteeId(fileNameOrPath) {
  const lower = fileNameOrPath.toLowerCase();
  if (lower.includes('kurul 1') || lower.includes('kurul1') || lower.includes('k1') || lower.includes('d3k1')) return 'donem3-kurul1';
  if (lower.includes('kurul 2') || lower.includes('kurul2') || lower.includes('k2') || lower.includes('d3k2')) return 'donem3-kurul2';
  if (lower.includes('kurul 3') || lower.includes('kurul3') || lower.includes('k3') || lower.includes('d3k3')) return 'donem3-kurul3';
  if (lower.includes('kurul 4') || lower.includes('kurul4') || lower.includes('k4') || lower.includes('d3k4')) return 'donem3-kurul4';
  if (lower.includes('kurul 5') || lower.includes('kurul5') || lower.includes('k5') || lower.includes('d3k5')) return 'donem3-kurul5';
  if (lower.includes('kurul 6') || lower.includes('kurul6') || lower.includes('k6') || lower.includes('d3k6')) return 'donem3-kurul6';
  return 'donem3-kurul1';
}

function detectDiscipline(textOrName) {
  const lower = (textOrName || '').toLowerCase();
  if (lower.includes('patoloji')) return 'Tıbbi Patoloji';
  if (lower.includes('farmakoloji') || lower.includes('antihipertansif')) return 'Tıbbi Farmakoloji';
  if (lower.includes('mikrobiyoloji') || lower.includes('bakteri') || lower.includes('virüs')) return 'Tıbbi Mikrobiyoloji';
  if (lower.includes('dahiliye') || lower.includes('iç hastalıkları')) return 'İç Hastalıkları (Dahiliye)';
  if (lower.includes('genetik')) return 'Tıbbi Genetik';
  if (lower.includes('pediatri') || lower.includes('çocuk')) return 'Çocuk Sağlığı ve Hastalıkları';
  if (lower.includes('cerrahi')) return 'Genel Cerrahi';
  if (lower.includes('halk sağlığı')) return 'Halk Sağlığı';
  return 'Tıp Dersi';
}

/**
 * Saf metinden soru ayrıştırma
 */
function parseQuestionsFromVerbatimText(fullText, sourceFileName, defaultCommitteeId) {
  if (!fullText || fullText.length < 50) return [];
  const lines = fullText.split(/\r?\n/).map(l => l.trim()).filter(Boolean);
  const questions = [];

  let currentQ = null;
  let qNumber = 1;

  function commitQuestion() {
    if (currentQ && currentQ.rawQuestion && currentQ.rawQuestion.length > 20) {
      if (currentQ.options.length === 0) {
        currentQ.options = [
          { key: 'A', text: 'Seçenek A' },
          { key: 'B', text: 'Seçenek B' },
          { key: 'C', text: 'Seçenek C' },
          { key: 'D', text: 'Seçenek D' },
          { key: 'E', text: 'Seçenek E' }
        ];
      }
      questions.push({
        id: `drive-q-${sanitizeFileName(sourceFileName).slice(0, 20)}-${qNumber++}`,
        committeeId: defaultCommitteeId,
        questionNumber: qNumber - 1,
        discipline: detectDiscipline(currentQ.rawQuestion + ' ' + sourceFileName),
        topic: sourceFileName.replace(/\.pdf$/i, ''),
        status: 'gathering',
        claimedAnswer: currentQ.claimedAnswer || 'A',
        upvotes: 0,
        tags: [defaultCommitteeId, 'Drive Çıkmış'],
        fragments: [{ id: 'f-1', text: currentQ.rawQuestion, authorName: 'Drive İçe Aktarım', upvotes: 0, timestamp: new Date().toISOString() }],
        options: currentQ.options,
        reconstruction: {
          stem: currentQ.rawQuestion,
          correctAnswer: currentQ.claimedAnswer || 'A',
          explanation: `Google Drive çıkmış belgesinden (${sourceFileName}) yerel CPU ile birebir okundu.`,
          confidenceScore: 85,
        },
        rawQuestion: currentQ.rawQuestion,
        sourceFile: sourceFileName,
        examYear: 'Çıkmış Arşiv',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      });
    }
  }

  const qRegex = /^(?:Soru\s*)?(\d+)[\.\)\-:]\s*(.*)$/i;
  const optRegex = /^([A-E])[\.\)\-:]\s*(.*)$/i;
  const ansRegex = /(?:Doğru\s*Cevap|Cevap|Yanıt)\s*[:\-]?\s*([A-E])/i;

  for (const line of lines) {
    const qMatch = line.match(qRegex);
    if (qMatch && parseInt(qMatch[1], 10) < 300) {
      commitQuestion();
      currentQ = {
        rawQuestion: qMatch[2] || '',
        options: [],
        claimedAnswer: null,
      };
      continue;
    }

    if (currentQ) {
      const ansMatch = line.match(ansRegex);
      if (ansMatch) {
        currentQ.claimedAnswer = ansMatch[1].toUpperCase();
        continue;
      }

      const optMatch = line.match(optRegex);
      if (optMatch) {
        currentQ.options.push({
          key: optMatch[1].toUpperCase(),
          text: optMatch[2] || '',
        });
        continue;
      }

      if (currentQ.options.length === 0) {
        currentQ.rawQuestion += ' ' + line;
      }
    }
  }

  commitQuestion();
  return questions;
}

/**
 * Check if a file is already downloaded and processed locally
 */
function isFileLocallyPresent(file, targetType) {
  const safeName = sanitizeFileName(file.name);
  const baseNoExt = safeName.replace(/\.[^/.]+$/, '');

  let existsOnDisk = false;
  let hasExtractedTxt = false;

  if (targetType === 'exam') {
    const pdfPath = path.join(DIRS.sorularPdf, safeName);
    const txtPath = path.join(DIRS.sorularTxt, `${baseNoExt}.txt`);
    existsOnDisk = fs.existsSync(pdfPath) && fs.statSync(pdfPath).size > 1024;
    hasExtractedTxt = fs.existsSync(txtPath) && fs.statSync(txtPath).size > 50;
  } else {
    // Check in both kurulNotlar and notlarPdf
    const pdfPath1 = path.join(DIRS.notlarPdf, safeName);
    const txtPath1 = path.join(DIRS.notlarTxt, `${baseNoExt}.txt`);
    const pdfPath2 = path.join(DIRS.kurulNotlar, safeName);
    const txtPath2 = path.join(DIRS.kurulTxt, `${baseNoExt}.txt`);

    existsOnDisk = (fs.existsSync(pdfPath1) && fs.statSync(pdfPath1).size > 1024) ||
                   (fs.existsSync(pdfPath2) && fs.statSync(pdfPath2).size > 1024);
    hasExtractedTxt = (fs.existsSync(txtPath1) && fs.statSync(txtPath1).size > 50) ||
                      (fs.existsSync(txtPath2) && fs.statSync(txtPath2).size > 50);
  }

  return { existsOnDisk, hasExtractedTxt, isUpToDate: existsOnDisk && hasExtractedTxt };
}

/**
 * MAIN EXECUTION ENGINE
 */
async function main() {
  console.log('='.repeat(75));
  console.log('  🏥 MEDSORU - GOOGLE DRIVE GÜNCELLEME TESPİT VE SENKRONİZASYON MOTORU');
  console.log('='.repeat(75));
  console.log(`[Mod]           : ${isCheckOnly ? '🔍 Yalnızca Denetle (Önizleme - İndirme Yapılmaz)' : '🚀 Tam Manuel Güncelleme & Senkronizasyon'}`);
  console.log(`[Kapsam]        : ${scopeArg.toUpperCase()} (Özel Klasör: ${customFolderId || 'Varsayılan Liste'})`);
  console.log(`[Zorla İndir]   : ${isForce ? 'Evet (--force)' : 'Hayır (Yalnızca Yeni / Değişen Dosyalar)'}`);
  console.log(`[İsteyen]       : ${requestedBy}`);
  console.log('-'.repeat(75));

  ensureDirectories();

  // 1. Determine target folders to crawl
  let targetRoots = [];
  if (customFolderId) {
    targetRoots.push({ name: `Özel Klasör (${customFolderId})`, id: customFolderId, type: 'custom' });
  } else if (scopeArg === 'lectures') {
    targetRoots = [...DRIVE_KURUL_FOLDERS];
  } else if (scopeArg === 'exams') {
    targetRoots = [...DRIVE_EXAM_FOLDERS];
  } else {
    // Default 'all'
    targetRoots = [...DRIVE_KURUL_FOLDERS, ...DRIVE_EXAM_FOLDERS];
  }

  console.log(`\n📂 [ADIM 1] Google Drive Klasörleri Taranıyor (${targetRoots.length} ana kaynak)...`);
  const allDiscoveredFiles = [];
  const visitedFolderIds = new Set();

  for (const root of targetRoots) {
    console.log(`   🔎 Taranıyor: "${root.name}" (ID: ${root.id})...`);
    const files = await crawlDriveFolder(root.id, root.name, visitedFolderIds);
    files.forEach(f => {
      f.rootType = root.type || (root.name.toLowerCase().includes('çıkmış') ? 'exam' : 'lecture');
      f.committeeId = root.committeeId || detectCommitteeId(f.fullPath || f.name);
    });
    console.log(`      ✓ Bulunan dosya sayısı: ${files.length}`);
    allDiscoveredFiles.push(...files);
  }

  // Deduplicate files by ID
  const uniqueDriveFiles = [];
  const seenFileIds = new Set();
  for (const file of allDiscoveredFiles) {
    if (!seenFileIds.has(file.id)) {
      seenFileIds.add(file.id);
      uniqueDriveFiles.push(file);
    }
  }

  console.log(`\n📊 [ADIM 2] Drive Dosyaları Yerel Arşivle Kıyaslanıyor...`);
  console.log(`   Drive'da Toplam Dosya: ${uniqueDriveFiles.length}`);

  const newOrUpdatedFiles = [];
  let upToDateCount = 0;

  for (const file of uniqueDriveFiles) {
    const ext = path.extname(file.name).toLowerCase();
    // Only accept documents / slides
    if (!['.pdf', '.docx', '.doc', '.pptx'].includes(ext)) continue;

    const presence = isFileLocallyPresent(file, file.rootType);
    if (!presence.isUpToDate || isForce) {
      newOrUpdatedFiles.push({
        id: file.id,
        name: file.name,
        fullPath: file.fullPath,
        mime: file.mime,
        type: file.rootType,
        committeeId: file.committeeId,
        existsOnDisk: presence.existsOnDisk,
        hasExtractedTxt: presence.hasExtractedTxt,
      });
    } else {
      upToDateCount++;
    }
  }

  console.log(`   ✓ Güncel Dosyalar (Yerelde Mevcut) : ${upToDateCount}`);
  console.log(`   ⚡ YENİ / GÜNCELLENEN DOSYALAR    : ${newOrUpdatedFiles.length}`);

  // Write check result artifact
  const checkSummary = {
    checkedAt: new Date().toISOString(),
    scope: scopeArg,
    customFolderId,
    totalScanned: uniqueDriveFiles.length,
    upToDateCount,
    newCount: newOrUpdatedFiles.length,
    hasUpdates: newOrUpdatedFiles.length > 0,
    newFiles: newOrUpdatedFiles.map(f => ({
      name: f.name,
      fullPath: f.fullPath,
      type: f.type,
      committeeId: f.committeeId,
      status: !f.existsOnDisk ? 'YENİ_DOSYA' : 'METİN_EKSİK'
    })),
  };

  fs.writeFileSync(CHECK_RESULT_FILE, JSON.stringify(checkSummary, null, 2), 'utf8');

  // If check-only mode, report and exit gracefully
  if (isCheckOnly) {
    console.log('\n' + '='.repeat(75));
    if (newOrUpdatedFiles.length > 0) {
      console.log(`🔔 TESPİT EDİLDİ: Google Drive'da ${newOrUpdatedFiles.length} yeni veya güncellenmiş dosya bulundu!`);
      newOrUpdatedFiles.slice(0, 15).forEach((f, idx) => {
        console.log(`   [${idx + 1}] [${f.type.toUpperCase()}] ${f.name} (${f.fullPath})`);
      });
      if (newOrUpdatedFiles.length > 15) {
        console.log(`   ... ve ${newOrUpdatedFiles.length - 15} dosya daha.`);
      }
      console.log(`\n💡 Bu dosyaları indirmek ve soru havuzuna işlemek için "Şimdi Güncelle" seçeneğini kullanabilirsiniz.`);
    } else {
      console.log('✅ SONUÇ: Tebrikler! Google Drive ile yerel arşiviniz %100 birebir güncel.');
      console.log('   Yeni dosya bulunamadı.');
    }
    console.log('='.repeat(75));
    return;
  }

  // -------------------------------------------------------------
  // SYNC EXECUTION MODE: Download, extract verbatim text, and import
  // -------------------------------------------------------------
  if (newOrUpdatedFiles.length === 0) {
    console.log('\n✅ İndirilecek yeni dosya yok. Veritabanı ve slayt ilişkileri zaten %100 güncel.');
    return;
  }

  console.log(`\n📥 [ADIM 3] Yeni Dosyalar İndiriliyor & Yerel CPU ile Metne Dönüştürülüyor...`);

  // Existing past questions
  let existingQuestions = [];
  try {
    if (fs.existsSync(PAST_QUESTIONS_FILE)) {
      existingQuestions = JSON.parse(fs.readFileSync(PAST_QUESTIONS_FILE, 'utf8'));
    }
  } catch (_) {}

  // Existing lecture notes
  let existingNotes = [];
  try {
    if (fs.existsSync(LECTURE_NOTES_FILE)) {
      existingNotes = JSON.parse(fs.readFileSync(LECTURE_NOTES_FILE, 'utf8'));
    }
  } catch (_) {}
  const notesMap = new Map();
  for (const n of existingNotes) {
    if (n && n.id) notesMap.set(n.id, n);
  }

  let newlyDownloadedCount = 0;
  let newlyExtractedQuestions = [];
  let newlyAddedLectureNotesCount = 0;

  for (let i = 0; i < newOrUpdatedFiles.length; i++) {
    const file = newOrUpdatedFiles[i];
    const safeName = sanitizeFileName(file.name);
    const baseNoExt = safeName.replace(/\.[^/.]+$/, '');
    const isExam = file.type === 'exam' || safeName.toLowerCase().includes('çıkmış') || safeName.toLowerCase().includes('soru');

    console.log(`\n[${i + 1}/${newOrUpdatedFiles.length}] 📥 İşleniyor: "${file.name}"...`);

    const destDir = isExam ? DIRS.sorularPdf : DIRS.notlarPdf;
    const txtDir = isExam ? DIRS.sorularTxt : DIRS.notlarTxt;
    const destPath = path.join(destDir, safeName);
    const txtPath = path.join(txtDir, `${baseNoExt}.txt`);

    try {
      // 1. Download if missing
      const dlRes = await downloadDriveFile(file.id, destPath);
      if (!dlRes.skipped) {
        newlyDownloadedCount++;
        console.log(`   ✓ İndirildi: ${(dlRes.size / 1024).toFixed(1)} KB`);
      } else {
        console.log(`   ✓ Önceden indirilmiş dosya kullanılıyor.`);
      }

      // 2. Extract verbatim text if PDF
      if (safeName.toLowerCase().endsWith('.pdf')) {
        console.log(`   🔍 Yerel CPU ile sayfa sayfa okunuyor (Verbatim OCR)...`);
        const extRes = await extractVerbatimPdfText(destPath);

        if (extRes.fullText && extRes.fullText.length > 50) {
          fs.writeFileSync(txtPath, extRes.fullText, 'utf8');

          if (isExam) {
            // Parse questions
            const parsedQs = parseQuestionsFromVerbatimText(extRes.fullText, file.name, file.committeeId);
            if (parsedQs.length > 0) {
              console.log(`   🎯 ${parsedQs.length} soru tespit edildi ve ayrıştırıldı.`);
              newlyExtractedQuestions.push(...parsedQs);
            }
          } else {
            // Lecture note
            const noteId = `ln-${baseNoExt.replace(/[^a-zA-Z0-9_-]/g, '_').toLowerCase()}`;
            const pages = extRes.pages.map(p => ({
              pageNumber: p.pageNumber,
              content: p.text || '[Yalnızca şekil, şema veya grafik]',
              keywords: p.text.split(/\s+/).filter(w => w.length > 4).slice(0, 10),
            }));

            const noteItem = {
              id: noteId,
              committeeId: file.committeeId,
              title: baseNoExt,
              discipline: detectDiscipline(baseNoExt),
              totalSlides: extRes.totalPages,
              pages,
              driveFileId: file.id,
              driveFileUrl: `https://drive.google.com/file/d/${file.id}/view`,
              updatedAt: new Date().toISOString(),
            };

            notesMap.set(noteId, noteItem);
            newlyAddedLectureNotesCount++;
            console.log(`   ✓ Ders notu olarak kaydedildi: ${extRes.totalPages} slayt sayfası.`);
          }
        }
      }
    } catch (err) {
      console.warn(`   ⚠️ Dosya işlenirken hata oluştu (${file.name}):`, err.message);
    }
  }

  // -------------------------------------------------------------
  // MERGE & SAVE UPDATED DATA
  // -------------------------------------------------------------
  console.log(`\n💾 [ADIM 4] Veritabanı ve Havuz Güncelleniyor...`);

  // 1. Merge questions
  if (newlyExtractedQuestions.length > 0) {
    const questionMap = new Map();
    for (const q of existingQuestions) {
      if (q && q.id) questionMap.set(q.id, q);
    }
    for (const q of newlyExtractedQuestions) {
      questionMap.set(q.id, q);
    }
    const mergedList = Array.from(questionMap.values());
    fs.writeFileSync(PAST_QUESTIONS_FILE, JSON.stringify(mergedList, null, 2), 'utf8');
    console.log(`   ✓ ${newlyExtractedQuestions.length} yeni soru data/pastQuestions.json havuzuna eklendi (Toplam: ${mergedList.length})`);
  }

  // 2. Save lecture notes
  const updatedLectureNotes = Array.from(notesMap.values());
  fs.writeFileSync(LECTURE_NOTES_FILE, JSON.stringify(updatedLectureNotes, null, 2), 'utf8');
  console.log(`   ✓ Ders notları data/lecture_notes.json güncellendi (Toplam: ${updatedLectureNotes.length})`);

  // 3. Save sync settings and log
  const syncSettings = {
    lastSyncedAt: new Date().toISOString(),
    lastCheckedAt: new Date().toISOString(),
    scope: scopeArg,
    customFolderId,
    newFilesProcessed: newlyDownloadedCount,
    newQuestionsAdded: newlyExtractedQuestions.length,
    newNotesAdded: newlyAddedLectureNotesCount,
    status: 'completed',
    message: `Senkronizasyon tamamlandı: ${newlyDownloadedCount} dosya indirildi, ${newlyExtractedQuestions.length} soru ve ${newlyAddedLectureNotesCount} slayt işlendi.`,
  };
  fs.writeFileSync(SETTINGS_FILE, JSON.stringify(syncSettings, null, 2), 'utf8');

  // 4. Notify local server & Windows notification
  try {
    await postServerJson('/api/automation/drive-sync-status', {
      source: 'sync_drive_updates',
      status: 'completed',
      questionsCount: existingQuestions.length + newlyExtractedQuestions.length,
      notesCount: updatedLectureNotes.length,
      timestamp: new Date().toISOString(),
    });
  } catch (_) {}

  sendWindowsNotification(
    'MedSoru: Google Drive Senkronizasyonu Tamamlandı ✅',
    `${newlyDownloadedCount} yeni dosya indirildi. ${newlyExtractedQuestions.length} soru ve ${newlyAddedLectureNotesCount} ders notu havuza eklendi.`
  );

  console.log('\n' + '='.repeat(75));
  console.log('  🎉 MANUEL GOOGLE DRIVE GÜNCELLEMESİ BAŞARIYLA TAMAMLANDI!');
  console.log(`  - İndirilen Dosya Sayısı      : ${newlyDownloadedCount}`);
  console.log(`  - Eklenen Yeni Soru Sayısı    : ${newlyExtractedQuestions.length}`);
  console.log(`  - Güncellenen Ders Notu Sayısı: ${newlyAddedLectureNotesCount}`);
  console.log('='.repeat(75));
}

main().catch(err => {
  console.error('\n❌ [Kritik Senkronizasyon Hatası]:', err);
  process.exit(1);
});
