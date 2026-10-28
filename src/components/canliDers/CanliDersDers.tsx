/**
 * Canlı ders ekranı (/canliders/<key>): üç görünüm — Metin, Metin + PDF (bölünmüş: masaüstünde yan yana, telefonda üst-alt),
 * yalnız PDF (seçim cihazda saklanır). Tam ekran: kabuk gizlenir, oynatıcı saklanır ama tek dokunuşla açılır.
 * Metin sesle akar (etkin paragraf + tahmini cümle vurgusu), görünüm etkin paragrafı ortada tutar; kullanıcı elle
 * kaydırınca/PDF'i gezince takip dokunma sonrası 5 sn durur ve "Canlı konuma dön" çıkar. Oynatıcı alt çubuktadır (CanliDersDock).
 */
import CanliDersKimlikHedef from './CanliDersKimlikHedef';
import { CanliDersBaslangic } from './CanliDersBaslangic';
import React, { Suspense, lazy, memo, useCallback, useMemo, useEffect, useLayoutEffect, useRef, useState } from 'react';
import { AlertTriangle, ArrowLeftRight, ArrowUpDown, BookOpen, Captions, MapPin, Download, ChevronDown, ChevronLeft, ChevronRight, ChevronUp, Check, Columns2, Copy, Crosshair, FileText, Maximize2, Minimize2, Minus, Package, Pause, Play, Palette, Plus, RotateCcw, Rows2, ScrollText, SkipBack, SkipForward } from 'lucide-react';
import { navigateTo, pathFor } from '../../router';
import { driveViewUrl, useDeckPdf } from '../../services/deckPdfService';
import { releasePageFullscreen, wasRecentlyScrollingOrTouching } from '../../utils/fullscreen';
import { lockScroll, unlockScroll } from '../../utils/scrollLock';
import { isIosBrowserTab, shouldAvoidNativeFullscreen } from '../../utils/device';
import { openPwaInstallGuide } from '../../services/pwaService';
import { cumleDuzeyleri } from '../../utils/maddele';
import {
  cdCumleAraligi, cdParagrafSinirlari, cdDetayBagla, cdKelimeBas, cdKonusulanKarakter, cdDetayGetir, cdDurum, cdMedspakUrl, cdOynat, cdParagrafa, cdSesUrl, cdTercihVaryant, cdToggle, cdBolumAtla, fmtSure, useCd, type CdDetay,
} from './canliDersStore';
import { useDersEkranTercih, useYatayDokunmatik } from '../../services/dersEkranTercih';
import { CdAiPanel, CdBolumSonu, CdMasa, CdSesliKitap, cdAiIste, cdBolumSonuDurAyarla, useCdBolumSonuDur, useMasaUygun } from './CdSesliEk';
import { toggleFavoriteCard } from '../../services/studyStore';
import { CdTasmaMenu, CdV15Bas, CdV15Gorunum, CdV15KalemDugme, CdV15KalemKutusu, CdV15Menu } from './CdV15'; // H332: CdTasmaMenu
import { GunlukDiyalog } from './CanliDersView';
import { CdCikmisChip, CdCikmisPencereKok, cikmisSayfada } from './CdCikmisChip';
import { useCdTur } from './useCdTur';
import { useUzunBasSecim } from './cdUzunBas';
import { cdTurGoruldu } from './canliDersTurDurum';
import { cdDersEtiketi } from './canliDersKategori';
import { ListeEkleDugme } from './CanliDersListem';
import { CevrimdisiDugme } from './CanliDersCevrimdisi';
import { CdDaha } from './CanliDersDaha';
import { cdMotivasyonAyarla, useCdMotivasyonAcik } from './canliDersMotivasyon';
import { CdTvKumanda } from './CanliDersTv';
import { MetniAktarDugme } from './CanliDersAktarDugme';
import { VideoOlusturDugme } from './CanliDersVideo';
import { Columns3, Headphones, Highlighter, SlidersHorizontal, Sparkles, Star } from 'lucide-react';
import { useKonuSayaci } from '../../services/calismaTakip';
import { KonuDugmeleri } from '../takip/KonuTakip';
import { toast } from '../ui/Toast';
import { useYildizliMi, useYildizliSayisi, yildizToggle } from '../../services/yildizliParagrafStore';
import { registerSelectionActions } from '../../utils/selectionShare';
import { YildizliParagraflarModal } from '../study/YildizliParagraflarModal';
import '../learn/pdf/pdfDoc.css';
import { SlideDrawingCanvas, getDrawingGlobalState, penPalette, setDrawingGlobalState, undoLastDrawing, useCanUndoDrawing, useDrawingGlobalState } from '../learn/SlideDrawingCanvas';
import { Popover, PopoverContent, PopoverTrigger, ToggleGroup, ToggleGroupItem } from '../ui/radix';
import { useAppearance } from '../../utils/appearance';
import { Eraser, MousePointer2, PenTool, Undo2 } from 'lucide-react';
import type { CdCikmisKonum, CdV2Cumle } from './canliDersStore';

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
import { CdParagrafTerimleri, CdTerimKatman, PdfAyarlarMenu, PdfGorunumDugme, TerimBaslikDugme, TerimDugme, cdTerimKatmani, usePdfGorunum } from './CdTerimKatman';

const TAKIP_ARA = 5000;

/** Kullanıcı ekrana dokununca/gezince takibi duraklatır; 5 sn etkileşim olmazsa metin ve PDF birlikte canlı konuma döner
 *  ("Canlı konuma dön" ile hemen de dönülür). Durum ortaktır: iki bölme aynı anda durur ve aynı anda sürer. */
let takipDurdu = false;
let takipZaman = 0;
const takipDinleyen = new Set<() => void>();
const takipYay = () => takipDinleyen.forEach((f) => f());
const takipDurdur = () => {
  window.clearTimeout(takipZaman);
  takipZaman = window.setTimeout(() => { takipDurdu = false; takipYay(); }, TAKIP_ARA);
  if (!takipDurdu) { takipDurdu = true; takipYay(); }
};
const takipSurdur = () => {
  window.clearTimeout(takipZaman);
  if (takipDurdu) { takipDurdu = false; takipYay(); }
};
const takipAbone = (f: () => void) => { takipDinleyen.add(f); return () => { takipDinleyen.delete(f); }; };
const takipOku = () => takipDurdu;

function useTakip() {
  const durdu = React.useSyncExternalStore(takipAbone, takipOku, takipOku);
  useEffect(() => () => { if (takipDinleyen.size === 0) takipSurdur(); }, []);
  return { durdu, durdur: takipDurdur, surdur: takipSurdur };
}

// yatay telefon (tasarım S15): alçak ve yatay ekranda da bölmeler yan yana
const GENIS_SORGU = '(min-width: 900px), (orientation: landscape) and (max-height: 520px)';
const genisMi = () => typeof window !== 'undefined' && window.matchMedia(GENIS_SORGU).matches;

type Gorunum = 'metin' | 'ikisi' | 'pdf' | 'altyazi';
const GORUNUM_KEY = 'medsoru_canli_ders_gorunum';
/** Kayıtlı görünüm; yoksa geniş ekranda bölünmüş, telefonda metin */
const ilkGorunum = (): Gorunum => {
  try {
    const v = localStorage.getItem(GORUNUM_KEY);
    if (v === 'metin' || v === 'ikisi' || v === 'pdf' || v === 'altyazi') return v;
  } catch { /* yok */ }
  // v15 (tasarım S19): telefonda da PDF üstte, metin altta
  return genisMi() || document.documentElement.dataset.v15 === 'on' ? 'ikisi' : 'metin';
};
const GORUNUMLER: { id: Gorunum; ad: string; ikon: React.ReactNode }[] = [
  { id: 'metin', ad: 'Metin', ikon: <ScrollText aria-hidden /> },
  { id: 'ikisi', ad: 'Metin + Slayt', ikon: <Columns2 aria-hidden /> },
  { id: 'pdf', ad: 'Slayt', ikon: <FileText aria-hidden /> },
  // tasarım S04: slayt tüm alanı alır, okunan cümle altta altyazı şeridinde
  { id: 'altyazi', ad: 'Slayt + altyazı', ikon: <Captions aria-hidden /> },
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
const ASAMA_KEY = 'medsoru_kamp_asama_v1';
function cdKayitliAsama(key: string): number | null {
  try { const v = JSON.parse(localStorage.getItem(ASAMA_KEY) || '{}')[key]; return Number.isFinite(v) ? v : null; } catch { return null; }
}
function cdAsamaKaydet(key: string, no: number) {
  try { const o = JSON.parse(localStorage.getItem(ASAMA_KEY) || '{}'); o[key] = no; localStorage.setItem(ASAMA_KEY, JSON.stringify(o)); } catch { /* yok */ }
}

function useVurguAcik(): [boolean, (v: boolean) => void] {
  const [v, setV] = useState(() => { try { return localStorage.getItem(VURGU_ANAHTAR) !== '0'; } catch { return true; } });
  return [v, (x: boolean) => { setV(x); try { localStorage.setItem(VURGU_ANAHTAR, x ? '1' : '0'); } catch { /* yok */ } }];
}

/** Modül içinde gömülü kullanım (TBG Sınav Kampı): geri bağlantısı yerine modülün gezinmesi, aşama aşama metin,
 *  yazı boyutu tam ekran dışında da. Bölüm başlıkları "N · Aşama adı" (aşama girişi) ve "N.M · Alt başlık" biçimindedir. */
export interface CdKamp { geri: React.ReactNode }

export default function CanliDersDers({ dersKey, kamp }: { dersKey: string; kamp?: CdKamp }) {
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
    return 60;   // izleme düzeni: slayt geniş, metin yanında (kullanıcı 2026-10-24: ekran kalabalık)
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
  /** Tam ekranda yüzen araçlar (yazı boyutu, PDF araç çubuğu) yalnız istenince açılır. */
  const [aracAcik, setAracAcik] = useState(false);
  // v15: üst bar + Görünüm çekmecesi + gruplu Ders seçenekleri (components/canliDers/CdV15.tsx)
  const { v15 } = useAppearance();
  const [gor15, setGor15] = useState(false);
  const [menu15, setMenu15] = useState(false);
  const [odak, setOdak] = useState(false);
  // S06 sesli kitap / S07 üç bölmeli masa: mevcut görünümlerin üstünde ek kip (cihazda saklanır)
  const [ozelKip, setOzelKipDurum] = useState<'kitap' | 'masa' | null>(() => { try { const v = localStorage.getItem('medsoru_cd_ozel_kip'); return v === 'kitap' || v === 'masa' ? v : null; } catch { return null; } });
  const setOzelKip = (k: 'kitap' | 'masa' | null) => { setOzelKipDurum(k); try { localStorage.setItem('medsoru_cd_ozel_kip', k || ''); } catch { /* yok */ } };
  const masaUygun = useMasaUygun();
  const [otoTam] = useDersEkranTercih('otoTam');
  const [yatayYan] = useDersEkranTercih('yatayYan');
  const yatayDokunmatik = useYatayDokunmatik();
  const bolumSonuDur = useCdBolumSonuDur();
  const [yazi, setYaziDurum] = useState<number>(() => { try { return Number(localStorage.getItem(YAZI_KEY)) || 20; } catch { return 20; } });
  const setYazi = (n: number | ((y: number) => number)) => setYaziDurum((y) => {
    const v = Math.min(YAZI_ENCOK, Math.max(YAZI_ENAZ, typeof n === 'function' ? n(y) : n));
    try { localStorage.setItem(YAZI_KEY, String(v)); } catch { /* yok */ }
    return v;
  });
  const [oynaticiAcik, setOynaticiAcik] = useState(true);
  // Açılış paneli: bu ders zaten çalmıyorsa ve paragraf bağlantısıyla gelinmediyse ders açılınca gösterilir
  // v15 (tasarım S19): açılış kartı yok, ders doğrudan PDF + metinle açılır; ses oynat düğmesiyle başlar
  const [acilis, setAcilis] = useState(() => !v15 && !kamp && !(cdDurum().key === dersKey && cdDurum().playing)
    && !new URLSearchParams(location.search).get('p') && !location.hash.startsWith('#p-'));
  useEffect(() => { if (buDersCaliyor) setAcilis(false); }, [buDersCaliyor]);
  const [yildizModalAcik, setYildizModalAcik] = useState(false);
  const [gunlukAcik, setGunlukAcik] = useState(false);
  const yildizSayisi = useYildizliSayisi();
  const rootRef = useRef<HTMLDivElement>(null);
  const govdeRef = useRef<HTMLDivElement>(null);
  const [yuk, setYuk] = useState<number | null>(null);
  const caliyorKey = useCd((s) => s.key);
  const caliyorBaslik = useCd((s) => s.baslik);
  const tanitim = useCdTur('ders', !!detay, () => !!document.querySelector('.cd-dock') && !!document.querySelector('.cd-metin p'));
  // H06: uzun basma turu — ders turu görüldükten sonra bir kez (metin bölmesi görünürken)
  const secimTur = useCdTur('secim', !!detay && !tanitim.tur && cdTurGoruldu('ders'), () => !!document.querySelector('.cd-metin .cd-p'));

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
    let pStr = sp.get('p') || (window.location.hash.startsWith('#p-') ? window.location.hash.replace('#p-', '') : null);
    // ?ara=<cümle> (spot "Derste dinle"): kelimeleri en çok örtüşen paragrafa git; zayıf eşleşmede kaydırma yok
    const ara = sp.get('ara');
    if (!pStr && ara) {
      const kel = (x: string) => x.toLocaleLowerCase('tr-TR').replace(/[^\p{L}\p{N}\s]/gu, ' ').split(/\s+/).filter((w) => w.length > 3).map((w) => w.slice(0, 5));
      const hedef = new Set(kel(ara));
      let en = -1, enP = 0;
      if (hedef.size) detay.bolumler.forEach((b) => b.paragraflar.forEach((p) => {
        const k = new Set(kel(p.metin));
        let n = 0; hedef.forEach((w) => { if (k.has(w)) n += 1; });
        const puan = n / hedef.size;
        if (puan > enP) { enP = puan; en = p.i; }
      }));
      if (en >= 0 && enP >= 0.45) pStr = String(en);
    }
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
        const bag = cdDetayBagla(d);
        setBaglanti(bag);
        // ?t=<sn> (arama "Sesli derste geçen yerler"): ders o saniyeye konur (oynatma kullanıcı hareketiyle başlar)
        const tSn = Number(new URLSearchParams(window.location.search).get('t'));
        if (bag !== 'baska' && Number.isFinite(tSn) && tSn > 0) cdOynat(d, undefined, { t: tSn, oynat: false });
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
    const mq = window.matchMedia(GENIS_SORGU);
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
  // O10 "Ders açılınca kendiliğinden tam ekran": Fullscreen API kullanıcı hareketi ister → ders açıldıktan sonraki ilk
  // dokunuş/tuşta bir kez açılır (sayfa yüklenir yüklenmez istek yapılmaz; reddedilirse yalnız uygulama içi tam ekran kalır)
  const otoTamYapildi = useRef(false);
  const tamAcRef = useRef(tamEkranAc);
  tamAcRef.current = tamEkranAc;
  useEffect(() => {
    if (!otoTam || !detay || kamp || otoTamYapildi.current) return;
    if (tamEkran) { otoTamYapildi.current = true; return; }
    const f = (e: Event) => {
      if (e instanceof KeyboardEvent && (e.key === 'Escape' || e.key === 'Tab' || e.ctrlKey || e.metaKey || e.altKey)) return;
      otoTamYapildi.current = true;
      kaldir();
      tamAcRef.current();
    };
    const kaldir = () => { window.removeEventListener('pointerup', f, true); window.removeEventListener('keydown', f, true); };
    window.addEventListener('pointerup', f, true);
    window.addEventListener('keydown', f, true);
    return kaldir;
  }, [otoTam, detay, kamp, tamEkran]);
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
        {kamp ? kamp.geri : <GeriBag />}
        <div className="cd-bos">
          <p>{kamp && /sesi henüz yok|bulunamadı/.test(hata)
            ? 'Sesli ders hazırlanıyor; birazdan burada olacak. Bu sırada diğer bölümleri kullanabilirsin.'
            // sunucunun iç hata kodu ("geçersiz ders", "bulunamadı") öğrenciye ham gösterilmez (H111p)
            : /geçersiz ders|bulunamadı|404|400/i.test(hata) ? 'Bu adreste bir sesli ders yok. Bağlantı eski ya da hatalı olabilir; listeden dersi seçebilirsin.' : hata}</p>
          {!kamp && <button type="button" className="cd-btn is-ana" onClick={() => navigateTo(pathFor('canli_ders'))}>Tüm sesli derslere dön</button>}
        </div>
      </div>
    );
  }
  if (!detay) {
    return (
      <div className="cd-root">
        {kamp ? kamp.geri : <GeriBag />}
        {v15 ? (
          // tasarım S13: slayt iskeleti + "Ders hazırlanıyor" + metin satırı iskeletleri
          <div className="cd-hazir" role="status" aria-label="Ders hazırlanıyor">
            <div className="cd-hazir-pdf" aria-hidden><i style={{ width: '50%' }} /><i /><i style={{ width: '80%' }} /><b /><i style={{ width: '70%' }} /></div>
            <div className="cd-hazir-bas"><span className="cd-spin" aria-hidden /><div><b>Ders hazırlanıyor</b><small>Metin, slayt eşleşmesi ve ses yükleniyor</small></div></div>
            <div className="cd-hazir-metin" aria-hidden><i style={{ width: '95%' }} /><i style={{ width: '88%' }} /><i style={{ width: '92%' }} /><i style={{ width: '60%' }} /></div>
          </div>
        ) : <div className="cd-bos" role="status"><span className="cd-spin" aria-hidden /> Ders yükleniyor…</div>}
      </div>
    );
  }

  const pdfVar = !!detay.pdf && detay.pdf.dosyalar.length > 0;
  // O10 "Yatayda yan yana": yatay telefon/tablette PDF + metin yan yana
  const yatayYanEtkin = yatayYan && yatayDokunmatik && pdfVar && !kamp;
  const mod: Gorunum = pdfVar ? (yatayYanEtkin ? 'ikisi' : gorunum) : 'metin';
  const metinGoster = mod === 'metin' || mod === 'ikisi';
  const pdfGoster = mod !== 'metin';
  const aktifYon: 'yan-yana' | 'ust-alt' = yatayYanEtkin ? 'yan-yana' : bolmeYon === 'oto' ? (genis ? 'yan-yana' : 'ust-alt') : bolmeYon;
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
    ? <CdMetinBolme key="metin" detay={detay} canli={buDers} kamp={!!kamp} />
    : <CdPdfBolme key="pdf" detay={detay} canli={buDers} />;
  const ikinciBolme = bolmeTers
    ? <CdPdfBolme key="pdf" detay={detay} canli={buDers} />
    : <CdMetinBolme key="metin" detay={detay} canli={buDers} kamp={!!kamp} />;

  return (
    <div
      className={`cd-root cd-ders is-${mod}${tamEkran ? ' is-tam' : ''}${tamEkran && aracAcik ? ' is-arac-acik' : ''}${vurguAcik ? '' : ' cd-vurgu-kapali'}${kamp ? ' cd-kamp' : ''}`}
      ref={rootRef}
      style={tamEkran ? ({ '--cd-tam-yazi': `${yazi}px` } as React.CSSProperties) : yuk ? ({ height: yuk, ...(kamp || v15 ? { '--cd-tam-yazi': `${yazi}px` } : {}) } as React.CSSProperties) : undefined}
    >
      {v15 && !tamEkran ? (
        <CdV15Bas
          geri={kamp ? kamp.geri : (
            // v15: geri, dersin ayrıntı sayfasına (içerikler + bölümler) döner
            <a className="cd-geri" href={pathFor('ders_detay', detay.key)} aria-label="Ders ayrıntısına dön"
              onClick={(e) => { if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return; e.preventDefault(); if ((window as unknown as { __icGezinti?: boolean }).__icGezinti && history.length > 1) history.back(); else navigateTo(pathFor('ders_detay', detay.key)); }}>
              <ChevronLeft aria-hidden />
            </a>
          )}
          ust={<>{cdDersEtiketi(detay)}<DersBolumEtiketi detay={detay} /></>}
          baslik={detay.baslik}
          title={`${cdDersEtiketi(detay)} · ${detay.baslik}`}
          pdfVar={pdfVar}
          terimVar={!!(detay.terim || detay.kisaltma)}
          mod={mod}
          setGorunum={setGorunum}
          onGorunum={() => setGor15(true)}
          onMenu={() => setMenu15(true)}
          onTamEkran={tamEkranAc}
          hizli={{
            yildiz: yildizSayisi, onYildiz: () => setYildizModalAcik(true),
            onOgren: detay.desteId ? () => navigateTo(`/dersler/interaktif/${detay.desteId}`) : undefined,
            vurguVar: !!detay.vurgu, vurgu: vurguAcik, setVurgu: setVurguAcik,
            yazi, setYazi, yaziEnaz: YAZI_ENAZ, yaziEncok: YAZI_ENCOK,
          }}
          ek={kamp && metinGoster ? <YaziAyar yazi={yazi} setYazi={setYazi} /> : null}
        />
      ) : (
      <header className="cd-ders-bas">
        {kamp ? kamp.geri : <GeriBag arsiv={Boolean(detay.arsiv || detay.donem === '2025-2026' || detay.key.startsWith('y25-'))} />}
        <div className="cd-ders-baslik">
          <small className="cd-ders-ust">
            {(detay.arsiv || detay.donem === '2025-2026' || detay.key.startsWith('y25-')) && (
              <span className="cd-chip is-arsiv">2025-2026 Arşiv</span>
            )}
            {detay.sinama && <span className="cd-chip is-arsiv is-sinama">SINAMA</span>}
            {cdDersEtiketi(detay)}
            <DersBolumEtiketi detay={detay} />
          </small>
          <h1 className="cd-ders-ad" title={`${cdDersEtiketi(detay)} · ${detay.baslik}`}>{detay.baslik}</h1>
        </div>
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
        </div>
        <div className="cd-ders-uc">
          {pdfVar && (() => {
            // telefonda görünüm seçici ayrı satır kaplamasın: tek düğme sırayla Metin → Metin + Slayt → Slayt
            const i = GORUNUMLER.findIndex((g) => g.id === mod);
            const sonraki = GORUNUMLER[(i + 1) % GORUNUMLER.length];
            return (
              <button type="button" className="cd-btn cd-gorunum-dongu" onClick={() => setGorunum(sonraki.id)}
                      title={`Görünüm: ${GORUNUMLER[i]?.ad} (dokun: ${sonraki.ad})`} aria-label={`Görünüm: ${GORUNUMLER[i]?.ad}. ${sonraki.ad} görünümüne geç`}>
                {GORUNUMLER[i]?.ikon}
              </button>
            );
          })()}
          {!tamEkran && (
            <button
              type="button"
              className="cd-btn is-ince"
              onClick={() => setGunlukAcik(true)}
              title="Sesli ders güncelleme günlüğü"
            >
              <FileText aria-hidden /> <span>Günlük</span>
            </button>
          )}
          {!tamEkran && detay.desteId && (
            <button
              type="button"
              className="cd-btn is-ince"
              onClick={() => navigateTo(`/dersler/interaktif/${detay.desteId}`)}
              title="Etkileşimli Öğren destesini aç"
            >
              <BookOpen aria-hidden /> <span>Öğren</span>
            </button>
          )}
          {!tamEkran && detay.medspakVar && (
            <a
              className="cd-btn is-ince"
              href={cdMedspakUrl(detay.key)}
              download={`${detay.key}.medspak`}
              title=".medspak ders paketini indir (PDF + ses + deste + günlük)"
            >
              <Package aria-hidden /> <span>.medspak</span>
            </a>
          )}
          {!tamEkran && (
            <KonuDugmeleri kucuk className="cd-ders-takip" modul="sesli" konu={detay.key} ad={detay.baslik}
              onTekrar={() => { const v = cdTercihVaryant(detay.varyantlar); if (v) cdOynat(detay, v.id, { t: 0 }); }} />
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
              {detay.pdf && <VideoOlusturDugme detay={detay} />}
              <MotivasyonDugme />
              {detay.vurgu && (
                <button type="button" className={`cd-btn${vurguAcik ? ' is-on' : ''}`} aria-pressed={vurguAcik} onClick={() => setVurguAcik(!vurguAcik)}
                  title="Çıkmışta, örnek sorularda ve spotlarda geçen cümleleri kırmızı ve işaretli göster">
                  <Highlighter aria-hidden /> <span>Önemli yerleri vurgula</span>
                </button>
              )}
              {tanitim.dugme}
              {pdfVar && <PdfAyarlarMenu terimVar={!!(detay.terim || detay.kisaltma)} />}
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
            </CdDaha>
          )}
          {kamp && !tamEkran && metinGoster && (
            <YaziAyar yazi={yazi} setYazi={setYazi} />
          )}
          {(detay.terim || detay.kisaltma) && <TerimBaslikDugme />}
          {tamEkran ? (
            <>
              <button
                type="button"
                className={`cd-btn is-ikon cd-tam-arac${aracAcik ? ' is-on' : ''}`}
                onClick={() => setAracAcik((x) => !x)}
                aria-pressed={aracAcik}
                aria-label={aracAcik ? 'Araçları gizle' : 'Araçları göster'}
                title={aracAcik ? 'Araçları gizle' : 'Araçlar (yazı boyutu, çizim, yakınlaştırma)'}
              >
                <SlidersHorizontal aria-hidden />
              </button>
              {metinGoster && aracAcik && (
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
      )}
      {v15 && (
        <>
          <CdV15Gorunum
            acik={gor15}
            onKapat={() => setGor15(false)}
            pdfVar={pdfVar}
            terimVar={!!(detay.terim || detay.kisaltma)}
            mod={mod}
            setGorunum={setGorunum}
            yon={bolmeYon}
            setYon={setBolmeYon}
            oran={pdfOran}
            setOran={setPdfOranHedef}
            ters={bolmeTers}
            setTers={setBolmeTers}
            onTamEkran={tamEkranAc}
            vurguVar={!!detay.vurgu}
            vurgu={vurguAcik}
            setVurgu={setVurguAcik}
            yazi={yazi}
            setYazi={setYazi}
            yaziEnaz={YAZI_ENAZ}
            yaziEncok={YAZI_ENCOK}
          />
          <CdV15Menu
            acik={menu15}
            onKapat={() => setMenu15(false)}
            gruplar={[
              {
                ad: 'Çalışma',
                ogeler: (
                  <>
                    <KonuDugmeleri kucuk className="cd-ders-takip" modul="sesli" konu={detay.key} ad={detay.baslik}
                      onTekrar={() => { const v = cdTercihVaryant(detay.varyantlar); if (v) cdOynat(detay, v.id, { t: 0 }); }} />
                    <button type="button" className={`cd-btn${ozelKip === 'kitap' ? ' is-on' : ''}`} onClick={() => { setMenu15(false); setOzelKip(ozelKip === 'kitap' ? null : 'kitap'); }}>
                      <Headphones aria-hidden /> <span>{ozelKip === 'kitap' ? 'Sesli kitaptan çık' : 'Sesli kitap kipi'}</span>
                    </button>
                    {masaUygun && (
                      <button type="button" className={`cd-btn${ozelKip === 'masa' ? ' is-on' : ''}`} onClick={() => { setMenu15(false); setOzelKip(ozelKip === 'masa' ? null : 'masa'); }}>
                        <Columns3 aria-hidden /> <span>{ozelKip === 'masa' ? 'Üç bölmeli masadan çık' : 'Üç bölmeli masa'}</span>
                      </button>
                    )}
                    <button type="button" className={`cd-btn${bolumSonuDur ? ' is-on' : ''}`} aria-pressed={bolumSonuDur} onClick={() => cdBolumSonuDurAyarla(!bolumSonuDur)}>
                      <Pause aria-hidden /> <span>Bölüm sonlarında dur: {bolumSonuDur ? 'Açık' : 'Kapalı'}</span>
                    </button>
                    <button type="button" className="cd-btn" onClick={() => { setMenu15(false); setYildizModalAcik(true); }}>
                      <Star aria-hidden /> <span>Yıldızlı paragraflar ({yildizSayisi})</span>
                    </button>
                    <ListeEkleDugme dersKey={detay.key} baslik={detay.baslik} etiketli />
                    {detay.vurgu && (
                      <button type="button" className={`cd-btn${vurguAcik ? ' is-on' : ''}`} aria-pressed={vurguAcik} onClick={() => setVurguAcik(!vurguAcik)}
                        title="Çıkmışta, örnek sorularda ve spotlarda geçen cümleleri kırmızı ve işaretli göster">
                        <Highlighter aria-hidden /> <span>Önemli yerleri vurgula</span>
                      </button>
                    )}
                    {detay.desteId && (
                      <button type="button" className="cd-btn" onClick={() => { setMenu15(false); navigateTo(`/dersler/interaktif/${detay.desteId}`); }}>
                        <BookOpen aria-hidden /> <span>Öğren destesine geç</span>
                      </button>
                    )}
                  </>
                ),
              },
              {
                ad: 'Kaydet ve paylaş',
                ogeler: (
                  <>
                    <CevrimdisiDugme dersKey={detay.key} baslik={detay.baslik} varyantlar={detay.varyantlar} />
                    {(() => {
                      const v = cdTercihVaryant(detay.varyantlar);
                      return v ? (
                        <a className="cd-btn" href={cdSesUrl(detay.key, v.id, true)} download>
                          <Download aria-hidden /> <span>MP3 indir</span>
                        </a>
                      ) : null;
                    })()}
                    <MetniAktarDugme detay={detay} vurguAcik={vurguAcik} />
                    {detay.pdf && <VideoOlusturDugme detay={detay} />}
                    {detay.medspakVar && (
                      <a className="cd-btn" href={cdMedspakUrl(detay.key)} download={`${detay.key}.medspak`} title="PDF + ses + deste + günlük tek pakette">
                        <Package aria-hidden /> <span>.medspak ders paketi</span>
                      </a>
                    )}
                  </>
                ),
              },
              {
                ad: 'Diğer',
                ogeler: (
                  <>
                    <button type="button" className="cd-btn" onClick={() => { setMenu15(false); setOdak(true); }}>
                      <ScrollText aria-hidden /> <span>Odak modu</span>
                    </button>
                    <button type="button" className="cd-btn" onClick={() => { setMenu15(false); setGunlukAcik(true); }}>
                      <FileText aria-hidden /> <span>Ders günlüğü</span>
                    </button>
                    {tanitim.dugme}
                    <MotivasyonDugme />
                  </>
                ),
              },
            ]}
          />
        </>
      )}
      {detay.sinama && !tamEkran && (
        <div className="cd-arsiv-uyari is-kompakt is-sinama" role="note">
          <AlertTriangle aria-hidden />
          <span>
            <b>{detay.sinamaEtiket || 'SINAMA — test verisi'}:</b> Bu ders sınama amacıyla eklenmiş test verisidir; <b>güncel dönem derslerinin listesinde görünmez.</b>
          </span>
        </div>
      )}
      {(detay.arsiv || detay.donem === '2025-2026' || detay.key.startsWith('y25-')) && !tamEkran && (
        <div className="cd-arsiv-uyari is-kompakt" role="note">
          <AlertTriangle aria-hidden />
          <span>
            <b>2025-2026 Dönemi Arşiv Dersi:</b> Bu içerik geçen yılın (2025-2026) slaytlarından hazırlanmıştır; <b>2026-2027 güncel dönem dersleriyle karışmaz.</b>
          </span>
        </div>
      )}
      {baglanti === 'baska' && !buDers && (
        <div className="cd-uyari">
          <span>Şu an çalan: <b>{caliyorBaslik}</b></span>
          <button type="button" className="cd-btn is-ana" onClick={() => { cdOynat(detay); setBaglanti('bagli'); }}>
            <Play aria-hidden /> Bu dersi dinle
          </button>
        </div>
      )}
      {acilis && (
        <CanliDersBaslangic detay={detay} gorunum={mod} pdfVar={pdfVar}
          setGorunum={(g) => setGorunum(g)} onKapat={() => { setAcilis(false); setBaglanti(cdDetayBagla(detay)); }} />
      )}
      {!acilis && ozelKip === 'kitap' && (
        <CdSesliKitap detay={detay} onMetin={() => setOzelKip(null)} onBasla={() => { cdOynat(detay); setBaglanti('bagli'); }} />
      )}
      {!acilis && ozelKip === 'masa' && masaUygun && (
        <CdMasa detay={detay} onParagraf={kaydirParagrafa}
          orta={pdfVar ? <CdPdfBolme detay={detay} canli={buDers} /> : <CdAltyazi detay={detay} canli={buDers} />}
          sag={<CdMetinBolme detay={detay} canli={buDers} kamp={!!kamp} />} />
      )}
      <CdBolumSonu detay={detay} />
      <CdAiPanel />
      <div
        ref={govdeRef}
        hidden={acilis || ozelKip === 'kitap' || (ozelKip === 'masa' && masaUygun)}
        className={`cd-govde${mod === 'altyazi' ? ' is-altyazi' : ''}${mod === 'ikisi' ? (aktifYon === 'yan-yana' ? ' is-iki' : ' is-ust-alt') : ''}`}
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
            {metinGoster && <CdMetinBolme detay={detay} canli={buDers} kamp={!!kamp} />}
            {mod === 'altyazi' && <CdAltyazi detay={detay} canli={buDers} />}
          </>
        )}
      </div>
      {tanitim.tur}
      {secimTur.tur}
      {odak && <CdOdakModu onKapat={() => setOdak(false)} />}
      <CanliDersKimlikHedef detay={detay} kok={rootRef} />
      {gunlukAcik && <GunlukDiyalog dersKey={detay.key} onKapat={() => setGunlukAcik(false)} />}
      {yildizModalAcik && (
        <YildizliParagraflarModal
          dersKey={dersKey}
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
        <button type="button" onClick={() => onOran(35)} className={Math.abs(oran - 35) <= 4 ? 'is-on' : ''} title={`${birinciAd} %35 · ${ikinciAd} %65`} aria-label={`${birinciAd} yüzde 35`}>35</button>
        <button type="button" onClick={() => onOran(50)} className={Math.abs(oran - 50) <= 4 ? 'is-on' : ''} title="Eşitle (%50 / %50)" aria-label="Bölmeyi eşitle">50</button>{/* H207: sayı düğmeleri ekran okuyucuda yalnız "35" diye okunuyordu */}
        <button type="button" onClick={() => onOran(65)} className={Math.abs(oran - 65) <= 4 ? 'is-on' : ''} title={`${birinciAd} %65 · ${ikinciAd} %35`} aria-label={`${birinciAd} yüzde 65`}>65</button>
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

/** Yazı boyutu (kamp kipinde tam ekran dışında da görünür) */
function YaziAyar({ yazi, setYazi }: { yazi: number; setYazi: (n: number) => void }) {
  return (
    <span className="cd-yazi" role="group" aria-label="Yazı boyutu">
      <button type="button" className="cd-btn is-ikon" onClick={() => setYazi(yazi - 2)} disabled={yazi <= YAZI_ENAZ} aria-label="Yazıyı küçült" title="Yazıyı küçült">
        <span aria-hidden className="cd-yazi-a is-kucuk">A</span>
      </button>
      <button type="button" className="cd-yazi-n" onClick={() => setYazi(20)} title="Varsayılan boyut" aria-label={`Yazı boyutu ${yazi} piksel, varsayılana dön`}>{yazi}</button>
      <button type="button" className="cd-btn is-ikon" onClick={() => setYazi(yazi + 2)} disabled={yazi >= YAZI_ENCOK} aria-label="Yazıyı büyüt" title="Yazıyı büyüt">
        <span aria-hidden className="cd-yazi-a">A</span>
      </button>
    </span>
  );
}

/* ---------------- kamp: aşamalar ---------------- */

/** Bölüm başlığı "N · Ad" aşama girişi, "N.M · Ad" alt başlıktır. */
export function kampBaslik(b: string): { asama: number; alt: number | null; ad: string } | null {
  const m = /^(\d+)(?:\.(\d+))?\s*·\s*(.+)$/.exec(b || '');
  return m ? { asama: +m[1], alt: m[2] ? +m[2] : null, ad: m[3].trim() } : null;
}
interface KampAsama { no: number; ad: string; bolumler: number[]; ilkP: number; sonP: number }
export function kampAsamalari(d: CdDetay): KampAsama[] {
  const out: KampAsama[] = [];
  d.bolumler.forEach((b, bi) => {
    const k = kampBaslik(b.baslik);
    if (!k || !b.paragraflar.length) return;
    let a = out.find((x) => x.no === k.asama);
    if (!a) { a = { no: k.asama, ad: k.alt === null ? k.ad : `Aşama ${k.asama}`, bolumler: [], ilkP: b.paragraflar[0].i, sonP: b.paragraflar[0].i }; out.push(a); }
    if (k.alt === null) a.ad = k.ad;
    a.bolumler.push(bi);
    a.ilkP = Math.min(a.ilkP, b.paragraflar[0].i);
    a.sonP = Math.max(a.sonP, b.paragraflar[b.paragraflar.length - 1].i);
  });
  return out;
}

function GeriBag({ arsiv = false }: { arsiv?: boolean }) {
  const hedef = arsiv ? `${pathFor('canli_ders')}?donem=2025-2026` : pathFor('canli_ders');
  return (
    <a
      className="cd-geri"
      href={hedef}
      onClick={(e) => {
        if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
        e.preventDefault();
        navigateTo(hedef);
      }}
    >
      <ChevronLeft aria-hidden /> <span>{arsiv ? '2025-2026 Arşivi' : 'Sesli dersler'}</span>
    </a>
  );
}

/* ---------------- metin ---------------- */

const hlDestek = () => typeof CSS !== 'undefined' && 'highlights' in CSS && typeof (window as any).Highlight === 'function';
/**
 * Odak modu (tasarım S05): yalnız akan metin; üst bar, slayt, oynatıcı ve yüzen öğeler gizlenir. Ortada altta üç düğme
 * (önceki bölüm · oynat/duraklat · sonraki bölüm); ekrana dokununca denetimler görünür, 3 sn sonra kendiliğinden kaybolur.
 */
function CdOdakModu({ onKapat }: { onKapat: () => void }) {
  const playing = useCd((s) => s.playing);
  const [goster, setGoster] = useState(true);
  const zaman = useRef(0);
  const uyandir = useCallback(() => {
    setGoster(true);
    window.clearTimeout(zaman.current);
    zaman.current = window.setTimeout(() => setGoster(false), 3000);
  }, []);
  useEffect(() => {
    document.documentElement.setAttribute('data-cd-odak', 'on');
    uyandir();
    const tik = (e: PointerEvent) => { if (!(e.target as HTMLElement).closest('.cd-odak-d')) uyandir(); };
    const tus = (e: KeyboardEvent) => { if (e.key === 'Escape') onKapat(); else uyandir(); };
    document.addEventListener('pointerdown', tik); document.addEventListener('keydown', tus);
    return () => { document.documentElement.removeAttribute('data-cd-odak'); document.removeEventListener('pointerdown', tik); document.removeEventListener('keydown', tus); window.clearTimeout(zaman.current); };
  }, [onKapat, uyandir]);
  return (
    <div className={`cd-odak-d${goster ? ' is-gor' : ''}`} role="toolbar" aria-label="Odak modu denetimleri">
      <div className="cd-odak-dug">
        <button type="button" onClick={() => { cdBolumAtla(-1); uyandir(); }} aria-label="Önceki bölüm"><SkipBack aria-hidden /></button>
        <button type="button" className="is-pl" onClick={() => { cdToggle(); uyandir(); }} aria-label={playing ? 'Duraklat' : 'Oynat'}>{playing ? <Pause aria-hidden /> : <Play aria-hidden />}</button>
        <button type="button" onClick={() => { cdBolumAtla(1); uyandir(); }} aria-label="Sonraki bölüm"><SkipForward aria-hidden /></button>
      </div>
      <small>Odak modu · ekrana dokun: denetimler · <button type="button" onClick={onKapat}>Çık</button></small>
    </div>
  );
}

/** Altyazı şeridi (tasarım S04): önceki cümle soluk, okunan cümle vurgulu; slayt kipinde PDF'in altında */
function CdAltyazi({ detay, canli }: { detay: CdDetay; canli: boolean }) {
  const aktif = useCd((s) => (canli ? s.aktif : -1));
  const cumle = useCd((s) => (canli ? s.cumle : -1));
  const par = React.useMemo(() => { for (const b of detay.bolumler) for (const p of b.paragraflar) if (p.i === aktif) return p; return null; }, [detay, aktif]);
  if (!par) return <div className="cd-altyazi is-bos" aria-hidden>Oynatınca okunan cümle burada görünür.</div>;
  const r = cumle >= 0 ? cdCumleAraligi(aktif, cumle) : null;
  const onceki = cumle > 0 ? cdCumleAraligi(aktif, cumle - 1) : null;
  const simdi = r ? par.metin.slice(r[0], r[1]).trim() : par.metin.split(/(?<=[.!?])\s+/)[0];
  const once = onceki ? par.metin.slice(onceki[0], onceki[1]).trim() : '';
  return (
    <div className="cd-altyazi" aria-live="polite">
      {once && <span className="cd-altyazi-once">{once.length > 90 ? `…${once.slice(-90).replace(/^\S*\s/, '')}` : once}</span>}{' '}
      <span className="cd-altyazi-simdi">{simdi}</span>
    </div>
  );
}

const HL_AD = 'cd-cumle';
const HL_KELIME = 'cd-kelime';

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

/** Önemli cümleler (çıkmış/spot/örnek soruyla eşleşen) marker + kırmızı kalın; anahtar terimler ayrıca kalın.
 *  [a, b) aralığına kırpılır (madde görünümünde her cümle ayrı satırdır). */
function vurguParcasi(metin: string, v: Vurgu | undefined, a: number, b: number): React.ReactNode[] {
  if (!v?.length) return [metin.slice(a, b)];
  const out: React.ReactNode[] = [];
  let k = a;
  for (const [s0, e0, tur, onem] of v) {
    if (tur !== 'c') continue;
    const s = Math.max(s0, a), e = Math.min(e0, b);
    if (e <= s || s < k) continue;
    if (s > k) out.push(metin.slice(k, s));
    const ic: React.ReactNode[] = [];
    let j = s;
    for (const [ts0, te0, tt] of v) {
      if (tt !== 't') continue;
      const ts = Math.max(ts0, s), te = Math.min(te0, e);
      if (te <= ts || ts < j) continue;
      if (ts > j) ic.push(metin.slice(j, ts));
      ic.push(<b key={ts} className="cd-terim">{metin.slice(ts, te)}</b>);
      j = te;
    }
    if (j < e) ic.push(metin.slice(j, e));
    out.push(<span key={s} className={`cd-onem o${onem}`} data-s={s0} data-e={e0} title={ONEM_AD[onem]}>{ic}</span>);
    k = e;
  }
  if (k < b) out.push(metin.slice(k, b));
  return out;
}

/** Paragrafı ses cümleleriyle aynı sınırlardan maddeler: ilk cümle giriş, kalanlar madde. Metin (ve karakter
 *  konumları) aynen korunur; madde imi yalnız CSS ::before olduğundan ses/cümle vurgusu etkilenmez. */
function VurguluMetin({ metin, v, i }: { metin: string; v?: Vurgu; i: number }) {
  const sin = cdParagrafSinirlari(i, metin);
  if (sin.length < 3) return <>{vurguParcasi(metin, v, 0, metin.length)}</>;
  const duz = cumleDuzeyleri(sin.map((e, c) => metin.slice(c ? sin[c - 1] : 0, e).trim()));
  return (
    <>
      {sin.map((e, c) => {
        const a = c ? sin[c - 1] : 0;
        const k = duz[c] === 0 ? 'cd-giris' : duz[c] === 2 ? 'cd-madde is-alt' : 'cd-madde';
        return <span key={a} className={k}>{vurguParcasi(metin, v, a, e)}</span>;
      })}
    </>
  );
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

const V2_TUR: Record<string, string> = { terim: 'Terim', sayi: 'Sayı', tuzak: 'Tuzak', cikmis: 'Çıkmış', tanim: 'Tanım' };

/** Ekran maddesi: **kalın** işaretleri + vurgu türleri (terim/sayı/tuzak/çıkmış/tanım) renkli parçalar olarak */
function v2Parcalar(ekran: string, vurgu: [string, string][]) {
  let duz = '';
  const kalin: [number, number][] = [];
  ekran.split('**').forEach((t, k) => { if (k % 2) kalin.push([duz.length, duz.length + t.length]); duz += t; });
  const tur = new Array<string | null>(duz.length).fill(null);
  const kucuk = duz.toLocaleLowerCase('tr');
  for (const [m, t] of vurgu) {
    const at = kucuk.indexOf(m.toLocaleLowerCase('tr'));
    if (at >= 0) for (let j = at; j < at + m.length; j++) tur[j] ??= t;
  }
  const out: { t: string; k: boolean; tur: string | null }[] = [];
  for (let j = 0; j < duz.length; j++) {
    const k = kalin.some(([a, b]) => j >= a && j < b);
    const son = out[out.length - 1];
    if (son && son.k === k && son.tur === tur[j]) son.t += duz[j];
    else out.push({ t: duz[j], k, tur: tur[j] });
  }
  return out;
}

/** Kurul 2+ (sesli metin v2): paragrafın ekran maddeleri; okunan cümlenin maddesi CdV2Su ile işaretlenir */
const CdV2Maddeler = memo(function CdV2Maddeler({ i, cs, deste }: { i: number; cs: CdV2Cumle[]; deste: string }) {
  return (
    <ul className="cd-v2" aria-label="Ekran maddeleri">
      {cs.map((c, ci) => c.e && (
        <li key={ci} data-i={i} data-c={ci} className="cd-v2-m" style={{ ['--d' as string]: Math.min(3, c.d) }}>
          <span className="cd-v2-e">
            {v2Parcalar(c.e, c.v).map((x, k) => {
              const ic = x.k ? <b>{x.t}</b> : x.t;
              return x.tur ? <mark key={k} className={`cd-v2-v is-${x.tur}`} title={V2_TUR[x.tur] || x.tur}>{ic}</mark> : <React.Fragment key={k}>{ic}</React.Fragment>;
            })}
          </span>
          {(c.c.length > 0 || c.a != null) && (
            <span className="cd-v2-rozetler">
              {c.c.length > 0 && <span className="cd-v2-cik" title={`Çıkmışta sorulmuş: ${c.c.join(', ')}`}><Star aria-hidden /> Çıkmış{c.c.length > 1 ? ` ×${c.c.length}` : ''}</span>}
              {c.a != null && (
                <a className="cd-v2-adim" href={`/ogren/${encodeURIComponent(deste)}?adim=${c.a}`}
                  onClick={(e) => { e.preventDefault(); navigateTo(`/ogren/${encodeURIComponent(deste)}?adim=${c.a}`); }}
                  title="Etkileşimli derste bu slayt adımını aç">Slayt {c.a}</a>
              )}
            </span>
          )}
        </li>
      ))}
    </ul>
  );
});

/** Okunan cümlenin ekran maddesini işaretler (DOM sınıfı; ders metni yeniden çizilmez) */
function CdV2Su({ pane, aktif, cumle }: { pane: React.RefObject<HTMLDivElement | null>; aktif: number; cumle: number }) {
  useEffect(() => {
    const el = aktif >= 0 && cumle >= 0 ? pane.current?.querySelector<HTMLElement>(`.cd-v2-m[data-i="${aktif}"][data-c="${cumle}"]`) : null;
    el?.classList.add('is-su');
    return () => el?.classList.remove('is-su');
  }, [pane, aktif, cumle]);
  return null;
}

/** Paragraf listesi bir kez çizilir; vurgu DOM üzerinden değişir (uzun metinde yeniden çizim yok). */
const MetinListe = memo(function MetinListe({ detay, onTik, kamp = false }: { detay: CdDetay; onTik: (i: number) => void; kamp?: boolean }) {
  return (
    <>
      {detay.bolumler.map((b, bi) => {
        const k = kamp ? kampBaslik(b.baslik) : null;
        return (
        <section key={bi} className={`cd-bolum${k ? (k.alt === null ? ' cd-k-giris' : ' cd-k-alt') : ''}`} data-asama={k?.asama} aria-label={k ? k.ad : b.baslik || `Bölüm ${bi + 1}`}>
          {k ? (
            k.alt === null
              ? <h2 className="cd-bolum-ad cd-k-asama"><span className="cd-k-no">Aşama {k.asama}</span>{k.ad}</h2>
              : <h3 className="cd-bolum-ad cd-k-baslik"><span className="cd-k-no">{k.asama}.{k.alt}</span>{k.ad}</h3>
          ) : b.baslik && <h2 className="cd-bolum-ad">{b.baslik}</h2>}
          {b.paragraflar.map((p) => (
            <div key={p.i} className="cd-p-sar">
              <p data-i={p.i} className="cd-p" onClick={() => onTik(p.i)}><VurguluMetin metin={p.metin} v={detay.vurgu?.[p.i]} i={p.i} /></p>
              {detay.v2?.p[p.i] && <CdV2Maddeler i={p.i} cs={detay.v2.p[p.i]} deste={detay.v2.deste} />}
              {(detay.terim || detay.kisaltma) && <CdParagrafTerimleri detay={detay} i={p.i} metin={p.metin} />}
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
        );
      })}
    </>
  );
});

/** Aşama çubuğu: hangi aşamadasın, hangileri bitti; dokununca o aşamaya geçilir (çalıyorsa ses de oraya atlar). */
function KampAsamaCubugu({ asamalar, gor, sesAsama, onSec }: { asamalar: KampAsama[]; gor: number; sesAsama: number; onSec: (no: number) => void }) {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    ref.current?.querySelector<HTMLElement>('.is-on')?.scrollIntoView({ block: 'nearest', inline: 'center', behavior: 'smooth' });
  }, [gor]);
  return (
    <nav className="cd-k-cubuk" aria-label="Aşamalar" ref={ref}>
      {asamalar.map((a) => {
        const durum = a.no === gor ? ' is-on' : sesAsama >= 0 && a.no < sesAsama ? ' is-bitti' : '';
        return (
          <button key={a.no} type="button" className={`cd-k-cip${durum}${a.no === sesAsama ? ' is-ses' : ''}`} onClick={() => onSec(a.no)}
            aria-current={a.no === gor ? 'step' : undefined} title={a.ad}>
            <span className="cd-k-cip-no">{a.no === 0 ? '★' : a.no}</span>
            <span className="cd-k-cip-ad">{a.ad}</span>
          </button>
        );
      })}
    </nav>
  );
}

/** Kelime kelime: sesin o an okuduğu kelime metinde işaretlenir. Ayrı ve görünmez bileşen: kelime değişince
 *  yalnız bu çalışır, ders metni yeniden çizilmez. Yalnız Highlight API ile (DOM'a dokunmaz). */
function CdKelimeIsaret({ pane, aktif, acik }: { pane: React.RefObject<HTMLDivElement | null>; aktif: number; acik: boolean }) {
  const kelimeBas = useCd(() => (acik ? cdKelimeBas() : -1));
  useEffect(() => {
    if (!hlDestek()) return;
    const el = aktif >= 0 && kelimeBas >= 0 ? pane.current?.querySelector<HTMLElement>(`p[data-i="${aktif}"]`) : null;
    const m = el?.textContent || '';
    if (!el || kelimeBas >= m.length) return void (CSS as any).highlights.delete(HL_KELIME);
    const son = m.slice(kelimeBas).search(/[\s,;:.!?…)"”’]/);
    const range = metinAraligi(el, kelimeBas, son < 0 ? m.length : kelimeBas + Math.max(1, son));
    if (range) (CSS as any).highlights.set(HL_KELIME, new (window as any).Highlight(range));
    else (CSS as any).highlights.delete(HL_KELIME);
  }, [aktif, kelimeBas, pane]);
  useEffect(() => () => {
    if (hlDestek()) (CSS as any).highlights.delete(HL_KELIME);
  }, []);
  return null;
}

/** Seçim araç çubuğu (tasarım S10): metinde seçim yapılınca Notlarım'a ekle · Yıldızla · Kopyala (utils/selectionShare).
 *  "Açıkla / Soru üret" yalnız kullanıcı tıklamasıyla mevcut /api/ai/general-chat ucunu çağırır (otomatik çağrı yok, AGENTS 20). */
function useCdSecimCubugu(paneRef: React.RefObject<HTMLDivElement | null>, detay: CdDetay) {
  useEffect(() => registerSelectionActions(({ host }) => {
    const pane = paneRef.current;
    if (!pane || !pane.contains(host)) return null;
    const pi = Number(host.closest<HTMLElement>('[data-i]')?.dataset.i ?? NaN);
    const bolum = detay.bolumler.find((b) => b.paragraflar.some((x) => x.i === pi));
    const par = bolum?.paragraflar.find((x) => x.i === pi);
    const link = `${pathFor('canli_ders', detay.key)}${Number.isFinite(pi) ? `?p=${pi}` : ''}`;
    return [
      {
        id: 'cd-not', label: 'Nota ekle', icon: 'M4 20l4-1 10-10-3-3L5 16zM14 7l3 3', tone: 'accent',
        run: ({ text }) => {
          try {
            const k = 'medsoru_notlarim_v1';
            const l = JSON.parse(localStorage.getItem(k) || '[]');
            l.unshift({ id: `n${Date.now().toString(36)}`, baslik: `${detay.baslik}${bolum?.baslik ? ` · ${bolum.baslik}` : ''}`, metin: `“${text.trim()}”`, renk: 'blue', at: Date.now(), kaynak: { ad: detay.baslik, bolum: bolum?.baslik, link, t: cdDurum().key === detay.key ? Math.floor(cdDurum().t) : undefined } });
            localStorage.setItem(k, JSON.stringify(l));
            window.dispatchEvent(new Event('medsoru:notlarim'));
            toast.success('Notlarım\'a eklendi', 'Menü › Notlarım');
          } catch { toast.error('Eklenemedi', 'Cihaz depolaması dolu olabilir.'); }
          window.getSelection()?.removeAllRanges();
        },
      },
      ...(par ? [{
        id: 'cd-yildiz', label: 'Spot yap', icon: 'M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.5 2.9 1-6.1L3.2 9.5l6.1-.9z',
        run: () => {
          yildizToggle({ id: `cd_${detay.key}_p${pi}`, kaynak: 'canli_ders', kaynakAd: 'Sesli ders', baslik: detay.baslik, altBaslik: bolum?.baslik, metin: par.metin, deeplink: link, meta: { dersKey: detay.key, paragrafIndex: pi } });
          window.getSelection()?.removeAllRanges();
        },
      }] : []),
      {
        id: 'cd-kart', label: 'Kart', icon: 'M4 7h13v12H4zM7 4h13v12',
        run: ({ text }) => {
          const t = text.trim();
          toggleFavoriteCard({ id: `cd-secim:${detay.key}:${t.slice(0, 80)}`, front: t, back: `${detay.baslik}${bolum?.baslik ? ` · ${bolum.baslik}` : ''}`, group: 'Sesli ders seçimleri' });
          toast.success('Kartlarına eklendi', '');
          window.getSelection()?.removeAllRanges();
        },
      },
      {
        id: 'cd-acikla', label: 'Açıkla', icon: 'M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z',
        run: ({ text }) => { cdAiIste('acikla', text, detay.baslik); window.getSelection()?.removeAllRanges(); },
      },
      // "Soru üret" kaldırıldı: soru yazan özellik kaynak getirmeli (CLAUDE.md Grounding); kaynaksız uç yok
      {
        id: 'cd-kopya', label: 'Kopyala', icon: 'M8 8h11v11H8zM5 16V5h11',
        run: ({ text }) => { void navigator.clipboard?.writeText(text.trim()).then(() => toast.success('Kopyalandı', '')); window.getSelection()?.removeAllRanges(); },
      },
    ];
  }), [paneRef, detay]);
}

function CdMetinBolme({ detay, canli, kamp = false }: { detay: CdDetay; canli: boolean; kamp?: boolean }) {
  const paneRef = useRef<HTMLDivElement>(null);
  useCdSecimCubugu(paneRef, detay);
  useUzunBasSecim(paneRef);
  const aktif = useCd((s) => (canli ? s.aktif : -1));
  const cumle = useCd((s) => (canli ? s.cumle : -1));
  const { durdu, durdur, surdur } = useTakip();
  // Kamp: metin aşama aşama gösterilir; görünen aşama sesi izler, elle seçilince oraya geçer
  const asamalar = useMemo(() => (kamp ? kampAsamalari(detay) : []), [kamp, detay]);
  const asamaOf = useCallback((i: number) => asamalar.find((a) => i >= a.ilkP && i <= a.sonP)?.no ?? -1, [asamalar]);
  const sesAsama = aktif >= 0 ? asamaOf(aktif) : -1;
  const [gorAsama, setGorAsama] = useState<number>(() => {
    const k = cdKayitliAsama(detay.key);
    return k ?? asamalar[0]?.no ?? 0;
  });
  useEffect(() => { if (kamp && sesAsama >= 0 && !durdu) setGorAsama(sesAsama); }, [kamp, sesAsama, durdu]);
  useEffect(() => { if (kamp) cdAsamaKaydet(detay.key, gorAsama); }, [kamp, detay.key, gorAsama]);
  const asamaSec = useCallback((no: number) => {
    setGorAsama(no);
    paneRef.current?.scrollTo({ top: 0 });
    const a = asamalar.find((x) => x.no === no);
    // Ses çalıyorsa o aşamanın başına atlar; çalmıyorsa yalnız metin değişir (Dinle'ye basınca oradan başlar)
    if (!a) return;
    const st = cdDurum();
    if (st.key === detay.key && st.playing) { if (asamaOf(st.aktif) !== no) { cdParagrafa(a.ilkP); surdur(); } }
    else if (st.key === detay.key) cdParagrafa(a.ilkP, false);
    else if (!st.playing) { const v = cdTercihVaryant(detay.varyantlar); if (v) cdOynat(detay, v.id, { oynat: false }); cdParagrafa(a.ilkP, false); }
  }, [asamalar, asamaOf, detay.key, surdur]);
  const gorIdx = asamalar.findIndex((a) => a.no === gorAsama);
  const onceki = useRef<HTMLElement | null>(null);
  const isaret = useRef<{ el: HTMLElement; metin: string } | null>(null);
  const ilk = useRef(true);
  /** Programatik kaydırmanın sürdüğü an (bu süre dışındaki scroll olayları kullanıcınındır) */
  const progUntil = useRef(0);
  const yenidenDene = useRef(0);
  const sonUst = useRef(0);

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
    if (!pane || st.aktif < 0) return;
    // Paragraf henüz çizilmemiş (ders yeni açıldı/aşama değişti): kısa aralıkla birkaç kez yeniden dene
    if (!el) {
      if (yenidenDene.current < 12) { yenidenDene.current += 1; window.setTimeout(() => kaydirRef.current(ani), 120); }
      return;
    }
    yenidenDene.current = 0;
    const z = elementZoom(pane) || 1;
    const pr = pane.getBoundingClientRect();
    let hr = el.getBoundingClientRect();
    // Gizli sekme/aşama (display:none) ya da sıfır boyutlu bölme: ölçüm anlamsız, yanlış konuma kaydırma
    if (pr.height < 8 || (hr.height === 0 && hr.width === 0)) return;
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
    // "Okunan cümleyi ortada tut" (Görünüm › Okuma): bant dar, her cümlede ortalanır
    const bant = document.documentElement.dataset.cdOrtala === 'on' ? 0.04 : 0.18;
    if (!ani && Math.abs(sapma) < pane.clientHeight * bant) return;
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
    sonUst.current = pane.scrollTop;
    const onScroll = () => {
      const n = Date.now();
      // Yerleşim kaynaklı küçük oynamalar (yazı tipi/görsel yüklenmesi, yuvarlama) elle gezinme sayılmaz
      const fark = Math.abs(pane.scrollTop - sonUst.current);
      sonUst.current = pane.scrollTop;
      if (fark < 3) return;
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
    <div className={`cd-bolme cd-metin-bolme${kamp ? ' is-kamp' : ''}`} data-gor-asama={kamp ? gorAsama : undefined}>
      {kamp && asamalar.length > 1 && <KampAsamaCubugu asamalar={asamalar} gor={gorAsama} sesAsama={sesAsama} onSec={asamaSec} />}
      <div className="cd-metin" ref={paneRef} tabIndex={0} aria-label="Konuşma metni">
        {kamp && <style>{`.cd-metin-bolme[data-gor-asama="${gorAsama}"] .cd-bolum[data-asama]:not([data-asama="${gorAsama}"]){display:none}`}</style>}
        <MetinListe detay={detay} onTik={onTik} kamp={kamp} />
        {kamp && gorIdx >= 0 && (
          <div className="cd-k-son">
            {gorIdx > 0 && (
              <button type="button" className="cd-btn" onClick={() => asamaSec(asamalar[gorIdx - 1].no)}>
                <ChevronLeft aria-hidden /> <span>{asamalar[gorIdx - 1].ad}</span>
              </button>
            )}
            {gorIdx < asamalar.length - 1 && (
              <button type="button" className="cd-btn is-ana" onClick={() => asamaSec(asamalar[gorIdx + 1].no)}>
                <span>Sonraki aşama: {asamalar[gorIdx + 1].ad}</span> <ChevronRight aria-hidden />
              </button>
            )}
          </div>
        )}
      </div>
      <CdKelimeIsaret pane={paneRef} aktif={aktif} acik={canli && !durdu} />
      {detay.v2 && <CdV2Su pane={paneRef} aktif={aktif} cumle={cumle} />}
      {durdu && canli ? (
        <button type="button" className="cd-donus" onClick={() => { surdur(); requestAnimationFrame(() => kaydir()); }}>
          <Crosshair aria-hidden /> Canlı konuma dön
        </button>
      ) : (
        null
      )}
    </div>
  );
}

/** Başlık üst satırında etkin bölüm (ders çalarken) */
function DersBolumEtiketi({ detay }: { detay: CdDetay }) {
  const b = useCd((s) => (s.key === detay.key ? s.bolum : -1));
  return b >= 0 ? <> · Bölüm {b + 1} / {detay.bolumler.length}</> : null;
}

/* ---------------- PDF ---------------- */

function CdPdfBolme({ detay, canli }: { detay: CdDetay; canli: boolean }) {
  const pdf = detay.pdf!;
  const info = useDeckPdf(pdf.deckId);
  const aktif = useCd((s) => (canli ? s.aktif : -1));
  const cumle = useCd((s) => (canli ? s.cumle : -1));
  const { durdu, durdur, surdur } = useTakip();
  const [zoom, setZoom] = useState(1);
  const [barGizli, setBarGizli] = useState(() => { try { return localStorage.getItem('cd_pdf_bar_gizli') === '1'; } catch { return false; } });
  const barDegis = () => setBarGizli((g) => { try { localStorage.setItem('cd_pdf_bar_gizli', g ? '0' : '1'); } catch { /* yok */ } return !g; });
  const [sayfaTema, setSayfaTema] = useState<'ozgun' | 'temiz' | 'sepya' | 'gece'>(() => {
    try { const v = localStorage.getItem('medsoru_cd_sayfa_tema'); return v === 'temiz' || v === 'sepya' || v === 'gece' ? v : 'ozgun'; } catch { return 'ozgun'; }
  });
  const sonrakiTema = () => setSayfaTema((t) => {
    const n = ({ ozgun: 'temiz', temiz: 'sepya', sepya: 'gece', gece: 'ozgun' } as const)[t];
    try { localStorage.setItem('medsoru_cd_sayfa_tema', n); } catch { /* yok */ }
    return n;
  });
  const [elle, setElle] = useState<{ dosya: number; sayfa: number } | null>(null);
  const [eslesmeKapali, setEslesmeKapali] = useState(-1);
  const wrapRef = useRef<HTMLDivElement>(null);
  const [hataMsj, setHataMsj] = useState<string | null>(null);

  // Etkin paragrafın eşlemesi; eşlemesi olmayan paragrafta son bilinen sayfada kalınır
  const sonHedef = useRef<{ dosya: number; sayfa: number }>({ dosya: 0, sayfa: 1 });
  const es = aktif >= 0 ? pdf.paragraflar[aktif] : null;
  const isr = aktif >= 0 && cumle >= 0 ? detay.isaret?.[String(aktif)]?.[cumle] ?? null : null;
  // Okunan kelime: cümle içindeki ses ilerlemesine göre son geçilen eşleşmiş kelime (yalnız değişince yeniden çizilir)
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
  // Çıkmış soru seçildiyse dayandığı cümlenin PDF yeri (işaret yoksa paragrafın hizalama sayfası)
  const [cikSec, setCikSec] = useState<CdCikmisKonum | null>(null);
  const cikYer = useMemo(() => {
    if (!cikSec) return null;
    const x = detay.isaret?.[String(cikSec.p)]?.[cikSec.c];
    if (x && x.t !== 'sayfa') return { dosya: x.d, sayfa: Math.max(1, x.s), l: x.l };
    const e = pdf.paragraflar[cikSec.p];
    if (!e) return null;
    const sy = x?.s ?? e.sayfalar?.[cikSec.c] ?? e.sayfa;
    const d = x?.d ?? e.dosyalar?.[cikSec.c] ?? e.dosya ?? 0;
    return Number.isFinite(sy) ? { dosya: d, sayfa: Math.max(1, sy), l: [] as number[][] } : null;
  }, [cikSec, detay.isaret, pdf]);
  // Takip sürerken hedef; durunca kullanıcının baktığı yer (sürdürünce yeniden hedefe kayar).
  // Ders çalmıyorken seçili çıkmış sorunun yeri kalıcıdır.
  const gor = durdu && elle ? elle : cikYer && (!canli || durdu) ? cikYer : hedef;
  // Ön çizim: sıradaki 8 cümlenin slaytları (aynı dosyada) — canlı takip o sayfaya atladığında çizim hazır olur
  const preload = useMemo(() => {
    if (!canli || aktif < 0) return undefined;
    const out: number[] = [];
    let kalan = 8;
    for (let i = aktif; i < pdf.paragraflar.length && kalan > 0; i++) {
      const e = pdf.paragraflar[i];
      const ix = detay.isaret?.[String(i)];
      const n = Math.max(1, e?.sayfalar?.length || ix?.length || 1);
      for (let c = i === aktif ? Math.max(0, cumle) : 0; c < n && kalan > 0; c++, kalan--) {
        const x = ix?.[c];
        const d = x ? x.d : (e?.dosyalar?.[c] ?? e?.dosya ?? 0);
        const sy = x && x.t !== 'sayfa' ? x.s : (e?.sayfalar?.[c] ?? e?.sayfa);
        if (d === gor.dosya && sy && !out.includes(sy)) out.push(sy);
      }
    }
    return out;
  }, [canli, aktif, cumle, pdf, detay.isaret, gor.dosya]);
  // Panel sayfaya sığmadıysa (cizim_uret: ek_alt) o sayfa altına boş alan eklenerek uzatılır; ders boyunca sabit
  // (anlatılan cümleye göre değişirse sayfalar kayardı)
  const ekAlt = useMemo(() => {
    const out: Record<number, { h: number; renk?: string }> = {};
    for (const cs of Object.values(detay.isaret || {})) {
      for (const x of cs || []) {
        if (!x || x.d !== gor.dosya) continue;
        for (const z of ((x as any).z || []) as any[]) {
          if (z?.ek_alt > 0) out[z.s] = { h: Math.max(out[z.s]?.h || 0, Math.min(0.6, z.ek_alt)), renk: z.ek_renk || out[z.s]?.renk };
        }
      }
    }
    return Object.keys(out).length ? out : null;
  }, [detay.isaret, gor.dosya]);
  // Terim + kısaltma katmanları tek haritada: PDF'te ikisi birlikte işaretlenir (kısaltmalar mavi kesikli)
  const terimKatman = useMemo(() => cdTerimKatmani(detay.terim, detay.kisaltma), [detay.terim, detay.kisaltma]);
  const terimDosya = terimKatman?.[String(gor.dosya)] || null;
  const gorunum = usePdfGorunum();
  const { v15 } = useAppearance();
  // Kelime takibi yalnız işaret katmanında (useFocus): görüntüleyici cümle başına bir kez çizilir, kelimede yeniden çizilmez
  const marks = useMemo<PdfMarks | null>(() => {
    // Slayt aynıysa (gor.sayfa === isr.s) kullanıcı elle kaysa/durdursa bile işaret ve çizim gizlenmez (kullanıcı inceleyebilsin)
    const ayniSayfa = isr ? isr.s === gor.sayfa : false;
    if (!canli || (durdu && !ayniSayfa) || !isr || (isr.t === 'sayfa' && !isr.y?.length && !(isr as any).z?.length) || isr.d !== gor.dosya) return null;
    const ws = isr.w;
    const yol = isr.y?.length ? isr.y : undefined;
    const useChar = (): number => useCd(() => cdKonusulanKarakter()?.c ?? -1);
    const useFocus = (): number => useCd(() => {
      if (!ws.length) return -1;
      const k = cdKonusulanKarakter();
      if (!k) return -1;
      // yalnız o an konuşulan kelimenin slayttaki karşılığı; karşılıksız kelimede işaret yok
      return ws.findIndex((w) => k.c >= w[0] && k.c < w[1]);
    });
    // H60 / H61: Çizim KESİNLİKLE yalnız o an okunan cümlenin kendi çizimidir (isr.z).
    // Sayfadaki tüm çizimler toplanamaz; aksi takdirde aynı anda 3 konum işaretlenir, iç içe çizgiler biner
    // ve her yeni cümleye geçildiğinde animasyon baştan tekrar oynar.
    let cizim = ((isr as any).z || undefined) as PdfMarks['cizim'];
    // PDF görünüm anahtarları (2026-10-26): kapatılan işaretçi hiç çizilmez
    if (!gorunum.tablo && isr.t === 'tablo') return null;
    // H85: okunabilir metinli tabloda çizim/panel/zoom yok — yalnız marker (işaret katmanı)
    if (isr.t === 'tablo') cizim = undefined;
    let lines = isr.l, words = ws.map((w) => w.slice(2)), path = yol;
    if (!gorunum.resim) {
      if (isr.t === 'resim') { lines = []; path = undefined; }
      // resim üstü kontur/eğri/odak çizimi yok, yakınlaştırma yok
      cizim = cizim?.filter((z) => z.tur !== 'kontur' && z.tur !== 'egri_faz' && !z.odak).map((z) => (z.yakin ? { ...z, yakin: undefined } : z));
    }
    if (!gorunum.iliski) cizim = cizim?.filter((z) => z.tur !== 'akis' && z.tur !== 'sema');
    if (!gorunum.metin && isr.t !== 'resim') { lines = []; words = []; path = undefined; }
    if (!gorunum.metin) words = [];
    if (!cizim?.length) cizim = undefined;
    if (!lines.length && !words.length && !path && !cizim) return null;
    return { page: isr.s, kind: isr.t, lines, words, useFocus, path, useChar: path || cizim?.length ? useChar : undefined, cizim };
  }, [canli, durdu, isr, gor.dosya, gor.sayfa, gorunum]);

  useEffect(() => { if (!durdu) setElle(null); }, [durdu]);

  // Sözleşmedeki dosya → sunucu akış adresi (ad/Drive kimliğiyle eşle, olmazsa sıra)
  const dosya = pdf.dosyalar[gor.dosya] || pdf.dosyalar[0];
  const sf = info?.files.find((f) => (dosya?.fileId && f.fileId === dosya.fileId) || f.name === dosya?.name) || info?.files[gor.dosya];
  const src = sf?.url;

  useEffect(() => {
    const w = wrapRef.current;
    if (!w) return;
    // Çizim açıkken sayfaya dokunmak canlı takibi bırakmaz (kalemle çizilen sayfa anlatılan sayfa olabilir)
    const on = (e: Event) => {
      if ((e.target as Element | null)?.closest?.('.cd-trm, .cd-trm-panel')) return; // terime dokunmak takibi bırakmaz
      if (getDrawingGlobalState().activeMode === 'none') durdur();
    };
    const hep = () => durdur();
    w.addEventListener('wheel', hep, { passive: true });
    w.addEventListener('touchmove', on, { passive: true });
    w.addEventListener('pointerdown', on);
    return () => {
      w.removeEventListener('wheel', hep);
      w.removeEventListener('touchmove', on);
      w.removeEventListener('pointerdown', on);
    };
  }, [durdur, src]);

  const onVisible = useCallback((p: number) => {
    if (durdu) setElle({ dosya: gor.dosya, sayfa: p });
  }, [durdu, gor.dosya]);

  const cizimAcik = useDrawingGlobalState().activeMode !== 'none';
  // Çizim kapsamı: ders + dosya + sayfa (tarayıcıda kalır); ekrandan çıkınca araç kapanır
  const cizimKok = `cd:${detay.key}:${dosya?.fileId || dosya?.name || gor.dosya}`;
  const pageOverlay = useCallback((n: number) => (
    <React.Fragment key={n}>
      {cikYer && cikSec && cikYer.dosya === gor.dosya && cikYer.sayfa === n && (
        <div className="cd-cik-kat" aria-hidden>
          {cikYer.l.map((b, i) => <span key={i} className="cd-cik-kutu" style={{ left: `${b[0] * 100}%`, top: `${b[1] * 100}%`, width: `${(b[2] - b[0]) * 100}%`, height: `${(b[3] - b[1]) * 100}%` }} />)}
        </div>
      )}
      <SlideDrawingCanvas scope={`${cizimKok}:${n}`} controls={false} />
      {gorunum.cikmis && <CdCikmisChip sorular={cikmisSayfada(detay.cikmisKonum, gor.dosya, n)} />}
      {terimDosya?.[String(n)] && (
        <CdTerimKatman sayfa={terimDosya[String(n)]} gizle={cizimAcik} />
      )}
    </React.Fragment>
  ), [cizimKok, cikYer, cikSec, gor.dosya, terimDosya, cizimAcik, detay.cikmisKonum, gorunum.cikmis]);
  const cikmisSec = useCallback((q: CdCikmisKonum | null) => {
    setCikSec(q);
    if (q) { setElle(null); durdur(); }
  }, [durdur]);
  const geriAlinir = useCanUndoDrawing();
  useEffect(() => () => setDrawingGlobalState({ activeMode: 'none' }), []);

  return (
    <div className={`cd-bolme cd-pdf-bolme${barGizli ? ' is-bar-gizli' : ''}`}>
      <CdCikmisPencereKok />
      <button type="button" className="cd-ib cd-bar-tgl is-ac" onClick={barDegis} aria-label="PDF araç çubuğunu göster" title="Araç çubuğunu göster"><ChevronDown /></button>
      <div className="cd-pdf-bar">
        <button type="button" className="cd-ib cd-bar-tgl is-gizle" onClick={barDegis} aria-label="PDF araç çubuğunu gizle" title="Araç çubuğunu gizle"><ChevronUp /></button>
        <FileText aria-hidden />
        {pdf.sayfaKaynak?.[gor.sayfa - 1] ? (() => {
          // Özet (kırpılmış) PDF: sayfanın asıl dersi ve slayt numarası (Son Prova)
          const k = pdf.sayfaKaynak![gor.sayfa - 1];
          return <span className="cd-pdf-ad" title={`${k.no}) ${k.ad} · slayt ${k.s} — özet PDF sayfa ${gor.sayfa}/${dosya?.pages || ''}`}>{k.no}) {k.ad} · <b>slayt {k.s}</b></span>;
        })() : <>
          <span className="cd-pdf-ad" title={dosya?.name}>{dosya?.name || 'Ders PDF\'i'}</span>
          <span className="cd-pdf-sayfa">s. {gor.sayfa}{dosya?.pages ? ` / ${dosya.pages}` : ''}</span>
        </>}
        {pdf.dosyalar.length > 1 && (
          <span className="cd-pdf-dosya">{(gor.dosya || 0) + 1}/{pdf.dosyalar.length}</span>
        )}
        <span className="cd-grow" />
        {!!detay.cikmisKonum?.length && <CikmisKonumDugme liste={detay.cikmisKonum} secili={cikSec} onSec={cikmisSec} />}
        {/* v15: terim ve görünüm üst bara/Görünüm çekmecesine taşındı; çizim araçları PDF'in yanında yüzer */}
        {v15 ? (
          <CdV15KalemDugme />
        ) : (
          <>
            {terimDosya && <TerimDugme />}
            <PdfGorunumDugme />
            <CizimDugme />
            <button type="button" className="cd-ib" onClick={undoLastDrawing} disabled={!geriAlinir} aria-label="Son çizimi geri al" title="Son çizimi geri al"><Undo2 /></button>
          </>
        )}
        {/* H332: v15'te sayfa teması (seyrek) PDF ⋯ menüsüne girdi; yakınlaştırma masaüstünde görünür, telefonda (≤600 px) menüde */}
        {!v15 && <button type="button" className="cd-ib" onClick={sonrakiTema} aria-label="Sayfa temasını değiştir" title={`Sayfa teması: ${({ ozgun: 'Özgün', temiz: 'Temiz', sepya: 'Sepya', gece: 'Gece' })[sayfaTema]} (değiştirmek için tıkla)`}><Palette /></button>}
        <button type="button" className="cd-ib cd-pdf-zb" onClick={() => setZoom((z) => Math.max(0.5, +(z - 0.25).toFixed(2)))} aria-label="Uzaklaştır" title="Uzaklaştır"><Minus /></button>
        <span className="cd-pdf-zoom">{Math.round(zoom * 100)}%</span>
        <button type="button" className="cd-ib cd-pdf-zb" onClick={() => setZoom((z) => Math.min(3, +(z + 0.25).toFixed(2)))} aria-label="Yakınlaştır" title="Yakınlaştır"><Plus /></button>
        {v15 && (
          <CdTasmaMenu etiket="PDF seçenekleri" className="cd-pdf-tm" ogeler={[
            { ad: `Sayfa teması: ${({ ozgun: 'Özgün', temiz: 'Temiz', sepya: 'Sepya', gece: 'Gece' })[sayfaTema]}`, ikon: <Palette />, ipucu: 'değiştir', kalAcik: true, onSec: sonrakiTema },
            { ad: 'Yakınlaştır', ikon: <Plus />, ipucu: `%${Math.round(zoom * 100)}`, kalAcik: true, disabled: zoom >= 3, ayrac: true, onSec: () => setZoom((z) => Math.min(3, +(z + 0.25).toFixed(2))) },
            { ad: 'Uzaklaştır', ikon: <Minus />, kalAcik: true, disabled: zoom <= 0.5, onSec: () => setZoom((z) => Math.max(0.5, +(z - 0.25).toFixed(2))) },
            { ad: 'Sayfaya sığdır (%100)', ikon: <FileText />, kalAcik: true, disabled: zoom === 1, onSec: () => setZoom(1) },
          ]} />
        )}
      </div>
      {v15 && <CdV15KalemKutusu />}
      <div className={`cd-pdf-govde dpv-body tema-${sayfaTema}`} ref={wrapRef}>
        {!info ? (
          <div className="cd-bos" role="status"><span className="cd-spin" aria-hidden /> PDF aranıyor…</div>
        ) : src && !hataMsj ? (
          <Suspense fallback={<div className="cd-bos" role="status"><span className="cd-spin" aria-hidden /> Görüntüleyici yükleniyor…</div>}>
            <PdfDocView
              key={src}
              src={src}
              page={gor.sayfa}
              highlight={cikYer && gor === cikYer ? [cikYer.sayfa, cikYer.sayfa] : canli && !durdu && es ? [hedef.sayfa, hedef.sayfa] : undefined}
              highlightLabel={cikYer && gor === cikYer ? `Çıkmış soru${cikSec?.yil ? ` · ${cikSec.yil}` : ''}` : 'Şu an anlatılan'}
              marks={marks}
              notes={gorunum.not ? detay.ogrenciNot?.[String(gor.dosya)] || null : null}
              preload={preload}
              zoom={zoom}
              onZoom={setZoom}
              onVisiblePage={onVisible}
              onError={setHataMsj}
              fit="width"
              pageOverlay={pageOverlay}
              ekAlt={gorunum.iliski ? ekAlt : null}
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
      {/* tasarım S14: anlatılan paragrafın PDF eşleşmesi yoksa slayt soluklaşır, son eşleşen sayfa söylenir */}
      {canli && !durdu && aktif >= 0 && !(es && Number.isFinite(es.sayfa)) && eslesmeKapali !== aktif && (
        <div className="cd-eslesme-yok" role="status">
          <MapPin aria-hidden />
          <div><b>Bu bölüm PDF'te bulunamadı</b><small>Hoca slayt dışında anlatıyor. Son eşleşen yer: s. {hedef.sayfa}.</small></div>
          <div className="cd-eslesme-d">
            <button type="button" onClick={() => setEslesmeKapali(aktif)}>s. {hedef.sayfa}'te kal</button>
            <button type="button" onClick={durdur}>PDF'i elle gez</button>
          </div>
        </div>
      )}
      {durdu && canli && (
        <button type="button" className="cd-donus" onClick={surdur}>
          <Crosshair aria-hidden /> Canlı konuma dön
        </button>
      )}
    </div>
  );
}

/** PDF çubuğunda "Çıkmış N": dersin çıkmış soruları; seçilen sorunun dayandığı yer PDF'te sayfa + bölge olarak vurgulanır */
function CikmisKonumDugme({ liste, secili, onSec }: { liste: CdCikmisKonum[]; secili: CdCikmisKonum | null; onSec: (q: CdCikmisKonum | null) => void }) {
  const [acik, setAcik] = useState(false);
  const i = secili ? liste.indexOf(secili) : -1;
  return (
    <div className="cd-cik">
      <Popover open={acik} onOpenChange={setAcik}>
        <PopoverTrigger asChild>
          <button type="button" className={`cd-cik-btn${secili ? ' is-on' : ''}`} title="Bu dersin çıkmış soruları: dokun, sorunun dayandığı yer PDF'te işaretlensin">
            <Star aria-hidden /> <span className="cd-cik-ad">Çıkmış</span> <b>{liste.length}</b>
          </button>
        </PopoverTrigger>
        <PopoverContent className="cd-cik-panel" aria-label="Çıkmış sorular">
          <div className="cd-cik-bas">
            <span>Çıkmış sorular · PDF'teki yeri</span>
            {secili && <button type="button" className="cd-cik-temizle" onClick={() => { onSec(null); setAcik(false); }}>Vurguyu kaldır</button>}
          </div>
          <div role="listbox" aria-label="Çıkmış sorular">
            {liste.map((q, k) => (
              <button key={q.id} type="button" role="option" aria-selected={q === secili} className={`cd-cik-oge${q === secili ? ' is-on' : ''}`}
                onClick={() => { onSec(q); setAcik(false); }}>
                <span className="cd-cik-oge-no">{k + 1}</span>
                <span className="cd-cik-oge-m">
                  <span className="cd-cik-oge-kok">{q.kok}</span>
                  {q.cevap && <span className="cd-cik-oge-cvp">Cevap: {q.cevap}</span>}
                </span>
                {q.yil && <span className="cd-cik-oge-yil">{q.yil}</span>}
              </button>
            ))}
          </div>
        </PopoverContent>
      </Popover>
      {secili && (
        <span className="cd-cik-gez">
          <button type="button" className="cd-ib" aria-label="Önceki çıkmış soru" disabled={i <= 0} onClick={() => onSec(liste[i - 1])}><ChevronLeft /></button>
          <span className="cd-cik-no">{i + 1}/{liste.length}</span>
          <button type="button" className="cd-ib" aria-label="Sonraki çıkmış soru" disabled={i >= liste.length - 1} onClick={() => onSec(liste[i + 1])}><ChevronRight /></button>
        </span>
      )}
    </div>
  );
}

/** PDF çubuğunda tek düğme: çizim aracı (kalem / fosforlu / silgi) ve renk açılır panelde; araç açıkken düğme vurgulu */
function CizimDugme() {
  const st = useDrawingGlobalState();
  const appearance = useAppearance();
  const acik = st.activeMode !== 'none';
  return (
    <Popover>
      <PopoverTrigger asChild>
        <button type="button" className={`cd-cik-btn cd-ciz-btn${acik ? ' is-on' : ''}`} aria-label="PDF'e yaz ve çiz" title="PDF'e yaz ve çiz">
          <PenTool aria-hidden /> <span className="cd-cik-ad">{acik ? ({ pen: 'Kalem', highlighter: 'Fosforlu', eraser: 'Silgi' } as Record<string, string>)[st.activeMode] : 'Çiz'}</span>
        </button>
      </PopoverTrigger>
      <PopoverContent className="cd-ciz-panel" aria-label="Çizim araçları">
        <ToggleGroup type="single" value={st.activeMode} aria-label="Araç"
          onValueChange={(v) => setDrawingGlobalState({ activeMode: (v || 'none') as typeof st.activeMode })}>
          <ToggleGroupItem value="none" aria-label="Kapalı"><MousePointer2 aria-hidden /> Kapalı</ToggleGroupItem>
          <ToggleGroupItem value="pen" aria-label="Kalem"><PenTool aria-hidden /> Kalem</ToggleGroupItem>
          <ToggleGroupItem value="highlighter" aria-label="Fosforlu kalem"><Highlighter aria-hidden /> Fosforlu</ToggleGroupItem>
          <ToggleGroupItem value="eraser" aria-label="Silgi"><Eraser aria-hidden /> Silgi</ToggleGroupItem>
        </ToggleGroup>
        <div className="cd-ciz-renk" role="radiogroup" aria-label="Renk">
          {penPalette(appearance.mode).map((c) => (
            <button key={c.id} type="button" role="radio" aria-checked={st.color === c.hex} aria-label={c.label} title={c.label}
              style={{ background: c.hex }} onClick={() => setDrawingGlobalState({ color: c.hex, activeMode: st.activeMode === 'none' || st.activeMode === 'eraser' ? 'pen' : st.activeMode })} />
          ))}
        </div>
        <p className="cd-ciz-not">Çizimler bu cihazda, ders ve sayfa başına saklanır. Kalemli cihazda parmak sayfayı kaydırır.</p>
      </PopoverContent>
    </Popover>
  );
}

/** ⋯ menüsü: motivasyon konuşmaları ve mola hatırlatması (varsayılan kapalı) */
function MotivasyonDugme() {
  const acik = useCdMotivasyonAcik();
  return (
    <button type="button" className={`cd-btn${acik ? ' is-on' : ''}`} aria-pressed={acik} onClick={() => cdMotivasyonAyarla(!acik)}
      title="Dersin başında, ortasında ve sonunda kısa teşvik cümleleri; 15–20 dakikada bir mola hatırlatması">
      <Sparkles aria-hidden /> <span>Motivasyon konuşmaları {acik ? 'açık' : 'kapalı'}</span>
    </button>
  );
}
