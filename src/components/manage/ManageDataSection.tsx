import React, { useEffect, useMemo, useState } from 'react';
import { Search, ArrowUp, ArrowDown, Columns3, Download, X, Trash2, CheckCircle2, Copy, RefreshCw, ChevronDown } from 'lucide-react';
import { Committee, QuestionItem } from '../../types';
import { ApiService } from '../../services/api';
import { toast } from '../ui/Toast';
import { Seg, SearchBox, EmptyState, ConfirmButton, Drawer } from './consoleUi';

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

const STATUS_TONE: Record<string, string> = { completed: 'is-ok', gathering: 'is-warn', empty: '' };
const STATUS_LABEL: Record<string, string> = { completed: 'Doğrulandı', gathering: 'Taslak', empty: 'Boş' };
const fmtDate = (s?: string) => (s ? new Date(s).toLocaleDateString('tr-TR', { day: '2-digit', month: '2-digit', year: '2-digit' }) : '—');
const stemOf = (q: Row) => q?.reconstruction?.stem || q?.stem || q?.rawQuestion?.stem || q?.fragments?.[0]?.text || q?.topic || '';
const Pill: React.FC<{ cls: string; children: React.ReactNode }> = ({ cls, children }) => <span className={`ms-tag ${cls}`}>{children}</span>;

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
          { key: 'state', label: 'Durum', width: '100px', value: (r) => (r.isAmbiguous ? 0 : r.reconstruction ? 2 : 1), render: (r) => (r.isAmbiguous ? <Pill cls="is-warn">Eksik</Pill> : r.reconstruction ? <Pill cls="is-ok">Düzenlendi</Pill> : <Pill cls="">Ham</Pill>) },
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
          { key: 'role', label: 'Rol', width: '90px', value: (r) => r.role || '', render: (r) => <Pill cls={r.role === 'admin' ? 'is-accent' : ''}>{r.role === 'admin' ? 'Yönetici' : 'Öğrenci'}</Pill> },
          { key: 'created', label: 'Kayıt', width: '80px', value: (r) => r.createdAt || '', render: (r) => fmtDate(r.createdAt) },
          { key: 'lastLogin', label: 'Son giriş', width: '84px', value: (r) => r.lastLoginAt || '', render: (r) => fmtDate(r.lastLoginAt) },
        ],
      },
      {
        id: 'decks',
        label: 'Dersler',
        load: async () => {
          // Tablo yalnızca özet bilgileri gösterir: hafif katalog yeterli
          const { DECK_CATALOG } = await import('../../data/deckStore');
          return DECK_CATALOG as unknown as Row[];
        },
        idOf: (r) => r.id,
        defaultSort: { key: 'title', dir: 1 },
        columns: [
          { key: 'title', label: 'Ders', width: 'minmax(0,1fr)', value: (r) => r.title || '' },
          { key: 'discipline', label: 'Branş', width: '160px', value: (r) => r.discipline || '' },
          { key: 'slides', label: 'Slayt', width: '64px', mono: true, value: (r) => r.slideCount || 0 },
          { key: 'cards', label: 'Kart', width: '64px', mono: true, value: (r) => r.cardCount || 0 },
          { key: 'qs', label: 'Soru', width: '64px', mono: true, value: (r) => r.questionCount || 0 },
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
          { key: 'pearl', label: 'Spot', width: '64px', value: (r) => (r.clinicalPearls ? 1 : 0), render: (r) => (r.clinicalPearls ? <Pill cls="is-ok">Var</Pill> : <span className="text-ink-3">—</span>) },
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
    void load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [dsId]);
  // Pool questions come from props; keep in sync
  useEffect(() => {
    if (dsId === 'questions') setRows(questions as Row[]);
  }, [questions, dsId]);

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
      }
  };

  return (
    <div className="flex flex-col gap-3 min-w-0">
      <Seg label="Veri kümesi" value={dsId} onChange={setDsId} options={DATASETS.map((d) => ({ id: d.id, label: d.label }))} className="self-start" />

      <div className="flex flex-wrap items-center gap-2">
        <SearchBox value={query} onChange={setQuery} placeholder={`${ds.label} içinde ara`} count={`${visible.length.toLocaleString('tr-TR')} kayıt`} className="flex-1 min-w-[220px]" />
        <div className="relative">
          <button type="button" onClick={() => setColMenu((v) => !v)} aria-expanded={colMenu} className="ms-btn">
            <Columns3 /> Sütunlar
          </button>
          {colMenu && (
            <>
              <div className="fixed inset-0 z-20" onClick={() => setColMenu(false)} aria-hidden="true" />
              <div className="ms-menu">
                {ds.columns.map((c) => (
                  <label key={c.key} className="ms-menu-item">
                    <input type="checkbox" checked={!hidden[c.key]} onChange={() => setHidden((h) => ({ ...h, [c.key]: !h[c.key] }))} />
                    {c.label}
                  </label>
                ))}
              </div>
            </>
          )}
        </div>
        <button type="button" onClick={() => exportCsv(false)} className="ms-btn">
          <Download /> CSV
        </button>
        <button type="button" onClick={() => void load()} aria-label="Yenile" title="Yenile" className="ms-btn is-ghost is-icon">
          <RefreshCw className={loading ? 'animate-spin' : ''} />
        </button>
      </div>

      <div className="ms-table-wrap">
        <div className="w-full min-w-[760px]">
          <div className="grid items-center gap-x-3 h-10 px-3 border-b border-line text-[12px] font-semibold text-ink-3 sticky top-0 bg-white z-[1]" style={{ gridTemplateColumns: grid }}>
            <input
              type="checkbox"
              aria-label="Bu sayfadakilerin hepsini seç"
              checked={allOnPage}
              onChange={() => setSelected((s) => (allOnPage ? s.filter((id) => !shown.some((r) => ds.idOf(r) === id)) : Array.from(new Set([...s, ...shown.map(ds.idOf)]))))}
              className="w-[15px] h-[15px] accent-accent cursor-pointer"
            />
            {cols.map((c) => (
              <button key={c.key} type="button" onClick={() => toggleSort(c.key)} className={`text-left inline-flex items-center gap-1 cursor-pointer hover:text-ink whitespace-nowrap ${sort.key === c.key ? 'text-ink' : ''}`} aria-sort={sort.key === c.key ? (sort.dir === 1 ? 'ascending' : 'descending') : undefined}>
                {c.label}
                {sort.key === c.key && (sort.dir === 1 ? <ArrowUp className="w-3 h-3" /> : <ArrowDown className="w-3 h-3" />)}
              </button>
            ))}
          </div>
          {loading && rows.length === 0 ? (
            <div className="p-3 flex flex-col gap-2" role="status" aria-label="Yükleniyor">
              {[0, 1, 2, 3, 4].map((i) => <div key={i} className="h-8 rounded-lg ms-shimmer" />)}
            </div>
          ) : shown.length === 0 ? (
            <EmptyState icon={Search} title={query ? 'Aramaya uyan kayıt yok' : 'Bu kümede kayıt yok'} />
          ) : (
            shown.map((r) => {
              const id = ds.idOf(r);
              const sel = selected.includes(id);
              const open = openId === id;
              return (
                <div
                  key={id}
                  onClick={() => setOpenId(open ? null : id)}
                  className={`grid items-center gap-x-3 min-h-10 px-3 py-1.5 border-b border-line-soft last:border-b-0 text-[13.5px] cursor-pointer transition-colors ${sel || open ? 'bg-accent-soft' : 'hover:bg-canvas'}`}
                  style={{ gridTemplateColumns: grid }}
                >
                  <input type="checkbox" checked={sel} onClick={(e) => e.stopPropagation()} onChange={() => toggleRow(id)} aria-label="Satırı seç" className="w-[15px] h-[15px] accent-accent cursor-pointer" />
                  {cols.map((c) => (
                    <span key={c.key} className={`min-w-0 truncate ${c.mono ? 'font-mono text-[12.5px]' : ''}`} title={String(c.value(r))}>
                      {c.render ? c.render(r) : c.value(r) || '—'}
                    </span>
                  ))}
                </div>
              );
            })
          )}
          {visible.length > limit && (
            <button type="button" onClick={() => setLimit((n) => n + 200)} className="w-full h-11 border-t border-line-soft text-[13px] font-semibold text-accent cursor-pointer inline-flex items-center justify-center gap-1 hover:bg-canvas">
              <ChevronDown className="w-4 h-4" />
              {(visible.length - limit).toLocaleString('tr-TR')} kayıt daha
            </button>
          )}
        </div>
      </div>

      {selected.length > 0 && (
        <div className="ms-bulkbar">
          <b>{selected.length} seçili</b>
          <button type="button" onClick={() => exportCsv(true)} className="ms-btn is-sm">
            <Download /> CSV
          </button>
          {ds.canVerify && (
            <button type="button" disabled={busy} onClick={() => void runBulk('verify', selected)} className="ms-btn is-sm">
              <CheckCircle2 /> Doğrula
            </button>
          )}
          {ds.canDelete && (
            <ConfirmButton icon={Trash2} className="ms-btn is-sm" confirmLabel={`Emin misin? ${selected.length} kaydı sil`} busy={busy} onConfirm={() => runBulk('delete', selected)}>
              Sil
            </ConfirmButton>
          )}
          <button type="button" onClick={() => setSelected([])} aria-label="Seçimi temizle" className="ms-btn is-sm is-icon">
            <X />
          </button>
        </div>
      )}

      <Drawer
        open={!!openRow}
        onClose={() => setOpenId(null)}
        label="Kayıt ayrıntısı"
        title={openRow ? String(ds.columns[0].value(openRow)).slice(0, 80) || 'Kayıt' : ''}
        foot={
          openRow && (
            <>
              <button
                type="button"
                onClick={() => {
                  navigator.clipboard?.writeText(JSON.stringify(openRow, null, 2)).then(
                    () => toast.success('Kopyalandı', 'Kaydın tamamı JSON olarak panoda'),
                    () => toast.error('Kopyalanamadı'),
                  );
                }}
                className="ms-btn"
              >
                <Copy /> JSON
              </button>
              {ds.canVerify && openRow.status !== 'completed' && (
                <button type="button" disabled={busy} onClick={() => void runBulk('verify', [ds.idOf(openRow)])} className="ms-btn is-ok">
                  <CheckCircle2 /> Doğrula
                </button>
              )}
              {ds.canDelete && (
                <ConfirmButton icon={Trash2} className="ms-btn is-danger" confirmLabel="Emin misin? Sil" busy={busy} onConfirm={() => runBulk('delete', [ds.idOf(openRow)])}>
                  Sil
                </ConfirmButton>
              )}
            </>
          )
        }
      >
        {openRow && (
          <dl className="ms-kv">
            {ds.columns.map((c) => (
              <React.Fragment key={c.key}>
                <dt>{c.label}</dt>
                <dd className={c.mono ? 'font-mono' : ''}>{c.render ? c.render(openRow) : String(c.value(openRow) || '—')}</dd>
              </React.Fragment>
            ))}
          </dl>
        )}
      </Drawer>
    </div>
  );
};
