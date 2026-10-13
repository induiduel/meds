import React, { startTransition, useEffect, useRef, useState } from 'react';

/**
 * Yazarken takılmayan metin kutusu (v11): değer yerel durumda anında güncellenir, üst bileşene
 * `onValue` geçiş önceliğinde (startTransition) iletilir — büyük formlar her tuşta bloklamaz.
 * Dışarıdan gelen değer (öneri seçimi, taslak yükleme) son gönderilenden farklıysa kutuya yazılır.
 */
type Props = Omit<React.TextareaHTMLAttributes<HTMLTextAreaElement>, 'value' | 'onChange' | 'defaultValue'> & {
  value: string;
  onValue: (v: string) => void;
};

export const FastTextarea = React.forwardRef<HTMLTextAreaElement, Props>(({ value, onValue, ...rest }, ref) => {
  const [local, setLocal] = useState(value);
  const sent = useRef(value);
  useEffect(() => {
    if (value !== sent.current) { sent.current = value; setLocal(value); }
  }, [value]);
  return (
    <textarea
      ref={ref}
      {...rest}
      value={local}
      onChange={(e) => {
        const v = e.target.value;
        setLocal(v);
        sent.current = v;
        startTransition(() => onValue(v));
      }}
    />
  );
});
FastTextarea.displayName = 'FastTextarea';
