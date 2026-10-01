/**
 * MedSoru Slayt İlişkisi Denetim ve Hatalı İlişkileri Kesme Scripti (Script 1)
 * (scripts/audit-and-disconnect-faulty-slides.mjs)
 * 
 * Amaç:
 * 1. Çıkmış sorular ile ilişkilendirilen her bir ders slaytını ve sayfasını kontrol eder.
 * 2. Bir hata olup olmadığını tespit eder (örn: soru içeriği ile ders slaytının uyuşmaması,
 *    olmayan ders notu/sayfası, çıkmış soru dosyasıyla eşleşmiş olma vb.).
 * 3. Hata durumunda ilgili ilişkiyi KESER (matchedNoteTitle, matchedSlidePage, lectureReference sıfırlanır).
 * 4. Geçerli olan ilişkileri korur, ilgili metinleri vurgular ve ayrıntılı denetim raporu üretir.
 */

import fs from 'fs';
import path from 'path';
import {
  ROOT_DIR,
  DATA_PAST_PATH,
  loadRealLectureNotes,
  buildNoteLookup,
  extractSalientTerms,
  buildHighlightedSnippet,
  savePastQuestions,
  turkishToLower
} from './slide-matching-utils.mjs';

const REPORT_PATH = path.join(ROOT_DIR, 'data', 'slide_audit_report.json');

export async function runSlideAudit(options = {}) {
  const { verbose = true, dryRun = false } = options;

  console.log('🔍 [Script 1: Slayt Denetimi] Başlatılıyor...');
  console.log(`📂 Veri yolu: ${DATA_PAST_PATH}`);

  // 1. Gerçek ders notlarını yükle ve indeksle
  const realNotes = loadRealLectureNotes();
  const noteLookup = buildNoteLookup(realNotes);
  console.log(`📚 Toplam ${realNotes.length} adet amfi ders sunumu belleğe yüklendi.`);

  // 2. Çıkmış soruları yükle
  if (!fs.existsSync(DATA_PAST_PATH)) {
    throw new Error(`pastQuestions.json bulunamadı: ${DATA_PAST_PATH}`);
  }
  const questions = JSON.parse(fs.readFileSync(DATA_PAST_PATH, 'utf8'));
  console.log(`📋 Toplam ${questions.length} soru inceleniyor...`);

  let totalAssociated = 0;
  let severedCount = 0;
  let verifiedCount = 0;
  let unassociatedCount = 0;

  const severedDetails = [];
  const verifiedDetails = [];

  for (let i = 0; i < questions.length; i++) {
    const q = questions[i];
    const noteTitle = q.lectureReference?.noteTitle || q.matchedNoteTitle;
    const pageNum = q.lectureReference?.pageNumber || q.matchedSlidePage;

    // Slayt ilişkisi yoksa atla
    if (!noteTitle && !pageNum) {
      unassociatedCount++;
      continue;
    }

    totalAssociated++;

    // Soru içeriğini derle
    const stem = q.reconstruction?.stem || q.rawQuestion?.stem || '';
    const optionsList = q.reconstruction?.options || q.rawQuestion?.options || [];
    const claimedAns = q.claimedAnswer || q.reconstruction?.correctAnswer || '';
    const correctOpt = optionsList.find(o => o.key === claimedAns);
    const answerText = correctOpt ? correctOpt.text : '';
    const questionText = `${q.topic || ''} ${stem} ${answerText}`;
    const { words: qWords, bigrams: qBigrams } = extractSalientTerms(questionText);

    // 1. Kontrol: Ders notu gerçek amfi notları arasında var mı?
    const note = noteLookup.findNote(noteTitle);
    if (!note) {
      // HATA: Ders notu amfi ders notları arasında yok (veya soru dosyasıyla eşleşmiş)
      severRelationship(q, `Ders notu ("${noteTitle}") amfi ders notları arşivinde bulunamadı veya çıkmış soru dosyasıdır.`);
      severedCount++;
      severedDetails.push({
        id: q.id,
        stem: stem.slice(0, 80),
        reason: `Ders notu ("${noteTitle}") bulunamadı/geçersiz`,
        previousMatch: { noteTitle, pageNum }
      });
      continue;
    }

    // 2. Kontrol: Sayfa numarası geçerli mi?
    const validPageNum = Number(pageNum);
    if (!validPageNum || validPageNum < 1 || validPageNum > (note.totalSlides || note.pages.length)) {
      severRelationship(q, `Geçersiz sayfa numarası: Slayt #${pageNum}, "${note.title}" toplam slayt: ${note.totalSlides || note.pages.length}`);
      severedCount++;
      severedDetails.push({
        id: q.id,
        stem: stem.slice(0, 80),
        reason: `Geçersiz sayfa numarası: #${pageNum} (Toplam: ${note.totalSlides})`,
        previousMatch: { noteTitle, pageNum }
      });
      continue;
    }

    const slidePage = (note.pages || []).find(p => p.pageNumber === validPageNum);
    if (!slidePage || !slidePage.content || slidePage.content.trim().length < 20) {
      severRelationship(q, `Slayt #${validPageNum} boş veya okunabilir metin içermiyor.`);
      severedCount++;
      severedDetails.push({
        id: q.id,
        stem: stem.slice(0, 80),
        reason: `Slayt #${validPageNum} boş içerik`,
        previousMatch: { noteTitle, pageNum }
      });
      continue;
    }

    // 3. Kontrol: Soru içeriği ile slayt sayfası içeriği uyuşuyor mu?
    const slideContent = slidePage.content;
    const lowerSlide = turkishToLower(slideContent);

    // Eşleşen terimler ve bigramları say
    const matchedBigrams = qBigrams.filter(bg => lowerSlide.includes(bg));
    const matchedWords = qWords.filter(w => lowerSlide.includes(w));

    // Konu & Başlık örtüşmesi
    const noteTitleNorm = turkishToLower(note.title);
    const topicNorm = turkishToLower(q.topic || '');
    const topicWords = q.topic ? extractSalientTerms(q.topic).words : [];
    const topicOverlap = topicWords.filter(tw => noteTitleNorm.includes(tw) || lowerSlide.includes(tw));

    // Karar Mantığı (Strict Validation):
    // Gerçek bir slayt ilişkisi için:
    // a) En az 1 anlamlı bigram (örn: "papiller tiroid", "orphan annie", "kuru öksürük")
    // VEYA
    // b) En az 3 spesifik soru kelimesi ve konu/başlık örtüşmesi
    const isValidMatch = 
      matchedBigrams.length >= 1 || 
      (matchedWords.length >= 3 && topicOverlap.length >= 1) ||
      (matchedWords.length >= 4);

    if (!isValidMatch) {
      // HATA: İçerik uyuşmuyor!
      const mismatchReason = `Soru içeriği ile slayt içeriği uyuşmuyor. Eşleşen kelime: ${matchedWords.length} (gereken en az 3-4), Bigram: ${matchedBigrams.length}`;
      severRelationship(q, mismatchReason);
      severedCount++;
      severedDetails.push({
        id: q.id,
        stem: stem.slice(0, 80),
        reason: mismatchReason,
        previousMatch: { noteTitle: note.title, pageNum: validPageNum },
        termsFound: matchedWords
      });
    } else {
      // DOĞRU İLİŞKİ: Korunur ve metin vurgulanır
      verifiedCount++;
      const allMatchedTerms = Array.from(new Set([...matchedBigrams, ...matchedWords]));
      const { highlightedText, snippet } = buildHighlightedSnippet(slideContent, allMatchedTerms);

      q.matchedNoteTitle = note.title;
      q.matchedSlidePage = validPageNum;
      q.lectureReference = {
        noteId: note.id,
        noteTitle: note.title,
        discipline: note.discipline || q.discipline,
        committeeId: note.committeeId || q.committeeId,
        pageNumber: validPageNum,
        totalSlides: note.totalSlides || note.pages.length,
        matchedSnippet: snippet,
        highlightedText,
        matchedTerms: allMatchedTerms.slice(0, 8),
        confidenceScore: Math.min(100, 70 + matchedBigrams.length * 15 + matchedWords.length * 5),
        reasoning: `Amfi Slayt Doğrulaması: "${note.title}" slayt #${validPageNum} içeriğinde (${allMatchedTerms.slice(0, 4).join(', ')}) ifadeleri soru içeriği ile doğrudan örtüşmektedir.`,
        driveFileUrl: note.driveFileUrl || null
      };

      q.slideAudit = {
        status: 'verified',
        auditedAt: new Date().toISOString(),
        matchedTermsCount: allMatchedTerms.length
      };

      verifiedDetails.push({
        id: q.id,
        noteTitle: note.title,
        pageNumber: validPageNum,
        matchedTerms: allMatchedTerms.slice(0, 5)
      });
    }
  }

  // İlişki kesme yardımcı fonksiyonu
  function severRelationship(question, reason) {
    question.slideAudit = {
      status: 'disconnected',
      auditedAt: new Date().toISOString(),
      reason,
      previousMatch: {
        noteTitle: question.matchedNoteTitle || question.lectureReference?.noteTitle,
        pageNumber: question.matchedSlidePage || question.lectureReference?.pageNumber
      }
    };
    question.matchedNoteTitle = null;
    question.matchedSlidePage = null;
    question.lectureReference = null;
  }

  // 4. Sonuçları kaydet
  if (!dryRun) {
    savePastQuestions(questions);
    console.log('💾 Güncellenen sorular JSON dosyalarına kaydedildi.');
  } else {
    console.log('⚠️ [DRY RUN] Dosyalara yazma işlemi yapılmadı.');
  }

  // 5. Rapor oluştur
  const auditReport = {
    executedAt: new Date().toISOString(),
    totalQuestions: questions.length,
    unassociatedInitially: unassociatedCount,
    totalAssociated,
    severedCount,
    verifiedCount,
    severedSample: severedDetails.slice(0, 20),
    verifiedSample: verifiedDetails.slice(0, 20)
  };

  fs.writeFileSync(REPORT_PATH, JSON.stringify(auditReport, null, 2), 'utf8');

  console.log('\n==============================================');
  console.log('📊 [Script 1: Denetim ve Kesme Özeti]');
  console.log('==============================================');
  console.log(`Toplam Soru               : ${questions.length}`);
  console.log(`Başlangıçta İlişkisiz Soru : ${unassociatedCount}`);
  console.log(`İncelenen İlişkili Soru   : ${totalAssociated}`);
  console.log(`❌ Kesilen Hatalı İlişki   : ${severedCount}`);
  console.log(`✅ Doğrulanan Geçerli İlişki: ${verifiedCount}`);
  console.log(`📄 Ayrıntılı Rapor        : ${REPORT_PATH}`);
  console.log('==============================================\n');

  return auditReport;
}

// Komut satırından doğrudan çalıştırıldığında
if (process.argv[1] && process.argv[1].endsWith('audit-and-disconnect-faulty-slides.mjs')) {
  runSlideAudit({ verbose: true, dryRun: false }).catch(err => {
    console.error('Kritik Hata:', err);
    process.exit(1);
  });
}
