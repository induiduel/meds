import React from 'react';

/**
 * Not defteri ve Öğren notları için biçimli metin gösterimi. Metin düz Markdown olarak saklanır:
 *  - `# başlık`, `## alt başlık`
 *  - `- madde`, `1. numaralı`; her 2 boşluk (ya da sekme) girinti bir alt düzey açar
 *  - `| a | b |` satırları tablo; `|---|---|` ayırıcı satırı başlığı belirler
 *  - `Not: …`, `Sınav: …` vurgu kutuları
 *  - satır içi: `**kalın**`, `*italik*`, `==vurgu==`, `[kırmızı]metin[/]` (kırmızı, yeşil, mavi, turuncu, mor)
 * HTML kabul edilmez; her şey React düğümü olarak üretilir (XSS yok).
 */

export const NOTE_COLORS = ['kırmızı', 'yeşil', 'mavi', 'turuncu', 'mor'] as const;
export type NoteColor = (typeof NOTE_COLORS)[number];
const COLOR_CLASS: Record<NoteColor, string> = {
  kırmızı: 'nm-c-red',
  yeşil: 'nm-c-green',
  mavi: 'nm-c-blue',
  turuncu: 'nm-c-orange',
  mor: 'nm-c-purple',
};

const INLINE = /(\*\*[^*\n]+\*\*|==[^=\n]+==|\*[^*\s\n][^*\n]*\*|\[(?:kırmızı|yeşil|mavi|turuncu|mor)\][^\n]*?\[\/\])/g;

export const NoteInline: React.FC<{ text: string }> = ({ text }) => {
  const parts = text.split(INLINE).filter((p) => p !== '' && p !== undefined);
  return (
    <>
      {parts.map((p, i) => {
        if (/^\*\*[^*]+\*\*$/.test(p)) return <strong key={i}><NoteInline text={p.slice(2, -2)} /></strong>;
        if (/^==[^=]+==$/.test(p)) return <mark key={i} className="nm-mark"><NoteInline text={p.slice(2, -2)} /></mark>;
        if (/^\*[^*]+\*$/.test(p)) return <em key={i}><NoteInline text={p.slice(1, -1)} /></em>;
        const c = p.match(/^\[(kırmızı|yeşil|mavi|turuncu|mor)\]([\s\S]*)\[\/\]$/);
        if (c) return <span key={i} className={COLOR_CLASS[c[1] as NoteColor]}><NoteInline text={c[2]} /></span>;
        return <React.Fragment key={i}>{p}</React.Fragment>;
      })}
    </>
  );
};

type ListItem = { text: string; ordered: boolean; children: ListItem[] };
type Block =
  | { kind: 'h'; level: 1 | 2; text: string }
  | { kind: 'p'; text: string }
  | { kind: 'list'; items: ListItem[]; ordered: boolean }
  | { kind: 'table'; head: string[] | null; rows: string[][] }
  | { kind: 'note'; tone: 'note' | 'exam'; text: string };

const LIST = /^((?: {2}|\t)*)(-|\*|\d+[.)])\s+(.*)$/;
const indentOf = (s: string) => s.replace(/\t/g, '  ').length / 2;
const cells = (line: string) => line.trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map((c) => c.trim());

export function parseNoteMarkdown(raw: string): Block[] {
  const lines = String(raw || '').replace(/\r/g, '').split('\n');
  const blocks: Block[] = [];
  let para: string[] = [];
  const flush = () => {
    if (para.length) blocks.push({ kind: 'p', text: para.join(' ') });
    para = [];
  };
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const t = line.trim();
    if (!t) { flush(); continue; }
    const h = t.match(/^(#{1,3})\s+(.+)$/);
    if (h) { flush(); blocks.push({ kind: 'h', level: h[1].length === 1 ? 1 : 2, text: h[2] }); continue; }
    const note = t.match(/^(not|sınav)\s*:\s*(.*)$/i);
    if (note) { flush(); blocks.push({ kind: 'note', tone: /^s/i.test(note[1]) ? 'exam' : 'note', text: note[2] }); continue; }
    if (t.startsWith('|')) {
      flush();
      const rows: string[][] = [];
      let head: string[] | null = null;
      while (i < lines.length && lines[i].trim().startsWith('|')) {
        const r = lines[i].trim();
        if (/^\|?\s*:?-{2,}/.test(r)) {
          if (rows.length === 1 && !head) head = rows.pop()!;
        } else rows.push(cells(r));
        i++;
      }
      i--;
      blocks.push({ kind: 'table', head, rows });
      continue;
    }
    const m = line.match(LIST);
    if (m) {
      flush();
      // Ardışık liste satırlarını girintiye göre ağaçlaştır
      const root: ListItem[] = [];
      const stack: { depth: number; list: ListItem[] }[] = [{ depth: -1, list: root }];
      const firstOrdered = /\d/.test(m[2]);
      while (i < lines.length) {
        const lm = lines[i].match(LIST);
        if (!lm) break;
        const depth = indentOf(lm[1]);
        const item: ListItem = { text: lm[3], ordered: /\d/.test(lm[2]), children: [] };
        while (stack.length > 1 && stack[stack.length - 1].depth >= depth) stack.pop();
        const parentList = stack[stack.length - 1].list;
        parentList.push(item);
        stack.push({ depth, list: item.children });
        i++;
      }
      i--;
      blocks.push({ kind: 'list', items: root, ordered: firstOrdered });
      continue;
    }
    para.push(t);
  }
  flush();
  return blocks;
}

const ListView: React.FC<{ items: ListItem[]; ordered: boolean }> = ({ items, ordered }) => {
  const Tag = ordered ? 'ol' : 'ul';
  return (
    <Tag className="nm-list">
      {items.map((it, i) => (
        <li key={i}>
          <NoteInline text={it.text} />
          {it.children.length > 0 && <ListView items={it.children} ordered={it.children[0].ordered} />}
        </li>
      ))}
    </Tag>
  );
};

export const NoteMarkdown: React.FC<{ text: string; className?: string }> = ({ text, className = '' }) => {
  const blocks = parseNoteMarkdown(text);
  return (
    <div className={`nm ${className}`}>
      {blocks.map((b, i) => {
        if (b.kind === 'h') return b.level === 1 ? <h3 key={i} className="nm-h1"><NoteInline text={b.text} /></h3> : <h4 key={i} className="nm-h2"><NoteInline text={b.text} /></h4>;
        if (b.kind === 'p') return <p key={i}><NoteInline text={b.text} /></p>;
        if (b.kind === 'list') return <ListView key={i} items={b.items} ordered={b.ordered} />;
        if (b.kind === 'note')
          return (
            <p key={i} className={`nm-note ${b.tone === 'exam' ? 'is-exam' : ''}`}>
              <b>{b.tone === 'exam' ? 'Sınav' : 'Not'}</b> <NoteInline text={b.text} />
            </p>
          );
        return (
          <div key={i} className="nm-table-wrap">
            <table className="nm-table">
              {b.head && (
                <thead><tr>{b.head.map((c, j) => <th key={j}><NoteInline text={c} /></th>)}</tr></thead>
              )}
              <tbody>
                {b.rows.map((r, ri) => <tr key={ri}>{r.map((c, j) => <td key={j}><NoteInline text={c} /></td>)}</tr>)}
              </tbody>
            </table>
          </div>
        );
      })}
    </div>
  );
};
