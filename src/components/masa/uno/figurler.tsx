/**
 * Sevimli Dostlar figürleri: elle çizilmiş satır içi SVG (hazır görsel yok). Her figür merkez (0,0), yaklaşık ±32 birim.
 * Kart çizimi (Kart.tsx), kural sayfası ve lobi aynı bileşenleri kullanır.
 */
import React from 'react';

export type FigurAd = 'kitty' | 'batman' | 'kuromi' | 'pony';
export const FIGUR_ADLAR: readonly FigurAd[] = ['kitty', 'batman', 'pony', 'kuromi'];
export const FIGUR_AD: Record<FigurAd, string> = { kitty: 'Fiyonklu Kedicik', batman: 'Yarasa', kuromi: 'Yaramaz Tavşan', pony: 'Gökkuşağı Tayı' };

const CIZGI = '#2a2226';
const GOKKUSAGI = ['#f0483e', '#ff9a2e', '#ffd53d', '#3fc56b', '#3d9bf0', '#9a5fe0'];

/** Fiyonklu beyaz kedicik: oval baş, sivri kulak, kırmızı fiyonk, sarı burun, bıyıklar; ağız yok */
export function Kedicik() {
  return (
    <g strokeLinejoin="round" strokeLinecap="round">
      <path d="M-25 -7 L-23 -27 Q-22 -30 -19 -28 L-7 -20 Z" fill="#fff" stroke={CIZGI} strokeWidth="2.2" />
      <path d="M25 -7 L23 -27 Q22 -30 19 -28 L7 -20 Z" fill="#fff" stroke={CIZGI} strokeWidth="2.2" />
      <ellipse cx="0" cy="2" rx="28" ry="21.500" fill="#fff" stroke={CIZGI} strokeWidth="2.2" />
      <ellipse cx="-13" cy="4" rx="2.700" ry="3.700" fill={CIZGI} />
      <ellipse cx="13" cy="4" rx="2.700" ry="3.700" fill={CIZGI} />
      <ellipse cx="0" cy="9.500" rx="3.400" ry="2.400" fill="#f7c600" stroke={CIZGI} strokeWidth="1.2" />
      <g stroke={CIZGI} strokeWidth="1.700" fill="none">
        <path d="M-22 2 L-33 -1 M-23 7.500 L-34 8 M-22 13 L-32 17" />
        <path d="M22 2 L33 -1 M23 7.500 L34 8 M22 13 L32 17" />
      </g>
      {/* fiyonk (sağ kulağın önünde) */}
      <g transform="translate(15 -19) rotate(14)" stroke={CIZGI} strokeWidth="1.800">
        <path d="M0 0 C-5 -9 -14 -9 -13 0 C-14 8 -5 8 0 0 Z" fill="#e8243c" />
        <path d="M0 0 C5 -9 14 -9 13 0 C14 8 5 8 0 0 Z" fill="#e8243c" />
        <circle r="3.800" fill="#e8243c" />
      </g>
    </g>
  );
}

/** Yarasa amblemi: sarı oval içinde siyah yarasa (merkez 0,0; ±15 × ±9) */
export function YarasaAmblem() {
  return (
    <g strokeLinejoin="round">
      <ellipse rx="15" ry="9" fill="#ffd21f" stroke="#111" strokeWidth="1.800" />
      <path d="M-12 -1 Q-9 -6 -5.500 -3 Q-4.500 -6 -2.500 -4.500 L-2 -6.500 L0 -4.500 L2 -6.500 L2.500 -4.500 Q4.500 -6 5.500 -3 Q9 -6 12 -1 Q8 -1.500 6.500 3 Q3 1 0 6.500 Q-3 1 -6.500 3 Q-8 -1.500 -12 -1 Z" fill="#111" />
    </g>
  );
}

/** Yarasa: sivri kulaklı koyu maske, beyaz göz yarıkları, açık çene */
export function Yarasa() {
  return (
    <g strokeLinejoin="round" strokeLinecap="round">
      <path d="M-19 -32 L-11 -15 Q0 -19 11 -15 L19 -32 L23 -6 Q24 14 0 28 Q-24 14 -23 -6 Z" fill="#23232b" stroke="#0c0c10" strokeWidth="2.2" />
      <path d="M-19 -32 L-11 -15 Q-6 -16.500 -3 -17 L-15 -8 Z M19 -32 L11 -15 Q6 -16.500 3 -17 L15 -8 Z" fill="#3a3a46" />
      <path d="M-14 7 Q-7 4 0 9 Q7 4 14 7 Q13 19 0 25 Q-13 19 -14 7 Z" fill="#f2c9a5" stroke="#0c0c10" strokeWidth="1.600" />
      <path d="M-5.500 16.500 L5.500 16.500" stroke="#7a4a36" strokeWidth="1.800" fill="none" />
      <path d="M-17 -5 L-4 -1 L-5.500 3.500 Q-11 4 -16 0 Z" fill="#fff" />
      <path d="M17 -5 L4 -1 L5.500 3.500 Q11 4 16 0 Z" fill="#fff" />
      <path d="M-18 -8 L-3 -3 M18 -8 L3 -3" stroke="#0c0c10" strokeWidth="2.200" fill="none" />
    </g>
  );
}

/** Gökkuşağı yeleli tay: iri gözlü gök mavisi baş, altı renkli yele, yanakta yıldız */
export function Tay() {
  return (
    <g strokeLinejoin="round" strokeLinecap="round">
      {/* arka yele: sağ omuza dökülen gökkuşağı */}
      {GOKKUSAGI.map((c, i) => (
        <path key={c} d={`M${6 + i * 1.2} ${-22 + i * 1.5} Q${33 - i * 1.5} ${-18 + i * 3} ${29 - i * 3.6} ${24 - i * 1.2}`} fill="none" stroke={c} strokeWidth="5" />
      ))}
      <path d="M13 -15 L20 -30 Q10 -29 5 -20 Z" fill="#9edbf9" stroke="#2f6f9a" strokeWidth="2" />
      <ellipse cx="-1" cy="2" rx="21" ry="20" fill="#9edbf9" stroke="#2f6f9a" strokeWidth="2.200" />
      <ellipse cx="-3" cy="15" rx="12.500" ry="8.500" fill="#c4eaff" stroke="#2f6f9a" strokeWidth="1.600" />
      {/* perçem: tepeden sol şakağa */}
      {GOKKUSAGI.map((c, i) => (
        <path key={c} d={`M${9 - i * 2} ${-18.500 + (i > 3 ? (i - 3) * 0.8 : 0)} Q${-3 - i * 2.4} ${-24 + i * 1.3} ${-12 - i * 1.5} ${-14 + i * 2.7}`} fill="none" stroke={c} strokeWidth="4" />
      ))}
      <path d="M-17 -10 L-23 -29 Q-13 -28 -8 -18 Z" fill="#9edbf9" stroke="#2f6f9a" strokeWidth="2" />
      <path d="M-17 -15 L-20.500 -25 Q-14.500 -24 -11.500 -18.500 Z" fill="#f7a8d0" />
      <g>
        <ellipse cx="-9.500" cy="1" rx="5.800" ry="7.600" fill="#fff" stroke="#1e2a3a" strokeWidth="1.500" />
        <ellipse cx="9" cy="1" rx="5.800" ry="7.600" fill="#fff" stroke="#1e2a3a" strokeWidth="1.500" />
        <ellipse cx="-9" cy="2" rx="3.900" ry="5.600" fill="#c2389a" />
        <ellipse cx="9.500" cy="2" rx="3.900" ry="5.600" fill="#c2389a" />
        <ellipse cx="-9" cy="2.800" rx="2" ry="3.300" fill="#1e1420" />
        <ellipse cx="9.500" cy="2.800" rx="2" ry="3.300" fill="#1e1420" />
        <circle cx="-10.500" cy="-1" r="1.700" fill="#fff" />
        <circle cx="8" cy="-1" r="1.700" fill="#fff" />
        <path d="M-15.500 -3 L-18.500 -5.500 M-14 -5.500 L-16 -8.500 M15 -3 L18 -5.500 M13.500 -5.500 L15.500 -8.500" stroke="#1e2a3a" strokeWidth="1.400" fill="none" />
      </g>
      <path d="M-7.500 14 L-7.400 14 M1.500 14 L1.600 14" stroke="#2f6f9a" strokeWidth="2" />
      <path d="M-8 18.500 Q-3 22 2 18.500" fill="none" stroke="#2f6f9a" strokeWidth="1.600" />
      <path d="M0 -4.200 L1.200 -1.300 L4.300 -1.100 L1.900 0.900 L2.700 3.900 L0 2.200 L-2.700 3.900 L-1.900 0.900 L-4.300 -1.100 L-1.200 -1.300 Z" transform="translate(15 13) scale(.9)" fill="#ffd53d" stroke="#c98f00" strokeWidth=".8" />
    </g>
  );
}

/** Yaramaz tavşan: siyah soytarı başlığı, uzun kulaklar, beyaz yüz, alında pembe kurukafa, şeytan kuyruğu */
export function Tavsan() {
  return (
    <g strokeLinejoin="round" strokeLinecap="round">
      {/* şeytan kuyruğu */}
      <path d="M18 20 Q30 24 30 13 Q30 8 26 8" fill="none" stroke="#2b2233" strokeWidth="2.600" />
      <path d="M26 3 L31 9.500 L22.500 10 Z" fill="#2b2233" />
      {/* kulaklar */}
      <path d="M-20 -6 Q-30 -22 -21 -33 Q-17 -36 -15 -31 Q-11 -22 -6 -15 Z" fill="#2b2233" stroke="#120d18" strokeWidth="2" />
      <path d="M20 -6 Q31 -20 26 -32 Q23 -37 19 -32 Q12 -23 6 -15 Z" fill="#2b2233" stroke="#120d18" strokeWidth="2" />
      <path d="M26 -32 Q31 -30 32 -24" fill="none" stroke="#2b2233" strokeWidth="3" />
      <ellipse cx="0" cy="3" rx="27" ry="21" fill="#2b2233" stroke="#120d18" strokeWidth="2.200" />
      <path d="M-20 6 Q-20 -5 -10 -5 Q-4 -5 0 1 Q4 -5 10 -5 Q20 -5 20 6 Q19 19 0 20 Q-19 19 -20 6 Z" fill="#fff" stroke="#120d18" strokeWidth="1.500" />
      <ellipse cx="-9.500" cy="7" rx="2.700" ry="3.500" fill="#120d18" />
      <ellipse cx="9.500" cy="7" rx="2.700" ry="3.500" fill="#120d18" />
      <path d="M-14 1.500 L-6 4 M14 1.500 L6 4" stroke="#120d18" strokeWidth="1.700" fill="none" />
      <ellipse cx="0" cy="11" rx="2" ry="1.500" fill="#ff6fae" />
      <path d="M-4.500 14.500 Q-1 17 0 14 Q1 17 5.500 13.500" fill="none" stroke="#120d18" strokeWidth="1.400" />
      {/* alındaki pembe kurukafa */}
      <g transform="translate(0 -11)">
        <path d="M-5 -1 Q-5 -6 0 -6 Q5 -6 5 -1 Q5 2 2.800 2.600 L2.800 4.600 L-2.800 4.600 L-2.800 2.600 Q-5 2 -5 -1 Z" fill="#ff6fae" stroke="#120d18" strokeWidth="1" />
        <circle cx="-2" cy="-1.200" r="1.200" fill="#120d18" />
        <circle cx="2" cy="-1.200" r="1.200" fill="#120d18" />
      </g>
    </g>
  );
}

/** Ada göre figür <g>'si (merkez 0,0) */
export function FigurG({ ad }: { ad: FigurAd }) {
  if (ad === 'kitty') return <Kedicik />;
  if (ad === 'batman') return <Yarasa />;
  if (ad === 'pony') return <Tay />;
  return <Tavsan />;
}

/** Tek başına figür (kural sayfası, lobi): kare SVG */
export function Figur({ ad, boy = 56, className }: { ad: FigurAd; boy?: number; className?: string }) {
  return (
    <svg className={className} width={boy} height={boy} viewBox="-38 -40 76 76" role="img" aria-label={FIGUR_AD[ad]} focusable="false">
      <FigurG ad={ad} />
    </svg>
  );
}

/** Karakter kartının etki simgesi (merkez 0,0; ±9): hediye paketi, siper, şimşek, gökkuşağı */
export function EtkiSimge({ ad }: { ad: FigurAd }) {
  if (ad === 'kitty') {
    return (
      <g stroke="#7a1226" strokeWidth="1.200" strokeLinejoin="round">
        <rect x="-8" y="-3" width="16" height="11" rx="1.500" fill="#ff8fa3" />
        <rect x="-9.500" y="-6.500" width="19" height="5" rx="1.500" fill="#ef3b5d" />
        <rect x="-1.800" y="-6.500" width="3.600" height="14.500" fill="#fff" stroke="none" />
        <path d="M0 -6.500 C-3 -11 -8 -10 -6 -7 Z M0 -6.500 C3 -11 8 -10 6 -7 Z" fill="#fff" />
      </g>
    );
  }
  if (ad === 'batman') {
    return (
      <g strokeLinejoin="round">
        <path d="M-8 -8 Q0 -5 8 -8 V0 Q8 7 0 10 Q-8 7 -8 0 Z" fill="#ffd21f" stroke="#111" strokeWidth="1.600" />
        <path d="M-5.500 -1 Q-3.500 -3.500 -2 -1.500 L-1 -3.500 L0 -2 L1 -3.500 L2 -1.500 Q3.500 -3.500 5.500 -1 Q3 -1 2.500 2 Q1 1 0 4 Q-1 1 -2.500 2 Q-3 -1 -5.500 -1 Z" fill="#111" />
      </g>
    );
  }
  if (ad === 'kuromi') {
    return <path d="M2 -10 L-6 1.500 L-1 1.500 L-3 10 L6.500 -2.500 L1 -2.500 Z" fill="#ffd53d" stroke="#3a1d55" strokeWidth="1.400" strokeLinejoin="round" />;
  }
  return (
    <g fill="none" strokeLinecap="butt">
      {['#f0483e', '#ffd53d', '#3fc56b', '#3d9bf0'].map((c, i) => (
        <path key={c} d={`M${-10 + i * 2.3} 6 A${10 - i * 2.3} ${10 - i * 2.3} 0 0 1 ${10 - i * 2.3} 6`} stroke={c} strokeWidth="2.400" />
      ))}
    </g>
  );
}
