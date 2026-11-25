import React, { useSyncExternalStore } from 'react';
import { v16Acik, v16Dinle } from '../../utils/v16';

/**
 * v16 ikon seti (tuval "MeDSor v16" › v16.css): 24'lük ızgara, 1.8 çizgi, yuvarlak uç, currentColor.
 * Boyutu üst öğenin `svg { width/height }` kuralı belirler (lucide ile aynı API: className, strokeWidth, aria-*).
 * `v16Ikonlu(lucide, ad)`: v16 açıkken bu ikonu, kapalıyken eskisini çizer — öğrenci v15'i aynen görür.
 */
const YOL = {
  ev: <path d="M4 11l8-6.5 8 6.5V20h-5v-5h-6v5H4z" />,
  kitap: <path d="M12 6.8C10.4 5.3 7.9 4.6 4 4.6v13.2c3.9 0 6.4.7 8 2.2 1.6-1.5 4.1-2.2 8-2.2V4.6c-3.9 0-6.4.7-8 2.2zM12 6.8V20" />,
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
  kapat: <path d="M6 6l12 12M18 6L6 18" />,
  tik: <path d="M5 12.5l4.5 4.5L19 7.5" strokeWidth={2} />,
  ara: <><circle cx="11" cy="11" r="6.5" /><path d="M20 20l-4.2-4.2" /></>,
  zil: <path d="M6 10a6 6 0 0112 0v4l1.5 3h-15L6 14zM10 20a2 2 0 004 0" />,
  ayar: <><path d="M4 7h10M18 7h2M4 17h4M12 17h8" /><circle cx="16" cy="7" r="2" /><circle cx="10" cy="17" r="2" /></>,
  bilgi: <><circle cx="12" cy="12" r="8.5" /><path d="M12 11v5M12 8h.01" /></>,
  yildiz: <path d="M12 4l2.4 5 5.4.6-4 3.7 1.1 5.3L12 16l-4.9 2.6 1.1-5.3-4-3.7 5.4-.6z" />,
  kalem: <path d="M4 20l4-1 11-11-3-3L5 16zM14 7l3 3" />,
  arti: <path d="M12 5v14M5 12h14" />,
  eksi: <path d="M5 12h14" />,
  geri: <path d="M15 5l-7 7 7 7" />,
  sag: <path d="M9 5l7 7-7 7" />,
  asagi: <path d="M6 9l6 6 6-6" />,
  yukari: <path d="M6 15l6-6 6 6" />,
  saat: <><circle cx="12" cy="13" r="7.5" /><path d="M12 9.5V13l2.5 1.5M10 3h4" /></>,
  not: <path d="M6 4h9l3 3v13H6zM9 11h6M9 15h4" />,
  kart: <><rect x="3.5" y="7" width="12.5" height="13" rx="2.5" /><path d="M8 7V6a2 2 0 012-2h8.5a2 2 0 012 2v9a2 2 0 01-2 2H16" /></>,
  isik: <path d="M9 18h6M10 21h4M12 3a6 6 0 00-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0012 3z" />,
  kalp: <path d="M12 20s-7-4.4-7-10a4 4 0 017-2.6A4 4 0 0119 10c0 5.6-7 10-7 10z" />,
  dna: <path d="M8 3c0 4.5 8 5.5 8 9s-8 4.5-8 9M16 3c0 4.5-8 5.5-8 9s8 4.5 8 9M9.5 6.5h5M9.5 17.5h5" />,
  kilit: <><rect x="5" y="10.5" width="14" height="9.5" rx="2" /><path d="M8 10.5V8a4 4 0 018 0v2.5" /></>,
  indir: <path d="M12 4v11M7 10.5l5 5 5-5M5 20h14" />,
  gonder: <path d="M4 12l16-7-6 16-3-6.5z" />,
  kupa: <path d="M8 4h8v5a4 4 0 01-8 0zM8 6H5a3 3 0 003 4M16 6h3a3 3 0 01-3 4M12 13v4M8.5 20h7" />,
  simsek: <path d="M13 3L5 14h6l-1 7 8-11h-6z" />,
  uyari: <path d="M12 4l9 16H3zM12 10v4M12 17h.01" />,
  cop: <path d="M5 7h14M10 7V5h4v2M7 7l1 13h8l1-13" />,
  kulak: <><path d="M4 14v-2a8 8 0 0116 0v2" /><path d="M4 14h2.5A1.5 1.5 0 018 15.5v3A1.5 1.5 0 016.5 20h-1A1.5 1.5 0 014 18.5zM20 14h-2.5a1.5 1.5 0 00-1.5 1.5v3a1.5 1.5 0 001.5 1.5h1a1.5 1.5 0 001.5-1.5z" /></>,
  grafik: <path d="M4 4v16h16M8 15l3.5-4 3 2.5L20 7" />,
  daha: <><circle cx="5" cy="12" r="1.7" fill="currentColor" stroke="none" /><circle cx="12" cy="12" r="1.7" fill="currentColor" stroke="none" /><circle cx="19" cy="12" r="1.7" fill="currentColor" stroke="none" /></>,
} as const;

export type IkonAd = keyof typeof YOL;

type SvgP = React.SVGProps<SVGSVGElement> & { strokeWidth?: number | string; size?: number | string };

export function Ikon({ ad, strokeWidth = 1.8, size, color, absoluteStrokeWidth: _a, ...p }: SvgP & { ad: IkonAd; absoluteStrokeWidth?: boolean }) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width={size ?? 24} height={size ?? 24} fill="none" stroke={color || 'currentColor'}
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
    if (!v16) return <Eski {...p} />;
    // lucide'in sınıf adları korunur (ör. .lucide-copy kuralları v16'da da tutsun)
    const ad0 = String((Eski as { displayName?: string }).displayName || '').replace(/([a-z0-9])([A-Z])/g, '$1-$2').toLowerCase();
    return <Ikon ad={ad} {...p} className={`lucide${ad0 ? ` lucide-${ad0}` : ''}${p.className ? ` ${p.className}` : ''}`} />;
  };
  C.displayName = `v16Ikon(${ad})`;
  m.set(ad, C);
  return C;
}
