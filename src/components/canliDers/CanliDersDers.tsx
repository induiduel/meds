/**
 * Canlı ders ekranı (/canliders/<key>): üç görünüm — Metin, Metin + PDF (bölünmüş: masaüstünde yan yana, telefonda üst-alt),
 * yalnız PDF (seçim cihazda saklanır). Tam ekran: kabuk gizlenir, oynatıcı saklanır ama tek dokunuşla açılır.
 * Metin sesle akar (etkin paragraf + tahmini cümle vurgusu), görünüm etkin paragrafı ortada tutar; kullanıcı elle
 * kaydırınca/PDF'i gezince takip 8 sn durur ve "Canlı konuma dön" çıkar. Oynatıcı alt çubuktadır (CanliDersDock).
 */
import React, { Suspense, lazy, memo, useCallback, useEffect, useLayoutEffect, useRef, useState } from 'react';
import { ChevronLeft, ChevronUp, Columns2, Crosshair, FileText, Maximize2, Minimize2, Minus, Pause, Play, Plus, ScrollText } from 'lucide-react';
import { navigateTo, pathFor } from '../../router';
import { driveViewUrl, useDeckPdf } from '../../services/deckPdfService';
import {
  cdCumleAraligi, cdDetayBagla, cdDetayGetir, cdDurum, cdOynat, cdParagrafa, cdToggle, fmtSure, useCd, type CdDetay,
} from './canliDersStore';
import { useCdTur } from './useCdTur';
import { cdDersEtiketi } from './canliDersKategori';
import { ListeEkleDugme } from './CanliDersListem';
import { CevrimdisiDugme } from './CanliDersCevrimdisi';
import { CdDaha } from './CanliDersDaha';
import { CdTvKumanda } from './CanliDersTv';
import '../learn/pdf/pdfDoc.css';

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

export default function CanliDersDers({ dersKey }: { dersKey: string }) {
  const [detay, setDetay] = useState<CdDetay | null>(null);
  const [hata, setHata] = useState<string | null>(null);
  const [baglanti, setBaglanti] = useState<'bagli' | 'yuklendi' | 'baska' | null>(null);
  const [genis, setGenis] = useState(genisMi);
  const [gorunum, setGorunumDurum] = useState<Gorunum>(ilkGorunum);
  const setGorunum = (g: Gorunum) => {
    setGorunumDurum(g);
    try { localStorage.setItem(GORUNUM_KEY, g); } catch { /* yok */ }
  };
  const [tamEkran, setTamEkran] = useState(false);
  const [yazi, setYaziDurum] = useState<number>(() => { try { return Number(localStorage.getItem(YAZI_KEY)) || 20; } catch { return 20; } });
  const setYazi = (n: number | ((y: number) => number)) => setYaziDurum((y) => {
    const v = Math.min(YAZI_ENCOK, Math.max(YAZI_ENAZ, typeof n === 'function' ? n(y) : n));
    try { localStorage.setItem(YAZI_KEY, String(v)); } catch { /* yok */ }
    return v;
  });
  const [oynaticiAcik, setOynaticiAcik] = useState(false);
  const rootRef = useRef<HTMLDivElement>(null);
  const [yuk, setYuk] = useState<number | null>(null);
  const caliyorKey = useCd((s) => s.key);
  const caliyorBaslik = useCd((s) => s.baslik);
  const tanitim = useCdTur('ders', !!detay, () => !!document.querySelector('.cd-dock') && !!document.querySelector('.cd-metin p'));

  useEffect(() => {
    let canli = true;
    setHata(null);
    cdDetayGetir(dersKey).then(
      (d) => {
        if (!canli) return;
        setDetay(d);
        setBaglanti(cdDetayBagla(d));
        document.title = `${cdDersEtiketi(d)} · ${d.baslik} · Canlı ders · MeDSor`;
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

  // Tam ekran: kabuk (menü, üst çubuk, alt sekmeler) gizlenir; oynatıcı saklı, "Oynatıcı" ile açılır.
  // Tarayıcı tam ekranı da istenir (destekleyen yerde); Esc ya da tarayıcıdan çıkış modu kapatır.
  useEffect(() => {
    const kok = document.documentElement;
    kok.classList.toggle('cd-tam-ekran', tamEkran);
    kok.classList.toggle('cd-tam-oynatici', tamEkran && oynaticiAcik);
    window.dispatchEvent(new Event('cd:dock'));
    if (!tamEkran) return;
    const onKey = (e: KeyboardEvent) => {
      const hedef = e.target as HTMLElement | null;
      if (!e.ctrlKey && !e.metaKey && !e.altKey && !hedef?.closest('input, textarea, [contenteditable="true"]')) {
        if (e.key === '+' || e.key === '=') { e.preventDefault(); setYazi((y) => y + 2); return; }
        if (e.key === '-') { e.preventDefault(); setYazi((y) => y - 2); return; }
      }
      if (e.key !== 'Escape' || document.querySelector('.cd-tur, .gu-ortu, [role="dialog"][aria-modal="true"]')) return;
      setTamEkran(false);
    };
    const onFs = () => { if (!document.fullscreenElement) setTamEkran(false); };
    document.addEventListener('keydown', onKey);
    document.addEventListener('fullscreenchange', onFs);
    return () => {
      document.removeEventListener('keydown', onKey);
      document.removeEventListener('fullscreenchange', onFs);
    };
  }, [tamEkran, oynaticiAcik]);
  useEffect(() => () => {
    document.documentElement.classList.remove('cd-tam-ekran', 'cd-tam-oynatici');
    if (document.fullscreenElement) void document.exitFullscreen?.().catch(() => {});
  }, []);
  const tamEkranAc = () => {
    setOynaticiAcik(false);
    setTamEkran(true);
    const kok = document.documentElement as HTMLElement & { webkitRequestFullscreen?: () => void };
    try {
      if (kok.requestFullscreen) void kok.requestFullscreen({ navigationUI: 'hide' }).catch(() => {});
      else kok.webkitRequestFullscreen?.();
    } catch { /* desteklenmiyor: yalnız sayfa içi tam ekran */ }
  };
  const tamEkranKapat = () => {
    setTamEkran(false);
    if (document.fullscreenElement) void document.exitFullscreen?.().catch(() => {});
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
      let alt = window.visualViewport?.height || window.innerHeight;
      const dock = document.querySelector('.cd-dock');
      if (dock) alt = Math.min(alt, dock.getBoundingClientRect().top);
      const tabs = document.querySelector<HTMLElement>('.s12-tabs, .sh-tabs');
      if (tabs) {
        const tr = tabs.getBoundingClientRect();
        if (tr.height > 0 && tr.top < alt && getComputedStyle(tabs).display !== 'none') alt = Math.min(alt, tr.top);
      }
      const z = elementZoom(el) || 1;
      setYuk(Math.max(320, (alt - Math.max(0, top) - 10) / z));
    };
    const plan = () => { if (!t) t = window.setTimeout(olc, 30); };
    olc();
    window.addEventListener('resize', plan);
    window.addEventListener('cd:dock', plan);
    const ro = new ResizeObserver(plan);
    ro.observe(document.documentElement);
    document.documentElement.classList.add('cd-ders-acik');
    return () => {
      window.clearTimeout(t);
      window.removeEventListener('resize', plan);
      window.removeEventListener('cd:dock', plan);
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
          <button type="button" className="cd-btn is-ana" onClick={() => navigateTo(pathFor('canli_ders'))}>Tüm canlı derslere dön</button>
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

  return (
    <div
      className={`cd-root cd-ders is-${mod}${tamEkran ? ' is-tam' : ''}`}
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
          {!tamEkran && (
            <>
            </>
          )}
        </div>
        <div className="cd-ders-uc">
          <CdTvKumanda />
          {!tamEkran && (
            <CdDaha etiket="Ders seçenekleri (çevrimdışı, listem, tanıtım)" className="cd-ders-daha">
              <CevrimdisiDugme dersKey={detay.key} baslik={detay.baslik} varyantlar={detay.varyantlar} />
              <ListeEkleDugme dersKey={detay.key} baslik={detay.baslik} etiketli />
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
              {!oynaticiAcik && <TamEkranOynat dersKey={detay.key} />}
              <button
                type="button"
                className={`cd-btn is-ikon cd-tam-oyn${oynaticiAcik ? ' is-on' : ''}`}
                onClick={() => setOynaticiAcik((x) => !x)}
                aria-pressed={oynaticiAcik}
                aria-label={oynaticiAcik ? 'Oynatıcıyı gizle' : 'Oynatıcıyı göster'}
                title={oynaticiAcik ? 'Oynatıcıyı gizle' : 'Oynatıcıyı göster'}
              >
                <ChevronUp aria-hidden />
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
      <div className={`cd-govde${mod === 'ikisi' ? (genis ? ' is-iki' : ' is-ust-alt') : ''}`}>
        {pdfGoster && <CdPdfBolme detay={detay} canli={buDers} />}
        {metinGoster && <CdMetinBolme detay={detay} canli={buDers} />}
      </div>
      {tanitim.tur}
    </div>
  );
}

/** Tam ekranda oynatıcı saklıyken başlıkta: oynat/duraklat + geçen süre */
function TamEkranOynat({ dersKey }: { dersKey: string }) {
  const buDers = useCd((s) => s.key === dersKey);
  const playing = useCd((s) => s.key === dersKey && s.playing);
  const t = useCd((s) => (s.key === dersKey ? Math.floor(s.t) : 0));
  const dur = useCd((s) => (s.key === dersKey ? s.dur : 0));
  return (
    <span className="cd-tam-ses">
      <span className="cd-tam-ses-t" aria-hidden>{fmtSure(t)}{dur ? ` / ${fmtSure(dur)}` : ''}</span>
      <button type="button" className="cd-oynat" onClick={() => buDers && cdToggle()} disabled={!buDers} aria-label={playing ? 'Duraklat' : 'Oynat'} title={playing ? 'Duraklat' : 'Oynat'}>
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
      <ChevronLeft aria-hidden /> <span>Canlı dersler</span>
    </a>
  );
}

/* ---------------- metin ---------------- */

const hlDestek = () => typeof CSS !== 'undefined' && 'highlights' in CSS && typeof (window as any).Highlight === 'function';
const HL_AD = 'cd-cumle';

/** Paragraf listesi bir kez çizilir; vurgu DOM üzerinden değişir (uzun metinde yeniden çizim yok). */
const MetinListe = memo(function MetinListe({ detay, onTik }: { detay: CdDetay; onTik: (i: number) => void }) {
  return (
    <>
      {detay.bolumler.map((b, bi) => (
        <section key={bi} className="cd-bolum" aria-label={b.baslik || `Bölüm ${bi + 1}`}>
          {b.baslik && <h2 className="cd-bolum-ad">{b.baslik}</h2>}
          {b.paragraflar.map((p) => (
            <p key={p.i} data-i={p.i} className="cd-p" onClick={() => onTik(p.i)}>{p.metin}</p>
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
  }, [detay]);

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
        m.el.textContent = m.metin;
        isaret.current = null;
      }
    };
    const el = aktif >= 0 ? pEl(aktif) : null;
    const r = el ? cdCumleAraligi(aktif, cumle) : null;
    if (!el || !r) return void temizle();
    if (destek) {
      const node = el.firstChild;
      if (!node || node.nodeType !== Node.TEXT_NODE) return void temizle();
      const len = (node.textContent || '').length;
      const range = document.createRange();
      range.setStart(node, Math.min(r[0], len));
      range.setEnd(node, Math.min(r[1], len));
      (CSS as any).highlights.set(HL_AD, new (window as any).Highlight(range));
    } else {
      const m = isaret.current;
      const metin = m && m.el === el ? m.metin : el.textContent || '';
      if (m && m.el !== el) m.el.textContent = m.metin;
      el.textContent = '';
      el.append(document.createTextNode(metin.slice(0, r[0])));
      const mk = document.createElement('mark');
      mk.className = 'cd-cumle';
      mk.textContent = metin.slice(r[0], r[1]);
      el.append(mk, document.createTextNode(metin.slice(r[1])));
      isaret.current = { el, metin };
    }
  }, [aktif, cumle]);
  useEffect(() => () => {
    if (hlDestek()) (CSS as any).highlights.delete(HL_AD);
  }, []);

  // Otomatik kaydırma: etkin paragraf (uzunsa cümle) görünür alanın ortasına yakın
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
    progUntil.current = Date.now() + (ani ? 150 : 1000);
    pane.scrollTo({ top: Math.max(0, pane.scrollTop + sapma), behavior: ani ? 'auto' : 'smooth' });
  }, []);
  useEffect(() => {
    if (!canli || durdu || aktif < 0) return;
    const ani = ilk.current;
    ilk.current = false;
    // content-visibility tahmini yüksekliklerle uzağa atlama: önce anında, sonra ince ayar
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
  const { durdu, durdur, surdur } = useTakip();
  const [zoom, setZoom] = useState(1);
  const [elle, setElle] = useState<{ dosya: number; sayfa: number } | null>(null);
  const wrapRef = useRef<HTMLDivElement>(null);
  const [hataMsj, setHataMsj] = useState<string | null>(null);

  // Etkin paragrafın eşlemesi; eşlemesi olmayan paragrafta son bilinen sayfada kalınır
  const sonHedef = useRef<{ dosya: number; sayfa: number }>({ dosya: 0, sayfa: 1 });
  const es = aktif >= 0 ? pdf.paragraflar[aktif] : null;
  if (es && Number.isFinite(es.sayfa)) sonHedef.current = { dosya: es.dosya || 0, sayfa: Math.max(1, es.sayfa) };
  if (aktif < 0 && !canli) {
    const ilk = pdf.paragraflar.find((x) => x && Number.isFinite(x.sayfa));
    if (ilk && sonHedef.current.sayfa === 1 && sonHedef.current.dosya === 0) sonHedef.current = { dosya: ilk.dosya || 0, sayfa: Math.max(1, ilk.sayfa) };
  }
  const hedef = sonHedef.current;
  // Takip sürerken hedef; durunca kullanıcının baktığı yer (sürdürünce yeniden hedefe kayar)
  const gor = durdu && elle ? elle : hedef;

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
