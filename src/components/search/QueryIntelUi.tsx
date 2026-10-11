import React, { useEffect, useRef, useState } from 'react';
import { ArrowUpLeft, BookA, CornerDownRight, Dna, FlaskConical, HeartPulse, Microscope, Pill, Sparkles, Stethoscope, Tag, Wand2 } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';

/**
 * Sorgu zekâsı arayüz parçaları (arama paleti + arama sayfası).
 *  - useQuerySuggest: yazarken /api/search/suggest (90 ms bekleme, iptal, istemci önbelleği). Sunucu ~1 ms yanıtlar,
 *    yanıt ayrıca 10 dk HTTP önbelleğinde; aynı önekte ağ isteği yok.
 *  - SuggestList: kavram (hastalık, ilaç, gen…) / sözcük / sonraki sözcük önerileri
 *  - UnderstandingBar: "Bunu mu kastettiniz?", tanınan kavramlar, niyet, eşanlamlı arama
 */

export interface SuggestItem {
  kind: 'concept' | 'word' | 'next' | 'fix';
  value: string;
  label: string;
  type?: string;
  ref?: { kind: string; id: string } | null;
  via?: string;
}

export interface ConceptLite {
  label: string;
  type: string;
  ref: { kind: string; id: string } | null;
}

export interface SuggestData {
  q: string;
  ready: boolean;
  suggestions: SuggestItem[];
  correction: { text: string; changes: { from: string; to: string }[] } | null;
  concepts: ConceptLite[];
  intent: string | null;
  ghost: string;
}

export interface Understanding {
  corrected: string | null;
  changes: { from: string; to: string }[];
  concepts: ConceptLite[];
  intent: string | null;
  rewrites: string[];
}

export const INTENT_LABEL: Record<string, string> = {
  treatment: 'Tedavi', diagnosis: 'Tanı', imaging: 'Görüntüleme', symptoms: 'Klinik bulgular', etiology: 'Etiyoloji',
  pathology: 'Patoloji', physiology: 'Fizyopatoloji', epidemiology: 'Epidemiyoloji', pathognomonic: 'Ayırıcı tanı',
};

export const CONCEPT_META: Record<string, { label: string; icon: React.ElementType }> = {
  disease: { label: 'Hastalık', icon: HeartPulse },
  drug: { label: 'İlaç', icon: Pill },
  gene: { label: 'Gen / protein', icon: Dna },
  pathogen: { label: 'Patojen', icon: Microscope },
  symptom: { label: 'Bulgu', icon: Stethoscope },
  procedure: { label: 'Tanı yöntemi', icon: FlaskConical },
  anatomy: { label: 'Anatomi', icon: Tag },
  term: { label: 'Terim', icon: BookA },
  topic: { label: 'Ders konusu', icon: BookA },
};

const cache = new Map<string, SuggestData>();

export function useQuerySuggest(q: string, enabled = true): SuggestData | null {
  const [data, setData] = useState<SuggestData | null>(null);
  const seq = useRef(0);
  useEffect(() => {
    if (!enabled || q.trim().length < 2) { setData(null); return; }
    const hit = cache.get(q);
    if (hit) { setData(hit); return; }
    const id = ++seq.current;
    const ctrl = new AbortController();
    const t = window.setTimeout(async () => {
      const res = await safeJsonFetch<SuggestData & { success: boolean }>(`/api/search/suggest?q=${encodeURIComponent(q)}&limit=6`, { signal: ctrl.signal });
      if (ctrl.signal.aborted || id !== seq.current) return;
      if (res.ok && res.data?.success) {
        if (res.data.ready) {
          cache.set(q, res.data);
          if (cache.size > 300) cache.delete(cache.keys().next().value as string);
        }
        setData(res.data);
      }
    }, 90);
    return () => { ctrl.abort(); window.clearTimeout(t); };
  }, [q, enabled]);
  return data;
}

export const ConceptIcon: React.FC<{ type?: string; className?: string }> = ({ type, className }) => {
  const Icon = (type && CONCEPT_META[type]?.icon) || Sparkles;
  return <Icon className={className || 'w-4 h-4'} aria-hidden />;
};

/** Öneri satırları: dokununca kutuya yazar (onPick), kavramda ayrıca türünü gösterir. */
export const SuggestList: React.FC<{
  items: SuggestItem[];
  cursor: number;
  onPick: (s: SuggestItem) => void;
  onHover?: (i: number) => void;
}> = ({ items, cursor, onPick, onHover }) => {
  if (!items.length) return null;
  return (
    <ul className="m-0 px-2 pt-2 pb-1 list-none" role="listbox" aria-label="Öneriler">
      {items.map((s, i) => (
        <li key={`${s.kind}-${s.value}`} role="option" aria-selected={i === cursor}>
          <button
            type="button"
            className={`ms-search-row ${i === cursor ? 'is-active' : ''}`}
            onMouseEnter={() => onHover?.(i)}
            onClick={() => onPick(s)}
          >
            {s.kind === 'concept' ? (
              <span className="w-7 h-7 rounded-lg bg-accent/10 text-accent grid place-items-center shrink-0"><ConceptIcon type={s.type} /></span>
            ) : (
              <span className="w-7 h-7 grid place-items-center shrink-0 text-ink-3"><CornerDownRight className="w-4 h-4" aria-hidden /></span>
            )}
            <span className="min-w-0 flex-1 text-left">
              <span className="block truncate text-md text-ink">{s.kind === 'concept' ? s.label : s.value}</span>
              {s.kind === 'concept' && (
                <span className="block truncate text-xs text-ink-3">
                  {CONCEPT_META[s.type || '']?.label || 'Kavram'}{s.via ? ` · “${s.via}”` : ''}
                </span>
              )}
            </span>
            <ArrowUpLeft className="w-4 h-4 text-ink-3 shrink-0" aria-hidden />
          </button>
        </li>
      ))}
    </ul>
  );
};

/** "Bunu mu kastettiniz?" satırı (paletteki yazım önerisi) */
export const DidYouMean: React.FC<{ text: string; onPick: (t: string) => void }> = ({ text, onPick }) => (
  <button type="button" className="ms-search-row" onClick={() => onPick(text)}>
    <span className="w-7 h-7 grid place-items-center shrink-0 text-warn"><Wand2 className="w-4 h-4" aria-hidden /></span>
    <span className="min-w-0 flex-1 text-left text-md text-ink-2 truncate">
      Bunu mu kastettin: <b className="text-ink font-semibold">{text}</b>
    </span>
  </button>
);

/**
 * Arama sayfasının üstünde: sorgunun nasıl anlaşıldığı.
 * Düzeltme uygulandıysa "… için sonuçlar · özgün sorguyla ara", tanınan kavramlar (hastalık sayfasına gider), niyet.
 */
export const UnderstandingBar: React.FC<{
  u: Understanding | undefined;
  query: string;
  onQuery: (q: string) => void;
  onOpenConcept: (c: ConceptLite) => void;
}> = ({ u, query, onQuery, onOpenConcept }) => {
  if (!u || (!u.corrected && !u.concepts.length && !u.intent && !u.rewrites.length)) return null;
  return (
    <div className="flex flex-col gap-2 rounded-2xl border border-line bg-surface px-3 py-2.5 text-sm">
      {u.corrected && (
        <p className="m-0 text-ink-2 flex items-center gap-1.5 flex-wrap">
          <Wand2 className="w-4 h-4 text-warn shrink-0" aria-hidden />
          <span><b className="text-ink">{u.corrected}</b> için sonuçlar gösteriliyor.</span>
          <button type="button" className="text-accent font-medium hover:underline" onClick={() => onQuery(`"${query}"`)}>“{query}” olarak ara</button>
        </p>
      )}
      {(u.concepts.length > 0 || u.intent) && (
        <div className="flex items-center gap-1.5 flex-wrap">
          {u.concepts.map((c) => {
            const openable = c.ref?.kind === 'disease' || c.ref?.kind === 'glossary';
            return (
              <button
                key={c.label}
                type="button"
                disabled={!openable}
                onClick={() => openable && onOpenConcept(c)}
                className={`inline-flex items-center gap-1.5 rounded-full border border-line px-2.5 py-1 text-ink ${openable ? 'hover:border-accent hover:text-accent' : 'cursor-default'}`}
                title={openable ? `${CONCEPT_META[c.type]?.label || 'Kavram'} sayfasını aç` : CONCEPT_META[c.type]?.label}
              >
                <ConceptIcon type={c.type} className="w-3.5 h-3.5" />
                <span className="truncate max-w-[16rem]">{c.label}</span>
              </button>
            );
          })}
          {u.intent && (
            <span className="inline-flex items-center gap-1 rounded-full bg-accent/10 text-accent px-2.5 py-1 font-medium">
              {INTENT_LABEL[u.intent] || u.intent} odaklı
            </span>
          )}
        </div>
      )}
      {u.rewrites.length > 0 && (
        <p className="m-0 text-ink-3 flex items-center gap-1.5 flex-wrap">
          <span>Eşanlamlıyla da arandı:</span>
          {u.rewrites.map((r) => (
            <button key={r} type="button" className="text-accent hover:underline" onClick={() => onQuery(r)}>{r}</button>
          ))}
        </p>
      )}
    </div>
  );
};
