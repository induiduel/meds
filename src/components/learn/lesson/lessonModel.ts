/**
 * Öğren ders ekranının veri katmanı: farklı deste biçimlerini (k1p-, learn-, deck-) tek bir
 * adım modeline çevirir, bölümleri çıkarır, kazanımları slayta eşler ve tamamlanan adımları saklar.
 */
import type { InteractiveDeck, SlideItem } from '../InteractiveDeckView';

export interface LessonQuestion {
  id: string;
  stem: string;
  options: { key: string; text: string; explanation?: string }[];
  answer: string;
  explanation?: string;
  examYear?: string;
  practice: boolean;
}

export interface LessonCard { id: string; front: string; back: string; hint?: string; category?: string }

export type PracticeItem =
  | { kind: 'ix'; data: any }
  | { kind: 'cards'; cards: LessonCard[] }
  | { kind: 'question'; q: LessonQuestion };

export interface LessonStep {
  index: number;
  slide: SlideItem;
  number: number;
  title: string;
  /** "Konu: alt başlık" biçimindeki başlığın konu kısmı */
  topic: string;
  subtopic: string;
  checkpoint: number;
  badge?: string;
  narrative: string;
  bullets: { title: string; desc: string; isKey?: boolean }[];
  table?: { title?: string; headers: string[]; rows: string[][] };
  formula?: { title: string; formula: string; explanation?: string };
  infographic?: { type: string; items: { label: string; value: string; detail?: string; color?: string }[] };
  spots: string[];
  terms: { term: string; explanation: string }[];
  questions: LessonQuestion[];
  cards: LessonCard[];
  interactives: any[];
  teacher?: { quote?: string; note?: string; kind?: string };
  important?: string;
  examTip?: string;
  section: number;
}

export interface LessonSection { index: number; name: string; steps: number[] }

const CP_RE = /^\[TEKRAR SAYFASI\s*-\s*CHECKPOINT\s*(\d+)\]\s*/i;

const splitTitle = (t: string): [string, string] => {
  const i = t.indexOf(':');
  return i > 3 && i < 80 ? [t.slice(0, i).trim(), t.slice(i + 1).trim()] : [t, ''];
};

const OPT_RE = /^\s*([A-Ea-e])[).:-]\s*/;
const normQuestion = (q: any, i: number, practiceDefault = false): LessonQuestion | null => {
  if (!q || typeof q !== 'object') return null;
  const stem = String(q.stem || q.question || '').trim();
  if (stem.length < 10 || !Array.isArray(q.options) || q.options.length < 2) return null;
  const options = q.options.map((o: any, k: number) => {
    if (typeof o === 'string') {
      const m = o.match(OPT_RE);
      return { key: m ? m[1].toUpperCase() : String.fromCharCode(65 + k), text: m ? o.slice(m[0].length) : o };
    }
    return { key: String(o.key || String.fromCharCode(65 + k)).toUpperCase(), text: String(o.text ?? ''), explanation: o.explanation };
  });
  // Doğru şık: önce şıklardaki işaret, sonra harf (answer/correctAnswer), en son sıra numarası (0 tabanlı)
  const flagged = q.options.findIndex((o: any) => o && typeof o === 'object' && o.isCorrect);
  const letterOf = (v: any) => {
    const t = String(v ?? '').trim();
    const m = t.match(OPT_RE) || t.match(/^([A-Ea-e])$/);
    return m ? m[1].toUpperCase() : options.find((o: any) => t && o.text === t)?.key || '';
  };
  let answer = flagged >= 0 ? options[flagged].key : letterOf(q.answer) || letterOf(q.correctAnswer);
  if (!answer && /^\d+$/.test(String(q.correctAnswer ?? '').trim())) answer = options[Number(q.correctAnswer)]?.key || '';
  const examYear = q.examYear ? String(q.examYear) : undefined;
  const practice = Boolean(q.isPracticeQuestion) || practiceDefault || /Çalışma|Özgün|Pekiştirme/i.test(examYear || '');
  return { id: String(q.id || `q-${i}`), stem, options, answer, explanation: q.explanation, examYear, practice };
};

const normCard = (c: any, i: number): LessonCard | null => {
  const front = String(c?.front || c?.question || '').trim();
  const back = String(c?.back || c?.answer || '').trim();
  return front && back ? { id: String(c.id || `c-${i}`), front, back, hint: c.hint, category: c.category } : null;
};


/**
 * Deste üreticisi bazı mekanizma zinciri basamaklarını 60 karakterde "…" ile kesmiş. Kesilen metnin
 * tamamı aynı slaytta (alt başlık, başlık, anahtar madde, anlatım satırı) durur; oradan tamamlanır.
 */
const TRUNC_RE = /\s*(\.\.\.|…)\s*$/;
const slideCandidates = (s: any): string[] => {
  const cc = s.coreContent && !Array.isArray(s.coreContent) ? s.coreContent : {};
  return [
    s.subtitle,
    s.title,
    ...(cc.keyBullets || []).flatMap((b: any) => [b?.desc, b?.title]),
    ...String(s.synthesisNarrative || s.content || '').split(/\n+|(?<=[.!?])\s+/),
  ]
    .map((x) => String(x || '').replace(/[*=#>]+/g, '').replace(/^\s*[-•]\s*/, '').trim())
    .filter((x) => x.length > 8);
};
export const repairTruncated = (text: string, candidates: string[]): string => {
  if (!TRUNC_RE.test(text)) return text;
  const body = text.replace(TRUNC_RE, '');
  const k = body.indexOf(':');
  const [label, frag] = k > 0 && k < 48 ? [body.slice(0, k + 1) + ' ', body.slice(k + 1).trim()] : ['', body.trim()];
  const head = fold(frag);
  if (head.length < 8) return text;
  // Eşit uzunluk: metin aslında tamdı, üretici yalnızca "…" eklemiş
  const full = candidates.find((c) => fold(c).startsWith(head) && c.length >= frag.length);
  return full ? `${label}${full}` : text;
};
const repairInteractive = (e: any, s: any) => {
  if (e.type !== 'causal_chain' || !Array.isArray(e.steps) || !e.steps.some((x: any) => typeof x === 'string' && TRUNC_RE.test(x))) return e;
  const cands = slideCandidates(s);
  return { ...e, steps: e.steps.map((x: any) => (typeof x === 'string' ? repairTruncated(x, cands) : x)) };
};

export function buildSteps(deck: InteractiveDeck): LessonStep[] {
  const rawSlides = (Array.isArray(deck.slides) && deck.slides.length ? deck.slides : (Array.isArray((deck as any).steps) ? (deck as any).steps : [])) as any[];
  const deckQuestions = Array.isArray(deck.questions) ? deck.questions : [];
  const questionsBySlide = new Map<number, any[]>();
  if (deckQuestions.length > 0) {
    deckQuestions.forEach((q: any, qi: number) => {
      const target = Number(q.targetSlide || q.slideNumber || q.targetStep);
      const slideNum = (target && target >= 1 && target <= rawSlides.length) ? target : ((qi % Math.max(1, rawSlides.length)) + 1);
      if (!questionsBySlide.has(slideNum)) questionsBySlide.set(slideNum, []);
      questionsBySlide.get(slideNum)!.push(q);
    });
  }
  return rawSlides.map((slide, index) => {
    const s: any = slide;
    const cpMatch = String(slide.title || '').match(CP_RE);
    const title = cpMatch ? String(slide.title).slice(cpMatch[0].length) : String(slide.title || `Adım ${index + 1}`);
    const [topic, subtopic] = splitTitle(title);
    const cc = s.coreContent && !Array.isArray(s.coreContent) ? s.coreContent : {};
    const bullets = Array.isArray(cc.keyBullets) ? cc.keyBullets.filter((b: any) => b && (b.title || b.desc)) : [];
    const slideNum = slide.slideNumber ?? index + 1;
    // Kullanıcı talimatı: Etkileşimli öğrenim modülünde örnek soru ve çıkmış soru gösterimi kaldırıldı.
    const questions: LessonQuestion[] = [];
    const interactives = (
      Array.isArray(s.interactiveElements) && s.interactiveElements.length
        ? s.interactiveElements
        : Array.isArray(s.elements) && s.elements.length
          ? s.elements
          : s.interactiveElement
            ? [s.interactiveElement]
            : []
    )
      .filter((e: any) => e && typeof e === 'object' && e.type)
      .map((e: any) => repairInteractive(e, s));
    const hl = s.professorAudioHighlight;
    const narrativeText = String(s.synthesisNarrative || s.content || (cc && typeof cc.text === 'string' ? cc.text : '') || '');
    return {
      index,
      slide,
      number: slide.slideNumber ?? index + 1,
      title,
      topic,
      subtopic,
      checkpoint: cpMatch ? Number(cpMatch[1]) : s.isCheckpoint ? Number(s.checkpointNumber) || 1 : 0,
      badge: slide.badge,
      narrative: narrativeText,
      bullets,
      table: cc.table?.rows?.length ? cc.table : undefined,
      formula: cc.formulaBox,
      infographic: cc.infographic?.items?.length ? cc.infographic : undefined,
      spots: ((s.spotPearls && s.spotPearls.length ? s.spotPearls : s.spots) || []).filter((x: any) => typeof x === 'string' && x.trim()),
      terms: (s.medicalTerms || []).filter((t: any) => t?.term),
      questions,
      cards: (s.flashcards || []).map(normCard).filter(Boolean) as LessonCard[],
      interactives,
      teacher: hl?.quote || hl?.note ? { quote: hl.quote, note: hl.note, kind: hl.emphasisType } : undefined,
      important: s.importantPoint,
      examTip: s.examTip,
      section: 0,
    };
  });
}

/**
 * Bölümler: tekrar sayfası olan destelerde her tekrar sayfası bir bölümü kapatır. Olmayanlarda
 * ardışık aynı konu etiketleri (badge) birleştirilir; etiketler çok dağınıksa ~8 adımlık gruplar yapılır.
 */
export function buildSections(steps: LessonStep[]): LessonSection[] {
  const out: LessonSection[] = [];
  if (steps.some((s) => s.checkpoint)) {
    let cur: number[] = [];
    steps.forEach((s) => {
      cur.push(s.index);
      if (s.checkpoint) {
        out.push({ index: out.length, name: s.title, steps: cur });
        cur = [];
      }
    });
    if (cur.length) out.push({ index: out.length, name: steps[cur[0]].topic, steps: cur });
  } else {
    const runs: { name: string; steps: number[] }[] = [];
    steps.forEach((s) => {
      const key = (s.badge || '').trim();
      const last = runs[runs.length - 1];
      if (last && key && last.name === key) last.steps.push(s.index);
      else runs.push({ name: key || s.topic, steps: [s.index] });
    });
    const useRuns = steps.length <= 10 || runs.length <= Math.max(3, steps.length * 0.6);
    if (useRuns) {
      // Tek adımlık ardışık koşuları bir öncekine katarak bölüm sayısını makul tut
      runs.forEach((r) => {
        const prev = out[out.length - 1];
        if (prev && r.steps.length === 1 && prev.steps.length < 4 && runs.length > 12) prev.steps.push(...r.steps);
        else out.push({ index: out.length, name: r.name, steps: [...r.steps] });
      });
    } else {
      const size = steps.length > 60 ? 10 : 8;
      for (let i = 0; i < steps.length; i += size) {
        const chunk = steps.slice(i, i + size).map((s) => s.index);
        out.push({ index: out.length, name: steps[i].topic, steps: chunk });
      }
    }
  }
  out.forEach((sec) => sec.steps.forEach((i) => (steps[i].section = sec.index)));
  return out;
}

/* ---- Kazanımlar: deste dizini yüklenir, slayta sıkı eşleşenler gösterilir ---- */
export interface DeckKazanim { m: string; c: number; p: number[] }
let kazIndex: Promise<Record<string, DeckKazanim[]>> | null = null;
export const loadKazanimIndex = () =>
  (kazIndex ||= import('../../../data/kazanimlar/byDeck.json').then((m: any) => (m.default || m) as Record<string, DeckKazanim[]>).catch(() => ({})));

const fold = (s: string) => s.toLocaleLowerCase('tr-TR').replace(/ı/g, 'i').normalize('NFKD').replace(/[̀-ͯ]/g, '');
const STOP = new Set(['tanimlar', 'aciklar', 'aciklamak', 'tanimlamak', 'bilmek', 'sayar', 'ayirt', 'eder', 'temel', 'genel', 'arasindaki', 'farklari', 'onemini', 'kavramini', 'kavramlarini', 'ozellikleri', 'ozelliklerini', 'klinik']);
const stems = (s: string) => new Set((fold(s).match(/[a-z0-9]+/g) || []).filter((w) => w.length >= 5 && !STOP.has(w)).map((w) => w.slice(0, 6)));

/** Slayt başlığı/alt başlığı/etiketi ile kazanım metni arasında en az iki ayırt edici ortak kök (ya da bir kök + aynı PDF sayfası) gerekir. */
export function matchKazanim(step: LessonStep, list: DeckKazanim[] | undefined, page?: number, deckTitle = ''): DeckKazanim[] {
  if (!list?.length) return [];
  // Dersin adındaki kelimeler (ör. genetik destesinde "genetik") her kazanımda geçer; ayırt edici sayılmaz
  const common = stems(deckTitle);
  const st = stems(`${step.title} ${step.slide.subtitle || ''} ${step.badge || ''}`);
  common.forEach((w) => st.delete(w));
  return list
    .map((k) => {
      const kt = stems(k.m);
      let shared = 0;
      kt.forEach((w) => st.has(w) && shared++);
      const pageHit = page != null && k.p.includes(page);
      return { k, score: shared + (pageHit ? 0.5 : 0), ok: shared >= 2 || (shared >= 1 && pageHit) };
    })
    .filter((x) => x.ok)
    .sort((a, b) => b.score - a.score)
    .slice(0, 4)
    .map((x) => x.k);
}

/* ---- Tamamlanan adımlar ---- */
const DONE_KEY = 'medsoru_learn_done_v1';
export const readDone = (deckId: string): Set<number> => {
  try {
    return new Set((JSON.parse(localStorage.getItem(DONE_KEY) || '{}')[deckId] || []) as number[]);
  } catch {
    return new Set();
  }
};
export const writeDone = (deckId: string, done: Set<number>) => {
  try {
    const all = JSON.parse(localStorage.getItem(DONE_KEY) || '{}');
    all[deckId] = [...done];
    localStorage.setItem(DONE_KEY, JSON.stringify(all));
  } catch {
    /* ignore */
  }
};

/* ---- Metin: güvenli, hafif markdown → HTML (yerel deste verisi için) ---- */
const esc = (s: string) => s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c] as string);
export const stripEmoji = (s: string) => String(s ?? '').replace(/[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}\u{2B50}\u{2B55}]️?/gu, '').replace(/^\s+/, '');
const TAG_TONE: Record<string, string> = { 'SINAV SPOTU': 'warn', 'KRİTİK UYARI': 'bad', 'ÖNEMLİ': 'bad', 'ÇIKMIŞ SORU': 'accent', 'KLİNİK İPUCU': 'accent', 'YÜKSEK VERİM': 'ok' };
export const spotTone = (s: string) => {
  const t = stripEmoji(s);
  const m = t.match(/^\[?([A-ZÇĞİÖŞÜ ]{4,})\]?\s*:?/);
  return m && TAG_TONE[m[1].trim()] ? TAG_TONE[m[1].trim()] : /^🔴/.test(s) ? 'bad' : /^🔵/.test(s) ? 'accent' : 'warn';
};
export const inline = (s: string) => {
  let t = esc(stripEmoji(s));
  t = t.replace(/^\[?([A-ZÇĞİÖŞÜ ]{4,})\]?\s*:\s*|\[([A-ZÇĞİÖŞÜ ]{4,})\]\s*/g, (_m, a, b) => {
    const k = String(a || b).trim();
    return `<span class="ls-tag is-${TAG_TONE[k] || 'plain'}">${k.charAt(0) + k.slice(1).toLocaleLowerCase('tr-TR')}</span> `;
  });
  return t.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>').replace(/==(.+?)==/g, '<mark>$1</mark>').replace(/(?<![*\w])\*(?!\s)([^*]+?)\*(?!\*)/g, '<em>$1</em>');
};
const NOTE_LABEL: Record<string, string> = { NOTE: 'Not', IMPORTANT: 'Önemli', CRITICAL: 'Kritik', WARNING: 'Uyarı', CAUTION: 'Dikkat', TIP: 'İpucu' };
/** Not kutusunun tonu: kritik/uyarı → kırmızı, sınav spotu → turuncu, klinik/önemli → mavi, özet → yeşil, gerisi nötr */
export const noteTone = (s: string) => {
  const t = s.toLocaleUpperCase('tr-TR');
  if (/KRİTİK|UYARI|DİKKAT|TUZAK|HAYATİ/.test(t)) return 'bad';
  if (/SINAV|SPOT|ÇIKMIŞ/.test(t)) return 'warn';
  if (/YÜKSEK VERİM|ÖZET|REÇETE/.test(t)) return 'ok';
  if (/KLİNİK|ÖNEMLİ|İPUCU|TANI/.test(t)) return 'accent';
  return 'plain';
};
export const mdToHtml = (src: string) => {
  const lines = String(src || '').split('\n');
  let out = '';
  let depth = 0;
  const close = (to: number) => {
    while (depth > to) {
      out += '</li></ul>';
      depth--;
    }
  };
  let tbl: string[][] = [];
  const flushTable = () => {
    if (!tbl.length) return;
    const rows = tbl.filter((r) => !r.every((c) => /^:?-{2,}:?$/.test(c)));
    const [head, ...body] = rows;
    out += `<div class="ls-table"><table><thead><tr>${head.map((c) => `<th>${inline(c)}</th>`).join('')}</tr></thead><tbody>${body
      .map((r) => `<tr>${r.map((c, i) => `<td data-h="${esc(stripEmoji(head[i] || '').replace(/\*/g, ''))}">${inline(c)}</td>`).join('')}</tr>`)
      .join('')}</tbody></table></div>`;
    tbl = [];
  };
  // Ardışık "> …" satırları tek not kutusu olur; "[!NOTE]" / "[TEMEL İLKE]" etiketi başlığa taşınır
  let quote: string[] = [];
  const flushQuote = () => {
    if (!quote.length) return;
    let label = '';
    const parts = quote.filter(Boolean);
    const first = parts[0] || '';
    const gh = first.match(/^\[!([A-Z]+)\]\s*(.*)$/i);
    if (gh) {
      label = NOTE_LABEL[gh[1].toUpperCase()] || gh[1];
      if (gh[2]) parts[0] = gh[2];
      else parts.shift();
    } else {
      const tag = stripEmoji(first).match(/^\[([A-ZÇĞİÖŞÜ ]{4,})\]\s*:?\s*|^([A-ZÇĞİÖŞÜ ]{4,}):\s*/);
      if (tag) {
        const k = String(tag[1] || tag[2]).trim();
        label = k.charAt(0) + k.slice(1).toLocaleLowerCase('tr-TR');
        parts[0] = stripEmoji(first).slice(tag[0].length);
      }
    }
    const body = parts.join(' ').trim();
    quote = [];
    if (!body) return;
    const tone = noteTone(`${label} ${label ? '' : body.slice(0, 40)}`);
    out += `<aside class="ls-note is-${tone}">${label ? `<span class="ls-note-k">${esc(label)}</span>` : ''}<p>${inline(body)}</p></aside>`;
  };
  for (const raw of lines) {
    if (raw.trim().startsWith('>')) {
      close(0);
      flushTable();
      quote.push(raw.trim().replace(/^>\s?/, '').trim());
      continue;
    }
    flushQuote();
    if (/^\s*\|.*\|\s*$/.test(raw)) {
      close(0);
      tbl.push(raw.trim().slice(1, -1).split('|').map((c) => c.trim()));
      continue;
    }
    flushTable();
    const m = raw.match(/^(\s*)(?:[-*•]|\d+[.)])\s+(.*)$/);
    if (m) {
      const lvl = Math.min(2, Math.floor(m[1].replace(/\t/g, '  ').length / 2) + 1);
      if (depth < lvl) while (depth < lvl) { out += '<ul><li>'; depth++; }
      else { close(lvl); out += '</li><li>'; }
      out += inline(m[2]);
      continue;
    }
    close(0);
    const line = raw.trim();
    if (!line || /^-{3,}$/.test(line)) continue;
    if (/^#{1,4}\s/.test(line)) out += `<h4>${inline(line.replace(/^#+\s*/, ''))}</h4>`;
    else out += `<p>${inline(line)}</p>`;
  }
  flushQuote();
  flushTable();
  close(0);
  return out;
};

/* ---- Terimler: adımın kendi terimleri + metinde geçen sözlük terimleri ---- */
export interface GlossaryLike { term: string; aliases?: string[]; category?: string; definition: string }
type Needle = { item: GlossaryLike; needle: string; shown: string };
let needleCache: { src: GlossaryLike[]; list: Needle[] } | null = null;
const needlesFor = (gl: GlossaryLike[]): Needle[] => {
  if (needleCache?.src === gl) return needleCache.list;
  const list: Needle[] = [];
  gl.forEach((item) => {
    if (!item?.term || !item.definition) return;
    [item.term, ...(item.aliases || [])].forEach((a) => {
      const shown = String(a).split(/[(/]/)[0].trim();
      const needle = fold(shown);
      if (needle.length >= 4) list.push({ item, needle, shown });
    });
  });
  list.sort((a, b) => b.needle.length - a.needle.length);
  needleCache = { src: gl, list };
  return list;
};
const enriched = new WeakMap<LessonStep, LessonStep>();
export function withGlossaryTerms(step: LessonStep, glossary: GlossaryLike[] | undefined, max = 14): LessonStep {
  if (!glossary?.length) return step;
  const hit = enriched.get(step);
  if (hit) return hit;
  const text = fold([step.title, step.slide.subtitle, step.narrative, ...step.bullets.map((b) => `${b.title} ${b.desc}`), ...step.spots, step.table?.rows.map((r) => r.join(' ')).join(' ')].filter(Boolean).join(' \n '));
  const have = new Set(step.terms.map((t) => fold(t.term)));
  const found: (LessonStep['terms'][number] & { match?: string; category?: string; at: number })[] = [];
  for (const n of needlesFor(glossary)) {
    if (step.terms.length + found.length >= max) break;
    const key = fold(n.item.term);
    if (have.has(key)) continue;
    const re = new RegExp(`(^|[^a-z0-9])${n.needle.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}`);
    const m = text.match(re);
    if (!m || m.index == null) continue;
    have.add(key);
    found.push({ term: n.item.term, explanation: n.item.definition, match: n.shown, category: n.item.category, at: m.index });
  }
  found.sort((a, b) => a.at - b.at);
  const out = { ...step, terms: [...step.terms, ...found.map(({ at: _at, ...t }) => t)] };
  enriched.set(step, out);
  return out;
}
