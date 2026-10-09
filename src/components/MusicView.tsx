import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  Music,
  Play,
  Pause,
  SkipBack,
  SkipForward,
  Volume2,
  VolumeX,
  ExternalLink,
  Plus,
  Trash2,
  ListMusic,
  Headphones,
  Info,
} from 'lucide-react';
import { PageHeader } from './ui/PageHeader';
import BUNDLED from '../data/musicTracks.json';

export interface MusicTrack {
  id: string;
  title: string;
  artist?: string;
  url: string;
  videoId?: string;
  listId?: string;
  custom?: boolean;
}

interface BundledTrack {
  id: string;
  title: string;
  artist?: string;
  url: string;
  videoId?: string;
  listId?: string;
}

const CUSTOM_KEY = 'medsoru_music_custom_v1';

declare global {
  interface Window {
    YT?: any;
    onYouTubeIframeAPIReady?: () => void;
  }
}

/** Normal paylaşım / embed / shorts / watch linklerinden videoId + listId çıkarır. */
export function parseYouTube(input: string): { videoId: string; listId?: string } | null {
  const raw = (input || '').trim();
  if (!raw) return null;
  if (/^[A-Za-z0-9_-]{11}$/.test(raw)) return { videoId: raw };
  // iframe embed kodu yapıştırılırsa içindeki src'yi bul
  const srcMatch = raw.match(/src="([^"]+)"/i);
  const candidate = srcMatch ? srcMatch[1] : raw;
  let url: URL | null = null;
  try {
    url = new URL(candidate.startsWith('http') ? candidate : `https://${candidate}`);
  } catch {
    return null;
  }
  const host = url.hostname.replace(/^www\./, '').toLowerCase();
  const listId = url.searchParams.get('list') || undefined;
  const getId = (v: string | null) =>
    v && /^[A-Za-z0-9_-]{11}$/.test(v) ? v : null;

  if (host === 'youtu.be') {
    const id = getId(url.pathname.split('/').filter(Boolean)[0] || null);
    return id ? { videoId: id, listId } : null;
  }
  if (host.endsWith('youtube.com') || host.endsWith('youtube-nocookie.com') || host === 'music.youtube.com') {
    const path = url.pathname;
    const v = getId(url.searchParams.get('v'));
    if (v) return { videoId: v, listId };
    for (const prefix of ['/embed/', '/shorts/', '/live/', '/v/']) {
      if (path.startsWith(prefix)) {
        const id = getId(path.slice(prefix.length).split('/')[0] || null);
        if (id) return { videoId: id, listId };
      }
    }
  }
  return null;
}

const isDirectAudio = (url: string) => /\.(mp3|m4a|aac|ogg|oga|wav|opus|flac)(\?|#|$)/i.test(url);

const fmt = (s: number) => {
  if (!Number.isFinite(s) || s < 0) return '0:00';
  const m = Math.floor(s / 60);
  const sec = Math.floor(s % 60);
  return `${m}:${String(sec).padStart(2, '0')}`;
};

const loadCustom = (): MusicTrack[] => {
  try {
    const raw = localStorage.getItem(CUSTOM_KEY);
    if (!raw) return [];
    const arr = JSON.parse(raw);
    if (!Array.isArray(arr)) return [];
    return arr.filter((t) => t && typeof t.url === 'string' && typeof t.title === 'string');
  } catch {
    return [];
  }
};

export const MusicView: React.FC<{ isAdmin: boolean }> = ({ isAdmin }) => {
  const [custom, setCustom] = useState<MusicTrack[]>(() => loadCustom());
  const [index, setIndex] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [apiReady, setApiReady] = useState(() => !!window.YT?.Player);
  const [cur, setCur] = useState(0);
  const [dur, setDur] = useState(0);
  const [volume, setVolume] = useState(80);
  const [muted, setMuted] = useState(false);
  const [formTitle, setFormTitle] = useState('');
  const [formUrl, setFormUrl] = useState('');
  const [formError, setFormError] = useState('');

  const tracks: MusicTrack[] = useMemo(() => {
    const base = (BUNDLED as BundledTrack[]).map((t) => ({ ...t, custom: false as const }));
    return [...base, ...custom];
  }, [custom]);

  const safeIndex = tracks.length === 0 ? 0 : Math.min(index, tracks.length - 1);
  const current = tracks[safeIndex];
  const yt = current && !isDirectAudio(current.url) ? parseYouTube(current.url) : null;
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const playerRef = useRef<any>(null);
  const playerElRef = useRef<HTMLDivElement | null>(null);
  const holderRef = useRef<HTMLDivElement | null>(null);

  // YouTube IFrame API'yi bir kez yükle
  useEffect(() => {
    if (window.YT?.Player) {
      setApiReady(true);
      return;
    }
    const prev = window.onYouTubeIframeAPIReady;
    window.onYouTubeIframeAPIReady = () => {
      prev?.();
      setApiReady(true);
    };
    const existing = document.querySelector('script[data-yt-api]');
    if (!existing) {
      const s = document.createElement('script');
      s.src = 'https://www.youtube.com/iframe_api';
      s.async = true;
      s.setAttribute('data-yt-api', '1');
      document.head.appendChild(s);
    }
  }, []);

  // Oynatıcıyı kur / parça değişiminde videoyu yükle
  useEffect(() => {
    if (!apiReady || !yt || !playerElRef.current) return;
    if (playerRef.current?.loadVideoById) {
      try {
        playerRef.current.loadVideoById({ videoId: yt.videoId });
      } catch {
        /* eski oyuncu; yeniden kurulur */
        try { playerRef.current?.destroy?.(); } catch { /* yoksay */ }
        playerRef.current = null;
      }
      if (playerRef.current) return;
    }
    try {
      playerRef.current = new window.YT.Player(playerElRef.current, {
        height: '2',
        width: '2',
        videoId: yt.videoId,
        playerVars: {
          autoplay: 0,
          controls: 0,
          disablekb: 1,
          fs: 0,
          iv_load_policy: 3,
          modestbranding: 1,
          playsinline: 1,
          rel: 0,
        },
        events: {
          onReady: (e: any) => {
            try {
              setDur(Number(e.target.getDuration?.() || 0));
              e.target.setVolume?.(volume);
            } catch { /* yoksay */ }
          },
          onStateChange: (e: any) => {
            const S = window.YT?.PlayerState;
            if (!S) return;
            if (e.data === S.PLAYING) setPlaying(true);
            else if (e.data === S.PAUSED || e.data === S.CUED) setPlaying(false);
            else if (e.data === S.ENDED) {
              setPlaying(false);
              setIndex((i) => (tracks.length > 1 ? (i + 1) % tracks.length : i));
            }
            try {
              setDur(Number(e.target.getDuration?.() || 0));
            } catch { /* yoksay */ }
          },
        },
      });
    } catch {
      /* API henüz hazır değilse bir sonraki denemede kurulur */
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [apiReady, current?.id]);

  // Süreyi yokla (oynatıcı hazır olunca)
  useEffect(() => {
    const t = window.setInterval(() => {
      const p = playerRef.current;
      if (p?.getCurrentTime && typeof p.getPlayerState === 'function') {
        try {
          const st = p.getPlayerState();
          if (st === window.YT?.PlayerState?.PLAYING) {
            setPlaying(true);
            setCur(Number(p.getCurrentTime() || 0));
            const d = Number(p.getDuration?.() || 0);
            if (d > 0) setDur(d);
          }
        } catch { /* yoksay */ }
      }
    }, 500);
    return () => window.clearInterval(t);
  }, []);

  // Parça değişince sayaçları sıfırla
  useEffect(() => {
    setCur(0);
    setPlaying(false);
    audioRef.current?.pause();
  }, [current?.id]);

  const toggle = useCallback(() => {
    if (!current) return;
    if (yt) {
      const p = playerRef.current;
      if (!p?.playVideo) return;
      try {
        const st = p.getPlayerState?.();
        if (st === window.YT?.PlayerState?.PLAYING) p.pauseVideo();
        else p.playVideo();
      } catch { /* yoksay */ }
    } else {
      const a = audioRef.current;
      if (!a) return;
      if (a.paused) void a.play().catch(() => {});
      else a.pause();
    }
  }, [current, yt]);

  const next = useCallback(() => {
    if (tracks.length === 0) return;
    setIndex((i) => (i + 1) % tracks.length);
  }, [tracks.length]);

  const prev = useCallback(() => {
    if (tracks.length === 0) return;
    setIndex((i) => (i - 1 + tracks.length) % tracks.length);
  }, [tracks.length]);

  const seek = (v: number) => {
    setCur(v);
    try {
      playerRef.current?.seekTo?.(v, true);
    } catch { /* yoksay */ }
    const a = audioRef.current;
    if (a && Number.isFinite(v)) a.currentTime = v;
  };

  const changeVolume = (v: number) => {
    setVolume(v);
    setMuted(v === 0);
    try {
      playerRef.current?.setVolume?.(v);
      if (v > 0) playerRef.current?.unMute?.();
    } catch { /* yoksay */ }
    if (audioRef.current) audioRef.current.volume = v / 100;
  };

  const toggleMute = () => {
    const nextMuted = !muted;
    setMuted(nextMuted);
    try {
      if (nextMuted) playerRef.current?.mute?.();
      else playerRef.current?.unMute?.();
    } catch { /* yoksay */ }
    if (audioRef.current) audioRef.current.muted = nextMuted;
  };

  const addTrack = () => {
    const title = formTitle.trim() || 'İsimsiz parça';
    const parsed = parseYouTube(formUrl) || (isDirectAudio(formUrl.trim()) ? { videoId: '' } : null);
    if (!formUrl.trim() || (!parsed && !isDirectAudio(formUrl.trim()))) {
      setFormError('Bu bağlantı anlaşılamadı. YouTube paylaşım linkini (youtu.be / youtube.com) ya da doğrudan .mp3 linkini yapıştır.');
      return;
    }
    const url = formUrl.trim();
    const id = `ozel-${Date.now().toString(36)}`;
    const entry: MusicTrack = {
      id,
      title,
      artist: 'Admin seçkisi',
      url,
      videoId: parsed && 'videoId' in parsed && parsed.videoId ? parsed.videoId : undefined,
      listId: parsed && 'listId' in parsed ? parsed.listId : undefined,
      custom: true,
    };
    const nextList = [...custom, entry];
    setCustom(nextList);
    try {
      localStorage.setItem(CUSTOM_KEY, JSON.stringify(nextList));
    } catch { /* yoksay */ }
    setFormTitle('');
    setFormUrl('');
    setFormError('');
    setIndex(tracks.length); // yeni parçaya geç
  };

  const removeTrack = (id: string) => {
    const nextList = custom.filter((t) => t.id !== id);
    setCustom(nextList);
    try {
      localStorage.setItem(CUSTOM_KEY, JSON.stringify(nextList));
    } catch { /* yoksay */ }
    setIndex(0);
  };

  const progress = dur > 0 ? Math.min(100, (cur / dur) * 100) : 0;

  return (
    <div className="w-full flex flex-col gap-3 sm:gap-4 min-w-0">
      <PageHeader
        eyebrow="Topluluk"
        title="Müzik"
        description="Adminin paylaştığı parçalar · yalnızca ses çalar — video gösterilmez, ders çalışırken arka planda dinlenir."
      />

      {/* Ana çalar */}
      <section className="bg-white border border-line rounded-2xl p-4 sm:p-5 flex flex-col gap-4">
        <div className="flex items-center gap-4">
          <span
            aria-hidden="true"
            className={`w-16 h-16 sm:w-20 sm:h-20 rounded-2xl flex items-center justify-center shrink-0 ${
              playing ? 'bg-accent text-white' : 'bg-canvas text-ink-2'
            }`}
          >
            {playing ? <Headphones className="w-8 h-8" /> : <Music className="w-8 h-8" />}
          </span>
          <div className="min-w-0 flex-1">
            <p className="m-0 text-[11px] font-semibold uppercase tracking-[0.08em] text-ink-3">
              {tracks.length === 0 ? 'Liste boş' : `Parça ${safeIndex + 1} / ${tracks.length}`}
            </p>
            <h2 className="m-0 font-display font-bold text-[19px] sm:text-[22px] tracking-[-0.02em] text-ink truncate">
              {current?.title || 'Henüz parça eklenmedi'}
            </h2>
            <p className="m-0 text-[13.5px] text-ink-2 truncate">{current?.artist || 'Admin seçkisi'}</p>
            {playing && (
              <span className="mt-1.5 flex items-end gap-1 h-4" aria-hidden="true">
                {[0, 1, 2, 3].map((i) => (
                  <span
                    key={i}
                    className="w-1 rounded-full bg-accent ms-eq-bar"
                    style={{ animationDelay: `${i * 0.18}s` }}
                  />
                ))}
              </span>
            )}
          </div>
          {current && (
            <a
              href={current.url}
              target="_blank"
              rel="noopener noreferrer"
              className="h-10 px-3 rounded-[10px] border border-line-2 text-ink font-semibold text-[13.5px] hidden sm:inline-flex items-center gap-1.5 shrink-0"
            >
              YouTube'da aç
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          )}
        </div>

        {/* İlerleme */}
        <div className="flex items-center gap-2.5">
          <span className="font-mono text-[12.5px] text-ink-2 w-10 text-right shrink-0">{fmt(cur)}</span>
          <input
            type="range"
            min={0}
            max={Math.max(1, Math.floor(dur))}
            step={1}
            value={Math.floor(Math.min(cur, dur || 0))}
            onChange={(e) => seek(Number(e.target.value))}
            aria-label="Parça konumu"
            className="flex-1 min-w-0 accent-[var(--accent)] cursor-pointer"
            disabled={!current}
          />
          <span className="font-mono text-[12.5px] text-ink-2 w-10 shrink-0">{fmt(dur)}</span>
        </div>
        <div
          className="h-1.5 rounded-full bg-line-soft overflow-hidden -mt-2"
          aria-hidden="true"
        >
          <div className="h-full rounded-full bg-accent transition-[width]" style={{ width: `${progress}%` }} />
        </div>

        {/* Kontroller */}
        <div className="flex items-center justify-center gap-2">
          <button
            type="button"
            onClick={prev}
            disabled={tracks.length < 2}
            aria-label="Önceki parça"
            className="w-11 h-11 rounded-full flex items-center justify-center text-ink-2 hover:text-ink hover:bg-canvas disabled:opacity-40 cursor-pointer"
          >
            <SkipBack className="w-5 h-5" />
          </button>
          <button
            type="button"
            onClick={toggle}
            disabled={!current}
            aria-label={playing ? 'Duraklat' : 'Oynat'}
            className="w-14 h-14 rounded-full bg-accent hover:bg-accent-hover text-white flex items-center justify-center cursor-pointer shadow-sm disabled:opacity-50"
          >
            {playing ? <Pause className="w-6 h-6" /> : <Play className="w-6 h-6 ml-0.5" />}
          </button>
          <button
            type="button"
            onClick={next}
            disabled={tracks.length < 2}
            aria-label="Sonraki parça"
            className="w-11 h-11 rounded-full flex items-center justify-center text-ink-2 hover:text-ink hover:bg-canvas disabled:opacity-40 cursor-pointer"
          >
            <SkipForward className="w-5 h-5" />
          </button>
        </div>

        {/* Ses */}
        <div className="flex items-center gap-2.5">
          <button
            type="button"
            onClick={toggleMute}
            aria-label={muted ? 'Sesi aç' : 'Sessize al'}
            className="w-9 h-9 rounded-lg flex items-center justify-center text-ink-2 hover:text-ink hover:bg-canvas cursor-pointer shrink-0"
          >
            {muted || volume === 0 ? <VolumeX className="w-4.5 h-4.5" /> : <Volume2 className="w-4.5 h-4.5" />}
          </button>
          <input
            type="range"
            min={0}
            max={100}
            value={muted ? 0 : volume}
            onChange={(e) => changeVolume(Number(e.target.value))}
            aria-label="Ses düzeyi"
            className="w-36 sm:w-44 accent-[var(--accent)] cursor-pointer"
          />
          <span className="font-mono text-[12.5px] text-ink-3">%{muted ? 0 : volume}</span>
        </div>

        {/* Gizli video kutusu: ses buradan gelir, görüntü gösterilmez */}
        <div ref={holderRef} aria-hidden="true" className="relative w-[2px] h-[2px] overflow-hidden opacity-0 pointer-events-none select-none">
          {yt && <div ref={playerElRef} />}
        </div>
        {!yt && current && (
          <audio
            ref={audioRef}
            src={current.url}
            preload="metadata"
            onPlay={() => setPlaying(true)}
            onPause={() => setPlaying(false)}
            onTimeUpdate={(e) => {
              const a = e.currentTarget;
              setCur(a.currentTime || 0);
              if (Number.isFinite(a.duration) && a.duration > 0) setDur(a.duration);
            }}
            onLoadedMetadata={(e) => {
              const a = e.currentTarget;
              if (Number.isFinite(a.duration)) setDur(a.duration);
            }}
            onEnded={next}
            className="w-full"
            controls={false}
          />
        )}
      </section>

      {/* Liste */}
      <section className="bg-white border border-line rounded-2xl overflow-hidden">
        <div className="flex items-center gap-2 px-4 py-3 border-b border-line-soft">
          <ListMusic className="w-4 h-4 text-ink-3 shrink-0" />
          <h3 className="m-0 flex-1 text-[15px] font-semibold text-ink">Çalma listesi</h3>
          <span className="text-[12.5px] text-ink-3">{tracks.length} parça</span>
        </div>
        {tracks.length === 0 ? (
          <p className="m-0 px-4 py-8 text-center text-[14px] text-ink-3">
            Liste boş. Yönetici ilk parçayı ekleyince burada görünür.
          </p>
        ) : (
          <ol className="list-none m-0 p-0">
            {tracks.map((t, i) => {
              const on = i === safeIndex;
              return (
                <li key={t.id} className={`flex items-center gap-3 px-3 sm:px-4 py-2.5 border-b border-line-soft last:border-b-0 ${on ? 'bg-accent-soft/60' : ''}`}>
                  <button
                    type="button"
                    onClick={() => setIndex(i)}
                    aria-label={`${t.title} parçasını çal`}
                    className={`w-10 h-10 rounded-xl flex items-center justify-center shrink-0 cursor-pointer ${
                      on ? 'bg-accent text-white' : 'bg-canvas text-ink-2 hover:text-ink'
                    }`}
                  >
                    {on && playing ? <Pause className="w-4.5 h-4.5" /> : <Play className="w-4.5 h-4.5 ml-0.5" />}
                  </button>
                  <span className="flex-1 min-w-0">
                    <span className={`block text-[14.5px] font-semibold truncate ${on ? 'text-accent' : 'text-ink'}`}>{t.title}</span>
                    <span className="block text-[12.5px] text-ink-3 truncate">{t.artist || 'Admin seçkisi'}</span>
                  </span>
                  <a
                    href={t.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    aria-label={`${t.title} bağlantısını yeni sekmede aç`}
                    className="w-9 h-9 rounded-lg hidden sm:flex items-center justify-center text-ink-3 hover:text-ink hover:bg-canvas shrink-0"
                  >
                    <ExternalLink className="w-4 h-4" />
                  </a>
                  {isAdmin && t.custom && (
                    <button
                      type="button"
                      onClick={() => removeTrack(t.id)}
                      aria-label={`${t.title} parçasını sil`}
                      className="w-9 h-9 rounded-lg flex items-center justify-center text-ink-3 hover:text-red-600 hover:bg-red-50 cursor-pointer shrink-0"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  )}
                </li>
              );
            })}
          </ol>
        )}
      </section>

      {/* Yönetici ekleme */}
      {isAdmin ? (
        <section className="bg-white border border-line rounded-2xl p-4 sm:p-5 flex flex-col gap-3">
          <h3 className="m-0 text-[15px] font-semibold text-ink flex items-center gap-2">
            <Plus className="w-4 h-4" />
            Yeni parça ekle (yönetici)
          </h3>
          <div className="grid sm:grid-cols-[1fr_2fr_auto] gap-2">
            <label className="flex flex-col gap-1 min-w-0">
              <span className="text-[12.5px] font-medium text-ink-2">Parça adı</span>
              <input
                value={formTitle}
                onChange={(e) => setFormTitle(e.target.value)}
                placeholder="Örn. Ahu Figan Dilber (Trap)"
                className="h-11 rounded-xl bg-canvas border border-line px-3 text-[14px] text-ink outline-none focus:border-accent"
              />
            </label>
            <label className="flex flex-col gap-1 min-w-0">
              <span className="text-[12.5px] font-medium text-ink-2">YouTube / ses bağlantısı</span>
              <input
                value={formUrl}
                onChange={(e) => setFormUrl(e.target.value)}
                placeholder="https://youtu.be/…  ya da  https://…/parca.mp3"
                inputMode="url"
                className="h-11 rounded-xl bg-canvas border border-line px-3 text-[14px] text-ink outline-none focus:border-accent"
              />
            </label>
            <span className="flex items-end">
              <button
                type="button"
                onClick={addTrack}
                className="h-11 px-5 rounded-xl bg-accent hover:bg-accent-hover text-white font-semibold text-[14.5px] cursor-pointer whitespace-nowrap"
              >
                Ekle
              </button>
            </span>
          </div>
          {formError && <p role="alert" className="m-0 text-[13.5px] text-red-600">{formError}</p>}
          <p className="m-0 text-[13px] text-ink-2 leading-relaxed flex gap-1.5">
            <Info className="w-4 h-4 shrink-0 mt-0.5 text-ink-3" />
            <span>Yerleştirme (embed / iframe) koduna gerek yok — normal YouTube paylaşım linkini yapıştırman yeterli, uygulama otomatik çözer (youtu.be, youtube.com/watch, /embed/, /shorts, liste parametresi dahil). Doğrudan .mp3 bağlantıları da çalınır.</span>
          </p>
        </section>
      ) : (
        <p className="m-0 text-[13px] text-ink-3 leading-relaxed">
          Yeni parça önerin varsa yöneticiye YouTube bağlantısını göndermen yeterli — yerleştirme kodu gerekmez.
        </p>
      )}
    </div>
  );
};
