import React, { useEffect, useMemo, useState } from 'react';
import { Archive, Download, ShieldCheck, ShieldAlert, Tags, PencilLine, StickyNote, FileJson } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { toast } from '../ui/Toast';
import { Drawer, EmptyState, Field, Seg } from './consoleUi';
import { Card14, DataTable, DetailLayout, DetailNav, FactList, PageActions, Pill, SearchField, StatRow, Tabs14, Toolbar, type Col } from '../v14/pageKit';
import { BulkBar, useSelection } from '../v14/manageKit';

/**
 * Ham soru havuzu: kullanıcıların eklediği her soru ve o soruya gelen her katkı (parça/ipucu, şık, "şık yoktu"
 * itirazı, yorum, bildirim, oy) soru başına tek kümede, append-only defterde (data/question_ledger, pg
 * question_raw_events). Bu ekran yalnız OKUR ve YENİ OLAY EKLER: sınıflandırma, düzenleme ve not ayrı olay
 * olarak yazılır; ham olaylar hiçbir yoldan silinmez ya da değiştirilmez. YZ önerileri ayrı katmanda görünür.
 */
type Summary = {
  qid: string;
  title: string;
  committeeId?: string;
  questionNumber?: number | string;
  discipline?: string;
  deleted: boolean;
  eventCount: number;
  firstSeen?: string;
  lastEvent?: string;
  chain: { ok: boolean; brokenAt?: number };
  classification: Record<string, any>;
  counts: Record<string, number>;
  aiCount: number;
};
type Ev = { eventId: string; seq: number; ts: string; type: string; actor: { kind: string; name?: string; uid?: string; email?: string }; payload: any };
type Cluster = Summary & { events: Ev[]; current: any; original: any; contributions: Record<string, any[]>; ai: any[]; admin: any[]; guard: any[] };
type Filtre = 'hepsi' | 'katki' | 'siniflanmamis' | 'yz' | 'silinmis' | 'bozuk';

const TYPE_LABEL: Record<string, string> = {
  baseline: 'Defter öncesi hal',
  question_created: 'Soru eklendi',
  fragment_added: 'Parça / ipucu',
  option_added: 'Şık eklendi',
  alternativeOption_added: 'Alternatif şık / "yoktu" itirazı',
  comment_added: 'Yorum',
  report_added: 'Bildirim',
  mergedSatellite_added: 'Birleşen taslak',
  vote_added: 'Oy',
  vote_removed: 'Oy geri alındı',
  field_changed: 'Alan değişti',
  guard_restored: 'Koruma: kayıp geri kondu',
  ai_suggestion: 'YZ önerisi (ayrı katman)',
  admin_classify: 'Sınıflandırma',
  admin_edit: 'Yönetici düzenlemesi',
  admin_note: 'Yönetici notu',
  admin_delete: 'Yönetici silmesi (anlık görüntü saklı)',
};
const fmt = (iso?: string) => (iso ? new Date(iso).toLocaleString('tr-TR', { day: 'numeric', month: 'short', year: '2-digit', hour: '2-digit', minute: '2-digit' }) : '—');
const who = (a: Ev['actor']) => (a?.kind === 'ai' ? `YZ · ${a.name || ''}` : a?.kind === 'admin' ? 'Yönetici' : a?.kind === 'system' ? 'Sistem' : a?.name || a?.uid || 'Kullanıcı');
const preview = (p: any) => {
  if (!p) return '';
  if (typeof p.text === 'string') return p.text;
  if (p.field) return `${p.field}: ${JSON.stringify(p.before ?? '')?.slice(0, 80)} → ${JSON.stringify(p.after ?? p.items ?? '')?.slice(0, 80)}`;
  return JSON.stringify(p).slice(0, 180);
};

export const ManageRawPoolSection: React.FC<{ adminEmail: string }> = ({ adminEmail }) => {
  const headers = useMemo(() => ({ 'Content-Type': 'application/json', 'x-admin-email': adminEmail || '' }), [adminEmail]);
  const [items, setItems] = useState<Summary[] | null>(null);
  const [q, setQ] = useState('');
  const [filtre, setFiltre] = useState<Filtre>('hepsi');
  const [open, setOpen] = useState<Cluster | null>(null);
  const [tab, setTab] = useState<'kume' | 'olaylar' | 'json'>('kume');
  const secim = useSelection<string>();
  const [topluBusy, setTopluBusy] = useState(false);
  const [topluSinif, setTopluSinif] = useState(false);

  const yukle = () =>
    safeJsonFetch<{ items: Summary[] }>('/api/admin/raw-pool', { headers }).then((r) => {
      if (r.ok && r.data) setItems(r.data.items);
      else toast.error('Ham havuz alınamadı.');
    });
  useEffect(() => {
    yukle();
  }, []);

  const ac = async (qid: string) => {
    const r = await safeJsonFetch<Cluster>(`/api/admin/raw-pool/${encodeURIComponent(qid)}`, { headers });
    if (r.ok && r.data) {
      setOpen(r.data);
      setTab('kume');
    } else toast.error('Küme açılamadı.');
  };

  const indir = async (format: 'json' | 'jsonl' | 'csv', ids?: string[]) => {
    const url = `/api/admin/raw-pool/export?format=${format}${ids ? `&ids=${encodeURIComponent(ids.join(','))}` : ''}`;
    const res = await fetch(url, { headers });
    if (!res.ok) return toast.error('Dışa aktarılamadı.');
    const blob = await res.blob();
    const name = /filename="([^"]+)"/.exec(res.headers.get('Content-Disposition') || '')?.[1] || `ham_havuz.${format}`;
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = name;
    a.click();
    URL.revokeObjectURL(a.href);
  };

  const say = useMemo(() => {
    const g = items || [];
    const katki = (x: Summary) => Object.values(x.counts || {}).reduce((a, b) => a + b, 0) > 0;
    return {
      hepsi: g.length,
      katki: g.filter(katki).length,
      siniflanmamis: g.filter((x) => !Object.keys(x.classification || {}).length).length,
      yz: g.filter((x) => x.aiCount > 0).length,
      silinmis: g.filter((x) => x.deleted).length,
      bozuk: g.filter((x) => !x.chain.ok).length,
      katkiFn: katki,
    };
  }, [items]);

  const liste = useMemo(() => {
    const t = q.trim().toLocaleLowerCase('tr');
    return (items || [])
      .filter((x) =>
        filtre === 'katki' ? say.katkiFn(x)
        : filtre === 'siniflanmamis' ? !Object.keys(x.classification || {}).length
        : filtre === 'yz' ? x.aiCount > 0
        : filtre === 'silinmis' ? x.deleted
        : filtre === 'bozuk' ? !x.chain.ok
        : true,
      )
      .filter((x) => !t || `${x.title} ${x.qid} ${x.discipline} ${x.committeeId} ${JSON.stringify(x.classification)}`.toLocaleLowerCase('tr').includes(t))
      .sort((a, b) => String(b.lastEvent).localeCompare(String(a.lastEvent)));
  }, [items, q, filtre, say]);
  const gorunen = liste.slice(0, 300);
  const secili = () => [...secim.sel];

  // Seçilenlere aynı sınıflandırmayı tek tek olay olarak yazar (ham kayıt değişmez)
  const topluSiniflandir = async (body: { category: string; quality: string; tags: string[] }) => {
    const ids = secili();
    setTopluBusy(true);
    let ok = 0, err = 0;
    for (const id of ids) {
      const r = await safeJsonFetch<any>(`/api/admin/raw-pool/${encodeURIComponent(id)}/classify`, { method: 'POST', headers, body: JSON.stringify(body) });
      if (r.ok && r.data?.success) ok++; else err++;
    }
    setTopluBusy(false);
    (err ? toast.error : toast.success)(`Sınıflandırma: ${ok} başarılı, ${err} hata.`);
    if (!err) { secim.clear(); setTopluSinif(false); }
    yukle();
  };

  const sinifMetni = (x: Summary) => [x.classification?.category, x.classification?.quality, ...(x.classification?.tags || [])].filter(Boolean).join(', ');
  const cols: Col<Summary>[] = [
    { key: 't', label: 'Soru', main: true, render: (x) => x.title || x.qid },
    { key: 's', label: 'Sınıf', render: (x) => (Object.keys(x.classification || {}).length ? <Pill tone="ok">{sinifMetni(x) || 'Sınıflandı'}</Pill> : <Pill tone="warn">Sınıflanmamış</Pill>) },
    { key: 'k', label: 'Kaynak', muted: true, render: (x) => [x.committeeId, x.questionNumber ? `S.${x.questionNumber}` : null, x.discipline].filter(Boolean).join(' · ') || '—' },
    { key: 'd', label: 'Durum', render: (x) => (
      <span className="inline-flex gap-1">
        {x.chain.ok ? <Pill tone="ok"><ShieldCheck className="w-3.5 h-3.5" aria-hidden="true" /> Zincir sağlam</Pill> : <Pill tone="bad"><ShieldAlert className="w-3.5 h-3.5" aria-hidden="true" /> Zincir bozuk</Pill>}
        {x.deleted && <Pill>Havuzdan kaldırıldı</Pill>}
        {x.aiCount > 0 && <Pill tone="acc">YZ {x.aiCount}</Pill>}
      </span>
    ) },
    { key: 'e', label: 'Olay', right: true, render: (x) => x.eventCount },
    { key: 'q', label: 'Kayıt no', mono: true, render: (x) => x.qid },
    { key: 'z', label: 'Son olay', muted: true, render: (x) => fmt(x.lastEvent) },
  ];

  const sonraki = () => {
    if (!open) return;
    const i = liste.findIndex((x) => x.qid === open.qid);
    const n = liste[i + 1];
    if (n) ac(n.qid); else setOpen(null);
  };

  return (
    <div className="flex flex-col gap-4 min-w-0">
      <PageActions
        note={<>Kullanıcıların eklediği sorular ve katkıları <b>ham veridir</b>: soru başına tek kümede, yalnız eklenen bir defterde tutulur. Hiçbir olay silinmez ya da değiştirilmez; sınıflandırma, düzenleme ve YZ önerileri ayrı olay olarak eklenir. Havuz soruları RAG'e alınmaz.</>}
      >
        <button type="button" className="m14-btn primary" onClick={() => indir('json')}><Download aria-hidden="true" /> JSON (kümeler)</button>
        <button type="button" className="m14-btn" onClick={() => indir('jsonl')}><FileJson aria-hidden="true" /> JSONL (olaylar)</button>
        <button type="button" className="m14-btn" onClick={() => indir('csv')}><Download aria-hidden="true" /> CSV</button>
      </PageActions>

      <StatRow
        stats={[
          { label: 'Defterdeki küme', value: items ? say.hepsi.toLocaleString('tr-TR') : '…', onClick: () => setFiltre('hepsi') },
          { label: 'Sınıflanmamış', value: items ? say.siniflanmamis.toLocaleString('tr-TR') : '…', tone: say.siniflanmamis ? 'warn' : 'ok', onClick: () => setFiltre('siniflanmamis') },
          { label: 'Katkı almış', value: items ? say.katki.toLocaleString('tr-TR') : '…', onClick: () => setFiltre('katki') },
          { label: 'Zincir bozuk', value: items ? say.bozuk.toLocaleString('tr-TR') : '…', tone: say.bozuk ? 'bad' : 'ok', onClick: say.bozuk ? () => setFiltre('bozuk') : undefined },
        ]}
      />

      <Toolbar>
        <Tabs14<Filtre>
          label="Süzgeç"
          value={filtre}
          onChange={setFiltre}
          options={[
            { id: 'hepsi', label: 'Hepsi', n: say.hepsi },
            { id: 'siniflanmamis', label: 'Sınıflanmamış', n: say.siniflanmamis },
            { id: 'katki', label: 'Katkı almış', n: say.katki },
            { id: 'yz', label: 'YZ önerisi var', n: say.yz },
            { id: 'silinmis', label: 'Havuzdan kaldırılmış', n: say.silinmis },
            ...(say.bozuk ? [{ id: 'bozuk' as const, label: 'Zincir bozuk', n: say.bozuk }] : []),
          ]}
        />
        <SearchField value={q} onChange={setQ} placeholder="Soru, ders, etiket ara" />
        <span className="text-sm text-ink-3 tabular-nums">{liste.length.toLocaleString('tr-TR')} küme{liste.length > 300 ? ' · ilk 300 gösteriliyor' : ''}</span>
      </Toolbar>

      <BulkBar
        count={secim.count}
        noun="küme"
        busy={topluBusy}
        onClear={secim.clear}
        actions={[
          { label: 'Sınıflandır', kind: 'main', run: () => setTopluSinif(true) },
          { label: 'JSON indir', run: () => { void indir('json', secili()); } },
          { label: 'JSONL indir', run: () => { void indir('jsonl', secili()); } },
          { label: 'CSV indir', run: () => { void indir('csv', secili()); } },
        ]}
      />

      {items === null ? (
        <div className="h-48 rounded-2xl ms-shimmer" role="status" aria-label="Yükleniyor" />
      ) : (
        <DataTable
          rows={gorunen}
          cols={cols}
          rowKey={(x) => x.qid}
          onOpen={(x) => ac(x.qid)}
          activeKey={open?.qid ?? null}
          selection={secim}
          minWidth={900}
          empty={<EmptyState icon={Archive} title="Bu süzgeçte küme yok" />}
        />
      )}

      <Drawer
        open={!!open}
        onClose={() => setOpen(null)}
        wide
        title={open?.title || ''}
        head={open && (
          <>
            <DetailNav list={liste} current={open as Summary} same={(a, b) => a.qid === b.qid} onGo={(x) => ac(x.qid)} />
            <Seg label="Görünüm" value={tab} onChange={setTab} options={[{ id: 'kume', label: 'Küme' }, { id: 'olaylar', label: 'Olaylar', n: open.events.length }, { id: 'json', label: 'JSON' }]} />
          </>
        )}
        foot={open && (
          <div className="flex flex-wrap gap-2">
            <button type="button" className="m14-btn" onClick={() => indir('json', [open.qid])}><Download aria-hidden="true" /> Bu kümeyi JSON indir</button>
          </div>
        )}
      >
        {open && tab === 'kume' && <KumeGorunumu key={open.qid} c={open} headers={headers} onChanged={() => { ac(open.qid); yukle(); }} onNext={sonraki} />}
        {open && tab === 'olaylar' && (
          <ol className="flex flex-col gap-2">
            {open.events.map((e) => (
              <li key={e.eventId} className="pk14-card" style={{ padding: '8px 12px' }}>
                <div className="text-sm text-ink-3">#{e.seq} · {fmt(e.ts)} · {who(e.actor)}</div>
                <div className="font-medium">{TYPE_LABEL[e.type] || e.type}</div>
                <div className="text-sm break-words">{preview(e.payload)}</div>
              </li>
            ))}
          </ol>
        )}
        {open && tab === 'json' && <pre className="text-xs whitespace-pre-wrap break-words">{JSON.stringify(open, null, 2)}</pre>}
      </Drawer>

      <Drawer open={topluSinif} onClose={() => setTopluSinif(false)} title={`${secim.count} kümeyi sınıflandır`}>
        <SiniflandirFormu busy={topluBusy} onSave={(b) => topluSiniflandir(b)} saveLabel={`${secim.count} kümeye kaydet`} />
      </Drawer>
    </div>
  );
};

const SiniflandirFormu: React.FC<{
  initial?: Record<string, any>;
  busy?: boolean;
  saveLabel: string;
  onSave: (b: { category: string; quality: string; tags: string[] }) => void;
  extra?: (b: { category: string; quality: string; tags: string[] }) => React.ReactNode;
}> = ({ initial = {}, busy, saveLabel, onSave, extra }) => {
  const [category, setCategory] = useState(initial.category || '');
  const [quality, setQuality] = useState(initial.quality || '');
  const [tags, setTags] = useState((initial.tags || []).join(', '));
  const body = { category, quality, tags: tags.split(',').map((t: string) => t.trim()).filter(Boolean) };
  return (
    <div className="flex flex-col gap-2">
      <div className="grid gap-2" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(min(100%, 180px), 1fr))' }}>
        <Field label="Kategori"><input className="ms-input" value={category} onChange={(e) => setCategory(e.target.value)} placeholder="ör. kök-tam, şık-eksik" /></Field>
        <Field label="Kalite"><select className="ms-input" value={quality} onChange={(e) => setQuality(e.target.value)}><option value="">—</option><option value="tam">Tam</option><option value="kismi">Kısmi</option><option value="belirsiz">Belirsiz</option><option value="kopya">Kopya</option><option value="hatali">Hatalı</option></select></Field>
        <Field label="Etiketler (virgülle)"><input className="ms-input" value={tags} onChange={(e) => setTags(e.target.value)} /></Field>
      </div>
      <div className="flex flex-wrap gap-2">
        <button type="button" className="m14-btn primary" disabled={busy} onClick={() => onSave(body)}>{saveLabel}</button>
        {extra?.(body)}
      </div>
    </div>
  );
};

const KumeGorunumu: React.FC<{ c: Cluster; headers: Record<string, string>; onChanged: () => void; onNext: () => void }> = ({ c, headers, onChanged, onNext }) => {
  const [discipline, setDiscipline] = useState(c.current?.discipline || '');
  const [topic, setTopic] = useState(c.current?.topic || '');
  const [answer, setAnswer] = useState(c.current?.claimedAnswer || '');
  const [note, setNote] = useState('');

  const post = async (path: string, body: any, ok: string) => {
    const r = await safeJsonFetch<any>(`/api/admin/raw-pool/${encodeURIComponent(c.qid)}/${path}`, { method: 'POST', headers, body: JSON.stringify(body) });
    if (r.ok && r.data?.success) { toast.success(ok); onChanged(); return true; }
    toast.error(r.data?.error || 'Kaydedilemedi.');
    return false;
  };

  const Liste: React.FC<{ title: string; rows: any[]; render: (r: any) => React.ReactNode }> = ({ title, rows, render }) =>
    rows?.length ? (
      <Card14 title={<>{title} <span className="text-ink-3 font-normal">({rows.length})</span></>}>
        <ul className="flex flex-col gap-1">
          {rows.map((r, i) => <li key={i} className="text-sm border-l-2 border-line pl-2 break-words">{render(r)}</li>)}
        </ul>
      </Card14>
    ) : null;
  const meta = (r: any) => <span className="text-ink-3"> — {r.author || r.suggestedBy || r.reportedBy || r.actor?.name || r.actor?.uid || 'anonim'} · {fmt(r.ts)}</span>;
  const katkiYok = !['fragments', 'options', 'alternativeOptions', 'comments', 'reports', 'fieldChanges'].some((k) => c.contributions?.[k]?.length) && !c.guard?.length && !c.ai?.length && !c.admin?.length;

  return (
    <DetailLayout
      main={
        <>
          <Card14 title="Ham kayıt (değiştirilemez)">
            <p className="text-sm text-ink-3">Bu defter yalnız eklemeyle büyür: kayıt silinemez ve üzerine yazılamaz. Yalnız sınıf, çalışma kopyası ve not ayrı olay olarak eklenir.</p>
          </Card14>
          {katkiYok && <p className="text-sm text-ink-3">Bu kümeye henüz katkı gelmemiş.</p>}
          <Liste title="Parçalar / ipuçları" rows={c.contributions.fragments} render={(r) => <>[{r.type || 'parça'}] {r.text}{meta(r)}</>} />
          <Liste title="Eklenen şıklar" rows={c.contributions.options} render={(r) => <>{r.key}) {r.text}{meta(r)}</>} />
          <Liste title='Alternatif şıklar / "bu şık yoktu" itirazları' rows={c.contributions.alternativeOptions} render={(r) => <>{r.key ? `${r.key}) ` : ''}{r.text || r.reason || JSON.stringify(r)}{meta(r)}</>} />
          <Liste title="Yorumlar" rows={c.contributions.comments} render={(r) => <>{r.text}{meta(r)}</>} />
          <Liste title="Bildirimler" rows={c.contributions.reports} render={(r) => <>{r.reason || r.text || r.message}{meta(r)}</>} />
          <Liste title="Değişiklik geçmişi (önceki hal saklı)" rows={c.contributions.fieldChanges} render={(r) => <>{preview(r)}{meta(r)}</>} />
          <Liste title="Koruma: geri konan katkılar" rows={c.guard} render={(r) => <>{r.field}: {r.note || `${(r.items || []).length} öge`}{meta(r)}</>} />
          <Liste title="YZ önerileri (ham veriyi değiştirmez)" rows={c.ai} render={(r) => <>{r.kind}: {JSON.stringify(r.result || r.optimizedData).slice(0, 220)}{meta(r)}</>} />
          <Liste title="Yönetici işlemleri" rows={c.admin} render={(r) => <>{TYPE_LABEL[r.type] || r.type}: {preview(r)}{meta(r)}</>} />
        </>
      }
      side={
        <>
          <FactList
            items={[
              { k: 'Kayıt no', v: <span className="font-mono text-xs">{c.qid}</span> },
              { k: 'Olay', v: c.eventCount },
              { k: 'İlk kayıt', v: fmt(c.firstSeen) },
              { k: 'Zincir', v: c.chain.ok ? <Pill tone="ok">Karma zinciri sağlam</Pill> : <Pill tone="bad">#{c.chain.brokenAt} olayında bozuk</Pill> },
              ...(c.deleted ? [{ k: 'Durum', v: 'Havuzdan kaldırılmış (tüm veri defterde)' }] : []),
            ]}
          />
          <Card14 title={<span className="inline-flex items-center gap-1"><Tags className="w-4 h-4" aria-hidden="true" /> Sınıflandır</span>}>
            <SiniflandirFormu
              initial={c.classification || {}}
              saveLabel="Sınıfı kaydet"
              onSave={(b) => post('classify', b, 'Sınıflandırma kaydedildi.')}
              extra={(b) => (
                <button type="button" className="m14-btn" onClick={async () => { if (await post('classify', b, 'Sınıflandırma kaydedildi.')) onNext(); }}>Kaydet ve sonraki</button>
              )}
            />
          </Card14>
          {!c.deleted && (
            <Card14 title={<span className="inline-flex items-center gap-1"><PencilLine className="w-4 h-4" aria-hidden="true" /> Çalışma kopyasını düzenle</span>}>
              <p className="text-sm text-ink-3 mb-2">Önceki değer ve düzenleme deftere ayrı olay olarak yazılır; ham katkılar değişmez.</p>
              <div className="grid gap-2" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(min(100%, 160px), 1fr))' }}>
                <Field label="Ders"><input className="ms-input" value={discipline} onChange={(e) => setDiscipline(e.target.value)} /></Field>
                <Field label="Konu"><input className="ms-input" value={topic} onChange={(e) => setTopic(e.target.value)} /></Field>
                <Field label="Cevap"><select className="ms-input" value={answer} onChange={(e) => setAnswer(e.target.value)}><option value="">—</option>{['A', 'B', 'C', 'D', 'E'].map((k) => <option key={k}>{k}</option>)}</select></Field>
              </div>
              <button type="button" className="m14-btn mt-2" onClick={() => post('edit', { patch: { discipline, topic, claimedAnswer: answer || undefined } }, 'Düzenleme kaydedildi.')}>Düzenlemeyi kaydet</button>
            </Card14>
          )}
          <Card14 title={<span className="inline-flex items-center gap-1"><StickyNote className="w-4 h-4" aria-hidden="true" /> Not ekle</span>}>
            <textarea className="ms-input w-full" rows={2} value={note} onChange={(e) => setNote(e.target.value)} aria-label="Not" />
            <button type="button" className="m14-btn mt-2" disabled={!note.trim()} onClick={() => { post('note', { text: note }, 'Not eklendi.'); setNote(''); }}>Notu ekle</button>
          </Card14>
        </>
      }
    />
  );
};
