/**
 * Canlı ders ekranı (/canliders/<key>): üç görünüm — Metin, Metin + PDF (bölünmüş: masaüstünde yan yana, telefonda üst-alt),
 * yalnız PDF (seçim cihazda saklanır). Tam ekran: kabuk gizlenir, oynatıcı saklanır ama tek dokunuşla açılır.
 * Metin sesle akar (etkin paragraf + tahmini cümle vurgusu), görünüm etkin paragrafı ortada tutar; kullanıcı elle
 * kaydırınca/PDF'i gezince takip 8 sn durur ve "Canlı konuma dön" çıkar. Oynatıcı alt çubuktadır (CanliDersDock).
 */
import CanliDersKimlikHedef from './CanliDersKimlikHedef';
import React, { Suspense, lazy, memo, useCallback, useMemo, useEffect, useLayoutEffect, useRef, useState } from 'react';
import { ArrowLeftRight, ArrowUpDown, ChevronDown, ChevronLeft, ChevronUp, Check, Columns2, Copy, Crosshair, FileText, Maximize2, Minimize2, Minus, Pause, Play, Plus, RotateCcw, Rows2, ScrollText } from 'lucide-react';
import { navigateTo, pathFor } from '../../router';
import { driveViewUrl, useDeckPdf } from '../../services/deckPdfService';
import { releasePageFullscreen, wasRecentlyScrollingOrTouching } from '../../utils/fullscreen';
import { lockScroll, unlockScroll } from '../../utils/scrollLock';
import { isIosBrowserTab, shouldAvoidNativeFullscreen } from '../../utils/device';
import { openPwaInstallGuide } from '../../services/pwaService';
import {
  cdCumleAraligi, cdCumleIlerleme, cdDetayBagla, cdDetayGetir, cdDurum, cdOynat, cdParagrafa, cdTercihVaryant, cdToggle, fmtSure, useCd, type CdDetay,
} from './canliDersStore';
import { useCdTur } from './useCdTur';
import { cdDersEtiketi } from './canliDersKategori';
import { ListeEkleDugme } from './CanliDersListem';
import { CevrimdisiDugme } from './CanliDersCevrimdisi';
import { CdDaha } from './CanliDersDaha';
import { CdTvKumanda } from './CanliDersTv';
import { MetniAktarDugme } from './CanliDersAktarDugme';
import { Highlighter, Star } from 'lucide-react';
import { useKonuSayaci } from '../../services/calismaTakip';
import { KonuDugmeleri } from '../takip/KonuTakip';
import { toast } from '../ui/Toast';
import { useYildizliMi, useYildizliSayisi, yildizToggle } from '../../services/yildizliParagrafStore';
import { YildizliParagraflarModal } from '../study/YildizliParagraflarModal';
import '../learn/pdf/pdfDoc.css';

/** iPhone/iPad'de tarayıcı sekmesinde adres çubuğu gizlenemez: gerçek tam ekran için PWA'yı öner. */
let pwaIpucuGosterildi = false;
function pwaIpucu() {
  if (pwaIpucuGosterildi || !isIosBrowserTab()) return;
  pwaIpucuGosterildi = true;
  toast.info(
    'Tam ekran modu açıldı',
    'Adres çubuğunu da tamamen gizlemek için uygulamayı Ana Ekrana ekleyebilirsin.',
    { label: 'Nasıl eklenir?', onClick: () => openPwaInstallGuide() },
  );
}

/** Öğenin görünür ölçeği (v12 yazı boyutu CSS zoom'u); utils/uiZoom.elementZoom ile aynı mantık. */
function elementZoom(el: Element | null | undefined): number {
  if (!el) return 1;
  const z = (el as Element & { currentCSSZoom?: number }).currentCSSZoom;
  if (typeof z === 'number' && z > 0) return z;
  const h = el as HTMLElement;
  if (h.offsetWidth > 0) {
    const r = el.getBoundingClientRect().width / h.offsetWidth;
    if (r > 0 && Number.isFinite(r)) return r;
  }
  return 1;
}

const PdfDocView = lazy(() => import('../learn/pdf/PdfDocView'));
import type { PdfMarks } from '../learn/pdf/PdfDocView';

const TAKIP_ARA = 8000;

/** Kullanıcı elle gezince takibi 8 sn duraklatır; süre dolunca ya da "Canlı konuma dön" ile sürer. */
function useTakip() {
  const [durdu, setDurdu] = useState(false);
  const timer = useRef(0);
  const durdur = useCallback(() => {
    setDurdu(true);
    window.clearTimeout(timer.current);
    timer.current = window.setTimeout(() => setDurdu(false), TAKIP_ARA);
  }, []);
  const surdur = useCallback(() => {
    window.clearTimeout(timer.current);
    setDurdu(false);
  }, []);
  useEffect(() => () => window.clearTimeout(timer.current), []);
  return { durdu, durdur, surdur };
}

const genisMi = () => typeof window !== 'undefined' && window.matchMedia('(min-width: 900px)').matches;

type Gorunum = 'metin' | 'ikisi' | 'pdf';
const GORUNUM_KEY = 'medsoru_canli_ders_gorunum';
/** Kayıtlı görünüm; yoksa geniş ekranda bölünmüş, telefonda metin */
const ilkGorunum = (): Gorunum => {
  try {
    const v = localStorage.getItem(GORUNUM_KEY);
    if (v === 'metin' || v === 'ikisi' || v === 'pdf') return v;
  } catch { /* yok */ }
  return genisMi() ? 'ikisi' : 'metin';
};
const GORUNUMLER: { id: Gorunum; ad: string; ikon: React.ReactNode }[] = [
  { id: 'metin', ad: 'Metin', ikon: <ScrollText aria-hidden /> },
  { id: 'ikisi', ad: 'Metin + PDF', ikon: <Columns2 aria-hidden /> },
  { id: 'pdf', ad: 'PDF', ikon: <FileText aria-hidden /> },
];

/** Tam ekran metin yazı boyutu (px), cihazda saklanır */
const YAZI_KEY = 'medsoru_canli_ders_tam_yazi';
const YAZI_ENAZ = 14;
const YAZI_ENCOK = 40;

/** Metin + PDF bölünmüş ekran dinamik boyut ve düzen tercihleri */
type BolmeYon = 'oto' | 'yan-yana' | 'ust-alt';
const BOLME_ORAN_KEY = 'medsoru_canli_ders_bolme_oran';
const BOLME_YON_KEY = 'medsoru_canli_ders_bolme_yon';
const BOLME_TERS_KEY = 'medsoru_canli_ders_bolme_ters';
const ORAN_MIN = 20;
const ORAN_MAX = 80;
const oranSinirla = (v: number) => Math.max(ORAN_MIN, Math.min(ORAN_MAX, Math.round(v)));

const VURGU_ANAHTAR = 'medsoru_canli_ders_vurgu_v1';

function useVurguAcik(): [boolean, (v: boolean) => void] {
  const [v, setV] = useState(() => { try { return localStorage.getItem(VURGU_ANAHTAR) !== '0'; } catch { return true; } });
  return [v, (x: boolean) => { setV(x); try { localStorage.setItem(VURGU_ANAHTAR, x ? '1' : '0'); } catch { /* yok */ } }];
}

export default function CanliDersDers({ dersKey }: { dersKey: string }) {
  const [vurguAcik, setVurguAcik] = useVurguAcik();
  // Bitirdiklerim: ses çalarken süreyi depo sayar; duraklatılmışken metni/slaytı okumak da bu derse sayılır
  const buDersCaliyor = useCd((s) => s.key === dersKey && s.playing);
  useKonuSayaci('sesli', buDersCaliyor ? null : dersKey);
  const [detay, setDetay] = useState<CdDetay | null>(null);
  const [hata, setHata] = useState<string | null>(null);
  const [baglanti, setBaglanti] = useState<'bagli' | 'yuklendi' | 'baska' | null>(null);
  const [genis, setGenis] = useState(genisMi);
  const [gorunum, setGorunumDurum] = useState<Gorunum>(ilkGorunum);
  const setGorunum = (g: Gorunum) => {
    setGorunumDurum(g);
    try { localStorage.setItem(GORUNUM_KEY, g); } catch { /* yok */ }
  };

  // Metin + PDF bölünmüş ekran dinamik boyut (%20-%80), yön (yan yana / üst-alt) ve sıra (PDF ↔ Metin)
  const [bolmeOran, setBolmeOranDurum] = useState<number>(() => {
    try {
      const n = Number(localStorage.getItem(BOLME_ORAN_KEY));
      if (Number.isFinite(n) && n >= ORAN_MIN && n <= ORAN_MAX) return Math.round(n);
    } catch { /* yok */ }
    return 50;
  });
  const setBolmeOran = useCallback((n: number | ((prev: number) => number)) => {
    setBolmeOranDurum((prev) => {
      const v = oranSinirla(typeof n === 'function' ? n(prev) : n);
      try { localStorage.setItem(BOLME_ORAN_KEY, String(v)); } catch { /* yok */ }
      return v;
    });
  }, []);

  const [bolmeYon, setBolmeYonDurum] = useState<BolmeYon>(() => {
    try {
      const v = localStorage.getItem(BOLME_YON_KEY);
      if (v === 'oto' || v === 'yan-yana' || v === 'ust-alt') return v;
    } catch { /* yok */ }
    return 'oto';
  });
  const setBolmeYon = useCallback((y: BolmeYon) => {
    setBolmeYonDurum(y);
    try { localStorage.setItem(BOLME_YON_KEY, y); } catch { /* yok */ }
  }, []);

  const [bolmeTers, setBolmeTersDurum] = useState<boolean>(() => {
    try { return localStorage.getItem(BOLME_TERS_KEY) === '1'; } catch { return false; }
  });
  const setBolmeTers = useCallback((t: boolean | ((prev: boolean) => boolean)) => {
    setBolmeTersDurum((prev) => {
      const v = typeof t === 'function' ? t(prev) : t;
      try { localStorage.setItem(BOLME_TERS_KEY, v ? '1' : '0'); } catch { /* yok */ }
      return v;
    });
  }, []);

  const [tamEkran, setTamEkran] = useState(() => document.documentElement.classList.contains('is-app-fullscreen'));
  const hadNativeFsRef = useRef(false);
  const [yazi, setYaziDurum] = useState<number>(() => { try { return Number(localStorage.getItem(YAZI_KEY)) || 20; } catch { return 20; } });
  const setYazi = (n: number | ((y: number) => number)) => setYaziDurum((y) => {
    const v = Math.min(YAZI_ENCOK, Math.max(YAZI_ENAZ, typeof n === 'function' ? n(y) : n));
    try { localStorage.setItem(YAZI_KEY, String(v)); } catch { /* yok */ }
    return v;
  });
  const [oynaticiAcik, setOynaticiAcik] = useState(true);
  const [yildizModalAcik, setYildizModalAcik] = useState(false);
  const yildizSayisi = useYildizliSayisi();
  const rootRef = useRef<HTMLDivElement>(null);
  const govdeRef = useRef<HTMLDivElement>(null);
  const [yuk, setYuk] = useState<number | null>(null);
  const caliyorKey = useCd((s) => s.key);
  const caliyorBaslik = useCd((s) => s.baslik);
  const tanitim = useCdTur('ders', !!detay, () => !!document.querySelector('.cd-dock') && !!document.querySelector('.cd-metin p'));

  // Deeplink ile gelen paragraf (?p=N ya da #p-N): o paragrafa kaydır ve hedef vurgusu ver
  const kaydirParagrafa = useCallback((pIdx: number) => {
    if (isNaN(pIdx) || pIdx < 0) return;
    const el = rootRef.current?.querySelector<HTMLElement>(`.cd-p[data-i="${pIdx}"]`);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'center' });
      el.classList.remove('is-hedef');
      void el.offsetWidth;
      el.classList.add('is-hedef');
      setTimeout(() => el.classList.remove('is-hedef'), 3000);
    }
  }, []);

  useEffect(() => {
    if (!detay) return;
    const sp = new URLSearchParams(window.location.search);
    const pStr = sp.get('p') || (window.location.hash.startsWith('#p-') ? window.location.hash.replace('#p-', '') : null);
    if (!pStr) return;
    const pIdx = parseInt(pStr, 10);
    const t = setTimeout(() => kaydirParagrafa(pIdx), 400);
    return () => clearTimeout(t);
  }, [detay, kaydirParagrafa]);

  useEffect(() => {
    const onPop = () => {
      const sp = new URLSearchParams(window.location.search);
      const pStr = sp.get('p') || (window.location.hash.startsWith('#p-') ? window.location.hash.replace('#p-', '') : null);
      if (!pStr) return;
      kaydirParagrafa(parseInt(pStr, 10));
    };
    window.addEventListener('popstate', onPop);
    return () => window.removeEventListener('popstate', onPop);
  }, [kaydirParagrafa]);

  useEffect(() => {
    let canli = true;
    setHata(null);
    cdDetayGetir(dersKey).then(
      (d) => {
        if (!canli) return;
        setDetay(d);
        setBaglanti(cdDetayBagla(d));
        document.title = `${cdDersEtiketi(d)} · ${d.baslik} · Sesli ders · MeDSor`;
      },
      (e) => canli && setHata(e?.message || 'Ders açılamadı.'),
    );
    return () => { canli = false; };
  }, [dersKey]);
  // Başka ders bitip kapanınca bu ders bağlanabilir
  useEffect(() => {
    if (detay && caliyorKey !== detay.key && !cdDurum().playing && baglanti === 'baska') setBaglanti(cdDetayBagla(detay));
  }, [caliyorKey, detay, baglanti]);
  const buDers = !!detay && caliyorKey === detay.key;

  useEffect(() => {
    const mq = window.matchMedia('(min-width: 900px)');
    const on = () => setGenis(mq.matches);
    mq.addEventListener('change', on);
    return () => mq.removeEventListener('change', on);
  }, []);

  // Tam ekran: kabuk (menü, üst çubuk, alt sekmeler) gizlenir; oynatıcı ve ilerleme çubuğu varsayılan olarak açıktır.
  // iOS/iPadOS WebKit'te tarayıcı native fullscreen dikey kaydırmada otomatik çıktığı için yalnız masaüstü/Android'de istenir.
  useEffect(() => {
    const kok = document.documentElement;
    kok.classList.toggle('cd-tam-ekran', tamEkran);
    kok.classList.toggle('cd-tam-oynatici', tamEkran && oynaticiAcik);
    window.dispatchEvent(new Event('cd:tam-ekran'));
    window.dispatchEvent(new Event('cd:dock'));
    const onFs = () => {
      const d = document as any;
      const fs = Boolean(d.fullscreenElement || d.webkitFullscreenElement);
      const appFs = kok.classList.contains('is-app-fullscreen');
      if (fs) {
        hadNativeFsRef.current = true;
        if (!tamEkran) {
          setOynaticiAcik(true);
          setTamEkran(true);
        }
      } else if (hadNativeFsRef.current) {
        hadNativeFsRef.current = false;
        // Kaydırma sırasında tetiklenen tarayıcı tam ekran çıkışlarında sayfa içi tam ekranda kal!
        if (!wasRecentlyScrollingOrTouching()) {
          kok.classList.remove('is-app-fullscreen');
          setTamEkran(false);
        }
      } else if (appFs && !tamEkran) {
        setOynaticiAcik(true);
        setTamEkran(true);
      }
    };
    document.addEventListener('fullscreenchange', onFs);
    document.addEventListener('webkitfullscreenchange', onFs);
    window.addEventListener('medsor:fullscreenchange', onFs);
    if (!tamEkran) {
      return () => {
        document.removeEventListener('fullscreenchange', onFs);
        document.removeEventListener('webkitfullscreenchange', onFs);
        window.removeEventListener('medsor:fullscreenchange', onFs);
      };
    }
    const onKey = (e: KeyboardEvent) => {
      const hedef = e.target as HTMLElement | null;
      if (!e.ctrlKey && !e.metaKey && !e.altKey && !hedef?.closest('input, textarea, [contenteditable="true"]')) {
        if (e.key === '+' || e.key === '=') { e.preventDefault(); setYazi((y) => y + 2); return; }
        if (e.key === '-') { e.preventDefault(); setYazi((y) => y - 2); return; }
      }
      if (e.key !== 'Escape' || document.querySelector('.cd-tur, .gu-ortu, [role="dialog"][aria-modal="true"]')) return;
      kok.classList.remove('is-app-fullscreen');
      setTamEkran(false);
    };
    document.addEventListener('keydown', onKey);
    return () => {
      document.removeEventListener('keydown', onKey);
      document.removeEventListener('fullscreenchange', onFs);
      document.removeEventListener('webkitfullscreenchange', onFs);
      window.removeEventListener('medsor:fullscreenchange', onFs);
    };
  }, [tamEkran, oynaticiAcik]);
  // Tam ekranda belge kaymasın: iOS Safari/Chrome adres çubuğunu geri getiren lastik kaydırma engellenir.
  useEffect(() => {
    if (!tamEkran) return;
    lockScroll();
    return () => unlockScroll();
  }, [tamEkran]);
  useEffect(() => () => {
    document.documentElement.classList.remove('cd-tam-ekran', 'cd-tam-oynatici');
    // Sayfa geçişinde tam ekran korunur, aksi hâlde kapanır.
    if (document.documentElement.classList.contains('is-app-fullscreen') || (document as any).fullscreenElement || (document as any).webkitFullscreenElement) releasePageFullscreen();
  }, []);
  const tamEkranAc = () => {
    setOynaticiAcik(true);
    setTamEkran(true);
    const kok = document.documentElement as HTMLElement & {
      webkitRequestFullscreen?: () => Promise<void> | void;
      webkitRequestFullScreen?: () => Promise<void> | void;
    };
    kok.classList.add('is-app-fullscreen', 'cd-tam-ekran', 'cd-tam-oynatici');
    try {
      window.scrollTo({ top: 0, left: 0, behavior: 'instant' as ScrollBehavior });
    } catch {
      window.scrollTo(0, 0);
    }
    if (shouldAvoidNativeFullscreen()) {
      return;
    }
    const req = kok.requestFullscreen || kok.webkitRequestFullscreen || kok.webkitRequestFullScreen;
    if (!req) {
      pwaIpucu();
      return;
    }
    try {
      const res = req.call(kok, { navigationUI: 'hide' } as FullscreenOptions);
      if (res && typeof (res as Promise<void>).catch === 'function') {
        (res as Promise<void>).catch(() => {});
      }
    } catch {
      try {
        req.call(kok);
      } catch {
        pwaIpucu();
      }
    }
  };
  const tamEkranKapat = () => {
    hadNativeFsRef.current = false;
    document.documentElement.classList.remove('is-app-fullscreen', 'cd-tam-ekran', 'cd-tam-oynatici');
    setTamEkran(false);
    const d = document as any;
    if (d.fullscreenElement || d.webkitFullscreenElement) {
      void (d.exitFullscreen || d.webkitExitFullscreen || d.webkitCancelFullScreen)?.call(d)?.catch?.(() => {});
    }
    window.dispatchEvent(new CustomEvent('medsor:fullscreenchange', { detail: { active: false } }));
  };

  // Sayfa içinde sabit yükseklik: üst çubuk ile alt oynatıcı/sekme çubuğu arasını doldurur (bölmeler kendi kayar)
  useLayoutEffect(() => {
    const el = rootRef.current;
    if (!el) return;
    let t = 0;
    const olc = () => {
      t = 0;
      const r = el.getBoundingClientRect();
      const top = r.top + window.scrollY; // belge konumu: sayfa en üstteyken görünür üst kenar
      // Bölmeler görünür alanın altına kadar uzanır; oynatıcı ve alt gezinme üstlerinde yüzen kart olarak durur.
      // Kartların kapladığı alt şerit kayan alanlara iç boşluk (--cd-ortu) olarak verilir: son satır kartın üstüne gelir.
      const ekranAlt = window.visualViewport?.height || window.innerHeight;
      let ust = ekranAlt;
      for (const sel of ['.cd-dock', '.s12-tabs, .sh-tabs', '.a13-island-wrap']) {
        const k = document.querySelector<HTMLElement>(sel);
        if (!k || getComputedStyle(k).display === 'none') continue;
        const kr = k.getBoundingClientRect();
        if (kr.height > 0 && kr.top < ust) ust = kr.top;
      }
      const z = elementZoom(el) || 1;
      el.style.setProperty('--cd-ortu', `${Math.max(0, Math.round((ekranAlt - ust) / z))}px`);
      setYuk(Math.max(180, (ekranAlt - Math.max(0, top) - 8) / z));
    };
    const plan = () => { if (!t) t = window.setTimeout(olc, 30); };
    olc();
    window.addEventListener('resize', plan);
    window.addEventListener('cd:dock', plan);
    window.addEventListener('cd:tam-ekran', plan);
    window.addEventListener('medsor:fullscreenchange', plan);
    document.addEventListener('fullscreenchange', plan);
    document.addEventListener('webkitfullscreenchange', plan);
    const ro = new ResizeObserver(plan);
    ro.observe(document.documentElement);
    document.documentElement.classList.add('cd-ders-acik');
    return () => {
      window.clearTimeout(t);
      window.removeEventListener('resize', plan);
      window.removeEventListener('cd:dock', plan);
      window.removeEventListener('cd:tam-ekran', plan);
      window.removeEventListener('medsor:fullscreenchange', plan);
      document.removeEventListener('fullscreenchange', plan);
      document.removeEventListener('webkitfullscreenchange', plan);
      ro.disconnect();
      document.documentElement.classList.remove('cd-ders-acik');
    };
  }, [detay]);

  if (hata) {
    return (
      <div className="cd-root">
        <GeriBag />
        <div className="cd-bos">
          <p>{hata}</p>
          <button type="button" className="cd-btn is-ana" onClick={() => navigateTo(pathFor('canli_ders'))}>Tüm sesli derslere dön</button>
        </div>
      </div>
    );
  }
  if (!detay) {
    return (
      <div className="cd-root">
        <GeriBag />
        <div className="cd-bos" role="status"><span className="cd-spin" aria-hidden /> Ders yükleniyor…</div>
      </div>
    );
  }

  const pdfVar = !!detay.pdf && detay.pdf.dosyalar.length > 0;
  const mod: Gorunum = pdfVar ? gorunum : 'metin';
  const metinGoster = mod !== 'pdf';
  const pdfGoster = mod !== 'metin';
  const aktifYon: 'yan-yana' | 'ust-alt' = bolmeYon === 'oto' ? (genis ? 'yan-yana' : 'ust-alt') : bolmeYon;
  const pdfOran = bolmeTers ? 100 - bolmeOran : bolmeOran;
  const metinOran = 100 - pdfOran;

  const setPdfOranHedef = (hedefPdf: number) => {
    setBolmeOran(bolmeTers ? 100 - hedefPdf : hedefPdf);
  };

  const govdeStil: React.CSSProperties | undefined = mod === 'ikisi'
    ? (aktifYon === 'yan-yana'
      ? { gridTemplateColumns: `minmax(0, ${bolmeOran}fr) 14px minmax(0, ${100 - bolmeOran}fr)`, gridTemplateRows: 'minmax(0, 1fr)' }
      : { gridTemplateColumns: 'minmax(0, 1fr)', gridTemplateRows: `minmax(0, ${bolmeOran}fr) 14px minmax(0, ${100 - bolmeOran}fr)` })
    : undefined;

  const birinciBolme = bolmeTers
    ? <CdMetinBolme key="metin" detay={detay} canli={buDers} />
    : <CdPdfBolme key="pdf" detay={detay} canli={buDers} />;
  const ikinciBolme = bolmeTers
    ? <CdPdfBolme key="pdf" detay={detay} canli={buDers} />
    : <CdMetinBolme key="metin" detay={detay} canli={buDers} />;

  return (
    <div
      className={`cd-root cd-ders is-${mod}${tamEkran ? ' is-tam' : ''}${vurguAcik ? '' : ' cd-vurgu-kapali'}`}
      ref={rootRef}
      style={tamEkran ? ({ '--cd-tam-yazi': `${yazi}px` } as React.CSSProperties) : yuk ? { height: yuk } : undefined}
    >
      <header className="cd-ders-bas">
        <GeriBag />
        <h1 className="cd-ders-ad" title={`${cdDersEtiketi(detay)} · ${detay.baslik}`}><span>{cdDersEtiketi(detay)} ·</span> {detay.baslik}</h1>
        <div className="cd-ders-arac">
          {pdfVar && (
            <div className="cd-sekmeler" role="radiogroup" aria-label="Görünüm">
              {GORUNUMLER.map((g) => (
                <button
                  key={g.id}
                  type="button"
                  role="radio"
                  aria-checked={mod === g.id}
                  className={mod === g.id ? 'is-on' : ''}
                  onClick={() => setGorunum(g.id)}
                  title={g.ad}
                >
                  {g.ikon} <span>{g.ad}</span>
                </button>
              ))}
            </div>
          )}
          {mod === 'ikisi' && (
            <div className="cd-duzen-arac" role="group" aria-label="Metin ve PDF bölme düzeni ve boyutu">
              <button
                type="button"
                className="cd-duzen-btn"
                onClick={() => setBolmeYon(aktifYon === 'yan-yana' ? 'ust-alt' : 'yan-yana')}
                title={aktifYon === 'yan-yana' ? 'Üst-alt düzene geç' : 'Yan yana düzene geç'}
                aria-label={aktifYon === 'yan-yana' ? 'Üst-alt düzene geç' : 'Yan yana düzene geç'}
              >
                {aktifYon === 'yan-yana' ? <Rows2 aria-hidden /> : <Columns2 aria-hidden />}
                <span className="cd-duzen-etiket">{aktifYon === 'yan-yana' ? 'Üst-Alt' : 'Yan Yana'}</span>
              </button>
              <button
                type="button"
                className={`cd-duzen-btn${bolmeTers ? ' is-on' : ''}`}
                onClick={() => setBolmeTers((t) => !t)}
                title={bolmeTers ? 'Konumu değiştir (Şu an: Metin önce, PDF sonra)' : 'Konumu değiştir (Şu an: PDF önce, Metin sonra)'}
                aria-label="Metin ve PDF yerini değiştir"
              >
                {aktifYon === 'yan-yana' ? <ArrowLeftRight aria-hidden /> : <ArrowUpDown aria-hidden />}
                <span className="cd-duzen-etiket">{bolmeTers ? 'Metin⇄PDF' : 'PDF⇄Metin'}</span>
              </button>
              <div className="cd-oran-grup" role="group" aria-label="PDF ve Metin boyut oranı">
                {[
                  { pdf: 35, ad: 'Metin+' },
                  { pdf: 50, ad: '50:50' },
                  { pdf: 65, ad: 'PDF+' },
                ].map((p) => {
                  const secili = Math.abs(pdfOran - p.pdf) <= 4;
                  return (
                    <button
                      key={p.pdf}
                      type="button"
                      className={`cd-oran-hap${secili ? ' is-on' : ''}`}
                      onClick={() => setPdfOranHedef(p.pdf)}
                      title={`PDF %${p.pdf} · Metin %${100 - p.pdf}`}
                      aria-pressed={secili}
                    >
                      {p.ad}
                    </button>
                  );
                })}
              </div>
            </div>
          )}
        </div>
        <div className="cd-ders-uc">
          {!tamEkran && (
            <KonuDugmeleri kucuk className="cd-ders-takip" modul="sesli" konu={detay.key} ad={detay.baslik}
              onTekrar={() => { const v = cdTercihVaryant(detay.varyantlar); if (v) cdOynat(detay, v.id, { t: 0 }); }} />
          )}
          {!tamEkran && (
            <button
              type="button"
              className={`cd-btn cd-btn-yildizli${yildizSayisi > 0 ? ' is-on' : ''}`}
              onClick={() => setYildizModalAcik(true)}
              title="Yıldızlı paragraflar (Tekrar listem)"
              aria-label={`Yıldızlı paragraflar${yildizSayisi > 0 ? ` (${yildizSayisi})` : ''}`}
              data-sayi={yildizSayisi > 0 ? (yildizSayisi > 99 ? '99+' : String(yildizSayisi)) : undefined}
            >
              <Star className="w-4 h-4" fill={yildizSayisi > 0 ? '#f59e0b' : 'none'} color={yildizSayisi > 0 ? '#f59e0b' : 'currentColor'} aria-hidden />
              <span>Yıldızlılar{yildizSayisi > 0 ? ` (${yildizSayisi})` : ''}</span>
            </button>
          )}
          {!tamEkran && (
            <CdDaha etiket="Ders seçenekleri (çevrimdışı, listem, metni dışa aktar, tanıtım)" className="cd-ders-daha">
              <button
                type="button"
                className="cd-btn"
                onClick={() => setYildizModalAcik(true)}
              >
                <Star aria-hidden /> <span>Yıldızlı paragraflar ({yildizSayisi})</span>
              </button>
              <CevrimdisiDugme dersKey={detay.key} baslik={detay.baslik} varyantlar={detay.varyantlar} />
              <ListeEkleDugme dersKey={detay.key} baslik={detay.baslik} etiketli />
              <MetniAktarDugme detay={detay} vurguAcik={vurguAcik} />
              {detay.vurgu && (
                <button type="button" className={`cd-btn${vurguAcik ? ' is-on' : ''}`} aria-pressed={vurguAcik} onClick={() => setVurguAcik(!vurguAcik)}
                  title="Çıkmışta, örnek sorularda ve spotlarda geçen cümleleri kırmızı ve işaretli göster">
                  <Highlighter aria-hidden /> <span>Önemli yerleri vurgula</span>
                </button>
              )}
              {tanitim.dugme}
            </CdDaha>
          )}
          {tamEkran ? (
            <>
              {metinGoster && (
                <span className="cd-yazi" role="group" aria-label="Yazı boyutu">
                  <button type="button" className="cd-btn is-ikon" onClick={() => setYazi(yazi - 2)} disabled={yazi <= YAZI_ENAZ} aria-label="Yazıyı küçült" title="Yazıyı küçült (−)">
                    <span aria-hidden className="cd-yazi-a is-kucuk">A</span>
                  </button>
                  <button type="button" className="cd-yazi-n" onClick={() => setYazi(20)} title="Varsayılan boyut" aria-label={`Yazı boyutu ${yazi} piksel, varsayılana dön`}>{yazi}</button>
                  <button type="button" className="cd-btn is-ikon" onClick={() => setYazi(yazi + 2)} disabled={yazi >= YAZI_ENCOK} aria-label="Yazıyı büyüt" title="Yazıyı büyüt (+)">
                    <span aria-hidden className="cd-yazi-a">A</span>
                  </button>
                </span>
              )}
              {!oynaticiAcik && <TamEkranOynat dersKey={detay.key} onBasla={() => { cdOynat(detay); setBaglanti('bagli'); }} onAc={() => setOynaticiAcik(true)} />}
              <button
                type="button"
                className={`cd-btn is-ikon cd-tam-oyn${oynaticiAcik ? ' is-on' : ''}`}
                onClick={() => setOynaticiAcik((x) => !x)}
                aria-pressed={oynaticiAcik}
                aria-label={oynaticiAcik ? 'Oynatıcıyı gizle' : 'Oynatıcıyı göster'}
                title={oynaticiAcik ? 'Oynatıcıyı gizle' : 'Oynatıcıyı göster'}
              >
                {oynaticiAcik ? <ChevronDown aria-hidden /> : <ChevronUp aria-hidden />}
              </button>
              <button type="button" className="cd-btn is-ikon" onClick={tamEkranKapat} aria-label="Tam ekrandan çık" title="Tam ekrandan çık (Esc)">
                <Minimize2 aria-hidden />
              </button>
            </>
          ) : (
            <button type="button" className="cd-btn is-ikon cd-tam-btn" onClick={tamEkranAc} aria-label="Tam ekran" title="Tam ekran">
              <Maximize2 aria-hidden />
            </button>
          )}
        </div>
      </header>
      {baglanti === 'baska' && !buDers && (
        <div className="cd-uyari">
          <span>Şu an çalan: <b>{caliyorBaslik}</b></span>
          <button type="button" className="cd-btn is-ana" onClick={() => { cdOynat(detay); setBaglanti('bagli'); }}>
            <Play aria-hidden /> Bu dersi dinle
          </button>
        </div>
      )}
      <div
        ref={govdeRef}
        className={`cd-govde${mod === 'ikisi' ? (aktifYon === 'yan-yana' ? ' is-iki' : ' is-ust-alt') : ''}`}
        style={govdeStil}
      >
        {mod === 'ikisi' ? (
          <>
            {birinciBolme}
            <CdBolmeAyrac
              govdeRef={govdeRef}
              yon={aktifYon}
              oran={bolmeOran}
              ters={bolmeTers}
              pdfOran={pdfOran}
              metinOran={metinOran}
              onOran={setBolmeOran}
              onTers={() => setBolmeTers((t) => !t)}
              onYon={() => setBolmeYon(aktifYon === 'yan-yana' ? 'ust-alt' : 'yan-yana')}
            />
            {ikinciBolme}
          </>
        ) : (
          <>
            {pdfGoster && <CdPdfBolme detay={detay} canli={buDers} />}
            {metinGoster && <CdMetinBolme detay={detay} canli={buDers} />}
          </>
        )}
      </div>
      {tanitim.tur}
      <CanliDersKimlikHedef detay={detay} kok={rootRef} />
      {yildizModalAcik && (
        <YildizliParagraflarModal
          onClose={() => setYildizModalAcik(false)}
          onGecis={(item) => {
            if (item.kaynak === 'canli_ders' && item.meta?.dersKey === dersKey && item.meta?.paragrafIndex !== undefined) {
              kaydirParagrafa(item.meta.paragrafIndex);
              return true;
            }
            return false;
          }}
        />
      )}
    </div>
  );
}

/** Metin + PDF arasında sürüklenebilir, dokunmatik ve klavye destekli dinamik boyut ayırıcı */
function CdBolmeAyrac({
  govdeRef,
  yon,
  oran,
  ters,
  pdfOran,
  metinOran,
  onOran,
  onTers,
  onYon,
}: {
  govdeRef: React.RefObject<HTMLDivElement | null>;
  yon: 'yan-yana' | 'ust-alt';
  oran: number;
  ters: boolean;
  pdfOran: number;
  metinOran: number;
  onOran: (n: number | ((prev: number) => number)) => void;
  onTers: () => void;
  onYon: () => void;
}) {
  const [surukleniyor, setSurukleniyor] = useState(false);

  const konumdanOran = useCallback((clientX: number, clientY: number) => {
    const el = govdeRef.current;
    if (!el) return;
    const r = el.getBoundingClientRect();
    if (yon === 'yan-yana') {
      if (r.width <= 0) return;
      onOran(((clientX - r.left) / r.width) * 100);
    } else {
      if (r.height <= 0) return;
      onOran(((clientY - r.top) / r.height) * 100);
    }
  }, [govdeRef, yon, onOran]);

  const onPointerDown = (e: React.PointerEvent<HTMLDivElement>) => {
    if ((e.target as HTMLElement).closest('button')) return;
    e.preventDefault();
    e.currentTarget.setPointerCapture(e.pointerId);
    setSurukleniyor(true);
  };

  const onPointerMove = (e: React.PointerEvent<HTMLDivElement>) => {
    if (!surukleniyor) return;
    konumdanOran(e.clientX, e.clientY);
  };

  const onPointerEnd = (e: React.PointerEvent<HTMLDivElement>) => {
    if (!surukleniyor) return;
    if (e.currentTarget.hasPointerCapture(e.pointerId)) {
      e.currentTarget.releasePointerCapture(e.pointerId);
    }
    setSurukleniyor(false);
  };

  const onKeyDown = (e: React.KeyboardEvent<HTMLDivElement>) => {
    const ileri = yon === 'yan-yana' ? e.key === 'ArrowRight' : e.key === 'ArrowDown';
    const geri = yon === 'yan-yana' ? e.key === 'ArrowLeft' : e.key === 'ArrowUp';
    if (ileri) { e.preventDefault(); onOran((v) => v + 5); }
    else if (geri) { e.preventDefault(); onOran((v) => v - 5); }
    else if (e.key === 'Home') { e.preventDefault(); onOran(30); }
    else if (e.key === 'End') { e.preventDefault(); onOran(70); }
    else if (e.key === 'Enter' || e.key === '0') { e.preventDefault(); onOran(50); }
  };

  const birinciAd = ters ? 'Metin' : 'PDF';
  const ikinciAd = ters ? 'PDF' : 'Metin';
  const birinciYuzde = ters ? metinOran : pdfOran;
  const ikinciYuzde = ters ? pdfOran : metinOran;

  return (
    <div
      role="separator"
      tabIndex={0}
      aria-orientation={yon === 'yan-yana' ? 'vertical' : 'horizontal'}
      aria-label="Metin ve PDF bölme boyutunu ayarla (sürükle, ok tuşlarıyla kaydır, çift tıkla sıfırla)"
      aria-valuenow={oran}
      aria-valuemin={ORAN_MIN}
      aria-valuemax={ORAN_MAX}
      title="Sürükleyerek boyutu ayarla · Çift tıkla %50/%50 eşitle"
      className={`cd-ayrac is-${yon}${surukleniyor ? ' is-surukleniyor' : ''}`}
      onPointerDown={onPointerDown}
      onPointerMove={onPointerMove}
      onPointerUp={onPointerEnd}
      onPointerCancel={onPointerEnd}
      onDoubleClick={() => onOran(50)}
      onKeyDown={onKeyDown}
    >
      <span className="cd-ayrac-tutamac" aria-hidden />
      <span className="cd-ayrac-deger" aria-hidden>
        {birinciAd} %{birinciYuzde} · {ikinciAd} %{ikinciYuzde}
      </span>
      <div className="cd-ayrac-hizli" onPointerDown={(e) => e.stopPropagation()}>
        <button type="button" onClick={() => onOran(35)} className={Math.abs(oran - 35) <= 4 ? 'is-on' : ''} title={`${birinciAd} %35 · ${ikinciAd} %65`}>35</button>
        <button type="button" onClick={() => onOran(50)} className={Math.abs(oran - 50) <= 4 ? 'is-on' : ''} title="Eşitle (%50 / %50)">50</button>
        <button type="button" onClick={() => onOran(65)} className={Math.abs(oran - 65) <= 4 ? 'is-on' : ''} title={`${birinciAd} %65 · ${ikinciAd} %35`}>65</button>
        <button type="button" onClick={onTers} title="PDF ve Metin yerini değiştir" aria-label="PDF ve Metin yerini değiştir">
          {yon === 'yan-yana' ? <ArrowLeftRight aria-hidden /> : <ArrowUpDown aria-hidden />}
        </button>
        <button type="button" onClick={onYon} title={yon === 'yan-yana' ? 'Üst-alt düzene geç' : 'Yan yana düzene geç'} aria-label="Bölme yönünü değiştir">
          {yon === 'yan-yana' ? <Rows2 aria-hidden /> : <Columns2 aria-hidden />}
        </button>
        {oran !== 50 && (
          <button type="button" onClick={() => onOran(50)} title="Varsayılan boyuta sıfırla (%50)" aria-label="Boyutu sıfırla">
            <RotateCcw aria-hidden />
          </button>
        )}
      </div>
    </div>
  );
}

/** Tam ekranda oynatıcı saklıyken başlıkta: oynat/duraklat + ilerleme çubuğu + geçen süre */
function TamEkranOynat({ dersKey, onBasla, onAc }: { dersKey: string; onBasla: () => void; onAc?: () => void }) {
  const buDers = useCd((s) => s.key === dersKey);
  const playing = useCd((s) => s.key === dersKey && s.playing);
  const t = useCd((s) => (s.key === dersKey ? Math.floor(s.t) : 0));
  const dur = useCd((s) => (s.key === dersKey ? s.dur : 0));
  const oran = dur > 0 ? Math.min(1, t / dur) : 0;
  return (
    <span className="cd-tam-ses">
      <button
        type="button"
        className="cd-tam-ses-bilgi"
        onClick={onAc}
        title="Oynatıcıyı aç"
        aria-label={`İlerleme: ${fmtSure(t)}${dur ? ` / ${fmtSure(dur)}` : ''}. Oynatıcıyı açmak için dokun`}
      >
        <span className="cd-tam-ses-t" aria-hidden>{fmtSure(t)}{dur ? ` / ${fmtSure(dur)}` : ''}</span>
        <span className="cd-ilerleme cd-tam-bar" aria-hidden><i style={{ transform: `scaleX(${oran})` }} /></span>
      </button>
      <button type="button" className="cd-oynat" onClick={() => (buDers ? cdToggle() : onBasla())} aria-label={playing ? 'Duraklat' : 'Oynat'} title={playing ? 'Duraklat' : 'Oynat'}>
        {playing ? <Pause aria-hidden /> : <Play aria-hidden />}
      </button>
    </span>
  );
}

function GeriBag() {
  return (
    <a
      className="cd-geri"
      href={pathFor('canli_ders')}
      onClick={(e) => {
        if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
        e.preventDefault();
        navigateTo(pathFor('canli_ders'));
      }}
    >
      <ChevronLeft aria-hidden /> <span>Sesli dersler</span>
    </a>
  );
}

/* ---------------- metin ---------------- */

const hlDestek = () => typeof CSS !== 'undefined' && 'highlights' in CSS && typeof (window as any).Highlight === 'function';
const HL_AD = 'cd-cumle';

/** Paragrafı panoya kopyalar; vurgu DOM'u değiştirdiği için metin p'den değil veriden alınır. */
function KopyalaDugme({ metin }: { metin: string }) {
  const [tamam, setTamam] = useState(false);
  const kopyala = async (e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await navigator.clipboard.writeText(metin);
      setTamam(true);
      window.setTimeout(() => setTamam(false), 1500);
    } catch {
      toast.error('Kopyalanamadı', 'Tarayıcı panoya erişime izin vermedi.');
    }
  };
  return (
    <button type="button" className={`cd-p-kopya${tamam ? ' is-tamam' : ''}`} onClick={kopyala}
      aria-label={tamam ? 'Kopyalandı' : 'Bu parçayı kopyala'} title={tamam ? 'Kopyalandı' : 'Kopyala'}>
      {tamam ? <Check aria-hidden /> : <Copy aria-hidden />}
    </button>
  );
}

type Vurgu = [number, number, 'c' | 't', number][];
const ONEM_AD: Record<number, string> = { 3: 'Çıkmışta sorulmuş', 2: 'Sınav spotu', 1: 'Örnek soruda geçiyor' };

/** Önemli cümleler (çıkmış/spot/örnek soruyla eşleşen) marker + kırmızı kalın; anahtar terimler ayrıca kalın. */
function VurguluMetin({ metin, v }: { metin: string; v?: Vurgu }) {
  if (!v?.length) return <>{metin}</>;
  const out: React.ReactNode[] = [];
  let k = 0;
  for (const [s, e, tur, onem] of v) {
    if (tur !== 'c' || s < k) continue;
    if (s > k) out.push(metin.slice(k, s));
    const ic: React.ReactNode[] = [];
    let j = s;
    for (const [ts, te, tt] of v) {
      if (tt !== 't' || ts < j || te > e) continue;
      if (ts > j) ic.push(metin.slice(j, ts));
      ic.push(<b key={ts} className="cd-terim">{metin.slice(ts, te)}</b>);
      j = te;
    }
    if (j < e) ic.push(metin.slice(j, e));
    out.push(<span key={s} className={`cd-onem o${onem}`} data-s={s} data-e={e} title={ONEM_AD[onem]}>{ic}</span>);
    k = e;
  }
  if (k < metin.length) out.push(metin.slice(k));
  return <>{out}</>;
}

/** Paragraf içi [s, e) karakter aralığını (iç içe öğeler dahil) kapsayan Range */
function metinAraligi(el: HTMLElement, s: number, e: number): Range | null {
  const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
  const r = document.createRange();
  let pos = 0, bas = false;
  for (let n = w.nextNode(); n; n = w.nextNode()) {
    const len = (n.textContent || '').length;
    if (!bas && s <= pos + len) { r.setStart(n, Math.max(0, s - pos)); bas = true; }
    if (bas && e <= pos + len) { r.setEnd(n, Math.max(0, e - pos)); return r; }
    pos += len;
  }
  return null;
}

function CdParagrafYildizDugme({
  dersKey,
  dersBaslik,
  bolumBaslik,
  paragrafIndex,
  metin,
}: {
  dersKey: string;
  dersBaslik: string;
  bolumBaslik?: string;
  paragrafIndex: number;
  metin: string;
}) {
  const yId = `cd_${dersKey}_p${paragrafIndex}`;
  const yildizli = useYildizliMi(yId);

  const toggle = (e: React.MouseEvent) => {
    e.stopPropagation();
    yildizToggle({
      id: yId,
      kaynak: 'canli_ders',
      kaynakAd: 'Sesli ders',
      baslik: dersBaslik,
      altBaslik: bolumBaslik,
      metin,
      deeplink: `${pathFor('canli_ders', dersKey)}?p=${paragrafIndex}`,
      meta: {
        dersKey,
        paragrafIndex,
      },
    });
  };

  return (
    <button
      type="button"
      className={`cd-p-yildiz${yildizli ? ' is-on' : ''}`}
      onClick={toggle}
      aria-label={yildizli ? 'Listemden çıkar' : 'Listeme ekle'}
      title={yildizli ? 'Yıldızlı (tekrar listesinde)' : 'Yıldızla (tekrar listesine ekle)'}
    >
      <Star fill={yildizli ? '#f59e0b' : 'none'} color={yildizli ? '#f59e0b' : 'currentColor'} aria-hidden />
    </button>
  );
}

/** Paragraf listesi bir kez çizilir; vurgu DOM üzerinden değişir (uzun metinde yeniden çizim yok). */
const MetinListe = memo(function MetinListe({ detay, onTik }: { detay: CdDetay; onTik: (i: number) => void }) {
  return (
    <>
      {detay.bolumler.map((b, bi) => (
        <section key={bi} className="cd-bolum" aria-label={b.baslik || `Bölüm ${bi + 1}`}>
          {b.baslik && <h2 className="cd-bolum-ad">{b.baslik}</h2>}
          {b.paragraflar.map((p) => (
            <div key={p.i} className="cd-p-sar">
              <p data-i={p.i} className="cd-p" onClick={() => onTik(p.i)}><VurguluMetin metin={p.metin} v={detay.vurgu?.[p.i]} /></p>
              <div className="cd-p-araclar">
                <CdParagrafYildizDugme
                  dersKey={detay.key}
                  dersBaslik={detay.baslik}
                  bolumBaslik={b.baslik}
                  paragrafIndex={p.i}
                  metin={p.metin}
                />
                <KopyalaDugme metin={p.metin} />
              </div>
            </div>
          ))}
        </section>
      ))}
    </>
  );
});

function CdMetinBolme({ detay, canli }: { detay: CdDetay; canli: boolean }) {
  const paneRef = useRef<HTMLDivElement>(null);
  const aktif = useCd((s) => (canli ? s.aktif : -1));
  const cumle = useCd((s) => (canli ? s.cumle : -1));
  const { durdu, durdur, surdur } = useTakip();
  const onceki = useRef<HTMLElement | null>(null);
  const isaret = useRef<{ el: HTMLElement; metin: string } | null>(null);
  const ilk = useRef(true);
  /** Programatik kaydırmanın sürdüğü an (bu süre dışındaki scroll olayları kullanıcınındır) */
  const progUntil = useRef(0);

  const onTik = useCallback((i: number) => {
    // Metin seçiliyse (kopyalama) atlama yapılmaz
    const sel = window.getSelection();
    if (sel && !sel.isCollapsed && sel.toString().trim()) return;
    if (cdDurum().key !== detay.key) cdOynat(detay, undefined, { oynat: false });
    cdParagrafa(i);
    // Dokunulan paragraftan sürerken takip de oradan devam eder (elle kaydırma sonrası "Canlı konuma dön" beklemeden)
    surdur();
  }, [detay, surdur]);

  const pEl = (i: number) => paneRef.current?.querySelector<HTMLElement>(`p[data-i="${i}"]`) || null;

  // Etkin paragraf sınıfı
  useEffect(() => {
    const el = aktif >= 0 ? pEl(aktif) : null;
    if (onceki.current && onceki.current !== el) onceki.current.classList.remove('is-on');
    if (el) el.classList.add('is-on');
    onceki.current = el;
  }, [aktif]);

  // Cümle vurgusu: CSS Highlight API (kapsamlı ::highlight), yoksa <mark> ile
  useEffect(() => {
    const destek = hlDestek();
    const temizle = () => {
      if (destek) (CSS as any).highlights.delete(HL_AD);
      const m = isaret.current;
      if (m) {
        m.el.innerHTML = m.metin;
        isaret.current = null;
      }
      paneRef.current?.querySelector('.cd-onem.is-canli')?.classList.remove('is-canli');
    };
    const el = aktif >= 0 ? pEl(aktif) : null;
    const r = el ? cdCumleAraligi(aktif, cumle) : null;
    if (!el || !r) return void temizle();
    // Okunan cümle önemliyse o an belirginleşir
    const onceki = paneRef.current?.querySelector<HTMLElement>('.cd-onem.is-canli');
    const simdi = [...el.querySelectorAll<HTMLElement>('.cd-onem')].find((o) => +o.dataset.s! < r[1] && +o.dataset.e! > r[0]) || null;
    if (onceki !== simdi) { onceki?.classList.remove('is-canli'); simdi?.classList.add('is-canli'); }
    if (destek) {
      const range = metinAraligi(el, r[0], r[1]);
      if (!range) return void temizle();
      (CSS as any).highlights.set(HL_AD, new (window as any).Highlight(range));
    } else {
      // Highlight API yoksa: <mark> sarılır, özgün işaretleme (önemli cümle spanları) saklanıp geri yüklenir
      const m = isaret.current;
      if (m) m.el.innerHTML = m.metin;
      const html = el.innerHTML;
      const range = metinAraligi(el, r[0], r[1]);
      const mk = document.createElement('mark');
      mk.className = 'cd-cumle';
      try { if (range) { mk.append(range.extractContents()); range.insertNode(mk); } } catch { /* bölünemeyen aralık: vurgusuz geç */ }
      isaret.current = { el, metin: html };
    }
  }, [aktif, cumle]);
  useEffect(() => () => {
    if (hlDestek()) (CSS as any).highlights.delete(HL_AD);
  }, []);

  // Otomatik kaydırma: etkin paragraf (uzunsa cümle) görünür alanın ortasına yakın
  const kaydirRef = useRef<(ani?: boolean) => void>(() => {});
  const kaydir = useCallback((ani = false) => {
    const pane = paneRef.current;
    const st = cdDurum();
    const el = st.aktif >= 0 ? pEl(st.aktif) : null;
    if (!pane || !el) return;
    const z = elementZoom(pane) || 1;
    const pr = pane.getBoundingClientRect();
    let hr = el.getBoundingClientRect();
    if (hr.height > pr.height * 0.6) {
      const m = el.querySelector('mark.cd-cumle');
      if (m) hr = m.getBoundingClientRect();
      else if (hlDestek()) {
        const hl = (CSS as any).highlights.get(HL_AD);
        const rg = hl && [...hl][0];
        if (rg) hr = (rg as Range).getBoundingClientRect();
      }
    }
    const merkez = (hr.top + hr.height / 2 - pr.top) / z;
    const hedefOrta = pane.clientHeight * 0.42;
    const sapma = merkez - hedefOrta;
    // Orta bant içindeyse dokunma (sürekli kıpırdamasın)
    if (!ani && Math.abs(sapma) < pane.clientHeight * 0.18) return;
    // Uzak atlama (bölüm geçişi, paragrafa dokunma): uzun yumuşak kaydırma iOS'ta yarıda kesilip yanlış yerde kalıyordu
    // → anında git, iki kare sonra ince ayar
    const uzak = Math.abs(sapma) > pane.clientHeight * 1.5;
    const hemen = ani || uzak;
    progUntil.current = Date.now() + (hemen ? 250 : 1000);
    pane.scrollTo({ top: Math.max(0, pane.scrollTop + sapma), behavior: hemen ? 'auto' : 'smooth' });
    if (uzak && !ani) requestAnimationFrame(() => requestAnimationFrame(() => kaydirRef.current(true)));
  }, []);
  kaydirRef.current = kaydir;
  useEffect(() => {
    if (!canli || durdu || aktif < 0) return;
    const ani = ilk.current;
    ilk.current = false;
    // İlk açılışta uzağa atlama: önce anında, sonra ince ayar (yazı tipi/yerleşim oturunca)
    const id = requestAnimationFrame(() => {
      kaydir(ani);
      if (ani) requestAnimationFrame(() => kaydir(true));
    });
    return () => cancelAnimationFrame(id);
  }, [aktif, cumle, durdu, canli, kaydir]);

  // Elle kaydırma algısı (programatik kaydırma bu olayları üretmez)
  useEffect(() => {
    const pane = paneRef.current;
    if (!pane) return;
    const on = () => durdur();
    const onDown = (e: PointerEvent) => { if (e.target === pane) durdur(); }; // kaydırma çubuğu
    const onKey = (e: KeyboardEvent) => { if (['PageUp', 'PageDown', 'Home', 'End', 'ArrowUp', 'ArrowDown'].includes(e.key)) durdur(); };
    // Diğer yollar (kaydırma çubuğu, erişilebilirlik araçları): bizim kaydırmamız dışında gelen scroll olayı
    const onScroll = () => {
      const n = Date.now();
      if (n <= progUntil.current) progUntil.current = Math.max(progUntil.current, n + 120); // yumuşak kaydırma sürüyor
      else durdur();
    };
    pane.addEventListener('scroll', onScroll, { passive: true });
    pane.addEventListener('wheel', on, { passive: true });
    pane.addEventListener('touchmove', on, { passive: true });
    pane.addEventListener('pointerdown', onDown);
    pane.addEventListener('keydown', onKey);
    return () => {
      pane.removeEventListener('wheel', on);
      pane.removeEventListener('touchmove', on);
      pane.removeEventListener('pointerdown', onDown);
      pane.removeEventListener('keydown', onKey);
      pane.removeEventListener('scroll', onScroll);
    };
  }, [durdur]);

  return (
    <div className="cd-bolme cd-metin-bolme">
      <div className="cd-metin" ref={paneRef} tabIndex={0} aria-label="Konuşma metni">
        <MetinListe detay={detay} onTik={onTik} />
      </div>
      {durdu && canli ? (
        <button type="button" className="cd-donus" onClick={() => { surdur(); requestAnimationFrame(() => kaydir()); }}>
          <Crosshair aria-hidden /> Canlı konuma dön
        </button>
      ) : (
        <BaslaCagri canli={canli} />
      )}
    </div>
  );
}

/** Ders ekranı ilk açıldığında (henüz çalmadıysa) ne yapılacağını söyleyen büyük düğme; ilk çalmadan sonra gizlenir. */
function BaslaCagri({ canli }: { canli: boolean }) {
  const playing = useCd((s) => canli && s.playing);
  const t = useCd((s) => (canli ? Math.floor(s.t) : 0));
  const [goster, setGoster] = useState(true);
  useEffect(() => { if (playing) setGoster(false); }, [playing]);
  if (!canli || !goster || playing) return null;
  const devam = t >= 5;
  const basla = () => {
    setGoster(false);
    cdToggle();
  };
  return (
    <div className="cd-basla" role="group" aria-label="Dinlemeye başla">
      <button type="button" className="cd-basla-btn" onClick={basla}>
        <span className="cd-basla-ikon" aria-hidden><Play /></span>
        <span>
          <b>{devam ? 'Kaldığın yerden devam et' : 'Dinlemeye başla'}</b>
          <small>{devam ? `${fmtSure(t)} konumundan sürer` : 'ya da bir paragrafa dokun, oradan başlasın'}</small>
        </span>
      </button>
      <button type="button" className="cd-basla-kapat" onClick={() => setGoster(false)} aria-label="Bu ipucunu gizle">×</button>
    </div>
  );
}

/* ---------------- PDF ---------------- */

function CdPdfBolme({ detay, canli }: { detay: CdDetay; canli: boolean }) {
  const pdf = detay.pdf!;
  const info = useDeckPdf(pdf.deckId);
  const aktif = useCd((s) => (canli ? s.aktif : -1));
  const cumle = useCd((s) => (canli ? s.cumle : -1));
  const { durdu, durdur, surdur } = useTakip();
  const [zoom, setZoom] = useState(1);
  const [elle, setElle] = useState<{ dosya: number; sayfa: number } | null>(null);
  const wrapRef = useRef<HTMLDivElement>(null);
  const [hataMsj, setHataMsj] = useState<string | null>(null);

  // Etkin paragrafın eşlemesi; eşlemesi olmayan paragrafta son bilinen sayfada kalınır
  const sonHedef = useRef<{ dosya: number; sayfa: number }>({ dosya: 0, sayfa: 1 });
  const es = aktif >= 0 ? pdf.paragraflar[aktif] : null;
  const isr = aktif >= 0 && cumle >= 0 ? detay.isaret?.[String(aktif)]?.[cumle] ?? null : null;
  // Okunan kelime: cümle içindeki ses ilerlemesine göre son geçilen eşleşmiş kelime (yalnız değişince yeniden çizilir)
  const kelime = useCd(() => {
    if (!isr || !isr.w.length) return -1;
    const o = cdCumleIlerleme();
    let k = 0;
    while (k + 1 < isr.w.length && isr.w[k + 1][0] <= o) k++;
    return k;
  });
  if (es && Number.isFinite(es.sayfa)) {
    let s = es.sayfa;
    let d = es.dosya || 0;
    if (Array.isArray(es.sayfalar) && cumle >= 0 && cumle < es.sayfalar.length) {
      const cs = es.sayfalar[cumle];
      if (typeof cs === 'number' && Number.isFinite(cs) && cs > 0) s = cs;
    }
    if (Array.isArray(es.dosyalar) && cumle >= 0 && cumle < es.dosyalar.length) {
      const cd = es.dosyalar[cumle];
      if (typeof cd === 'number' && Number.isFinite(cd) && cd >= 0) d = cd;
    }
    // Önceden hizalanmış işaret (pdf_isaret.py) komşu slaytı daha kesin bulduysa o sayfa kullanılır
    if (isr && isr.t !== 'sayfa') { s = isr.s; d = isr.d; }
    sonHedef.current = { dosya: d, sayfa: Math.max(1, s) };
  }
  if (aktif < 0 && !canli) {
    const ilk = pdf.paragraflar.find((x) => x && Number.isFinite(x.sayfa));
    if (ilk && sonHedef.current.sayfa === 1 && sonHedef.current.dosya === 0) sonHedef.current = { dosya: ilk.dosya || 0, sayfa: Math.max(1, ilk.sayfa) };
  }
  const hedef = sonHedef.current;
  // Takip sürerken hedef; durunca kullanıcının baktığı yer (sürdürünce yeniden hedefe kayar)
  const gor = durdu && elle ? elle : hedef;
  const marks = useMemo<PdfMarks | null>(() => {
    if (!canli || durdu || !isr || isr.t === 'sayfa' || isr.d !== gor.dosya) return null;
    const focus = isr.t === 'resim' ? isr.l[0] : kelime >= 0 ? isr.w[kelime].slice(1) : null;
    return { page: isr.s, kind: isr.t, lines: isr.l, focus };
  }, [canli, durdu, isr, kelime, gor.dosya]);

  useEffect(() => { if (!durdu) setElle(null); }, [durdu]);

  // Sözleşmedeki dosya → sunucu akış adresi (ad/Drive kimliğiyle eşle, olmazsa sıra)
  const dosya = pdf.dosyalar[gor.dosya] || pdf.dosyalar[0];
  const sf = info?.files.find((f) => (dosya?.fileId && f.fileId === dosya.fileId) || f.name === dosya?.name) || info?.files[gor.dosya];
  const src = sf?.url;

  useEffect(() => {
    const w = wrapRef.current;
    if (!w) return;
    const on = () => durdur();
    w.addEventListener('wheel', on, { passive: true });
    w.addEventListener('touchmove', on, { passive: true });
    w.addEventListener('pointerdown', on);
    return () => {
      w.removeEventListener('wheel', on);
      w.removeEventListener('touchmove', on);
      w.removeEventListener('pointerdown', on);
    };
  }, [durdur, src]);

  const onVisible = useCallback((p: number) => {
    if (durdu) setElle({ dosya: gor.dosya, sayfa: p });
  }, [durdu, gor.dosya]);

  return (
    <div className="cd-bolme cd-pdf-bolme">
      <div className="cd-pdf-bar">
        <FileText aria-hidden />
        <span className="cd-pdf-ad" title={dosya?.name}>{dosya?.name || 'Ders PDF\'i'}</span>
        <span className="cd-pdf-sayfa">s. {gor.sayfa}{dosya?.pages ? ` / ${dosya.pages}` : ''}</span>
        {pdf.dosyalar.length > 1 && (
          <span className="cd-pdf-dosya">{(gor.dosya || 0) + 1}/{pdf.dosyalar.length}</span>
        )}
        <span className="cd-grow" />
        <button type="button" className="cd-ib" onClick={() => setZoom((z) => Math.max(0.5, +(z - 0.25).toFixed(2)))} aria-label="Uzaklaştır"><Minus /></button>
        <span className="cd-pdf-zoom">{Math.round(zoom * 100)}%</span>
        <button type="button" className="cd-ib" onClick={() => setZoom((z) => Math.min(3, +(z + 0.25).toFixed(2)))} aria-label="Yakınlaştır"><Plus /></button>
      </div>
      <div className="cd-pdf-govde dpv-body" ref={wrapRef}>
        {!info ? (
          <div className="cd-bos" role="status"><span className="cd-spin" aria-hidden /> PDF aranıyor…</div>
        ) : src && !hataMsj ? (
          <Suspense fallback={<div className="cd-bos" role="status"><span className="cd-spin" aria-hidden /> Görüntüleyici yükleniyor…</div>}>
            <PdfDocView
              key={src}
              src={src}
              page={gor.sayfa}
              highlight={canli && !durdu && es ? [hedef.sayfa, hedef.sayfa] : undefined}
              highlightLabel="Şu an anlatılan"
              marks={marks}
              zoom={zoom}
              onZoom={setZoom}
              onVisiblePage={onVisible}
              onError={setHataMsj}
              fit="width"
            />
          </Suspense>
        ) : (
          <div className="cd-bos">
            <p>{hataMsj || 'Bu dersin PDF\'i uygulama içinde açılamıyor.'}</p>
            {dosya?.fileId && (
              <a className="cd-btn" href={driveViewUrl(dosya.fileId)} target="_blank" rel="noreferrer">Drive'da aç</a>
            )}
          </div>
        )}
      </div>
      {durdu && canli && (
        <button type="button" className="cd-donus" onClick={surdur}>
          <Crosshair aria-hidden /> Canlı konuma dön
        </button>
      )}
    </div>
  );
}
