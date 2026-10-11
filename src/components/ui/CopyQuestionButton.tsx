import React, { useEffect, useRef, useState } from 'react';
import { Check, Copy } from 'lucide-react';
import { copyQuestion, CopyOption } from '../../utils/copyQuestion';
import { toast } from './Toast';

interface Props {
  stem: string;
  options: CopyOption[] | Record<string, string>;
  className?: string;
}

/** Soru kartı başlığındaki tek tıkla kopyala düğmesi: yalnız kök ve şıklar panoya gider. */
export const CopyQuestionButton: React.FC<Props> = ({ stem, options, className = '' }) => {
  const [done, setDone] = useState(false);
  const timer = useRef<number | undefined>(undefined);
  useEffect(() => () => window.clearTimeout(timer.current), []);

  const onClick = async () => {
    const ok = await copyQuestion(stem, options);
    if (!ok) {
      toast.error('Kopyalanamadı', 'Tarayıcı panoya erişime izin vermedi.');
      return;
    }
    setDone(true);
    toast.success('Soru kopyalandı', 'Soru kökü ve şıklar panoya kopyalandı.');
    window.clearTimeout(timer.current);
    timer.current = window.setTimeout(() => setDone(false), 1800);
  };

  const label = done ? 'Kopyalandı' : 'Soru kökünü ve şıkları kopyala';
  return (
    <button
      type="button"
      onClick={onClick}
      aria-label={label}
      title={label}
      className={`h-9 w-9 shrink-0 rounded-[10px] border inline-flex items-center justify-center cursor-pointer transition-colors ${
        done ? 'text-ok border-ok/40 bg-ok-soft' : 'text-ink-2 bg-white border-line hover:border-line-2 hover:text-ink'
      } ${className}`}
    >
      {done ? <Check className="w-4 h-4" strokeWidth={2.4} /> : <Copy className="w-4 h-4" />}
    </button>
  );
};
