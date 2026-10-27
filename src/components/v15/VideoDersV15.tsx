import React, { useEffect, useMemo, useRef, useState } from 'react';
import { BookOpen, Maximize, Minimize, PictureInPicture2, Play, Video } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { linkClick, navigateTo } from '../../router';
import { useV15Baslik } from './baslik';
import { dersAdi, dersYolu, useDersListesi } from './dersVeri';
import '../../styles/v15/ogren.css';
import '../../styles/v15/video.css';

/**
 * v15 · O01 Video ders, O02 Tam ekran, O03 Resim içinde resim. Adres: /video-ders (?v=<video kimliği>).
 * Videolar yönetici GPU kuyruğunun hazır çıktısıdır (services/dersVideoIs.ts → services/dersVideoOynat.ts);
 * akış 2 saatlik imzalı adresle gelir. Hazır video yoksa ekran boş durum gösterir; giriş kartı (useHazirVideolar)
 * yalnız video varken görünür.
 */
export interface HazirVideo { id: string; key: string; cozunurluk: string; bayt: number; bitti: string }

let onbellek: { t: number; v: HazirVideo[] } | null = null;
export function useHazirVideolar() {
  const [v, setV] = useState<HazirVideo[] | null>(onbellek && Date.now() - onbellek.t < 120_000 ? onbellek.v : null);
  useEffect(() => {
    if (v) return;
    let canli = true;
    void safeJsonFetch<{ videolar: HazirVideo[] }>('/api/ders-video/hazir').then((r) => {
      const l = r.ok ? r.data?.videolar || [] : [];
      onbellek = { t: Date.now(), v: l };
      if (canli) setV(l);
    });
    return () => { canli = false; };
  }, [v]);
  return v;
}

const vParam = () => new URLSearchParams(location.search).get('v');
const mb = (b: number) => (b ? `${(b / 1048576).toFixed(0)} MB` : '');

export default function VideoDersV15() {
  const videolar = useHazirVideolar();
  const { dersler } = useDersListesi();
  const [secili, setSecili0] = useState<string | null>(vParam);
  useEffect(() => { const f = () => setSecili0(vParam()); window.addEventListener('popstate', f); return () => window.removeEventListener('popstate', f); }, []);
  const setSecili = (id: string) => {
    if (id === secili) return;
    try { history.pushState(history.state, '', `${location.pathname}?v=${id}`); } catch { /* yok */ }
    setSecili0(id);
  };
  const ad = (key: string) => { const d = dersler?.find((x) => x.key === key); return d ? dersAdi(d) : key; };
  const brans = (key: string) => dersler?.find((x) => x.key === key)?.brans || 'Sesli ders';
  const aktif = useMemo(() => (videolar || []).find((x) => x.id === secili) || (videolar || [])[0] || null, [videolar, secili]);
  useV15Baslik({ baslik: 'Video ders', alt: aktif ? brans(aktif.key) : `${videolar?.length ?? 0} video`, ...(secili ? { geri: '/video-ders' } : {}) });

  if (videolar == null) return <p className="b15-bos v15-card">Videolar yükleniyor…</p>;
  if (!videolar.length || !aktif) {
    return (
      <div className="v15-card vd15-bos">
        <Video aria-hidden />
        <b>Henüz hazır ders videosu yok</b>
        <p>Sesli derslerin videoları hazırlandıkça burada izlenebilir. O zamana kadar dersleri sesli ders ekranından dinleyebilirsin.</p>
        <a className="v15-btn" href="/dersler" onClick={linkClick(() => navigateTo('/dersler'))}><BookOpen aria-hidden />Derslere git</a>
      </div>
    );
  }
  const siradaki = videolar.filter((x) => x.id !== aktif.id);
  return (
    <div className="vd15">
      <h1 className="sr-only">Video ders: {ad(aktif.key)}</h1>
      <div className="vd15-ana">
        <Oynatici key={aktif.id} video={aktif} baslik={ad(aktif.key)} />
        <div className="vd15-bilgi">
          <b>{ad(aktif.key)}</b>
          <span className="v15-cap">{brans(aktif.key)} · {aktif.cozunurluk}{aktif.bayt ? ` · ${mb(aktif.bayt)}` : ''}</span>
        </div>
        <div className="vd15-eylem">
          <a className="v15-btn is-soft" href={dersYolu(aktif.key)} onClick={linkClick(() => navigateTo(dersYolu(aktif.key)))}><BookOpen aria-hidden />Ders sayfası</a>
        </div>
      </div>
      {siradaki.length > 0 && (
        <aside className="vd15-yan" aria-label="Diğer videolar">
          <h2 className="v15-cap">Sıradaki</h2>
          <ul className="v15-card vd15-liste">
            {siradaki.map((x) => (
              <li key={x.id}>
                <button type="button" className="vd15-li" onClick={() => setSecili(x.id)}>
                  <span className="v15-tile" aria-hidden><Play /></span>
                  <span className="vd15-li-t"><b>{ad(x.key)}</b><small>{brans(x.key)} · {x.cozunurluk}</small></span>
                </button>
              </li>
            ))}
          </ul>
        </aside>
      )}
    </div>
  );
}

function Oynatici({ video, baslik }: { video: HazirVideo; baslik: string }) {
  const kap = useRef<HTMLDivElement | null>(null);
  const vid = useRef<HTMLVideoElement | null>(null);
  const [src, setSrc] = useState<string | null>(null);
  const [hata, setHata] = useState('');
  const [tam, setTam] = useState(false);
  const [pip, setPip] = useState(false);
  const pipVar = typeof document !== 'undefined' && 'pictureInPictureEnabled' in document && (document as any).pictureInPictureEnabled;
  useEffect(() => {
    let canli = true;
    setSrc(null); setHata('');
    void safeJsonFetch<{ url: string }>(`/api/ders-video/${video.id}/baglanti`).then((r) => {
      if (!canli) return;
      if (r.ok && r.data?.url) setSrc(r.data.url); else setHata(r.error || 'Video açılamadı.');
    });
    return () => { canli = false; };
  }, [video.id]);
  useEffect(() => {
    const f = () => setTam(document.fullscreenElement === kap.current);
    document.addEventListener('fullscreenchange', f);
    return () => document.removeEventListener('fullscreenchange', f);
  }, []);
  useEffect(() => {
    const v = vid.current; if (!v) return;
    const a = () => setPip(true), b = () => setPip(false);
    v.addEventListener('enterpictureinpicture', a); v.addEventListener('leavepictureinpicture', b);
    return () => { v.removeEventListener('enterpictureinpicture', a); v.removeEventListener('leavepictureinpicture', b); };
  }, [src]);
  // Sayfadan ayrılınca resim içinde resim kapanmaz (O03: not alırken izlemeye devam); bileşen kalkarken yalnız tam ekrandan çık
  useEffect(() => () => { if (document.fullscreenElement && document.fullscreenElement === kap.current) void document.exitFullscreen().catch(() => {}); }, []);

  const tamEkran = async () => {
    try {
      if (document.fullscreenElement) await document.exitFullscreen();
      else if (kap.current?.requestFullscreen) await kap.current.requestFullscreen();
      else (vid.current as any)?.webkitEnterFullscreen?.(); // iOS Safari: yalnız video öğesi tam ekran olur
    } catch { /* izin yok */ }
  };
  const resimIcinde = async () => {
    const v = vid.current; if (!v) return;
    try {
      if (document.pictureInPictureElement) await document.exitPictureInPicture();
      else await v.requestPictureInPicture();
    } catch { setHata('Resim içinde resim bu tarayıcıda açılamadı.'); }
  };

  return (
    <div ref={kap} className={`vd15-oyn${tam ? ' is-tam' : ''}`}>
      {src ? (
        <video ref={vid} src={src} controls playsInline preload="metadata" className="vd15-video" aria-label={baslik}
          onError={() => setHata('Video yüklenemedi; bağlantı süresi dolmuş olabilir. Sayfayı yenile.')} />
      ) : (
        <div className="vd15-yer" role="status">{hata || 'Video hazırlanıyor…'}</div>
      )}
      {tam && <div className="vd15-tam-bas" aria-hidden><b>{baslik}</b></div>}
      <div className="vd15-arac">
        {pipVar && <button type="button" className="vd15-ib" onClick={resimIcinde} disabled={!src} aria-pressed={pip} aria-label={pip ? 'Resim içinde resimden çık' : 'Resim içinde resim'} title="Resim içinde resim"><PictureInPicture2 aria-hidden /></button>}
        <button type="button" className="vd15-ib" onClick={tamEkran} disabled={!src} aria-pressed={tam} aria-label={tam ? 'Tam ekrandan çık' : 'Tam ekran'} title="Tam ekran">{tam ? <Minimize aria-hidden /> : <Maximize aria-hidden />}</button>
      </div>
      {src && hata && <p className="vd15-hata" role="status">{hata}</p>}
    </div>
  );
}
