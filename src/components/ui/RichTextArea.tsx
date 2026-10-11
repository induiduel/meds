import React, { useRef, useState } from 'react';
import { Bold, Italic, Highlighter, Heading2, List, ListOrdered, IndentIncrease, IndentDecrease, Table2, MessageSquareWarning, GraduationCap, Palette } from 'lucide-react';
import { Segmented } from './kit';
import { NoteMarkdown, NOTE_COLORS, NoteColor } from './NoteMarkdown';

/**
 * Biçimli metin alanı (v8). Metin düz Markdown olarak saklanır ve SourceText ile aynı kurallarla gösterilir:
 * `## başlık`, `- madde`, `1. numaralı`, `**kalın**`, `Not: …`, `Sınav: …` satırları.
 *  - Araç çubuğu seçimi sarar ya da satır başına işaret koyar; tekrar basınca kaldırır.
 *  - Ctrl/⌘+B kalın; Enter liste satırını sürdürür, boş madde satırında listeden çıkar.
 *  - Telefonda araç çubuğu klavyenin üstüne yapışır (sticky bottom).
 *  - "Önizle" yazılanı okuma görünümünde gösterir.
 *  - Yeniden kurulum (2026-10-11): italik, ==vurgu==, renkli metin, iç içe girinti (Tab / Shift+Tab),
 *    tablo ekleme. Gösterim `NoteMarkdown` ile yapılır.
 */
type Mode = 'write' | 'preview';

const LINE_MARKS = [
  { id: 'h', re: /^##\s+/, mark: '## ' },
  { id: 'ul', re: /^(\s*)-\s+/, mark: '- ' },
  { id: 'ol', re: /^(\s*)\d+[.)]\s+/, mark: '1. ' },
  { id: 'note', re: /^Not:\s*/i, mark: 'Not: ' },
  { id: 'exam', re: /^Sınav:\s*/i, mark: 'Sınav: ' },
] as const;

export const RichTextArea: React.FC<{
  id: string;
  value: string;
  onChange: (v: string) => void;
  placeholder?: string;
  mode: Mode;
  onModeChange: (m: Mode) => void;
  minRows?: number;
  label: string;
}> = ({ id, value, onChange, placeholder, mode, onModeChange, label }) => {
  const ref = useRef<HTMLTextAreaElement>(null);

  const apply = (next: string, selStart: number, selEnd: number) => {
    onChange(next);
    requestAnimationFrame(() => {
      const t = ref.current;
      if (!t) return;
      t.focus();
      t.setSelectionRange(selStart, selEnd);
    });
  };

  const [colorOpen, setColorOpen] = useState(false);

  const wrap = (mark: string, close: string = mark, placeholder = 'metin') => {
    const t = ref.current;
    if (!t) return;
    const { selectionStart: a, selectionEnd: b } = t;
    const sel = value.slice(a, b);
    const before = value.slice(0, a);
    const after = value.slice(b);
    // Zaten sarılıysa kaldır
    if (before.endsWith(mark) && after.startsWith(close)) {
      apply(before.slice(0, -mark.length) + sel + after.slice(close.length), a - mark.length, b - mark.length);
      return;
    }
    const inner = sel || placeholder;
    apply(before + mark + inner + close + after, a + mark.length, a + mark.length + inner.length);
  };

  /** Seçili satırların girintisini 2 boşluk artırır/azaltır (iç içe madde). */
  const indent = (dir: 1 | -1) => {
    const t = ref.current;
    if (!t) return;
    const { selectionStart: a, selectionEnd: b } = t;
    const start = value.lastIndexOf('\n', a - 1) + 1;
    const endIdx = value.indexOf('\n', b);
    const end = endIdx === -1 ? value.length : endIdx;
    const lines = value.slice(start, end).split('\n');
    let firstDelta = 0;
    const next = lines.map((l, i) => {
      if (dir === 1) { if (i === 0) firstDelta = 2; return '  ' + l; }
      const cut = l.startsWith('  ') ? 2 : l.startsWith('\t') || l.startsWith(' ') ? 1 : 0;
      if (i === 0) firstDelta = -cut;
      return l.slice(cut);
    });
    const joined = next.join('\n');
    apply(value.slice(0, start) + joined + value.slice(end), Math.max(start, a + firstDelta), start + joined.length);
  };

  const insertTable = () => {
    const t = ref.current;
    if (!t) return;
    const a = t.selectionStart;
    const lineStart = value.lastIndexOf('\n', a - 1) + 1;
    const atLineStart = value.slice(lineStart, a).trim() === '';
    const tpl = '| Başlık | Başlık |\n|---|---|\n| Hücre | Hücre |\n| Hücre | Hücre |\n';
    const pre = atLineStart ? '' : '\n\n';
    const ins = pre + tpl;
    const sel = a + pre.length + 2;
    apply(value.slice(0, a) + ins + value.slice(a), sel, sel + 'Başlık'.length);
  };

  const toggleLine = (kind: (typeof LINE_MARKS)[number]['id']) => {
    const t = ref.current;
    if (!t) return;
    const { selectionStart: a, selectionEnd: b } = t;
    const start = value.lastIndexOf('\n', a - 1) + 1;
    const endIdx = value.indexOf('\n', b);
    const end = endIdx === -1 ? value.length : endIdx;
    const lines = value.slice(start, end).split('\n');
    const spec = LINE_MARKS.find((m) => m.id === kind)!;
    const allHave = lines.every((l) => spec.re.test(l));
    let n = 0;
    const next = lines.map((l) => {
      // Başka bir satır işaretini önce temizle
      const lead = (l.match(/^\s*/) || [''])[0];
      let base = l.slice(lead.length);
      for (const m of LINE_MARKS) base = base.replace(m.re, '');
      if (allHave) return lead + base;
      n += 1;
      return lead + (kind === 'ol' ? `${n}. ` : spec.mark) + base;
    });
    const joined = next.join('\n');
    apply(value.slice(0, start) + joined + value.slice(end), start, start + joined.length);
  };

  const onKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'b') {
      e.preventDefault();
      wrap('**', '**', 'kalın');
      return;
    }
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'i') {
      e.preventDefault();
      wrap('*', '*', 'italik');
      return;
    }
    if ((e.metaKey || e.ctrlKey) && e.shiftKey && e.key.toLowerCase() === 'h') {
      e.preventDefault();
      wrap('==', '==', 'vurgu');
      return;
    }
    if (e.key === 'Tab') {
      const line = value.slice(value.lastIndexOf('\n', e.currentTarget.selectionStart - 1) + 1);
      // Liste satırında ya da çok satırlı seçimde sekme girinti yapar; diğer durumda odak normal ilerler.
      if (/^\s*(-|\d+[.)])\s/.test(line) || e.currentTarget.selectionStart !== e.currentTarget.selectionEnd) {
        e.preventDefault();
        indent(e.shiftKey ? -1 : 1);
      }
      return;
    }
    if (e.key !== 'Enter' || e.shiftKey) return;
    const t = e.currentTarget;
    const a = t.selectionStart;
    if (a !== t.selectionEnd) return;
    const start = value.lastIndexOf('\n', a - 1) + 1;
    const line = value.slice(start, a);
    const m = line.match(/^(\s*)(-\s+|(\d+)[.)]\s+)(.*)$/);
    if (!m) return;
    e.preventDefault();
    if (!m[4].trim()) {
      // Boş madde: girintiliyse bir düzey çık, değilse listeden çık
      if (m[1].length >= 2) {
        apply(value.slice(0, start) + line.slice(2) + value.slice(a), a - 2, a - 2);
        return;
      }
      apply(value.slice(0, start) + value.slice(a), start, start);
      return;
    }
    const mark = m[3] ? `${Number(m[3]) + 1}. ` : '- ';
    const ins = '\n' + m[1] + mark;
    apply(value.slice(0, a) + ins + value.slice(a), a + ins.length, a + ins.length);
  };

  const tools: { icon: React.ElementType; label: string; run: () => void; kbd?: string }[] = [
    { icon: Bold, label: 'Kalın', run: () => wrap('**', '**', 'kalın'), kbd: 'Ctrl+B' },
    { icon: Italic, label: 'İtalik', run: () => wrap('*', '*', 'italik'), kbd: 'Ctrl+I' },
    { icon: Highlighter, label: 'Fosforlu vurgu', run: () => wrap('==', '==', 'vurgu'), kbd: 'Ctrl+Shift+H' },
    { icon: Heading2, label: 'Başlık', run: () => toggleLine('h') },
    { icon: List, label: 'Madde', run: () => toggleLine('ul') },
    { icon: ListOrdered, label: 'Numaralı', run: () => toggleLine('ol') },
    { icon: IndentIncrease, label: 'Girintiyi artır', run: () => indent(1), kbd: 'Tab' },
    { icon: IndentDecrease, label: 'Girintiyi azalt', run: () => indent(-1), kbd: 'Shift+Tab' },
    { icon: Table2, label: 'Tablo ekle', run: insertTable },
    { icon: MessageSquareWarning, label: 'Not kutusu', run: () => toggleLine('note') },
    { icon: GraduationCap, label: 'Sınav spotu', run: () => toggleLine('exam') },
  ];

  return (
    <div className="rt">
      <div className="rt-bar" role="toolbar" aria-label="Biçim">
        {mode === 'write' &&
          tools.map(({ icon: Icon, label: l, run, kbd }) => (
            <button
              key={l}
              type="button"
              className="rt-tool"
              onMouseDown={(e) => e.preventDefault()}
              onClick={run}
              title={kbd ? `${l} (${kbd})` : l}
              aria-label={l}
            >
              <Icon />
            </button>
          ))}
        {mode === 'write' && (
          <span className="rt-color">
            <button
              type="button"
              className="rt-tool"
              onMouseDown={(e) => e.preventDefault()}
              onClick={() => setColorOpen((v) => !v)}
              aria-expanded={colorOpen}
              aria-label="Metin rengi"
              title="Metin rengi"
            >
              <Palette />
            </button>
            {colorOpen && (
              <span className="rt-swatches" role="group" aria-label="Renk seç">
                {NOTE_COLORS.map((c: NoteColor) => (
                  <button
                    key={c}
                    type="button"
                    className={`rt-swatch nm-sw-${c}`}
                    onMouseDown={(e) => e.preventDefault()}
                    onClick={() => { wrap(`[${c}]`, '[/]', 'renkli'); setColorOpen(false); }}
                    aria-label={`${c} renk`}
                    title={c}
                  />
                ))}
              </span>
            )}
          </span>
        )}
        <span className="rt-sp" />
        <Segmented<Mode>
          className="rt-mode"
          label="Düzenleyici kipi"
          value={mode}
          onChange={onModeChange}
          options={[
            { value: 'write', label: 'Yaz' },
            { value: 'preview', label: 'Önizle' },
          ]}
        />
      </div>
      {mode === 'write' ? (
        <>
          <label className="sr-only" htmlFor={id}>{label}</label>
          <textarea
            id={id}
            ref={ref}
            className="rt-area"
            value={value}
            onChange={(e) => onChange(e.target.value)}
            onKeyDown={onKeyDown}
            placeholder={placeholder}
          />
        </>
      ) : (
        <div className="rt-preview" aria-label={`${label} önizlemesi`}>
          {value.trim() ? <NoteMarkdown text={value} /> : <p className="ui-hint">Önizlenecek bir şey yok.</p>}
        </div>
      )}
    </div>
  );
};
