/**
 * KMB Lottie videosu — etkileşimli oynatıcı. Denetimler görüntünün üstünde yüzer, oynarken 3 sn sonra gizlenir (altta ince
 * ilerleme çizgisi kalır). Jestler (H461): DOKUNMATİK tek dokunuş yalnız denetimleri gösterir/gizler (oynatmayı ellemez);
 * kenarda çift dokunuş ±10 sn, ardından aynı kenara her dokunuş +10 (toplam görünür); ortada çift dokunuş oynat/duraklat;
 * basılı tutma 2× hız; yana kaydırma sarar (hedef süre + cümle görünür). FARE tık oynat/duraklat, çift tık tam ekran.
 * Orta düğmeler (−10 · oynat · +10), cümle listesi menüsü, hız menüsü, zaman çubuğu cümle parçalı + üzerinde önizleme.
 * Bitişte iptal edilebilir geri sayım (`otoSonraki`; `bekle` soru yanıtlanana dek durdurur). `ref.bolumeGit(i)` cümleye atlar.
 * Klavye: boşluk/k, ←/→ ya da j/l 10 sn, ↑/↓ cümle, 0–9 yüzde, f tam ekran, c altyazı.
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
import LINDEX2 from '../../data/kmb/lottie2b/index.json';
import AINDEX2 from '../../data/kmb/lottie2b/adimlar.json';

export type LottieBilgi = {
  ad: string; baslik: string; sure: number; sesli?: boolean;
  bolumler: { baslik: string; metin: string; bas: number; son: number; ses_bas?: number }[];
  kamera?: [number, number, number, number][];
  etiketler: { bas: number; son: number; x: number; y: number; metin: string; tur: string }[];
  sayaclar: { bas: number; son: number; v1: number; v2: number; birim: string; x: number; y: number; ondalik: number }[];
  adim?: string;
};
type SesKayit = Record<string, { h: string; sure: number; zaman: [number, number][] }>;

/** Lottie sürümü (2026-11-01): 2B düz çizgi film hattı `lottie2b/` (scripts/kmb/lottie2b) varsayılan; eski gerçekçi hat
 *  `lottie/` korunur ve `localStorage.medsoru_kmb_lottie_eski='1'` ile (karşılaştırma) seçilir. Aynı ad için 2B dosyası yoksa eskisi. */
export const ESKI_TERCIH = 'medsoru_kmb_lottie_eski';
export const eskiLottie = () => { try { return localStorage.getItem(ESKI_TERCIH) === '1'; } catch { return false; } };
const VERI1 = import.meta.glob(['../../data/kmb/lottie/*.json', '!../../data/kmb/lottie/index.json', '!../../data/kmb/lottie/adimlar.json']);
const VERI2 = import.meta.glob(['../../data/kmb/lottie2b/*.json', '!../../data/kmb/lottie2b/index.json', '!../../data/kmb/lottie2b/adimlar.json']);
const ikiB = (ad: string) => !eskiLottie() && !!VERI2[`../../data/kmb/lottie2b/${ad}.json`];
/** Konu videoları (lottie_uret.py) + adım videoları (adim_lottie.py: her cümle bir bölüm, ses `o-<adım>`); 2B kaydı eskinin yerine geçer */
const ESKI = [...(LINDEX as unknown as LottieBilgi[]), ...(AINDEX as unknown as LottieBilgi[])];
const YENI = [...(LINDEX2 as unknown as LottieBilgi[]), ...(AINDEX2 as unknown as LottieBilgi[])];
export const LOTTILER: LottieBilgi[] = ESKI.map((v) => (ikiB(v.ad) && YENI.find((y) => y.ad === v.ad)) || v);
export const klipAdi = (v: LottieBilgi) => (v.adim ? `o-${v.adim}` : `l-${v.ad}`);
export const sn = (t: number) => `${Math.floor(t / 60)}:${String(Math.floor(t % 60)).padStart(2, '0')}`;
export const KMB_DURDUR = 'kmb-durdur';
const ATLA = 10;

const ONBELLEK = new Map<string, Promise<any>>();
/** Lottie JSON'unu önbelleğe al (sonraki videoyu önceden yüklemek için) */
export function lottieOnYukle(ad: string): Promise<any> {
  let p = ONBELLEK.get(ad);
  if (!p) {
    const y = ikiB(ad) ? VERI2[`../../data/kmb/lottie2b/${ad}.json`] : VERI1[`../../data/kmb/lottie/${ad}.json`];
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
  /** bitince bu kadar ms sonra sonrakine kendiliğinden geç (geri sayım görünür; yeniden izle/konumlama iptal eder) */
  otoSonraki?: number;
  /** bitişte geri sayım başlamasın (ör. adımın hızlı kontrol sorusu yanıtlanmadı); bitiş ekranında `bekleMetin` görünür */
  bekle?: boolean;
  bekleMetin?: string;
  /** kabı tamamen doldur (ders videosu tam ekran düzeni) */
  doldur?: boolean;
  /** denetimler açıldı/gizlendi (ders videosu üst şeridini aynı anda açıp kapatır) */
  onGoster?: (acik: boolean) => void;
};
export type VideoTutamac = { bolumeGit: (i: number) => void; oynat: () => void; durdur: () => void };

/** Altyazı ve hız tercihi cihazda/hesapta kalır (her videoda yeniden açılıp kapanmasın) */
const TERCIH = 'medsoru_kmb_oynatici_v1';
const tercihOku = (): { cc: boolean; hiz: number } => { try { return { cc: true, hiz: 1, ...JSON.parse(localStorage.getItem(TERCIH) || '{}') }; } catch { return { cc: true, hiz: 1 }; } };
const tercihYaz = (p: Partial<{ cc: boolean; hiz: number }>) => { try { localStorage.setItem(TERCIH, JSON.stringify({ ...tercihOku(), ...p })); } catch { /* özel pencere */ } };
const HIZLAR = [0.75, 1, 1.25, 1.5, 2];
/** Jest eşikleri: çift dokunuş aralığı, seri sarma penceresi, basılı tutma, kaydırma başlangıcı (px) */
const CIFT_MS = 280, SERI_MS = 700, UZUN_MS = 450, KAYMA_PX = 14;
const GIZLE_MS = 3000;
const JEST_IPUCU = 'medsoru_kmb_jest_ipucu_v1';

const Ikon = ({ d }: { d: string }) => <svg viewBox="0 0 24 24" aria-hidden><path d={d} /></svg>;
const I = {
  oynat: 'M8 5v14l11-7z', dur: 'M7 5h3.5v14H7zM13.5 5H17v14h-3.5z',
  onceki: 'M6 5h2v14H6zM20 5v14L9 12z', sonraki: 'M16 5h2v14h-2zM4 5v14l11-7z',
  geri10: 'M12 5V2L7 6l5 4V7a6 6 0 1 1-6 6H4a8 8 0 1 0 8-8z', ileri10: 'M12 5V2l5 4-5 4V7a6 6 0 1 0 6 6h2a8 8 0 1 1-8-8z',
  liste: 'M4 6h2v2H4zM8 6h12v2H8zM4 11h2v2H4zM8 11h12v2H8zM4 16h2v2H4zM8 16h12v2H8z',
  tam: 'M4 4h7v2H6v5H4zM13 4h7v7h-2V6h-5zM4 13h2v5h5v2H4zM18 13h2v7h-7v-2h5z',
  tamCik: 'M9 4v5H4v2h7V4zM15 4h-2v7h7V9h-5zM4 15h5v5h2v-7H4zM13 13v7h2v-5h5v-2z',
  kapat: 'M6.4 5 5 6.4 10.6 12 5 17.6 6.4 19l5.6-5.6 5.6 5.6 1.4-1.4-5.6-5.6L19 6.4 17.6 5 12 10.6z',
};

const LottieVideo = React.forwardRef<VideoTutamac, Props>(function LottieVideo({ ad, kod, ses, zaman, kompakt, otomatik, onBitti, onZaman, sonraki, otoSonraki, bekle, bekleMetin, doldur, onGoster }, ref) {
  const v = LOTTILER.find((x) => x.ad === ad);
  const kap = useRef<HTMLDivElement>(null);
  const sahneKap = useRef<HTMLDivElement>(null);
  const audio = useRef<HTMLAudioElement | null>(null);
  const saat = useRef({ bas: 0, t: 0 });
  const tRef = useRef(0);
  const sahne = useRef<SahneTutamac>(null);
  const bekliyor = useRef(false);
  const gizleZ = useRef(0);
  const [t, setT] = useState(0);
  const [cal, setCal] = useState(false);
  const [hiz, setHizS] = useState(() => tercihOku().hiz);
  const [hizli, setHizli] = useState(false); // basılı tutma: geçici 2×
  const [altyazi, setAltyaziS] = useState(() => tercihOku().cc);
  const [tam, setTam] = useState(false);
  const [sahte, setSahte] = useState(false);
  const [goster, setGoster] = useState(true); // denetimler (alt çubuk + orta düğmeler)
  const [menu, setMenu] = useState<'' | 'cumle' | 'hiz'>('');
  const [bitti, setBitti] = useState(false);
  const [otoIptal, setOtoIptal] = useState(false);
  const [atlama, setAtlama] = useState<{ yon: 1 | -1; sn: number; k: number } | null>(null);
  const [kayma, setKayma] = useState<number | null>(null); // yana kaydırarak sarma: hedef saniye
  const [ipucu, setIpucu] = useState<{ x: number; t: number } | null>(null); // zaman çubuğu önizlemesi
  const [isik, setIsik] = useState<'' | 'oynat' | 'dur'>(''); // fareyle tıklayınca ortada kısa simge
  const [jestIpucu, setJestIpucu] = useState(false); // dokunmatikte ilk oynatmada bir kez
  const klip = v ? ses?.[klipAdi(v)] : undefined;
  const dis = zaman !== undefined;
  const sure = v?.sure || 1;
  const etkinHiz = hizli ? 2 : hiz;
  // hız değişince saat yeniden tabanlanır (geçen süre yeni hızla yeniden hesaplanıp görüntü zıplamasın)
  const tabanla = () => { saat.current = { bas: performance.now(), t: tRef.current }; };
  const setHiz = (h: number) => { tabanla(); if (audio.current) audio.current.playbackRate = h; setHizS(h); tercihYaz({ hiz: h }); };
  const setAltyazi = (f: (x: boolean) => boolean) => setAltyaziS((x) => { const y = f(x); tercihYaz({ cc: y }); return y; });

  const git = useCallback((s: number) => {
    const y = Math.max(0, Math.min(sure, s));
    saat.current = { bas: performance.now(), t: y };
    tRef.current = y;
    setT(y);
    setBitti(false);
  }, [sure]);
  /** denetimleri göster; oynarken ve menü kapalıyken GIZLE_MS sonra gizle */
  const calRef = useRef(false);
  calRef.current = cal;
  const menuRef = useRef(menu);
  menuRef.current = menu;
  const gizlemeKur = useCallback(() => {
    window.clearTimeout(gizleZ.current);
    gizleZ.current = window.setTimeout(() => { if (calRef.current && !menuRef.current) setGoster(false); }, GIZLE_MS);
  }, []);
  const uyandir = useCallback(() => { setGoster(true); gizlemeKur(); }, [gizlemeKur]);
  useEffect(() => () => window.clearTimeout(gizleZ.current), []);
  const durdur = useCallback(() => { audio.current?.pause(); setCal(false); setGoster(true); }, []);
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
    setT(s);
    setBitti(false);
    setOtoIptal(false);
    setCal(true);
    gizlemeKur();
  }, [sure, klip, kod, ad, v, gizlemeKur]);
  const bolumeGit = useCallback((i: number) => {
    const b = v?.bolumler[Math.max(0, Math.min(i, (v?.bolumler.length || 1) - 1))];
    if (!b) return;
    // bölüm başından biraz önce: cümle kesilmeden, ses baştan duyulsun
    oynat(Math.max(0, b.bas - 0.05));
  }, [v, oynat]);
  React.useImperativeHandle(ref, () => ({ bolumeGit, oynat: () => oynat(), durdur }), [bolumeGit, oynat, durdur]);
  const degistir = () => (cal ? durdur() : oynat());
  useEffect(() => {
    if (!cal) return;
    try {
      if (localStorage.getItem(JEST_IPUCU) || !window.matchMedia('(hover: none)').matches) return;
      localStorage.setItem(JEST_IPUCU, '1');
    } catch { return; }
    setJestIpucu(true);
    const z = window.setTimeout(() => setJestIpucu(false), 6000);
    return () => window.clearTimeout(z);
  }, [cal]);

  // oynatma döngüsü: saat video saatidir. Ses bölüm içinde ses saatine eşlenir; bekleme payında durur, sonraki bölümde
  // kaldığı yerden sürer (yakınsa konumlanmaz). Sapma küçükse saat yumuşakça sese çekilir (zıplama yok), ses tamponlanırken
  // görüntü bekler (ses görüntünün gerisinde kalmaz), yalnız büyük sapmada ses konumlanır (blob olduğu için anında).
  useEffect(() => {
    if (!cal || dis) return;
    let id = 0, son = 0, onceki = performance.now();
    if (audio.current) audio.current.playbackRate = etkinHiz;
    const adim = (now: number) => {
      let s = saat.current.t + ((now - saat.current.bas) / 1000) * etkinHiz;
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
              a.playbackRate = etkinHiz;
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
        s = sure; a?.pause(); tRef.current = s; setT(s); setCal(false); setGoster(true); setBitti(true); onBitti?.();
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
  }, [cal, dis, klip, etkinHiz, sure, v]);
  // duraklatılmışken konum değişince dış dünyaya bildir (metin vurgusu konumu izlesin)
  useEffect(() => { if (!cal && !dis) onZaman?.(t); /* eslint-disable-next-line react-hooks/exhaustive-deps */ }, [t, cal, dis]);

  // bitince geri sayımla sıradakine geç; "Burada kal" ya da bekleyen soru durdurur (sarma iptal etmez: sarınca bitti düşer,
  // video yeniden biterse geri sayım yeniden başlar)
  const sonrakiRef = useRef(sonraki);
  sonrakiRef.current = sonraki;
  useEffect(() => {
    if (!bitti || otoIptal || bekle || otoSonraki === undefined || !sonrakiRef.current) return;
    const z = window.setTimeout(() => sonrakiRef.current?.git(), otoSonraki);
    return () => window.clearTimeout(z);
  }, [bitti, otoIptal, bekle, otoSonraki]);

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
  /** ±10 sn; seri dokunuşlarda toplam gösterilir (−10, −20 …) */
  const atla = (yon: 1 | -1) => {
    git(tRef.current + yon * ATLA);
    if (cal) saat.current = { bas: performance.now(), t: tRef.current };
    setAtlama((a) => ({ yon, sn: a && a.yon === yon ? a.sn + ATLA : ATLA, k: (a?.k || 0) + 1 }));
  };
  useEffect(() => { if (!atlama) return; const z = window.setTimeout(() => setAtlama(null), SERI_MS + 200); return () => window.clearTimeout(z); }, [atlama]);
  useEffect(() => { if (!isik) return; const z = window.setTimeout(() => setIsik(''), 500); return () => window.clearTimeout(z); }, [isik]);

  // ———— jest katmanı (pointer olayları; fare ve dokunmatik ayrı kurallar)
  //  Dokunmatik: tek dokunuş denetimleri göster/gizle · kenarda çift dokunuş ±10 sn (sonraki her dokunuş +10) ·
  //  ortada çift dokunuş oynat/duraklat · basılı tut 2× · yana kaydır sar.  Fare: tık oynat/duraklat · çift tık tam ekran.
  const j = useRef({ id: -1, x0: 0, y0: 0, t0: 0, tip: '', kayiyor: false, dikey: false, uzunZ: 0, uzun: false, tekZ: 0, sonDokunus: 0, sonBolge: '', seriSon: 0, seriYon: 0 as 0 | 1 | -1, sonTik: 0 });
  const bolge = (x: number) => {
    const r = sahneKap.current!.getBoundingClientRect();
    const f = (x - r.left) / r.width;
    return f < 0.35 ? 'sol' : f > 0.65 ? 'sag' : 'orta';
  };
  const jestBas = (e: React.PointerEvent) => {
    if (e.button !== 0 || dis) return;
    const g = j.current;
    Object.assign(g, { id: e.pointerId, x0: e.clientX, y0: e.clientY, t0: performance.now(), tip: e.pointerType, kayiyor: false, dikey: false, uzun: false });
    window.clearTimeout(g.uzunZ);
    if (cal) g.uzunZ = window.setTimeout(() => { g.uzun = true; tabanla(); setHizli(true); }, UZUN_MS);
  };
  const jestKay = (e: React.PointerEvent) => {
    const g = j.current;
    if (e.pointerId !== g.id) { if (e.pointerType === 'mouse') uyandir(); return; }
    const dx = e.clientX - g.x0, dy = e.clientY - g.y0;
    if (!g.kayiyor && !g.dikey && Math.hypot(dx, dy) > KAYMA_PX) {
      window.clearTimeout(g.uzunZ);
      if (Math.abs(dx) > Math.abs(dy) * 1.3 && g.tip !== 'mouse' && !g.uzun) { g.kayiyor = true; (e.target as Element).setPointerCapture?.(e.pointerId); }
      else g.dikey = true;
    }
    if (g.kayiyor) {
      // ekran genişliği = videonun en çok 90 sn'si (kısa videoda tüm süre); ince ayar parmağın altında kalır
      const w = sahneKap.current?.getBoundingClientRect().width || 1;
      setKayma(Math.max(0, Math.min(sure, tRef.current + (dx / w) * Math.min(sure, 90))));
      setGoster(true);
    }
  };
  const jestBit = (e: React.PointerEvent) => {
    const g = j.current;
    if (e.pointerId !== g.id) return;
    g.id = -1;
    window.clearTimeout(g.uzunZ);
    if (g.uzun) { g.uzun = false; tabanla(); setHizli(false); return; }
    if (g.kayiyor) { if (kayma !== null) { git(kayma); if (cal) saat.current = { bas: performance.now(), t: kayma }; } setKayma(null); gizlemeKur(); return; }
    if (g.dikey || e.type === 'pointercancel') return;
    const simdi = performance.now();
    const b = bolge(e.clientX);
    if (jestIpucu) setJestIpucu(false);
    if (g.tip === 'mouse') {
      // fare: tık oynat/duraklat; çift tık tam ekran (ilk tıkın oynat/duraklatı geri alınır)
      if (simdi - g.sonTik < CIFT_MS) { g.sonTik = 0; degistir(); tamEkran(); return; }
      g.sonTik = simdi;
      setIsik(cal ? 'dur' : 'oynat');
      degistir();
      uyandir();
      return;
    }
    // dokunmatik: seri sarma penceresindeyse aynı kenara her dokunuş yeniden sarar
    // yalnız aynı kenara: sağa sararken sola dokunmak tek başına geri sarmaz, çift dokunuş beklenir
    if (g.seriYon && simdi - g.seriSon < SERI_MS && b !== 'orta' && (b === 'sol' ? -1 : 1) === g.seriYon) {
      const yon = g.seriYon;
      window.clearTimeout(g.tekZ);
      atla(yon); g.seriSon = simdi; g.seriYon = yon;
      return;
    }
    if (simdi - g.sonDokunus < CIFT_MS && g.sonBolge === b) {
      window.clearTimeout(g.tekZ);
      g.sonDokunus = 0;
      if (b === 'orta') { degistir(); setIsik(cal ? 'dur' : 'oynat'); }
      else { const yon = b === 'sol' ? -1 : 1; atla(yon); g.seriSon = simdi; g.seriYon = yon; }
      return;
    }
    g.sonDokunus = simdi; g.sonBolge = b; g.seriYon = 0;
    window.clearTimeout(g.tekZ);
    // tek dokunuş: yalnız denetimler (çift dokunuş beklenir, sonra karar)
    g.tekZ = window.setTimeout(() => {
      setMenu('');
      setGoster((x) => { if (!x) gizlemeKur(); return !x; });
    }, CIFT_MS);
  };
  useEffect(() => () => { window.clearTimeout(j.current.tekZ); window.clearTimeout(j.current.uzunZ); }, []);

  // tek dokunuş durgunken de denetimleri gizleyebilir (temiz görüntü); menü açıkken ve bitişte hep açık
  const acik = goster || !!menu || bitti;
  useEffect(() => { onGoster?.(acik); /* eslint-disable-next-line react-hooks/exhaustive-deps */ }, [acik]);
  const bi = v ? bolumAn(v, t) : 0;
  const tus = (e: React.KeyboardEvent) => {
    if ((e.target as HTMLElement).closest('.kmb-lv-menu')) return;
    uyandir();
    const k = e.key;
    if (k === ' ' || k === 'k') { e.preventDefault(); degistir(); }
    else if (k === 'ArrowRight' || k === 'l') { e.preventDefault(); atla(1); }
    else if (k === 'ArrowLeft' || k === 'j') { e.preventDefault(); atla(-1); }
    else if (k === 'ArrowUp' || k === 'p') { e.preventDefault(); bolumeGit(bi - (t - (v?.bolumler[bi]?.bas ?? 0) > 1.5 ? 0 : 1)); }
    else if (k === 'ArrowDown' || k === 'n') { e.preventDefault(); bolumeGit(bi + 1); }
    else if (/^[0-9]$/.test(k)) { e.preventDefault(); git((Number(k) / 10) * sure); }
    else if (k === 'f') tamEkran();
    else if (k === 'c') setAltyazi((x) => !x);
    else if (k === 'Escape') { if (menu) setMenu(''); else if (sahte) setSahte(false); }
  };

  if (!v) return null;
  const bolum = v.bolumler[bi];
  const konusuyor = bolum && t >= bolum.bas - 0.2 && t <= bolum.son + 0.3;

  if (dis) {
    return (
      <div className="kmb-lv kmb-lv-dis">
        <div className="kmb-lv-sahne"><LottieSahne ad={ad} kare={t} /><Katman v={v} t={t} /></div>
      </div>
    );
  }
  const gt = kayma ?? t; // gösterilen zaman (kaydırırken hedef)
  const yuzde = (gt / sure) * 100;
  const geriSay = bitti && !otoIptal && !bekle && otoSonraki !== undefined && !!sonraki;
  const onceki = () => bolumeGit(bi - (t - (bolum?.bas ?? 0) > 1.5 ? 0 : 1));
  const ipBolum = ipucu ? v.bolumler[bolumAn(v, ipucu.t)] : undefined;
  return (
    <div ref={kap} className={`kmb-lv${tamMi ? ' tam' : ''}${sahte ? ' sahte' : ''}${kompakt ? ' kompakt' : ''}${doldur ? ' doldur' : ''}${acik ? '' : ' gizli'}${cal ? ' calan' : ''}`}
      tabIndex={0} onKeyDown={tus} aria-label={`Video: ${v.baslik}`} onMouseLeave={() => { setIpucu(null); if (cal && !menu) setGoster(false); }}>
      <div className="kmb-lv-sahne" ref={sahneKap}>
        {/* durgun ve başta: ilk bölümün bir karesi kapak olarak (boş sahne görünmesin) */}
        <LottieSahne ref={sahne} ad={ad} kare={kayma ?? (!cal && t < 0.05 ? Math.min(sure, (v.bolumler[0]?.bas ?? 0) + 1.2) : t)} />
        <Katman v={v} t={kayma ?? t} />
        {/* jest katmanı: dokunma/tıklama kuralları yukarıda; klavye ve ekran okuyucu için alttaki gerçek düğmeler */}
        <div className="kmb-lv-jest" aria-hidden onPointerDown={jestBas} onPointerMove={jestKay} onPointerUp={jestBit} onPointerCancel={jestBit}
          onContextMenu={(e) => e.preventDefault()} />
        {atlama && <span key={atlama.k} className={`kmb-lv-atlama ${atlama.yon > 0 ? 'ileri' : 'geri'}`} aria-live="polite">
          <Ikon d={atlama.yon > 0 ? I.ileri10 : I.geri10} />{atlama.yon > 0 ? '+' : '−'}{atlama.sn} sn</span>}
        {hizli && <span className="kmb-lv-rozet">2× ▸▸</span>}
        {jestIpucu && (
          <button className="kmb-lv-jest-ipucu" onClick={() => setJestIpucu(false)}>
            <span><b>Dokun</b> denetimleri aç/kapat</span><span><b>Kenara çift dokun</b> ±10 sn</span><span><b>Basılı tut</b> 2× hız</span><span><b>Yana kaydır</b> sar</span>
          </button>
        )}
        {kayma !== null && <span className="kmb-lv-kayma"><b>{sn(kayma)}</b> / {sn(sure)}<small>{(kayma - t >= 0 ? '+' : '−') + Math.abs(Math.round(kayma - t))} sn · Cümle {bolumAn(v, kayma) + 1}</small></span>}
        {isik && <span className="kmb-lv-isik" aria-hidden><Ikon d={isik === 'oynat' ? I.oynat : I.dur} /></span>}
        {/* orta düğmeler: denetimler açıkken (ya da durgunken) — açıkça görülebilen ±10 ve oynat/duraklat */}
        {!bitti && kayma === null && acik && (
          <div className={`kmb-lv-orta${cal ? '' : ' durgun'}`}>
            {/* yanlarda ±10 değil cümle düğmeleri: kenar bölgeleri yalnız çift dokunuşla sarar, tek dokunuş sarmaz (H461) */}
            <button className="yan" onClick={() => { onceki(); gizlemeKur(); }} aria-label="Önceki cümle"><Ikon d={I.onceki} /></button>
            <button className="ana" onClick={() => { degistir(); }} aria-label={cal ? 'Duraklat' : 'Oynat'}><Ikon d={cal ? I.dur : I.oynat} /></button>
            <button className="yan" onClick={() => { bolumeGit(bi + 1); gizlemeKur(); }} disabled={bi >= v.bolumler.length - 1} aria-label="Sonraki cümle"><Ikon d={I.sonraki} /></button>
          </div>
        )}
        {altyazi && bolum?.metin && <div className={`kmb-lv-altyazi${konusuyor ? '' : ' sessiz'}`} aria-live="polite"><span>{bolum.metin}</span></div>}
        {bitti && (
          <div className="kmb-lv-son">
            {bekle && bekleMetin && <p className="kmb-lv-son-bas">{bekleMetin}</p>}
            {sonraki && !bekle && <p className="kmb-lv-son-bas">{geriSay ? 'Sıradaki birazdan başlıyor' : 'Sıradaki'}</p>}
            {sonraki && <button className={`ana${geriSay ? ' geri-say' : ''}`} style={geriSay ? { ['--kmb-gs' as string]: `${otoSonraki}ms` } : undefined} onClick={sonraki.git}>{sonraki.baslik} ›</button>}
            <div className="kmb-lv-son-alt">
              <button onClick={() => oynat(0)}>↺ Yeniden izle</button>
              {geriSay && <button onClick={() => setOtoIptal(true)}>Burada kal</button>}
            </div>
          </div>
        )}
        {tamMi && !doldur && <div className="kmb-lv-ust"><b>{v.baslik}</b><button onClick={tamEkran} aria-label="Tam ekrandan çık"><Ikon d={I.kapat} /></button></div>}
        {menu === 'cumle' && (
          <div className="kmb-lv-menu" role="dialog" aria-label="Cümleler">
            <div className="bas"><b>Cümleler</b><button onClick={() => setMenu('')} aria-label="Kapat"><Ikon d={I.kapat} /></button></div>
            <ol>
              {v.bolumler.map((b, i) => (
                <li key={i}><button className={i === bi ? 'etkin' : ''} aria-current={i === bi ? 'true' : undefined} onClick={() => { setMenu(''); bolumeGit(i); }}>
                  <span className="z">{sn(b.bas)}</span><span>{b.metin || b.baslik}</span></button></li>
              ))}
            </ol>
          </div>
        )}
        {menu === 'hiz' && (
          <div className="kmb-lv-menu kucuk" role="dialog" aria-label="Oynatma hızı">
            <div className="bas"><b>Hız</b><button onClick={() => setMenu('')} aria-label="Kapat"><Ikon d={I.kapat} /></button></div>
            <ol>
              {HIZLAR.map((h) => <li key={h}><button className={h === hiz ? 'etkin' : ''} aria-pressed={h === hiz} onClick={() => { setHiz(h); setMenu(''); gizlemeKur(); }}>{h === 1 ? 'Normal' : `${h}×`}</button></li>)}
            </ol>
          </div>
        )}
        {/* denetimler gizliyken yalnız ince ilerleme çizgisi */}
        <div className="kmb-lv-ince" aria-hidden><i style={{ width: `${yuzde}%` }} /></div>
      </div>
      <div className="kmb-lv-cubuk" onPointerMove={(e) => { if (e.pointerType === 'mouse') uyandir(); }}>
        <div className="kmb-lv-zaman"
          onPointerMove={(e) => { const r = e.currentTarget.getBoundingClientRect(); const f = Math.max(0, Math.min(1, (e.clientX - r.left) / r.width)); setIpucu({ x: f * 100, t: f * sure }); }}
          onPointerLeave={() => setIpucu(null)}>
          <div className="kmb-lv-iz">
            {v.bolumler.map((b, i) => {
              const s1 = (b.bas / sure) * 100, s2 = ((v.bolumler[i + 1]?.bas ?? sure) / sure) * 100;
              const dolu = Math.max(0, Math.min(1, (gt - b.bas) / Math.max(0.01, (v.bolumler[i + 1]?.bas ?? sure) - b.bas)));
              return <span key={i} className={`kmb-lv-parca${i === bi ? ' etkin' : ''}`} style={{ left: `${i === 0 ? 0 : s1}%`, width: `${s2 - (i === 0 ? 0 : s1)}%` }}><i style={{ width: `${dolu * 100}%` }} /></span>;
            })}
          </div>
          <span className="kmb-lv-tutamac" style={{ left: `${yuzde}%` }} />
          {ipucu && (
            <span className="kmb-lv-onizle" style={{ left: `clamp(70px, ${ipucu.x}%, calc(100% - 70px))` }}>
              <b>{sn(ipucu.t)}</b>{ipBolum && <small>{ipBolum.metin || ipBolum.baslik}</small>}
            </span>
          )}
          <input type="range" min={0} max={sure} step={0.1} value={gt} aria-label="Zaman" aria-valuetext={`${sn(t)} / ${sn(sure)}, cümle ${bi + 1}`}
            onChange={(e) => { git(Number(e.target.value)); uyandir(); if (cal) saat.current = { bas: performance.now(), t: Number(e.target.value) }; }} />
        </div>
        <div className="kmb-lv-dugmeler">
          <button className="kmb-lv-bol" onClick={onceki} aria-label="Cümlenin başına / önceki cümle" title="Önceki cümle (↑)"><Ikon d={I.onceki} /></button>
          <button onClick={degistir} aria-label={cal ? 'Duraklat' : 'Oynat'} title={cal ? 'Duraklat (boşluk)' : 'Oynat (boşluk)'}><Ikon d={cal ? I.dur : I.oynat} /></button>
          <button className="kmb-lv-bol" onClick={() => bolumeGit(bi + 1)} disabled={bi >= v.bolumler.length - 1} aria-label="Sonraki cümle" title="Sonraki cümle (↓)"><Ikon d={I.sonraki} /></button>
          <span className="kmb-lv-sure">{sn(gt)} / {sn(sure)}</span>
          <span className="kmb-lv-baslik">{bolum ? `Cümle ${bi + 1}/${v.bolumler.length}` : ''}</span>
          <button className={menu === 'cumle' ? 'etkin' : ''} onClick={() => { setMenu((m) => (m === 'cumle' ? '' : 'cumle')); setGoster(true); }} aria-label="Cümle listesi" aria-expanded={menu === 'cumle'} title="Cümleler"><Ikon d={I.liste} /></button>
          <button className="kmb-lv-hiz" onClick={() => { setMenu((m) => (m === 'hiz' ? '' : 'hiz')); setGoster(true); }} aria-label={`Oynatma hızı ${hiz}×`} aria-expanded={menu === 'hiz'}>{hiz}×</button>
          <button className={altyazi ? 'etkin' : ''} onClick={() => setAltyazi((x) => !x)} aria-label="Altyazı" aria-pressed={altyazi} title="Altyazı (c)">CC</button>
          <button onClick={tamEkran} aria-label={tamMi ? 'Tam ekrandan çık' : 'Tam ekran'} title="Tam ekran (f)"><Ikon d={tamMi ? I.tamCik : I.tam} /></button>
        </div>
      </div>
    </div>
  );
});
export default LottieVideo;
