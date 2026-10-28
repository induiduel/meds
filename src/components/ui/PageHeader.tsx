import React from 'react';
import '../../styles/ayrik-cx.css';

/**
 * Tüm sayfaların ortak başlığı — Çıkmış sorular dili: büyük başlık + yanında canlı mono sayaç,
 * sağda sessiz araçlar. Açıklama tek sakin satırdır (telefonda gizlenir). İstatistikler kutu değil,
 * başlığın yanındaki sayacın parçasıdır: "66 ders · 8.774 soru".
 */
export interface PageStat {
  label: string;
  value: React.ReactNode;
  tone?: 'default' | 'accent' | 'ok' | 'warn';
}

const lower = (s: string) => s.toLocaleLowerCase('tr-TR');

export const PageHeader: React.FC<{
  /** Eski üst etiket; başlık kendi ağırlığını taşır, gösterilmez */
  eyebrow?: React.ReactNode;
  title: React.ReactNode;
  description?: React.ReactNode;
  actions?: React.ReactNode;
  stats?: PageStat[];
  className?: string;
  children?: React.ReactNode;
}> = ({ title, description, actions, stats, className = '', children }) => (
  <header className={`cx-page ${className}`}>
    <div className="cx-head">
      <h1 className="ms-page-title cx-title">{title}</h1>
      {stats && stats.length > 0 && (
        <span className="cx-count" aria-live="polite">
          {stats.map((s, i) => (
            <span key={s.label} className={`cx-stat ${s.tone && s.tone !== 'default' ? `is-${s.tone}` : ''}`}>
              {i > 0 && <i aria-hidden>·</i>}
              {s.value} <small>{lower(s.label)}</small>
            </span>
          ))}
        </span>
      )}
      {actions && <div className="cx-head-tools ms-ph-actions">{actions}</div>}
    </div>
    {description && <p className="ms-page-desc cx-desc">{description}</p>}
    {children}
  </header>
);
