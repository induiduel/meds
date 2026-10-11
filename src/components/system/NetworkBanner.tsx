import React, { useEffect, useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { WifiOff, Wifi, CloudUpload, RefreshCw } from 'lucide-react';
import { useNetState, type NetState } from '../../services/net';
import { offlineDatabaseService } from '../../services/offlineDatabaseService';
import './system.css';

/**
 * Bağlantı şeridi: ağ zayıf ya da yokken ekranın üstünde ince bir kapsül belirir, bekleyen işlem sayısını
 * gösterir ve "Şimdi dene" ile kuyruğu boşaltır. Bağlantı dönünce kısa bir "geri geldi" onayıyla kaybolur.
 * Kendi köküne bağlanır (App'ten bağımsız) → her ekranda, tam ekran derslerde bile görünür.
 */
const NetworkBanner: React.FC = () => {
  const net = useNetState();
  const [queued, setQueued] = useState(offlineDatabaseService.getState().queuedActionsCount);
  const [flash, setFlash] = useState(false);
  const [busy, setBusy] = useState(false);
  const prev = useRef<NetState>(net);

  useEffect(() => offlineDatabaseService.subscribe((s) => setQueued(s.queuedActionsCount)), []);
  useEffect(() => {
    if (prev.current !== 'online' && net === 'online') {
      setFlash(true);
      const t = window.setTimeout(() => setFlash(false), 2200);
      prev.current = net;
      return () => window.clearTimeout(t);
    }
    prev.current = net;
  }, [net]);

  const retry = async () => {
    if (busy) return;
    setBusy(true);
    try {
      await offlineDatabaseService.syncOfflineQueue();
    } finally {
      setBusy(false);
    }
  };

  const visible = net !== 'online' || flash || (queued > 0 && net === 'online');
  const kind = net === 'offline' ? 'is-off' : net === 'slow' ? 'is-slow' : 'is-ok';
  const Icon = net === 'offline' ? WifiOff : net === 'slow' ? Wifi : queued > 0 ? CloudUpload : Wifi;
  const text =
    net === 'offline'
      ? 'Çevrimdışısın'
      : net === 'slow'
        ? 'Bağlantı zayıf'
        : queued > 0
          ? 'Bekleyen işlemler gönderiliyor'
          : 'Bağlantı geri geldi';

  return (
    <div className={`nb-wrap ${visible ? 'is-in' : ''}`} aria-live="polite" role="status">
      {visible && (
        <div className={`nb-pill ${kind}`}>
          <span className="nb-ico"><Icon aria-hidden /></span>
          <span className="nb-t">{text}</span>
          {queued > 0 && <span className="nb-q" title="Sırada bekleyen işlem">{queued} sırada</span>}
          {queued > 0 && net !== 'offline' && (
            <button type="button" className={`nb-btn ${busy ? 'is-busy' : ''}`} onClick={retry} aria-label="Bekleyen işlemleri şimdi gönder">
              <RefreshCw aria-hidden />
            </button>
          )}
        </div>
      )}
    </div>
  );
};

let mounted = false;
export function installNetworkBanner() {
  if (mounted || typeof document === 'undefined') return;
  mounted = true;
  const host = document.createElement('div');
  host.id = 'net-banner-root';
  document.body.appendChild(host);
  createRoot(host).render(<NetworkBanner />);
}
