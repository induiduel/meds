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
      artist: 'Admin seçkisi',
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

  return (
    <div className="w-full flex flex-col gap-3 sm:gap-4 min-w-0">
      <PageHeader
        eyebrow="Topluluk"
        title="Müzik"
        description="Adminin paylaştığı parçalar · yalnızca ses — başka sayfalara geçince de çalmaya devam eder, bildirimden ve kilit ekranından kontrol edilir."
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
                    onClick={() => playIndex(i)}
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
