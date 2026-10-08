import React, { Suspense, useEffect, useRef, useState } from 'react';
import { ArrowUpRight, ChevronDown, Loader2, Search, X } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import type { LectureNote } from '../../types';
import { PageHeader } from '../ui/PageHeader';
import { fetchSearch, Highlight, TypeTag, TYPE_META, TYPE_ORDER, type SearchDocType, type SearchHit, type SearchResponse } from './searchShared';
import { rememberSearch } from './SearchPalette';

const PAGE = 20;

const SlideReaderModal = React.lazy(() => import('../SlideReaderModal').then((m) => ({ default: m.SlideReaderModal || (m as any).default })));

/** Sonucun açılacağı yer; null ise yalnızca sayfa içinde okunur */
export const SOURCE_ACTION: Partial<Record<SearchDocType, string>> = {
  lecture_slide: 'Slaytı aç',
  summary: 'Özeti aç',
  past_question: 'Çıkmış sorularda aç',
  deepseek_contribution: 'Çıkmış sorularda aç',
  active_question: 'Havuzda aç',
  user_contribution: 'Havuzda aç',
  transcript: 'Ses kayıtlarına git',
};

interface SearchViewProps {
  initialQuery: string;
  focusId?: string;
  committeeId?: string;
  onQueryChange: (q: string) => void;
  /** Slayt dışındaki kaynaklar ilgili sayfada açılır */
  onOpenSource: (hit: SearchHit) => void;
}

/** Tüm arama sonuçları: tür süzgeci, sayfalı liste, sonuç içinde açılır tam metin. */
export const SearchView: React.FC<SearchViewProps> = ({ initialQuery, focusId, committeeId, onQueryChange, onOpenSource }) => {
  const [slide, setSlide] = useState<{ note: LectureNote; page?: number } | null>(null);
  const [openingId, setOpeningId] = useState<string | null>(null);
  const openSource = async (r: SearchHit) => {
    if (r.documentType !== 'lecture_slide') return onOpenSource(r);
    setOpeningId(r.id);
    const res = await safeJsonFetch<LectureNote>(`/api/lecture-notes/${encodeURIComponent(r.documentId)}`);
    setOpeningId(null);
    if (res.ok && res.data?.pages) setSlide({ note: res.data, page: r.pageNumber });
  };
  const [input, setInput] = useState(initialQuery);
  const [query, setQuery] = useState(initialQuery);
  const [type, setType] = useState<SearchDocType | 'all'>('all');
  const [data, setData] = useState<SearchResponse | null>(null);
  const [items, setItems] = useState<SearchHit[]>([]);
  const [loading, setLoading] = useState(false);
  const [loadingMore, setLoadingMore] = useState(false);
  const [openId, setOpenId] = useState<string | undefined>(focusId);
  const [byType, setByType] = useState<SearchResponse['byType']>({});
  const listTop = useRef<HTMLDivElement>(null);

  // Adres çubuğundan ya da paletten gelen yeni sorgu
  useEffect(() => { setInput(initialQuery); setQuery(initialQuery); }, [initialQuery]);
  useEffect(() => { setOpenId(focusId); }, [focusId]);

  useEffect(() => {
    if (!query.trim()) { setData(null); setItems([]); setByType({}); return; }
    const ctrl = new AbortController();
    setLoading(true);
    fetchSearch(query, { limit: PAGE, types: type === 'all' ? undefined : [type], committeeId }, ctrl.signal).then((res) => {
      if (ctrl.signal.aborted) return;
      setData(res);
      setItems(res?.results || []);
      if (type === 'all' || !Object.keys(byType).length) setByType(res?.byType || {});
      setLoading(false);
    });
    return () => ctrl.abort();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [query, type, committeeId]);

  // Odaklanan sonuca kaydır
  useEffect(() => {
    if (!openId || loading) return;
    const el = document.querySelector<HTMLElement>(`[data-hit="${CSS.escape(openId)}"]`);
    el?.scrollIntoView({ block: 'center', behavior: 'smooth' });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [loading]);

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    const q = input.trim();
    if (!q) return;
    rememberSearch(q);
    setType('all');
    setQuery(q);
    setOpenId(undefined);
    onQueryChange(q);
  };

  const loadMore = async () => {
    if (!data) return;
    setLoadingMore(true);
    const res = await fetchSearch(query, { limit: PAGE, offset: items.length, types: type === 'all' ? undefined : [type], committeeId });
    setItems((prev) => [...prev, ...(res?.results || [])]);
    setLoadingMore(false);
  };

  const allCount = Object.values(byType).reduce((a, b) => a + (b || 0), 0);
  const chips = TYPE_ORDER.filter((t) => byType[t]);
  const total = data?.total ?? 0;

  return (
    <div className="flex flex-col gap-4 min-w-0 pb-12">
      <PageHeader title="Arama" description={query ? undefined : 'Slaytlar, özetler, çıkmış sorular ve ses kayıtlarının tamamında ara.'} />

      <form onSubmit={submit} role="search" className="ms-search-field is-page">
        <Search className="w-[18px] h-[18px] text-ink-3 shrink-0" />
        <input
          type="search"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Hastalık, ilaç, bulgu, soru…"
          aria-label="Ara"
          enterKeyHint="search"
          autoComplete="off"
          spellCheck={false}
        />
        {input && (
          <button type="button" className="ms-search-icon-btn" onClick={() => setInput('')} aria-label="Temizle">
            <X className="w-4 h-4" />
          </button>
        )}
        <button type="submit" className="ms-search-submit">Ara</button>
      </form>

      {chips.length > 0 && (
        <div className="flex gap-2 overflow-x-auto no-scrollbar -mx-4 px-4 sm:mx-0 sm:px-0" role="tablist" aria-label="Kaynak türü">
          {(['all', ...chips] as const).map((t) => {
            const on = type === t;
            const count = t === 'all' ? allCount : byType[t];
            return (
              <button
                key={t}
                type="button"
                role="tab"
                aria-selected={on}
                onClick={() => { setType(t); setOpenId(undefined); listTop.current?.scrollIntoView({ block: 'nearest' }); }}
                className={`ms-chip ${on ? 'is-on' : ''}`}
              >
                {t === 'all' ? 'Tümü' : TYPE_META[t].label}
                <span className="ms-chip-count">{count}{data?.capped && t === 'all' ? '+' : ''}</span>
              </button>
            );
          })}
        </div>
      )}

      <div ref={listTop} />

      {loading ? (
        <div className="flex flex-col gap-2">
          {[0, 1, 2, 3].map((i) => <div key={i} className="h-[92px] rounded-2xl bg-white border border-line animate-pulse" />)}
        </div>
      ) : !query ? null : items.length === 0 ? (
        <div className="py-14 text-center text-[15px] text-ink-3">“{query}” için sonuç bulunamadı. Daha kısa ya da farklı bir ifade dene.</div>
      ) : (
        <>
          <p className="m-0 text-[13px] text-ink-3">
            “<span className="text-ink font-medium">{query}</span>” için {total}{data?.capped ? '+' : ''} sonuç · alaka sırasına göre
          </p>
          <ol className="m-0 p-0 list-none flex flex-col gap-2">
            {items.map((r) => {
              const open = openId === r.id;
              return (
                <li key={r.id} data-hit={r.id} className={`ms-hit ${open ? 'is-open' : ''}`}>
                  <button type="button" className="ms-hit-head" aria-expanded={open} onClick={() => setOpenId(open ? undefined : r.id)}>
                    <span className="flex items-center gap-2 min-w-0 flex-wrap">
                      <TypeTag type={r.documentType} />
                      {r.discipline && <span className="text-[12px] text-ink-3 truncate max-w-full">{r.discipline}</span>}
                      {r.pageNumber ? <span className="text-[12px] text-ink-3">· s. {r.pageNumber}</span> : null}
                    </span>
                    <span className="ms-hit-title"><Highlight text={r.title} query={query} /></span>
                    {!open && <span className="ms-hit-snippet"><Highlight text={r.snippet} query={query} /></span>}
                    <ChevronDown className="ms-hit-chev w-4 h-4" aria-hidden="true" />
                  </button>
                  <div className="ms-collapsible-body">
                    <div className="min-h-0 overflow-hidden">
                      {SOURCE_ACTION[r.documentType] && (
                        <div className="ms-hit-actions">
                          <button type="button" onClick={() => openSource(r)} disabled={openingId === r.id} className="h-10 px-4 rounded-full bg-accent-soft text-accent text-[14px] font-semibold inline-flex items-center gap-1.5 cursor-pointer hover:bg-accent hover:text-white transition-colors disabled:opacity-60">
                            {openingId === r.id ? <Loader2 className="w-4 h-4 animate-spin" /> : <ArrowUpRight className="w-4 h-4" />}
                            {SOURCE_ACTION[r.documentType]}
                          </button>
                        </div>
                      )}
                      <div className="ms-hit-full"><Highlight text={r.content} query={query} /></div>
                    </div>
                  </div>
                </li>
              );
            })}
          </ol>
          {items.length < total && (
            <button type="button" onClick={loadMore} disabled={loadingMore} className="self-center h-11 px-5 rounded-full border border-line-2 bg-white text-[14px] font-semibold text-ink cursor-pointer hover:bg-canvas disabled:opacity-60 inline-flex items-center gap-2">
              {loadingMore && <Loader2 className="w-4 h-4 animate-spin" />}
              Daha fazla göster
            </button>
          )}
        </>
      )}

      {slide && (
        <Suspense fallback={null}>
          <SlideReaderModal isOpen note={slide.note} initialPageNumber={slide.page} onClose={() => setSlide(null)} />
        </Suspense>
      )}
    </div>
  );
};
