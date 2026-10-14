import React, { useState, useEffect, useMemo, useRef, useCallback } from 'react';
import {
  Archive,
  ArrowUpRight,
  BookOpenText,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  Compass,
  GraduationCap,
  Presentation,
  RotateCcw,
  Sparkles,
  Target,
  Zap,
} from 'lucide-react';
import { PageToolbar, QuickOptions, type ToolbarQuick } from './ui/PageToolbar';
import { foldText } from '../services/searchText';
import { navigateTo, pathFor } from '../router';
import './kazanimlar.css';
import '../styles/v12/secondary.css';

/**
 * Kazanımlar (v11) — Kurul → Ders → Konu → kazanım hiyerarşisi.
 *  - Üst çubuk: arama + hızlı haplar (Kurul ▾ · Ders ▾ · Kapsam ▾).
 *  - Sol: kurul özeti (toplam kapsam çubuğu) + derse göre gruplu konu listesi; her konuda kapsam çubuğu ve sayı.
 *  - Sağ: konum yolu, konu başlığı, kapsam özeti (çubuk + kısa açıklama), konu düzeyi eylemler (Öğren, örnek, spot, çıkmış),
 *    numaralı kazanım satırları (numara rozeti kapsam renginde; altında kaynak sayıları). Satır açılınca kaynaklar
 *    gruplar hâlinde: slayt (sayfaya git), özet, sözlük, çıkmış (Çıkmış'ta aç), örnek soru (yerinde çöz / modda aç).
 *  - Kapsam: tam = desteye (slayt) ve soruya (çıkmış ya da örnek) bağlı; kısmi = ikisinden biri; yok = hiçbiri.
 *  - Telefon (<768): önce konu listesi, dokununca ayrıntı ("Dersler" geri düğmesiyle dönülür), tek sütun.
 *  - Adres: ?kurul=1&konu=<ders::konu> (paylaşılabilir; geri tuşu bozulmaz, replaceState).
 * Sınıf öneki `kz-` (components/kazanimlar.css).
 */

interface KazanimItem {
  id: string;
  metin: string;
  totalCikmisCount?: number;
  totalOrnekCount?: number;
  firstOrnekKazanimNo?: number;
  slaytlar: Array<{ kaynak: string; sayfa: number; alinti?: string; deckId?: string }>;
  cikmisSorular: Array<{
    id: string;
    questionNumber?: number;
    stem: string;
    correctAnswer: string;
    options: Array<{ key: string; text: string }>;
    year: string;
    discipline: string;
    topic: string;
    explanation?: string;
  }>;
  ornekSorular: Array<{
    id: string;
    kazanimNo?: number;
    zorluk?: string;
    soru: string;
    secenekler: Record<string, string>;
    dogru: string;
    aciklama?: string;
  }>;
  sozlukTerimleri: Array<{ term: string; definition: string; pearl?: string }>;
  ozetler: string[];
}

interface KonuGroup { konu: string; kazanimlar: KazanimItem[] }
interface DersGroup { ders: string; count: number; konular: KonuGroup[] }
interface KurulData { kurul: number; name: string; totalCount: number; dersler: DersGroup[] }

/** Sınav spotları (yalnız Kurul 1): deste → spot sayısı ve ilk spot (derin bağlantı için) */
interface SpotOzet { n: number; ilk: string }

const liteLoaders = import.meta.glob('../data/kazanimlar/lite/k*.json', { import: 'default' }) as Record<string, () => Promise<any>>;
const questionLoaders = import.meta.glob('../data/kazanimlar/questions/k*.json', { import: 'default' }) as Record<string, () => Promise<any>>;

/** Kurul adları (index.json ile aynı; hap ipucunda gösterilir) */
const KURUL_AD: Record<number, string> = {
  1: 'Ürogenital ve Obstetrik',
  2: 'Nöropsikiyatri',
  3: 'Gastrointestinal Sistem',
  4: 'Dolaşım, Solunum ve Tümör',
  5: 'Ortopedi, Travmatoloji ve Hematopoetik',
  6: 'Endokrin, Metabolizma ve Yaşlanma',
};

interface Props {
  onNavigateToLearn?: (deckId?: string, slideNumber?: number) => void;
  onNavigateToPastExams?: (query?: string) => void;
  onNavigateToOrnek?: (lessonId?: string, kazanimNo?: number) => void;
}

type Kapsam = 0 | 1 | 2;
type KapsamFiltre = 'all' | '2' | '1' | '0';

/** Konu (ders saati): kazanımlar asıl sırasıyla (örnek soru numarası için `no`) */
interface Ders {
  key: string;
  ders: string;
  konu: string;
  no: number | null;
  deckId?: string;
  items: Array<{ k: KazanimItem; no: number }>;
}

const cikmisSayisi = (k: KazanimItem) => k.totalCikmisCount ?? (k.cikmisSorular ? k.cikmisSorular.length : 0);
const ornekSayisi = (k: KazanimItem) => k.totalOrnekCount ?? (k.ornekSorular ? k.ornekSorular.length : 0);
const kapsamOf = (k: KazanimItem): Kapsam =>
  (Number(k.slaytlar.length > 0) + Number(cikmisSayisi(k) > 0 || ornekSayisi(k) > 0)) as Kapsam;
const KAPSAM_AD: Record<Kapsam, string> = { 2: 'Tam kapsam', 1: 'Kısmi kapsam', 0: 'İçerik yok' };
const KAPSAM_KISA: Record<Kapsam, string> = { 2: 'tam', 1: 'kısmi', 0: 'içerik yok' };

/** Destenin numarası: "k1-03-hucresel-adaptasyonlar" → 3 (konudaki en sık deste) */
function desteBilgisi(konu: KonuGroup): { no: number | null; deckId?: string } {
  const say = new Map<string, number>();
  for (const k of konu.kazanimlar) for (const s of k.slaytlar) if (s.deckId) say.set(s.deckId, (say.get(s.deckId) || 0) + 1);
  const deckId = [...say.entries()].sort((a, b) => b[1] - a[1])[0]?.[0];
  const m = deckId?.match(/^k\d+-(\d+)-/);
  return { no: m ? parseInt(m[1], 10) : null, deckId };
}

function kapsamSay(items: KazanimItem[]): [number, number, number] {
  const n: [number, number, number] = [0, 0, 0];
  for (const k of items) n[kapsamOf(k)] += 1;
  return n;
}

function useMedia(q: string) {
  const [on, setOn] = useState(() => typeof window !== 'undefined' && !!window.matchMedia?.(q).matches);
  useEffect(() => {
    const m = window.matchMedia?.(q);
    if (!m) return;
    const f = () => setOn(m.matches);
    f();
    m.addEventListener('change', f);
    return () => m.removeEventListener('change', f);
  }, [q]);
  return on;
}

const readUrl = () => {
  try {
    const p = new URLSearchParams(window.location.search);
    const k = Number(p.get('kurul'));
    return { kurul: k >= 1 && k <= 6 ? k : 1, konu: p.get('konu') };
  } catch {
    return { kurul: 1, konu: null };
  }
};

export const KazanimlarView: React.FC<Props> = ({ onNavigateToLearn, onNavigateToPastExams, onNavigateToOrnek }) => {
  const initial = useRef(readUrl());
  const [selectedKurul, setSelectedKurul] = useState<number>(initial.current.kurul);
  const [selectedDers, setSelectedDers] = useState<string>('all');
  const [kapsamFiltre, setKapsamFiltre] = useState<KapsamFiltre>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [kurulData, setKurulData] = useState<KurulData | null>(null);
  const [questionMap, setQuestionMap] = useState<Record<string, { cikmisSorular?: KazanimItem['cikmisSorular']; ornekSorular?: KazanimItem['ornekSorular'] }> | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [loadError, setLoadError] = useState(false);
  const [reloadTick, setReloadTick] = useState(0);
  const [spots, setSpots] = useState<Map<string, SpotOzet> | null>(null);

  const [selectedKey, setSelectedKey] = useState<string | null>(initial.current.konu);
  /** Telefonda ayrıntı açık mı (liste ↔ ayrıntı yığını); adresle gelen konu doğrudan açılır */
  const [phoneDetail, setPhoneDetail] = useState(Boolean(initial.current.konu));
  const [openKz, setOpenKz] = useState<string | null>(null);
  const [ornekAnswers, setOrnekAnswers] = useState<Record<string, string>>({});

  const isPhone = useMedia('(max-width: 767px)');
  const rootRef = useRef<HTMLDivElement>(null);
  const detailRef = useRef<HTMLElement>(null);
  const prevKurul = useRef(initial.current.kurul);

  useEffect(() => {
    let alive = true;
    setLoading(true);
    setLoadError(false);
    setSelectedDers('all');
    setOpenKz(null);
    setQuestionMap(null);
    // İlk yüklemede adresteki konu korunur; kurul değişince seçim sıfırlanır
    if (prevKurul.current !== selectedKurul) { setSelectedKey(null); setPhoneDetail(false); }
    prevKurul.current = selectedKurul;
    const liteFn = liteLoaders[`../data/kazanimlar/lite/k${selectedKurul}.json`];
    if (!liteFn) {
      setLoadError(true);
      setLoading(false);
      return;
    }
    liteFn()
      .then((m) => { if (alive) { setKurulData(m ? (m.default || m) : null); setLoading(false); } })
      .catch(() => { if (alive) { setLoadError(true); setLoading(false); } });
    return () => { alive = false; };
  }, [selectedKurul, reloadTick]);

  // Bir kazanım satırı açılınca o kurulun soru havuzunu (questions/k*.json) isteğe bağlı yükle
  useEffect(() => {
    if (!openKz || questionMap) return;
    const qFn = questionLoaders[`../data/kazanimlar/questions/k${selectedKurul}.json`];
    if (!qFn) return;
    let alive = true;
    qFn()
      .then((m) => { if (alive && m) setQuestionMap(m.default || m); })
      .catch(() => {});
    return () => { alive = false; };
  }, [openKz, selectedKurul, questionMap]);

  // Sınav spotları yalnız Kurul 1'de var: deste kimliğine göre konu başına sayı (kazanım verisinden sonra yüklenir)
  useEffect(() => {
    if (selectedKurul !== 1 || loading || spots) return;
    let alive = true;
    import('../data/exam_spots_k1.json')
      .then((m) => {
        if (!alive) return;
        const v = (m.default ?? m) as unknown as { dersler: Array<{ no: number; id: string }>; spotlar: Array<{ id: string; ders: number }> };
        const byNo = new Map<number, SpotOzet>();
        for (const s of v.spotlar) {
          const cur = byNo.get(s.ders);
          if (cur) cur.n += 1;
          else byNo.set(s.ders, { n: 1, ilk: s.id });
        }
        const out = new Map<string, SpotOzet>();
        for (const d of v.dersler) { const o = byNo.get(d.no); if (o) out.set(d.id, o); }
        setSpots(out);
      })
      .catch(() => { /* spotlar isteğe bağlı */ });
    return () => { alive = false; };
  }, [selectedKurul, loading, spots]);

  // Üst çubuğun yüksekliği: masaüstünde konu listesi bunun altına yapışır
  useEffect(() => {
    const root = rootRef.current;
    const bar = root?.querySelector('.pt-root') as HTMLElement | null;
    if (!root || !bar || typeof ResizeObserver === 'undefined') return;
    const ro = new ResizeObserver(() => root.style.setProperty('--kz-bar', `${Math.round(bar.getBoundingClientRect().height)}px`));
    ro.observe(bar);
    return () => ro.disconnect();
  }, []);

  /** Ders (disiplin) grupları, ders programı sırasıyla; grup içinde deste numarası varsa ona göre */
  const groups = useMemo(() => {
    if (!kurulData) return [] as Array<{ ders: string; lessons: Ders[] }>;
    return kurulData.dersler.map((d) => {
      const lessons: Ders[] = d.konular.map((konu) => {
        const { no, deckId } = desteBilgisi(konu);
        return { key: `${d.ders}::${konu.konu}`, ders: d.ders, konu: konu.konu, no, deckId, items: konu.kazanimlar.map((k, i) => ({ k, no: i + 1 })) };
      });
      if (lessons.every((l) => l.no != null)) lessons.sort((a, b) => a.no! - b.no!);
      return { ders: d.ders, lessons };
    });
  }, [kurulData]);

  const searching = Boolean(searchQuery.trim());
  const narrowing = searching || kapsamFiltre !== 'all';

  // Süzme: ders + kapsam + arama (kazanım metni, konu, ders adı, sözlük terimi; Türkçe karakter duyarsız)
  const shownGroups = useMemo(() => {
    const terms = foldText(searchQuery.trim()).split(/\s+/).filter(Boolean);
    return groups
      .filter((g) => selectedDers === 'all' || g.ders === selectedDers)
      .map((g) => ({
        ders: g.ders,
        lessons: g.lessons
          .map((l) => {
            const head = foldText(`${l.konu} ${l.ders}`);
            const hits = l.items.filter(({ k }) => {
              if (kapsamFiltre !== 'all' && String(kapsamOf(k)) !== kapsamFiltre) return false;
              if (!terms.length) return true;
              const t = `${head} ${foldText(k.metin)} ${foldText(k.sozlukTerimleri.map((s) => s.term).join(' '))}`;
              return terms.every((w) => t.includes(w));
            });
            return { l, hits };
          })
          .filter((x) => x.hits.length > 0),
      }))
      .filter((g) => g.lessons.length > 0);
  }, [groups, selectedDers, searchQuery, kapsamFiltre]);

  const flat = useMemo(() => shownGroups.flatMap((g) => g.lessons), [shownGroups]);
  const totalFiltered = useMemo(() => flat.reduce((a, x) => a + x.hits.length, 0), [flat]);
  const kurulItems = useMemo(() => groups.flatMap((g) => g.lessons.flatMap((l) => l.items.map((x) => x.k))), [groups]);

  const current = useMemo(
    () => flat.find((x) => x.l.key === selectedKey) || (isPhone ? null : flat[0]) || null,
    [flat, selectedKey, isPhone],
  );
  const showDetail = !isPhone || (phoneDetail && current != null);
  // Süzgeç açık konuyu listeden düşürdüyse telefonda listeye dönülür
  useEffect(() => { if (!loading && phoneDetail && !current) setPhoneDetail(false); }, [loading, phoneDetail, current]);

  // Adres çubuğu: kurul + açık konu (geçmişe kayıt eklemez)
  useEffect(() => {
    if (loading) return;
    try {
      const p = new URLSearchParams();
      if (selectedKurul !== 1) p.set('kurul', String(selectedKurul));
      if (selectedKey && (phoneDetail || !isPhone)) p.set('konu', selectedKey);
      const qs = p.toString();
      const next = `${pathFor('kazanimlar')}${qs ? `?${qs}` : ''}`;
      if (`${window.location.pathname}${window.location.search}` !== next) window.history.replaceState(window.history.state, '', next);
    } catch { /* adres yazılamadıysa yalnız durum */ }
  }, [selectedKurul, selectedKey, phoneDetail, isPhone, loading]);

  const openLesson = useCallback((key: string) => {
    setSelectedKey(key);
    setOpenKz(null);
    setPhoneDetail(true);
    // Telefonda ayrıntı listenin yerine geçer: sayfanın başına; masaüstünde ayrıntı bölmesinin başına
    requestAnimationFrame(() => {
      const el = detailRef.current;
      if (!el) return;
      if (window.matchMedia?.('(max-width: 767px)').matches) window.scrollTo({ top: 0 });
      else if (el.getBoundingClientRect().top < 0) el.scrollIntoView({ block: 'start' });
    });
  }, []);

  const backToList = () => {
    const key = current?.l.key;
    setPhoneDetail(false);
    requestAnimationFrame(() => {
      if (key) document.querySelector(`[data-kz-lesson="${CSS.escape(key)}"]`)?.scrollIntoView({ block: 'center' });
    });
  };

  const clearAll = () => { setSearchQuery(''); setSelectedDers('all'); setKapsamFiltre('all'); };

  /* Hızlı haplar: Kurul · Ders · Kapsam */
  const dersCounts = useMemo(() => groups.map((g) => ({ ders: g.ders, n: g.lessons.reduce((a, l) => a + l.items.length, 0) })), [groups]);
  const kapsamCounts = useMemo(
    () => kapsamSay(groups.filter((g) => selectedDers === 'all' || g.ders === selectedDers).flatMap((g) => g.lessons.flatMap((l) => l.items.map((x) => x.k)))),
    [groups, selectedDers],
  );
  const quick: ToolbarQuick[] = [
    {
      id: 'kurul',
      label: 'Kurul',
      value: `Kurul ${selectedKurul}`,
      content: (close) => (
        <QuickOptions
          close={close}
          value={String(selectedKurul)}
          onPick={(id) => setSelectedKurul(Number(id))}
          options={[1, 2, 3, 4, 5, 6].map((k) => ({ id: String(k), label: `Kurul ${k}`, hint: KURUL_AD[k] }))}
        />
      ),
    },
    ...(dersCounts.length > 1 ? [{
      id: 'ders',
      label: 'Ders',
      wide: true,
      value: selectedDers !== 'all' ? selectedDers : undefined,
      onClear: () => setSelectedDers('all'),
      content: (close: () => void) => (
        <QuickOptions
          close={close}
          searchable={dersCounts.length > 8}
          placeholder="Ders ara"
          value={selectedDers}
          onPick={setSelectedDers}
          options={[{ id: 'all', label: 'Tüm dersler', count: kurulItems.length }, ...dersCounts.map((d) => ({ id: d.ders, label: d.ders, count: d.n }))]}
        />
      ),
    }] : []),
    {
      id: 'kapsam',
      label: 'Kapsam',
      value: kapsamFiltre !== 'all' ? KAPSAM_AD[Number(kapsamFiltre) as Kapsam] : undefined,
      onClear: () => setKapsamFiltre('all'),
      content: (close) => (
        <QuickOptions
          close={close}
          value={kapsamFiltre}
          onPick={(id) => setKapsamFiltre(id as KapsamFiltre)}
          options={[
            { id: 'all', label: 'Tüm kazanımlar', count: kapsamCounts[0] + kapsamCounts[1] + kapsamCounts[2] },
            { id: '2', label: 'Tam kapsam', hint: 'Desteye ve soruya bağlı', count: kapsamCounts[2] },
            { id: '1', label: 'Kısmi kapsam', hint: 'Yalnız deste ya da yalnız soru', count: kapsamCounts[1] },
            { id: '0', label: 'İçerik yok', hint: 'Henüz kaynak bağlanmamış', count: kapsamCounts[0] },
          ]}
        />
      ),
    },
  ];

  const kurulKapsam = useMemo(() => kapsamSay(kurulItems), [kurulItems]);

  return (
    <div className="kz-page o12-page o12-kz" ref={rootRef}>
      <PageToolbar
        title="Kazanımlar"
        count={kurulData && !loading
          ? `${flat.length} konu · ${totalFiltered.toLocaleString('tr-TR')} kazanım`
          : `Kurul ${selectedKurul}`}
        search={{ value: searchQuery, onChange: setSearchQuery, placeholder: 'Kazanım, konu, terim ara' }}
        quick={quick}
      />

      {loading ? (
        <div className="kz-body" aria-busy="true" aria-label={`Kurul ${selectedKurul} kazanımları yükleniyor`}>
          <div className="kz-nav">
            <div className="kz-skel-col" style={{ padding: '6px 6px 12px' }}>
              <span className="ui-skel" style={{ width: '55%', height: 12 }} />
              <span className="ui-skel" style={{ width: '100%', height: 6 }} />
            </div>
            {Array.from({ length: 8 }, (_, i) => (
              <div key={i} className="kz-skel-row">
                <span className="ui-skel" style={{ width: 22, height: 12 }} />
                <span className="kz-skel-col">
                  <span className="ui-skel" style={{ width: `${60 + ((i * 13) % 35)}%`, height: 12 }} />
                  <span className="ui-skel" style={{ width: 120, height: 5 }} />
                </span>
              </div>
            ))}
          </div>
          <div className="kz-detail is-skel">
            <span className="ui-skel" style={{ width: 160, height: 11 }} />
            <span className="ui-skel" style={{ width: '55%', height: 22 }} />
            <span className="ui-skel" style={{ width: '100%', height: 8 }} />
            {Array.from({ length: 5 }, (_, i) => <span key={i} className="ui-skel" style={{ height: 58, borderRadius: 12 }} />)}
          </div>
        </div>
      ) : loadError || !kurulData ? (
        <div className="kz-empty">
          <Compass aria-hidden />
          <b>Kurul {selectedKurul} kazanımları yüklenemedi</b>
          <p>Bağlantını kontrol edip yeniden dene.</p>
          <button type="button" className="ui-btn is-tonal is-sm" onClick={() => setReloadTick((n) => n + 1)}>
            <RotateCcw aria-hidden /> Yeniden dene
          </button>
        </div>
      ) : flat.length === 0 ? (
        <div className="kz-empty">
          <Compass aria-hidden />
          <b>Eşleşen kazanım yok</b>
          <p>{searching ? 'Kelimeyi kısalt ya da süzgeçleri kaldır.' : 'Bu süzgeçle eşleşen kazanım bulunmuyor.'}</p>
          <button type="button" className="ui-btn is-tonal is-sm" onClick={clearAll}>Süzgeçleri temizle</button>
        </div>
      ) : (
        <div className={`kz-body ${showDetail && isPhone ? 'is-phone-detail' : ''}`}>
          {/* Konu listesi: kurul özeti + derse göre gruplar */}
          {(!isPhone || !showDetail) && (
            <nav className="kz-nav" aria-label={`Kurul ${selectedKurul} konuları`}>
              <div className="kz-kurul">
                <p className="kz-kurul-t"><b>Kurul {selectedKurul}</b> {kurulData.name.replace(/\s*Kurulu$/, '')}</p>
                <Meter n={kurulKapsam} />
                <p className="kz-kurul-s">
                  {kurulItems.length.toLocaleString('tr-TR')} kazanım · <span className="kz-c2">%{pct(kurulKapsam[2], kurulItems.length)} tam kapsam</span>
                </p>
              </div>
              {shownGroups.map((g) => (
                <section key={g.ders} className="kz-group" aria-label={g.ders}>
                  <h3 className="kz-group-h">
                    <span>{g.ders}</span>
                    <span className="kz-group-n">{g.lessons.length}</span>
                  </h3>
                  <ul>
                    {g.lessons.map(({ l, hits }) => {
                      const on = current?.l.key === l.key;
                      const n = kapsamSay(l.items.map((x) => x.k));
                      return (
                        <li key={l.key}>
                          <button
                            type="button"
                            data-kz-lesson={l.key}
                            className={`kz-lesson ${on ? 'is-on' : ''}`}
                            aria-current={on && !isPhone ? 'true' : undefined}
                            onClick={() => openLesson(l.key)}
                          >
                            {l.no != null && <span className="kz-lesson-no" aria-label={`Ders ${l.no}`}>{l.no}</span>}
                            <span className="kz-lesson-main">
                              <span className="kz-lesson-t">{l.konu}</span>
                              <span className="kz-lesson-meta">
                                <Meter n={n} small />
                                <span className="kz-lesson-c">
                                  {narrowing ? `${hits.length}/${l.items.length}` : `${n[2]}/${l.items.length}`}
                                  <span className="sr-only">{narrowing ? ' kazanım eşleşti' : ' kazanım tam kapsamlı'}</span>
                                </span>
                              </span>
                            </span>
                            <ChevronRight className="kz-lesson-go" aria-hidden />
                          </button>
                        </li>
                      );
                    })}
                  </ul>
                </section>
              ))}
            </nav>
          )}

          {/* Konu ayrıntısı */}
          {showDetail && current && (
            <LessonDetail
              ref={detailRef}
              kurul={selectedKurul}
              lesson={current.l}
              hits={current.hits}
              narrowing={narrowing}
              onClearNarrowing={() => { setSearchQuery(''); setKapsamFiltre('all'); }}
              isPhone={isPhone}
              onBack={backToList}
              openKz={openKz}
              setOpenKz={setOpenKz}
              questionMap={questionMap}
              spot={current.l.deckId ? spots?.get(current.l.deckId) : undefined}
              ornekAnswers={ornekAnswers}
              setOrnekAnswer={(id, key) => setOrnekAnswers((p) => ({ ...p, [id]: key }))}
              onNavigateToLearn={onNavigateToLearn}
              onNavigateToPastExams={onNavigateToPastExams}
              onNavigateToOrnek={onNavigateToOrnek}
            />
          )}
        </div>
      )}
    </div>
  );
};

const pct = (a: number, b: number) => (b ? Math.round((a / b) * 100) : 0);

/** Kapsam çubuğu: tam · kısmi · yok oranları (renk + metin alternatifi) */
const Meter: React.FC<{ n: [number, number, number]; small?: boolean }> = ({ n, small }) => {
  const total = n[0] + n[1] + n[2];
  return (
    <span className={`kz-meter ${small ? 'is-sm' : ''}`} role="img" aria-label={`${total} kazanımdan ${n[2]} tam, ${n[1]} kısmi, ${n[0]} içerik yok`}>
      {total > 0 && (
        <>
          {n[2] > 0 && <i className="is-2" style={{ flexGrow: n[2] }} />}
          {n[1] > 0 && <i className="is-1" style={{ flexGrow: n[1] }} />}
          {n[0] > 0 && <i className="is-0" style={{ flexGrow: n[0] }} />}
        </>
      )}
    </span>
  );
};

interface DetailProps {
  kurul: number;
  lesson: Ders;
  hits: Array<{ k: KazanimItem; no: number }>;
  narrowing: boolean;
  onClearNarrowing: () => void;
  isPhone: boolean;
  onBack: () => void;
  openKz: string | null;
  setOpenKz: React.Dispatch<React.SetStateAction<string | null>>;
  questionMap: Record<string, { cikmisSorular?: KazanimItem['cikmisSorular']; ornekSorular?: KazanimItem['ornekSorular'] }> | null;
  spot?: SpotOzet;
  ornekAnswers: Record<string, string>;
  setOrnekAnswer: (id: string, key: string) => void;
  onNavigateToLearn?: Props['onNavigateToLearn'];
  onNavigateToPastExams?: Props['onNavigateToPastExams'];
  onNavigateToOrnek?: Props['onNavigateToOrnek'];
}

const LessonDetail = React.forwardRef<HTMLElement, DetailProps>(function LessonDetail({
  kurul, lesson, hits, narrowing, onClearNarrowing, isPhone, onBack, openKz, setOpenKz, questionMap, spot, ornekAnswers, setOrnekAnswer,
  onNavigateToLearn, onNavigateToPastExams, onNavigateToOrnek,
}, ref) {
  const all = lesson.items.map((x) => x.k);
  const n = kapsamSay(all);
  const hasOrnek = all.some((k) => ornekSayisi(k) > 0);
  const hasCikmis = all.some((k) => cikmisSayisi(k) > 0);

  return (
    <section className="kz-detail" ref={ref} aria-labelledby="kz-detail-h">
      {isPhone && (
        <button type="button" className="kz-back" onClick={onBack}>
          <ChevronLeft aria-hidden /> Dersler
        </button>
      )}
      <header className="kz-dh">
        <p className="kz-crumb">
          <span>Kurul {kurul}</span>
          <ChevronRight aria-hidden />
          <span>{lesson.ders}</span>
          {lesson.no != null && <><ChevronRight aria-hidden /><span>Ders {lesson.no}</span></>}
        </p>
        <h2 id="kz-detail-h">{lesson.konu}</h2>

        <div className="kz-sum">
          <Meter n={n} />
          <p className="kz-sum-t">
            <span><b>{all.length}</b> kazanım</span>
            {([2, 1, 0] as Kapsam[]).filter((c) => n[c] > 0).map((c) => (
              <span key={c} className="kz-sum-i"><i className={`kz-lv is-${c}`} aria-hidden />{n[c]} {KAPSAM_KISA[c]}</span>
            ))}
          </p>
          <p className="kz-sum-note">Tam: desteye ve soruya bağlı · Kısmi: yalnız biri · İçerik yok: kaynak bağlanmamış</p>
        </div>

        <div className="kz-acts">
          {onNavigateToLearn && lesson.deckId && (
            <button type="button" className="ui-btn is-tonal is-sm" onClick={() => onNavigateToLearn(lesson.deckId)}>
              <GraduationCap aria-hidden /> Öğren'de aç
            </button>
          )}
          {onNavigateToOrnek && hasOrnek && (
            <button type="button" className="ui-btn is-ghost is-sm" onClick={() => onNavigateToOrnek(lesson.deckId)}>
              <Target aria-hidden /> Örnek sorular
            </button>
          )}
          {onNavigateToPastExams && hasCikmis && (
            <button type="button" className="ui-btn is-ghost is-sm" onClick={() => onNavigateToPastExams(lesson.konu)}>
              <Archive aria-hidden /> Çıkmış sorular
            </button>
          )}
          {spot && (
            <button type="button" className="ui-btn is-ghost is-sm" onClick={() => navigateTo(`${pathFor('spots')}?id=${encodeURIComponent(spot.ilk)}`)}>
              <Zap aria-hidden /> Sınav spotları · {spot.n}
            </button>
          )}
        </div>
      </header>

      {narrowing && hits.length < lesson.items.length && (
        <p className="kz-narrow" role="status">
          {lesson.items.length} kazanımdan <b>{hits.length}</b> tanesi gösteriliyor.
          <button type="button" onClick={onClearNarrowing}>Tümünü göster</button>
        </p>
      )}

      <ol className="kz-rows">
        {hits.map(({ k, no }) => {
          const qExtra = openKz === k.id && questionMap ? questionMap[k.id] : undefined;
          const mergedK = qExtra
            ? {
                ...k,
                cikmisSorular: qExtra.cikmisSorular || k.cikmisSorular,
                ornekSorular: qExtra.ornekSorular || k.ornekSorular,
              }
            : k;
          return (
            <KazanimRow
              key={k.id || no}
              k={mergedK}
              no={no}
              konu={lesson.konu}
              open={openKz === k.id}
              onToggle={() => setOpenKz((cur) => (cur === k.id ? null : k.id))}
              ornekAnswers={ornekAnswers}
              setOrnekAnswer={setOrnekAnswer}
              onNavigateToLearn={onNavigateToLearn}
              onNavigateToPastExams={onNavigateToPastExams}
              onNavigateToOrnek={onNavigateToOrnek}
            />
          );
        })}
      </ol>
    </section>
  );
});

type SrcKind = 'slayt' | 'ozet' | 'sozluk' | 'cikmis' | 'ornek';
const SRC_META: Record<SrcKind, { label: string; icon: React.ElementType }> = {
  slayt: { label: 'Slayt', icon: Presentation },
  ozet: { label: 'Özet', icon: Sparkles },
  sozluk: { label: 'Sözlük', icon: BookOpenText },
  cikmis: { label: 'Çıkmış', icon: Archive },
  ornek: { label: 'Örnek soru', icon: Target },
};
const srcCounts = (k: KazanimItem): Array<[SrcKind, number]> => ([
  ['slayt', k.slaytlar.length],
  ['ozet', k.ozetler.length],
  ['sozluk', k.sozlukTerimleri.length],
  ['cikmis', cikmisSayisi(k)],
  ['ornek', ornekSayisi(k)],
] as Array<[SrcKind, number]>).filter(([, n]) => n > 0);

const KazanimRow: React.FC<{
  k: KazanimItem;
  no: number;
  konu: string;
  open: boolean;
  onToggle: () => void;
  ornekAnswers: Record<string, string>;
  setOrnekAnswer: (id: string, key: string) => void;
  onNavigateToLearn?: Props['onNavigateToLearn'];
  onNavigateToPastExams?: Props['onNavigateToPastExams'];
  onNavigateToOrnek?: Props['onNavigateToOrnek'];
}> = ({ k, no, konu, open, onToggle, ...rest }) => {
  const level = kapsamOf(k);
  const counts = srcCounts(k);
  const panelId = `kz-p-${k.id}`;
  const hasAny = counts.length > 0;
  return (
    <li className={`kz-row ${open ? 'is-open' : ''}`} data-auto-reveal>
      <button
        type="button"
        className="kz-row-head"
        aria-expanded={hasAny ? open : undefined}
        aria-controls={hasAny ? panelId : undefined}
        disabled={!hasAny}
        onClick={onToggle}
      >
        <span className={`kz-num is-${level}`} title={KAPSAM_AD[level]}>
          {no}
          <span className="sr-only">. kazanım, {KAPSAM_AD[level]}: </span>
        </span>
        <span className="kz-row-body">
          <span className="kz-row-t">{k.metin}</span>
          <span className="kz-row-src">
            {hasAny
              ? counts.map(([s, n]) => {
                const Icon = SRC_META[s].icon;
                return <span key={s}><Icon aria-hidden />{SRC_META[s].label} {n}</span>;
              })
              : <span className="is-none">Henüz kaynak bağlanmamış</span>}
          </span>
        </span>
        {hasAny && <ChevronDown className="kz-row-chev" aria-hidden />}
      </button>
      {open && hasAny && (
        <div id={panelId} className="kz-panel">
          <Kaynaklar k={k} no={no} konu={konu} {...rest} />
        </div>
      )}
    </li>
  );
};

/** Bir grubun önizleme sınırı; fazlası "n tane daha" ile açılır */
const PREVIEW = 3;

const Group: React.FC<{
  kind: SrcKind;
  n: number;
  action?: { label: string; onClick: () => void };
  /** Önizlenebilir öge sayısı (örnek soruda gömülü olanlar toplamdan az olabilir) */
  listN?: number;
  children: (limit: number | undefined) => React.ReactNode;
}> = ({ kind, n, listN = n, action, children }) => {
  const [all, setAll] = useState(false);
  const Icon = SRC_META[kind].icon;
  const limit = all ? undefined : PREVIEW;
  return (
    <section className="kz-sg" aria-label={`${SRC_META[kind].label} (${n})`}>
      <header className="kz-sg-h">
        <Icon aria-hidden />
        <b>{SRC_META[kind].label}</b>
        <span className="kz-sg-n">{n}</span>
        {action && (
          <button type="button" className="kz-sg-go" onClick={action.onClick}>
            {action.label} <ArrowUpRight aria-hidden />
          </button>
        )}
      </header>
      {children(limit)}
      {!all && listN > PREVIEW && (
        <button type="button" className="kz-sg-more" onClick={() => setAll(true)}>{listN - PREVIEW} tane daha göster</button>
      )}
    </section>
  );
};

/** Kazanıma bağlı kaynaklar: gruplar hâlinde, her grupta sayı + doğrudan açma eylemi */
const Kaynaklar: React.FC<{
  k: KazanimItem;
  no: number;
  konu: string;
  ornekAnswers: Record<string, string>;
  setOrnekAnswer: (id: string, key: string) => void;
  onNavigateToLearn?: Props['onNavigateToLearn'];
  onNavigateToPastExams?: Props['onNavigateToPastExams'];
  onNavigateToOrnek?: Props['onNavigateToOrnek'];
}> = ({ k, no, konu, ornekAnswers, setOrnekAnswer, onNavigateToLearn, onNavigateToPastExams, onNavigateToOrnek }) => {
  const firstDeck = k.slaytlar.find((s) => s.deckId);
  const cikmisN = cikmisSayisi(k);
  const ornekN = ornekSayisi(k);
  return (
    <div className="kz-src">
      {k.slaytlar.length > 0 && (
        <Group
          kind="slayt"
          n={k.slaytlar.length}
          action={onNavigateToLearn && firstDeck ? { label: "Öğren'de aç", onClick: () => onNavigateToLearn(firstDeck.deckId, firstDeck.sayfa) } : undefined}
        >
          {(limit) => (
            <ul className="kz-links">
              {k.slaytlar.slice(0, limit).map((sl, i) => (
                <li key={i}>
                  {onNavigateToLearn ? (
                    <button type="button" className="kz-link" onClick={() => onNavigateToLearn(sl.deckId, sl.sayfa)} title="Öğren modunda bu sayfayı aç">
                      <span className="kz-link-main">
                        <span className="kz-link-t">{sl.kaynak}</span>
                        {sl.alinti && <span className="kz-link-s">{sl.alinti}</span>}
                      </span>
                      <span className="kz-link-p">s. {sl.sayfa}<ChevronRight aria-hidden /></span>
                    </button>
                  ) : (
                    <div className="kz-link">
                      <span className="kz-link-main">
                        <span className="kz-link-t">{sl.kaynak}</span>
                        {sl.alinti && <span className="kz-link-s">{sl.alinti}</span>}
                      </span>
                      <span className="kz-link-p">s. {sl.sayfa}</span>
                    </div>
                  )}
                </li>
              ))}
            </ul>
          )}
        </Group>
      )}

      {k.ozetler.length > 0 && (
        <Group kind="ozet" n={k.ozetler.length}>
          {(limit) => <ul className="kz-bullets">{k.ozetler.slice(0, limit).map((b, i) => <li key={i}>{b}</li>)}</ul>}
        </Group>
      )}

      {k.sozlukTerimleri.length > 0 && (
        <Group kind="sozluk" n={k.sozlukTerimleri.length}>
          {(limit) => (
            <dl className="kz-terms">
              {k.sozlukTerimleri.slice(0, limit).map((t, i) => (
                <div key={i}>
                  <dt>{t.term}</dt>
                  <dd>{t.definition}{t.pearl && <span className="kz-pearl">{t.pearl}</span>}</dd>
                </div>
              ))}
            </dl>
          )}
        </Group>
      )}

      {cikmisN > 0 && (
        <Group
          kind="cikmis"
          n={cikmisN}
          listN={(k.cikmisSorular || []).length}
          action={onNavigateToPastExams ? { label: "Çıkmış'ta aç", onClick: () => onNavigateToPastExams(konu) } : undefined}
        >
          {(limit) => (
            <ul className="kz-qs">
              {(k.cikmisSorular || []).slice(0, limit).map((q) => (
                <li key={q.id} className="kz-q">
                  <p className="kz-q-meta">
                    <b>{q.year || 'Arşiv'}</b>{q.questionNumber ? ` · Soru ${q.questionNumber}` : ''}
                    {q.correctAnswer && <span className="kz-q-ok">Doğru: {q.correctAnswer}</span>}
                  </p>
                  <p className="kz-q-stem">{q.stem}</p>
                  {q.options?.length > 0 && (
                    <ul className="kz-opts">
                      {q.options.map((opt) => (
                        <li key={opt.key} className={opt.key === q.correctAnswer ? 'is-ok' : ''}>
                          <b>{opt.key})</b> <span>{opt.text}</span>
                        </li>
                      ))}
                    </ul>
                  )}
                  {q.explanation && (
                    <details className="kz-x">
                      <summary>Açıklama</summary>
                      <p>{q.explanation}</p>
                    </details>
                  )}
                </li>
              ))}
            </ul>
          )}
        </Group>
      )}

      {ornekN > 0 && (
        <Group
          kind="ornek"
          n={ornekN}
          listN={(k.ornekSorular || []).length}
          action={onNavigateToOrnek ? {
            label: 'Örnek sorularda çöz',
            onClick: () => onNavigateToOrnek(firstDeck?.deckId, k.firstOrnekKazanimNo || k.ornekSorular?.[0]?.kazanimNo || no),
          } : undefined}
        >
          {(limit) => (
            <ul className="kz-qs">
              {(k.ornekSorular || []).slice(0, limit).map((oq) => {
                const pick = ornekAnswers[oq.id];
                const solved = Boolean(pick);
                const right = pick === oq.dogru;
                return (
                  <li key={oq.id} className="kz-q">
                    <p className="kz-q-meta">
                      <span className="kz-q-tag">{oq.zorluk || 'Standart'}</span>
                      {solved && <span className={right ? 'kz-q-ok' : 'kz-q-bad'}>{right ? 'Doğru' : `Doğru yanıt: ${oq.dogru}`}</span>}
                    </p>
                    <p className="kz-q-stem">{oq.soru}</p>
                    <div className="kz-choices" role="group" aria-label="Seçenekler">
                      {Object.entries(oq.secenekler || {}).map(([key, text]) => {
                        const state = solved ? (key === oq.dogru ? 'is-ok' : pick === key ? 'is-bad' : '') : '';
                        return (
                          <button key={key} type="button" disabled={solved} className={`kz-choice ${state}`} onClick={() => setOrnekAnswer(oq.id, key)}>
                            <b>{key})</b> <span>{text}</span>
                          </button>
                        );
                      })}
                    </div>
                    {solved && oq.aciklama && <p className="kz-q-x"><b>Açıklama:</b> {oq.aciklama}</p>}
                  </li>
                );
              })}
            </ul>
          )}
        </Group>
      )}
    </div>
  );
};
