import React, { useEffect, useState } from 'react';
import { ChevronDown, GraduationCap, Tags } from 'lucide-react';
import { safeJsonFetch } from '../services/api';
import { SourceText } from './ui/SourceText';

/**
 * Çıkmış soru kartında "Müfredat & Kaynak" paneli.
 * Veri: /api/questions/:id/insights — gösterilen: müfredat kazanımı (Faz 9 birleşik, Faz 8 öncelikli, yalnız yüksek güven),
 * Faz 5/6.5 terimleri, eş anlamlılar ve kanıtlı sözlükten kısaltma açılımları.
 * Açılınca bir kez yüklenir; analiz yoksa panel hiç görünmez.
 */

const cache = new Map<string, any | null>();

/** Yönetim konsolunda elle düzeltme sonrası önizlemenin yeniden yüklenmesi için. */
export function clearInsightsCache(questionId?: string) {
  if (questionId) cache.delete(questionId);
  else cache.clear();
}

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

/** bare: başlık/aç-kapa olmadan, içerik doğrudan (ör. "Hakkında" penceresinde) */
export function QuestionInsightsPanel({
  questionId,
  bare = false,
  onOpenSlide,
}: {
  questionId: string;
  bare?: boolean;
  onOpenSlide?: (kaynak: string, sayfa: number) => void;
}) {
  const [open, setOpen] = useState(bare);
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

  if (!probed) return bare ? <p className="m-0 text-[12.5px] text-ink-3">Müfredat bilgisi yükleniyor…</p> : null;
  if (!data) return bare ? <p className="m-0 text-[12.5px] text-ink-3">Bu soru için müfredat analizi henüz yok.</p> : null;

  const f5 = data.faz5;
  const f65 = data.faz6_5;
  const f6 = data.faz6;
  const mf = data.mufredat || data.faz8; // mufredat: sınav başlığı / Faz 9 birleşik (Faz 8 öncelikli)
  const k = mf?.kazanimlar?.[0];
  const ents: { ad: string }[] = Array.isArray(data.varliklar) ? data.varliklar : [];
  const f65Terms = Array.isArray(f65?.terimler) ? f65.terimler : [];
  const f5Terms = Array.isArray(f5?.terimler) ? f5.terimler : [];
  // Faz 13 kimlikli varlıklar önce; sonra Faz 6.5 / Faz 5 terimleri
  const terms: string[] = Array.from(new Set<string>([...ents.map((e) => e?.ad).filter(Boolean), ...f65Terms, ...f5Terms])).slice(0, 14);
  const synonyms = Object.entries((f65?.esanlamlilar || {}) as Record<string, string[]>).filter(([, v]) => Array.isArray(v) && v.length);
  const abbrs = Object.entries((f65?.kisaltmalar || {}) as Record<string, string>);
  const slides: { kaynak: string; sayfa: number; alinti?: string }[] = Array.isArray(data.slayt?.slaytlar) ? data.slayt.slaytlar : [];
  const ddx: { hastalik: string; ozellik?: string }[] = Array.isArray(f6?.ayirici_tani) ? f6.ayirici_tani : [];
  const icd: string[] = Array.isArray(f6?.icd10) ? f6.icd10 : [];
  if (!k && !terms.length && !synonyms.length && !abbrs.length && !slides.length && !ddx.length) return bare ? <p className="m-0 text-[12.5px] text-ink-3">Bu soru için müfredat analizi henüz yok.</p> : null;
  const baslik = k ? [k.ders, k.konu].filter(Boolean).join(' · ') : slides.length ? 'İlgili slaytlar' : 'Terimler';
  const h4 = 'm-0 text-[12px] font-semibold uppercase tracking-wide text-ink-3 flex items-center gap-1';

  const content = (
    <>
      {k && (
        <section className="flex flex-col gap-1">
          <h4 className={h4}>{k.kazanim ? 'Kazanım' : 'Müfredat'}{mf?.dogrulama === 'sinav_basligi' ? ' · sınav başlığından' : ' · Faz 8'}</h4>
          {k.kazanim && <p className="m-0 text-ink">{k.kazanim}</p>}
          <p className="m-0 text-[12px] text-ink-3">{['Kurul ' + k.kurul, k.ders, k.konu].filter(Boolean).join(' · ')}</p>
        </section>
      )}

      {slides.length > 0 && (
        <section className="flex flex-col gap-1.5">
          <h4 className={h4}>
            İlgili slaytlar
            <span className="normal-case tracking-normal font-normal">· eşleşme güveni {data.slayt?.guven || '-'}</span>
          </h4>
          {slides.slice(0, 3).map((sl) => (
            <div key={`${sl.kaynak}-${sl.sayfa}`} className="rounded-lg bg-canvas px-3 py-2 flex items-center justify-between gap-2 border border-line-2/50">
              <div className="min-w-0 flex-1">
                <p className="m-0 text-[13px] font-semibold text-ink truncate">
                  {sl.kaynak} <span className="font-normal text-ink-3">· sayfa {sl.sayfa}</span>
                </p>
                {sl.alinti && <SourceText text={sl.alinti.replace(/^\[[^\]]*\]\s*/, '')} size="sm" terms={terms.slice(0, 8)} />}
              </div>
              {onOpenSlide && (
                <button
                  type="button"
                  onClick={() => onOpenSlide(sl.kaynak, sl.sayfa)}
                  className="ms-btn is-tonal is-sm shrink-0"
                  title="İlgili slayta yönlendir"
                >
                  <GraduationCap className="w-3.5 h-3.5" /> <span className="hidden sm:inline">Slayta Git</span>
                </button>
              )}
            </div>
          ))}
        </section>
      )}

      {abbrs.length > 0 && (
        <section className="flex flex-col gap-1">
          <h4 className={h4}>Kısaltmalar</h4>
          {abbrs.map(([ab, exp]) => (
            <p key={ab} className="m-0 text-[12.5px]">
              <span className="font-semibold text-ink">{ab}</span> = {exp}
            </p>
          ))}
        </section>
      )}

      {(terms.length > 0 || synonyms.length > 0) && (
        <section className="flex flex-col gap-1.5">
          <h4 className={h4}>
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

      {(ddx.length > 0 || icd.length > 0) && (
        <section className="flex flex-col gap-1">
          <h4 className={h4}>
            Ayırıcı tanı
            <span className="normal-case tracking-normal font-normal">· {f6?.dogrulanmadi ? 'yapay zekâ, doğrulanmadı' : 'ders materyaliyle desteklenen'}</span>
          </h4>
          {ddx.slice(0, 5).map((d) => (
            <p key={d.hastalik} className="m-0 text-[12.5px]">
              <span className="font-semibold text-ink">{d.hastalik}</span>
              {d.ozellik ? ` — ${d.ozellik}` : ''}
            </p>
          ))}
          {icd.length > 0 && <p className="m-0 text-[12px] text-ink-3">ICD-10: {icd.join(', ')}</p>}
        </section>
      )}
    </>
  );

  if (bare) return <div className="flex flex-col gap-3.5 text-[13.5px] text-ink-2">{content}</div>;

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
      {open && <div className="px-3.5 pb-3.5 flex flex-col gap-3 text-[13.5px] text-ink-2">{content}</div>}
    </div>
  );
}
