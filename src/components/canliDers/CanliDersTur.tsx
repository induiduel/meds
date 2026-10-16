/**
 * Canlı ders tanıtım turu — iki parça:
 *   • liste: /canliders (canlı ders nedir, arama, kategoriler, Dinle, Oynat, seçenekler (sesler/MP3/çevrimdışı/listem), arka planda dinleme)
 *   • ders:  /canliders/<key> (PDF, metin, takip, oynatıcı, bölümler, ses/hız/indirme, kısayollar, mini oynatıcı)
 * Öğren turunun (LearnTour) görsel dilini ve sınıflarını (wt-/lt-) kullanır: SVG maskeli karartmada delik + kart.
 * Öğesi sayfada olmayan `optional` duraklar atlanır (PDF yok, oynatıcı başka derste, geniş ekranda sekme yok…);
 * öğesi olmayan zorunlu durak kart ortada açılır. Tur sesi durdurmaz; oynatıcının klavye kısayolları tur açıkken
 * tura gider (Esc kapatır, ←/→ durak değiştirir). Katman body'ye taşınır (v12 ölçek katmanından etkilenmesin).
 */
import React, { useCallback, useEffect, useLayoutEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import {
  AudioLines, ChevronLeft, ChevronRight, Crosshair, Download, FileText, Gauge, Headphones, Keyboard, ListOrdered,
  MonitorSmartphone, Play, ScrollText, Search, SlidersHorizontal, Smartphone, X,
} from 'lucide-react';
import { cdTurIsaretle, type CdTurTuru } from './canliDersTurDurum';
import '../onboarding/welcome-tour.css';
import '../onboarding/learn-tour.css';

type Durak = {
  /** Vurgulanacak öğe; yoksa kart ortada açılır */
  sel?: string;
  icon: React.ElementType;
  eyebrow: string;
  title: string;
  text: string;
  points: string[];
  /** Öğe sayfada yoksa durağı atla */
  optional?: boolean;
  /** Eşleşen tüm görünür öğeleri tek delikte birleştir */
  union?: boolean;
  /** Yalnız ince işaretçili (fare/klavye) cihazlarda göster */
  masaustu?: boolean;
};

const satir = '.cd-satirlar > .cd-satir:first-child';

const LISTE: Durak[] = [
  {
    sel: '.cd-liste-baslik',
    icon: Headphones,
    eyebrow: 'Canlı ders',
    title: 'Dersi dinleyerek çalış',
    text: 'Her ders sesli anlatılır; konuşma metni ve dersin slaytları sesle eşzamanlı akar.',
    points: ['Okunan cümle metinde vurgulanır', 'Anlatılan slayt sayfası kendiliğinden açılır', 'Dinlerken başka sayfaya geçebilirsin, ses sürer'],
  },
  {
    sel: '.cd-ara',
    icon: Search,
    eyebrow: 'Arama',
    title: 'Dersi bul',
    text: 'Ders adını ya da numarasını yaz; liste anında daralır.',
    points: ['Büyük-küçük harf ve Türkçe karakter fark etmez', '× ile aramayı temizle'],
  },
  {
    sel: '.cd-kat-cipler',
    icon: ListOrdered,
    eyebrow: 'Kategoriler',
    title: 'Konuya göre süz',
    text: 'Dersler konu başlıklarına ayrılmıştır; bir çipe dokununca yalnız o konunun dersleri kalır.',
    points: ['“Yarım kalanlar” dinlemeye başladığın dersleri toplar', 'Kategori başlığına dokunarak bölümü katlayabilirsin'],
    optional: true,
  },
  {
    sel: `${satir} .cd-satir-ad`,
    icon: AudioLines,
    eyebrow: 'Ders satırı',
    title: 'Süre ve ilerleme',
    text: 'Her satırda dersin süresi, kaç seslendirmesi olduğu ve ne kadarını dinlediğin yazar.',
    points: ['Çalan dersin satırı renkle işaretlenir'],
    optional: true,
  },
  {
    sel: `${satir} .cd-btn.is-ana`,
    icon: Headphones,
    eyebrow: 'Dinle',
    title: 'Ders ekranını aç',
    text: '“Dinle” dersi metin ve slaytlarla birlikte açar. Ders adına dokunmak da aynı işi yapar.',
    points: ['Masaüstünde PDF ve metin yan yana, telefonda sekmeli', 'Kaldığın yer hatırlanır'],
    optional: true,
  },
  {
    sel: `${satir} .cd-satir-eylem > button.cd-btn:not(.is-ana):not(.is-ikon)`,
    icon: Play,
    eyebrow: 'Oynat',
    title: 'Yalnız sesi başlat',
    text: '“Oynat” sayfadan ayrılmadan yalnız sesi çalar; alttaki küçük oynatıcıdan yönetirsin.',
    points: ['Aynı düğme çalarken “Duraklat” olur', 'Yürürken ya da yolda dinlemek için ideal'],
    optional: true,
  },
  {
    sel: `${satir} .cd-satir-diger .cd-btn`,
    icon: SlidersHorizontal,
    eyebrow: 'Seçenekler',
    title: 'Ses, indirme ve listem',
    text: '“⋯” düğmesi dersin diğer işlemlerini açar.',
    points: ['Başka bir seslendirmeyi oynat ya da MP3 indir', 'Çevrimdışı: ses, metin ve slaytları cihaza indir', 'Listeme ekle: dersleri sırayla dinlemek için'],
    optional: true,
  },
  {
    sel: '.cd-dock.is-mini .cd-mini',
    icon: Smartphone,
    eyebrow: 'Arka planda',
    title: 'Ses seni takip eder',
    text: 'Başka bir sayfaya geçince ders altta mini oynatıcıda çalmaya devam eder.',
    points: [
      'Ekran kapalıyken ve kilit ekranında da çalar',
      'Kilit ekranı / bildirim denetimleriyle duraklat ve sar',
      'Mini oynatıcıdan derse dönebilir, hızı değiştirebilirsin',
    ],
  },
];

const dock = '.cd-dock.is-tam';

const DERS: Durak[] = [
  {
    sel: '.cd-ders-ad',
    icon: Headphones,
    eyebrow: 'Ders ekranı',
    title: 'Dinle, oku, izle',
    text: 'Ses çalarken metin ve slaytlar kendiliğinden ilerler; sen yalnız dinle.',
    points: ['Oynatıcı altta sabittir', 'Sağ üstteki “Tanıtım” (?) düğmesi bu turu yeniden açar'],
  },
  {
    sel: '.cd-sekmeler',
    icon: MonitorSmartphone,
    eyebrow: 'Görünüm',
    title: 'Metin, Metin + PDF ya da yalnız PDF',
    text: 'İstediğin görünümü seç; Metin + PDF ekranı böler (telefonda üstte PDF, altta metin).',
    points: ['Seçimin bu cihazda hatırlanır', 'Ses görünüm değişince durmaz; anlatılan sayfa kendiliğinden açılır'],
    optional: true,
  },
  {
    sel: '.cd-tam-btn',
    icon: MonitorSmartphone,
    eyebrow: 'Odak',
    title: 'Tam ekran',
    text: 'Menüler ve oynatıcı gizlenir, yalnız metin ve PDF kalır. Ses çalmayı sürdürür.',
    points: ['Sağ alttaki düğmeyle oynat/duraklat ya da oynatıcıyı aç', 'Çıkmak için sağ üstteki düğme ya da Esc'],
    optional: true,
  },
  {
    sel: '.cd-pdf-bolme',
    icon: FileText,
    eyebrow: 'Slaytlar',
    title: 'Ders PDF’i',
    text: 'Anlatılan sayfa “Şu an anlatılan” etiketiyle işaretlenir ve sesle birlikte kendiliğinden ilerler.',
    points: ['Üst çubukta sayfa numarası ve yakınlaştırma', 'PDF’i gezersen takip kısa süre durur'],
    optional: true,
  },
  {
    sel: '.cd-metin-bolme',
    icon: ScrollText,
    eyebrow: 'Metin',
    title: 'Konuşma metni',
    text: 'Okunan paragraf ve cümle vurgulanır; metin onu ortada tutacak şekilde kayar.',
    points: ['Bir paragrafa dokun: ses o yerden devam eder', 'Metni seçip kopyalayabilirsin; seçerken atlamaz'],
  },
  {
    sel: '.cd-metin-bolme',
    icon: Crosshair,
    eyebrow: 'Takip',
    title: 'Elle gezinince',
    text: 'Metni ya da PDF’i elle kaydırınca otomatik takip durur, okuduğun yer kaçmaz.',
    points: ['Altta “Canlı konuma dön” düğmesi çıkar', 'Dokunmazsan birkaç saniye sonra takip kendiliğinden sürer'],
  },
  {
    sel: `${dock} .cd-denetim-orta`,
    icon: Play,
    eyebrow: 'Oynatıcı',
    title: 'Oynat ve sar',
    text: 'Ortadaki düğme oynatır ya da duraklatır; yanındakiler 10 sn sarar, en dıştakiler önceki/sonraki bölüme atlar.',
    points: ['Halka dönüyorsa ses yükleniyor demektir'],
    optional: true,
  },
  {
    sel: `${dock} .cd-zaman, ${dock} .cd-menu-kap`,
    union: true,
    icon: ListOrdered,
    eyebrow: 'Zaman çubuğu',
    title: 'Bölümler arasında gez',
    text: 'Çubuğa dokun ya da sürükle; çizgiler bölüm başlarını gösterir, sürüklerken bölüm adı görünür.',
    points: ['Soldaki düğme şu anki bölümü gösterir; dokununca bölüm listesi açılır', 'Çubuk odaktayken ←/→ 5 sn, PageUp/Down 1 dk sarar'],
    optional: true,
  },
  {
    sel: `${dock} .cd-denetim-sag`,
    icon: Gauge,
    eyebrow: 'Ayarlar',
    title: 'Ses, hız, indirme',
    text: 'Hızı 1× ile 4× arasında ayarla; “⋯” menüsünden anlatan sesi seç, tekrarı aç ya da dersi MP3 olarak indir.',
    points: ['Ses değişince kaldığın yer korunur', 'Hız ve ses seçimin hatırlanır'],
    optional: true,
  },
  {
    sel: dock,
    icon: Keyboard,
    eyebrow: 'Kısayollar',
    title: 'Klavyeyle denetle',
    text: 'Bir yazı alanında değilken:',
    points: ['Boşluk: oynat / duraklat', '← / →: 10 sn geri / ileri'],
    optional: true,
    masaustu: true,
  },
  {
    sel: '.cd-ders-daha .cd-daha-btn',
    icon: SlidersHorizontal,
    eyebrow: 'Seçenekler',
    title: 'Çevrimdışı ve listem',
    text: 'Başlıktaki “⋯” menüsü dersi cihaza indirir, listene ekler ve bu tanıtımı yeniden açar.',
    points: ['Çevrimdışı: ses, metin ve slaytlar internetsiz açılır'],
    optional: true,
  },
  {
    sel: '.cd-geri',
    icon: Smartphone,
    eyebrow: 'Arka planda',
    title: 'Sayfadan çıksan da çalar',
    text: 'Başka bir sayfaya geçince ders altta mini oynatıcıda sürer; dokununca bu ekrana dönersin.',
    points: ['Ekran kapalıyken ve kilit ekranında da çalmaya devam eder', 'Kilit ekranı denetimleriyle duraklat ve sar'],
  },
];

const gorunur = (el: Element | null): el is HTMLElement => {
  if (!(el instanceof HTMLElement)) return false;
  const r = el.getBoundingClientRect();
  if (r.width < 4 || r.height < 4) return false;
  const cs = getComputedStyle(el);
  return cs.visibility !== 'hidden' && cs.display !== 'none' && Number(cs.opacity) > 0.05;
};
const ilkGorunur = (sel?: string) => {
  if (!sel) return null;
  for (const el of Array.from(document.querySelectorAll(sel))) if (gorunur(el)) return el;
  return null;
};
const hedefRect = (d: Durak): DOMRect | null => {
  if (!d.sel) return null;
  if (!d.union) return ilkGorunur(d.sel)?.getBoundingClientRect() ?? null;
  const rs = Array.from(document.querySelectorAll(d.sel)).filter(gorunur).map((e) => e.getBoundingClientRect());
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

export default function CanliDersTur({ tur, onClose }: { tur: CdTurTuru; onClose: () => void }) {
  const [tum] = useState(() => {
    let ince = true;
    try { ince = window.matchMedia('(hover: hover) and (pointer: fine)').matches; } catch { /* eski tarayıcı */ }
    return (tur === 'liste' ? LISTE : DERS).filter((d) => ince || !d.masaustu);
  });
  const [cur, setCur] = useState(0);
  // Sayfada bulunmayan isteğe bağlı duraklar her çizimde ayıklanır (oynatıcı geç yüklenebilir; sayaç doğru kalsın)
  const duraklar = tum.filter((d, n) => n === cur || !d.optional || ilkGorunur(d.sel));
  const i = Math.max(0, duraklar.indexOf(tum[cur]));
  const durak = duraklar[i];
  const toplam = duraklar.length;
  const git = (n: number) => setCur(tum.indexOf(duraklar[n]));
  // Hangi isteğe bağlı durakların öğesi sayfada: değişince yeniden çiz (sayaç ve ilerleme noktaları güncel kalsın)
  const [, setImza] = useState('');
  const [hole, setHole] = useState<Rect | null>(null);
  const [pos, setPos] = useState<Pos>({ top: 0, left: 0, place: 'center' });
  const cardRef = useRef<HTMLDivElement>(null);
  const oncekiOdak = useRef<HTMLElement | null>(typeof document !== 'undefined' ? (document.activeElement as HTMLElement | null) : null);

  useEffect(() => {
    cdTurIsaretle(tur, 'basladi'); // yarıda sayfadan çıkılsa da yeniden kendiliğinden açılmasın
    const odak = oncekiOdak.current;
    return () => {
      if (odak && odak.isConnected && odak !== document.body) odak.focus({ preventScroll: true });
    };
  }, [tur]);

  const bitir = useCallback(
    (nasil: 'bitti' | 'atlandi') => {
      cdTurIsaretle(tur, nasil);
      onClose();
    },
    [tur, onClose],
  );

  const olc = useCallback(() => {
    if (!durak) return;
    const r = hedefRect(durak);
    if (!r) {
      setHole(null);
      setPos((o) => (o.place === 'center' ? o : { top: 0, left: 0, place: 'center' }));
      return;
    }
    const vw = window.innerWidth;
    const vh = window.innerHeight;
    const pad = 6;
    const top = Math.max(8, r.top - pad);
    const bottom = Math.min(vh - 8, r.bottom + pad);
    const left = Math.max(8, r.left - pad);
    const h: Rect = { top, left, width: Math.min(vw - 8 - left, r.width + pad * 2), height: Math.max(24, bottom - top) };
    setHole((o) => (o && o.top === h.top && o.left === h.left && o.width === h.width && o.height === h.height ? o : h));
    const yer = (p: Pos) => setPos((o) => (o.top === p.top && o.left === p.left && o.place === p.place ? o : p));
    const cw = Math.min(360, vw - 32);
    const ch = cardRef.current?.offsetHeight || 280;
    const gap = 14;
    if (h.left + h.width + gap + cw + 16 <= vw) {
      yer({ top: Math.max(16, Math.min(vh - ch - 16, h.top + h.height / 2 - ch / 2)), left: h.left + h.width + gap, place: 'right' });
      return;
    }
    if (h.left - gap - cw >= 16) {
      yer({ top: Math.max(16, Math.min(vh - ch - 16, h.top + h.height / 2 - ch / 2)), left: h.left - gap - cw, place: 'left' });
      return;
    }
    const x = Math.max(16, Math.min(vw - cw - 16, h.left + h.width / 2 - cw / 2));
    const ust = h.top - gap - 16;
    const alt = vh - (h.top + h.height) - gap - 16;
    if (alt >= ch) yer({ top: h.top + h.height + gap, left: x, place: 'below' });
    else if (ust >= ch) yer({ top: h.top - gap - ch, left: x, place: 'above' });
    // Sığmıyorsa kart hedefin daha az yer kaplayan yarısının üstüne biner
    else yer({ top: h.top + h.height / 2 > vh / 2 ? 16 : Math.max(16, vh - ch - 16), left: x, place: 'below' });
  }, [durak]);

  // Hedef ekran dışındaysa görünür yap (uzun listede satır aşağıda kalabilir)
  useEffect(() => {
    const el = ilkGorunur(durak?.sel);
    if (el) {
      const r = el.getBoundingClientRect();
      if (r.bottom < 0 || r.top > window.innerHeight - 80) el.scrollIntoView({ block: 'center', behavior: 'smooth' });
    }
    const ts = [120, 450].map((ms) => window.setTimeout(olc, ms));
    return () => ts.forEach(window.clearTimeout);
  }, [durak, olc]);

  useLayoutEffect(() => {
    olc();
    const raf = requestAnimationFrame(olc);
    return () => cancelAnimationFrame(raf);
  }, [olc]);

  useEffect(() => {
    let raf = 0;
    const on = () => {
      if (!raf) raf = requestAnimationFrame(() => {
        raf = 0;
        olc();
        setImza(tum.map((d) => (!d.optional || ilkGorunur(d.sel) ? 1 : 0)).join(''));
      });
    };
    window.addEventListener('resize', on);
    window.addEventListener('scroll', on, true);
    window.visualViewport?.addEventListener('resize', on);
    const ro = new ResizeObserver(on);
    if (cardRef.current) ro.observe(cardRef.current);
    ro.observe(document.documentElement);
    // Oynatıcı tembel yüklenir / sekme değişir: DOM değişince yeniden ölç (duraklar da yeniden süzülür)
    const mo = new MutationObserver(on);
    mo.observe(document.querySelector('#root') || document.body, { childList: true, subtree: true });
    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener('resize', on);
      window.removeEventListener('scroll', on, true);
      window.visualViewport?.removeEventListener('resize', on);
      ro.disconnect();
      mo.disconnect();
    };
  }, [olc, tum]);

  const ileri = () => (i < toplam - 1 ? git(i + 1) : bitir('bitti'));
  const geri = () => i > 0 && git(i - 1);

  // Klavye: oynatıcının kısayolları (boşluk, ←/→) tur açıkken çalışmasın; Tab kartın içinde döner
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Tab') {
        const card = cardRef.current;
        if (!card) return;
        const f = Array.from(card.querySelectorAll<HTMLElement>('button:not([disabled])'));
        if (!f.length) return;
        const a = document.activeElement;
        if (!card.contains(a)) {
          e.preventDefault();
          f[0].focus();
        } else if (e.shiftKey && (a === f[0] || a === card)) {
          e.preventDefault();
          f[f.length - 1].focus();
        } else if (!e.shiftKey && a === f[f.length - 1]) {
          e.preventDefault();
          f[0].focus();
        }
        return;
      }
      if (e.key === 'Enter') return;
      e.stopPropagation();
      if (e.key === 'Escape') {
        e.preventDefault();
        bitir('atlandi');
      } else if (e.key === 'ArrowRight') {
        e.preventDefault();
        ileri();
      } else if (e.key === 'ArrowLeft') {
        e.preventDefault();
        geri();
      } else if (e.key === ' ' && !(e.target instanceof HTMLButtonElement)) {
        e.preventDefault(); // sayfa kaymasın, ses durup başlamasın
      }
    };
    window.addEventListener('keydown', onKey, true);
    return () => window.removeEventListener('keydown', onKey, true);
  });

  useEffect(() => {
    cardRef.current?.focus({ preventScroll: true });
  }, [i]);

  if (!durak) return null;
  const Icon = durak.icon;
  const son = i === toplam - 1;
  return createPortal(
    <div className="wt-tour lt-root cd-tur" role="dialog" aria-modal="true" aria-labelledby="cdt-t" aria-describedby="cdt-d">
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
        className={`wt-card lt-card is-${pos.place}`}
        style={pos.place === 'center' ? undefined : { top: pos.top, left: pos.left }}
      >
        <div className="wt-card-h">
          <span className="lt-ico" aria-hidden="true"><Icon /></span>
          <span className="wt-card-eb">{durak.eyebrow}</span>
          <span className="wt-count" aria-label={`${toplam} duraktan ${i + 1}.`}>{i + 1}/{toplam}</span>
          <button type="button" className="wt-x is-sm" onClick={() => bitir('atlandi')} aria-label="Turu kapat"><X /></button>
        </div>
        <div className="wt-card-b" key={i} aria-live="polite">
          <h2 id="cdt-t" className="wt-card-t">{durak.title}</h2>
          <p id="cdt-d" className="wt-card-p">{durak.text}</p>
          <ul className="wt-points">
            {durak.points.map((p) => <li key={p}>{p}</li>)}
          </ul>
        </div>
        <div className="wt-card-f">
          <div className="wt-prog" aria-hidden="true">
            {duraklar.map((_, n) => <i key={n} className={n === i ? 'is-on' : n < i ? 'is-past' : ''} />)}
          </div>
          <button type="button" className="wt-nav" onClick={geri} disabled={i === 0} aria-label="Önceki"><ChevronLeft /></button>
          <button type="button" className="wt-nav is-primary" onClick={ileri}>
            {son ? 'Bitir' : 'İleri'} {!son && <ChevronRight aria-hidden="true" />}
          </button>
        </div>
      </div>
    </div>,
    document.body,
  );
}
