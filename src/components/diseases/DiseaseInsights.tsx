import React, { useEffect, useState } from 'react';
import { ArrowUpRight, BookOpen, ClipboardPlus, GitBranch, Loader2, ShieldAlert, ShieldCheck } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import type { DiseaseProfile } from '../../types/disease';
import { ConceptIcon, CONCEPT_META } from '../search/QueryIntelUi';
import './diseaseInsights.css';

/**
 * Hastalık bilgi grafiği (sunucu: /api/diseases/:id/insights) arayüzü.
 *  - Profil alanı şablon/dolgu ise yerine ders kaynaklarından çıkarılmış kanıt cümleleri (kaynak künyeli) gösterilir
 *  - Kalite şeridi: dolu / dolgu / boş bölüm sayısı, güncellenebilir bölümler
 *  - İlişkili kavramlar ve hastalıklar (aynı cümlede geçiş × özgüllük; "ayırıcı tanı" bağlamı işaretli)
 *  - "Forma aktar": kanıt cümlesi düzenleme formunun ilgili alanına eklenir (insan onayıyla güncelleme)
 */

export type SectionKey = 'treatment' | 'diagnosis' | 'imaging' | 'symptoms' | 'etiology' | 'pathology' | 'physiology' | 'epidemiology' | 'pathognomonic' | 'general';
export type FieldStatus = 'ok' | 'placeholder' | 'empty';

export interface Evidence {
  t: string;
  section: SectionKey;
  score: number;
  src: { type: string; title: string; chunkId: string; committee?: string; discipline?: string };
}

export interface DiseaseInsightsData {
  id: string;
  name: string;
  mentions: number;
  byType: Record<string, number>;
  sources: Array<{ title: string; type: string; n: number }>;
  evidence: Partial<Record<SectionKey, Evidence[]>>;
  related: Array<{ label: string; type: string; ref: string; w: number }>;
  relatedDiseases: Array<{ id: string; name: string; w: number; ddx: boolean }>;
  audit: { fields: Partial<Record<SectionKey, FieldStatus>>; completeness: number; updatable: SectionKey[]; flags: string[]; priority: number } | null;
  builtAt: string | null;
  mode: 'graph' | 'live';
}

const SRC_LABEL: Record<string, string> = {
  lecture_slide: 'Ders slaytı', summary: 'Özet', transcript: 'Ses kaydı', past_question: 'Çıkmış soru', ornek_question: 'Örnek soru', deck_slide: 'İnteraktif slayt',
};

const SECTION_TITLE: Record<SectionKey, string> = {
  symptoms: 'Klinik bulgular', pathognomonic: 'Patognomonik', etiology: 'Etiyoloji', physiology: 'Fizyopatoloji', pathology: 'Patoloji',
  diagnosis: 'Tanı', imaging: 'Görüntüleme', treatment: 'Tedavi', epidemiology: 'Epidemiyoloji', general: 'Genel',
};

const cache = new Map<string, DiseaseInsightsData>();

export function useDiseaseInsights(d: DiseaseProfile | null): { data: DiseaseInsightsData | null; loading: boolean } {
  const [data, setData] = useState<DiseaseInsightsData | null>(null);
  const [loading, setLoading] = useState(false);
  useEffect(() => {
    if (!d) { setData(null); return; }
    const key = `${d.id}|${d.updatedAt}`;
    const hit = cache.get(key);
    if (hit) { setData(hit); return; }
    const ctrl = new AbortController();
    setLoading(true);
    setData(null);
    // Grafikte olmayan (kullanıcı eklemesi) profil için ad + Latince ad ile anlık analiz
    const qs = new URLSearchParams({ name: d.name });
    if (d.latinName) qs.set('latin', d.latinName);
    safeJsonFetch<{ success: boolean; insights: DiseaseInsightsData }>(`/api/diseases/${encodeURIComponent(d.id)}/insights?${qs}`, { signal: ctrl.signal }).then((res) => {
      if (ctrl.signal.aborted) return;
      setLoading(false);
      if (res.ok && res.data?.success) {
        cache.set(key, res.data.insights);
        if (cache.size > 60) cache.delete(cache.keys().next().value as string);
        setData(res.data.insights);
      }
    });
    return () => ctrl.abort();
  }, [d?.id, d?.updatedAt]);
  return { data, loading };
}

/** Bölümün gösterilecek maddeleri: profil alanı gerçekse kendisi; dolgu/boşsa null (kanıt gösterilir) */
export function realItems(items: string[] | undefined, status: FieldStatus | undefined): string[] | null {
  if (status && status !== 'ok') return null;
  return items || [];
}

export const EvidenceList: React.FC<{ items?: Evidence[]; onAdopt?: (e: Evidence) => void; limit?: number }> = ({ items, onAdopt, limit = 4 }) => {
  const [all, setAll] = useState(false);
  if (!items?.length) return null;
  const shown = all ? items : items.slice(0, limit);
  return (
    <div className="dz-ev">
      <p className="dz-ev-h"><BookOpen aria-hidden /> Ders kaynaklarından</p>
      <ul className="dz-ev-list">
        {shown.map((e, i) => (
          <li key={i}>
            <p className="dz-ev-t">{e.t}</p>
            <p className="dz-ev-src">
              <span>{SRC_LABEL[e.src.type] || e.src.type}</span>
              {e.src.title && <span className="truncate">· {e.src.title}</span>}
              {onAdopt && (
                <button type="button" className="dz-ev-adopt" onClick={() => onAdopt(e)} title="Bu cümleyi düzenleme formunda ilgili alana ekle">
                  <ClipboardPlus aria-hidden /> Forma aktar
                </button>
              )}
            </p>
          </li>
        ))}
      </ul>
      {items.length > limit && (
        <button type="button" className="dz-ev-more" onClick={() => setAll((v) => !v)}>{all ? 'Daha az göster' : `${items.length - limit} kanıt daha`}</button>
      )}
    </div>
  );
};

export const QualityStrip: React.FC<{ data: DiseaseInsightsData | null; loading: boolean }> = ({ data, loading }) => {
  if (loading && !data) return <p className="dz-q is-loading"><Loader2 className="animate-spin" aria-hidden /> Kaynaklar analiz ediliyor…</p>;
  if (!data?.audit) return null;
  const f = Object.values(data.audit.fields);
  const ok = f.filter((x) => x === 'ok').length;
  const weak = f.length - ok;
  const pct = Math.round(data.audit.completeness * 100);
  const good = pct >= 70;
  return (
    <div className={`dz-q ${good ? 'is-good' : 'is-weak'}`}>
      <span className="dz-q-ic" aria-hidden>{good ? <ShieldCheck /> : <ShieldAlert />}</span>
      <div className="dz-q-body">
        <p className="dz-q-t">
          Profil doluluğu <b>%{pct}</b>
          <span> · {ok} bölüm kaynaklı{weak ? `, ${weak} bölüm şablon/boş` : ''} · {data.mentions.toLocaleString('tr-TR')} kaynak cümlesi</span>
        </p>
        <div className="dz-q-bar" aria-hidden><i style={{ width: `${pct}%` }} /></div>
        {data.audit.updatable.length > 0 && (
          <p className="dz-q-s">Kaynakta bilgisi olan eksik bölümler: {data.audit.updatable.map((s) => SECTION_TITLE[s]).join(', ')}</p>
        )}
      </div>
    </div>
  );
};

export const RelatedPanel: React.FC<{
  data: DiseaseInsightsData | null;
  onOpenDisease: (id: string) => void;
  onSearch: (q: string) => void;
}> = ({ data, onOpenDisease, onSearch }) => {
  if (!data || (!data.related.length && !data.relatedDiseases.length)) return null;
  return (
    <section className="dz-sec is-ai">
      <header className="dz-sec-h">
        <span className="dz-sec-ic" aria-hidden><GitBranch /></span>
        <h4>Bağlantılı kavramlar</h4>
      </header>
      {data.relatedDiseases.length > 0 && (
        <>
          <h5 className="dz-sub">İlişkili hastalıklar</h5>
          <div className="dz-chips">
            {data.relatedDiseases.map((r) => (
              <button key={r.id} type="button" className="dz-chip" onClick={() => onOpenDisease(r.id)} title={r.ddx ? 'Kaynaklarda ayırıcı tanı bağlamında geçiyor' : 'Kaynaklarda birlikte geçiyor'}>
                <ConceptIcon type="disease" className="w-3.5 h-3.5" /> {r.name}{r.ddx && <em>ayırıcı tanı</em>}
              </button>
            ))}
          </div>
        </>
      )}
      {data.related.length > 0 && (
        <>
          <h5 className="dz-sub">Sık birlikte geçen kavramlar</h5>
          <div className="dz-chips">
            {data.related.slice(0, 14).map((r) => (
              <button key={r.ref} type="button" className="dz-chip" onClick={() => onSearch(`${data.name.replace(/\s*\([^)]*\)/g, '')} ${r.label}`)} title={`${CONCEPT_META[r.type]?.label || 'Kavram'} — ikisini birlikte ara`}>
                <ConceptIcon type={r.type} className="w-3.5 h-3.5" /> {r.label} <ArrowUpRight className="w-3 h-3 opacity-60" aria-hidden />
              </button>
            ))}
          </div>
        </>
      )}
      {data.sources.length > 0 && (
        <>
          <h5 className="dz-sub">En çok geçtiği kaynaklar</h5>
          <ul className="dz-srclist">
            {data.sources.slice(0, 5).map((s, i) => (
              <li key={i}><span>{SRC_LABEL[s.type] || s.type}</span> {s.title} <b>{s.n}</b></li>
            ))}
          </ul>
        </>
      )}
    </section>
  );
};
