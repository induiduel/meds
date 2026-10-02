#!/usr/bin/env node
/**
 * =============================================================================
 * merge-same-exam-duplicates.mjs
 * -----------------------------------------------------------------------------
 * Eşleşen sorular birbirini tekrar eden sorular veya birbirine aşırı benzeyen
 * ve cevapları aynı olan sorular eğerki aynı sene aynı kurulda sorulduysa mutlaka
 * aynı soru altında birleştiren script.
 * 
 * - Eğer farklı kurullarda veya senelerde yazıldığı kesinse sorular korunur.
 * - Çelişkili / zıt cevaplara sahip sorular asla birleştirilmez.
 * - Master soru seçilir ve mükerrer kopyaların ID ve kaynakları master soruya işlenir.
 * =============================================================================
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Metin normalizasyonu
function trLower(text) {
  if (!text) return '';
  return text
    .replace(/İ/g, 'i')
    .replace(/I/g, 'ı')
    .replace(/Ö/g, 'o')
    .replace(/ö/g, 'o')
    .replace(/Ü/g, 'u')
    .replace(/ü/g, 'u')
    .replace(/Ş/g, 's')
    .replace(/ş/g, 's')
    .replace(/Ç/g, 'c')
    .replace(/ç/g, 'c')
    .replace(/Ğ/g, 'g')
    .replace(/ğ/g, 'g')
    .toLowerCase()
    .replace(/\u0307/g, '')
    .replace(/\u0327/g, '');
}

function cleanForMatch(text) {
  if (!text) return '';
  let t = trLower(text);
  t = t.replace(/^(?:soru\s*)?\d+[\.\)\-\:\s]+/i, '').trim();
  t = t.replace(/^[a-e][\.\)\-\:\s]+/i, '').trim();
  t = t.replace(/(?:donem\s*\d|kurul\s*\d|enfeksiyon|patoloji|farmakoloji|halk\s*sagligi).*$/i, '');
  return t.replace(/[^a-z0-9]/g, '');
}

// Zıt kavramlar kontrolü
const ANTONYMS = [
  ['minor', 'major'],
  ['akut', 'kronik'],
  ['artar', 'azalir'],
  ['artis', 'azalis'],
  ['hizli', 'uzun'],
  ['hizli', 'yavas'],
  ['benign', 'malign'],
  ['pozitif', 'negatif'],
  ['primer', 'sekonder'],
  ['hipo', 'hiper'],
  ['endojen', 'ekzojen'],
  ['dogru', 'yanlis'],
  ['komplike', 'komplikeolmayan'],
  ['drift', 'shift']
];

function hasAntonymContradiction(text1, text2) {
  const c1 = cleanForMatch(text1);
  const c2 = cleanForMatch(text2);
  for (const [w1, w2] of ANTONYMS) {
    if ((c1.includes(w1) && c2.includes(w2)) || (c2.includes(w1) && c1.includes(w2))) {
      return true;
    }
  }
  return false;
}

// Levenshtein / Dice / SequenceMatcher benzeri benzerlik hesaplama
function calculateSimilarity(str1, str2) {
  if (str1 === str2) return 1.0;
  if (!str1 || !str2) return 0.0;
  if (str1.startsWith(str2) || str2.startsWith(str1)) {
    return Math.min(str1.length, str2.length) / Math.max(str1.length, str2.length);
  }
  
  // Bigram Dice Coefficient (hızlı ve metin benzerliğinde çok etkili)
  const getBigrams = (s) => {
    const bigrams = new Map();
    for (let i = 0; i < s.length - 1; i++) {
      const b = s.substring(i, i + 2);
      bigrams.set(b, (bigrams.get(b) || 0) + 1);
    }
    return bigrams;
  };

  const b1 = getBigrams(str1);
  const b2 = getBigrams(str2);
  let intersection = 0;
  for (const [b, count] of b1.entries()) {
    if (b2.has(b)) {
      intersection += Math.min(count, b2.get(b));
    }
  }

  const total = (str1.length - 1) + (str2.length - 1);
  return total > 0 ? (2 * intersection) / total : 0.0;
}

// Kurul ve Yıl Normalizasyonu
function normalizeCommittee(committeeId, sourceFile = '') {
  const combined = trLower(`${committeeId || ''} ${sourceFile || ''}`);
  if (/kurul\s*1|kurul1|kurul\s*i\b|1\.?\s*kurul/i.test(combined)) return 'donem3-kurul1';
  if (/kurul\s*2|kurul2|kurul\s*ii\b|2\.?\s*kurul|noropsikiyatri/i.test(combined)) return 'donem3-kurul2';
  if (/kurul\s*3|kurul3|kurul\s*iii\b|3\.?\s*kurul|gis|gastro/i.test(combined)) return 'donem3-kurul3';
  if (/kurul\s*4|kurul4|kurul\s*iv\b|4\.?\s*kurul|dolasim|solunum|kardiyo/i.test(combined)) return 'donem3-kurul4';
  if (/kurul\s*5|kurul5|kurul\s*v\b|5\.?\s*kurul|ortopedi|urogenital/i.test(combined)) return 'donem3-kurul5';
  if (/kurul\s*6|kurul6|kurul\s*vi\b|6\.?\s*kurul|endokrin/i.test(combined)) return 'donem3-kurul6';
  if (/final/i.test(combined)) return 'donem3-final';
  if (/but/i.test(combined)) return 'donem3-butunleme';
  return committeeId || 'donem3-kurul1';
}

function normalizeYear(yearVal, sourceFile = '') {
  const combined = `${yearVal || ''} ${sourceFile || ''}`;
  const m = combined.match(/20\d{2}[\-\/]20\d{2}/);
  if (m) return m[0].replace('/', '-');

  if (/2020-2021|20\s*21/i.test(combined)) return '2020-2021';
  if (/2021-2022|21\s*22|2021/i.test(combined)) return '2021-2022';
  if (/2022-2023|22\s*23|2022/i.test(combined)) return '2022-2023';
  if (/2023-2024|2023/i.test(combined)) return '2023-2024';
  if (/2024-2025|2024/i.test(combined)) return '2024-2025';
  if (/2025-2026|25-26/i.test(combined)) return '2025-2026';
  if (/2016-2017/i.test(combined)) return '2016-2017';
  if (/arsiv|gecmis/i.test(trLower(combined))) return 'arsiv';

  return yearVal || 'arsiv';
}

function extractStem(q) {
  let stem = q.stem || (q.reconstruction && q.reconstruction.stem) || (q.rawQuestion && q.rawQuestion.stem) || '';
  return stem.trim();
}

function extractOptions(q) {
  let opts = q.options || (q.reconstruction && q.reconstruction.options) || (q.rawQuestion && q.rawQuestion.options) || [];
  return opts.map(o => ({
    key: (o.key || '').trim().toUpperCase(),
    text: (o.text || '').trim(),
    cleanText: cleanForMatch(o.text || ''),
    isCorrect: Boolean(o.isCorrect)
  }));
}

function extractCorrectAnswer(q, cleanOpts) {
  let ansKey = (q.correctAnswer || (q.rawQuestion && q.rawQuestion.claimedAnswer) || (q.reconstruction && q.reconstruction.correctAnswer) || '').trim().toUpperCase();
  let ansText = '';
  for (const o of cleanOpts) {
    if ((ansKey && o.key === ansKey) || o.isCorrect) {
      ansText = o.text;
      if (!ansKey && o.key) ansKey = o.key;
      break;
    }
  }
  return { ansKey, ansClean: cleanForMatch(ansText), ansRaw: ansText };
}

function calculateScore(q) {
  let s = 0;
  const qid = String(q.id || '');
  if (qid.startsWith('d3-k')) s += 120;
  if (q.is_curated) s += 60;
  if ((q.explanation || '').length > 100) s += 50;
  else if ((q.explanation || '').length > 30) s += 25;
  if ((q.options || []).length === 5) s += 30;
  if (q.reconstruction) s += 15;
  return s;
}

// Ana deduplikasyon fonksiyonu
export function deduplicateQuestions(questions, similarityThreshold = 0.82) {
  const processed = questions.map((q, idx) => {
    const stem = extractStem(q);
    const cleanStem = cleanForMatch(stem);
    const opts = extractOptions(q);
    const { ansKey, ansClean, ansRaw } = extractCorrectAnswer(q, opts);
    const normCid = normalizeCommittee(q.committeeId, q.sourceFile || q.source);
    const normYr = normalizeYear(q.examYear || q.year, q.sourceFile || q.source);
    const isCurated = String(q.id || '').startsWith('d3-k') || ((q.explanation || '').length > 40);

    return {
      idx,
      id: q.id || `q-${idx}`,
      raw: q,
      stem,
      cleanStem,
      opts,
      ansKey,
      ansClean,
      ansRaw,
      normCid,
      normYr,
      isCurated,
      score: calculateScore(q)
    };
  });

  // Hızlı bloklama (shingle indeksi)
  const shingleIndex = new Map();
  processed.forEach((p, idx) => {
    const s = p.cleanStem;
    if (s.length < 10) return;
    for (let start = 0; start < Math.min(s.length - 8, 48); start += 6) {
      const shingle = s.substring(start, start + 8);
      if (!shingleIndex.has(shingle)) shingleIndex.set(shingle, []);
      shingleIndex.get(shingle).push(idx);
    }
  });

  const candidatePairs = new Set();
  for (const idxList of shingleIndex.values()) {
    if (idxList.length > 1 && idxList.length < 120) {
      for (let i = 0; i < idxList.length; i++) {
        for (let j = i + 1; j < idxList.length; j++) {
          const a = Math.min(idxList[i], idxList[j]);
          const b = Math.max(idxList[i], idxList[j]);
          candidatePairs.add(`${a},${b}`);
        }
      }
    }
  }

  // Disjoint set
  const parent = new Map();
  function find(i) {
    if (!parent.has(i)) parent.set(i, i);
    if (parent.get(i) !== i) {
      parent.set(i, find(parent.get(i)));
    }
    return parent.get(i);
  }
  function union(i, j) {
    const rootI = find(i);
    const rootJ = find(j);
    if (rootI !== rootJ) parent.set(rootJ, rootI);
  }

  const mergeEvents = [];
  const crossExamRefs = new Map();

  for (const pairStr of candidatePairs) {
    const [i, j] = pairStr.split(',').map(Number);
    const p1 = processed[i];
    const p2 = processed[j];

    const isSameKurul = p1.normCid === p2.normCid;
    const isSameYear = p1.normYr === p2.normYr;

    if (p1.cleanStem.length < 10 || p2.cleanStem.length < 10) continue;
    if (hasAntonymContradiction(p1.stem, p2.stem)) continue;

    const stemSim = calculateSimilarity(p1.cleanStem, p2.cleanStem);
    if (stemSim < similarityThreshold) continue;

    // Seçenekler kontrolü
    const optTexts1 = p1.opts.map(o => o.cleanText).filter(t => t.length > 3);
    const optTexts2 = p2.opts.map(o => o.cleanText).filter(t => t.length > 3);
    const set1 = new Set(optTexts1);
    const matchingOptsCount = optTexts2.filter(t => set1.has(t)).length;
    const isIdenticalOpts = matchingOptsCount >= 4 && optTexts1.length >= 4 && optTexts2.length >= 4;

    // Cevap kontrolü
    let ansMatch = false;
    let ansReason = '';

    if (p1.ansClean && p2.ansClean) {
      if (hasAntonymContradiction(p1.ansRaw, p2.ansRaw)) {
        ansMatch = false;
      } else if (p1.ansClean === p2.ansClean) {
        ansMatch = true;
        ansReason = 'exact_answer_text';
      } else if (calculateSimilarity(p1.ansClean, p2.ansClean) >= 0.75) {
        ansMatch = true;
        ansReason = 'similar_answer_text';
      } else if ((p1.ansClean.length > 5 && p1.ansClean.includes(p2.ansClean)) || (p2.ansClean.length > 5 && p2.ansClean.includes(p1.ansClean))) {
        ansMatch = true;
        ansReason = 'contained_answer_text';
      } else if (isIdenticalOpts && stemSim >= 0.90 && (p1.isCurated !== p2.isCurated)) {
        ansMatch = true;
        ansReason = 'exact_options_curated_twin';
      }
    } else if (isIdenticalOpts && stemSim >= 0.90) {
      ansMatch = true;
      ansReason = 'twin_missing_text';
    } else if (p1.ansKey && p2.ansKey && p1.ansKey === p2.ansKey && stemSim >= 0.92) {
      ansMatch = true;
      ansReason = 'same_key_no_text';
    }

    if (!ansMatch) continue;

    // KULLANICI KURALI:
    // Eğer aynı sene aynı kurulda sorulduysa BİRLEŞTİR, farklı sene veya kurulsa KORU!
    if (isSameKurul && isSameYear) {
      union(i, j);
      mergeEvents.push({
        q1: p1.id,
        q2: p2.id,
        kurul: p1.normCid,
        year: p1.normYr,
        sim: stemSim.toFixed(2),
        reason: ansReason
      });
    } else {
      if (!crossExamRefs.has(i)) crossExamRefs.set(i, []);
      if (!crossExamRefs.has(j)) crossExamRefs.set(j, []);
      crossExamRefs.get(i).push({ target_id: p2.id, committee: p2.normCid, year: p2.normYr, sim: stemSim.toFixed(2) });
      crossExamRefs.get(j).push({ target_id: p1.id, committee: p1.normCid, year: p1.normYr, sim: stemSim.toFixed(2) });
    }
  }

  // Kümeleri oluştur
  const clusters = new Map();
  for (let idx = 0; idx < processed.length; idx++) {
    const root = find(idx);
    if (!clusters.has(root)) clusters.set(root, []);
    clusters.get(root).push(idx);
  }

  const finalQuestions = [];
  const mergedAudit = [];

  for (const memberIndices of clusters.values()) {
    if (memberIndices.length === 1) {
      const idx = memberIndices[0];
      const qObj = { ...processed[idx].raw };
      if (crossExamRefs.has(idx)) {
        qObj.crossExamReferences = crossExamRefs.get(idx);
        const tags = Array.isArray(qObj.tags) ? [...qObj.tags] : [];
        if (!tags.includes('Tekrar Sorulan Soru')) tags.push('Tekrar Sorulan Soru');
        qObj.tags = tags;
      }
      finalQuestions.push(qObj);
    } else {
      // Birleştir
      const members = memberIndices.map(idx => processed[idx]);
      members.sort((a, b) => b.score - a.score || b.stem.length - a.stem.length);
      const master = members[0];
      const secondaries = members.slice(1);

      const mergedQ = { ...master.raw };
      const mergedIds = Array.isArray(mergedQ.mergedQuestionIds) ? [...mergedQ.mergedQuestionIds] : [];
      secondaries.forEach(s => {
        if (!mergedIds.includes(s.id) && s.id !== master.id) mergedIds.push(s.id);
      });
      mergedQ.mergedQuestionIds = mergedIds;

      const sources = new Set();
      if (mergedQ.sourceFile || mergedQ.source) sources.add(mergedQ.sourceFile || mergedQ.source);
      secondaries.forEach(s => {
        const sf = s.raw.sourceFile || s.raw.source;
        if (sf) sources.add(sf);
      });
      mergedQ.sourceFiles = Array.from(sources);
      mergedQ.duplicateExamOccurrences = members.length;
      mergedQ.mergedVariants = secondaries.map(s => ({
        id: s.id,
        source: s.raw.sourceFile || s.raw.source,
        stem: s.stem
      }));

      finalQuestions.push(mergedQ);
      mergedAudit.push({
        masterId: master.id,
        committee: master.normCid,
        year: master.normYr,
        mergedCount: secondaries.length,
        mergedIds
      });
    }
  }

  return {
    finalQuestions,
    report: {
      initialCount: questions.length,
      finalCount: finalQuestions.length,
      mergedDuplicates: questions.length - finalQuestions.length,
      mergedClustersCount: mergedAudit.length,
      crossExamCount: crossExamRefs.size,
      mergedAudit
    }
  };
}

// Doğrudan çalıştırma
async function main() {
  const args = process.argv.slice(2);
  const isApply = args.includes('--apply') || args.includes('-a');
  const targetPath = path.resolve(__dirname, '..', 'src', 'data', 'pastQuestions.json');
  const dataPath = path.resolve(__dirname, '..', 'data', 'pastQuestions.json');

  console.log('='.repeat(70));
  console.log('🚀 TIP ÇIKMIŞ SORULARI AYNI SENE & AYNI KURUL BİRLEŞTİRME (Node.js)');
  console.log('='.repeat(70));
  console.log(`Mod: ${isApply ? 'DEĞİŞİKLİKLERİ UYGULA (--apply)' : 'DRY-RUN (Simülasyon)'}`);

  const targets = [targetPath, dataPath].filter(p => fs.existsSync(p));
  for (const t of targets) {
    console.log(`\n📂 Dosya inceleniyor: ${t}`);
    const questions = JSON.parse(fs.readFileSync(t, 'utf8'));
    const { finalQuestions, report } = deduplicateQuestions(questions);

    console.log(`   ✅ Başlangıç: ${report.initialCount} soru`);
    console.log(`   ✅ Aynı sene/kurulda birleştirilen: ${report.mergedDuplicates} mükerrer soru`);
    console.log(`   ✅ Nihai soru sayısı: ${report.finalCount}`);
    console.log(`   ✅ Farklı sene/kurulda korunan tekrarlar: ${report.crossExamCount}`);

    if (isApply && report.mergedDuplicates > 0) {
      const bak = `${t}.${Date.now()}.bak`;
      fs.copyFileSync(t, bak);
      console.log(`   💾 Yedek alındı: ${bak}`);
      fs.writeFileSync(t, JSON.stringify(finalQuestions, null, 2), 'utf8');
      console.log(`   ✨ Kaydedildi: ${t}`);
    } else if (!isApply) {
      console.log('   ℹ️ Değişiklikleri kaydetmek için scripti --apply ile çalıştırın.');
    }
  }
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  main().catch(console.error);
}
