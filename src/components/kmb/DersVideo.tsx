/**
 * KMB ders videosu — dersin tamamı tam ekranda bir video gibi akar. Ekranda her an TEK görsel vardır: o cümlede anlatılan
 * yapının bulunduğu sahne (cümlenin eylem kimliklerinden seçilir; `gorsel` alanı elle belirler). Kamera vurgulanan yapıya
 * yumuşakça yaklaşır. Her adımın anlatımından sonra o adımın sesli Lottie gösterimi oynar (aşama aşama: önce anlat, sonra
 * göster). Adım başında başlık kartı, altta altyazı. Ses: `o-<adım>` ve `l-<video>` (EMA); saat tek, ses ona eşlenir.
 */
import React, { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import { getCustomApiUrl } from '../../services/api';
import { SAHNELER, SAHNE_OGELERI, SahneCiz, type SahneDurum } from './sahneler';
import { uygula } from './eylem';
import LottieVideo, { KMB_DURDUR, LOTTILER, klipAdi, sesZamani, type LottieBilgi } from './LottieVideo';
import type { Adim, Ders, SesKayit } from './KmbAsistan';

const sn = (t: number) => `${Math.floor(t / 60)}:${String(Math.floor(t % 60)).padStart(2, '0')}`;
const ARA = 0.9;
const KART = 1.6; // başlık kartı süresi (adımın başında, ses bundan sonra başlar)

type Parca =
  | { tur: 'adim'; ai: number; bas: number; sure: number; zaman: [number, number][]; klip?: { h: string; sure: number } }
  | { tur: 'lottie'; ai: number; bas: number; sure: number; v: LottieBilgi; klip?: { h: string; sure: number } };

/** Cümle için görsel: eylem kimliklerinin en çok düştüğü sahne; yoksa bir önceki */
function gorselSec(a: Adim, ci: number): string {
  const sahneler = [a.sahne, ...(a.ek || []).filter((e) => !e.startsWith('lottie:'))];
  let onceki = a.sahne;
  for (let i = 0; i <= ci; i++) {
    const c = a.cumleler[i] as Adim['cumleler'][number] & { gorsel?: string };
    if (c.gorsel) { onceki = c.gorsel; continue; }
    const say = sahneler.map((s) => (c.eylem || []).filter((e) => SAHNE_OGELERI[s]?.includes(e.id)).length);
    const m = Math.max(...say);
    if (m > 0) onceki = sahneler[say.indexOf(m)];
  }
  return onceki;
}

/** Kamera: cümlenin ilk görünür hedefine yakınlaş (Ken Burns); hedef yoksa tüm sahne */
function KameraSahne({ sahne, durum, hedef }: { sahne: string; durum: SahneDurum; hedef?: string }) {
  const kap = useRef<HTMLDivElement>(null);
  const [tf, setTf] = useState('scale(1)');
  useLayoutEffect(() => {
    const svg = kap.current?.querySelector('svg') as SVGSVGElement | null;
    const el = hedef ? svg?.querySelector(`[data-id="${hedef}"]`) as SVGGraphicsElement | null : null;
    if (!el) { setTf('translate(0,0) scale(1)'); return; }
    let b: DOMRect;
    try { b = el.getBBox() as DOMRect; } catch { return; }
    if (!b.width && !b.height) { setTf('translate(0,0) scale(1)'); return; }
    const z = Math.max(1, Math.min(1.9, 0.55 * Math.min(800 / Math.max(b.width, 40), 500 / Math.max(b.height, 40))));
    const cx = b.x + b.width / 2, cy = b.y + b.height / 2;
    // görünür alanın taşmaması için merkez sınırlanır
    const mx = Math.min(800 - 400 / z, Math.max(400 / z, cx)), my = Math.min(500 - 250 / z, Math.max(250 / z, cy));
    setTf(`translate(${((400 - mx * z) / 800) * 100}%, ${((250 - my * z) / 500) * 100}%) scale(${z})`);
  }, [sahne, hedef]);
  return (
    <div ref={kap} className="kmb-dv-kamera" style={{ transform: tf }}>
      <SahneCiz sahne={sahne} durum={durum} />
    </div>
  );
}

export default function DersVideo({ ders, ses, bas = 0, onKapat }: { ders: Ders; ses: SesKayit | null; bas?: number; onKapat: () => void }) {
  const kap = useRef<HTMLDivElement>(null);
  const audio = useRef<HTMLAudioElement | null>(null);
  const saat = useRef({ bas: 0, t: 0 });

  const plan = useMemo(() => {
    let t = 0;
    const P: Parca[] = [];
    ders.adimlar.forEach((a, ai) => {
      const k = ses?.[`o-${a.id}`];
      const av = LOTTILER.find((x) => x.adim === a.id);
      if (av) {
        P.push({ tur: 'lottie', ai, bas: t, sure: av.sure + KART, v: av, klip: k });
        t += av.sure + KART + ARA;
        return;
      }
      const zaman = (k?.zaman ?? (() => { let x = 0; return a.cumleler.map((c) => { const b = x; x += c.metin.length / 14 + 0.45; return [b, x - 0.45] as [number, number]; }); })())
        .map(([x, y]) => [x + KART, y + KART] as [number, number]);
      const sure = (k?.sure ?? zaman[zaman.length - 1][1] - KART) + KART;
      P.push({ tur: 'adim', ai, bas: t, sure, zaman, klip: k });
      t += sure + ARA;
    });
    return P;
  }, [ders, ses]);
  const toplam = plan.length ? plan[plan.length - 1].bas + plan[plan.length - 1].sure : 1;
  const ilk = plan.findIndex((p) => p.ai === bas);
  const [T, setT] = useState(plan[Math.max(0, ilk)]?.bas ?? 0);
  const [cal, setCal] = useState(false);
  const [hiz, setHiz] = useState(1);
  const [altyazi, setAltyazi] = useState(true);

  const pi = Math.max(0, plan.findIndex((p, i) => T < (plan[i + 1]?.bas ?? Infinity)));
  const P = plan[pi];
  const lt = T - P.bas;
  const adim = ders.adimlar[P.ai];

  // bu parçada sesin nerede olması gerektiği (null = sessiz an)
  const sesHedef = useCallback((p: Parca, t: number): number | null => {
    if (!p.klip) return null;
    if (p.tur === 'adim') { const x = t - KART; return x >= 0 && x < p.klip.sure ? x : null; }
    const x = t - KART;
    if (x < 0) return null;
    const s = sesZamani(p.v, x);
    return s !== null && s < p.klip.sure ? s : null;
  }, []);
  const klipUrl = (p: Parca) => `${getCustomApiUrl() || ''}/api/cozucu-ses/kmb/ema/${ders.kod}/${p.tur === 'adim' ? `o-${ders.adimlar[p.ai].id}` : klipAdi(p.v)}.mp3?v=${p.klip?.h}`;

  const git = useCallback((t: number) => {
    const y = Math.max(0, Math.min(toplam, t));
    saat.current = { bas: performance.now(), t: y };
    setT(y);
  }, [toplam]);
  const oynat = useCallback(() => {
    window.dispatchEvent(new CustomEvent(KMB_DURDUR, { detail: 'ders-video' }));
    saat.current = { bas: performance.now(), t: T >= toplam - 0.1 ? 0 : T };
    setCal(true);
  }, [T, toplam]);
  const durdur = useCallback(() => { audio.current?.pause(); setCal(false); }, []);

  useEffect(() => {
    if (!cal) return;
    let id = 0, son = 0;
    const a = audio.current || (audio.current = new Audio());
    const adimla = (now: number) => {
      const t = saat.current.t + ((now - saat.current.bas) / 1000) * hiz;
      if (t >= toplam) { a.pause(); setT(toplam); setCal(false); return; }
      const i = Math.max(0, plan.findIndex((p, j) => t < (plan[j + 1]?.bas ?? Infinity)));
      const p = plan[i];
      const h = sesHedef(p, t - p.bas);
      if (h === null) { if (!a.paused) a.pause(); }
      else {
        const url = klipUrl(p);
        if (!a.src.endsWith(url.split('/api/')[1])) { a.src = url; a.currentTime = h; }
        a.playbackRate = hiz;
        if (a.paused) { a.currentTime = h; a.play().catch(() => { /* görüntü sürer */ }); }
        else if (Math.abs(a.currentTime - h) > 0.3) a.currentTime = h;
      }
      if (now - son > 50) { setT(t); son = now; }
      id = requestAnimationFrame(adimla);
    };
    id = requestAnimationFrame(adimla);
    return () => { cancelAnimationFrame(id); a.pause(); };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [cal, hiz, plan, toplam, sesHedef]);

  useEffect(() => {
    kap.current?.requestFullscreen?.().catch(() => { /* izin yoksa kaplama pencereyi kaplar */ });
    kap.current?.focus();
    const d = (e: Event) => { if ((e as CustomEvent).detail !== 'ders-video') durdur(); };
    window.addEventListener(KMB_DURDUR, d);
    return () => { window.removeEventListener(KMB_DURDUR, d); audio.current?.pause(); };
  }, [durdur]);
  const kapat = () => { audio.current?.pause(); if (document.fullscreenElement) document.exitFullscreen().catch(() => {}); onKapat(); };
  const adimaGit = (yon: number) => {
    const hedefAi = Math.max(0, Math.min(ders.adimlar.length - 1, P.ai + yon));
    const p = plan.find((x) => x.ai === hedefAi && x.tur === 'adim');
    if (p) git(p.bas);
  };
  const tus = (e: React.KeyboardEvent) => {
    if (e.key === ' ' || e.key === 'k') { e.preventDefault(); if (cal) durdur(); else oynat(); }
    else if (e.key === 'ArrowRight') git(T + 5);
    else if (e.key === 'ArrowLeft') git(T - 5);
    else if (e.key === 'n' || e.key === 'PageDown') adimaGit(1);
    else if (e.key === 'p' || e.key === 'PageUp') adimaGit(-1);
    else if (e.key === 'c') setAltyazi((x) => !x);
    else if (e.key === 'Escape') kapat();
  };

  // adım parçası: etkin cümle, birikmiş eylemler, görsel, kamera hedefi
  const ci = P.tur === 'adim' ? P.zaman.findIndex((z, j) => lt < (P.zaman[j + 1]?.[0] ?? Infinity) && lt >= z[0] - 0.05) : -1;
  const cAktif = P.tur === 'adim' ? Math.max(-1, ci) : -1;
  const durum = useMemo(() => {
    let d: SahneDurum = {};
    if (P.tur === 'adim') adim.cumleler.slice(0, cAktif + 1).forEach((c) => { d = uygula(d, c.eylem); });
    return d;
  }, [P, adim, cAktif]);
  const gorsel = P.tur === 'adim' ? gorselSec(adim, Math.max(0, cAktif)) : '';
  const hedef = P.tur === 'adim' && cAktif >= 0
    ? (adim.cumleler[cAktif].eylem || []).find((e) => e.t !== 'gizle' && SAHNE_OGELERI[gorsel]?.includes(e.id))?.id : undefined;
  let yazi = '';
  if (P.tur === 'adim' && cAktif >= 0 && lt <= P.zaman[cAktif][1] + 0.4) yazi = adim.cumleler[cAktif].metin;
  if (P.tur === 'lottie') {
    const x = lt - KART;
    const b = P.v.bolumler.find((q) => x >= q.bas - 0.2 && x <= q.son + 0.4);
    yazi = b?.metin || '';
  }
  const kart = lt < KART;
  const adimNo = P.ai + 1;

  return (
    <div ref={kap} className="kmb-dv" tabIndex={0} onKeyDown={tus} role="dialog" aria-label={`Ders videosu: ${ders.ad}`}>
      <div className="kmb-dv-ust">
        <div><span className="kmb-dv-no">{adimNo} / {ders.adimlar.length}</span><b>{adim.baslik}</b></div>
        <button onClick={kapat} aria-label="Kapat">✕</button>
      </div>
      <div className="kmb-dv-tek" onClick={() => (cal ? durdur() : oynat())}>
        <div className="kmb-dv-cerceve">
          {P.tur === 'adim'
            ? <div key={`${adim.id}-${gorsel}`} className="kmb-dv-gecis"><KameraSahne sahne={gorsel} durum={durum} hedef={hedef} /></div>
            : <div key={`l-${P.v.ad}`} className="kmb-dv-gecis"><LottieVideo ad={P.v.ad} kod={ders.kod} ses={ses} zaman={Math.max(0, lt - KART)} /></div>}
          {kart && (
            <div className="kmb-dv-kart">
              {P.tur === 'adim'
                ? <><span>Adım {adimNo}</span><b>{adim.baslik}</b></>
                : <><span>Adım {adimNo}</span><b>{adim.baslik}</b></>}
            </div>
          )}
          {!cal && !kart && <span className="kmb-lv-buyuk-oynat" aria-hidden>▶</span>}
          {P.tur === 'adim' && <span className="kmb-dv-gorsel-ad">{SAHNELER[gorsel]?.ad}</span>}
        </div>
      </div>
      {altyazi && <div className={`kmb-dv-altyazi${yazi ? '' : ' sessiz'}`}>{yazi || ' '}</div>}
      <div className="kmb-lv-cubuk kmb-dv-cubuk">
        <div className="kmb-lv-zaman">
          {plan.map((p, i) => <span key={i} className={`kmb-lv-bolum-isaret${p.tur === 'lottie' ? ' lottie' : ''}`} style={{ left: `${(p.bas / toplam) * 100}%` }} title={ders.adimlar[p.ai].baslik} />)}
          <div className="kmb-lv-dolu" style={{ width: `${(T / toplam) * 100}%` }} />
          <input type="range" min={0} max={toplam} step={0.1} value={T} aria-label="Zaman" onChange={(e) => git(Number(e.target.value))} />
        </div>
        <div className="kmb-lv-dugmeler">
          <button onClick={() => adimaGit(-1)} aria-label="Önceki adım">⏮</button>
          <button onClick={() => (cal ? durdur() : oynat())} aria-label={cal ? 'Duraklat' : 'Oynat'}>{cal ? '❚❚' : '▶'}</button>
          <button onClick={() => adimaGit(1)} aria-label="Sonraki adım">⏭</button>
          <span className="kmb-lv-sure">{sn(T)} / {sn(toplam)}</span>
          <span className="kmb-lv-baslik">{ders.ad}</span>
          <select value={hiz} onChange={(e) => setHiz(Number(e.target.value))} aria-label="Hız">
            {[0.75, 1, 1.25, 1.5].map((h) => <option key={h} value={h}>{h}×</option>)}
          </select>
          <button className={altyazi ? 'etkin' : ''} onClick={() => setAltyazi((x) => !x)} aria-label="Altyazı">CC</button>
        </div>
      </div>
    </div>
  );
}
