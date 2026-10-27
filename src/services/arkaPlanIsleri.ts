/**
 * Arka plan işleri (tasarım AB01/AB02): cihazda gerçekten izlenen işleri tek listede toplar — paralel kuyruk değildir.
 *  - Çevrimdışı paket indirmeleri: cevrimdisi/paketMotoru (aktif iş, kuyruk, bekleme nedeni, hatalar, duraklatma)
 *  - Sesli ders video dışa aktarımı: canliDers/cdVideoIs (tarayıcıda MP4 üretimi)
 *  - Eşitleme: userKvSync dirtyKvCount (gönderilmemiş profil değişiklikleri) + offlineDatabaseService gönderim kuyruğu
 */
import { useEffect, useState, useSyncExternalStore } from 'react';
import { useCevrimdisi } from './cevrimdisi/paketMotoru';
import { cdVideoIsAl, cdVideoIsDinle } from '../components/canliDers/cdVideoIs';
import { dirtyKvCount, onProfileDataChange } from './userKvSync';
import { offlineDatabaseService } from './offlineDatabaseService';
import { useNetState } from './net';

export function useVideoIs() {
  return useSyncExternalStore(cdVideoIsDinle, cdVideoIsAl, cdVideoIsAl);
}

export function useEsitlemeBekleyen() {
  const [kv, setKv] = useState(dirtyKvCount);
  const [kuyruk, setKuyruk] = useState(() => offlineDatabaseService.getState().queuedActionsCount || 0);
  useEffect(() => {
    const off1 = onProfileDataChange(() => setKv(dirtyKvCount()));
    const off2 = offlineDatabaseService.subscribe((s) => setKuyruk(s.queuedActionsCount || 0));
    const yenile = () => setKv(dirtyKvCount());
    window.addEventListener('medsoru:user-data-synced', yenile);
    const t = window.setInterval(yenile, 10_000);
    return () => { off1(); off2(); window.removeEventListener('medsoru:user-data-synced', yenile); window.clearInterval(t); };
  }, []);
  return { kv, kuyruk };
}

/** Üst bar göstergesi için iş sayısı: sürüp giden/sıradaki indirmeler + video + (çevrimdışıyken) bekleyen eşitleme */
export function useArkaPlanOzet() {
  const s = useCevrimdisi();
  const video = useVideoIs();
  const { kv, kuyruk } = useEsitlemeBekleyen();
  const ag = useNetState();
  const indirme = new Set([...(s.aktif ? [s.aktif.id] : []), ...s.kuyruk]);
  const esitleme = ag === 'offline' && kv + kuyruk > 0;
  const toplam = indirme.size + (video ? 1 : 0) + (esitleme ? 1 : 0);
  return { s, video, kv, kuyruk, ag, indirme: indirme.size, esitleme, toplam };
}
