/**
 * Canlı ders oynatıcısı (App düzeyinde, sayfa içeriğinin dışında): ders ekranında tam çubuk (zaman çubuğu + bölüm
 * işaretleri, sarma, hız, ses seçimi, indirme, bölümler), başka sayfalarda küçük mini oynatıcı. Ses öğesi
 * canliDersStore'dadır; bu bileşen yalnız denetimdir.
 */
import React, { useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import { ArrowUpRight, ChevronDown, ChevronUp, Download, ListOrdered, Pause, Play, RotateCcw, RotateCw, SkipBack, SkipForward, X } from 'lucide-react';
import { navigateTo, pathFor } from '../../router';
import {
  CD_HIZLAR, cdAtla, cdBolumAtla, cdBolumBaslari, cdDosyaAdi, cdHiz, cdHizDongu, cdKapat, cdSar, cdSesKisa, cdSesUrl, cdToggle, cdVaryant, cdDurum,
  fmtSure, useCd,
} from './canliDersStore';
import { ListeDockDenetim, TekrarSecici } from './CanliDersListem';
import { CdDaha } from './CanliDersDaha';
import { cdMotivasyonKur } from './canliDersMotivasyon';
import { cdTvMi, cdTvTus, type TvEylem } from './CanliDersTv';
import '../../styles/canli-ders.css';

const hizYaz = (r: number) => `${String(r).replace('.', ',')}×`;

/** Ders ekranında oynatıcı küçük hapa indirilebilir (metin alanı genişler); tercih cihazda saklanır */
const GIZLI_KEY = 'medsoru_cd_dock_kucuk_v1';
const gizliOku = () => { try { return localStorage.getItem(GIZLI_KEY) === '1'; } catch { return false; } };

export default function CanliDersDock({ activeTab, dersKey }: { activeTab: string; dersKey?: string }) {
  useEffect(() => { cdMotivasyonKur(); }, []);
  const key = useCd((s) => s.key);
  const tam = activeTab === 'canli_ders' && !!dersKey && dersKey === key;
  const ref = useRef<HTMLDivElement>(null);
  const [alt, setAlt] = useState(0);
  const [kucuk, setKucukHam] = useState(gizliOku);
  const setKucuk = (v: boolean) => { setKucukHam(v); try { localStorage.setItem(GIZLI_KEY, v ? '1' : '0'); } catch { /* yok */ } };

  // Konum: telefonda alt sekme çubuğunun üstü; yüksekliği sayfaya bildirilir (içerik altta kalmasın)
  useLayoutEffect(() => {
    const el = ref.current;
    if (!el) return;
    const vv = window.visualViewport;
    let t = 0;
    const olc = () => {
      t = 0;
      const kok = document.documentElement;
      const tamFs = kok.classList.contains('cd-tam-ekran') || kok.classList.contains('is-app-fullscreen');
      const tabs = document.querySelector<HTMLElement>('.a13-island-wrap, .s12-tabs, .sh-tabs');
      // Görünür alanı visualViewport'tan ölç: iOS Safari/Chrome'da adres çubuğu ve klavye
      // window.innerHeight'i değiştirmeden görünür alanı kaydırır; dock aksi hâlde tarayıcı
      // altlığının altında/klavyenin arkasında kalıyordu.
      const viewH = Math.round(vv?.height || window.innerHeight);
      const viewTop = Math.round(vv?.offsetTop || 0);
      const viewBottom = viewTop + viewH;
      let b = Math.max(0, window.innerHeight - viewBottom);
      if (!tamFs && tabs && getComputedStyle(tabs).display !== 'none') {
        const r = tabs.getBoundingClientRect();
        if (r.height > 0 && r.top < viewBottom) b = Math.max(b, viewBottom - r.top);
      }
      setAlt(b);
      const gizli = getComputedStyle(el).display === 'none';
      kok.style.setProperty('--cd-dock-h', `${gizli ? 0 : Math.round(el.offsetHeight + b)}px`);
      window.dispatchEvent(new Event('cd:dock'));
    };
    const plan = () => { if (!t) t = window.setTimeout(olc, 30); };
    const fsPlan = () => {
      olc();
      window.setTimeout(olc, 100);
    };
    olc();
    const ro = new ResizeObserver(plan);
    ro.observe(el);
    const tabs = document.querySelector('.a13-island-wrap, .s12-tabs, .sh-tabs');
    if (tabs) ro.observe(tabs);
    window.addEventListener('resize', plan);
    vv?.addEventListener('resize', plan);
    vv?.addEventListener('scroll', plan);
    window.addEventListener('cd:tam-ekran', fsPlan);
    window.addEventListener('medsor:fullscreenchange', fsPlan);
    document.addEventListener('fullscreenchange', fsPlan);
    document.addEventListener('webkitfullscreenchange', fsPlan);
    document.documentElement.classList.add('cd-dock-acik');
    return () => {
      window.clearTimeout(t);
      ro.disconnect();
      window.removeEventListener('resize', plan);
      vv?.removeEventListener('resize', plan);
      vv?.removeEventListener('scroll', plan);
      window.removeEventListener('cd:tam-ekran', fsPlan);
      window.removeEventListener('medsor:fullscreenchange', fsPlan);
      document.removeEventListener('fullscreenchange', fsPlan);
      document.removeEventListener('webkitfullscreenchange', fsPlan);
      document.documentElement.classList.remove('cd-dock-acik');
      document.documentElement.style.removeProperty('--cd-dock-h');
      window.dispatchEvent(new Event('cd:dock'));
    };
  }, [tam, key, kucuk]);

  // Klavye / TV kumandası (yalnız ders ekranında): boşluk-OK-⏯ oynat/duraklat, ←/→ 10 sn, ⏪/⏩ 30 sn,
  // TV'de ▲/▼ ve kanal/parça tuşları bölüm atlar (CanliDersTv)
  useEffect(() => {
    if (!tam) return;
    const tv = cdTvMi();
    const on = (e: KeyboardEvent) => {
      if (e.defaultPrevented || e.metaKey || e.ctrlKey || e.altKey) return;
      const t = e.target as HTMLElement | null;
      if (t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName))) return;
      if (t?.closest?.('[role="slider"], [role="dialog"], [role="menu"], [role="alertdialog"]')) return;
      if (e.key === ' ' || e.code === 'Space') {
        if (t && /^(BUTTON|A)$/.test(t.tagName)) return; // odaktaki düğme kendi işini yapar
        e.preventDefault();
        cdToggle();
        return;
      }
      const ey = cdTvTus(e, tv);
      if (!ey) return;
      // OK: odakta düğme/bağlantı varsa onu çalıştırsın
      if ((e.key === 'Enter' || e.keyCode === 13) && t && /^(BUTTON|A)$/.test(t.tagName)) return;
      e.preventDefault();
      if (ey === 'degistir') cdToggle();
      else if (ey === 'oynat') { if (!cdDurum().playing) cdToggle(); }
      else if (ey === 'duraklat') { if (cdDurum().playing) cdToggle(); }
      else if (ey === 'geri') cdSar(-10);
      else if (ey === 'ileri') cdSar(10);
      else if (ey === 'geriCok') cdSar(-30);
      else if (ey === 'ileriCok') cdSar(30);
      else if (ey === 'oncekiBolum') cdBolumAtla(-1);
      else cdBolumAtla(1);
      if (tv) tvGoster(ey);
    };
    window.addEventListener('keydown', on);
    return () => window.removeEventListener('keydown', on);
  }, [tam]);
  // TV: basılan tuşun kısa geri bildirimi
  const [tvIz, setTvIz] = useState<{ m: string; n: number } | null>(null);
  const tvGoster = (ey: TvEylem) => {
    const m: Record<TvEylem, string> = { degistir: cdDurum().playing ? '▶ Oynatılıyor' : '❚❚ Duraklatıldı', oynat: '▶ Oynatılıyor', duraklat: '❚❚ Duraklatıldı',
      geri: '◀ 10 sn geri', ileri: '10 sn ileri ▶', geriCok: '⏪ 30 sn geri', ileriCok: '30 sn ileri ⏩', oncekiBolum: '▲ Önceki bölüm', sonrakiBolum: '▼ Sonraki bölüm' };
    setTvIz((x) => ({ m: m[ey], n: (x?.n || 0) + 1 }));
  };
  useEffect(() => { if (!tvIz) return; const i = window.setTimeout(() => setTvIz(null), 1200); return () => window.clearTimeout(i); }, [tvIz]);

  if (!key) return null;
  return (
    <div ref={ref} className={`cd-root cd-dock ${tam ? (kucuk ? 'is-tam is-kucuk' : 'is-tam') : 'is-mini'}`} style={{ bottom: alt }} role="region" aria-label="Sesli ders oynatıcısı">
      {!tam ? <MiniOynatici /> : kucuk ? <KucukOynatici onAc={() => setKucuk(false)} /> : <TamOynatici onKucult={() => setKucuk(true)} />}
      {tvIz && <div key={tvIz.n} className="cd-tv-iz" role="status">{tvIz.m}</div>}
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
  /** İmlecin (fare/kalem) üstünde durduğu zaman; dokunmatikte yalnız sürüklerken dolar */
  const [uzerinde, setUzerinde] = useState<number | null>(null);
  const ref = useRef<HTMLDivElement>(null);
  /*
   * YouTube tarzı bölüm çubuğu: her bölüm ayrı bir parça (aralarında boşluk), dolu kısım parça parça ilerler.
   * Üstüne gelince parça kalınlaşır ve ipucunda "Bölüm k · ad" + zaman görünür; tıklama/sürükleme o ana atlar.
   */
  const parcalar = useMemo(() => {
    const b = cdBolumBaslari();
    if (!dur || b.length < 2) return [{ s: 0, e: dur || 1, ad: '', k: -1 }];
    return b.map((s, k) => ({ s, e: k + 1 < b.length ? b[k + 1] : dur, ad: detay?.bolumler[k]?.baslik || `Bölüm ${k + 1}`, k }));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [zs, detay, dur]);
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
  const onMove = (e: React.PointerEvent) => {
    if (!dur) return;
    const x = xden(e.clientX);
    if (surukle != null) setSurukle(x);
    if (e.pointerType !== 'touch') setUzerinde(x);
  };
  const onUp = (e: React.PointerEvent) => {
    if (surukle == null) return;
    cdAtla(xden(e.clientX));
    setSurukle(null);
  };
  const bolumIndex = (x: number) => {
    for (let k = parcalar.length - 1; k >= 0; k--) if (x >= parcalar[k].s) return k;
    return 0;
  };
  const onKey = (e: React.KeyboardEvent) => {
    // Shift + ok: önceki / sonraki bölümün başı (YouTube'daki bölüm atlama)
    if (e.shiftKey && (e.key === 'ArrowLeft' || e.key === 'ArrowRight') && parcalar.length > 1) {
      e.preventDefault(); e.stopPropagation();
      const k = bolumIndex(t);
      const hedef = e.key === 'ArrowRight' ? Math.min(parcalar.length - 1, k + 1) : (t - parcalar[k].s > 3 ? k : Math.max(0, k - 1));
      cdAtla(parcalar[hedef].s);
      return;
    }
    const m: Record<string, number> = { ArrowLeft: -5, ArrowDown: -5, ArrowRight: 5, ArrowUp: 5, PageDown: -60, PageUp: 60 };
    if (e.key in m) { e.preventDefault(); e.stopPropagation(); cdSar(m[e.key]); }
    else if (e.key === 'Home') { e.preventDefault(); cdAtla(0); }
    else if (e.key === 'End') { e.preventDefault(); cdAtla(Math.max(0, dur - 1)); }
  };
  const ipucuZaman = surukle ?? uzerinde;
  const ipucuParca = ipucuZaman != null ? parcalar[bolumIndex(ipucuZaman)] : undefined;
  const ipucuOran = ipucuZaman != null && dur > 0 ? ipucuZaman / dur : 0;
  const etkinParca = bolumIndex(goster);

  return (
    <div className="cd-zaman">
      <span className="cd-sure">{fmtSure(goster)}</span>
      <div
        ref={ref}
        className={`cd-cubuk${surukle != null ? ' is-surukle' : ''}${parcalar.length > 1 ? ' is-bolumlu' : ''}`}
        role="slider"
        tabIndex={0}
        aria-label={parcalar.length > 1 ? 'Konum (Shift + ok: bölüm atla)' : 'Konum'}
        aria-valuemin={0}
        aria-valuemax={Math.round(dur)}
        aria-valuenow={Math.round(goster)}
        aria-valuetext={`${fmtSure(goster)} / ${fmtSure(dur)}${parcalar[etkinParca]?.ad ? `, ${parcalar[etkinParca].ad}` : ''}`}
        onPointerDown={onDown}
        onPointerMove={onMove}
        onPointerLeave={() => setUzerinde(null)}
        onPointerUp={onUp}
        onPointerCancel={() => { setSurukle(null); setUzerinde(null); }}
        onKeyDown={onKey}
      >
        <div className="cd-parcalar">
          {parcalar.map((p) => {
            const gen = Math.max(0, p.e - p.s);
            const dolu = gen > 0 ? Math.min(1, Math.max(0, (goster - p.s) / gen)) : 0;
            const ustunde = ipucuParca === p && parcalar.length > 1;
            return (
              <span key={p.k} className={`cd-bparca${ustunde ? ' is-ustunde' : ''}${p.k === parcalar[etkinParca]?.k ? ' is-etkin' : ''}`} style={{ flexGrow: gen || 1 }}>
                <i style={{ transform: `scaleX(${dolu})` }} />
              </span>
            );
          })}
        </div>
        <span className="cd-tutamac" style={{ left: `${oran * 100}%` }} />
        {ipucuZaman != null && (
          <span className="cd-ipucu" style={{ ['--x' as string]: ipucuOran }}>
            {ipucuParca?.ad && <b>{ipucuParca.k + 1}. {ipucuParca.ad}</b>}
            <span>{fmtSure(ipucuZaman)}</span>
          </span>
        )}
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

/** Ders ekranında küçültülmüş oynatıcı: oynat/duraklat, ince ilerleme, bölüm adı; dokununca açılır */
function KucukOynatici({ onAc }: { onAc: () => void }) {
  const t = useCd((s) => Math.floor(s.t));
  const dur = useCd((s) => s.dur);
  const bolum = useCd((s) => s.bolum);
  const detay = useCd((s) => s.detay);
  const ad = (bolum >= 0 && detay?.bolumler[bolum]?.baslik) || 'Sesli ders';
  return (
    <div className="cd-kucuk">
      <OynatDugme />
      <button type="button" className="cd-kucuk-ad" onClick={onAc} aria-label="Oynatıcıyı aç">
        <b>{ad}</b>
        <span className="cd-kucuk-ilerleme" aria-hidden><i style={{ transform: `scaleX(${dur ? Math.min(1, t / dur) : 0})` }} /></span>
        <small>{fmtSure(t)} / {fmtSure(dur)}</small>
      </button>
      <button type="button" className="cd-ib" onClick={onAc} aria-label="Oynatıcıyı aç" title="Oynatıcıyı aç"><ChevronUp aria-hidden /></button>
    </div>
  );
}

/** Henüz dinlenmemiş derste ne yapılacağını söyleyen satır (metnin üstüne binmez) */
function BaslaIpucu() {
  const playing = useCd((s) => s.playing);
  const t = useCd((s) => Math.floor(s.t));
  const [basladi, setBasladi] = useState(false);
  useEffect(() => { if (playing) setBasladi(true); }, [playing]);
  if (basladi || playing) return null;
  return <p className="cd-basla-satir">{t >= 5 ? `Oynat'a bas: ${fmtSure(t)} konumundan sürer.` : "Başlatmak için oynat'a bas ya da metinde bir paragrafa dokun."}</p>;
}

function TamOynatici({ onKucult }: { onKucult: () => void }) {
  return (
    <div className="cd-tam">
      <button type="button" className="cd-ib cd-kucult" onClick={onKucult} aria-label="Oynatıcıyı küçült" title="Oynatıcıyı küçült"><ChevronDown aria-hidden /></button>
      <BaslaIpucu />
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
        <b>{no ? `${no} · ` : ''}{baslik}</b>
        <small>{hata || `Sesli ders · ${fmtSure(t)} / ${fmtSure(dur)}`}</small>
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
