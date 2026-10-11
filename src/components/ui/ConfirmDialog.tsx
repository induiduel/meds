import React, { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { AlertTriangle, HelpCircle } from 'lucide-react';

/**
 * Uyarı diyaloğu (v8). Tarayıcının confirm() penceresinin yerine:
 *   if (!(await confirmDialog({ title: 'Not silinsin mi?', confirmLabel: 'Sil', tone: 'danger' }))) return;
 * Başlık bir soru, eylem düğmesi eylemi adlandırır; odak güvenli seçenekte (Vazgeç), Esc ve dış tıklama vazgeçer.
 * ConfirmHost uygulamaya bir kez bağlanır (App). Bağlı değilse window.confirm'e düşer.
 */
export interface ConfirmOptions {
  title: string;
  message?: string;
  confirmLabel?: string;
  cancelLabel?: string;
  tone?: 'danger' | 'default';
}
type Req = ConfirmOptions & { resolve: (v: boolean) => void };

let push: ((r: Req) => void) | null = null;

export const confirmDialog = (o: ConfirmOptions): Promise<boolean> =>
  new Promise((resolve) => {
    if (!push) {
      resolve(window.confirm([o.title, o.message].filter(Boolean).join('\n\n')));
      return;
    }
    push({ ...o, resolve });
  });

export const ConfirmHost: React.FC = () => {
  const [req, setReq] = useState<Req | null>(null);
  const [closing, setClosing] = useState(false);
  const cancelRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    push = (r) => {
      setClosing(false);
      setReq((cur) => {
        cur?.resolve(false);
        return r;
      });
    };
    return () => {
      push = null;
    };
  }, []);

  const done = (v: boolean) => {
    if (!req || closing) return;
    const r = req;
    setClosing(true);
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    window.setTimeout(() => {
      setReq(null);
      setClosing(false);
      r.resolve(v);
    }, reduce ? 0 : 160);
  };

  useEffect(() => {
    if (!req) return;
    const prev = document.activeElement as HTMLElement | null;
    cancelRef.current?.focus();
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        e.stopImmediatePropagation();
        done(false);
      }
    };
    document.addEventListener('keydown', onKey, true);
    return () => {
      document.removeEventListener('keydown', onKey, true);
      prev?.focus?.();
    };
  }, [req]);

  if (!req) return null;
  const danger = req.tone === 'danger';
  const Icon = danger ? AlertTriangle : HelpCircle;
  return createPortal(
    <div className={`cf-root ${closing ? 'is-closing' : ''}`} onMouseDown={(e) => e.target === e.currentTarget && done(false)}>
      <div role="alertdialog" aria-modal="true" aria-labelledby="cf-t" aria-describedby={req.message ? 'cf-m' : undefined} className={`cf ${danger ? 'is-danger' : ''}`}>
        <span className="cf-ic" aria-hidden><Icon /></span>
        <h2 id="cf-t" className="cf-t">{req.title}</h2>
        {req.message && <p id="cf-m" className="cf-m">{req.message}</p>}
        <div className="cf-acts">
          <button ref={cancelRef} type="button" className="ui-btn" onClick={() => done(false)}>{req.cancelLabel || 'Vazgeç'}</button>
          <button type="button" className={`ui-btn ${danger ? 'cf-danger' : 'is-primary'}`} onClick={() => done(true)}>{req.confirmLabel || 'Tamam'}</button>
        </div>
      </div>
    </div>,
    document.body
  );
};

/** confirm() metnini olduğu gibi alır: ilk satır başlık, kalanı açıklama; silme/ban sözcüklerinde kırmızı ton. */
export const confirmText = (text: string, confirmLabel?: string) => {
  const [first, ...rest] = String(text).split(/\n+/);
  const danger = /sil|ban|kaldır|geri al|temizle|kalıcı/i.test(text);
  return confirmDialog({
    title: first.trim(),
    message: rest.join('\n').trim() || undefined,
    confirmLabel: confirmLabel || (danger ? (/ban/i.test(text) ? 'Sil ve banla' : /geri al/i.test(text) ? 'Geri al' : 'Sil') : 'Devam et'),
    tone: danger ? 'danger' : 'default',
  });
};
