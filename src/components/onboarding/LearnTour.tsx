import React, { useCallback, useEffect, useLayoutEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import {
  AlertTriangle, BookOpenCheck, ChevronDown, ChevronLeft, ChevronRight, Compass, FileText, Filter, Flag, LayoutGrid, ListTree,
  MousePointerClick, Navigation, RotateCcw, Search, Sparkles, Wrench, X,
} from 'lucide-react';
import { IX_META } from '../learn/lesson/LessonBlocks';
import { useAppearance } from '../../utils/appearance';
import { markLearnTourSeen, type LearnTourKind } from './learnTourState';
import './welcome-tour.css';
import './learn-tour.css';

/* ------------------------------------------------------------------
 * Öğren turu — iki parça:
 *   • library: Öğren kitaplığı (ara, süzgeçler, devam et, hata defteri, ders listesi)
 *   • lesson:  ders oynatıcısı (ilerleme, slayt listesi, anlatım, Pekiştir, bilgi sekmeleri, PDF, araçlar, gezinme)
 * İkisi de "Etkileşim rehberi" ile biter: 15 etkileşim türünün ne olduğu, nasıl çözüldüğü, neyi ölçtüğü.
 * Gerçek öğe SVG maskeli karartmada delikle vurgulanır (WelcomeTour ile aynı dil, wt- sınıfları);
 * öğe yoksa (tasarım/genişlik farkı) kart ortada açılır, `optional` duraklar atlanır.
 * Durum profilde (`medsoru_learn_tour_*`, userKvSync); oynatıcı Araçlar › "Nasıl kullanılır?" yeniden açar.
 * Katman body'ye taşınır: v12'de .sh-main ölçek (zoom) katmanından etkilenmesin, oynatıcının (z 60) üstünde kalsın.
 * ------------------------------------------------------------------ */

type Stop = {
  sel: string;
  icon: React.ElementType;
  eyebrow: string;
  title: string;
  text: string;
  points: string[];
  /** Öğe sayfada yoksa durağı atla (ör. hiç ders açılmadıysa "Devam et") */
  optional?: boolean;
  /** Eşleşen tüm görünür öğeleri tek delikte birleştir (ör. durum + kurul/ders hapları) */
  union?: boolean;
};

const LIBRARY: Stop[] = [
  {
    sel: '.l12-search, [data-page-search]',
    icon: Search,
    eyebrow: 'Kitaplık',
    title: 'Ders ya da konu ara',
    text: 'Her ders, amfi slaytlarından kurulmuş adım adım bir anlatımdır. Aradığın konuyu yazman yeter.',
    points: ['Ders adı, hoca ya da konu başlığıyla bulur', 'Klavyede / tuşu kutuya atlar, Esc temizler'],
  },
  {
    sel: '.l12-seg, .l12-pills',
    union: true,
    icon: Filter,
    eyebrow: 'Süzgeçler',
    title: 'Durum, kurul ve ders',
    text: 'Listeyi daralt: başladıkların, bitirdiklerin ya da yalnız bir kurulun dersleri.',
    points: ['Devam eden / Bitti sayıları yanında görünür', 'Kurul ve Ders haplarından seç, × ile temizle', 'Sıralama: kurul sırası, son açılan ya da ada göre'],
  },
  {
    sel: '.l12-cont-list',
    icon: RotateCcw,
    eyebrow: 'Kaldığın yer',
    title: 'Devam et',
    text: 'Yarım bıraktığın dersler son açılana göre burada; dokununca kaldığın adımdan açılır.',
    points: ['Çubuk dersin ne kadarını gördüğünü gösterir', 'İlerlemen profiline kaydedilir, başka cihazda da sürer'],
    optional: true,
  },
  {
    sel: '.l12-link',
    icon: AlertTriangle,
    eyebrow: 'Tekrar',
    title: 'Hata defteri',
    text: 'Ders içindeki etkileşimlerde yanlış yaptıkların burada birikir ve aralıklı tekrarla yeniden önüne gelir.',
    points: ['“Vadesi geldi” olanları önce çöz', '“Kaynağa git” seni sorunun geçtiği adıma götürür'],
    optional: true,
  },
  {
    sel: '.l12-group, .l12-list, .l12-grid',
    icon: BookOpenCheck,
    eyebrow: 'Dersler',
    title: 'Ders listesi',
    text: 'Dersler kurullara göre gruplanır. Bir satıra dokununca ders oynatıcısı açılır.',
    points: [
      'PDF rozeti: dersin orijinal amfi slaytı',
      'Yüzde, gördüğün adım oranıdır; bitenler işaretlenir',
      'İlk açtığında ders ekranı da kısaca tanıtılır',
    ],
  },
  {
    sel: '.l12-view',
    icon: LayoutGrid,
    eyebrow: 'Görünüm',
    title: 'Liste ya da ızgara',
    text: 'Dersleri sıkı liste ya da kart ızgarası olarak gör; seçimin hatırlanır.',
    points: ['Telefonda liste, geniş ekranda ızgara daha rahat okunur'],
    optional: true,
  },
];

const LESSON: Stop[] = [
  {
    sel: '.x12-prog, .ls-segbar, .lv-bb-count',
    icon: Navigation,
    eyebrow: 'Ders oynatıcısı',
    title: 'Neredesin?',
    text: 'Ders bölümlere, bölümler adımlara ayrılır. Çubuk dersteki yerini gösterir.',
    points: ['Her adım tek bir alt konuyu anlatır, tekrar etmez', 'Gördüğün adımlar kaydedilir; çıkınca kaldığın yerden açılır'],
  },
  {
    sel: '.ls-root [aria-label="Slaytlar"], .lv-bb-count',
    icon: ListTree,
    eyebrow: 'İçindekiler',
    title: 'Slayt listesi',
    text: 'Bölümler ve adımlar katlanır bir listede. İstediğin adıma atla.',
    points: ['Bitirdiğin adımlar işaretli görünür', 'Derste ara (Ctrl+K) bir terimin geçtiği adımları bulur'],
  },
  {
    sel: '.ls-root .x12-head, .ls-root .ls-head',
    icon: FileText,
    eyebrow: 'Anlatım',
    title: 'Önce oku',
    text: 'Her adım kısa bir girişle başlar; mekanizma maddeler halinde, sınav için kritik nokta vurgu kutusunda.',
    points: [
      'Altı çizili terimlere dokununca kısa tanımı açılır',
      'Etkileşimler yalnız o adıma kadar anlatılanları sorar; ileriden soru gelmez',
      'Bir hata görürsen bayrak simgesiyle bildir',
    ],
  },
  {
    sel: '.ls-root .ls-practice, .ls-root .x12-studio-r, .ls-root .ls-B-side',
    icon: MousePointerClick,
    eyebrow: 'Pekiştir',
    title: 'Etkileşimler',
    text: 'Okuduğunu her adımda 4–6 küçük etkileşimle sınarsın: mini soru, boşluk doldurma, mekanizma zinciri, karşılaştırma…',
    points: [
      'Üstteki simgeler adımdaki etkileşimler; bitenler ✓ olur',
      'İlk seçimin cevabındır, sonra her şıkkın gerekçesi açılır',
      'Yanlışların hata defterine düşer',
    ],
  },
  {
    sel: '.ls-root .x12-nav-tabs, .ls-root .ls-dock-bar',
    icon: Flag,
    eyebrow: 'Bilgi',
    title: 'Spot, hoca notu, terimler',
    text: 'Adıma bağlı ek bilgiler sekmelerde durur; sayı rozeti içerik olduğunu gösterir.',
    points: ['Sınav spotu: çıkmışlarda sık sorulan nokta', 'Kazanımlar: müfredatın bu adımdan beklediği', 'Kaynak: adımın dayandığı amfi slaytı'],
    optional: true,
  },
  {
    sel: '.ls-root [aria-label="Ders PDF\'i"]',
    icon: BookOpenCheck,
    eyebrow: 'Kaynak',
    title: 'Dersin PDF’i',
    text: 'Orijinal amfi slaytı tek başına ya da anlatımın yanında bölünmüş ekranda açılır.',
    points: ['Adım değiştikçe PDF ilgili sayfaya gider'],
    optional: true,
  },
  {
    sel: '.ls-root .x12-tools-btn, .ls-root .ls-tools [aria-label="Araçlar"]',
    icon: Wrench,
    eyebrow: 'Araçlar',
    title: 'Çalışma araçları',
    text: 'Ders ekranını kendine göre ayarla.',
    points: [
      'Hatırlama: kalın ifadeler örtülür, dokununca açılır',
      'Marker ve kalem, Notlarım, Asistan, Sözlük',
      'Odak seansı (O) ve tam ekran (F)',
      'Bu turu buradan “Nasıl kullanılır?” ile yeniden aç',
    ],
  },
  {
    sel: '.ls-root .x12-nav, .ls-root .ls-flownav, .ls-root .lv-bottombar',
    icon: ChevronRight,
    eyebrow: 'Gezinme',
    title: 'Adım adım ilerle',
    text: 'Sonraki düğmesi bir sonraki adımın başlığını gösterir.',
    points: ['Klavyede ← → ile adım değiştir, Esc kitaplığa döner', 'Telefonda sağa-sola kaydırarak da geçebilirsin'],
  },
];

/* Etkileşim rehberi — simge ve ad oynatıcıyla aynı kaynaktan (IX_META) */
type IxGuide = { type: string; how: string; why: string; game?: boolean };
const IX_GUIDE: IxGuide[] = [
  { type: 'micro_quiz', how: '4–5 şıktan birini seç; ilk seçimin cevabındır. Sonra her şıkka dokunarak neden doğru ya da yanlış olduğunu oku.', why: 'Mekanizma ve ayırıcı tanı muhakemesi; çeldiriciler öğrendiğin komşu kavramlardan.' },
  { type: 'branching_logic', how: 'Kısa bir vaka okunur; ilk yaklaşımını seç. Her seçeneğin geri bildirimi açılır.', why: 'Bilgiyi klinik karara çevirme.' },
  { type: 'cloze_masking', how: 'Cümledeki boşluğu önce kafanda doldur, sonra dokunarak aç. İpucu cevabı ele vermez.', why: 'Anlatımdaki anahtar terimi geri çağırma.' },
  { type: 'interactive_table', how: 'Tablodaki gizli hücreleri tek tek dokunarak aç; açmadan önce tahmin et.', why: 'Değer, sınıflama ve karşılaştırma ezberini yapılandırma.' },
  { type: 'causal_chain', how: '“Sonraki basamak” ile mekanizmayı halka halka aç; her adımda bir sonrakini tahmin et. Alt halkalar ayrışan yolları gösterir.', why: 'Neden–sonuç sırasını kurma (tetikleyici → ilerleme → klinik).' },
  { type: 'before_after_slider', how: 'İki kavram yan yana; aynı satırdaki maddeler aynı ölçütü karşılaştırır.', why: 'Sık karıştırılan iki tablonun farkını görme.' },
  { type: 'active_recall', how: 'Cevabı önce kafanda kur, sonra “Cevabı göster”. Kendini Hatırlamadım / Kısmen / Tam diye puanla.', why: 'Geri çağırma; hatırlamadıkların tekrara eklenir.' },
  { type: 'spot_the_lie', how: '3–4 önermeden tam biri tuzaktır; onu bul. Her önermenin gerekçesi açılır.', why: 'Klasik sınav çeldiricisini tanıma.' },
  { type: 'swipe_matching', how: 'Kartları iki kategoriden birine at: kaydır, düğmelere ya da ← → tuşlarına bas.', why: 'Hızlı refleks ayrımı.' },
  { type: 'feature_bidding', how: 'Ortadaki özellik hangi tabloya ait? Hastalığı ve güvenini (1×–3×) seç; yanlışta çarpan kadar puan gider.', why: 'Ne kadar emin olduğunu da ölçer (metabiliş).' },
  { type: 'venn_grid', how: 'Her ölçüt için A, B, ikisi de ya da hiçbiri seç.', why: 'İki hastalığın ortak ve ayırıcı özelliklerini ayıklama.' },
  { type: 'cards', how: 'Karta dokun, arka yüzü çevrilir.', why: 'Kısa bilgi tekrarı.' },
  { type: 'sequence_order', how: 'Basamakları doğru sıraya diz.', why: 'Süreç ve evre sırası.', game: true },
  { type: 'estimate_slider', how: 'Kaydırıcıyla değeri tahmin et ve kilitle; doğru aralık bandı görünür.', why: 'Sayısal değerlerin büyüklük duygusu.', game: true },
  { type: 'perturbation', how: 'Bir değişken artarsa ya da azalırsa ötekiler ne olur? Her biri için yön seç.', why: 'Mekanizmayı ileri doğru işletme.', game: true },
  { type: 'fix_the_text', how: 'Metindeki yanlış ifadeleri bul ve düzelt.', why: 'Ayrıntıdaki hatayı yakalama.', game: true },
];

const visible = (el: Element | null): el is HTMLElement => {
  if (!(el instanceof HTMLElement)) return false;
  const r = el.getBoundingClientRect();
  if (r.width < 4 || r.height < 4) return false;
  const cs = getComputedStyle(el);
  return cs.visibility !== 'hidden' && cs.display !== 'none' && Number(cs.opacity) > 0.05;
};
const firstVisible = (sel: string) => {
  for (const el of Array.from(document.querySelectorAll(sel))) if (visible(el)) return el;
  return null;
};
/** Hedefin ekran dikdörtgeni; `union` ise görünür eşleşmelerin hepsini kapsar */
const targetRect = (stop: Stop): DOMRect | null => {
  if (!stop.union) return firstVisible(stop.sel)?.getBoundingClientRect() ?? null;
  const rs = Array.from(document.querySelectorAll(stop.sel)).filter(visible).map((e) => e.getBoundingClientRect());
  if (!rs.length) return null;
  const l = Math.min(...rs.map((r) => r.left)), t = Math.min(...rs.map((r) => r.top));
  return new DOMRect(l, t, Math.max(...rs.map((r) => r.right)) - l, Math.max(...rs.map((r) => r.bottom)) - t);
};

type Rect = { top: number; left: number; width: number; height: number };
const roundRect = ({ top: y, left: x, width: w, height: h }: Rect, r: number) => {
  const k = Math.min(r, w / 2, h / 2);
  return `M${x + k} ${y}H${x + w - k}A${k} ${k} 0 0 1 ${x + w} ${y + k}V${y + h - k}A${k} ${k} 0 0 1 ${x + w - k} ${y + h}H${x + k}A${k} ${k} 0 0 1 ${x} ${y + h - k}V${y + k}A${k} ${k} 0 0 1 ${x + k} ${y}Z`;
};

type Pos = { top: number; left: number; place: 'right' | 'left' | 'above' | 'below' | 'center' };

export const LearnTour: React.FC<{ kind: LearnTourKind; startAtCatalog?: boolean; onClose: () => void }> = ({ kind, startAtCatalog, onClose }) => {
  // Sayfada bulunmayan isteğe bağlı duraklar her çizimde ayıklanır (içerik geç yüklenebilir; sayaç doğru kalsın)
  const all = kind === 'library' ? LIBRARY : LESSON;
  const [cur, setCur] = useState(all[0].title);
  const stops = all.filter((s) => s.title === cur || !s.optional || firstVisible(s.sel));
  const [phase, setPhase] = useState<'tour' | 'catalog'>(startAtCatalog ? 'catalog' : 'tour');
  const i = Math.max(0, stops.findIndex((s) => s.title === cur));
  const setI = (n: number) => setCur(stops[n].title);
  const [open, setOpen] = useState<string | null>(null);
  const [hole, setHole] = useState<Rect | null>(null);
  const [pos, setPos] = useState<Pos>({ top: 0, left: 0, place: 'center' });
  const cardRef = useRef<HTMLDivElement>(null);
  const v12 = useAppearance().design === 'v12';
  const stop = stops[i];
  const total = stops.length;

  const finish = useCallback(
    (how: 'done' | 'skipped') => {
      markLearnTourSeen(kind, how);
      onClose();
    },
    [kind, onClose]
  );

  const measure = useCallback(() => {
    if (phase !== 'tour' || !stop) return;
    const r = targetRect(stop);
    if (!r) {
      setHole(null);
      setPos({ top: 0, left: 0, place: 'center' });
      return;
    }
    const vw = window.innerWidth;
    const vh = window.innerHeight;
    const pad = 6;
    // Çok büyük hedef (ör. Pekiştir paneli) ekrana sığacak şekilde kırpılır
    const top = Math.max(8, r.top - pad);
    const bottom = Math.min(vh - 8, r.bottom + pad);
    const h: Rect = { top, left: Math.max(8, r.left - pad), width: Math.min(vw - 16, r.width + pad * 2), height: Math.max(24, bottom - top) };
    setHole(h);
    const cw = Math.min(360, vw - 32);
    const ch = cardRef.current?.offsetHeight || 300;
    const gap = 14;
    if (h.left + h.width + gap + cw + 16 <= vw) {
      setPos({ top: Math.max(16, Math.min(vh - ch - 16, h.top + h.height / 2 - ch / 2)), left: h.left + h.width + gap, place: 'right' });
      return;
    }
    if (h.left - gap - cw >= 16) {
      setPos({ top: Math.max(16, Math.min(vh - ch - 16, h.top + h.height / 2 - ch / 2)), left: h.left - gap - cw, place: 'left' });
      return;
    }
    const left = Math.max(16, Math.min(vw - cw - 16, h.left + h.width / 2 - cw / 2));
    const spaceAbove = h.top - gap - 16;
    const spaceBelow = vh - (h.top + h.height) - gap - 16;
    if (spaceBelow >= ch) setPos({ top: h.top + h.height + gap, left, place: 'below' });
    else if (spaceAbove >= ch) setPos({ top: h.top - gap - ch, left, place: 'above' });
    // Sığmıyorsa kart hedefin daha az yer kaplayan yarısının üstüne biner
    else setPos({ top: h.top + h.height / 2 > vh / 2 ? 16 : vh - ch - 16, left, place: 'below' });
  }, [phase, stop]);

  // Hedef ekran dışındaysa görünür yap (telefonda Pekiştir aşağıda kalır)
  useEffect(() => {
    if (phase !== 'tour' || !stop) return;
    const el = firstVisible(stop.sel);
    if (!el) return;
    const r = el.getBoundingClientRect();
    if (r.bottom < 0 || r.top > window.innerHeight - 80) el.scrollIntoView({ block: 'start', behavior: 'smooth' });
    const ts = [120, 450].map((ms) => window.setTimeout(measure, ms));
    return () => ts.forEach(window.clearTimeout);
  }, [phase, stop, measure]);

  useLayoutEffect(() => {
    measure();
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

  const next = () => (i < total - 1 ? setI(i + 1) : setPhase('catalog'));
  const prev = () => (phase === 'catalog' ? (total ? (setPhase('tour'), setI(total - 1)) : undefined) : i > 0 && setI(i - 1));

  // Klavye: oynatıcının kısayolları (Esc = kitaplığa dön, oklar = adım) tur açıkken çalışmasın
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Tab' || e.key === 'Enter' || e.key === ' ') return;
      e.stopPropagation();
      if (e.key === 'Escape') {
        e.preventDefault();
        finish('skipped');
      } else if (phase === 'tour' && e.key === 'ArrowRight') next();
      else if (phase === 'tour' && e.key === 'ArrowLeft') prev();
    };
    window.addEventListener('keydown', onKey, true);
    return () => window.removeEventListener('keydown', onKey, true);
  });

  useEffect(() => {
    cardRef.current?.focus({ preventScroll: true });
  }, [phase, i]);

  let body: React.ReactNode;
  if (phase === 'catalog') {
    const lessonIx = IX_GUIDE.filter((g) => !g.game);
    const games = IX_GUIDE.filter((g) => g.game);
    const row = (g: IxGuide) => {
      const [Icon, label] = IX_META[g.type] || [Sparkles, g.type];
      const on = open === g.type;
      return (
        <li key={g.type} className={on ? 'is-open' : ''}>
          <button type="button" className="lt-ix" aria-expanded={on} onClick={() => setOpen(on ? null : g.type)}>
            <span className="lt-ix-ico" aria-hidden="true"><Icon /></span>
            <span className="lt-ix-t">{label}</span>
            <ChevronDown className="lt-ix-chev" aria-hidden="true" />
          </button>
          {on && (
            <div className="lt-ix-b">
              <p><b>Nasıl:</b> {g.how}</p>
              <p><b>Neyi ölçer:</b> {g.why}</p>
            </div>
          )}
        </li>
      );
    };
    body = (
      <div className="wt-tour lt-root" role="dialog" aria-modal="true" aria-labelledby="lt-h">
        <div className="wt-scrim is-solid" onClick={() => finish('done')} />
        <div ref={cardRef} tabIndex={-1} className={`lt-cat ${v12 ? 'is-v12' : ''}`}>
          <div className="lt-cat-h">
            <span className="lt-cat-ico" aria-hidden="true"><Compass /></span>
            <div>
              <h2 id="lt-h">Etkileşim rehberi</h2>
              <p>Pekiştir bölümünde karşılaşacağın türler. Birine dokun, nasıl çözüldüğünü gör.</p>
            </div>
            <button type="button" className="wt-x is-sm" onClick={() => finish('done')} aria-label="Rehberi kapat"><X /></button>
          </div>
          <div className="lt-cat-b">
            <ul className="lt-ix-list">{lessonIx.map(row)}</ul>
            <h3 className="lt-cat-sub">Ders sonu oyunları <span>son adımda</span></h3>
            <ul className="lt-ix-list">{games.map(row)}</ul>
            <p className="lt-cat-note">
              Her etkileşim yalnız o adıma kadar anlatılanları sorar. Takıldığın ya da hatalı bulduğun bir öge için kartın köşesindeki bayrağa dokun.
            </p>
          </div>
          <div className="lt-cat-f">
            {total > 0 && (
              <button type="button" className="wt-nav" onClick={prev} aria-label="Tura dön"><ChevronLeft /></button>
            )}
            <span className="lt-grow" />
            <button type="button" className="wt-nav is-primary" onClick={() => finish('done')}>
              {kind === 'library' ? 'Derslere başla' : 'Derse dön'} <ChevronRight aria-hidden="true" />
            </button>
          </div>
        </div>
      </div>
    );
  } else {
    const Icon = stop.icon;
    body = (
      <div className="wt-tour lt-root" role="dialog" aria-modal="true" aria-labelledby="wt-t" aria-describedby="wt-d">
        {hole ? (
          <svg className="wt-scrim" aria-hidden="true">
            <path fillRule="evenodd" d={`M0 0H${window.innerWidth}V${window.innerHeight}H0Z ${roundRect(hole, 12)}`} />
          </svg>
        ) : (
          <div className="wt-scrim is-solid" />
        )}
        {hole && <div className="wt-hole" aria-hidden="true" style={{ top: hole.top, left: hole.left, width: hole.width, height: hole.height }} />}
        <div
          ref={cardRef}
          tabIndex={-1}
          className={`wt-card lt-card is-${pos.place} ${v12 ? 'is-v12' : ''}`}
          style={pos.place === 'center' ? undefined : { top: pos.top, left: pos.left }}
        >
          <div className="wt-card-h">
            <span className="lt-ico" aria-hidden="true"><Icon /></span>
            <span className="wt-card-eb">{stop.eyebrow}</span>
            <span className="wt-count" aria-label={`${total} duraktan ${i + 1}.`}>{i + 1}/{total}</span>
            <button type="button" className="wt-x is-sm" onClick={() => finish('skipped')} aria-label="Turu kapat"><X /></button>
          </div>
          <div className="wt-card-b" key={i}>
            <h2 id="wt-t" className="wt-card-t">{stop.title}</h2>
            <p id="wt-d" className="wt-card-p">{stop.text}</p>
            <ul className="wt-points">
              {stop.points.map((p) => <li key={p}>{p}</li>)}
            </ul>
          </div>
          <div className="wt-card-f">
            <div className="wt-prog" aria-hidden="true">
              {stops.map((_, n) => <i key={n} className={n === i ? 'is-on' : n < i ? 'is-past' : ''} />)}
            </div>
            <button type="button" className="wt-nav" onClick={prev} disabled={i === 0} aria-label="Önceki"><ChevronLeft /></button>
            <button type="button" className="wt-nav is-primary" onClick={next}>
              {i === total - 1 ? 'Etkileşimler' : 'İleri'} <ChevronRight aria-hidden="true" />
            </button>
          </div>
        </div>
      </div>
    );
  }
  return createPortal(body, document.body);
};

export default LearnTour;
