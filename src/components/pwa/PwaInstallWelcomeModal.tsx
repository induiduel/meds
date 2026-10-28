import React, { useState } from 'react';
import { Archive, CloudDownload, Smartphone, WifiOff } from 'lucide-react';
import { pwaService, PWA_WELCOME_STORAGE_KEY } from '../../services/pwaService';
import { offlineDatabaseService } from '../../services/offlineDatabaseService';
import { Dialog } from '../ui/Dialog';
import { useAppearance } from '../../utils/appearance';
import { PwaWelcomeV12 } from '../v12/OnboardingV12';
import '../../styles/ayrik-of.css';

export { PWA_WELCOME_STORAGE_KEY };

interface PwaInstallWelcomeModalProps {
  isOpen: boolean;
  onClose: () => void;
  onOpenOfflineDatabase: () => void;
}

const remember = (permanent: boolean) => {
  try {
    localStorage.setItem(PWA_WELCOME_STORAGE_KEY, permanent ? 'permanent' : String(Date.now()));
  } catch {
    /* gizli sekme */
  }
};

/**
 * Öğrenciye açılışta bir kez sorulur: uygulamayı ekle + veriyi cihaza indir.
 * Yöneticiye gösterilmez (teknik ayrıntı çevrimdışı penceresinde).
 */
export const PwaInstallWelcomeModal: React.FC<PwaInstallWelcomeModalProps> = ({ isOpen, onClose, onOpenOfflineDatabase }) => {
  const [busy, setBusy] = useState(false);
  const v12 = useAppearance().design === 'v12';
  if (!isOpen) return null;

  const close = (permanent: boolean) => {
    remember(permanent);
    onClose();
  };

  const accept = async () => {
    setBusy(true);
    remember(true);
    const st = pwaService.getState();
    if (st.hasNativePrompt && !st.isInstalled) {
      await pwaService.promptInstall({ silentIfUnsupported: true });
    }
    onClose();
    onOpenOfflineDatabase();
    window.setTimeout(() => offlineDatabaseService.downloadEntireDatabase(), 300);
  };

  const openInstall = () => {
    remember(false);
    onClose();
    pwaService.openInstallGuide();
  };

  if (v12) return <PwaWelcomeV12 busy={busy} onLater={() => close(false)} onNever={() => close(true)} onAccept={accept} onInstallGuide={!pwaService.getState().isInstalled ? openInstall : undefined} />;

  return (
    <Dialog
      title="İnternetsiz de çalışsın mı?"
      onClose={() => close(false)}
      width="max-w-md"
      footer={
        <>
          <button type="button" className="ms-btn is-ghost is-sm mr-auto" onClick={() => close(true)}>Bir daha sorma</button>
          {!pwaService.getState().isInstalled && (
            <button type="button" className="ms-btn is-tonal" onClick={openInstall}>
              <Smartphone /> Ana Ekrana Ekle
            </button>
          )}
          <button type="button" className="ms-btn is-ghost" onClick={() => close(false)}>Sonra</button>
          <button type="button" className="ms-btn is-primary" onClick={accept} disabled={busy}>
            <CloudDownload /> İndir
          </button>
        </>
      }
    >
      <div className="of">
        <p className="of-lead">Soruları ve dersleri bir kez cihazına indir; metroda, nöbette, sınav salonunun kapısında açılır.</p>
        <ul className="of-perks">
          <li style={{ '--i': 0 } as React.CSSProperties}><WifiOff aria-hidden /><span><b>Bağlantı gerekmez</b>Çıkmış sorular, Öğren, Sözlük ve Kartlar cihazında.</span></li>
          <li style={{ '--i': 1 } as React.CSSProperties}><Smartphone aria-hidden /><span><b>Uygulama gibi</b>Ana ekrandan tek dokunuşla, tam ekran açılır.</span></li>
          <li style={{ '--i': 2 } as React.CSSProperties}><Archive aria-hidden /><span><b>Kendini günceller</b>İnternete bağlanınca yeni sorular gelir.</span></li>
        </ul>
      </div>
    </Dialog>
  );
};
