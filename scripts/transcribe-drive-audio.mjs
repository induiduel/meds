#!/usr/bin/env node

/**
 * scripts/transcribe-drive-audio.mjs
 * 
 * MedSoru Tıbbi Amfi Ses Kayıtları Transkripsiyon ve Ders Eşleştirme Motoru
 * ------------------------------------------------------------------------
 * Google Gemini (3.5 Flash-Lite & 3.8 Flash) ile:
 *   1. Amfi ses kayıtlarını (.m4a, .mp3, .wav) TÜM DAKİKALARIYLA (dakika dakika) transkribe eder.
 *   2. 25 dakikadan uzun kayıtları otomatik zaman pencerelerine (00:00-20:00, 20:00-40:00 vb.) bölerek
 *      token sınırlarına takılmadan ve hiçbir cümleyi atlamadan %100 eksiksiz (verbatim) işler.
 *   3. Tıp müfredatı (Karabük Tıp Dönem 3) ve 347 ders özeti kataloğunu
 *      kullanarak ses dosyasının GERÇEKTE hangi Kurula, hangi Disipline ve hangi
 *      Ders Başlığına ait olduğunu tespit eder.
 *   4. Tıbbi literatür ve doğru tıbbi terminoloji (Latince anatomik yapılar, patoloji,
 *      mikrobiyoloji, farmakoloji) ile fonetik bozulmaları engeller.
 *   5. Amfi sınav ve TUS hap bilgilerini (High-Yield Pearls) özel kutularda özetler.
 *   6. Kota ve Hız Limiti Yönetimi (Rate Limiting, RPM/TPM koruması, 429 backoff).
 *   7. Kaldığı yerden devam edebilen yapılandırılmış manifest (transcription_manifest.json).
 */

import fs from 'fs';
import path from 'path';
import os from 'os';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';
import { GoogleGenAI } from '@google/genai';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');
const BASE_DATABASE_DIR = process.env.MEDS_DATABASE_DIR || 'C:\\Users\\indui\\Desktop\\meds_database';

// Varsayılan Arama Yolları
const DEFAULT_AUDIO_DIRS = [
  'C:\\Users\\indui\\Desktop\\Quick',
  path.join(BASE_DATABASE_DIR, 'ses_kayitlari'),
  path.join(ROOT_DIR, 'audio')
];

const TRANSCRIPTION_OUT_DIR = path.join(BASE_DATABASE_DIR, 'transcriptions');
const MANIFEST_PATH = path.join(TRANSCRIPTION_OUT_DIR, 'transcription_manifest.json');
const SUMMARIES_CATALOG_PATH = path.join(ROOT_DIR, 'src', 'data', 'summaries_meta.json');

// CLI Parametreleri
const args = process.argv.slice(2);
const customInputArg = args.find(a => a.startsWith('--input='))?.split('=')[1] || null;
const modelArg = args.find(a => a.startsWith('--model='))?.split('=')[1] || 'gemini-3.5-flash-lite';
const delayArg = parseInt(args.find(a => a.startsWith('--delay='))?.split('=')[1] || '6', 10);
const isForce = args.includes('--force') || args.includes('-f');
const limitArg = parseInt(args.find(a => a.startsWith('--limit='))?.split('=')[1] || '0', 10);

const GEMINI_API_KEY = process.env.GEMINI_API_KEY || process.env.GOOGLE_API_KEY || '';

// M4A / MP4 Süre Okuyucu (mvhd atomu)
function getM4aDuration(filePath) {
  try {
    const fd = fs.openSync(filePath, 'r');
    const stat = fs.fstatSync(fd);
    const size = stat.size;
    const buf = Buffer.alloc(Math.min(size, 6 * 1024 * 1024));
    // Sona bak (moov atomu genellikle sondadır)
    fs.readSync(fd, buf, 0, buf.length, Math.max(0, size - buf.length));
    let idx = buf.indexOf('mvhd');
    if (idx === -1) {
      // Başa bak
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

// Zaman Pencereleri Üretici (15'er dakikalık güvenli dilimler)
function createTimeWindows(durationSeconds, windowSizeSec = 900) {
  if (!durationSeconds || durationSeconds <= 900) {
    // 15 dk ve altı tek parça işlenebilir
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

// ASCII Güvenli İsim Dönüştürücü (HTTP Header ve File API ByteString hatasını önler)
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

function loadSummariesCatalog() {
  if (fs.existsSync(SUMMARIES_CATALOG_PATH)) {
    try {
      const data = JSON.parse(fs.readFileSync(SUMMARIES_CATALOG_PATH, 'utf8'));
      console.log(`📚 ${data.length} Ders Özeti Kataloğu Yüklendi.`);
      return data;
    } catch (e) {
      console.warn('⚠️ summaries_meta.json okunamadı:', e.message);
    }
  }
  return [];
}

function findBestLectureCandidate(fileName, catalog) {
  const cleanName = normalizeText(path.basename(fileName, path.extname(fileName)));
  const words = cleanName.split(' ').filter(w => w.length > 2);

  let best = null;
  let maxScore = 0;

  for (const item of catalog) {
    const target = normalizeText(`${item.discipline || ''} ${item.title || ''} ${(item.keyPoints || []).join(' ')}`);
    let score = 0;
    for (const w of words) {
      if (target.includes(w)) score++;
    }
    if (score > maxScore) {
      maxScore = score;
      best = item;
    }
  }

  if (best && maxScore >= 2) {
    return {
      committeeId: best.committeeId || 'donem3-kurul1',
      kurul: best.kurul || 1,
      discipline: best.discipline,
      title: best.title,
      keyPoints: best.keyPoints || [],
      confidence: maxScore >= 4 ? 'Yüksek' : 'Orta'
    };
  }

  // Varsayılan Kurul 1 Heuristiği
  let disc = 'Tıp Fakültesi';
  if (cleanName.includes('genetik')) disc = 'Tıbbi Genetik';
  else if (cleanName.includes('uroloji')) disc = 'Üroloji';
  else if (cleanName.includes('enfeksiyon')) disc = 'Enfeksiyon Hastalıkları';
  else if (cleanName.includes('halk')) disc = 'Halk Sağlığı';
  else if (cleanName.includes('patoloji')) disc = 'Tıbbi Patoloji';

  return {
    committeeId: 'donem3-kurul1',
    kurul: 1,
    discipline: disc,
    title: path.basename(fileName, path.extname(fileName)),
    keyPoints: [],
    confidence: 'Ön Sezgisel'
  };
}

function buildMetadataPrompt(candidate, fileName) {
  const kpStr = candidate.keyPoints && candidate.keyPoints.length > 0
    ? candidate.keyPoints.map(k => `- ${k}`).join('\n')
    : 'Mevcut değil';

  return `Sen Karabük Üniversitesi Tıp Fakültesi Dönem 3 amfi dersleri ve klinik müfredat uzmanısın.
SES DOSYASI: ${fileName}
Ön Eşleştirme (Aday Ders): ${candidate.discipline} - ${candidate.title}
Tıbbi Referans İpuçları:
${kpStr}

GÖREVLERİN:
1. Ses kaydının başındaki konuşmalardan, hoca hitabından ve ders konusundan hareketle dersin gerçek kimliğini tespit et:
   - Gerçek Dönem 3 Kurulu (Kurul 1-6)
   - Tıp Disiplini (örn. Halk Sağlığı, Tıbbi Genetik, Üroloji, Patoloji, vb.)
   - Resmi Ders Adı
   - Öğretim Üyesi (Hocanın Adı)
2. Dersin genel özetini ve işlenen temel kavramları çıkar.
3. Amfi ve sınav için en kritik hap bilgileri (High-Yield Pearls) listele.

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

## ⭐ Amfi & Sınav Hap Bilgileri (High-Yield Pearls)
- **[Kavram 1]:** [Hocanın özellikle sınav için uyardığı kritik nokta]
- **[Kavram 2]:** [Klinik / TUS ipucu]
- **[Kavram 3]:** ...
`;
}

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

async function main() {
  console.log('=================================================================');
  console.log('🩺 MedSoru - Tıbbi Amfi Ses Kayıtları Tam Transkripsiyon Motoru');
  console.log('⚡ Özellik: Tüm Dakikaları Kapsayan Kesintisiz Verbatim Çözümleme');
  console.log(`🤖 Tercih Edilen Model: ${modelArg} (1M Token Çok Modlu)`);
  console.log('=================================================================');

  if (!GEMINI_API_KEY) {
    console.error('\n❌ [Hata] GEMINI_API_KEY tanımlı değil!');
    console.error('Lütfen .env dosyasına ekleyin veya PowerShell üzerinden tanımlayın:');
    console.error('  $env:GEMINI_API_KEY="AIzaSy..."\n');
    process.exit(1);
  }

  // 1. Ses Kaynak Klasörünü Bul
  let audioDir = customInputArg;
  if (!audioDir || !fs.existsSync(audioDir)) {
    for (const d of DEFAULT_AUDIO_DIRS) {
      if (fs.existsSync(d)) {
        const files = fs.readdirSync(d);
        if (files.some(f => /\.(m4a|mp3|wav|aac|ogg|flac)$/i.test(f))) {
          audioDir = d;
          break;
        }
      }
    }
  }

  if (!audioDir || !fs.existsSync(audioDir)) {
    console.error('❌ [Hata] Ses kayıtlarının bulunduğu klasör bulunamadı!');
    console.error('Lütfen geçerli bir yol belirtin: node scripts/transcribe-drive-audio.mjs --input="C:\\Klasor"');
    process.exit(1);
  }

  console.log(`📂 Ses Klasörü: ${audioDir}`);

  // 2. Çıktı Klasörünü Hazırla
  if (!fs.existsSync(TRANSCRIPTION_OUT_DIR)) {
    fs.mkdirSync(TRANSCRIPTION_OUT_DIR, { recursive: true });
  }
  console.log(`💾 Transkript Klasörü: ${TRANSCRIPTION_OUT_DIR}`);

  // 3. Manifesti Oku
  let manifest = {};
  if (fs.existsSync(MANIFEST_PATH) && !isForce) {
    try {
      manifest = JSON.parse(fs.readFileSync(MANIFEST_PATH, 'utf8'));
    } catch (e) {
      manifest = {};
    }
  }

  // 4. Katalog Yükle
  const catalog = loadSummariesCatalog();

  // 5. Ses Dosyalarını Topla ve Boyuta Göre Sırala
  const supportedExts = new Set(['.m4a', '.mp3', '.wav', '.aac', '.ogg', '.flac']);
  const allFiles = fs.readdirSync(audioDir);
  const audioFiles = allFiles
    .filter(f => supportedExts.has(path.extname(f).toLowerCase()))
    .map(f => path.join(audioDir, f))
    .sort((a, b) => fs.statSync(a).size - fs.statSync(b).size);

  if (audioFiles.length === 0) {
    console.log(`⚠️ Klasörde desteklenen formatta ses dosyası bulunamadı: ${audioDir}`);
    process.exit(0);
  }

  console.log(`🎯 Bulunan Ses Kaydı Sayısı: ${audioFiles.length}`);

  // 6. Gemini İstemcisi
  const ai = new GoogleGenAI({ apiKey: GEMINI_API_KEY });

  let processedCount = 0;

  for (let i = 0; i < audioFiles.length; i++) {
    if (limitArg > 0 && processedCount >= limitArg) {
      console.log(`\n🛑 Limit sınırına (${limitArg}) ulaşıldı, işlem tamamlandı.`);
      break;
    }

    const audioPath = audioFiles[i];
    const fileName = path.basename(audioPath);
    const fileId = path.basename(audioPath, path.extname(audioPath));
    const fileSizeMB = (fs.statSync(audioPath).size / (1024 * 1024)).toFixed(1);

    // Süre tespiti
    const durationSec = getM4aDuration(audioPath);
    const durationStr = durationSec ? `${(durationSec / 60).toFixed(1)} dk (${Math.round(durationSec)} sn)` : 'Bilinmiyor';

    if (!isForce && manifest[fileId]?.status === 'completed' && manifest[fileId]?.totalDurationMinutes) {
      console.log(`\n⏩ [${i + 1}/${audioFiles.length}] Zaten Tamamlandı (Atlandı): ${fileName}`);
      continue;
    }

    console.log(`\n=======================================================`);
    console.log(`▶️ [${i + 1}/${audioFiles.length}] İşleniyor: ${fileName}`);
    console.log(`   📊 Boyut: ${fileSizeMB} MB | Süre: ${durationStr}`);
    console.log(`=======================================================`);

    const candidate = findBestLectureCandidate(fileName, catalog);
    console.log(`🔍 Ön Tespit: Kurul ${candidate.kurul} | ${candidate.discipline} | ${candidate.title}`);

    // Zaman pencerelerini hesapla
    const windows = createTimeWindows(durationSec, 900); // 15'er dakikalık pencereler
    console.log(`⏱️ Zaman Pencereleri: Toplam ${windows.length} parça (${windows.map(w => `${w.startStr}-${w.endStr}`).join(', ')})`);

    // ASCII Safe Geçici Dosya
    const ext = path.extname(fileName).toLowerCase();
    const safeBase = toAsciiSafeName(path.basename(fileName, ext));
    const tmpUploadPath = path.join(os.tmpdir(), `meds_${Date.now()}_${safeBase}${ext}`);
    fs.copyFileSync(audioPath, tmpUploadPath);

    let uploadedFile = null;

    try {
      console.log(`   ☁️ File API'ye yükleniyor...`);
      const mimeType = ext === '.m4a' ? 'audio/mp4' : 'audio/mpeg';

      uploadedFile = await ai.files.upload({
        file: tmpUploadPath,
        config: {
          mimeType,
          displayName: `${safeBase}${ext}`
        }
      });

      console.log(`   ☁️ File URI: ${uploadedFile.uri} | Durum: ${uploadedFile.state}`);

      // Durum Kontrolü
      let getFile = await ai.files.get({ name: uploadedFile.name });
      let retries = 0;
      while (getFile.state === 'PROCESSING' && retries < 60) {
        process.stdout.write('.');
        await new Promise(r => setTimeout(r, 4000));
        getFile = await ai.files.get({ name: uploadedFile.name });
        retries++;
      }

      if (getFile.state !== 'ACTIVE') {
        throw new Error(`Dosya işlenemedi. Durum: ${getFile.state}`);
      }

      // Adım 1: Ders Bilgileri, Özet ve Amfi Sınav Hap Bilgileri
      console.log(`\n   🧠 Ders Kimliği, Özet ve Amfi Sınav Hap Bilgileri Çıkarılıyor...`);
      const metaPrompt = buildMetadataPrompt(candidate, fileName);
      let metaMarkdown = '';
      let parsedMeta = null;

      for (let attempt = 1; attempt <= 2; attempt++) {
        try {
          const metaRes = await ai.models.generateContent({
            model: modelArg,
            contents: [
              { fileData: { fileUri: getFile.uri, mimeType: getFile.mimeType || mimeType } },
              metaPrompt
            ],
            config: {
              temperature: 0.2,
              maxOutputTokens: 2048
            }
          });
          metaMarkdown = extractResponseText(metaRes);
          if (metaMarkdown && metaMarkdown.length > 50) {
            parsedMeta = parseMarkdownMetadata(metaMarkdown);
            break;
          }
        } catch (metaErr) {
          const isQuota = metaErr.message?.includes('429') || metaErr.message?.includes('RESOURCE_EXHAUSTED');
          if (isQuota) {
            const waitSec = 35 * attempt;
            console.warn(`   ⚠️ Kota (429) uyarısı! ${waitSec} saniye bekleniyor...`);
            await new Promise(r => setTimeout(r, waitSec * 1000));
          } else {
            console.warn(`   ⚠️ Meta çıkarma uyarısı:`, metaErr.message);
            break;
          }
        }
      }

      if (!metaMarkdown) {
        metaMarkdown = `# 🩺 ${candidate.title}\n\n> **Kurul:** Kurul ${candidate.kurul}\n> **Disiplin:** ${candidate.discipline}\n> **Kaynak:** \`${fileName}\`\n\n---\n\n## 📌 Dersin Genel Özeti\n${candidate.title} ders kaydı.`;
      }

      console.log(`   ✅ Ders Kimliği: ${parsedMeta?.lectureTitle || candidate.title} (${parsedMeta?.discipline || candidate.discipline})`);

      // Kısa ara
      await new Promise(r => setTimeout(r, Math.max(3, delayArg) * 1000));

      // Adım 2: Pencereleri sırayla transkribe et (Saf Verbatim)
      const segmentTexts = [];

      for (const win of windows) {
        console.log(`\n   🎙️ Parça Transkribe Ediliyor [${win.index}/${win.total}]: ${win.startStr} - ${win.endStr}...`);
        const prompt = buildVerbatimSegmentPrompt(fileName, win);

        let windowSuccess = false;
        let windowText = '';

        for (let attempt = 1; attempt <= 2; attempt++) {
          try {
            const response = await ai.models.generateContent({
              model: modelArg,
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
              break;
            }
          } catch (genErr) {
            const isQuota = genErr.message?.includes('429') || genErr.message?.includes('RESOURCE_EXHAUSTED');
            if (isQuota) {
              const waitSec = 35 * attempt;
              console.warn(`   ⚠️ Kota (429) uyarısı! ${waitSec} saniye bekleniyor...`);
              await new Promise(r => setTimeout(r, waitSec * 1000));
            } else {
              throw genErr;
            }
          }
        }

        if (!windowSuccess || !windowText) {
          throw new Error(`Parça (${win.startStr}-${win.endStr}) transkribe edilemedi.`);
        }

        console.log(`   ✅ Parça Tamamlandı: ${windowText.length} karakter, ${windowText.split('\n').length} satır`);
        segmentTexts.push(windowText);

        // Pencere arası kota koruma beklemesi
        if (!win.isLast) {
          console.log(`   ⏱️ Parça arası güvenlik beklemesi (${delayArg} sn)...`);
          await new Promise(r => setTimeout(r, delayArg * 1000));
        }
      }

      // Parçaları biçimlendir ve birleştir
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

      console.log(`\n🎉 EKSİKSİZ TRANSKRİPT KAYDEDİLDİ: ${path.basename(outMdPath)}`);
      console.log(`   📏 Toplam Boyut: ${finalMarkdown.length} karakter, ${finalMarkdown.split('\n').length} satır`);
      console.log(`   🎓 Ders: ${parsedMeta?.lectureTitle || candidate.title} (${parsedMeta?.discipline || candidate.discipline})`);
      console.log(`   👨‍🏫 Hoca: ${parsedMeta?.instructor || 'Belirtilmedi'}`);

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
        modelUsed: modelArg,
        status: 'completed',
        processedAt: new Date().toISOString()
      };

      fs.writeFileSync(MANIFEST_PATH, JSON.stringify(manifest, null, 2), 'utf8');
      processedCount++;

      // Dosyalar arası güvenlik beklemesi
      console.log(`   ⏱️ Sıradaki dosya öncesi kota koruması (${delayArg} sn)...`);
      await new Promise(r => setTimeout(r, delayArg * 1000));

    } catch (err) {
      console.error(`❌ Hata (${fileName}):`, err.message);
      manifest[fileId] = {
        audioFileName: fileName,
        status: 'error',
        errorMessage: err.message,
        attemptedAt: new Date().toISOString()
      };
      fs.writeFileSync(MANIFEST_PATH, JSON.stringify(manifest, null, 2), 'utf8');
    } finally {
      // Geçici dosyaları temizle
      if (fs.existsSync(tmpUploadPath)) {
        try { fs.unlinkSync(tmpUploadPath); } catch (_) {}
      }
      if (uploadedFile) {
        try {
          await ai.files.delete({ name: uploadedFile.name });
          console.log(`   🧹 File API geçici depolaması temizlendi.`);
        } catch (_) {}
      }
    }
  }

  console.log('\n=======================================================');
  console.log(`🎉 İşlem Tamamlandı! Toplam ${processedCount} ses kaydı tam transkribe edildi.`);
  console.log(`📁 Transkriptler: ${TRANSCRIPTION_OUT_DIR}`);
  console.log(`📋 Manifest: ${MANIFEST_PATH}`);
  console.log('=======================================================');
}

main().catch(err => {
  console.error('Kritik Hata:', err);
  process.exit(1);
});
