#!/usr/bin/env node
/**
 * scripts/fix-nested-and-embedded-questions.mjs
 * 
 * MedSoru İç İçe Geçmiş Şıklar, Soru Kökünde Kalan Şıklar ve
 * Birbirine Yapışmış Soruları Ayrıştırma ve Düzeltme Motoru
 * 
 * Çözülen Sorunlar:
 * 1. Şık İçinde Şık (Nested Options):
 *    Örnek: B şıkkında "Öksürük ? C) Postoperatif agri" bulunması ve C şıkkının eksik kalması.
 *    -> B: "Öksürük", C: "Postoperatif agri" olarak ayrıştırılır ve sıralı A, B, C, D, E tamamlanır.
 * 
 * 2. Soru Kökünde Unutulmuş Şıklar (Options Trapped in Stem):
 *    Örnek: Soru kökünde "Hangisi sıvı ilaç değildir? a. Solüsyon b. Damla c. Komprime d. Jel e. Lavman"
 *    yazıp şıklar dizisinde sadece dummy "Seçenek A", "Seçenek B" bulunması.
 *    -> Soru kökü temizlenir, şıklar A..E olarak doğru metinlerle şık dizisine aktarılır.
 * 
 * 3. Birbirine Yapışmış / İç İçe Geçen Sorular (Merged Questions):
 *    Örnek: Bir sorunun son şıkkına başka bir sorunun ("19-Crohn ve ülseratif kolitin kiyaslamasi...")
 *    yapışması.
 *    -> Asıl şık temizlenir, yapışan yeni soru bağımsız bir soru olarak sisteme kazandırılır.
 * 
 * 4. Tıbbi Terim Koruması:
 *    E. coli, C. albicans, C-reaktif protein, E-cadherin, Hepatit B, Vitamin B12 gibi tıbbi
 *    ifadelerin yanlışlıkla şık olarak parçalanması engellenir.
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');

const DATA_PAST_PATH = path.join(ROOT_DIR, 'data', 'pastQuestions.json');
const SRC_PAST_PATH = path.join(ROOT_DIR, 'src', 'data', 'pastQuestions.json');
const BACKUP_PATH = path.join(ROOT_DIR, 'data', 'pastQuestions.backup_before_nested_fix.json');
const REPORT_PATH = path.join(ROOT_DIR, 'data', 'nested_fix_report.json');

// --- TIBBİ VE BİYOLOJİK KORUMA SÖZLÜĞÜ (Asla şık zannedilmeyecek terimler) ---
const PROTECTED_TERMS_REGEX = new RegExp(
  '\\b(?:' +
  'E\\.\\s*coli|E\\.\\s*Coli|C\\.\\s*difficile|C\\.\\s*albicans|C\\.\\s*tetani|C\\.\\s*botulinum|' +
  'C\\.\\s*diphtheriae|C\\.\\s*perfringens|C\\.\\s*jejuni|C\\.\\s*psittaci|C\\.\\s*burnetii|' +
  'B\\.\\s*anthracis|B\\.\\s*cereus|B\\.\\s*pertussis|B\\.\\s*burgdorferi|B\\.\\s*fragilis|' +
  'S\\.\\s*aureus|S\\.\\s*pneumoniae|S\\.\\s*pyogenes|S\\.\\s*agalactiae|' +
  'H\\.\\s*pylori|H\\.\\s*influenzae|P\\.\\s*aeruginosa|M\\.\\s*tuberculosis|' +
  'C-reaktif|E-cadherin|N-cadherin|TGF-B|HLA-B27|' +
  'Hepatit\\s+[A-E]|Vitamin\\s+[A-E]|B\\s*hücre|B\\s*lenfosit|T\\s*hücre|T\\s*lenfosit|' +
  'Tip\\s+[A-E]|Evre\\s+[A-E]|Grup\\s+[A-E]|Derece\\s+[A-E]' +
  ')\\b',
  'gi'
);

function isDummyOrFiller(text) {
  if (!text) return true;
  const t = String(text).trim().toLowerCase();
  if (t.startsWith('seçenek ') || t.startsWith('secenek ') || t === 'seçenek' || t === 'secenek') return true;
  if (t.includes('ocr eksik şıkkı')) return true;
  if (['distrofik kalsifikasyon', 'lipofuskin birikimi', 'koagülasyon nekrozu ve nükleer piknoz'].includes(t)) return true;
  return false;
}

/**
 * 1. ŞIK İÇİNDEKİ GİZLİ ŞIKLARI AYRIŞTIRICI
 * Örn: "Öksürük ? C) Postoperatif agri" -> B: "Öksürük", C: "Postoperatif agri"
 */
function findEmbeddedOptions(text, currentKey) {
  if (!text) return [];

  const placeholders = {};
  let safeText = text.replace(PROTECTED_TERMS_REGEX, (match) => {
    const key = `__PROTECTED_${Object.keys(placeholders).length}__`;
    placeholders[key] = match;
    return key;
  });

  // OCR özel karakter normalizasyonu (© -> C, € -> E)
  safeText = safeText.replace(/©\s*[\)\.\-]/g, 'C) ');
  safeText = safeText.replace(/€\s*[\)\.\-]/g, 'E) ');

  const pattern = /(?:^|[\s\?\;\,\t\|]+)\??\s*([A-Ea-e])[\)\.\-]\s*/g;
  const splits = [];
  let m;

  while ((m = pattern.exec(safeText)) !== null) {
    const letter = m[1].toUpperCase();
    if (m.index === 0 && letter === currentKey) continue;
    const after = safeText.slice(m.index + m[0].length);
    if (after.trim().length < 2) continue;
    splits.push({ start: m.index, end: m.index + m[0].length, letter });
  }

  if (splits.length === 0) return [];

  const chunks = [];
  let initialText = safeText.slice(0, splits[0].start).trim();
  initialText = initialText.replace(/[\s\?\;\,\t\|]+$/, '');
  for (const [pKey, pVal] of Object.entries(placeholders)) {
    initialText = initialText.replaceAll(pKey, pVal);
  }
  chunks.push({ key: currentKey, text: initialText });

  for (let idx = 0; idx < splits.length; idx++) {
    const nextStart = idx + 1 < splits.length ? splits[idx + 1].start : safeText.length;
    let chunkText = safeText.slice(splits[idx].end, nextStart).trim();
    chunkText = chunkText.replace(/[\s\?\;\,\t\|]+$/, '');
    for (const [pKey, pVal] of Object.entries(placeholders)) {
      chunkText = chunkText.replaceAll(pKey, pVal);
    }
    chunks.push({ key: splits[idx].letter, text: chunkText });
  }

  return chunks;
}

/**
 * 2. SORU KÖKÜ İÇİNDE KALMIŞ ŞIKLARI AYRIŞTIRICI
 * Örn: "Aşağıdakilerden hangisi... değildir? a. Solüsyon b. Damla c. Komprime d. Jel e. Lavman"
 */
function extractOptionsFromStem(stem) {
  if (!stem) return null;

  const allMarkers = [];
  const markerRegex = /(?:^|[\s\n])([a-eA-E])[\)\.\-]\s*/g;
  let m;

  while ((m = markerRegex.exec(stem)) !== null) {
    allMarkers.push({ index: m.index, matchLength: m[0].length, letter: m[1].toUpperCase() });
  }

  if (allMarkers.length < 3) return null;

  // A -> B -> C -> D sıralı sekansını bul
  let seqStartIdx = -1;
  for (let i = 0; i < allMarkers.length; i++) {
    if (allMarkers[i].letter === 'A') {
      const expected = ['B', 'C', 'D'];
      let lastIdx = i;
      let matchedCount = 1;
      for (const exp of expected) {
        let foundNext = false;
        for (let j = lastIdx + 1; j < Math.min(lastIdx + 3, allMarkers.length); j++) {
          if (allMarkers[j].letter === exp) {
            matchedCount++;
            lastIdx = j;
            foundNext = true;
            break;
          }
        }
        if (!foundNext) break;
      }
      if (matchedCount >= 4) {
        seqStartIdx = i;
        break;
      }
    }
  }

  if (seqStartIdx === -1) return null;

  const aMarker = allMarkers[seqStartIdx];
  const cleanStem = stem.slice(0, aMarker.index).trim();

  // A'dan başlayarak ardışık harfleri topla
  const expectedLetters = ['A', 'B', 'C', 'D', 'E'];
  let expPtr = 0;
  const optMatches = [];

  for (let idx = seqStartIdx; idx < allMarkers.length; idx++) {
    const item = allMarkers[idx];
    if (expPtr < expectedLetters.length && item.letter === expectedLetters[expPtr]) {
      optMatches.push(item);
      expPtr++;
      if (expPtr === expectedLetters.length) break;
    }
  }

  if (optMatches.length < 4) return null;

  const options = [];
  for (let idx = 0; idx < optMatches.length; idx++) {
    const cur = optMatches[idx];
    const start = cur.index + cur.matchLength;
    const end = idx + 1 < optMatches.length ? optMatches[idx + 1].index : stem.length;
    let optText = stem.slice(start, end).trim();

    // Son şıkta sayfa sonu altbilgilerini temizle
    if (idx === optMatches.length - 1) {
      optText = optText.replace(/[\s\n]+(?:X\s+C\s+t\s+M\s+E\s+R\s+\d+|\d{1,2}|Viroloji|Patoloji|Farmakoloji)\s*$/i, '');
      optText = optText.replace(/,\s*$/, '').trim();
    }

    options.push({
      key: cur.letter,
      text: optText
    });
  }

  return { cleanStem, options };
}

/**
 * 3. ŞIK VEYA KÖK İÇİNE YAPIŞMIŞ İKİNCİ SORULARI AYRIŞTIRICI
 */
function extractEmbeddedQuestions(text) {
  if (!text || text.length < 80) return { cleanText: text, extractedQuestions: [] };

  const qMatch = /(?:^|\s+)(\d{1,3})[\.\-\)]\s*([A-ZÇĞİÖŞÜ][^?\n]{6,}\?)/.exec(text);
  if (!qMatch || qMatch.index < 10) return { cleanText: text, extractedQuestions: [] };

  let cleanPrefix = text.slice(0, qMatch.index).trim();
  cleanPrefix = cleanPrefix.replace(/[\s\n]+(?:ortopedi|üroloji|patoloji|dahiliye|pediatri|kardiyoloji)?\s*\(\d+\/\d+\)\s*$/i, '');
  cleanPrefix = cleanPrefix.replace(/\[\d{1,2}[\.\/]\d{1,2}[\.\/]\d{2,4}\s+\d{2}:\d{2}\].*$/, '').trim();

  const remainder = text.slice(qMatch.index).trim();
  const qMatches = [...remainder.matchAll(/(?:^|\s+)(\d{1,3})[\.\-\)]\s*([A-ZÇĞİÖŞÜ][^?\n]{5,}\?)/g)];
  if (qMatches.length === 0) return { cleanText: cleanPrefix, extractedQuestions: [] };

  const extracted = [];
  for (let idx = 0; idx < qMatches.length; idx++) {
    const cur = qMatches[idx];
    const qNum = parseInt(cur[1], 10);
    const qStem = cur[2].trim();
    const startOfOpts = cur.index + cur[0].length;
    const endOfChunk = idx + 1 < qMatches.length ? qMatches[idx + 1].index : remainder.length;
    const optsBlock = remainder.slice(startOfOpts, endOfChunk).trim();

    const optMatches = [...optsBlock.matchAll(/(?:^|[\s\n])([A-Ea-e])[\)\.\-]\s*/g)];
    const options = [];
    if (optMatches.length >= 3) {
      for (let oIdx = 0; oIdx < optMatches.length; oIdx++) {
        const om = optMatches[oIdx];
        const s = om.index + om[0].length;
        const e = oIdx + 1 < optMatches.length ? optMatches[oIdx + 1].index : optsBlock.length;
        let otext = optsBlock.slice(s, e).trim();
        otext = otext.replace(/[\s\n]*(?:cevap|yanıt)[\:\s]+[A-E1-5].*$/i, '').trim();
        options.push({ key: om[1].toUpperCase(), text: otext });
      }
    }

    extracted.push({
      questionNumber: qNum,
      stem: qStem,
      options
    });
  }

  return { cleanText: cleanPrefix, extractedQuestions: extracted };
}

// --- ANA DÜZELTME VE ÇALIŞTIRMA MOTORU ---
export async function runNestedAndEmbeddedFixer(options = {}) {
  const isDryRun = options.dryRun || process.argv.includes('--dry-run');
  const syncSupabase = options.syncSupabase || process.argv.includes('--sync-supabase');

  console.log('='.repeat(70));
  console.log('🩺 MedSoru: İç İçe Şık ve Soru Ayrıştırma & Düzeltme Motoru');
  console.log(`📁 Kaynak: ${DATA_PAST_PATH}`);
  console.log(`⚙️  Mod: ${isDryRun ? '🔍 SIMULATION / DRY-RUN (Değişiklik yazılmaz)' : '🚀 FIX & SAVE'}`);
  console.log('='.repeat(70));

  if (!fs.existsSync(DATA_PAST_PATH)) {
    console.error('❌ pastQuestions.json dosyası bulunamadı:', DATA_PAST_PATH);
    return;
  }

  const rawContent = fs.readFileSync(DATA_PAST_PATH, 'utf8');
  const questions = JSON.parse(rawContent);
  console.log(`📊 Toplam ${questions.length} soru yüklendi.\n`);

  // Yedek al
  if (!isDryRun && !fs.existsSync(BACKUP_PATH)) {
    fs.writeFileSync(BACKUP_PATH, rawContent, 'utf8');
    console.log(`💾 Güvenlik yedeği alındı: ${BACKUP_PATH}`);
  }

  let nestedCount = 0;
  let stemExtractedCount = 0;
  let attachedQuestionsCount = 0;
  const newQuestionsToAdd = [];
  const report = [];

  for (let i = 0; i < questions.length; i++) {
    const q = questions[i];
    let isModified = false;
    const auditEntry = { id: q.id, changes: [] };

    // Soru kökü ve şıkları al
    const rec = q.reconstruction || {};
    const raw = q.rawQuestion || {};
    let stem = rec.stem || raw.stem || '';
    let opts = rec.options || raw.options || [];

    // --- KONTROL 1: Şıklar Soru Kökünde Unutulmuş ve Şıklar Dummy/Boş mu? ---
    const allDummy = opts.length === 0 || opts.every(o => isDummyOrFiller(o.text));
    const hasFew = opts.length < 4;

    if (allDummy || hasFew) {
      const stemResult = extractOptionsFromStem(stem);
      if (stemResult) {
        stemExtractedCount++;
        isModified = true;
        auditEntry.changes.push({
          type: 'stem_options_extracted',
          originalStem: stem,
          newStem: stemResult.cleanStem,
          extractedOptionsCount: stemResult.options.length
        });

        stem = stemResult.cleanStem;
        opts = stemResult.options.map(o => ({
          key: o.key,
          text: o.text,
          isCorrect: false
        }));

        if (q.reconstruction) {
          q.reconstruction.stem = stem;
          q.reconstruction.options = opts;
        }
        if (q.rawQuestion) {
          q.rawQuestion.stem = stem;
          q.rawQuestion.options = opts.map(o => ({ key: o.key, text: o.text }));
        }
      }
    }

    // --- KONTROL 2: Şıkların İçinde Başka Şık Var mı? (Nested Options) ---
    let hadNested = false;
    const finalOptsMap = {};

    // Önce mevcut temiz şıkları haritaya al (dummy olmayanlar)
    for (const o of opts) {
      if (!isDummyOrFiller(o.text)) {
        finalOptsMap[o.key] = {
          key: o.key,
          text: o.text,
          isCorrect: !!o.isCorrect
        };
      }
    }

    for (const o of opts) {
      const splits = findEmbeddedOptions(o.text, o.key);
      if (splits.length > 1) {
        hadNested = true;
        auditEntry.changes.push({
          type: 'nested_option_split',
          optionKey: o.key,
          originalText: o.text,
          splits
        });

        // Parçalanan şıkları yerleştir
        for (const s of splits) {
          finalOptsMap[s.key] = {
            key: s.key,
            text: s.text,
            isCorrect: (s.key === o.key ? !!o.isCorrect : false)
          };
        }
      }
    }

    if (hadNested) {
      nestedCount++;
      isModified = true;

      // Sıralı A..E oluştur
      const sortedKeys = ['A', 'B', 'C', 'D', 'E'];
      const rebuiltOpts = [];
      for (const k of sortedKeys) {
        if (finalOptsMap[k]) {
          rebuiltOpts.push(finalOptsMap[k]);
        }
      }

      if (rebuiltOpts.length >= 3) {
        opts = rebuiltOpts;
        if (q.reconstruction) {
          q.reconstruction.options = rebuiltOpts;
        }
        if (q.rawQuestion) {
          q.rawQuestion.options = rebuiltOpts.map(o => ({ key: o.key, text: o.text }));
        }
      }
    }

    // --- KONTROL 3: Şıkların Sonuna Başka Bir Soru Yapışmış mı? ---
    for (const o of opts) {
      const detached = extractEmbeddedQuestions(o.text);
      if (detached.extractedQuestions.length > 0) {
        isModified = true;
        auditEntry.changes.push({
          type: 'embedded_question_detached',
          optionKey: o.key,
          originalText: o.text,
          cleanText: detached.cleanText,
          extractedCount: detached.extractedQuestions.length
        });

        o.text = detached.cleanText;
        if (q.rawQuestion?.options) {
          const rawMatch = q.rawQuestion.options.find(ro => ro.key === o.key);
          if (rawMatch) rawMatch.text = detached.cleanText;
        }

        for (const eq of detached.extractedQuestions) {
          attachedQuestionsCount++;
          // Yeni bağımsız soru oluştur
          const newId = `${q.id}-split-q${eq.questionNumber}`;
          const newQ = {
            id: newId,
            sourceFile: q.sourceFile,
            committeeId: q.committeeId,
            examYear: q.examYear,
            questionNumber: eq.questionNumber,
            discipline: q.discipline || 'Klinik Tıp',
            topic: `${q.discipline || 'Genel Tıp'} Çıkmış Soru #${eq.questionNumber}`,
            rawQuestion: {
              stem: eq.stem,
              options: eq.options.map(x => ({ key: x.key, text: x.text })),
              claimedAnswer: null
            },
            reconstruction: {
              stem: eq.stem,
              options: eq.options.map(x => ({ key: x.key, text: x.text, isCorrect: false })),
              correctAnswer: null,
              explanation: `${q.sourceFile || 'Çıkmış sınav'} arşivinden ayrıştırılarak kurtarılmış sorudur.`,
              isAiRefined: false,
              reconstructionQuality: 'restored'
            },
            isPastExam: true,
            isSuspect: false,
            isAmbiguous: false,
            isLocked: false,
            upvotes: 0,
            comments: [],
            reports: [],
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString()
          };
          newQuestionsToAdd.push(newQ);
        }
      }
    }

    if (isModified) {
      q.updatedAt = new Date().toISOString();
      report.push(auditEntry);
    }
  }

  console.log('='.repeat(70));
  console.log('📊 ANALİZ VE İŞLEM SONUÇLARI:');
  console.log(`✅ Şık İçinde Şık Bulunup Ayrıştırılan Soru: ${nestedCount}`);
  console.log(`✅ Kök İçinde Unutulup Şıklara Dönüştürülen Soru: ${stemExtractedCount}`);
  console.log(`✅ Şıklardan Ayrıştırılarak Kurtarılan Yeni Soru: ${attachedQuestionsCount}`);
  console.log(`📝 Toplam Düzeltilen Ana Soru: ${report.length}`);
  console.log('='.repeat(70));

  if (!isDryRun) {
    // Yeni kurtarılan soruları listeye ekle
    if (newQuestionsToAdd.length > 0) {
      questions.push(...newQuestionsToAdd);
      console.log(`➕ ${newQuestionsToAdd.length} yeni soru arşive eklendi (Yeni toplam: ${questions.length}).`);
    }

    // 1. meds/data/pastQuestions.json ve meds/src/data/pastQuestions.json güncelle
    fs.writeFileSync(DATA_PAST_PATH, JSON.stringify(questions, null, 2), 'utf8');
    console.log(`💾 Güncellendi: ${DATA_PAST_PATH}`);

    if (fs.existsSync(path.dirname(SRC_PAST_PATH))) {
      fs.writeFileSync(SRC_PAST_PATH, JSON.stringify(questions, null, 2), 'utf8');
      console.log(`💾 Güncellendi: ${SRC_PAST_PATH}`);
    }

    // 2. Raporu kaydet
    fs.writeFileSync(REPORT_PATH, JSON.stringify(report, null, 2), 'utf8');
    console.log(`📄 Rapor oluşturuldu: ${REPORT_PATH}`);

    // 3. Modüler Veritabanını Derle (build-database-json.mjs)
    console.log('\n🔄 Modüler database_json derleniyor (build-database-json.mjs)...');
    try {
      const buildScript = path.join(ROOT_DIR, 'scripts', 'build-database-json.mjs');
      if (fs.existsSync(buildScript)) {
        execSync(`node "${buildScript}"`, { stdio: 'inherit' });
        console.log('✅ database_json başarıyla güncellendi.');
      }
    } catch (e) {
      console.warn('⚠️ build-database-json çalıştırma uyarısı:', e.message);
    }

    // 4. Opsiyonel Supabase Eşitleme
    if (syncSupabase) {
      console.log('\n☁️ Supabase senkronizasyonu başlatılıyor...');
      try {
        const syncScript = path.join(ROOT_DIR, 'scripts', 'sync-past-questions-to-supabase.mjs');
        if (fs.existsSync(syncScript)) {
          execSync(`node "${syncScript}"`, { stdio: 'inherit' });
          console.log('✅ Supabase senkronizasyonu tamamlandı.');
        }
      } catch (e) {
        console.warn('⚠️ Supabase senkronizasyon hatası:', e.message);
      }
    }
  } else {
    console.log('\n🔍 [DRY-RUN] Hiçbir dosya değiştirilmedi. Kalıcı uygulamak için --fix parametresi kullanın.');
  }

  return {
    nestedCount,
    stemExtractedCount,
    attachedQuestionsCount,
    totalModified: report.length,
    newQuestionsCount: newQuestionsToAdd.length
  };
}

// CLI doğrudan çağrıldığında çalıştır
if (process.argv[1] && process.argv[1].endsWith('fix-nested-and-embedded-questions.mjs')) {
  runNestedAndEmbeddedFixer();
}
