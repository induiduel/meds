import React, { useState } from 'react';
import { Search, SlidersHorizontal, X } from 'lucide-react';
import { Sheet } from './Sheet';

/**
 * Ortak kompakt sayfa başlığı (v10) — Sözlük, Çıkmış sorular ve Soru havuzu aynı iskeleti kullanır.
 *  - Masaüstü (≥1024): başlık · sayaç · arama · segment · Süzgeç · araçlar tek satır (52 px).
 *  - Tablet (768–1023): 1. satır başlık + Süzgeç + araçlar, 2. satır arama + segment.
 *  - Telefon (<768): başlık satırı · arama + Süzgeç · yatay kayan segment (en çok ~128 px).
 *  - İkincil süzgeçler sayfada değil "Süzgeç" sayfasında (Sheet) durur; etkin olanlar tek çip satırında görünür.
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
  /** Sağdaki sessiz araçlar (simge düğmeleri, görünüm seçici…) */
  tools?: React.ReactNode;
  className?: string;
  children?: React.ReactNode;
}

export function PageToolbar<T extends string = string>({
  title, count, search, segments, filters, filterCount = 0, filterTitle = 'Süzgeç', chips, onClearChips, tools, className = '', children,
}: PageToolbarProps<T>) {
  const [open, setOpen] = useState(false);
  return (
    <header className={`pt-root ${className}`}>
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
              value={search.value}
              onChange={(e) => search.onChange(e.target.value)}
              placeholder={search.placeholder || 'Ara'}
              aria-label={search.placeholder || 'Ara'}
              enterKeyHint="search"
            />
            {search.value && (
              <button type="button" className="pt-clear" onClick={() => search.onChange('')} aria-label="Aramayı temizle">
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
        {filters && (
          <button type="button" className="pt-filter" onClick={() => setOpen(true)} aria-haspopup="dialog">
            <SlidersHorizontal aria-hidden />
            <span className="pt-filter-l">Süzgeç</span>
            {filterCount > 0 && <span className="pt-badge" aria-label={`${filterCount} etkin süzgeç`}>{filterCount}</span>}
          </button>
        )}
        {tools && <div className="pt-tools">{tools}</div>}
      </div>
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
