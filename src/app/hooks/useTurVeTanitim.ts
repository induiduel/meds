/**
 * Karşılama turu, giriş uyarısı ve tanıtım videoları (2026-11-17, App.tsx'ten saf taşıma — davranış aynı).
 */
import { useState, useEffect, useRef, type Dispatch, type SetStateAction } from 'react';
import { tourSeen } from '../../components/onboarding/tourState';
import { girisUyarisiKabulEdildi } from '../../components/onboarding/girisUyarisiDurum';

type Mod = 'login' | 'register' | 'admin';

export function useTurVeTanitim<T extends string>(
  activeTab: T,
  currentUser: { uid: string } | null,
  isAdmin: boolean,
  showOnboarding: boolean,
  setAuthModalInitialMode: Dispatch<SetStateAction<Mod>>,
  setIsAuthModalOpen: Dispatch<SetStateAction<boolean>>,
) {
  const [showTour, setShowTour] = useState(false);
  // Giriş bilgilendirmesi (yapay zekâ uyarısı): kabul edilmeden uygulama kullanılmaz; turlar kabulü bekler
  const [girisUyarisi, setGirisUyarisi] = useState(() => !girisUyarisiKabulEdildi() && !/^\/manage(\/|$)/.test(window.location.pathname));
  const justAuthedRef = useRef(false);
  const activeTabRef = useRef(activeTab);
  activeTabRef.current = activeTab;
  useEffect(() => {
    const on = () => setShowTour(true);
    window.addEventListener('medsoru:tour', on);
    return () => window.removeEventListener('medsoru:tour', on);
  }, []);
  // H167: ekranlar (ör. Arkadaşlar "Giriş gerekli") giriş penceresini `medsoru:giris-ac` olayıyla açar
  useEffect(() => {
    const on = () => { setAuthModalInitialMode('login'); setIsAuthModalOpen(true); };
    window.addEventListener('medsoru:giris-ac', on);
    return () => window.removeEventListener('medsoru:giris-ac', on);
  }, []);
  // Tanıtım videoları: turdan sonra bir kez (`medsoru_tanitim_v1`); `medsoru:tanitim` ile yeniden
  const [showTanitim, setShowTanitim] = useState(false);
  useEffect(() => {
    const on = () => setShowTanitim(true);
    window.addEventListener('medsoru:tanitim', on);
    return () => window.removeEventListener('medsoru:tanitim', on);
  }, []);
  const tanitimGoruldu = () => { try { return localStorage.getItem('medsoru_tanitim_v1') === '1'; } catch { return true; } };
  useEffect(() => {
    // Turu önceden görmüş öğrenciye de bir kez
    if (!currentUser || isAdmin || girisUyarisi || !tourSeen() || tanitimGoruldu()) return;
    const t = window.setTimeout(() => {
      if (!document.querySelector('[role="dialog"][aria-modal="true"]') && !['manage', 'practice', 'admin'].includes(activeTabRef.current)) setShowTanitim(true);
    }, 5000);
    return () => window.clearTimeout(t);
  }, [currentUser?.uid, isAdmin, girisUyarisi]);
  useEffect(() => {
    if (!currentUser || isAdmin || showOnboarding || girisUyarisi || tourSeen()) return;
    // Başka cihazda turu görmüş öğrencinin profili gelsin diye kısa bekle (eşitleme `medsoru_tour_v1`'i getirir)
    let fired = false;
    const check = () => {
      if (fired) return;
      fired = true;
      const busy = document.querySelector('.sh-sheet-root, .ls-root, .cf-root, [role="dialog"][aria-modal="true"]');
      if (!tourSeen() && !busy && !['manage', 'practice', 'admin'].includes(activeTabRef.current)) setShowTour(true);
    };
    const onRestored = () => window.setTimeout(check, 250);
    window.addEventListener('medsoru:user-data-restored', onRestored);
    const t = window.setTimeout(check, justAuthedRef.current ? 900 : 4000);
    justAuthedRef.current = false;
    return () => {
      window.clearTimeout(t);
      window.removeEventListener('medsoru:user-data-restored', onRestored);
    };
  }, [currentUser?.uid, isAdmin, showOnboarding, girisUyarisi]);
  return { showTour, setShowTour, girisUyarisi, setGirisUyarisi, justAuthedRef, activeTabRef, showTanitim, setShowTanitim, tanitimGoruldu };
}
