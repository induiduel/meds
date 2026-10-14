import React, { useEffect, useMemo, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { ArrowRight, CornerDownLeft, Loader2, Moon, Search, Sun, X } from 'lucide-react';
import { fetchSearch, Highlight, TypeTag, TYPE_META, type SearchHit, type SearchResponse } from './searchShared';
import { DidYouMean, SuggestList, useQuerySuggest, type SuggestItem } from './QueryIntelUi';
import { navigateTo, pathFor, type AppRoute } from '../../router';
import { useAppearance } from '../../utils/appearance';
import { useTheme } from '../../utils/theme';
import { NAV_ITEMS } from '../shell/navModel';
import { BOLUMLER as SAGLIK_BOLUMLERI } from '../saglik/saglikVeri';

interface SearchPaletteProps {
  initialQuery?: string;
  committeeId?: string;
  onClose: () => void;
  /** Tüm sonuçlar sayfasına gider; focusId verilirse o sonuç açık gelir. hit: seçilen sonuç (kaynağında açılabilir) */
  onOpenResults: (query: string, focusId?: string, hit?: SearchHit) => void;
  /** v12: "Ara ya da git" — sayfa adları ve komutlar da listelenir; seçilince bu rota açılır */
  onGo?: (r: AppRoute) => void;
}

/** v12 sayfa/komut eşleşmesi için Türkçe katlama */
const foldTr = (t: string) => t.toLocaleLowerCase('tr-TR').normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/ı/g, 'i');
type PaletteAction = { key: string; label: string; meta: string; icon: React.ElementType; run: () => void };

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
export const SearchPalette: React.FC<SearchPaletteProps> = ({ initialQuery = '', committeeId, onClose, onOpenResults, onGo }) => {
  const v12 = useAppearance().design === 'v12';
  const { theme, toggle: toggleTheme } = useTheme();
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
      const res = await fetchSearch(query, { limit: 5, committeeId, fast: true }, ctrl.signal);
      if (ctrl.signal.aborted) return;
      setData(res);
      setFailed(!res);
      setLoading(false);
    }, 220);
    return () => { ctrl.abort(); window.clearTimeout(t); };
  }, [q, committeeId]);

  const rawResults = data?.results || [];
  const query = q.trim();
  // v12: sonuçlar türüne göre gruplanır (grup sırası = en alakalı sonucun türü önce; grup içi sıra korunur)
  const results = useMemo(() => {
    if (!v12 || rawResults.length < 2) return rawResults;
    const order: string[] = [];
    for (const r of rawResults) if (!order.includes(r.documentType)) order.push(r.documentType);
    return order.flatMap((t) => rawResults.filter((r) => r.documentType === t));
  }, [v12, rawResults]);
  // v12: sayfalar ve komutlar ("Ara ya da git")
  const actions = useMemo<PaletteAction[]>(() => {
    if (!v12 || !onGo) return [];
    const fq = foldTr(query);
    const go = (r: AppRoute) => () => { onGo(r); onClose(); };
    const pages: PaletteAction[] = fq
      ? Object.values(NAV_ITEMS)
          .filter((it) => foldTr(it.label).includes(fq) || (it.short && foldTr(it.short).includes(fq)) || foldTr(it.hint).split(/[\s,]+/).some((w) => w.startsWith(fq)))
          .slice(0, 4)
          .map((it) => ({ key: `p:${it.id}`, label: it.label, meta: 'sayfa', icon: it.icon, run: go(it.id) }))
      : [];
    const cmds: (PaletteAction & { words: string })[] = [
      { key: 'c:add', label: 'Soru ekle', meta: 'komut', icon: NAV_ITEMS.quick_add.icon, run: go('quick_add'), words: 'soru ekle katki yeni' },
      { key: 'c:theme', label: theme === 'dark' ? 'Aydınlık temaya geç' : 'Koyu temaya geç', meta: 'komut', icon: theme === 'dark' ? Sun : Moon, run: toggleTheme, words: 'tema koyu aydinlik karanlik gece' },
    ];
    const cmdHits = cmds.filter((c) => !fq || c.words.split(' ').some((w) => w.startsWith(fq)) || foldTr(c.label).includes(fq));
    // Sağlık Bakanlığı alt sayfaları (/saglik/<bölüm>): "aşı takvimi", "karabük", "yenidoğan tarama" doğrudan açılır
    const saglik: PaletteAction[] = fq.length >= 3
      ? SAGLIK_BOLUMLERI.filter((b) => b.slug && (foldTr(b.ad).includes(fq) || foldTr(b.aciklama).split(/[\s,:()]+/).some((w) => w.startsWith(fq))))
          .slice(0, 3)
          .map((b) => ({ key: `s:${b.id}`, label: `Sağlık Bakanlığı › ${b.ad}`, meta: 'sayfa', icon: b.icon, run: () => { navigateTo(`${pathFor('health_ministry')}/${b.slug}`); onClose(); } }))
      : [];
    return [...pages, ...saglik, ...cmdHits];
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [v12, onGo, query, theme]);
  const A = actions.length;
  // Yazarken öneriler: kavramlar + sözcük tamamlama + yazım düzeltmesi (sunucu ~1 ms, 90 ms bekleme)
  const sug = useQuerySuggest(q);
  const suggestions: SuggestItem[] = (sug?.q === q ? sug.suggestions : []).slice(0, 5);
  const correction = sug?.q === q ? sug.correction?.text : null;
  const S = suggestions.length;
  const pickSuggestion = (s: SuggestItem) => {
    // Kavram seçilince doğrudan aranır (sonuçlarda varlık kartı başta); sözcük önerisi kutuya yazılır, yazmaya devam
    if (s.kind === 'concept') { rememberSearch(s.value); onOpenResults(s.value); onClose(); return; }
    setQ(/\s$/.test(s.value) ? s.value : `${s.value} `);
    inputRef.current?.focus();
  };
  const seeAll = (focusId?: string) => {
    if (!query) return;
    rememberSearch(query);
    onOpenResults(query, focusId, focusId ? results.find((r) => r.id === focusId) : undefined);
    onClose();
  };

  const onKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') { e.preventDefault(); onClose(); }
    else if (e.key === 'ArrowDown') { e.preventDefault(); setCursor((c) => Math.min(S + results.length + A - 1, c + 1)); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); setCursor((c) => Math.max(-1, c - 1)); }
    else if (e.key === 'Tab' && !e.shiftKey && S > 0) { e.preventDefault(); pickSuggestion(suggestions[Math.max(0, Math.min(cursor, S - 1))]); }
    else if (e.key === 'Enter') {
      e.preventDefault();
      if (cursor >= 0 && cursor < S) pickSuggestion(suggestions[cursor]);
      else if (A > 0 && cursor >= S + results.length) actions[cursor - S - results.length]?.run();
      else seeAll(cursor >= S ? results[cursor - S]?.id : undefined);
    }
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
            placeholder={v12 && onGo ? 'Hastalık, ilaç, soru ara ya da sayfaya git…' : 'Hastalık, ilaç, bulgu, soru…'}
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
          {v12 && <kbd className="s12-kbd s12-pal-esc" aria-hidden="true">esc</kbd>}
          <button type="button" className="ms-search-cancel" onClick={onClose}>Vazgeç</button>
        </div>

        <div className="ms-search-body">
          {query.length < 2 ? (
            recent.length > 0 ? (
              <div className="p-2">
                <div className="px-2 pt-1 pb-2 text-xs font-semibold text-ink-3 s12-pal-gh">Son aramalar</div>
                {recent.map((r) => (
                  <button key={r} type="button" className="ms-search-row" onClick={() => setQ(r)}>
                    <Search className="w-4 h-4 text-ink-3 shrink-0" />
                    <span className="truncate text-md text-ink">{r}</span>
                  </button>
                ))}
              </div>
            ) : v12 && A > 0 ? null : (
              <p className="m-0 px-5 py-8 text-center text-base text-ink-3">
                Slaytlar, özetler, çıkmış sorular ve ses kayıtlarının tamamında arar.
              </p>
            )
          ) : null}
          {query.length >= 2 && (correction || S > 0) && (
            <div className="border-b border-line">
              {correction && <div className="px-2 pt-2"><DidYouMean text={correction} onPick={(t) => { setQ(t); inputRef.current?.focus(); }} /></div>}
              <SuggestList items={suggestions} cursor={cursor} onPick={pickSuggestion} onHover={setCursor} />
            </div>
          )}
          {query.length < 2 ? null : failed ? (
            <p className="m-0 px-5 py-8 text-center text-base text-ink-3">Arama şu an yapılamadı. Bağlantını kontrol edip tekrar dene.</p>
          ) : data && results.length === 0 && !loading ? (
            <p className="m-0 px-5 py-8 text-center text-base text-ink-3">“{query}” için sonuç bulunamadı.</p>
          ) : (
            <ul className="m-0 p-2 list-none" role="listbox" aria-label="Sonuçlar">
              {results.map((r, i) => v12 ? (
                <React.Fragment key={r.id}>
                  {(i === 0 || results[i - 1].documentType !== r.documentType) && (
                    <li role="presentation" className="s12-pal-gh">{TYPE_META[r.documentType]?.label || r.documentType}</li>
                  )}
                  <li role="option" aria-selected={i + S === cursor}>
                    <button
                      type="button"
                      className={`ms-search-hit s12-pal-hit ${i + S === cursor ? 'is-active' : ''}`}
                      onMouseEnter={() => setCursor(i + S)}
                      onClick={() => seeAll(r.id)}
                    >
                      <span className="s12-pal-hit-t">
                        <span className="ms-search-hit-title"><Highlight text={r.title} query={query} /></span>
                        <span className="ms-search-hit-snippet"><Highlight text={r.snippet} query={query} /></span>
                      </span>
                      {r.discipline && <span className="s12-pal-meta">{r.discipline}</span>}
                    </button>
                  </li>
                </React.Fragment>
              ) : (
                <li key={r.id} role="option" aria-selected={i + S === cursor}>
                  <button
                    type="button"
                    className={`ms-search-hit ${i + S === cursor ? 'is-active' : ''}`}
                    onMouseEnter={() => setCursor(i + S)}
                    onClick={() => seeAll(r.id)}
                  >
                    <span className="flex items-center gap-2 min-w-0">
                      <TypeTag type={r.documentType} />
                      {r.discipline && <span className="text-xs text-ink-3 truncate">· {r.discipline}</span>}
                    </span>
                    <span className="ms-search-hit-title"><Highlight text={r.title} query={query} /></span>
                    <span className="ms-search-hit-snippet"><Highlight text={r.snippet} query={query} /></span>
                  </button>
                </li>
              ))}
            </ul>
          )}
          {A > 0 && (
            <ul className="m-0 px-2 pb-2 list-none" role="listbox" aria-label="Sayfalar ve komutlar">
              {actions.map((a, j) => {
                const idx = S + results.length + j;
                const Icon = a.icon;
                const head = j === 0 || actions[j - 1].meta !== a.meta;
                return (
                  <React.Fragment key={a.key}>
                    {head && <li role="presentation" className="s12-pal-gh">{a.meta === 'sayfa' ? 'Sayfalar' : 'Komutlar'}</li>}
                    <li role="option" aria-selected={idx === cursor}>
                      <button type="button" className={`s12-pal-act ${idx === cursor ? 'is-active' : ''}`} onMouseEnter={() => setCursor(idx)} onClick={a.run}>
                        <Icon className="s12-pal-ico" aria-hidden="true" />
                        <span className="s12-pal-act-t">{a.label}</span>
                        <span className="s12-pal-meta">{a.meta}</span>
                      </button>
                    </li>
                  </React.Fragment>
                );
              })}
            </ul>
          )}
        </div>

        {v12 && (
          <div className="s12-pal-foot">
            <span className="s12-pal-keys" aria-hidden="true">
              <span><kbd className="s12-kbd">↑↓</kbd> seç</span>
              <span><kbd className="s12-kbd">↵</kbd> aç</span>
              {S > 0 && <span><kbd className="s12-kbd">tab</kbd> tamamla</span>}
            </span>
            <span className="s12-grow" />
            {query.length >= 2 && data && data.total > 0 ? (
              <button type="button" className="s12-pal-all" onClick={() => seeAll()}>
                Tümünü gör <span className="s12-pal-meta">· {totalLabel} sonuç</span>
                <ArrowRight className="s12-pal-ico" aria-hidden="true" />
              </button>
            ) : (
              <button type="button" className="s12-pal-close" onClick={onClose}>Kapat</button>
            )}
          </div>
        )}
        {!v12 && query.length >= 2 && data && data.total > 0 && (
          <button type="button" className="ms-search-footer" onClick={() => seeAll()}>
            <span className="min-w-0 truncate">Tümünü gör <span className="text-ink-3 font-normal">· {totalLabel} sonuç</span></span>
            <span className="hidden sm:inline-flex items-center gap-1 text-xs text-ink-3 font-normal">
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
