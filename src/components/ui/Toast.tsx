import React, { useEffect, useState } from 'react';
import { createPortal } from 'react-dom';
import { X } from 'lucide-react';

/**
 * App-wide floating notifications. Call from anywhere:
 *   toast.error('Kaydedilemedi', 'Bağlantını kontrol edip tekrar dene.')
 *   toast.success('Havuza eklendi')
 * Errors stay a little longer and can carry a "Tekrar dene" action.
 */
export type ToastKind = 'error' | 'success' | 'info';
export interface ToastItem {
  id: number;
  kind: ToastKind;
  title: string;
  message?: string;
  action?: { label: string; onClick: () => void };
}

type Listener = (items: ToastItem[]) => void;
let items: ToastItem[] = [];
let nextId = 1;
const listeners = new Set<Listener>();
const emit = () => listeners.forEach((l) => l(items));
const recent = new Map<string, number>();

const push = (kind: ToastKind, title: string, message?: string, action?: ToastItem['action']) => {
  // Same message within 4 s is shown once
  const key = `${kind}|${title}|${message || ''}`;
  const now = Date.now();
  if ((recent.get(key) || 0) > now - 4000) return -1;
  recent.set(key, now);
  const id = nextId++;
  items = [...items, { id, kind, title, message, action }].slice(-4);
  emit();
  window.setTimeout(() => dismiss(id), kind === 'error' ? 7000 : 4200);
  return id;
};

export const dismiss = (id: number) => {
  items = items.filter((t) => t.id !== id);
  emit();
};

export const toast = {
  error: (title: string, message?: string, action?: ToastItem['action']) => push('error', title, message, action),
  success: (title: string, message?: string) => push('success', title, message),
  info: (title: string, message?: string) => push('info', title, message),
};

// ---------------------------------------------------------------------------
// Little faces: the capsule mascot, worried for errors and happy for success
// ---------------------------------------------------------------------------
const Face: React.FC<{ kind: ToastKind }> = ({ kind }) => {
  const color = kind === 'error' ? '#E0566E' : kind === 'success' ? '#1F9D55' : '#1E4FD8';
  return (
    <svg width="44" height="44" viewBox="0 0 48 48" aria-hidden="true" className={kind === 'error' ? 'ms-wobble' : 'ms-float'}>
      <g transform="rotate(-16 24 24)">
        <rect x="13" y="6" width="22" height="36" rx="11" fill="#FFFFFF" stroke="#0E1A26" strokeWidth="2" />
        <path d="M13 24v-7a11 11 0 0 1 22 0v7z" fill={color} stroke="#0E1A26" strokeWidth="2" strokeLinejoin="round" />
        <g className="ms-blink">
          <circle cx="20" cy="30" r="1.7" fill="#0E1A26" />
          <circle cx="28" cy="30" r="1.7" fill="#0E1A26" />
        </g>
        {kind === 'error' ? (
          <>
            <path d="M21 36q3-2.4 6 0" stroke="#0E1A26" strokeWidth="1.8" strokeLinecap="round" fill="none" />
            <path className="ms-drop" d="M31.5 25.5c1.4 1.8 1.4 3.2 0 3.8-1.4-.6-1.4-2 0-3.8z" fill="#6AA8F5" />
          </>
        ) : (
          <path d="M21 34.5q3 2.6 6 0" stroke="#0E1A26" strokeWidth="1.8" strokeLinecap="round" fill="none" />
        )}
      </g>
    </svg>
  );
};

const TONE: Record<ToastKind, { ring: string; title: string; bar: string }> = {
  error: { ring: 'border-rose-200', title: 'text-rose-700', bar: 'bg-rose-500' },
  success: { ring: 'border-emerald-200', title: 'text-ok', bar: 'bg-ok-bright' },
  info: { ring: 'border-accent/20', title: 'text-accent', bar: 'bg-accent' },
};

/** Mount once (App). Renders inside the fullscreen element when one is active. */
export const ToastHost: React.FC = () => {
  const [list, setList] = useState<ToastItem[]>(items);
  const [host, setHost] = useState<Element | null>(null);

  useEffect(() => {
    const l: Listener = (next) => setList(next);
    listeners.add(l);
    const fs = () => setHost(document.fullscreenElement);
    document.addEventListener('fullscreenchange', fs);
    fs();
    return () => {
      listeners.delete(l);
      document.removeEventListener('fullscreenchange', fs);
    };
  }, []);

  if (typeof document === 'undefined') return null;
  const ui = (
    <div
      aria-live="assertive"
      className="pointer-events-none fixed z-[100000] left-0 right-0 bottom-[calc(84px+env(safe-area-inset-bottom))] md:bottom-6 px-3 flex flex-col items-center md:items-end md:right-6 md:left-auto gap-2 print:hidden"
    >
      {list.map((t) => {
        const tone = TONE[t.kind];
        return (
          <div
            key={t.id}
            role={t.kind === 'error' ? 'alert' : 'status'}
            className={`ms-toast-in pointer-events-auto relative w-full max-w-[400px] overflow-hidden rounded-2xl bg-white border ${tone.ring} shadow-lg pl-2.5 pr-2 py-2.5 flex items-center gap-2.5`}
          >
            <Face kind={t.kind} />
            <div className="flex-1 min-w-0">
              <p className={`m-0 text-[14.5px] font-semibold leading-snug ${tone.title}`}>{t.title}</p>
              {t.message && <p className="m-0 mt-0.5 text-[13.5px] text-ink-2 leading-snug break-words">{t.message}</p>}
              {t.action && (
                <button
                  type="button"
                  onClick={() => {
                    dismiss(t.id);
                    t.action!.onClick();
                  }}
                  className="mt-1.5 h-8 px-3 rounded-lg bg-canvas hover:bg-line-soft text-[13px] font-semibold text-ink cursor-pointer"
                >
                  {t.action.label}
                </button>
              )}
            </div>
            <button
              type="button"
              onClick={() => dismiss(t.id)}
              aria-label="Bildirimi kapat"
              className="self-start w-8 h-8 rounded-full flex items-center justify-center text-ink-3 hover:text-ink hover:bg-canvas cursor-pointer shrink-0"
            >
              <X className="w-4 h-4" />
            </button>
            <span className={`ms-toast-timer absolute left-0 bottom-0 h-[3px] ${tone.bar}`} style={{ animationDuration: t.kind === 'error' ? '7s' : '4.2s' }} />
          </div>
        );
      })}
    </div>
  );
  return createPortal(ui, host || document.body);
};

// ---------------------------------------------------------------------------
// Global safety net: failed actions that only used alert() or threw silently
// ---------------------------------------------------------------------------
const ERROR_WORDS = /hata|başarısız|basarisiz|yapılamadı|kaydedilemedi|yüklenemedi|gönderilemedi|oluşturulamadı|bulunamadı|olmadı|ulaşılamadı|error|failed/i;
const BENIGN = /websocket|vite|hmr|resizeobserver|aborterror|the user aborted|load failed|failed to fetch dynamically/i;

let installed = false;
/** Routes window.alert() and unhandled promise rejections into toasts. Call once at startup. */
export const installToastBridge = () => {
  if (installed || typeof window === 'undefined') return;
  installed = true;

  window.alert = (msg?: any) => {
    const text = String(msg ?? '').trim();
    if (!text) return;
    const [first, ...rest] = text.split(/\n+|:\s(?=.)/);
    if (ERROR_WORDS.test(text)) toast.error(first.length > 70 ? 'İşlem tamamlanamadı' : first, first.length > 70 ? text : rest.join(': ') || undefined);
    else toast.info(first.length > 70 ? 'Bilgi' : first, first.length > 70 ? text : rest.join(': ') || undefined);
  };

  window.addEventListener('unhandledrejection', (e) => {
    const reason: any = e.reason;
    const msg = String(reason?.message || reason || '');
    if (!msg || BENIGN.test(msg) || e.defaultPrevented) return;
    toast.error('Bir işlem tamamlanamadı', msg.length > 160 ? msg.slice(0, 157) + '…' : msg);
  });
};
