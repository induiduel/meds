import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { ArrowUpRight, CheckCircle2, ChevronLeft, ChevronRight, CircleAlert, CircleDashed, Copy, Download, Eye, Link2, Plus, Save, Tag, Trash2, X } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { toast } from '../ui/Toast';
import { TagInput } from '../ui/TagInput';
import { confirmDialog } from '../ui/ConfirmDialog';
import { EmptyState, Drawer, Seg } from './consoleUi';
import { PageActions, StatRow, Tabs14, SearchField, Toolbar, DataTable, DetailNav, Pill, type Col } from '../v14/pageKit';
import { BulkBar, useSelection, JsonView, type BulkAction } from '../v14/manageKit';
import './catalog.css';

/**
 * Veri kataloğu: uygulamadaki her veri türü tek ekranda.
 *  - Tür seç → ara, sınıflara göre süz (kurul, ders, tür…), sırala, sayfala.
 *  - Her kayıt ayrı DEĞERLENDİRİLİR (Onaylı / İncelemede / Sorunlu) ve ETİKETLENİR; toplu da yapılabilir.
 *    Bu katman kaynak veriyi değiştirmez (sunucuda data/catalog_annotations.json).
 *  - Kayıt sayfası: düzenlenebilir alanlar (sunucu yalnız izinli alanları yazar, yedek alır), ilişkiler
 *    (deste ↔ kazanım ↔ örnek soru ↔ çıkmış ↔ terim ↔ hastalık; dokununca o kayda gider), ham JSON.
 *  - Toplu seçim (sayfa ya da süzgece uyan tümü) → Sil (çöp kutusuna, geri yüklenebilir) / Kalıcı sil.
 *    Çöp kutusu ayrı bir tür olarak listelenir: Geri yükle / Kalıcı sil.
 * Uçlar: src/services/dataCatalogService.ts
 */
type Status = '' | 'onayli' | 'inceleme' | 'sorunlu';
interface Ann { status: Status; tags: string[]; note: string; updatedAt: string; by?: string }
interface EntityInfo { id: string; label: string; group: string; source: string; creatable?: boolean; editable: string[]; deletable?: boolean; restorable?: boolean; arrays: string[]; facets: { key: string; label: string }[]; count: number; reviewed: Record<string, number> }
interface Item { id: string; title: string; subtitle: string; ann: Ann | null }
interface ListResp { total: number; page: number; size: number; items: Item[]; facets: Record<string, { value: string; n: number }[]> }
interface Rel { entity: string; id: string; title: string; why: string }
interface Detail { id: string; title: string; record: Record<string, any>; relations: Rel[]; ann: Ann | null; editable: string[]; form?: Record<string, any> | null; site?: { status: 'shown' | 'merged' | 'hidden'; shownId?: string } }
interface FormField { key: string; label: string; kind?: 'text' | 'long' | 'number' | 'options' | 'choice' | 'list'; required?: boolean; choices?: string[]; free?: boolean; hint?: string }
/** Yeni kayıt (base yok) ya da çoğaltma (base = asıl kaydın kimliği + ön dolu form) */
interface CreateTarget { entity: string; base?: { id: string; title: string; form: Record<string, any> } }
const OPTION_KEYS = ['A', 'B', 'C', 'D', 'E'];

const STATUS: { id: Status | 'yok'; label: string; icon: React.ElementType; tone: string }[] = [
  { id: 'onayli', label: 'Onaylı', icon: CheckCircle2, tone: 'is-ok' },
  { id: 'inceleme', label: 'İncelemede', icon: Eye, tone: 'is-warn' },
  { id: 'sorunlu', label: 'Sorunlu', icon: CircleAlert, tone: 'is-bad' },
  { id: 'yok', label: 'Değerlendirilmedi', icon: CircleDashed, tone: '' },
];
const statusMeta = (s?: string) => STATUS.find((x) => x.id === s);
const PAGE = 50;
/** Alan adlarının Türkçe karşılıkları (bilinmeyen alan olduğu gibi gösterilir) */
const FIELD_LABELS: Record<string, string> = {
  stem: 'Soru kökü', correctAnswer: 'Doğru cevap', explanation: 'Açıklama', topic: 'Konu', discipline: 'Ders', committeeId: 'Kurul',
  examYear: 'Sınav yılı', tags: 'Etiketler', title: 'Başlık', shortTitle: 'Kısa başlık', committee: 'Kurul', instructor: 'Öğretim üyesi',
  category: 'Kategori', term: 'Terim', definition: 'Tanım', description: 'Açıklama', clinicalPearl: 'Klinik inci', aliases: 'Eş anlamlılar',
  front: 'Ön yüz', back: 'Arka yüz', note: 'Not', answer: 'Cevap', konu: 'Konu', group: 'Grup', artist: 'Sanatçı', url: 'Bağlantı',
};

const api = async <T,>(url: string, init?: RequestInit): Promise<T> => {
  const r = await safeJsonFetch<T>(url, init);
  if (!r.ok) throw new Error((r.data as any)?.error || r.error || `İstek başarısız (${r.status})`);
  return r.data as T;
};
const toCsv = (rows: Item[]) => {
  const esc = (v: unknown) => `"${String(v ?? '').replace(/"/g, '""')}"`;
  return ['id;başlık;açıklama;durum;etiketler', ...rows.map((r) => [r.id, r.title, r.subtitle, statusMeta(r.ann?.status || 'yok')?.label, (r.ann?.tags || []).join(', ')].map(esc).join(';'))].join('\n');
};

export const ManageCatalogSection: React.FC<{ adminEmail: string }> = ({ adminEmail }) => {
  const headers = useMemo(() => ({ 'Content-Type': 'application/json', 'x-admin-email': adminEmail }), [adminEmail]);
  const [entities, setEntities] = useState<EntityInfo[]>([]);
  const [entity, setEntity] = useState<string>(() => {
    try { return localStorage.getItem('medsoru_catalog_entity') || 'past'; } catch { return 'past'; }
  });
  const [q, setQ] = useState('');
  const [debQ, setDebQ] = useState('');
  const [filters, setFilters] = useState<Record<string, string>>({});
  const [sort, setSort] = useState('');
  const [page, setPage] = useState(0);
  const [list, setList] = useState<ListResp | null>(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState('');
  const selection = useSelection<string>();
  const sel = selection.sel;
  const [open, setOpen] = useState<{ entity: string; id: string } | null>(null);
  const [creating, setCreating] = useState<CreateTarget | null>(null);
  const reqId = useRef(0);

  const info = entities.find((e) => e.id === entity);
  const groups = useMemo(() => {
    const m = new Map<string, EntityInfo[]>();
    for (const e of entities) m.set(e.group, [...(m.get(e.group) || []), e]);
    return Array.from(m);
  }, [entities]);

  const loadEntities = useCallback(() => {
    api<{ entities: EntityInfo[] }>('/api/admin/catalog', { headers }).then((d) => setEntities(d.entities)).catch((e) => setErr(e.message));
  }, [headers]);
  useEffect(loadEntities, [loadEntities]);

  useEffect(() => {
    const t = window.setTimeout(() => setDebQ(q.trim()), 280);
    return () => window.clearTimeout(t);
  }, [q]);
  useEffect(() => {
    try { localStorage.setItem('medsoru_catalog_entity', entity); } catch { /* yok */ }
    setFilters({});
    setPage(0);
    selection.clear();
  }, [entity]);
  useEffect(() => { setPage(0); selection.clear(); }, [debQ, filters, sort]); // eslint-disable-line react-hooks/exhaustive-deps

  const load = useCallback(() => {
    const id = ++reqId.current;
    const p = new URLSearchParams({ q: debQ, page: String(page), size: String(PAGE), sort });
    for (const [k, v] of Object.entries(filters)) if (v) p.set(`f.${k}`, v);
    setLoading(true);
    setErr('');
    api<ListResp>(`/api/admin/catalog/${entity}?${p}`, { headers })
      .then((d) => { if (id === reqId.current) setList(d); })
      .catch((e) => { if (id === reqId.current) setErr(e.message); })
      .finally(() => { if (id === reqId.current) setLoading(false); });
  }, [entity, debQ, page, sort, filters, headers]);
  useEffect(load, [load]);

  const annotate = async (ids: string[], body: Record<string, unknown>, ent = entity) => {
    await api(`/api/admin/catalog/${ent}/annotate`, { method: 'POST', headers, body: JSON.stringify({ ids, ...body }) });
    load();
    loadEntities();
  };
  const bulk = async (body: Record<string, unknown>, label: string) => {
    const ids = Array.from(sel);
    try {
      await annotate(ids, body);
      toast.success(label, `${ids.length} kayıt güncellendi.`);
      selection.clear();
    } catch (e: any) {
      toast.error('Güncellenemedi', e.message);
    }
  };
  const [bulkTag, setBulkTag] = useState('');
  const [busyBulk, setBusyBulk] = useState(false);
  const isTrash = entity === 'trash';

  /** Süzgece uyan tüm kayıtları seç (sayfalardan bağımsız) */
  const selectAllMatching = async () => {
    const p = new URLSearchParams({ q: debQ, idsOnly: '1' });
    for (const [k, v] of Object.entries(filters)) if (v) p.set(`f.${k}`, v);
    try {
      const d = await api<{ ids: string[] }>(`/api/admin/catalog/${entity}?${p}`, { headers });
      selection.clear();
      selection.toggleAll(d.ids);
    } catch (e: any) {
      toast.error('Seçilemedi', e.message);
    }
  };

  const removeSelected = async (permanent: boolean) => {
    const ids = Array.from(sel);
    setBusyBulk(true);
    try {
      const r = await api<{ deleted: number }>(`/api/admin/catalog/${entity}/delete`, { method: 'POST', headers, body: JSON.stringify({ ids, permanent }) });
      toast.success(permanent || isTrash ? 'Kalıcı olarak silindi' : 'Çöp kutusuna taşındı', `${r.deleted.toLocaleString('tr-TR')} kayıt.`);
      selection.clear();
      load();
      loadEntities();
    } catch (e: any) {
      toast.error('Silinemedi', e.message);
    } finally {
      setBusyBulk(false);
    }
  };

  const duplicateSelected = async () => {
    const ids = Array.from(sel);
    if (ids.length > 20 && !(await confirmDialog({ title: `${ids.length.toLocaleString('tr-TR')} kayıt çoğaltılsın mı?`, message: 'Her kaydın kopyası yeni kimlikle aslının arkasına eklenir.', confirmLabel: 'Çoğalt' }))) return;
    setBusyBulk(true);
    try {
      const r = await api<{ ids: string[]; note: string }>(`/api/admin/catalog/${entity}/duplicate`, { method: 'POST', headers, body: JSON.stringify({ ids }) });
      toast.success(`${r.ids.length.toLocaleString('tr-TR')} kayıt çoğaltıldı`, r.note);
      selection.clear();
    } catch (e: any) {
      toast.error('Çoğaltılamadı', e.message);
    } finally {
      setBusyBulk(false);
      load();
      loadEntities();
    }
  };

  const restoreSelected = async () => {
    const ids = Array.from(sel);
    setBusyBulk(true);
    try {
      const r = await api<{ restored: number; errors: string[] }>('/api/admin/catalog/trash/restore', { method: 'POST', headers, body: JSON.stringify({ ids }) });
      if (r.errors?.length) toast.error('Bazıları geri yüklenemedi', r.errors.join(' · '));
      if (r.restored) toast.success('Geri yüklendi', `${r.restored.toLocaleString('tr-TR')} kayıt kaynağına döndü.`);
      selection.clear();
      load();
      loadEntities();
    } catch (e: any) {
      toast.error('Geri yüklenemedi', e.message);
    } finally {
      setBusyBulk(false);
    }
  };

  const exportCsv = () => {
    if (!list?.items.length) return;
    const blob = new Blob(['﻿' + toCsv(list.items)], { type: 'text/csv;charset=utf-8' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `katalog-${entity}-s${page + 1}.csv`;
    a.click();
    URL.revokeObjectURL(a.href);
  };

  const pages = list ? Math.max(1, Math.ceil(list.total / PAGE)) : 1;
  const items = list?.items || [];
  const reviewedN = info ? Object.entries(info.reviewed || {}).reduce((a, [k, v]) => (k && k !== 'yok' ? a + (v || 0) : a), 0) : 0;
  const trashN = entities.find((e) => e.id === 'trash')?.count;
  const statusTab = (filters.status || 'all') as string;

  const cols: Col<Item>[] = [
    { key: 'title', label: 'Kayıt', main: true, render: (it) => (
      <>{it.title || <i>(başlıksız)</i>}{it.subtitle ? <span className="ct-sub"> · {it.subtitle}</span> : null}</>
    ) },
    { key: 'status', label: 'Durum', width: 140, render: (it) => {
      const st = statusMeta(it.ann?.status);
      return st && it.ann?.status ? <Pill tone={st.tone === 'is-ok' ? 'ok' : st.tone === 'is-warn' ? 'warn' : 'bad'}>{st.label}</Pill> : <span className="ct-muted">—</span>;
    } },
    { key: 'tags', label: 'Etiketler', width: 180, render: (it) => (
      <span className="ct-tags">{(it.ann?.tags || []).slice(0, 3).map((t) => <span key={t} className="ui-tag">#{t}</span>)}</span>
    ) },
    { key: 'id', label: 'Kimlik', mono: true, width: 150, render: (it) => it.id },
  ];

  const bulkActions: BulkAction[] = isTrash
    ? [
        { label: 'Geri yükle', kind: 'main', run: restoreSelected },
        { label: 'Kalıcı sil', kind: 'danger', confirm: `${sel.size} kaydı kalıcı sil (geri alınamaz)`, run: () => removeSelected(true) },
      ]
    : [
        ...STATUS.slice(0, 3).map((s): BulkAction => ({ label: s.label, kind: s.id === 'onayli' ? 'main' : undefined, run: () => bulk({ status: s.id }, s.label) })),
        { label: 'Durumu kaldır', run: () => bulk({ status: '' }, 'Değerlendirme kaldırıldı') },
        ...(info?.creatable ? [{ label: 'Çoğalt', run: duplicateSelected } as BulkAction] : []),
        ...(info?.deletable ? [
          { label: 'Çöpe taşı', kind: 'danger', confirm: `${sel.size} kaydı çöpe taşı`, run: () => removeSelected(false) } as BulkAction,
          { label: 'Kalıcı sil', kind: 'danger', confirm: `${sel.size} kaydı kalıcı sil (geri alınamaz)`, run: () => removeSelected(true) } as BulkAction,
        ] : []),
      ];

  return (
    <div className="ct-root">
      {/* Tür seçici: gruplu, sayılı */}
      <nav className="ct-types" aria-label="Veri türü">
        {groups.map(([g, list]) => (
          <div key={g} className="ct-tgroup">
            <span className="ct-tg">{g}</span>
            {list.map((e) => (
              <button key={e.id} type="button" className={`ct-type ${e.id === entity ? 'is-on' : ''}`} aria-pressed={e.id === entity} onClick={() => setEntity(e.id)}>
                <span>{e.label}</span>
                <b>{e.count.toLocaleString('tr-TR')}</b>
                {(e.reviewed.sorunlu || 0) > 0 && <i className="ct-dot is-bad" title={`${e.reviewed.sorunlu} sorunlu`} />}
              </button>
            ))}
          </div>
        ))}
      </nav>

      <div className="ct-main">
        <PageActions note={info ? <>{info.label} · kaynak <code className="ct-code">{info.source}</code> · {info.editable.length ? 'düzenlenebilir alanlar var' : 'salt okunur (değerlendirme açık)'}</> : 'Yükleniyor…'}>
          {!isTrash && entities.some((e) => e.id === 'trash') && (
            <button type="button" className="m14-btn" onClick={() => setEntity('trash')}><Trash2 aria-hidden /> Çöp kutusu</button>
          )}
          <button type="button" className="m14-btn" onClick={exportCsv} disabled={!list?.items.length} title="Bu sayfayı CSV olarak indir"><Download aria-hidden /> CSV</button>
          {info?.creatable && (
            <button type="button" className="m14-btn primary" onClick={() => setCreating({ entity })} title="Bu türün şablonuyla yeni kayıt ekle"><Plus aria-hidden /> Yeni kayıt</button>
          )}
        </PageActions>

        <StatRow stats={[
          { label: 'Kayıt', value: (list?.total ?? info?.count ?? 0).toLocaleString('tr-TR') },
          { label: 'Değerlendirilmiş', value: reviewedN.toLocaleString('tr-TR'), tone: 'ok' },
          { label: 'Sorunlu', value: (info?.reviewed.sorunlu || 0).toLocaleString('tr-TR'), tone: (info?.reviewed.sorunlu || 0) > 0 ? 'bad' : undefined, onClick: () => setFilters((f) => ({ ...f, status: 'sorunlu' })), hint: 'Sorunluları süz' },
          ...(trashN !== undefined ? [{ label: 'Çöpte', value: trashN.toLocaleString('tr-TR'), onClick: () => setEntity('trash'), hint: 'Çöp kutusunu aç' }] : []),
        ]} />

        <Toolbar>
          <Tabs14<string>
            label="Değerlendirme durumu"
            value={statusTab}
            onChange={(v) => setFilters((f) => ({ ...f, status: v === 'all' ? '' : v }))}
            options={[{ id: 'all', label: 'Tümü' }, ...STATUS.map((s) => ({ id: s.id as string, label: s.label, n: list?.facets.status?.find((x) => x.value === s.id)?.n }))]}
          />
          <SearchField value={q} onChange={setQ} placeholder={`${info?.label || 'Kayıt'} içinde ara`} />
        </Toolbar>
        <Toolbar>
          <select className="pk14-sel" value={sort} onChange={(e) => setSort(e.target.value)} aria-label="Sıralama">
            <option value="">Varsayılan sıra</option>
            <option value="title">Başlığa göre</option>
            <option value="updated">Son güncellenen</option>
          </select>
          {info?.facets.map((f) => {
            const opts = list?.facets[f.key] || [];
            if (!opts.length && !filters[f.key]) return null;
            return (
              <select key={f.key} className={`pk14-sel ${filters[f.key] ? 'is-on' : ''}`} value={filters[f.key] || ''} onChange={(e) => setFilters((x) => ({ ...x, [f.key]: e.target.value }))} aria-label={f.label}>
                <option value="">{f.label}: tümü</option>
                {opts.map((o) => <option key={o.value} value={o.value}>{o.value} ({o.n})</option>)}
              </select>
            );
          })}
          {(list?.facets.tag?.length || filters.tag) ? (
            <select className={`pk14-sel ${filters.tag ? 'is-on' : ''}`} value={filters.tag || ''} onChange={(e) => setFilters((x) => ({ ...x, tag: e.target.value }))} aria-label="Etiket">
              <option value="">Etiket: tümü</option>
              {(list?.facets.tag || []).map((o) => <option key={o.value} value={o.value}>#{o.value} ({o.n})</option>)}
            </select>
          ) : null}
          {Object.values(filters).some(Boolean) && (
            <button type="button" className="m14-btn ghost" onClick={() => setFilters({})}><X aria-hidden /> Süzgeçleri temizle</button>
          )}
          {list && <span className="ct-count">{list.total.toLocaleString('tr-TR')} kayıt · sayfa {page + 1}/{pages}</span>}
        </Toolbar>

        <BulkBar count={sel.size} noun="kayıt" busy={busyBulk} onClear={selection.clear} actions={bulkActions} />
        {sel.size > 0 && (
          <div className="ct-bulk-extra">
            {list && sel.size < list.total && (
              <button type="button" className="m14-btn ghost" onClick={() => void selectAllMatching()}>Süzgece uyan tümünü seç ({list.total.toLocaleString('tr-TR')})</button>
            )}
            {!isTrash && (
              <form className="ct-bulk-tag" onSubmit={(e) => { e.preventDefault(); if (bulkTag.trim()) { void bulk({ addTags: [bulkTag.trim()] }, 'Etiket eklendi'); setBulkTag(''); } }}>
                <Tag aria-hidden />
                <input value={bulkTag} onChange={(e) => setBulkTag(e.target.value)} placeholder="Seçililere etiket ekle" aria-label="Seçililere etiket ekle" />
              </form>
            )}
          </div>
        )}
        {sel.size === 0 && list && list.total > list.items.length && (
          <button type="button" className="ct-selall" onClick={() => void selectAllMatching()}>Süzgece uyan tümünü seç ({list.total.toLocaleString('tr-TR')})</button>
        )}

        {err && <div className="ui-callout is-bad"><CircleAlert /> {err}</div>}

        <DataTable<Item>
          rows={items}
          cols={cols}
          rowKey={(it) => it.id}
          onOpen={(it) => setOpen({ entity, id: it.id })}
          selection={selection}
          busy={loading}
          minWidth={720}
          activeKey={open?.entity === entity ? open.id : null}
          empty={loading ? 'Yükleniyor…' : <EmptyState title="Kayıt yok">Aramayı ya da süzgeçleri değiştirin.</EmptyState>}
        />

        {pages > 1 && (
          <nav className="ct-pager" aria-label="Sayfalar">
            <button type="button" className="m14-btn" disabled={page === 0} onClick={() => setPage((p) => p - 1)}><ChevronLeft aria-hidden /> Önceki</button>
            <span>{page + 1} / {pages}</span>
            <button type="button" className="m14-btn" disabled={page >= pages - 1} onClick={() => setPage((p) => p + 1)}>Sonraki <ChevronRight aria-hidden /></button>
          </nav>
        )}
      </div>

      {open && (
        <CatalogDetail
          key={`${open.entity}:${open.id}`}
          target={open}
          entities={entities}
          headers={headers}
          nav={open.entity === entity ? items : []}
          onClose={() => setOpen(null)}
          onNavigate={(t) => setOpen(t)}
          onSaved={() => { load(); loadEntities(); }}
          annotate={annotate}
          onDuplicate={(base) => { setOpen(null); setCreating({ entity: open.entity, base }); }}
        />
      )}

      {creating && (
        <CatalogCreate
          key={`${creating.entity}:${creating.base?.id || 'yeni'}`}
          target={creating}
          entity={entities.find((e) => e.id === creating.entity)}
          headers={headers}
          onClose={() => setCreating(null)}
          onCreated={(id) => { const ent = creating.entity; setCreating(null); load(); loadEntities(); setOpen({ entity: ent, id }); }}
        />
      )}
    </div>
  );
};

const CatalogDetail: React.FC<{
  target: { entity: string; id: string };
  entities: EntityInfo[];
  headers: Record<string, string>;
  nav: Item[];
  onClose: () => void;
  onNavigate: (t: { entity: string; id: string }) => void;
  onSaved: () => void;
  annotate: (ids: string[], body: Record<string, unknown>, ent?: string) => Promise<void>;
  onDuplicate: (base: { id: string; title: string; form: Record<string, any> }) => void;
}> = ({ target, entities, headers, nav, onClose, onNavigate, onSaved, annotate, onDuplicate }) => {
  const [d, setD] = useState<Detail | null>(null);
  const [err, setErr] = useState('');
  const [tab, setTab] = useState<'fields' | 'review' | 'rel' | 'raw'>('fields');
  const [rawView, setRawView] = useState<'gorsel' | 'ham'>('gorsel');
  const [draft, setDraft] = useState<Record<string, any>>({});
  const [ann, setAnn] = useState<Ann>({ status: '', tags: [], note: '', updatedAt: '' });
  const [busy, setBusy] = useState(false);
  const ent = entities.find((e) => e.id === target.entity);

  useEffect(() => {
    // "ders:<id>" kısa yolu: ilişki bir ders grubuna işaret ediyor → kayıt yerine bilgi göster
    if (target.id.startsWith('ders:')) { setErr('Bu bağlantı bir ders grubudur; Örnek sorular listesinde ders süzgeciyle açın.'); return; }
    api<Detail>(`/api/admin/catalog/${target.entity}/${encodeURIComponent(target.id)}`, { headers })
      .then((x) => {
        setD(x);
        setDraft(Object.fromEntries(x.editable.map((k) => [k, Array.isArray(x.record[k]) ? x.record[k].join(', ') : x.record[k] ?? ''])));
        setAnn(x.ann || { status: '', tags: [], note: '', updatedAt: '' });
        if (!x.editable.length) setTab('review');
      })
      .catch((e) => setErr(e.message));
  }, [target, headers]);

  const dirty = d ? d.editable.some((k) => String(draft[k] ?? '') !== String(Array.isArray(d.record[k]) ? d.record[k].join(', ') : d.record[k] ?? '')) : false;

  const saveFields = async () => {
    if (!d || !dirty) return;
    setBusy(true);
    try {
      const patch = Object.fromEntries(d.editable.filter((k) => String(draft[k] ?? '') !== String(Array.isArray(d.record[k]) ? d.record[k].join(', ') : d.record[k] ?? '')).map((k) => [k, draft[k]]));
      const r = await api<{ record: any; note: string }>(`/api/admin/catalog/${target.entity}/${encodeURIComponent(target.id)}`, { method: 'PUT', headers, body: JSON.stringify({ patch }) });
      setD({ ...d, record: { ...d.record, ...r.record } });
      toast.success('Kaydedildi', r.note);
      onSaved();
    } catch (e: any) {
      toast.error('Kaydedilemedi', e.message);
    } finally {
      setBusy(false);
    }
  };
  const saveReview = async () => {
    setBusy(true);
    try {
      await annotate([target.id], { status: ann.status, tags: ann.tags, note: ann.note }, target.entity);
      toast.success('Değerlendirme kaydedildi');
    } catch (e: any) {
      toast.error('Kaydedilemedi', e.message);
    } finally {
      setBusy(false);
    }
  };

  const relGroups = useMemo(() => {
    const m = new Map<string, Rel[]>();
    for (const r of d?.relations || []) m.set(r.entity, [...(m.get(r.entity) || []), r]);
    return Array.from(m);
  }, [d]);
  const labelOf = (id: string) => entities.find((e) => e.id === id)?.label || id;
  const long = (k: string) => /stem|definition|description|explanation|back|front|note|clinicalPearl|metin|soru/i.test(k);

  return (
    <Drawer
      open
      onClose={onClose}
      wide
      title={d?.title || (err ? 'Kayıt' : 'Yükleniyor…')}
      label={ent ? `${ent.label} · ${target.id}` : target.id}
      head={
        <>
          <DetailNav list={nav} current={nav.find((x) => x.id === target.id) || null} same={(a, b) => a.id === b.id} onGo={(it) => onNavigate({ entity: target.entity, id: it.id })} />
          {d?.form && (
            <button type="button" className="m14-btn" onClick={() => onDuplicate({ id: d.id, title: d.title, form: d.form! })} title="Bu kaydın kopyasını düzenleyip ekle"><Copy aria-hidden /> Çoğalt</button>
          )}
        </>
      }
      foot={
        tab === 'fields' && d?.editable.length ? (
          <div className="ct-foot">
            <span>{dirty ? 'Kaydedilmemiş değişiklik var' : 'Değişiklik yok'}</span>
            <button type="button" className="m14-btn primary" disabled={!dirty || busy} onClick={() => void saveFields()}><Save aria-hidden /> {busy ? 'Kaydediliyor…' : 'Kaydet'}</button>
          </div>
        ) : tab === 'review' ? (
          <div className="ct-foot">
            <span>{ann.updatedAt ? `Son: ${new Date(ann.updatedAt).toLocaleString('tr-TR')}${ann.by ? ` · ${ann.by}` : ''}` : 'Henüz değerlendirilmedi'}</span>
            <button type="button" className="m14-btn primary" disabled={busy} onClick={() => void saveReview()}><Save aria-hidden /> {busy ? 'Kaydediliyor…' : 'Değerlendirmeyi kaydet'}</button>
          </div>
        ) : undefined
      }
    >
      <p className="ct-sub-line">{ent ? `${ent.label} · ` : ''}<code className="ct-code">{target.id}</code></p>
      {err && <div className="ui-callout is-warn"><CircleAlert /> {err}</div>}
      {!d && !err && <div className="flex flex-col gap-2 p-1">{[80, 60, 70].map((w) => <span key={w} className="ui-skel" style={{ height: 14, width: `${w}%` }} />)}</div>}
      {d && (
        <div className="ct-detail">
          {d.site?.status === 'merged' && (
            <div className="ui-callout is-warn">
              <CircleAlert />
              <span>
                Bu soru sitede gösterilmiyor: kopya olarak <b>#{d.site.shownId}</b> ile birleştirilmiş, sitede o kayıt görünüyor.
                Kök, cevap, açıklama, konu, ders ve kurul düzeltmeleri gruptaki tüm kopyalara yazılır.{' '}
                <button type="button" className="ui-btn is-sm" onClick={() => onNavigate({ entity: 'past', id: d.site!.shownId! })}><ArrowUpRight /> Sitedeki kaydı aç</button>
              </span>
            </div>
          )}
          {d.site?.status === 'hidden' && (
            <div className="ui-callout is-warn"><CircleAlert /> Bu soru sitede gösterilmiyor (karantinada ya da yayından kaldırılmış).</div>
          )}
          <Tabs14<'fields' | 'review' | 'rel' | 'raw'>
            label="Kayıt görünümü"
            value={tab}
            onChange={setTab}
            options={[
              ...(d.editable.length > 0 ? [{ id: 'fields' as const, label: 'Alanlar' }] : []),
              { id: 'review' as const, label: 'Değerlendirme' },
              { id: 'rel' as const, label: 'İlişkiler', n: d.relations.length || undefined },
              { id: 'raw' as const, label: 'Veri' },
            ]}
          />

          {tab === 'fields' && (
            <div className="ct-fields" key="f">
              {d.editable.map((k) => (
                <div key={k} className="ui-field">
                  <label htmlFor={`ct-${k}`}>{FIELD_LABELS[k] || k}{ent?.arrays.includes(k) ? ' (virgülle ayır)' : ''}</label>
                  {long(k) ? (
                    <textarea id={`ct-${k}`} className="ui-input ct-ta" rows={k === 'stem' || k === 'definition' ? 5 : 3} value={draft[k] ?? ''} onChange={(e) => setDraft((x) => ({ ...x, [k]: e.target.value }))} />
                  ) : (
                    <input id={`ct-${k}`} className="ui-input" value={draft[k] ?? ''} onChange={(e) => setDraft((x) => ({ ...x, [k]: e.target.value }))} />
                  )}
                </div>
              ))}
              <p className="ui-hint">Sunucu yalnız bu alanları yazar ve önce yedek alır. Kaydedince değişiklik sitede hemen görünür.</p>
            </div>
          )}

          {tab === 'review' && (
            <div className="ct-fields" key="r">
              <div className="ui-field">
                <label>Durum</label>
                <div className="ct-status is-big" role="radiogroup" aria-label="Durum">
                  {STATUS.map((s) => {
                    const id = s.id === 'yok' ? '' : s.id;
                    return (
                      <button key={s.id} type="button" role="radio" aria-checked={ann.status === id} className={`${s.tone} ${ann.status === id ? 'is-on' : ''}`} onClick={() => setAnn((a) => ({ ...a, status: id as Status }))}>
                        <s.icon aria-hidden /> {s.label}
                      </button>
                    );
                  })}
                </div>
              </div>
              <div className="ui-field">
                <label>Etiketler (sınıflandırma)</label>
                <TagInput label="Etiketler" value={ann.tags} onChange={(tags) => setAnn((a) => ({ ...a, tags }))} suggestions={['tekrar', 'kaynak-eksik', 'cevap-şüpheli', 'yazım', 'güncel', 'öncelikli', 'kopya']} />
              </div>
              <div className="ui-field">
                <label htmlFor="ct-note">Not</label>
                <textarea id="ct-note" className="ui-input ct-ta" rows={4} value={ann.note} onChange={(e) => setAnn((a) => ({ ...a, note: e.target.value }))} placeholder="Neden bu durumda? Ne yapılmalı?" />
              </div>
            </div>
          )}

          {tab === 'rel' && (
            <div className="ct-rels" key="l">
              {!relGroups.length && <EmptyState title="İlişki bulunamadı">Bu kayıt için otomatik bağlantı yok.</EmptyState>}
              {relGroups.map(([e, rels]) => (
                <section key={e} className="ui-section">
                  <div className="ui-section-h"><h2>{labelOf(e)} · {rels.length}</h2></div>
                  <div className="ui-group">
                    {rels.map((r) => (
                      <button key={`${r.entity}:${r.id}`} type="button" className="ui-row has-icon" onClick={() => onNavigate({ entity: r.entity, id: r.id })}>
                        <span className="ui-ico is-soft"><Link2 /></span>
                        <span className="ui-row-main"><b>{r.title}</b><span>{r.why}</span></span>
                        <span className="ui-row-end"><ArrowUpRight className="w-4 h-4" /></span>
                      </button>
                    ))}
                  </div>
                </section>
              ))}
            </div>
          )}

          {tab === 'raw' && (
            <div className="ct-fields" key="j">
              <Seg value={rawView} onChange={setRawView} label="Veri görünümü" options={[{ id: 'gorsel' as const, label: 'Görsel' }, { id: 'ham' as const, label: 'Ham JSON' }]} />
              {rawView === 'gorsel' ? <JsonView value={d.record} /> : <pre className="ct-raw">{JSON.stringify(d.record, null, 2)}</pre>}
            </div>
          )}
        </div>
      )}
    </Drawer>
  );
};

/** Şablonlu yeni kayıt / çoğaltma formu. Alanlar ve seçenekler sunucudaki şablondan gelir (dataCatalogService CREATE). */
const CatalogCreate: React.FC<{
  target: CreateTarget;
  entity?: EntityInfo;
  headers: Record<string, string>;
  onClose: () => void;
  onCreated: (id: string) => void;
}> = ({ target, entity, headers, onClose, onCreated }) => {
  const [fields, setFields] = useState<FormField[] | null>(null);
  const [values, setValues] = useState<Record<string, any>>(() => ({ ...(target.base?.form || {}) }));
  const [err, setErr] = useState('');
  const [busy, setBusy] = useState(false);
  const isDup = !!target.base;

  useEffect(() => {
    api<{ fields: FormField[] }>(`/api/admin/catalog/${target.entity}/template`, { headers })
      .then((x) => setFields(x.fields))
      .catch((e) => setErr(e.message));
  }, [target.entity, headers]);

  const set = (k: string, v: string) => { setValues((x) => ({ ...x, [k]: v })); setErr(''); };
  const setOpt = (k: string, v: string) => { setValues((x) => ({ ...x, options: { ...(x.options || {}), [k]: v } })); setErr(''); };
  const missing = (fields || []).filter((f) => f.required && f.kind !== 'options' && !String(values[f.key] ?? '').trim()).map((f) => f.label);

  const submit = async () => {
    if (busy || !fields) return;
    if (missing.length) { setErr(`Zorunlu alanlar boş: ${missing.join(', ')}`); return; }
    setBusy(true);
    try {
      const r = isDup
        ? await api<{ id: string; note: string }>(`/api/admin/catalog/${target.entity}/duplicate`, { method: 'POST', headers, body: JSON.stringify({ id: target.base!.id, values }) })
        : await api<{ id: string; note: string }>(`/api/admin/catalog/${target.entity}`, { method: 'POST', headers, body: JSON.stringify({ values }) });
      toast.success(isDup ? 'Kopya oluşturuldu' : 'Kayıt eklendi', r.note);
      onCreated(r.id);
    } catch (e: any) {
      setErr(e.message);
    } finally {
      setBusy(false);
    }
  };

  const field = (f: FormField) => {
    const id = `ctn-${f.key}`;
    const hint = f.hint ? <p className="ui-hint">{f.hint}</p> : null;
    const v = values[f.key] ?? '';
    if (f.kind === 'options') {
      return (
        <div key={f.key} className="ui-field">
          <label>{f.label}{f.required ? ' *' : ''}</label>
          <div className="ct-opts">
            {OPTION_KEYS.map((k) => (
              <div key={k} className="ct-opt">
                <b aria-hidden>{k}</b>
                <input className="ui-input" value={values.options?.[k] ?? ''} onChange={(e) => setOpt(k, e.target.value)} aria-label={`${k} şıkkı`} placeholder={k === 'A' || k === 'B' ? 'Şık metni' : 'İsteğe bağlı'} />
              </div>
            ))}
          </div>
          {hint}
        </div>
      );
    }
    const label = <label htmlFor={id}>{f.label}{f.required ? ' *' : ''}{f.kind === 'list' ? ' (virgülle ayır)' : ''}</label>;
    if (f.kind === 'choice' && !f.free) {
      return (
        <div key={f.key} className="ui-field">
          {label}
          <select id={id} className="ui-input" value={v} onChange={(e) => set(f.key, e.target.value)}>
            <option value="">Seçin…</option>
            {(f.choices || []).map((c) => <option key={c} value={c}>{c}</option>)}
          </select>
          {hint}
        </div>
      );
    }
    return (
      <div key={f.key} className="ui-field">
        {label}
        {f.kind === 'long' ? (
          <textarea id={id} className="ui-input ct-ta" rows={['stem', 'definition', 'front'].includes(f.key) ? 5 : 3} value={v} onChange={(e) => set(f.key, e.target.value)} />
        ) : (
          <input id={id} className="ui-input" type={f.kind === 'number' ? 'number' : 'text'} value={v} onChange={(e) => set(f.key, e.target.value)} list={f.kind === 'choice' ? `${id}-dl` : undefined} autoComplete="off" />
        )}
        {f.kind === 'choice' && <datalist id={`${id}-dl`}>{(f.choices || []).map((c) => <option key={c} value={c} />)}</datalist>}
        {hint}
      </div>
    );
  };

  return (
    <Drawer
      open
      onClose={onClose}
      wide
      title={isDup ? 'Kaydı çoğalt' : `Yeni kayıt · ${entity?.label || target.entity}`}
      foot={
        <div className="ct-foot">
          <span>{isDup ? 'Kopya yeni kimlikle aslının arkasına eklenir.' : 'Kimlik otomatik verilir; kayıt bu türün şablonuyla kurulur.'}</span>
          <div className="ct-foot-act">
            <button type="button" className="m14-btn" onClick={onClose}>Vazgeç</button>
            <button type="button" className="m14-btn primary" disabled={busy || !fields} onClick={() => void submit()}>
              {isDup ? <><Copy aria-hidden /> Kopyayı oluştur</> : <><Plus aria-hidden /> Ekle</>}
            </button>
          </div>
        </div>
      }
    >
      {(isDup || entity) && <p className="ct-sub-line">{isDup ? `Asıl: ${target.base!.title}` : `Kaynak: ${entity!.source}`}</p>}
      <form className="ct-fields" onSubmit={(e) => { e.preventDefault(); void submit(); }}>
        {err && <div className="ui-callout is-bad"><CircleAlert /> {err}</div>}
        {!fields && !err && [80, 60, 70].map((w) => <span key={w} className="ui-skel" style={{ height: 14, width: `${w}%` }} />)}
        {fields?.map(field)}
        {isDup && <p className="ui-hint">Formda görünmeyen alanlar (kaynak, kanıt, kazanım vb.) asıl kayıttan aynen kopyalanır; oy, beğeni ve bildirimler sıfırlanır.</p>}
      </form>
    </Drawer>
  );
};
