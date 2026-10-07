import React, { useMemo } from 'react';
import { splitHighlights } from '../../services/searchText';

/** Arama terimlerini <mark> ile vurgular (Türkçe karakter katlamalı). */
export const Highlight: React.FC<{ text: string; terms?: string[] }> = ({ text, terms }) => {
  const parts = useMemo(() => splitHighlights(text, terms || []), [text, terms]);
  if (parts.length === 1 && !parts[0].hit) return <>{text}</>;
  return (
    <>
      {parts.map((p, i) => (p.hit ? <mark key={i} className="ms-hl">{p.t}</mark> : <React.Fragment key={i}>{p.t}</React.Fragment>))}
    </>
  );
};

export interface StemParts {
  lead: string;
  items: { mark: string; text: string }[];
  tail: string;
}

const ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X'];
const LINE_ITEM = /^\s*(?:((?=[IVX])(?:X|IX|IV|V?I{0,3}))\s*[.)\-]|(\d{1,2})\s*[.)]|([a-eA-E])\)|([•\-–*·▪●◦]))\s+(.+)$/;
const QUESTION_TAIL = /(hangisi|hangileri|yukarıda|yukarıdaki|aşağıdaki|doğrudur|yanlıştır|nedir|\?)/i;

function seqOk(marks: string[], kind: 'roman' | 'num' | 'alpha' | 'bullet'): boolean {
  if (kind === 'bullet') return true;
  return marks.every((m, i) => {
    if (kind === 'roman') return m.toUpperCase() === ROMAN[i];
    if (kind === 'num') return Number(m) === i + 1;
    return m.toLowerCase() === 'abcdefghij'[i];
  });
}

/** Son maddeye yapışmış soru cümlesini ("… Yukarıdakilerden hangileri doğrudur?") ayırır. */
function splitTrailingQuestion(text: string): [string, string] {
  const re = /[.;:!]\s+(?=[A-ZÇĞİÖŞÜ])/g;
  let m: RegExpExecArray | null;
  let cut = -1;
  while ((m = re.exec(text))) cut = m.index + 1;
  if (cut > 0) {
    const rest = text.slice(cut).trim();
    if (QUESTION_TAIL.test(rest) && rest.length < 220) return [text.slice(0, cut).trim(), rest];
  }
  return [text, ''];
}

/** Soru kökünü giriş + maddeler + soru cümlesi olarak ayırır. Madde yoksa items boş döner. */
export function parseStem(raw: string): StemParts {
  const text = String(raw || '').replace(/\r/g, '').trim();
  const empty: StemParts = { lead: text, items: [], tail: '' };
  if (!text) return empty;

  // 1) Satır başı maddeler
  const lines = text.split('\n');
  const lead: string[] = [];
  const items: { mark: string; text: string; kind: 'roman' | 'num' | 'alpha' | 'bullet' }[] = [];
  const tail: string[] = [];
  let phase: 'lead' | 'items' | 'tail' = 'lead';
  let prevBlank = false;
  for (const line of lines) {
    const t = line.trim();
    if (!t) { prevBlank = true; continue; }
    const m = t.match(LINE_ITEM);
    if (m && phase !== 'tail') {
      const kind = m[1] ? 'roman' : m[2] ? 'num' : m[3] ? 'alpha' : 'bullet';
      items.push({ mark: (m[1] || m[2] || m[3] || '').toUpperCase(), text: m[5].trim(), kind });
      phase = 'items';
    } else if (phase === 'lead') {
      lead.push(t);
    } else if (phase === 'items' && !prevBlank && !QUESTION_TAIL.test(t)) {
      items[items.length - 1].text += ' ' + t;
    } else {
      phase = 'tail';
      tail.push(t);
    }
    prevBlank = false;
  }
  if (items.length >= 2 && items.every((i) => i.kind === items[0].kind) && seqOk(items.map((i) => i.mark), items[0].kind)) {
    const out = items.map((i) => ({ mark: i.kind === 'bullet' ? '' : i.mark, text: i.text }));
    let tailText = tail.join(' ');
    if (!tailText) {
      const [body, q] = splitTrailingQuestion(out[out.length - 1].text);
      if (q) { out[out.length - 1].text = body; tailText = q; }
    }
    return { lead: lead.join(' '), items: out, tail: tailText };
  }

  // 2) Satır içi roma rakamlı maddeler: "… ? I. Fizyolojik sarılık II. Gilbert …"
  const flat = text.replace(/\s+/g, ' ');
  const re = /(^|[\s(:;,.?])(X|IX|IV|V?I{1,3}|V)\s*[.)]\s+/g;
  const hits: { at: number; end: number; mark: string }[] = [];
  let m: RegExpExecArray | null;
  while ((m = re.exec(flat))) {
    const expected = ROMAN[hits.length];
    if (m[2] === expected) hits.push({ at: m.index + m[1].length, end: m.index + m[0].length, mark: m[2] });
    else if (m[2] === 'I' && hits.length) break;
  }
  if (hits.length >= 2) {
    const out = hits.map((h, i) => ({ mark: h.mark, text: flat.slice(h.end, i + 1 < hits.length ? hits[i + 1].at : undefined).trim() }));
    const [body, q] = splitTrailingQuestion(out[out.length - 1].text);
    out[out.length - 1].text = body;
    return { lead: flat.slice(0, hits[0].at).trim(), items: out, tail: q };
  }
  return empty;
}

/**
 * Soru kökü: maddeli köklerde (I., II. …, 1), •) maddeler ayrı satırlarda ve işaretli gösterilir,
 * soru cümlesi altta vurgulanır. Maddesiz kök tek paragraf olarak kalır.
 */
export const StemText: React.FC<{
  text: string;
  terms?: string[];
  className?: string;
  size?: 'md' | 'sm';
}> = ({ text, terms, className = '', size = 'md' }) => {
  const parts = useMemo(() => parseStem(text), [text]);
  const cls = `ms-stem ${size === 'sm' ? 'is-sm' : ''} ${className}`;
  if (!parts.items.length) {
    return (
      <p className={`${cls} m-0 whitespace-pre-line`}>
        <Highlight text={parts.lead} terms={terms} />
      </p>
    );
  }
  return (
    <div className={cls}>
      {parts.lead && <p className="m-0"><Highlight text={parts.lead} terms={terms} /></p>}
      <ol className="ms-stem-list">
        {parts.items.map((it, i) => (
          <li key={i}>
            <span className={`ms-stem-mark ${it.mark ? '' : 'is-dot'}`} aria-hidden={!it.mark}>{it.mark}</span>
            <span className="min-w-0"><Highlight text={it.text} terms={terms} /></span>
          </li>
        ))}
      </ol>
      {parts.tail && <p className="ms-stem-tail m-0"><Highlight text={parts.tail} terms={terms} /></p>}
    </div>
  );
};
