/**
 * Canlı ders oynatıcısı (App düzeyinde, sayfa içeriğinin dışında): ders ekranında tam çubuk (zaman çubuğu + bölüm
 * işaretleri, sarma, hız, ses seçimi, indirme, bölümler), başka sayfalarda küçük mini oynatıcı. Ses öğesi
 * canliDersStore'dadır; bu bileşen yalnız denetimdir.
 */
import React, { useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import { ArrowUpRight, Download, ListOrdered, Pause, Play, RotateCcw, RotateCw, SkipBack, SkipForward, X } from 'lucide-react';
import { navigateTo, pathFor } from '../../router';
import {
  CD_HIZLAR, cdAtla, cdBolumAtla, cdBolumBaslari, cdDosyaAdi, cdHiz, cdHizDongu, cdKapat, cdSar, cdSesKisa, cdSesUrl, cdToggle, cdVaryant,
  fmtSure, useCd,
} from './canliDersStore';
import { ListeDockDenetim, TekrarSecici } from './CanliDersListem';
import { CdDaha } from './CanliDersDaha';
import '../../styles/canli-ders.css';

const hizYaz = (r: number) => `${String(r).replace('.', ',')}×`;

export default function CanliDersDock({ activeTab, dersKey }: { activeTab: string; dersKey?: string }) {
  const key = useCd((s) => s.key);
  const tam = activeTab === 'canli_ders' && !!dersKey && dersKey === key;
  const ref = useRef<HTMLDivElement>(null);
  const [alt, setAlt] = useState(0);

  // Konum: telefonda alt sekme çubuğunun üstü; yüksekliği sayfaya bildirilir (içerik altta kalmasın)
  useLayoutEffect(() => {
    const el = ref.current;
    if (!el) return;
    let t = 0;
    const olc = () => {
      t = 0;
      const tabs = document.querySelector<HTMLElement>('.s12-tabs, .sh-tabs');
      let b = 0;
      if (tabs && getComputedStyle(tabs).display !== 'none') {
        const r = tabs.getBoundingClientRect();
        if (r.height > 0 && r.top < window.innerHeight) b = Math.max(0, window.innerHeight - r.top);
      }
      setAlt(b);
      document.documentElement.style.setProperty('--cd-dock-h', `${Math.round(el.offsetHeight + b)}px`);
      window.dispatchEvent(new Event('cd:dock'));
    };
    const plan = () => { if (!t) t = window.setTimeout(olc, 30); };
    olc();
    const ro = new ResizeObserver(plan);
    ro.observe(el);
    const tabs = document.querySelector('.s12-tabs, .sh-tabs');
    if (tabs) ro.observe(tabs);
    window.addEventListener('resize', plan);
    document.documentElement.classList.add('cd-dock-acik');
    return () => {
      window.clearTimeout(t);
      ro.disconnect();
      window.removeEventListener('resize', plan);
      document.documentElement.classList.remove('cd-dock-acik');
      document.documentElement.style.removeProperty('--cd-dock-h');
      window.dispatchEvent(new Event('cd:dock'));
    };
  }, [tam, key]);

  // Klavye (yalnız ders ekranında): boşluk oynat/duraklat, ←/→ 10 sn
  useEffect(() => {
    if (!tam) return;
    const on = (e: KeyboardEvent) => {
      if (e.defaultPrevented || e.metaKey || e.ctrlKey || e.altKey) return;
      const t = e.target as HTMLElement | null;
      if (t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName))) return;
      if (t?.closest('[role="slider"], [role="dialog"], [role="menu"]')) return;
      if (e.key === ' ' || e.code === 'Space') {
        if (t && /^(BUTTON|A)$/.test(t.tagName)) return; // odaktaki düğme kendi işini yapar
        e.preventDefault();
        cdToggle();
      } else if (e.key === 'ArrowLeft') {
        e.preventDefault();
        cdSar(-10);
      } else if (e.key === 'ArrowRight') {
        e.preventDefault();
        cdSar(10);
      }
    };
    window.addEventListener('keydown', on);
    return () => window.removeEventListener('keydown', on);
  }, [tam]);

  if (!key) return null;
  return (
    <div ref={ref} className={`cd-root cd-dock ${tam ? 'is-tam' : 'is-mini'}`} style={{ bottom: alt }} role="region" aria-label="Canlı ders oynatıcısı">
      {tam ? <TamOynatici /> : <MiniOynatici />}
    </div>
  );
}

/* ---------------- ortak ---------------- */

function OynatDugme({ buyuk }: { buyuk?: boolean }) {
  const playing = useCd((s) => s.playing);
  const bekliyor = useCd((s) => s.bekliyor && s.playing);
  return (
    <button
      type="button"
      className={`cd-oynat${buyuk ? ' is-buyuk' : ''}${bekliyor ? ' is-bekliyor' : ''}`}
      onClick={cdToggle}
      aria-label={playing ? 'Duraklat' : 'Oynat'}
      title={playing ? 'Duraklat (boşluk)' : 'Oynat (boşluk)'}
    >
      {playing ? <Pause aria-hidden /> : <Play aria-hidden />}
    </button>
  );
}

function HizSecici() {
  const rate = useCd((s) => s.rate);
  return (
    <label className="cd-sec" title="Oynatma hızı">
      <span className="cd-sr">Oynatma hızı</span>
      <select value={rate} onChange={(e) => cdHiz(Number(e.target.value))} aria-label="Oynatma hızı">
        {CD_HIZLAR.map((r) => <option key={r} value={r}>{hizYaz(r)}</option>)}
      </select>
    </label>
  );
}

function SesSecici() {
  const vid = useCd((s) => s.vid);
  const varyantlar = useCd((s) => s.varyantlar);
  if (varyantlar.length < 2) {
    const v = varyantlar[0];
    return v ? <span className="cd-ses-tek" title={v.etiket || undefined}>{cdSesKisa(v)}</span> : null;
  }
  return (
    <label className="cd-sec" title="Ses">
      <span className="cd-sr">Ses</span>
      <select value={vid || ''} onChange={(e) => cdVaryant(e.target.value)} aria-label="Ses seçimi">
        {varyantlar.map((v) => <option key={v.id} value={v.id} title={v.etiket || undefined}>{cdSesKisa(v)}</option>)}
      </select>
    </label>
  );
}

function IndirBag() {
  const key = useCd((s) => s.key);
  const vid = useCd((s) => s.vid);
  const no = useCd((s) => s.no);
  const baslik = useCd((s) => s.baslik);
  const varyantlar = useCd((s) => s.varyantlar);
  if (!key || !vid) return null;
  const v = varyantlar.find((x) => x.id === vid);
  return (
    <a className="cd-ib" href={cdSesUrl(key, vid, true)} download={cdDosyaAdi(no, baslik, v?.ses || v?.etiket)} aria-label="MP3 indir" title="MP3 indir">
      <Download aria-hidden />
    </a>
  );
}

/* ---------------- zaman çubuğu ---------------- */

function ZamanCubugu() {
  const t = useCd((s) => s.t);
  const dur = useCd((s) => s.dur);
  const zs = useCd((s) => s.zs);
  const detay = useCd((s) => s.detay);
  const [surukle, setSurukle] = useState<number | null>(null);
  const ref = useRef<HTMLDivElement>(null);
  const isaretler = useMemo(() => {
    const b = cdBolumBaslari();
    return b.map((s, k) => ({ s, ad: detay?.bolumler[k]?.baslik || `Bölüm ${k + 1}` }));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [zs, detay]);
  const goster = surukle ?? t;
  const oran = dur > 0 ? Math.min(1, goster / dur) : 0;

  const xden = (clientX: number) => {
    const r = ref.current!.getBoundingClientRect();
    return Math.min(1, Math.max(0, (clientX - r.left) / Math.max(1, r.width))) * dur;
  };
  const onDown = (e: React.PointerEvent) => {
    if (!dur || e.button !== 0) return;
    e.preventDefault();
    (e.currentTarget as HTMLElement).setPointerCapture(e.pointerId);
    (e.currentTarget as HTMLElement).focus();
    setSurukle(xden(e.clientX));
  };
  const onMove = (e: React.PointerEvent) => { if (surukle != null) setSurukle(xden(e.clientX)); };
  const onUp = (e: React.PointerEvent) => {
    if (surukle == null) return;
    cdAtla(xden(e.clientX));
    setSurukle(null);
  };
  const onKey = (e: React.KeyboardEvent) => {
    const m: Record<string, number> = { ArrowLeft: -5, ArrowDown: -5, ArrowRight: 5, ArrowUp: 5, PageDown: -60, PageUp: 60 };
    if (e.key in m) { e.preventDefault(); e.stopPropagation(); cdSar(m[e.key]); }
    else if (e.key === 'Home') { e.preventDefault(); cdAtla(0); }
    else if (e.key === 'End') { e.preventDefault(); cdAtla(Math.max(0, dur - 1)); }
  };
  const bolumAdi = surukle != null ? [...isaretler].reverse().find((x) => x.s <= surukle)?.ad : undefined;

  return (
    <div className="cd-zaman">
      <span className="cd-sure">{fmtSure(goster)}</span>
      <div
        ref={ref}
        className={`cd-cubuk${surukle != null ? ' is-surukle' : ''}`}
        role="slider"
        tabIndex={0}
        aria-label="Konum"
        aria-valuemin={0}
        aria-valuemax={Math.round(dur)}
        aria-valuenow={Math.round(goster)}
        aria-valuetext={`${fmtSure(goster)} / ${fmtSure(dur)}`}
        onPointerDown={onDown}
        onPointerMove={onMove}
        onPointerUp={onUp}
        onPointerCancel={() => setSurukle(null)}
        onKeyDown={onKey}
      >
        <div className="cd-cubuk-iz">
          <div className="cd-cubuk-dolu" style={{ transform: `scaleX(${oran})` }} />
          {dur > 0 && isaretler.map((x, k) => k > 0 && (
            <span key={k} className="cd-isaret" style={{ left: `${(x.s / dur) * 100}%` }} title={x.ad} />
          ))}
        </div>
        <span className="cd-tutamac" style={{ left: `${oran * 100}%` }} />
        {bolumAdi && <span className="cd-ipucu" style={{ left: `${oran * 100}%` }}>{bolumAdi}</span>}
      </div>
      <span className="cd-sure">{fmtSure(dur)}</span>
    </div>
  );
}

/* ---------------- bölümler ---------------- */

function BolumMenu() {
  const [acik, setAcik] = useState(false);
  const detay = useCd((s) => s.detay);
  const bolum = useCd((s) => s.bolum);
  const zs = useCd((s) => s.zs);
  const ref = useRef<HTMLDivElement>(null);
  const baslar = useMemo(() => cdBolumBaslari(), [zs, detay]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => {
    if (!acik) return;
    const dis = (e: PointerEvent) => { if (!ref.current?.contains(e.target as Node)) setAcik(false); };
    const esc = (e: KeyboardEvent) => { if (e.key === 'Escape') { e.stopPropagation(); setAcik(false); } };
    document.addEventListener('pointerdown', dis);
    document.addEventListener('keydown', esc, true);
    requestAnimationFrame(() => ref.current?.querySelector<HTMLElement>('.cd-bolumler .is-on, .cd-bolumler button')?.focus());
    return () => {
      document.removeEventListener('pointerdown', dis);
      document.removeEventListener('keydown', esc, true);
    };
  }, [acik]);
  if (!detay || detay.bolumler.length < 2) return null;
  const simdiki = bolum >= 0 ? detay.bolumler[bolum]?.baslik || `Bölüm ${bolum + 1}` : '';
  return (
    <div className="cd-menu-kap" ref={ref}>
      <button
        type="button"
        className={`cd-ib cd-bolum-btn${acik ? ' is-on' : ''}`}
        aria-haspopup="menu"
        aria-expanded={acik}
        onClick={() => setAcik((x) => !x)}
        title={simdiki ? `Şu anki bölüm: ${simdiki}` : 'Bölümler'}
        aria-label={`Bölümler${bolum >= 0 ? ` (şu an ${bolum + 1}/${detay.bolumler.length}: ${simdiki})` : ''}`}
      >
        <ListOrdered aria-hidden />
        <span className="cd-bolum-sira">{bolum >= 0 ? bolum + 1 : '–'}/{detay.bolumler.length}</span>
      </button>
      {acik && (
        <div className="cd-bolumler" role="menu" aria-label="Bölümler">
          {detay.bolumler.map((b, k) => (
            <button
              key={k}
              type="button"
              role="menuitem"
              className={k === bolum ? 'is-on' : ''}
              onClick={() => { if (baslar[k] != null) cdAtla(baslar[k]); setAcik(false); }}
            >
              <span className="cd-bl-no">{k + 1}</span>
              <span className="cd-bl-ad">{b.baslik || `Bölüm ${k + 1}`}</span>
              {baslar[k] != null && <span className="cd-bl-t">{fmtSure(baslar[k])}</span>}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

/* ---------------- tam / mini ---------------- */

function Hata() {
  const hata = useCd((s) => s.hata);
  return hata ? <p className="cd-hata">{hata}</p> : null;
}

/** Önceki/sonraki bölüm (bölüm yoksa 30 sn sarar) */
function BolumAtla({ yon }: { yon: 1 | -1 }) {
  const bolumVar = useCd((s) => (s.detay?.bolumler.length || 0) > 1);
  const ad = bolumVar ? (yon < 0 ? 'Önceki bölüm (bölüm başı)' : 'Sonraki bölüm') : yon < 0 ? '30 saniye geri' : '30 saniye ileri';
  return (
    <button type="button" className="cd-ib cd-sar" onClick={() => cdBolumAtla(yon)} aria-label={ad} title={ad}>
      {yon < 0 ? <SkipBack aria-hidden /> : <SkipForward aria-hidden />}
      <span>{bolumVar ? 'bölüm' : '30'}</span>
    </button>
  );
}

/** Şu an anlatılan bölüm: oynatıcının üst satırı */
function SimdikiBolum() {
  const bolum = useCd((s) => s.bolum);
  const ad = useCd((s) => (s.bolum >= 0 ? s.detay?.bolumler[s.bolum]?.baslik || '' : ''));
  const n = useCd((s) => s.detay?.bolumler.length || 0);
  if (bolum < 0 || n < 2) return null;
  return (
    <p className="cd-simdi" aria-live="polite">
      <span>Bölüm {bolum + 1}/{n}</span> {ad || `Bölüm ${bolum + 1}`}
    </p>
  );
}

function TamOynatici() {
  return (
    <div className="cd-tam">
      <SimdikiBolum />
      <ZamanCubugu />
      <ListeDockDenetim dar />
      <div className="cd-denetim">
        <div className="cd-denetim-sol">
          <BolumMenu />
          <ListeDockDenetim />
        </div>
        <div className="cd-denetim-orta">
          <BolumAtla yon={-1} />
          <button type="button" className="cd-ib cd-sar" onClick={() => cdSar(-10)} aria-label="10 saniye geri" title="10 sn geri (←)"><RotateCcw aria-hidden /><span>10</span></button>
          <OynatDugme buyuk />
          <button type="button" className="cd-ib cd-sar" onClick={() => cdSar(10)} aria-label="10 saniye ileri" title="10 sn ileri (→)"><RotateCw aria-hidden /><span>10</span></button>
          <BolumAtla yon={1} />
        </div>
        <div className="cd-denetim-sag">
          <HizSecici />
          <CdDaha etiket="Oynatıcı seçenekleri (ses, tekrar, MP3)" yukari className="cd-dock-daha">
            <div className="cd-daha-satir"><span>Ses</span><SesSecici /></div>
            <div className="cd-daha-satir"><span>Tekrar</span><TekrarSecici /></div>
            <div className="cd-daha-satir"><span>MP3 indir</span><IndirBag /></div>
          </CdDaha>
        </div>
      </div>
      <Hata />
    </div>
  );
}

function MiniOynatici() {
  const key = useCd((s) => s.key);
  const no = useCd((s) => s.no);
  const baslik = useCd((s) => s.baslik);
  const rate = useCd((s) => s.rate);
  const t = useCd((s) => Math.floor(s.t));
  const dur = useCd((s) => s.dur);
  const hata = useCd((s) => s.hata);
  const don = () => key && navigateTo(pathFor('canli_ders', key));
  return (
    <div className="cd-mini">
      <div className="cd-mini-ilerleme" aria-hidden><i style={{ transform: `scaleX(${dur ? Math.min(1, t / dur) : 0})` }} /></div>
      <button type="button" className="cd-mini-ad" onClick={don} aria-label={`Derse dön: ${baslik}`}>
        <b>{no ? `${no}. ` : ''}{baslik}</b>
        <small>{hata || `Canlı ders · ${fmtSure(t)} / ${fmtSure(dur)}`}</small>
      </button>
      <OynatDugme />
      <ListeDockDenetim mini />
      <button type="button" className="cd-ib cd-mini-hiz" onClick={cdHizDongu} aria-label={`Oynatma hızı ${hizYaz(rate)} (değiştir)`} title="Hız">
        {hizYaz(rate)}
      </button>
      <button type="button" className="cd-ib cd-mini-don" onClick={don} aria-label="Derse dön" title="Derse dön"><ArrowUpRight aria-hidden /></button>
      <button type="button" className="cd-ib" onClick={cdKapat} aria-label="Oynatıcıyı kapat" title="Kapat"><X aria-hidden /></button>
    </div>
  );
}
