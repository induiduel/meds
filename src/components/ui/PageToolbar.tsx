import React, { startTransition, useEffect, useLayoutEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { Check, ChevronDown, Search, SlidersHorizontal, X } from 'lucide-react';
import { Sheet } from './Sheet';
import { useAppearance } from '../../utils/appearance';

/**
 * Ortak kompakt sayfa başlığı (v10) — Sözlük, Çıkmış sorular ve Soru havuzu aynı iskeleti kullanır.
 *  - Masaüstü (≥1024): başlık · sayaç · arama · segment · Süzgeç · araçlar tek satır (52 px).
 *  - Tablet (768–1023): 1. satır başlık + Süzgeç + araçlar, 2. satır arama + segment.
 *  - Telefon (<768): başlık satırı · arama + Süzgeç · yatay kayan segment (en çok ~128 px).
 *  - İkincil süzgeçler sayfada değil "Süzgeç" sayfasında (Sheet) durur; etkin olanlar tek çip satırında görünür.
 *  - Yapışkan DEĞİL: sayfayla birlikte kayar, kaydırınca ekranda yer kaplamaz. Aşağıda kalınca
 *    shell/ScrollTopFab ile tek dokunuşta başa dönülür (arama odaklanır).
 * Stil: styles/toolbar.css (.pt-*). Arama "/" kısayoluyla odaklanır (input'a data-page-search verilir).
 */
export interface ToolbarSegment<T extends string = string> {
  id: T;
  label: string;
  count?: number;
}
export interface ToolbarChip {
  id: string;
  label: string;
  onRemove: () => void;
}

/**
 * Hızlı süzgeç hapı: "Ders ▾" — seçim yapılınca hap seçili değeri gösterir ve vurgulanır.
 * Masaüstünde hapın altında küçük pencere, telefonda alt sayfa açar. İçerik genelde <QuickOptions>.
 */
export interface ToolbarQuick {
  id: string;
  label: string;
  /** Seçili değerin kısa adı; verilirse hap etkin görünür ("Ders: Patoloji") */
  value?: string;
  onClear?: () => void;
  content: (close: () => void) => React.ReactNode;
  /** Geniş pencere (uzun listeler için) */
  wide?: boolean;
}

export interface PageToolbarProps<T extends string = string> {
  title: React.ReactNode;
  count?: React.ReactNode;
  search?: { value: string; onChange: (v: string) => void; placeholder?: string };
  segments?: { options: ToolbarSegment<T>[]; value: T; onChange: (v: T) => void; label?: string };
  /** Süzgeç sayfasının içeriği; verilmezse düğme görünmez */
  filters?: React.ReactNode;
  filterCount?: number;
  filterTitle?: string;
  chips?: ToolbarChip[];
  onClearChips?: () => void;
  /** Arama satırının altında tek satır hızlı süzgeç hapları (Durum ▾ · Kurul ▾ · Ders ▾ · Sırala ▾) */
  quick?: ToolbarQuick[];
  /** Sağdaki sessiz araçlar (simge düğmeleri, görünüm seçici…) */
  tools?: React.ReactNode;
  className?: string;
  children?: React.ReactNode;
}

export function PageToolbar<T extends string = string>({
  title, count, search, segments, filters, filterCount = 0, filterTitle = 'Süzgeç', chips, onClearChips, quick, tools, className = '', children,
}: PageToolbarProps<T>) {
  const [open, setOpen] = useState(false);
  const rootRef = useRef<HTMLElement>(null);
  const look = useAppearance();
  // v11 basit süzgeç modu: "Süzgeç" sayfası yalnız etkin süzgeç varsa ya da kullanıcı açarsa görünür
  const [advOnce, setAdvOnce] = useState(false);
  const showFilterBtn = !!filters && (look.design === 'v10' || look.filters === 'gelismis' || filterCount > 0 || advOnce || !quick?.length);
  // Yazarken takılma olmasın: kutu yerel durumla anında güncellenir, ağır liste süzmesi geçiş önceliğinde koşar
  const [q, setQ] = useState(search?.value ?? '');
  const sentRef = useRef(search?.value ?? '');
  useEffect(() => {
    if (search && search.value !== sentRef.current) { sentRef.current = search.value; setQ(search.value); }
  }, [search?.value]);
  const typeQ = (v: string) => {
    setQ(v);
    sentRef.current = v;
    startTransition(() => search?.onChange(v));
  };
  // Başlık satırının yüksekliği: kompakt hâlde çubuk bu kadar yukarı kayar (arama satırı üst çubuğun hemen altına gelir).
  useLayoutEffect(() => {
    const root = rootRef.current;
    if (!root || typeof ResizeObserver === 'undefined') return;
    const measure = () => {
      const s = root.querySelector<HTMLElement>('.pt-search, .pt-seg');
      const pad = parseFloat(getComputedStyle(root).paddingTop) || 0;
      const lead = s ? Math.max(0, s.offsetTop - pad) : 0;
      root.style.setProperty('--pt-lead', `${lead}px`);
    };
    measure();
    const ro = new ResizeObserver(measure);
    ro.observe(root);
    return () => ro.disconnect();
  }, []);
  return (
    <header ref={rootRef} className={`pt-root ${className}`}>
      <div className="pt-row">
        <div className="pt-title">
          <h1 className="pt-h">{title}</h1>
          {count != null && <span className="pt-count" aria-live="polite">{count}</span>}
        </div>
        {search && (
          <label className="pt-search">
            <Search aria-hidden />
            <input
              type="search"
              data-page-search
              value={q}
              onChange={(e) => typeQ(e.target.value)}
              placeholder={search.placeholder || 'Ara'}
              aria-label={search.placeholder || 'Ara'}
              enterKeyHint="search"
            />
            {q && (
              <button type="button" className="pt-clear" onClick={() => typeQ('')} aria-label="Aramayı temizle">
                <X aria-hidden />
              </button>
            )}
          </label>
        )}
        {segments && (
          <div className="pt-seg" role="tablist" aria-label={segments.label || 'Görünüm'}>
            {segments.options.map((o) => (
              <button
                key={o.id}
                type="button"
                role="tab"
                aria-selected={o.id === segments.value}
                className={o.id === segments.value ? 'is-on' : ''}
                onClick={() => segments.onChange(o.id)}
              >
                {o.label}
                {o.count != null && <span className="pt-seg-n">{o.count.toLocaleString('tr-TR')}</span>}
              </button>
            ))}
          </div>
        )}
        {showFilterBtn && (
          <button type="button" className="pt-filter" onClick={() => setOpen(true)} aria-haspopup="dialog">
            <SlidersHorizontal aria-hidden />
            <span className="pt-filter-l">Süzgeç</span>
            {filterCount > 0 && <span className="pt-badge" aria-label={`${filterCount} etkin süzgeç`}>{filterCount}</span>}
          </button>
        )}
        {tools && <div className="pt-tools">{tools}</div>}
      </div>
      {quick && quick.length > 0 && (
        <div className="pt-quick" role="toolbar" aria-label="Hızlı süzgeçler">
          {quick.map((qp) => <QuickPill key={qp.id} q={qp} />)}
          {filters && !showFilterBtn && (
            <button type="button" className="pt-more" onClick={() => { setAdvOnce(true); setOpen(true); }} aria-haspopup="dialog">
              <SlidersHorizontal aria-hidden />Daha fazla
            </button>
          )}
        </div>
      )}
      {chips && chips.length > 0 && (
        <div className="pt-chips">
          {chips.map((c) => (
            <button key={c.id} type="button" className="pt-chip" onClick={c.onRemove} aria-label={`${c.label} süzgecini kaldır`}>
              {c.label}
              <X aria-hidden />
            </button>
          ))}
          {onClearChips && chips.length > 1 && (
            <button type="button" className="pt-chip-clear" onClick={onClearChips}>Temizle</button>
          )}
        </div>
      )}
      {children}
      {filters && (
        <Sheet open={open} onClose={() => setOpen(false)} title={filterTitle} width={460}
          footer={<button type="button" className="ui-btn is-primary" style={{ width: '100%' }} onClick={() => setOpen(false)}>Uygula</button>}>
          <div className="pt-sheet">{filters}</div>
        </Sheet>
      )}
    </header>
  );
}

/** Süzgeç sayfasında tek bir grup: başlık + seçenek hapları (tek seçim) */
export function FilterPills<T extends string>({ label, options, value, onChange }: {
  label: string;
  options: { id: T; label: string; count?: number }[];
  value: T;
  onChange: (v: T) => void;
}) {
  return (
    <fieldset className="pt-fgroup">
      <legend>{label}</legend>
      <div className="pt-pills">
        {options.map((o) => (
          <button key={o.id} type="button" aria-pressed={o.id === value} className={o.id === value ? 'is-on' : ''} onClick={() => onChange(o.id)}>
            {o.label}
            {o.count != null && <span>{o.count.toLocaleString('tr-TR')}</span>}
          </button>
        ))}
      </div>
    </fieldset>
  );
}

const isPhone = () => typeof window !== 'undefined' && window.matchMedia('(max-width: 767px)').matches;

export function QuickPill({ q }: { q: ToolbarQuick }) {
  const [open, setOpen] = useState(false);
  const [phone, setPhone] = useState(false);
  const [pos, setPos] = useState<{ left: number; top: number; width: number } | null>(null);
  const btnRef = useRef<HTMLButtonElement>(null);
  const popRef = useRef<HTMLDivElement>(null);
  const close = () => { setOpen(false); btnRef.current?.focus({ preventScroll: true }); };
  const toggle = () => {
    if (open) { setOpen(false); return; }
    const p = isPhone();
    setPhone(p);
    if (!p && btnRef.current) {
      const r = btnRef.current.getBoundingClientRect();
      const width = q.wide ? 360 : 280;
      const left = Math.max(12, Math.min(r.left, window.innerWidth - width - 12));
      setPos({ left, top: r.bottom + 6, width });
    }
    setOpen(true);
  };
  // Masaüstü penceresi: dışarı tıklama, Esc, kaydırma ve yeniden boyutlama kapatır
  React.useEffect(() => {
    if (!open || phone) return;
    const onDown = (e: PointerEvent) => {
      const t = e.target as Node;
      if (popRef.current?.contains(t) || btnRef.current?.contains(t)) return;
      setOpen(false);
    };
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') close(); };
    const onScroll = (e: Event) => { if (!popRef.current?.contains(e.target as Node)) setOpen(false); };
    document.addEventListener('pointerdown', onDown, true);
    document.addEventListener('keydown', onKey);
    window.addEventListener('scroll', onScroll, true);
    window.addEventListener('resize', close);
    requestAnimationFrame(() => popRef.current?.querySelector<HTMLElement>('input, [aria-checked="true"], button')?.focus({ preventScroll: true }));
    return () => {
      document.removeEventListener('pointerdown', onDown, true);
      document.removeEventListener('keydown', onKey);
      window.removeEventListener('scroll', onScroll, true);
      window.removeEventListener('resize', close);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open, phone]);
  const on = Boolean(q.value);
  return (
    <>
      <span className={`pt-q ${on ? 'is-on' : ''} ${open ? 'is-open' : ''}`}>
        <button ref={btnRef} type="button" className="pt-q-btn" aria-haspopup="dialog" aria-expanded={open} onClick={toggle}>
          <span className="pt-q-l">{q.label}</span>
          {on && <span className="pt-q-v">{q.value}</span>}
          {!on && <ChevronDown aria-hidden />}
        </button>
        {on && q.onClear && (
          <button type="button" className="pt-q-x" onClick={q.onClear} aria-label={`${q.label} süzgecini kaldır`}><X aria-hidden /></button>
        )}
      </span>
      {open && phone && (
        <Sheet open onClose={close} title={q.label} width={420}>
          <div className="pt-qsheet">{q.content(close)}</div>
        </Sheet>
      )}
      {open && !phone && pos && createPortal(
        <div ref={popRef} className="pt-pop" role="dialog" aria-label={q.label} style={{ left: pos.left, top: pos.top, width: pos.width }}>
          {q.content(close)}
        </div>,
        document.body,
      )}
    </>
  );
}

export interface QuickOption { id: string; label: string; count?: number; hint?: string; group?: string; className?: string }

/** Hızlı süzgeç penceresinde tek seçimli liste: isteğe bağlı arama, grup başlıkları, sayılar, ✓ işareti. */
export function QuickOptions({ options, value, onPick, close, searchable, placeholder = 'Ara' }: {
  options: QuickOption[];
  value: string;
  onPick: (id: string) => void;
  close: () => void;
  searchable?: boolean;
  placeholder?: string;
}) {
  const [q, setQ] = useState('');
  const fold = (t: string) => t.toLocaleLowerCase('tr').normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/ı/g, 'i');
  const shown = q ? options.filter((o) => fold(o.label).includes(fold(q))) : options;
  let lastGroup: string | undefined;
  return (
    <div className="pt-qo">
      {searchable && (
        <label className="pt-qo-q">
          <Search aria-hidden />
          <input value={q} onChange={(e) => setQ(e.target.value)} placeholder={placeholder} aria-label={placeholder} />
        </label>
      )}
      <div className="pt-qo-list" role="radiogroup">
        {shown.length === 0 && <p className="pt-qo-empty">Eşleşen seçenek yok</p>}
        {shown.map((o) => {
          const head = !q && o.group && o.group !== lastGroup ? o.group : null;
          lastGroup = o.group;
          const sel = o.id === value;
          return (
            <React.Fragment key={o.id}>
              {head && <div className="pt-qo-g">{head}</div>}
              <button
                type="button"
                role="radio"
                aria-checked={sel}
                className={`pt-qo-opt ${sel ? 'is-on' : ''} ${o.count === 0 && !sel ? 'is-zero' : ''} ${o.className || ''}`}
                onClick={() => { onPick(o.id); close(); }}
              >
                <span className="pt-qo-t">{o.label}{o.hint && <small>{o.hint}</small>}</span>
                {o.count != null && <span className="pt-qo-n">{o.count.toLocaleString('tr-TR')}</span>}
                <span className="pt-qo-c" aria-hidden>{sel && <Check strokeWidth={3} />}</span>
              </button>
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
}
