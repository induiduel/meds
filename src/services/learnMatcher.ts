import interactiveDecksData from '../data/interactive_learning_decks.json';
import { QuestionItem } from '../types';
import { SlideFlashcard } from '../components/learn/InteractiveDeckView';

export interface QuestionLearnMatch {
  deckId: string;
  deckTitle: string;
  discipline: string;
  committee: string;
  slideNumber: number;
  slideTitle: string;
  badge: string;
  badgeColor?: string;
  synthesisNarrative?: string;
  spotPearls?: string[];
  flashcards?: SlideFlashcard[];
  matchType: 'direct' | 'stem' | 'keyword';
  matchScore: number;
}

function normalizeTr(str: string): string {
  if (!str) return '';
  return str.toLowerCase()
    .replace(/İ/g, 'i').replace(/I/g, 'ı').replace(/ı/g, 'i')
    .replace(/ğ/g, 'g').replace(/ü/g, 'u').replace(/ş/g, 's')
    .replace(/ö/g, 'o').replace(/ç/g, 'c');
}

class LearnMatcherService {
  private directIdMap = new Map<string, QuestionLearnMatch>();
  private directStemMap = new Map<string, QuestionLearnMatch>();
  private slideIndex: Array<QuestionLearnMatch & { keywords: string[]; normDiscipline: string }> = [];
  private cache = new Map<string, QuestionLearnMatch | null>();

  constructor() {
    this.init();
  }

  private init() {
    const decks = (interactiveDecksData as any[]) || [];

    for (const d of decks) {
      const deckTitle = d.shortTitle || d.title || 'Ders';
      const deckDiscipline = d.discipline || '';
      const deckCommittee = d.committee || '';

      for (const s of (d.slides || [])) {
        const slideMatchBase: QuestionLearnMatch = {
          deckId: d.id,
          deckTitle,
          discipline: deckDiscipline,
          committee: deckCommittee,
          slideNumber: s.slideNumber || 1,
          slideTitle: s.title || '',
          badge: s.badge || 'Ders Notu',
          badgeColor: s.badgeColor,
          synthesisNarrative: s.synthesisNarrative,
          spotPearls: s.spotPearls,
          flashcards: s.flashcards,
          matchType: 'direct',
          matchScore: 100
        };

        // 1. Direct question matches inside deck
        for (const rq of (s.relatedQuestions || [])) {
          if (rq.id) {
            this.directIdMap.set(rq.id, { ...slideMatchBase, matchType: 'direct', matchScore: rq.matchScore || 100 });
          }
          if (rq.stem && rq.stem.length > 20) {
            const key = normalizeTr(rq.stem.slice(0, 70)).replace(/[^a-z0-9]/g, '');
            if (key) {
              this.directStemMap.set(key, { ...slideMatchBase, matchType: 'stem', matchScore: 95 });
            }
          }
        }

        // 2. Keyword searchable index
        const fullSlideText = normalizeTr(
          `${d.title} ${d.discipline} ${s.title} ${s.badge} ${(s.spotPearls || []).join(' ')} ${s.synthesisNarrative || ''}`
        );
        const words = Array.from(new Set(fullSlideText.match(/[a-z]{5,}/g) || []));

        this.slideIndex.push({
          ...slideMatchBase,
          keywords: words,
          normDiscipline: normalizeTr(deckDiscipline)
        });
      }
    }
  }

  public getMatch(q: QuestionItem): QuestionLearnMatch | null {
    if (!q || !q.id) return null;
    if (this.cache.has(q.id)) {
      return this.cache.get(q.id)!;
    }

    // 1. Exact ID match
    if (this.directIdMap.has(q.id)) {
      const match = this.directIdMap.get(q.id)!;
      this.cache.set(q.id, match);
      return match;
    }

    // 2. Stem match
    const stem = q.stem || q.reconstruction?.stem || q.rawQuestion?.stem || '';
    if (stem.length > 20) {
      const stemKey = normalizeTr(stem.slice(0, 70)).replace(/[^a-z0-9]/g, '');
      if (stemKey && this.directStemMap.has(stemKey)) {
        const match = this.directStemMap.get(stemKey)!;
        this.cache.set(q.id, match);
        return match;
      }
    }

    // 3. Keyword / Topic match with strict discipline & multi-keyword requirement
    const qDiscipline = normalizeTr(q.discipline || '');
    const qText = normalizeTr(
      `${q.topic || ''} ${q.discipline || ''} ${stem} ${q.reconstruction?.stem || ''}`
    );

    let bestMatch: QuestionLearnMatch | null = null;
    let highestScore = 0;

    for (const item of this.slideIndex) {
      // Must match discipline
      const isDisciplineMatch = qDiscipline && (
        item.normDiscipline.includes(qDiscipline) ||
        qDiscipline.includes(item.normDiscipline)
      );
      if (!isDisciplineMatch) continue;

      let score = 5;
      let matchedWordCount = 0;

      for (const kw of item.keywords) {
        if (kw.length >= 6 && qText.includes(kw)) {
          score += 3;
          matchedWordCount++;
        }
      }

      // High confidence threshold: at least 3 distinct significant medical keywords
      if (matchedWordCount >= 3 && score >= 14 && score > highestScore) {
        highestScore = score;
        bestMatch = {
          ...item,
          matchType: 'keyword',
          matchScore: Math.min(95, Math.round((score / 25) * 100))
        };
      }
    }

    this.cache.set(q.id, bestMatch);
    return bestMatch;
  }
}

export const learnMatcher = new LearnMatcherService();
