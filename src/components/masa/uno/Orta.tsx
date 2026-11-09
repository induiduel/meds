import React, { useEffect, useRef } from 'react';
import type { UnoKart, UnoRenk } from '../../../services/masa/tipler';
import { azHareket } from '../ortak';
import { KartGorsel, RenkBicimi } from './Kart';
import { yiginAci } from './canlandir';
import { temaAl, UNO_SIRA } from './temalar';
import type { Nokta, Yerlesim } from './yerlesim';

export interface YiginKart { kart: UnoKart; vurgu: boolean }

interface Props {
  yer: Yerlesim;
  tema: string;
  yigin: YiginKart[];
  deste: number;
  renk: UnoRenk;
  yon: 1 | -1;
  /** Yön değişiminde artan sayaç (halka vurgusu) */
  yonVurus: number;
  cekilebilir: boolean;
  /** Elden kart sürüklenirken bırakma hedefi parlar */
  hedef: boolean;
  oneriCek: boolean;
  onCek: (kaynak?: Nokta) => void;
  onReddet: () => void;
}

/** Masanın ortası: atık yığını, renk + yön halkası, çekme destesi */
export default function Orta({ yer, tema, yigin, deste, renk, yon, yonVurus, cekilebilir, hedef, oneriCek, onCek, onReddet }: Props) {
  const t = temaAl(tema);
  const ton = t.renk[renk];
  const donRef = useRef<HTMLDivElement>(null);
  const donAn = useRef<Animation | null>(null);

  // Halka sürekli döner; yön değişince hız işareti döner (sıçrama olmaz)
  useEffect(() => {
    const el = donRef.current;
    if (!el || azHareket() || !el.animate) return;
    const an = el.animate([{ transform: 'rotate(0deg)' }, { transform: 'rotate(360deg)' }], { duration: 16000, iterations: Infinity });
    donAn.current = an;
    return () => { an.cancel(); donAn.current = null; };
  }, []);
  useEffect(() => { try { donAn.current?.updatePlaybackRate(yon); } catch { /* yok */ } }, [yon]);

  /* ---- desteden ele sürükleme ---- */
  const ustRef = useRef<HTMLDivElement>(null);
  const s = useRef<{ pid: number; sx: number; sy: number; dx: number; dy: number; oynadi: boolean; raf: number } | null>(null);
  const birak = (geri: boolean) => {
    const el = ustRef.current;
    const d = s.current;
    s.current = null;
    if (d) cancelAnimationFrame(d.raf);
    if (!el) return;
    el.classList.remove('um-havada');
    if (geri) { el.classList.add('um-donus'); window.setTimeout(() => el.classList.remove('um-donus'), 480); }
    el.style.transform = '';
  };
  const asagi = (e: React.PointerEvent) => {
    if (s.current || (e.pointerType === 'mouse' && e.button !== 0)) return;
    s.current = { pid: e.pointerId, sx: e.clientX, sy: e.clientY, dx: 0, dy: 0, oynadi: false, raf: 0 };
    try { e.currentTarget.setPointerCapture(e.pointerId); } catch { /* yok */ }
  };
  const hareket = (e: React.PointerEvent) => {
    const d = s.current;
    if (!d || d.pid !== e.pointerId) return;
    d.dx = e.clientX - d.sx; d.dy = e.clientY - d.sy;
    if (!d.oynadi) {
      if (Math.hypot(d.dx, d.dy) < 8 || !cekilebilir) return;
      d.oynadi = true;
      ustRef.current?.classList.add('um-havada');
    }
    if (!d.raf) d.raf = requestAnimationFrame(() => {
      d.raf = 0;
      if (s.current === d && ustRef.current) ustRef.current.style.transform = `translate3d(${d.dx}px, ${d.dy}px, 0) rotate(${Math.max(-12, Math.min(12, d.dx * 0.06))}deg) scale(1.12)`;
    });
  };
  const yukari = (e: React.PointerEvent) => {
    const d = s.current;
    if (!d || d.pid !== e.pointerId) return;
    if (!d.oynadi) { birak(false); if (cekilebilir) onCek(); else onReddet(); return; }
    const y = yer.deste.y + d.dy;
    if (y > yer.elUst - yer.kh * 0.35) { birak(false); onCek({ x: yer.deste.x + d.dx, y }); } else birak(true);
  };
  const iptal = (e: React.PointerEvent) => { if (s.current?.pid === e.pointerId) birak(true); };

  const kat = Math.min(3, Math.max(0, Math.ceil(deste / 12)));
  const ISIK = yer.halka * 2.4;
  const C = 2 * Math.PI * 52;
  const dilim = C / 3;
  return (
    <div className="um-orta">
      <div className="um-isik-yer" style={{ transform: `translate3d(${yer.atik.x}px, ${yer.atik.y}px, 0)` }} aria-hidden="true">
        <div className="um-isik-kap" style={{ width: ISIK, height: ISIK }}>
          {UNO_SIRA.map((r) => <div key={r} className={`um-isik${r === renk ? ' um-acik' : ''}`} style={{ background: `radial-gradient(closest-side, ${t.renk[r].ana}, transparent)` }} />)}
        </div>
      </div>

      <div className={`um-halka-yer${hedef ? ' um-hedef' : ''}`} style={{ transform: `translate3d(${yer.atik.x}px, ${yer.atik.y}px, 0)` }}>
        <div className="um-halka" style={{ width: yer.halka, height: yer.halka }}>
          {yonVurus > 0 && <div key={yonVurus} className="um-halka-nabiz" style={{ borderColor: ton.acik }} aria-hidden="true" />}
          <div className="um-halka-vur">
            <div ref={donRef} className="um-halka-don">
              <svg className="um-halka-svg" viewBox="-62 -62 124 124" style={{ transform: `scaleX(${yon})` }} aria-hidden="true">
                <circle r="52" fill="none" stroke="rgba(255,255,255,.14)" strokeWidth="9" />
                <circle r="52" fill="none" stroke={ton.ana} strokeWidth="5.500" strokeLinecap="round" strokeDasharray={`${dilim - 26} 26`} />
                {[0, 1, 2].map((i) => (
                  <polygon key={i} points="-7.500,-3 7.500,-3 0,10" fill={ton.acik} stroke="rgba(0,0,0,.35)" strokeWidth="1" transform={`rotate(${((dilim * (i + 1) - 20) / C) * 360}) translate(52 0)`} />
                ))}
              </svg>
            </div>
          </div>
          <div className="um-hedef-cember" aria-hidden="true" />
        </div>
      </div>

      <div className="um-yigin" style={{ transform: `translate3d(${yer.atik.x}px, ${yer.atik.y}px, 0)` }} aria-label={`Atık yığını. Geçerli renk: ${ton.ad}`} role="group">
        {yigin.map((y, i) => {
          const ust = i === yigin.length - 1;
          const id = y.kart.id;
          const dx = ust ? 0 : (((id * 13) % 15) - 7) * 0.012 * yer.pk;
          const dy = ust ? 0 : (((id * 29) % 13) - 6) * 0.012 * yer.pk;
          return (
            <div key={id} className={`um-yigin-kart${ust ? ' um-ust' : ''}${y.vurgu ? ' um-vurgu' : ''}`} style={{ transform: `translate3d(${dx}px, ${dy}px, 0) rotate(${yiginAci(id) * (ust ? 0.3 : 1)}deg) scale(${ust ? 1 : 0.94})`, width: yer.pk, height: yer.pk * 1.5, marginLeft: -yer.pk / 2, marginTop: -yer.pk * 0.75 }}>
              <KartGorsel kart={y.kart} tema={tema} boy={yer.pk} />
            </div>
          );
        })}
      </div>

      <div className="um-renk-rozet" style={{ transform: `translate3d(${yer.atik.x + yer.halka * 0.36}px, ${yer.atik.y + yer.halka * 0.36}px, 0)` }} title={`Geçerli renk: ${ton.ad}`}>
        <span className="um-renk-rozet-ic" style={{ background: ton.ana }}>
          <svg viewBox="-10 -10 20 20" aria-hidden="true"><RenkBicimi renk={renk} b={5} /></svg>
        </span>
      </div>
      {yer.renkEtiketi && (
        <div className="um-renk-etiket-yer" style={{ transform: `translate3d(${yer.atik.x}px, ${yer.atik.y + yer.halka / 2 + 6}px, 0)` }}>
          <span className="um-renk-etiket" aria-live="polite">Renk: <b>{ton.ad}</b></span>
        </div>
      )}

      <div className="um-deste-yer" style={{ transform: `translate3d(${yer.deste.x}px, ${yer.deste.y}px, 0)` }}>
        <div
          className={`um-deste${cekilebilir ? ' um-cekilebilir' : ''}${oneriCek ? ' um-oneri' : ''}${deste ? '' : ' um-bos'}`}
          style={{ width: yer.pk, height: yer.pk * 1.5 }}
          role="button" tabIndex={0}
          aria-label={`Desteden kart çek (kalan ${deste})`}
          aria-disabled={!cekilebilir}
          onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); if (cekilebilir) onCek(); else onReddet(); } }}
          onPointerDown={asagi} onPointerMove={hareket} onPointerUp={yukari} onPointerCancel={iptal}
          onContextMenu={(e) => e.preventDefault()}
        >
          {Array.from({ length: kat }, (_, i) => (
            <div key={i} className="um-deste-kat" style={{ transform: `translate3d(${-(kat - i) * 1.5}px, ${(kat - i) * 2}px, 0)` }}><KartGorsel tema={tema} boy={yer.pk} kapali /></div>
          ))}
          {deste > 0 && <div ref={ustRef} className="um-deste-ust"><KartGorsel tema={tema} boy={yer.pk} kapali /></div>}
          <span className="um-deste-sayi">{deste}</span>
          {cekilebilir && <span className="um-deste-yazi">Çek</span>}
        </div>
      </div>
    </div>
  );
}
