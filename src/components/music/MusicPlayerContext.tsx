import React, { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from 'react';
import BUNDLED from '../../data/musicTracks.json';

/*
 * Uygulama genelinde tek müzik çalar. Sağlayıcı App kökünde durduğu için sayfa
 * değişince çalma kesilmez; Media Session API ile bildirim / kilit ekranı /
 * kulaklık tuşlarından kontrol edilir.
 */

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
const VOLUME_KEY = 'medsoru_music_volume_v1';

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

export const isDirectAudio = (url: string) => /\.(mp3|m4a|aac|ogg|oga|wav|opus|flac)(\?|#|$)/i.test(url);

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

const saveCustom = (list: MusicTrack[]) => {
  try {
    localStorage.setItem(CUSTOM_KEY, JSON.stringify(list));
  } catch { /* yoksay */ }
};

const loadVolume = () => {
  try {
    const v = Number(localStorage.getItem(VOLUME_KEY));
    return Number.isFinite(v) && v >= 0 && v <= 100 && localStorage.getItem(VOLUME_KEY) !== null ? v : 80;
  } catch {
    return 80;
  }
};

/*
 * YouTube sesi çapraz kaynaklı iframe'den gelir; tarayıcı bildirimi üst çerçeveye
 * bağlamaz. Üst çerçevede sessiz bir ses döngüsü çalarak medya oturumunu
 * sahipleniriz; böylece bildirimdeki başlık ve tuşlar bize gelir.
 */
let silentUrl: string | null = null;
const getSilentUrl = () => {
  if (silentUrl) return silentUrl;
  const rate = 8000;
  const seconds = 20;
  const n = rate * seconds;
  const buf = new ArrayBuffer(44 + n);
  const v = new DataView(buf);
  const w = (o: number, s: string) => { for (let i = 0; i < s.length; i++) v.setUint8(o + i, s.charCodeAt(i)); };
  w(0, 'RIFF'); v.setUint32(4, 36 + n, true); w(8, 'WAVE');
  w(12, 'fmt '); v.setUint32(16, 16, true); v.setUint16(20, 1, true); v.setUint16(22, 1, true);
  v.setUint32(24, rate, true); v.setUint32(28, rate, true); v.setUint16(32, 1, true); v.setUint16(34, 8, true);
  w(36, 'data'); v.setUint32(40, n, true);
  new Uint8Array(buf, 44).fill(128); // 8 bit PCM'de sessizlik = 128
  silentUrl = URL.createObjectURL(new Blob([buf], { type: 'audio/wav' }));
  return silentUrl;
};

interface MusicPlayerValue {
  tracks: MusicTrack[];
  custom: MusicTrack[];
  index: number;
  current: MusicTrack | undefined;
  playing: boolean;
  /** Kullanıcı bu oturumda en az bir kez çalmaya başladı mı (mini çaları göstermek için). */
  started: boolean;
  cur: number;
  dur: number;
  volume: number;
  muted: boolean;
  toggle: () => void;
  play: () => void;
  pause: () => void;
  stop: () => void;
  next: () => void;
  prev: () => void;
  playIndex: (i: number) => void;
  seek: (v: number) => void;
  setVolume: (v: number) => void;
  toggleMute: () => void;
  addTrack: (t: MusicTrack) => void;
  removeTrack: (id: string) => void;
}

const MusicPlayerContext = createContext<MusicPlayerValue | null>(null);

export const useMusicPlayer = () => {
  const ctx = useContext(MusicPlayerContext);
  if (!ctx) throw new Error('useMusicPlayer, MusicPlayerProvider içinde kullanılmalı');
  return ctx;
};

export const MusicPlayerProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [custom, setCustom] = useState<MusicTrack[]>(() => loadCustom());
  const [index, setIndex] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [started, setStarted] = useState(false);
  const [apiReady, setApiReady] = useState(() => !!window.YT?.Player);
  const [cur, setCur] = useState(0);
  const [dur, setDur] = useState(0);
  const [volume, setVolumeState] = useState(loadVolume);
  const [muted, setMuted] = useState(false);

  const tracks: MusicTrack[] = useMemo(() => {
    const base = (BUNDLED as BundledTrack[]).map((t) => ({ ...t, custom: false as const }));
    return [...base, ...custom];
  }, [custom]);

  const safeIndex = tracks.length === 0 ? 0 : Math.min(index, tracks.length - 1);
  const current = tracks[safeIndex];
  const yt = current && !isDirectAudio(current.url) ? parseYouTube(current.url) : null;
  const ytVideoId = yt?.videoId;

  const audioRef = useRef<HTMLAudioElement | null>(null);
  const keepAliveRef = useRef<HTMLAudioElement | null>(null);
  const playerRef = useRef<any>(null);
  const playerReadyRef = useRef(false);
  const playerElRef = useRef<HTMLDivElement | null>(null);
  /** Parça değişince otomatik başlasın mı (çalarken geçildiyse ya da listeden seçildiyse). */
  const autoPlayRef = useRef(false);
  const tracksLenRef = useRef(tracks.length);
  tracksLenRef.current = tracks.length;
  const volumeRef = useRef(volume);
  volumeRef.current = volume;

  const startKeepAlive = useCallback(() => {
    const k = keepAliveRef.current;
    if (!k) return;
    if (!k.src) k.src = getSilentUrl();
    if (k.paused) void k.play().catch(() => {});
  }, []);

  const stopKeepAlive = useCallback(() => {
    const k = keepAliveRef.current;
    if (k && !k.paused) k.pause();
  }, []);

  // YouTube IFrame API'yi bir kez yükle
  useEffect(() => {
    if (window.YT?.Player) {
      setApiReady(true);
      return;
    }
    const prevReady = window.onYouTubeIframeAPIReady;
    window.onYouTubeIframeAPIReady = () => {
      prevReady?.();
      setApiReady(true);
    };
    if (!document.querySelector('script[data-yt-api]')) {
      const s = document.createElement('script');
      s.src = 'https://www.youtube.com/iframe_api';
      s.async = true;
      s.setAttribute('data-yt-api', '1');
      document.head.appendChild(s);
    }
  }, []);

  const next = useCallback(() => {
    if (tracksLenRef.current === 0) return;
    autoPlayRef.current = true;
    setIndex((i) => (i + 1) % tracksLenRef.current);
  }, []);

  const prev = useCallback(() => {
    if (tracksLenRef.current === 0) return;
    autoPlayRef.current = true;
    setIndex((i) => (i - 1 + tracksLenRef.current) % tracksLenRef.current);
  }, []);

  // Oynatıcıyı bir kez kur; parça değişiminde yalnızca videoyu değiştir
  useEffect(() => {
    if (!apiReady || !ytVideoId || !playerElRef.current) return;
    const p = playerRef.current;
    if (p && playerReadyRef.current) {
      try {
        if (autoPlayRef.current) p.loadVideoById({ videoId: ytVideoId });
        else p.cueVideoById({ videoId: ytVideoId });
        return;
      } catch {
        try { p.destroy?.(); } catch { /* yoksay */ }
        playerRef.current = null;
        playerReadyRef.current = false;
      }
    }
    if (playerRef.current) return; // kuruluyor; onReady doğru videoyu yükler
    try {
      // YT.Player hedef düğümü iframe ile değiştirir; React'in düğümüne dokunmasın diye ayrı düğüm aç
      const target = document.createElement('div');
      playerElRef.current.replaceChildren(target);
      playerRef.current = new window.YT.Player(target, {
        height: '2',
        width: '2',
        videoId: ytVideoId,
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
            playerReadyRef.current = true;
            try {
              e.target.setVolume?.(volumeRef.current);
              setDur(Number(e.target.getDuration?.() || 0));
              if (autoPlayRef.current) e.target.playVideo?.();
            } catch { /* yoksay */ }
          },
          onStateChange: (e: any) => {
            const S = window.YT?.PlayerState;
            if (!S) return;
            if (e.data === S.PLAYING) {
              setPlaying(true);
              setStarted(true);
              startKeepAlive();
            } else if (e.data === S.PAUSED) {
              setPlaying(false);
              stopKeepAlive();
            } else if (e.data === S.ENDED) {
              if (tracksLenRef.current > 1) next();
              else {
                setPlaying(false);
                stopKeepAlive();
              }
            }
            try {
              const d = Number(e.target.getDuration?.() || 0);
              if (d > 0) setDur(d);
            } catch { /* yoksay */ }
          },
        },
      });
    } catch {
      /* API henüz hazır değilse bir sonraki denemede kurulur */
    }
  }, [apiReady, ytVideoId, current?.id, next, startKeepAlive, stopKeepAlive]);

  // YouTube konumunu yokla
  useEffect(() => {
    const t = window.setInterval(() => {
      const p = playerRef.current;
      if (!playerReadyRef.current || typeof p?.getPlayerState !== 'function') return;
      try {
        if (p.getPlayerState() === window.YT?.PlayerState?.PLAYING) {
          setCur(Number(p.getCurrentTime() || 0));
          const d = Number(p.getDuration?.() || 0);
          if (d > 0) setDur(d);
        }
      } catch { /* yoksay */ }
    }, 500);
    return () => window.clearInterval(t);
  }, []);

  // Parça değişince sayaçları sıfırla; YouTube dışı parçaya geçildiyse videoyu durdur
  useEffect(() => {
    setCur(0);
    setDur(0);
    if (!ytVideoId) {
      try { playerRef.current?.stopVideo?.(); } catch { /* yoksay */ }
      stopKeepAlive();
    }
    if (ytVideoId) audioRef.current?.pause();
    if (!autoPlayRef.current) setPlaying(false);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [current?.id]);

  // Doğrudan ses dosyası: parça değişince otomatik başlat
  useEffect(() => {
    const a = audioRef.current;
    if (!a || ytVideoId || !current) return;
    a.volume = volumeRef.current / 100;
    if (autoPlayRef.current) void a.play().catch(() => setPlaying(false));
  }, [current, ytVideoId]);

  const play = useCallback(() => {
    if (!current) return;
    autoPlayRef.current = true;
    setStarted(true);
    if (ytVideoId) {
      startKeepAlive(); // kullanıcı hareketi içinde başlasın ki tarayıcı izin versin
      try { playerRef.current?.playVideo?.(); } catch { /* yoksay */ }
    } else {
      void audioRef.current?.play().catch(() => {});
    }
  }, [current, ytVideoId, startKeepAlive]);

  const pause = useCallback(() => {
    autoPlayRef.current = false;
    if (ytVideoId) {
      try { playerRef.current?.pauseVideo?.(); } catch { /* yoksay */ }
      stopKeepAlive();
      setPlaying(false);
    } else {
      audioRef.current?.pause();
    }
  }, [ytVideoId, stopKeepAlive]);

  const stop = useCallback(() => {
    pause();
    try { playerRef.current?.seekTo?.(0, true); } catch { /* yoksay */ }
    if (audioRef.current) audioRef.current.currentTime = 0;
    setCur(0);
    setStarted(false);
  }, [pause]);

  const playingRef = useRef(playing);
  playingRef.current = playing;
  const toggle = useCallback(() => {
    if (playingRef.current) pause();
    else play();
  }, [play, pause]);

  const playIndex = useCallback((i: number) => {
    if (i === safeIndex) {
      toggle();
      return;
    }
    autoPlayRef.current = true;
    setStarted(true);
    if (tracks[i] && !isDirectAudio(tracks[i].url)) startKeepAlive();
    setIndex(i);
  }, [safeIndex, toggle, tracks, startKeepAlive]);

  const seek = useCallback((v: number) => {
    if (!Number.isFinite(v)) return;
    setCur(v);
    try { playerRef.current?.seekTo?.(v, true); } catch { /* yoksay */ }
    if (audioRef.current && !ytVideoId) audioRef.current.currentTime = v;
  }, [ytVideoId]);

  const setVolume = useCallback((v: number) => {
    setVolumeState(v);
    setMuted(v === 0);
    try {
      playerRef.current?.setVolume?.(v);
      if (v > 0) playerRef.current?.unMute?.();
    } catch { /* yoksay */ }
    if (audioRef.current) {
      audioRef.current.volume = v / 100;
      audioRef.current.muted = v === 0;
    }
    try { localStorage.setItem(VOLUME_KEY, String(v)); } catch { /* yoksay */ }
  }, []);

  const toggleMute = useCallback(() => {
    setMuted((m) => {
      const nextMuted = !m;
      try {
        if (nextMuted) playerRef.current?.mute?.();
        else playerRef.current?.unMute?.();
      } catch { /* yoksay */ }
      if (audioRef.current) audioRef.current.muted = nextMuted;
      return nextMuted;
    });
  }, []);

  const addTrack = useCallback((t: MusicTrack) => {
    setCustom((list) => {
      const nextList = [...list, t];
      saveCustom(nextList);
      return nextList;
    });
    autoPlayRef.current = false;
    setIndex(tracks.length);
  }, [tracks.length]);

  const removeTrack = useCallback((id: string) => {
    const removingCurrent = current?.id === id;
    setCustom((list) => {
      const nextList = list.filter((t) => t.id !== id);
      saveCustom(nextList);
      return nextList;
    });
    if (removingCurrent) {
      pause();
      setIndex(0);
    }
  }, [current?.id, pause]);

  // ── Media Session: bildirim, kilit ekranı, kulaklık / klavye medya tuşları ──
  useEffect(() => {
    if (!('mediaSession' in navigator)) return;
    const ms = navigator.mediaSession;
    if (!current || !started) {
      ms.metadata = null;
      return;
    }
    const artwork = ytVideoId
      ? [
          { src: `https://i.ytimg.com/vi/${ytVideoId}/mqdefault.jpg`, sizes: '320x180', type: 'image/jpeg' },
          { src: `https://i.ytimg.com/vi/${ytVideoId}/hqdefault.jpg`, sizes: '480x360', type: 'image/jpeg' },
        ]
      : [];
    try {
      ms.metadata = new MediaMetadata({
        title: current.title,
        artist: current.artist || 'Admin seçkisi',
        album: 'MedSoru · Müzik',
        artwork,
      });
    } catch { /* yoksay */ }
  }, [current, started, ytVideoId]);

  useEffect(() => {
    if (!('mediaSession' in navigator)) return;
    navigator.mediaSession.playbackState = !started ? 'none' : playing ? 'playing' : 'paused';
  }, [playing, started]);

  const curRef = useRef(cur);
  curRef.current = cur;
  useEffect(() => {
    if (!('mediaSession' in navigator)) return;
    const ms = navigator.mediaSession;
    const set = (action: MediaSessionAction, handler: MediaSessionActionHandler | null) => {
      try { ms.setActionHandler(action, handler); } catch { /* desteklenmiyor */ }
    };
    set('play', () => play());
    set('pause', () => pause());
    set('stop', () => stop());
    set('nexttrack', tracks.length > 1 ? () => next() : null);
    set('previoustrack', tracks.length > 1 ? () => prev() : null);
    set('seekto', (d) => { if (d.seekTime != null) seek(d.seekTime); });
    set('seekbackward', (d) => seek(Math.max(0, curRef.current - (d.seekOffset || 10))));
    set('seekforward', (d) => seek(curRef.current + (d.seekOffset || 10)));
    return () => {
      (['play', 'pause', 'stop', 'nexttrack', 'previoustrack', 'seekto', 'seekbackward', 'seekforward'] as MediaSessionAction[])
        .forEach((a) => set(a, null));
    };
  }, [play, pause, stop, next, prev, seek, tracks.length]);

  // Bildirimdeki ilerleme çubuğu (saniyede bir yeter)
  const curSec = Math.floor(cur);
  useEffect(() => {
    if (!('mediaSession' in navigator) || !started || !(dur > 0)) return;
    try {
      navigator.mediaSession.setPositionState?.({
        duration: dur,
        playbackRate: 1,
        position: Math.min(curSec, dur),
      });
    } catch { /* yoksay */ }
  }, [curSec, dur, started]);

  const value = useMemo<MusicPlayerValue>(() => ({
    tracks, custom, index: safeIndex, current, playing, started, cur, dur, volume, muted,
    toggle, play, pause, stop, next, prev, playIndex, seek, setVolume, toggleMute, addTrack, removeTrack,
  }), [tracks, custom, safeIndex, current, playing, started, cur, dur, volume, muted,
    toggle, play, pause, stop, next, prev, playIndex, seek, setVolume, toggleMute, addTrack, removeTrack]);

  return (
    <MusicPlayerContext.Provider value={value}>
      {children}
      {/* Gizli video kutusu: ses buradan gelir, görüntü gösterilmez. Kökte durduğu için sayfa geçişlerinde yaşar. */}
      <div ref={playerElRef} aria-hidden="true" className="fixed left-0 bottom-0 w-[2px] h-[2px] overflow-hidden opacity-0 pointer-events-none select-none print:hidden">
      </div>
      <audio
        ref={keepAliveRef}
        loop
        preload="none"
        aria-hidden="true"
        onPause={() => {
          // Kulaklık çıkarılınca vb. tarayıcı sessiz döngüyü durdurursa YouTube'u da durdur
          if (ytVideoId && playingRef.current && autoPlayRef.current) {
            autoPlayRef.current = false;
            try { playerRef.current?.pauseVideo?.(); } catch { /* yoksay */ }
          }
        }}
      />
      {!ytVideoId && current && (
        <audio
          ref={audioRef}
          src={current.url}
          preload="metadata"
          onPlay={() => { setPlaying(true); setStarted(true); }}
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
          onEnded={() => (tracksLenRef.current > 1 ? next() : setPlaying(false))}
        />
      )}
    </MusicPlayerContext.Provider>
  );
};
