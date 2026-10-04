import React, { useEffect, useMemo, useState } from 'react';
import { Search, ArrowUp, ArrowDown, Columns3, Download, X, Trash2, CheckCircle2, Copy, RefreshCw, ChevronDown } from 'lucide-react';
import { Committee, QuestionItem } from '../../types';
import { ApiService } from '../../services/api';
import { toast } from '../ui/Toast';

/**
 * v3 "Tüm veriler": one sortable table for every dataset the site keeps.
 * Pick a dataset, search, sort by any column, hide columns, select rows for bulk actions,
 * open a row for its details, export CSV. Destructive actions ask once, inline.
 */
type DatasetId = 'questions' | 'past' | 'users' | 'decks' | 'glossary' | 'summaries';
type Row = Record<string, any>;

interface Column {
  key: string;
  label: string;
  width?: string; // CSS grid track
  value: (r: Row) => string | number;
  render?: (r: Row) => React.ReactNode;
  mono?: boolean;
}

interface Dataset {
  id: DatasetId;
  label: string;
  load: () => Promise<Row[]>;
  idOf: (r: Row) => string;
  columns: Column[];
  defaultSort: { key: string; dir: 1 | -1 };
  /** Bulk/row actions that change data (only where the API supports it) */
  canDelete?: boolean;
  canVerify?: boolean;
}

interface Props {
  adminEmail: string;
  questions: QuestionItem[];
  committees: Committee[];
  onRefreshData: () => Promise<void>;
}

const STATUS_TONE: Record<string, string> = {
  completed: 'bg-ok-soft text-ok',
  gathering: 'bg-warn-soft text-warn',
  empty: 'bg-canvas text-ink-2',
};
const STATUS_LABEL: Record<string, string> = { completed: 'Doğrulandı', gathering: 'Taslak', empty: 'Boş' };
const fmtDate = (s?: string) => (s ? new Date(s).toLocaleDateString('tr-TR', { day: '2-digit', month: '2-digit', year: '2-digit' }) : '—');
const stemOf = (q: Row) => q?.reconstruction?.stem || q?.stem || q?.rawQuestion?.stem || q?.fragments?.[0]?.text || q?.topic || '';
const Pill: React.FC<{ cls: string; children: React.ReactNode }> = ({ cls, children }) => (
  <span className={`inline-flex items-center h-5 px-1.5 rounded-full text-[11.5px] font-semibold whitespace-nowrap ${cls}`}>{children}</span>
);

export const ManageDataSection: React.FC<Props> = ({ adminEmail, questions, committees, onRefreshData }) => {
  const committeeName = (id?: string) => {
    const known = committees.find((c) => c.id === id)?.name;
    if (known) return known.replace(/^Dönem 3\s*-\s*/i, '').split(':')[0];
    // "donem2-kurul4" → "D2 Kurul 4", "donem3-final" → "D3 Final"
    const m = (id || '').match(/^donem(\d)-(kurul(\d)|final|butunleme)$/);
    if (!m) return id || '—';
    return `D${m[1]} ${m[3] ? `Kurul ${m[3]}` : m[2] === 'final' ? 'Final' : 'Bütünleme'}`;
  };

  const DATASETS: Dataset[] = useMemo(
    () => [
      {
        id: 'questions',
        label: 'Havuz soruları',
        load: async () => questions as Row[],
        idOf: (r) => r.id,
        canDelete: true,
        canVerify: true,
        defaultSort: { key: 'no', dir: 1 },
        columns: [
          { key: 'no', label: 'No', width: '56px', mono: true, value: (r) => (r.isUnassignedNumber ? 9999 : r.questionNumber || 0), render: (r) => (r.isUnassignedNumber ? '?' : r.questionNumber) },
          { key: 'stem', label: 'Soru', width: 'minmax(0,1fr)', value: (r) => stemOf(r) },
          { key: 'discipline', label: 'Ders', width: '140px', value: (r) => r.discipline || '' },
          { key: 'status', label: 'Durum', width: '100px', value: (r) => r.status || '', render: (r) => <Pill cls={STATUS_TONE[r.status] || STATUS_TONE.empty}>{STATUS_LABEL[r.status] || r.status || '—'}</Pill> },
          { key: 'fragments', label: 'Parça', width: '60px', mono: true, value: (r) => r.fragments?.length || 0 },
          { key: 'options', label: 'Şık', width: '50px', mono: true, value: (r) => r.options?.length || 0 },
          { key: 'upvotes', label: 'Beğeni', width: '64px', mono: true, value: (r) => r.upvotes || 0 },
          { key: 'updatedAt', label: 'Güncel', width: '80px', value: (r) => r.updatedAt || '', render: (r) => fmtDate(r.updatedAt) },
        ],
      },
      {
        id: 'past',
        label: 'Çıkmış sorular',
        load: async () => (await ApiService.getPastQuestions({ includeAmbiguous: true })) as Row[],
        idOf: (r) => String(r.id),
        defaultSort: { key: 'year', dir: -1 },
        columns: [
          { key: 'no', label: 'No', width: '56px', mono: true, value: (r) => r.questionNumber || 0 },
          { key: 'stem', label: 'Soru', width: 'minmax(0,1fr)', value: (r) => stemOf(r) },
          { key: 'discipline', label: 'Ders', width: '140px', value: (r) => r.discipline || '' },
          { key: 'committee', label: 'Kurul', width: '110px', value: (r) => committeeName(r.committeeId) },
          { key: 'year', label: 'Yıl', width: '90px', value: (r) => r.examYear || '' },
          { key: 'state', label: 'Durum', width: '100px', value: (r) => (r.isAmbiguous ? 0 : r.reconstruction ? 2 : 1), render: (r) => (r.isAmbiguous ? <Pill cls="bg-warn-soft text-warn">Eksik</Pill> : r.reconstruction ? <Pill cls="bg-ok-soft text-ok">Düzenlendi</Pill> : <Pill cls="bg-canvas text-ink-2">Ham</Pill>) },
          { key: 'answer', label: 'Cevap', width: '60px', mono: true, value: (r) => r.reconstruction?.correctAnswer || r.correctAnswer || r.claimedAnswer || '' },
        ],
      },
      {
        id: 'users',
        label: 'Kullanıcılar',
        load: async () => (await ApiService.adminGetUsers(adminEmail)) as Row[],
        idOf: (r) => r.uid || r.email,
        canDelete: true,
        defaultSort: { key: 'lastLogin', dir: -1 },
        columns: [
          { key: 'name', label: 'Ad', width: 'minmax(0,1fr)', value: (r) => r.displayName || r.email || '' },
          { key: 'email', label: 'E-posta', width: '200px', value: (r) => r.email || '' },
          { key: 'no', label: 'Öğrenci no', width: '120px', mono: true, value: (r) => r.studentNumber || '' },
          { key: 'role', label: 'Rol', width: '90px', value: (r) => r.role || '', render: (r) => <Pill cls={r.role === 'admin' ? 'bg-accent-soft text-accent' : 'bg-canvas text-ink-2'}>{r.role === 'admin' ? 'Yönetici' : 'Öğrenci'}</Pill> },
          { key: 'created', label: 'Kayıt', width: '80px', value: (r) => r.createdAt || '', render: (r) => fmtDate(r.createdAt) },
          { key: 'lastLogin', label: 'Son giriş', width: '84px', value: (r) => r.lastLoginAt || '', render: (r) => fmtDate(r.lastLoginAt) },
        ],
      },
      {
        id: 'decks',
        label: 'Dersler',
        load: async () => {
          const mod: any = await import('../../data/interactive_learning_decks.json');
          return ((mod.default || mod) as Row[]).filter((d) => d && Array.isArray(d.slides));
        },
        idOf: (r) => r.id,
        defaultSort: { key: 'title', dir: 1 },
        columns: [
          { key: 'title', label: 'Ders', width: 'minmax(0,1fr)', value: (r) => r.title || '' },
          { key: 'discipline', label: 'Branş', width: '160px', value: (r) => r.discipline || '' },
          { key: 'slides', label: 'Slayt', width: '64px', mono: true, value: (r) => r.slides?.length || 0 },
          { key: 'cards', label: 'Kart', width: '64px', mono: true, value: (r) => (r.slides || []).reduce((n: number, s: Row) => n + (s.flashcards?.length || 0), 0) },
          { key: 'qs', label: 'Soru', width: '64px', mono: true, value: (r) => (r.slides || []).reduce((n: number, s: Row) => n + (s.relatedQuestions?.length || 0), 0) },
          { key: 'instructor', label: 'Hoca', width: '160px', value: (r) => r.instructor || '' },
        ],
      },
      {
        id: 'glossary',
        label: 'Sözlük',
        load: async () => (await import('../../data/glossary')).GLOSSARY as Row[],
        idOf: (r) => r.term,
        defaultSort: { key: 'term', dir: 1 },
        columns: [
          { key: 'term', label: 'Terim', width: '200px', value: (r) => r.term || '' },
          { key: 'category', label: 'Kategori', width: '140px', value: (r) => r.category || '' },
          { key: 'definition', label: 'Tanım', width: 'minmax(0,1fr)', value: (r) => r.definition || '' },
          { key: 'pearl', label: 'Spot', width: '64px', value: (r) => (r.clinicalPearls ? 1 : 0), render: (r) => (r.clinicalPearls ? <Pill cls="bg-ok-soft text-ok">Var</Pill> : <span className="text-ink-3">—</span>) },
        ],
      },
      {
        id: 'summaries',
        label: 'Özetler',
        load: async () => {
          const mod: any = await import('../../data/lectureSummariesCatalog.json');
          const v = mod.default || mod;
          return (Array.isArray(v) ? v : Object.values(v)) as Row[];
        },
        idOf: (r) => r.id,
        defaultSort: { key: 'kurul', dir: 1 },
        columns: [
          { key: 'kurul', label: 'Kurul', width: '64px', mono: true, value: (r) => r.kurul || 0 },
          { key: 'title', label: 'Başlık', width: 'minmax(0,1fr)', value: (r) => r.title || '' },
          { key: 'discipline', label: 'Ders', width: '170px', value: (r) => r.discipline || '' },
          { key: 'points', label: 'Başlık sayısı', width: '100px', mono: true, value: (r) => r.keyPoints?.length || 0 },
          { key: 'file', label: 'Dosya', width: '200px', value: (r) => r.fileName || '' },
        ],
      },
    ],
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [questions, adminEmail, committees]
  );

  const [dsId, setDsId] = useState<DatasetId>('questions');
  const ds = DATASETS.find((d) => d.id === dsId) || DATASETS[0];
  const [rows, setRows] = useState<Row[]>([]);
  const [loading, setLoading] = useState(false);
  const [query, setQuery] = useState('');
  const [sort, setSort] = useState(ds.defaultSort);
  const [hidden, setHidden] = useState<Record<string, boolean>>({});
  const [colMenu, setColMenu] = useState(false);
  const [selected, setSelected] = useState<string[]>([]);
  const [openId, setOpenId] = useState<string | null>(null);
  const [limit, setLimit] = useState(100);
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [busy, setBusy] = useState(false);

  const load = async () => {
    setLoading(true);
    try {
      setRows(await ds.load());
    } catch (e: any) {
      setRows([]);
      toast.error(`${ds.label} yüklenemedi`, e?.message || 'Sunucuya ulaşılamadı.');
    } finally {
      setLoading(false);
    }
  };

  // Switching dataset resets view state
  useEffect(() => {
    setSort(ds.defaultSort);
    setHidden({});
    setSelected([]);
    setOpenId(null);
    setQuery('');
    setLimit(100);
    setConfirmDelete(false);
    void load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [dsId]);
  // Pool questions come from props; keep in sync
  useEffect(() => {
    if (dsId === 'questions') setRows(questions as Row[]);
  }, [questions, dsId]);
  useEffect(() => {
    if (!confirmDelete) return;
    const t = window.setTimeout(() => setConfirmDelete(false), 4000);
    return () => window.clearTimeout(t);
  }, [confirmDelete]);

  const cols = ds.columns.filter((c) => !hidden[c.key]);
  const grid = `28px ${cols.map((c) => c.width || '1fr').join(' ')}`;

  const visible = useMemo(() => {
    const q = query.trim().toLocaleLowerCase('tr-TR');
    const filtered = q
      ? rows.filter((r) => ds.columns.some((c) => String(c.value(r)).toLocaleLowerCase('tr-TR').includes(q)))
      : rows;
    const col = ds.columns.find((c) => c.key === sort.key);
    if (!col) return filtered;
    return [...filtered].sort((a, b) => {
      const x = col.value(a);
      const y = col.value(b);
      const cmp = typeof x === 'number' && typeof y === 'number' ? x - y : String(x).localeCompare(String(y), 'tr', { numeric: true });
      return cmp * sort.dir;
    });
  }, [rows, query, sort, ds]);

  const shown = visible.slice(0, limit);
  const allOnPage = shown.length > 0 && shown.every((r) => selected.includes(ds.idOf(r)));
  const openRow = openId ? rows.find((r) => ds.idOf(r) === openId) : null;

  const toggleSort = (key: string) => setSort((s) => (s.key === key ? { key, dir: s.dir === 1 ? -1 : 1 } : { key, dir: 1 }));
  const toggleRow = (id: string) => setSelected((s) => (s.includes(id) ? s.filter((x) => x !== id) : [...s, id]));

  const exportCsv = (onlySelected: boolean) => {
    const src = onlySelected ? visible.filter((r) => selected.includes(ds.idOf(r))) : visible;
    const esc = (v: any) => `"${String(v ?? '').replace(/"/g, '""').replace(/\s+/g, ' ')}"`;
    const csv = [ds.columns.map((c) => esc(c.label)).join(','), ...src.map((r) => ds.columns.map((c) => esc(c.value(r))).join(','))].join('\n');
    const url = URL.createObjectURL(new Blob(['﻿' + csv], { type: 'text/csv;charset=utf-8' }));
    const a = document.createElement('a');
    a.href = url;
    a.download = `medsoru_${ds.id}_${new Date().toISOString().slice(0, 10)}.csv`;
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 3000);
    toast.success('CSV hazır', `${src.length} satır`);
  };

  const runBulk = async (kind: 'delete' | 'verify', ids: string[]) => {
    setBusy(true);
    let ok = 0;
    try {
      for (const id of ids) {
        try {
          if (kind === 'delete') {
            if (ds.id === 'questions') await ApiService.adminDeleteQuestion(adminEmail, id);
            else if (ds.id === 'users') await ApiService.adminDeleteUser(adminEmail, id);
          } else if (ds.id === 'questions') {
            await ApiService.adminUpdateQuestion(adminEmail, id, { status: 'completed' } as Partial<QuestionItem>);
          }
          ok++;
        } catch {
          /* counted below */
        }
      }
      if (ok) toast.success(kind === 'delete' ? 'Silindi' : 'Doğrulandı', `${ok} kayıt`);
      if (ok < ids.length) toast.error('Bazı kayıtlar işlenemedi', `${ids.length - ok} kayıt değişmedi.`);
      setSelected([]);
      setOpenId(null);
      if (ds.id === 'questions') await onRefreshData();
      else await load();
    } finally {
      setBusy(false);
      setConfirmDelete(false);
    }
  };

  return (
    <div className="flex flex-col gap-3 min-w-0">
      {/* Dataset picker */}
      <div role="tablist" aria-label="Veri kümesi" className="flex gap-1 bg-canvas rounded-xl p-1 overflow-x-auto no-scrollbar self-start max-w-full">
        {DATASETS.map((d) => (
          <button
            key={d.id}
            type="button"
            role="tab"
            aria-selected={dsId === d.id}
            onClick={() => setDsId(d.id)}
            className={`shrink-0 h-8 px-3 rounded-lg text-[13px] whitespace-nowrap cursor-pointer ${
              dsId === d.id ? 'bg-white text-ink font-semibold shadow-xs' : 'text-ink-2 hover:text-ink'
            }`}
          >
            {d.label}
          </button>
        ))}
      </div>

      {/* Toolbar */}
      <div className="flex flex-wrap items-center gap-2">
        <label className="flex-1 min-w-[200px] flex items-center gap-2 h-9 px-3 rounded-[10px] bg-white border border-line focus-within:border-accent">
          <Search className="w-4 h-4 text-ink-3 shrink-0" />
          <span className="sr-only">Tabloda ara</span>
          <input
            type="search"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder={`${ds.label} içinde ara`}
            className="flex-1 min-w-0 bg-transparent border-0 outline-0 text-[14px] placeholder:text-slate-600"
          />
        </label>
        <span className="text-[12.5px] text-ink-3 font-mono">{visible.length.toLocaleString('tr-TR')} kayıt</span>
        <div className="relative">
          <button
            type="button"
            onClick={() => setColMenu((v) => !v)}
            aria-expanded={colMenu}
            className="h-9 px-3 rounded-[10px] border border-line bg-white text-[13px] font-semibold text-ink inline-flex items-center gap-1.5 cursor-pointer"
          >
            <Columns3 className="w-4 h-4" />
            Sütunlar
          </button>
          {colMenu && (
            <div className="absolute right-0 top-10 z-30 w-[200px] bg-white border border-line rounded-xl shadow-lg p-1.5">
              {ds.columns.map((c) => (
                <label key={c.key} className="flex items-center gap-2 h-8 px-2 rounded-lg hover:bg-canvas text-[13px] cursor-pointer">
                  <input
                    type="checkbox"
                    checked={!hidden[c.key]}
                    onChange={() => setHidden((h) => ({ ...h, [c.key]: !h[c.key] }))}
                    className="w-4 h-4 accent-[#2453E6]"
                  />
                  {c.label}
                </label>
              ))}
            </div>
          )}
        </div>
        <button type="button" onClick={() => exportCsv(false)} className="h-9 px-3 rounded-[10px] border border-line bg-white text-[13px] font-semibold text-ink inline-flex items-center gap-1.5 cursor-pointer">
          <Download className="w-4 h-4" />
          CSV
        </button>
        <button type="button" onClick={() => void load()} aria-label="Yenile" className="w-9 h-9 rounded-[10px] border border-line bg-white text-ink-2 inline-flex items-center justify-center cursor-pointer">
          <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
        </button>
      </div>

      {/* Bulk bar */}
      {selected.length > 0 && (
        <div className="flex flex-wrap items-center gap-2 bg-ink text-white rounded-xl pl-3.5 pr-2 py-1.5">
          <b className="text-[13px]">{selected.length} seçili</b>
          <span className="flex-1" />
          <button type="button" onClick={() => exportCsv(true)} className="h-8 px-2.5 rounded-lg border border-white/25 text-[12.5px] font-semibold inline-flex items-center gap-1.5 cursor-pointer">
            <Download className="w-3.5 h-3.5" />
            CSV
          </button>
          {ds.canVerify && (
            <button type="button" disabled={busy} onClick={() => void runBulk('verify', selected)} className="h-8 px-2.5 rounded-lg border border-white/25 text-[12.5px] font-semibold inline-flex items-center gap-1.5 cursor-pointer disabled:opacity-50">
              <CheckCircle2 className="w-3.5 h-3.5" />
              Doğrula
            </button>
          )}
          {ds.canDelete && (
            <button
              type="button"
              disabled={busy}
              onClick={() => (confirmDelete ? void runBulk('delete', selected) : setConfirmDelete(true))}
              className="h-8 px-2.5 rounded-lg bg-bad text-white text-[12.5px] font-semibold inline-flex items-center gap-1.5 cursor-pointer disabled:opacity-50"
            >
              <Trash2 className="w-3.5 h-3.5" />
              {confirmDelete ? `Emin misin? ${selected.length} kaydı sil` : 'Sil'}
            </button>
          )}
          <button type="button" onClick={() => setSelected([])} aria-label="Seçimi temizle" className="w-8 h-8 rounded-lg inline-flex items-center justify-center cursor-pointer">
            <X className="w-4 h-4" />
          </button>
        </div>
      )}

      <div className="flex gap-3 min-w-0 items-start">
        {/* Table */}
        <div className="flex-1 min-w-0 bg-white border border-line rounded-xl overflow-x-auto">
          <div className="w-full min-w-[760px]">
            <div className="grid items-center gap-x-3 h-9 px-3 border-b border-line bg-field text-[12px] font-semibold text-ink-3 sticky top-0" style={{ gridTemplateColumns: grid }}>
              <input
                type="checkbox"
                aria-label="Bu sayfadakilerin hepsini seç"
                checked={allOnPage}
                onChange={() => setSelected((s) => (allOnPage ? s.filter((id) => !shown.some((r) => ds.idOf(r) === id)) : Array.from(new Set([...s, ...shown.map(ds.idOf)]))))}
                className="w-4 h-4 accent-[#2453E6]"
              />
              {cols.map((c) => (
                <button key={c.key} type="button" onClick={() => toggleSort(c.key)} className="text-left inline-flex items-center gap-1 cursor-pointer hover:text-ink whitespace-nowrap" aria-sort={sort.key === c.key ? (sort.dir === 1 ? 'ascending' : 'descending') : undefined}>
                  {c.label}
                  {sort.key === c.key && (sort.dir === 1 ? <ArrowUp className="w-3 h-3" /> : <ArrowDown className="w-3 h-3" />)}
                </button>
              ))}
            </div>
            {loading && rows.length === 0 ? (
              <p className="m-0 px-4 py-10 text-center text-[14px] text-ink-3">Yükleniyor…</p>
            ) : shown.length === 0 ? (
              <p className="m-0 px-4 py-10 text-center text-[14px] text-ink-3">Kayıt yok.</p>
            ) : (
              shown.map((r) => {
                const id = ds.idOf(r);
                const sel = selected.includes(id);
                const open = openId === id;
                return (
                  <div
                    key={id}
                    onClick={() => setOpenId(open ? null : id)}
                    className={`grid items-center gap-x-3 min-h-10 px-3 py-1.5 border-b border-line-soft text-[13.5px] cursor-pointer ${sel ? 'bg-accent-soft' : open ? 'bg-canvas' : 'hover:bg-field'}`}
                    style={{ gridTemplateColumns: grid }}
                  >
                    <input
                      type="checkbox"
                      checked={sel}
                      onClick={(e) => e.stopPropagation()}
                      onChange={() => toggleRow(id)}
                      aria-label="Satırı seç"
                      className="w-4 h-4 accent-[#2453E6]"
                    />
                    {cols.map((c) => (
                      <span key={c.key} className={`min-w-0 truncate ${c.mono ? 'font-mono' : ''}`} title={String(c.value(r))}>
                        {c.render ? c.render(r) : c.value(r) || '—'}
                      </span>
                    ))}
                  </div>
                );
              })
            )}
            {visible.length > limit && (
              <button type="button" onClick={() => setLimit((n) => n + 200)} className="w-full h-10 text-[13px] font-semibold text-accent cursor-pointer inline-flex items-center justify-center gap-1">
                <ChevronDown className="w-4 h-4" />
                {(visible.length - limit).toLocaleString('tr-TR')} kayıt daha
              </button>
            )}
          </div>
        </div>

        {/* Detail panel */}
        {openRow && (
          <button type="button" aria-label="Paneli kapat" onClick={() => setOpenId(null)} className="ms-fade-in lg:hidden fixed inset-0 z-40 bg-[rgba(14,26,38,0.35)] cursor-default" />
        )}
        {openRow && (
          <aside
            role="dialog"
            aria-label="Kayıt ayrıntısı"
            onKeyDown={(e) => e.key === 'Escape' && setOpenId(null)}
            className="ms-slide-left lg:animate-none fixed lg:sticky z-50 lg:z-auto top-0 right-0 bottom-0 w-[min(420px,92vw)] lg:w-[320px] shrink-0 flex flex-col bg-white border-l lg:border border-line lg:rounded-xl overflow-hidden lg:max-h-[calc(100dvh-220px)] shadow-lg lg:shadow-none"
          >
            <div className="flex items-center gap-2 px-3.5 py-3 border-b border-line">
              <span className="text-[14px] font-semibold flex-1 truncate">{String(ds.columns[0].value(openRow)) || 'Kayıt'}</span>
              <button type="button" onClick={() => setOpenId(null)} aria-label="Kapat" className="w-8 h-8 rounded-full inline-flex items-center justify-center text-ink-2 hover:bg-canvas cursor-pointer">
                <X className="w-4 h-4" />
              </button>
            </div>
            <div className="flex-1 overflow-y-auto px-3.5 py-3 flex flex-col gap-2">
              {ds.columns.map((c) => (
                <div key={c.key} className="flex flex-col gap-0.5">
                  <span className="text-[11.5px] font-semibold uppercase tracking-[0.06em] text-ink-3">{c.label}</span>
                  <span className={`text-[13.5px] text-ink break-words ${c.mono ? 'font-mono' : ''}`}>{c.render ? c.render(openRow) : String(c.value(openRow) || '—')}</span>
                </div>
              ))}
            </div>
            <div className="flex flex-wrap gap-1.5 px-3.5 py-3 border-t border-line">
              <button
                type="button"
                onClick={() => {
                  navigator.clipboard?.writeText(JSON.stringify(openRow, null, 2)).then(
                    () => toast.success('Kopyalandı', 'Kaydın tamamı JSON olarak panoda'),
                    () => toast.error('Kopyalanamadı')
                  );
                }}
                className="h-8 px-2.5 rounded-lg border border-line text-[12.5px] font-semibold inline-flex items-center gap-1.5 cursor-pointer"
              >
                <Copy className="w-3.5 h-3.5" />
                JSON
              </button>
              {ds.canVerify && openRow.status !== 'completed' && (
                <button type="button" disabled={busy} onClick={() => void runBulk('verify', [ds.idOf(openRow)])} className="h-8 px-2.5 rounded-lg border border-line text-[12.5px] font-semibold inline-flex items-center gap-1.5 cursor-pointer disabled:opacity-50">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  Doğrula
                </button>
              )}
              {ds.canDelete && (
                <button
                  type="button"
                  disabled={busy}
                  onClick={() => {
                    setSelected([ds.idOf(openRow)]);
                    setConfirmDelete(true);
                  }}
                  className="h-8 px-2.5 rounded-lg bg-bad-soft text-bad-text text-[12.5px] font-semibold inline-flex items-center gap-1.5 cursor-pointer disabled:opacity-50"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                  Sil…
                </button>
              )}
            </div>
          </aside>
        )}
      </div>
    </div>
  );
};
