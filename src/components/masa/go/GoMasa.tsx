/**
 * Go masası: ahşap tahta (SVG), koy → onayla, son hamle halkası, ko işareti, kâsedeki esirler, saat, sayım ekranı.
 * Kurallar motor/go.ts; ekran yalnız son görünümden çizilir.
 */
import React, { useEffect, useMemo, useRef, useState } from 'react';
import { AnimatePresence, motion } from 'motion/react';
import { Check, Flag, Play, RotateCcw, SkipForward, X } from 'lucide-react';
import type { GoGorunum, GoTas, OdaGorunum } from '../../../services/masa/tipler';
import { masa } from '../../../services/masa/istemci';
import { azHareket, sesCal, titret } from '../ortak';
import { Onay } from '../kabukOrtak';
import { OyuncuSerit, benOyuncuMu, rakipId } from '../tahta/ortak';
import '../../../styles/masa/tahta.css';

const HARF = 'ABCDEFGHJKLMNOPQRST';

export default function GoMasa({ oda }: { oda: OdaGorunum }) {
  const g = oda.oyun?.tur === 'go' ? (oda.oyun as GoGorunum) : null;
  if (!g) return null;
  return <Tahta oda={oda} g={g} />;
}

function Tahta({ oda, g }: { oda: OdaGorunum; g: GoGorunum }) {
  const n = g.boyut, ben = oda.ben, oyuncu = benOyuncuMu(oda);
  const rakip = rakipId(oda);
  const benRenk: GoTas = g.renkler[ben] || 'S';
  const etkin = oyuncu && oda.asama === 'oyun' && !oda.durdu && !g.bitti;
  const siraBende = etkin && g.asama === 'oyun' && g.sira === ben;
  const sayim = g.asama === 'sayim';
  const asistan = oda.ayar.asistan !== false;
  const [secim, setSecim] = useState<number | null>(null);
  const [teslim, setTeslim] = useState(false);
  const yasal = useMemo(() => new Set(g.yasal), [g.yasal]);
  const olu = useMemo(() => new Set(g.olu), [g.olu]);
  const alanS = useMemo(() => new Set(g.alan?.S || []), [g.alan]);
  const alanB = useMemo(() => new Set(g.alan?.B || []), [g.alan]);
  const az = azHareket();

  // Sıra değişince seçim düşer; taş sesi
  useEffect(() => { setSecim(null); }, [g.hamleSayisi, g.asama]);
  const onceki = useRef(g.hamleSayisi);
  useEffect(() => {
    if (g.hamleSayisi > onceki.current && g.son) { sesCal(g.son.i >= 0 ? 'birak' : 'sira'); if (g.sira === ben && !g.bitti) sesCal('sira'); }
    onceki.current = g.hamleSayisi;
  }, [g.hamleSayisi]); // eslint-disable-line react-hooks/exhaustive-deps

  // Alınan taşlar: önceki tahtada olup şimdi boşalanlar kısa süre "uçan" taş olarak çizilir
  const oncekiTahta = useRef(g.tahta);
  const [ucan, setUcan] = useState<{ i: number; r: GoTas; k: number }[]>([]);
  useEffect(() => {
    const eski = oncekiTahta.current;
    const giden = eski.length === g.tahta.length ? eski.map((r, i) => (r && !g.tahta[i] ? { i, r: r as GoTas, k: Date.now() + i } : null)).filter(Boolean) as { i: number; r: GoTas; k: number }[] : [];
    oncekiTahta.current = g.tahta;
    if (!giden.length || az) return;
    setUcan(giden);
    const t = setTimeout(() => setUcan([]), 700);
    return () => clearTimeout(t);
  }, [g.tahta]); // eslint-disable-line react-hooks/exhaustive-deps

  const dokun = (i: number) => {
    if (!etkin) return;
    if (sayim) { if (g.tahta[i]) { masa.hamle({ t: 'olu', i }); titret(8); } return; }
    if (!siraBende || g.tahta[i]) return;
    if (!yasal.has(i)) { sesCal('hata'); titret([10, 40, 10]); return; }
    if (secim === i) { koy(); return; }
    setSecim(i); sesCal('tas'); titret(6);
  };
  const koy = () => {
    if (secim == null) return;
    masa.hamle({ t: 'koy', i: secim }); titret(14);
    setSecim(null);
  };

  // SVG ölçüleri: kesişim aralığı 1 birim, kenar payı 0.9 (koordinat harfleri için)
  const P = 0.9, W = n - 1 + 2 * P;
  const xy = (i: number) => ({ x: P + (i % n), y: P + Math.floor(i / n) });
  const r = 0.47;

  const esirS = g.esir.S, esirB = g.esir.B;
  const renkAd = (c: GoTas) => (c === 'S' ? 'Siyah' : 'Beyaz');
  const ustRenk: GoTas = benRenk === 'S' ? 'B' : 'S';

  return (
    <div className="tm-kok tm-go">
      <div className="tm-go-ahsap" aria-hidden="true" />
      <OyuncuSerit oda={oda} id={rakip} isaret={<><i className={`tm-go-ikon is-${ustRenk}`} />{renkAd(ustRenk)}{ustRenk === 'B' && <small> · komi {String(g.komi).replace('.', ',')}</small>}</>}
        sag={<><Saat g={g} renk={ustRenk} aktif={!sayim && g.sira === rakip && oda.asama === 'oyun' && !oda.durdu} /><Kase renk={ustRenk === 'S' ? 'B' : 'S'} sayi={ustRenk === 'S' ? esirS : esirB} /></>} />

      <div className="tm-go-sahne">
        <svg className="tm-go-tahta" viewBox={`0 0 ${W} ${W}`} role="grid" aria-label={`${n}×${n} Go tahtası`}>
          <defs>
            <radialGradient id="tm-go-s" cx="35%" cy="30%" r="75%"><stop offset="0" stopColor="#6b6b6b" /><stop offset=".35" stopColor="#262626" /><stop offset="1" stopColor="#050505" /></radialGradient>
            <radialGradient id="tm-go-b" cx="35%" cy="30%" r="80%"><stop offset="0" stopColor="#ffffff" /><stop offset=".6" stopColor="#ece9e1" /><stop offset="1" stopColor="#c9c3b6" /></radialGradient>
            <linearGradient id="tm-go-zemin" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stopColor="#e9c27a" /><stop offset=".5" stopColor="#ddb065" /><stop offset="1" stopColor="#cf9f55" /></linearGradient>
            <filter id="tm-go-golge" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx=".05" dy=".08" stdDeviation=".05" floodOpacity=".45" /></filter>
          </defs>
          <rect x="0" y="0" width={W} height={W} rx=".25" fill="url(#tm-go-zemin)" />
          {/* ağaç damarı */}
          {Array.from({ length: 9 }, (_, k) => (
            <path key={k} d={`M0 ${(k + 0.5) * W / 9} C ${W * 0.3} ${(k + 0.2) * W / 9}, ${W * 0.6} ${(k + 0.9) * W / 9}, ${W} ${(k + 0.4) * W / 9}`} stroke="#b5823f" strokeOpacity=".18" strokeWidth=".06" fill="none" />
          ))}
          {Array.from({ length: n }, (_, k) => (
            <g key={k} stroke="#2a1c0c" strokeWidth={k === 0 || k === n - 1 ? 0.045 : 0.028}>
              <line x1={P} y1={P + k} x2={P + n - 1} y2={P + k} />
              <line x1={P + k} y1={P} x2={P + k} y2={P + n - 1} />
            </g>
          ))}
          {Array.from({ length: n }, (_, k) => (
            <g key={`h${k}`} className="tm-go-koor" fontSize=".32">
              <text x={P + k} y={P * 0.45} textAnchor="middle" dominantBaseline="middle">{HARF[k]}</text>
              <text x={P * 0.42} y={P + k} textAnchor="middle" dominantBaseline="middle">{n - k}</text>
            </g>
          ))}
          {g.yildiz.map((i) => { const p = xy(i); return <circle key={`y${i}`} cx={p.x} cy={p.y} r=".09" fill="#2a1c0c" />; })}

          {/* sayım: alan noktaları */}
          {sayim && g.tahta.map((_, i) => {
            const a = alanS.has(i) ? 'S' : alanB.has(i) ? 'B' : null;
            if (!a) return null;
            const p = xy(i);
            return <rect key={`a${i}`} x={p.x - 0.15} y={p.y - 0.15} width=".3" height=".3" rx=".04" className={`tm-go-alan is-${a}`} />;
          })}

          {/* taşlar */}
          {g.tahta.map((t, i) => {
            if (!t) return null;
            const p = xy(i), o = olu.has(i);
            return (
              <motion.g key={`t${i}-${t}`} initial={az ? false : { scale: 1.25, opacity: 0.4 }} animate={{ scale: 1, opacity: o ? 0.42 : 1 }} transition={{ type: 'spring', stiffness: 520, damping: 22 }} style={{ transformOrigin: `${p.x}px ${p.y}px`, transformBox: 'view-box' }}>
                <circle cx={p.x} cy={p.y} r={r} fill={`url(#tm-go-${t === 'S' ? 's' : 'b'})`} filter="url(#tm-go-golge)" />
                {o && <path d={`M${p.x - 0.2} ${p.y - 0.2}L${p.x + 0.2} ${p.y + 0.2}M${p.x + 0.2} ${p.y - 0.2}L${p.x - 0.2} ${p.y + 0.2}`} stroke="#c0392b" strokeWidth=".08" strokeLinecap="round" />}
              </motion.g>
            );
          })}
          <AnimatePresence>
            {ucan.map((u) => {
              const p = xy(u.i), hedefY = (u.r === benRenk) === true ? W + 1 : -1; // alınan taş alanın kâsesine
              return (
                <motion.circle key={u.k} cx={p.x} cy={p.y} r={r} fill={`url(#tm-go-${u.r === 'S' ? 's' : 'b'})`}
                  initial={{ opacity: 1 }} animate={{ opacity: 0, cy: hedefY, cx: W - 1 }} transition={{ duration: 0.65, ease: 'easeIn' }} />
              );
            })}
          </AnimatePresence>

          {g.son && g.son.i >= 0 && g.tahta[g.son.i] && (() => { const p = xy(g.son.i); return <circle cx={p.x} cy={p.y} r=".2" fill="none" stroke={g.tahta[g.son.i] === 'S' ? '#fff' : '#111'} strokeWidth=".06" />; })()}
          {g.ko != null && !sayim && (() => { const p = xy(g.ko); return <rect x={p.x - 0.14} y={p.y - 0.14} width=".28" height=".28" fill="none" stroke="#7a1f12" strokeWidth=".06" />; })()}

          {/* koy → onayla: yarı saydam taş + kesişim vurgu çizgileri */}
          {secim != null && (() => {
            const p = xy(secim);
            return (
              <g pointerEvents="none">
                <line x1={P} y1={p.y} x2={P + n - 1} y2={p.y} className="tm-go-vurgu" />
                <line x1={p.x} y1={P} x2={p.x} y2={P + n - 1} className="tm-go-vurgu" />
                <circle cx={p.x} cy={p.y} r={r} fill={`url(#tm-go-${benRenk === 'S' ? 's' : 'b'})`} opacity=".62" />
              </g>
            );
          })()}

          {/* dokunma alanları (asistan açıkken yasal noktalarda gölge) */}
          {g.tahta.map((t, i) => {
            const p = xy(i);
            const gol = asistan && siraBende && !t && yasal.has(i) && secim == null && n <= 9;
            return (
              <g key={`d${i}`}>
                {gol && <circle cx={p.x} cy={p.y} r=".09" className="tm-go-golge-nokta" />}
                <rect x={p.x - 0.5} y={p.y - 0.5} width="1" height="1" fill="transparent" role="gridcell"
                  aria-label={`${HARF[i % n]}${n - Math.floor(i / n)}${t ? (t === 'S' ? ' siyah taş' : ' beyaz taş') : ''}`}
                  onClick={() => dokun(i)} style={{ cursor: etkin && (sayim ? !!t : siraBende && !t) ? 'pointer' : 'default' }} />
              </g>
            );
          })}
        </svg>
      </div>

      {sayim && g.puan && (
        <div className="tm-go-sayim" role="status">
          <b>Sayım</b>
          <span>Siyah <strong>{g.puan.S}</strong> – Beyaz <strong>{String(g.puan.B).replace('.', ',')}</strong></span>
          <small>Ölü grupları işaretlemek için taşa dokun. İkiniz de onaylayınca el biter. {g.onay.length ? `Onaylayan: ${g.onay.map((o) => (o === ben ? 'sen' : 'rakip')).join(', ')}` : ''}</small>
        </div>
      )}

      <OyuncuSerit oda={oda} id={ben} alt isaret={<><i className={`tm-go-ikon is-${benRenk}`} />{renkAd(benRenk)}{benRenk === 'B' && <small> · komi {String(g.komi).replace('.', ',')}</small>}{g.handikap > 1 && <small> · handikap {g.handikap}</small>}</>}
        sag={<><Saat g={g} renk={benRenk} aktif={!sayim && siraBende} /><Kase renk={benRenk === 'S' ? 'B' : 'S'} sayi={benRenk === 'S' ? esirS : esirB} /></>} />

      {oyuncu && (
        <div className="tm-eylem">
          <button type="button" className="mk-dugme is-soluk" onClick={() => setTeslim(true)} disabled={!etkin} aria-label="Teslim ol"><Flag size={18} /></button>
          {sayim ? (
            <>
              <button type="button" className="mk-dugme is-acik" onClick={() => masa.hamle({ t: 'devam' })} disabled={!etkin}><Play size={18} /> Oyuna dön</button>
              <button type="button" className="mk-dugme is-ana" onClick={() => masa.hamle({ t: 'onayla' })} disabled={!etkin || g.onay.includes(ben)}><Check size={18} /> {g.onay.includes(ben) ? 'Onayladın' : 'Sayımı onayla'}</button>
            </>
          ) : (
            <>
              {(oda.geriAl ?? 0) > 0 && <button type="button" className="mk-dugme is-soluk" onClick={() => { masa.geriAl(); setSecim(null); }} disabled={!siraBende} aria-label="Son hamleni geri al" title="Son hamleni (ve botun yanıtını) geri al"><RotateCcw size={18} /></button>}
              <button type="button" className="mk-dugme is-acik" onClick={() => { masa.hamle({ t: 'pas' }); setSecim(null); }} disabled={!siraBende}><SkipForward size={18} /> Pas</button>
              {secim != null && <button type="button" className="mk-dugme is-soluk" onClick={() => setSecim(null)} aria-label="Seçimi bırak"><X size={18} /></button>}
              <button type="button" className="mk-dugme is-ana" onClick={koy} disabled={secim == null}><Check size={18} /> Onayla</button>
            </>
          )}
        </div>
      )}
      {!sayim && g.son?.i === -1 && !g.bitti && <p className="tm-not" role="status">{g.son.renk === benRenk ? 'Pas dedin.' : 'Rakip pas dedi. Sen de pas dersen sayıma geçilir.'}</p>}
      <Onay ac={teslim} kapat={() => setTeslim(false)} baslik="Teslim ol" onayAd="Teslim ol" tehlike onay={() => masa.hamle({ t: 'teslim' })} metin="Bu eli rakibe bırakırsın." />
    </div>
  );
}

function Kase({ renk, sayi }: { renk: GoTas; sayi: number }) {
  return (
    <span className={`tm-go-kase is-${renk}`} aria-label={`${sayi} esir`}>
      <i />{sayi > 0 && <motion.b key={sayi} initial={{ scale: 1.5 }} animate={{ scale: 1 }}>× {sayi}</motion.b>}
    </span>
  );
}

const sureYaz = (ms: number) => { const s = Math.max(0, Math.ceil(ms / 1000)); return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`; };

/** Saat: ana süre (dk:sn) → bitince byo-yomi (aralık sn × hak). Sıradakinde yerelde geri sayar. */
function Saat({ g, renk, aktif }: { g: GoGorunum; renk: GoTas; aktif: boolean }) {
  const [, setT] = useState(0);
  const alindi = useRef(Date.now());
  useEffect(() => { alindi.current = Date.now(); }, [g]);
  useEffect(() => { if (!aktif || !g.saat) return; const i = setInterval(() => setT((x) => x + 1), 250); return () => clearInterval(i); }, [aktif, g.saat]);
  if (!g.saat) return null;
  const gecen = aktif ? g.saat.gecen + (Date.now() - alindi.current) : 0;
  let ana = g.saat.ana[renk] - gecen, per = g.saat.periyot[renk], byo = g.saat.byo;
  let metin: string;
  if (ana > 0) metin = sureYaz(ana);
  else {
    const asim = -ana, yenen = Math.floor(asim / byo);
    per -= yenen; ana = byo - (asim - yenen * byo);
    metin = per > 0 ? `${Math.ceil(ana / 1000)} sn ×${per}` : '0:00';
  }
  const az = (g.saat.ana[renk] - gecen <= 0 && per <= 1) || (g.saat.ana[renk] - gecen > 0 && g.saat.ana[renk] - gecen < 20_000 && !byo);
  return <span className={`tm-saat${aktif ? ' is-aktif' : ''}${az && aktif ? ' is-az' : ''}`} role="timer" aria-label={`Kalan süre ${metin}`}>{metin}</span>;
}
