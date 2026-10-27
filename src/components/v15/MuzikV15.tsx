import React, { useEffect, useState } from 'react';
import { Headphones, ListMusic, Pause, Play, Plus, SkipBack, SkipForward, Timer, Trash2 } from 'lucide-react';
import { isDirectAudio, parseYouTube, useMusicPlayer, type MusicTrack } from '../music/MusicPlayerContext';
import { useV15Baslik } from './baslik';
import { useCd } from '../canliDers/canliDersStore';
import '../../styles/v15/ogren.css';
import '../../styles/v15/dersler.css';
import '../../styles/v15/liste2.css';

/**
 * v15 · Çalışma müziği (tasarım B22 b2muzik). Çalar kartı (kapak, parça, ilerleme, önceki/oynat/sonraki) + süre çipleri
 * (25 dk · 45 dk · Ders bitene kadar: süre dolunca ya da sesli ders bitince müzik durur) + liste. Çalma motoru ve
 * hesaba kayıt MusicPlayerContext'te (sayfa değişince çalmaya devam eder); bu ekran yalnız yapı.
 */
const fmt = (s: number) => (Number.isFinite(s) && s > 0 ? `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, '0')}` : '0:00');
type Sure = 25 | 45 | 'ders' | null;
let bitis: { t: number; sure: Sure } = { t: 0, sure: null };

export default function MuzikV15() {
  const m = useMusicPlayer();
  const [liste, setListe] = useState<'all' | 'mine' | 'picks'>('all');
  const [url, setUrl] = useState('');
  const [ad, setAd] = useState('');
  const [hata, setHata] = useState('');
  const [sure, setSure0] = useState<Sure>(bitis.sure);
  const [, tik] = useState(0);
  useV15Baslik({ baslik: 'Çalışma müziği', alt: 'Odak için sözsüz listeler' });

  const setSure = (s: Sure) => { bitis = { sure: s, t: typeof s === 'number' ? Date.now() + s * 60000 : 0 }; setSure0(s); };
  // süre dolunca müzik durur; "Ders bitene kadar": sesli ders sesi bitince (ended) durur
  useEffect(() => {
    if (!sure) return;
    const id = window.setInterval(() => {
      tik((n) => n + 1);
      if (typeof sure === 'number' && Date.now() >= bitis.t) { if (m.playing) m.toggle(); setSure(null); }
    }, 1000);
    return () => window.clearInterval(id);
  }, [sure, m.playing]);
  // "Ders bitene kadar": çalan sesli ders sona erince müzik durur
  const cdBitti = useCd((s) => !!s.key && !s.playing && s.dur > 0 && s.t >= s.dur - 1);
  useEffect(() => { if (sure === 'ders' && cdBitti) { if (m.playing) m.toggle(); setSure(null); } }, [cdBitti, sure]);

  const ekle = () => {
    const u = url.trim();
    const p = parseYouTube(u);
    if (!u || (!p && !isDirectAudio(u))) { setHata('Bu bağlantı anlaşılamadı. YouTube paylaşım linkini ya da doğrudan .mp3 linkini yapıştır.'); return; }
    const t: MusicTrack = { id: `ozel-${Date.now().toString(36)}`, title: ad.trim() || 'İsimsiz parça', artist: 'Senin listen', url: u, videoId: p && 'videoId' in p ? p.videoId || undefined : undefined, listId: p && 'listId' in p ? p.listId : undefined, custom: true };
    m.addTrack(t); setUrl(''); setAd(''); setHata('');
  };
  const benim = m.tracks.filter((t) => t.custom).length;
  const goster = m.tracks.map((t, i) => ({ t, i })).filter(({ t }) => liste === 'all' || (liste === 'mine' ? t.custom : !t.custom));
  const yuzde = m.dur > 0 ? Math.min(100, (m.cur / m.dur) * 100) : 0;
  const kalanDk = typeof sure === 'number' ? Math.max(0, Math.ceil((bitis.t - Date.now()) / 60000)) : null;

  return (
    <div className="b15 l2-cols">
      <h1 className="sr-only">Çalışma müziği</h1>
      <section className="v15-card mz15-calar">
        <span className="mz15-kapak" aria-hidden><Headphones /></span>
        <b className="mz15-ad">{m.current?.title || 'Parça seçilmedi'}</b>
        <span className="v15-cap">{m.current ? `${m.current.custom ? 'Senin listen' : m.current.artist || 'Seçki'}${kalanDk != null ? ` · ${kalanDk} dk kaldı` : sure === 'ders' ? ' · ders bitene kadar' : ''}` : 'Listeden bir parça seç'}</span>
        <input type="range" className="mz15-ilerleme" min={0} max={Math.max(1, Math.floor(m.dur))} value={Math.floor(Math.min(m.cur, m.dur || 0))} onChange={(e) => m.seek(Number(e.target.value))} disabled={!m.current} aria-label="Parça konumu" style={{ '--p': `${yuzde}%` } as React.CSSProperties} />
        <div className="mz15-zaman"><span>{fmt(m.cur)}</span><span>{fmt(m.dur)}</span></div>
        <div className="mz15-dug">
          <button type="button" className="v15-ib" onClick={m.prev} disabled={m.tracks.length < 2} aria-label="Önceki parça"><SkipBack aria-hidden /></button>
          <button type="button" className="v15-ib mz15-pl" onClick={m.toggle} disabled={!m.current} aria-label={m.playing ? 'Duraklat' : 'Oynat'}>{m.playing ? <Pause aria-hidden /> : <Play aria-hidden />}</button>
          <button type="button" className="v15-ib" onClick={m.next} disabled={m.tracks.length < 2} aria-label="Sonraki parça"><SkipForward aria-hidden /></button>
        </div>
        <div className="o15-cipler mz15-sure" role="group" aria-label="Çalma süresi">
          <Timer aria-hidden />
          {([[25, '25 dk'], [45, '45 dk'], ['ders', 'Ders bitene kadar']] as [Sure, string][]).map(([s, t]) => (
            <button key={String(s)} type="button" className={`o15-cip${sure === s ? ' is-on' : ''}`} aria-pressed={sure === s} onClick={() => setSure(sure === s ? null : s)}>{t}</button>
          ))}
        </div>
      </section>

      <div className="l2-yan">
        <div className="v15-seg" role="tablist" aria-label="Liste">
          {([['all', `Tümü (${m.tracks.length})`], ['picks', `Seçki (${m.tracks.length - benim})`], ['mine', `Senin listen (${benim})`]] as const).map(([id, t]) => (
            <button key={id} type="button" role="tab" aria-selected={liste === id} aria-current={liste === id ? 'page' : undefined} onClick={() => setListe(id)}>{t}</button>
          ))}
        </div>
        {goster.length ? (
          <ul className="b15-list v15-card" role="list">
            {goster.map(({ t, i }) => {
              const on = i === m.index;
              return (
                <li key={t.id} className="l2-sat">
                  <button type="button" className="b15-row" onClick={() => (on ? m.toggle() : m.playIndex(i))}>
                    <span className={`v15-tile ${on ? '' : 'is-n'}`}>{on && m.playing ? <Pause aria-hidden /> : t.custom ? <Headphones aria-hidden /> : <ListMusic aria-hidden />}</span>
                    <span className="b15-row-t"><b>{t.title}</b><span>{t.custom ? 'Senin listen' : t.artist || 'Seçki'}{/youtu/.test(t.url) ? ' · YouTube' : ' · Ses'}</span></span>
                    {on && <span className="v15-tag is-a">{m.playing ? 'Çalıyor' : 'Duraklatıldı'}</span>}
                  </button>
                  {t.custom && <button type="button" className="v15-ib l2-sil" onClick={() => m.removeTrack(t.id)} aria-label={`${t.title} parçasını çıkar`}><Trash2 aria-hidden /></button>}
                </li>
              );
            })}
          </ul>
        ) : <p className="b15-bos v15-card">{liste === 'mine' ? 'Henüz parça eklemedin. Aşağıya bir YouTube bağlantısı yapıştır.' : 'Liste boş.'}</p>}
        <form className="v15-card mz15-ekle" onSubmit={(e) => { e.preventDefault(); ekle(); }}>
          <b>Listene ekle</b>
          <input value={url} onChange={(e) => setUrl(e.target.value)} placeholder="YouTube ya da .mp3 bağlantısı" inputMode="url" aria-label="Parça bağlantısı" />
          <input value={ad} onChange={(e) => setAd(e.target.value)} placeholder="Parça adı (isteğe bağlı)" aria-label="Parça adı" />
          {hata && <p role="alert" className="mz15-hata">{hata}</p>}
          <button type="submit" className="v15-btn"><Plus aria-hidden /> Ekle</button>
        </form>
      </div>
    </div>
  );
}
