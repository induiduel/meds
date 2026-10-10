import React, { useState, useEffect } from 'react';
import { Wifi, WifiOff, CheckCircle2, DownloadCloud, RefreshCw } from 'lucide-react';
import { offlineDatabaseService, OfflineState } from '../../services/offlineDatabaseService';

interface OfflineStatusBadgeProps {
  onClick: () => void;
  className?: string;
  variant?: 'pill' | 'icon' | 'compact';
}

export const OfflineStatusBadge: React.FC<OfflineStatusBadgeProps> = ({
  onClick,
  className = '',
  variant = 'pill',
}) => {
  const [offlineState, setOfflineState] = useState<OfflineState>(offlineDatabaseService.getState());

  useEffect(() => {
    return offlineDatabaseService.subscribe(setOfflineState);
  }, []);

  const { isOnline, isDatabaseDownloaded, isDownloading, progress } = offlineState;

  // Çevrimdışıysa (İnternet Yok)
  if (!isOnline) {
    if (variant === 'icon') {
      return (
        <button
          type="button"
          onClick={onClick}
          title="Çevrimdışı Mod (İnternet Yok) - Veritabanı Aktif"
          className={`w-9 h-9 rounded-xl bg-amber-500/10 text-amber-600 flex items-center justify-center cursor-pointer hover:bg-amber-500/20 transition-colors ${className}`}
        >
          <WifiOff className="w-4 h-4" />
        </button>
      );
    }
    return (
      <button
        type="button"
        onClick={onClick}
        title="Çevrimdışı Mod - Yerel veritabanı devrede"
        className={`px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-500/15 text-amber-700 dark:text-amber-300 border border-amber-500/30 flex items-center gap-1.5 cursor-pointer hover:bg-amber-500/25 transition-all ${className}`}
      >
        <span className="w-2 h-2 rounded-full bg-amber-500 animate-pulse" />
        <span className="hidden sm:inline">Çevrimdışı Mod</span>
        <span className="sm:hidden">Çevrimdışı</span>
      </button>
    );
  }

  // İndirme işlemi sürüyorsa
  if (isDownloading) {
    return (
      <button
        type="button"
        onClick={onClick}
        title={`Veritabanı İndiriliyor: %${progress.percent}`}
        className={`px-2.5 py-1 rounded-full text-xs font-semibold bg-accent-soft text-accent border border-accent/30 flex items-center gap-1.5 cursor-pointer ${className}`}
      >
        <RefreshCw className="w-3.5 h-3.5 animate-spin" />
        <span>%{progress.percent}</span>
      </button>
    );
  }

  // Veritabanı cihazda kurulmuşsa
  if (isDatabaseDownloaded) {
    if (variant === 'icon') {
      return (
        <button
          type="button"
          onClick={onClick}
          title="Tüm Veritabanı Cihazınızda Kurulu (Çevrimdışı Hazır)"
          className={`w-9 h-9 rounded-xl bg-emerald-500/10 text-emerald-600 flex items-center justify-center cursor-pointer hover:bg-emerald-500/20 transition-colors ${className}`}
        >
          <CheckCircle2 className="w-4 h-4" />
        </button>
      );
    }
    return (
      <button
        type="button"
        onClick={onClick}
        title="Tüm Veritabanı Cihazınızda Kurulu (Çevrimdışı Hazır)"
        className={`px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 border border-emerald-500/20 flex items-center gap-1.5 cursor-pointer hover:bg-emerald-500/20 transition-all ${className}`}
      >
        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
        <span className="hidden md:inline">Çevrimdışı Hazır</span>
      </button>
    );
  }

  // Henüz indirilmemişse
  if (variant === 'icon') {
    return (
      <button
        type="button"
        onClick={onClick}
        title="Tüm Veritabanını Cihaza İndir (Çevrimdışı Yap)"
        className={`w-9 h-9 rounded-xl bg-canvas text-ink-2 hover:text-ink flex items-center justify-center cursor-pointer hover:bg-line-soft transition-colors ${className}`}
      >
        <DownloadCloud className="w-4 h-4" />
      </button>
    );
  }

  return (
    <button
      type="button"
      onClick={onClick}
      title="Tüm Veritabanını Cihaza İndir (Çevrimdışı Kullanım)"
      className={`px-2.5 py-1 rounded-full text-xs font-medium bg-canvas text-ink-2 hover:text-ink border border-line flex items-center gap-1.5 cursor-pointer hover:bg-surface-hover transition-all ${className}`}
    >
      <DownloadCloud className="w-3.5 h-3.5 text-accent" />
      <span className="hidden sm:inline">Çevrimdışı İndir</span>
    </button>
  );
};
