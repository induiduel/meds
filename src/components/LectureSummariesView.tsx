import React, { useEffect, useMemo, useState } from 'react';
import { Check, ChevronRight, Clock, Download, GraduationCap, Search, X } from 'lucide-react';
import { PageHeader } from './ui/PageHeader';
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

/**
 * Ders özetleri (v9, sıfırdan). Yapı:
 *   başlık + PDF · "Okumaya devam" şeridi (yarım kalan özetler) · arama + ders süzgeci · kurul şeridi
 *   → Tümü'nde kurul kurul, bir kurulda ders ders gruplanmış kartlar; aramada düz sonuç listesi.
 * Kart: ders rengi (--d), başlık, öğretim üyesi, okuma süresi ve okuma durumu (yeni / %ilerleme / bitti).
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

const ReadState: React.FC<{ mark?: ReadingMark }> = ({ mark }) => {
  if (!mark || mark.p < 2) return null;
  if (mark.p >= 97)
    return (
      <span className="sl-state is-done">
        <Check aria-hidden /> Bitti
      </span>
    );
  return (
    <span className="sl-state">
      <i className="sr-ring is-xs" style={{ '--p': mark.p } as React.CSSProperties} aria-hidden />%{Math.round(mark.p)}
    </span>
  );
};

const Card: React.FC<{ s: SummaryMeta; i: number; mark?: ReadingMark; showKurul: boolean; onOpen: () => void }> = ({ s, i, mark, showKurul, onOpen }) => (
  <li className={`sl-item ${disciplineClass(s.discipline)}`} style={{ '--i': Math.min(i, 14) } as React.CSSProperties}>
    <button type="button" className="sl-card" onClick={onOpen}>
      <span className="sl-card-top">
        <span className="hk-eyebrow">
          <i className="hk-dot" aria-hidden />
          <span>{disciplineLabel(s.discipline)}</span>
        </span>
        {showKurul && <span className="sl-kurul">K{s.kurul}</span>}
        <ReadState mark={mark} />
      </span>
      <span className="sl-card-t">{s.title}</span>
      {s.instructor && (
        <span className="sl-card-who">
          <GraduationCap aria-hidden />
          <span>{s.instructor}</span>
        </span>
      )}
      <span className="sl-card-foot">
        <span>
          <Clock aria-hidden /> {s.readingTimeMinutes} dk
        </span>
        {s.sourceYear && <span title={s.pdfName ? `${s.pdfName} · ${s.sourceDate || ''}` : s.sourceDate}>{s.sourceYear}</span>}
        <ChevronRight className="sl-card-go" aria-hidden />
      </span>
      {mark && mark.p >= 2 && mark.p < 97 && (
        <span className="sl-card-bar" aria-hidden>
          <i style={{ transform: `scaleX(${mark.p / 100})` }} />
        </span>
      )}
    </button>
  </li>
);

export const LectureSummariesView: React.FC<LectureSummariesViewProps> = ({ onOpenPdfModal, initialSummaryId }) => {
  const [kurul, setKurul] = useState<number | 'all'>('all');
  const [discipline, setDiscipline] = useState('all');
  const [query, setQuery] = useState('');
  const [active, setActive] = useState<SummaryDetail | null>(null);
  const progress = useReadingProgress();

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
        if (!q) return true;
        return [s.title, s.discipline, s.instructor || '', ...(s.keyPoints || [])].some((f) => fold(f).includes(q));
      }),
    [summaries, kurul, discipline, q]
  );

  // Gruplar: arama → düz liste; Tümü → kurul; kurul seçili → ders
  const groups = useMemo(() => {
    if (q || discipline !== 'all') return [{ key: 'flat', title: '', sub: '', items: filtered }];
    if (kurul === 'all') {
      return KURULS.map((k) => ({ key: `k${k}`, title: `Kurul ${k}`, sub: KURUL_LABELS[k], items: filtered.filter((s) => s.kurul === k) })).filter((g) => g.items.length);
    }
    const map = new Map<string, SummaryMeta[]>();
    filtered.forEach((s) => map.set(s.discipline, [...(map.get(s.discipline) || []), s]));
    return Array.from(map.entries())
      .sort((a, b) => b[1].length - a[1].length || a[0].localeCompare(b[0], 'tr'))
      .map(([d, items]) => ({ key: d, title: disciplineLabel(d), sub: d !== disciplineLabel(d) ? d : '', items, d }));
  }, [filtered, kurul, discipline, q]);
  const ordered = useMemo(() => groups.flatMap((g) => g.items), [groups]);

  // Yarım kalan özetler (son okunan önce)
  const inProgress = useMemo(
    () =>
      Object.entries(progress)
        .filter(([id, m]) => m.p >= 2 && m.p < 97 && byId.has(id))
        .sort((a, b) => b[1].t - a[1].t)
        .slice(0, 8)
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
      const highlight = new URLSearchParams(window.location.search).get('highlight');
      if (highlight) window.setTimeout(() => triggerDomHighlightAndScroll(highlight), 500);
    } catch (e) {
      console.warn('Özet detay yükleme hatası:', e);
    }
  };

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
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

  let idx = 0;
  return (
    <div className="sl-page">
      <PageHeader
        title="Ders özetleri"
        description="Amfi notlarından derlenmiş özetler: mekanizmalar, tablolar, sınav tuzakları ve çıkmış sorular."
        stats={[
          { label: 'özet', value: summaries.length },
          ...(doneCount ? [{ label: 'bitti', value: doneCount, tone: 'ok' as const }] : []),
        ]}
        actions={
          onOpenPdfModal && (
            <button type="button" onClick={onOpenPdfModal} className="ms-btn" aria-label="PDF indir">
              <Download aria-hidden />
              <span className="hidden sm:inline">PDF indir</span>
            </button>
          )
        }
      />

      {inProgress.length > 0 && !q && (
        <section className="sl-continue" aria-label="Okumaya devam">
          <h2 className="sl-h">Okumaya devam</h2>
          <ul className="sl-continue-rail">
            {inProgress.map(({ s, m }, i) => (
              <li key={s.id} className={disciplineClass(s.discipline)} style={{ '--i': i } as React.CSSProperties}>
                <button type="button" className="sl-cont" onClick={() => open(s)}>
                  <span className="sr-ring is-lg" style={{ '--p': m.p } as React.CSSProperties} aria-hidden>
                    <b>%{Math.round(m.p)}</b>
                  </span>
                  <span className="sl-cont-txt">
                    <span className="hk-eyebrow">
                      <i className="hk-dot" aria-hidden />
                      <span>{disciplineLabel(s.discipline)}</span>
                    </span>
                    <b>{s.title}</b>
                    <small>~{Math.max(1, Math.round(s.readingTimeMinutes * (1 - m.p / 100)))} dk kaldı</small>
                  </span>
                </button>
              </li>
            ))}
          </ul>
        </section>
      )}

      <div className="sl-filters">
        <label className="cx-search sl-search">
          <Search aria-hidden />
          <span className="sr-only">Özetlerde ara</span>
          <input type="search" value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Ders, konu ya da hoca ara" />
          {query && (
            <button type="button" className="cx-search-x" onClick={() => setQuery('')} aria-label="Aramayı temizle">
              <X />
            </button>
          )}
        </label>
        <label className="sr-only" htmlFor="sl-discipline">
          Ders
        </label>
        <select id="sl-discipline" value={discipline} onChange={(e) => setDiscipline(e.target.value)} className="ms-select sl-select">
          <option value="all">
            {kurul === 'all' ? 'Tüm dersler' : `Kurul ${kurul} dersleri`} ({disciplines.length})
          </option>
          {disciplines.map((d) => (
            <option key={d} value={d}>
              {d}
            </option>
          ))}
        </select>
      </div>

      <nav className="cx-tabs sl-tabs" aria-label="Kurul" role="radiogroup">
        {(['all', ...KURULS] as const).map((k) => {
          const on = kurul === k;
          const count = k === 'all' ? summaries.length : summaries.filter((s) => s.kurul === k).length;
          return (
            <button
              key={String(k)}
              type="button"
              role="radio"
              aria-checked={on}
              title={k === 'all' ? undefined : `Kurul ${k}: ${KURUL_LABELS[k]}`}
              onClick={() => setKurul(k)}
              className={`cx-tab ${on ? 'is-on' : ''} ${count === 0 ? 'is-zero' : ''}`}
            >
              {k === 'all' ? 'Tümü' : `Kurul ${k}`} <small>{count}</small>
            </button>
          );
        })}
      </nav>

      {filtered.length === 0 ? (
        <div className="sl-empty">
          <Search aria-hidden />
          <h3>Bu süzgeçte özet yok</h3>
          <p>Aramayı temizle ya da başka bir kurul seç.</p>
          {(query || discipline !== 'all') && (
            <button type="button" className="ms-btn" onClick={() => { setQuery(''); setDiscipline('all'); }}>
              Süzgeçleri temizle
            </button>
          )}
        </div>
      ) : (
        <div className="sl-groups" key={`${kurul}|${discipline}`}>
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
                q && (
                  <p className="sl-result" aria-live="polite">
                    {g.items.length} sonuç
                  </p>
                )
              )}
              <ul className="sl-grid">
                {g.items.map((s) => (
                  <Card key={s.id} s={s} i={idx++} mark={progress[s.id]} showKurul={kurul === 'all' && !g.title} onOpen={() => open(s)} />
                ))}
              </ul>
            </section>
          ))}
        </div>
      )}

      {active && (
        <SummaryReader
          summary={active}
          onClose={() => setActive(null)}
          onOpenPdfModal={onOpenPdfModal}
          next={next}
          onOpenNext={next ? () => open(next) : undefined}
        />
      )}
    </div>
  );
};
