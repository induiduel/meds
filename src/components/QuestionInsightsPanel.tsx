import React, { useEffect, useState } from 'react';
import { ChevronDown, GraduationCap, Tags } from 'lucide-react';
import { safeJsonFetch } from '../services/api';

/**
 * Çıkmış soru kartında "Müfredat & Kaynak" paneli.
 * Veri: /api/questions/:id/insights — gösterilen: müfredat kazanımı (Faz 9 birleşik, Faz 8 öncelikli, yalnız yüksek güven),
 * Faz 5/6.5 terimleri, eş anlamlılar ve kanıtlı sözlükten kısaltma açılımları.
 * Açılınca bir kez yüklenir; analiz yoksa panel hiç görünmez.
 */

const cache = new Map<string, any | null>();

function Chips({ items }: { items: string[] }) {
  if (!items.length) return null;
  return (
    <div className="flex flex-wrap gap-1.5">
      {items.map((t) => (
        <span key={t} className="px-2 py-0.5 rounded-full bg-canvas text-[12px] text-ink-2">
          {t}
        </span>
      ))}
    </div>
  );
}

export function QuestionInsightsPanel({ questionId }: { questionId: string }) {
  const [open, setOpen] = useState(false);
  const [data, setData] = useState<any | null | undefined>(cache.has(questionId) ? cache.get(questionId) : undefined);
  const [probed, setProbed] = useState(cache.has(questionId));

  // Panel başlığını yalnızca analizi olan sorularda göstermek için hafif ön yükleme
  useEffect(() => {
    if (cache.has(questionId)) return;
    let alive = true;
    safeJsonFetch<{ insights: any }>(`/api/questions/${encodeURIComponent(questionId)}/insights`).then((r) => {
      const v = r.ok ? r.data?.insights || null : null;
      cache.set(questionId, v);
      if (alive) {
        setData(v);
        setProbed(true);
      }
    });
    return () => {
      alive = false;
    };
  }, [questionId]);

  if (!probed || !data) return null;

  // Yalnızca kazanım (Faz 8 yüksek güven), terimler ve eş anlamlılar gösterilir; diğer faz alanları gizli.
  const f5 = data.faz5;
  const f65 = data.faz6_5;
  const k = (data.mufredat || data.faz8)?.kazanimlar?.[0]; // mufredat: Faz 9 birleşik (Faz 8 öncelikli)
  const terms: string[] = Array.from(new Set<string>([...(f65?.terimler || []), ...(f5?.terimler || [])])).slice(0, 12);
  const synonyms = Object.entries((f65?.esanlamlilar || {}) as Record<string, string[]>).filter(([, v]) => v?.length);
  if (!k && !terms.length && !synonyms.length) return null;
  const baslik = k ? [k.ders, k.konu].filter(Boolean).join(' · ') : 'Terimler';

  return (
    <div className="rounded-xl bg-field">
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        aria-expanded={open}
        className="w-full min-h-11 px-3.5 py-2 flex items-center justify-between gap-2 text-left text-[14px] font-semibold text-ink cursor-pointer"
      >
        <span className="flex items-center gap-1.5 min-w-0">
          <GraduationCap className="w-4 h-4 text-ink-3 shrink-0" />
          <span className="truncate">{baslik}</span>
        </span>
        <ChevronDown className={`w-4 h-4 text-ink-3 shrink-0 transition-transform ${open ? 'rotate-180' : ''}`} />
      </button>
      {open && (
        <div className="px-3.5 pb-3.5 flex flex-col gap-3 text-[13.5px] text-ink-2">
          {k && (
            <section className="flex flex-col gap-1">
              <h4 className="m-0 text-[12px] font-semibold uppercase tracking-wide text-ink-3">{k.kazanim ? 'Kazanım' : 'Müfredat'}</h4>
              {k.kazanim && <p className="m-0 text-ink">{k.kazanim}</p>}
              <p className="m-0 text-[12px] text-ink-3">
                {['Kurul ' + k.kurul, k.ders, k.konu].filter(Boolean).join(' · ')}
              </p>
            </section>
          )}

          {(terms.length > 0 || synonyms.length > 0) && (
            <section className="flex flex-col gap-1.5">
              <h4 className="m-0 text-[12px] font-semibold uppercase tracking-wide text-ink-3 flex items-center gap-1">
                <Tags className="w-3.5 h-3.5" /> Terimler
              </h4>
              <Chips items={terms} />
              {synonyms.map(([t, syn]) => (
                <p key={t} className="m-0 text-[12.5px]">
                  <span className="font-semibold text-ink">{t}</span> = {syn.join(', ')}
                </p>
              ))}
            </section>
          )}
        </div>
      )}
    </div>
  );
}
