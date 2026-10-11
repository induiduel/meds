/**
 * Soru Çapraz Veri & Karantina-Redaksiyon Denetim Servisi
 * (Question Cross Data & Quarantine-Redaction Audit Service)
 *
 * Amaç:
 * 1. Karantinadaki bir soruya hata bildirimi geldiğinde veya incelendiğinde;
 *    o sorunun karantinada olma sebeplerini, kendi içindeki redaksiyonu (reconstruction)
 *    ve sistemde aynı veya farklı ID ile var olan redakte edilmiş kopyalarını/kardeşlerini tespit eder.
 * 2. Yapay zekanın "Var olan temiz bir redaksiyonu çöpe atmasını veya bozmasını" KESİNLİKLE engeller.
 * 3. Yapay zekaya hem karantina nedenini hem de sistemdeki en kaliteli redakte referansı sunar.
 * 4. Hata çözüldüğünde karantinadan çıkarma (release) ve kardeş sorularla çift taraflı senkronizasyon sağlar.
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const ROOT_DIR = path.resolve(__dirname, '..', '..'); // meds/
const DATA_DIR = path.resolve(ROOT_DIR, 'data');
const SRC_DATA_DIR = path.resolve(ROOT_DIR, 'src', 'data');
const REPO_ROOT = path.resolve(ROOT_DIR, '..');

const PAST_QUESTIONS_FILE = path.resolve(DATA_DIR, 'pastQuestions.json');
const SRC_PAST_QUESTIONS_FILE = path.resolve(SRC_DATA_DIR, 'pastQuestions.json');
const PRACTICE_QUESTIONS_FILE = path.resolve(DATA_DIR, 'questions.json');

const QUARANTINE_FILE = path.join(
  process.env.MEDS_DATABASE_DIR || path.resolve(REPO_ROOT, 'meds_database'),
  'derived',
  'quarantine',
  'karantina.json'
);

const MERGE_FILE = path.join(
  process.env.MEDS_DATABASE_DIR
    ? path.dirname(process.env.MEDS_DATABASE_DIR)
    : REPO_ROOT,
  'meds_database_v2',
  'soru_birlestirme',
  'birlestirmeler.json'
);

export interface RedactedCandidate {
  id: string;
  stem: string;
  options: any[];
  correctAnswer?: string;
  explanation?: string;
  reconstruction?: any;
  status?: string;
  isQuarantined?: boolean;
  sourceType: 'local_reconstruction' | 'quarantine_repair' | 'merge_group' | 'similarity_search';
  confidence: number;
}

export interface QuestionCrossData {
  targetId: string;
  stem: string;
  isQuarantined: boolean;
  quarantineReasons: string[];
  quarantineSource?: string;
  quarantineRecord?: any;
  quarantineRepair?: { stem: string; options: any[] };
  hasLocalReconstruction: boolean;
  localReconstruction?: any;
  hasRevisions: boolean;
  latestRevisions?: any[];
  mergeGroup?: {
    groupId: string;
    isAsil: boolean;
    asilId: string;
    uyeler: string[];
    otherMembers: Array<{
      id: string;
      stem: string;
      isQuarantined: boolean;
      status?: string;
      hasReconstruction: boolean;
      reconstruction?: any;
      options: any[];
      correctAnswer?: string;
      explanation?: string;
    }>;
  };
  similarRedactedQuestions: RedactedCandidate[];
  bestRedactedReference?: RedactedCandidate;
}

function readJsonSafe<T>(filePath: string, fallback: T): T {
  try {
    if (fs.existsSync(filePath)) {
      return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
    }
  } catch (err) {
    console.error(`[QuestionCrossAudit] JSON okunamadı (${filePath}):`, err);
  }
  return fallback;
}

function writeJsonAtomic(filePath: string, data: any) {
  const dir = path.dirname(filePath);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  const content = JSON.stringify(data, null, 2);
  const tempPath = `${filePath}.tmp_${Date.now()}_${Math.random().toString(36).slice(2, 6)}`;
  fs.writeFileSync(tempPath, content, 'utf-8');
  fs.renameSync(tempPath, filePath);
}

/** Gürültülü sınav sitesi artıklarını metinden arındırarak benzerlik karşılaştırması yapar */
function cleanStemForMatching(text: string): string {
  if (!text) return '';
  return text
    .replace(/https?:\/\/\S+/gi, '')
    .replace(/s[ıi]nav\.karab[üu]k\.edu\.tr/gi, '')
    .replace(/D[ÖO]NEM\s*\d\s*(B[ÜU]T[ÜU]NLEME|F[İI]NAL|KURUL)\s*SORU/gi, '')
    .replace(/S[ıi]ra\s*No/gi, '')
    .replace(/Anasayfa\s*\/?\s*S[ıi]nav\s*Sonucu/gi, '')
    .replace(/\b\d{2}\.\d{2}\.\d{4}\b/g, '')
    .replace(/[^\w\sğüşıöçĞÜŞİÖÇ]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
    .toLowerCase();
}

/** Basit kelime kümesi Jaccard benzerliği (0.0 - 1.0) */
function calculateStemSimilarity(a: string, b: string): number {
  const cleanA = cleanStemForMatching(a);
  const cleanB = cleanStemForMatching(b);
  if (!cleanA || !cleanB) return 0;
  if (cleanA === cleanB) return 1.0;

  const wordsA = new Set(cleanA.split(' ').filter((w) => w.length > 2));
  const wordsB = new Set(cleanB.split(' ').filter((w) => w.length > 2));
  if (wordsA.size === 0 || wordsB.size === 0) return 0;

  let intersection = 0;
  for (const w of wordsA) {
    if (wordsB.has(w)) intersection++;
  }
  const union = new Set([...wordsA, ...wordsB]).size;
  return union === 0 ? 0 : intersection / union;
}

/**
 * Verilen bir soru kimliği için sistemdeki tüm çapraz verileri derinlemesine tarar:
 * Karantina kaydı, kendi redaksiyonu, birleştirme grupları ve ilişkili redakte kopyalar.
 */
export function detectQuestionCrossData(targetId: string, source: 'past_question' | 'practice_question' = 'past_question'): QuestionCrossData {
  const targetIdStr = String(targetId).trim();

  // 1. Soruyu Yükle
  let q: any = null;
  const pastList = readJsonSafe<any[]>(PAST_QUESTIONS_FILE, []);
  if (source === 'past_question') {
    q = pastList.find((x) => String(x.id).trim() === targetIdStr);
    if (!q) {
      const srcList = readJsonSafe<any[]>(SRC_PAST_QUESTIONS_FILE, []);
      q = srcList.find((x) => String(x.id).trim() === targetIdStr);
    }
  } else {
    const practiceList = readJsonSafe<any[]>(PRACTICE_QUESTIONS_FILE, []);
    q = practiceList.find((x) => String(x.id).trim() === targetIdStr);
  }

  // Soru bulunamadıysa temel boş şablon
  if (!q) {
    return {
      targetId: targetIdStr,
      stem: '',
      isQuarantined: false,
      quarantineReasons: [],
      hasLocalReconstruction: false,
      hasRevisions: false,
      similarRedactedQuestions: [],
    };
  }

  // 2. Karantina Kayıtlarını Oku
  const karantina = readJsonSafe<any>(QUARANTINE_FILE, { sorular: {}, onarim: {} });
  const qKarantinaInfo = karantina.sorular?.[targetIdStr] || null;
  const qKarantinaRepair = karantina.onarim?.[targetIdStr] || null;

  const isQuarantined = Boolean(
    q.isQuarantined ||
      q.status === 'quarantined' ||
      (Array.isArray(q.tags) && q.tags.includes('karantina')) ||
      Boolean(qKarantinaInfo)
  );

  const quarantineReasons: string[] = [
    ...(qKarantinaInfo?.neden || []),
    ...(Array.isArray(q.quarantineReasons) ? q.quarantineReasons : []),
    ...(q.quarantineReason ? [q.quarantineReason] : []),
  ];
  const uniqueQuarantineReasons = Array.from(new Set(quarantineReasons));

  // 3. Kendi Redaksiyon / Rekonstrüksiyon Verisi
  const hasLocalReconstruction = Boolean(
    q.reconstruction && (q.reconstruction.stem || q.reconstruction.options?.length)
  );
  const localReconstruction = hasLocalReconstruction ? q.reconstruction : null;

  const hasRevisions = Array.isArray(q.revisions) && q.revisions.length > 0;
  const latestRevisions = hasRevisions ? q.revisions.slice(-3) : [];

  // 4. Birleştirme Gruplarını (birlestirmeler.json) Oku
  const birlestirmeler = readJsonSafe<any>(MERGE_FILE, { gruplar: [] });
  const allGroups: any[] = birlestirmeler.gruplar || [];

  let mergeGroup: QuestionCrossData['mergeGroup'] | undefined = undefined;
  let bestCandidateFromMerge: RedactedCandidate | null = null;

  const targetGroup = allGroups.find(
    (g) =>
      g.durum !== 'ayrildi' &&
      (String(g.asil).trim() === targetIdStr || (Array.isArray(g.uyeler) && g.uyeler.some((u: any) => String(u).trim() === targetIdStr)))
  );

  if (targetGroup) {
    const uyeler = (targetGroup.uyeler || []).map((u: any) => String(u).trim());
    const isAsil = String(targetGroup.asil).trim() === targetIdStr;
    const otherMemberIds = uyeler.filter((u: string) => u !== targetIdStr);

    const otherMembers = otherMemberIds
      .map((mId: string) => {
        const mq = pastList.find((x) => String(x.id).trim() === mId);
        if (!mq) return null;
        const mKarInfo = karantina.sorular?.[mId];
        const mIsKar = Boolean(
          mq.isQuarantined ||
            mq.status === 'quarantined' ||
            (Array.isArray(mq.tags) && mq.tags.includes('karantina')) ||
            mKarInfo
        );
        const mHasRec = Boolean(mq.reconstruction && (mq.reconstruction.stem || mq.reconstruction.options?.length));
        return {
          id: mId,
          stem: mq.stem || mq.reconstruction?.stem || '',
          isQuarantined: mIsKar,
          status: mq.status,
          hasReconstruction: mHasRec,
          reconstruction: mq.reconstruction,
          options: mq.options || mq.reconstruction?.options || [],
          correctAnswer: mq.correctAnswer || mq.reconstruction?.correctAnswer,
          explanation: mq.explanation || mq.reconstruction?.explanation,
        };
      })
      .filter(Boolean) as any[];

    mergeGroup = {
      groupId: targetGroup.id,
      isAsil,
      asilId: String(targetGroup.asil).trim(),
      uyeler,
      otherMembers,
    };

    // Gruptaki en kaliteli redakte adayını seç:
    // Tercih: Karantinada olmayan + reconstruction içeren + en uzun açıklama veya stem
    const validCandidates = otherMembers.filter((m) => !m.isQuarantined);
    const sorted = [...(validCandidates.length > 0 ? validCandidates : otherMembers)].sort((a, b) => {
      const aScore = (a.hasReconstruction ? 10 : 0) + (a.status === 'verified' || a.status === 'approved' ? 5 : 0) + (a.explanation ? 3 : 0);
      const bScore = (b.hasReconstruction ? 10 : 0) + (b.status === 'verified' || b.status === 'approved' ? 5 : 0) + (b.explanation ? 3 : 0);
      return bScore - aScore;
    });

    if (sorted.length > 0) {
      const best = sorted[0];
      bestCandidateFromMerge = {
        id: best.id,
        stem: best.reconstruction?.stem || best.stem,
        options: best.reconstruction?.options || best.options,
        correctAnswer: best.reconstruction?.correctAnswer || best.correctAnswer,
        explanation: best.reconstruction?.explanation || best.explanation,
        reconstruction: best.reconstruction,
        status: best.status,
        isQuarantined: best.isQuarantined,
        sourceType: 'merge_group',
        confidence: targetGroup.benzerlik || 0.85,
      };
    }
  }

  // 5. Benzerlik Taraması (Grupta yoksa veya ek destek için)
  const similarRedactedQuestions: RedactedCandidate[] = [];
  const currentCleanStem = cleanStemForMatching(q.stem || q.reconstruction?.stem || '');

  if (currentCleanStem.length >= 15) {
    for (const otherQ of pastList) {
      const otherId = String(otherQ.id).trim();
      if (otherId === targetIdStr) continue;
      if (mergeGroup && mergeGroup.uyeler.includes(otherId)) continue; // Gruptakiler zaten incelendi

      const otherCleanStem = cleanStemForMatching(otherQ.stem || otherQ.reconstruction?.stem || '');
      if (otherCleanStem.length < 15) continue;

      const sim = calculateStemSimilarity(currentCleanStem, otherCleanStem);
      if (sim >= 0.62) {
        const otherIsKar = Boolean(
          otherQ.isQuarantined ||
            otherQ.status === 'quarantined' ||
            (Array.isArray(otherQ.tags) && otherQ.tags.includes('karantina')) ||
            karantina.sorular?.[otherId]
        );
        const otherHasRec = Boolean(otherQ.reconstruction && (otherQ.reconstruction.stem || otherQ.reconstruction.options?.length));

        similarRedactedQuestions.push({
          id: otherId,
          stem: otherQ.reconstruction?.stem || otherQ.stem,
          options: otherQ.reconstruction?.options || otherQ.options,
          correctAnswer: otherQ.reconstruction?.correctAnswer || otherQ.correctAnswer,
          explanation: otherQ.reconstruction?.explanation || otherQ.explanation,
          reconstruction: otherQ.reconstruction,
          status: otherQ.status,
          isQuarantined: otherIsKar,
          sourceType: 'similarity_search',
          confidence: Math.round(sim * 100) / 100,
        });
      }
    }
  }

  // Sırala: Karantinada olmayan, en yüksek benzerlik
  similarRedactedQuestions.sort((a, b) => {
    if (a.isQuarantined !== b.isQuarantined) return a.isQuarantined ? 1 : -1;
    return b.confidence - a.confidence;
  });

  // 6. Nihai "En İyi Redakte Referans" (Best Redacted Reference) Belirleme
  let bestRedactedReference: RedactedCandidate | undefined = undefined;

  if (bestCandidateFromMerge && !bestCandidateFromMerge.isQuarantined) {
    bestRedactedReference = bestCandidateFromMerge;
  } else if (hasLocalReconstruction && localReconstruction.stem && localReconstruction.options?.length >= 3) {
    bestRedactedReference = {
      id: targetIdStr,
      stem: localReconstruction.stem,
      options: localReconstruction.options,
      correctAnswer: localReconstruction.correctAnswer || q.correctAnswer,
      explanation: localReconstruction.explanation || q.explanation,
      reconstruction: localReconstruction,
      status: q.status,
      isQuarantined,
      sourceType: 'local_reconstruction',
      confidence: 1.0,
    };
  } else if (qKarantinaRepair && qKarantinaRepair.stem && qKarantinaRepair.options?.length >= 3) {
    bestRedactedReference = {
      id: targetIdStr,
      stem: qKarantinaRepair.stem,
      options: qKarantinaRepair.options,
      correctAnswer: q.correctAnswer,
      explanation: q.explanation,
      status: q.status,
      isQuarantined,
      sourceType: 'quarantine_repair',
      confidence: 0.9,
    };
  } else if (similarRedactedQuestions.length > 0 && !similarRedactedQuestions[0].isQuarantined) {
    bestRedactedReference = similarRedactedQuestions[0];
  } else if (bestCandidateFromMerge) {
    bestRedactedReference = bestCandidateFromMerge;
  }

  return {
    targetId: targetIdStr,
    stem: q.stem || '',
    isQuarantined,
    quarantineReasons: uniqueQuarantineReasons,
    quarantineSource: qKarantinaInfo?.kaynak || q.quarantineSource,
    quarantineRecord: qKarantinaInfo,
    quarantineRepair: qKarantinaRepair,
    hasLocalReconstruction,
    localReconstruction,
    hasRevisions,
    latestRevisions,
    mergeGroup,
    similarRedactedQuestions: similarRedactedQuestions.slice(0, 3),
    bestRedactedReference,
  };
}

/**
 * Yapay zeka promptuna eklenecek zengin Çapraz Veri & Karantina & Redaksiyon Bölümünü oluşturur.
 */
export function buildCrossDataPromptSection(crossData: QuestionCrossData): string {
  const sections: string[] = [];

  sections.push('=== SİSTEMSEL ÇAPRAZ VERİ & KARANTİNA DENETİM DOSYASI ===');
  sections.push(`Hedef Soru ID: ${crossData.targetId}`);
  sections.push(`Karantina Durumu: ${crossData.isQuarantined ? '⚠️ KARANTİNADA (Kusurlu/Enkaz Kayıt)' : '✓ Standart Yayında'}`);

  if (crossData.isQuarantined) {
    sections.push(`Karantina Nedenleri: ${crossData.quarantineReasons.join(', ') || 'Belirtilmedi'}`);
    if (crossData.quarantineSource) {
      sections.push(`Karantina Kaynağı: ${crossData.quarantineSource}`);
    }
  }

  // 1. Kendi Redaksiyon Durumu
  if (crossData.hasLocalReconstruction) {
    sections.push('\n[MEVCUT YEREL REDAKSİYON (reconstruction) KAYDI]:');
    sections.push(`- Redakte Edilmiş Kök: ${crossData.localReconstruction.stem}`);
    sections.push(`- Doğru Cevap: ${crossData.localReconstruction.correctAnswer || 'Belirtilmemiş'}`);
    sections.push(`- Şık Sayısı: ${crossData.localReconstruction.options?.length || 0}`);
    if (crossData.localReconstruction.explanation) {
      sections.push(`- Açıklama: ${crossData.localReconstruction.explanation}`);
    }
  }

  // 2. Karantina Onarım Kaydı
  if (crossData.quarantineRepair) {
    sections.push('\n[KARANTİNA DOSYASINDAKİ MEVCUT ONARIM (quarantine.json onarim)]:');
    sections.push(`- Onarılmış Kök: ${crossData.quarantineRepair.stem}`);
    sections.push(`- Onarılmış Şıklar: ${crossData.quarantineRepair.options?.map((o) => `${o.key}) ${o.text}`).join(' | ')}`);
  }

  // 3. Birleştirme Grubu ve Kardeş Sorular
  if (crossData.mergeGroup) {
    sections.push('\n[BİRLEŞTİRME GRUBU (birlestirmeler.json)]:');
    sections.push(`- Grup ID: ${crossData.mergeGroup.groupId} (Asıl Soru: #${crossData.mergeGroup.asilId})`);
    sections.push(`- Gruptaki Diğer Sorular: ${crossData.mergeGroup.otherMembers.map((m) => `#${m.id} (${m.isQuarantined ? 'Karantina' : 'Yayında'})`).join(', ')}`);

    for (const m of crossData.mergeGroup.otherMembers) {
      if (!m.isQuarantined && (m.hasReconstruction || m.explanation)) {
        sections.push(`  * Kardeş Soru #${m.id} [TEMİZ / REDAKTE EDİLMİŞ]:`);
        sections.push(`    Kök: ${m.stem}`);
        sections.push(`    Cevap: ${m.correctAnswer || '?'}`);
        if (m.explanation) sections.push(`    Açıklama: ${m.explanation}`);
      }
    }
  }

  // 4. Eşleşen Benzer Redakte Sorular
  if (crossData.similarRedactedQuestions.length > 0) {
    sections.push('\n[SİSTEMDE BENZER KÖKE SAHİP DİĞER SORULAR]:');
    for (const sq of crossData.similarRedactedQuestions) {
      sections.push(`- Soru #${sq.id} (Benzerlik: %${Math.round(sq.confidence * 100)}, Durum: ${sq.isQuarantined ? 'Karantina' : 'Yayında'}):`);
      sections.push(`  Kök: ${sq.stem.slice(0, 140)}...`);
      sections.push(`  Cevap: ${sq.correctAnswer || '?'}`);
    }
  }

  // 5. En İyi Redakte Referans Özeti
  if (crossData.bestRedactedReference) {
    const ref = crossData.bestRedactedReference;
    sections.push('\n⭐ [SİSTEMDE TESPİT EDİLEN EN KALİTELİ REDAKTE REFERANS KAYIT]:');
    sections.push(`- Referans Kaynak Türü: ${ref.sourceType} (Soru #${ref.id})`);
    sections.push(`- Temiz Soru Kökü: ${ref.stem}`);
    sections.push(`- Referans Şıklar:\n${(ref.options || []).map((o: any) => `  ${o.key}) ${o.text}`).join('\n')}`);
    sections.push(`- Doğru Cevap: ${ref.correctAnswer}`);
    if (ref.explanation) sections.push(`- Referans Açıklama: ${ref.explanation}`);
  }

  sections.push('\n======================================================================');
  sections.push('🚨 YAPAY ZEKA İÇİN ÇAPRAZ VERİ & REDAKSİYON KORUMA TALİMATLARI:');
  sections.push('1. VAR OLAN DOĞRU BİR REDAKSİYONU ASLA ÇÖPE ATMA VEYA BOZMA!');
  sections.push('   Eğer sorunun daha önce yapılmış temiz bir redaksiyonu veya sistemde farklı ID ile temiz bir kardeşi varsa, bu metni temel al.');
  sections.push('2. Kullanıcının hata bildirimini (itirazını), karantinadaki bozuk/enkaz metin üzerinden değil; sistemdeki en temiz redakte referans üzerinden değerlendir.');
  sections.push('3. Eğer soru karantinada ise ve bu onarım ile soru tıbbi ve biçimsel olarak kusursuz hale getiriliyorsa:');
  sections.push('   "release_quarantine": true olarak işaretle (soru karantinadan kurtarılacaktır).');
  sections.push('4. Eğer sistemdeki mevcut redaksiyon zaten doğru ise ve kullanıcının itirazı haksız ise:');
  sections.push('   "has_error": false, "actionTaken": "verified_correct" döndür, mevcut redaksiyonu koru ve gerekçesini açıkla.');
  sections.push('5. Eğer soru birleştirme grubunda başka bir soruyla kardeş ise, yaptığın düzenlemenin kardeş soruyla çelişmemesini sağla.');
  sections.push('======================================================================\n');

  return sections.join('\n');
}

/**
 * Bir soruyu karantina dosyasından (derived/quarantine/karantina.json) resmi olarak çıkarır
 * ve onarılmış halini karantina.json onarım listesine kaydeder.
 */
export function releaseQuestionFromQuarantine(
  questionId: string,
  repairedData?: { stem: string; options: any[] }
): { success: boolean; removedFromQuarantine: boolean; error?: string } {
  try {
    const karantina = readJsonSafe<any>(QUARANTINE_FILE, { sorular: {}, onarim: {} });
    let removed = false;

    if (karantina.sorular && karantina.sorular[questionId]) {
      delete karantina.sorular[questionId];
      removed = true;
    }

    if (repairedData && repairedData.stem && Array.isArray(repairedData.options)) {
      if (!karantina.onarim) karantina.onarim = {};
      karantina.onarim[questionId] = {
        stem: repairedData.stem,
        options: repairedData.options.map((o: any) => ({ key: o.key, text: o.text })),
      };
    }

    if (removed || repairedData) {
      writeJsonAtomic(QUARANTINE_FILE, karantina);
    }

    return { success: true, removedFromQuarantine: removed };
  } catch (err: any) {
    console.error(`[QuestionCrossAudit] Karantinadan çıkarma hatası (#${questionId}):`, err);
    return { success: false, removedFromQuarantine: false, error: err.message };
  }
}

/**
 * Geri alma (Rollback) senaryosunda soruyu eski karantina durumuna geri yükler.
 */
export function restoreQuestionToQuarantine(
  questionId: string,
  originalQuarantineRecord: any,
  hadQuarantineRepair: boolean,
  originalRepairData?: any
): { success: boolean; error?: string } {
  try {
    const karantina = readJsonSafe<any>(QUARANTINE_FILE, { sorular: {}, onarim: {} });

    if (originalQuarantineRecord) {
      if (!karantina.sorular) karantina.sorular = {};
      karantina.sorular[questionId] = originalQuarantineRecord;
    }

    if (hadQuarantineRepair && originalRepairData) {
      if (!karantina.onarim) karantina.onarim = {};
      karantina.onarim[questionId] = originalRepairData;
    } else if (!hadQuarantineRepair && karantina.onarim?.[questionId]) {
      delete karantina.onarim[questionId];
    }

    writeJsonAtomic(QUARANTINE_FILE, karantina);
    return { success: true };
  } catch (err: any) {
    console.error(`[QuestionCrossAudit] Karantinaya geri alma hatası (#${questionId}):`, err);
    return { success: false, error: err.message };
  }
}
