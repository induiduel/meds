/**
 * KMB hikâye filmi — dersin tüm adım videoları tek bir tam ekran akışta, bir hikâye gibi: her bölümün başında
 * o bölümle kazanılan öğrenim hedefleri (kazanım kartı), bölüm videosu (2B Lottie + EMA sesi), bölüm sonunda öğretici
 * bulgular (püf noktaları, dikkat, sık hata) ve sonda tüm kazanımların onay listesi. Kartlar geri sayımla kendiliğinden
 * ilerler (dokunuş/Devam ile hemen), video bitince sonraki karta geçilir; bölüm şeridinden atlanır. Klavye: ←/→ bölüm,
 * boşluk video, Esc kapat. `?hikaye=1` ile doğrudan açılır (sınama). İzlenen adımlar `izlendi` ile bildirilir.
 */
import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { lockScroll, unlockScroll } from '../../utils/scrollLock';
import { createPortal } from 'react-dom';
import LottieVideo, { KMB_DURDUR, LOTTILER, lottieOnYukle } from './LottieVideo';
import type { Ders, SesKayit } from './kmbVeri';

type Kart = { tip: 'acilis' } | { tip: 'kazanim'; ai: number } | { tip: 'video'; ai: number } | { tip: 'bulgu'; ai: number } | { tip: 'son' };

const Ikon = ({ d }: { d: string }) => <svg viewBox="0 0 24 24" aria-hidden><path d={d} /></svg>;
const I = {
  onceki: 'M6 5h2v14H6zM20 5v14L9 12z', sonraki: 'M16 5h2v14h-2zM4 5v14l11-7z',
  kapat: 'M6.4 5 5 6.4 10.6 12 5 17.6 6.4 19l5.6-5.6 5.6 5.6 1.4-1.4-5.6-5.6L19 6.4 17.6 5 12 10.6z',
  tik: 'M9 16.2 4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4z', yildiz: 'm12 2 3 6.6 7 .8-5.2 4.8 1.4 7-6.2-3.6L5.8 21.2l1.4-7L2 9.4l7-.8z',
  uyari: 'M1 21h22L12 2zm12-3h-2v-2h2zm0-4h-2v-4h2z', puf: 'M9 21h6v-1H9zm3-19a7 7 0 0 0-4 12.7V17h8v-2.3A7 7 0 0 0 12 2z',
};
/** Kart süresi: metin uzunluğuna göre 6–14 sn (öğrenci okuyabilsin; isterse hemen geçer) */
const kartSuresi = (metin: string) => Math.min(14, Math.max(6, 3 + metin.length / 22));

export default function HikayeFilmi({ ders, ses, onKapat, izlendi, onSinav }: {
  ders: Ders; ses: SesKayit | null; onKapat: () => void; izlendi?: (adimId: string) => void; onSinav?: () => void;
}) {
  const kap = useRef<HTMLDivElement>(null);
  const adimlar = useMemo(() => ders.adimlar.filter((a) => LOTTILER.some((x) => x.adim === a.id)), [ders]);
  // kazanımlar ilk geçtikleri adımda tanıtılır (her hedef bir kez)
  const kazanimlar = useMemo(() => {
    const gorulen = new Set<number>();
    return adimlar.map((a) => ders.hedefler.filter((h) => h.adimlar.includes(a.id) && !gorulen.has(h.no) && gorulen.add(h.no)));
  }, [adimlar, ders]);
  const kartlar = useMemo<Kart[]>(() => {
    const k: Kart[] = [{ tip: 'acilis' }];
    adimlar.forEach((a, ai) => {
      if (kazanimlar[ai].length) k.push({ tip: 'kazanim', ai });
      k.push({ tip: 'video', ai });
      const hata = kazanimlar[ai].map((h) => ders.hedefCalisma?.find((c) => c.no === h.no)?.hata).filter(Boolean);
      if ((a.puf?.length || 0) + (a.dikkat?.length || 0) + hata.length > 0) k.push({ tip: 'bulgu', ai });
    });
    k.push({ tip: 'son' });
    return k;
  }, [adimlar, kazanimlar, ders]);
  const [ki, setKi] = useState(0);
  const [uyanik, setUyanik] = useState(true);
  const [sayac, setSayac] = useState(0); // kart geri sayımı (sn)
  const kart = kartlar[ki];
  const sonraki = kartlar[ki + 1];
  const bolumNo = (k: Kart) => ('ai' in k ? k.ai : k.tip === 'son' ? adimlar.length - 1 : -1);
  const ai = bolumNo(kart);

  useEffect(() => {
    kap.current?.requestFullscreen?.().catch(() => { /* izin yoksa katman pencereyi kaplar */ });
    try { (screen.orientation as any)?.lock?.('landscape').catch(() => {}); } catch { /* yok */ }
    lockScroll();
    document.body.classList.add('kmb-film-acik');
    return () => { unlockScroll(); document.body.classList.remove('kmb-film-acik'); window.dispatchEvent(new CustomEvent(KMB_DURDUR, { detail: 'kapat' })); };
  }, []);
  // sonraki video önceden yüklenir
  useEffect(() => {
    const v = kartlar.slice(ki + 1).find((k) => k.tip === 'video') as { tip: 'video'; ai: number } | undefined;
    if (v) lottieOnYukle(`adim-${adimlar[v.ai].id}`).catch(() => {});
  }, [ki, kartlar, adimlar]);
  const git = useCallback((i: number) => { setKi(Math.max(0, Math.min(kartlar.length - 1, i))); setUyanik(true); }, [kartlar.length]);
  const ileri = useCallback(() => { if (kart.tip === 'video') izlendi?.(adimlar[kart.ai].id); git(ki + 1); }, [kart, ki, git, izlendi, adimlar]);
  const bolumeGit = (b: number) => git(Math.max(1, kartlar.findIndex((k) => 'ai' in k && k.ai === b)));
  // kart geri sayımı
  const kartMetni = (k: Kart) => {
    if (k.tip === 'acilis') return ders.amac;
    if (k.tip === 'kazanim') return kazanimlar[k.ai].map((h) => h.metin).join(' ');
    if (k.tip === 'bulgu') return [...(adimlar[k.ai].puf || []), ...(adimlar[k.ai].dikkat || [])].join(' ');
    return '';
  };
  useEffect(() => {
    if (kart.tip === 'video' || kart.tip === 'son') { setSayac(0); return; }
    const sure = kartSuresi(kartMetni(kart));
    const t0 = performance.now();
    setSayac(sure);
    const z = window.setInterval(() => {
      const kalan = sure - (performance.now() - t0) / 1000;
      if (kalan <= 0) { window.clearInterval(z); ileri(); } else setSayac(kalan);
    }, 100);
    return () => window.clearInterval(z);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ki]);
  const kapat = () => { if (document.fullscreenElement) document.exitFullscreen().catch(() => {}); onKapat(); };
  const tus = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') kapat();
    else if (e.key === 'ArrowRight' && kart.tip !== 'video') { e.preventDefault(); ileri(); }
    else if (e.key === 'ArrowLeft' && kart.tip !== 'video') { e.preventDefault(); git(ki - 1); }
    else if (e.key === 'PageDown') { e.preventDefault(); bolumeGit(Math.min(adimlar.length - 1, Math.max(0, ai) + 1)); }
    else if (e.key === 'PageUp') { e.preventDefault(); bolumeGit(Math.max(0, ai - 1)); }
  };
  const a = ai >= 0 ? adimlar[ai] : null;
  const sonrakiVideo = kartlar.slice(ki + 1).find((k) => k.tip === 'video') as { tip: 'video'; ai: number } | undefined;

  const kartGovde = () => {
    if (kart.tip === 'acilis') {
      return (
        <div className="kmb-hk-kart acilis">
          <small className="kmb-hk-ust">Hikâye filmi · {adimlar.length} bölüm · {ders.hedefler.length} kazanım</small>
          <h1>{ders.ad}</h1>
          <p>{ders.amac}</p>
          <ol className="kmb-hk-icindekiler">{adimlar.map((x, i) => <li key={x.id}><button onClick={() => bolumeGit(i)}><b>{i + 1}</b> {x.baslik}</button></li>)}</ol>
        </div>
      );
    }
    if (kart.tip === 'kazanim') {
      return (
        <div className="kmb-hk-kart kazanim">
          <small className="kmb-hk-ust">Bölüm {kart.ai + 1} / {adimlar.length} · {kazanimlar[kart.ai].length > 1 ? 'Kazanımlar' : 'Kazanım'}</small>
          <h2>{adimlar[kart.ai].baslik}</h2>
          <ul className="kmb-hk-liste">
            {kazanimlar[kart.ai].map((h) => <li key={h.no}><span className="kmb-hk-no"><Ikon d={I.yildiz} />{h.no}</span><span>{h.metin}</span></li>)}
          </ul>
        </div>
      );
    }
    if (kart.tip === 'bulgu') {
      const x = adimlar[kart.ai];
      const hata = kazanimlar[kart.ai].map((h) => ders.hedefCalisma?.find((c) => c.no === h.no)?.hata).filter((m): m is string => !!m);
      return (
        <div className="kmb-hk-kart bulgu">
          <small className="kmb-hk-ust">Bölüm {kart.ai + 1} · Öğretici bulgular</small>
          <h2>{x.baslik}</h2>
          <ul className="kmb-hk-liste">
            {(x.puf || []).map((m, i) => <li key={`p${i}`} className="puf"><span className="kmb-hk-no"><Ikon d={I.puf} /></span><span>{m}</span></li>)}
            {(x.dikkat || []).map((m, i) => <li key={`d${i}`} className="dikkat"><span className="kmb-hk-no"><Ikon d={I.uyari} /></span><span>{m}</span></li>)}
            {hata.map((m, i) => <li key={`h${i}`} className="hata"><span className="kmb-hk-no"><Ikon d={I.uyari} /></span><span><b>Sık hata:</b> {m}</span></li>)}
          </ul>
        </div>
      );
    }
    return (
      <div className="kmb-hk-kart son">
        <small className="kmb-hk-ust">Film bitti · {ders.hedefler.length} kazanım</small>
        <h2>Bu derste kazandıkların</h2>
        <ol className="kmb-hk-liste iki">{ders.hedefler.map((h) => <li key={h.no}><span className="kmb-hk-no ok"><Ikon d={I.tik} /></span><span>{h.metin}</span></li>)}</ol>
        <div className="kmb-hk-son-dugmeler">
          <button onClick={() => git(0)}>↺ Baştan izle</button>
          {onSinav && <button className="ana" onClick={() => { kapat(); onSinav(); }}>Sınava geç ›</button>}
          <button onClick={kapat}>Kapat</button>
        </div>
      </div>
    );
  };

  return createPortal(
    <div ref={kap} className={`kmb-hk kmb-kok${uyanik || kart.tip !== 'video' ? '' : ' uyku'}`} role="dialog" aria-label={`Hikâye filmi: ${ders.ad}`} tabIndex={-1} onKeyDown={tus}>
      <div className="kmb-hk-ust-cubuk">
        <div className="kmb-hk-serit" role="tablist" aria-label="Bölümler">
          {adimlar.map((x, j) => <button key={x.id} role="tab" aria-selected={j === ai} title={`${j + 1}. ${x.baslik}`} className={`${j === ai ? 'etkin' : ''}${j < ai ? ' gecti' : ''}`} onClick={() => bolumeGit(j)} />)}
        </div>
        <div className="kmb-hk-baslik">{a ? <><span className="kmb-hk-bolum">{ai + 1} / {adimlar.length}</span><b>{a.baslik}</b></> : <b>{ders.ad}</b>}</div>
        <div className="kmb-hk-dugmeler">
          <button onClick={() => bolumeGit(Math.max(0, ai - 1))} disabled={ai <= 0} aria-label="Önceki bölüm"><Ikon d={I.onceki} /></button>
          <button onClick={() => bolumeGit(ai + 1)} disabled={ai >= adimlar.length - 1} aria-label="Sonraki bölüm"><Ikon d={I.sonraki} /></button>
          <button onClick={kapat} aria-label="Kapat"><Ikon d={I.kapat} /></button>
        </div>
      </div>
      <div className="kmb-hk-govde">
        {kart.tip === 'video' && a ? (
          <LottieVideo key={a.id} ad={`adim-${a.id}`} kod={ders.kod} ses={ses} otomatik doldur onGoster={setUyanik}
            onBitti={() => izlendi?.(a.id)} otoSonraki={900}
            sonraki={sonraki ? { ad: sonrakiVideo ? `adim-${adimlar[sonrakiVideo.ai].id}` : `adim-${a.id}`, baslik: sonraki.tip === 'bulgu' ? 'Öğretici bulgular' : sonraki.tip === 'kazanim' ? `Bölüm ${sonraki.ai + 1}` : sonraki.tip === 'video' ? adimlar[sonraki.ai].baslik : 'Özet', git: ileri } : undefined} />
        ) : (
          <div className="kmb-hk-kart-kap" onClick={(e) => { if ((e.target as HTMLElement).closest('button')) return; if (kart.tip !== 'son') ileri(); }}>
            {kartGovde()}
            {kart.tip !== 'son' && (
              <button className="kmb-hk-devam" onClick={ileri} style={{ ['--kmb-hk-s' as string]: `${kartSuresi(kartMetni(kart))}s` }}>
                <i aria-hidden><b style={{ transform: `scaleX(${Math.max(0, sayac / kartSuresi(kartMetni(kart)))})` }} /></i>
                {sonraki?.tip === 'video' ? 'Videoyu başlat' : 'Devam'} <small>{Math.ceil(sayac)} sn</small>
              </button>
            )}
          </div>
        )}
      </div>
    </div>,
    document.body,
  );
}
