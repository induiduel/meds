import React, { useMemo, useRef, useState } from 'react';
import { MoreHorizontal, Pause, Play, RotateCcw, RotateCw, SkipBack, SkipForward } from 'lucide-react';
import type { EkModul } from './ekVeri';
import { HIZLAR, type Sira } from './ekOrtak';

/**
 * Sesli ders oynatıcısıyla aynı düzen (canlı ders v15 alt oynatıcısı, tasarım S19): parça parça ilerleyen çubuk (her parça bir
 * soru; üstüne gelince "Soru k" + zaman, tıklama/sürükleme o ana atlar), süre · şu an · toplam, önceki · −10 · büyük oynat ·
 * +10 · sonraki, hız hapı ve ⋯ (hız listesi). Ses öğesi ekOrtak'ın ortak öğesidir (kilit ekranı, arka plan, hız aynı).
 * grup: kaç klip bir parça (soru + çözüm = 2).
 */
const sa = (sn: number) => `${Math.floor(sn / 60)}:${String(Math.floor(sn % 60)).padStart(2, '0')}`;
const hizYaz = (h: number) => `${String(h).replace('.', ',')}×`;

export const EkSesliOynatici: React.FC<{ m: EkModul; sira: Sira; klipler: string[]; grup: number; birim: string; ad: (parca: number, klip: number) => string }> = ({ m, sira, klipler, grup, birim, ad }) => {
  const [ayar, setAyar] = useState(false);
  const [surukle, setSurukle] = useState<number | null>(null);
  const [uzerinde, setUzerinde] = useState<number | null>(null);
  const ref = useRef<HTMLDivElement>(null);
  // klip başlangıçları (sn) ve parçalar
  const { bas, dur, parcalar } = useMemo(() => {
    const b: number[] = [];
    let t = 0;
    klipler.forEach((k) => { b.push(t); t += m.klip[k]?.sure || 0; });
    const p = [];
    for (let k = 0; k < klipler.length; k += grup) p.push({ s: b[k], e: k + grup < klipler.length ? b[k + grup] : t, no: k / grup });
    return { bas: b, dur: t, parcalar: p };
  }, [m, klipler, grup]);
  const simdi = sira.i >= 0 ? bas[sira.i] + Math.min(sira.klipAn.t, m.klip[klipler[sira.i]]?.sure || 0) : 0;
  const goster = surukle ?? simdi;
  const oran = dur > 0 ? Math.min(1, goster / dur) : 0;
  const parcaNo = (x: number) => { let k = parcalar.length - 1; while (k > 0 && x < parcalar[k].s) k--; return k; };
  const etkin = parcaNo(goster);
  const xden = (cx: number) => { const r = ref.current!.getBoundingClientRect(); return Math.min(1, Math.max(0, (cx - r.left) / Math.max(1, r.width))) * dur; };
  const git = (x: number) => {
    let k = klipler.length - 1;
    while (k > 0 && x < bas[k]) k--;
    sira.konum(k, x - bas[k]);
  };
  const parcaGit = (p: number) => sira.cal(Math.max(0, Math.min(parcalar.length - 1, p)) * grup);
  const ipucu = surukle ?? uzerinde;
  const onKey = (e: React.KeyboardEvent) => {
    const adim: Record<string, number> = { ArrowLeft: -5, ArrowRight: 5, PageDown: -60, PageUp: 60 };
    if (e.shiftKey && (e.key === 'ArrowLeft' || e.key === 'ArrowRight')) { e.preventDefault(); parcaGit(etkin + (e.key === 'ArrowRight' ? 1 : -1)); return; }
    if (e.key in adim) { e.preventDefault(); git(Math.max(0, Math.min(dur - 0.5, goster + adim[e.key]))); }
  };
  if (!sira.sesVar) return <p className="ekm-not">Sesli çözüm hazırlanıyor.</p>;
  return (
    <div className={`ekm-oyn v15-card${sira.caliyor ? ' is-caliyor' : ''}`} role="region" aria-label="Sesli çözüm oynatıcısı">
      <div className="ekm-oyn-zaman">
        <span>{sa(goster)}</span>
        <div
          ref={ref}
          className={`ekm-oyn-cubuk${surukle != null ? ' is-surukle' : ''}`}
          role="slider" tabIndex={0}
          aria-label={`Konum (Shift + ok: ${birim.toLowerCase()} atla)`}
          aria-valuemin={0} aria-valuemax={Math.round(dur)} aria-valuenow={Math.round(goster)}
          aria-valuetext={`${sa(goster)} / ${sa(dur)}, ${birim} ${etkin + 1}`}
          onPointerDown={(e) => { if (e.button !== 0) return; e.preventDefault(); e.currentTarget.setPointerCapture(e.pointerId); setSurukle(xden(e.clientX)); }}
          onPointerMove={(e) => { const x = xden(e.clientX); if (surukle != null) setSurukle(x); if (e.pointerType !== 'touch') setUzerinde(x); }}
          onPointerUp={(e) => { if (surukle == null) return; git(xden(e.clientX)); setSurukle(null); }}
          onPointerLeave={() => setUzerinde(null)}
          onPointerCancel={() => { setSurukle(null); setUzerinde(null); }}
          onKeyDown={onKey}
        >
          <div className="ekm-oyn-parcalar">
            {parcalar.map((p) => {
              const gen = Math.max(0.01, p.e - p.s);
              return <span key={p.no} className={p.no === etkin ? 'is-etkin' : undefined} style={{ flexGrow: gen }}><i style={{ transform: `scaleX(${Math.min(1, Math.max(0, (goster - p.s) / gen))})` }} /></span>;
            })}
          </div>
          <span className="ekm-oyn-tutamac" style={{ left: `${oran * 100}%` }} />
          {ipucu != null && (
            <span className="ekm-oyn-ipucu" style={{ ['--x' as string]: dur ? ipucu / dur : 0 }}>
              <b>{birim} {parcaNo(ipucu) + 1}</b><span>{sa(ipucu)}</span>
            </span>
          )}
        </div>
        <span>{sa(dur)}</span>
      </div>
      <div className="ekm-oyn-den">
        <div className="ekm-oyn-orta">
          <button type="button" onClick={() => parcaGit(sira.i < 0 ? 0 : etkin - 1)} aria-label={`Önceki ${birim.toLowerCase()}`} title={`Önceki ${birim.toLowerCase()}`}><SkipBack aria-hidden /></button>
          <button type="button" onClick={() => sira.atla(-10)} disabled={sira.i < 0} aria-label="10 saniye geri" title="10 sn geri"><RotateCcw aria-hidden /></button>
          <button type="button" className="is-oynat" onClick={sira.dugme} aria-label={sira.caliyor ? 'Duraklat' : 'Oynat'}>{sira.caliyor ? <Pause aria-hidden /> : <Play aria-hidden />}</button>
          <button type="button" onClick={() => sira.atla(10)} disabled={sira.i < 0} aria-label="10 saniye ileri" title="10 sn ileri"><RotateCw aria-hidden /></button>
          <button type="button" onClick={() => parcaGit(sira.i < 0 ? 1 : etkin + 1)} aria-label={`Sonraki ${birim.toLowerCase()}`} title={`Sonraki ${birim.toLowerCase()}`}><SkipForward aria-hidden /></button>
        </div>
        <span className="ekm-oyn-ad">{sira.i >= 0 ? ad(etkin, sira.i) : `${parcalar.length} ${birim.toLowerCase()} · EMA sesi`}</span>
        <button type="button" className="ekm-oyn-hiz" onClick={sira.hizDegis} aria-label={`Oynatma hızı ${hizYaz(sira.hiz)} (değiştir)`} title="Hız (dokundukça değişir)">{hizYaz(sira.hiz)}</button>
        <button type="button" className={`ekm-oyn-daha${ayar ? ' is-on' : ''}`} onClick={() => setAyar(!ayar)} aria-expanded={ayar} aria-label="Oynatıcı seçenekleri"><MoreHorizontal aria-hidden /></button>
      </div>
      {ayar && (
        <div className="ekm-ayar" role="group" aria-label="Oynatıcı seçenekleri">
          <div className="ekm-ayar-satir">
            <span>Okuma hızı</span>
            <div className="ekm-hizlar">
              {HIZLAR.map((h) => <button key={h} type="button" className={sira.hiz === h ? 'is-on' : ''} aria-pressed={sira.hiz === h} onClick={() => sira.hizAyarla(h)}>{hizYaz(h)}</button>)}
            </div>
          </div>
          {sira.i >= 0 && (
            <div className="ekm-ayar-satir">
              <span>Baştan başla</span>
              <button type="button" className="v15-btn is-ghost" onClick={() => sira.durdur()}>Durdur ve başa dön</button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
