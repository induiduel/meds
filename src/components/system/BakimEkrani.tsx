import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Settings } from 'lucide-react';
import { useEsitlemeBekleyen } from '../../services/arkaPlanIsleri';
import '../../styles/v15/ek15.css';

/**
 * v15 · Bakım ekranı (tasarım AB18 bakim). Gösterim koşulu: GET /api/bakim → 503 + {bakim:true, sure?}
 * (sunucu: MEDS_BAKIM=1 ya da POST /api/admin/bakim; src/services/bakimHataRoutes.ts) ya da /surum.json'da `bakim` alanı.
 * Denetim: açılışta, 60 sn'de bir, sekmeye dönünce, bağlantı gelince. "Çalışman kaydedildi" yalnız eşitleme kuyruğu
 * (gönderilmemiş profil anahtarı + çevrimdışı gönderim kuyruğu) boşsa yazılır. Yönetim konsolunda gösterilmez.
 */
interface Durum { bakim: boolean; sure?: string; mesaj?: string }

async function denetle(): Promise<Durum> {
  try {
    const r = await fetch(`/api/bakim?t=${Date.now()}`, { cache: 'no-store' });
    if (r.status === 503) {
      const j = await r.json().catch(() => null);
      if (j?.bakim) return { bakim: true, sure: typeof j.sure === 'string' ? j.sure : undefined, mesaj: typeof j.mesaj === 'string' ? j.mesaj : undefined };
    }
  } catch { /* ağ yok: bakım sayılmaz */ }
  try {
    const r = await fetch(`/surum.json?t=${Date.now()}`, { cache: 'no-store' });
    if (r.ok) {
      const j = await r.json().catch(() => null);
      const b = j?.bakim;
      if (b) return { bakim: true, sure: typeof b === 'object' && typeof b.sure === 'string' ? b.sure : typeof b === 'string' ? b : undefined };
    }
  } catch { /* yok */ }
  return { bakim: false };
}

function BakimEkrani() {
  const [d, setD] = useState<Durum>({ bakim: false });
  useEffect(() => {
    if (/^\/(meds\/)?manage(\/|$)/.test(window.location.pathname)) return;
    let canli = true;
    const bak = () => { void denetle().then((x) => { if (canli) setD(x); }); };
    bak();
    // Gizli sekmede yoklama yok (görünür olunca `gor` hemen denetler); eskiden arka planda da dakikada iki istek.
    const t = window.setInterval(() => { if (document.visibilityState === 'visible') bak(); }, 60_000);
    const gor = () => { if (document.visibilityState === 'visible') bak(); };
    document.addEventListener('visibilitychange', gor);
    window.addEventListener('online', bak);
    return () => { canli = false; window.clearInterval(t); document.removeEventListener('visibilitychange', gor); window.removeEventListener('online', bak); };
  }, []);
  if (!d.bakim) return null;
  return <Ekran sure={d.sure} mesaj={d.mesaj} />;
}

function Ekran({ sure, mesaj }: { sure?: string; mesaj?: string }) {
  const { kv, kuyruk } = useEsitlemeBekleyen();
  const bos = kv + kuyruk === 0;
  return (
    <div className="bk15" role="alertdialog" aria-modal="true" aria-labelledby="bk15-b">
      <div className="bk15-k v15-card">
        <Settings className="bk15-ik" aria-hidden />
        <h1 id="bk15-b">Kısa bakım</h1>
        <p>{mesaj || 'Siteyi iyileştiriyoruz. Birazdan kendiliğinden geri döneceğiz.'}</p>
        {sure && <p className="bk15-sure">Tahmini süre: <b>{sure}</b></p>}
        <p className="v15-cap">{bos ? 'Çalışman kaydedildi.' : 'Gönderilmeyi bekleyen değişikliklerin bu cihazda duruyor; bakım bitince kendiliğinden gönderilecek.'}</p>
        <a className="v15-btn is-ghost" href="/cevrimdisi">İndirilen derslerim</a>
      </div>
    </div>
  );
}

let kurulu = false;
export function installBakimEkrani() {
  if (kurulu || typeof document === 'undefined') return;
  kurulu = true;
  const host = document.createElement('div');
  host.id = 'bakim-root';
  document.body.appendChild(host);
  createRoot(host).render(<BakimEkrani />);
}
