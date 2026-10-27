import React from 'react';
/**
 * Elle yazılmış Lottie animasyonları (tasarım sistemi: assets/Motion). Katman sınıfları
 * (lt-clinic, lt-accent, lt-ok, lt-faint) index.css'te tokenlara boyanır; koyu tema kendiliğinden uyar.
 * lottie-web ve animasyon verisi yalnız gerektiğinde yüklenir (veri açılış paketinde 350 KB tutuyordu);
 * "hareketi azalt" açıksa son karede durur.
 */
const SOURCES = {
  ecg: () => import('../../assets/lottie/ecg-pulse.json'),
  check: () => import('../../assets/lottie/check-success.json'),
  empty: () => import('../../assets/lottie/empty-search.json'),
  kutlama: () => import('../../assets/lottie/kutlama.json'),
  zirve: () => import('../../assets/lottie/zirve.json'),
  calisma: () => import('../../assets/lottie/calisma.json'),
  sevgi: () => import('../../assets/lottie/sevgi.json'),
  gunes: () => import('../../assets/lottie/gunes.json'),
} as const;
export type LottieName = keyof typeof SOURCES;

export const Lottie: React.FC<{ name: LottieName; loop?: boolean; className?: string; style?: React.CSSProperties }> = ({
  name,
  loop = true,
  className = '',
  style,
}) => {
  const ref = React.useRef<HTMLDivElement>(null);
  React.useEffect(() => {
    let anim: { destroy: () => void } | null = null;
    let cancelled = false;
    const reduce = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
    Promise.all([import('lottie-web/build/player/lottie_light'), SOURCES[name]()]).then(([{ default: lottie }, veri]) => {
      if (cancelled || !ref.current) return;
      const a = lottie.loadAnimation({
        container: ref.current,
        renderer: 'svg',
        loop: loop && !reduce,
        autoplay: !reduce,
        // her örnek kendi kopyasıyla çalışır (lottie veriyi yerinde değiştirir)
        animationData: JSON.parse(JSON.stringify(veri.default)),
      });
      if (reduce) a.goToAndStop(a.totalFrames - 1, true);
      anim = a;
    });
    return () => {
      cancelled = true;
      anim?.destroy();
    };
  }, [name, loop]);
  return <div ref={ref} className={`ms-lottie ${className}`} style={style} aria-hidden="true" />;
};
