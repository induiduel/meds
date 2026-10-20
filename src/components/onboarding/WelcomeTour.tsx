import React, { useCallback, useEffect, useLayoutEffect, useRef, useState } from 'react';
import { ArrowRight, Check, ChevronLeft, ChevronRight, Sparkles, X } from 'lucide-react';
import { ROUTE_PATHS, type AppRoute } from '../../router';
import { NAV_ITEMS } from '../shell/navModel';
import { markTourSeen as markSeen } from './tourState';
import { useAppearance } from '../../utils/appearance';
import { TourCardV12, WelcomeFullV12 } from '../v12/OnboardingV12';
import { groupOf } from '../v13/navGroups';
import './welcome-tour.css';

/* ------------------------------------------------------------------
 * Hoş geldin turu: kayıt/girişten sonra bir kez açılır.
 *   1) Karşılama: MeDSor nedir, üç ayak (öğren · soru çöz · birlikte kur).
 *   2) Rehberli tur: gerçek menü öğeleri sırayla vurgulanır (kenar menüsü ya da alt gezinme),
 *      her durakta sayfanın ne işe yaradığı ve neler yapılabileceği anlatılır.
 *   3) Bitiş: "Nereden başlamak istersin?" → seçilen sayfa açılır.
 * Durum profilde tutulur (`medsoru_tour_v1`, userKvSync), başka cihazda tekrar açılmaz.
 * Ayarlar › Hesap ve veri › "Tanıtım turu" ya da `medsoru:tour` olayı yeniden başlatır.
 * ------------------------------------------------------------------ */

type Stop = {
  route: AppRoute;
  /** Kenar menüsünde (≥768px) hedef */
  side: string;
  /** Alt gezinmede (<768px) hedef; yoksa "Daha" düğmesi */
  tab?: string;
  eyebrow: string;
  title: string;
  text: string;
  points: string[];
  /** Telefonda hedef "Daha" düğmesiyse gösterilecek not */
  moreNote?: string;
};

const href = (r: AppRoute) => `a[href="${ROUTE_PATHS[r]}"]`;

const MORE_BTN = '.sh-tabs button[aria-haspopup="dialog"], .s12-tabs button[aria-haspopup="dialog"], .a13-island button[aria-haspopup="dialog"]';
/** "Daha" sayfasındaki satır (telefon): tur sayfayı açar, satırı vurgular */
const moreRow = (r: AppRoute) => `.sh-more a[href="${ROUTE_PATHS[r]}"], .s12-more a[href="${ROUTE_PATHS[r]}"], .a13-menu a[href="${ROUTE_PATHS[r]}"]`;
const setMoreSheet = (open: boolean) => window.dispatchEvent(new CustomEvent('medsoru:more', { detail: { open } }));

const STOPS: Stop[] = [
  {
    route: 'search',
    side: '.sh-side-search, .s12-rail-search',
    tab: '.sh-top-search-i, .sh-top-search, .s12-top-tools [aria-label*="Ara"]',
    eyebrow: 'Her yerden',
    title: 'Tek kutudan ara',
    text: 'Bir terim, hastalık ya da soru parçası yaz; bütün veri setleri birlikte taranır.',
    points: ['Çıkmış sorular, soru havuzu, ders notları ve sözlük aynı listede', 'Klavyede / ya da Ctrl+K ile anında açılır'],
  },
  {
    route: 'quick_add',
    side: '.sh-side-add, .s12-add',
    tab: '.sh-tab-fab, .s12-tab-plus',
    eyebrow: 'Birlikte kur',
    title: 'Sınavdan hatırladığını ekle',
    text: 'Aklında kalan birkaç kelime yeter. Yazdıkça ders slaytları ve çıkmışlar taranır, en yakın eşleşmeler önüne gelir.',
    points: [
      'Havuzda aynı soru varsa ona bağlanır, parçalar birleşir',
      'Yoksa yeni soru açılır; şıkları başkaları tamamlar',
      'Katkın adınla görünür, sıralamaya yazılır',
    ],
  },
  {
    route: 'today',
    side: `.sh-side ${href('today')}, .s12-rail ${href('today')}`,
    eyebrow: 'Günlük',
    title: 'Bugün',
    text: 'Her gün buradan başla: kaldığın ders, günün sınav spotu ve haftalık çalışma süren tek ekranda.',
    points: ['Yarım kalan desteye tek dokunuşla dön', 'Haftanın çalışma ritmini gör'],
    moreNote: 'Telefonda “Daha” menüsünün en üstünde.',
  },
  {
    route: 'learn',
    side: `.sh-side ${href('learn')}, .s12-rail ${href('learn')}`,
    tab: `.sh-tabs ${href('learn')}, .s12-tabs ${href('learn')}`,
    eyebrow: 'Öğren',
    title: 'İnteraktif ders desteleri',
    text: 'Her ders, amfi slaytlarından kurulmuş adım adım bir anlatımdır. Okurken küçük etkileşimlerle bilgiyi sınarsın.',
    points: [
      'Mini sorular, boşluk doldurma, mekanizma zincirleri, karşılaştırma tabloları',
      'Dersin orijinal PDF’i yanında açılır',
      'Terimlerin üstüne dokununca kısa tanımı görünür; ilerlemen kaydedilir',
    ],
  },
  {
    route: 'spots',
    side: `.sh-side ${href('spots')}, .s12-rail ${href('spots')}`,
    eyebrow: 'Hızlı tekrar',
    title: 'Spotlar, kartlar, özetler',
    text: 'Sınava yakın dönemde kısa tekrar için üç araç:',
    points: [
      'Sınav spotları: en sık sorulanlar, ayırıcı bulgular, tuzaklar',
      'Ezber kartları: aralıklı tekrarla unutmadan öğren',
      'Ders özetleri: dersin uzun okuması, spotlar vurgulu',
    ],
    moreNote: 'Telefonda “Daha” menüsünde, Öğren grubunda.',
  },
  {
    route: 'past_exams',
    side: `.sh-side ${href('past_exams')}, .s12-rail ${href('past_exams')}`,
    tab: `.sh-tabs ${href('past_exams')}, .s12-tabs ${href('past_exams')}`,
    eyebrow: 'Soru çöz',
    title: 'Çıkmış sorular',
    text: 'Kurullara ve derslere göre ayrılmış, cevap anahtarı doğrulanmış çıkmış sorular.',
    points: ['Her şıkkın neden doğru ya da yanlış olduğu açıklamalı', 'Hatalı gördüğün soruyu tek dokunuşla bildir'],
  },
  {
    route: 'study',
    side: `.sh-side ${href('study')}, .s12-rail ${href('study')}`,
    eyebrow: 'Soru çöz',
    title: 'Çalış ve test çöz',
    text: 'Kendini sınamak için: kurul seç, soru çöz, yanlışlarını tekrar et.',
    points: [
      'Test çöz: süreli deneme sınavı',
      'Örnek sorular: kazanımlara göre yazılmış yeni sorular',
      'Yanlışların ve favorilerin ayrı listede birikir',
    ],
    moreNote: 'Telefonda “Daha” menüsünde, Soru çöz grubunda.',
  },
  {
    route: 'glossary',
    side: `.sh-side ${href('glossary')}, .s12-rail ${href('glossary')}`,
    eyebrow: 'Başvuru',
    title: 'Sözlük, hastalıklar, kazanımlar',
    text: 'Takıldığın bir kavrama bakmak için başvuru kaynakları.',
    points: [
      'Sözlük: hastalık ve ilaç bilgi kartları',
      'Hastalıklar: klinik atlas',
      'Kazanımlar: müfredatta hangi dersten ne bekleniyor',
    ],
    moreNote: 'Telefonda “Daha” menüsünde, Başvuru grubunda.',
  },
  {
    route: 'questions',
    side: `.sh-side ${href('questions')}, .s12-rail ${href('questions')}`,
    tab: `.sh-tabs ${href('questions')}, .s12-tabs ${href('questions')}`,
    eyebrow: 'Topluluk',
    title: 'Soru havuzu',
    text: 'Son kurulda sorulan soruların herkesin katkısıyla yeniden kurulduğu yer.',
    points: [
      'Eksik şıkları ve cevabı tamamla, cevap oylamasına katıl',
      'Soru haritası 1–100 arası hangi soruların bulunduğunu gösterir',
      'Sıralama en çok katkı verenleri listeler',
    ],
  },
  {
    route: 'settings',
    side: '.sh-side-user, .s12-me, .s12-rail .s12-av',
    tab: '.sh-acct-btn, .s12-acct-anchor button',
    eyebrow: 'Senin alanın',
    title: 'Profil ve ayarlar',
    text: 'Uygulamayı kendine göre ayarla. Yaptığın her şey profiline kaydedilir; başka cihazda giriş yapınca kaldığın yerden devam edersin.',
    points: [
      'Tema, renk paleti, yazı yoğunluğu, görüntüleme modu',
      'Soruları cihaza indirip internetsiz çalış',
      'Bu turu buradan yeniden başlatabilirsin',
    ],
  },
];

const PILLARS = [
  { route: 'learn' as AppRoute, title: 'Öğren', text: 'Amfi slaytlarından kurulmuş interaktif dersler, spotlar ve kartlar' },
  { route: 'past_exams' as AppRoute, title: 'Soru çöz', text: 'Doğrulanmış çıkmışlar, örnek sorular ve süreli testler' },
  { route: 'questions' as AppRoute, title: 'Birlikte kur', text: 'Sınavdan hatırladıklarını ekle, sorular birlikte tamamlansın' },
];

const STARTS: { route: AppRoute; text: string }[] = [
  { route: 'today', text: 'Günün özeti ve kaldığın yer' },
  { route: 'learn', text: 'Bir ders destesi aç' },
  { route: 'past_exams', text: 'Çıkmışlarla kendini sına' },
  { route: 'quick_add', text: 'Hatırladığın soruyu yaz' },
];

/** v13 "Ada" kabuğu: sayfalar öbeklerde. Seçiciler sırayla denenir (önce açık paneldeki satır, sonra öbek düğmesi). */
const isV13 = () => document.documentElement.dataset.v13 === 'on';
const V13_SIDE: Partial<Record<AppRoute, string[]>> = {
  search: ['.a13-side .a13-sbtn[aria-label^="Ara"]'],
  quick_add: ['.a13-side .a13-add'],
  settings: ['.a13-side .a13-me'],
};
const V13_TAB: Partial<Record<AppRoute, string[]>> = {
  search: ['.a13-top .a13-find'],
  quick_add: ['.a13-island .a13-tab-add'],
  settings: [],
};
const v13Side = (r: AppRoute) => {
  const g = groupOf(r);
  return V13_SIDE[r] || [`.a13-side .a13-panel ${href(r)}`, ...(g ? [`.a13-side .a13-groups [data-g="${g.id}"]`] : [])];
};
/** Telefonda yalnız alt adadaki öbekler doğrudan hedeflenir; diğerleri Menü sayfasından (moreRow) */
const v13Tab = (r: AppRoute) => {
  const g = groupOf(r);
  return V13_TAB[r] || (g ? [`.a13-island [data-g="${g.id}"]`] : []);
};

const visible = (el: Element | null): el is HTMLElement => {
  if (!(el instanceof HTMLElement)) return false;
  const r = el.getBoundingClientRect();
  if (r.width < 4 || r.height < 4) return false;
  const cs = getComputedStyle(el);
  return cs.visibility !== 'hidden' && cs.display !== 'none' && Number(cs.opacity) > 0.05;
};
const firstVisible = (sel?: string | string[]) => {
  if (!sel) return null;
  for (const one of Array.isArray(sel) ? sel : [sel])
    for (const el of Array.from(document.querySelectorAll(one))) if (visible(el)) return el;
  return null;
};
const moreNoteOf = (s: Stop) => {
  if (!isV13()) return s.moreNote;
  const g = groupOf(s.route);
  return g ? `Telefonda “Menü” sayfasında, ${g.label} bölümünde.` : 'Telefonda “Menü” sayfasında.';
};
const sideSel = (s: Stop) => (isV13() ? v13Side(s.route) : s.side);
const tabSel = (s: Stop) => (isV13() ? v13Tab(s.route) : s.tab);

type Rect = { top: number; left: number; width: number; height: number };
/** Karartma katmanındaki deliğin yolu (kenar yarıçaplı dikdörtgen); büyük box-shadow yayılımı bazı GPU'larda kırpılıyordu */
const roundRect = ({ top: y, left: x, width: w, height: h }: Rect, r: number) => {
  const k = Math.min(r, w / 2, h / 2);
  return `M${x + k} ${y}H${x + w - k}A${k} ${k} 0 0 1 ${x + w} ${y + k}V${y + h - k}A${k} ${k} 0 0 1 ${x + w - k} ${y + h}H${x + k}A${k} ${k} 0 0 1 ${x} ${y + h - k}V${y + k}A${k} ${k} 0 0 1 ${x + k} ${y}Z`;
};
type Phase = 'intro' | 'tour' | 'finish';

const PillarIcon: React.FC<{ route: AppRoute; size?: number }> = ({ route, size = 40 }) => {
  const it = NAV_ITEMS[route];
  const Icon = it.icon;
  return (
    <span className="wt-ico" style={{ '--ico-bg': it.tint, '--ico-s': `${size}px` } as React.CSSProperties} aria-hidden="true">
      <Icon strokeWidth={2.1} />
    </span>
  );
};

export const WelcomeTour: React.FC<{ name?: string | null; onGo: (r: AppRoute) => void; onClose: () => void }> = ({ name, onGo, onClose }) => {
  const [phase, setPhase] = useState<Phase>('intro');
  const [i, setI] = useState(0);
  const [hole, setHole] = useState<Rect | null>(null);
  const [viaMore, setViaMore] = useState(false);
  const [pos, setPos] = useState<{ top: number; left: number; place: 'right' | 'above' | 'below' | 'center' }>({ top: 0, left: 0, place: 'center' });
  const cardRef = useRef<HTMLDivElement>(null);
  const v12 = useAppearance().design === 'v12';
  const stop = STOPS[i];
  const first = (name || '').trim().split(/\s+/)[0];

  const finish = useCallback(
    (how: 'done' | 'skipped', go?: AppRoute) => {
      markSeen(how);
      onClose();
      if (go) onGo(go);
    },
    [onClose, onGo]
  );

  // Hedefi bul, vurgu deliğini ve kartın yerini hesapla
  const measure = useCallback(() => {
    if (phase !== 'tour') return;
    const phone = window.innerWidth < 768;
    let el = phone ? firstVisible(tabSel(stop)) : firstVisible(sideSel(stop));
    let more = false;
    if (!el && phone) {
      // Sayfa "Daha" menüsünde: menü açık ve satır çizildiyse satırı, değilse (açılış animasyonu) şimdilik düğmeyi vurgula
      const row = document.querySelector<HTMLElement>(moreRow(stop.route));
      if (row && visible(row)) {
        const r0 = row.getBoundingClientRect();
        if (r0.top < 80 || r0.bottom > window.innerHeight - 200) row.scrollIntoView({ block: 'center' });
        el = row;
      } else el = firstVisible(MORE_BTN);
      more = !!el;
    }
    if (!el && !phone) el = firstVisible(tabSel(stop)); // akış/odak modunda kenar menüsü şeritte olabilir
    setViaMore(more);
    if (!el) {
      setHole(null);
      setPos({ top: 0, left: 0, place: 'center' });
      return;
    }
    const r = el.getBoundingClientRect();
    const pad = 6;
    const h = { top: r.top - pad, left: r.left - pad, width: r.width + pad * 2, height: r.height + pad * 2 };
    setHole(h);
    const vw = window.innerWidth;
    const vh = window.innerHeight;
    const cw = Math.min(360, vw - 32);
    const ch = cardRef.current?.offsetHeight || 280;
    const gap = 14;
    if (h.left + h.width + gap + cw + 16 <= vw && h.left < vw * 0.4) {
      // kenar menüsü: sağına
      const top = Math.max(16, Math.min(vh - ch - 16, h.top + h.height / 2 - ch / 2));
      setPos({ top, left: h.left + h.width + gap, place: 'right' });
      return;
    }
    const left = Math.max(16, Math.min(vw - cw - 16, h.left + h.width / 2 - cw / 2));
    if (h.top + h.height / 2 > vh / 2) setPos({ top: Math.max(16, h.top - gap - ch), left, place: 'above' });
    else setPos({ top: Math.min(vh - ch - 16, h.top + h.height + gap), left, place: 'below' });
  }, [phase, stop]);

  // Telefonda hedefi alt sekmelerde olmayan duraklar için "Daha" sayfasını aç; diğerlerinde ve tur bitince kapat
  const needMore = phase === 'tour' && !firstVisible(tabSel(stop)) && typeof window !== 'undefined' && window.innerWidth < 768;
  useEffect(() => {
    setMoreSheet(needMore);
    if (!needMore) return;
    // Sayfa kayarak açılır: animasyon boyunca (≈1 sn) her karede yeniden ölç
    const t0 = performance.now();
    let raf = 0;
    const loop = () => { measure(); if (performance.now() - t0 < 1100) raf = requestAnimationFrame(loop); };
    raf = requestAnimationFrame(loop);
    // Sekme arka plandayken kare döngüsü durur: zamanlayıcı yedeği ve animasyon bitişi
    const ts = [350, 700, 1150].map((ms) => window.setTimeout(measure, ms));
    const onEnd = () => measure();
    document.addEventListener('transitionend', onEnd, true);
    document.addEventListener('animationend', onEnd, true);
    return () => {
      cancelAnimationFrame(raf);
      ts.forEach(window.clearTimeout);
      document.removeEventListener('transitionend', onEnd, true);
      document.removeEventListener('animationend', onEnd, true);
    };
  }, [needMore, i, measure]);
  useEffect(() => () => { setMoreSheet(false); }, []);

  useLayoutEffect(() => {
    measure();
    // kart yüksekliği ilk çizimden sonra belli olur
    const raf = requestAnimationFrame(measure);
    return () => cancelAnimationFrame(raf);
  }, [measure]);

  useEffect(() => {
    if (phase !== 'tour') return;
    const on = () => measure();
    window.addEventListener('resize', on);
    window.addEventListener('scroll', on, true);
    const ro = new ResizeObserver(on);
    if (cardRef.current) ro.observe(cardRef.current);
    return () => {
      window.removeEventListener('resize', on);
      window.removeEventListener('scroll', on, true);
      ro.disconnect();
    };
  }, [phase, measure]);

  const next = () => (i < STOPS.length - 1 ? setI(i + 1) : setPhase('finish'));
  const prev = () => (i > 0 ? setI(i - 1) : setPhase('intro'));

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        e.preventDefault();
        finish('skipped');
      }
      if (phase !== 'tour') return;
      if (e.key === 'ArrowRight') next();
      if (e.key === 'ArrowLeft') prev();
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  });

  // Her adımda odak karta: ekran okuyucu yeni metni okur
  useEffect(() => {
    cardRef.current?.focus({ preventScroll: true });
  }, [phase, i]);

  if ((phase === 'intro' || phase === 'finish') && v12) {
    return (
      <WelcomeFullV12
        phase={phase}
        cardRef={cardRef}
        first={first}
        stopCount={STOPS.length}
        pillars={PILLARS}
        starts={STARTS}
        onStartTour={() => { setI(0); setPhase('tour'); }}
        onSkip={() => finish('skipped')}
        onPick={(r) => finish('done', r)}
        onBackToTour={() => { setI(STOPS.length - 1); setPhase('tour'); }}
      />
    );
  }

  if (phase === 'intro' || phase === 'finish') {
    const intro = phase === 'intro';
    return (
      <div className="wt-full" role="dialog" aria-modal="true" aria-labelledby="wt-h">
        <div className="wt-full-top">
          <span className="ms-onboard-brand">Me<span>DS</span>or</span>
          <button type="button" className="wt-x" onClick={() => finish('skipped')} aria-label="Tanıtımı kapat">
            <X />
          </button>
        </div>
        <div className="wt-full-body">
          <div ref={cardRef} tabIndex={-1} className={`wt-sheet ${intro ? '' : 'is-finish'}`} key={phase}>
            {intro ? (
              <>
                <span className="wt-badge"><Sparkles aria-hidden="true" /> Hesabın hazır</span>
                <h1 id="wt-h" className="wt-h1">{first ? `Hoş geldin, ${first}` : 'Hoş geldin'}</h1>
                <p className="wt-lead">
                  MeDSor, Dönem 3 için ders slaytlarını, doğrulanmış çıkmış soruları ve öğrencilerin hatırladıklarını tek yerde toplar.
                  Üç şey için buradasın:
                </p>
                <ul className="wt-pillars">
                  {PILLARS.map((p, n) => (
                    <li key={p.route} style={{ animationDelay: `${0.12 + n * 0.08}s` }}>
                      <PillarIcon route={p.route} />
                      <span><b>{p.title}</b><span>{p.text}</span></span>
                    </li>
                  ))}
                </ul>
                <div className="wt-actions">
                  <button type="button" className="wt-btn is-primary" onClick={() => { setI(0); setPhase('tour'); }}>
                    Kısa turu başlat <span className="wt-btn-sub">{STOPS.length} durak · 1 dk</span>
                    <ArrowRight aria-hidden="true" />
                  </button>
                  <button type="button" className="wt-btn is-ghost" onClick={() => finish('skipped')}>
                    Kendim keşfederim
                  </button>
                </div>
              </>
            ) : (
              <>
                <span className="wt-badge is-good"><Check aria-hidden="true" /> Tur bitti</span>
                <h1 id="wt-h" className="wt-h1">Nereden başlamak istersin?</h1>
                <p className="wt-lead">Seçtiğin sayfa açılır. Turu istediğin zaman Profil ve ayarlar › Hesap ve veri’den yeniden izleyebilirsin.</p>
                <div className="wt-starts">
                  {STARTS.map((s, n) => (
                    <button
                      key={s.route}
                      type="button"
                      className="wt-start"
                      style={{ animationDelay: `${0.06 + n * 0.06}s` }}
                      onClick={() => finish('done', s.route)}
                    >
                      <PillarIcon route={s.route} size={36} />
                      <span><b>{NAV_ITEMS[s.route].label}</b><span>{s.text}</span></span>
                      <ChevronRight className="wt-start-chev" aria-hidden="true" />
                    </button>
                  ))}
                </div>
                <div className="wt-actions">
                  <button type="button" className="wt-btn is-ghost" onClick={() => { setI(STOPS.length - 1); setPhase('tour'); }}>
                    <ChevronLeft aria-hidden="true" /> Tura dön
                  </button>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    );
  }

  const hasIcon = stop.route in NAV_ITEMS;
  return (
    <div className="wt-tour" role="dialog" aria-modal="true" aria-labelledby="wt-t" aria-describedby="wt-d">
      {/* Tıklama yakalayıcı: tur sırasında alttaki sayfa kullanılamaz */}
      {hole ? (
        <svg className="wt-scrim" aria-hidden="true">
          <path fillRule="evenodd" d={`M0 0H${window.innerWidth}V${window.innerHeight}H0Z ${roundRect(hole, 14)}`} />
        </svg>
      ) : (
        <div className="wt-scrim is-solid" />
      )}
      {hole && (
        <div
          className="wt-hole"
          aria-hidden="true"
          style={{ top: hole.top, left: hole.left, width: hole.width, height: hole.height }}
        />
      )}
      {v12 ? (
        <TourCardV12
          cardRef={cardRef}
          place={pos.place}
          top={pos.top}
          left={pos.left}
          index={i}
          total={STOPS.length}
          route={stop.route}
          title={stop.title}
          text={stop.text}
          points={stop.points}
          note={viaMore ? moreNoteOf(stop) : undefined}
          onPrev={prev}
          onNext={next}
          onClose={() => finish('skipped')}
        />
      ) : (
      <div
        ref={cardRef}
        tabIndex={-1}
        className={`wt-card is-${pos.place}`}
        style={pos.place === 'center' ? undefined : { top: pos.top, left: pos.left }}
      >
        <div className="wt-card-h">
          {hasIcon ? <PillarIcon route={stop.route} size={34} /> : <span className="wt-ico is-search" aria-hidden="true">/</span>}
          <span className="wt-card-eb">{stop.eyebrow}</span>
          <span className="wt-count" aria-label={`${STOPS.length} duraktan ${i + 1}.`}>{i + 1}/{STOPS.length}</span>
          <button type="button" className="wt-x is-sm" onClick={() => finish('skipped')} aria-label="Turu kapat">
            <X />
          </button>
        </div>
        <div className="wt-card-b" key={i}>
          <h2 id="wt-t" className="wt-card-t">{stop.title}</h2>
          <p id="wt-d" className="wt-card-p">{stop.text}</p>
          <ul className="wt-points">
            {stop.points.map((p) => (
              <li key={p}>{p}</li>
            ))}
          </ul>
          {viaMore && moreNoteOf(stop) && <p className="wt-more-note">{moreNoteOf(stop)}</p>}
        </div>
        <div className="wt-card-f">
          <div className="wt-prog" aria-hidden="true">
            {STOPS.map((_, n) => (
              <i key={n} className={n === i ? 'is-on' : n < i ? 'is-past' : ''} />
            ))}
          </div>
          <button type="button" className="wt-nav" onClick={prev} aria-label="Önceki">
            <ChevronLeft />
          </button>
          <button type="button" className="wt-nav is-primary" onClick={next}>
            {i === STOPS.length - 1 ? 'Bitir' : 'İleri'}
            <ChevronRight aria-hidden="true" />
          </button>
        </div>
      </div>
      )}
    </div>
  );
};

export default WelcomeTour;
