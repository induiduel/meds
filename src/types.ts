export interface MemoryFragment {
  id: string;
  author: string;
  authorUid?: string;
  authorStudentNumber?: string;
  text: string;
  type: 'stem' | 'option' | 'clue' | 'answer';
  timestamp: string;
  upvotes: number;
  likedBy?: string[];
}

export interface QuestionOption {
  key: 'A' | 'B' | 'C' | 'D' | 'E';
  text: string;
  suggestedBy?: string;
  suggestedByUid?: string;
  isAiGenerated?: boolean;
  upvotes: number;
  likedBy?: string[];
}

export interface ReconstructedQuestion {
  stem: string;
  options: { key: 'A' | 'B' | 'C' | 'D' | 'E'; text: string; isAiFilled?: boolean; isCorrect?: boolean }[];
  correctAnswer: 'A' | 'B' | 'C' | 'D' | 'E';
  explanation: string;
  confidenceScore: number; // 0 - 100
  notesAndDiscrepancies?: string;
  lastUpdated: string;
  evidenceText?: string;
  reconstructionQuality?: string;
  qualityScore?: number;
  isAiRefined?: boolean;
  /** Course material / past questions the AI based this reconstruction on. */
  sources?: SourceRef[];
}

export interface SourceRef {
  documentId: string;
  documentType: 'past_question' | 'lecture_slide' | 'summary' | 'transcript' | string;
  title: string;
  discipline?: string;
  pageNumber?: number;
  snippet: string;
}

export interface QuestionRevision {
  id: string;
  version: number;
  editedAt: string;
  editorName: string;
  editorUid?: string;
  editorStudentNumber?: string;
  changeSummary?: string;
  stem?: string;
  discipline?: string;
  topic?: string;
  claimedAnswer?: 'A' | 'B' | 'C' | 'D' | 'E';
  options?: QuestionOption[];
  explanation?: string;
}

export interface QuestionLectureMatch {
  noteId: string;
  noteTitle: string;
  discipline: string;
  pageNumber: number;
  matchedSnippet: string;
  confidenceScore: number;
  reasoning: string;
  driveFileId?: string;
  driveFileUrl?: string;
  highlightedText?: string;
  matchedTerms?: string[];
  totalSlides?: number;
}

export interface LectureNotePage {
  pageNumber: number;
  content: string;
  keywords: string[];
}

export interface LectureNote {
  id: string;
  committeeId: string;
  discipline: string;
  title: string;
  instructor?: string;
  totalSlides: number;
  pages: LectureNotePage[];
  uploadedBy?: string;
  uploadedAt: string;
  driveFileId?: string;
  driveFileUrl?: string;
  pageCount?: number;
  renderedAt?: string;
}

export interface UserLeaderboardEntry {
  uid: string;
  rumuz: string;
  studentNumber?: string;
  totalPoints: number;
  questionsCount: number;
  optionsCount: number;
  upvotesReceived: number;
  rank: number;
}

export interface QuestionItem {
  id: string;
  committeeId: string;
  questionNumber: number;
  discipline: string;
  topic: string;
  status: 'empty' | 'gathering' | 'reconstructing' | 'completed';
  fragments: MemoryFragment[];
  options: QuestionOption[];
  claimedAnswer?: 'A' | 'B' | 'C' | 'D' | 'E';
  reconstruction?: ReconstructedQuestion;
  tags: string[];
  examYear?: string;
  term?: string;
  instructor?: string;
  rawStem?: string;
  isPastExam?: boolean;
  isUnassignedNumber?: boolean;
  suggestedQuestionNumber?: number;
  placementNotes?: string;
  contributedByUid?: string;
  contributedByName?: string;
  contributedByStudentNumber?: string;
  revisions?: QuestionRevision[];
  lectureReference?: QuestionLectureMatch;
  upvotes?: number;
  likedBy?: string[];
  sourceFile?: string;
  sourceNote?: string;
  correctAnswer?: 'A' | 'B' | 'C' | 'D' | 'E';
  isAmbiguous?: boolean;
  comments?: Array<{ id?: string; author: string; text: string; createdAt?: string }>;
  reports?: Array<{ id?: string; reason: string; details?: string; reportedBy?: string; reportedAt?: string }>;
  isLocked?: boolean;
  author?: string;
  mergedSatellites?: QuestionItem[];
  isMerged?: boolean;
  customRedactedBy?: string;
  customRedactedAt?: string;
  customRedactionPrompt?: string;
  matchedNoteTitle?: string | null;
  matchedSlidePage?: number | null;
  slideAudit?: {
    status: 'verified' | 'disconnected' | 'linked' | 'unmatched';
    auditedAt?: string;
    linkedAt?: string;
    reason?: string;
    score?: number;
    matchedTermsCount?: number;
    previousMatch?: {
      noteTitle?: string | null;
      pageNumber?: number | null;
    };
  };
  stem?: string;
  rawQuestion?: {
    stem?: string;
    options?: QuestionOption[] | string[];
    answer?: string;
    [key: string]: any;
  };
  explanation?: string;
  evidenceText?: string;
  lectureMatches?: any[];
  lectureRefs?: any[];
  deepseekEnriched?: boolean;
  verification?: {
    answerStatus?: string;
    evidenceStatus?: string;
    confidence?: number;
    curriculumFit?: string;
    status?: string;
    qualityScore?: number;
    changes?: string[];
    needsReview?: boolean;
    reviewReason?: string;
  };
  advancedQuestion?: any;
  hasAdvancedVersion?: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface UserProfile {
  uid: string;
  email: string | null;
  displayName: string | null;
  studentNumber?: string | null;
  congratsSentCommittees?: string[];
  createdAt?: string;
  updatedAt?: string;
}

export interface AdminNotification {
  id: string;
  type: 'unassigned_question' | 'new_fragment' | 'batch_cluster_ready';
  committeeId: string;
  questionId?: string;
  title: string;
  message: string;
  author: string;
  timestamp: string;
  isRead: boolean;
}

export interface Committee {
  id: string;
  name: string;
  year: number;
  term: string;
  targetCount: number;
  description: string;
  code?: string;
  examDate?: string;
  disciplines?: string[];
  academicYear?: string;
  targetQuestions?: number;
  color?: string;
}

export type {
  DraftAnchorScore,
  DraftCompatibilityResult,
  DraftCluster,
  ClusterAnalysisSummary,
  ClusterTuning,
  OptionAlignment
} from './services/draftClusteringService';
