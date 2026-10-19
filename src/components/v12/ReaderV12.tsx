/**
 * Okuma yüzeyi çerçevesi — v12 "Net" (canvas panosu Notes.dc.html). Ders notları, ders özetleri ve ses kayıtları
 * okuyucuları bu kabuğu paylaşır; yalnız data-design='v12' iken çizilir (v10/v11 okuyucuları olduğu gibi kalır).
 *
 * Yapı (canvas ile birebir):
 *  - Üst çubuk: geri · başlık (1 satır) + künye · A− 17 A+ (görünüm yazı boyutu) · Tırnaklı | Düz (okuma yazı tipi)
 *    · Odak · İçindekiler · çağıranın araçları (kalem, arama) · Diğer seçenekler (⋮ menü)
 *  - 2 px okuma ilerleme çizgisi
 *  - Gövde: katlanır içindekiler (etkin başlık vurgulu) · okuma sütunu (Literata ~17 px, en çok 68ch) · geniş ekranda
 *    "Notlarım" kenar paneli. Odak açıkken içindekiler ve kenar paneli kapanır, okuyucu kenar menünün üstüne genişler.
 *  - Dar alanda (kap < 900 px) içindekiler üst çubuğun altında açılır katman olur; < 640 px yazı denetimleri ⋮ menüye iner.
 * Yazı boyutu ve yazı tipi uygulama görünüm tercihidir (appearance.textSize / reading) — tüm okuma yüzeyleri ortak.
 * İlerleme ve etkin bölüm çağırandan gelebilir (özet okuyucusu kendi kaydını tutar); gelmezse çerçeve kendisi
 * `[data-r12-sec]` başlıklarından hesaplar. Stil: styles/v12/reader.css (.r12-*).
 */
import React, { useCallback, useEffect, useLayoutEffect, useRef, useState } from 'react';
import { AlignLeft, ChevronLeft, ChevronRight, Focus, Maximize2, Minimize2, MoreVertical } from 'lucide-react';
import { useAppearance, TEXT_PX_MAX, TEXT_PX_MIN } from '../../utils/appearance';
import { lockScroll, unlockScroll } from '../../utils/scrollLock';
import { detectIosDevice, openPwaInstallGuide } from '../../services/pwaService';
import { wasRecentlyScrollingOrTouching } from '../../utils/fullscreen';
import { toast } from '../ui/Toast';
import '../../styles/v12/reader.css';

export interface ReaderTocItem {
  id: string;
  title: string;
  /** 2 = bölüm, 3 = alt başlık (girintili) */
  level?: 2 | 3;
  /** Sağda küçük sayı (soru/spot sayısı vb.) */
  count?: number;
}

export interface ReaderV12Props {
  title: string;
  meta?: React.ReactNode;
  ariaLabel?: string;
  onBack: () => void;
  backLabel?: string;
  toc: ReaderTocItem[];
  /** Denetimli etkin başlık; verilmezse kaydırmadan hesaplanır */
  activeId?: string;
  /** Başlığa atlama (verilmezse [data-r12-sec]/[data-sec]/[data-anchor] öğesine kaydırılır) */
  onJump?: (id: string) => void;
  /** Denetimli ilerleme (0–100); verilmezse kaydırmadan hesaplanır */
  progress?: number;
  scrollRef?: React.RefObject<HTMLDivElement | null>;
  onScroll?: () => void;
  onPointerUp?: () => void;
  onKeyUp?: () => void;
  /** Başlık alanının yerine geçer (ör. belge içi arama kutusu) */
  titleSlot?: React.ReactNode;
  /** Üst çubukta Odak'tan sonra gelen araçlar (kalem, arama …) */
  tools?: React.ReactNode;
  /** "Diğer seçenekler" menüsüne eklenecek öğeler (R12MenuItem / R12MenuGroup) */
  menu?: React.ReactNode;
  /** Geniş ekranda sağ kenar paneli (Notlarım) */
  margin?: React.ReactNode;
  marginLabel?: string;
  /** Kenar paneli sığmadığında makalenin altına konan içerik */
  after?: React.ReactNode;
  /** Yüzen öğeler (kaldığın yerden devam, başa dön …) */
  floating?: React.ReactNode;
  /** Esc okuyucuyu kapatsın mı (çağıran kendi klavye işleyicisini kuruyorsa false) */
  escToClose?: boolean;
  closing?: boolean;
  rootRef?: React.Ref<HTMLDivElement>;
  className?: string;
  /** Satır genişliği: dar 60ch · normal 68ch · geniş 78ch */
  measure?: 'narrow' | 'normal' | 'wide';
  children: React.ReactNode;
}

const PREF_KEY = 'medsoru_r12_reader';
type Pref = { toc?: boolean; focus?: boolean };
const readPref = (): Pref => {
  try {
    return JSON.parse(localStorage.getItem(PREF_KEY) || '{}') as Pref;
  } catch {
    return {};
  }
};
const writePref = (p: Pref) => {
  try {
    localStorage.setItem(PREF_KEY, JSON.stringify({ ...readPref(), ...p }));
  } catch {
    /* gizli pencere: tercih bu oturumla sınırlı */
  }
};
const reduceMotion = () =>
  typeof window !== 'undefined' &&
  (window.matchMedia?.('(prefers-reduced-motion: reduce)').matches || document.documentElement.dataset.motion === 'reduced');

/** Yazı boyutu ve okuma yazı tipi (üst çubukta ve dar ekranda menüde aynı denetim) */
const TypeControls: React.FC<{ inMenu?: boolean }> = ({ inMenu }) => {
  const look = useAppearance();
  const px = look.textPx;
  return (
    <div className={inMenu ? 'r12-menu-type' : 'r12-type'}>
      <div className="r12-size" role="group" aria-label="Yazı boyutu">
        <button type="button" onClick={() => look.set({ textPx: px - 1 })} disabled={px <= TEXT_PX_MIN} aria-label="Yazıyı küçült">
          A−
        </button>
        <span aria-live="polite" aria-label={`Yazı boyutu ${px + 1} piksel`}>
          {px + 1}
        </span>
        <button type="button" onClick={() => look.set({ textPx: px + 1 })} disabled={px >= TEXT_PX_MAX} aria-label="Yazıyı büyüt">
          A+
        </button>
      </div>
      <div className="r12-seg" role="radiogroup" aria-label="Okuma yazı tipi">
        <button type="button" role="radio" aria-checked={look.reading === 'serif'} className={look.reading === 'serif' ? 'is-on' : ''} onClick={() => look.set({ reading: 'serif' })}>
          Tırnaklı
        </button>
        <button type="button" role="radio" aria-checked={look.reading === 'sans'} className={look.reading === 'sans' ? 'is-on' : ''} onClick={() => look.set({ reading: 'sans' })}>
          Düz
        </button>
      </div>
    </div>
  );
};

// ── Menü parçaları ────────────────────────────────────────────────────────────────────────────────
export const R12MenuGroup: React.FC<{ label?: string; children: React.ReactNode }> = ({ label, children }) => (
  <div className="r12-menu-group" role="group" aria-label={label}>
    {label && <span className="r12-menu-label">{label}</span>}
    {children}
  </div>
);

export const R12MenuItem: React.FC<{
  icon?: React.ElementType;
  label: React.ReactNode;
  hint?: React.ReactNode;
  onClick?: () => void;
  href?: string;
  /** Aç/kapa öğesi: aria-checked ile anahtar görünümü */
  checked?: boolean;
  danger?: boolean;
  disabled?: boolean;
  /** Tıklanınca menü açık kalsın (aç/kapa öğeleri) */
  keepOpen?: boolean;
}> = ({ icon: Icon, label, hint, onClick, href, checked, danger, disabled, keepOpen }) => {
  const cls = `r12-menu-item ${danger ? 'is-danger' : ''}`;
  const body = (
    <>
      {Icon && <Icon aria-hidden />}
      <span className="r12-menu-t">{label}</span>
      {hint != null && <small>{hint}</small>}
      {checked !== undefined && <i className={`r12-switch ${checked ? 'is-on' : ''}`} aria-hidden />}
    </>
  );
  if (href)
    return (
      <a className={cls} href={href} target="_blank" rel="noopener noreferrer" role="menuitem" data-r12-close>
        {body}
      </a>
    );
  return (
    <button
      type="button"
      className={cls}
      role={checked !== undefined ? 'menuitemcheckbox' : 'menuitem'}
      aria-checked={checked}
      onClick={onClick}
      disabled={disabled}
      data-r12-close={keepOpen || checked !== undefined ? undefined : ''}
    >
      {body}
    </button>
  );
};

/** Menüde tek seçimli küçük segment (tema, satır genişliği) */
export function R12MenuSeg<T extends string>({ label, value, options, onChange }: { label: string; value: T; options: { id: T; label: string }[]; onChange: (v: T) => void }) {
  return (
    <div className="r12-menu-seg">
      <span className="r12-menu-label">{label}</span>
      <div className="r12-seg is-full" role="radiogroup" aria-label={label}>
        {options.map((o) => (
          <button key={o.id} type="button" role="radio" aria-checked={value === o.id} className={value === o.id ? 'is-on' : ''} onClick={() => onChange(o.id)}>
            {o.label}
          </button>
        ))}
      </div>
    </div>
  );
}

// ── Çerçeve ───────────────────────────────────────────────────────────────────────────────────────
export const ReaderV12: React.FC<ReaderV12Props> = ({
  title,
  meta,
  ariaLabel,
  onBack,
  backLabel = 'Geri dön',
  toc,
  activeId: activeIdProp,
  onJump,
  progress: progressProp,
  scrollRef: scrollRefProp,
  onScroll,
  onPointerUp,
  onKeyUp,
  titleSlot,
  tools,
  menu,
  margin,
  marginLabel = 'Notlarım',
  after,
  floating,
  escToClose = true,
  closing,
  rootRef,
  className = '',
  measure = 'normal',
  children,
}) => {
  const ownScroll = useRef<HTMLDivElement>(null);
  const scrollRef = scrollRefProp || ownScroll;
  const frameRef = useRef<HTMLDivElement | null>(null);
  const moreRef = useRef<HTMLButtonElement>(null);
  const popRef = useRef<HTMLDivElement>(null);

  const [width, setWidth] = useState(() => (typeof window !== 'undefined' ? window.innerWidth : 1280));
  const wide = width >= 900;
  const roomy = width >= 1240;
  const narrow = width < 640;
  const [tocPref, setTocPref] = useState<boolean>(() => readPref().toc !== false);
  const [tocPop, setTocPop] = useState(false);
  const [focusPref, setFocus] = useState<boolean>(() => readPref().focus === true);
  const [isFs, setIsFs] = useState(false);
  const [immersive, setImmersive] = useState(false);
  const fsOn = isFs || immersive;
  // Telefonda kenar paneli/ray zaten yok: Odak düğmesi gizlenir ve kayıtlı Odak tercihi içindekileri kilitlemez
  const focus = (focusPref && !narrow) || fsOn;
  const [menuOpen, setMenuOpen] = useState(false);
  const [ownProgress, setOwnProgress] = useState(0);
  const [ownActive, setOwnActive] = useState('');
  const progress = progressProp ?? ownProgress;
  const activeId = activeIdProp ?? ownActive;
  const tocOpen = !focus && (wide ? tocPref : tocPop);
  const showMargin = !!margin && roomy && !focus;

  const hadNativeFsRef = useRef(false);
  useEffect(() => {
    const on = () => {
      const d = document as any;
      const f = !!(d.fullscreenElement || d.webkitFullscreenElement || d.webkitCurrentFullScreenElement);
      setIsFs(f);
      if (f) {
        hadNativeFsRef.current = true;
        setImmersive(false);
      } else if (hadNativeFsRef.current) {
        hadNativeFsRef.current = false;
        if (detectIosDevice() || wasRecentlyScrollingOrTouching()) {
          setImmersive(true);
        }
      }
    };
    document.addEventListener('fullscreenchange', on);
    document.addEventListener('webkitfullscreenchange', on);
    return () => {
      document.removeEventListener('fullscreenchange', on);
      document.removeEventListener('webkitfullscreenchange', on);
    };
  }, []);

  const toggleFs = () => {
    setMenuOpen(false);
    const d = document as any;
    if (immersive) {
      setImmersive(false);
      if (d.fullscreenElement || d.webkitFullscreenElement || d.webkitCurrentFullScreenElement) {
        hadNativeFsRef.current = false;
        (d.exitFullscreen || d.webkitExitFullscreen || d.webkitCancelFullScreen)?.call(d)?.catch?.(() => {});
      }
      return;
    }
    if (d.fullscreenElement || d.webkitFullscreenElement || d.webkitCurrentFullScreenElement) {
      hadNativeFsRef.current = false;
      (d.exitFullscreen || d.webkitExitFullscreen || d.webkitCancelFullScreen)?.call(d)?.catch?.(() => {});
      return;
    }
    const el: any = document.documentElement;
    const req = !detectIosDevice() && (el.requestFullscreen || el.webkitRequestFullscreen || el.webkitRequestFullScreen);
    if (!req) {
      setImmersive(true);
      const isStandalone = window.matchMedia?.('(display-mode: standalone)').matches || (navigator as any).standalone === true;
      if (detectIosDevice() && !isStandalone) {
        toast.info(
          'Tam ekran okuma modu açıldı',
          'Adres çubuğunu da tamamen gizlemek için uygulamayı Ana Ekrana ekleyebilirsin.',
          { label: 'Nasıl eklenir?', onClick: () => openPwaInstallGuide() }
        );
      }
      return;
    }
    let settled = false;
    try {
      const p = req.call(el, { navigationUI: 'hide' });
      p?.then?.(() => (settled = true), () => {
        settled = true;
        setImmersive(true);
      });
    } catch {
      try {
        const p2 = req.call(el);
        p2?.then?.(() => (settled = true), () => {
          settled = true;
          setImmersive(true);
        });
      } catch {
        setImmersive(true);
        return;
      }
    }
    window.setTimeout(() => {
      if (!settled && !d.fullscreenElement && !d.webkitFullscreenElement && !d.webkitCurrentFullScreenElement) setImmersive(true);
    }, 800);
  };

  useLayoutEffect(() => {
    lockScroll();
    return unlockScroll;
  }, []);

  // Kap genişliği (kenar menü açıkken görünüm genişliğinden dar): içindekiler/kenar paneli kararları buna göre
  useLayoutEffect(() => {
    const el = frameRef.current;
    if (!el) return;
    setWidth(el.clientWidth);
    if (typeof ResizeObserver === 'undefined') return;
    const ro = new ResizeObserver(([e]) => setWidth(Math.round(e.contentRect.width)));
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  const setRefs = useCallback(
    (node: HTMLDivElement | null) => {
      frameRef.current = node;
      if (typeof rootRef === 'function') rootRef(node);
      else if (rootRef && typeof rootRef === 'object') (rootRef as React.MutableRefObject<HTMLDivElement | null>).current = node;
    },
    [rootRef]
  );

  // Kendi ilerleme / etkin bölüm hesabı (denetimli değilse)
  const raf = useRef(0);
  const handleScroll = () => {
    onScroll?.();
    if (progressProp !== undefined && activeIdProp !== undefined) return;
    if (raf.current) return;
    raf.current = requestAnimationFrame(() => {
      raf.current = 0;
      const el = scrollRef.current;
      if (!el) return;
      const max = el.scrollHeight - el.clientHeight;
      setOwnProgress(max > 0 ? Math.min(100, Math.max(0, (el.scrollTop / max) * 100)) : 0);
      const top = el.getBoundingClientRect().top + 96;
      let cur = '';
      el.querySelectorAll<HTMLElement>('[data-r12-sec]').forEach((h) => {
        if (h.getBoundingClientRect().top <= top) cur = h.dataset.r12Sec || '';
      });
      setOwnActive(cur);
    });
  };
  useEffect(() => () => cancelAnimationFrame(raf.current), []);

  const jump = (id: string) => {
    setTocPop(false);
    if (onJump) return onJump(id);
    const esc = typeof CSS !== 'undefined' && CSS.escape ? CSS.escape(id) : id;
    const el = scrollRef.current?.querySelector<HTMLElement>(`[data-r12-sec="${esc}"], [data-sec="${esc}"], [data-anchor="${esc}"]`);
    el?.scrollIntoView({ behavior: reduceMotion() ? 'auto' : 'smooth', block: 'start' });
  };

  const toggleToc = () => {
    if (wide) {
      setTocPref((v) => {
        writePref({ toc: !v });
        return !v;
      });
    } else setTocPop((v) => !v);
  };
  const toggleFocus = () =>
    setFocus((v) => {
      writePref({ focus: !v });
      if (!v) setTocPop(false);
      return !v;
    });

  // Klavye: Esc önce açık katmanı, sonra okuyucuyu kapatır
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key !== 'Escape' || e.defaultPrevented) return;
      if (menuOpen) {
        setMenuOpen(false);
        moreRef.current?.focus();
        e.stopImmediatePropagation();
        return;
      }
      if (tocPop) {
        setTocPop(false);
        e.stopImmediatePropagation();
        return;
      }
      if (immersive) {
        setImmersive(false);
        e.stopImmediatePropagation();
        return;
      }
      // Üstte onay penceresi / alt sayfa varsa Esc onundur
      if (document.querySelector('.cf-root, .sh-sheet-root')) return;
      if (escToClose && !document.fullscreenElement) onBack();
    };
    // Yakalama evresi: çağıranın (özet okuyucusu) Esc işleyicisinden önce katmanları kapatır
    window.addEventListener('keydown', onKey, true);
    return () => window.removeEventListener('keydown', onKey, true);
  }, [menuOpen, tocPop, immersive, escToClose, onBack]);

  /** Menüdeki görünür, etkin öğeler (dar ekran bölümü geniş ekranda gizlidir) */
  const menuItems = () =>
    Array.from(popRef.current?.querySelectorAll<HTMLElement>('button:not(:disabled), a[href]') || []).filter((el) => el.offsetParent !== null);

  // Menü açılınca ilk öğeye odak
  useEffect(() => {
    if (!menuOpen) return;
    menuItems()[0]?.focus();
  }, [menuOpen]);

  const onMenuClick = (e: React.MouseEvent) => {
    if ((e.target as HTMLElement).closest('[data-r12-close]')) setMenuOpen(false);
  };
  const onMenuKey = (e: React.KeyboardEvent) => {
    if (e.key !== 'ArrowDown' && e.key !== 'ArrowUp') return;
    const items = menuItems();
    const i = items.indexOf(document.activeElement as HTMLElement);
    const next = items[(i + (e.key === 'ArrowDown' ? 1 : -1) + items.length) % items.length];
    next?.focus();
    e.preventDefault();
  };

  const pct = Math.round(progress);

  const Toc = (
    <nav id="r12-toc" className={`r12-toc ${wide ? 'is-rail' : 'is-pop'}`} aria-label="İçindekiler">
      <div className="r12-toc-h">
        <span>İçindekiler</span>
        <button type="button" className="r12-ib is-sm" onClick={toggleToc} aria-label="İçindekileri kapat">
          <ChevronLeft aria-hidden />
        </button>
      </div>
      {toc.length === 0 ? (
        <p className="r12-toc-empty">Bu metinde başlık yok.</p>
      ) : (
        <ol className="r12-toc-list">
          {toc.map((t) => {
            const on = t.id === activeId;
            return (
              <li key={t.id}>
                <a
                  href={`#${t.id}`}
                  className={`${t.level === 3 ? 'is-h3' : ''} ${on ? 'is-on' : ''}`}
                  aria-current={on ? 'location' : undefined}
                  onClick={(e) => {
                    e.preventDefault();
                    jump(t.id);
                  }}
                >
                  <span>{t.title}</span>
                  {t.count ? <small>{t.count}</small> : null}
                </a>
              </li>
            );
          })}
        </ol>
      )}
    </nav>
  );

  return (
    <div
      ref={setRefs}
      className={`r12-root ${focus ? 'is-focus' : ''} ${immersive ? 'is-immersive' : ''} ${closing ? 'is-closing' : ''} ${className}`}
      role="dialog"
      aria-modal="true"
      aria-label={ariaLabel || title}
    >
      {immersive && (
        <button type="button" className="r12-exit-fs" onClick={() => setImmersive(false)} aria-label="Tam ekrandan çık" title="Tam ekrandan çık (Esc)">
          <Minimize2 aria-hidden />
          <span>Küçült</span>
        </button>
      )}
      <header className="r12-top">
        <button type="button" className="r12-ib" onClick={onBack} aria-label={backLabel} title={`${backLabel} (Esc)`}>
          <ChevronLeft aria-hidden />
        </button>
        {titleSlot || (
          <div className="r12-title">
            <b>{title}</b>
            {meta && <span>{meta}</span>}
          </div>
        )}
        <div className="r12-tools">
          <TypeControls />
          {!narrow && (
            <button type="button" className={`r12-tbtn ${focusPref ? 'is-on' : ''}`} aria-pressed={focusPref} onClick={toggleFocus} title="Odak: içindekiler ve paneller kapanır">
              <Focus aria-hidden />
              <span>{focusPref ? 'Odak açık' : 'Odak'}</span>
            </button>
          )}
          <button
            type="button"
            className={`r12-ib ${fsOn ? 'is-on' : ''}`}
            aria-pressed={fsOn}
            onClick={toggleFs}
            aria-label={fsOn ? 'Tam ekrandan çık' : 'Tam ekran okuma'}
            title={fsOn ? 'Tam ekrandan çık (Esc)' : 'Tam ekran okuma'}
          >
            {fsOn ? <Minimize2 aria-hidden /> : <Maximize2 aria-hidden />}
          </button>
          {!focus && (
            <button type="button" className={`r12-tbtn ${tocOpen ? 'is-on' : ''}`} aria-pressed={tocOpen} aria-controls="r12-toc" aria-expanded={tocOpen} onClick={toggleToc}>
              <AlignLeft aria-hidden />
              <span>İçindekiler</span>
            </button>
          )}
          {tools}
          <div className="r12-more">
            <button
              ref={moreRef}
              type="button"
              className={`r12-ib ${menuOpen ? 'is-on' : ''}`}
              aria-label="Diğer seçenekler"
              aria-haspopup="menu"
              aria-expanded={menuOpen}
              onClick={() => setMenuOpen((v) => !v)}
            >
              <MoreVertical aria-hidden />
            </button>
            {menuOpen && (
              <>
                <button type="button" className="r12-scrim" aria-label="Menüyü kapat" tabIndex={-1} onClick={() => setMenuOpen(false)} />
                <div ref={popRef} className="r12-menu" role="menu" aria-label="Diğer seçenekler" onClick={onMenuClick} onKeyDown={onMenuKey}>
                  <div className="r12-menu-narrow">
                    <R12MenuGroup label="Görünüm">
                      <TypeControls inMenu />
                      <R12MenuItem
                        icon={fsOn ? Minimize2 : Maximize2}
                        label={fsOn ? 'Tam ekrandan çık' : 'Tam ekran okuma'}
                        onClick={toggleFs}
                      />
                    </R12MenuGroup>
                  </div>
                  {menu}
                </div>
              </>
            )}
          </div>
        </div>
      </header>
      <div className="r12-progress" role="progressbar" aria-label="Okuma ilerlemesi" aria-valuemin={0} aria-valuemax={100} aria-valuenow={pct}>
        <i style={{ transform: `scaleX(${progress / 100})` }} />
      </div>

      {tocOpen && !wide && (
        <div className="r12-popwrap">
          <button type="button" className="r12-scrim" aria-label="İçindekileri kapat" tabIndex={-1} onClick={() => setTocPop(false)} />
          {Toc}
        </div>
      )}

      <div ref={scrollRef} className="r12-scroll" onScroll={handleScroll} onPointerUp={onPointerUp} onKeyUp={onKeyUp}>
        <div className="r12-body">
          {tocOpen && wide && Toc}
          <div className="r12-center">
            <div className={`r12-col m-${measure}`}>
              <div className="r12-article">{children}</div>
              {!showMargin && after && <div className="r12-after">{after}</div>}
            </div>
          </div>
          {showMargin && (
            <aside className="r12-margin" aria-label={marginLabel}>
              {margin}
            </aside>
          )}
        </div>
      </div>
      {floating}
    </div>
  );
};

/** Kalem işaretine kaydırır (Notlarım panelinden): kayıtlı metin konumu, kaymışsa ifadenin kendisi aranır. */
export function scrollToMark(root: HTMLElement | null | undefined, m: { start: number; end: number; text: string }) {
  if (!root) return;
  const text = root.textContent || '';
  let at = text.slice(m.start, m.end) === m.text ? m.start : text.indexOf(m.text);
  if (at < 0) at = m.start;
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  let pos = 0;
  let node: Node | null;
  while ((node = walker.nextNode())) {
    const len = node.textContent?.length || 0;
    if (pos + len > at) {
      node.parentElement?.scrollIntoView({ behavior: reduceMotion() ? 'auto' : 'smooth', block: 'center' });
      return;
    }
    pos += len;
  }
}

/** Okuyucu altındaki "sıradaki" bağlantısı gibi satır düğmesi (liste satırlarıyla aynı dil) */
export const R12NextRow: React.FC<{ label: string; title: string; meta?: React.ReactNode; onClick: () => void }> = ({ label, title, meta, onClick }) => (
  <button type="button" className="r12-next" onClick={onClick}>
    <span>
      <small>{label}</small>
      <b>{title}</b>
      {meta && <em>{meta}</em>}
    </span>
    <ChevronRight aria-hidden />
  </button>
);
