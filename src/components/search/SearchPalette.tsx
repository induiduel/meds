import React, { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { ArrowRight, CornerDownLeft, Loader2, Search, X } from 'lucide-react';
import { fetchSearch, Highlight, TypeTag, type SearchResponse } from './searchShared';

interface SearchPaletteProps {
  initialQuery?: string;
  committeeId?: string;
  onClose: () => void;
  /** Tüm sonuçlar sayfasına gider; focusId verilirse o sonuç açık gelir */
  onOpenResults: (query: string, focusId?: string) => void;
}

const RECENT_KEY = 'medsoru_recent_searches';
const readRecent = (): string[] => {
  try { return JSON.parse(localStorage.getItem(RECENT_KEY) || '[]').slice(0, 5); } catch { return []; }
};
export const rememberSearch = (q: string) => {
  try {
    const next = [q, ...readRecent().filter((r) => r !== q)].slice(0, 5);
    localStorage.setItem(RECENT_KEY, JSON.stringify(next));
  } catch { /* gizli pencere */ }
};

/** Komut paleti tarzı hızlı arama: yazdıkça en alakalı 5 sonuç (BM25). */
export const SearchPalette: React.FC<SearchPaletteProps> = ({ initialQuery = '', committeeId, onClose, onOpenResults }) => {
  const [q, setQ] = useState(initialQuery);
  const [data, setData] = useState<SearchResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [failed, setFailed] = useState(false);
  const [cursor, setCursor] = useState(-1);
  const [recent] = useState(readRecent);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    inputRef.current?.focus();
    inputRef.current?.select();
    const prev = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => { document.body.style.overflow = prev; };
  }, []);

  useEffect(() => {
    const query = q.trim();
    setCursor(-1);
    if (query.length < 2) { setData(null); setLoading(false); setFailed(false); return; }
    const ctrl = new AbortController();
    setLoading(true);
    const t = window.setTimeout(async () => {
      const res = await fetchSearch(query, { limit: 5, committeeId }, ctrl.signal);
      if (ctrl.signal.aborted) return;
      setData(res);
      setFailed(!res);
      setLoading(false);
    }, 200);
    return () => { ctrl.abort(); window.clearTimeout(t); };
  }, [q, committeeId]);

  const results = data?.results || [];
  const query = q.trim();
  const seeAll = (focusId?: string) => {
    if (!query) return;
    rememberSearch(query);
    onOpenResults(query, focusId);
    onClose();
  };

  const onKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') { e.preventDefault(); onClose(); }
    else if (e.key === 'ArrowDown') { e.preventDefault(); setCursor((c) => Math.min(results.length - 1, c + 1)); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); setCursor((c) => Math.max(-1, c - 1)); }
    else if (e.key === 'Enter') { e.preventDefault(); seeAll(cursor >= 0 ? results[cursor]?.id : undefined); }
  };

  const totalLabel = data ? `${data.total}${data.capped ? '+' : ''}` : '';

  return createPortal(
    <div className="ms-search-overlay" onMouseDown={(e) => e.target === e.currentTarget && onClose()}>
      <div className="ms-search-panel" role="dialog" aria-modal="true" aria-label="Ara">
        <div className="ms-search-field">
          <Search className="w-[18px] h-[18px] text-ink-3 shrink-0" />
          <input
            ref={inputRef}
            type="search"
            value={q}
            onChange={(e) => setQ(e.target.value)}
            onKeyDown={onKeyDown}
            placeholder="Hastalık, ilaç, bulgu, soru…"
            aria-label="Tüm kaynaklarda ara"
            enterKeyHint="search"
            autoComplete="off"
            spellCheck={false}
          />
          {loading ? (
            <Loader2 className="w-4 h-4 text-ink-3 animate-spin shrink-0" />
          ) : q ? (
            <button type="button" className="ms-search-icon-btn" onClick={() => { setQ(''); inputRef.current?.focus(); }} aria-label="Temizle">
              <X className="w-4 h-4" />
            </button>
          ) : null}
          <button type="button" className="ms-search-cancel" onClick={onClose}>Vazgeç</button>
        </div>

        <div className="ms-search-body">
          {query.length < 2 ? (
            recent.length > 0 ? (
              <div className="p-2">
                <div className="px-2 pt-1 pb-2 text-[12px] font-semibold text-ink-3">Son aramalar</div>
                {recent.map((r) => (
                  <button key={r} type="button" className="ms-search-row" onClick={() => setQ(r)}>
                    <Search className="w-4 h-4 text-ink-3 shrink-0" />
                    <span className="truncate text-[15px] text-ink">{r}</span>
                  </button>
                ))}
              </div>
            ) : (
              <p className="m-0 px-5 py-8 text-center text-[14px] text-ink-3">
                Slaytlar, özetler, çıkmış sorular ve ses kayıtlarının tamamında arar.
              </p>
            )
          ) : failed ? (
            <p className="m-0 px-5 py-8 text-center text-[14px] text-ink-3">Arama şu an yapılamadı. Bağlantını kontrol edip tekrar dene.</p>
          ) : data && results.length === 0 && !loading ? (
            <p className="m-0 px-5 py-8 text-center text-[14px] text-ink-3">“{query}” için sonuç bulunamadı.</p>
          ) : (
            <ul className="m-0 p-2 list-none" role="listbox">
              {results.map((r, i) => (
                <li key={r.id} role="option" aria-selected={i === cursor}>
                  <button
                    type="button"
                    className={`ms-search-hit ${i === cursor ? 'is-active' : ''}`}
                    onMouseEnter={() => setCursor(i)}
                    onClick={() => seeAll(r.id)}
                  >
                    <span className="flex items-center gap-2 min-w-0">
                      <TypeTag type={r.documentType} />
                      {r.discipline && <span className="text-[12px] text-ink-3 truncate">· {r.discipline}</span>}
                    </span>
                    <span className="ms-search-hit-title"><Highlight text={r.title} query={query} /></span>
                    <span className="ms-search-hit-snippet"><Highlight text={r.snippet} query={query} /></span>
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>

        {query.length >= 2 && data && data.total > 0 && (
          <button type="button" className="ms-search-footer" onClick={() => seeAll()}>
            <span className="min-w-0 truncate">Tümünü gör <span className="text-ink-3 font-normal">· {totalLabel} sonuç</span></span>
            <span className="hidden sm:inline-flex items-center gap-1 text-[12px] text-ink-3 font-normal">
              <CornerDownLeft className="w-3.5 h-3.5" /> Enter
            </span>
            <ArrowRight className="sm:hidden w-4 h-4" />
          </button>
        )}
      </div>
    </div>,
    document.body
  );
};
