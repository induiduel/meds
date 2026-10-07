#!/usr/bin/env node

/**
 * scripts/transcribe-drive-audio.mjs
 * 
 * MedSoru Tıbbi Amfi Ses Kayıtları Transkripsiyon, Ders Eşleştirme ve İzleme Motoru
 * ---------------------------------------------------------------------------------
 * 1. Google Drive ('G:\Drive'ım\Tıp Genel\Ses Kayıtları Dönem 3 (26-27)') klasörünü
 *    özyinelemeli (recursive) tarar ve yeni ses kayıtlarını yerel 'meds_database/ses_kayitlari'
 *    klasörüne %100 eksiksiz indirir.
 * 2. Tıp müfredatı (Karabük Tıp Dönem 3), 347 amfi dersi özeti ve geçmiş Kurul çıkmış soruları
 *    ile eşleştirme yaparak dersin Kurul, Disiplin, Hoca ve Konu kimliğini tespit eder.
 * 3. Karabük Tıp çıkmış sınav sorularını (pastQuestions / redakte_sorular) prompta enjekte ederek
 *    amfide hocanın sınav uyarısı yaptığı yerleri 'High-Yield Pearls' olarak çıkarır.
 * 4. Gemini 3.5 Flash-Lite ve 3.8 Flash Multimodal File API ile 15'er dakikalık pencereler halinde
 *    dakika dakika, %100 KESİNTİSİZ ve KELİMESİ KELİMESİNE (verbatim) transkript üretir.
 * 5. Kalıcı otomatik izleme (--watch) modu ile Google Drive'a yeni ses eklendiğinde
 *    otomatik olarak algılayıp transkribe eder.
 */

import fs from 'fs';
import path from 'path';
import os from 'os';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';
import { GoogleGenAI } from '@google/genai';

dotenv.config();

// Global Crash Koruma Handlers
process.on('uncaughtException', (err) => {
  log(`⚠️ [Global Koruma] Yakalanmamış İstisna: ${err.message}`);
});
process.on('unhandledRejection', (reason) => {
  log(`⚠️ [Global Koruma] Yakalanmamış Promise Reddi: ${reason?.message || reason}`);
});

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');
const BASE_DATABASE_DIR = process.env.MEDS_DATABASE_DIR || `${process.env.MEDS_DATABASE_DIR || '/home/indu/medsor/meds_database'}`;

// Klasör Yolları
const DRIVE_ROOT_DIR = path.join('G:', "Drive'ım", 'Tıp Genel', 'Ses Kayıtları Dönem 3 (26-27)');
const LOCAL_AUDIO_DIR = path.join(BASE_DATABASE_DIR, 'ses_kayitlari');
const TRANSCRIPTION_OUT_DIR = path.join(BASE_DATABASE_DIR, 'transcriptions');
const MANIFEST_PATH = path.join(TRANSCRIPTION_OUT_DIR, 'transcription_manifest.json');
const WATCHER_LOG_PATH = path.join(TRANSCRIPTION_OUT_DIR, 'watcher.log');

const SUMMARIES_CATALOG_PATHS = [
  path.join(ROOT_DIR, 'src', 'data', 'summaries_meta.json'),
  path.join(BASE_DATABASE_DIR, 'redakte_ozet_manifest.json')
];

const REDAKTE_SORULAR_DIR = path.join(BASE_DATABASE_DIR, 'redakte_sorular');
const PAST_QUESTIONS_PATH = path.join(ROOT_DIR, 'data', 'pastQuestions.json');

// Komut Satırı Argümanları
const args = process.argv.slice(2);
const isWatchMode = args.includes('--watch') || args.includes('-w');
const isForce = args.includes('--force') || args.includes('-f');
const modelArg = args.find(a => a.startsWith('--model='))?.split('=')[1] || 'gemini-3.5-flash-lite';
const delayArg = parseInt(args.find(a => a.startsWith('--delay='))?.split('=')[1] || '6', 10);
const limitArg = parseInt(args.find(a => a.startsWith('--limit='))?.split('=')[1] || '0', 10);
const watchIntervalSec = parseInt(args.find(a => a.startsWith('--interval='))?.split('=')[1] || '60', 10);

const GEMINI_API_KEY = process.env.GEMINI_API_KEY || process.env.GOOGLE_API_KEY || '';

// Logger
function log(msg, alsoConsole = true) {
  const timeStr = new Date().toISOString().replace('T', ' ').substring(0, 19);
  const formatted = `[${timeStr}] ${msg}`;
  if (alsoConsole) console.log(formatted);
  try {
    fs.mkdirSync(TRANSCRIPTION_OUT_DIR, { recursive: true });
    fs.appendFileSync(WATCHER_LOG_PATH, formatted + '\n', 'utf8');
  } catch (_) {}
}

// M4A / MP4 Süre Okuyucu (mvhd atomu)
function getM4aDuration(filePath) {
  try {
    const fd = fs.openSync(filePath, 'r');
    const stat = fs.fstatSync(fd);
    const size = stat.size;
    const buf = Buffer.alloc(Math.min(size, 6 * 1024 * 1024));
    fs.readSync(fd, buf, 0, buf.length, Math.max(0, size - buf.length));
    let idx = buf.indexOf('mvhd');
    if (idx === -1) {
      fs.readSync(fd, buf, 0, buf.length, 0);
      idx = buf.indexOf('mvhd');
    }
    fs.closeSync(fd);
    if (idx !== -1) {
      const version = buf[idx + 4];
      if (version === 0) {
        const timescale = buf.readUInt32BE(idx + 16);
        const duration = buf.readUInt32BE(idx + 20);
        return duration / timescale;
      } else {
        const timescale = buf.readUInt32BE(idx + 24);
        const duration = Number(buf.readBigUInt64BE(idx + 28));
        return duration / timescale;
      }
    }
  } catch (_) {}
  return null;
}

function formatSeconds(totalSec) {
  const m = Math.floor(totalSec / 60);
  const s = Math.floor(totalSec % 60);
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
}

// 15'er Dakikalık Güvenli Zaman Pencereleri
function createTimeWindows(durationSeconds, windowSizeSec = 900) {
  if (!durationSeconds || durationSeconds <= 900) {
    return [{
      index: 1,
      total: 1,
      startStr: '00:00',
      endStr: durationSeconds ? formatSeconds(durationSeconds) : 'Ders Sonu',
      startSec: 0,
      endSec: durationSeconds || 0,
      isFirst: true,
      isLast: true
    }];
  }

  const windows = [];
  let currentStart = 0;
  let idx = 1;

  while (currentStart < durationSeconds) {
    const currentEnd = Math.min(currentStart + windowSizeSec, durationSeconds);
    const isFirst = idx === 1;
    const isLast = currentEnd >= durationSeconds;

    windows.push({
      index: idx,
      startStr: formatSeconds(currentStart),
      endStr: formatSeconds(currentEnd),
      startSec: currentStart,
      endSec: currentEnd,
      isFirst,
      isLast
    });

    idx++;
    currentStart = currentEnd;
  }

  windows.forEach(w => w.total = windows.length);
  return windows;
}

// ASCII Güvenli İsim
function toAsciiSafeName(str) {
  return str
    .replace(/ı/g, 'i').replace(/İ/g, 'I')
    .replace(/ğ/g, 'g').replace(/Ğ/g, 'G')
    .replace(/ü/g, 'u').replace(/Ü/g, 'U')
    .replace(/ş/g, 's').replace(/Ş/g, 'S')
    .replace(/ö/g, 'o').replace(/Ö/g, 'O')
    .replace(/ç/g, 'c').replace(/Ç/g, 'C')
    .replace(/[^a-zA-Z0-9._-]/g, '_');
}

// Tıbbi Kısaltma ve Yazım Düzeltmeleri
const TYPO_MAP = {
  'üoloji': 'üroloji',
  'uoloji': 'üroloji',
  'saülığı': 'sağlığı',
  'sauiligi': 'sağlığı',
  'genetşk': 'genetik',
  'genetsk': 'genetik',
  'tbg': 'tıbbi genetik',
  'hs': 'halk sağlığı',
  'farmakolji': 'farmakoloji',
  'patolji': 'patoloji',
  'enfeksyon': 'enfeksiyon',
};

function normalizeText(str) {
  if (!str) return '';
  let s = str.toLowerCase();
  for (const [typo, fix] of Object.entries(TYPO_MAP)) {
    s = s.replace(new RegExp(`\\b${typo}\\b`, 'gi'), fix);
    s = s.replace(new RegExp(typo, 'gi'), fix);
  }
  return s
    .replace(/[ıİ]/g, 'i').replace(/[ğĞ]/g, 'g').replace(/[üÜ]/g, 'u')
    .replace(/[şŞ]/g, 's').replace(/[öÖ]/g, 'o').replace(/[çÇ]/g, 'c')
    .replace(/[^a-z0-9\s]/g, ' ')
    .replace(/\s+/g, ' ').trim();
}

// 1. Bilgi Tabanını Yükle (Ders Özetleri Kataloğu)
function loadSummariesCatalog() {
  for (const cp of SUMMARIES_CATALOG_PATHS) {
    if (fs.existsSync(cp)) {
      try {
        const data = JSON.parse(fs.readFileSync(cp, 'utf8'));
        log(`📚 Ders Kataloğu Yüklendi (${data.length} ders): ${path.basename(cp)}`);
        return data;
      } catch (e) {
        log(`⚠️ Katalog okuma hatası (${cp}): ${e.message}`);
      }
    }
  }
  return [];
}

// 2. Çıkmış Sınav Soruları Veritabanını Yükle
function loadPastQuestionsDatabase() {
  let allQuestions = [];
  
  // A) Redakte Sorular klasöründeki resmi sorular
  if (fs.existsSync(REDAKTE_SORULAR_DIR)) {
    try {
      const files = fs.readdirSync(REDAKTE_SORULAR_DIR).filter(f => f.endsWith('.json'));
      for (const f of files) {
        const fPath = path.join(REDAKTE_SORULAR_DIR, f);
        try {
          const qList = JSON.parse(fs.readFileSync(fPath, 'utf8'));
          if (Array.isArray(qList)) {
            allQuestions.push(...qList);
          }
        } catch (_) {}
      }
      log(`🎯 Redakte Soru Havuzundan ${allQuestions.length} soru yüklendi.`);
    } catch (_) {}
  }

  // B) pastQuestions.json (Geniş Çıkmışlar Havuzu)
  if (allQuestions.length === 0 && fs.existsSync(PAST_QUESTIONS_PATH)) {
    try {
      const raw = JSON.parse(fs.readFileSync(PAST_QUESTIONS_PATH, 'utf8'));
      if (Array.isArray(raw)) {
        allQuestions.push(...raw);
        log(`🎯 pastQuestions.json havuzundan ${allQuestions.length} soru yüklendi.`);
      }
    } catch (_) {}
  }

  return allQuestions;
}

// Aday Ders Eşleştirme (Klasör Hiyerarşisi + Dosya Adı)
function findBestLectureCandidate(filePath, catalog) {
  const fileName = path.basename(filePath);
  const cleanName = normalizeText(path.basename(fileName, path.extname(fileName)));
  const relativeParts = filePath.split(path.sep).map(p => normalizeText(p));
  const fullContext = relativeParts.join(' ') + ' ' + cleanName;
  const words = fullContext.split(' ').filter(w => w.length > 2);

  let best = null;
  let maxScore = 0;

  for (const item of catalog) {
    const target = normalizeText(`${item.committeeId || ''} ${item.discipline || ''} ${item.title || ''} ${(item.keyPoints || []).join(' ')}`);
    let score = 0;
    for (const w of words) {
      if (target.includes(w)) score++;
    }
    if (score > maxScore) {
      maxScore = score;
      best = item;
    }
  }

  // Klasörden doğrudan tespit
  let detectedDiscipline = 'Tıp Fakültesi';
  let detectedKurul = 1;
  let committeeId = 'donem3-kurul1';

  if (fullContext.includes('patoloji')) detectedDiscipline = 'Tıbbi Patoloji';
  else if (fullContext.includes('uroloji')) detectedDiscipline = 'Üroloji';
  else if (fullContext.includes('enfeksiyon')) detectedDiscipline = 'Enfeksiyon Hastalıkları';
  else if (fullContext.includes('halk')) detectedDiscipline = 'Halk Sağlığı';
  else if (fullContext.includes('genetik') || fullContext.includes('tbg')) detectedDiscipline = 'Tıbbi Genetik';

  for (let k = 1; k <= 6; k++) {
    if (fullContext.includes(`kurul ${k}`) || fullContext.includes(`kurul${k}`) || fullContext.includes(`k${k}`)) {
      detectedKurul = k;
      committeeId = `donem3-kurul${k}`;
      break;
    }
  }

  if (best && maxScore >= 2) {
    return {
      committeeId: best.committeeId || committeeId,
      kurul: best.kurul || detectedKurul,
      discipline: best.discipline || detectedDiscipline,
      title: best.title,
      keyPoints: best.keyPoints || [],
      confidence: maxScore >= 4 ? 'Yüksek' : 'Orta'
    };
  }

  return {
    committeeId,
    kurul: detectedKurul,
    discipline: detectedDiscipline,
    title: path.basename(fileName, path.extname(fileName)),
    keyPoints: [],
    confidence: 'Ön Sezgisel'
  };
}

// Konuyla İlişkili Çıkmış Sınav Sorularını Bul
function findMatchingPastQuestions(candidate, fileName, allQuestions, maxCount = 5) {
  if (!allQuestions || allQuestions.length === 0) return [];

  const searchKeywords = [
    ...normalizeText(candidate.title).split(' '),
    ...normalizeText(candidate.discipline).split(' '),
    ...normalizeText(path.basename(fileName, path.extname(fileName))).split(' ')
  ].filter(w => w.length > 3 && !['dersi', 'kaydi', 'gunu', 'giris', 'kurul', 'donem', 'genel'].includes(w));

  const scored = [];
  const commId = candidate.committeeId || `donem3-kurul${candidate.kurul}`;

  for (const q of allQuestions) {
    let score = 0;
    // Aynı kurul ise öncelik ver
    if (q.committeeId === commId || q.kurul === candidate.kurul) score += 2;
    // Aynı branş ise öncelik ver
    const qDisc = normalizeText(q.discipline || '');
    const cDisc = normalizeText(candidate.discipline || '');
    if (qDisc && cDisc && (qDisc.includes(cDisc) || cDisc.includes(qDisc))) score += 4;

    const qText = normalizeText(`${q.topic || ''} ${q.stem || ''} ${q.explanation || ''}`);
    for (const kw of searchKeywords) {
      if (qText.includes(kw)) score += 3;
    }

    if (score >= 5) {
      scored.push({ q, score });
    }
  }

  scored.sort((a, b) => b.score - a.score);
  return scored.slice(0, maxCount).map(s => s.q);
}

// Metadata & Sınav Hap Bilgileri Promptu
function buildMetadataPrompt(candidate, fileName, relatedQuestions) {
  const kpStr = candidate.keyPoints && candidate.keyPoints.length > 0
    ? candidate.keyPoints.map(k => `- ${k}`).join('\n')
    : 'Mevcut değil';

  let questionsStr = 'Bu ders konusuyla doğrudan eşleşen arşiv sorusu bulunamadı.';
  if (relatedQuestions && relatedQuestions.length > 0) {
    questionsStr = relatedQuestions.map((q, idx) => {
      const correctOpt = q.options?.find(o => o.key === q.correctAnswer || o.isCorrect)?.text || q.correctAnswer || 'Belirtilmedi';
      const expl = q.explanation ? `\n   *Açıklama/Klinik:* ${q.explanation.substring(0, 200)}...` : '';
      return `${idx + 1}. [${q.discipline || 'Tıp'} / ${q.examYear || 'Çıkmış'}] **Soru:** ${q.stem}\n   *Doğru Yanıt:* ${correctOpt}${expl}`;
    }).join('\n\n');
  }

  return `Sen Karabük Üniversitesi Tıp Fakültesi Dönem 3 amfi dersleri ve klinik müfredat uzmanısın.
SES DOSYASI: ${fileName}
Ön Eşleştirme (Aday Ders): ${candidate.discipline} - ${candidate.title}

DERS NOTLARI VE SLAYT REFERANS NOKTALARI:
${kpStr}

🎯 İLİŞKİLİ KARABÜK TIP ÇIKMIŞ SINAV SORULARI & RESMİ ARŞİV:
${questionsStr}

GÖREVLERİN:
1. Ses kaydının başındaki konuşmalardan, hoca hitabından ve ders konusundan hareketle dersin gerçek kimliğini tespit et:
   - Gerçek Dönem 3 Kurulu (Kurul 1-6)
   - Tıp Disiplini (örn. Halk Sağlığı, Tıbbi Genetik, Üroloji, Patoloji, Farmakoloji vb.)
   - Resmi Ders Adı
   - Öğretim Üyesi (Hocanın Adı)
2. Dersin genel özetini ve işlenen temel kavramları çıkar.
3. Amfi ve sınav için en kritik hap bilgileri (High-Yield Pearls) listele.
   - ÖZELLİKLE yukarıda verilen çıkmış sınav soruları veya hocanın amfide 'burası sınavda gelir', 'TUS'ta sorarlar' dediği noktaları vurgula.

ÇIKTI FORMATI:
# 🩺 [Tespit Edilen Resmi Ders Adı]

> **Kurul:** Kurul X - [Kurul Adı] (TIP XXX)  
> **Disiplin:** [Tıp Disiplini]  
> **Öğretim Üyesi:** [Hocanın Adı veya 'Belirtilmedi']  
> **Kaynak Ses Kaydı:** \`${fileName}\`  
> **Tespit Güveni:** [%95 - Doğrulandı]  

---

## 📌 Dersin Genel Özeti ve Anahtar Kavramlar
[Dersin ana hatları ve işlenen temel kavramlar]

## ⭐ Amfi & Sınav Hap Bilgileri (High-Yield Pearls & Çıkmış Sorular)
- **[Kavram 1]:** [Hocanın özellikle sınav için uyardığı kritik nokta / Çıkmış soru paraleli]
- **[Kavram 2]:** [Klinik / TUS ipucu]
- **[Kavram 3]:** ...
`;
}

// Saf Verbatim Transkripsiyon Promptu
function buildVerbatimSegmentPrompt(fileName, window) {
  return `Sen Tıp Fakültesi amfi derslerinin resmi tutanak kâtibi ve klinik transkripsiyon uzmanısın.

SES DOSYASI: ${fileName}
BÖLÜM: ${window.index}/${window.total} (Zaman Aralığı: ${window.startStr} - ${window.endStr})

GÖREVİN:
Bu ses kaydının YALNIZCA [${window.startStr}] ile [${window.endStr}] arasındaki konuşmalarını KESİNTİSİZ ve KELİMESİ KELİMESİNE (verbatim) transkribe etmektir.

KESİN KURALLAR:
1. KESİNLİKLE ÖZETLEME YAPMA. Cümleleri kısaltma veya atlama.
2. Hocanın ağzından çıkan her cümleyi, anlatılan teorik bilgileri, slayt okumalarını ve açıklamaları eksiksiz tam metin olarak yaz.
3. Başlık, selamlama veya özet YAZMA. Doğrudan [${window.startStr}] konuşmasıyla başla.
4. Her 1-2 dakikalık konuşmanın başına kronolojik zaman damgası koy ([${window.startStr}], [${formatSeconds(window.startSec + 90)}] vb.).
5. Tıbbi terimleri, anatomik isimleri ve ilaç adlarını doğru tıp imlasıyla yaz.`;
}

function extractResponseText(response) {
  if (response.text) return response.text;
  const parts = response.candidates?.[0]?.content?.parts || [];
  const textParts = parts.filter(p => p.text && !p.thought).map(p => p.text);
  if (textParts.length > 0) return textParts.join('\n');
  return parts.map(p => p.text).filter(Boolean).join('\n');
}

function parseMarkdownMetadata(mdText) {
  const meta = {
    lectureTitle: '',
    committee: '',
    discipline: '',
    instructor: '',
    confidence: ''
  };

  const titleMatch = mdText.match(/^#\s*🩺\s*(.+)$/m);
  if (titleMatch) meta.lectureTitle = titleMatch[1].trim();

  const kurulMatch = mdText.match(/\*\*Kurul:\*\*\s*(.+)/);
  if (kurulMatch) meta.committee = kurulMatch[1].trim();

  const discMatch = mdText.match(/\*\*Disiplin:\*\*\s*(.+)/);
  if (discMatch) meta.discipline = discMatch[1].trim();

  const instMatch = mdText.match(/\*\*Öğretim Üyesi:\*\*\s*(.+)/);
  if (instMatch) meta.instructor = instMatch[1].trim();

  const confMatch = mdText.match(/\*\*Tespit Güveni:\*\*\s*(.+)/);
  if (confMatch) meta.confidence = confMatch[1].trim();

  return meta;
}

// 3. Google Drive'dan Yerel Bilgisayara İndirme / Senkronizasyon
function syncDriveAudioToLocal() {
  log(`\n🔄 [Drive Senkronizasyon] Google Drive kontrol ediliyor: ${DRIVE_ROOT_DIR}...`);
  fs.mkdirSync(LOCAL_AUDIO_DIR, { recursive: true });

  if (!fs.existsSync(DRIVE_ROOT_DIR)) {
    log(`⚠️ Drive yolu bulunamadı (${DRIVE_ROOT_DIR}). Yalnızca yerel klasör kullanılacak: ${LOCAL_AUDIO_DIR}`);
    return [];
  }

  function scanDir(dir) {
    let results = [];
    try {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory()) {
          results = results.concat(scanDir(fullPath));
        } else if (/\.(m4a|mp3|wav|aac|ogg|flac)$/i.test(entry.name)) {
          results.push(fullPath);
        }
      }
    } catch (e) {
      log(`⚠️ Dizin okuma hatası (${dir}): ${e.message}`);
    }
    return results;
  }

  const driveFiles = scanDir(DRIVE_ROOT_DIR);
  log(`📡 Google Drive'da bulunan toplam ses kaydı: ${driveFiles.length}`);

  let downloadedCount = 0;
  const localSyncedFiles = [];

  for (const driveFile of driveFiles) {
    const relPath = path.relative(DRIVE_ROOT_DIR, driveFile);
    const localDest = path.join(LOCAL_AUDIO_DIR, relPath);
    const driveStat = fs.statSync(driveFile);

    let needsCopy = false;
    if (!fs.existsSync(localDest)) {
      needsCopy = true;
    } else {
      const localStat = fs.statSync(localDest);
      if (localStat.size !== driveStat.size) {
        needsCopy = true;
      }
    }

    if (needsCopy) {
      fs.mkdirSync(path.dirname(localDest), { recursive: true });
      log(`⬇️ [İndiriliyor] ${relPath} (${(driveStat.size / (1024 * 1024)).toFixed(1)} MB)...`);
      try {
        fs.copyFileSync(driveFile, localDest);
        downloadedCount++;
        log(`   ✅ Bilgisayara başarıyla indirildi: ${path.basename(localDest)}`);
      } catch (err) {
        log(`   ❌ İndirme hatası (${relPath}): ${err.message}`);
      }
    }

    if (fs.existsSync(localDest)) {
      localSyncedFiles.push(localDest);
    }
  }

  if (downloadedCount > 0) {
    log(`🎉 Google Drive'dan ${downloadedCount} yeni ses kaydı bilgisayara indirildi!`);
  } else {
    log(`✨ Google Drive ve yerel ses klasörü birebir senkronize.`);
  }

  return localSyncedFiles;
}

// Yerel Ses Klasörünü Tara
function scanLocalAudioFiles() {
  const dirsToScan = [LOCAL_AUDIO_DIR, path.join(process.env.HOME || process.env.USERPROFILE || '.', 'Desktop', 'Quick')];
  const foundMap = new Map();

  function scan(dir) {
    if (!fs.existsSync(dir)) return;
    try {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory()) {
          scan(fullPath);
        } else if (/\.(m4a|mp3|wav|aac|ogg|flac)$/i.test(entry.name)) {
          const size = fs.statSync(fullPath).size;
          // Exact duplicate detection (name + size)
          const key = `${entry.name}_${size}`;
          if (!foundMap.has(key)) {
            foundMap.set(key, { fullPath, name: entry.name, size });
          }
        }
      }
    } catch (_) {}
  }

  dirsToScan.forEach(scan);
  return Array.from(foundMap.values()).map(v => v.fullPath);
}

// 4. Tek Bir Ses Dosyasını Gemini API ile Transkribe Et
async function processSingleAudioFile(audioPath, ai, catalog, questionsDb, manifest) {
  const fileName = path.basename(audioPath);
  const fileId = path.basename(audioPath, path.extname(audioPath));
  const fileSizeMB = (fs.statSync(audioPath).size / (1024 * 1024)).toFixed(1);

  const durationSec = getM4aDuration(audioPath);
  const durationStr = durationSec ? `${(durationSec / 60).toFixed(1)} dk (${Math.round(durationSec)} sn)` : 'Bilinmiyor';

  log(`\n=======================================================`);
  log(`▶️ Ses Dosyası İşleniyor: ${fileName}`);
  log(`   📊 Boyut: ${fileSizeMB} MB | Süre: ${durationStr}`);
  log(`=======================================================`);

  // Aday ders ve çıkmış soru tespiti
  const candidate = findBestLectureCandidate(audioPath, catalog);
  const relatedQuestions = findMatchingPastQuestions(candidate, fileName, questionsDb, 4);

  log(`🔍 Tespit Edilen Ders Adayı: Kurul ${candidate.kurul} | ${candidate.discipline} | ${candidate.title}`);
  log(`🎯 İlgili Çıkmış Sınav Sorusu: ${relatedQuestions.length} adet bulundu.`);

  // 15'er dakikalık pencereler
  const windows = createTimeWindows(durationSec, 900);
  log(`⏱️ Zaman Pencereleri: Toplam ${windows.length} parça (${windows.map(w => `${w.startStr}-${w.endStr}`).join(', ')})`);

  // ASCII Safe Geçici Dosya
  const ext = path.extname(fileName).toLowerCase();
  const safeBase = toAsciiSafeName(path.basename(fileName, ext));
  const tmpUploadPath = path.join(os.tmpdir(), `meds_${Date.now()}_${safeBase}${ext}`);
  fs.copyFileSync(audioPath, tmpUploadPath);

  let uploadedFile = null;

  try {
    const mimeType = ext === '.m4a' ? 'audio/mp4' : 'audio/mpeg';

    for (let upAttempt = 1; upAttempt <= 3; upAttempt++) {
      try {
        log(`   ☁️ Gemini File API'ye yükleniyor (Deneme ${upAttempt}/3)...`);
        uploadedFile = await ai.files.upload({
          file: tmpUploadPath,
          config: {
            mimeType,
            displayName: `${safeBase}${ext}`
          }
        });
        if (uploadedFile?.name) break;
      } catch (upErr) {
        log(`   ⚠️ Yükleme hatası (${upErr.message}). ${15 * upAttempt} sn sonra tekrar denenecek...`);
        if (upAttempt === 3) throw upErr;
        await new Promise(r => setTimeout(r, 15 * upAttempt * 1000));
      }
    }

    log(`   ☁️ File URI: ${uploadedFile.uri} | Durum: ${uploadedFile.state}`);

    // Yükleme kontrolü
    let getFile = await ai.files.get({ name: uploadedFile.name });
    let retries = 0;
    while (getFile.state === 'PROCESSING' && retries < 60) {
      process.stdout.write('.');
      await new Promise(r => setTimeout(r, 4000));
      getFile = await ai.files.get({ name: uploadedFile.name });
      retries++;
    }

    if (getFile.state !== 'ACTIVE') {
      throw new Error(`Ses dosyası Gemini deposunda hazır hale gelemedi: ${getFile.state}`);
    }

    // Aşama 1: Ders Kimliği, Özet ve Amfi Sınav Hap Bilgileri
    log(`\n   🧠 Ders Kimliği, Özet ve Amfi Sınav Hap Bilgileri Çıkarılıyor...`);
    const metaPrompt = buildMetadataPrompt(candidate, fileName, relatedQuestions);
    let metaMarkdown = '';
    let parsedMeta = null;

    const candModels = [modelArg, modelArg === 'gemini-3.5-flash-lite' ? 'gemini-3.8-flash' : 'gemini-3.5-flash-lite'];
    let activeModel = modelArg;

    for (let attempt = 1; attempt <= 3; attempt++) {
      const curMod = candModels[(attempt - 1) % candModels.length];
      try {
        const metaRes = await ai.models.generateContent({
          model: curMod,
          contents: [
            { fileData: { fileUri: getFile.uri, mimeType: getFile.mimeType || mimeType } },
            metaPrompt
          ],
          config: {
            temperature: 0.2,
            maxOutputTokens: 2500
          }
        });
        metaMarkdown = extractResponseText(metaRes);
        if (metaMarkdown && metaMarkdown.length > 50) {
          parsedMeta = parseMarkdownMetadata(metaMarkdown);
          activeModel = curMod;
          break;
        }
      } catch (metaErr) {
        const isQuota = metaErr.message?.includes('429') || metaErr.message?.includes('RESOURCE_EXHAUSTED') || metaErr.message?.includes('503') || metaErr.message?.includes('UNAVAILABLE');
        if (isQuota) {
          const waitSec = 20 * attempt;
          log(`   ⚠️ Kota/Yoğunluk uyarısı (${curMod})! ${waitSec} saniye bekleniyor...`);
          await new Promise(r => setTimeout(r, waitSec * 1000));
        } else {
          log(`   ⚠️ Meta analizi uyarısı: ${metaErr.message}`);
          break;
        }
      }
    }

    if (!metaMarkdown) {
      metaMarkdown = `# 🩺 ${candidate.title}\n\n> **Kurul:** Kurul ${candidate.kurul}\n> **Disiplin:** ${candidate.discipline}\n> **Kaynak:** \`${fileName}\`\n\n---\n\n## 📌 Dersin Genel Özeti\n${candidate.title} ders kaydı.`;
    }

    log(`   ✅ Ders Kimliği Çıkarıldı: ${parsedMeta?.lectureTitle || candidate.title} (${parsedMeta?.discipline || candidate.discipline})`);

    // Güvenlik beklemesi
    await new Promise(r => setTimeout(r, Math.max(3, delayArg) * 1000));

    // Aşama 2: 15'er Dakikalık Dilimler Halinde Kesintisiz Verbatim Transkripsiyon
    const segmentTexts = [];

    for (const win of windows) {
      log(`\n   🎙️ Parça Transkribe Ediliyor [${win.index}/${win.total}]: ${win.startStr} - ${win.endStr}...`);
      const prompt = buildVerbatimSegmentPrompt(fileName, win);

      let windowSuccess = false;
      let windowText = '';

      for (let attempt = 1; attempt <= 4; attempt++) {
        const curMod = candModels[(attempt - 1) % candModels.length];
        try {
          const response = await ai.models.generateContent({
            model: curMod,
            contents: [
              { fileData: { fileUri: getFile.uri, mimeType: getFile.mimeType || mimeType } },
              prompt
            ],
            config: {
              temperature: 0.1,
              maxOutputTokens: 8192
            }
          });
          windowText = extractResponseText(response);
          if (windowText && windowText.length > 50) {
            windowSuccess = true;
            activeModel = curMod;
            break;
          }
        } catch (genErr) {
          const isQuota = genErr.message?.includes('429') || genErr.message?.includes('RESOURCE_EXHAUSTED') || genErr.message?.includes('503') || genErr.message?.includes('UNAVAILABLE');
          if (isQuota) {
            const waitSec = 20 * attempt;
            log(`   ⚠️ Kota/Yoğunluk uyarısı (${curMod})! Alternatif modele geçiliyor, ${waitSec} sn bekleniyor...`);
            await new Promise(r => setTimeout(r, waitSec * 1000));
          } else {
            log(`   ⚠️ Parça üretim uyarısı (${curMod}): ${genErr.message}`);
            await new Promise(r => setTimeout(r, 10000));
          }
        }
      }

      if (!windowSuccess || !windowText) {
        throw new Error(`Parça (${win.startStr}-${win.endStr}) transkribe edilemedi.`);
      }

      log(`   ✅ Parça Tamamlandı: ${windowText.length} karakter, ${windowText.split('\n').length} satır`);
      segmentTexts.push(windowText);

      if (!win.isLast) {
        log(`   ⏱️ Parça arası güvenlik beklemesi (${delayArg} sn)...`);
        await new Promise(r => setTimeout(r, delayArg * 1000));
      }
    }

    // Parçaları birleştir
    const transcriptSections = segmentTexts.map((txt, idx) => {
      const win = windows[idx];
      return `### Bölüm ${win.index} (${win.startStr} - ${win.endStr})\n\n${txt}`;
    });

    const finalMarkdown = `${metaMarkdown}

---

## 📝 Tam Ders Transkripti (Dakika Dakika Eksiksiz)

${transcriptSections.join('\n\n---\n\n')}
`;

    // Markdown Çıktısını Kaydet
    const safeTitle = toAsciiSafeName(parsedMeta?.lectureTitle || candidate.title || fileName.replace(/\.[^/.]+$/, ''));
    const outMdPath = path.join(TRANSCRIPTION_OUT_DIR, `${safeTitle}_Transkript.md`);
    fs.writeFileSync(outMdPath, finalMarkdown, 'utf8');

    log(`\n🎉 EKSİKSİZ TRANSKRİPT KAYDEDİLDİ: ${path.basename(outMdPath)}`);
    log(`   📏 Toplam Boyut: ${finalMarkdown.length} karakter, ${finalMarkdown.split('\n').length} satır`);
    log(`   🎓 Ders: ${parsedMeta?.lectureTitle || candidate.title} (${parsedMeta?.discipline || candidate.discipline})`);
    log(`   👨‍🏫 Hoca: ${parsedMeta?.instructor || 'Belirtilmedi'}`);

    // Manifest Güncelle
    manifest[fileId] = {
      audioFileName: fileName,
      fileSizeMB: parseFloat(fileSizeMB),
      totalDurationMinutes: durationSec ? parseFloat((durationSec / 60).toFixed(1)) : null,
      windowsCount: windows.length,
      markdownFile: path.basename(outMdPath),
      totalCharacters: finalMarkdown.length,
      lectureTitle: parsedMeta?.lectureTitle || candidate.title,
      committee: parsedMeta?.committee || `Kurul ${candidate.kurul}`,
      discipline: parsedMeta?.discipline || candidate.discipline,
      instructor: parsedMeta?.instructor || 'Belirtilmedi',
      confidence: parsedMeta?.confidence || candidate.confidence,
      relatedQuestionsCount: relatedQuestions.length,
      modelUsed: modelArg,
      status: 'completed',
      processedAt: new Date().toISOString()
    };

    fs.writeFileSync(MANIFEST_PATH, JSON.stringify(manifest, null, 2), 'utf8');
    return true;

  } catch (err) {
    log(`❌ Hata (${fileName}): ${err.message}`);
    manifest[fileId] = {
      audioFileName: fileName,
      status: 'error',
      errorMessage: err.message,
      attemptedAt: new Date().toISOString()
    };
    fs.writeFileSync(MANIFEST_PATH, JSON.stringify(manifest, null, 2), 'utf8');
    return false;
  } finally {
    // Geçici dosyaları temizle
    if (fs.existsSync(tmpUploadPath)) {
      try { fs.unlinkSync(tmpUploadPath); } catch (_) {}
    }
    if (uploadedFile) {
      try {
        await ai.files.delete({ name: uploadedFile.name });
        log(`   🧹 Gemini File API geçici depolaması temizlendi.`);
      } catch (_) {}
    }
  }
}

// 5. Bir Tarama Döngüsü (Drive Senkronize Et -> Transkribe Edilecekleri Belirle -> İşle)
async function runSingleCycle(ai, catalog, questionsDb) {
  // A) Drive'dan bilgisayara indir
  syncDriveAudioToLocal();

  // B) Yerel ses kayıtlarını listele
  const allAudioFiles = scanLocalAudioFiles();

  // C) Manifesti oku
  let manifest = {};
  if (fs.existsSync(MANIFEST_PATH)) {
    try {
      manifest = JSON.parse(fs.readFileSync(MANIFEST_PATH, 'utf8'));
    } catch (_) {
      manifest = {};
    }
  }

  // D) Henüz işlenmemiş dosyaları filtrele
  const filesToProcess = [];
  for (const fPath of allAudioFiles) {
    const fName = path.basename(fPath);
    const stem = path.basename(fPath, path.extname(fPath));
    const isDone = !isForce && (
      (manifest[stem]?.status === 'completed' && manifest[stem]?.totalDurationMinutes) ||
      Object.values(manifest).some(v => (v.audioFileName === fName || v.filename === fName) && v.status === 'completed')
    );

    if (!isDone) {
      filesToProcess.push(fPath);
    }
  }

  if (filesToProcess.length === 0) {
    log(`💤 [Beklemede] İşlenecek yeni ses kaydı yok. Tüm dosyalar güncel.`);
    return 0;
  }

  log(`\n🎯 İŞLENECEK YENİ SES DOSYASI SAYISI: ${filesToProcess.length}`);
  filesToProcess.forEach((f, idx) => log(`   ${idx + 1}. ${path.basename(f)}`));

  // Boyuta göre sırala (küçükten büyüğe)
  filesToProcess.sort((a, b) => fs.statSync(a).size - fs.statSync(b).size);

  let successCount = 0;
  for (let i = 0; i < filesToProcess.length; i++) {
    if (limitArg > 0 && successCount >= limitArg) {
      log(`🛑 Limit sınırına (${limitArg}) ulaşıldı.`);
      break;
    }

    const currentFile = filesToProcess[i];
    log(`\n⏳ [${i + 1}/${filesToProcess.length}] Başlatılıyor: ${path.basename(currentFile)}`);

    const ok = await processSingleAudioFile(currentFile, ai, catalog, questionsDb, manifest);
    if (ok) {
      successCount++;
    }

    // Dosyalar arası güvenlik beklemesi
    if (i < filesToProcess.length - 1) {
      log(`⏱️ Sıradaki dosya öncesi kota koruması beklemesi (${delayArg} sn)...`);
      await new Promise(r => setTimeout(r, delayArg * 1000));
    }
  }

  log(`\n✨ Döngü Tamamlandı: ${successCount} ses dosyası başarıyla transkribe edildi.`);
  return successCount;
}

// 6. Ana Giriş Fonksiyonu
async function main() {
  log('=================================================================');
  log('🩺 MedSoru - Tıbbi Amfi Ses Kayıtları Tam Transkripsiyon & İzleme');
  log(`⚡ Mod: ${isWatchMode ? '🛡️ Kalıcı Otomatik İzleyici (Watcher Daemon)' : '⚡ Tek Seferlik Senkronizasyon ve İşlem'}`);
  log(`🤖 Tercih Edilen Model: ${modelArg} (1M Token Çok Modlu)`);
  log('=================================================================');

  if (!GEMINI_API_KEY) {
    log('❌ [Hata] GEMINI_API_KEY ortam değişkeni veya .env içinde tanımlı değil!');
    process.exit(1);
  }

  // Veritabanı ve katalogları yükle
  const catalog = loadSummariesCatalog();
  const questionsDb = loadPastQuestionsDatabase();
  const ai = new GoogleGenAI({ apiKey: GEMINI_API_KEY });

  if (!isWatchMode) {
    // Tek seferlik tam çalıştırma
    await runSingleCycle(ai, catalog, questionsDb);
    log('🏁 Tek seferlik transkripsiyon işlemi sonlandı.');
    return;
  }

  // Kalıcı Watcher Modu
  log(`\n👀 [Watcher Aktif] Her ${watchIntervalSec} saniyede bir Google Drive kontrol edilecek...`);
  log(`📁 Transkript Çıktıları: ${TRANSCRIPTION_OUT_DIR}`);
  log(`📜 Log Dosyası: ${WATCHER_LOG_PATH}`);

  while (true) {
    try {
      await runSingleCycle(ai, catalog, questionsDb);
    } catch (cycleErr) {
      log(`⚠️ Watcher döngü hatası (kurtarılıyor): ${cycleErr.message}`);
    }

    log(`⏱️ Sonraki kontrol ${watchIntervalSec} saniye sonra...`);
    await new Promise(r => setTimeout(r, watchIntervalSec * 1000));
  }
}

main().catch(err => {
  log(`💥 Kritik Başlatma Hatası: ${err.message}`);
  process.exit(1);
});
