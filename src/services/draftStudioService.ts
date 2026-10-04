/**
 * Taslak stüdyosu: öğrencilerin eklediği dağınık parçaları (kök, şık, ipucu, cevap)
 * elle soru adaylarına toplamak için istemci tarafı model.
 *
 * Hiyerarşi:  Ders › Konu (iç içe gruplar) › Soru adayı › Parçalar
 * Durum cihazda (localStorage, kurul başına) tutulur; "Soruya dönüştür" sunucuya yazar.
 */
import type { MemoryFragment, QuestionItem, QuestionOption } from '../types';

export type FragKind = MemoryFragment['type'];
export type OptKey = 'A' | 'B' | 'C' | 'D' | 'E';
export const OPT_KEYS: OptKey[] = ['A', 'B', 'C', 'D', 'E'];

export const KIND_LABEL: Record<FragKind, string> = { stem: 'Kök', option: 'Şık', clue: 'İpucu', answer: 'Cevap' };

/** Bir taslaktan çıkan tek parça. id = `${draftId}::${fragmentId}` */
export interface StudioFragment {
  id: string;
  draftId: string;
  kind: FragKind;
  text: string;
  author: string;
  timestamp: string;
  discipline: string;
  topic: string;
  questionNumber?: number;
  terms: string[];
}

export interface StudioGroup {
  id: string;
  label: string;
  discipline: string;
  parentId: string | null;
  collapsed?: boolean;
}

export interface StudioCandidate {
  id: string;
  groupId: string | null;
  title: string;
  stem: string;
  options: Record<OptKey, string>;
  answer?: OptKey;
  fragmentIds: string[];
  /** Hangi şık hangi parçadan geldi */
  optionSources: Partial<Record<OptKey, string>>;
  terms: string[];
  notes: string;
  status: 'open' | 'ready' | 'done';
  questionNumber?: number;
  convertedQuestionId?: string;
  updatedAt: string;
}

export interface StudioState {
  v: 1;
  groups: StudioGroup[];
  candidates: StudioCandidate[];
  /** Eş anlamlı terim grupları: kanonik terim → diğerleri */
  synonyms: Record<string, string[]>;
  /** Akış görünümünde elle taşınan düğüm konumları */
  positions: Record<string, { x: number; y: number }>;
  hiddenFragmentIds: string[];
}

export const emptyState = (): StudioState => ({ v: 1, groups: [], candidates: [], synonyms: {}, positions: {}, hiddenFragmentIds: [] });

const key = (committeeId: string) => `medsoru_draft_studio_${committeeId || 'genel'}`;

export function loadStudio(committeeId: string): StudioState {
  try {
    const raw = localStorage.getItem(key(committeeId));
    if (!raw) return emptyState();
    const s = JSON.parse(raw);
    return s && s.v === 1 ? { ...emptyState(), ...s } : emptyState();
  } catch {
    return emptyState();
  }
}

export function saveStudio(committeeId: string, s: StudioState) {
  try {
    localStorage.setItem(key(committeeId), JSON.stringify(s));
  } catch {
    /* kota dolu: sessizce geç */
  }
}

export const uid = (p: string) => `${p}_${Date.now().toString(36)}${Math.random().toString(36).slice(2, 6)}`;

// ---------------------------------------------------------------------------
// Terimler: Türkçe katlama + durak kelimeler + 5 harflik kök (arama motoruyla aynı mantık)
// ---------------------------------------------------------------------------
const TR_FOLD: Record<string, string> = { ı: 'i', ç: 'c', ğ: 'g', ö: 'o', ş: 's', ü: 'u', â: 'a', î: 'i', û: 'u' };
export const fold = (t: string) => t.toLocaleLowerCase('tr').replace(/[ıçğöşüâîû]/g, (c) => TR_FOLD[c] || c);

const STOP = new Set(
  [
    've', 'ile', 'veya', 'için', 'gibi', 'kadar', 'daha', 'olan', 'olarak', 'bir', 'bu', 'şu', 'her', 'tüm', 'en', 'de', 'da', 'ki', 'mi',
    'hangisidir', 'aşağıdakilerden', 'hangisi', 'nedir', 'aşağıdaki', 'vardı', 'vardır', 'yoktur', 'doğrudur', 'yanlıştır', 'göre',
    'ilgili', 'soru', 'sorusu', 'sordu', 'soruldu', 'çıktı', 'çıkmış', 'sınav', 'sınavda', 'galiba', 'sanırım', 'hatırlıyorum',
    'şık', 'şıkkı', 'şıklar', 'cevap', 'cevabı', 'hasta', 'hastada', 'olgu', 'yaşında', 'kadın', 'erkek', 'tanı', 'olası', 'muhtemel',
    'ilk', 'sonra', 'önce', 'neden', 'nasıl', 'ama', 'fakat', 'çok', 'az', 'var', 'yok', 'oldu', 'olur', 'şey',
    'diye', 'idi', 'gibiydi', 'soruda', 'sorunda', 'soruyordu', 'sorusunda', 'hatırlamıyorum', 'bilmiyorum', 'acaba',
  ].map(fold)
);

/** Karşılaştırma anahtarı: katlanmış 5 harflik kök (görüntü biçimi korunur). */
export const stemOf = (w: string) => {
  const f = fold(w);
  return f.length > 5 ? f.slice(0, 5) : f;
};

export function extractTerms(text: string): string[] {
  const out = new Set<string>();
  // Görüntüde Türkçe yazım korunur; durak kelime ve karşılaştırma katlanmış biçimle yapılır
  for (const raw of text.toLocaleLowerCase('tr').replace(/[^a-z0-9çğıöşüâîû\s-]/g, ' ').split(/\s+/)) {
    const w = raw.replace(/^-+|-+$/g, '');
    if (w.length < 4 || STOP.has(fold(w)) || /^\d+$/.test(w)) continue;
    out.add(w);
  }
  return [...out];
}

/** Bir terimin kanonik halini döndürür (eş anlamlı gruplara göre). */
export function canonical(term: string, synonyms: StudioState['synonyms']): string {
  for (const [head, rest] of Object.entries(synonyms)) if (head === term || rest.includes(term)) return head;
  return term;
}

/** Aynı köke sahip terimleri otomatik eş anlamlı öneri olarak gruplar (böbrek/böbreğin…). */
export function suggestSynonyms(terms: string[], synonyms: StudioState['synonyms']): string[][] {
  const by: Record<string, string[]> = {};
  for (const t of terms) {
    const c = canonical(t, synonyms);
    if (c !== t) continue;
    (by[stemOf(t)] ||= []).push(t);
  }
  return Object.values(by).filter((g) => g.length > 1);
}

// ---------------------------------------------------------------------------
// Parçalar
// ---------------------------------------------------------------------------
export function fragmentsFromDrafts(drafts: QuestionItem[]): StudioFragment[] {
  const out: StudioFragment[] = [];
  for (const q of drafts) {
    const frs = q.fragments || [];
    frs.forEach((f, i) => {
      if (!f?.text?.trim()) return;
      out.push({
        id: `${q.id}::${f.id || i}`,
        draftId: q.id,
        kind: f.type || 'stem',
        text: f.text.trim(),
        author: f.author || q.contributedByName || 'Anonim',
        timestamp: f.timestamp || '',
        discipline: q.discipline || 'Belirsiz',
        topic: q.topic || '',
        questionNumber: q.isUnassignedNumber ? undefined : q.questionNumber || undefined,
        terms: extractTerms(f.text),
      });
    });
    // Ayrı kaydedilmiş şıklar da parça olarak gelir
    (q.options || []).forEach((o: QuestionOption) => {
      if (!o?.text?.trim()) return;
      out.push({
        id: `${q.id}::opt-${o.key}`,
        draftId: q.id,
        kind: 'option',
        text: `${o.key}) ${o.text.trim()}`,
        author: o.suggestedBy || q.contributedByName || 'Anonim',
        timestamp: '',
        discipline: q.discipline || 'Belirsiz',
        topic: q.topic || '',
        questionNumber: q.isUnassignedNumber ? undefined : q.questionNumber || undefined,
        terms: extractTerms(o.text),
      });
    });
  }
  return out;
}

/** Kök bazlı Jaccard benzerliği (0–1). */
export function similarity(a: string[], b: string[], synonyms: StudioState['synonyms']): number {
  if (!a.length || !b.length) return 0;
  const A = new Set(a.map((t) => stemOf(canonical(t, synonyms))));
  const B = new Set(b.map((t) => stemOf(canonical(t, synonyms))));
  let inter = 0;
  A.forEach((x) => B.has(x) && inter++);
  return inter / (A.size + B.size - inter);
}

/**
 * Atanmamış parçaları benzerliğe göre kümeleyip aday önerir.
 * Aynı soru numarası ya da eşik üstü benzerlik → aynı küme.
 */
export function autoCluster(frs: StudioFragment[], synonyms: StudioState['synonyms'], threshold = 0.22): StudioFragment[][] {
  const parent = frs.map((_, i) => i);
  const find = (i: number): number => (parent[i] === i ? i : (parent[i] = find(parent[i])));
  const join = (a: number, b: number) => {
    parent[find(a)] = find(b);
  };
  for (let i = 0; i < frs.length; i++)
    for (let j = i + 1; j < frs.length; j++) {
      const a = frs[i], b = frs[j];
      if (a.discipline !== b.discipline && a.discipline !== 'Belirsiz' && b.discipline !== 'Belirsiz') continue;
      if ((a.questionNumber && a.questionNumber === b.questionNumber) || similarity(a.terms, b.terms, synonyms) >= threshold) join(i, j);
    }
  const groups: Record<number, StudioFragment[]> = {};
  frs.forEach((f, i) => (groups[find(i)] ||= []).push(f));
  return Object.values(groups).filter((g) => g.length > 1).sort((a, b) => b.length - a.length);
}

export function newCandidate(partial: Partial<StudioCandidate> = {}): StudioCandidate {
  return {
    id: uid('ad'),
    groupId: null,
    title: '',
    stem: '',
    options: { A: '', B: '', C: '', D: '', E: '' },
    fragmentIds: [],
    optionSources: {},
    terms: [],
    notes: '',
    status: 'open',
    updatedAt: new Date().toISOString(),
    ...partial,
  };
}

/** "A) metin" biçimindeki şık parçasından harf ve metni ayırır. */
export function parseOption(text: string): { key?: OptKey; text: string } {
  const m = text.match(/^\s*([A-Ea-e])\s*[)\].:-]\s*(.+)$/s);
  return m ? { key: m[1].toUpperCase() as OptKey, text: m[2].trim() } : { text: text.trim() };
}

/** Adayın sunucuya gönderilecek soru alanları. */
export function candidateToQuestionPatch(c: StudioCandidate, discipline: string, topic: string): Partial<QuestionItem> {
  const options: QuestionOption[] = OPT_KEYS.filter((k) => c.options[k].trim()).map((k) => ({ key: k, text: c.options[k].trim(), upvotes: 0 }));
  return {
    discipline,
    topic: topic || c.title || discipline,
    rawStem: c.stem.trim(),
    options,
    claimedAnswer: c.answer,
    tags: c.terms,
    placementNotes: c.notes || undefined,
    status: c.stem.trim() && options.length >= 4 && c.answer ? 'reconstructing' : 'gathering',
    ...(c.questionNumber ? { questionNumber: c.questionNumber, isUnassignedNumber: false } : {}),
  };
}
