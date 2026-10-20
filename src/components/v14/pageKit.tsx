import React from 'react';
import { Search } from 'lucide-react';
import { SelectAllBox } from './manageKit';
import '../../styles/v14/manage.css';

/**
 * v14 bölüm sayfası parçaları — canvas ListeSablon.dc.html kalıbının React karşılığı.
 * Bir bölüm sayfası şu sırayla kurulur:
 *   <PageActions>  (birincil/ikincil eylemler; başlık kabukta)
 *   <StatRow>      (sayı kartları, isteğe bağlı)
 *   <Toolbar>      (Tabs14 + SearchField + süzgeçler; sarılır)
 *   <BulkBar>      (manageKit; yalnız seçim varken)
 *   <DataTable>    (seçim kutulu tablo; satıra tıkla → Drawer = tam alan çalışma alanı)
 * Ayrıntı/düzenleme için consoleUi Drawer kullanılır (v14'te içerik alanının tamamını kaplar);
 * DetailNav ile önceki/sonraki geçişi Drawer `head`ine konur.
 */

export const PageActions: React.FC<{ children: React.ReactNode; note?: React.ReactNode }> = ({ children, note }) => (
  <div className="pk14-actions">
    {note && <p className="pk14-note">{note}</p>}
    <div className="pk14-actions-btns">{children}</div>
  </div>
);

export type Stat = { label: React.ReactNode; value: React.ReactNode; tone?: 'ok' | 'warn' | 'bad' | 'acc'; onClick?: () => void; hint?: string };
export const StatRow: React.FC<{ stats: Stat[] }> = ({ stats }) => (
  <section className="pk14-stats" aria-label="Özet">
    {stats.map((s, i) => {
      const body = (
        <>
          <span className="l">{s.label}</span>
          <span className={`v ${s.tone || ''}`}>{s.value}</span>
        </>
      );
      return s.onClick ? (
        <button key={i} type="button" className="pk14-stat is-btn" onClick={s.onClick} title={s.hint}>{body}</button>
      ) : (
        <div key={i} className="pk14-stat" title={s.hint}>{body}</div>
      );
    })}
  </section>
);

export function Tabs14<T extends string>({ value, onChange, options, label }: {
  value: T;
  onChange: (v: T) => void;
  options: { id: T; label: React.ReactNode; n?: number }[];
  label: string;
}) {
  return (
    <div role="tablist" aria-label={label} className="pk14-tabs">
      {options.map((o) => (
        <button key={o.id} type="button" role="tab" aria-selected={value === o.id} className={value === o.id ? 'on' : ''} onClick={() => onChange(o.id)}>
          {o.label}
          {o.n !== undefined && <span className="n">{o.n.toLocaleString('tr-TR')}</span>}
        </button>
      ))}
    </div>
  );
}

export const SearchField: React.FC<{ value: string; onChange: (v: string) => void; placeholder?: string; label?: string }> = ({ value, onChange, placeholder = 'Ara', label = 'Ara' }) => (
  <label className="pk14-search">
    <Search aria-hidden="true" />
    <input type="search" value={value} onChange={(e) => onChange(e.target.value)} placeholder={placeholder} aria-label={label} />
  </label>
);

export const Toolbar: React.FC<{ children: React.ReactNode }> = ({ children }) => <div className="pk14-toolbar">{children}</div>;

export type Col<R> = {
  key: string;
  label: React.ReactNode;
  render: (r: R) => React.ReactNode;
  /** sayısal sütun: sağa yaslı */
  right?: boolean;
  mono?: boolean;
  muted?: boolean;
  /** ana sütun: genişler, tek satır "…" ile kısalır */
  main?: boolean;
  width?: number | string;
};

export function DataTable<R>({
  rows, cols, rowKey, onOpen, selection, empty = 'Kayıt yok.', minWidth = 760, activeKey, busy,
}: {
  rows: R[];
  cols: Col<R>[];
  rowKey: (r: R) => string;
  onOpen?: (r: R) => void;
  selection?: { has: (k: string) => boolean; toggle: (k: string) => void; toggleAll: (keys: string[]) => void; allOf: (keys: string[]) => boolean; someOf: (keys: string[]) => boolean };
  empty?: React.ReactNode;
  minWidth?: number;
  activeKey?: string | null;
  busy?: boolean;
}) {
  const keys = rows.map(rowKey);
  return (
    <div className="pk14-tablebox" aria-busy={busy || undefined}>
      <table className="pk14-table" style={{ minWidth }}>
        <thead>
          <tr>
            {selection && (
              <th className="chk">
                <SelectAllBox all={selection.allOf(keys)} some={selection.someOf(keys)} onChange={() => selection.toggleAll(keys)} />
              </th>
            )}
            {cols.map((c) => (
              <th key={c.key} className={`${c.right ? 'r' : ''}`} style={c.width ? { width: c.width } : undefined}>{c.label}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => {
            const k = rowKey(r);
            const on = selection?.has(k);
            return (
              <tr
                key={k}
                className={`${on ? 'is-picked' : ''} ${activeKey === k ? 'is-active' : ''} ${onOpen ? 'is-click' : ''}`}
                tabIndex={onOpen ? 0 : undefined}
                onClick={onOpen ? () => onOpen(r) : undefined}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && onOpen) onOpen(r);
                  if (selection && (e.key === 'x' || e.key === ' ')) { e.preventDefault(); selection.toggle(k); }
                }}
              >
                {selection && (
                  <td className="chk" onClick={(e) => e.stopPropagation()}>
                    <input type="checkbox" checked={!!on} onChange={() => selection.toggle(k)} aria-label="Seç" />
                  </td>
                )}
                {cols.map((c) => (
                  <td key={c.key} className={`${c.right ? 'r' : ''} ${c.mono ? 'mono' : ''} ${c.muted ? 'muted' : ''} ${c.main ? 'main' : ''}`}>
                    {c.main ? <span className="clip">{c.render(r)}</span> : c.render(r)}
                  </td>
                ))}
              </tr>
            );
          })}
          {rows.length === 0 && (
            <tr><td className="pk14-empty" colSpan={cols.length + (selection ? 1 : 0)}>{empty}</td></tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export const Pill: React.FC<{ tone?: 'ok' | 'warn' | 'bad' | 'acc' | ''; children: React.ReactNode }> = ({ tone = '', children }) => (
  <span className={`m14-pill ${tone}`}>{children}</span>
);

/** Ayrıntı alanında önceki / sonraki (Drawer head içine) */
export function DetailNav<R>({ list, current, same, onGo }: { list: R[]; current: R | null; same: (a: R, b: R) => boolean; onGo: (r: R) => void }) {
  const i = current ? list.findIndex((x) => same(x, current)) : -1;
  if (i < 0 || list.length < 2) return null;
  return (
    <span className="pk14-dnav">
      <span className="pos">{i + 1} / {list.length}</span>
      <button type="button" className="m14-btn icon" aria-label="Önceki" onClick={() => onGo(list[(i - 1 + list.length) % list.length])}>‹</button>
      <button type="button" className="m14-btn icon" aria-label="Sonraki" onClick={() => onGo(list[(i + 1) % list.length])}>›</button>
    </span>
  );
}

/** Ayrıntı alanı gövdesi: ana içerik + sağda bilgi alanı (dar ekranda alta iner) */
export const DetailLayout: React.FC<{ main: React.ReactNode; side?: React.ReactNode }> = ({ main, side }) => (
  <div className="pk14-detail">
    <div className="pk14-detail-main">{main}</div>
    {side && <aside className="pk14-detail-side">{side}</aside>}
  </div>
);
export const FactList: React.FC<{ items: { k: React.ReactNode; v: React.ReactNode }[] }> = ({ items }) => (
  <dl className="pk14-facts">
    {items.map((it, i) => (
      <React.Fragment key={i}><dt>{it.k}</dt><dd>{it.v ?? '—'}</dd></React.Fragment>
    ))}
  </dl>
);
export const Card14: React.FC<{ title?: React.ReactNode; tools?: React.ReactNode; children: React.ReactNode; flush?: boolean }> = ({ title, tools, children, flush }) => (
  <section className="pk14-card">
    {(title || tools) && <header>{title && <h2>{title}</h2>}{tools && <div className="t">{tools}</div>}</header>}
    <div className={flush ? '' : 'b'}>{children}</div>
  </section>
);
