/**
 * MedSoru Slayt Eşleştirme, Bağlama ve Vurgulama Scripti (Script 2)
 * (scripts/match-and-link-lecture-slides.mjs)
 * 
 * Amaç:
 * 1. Henüz ders ilişkisi olmayan ya da hatalı ders ilişkisine sahip olduğu
 *    tespit edilen (Script 1 ile ilişkisi kesilmiş) soruları inceler.
 * 2. Paylaşılan tüm amfi ders notlarını (788 sunum, 40.000+ slayt sayfası) tarar.
 * 3. Sorunun konusu ile ders notunun konusu eşleşiyorsa VE soru gerçekten o slayttan
 *    bir bilgi içeriyorsa aralarında güçlü bir ilişki kurar.
 * 4. İlişkili slaytta hangi metnin ilişkili olduğunu tespit eder ve ==...== ile vurgular (highlight).
 * 5. lectureReference, matchedNoteTitle ve matchedSlidePage alanlarını eksiksiz günceller.
 */

import fs from 'fs';
import path from 'path';
import {
  ROOT_DIR,
  DATA_PAST_PATH,
  loadRealLectureNotes,
  cleanTitle,
  turkishToLower,
  extractSalientTerms,
  buildHighlightedSnippet,
  savePastQuestions
} from './slide-matching-utils.mjs';

const REPORT_PATH = path.join(ROOT_DIR, 'data', 'slide_match_report.json');

/**
 * Bütün amfi slaytları üzerinde ters dizin (inverted index) inşa eder
 */
export function buildSlideInvertedIndex(realNotes) {
  const index = new Map();
  const allPages = [];

  for (let nIdx = 0; nIdx < realNotes.length; nIdx++) {
    const note = realNotes[nIdx];
    const pages = note.pages || [];
    for (let p = 0; p < pages.length; p++) {
      const page = pages[p];
      if (!page.content || page.content.trim().length < 20) continue;

      const pIdx = allPages.length;
      allPages.push({
        pIdx,
        nIdx,
        noteId: note.id,
        noteTitle: note.title,
        cleanNoteTitle: cleanTitle(note.title),
        discipline: note.discipline,
        committeeId: note.committeeId,
        pageNumber: page.pageNumber,
        totalSlides: note.totalSlides || pages.length,
        content: page.content,
        driveFileUrl: note.driveFileUrl || null
      });

      const { words, bigrams } = extractSalientTerms(page.content);
      const seen = new Set();

      for (const w of words) {
        if (seen.has(w)) continue;
        seen.add(w);
        let list = index.get(w);
        if (!list) { list = []; index.set(w, list); }
        list.push(pIdx);
      }

      for (const bg of bigrams) {
        if (seen.has(bg)) continue;
        seen.add(bg);
        let list = index.get(bg);
        if (!list) { list = []; index.set(bg, list); }
        list.push(pIdx);
      }
    }
  }

  return { index, allPages };
}

/**
 * Tek bir soru için en uygun slayt sayfasını bulur
 */
export function findBestMatchingSlideForQuestion(question, invertedIndex, allPages, minScore = 60) {
  const stem = question.reconstruction?.stem || question.rawQuestion?.stem || '';
  const claimedAns = question.claimedAnswer || question.reconstruction?.correctAnswer;
  const opts = question.reconstruction?.options || question.rawQuestion?.options || [];
  const correctOpt = opts.find(o => o.key === claimedAns);
  const ansText = correctOpt ? correctOpt.text : '';

  const { words: qWords, bigrams: qBigrams } = extractSalientTerms(`${stem} ${ansText}`);
  const topicWords = question.topic ? extractSalientTerms(question.topic).words : [];

  if (qWords.length === 0 && qBigrams.length === 0) return null;

  const pageScores = new Map();

  // 1. Bigram eşleşmeleri (büyük puan)
  for (const bg of qBigrams) {
    const list = invertedIndex.get(bg);
    if (!list) continue;
    const bgWeight = list.length < 30 ? 45 : 25;
    for (const pIdx of list) {
      pageScores.set(pIdx, (pageScores.get(pIdx) || 0) + bgWeight);
    }
  }

  // 2. Tıbbi anahtar kelime eşleşmeleri (IDF ağırlıklı)
  for (const w of qWords) {
    const list = invertedIndex.get(w);
    if (!list) continue;
    // Nadir kelimeler (örn: Orphan, TMPRSS2, Feokromositoma) daha yüksek puan alır
    const idfWeight = list.length < 20 ? 25 : list.length < 100 ? 12 : list.length < 400 ? 6 : 2;
    for (const pIdx of list) {
      pageScores.set(pIdx, (pageScores.get(pIdx) || 0) + idfWeight);
    }
  }

  if (pageScores.size === 0) return null;

  // En yüksek puanlı 15 adayı derin incelemeye al
  const topCandidates = Array.from(pageScores.entries())
    .sort((a, b) => b[1] - a[1])
    .slice(0, 15);

  let bestMatch = null;
  let highestScore = 0;

  for (const [pIdx, baseScore] of topCandidates) {
    const page = allPages[pIdx];
    const noteTitleNorm = turkishToLower(page.cleanNoteTitle || page.noteTitle);
    const qTopicNorm = turkishToLower(question.topic || '');
    const qDisciplineNorm = turkishToLower(question.discipline || '');
    const pageDisciplineNorm = turkishToLower(page.discipline || '');

    // Şart 1 Kontrolü: Sorunun konusu ile ders notunun konusunun eşleşmesi
    let topicScore = 0;
    let topicMatched = false;

    for (const tw of topicWords) {
      if (noteTitleNorm.includes(tw)) {
        topicScore += 30;
        topicMatched = true;
      }
    }

    // Doğrudan başlık / konu alt dize eşleşmesi
    if (qTopicNorm && (noteTitleNorm.includes(qTopicNorm) || qTopicNorm.includes(noteTitleNorm))) {
      topicScore += 45;
      topicMatched = true;
    }

    // Disiplin uyumu
    let discScore = 0;
    if (qDisciplineNorm && pageDisciplineNorm) {
      if (pageDisciplineNorm.includes(qDisciplineNorm) || qDisciplineNorm.includes(pageDisciplineNorm)) {
        discScore += 25;
      } else if (
        (qDisciplineNorm.includes('patoloji') && pageDisciplineNorm.includes('cerrahi')) ||
        (qDisciplineNorm.includes('farmakoloji') && pageDisciplineNorm.includes('dahiliye'))
      ) {
        discScore += 10; // Yakın klinik branş
      } else {
        // Tamamen alakasız branş cezası (örn: Genetik sorusuna Kulak Burun Boğaz slaytı)
        discScore -= 30;
      }
    }

    // Komite uyumu
    let commScore = 0;
    if (question.committeeId && page.committeeId && question.committeeId === page.committeeId) {
      commScore += 20;
    }

    // Şart 2 Kontrolü: Sorunun kökündeki veya doğru cevabındaki bilginin slaytta doğrudan geçmesi
    const lowerPage = turkishToLower(page.content);
    const confirmedBigrams = qBigrams.filter(bg => lowerPage.includes(bg));
    const confirmedWords = qWords.filter(w => lowerPage.includes(w));

    // Doğru cevap terimi slaytta geçiyor mu?
    let answerInSlide = false;
    if (ansText && ansText.length >= 4) {
      const { words: ansWords } = extractSalientTerms(ansText);
      if (ansWords.some(aw => lowerPage.includes(aw))) {
        answerInSlide = true;
      }
    }

    let currentScore = baseScore;
    if (answerInSlide) {
      currentScore += 25;
    }

    // Toplam bileşik skor
    const totalScore = currentScore + topicScore + discScore + commScore;

    // Katı Kabul Eşiği:
    // 1) En az 1 bigram veya en az 3 spesifik kelime doğrulanmalı
    // 2) Konu örtüşmesi veya yüksek oranda doğrulanmış tıbbi kavram olmalı
    const meetsVerification = 
      (confirmedBigrams.length >= 1 && (confirmedWords.length >= 2 || topicMatched)) ||
      (confirmedWords.length >= 4) ||
      (confirmedWords.length >= 3 && topicMatched);

    if (meetsVerification && totalScore >= minScore && totalScore > highestScore) {
      highestScore = totalScore;
      const allMatchedTerms = Array.from(new Set([...confirmedBigrams, ...confirmedWords]));
      bestMatch = {
        page,
        score: totalScore,
        matchedTerms: allMatchedTerms,
        topicMatched,
        answerInSlide
      };
    }
  }

  return bestMatch;
}

/**
 * İlişkisiz veya hatalı sorular için eşleştirme ve bağlama ana fonksiyonu
 */
export async function runSlideMatching(options = {}) {
  const { verbose = true, dryRun = false, minScore = 60, limit = null } = options;

  console.log('🔗 [Script 2: Slayt Eşleştirme ve Vurgulama] Başlatılıyor...');
  console.log(`📂 Veri yolu: ${DATA_PAST_PATH}`);

  // 1. Gerçek ders notlarını yükle ve indeksle
  const realNotes = loadRealLectureNotes();
  console.log(`📚 Toplam ${realNotes.length} adet amfi ders sunumu analiz ediliyor...`);
  console.time('İndeksleme Süresi');
  const { index, allPages } = buildSlideInvertedIndex(realNotes);
  console.timeEnd('İndeksleme Süresi');
  console.log(`⚡ Toplam ${allPages.length} slayt sayfası ve ${index.size} tıbbi terim indekslendi.`);

  // 2. Çıkmış soruları yükle
  const questions = JSON.parse(fs.readFileSync(DATA_PAST_PATH, 'utf8'));

  // Eşleştirilmesi gereken sorular: Henüz ilişkisi olmayan veya ilişkisi kesilmiş sorular
  const targetQuestions = [];
  for (let i = 0; i < questions.length; i++) {
    const q = questions[i];
    const hasRelation = Boolean(q.lectureReference?.noteTitle || q.matchedNoteTitle);
    const wasDisconnected = q.slideAudit?.status === 'disconnected';

    if (!hasRelation || wasDisconnected) {
      targetQuestions.push(q);
    }
  }

  console.log(`🎯 İncelenecek / Slayt eşleşmesi aranacak soru sayısı: ${targetQuestions.length}`);

  const processList = limit ? targetQuestions.slice(0, limit) : targetQuestions;
  let newlyMatchedCount = 0;
  let unmatchedCount = 0;

  const matchDetails = [];

  for (let i = 0; i < processList.length; i++) {
    const q = processList[i];
    const match = findBestMatchingSlideForQuestion(q, index, allPages, minScore);

    if (match) {
      newlyMatchedCount++;
      const { page, score, matchedTerms } = match;

      // İlgili metni tespit et ve vurgula
      const { highlightedText, snippet } = buildHighlightedSnippet(page.content, matchedTerms);

      const confidenceScore = Math.min(99, Math.max(75, Math.round(50 + score * 0.3)));

      q.lectureReference = {
        noteId: page.noteId,
        noteTitle: page.noteTitle,
        discipline: page.discipline || q.discipline,
        committeeId: page.committeeId || q.committeeId,
        pageNumber: page.pageNumber,
        totalSlides: page.totalSlides,
        matchedSnippet: snippet,
        highlightedText,
        matchedTerms: matchedTerms.slice(0, 8),
        confidenceScore,
        reasoning: `Amfi Slayt Eşleşmesi: Soru konusu (${q.topic || q.discipline}) ile "${page.noteTitle}" dersinin ${page.pageNumber}. slaytındaki (${matchedTerms.slice(0, 4).join(', ')}) ifadeleri birebir örtüşmektedir.`,
        driveFileUrl: page.driveFileUrl || null
      };

      q.matchedNoteTitle = page.noteTitle;
      q.matchedSlidePage = page.pageNumber;
      q.slideAudit = {
        status: 'linked',
        linkedAt: new Date().toISOString(),
        score,
        matchedTermsCount: matchedTerms.length
      };

      matchDetails.push({
        id: q.id,
        topic: q.topic,
        stem: (q.reconstruction?.stem || q.rawQuestion?.stem || '').slice(0, 80),
        matchedNote: page.noteTitle,
        pageNumber: page.pageNumber,
        score,
        highlightedText: highlightedText.slice(0, 100),
        snippet: snippet.slice(0, 140)
      });
    } else {
      unmatchedCount++;
      // Güvenilir eşleşme bulunamayan sorular ilişkisiz olarak bırakılır (sahte eşleşme yapılmaz)
      q.slideAudit = {
        status: 'unmatched',
        auditedAt: new Date().toISOString(),
        note: 'Mevcut ders slaytlarında yeterli eşleşme bulunamadı.'
      };
    }

    if (verbose && (i + 1) % 250 === 0) {
      console.log(`⏳ ${i + 1}/${processList.length} soru işlendi... (Yeni eşleşen: ${newlyMatchedCount})`);
    }
  }

  // 3. Sonuçları kaydet
  if (!dryRun) {
    savePastQuestions(questions);
    console.log('💾 Eşleştirilen sorular veritabanına kaydedildi.');
  } else {
    console.log('⚠️ [DRY RUN] Dosyalara yazma işlemi yapılmadı.');
  }

  // 4. Eşleştirme raporu oluştur
  const matchReport = {
    executedAt: new Date().toISOString(),
    totalAuditedForMatch: processList.length,
    newlyMatchedCount,
    unmatchedCount,
    minScoreThreshold: minScore,
    sampleMatches: matchDetails.slice(0, 30)
  };

  fs.writeFileSync(REPORT_PATH, JSON.stringify(matchReport, null, 2), 'utf8');

  console.log('\n==============================================');
  console.log('📊 [Script 2: Eşleştirme ve Vurgulama Özeti]');
  console.log('==============================================');
  console.log(`İncelenen Hedef Soru       : ${processList.length}`);
  console.log(`🎯 Başarıyla Eşleşen ve Bağlanan: ${newlyMatchedCount}`);
  console.log(`⚪ Slaytı Bulunamayan/İlişkisiz: ${unmatchedCount}`);
  console.log(`📄 Ayrıntılı Eşleşme Raporu: ${REPORT_PATH}`);
  console.log('==============================================\n');

  return matchReport;
}

// Komut satırından doğrudan çalıştırıldığında
if (process.argv[1] && process.argv[1].endsWith('match-and-link-lecture-slides.mjs')) {
  runSlideMatching({ verbose: true, dryRun: false }).catch(err => {
    console.error('Kritik Hata:', err);
    process.exit(1);
  });
}
