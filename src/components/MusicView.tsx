import React, { useState } from 'react';
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
  Check,
} from 'lucide-react';
import { PageHeader } from './ui/PageHeader';
import { isDirectAudio, parseYouTube, useMusicPlayer, type MusicTrack } from './music/MusicPlayerContext';

export { parseYouTube };

const fmt = (s: number) => {
  if (!Number.isFinite(s) || s < 0) return '0:00';
  const m = Math.floor(s / 60);
  const sec = Math.floor(s % 60);
  return `${m}:${String(sec).padStart(2, '0')}`;
};

export const MusicView: React.FC<{ isAdmin: boolean }> = ({ isAdmin }) => {
  const {
    tracks, index: safeIndex, current, playing, cur, dur, volume, muted,
    toggle, next, prev, playIndex, seek, setVolume: changeVolume, toggleMute,
    addTrack: addToPlayer, removeTrack,
  } = useMusicPlayer();
  const [formTitle, setFormTitle] = useState('');
  const [formUrl, setFormUrl] = useState('');
  const [formError, setFormError] = useState('');

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
      artist: 'Senin listen',
      url,
      videoId: parsed && 'videoId' in parsed && parsed.videoId ? parsed.videoId : undefined,
      listId: parsed && 'listId' in parsed ? parsed.listId : undefined,
      custom: true,
    };
    addToPlayer(entry);
    setFormTitle('');
    setFormUrl('');
    setFormError('');
  };

  const progress = dur > 0 ? Math.min(100, (cur / dur) * 100) : 0;
  const [list, setList] = useState<'mine' | 'all' | 'picks'>('all');
  const mine = tracks.filter((t) => t.custom).length;
  const shown = tracks.map((t, i) => ({ t, i })).filter(({ t }) => list === 'all' || (list === 'mine' ? t.custom : !t.custom));

  return (
    <div className="mux">
      <PageHeader
        eyebrow="Topluluk"
        title="Müzik"
        description="Çalışırken dinle. Eklediğin parçalar hesabına kaydedilir; sayfa değişince de çalmaya devam eder."
      />

      <div className="mux-body">
        <aside className="mux-lists" aria-label="Çalma listeleri">
          <span className="mux-cap">ÇALMA LİSTELERİ</span>
          {([['all', 'Tümü', tracks.length], ['mine', 'Senin listen', mine], ['picks', 'Seçki', tracks.length - mine]] as const).map(([id, l, n]) => (
            <button key={id} type="button" className={`mux-list ${list === id ? 'is-on' : ''}`} aria-pressed={list === id} onClick={() => setList(id)}>
              {id === 'mine' ? <Headphones aria-hidden /> : <ListMusic aria-hidden />}
              <span>{l}</span>
              <span className="n">{n}</span>
            </button>
          ))}
        </aside>

        <section className="mux-main" aria-label="Parçalar">
          <div className="mux-h">
            <b>{list === 'mine' ? 'Senin listen' : list === 'picks' ? 'Seçki' : 'Tüm parçalar'}</b>
            <span className="mux-saved"><Check aria-hidden />Hesabına kaydedilir</span>
          </div>
          <form className="mux-add" onSubmit={(e) => { e.preventDefault(); addTrack(); }}>
            <input value={formUrl} onChange={(e) => setFormUrl(e.target.value)} placeholder="YouTube ya da .mp3 bağlantısı yapıştır" inputMode="url" aria-label="Parça bağlantısı" />
            <input value={formTitle} onChange={(e) => setFormTitle(e.target.value)} placeholder="Parça adı (isteğe bağlı)" aria-label="Parça adı" className="is-title" />
            <button type="submit" className="os-btn is-primary"><Plus aria-hidden />Listeye ekle</button>
          </form>
          {formError && <p role="alert" className="mux-err">{formError}</p>}
          {shown.length === 0 ? (
            <p className="mux-empty">{list === 'mine' ? 'Henüz parça eklemedin. Bir YouTube bağlantısı yapıştır.' : 'Liste boş.'}</p>
          ) : (
            <ol className="mux-tracks">
              {shown.map(({ t, i }, n) => {
                const on = i === safeIndex;
                return (
                  <li key={t.id} className={on ? 'is-on' : ''}>
                    <button type="button" className="mux-play" onClick={() => playIndex(i)} aria-label={`${t.title} parçasını ${on && playing ? 'duraklat' : 'çal'}`}>
                      {on && playing ? <Pause aria-hidden /> : <span className="mux-no">{n + 1}</span>}
                    </button>
                    <span className="mux-t">
                      <b>{t.title}</b>
                      <span>{t.custom ? 'Senin listen' : t.artist || 'Seçki'}{/youtu/.test(t.url) ? ' · YouTube' : ' · Ses'}</span>
                    </span>
                    <a href={t.url} target="_blank" rel="noopener noreferrer" className="qk-ib" aria-label={`${t.title} bağlantısını yeni sekmede aç`}><ExternalLink aria-hidden /></a>
                    {t.custom && (
                      <button type="button" className="qk-ib" onClick={() => removeTrack(t.id)} aria-label={`${t.title} parçasını listeden çıkar`}><Trash2 aria-hidden /></button>
                    )}
                  </li>
                );
              })}
            </ol>
          )}
          <p className="mux-tip"><Info aria-hidden />Yerleştirme koduna gerek yok: youtu.be, youtube.com/watch, /shorts ve liste bağlantıları çözülür; doğrudan .mp3 de çalınır.</p>
        </section>
      </div>

      {/* Yapışkan çalar */}
      <div className="mux-player" role="region" aria-label="Çalar">
        <button type="button" onClick={prev} disabled={tracks.length < 2} aria-label="Önceki parça" className="qk-ib"><SkipBack aria-hidden /></button>
        <button type="button" onClick={toggle} disabled={!current} aria-label={playing ? 'Duraklat' : 'Oynat'} className="mux-pp">
          {playing ? <Pause aria-hidden /> : <Play aria-hidden />}
        </button>
        <button type="button" onClick={next} disabled={tracks.length < 2} aria-label="Sonraki parça" className="qk-ib"><SkipForward aria-hidden /></button>
        <span className="mux-now">
          <b>{current?.title || 'Parça seçilmedi'}</b>
          <span>{tracks.length ? `Parça ${safeIndex + 1} / ${tracks.length}` : 'Liste boş'}</span>
        </span>
        <span className="mux-time">{fmt(cur)}</span>
        <input type="range" min={0} max={Math.max(1, Math.floor(dur))} step={1} value={Math.floor(Math.min(cur, dur || 0))} onChange={(e) => seek(Number(e.target.value))} aria-label="Parça konumu" disabled={!current} className="mux-seek" style={{ '--p': `${progress}%` } as React.CSSProperties} />
        <span className="mux-time">{fmt(dur)}</span>
        <button type="button" onClick={toggleMute} aria-label={muted ? 'Sesi aç' : 'Sessize al'} className="qk-ib mux-vol-b">
          {muted || volume === 0 ? <VolumeX aria-hidden /> : <Volume2 aria-hidden />}
        </button>
        <input type="range" min={0} max={100} value={muted ? 0 : volume} onChange={(e) => changeVolume(Number(e.target.value))} aria-label="Ses düzeyi" className="mux-vol" />
      </div>
    </div>
  );
};
