import React, { useEffect, useMemo, useState } from 'react';
import { Check, Crown, Split, Undo2, Copy } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { toast } from '../ui/Toast';

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

  const tab = (id: Filtre, label: string) => (
    <button
      key={id}
      type="button"
      onClick={() => {
        setFiltre(id);
        setSayfa(1);
      }}
      className={`h-9 px-3 rounded-lg text-[13px] font-medium cursor-pointer border ${filtre === id ? 'bg-ink text-white border-ink' : 'bg-white text-ink-2 border-line hover:bg-canvas'}`}
      aria-pressed={filtre === id}
    >
      {label} <span className="opacity-70">{say[id]}</span>
    </button>
  );

  return (
    <div className="flex flex-col gap-3 min-w-0">
      <div className="flex flex-col gap-1">
        <h2 className="m-0 text-[16px] font-bold text-ink">Birleştirilen sorular</h2>
        <p className="m-0 text-[13px] text-ink-3 max-w-3xl">
          Aynı soru farklı sınav dökümlerinden farklı kimliklerle birden çok kez girilmiş. Sitede her gruptan yalnız{' '}
          <b>asıl</b> soru gösterilir, kopyalar gizlenir (veri silinmez). Metinler farklıysa doğru olanı asıl yapın; aslında farklı
          sorularsa grubu ayırın.
        </p>
      </div>
      <div className="flex flex-wrap gap-1.5" role="group" aria-label="Filtre">
        {tab('incele', 'İncelenmeli (metin farklı)')}
        {tab('ayni', 'Birebir aynı')}
        {tab('onayli', 'Onaylandı')}
        {tab('ayrildi', 'Ayrıldı')}
        {tab('hepsi', 'Hepsi')}
      </div>

      {gruplar === null ? (
        <p className="m-0 text-[13px] text-ink-3">Yükleniyor…</p>
      ) : liste.length === 0 ? (
        <p className="m-0 text-[13px] text-ink-3">Bu filtrede grup yok.</p>
      ) : (
        <>
          {liste.slice(0, sayfa * PAGE).map((g) => (
            <section key={g.id} className="rounded-xl border border-line bg-white p-3 flex flex-col gap-2.5">
              <header className="flex flex-wrap items-center gap-2 text-[12.5px] text-ink-3">
                <span className="font-mono text-ink-2">{g.id}</span>
                <span>· {g.uyeler.length} soru</span>
                <span>· benzerlik {(g.benzerlik * 100).toFixed(0)}%</span>
                <span className={`px-1.5 rounded ${g.birebir_ayni ? 'bg-emerald-50 text-emerald-700' : 'bg-amber-50 text-amber-800'}`}>
                  {g.birebir_ayni ? 'birebir aynı' : 'metin farklı'}
                </span>
                <span className="px-1.5 rounded bg-canvas text-ink-2">
                  {g.durum === 'otomatik' ? 'otomatik birleşti' : g.durum === 'onayli' ? 'onaylandı' : 'ayrıldı (hepsi görünür)'}
                </span>
                <span className="ml-auto flex gap-1.5">
                  {g.durum !== 'ayrildi' ? (
                    <>
                      {g.durum !== 'onayli' && (
                        <button type="button" disabled={busy === g.id} onClick={() => islem(g, { action: 'confirm' }, 'Birleştirme onaylandı.')} className="h-8 px-2.5 rounded-lg border border-line text-[12.5px] font-semibold text-ink-2 hover:bg-emerald-50 hover:text-emerald-800 inline-flex items-center gap-1 cursor-pointer disabled:opacity-50">
                          <Check className="w-3.5 h-3.5" /> Onayla
                        </button>
                      )}
                      <button type="button" disabled={busy === g.id} onClick={() => islem(g, { action: 'split' }, 'Grup ayrıldı; tüm sorular sitede görünür.')} className="h-8 px-2.5 rounded-lg border border-line text-[12.5px] font-semibold text-ink-2 hover:bg-rose-50 hover:text-rose-800 inline-flex items-center gap-1 cursor-pointer disabled:opacity-50">
                        <Split className="w-3.5 h-3.5" /> Farklı sorular, ayır
                      </button>
                    </>
                  ) : (
                    <button type="button" disabled={busy === g.id} onClick={() => islem(g, { action: 'restore' }, 'Grup yeniden birleştirildi.')} className="h-8 px-2.5 rounded-lg border border-line text-[12.5px] font-semibold text-ink-2 hover:bg-canvas inline-flex items-center gap-1 cursor-pointer disabled:opacity-50">
                      <Undo2 className="w-3.5 h-3.5" /> Yeniden birleştir
                    </button>
                  )}
                </span>
              </header>
              <div className="grid gap-2" style={{ gridTemplateColumns: `repeat(auto-fit, minmax(min(100%, 260px), 1fr))` }}>
                {g.sorular.map((q) => {
                  const asil = q.id === g.asil && g.durum !== 'ayrildi';
                  return (
                    <article key={q.id} className={`rounded-lg p-2.5 flex flex-col gap-1.5 min-w-0 border ${asil ? 'border-emerald-300 bg-emerald-50/40' : 'border-line-soft bg-canvas/40'}`}>
                      <div className="flex items-center gap-1.5 text-[11.5px] text-ink-3 min-w-0">
                        {asil ? <Crown className="w-3.5 h-3.5 text-emerald-700 shrink-0" /> : <Copy className="w-3.5 h-3.5 shrink-0" />}
                        <span className="font-mono truncate">{q.id}</span>
                        <span className="truncate">· {[q.committeeId, q.discipline, q.year].filter(Boolean).join(' · ')}</span>
                      </div>
                      <p className="m-0 text-[13.5px] text-ink leading-snug break-words whitespace-pre-wrap">{q.stem || <i className="text-ink-3">kök yok</i>}</p>
                      <ol className="m-0 p-0 list-none flex flex-col gap-0.5 text-[12.5px] text-ink-2">
                        {q.options.map((o, i) => (
                          <li key={i} className={LETTERS[i] === q.correctAnswer ? 'font-semibold text-emerald-800' : ''}>
                            {LETTERS[i]}) {o}
                          </li>
                        ))}
                      </ol>
                      <div className="flex items-center justify-between gap-2 mt-auto pt-1">
                        <span className="text-[11.5px] text-ink-3">Cevap: {q.correctAnswer || '–'}</span>
                        {!asil && g.durum !== 'ayrildi' && (
                          <button type="button" disabled={busy === g.id} onClick={() => islem(g, { action: 'primary', asil: q.id }, 'Asıl soru değiştirildi.')} className="h-8 px-2.5 rounded-lg border border-line text-[12.5px] font-semibold text-ink-2 hover:bg-emerald-50 hover:text-emerald-800 inline-flex items-center gap-1 cursor-pointer disabled:opacity-50">
                            <Crown className="w-3.5 h-3.5" /> Bunu asıl yap
                          </button>
                        )}
                        {asil && <span className="text-[11.5px] font-semibold text-emerald-800">Sitede görünen</span>}
                      </div>
                    </article>
                  );
                })}
              </div>
            </section>
          ))}
          {liste.length > sayfa * PAGE && (
            <button type="button" onClick={() => setSayfa((n) => n + 1)} className="self-center h-9 px-4 rounded-lg border border-line text-[13px] text-ink-2 hover:bg-canvas cursor-pointer">
              Daha fazla göster ({liste.length - sayfa * PAGE} grup daha)
            </button>
          )}
        </>
      )}
    </div>
  );
};

export default ManageMergesSection;
