import React, { useEffect, useMemo, useState } from 'react';
import { Check, Crown, Split, Undo2, Copy, Info, CheckCircle2, ChevronDown } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { toast } from '../ui/Toast';
import { ChipBar, EmptyState } from './consoleUi';

/**
 * "Birleştirilen sorular": farklı kimliklerle iki kez girilmiş aynı çıkmış sorular (src/services/questionMerge.ts).
 * Sitede her gruptan yalnız asıl soru görünür; kopyalar gizlidir. Burada yönetici grubu yan yana görür, asıl soruyu
 * değiştirir, birleştirmeyi onaylar ya da ayırır (ayrılan grubun tüm soruları yeniden görünür).
 * Birebir aynı olmayan gruplar önce listelenir: farklı olan metinlerden doğru olanı seçmek gerekir.
 */
type Soru = { id: string; stem: string; options: string[]; correctAnswer: string; committeeId: string; discipline: string; year: string; source: string };
type Grup = {
  id: string;
  asil: string;
  uyeler: string[];
  birebir_ayni: boolean;
  benzerlik: number;
  durum: 'otomatik' | 'onayli' | 'ayrildi';
  sorular: Soru[];
};
type Filtre = 'incele' | 'ayni' | 'onayli' | 'ayrildi' | 'hepsi';

const LETTERS = ['A', 'B', 'C', 'D', 'E'];
const PAGE = 20;

export const ManageMergesSection: React.FC<{ adminEmail: string }> = ({ adminEmail }) => {
  const headers = { 'Content-Type': 'application/json', 'x-admin-email': adminEmail || '' };
  const [gruplar, setGruplar] = useState<Grup[] | null>(null);
  const [filtre, setFiltre] = useState<Filtre>('incele');
  const [sayfa, setSayfa] = useState(1);
  const [busy, setBusy] = useState<string | null>(null);

  const yukle = () =>
    safeJsonFetch<{ gruplar: Grup[] }>('/api/admin/question-merges', { headers }).then((r) => {
      if (r.ok && r.data) setGruplar(r.data.gruplar);
      else toast.error('Birleştirmeler alınamadı.');
    });
  useEffect(() => {
    yukle();
  }, []);

  const say = useMemo(() => {
    const g = gruplar || [];
    return {
      incele: g.filter((x) => x.durum === 'otomatik' && !x.birebir_ayni).length,
      ayni: g.filter((x) => x.durum === 'otomatik' && x.birebir_ayni).length,
      onayli: g.filter((x) => x.durum === 'onayli').length,
      ayrildi: g.filter((x) => x.durum === 'ayrildi').length,
      hepsi: g.length,
    };
  }, [gruplar]);

  const liste = useMemo(() => {
    const g = gruplar || [];
    const f =
      filtre === 'incele' ? g.filter((x) => x.durum === 'otomatik' && !x.birebir_ayni)
      : filtre === 'ayni' ? g.filter((x) => x.durum === 'otomatik' && x.birebir_ayni)
      : filtre === 'onayli' ? g.filter((x) => x.durum === 'onayli')
      : filtre === 'ayrildi' ? g.filter((x) => x.durum === 'ayrildi')
      : g;
    return [...f].sort((a, b) => a.benzerlik - b.benzerlik);
  }, [gruplar, filtre]);

  const islem = async (g: Grup, body: Record<string, string>, mesaj: string) => {
    setBusy(g.id);
    const r = await safeJsonFetch<{ success: boolean; grup: Grup; error?: string }>(`/api/admin/question-merges/${encodeURIComponent(g.id)}`, {
      method: 'POST',
      headers,
      body: JSON.stringify(body),
    });
    setBusy(null);
    if (r.ok && r.data?.success) {
      setGruplar((prev) => (prev || []).map((x) => (x.id === g.id ? { ...x, ...r.data!.grup } : x)));
      toast.success(mesaj);
    } else toast.error(r.data?.error || r.error || 'İşlem yapılamadı.');
  };

  const durumTag = (g: Grup) =>
    g.durum === 'onayli' ? <span className="ms-tag is-ok"><Check /> Onaylandı</span>
    : g.durum === 'ayrildi' ? <span className="ms-tag">Ayrıldı · hepsi görünür</span>
    : <span className="ms-tag is-accent">Otomatik birleşti</span>;

  return (
    <div className="flex flex-col gap-3 min-w-0">
      <div className="ms-alert is-accent">
        <Info aria-hidden="true" />
        <span>
          Aynı soru farklı dökümlerden farklı kimliklerle birden çok kez girilmiş. Sitede her gruptan yalnız <b>asıl</b> soru görünür, kopyalar
          gizlenir (veri silinmez). Metinler farklıysa doğru olanı asıl yap; aslında farklı sorularsa grubu ayır.
        </span>
      </div>
      <ChipBar
        label="Grup durumu"
        value={filtre}
        onChange={(v) => {
          setFiltre(v);
          setSayfa(1);
        }}
        options={[
          { id: 'incele', label: 'İncelenmeli · metin farklı', n: say.incele },
          { id: 'ayni', label: 'Birebir aynı', n: say.ayni },
          { id: 'onayli', label: 'Onaylandı', n: say.onayli },
          { id: 'ayrildi', label: 'Ayrıldı', n: say.ayrildi },
          { id: 'hepsi', label: 'Hepsi', n: say.hepsi },
        ]}
      />

      {gruplar === null ? (
        <div className="flex flex-col gap-3" role="status" aria-label="Yükleniyor">
          {[0, 1].map((i) => <div key={i} className="h-48 rounded-2xl ms-shimmer" />)}
        </div>
      ) : liste.length === 0 ? (
        <section className="ms-panel">
          <EmptyState icon={CheckCircle2} title="Bu filtrede grup yok">{filtre === 'incele' ? 'İncelenmesi gereken birleştirme kalmadı.' : null}</EmptyState>
        </section>
      ) : (
        <>
          {liste.slice(0, sayfa * PAGE).map((g) => (
            <section key={g.id} className="ms-panel">
              <header className="ms-panel-head">
                <span className="flex flex-wrap items-center gap-1.5 min-w-0">
                  <span className={`ms-tag ${g.birebir_ayni ? 'is-ok' : 'is-warn'}`}>{g.birebir_ayni ? 'Birebir aynı' : 'Metin farklı'}</span>
                  {durumTag(g)}
                  <span className="text-[12.5px] text-ink-3 tabular-nums">{g.uyeler.length} soru · benzerlik %{(g.benzerlik * 100).toFixed(0)}</span>
                  <span className="font-mono text-[11.5px] text-ink-3 truncate max-w-[18ch]" title={g.id}>{g.id}</span>
                </span>
                <span className="ms-panel-tools">
                  {g.durum !== 'ayrildi' ? (
                    <>
                      {g.durum !== 'onayli' && (
                        <button type="button" disabled={busy === g.id} onClick={() => islem(g, { action: 'confirm' }, 'Birleştirme onaylandı.')} className="ms-btn is-sm is-ok">
                          <Check /> Onayla
                        </button>
                      )}
                      <button type="button" disabled={busy === g.id} onClick={() => islem(g, { action: 'split' }, 'Grup ayrıldı; tüm sorular sitede görünür.')} className="ms-btn is-sm">
                        <Split /> Farklı sorular, ayır
                      </button>
                    </>
                  ) : (
                    <button type="button" disabled={busy === g.id} onClick={() => islem(g, { action: 'restore' }, 'Grup yeniden birleştirildi.')} className="ms-btn is-sm">
                      <Undo2 /> Yeniden birleştir
                    </button>
                  )}
                </span>
              </header>
              <div className="p-3 grid gap-2" style={{ gridTemplateColumns: `repeat(auto-fit, minmax(min(100%, 280px), 1fr))` }}>
                {g.sorular.map((q) => {
                  const asil = q.id === g.asil && g.durum !== 'ayrildi';
                  return (
                    <article key={q.id} className={`rounded-xl p-3 flex flex-col gap-2 min-w-0 ${asil ? 'bg-ok-tint ring-1 ring-ok/35' : 'bg-canvas'}`}>
                      <div className="flex items-center gap-1.5 text-[12px] text-ink-3 min-w-0">
                        {asil ? <span className="ms-tag is-ok"><Crown /> Asıl</span> : <span className="ms-tag"><Copy /> Kopya</span>}
                        <span className="truncate">{[q.committeeId, q.discipline, q.year].filter(Boolean).join(' · ')}</span>
                      </div>
                      <p className="m-0 text-[14px] text-ink leading-relaxed break-words whitespace-pre-wrap">{q.stem || <i className="text-ink-3">Kök yok</i>}</p>
                      <ol className="m-0 p-0 list-none flex flex-col gap-1">
                        {q.options.map((o, i) => {
                          const ok = LETTERS[i] === q.correctAnswer;
                          return (
                            <li key={i} className={`flex items-start gap-2 text-[13px] leading-snug ${ok ? 'text-ok font-semibold' : 'text-ink-2'}`}>
                              <span className={`shrink-0 w-5 h-5 rounded-md inline-flex items-center justify-center font-mono text-[11.5px] ${ok ? 'bg-ok text-white' : 'bg-white text-ink-3'}`}>{LETTERS[i]}</span>
                              <span className="min-w-0">{o}</span>
                            </li>
                          );
                        })}
                      </ol>
                      <div className="flex items-center justify-between gap-2 mt-auto pt-1">
                        <span className="font-mono text-[11.5px] text-ink-3 truncate" title={q.id}>{q.id}</span>
                        {!asil && g.durum !== 'ayrildi' && (
                          <button type="button" disabled={busy === g.id} onClick={() => islem(g, { action: 'primary', asil: q.id }, 'Asıl soru değiştirildi.')} className="ms-btn is-sm is-tonal">
                            <Crown /> Bunu asıl yap
                          </button>
                        )}
                        {asil && <span className="text-[12px] font-semibold text-ok">Sitede görünen</span>}
                      </div>
                    </article>
                  );
                })}
              </div>
            </section>
          ))}
          {liste.length > sayfa * PAGE && (
            <button type="button" onClick={() => setSayfa((n) => n + 1)} className="ms-btn self-center">
              <ChevronDown /> {liste.length - sayfa * PAGE} grup daha
            </button>
          )}
        </>
      )}
    </div>
  );
};

export default ManageMergesSection;
