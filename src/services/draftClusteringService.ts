/**
 * ==============================================================================
 * MedSoru Akıllı Taslak Kümeleme, Çapa Soru Tespiti ve Birleştirme Motoru
 * (src/services/draftClusteringService.ts)
 * ==============================================================================
 * Bu servis:
 * 1. Öğrencilerin sisteme eklediği ham taslakları (drafts) analiz eder.
 * 2. 100 soruluk bir komite sınavında farklı öğrencilerin aynı soruyu farklı
 *    şekillerde girmesi sonucu oluşan soru şişkinliğini (200-500 taslak) önler.
 * 3. Çok katmanlı kriterlerle taslakları inceler:
 *    - Çapa Soru Skoru (Anchor Score): Ders, konu, şık sayısı ve detay zenginliği
 *    - Şık Sırasından Bağımsız Küme Benzerliği (A/B/C/D/E permütasyon koruması)
 *    - Farklı Kitapçık Soru Numarası Esnekliği (10. soru vs 46. soru eşleşmesi)
 *    - Tıbbi Varlık ve Terim Kesişimi (İlaç, mikrop, semptom, lab değerleri)
 *    - Aynı Konudaki Çoklu Soruları Ayırt Etme (Soru hedefi/çelişki kontrolü)
 * 4. Uyumlu taslakları tek bir ana soru çatısı altında birleştirir (merge).
 * ==============================================================================
 */

import { QuestionItem, MemoryFragment, QuestionOption, QuestionRevision } from '../types';

// ==========================================
// TİPLER VE VERİ YAPILARI
// ==========================================

export interface DraftAnchorScore {
  total: number; // 0 - 100
  isAnchor: boolean;
  stemDetailScore: number; // 0 - 30
  metadataScore: number; // 0 - 25 (Discipline, topic)
  optionsScore: number; // 0 - 25 (Şık sayısı ve kalitesi)
  answerScore: number; // 0 - 10 (Doğru cevap varlığı)
  socialScore: number; // 0 - 10 (Upvote, yorum, fragment sayısı)
  classification: 'anchor' | 'standard' | 'vague_fragment';
}

export interface OptionAlignment {
  anchorOption?: QuestionOption;
  satelliteOption?: QuestionOption;
  similarity: number; // 0 - 1
  isShared: boolean;
}

export interface DraftCompatibilityResult {
  score: number; // 0 - 100
  recommendation: 'auto_merge' | 'suggest_merge' | 'distinct';
  reasons: string[];
  stemSimilarity: number; // 0 - 100
  optionSetSimilarity: number; // 0 - 100
  sharedMedicalEntities: string[];
  targetQuestionAlignment: 'matching' | 'different_aspect' | 'conflicting';
  bookletNumberNote?: string;
  matchedOptionAlignments: OptionAlignment[];
}

export interface DraftCluster {
  id: string;
  committeeId: string;
  anchorQuestion: QuestionItem;
  satelliteDrafts: Array<{
    question: QuestionItem;
    compatibility: DraftCompatibilityResult;
  }>;
  overallConfidence: number; // 0 - 100
  status: 'ready_to_merge' | 'needs_review' | 'merged';
  estimatedUniqueSlots: number;
}

export interface ClusterAnalysisSummary {
  totalDrafts: number;
  estimatedTrueQuestions: number;
  identifiedAnchors: number;
  vagueDraftsCount: number;
  mergeableClustersCount: number;
  potentialSavedDuplicates: number;
  clusters: DraftCluster[];
  unmatchedVagueDrafts: QuestionItem[];
}

// ==========================================
// METİN VE TIBBİ VARLIK NORMALİZASYONU
// ==========================================

// Türkçe karakterleri normalize et ve durak kelimeleri temizle
export function normalizeMedicalText(text: string = ''): string {
  if (!text) return '';
  return text
    .toLowerCase()
    .replace(/İ/g, 'i')
    .replace(/I/g, 'ı')
    .replace(/ğ/g, 'g')
    .replace(/ü/g, 'u')
    .replace(/ş/g, 's')
    .replace(/ö/g, 'o')
    .replace(/ç/g, 'c')
    .replace(/[^\w\s\d]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

// Tıbbi anahtar kelimeleri ve varlıkları (ilaç, mikroorganizma, semptom, lab) çıkarma
const MEDICAL_STOP_WORDS = new Set([
  'bir', 've', 'ile', 'bu', 'icin', 'olan', 'olarak', 'gibi', 'en', 'daha',
  'cok', 'kadar', 'sonra', 'once', 'hangisi', 'hangisidir', 'asagidakilerden',
  'asagidaki', 'nedir', 'verilmistir', 'gorulur', 'gorulmez', 'degildir',
  'yanlistir', 'dogrudur', 'sorusu', 'hoca', 'slaytta', 'sinavda', 'cikmis',
  'soruldu', 'geldi', 'vardi', 'hasta', 'hastada', 'yasta', 'erkek', 'kadin'
]);

export function extractMedicalEntities(text: string): string[] {
  const normalized = normalizeMedicalText(text);
  const words = normalized.split(' ');
  const entities: string[] = [];

  for (const word of words) {
    if (word.length < 3 || MEDICAL_STOP_WORDS.has(word)) continue;

    // Tıbbi ek ve kalıp kontrolleri (ilaç son ekleri, patoloji terimleri)
    const isMedicalPattern =
      // İlaç son ekleri
      /(olol|pril|sartan|dipin|statin|cillin|penem|mycin|misin|siklidin|triptan|kain|afil|tidin|prazol|avir|umab|ib|azid|mide)$/i.test(word) ||
      // Mikrobiyoloji / Genetik / Biyokimya
      /(klor|gluk|lipid|kolest|enzim|kinaz|sentaz|laktat|eritro|loko|tromb|antijen|antikor|bakteri|virus|bacil|koku|suje)$/i.test(word) ||
      // Semptom / Sendrom / Anatomi
      /(odip|pleji|nefri|pne|hepat|kard|sinir|arter|ven|pleksus|lob|nodul|nekroz|fibroz|odip)$/i.test(word) ||
      // Sayısal klinik veriler (örn: 126, mg, ekg, ph, mmhg)
      /^\d+(mg|g|ml|meq|iu|mmhg)?$/i.test(word);

    if (isMedicalPattern || word.length >= 6) {
      if (!entities.includes(word)) {
        entities.push(word);
      }
    }
  }

  return entities;
}

// Soru kökünden sorunun neyi sorduğunu (hedefini) tahmin etme
export function detectQuestionTarget(text: string): 'etiology' | 'treatment' | 'diagnosis' | 'mechanism' | 'anatomy' | 'general' {
  const norm = normalizeMedicalText(text);

  if (/etken|mikroorganizma|bakteri|virus|parazit|ajan|sebep|hangi mikro|ajani/i.test(norm)) {
    return 'etiology';
  }
  if (/tedavi|ilac|farmako|ilk tercih|hangisi verilir|antidot|agonist|antagonist|blokor|doz/i.test(norm)) {
    return 'treatment';
  }
  if (/tani|tani koydurucu|biyopsi|laboratuvar|ekg|radyoloji|bt|mri|altin standart|en duyarlı/i.test(norm)) {
    return 'diagnosis';
  }
  if (/mekanizma|patofizyoloji|neden olur|yolak|reseptor|genetik|mutasyon|enzim eksikligi/i.test(norm)) {
    return 'mechanism';
  }
  if (/nerve|arter|kas|sinir|foramen|anatom|inervasyon|komsu|segment/i.test(norm)) {
    return 'anatomy';
  }
  return 'general';
}

// ==========================================
// BENZERLİK HESAPLAMA FONKSİYONLARI
// ==========================================

// Levenshtein benzerliği (0 - 1 arası oran)
export function calculateLevenshteinSimilarity(str1: string, str2: string): number {
  const s1 = normalizeMedicalText(str1);
  const s2 = normalizeMedicalText(str2);
  if (!s1 && !s2) return 1;
  if (!s1 || !s2) return 0;
  if (s1 === s2) return 1;

  const track = Array(s2.length + 1)
    .fill(null)
    .map(() => Array(s1.length + 1).fill(null));

  for (let i = 0; i <= s1.length; i += 1) track[0][i] = i;
  for (let j = 0; j <= s2.length; j += 1) track[j][0] = j;

  for (let j = 1; j <= s2.length; j += 1) {
    for (let i = 1; i <= s1.length; i += 1) {
      const indicator = s1[i - 1] === s2[j - 1] ? 0 : 1;
      track[j][i] = Math.min(
        track[j][i - 1] + 1, // deletion
        track[j - 1][i] + 1, // insertion
        track[j - 1][i - 1] + indicator // substitution
      );
    }
  }

  const distance = track[s2.length][s1.length];
  const maxLen = Math.max(s1.length, s2.length);
  return Math.max(0, 1 - distance / maxLen);
}

// Jaccard Token Kesişimi (0 - 100)
export function calculateTokenJaccard(textA: string, textB: string): number {
  const tokensA = new Set(normalizeMedicalText(textA).split(' ').filter(w => w.length > 2 && !MEDICAL_STOP_WORDS.has(w)));
  const tokensB = new Set(normalizeMedicalText(textB).split(' ').filter(w => w.length > 2 && !MEDICAL_STOP_WORDS.has(w)));

  if (tokensA.size === 0 && tokensB.size === 0) return 0;
  if (tokensA.size === 0 || tokensB.size === 0) return 0;

  let intersection = 0;
  tokensA.forEach((token) => {
    if (tokensB.has(token)) intersection++;
  });

  const union = new Set([...tokensA, ...tokensB]).size;
  return (intersection / union) * 100;
}

// ==========================================
// 1. ÇAPA SKORU (ANCHOR SCORE) HESAPLAMA
// ==========================================
/**
 * Bir taslağın ana soru kalıbı (çapa) olmaya ne kadar uygun olduğunu belirler.
 * Detaylı soru köküne, derse, konuya ve çoklu şıklara sahip sorular yüksek puan alır.
 */
export function calculateDraftAnchorScore(question: QuestionItem): DraftAnchorScore {
  let stemDetailScore = 0;
  let metadataScore = 0;
  let optionsScore = 0;
  let answerScore = 0;
  let socialScore = 0;

  // Soru kökü metnini topla
  const fullStem = [
    question.reconstruction?.stem || '',
    question.stem || '',
    question.rawStem || '',
    ...(question.fragments?.map((f) => f.text) || [])
  ].filter(Boolean).join(' ');

  const stemWords = fullStem.split(/\s+/).filter(Boolean).length;
  if (stemWords >= 35) stemDetailScore = 30;
  else if (stemWords >= 20) stemDetailScore = 22;
  else if (stemWords >= 10) stemDetailScore = 14;
  else if (stemWords > 3) stemDetailScore = 6;
  else stemDetailScore = 1;

  // Klinik vaka ve detay kelimeleri
  if (/hasta|sikayeti|fizik muayene|laboratuvar|tedavi|ekg|biyopsi/i.test(fullStem)) {
    stemDetailScore = Math.min(30, stemDetailScore + 5);
  }

  // Ders ve Konu Bilgisi
  const hasDiscipline = question.discipline && question.discipline !== 'Belirtilmedi' && question.discipline !== 'Kurul';
  const hasTopic = question.topic && !question.topic.includes('Numarası Belirsiz') && !question.topic.includes('Soru #');

  if (hasDiscipline) metadataScore += 15;
  if (hasTopic) metadataScore += 10;

  // Şık Sayısı ve Kalitesi (Kitapçık şıklarının varlığı)
  const validOptions = (question.options || []).filter((o) => o.text && o.text.trim().length > 1);
  if (validOptions.length >= 5) optionsScore = 25;
  else if (validOptions.length >= 4) optionsScore = 20;
  else if (validOptions.length >= 3) optionsScore = 15;
  else if (validOptions.length >= 1) optionsScore = 8;
  else optionsScore = 0;

  // Doğru Cevap Varlığı
  if (question.claimedAnswer || question.correctAnswer || question.reconstruction?.correctAnswer) {
    answerScore = 10;
  }

  // Sosyal ve Doğrulama Skoru (Katkıcılar, upvotelar, fragmentlar)
  const fragmentsCount = question.fragments?.length || 0;
  const upvotes = question.upvotes || 0;
  if (fragmentsCount >= 3 || upvotes >= 5) socialScore = 10;
  else if (fragmentsCount >= 1 || upvotes >= 1) socialScore = 6;

  const total = Math.min(100, stemDetailScore + metadataScore + optionsScore + answerScore + socialScore);

  let classification: 'anchor' | 'standard' | 'vague_fragment';
  if (total >= 65 && validOptions.length >= 2) {
    classification = 'anchor';
  } else if (total < 35 && validOptions.length <= 1) {
    classification = 'vague_fragment';
  } else {
    classification = 'standard';
  }

  return {
    total,
    isAnchor: classification === 'anchor',
    stemDetailScore,
    metadataScore,
    optionsScore,
    answerScore,
    socialScore,
    classification
  };
}

// ==========================================
// 2. ŞIK SIRASINDAN BAĞIMSIZ ŞIK KÜMESİ EŞLEŞTİRMESİ
// ==========================================
/**
 * Kitapçıklarda şıklar karışık sıralandığı için (Örn: A'daki Salbutamol, B'de D şıkkı olabilir),
 * şık harfine bakılmaksızın içerik benzerliği ve eşleşen şık sayısı hesaplanır.
 */
export function calculateOptionSetSimilarity(
  optionsA: QuestionOption[] = [],
  optionsB: QuestionOption[] = []
): { score: number; alignments: OptionAlignment[]; matchedCount: number } {
  const validA = optionsA.filter((o) => o.text && o.text.trim().length > 1);
  const validB = optionsB.filter((o) => o.text && o.text.trim().length > 1);

  if (validA.length === 0 || validB.length === 0) {
    return { score: 0, alignments: [], matchedCount: 0 };
  }

  const alignments: OptionAlignment[] = [];
  let totalMatchScore = 0;
  let matchedCount = 0;

  const usedBIndices = new Set<number>();

  for (const optA of validA) {
    let bestSim = 0;
    let bestBIdx = -1;

    for (let j = 0; j < validB.length; j++) {
      if (usedBIndices.has(j)) continue;
      const optB = validB[j];

      // Exact match or Levenshtein
      const sim = calculateLevenshteinSimilarity(optA.text, optB.text);
      if (sim > bestSim) {
        bestSim = sim;
        bestBIdx = j;
      }
    }

    if (bestBIdx !== -1 && bestSim >= 0.65) {
      usedBIndices.add(bestBIdx);
      matchedCount++;
      totalMatchScore += bestSim;
      alignments.push({
        anchorOption: optA,
        satelliteOption: validB[bestBIdx],
        similarity: bestSim,
        isShared: true
      });
    } else {
      alignments.push({
        anchorOption: optA,
        similarity: 0,
        isShared: false
      });
    }
  }

  // Max possible matches
  const minOptionsCount = Math.min(validA.length, validB.length);
  const rawRatio = matchedCount / minOptionsCount;

  // Eğer 2 veya daha fazla şık birebir aynıysa bu ÇOK GÜÇLÜ bir aynı soru kanıtıdır!
  let score = Math.round(rawRatio * 100);
  if (matchedCount >= 2 && score >= 60) {
    score = Math.min(100, score + 15);
  }

  return { score, alignments, matchedCount };
}

// ==========================================
// 3. İKİ TASLAK ARASINDA ÇOK KATMANLI UYUM ANALİZİ
// ==========================================
export function calculateDraftCompatibility(
  draftA: QuestionItem,
  draftB: QuestionItem
): DraftCompatibilityResult {
  const reasons: string[] = [];

  // A ve B'nin soru kökü metinleri
  const stemA = [
    draftA.reconstruction?.stem,
    draftA.stem,
    draftA.rawStem,
    ...(draftA.fragments?.map((f) => f.text) || [])
  ].filter(Boolean).join(' ');

  const stemB = [
    draftB.reconstruction?.stem,
    draftB.stem,
    draftB.rawStem,
    ...(draftB.fragments?.map((f) => f.text) || [])
  ].filter(Boolean).join(' ');

  // 1. Kök Benzerliği (Token Jaccard & Levenshtein)
  const tokenSim = calculateTokenJaccard(stemA, stemB);
  const levSim = calculateLevenshteinSimilarity(stemA, stemB) * 100;
  const stemSimilarity = Math.round(tokenSim * 0.7 + levSim * 0.3);

  if (stemSimilarity >= 60) {
    reasons.push(`Soru kökü ve ipuçları yüksek oranda (%${stemSimilarity}) benziyor.`);
  }

  // 2. Şık Kümesi Eşleşmesi (Şık sırasından bağımsız)
  const optionMatch = calculateOptionSetSimilarity(draftA.options, draftB.options);
  const optionSetSimilarity = optionMatch.score;

  if (optionMatch.matchedCount >= 2) {
    reasons.push(`${optionMatch.matchedCount} ortak şık tespit edildi (Kitapçık şık permütasyonu doğrulandı).`);
  } else if (optionMatch.matchedCount === 1) {
    reasons.push(`1 ortak şık örtüşmesi var.`);
  }

  // 3. Tıbbi Varlık ve Terim Kesişimi
  const entitiesA = extractMedicalEntities(stemA + ' ' + (draftA.options || []).map(o => o.text).join(' '));
  const entitiesB = extractMedicalEntities(stemB + ' ' + (draftB.options || []).map(o => o.text).join(' '));

  const sharedMedicalEntities = entitiesA.filter((e) => entitiesB.includes(e));

  if (sharedMedicalEntities.length >= 2) {
    reasons.push(`Kritik tıbbi varlıklar ortak: ${sharedMedicalEntities.slice(0, 4).join(', ')}`);
  }

  // 4. Doğru Cevap Tahmini Uyumu
  const answerA = draftA.claimedAnswer || draftA.correctAnswer || draftA.reconstruction?.correctAnswer;
  const answerB = draftB.claimedAnswer || draftB.correctAnswer || draftB.reconstruction?.correctAnswer;
  let answerAgreementBonus = 0;

  if (answerA && answerB) {
    // Şık harfi kitapçıklarda değişebilir. Bu yüzden harften ziyade metin karşılığına bakılır:
    const optTextA = draftA.options?.find(o => o.key === answerA)?.text || answerA;
    const optTextB = draftB.options?.find(o => o.key === answerB)?.text || answerB;

    const optSim = calculateLevenshteinSimilarity(optTextA, optTextB);
    if (optSim >= 0.8) {
      answerAgreementBonus = 15;
      reasons.push(`Öğrencilerin hatırladığı doğru cevaplar birbiriyle uyumlu ("${optTextA}").`);
    } else if (answerA === answerB && optionMatch.matchedCount > 0) {
      answerAgreementBonus = 10;
      reasons.push(`Aynı şık harfi (${answerA}) doğru cevap olarak işaretlenmiş.`);
    }
  }

  // 5. Soru Hedefi ve Çelişki Koruması (Aynı konuda birden fazla soru gelme durumu)
  const targetA = detectQuestionTarget(stemA);
  const targetB = detectQuestionTarget(stemB);

  let targetAlignment: 'matching' | 'different_aspect' | 'conflicting' = 'matching';
  let penalty = 0;

  if (targetA !== 'general' && targetB !== 'general' && targetA !== targetB) {
    // Örneğin biri etken sorarken diğeri ilaç soruyorsa
    targetAlignment = 'conflicting';
    penalty = 35; // Çelişki cezası! Aynı konuda iki farklı soru olabilir!
    reasons.push(`DİKKAT: Biri "${targetA}" diğeri "${targetB}" soruyor olabilir. Ayrı sorular olma ihtimali yüksek.`);
  } else if (targetA !== 'general' && targetB !== 'general' && targetA === targetB) {
    targetAlignment = 'matching';
    reasons.push(`Soru hedefi tam örtüşüyor (Her ikisi de "${targetA}" sorguluyor).`);
  }

  // 6. Kitapçık ve Soru Numarası Notu
  let bookletNumberNote: string | undefined;
  if (!draftA.isUnassignedNumber && !draftB.isUnassignedNumber && draftA.questionNumber && draftB.questionNumber) {
    if (draftA.questionNumber === draftB.questionNumber) {
      reasons.push(`Aynı soru numarasına sahipler (#${draftA.questionNumber}).`);
    } else {
      bookletNumberNote = `Farklı kitapçık numaraları tespit edildi (Biri #${draftA.questionNumber}, diğeri #${draftB.questionNumber}).`;
      reasons.push(bookletNumberNote);
    }
  }

  // 7. Nihai Uyum Skoru (Ağırlıklı Hesaplama)
  // Şık kümesi ve tıbbi varlıklar, soru kökü kelimelerinden daha güvenilirdir.
  let overallScore = 0;

  if (optionMatch.matchedCount >= 2) {
    // 2 ortak şık varsa en az %75 ile başlar
    overallScore = 75 + Math.min(25, sharedMedicalEntities.length * 5 + stemSimilarity * 0.15);
  } else if (sharedMedicalEntities.length >= 3) {
    // 3 nadir tıbbi terim ortaksa
    overallScore = 65 + Math.min(30, stemSimilarity * 0.3 + optionSetSimilarity * 0.2);
  } else {
    // Genel harmanlama
    overallScore = (
      stemSimilarity * 0.40 +
      optionSetSimilarity * 0.35 +
      Math.min(25, sharedMedicalEntities.length * 8)
    );
  }

  overallScore += answerAgreementBonus;
  overallScore -= penalty;
  overallScore = Math.max(0, Math.min(100, Math.round(overallScore)));

  // Tavsiye Kararı
  let recommendation: 'auto_merge' | 'suggest_merge' | 'distinct';
  if (overallScore >= 82 && targetAlignment !== 'conflicting') {
    recommendation = 'auto_merge';
  } else if (overallScore >= 55 && targetAlignment !== 'conflicting') {
    recommendation = 'suggest_merge';
  } else {
    recommendation = 'distinct';
  }

  return {
    score: overallScore,
    recommendation,
    reasons,
    stemSimilarity,
    optionSetSimilarity,
    sharedMedicalEntities,
    targetQuestionAlignment: targetAlignment,
    bookletNumberNote,
    matchedOptionAlignments: optionMatch.alignments
  };
}

// ==========================================
// 4. BİRLEŞTİRME VE İÇ İÇE GEÇİRME MOTORU
// ==========================================
/**
 * Anchor soru ile uydu taslakları tek bir yetkin soru altında toplar.
 * Öğrenci katkılarını ve şıklarını kaybetmeden eksiksiz 5 şık ve zengin soruya dönüştürür.
 */
export function mergeDrafts(
  anchorQuestion: QuestionItem,
  satelliteQuestions: QuestionItem[],
  performedBy: { name?: string; uid?: string; email?: string } = {}
): { consolidated: QuestionItem; mergedIds: string[] } {
  const mergedIds: string[] = satelliteQuestions.map((q) => q.id);
  const now = new Date().toISOString();

  // 1. Yeni veya mevcut parçacıkları topla (Memory Fragments)
  const consolidatedFragments: MemoryFragment[] = [...(anchorQuestion.fragments || [])];

  // 2. Şıkları harmanla (Disjoint options - A, B Kitapçığındaki farklı şıkları bir araya getir)
  const consolidatedOptions: QuestionOption[] = [...(anchorQuestion.options || [])];

  for (const sat of satelliteQuestions) {
    // Uydu taslağın kökünü bir fragment olarak ekle (hatırlanan parça olarak koru)
    const satStem = sat.reconstruction?.stem || sat.stem || sat.rawStem || '';
    if (satStem && !consolidatedFragments.some((f) => f.text.trim() === satStem.trim())) {
      consolidatedFragments.push({
        id: `f-merged-${Date.now()}-${Math.random().toString(36).substring(2, 6)}`,
        author: sat.contributedByName || sat.author || 'Anonim Katkıcı',
        authorUid: sat.contributedByUid,
        authorStudentNumber: sat.contributedByStudentNumber,
        text: `[Birleştirilen Taslak #${sat.questionNumber || 'Belirsiz'}]: ${satStem}`,
        type: 'stem',
        timestamp: now,
        upvotes: sat.upvotes || 1
      });
    }

    // Uydu taslaktaki var olan fragmentları aktar
    if (sat.fragments && sat.fragments.length > 0) {
      for (const f of sat.fragments) {
        if (!consolidatedFragments.some((cf) => cf.id === f.id || cf.text === f.text)) {
          consolidatedFragments.push(f);
        }
      }
    }

    // Şıkları harmanla
    if (sat.options && sat.options.length > 0) {
      for (const satOpt of sat.options) {
        if (!satOpt.text || !satOpt.text.trim()) continue;

        // Anchor şıklarında bu metne çok benzer bir şık var mı?
        const existingOpt = consolidatedOptions.find((ao) =>
          calculateLevenshteinSimilarity(ao.text, satOpt.text) >= 0.8
        );

        if (existingOpt) {
          // Var olan şıkkın upvote'unu artır
          existingOpt.upvotes = (existingOpt.upvotes || 1) + (satOpt.upvotes || 1);
        } else {
          // Henüz eklenmemiş bir şık ise, boş olan bir harf anahtarına ata (A, B, C, D, E)
          const usedKeys = new Set(consolidatedOptions.map((o) => o.key));
          const availableKey = (['A', 'B', 'C', 'D', 'E'] as const).find((k) => !usedKeys.has(k));

          if (availableKey) {
            consolidatedOptions.push({
              key: availableKey,
              text: satOpt.text.trim(),
              suggestedBy: satOpt.suggestedBy || sat.contributedByName || 'Taslak Birleştirme',
              suggestedByUid: satOpt.suggestedByUid || sat.contributedByUid,
              upvotes: satOpt.upvotes || 1
            });
          }
        }
      }
    }
  }

  // 3. Etiketleri birleştir
  const allTags = new Set([
    ...(anchorQuestion.tags || []),
    ...satelliteQuestions.flatMap((q) => q.tags || []),
    'taslak-birlestirildi'
  ]);

  // 4. Revizyon geçmişine kaydet
  const revisions: QuestionRevision[] = [
    ...(anchorQuestion.revisions || []),
    {
      id: `rev-merge-${Date.now()}`,
      version: (anchorQuestion.revisions?.length || 0) + 1,
      editedAt: now,
      editorName: performedBy.name || 'Akıllı Taslak Konsolidasyonu',
      editorUid: performedBy.uid,
      changeSummary: `${satelliteQuestions.length} adet benzer taslak bu ana soru altında birleştirildi.`
    }
  ];

  // 5. Konsolide edilmiş soru nesnesi
  const consolidated: QuestionItem = {
    ...anchorQuestion,
    fragments: consolidatedFragments,
    options: consolidatedOptions.sort((a, b) => a.key.localeCompare(b.key)),
    tags: Array.from(allTags),
    status: consolidatedOptions.length >= 4 && consolidatedFragments.length >= 2 ? 'gathering' : anchorQuestion.status,
    revisions,
    updatedAt: now,
    placementNotes: [
      anchorQuestion.placementNotes || '',
      `[${new Date().toLocaleDateString('tr-TR')}]: ${satelliteQuestions.length} taslak ile iç içe geçirildi.`
    ].filter(Boolean).join(' ')
  };

  return { consolidated, mergedIds };
}

// ==========================================
// 5. BÜTÜNSEL KOMİTE TASLAK KÜMELEME SERVİSİ
// ==========================================
/**
 * Komitedeki tüm soruları ve taslakları tarar.
 * Fazlalık taslakları tespit edip gerçek soru sayısını tahmin eder ve birleştirme kümeleri üretir.
 */
export function clusterDraftsForCommittee(
  questions: QuestionItem[],
  committeeId: string
): ClusterAnalysisSummary {
  const commQuestions = questions.filter((q) => q.committeeId === committeeId);

  // Her taslağın Çapa Skorunu hesapla
  const scoredQuestions = commQuestions.map((q) => ({
    question: q,
    anchorScore: calculateDraftAnchorScore(q)
  }));

  // Puanı yüksek olanlar önce gelecek şekilde sırala
  scoredQuestions.sort((a, b) => b.anchorScore.total - a.anchorScore.total);

  const assignedToCluster = new Set<string>();
  const clusters: DraftCluster[] = [];
  const unmatchedVagueDrafts: QuestionItem[] = [];

  for (let i = 0; i < scoredQuestions.length; i++) {
    const current = scoredQuestions[i];
    if (assignedToCluster.has(current.question.id)) continue;

    // Eğer soru tamamen muğlaksa ve henüz kimseyle eşleşmediyse
    if (current.anchorScore.classification === 'vague_fragment') {
      unmatchedVagueDrafts.push(current.question);
      continue;
    }

    const satellites: Array<{ question: QuestionItem; compatibility: DraftCompatibilityResult }> = [];

    // Diğer taslaklarla uyumunu test et
    for (let j = 0; j < scoredQuestions.length; j++) {
      if (i === j) continue;
      const candidate = scoredQuestions[j];
      if (assignedToCluster.has(candidate.question.id)) continue;

      const comp = calculateDraftCompatibility(current.question, candidate.question);

      if (comp.recommendation !== 'distinct') {
        satellites.push({
          question: candidate.question,
          compatibility: comp
        });
        assignedToCluster.add(candidate.question.id);
      }
    }

    if (satellites.length > 0) {
      assignedToCluster.add(current.question.id);

      const avgConfidence = Math.round(
        satellites.reduce((acc, s) => acc + s.compatibility.score, 0) / satellites.length
      );

      clusters.push({
        id: `cluster-${current.question.id}-${Date.now()}`,
        committeeId,
        anchorQuestion: current.question,
        satelliteDrafts: satellites,
        overallConfidence: avgConfidence,
        status: avgConfidence >= 80 ? 'ready_to_merge' : 'needs_review',
        estimatedUniqueSlots: 1
      });
    }
  }

  // Muğlak soruların kalanları için çapa taraması (tekrar kontrol)
  const remainingVague: QuestionItem[] = [];
  for (const vagueQ of unmatchedVagueDrafts) {
    if (assignedToCluster.has(vagueQ.id)) continue;

    let bestCluster: DraftCluster | null = null;
    let bestScore = 0;
    let bestComp: DraftCompatibilityResult | null = null;

    for (const cluster of clusters) {
      const comp = calculateDraftCompatibility(cluster.anchorQuestion, vagueQ);
      if (comp.score > bestScore && comp.score >= 50 && comp.targetQuestionAlignment !== 'conflicting') {
        bestScore = comp.score;
        bestCluster = cluster;
        bestComp = comp;
      }
    }

    if (bestCluster && bestComp) {
      bestCluster.satelliteDrafts.push({
        question: vagueQ,
        compatibility: bestComp
      });
      assignedToCluster.add(vagueQ.id);
    } else {
      remainingVague.push(vagueQ);
    }
  }

  const identifiedAnchors = clusters.length;
  const potentialSavedDuplicates = clusters.reduce((acc, c) => acc + c.satelliteDrafts.length, 0);
  const estimatedTrueQuestions = commQuestions.length - potentialSavedDuplicates;

  return {
    totalDrafts: commQuestions.length,
    estimatedTrueQuestions,
    identifiedAnchors,
    vagueDraftsCount: remainingVague.length,
    mergeableClustersCount: clusters.length,
    potentialSavedDuplicates,
    clusters,
    unmatchedVagueDrafts: remainingVague
  };
}

// ==========================================
// 6. ANLIK YAZARKEN BENZERLİK ARAMA (REAL-TIME AUTO-SUGGEST)
// ==========================================
/**
 * Kullanıcı katkı modalında soru veya ipucu yazarken,
 * var olan taslaklar arasında %60'tan fazla benzeyen bir soru varsa anında yakalar.
 * Böylece kullanıcı yeni bir taslak açmak yerine var olan soruya doğrudan katkı sağlar.
 */
export function findRealtimeMatchingDraft(
  input: {
    committeeId: string;
    discipline?: string;
    topic?: string;
    text: string;
    options?: Array<{ key: string; text: string }>;
  },
  existingQuestions: QuestionItem[]
): {
  matchFound: boolean;
  matchedQuestion?: QuestionItem;
  compatibility?: DraftCompatibilityResult;
} {
  if (!input.text || input.text.trim().length < 8) {
    return { matchFound: false };
  }

  // Sahte bir geçici soru oluşturup mevcut sorularla karşılaştır
  const tempQuestion: QuestionItem = {
    id: 'temp-input',
    committeeId: input.committeeId,
    questionNumber: 0,
    discipline: input.discipline || 'Belirtilmedi',
    topic: input.topic || '',
    status: 'gathering',
    fragments: [
      {
        id: 'temp-f',
        author: 'Geçici',
        text: input.text,
        type: 'stem',
        timestamp: new Date().toISOString(),
        upvotes: 0
      }
    ],
    options: (input.options || []).map((o) => ({
      key: o.key as any,
      text: o.text,
      upvotes: 0
    })),
    tags: [],
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  };

  const pool = existingQuestions.filter((q) => q.committeeId === input.committeeId);

  let bestMatch: QuestionItem | null = null;
  let bestComp: DraftCompatibilityResult | null = null;
  let highestScore = 0;

  for (const q of pool) {
    const comp = calculateDraftCompatibility(q, tempQuestion);
    if (comp.score > highestScore && comp.score >= 58 && comp.targetQuestionAlignment !== 'conflicting') {
      highestScore = comp.score;
      bestMatch = q;
      bestComp = comp;
    }
  }

  if (bestMatch && bestComp) {
    return {
      matchFound: true,
      matchedQuestion: bestMatch,
      compatibility: bestComp
    };
  }

  return { matchFound: false };
}
