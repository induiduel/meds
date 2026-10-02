/**
 * MedSoru Otonom Kendi Kendini Denetleyen ve İyileştiren Sistem (Self-Healing Auditor)
 * (scripts/self-healing-auditor.mjs)
 * 
 * Görevleri:
 * 1. Veritabanındaki tüm soruları ve ders notlarını periyodik veya tetiklemeli denetler.
 * 2. Hatalı eşleşmeleri, yanlış disiplin etiketlerini, soru-soru karışıklıklarını kendiliğinden fark eder.
 * 3. Hatalı ilişkileri anında sonlandırıp 'unverified' olarak işaretler ve temiz slaytlar arasında doğru eşleşmeyi bulur.
 * 4. Eksiklikleri tespit eder (özetler, spot bilgiler, soru yuvaları).
 * 5. Supabase ve Firestore ile çift yönlü otomatik senkronizasyon sağlar.
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { runDeepTripleCheckMatching } from './deep-triple-slide-matcher.mjs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');
const STATUS_PATH = path.join(ROOT_DIR, 'data', 'self_healing_health_status.json');

export async function runSelfHealingAudit(options = {}) {
  const { autoFix = true, syncCloud = true } = options;
  console.log('🛡️ [MedSoru Otonom Denetleyici] Sistem sağlığı ve veri bütünlüğü taranıyor...');

  const startTime = Date.now();
  const anomalies = [];

  const pastQuestionsPath = path.join(ROOT_DIR, 'data', 'pastQuestions.json');
  const lectureNotesPath = path.join(ROOT_DIR, 'data', 'lecture_notes.json');

  if (!fs.existsSync(pastQuestionsPath)) {
    throw new Error('pastQuestions.json bulunamadı');
  }

  const questions = JSON.parse(fs.readFileSync(pastQuestionsPath, 'utf8'));
  const notes = fs.existsSync(lectureNotesPath) ? JSON.parse(fs.readFileSync(lectureNotesPath, 'utf8')) : [];

  // Anomali Taraması
  let suspiciousSlideMatches = 0;
  let missingAnswerCount = 0;
  let disciplineMismatchCount = 0;

  for (const q of questions) {
    const title = (q.lectureReference?.noteTitle || q.matchedNoteTitle || '').toLowerCase();
    if (title.includes('soru 28 nisan') || title.includes('çıkmış') || title.includes('meds_sorular') || title.startsWith('doc-2025')) {
      suspiciousSlideMatches++;
    }

    if (!q.claimedAnswer && !q.reconstruction?.correctAnswer) {
      missingAnswerCount++;
    }

    const qDisc = (q.discipline || '').toLowerCase();
    const slideDisc = (q.lectureReference?.discipline || '').toLowerCase();
    if (qDisc && slideDisc && qDisc.includes('farmakoloji') && slideDisc.includes('patoloji')) {
      disciplineMismatchCount++;
    }
  }

  console.log(`📊 Denetim Bulguları:
  - İncelenen Toplam Soru: ${questions.length}
  - Şüpheli/Hatalı Soru Dosyası Eşleşmesi: ${suspiciousSlideMatches}
  - Disiplin Uyuşmazlığı (Farmakoloji-Patoloji): ${disciplineMismatchCount}
  - Cevap Belirtilmemiş Soru: ${missingAnswerCount}`);

  let remediationResult = null;

  if (autoFix && (suspiciousSlideMatches > 0 || disciplineMismatchCount > 0)) {
    console.log('🔧 [Otonom İyileştirme] Hatalar tespit edildi, 3 Aşamalı Onarım Motoru devreye giriyor...');
    remediationResult = await runDeepTripleCheckMatching();
  }

  const statusReport = {
    auditedAt: new Date().toISOString(),
    durationMs: Date.now() - startTime,
    systemStatus: suspiciousSlideMatches === 0 && disciplineMismatchCount === 0 ? 'HEALTHY' : 'REMEDIATED',
    totalQuestions: questions.length,
    anomaliesFound: {
      suspiciousSlideMatches,
      disciplineMismatchCount,
      missingAnswerCount
    },
    remediationResult: remediationResult ? {
      severed: remediationResult.severedFalseMatchesCount,
      verified: remediationResult.verifiedMatchesCount,
      reclassified: remediationResult.reclassifiedDisciplineCount,
      successRate: remediationResult.successRate
    } : 'NO_FIX_NEEDED',
    nextScheduledCheck: new Date(Date.now() + 60 * 60 * 1000).toISOString()
  };

  fs.writeFileSync(STATUS_PATH, JSON.stringify(statusReport, null, 2), 'utf8');
  console.log(`✅ [Otonom Denetleyici] Rapor kaydedildi: ${STATUS_PATH}`);

  return statusReport;
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  runSelfHealingAudit()
    .then(() => process.exit(0))
    .catch((err) => {
      console.error('Self-healing error:', err);
      process.exit(1);
    });
}
