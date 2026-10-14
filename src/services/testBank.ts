/**
 * Test çöz soru bankası: uygulamanın çözülebilir (tek doğru cevaplı) tüm soru kaynakları tek modelde toplanır.
 *  - Çıkmış sorular (arşiv; studyStore.loadArchiveBank)
 *  - Kazanım temelli örnek sorular (ornek_sorular/k1)
 *  - Öğren destelerinin etkileşimli ögeleri: mini soru (micro_quiz), klinik karar (branching_logic),
 *    tuzak avı (spot_the_lie → "hangisi yanlıştır?")
 * Soru havuzundaki kullanıcı eklemeleri bilerek DIŞARIDA bırakılır (doğrulanmamış, kullanıcı kaynaklı veri).
 *
 * Örnek soru dosyaları ve desteler büyük olduğundan hepsi yüklenmez: ölçütlere uyan dosyalar karıştırılır ve
 * istenen soru sayısını karşılayacak kadarı (en çok MAX_FILES) okunur.
 */
import { loadArchiveBank } from './studyStore';
import { normalizeDonem3Discipline } from '../data/curriculumData';
import { DECK_CATALOG, loadDeck } from '../data/deckStore';
import { ORNEK_INDEX, loadOrnekQuestions, miniQuestionsFromDeck, type PdfQuestion } from '../components/pdf/pdfSources';
import { cleanWhy } from '../components/learn/lesson/LessonBlocks';

export type TestSource = 'cikmis' | 'ornek' | 'mini' | 'vaka' | 'tuzak';
export type Difficulty = 'kolay' | 'orta' | 'zor';

export const SOURCE_ORDER: TestSource[] = ['cikmis', 'ornek', 'mini', 'vaka', 'tuzak'];
export const SOURCE_INFO: Record<TestSource, { label: string; hint: string; kurul1Only: boolean }> = {
  cikmis: { label: 'Çıkmış', hint: 'Geçmiş sınav soruları', kurul1Only: false },
  ornek: { label: 'Örnek soru', hint: 'Kazanım temelli, zorluk seçilir', kurul1Only: true },
  mini: { label: 'Mini soru', hint: 'Öğren adımlarındaki sorular', kurul1Only: true },
  vaka: { label: 'Klinik karar', hint: 'Öğren vaka senaryoları', kurul1Only: true },
  tuzak: { label: 'Tuzak avı', hint: 'Hangisi yanlıştır?', kurul1Only: true },
};
/** Örnek sorular ve Öğren desteleri şimdilik yalnız Kurul 1'de */
export const KURUL1 = 'donem3-kurul1';

export interface TestOption {
  key: string;
  text: string;
  why?: string;
}
export interface TestQuestion {
  id: string;
  source: TestSource;
  committeeId: string;
  discipline: string;
  topic: string;
  year?: string;
  difficulty?: Difficulty;
  /** Kısa köken: "2024-2025 Kurul" · "Öğren · Üriner Obstrüksiyon" */
  origin: string;
  stem: string;
  options: TestOption[];
  answer: string;
  explanation: string;
}

export interface TestCriteria {
  sources: TestSource[];
  /** 'all' ya da kurul kimliği */
  committeeId: string;
  /** Boş: hepsi */
  disciplines: string[];
  /** Yalnız örnek sorulara uygulanır; boş: hepsi */
  difficulties: Difficulty[];
  count: number;
}

export const DEFAULT_CRITERIA: TestCriteria = { sources: [...SOURCE_ORDER], committeeId: 'all', disciplines: [], difficulties: [], count: 20 };

const MAX_FILES = 12;
/** Testte görsel gösterilmez: şekle/görsele dayanan sorular dışarıda kalır */
const NEEDS_IMAGE = /(?:şekil|görsel|resim|figür)\s*\d|(?:yukarıdaki|aşağıdaki|verilen) (?:şekil|görsel|resim|fotoğraf|mikrograf)|\bbu (?:görsel|resim|fotoğraf|mikrograf)/i;
const needsImage = (q: { stem: string; options: { text: string }[] }) => NEEDS_IMAGE.test(q.stem) || q.options.some((o) => /(şekil|görsel)\s*\d/i.test(o.text));
/** Bir deste/dosyadan kaynak başına en çok kaç soru (konu çeşitliliği) */
const perFileCap = (per: number) => Math.max(2, Math.ceil(per / 3));
const LETTERS = ['A', 'B', 'C', 'D', 'E'];
const s = (v: any) => String(v ?? '').trim();

/** Ders adı tek biçime: "Üroloji / Tıbbi Patoloji" → "Üroloji"; Dönem 3 müfredat adlarına eşlenir. */
export const disciplineName = (raw?: string) => {
  const first = s(raw).split(/\s*(?:\/|&|,)\s*/)[0] || s(raw);
  return normalizeDonem3Discipline(first) || first || 'Genel';
};

export function shuffle<T>(arr: T[]): T[] {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

/** Ölçüt yokken: bütün kaynaklardan, bütün kurullardan rastgele 20 soru */
export const randomCriteria = (): TestCriteria => ({ ...DEFAULT_CRITERIA, sources: [...SOURCE_ORDER] });

const usesKurul1 = (c: TestCriteria) => c.committeeId === 'all' || c.committeeId === KURUL1;
const discOk = (c: TestCriteria, d: string) => !c.disciplines.length || c.disciplines.includes(d);

/** Açıklamayı Test çöz'ün ayrıştırıcısına uygun başlıklarla kurar (【Doğru yanıt gerekçesi】 → "Neden X"). */
const composeExplanation = (options: TestOption[], answer: string, base?: string) => {
  if (base && /【[^】]+】/.test(base)) return base;
  const right = options.find((o) => o.key === answer)?.why;
  const wrong = options.filter((o) => o.key !== answer && o.why).map((o) => `${o.key}) ${o.why}`);
  const parts: string[] = [];
  if (right || base) parts.push(`【Doğru yanıt gerekçesi】 ${right || base}`);
  if (right && base && base !== right) parts.push(`【Mekanizma】 ${base}`);
  if (wrong.length) parts.push(`【Çeldiriciler】 ${wrong.join('\n')}`);
  return parts.join('\n');
};

const fromPdf = (q: PdfQuestion, source: TestSource, origin: string): TestQuestion | null => {
  if (needsImage(q)) return null;
  const options = q.options.filter((o) => o.text).slice(0, 5).map((o, i) => ({ key: LETTERS[i], text: o.text, why: o.why, _old: o.key }));
  const ans = options.find((o) => o._old === q.answer)?.key;
  if (!q.stem || options.length < 2 || !ans) return null;
  const opts = options.map(({ _old, ...o }) => o);
  return {
    id: `${source}:${q.id}`,
    source,
    committeeId: q.committeeId || KURUL1,
    discipline: disciplineName(q.discipline),
    topic: s(q.topic),
    difficulty: q.difficulty,
    origin,
    stem: q.stem,
    options: opts,
    answer: ans,
    explanation: composeExplanation(opts, ans, q.explanation),
  };
};

/** Tuzak avı: 3-4 önermeden tam biri yanlış → "Aşağıdakilerden hangisi yanlıştır?" */
function lieQuestionsFromDeck(deck: any): PdfQuestion[] {
  const out: PdfQuestion[] = [];
  (Array.isArray(deck?.slides) ? deck.slides : []).forEach((sl: any, idx: number) => {
    const els: any[] = Array.isArray(sl.interactiveElements) ? sl.interactiveElements : Array.isArray(sl.elements) ? sl.elements : [];
    els.filter((e) => e?.type === 'spot_the_lie').forEach((e, j) => {
      const items: any[] = (e.items || e.statements || []).filter((it: any) => s(it.text));
      if (items.length < 3 || items.length > 5 || items.filter((it) => it.isLie).length !== 1) return;
      const opts = shuffle(items).map((it, k) => ({ key: LETTERS[k], text: s(it.text), why: cleanWhy(it.explanation) || undefined, lie: !!it.isLie }));
      const topic = s(e.topic || e.title);
      if (NEEDS_IMAGE.test(topic)) return;
      out.push({
        id: `${deck.id}:${sl.slideNumber ?? idx + 1}:lie${j}`,
        source: 'mini',
        discipline: s(deck.discipline),
        topic: s(deck.shortTitle || deck.title),
        // Bazı ögelerde konu alanı zaten soru cümlesi ("…hangisi yanlıştır (tuzaktır)? Odak: …")
        stem: /hangisi/i.test(topic)
          ? topic.replace(/\s*\(tuzaktır\)/i, '')
          : `${topic ? `${topic.replace(/[.:]\s*$/, '')}: ` : ''}Aşağıdaki ifadelerden hangisi yanlıştır?`,
        options: opts.map(({ lie: _l, ...o }) => o),
        answer: opts.find((o) => o.lie)?.key,
        refs: [],
        badges: [],
      });
    });
  });
  return out;
}

/** Ölçütlere uyan aday dosya sayıları (kurulumdaki sayaçlar için; yükleme yapmaz). */
export function catalogCounts(c: Pick<TestCriteria, 'committeeId' | 'disciplines'>) {
  const k1 = c.committeeId === 'all' || c.committeeId === KURUL1;
  const crit = { ...DEFAULT_CRITERIA, ...c };
  const decks = k1 ? DECK_CATALOG.filter((d) => discOk(crit, disciplineName(d.discipline))) : [];
  const ornek = k1 ? ORNEK_INDEX.filter((r) => discOk(crit, disciplineName(r.ders))) : [];
  return { decks: decks.length, ornekFiles: ornek.length, ornekQuestions: ornek.reduce((n, r) => n + (r.soru_sayisi || 0), 0) };
}

/** Kurulumdaki ders listesi: çıkmış bankası + (Kurul 1 seçiliyse) deste ve örnek dersleri */
export function disciplineOptions(archive: TestQuestion[], committeeId: string): [string, number][] {
  const m = new Map<string, number>();
  archive.filter((q) => committeeId === 'all' || q.committeeId === committeeId).forEach((q) => m.set(q.discipline, (m.get(q.discipline) || 0) + 1));
  if (committeeId === 'all' || committeeId === KURUL1) {
    DECK_CATALOG.forEach((d) => m.set(disciplineName(d.discipline), (m.get(disciplineName(d.discipline)) || 0) + (d.questionCount || 0)));
    ORNEK_INDEX.forEach((r) => m.set(disciplineName(r.ders), (m.get(disciplineName(r.ders)) || 0) + (r.soru_sayisi || 0)));
  }
  return [...m.entries()].filter(([, n]) => n > 0).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], 'tr'));
}

let archiveCache: TestQuestion[] | null = null;
/** Çıkmış sorular test modelinde (önbellekli). Havuz soruları buraya hiç girmez. */
export async function loadArchiveTests(): Promise<TestQuestion[]> {
  if (archiveCache) return archiveCache;
  const list = await loadArchiveBank();
  archiveCache = list
    .filter((q) => q.source === 'arşiv')
    .map((q) => ({
      id: `cikmis:${q.id}`,
      source: 'cikmis' as const,
      committeeId: q.committeeId,
      discipline: disciplineName(q.discipline),
      topic: q.topic,
      year: q.year,
      origin: [q.year, q.number ? `${q.number}. soru` : ''].filter(Boolean).join(' · ') || 'Çıkmış',
      stem: q.stem,
      options: q.options.map((o) => ({ key: o.key, text: o.text })),
      answer: q.answer,
      explanation: q.explanation,
    }));
  return archiveCache;
}

/**
 * Ölçütlere göre test kurar. Soru sayısı seçili kaynaklara eşit paylaştırılır; bir kaynak payını
 * dolduramazsa kalan diğerlerinden tamamlanır. Sonuç karışık sıradadır.
 */
export async function buildTest(c: TestCriteria, onProgress?: (msg: string) => void): Promise<TestQuestion[]> {
  const sources = c.sources.length ? c.sources : [...SOURCE_ORDER];
  const pools: Partial<Record<TestSource, TestQuestion[]>> = {};
  const per = Math.max(1, Math.ceil(c.count / sources.length));

  if (sources.includes('cikmis')) {
    onProgress?.('Çıkmış sorular yükleniyor…');
    const all = await loadArchiveTests();
    pools.cikmis = all.filter((q) => (c.committeeId === 'all' || q.committeeId === c.committeeId) && discOk(c, q.discipline));
  }

  if (sources.includes('ornek') && usesKurul1(c)) {
    onProgress?.('Örnek sorular yükleniyor…');
    const files = shuffle(ORNEK_INDEX.filter((r) => discOk(c, disciplineName(r.ders))));
    const acc: TestQuestion[] = [];
    for (const r of files.slice(0, MAX_FILES)) {
      const qs = shuffle(await loadOrnekQuestions(r.id));
      let n = 0;
      for (const q of qs) {
        if (n >= perFileCap(per) * 2) break;
        if (c.difficulties.length && !(q.difficulty && c.difficulties.includes(q.difficulty))) continue;
        const t = fromPdf(q, 'ornek', `Örnek · ${r.konu}`);
        if (t) {
          acc.push(t);
          n++;
        }
      }
      if (acc.length >= per * 2) break;
    }
    pools.ornek = acc;
  }

  const deckSources = sources.filter((x): x is 'mini' | 'vaka' | 'tuzak' => x === 'mini' || x === 'vaka' || x === 'tuzak');
  if (deckSources.length && usesKurul1(c)) {
    onProgress?.('Öğren desteleri yükleniyor…');
    const decks = shuffle(DECK_CATALOG.filter((d) => discOk(c, disciplineName(d.discipline))));
    const acc: Record<'mini' | 'vaka' | 'tuzak', TestQuestion[]> = { mini: [], vaka: [], tuzak: [] };
    for (const entry of decks.slice(0, MAX_FILES)) {
      const deck = await loadDeck<any>(entry.id).catch(() => null);
      if (!deck) continue;
      const origin = `Öğren · ${s(entry.shortTitle || entry.title)}`;
      const got: Record<'mini' | 'vaka' | 'tuzak', number> = { mini: 0, vaka: 0, tuzak: 0 };
      const add = (q: PdfQuestion, src: 'mini' | 'vaka' | 'tuzak') => {
        if (!deckSources.includes(src) || got[src] >= perFileCap(per)) return;
        const t = fromPdf(q, src, origin);
        if (t) {
          acc[src].push(t);
          got[src]++;
        }
      };
      if (deckSources.includes('mini') || deckSources.includes('vaka')) {
        shuffle(miniQuestionsFromDeck(deck, deckSources.includes('vaka'))).forEach((q) => add(q, q.badges.some((b) => b.label === 'Klinik karar') ? 'vaka' : 'mini'));
      }
      if (deckSources.includes('tuzak')) shuffle(lieQuestionsFromDeck(deck)).forEach((q) => add(q, 'tuzak'));
      if (deckSources.every((x) => acc[x].length >= per * 2)) break;
    }
    deckSources.forEach((x) => (pools[x] = acc[x]));
  }

  // Paylaştır: her kaynaktan payı kadar, eksik kalırsa artanlardan doldur
  const shuffled = Object.fromEntries(Object.entries(pools).map(([k, v]) => [k, shuffle(v || [])])) as Record<TestSource, TestQuestion[]>;
  const picked: TestQuestion[] = [];
  const seen = new Set<string>();
  const take = (q: TestQuestion) => {
    const key = q.stem.slice(0, 120);
    if (seen.has(key)) return false;
    seen.add(key);
    picked.push(q);
    return true;
  };
  for (const src of sources) {
    let n = 0;
    for (const q of shuffled[src] || []) {
      if (n >= per || picked.length >= c.count) break;
      if (take(q)) n++;
    }
  }
  if (picked.length < c.count) {
    const rest = shuffle(sources.flatMap((src) => shuffled[src] || []));
    for (const q of rest) {
      if (picked.length >= c.count) break;
      take(q);
    }
  }
  return shuffle(picked).slice(0, c.count);
}
