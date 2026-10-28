import React, { useEffect, useRef, useState, useSyncExternalStore } from 'react';
import { createRoot } from 'react-dom/client';
import { Sparkles, RefreshCw } from 'lucide-react';
import './system.css';
import { cevrimdisiMi } from '../../services/net';

declare const __MEDS_SURUM__: string;
declare const __MEDS_ONEM__: number;

/**
 * Önemli güncelleme diyaloğu: /api/surum (dist/surum.json) açık sekmeninkinden büyük bir önem sayısı bildirince
 * "Siteyi güncelle" diyaloğu açılır; Güncelle → bekleyen SW etkinleşir, sayfa yeni sürümle yenilenir.
 * Önem sayısı guncelleme_notu.json'dan gelir (yalnız önemli güncellemede artırılır); küçük derlemeler diyalog açmaz.
 * Biriken güncelleme sayısı = sunucu önemi − sekmenin önemi. 2+ birikmişse diyalog kendiliğinden açılır; yalnız 1 ise
 * diyalog açılmaz, üst çubukta GuncellemeSimgesi görünür (dokununca aynı diyalog). Durum modül deposundadır: diyalog
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

const goruldu = (): number => {
  try { return Number(localStorage.getItem(GORULDU_KEY)) || 0; } catch { return 0; }
};
const gorulduYaz = (onem: number) => {
  try { if (onem > goruldu()) localStorage.setItem(GORULDU_KEY, String(onem)); } catch { /* depolama kapalı */ }
};
/* ── Ortak depo: bekleyen güncelleme + diyalog açık mı ── */
type Durum = { bilgi: Bilgi | null; acik: boolean };
let durum: Durum = { bilgi: null, acik: false };
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

type Bilgi = { surum: string; onem: number; baslik?: string; maddeler?: string[] };

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
    // Bu sekme zaten yeni sürümdeyse kaydı ilerlet (başka sekmede/yenilemede aynı sürüm yeniden sorulmasın)
    gorulduYaz(ONEM);
    let iptal = false;
    let indirildi = false;
    const denetle = async () => {
      if (document.visibilityState !== 'visible') return;
      const b = await sunucuSurumu();
      if (iptal || !b || b.onem <= ONEM || b.surum === SURUM) return;
      yay({ bilgi: b }); // üst çubuk simgesi her durumda görünür
      if (birikmis(b) < 2 || b.onem <= goruldu()) {
        // Tek güncelleme ya da daha önce sorulmuş: diyalog açma, yalnız arka planda hazırla
        if (!indirildi) { indirildi = true; sessizIndir(); }
        return;
      }
      yay({ acik: true });
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

  if (!bilgi) return null;
  const sonra = () => { gorulduYaz(bilgi.onem); sessizIndir(); yay({ acik: false }); };
  const maddeler = (bilgi.maddeler || []).filter(Boolean);

  return (
    <div className="up-scrim" role="presentation" onKeyDown={(e) => { if (e.key === 'Escape') sonra(); }}>
      <div className="up-card" role="alertdialog" aria-modal="true" aria-labelledby="up-baslik" aria-describedby="up-govde">
        <div className="up-ico"><Sparkles /></div>
        <h2 id="up-baslik" className="up-h">{bilgi.baslik || 'Site güncellendi'}</h2>
        <div id="up-govde" className="up-b">
          {maddeler.length ? <ul>{maddeler.map((m, i) => <li key={i}>{m}</li>)}</ul> : <p>Yeni değişikliklerin hepsini görmek için siteyi yenile.</p>}
          <p className="up-not">Notların ve ilerlemen korunur. “Sonra” dersen site sonraki açılışında kendiliğinden yenilenir; o zamana dek üst çubuktaki ✦ simgesinden güncelleyebilirsin. <a href="/guncellemeler" target="_blank" rel="noopener">Tüm sürüm notları</a></p>
        </div>
        <div className="up-act">
          <button type="button" className="up-btn is-2" onClick={sonra}>Sonra</button>
          <button ref={dugme} type="button" className="up-btn is-1" disabled={mesgul} onClick={() => { gorulduYaz(bilgi.onem); setMesgul(true); void guncelle(); }}>
            <RefreshCw className={mesgul ? 'is-spin' : ''} /> Siteyi güncelle
          </button>
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
