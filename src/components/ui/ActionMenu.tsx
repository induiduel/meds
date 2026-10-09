import React, { useEffect, useLayoutEffect, useRef, useState } from 'react';
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
  /** Mavi tetikleyici ve önünde ikon: menüde öne çıkan bir şey var (ör. Öğren slaytı). */
  highlight?: { icon: React.ElementType; title: string };
}

const toneCls = {
  default: 'text-ink',
  accent: 'text-accent',
  danger: 'text-rose-700',
};

/**
 * One "⋯ İşlemler" button that collects a card's secondary actions.
 * Desktop/tablet: anchored dropdown. Phones (<640px): bottom sheet, like a native app.
 */
export const ActionMenu: React.FC<ActionMenuProps> = ({ items, label, title = 'İşlemler', className = '', highlight }) => {
  const [open, setOpen] = useState(false);
  const [isPhone, setIsPhone] = useState(() => typeof window !== 'undefined' && window.innerWidth < 640);
  const rootRef = useRef<HTMLDivElement>(null);
  const menuRef = useRef<HTMLDivElement>(null);
  const visible = items.filter(Boolean);
  // Masaüstü menüsü belgenin üst katmanına (portal) çizilir: kartların katmanları ya da taşma kırpması menüyü örtmez.
  // Düğmenin altında yer yoksa yukarı açılır; yükseklik ekrana sığacak kadar sınırlanır.
  const [pos, setPos] = useState<{ top?: number; bottom?: number; right: number; maxH: number } | null>(null);
  const place = () => {
    const btn = rootRef.current?.querySelector('button');
    if (!btn) return;
    const r = btn.getBoundingClientRect();
    const vh = window.innerHeight;
    const below = vh - r.bottom - 12;
    const above = r.top - 12;
    const want = Math.min(menuRef.current?.scrollHeight || 420, 520);
    const right = Math.max(8, window.innerWidth - r.right);
    if (below >= Math.min(want, 280) || below >= above) setPos({ top: r.bottom + 6, right, maxH: Math.max(160, below) });
    else setPos({ bottom: vh - r.top + 6, right, maxH: Math.max(160, above) });
  };
  useLayoutEffect(() => {
    if (!open || isPhone) return;
    place();
    const raf = requestAnimationFrame(place);
    const onMove = () => place();
    window.addEventListener('resize', onMove);
    window.addEventListener('scroll', onMove, true);
    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener('resize', onMove);
      window.removeEventListener('scroll', onMove, true);
    };
  }, [open, isPhone]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    if (!open) return;
    setIsPhone(window.innerWidth < 640);
    const onDown = (e: MouseEvent) => {
      const t = e.target as HTMLElement;
      if (t.closest?.('[data-action-sheet]') || menuRef.current?.contains(t)) return;
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
                    : 'min-h-[38px] px-2.5 rounded-lg text-[14px] hover:bg-canvas'
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
        aria-label={label ? undefined : highlight ? `${title} · ${highlight.title}` : title}
        title={highlight ? `${title} · ${highlight.title}` : title}
        className={`h-9 rounded-[10px] border flex items-center justify-center gap-1 text-[13.5px] font-semibold cursor-pointer transition-colors ${
          label || highlight ? 'px-2' : 'w-9'
        } ${
          highlight
            ? `text-accent border-accent/40 ${open ? 'bg-accent-soft border-accent' : 'bg-accent-soft hover:border-accent'}`
            : `text-ink ${open ? 'bg-canvas border-line-2' : 'bg-white border-line hover:border-line-2'}`
        }`}
      >
        {highlight && <highlight.icon className="w-4 h-4" />}
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
                className="absolute left-0 right-0 bottom-0 max-h-[80dvh] overflow-y-auto bg-white rounded-t-2xl px-4 pt-2 pb-[max(env(safe-area-inset-bottom),20px)] shadow-lg"
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
          createPortal(
            <div
              ref={menuRef}
              role="menu"
              aria-label={title}
              data-action-sheet
              style={{ position: 'fixed', top: pos?.top, bottom: pos?.bottom, right: pos?.right ?? 8, maxHeight: pos?.maxH, visibility: pos ? 'visible' : 'hidden' }}
              className="ms-menu-pop z-[75] w-[264px] overflow-y-auto overscroll-contain bg-white border border-line rounded-xl p-1.5 shadow-lg"
            >
              {list(false)}
            </div>,
            document.body
          )
        ))}
    </div>
  );
};
