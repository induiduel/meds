import React, { useId, useState } from 'react';
import { ChevronDown } from 'lucide-react';

interface FilterGroupProps {
  title: string;
  /** Kapalıyken başlığın yanında görünen kısa özet ("Patoloji", "2 seçili"). */
  summary?: string;
  defaultOpen?: boolean;
  /** Başlık satırının sağındaki ek düğme (ör. "Temizle"). */
  action?: React.ReactNode;
  children: React.ReactNode;
}

/** Açılır-kapanır süzgeç bölümü: yükseklik grid satırıyla akıcı biçimde açılır, içerik akışta kalır. */
export const FilterGroup: React.FC<FilterGroupProps> = ({ title, summary, defaultOpen = true, action, children }) => {
  const [open, setOpen] = useState(defaultOpen);
  const bodyId = useId();
  return (
    <section className="ui-section rb-fg">
      <div className="ui-section-h rb-fg-h">
        <button type="button" className="rb-fg-t" aria-expanded={open} aria-controls={bodyId} onClick={() => setOpen((v) => !v)}>
          <h2>{title}</h2>
          {!open && summary && <span className="rb-fg-s">{summary}</span>}
          <ChevronDown className={`rb-fg-c ${open ? 'is-open' : ''}`} aria-hidden />
        </button>
        {action}
      </div>
      <div id={bodyId} className={`rb-fg-b ${open ? 'is-open' : ''}`}>
        <div className="rb-fg-in" inert={!open ? true : undefined}>
          {children}
        </div>
      </div>
    </section>
  );
};
