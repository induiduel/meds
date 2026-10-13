import React, { useState, useEffect, useMemo, useRef, useCallback } from 'react';
import {
  Archive,
  BookOpenText,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  Compass,
  ExternalLink,
  GraduationCap,
  Presentation,
  Sparkles,
  Target,
  Zap,
} from 'lucide-react';
import { PageToolbar, FilterPills, type ToolbarChip } from './ui/PageToolbar';
import { foldText } from '../services/searchText';
import { navigateTo, pathFor } from '../router';
import './kazanimlar.css';

/**
 * Kazanımlar (v10 kompakt) — ders listesi + ders ayrıntısı.
 *  - Sol: kurulun dersleri (konu = ders saati); her satırda kazanım başına küçük kapsam hücresi.
 *  - Sağ: ders başlığı + kazanım satırları (kapsam noktası · metin · Deste / Soru / Özet etiketleri).
 *    Satıra dokununca bağlı kaynaklar (slayt, çıkmış, örnek soru, sözlük, özet) aynı satırın altında açılır.
 *  - Kapsam: tam = desteye (slayt) ve soruya (çıkmış ya da örnek) bağlı; kısmi = ikisinden biri; yok = hiçbiri.
 *  - Telefon (<768): önce ders listesi, derse dokununca ayrıntı (geri düğmesiyle listeye dönülür), tek sütun.
 * Sınıf öneki `kz-` (styles: components/kazanimlar.css); başka ekranın sınıflarıyla çakışmaz.
 */

interface KazanimItem {
  id: string;
  metin: string;
  totalOrnekCount?: number;
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
  sozlukTerimleri: Array<{
    term: string;
    definition: string;
    pearl?: string;
  }>;
  ozetler: string[];
}

interface KonuGroup {
  konu: string;
  kazanimlar: KazanimItem[];
}

interface DersGroup {
  ders: string;
  count: number;
  konular: KonuGroup[];
}

interface KurulData {
  kurul: number;
  name: string;
  totalCount: number;
  dersler: DersGroup[];
}

/** Sınav spotları (yalnız Kurul 1): ders → spot sayısı ve ilk spot (derin bağlantı için) */
interface SpotOzet { n: number; ilk: string }

const loaders: Record<number, () => Promise<{ default: any }>> = {
  1: () => import('../data/kazanimlar/k1.json'),
  2: () => import('../data/kazanimlar/k2.json'),
  3: () => import('../data/kazanimlar/k3.json'),
  4: () => import('../data/kazanimlar/k4.json'),
  5: () => import('../data/kazanimlar/k5.json'),
  6: () => import('../data/kazanimlar/k6.json'),
};

interface Props {
  onNavigateToLearn?: (deckId?: string, slideNumber?: number) => void;
  onNavigateToPastExams?: (query?: string) => void;
  onNavigateToOrnek?: (lessonId?: string, kazanimNo?: number) => void;
}

type Kapsam = 0 | 1 | 2;
type KaynakSekme = 'slayt' | 'cikmis' | 'ornek' | 'sozluk' | 'ozet';

/** Ders (konu) satırı: kazanımlar asıl sırasıyla (örnek soru numarası için `no`) */
interface Ders {
  key: string;
  ders: string;
  konu: string;
  no: number | null;
  deckId?: string;
  items: Array<{ k: KazanimItem; no: number }>;
}

const ornekSayisi = (k: KazanimItem) => k.totalOrnekCount ?? (k.ornekSorular ? k.ornekSorular.length : 0);
const desteVar = (k: KazanimItem) => k.slaytlar.length > 0;
const soruVar = (k: KazanimItem) => k.cikmisSorular.length > 0 || ornekSayisi(k) > 0;
const ozetVar = (k: KazanimItem) => k.ozetler.length > 0;
const kapsamOf = (k: KazanimItem): Kapsam => {
  const n = Number(desteVar(k)) + Number(soruVar(k));
  return n as Kapsam;
};
const KAPSAM_AD: Record<Kapsam, string> = { 2: 'Tam kapsam', 1: 'Kısmi kapsam', 0: 'İçerik yok' };

/** Destenin numarası: "k1-03-hucresel-adaptasyonlar" → 3 (konudaki en sık deste) */
function desteBilgisi(konu: KonuGroup): { no: number | null; deckId?: string } {
  const say = new Map<string, number>();
  for (const k of konu.kazanimlar) for (const s of k.slaytlar) if (s.deckId) say.set(s.deckId, (say.get(s.deckId) || 0) + 1);
  const deckId = [...say.entries()].sort((a, b) => b[1] - a[1])[0]?.[0];
  const m = deckId?.match(/^k\d+-(\d+)-/);
  return { no: m ? parseInt(m[1], 10) : null, deckId };
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

export const KazanimlarView: React.FC<Props> = ({
  onNavigateToLearn,
  onNavigateToPastExams,
  onNavigateToOrnek,
}) => {
  const [selectedKurul, setSelectedKurul] = useState<number>(1);
  const [selectedDers, setSelectedDers] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [kurulData, setKurulData] = useState<KurulData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [spots, setSpots] = useState<Map<string, SpotOzet> | null>(null);

  const [selectedKey, setSelectedKey] = useState<string | null>(null);
  /** Telefonda ders ayrıntısı açık mı (liste ↔ ayrıntı yığını) */
  const [phoneDetail, setPhoneDetail] = useState(false);
  const [openKz, setOpenKz] = useState<string | null>(null);
  const [activeTabByKazanim, setActiveTabByKazanim] = useState<Record<string, KaynakSekme>>({});
  // Örnek soruların çözüm durumu
  const [ornekAnswers, setOrnekAnswers] = useState<Record<string, string>>({});

  const isPhone = useMedia('(max-width: 767px)');
  const rootRef = useRef<HTMLDivElement>(null);
  const detailRef = useRef<HTMLElement>(null);

  useEffect(() => {
    let alive = true;
    setLoading(true);
    setSelectedDers('all');
    setSelectedKey(null);
    setPhoneDetail(false);
    setOpenKz(null);
    const loader = loaders[selectedKurul];
    if (loader) {
      loader()
        .then((m) => {
          if (alive) {
            setKurulData(m ? (m.default || m) : null);
            setLoading(false);
          }
        })
        .catch(() => {
          if (alive) setLoading(false);
        });
    }
    return () => {
      alive = false;
    };
  }, [selectedKurul]);

  // Sınav spotları yalnız Kurul 1'de var: deste kimliğine göre ders başına sayı (kazanım verisinden sonra yüklenir)
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

  // Üst çubuğun yüksekliği: masaüstünde ders listesi bunun altına yapışır
  useEffect(() => {
    const root = rootRef.current;
    const bar = root?.querySelector('.pt-root') as HTMLElement | null;
    if (!root || !bar || typeof ResizeObserver === 'undefined') return;
    const ro = new ResizeObserver(() => root.style.setProperty('--kz-bar', `${Math.round(bar.getBoundingClientRect().height)}px`));
    ro.observe(bar);
    return () => ro.disconnect();
  }, []);

  const dersList = useMemo(() => {
    if (!kurulData) return [];
    return kurulData.dersler.map((d) => ({ ders: d.ders, count: d.count }));
  }, [kurulData]);

  // Tüm dersler (konu = ders saati), deste numarasına göre sıralı
  const allLessons = useMemo<Ders[]>(() => {
    if (!kurulData) return [];
    const out: Ders[] = [];
    for (const d of kurulData.dersler) {
      for (const konu of d.konular) {
        const { no, deckId } = desteBilgisi(konu);
        out.push({ key: `${d.ders}::${konu.konu}`, ders: d.ders, konu: konu.konu, no, deckId, items: konu.kazanimlar.map((k, i) => ({ k, no: i + 1 })) });
      }
    }
    if (out.every((l) => l.no != null)) out.sort((a, b) => (a.no! - b.no!) || a.konu.localeCompare(b.konu, 'tr'));
    return out;
  }, [kurulData]);

  // Süzme: ders süzgeci + arama (kazanım metni, konu, ders adı, sözlük terimi; Türkçe karakter duyarsız)
  const lessons = useMemo(() => {
    const q = foldText(searchQuery.trim());
    const terms = q.split(/\s+/).filter(Boolean);
    return allLessons
      .filter((l) => selectedDers === 'all' || l.ders === selectedDers)
      .map((l) => {
        if (!terms.length) return { l, hits: l.items };
        const head = foldText(`${l.konu} ${l.ders}`);
        const hits = l.items.filter(({ k }) => {
          const t = `${head} ${foldText(k.metin)} ${foldText(k.sozlukTerimleri.map((s) => s.term).join(' '))}`;
          return terms.every((w) => t.includes(w));
        });
        return { l, hits };
      })
      .filter((x) => x.hits.length > 0);
  }, [allLessons, selectedDers, searchQuery]);

  const totalFilteredCount = useMemo(() => lessons.reduce((a, x) => a + x.hits.length, 0), [lessons]);

  const current = useMemo(
    () => lessons.find((x) => x.l.key === selectedKey) || (isPhone ? null : lessons[0]) || null,
    [lessons, selectedKey, isPhone],
  );
  const showDetail = !isPhone || (phoneDetail && current != null);
  // Arama/süzgeç açık dersi listeden düşürdüyse telefonda liste görünümüne dönülür
  useEffect(() => { if (phoneDetail && !current) setPhoneDetail(false); }, [phoneDetail, current]);

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

  const toggleKz = (k: KazanimItem) => {
    setOpenKz((cur) => (cur === k.id ? null : k.id));
    setActiveTabByKazanim((prev) => {
      if (prev[k.id]) return prev;
      const first: KaynakSekme | undefined = k.slaytlar.length ? 'slayt' : k.cikmisSorular.length ? 'cikmis' : ornekSayisi(k) ? 'ornek' : k.sozlukTerimleri.length ? 'sozluk' : k.ozetler.length ? 'ozet' : undefined;
      return first ? { ...prev, [k.id]: first } : prev;
    });
  };

  const chips: ToolbarChip[] = selectedDers !== 'all' ? [{ id: 'ders', label: selectedDers, onRemove: () => setSelectedDers('all') }] : [];

  const legend = (
    <span className="kz-legend" aria-label="Kapsam açıklaması">
      <span><i className="kz-lv is-2" aria-hidden />Tam kapsam</span>
      <span><i className="kz-lv is-1" aria-hidden />Kısmi</span>
      <span><i className="kz-lv is-0" aria-hidden />İçerik yok</span>
    </span>
  );

  return (
    <div className="kz-page" ref={rootRef}>
      <PageToolbar
        title="Kazanımlar"
        count={kurulData && !loading ? `Kurul ${selectedKurul} · ${lessons.length} ders · ${totalFilteredCount.toLocaleString('tr-TR')} kazanım` : `Kurul ${selectedKurul}`}
        search={{ value: searchQuery, onChange: setSearchQuery, placeholder: 'Kazanım, konu, terim ara' }}
        segments={{
          label: 'Kurul seçimi',
          value: String(selectedKurul),
          onChange: (v) => setSelectedKurul(Number(v)),
          options: [1, 2, 3, 4, 5, 6].map((k) => ({ id: String(k), label: `Kurul ${k}` })),
        }}
        filters={dersList.length > 1 ? (
          <FilterPills
            label="Ders"
            value={selectedDers}
            onChange={setSelectedDers}
            options={[{ id: 'all', label: 'Tüm dersler', count: kurulData?.totalCount || 0 }, ...dersList.map((d) => ({ id: d.ders, label: d.ders, count: d.count }))]}
          />
        ) : undefined}
        filterCount={selectedDers !== 'all' ? 1 : 0}
        filterTitle="Kazanım süzgeci"
        chips={chips}
        tools={<span className="kz-legend-top">{legend}</span>}
      >
        <div className="kz-legend-sub">{legend}</div>
      </PageToolbar>

      {loading ? (
        <div className="kz-body" aria-busy="true" aria-label={`Kurul ${selectedKurul} kazanımları yükleniyor`}>
          <div className="kz-nav">
            {Array.from({ length: 8 }, (_, i) => (
              <div key={i} className="kz-skel-row"><span className="ui-skel" style={{ width: 22, height: 12 }} /><span className="kz-skel-col"><span className="ui-skel" style={{ width: `${60 + ((i * 13) % 35)}%`, height: 12 }} /><span className="ui-skel" style={{ width: 90, height: 6 }} /></span></div>
            ))}
          </div>
          <div className="kz-detail is-skel">
            <span className="ui-skel" style={{ width: 140, height: 12 }} />
            <span className="ui-skel" style={{ width: '50%', height: 20 }} />
            {Array.from({ length: 5 }, (_, i) => <span key={i} className="ui-skel" style={{ height: 52, borderRadius: 12 }} />)}
          </div>
        </div>
      ) : lessons.length === 0 ? (
        <div className="kz-empty">
          <Compass aria-hidden />
          <b>Eşleşen kazanım yok</b>
          <p>Kelimeyi kısalt ya da ders süzgecini kaldır.</p>
          <button type="button" className="ui-btn is-tonal is-sm" onClick={() => { setSearchQuery(''); setSelectedDers('all'); }}>Süzgeçleri temizle</button>
        </div>
      ) : (
        <div className={`kz-body ${showDetail && isPhone ? 'is-phone-detail' : ''}`}>
          {/* Ders listesi */}
          {(!isPhone || !showDetail) && (
            <nav className="kz-nav" aria-label="Dersler">
              {kurulData?.name && <p className="kz-nav-h">{kurulData.name}</p>}
              <ul>
                {lessons.map(({ l, hits }) => {
                  const on = current?.l.key === l.key;
                  const searching = Boolean(searchQuery.trim());
                  const tam = l.items.filter(({ k }) => kapsamOf(k) === 2).length;
                  return (
                    <li key={l.key}>
                      <button
                        type="button"
                        data-kz-lesson={l.key}
                        className={`kz-lesson ${on ? 'is-on' : ''}`}
                        aria-current={on && !isPhone ? 'true' : undefined}
                        onClick={() => openLesson(l.key)}
                        title={`${l.ders} · ${l.konu}`}
                      >
                        <span className="kz-lesson-no">{l.no ?? '·'}</span>
                        <span className="kz-lesson-main">
                          <span className="kz-lesson-t">{l.konu}</span>
                          <span className="kz-cells" aria-label={`${l.items.length} kazanımdan ${tam} tanesi tam kapsamlı`}>
                            {l.items.map(({ k }) => <i key={k.id} className={`kz-cell is-${kapsamOf(k)}`} />)}
                          </span>
                        </span>
                        {searching ? <span className="kz-lesson-n">{hits.length}</span> : null}
                        <ChevronRight className="kz-lesson-go" aria-hidden />
                      </button>
                    </li>
                  );
                })}
              </ul>
            </nav>
          )}

          {/* Ders ayrıntısı */}
          {showDetail && current && (
            <section className="kz-detail" ref={detailRef} aria-labelledby="kz-detail-h">
              {isPhone && (
                <button type="button" className="kz-back" onClick={backToList}>
                  <ChevronLeft aria-hidden /> Dersler
                </button>
              )}
              <header className="kz-dh">
                <div className="kz-dh-main">
                  <span className="kz-dh-sub">{current.l.no != null ? `Ders ${current.l.no} · ` : ''}{current.l.ders}</span>
                  <h2 id="kz-detail-h">{current.l.konu}</h2>
                  <KapsamOzeti items={current.l.items.map((x) => x.k)} />
                </div>
                <div className="kz-dh-acts">
                  {onNavigateToLearn && current.l.deckId && (
                    <button type="button" className="ui-btn is-tonal is-sm" onClick={() => onNavigateToLearn(current.l.deckId)}>
                      <GraduationCap aria-hidden /> Öğren'de aç
                    </button>
                  )}
                  {onNavigateToOrnek && current.l.items.some(({ k }) => ornekSayisi(k) > 0) && (
                    <button type="button" className="ui-btn is-ghost is-sm" onClick={() => onNavigateToOrnek(current.l.deckId)}>
                      <Target aria-hidden /> Örnek sorular
                    </button>
                  )}
                  {current.l.deckId && spots?.get(current.l.deckId) && (
                    <button type="button" className="ui-btn is-ghost is-sm" onClick={() => navigateTo(`${pathFor('spots')}?id=${encodeURIComponent(spots.get(current.l.deckId!)!.ilk)}`)}>
                      <Zap aria-hidden /> Sınav spotları · {spots.get(current.l.deckId)!.n}
                    </button>
                  )}
                </div>
              </header>

              <ol className="kz-rows">
                {current.hits.map(({ k: kazanim, no }) => {
                  const level = kapsamOf(kazanim);
                  const isOpen = openKz === kazanim.id;
                  const hasAny = kazanim.slaytlar.length + kazanim.cikmisSorular.length + ornekSayisi(kazanim) + kazanim.sozlukTerimleri.length + kazanim.ozetler.length > 0;
                  const panelId = `kz-p-${kazanim.id}`;
                  return (
                    <li key={kazanim.id || no} className={`kz-row ${isOpen ? 'is-open' : ''}`} data-auto-reveal>
                      <button
                        type="button"
                        className="kz-row-head"
                        aria-expanded={hasAny ? isOpen : undefined}
                        aria-controls={hasAny ? panelId : undefined}
                        disabled={!hasAny}
                        onClick={() => toggleKz(kazanim)}
                      >
                        <i className={`kz-dot is-${level}`} aria-hidden />
                        <span className="sr-only">{KAPSAM_AD[level]}. </span>
                        <span className="kz-row-no" aria-hidden>{no}</span>
                        <span className="kz-row-t">{kazanim.metin}</span>
                        <span className="kz-tags">
                          <Tag on={desteVar(kazanim)}>Deste</Tag>
                          <Tag on={soruVar(kazanim)}>Soru</Tag>
                          <Tag on={ozetVar(kazanim)}>Özet</Tag>
                        </span>
                        {hasAny && <ChevronDown className="kz-row-chev" aria-hidden />}
                      </button>
                      {isOpen && (
                        <div id={panelId} className="kz-panel">
                          <KaynakPaneli
                            kazanim={kazanim}
                            no={no}
                            konu={current.l.konu}
                            tab={activeTabByKazanim[kazanim.id]}
                            setTab={(t) => setActiveTabByKazanim((p) => ({ ...p, [kazanim.id]: t }))}
                            ornekAnswers={ornekAnswers}
                            setOrnekAnswer={(id, key) => setOrnekAnswers((p) => ({ ...p, [id]: key }))}
                            onNavigateToLearn={onNavigateToLearn}
                            onNavigateToPastExams={onNavigateToPastExams}
                            onNavigateToOrnek={onNavigateToOrnek}
                          />
                        </div>
                      )}
                    </li>
                  );
                })}
              </ol>
            </section>
          )}
        </div>
      )}
    </div>
  );
};

const Tag: React.FC<{ on: boolean; children: React.ReactNode }> = ({ on, children }) => (
  <span className={`kz-tag ${on ? 'is-on' : 'is-off'}`}>
    {children}
    <span className="sr-only">{on ? ' var' : ' yok'}</span>
  </span>
);

const KapsamOzeti: React.FC<{ items: KazanimItem[] }> = ({ items }) => {
  const n = [0, 0, 0];
  for (const k of items) n[kapsamOf(k)] += 1;
  return (
    <p className="kz-dh-meta">
      <b>{items.length}</b> kazanım
      {n[2] > 0 && <> · <span className="kz-c2">{n[2]} tam</span></>}
      {n[1] > 0 && <> · <span className="kz-c1">{n[1]} kısmi</span></>}
      {n[0] > 0 && <> · <span className="kz-c0">{n[0]} içerik yok</span></>}
    </p>
  );
};

/** Kazanıma bağlı kaynaklar: sekmeli; içerik eski görünümle aynı (slayta git, çıkmış, örnek soru çöz, sözlük, özet) */
const KaynakPaneli: React.FC<{
  kazanim: KazanimItem;
  no: number;
  konu: string;
  tab?: KaynakSekme;
  setTab: (t: KaynakSekme) => void;
  ornekAnswers: Record<string, string>;
  setOrnekAnswer: (id: string, key: string) => void;
  onNavigateToLearn?: Props['onNavigateToLearn'];
  onNavigateToPastExams?: Props['onNavigateToPastExams'];
  onNavigateToOrnek?: Props['onNavigateToOrnek'];
}> = ({ kazanim, no, konu, tab, setTab, ornekAnswers, setOrnekAnswer, onNavigateToLearn, onNavigateToPastExams, onNavigateToOrnek }) => {
  const ornekCount = ornekSayisi(kazanim);
  const tabs: Array<{ id: KaynakSekme; label: string; n: number; icon: React.ElementType }> = [
    { id: 'slayt' as const, label: 'Slayt', n: kazanim.slaytlar.length, icon: Presentation },
    { id: 'cikmis' as const, label: 'Çıkmış', n: kazanim.cikmisSorular.length, icon: Archive },
    { id: 'ornek' as const, label: 'Örnek soru', n: ornekCount, icon: Target },
    { id: 'sozluk' as const, label: 'Sözlük', n: kazanim.sozlukTerimleri.length, icon: BookOpenText },
    { id: 'ozet' as const, label: 'Özet', n: kazanim.ozetler.length, icon: Sparkles },
  ].filter((t) => t.n > 0);
  const active = tab && tabs.some((t) => t.id === tab) ? tab : tabs[0]?.id;
  const base = `kz-t-${kazanim.id}`;

  return (
    <>
      <div className="kz-ptabs" role="tablist" aria-label="Bağlı kaynaklar">
        {tabs.map((t) => {
          const Icon = t.icon;
          return (
            <button
              key={t.id}
              type="button"
              role="tab"
              id={`${base}-${t.id}`}
              aria-selected={active === t.id}
              aria-controls={`${base}-${t.id}-p`}
              className={active === t.id ? 'is-on' : ''}
              onClick={() => setTab(t.id)}
            >
              <Icon aria-hidden /> {t.label} <span className="kz-ptab-n">{t.n}</span>
            </button>
          );
        })}
      </div>

      <div className="kz-pbody" role="tabpanel" id={`${base}-${active}-p`} aria-labelledby={`${base}-${active}`}>
        {active === 'slayt' && (
          <ul className="kz-plist">
            {kazanim.slaytlar.map((sl, sIdx) => (
              <li key={sIdx} className="kz-pitem is-row">
                <div className="kz-pitem-main">
                  <p className="kz-pitem-t">{sl.kaynak} <span>· sayfa {sl.sayfa}</span></p>
                  {sl.alinti && <p className="kz-pitem-s">{sl.alinti}</p>}
                </div>
                {onNavigateToLearn && (
                  <button type="button" className="ui-btn is-tonal is-sm" onClick={() => onNavigateToLearn(sl.deckId, sl.sayfa)} title="Öğren modunda aç">
                    <GraduationCap aria-hidden /> Slayta git
                  </button>
                )}
              </li>
            ))}
          </ul>
        )}

        {active === 'cikmis' && (
          <>
            {onNavigateToPastExams && (
              <button type="button" className="kz-plink" onClick={() => onNavigateToPastExams(konu)}>
                Çıkmış'ta tümünü gör <ExternalLink aria-hidden />
              </button>
            )}
            <ul className="kz-plist">
              {kazanim.cikmisSorular.map((q) => (
                <li key={q.id} className="kz-pitem">
                  <p className="kz-pitem-meta">
                    <b>Soru #{q.questionNumber || '–'} · {q.year || 'Arşiv'}</b>
                    {q.correctAnswer && <span className="ms-tag is-ok">Doğru: {q.correctAnswer}</span>}
                  </p>
                  <p className="kz-pitem-q">{q.stem}</p>
                  {q.options && q.options.length > 0 && (
                    <ul className="kz-opts">
                      {q.options.map((opt) => (
                        <li key={opt.key} className={opt.key === q.correctAnswer ? 'is-ok' : ''}>
                          <b>{opt.key})</b> <span>{opt.text}</span>
                        </li>
                      ))}
                    </ul>
                  )}
                  {q.explanation && <p className="kz-pitem-x">{q.explanation}</p>}
                </li>
              ))}
            </ul>
          </>
        )}

        {active === 'ornek' && (
          <>
            {onNavigateToOrnek && (
              <button
                type="button"
                className="kz-plink"
                onClick={() => {
                  const targetDeckId = kazanim.slaytlar?.find((s) => s.deckId)?.deckId;
                  const targetKazanimNo = kazanim.ornekSorular?.[0]?.kazanimNo || no;
                  onNavigateToOrnek(targetDeckId, targetKazanimNo);
                }}
              >
                Örnek sorular modunda aç <ExternalLink aria-hidden />
              </button>
            )}
            <ul className="kz-plist">
              {kazanim.ornekSorular.map((oq) => {
                const userPick = ornekAnswers[oq.id];
                const solved = !!userPick;
                const isCorrect = userPick === oq.dogru;
                return (
                  <li key={oq.id} className="kz-pitem">
                    <p className="kz-pitem-meta">
                      <span className="ms-tag is-accent">{oq.zorluk || 'Standart'}</span>
                      {solved && <span className={`ms-tag ${isCorrect ? 'is-ok' : 'is-bad'}`}>{isCorrect ? '✓ Doğru' : `Yanıt: ${oq.dogru}`}</span>}
                    </p>
                    <p className="kz-pitem-q">{oq.soru}</p>
                    <div className="kz-choices">
                      {Object.entries(oq.secenekler || {}).map(([key, text]) => {
                        const state = solved ? (key === oq.dogru ? 'is-ok' : userPick === key ? 'is-bad' : '') : '';
                        return (
                          <button key={key} type="button" disabled={solved} className={`kz-choice ${state}`} onClick={() => setOrnekAnswer(oq.id, key)}>
                            <b>{key})</b> <span>{text}</span>
                          </button>
                        );
                      })}
                    </div>
                    {solved && oq.aciklama && <p className="kz-pitem-x is-note"><b>Açıklama:</b> {oq.aciklama}</p>}
                  </li>
                );
              })}
            </ul>
          </>
        )}

        {active === 'sozluk' && (
          <ul className="kz-plist">
            {kazanim.sozlukTerimleri.map((t, idx) => (
              <li key={idx} className="kz-pitem">
                <p className="kz-pitem-t">{t.term}</p>
                <p className="kz-pitem-s">{t.definition}</p>
                {t.pearl && <p className="kz-pitem-x">💡 {t.pearl}</p>}
              </li>
            ))}
          </ul>
        )}

        {active === 'ozet' && (
          <ul className="kz-bullets">
            {kazanim.ozetler.map((bullet, idx) => <li key={idx}>{bullet}</li>)}
          </ul>
        )}
      </div>
    </>
  );
};
