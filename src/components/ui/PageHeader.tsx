import React from 'react';

/**
 * Tüm sayfaların ortak başlığı: küçük üst etiket, büyük başlık, açıklama,
 * sağda eylemler ve isteğe bağlı istatistik satırı. Dar ekranda eylemler alta iner.
 */
export interface PageStat {
  label: string;
  value: React.ReactNode;
  tone?: 'default' | 'accent' | 'ok' | 'warn';
}

const TONE: Record<NonNullable<PageStat['tone']>, string> = {
  default: 'text-ink',
  accent: 'text-accent',
  ok: 'text-ok',
  warn: 'text-warn',
};

export const PageHeader: React.FC<{
  eyebrow?: React.ReactNode;
  title: React.ReactNode;
  description?: React.ReactNode;
  actions?: React.ReactNode;
  stats?: PageStat[];
  className?: string;
  children?: React.ReactNode;
}> = ({ eyebrow, title, description, actions, stats, className = '', children }) => (
  <header className={`flex flex-col gap-3 ${className}`}>
    <div className="flex flex-wrap items-end justify-between gap-x-6 gap-y-3">
      <div className="min-w-0 flex flex-col gap-1.5 max-w-3xl">
        {eyebrow && <span className="ms-eyebrow">{eyebrow}</span>}
        <h1 className="ms-page-title m-0 text-[24px] sm:text-[28px] text-ink">{title}</h1>
        {description && <p className="m-0 text-[14px] leading-relaxed text-ink-2">{description}</p>}
      </div>
      {actions && <div className="flex flex-wrap items-center gap-2 shrink-0">{actions}</div>}
    </div>
    {stats && stats.length > 0 && (
      <dl className="ms-stats m-0 flex flex-wrap gap-2">
        {stats.map((s) => (
          <div key={s.label} className="min-w-[112px] bg-white border border-line rounded-xl px-3 py-2 flex flex-col">
            <dt className="text-[11.5px] font-medium text-ink-3">{s.label}</dt>
            <dd className={`m-0 text-[17px] font-bold font-mono tracking-tight ${TONE[s.tone || 'default']}`}>{s.value}</dd>
          </div>
        ))}
      </dl>
    )}
    {children}
  </header>
);
