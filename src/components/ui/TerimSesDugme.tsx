import React, { useEffect, useRef, useState } from 'react';
import { Volume2 } from 'lucide-react';
import { getCustomApiUrl } from '../../services/api';
import '../../styles/terimSes.css';

/** Terim / kısaltma / bilgi paketini hazır EMA sesiyle okutur (/api/terim-ses). Klip yoksa düğme kendini gizler. */
let calan: HTMLAudioElement | null = null;
let calanKapat: (() => void) | null = null;

export function TerimSesDugme({ baslik, govde, className }: { baslik: string; govde: string; className?: string }) {
  const [durum, setDurum] = useState<'bos' | 'caliyor' | 'yok'>('bos');
  const ref = useRef<HTMLAudioElement | null>(null);
  useEffect(() => () => { if (ref.current && calan === ref.current) { ref.current.pause(); calan = null; } }, []);
  if (!baslik || !govde || durum === 'yok') return null;
  const tikla = (e: React.MouseEvent) => {
    e.stopPropagation(); e.preventDefault();
    if (durum === 'caliyor') { ref.current?.pause(); setDurum('bos'); calan = null; return; }
    calan?.pause(); calanKapat?.();
    const base = (getCustomApiUrl() || '').replace(/\/$/, '');
    const a = new Audio(`${base}/api/terim-ses?b=${encodeURIComponent(baslik)}&g=${encodeURIComponent(govde)}`);
    ref.current = a; calan = a; calanKapat = () => setDurum('bos');
    a.onended = () => setDurum('bos');
    a.onerror = () => setDurum('yok');
    setDurum('caliyor');
    a.play().catch(() => setDurum((d) => (d === 'caliyor' ? 'bos' : d)));
  };
  return (
    <button type="button" className={`terim-ses${durum === 'caliyor' ? ' is-on' : ''}${className ? ' ' + className : ''}`} onClick={tikla}
      aria-pressed={durum === 'caliyor'} aria-label={`${baslik} — sesli oku`} title="Sesli oku">
      <Volume2 aria-hidden />
    </button>
  );
}
