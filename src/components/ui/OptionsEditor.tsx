import React, { useEffect, useRef } from 'react';
import { Plus, X, Check } from 'lucide-react';

export type OptionKey = 'A' | 'B' | 'C' | 'D' | 'E';
export const OPTION_KEYS: OptionKey[] = ['A', 'B', 'C', 'D', 'E'];

export interface OptionsEditorProps {
  /** Option texts; only keys in `visible` are shown */
  options: Record<OptionKey, string>;
  onChange: (key: OptionKey, text: string) => void;
  /** How many rows are shown (1–5); rows grow with the (+) button */
  count: number;
  onCountChange: (n: number) => void;
  /** The option the student remembers as correct */
  answer?: OptionKey;
  onAnswerChange: (key: OptionKey | undefined) => void;
  /** Optional "why" note that opens under the list once an answer is picked */
  reason?: string;
  onReasonChange?: (text: string) => void;
}

/**
 * Option list that starts with one row. "+ Şık ekle" adds the next letter;
 * tapping a letter marks that option as the correct answer and opens a "Neden?" note.
 */
export const OptionsEditor: React.FC<OptionsEditorProps> = ({
  options,
  onChange,
  count,
  onCountChange,
  answer,
  onAnswerChange,
  reason = '',
  onReasonChange,
}) => {
  const keys = OPTION_KEYS.slice(0, Math.max(1, Math.min(5, count)));
  const lastAdded = useRef<OptionKey | null>(null);
  const inputs = useRef<Partial<Record<OptionKey, HTMLInputElement | null>>>({});

  // Focus a freshly added row
  useEffect(() => {
    const k = lastAdded.current;
    if (k) {
      inputs.current[k]?.focus();
      lastAdded.current = null;
    }
  }, [count]);

  const add = () => {
    if (count >= 5) return;
    lastAdded.current = OPTION_KEYS[count];
    onCountChange(count + 1);
  };

  /** Removing a row shifts the following texts up so letters stay contiguous. */
  const remove = (k: OptionKey) => {
    const idx = OPTION_KEYS.indexOf(k);
    for (let i = idx; i < count - 1; i++) onChange(OPTION_KEYS[i], options[OPTION_KEYS[i + 1]]);
    onChange(OPTION_KEYS[count - 1], '');
    if (answer) {
      const ai = OPTION_KEYS.indexOf(answer);
      if (ai === idx) onAnswerChange(undefined);
      else if (ai > idx) onAnswerChange(OPTION_KEYS[ai - 1]);
    }
    onCountChange(Math.max(1, count - 1));
  };

  return (
    <div className="flex flex-col gap-1.5">
      <p className="m-0 px-0.5 text-[12.5px] text-ink-3">Doğru olduğunu düşündüğün şıkkın harfine dokun.</p>
      {keys.map((k) => {
        const on = answer === k;
        return (
          <div
            key={k}
            className={`ms-pop-in flex items-center gap-2 h-12 pl-1.5 pr-1.5 rounded-xl border transition-colors ${
              on ? 'bg-ok-tint border-emerald-400' : 'bg-field border-transparent focus-within:border-accent focus-within:bg-white'
            }`}
          >
            <button
              type="button"
              onClick={() => onAnswerChange(on ? undefined : k)}
              aria-pressed={on}
              aria-label={on ? `${k} doğru cevap olarak işaretli, kaldırmak için dokun` : `${k} şıkkını doğru cevap olarak işaretle`}
              title={on ? 'Doğru cevap' : 'Doğru cevap olarak işaretle'}
              className={`w-9 h-9 rounded-[10px] flex items-center justify-center font-mono text-[14px] font-semibold shrink-0 cursor-pointer transition-all ${
                on ? 'bg-ok text-white shadow-sm' : 'bg-white border border-line text-ink-2 hover:border-ok hover:text-ok'
              }`}
            >
              {on ? <Check className="w-4 h-4" strokeWidth={3} /> : k}
            </button>
            <input
              ref={(el) => {
                inputs.current[k] = el;
              }}
              type="text"
              value={options[k]}
              onChange={(e) => onChange(k, e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault();
                  if (k === keys[keys.length - 1] && options[k].trim()) add();
                }
              }}
              placeholder={`${k} şıkkı`}
              aria-label={`${k} şıkkı`}
              className="flex-1 min-w-0 bg-transparent border-0 outline-0 text-[16px] sm:text-[15px] placeholder:text-slate-600"
            />
            {on && <span className="hidden sm:inline text-[12px] font-semibold text-ok pr-1">Doğru</span>}
            {count > 1 && (
              <button
                type="button"
                onClick={() => remove(k)}
                aria-label={`${k} şıkkını kaldır`}
                className="w-8 h-8 rounded-lg flex items-center justify-center text-ink-3 hover:text-ink hover:bg-white cursor-pointer shrink-0"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>
        );
      })}

      {count < 5 && (
        <button
          type="button"
          onClick={add}
          className="self-start h-10 pl-2 pr-3.5 rounded-xl border border-dashed border-line-2 text-[14px] font-semibold text-accent inline-flex items-center gap-2 cursor-pointer hover:border-accent hover:bg-accent-soft/50 transition-colors"
        >
          <span className="w-6 h-6 rounded-full bg-accent text-white flex items-center justify-center">
            <Plus className="w-3.5 h-3.5" strokeWidth={2.6} />
          </span>
          {OPTION_KEYS[count]} şıkkını ekle
        </button>
      )}

      {answer && onReasonChange && (
        <div className="ms-pop-in mt-1 rounded-xl bg-ok-tint border border-emerald-200 p-3 flex flex-col gap-2">
          <label htmlFor="answer-reason" className="text-[13.5px] font-semibold text-ok">
            Neden {answer}? <span className="font-normal text-ink-3">Fikrini yaz (isteğe bağlı)</span>
          </label>
          <textarea
            id="answer-reason"
            rows={2}
            value={reason}
            onChange={(e) => onReasonChange(e.target.value)}
            placeholder="Örn. hoca derste bu bulguyu özellikle vurgulamıştı…"
            className="resize-none rounded-[10px] bg-white border border-transparent px-3 py-2.5 text-[15px] leading-[1.5] outline-0 focus:border-ok placeholder:text-slate-600"
          />
        </div>
      )}
    </div>
  );
};
