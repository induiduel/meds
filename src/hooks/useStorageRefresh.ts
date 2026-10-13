import { useEffect, useRef } from 'react';

/**
 * Profil eşitlemesi (başka cihaz/sekme) bu anahtarlardan birini değiştirince `onChange` çağrılır; açık ekran
 * yeniden yüklenmeden güncellenir. Olay userKvSync.applyKv ve tarayıcının sekmeler arası `storage` olayıdır.
 */
export function useStorageRefresh(keys: string[], onChange: () => void): void {
  const cb = useRef(onChange);
  cb.current = onChange;
  const sig = keys.join('|');
  useEffect(() => {
    const set = new Set(sig.split('|'));
    const h = (e: StorageEvent) => {
      if (e.key && set.has(e.key)) cb.current();
    };
    window.addEventListener('storage', h);
    return () => window.removeEventListener('storage', h);
  }, [sig]);
}
