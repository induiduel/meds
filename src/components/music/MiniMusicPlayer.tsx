import React from 'react';
import { Music, Pause, Play, SkipForward, X } from 'lucide-react';
import { useMusicPlayer } from './MusicPlayerContext';

/** Müzik sayfası dışındaki sayfalarda çalan parçayı gösteren küçük çalar. */
export const MiniMusicPlayer: React.FC<{ onOpen: () => void }> = ({ onOpen }) => {
  const { current, playing, started, cur, dur, toggle, next, stop, tracks } = useMusicPlayer();
  if (!started || !current) return null;
  const progress = dur > 0 ? Math.min(100, (cur / dur) * 100) : 0;

  return (
    <div
      className="ms-hide-on-kb fixed z-[45] left-3 right-[84px] bottom-[calc(76px+env(safe-area-inset-bottom))] md:right-auto md:left-[92px] lg:left-[248px] md:bottom-4 md:w-[340px] bg-white/95 backdrop-blur border border-line rounded-2xl shadow-lg overflow-hidden print:hidden"
      role="region"
      aria-label="Müzik çalar"
    >
      <div className="flex items-center gap-2 pl-2 pr-1.5 py-1.5">
        <button
          type="button"
          onClick={onOpen}
          className="flex items-center gap-2.5 flex-1 min-w-0 text-left cursor-pointer rounded-xl p-1 hover:bg-canvas"
          aria-label="Müzik sayfasını aç"
        >
          <span className={`w-9 h-9 rounded-xl flex items-center justify-center shrink-0 ${playing ? 'bg-accent text-white' : 'bg-canvas text-ink-2'}`}>
            <Music className="w-4.5 h-4.5" />
          </span>
          <span className="min-w-0">
            <span className="block text-[13.5px] font-semibold text-ink truncate">{current.title}</span>
            <span className="block text-[12px] text-ink-3 truncate">{playing ? 'Çalıyor' : 'Duraklatıldı'} · {current.artist || 'Admin seçkisi'}</span>
          </span>
        </button>
        <button
          type="button"
          onClick={toggle}
          aria-label={playing ? 'Duraklat' : 'Oynat'}
          className="w-10 h-10 rounded-full bg-accent hover:bg-accent-hover text-white flex items-center justify-center shrink-0 cursor-pointer"
        >
          {playing ? <Pause className="w-4.5 h-4.5" /> : <Play className="w-4.5 h-4.5 ml-0.5" />}
        </button>
        {tracks.length > 1 && (
          <button
            type="button"
            onClick={next}
            aria-label="Sonraki parça"
            className="w-9 h-9 rounded-full hidden sm:flex items-center justify-center text-ink-2 hover:text-ink hover:bg-canvas shrink-0 cursor-pointer"
          >
            <SkipForward className="w-4.5 h-4.5" />
          </button>
        )}
        <button
          type="button"
          onClick={stop}
          aria-label="Çaları kapat"
          className="w-8 h-8 rounded-full flex items-center justify-center text-ink-3 hover:text-ink hover:bg-canvas shrink-0 cursor-pointer"
        >
          <X className="w-4 h-4" />
        </button>
      </div>
      <div className="h-[3px] bg-line-soft" aria-hidden="true">
        <div className="h-full bg-accent transition-[width] duration-500" style={{ width: `${progress}%` }} />
      </div>
    </div>
  );
};
