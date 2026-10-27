/**
 * KMB Lottie videosu — gerçek video oynatıcı gibi: oynat/duraklat, ekranın solunda ve sağında 10 sn geri/ileri (çift dokunma
 * da), bölüm işaretli zaman çubuğu, süre, hız, video üstünde altyazı, tam ekran (iOS'ta sahte tam ekran), denetimler tam
 * ekranda kendiliğinden gizlenir. Klavye: boşluk/k, ←/→ 10 sn, f tam ekran, c altyazı.
 * Başarım (mobil/tablet donması): sayfada aynı anda tek animasyon çalar (KMB_DURDUR); animasyon ancak ekrana yaklaşınca
 * kurulur, uzaklaşınca yok edilir; JSON modül önbelleğinde (ön yükleme `lottieOnYukle`); kare yalnız değişince çizilir,
 * arayüz saati 10 fps. `zaman` verilirse (ders videosu) dış saatle sessiz çizer.
 * Ses: EMA klibi `o-<adım>` (adım videosu) ya da `l-<ad>` (konu videosu); bölüm içinde ses saatine eşlenir, bekleme payında durur.
 * Veri: scripts/kmb/lottie_uret.py + adim_lottie.py → src/data/kmb/lottie/.
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
export const sn = (t: number) => `${Math.floor(t / 60)}:${String(Math.floor(t % 60)).padStart(2, '0')}`;
export const KMB_DURDUR = 'kmb-durdur';
const ATLA = 10;

const ONBELLEK = new Map<string, Promise<any>>();
/** Lottie JSON'unu önbelleğe al (sonraki videoyu önceden yüklemek için) */
export function lottieOnYukle(ad: string): Promise<any> {
  let p = ONBELLEK.get(ad);
  if (!p) {
    const y = VERI[`../../data/kmb/lottie/${ad}.json`];
    p = y ? y().then((m: any) => m.default || m) : Promise.reject(new Error(`video yok: ${ad}`));
    ONBELLEK.set(ad, p);
  }
  return p;
}
/** EMA klibi bütünüyle belleğe alınır (blob): cümle geçişlerinde ses ağdan yeniden konumlanmaz → takılma yok */
const SES = new Map<string, Promise<string>>();
export function sesOnYukle(url: string): Promise<string> {
  let p = SES.get(url);
  if (!p) {
    p = fetch(url).then((r) => (r.ok ? r.blob() : Promise.reject(new Error(String(r.status))))).then((b) => URL.createObjectURL(b))
      .catch(() => { SES.delete(url); return url; });
    SES.set(url, p);
  }
  return p;
}
export const klipUrl = (kod: string, v: LottieBilgi, h: string) => `${getCustomApiUrl() || ''}/api/cozucu-ses/kmb/ema/${kod}/${klipAdi(v)}.mp3?v=${h}`;
let OYNATICI: Promise<any> | null = null;
// canvas çizici: mobil/tablette yüzlerce SVG öğesi yerine tek tuval boyanır (çok daha hızlı)
const oynaticiYukle = () => (OYNATICI ||= import('lottie-web/build/player/lottie_canvas').then((L: any) => L.default || L));

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

export const bolumAn = (v: LottieBilgi, t: number) => Math.max(0, v.bolumler.findIndex((b, i) => t < (v.bolumler[i + 1]?.bas ?? Infinity)));

/** Üstteki HTML katmanı: etiketler + sayaçlar (Türkçe karakterler net); kamerayla birlikte kayar, kadraja sıkıştırılır */
export function Katman({ v, t }: { v: LottieBilgi; t: number }) {
  const [cx, cy, z] = kameraAn(v, t);
  const k = z / 100;
  const sik = (n: number, a: number, b: number) => Math.min(b, Math.max(a, n));
  // altta altyazı bölgesi (%76+) etiketlere kapalı; aynı anda görünen etiketler birbirine binmesin diye aşağı itilir
  const dolu: [number, number][] = [];
  const yer = (x: number, y: number) => {
    const l = sik((400 + (x - cx) * k) / 8, 12, 88);
    let tp = sik((250 + (y - cy) * k) / 5, 8, 72);
    for (let n = 0; n < 6 && dolu.some(([a, b]) => Math.abs(a - l) < 26 && Math.abs(b - tp) < 8); n++) tp = tp + 8 > 72 ? tp - 8 * (n + 1) : tp + 8;
    dolu.push([l, tp]);
    return { left: `${l}%`, top: `${sik(tp, 6, 72)}%` };
  };
  return (
    <div className="kmb-lv-katman" aria-hidden>
      {v.sayaclar.filter((s) => t >= s.bas).map((s, i) => {
        const f = Math.min(1, Math.max(0, (t - s.bas) / Math.max(0.01, s.son - s.bas)));
        return <span key={`s${i}`} className="kmb-lv-sayac" style={yer(s.x, s.y)}>{(s.v1 + (s.v2 - s.v1) * f).toFixed(s.ondalik)} {s.birim}</span>;
      })}
      {v.etiketler.filter((e) => t >= e.bas && t <= e.son).map((e, i) => (
        <span key={`${e.bas}-${i}`} className={`kmb-lv-etiket ${e.tur}`} style={yer(e.x, e.y)}>{e.metin}</span>
      ))}
    </div>
  );
}

export type SahneTutamac = { ciz: (sn: number) => void };

/** Lottie sahnesi (canvas): ekrana yaklaşınca kurulur, uzaklaşınca yok edilir. Kareyi React'ten bağımsız çizmek için
 *  `tutamac.ciz(sn)` her ekran yenilemesinde çağrılır (arayüz durumu 10 fps; animasyon 60 fps). `kare` ilk/durgun kare. */
export const LottieSahne = React.forwardRef<SahneTutamac, { ad: string; kare: number; onHazir?: () => void }>(function LottieSahne({ ad, kare, onHazir }, ref) {
  const kap = useRef<HTMLDivElement>(null);
  const anim = useRef<any>(null);
  const son = useRef(-1);
  const [gorunur, setGorunur] = useState(false);
  const ciz = useCallback((s: number) => {
    const a = anim.current;
    if (!a) return;
    const f = Math.max(0, Math.min(a.totalFrames - 1, Math.round(s * 30)));
    if (f !== son.current) { son.current = f; a.goToAndStop(f, true); }
  }, []);
  React.useImperativeHandle(ref, () => ({ ciz }), [ciz]);
  useEffect(() => {
    const el = kap.current;
    if (!el || typeof IntersectionObserver === 'undefined') { setGorunur(true); return; }
    const io = new IntersectionObserver(([e]) => setGorunur(e.isIntersecting), { rootMargin: '300px' });
    io.observe(el);
    return () => io.disconnect();
  }, []);
  useEffect(() => {
    if (!gorunur) return;
    let iptal = false;
    let ro: ResizeObserver | null = null;
    Promise.all([lottieOnYukle(ad), oynaticiYukle()]).then(([data, L]) => {
      if (iptal || !kap.current) return;
      anim.current = L.loadAnimation({ container: kap.current, renderer: 'canvas', loop: false, autoplay: false,
        animationData: JSON.parse(JSON.stringify(data)),
        rendererSettings: { preserveAspectRatio: 'xMidYMid meet', clearCanvas: true, progressiveLoad: false,
          // yüksek yoğunluklu ekranlarda 2'nin üstü gereksiz boyama yükü
          dpr: Math.min(2, window.devicePixelRatio || 1) } });
      anim.current.setSubframe(false);
      son.current = -1;
      anim.current.addEventListener('DOMLoaded', () => { ciz(kareRef.current); onHazir?.(); });
      ro = new ResizeObserver(() => anim.current?.resize());
      ro.observe(kap.current);
    });
    return () => { iptal = true; ro?.disconnect(); anim.current?.destroy(); anim.current = null; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ad, gorunur]);
  const kareRef = useRef(kare);
  kareRef.current = kare;
  useEffect(() => { ciz(kare); }, [kare, ciz]);
  return <div ref={kap} className="kmb-lv-lottie" />;
});

type Props = {
  ad: string; kod: string; ses: SesKayit | null;
  /** dış saat (sn): verilirse sessiz, denetimsiz çizer (ders videosu) */
  zaman?: number;
  kompakt?: boolean;
  /** açılınca kendiliğinden oynat */
  otomatik?: boolean;
  onBitti?: () => void;
  onZaman?: (t: number) => void;
  /** sonraki video (önceden yüklenir; bitince "Sıradaki" düğmesi) */
  sonraki?: { ad: string; baslik: string; git: () => void };
  /** kabı tamamen doldur (ders videosu tam ekran düzeni) */
  doldur?: boolean;
};

export default function LottieVideo({ ad, kod, ses, zaman, kompakt, otomatik, onBitti, onZaman, sonraki, doldur }: Props) {
  const v = LOTTILER.find((x) => x.ad === ad);
  const kap = useRef<HTMLDivElement>(null);
  const audio = useRef<HTMLAudioElement | null>(null);
  const saat = useRef({ bas: 0, t: 0 });
  const tRef = useRef(0);
  const sahne = useRef<SahneTutamac>(null);
  const bekliyor = useRef(false);
    const [t, setT] = useState(0);
  const [cal, setCal] = useState(false);
  const [hiz, setHiz] = useState(1);
  const [altyazi, setAltyazi] = useState(true);
  const [tam, setTam] = useState(false);
  const [sahte, setSahte] = useState(false);
  const [gizli, setGizli] = useState(false);
  const [bitti, setBitti] = useState(false);
  const [atlama, setAtlama] = useState<'' | 'geri' | 'ileri'>('');
  const klip = v ? ses?.[klipAdi(v)] : undefined;
  const dis = zaman !== undefined;
  const sure = v?.sure || 1;

  const git = useCallback((s: number) => {
    const y = Math.max(0, Math.min(sure, s));
    saat.current = { bas: performance.now(), t: y };
    tRef.current = y;
    setT(y);
    setBitti(false);
  }, [sure]);
  // tam ekranda denetimler 2,5 sn hareketsizlikten sonra gizlenir
  const uyandir = useCallback(() => {
    setGizli(false);
    window.clearTimeout((uyandir as any)._z);
    (uyandir as any)._z = window.setTimeout(() => setGizli(true), 2500);
  }, []);
  const durdur = useCallback(() => { audio.current?.pause(); setCal(false); }, []);
  const oynat = useCallback((bas?: number) => {
    window.dispatchEvent(new CustomEvent(KMB_DURDUR, { detail: ad }));
    const s = bas ?? (tRef.current >= sure - 0.1 ? 0 : tRef.current);
    if (klip && v && !audio.current) {
      const url = klipUrl(kod, v, klip.h);
      const a = new Audio();
      a.preload = 'auto';
      audio.current = a;
      sesOnYukle(url).then((u) => { if (audio.current === a && !a.src) a.src = u; });
    }
    saat.current = { bas: performance.now(), t: s };
    tRef.current = s;
    setBitti(false);
    setCal(true);
    uyandir(); // oynatma başlayınca da gizlenme sayacı işler
  }, [sure, klip, kod, ad, v, uyandir]);

  // oynatma döngüsü: saat video saatidir. Ses bölüm içinde ses saatine eşlenir; bekleme payında durur, sonraki bölümde
  // kaldığı yerden sürer (yakınsa konumlanmaz). Sapma küçükse saat yumuşakça sese çekilir (zıplama yok), ses tamponlanırken
  // görüntü bekler (ses görüntünün gerisinde kalmaz), yalnız büyük sapmada ses konumlanır (blob olduğu için anında).
  useEffect(() => {
    if (!cal || dis) return;
    let id = 0, son = 0, onceki = performance.now();
    const adim = (now: number) => {
      let s = saat.current.t + ((now - saat.current.bas) / 1000) * hiz;
      const a = audio.current;
      if (a && klip && v) {
        const b = v.bolumler.find((x) => x.ses_bas !== undefined && s >= x.bas - 0.05 && s < x.son + 0.15);
        if (b && b.ses_bas !== undefined) {
          const hedef = b.ses_bas + (s - b.bas);
          if (!a.src) {
            // ses henüz inmedi: görüntü beklesin
            s = tRef.current; saat.current = { bas: now, t: s };
          } else if (a.paused) {
            if (!bekliyor.current && hedef < klip.sure) {
              bekliyor.current = true;
              a.playbackRate = hiz;
              if (Math.abs(a.currentTime - hedef) > 0.3) a.currentTime = Math.max(0, hedef);
              a.play().catch(() => { /* görüntü iç saatle sürer */ }).finally(() => { bekliyor.current = false; });
            }
          } else if (a.readyState < 3 || a.seeking) {
            s = tRef.current; saat.current = { bas: now, t: s };
          } else {
            const fark = b.bas + (a.currentTime - b.ses_bas) - s;
            if (Math.abs(fark) > 0.6) a.currentTime = Math.max(0, hedef);
            else if (Math.abs(fark) > 0.03) { s += fark * Math.min(1, (now - onceki) / 250); saat.current = { bas: now, t: s }; }
          }
        } else if (!a.paused) a.pause();
      }
      onceki = now;
      if (s >= sure) {
        s = sure; a?.pause(); tRef.current = s; setT(s); setCal(false); setBitti(true); onBitti?.();
        return;
      }
      tRef.current = s;
      sahne.current?.ciz(s); // her ekran yenilemesinde kare (React'ten bağımsız)
      if (now - son > 100) { setT(s); onZaman?.(s); son = now; }
      id = requestAnimationFrame(adim);
    };
    id = requestAnimationFrame(adim);
    return () => { cancelAnimationFrame(id); audio.current?.pause(); };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [cal, dis, klip, hiz, sure, v]);

  // açılışta sesi önceden indir (ilk oynatmada bekleme olmasın); sonraki videonun sesi de
  useEffect(() => { if (klip && v && !dis) sesOnYukle(klipUrl(kod, v, klip.h)).catch(() => {}); }, [klip, v, kod, dis]);
  useEffect(() => { if (dis) setT((zaman as number) % sure); }, [dis, zaman, sure]);
  useEffect(() => {
    if (!sonraki) return;
    lottieOnYukle(sonraki.ad).catch(() => {});
    const sv = LOTTILER.find((x) => x.ad === sonraki.ad);
    const sk = sv && ses?.[klipAdi(sv)];
    if (sv && sk) sesOnYukle(klipUrl(kod, sv, sk.h)).catch(() => {});
  }, [sonraki, ses, kod]);
  useEffect(() => { if (otomatik && !dis) oynat(0); /* eslint-disable-next-line react-hooks/exhaustive-deps */ }, [ad]);
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

  const tamMi = tam || sahte;
  const tamEkran = () => {
    if (tamMi) {
      if (document.fullscreenElement) document.exitFullscreen().catch(() => {});
      setSahte(false);
      return;
    }
    const el = kap.current as any;
    if (el?.requestFullscreen) el.requestFullscreen().catch(() => setSahte(true));
    else setSahte(true); // iOS Safari: öğe tam ekranı yok → pencereyi kaplayan katman
    try { (screen.orientation as any)?.lock?.('landscape').catch(() => {}); } catch { /* yönlendirme kilidi yoksa geç */ }
  };
  const atla = (yon: 1 | -1) => {
    git(tRef.current + yon * ATLA);
    setAtlama(yon > 0 ? 'ileri' : 'geri');
    window.setTimeout(() => setAtlama(''), 500);
    if (cal) saat.current = { bas: performance.now(), t: tRef.current };
  };
  const tus = (e: React.KeyboardEvent) => {
    uyandir();
    if (e.key === ' ' || e.key === 'k') { e.preventDefault(); if (cal) durdur(); else oynat(); }
    else if (e.key === 'ArrowRight') atla(1);
    else if (e.key === 'ArrowLeft') atla(-1);
    else if (e.key === 'f') tamEkran();
    else if (e.key === 'c') setAltyazi((x) => !x);
    else if (e.key === 'Escape' && sahte) setSahte(false);
  };

  if (!v) return null;
  const bi = bolumAn(v, t);
  const bolum = v.bolumler[bi];
  const konusuyor = bolum && t >= bolum.bas - 0.2 && t <= bolum.son + 0.3;

  if (dis) {
    return (
      <div className="kmb-lv kmb-lv-dis">
        <div className="kmb-lv-sahne"><LottieSahne ad={ad} kare={t} /><Katman v={v} t={t} /></div>
      </div>
    );
  }
  const yuzde = (t / sure) * 100;
  return (
    <div ref={kap} className={`kmb-lv${tamMi ? ' tam' : ''}${sahte ? ' sahte' : ''}${kompakt ? ' kompakt' : ''}${doldur ? ' doldur' : ''}${gizli && cal ? ' gizli' : ''}${cal ? ' calan' : ''}`}
      tabIndex={0} onKeyDown={tus} onMouseMove={uyandir} onTouchStart={uyandir} aria-label={`Video: ${v.baslik}`}>
      <div className="kmb-lv-sahne">
        {/* durgun ve başta: ilk bölümün bir karesi kapak olarak (boş sahne görünmesin) */}
        <LottieSahne ref={sahne} ad={ad} kare={!cal && t < 0.05 ? Math.min(sure, (v.bolumler[0]?.bas ?? 0) + 1.2) : t} />
        <Katman v={v} t={t} />
        {/* dokunma alanları: sol 10 sn geri, orta oynat/duraklat, sağ 10 sn ileri (yazısız; geri bildirim yalnız dokununca) */}
        <button className="kmb-lv-alan sol" aria-label="10 saniye geri" onClick={() => atla(-1)} />
        <button className="kmb-lv-alan orta" aria-label={cal ? 'Duraklat' : 'Oynat'} onClick={() => (cal ? durdur() : oynat())} />
        <button className="kmb-lv-alan sag" aria-label="10 saniye ileri" onClick={() => atla(1)} />
        {atlama && <span className={`kmb-lv-atlama ${atlama}`}>{atlama === 'ileri' ? '+10 sn' : '−10 sn'}</span>}
        {!cal && !bitti && <span className="kmb-lv-buyuk-oynat" aria-hidden><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z" /></svg></span>}
        {altyazi && bolum?.metin && <div className={`kmb-lv-altyazi${konusuyor ? '' : ' sessiz'}`} aria-live="polite"><span>{bolum.metin}</span></div>}
        {bitti && (
          <div className="kmb-lv-son">
            <button onClick={() => oynat(0)}>↺ Yeniden izle</button>
            {sonraki && <button className="ana" onClick={sonraki.git}>Sıradaki: {sonraki.baslik} ›</button>}
          </div>
        )}
        {tamMi && !doldur && <div className="kmb-lv-ust"><b>{v.baslik}</b><button onClick={tamEkran} aria-label="Tam ekrandan çık">✕</button></div>}
      </div>
      <div className="kmb-lv-cubuk">
        <div className="kmb-lv-zaman">
          <div className="kmb-lv-iz">
            <div className="kmb-lv-dolu" style={{ width: `${yuzde}%` }} />
            {v.bolumler.slice(1).map((b, i) => <span key={i} className="kmb-lv-bolum-isaret" style={{ left: `${(b.bas / sure) * 100}%` }} />)}
          </div>
          <span className="kmb-lv-tutamac" style={{ left: `${yuzde}%` }} />
          <input type="range" min={0} max={sure} step={0.1} value={t} aria-label="Zaman" onChange={(e) => { git(Number(e.target.value)); if (cal) saat.current = { bas: performance.now(), t: Number(e.target.value) }; }} />
        </div>
        <div className="kmb-lv-dugmeler">
          <button onClick={() => (cal ? durdur() : oynat())} aria-label={cal ? 'Duraklat' : 'Oynat'}>
            <svg viewBox="0 0 24 24">{cal ? <path d="M7 5h3.5v14H7zM13.5 5H17v14h-3.5z" /> : <path d="M8 5v14l11-7z" />}</svg>
          </button>
          <span className="kmb-lv-sure">{sn(t)} / {sn(sure)}</span>
          <span className="kmb-lv-baslik">{bolum ? `${bi + 1}/${v.bolumler.length} · ${bolum.baslik}` : ''}</span>
          <button className="kmb-lv-hiz" onClick={() => setHiz((h) => [1, 1.25, 1.5, 0.75][([1, 1.25, 1.5, 0.75].indexOf(h) + 1) % 4])} aria-label="Oynatma hızı">{hiz}×</button>
          <button className={altyazi ? 'etkin' : ''} onClick={() => setAltyazi((x) => !x)} aria-label="Altyazı" aria-pressed={altyazi}>CC</button>
          <button onClick={tamEkran} aria-label={tamMi ? 'Tam ekrandan çık' : 'Tam ekran'}>
            <svg viewBox="0 0 24 24">{tamMi ? <path d="M9 4v5H4v2h7V4zM15 4h-2v7h7V9h-5zM4 15h5v5h2v-7H4zM13 13v7h2v-5h5v-2z" /> : <path d="M4 4h7v2H6v5H4zM13 4h7v7h-2V6h-5zM4 13h2v5h5v2H4zM18 13h2v7h-7v-2h5z" />}</svg>
          </button>
        </div>
      </div>
    </div>
  );
}
