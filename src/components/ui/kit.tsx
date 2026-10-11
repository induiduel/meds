import React, { useId } from 'react';

/**
 * v8 ortak parçaları (stiller styles/appearance.css · ".ui-*").
 * Yalnız token okur; yoğunluk (data-density) ve palet (data-mode/data-palette) değişince kendiliğinden uyar.
 */

export function Segmented<T extends string>({
  value,
  options,
  onChange,
  label,
  className = '',
}: {
  value: T;
  options: { value: T; label: React.ReactNode; title?: string }[];
  onChange: (v: T) => void;
  label: string;
  className?: string;
}) {
  const i = Math.max(0, options.findIndex((o) => o.value === value));
  const n = options.length;
  const onKey = (e: React.KeyboardEvent) => {
    if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
    e.preventDefault();
    const next = options[(i + (e.key === 'ArrowRight' ? 1 : n - 1)) % n];
    onChange(next.value);
    (e.currentTarget.querySelectorAll('button')[options.indexOf(next)] as HTMLButtonElement | undefined)?.focus();
  };
  return (
    <div role="radiogroup" aria-label={label} className={`ui-seg ${className}`} onKeyDown={onKey}>
      <span
        className="ui-seg-thumb"
        aria-hidden="true"
        style={{ width: `calc((100% - 4px) / ${n})`, transform: `translateX(${i * 100}%)` }}
      />
      {options.map((o) => (
        <button
          key={o.value}
          type="button"
          role="radio"
          aria-checked={o.value === value}
          tabIndex={o.value === value ? 0 : -1}
          title={o.title}
          onClick={() => onChange(o.value)}
        >
          {o.label}
        </button>
      ))}
    </div>
  );
}

export const Switch: React.FC<{ checked: boolean; onChange: (v: boolean) => void; label: string; disabled?: boolean; id?: string }> = ({
  checked,
  onChange,
  label,
  disabled,
  id,
}) => (
  <button
    id={id}
    type="button"
    role="switch"
    aria-checked={checked}
    aria-label={label}
    disabled={disabled}
    className="ui-switch"
    onClick={() => onChange(!checked)}
  />
);

export const Section: React.FC<{ id?: string; title?: React.ReactNode; end?: React.ReactNode; foot?: React.ReactNode; children: React.ReactNode }> = ({
  id,
  title,
  end,
  foot,
  children,
}) => {
  const hid = useId();
  return (
    <section id={id} className="ui-section" aria-labelledby={title ? hid : undefined} style={{ scrollMarginTop: 64 }}>
      {(title || end) && (
        <div className="ui-section-h">
          {title && <h2 id={hid}>{title}</h2>}
          {end}
        </div>
      )}
      {children}
      {foot && <p className="ui-section-foot">{foot}</p>}
    </section>
  );
};

export const Row: React.FC<{
  icon?: React.ElementType;
  iconBg?: string;
  title: React.ReactNode;
  sub?: React.ReactNode;
  end?: React.ReactNode;
  onClick?: () => void;
  stack?: boolean;
  children?: React.ReactNode;
}> = ({ icon: Icon, iconBg, title, sub, end, onClick, stack, children }) => {
  const inner = (
    <>
      {Icon && (
        <span className="ui-ico" style={iconBg ? ({ '--ico-bg': iconBg, '--ico-fg': '#fff' } as React.CSSProperties) : undefined}>
          <Icon strokeWidth={2.1} />
        </span>
      )}
      <span className="ui-row-main">
        <b>{title}</b>
        {sub && <span>{sub}</span>}
      </span>
      {end && <span className="ui-row-end">{end}</span>}
    </>
  );
  const cls = `ui-row ${Icon ? 'has-icon' : ''}`;
  if (stack)
    return (
      <div className={`${cls} ui-row-stack`}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12, minWidth: 0 }}>{inner}</div>
        {children}
      </div>
    );
  if (onClick)
    return (
      <button type="button" className={cls} onClick={onClick}>
        {inner}
      </button>
    );
  return <div className={cls}>{inner}</div>;
};
