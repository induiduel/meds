import React, { useState } from 'react';
import { ChevronDown } from 'lucide-react';

interface CollapsibleProps {
  title: React.ReactNode;
  count?: number;
  defaultOpen?: boolean;
  open?: boolean;
  onToggle?: (open: boolean) => void;
  className?: string;
  /** Başlık satırı küçük baloncuk (chip) olarak çizilir */
  bubble?: boolean;
  children: React.ReactNode;
}

/** Açılır/kapanır liste: yükseklik grid-rows 0fr → 1fr ile akıcı geçer. */
export const Collapsible: React.FC<CollapsibleProps> = ({
  title, count, defaultOpen = false, open, onToggle, className = '', bubble = false, children,
}) => {
  const [inner, setInner] = useState(defaultOpen);
  const isOpen = open ?? inner;
  const toggle = () => {
    const next = !isOpen;
    if (open === undefined) setInner(next);
    onToggle?.(next);
  };

  return (
    <div className={`ms-collapsible ${isOpen ? 'is-open' : ''} ${bubble ? 'is-bubble' : ''} ${className}`}>
      <button type="button" className="ms-collapsible-head" aria-expanded={isOpen} onClick={toggle}>
        <span className="min-w-0 flex-1 truncate text-left">{title}</span>
        {typeof count === 'number' && <span className="ms-collapsible-count">{count}</span>}
        <ChevronDown className="ms-collapsible-chev w-4 h-4 shrink-0" />
      </button>
      <div className="ms-collapsible-body" aria-hidden={!isOpen}>
        <div className="min-h-0 overflow-hidden">
          <div className="ms-collapsible-inner">{children}</div>
        </div>
      </div>
    </div>
  );
};
