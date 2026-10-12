/**
 * Ders özeti markdown'ını okuyucunun çizeceği yapıya çevirir (saf işlev, arayüzden bağımsız).
 *
 * Girdi biçimi (src/data/summaries/kurulN.json → content):
 *   📘 Başlık: Detaylı Çalışma Metni
 *   **Ders Kodu & Başlığı:** … / **Öğretim Üyesi:** … / **Müfredat Dönemi:** … / **Tıbbi Kaynak ve Kılavuzlar:** …
 *   ## 1. Bölüm            → bölüm (Öğrenim hedefleri / gövde / spot duvarı / çıkmış sorular)
 *   ### Alt başlık         → alt bölüm (şablon alt başlıklar gizlenir, maddeleri öncekine katılır)
 *   > [!WARNING] …         → uyarı kutusu (ilk satırdaki **Başlık:** kutu başlığı olur)
 *   | a | b |              → tablo
 *   ### Soru N: [etiket]   → çıkmış soru (şıklar, <details> içinde cevap + çözüm)
 * Metin silinmez ya da uydurulmaz; yalnız yapı çıkarılır.
 */
import { structureBulletBlock, isBoilerplateSubheading, foldForCompare, type RichGroup } from './summaryStructure';

export type CalloutTone = 'warning' | 'important' | 'tip' | 'note';

export type Block =
  | { kind: 'rich'; groups: RichGroup[] }
  | { kind: 'sub'; id: string; title: string; groups: RichGroup[] }
  | { kind: 'callout'; tone: CalloutTone; title?: string; text: string; items: string[] }
  | { kind: 'table'; id: string; headers: string[]; rows: string[][] }
  | { kind: 'para'; text: string };

export interface Question {
  id: string;
  number: string;
  tag?: string;
  stem: string;
  options: { letter: string; text: string }[];
  answer?: string;
  explanation?: string;
}

export interface Spot {
  term?: string;
  text: string;
}

export type SectionKind = 'objectives' | 'body' | 'spot' | 'questions';

export interface Section {
  id: string;
  number?: string;
  title: string;
  /** Slayt başlığı çok uzunsa başlıktan ayrılan devamı */
  context?: string;
  kind: SectionKind;
  blocks: Block[];
  /** İçindekiler için alt başlıklar ve tablolar */
  subs: { id: string; title: string; table?: boolean }[];
  objectives: string[];
  spots: Spot[];
  questions: Question[];
}

export interface SummaryDoc {
  meta: { title?: string; course?: string; instructor?: string; term?: string; sources?: string };
  sections: Section[];
  counts: { sections: number; tables: number; questions: number; spots: number };
}

const EMOJI = /[\p{Extended_Pictographic}\u{FE0F}\u{200D}]/gu;
/** Slayt artıkları: emoji ve özel kullanım alanı imleri (Wingdings madde işareti \uf0a2 vb.) */
const PUA = /[\uE000-\uF8FF]/g;
export const stripEmoji = (s: string) => s.replace(EMOJI, '').replace(PUA, ' ').replace(/\s{2,}/g, ' ').trim();

/** "**Başlık:** metin" → ["Başlık", "metin"]; yoksa null */
const leadingBold = (s: string): [string, string] | null => {
  const m = s.match(/^\*\*(.+?)\*\*\s*[:.]?\s*(.*)$/s);
  if (!m) return null;
  const head = m[1].replace(/[:.]\s*$/, '').trim();
  return head ? [head, m[2].trim()] : null;
};

/** Bölüm gövdesini blok parçalarına ayırır: ### başlık, > kutu ve ardışık tablo satırları ayrı parçadır. */
const splitChunks = (content: string): string[] => {
  const chunks: string[] = [];
  let cur: string[] = [];
  let mode: 'text' | 'table' | 'callout' = 'text';
  const flush = () => {
    if (cur.length) chunks.push(cur.join('\n'));
    cur = [];
  };
  for (const line of content.split('\n')) {
    const t = line.trim();
    const isTable = /^\|.*\|$/.test(t);
    const isQuote = t.startsWith('>');
    if (/^###\s+/.test(t)) {
      flush();
      mode = 'text';
    } else if (isQuote && (mode !== 'callout' || /^>\s*\[!/.test(t))) {
      flush();
      mode = 'callout';
    } else if (isTable && mode !== 'table') {
      flush();
      mode = 'table';
    } else if (mode === 'table' && !isTable) {
      flush();
      mode = 'text';
    } else if (mode === 'callout' && !isQuote) {
      flush();
      mode = 'text';
    }
    cur.push(line);
  }
  flush();
  return chunks;
};

const parseCallout = (chunk: string): Extract<Block, { kind: 'callout' }> | null => {
  const lines = chunk.split('\n').map((l) => l.trim().replace(/^>\s?/, ''));
  const first = lines[0] || '';
  const typeMatch = first.match(/^\[!(\w+)\]\s*(.*)$/);
  const type = (typeMatch?.[1] || 'NOTE').toUpperCase();
  const tone: CalloutTone = type === 'WARNING' || type === 'CAUTION' ? 'warning' : type === 'IMPORTANT' ? 'important' : type === 'TIP' ? 'tip' : 'note';
  const body = [typeMatch ? typeMatch[2] : first, ...lines.slice(1)].map((l) => l.trim()).filter(Boolean);
  let title: string | undefined;
  const textParts: string[] = [];
  const items: string[] = [];
  body.forEach((l, i) => {
    if (/^[-*•]\s+/.test(l)) {
      const item = stripEmoji(l.replace(/^[-*•]\s+/, ''));
      if (item) items.push(item);
      return;
    }
    if (i === 0) {
      const lb = leadingBold(l);
      if (lb) {
        title = stripEmoji(lb[0]);
        if (lb[1]) textParts.push(lb[1]);
        return;
      }
    }
    textParts.push(l);
  });
  const text = stripEmoji(textParts.join(' '));
  if (!text && !items.length && !title) return null;
  return { kind: 'callout', tone, title, text, items };
};

const parseTable = (chunk: string, id: string): Extract<Block, { kind: 'table' }> | null => {
  const rowsRaw = chunk.split('\n').map((l) => l.trim()).filter((l) => l.startsWith('|'));
  if (rowsRaw.length < 2) return null;
  const cells = (l: string) => l.replace(/^\|/, '').replace(/\|$/, '').split('|').map((c) => c.trim());
  const headers = cells(rowsRaw[0]);
  const isSep = (l: string) => l.replace(/[:\-|\s]/g, '').length === 0;
  const rows = rowsRaw.slice(isSep(rowsRaw[1]) ? 2 : 1).filter((l) => !isSep(l)).map(cells);
  if (!headers.length || !rows.length) return null;
  // Eksik hücreleri doldur ki kolonlar kaymasın
  const n = Math.max(headers.length, ...rows.map((r) => r.length));
  const pad = (r: string[]) => (r.length < n ? [...r, ...Array(n - r.length).fill('')] : r);
  return { kind: 'table', id, headers: pad(headers), rows: rows.map(pad) };
};

const QUESTION_HEAD = /^Soru\s*(\d+)?\s*[:.)-]?\s*(?:\[(.*?)\])?/i;

const looksLikeQuestion = (heading: string, rest: string) =>
  QUESTION_HEAD.test(heading) && (/\*\*Soru \/ Öncül:\*\*/.test(rest) || /^[-*]\s*\*\*[A-E]\)\*\*/m.test(rest) || rest.includes('<details>'));

const parseQuestion = (heading: string, rest: string, id: string, fallbackNo: number): Question => {
  const m = heading.match(QUESTION_HEAD);
  const stemParts: string[] = [];
  const options: Question['options'] = [];
  const solution: string[] = [];
  let inDetails = false;
  let lastWasOption = false;
  for (const raw of rest.split('\n')) {
    const l = raw.trim();
    if (!l) continue;
    if (l.startsWith('<details')) {
      inDetails = true;
      continue;
    }
    if (l.startsWith('</details')) {
      inDetails = false;
      continue;
    }
    if (inDetails) {
      if (/^<summary/i.test(l) || /^Sınav Simülasyonu/i.test(stripEmoji(l))) continue;
      solution.push(stripEmoji(l));
      continue;
    }
    const opt = l.match(/^[-*]\s*(?:\*\*)?([A-E])\)(?:\*\*)?\s*(.*)$/);
    if (opt) {
      options.push({ letter: opt[1], text: opt[2].trim() });
      lastWasOption = true;
      continue;
    }
    if (lastWasOption && /^\s{2,}[-*]\s+/.test(raw) && options.length) {
      // Bölünmüş şık devamı ("B) SM" + "  - A (Spinal …)") → aynı şıkka eklenir
      const prev = options[options.length - 1];
      const cont = l.replace(/^[-*]\s+/, '');
      prev.text = /[A-ZÇĞİÖŞÜ]$/.test(prev.text) && /^[A-Z]\s/.test(cont) ? prev.text + cont : `${prev.text} ${cont}`;
      continue;
    }
    lastWasOption = false;
    stemParts.push(l.replace(/^\*\*Soru \/ Öncül:\*\*\s*/, ''));
  }
  const sol = solution.join('\n');
  const answer = sol.match(/Doğru Cevap:\**\s*([A-Ea-e])\b/)?.[1]?.toUpperCase();
  let explanation = '';
  const ex = sol.match(/Çözüm Notu:\**\s*([\s\S]*)$/);
  if (ex) explanation = ex[1].trim();
  else explanation = sol.replace(/^.*Doğru Cevap:.*$/m, '').trim();
  return {
    id,
    number: m?.[1] || String(fallbackNo),
    tag: m?.[2]?.trim() || undefined,
    stem: stemParts.join('\n').trim(),
    options,
    answer,
    explanation: explanation || undefined,
  };
};

/** Spot duvarındaki maddeler: "- **Terim:** metin" ya da "> - 📌 **metin**" */
const collectSpots = (content: string): Spot[] => {
  const out: Spot[] = [];
  for (const raw of content.split('\n')) {
    const l = raw.trim().replace(/^>\s?/, '').trim();
    if (!/^[-*•]\s+/.test(l)) continue;
    if (/^\s{2,}/.test(raw.replace(/^>\s?/, ''))) {
      // Alt madde: bir öncekine eklenir
      const prev = out[out.length - 1];
      if (prev) prev.text = `${prev.text} ${stripEmoji(l.replace(/^[-*•]\s+/, ''))}`.trim();
      continue;
    }
    const body = stripEmoji(l.replace(/^[-*•]\s+/, ''));
    const lb = leadingBold(body);
    if (lb && lb[1]) out.push({ term: lb[0], text: lb[1] });
    else if (lb) out.push({ text: lb[0] });
    else if (body) out.push({ text: body });
  }
  return out;
};

const slug = (s: string) =>
  foldForCompare(s)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 32);

export function parseSummary(raw: string): SummaryDoc {
  const text = (raw || '').replace(/\r\n?/g, '\n');
  const firstSection = text.search(/^##\s+/m);
  const head = firstSection > 0 ? text.slice(0, firstSection) : '';
  const meta: SummaryDoc['meta'] = {};
  for (const l of head.split('\n').map((x) => x.trim())) {
    if (/^📘/u.test(l)) meta.title = stripEmoji(l).replace(/:\s*Detaylı Çalışma Metni.*$/i, '').trim();
    const field = (label: string) => (l.includes(`**${label}:**`) ? l.split(`**${label}:**`)[1].trim() : undefined);
    meta.course ??= field('Ders Kodu & Başlığı');
    meta.instructor ??= field('Öğretim Üyesi');
    meta.term ??= field('Müfredat Dönemi');
    meta.sources ??= field('Tıbbi Kaynak ve Kılavuzlar');
  }

  const body = firstSection >= 0 ? text.slice(firstSection) : text;
  const rawSections = body.split(/(?=^##\s+)/m).filter((s) => s.trim());
  const counts = { sections: 0, tables: 0, questions: 0, spots: 0 };
  const usedIds = new Set<string>();

  const sections: Section[] = rawSections.map((secStr, si) => {
    const lines = secStr.split('\n');
    // Bozuk büyük/küçük harf dönüşümü: "Peri̇yodi̇k" (i + birleşen nokta) → "Periyodik"
    const rawHeading = (lines[0] || '').replace(/^##\s+/, '').replace(/i\u0307/g, 'i').replace(/\s*[\uE000-\uF8FF]\s*/g, '  ').trim();
    const heading = stripEmoji(rawHeading);
    let number: string | undefined;
    let title = heading || `Bölüm ${si + 1}`;
    let context: string | undefined;
    // Slayt başlığı + ilk satır çift boşlukla birleşmişse oradan ayrılır
    const glued = rawHeading.match(/^(.*?\S)\s{2,}(\S.*)$/);
    if (glued) {
      title = stripEmoji(glued[1]);
      context = stripEmoji(glued[2]);
    }
    const num = title.match(/^(\d+)\s*[.)-]\s*(.*)$/);
    if (num) {
      number = num[1];
      title = num[2].trim();
    }
    if (title.length > 72) {
      const br = title.match(/^(.{24,64}?)([,:;.!?]\s+)(.*)$/);
      if (br) {
        title = br[1].trim();
        context = [br[3].trim(), context].filter(Boolean).join(' ');
      } else {
        const cut = title.lastIndexOf(' ', 60);
        context = [title.slice(cut > 30 ? cut + 1 : 60).trim(), context].filter(Boolean).join(' ');
        title = `${title.slice(0, cut > 30 ? cut : 60).trim()}…`;
      }
    }
    let base = `s${si + 1}-${slug(title) || 'bolum'}`;
    while (usedIds.has(base)) base += '-x';
    usedIds.add(base);

    const low = title.toLocaleLowerCase('tr');
    const kind: SectionKind = /öğrenim hedefleri/.test(low)
      ? 'objectives'
      : /spot bilgiler|hızlı tekrar/.test(low)
        ? 'spot'
        : /çıkmış.*soru/.test(low)
          ? 'questions'
          : 'body';

    const content = lines.slice(1).join('\n');
    const sec: Section = { id: base, number, title, context, kind, blocks: [], subs: [], objectives: [], spots: [], questions: [] };

    if (kind === 'objectives') {
      sec.objectives = content
        .split('\n')
        .map((l) => l.trim())
        .filter((l) => /^[-*•]\s+/.test(l))
        .map((l) => stripEmoji(l.replace(/^[-*•]\s+/, '')));
    }
    if (kind === 'spot') {
      sec.spots = collectSpots(content);
      counts.spots += sec.spots.length;
    }

    if (kind === 'body' || kind === 'questions' || (kind === 'objectives' && !sec.objectives.length)) {
      const bodyKeys: string[] = [];
      splitChunks(content).forEach((chunk, ci) => {
        const t = chunk.trim();
        if (!t) return;
        if (t.startsWith('### ')) {
          const [h, ...restLines] = t.split('\n');
          const subTitle = stripEmoji(h.replace(/^###\s+/, ''));
          const rest = restLines.join('\n');
          if (looksLikeQuestion(subTitle, rest)) {
            sec.questions.push(parseQuestion(subTitle, rest, `${base}-q${sec.questions.length + 1}`, sec.questions.length + 1));
            return;
          }
          const groups = structureBulletBlock(rest);
          rest.split('\n').forEach((l) => bodyKeys.push(foldForCompare(l.replace(/^\s*[-*]\s*/, ''))));
          if (isBoilerplateSubheading(subTitle)) {
            const prev = sec.blocks[sec.blocks.length - 1];
            if (prev?.kind === 'rich') prev.groups.push(...groups);
            else if (groups.length) sec.blocks.push({ kind: 'rich', groups });
            return;
          }
          const id = `${base}-h${ci}`;
          sec.subs.push({ id, title: subTitle });
          sec.blocks.push({ kind: 'sub', id, title: subTitle, groups });
          return;
        }
        if (t.startsWith('>')) {
          const c = parseCallout(t);
          if (c) sec.blocks.push(c);
          return;
        }
        if (t.startsWith('|')) {
          const id = `${base}-t${ci}`;
          const tb = parseTable(t, id);
          if (tb) {
            counts.tables += 1;
            sec.subs.push({ id, title: tb.headers.slice(0, 2).filter(Boolean).join(' / ') || 'Tablo', table: true });
            sec.blocks.push(tb);
            return;
          }
        }
        for (const para of t.split(/\n{2,}/)) {
          const p = para.trim();
          if (!p) continue;
          if (/^[-*]\s+/.test(p)) {
            const groups = structureBulletBlock(p);
            p.split('\n').forEach((l) => bodyKeys.push(foldForCompare(l.replace(/^\s*[-*]\s*/, ''))));
            const prev = sec.blocks[sec.blocks.length - 1];
            if (prev?.kind === 'rich') prev.groups.push(...groups);
            else if (groups.length) sec.blocks.push({ kind: 'rich', groups });
          } else {
            sec.blocks.push({ kind: 'para', text: stripEmoji(p.replace(/\n/g, ' ')) });
          }
        }
      });
      // Uzun slayt başlığı ilk maddede aynen tekrar ediyorsa devam satırını gösterme
      if (sec.context) {
        const whole = foldForCompare(heading.replace(/^\d+\s*[.)-]\s*/, ''));
        const ctx = foldForCompare(sec.context).slice(0, 40);
        if (bodyKeys.includes(whole) || (ctx.length > 12 && bodyKeys.some((k) => k.includes(ctx)))) sec.context = undefined;
      }
      if (sec.questions.length && !sec.blocks.length) sec.kind = 'questions';
    }
    counts.questions += sec.questions.length;
    return sec;
  });

  // Boş bölümleri at (yalnız başlıktan ibaret)
  const kept = sections.filter((s) => s.blocks.length || s.objectives.length || s.spots.length || s.questions.length);
  counts.sections = kept.filter((s) => s.kind === 'body').length;
  return { meta, sections: kept, counts };
}
