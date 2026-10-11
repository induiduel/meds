import React, { useId, useMemo, useRef, useState } from 'react';
import { Plus, X } from 'lucide-react';

/**
 * Etiket girişi (v8). Enter, virgül ya da Sekme çip yapar; ⌫ boş alanda son çipi seçer, ikinci ⌫ siler.
 * Öneriler var olan etiketlerden gelir (↑/↓ + Enter). Aynı etiket eklenmez: var olan çip kısaca sallanır.
 */
const norm = (t: string) => t.trim().replace(/\s+/g, ' ').replace(/^#/, '').slice(0, 32);

export const TagInput: React.FC<{
  value: string[];
  onChange: (tags: string[]) => void;
  suggestions?: string[];
  label: string;
  placeholder?: string;
  max?: number;
}> = ({ value, onChange, suggestions = [], label, placeholder = 'Etiket ekle', max = 12 }) => {
  const id = useId();
  const [text, setText] = useState('');
  const [armed, setArmed] = useState(false);
  const [shake, setShake] = useState<string | null>(null);
  const [cursor, setCursor] = useState(-1);
  const [focus, setFocus] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const lower = (s: string) => s.toLocaleLowerCase('tr-TR');

  const options = useMemo(() => {
    const q = lower(norm(text));
    const have = new Set(value.map(lower));
    return [...new Set(suggestions)].filter((s) => !have.has(lower(s)) && (!q || lower(s).includes(q))).slice(0, 6);
  }, [text, suggestions, value]);

  const add = (raw: string) => {
    const t = norm(raw);
    if (!t) return;
    const dup = value.find((v) => lower(v) === lower(t));
    if (dup) {
      setShake(dup);
      window.setTimeout(() => setShake(null), 400);
      setText('');
      return;
    }
    if (value.length >= max) return;
    onChange([...value, t]);
    setText('');
    setCursor(-1);
  };

  const onKey = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'ArrowDown' && options.length) {
      e.preventDefault();
      setCursor((c) => (c + 1) % options.length);
      return;
    }
    if (e.key === 'ArrowUp' && options.length) {
      e.preventDefault();
      setCursor((c) => (c <= 0 ? options.length - 1 : c - 1));
      return;
    }
    if (e.key === 'Enter' || e.key === ',' || (e.key === 'Tab' && text.trim())) {
      if (e.key === 'Tab' && !text.trim()) return;
      e.preventDefault();
      add(cursor >= 0 && options[cursor] ? options[cursor] : text);
      return;
    }
    if (e.key === 'Backspace' && !text && value.length) {
      if (armed) {
        onChange(value.slice(0, -1));
        setArmed(false);
      } else setArmed(true);
      return;
    }
    if (e.key === 'Escape') {
      setText('');
      setCursor(-1);
    }
    setArmed(false);
  };

  return (
    <div className={`tg ${focus ? 'is-focus' : ''}`} onClick={() => inputRef.current?.focus()}>
      <ul className="tg-list" aria-label={label}>
        {value.map((t, i) => (
          <li key={t} className={`tg-chip ${shake === t ? 'is-shake' : ''} ${armed && i === value.length - 1 ? 'is-armed' : ''}`}>
            <span>#{t}</span>
            <button type="button" aria-label={`${t} etiketini kaldır`} onClick={(e) => { e.stopPropagation(); onChange(value.filter((v) => v !== t)); }}>
              <X />
            </button>
          </li>
        ))}
        <li className="tg-input">
          <label className="sr-only" htmlFor={id}>{label}</label>
          <input
            id={id}
            ref={inputRef}
            value={text}
            onChange={(e) => { setText(e.target.value.replace(',', '')); setArmed(false); setCursor(-1); }}
            onKeyDown={onKey}
            onFocus={() => setFocus(true)}
            onBlur={() => window.setTimeout(() => setFocus(false), 120)}
            placeholder={value.length ? '' : placeholder}
            disabled={value.length >= max}
            role="combobox"
            aria-expanded={focus && options.length > 0}
            aria-controls={`${id}-l`}
            autoComplete="off"
          />
        </li>
      </ul>
      {focus && (options.length > 0 || text.trim()) && (
        <ul id={`${id}-l`} role="listbox" className="tg-pop" onMouseDown={(e) => e.preventDefault()}>
          {text.trim() && !options.some((o) => lower(o) === lower(norm(text))) && (
            <li role="option" aria-selected={cursor === -1} className={cursor === -1 ? 'is-on' : ''} onClick={() => add(text)}>
              <Plus /> “{norm(text)}” ekle
            </li>
          )}
          {options.map((o, i) => (
            <li key={o} role="option" aria-selected={cursor === i} className={cursor === i ? 'is-on' : ''} onClick={() => add(o)}>
              #{o}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};
