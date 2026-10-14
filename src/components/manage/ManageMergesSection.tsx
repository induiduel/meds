import React, { useEffect, useMemo, useState } from 'react';
import { Check, Crown, Split, Undo2, Copy, Info, CheckCircle2, ChevronDown, CopyCheck, TriangleAlert } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { toast } from '../ui/Toast';
import { ChipBar, EmptyState } from './consoleUi';
import { confirmDialog } from '../ui/ConfirmDialog';

/**
 * "Birleştirilen sorular": farklı kimliklerle iki kez girilmiş aynı çıkmış sorular (src/services/questionMerge.ts).
 * Sitede her gruptan yalnız asıl soru görünür; kopyalar gizlidir. Burada yönetici grubu yan yana görür, asıl soruyu
 * değiştirir, birleştirmeyi onaylar ya da ayırır (ayrılan grubun tüm soruları yeniden görünür).
 * Birebir aynı olmayan gruplar önce listelenir: farklı olan metinlerden doğru olanı seçmek gerekir.
 * "Düzeltme kopyada kaldı": gizli bir kopya grup oluştuktan sonra düzeltilmiş ama sitede görünen kopya farklı —
 * düzeltme sitede görünmüyor. "Bu sürümü tüm kopyalara yaz" seçilen kopyanın içeriğini gruptaki hepsine yazar.
 */
type Soru = { id: string; stem: string; options: string[]; correctAnswer: string; committeeId: string; discipline: string; year: string; source: string; duzenleme?: { at: string; kind: string } | null; ayrisik?: boolean };
type Grup = {
  id: string;
  asil: string;
  uyeler: string[];
  birebir_ayni: boolean;
  benzerlik: number;
  durum: 'otomatik' | 'onayli' | 'ayrildi';
  gorunen?: string | null;
  ayrisik?: boolean;
  /** Sonradan eklenen üyelerin asılla metin benzerliği (0–1); %99 altı "olası aynı soru" demektir. */
  olasilik?: Record<string, number>;
  sorular: Soru[];
};
type Filtre = 'ayrisik' | 'incele' | 'ayni' | 'onayli' | 'ayrildi' | 'hepsi';

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
      if (r.ok && r.data) {
        setGruplar(r.data.gruplar);
        // Düzeltmesi gizli kopyada kalmış grup varsa önce onlar gösterilir
        if (gruplar === null && r.data.gruplar.some((g) => g.ayrisik && g.durum !== 'ayrildi')) setFiltre('ayrisik');
      } else toast.error('Birleştirmeler alınamadı.');
    });
  useEffect(() => {
    yukle();
  }, []);

  const say = useMemo(() => {
    const g = gruplar || [];
    return {
      ayrisik: g.filter((x) => x.ayrisik && x.durum !== 'ayrildi').length,
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
      filtre === 'ayrisik' ? g.filter((x) => x.ayrisik && x.durum !== 'ayrildi')
      : filtre === 'incele' ? g.filter((x) => x.durum === 'otomatik' && !x.birebir_ayni)
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
      if (body.action === 'sync') yukle();
      else setGruplar((prev) => (prev || []).map((x) => (x.id === g.id ? { ...x, ...r.data!.grup } : x)));
      toast.success(mesaj);
    } else toast.error(r.data?.error || r.error || 'İşlem yapılamadı.');
  };

  const esitle = async (g: Grup, q: Soru) => {
    const ok = await confirmDialog({
      title: 'Bu sürüm tüm kopyalara yazılsın mı?',
      message: `#${q.id} kopyasının kökü, şıkları, cevabı ve açıklaması gruptaki diğer ${g.uyeler.length - 1} kopyaya yazılır; sitede bu sürüm görünür. Kopyaların önceki hâli revizyon olarak saklanır. Sınav yılı, oylar ve yorumlar değişmez.`,
      confirmLabel: 'Tüm kopyalara yaz',
    });
    if (ok) islem(g, { action: 'sync', kaynak: q.id }, 'Tüm kopyalar bu sürüme eşitlendi.');
  };
  const tarih = (iso: string) => new Date(iso).toLocaleString('tr-TR', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' });

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
          ...(say.ayrisik ? [{ id: 'ayrisik' as const, label: 'Düzeltme kopyada kaldı', n: say.ayrisik }] : []),
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
                  {g.ayrisik && g.durum !== 'ayrildi' && <span className="ms-tag is-bad"><TriangleAlert /> Düzeltme kopyada kaldı</span>}
                  <span className={`ms-tag ${g.birebir_ayni ? 'is-ok' : 'is-warn'}`}>{g.birebir_ayni ? 'Birebir aynı' : 'Metin farklı'}</span>
                  {durumTag(g)}
                  <span className="text-sm text-ink-3 tabular-nums">{g.uyeler.length} soru · benzerlik %{(g.benzerlik * 100).toFixed(0)}</span>
                  <span className="font-mono text-xs text-ink-3 truncate max-w-[18ch]" title={g.id}>{g.id}</span>
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
                  const sitede = g.durum !== 'ayrildi' && q.id === (g.gorunen || g.asil);
                  return (
                    <article key={q.id} className={`rounded-xl p-3 flex flex-col gap-2 min-w-0 ${sitede ? 'bg-ok-tint ring-1 ring-ok/35' : q.ayrisik ? 'bg-canvas ring-1 ring-bad/40' : 'bg-canvas'}`}>
                      <div className="flex items-center gap-1.5 text-xs text-ink-3 min-w-0">
                        {asil ? <span className="ms-tag is-ok"><Crown /> Asıl</span> : <span className="ms-tag"><Copy /> Kopya</span>}
                        {!asil && g.olasilik?.[q.id] !== undefined && g.olasilik[q.id] < 0.99 && (
                          <span className="ms-tag is-warn tabular-nums" title="Metin benzerliği; aynı soru olduğu kesin değil">Olası %{Math.round(g.olasilik[q.id] * 100)}</span>
                        )}
                        <span className="truncate">{[q.committeeId, q.discipline, q.year].filter(Boolean).join(' · ')}</span>
                      </div>
                      {(q.duzenleme || q.ayrisik) && (
                        <p className={`m-0 text-xs ${q.ayrisik ? 'text-bad font-semibold' : 'text-ink-3'}`}>
                          {q.ayrisik ? 'Bu kopyadaki düzeltme sitede görünmüyor · ' : 'Son düzeltme: '}
                          {q.duzenleme ? `${q.duzenleme.kind} · ${tarih(q.duzenleme.at)}` : ''}
                        </p>
                      )}
                      <p className="m-0 text-base text-ink leading-relaxed break-words whitespace-pre-wrap">{q.stem || <i className="text-ink-3">Kök yok</i>}</p>
                      <ol className="m-0 p-0 list-none flex flex-col gap-1">
                        {q.options.map((o, i) => {
                          const ok = LETTERS[i] === q.correctAnswer;
                          return (
                            <li key={i} className={`flex items-start gap-2 text-sm leading-snug ${ok ? 'text-ok font-semibold' : 'text-ink-2'}`}>
                              <span className={`shrink-0 w-5 h-5 rounded-md inline-flex items-center justify-center font-mono text-xs ${ok ? 'bg-ok text-white' : 'bg-white text-ink-3'}`}>{LETTERS[i]}</span>
                              <span className="min-w-0">{o}</span>
                            </li>
                          );
                        })}
                      </ol>
                      <div className="flex items-center justify-between gap-2 mt-auto pt-1">
                        <span className="font-mono text-xs text-ink-3 truncate" title={q.id}>{q.id}</span>
                        {!asil && g.durum !== 'ayrildi' && (
                          <button type="button" disabled={busy === g.id} onClick={() => islem(g, { action: 'primary', asil: q.id }, 'Asıl soru değiştirildi.')} className="ms-btn is-sm is-tonal">
                            <Crown /> Bunu asıl yap
                          </button>
                        )}
                        {sitede && <span className="text-xs font-semibold text-ok">Sitede görünen</span>}
                      </div>
                      {g.durum !== 'ayrildi' && (!g.birebir_ayni || g.ayrisik) && (
                        <button type="button" disabled={busy === g.id} onClick={() => esitle(g, q)} className={`ms-btn is-sm ${q.ayrisik ? 'is-ok' : ''} self-start`}>
                          <CopyCheck /> Bu sürümü tüm kopyalara yaz
                        </button>
                      )}
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
