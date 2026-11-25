import React, { useSyncExternalStore } from 'react';
import { v16Acik, v16Dinle } from '../../utils/v16';

/**
 * v16 ikon seti (tuval "MeDSor v16" › v16.css): 24'lük ızgara, 1.8 çizgi, yuvarlak uç, currentColor.
 * Boyutu üst öğenin `svg { width/height }` kuralı belirler (lucide ile aynı API: className, strokeWidth, aria-*).
 * `v16Ikonlu(lucide, ad)`: v16 açıkken bu ikonu, kapalıyken eskisini çizer — öğrenci v15'i aynen görür.
 */
const YOL = {
  ev: <path d="M4 11l8-6.5 8 6.5V20h-5v-5h-6v5H4z" />,
  kitap: <path d="M4 5.5A1.5 1.5 0 015.5 4H11v16H5.5A1.5 1.5 0 014 18.5zM20 5.5A1.5 1.5 0 0018.5 4H13v16h5.5a1.5 1.5 0 001.5-1.5z" />,
  soru: <><rect x="4" y="4" width="16" height="16" rx="4" /><path d="M9.8 9.5a2.3 2.3 0 114 1.6c-.9.6-1.8 1.1-1.8 2.4M12 16.5h.01" /></>,
  hedef: <><circle cx="12" cy="12" r="8.5" /><circle cx="12" cy="12" r="4.5" /><circle cx="12" cy="12" r=".8" fill="currentColor" /></>,
  klasor: <path d="M4 7a2 2 0 012-2h4l2 2h6a2 2 0 012 2v8a2 2 0 01-2 2H6a2 2 0 01-2-2z" />,
  oyun: <><rect x="2.5" y="7" width="19" height="11" rx="5.5" /><path d="M7.5 10.5v4M5.5 12.5h4M15.5 11.5h.01M18 13.5h.01" /></>,
  izgara: <><rect x="4" y="4" width="6.5" height="6.5" rx="1.8" /><rect x="13.5" y="4" width="6.5" height="6.5" rx="1.8" /><rect x="4" y="13.5" width="6.5" height="6.5" rx="1.8" /><rect x="13.5" y="13.5" width="6.5" height="6.5" rx="1.8" /></>,
  steto: <><path d="M5 3v5a4.5 4.5 0 009 0V3M9.5 12.5V15a5 5 0 0010 0v-2" /><circle cx="19.5" cy="11" r="2" /></>,
  sohbet: <path d="M4 6a2 2 0 012-2h12a2 2 0 012 2v9a2 2 0 01-2 2H10l-5 4v-4H6a2 2 0 01-2-2z" />,
  kisi: <><circle cx="12" cy="8.5" r="3.8" /><path d="M5 20a7 7 0 0114 0" /></>,
  kalkan: <path d="M12 3.5l7 3v5c0 4.5-3 7.8-7 9-4-1.2-7-4.5-7-9v-5z" />,
  oynat: <path d="M8 5.5v13a1 1 0 001.5.86l10.4-6.5a1 1 0 000-1.72L9.5 4.64A1 1 0 008 5.5z" fill="currentColor" stroke="none" />,
  duraklat: <><rect x="6" y="5" width="4" height="14" rx="1.2" fill="currentColor" stroke="none" /><rect x="14" y="5" width="4" height="14" rx="1.2" fill="currentColor" stroke="none" /></>,
  onceki: <path d="M18 6l-8 6 8 6zM6 6v12" />,
  sonraki: <path d="M6 6l8 6-8 6zM18 6v12" />,
  geri10: <path d="M4 12a8 8 0 108-8H8M8 1L5 4l3 3" />,
  ileri10: <path d="M20 12a8 8 0 11-8-8h4M16 1l3 3-3 3" />,
  liste: <path d="M9 6h11M9 12h11M9 18h11M4 6h.01M4 12h.01M4 18h.01" />,
  daha: <><circle cx="5" cy="12" r="1.7" fill="currentColor" stroke="none" /><circle cx="12" cy="12" r="1.7" fill="currentColor" stroke="none" /><circle cx="19" cy="12" r="1.7" fill="currentColor" stroke="none" /></>,
} as const;

export type IkonAd = keyof typeof YOL;

type SvgP = React.SVGProps<SVGSVGElement> & { strokeWidth?: number | string; size?: number | string };

export function Ikon({ ad, strokeWidth = 1.8, size, ...p }: SvgP & { ad: IkonAd }) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width={size ?? 24} height={size ?? 24} fill="none" stroke="currentColor"
      strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" aria-hidden={p['aria-label'] ? undefined : true} {...p}>
      {YOL[ad]}
    </svg>
  );
}

const onbellek = new Map<React.ElementType, Map<IkonAd, React.FC<SvgP>>>();

/** Aynı (eski, ad) çifti için hep aynı bileşen döner (React her çizimde yeni tür görüp yeniden kurmasın). */
export function v16Ikonlu(Eski: React.ElementType, ad: IkonAd): React.FC<SvgP> {
  let m = onbellek.get(Eski);
  if (!m) { m = new Map(); onbellek.set(Eski, m); }
  const var_ = m.get(ad);
  if (var_) return var_;
  const C: React.FC<SvgP> = (p) => {
    const v16 = useSyncExternalStore(v16Dinle, v16Acik, () => false);
    return v16 ? <Ikon ad={ad} {...p} /> : <Eski {...p} />;
  };
  C.displayName = `v16Ikon(${ad})`;
  m.set(ad, C);
  return C;
}
