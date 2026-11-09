/**
 * XOX masası: kâğıt tahta, elle çizilir gibi X/O (çizilme animasyonu), kazanan diziye çekilen çizgi, beraberlikte sarsıntı.
 * Kurallar motor/xox.ts.
 */
import React, { useEffect, useRef } from 'react';
import { motion, useAnimationControls } from 'motion/react';
import { Flag } from 'lucide-react';
import type { OdaGorunum, XoxGorunum } from '../../../services/masa/tipler';
import { masa } from '../../../services/masa/istemci';
import { azHareket, sesCal, titret } from '../ortak';
import { OyuncuSerit, benOyuncuMu, rakipId } from '../tahta/ortak';
import '../../../styles/masa/tahta.css';

const RENK = { X: '#c2410c', O: '#1d4ed8' };

export default function XoxMasa({ oda }: { oda: OdaGorunum }) {
  const x = oda.oyun?.tur === 'xox' ? (oda.oyun as XoxGorunum) : null;
  if (!x) return null;
  return <Tahta oda={oda} x={x} />;
}

function Isaret({ t, cx, cy, s }: { t: 'X' | 'O'; cx: number; cy: number; s: number }) {
  const az = azHareket();
  const anim = (gec = 0) => ({ initial: az ? false as const : { pathLength: 0 }, animate: { pathLength: 1 }, transition: { duration: 0.22, delay: gec, ease: 'easeOut' as const } });
  const r = s * 0.3;
  return t === 'X' ? (
    <g stroke={RENK.X} strokeWidth={s * 0.11} strokeLinecap="round" fill="none">
      <motion.path d={`M${cx - r} ${cy - r * 1.02}Q${cx} ${cy + r * 0.05} ${cx + r * 1.03} ${cy + r}`} {...anim()} />
      <motion.path d={`M${cx + r} ${cy - r}Q${cx + r * 0.05} ${cy} ${cx - r * 0.98} ${cy + r * 1.04}`} {...anim(0.18)} />
    </g>
  ) : (
    <motion.path d={`M${cx} ${cy - r}a${r} ${r} 0 1 1 -0.1 0.02`} stroke={RENK.O} strokeWidth={s * 0.1} strokeLinecap="round" fill="none" {...anim()} />
  );
}

function Tahta({ oda, x }: { oda: OdaGorunum; x: XoxGorunum }) {
  const n = x.boyut, ben = oda.ben, rakip = rakipId(oda), oyuncu = benOyuncuMu(oda);
  const etkin = oyuncu && oda.asama === 'oyun' && !oda.durdu && !x.bitti;
  const siraBende = etkin && x.sira === ben;
  const S = 100, W = n * S;
  const kont = useAnimationControls();
  const dolu = x.tahta.filter(Boolean).length;
  const onceki = useRef(dolu);
  useEffect(() => {
    if (dolu > onceki.current) sesCal('tas');
    onceki.current = dolu;
    if (x.bitti && !x.cizgi && !azHareket()) void kont.start({ x: [0, -8, 8, -5, 5, 0], transition: { duration: 0.45 } });
  }, [dolu, x.bitti]); // eslint-disable-line react-hooks/exhaustive-deps

  const merkez = (i: number) => ({ x: (i % n) * S + S / 2, y: Math.floor(i / n) * S + S / 2 });
  const benIs = x.isaretler[ben], rakipIs = x.isaretler[rakip];
  const ikon = (t?: 'X' | 'O') => t && <b style={{ color: RENK[t] }} className="tm-xox-ikon">{t}</b>;

  return (
    <div className="tm-kok tm-xox">
      <OyuncuSerit oda={oda} id={rakip} isaret={ikon(rakipIs)} sag={<small>{x.hedef}'lü dizi</small>} />
      <div className="tm-xox-sahne">
        <motion.svg animate={kont} className="tm-xox-tahta" viewBox={`-10 -10 ${W + 20} ${W + 20}`} role="grid" aria-label={`${n}×${n} XOX tahtası`}>
          <rect x="-10" y="-10" width={W + 20} height={W + 20} rx="18" className="tm-xox-kagit" />
          {Array.from({ length: n - 1 }, (_, k) => (
            <g key={k} stroke="#3b3b3b" strokeOpacity=".55" strokeWidth="3.5" strokeLinecap="round">
              <path d={`M${(k + 1) * S + (k % 2 ? 1.5 : -1.5)} 8Q${(k + 1) * S + 2} ${W / 2} ${(k + 1) * S - 1} ${W - 8}`} fill="none" />
              <path d={`M8 ${(k + 1) * S - 1}Q${W / 2} ${(k + 1) * S + 2.5} ${W - 8} ${(k + 1) * S + 1}`} fill="none" />
            </g>
          ))}
          {x.tahta.map((t, i) => {
            const m = merkez(i);
            return (
              <g key={i}>
                {t && <Isaret t={t} cx={m.x} cy={m.y} s={S} />}
                {x.son === i && t && <circle cx={m.x + S * 0.36} cy={m.y - S * 0.36} r="5" fill={RENK[t]} />}
                <rect x={m.x - S / 2} y={m.y - S / 2} width={S} height={S} fill="transparent" role="gridcell"
                  aria-label={`${Math.floor(i / n) + 1}. satır ${(i % n) + 1}. sütun${t ? ` ${t}` : ' boş'}`}
                  style={{ cursor: siraBende && !t ? 'pointer' : 'default' }}
                  onClick={() => { if (siraBende && !t) { masa.hamle({ t: 'koy', i }); titret(10); } else if (siraBende) sesCal('hata'); }} />
              </g>
            );
          })}
          {x.cizgi && x.cizgi.length > 1 && (() => {
            const a = merkez(x.cizgi[0]), b = merkez(x.cizgi[x.cizgi.length - 1]);
            const dx = b.x - a.x, dy = b.y - a.y, l = Math.hypot(dx, dy) || 1, u = S * 0.32;
            return (
              <motion.line x1={a.x - (dx / l) * u} y1={a.y - (dy / l) * u} x2={b.x + (dx / l) * u} y2={b.y + (dy / l) * u}
                stroke="#111" strokeOpacity=".75" strokeWidth="9" strokeLinecap="round"
                initial={azHareket() ? false : { pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 0.45, delay: 0.25 }} />
            );
          })()}
        </motion.svg>
      </div>
      <OyuncuSerit oda={oda} id={ben} alt isaret={ikon(benIs)} sag={<small>{n}×{n}</small>} />
      {oyuncu && (
        <div className="tm-eylem">
          <p className="tm-not">{x.bitti ? (x.cizgi ? 'Dizi tamamlandı.' : 'Tahta doldu: berabere.') : siraBende ? 'Boş bir kareye dokun.' : 'Rakip düşünüyor…'}</p>
          <button type="button" className="mk-dugme is-soluk" disabled={!etkin} onClick={() => masa.hamle({ t: 'teslim' })} aria-label="Teslim ol"><Flag size={18} /></button>
        </div>
      )}
    </div>
  );
}
