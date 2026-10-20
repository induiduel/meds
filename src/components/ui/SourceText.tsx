import React, { useMemo } from 'react';
import { foldText } from '../../services/searchText';
import { focusMarks } from '../../services/questionFocus';
import { maddele as maddeleMetin } from '../../utils/maddele';

/**
 * Ders notu / ders özeti / açıklama gibi kaynak metinlerini düz metin yerine okunur biçimde gösterir:
 * başlık satırları, madde işaretleri, "Terim: açıklama" satırları, **kalın** vurgular ve
 * "Not / Önemli / Dikkat / Sınav" gibi uyarı satırları ayrı bloklara ayrılır. Uzun tek paragraf
 * birkaç cümlelik paragraflara bölünür. Metnin kendisi değiştirilmez, yalnızca yapısı gösterilir.
 */

type Block =
  | { kind: 'h'; text: string }
  | { kind: 'p'; text: string }
  | { kind: 'li'; items: { mark: string; text: string; dz?: number }[]; ordered: boolean }
  | { kind: 'note'; label: string; text: string };

const BULLET = /^\s*(?:[-–•*▪●◦·►➢✓]|(\d{1,2})[.)]|([a-eA-E])\))\s+(.+)$/;
const NOTE = /^\s*(not|önemli|dikkat|ipucu|uyarı|sınav(?:da)?(?: için)?|klinik(?: not| ipucu)?|akılda tut|özetle|sonuç)\s*[:!–-]\s*(.+)$/i;
const MD_HEAD = /^\s*#{1,4}\s+(.+?)\s*#*\s*$/;

function isHeading(line: string, next?: string): boolean {
  const t = line.trim();
  if (!t || t.length > 70) return false;
  if (/[:：]$/.test(t) && !/\s{2,}/.test(t) && t.split(/\s+/).length <= 8) return true;
  // Kısa, tamamı büyük harfli satır (OCR başlıkları): "PATOGENEZ", "KLİNİK BULGULAR"
  const letters = t.replace(/[^A-Za-zÇĞİÖŞÜçğıöşü]/g, '');
  if (letters.length >= 4 && letters === letters.toLocaleUpperCase('tr-TR') && t.split(/\s+/).length <= 6 && !!next) return true;
  return false;
}

/** Uzun tek paragrafı 2–3 cümlelik parçalara böler (kısaltmalarda bölmemeye çalışır). */
function splitLongParagraph(text: string): string[] {
  if (text.length < 360) return [text];
  const sentences = text.match(/[^.!?]+(?:[.!?]+(?=\s+[A-ZÇĞİÖŞÜ0-9(]|\s*$)|$)/g)?.map((s) => s.trim()).filter(Boolean) || [text];
  if (sentences.length < 3) return [text];
  const out: string[] = [];
  let cur = '';
  for (const s of sentences) {
    cur = cur ? `${cur} ${s}` : s;
    if (cur.length > 220) {
      out.push(cur);
      cur = '';
    }
  }
  if (cur) out.length && cur.length < 80 ? (out[out.length - 1] += ' ' + cur) : out.push(cur);
  return out;
}

export function parseSourceText(raw: string, uzunBol = true): Block[] {
  const text = String(raw || '')
    .replace(/\r/g, '')
    // satır başı girintisi korunur (iç içe madde düzeyi ondan bulunur), satır içi boşluklar tekleşir
    .replace(/(\S)[ \t ]+/g, '$1 ')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
  if (!text) return [];
  const lines = text.split('\n');
  const blocks: Block[] = [];
  let para: string[] = [];
  let girinti: number[] = [];
  const flush = () => {
    if (!para.length) return;
    const joined = para.join(' ').trim();
    para = [];
    if (joined) (uzunBol ? splitLongParagraph(joined) : [joined]).forEach((p) => blocks.push({ kind: 'p', text: p }));
  };
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    if (!line) { flush(); continue; }
    const md = line.match(MD_HEAD);
    if (md) { flush(); blocks.push({ kind: 'h', text: md[1] }); continue; }
    const note = line.match(NOTE);
    if (note) { flush(); blocks.push({ kind: 'note', label: note[1], text: note[2] }); continue; }
    const b = line.match(BULLET);
    if (b) {
      flush();
      const mark = b[1] || b[2] || '';
      const g = (lines[i].match(/^[ \t ]*/)?.[0] || '').replace(/\t/g, '    ').length;
      const last = blocks[blocks.length - 1];
      const ayniListe = !!last && last.kind === 'li' && (g > 0 || last.ordered === Boolean(mark));
      if (!ayniListe) girinti = [];
      while (girinti.length && girinti[girinti.length - 1] > g) girinti.pop();
      if (!girinti.length || girinti[girinti.length - 1] < g) girinti.push(g);
      const it = { mark, text: b[3], dz: Math.min(2, girinti.length - 1) };
      if (ayniListe) (last as Extract<Block, { kind: 'li' }>).items.push(it);
      else blocks.push({ kind: 'li', items: [it], ordered: Boolean(mark) });
      continue;
    }
    // Maddenin alt satırı (girintisiz devam): önceki madde boş satırla kesilmediyse ona eklenir
    const last = blocks[blocks.length - 1];
    if (!para.length && last && last.kind === 'li' && lines[i - 1]?.trim() && !isHeading(line, lines[i + 1])) {
      last.items[last.items.length - 1].text += ' ' + line;
      continue;
    }
    if (isHeading(line, lines[i + 1]?.trim())) { flush(); blocks.push({ kind: 'h', text: line.replace(/[:：]$/, '') }); continue; }
    para.push(line);
  }
  flush();
  return blocks;
}

/** Terimleri işaretler: 1 = soru/arama terimi, 2 = doğru şık ifadesi. */
export const Marked: React.FC<{ text: string; terms?: string[]; answerTerms?: string[] }> = ({ text, terms, answerTerms }) => {
  const parts = useMemo(() => {
    if (!terms?.length && !answerTerms?.length) return null;
    const marks = focusMarks(text, terms || [], answerTerms || []);
    const out: { t: string; v: number }[] = [];
    let start = 0;
    for (let i = 1; i <= text.length; i++) {
      if (i === text.length || marks[i] !== marks[start]) {
        out.push({ t: text.slice(start, i), v: marks[start] });
        start = i;
      }
    }
    return out.some((p) => p.v) ? out : null;
  }, [text, terms, answerTerms]);
  if (!parts) return <>{text}</>;
  return (
    <>
      {parts.map((p, i) =>
        p.v ? <mark key={i} className={`ms-hl ${p.v === 2 ? 'is-answer' : ''}`}>{p.t}</mark> : <React.Fragment key={i}>{p.t}</React.Fragment>,
      )}
    </>
  );
};

/** Satır içi: **kalın**, "Terim: açıklama" başı ve oklar; kalan metin arama/soru terimleriyle vurgulanır. */
const Inline: React.FC<{ text: string; terms?: string[]; answerTerms?: string[]; lead?: boolean }> = ({ text, terms, answerTerms, lead = true }) => {
  let body = text;
  let key: string | null = null;
  if (lead) {
    const m = body.match(/^([^:.;!?]{2,42}):\s+(.+)$/);
    if (m && !/^https?$/i.test(m[1]) && m[1].split(/\s+/).length <= 5) {
      key = m[1];
      body = m[2];
    }
  }
  const parts = body.split(/(\*\*[^*]+\*\*|→|->|⇒)/g).filter((p) => p !== '');
  return (
    <>
      {key && <strong className="ms-src-key">{key}:</strong>}
      {key && ' '}
      {parts.map((p, i) => {
        if (/^\*\*[^*]+\*\*$/.test(p)) return <strong key={i}><Marked text={p.slice(2, -2)} terms={terms} answerTerms={answerTerms} /></strong>;
        if (p === '→' || p === '->' || p === '⇒') return <span key={i} className="ms-src-arrow" aria-hidden>→</span>;
        return <React.Fragment key={i}><Marked text={p} terms={terms} answerTerms={answerTerms} /></React.Fragment>;
      })}
    </>
  );
};

export const SourceText: React.FC<{
  text: string;
  /** Vurgulanacak terimler (katlanmış ya da düz; içeride katlanır) */
  terms?: string[];
  /** Doğru şık ifadeleri: yeşil işaretlenir */
  answerTerms?: string[];
  size?: 'sm' | 'md';
  className?: string;
  /** Düz anlatım paragraflarını sesli ders metnindeki gibi giriş + (iç içe) maddelere ayır */
  maddele?: boolean;
}> = ({ text, terms, answerTerms, size = 'md', className = '', maddele = false }) => {
  const blocks = useMemo(() => parseSourceText(text, !maddele), [text, maddele]);
  const fold = (l?: string[]) => (l || []).map((t) => foldText(String(t || '').trim())).filter((t) => t.length >= 2);
  const folded = useMemo(() => fold(terms), [terms]);
  const ans = useMemo(() => fold(answerTerms), [answerTerms]);
  if (!blocks.length) return null;
  return (
    <div className={`ms-src ${size === 'sm' ? 'is-sm' : ''} ${className}`}>
      {blocks.map((b, i) => {
        if (b.kind === 'h') return <h5 key={i} className="ms-src-h"><Marked text={b.text} terms={folded} answerTerms={ans} /></h5>;
        if (b.kind === 'note')
          return (
            <p key={i} className="ms-src-note">
              <span className="ms-src-note-label">{b.label.charAt(0).toLocaleUpperCase('tr-TR') + b.label.slice(1)}</span>
              <Inline text={b.text} terms={folded} answerTerms={ans} lead={false} />
            </p>
          );
        if (b.kind === 'li')
          return (
            <ul key={i} className={`ms-src-list ${b.ordered ? 'is-ordered' : ''}`}>
              {b.items.map((it, j) => (
                <li key={j} className={it.dz ? `is-dz${it.dz}` : undefined} style={it.dz ? { marginInlineStart: `${it.dz * 1.15}em` } : undefined}>
                  <span className="ms-src-mark" aria-hidden>{it.mark ? `${it.mark}.` : ['•', '◦', '▪'][it.dz || 0]}</span>
                  <span className="min-w-0"><Inline text={it.text} terms={folded} answerTerms={ans} /></span>
                </li>
              ))}
            </ul>
          );
        const md = maddele ? maddeleMetin(b.text) : null;
        if (md)
          return (
            <div key={i} className="ms-src-p ms-src-md">
              {md.map((m, j) => (
                <span key={j} className={m.d === 0 ? 'ms-md-giris' : m.d === 2 ? 'ms-md-madde is-alt' : 'ms-md-madde'}>
                  <Inline text={m.t} terms={folded} answerTerms={ans} lead={m.d === 0} />
                </span>
              ))}
            </div>
          );
        return <p key={i} className="ms-src-p"><Inline text={b.text} terms={folded} answerTerms={ans} /></p>;
      })}
    </div>
  );
};
