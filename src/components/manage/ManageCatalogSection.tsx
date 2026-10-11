import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { ArrowUpRight, CheckCircle2, ChevronLeft, ChevronRight, CircleAlert, CircleDashed, Download, Eye, Link2, Save, Tag, X } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { toast } from '../ui/Toast';
import { Sheet } from '../ui/Sheet';
import { TagInput } from '../ui/TagInput';
import { SearchBox, EmptyState } from './consoleUi';
import './catalog.css';

/**
 * Veri kataloğu: uygulamadaki her veri türü tek ekranda.
 *  - Tür seç → ara, sınıflara göre süz (kurul, ders, tür…), sırala, sayfala.
 *  - Her kayıt ayrı DEĞERLENDİRİLİR (Onaylı / İncelemede / Sorunlu) ve ETİKETLENİR; toplu da yapılabilir.
 *    Bu katman kaynak veriyi değiştirmez (sunucuda data/catalog_annotations.json).
 *  - Kayıt sayfası: düzenlenebilir alanlar (sunucu yalnız izinli alanları yazar, yedek alır), ilişkiler
 *    (deste ↔ kazanım ↔ örnek soru ↔ çıkmış ↔ terim ↔ hastalık; dokununca o kayda gider), ham JSON.
 * Uçlar: src/services/dataCatalogService.ts
 */
type Status = '' | 'onayli' | 'inceleme' | 'sorunlu';
interface Ann { status: Status; tags: string[]; note: string; updatedAt: string; by?: string }
interface EntityInfo { id: string; label: string; group: string; source: string; editable: string[]; arrays: string[]; facets: { key: string; label: string }[]; count: number; reviewed: Record<string, number> }
interface Item { id: string; title: string; subtitle: string; ann: Ann | null }
interface ListResp { total: number; page: number; size: number; items: Item[]; facets: Record<string, { value: string; n: number }[]> }
interface Rel { entity: string; id: string; title: string; why: string }
interface Detail { id: string; title: string; record: Record<string, any>; relations: Rel[]; ann: Ann | null; editable: string[] }

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
  const [sel, setSel] = useState<Set<string>>(new Set());
  const [open, setOpen] = useState<{ entity: string; id: string } | null>(null);
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
    setSel(new Set());
  }, [entity]);
  useEffect(() => { setPage(0); setSel(new Set()); }, [debQ, filters, sort]);

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
      setSel(new Set());
    } catch (e: any) {
      toast.error('Güncellenemedi', e.message);
    }
  };
  const [bulkTag, setBulkTag] = useState('');

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
  const allOnPage = !!list?.items.length && list.items.every((i) => sel.has(i.id));

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
        <header className="ct-head">
          <div className="min-w-0">
            <h2>{info?.label || 'Veri kataloğu'}</h2>
            <p>
              {info ? <>Kaynak: <code>{info.source}</code> · {info.editable.length ? 'düzenlenebilir alanlar var' : 'salt okunur (değerlendirme açık)'}</> : 'Yükleniyor…'}
            </p>
          </div>
          <div className="ct-head-act">
            <select className="ct-select" value={sort} onChange={(e) => setSort(e.target.value)} aria-label="Sıralama">
              <option value="">Varsayılan sıra</option>
              <option value="title">Başlığa göre</option>
              <option value="updated">Son güncellenen</option>
            </select>
            <button type="button" className="ui-btn is-sm" onClick={exportCsv} disabled={!list?.items.length} title="Bu sayfayı CSV olarak indir"><Download /> CSV</button>
          </div>
        </header>

        <SearchBox value={q} onChange={setQ} placeholder={`${info?.label || 'Kayıt'} içinde ara…`} count={list ? list.total.toLocaleString('tr-TR') : undefined} />

        {/* Sınıflar */}
        <div className="ct-filters">
          <div className="ct-status" role="radiogroup" aria-label="Değerlendirme durumu">
            <button type="button" role="radio" aria-checked={!filters.status} className={!filters.status ? 'is-on' : ''} onClick={() => setFilters((f) => ({ ...f, status: '' }))}>Tümü</button>
            {STATUS.map((s) => {
              const n = list?.facets.status?.find((x) => x.value === s.id)?.n;
              return (
                <button key={s.id} type="button" role="radio" aria-checked={filters.status === s.id} className={`${s.tone} ${filters.status === s.id ? 'is-on' : ''}`} onClick={() => setFilters((f) => ({ ...f, status: f.status === s.id ? '' : s.id }))}>
                  <s.icon aria-hidden /> {s.label}{n ? <b>{n}</b> : null}
                </button>
              );
            })}
          </div>
          {info?.facets.map((f) => {
            const opts = list?.facets[f.key] || [];
            if (!opts.length && !filters[f.key]) return null;
            return (
              <select key={f.key} className={`ct-select ${filters[f.key] ? 'is-on' : ''}`} value={filters[f.key] || ''} onChange={(e) => setFilters((x) => ({ ...x, [f.key]: e.target.value }))} aria-label={f.label}>
                <option value="">{f.label}: tümü</option>
                {opts.map((o) => <option key={o.value} value={o.value}>{o.value} ({o.n})</option>)}
              </select>
            );
          })}
          {(list?.facets.tag?.length || filters.tag) ? (
            <select className={`ct-select ${filters.tag ? 'is-on' : ''}`} value={filters.tag || ''} onChange={(e) => setFilters((x) => ({ ...x, tag: e.target.value }))} aria-label="Etiket">
              <option value="">Etiket: tümü</option>
              {(list?.facets.tag || []).map((o) => <option key={o.value} value={o.value}>#{o.value} ({o.n})</option>)}
            </select>
          ) : null}
          {Object.values(filters).some(Boolean) && (
            <button type="button" className="ui-btn is-sm is-ghost" onClick={() => setFilters({})}><X /> Süzgeçleri temizle</button>
          )}
        </div>

        {/* Toplu değerlendirme çubuğu */}
        {sel.size > 0 && (
          <div className="ct-bulk" role="toolbar" aria-label="Toplu işlem">
            <b>{sel.size} seçili</b>
            {STATUS.slice(0, 3).map((s) => (
              <button key={s.id} type="button" className={`ui-btn is-sm ${s.id === 'onayli' ? 'is-tonal' : ''}`} onClick={() => void bulk({ status: s.id }, s.label)}><s.icon /> {s.label}</button>
            ))}
            <button type="button" className="ui-btn is-sm is-ghost" onClick={() => void bulk({ status: '' }, 'Değerlendirme kaldırıldı')}>Durumu kaldır</button>
            <form className="ct-bulk-tag" onSubmit={(e) => { e.preventDefault(); if (bulkTag.trim()) { void bulk({ addTags: [bulkTag.trim()] }, 'Etiket eklendi'); setBulkTag(''); } }}>
              <Tag aria-hidden />
              <input value={bulkTag} onChange={(e) => setBulkTag(e.target.value)} placeholder="Etiket ekle" aria-label="Seçililere etiket ekle" />
            </form>
            <button type="button" className="ui-btn is-sm is-ghost" onClick={() => setSel(new Set())} aria-label="Seçimi temizle"><X /></button>
          </div>
        )}

        {err && <div className="ui-callout is-bad"><CircleAlert /> {err}</div>}

        <div className={`ct-list ${loading ? 'is-loading' : ''}`} aria-busy={loading}>
          {list && list.items.length > 0 && (
            <label className="ct-row is-head">
              <input type="checkbox" checked={allOnPage} onChange={() => setSel((s) => { const n = new Set(s); list.items.forEach((i) => (allOnPage ? n.delete(i.id) : n.add(i.id))); return n; })} aria-label="Bu sayfadakilerin tümünü seç" />
              <span>{list.total.toLocaleString('tr-TR')} kayıt · sayfa {page + 1}/{pages}</span>
            </label>
          )}
          {list?.items.map((it, i) => {
            const st = statusMeta(it.ann?.status);
            return (
              <div key={it.id} className={`ct-row ${sel.has(it.id) ? 'is-sel' : ''}`} style={{ animationDelay: `${Math.min(i, 12) * 18}ms` }}>
                <input type="checkbox" checked={sel.has(it.id)} onChange={() => setSel((s) => { const n = new Set(s); n.has(it.id) ? n.delete(it.id) : n.add(it.id); return n; })} aria-label="Seç" />
                <button type="button" className="ct-row-main" onClick={() => setOpen({ entity, id: it.id })}>
                  <b>{it.title || <i>(başlıksız)</i>}</b>
                  <span>{it.subtitle}</span>
                </button>
                <div className="ct-row-end">
                  {(it.ann?.tags || []).slice(0, 3).map((t) => <span key={t} className="ui-tag">#{t}</span>)}
                  {st && it.ann?.status ? <span className={`ui-tag ${st.tone}`}><st.icon className="w-3 h-3" /> {st.label}</span> : null}
                  <ChevronRight className="ct-chev" aria-hidden />
                </div>
              </div>
            );
          })}
          {list && !list.items.length && !loading && <EmptyState title="Kayıt yok">Aramayı ya da süzgeçleri değiştirin.</EmptyState>}
          {!list && loading && Array.from({ length: 6 }, (_, i) => <div key={i} className="ct-row"><span className="ui-skel" style={{ height: 14, width: `${60 + (i % 3) * 12}%` }} /></div>)}
        </div>

        {pages > 1 && (
          <nav className="ct-pager" aria-label="Sayfalar">
            <button type="button" className="ui-btn is-sm" disabled={page === 0} onClick={() => setPage((p) => p - 1)}><ChevronLeft /> Önceki</button>
            <span>{page + 1} / {pages}</span>
            <button type="button" className="ui-btn is-sm" disabled={page >= pages - 1} onClick={() => setPage((p) => p + 1)}>Sonraki <ChevronRight /></button>
          </nav>
        )}
      </div>

      {open && (
        <CatalogDetail
          key={`${open.entity}:${open.id}`}
          target={open}
          entities={entities}
          headers={headers}
          onClose={() => setOpen(null)}
          onNavigate={(t) => setOpen(t)}
          onSaved={() => { load(); loadEntities(); }}
          annotate={annotate}
        />
      )}
    </div>
  );
};

const CatalogDetail: React.FC<{
  target: { entity: string; id: string };
  entities: EntityInfo[];
  headers: Record<string, string>;
  onClose: () => void;
  onNavigate: (t: { entity: string; id: string }) => void;
  onSaved: () => void;
  annotate: (ids: string[], body: Record<string, unknown>, ent?: string) => Promise<void>;
}> = ({ target, entities, headers, onClose, onNavigate, onSaved, annotate }) => {
  const [d, setD] = useState<Detail | null>(null);
  const [err, setErr] = useState('');
  const [tab, setTab] = useState<'fields' | 'review' | 'rel' | 'raw'>('fields');
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
    <Sheet
      open
      onClose={onClose}
      size="full"
      width={760}
      title={d?.title || (err ? 'Kayıt' : 'Yükleniyor…')}
      subtitle={ent ? `${ent.label} · ${target.id}` : target.id}
      footer={
        tab === 'fields' && d?.editable.length ? (
          <div className="ct-foot">
            <span>{dirty ? 'Kaydedilmemiş değişiklik var' : 'Değişiklik yok'}</span>
            <button type="button" className={`ui-btn is-primary ${busy ? 'is-loading' : ''}`} disabled={!dirty || busy} onClick={() => void saveFields()}><Save /> Kaydet</button>
          </div>
        ) : tab === 'review' ? (
          <div className="ct-foot">
            <span>{ann.updatedAt ? `Son: ${new Date(ann.updatedAt).toLocaleString('tr-TR')}${ann.by ? ` · ${ann.by}` : ''}` : 'Henüz değerlendirilmedi'}</span>
            <button type="button" className={`ui-btn is-primary ${busy ? 'is-loading' : ''}`} disabled={busy} onClick={() => void saveReview()}><Save /> Değerlendirmeyi kaydet</button>
          </div>
        ) : undefined
      }
    >
      {err && <div className="ui-callout is-warn"><CircleAlert /> {err}</div>}
      {!d && !err && <div className="flex flex-col gap-2 p-1">{[80, 60, 70].map((w) => <span key={w} className="ui-skel" style={{ height: 14, width: `${w}%` }} />)}</div>}
      {d && (
        <div className="ct-detail">
          <div className="ui-seg ct-tabs" role="tablist">
            {d.editable.length > 0 && <button type="button" role="tab" aria-checked={tab === 'fields'} aria-selected={tab === 'fields'} onClick={() => setTab('fields')}>Alanlar</button>}
            <button type="button" role="tab" aria-checked={tab === 'review'} aria-selected={tab === 'review'} onClick={() => setTab('review')}>Değerlendirme</button>
            <button type="button" role="tab" aria-checked={tab === 'rel'} aria-selected={tab === 'rel'} onClick={() => setTab('rel')}>İlişkiler{d.relations.length ? ` (${d.relations.length})` : ''}</button>
            <button type="button" role="tab" aria-checked={tab === 'raw'} aria-selected={tab === 'raw'} onClick={() => setTab('raw')}>Ham veri</button>
          </div>

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
              <p className="ui-hint">Sunucu yalnız bu alanları yazar ve önce yedek alır. Uygulama paketine gömülü veriler (src/data) bir sonraki derlemede güncellenir.</p>
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

          {tab === 'raw' && <pre className="ct-raw" key="j">{JSON.stringify(d.record, null, 2)}</pre>}
        </div>
      )}
    </Sheet>
  );
};
