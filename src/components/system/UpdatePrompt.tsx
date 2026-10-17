import React, { useEffect, useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Sparkles, RefreshCw } from 'lucide-react';
import './system.css';

declare const __MEDS_SURUM__: string;
declare const __MEDS_ONEM__: number;

/**
 * Önemli güncelleme diyaloğu: /api/surum (dist/surum.json) açık sekmeninkinden büyük bir önem sayısı bildirince
 * "Siteyi güncelle" diyaloğu açılır; Güncelle → bekleyen SW etkinleşir, sayfa yeni sürümle yenilenir.
 * Önem sayısı guncelleme_notu.json'dan gelir (yalnız önemli güncellemede artırılır); küçük derlemeler diyalog açmaz.
 * Denetim: açılıştan 20 sn sonra, 5 dk'da bir, sekmeye dönünce ve bağlantı gelince. "Sonra" 30 dk erteler.
 */
const ONEM = typeof __MEDS_ONEM__ === 'number' ? __MEDS_ONEM__ : 0;
const SURUM = typeof __MEDS_SURUM__ === 'string' ? __MEDS_SURUM__ : '';
const ERTELE_MS = 30 * 60 * 1000;
const ARALIK_MS = 5 * 60 * 1000;

type Bilgi = { surum: string; onem: number; baslik?: string; maddeler?: string[] };

async function sunucuSurumu(): Promise<Bilgi | null> {
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
  const [bilgi, setBilgi] = useState<Bilgi | null>(null);
  const [mesgul, setMesgul] = useState(false);
  const erteleme = useRef(0);
  const dugme = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (import.meta.env.DEV) return;
    let iptal = false;
    const denetle = async () => {
      if (document.visibilityState !== 'visible' || Date.now() < erteleme.current) return;
      const b = await sunucuSurumu();
      if (!iptal && b && b.onem > ONEM && b.surum !== SURUM) setBilgi(b);
    };
    const ilk = window.setTimeout(denetle, 20_000);
    const aralik = window.setInterval(denetle, ARALIK_MS);
    const gorunur = () => void denetle();
    document.addEventListener('visibilitychange', gorunur);
    window.addEventListener('online', gorunur);
    return () => {
      iptal = true;
      window.clearTimeout(ilk);
      window.clearInterval(aralik);
      document.removeEventListener('visibilitychange', gorunur);
      window.removeEventListener('online', gorunur);
    };
  }, []);

  useEffect(() => { if (bilgi) dugme.current?.focus(); }, [bilgi]);

  if (!bilgi) return null;
  const sonra = () => { erteleme.current = Date.now() + ERTELE_MS; setBilgi(null); };
  const maddeler = (bilgi.maddeler || []).filter(Boolean);

  return (
    <div className="up-scrim" role="presentation" onKeyDown={(e) => { if (e.key === 'Escape') sonra(); }}>
      <div className="up-card" role="alertdialog" aria-modal="true" aria-labelledby="up-baslik" aria-describedby="up-govde">
        <div className="up-ico"><Sparkles /></div>
        <h2 id="up-baslik" className="up-h">{bilgi.baslik || 'Site güncellendi'}</h2>
        <div id="up-govde" className="up-b">
          {maddeler.length ? <ul>{maddeler.map((m, i) => <li key={i}>{m}</li>)}</ul> : <p>Yeni değişikliklerin hepsini görmek için siteyi yenile.</p>}
          <p className="up-not">Notların ve ilerlemen korunur.</p>
        </div>
        <div className="up-act">
          <button type="button" className="up-btn is-2" onClick={sonra}>Sonra</button>
          <button ref={dugme} type="button" className="up-btn is-1" disabled={mesgul} onClick={() => { setMesgul(true); void guncelle(); }}>
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
