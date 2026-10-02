import React, { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { MoreHorizontal, X } from 'lucide-react';

export interface ActionItem {
  label: string;
  icon?: React.ElementType;
  onClick: () => void;
  /** Items with the same group are listed together, separated by a rule. */
  group?: string;
  tone?: 'default' | 'accent' | 'danger';
  disabled?: boolean;
  hint?: string;
}

interface ActionMenuProps {
  items: ActionItem[];
  /** Visible text on the trigger; omit for an icon-only "⋯" button. */
  label?: string;
  /** Accessible name and the sheet title on phones. */
  title?: string;
  className?: string;
}

const toneCls = {
  default: 'text-ink',
  accent: 'text-accent',
  danger: 'text-[#B4233C]',
};

/**
 * One "⋯ İşlemler" button that collects a card's secondary actions.
 * Desktop/tablet: anchored dropdown. Phones (<640px): bottom sheet, like a native app.
 */
export const ActionMenu: React.FC<ActionMenuProps> = ({ items, label, title = 'İşlemler', className = '' }) => {
  const [open, setOpen] = useState(false);
  const [isPhone, setIsPhone] = useState(() => typeof window !== 'undefined' && window.innerWidth < 640);
  const rootRef = useRef<HTMLDivElement>(null);
  const visible = items.filter(Boolean);

  useEffect(() => {
    if (!open) return;
    setIsPhone(window.innerWidth < 640);
    const onDown = (e: MouseEvent) => {
      const t = e.target as HTMLElement;
      if (t.closest?.('[data-action-sheet]')) return;
      if (rootRef.current && !rootRef.current.contains(t)) setOpen(false);
    };
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && setOpen(false);
    document.addEventListener('mousedown', onDown);
    document.addEventListener('keydown', onKey);
    return () => {
      document.removeEventListener('mousedown', onDown);
      document.removeEventListener('keydown', onKey);
    };
  }, [open]);

  if (visible.length === 0) return null;

  // Group consecutive items; a rule separates groups
  const groups: ActionItem[][] = [];
  visible.forEach((it) => {
    const last = groups[groups.length - 1];
    if (last && last[0].group === it.group) last.push(it);
    else groups.push([it]);
  });

  const run = (it: ActionItem) => {
    setOpen(false);
    it.onClick();
  };

  const list = (big: boolean) =>
    groups.map((g, gi) => (
      <div key={gi} className={gi > 0 ? (big ? 'mt-2' : 'border-t border-line-soft mt-1 pt-1') : ''}>
        {g[0].group && (
          <div className={`px-2.5 ${big ? 'pt-1 pb-1.5' : 'pt-1.5 pb-1'} text-[11.5px] font-semibold uppercase tracking-[0.06em] text-ink-3`}>{g[0].group}</div>
        )}
        <div className={big ? 'bg-canvas rounded-2xl overflow-hidden' : ''}>
          {g.map((it, i) => {
            const Icon = it.icon;
            return (
              <button
                key={it.label}
                type="button"
                role="menuitem"
                disabled={it.disabled}
                onClick={() => run(it)}
                className={`w-full flex items-center gap-3 text-left cursor-pointer disabled:opacity-50 ${toneCls[it.tone || 'default']} ${
                  big
                    ? `min-h-[52px] px-4 text-[15.5px] ${i > 0 ? 'border-t border-line' : ''}`
                    : 'min-h-[38px] px-2.5 rounded-[9px] text-[14px] hover:bg-canvas'
                }`}
              >
                {Icon && <Icon className={big ? 'w-5 h-5 shrink-0' : 'w-4 h-4 shrink-0 opacity-80'} />}
                <span className="flex-1 min-w-0 truncate">{it.label}</span>
                {it.hint && <span className="text-[12px] text-ink-3 shrink-0">{it.hint}</span>}
              </button>
            );
          })}
        </div>
      </div>
    ));

  return (
    <div className={`relative shrink-0 ${className}`} ref={rootRef}>
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        aria-haspopup="menu"
        aria-expanded={open}
        aria-label={label ? undefined : title}
        title={title}
        className={`h-9 rounded-[10px] border flex items-center justify-center gap-1.5 text-[13.5px] font-semibold text-ink cursor-pointer transition-colors ${
          label ? 'px-2.5' : 'w-9'
        } ${open ? 'bg-canvas border-line-2' : 'bg-white border-line hover:border-line-2'}`}
      >
        <MoreHorizontal className="w-[18px] h-[18px]" />
        {label && <span className="hidden sm:inline">{label}</span>}
      </button>

      {open &&
        (isPhone ? (
          createPortal(
            <div data-action-sheet className="fixed inset-0 z-[70]" role="dialog" aria-modal="true" aria-label={title}>
              <button type="button" aria-label="Kapat" onClick={() => setOpen(false)} className="absolute inset-0 bg-[rgba(14,26,38,0.4)] cursor-default" />
              <div
                role="menu"
                className="absolute left-0 right-0 bottom-0 max-h-[80dvh] overflow-y-auto bg-white rounded-t-[24px] px-4 pt-2 pb-[max(env(safe-area-inset-bottom),20px)] shadow-[0_-10px_40px_rgba(14,26,38,0.18)]"
              >
                <span className="block mx-auto w-10 h-[5px] rounded-full bg-line-2" aria-hidden="true" />
                <div className="flex items-center py-2">
                  <span className="flex-1 text-[18px] font-bold">{title}</span>
                  <button type="button" onClick={() => setOpen(false)} aria-label="Kapat" className="w-10 h-10 -mr-2 rounded-full flex items-center justify-center text-ink-2 cursor-pointer">
                    <X className="w-5 h-5" />
                  </button>
                </div>
                {list(true)}
              </div>
            </div>,
            document.body
          )
        ) : (
          <div
            role="menu"
            className="absolute right-0 top-11 z-40 w-[248px] bg-white border border-line rounded-[14px] p-1.5 shadow-[0_16px_40px_rgba(14,26,38,0.14)]"
          >
            {list(false)}
          </div>
        ))}
    </div>
  );
};
