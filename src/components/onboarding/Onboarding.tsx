import React, { Suspense, useEffect, useRef, useState } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import type { AppUser } from '../../services/auth';
import { useAppearance } from '../../utils/appearance';
import { OnboardingV12 } from '../v12/OnboardingV12';

const UserAuthModal = React.lazy(() => import('../UserAuthModal').then(m => ({ default: m.UserAuthModal || (m as any).default })));

/* ------------------------------------------------------------------
 * Tanıtım: 4 animasyonlu sahne + 5. adımda kayıt / giriş.
 * ------------------------------------------------------------------ */
const STEPS = [
  { title: 'Hatırladığını yaz', text: 'Sınavdan aklında kalan birkaç kelime yeterli. Parçaları herkes birlikte tamamlar.' },
  { title: 'Kaynaklardan bulunur', text: 'Ders slaytları ve çıkmış sorular taranır; en yakın eşleşmeler önüne gelir.' },
  { title: 'Soru yeniden kurulur', text: 'Yapay zekâ, yalnızca bulunan kaynaklara dayanarak sorunun tam hâlini yazar.' },
  { title: 'Çalış, tekrar et', text: 'Test çöz, slaytları oku, terimleri dokunarak öğren. Telefon, tablet, bilgisayar.' },
  { title: 'Hadi başlayalım', text: 'Katkılarını takip etmek için hesabını oluştur ya da giriş yap.' },
];

const Scene: React.FC<{ step: number }> = ({ step }) => {
  // Lottie benzeri, saf SVG + CSS animasyonları (ek kütüphane yok, hızlı açılır)
  if (step === 0) {
    return (
      <svg viewBox="0 0 200 160" className="ms-scene">
        <rect x="30" y="28" width="140" height="104" rx="16" className="sc-card" />
        <rect x="48" y="52" width="0" height="8" rx="4" className="sc-ink sc-type1" />
        <rect x="48" y="70" width="0" height="8" rx="4" className="sc-ink sc-type2" />
        <rect x="48" y="88" width="0" height="8" rx="4" className="sc-accent sc-type3" />
        <rect x="140" y="104" width="2" height="14" className="sc-caret" />
      </svg>
    );
  }
  if (step === 1) {
    return (
      <svg viewBox="0 0 200 160" className="ms-scene">
        <rect x="38" y="36" width="92" height="74" rx="12" className="sc-card sc-stack3" />
        <rect x="50" y="46" width="92" height="74" rx="12" className="sc-card sc-stack2" />
        <rect x="62" y="56" width="92" height="74" rx="12" className="sc-card sc-stack1" />
        <g className="sc-lens">
          <circle cx="0" cy="0" r="20" className="sc-lens-ring" />
          <line x1="14" y1="14" x2="28" y2="28" className="sc-lens-handle" />
        </g>
      </svg>
    );
  }
  if (step === 2) {
    return (
      <svg viewBox="0 0 200 160" className="ms-scene">
        <rect x="40" y="24" width="120" height="112" rx="16" className="sc-card" />
        {[0, 1, 2, 3].map(i => (
          <g key={i} className="sc-opt" style={{ animationDelay: `${0.25 + i * 0.18}s` }}>
            <circle cx="62" cy={52 + i * 22} r="6" className={i === 2 ? 'sc-accent' : 'sc-dim'} />
            <rect x="76" y={49 + i * 22} width={60 - i * 6} height="6" rx="3" className="sc-ink" />
          </g>
        ))}
        <path d="M58 96 l4 4 l8 -8" className="sc-check" />
      </svg>
    );
  }
  if (step === 3) {
    return (
      <svg viewBox="0 0 200 160" className="ms-scene">
        <rect x="20" y="40" width="96" height="70" rx="10" className="sc-card sc-dev1" />
        <rect x="104" y="30" width="58" height="84" rx="10" className="sc-card sc-dev2" />
        <rect x="150" y="62" width="32" height="58" rx="8" className="sc-card sc-dev3" />
        <path d="M60 128 q40 -22 80 0" className="sc-arc" />
      </svg>
    );
  }
  return (
    <svg viewBox="0 0 200 160" className="ms-scene">
      <circle cx="100" cy="68" r="30" className="sc-card sc-pop" />
      <circle cx="100" cy="60" r="11" className="sc-accent" />
      <path d="M80 88 q20 -18 40 0" className="sc-arc" />
    </svg>
  );
};

/** v15 tasarımı (I02–I04): üç tanıtım + giriş (I05) */
const STEPS_V15 = [
  { title: 'Dinlerken PDF’in seni takip etsin', text: 'Hocanın anlattığı cümle metinde ve PDF’te aynı anda işaretlenir.' },
  { title: 'Yanlışın anında açıklanır', text: 'Her şık için ne olduğu, ne işe yaradığı ve neden doğru ya da yanlış olduğu.' },
  { title: 'Hücreni büyüt', text: 'Çalıştıkça glukoz, başardıkça DNA kazan; hücren evrimleşsin.' },
  { title: 'Hesabına gir', text: '' },
];

interface OnboardingProps {
  onAuthSuccess: (user: AppUser, token?: string | null) => void;
  onClose?: () => void;
}

export const Onboarding: React.FC<OnboardingProps> = ({ onAuthSuccess, onClose }) => {
  const [step, setStep] = useState(0);
  const [dir, setDir] = useState<1 | -1>(1);
  const touchX = useRef<number | null>(null);
  const gor = useAppearance();
  const v12 = gor.design === 'v12';
  const adimlar = gor.v15 ? STEPS_V15 : STEPS;
  const last = adimlar.length - 1;

  const go = (n: number) => {
    const next = Math.max(0, Math.min(last, n));
    if (next === step) return;
    setDir(next > step ? 1 : -1);
    setStep(next);
  };

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.target as HTMLElement)?.closest('input,textarea,select')) return;
      if (e.key === 'ArrowRight') go(step + 1);
      if (e.key === 'ArrowLeft') go(step - 1);
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  });

  const s = adimlar[step] || adimlar[last];
  const isAuth = step === last;
  const onTouchStart = (e: React.TouchEvent) => { if (!isAuth) touchX.current = e.touches[0].clientX; };
  const onTouchEnd = (e: React.TouchEvent) => {
    if (touchX.current == null) return;
    const dx = e.changedTouches[0].clientX - touchX.current;
    touchX.current = null;
    if (Math.abs(dx) > 50) go(step + (dx < 0 ? 1 : -1));
  };

  if (v12) {
    return (
      <OnboardingV12
        steps={adimlar}
        step={step}
        dir={dir}
        go={go}
        onTouchStart={onTouchStart}
        onTouchEnd={onTouchEnd}
        onClose={onClose}
        auth={
          <Suspense fallback={<div className="e12-auth-skel" aria-hidden="true" />}>
            <UserAuthModal isOpen embedded mandatory onClose={() => {}} onAuthSuccess={onAuthSuccess} initialMode={gor.v15 ? 'login' : 'register'} />
          </Suspense>
        }
      />
    );
  }

  return (
    <div
      className="ms-onboard"
      role="dialog"
      aria-modal="true"
      aria-label="MeDSor tanıtımı"
      onTouchStart={onTouchStart}
      onTouchEnd={onTouchEnd}
    >
      <div className="ms-onboard-top">
        <span className="ms-onboard-brand">Me<span>DS</span>or</span>
        {!isAuth && (
          <button type="button" className="ms-onboard-skip" onClick={() => go(last)}>
            Atla
          </button>
        )}
      </div>

      <div className={`ms-onboard-body ${isAuth ? 'is-auth' : ''}`}>
        <div key={step} className={`ms-onboard-step ${dir > 0 ? 'from-right' : 'from-left'}`}>
          {!isAuth && (
            <div className="ms-onboard-art">
              <Scene step={step} />
            </div>
          )}
          <h1 className="ms-onboard-title">{s.title}</h1>
          <p className="ms-onboard-text">{s.text}</p>
          {isAuth && (
            <div className="ms-onboard-auth">
              <Suspense fallback={<div className="h-64 rounded-2xl bg-white border border-line animate-pulse" />}>
                <UserAuthModal isOpen embedded mandatory onClose={() => {}} onAuthSuccess={onAuthSuccess} initialMode="register" />
              </Suspense>
            </div>
          )}
        </div>
      </div>

      <div className="ms-onboard-nav">
        <button
          type="button"
          className="ms-onboard-round"
          onClick={() => go(step - 1)}
          disabled={step === 0}
          aria-label="Geri"
        >
          <ChevronLeft className="w-5 h-5" />
        </button>
        <div className="ms-onboard-dots" role="tablist">
          {STEPS.map((_, i) => (
            <button
              key={i}
              type="button"
              role="tab"
              aria-selected={i === step}
              aria-label={`${i + 1}. adım`}
              className={i === step ? 'is-on' : ''}
              onClick={() => go(i)}
            />
          ))}
        </div>
        {isAuth ? (
          <span className="w-11" />
        ) : (
          <button type="button" className="ms-onboard-round is-primary" onClick={() => go(step + 1)} aria-label="İleri">
            <ChevronRight className="w-5 h-5" />
          </button>
        )}
      </div>
    </div>
  );
};
