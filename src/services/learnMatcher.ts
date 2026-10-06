import { loadAllDecks } from '../data/deckStore';
import { safeJsonFetch } from './api';
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

const STOP_KEYWORDS = new Set([
  'hastalik', 'hastaliklar', 'hastaliklari', 'hastaliklarinin',
  'nedir', 'nelerdir', 'hangisi', 'yanlistir', 'dogrudur',
  'klinik', 'tedavi', 'tedavisi', 'bulgular', 'ozellikler',
  'belirtiler', 'primer', 'sekonder', 'yonetim', 'uygulama',
  'degildir', 'nedenle', 'birlikte', 'olarak', 'iliski', 'iliskili',
  'asagidakilerden', 'ifadelerden', 'durumlardan', 'tanisi', 'tipleri'
]);

function isDisciplineCompatible(qDisc: string, deckDisc: string): boolean {
  if (!qDisc || !deckDisc) return false;
  const q = normalizeTr(qDisc);
  const d = normalizeTr(deckDisc);
  if (!q || !d) return false;
  if (q === d) return true;

  // Distinct medical branches that must NOT be confused with each other
  const distinctBranches = [
    ['patoloji'],
    ['farmakoloji'],
    ['dahiliye', 'ic hastaliklari', 'endokrinoloji', 'gastroenteroloji', 'nefroloji', 'hematoloji', 'romatoloji'],
    ['uroloji'],
    ['genetik'],
    ['halk sagligi', 'toplum hekimligi'],
    ['mikrobiyoloji', 'enfeksiyon'],
    ['kardiyoloji'],
    ['kadin hastaliklari', 'dogum', 'obstetrik', 'jinekoloji'],
    ['cocuk', 'pediatri'],
    ['noroloji'],
    ['psikiyatri', 'ruh sagligi'],
    ['biyokimya'],
    ['fizyoloji'],
    ['histoloji', 'embriyoloji'],
    ['anatomi'],
  ];

  let qBranchIdx = -1;
  let dBranchIdx = -1;

  for (let i = 0; i < distinctBranches.length; i++) {
    const list = distinctBranches[i];
    if (qBranchIdx === -1 && list.some(term => q.includes(term))) {
      qBranchIdx = i;
    }
    if (dBranchIdx === -1 && list.some(term => d.includes(term))) {
      dBranchIdx = i;
    }
  }

  if (qBranchIdx !== -1 && dBranchIdx !== -1) {
    return qBranchIdx === dBranchIdx;
  }

  return q.includes(d) || d.includes(q);
}

class LearnMatcherService {
  private directIdMap = new Map<string, QuestionLearnMatch>();
  private directStemMap = new Map<string, QuestionLearnMatch>();
  private slideByKey = new Map<string, QuestionLearnMatch>();
  private slideIndex: Array<QuestionLearnMatch & { keywords: string[]; normDiscipline: string; rawDiscipline: string }> = [];
  private cache = new Map<string, QuestionLearnMatch | null>();

  private loading: Promise<void> | null = null;
  /** Sunucuda önceden hesaplanan bağlantılar (scripts/advanced_ai/learn_links.py: BM25+e5+cross-encoder, eşikli). */
  private computed: Map<string, { deckId: string; slideNumber: number }> | null = null;

  /**
   * Slayt indeksini arka planda kurar (desteler parça parça yüklenir). Hazır olana kadar
   * getMatch null döner; çağıran taraf promise çözülünce yeniden çizer.
   */
  public ensureLoaded(): Promise<void> {
    if (!this.loading) {
      const links = safeJsonFetch<{ baglantilar: Record<string, { deckId: string; slideNumber: number }> }>('/api/learn-links')
        .then((r) => {
          if (r.ok && r.data?.baglantilar) this.computed = new Map(Object.entries(r.data.baglantilar));
        })
        .catch(() => {});
      this.loading = Promise.all([loadAllDecks<any>(), links]).then(([decks]) => {
        this.init(decks);
        this.cache.clear();
      });
    }
    return this.loading;
  }

  private init(decks: any[]) {

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

        this.slideByKey.set(`${d.id}#${Number(s.slideNumber || 1)}`, slideMatchBase as QuestionLearnMatch);

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
        const pearlsText = (s.spotPearls || [])
          .map((p: any) => typeof p === 'string' ? p : `${p?.badge || ''} ${p?.text || ''}`)
          .join(' ');
        const fullSlideText = normalizeTr(
          `${d.title} ${deckDiscipline} ${s.title} ${s.badge} ${pearlsText} ${s.synthesisNarrative || ''}`
        );
        const words = Array.from(new Set(fullSlideText.match(/[a-z]{5,}/g) || []))
          .filter(w => !STOP_KEYWORDS.has(w));

        this.slideIndex.push({
          ...slideMatchBase,
          keywords: words,
          normDiscipline: normalizeTr(deckDiscipline),
          rawDiscipline: deckDiscipline
        });
      }
    }
  }

  public getMatch(q: QuestionItem): QuestionLearnMatch | null {
    if (!q || !q.id) return null;
    if (this.cache.has(q.id)) {
      return this.cache.get(q.id)!;
    }

    // 0. Önceden hesaplanmış bağlantı (güvenilir). Harita yüklendiyse ve bu soru için bağlantı yoksa
    //    tahmin edilmez: yanlış slayta göndermek yerine "Öğren" gösterilmez.
    if (this.computed) {
      const c = this.computed.get(String(q.id));
      const hit = c ? this.slideByKey.get(`${c.deckId}#${c.slideNumber}`) : undefined;
      if (hit) {
        const res = { ...hit, matchType: 'computed' as any, matchScore: 90 };
        this.cache.set(q.id, res);
        return res;
      }
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

    // 3. Anahtar kelime tahmini: genel kelimesi bol giriş/özet slaytlarına yanlış yönlendiriyordu (denetim 2026-10-06).
    //    Sunucu bağlantıları yüklendiyse kullanılmaz; yalnızca sunucuya erişilemezse son çare.
    if (this.computed) {
      this.cache.set(q.id, null);
      return null;
    }
    const qDiscipline = q.discipline || '';
    if (!qDiscipline) {
      this.cache.set(q.id, null);
      return null;
    }

    const stemNorm = normalizeTr(stem);
    const topicNorm = normalizeTr(q.topic || '');
    const qText = `${topicNorm} ${normalizeTr(qDiscipline)} ${stemNorm}`;

    let bestMatch: QuestionLearnMatch | null = null;
    let highestScore = 0;

    for (const item of this.slideIndex) {
      // Must strictly be discipline compatible
      if (!isDisciplineCompatible(qDiscipline, item.rawDiscipline)) {
        continue;
      }

      let score = 5;
      let matchedWordCount = 0;

      for (const kw of item.keywords) {
        if (kw.length >= 6 && qText.includes(kw)) {
          // Extra weight if keyword is explicitly in question topic or question stem
          if (topicNorm.includes(kw)) {
            score += 5;
          } else {
            score += 3;
          }
          matchedWordCount++;
        }
      }

      // High confidence threshold: at least 3 distinct significant medical keywords and minimum score 16
      if (matchedWordCount >= 3 && score >= 16 && score > highestScore) {
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
