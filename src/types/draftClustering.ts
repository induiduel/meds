import { QuestionItem, QuestionOption } from '../types';

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
