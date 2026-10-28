/**
 * Yönetim ayrı girişi (2026-10-28, manage.html). Öğrenci uygulamasının ortak girişini (App.tsx, ~540 KB gzip) yüklemez:
 * yalnız kimlik (Firebase + adminFetchAuth), görünüm tokenları (palettes.ts), kit ve v16 kabuğu.
 * - Sunucu /manage* gezinmelerine manage.html döndürür (server.ts; Vite geliştirmede scripts/vite/yonetimGirisi.ts).
 * - Yönetici değilse (moderatör) ya da ?kabuk=v14 istendiyse tam uygulama (main.tsx) dinamik yüklenir: eski konsol orada.
 */
import React, { useEffect, useState } from 'react';
import { createRoot, type Root } from 'react-dom/client';
import { installAdminFetchAuth } from './services/adminFetchAuth';
import { applyTheme, readTheme } from './utils/theme';
import { ADMIN_EMAIL, auth, getLocalAdminSession, googleSignIn, setLocalAdminSession } from './services/auth';
import { setStoredPanelSecret } from './config/deployment';
import { realtimeEventService } from './services/realtimeEvents';
import { ManageV16 } from './components/manage16/ManageV16';
import './styles/yonetim-temel.css';

installAdminFetchAuth();
applyTheme(readTheme());

const yoneticiMi = (e?: string | null) => !!e && e.toLowerCase() === ADMIN_EMAIL.toLowerCase();

function eskiKabukIstendi(): boolean {
  try {
    const k = new URLSearchParams(window.location.search).get('kabuk');
    if (k === 'v14' || k === 'v16') sessionStorage.setItem('medsoru_manage_kabuk', k);
    return sessionStorage.getItem('medsoru_manage_kabuk') === 'v14';
  } catch { return false; }
}

let kok: Root | null = null;
/** Tam öğrenci uygulamasına düş (eski konsol, moderatör): kendi kökümüzü bırakıp main.tsx'i yükler */
function tamUygulama() {
  kok?.unmount();
  kok = null;
  void import('./main');
}

type Durum = 'bekle' | 'yonetici' | 'giris';

const Giris: React.FC<{ tamam: () => void }> = ({ tamam }) => {
  const [hata, setHata] = useState('');
  const [mesgul, setMesgul] = useState(false);
  return (
    <div className="yt-giris">
      <div className="yt-giris-kart">
        <b className="yt-logo" aria-hidden="true">M</b>
        <h1>MeDSor Yönetim</h1>
        <p>Bu konsol yalnız yöneticilere ve moderatörlere açık. Hesabınla ya da kalıcı yönetici anahtarınla giriş yap.</p>
        <div className="yt-giris-dugmeler">
          <a className="yt-btn" href="/">Siteye dön</a>
          <button type="button" className="yt-btn birincil" disabled={mesgul} onClick={async () => {
            setMesgul(true); setHata('');
            try {
              const r = await googleSignIn();
              if (r?.user && yoneticiMi(r.user.email)) tamam(); else if (r?.user) tamUygulama();
            } catch (e: any) { setHata(e?.message || 'Giriş yapılamadı.'); } finally { setMesgul(false); }
          }}>Google ile giriş</button>
        </div>
        <form onSubmit={(e) => {
          e.preventDefault();
          const sec = String(new FormData(e.currentTarget).get('panelSecret') || '').trim();
          if (sec.length < 24) { setHata('Geçerli bir MEDS_PANEL_SECRET (en az 24 karakter) girin.'); return; }
          setStoredPanelSecret(sec);
          setLocalAdminSession(ADMIN_EMAIL);
          try { localStorage.setItem('medsoru_user_registered', 'true'); } catch { /* */ }
          tamam();
        }}>
          <label htmlFor="yt-anahtar">Kalıcı yönetici anahtarı (MEDS_PANEL_SECRET)</label>
          <div className="yt-satir">
            <input id="yt-anahtar" name="panelSecret" type="password" autoComplete="off" placeholder="Anahtarı yapıştırın…" />
            <button type="submit" className="yt-btn">Bağlan</button>
          </div>
        </form>
        {hata && <p className="yt-hata" role="alert">{hata}</p>}
      </div>
    </div>
  );
};

const YonetimGirisi: React.FC = () => {
  const [durum, setDurum] = useState<Durum>(() => (yoneticiMi(getLocalAdminSession()?.email) ? 'yonetici' : 'bekle'));
  useEffect(() => {
    if (durum !== 'bekle') return;
    let iptal = false;
    const bitti = () => {
      if (iptal) return;
      const u = auth.currentUser;
      if (yoneticiMi(u?.email)) setDurum('yonetici');
      else if (u) tamUygulama(); // moderatör olabilir: rolü tam uygulama sunucudan öğrenir
      else setDurum('giris');
    };
    const hazir = typeof (auth as any).authStateReady === 'function' ? (auth as any).authStateReady() : Promise.resolve();
    void Promise.race([hazir, new Promise((r) => setTimeout(r, 6000))]).then(bitti, bitti);
    return () => { iptal = true; };
  }, [durum]);
  useEffect(() => { if (durum === 'yonetici') realtimeEventService.connect(); }, [durum]);

  if (durum === 'bekle') return <div className="yt-bekle" role="status" aria-label="Yükleniyor"><span /></div>;
  if (durum === 'giris') return <Giris tamam={() => setDurum('yonetici')} />;
  return <ManageV16 adminEmail={ADMIN_EMAIL} onExit={() => window.location.assign('/')} />;
};

if (eskiKabukIstendi()) {
  tamUygulama();
} else {
  kok = createRoot(document.getElementById('root')!);
  kok.render(<YonetimGirisi />);
}

// Dağıtımdan sonra eski parça istenirse (404) bir kez yenile
window.addEventListener('vite:preloadError', (e) => {
  const k = 'medsoru_last_chunk_reload';
  const simdi = Date.now();
  if (simdi - Number(sessionStorage.getItem(k) || 0) > 5000) {
    sessionStorage.setItem(k, String(simdi));
    e.preventDefault();
    window.location.reload();
  }
});
