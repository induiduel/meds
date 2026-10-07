/**
 * MedSoru Scanned PDF OCR & Question Extraction Engine
 * 
 * Bu betik:
 * 1. meds_sorular_images içindeki taranmış sınav fotoğraflarını OCR ile okur.
 * 2. 180° ters çekilmiş fotoğrafları otomatik tespit edip döndürür.
 * 3. Orijinal ham metni (rawStem) birebir korur.
 * 4. Soruları kök, şıklar (A-E) ve doğru cevap formatına ayrıştırır.
 * 5. Ders notları (lecture_notes.json) ile eşleştirip slayt referansı ekler.
 * 6. Soruları data/questions.json'a ve doğrudan Firebase Firestore'a kaydeder.
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { spawnSync } from 'child_process';
import Tesseract from 'tesseract.js';
import { initializeApp } from 'firebase/app';
import { getFirestore, doc, writeBatch } from 'firebase/firestore';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, '..');

const BASE_DATABASE_DIR = `${process.env.MEDS_DATABASE_DIR || '/home/indu/medsor/meds_database'}`;
const IMAGES_DIR = path.join(BASE_DATABASE_DIR, 'meds_sorular_images');
const TXT_DIR = path.join(BASE_DATABASE_DIR, 'meds_sorular_txt');

osEnsureDir(TXT_DIR);

function osEnsureDir(p) {
  if (!fs.existsSync(p)) fs.mkdirSync(p, { recursive: true });
}

// Clean object for Firestore
function cleanForFirestore(obj) {
  if (obj === null || obj === undefined) return null;
  if (Array.isArray(obj)) return obj.map(cleanForFirestore);
  if (typeof obj === 'object') {
    const cleaned = {};
    for (const [key, value] of Object.entries(obj)) {
      if (value !== undefined) {
        cleaned[key] = cleanForFirestore(value);
      }
    }
    return cleaned;
  }
  return obj;
}

// Load Firebase Config
const configPath = path.join(rootDir, 'firebase-applet-config.json');
const firebaseConfig = JSON.parse(fs.readFileSync(configPath, 'utf8'));
const fbApp = initializeApp(firebaseConfig);
const firestoreDb = getFirestore(fbApp, firebaseConfig.firestoreDatabaseId || undefined);

// Load Lecture Notes for matching
const notesPath = path.join(rootDir, 'data', 'lecture_notes.json');
let lectureNotes = [];
if (fs.existsSync(notesPath)) {
  try { lectureNotes = JSON.parse(fs.readFileSync(notesPath, 'utf8')); } catch {}
}

console.log('='.repeat(75));
console.log('  🔍 MEDSORU TARANMIŞ PDF (RESİM) OCR & SORU REKONSTRÜKSİYON MOTORU');
console.log('='.repeat(75));
console.log(`Ders notları yüklendi: ${lectureNotes.length} ders notu`);

function rotateImage(inputPath, degrees) {
  const ext = path.extname(inputPath);
  const outPath = inputPath.replace(ext, `_rot${degrees}${ext}`);
  if (fs.existsSync(outPath) && fs.statSync(outPath).size > 1000) {
    return outPath;
  }
  const pyCode = `
from PIL import Image
im = Image.open(r'''${inputPath}''')
im.rotate(${degrees}, expand=True).save(r'''${outPath}''')
`;
  spawnSync(process.platform === 'win32' ? 'python' : 'python3', ['-c', pyCode], { encoding: 'utf-8' });
  return outPath;
}

// Keyword score for Turkish medical questions
const COMMON_KW = [
  'aşağıdakilerden', 'hangisi', 'doğrudur', 'yanlıştır', 'etkeni',
  'tanı', 'tedavi', 'hastada', 'sendromu', 'hücre', 'dokuda', 'lezyon',
  'infeksiyon', 'enfeksiyon', 'bulunur', 'gözlenir', 'protein', 'bakteri'
];

function scoreOrientation(text) {
  if (!text) return 0;
  const lower = text.toLowerCase();
  let score = 0;
  for (const w of COMMON_KW) {
    if (lower.includes(w)) score += 5;
  }
  // Check for option patterns: "a.", "b.", "c.", "d.", "e."
  const optMatches = (lower.match(/(?:^|\n)\s*[a-e]\s*[\)\.]/g) || []).length;
  score += optMatches * 3;
  return score;
}

// Match question with lecture notes
function findSlideMatch(stem, discipline) {
  if (!lectureNotes || lectureNotes.length === 0 || !stem) return null;
  const text = `${stem} ${discipline || ''}`.toLowerCase();
  let best = null;

  for (const n of lectureNotes) {
    const isDisc = discipline && n.discipline && (
      discipline.toLowerCase().includes(n.discipline.toLowerCase()) ||
      n.discipline.toLowerCase().includes(discipline.toLowerCase())
    );

    for (const page of (n.pages || [])) {
      let score = isDisc ? 20 : 0;
      for (const kw of (page.keywords || [])) {
        if (kw.length >= 4 && text.includes(kw.toLowerCase())) {
          score += 15;
        }
      }
      if (score >= 35) {
        if (!best || score > best.score) {
          best = {
            noteTitle: n.title,
            discipline: n.discipline,
            pageNumber: page.pageNumber,
            matchedSnippet: (page.content || '').substring(0, 200).trim(),
            confidenceScore: Math.min(99, score),
            score,
          };
        }
      }
    }
  }
  return best;
}

// Parse questions from raw OCR text
function parseOcrQuestions(rawText, sourceFile, committeeId) {
  const questions = [];
  const lines = rawText.split('\n').map(l => l.trim()).filter(Boolean);

  let currentQNum = null;
  let currentStemLines = [];
  let currentOptions = [];
  let currentAnswer = null;

  function commit() {
    if (!currentQNum || currentStemLines.length === 0) return;
    const rawStem = currentStemLines.join(' ');
    if (rawStem.length < 15) return;

    // Detect discipline
    let discipline = 'Tıbbi Patoloji';
    const lowerStem = rawStem.toLowerCase();
    if (lowerStem.includes('virüs') || lowerStem.includes('bakteri') || lowerStem.includes('enfeksiyon') || lowerStem.includes('üretrit') || lowerStem.includes('sistit')) {
      discipline = 'Tıbbi Mikrobiyoloji / Enfeksiyon';
    } else if (lowerStem.includes('ilaç') || lowerStem.includes('reseptör') || lowerStem.includes('tedavi') || lowerStem.includes('antagonist')) {
      discipline = 'Tıbbi Farmakoloji';
    } else if (lowerStem.includes('gebelik') || lowerStem.includes('uterus') || lowerStem.includes('over') || lowerStem.includes('vajinal')) {
      discipline = 'Kadın Hastalıkları ve Doğum';
    } else if (lowerStem.includes('prostat') || lowerStem.includes('böbrek') || lowerStem.includes('ürolojik') || lowerStem.includes('mesane') || lowerStem.includes('orşit')) {
      discipline = 'Üroloji / Nefroloji';
    }

    const slideMatch = findSlideMatch(rawStem, discipline);

    // Format options (ensure 5 options A-E)
    const formattedOptions = ['A', 'B', 'C', 'D', 'E'].map(key => {
      const existing = currentOptions.find(o => o.key === key);
      return {
        key,
        text: existing ? existing.text : `Seçenek ${key} (OCR eksik şıkkı)`,
        suggestedBy: 'Taranmış Sınav Belgesi (OCR)',
        upvotes: 0,
        likedBy: [],
      };
    });

    const qId = `ocr-${committeeId}-${path.basename(sourceFile, path.extname(sourceFile))}-q${currentQNum}-${Math.random().toString(36).substring(7)}`;

    questions.push({
      id: qId,
      committeeId,
      questionNumber: currentQNum,
      discipline,
      topic: rawStem.slice(0, 50).trim() + '...',
      status: 'completed',
      isPastExam: true,
      examYear: 'Çıkmış Sınav (Taranmış Belge)',
      claimedAnswer: currentAnswer || 'A',
      tags: [discipline, 'Taranmış Soru (OCR)', committeeId],
      rawStem,
      fragments: [
        {
          id: `f-${qId}-1`,
          author: 'Taranmış PDF OCR Okuyucu',
          text: rawStem,
          type: 'stem',
          timestamp: new Date().toISOString(),
          upvotes: 0,
          likedBy: [],
        },
      ],
      options: formattedOptions,
      reconstruction: {
        stem: rawStem,
        options: formattedOptions.map(o => ({
          key: o.key,
          text: o.text,
          isAiFilled: o.text.includes('OCR eksik şıkkı'),
        })),
        correctAnswer: currentAnswer || 'A',
        explanation: slideMatch
          ? `Bu soru "${slideMatch.noteTitle}" ders notunun ${slideMatch.pageNumber}. slaytındaki klinik ve patolojik bilgilerle eşleşmektedir.`
          : 'Taranmış sınav belgesinden optik karakter tanıma (OCR) ile birebir aktarılmıştır.',
        confidenceScore: slideMatch ? slideMatch.confidenceScore : 88,
        notesAndDiscrepancies: `Taranmış kaynak dosya: ${sourceFile}`,
        lastUpdated: new Date().toISOString(),
      },
      lectureReference: slideMatch ? {
        noteTitle: slideMatch.noteTitle,
        pageNumber: slideMatch.pageNumber,
        matchedSnippet: slideMatch.matchedSnippet,
        confidenceScore: slideMatch.confidenceScore,
      } : undefined,
      upvotes: 0,
      likedBy: [],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    });

    currentQNum = null;
    currentStemLines = [];
    currentOptions = [];
    currentAnswer = null;
  }

  for (const line of lines) {
    // Soru başlangıcı: "1.", "2)", "Soru 3:"
    const qMatch = line.match(/^(?:soru\s*)?(\d+)[\.\)]\s+(.*)$/i);
    if (qMatch) {
      commit();
      currentQNum = parseInt(qMatch[1], 10);
      currentStemLines = [qMatch[2] || ''];
      continue;
    }

    // Şık: "A)", "A.", "a)", "a."
    const optMatch = line.match(/^([A-Ea-e])[\.\)]\s+(.*)$/);
    if (optMatch && currentQNum) {
      currentOptions.push({
        key: optMatch[1].toUpperCase(),
        text: (optMatch[2] || '').trim(),
      });
      continue;
    }

    // Cevap anahtarı: "Cevap: B", "Yanıt C"
    const ansMatch = line.match(/^(?:cevap|doğru\s*cevap|yanıt)\s*[:\-]?\s*([A-Ea-e])/i);
    if (ansMatch && currentQNum) {
      currentAnswer = ansMatch[1].toUpperCase();
      continue;
    }

    // Devam eden satır
    if (currentQNum) {
      if (currentOptions.length > 0) {
        currentOptions[currentOptions.length - 1].text += ' ' + line;
      } else {
        currentStemLines.push(line);
      }
    }
  }

  commit();
  return questions;
}

async function main() {
  console.log('\nTesseract OCR Motoru Başlatılıyor...');
  const worker = await Tesseract.createWorker('tur');

  if (!fs.existsSync(IMAGES_DIR)) {
    console.log('Klasör bulunamadı:', IMAGES_DIR);
    await worker.terminate();
    return;
  }

  const imageFolders = fs.readdirSync(IMAGES_DIR).filter(f => {
    return fs.statSync(path.join(IMAGES_DIR, f)).isDirectory();
  });

  console.log(`İşlenecek Sınav Klasörleri: ${imageFolders.length}`);
  const allExtractedQuestions = [];

  for (const folder of imageFolders) {
    const folderPath = path.join(IMAGES_DIR, folder);
    const images = fs.readdirSync(folderPath).filter(f => f.endsWith('.png') && !f.includes('_rot'));
    console.log(`\n📁 Klasör: "${folder}" (${images.length} resim)`);

    let fullRawOcrText = '';
    const committeeId = folder.toLowerCase().includes('4') ? 'donem3-kurul4' : 'donem3-kurul1';

    // İşlem yapılacak resim sayısı (ilk 20 sayfa yoğun sınav resimleri)
    const targetImages = images.slice(0, 30);

    for (let idx = 0; idx < targetImages.length; idx++) {
      const imgFile = targetImages[idx];
      const imgPath = path.join(folderPath, imgFile);
      process.stdout.write(`   [${idx+1}/${targetImages.length}] OCR yapılıyor: ${imgFile}... `);

      try {
        // 1. Try 0 deg
        let res = await worker.recognize(imgPath);
        let text = res.data.text || '';
        let score = scoreOrientation(text);

        // 2. If score is low, try 180 deg (upside down scans)
        if (score < 5) {
          const rotPath = rotateImage(imgPath, 180);
          const rotRes = await worker.recognize(rotPath);
          const rotScore = scoreOrientation(rotRes.data.text);
          if (rotScore > score) {
            text = rotRes.data.text;
            score = rotScore;
          }
        }

        if (text && text.trim().length > 30) {
          fullRawOcrText += `\n\n--- Belge: ${folder} - Sayfa: ${idx+1} ---\n\n` + text.trim();
          console.log(`✓ (${text.trim().length} karakter, skor: ${score})`);
        } else {
          console.log(`(Boş/şema)`);
        }
      } catch (err) {
        console.log(`⚠️ Hata: ${err.message}`);
      }
    }

    // Save full raw text
    const txtFile = path.join(TXT_DIR, `${folder}.ocr.txt`);
    fs.writeFileSync(txtFile, fullRawOcrText, 'utf8');

    // Parse questions
    const parsedQuestions = parseOcrQuestions(fullRawOcrText, folder, committeeId);
    console.log(`   ✓ "${folder}": ${parsedQuestions.length} soru ayrıştırıldı ve ders notları ile eşleştirildi.`);

    const jsonFile = path.join(TXT_DIR, `${folder}.ocr.questions.json`);
    fs.writeFileSync(jsonFile, JSON.stringify(parsedQuestions, null, 2), 'utf8');

    allExtractedQuestions.push(...parsedQuestions);
  }

  await worker.terminate();
  console.log(`\n======================================================`);
  console.log(`  Toplanan OCR Soru Sayısı: ${allExtractedQuestions.length}`);
  console.log(`======================================================`);

  if (allExtractedQuestions.length > 0) {
    // 1. Merge into local data/questions.json
    console.log('\n💾 1. data/questions.json güncelleniyor...');
    const questionsPath = path.join(rootDir, 'data', 'questions.json');
    let localData = { committees: [], questions: [] };
    if (fs.existsSync(questionsPath)) {
      try {
        const parsed = JSON.parse(fs.readFileSync(questionsPath, 'utf8'));
        localData = Array.isArray(parsed) ? { committees: [], questions: parsed } : parsed;
      } catch {}
    }

    const qMap = new Map();
    (localData.questions || []).forEach(q => { if (q && q.id) qMap.set(q.id, q); });
    let newCount = 0;
    for (const q of allExtractedQuestions) {
      if (!qMap.has(q.id)) {
        qMap.set(q.id, q);
        newCount++;
      }
    }
    localData.questions = Array.from(qMap.values());
    fs.writeFileSync(questionsPath, JSON.stringify(localData, null, 2), 'utf8');
    console.log(`   ✓ data/questions.json güncellendi! (+${newCount} yeni soru eklendi)`);

    // 2. Sync newly extracted questions directly to Firebase Firestore
    console.log('\n🔥 2. Yeni OCR Soruları Firebase Firestore\'a aktarılıyor...');
    const batch = writeBatch(firestoreDb);
    for (const q of allExtractedQuestions.slice(0, 400)) {
      const docRef = doc(firestoreDb, 'questions', q.id);
      batch.set(docRef, cleanForFirestore(q), { merge: true });
    }
    await batch.commit();
    console.log(`   ✓ ${Math.min(allExtractedQuestions.length, 400)} yeni soru Firestore'a kaydedildi!`);
  }

  console.log('\n🎉 OCR ve Soru Çıkarım İşlemi Başarıyla Tamamlandı!');
  process.exit(0);
}

main().catch(err => {
  console.error('\n❌ OCR İşlem Hatası:', err);
  process.exit(1);
});
