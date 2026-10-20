import React, { useEffect, useMemo, useState } from 'react';
import { Check, Crown, Split, Undo2, Copy, CheckCircle2, ChevronDown, CopyCheck, TriangleAlert, RefreshCw } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { toast } from '../ui/Toast';
import { Drawer, EmptyState } from './consoleUi';
import { DataTable, DetailNav, PageActions, Pill, SearchField, StatRow, Tabs14, Toolbar, type Col } from '../v14/pageKit';
import { BulkBar, useSelection } from '../v14/manageKit';
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
  const [q, setQ] = useState('');
  const [acikId, setAcikId] = useState<string | null>(null);
  const [topluBusy, setTopluBusy] = useState(false);
  const secim = useSelection<string>();

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
    const t = q.trim().toLocaleLowerCase('tr');
    const f2 = t ? f.filter((x) => `${x.id} ${x.sorular.map((s) => `${s.id} ${s.stem}`).join(' ')}`.toLocaleLowerCase('tr').includes(t)) : f;
    return [...f2].sort((a, b) => a.benzerlik - b.benzerlik);
  }, [gruplar, filtre, q]);
  const acik = acikId ? (gruplar || []).find((g) => g.id === acikId) || null : null;
  const asilSoru = (g: Grup) => g.sorular.find((s) => s.id === (g.gorunen || g.asil)) || g.sorular[0];

  const istek = (g: Grup, body: Record<string, string>) =>
    safeJsonFetch<{ success: boolean; grup: Grup; error?: string }>(`/api/admin/question-merges/${encodeURIComponent(g.id)}`, {
      method: 'POST',
      headers,
      body: JSON.stringify(body),
    });
  const islem = async (g: Grup, body: Record<string, string>, mesaj: string) => {
    setBusy(g.id);
    const r = await istek(g, body);
    setBusy(null);
    if (r.ok && r.data?.success) {
      if (body.action === 'sync') yukle();
      else setGruplar((prev) => (prev || []).map((x) => (x.id === g.id ? { ...x, ...r.data!.grup } : x)));
      toast.success(mesaj);
      return true;
    }
    toast.error(r.data?.error || r.error || 'İşlem yapılamadı.');
    return false;
  };
  // Toplu işlem: tek grup ucunu sırayla çağırır
  const toplu = async (action: 'confirm' | 'split' | 'restore', uygun: (g: Grup) => boolean, ad: string) => {
    const hedef = (gruplar || []).filter((g) => secim.has(g.id) && uygun(g));
    if (!hedef.length) { toast.error('Seçilenlerde bu işleme uygun grup yok.'); return; }
    setTopluBusy(true);
    let ok = 0, err = 0;
    const yeni: Record<string, Grup> = {};
    for (const g of hedef) {
      const r = await istek(g, { action });
      if (r.ok && r.data?.success) { ok++; yeni[g.id] = r.data.grup; } else err++;
    }
    setTopluBusy(false);
    setGruplar((prev) => (prev || []).map((x) => (yeni[x.id] ? { ...x, ...yeni[x.id] } : x)));
    (err ? toast.error : toast.success)(`${ad}: ${ok} başarılı, ${err} hata.`);
    if (!err) secim.clear();
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

  const karsilastir = (g: Grup) => (
    <div className="grid gap-2" style={{ gridTemplateColumns: `repeat(auto-fit, minmax(min(100%, 280px), 1fr))` }}>
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
                    <span className={`shrink-0 w-5 h-5 rounded-md inline-flex items-center justify-center font-mono text-xs ${ok ? 'bg-ok text-white' : 'bg-field text-ink-3'}`}>{LETTERS[i]}</span>
                    <span className="min-w-0">{o}</span>
                  </li>
                );
              })}
            </ol>
            <div className="flex items-center justify-between gap-2 mt-auto pt-1">
              <span className="font-mono text-xs text-ink-3 truncate" title={q.id}>{q.id}</span>
              {!asil && g.durum !== 'ayrildi' && (
                <button type="button" disabled={busy === g.id} onClick={() => islem(g, { action: 'primary', asil: q.id }, 'Asıl soru değiştirildi.')} className="m14-btn">
                  <Crown /> Bunu asıl yap
                </button>
              )}
              {sitede && <span className="text-xs font-semibold text-ok">Sitede görünen</span>}
            </div>
            {g.durum !== 'ayrildi' && (!g.birebir_ayni || g.ayrisik) && (
              <button type="button" disabled={busy === g.id} onClick={() => esitle(g, q)} className={`m14-btn ${q.ayrisik ? "primary" : ""} self-start`}>
                <CopyCheck /> Bu sürümü tüm kopyalara yaz
              </button>
            )}
          </article>
        );
      })}
    </div>
  );

  const cols: Col<Grup>[] = [
    { key: 'k', label: 'Ana soru', main: true, render: (g) => asilSoru(g)?.stem || g.id },
    { key: 'd', label: 'Durum', render: (g) => (
      <span className="inline-flex gap-1">
        {g.ayrisik && g.durum !== 'ayrildi' && <Pill tone="bad">Düzeltme kopyada</Pill>}
        <Pill tone={g.durum === 'onayli' ? 'ok' : g.durum === 'ayrildi' ? '' : 'acc'}>{g.durum === 'onayli' ? 'Onaylandı' : g.durum === 'ayrildi' ? 'Ayrıldı' : 'Otomatik'}</Pill>
        <Pill tone={g.birebir_ayni ? 'ok' : 'warn'}>{g.birebir_ayni ? 'Birebir aynı' : 'Metin farklı'}</Pill>
      </span>
    ) },
    { key: 'n', label: 'Soru', right: true, render: (g) => g.uyeler.length },
    { key: 'b', label: 'Benzerlik', right: true, render: (g) => `%${(g.benzerlik * 100).toFixed(0)}` },
    { key: 'y', label: 'Yıl / kurul', muted: true, render: (g) => { const a = asilSoru(g); return [a?.year, a?.committeeId].filter(Boolean).join(' · ') || '—'; } },
    { key: 'g', label: 'Grup', mono: true, render: (g) => g.id },
  ];

  const sonrakiAc = (g: Grup) => {
    const i = liste.findIndex((x) => x.id === g.id);
    const n = liste[i + 1];
    setAcikId(n && n.id !== g.id ? n.id : null);
  };

  return (
    <div className="flex flex-col gap-4 min-w-0">
      <PageActions
        note={<>Aynı soru farklı dökümlerden farklı kimliklerle birden çok kez girilmiş. Sitede her gruptan yalnız <b>asıl</b> soru görünür, kopyalar gizlenir (veri silinmez). Metinler farklıysa doğru olanı asıl yap; aslında farklı sorularsa grubu ayır.</>}
      >
        <button type="button" className="m14-btn" onClick={() => yukle()}><RefreshCw aria-hidden="true" /> Yenile</button>
      </PageActions>

      <StatRow
        stats={[
          { label: 'Birleşme grubu', value: gruplar ? say.hepsi.toLocaleString('tr-TR') : '…', onClick: () => { setFiltre('hepsi'); setSayfa(1); } },
          { label: 'Düzeltme kopyada kaldı', value: gruplar ? say.ayrisik.toLocaleString('tr-TR') : '…', tone: say.ayrisik ? 'bad' : 'ok', onClick: say.ayrisik ? () => { setFiltre('ayrisik'); setSayfa(1); } : undefined },
          { label: 'İnceleme bekleyen', value: gruplar ? say.incele.toLocaleString('tr-TR') : '…', tone: say.incele ? 'warn' : 'ok', onClick: () => { setFiltre('incele'); setSayfa(1); } },
          { label: 'Onaylı', value: gruplar ? say.onayli.toLocaleString('tr-TR') : '…', onClick: () => { setFiltre('onayli'); setSayfa(1); } },
        ]}
      />

      <Toolbar>
        <Tabs14<Filtre>
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
        <SearchField value={q} onChange={(v) => { setQ(v); setSayfa(1); }} placeholder="Soru kökü ya da grup kimliği" />
      </Toolbar>

      <BulkBar
        count={secim.count}
        noun="grup"
        busy={topluBusy}
        onClear={secim.clear}
        actions={[
          { label: 'Onayla', kind: 'main', run: () => toplu('confirm', (g) => g.durum === 'otomatik', 'Onay') },
          { label: 'Yeniden birleştir', run: () => toplu('restore', (g) => g.durum === 'ayrildi', 'Yeniden birleştirme') },
          { label: 'Grupları ayır', kind: 'danger', confirm: `${secim.count} grubu ayırmayı onayla`, run: () => toplu('split', (g) => g.durum !== 'ayrildi', 'Ayırma') },
        ]}
      />

      {gruplar === null ? (
        <div className="h-48 rounded-2xl ms-shimmer" role="status" aria-label="Yükleniyor" />
      ) : (
        <>
          <DataTable
            rows={liste.slice(0, sayfa * PAGE)}
            cols={cols}
            rowKey={(g) => g.id}
            onOpen={(g) => setAcikId(g.id)}
            activeKey={acikId}
            selection={secim}
            minWidth={900}
            empty={<EmptyState icon={CheckCircle2} title="Bu filtrede grup yok">{filtre === 'incele' ? 'İncelenmesi gereken birleştirme kalmadı.' : null}</EmptyState>}
          />
          {liste.length > sayfa * PAGE && (
            <button type="button" onClick={() => setSayfa((n) => n + 1)} className="m14-btn self-center">
              <ChevronDown aria-hidden="true" /> {liste.length - sayfa * PAGE} grup daha
            </button>
          )}
        </>
      )}

      <Drawer
        open={!!acik}
        onClose={() => setAcikId(null)}
        wide
        title={acik ? `Yan yana karşılaştırma · ${acik.uyeler.length} soru` : ''}
        head={acik && <DetailNav list={liste} current={acik} same={(a, b) => a.id === b.id} onGo={(g) => setAcikId(g.id)} />}
        foot={acik && (
          <div className="flex flex-wrap gap-2">
            {acik.durum !== 'ayrildi' ? (
              <>
                <button type="button" disabled={busy === acik.id} onClick={() => islem(acik, { action: 'split' }, 'Grup ayrıldı; tüm sorular sitede görünür.')} className="m14-btn danger">
                  <Split aria-hidden="true" /> Farklı sorular, ayır
                </button>
                {acik.durum !== 'onayli' && (
                  <>
                    <button type="button" disabled={busy === acik.id} onClick={() => islem(acik, { action: 'confirm' }, 'Birleştirme onaylandı.')} className="m14-btn">
                      <Check aria-hidden="true" /> Onayla
                    </button>
                    <button type="button" disabled={busy === acik.id} onClick={async () => { if (await islem(acik, { action: 'confirm' }, 'Birleştirme onaylandı.')) sonrakiAc(acik); }} className="m14-btn primary">
                      <Check aria-hidden="true" /> Onayla ve sonraki
                    </button>
                  </>
                )}
              </>
            ) : (
              <button type="button" disabled={busy === acik.id} onClick={() => islem(acik, { action: 'restore' }, 'Grup yeniden birleştirildi.')} className="m14-btn primary">
                <Undo2 aria-hidden="true" /> Yeniden birleştir
              </button>
            )}
          </div>
        )}
      >
        {acik && (
          <div className="flex flex-col gap-3">
            <div className="flex flex-wrap items-center gap-1.5 min-w-0">
              {acik.ayrisik && acik.durum !== 'ayrildi' && <Pill tone="bad"><TriangleAlert className="w-3.5 h-3.5" aria-hidden="true" /> Düzeltme kopyada kaldı</Pill>}
              <Pill tone={acik.birebir_ayni ? 'ok' : 'warn'}>{acik.birebir_ayni ? 'Birebir aynı' : 'Metin farklı'}</Pill>
              {durumTag(acik)}
              <span className="text-sm text-ink-3 tabular-nums">benzerlik %{(acik.benzerlik * 100).toFixed(0)}</span>
              <span className="font-mono text-xs text-ink-3 break-all">{acik.id}</span>
            </div>
            <p className="text-sm text-ink-3 m-0">Yalnız aynı yıl ve kurul birleşir. Anlamı farklı olan kopya ayrı soru olarak ayrılır. “Bu sürümü tüm kopyalara yaz” seçilen kopyanın içeriğini gruptaki hepsine uygular.</p>
            {karsilastir(acik)}
          </div>
        )}
      </Drawer>
    </div>
  );
};

export default ManageMergesSection;
