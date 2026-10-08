import React, { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { Search, X } from 'lucide-react';

/**
 * Yönetim konsolunun ortak parçaları. Görünüm index.css içindeki
 * "Yönetim konsolu · v3" bölümündedir (ms-panel, ms-row, ms-input …).
 */

export const Panel: React.FC<{
  title?: React.ReactNode;
  icon?: React.ElementType;
  count?: React.ReactNode;
  desc?: React.ReactNode;
  tools?: React.ReactNode;
  /** true: gövde dolgusuz (liste ya da tablo doğrudan girer) */
  flush?: boolean;
  className?: string;
  bodyClassName?: string;
  children?: React.ReactNode;
}> = ({ title, icon: Icon, count, desc, tools, flush, className = '', bodyClassName = '', children }) => (
  <section className={`ms-panel ${className}`}>
    {(title || tools) && (
      <header className="ms-panel-head">
        {title && (
          <h2 className="ms-panel-title">
            {Icon && <Icon aria-hidden="true" />}
            <span className="min-w-0">{title}</span>
            {count !== undefined && <span className="n">{count}</span>}
          </h2>
        )}
        {tools && <div className="ms-panel-tools">{tools}</div>}
        {desc && <p className="ms-panel-desc">{desc}</p>}
      </header>
    )}
    {flush ? children : <div className={`ms-panel-body ${bodyClassName}`}>{children}</div>}
  </section>
);

export const EmptyState: React.FC<{
  icon?: React.ElementType;
  title: React.ReactNode;
  children?: React.ReactNode;
  action?: React.ReactNode;
}> = ({ icon: Icon, title, children, action }) => (
  <div className="ms-empty">
    {Icon && <Icon aria-hidden="true" />}
    <b>{title}</b>
    {children && <p>{children}</p>}
    {action}
  </div>
);

export const Switch: React.FC<{
  checked: boolean;
  onChange: (v: boolean) => void;
  label: React.ReactNode;
  hint?: React.ReactNode;
  disabled?: boolean;
}> = ({ checked, onChange, label, hint, disabled }) => (
  <label className="ms-switch">
    <input type="checkbox" role="switch" checked={checked} disabled={disabled} onChange={(e) => onChange(e.target.checked)} />
    <span className="ms-switch-track" aria-hidden="true" />
    <span className="ms-switch-text">
      {label}
      {hint && <small>{hint}</small>}
    </span>
  </label>
);

export const Field: React.FC<{ label: React.ReactNode; hint?: React.ReactNode; className?: string; children: React.ReactNode }> = ({
  label,
  hint,
  className = '',
  children,
}) => (
  <label className={`ms-field ${className}`}>
    <span className="lbl">{label}</span>
    {children}
    {hint && <span className="hint">{hint}</span>}
  </label>
);

/** Sayfa içi arama kutusu (ms-qsearch): temizleme düğmesi ve isteğe bağlı sonuç sayısı. */
export const SearchBox: React.FC<{
  value: string;
  onChange: (v: string) => void;
  placeholder: string;
  label?: string;
  count?: React.ReactNode;
  className?: string;
}> = ({ value, onChange, placeholder, label, count, className = '' }) => (
  <label className={`ms-qsearch ${className}`}>
    <Search aria-hidden="true" />
    <span className="sr-only">{label || placeholder}</span>
    <input type="search" value={value} onChange={(e) => onChange(e.target.value)} placeholder={placeholder} />
    {count !== undefined && !value && <span className="text-[12.5px] text-ink-3 pr-2 shrink-0 tabular-nums">{count}</span>}
    {value && (
      <button type="button" onClick={() => onChange('')} className="ms-btn is-ghost is-icon is-sm" aria-label="Aramayı temizle">
        <X />
      </button>
    )}
  </label>
);

/**
 * İki adımlı yıkıcı eylem: ilk dokunuş düğmeyi kırmızıya çevirir ve onay metnini gösterir,
 * ikincisi işlemi yapar. 4 sn içinde onaylanmazsa eski haline döner.
 */
export const ConfirmButton: React.FC<{
  onConfirm: () => void | Promise<void>;
  children: React.ReactNode;
  confirmLabel: React.ReactNode;
  icon?: React.ElementType;
  busy?: boolean;
  busyLabel?: React.ReactNode;
  disabled?: boolean;
  className?: string;
  title?: string;
}> = ({ onConfirm, children, confirmLabel, icon: Icon, busy, busyLabel, disabled, className = 'ms-btn is-sm is-danger', title }) => {
  const [armed, setArmed] = useState(false);
  useEffect(() => {
    if (!armed) return;
    const t = window.setTimeout(() => setArmed(false), 4000);
    return () => window.clearTimeout(t);
  }, [armed]);
  return (
    <button
      type="button"
      title={title}
      disabled={disabled || busy}
      onClick={(e) => {
        e.stopPropagation();
        if (!armed) return setArmed(true);
        setArmed(false);
        void onConfirm();
      }}
      className={`${className} ${armed ? 'is-armed' : ''}`}
    >
      {Icon && <Icon aria-hidden="true" />}
      {busy ? busyLabel || children : armed ? confirmLabel : children}
    </button>
  );
};

/**
 * Yan çekmece: masaüstünde sağdan, telefonda alttan açılır. Gövdeye taşınır (yoğunluk ölçeği
 * uygulanan konsol gövdesinden etkilenmesin). Esc ve arka plan kapatır.
 */
export const Drawer: React.FC<{
  open: boolean;
  onClose: () => void;
  title: React.ReactNode;
  label?: string;
  wide?: boolean;
  head?: React.ReactNode;
  foot?: React.ReactNode;
  children: React.ReactNode;
}> = ({ open, onClose, title, label, wide, head, foot, children }) => {
  const ref = useRef<HTMLElement>(null);
  useEffect(() => {
    if (!open) return;
    const prev = document.activeElement as HTMLElement | null;
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && onClose();
    window.addEventListener('keydown', onKey);
    ref.current?.focus();
    return () => {
      window.removeEventListener('keydown', onKey);
      prev?.focus?.();
    };
  }, [open, onClose]);
  if (!open) return null;
  return createPortal(
    <>
      <div className="ms-drawer-scrim" onClick={onClose} aria-hidden="true" />
      <aside ref={ref} tabIndex={-1} role="dialog" aria-modal="true" aria-label={label || (typeof title === 'string' ? title : undefined)} className={`ms-drawer outline-none ${wide ? 'is-wide' : ''}`}>
        <div className="ms-drawer-head">
          <h2 className="ms-drawer-title truncate">{title}</h2>
          {head}
          <button type="button" onClick={onClose} className="ms-btn is-ghost is-icon" aria-label="Kapat">
            <X />
          </button>
        </div>
        <div className="ms-drawer-body">{children}</div>
        {foot && <div className="ms-drawer-foot">{foot}</div>}
      </aside>
    </>,
    document.body,
  );
};

/** Bölümlü seçici (ms-seg) */
export function Seg<T extends string>({
  value,
  onChange,
  options,
  label,
  className = '',
}: {
  value: T;
  onChange: (v: T) => void;
  options: { id: T; label: React.ReactNode; n?: React.ReactNode }[];
  label: string;
  className?: string;
}) {
  return (
    <div role="radiogroup" aria-label={label} className={`ms-seg ${className}`}>
      {options.map((o) => (
        <button key={o.id} type="button" role="radio" aria-checked={value === o.id} onClick={() => onChange(o.id)}>
          {o.label}
          {o.n !== undefined && <span className="n">{o.n}</span>}
        </button>
      ))}
    </div>
  );
}

/** Filtre çipleri (ms-chipbar + ms-fchip) */
export function ChipBar<T extends string>({
  value,
  onChange,
  options,
  label,
  wrap,
}: {
  value: T;
  onChange: (v: T) => void;
  options: { id: T; label: React.ReactNode; n?: number; icon?: React.ElementType }[];
  label: string;
  wrap?: boolean;
}) {
  return (
    <div role="radiogroup" aria-label={label} className={`ms-chipbar ${wrap ? 'is-wrap' : ''}`}>
      {options.map((o) => {
        const on = value === o.id;
        const Icon = o.icon;
        return (
          <button
            key={o.id}
            type="button"
            role="radio"
            aria-checked={on}
            onClick={() => onChange(o.id)}
            className={`ms-fchip ${on ? 'is-on' : ''} ${o.n === 0 && !on ? 'is-zero' : ''}`}
          >
            {Icon && <Icon className="w-3.5 h-3.5" aria-hidden="true" />}
            {o.label}
            {o.n !== undefined && <span className="n">{o.n.toLocaleString('tr-TR')}</span>}
          </button>
        );
      })}
    </div>
  );
}

const startOfDay = (d: Date) => new Date(d.getFullYear(), d.getMonth(), d.getDate()).getTime();

/** "Bugün", "Dün", "5 Ekim" ya da "5 Ekim 2025" */
export const dayLabel = (iso?: string) => {
  if (!iso) return 'Tarihsiz';
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return 'Tarihsiz';
  const diff = Math.round((startOfDay(new Date()) - startOfDay(d)) / 86400000);
  if (diff === 0) return 'Bugün';
  if (diff === 1) return 'Dün';
  const sameYear = d.getFullYear() === new Date().getFullYear();
  return d.toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', ...(sameYear ? {} : { year: 'numeric' }) });
};

/** "14:43" ya da "6 Eki 14:43" */
export const timeLabel = (iso?: string, withDay = false) => {
  if (!iso) return '';
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return '';
  const t = d.toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' });
  return withDay ? `${d.toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' })} ${t}` : t;
};

/** Konsol bildirimini tonuna göre toast olarak gösterir */
const ERROR_WORDS = /yüklenemedi|edilemedi|başarısız|bulunamadı|silinemez|silinemedi|zorunlu|yapılamadı|alınamadı|gönderilemedi|çevrilemedi|hata|olmadı/i;
export const classifyNotice = (msg: string): 'error' | 'success' => (ERROR_WORDS.test(msg) ? 'error' : 'success');

/** Betik/eşitleme günlük satırının tonu (ms-term içindeki renk sınıfı) */
export const logTone = (line: string) =>
  /\[HATA\]|\[STDERR\]|\bERR|error|Error|HATA/.test(line)
    ? 'is-error'
    : /\[BAŞARILI\]|✓|BAŞARIYLA|TAMAMLANDI/.test(line)
      ? 'is-ok'
      : /\[UYARI\]|WARN|⚠|TESPİT EDİLDİ/.test(line)
        ? 'is-warn'
        : /BAŞLADI|İşleniyor|Taranıyor|\[Başlatılıyor\]/.test(line)
          ? 'is-info'
          : '';
