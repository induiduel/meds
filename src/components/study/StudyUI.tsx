import React from 'react';
import { parseExplanation } from '../QuestionCard';
import { OptionKey, StudyQuestion } from '../../services/studyStore';

/** Segmented control (single choice). */
export function Segmented<T extends string | number>({
  value,
  options,
  onChange,
  label,
  size = 'md',
}: {
  value: T;
  options: { value: T; label: React.ReactNode }[];
  onChange: (v: T) => void;
  label: string;
  size?: 'sm' | 'md';
}) {
  return (
    <div role="radiogroup" aria-label={label} className="inline-flex gap-1 bg-canvas rounded-[10px] p-[3px] max-w-full overflow-x-auto no-scrollbar">
      {options.map((o) => {
        const on = o.value === value;
        return (
          <button
            key={String(o.value)}
            type="button"
            role="radio"
            aria-checked={on}
            onClick={() => onChange(o.value)}
            className={`shrink-0 whitespace-nowrap rounded-lg cursor-pointer ${size === 'sm' ? 'h-8 px-2.5 text-[13px]' : 'h-9 px-3 text-[14px]'} ${
              on ? 'bg-white font-semibold shadow-xs text-ink' : 'text-ink-2 hover:text-ink'
            }`}
          >
            {o.label}
          </button>
        );
      })}
    </div>
  );
}

export const Field: React.FC<{ label: string; children: React.ReactNode; className?: string }> = ({ label, children, className = '' }) => (
  <label className={`flex flex-col gap-1.5 text-[13px] font-semibold text-ink-2 ${className}`}>
    {label}
    {children}
  </label>
);

export const selectCls = 'h-10 border border-line-2 rounded-[10px] px-3 text-[14px] font-normal text-ink bg-white cursor-pointer min-w-0';
export const cardCls = 'bg-white border border-line rounded-2xl';
export const btnPrimary =
  'h-10 px-4 rounded-[10px] bg-accent hover:bg-accent-hover text-white text-[14px] font-semibold inline-flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed';
export const btnSecondary =
  'h-10 px-3.5 rounded-[10px] border border-line-2 bg-white text-ink text-[14px] font-semibold inline-flex items-center justify-center gap-2 cursor-pointer hover:border-ink-3 disabled:opacity-50 disabled:cursor-not-allowed';
export const btnGhost = 'h-10 px-3 rounded-[10px] text-ink-2 hover:text-ink hover:bg-canvas text-[14px] font-semibold inline-flex items-center gap-2 cursor-pointer';

/** One answer option; state decides colour. */
export const OptionButton: React.FC<{
  opt: { key: OptionKey; text: string };
  state: 'idle' | 'selected' | 'correct' | 'wrong' | 'muted';
  onClick?: () => void;
  disabled?: boolean;
  tag?: string;
}> = ({ opt, state, onClick, disabled, tag }) => {
  const box = {
    idle: 'border border-line bg-white hover:border-line-2',
    selected: 'border-[1.5px] border-accent bg-accent-soft',
    correct: 'border-[1.5px] border-ok-bright bg-ok-tint',
    wrong: 'border-[1.5px] border-bad bg-bad-soft',
    muted: 'border border-line bg-white opacity-70',
  }[state];
  const key = {
    idle: 'bg-canvas text-ink',
    selected: 'bg-accent text-white',
    correct: 'bg-ok text-white',
    wrong: 'bg-bad text-white',
    muted: 'bg-canvas text-ink-2',
  }[state];
  const tagCls = state === 'correct' ? 'text-ok' : state === 'wrong' ? 'text-bad-text' : 'text-accent';
  return (
    <button
      type="button"
      role="radio"
      aria-checked={state === 'selected' || state === 'wrong' || (state === 'correct' && tag === 'Senin cevabın')}
      onClick={onClick}
      disabled={disabled}
      className={`w-full flex items-center gap-3 min-h-[48px] px-3 py-2 rounded-xl text-[15px] leading-snug text-left transition-colors ${box} ${
        disabled ? 'cursor-default' : 'cursor-pointer'
      }`}
    >
      <span className={`w-8 h-8 shrink-0 rounded-lg flex items-center justify-center font-mono text-[13px] ${key}`}>{opt.key}</span>
      <span className="flex-1 min-w-0 break-words">{opt.text}</span>
      {tag && <span className={`text-[12px] font-semibold whitespace-nowrap ${tagCls}`}>{tag}</span>}
    </button>
  );
};

/** Compact explanation: labelled sections when the redactor wrote them. */
export const ExplanationBlock: React.FC<{ q: StudyQuestion; compact?: boolean }> = ({ q, compact }) => {
  if (!q.explanation) {
    return <p className="m-0 text-[14px] text-ink-2">Bu soru için açıklama henüz yazılmadı.</p>;
  }
  const sections = parseExplanation(q.explanation, q.answer);
  return (
    <div className="flex flex-col gap-3">
      {sections.map((s, i) => (
        <div key={i} className={sections.length > 1 ? 'grid grid-cols-1 sm:grid-cols-[120px_minmax(0,1fr)] gap-1 sm:gap-4' : ''}>
          {sections.length > 1 && <div className="text-[12px] font-semibold uppercase tracking-[0.06em] text-ink-2 pt-0.5">{s.label}</div>}
          <p
            className={`m-0 whitespace-pre-line leading-[1.6] ${compact ? 'text-[14px]' : 'text-[15px]'} ${
              s.pearl ? 'px-3 py-2.5 rounded-lg bg-accent-soft' : ''
            }`}
          >
            {s.body}
          </p>
        </div>
      ))}
    </div>
  );
};

export const EmptyState: React.FC<{ title: string; body?: string; action?: React.ReactNode }> = ({ title, body, action }) => (
  <div className={`${cardCls} px-6 py-12 text-center flex flex-col items-center gap-3`}>
    <h3 className="m-0 font-display text-[20px] font-bold tracking-[-0.02em]">{title}</h3>
    {body && <p className="m-0 text-[14px] text-ink-2 max-w-[420px]">{body}</p>}
    {action}
  </div>
);

export const formatDuration = (sec: number) => {
  const h = Math.floor(sec / 3600);
  const m = Math.floor((sec % 3600) / 60);
  const s = sec % 60;
  return h > 0 ? `${h}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}` : `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
};

export const isTypingTarget = (t: EventTarget | null) => {
  const el = t as HTMLElement | null;
  return !!el && (['INPUT', 'TEXTAREA', 'SELECT'].includes(el.tagName) || el.isContentEditable);
};
