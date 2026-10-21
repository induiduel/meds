import React, { useEffect, useState } from 'react';
import { CloudDownload, CloudCheck, WifiOff } from 'lucide-react';
import { offlineDatabaseService, OfflineState } from '../../services/offlineDatabaseService';
import { paketDurumu, useCevrimdisi } from '../../services/cevrimdisi/paketMotoru';
import { sayfaPaketleri } from '../../services/cevrimdisi/sayfaPaketleri';
import { navigateTo } from '../../router';

interface OfflineStatusBadgeProps {
  onClick: () => void;
  className?: string;
  /** Yönetici boyut ve bekleyen işlem sayısını da görür; öğrenciye yalnız durum simgesi */
  isAdmin?: boolean;
}

/**
 * Üst çubuktaki çevrimdışı göstergesi. Öğrenci: sessiz simge, yalnız internet yokken ya da
 * indirme sürerken yazı belirir. Yönetici: durum + boyut + kuyruk tek hapta.
 */
export const OfflineStatusBadge: React.FC<OfflineStatusBadgeProps> = ({ onClick: _ilk, className = '', isAdmin }) => {
  let onClick = _ilk;
  const [o, setO] = useState<OfflineState>(offlineDatabaseService.getState());
  useEffect(() => offlineDatabaseService.subscribe(setO), []);
  const { isOnline, isDownloading, progress, stats, queuedActionsCount } = o;
  // Simge bulunulan sayfaya göre: bu sayfanın paketleri cihazdaysa "hazır"; dokununca Çevrimdışı merkezi bu sayfanın kartıyla açılır
  const S = useCevrimdisi();
  const adres = typeof location !== 'undefined' ? location.pathname + location.search : '/';
  const ids = sayfaPaketleri(adres, S.katalog);
  const sayfaHazir = ids.length > 0 && ids.every((id) => ['tamam', 'guncelleme'].includes(paketDurumu(id, S)));
  const isDatabaseDownloaded = ids.length ? sayfaHazir : o.isDatabaseDownloaded;
  onClick = () => { if (!location.pathname.startsWith('/cevrimdisi')) navigateTo(`/cevrimdisi?sayfa=${encodeURIComponent(adres)}`); };

  if (isDownloading) {
    return (
      <button type="button" onClick={onClick} className={`of-badge is-busy ${className}`} style={{ '--p': progress.percent } as React.CSSProperties} title={`${progress.stage} · %${progress.percent}`} aria-label={`İndiriliyor, yüzde ${progress.percent}`}>
        <CloudDownload aria-hidden />
        <b>%{progress.percent}</b>
      </button>
    );
  }

  if (!isOnline) {
    return (
      <button type="button" onClick={onClick} className={`of-badge is-offline ${className}`} title={isDatabaseDownloaded ? 'İnternet yok · cihazdaki veriyle çalışıyor' : 'İnternet yok'}>
        <WifiOff aria-hidden />
        <span>Çevrimdışı</span>
        {isAdmin && queuedActionsCount > 0 && <b className="of-q">{queuedActionsCount}</b>}
      </button>
    );
  }

  if (isAdmin) {
    return (
      <button type="button" onClick={onClick} className={`of-badge is-admin ${isDatabaseDownloaded ? 'is-ready' : ''} ${className}`} title="Çevrimdışı veritabanı">
        {isDatabaseDownloaded ? <CloudCheck aria-hidden /> : <CloudDownload aria-hidden />}
        <span className="hidden sm:inline">{isDatabaseDownloaded ? `${stats.estimatedSizeMb || 0} MB` : 'İndirilmedi'}</span>
        {queuedActionsCount > 0 && <b className="of-q" title="Bekleyen işlem">{queuedActionsCount}</b>}
      </button>
    );
  }

  return (
    <button
      type="button"
      onClick={onClick}
      className={`of-badge is-icon ${isDatabaseDownloaded ? 'is-ready' : ''} ${className}`}
      title={isDatabaseDownloaded ? 'Bu sayfa çevrimdışı hazır' : 'Bu sayfayı çevrimdışı kullan'}
      aria-label={isDatabaseDownloaded ? 'Bu sayfa çevrimdışı hazır' : 'Bu sayfayı çevrimdışı kullan'}
    >
      {isDatabaseDownloaded ? <CloudCheck aria-hidden /> : <CloudDownload aria-hidden />}
    </button>
  );
};
