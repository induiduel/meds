import { icKonum, icUrl } from '../siteHaritasi';
import React, { useEffect, useMemo, useRef, useState } from 'react';
import { pathFor } from '../router';
import { Check, ChevronRight, Download, Search } from 'lucide-react';
import { FilterPills, PageToolbar, type ToolbarChip } from './ui/PageToolbar';
import { disciplineClass, disciplineLabel } from '../utils/discipline';
import summariesMetaData from '../data/summaries_meta.json';
// Resmi ders programı + kaynak PDF eşleşmesi: scripts/pipeline/10-enrich-summaries.mjs üretir
import summariesEnrichment from '../data/summaries_enrichment.json';
import curriculumDisciplines from '../data/curriculum_disciplines.json';
import { SummaryReader } from './summary/SummaryReader';
import { useReadingProgress, type ReadingMark } from './summary/readerStore';
import { triggerDomHighlightAndScroll } from '../services/universalRedirectService';
import { safeJsonFetch } from '../services/api';
import { queryClient } from '../queryClient';
import { offlineDatabaseService } from '../services/offlineDatabaseService';
import { useAppearance } from '../utils/appearance';
import { LectureSummariesV12 } from './v12/LectureSummariesV12';
import '../styles/summary.css';

/**
 * Ders özetleri (v10 kompakt). Yapı:
 *   PageToolbar (başlık · sayaç · arama · Tümü / Kurul 1–6 · Süzgeç sayfası: ders + okuma durumu · PDF indir)
 *   → "Okumaya devam" (yarım kalan özetler, en çok 3 satır) → Tümü'nde kurul kurul, bir kurulda ders ders
 *   gruplanmış kompakt ders listesi; aramada/süzgeçte düz liste.
 * Satır: ders no · başlık · ders + öğretim üyesi · okuma süresi ve durumu (yeni / %ilerleme / bitti).
 * Okuyucu: summary/SummaryReader (uygulama temasıyla, ayrı tema yok). Stil: styles/summary.css (.sl-*).
 */

export interface SummaryMeta {
  id: string;
  kurul: number;
  committeeId: string;
  discipline: string;
  title: string;
  instructor?: string;
  fileName: string;
  keyPoints: string[];
  charCount: number;
  readingTimeMinutes: number;
  /** Kaynak PDF'in oluşturulma yılı (biliniyorsa) */
  sourceYear?: number;
  sourceDate?: string;
  pdfName?: string;
}

export interface SummaryDetail extends SummaryMeta {
  content?: string;
}

type Enrichment = { lessonTitle?: string; discipline?: string; instructor?: string; sourceYear?: number; sourceDate?: string; pdfName?: string };
const ENRICH = summariesEnrichment as Record<string, Enrichment>;
const KURUL_DISCIPLINES = curriculumDisciplines as Record<string, string[]>;

const KURUL_LABELS: Record<number, string> = {
  1: 'Ürogenital & Obstetrik',
  2: 'Nöropsikiyatri',
  3: 'Gastrointestinal Sistem',
  4: 'Dolaşım, Solunum & Tümör',
  5: 'Ortopedi, Travma & Hematopoetik',
  6: 'Endokrin & Yaşlanma',
};
const KURULS = [1, 2, 3, 4, 5, 6] as const;

/** Dosya adından türemiş başlıkları toparlar: baştaki sıra numarası, "D3", alt çizgi vb. */
const cleanTitle = (t: string) =>
  t
    .replace(/^\s*\d+\s*[).\-]?\s*/, '')
    .replace(/\b(d\d+|son|kopya|\(\d+\))\b/gi, ' ')
    .replace(/\s{2,}/g, ' ')
    .trim()
    .replace(/^\p{Ll}/u, (c) => c.toLocaleUpperCase('tr')) || t;

const fold = (s: string) => s.toLocaleLowerCase('tr').normalize('NFD').replace(/[̀-ͯ]/g, '');

interface LectureSummariesViewProps {
  onOpenPdfModal?: () => void;
  /** Aramadan gelince doğrudan açılacak özet */
  initialSummaryId?: string;
}

async function loadSummaryDetail(meta: SummaryMeta): Promise<SummaryDetail | null> {
  // 0. Cihaz hafızası (IndexedDB)
  try {
    const saved = await offlineDatabaseService.getSummaries();
    const hit = saved.find((s: any) => s.id === meta.id);
    if (hit?.content) return hit;
  } catch {
    /* yoksa sıradakine geç */
  }
  // 1. Sunucu (kullanıcının seçtiği API adresine saygılı)
  if (typeof navigator === 'undefined' || navigator.onLine) {
    const res = await safeJsonFetch<{ success?: boolean; summary?: SummaryDetail }>(`/api/summaries/${encodeURIComponent(meta.id)}`);
    if (res.ok && res.data?.summary?.content) return res.data.summary;
  }
  // 2. Paketle gelen kurul dosyası (çevrimdışı)
  const loaders: Record<number, () => Promise<any>> = {
    1: () => import('../data/summaries/kurul1.json'),
    2: () => import('../data/summaries/kurul2.json'),
    3: () => import('../data/summaries/kurul3.json'),
    4: () => import('../data/summaries/kurul4.json'),
    5: () => import('../data/summaries/kurul5.json'),
    6: () => import('../data/summaries/kurul6.json'),
  };
  try {
    const mod = await (loaders[meta.kurul] || loaders[1])();
    const list: SummaryDetail[] = mod.default || mod;
    return list.find((s) => s.id === meta.id) || null;
  } catch (e) {
    console.warn('Özet içeriği yüklenemedi:', e);
    return null;
  }
}

/** "k1-07-…" → 7 (ders programı sırası); yoksa liste sırası */
const lessonNo = (id: string, fallback: number) => {
  const m = id.match(/^k\d+-(\d{1,3})-/);
  return m ? Number(m[1]) : fallback;
};

type ReadFilter = 'all' | 'new' | 'reading' | 'done';
const READ_LABEL: Record<ReadFilter, string> = { all: 'Tümü', new: 'Okunmadı', reading: 'Yarım kalan', done: 'Bitti' };
const readStateOf = (m?: ReadingMark): Exclude<ReadFilter, 'all'> => (!m || m.p < 2 ? 'new' : m.p >= 97 ? 'done' : 'reading');

const ReadState: React.FC<{ mark?: ReadingMark; minutes: number }> = ({ mark, minutes }) => {
  if (mark && mark.p >= 97)
    return (
      <span className="sl-state is-done">
        <Check aria-hidden /> Bitti
      </span>
    );
  if (mark && mark.p >= 2)
    return (
      <span className="sl-state is-reading" aria-label={`%${Math.round(mark.p)} okundu`}>
        <span className="sl-bar" aria-hidden>
          <i style={{ transform: `scaleX(${mark.p / 100})` }} />
        </span>
        %{Math.round(mark.p)}
      </span>
    );
  return <span className="sl-state">{minutes} dk</span>;
};

const Row: React.FC<{ s: SummaryMeta; no: number; mark?: ReadingMark; showKurul: boolean; onOpen: () => void }> = ({ s, no, mark, showKurul, onOpen }) => (
  <li className={`sl-item ${disciplineClass(s.discipline)}`}>
    <button type="button" className="sl-row" onClick={onOpen}>
      <span className="sl-no" aria-hidden>
        {String(no).padStart(2, '0')}
      </span>
      <span className="sl-row-main">
        <span className="sl-row-t">{s.title}</span>
        <span className="sl-row-m">
          <i className="hk-dot" aria-hidden />
          <span>{disciplineLabel(s.discipline)}</span>
          {showKurul && <span className="sl-kurul">K{s.kurul}</span>}
          {s.instructor && <span className="sl-row-who">· {s.instructor}</span>}
        </span>
      </span>
      <ReadState mark={mark} minutes={s.readingTimeMinutes} />
      <ChevronRight className="sl-go" aria-hidden />
    </button>
  </li>
);

export const LectureSummariesView: React.FC<LectureSummariesViewProps> = ({ onOpenPdfModal, initialSummaryId }) => {
  const [kurul, setKurul] = useState<number | 'all'>('all');
  const [discipline, setDiscipline] = useState('all');
  const [query, setQuery] = useState('');
  const [readFilter, setReadFilter] = useState<ReadFilter>('all');
  const [active, setActive] = useState<SummaryDetail | null>(null);
  const progress = useReadingProgress();
  const v12 = useAppearance().design === 'v12';

  // Ders programından gelen gerçek ders adı, branş ve öğretim üyesi; kaynak PDF yılı
  const summaries: SummaryMeta[] = useMemo(
    () =>
      (summariesMetaData as SummaryMeta[]).map((s) => {
        const e = ENRICH[s.id] || {};
        return {
          ...s,
          title: e.lessonTitle || cleanTitle(s.title),
          discipline: e.discipline || s.discipline,
          instructor: e.instructor || s.instructor,
          sourceYear: e.sourceYear,
          sourceDate: e.sourceDate,
          pdfName: e.pdfName,
        };
      }),
    []
  );
  const byId = useMemo(() => new Map(summaries.map((s) => [s.id, s])), [summaries]);

  // Kurul seçiliyse yalnız o kurulda verilen dersler (resmi programdan; özeti olanlar)
  const disciplines = useMemo(() => {
    const have = new Set(summaries.filter((s) => kurul === 'all' || s.kurul === kurul).map((s) => s.discipline).filter(Boolean));
    const program = kurul === 'all' ? null : KURUL_DISCIPLINES[String(kurul)];
    const list = program ? program.filter((d) => have.has(d)) : Array.from(have);
    return list.sort((a, b) => a.localeCompare(b, 'tr'));
  }, [summaries, kurul]);

  useEffect(() => {
    if (discipline !== 'all' && !disciplines.includes(discipline)) setDiscipline('all');
  }, [disciplines, discipline]);

  const q = fold(query.trim());
  const filtered = useMemo(
    () =>
      summaries.filter((s) => {
        if (kurul !== 'all' && s.kurul !== kurul) return false;
        if (discipline !== 'all' && s.discipline !== discipline) return false;
        if (readFilter !== 'all' && readStateOf(progress[s.id]) !== readFilter) return false;
        if (!q) return true;
        return [s.title, s.discipline, s.instructor || '', ...(s.keyPoints || [])].some((f) => fold(f).includes(q));
      }),
    [summaries, kurul, discipline, q, readFilter, progress]
  );

  // Gruplar: arama → düz liste; Tümü → kurul; kurul seçili → ders
  const groups = useMemo(() => {
    if (q || discipline !== 'all' || readFilter !== 'all') return [{ key: 'flat', title: '', sub: '', items: filtered }];
    if (kurul === 'all') {
      return KURULS.map((k) => ({ key: `k${k}`, title: `Kurul ${k}`, sub: KURUL_LABELS[k], items: filtered.filter((s) => s.kurul === k) })).filter((g) => g.items.length);
    }
    const map = new Map<string, SummaryMeta[]>();
    filtered.forEach((s) => map.set(s.discipline, [...(map.get(s.discipline) || []), s]));
    return Array.from(map.entries())
      .sort((a, b) => b[1].length - a[1].length || a[0].localeCompare(b[0], 'tr'))
      .map(([d, items]) => ({ key: d, title: disciplineLabel(d), sub: d !== disciplineLabel(d) ? d : '', items, d }));
  }, [filtered, kurul, discipline, q, readFilter]);
  const ordered = useMemo(() => groups.flatMap((g) => g.items), [groups]);

  // Yarım kalan özetler (son okunan önce)
  const inProgress = useMemo(
    () =>
      Object.entries(progress)
        .filter(([id, m]) => m.p >= 2 && m.p < 97 && byId.has(id))
        .sort((a, b) => b[1].t - a[1].t)
        .slice(0, 3)
        .map(([id, m]) => ({ s: byId.get(id)!, m })),
    [progress, byId]
  );
  const doneCount = useMemo(() => summaries.filter((s) => (progress[s.id]?.p || 0) >= 97).length, [summaries, progress]);

  const open = async (meta: SummaryMeta) => {
    setActive(meta); // okuyucu hemen açılır, içerik gelene kadar iskelet gösterir
    try {
      const detail = await queryClient.fetchQuery({
        queryKey: ['summary-detail', meta.id],
        queryFn: () => loadSummaryDetail(meta),
        staleTime: 1000 * 60 * 60,
      });
      setActive((cur) => (cur && cur.id === meta.id ? (detail ? { ...meta, ...detail, title: meta.title, discipline: meta.discipline, instructor: meta.instructor } : cur) : cur));
      if (!detail) return;
      const highlight = new URLSearchParams(icKonum().search).get('highlight');
      if (highlight) window.setTimeout(() => triggerDomHighlightAndScroll(highlight), 500);
    } catch (e) {
      console.warn('Özet detay yükleme hatası:', e);
    }
  };

  // Açık özet adreste tutulur (/ozetler/<id>): okuyucu açılınca geçmişe kayıt eklenir, böylece başka sayfaya gidip
  // Geri ile dönünce (tam ekranda da) aynı özet yeniden açılır; telefonda geri hareketi okuyucuyu kapatır.
  const pushedRef = useRef(false);
  const activeIdRef = useRef<string | null>(null);
  activeIdRef.current = active?.id ?? null;
  const yolId = () => {
    const m = icKonum().pathname.match(/^\/ozetler\/([^/?#]+)/);
    return m ? decodeURIComponent(m[1]) : new URLSearchParams(icKonum().search).get('id');
  };
  const openAt = (meta: SummaryMeta, replace = false) => {
    void open(meta);
    if (yolId() === meta.id) return;
    window.history[replace ? 'replaceState' : 'pushState'](window.history.state, '', pathFor('summaries', meta.id));
    if (!replace) pushedRef.current = true;
  };
  const closeReader = () => {
    setActive(null);
    if (!yolId()) return;
    if (pushedRef.current) {
      pushedRef.current = false;
      window.history.back();
      return;
    }
    window.history.replaceState(window.history.state, '', pathFor('summaries'));
  };
  useEffect(() => {
    const onPop = () => {
      pushedRef.current = false;
      const id = yolId();
      if (!id) return setActive(null);
      const meta = byId.get(id);
      if (meta && activeIdRef.current !== id) void open(meta);
    };
    window.addEventListener('popstate', onPop);
    return () => window.removeEventListener('popstate', onPop);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [byId]);

  useEffect(() => {
    const params = new URLSearchParams(icKonum().search);
    const target = initialSummaryId || params.get('id') || params.get('summaryId') || params.get('noteId');
    const highlight = params.get('highlight');
    if (target) {
      const meta = byId.get(target);
      if (meta) open(meta);
    } else if (highlight) {
      window.setTimeout(() => triggerDomHighlightAndScroll(highlight), 500);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [initialSummaryId, byId]);

  const nextOf = (id: string) => {
    const i = ordered.findIndex((s) => s.id === id);
    return i >= 0 ? ordered[i + 1] : undefined;
  };
  const next = active ? nextOf(active.id) : undefined;

  const chips: ToolbarChip[] = [
    ...(discipline !== 'all' ? [{ id: 'd', label: discipline, onRemove: () => setDiscipline('all') }] : []),
    ...(readFilter !== 'all' ? [{ id: 'r', label: READ_LABEL[readFilter], onRemove: () => setReadFilter('all') }] : []),
  ];
  const kurulCount = (k: number) => summaries.filter((s) => s.kurul === k).length;

  const toolbar = (
      <PageToolbar<string>
        title="Ders özetleri"
        count={
          filtered.length === summaries.length
            ? `${summaries.length} özet${doneCount ? ` · ${doneCount} bitti` : ''}`
            : `${filtered.length} / ${summaries.length}`
        }
        search={{ value: query, onChange: setQuery, placeholder: 'Ders, konu ya da hoca ara' }}
        segments={{
          label: 'Kurul',
          value: String(kurul),
          onChange: (v) => setKurul(v === 'all' ? 'all' : Number(v)),
          options: [
            { id: 'all', label: 'Tümü', count: summaries.length },
            ...KURULS.filter((k) => kurulCount(k) > 0).map((k) => ({ id: String(k), label: `Kurul ${k}`, count: kurulCount(k) })),
          ],
        }}
        filters={
          <>
            <FilterPills
              label={kurul === 'all' ? 'Ders' : `Kurul ${kurul} dersleri`}
              value={discipline}
              onChange={setDiscipline}
              options={[
                { id: 'all', label: 'Tüm dersler', count: summaries.filter((s) => kurul === 'all' || s.kurul === kurul).length },
                ...disciplines.map((d) => ({ id: d, label: d, count: summaries.filter((s) => s.discipline === d && (kurul === 'all' || s.kurul === kurul)).length })),
              ]}
            />
            <FilterPills<ReadFilter>
              label="Okuma durumu"
              value={readFilter}
              onChange={setReadFilter}
              options={(Object.keys(READ_LABEL) as ReadFilter[]).map((id) => ({ id, label: READ_LABEL[id] }))}
            />
          </>
        }
        filterCount={chips.length}
        chips={chips}
        onClearChips={() => {
          setDiscipline('all');
          setReadFilter('all');
        }}
        tools={
          onOpenPdfModal && (
            <button type="button" onClick={onOpenPdfModal} className="pt-icon" aria-label="PDF indir" title="PDF indir">
              <Download aria-hidden />
            </button>
          )
        }
      />
  );
  const clearFilters = () => {
    setQuery('');
    setDiscipline('all');
    setReadFilter('all');
  };
  const reader = active && (
    <SummaryReader summary={active} onClose={closeReader} onOpenPdfModal={onOpenPdfModal} next={next} onOpenNext={next ? () => openAt(next, true) : undefined} />
  );

  if (v12)
    return (
      <LectureSummariesV12
        toolbar={toolbar}
        inProgress={inProgress}
        showContinue={!q && readFilter === 'all'}
        groups={groups}
        filteredCount={filtered.length}
        filtering={!!q || discipline !== 'all' || readFilter !== 'all'}
        onClearFilters={clearFilters}
        progress={progress}
        kurulAll={kurul === 'all'}
        lessonNo={lessonNo}
        onOpen={(m) => openAt(m)}
        reader={reader}
      />
    );

  let idx = 0;
  return (
    <div className="sl-page">
      {toolbar}

      {inProgress.length > 0 && !q && readFilter === 'all' && (
        <section className="sl-group sl-continue" aria-label="Okumaya devam">
          <header className="sl-group-h">
            <h2 className="sl-h">Okumaya devam</h2>
          </header>
          <ul className="sl-list">
            {inProgress.map(({ s, m }) => (
              <li key={s.id} className={`sl-item ${disciplineClass(s.discipline)}`}>
                <button type="button" className="sl-row" onClick={() => openAt(s)}>
                  <span className="sr-ring is-sm" style={{ '--p': m.p } as React.CSSProperties} aria-hidden />
                  <span className="sl-row-main">
                    <span className="sl-row-t">{s.title}</span>
                    <span className="sl-row-m">
                      <i className="hk-dot" aria-hidden />
                      <span>{disciplineLabel(s.discipline)}</span>
                      <span>· ~{Math.max(1, Math.round(s.readingTimeMinutes * (1 - m.p / 100)))} dk kaldı</span>
                    </span>
                  </span>
                  <span className="sl-state is-reading">%{Math.round(m.p)}</span>
                  <ChevronRight className="sl-go" aria-hidden />
                </button>
              </li>
            ))}
          </ul>
        </section>
      )}

      {filtered.length === 0 ? (
        <div className="sl-empty">
          <Search aria-hidden />
          <h3>Bu süzgeçte özet yok</h3>
          <p>Aramayı temizle ya da başka bir kurul seç.</p>
          {(query || discipline !== 'all' || readFilter !== 'all') && (
            <button
              type="button"
              className="ui-btn is-sm"
              onClick={() => {
                setQuery('');
                setDiscipline('all');
                setReadFilter('all');
              }}
            >
              Süzgeçleri temizle
            </button>
          )}
        </div>
      ) : (
        <div className="sl-groups" key={`${kurul}|${discipline}|${readFilter}`}>
          {groups.map((g) => (
            <section key={g.key} className={`sl-group ${'d' in g && g.d ? disciplineClass(g.d as string) : ''}`} aria-label={g.title || 'Sonuçlar'}>
              {g.title ? (
                <header className="sl-group-h">
                  {'d' in g && <i className="hk-dot" aria-hidden />}
                  <h2 className="sl-h">{g.title}</h2>
                  {g.sub && <span>{g.sub}</span>}
                  <small>{g.items.length}</small>
                </header>
              ) : (
                (q || discipline !== 'all' || readFilter !== 'all') && (
                  <p className="sl-result" aria-live="polite">
                    {g.items.length} sonuç
                  </p>
                )
              )}
              <ul className="sl-list">
                {g.items.map((s) => (
                  <Row key={s.id} s={s} no={lessonNo(s.id, ++idx)} mark={progress[s.id]} showKurul={kurul === 'all' && !g.title} onOpen={() => openAt(s)} />
                ))}
              </ul>
            </section>
          ))}
        </div>
      )}

      {active && (
        <SummaryReader
          summary={active}
          onClose={closeReader}
          onOpenPdfModal={onOpenPdfModal}
          next={next}
          onOpenNext={next ? () => openAt(next, true) : undefined}
        />
      )}
    </div>
  );
};
