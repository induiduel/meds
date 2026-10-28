import React, { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { AlertCircle, Check, Info, MessageCircle, Send, UserPlus, X } from 'lucide-react';

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
  /** geri al bildirimi: sağda 6 sn'lik geri sayım halkası */
  undo?: boolean;
  /** zengin (sohbet / arkadaşlık) bildirimi: ekranın üstünde, etkileşimli */
  rich?: RichToast;
}
export interface RichToast {
  variant: 'mesaj' | 'arkadas' | 'davet';
  ad: string;
  title: string;
  message?: string;
  /** kartın kendisine tıklanınca */
  onOpen?: () => void;
  /** 'Kabul' / 'Reddet' gibi düğmeler; çözülürse kart kapanır, hata dizesi dönerse kartta gösterilir */
  actions?: { label: string; primary?: boolean; run: () => Promise<string | void> | string | void }[];
  /** satır içi hızlı yanıt (yalnız sohbet); hata dizesi dönerse gösterilir */
  reply?: (metin: string) => Promise<string | void>;
}
const RICH_MS = 9000;

type Listener = (items: ToastItem[]) => void;
let items: ToastItem[] = [];
let nextId = 1;
const listeners = new Set<Listener>();
const emit = () => listeners.forEach((l) => l(items));
const recent = new Map<string, number>();

// Bildirim geçmişi: her toast (kısa onaylar hariç) kullanıcının profil bildirimlerine de yazılır.
// Kaydedici userNotificationService tarafından bağlanır (içe aktarma döngüsü olmasın diye).
type ToastRecorder = (kind: ToastKind, title: string, message?: string) => void;
let recorder: ToastRecorder | null = null;
export const setToastRecorder = (fn: ToastRecorder | null) => {
  recorder = fn;
};

const push = (kind: ToastKind, title: string, message?: string, action?: ToastItem['action'], record = true) => {
  // Same message within 4 s is shown once
  const key = `${kind}|${title}|${message || ''}`;
  const now = Date.now();
  if ((recent.get(key) || 0) > now - 4000) return -1;
  recent.set(key, now);
  if (record && recorder) {
    try {
      recorder(kind, title, message);
    } catch {
      /* geçmiş yazılamazsa toast yine görünür */
    }
  }
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

/** Geri alınabilir işlem (tasarım AB12): "… silindi · Geri al", 6 sn; bildirim geçmişine yazılmaz */
export const geriAlinabilir = (title: string, geriAl: () => void) => {
  const id = nextId++;
  items = [...items, { id, kind: 'info' as ToastKind, title, action: { label: 'Geri al', onClick: geriAl }, undo: true }].slice(-4);
  emit();
  window.setTimeout(() => dismiss(id), 6000);
  return id;
};

/** Sohbet mesajı / arkadaşlık isteği: üstte kayan, hover'da duran, düğmeli ve hızlı yanıtlı kart. */
export const richToast = (rich: RichToast) => {
  const id = nextId++;
  items = [...items.filter((t) => !(t.rich && t.rich.variant === rich.variant && t.rich.ad === rich.ad && t.rich.title === rich.title)), { id, kind: 'info' as ToastKind, title: rich.title, message: rich.message, rich }].slice(-6);
  emit();
  return id;
};

export const toast = {
  error: (title: string, message?: string, action?: ToastItem['action']) => push('error', title, message, action),
  success: (title: string, message?: string, action?: ToastItem['action']) => push('success', title, message, action),
  info: (title: string, message?: string, action?: ToastItem['action']) => push('info', title, message, action),
  /** Geçmişe yazmadan göster (zaten bildirim geçmişinde olan bir kaydı duyurmak için). */
  show: (kind: ToastKind, title: string, message?: string) => push(kind, title, message, undefined, false),
};

/** Mount once (App). Renders inside the fullscreen element when one is active. */
const basHarf = (s: string) => s.split(/\s+/).filter(Boolean).slice(0, 2).map((w) => w[0]).join('').toLocaleUpperCase('tr-TR') || '?';

const RichCard: React.FC<{ t: ToastItem }> = ({ t }) => {
  const r = t.rich!;
  const [hata, setHata] = useState('');
  const [mesgul, setMesgul] = useState(false);
  const [yanit, setYanit] = useState('');
  const [yazma, setYazma] = useState(false);
  const [bitti, setBitti] = useState('');
  const dur = useRef(false);
  const kalan = useRef(RICH_MS);
  useEffect(() => {
    let son = Date.now();
    const iv = window.setInterval(() => {
      const now = Date.now();
      if (!dur.current) kalan.current -= now - son;
      son = now;
      if (kalan.current <= 0) dismiss(t.id);
    }, 200);
    return () => window.clearInterval(iv);
  }, [t.id]);
  const calistir = async (fn: () => Promise<string | void> | string | void, tamam?: string) => {
    setMesgul(true); setHata('');
    try {
      const h = await fn();
      if (h) setHata(h);
      else if (tamam) { setBitti(tamam); kalan.current = 1600; }
      else dismiss(t.id);
    } catch { setHata('İşlem yapılamadı.'); }
    setMesgul(false);
  };
  const gonder = (e: React.FormEvent) => {
    e.preventDefault();
    const m = yanit.trim();
    if (!m || !r.reply) return;
    void calistir(async () => { const h = await r.reply!(m); if (!h) setYanit(''); return h; }, 'Yanıt gönderildi');
  };
  return (
    <div role="status" className={`tst-rich is-${r.variant}`} onMouseEnter={() => (dur.current = true)} onMouseLeave={() => (dur.current = yazma)}>
      <div className="tst-rich-row">
        <span className="tst-rich-av" aria-hidden>{basHarf(r.ad)}<i>{r.variant === 'mesaj' ? <MessageCircle /> : <UserPlus />}</i></span>
        <button type="button" className="tst-rich-body" onClick={() => { dismiss(t.id); r.onOpen?.(); }}>
          <span className="tst-rich-t">{bitti || r.title}</span>
          {!bitti && r.message && <span className="tst-rich-m">{r.message}</span>}
        </button>
        <button type="button" className="tst-x" onClick={() => dismiss(t.id)} aria-label="Bildirimi kapat"><X /></button>
      </div>
      {!bitti && (r.actions?.length || r.reply) && (
        <div className="tst-rich-act">
          {r.actions?.map((a) => (
            <button key={a.label} type="button" disabled={mesgul} className={a.primary ? 'is-primary' : ''} onClick={() => calistir(a.run, a.primary ? 'Tamam' : undefined)}>{a.label}</button>
          ))}
          {r.reply && !yazma && <button type="button" onClick={() => { setYazma(true); dur.current = true; }}>Hızlı yanıt</button>}
        </div>
      )}
      {!bitti && yazma && r.reply && (
        <form className="tst-rich-form" onSubmit={gonder}>
          <input autoFocus value={yanit} maxLength={500} onChange={(e) => setYanit(e.target.value)} placeholder="Yanıt yaz…" aria-label="Hızlı yanıt" />
          <button type="submit" disabled={mesgul || !yanit.trim()} aria-label="Gönder"><Send /></button>
        </form>
      )}
      {hata && <p className="tst-rich-err">{hata}</p>}
    </div>
  );
};

export const ToastHost: React.FC = () => {
  const [list, setList] = useState<ToastItem[]>(items);
  const [host, setHost] = useState<Element | null>(null);

  useEffect(() => {
    const l: Listener = (next) => setList(next);
    listeners.add(l);
    const fs = () => setHost(document.fullscreenElement || (document as any).webkitFullscreenElement || null);
    document.addEventListener('fullscreenchange', fs);
    document.addEventListener('webkitfullscreenchange', fs);
    fs();
    return () => {
      listeners.delete(l);
      document.removeEventListener('fullscreenchange', fs);
      document.removeEventListener('webkitfullscreenchange', fs);
    };
  }, []);

  if (typeof document === 'undefined') return null;
      // v8: sade kapsül. Durum simgesi + başlık + mesaj + eylem; en yeni altta, en çok 3; zamanlayıcı alt çizgide
  const ICON: Record<ToastKind, React.ElementType> = { error: AlertCircle, success: Check, info: Info };
  const v8 = (
    <div aria-live="polite" className="tst-host print:hidden">
      {list.filter((t) => !t.rich).slice(-3).map((t) => {
        const Icon = ICON[t.kind];
        return (
          <div key={t.id} role={t.kind === 'error' ? 'alert' : 'status'} className={`tst is-${t.kind}`}>
            <span className="tst-ic" aria-hidden><Icon strokeWidth={2.6} /></span>
            <div className="tst-body">
              <p className="tst-t">{t.title}</p>
              {t.message && <p className="tst-m">{t.message}</p>}
            </div>
            {t.action && (
              <button type="button" className="tst-act" onClick={() => { dismiss(t.id); t.action!.onClick(); }}>
                {t.action.label}
              </button>
            )}
            <button type="button" className="tst-x" onClick={() => dismiss(t.id)} aria-label="Bildirimi kapat"><X /></button>
            <span className="tst-timer" style={{ animationDuration: t.undo ? '6s' : t.kind === 'error' ? '7s' : '4.2s' }} />
          </div>
        );
      })}
    </div>
  );
  const ust = list.filter((t) => t.rich).slice(-3);
  return createPortal(<>{v8}{ust.length > 0 && <div aria-live="polite" className="tst-top-host print:hidden">{ust.map((t) => <RichCard key={t.id} t={t} />)}</div>}</>, host || document.body);
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
