import React, { useEffect, useRef, useState, useSyncExternalStore } from 'react';
import { createRoot } from 'react-dom/client';
import { Sparkles, RefreshCw, X } from 'lucide-react';
import { Madde, YenilikKarti, type Yenilik } from '../guncellemeler/SurumNotu';
import '../../styles/guncellemeler.css';
import './system.css';
import { cevrimdisiMi } from '../../services/net';

declare const __MEDS_SURUM__: string;
declare const __MEDS_ONEM__: number;
declare const __MEDS_NOT__: { baslik?: string; maddeler?: string[]; yenilikler?: Yenilik[] };

/**
 * Önemli güncelleme diyaloğu: /api/surum (dist/surum.json) açık sekmeninkinden büyük bir önem sayısı bildirince
 * "Siteyi güncelle" diyaloğu açılır; Güncelle → bekleyen SW etkinleşir, sayfa yeni sürümle yenilenir.
 * Önem sayısı guncelleme_notu.json'dan gelir (yalnız önemli güncellemede artırılır); küçük derlemeler diyalog açmaz.
 * Biriken güncelleme sayısı = sunucu önemi − sekmenin önemi. Diyalog HİÇBİR durumda kendiliğinden açılmaz (2026-10-29 kararı);
 * üst çubukta GuncellemeSimgesi görünür, yalnız dokununca diyalog açılır. Durum modül deposundadır: diyalog
 * ayrı React kökünde, simge kabukta olsa da aynı bilgiyi okur.
 * Kendiliğinden açılan diyalog her önem sayısı için bu cihazda YALNIZ BİR KEZ sorulur (GORULDU_KEY, cihaza özel, profil eşitlemesine girmez):
 * "Sonra" ya da "Güncelle" sonrası aynı sürüm için diyalog bir daha açılmaz — yenileme önbellekten eski paketi
 * getirse bile döngü olmaz; yeni sürüm arka planda iner ve sonraki açılışta sessizce gelir. Bir sekmede kapatılan
 * diyalog diğer sekmelerde de kapanır. Denetim: açılıştan 20 sn sonra, 5 dk'da bir, sekmeye dönünce ve bağlantı gelince.
 */
const ONEM = typeof __MEDS_ONEM__ === 'number' ? __MEDS_ONEM__ : 0;
const SURUM = typeof __MEDS_SURUM__ === 'string' ? __MEDS_SURUM__ : '';
const ARALIK_MS = 5 * 60 * 1000;
const GORULDU_KEY = 'medsoru_guncelleme_goruldu_v1';
/** Bu cihazda "Yenilikler" penceresinin gösterildiği son önem sayısı (yeni sürüme geçtikten sonraki ilk açılış) */
const YENILIK_KEY = 'medsoru_yenilik_goruldu_v1';
const NOT = typeof __MEDS_NOT__ === 'object' && __MEDS_NOT__ ? __MEDS_NOT__ : {};

const goruldu = (): number => {
  try { return Number(localStorage.getItem(GORULDU_KEY)) || 0; } catch { return 0; }
};
const gorulduYaz = (onem: number) => {
  try { if (onem > goruldu()) localStorage.setItem(GORULDU_KEY, String(onem)); } catch { /* depolama kapalı */ }
};
/* ── Ortak depo: bekleyen güncelleme + diyalog açık mı ── */
type Durum = { bilgi: Bilgi | null; acik: boolean; yenilik: boolean };
let durum: Durum = { bilgi: null, acik: false, yenilik: false };
const dinleyiciler = new Set<() => void>();
const yay = (d: Partial<Durum>) => { durum = { ...durum, ...d }; dinleyiciler.forEach((f) => f()); };
const abone = (f: () => void) => { dinleyiciler.add(f); return () => { dinleyiciler.delete(f); }; };
const useDurum = () => useSyncExternalStore(abone, () => durum, () => durum);
/** Biriken güncelleme sayısı (önem farkı) */
const birikmis = (b: Bilgi | null) => (b ? Math.max(0, b.onem - ONEM) : 0);

/** Üst çubuk simgesi: bekleyen güncelleme varken görünür; dokununca notlar + "Siteyi güncelle" */
export const GuncellemeSimgesi: React.FC<{ className?: string }> = ({ className = '' }) => {
  const { bilgi } = useDurum();
  if (!bilgi) return null;
  const n = birikmis(bilgi);
  return (
    <button type="button" className={`up-ikon ${className}`} onClick={() => yay({ acik: true })}
      aria-label={n > 1 ? `${n} güncelleme var, ayrıntı ve güncelle` : 'Güncelleme var, ayrıntı ve güncelle'} title="Site güncellendi — yenilemek için dokun">
      <Sparkles aria-hidden />
      <span className="up-ikon-n" aria-hidden />
    </button>
  );
};

/** Yeni sürümü sormadan arka planda indir; sonraki açılışta kendiliğinden etkinleşir */
const sessizIndir = () => { navigator.serviceWorker?.getRegistration().then((r) => r?.update()).catch(() => {}); };

type Bilgi = { surum: string; onem: number; baslik?: string; maddeler?: string[]; yenilikler?: Yenilik[] };

async function sunucuSurumu(): Promise<Bilgi | null> {
  if (cevrimdisiMi()) return null; // çevrimdışıyken sürüm sorulmaz; bağlantı gelince yeniden denetlenir
  try {
    const r = await fetch(`/api/surum?t=${Date.now()}`, { cache: 'no-store' });
    if (!r.ok) return null;
    const j = await r.json();
    return j && typeof j.onem === 'number' ? j : null;
  } catch {
    return null;
  }
}

async function guncelle() {
  try {
    const reg = await navigator.serviceWorker?.getRegistration();
    await reg?.update().catch(() => {});
    const bekleyen = reg?.waiting || reg?.installing;
    bekleyen?.postMessage({ type: 'SKIP_WAITING' });
    // index.html ve sürümsüz çalışma zamanı kopyaları eski sürümü geri vermesin (canlı ders çevrimdışı önbelleği korunur)
    if ('caches' in window) {
      for (const k of await caches.keys()) if (/^medsoru-(runtime|static)-/.test(k)) await caches.delete(k);
      // SW gezinmede kabuğu bütün önbelleklerde arar; başka önbellekte kalan eski '/' ya da '/index.html'
      // "Güncelle"den sonra eski sürümü geri açıyordu (H503)
      for (const k of await caches.keys()) {
        if (/canli-ders|pdf-offline|paket|bekleyen|paylasim/.test(k)) continue; // çevrimdışı ders paketleri korunur
        const c = await caches.open(k);
        for (const r of await c.keys()) {
          const u = new URL(r.url);
          if (u.origin === location.origin && (u.pathname === '/' || u.pathname.endsWith('.html') || !/\.[a-z0-9]+$/i.test(u.pathname)) && !u.pathname.startsWith('/api/')) await c.delete(r);
        }
      }
    }
  } catch { /* yine de yenile */ }
  window.location.reload();
}

const UpdatePrompt: React.FC = () => {
  const { bilgi: bekleyen, acik } = useDurum();
  const bilgi = acik ? bekleyen : null;
  const [mesgul, setMesgul] = useState(false);
  const dugme = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (import.meta.env.DEV) return;
    // Yeni sürüme geçtikten sonraki ilk açılış: yalnız bilgilendiren "Yenilikler" penceresi (yenileme gerekmez).
    // Hiç kaydı olmayan (ilk kez gelen) cihaza gösterilmez; kayıt sessizce yazılır.
    try {
      const once = localStorage.getItem(YENILIK_KEY) ?? localStorage.getItem(GORULDU_KEY);
      if (once !== null && Number(once) < ONEM && ONEM > 0) yay({ yenilik: true });
      // Kayıt yalnız ileri gider: önbellekten açılan eski kabuk (daha küçük ONEM) kaydı geri yazarsa
      // yeni sürüm her açılışta "Yenilikler"i yeniden gösteriyordu (H503)
      if (once === null || Number(once) < ONEM) localStorage.setItem(YENILIK_KEY, String(ONEM));
    } catch { /* depolama kapalı */ }
    // Bu sekme zaten yeni sürümdeyse kaydı ilerlet (başka sekmede/yenilemede aynı sürüm yeniden sorulmasın)
    gorulduYaz(ONEM);
    let iptal = false;
    let indirildi = false;
    const denetle = async () => {
      if (document.visibilityState !== 'visible') return;
      const b = await sunucuSurumu();
      if (iptal || !b || b.onem <= ONEM || b.surum === SURUM) return;
      // Eski sürümdeki sekme: "Güncelle" penceresi bu önem için cihazda bir kez kendiliğinden açılır (2026-10-31 kararı);
      // sonrasında yalnız üst çubuk ✦ simgesi kalır. Yeni sürüm arka planda iner.
      yay({ bilgi: b, acik: durum.acik || (b.onem > goruldu() && !durum.yenilik) });
      if (!indirildi) { indirildi = true; sessizIndir(); }
    };
    const ilk = window.setTimeout(denetle, 20_000);
    const aralik = window.setInterval(denetle, ARALIK_MS);
    const gorunur = () => void denetle();
    // Başka sekmede kapatıldı/güncellendi: bu sekmedeki diyalog da kapansın
    const depo = (e: StorageEvent) => {
      if (e.key !== GORULDU_KEY) return;
      if (durum.bilgi && durum.bilgi.onem <= goruldu()) yay({ acik: false });
    };
    document.addEventListener('visibilitychange', gorunur);
    window.addEventListener('online', gorunur);
    window.addEventListener('storage', depo);
    return () => {
      iptal = true;
      window.clearTimeout(ilk);
      window.clearInterval(aralik);
      document.removeEventListener('visibilitychange', gorunur);
      window.removeEventListener('online', gorunur);
      window.removeEventListener('storage', depo);
    };
  }, []);

  useEffect(() => { if (bilgi) dugme.current?.focus(); }, [bilgi]);

  const { yenilik } = useDurum();
  if (!bilgi && yenilik) return <Pencere kip="yenilik" baslik={NOT.baslik} maddeler={NOT.maddeler} yenilikler={NOT.yenilikler} kapat={() => yay({ yenilik: false })} />;
  if (!bilgi) return null;
  const sonra = () => { gorulduYaz(bilgi.onem); sessizIndir(); yay({ acik: false }); };
  const n = birikmis(bilgi);
  return (
    <Pencere kip="guncelle" baslik={bilgi.baslik} maddeler={bilgi.maddeler} yenilikler={bilgi.yenilikler} kapat={sonra}
      ust={n > 1 ? `${n} güncelleme birikti` : 'Yeni sürüm hazır'}
      alt={<>
        <button type="button" className="up-btn is-2" onClick={sonra}>Sonra</button>
        <button ref={dugme} type="button" className="up-btn is-1" disabled={mesgul} onClick={() => { gorulduYaz(bilgi.onem); setMesgul(true); void guncelle(); }}>
          <RefreshCw className={mesgul ? 'is-spin' : ''} /> Siteyi güncelle
        </button>
      </>}
      not="Notların ve ilerlemen korunur. “Sonra” dersen site sonraki açılışında kendiliğinden yenilenir; o zamana dek üst çubuktaki ✦ simgesinden güncelleyebilirsin." />
  );
};

/** Ortak pencere: kip "guncelle" (eski sürüm → yenile) ya da "yenilik" (yeni sürüm açıldı → yalnız bilgi) */
const Pencere: React.FC<{ kip: 'guncelle' | 'yenilik'; baslik?: string; maddeler?: string[]; yenilikler?: Yenilik[];
  kapat: () => void; ust?: string; alt?: React.ReactNode; not?: string }> = ({ kip, baslik, maddeler, yenilikler, kapat, ust, alt, not }) => {
  const tamam = useRef<HTMLButtonElement>(null);
  useEffect(() => { if (kip === 'yenilik') tamam.current?.focus(); }, [kip]);
  // Esc odak pencerenin dışındayken de kapatır (perdeye bağlı dinleyici yalnız odak içerideyken çalışıyordu)
  const kapatRef = useRef(kapat); kapatRef.current = kapat;
  useEffect(() => {
    const tus = (e: KeyboardEvent) => { if (e.key === 'Escape') kapatRef.current(); };
    document.addEventListener('keydown', tus);
    return () => document.removeEventListener('keydown', tus);
  }, []);
  const ys = (yenilikler || []).filter((y) => y && y.ad);
  const ms = (maddeler || []).filter(Boolean);
  return (
    <div className="up-scrim" role="presentation"
      onClick={(e) => { if (kip === 'yenilik' && e.target === e.currentTarget) kapat(); }}>
      <div className={`up-card up-genis is-${kip}`} role={kip === 'guncelle' ? 'alertdialog' : 'dialog'} aria-modal="true" aria-labelledby="up-baslik">
        <button type="button" className="up-x" onClick={kapat} aria-label="Kapat"><X /></button>
        <div className="up-bas">
          <div className="up-ico">{kip === 'guncelle' ? <RefreshCw /> : <Sparkles />}</div>
          <div>
            <p className="up-ust">{ust || (kip === 'yenilik' ? 'Yenilikler · bu sürümde' : 'Yeni sürüm')}</p>
            <h2 id="up-baslik" className="up-h">{baslik || (kip === 'yenilik' ? 'Site güncellendi' : 'Siteyi güncelle')}</h2>
          </div>
        </div>
        <div className="up-b">
          {ys.length > 0 && <div className="sn-liste">{ys.map((y, i) => <YenilikKarti key={i} y={y} onGit={kapat} />)}</div>}
          {ms.length > 0 && (
            <>
              {ys.length > 0 && <h3 className="up-ara">Ayrıca</h3>}
              <ul className="sn-madde">{ms.map((m, i) => <li key={i}><Madde m={m} /></li>)}</ul>
            </>
          )}
          {!ys.length && !ms.length && <p>Yeni değişikliklerin hepsini görmek için siteyi yenile.</p>}
        </div>
        {not && <p className="up-not">{not}</p>}
        <div className="up-act">
          {alt || <>
            <a className="up-btn is-2" href="/guncellemeler" onClick={kapat}>Tüm sürüm notları</a>
            <button ref={tamam} type="button" className="up-btn is-1" onClick={kapat}>Anladım</button>
          </>}
        </div>
      </div>
    </div>
  );
};

let mounted = false;
export function installUpdatePrompt() {
  if (mounted || typeof document === 'undefined') return;
  mounted = true;
  const host = document.createElement('div');
  host.id = 'update-prompt-root';
  document.body.appendChild(host);
  createRoot(host).render(<UpdatePrompt />);
}
