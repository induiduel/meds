import React from 'react';
import ecgPulse from '../../assets/lottie/ecg-pulse.json';
import checkSuccess from '../../assets/lottie/check-success.json';
import emptySearch from '../../assets/lottie/empty-search.json';
import kutlama from '../../assets/lottie/kutlama.json';
import zirve from '../../assets/lottie/zirve.json';
import calisma from '../../assets/lottie/calisma.json';
import sevgi from '../../assets/lottie/sevgi.json';
import gunes from '../../assets/lottie/gunes.json';

/**
 * Elle yazılmış Lottie animasyonları (tasarım sistemi: assets/Motion). Katman sınıfları
 * (lt-clinic, lt-accent, lt-ok, lt-faint) index.css'te tokenlara boyanır; koyu tema kendiliğinden uyar.
 * lottie-web yalnız gerektiğinde yüklenir; "hareketi azalt" açıksa son karede durur.
 */
const SOURCES = { ecg: ecgPulse, check: checkSuccess, empty: emptySearch, kutlama, zirve, calisma, sevgi, gunes } as const;
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
    import('lottie-web/build/player/lottie_light').then(({ default: lottie }) => {
      if (cancelled || !ref.current) return;
      const a = lottie.loadAnimation({
        container: ref.current,
        renderer: 'svg',
        loop: loop && !reduce,
        autoplay: !reduce,
        // her örnek kendi kopyasıyla çalışır (lottie veriyi yerinde değiştirir)
        animationData: JSON.parse(JSON.stringify(SOURCES[name])),
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
