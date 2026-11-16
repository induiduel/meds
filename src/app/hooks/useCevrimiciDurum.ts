/**
 * Çevrimiçi durumu + /?kimlik_yok bildirimi (2026-11-17, App.tsx'ten saf taşıma — davranış aynı).
 */
import { useState, useEffect } from 'react';
import { toast } from '../../components/ui/Toast';
import { offlineDatabaseService } from '../../services/offlineDatabaseService';

export function useCevrimiciDurum() {
  const [isOnline, setIsOnline] = useState(typeof navigator !== 'undefined' ? navigator.onLine : true);

  useEffect(() => {
    return offlineDatabaseService.subscribe((s) => setIsOnline(s.isOnline));
  }, []);

  // /k/<kimlik> çözülemezse sunucu /?kimlik_yok=<id> ile gönderir: kısa bilgi + parametreyi adresten temizle
  useEffect(() => {
    const id = new URLSearchParams(window.location.search).get('kimlik_yok');
    if (id === null) return;
    const t = window.setTimeout(() => {
      toast.info('Kayıt bulunamadı', `Bu bağlantının gösterdiği kayıt bulunamadı${id ? ` (${id.slice(0, 40)})` : ''}.`);
      try {
        const u = new URL(window.location.href);
        u.searchParams.delete('kimlik_yok');
        window.history.replaceState(window.history.state, '', u.pathname + u.search + u.hash);
      } catch { /* yok */ }
    }, 500);
    return () => clearTimeout(t);
  }, []);
  return { isOnline };
}
