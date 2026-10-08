/**
 * ==============================================================================
 * MedSoru Akıllı Taslak Kümeleme, Çapa Soru Tespiti ve Birleştirme Motoru
 * (src/services/draftClusteringService.ts) - Gelişmiş Tıbbi Kavram & AI Destekli
 * ==============================================================================
 */

import { QuestionItem, MemoryFragment, QuestionOption, QuestionRevision, AlternativeOption } from '../types';
import { GoogleGenAI } from '@google/genai';
import { areWordsFuzzyEqual, damerauLevenshtein, foldTurkish, toContextHashtag } from '../utils/fuzzyMatching.ts';

// ==========================================
// TİPLER VE VERİ YAPILARI
// ==========================================

export interface DraftAnchorScore {
  total: number; // 0 - 100
  isAnchor: boolean;
  stemDetailScore: number;
  metadataScore: number;
  optionsScore: number;
  answerScore: number;
  socialScore: number;
  classification: 'anchor' | 'standard' | 'vague_fragment';
}

export interface OptionAlignment {
  anchorOption?: QuestionOption;
  satelliteOption?: QuestionOption;
  similarity: number;
  isShared: boolean;
}

export interface DraftCompatibilityResult {
  score: number; // 0 - 100
  recommendation: 'auto_merge' | 'suggest_merge' | 'distinct';
  reasons: string[];
  stemSimilarity: number;
  optionSetSimilarity: number;
  sharedMedicalEntities: string[];
  sharedConcepts: string[];
  contextHashtag?: string;
  targetQuestionAlignment: 'matching' | 'different_aspect' | 'conflicting';
  bookletNumberNote?: string;
  matchedOptionAlignments: OptionAlignment[];
  aiAnalysis?: {
    isSameQuestion: boolean;
    confidence: number;
    explanation: string;
    commonSubject?: string;
  };
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
  detectedSubject?: string;
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
// KÜMELEME HASSASİYET AYARI + "AYNI DEĞİL" ENGEL LİSTESİ
// ==========================================

export interface ClusterTuning {
  /** Bu puanın üstü otomatik birleştirme adayıdır. */
  autoThreshold: number;
  /** Bu puanın üstü incelemeye değerdir. */
  suggestThreshold: number;
  /** Muğlak taslakların kümeye tutunma eşiği. */
  vagueAttachThreshold: number;
  /** Kümenin "hazır" sayılacağı ortalama güven. */
  readyConfidence: number;
  /** Çapa kalitesi eşiği (altı her zaman incelemeye düşer). */
  anchorQualityThreshold: number;
  /** "Aynı değil" işaretlenmiş id çiftleri. */
  blocked?: Set<string>;
}

export const CLUSTER_PRESETS: Record<'strict' | 'balanced' | 'loose', Omit<ClusterTuning, 'blocked'>> = {
  strict: { autoThreshold: 80, suggestThreshold: 50, vagueAttachThreshold: 55, readyConfidence: 75, anchorQualityThreshold: 50 },
  balanced: { autoThreshold: 68, suggestThreshold: 38, vagueAttachThreshold: 45, readyConfidence: 70, anchorQualityThreshold: 40 },
  loose: { autoThreshold: 60, suggestThreshold: 30, vagueAttachThreshold: 35, readyConfidence: 60, anchorQualityThreshold: 30 },
};

export const DEFAULT_CLUSTER_TUNING: Omit<ClusterTuning, 'blocked'> = CLUSTER_PRESETS.balanced;

export function resolveTuning(tuning?: ClusterTuning): Required<Omit<ClusterTuning, 'blocked'>> & Pick<ClusterTuning, 'blocked'> {
  const base = { ...DEFAULT_CLUSTER_TUNING, ...(tuning || {}) };
  return base as Required<Omit<ClusterTuning, 'blocked'>> & Pick<ClusterTuning, 'blocked'>;
}

export const pairKey = (a: string, b: string) => [a || '', b || ''].sort().join('|');

const BLOCK_KEY = 'medsoru_cluster_blocklist_v1';

function readBlockStorage(): Set<string> {
  try {
    if (typeof localStorage === 'undefined') return new Set();
    const raw = localStorage.getItem(BLOCK_KEY);
    if (!raw) return new Set();
    const arr = JSON.parse(raw);
    return new Set(Array.isArray(arr) ? arr.filter((x) => typeof x === 'string') : []);
  } catch {
    return new Set();
  }
}

/** Kullanıcının "aynı soru değil" dediği çiftler (kalıcı, tarayıcıda saklanır). */
export function loadBlockedPairs(): Set<string> {
  return readBlockStorage();
}

export function blockPair(a: string, b: string): Set<string> {
  const next = readBlockStorage();
  next.add(pairKey(a, b));
  try {
    if (typeof localStorage !== 'undefined') {
      localStorage.setItem(BLOCK_KEY, JSON.stringify([...next]));
    }
  } catch {
    /* yoksay */
  }
  return next;
}

export function clearBlockedPairs(): void {
  try {
    if (typeof localStorage !== 'undefined') localStorage.removeItem(BLOCK_KEY);
  } catch {
    /* yoksay */
  }
}

// ==========================================
// TIBBİ KAVRAM VE SENDROM KÜMELERİ (MED-CONCEPT BANKS)
// ==========================================

export interface MedicalConceptBank {
  id: string;
  name: string;
  disciplines: string[];
  terms: string[];
}

// 2,4 MB'lık kavram bankası ilk açılışı yavaşlatmasın diye ayrı parça olarak, boşta yüklenir.
// Yüklenene kadar kavram tespiti boş döner; taslak eşleştirme metin benzerliğiyle çalışmaya devam eder.
export let MEDICAL_CONCEPT_BANKS: MedicalConceptBank[] = [];
let conceptsPromise: Promise<void> | null = null;
export function loadMedicalConcepts(): Promise<void> {
  if (!conceptsPromise) {
    conceptsPromise = import('../data/medicalConcepts5000.json')
      .then((m: any) => {
        MEDICAL_CONCEPT_BANKS = (m ? (m.default || m) : []) as MedicalConceptBank[];
        termToConceptMap = null;
        fuzzyBuckets = null;
        fuzzyCache.clear();
      })
      .catch(() => { conceptsPromise = null; });
  }
  return conceptsPromise;
}

// ==========================================
// METİN NORMALİZASYONU (TÜRKÇE DESTEKLİ)
// ==========================================

export function normalizeMedicalText(text: string = ''): string {
  if (!text) return '';
  return text
    .toLocaleLowerCase('tr-TR')
    .replace(/ı/g, 'i')
    .replace(/ğ/g, 'g')
    .replace(/ü/g, 'u')
    .replace(/ş/g, 's')
    .replace(/ö/g, 'o')
    .replace(/ç/g, 'c')
    .replace(/[^a-z0-9\s]/gi, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

const MEDICAL_STOP_WORDS = new Set([
  'bir', 've', 'ile', 'bu', 'icin', 'olan', 'olarak', 'gibi', 'en', 'daha',
  'cok', 'kadar', 'sonra', 'once', 'hangisi', 'hangisidir', 'asagidakilerden',
  'asagidaki', 'nedir', 'verilmistir', 'gorulur', 'gorulmez', 'degildir',
  'yanlistir', 'dogrudur', 'sorusu', 'hoca', 'slaytta', 'sinavda', 'cikmis',
  'soruldu', 'geldi', 'vardi', 'hasta', 'hastada', 'yasta', 'erkek', 'kadin',
  'ben', 'bence', 'sanki', 'diye', 'kismini', 'hatirliyorum', 'soruyordu',
  'tibbi', 'hatirlanan', 'soru', 'dersi', 'kurul', 'bolum', 'anabilim', 'dali', 'ipucu', 'donem', 'patoloji', 'farmakoloji', 'mikrobiyoloji', 'biyokimya', 'anatomi', 'fizyoloji', 'histoloji', 'genetik', 'dahiliye', 'pediatri'
]);

export function extractMedicalEntities(text: string): string[] {
  const normalized = normalizeMedicalText(text);
  const words = normalized.split(' ');
  const entities: string[] = [];

  // Önemli kısa tıbbi kısaltmalar ve terimler
  const shortMedicalTerms = new Set([
    'nt', 'av', 'ekg', 'usg', 'mri', 'bt', 'arb', 'bcye', 'dna', 'rna',
    'down', 'ense', 'kalp', 'burun', 'bebek', 'koku', 'kemi', 'kemik',
    'pam', 'ace', 'dm', 'ht', 'vsd', 'asd', 'avsd', 'tbc', 'crp', 'esr'
  ]);

  for (const word of words) {
    if (word.length < 2 || MEDICAL_STOP_WORDS.has(word)) continue;

    if (shortMedicalTerms.has(word)) {
      if (!entities.includes(word)) entities.push(word);
      continue;
    }

    if (word.length < 3) continue;

    // Tıbbi sonekler ve örüntüler
    const isMedicalPattern =
      /(olol|pril|sartan|dipin|statin|cillin|penem|mycin|misin|siklidin|triptan|kain|afil|tidin|prazol|avir|umab|ib|azid|mide)$/i.test(word) ||
      /(klor|gluk|lipid|kolest|enzim|kinaz|sentaz|laktat|eritro|loko|tromb|antijen|antikor|bakteri|virus|bacil|koku|suje)$/i.test(word) ||
      /(odip|pleji|nefri|pne|hepat|kard|sinir|arter|ven|pleksus|lob|nodul|nekroz|fibroz|trizomi|kromozom|karyotip)$/i.test(word) ||
      /^\d+(mg|g|ml|meq|iu|mmhg)?$/i.test(word);

    if (isMedicalPattern || word.length >= 4) {
      if (!entities.includes(word)) {
        entities.push(word);
      }
    }
  }

  return entities;
}

// Hızlı Ters İndeks (Inverted Index) - 5,000+ Tıbbi Kavram için O(1) arama
let termToConceptMap: Map<string, MedicalConceptBank[]> | null = null;

function getTermToConceptMap(): Map<string, MedicalConceptBank[]> {
  if (termToConceptMap) return termToConceptMap;
  if (MEDICAL_CONCEPT_BANKS.length === 0) {
    void loadMedicalConcepts();
    return new Map();
  }
  termToConceptMap = new Map();

  for (const concept of MEDICAL_CONCEPT_BANKS) {
    if (!concept.terms) continue;
    for (const term of concept.terms) {
      const cleanTerm = normalizeMedicalText(term);
      if (cleanTerm.length < 3 || MEDICAL_STOP_WORDS.has(cleanTerm)) continue;
      const list = termToConceptMap.get(cleanTerm);
      if (list) {
        if (list.length < 30) {
          list.push(concept);
        }
      } else {
        termToConceptMap.set(cleanTerm, [concept]);
      }
    }
  }
  return termToConceptMap;
}

// Bulanık arama için terimler uzunluk + ilk harfe göre gruplanır: her öbekte sözlüğün tamamını
// taramak yerine yalnızca ±2 uzunluktaki ve aynı harfle başlayan terimlere bakılır (yazarken donmayı önler).
let fuzzyBuckets: Map<string, string[]> | null = null;
const fuzzyCache = new Map<string, string | null>();
function fuzzyLookup(phrase: string): MedicalConceptBank[] | undefined {
  const index = getTermToConceptMap();
  if (!fuzzyBuckets) {
    fuzzyBuckets = new Map();
    for (const term of index.keys()) {
      const key = `${term.length}:${term[0]}`;
      const list = fuzzyBuckets.get(key);
      if (list) list.push(term);
      else fuzzyBuckets.set(key, [term]);
    }
  }
  let found = fuzzyCache.get(phrase);
  if (found === undefined) {
    found = null;
    outer: for (let d = 0; d <= 2; d++) {
      for (const len of d === 0 ? [phrase.length] : [phrase.length - d, phrase.length + d]) {
        for (const term of fuzzyBuckets.get(`${len}:${phrase[0]}`) || []) {
          if (areWordsFuzzyEqual(phrase, term)) { found = term; break outer; }
        }
      }
    }
    if (fuzzyCache.size > 5000) fuzzyCache.clear();
    fuzzyCache.set(phrase, found);
  }
  return found ? index.get(found) : undefined;
}

/** Sözlük indekslerini tarayıcı boştayken kurar; ilk tuş vuruşu bu maliyeti ödemez. */
export function warmMedicalIndex(): void {
  const run = () => {
    loadMedicalConcepts().then(() => {
      try { getTermToConceptMap(); fuzzyLookup('hiperkalsemi'); } catch { /* yok say */ }
    });
  };
  const ric = (window as any).requestIdleCallback as undefined | ((cb: () => void, o?: { timeout: number }) => void);
  if (ric) ric(run, { timeout: 4000 });
  else setTimeout(run, 1500);
}

// Metinden eşleşen Tıbbi Kavram Bankalarını bulma (5,000+ kavram üzerinde anlık O(1) eşleşme)
export function detectMedicalConcepts(text: string, discipline?: string): MedicalConceptBank[] {
  const norm = normalizeMedicalText(text);
  if (!norm || norm.length < 3) return [];

  const index = getTermToConceptMap();
  const matchedMap = new Map<string, { concept: MedicalConceptBank; matchCount: number }>();
  const words = norm.split(' ').filter((w) => w.length >= 3 && !MEDICAL_STOP_WORDS.has(w));

  // 1'li, 2'li ve 3'lü kelime öbeklerini oluştur
  const phrases: string[] = [...words];
  for (let i = 0; i < words.length - 1; i++) {
    phrases.push(`${words[i]} ${words[i + 1]}`);
    if (i < words.length - 2) {
      phrases.push(`${words[i]} ${words[i + 1]} ${words[i + 2]}`);
    }
  }

  const discLower = discipline && discipline !== 'Belirtilmedi' ? discipline.toLowerCase() : null;

  for (const phrase of phrases) {
    let hits = index.get(phrase);
    if (!hits && phrase.length >= 6) {
      // Harf eksikliği ve yer değiştirmesi için terim bankasında bulanık arama (gruplu + önbellekli)
      hits = fuzzyLookup(phrase);
    }
    if (!hits) continue;

    for (const concept of hits) {
      if (discLower && concept.disciplines && concept.disciplines.length > 0) {
        const discMatch = concept.disciplines.some(
          (d) => discLower.includes(d.toLowerCase()) || d.toLowerCase().includes(discLower)
        );
        if (!discMatch) continue;
      }

      const existing = matchedMap.get(concept.id);
      if (existing) {
        existing.matchCount++;
      } else {
        matchedMap.set(concept.id, { concept, matchCount: 1 });
      }
    }
  }

  return Array.from(matchedMap.values())
    .sort((a, b) => b.matchCount - a.matchCount)
    .map((item) => item.concept);
}

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
// BENZERLİK HESAPLAMA METOTLARI
// ==========================================

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
        track[j][i - 1] + 1,
        track[j - 1][i] + 1,
        track[j - 1][i - 1] + indicator
      );
    }
  }

  const distance = track[s2.length][s1.length];
  const maxLen = Math.max(s1.length, s2.length);
  return Math.max(0, 1 - distance / maxLen);
}

export function calculateTokenJaccard(textA: string, textB: string): number {
  const tokensA = Array.from(new Set(normalizeMedicalText(textA).split(' ').filter(w => w.length > 2 && !MEDICAL_STOP_WORDS.has(w))));
  const tokensB = Array.from(new Set(normalizeMedicalText(textB).split(' ').filter(w => w.length > 2 && !MEDICAL_STOP_WORDS.has(w))));

  if (tokensA.length === 0 && tokensB.length === 0) return 0;
  if (tokensA.length === 0 || tokensB.length === 0) return 0;

  const setB = new Set(tokensB);
  let intersection = 0;
  const matchedB = new Set<string>();

  for (const tokenA of tokensA) {
    if (setB.has(tokenA)) {
      intersection += 1.0;
      matchedB.add(tokenA);
    } else {
      // Harf eksikliği (sendrmu -> sendromu) ve yer değiştirmesi (sendormu -> sendromu) denetimi
      const fuzzyMatch = tokensB.find((b) => !matchedB.has(b) && areWordsFuzzyEqual(tokenA, b));
      if (fuzzyMatch) {
        intersection += 0.9;
        matchedB.add(fuzzyMatch);
      }
    }
  }

  const union = tokensA.length + tokensB.length - intersection;
  return Math.min(100, (intersection / Math.max(1, union)) * 100);
}

// ==========================================
// 1. ÇAPA SKORU (ANCHOR SCORE) HESAPLAMA
// ==========================================
export function calculateDraftAnchorScore(question: QuestionItem): DraftAnchorScore {
  let stemDetailScore = 0;
  let metadataScore = 0;
  let optionsScore = 0;
  let answerScore = 0;
  let socialScore = 0;

  const fullStem = [
    question.reconstruction?.stem || '',
    question.stem || '',
    question.rawStem || '',
    ...(question.fragments?.map((f) => f.text) || [])
  ].filter(Boolean).join(' ');

  const stemWords = fullStem.split(/\s+/).filter(Boolean).length;
  if (stemWords >= 30) stemDetailScore = 30;
  else if (stemWords >= 18) stemDetailScore = 22;
  else if (stemWords >= 10) stemDetailScore = 15;
  else if (stemWords > 3) stemDetailScore = 8;
  else stemDetailScore = 2;

  if (/hasta|sikayet|muayene|laboratuvar|tedavi|ekg|biyopsi|ultrason|trizomi|sendrom/i.test(fullStem)) {
    stemDetailScore = Math.min(30, stemDetailScore + 5);
  }

  const hasDiscipline = question.discipline && question.discipline !== 'Belirtilmedi' && question.discipline !== 'Kurul';
  const hasTopic = question.topic && !question.topic.includes('Numarası Belirsiz') && !question.topic.includes('Soru #');

  if (hasDiscipline) metadataScore += 15;
  if (hasTopic) metadataScore += 10;

  const validOptions = (question.options || []).filter((o) => o.text && o.text.trim().length > 1);
  if (validOptions.length >= 5) optionsScore = 25;
  else if (validOptions.length >= 4) optionsScore = 20;
  else if (validOptions.length >= 2) optionsScore = 15;
  else if (validOptions.length >= 1) optionsScore = 8;
  else optionsScore = 0;

  if (question.claimedAnswer || question.correctAnswer || question.reconstruction?.correctAnswer) {
    answerScore = 10;
  }

  const fragmentsCount = question.fragments?.length || 0;
  const upvotes = question.upvotes || 0;
  if (fragmentsCount >= 3 || upvotes >= 4) socialScore = 10;
  else if (fragmentsCount >= 1 || upvotes >= 1) socialScore = 6;

  const total = Math.min(100, stemDetailScore + metadataScore + optionsScore + answerScore + socialScore);

  let classification: 'anchor' | 'standard' | 'vague_fragment';
  // Düzeltme: Şık sayısı az olsa bile vaka/kök detayı yüksek ve dersi belli sorular çapa olabilir!
  if (total >= 50 && stemWords >= 12 && hasDiscipline) {
    classification = 'anchor';
  } else if (total < 30 && stemWords < 8) {
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
// 2. ŞIK KÜMESİ BENZERLİĞİ
// ==========================================
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

  const minOptionsCount = Math.min(validA.length, validB.length);
  const rawRatio = matchedCount / minOptionsCount;
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
  draftB: QuestionItem,
  tuning?: ClusterTuning
): DraftCompatibilityResult {
  const t = resolveTuning(tuning);
  const reasons: string[] = [];

  const distinct = (why: string): DraftCompatibilityResult => ({
    score: 0,
    recommendation: 'distinct',
    reasons: [why],
    stemSimilarity: 0,
    optionSetSimilarity: 0,
    sharedMedicalEntities: [],
    sharedConcepts: [],
    targetQuestionAlignment: 'conflicting',
    matchedOptionAlignments: []
  });

  // -1. KULLANICI ENGELİ: daha önce "aynı soru değil" denmiş çift asla kümelenmez.
  if (t.blocked?.has(pairKey(draftA.id, draftB.id))) {
    return distinct('Daha önce farklı sorular olarak işaretlendi.');
  }

  const textA = [
    draftA.topic,
    draftA.reconstruction?.stem,
    draftA.stem,
    draftA.rawStem,
    ...(draftA.fragments?.map((f) => f.text) || []),
    ...(draftA.options || []).map((o) => o.text)
  ].filter(Boolean).join(' ');

  const textB = [
    draftB.topic,
    draftB.reconstruction?.stem,
    draftB.stem,
    draftB.rawStem,
    ...(draftB.fragments?.map((f) => f.text) || []),
    ...(draftB.options || []).map((o) => o.text)
  ].filter(Boolean).join(' ');

  // 0. DERS ÇELİŞKİ KORUYUCUSU (Discipline Hard Guardrail)
  const discA = (draftA.discipline || '').trim().toLowerCase();
  const discB = (draftB.discipline || '').trim().toLowerCase();
  const isGenericA = !discA || discA === 'belirtilmedi' || discA === 'kurul' || discA === 'tip';
  const isGenericB = !discB || discB === 'belirtilmedi' || discB === 'kurul' || discB === 'tip';

  if (!isGenericA && !isGenericB && discA !== discB) {
    // İki farklı ana ders (Örn: Tıbbi Patoloji ≠ Tıbbi Genetik) asla birleşemez!
    return {
      score: 0,
      recommendation: 'distinct',
      reasons: [`Farklı anabilim dalı / ders (${draftA.discipline} ≠ ${draftB.discipline}).`],
      stemSimilarity: 0,
      optionSetSimilarity: 0,
      sharedMedicalEntities: [],
      sharedConcepts: [],
      targetQuestionAlignment: 'conflicting',
      matchedOptionAlignments: []
    };
  }

  // 1. Ders Uyumu
  const sameDiscipline = !isGenericA && !isGenericB && discA === discB;
  if (sameDiscipline) {
    reasons.push(`Aynı ders havuzu (${draftA.discipline}).`);
  }

  // 2. Tıbbi Kavram Bankası Eşleşmesi (Sendrom & Konsept Kümeleri)
  const conceptsA = detectMedicalConcepts(textA, draftA.discipline);
  const conceptsB = detectMedicalConcepts(textB, draftB.discipline);
  const sharedConcepts = conceptsA.filter((ca) => conceptsB.some((cb) => cb.id === ca.id));

  let conceptBonus = 0;
  if (sharedConcepts.length > 0) {
    // Tek bir kavram adı (65 puanlık eski taban) tek başına hükmetmez;
    // asıl ağırlık kök + terim + şık kanıtındadır.
    conceptBonus = 40;
    reasons.push(`Ortak tıbbi sendrom/kavram tespit edildi: "${sharedConcepts[0].name}".`);
  }

  // 3. Kök Benzerliği (Token Jaccard & Levenshtein)
  const tokenSim = calculateTokenJaccard(textA, textB);
  const levSim = calculateLevenshteinSimilarity(textA, textB) * 100;
  const stemSimilarity = Math.round(tokenSim * 0.7 + levSim * 0.3);

  if (stemSimilarity >= 45) {
    reasons.push(`Soru metni ve ipuçları benziyor (%${stemSimilarity}).`);
  }

  // 4. Şık Kümesi Eşleşmesi (Şık sırasından bağımsız)
  const optionMatch = calculateOptionSetSimilarity(draftA.options, draftB.options);
  const optionSetSimilarity = optionMatch.score;

  if (optionMatch.matchedCount >= 2) {
    reasons.push(`${optionMatch.matchedCount} ortak şık tespit edildi (Kitapçık şık permütasyonu doğrulandı).`);
  } else if (optionMatch.matchedCount === 1) {
    reasons.push(`1 ortak şık örtüşmesi var.`);
  }

  // 5. Tıbbi Varlık ve Terim Kesişimi
  const entitiesA = extractMedicalEntities(textA);
  const entitiesB = extractMedicalEntities(textB);
  const sharedMedicalEntities = entitiesA.filter((e) => entitiesB.includes(e));

  if (sharedMedicalEntities.length >= 2) {
    reasons.push(`Kritik tıbbi terimler ortak: ${sharedMedicalEntities.slice(0, 4).join(', ')}`);
  } else if (sharedMedicalEntities.length === 1) {
    reasons.push(`Ortak terim: ${sharedMedicalEntities[0]}`);
  }

  // 5b. KISA-METİN KORUMASI: iki taraf da bir-iki cümlelik ipucundan ibaretse,
  // şık örtüşmesi ya da aynı soru numarası yoksa kümelenme yapılmaz.
  const contentWords = (text: string) =>
    normalizeMedicalText(text).split(' ').filter((w) => w.length > 2 && !MEDICAL_STOP_WORDS.has(w)).length;
  const sameNumber =
    !draftA.isUnassignedNumber && !draftB.isUnassignedNumber &&
    Boolean(draftA.questionNumber) && draftA.questionNumber === draftB.questionNumber;
  if (
    contentWords(textA) < 8 && contentWords(textB) < 8 &&
    optionMatch.matchedCount < 2 && !sameNumber
  ) {
    return distinct('Her iki taslak da çok kısa ve ortak şık/soru numarası yok; güvenli eşleşme kurulamadı.');
  }

  // 6. Doğru Cevap Tahmini Uyumu
  const answerA = draftA.claimedAnswer || draftA.correctAnswer || draftA.reconstruction?.correctAnswer;
  const answerB = draftB.claimedAnswer || draftB.correctAnswer || draftB.reconstruction?.correctAnswer;
  let answerAgreementBonus = 0;

  if (answerA && answerB) {
    const optTextA = draftA.options?.find(o => o.key === answerA)?.text || answerA;
    const optTextB = draftB.options?.find(o => o.key === answerB)?.text || answerB;
    const optSim = calculateLevenshteinSimilarity(optTextA, optTextB);
    if (optSim >= 0.7) {
      answerAgreementBonus = 15;
      reasons.push(`Öğrencilerin doğru cevap tahminleri uyumlu ("${optTextA}").`);
    }
  }

  // 7. Soru Hedefi ve Çelişki Koruması
  const targetA = detectQuestionTarget(textA);
  const targetB = detectQuestionTarget(textB);

  let targetAlignment: 'matching' | 'different_aspect' | 'conflicting' = 'matching';
  let penalty = 0;

  if (targetA !== 'general' && targetB !== 'general' && targetA !== targetB) {
    if (sharedConcepts.length === 0) {
      targetAlignment = 'conflicting';
      penalty = 25;
      reasons.push(`DİKKAT: Biri "${targetA}" diğeri "${targetB}" soruyor olabilir.`);
    } else {
      targetAlignment = 'different_aspect';
      reasons.push(`Aynı konunun farklı yönleri hatırlanmış (Klinik & Tanı).`);
    }
  }

  // 8. Kitapçık ve Soru Numarası Notu
  let bookletNumberNote: string | undefined;
  if (!draftA.isUnassignedNumber && !draftB.isUnassignedNumber && draftA.questionNumber && draftB.questionNumber) {
    if (draftA.questionNumber === draftB.questionNumber) {
      reasons.push(`Aynı soru numarasına sahipler (#${draftA.questionNumber}).`);
    } else {
      bookletNumberNote = `Farklı kitapçık numaraları tespit edildi (Biri #${draftA.questionNumber}, diğeri #${draftB.questionNumber}).`;
      reasons.push(bookletNumberNote);
    }
  }

  // 9. Nihai Skor Harmanlama
  let overallScore = 0;

  if (sharedConcepts.length > 0) {
    // Kavram örtüşmesi tabanı verir; otomasyon için kök/şık/sayı kanıtı şarttır.
    // Aynı soru numarası, aynı kitapçık sorusuna işaret ettiği için ek destektir.
    overallScore = conceptBonus + Math.min(40,
      stemSimilarity * 0.35 +
      sharedMedicalEntities.length * 6 +
      (sameDiscipline ? 8 : 0) +
      (sameNumber ? 10 : 0));
    const weakEvidence =
      stemSimilarity < 20 && sharedMedicalEntities.length < 2 && optionMatch.matchedCount < 2 && !sameNumber;
    if (weakEvidence) {
      overallScore = Math.min(overallScore, t.autoThreshold - 4);
      reasons.push('Yalnızca kavram adı örtüşüyor; kök ve şık desteği zayıf olduğu için insan incelemesi gerekir.');
    }
  } else if (optionMatch.matchedCount >= 2) {
    // En az 2 ortak şık güçlü sinyaldir; ama kök tamamen farklıysa temkinli olunur.
    const optBase = (stemSimilarity >= 15 || sameNumber) ? 75 : 60;
    overallScore = optBase + Math.min(25, sharedMedicalEntities.length * 5 + stemSimilarity * 0.15);
  } else if (sharedMedicalEntities.length >= 2) {
    overallScore = 50 + Math.min(35, stemSimilarity * 0.35 + optionSetSimilarity * 0.25 + (sameDiscipline ? 10 : 0));
  } else {
    overallScore = (
      stemSimilarity * 0.45 +
      optionSetSimilarity * 0.35 +
      (sameDiscipline ? 15 : 0) +
      Math.min(20, sharedMedicalEntities.length * 8)
    );
  }

  overallScore += answerAgreementBonus;
  overallScore -= penalty;
  overallScore = Math.max(0, Math.min(100, Math.round(overallScore)));

  let recommendation: 'auto_merge' | 'suggest_merge' | 'distinct';
  if (overallScore >= t.autoThreshold && targetAlignment !== 'conflicting') {
    recommendation = 'auto_merge';
  } else if (overallScore >= t.suggestThreshold && targetAlignment !== 'conflicting') {
    recommendation = 'suggest_merge';
  } else {
    recommendation = 'distinct';
  }

  const primaryConcept = sharedConcepts[0]?.name || draftA.topic || draftB.topic || '';
  const contextHashtag = toContextHashtag(primaryConcept);

  return {
    score: overallScore,
    recommendation,
    reasons,
    stemSimilarity,
    optionSetSimilarity,
    sharedMedicalEntities,
    sharedConcepts: sharedConcepts.map((c) => c.name),
    contextHashtag,
    targetQuestionAlignment: targetAlignment,
    bookletNumberNote,
    matchedOptionAlignments: optionMatch.alignments
  };
}

// ==========================================
// 4. BİRLEŞTİRME VE İÇ İÇE GEÇİRME MOTORU
// ==========================================
export function mergeDrafts(
  anchorQuestion: QuestionItem,
  satelliteQuestions: QuestionItem[],
  performedBy: { name?: string; uid?: string; email?: string } = {}
): { consolidated: QuestionItem; mergedIds: string[] } {
  const mergedIds: string[] = satelliteQuestions.map((q) => q.id);
  const now = new Date().toISOString();

  const consolidatedFragments: MemoryFragment[] = [...(anchorQuestion.fragments || [])];
  const consolidatedOptions: QuestionOption[] = [...(anchorQuestion.options || [])];
  const consolidatedAlternativeOptions: AlternativeOption[] = [...(anchorQuestion.alternativeOptions || [])];

  for (const sat of satelliteQuestions) {
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

    if (sat.fragments && sat.fragments.length > 0) {
      for (const f of sat.fragments) {
        if (!consolidatedFragments.some((cf) => cf.id === f.id || cf.text.trim() === f.text.trim())) {
          consolidatedFragments.push(f);
        }
      }
    }

    if (sat.options && sat.options.length > 0) {
      for (const satOpt of sat.options) {
        if (!satOpt.text || !satOpt.text.trim()) continue;

        // Birebir veya yüksek benzerlik kontrolü (>= 0.65 benzerlikte eş kabul et ve oyları birleştir)
        const existingOpt = consolidatedOptions.find((ao) =>
          calculateLevenshteinSimilarity(ao.text, satOpt.text) >= 0.65
        );

        if (existingOpt) {
          existingOpt.upvotes = (existingOpt.upvotes || 1) + (satOpt.upvotes || 1);
        } else {
          const usedKeys = new Set(consolidatedOptions.map((o) => o.key));
          const availableKey = (['A', 'B', 'C', 'D', 'E'] as const).find((k) => !usedKeys.has(k));

          if (availableKey && consolidatedOptions.length < 5) {
            consolidatedOptions.push({
              key: availableKey,
              text: satOpt.text.trim(),
              suggestedBy: satOpt.suggestedBy || sat.contributedByName || 'Taslak Birleştirme',
              suggestedByUid: satOpt.suggestedByUid || sat.contributedByUid,
              upvotes: satOpt.upvotes || 1
            });
          } else {
            // 5'ten fazla şık varsa: Mevcut alternatif şıklarla benzerlik kontrolü yap
            const existingAlt = consolidatedAlternativeOptions.find((alt) =>
              calculateLevenshteinSimilarity(alt.text, satOpt.text) >= 0.65
            );
            if (existingAlt) {
              existingAlt.upvotes = (existingAlt.upvotes || 1) + (satOpt.upvotes || 1);
            } else {
              // Bambaşka farklı bir şık -> Alternatif Şık olarak kaydet
              consolidatedAlternativeOptions.push({
                id: `alt-opt-${Date.now()}-${Math.random().toString(36).substring(2, 7)}`,
                text: satOpt.text.trim(),
                sourceQuestionId: sat.id,
                suggestedBy: satOpt.suggestedBy || sat.contributedByName || 'Taslak Birleştirme',
                suggestedByUid: satOpt.suggestedByUid || sat.contributedByUid,
                upvotes: satOpt.upvotes || 1,
                reason: `Birleştirilen Soru #${sat.questionNumber || 'Taslak'} alternatifi`
              });
            }
          }
        }
      }
    }

    // Ayrıca uydunun mevcut alternatif şıkları varsa onları da konsolide et
    if (sat.alternativeOptions && sat.alternativeOptions.length > 0) {
      for (const satAlt of sat.alternativeOptions) {
        if (!satAlt.text || !satAlt.text.trim()) continue;
        const matchingInMain = consolidatedOptions.find((ao) =>
          calculateLevenshteinSimilarity(ao.text, satAlt.text) >= 0.65
        );
        if (matchingInMain) {
          matchingInMain.upvotes = (matchingInMain.upvotes || 1) + (satAlt.upvotes || 1);
          continue;
        }
        const matchingInAlt = consolidatedAlternativeOptions.find((ao) =>
          calculateLevenshteinSimilarity(ao.text, satAlt.text) >= 0.65
        );
        if (matchingInAlt) {
          matchingInAlt.upvotes = (matchingInAlt.upvotes || 1) + (satAlt.upvotes || 1);
        } else {
          consolidatedAlternativeOptions.push(satAlt);
        }
      }
    }
  }

  const allTags = new Set([
    ...(anchorQuestion.tags || []),
    ...satelliteQuestions.flatMap((q) => q.tags || []),
    'taslak-birlestirildi'
  ]);

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

  const consolidated: QuestionItem = {
    ...anchorQuestion,
    fragments: consolidatedFragments,
    options: consolidatedOptions.sort((a, b) => a.key.localeCompare(b.key)),
    alternativeOptions: consolidatedAlternativeOptions.length > 0 ? consolidatedAlternativeOptions : undefined,
    tags: Array.from(allTags),
    status: consolidatedOptions.length >= 4 && consolidatedFragments.length >= 2 ? 'gathering' : anchorQuestion.status,
    mergedSatellites: [
      ...(anchorQuestion.mergedSatellites || []),
      ...satelliteQuestions
    ],
    isMerged: true,
    revisions,
    updatedAt: now,
    placementNotes: [
      anchorQuestion.placementNotes || '',
      `[${new Date().toLocaleDateString('tr-TR')}]: ${satelliteQuestions.length} taslak ile iç içe geçirildi.`
    ].filter(Boolean).join(' ')
  };

  return { consolidated, mergedIds };
}

/**
 * Birleştirilmiş (iç içe geçmiş) taslağı geri alıp ana soru ve bağımsız
 * uydu taslaklara ayrıştırır.
 */
export function unmergeQuestion(
  consolidatedQuestion: QuestionItem
): {
  anchor: QuestionItem;
  restoredSatellites: QuestionItem[];
} {
  const now = new Date().toISOString();
  const restoredSatellites: QuestionItem[] = [];

  // 1. Varsa orijinal uydu taslak kopyalarını geri yükle
  if (consolidatedQuestion.mergedSatellites && consolidatedQuestion.mergedSatellites.length > 0) {
    for (const sat of consolidatedQuestion.mergedSatellites) {
      restoredSatellites.push({
        ...sat,
        id: sat.id || `restored-sat-${Date.now()}-${Math.random().toString(36).substring(2, 7)}`,
        status: sat.status || 'gathering',
        tags: (sat.tags || []).filter((t) => t !== 'taslak-birlestirildi'),
        updatedAt: now
      });
    }
  } else {
    // 2. Yedek: [Birleştirilen Taslak ...] etiketli parçalardan ayrıştır
    const mergedFrags = (consolidatedQuestion.fragments || []).filter((f) =>
      f.text.includes('[Birleştirilen Taslak')
    );

    for (let i = 0; i < mergedFrags.length; i++) {
      const mf = mergedFrags[i];
      const match = mf.text.match(/^\[Birleştirilen Taslak #([^\]]+)\]:\s*([\s\S]*)$/);
      const qNum = match ? parseInt(match[1], 10) : 0;
      const cleanStem = match ? match[2].trim() : mf.text.trim();

      restoredSatellites.push({
        id: `restored-sat-${Date.now()}-${i}-${Math.random().toString(36).substring(2, 6)}`,
        committeeId: consolidatedQuestion.committeeId,
        questionNumber: !isNaN(qNum) ? qNum : 0,
        discipline: consolidatedQuestion.discipline || 'Belirtilmedi',
        topic: consolidatedQuestion.topic || '',
        status: 'gathering',
        fragments: [
          {
            id: `f-restored-${Date.now()}-${i}`,
            author: mf.author || 'Taslak Yazarı',
            authorUid: mf.authorUid,
            authorStudentNumber: mf.authorStudentNumber,
            text: cleanStem,
            type: 'stem',
            timestamp: mf.timestamp || now,
            upvotes: mf.upvotes || 1
          }
        ],
        options: [],
        tags: [],
        createdAt: mf.timestamp || now,
        updatedAt: now
      });
    }
  }

  // 3. Çapa sorunun temizlenmesi (birleştirme parçaları ve etiketler çıkarılır)
  const cleanedFragments = (consolidatedQuestion.fragments || []).filter(
    (f) => !f.text.includes('[Birleştirilen Taslak')
  );

  const cleanedTags = (consolidatedQuestion.tags || []).filter(
    (t) => t !== 'taslak-birlestirildi'
  );

  const revisions: QuestionRevision[] = [
    ...(consolidatedQuestion.revisions || []),
    {
      id: `rev-unmerge-${Date.now()}`,
      version: (consolidatedQuestion.revisions?.length || 0) + 1,
      editedAt: now,
      editorName: 'Taslak Ayırma',
      changeSummary: `${restoredSatellites.length} adet birleştirilmiş taslak ayrıldı ve bağımsız taslak olarak geri yüklendi.`
    }
  ];

  const anchor: QuestionItem = {
    ...consolidatedQuestion,
    fragments: cleanedFragments,
    tags: cleanedTags,
    mergedSatellites: [],
    alternativeOptions: undefined,
    isMerged: false,
    revisions,
    updatedAt: now
  };

  return { anchor, restoredSatellites };
}

// ==========================================
// 5. BÜTÜNSEL KOMİTE KÜMELEME MOTORU
// ==========================================
export function clusterDraftsForCommittee(
  questions: QuestionItem[],
  committeeId: string,
  tuning?: ClusterTuning
): ClusterAnalysisSummary {
  const t = resolveTuning(tuning);
  if (!t.blocked) t.blocked = loadBlockedPairs();
  const commQuestions = questions.filter((q) => q.committeeId === committeeId);

  const scoredQuestions = commQuestions.map((q) => ({
    question: q,
    anchorScore: calculateDraftAnchorScore(q)
  }));

  // En detaylı ve puanı yüksek taslaklar başa gelir
  scoredQuestions.sort((a, b) => b.anchorScore.total - a.anchorScore.total);

  const assignedToCluster = new Set<string>();
  const clusters: DraftCluster[] = [];
  const unmatchedVagueDrafts: QuestionItem[] = [];

  for (let i = 0; i < scoredQuestions.length; i++) {
    const current = scoredQuestions[i];
    if (assignedToCluster.has(current.question.id)) continue;

    const satellites: Array<{ question: QuestionItem; compatibility: DraftCompatibilityResult }> = [];

    for (let j = 0; j < scoredQuestions.length; j++) {
      if (i === j) continue;
      const candidate = scoredQuestions[j];
      if (assignedToCluster.has(candidate.question.id)) continue;

      const comp = calculateDraftCompatibility(current.question, candidate.question, t);

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

      const detectedSubject = satellites[0].compatibility.sharedConcepts?.[0] || current.question.topic;

      // Çapa kalitesi düşükse küme ne kadar güvenli görünürse görünsün incelemeye düşer.
      const anchorWeak = current.anchorScore.total < t.anchorQualityThreshold;

      clusters.push({
        id: `cluster-${current.question.id}-${Date.now()}`,
        committeeId,
        anchorQuestion: current.question,
        satelliteDrafts: satellites,
        overallConfidence: avgConfidence,
        status: !anchorWeak && avgConfidence >= t.readyConfidence ? 'ready_to_merge' : 'needs_review',
        estimatedUniqueSlots: 1,
        detectedSubject
      });
    } else {
      if (current.anchorScore.classification === 'vague_fragment') {
        unmatchedVagueDrafts.push(current.question);
      }
    }
  }

  // Kalan sorular için kümelerle ikinci tur gevşek eşleştirme
  const remainingVague: QuestionItem[] = [];
  for (const vagueQ of unmatchedVagueDrafts) {
    if (assignedToCluster.has(vagueQ.id)) continue;

    let bestCluster: DraftCluster | null = null;
    let bestScore = 0;
    let bestComp: DraftCompatibilityResult | null = null;

    for (const cluster of clusters) {
      const comp = calculateDraftCompatibility(cluster.anchorQuestion, vagueQ, t);
      if (comp.score > bestScore && comp.score >= t.vagueAttachThreshold && comp.targetQuestionAlignment !== 'conflicting') {
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
// 6. ANLIK YAZARKEN BENZERLİK ARAMA
// ==========================================
export interface RealtimeMatchItem {
  question: QuestionItem;
  compatibility: DraftCompatibilityResult;
  contextHashtag?: string;
  isCrossCommittee?: boolean;
}

export function findRealtimeMatchingDrafts(
  input: {
    committeeId: string;
    discipline?: string;
    topic?: string;
    text: string;
    options?: Array<{ key: string; text: string }>;
  },
  existingQuestions: QuestionItem[],
  minScore = 35,
  limit = 5,
  includeCrossCommittee = true
): RealtimeMatchItem[] {
  if (!input.text || input.text.trim().length < 6) {
    return [];
  }

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

  const matches: RealtimeMatchItem[] = [];

  // 1. Önce o anki kurul soruları taranır
  const sameCommPool = existingQuestions.filter((q) => q.committeeId === input.committeeId);
  for (const q of sameCommPool) {
    const comp = calculateDraftCompatibility(q, tempQuestion);
    if (comp.score >= minScore && comp.targetQuestionAlignment !== 'conflicting') {
      const contextHashtag = comp.contextHashtag || toContextHashtag(q.topic || input.topic || '');
      matches.push({
        question: q,
        compatibility: comp,
        contextHashtag,
        isCrossCommittee: false
      });
    }
  }

  // 2. Çapraz kurul kontrolü: Eğer aynı kurulda güçlü eşleşme azsa diğer kurullardaki sorular da kontrol edilir
  if (includeCrossCommittee && matches.length < 3) {
    const otherPool = existingQuestions.filter((q) => q.committeeId !== input.committeeId);
    for (const q of otherPool) {
      // Çapraz kurulda eşleşme eşiği biraz daha yüksek tutulur (%50+)
      const comp = calculateDraftCompatibility(q, tempQuestion);
      if (comp.score >= Math.max(50, minScore + 10) && comp.targetQuestionAlignment !== 'conflicting') {
        const contextHashtag = comp.contextHashtag || toContextHashtag(q.topic || input.topic || '');
        matches.push({
          question: q,
          compatibility: comp,
          contextHashtag,
          isCrossCommittee: true
        });
      }
    }
  }

  // En belirgin benzer soru ilk başta (aynı kurul sorularına hafif öncelik)
  matches.sort((a, b) => {
    const scoreA = a.compatibility.score + (a.isCrossCommittee ? 0 : 5);
    const scoreB = b.compatibility.score + (b.isCrossCommittee ? 0 : 5);
    return scoreB - scoreA;
  });

  return matches.slice(0, limit);
}

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
  contextHashtag?: string;
  allMatches?: RealtimeMatchItem[];
} {
  const allMatches = findRealtimeMatchingDrafts(input, existingQuestions, 35, 6);
  if (allMatches.length > 0) {
    return {
      matchFound: true,
      matchedQuestion: allMatches[0].question,
      compatibility: allMatches[0].compatibility,
      contextHashtag: allMatches[0].contextHashtag,
      allMatches
    };
  }

  return { matchFound: false, allMatches: [] };
}

// ==========================================
// 7. GEMINI AI SEMANTİK DERİN EŞLEŞTİRİCİ
// ==========================================
/**
 * Karmaşık ve farklı kelimelerle ifade edilmiş öğrenci hatırlamalarını
 * Gemini 3.8 Flash ile derinlemesine karşılaştırır.
 */
export async function checkSemanticMatchWithAi(
  draftA: QuestionItem,
  draftB: QuestionItem
): Promise<{ isSameQuestion: boolean; confidence: number; explanation: string; commonSubject?: string }> {
  try {
    const apiKey = process.env.GEMINI_API_KEY || process.env.GEMINI_FREE_KEY_2 || process.env.GEMINI_BILLED_KEY;
    if (!apiKey) {
      return { isSameQuestion: false, confidence: 0, explanation: 'API key yok' };
    }

    const ai = new GoogleGenAI({ apiKey });

    const textA = [
      draftA.discipline ? `Ders: ${draftA.discipline}` : '',
      draftA.topic ? `Konu: ${draftA.topic}` : '',
      `Soru/İpuçları: ${draftA.fragments?.map(f => f.text).join(' ') || draftA.stem || ''}`,
      `Şıklar: ${(draftA.options || []).map(o => `${o.key}) ${o.text}`).join(', ')}`
    ].filter(Boolean).join('\n');

    const textB = [
      draftB.discipline ? `Ders: ${draftB.discipline}` : '',
      draftB.topic ? `Konu: ${draftB.topic}` : '',
      `Soru/İpuçları: ${draftB.fragments?.map(f => f.text).join(' ') || draftB.stem || ''}`,
      `Şıklar: ${(draftB.options || []).map(o => `${o.key}) ${o.text}`).join(', ')}`
    ].filter(Boolean).join('\n');

    const prompt = `Aşağıda aynı tıp fakültesi komite sınavından çıkan iki farklı öğrencinin hafızasından sisteme eklediği iki soru taslağı verilmiştir.
Öğrenciler aynı sorunun farklı kısımlarını (örn: biri fetal ultrason bulgularını, diğeri kromozom sayısını ve kalp bulgusunu, biri sadece şıkkı) hatırlamış olabilir.
Ayrıca farklı kitapçıklardan dolayı şık harfleri ve soru numaraları farklı olabilir.

TASLAK 1:
${textA}

TASLAK 2:
${textB}

GÖREV:
Bu iki taslağın AYNI tıp fakültesi kurul sorusuna ait olup olmadığını değerlendir.
Sadece geçerli bir JSON yanıtı döndür:
{
  "isSameQuestion": true | false,
  "confidence": 0-100,
  "commonSubject": "Hastalık/Konu adı (örn: Down Sendromu (Trizomi 21))",
  "explanation": "Neden aynı veya farklı olduğuna dair tek cümlelik tıp açıklaması"
}`;

    const response = await ai.models.generateContent({
      model: 'gemini-2.5-flash',
      contents: prompt,
      config: { responseMimeType: 'application/json' }
    });

    const parsed = JSON.parse(response.text || '{}');
    return {
      isSameQuestion: Boolean(parsed.isSameQuestion),
      confidence: Number(parsed.confidence) || 0,
      explanation: parsed.explanation || '',
      commonSubject: parsed.commonSubject
    };
  } catch (e: any) {
    return { isSameQuestion: false, confidence: 0, explanation: e.message || 'AI hatası' };
  }
}
