import React from 'react';

/**
 * Small hand-drawn SVG animations (no external assets). Keyframes live in index.css
 * under "MeDSor animations" and are disabled for prefers-reduced-motion.
 */

/** Two-tone capsule mascot that bounces and blinks. The default "please wait". */
export const CapsuleLoader: React.FC<{ size?: number; className?: string }> = ({ size = 72, className = '' }) => (
  <svg width={size} height={size} viewBox="0 0 80 80" className={className} aria-hidden="true">
    <ellipse className="ms-shadow" cx="40" cy="72" rx="16" ry="3.2" fill="#0E1A26" opacity="0.12" />
    <g className="ms-bounce">
      <g transform="rotate(-18 40 38)">
        <rect x="22" y="14" width="36" height="52" rx="18" fill="#FFFFFF" stroke="#0E1A26" strokeWidth="2.4" />
        <path d="M22 40V32a18 18 0 0 1 36 0v8z" fill="#1E4FD8" stroke="#0E1A26" strokeWidth="2.4" strokeLinejoin="round" />
        <path d="M29 24a10 10 0 0 1 8-5" stroke="#FFFFFF" strokeWidth="2.6" strokeLinecap="round" fill="none" opacity="0.7" />
        <g className="ms-blink">
          <circle cx="34" cy="48" r="2.4" fill="#0E1A26" />
          <circle cx="46" cy="48" r="2.4" fill="#0E1A26" />
        </g>
        <path d="M36 54.5q4 3 8 0" stroke="#0E1A26" strokeWidth="2.2" strokeLinecap="round" fill="none" />
        <circle cx="30.5" cy="53" r="2.2" fill="#F59EB2" opacity="0.8" />
        <circle cx="49.5" cy="53" r="2.2" fill="#F59EB2" opacity="0.8" />
      </g>
    </g>
  </svg>
);

/** An open book whose page keeps turning — for lessons and long lists. */
export const BookLoader: React.FC<{ size?: number; className?: string }> = ({ size = 80, className = '' }) => (
  <svg width={size} height={size * 0.75} viewBox="0 0 96 72" className={className} aria-hidden="true">
    <ellipse cx="48" cy="66" rx="30" ry="3" fill="#0E1A26" opacity="0.1" />
    <path d="M48 16C40 10 26 9 12 12v44c14-3 28-2 36 4z" fill="#EEF3FE" stroke="#0E1A26" strokeWidth="2.2" strokeLinejoin="round" />
    <path d="M48 16c8-6 22-7 36-4v44c-14-3-28-2-36 4z" fill="#FFFFFF" stroke="#0E1A26" strokeWidth="2.2" strokeLinejoin="round" />
    <g stroke="#9DB6F6" strokeWidth="2" strokeLinecap="round">
      <path d="M20 24h20M20 31h20M20 38h14" />
      <path d="M56 24h20M56 31h20M56 38h16" />
    </g>
    <path className="ms-page" d="M48 16c8-6 22-7 36-4v44c-14-3-28-2-36 4z" fill="#FFF9EF" stroke="#0E1A26" strokeWidth="2.2" strokeLinejoin="round" />
    <line x1="48" y1="16" x2="48" y2="60" stroke="#0E1A26" strokeWidth="2.2" />
  </svg>
);

/** Sheets flying into a tray — for building a PDF. */
export const PaperLoader: React.FC<{ size?: number; className?: string }> = ({ size = 84, className = '' }) => (
  <svg width={size} height={size} viewBox="0 0 84 84" className={className} aria-hidden="true">
    <g className="ms-sheet ms-sheet-1">
      <rect x="27" y="10" width="30" height="38" rx="4" fill="#FFFFFF" stroke="#0E1A26" strokeWidth="2.2" />
      <path d="M33 20h18M33 26h18M33 32h12" stroke="#9DB6F6" strokeWidth="2" strokeLinecap="round" />
    </g>
    <g className="ms-sheet ms-sheet-2">
      <rect x="27" y="10" width="30" height="38" rx="4" fill="#FFFFFF" stroke="#0E1A26" strokeWidth="2.2" />
      <path d="M33 20h18M33 26h10" stroke="#F5C27A" strokeWidth="2" strokeLinecap="round" />
    </g>
    <path d="M14 52h56l-6 20H20z" fill="#1E4FD8" stroke="#0E1A26" strokeWidth="2.2" strokeLinejoin="round" />
    <path d="M30 60h24" stroke="#FFFFFF" strokeWidth="2.4" strokeLinecap="round" opacity="0.85" />
  </svg>
);

/** Check that draws itself inside a ring, with a little confetti pop. */
export const SuccessCheck: React.FC<{ size?: number; className?: string }> = ({ size = 72, className = '' }) => (
  <svg width={size} height={size} viewBox="0 0 80 80" className={className} aria-hidden="true">
    <g className="ms-confetti">
      <circle cx="12" cy="20" r="3" fill="#F59E0B" />
      <rect x="64" y="12" width="6" height="6" rx="1.5" fill="#1E4FD8" transform="rotate(20 67 15)" />
      <circle cx="70" cy="56" r="2.6" fill="#E0566E" />
      <rect x="8" y="58" width="6" height="6" rx="1.5" fill="#7C3AED" transform="rotate(-15 11 61)" />
      <circle cx="40" cy="5" r="2.4" fill="#1F9D55" />
    </g>
    <circle className="ms-ring" cx="40" cy="40" r="26" fill="#E4F3E9" stroke="#1F9D55" strokeWidth="3" />
    <path className="ms-check" d="M28 41l8 8 16-17" fill="none" stroke="#157A3E" strokeWidth="4.5" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

/**
 * Covers its (relative) parent with a soft blur and a centered animation.
 * Use inside a `relative` container; set `fixed` to cover the whole screen.
 */
export const BlurOverlay: React.FC<{
  show: boolean;
  label?: string;
  hint?: string;
  icon?: React.ReactNode;
  fixed?: boolean;
  rounded?: string;
}> = ({ show, label, hint, icon, fixed = false, rounded = 'rounded-[inherit]' }) =>
  show ? (
    <div
      role="status"
      aria-live="polite"
      className={`${fixed ? 'fixed' : 'absolute'} inset-0 z-30 ${rounded} bg-white/60 backdrop-blur-[6px] flex flex-col items-center justify-center gap-2 text-center px-6 ms-fade-in`}
    >
      {icon || <CapsuleLoader />}
      {label && <span className="text-[15px] font-semibold text-ink">{label}</span>}
      {hint && <span className="text-[13px] text-ink-3 max-w-[280px]">{hint}</span>}
    </div>
  ) : null;

/** Full-width "loading this section" placeholder. */
export const SectionLoader: React.FC<{ label?: string; variant?: 'capsule' | 'book' }> = ({ label = 'Bölüm yükleniyor…', variant = 'capsule' }) => (
  <div role="status" className="py-16 sm:py-20 flex flex-col items-center justify-center gap-2 text-ink-2 ms-fade-in">
    {variant === 'book' ? <BookLoader /> : <CapsuleLoader />}
    <span className="text-[14px] font-medium">{label}</span>
  </div>
);

const THINKING_STEPS = ['Ders notunu okuyor…', 'Slayttaki vurguları tarıyor…', 'Çıkmış sorulara bakıyor…', 'Yanıtı yazıyor…'];

/**
 * "AI is thinking" card: a chat-bubble mascot whose eyes look around while it types,
 * twinkling sparkles, rotating status lines and shimmering placeholder text.
 */
export const AiThinking: React.FC<{ steps?: string[]; className?: string }> = ({ steps = THINKING_STEPS, className = '' }) => {
  const [step, setStep] = React.useState(0);
  React.useEffect(() => {
    const t = window.setInterval(() => setStep((s) => (s + 1) % steps.length), 1900);
    return () => window.clearInterval(t);
  }, [steps.length]);

  return (
    <div role="status" aria-live="polite" className={`ms-pop-in rounded-2xl bg-accent-soft/70 border border-accent/10 p-3.5 flex flex-col gap-3 ${className}`}>
      <div className="flex items-center gap-3">
        <svg width="58" height="58" viewBox="0 0 64 64" className="shrink-0" aria-hidden="true">
          <g className="ms-twinkle">
            <path d="M8 12l1.6 3.4L13 17l-3.4 1.6L8 22l-1.6-3.4L3 17l3.4-1.6z" fill="#F59E0B" />
          </g>
          <g className="ms-twinkle ms-twinkle-2">
            <path d="M55 6l1.2 2.6L59 10l-2.8 1.2L55 14l-1.2-2.8L51 10l2.8-1.4z" fill="#7C3AED" />
          </g>
          <g className="ms-float">
            <path d="M14 16h36a8 8 0 0 1 8 8v16a8 8 0 0 1-8 8H30l-9 7v-7h-7a8 8 0 0 1-8-8V24a8 8 0 0 1 8-8z" fill="#FFFFFF" stroke="#0E1A26" strokeWidth="2.2" strokeLinejoin="round" />
            <g className="ms-look">
              <circle cx="25" cy="29" r="2.6" fill="#0E1A26" />
              <circle cx="39" cy="29" r="2.6" fill="#0E1A26" />
            </g>
            <circle cx="21" cy="34" r="2" fill="#F59EB2" opacity="0.8" />
            <circle cx="43" cy="34" r="2" fill="#F59EB2" opacity="0.8" />
            <circle className="ms-dot" cx="25" cy="40" r="2.2" fill="#1E4FD8" />
            <circle className="ms-dot ms-dot-2" cx="32" cy="40" r="2.2" fill="#1E4FD8" />
            <circle className="ms-dot ms-dot-3" cx="39" cy="40" r="2.2" fill="#1E4FD8" />
          </g>
        </svg>
        <div className="min-w-0 flex flex-col">
          <span className="text-[14px] font-semibold text-accent">AI düşünüyor</span>
          <span key={step} className="ms-fade-in text-[13px] text-ink-2 truncate">
            {steps[step]}
          </span>
        </div>
      </div>
      <div className="flex flex-col gap-2" aria-hidden="true">
        <span className="ms-shimmer h-2.5 rounded-full w-[92%]" />
        <span className="ms-shimmer h-2.5 rounded-full w-[78%]" />
        <span className="ms-shimmer h-2.5 rounded-full w-[60%]" />
      </div>
    </div>
  );
};
