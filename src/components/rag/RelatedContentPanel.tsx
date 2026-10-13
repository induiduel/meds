import React, { useEffect, useRef, useState } from 'react';
import { Layers, Sparkles } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { linkClick, navigateTo } from '../../router';

type RelatedItem = {
  id: string;
  documentId: string;
  documentType: string;
  title: string;
  pageNumber: number | null;
  similarity: number;
  snippet: string;
  link: string | null;
};

const TYPE_LABEL: Record<string, string> = {
  lecture_slide: 'Slayt',
  summary: 'Özet',
  deck_slide: 'Öğren',
  disease: 'Hastalık',
  glossary_term: 'Sözlük',
  transcript: 'Ders kaydı',
  past_question: 'Çıkmış',
  ornek_question: 'Örnek soru',
};

type Mode = 'ilgili' | 'benzer';

/**
 * Anlamsal olarak ilişkili içerik (saklanan bge-m3 vektörlerinden, /api/rag/related): soruya en yakın ders materyali
 * ve benzer sorular. Yalnız görünür olunca ve sekme başına bir kez istek atar; yanıt sunucuda 10 dk önbellektedir.
 */
export const RelatedContentPanel: React.FC<{ questionId: string; title?: string }> = ({ questionId, title = 'Anlamca ilişkili' }) => {
  const ref = useRef<HTMLElement | null>(null);
  const [visible, setVisible] = useState(false);
  const [mode, setMode] = useState<Mode>('ilgili');
  const [data, setData] = useState<Partial<Record<Mode, RelatedItem[] | 'hata'>>>({});

  useEffect(() => {
    const el = ref.current;
    if (!el || visible) return;
    if (typeof IntersectionObserver === 'undefined') { setVisible(true); return; }
    const io = new IntersectionObserver((es) => { if (es.some((e) => e.isIntersecting)) { setVisible(true); io.disconnect(); } }, { rootMargin: '200px' });
    io.observe(el);
    return () => io.disconnect();
  }, [visible]);

  useEffect(() => {
    if (!visible || data[mode] !== undefined) return;
    let alive = true;
    const qs = new URLSearchParams({ type: 'past_question', doc: questionId, mod: mode, limit: '6' });
    safeJsonFetch<{ items: RelatedItem[] }>(`/api/rag/related?${qs}`).then((r) => {
      if (!alive) return;
      setData((d) => ({ ...d, [mode]: r.ok && r.data ? r.data.items || [] : 'hata' }));
    });
    return () => { alive = false; };
  }, [visible, mode, questionId, data]);

  const items = data[mode];
  return (
    <section ref={ref} className="flex flex-col gap-2" aria-busy={items === undefined}>
      <div className="flex items-center justify-between gap-2 flex-wrap">
        <h3 className="m-0 text-xs font-bold uppercase tracking-[0.07em] text-ink-3 flex items-center gap-1.5">
          <Sparkles className="w-3.5 h-3.5" /> {title}
        </h3>
        <div className="flex gap-1" role="tablist" aria-label="İlişkili içerik türü">
          {(['ilgili', 'benzer'] as Mode[]).map((m) => (
            <button
              key={m}
              type="button"
              role="tab"
              aria-selected={mode === m}
              onClick={() => setMode(m)}
              className={`ms-btn is-sm h-7 px-2.5 text-xs ${mode === m ? 'is-tonal' : 'is-ghost'}`}
            >
              {m === 'ilgili' ? 'Ders materyali' : 'Benzer sorular'}
            </button>
          ))}
        </div>
      </div>
      {items === undefined ? (
        <div className="flex flex-col gap-1.5" aria-hidden="true">
          {[0, 1, 2].map((i) => <div key={i} className="h-12 rounded-lg bg-field animate-pulse" />)}
        </div>
      ) : items === 'hata' ? (
        <p className="m-0 text-sm text-ink-3">İlişkili içerik şu an alınamadı.</p>
      ) : items.length === 0 ? (
        <p className="m-0 text-sm text-ink-3">{mode === 'ilgili' ? 'Bu soruya yeterince yakın ders materyali bulunamadı.' : 'Benzer soru bulunamadı.'}</p>
      ) : (
        <ul className="m-0 p-0 list-none flex flex-col gap-1.5">
          {items.map((it) => {
            const body = (
              <>
                <div className="flex items-center gap-1.5 min-w-0">
                  <span className="ms-tag shrink-0">{TYPE_LABEL[it.documentType] || it.documentType}</span>
                  <span className="text-sm font-semibold text-ink truncate">{it.title}</span>
                  {it.pageNumber && it.documentType === 'lecture_slide' ? <span className="text-xs text-ink-3 shrink-0">s. {it.pageNumber}</span> : null}
                  <span className="ml-auto text-xs tabular-nums text-ink-3 shrink-0" title="Anlamsal benzerlik">%{Math.round(it.similarity * 100)}</span>
                </div>
                <p className="m-0 mt-0.5 text-sm text-ink-2 leading-snug line-clamp-2">{it.snippet}</p>
              </>
            );
            return (
              <li key={it.id}>
                {it.link ? (
                  <a
                    href={it.link}
                    onClick={linkClick(() => navigateTo(it.link!))}
                    className="block rounded-lg px-3 py-2 bg-field hover:bg-ink/5 no-underline text-inherit"
                  >
                    {body}
                  </a>
                ) : (
                  <div className="rounded-lg px-3 py-2 bg-field">{body}</div>
                )}
              </li>
            );
          })}
        </ul>
      )}
      {Array.isArray(items) && items.length > 0 && (
        <p className="m-0 text-[11px] text-ink-3 flex items-center gap-1"><Layers className="w-3 h-3" /> Anlam benzerliğiyle bulundu; kaynak teyidi değildir.</p>
      )}
    </section>
  );
};
