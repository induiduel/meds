import React, { useEffect, useState } from 'react';
import { CloudDownload, CloudCheck, WifiOff } from 'lucide-react';
import { offlineDatabaseService, OfflineState } from '../../services/offlineDatabaseService';

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
export const OfflineStatusBadge: React.FC<OfflineStatusBadgeProps> = ({ onClick, className = '', isAdmin }) => {
  const [o, setO] = useState<OfflineState>(offlineDatabaseService.getState());
  useEffect(() => offlineDatabaseService.subscribe(setO), []);
  const { isOnline, isDatabaseDownloaded, isDownloading, progress, stats, queuedActionsCount } = o;

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
      title={isDatabaseDownloaded ? 'Çevrimdışı hazır' : 'Çevrimdışı kullanım için indir'}
      aria-label={isDatabaseDownloaded ? 'Çevrimdışı hazır' : 'Çevrimdışı kullanım için indir'}
    >
      {isDatabaseDownloaded ? <CloudCheck aria-hidden /> : <CloudDownload aria-hidden />}
    </button>
  );
};
