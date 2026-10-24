/**
 * KMB Lottie videosu — video oynatıcı hissi: oynat/duraklat, bölüm işaretli zaman çubuğu, süre, hız, altyazı, tam ekran,
 * klavye (boşluk/k, ←/→ 5 sn, f tam ekran, c altyazı). Ses EMA klibi `l-<ad>` (src/data/kmb/ses_<kod>.json); ses yoksa iç saat.
 * `zaman` verilirse (ders videosu içinde) sessiz çalışır ve kareyi dışarıdaki saate göre (döngüyle) çizer.
 * Lottie JSON ve bölüm/etiket/sayaç bilgisi scripts/kmb/lottie_uret.py üretir (src/data/kmb/lottie/).
 */
import React, { useCallback, useEffect, useRef, useState } from 'react';
import { getCustomApiUrl } from '../../services/api';
import LINDEX from '../../data/kmb/lottie/index.json';
import AINDEX from '../../data/kmb/lottie/adimlar.json';

export type LottieBilgi = {
  ad: string; baslik: string; sure: number; sesli?: boolean;
  bolumler: { baslik: string; metin: string; bas: number; son: number; ses_bas?: number }[];
  kamera?: [number, number, number, number][];
  etiketler: { bas: number; son: number; x: number; y: number; metin: string; tur: string }[];
  sayaclar: { bas: number; son: number; v1: number; v2: number; birim: string; x: number; y: number; ondalik: number }[];
  adim?: string;
};
type SesKayit = Record<string, { h: string; sure: number; zaman: [number, number][] }>;

/** Konu videoları (lottie_uret.py) + adım videoları (adim_lottie.py: her cümle bir bölüm, ses `o-<adım>`) */
export const LOTTILER = [...(LINDEX as LottieBilgi[]), ...(AINDEX as LottieBilgi[])];
export const klipAdi = (v: LottieBilgi) => (v.adim ? `o-${v.adim}` : `l-${v.ad}`);
const VERI = import.meta.glob(['../../data/kmb/lottie/*.json', '!../../data/kmb/lottie/index.json', '!../../data/kmb/lottie/adimlar.json']);
const sn = (t: number) => `${Math.floor(t / 60)}:${String(Math.floor(t % 60)).padStart(2, '0')}`;
export const KMB_DURDUR = 'kmb-durdur';

/** Kamera (lottie_dsl.kamera ile aynı kareler; Lottie kolaylaştırmasına yakın smoothstep) → [cx, cy, z] */
export function kameraAn(v: LottieBilgi, t: number): [number, number, number] {
  const k = v.kamera;
  if (!k?.length) return [400, 250, 100];
  if (t <= k[0][0]) return [k[0][1], k[0][2], k[0][3]];
  for (let i = 0; i < k.length - 1; i++) {
    const [a, b] = [k[i], k[i + 1]];
    if (t <= b[0]) {
      const f = b[0] === a[0] ? 1 : (t - a[0]) / (b[0] - a[0]);
      const e = f * f * (3 - 2 * f);
      return [a[1] + (b[1] - a[1]) * e, a[2] + (b[2] - a[2]) * e, a[3] + (b[3] - a[3]) * e];
    }
  }
  const s = k[k.length - 1];
  return [s[1], s[2], s[3]];
}

/** Video saatinden ses saatine: bölüm içindeyse ses zamanı, bekleme payındaysa null */
export function sesZamani(v: LottieBilgi, t: number): number | null {
  for (const b of v.bolumler) {
    if (b.ses_bas === undefined) return t;
    if (t >= b.bas && t < b.son + 0.15) return b.ses_bas + (t - b.bas);
  }
  return null;
}

/** Üstteki HTML katmanı: etiketler + sayaçlar (Lottie'de yazı yok; Türkçe karakterler net) */
export function Katman({ v, t }: { v: LottieBilgi; t: number }) {
  const [cx, cy, z] = kameraAn(v, t);
  const k = z / 100;
  const yer = (x: number, y: number) => ({ left: `${(400 + (x - cx) * k) / 8}%`, top: `${(250 + (y - cy) * k) / 5}%` });
  return (
    <div className="kmb-lv-katman" aria-hidden>
      {v.etiketler.filter((e) => t >= e.bas && t <= e.son).map((e, i) => (
        <span key={i} className={`kmb-lv-etiket ${e.tur}`} style={yer(e.x, e.y)}>{e.metin}</span>
      ))}
      {v.sayaclar.filter((s) => t >= s.bas).map((s, i) => {
        const f = Math.min(1, Math.max(0, (t - s.bas) / Math.max(0.01, s.son - s.bas)));
        return <span key={`s${i}`} className="kmb-lv-sayac" style={yer(s.x, s.y)}>{(s.v1 + (s.v2 - s.v1) * f).toFixed(s.ondalik)} {s.birim}</span>;
      })}
    </div>
  );
}

export default function LottieVideo({ ad, kod, ses, zaman, kompakt }: { ad: string; kod: string; ses: SesKayit | null; zaman?: number; kompakt?: boolean }) {
  const v = LOTTILER.find((x) => x.ad === ad);
  const kap = useRef<HTMLDivElement>(null);
  const sahne = useRef<HTMLDivElement>(null);
  const anim = useRef<any>(null);
  const audio = useRef<HTMLAudioElement | null>(null);
  const saat = useRef({ bas: 0, t: 0 });
  const [t, setT] = useState(0);
  const [cal, setCal] = useState(false);
  const [hiz, setHiz] = useState(1);
  const [altyazi, setAltyazi] = useState(true);
  const [tam, setTam] = useState(false);
  const klip = v ? ses?.[klipAdi(v)] : undefined;
  const dis = zaman !== undefined;
  const sure = v?.sure || 1;

  useEffect(() => {
    let iptal = false;
    const yukle = VERI[`../../data/kmb/lottie/${ad}.json`];
    if (!yukle || !sahne.current) return;
    Promise.all([yukle(), import('lottie-web/build/player/lottie_light')]).then(([m, L]: any[]) => {
      if (iptal || !sahne.current) return;
      anim.current = (L.default || L).loadAnimation({ container: sahne.current, renderer: 'svg', loop: false, autoplay: false, animationData: m.default || m,
        rendererSettings: { preserveAspectRatio: 'xMidYMid meet' } });
      anim.current.goToAndStop(0, true);
    });
    return () => { iptal = true; anim.current?.destroy(); anim.current = null; };
  }, [ad]);

  const kareyeGit = useCallback((s: number) => { anim.current?.goToAndStop(Math.min(s, sure - 0.05) * 30, true); }, [sure]);

  // dış saat (ders videosu): döngüyle çiz
  useEffect(() => { if (dis) { const s = (zaman as number) % sure; kareyeGit(s); setT(s); } }, [dis, zaman, sure, kareyeGit]);

  const durdur = useCallback(() => { audio.current?.pause(); setCal(false); }, []);
  const git = useCallback((s: number) => {
    const y = Math.max(0, Math.min(sure, s));
    saat.current = { bas: performance.now(), t: y };
    kareyeGit(y); setT(y);
  }, [sure, kareyeGit]);
  const oynat = useCallback((bas?: number) => {
    window.dispatchEvent(new CustomEvent(KMB_DURDUR, { detail: ad }));
    const s = bas ?? (t >= sure - 0.1 ? 0 : t);
    if (klip && !audio.current) audio.current = new Audio(`${getCustomApiUrl() || ''}/api/cozucu-ses/kmb/ema/${kod}/${klipAdi(v!)}.mp3?v=${klip.h}`);
    saat.current = { bas: performance.now(), t: s };
    setCal(true);
  }, [t, sure, klip, kod, ad, v]);

  // Oynatma döngüsü: saat video saatidir (bekleme payları dahil). Ses yalnız bölüm içinde, ses saatine eşlenerek çalar;
  // payda durur. Sapma 0,25 sn'yi geçerse ses yeniden konumlanır.
  useEffect(() => {
    if (!cal || dis) return;
    let id = 0, son = 0;
    const adim = (now: number) => {
      let s = saat.current.t + ((now - saat.current.bas) / 1000) * hiz;
      const a = audio.current;
      if (a && klip && v) {
        const hedef = sesZamani(v, s);
        if (hedef === null || hedef >= klip.sure) { if (!a.paused) a.pause(); }
        else {
          a.playbackRate = hiz;
          if (a.paused) { a.currentTime = hedef; a.play().catch(() => { /* ses açılamadı: görüntü sürer */ }); }
          else if (Math.abs(a.currentTime - hedef) > 0.25) a.currentTime = hedef;
        }
      }
      if (s >= sure) { s = sure; a?.pause(); kareyeGit(s); setT(s); setCal(false); return; }
      kareyeGit(s);
      if (now - son > 50) { setT(s); son = now; }
      id = requestAnimationFrame(adim);
    };
    id = requestAnimationFrame(adim);
    return () => { cancelAnimationFrame(id); audio.current?.pause(); };
  }, [cal, dis, klip, hiz, sure, kareyeGit, v]);

  useEffect(() => { if (audio.current) audio.current.playbackRate = hiz; }, [hiz]);
  useEffect(() => {
    const f = (e: Event) => { if ((e as CustomEvent).detail !== ad) durdur(); };
    window.addEventListener(KMB_DURDUR, f);
    return () => { window.removeEventListener(KMB_DURDUR, f); audio.current?.pause(); };
  }, [ad, durdur]);
  useEffect(() => {
    const f = () => setTam(document.fullscreenElement === kap.current);
    document.addEventListener('fullscreenchange', f);
    return () => document.removeEventListener('fullscreenchange', f);
  }, []);
  const tamEkran = () => { if (document.fullscreenElement) document.exitFullscreen(); else kap.current?.requestFullscreen?.(); };
  const tus = (e: React.KeyboardEvent) => {
    if (e.key === ' ' || e.key === 'k') { e.preventDefault(); if (cal) durdur(); else oynat(); }
    else if (e.key === 'ArrowRight') git(t + 5);
    else if (e.key === 'ArrowLeft') git(t - 5);
    else if (e.key === 'f') tamEkran();
    else if (e.key === 'c') setAltyazi((x) => !x);
  };

  if (!v) return null;
  const bi = Math.max(0, v.bolumler.findIndex((b, i) => t < (v.bolumler[i + 1]?.bas ?? Infinity)));
  const bolum = v.bolumler[bi];
  const konusuyor = bolum && t >= bolum.bas - 0.2 && t <= bolum.son + 0.3;

  if (dis) {
    return (
      <div className="kmb-lv kmb-lv-dis">
        <div className="kmb-lv-sahne"><div ref={sahne} className="kmb-lv-lottie" /><Katman v={v} t={t} /></div>
      </div>
    );
  }
  return (
    <div ref={kap} className={`kmb-lv${tam ? ' tam' : ''}${kompakt ? ' kompakt' : ''}`} tabIndex={0} onKeyDown={tus} aria-label={`Video: ${v.baslik}`}>
      <div className="kmb-lv-sahne" onClick={() => (cal ? durdur() : oynat())}>
        <div ref={sahne} className="kmb-lv-lottie" />
        <Katman v={v} t={t} />
        {!cal && <span className="kmb-lv-buyuk-oynat" aria-hidden>▶</span>}
        {tam && <div className="kmb-lv-ust"><b>{v.baslik}</b><span>{bolum?.baslik}</span></div>}
      </div>
      {altyazi && <div className={`kmb-lv-altyazi${konusuyor ? '' : ' sessiz'}`}>{bolum?.metin}</div>}
      <div className="kmb-lv-cubuk">
        <div className="kmb-lv-zaman">
          {v.bolumler.map((b, i) => <span key={i} className="kmb-lv-bolum-isaret" style={{ left: `${(b.bas / sure) * 100}%` }} title={b.baslik} />)}
          <div className="kmb-lv-dolu" style={{ width: `${(t / sure) * 100}%` }} />
          <input type="range" min={0} max={sure} step={0.05} value={t} aria-label="Zaman" onChange={(e) => git(Number(e.target.value))} />
        </div>
        <div className="kmb-lv-dugmeler">
          <button onClick={() => (cal ? durdur() : oynat())} aria-label={cal ? 'Duraklat' : 'Oynat'}>{cal ? '❚❚' : '▶'}</button>
          <button onClick={() => git(t - 5)} aria-label="5 sn geri">↺5</button>
          <button onClick={() => git(t + 5)} aria-label="5 sn ileri">5↻</button>
          <span className="kmb-lv-sure">{sn(t)} / {sn(sure)}</span>
          <span className="kmb-lv-baslik">{v.baslik}{bolum ? ` · ${bolum.baslik}` : ''}</span>
          <select value={hiz} onChange={(e) => setHiz(Number(e.target.value))} aria-label="Hız">
            {[0.75, 1, 1.25, 1.5].map((h) => <option key={h} value={h}>{h}×</option>)}
          </select>
          <button className={altyazi ? 'etkin' : ''} onClick={() => setAltyazi((x) => !x)} aria-label="Altyazı">CC</button>
          <button onClick={tamEkran} aria-label="Tam ekran">{tam ? '⤡' : '⤢'}</button>
        </div>
      </div>
      {!kompakt && (
        <ol className="kmb-lv-bolumler">
          {v.bolumler.map((b, i) => (
            <li key={i} className={i === bi ? 'etkin' : ''}><button onClick={() => { git(b.bas); oynat(b.bas); }}><span>{sn(b.bas)}</span> {b.baslik}</button></li>
          ))}
        </ol>
      )}
    </div>
  );
}
