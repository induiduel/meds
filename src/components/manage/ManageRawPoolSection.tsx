import React, { useEffect, useMemo, useState } from 'react';
import { Archive, Download, Info, ShieldCheck, ShieldAlert, Tags, PencilLine, StickyNote, FileJson } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { toast } from '../ui/Toast';
import { ChipBar, Drawer, EmptyState, Field, SearchBox, Seg } from './consoleUi';

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

  return (
    <div className="flex flex-col gap-3 min-w-0">
      <div className="ms-alert is-accent">
        <Info aria-hidden="true" />
        <span>
          Kullanıcıların eklediği sorular ve katkıları <b>ham veridir</b>: soru başına tek kümede, yalnız eklenen bir defterde tutulur. Hiçbir
          olay silinmez ya da değiştirilmez; sınıflandırma, düzenleme ve YZ önerileri ayrı olay olarak eklenir. Havuz soruları RAG'e alınmaz.
        </span>
      </div>

      <div className="flex flex-wrap items-center gap-2">
        <SearchBox value={q} onChange={setQ} placeholder="Soru, ders, etiket ara" count={liste.length} className="flex-1 min-w-[220px]" />
        <button type="button" className="ms-btn" onClick={() => indir('json')}><Download /> JSON (kümeler)</button>
        <button type="button" className="ms-btn" onClick={() => indir('jsonl')}><FileJson /> JSONL (olaylar)</button>
        <button type="button" className="ms-btn" onClick={() => indir('csv')}><Download /> CSV</button>
      </div>

      <ChipBar
        label="Süzgeç"
        value={filtre}
        onChange={setFiltre}
        wrap
        options={[
          { id: 'hepsi', label: 'Hepsi', n: say.hepsi },
          { id: 'katki', label: 'Katkı almış', n: say.katki },
          { id: 'siniflanmamis', label: 'Sınıflanmamış', n: say.siniflanmamis },
          { id: 'yz', label: 'YZ önerisi var', n: say.yz },
          { id: 'silinmis', label: 'Havuzdan kaldırılmış', n: say.silinmis },
          ...(say.bozuk ? [{ id: 'bozuk' as const, label: 'Zincir bozuk', n: say.bozuk }] : []),
        ]}
      />

      {items === null ? (
        <div className="h-48 rounded-2xl ms-shimmer" role="status" aria-label="Yükleniyor" />
      ) : liste.length === 0 ? (
        <section className="ms-panel"><EmptyState icon={Archive} title="Bu süzgeçte küme yok" /></section>
      ) : (
        <section className="ms-panel" style={{ padding: 0 }}>
          {liste.slice(0, 300).map((x) => (
            <button key={x.qid} type="button" className="ms-row w-full text-left" onClick={() => ac(x.qid)} style={{ display: 'flex', gap: 12, padding: '10px 14px', alignItems: 'flex-start' }}>
              {x.chain.ok ? <ShieldCheck className="w-4 h-4 shrink-0 text-ok" aria-label="Zincir sağlam" /> : <ShieldAlert className="w-4 h-4 shrink-0 text-danger" aria-label="Zincir bozuk" />}
              <span className="min-w-0 flex-1">
                <span className="block truncate font-medium">{x.title}</span>
                <span className="block text-sm text-ink-3 truncate">
                  {[x.committeeId, x.questionNumber ? `S.${x.questionNumber}` : null, x.discipline, x.deleted ? 'havuzdan kaldırıldı' : null].filter(Boolean).join(' · ')}
                  {Object.keys(x.classification || {}).length ? ` · sınıf: ${[x.classification.category, x.classification.quality, ...(x.classification.tags || [])].filter(Boolean).join(', ')}` : ''}
                </span>
              </span>
              <span className="text-sm text-ink-3 tabular-nums shrink-0 text-right">
                {x.eventCount} olay
                <br />
                {fmt(x.lastEvent)}
              </span>
            </button>
          ))}
        </section>
      )}

      <Drawer
        open={!!open}
        onClose={() => setOpen(null)}
        wide
        title={open?.title || ''}
        head={open && <Seg label="Görünüm" value={tab} onChange={setTab} options={[{ id: 'kume', label: 'Küme' }, { id: 'olaylar', label: 'Olaylar', n: open.events.length }, { id: 'json', label: 'JSON' }]} />}
        foot={open && (
          <div className="flex gap-2">
            <button type="button" className="ms-btn" onClick={() => indir('json', [open.qid])}><Download /> Bu kümeyi JSON indir</button>
          </div>
        )}
      >
        {open && tab === 'kume' && <KumeGorunumu c={open} headers={headers} onChanged={() => { ac(open.qid); yukle(); }} />}
        {open && tab === 'olaylar' && (
          <ol className="flex flex-col gap-2">
            {open.events.map((e) => (
              <li key={e.eventId} className="ms-panel" style={{ padding: '8px 12px' }}>
                <div className="text-sm text-ink-3">#{e.seq} · {fmt(e.ts)} · {who(e.actor)}</div>
                <div className="font-medium">{TYPE_LABEL[e.type] || e.type}</div>
                <div className="text-sm break-words">{preview(e.payload)}</div>
              </li>
            ))}
          </ol>
        )}
        {open && tab === 'json' && <pre className="text-xs whitespace-pre-wrap break-words">{JSON.stringify(open, null, 2)}</pre>}
      </Drawer>
    </div>
  );
};

const KumeGorunumu: React.FC<{ c: Cluster; headers: Record<string, string>; onChanged: () => void }> = ({ c, headers, onChanged }) => {
  const cls = c.classification || {};
  const [category, setCategory] = useState(cls.category || '');
  const [quality, setQuality] = useState(cls.quality || '');
  const [tags, setTags] = useState((cls.tags || []).join(', '));
  const [discipline, setDiscipline] = useState(c.current?.discipline || '');
  const [topic, setTopic] = useState(c.current?.topic || '');
  const [answer, setAnswer] = useState(c.current?.claimedAnswer || '');
  const [note, setNote] = useState('');

  const post = async (path: string, body: any, ok: string) => {
    const r = await safeJsonFetch<any>(`/api/admin/raw-pool/${encodeURIComponent(c.qid)}/${path}`, { method: 'POST', headers, body: JSON.stringify(body) });
    if (r.ok && r.data?.success) { toast.success(ok); onChanged(); } else toast.error(r.data?.error || 'Kaydedilemedi.');
  };

  const Liste: React.FC<{ title: string; rows: any[]; render: (r: any) => React.ReactNode }> = ({ title, rows, render }) =>
    rows.length ? (
      <section>
        <h3 className="font-semibold mb-1">{title} <span className="text-ink-3">({rows.length})</span></h3>
        <ul className="flex flex-col gap-1">
          {rows.map((r, i) => <li key={i} className="text-sm border-l-2 border-line pl-2">{render(r)}</li>)}
        </ul>
      </section>
    ) : null;
  const meta = (r: any) => <span className="text-ink-3"> — {r.author || r.suggestedBy || r.reportedBy || r.actor?.name || r.actor?.uid || 'anonim'} · {fmt(r.ts)}</span>;

  return (
    <div className="flex flex-col gap-4">
      <div className="text-sm text-ink-3">
        {c.qid} · {c.eventCount} olay · ilk kayıt {fmt(c.firstSeen)} · {c.chain.ok ? 'karma zinciri sağlam' : `zincir #${c.chain.brokenAt} olayında bozuk`}
        {c.deleted ? ' · havuzdan kaldırılmış (tüm veri defterde)' : ''}
      </div>

      <Liste title="Parçalar / ipuçları" rows={c.contributions.fragments} render={(r) => <>[{r.type || 'parça'}] {r.text}{meta(r)}</>} />
      <Liste title="Eklenen şıklar" rows={c.contributions.options} render={(r) => <>{r.key}) {r.text}{meta(r)}</>} />
      <Liste title='Alternatif şıklar / "bu şık yoktu" itirazları' rows={c.contributions.alternativeOptions} render={(r) => <>{r.key ? `${r.key}) ` : ''}{r.text || r.reason || JSON.stringify(r)}{meta(r)}</>} />
      <Liste title="Yorumlar" rows={c.contributions.comments} render={(r) => <>{r.text}{meta(r)}</>} />
      <Liste title="Bildirimler" rows={c.contributions.reports} render={(r) => <>{r.reason || r.text || r.message}{meta(r)}</>} />
      <Liste title="Değişiklik geçmişi (önceki hal saklı)" rows={c.contributions.fieldChanges} render={(r) => <>{preview(r)}{meta(r)}</>} />
      <Liste title="Koruma: geri konan katkılar" rows={c.guard} render={(r) => <>{r.field}: {r.note || `${(r.items || []).length} öge`}{meta(r)}</>} />
      <Liste title="YZ önerileri (ham veriyi değiştirmez)" rows={c.ai} render={(r) => <>{r.kind}: {JSON.stringify(r.result || r.optimizedData).slice(0, 220)}{meta(r)}</>} />
      <Liste title="Yönetici işlemleri" rows={c.admin} render={(r) => <>{TYPE_LABEL[r.type] || r.type}: {preview(r)}{meta(r)}</>} />

      <section className="ms-panel" style={{ padding: 12 }}>
        <h3 className="font-semibold mb-2 flex items-center gap-1"><Tags className="w-4 h-4" /> Sınıflandır</h3>
        <div className="grid gap-2" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))' }}>
          <Field label="Kategori"><input className="ms-input" value={category} onChange={(e) => setCategory(e.target.value)} placeholder="ör. kök-tam, şık-eksik" /></Field>
          <Field label="Kalite"><select className="ms-input" value={quality} onChange={(e) => setQuality(e.target.value)}><option value="">—</option><option value="tam">Tam</option><option value="kismi">Kısmi</option><option value="belirsiz">Belirsiz</option><option value="kopya">Kopya</option><option value="hatali">Hatalı</option></select></Field>
          <Field label="Etiketler (virgülle)"><input className="ms-input" value={tags} onChange={(e) => setTags(e.target.value)} /></Field>
        </div>
        <button type="button" className="ms-btn is-primary mt-2" onClick={() => post('classify', { category, quality, tags: tags.split(',').map((t: string) => t.trim()).filter(Boolean) }, 'Sınıflandırma kaydedildi.')}>Sınıflandırmayı kaydet</button>
      </section>

      {!c.deleted && (
        <section className="ms-panel" style={{ padding: 12 }}>
          <h3 className="font-semibold mb-2 flex items-center gap-1"><PencilLine className="w-4 h-4" /> Çalışma kopyasını düzenle</h3>
          <p className="text-sm text-ink-3 mb-2">Önceki değer ve düzenleme deftere ayrı olay olarak yazılır; ham katkılar değişmez.</p>
          <div className="grid gap-2" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))' }}>
            <Field label="Ders"><input className="ms-input" value={discipline} onChange={(e) => setDiscipline(e.target.value)} /></Field>
            <Field label="Konu"><input className="ms-input" value={topic} onChange={(e) => setTopic(e.target.value)} /></Field>
            <Field label="Cevap"><select className="ms-input" value={answer} onChange={(e) => setAnswer(e.target.value)}><option value="">—</option>{['A', 'B', 'C', 'D', 'E'].map((k) => <option key={k}>{k}</option>)}</select></Field>
          </div>
          <button type="button" className="ms-btn mt-2" onClick={() => post('edit', { patch: { discipline, topic, claimedAnswer: answer || undefined } }, 'Düzenleme kaydedildi.')}>Düzenlemeyi kaydet</button>
        </section>
      )}

      <section className="ms-panel" style={{ padding: 12 }}>
        <h3 className="font-semibold mb-2 flex items-center gap-1"><StickyNote className="w-4 h-4" /> Not ekle</h3>
        <textarea className="ms-input w-full" rows={2} value={note} onChange={(e) => setNote(e.target.value)} />
        <button type="button" className="ms-btn mt-2" disabled={!note.trim()} onClick={() => { post('note', { text: note }, 'Not eklendi.'); setNote(''); }}>Notu ekle</button>
      </section>
    </div>
  );
};
