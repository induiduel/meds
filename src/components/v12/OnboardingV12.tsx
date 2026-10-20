import React, { useEffect, useId, useRef } from 'react';
import { createPortal } from 'react-dom';
import {
  Activity, Archive, ArrowRight, Check, ChevronLeft, ChevronRight, CloudDownload, FileText, Layers, Monitor,
  Search, Smartphone, Sparkles, Tablet, WifiOff, X,
} from 'lucide-react';
import { lockScroll, unlockScroll } from '../../utils/scrollLock';
import { NAV_ITEMS } from '../shell/navModel';
import type { AppRoute } from '../../router';
import '../../styles/v12/entry.css';

/* =============================================================================
 * v12 "Net" — giriş yüzeyleri (canvas: Entry.dc.html + Overlays.dc.html). Önek: e12-.
 * Yalnız html[data-design='v12'] iken çizilir; durum ve işlev çağıran bileşende kalır
 * (Onboarding, WelcomeTour, PwaInstallWelcomeModal), burada yalnız yapı ve görünüm var.
 * ============================================================================= */

const FOCUSABLE = 'a[href],button:not([disabled]),input:not([disabled]),select,textarea,[tabindex]:not([tabindex="-1"])';

/**
 * v12 diyalog kalıbı (Overlays panosu): sola hizalı, 12 px köşe, 1 px çizgi, tek yumuşak gölge, %38 örtü.
 * Telefonda (<640px) alttan açılan sayfa + tutamaç. Esc ve dış tıklama kapatır (dismissable), odak içeride döner.
 */
export const EntryDialogV12: React.FC<{
  labelledBy: string;
  describedBy?: string;
  onClose: () => void;
  width?: number;
  dismissable?: boolean;
  children: React.ReactNode;
}> = ({ labelledBy, describedBy, onClose, width = 440, dismissable = true, children }) => {
  const panelRef = useRef<HTMLDivElement>(null);
  const closeRef = useRef(onClose);
  closeRef.current = onClose;

  useEffect(() => {
    const prev = document.activeElement as HTMLElement | null;
    panelRef.current?.focus({ preventScroll: true });
    lockScroll();
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && dismissable) {
        e.stopPropagation();
        closeRef.current();
      }
      if (e.key === 'Tab' && panelRef.current) {
        const f = panelRef.current.querySelectorAll<HTMLElement>(FOCUSABLE);
        if (!f.length) return;
        const first = f[0];
        const last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault();
          last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
      }
    };
    document.addEventListener('keydown', onKey);
    return () => {
      document.removeEventListener('keydown', onKey);
      unlockScroll();
      prev?.focus?.({ preventScroll: true });
    };
  }, [dismissable]);

  return createPortal(
    <div className="e12-scrim" onMouseDown={(e) => dismissable && e.target === e.currentTarget && onClose()}>
      <div
        ref={panelRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby={labelledBy}
        aria-describedby={describedBy}
        tabIndex={-1}
        className="e12-dlg"
        style={{ '--e12-dlg-w': `${width}px` } as React.CSSProperties}
      >
        {children}
      </div>
    </div>,
    document.body
  );
};

/** Marka: vurgu karesi + kelime (kabuktaki sh-brand ile aynı dil) */
export const BrandV12: React.FC = () => (
  <span className="e12-brand">
    <span className="e12-brand-mark" aria-hidden="true"><Activity strokeWidth={2.4} /></span>
    MeDSor
  </span>
);

/* -----------------------------------------------------------------------------
 * Tanıtım (giriş öncesi): canvas "Tanıtım" kartı — üstte adım noktaları, başlık, metin,
 * küçük örnek ekran; altta Atla · Devam. Son adımda kart giriş/kayıt kartını taşır.
 * --------------------------------------------------------------------------- */

/** Her adımın küçük örnek ekranı: süs, okunmaz (aria-hidden), uydurma sayı içermez */
const Demo: React.FC<{ step: number }> = ({ step }) => {
  if (step === 0) {
    return (
      <div className="e12-demo" aria-hidden="true">
        <div className="e12-demo-field"><span>renin salınımı… makula densa?</span><i className="e12-caret" /></div>
        <span className="e12-demo-meta">Kök, şık ya da tek bir kelime yeter</span>
      </div>
    );
  }
  if (step === 1) {
    return (
      <div className="e12-demo" aria-hidden="true">
        <div className="e12-demo-field is-sm"><Search /><span>renin salınımı… makula densa?</span></div>
        <div className="e12-demo-row"><span className="e12-lead is-acc"><Layers /></span><span className="e12-grow">Benzer çıkmış sorular</span><span className="e12-badge is-acc">Eşleşme</span></div>
        <div className="e12-demo-row"><span className="e12-lead"><FileText /></span><span className="e12-grow">Ders slaytları</span><span className="e12-badge">Kaynak</span></div>
      </div>
    );
  }
  if (step === 2) {
    return (
      <div className="e12-demo" aria-hidden="true">
        <div className="e12-demo-stem"><i style={{ width: '92%' }} /><i style={{ width: '64%' }} /></div>
        {['A', 'B', 'C', 'D'].map((k, n) => (
          <div key={k} className={`e12-demo-opt ${n === 2 ? 'is-ok' : ''}`}>
            <span className="k">{n === 2 ? <Check /> : k}</span>
            <i style={{ width: `${[58, 44, 66, 38][n]}%` }} />
          </div>
        ))}
        <div className="e12-badges"><span className="e12-badge is-ai"><Sparkles /> Yalnız bulunan kaynaklara dayanır</span></div>
      </div>
    );
  }
  return (
    <div className="e12-demo" aria-hidden="true">
      <div className="e12-badges">
        <span className="e12-badge is-acc">Test çöz</span>
        <span className="e12-badge">Slaytları oku</span>
        <span className="e12-badge">Terimleri öğren</span>
      </div>
      <div className="e12-demo-devs">
        <span><Smartphone /> Telefon</span>
        <span><Tablet /> Tablet</span>
        <span><Monitor /> Bilgisayar</span>
      </div>
    </div>
  );
};

export interface OnboardingV12Props {
  steps: { title: string; text: string }[];
  step: number;
  dir: 1 | -1;
  go: (n: number) => void;
  onTouchStart: (e: React.TouchEvent) => void;
  onTouchEnd: (e: React.TouchEvent) => void;
  /** Son adımdaki gömülü giriş / kayıt kartı */
  auth: React.ReactNode;
  /** Tanıtımı (kayıt ekranı dahil) kapatır */
  onClose?: () => void;
}

export const OnboardingV12: React.FC<OnboardingV12Props> = ({ steps, step, dir, go, onTouchStart, onTouchEnd, auth, onClose }) => {
  const last = steps.length - 1;
  const isAuth = step === last;
  const s = steps[step];

  const dots = (
    <div className="e12-dots" role="tablist" aria-label="Tanıtım adımları">
      {steps.map((st, i) => (
        <button
          key={i}
          type="button"
          role="tab"
          aria-selected={i === step}
          aria-label={`${i + 1}. adım: ${st.title}`}
          className={i === step ? 'is-on' : ''}
          onClick={() => go(i)}
        />
      ))}
    </div>
  );

  return (
    <div className="e12-ob" role="dialog" aria-modal="true" aria-label="MeDSor tanıtımı" onTouchStart={onTouchStart} onTouchEnd={onTouchEnd}>
      <div className="e12-ob-top"><BrandV12 /></div>
      <div className="e12-ob-body">
        <div className={`e12-ob-card ${isAuth ? 'is-auth' : ''}`}>
          {isAuth ? (
            <div className="e12-ob-main is-auth">
              <div className="e12-ob-authbar">
                <button type="button" className="e12-btn is-ghost is-sm" onClick={() => go(step - 1)}>
                  <ChevronLeft aria-hidden="true" /> Geri
                </button>
                <span className="e12-grow" />
                {dots}
                {onClose && (
                  <button type="button" className="e12-btn is-ghost is-icon is-sm" onClick={onClose} aria-label="Kapat" title="Kapat, kayıt olmadan devam et">
                    <X aria-hidden="true" />
                  </button>
                )}
              </div>
              <div key={step} className={`e12-ob-step ${dir > 0 ? 'from-right' : 'from-left'} is-auth`}>{auth}</div>
            </div>
          ) : (
            <>
              <div className="e12-ob-main">
                {dots}
                <div key={step} className={`e12-ob-step ${dir > 0 ? 'from-right' : 'from-left'}`}>
                  <h1 className="e12-ob-t">{s.title}</h1>
                  <p className="e12-ob-p">{s.text}</p>
                  <Demo step={step} />
                </div>
              </div>
              <div className="e12-ob-foot">
                {step > 0 && (
                  <button type="button" className="e12-btn is-ghost is-icon" onClick={() => go(step - 1)} aria-label="Geri">
                    <ChevronLeft aria-hidden="true" />
                  </button>
                )}
                <button type="button" className="e12-btn is-ghost" onClick={() => go(last)}>Atla</button>
                <span className="e12-grow" />
                <button type="button" className="e12-btn is-pri" onClick={() => go(step + 1)}>
                  Devam <ChevronRight aria-hidden="true" />
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

/* -----------------------------------------------------------------------------
 * Hoş geldin turu (giriş sonrası): karşılama ve bitiş tam ekran kart; rehberli turda durak kartı.
 * --------------------------------------------------------------------------- */

const RouteIcon: React.FC<{ route: AppRoute; tone?: 'acc' | '' }> = ({ route, tone = '' }) => {
  const it = NAV_ITEMS[route as keyof typeof NAV_ITEMS];
  const Icon = it?.icon || Search;
  return (
    <span className={`e12-lead ${tone ? `is-${tone}` : ''}`} aria-hidden="true">
      <Icon />
    </span>
  );
};

export interface WelcomeFullV12Props {
  phase: 'intro' | 'finish';
  cardRef: React.Ref<HTMLDivElement>;
  first: string;
  stopCount: number;
  pillars: { route: AppRoute; title: string; text: string }[];
  starts: { route: AppRoute; text: string }[];
  onStartTour: () => void;
  onSkip: () => void;
  onPick: (r: AppRoute) => void;
  onBackToTour: () => void;
}

export const WelcomeFullV12: React.FC<WelcomeFullV12Props> = ({ phase, cardRef, first, stopCount, pillars, starts, onStartTour, onSkip, onPick, onBackToTour }) => {
  const intro = phase === 'intro';
  return (
    <div className="e12-wt" role="dialog" aria-modal="true" aria-labelledby="e12-wt-h">
      <div className="e12-wt-top">
        <BrandV12 />
        <span className="e12-grow" />
        <button type="button" className="e12-btn is-ghost is-icon" onClick={onSkip} aria-label="Tanıtımı kapat">
          <X aria-hidden="true" />
        </button>
      </div>
      <div className="e12-wt-body">
        <div ref={cardRef} tabIndex={-1} className="e12-wt-card" key={phase}>
          <div className="e12-wt-main">
            {intro ? (
              <>
                <h1 id="e12-wt-h" className="e12-wt-h">{first ? `Hoş geldin, ${first}` : 'Hoş geldin'}</h1>
                <p className="e12-wt-lead">
                  <span className="e12-wt-state is-acc"><Sparkles aria-hidden="true" /> Hesabın hazır.</span>{' '}
                  MeDSor, Dönem 3 için ders slaytlarını, doğrulanmış çıkmış soruları ve öğrencilerin hatırladıklarını tek yerde toplar.
                  Üç şey için buradasın:
                </p>
                <ul className="e12-list">
                  {pillars.map((p) => (
                    <li key={p.route} className="e12-row">
                      <RouteIcon route={p.route} />
                      <span className="e12-row-t"><b>{p.title}</b><span>{p.text}</span></span>
                    </li>
                  ))}
                </ul>
              </>
            ) : (
              <>
                <h1 id="e12-wt-h" className="e12-wt-h">Nereden başlamak istersin?</h1>
                <p className="e12-wt-lead">
                  <span className="e12-wt-state is-ok"><Check aria-hidden="true" /> Tur bitti.</span>{' '}
                  Seçtiğin sayfa açılır. Turu istediğin zaman Profil ve ayarlar › Hesap ve veri’den yeniden izleyebilirsin.
                </p>
                <ul className="e12-list">
                  {starts.map((s) => (
                    <li key={s.route}>
                      <button type="button" className="e12-row is-btn" onClick={() => onPick(s.route)}>
                        <RouteIcon route={s.route} />
                        <span className="e12-row-t"><b>{NAV_ITEMS[s.route as keyof typeof NAV_ITEMS]?.label}</b><span>{s.text}</span></span>
                        <ChevronRight className="e12-row-chev" aria-hidden="true" />
                      </button>
                    </li>
                  ))}
                </ul>
              </>
            )}
          </div>
          <div className="e12-wt-foot">
            {intro ? (
              <>
                <button type="button" className="e12-btn is-ghost" onClick={onSkip}>Kendim keşfederim</button>
                <span className="e12-grow" />
                <button type="button" className="e12-btn is-pri" onClick={onStartTour}>
                  Kısa turu başlat <span className="e12-btn-sub">{stopCount} durak · 1 dk</span>
                  <ArrowRight aria-hidden="true" />
                </button>
              </>
            ) : (
              <button type="button" className="e12-btn is-ghost" onClick={onBackToTour}>
                <ChevronLeft aria-hidden="true" /> Tura dön
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export interface TourCardV12Props {
  cardRef: React.Ref<HTMLDivElement>;
  place: 'right' | 'above' | 'below' | 'center';
  top: number;
  left: number;
  index: number;
  total: number;
  route: AppRoute;
  title: string;
  text: string;
  points: string[];
  note?: string;
  onPrev: () => void;
  onNext: () => void;
  onClose: () => void;
}

/** Rehberli tur durak kartı: simge + başlık + kapat; metin, maddeler; altta sayaç, ilerleme çubuğu, Önceki · İleri */
export const TourCardV12: React.FC<TourCardV12Props> = ({ cardRef, place, top, left, index, total, route, title, text, points, note, onPrev, onNext, onClose }) => (
  <div
    ref={cardRef}
    tabIndex={-1}
    className={`e12-tc is-${place}`}
    style={place === 'center' ? undefined : { top, left }}
  >
    <div className="e12-tc-h">
      <RouteIcon route={route} tone="acc" />
      <h2 id="wt-t" className="e12-tc-t">{title}</h2>
      <button type="button" className="e12-btn is-ghost is-icon is-sm" onClick={onClose} aria-label="Turu kapat">
        <X aria-hidden="true" />
      </button>
    </div>
    <div className="e12-tc-b" key={index}>
      <p id="wt-d" className="e12-tc-p">{text}</p>
      <ul className="e12-tc-pts">
        {points.map((p) => (
          <li key={p}>{p}</li>
        ))}
      </ul>
      {note && <p className="e12-tc-note">{note}</p>}
    </div>
    <div className="e12-tc-f">
      <span className="e12-tc-n" aria-label={`${total} duraktan ${index + 1}.`}>{index + 1} / {total}</span>
      <span className="e12-bar" aria-hidden="true"><i style={{ transform: `scaleX(${(index + 1) / total})` }} /></span>
      <button type="button" className="e12-btn is-ghost is-icon is-sm" onClick={onPrev} aria-label="Önceki">
        <ChevronLeft aria-hidden="true" />
      </button>
      <button type="button" className="e12-btn is-pri is-sm" onClick={onNext}>
        {index === total - 1 ? 'Bitir' : 'İleri'}
        <ChevronRight aria-hidden="true" />
      </button>
    </div>
  </div>
);

/* -----------------------------------------------------------------------------
 * Uygulamayı ekle / internetsiz çalış (PwaInstallWelcomeModal v12 görünümü)
 * --------------------------------------------------------------------------- */

export const PwaWelcomeV12: React.FC<{ busy: boolean; onLater: () => void; onNever: () => void; onAccept: () => void; onInstallGuide?: () => void }> = ({ busy, onLater, onNever, onAccept, onInstallGuide }) => {
  const id = useId();
  return (
    <EntryDialogV12 labelledBy={`${id}-t`} describedBy={`${id}-d`} onClose={onLater} width={440}>
      <div className="e12-dlg-h">
        <span className="e12-lead is-acc" aria-hidden="true"><CloudDownload /></span>
        <div><h2 id={`${id}-t`}>İnternetsiz de çalışsın mı?</h2></div>
        <button type="button" className="e12-btn is-ghost is-icon is-sm" onClick={onLater} aria-label="Kapat"><X aria-hidden="true" /></button>
      </div>
      <div className="e12-dlg-b">
        <p id={`${id}-d`} className="e12-dlg-lead">Soruları ve dersleri bir kez cihazına indir; metroda, nöbette, sınav salonunun kapısında açılır.</p>
        <ul className="e12-perks">
          <li><span className="e12-lead" aria-hidden="true"><WifiOff /></span><span><b>Bağlantı gerekmez</b><span>Çıkmış sorular, Öğren, Sözlük ve Kartlar cihazında.</span></span></li>
          <li><span className="e12-lead" aria-hidden="true"><Smartphone /></span><span><b>Uygulama gibi</b><span>Ana ekrandan tek dokunuşla, tam ekran açılır.</span></span></li>
          <li><span className="e12-lead" aria-hidden="true"><Archive /></span><span><b>Kendini günceller</b><span>İnternete bağlanınca yeni sorular gelir.</span></span></li>
        </ul>
      </div>
      <div className="e12-dlg-f">
        <button type="button" className="e12-btn is-ghost is-sm" onClick={onNever}>Bir daha sorma</button>
        <span className="e12-grow" />
        {onInstallGuide && (
          <button type="button" className="e12-btn is-sm" onClick={onInstallGuide}>
            <Smartphone aria-hidden="true" /> Ana Ekrana Ekle
          </button>
        )}
        <button type="button" className="e12-btn is-ghost" onClick={onLater}>Sonra</button>
        <button type="button" className="e12-btn is-pri" onClick={onAccept} disabled={busy}>
          <CloudDownload aria-hidden="true" /> İndir
        </button>
      </div>
    </EntryDialogV12>
  );
};
