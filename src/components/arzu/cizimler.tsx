/**
 * Arzu katmanının vektörel çizimleri. Hepsi elle kurulmuş SVG; animasyonlar CSS'tedir (arzu.css) ve sınıf
 * adlarıyla bağlanır: tilkinin dört bacağı ayrı eklemlidir (`ar-bacak-*`), kuyruk ve baş ayrı gruptur.
 */
import React from 'react';

/* ───────────────────────────── Renkler ───────────────────────────── */
const T = {
  turuncu: '#EF7F2F',
  turuncuKoyu: '#D4641C',
  turuncuGolge: '#B9531A',
  krem: '#FFF6EC',
  koyu: '#2B1A12',
  burun: '#1E130E',
  yanak: '#FF9DB4',
  kalp: '#FF5C86',
  kalpKoyu: '#E8306A',
};

/* ───────────────────────────── Kalp ───────────────────────────── */
export const KALP_YOLU =
  'M12 21.3s-7.4-4.7-9.8-9.3C.4 8.6 2.5 4 6.6 4c2 0 3.6 1 4.4 2.5C11.8 5 13.4 4 15.4 4c4.1 0 6.2 4.6 4.4 8-2.4 4.6-7.8 9.3-7.8 9.3z';

export const Kalp: React.FC<{ size?: number; color?: string; className?: string; parlak?: boolean }> = ({
  size = 20, color = T.kalp, className, parlak = true,
}) => (
  <svg viewBox="0 0 24 24" width={size} height={size} className={className} aria-hidden="true">
    <path d={KALP_YOLU} fill={color} />
    {parlak && <ellipse cx="8" cy="8.6" rx="1.7" ry="2.3" fill="#fff" opacity=".55" transform="rotate(-28 8 8.6)" />}
  </svg>
);

/* ───────────────────────────── Yürüyen tilki (yan görünüm, sağa bakar) ───────────────────────────── */
function Bacak({ sinif, arka = false, uzak = false }: { sinif: string; arka?: boolean; uzak?: boolean }) {
  const govde = uzak ? T.turuncuGolge : T.turuncu;
  const corap = uzak ? '#1C120C' : T.koyu;
  return (
    <g className={`ar-bacak ${sinif}`}>
      {arka && <ellipse cx="2" cy="4" rx="11" ry="9" fill={govde} />}
      <path d="M-5 0 L5.5 0 L4.5 19 L6.5 33 L-2.5 33 L-3.5 19 Z" fill={govde} />
      <path d="M-3.4 21 L4.8 21 L6.5 33 L-2.5 33 Z" fill={corap} />
      <path d="M-3.5 31 h11 a3 3 0 0 1 0 6 h-11 a3 3 0 0 1 0-6z" fill={corap} />
    </g>
  );
}

export const TilkiYuruyen: React.FC<{ className?: string; width?: number }> = ({ className = '', width = 150 }) => (
  <svg viewBox="0 0 160 100" width={width} height={width * 100 / 160} className={`ar-tilki ${className}`} aria-hidden="true">
    {/* uzak bacaklar */}
    <g transform="translate(52 60)"><Bacak sinif="ar-bacak-ua" arka uzak /></g>
    <g transform="translate(103 60)"><Bacak sinif="ar-bacak-uo" uzak /></g>
    {/* kuyruk */}
    <g transform="translate(40 56)"><g className="ar-kuyruk">
      <path d="M0 0 C-14 -4 -34 -2 -40 -22 C-44 -36 -30 -46 -16 -40 C-6 -36 -4 -22 2 -8 Z" fill={T.turuncu} />
      <path d="M-22 -37 C-30 -41 -41 -36 -39 -26 C-38 -20 -33 -16 -28 -17 C-31 -24 -28 -32 -22 -37 Z" fill={T.krem} />
      <path d="M0 0 C-8 -3 -18 -2 -24 -8 C-16 -6 -8 -4 2 -6 Z" fill={T.turuncuGolge} opacity=".6" />
    </g></g>
    {/* gövde */}
    <g className="ar-govde">
      <path d="M40 50 C42 36 66 28 94 32 C112 34 124 40 126 50 C128 64 112 77 86 77 L54 77 C42 77 34 68 36 58 Z" fill={T.turuncu} />
      <path d="M58 77 C62 68 90 64 118 60 C119 69 108 77 92 77 Z" fill={T.krem} />
      <path d="M44 72 C50 76 60 77 70 77 L54 77 C50 77 46 75 44 72 Z" fill={T.turuncuGolge} opacity=".5" />
    </g>
    {/* yakın bacaklar */}
    <g transform="translate(50 60)"><Bacak sinif="ar-bacak-ya" arka /></g>
    <g transform="translate(101 60)"><Bacak sinif="ar-bacak-yo" /></g>
    {/* baş */}
    <g transform="translate(106 20)"><g className="ar-bas">
      <g className="ar-kulak ar-kulak-a"><path d="M9 7 L3 -14 L24 1 Z" fill={T.turuncu} /><path d="M10 4 L6 -9 L20 1 Z" fill={T.koyu} opacity=".75" /></g>
      <g className="ar-kulak ar-kulak-o"><path d="M24 3 L30 -12 L38 6 Z" fill={T.turuncu} /><path d="M25 3 L30 -7 L35 5 Z" fill={T.koyu} opacity=".75" /></g>
      <path d="M0 21 C0 7 12 0 24 2 L47 21 C41 29 31 35 19 35 C7 35 0 31 0 21 Z" fill={T.turuncu} />
      <path d="M22 19 C30 16 40 18 47 21 C41 27 32 31 24 29 C21 26 20 22 22 19 Z" fill={T.krem} />
      <g className="ar-tilki-goz"><ellipse cx="19" cy="15" rx="2.7" ry="3.4" fill={T.koyu} /><circle cx="18.2" cy="13.8" r="1" fill="#fff" /></g>
      <circle cx="46" cy="21" r="2.8" fill={T.burun} />
      <circle cx="45.2" cy="20.2" r=".8" fill="#fff" opacity=".7" />
      <circle cx="29" cy="24" r="3.2" fill={T.yanak} opacity=".45" />
    </g></g>
  </svg>
);

/* ───────────────────────────── Oturan tilki, kalp tutar (karşılama) ───────────────────────────── */
export const TilkiOturan: React.FC<{ className?: string; width?: number }> = ({ className = '', width = 220 }) => (
  <svg viewBox="0 0 200 220" width={width} height={width * 220 / 200} className={`ar-oturan ${className}`} aria-hidden="true">
    <defs>
      <linearGradient id="ar-kalp-g" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stopColor="#FF7FA3" /><stop offset=".6" stopColor={T.kalp} /><stop offset="1" stopColor={T.kalpKoyu} />
      </linearGradient>
    </defs>
    {/* kuyruk: arkadan çıkar, sağa sarılır */}
    <g className="ar-oturan-kuyruk">
      <path d="M136 172 C164 184 196 172 194 142 C192 122 172 112 158 124 C146 134 150 152 132 160 Z" fill={T.turuncu} />
      <path d="M170 120 C184 118 195 130 193 146 C192 157 184 164 176 166 C185 154 183 136 170 120 Z" fill={T.krem} />
      <path d="M136 172 C150 178 164 180 176 176 C160 176 146 172 134 164 Z" fill={T.turuncuGolge} opacity=".5" />
    </g>
    {/* arka kalçalar */}
    <ellipse cx="60" cy="178" rx="25" ry="21" fill={T.turuncu} />
    <ellipse cx="140" cy="178" rx="25" ry="21" fill={T.turuncu} />
    <ellipse cx="60" cy="184" rx="18" ry="13" fill={T.turuncuGolge} opacity=".35" />
    <ellipse cx="140" cy="184" rx="18" ry="13" fill={T.turuncuGolge} opacity=".35" />
    {/* gövde */}
    <path d="M100 96 C70 96 56 136 56 180 C56 196 76 206 100 206 C124 206 144 196 144 180 C144 136 130 96 100 96 Z" fill={T.turuncu} />
    <path d="M100 116 C82 116 74 152 74 190 C74 199 86 204 100 204 C114 204 126 199 126 190 C126 152 118 116 100 116 Z" fill={T.krem} />
    {/* arka pençeler (koyu çorap) */}
    <ellipse cx="62" cy="199" rx="17" ry="7.5" fill={T.koyu} />
    <ellipse cx="138" cy="199" rx="17" ry="7.5" fill={T.koyu} />
    <path d="M52 198 a3.5 3.5 0 0 1 7 0 M60 197 a3.5 3.5 0 0 1 7 0 M68 198 a3.5 3.5 0 0 1 7 0" stroke="#5A4034" strokeWidth="1.4" fill="none" strokeLinecap="round" />
    <path d="M128 198 a3.5 3.5 0 0 1 7 0 M136 197 a3.5 3.5 0 0 1 7 0 M144 198 a3.5 3.5 0 0 1 7 0" stroke="#5A4034" strokeWidth="1.4" fill="none" strokeLinecap="round" />
    {/* ön kollar */}
    <path d="M68 128 C60 148 64 164 82 166" stroke={T.turuncu} strokeWidth="13" strokeLinecap="round" fill="none" />
    <path d="M132 128 C140 148 136 164 118 166" stroke={T.turuncu} strokeWidth="13" strokeLinecap="round" fill="none" />
    {/* kalp (kucakta) */}
    <g transform="translate(100 150)">
      <g className="ar-oturan-kalp">
        <path transform="translate(-24 -22) scale(2)" d={KALP_YOLU} fill="url(#ar-kalp-g)" />
        <ellipse cx="-8" cy="-9" rx="3.6" ry="5" fill="#fff" opacity=".5" transform="rotate(-28 -8 -9)" />
      </g>
    </g>
    {/* pençeler kalbi tutar */}
    <ellipse cx="84" cy="165" rx="7.5" ry="5.5" fill={T.koyu} transform="rotate(-12 84 165)" />
    <ellipse cx="116" cy="165" rx="7.5" ry="5.5" fill={T.koyu} transform="rotate(12 116 165)" />
    {/* baş */}
    <g className="ar-oturan-bas">
      <path d="M64 54 L52 6 L92 36 Z" fill={T.turuncu} />
      <path d="M67 49 L59 16 L85 37 Z" fill={T.koyu} opacity=".72" />
      <path d="M136 54 L148 6 L108 36 Z" fill={T.turuncu} />
      <path d="M133 49 L141 16 L115 37 Z" fill={T.koyu} opacity=".72" />
      <path d="M100 26 C70 26 50 48 50 76 C50 102 76 116 100 116 C124 116 150 102 150 76 C150 48 130 26 100 26 Z" fill={T.turuncu} />
      <path d="M60 86 C60 72 80 70 100 80 C120 70 140 72 140 86 C140 102 122 112 100 112 C78 112 60 102 60 86 Z" fill={T.krem} />
      <g className="ar-goz">
        <ellipse cx="80" cy="73" rx="4.6" ry="6" fill={T.koyu} />
        <circle cx="78.4" cy="70.6" r="1.7" fill="#fff" />
        <ellipse cx="120" cy="73" rx="4.6" ry="6" fill={T.koyu} />
        <circle cx="118.4" cy="70.6" r="1.7" fill="#fff" />
      </g>
      <path d="M93 88 C93 84 107 84 107 88 C107 93 100 97 100 97 C100 97 93 93 93 88 Z" fill={T.burun} />
      <path d="M92 100 Q100 106 108 100" stroke={T.koyu} strokeWidth="1.8" strokeLinecap="round" fill="none" />
      <circle cx="67" cy="91" r="6" fill={T.yanak} opacity=".5" />
      <circle cx="133" cy="91" r="6" fill={T.yanak} opacity=".5" />
    </g>
  </svg>
);

/* ───────────────────────────── Kitty & Batman: bir çift ───────────────────────────── */
export const KittyVeBatman: React.FC<{ className?: string; width?: number }> = ({ className = '', width = 180 }) => (
  <svg viewBox="0 0 220 140" width={width} height={width * 140 / 220} className={`ar-cift ${className}`} aria-hidden="true">
    {/* ortak kalp */}
    <g transform="translate(110 34)">
      <g className="ar-cift-kalp">
        <path transform="translate(-9 -9) scale(.75)" d={KALP_YOLU} fill={T.kalp} />
      </g>
    </g>

    {/* ── Batman (sağ) ── */}
    <g className="ar-batman">
      {/* pelerin */}
      <path d="M131 90 L122 136 L139 127 L155 137 L171 127 L188 136 L179 90 Z" fill="#141826" />
      {/* gövde */}
      <path d="M137 90 L173 90 L179 128 L131 128 Z" fill="#3A3F4E" />
      <rect x="131" y="118" width="48" height="5" fill="#F4C430" />
      <ellipse cx="155" cy="105" rx="11" ry="6.5" fill="#F4C430" />
      <path d="M147.5 105 l3-3.2 2.2 2 2.3-2.4 2.3 2.4 2.2-2 3 3.2 -3 2.2 -2.2-1 -2.3 2.2 -2.3-2.2 -2.2 1 z" fill="#1F2430" />
      {/* kollar */}
      <path d="M137 96 C128 100 118 106 112 112" stroke="#3A3F4E" strokeWidth="9" strokeLinecap="round" fill="none" />
      <path d="M173 96 C180 102 184 110 184 118" stroke="#3A3F4E" strokeWidth="9" strokeLinecap="round" fill="none" />
      <circle cx="184" cy="119" r="5.5" fill="#1F2430" />
      {/* kafa + maske */}
      <path d="M126 44 L121 12 L147 30 Z" fill="#1F2430" />
      <path d="M184 44 L189 12 L163 30 Z" fill="#1F2430" />
      <path d="M118 62 C118 36 136 24 155 24 C174 24 192 36 192 62 C192 82 176 92 155 92 C134 92 118 82 118 62 Z" fill="#1F2430" />
      <path d="M135 70 C137 90 173 90 175 70 C166 77 144 77 135 70 Z" fill="#F3CBAA" />
      <path d="M149 83 Q155 87 161 83" stroke="#7A4B3A" strokeWidth="1.6" strokeLinecap="round" fill="none" />
      <path d="M138 58 L154 61 L151 69 L137 66 Z" fill="#fff" />
      <path d="M172 58 L156 61 L159 69 L173 66 Z" fill="#fff" />
    </g>

    {/* ── Hello Kitty (sol) ── */}
    <g className="ar-kitty">
      {/* bacaklar / ayaklar */}
      <ellipse cx="52" cy="128" rx="11" ry="6" fill="#fff" stroke="#222" strokeWidth="1.6" />
      <ellipse cx="78" cy="128" rx="11" ry="6" fill="#fff" stroke="#222" strokeWidth="1.6" />
      {/* tulum */}
      <path d="M44 92 L86 92 L92 124 L38 124 Z" fill="#3B7DD8" stroke="#222" strokeWidth="1.6" strokeLinejoin="round" />
      <rect x="55" y="92" width="20" height="10" fill="#fff" stroke="#222" strokeWidth="1.4" />
      <circle cx="65" cy="110" r="3" fill="#F4C430" stroke="#222" strokeWidth="1" />
      {/* kollar */}
      <path d="M44 98 C36 104 32 110 34 118" stroke="#222" strokeWidth="9.6" strokeLinecap="round" fill="none" />
      <path d="M44 98 C36 104 32 110 34 118" stroke="#fff" strokeWidth="6.4" strokeLinecap="round" fill="none" />
      <path d="M86 98 C94 102 102 108 108 112" stroke="#222" strokeWidth="9.6" strokeLinecap="round" fill="none" />
      <path d="M86 98 C94 102 102 108 108 112" stroke="#fff" strokeWidth="6.4" strokeLinecap="round" fill="none" />
      <circle cx="34" cy="119" r="5.2" fill="#fff" stroke="#222" strokeWidth="1.6" />
      {/* el ele */}
      <circle cx="110" cy="113" r="6" fill="#fff" stroke="#222" strokeWidth="1.6" />
      <circle cx="113" cy="114" r="4.6" fill="#1F2430" />
      {/* kafa */}
      <path d="M30 44 L26 16 L52 30 Z" fill="#fff" stroke="#222" strokeWidth="1.8" strokeLinejoin="round" />
      <path d="M100 44 L104 16 L78 30 Z" fill="#fff" stroke="#222" strokeWidth="1.8" strokeLinejoin="round" />
      <path d="M22 62 C22 36 42 24 65 24 C88 24 108 36 108 62 C108 82 90 92 65 92 C40 92 22 82 22 62 Z" fill="#fff" stroke="#222" strokeWidth="1.8" />
      {/* fiyonk */}
      <g transform="translate(88 30)">
        <path d="M0 0 C-12 -8 -16 6 -4 6 Z" fill="#E8303A" stroke="#222" strokeWidth="1.3" strokeLinejoin="round" />
        <path d="M0 0 C12 -10 20 4 6 6 Z" fill="#E8303A" stroke="#222" strokeWidth="1.3" strokeLinejoin="round" />
        <circle cx="1" cy="2" r="3.2" fill="#E8303A" stroke="#222" strokeWidth="1.3" />
      </g>
      {/* yüz */}
      <ellipse cx="50" cy="62" rx="2.8" ry="5" fill="#222" />
      <ellipse cx="80" cy="62" rx="2.8" ry="5" fill="#222" />
      <ellipse cx="65" cy="71" rx="4" ry="2.8" fill="#F4C430" stroke="#222" strokeWidth="1" />
      <g stroke="#222" strokeWidth="1.5" strokeLinecap="round">
        <path d="M8 56 L33 61 M6 67 L33 67 M8 78 L33 73" />
        <path d="M122 56 L97 61 M124 67 L97 67 M122 78 L97 73" />
      </g>
    </g>
  </svg>
);

/* ───────────────────────────── Asılı kalp (üst çubuktan sarkar) ───────────────────────────── */
export const KalpAskisiCizim: React.FC = () => (
  <svg viewBox="0 0 40 96" width="40" height="96" aria-hidden="true">
    <defs>
      <linearGradient id="ar-aski-g" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stopColor="#FF8FB0" /><stop offset=".55" stopColor={T.kalp} /><stop offset="1" stopColor={T.kalpKoyu} />
      </linearGradient>
    </defs>
    <path d="M20 0 V54" stroke="#C98A73" strokeWidth="1.4" strokeDasharray="3 2" />
    <circle cx="20" cy="55" r="2.4" fill="#C98A73" />
    <g className="ar-aski-kalp" transform="translate(20 76)">
      <circle r="24" fill="transparent" />
      <path transform="translate(-19 -18) scale(1.6)" d={KALP_YOLU} fill="url(#ar-aski-g)" />
      <ellipse cx="-7" cy="-7" rx="3" ry="4.2" fill="#fff" opacity=".5" transform="rotate(-28 -7 -7)" />
    </g>
  </svg>
);

/* ───────────────────────────── Sekme simgesi: tilki + kalp ───────────────────────────── */
export const ARZU_FAVICON_SVG = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FF8FB0"/><stop offset=".55" stop-color="#FF5C86"/><stop offset="1" stop-color="#E8306A"/></linearGradient></defs><rect width="512" height="512" rx="116" fill="url(#g)"/><path d="M118 214 L98 88 L214 166 Z" fill="#EF7F2F"/><path d="M394 214 L414 88 L298 166 Z" fill="#EF7F2F"/><path d="M130 208 L116 118 L196 170 Z" fill="#2B1A12" opacity=".7"/><path d="M382 208 L396 118 L316 170 Z" fill="#2B1A12" opacity=".7"/><path d="M256 150 C166 150 108 212 108 288 C108 366 180 412 256 412 C332 412 404 366 404 288 C404 212 346 150 256 150Z" fill="#EF7F2F"/><path d="M136 300 C150 364 212 398 256 398 C300 398 362 364 376 300 C344 340 300 356 256 356 C212 356 168 340 136 300Z" fill="#FFF6EC"/><ellipse cx="204" cy="268" rx="14" ry="18" fill="#2B1A12"/><ellipse cx="308" cy="268" rx="14" ry="18" fill="#2B1A12"/><circle cx="199" cy="261" r="5" fill="#fff"/><circle cx="303" cy="261" r="5" fill="#fff"/><path d="M236 318 C236 306 276 306 276 318 C276 330 256 340 256 340 C256 340 236 330 236 318Z" fill="#1E130E"/><path transform="translate(300 300) scale(7.2)" d="${KALP_YOLU}" fill="#fff" opacity=".95"/></svg>`;
