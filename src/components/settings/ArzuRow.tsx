import React from 'react';
import { Sparkles } from 'lucide-react';
import { auth, type AppUser } from '../../services/auth';
import { arzuHesabiMi, arzuKatmaniAyarla, useArzuAcik } from '../arzu/arzuKimlik';
import { toast } from '../ui/Toast';

/**
 * Ayarlar · küçük sürprizler (tilki, kalpler, notlar) aç/kapa. Yalnız katmanı görebilen hesaplarda listelenir;
 * tercih cihaza özeldir (medsoru_arzu_kapali). Sürüm notlarında anılmaz.
 */
export const ArzuRow: React.FC<{ currentUser?: AppUser | null }> = ({ currentUser }) => {
  const acik = useArzuAcik();
  const user = currentUser === undefined ? (auth.currentUser as AppUser | null) : currentUser;
  if (!arzuHesabiMi(user)) return null;
  const degistir = () => {
    arzuKatmaniAyarla(!acik);
    if (acik) toast.info('Küçük sürprizler kapatıldı', 'İstediğin zaman buradan yeniden açabilirsin.');
    else toast.success('Küçük sürprizler açık', 'Tilki yine ortalarda.');
  };
  return (
    <div className="ui-row has-icon">
      <span className="ui-ico" style={{ '--ico-bg': 'var(--color-accent)', '--ico-fg': 'var(--color-on-solid)' } as React.CSSProperties}>
        <Sparkles strokeWidth={2.1} />
      </span>
      <span className="ui-row-main">
        <b>Küçük sürprizler</b>
        <span>{acik ? 'Açık — tilki, kalpler ve notlar görünür' : 'Kapalı — tilki, kalpler ve notlar gizli'}</span>
      </span>
      <button type="button" role="switch" aria-checked={acik} className={`ui-btn is-sm ${acik ? 'is-tonal' : 'is-primary'}`} onClick={degistir}>
        {acik ? 'Kapat' : 'Aç'}
      </button>
    </div>
  );
};
