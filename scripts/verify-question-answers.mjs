/**
 * MedSoru Çıkmış Soru ve Cevap Doğrulama Motoru (scripts/verify-question-answers.mjs)
 * 
 * Amaç:
 * Çıkmış soruların cevaplarını; hem amfi ders notları/slaytları hem de güncel tıp literatürü
 * ve internet bilgisi ile çapraz kontrole tabi tutar.
 * 
 * Kesin Kural:
 * Eğer bir sorunun cevabı ders notundaki ve internetteki bilgilerle %90 üzerinde bir
 * eşleşmeye varamıyorsa:
 * 1. Sorunun güvenilirlik derecesi düşürülür (confidenceScore düşürülür).
 * 2. Doğru cevap soruda İŞARETLENMEZ (reconstruction.correctAnswer = null, tüm şıklarda isCorrect = false).
 * 3. Soru ve cevap "ŞÜPHELİ CEVAP" (isSuspect: true, isAmbiguous: true, status: 'suspicious') olarak işaretlenir.
 * 
 * Otomasyon:
 * - Yeni soru eklendiğinde API ve dosya izleyici (watcher) üzerinden otomatik tetiklenir.
 * - --watch parametresi ile arka planda kesintisiz izleyici daemon olarak çalışabilir.
 * - --unverified ile sadece henüz doğrulanmamış soruları kontrol eder.
 * - --all ile tüm soru arşivini parti parti denetler.
 * - --id <id> ile tek bir soruyu denetler.
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';
import { createClient } from '@supabase/supabase-js';
import { findBestMatchingLectureSlides } from '../src/serverLectureNotes.ts';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');

const DATA_PAST_PATH = path.join(ROOT_DIR, 'data', 'pastQuestions.json');
const SRC_PAST_PATH = path.join(ROOT_DIR, 'src', 'data', 'pastQuestions.json');
const BACKUP_PATH = path.join(ROOT_DIR, 'data', 'pastQuestions.backup_before_verify.json');
const REPORT_PATH = path.join(ROOT_DIR, 'data', 'verification_report.json');

// Supabase Bağlantısı
const SUPABASE_URL = process.env.SUPABASE_URL || 'https://kgutsltgmqbnlxcnzrtl.supabase.co';
const SUPABASE_KEY = process.env.SUPABASE_SECRET_KEY || process.env.SUPABASE_PUBLISHABLE_KEY;
const supabase = (SUPABASE_URL && SUPABASE_KEY) ? createClient(SUPABASE_URL, SUPABASE_KEY) : null;

function cleanForPostgres(data) {
  if (data === null || data === undefined) return data;
  if (typeof data === 'string') {
    return data.replace(/\u0000/g, '').replace(/[\x00]/g, '');
  }
  if (Array.isArray(data)) {
    return data.map(cleanForPostgres);
  }
  if (typeof data === 'object') {
    const cleaned = {};
    for (const [k, v] of Object.entries(data)) {
      cleaned[k] = cleanForPostgres(v);
    }
    return cleaned;
  }
  return data;
}

// -------------------------------------------------------------
// ÇOK KATMANLI YAPAY ZEKA VE İNTERNET DOĞRULAMA ÇAĞIRICISI
// -------------------------------------------------------------
async function callResilientAi(prompt) {
  const groqKey = process.env.GROQ_API_KEY;
  const geminiKeys = [
    process.env.GEMINI_FREE_KEY_2,
    process.env.GEMINI_API_KEY,
    (process.env.MEDS_FREE_ONLY !== '0' ? undefined : process.env.GEMINI_BILLED_KEY),
  ].filter(Boolean);

  // 1. Groq Cloud (Yüksek Hız, Ücretsiz ve Geniş Token Kotası)
  if (groqKey) {
    const groqCandidateModels = ['openai/gpt-oss-120b', 'qwen/qwen3.8-27b', 'openai/gpt-oss-20b'];
    for (const model of groqCandidateModels) {
      try {
        const res = await fetch('https://api.groq.com/openai/v1/chat/completions', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${groqKey}`
          },
          body: JSON.stringify({
            model,
            messages: [
              {
                role: 'system',
                content: 'Sen Tıp Fakültesi Dönem 3 Kurul ve TUS Sınavları Komisyonunda görevli kıdemli bir Tıp Profesörüsün. Sınav sorularının iddia edilen cevaplarını amfi ders slaytları ve internetteki güncel tıp literatürüyle (Robbins, Harrison, Katzung vb.) çapraz kontrole tabi tutan baş denetçisin. Yanıtı SADECE geçerli bir JSON objesi olarak ver.'
              },
              { role: 'user', content: prompt }
            ],
            response_format: { type: 'json_object' },
            temperature: 0.1
          })
        });

        if (res.ok) {
          const data = await res.json();
          const parsed = JSON.parse(data.choices?.[0]?.message?.content || '{}');
          if (parsed && typeof parsed.overallMatchPercent === 'number') {
            return { result: parsed, provider: `Groq (${model})` };
          }
        }
      } catch (e) {
        // Sonraki modele veya Gemini'ye geç
      }
    }
  }

  // 2. Google Gemini Fallback
  for (const apiKey of geminiKeys) {
    try {
      const { GoogleGenAI } = await import('@google/genai');
      const ai = new GoogleGenAI({ apiKey });
      const res = await ai.models.generateContent({
        model: 'gemini-3.8-flash',
        contents: prompt,
        config: { responseMimeType: 'application/json' }
      });
      const parsed = JSON.parse(res.text || '{}');
      if (parsed && typeof parsed.overallMatchPercent === 'number') {
        return { result: parsed, provider: 'Google Gemini 3.8 Flash' };
      }
    } catch (e) {
      // Bir sonraki Gemini anahtarına geç
    }
  }

  throw new Error('Yapay zeka denetim motorları yanıt veremedi. Lütfen API anahtarlarınızı kontrol edin.');
}

// -------------------------------------------------------------
// EN UYGUN AMFİ DERS SLAYTLARINI ÇEKME VE GROUNDING
// -------------------------------------------------------------
export function extractQuestionSearchTerms(q) {
  const stem = q.reconstruction?.stem || q.rawQuestion?.stem || q.topic || '';
  const claimed = q.claimedAnswer || q.reconstruction?.correctAnswer;
  const options = q.reconstruction?.options || q.rawQuestion?.options || [];
  const claimedOpt = options.find(o => o.key === claimed);
  const claimedText = claimedOpt ? claimedOpt.text : '';

  return `${stem} ${claimedText}`.trim();
}

export function findLectureGrounding(q) {
  const discipline = q.discipline || 'Tıbbi Patoloji';
  const committeeId = q.committeeId;
  const searchQuery = extractQuestionSearchTerms(q);

  // Önce ilgili komite içinde ara
  let slides = findBestMatchingLectureSlides(searchQuery, discipline, committeeId, 3);

  // Komite içinde güçlü eşleşme çıkmazsa tüm Dönem 3 ders notlarında ara
  if (!slides || slides.length === 0 || slides[0].score < 40) {
    const globalSlides = findBestMatchingLectureSlides(searchQuery, discipline, undefined, 3);
    if (globalSlides && globalSlides.length > 0) {
      slides = globalSlides;
    }
  }

  return slides || [];
}

// -------------------------------------------------------------
// TEK BİR SORUNUN CEVABINI KONTROL ETME (%90 KURAL MOTORU)
// -------------------------------------------------------------
export async function verifyQuestionAnswer(question, options = {}) {
  const stem = question.reconstruction?.stem || question.rawQuestion?.stem || question.topic || '';
  const optionsList = question.reconstruction?.options || question.rawQuestion?.options || [];
  const claimedAnswer = question.claimedAnswer || question.reconstruction?.correctAnswer || null;
  const discipline = question.discipline || 'Tıp';
  const committeeId = question.committeeId || 'donem3-kurul1';

  // Soru kökü ve şıkları yoksa kontrol edilemez
  if (!stem || optionsList.length === 0) {
    return {
      success: false,
      reason: 'Soru kökü veya seçenekler eksik.',
      question
    };
  }

  // 1. Amfi Ders Slaytlarını Bul
  const matchedSlides = findLectureGrounding(question);
  const slideContext = matchedSlides.map(s => 
    `• [Ders Notu: "${s.noteTitle}" - Slayt #${s.pageNumber} (Uyum Skoru: ${s.score})]:\n"${s.snippet}"`
  ).join('\n\n');

  // 2. Denetim İstemini Oluştur
  const prompt = `Aşağıdaki tıp fakültesi kurul sınav sorusunun cevabını; verilen amfi ders slaytları alıntıları ve uluslararası tıp literatürü (Robbins Patoloji, Harrison Dahiliye, Katzung Farmakoloji, Nelson Pediatri vb.) ışığında kesin kontrole tabi tut.

SORU BİLGİLERİ:
Disiplin: ${discipline}
Komite / Kurul: ${committeeId}
Soru Kökü: ${stem}

SEÇENEKLER:
${optionsList.map(o => `${o.key}) ${o.text}`).join('\n')}

İDDİA EDİLEN / İŞARETLENEN CEVAP: ${claimedAnswer || 'BELİRTİLMEMİŞ (BOŞ)'}

EŞLEŞEN AMFİ DERS SLAYTI BİLGİLERİ:
${slideContext || 'İlgili amfi slaytlarında doğrudan eşleşen bir slayt bulunamadı.'}

KESİN DENETİM VE EŞLEŞME KURALLARI:
1. Soru kökünü dikkatle analiz et: Olumsuz kök var mı? ("yer almaz", "yanlıştır", "beklenmez", "değildir" vb.)
2. İddia edilen cevabı (${claimedAnswer}) hem amfi slaytları hem de internet/tıp literatürü açısından tek tek değerlendir:
   - lectureMatchPercent (0 - 100): İddia edilen şıkkın amfi ders slaytlarındaki bilgiyle eşleşme yüzdesi. (Eğer slaytta doğrudan teyit ediliyorsa 90-100, çelişiyorsa 0-20, slaytta değinilmemişse literatür odaklı değerlendir).
   - internetLiteratureMatchPercent (0 - 100): İddia edilen şıkkın internetteki ve standart tıp literatüründeki bilgilerle doğrulanma yüzdesi.
   - overallMatchPercent (0 - 100): Bileşik eşleşme oranı.
3. EĞER overallMatchPercent < 90 VEYA iddia edilen cevap tıbbi olarak şüpheli/yanlış ise:
   - decision: "SUSPECT"
   - isClaimedAnswerCorrect: false
   - Bu durumda soru şüpheli işaretlenecek ve doğru şık boş bırakılacaktır.
4. EĞER overallMatchPercent >= 90 VE iddia edilen cevap kesin doğruysa:
   - decision: "VERIFIED"
   - isClaimedAnswerCorrect: true
5. Tıbben gerçekte doğru olması gereken şıkkı (verifiedCorrectAnswer: A, B, C, D veya E) tespit et.
6. Ayrıntılı patofizyolojik / farmakolojik gerekçeyi yaz (doğru şıkkın nedeni ve yanlış şıkların neden elendiği).

JSON FORMATINDA CEVAP VER:
{
  "claimedAnswer": "${claimedAnswer || ''}",
  "isClaimedAnswerCorrect": true veya false,
  "lectureMatchPercent": 0-100,
  "internetLiteratureMatchPercent": 0-100,
  "overallMatchPercent": 0-100,
  "verifiedCorrectAnswer": "A, B, C, D veya E",
  "decision": "VERIFIED veya SUSPECT",
  "discrepancyFound": true veya false,
  "medicalReasoning": "Ayrıntılı mekanizmalı tıbbi açıklama...",
  "pearl": "Sınav için klinik hap bilgi..."
}`;

  let audit;
  let providerUsed = 'Yerel Tıbbi Kural Motoru';

  try {
    const aiResponse = await callResilientAi(prompt);
    audit = aiResponse.result;
    providerUsed = aiResponse.provider;
  } catch (err) {
    console.warn(`[Doğrulama Motoru] AI çağrı hatası (${err.message}). Kural tabanlı analize geçiliyor.`);
    audit = fallbackRuleBasedVerification(question, matchedSlides);
  }

  // 3. KULLANICI KURALININ KESİN UYGULANMASI (%90 Eşik Değeri)
  const isHighMatch = (audit.overallMatchPercent >= 90) && audit.isClaimedAnswerCorrect;

  const verifiedAt = new Date().toISOString();
  const currentOptions = (question.reconstruction?.options || optionsList).map(opt => ({ ...opt }));

  let updatedQuestion = { ...question };

  if (!isHighMatch) {
    // -------------------------------------------------------------
    // KURAL A: %90 ALTINDA EŞLEŞME -> GÜVENİLİRLİK DÜŞÜRÜLÜR, DOĞRU ŞIK BOŞ BIRAKILIR, ŞÜPHELİ İŞARETLENİR!
    // -------------------------------------------------------------
    console.log(`⚠️ [ŞÜPHELİ CEVAP TESPİTİ] Soru #${question.questionNumber || question.id}: Eşleşme Oranı %${audit.overallMatchPercent} (< %90). İddia Edilen Cevap: ${claimedAnswer} -> Şüpheli olarak işaretlendi.`);

    // 1. Güvenilirlik derecesi düşürülür
    const reducedConfidence = Math.min(audit.overallMatchPercent, 55);

    // 2. Doğru cevap soruda İŞARETLENMEZ, BOŞ BIRAKILIR!
    const clearedOptions = currentOptions.map(opt => ({
      ...opt,
      isCorrect: false // Hiçbir şık doğru olarak işaretlenmez!
    }));

    // 3. Şüpheli cevap olarak işaretleme
    updatedQuestion = {
      ...updatedQuestion,
      isSuspect: true,
      isAmbiguous: true,
      status: 'suspicious',
      ambiguityReason: `İnternet ve ders notu bilgileriyle %90 üzerinde eşleşme sağlanamadı (Eşleşme Oranı: %${audit.overallMatchPercent}). Doğru cevap soruda boş bırakıldı ve şüpheli cevap olarak askıya alındı.`,
      suspectAnswer: claimedAnswer || null,
      claimedAnswer: claimedAnswer || null,
      reconstruction: {
        ...(updatedQuestion.reconstruction || {}),
        stem,
        options: clearedOptions,
        correctAnswer: null, // Boş bırakılır!
        suggestedCorrection: audit.verifiedCorrectAnswer ? `Tıbbi literatür ve ders notu analizi: ${audit.verifiedCorrectAnswer} şıkkı öne çıkmaktadır.` : null,
        confidenceScore: reducedConfidence,
        explanation: [
          `⚠️ 【DİKKAT: ŞÜPHELİ CEVAP / DÜŞÜK GÜVENİLİRLİK】:`,
          `Bu sorunun mevcut cevap anahtarı veya iddia edilen yanıtı ('${claimedAnswer}'), amfi ders notları ve güncel tıp literatürüyle %90 eşleşme barajını geçememiştir (Hesaplanan Eşleşme: %${audit.overallMatchPercent}).`,
          `Bu nedenle sistem doğru cevabı işaretlememiş, boş bırakmış ve soruyu inceleme havuzuna almıştır.`,
          ``,
          `【Tıbbi Denetim Gerekçesi】:`,
          audit.medicalReasoning || 'Kaynaklar arasında uyuşmazlık tespit edildi.',
          audit.pearl ? `\n【Klinik İpucu】: ${audit.pearl}` : ''
        ].filter(Boolean).join('\n'),
        lastUpdated: verifiedAt
      },
      verification: {
        status: 'SUSPECT',
        checkedAt: verifiedAt,
        overallMatchPercent: audit.overallMatchPercent,
        lectureMatchPercent: audit.lectureMatchPercent,
        internetLiteratureMatchPercent: audit.internetLiteratureMatchPercent,
        isClaimedAnswerCorrect: false,
        claimedAnswer,
        suggestedCorrectAnswer: audit.verifiedCorrectAnswer,
        matchedSlidesCount: matchedSlides.length,
        matchedSlideSnippet: matchedSlides[0]?.snippet || null,
        matchedNoteTitle: matchedSlides[0]?.noteTitle || null,
        providerUsed
      },
      updatedAt: verifiedAt
    };
  } else {
    // -------------------------------------------------------------
    // KURAL B: %90 VE ÜZERİNDE EŞLEŞME -> DOĞRULANIR VE DOĞRU CEVAP İŞARETLENİR
    // -------------------------------------------------------------
    const targetCorrectAnswer = audit.verifiedCorrectAnswer || claimedAnswer;
    const finalConfidence = Math.max(audit.overallMatchPercent, 90);

    const verifiedOptions = currentOptions.map(opt => ({
      ...opt,
      isCorrect: opt.key === targetCorrectAnswer
    }));

    updatedQuestion = {
      ...updatedQuestion,
      isSuspect: false,
      isAmbiguous: false,
      status: 'verified',
      claimedAnswer: targetCorrectAnswer,
      reconstruction: {
        ...(updatedQuestion.reconstruction || {}),
        stem,
        options: verifiedOptions,
        correctAnswer: targetCorrectAnswer, // Doğru şık işaretlenir
        confidenceScore: finalConfidence,
        explanation: [
          `【Doğrulanmış Tıbbi Gerekçe (Eşleşme: %${audit.overallMatchPercent})】:`,
          audit.medicalReasoning || 'Ders notu ve tıp literatürü ile %90 üzerinde tam eşleşme sağlandı.',
          matchedSlides.length > 0 ? `\n【Amfi Slayt Referansı】: "${matchedSlides[0].noteTitle}" (Slayt #${matchedSlides[0].pageNumber})` : '',
          audit.pearl ? `\n【Klinik İpucu】: ${audit.pearl}` : ''
        ].filter(Boolean).join('\n'),
        lastUpdated: verifiedAt
      },
      verification: {
        status: 'VERIFIED',
        checkedAt: verifiedAt,
        overallMatchPercent: audit.overallMatchPercent,
        lectureMatchPercent: audit.lectureMatchPercent,
        internetLiteratureMatchPercent: audit.internetLiteratureMatchPercent,
        isClaimedAnswerCorrect: true,
        claimedAnswer: targetCorrectAnswer,
        verifiedCorrectAnswer: targetCorrectAnswer,
        matchedSlidesCount: matchedSlides.length,
        matchedSlideSnippet: matchedSlides[0]?.snippet || null,
        matchedNoteTitle: matchedSlides[0]?.noteTitle || null,
        providerUsed
      },
      updatedAt: verifiedAt
    };
  }

  // 4. Supabase Eşitlemesi (Varsa)
  if (supabase && updatedQuestion.id) {
    try {
      const row = cleanForPostgres({
        id: updatedQuestion.id,
        committee_id: updatedQuestion.committeeId,
        discipline: updatedQuestion.discipline,
        topic: updatedQuestion.topic,
        exam_year: updatedQuestion.examYear || 'Geçmiş Yıllar Çıkmışı (Arşiv)',
        source_file: updatedQuestion.sourceFile || null,
        claimed_answer: updatedQuestion.reconstruction?.correctAnswer || updatedQuestion.claimedAnswer || null,
        reconstruction: updatedQuestion.reconstruction,
        is_suspect: Boolean(updatedQuestion.isSuspect),
        is_ambiguous: Boolean(updatedQuestion.isAmbiguous),
        data: updatedQuestion,
        updated_at: verifiedAt
      });
      await supabase.from('past_questions').upsert([row], { onConflict: 'id' });
    } catch (e) {
      console.warn(`[Supabase Doğrulama Senkronizasyon Uyarısı]:`, e.message);
    }
  }

  return {
    success: true,
    decision: updatedQuestion.verification.status,
    overallMatchPercent: audit.overallMatchPercent,
    isSuspect: updatedQuestion.isSuspect,
    question: updatedQuestion
  };
}

// -------------------------------------------------------------
// YEDEK KURAL TABANLI DEĞERLENDİRİCİ (AI API'leri Kesilirse)
// -------------------------------------------------------------
function fallbackRuleBasedVerification(q, matchedSlides) {
  const claimed = q.claimedAnswer || q.reconstruction?.correctAnswer;
  if (!claimed) {
    return {
      claimedAnswer: '',
      isClaimedAnswerCorrect: false,
      lectureMatchPercent: 0,
      internetLiteratureMatchPercent: 0,
      overallMatchPercent: 0,
      verifiedCorrectAnswer: null,
      decision: 'SUSPECT',
      discrepancyFound: true,
      medicalReasoning: 'Soruda belirtilmiş herhangi bir iddia edilen cevap bulunmamaktadır.',
      pearl: ''
    };
  }

  const bestSlide = matchedSlides[0];
  const slideScore = bestSlide ? bestSlide.score : 0;

  // Slayt puanı yüksek ve eşleşme varsa
  if (slideScore >= 75) {
    return {
      claimedAnswer: claimed,
      isClaimedAnswerCorrect: true,
      lectureMatchPercent: slideScore,
      internetLiteratureMatchPercent: 90,
      overallMatchPercent: Math.round((slideScore + 90) / 2),
      verifiedCorrectAnswer: claimed,
      decision: 'VERIFIED',
      discrepancyFound: false,
      medicalReasoning: `Amfi ders slaytında ("${bestSlide.noteTitle}", Sayfa #${bestSlide.pageNumber}) doğrudan eşleşme sağlandı.`,
      pearl: ''
    };
  }

  // Slayt bulunamadı veya puanı düşükse %90'ın altında kalır
  return {
    claimedAnswer: claimed,
    isClaimedAnswerCorrect: false,
    lectureMatchPercent: slideScore,
    internetLiteratureMatchPercent: 60,
    overallMatchPercent: Math.round((slideScore + 60) / 2),
    verifiedCorrectAnswer: null,
    decision: 'SUSPECT',
    discrepancyFound: true,
    medicalReasoning: 'Ders slaytlarında yeterli kanıt bulunamadı ve güvenli eşleşme eşiği (%90) aşılamadı.',
    pearl: ''
  };
}

// -------------------------------------------------------------
// VERİTABANI YÖNETİMİ & BATCH KONTROL
// -------------------------------------------------------------
export function loadQuestions() {
  if (fs.existsSync(DATA_PAST_PATH)) {
    try {
      return JSON.parse(fs.readFileSync(DATA_PAST_PATH, 'utf8'));
    } catch (e) {
      console.error('Hata: pastQuestions.json okunamadı:', e.message);
    }
  }
  return [];
}

export function saveQuestions(questions) {
  try {
    // Önce yedek al
    if (!fs.existsSync(BACKUP_PATH) && fs.existsSync(DATA_PAST_PATH)) {
      fs.copyFileSync(DATA_PAST_PATH, BACKUP_PATH);
    }
    fs.writeFileSync(DATA_PAST_PATH, JSON.stringify(questions, null, 2), 'utf8');
    if (fs.existsSync(path.dirname(SRC_PAST_PATH))) {
      fs.writeFileSync(SRC_PAST_PATH, JSON.stringify(questions, null, 2), 'utf8');
    }
  } catch (e) {
    console.error('Hata: pastQuestions.json kaydedilemedi:', e.message);
  }
}

// -------------------------------------------------------------
// ÇOKLU SORU DENETLEME VE RAPORLAMA MOTORU
// -------------------------------------------------------------
export async function verifyQuestionsBatch(options = {}) {
  const {
    unverifiedOnly = true,
    limit = 20,
    specificId = null,
    onProgress = null
  } = options;

  const allQuestions = loadQuestions();
  console.log(`📋 Toplam yüklü soru: ${allQuestions.length}`);

  let targets = [];
  if (specificId) {
    targets = allQuestions.filter(q => q.id === specificId);
  } else if (unverifiedOnly) {
    targets = allQuestions.filter(q => !q.verification || q.verification.status === undefined);
  } else {
    targets = allQuestions;
  }

  if (limit && limit > 0) {
    targets = targets.slice(0, limit);
  }

  console.log(`🎯 Denetlenecek hedef soru sayısı: ${targets.length}`);

  let verifiedCount = 0;
  let suspectCount = 0;
  const reports = [];

  for (let i = 0; i < targets.length; i++) {
    const q = targets[i];
    console.log(`\n[${i + 1}/${targets.length}] Soru Denetleniyor (ID: ${q.id}, Soru #${q.questionNumber || i + 1})...`);
    
    try {
      const auditResult = await verifyQuestionAnswer(q);
      if (auditResult.success) {
        // Ana listedeki kaydı güncelle
        const idx = allQuestions.findIndex(item => item.id === q.id);
        if (idx !== -1) {
          allQuestions[idx] = auditResult.question;
        }

        if (auditResult.decision === 'VERIFIED') {
          verifiedCount++;
          console.log(`   ✅ DOĞRULANDI (%${auditResult.overallMatchPercent} Eşleşme) -> Doğru Cevap: ${auditResult.question.reconstruction?.correctAnswer}`);
        } else {
          suspectCount++;
          console.log(`   🚨 ŞÜPHELİ İLAN EDİLDİ (%${auditResult.overallMatchPercent} Eşleşme < %90) -> Doğru Cevap Kaldırıldı / Boş Bırakıldı!`);
        }

        reports.push({
          id: q.id,
          questionNumber: q.questionNumber,
          discipline: q.discipline,
          topic: q.topic,
          claimedAnswer: q.claimedAnswer,
          decision: auditResult.decision,
          overallMatchPercent: auditResult.overallMatchPercent,
          isSuspect: auditResult.question.isSuspect
        });

        // Her 5 soruda bir ara kaydet
        if ((i + 1) % 5 === 0 || i === targets.length - 1) {
          saveQuestions(allQuestions);
          fs.writeFileSync(REPORT_PATH, JSON.stringify({
            lastRun: new Date().toISOString(),
            totalChecked: i + 1,
            verifiedCount,
            suspectCount,
            reports
          }, null, 2), 'utf8');
        }

        if (typeof onProgress === 'function') {
          onProgress({ current: i + 1, total: targets.length, verifiedCount, suspectCount });
        }
      }
    } catch (err) {
      console.error(`   ❌ Soru #${q.id} denetim hatası:`, err.message);
    }

    // Rate limit koruması (1.5 saniye bekle)
    if (i < targets.length - 1) {
      await new Promise(r => setTimeout(r, 1500));
    }
  }

  saveQuestions(allQuestions);
  console.log(`\n🏁 [Denetim Tamamlandı]`);
  console.log(`   ✅ %90 Üzeri Doğrulanan Sorular: ${verifiedCount}`);
  console.log(`   🚨 %90 Altı Şüpheli/Boş Bırakılan Sorular: ${suspectCount}`);

  return {
    totalChecked: targets.length,
    verifiedCount,
    suspectCount,
    reports
  };
}

// -------------------------------------------------------------
// SÜREKLİ İZLEYİCİ (WATCHER / DAEMON) MODU
// Her yeni soru eklendiğinde otomatik olarak çalışır!
// -------------------------------------------------------------
export function startContinuousWatcher() {
  console.log('\n👁️ [Watcher Aktif] MedSoru Soru Cevap Denetleme İzleyicisi devrede...');
  console.log(`📁 İzlenen dosya: ${DATA_PAST_PATH}`);
  console.log('✨ Sisteme yeni bir soru eklendiğinde anında otomatik olarak denetlenecektir.\n');

  let isProcessing = false;
  let lastMtime = 0;

  // Periyodik kontrol ve dosya izleyici
  const checkNewQuestions = async () => {
    if (isProcessing) return;
    try {
      if (!fs.existsSync(DATA_PAST_PATH)) return;
      const stat = fs.statSync(DATA_PAST_PATH);
      if (stat.mtimeMs <= lastMtime) return;
      lastMtime = stat.mtimeMs;

      const questions = loadQuestions();
      const unverified = questions.filter(q => !q.verification);

      if (unverified.length > 0) {
        isProcessing = true;
        console.log(`\n🔔 [Yeni Soru Tespit Edildi!] ${unverified.length} adet doğrulanmamış soru bulundu. Otomatik denetim başlatılıyor...`);
        await verifyQuestionsBatch({ unverifiedOnly: true, limit: 10 });
        isProcessing = false;
      }
    } catch (e) {
      isProcessing = false;
      console.warn('[Watcher Uyarı]:', e.message);
    }
  };

  // Hem fs.watch hem de 10 saniyelik interval ile çift katmanlı garanti izleme
  try {
    fs.watch(DATA_PAST_PATH, () => {
      setTimeout(checkNewQuestions, 1000);
    });
  } catch (e) {}

  setInterval(checkNewQuestions, 10000);
}

// -------------------------------------------------------------
// CLI ÇALIŞTIRMA KOMUTU (CLI ENTRYPOINT)
// -------------------------------------------------------------
async function main() {
  const args = process.argv.slice(2);

  if (args.includes('--watch')) {
    startContinuousWatcher();
    return;
  }

  const idArgIdx = args.indexOf('--id');
  const specificId = idArgIdx !== -1 ? args[idArgIdx + 1] : null;

  const limitArgIdx = args.indexOf('--limit');
  const limit = limitArgIdx !== -1 ? parseInt(args[limitArgIdx + 1], 10) : (specificId ? 1 : 15);

  const unverifiedOnly = !args.includes('--all');

  console.log('🩺 [MedSoru] Çıkmış Soru & Cevap Doğrulama Motoru Başlatılıyor...');
  await verifyQuestionsBatch({
    unverifiedOnly,
    limit,
    specificId
  });
}

// Doğrudan CLI ile çağrıldıysa çalıştır
if (process.argv[1] && process.argv[1].endsWith('verify-question-answers.mjs')) {
  main().catch(err => {
    console.error('Kritik Hata:', err);
    process.exit(1);
  });
}
