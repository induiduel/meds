import React, { useEffect, useMemo, useState } from 'react';
import { Search, ArrowUp, ArrowDown, Columns3, Download, X, Trash2, CheckCircle2, Copy, RefreshCw, ChevronDown, Save, RotateCcw, Sparkles, AlertTriangle, FileJson, Check, User, History, Calendar, FileText, ArrowRight } from 'lucide-react';
import { Committee, QuestionItem } from '../../types';
import { ApiService } from '../../services/api';
import { toast } from '../ui/Toast';
import { Seg, SearchBox, EmptyState, ConfirmButton, Drawer } from './consoleUi';
import { AdminEditQuestionModal } from '../AdminEditQuestionModal';

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
  initialFocusId?: string | null;
  initialDsId?: DatasetId;
  onClearFocus?: () => void;
}

const STATUS_TONE: Record<string, string> = { completed: 'is-ok', gathering: 'is-warn', empty: '' };
const STATUS_LABEL: Record<string, string> = { completed: 'Doğrulandı', gathering: 'Taslak', empty: 'Boş' };
const fmtDate = (s?: string) => (s ? new Date(s).toLocaleDateString('tr-TR', { day: '2-digit', month: '2-digit', year: '2-digit' }) : '—');
const stemOf = (q: Row) => q?.reconstruction?.stem || q?.stem || q?.rawQuestion?.stem || q?.fragments?.[0]?.text || q?.topic || '';
const Pill: React.FC<{ cls: string; children: React.ReactNode }> = ({ cls, children }) => <span className={`ms-tag ${cls}`}>{children}</span>;

export const ManageDataSection: React.FC<Props> = ({
  adminEmail,
  questions,
  committees,
  onRefreshData,
  initialFocusId,
  initialDsId,
  onClearFocus,
}) => {
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
          { key: 'author', label: 'Ekleyen', width: '130px', value: (r) => r.contributedByName || r.author || r.fragments?.[0]?.author || '', render: (r) => {
            const author = r.contributedByName || r.author || r.fragments?.[0]?.author;
            return author ? <span className="text-ink font-medium truncate max-w-[120px] inline-block">{author}</span> : <span className="text-ink-3">—</span>;
          }},
          { key: 'updatedAt', label: 'Güncel', width: '80px', value: (r) => r.updatedAt || '', render: (r) => fmtDate(r.updatedAt) },
        ],
      },
      {
        id: 'past',
        label: 'Çıkmış sorular',
        canDelete: true,
        load: async () => (await ApiService.getPastQuestions({ includeAmbiguous: true })) as Row[],
        idOf: (r) => String(r.id),
        defaultSort: { key: 'year', dir: -1 },
        columns: [
          { key: 'no', label: 'No', width: '56px', mono: true, value: (r) => r.questionNumber || 0 },
          { key: 'stem', label: 'Soru', width: 'minmax(0,1fr)', value: (r) => stemOf(r) },
          { key: 'discipline', label: 'Ders', width: '140px', value: (r) => r.discipline || '' },
          { key: 'committee', label: 'Kurul', width: '110px', value: (r) => committeeName(r.committeeId) },
          { key: 'year', label: 'Yıl', width: '90px', value: (r) => r.examYear || '' },
          { key: 'author', label: 'Ekleyen / Kaynak', width: '130px', value: (r) => r.contributedByName || r.author || r.sourceFile || '', render: (r) => {
            const author = r.contributedByName || r.author || r.sourceFile;
            return author ? <span className="text-ink font-medium truncate max-w-[120px] inline-block" title={author}>{author}</span> : <span className="text-ink-3">—</span>;
          }},
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
          const mod: any = await import('../../data/summaries_meta.json');
          const v = mod ? (mod.default || mod) : [];
          return (Array.isArray(v) ? v : Object.values(v || {})) as Row[];
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

  const [dsId, setDsId] = useState<DatasetId>(initialDsId || 'questions');
  const ds = DATASETS.find((d) => d.id === dsId) || DATASETS[0];
  const [rows, setRows] = useState<Row[]>([]);
  const [loading, setLoading] = useState(false);
  const [query, setQuery] = useState(initialFocusId ? String(initialFocusId) : '');
  const [sort, setSort] = useState(ds.defaultSort);
  const [hidden, setHidden] = useState<Record<string, boolean>>({});
  const [colMenu, setColMenu] = useState(false);
  const [selected, setSelected] = useState<string[]>([]);
  const [openId, setOpenId] = useState<string | null>(initialFocusId || null);
  const [limit, setLimit] = useState(100);
  const [busy, setBusy] = useState(false);

  // initialFocusId veya initialDsId değiştiğinde dinamik aç
  useEffect(() => {
    if (initialDsId) setDsId(initialDsId);
    if (initialFocusId) {
      setOpenId(initialFocusId);
      setQuery(String(initialFocusId));
    }
  }, [initialFocusId, initialDsId]);

  // Düzenleme durumu (Form & JSON)
  const [editDraft, setEditDraft] = useState<Row | null>(null);
  const [jsonText, setJsonText] = useState<string>('');
  const [jsonError, setJsonError] = useState<string | null>(null);
  const [editTab, setEditTab] = useState<'form' | 'json' | 'history'>('form');
  const [savingRow, setSavingRow] = useState(false);
  const [wizardQuestion, setWizardQuestion] = useState<QuestionItem | null>(null);

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

  // openRow değiştiğinde düzenleme taslağını senkronize et
  useEffect(() => {
    if (openRow) {
      const copy = JSON.parse(JSON.stringify(openRow));
      setEditDraft(copy);
      setJsonText(JSON.stringify(copy, null, 2));
      setJsonError(null);
      setEditTab('form');
    } else {
      setEditDraft(null);
      setJsonText('');
      setJsonError(null);
    }
  }, [openId, openRow]);

  const toggleSort = (key: string) => setSort((s) => (s.key === key ? { key, dir: s.dir === 1 ? -1 : 1 } : { key, dir: 1 }));
  const toggleRow = (id: string) => setSelected((s) => (s.includes(id) ? s.filter((x) => x !== id) : [...s, id]));

  // Düzenleme yardımcıları
  const handleFormChange = (key: string, value: any) => {
    setEditDraft((prev) => {
      if (!prev) return null;
      const next = { ...prev, [key]: value };
      setJsonText(JSON.stringify(next, null, 2));
      return next;
    });
  };

  const handleJsonChange = (text: string) => {
    setJsonText(text);
    try {
      const parsed = JSON.parse(text);
      setEditDraft(parsed);
      setJsonError(null);
    } catch (e: any) {
      setJsonError(e.message);
    }
  };

  const handleFormatJson = () => {
    try {
      const parsed = JSON.parse(jsonText);
      const formatted = JSON.stringify(parsed, null, 2);
      setJsonText(formatted);
      setEditDraft(parsed);
      setJsonError(null);
      toast.success('JSON biçimlendirildi');
    } catch (e: any) {
      toast.error('JSON biçimlendirilemedi', e.message);
    }
  };

  const handleResetDraft = () => {
    if (openRow) {
      const copy = JSON.parse(JSON.stringify(openRow));
      setEditDraft(copy);
      setJsonText(JSON.stringify(copy, null, 2));
      setJsonError(null);
      toast.info('Değişiklikler geri alındı');
    }
  };

  // Soru için özel düzenleme yardımcıları
  const handleQuestionStemChange = (stem: string) => {
    setEditDraft((prev: any) => {
      if (!prev) return null;
      const rec = prev.reconstruction ? { ...prev.reconstruction, stem } : undefined;
      const next = {
        ...prev,
        stem,
        ...(rec ? { reconstruction: rec } : {}),
      };
      setJsonText(JSON.stringify(next, null, 2));
      return next;
    });
  };

  const handleQuestionAnswerChange = (ans: string) => {
    setEditDraft((prev: any) => {
      if (!prev) return null;
      const rec = prev.reconstruction ? { ...prev.reconstruction, correctAnswer: ans } : undefined;
      const next = {
        ...prev,
        correctAnswer: ans,
        claimedAnswer: ans,
        ...(rec ? { reconstruction: rec } : {}),
      };
      setJsonText(JSON.stringify(next, null, 2));
      return next;
    });
  };

  const handleQuestionOptionChange = (optKey: string, text: string) => {
    setEditDraft((prev: any) => {
      if (!prev) return null;
      const currentOpts = Array.isArray(prev.options) ? [...prev.options] : [];
      const idx = currentOpts.findIndex((o: any) => o.key === optKey);
      if (idx !== -1) {
        currentOpts[idx] = { ...currentOpts[idx], text };
      } else {
        currentOpts.push({ key: optKey, text });
      }

      const rec = prev.reconstruction ? { ...prev.reconstruction } : null;
      if (rec && Array.isArray(rec.options)) {
        const rIdx = rec.options.findIndex((o: any) => o.key === optKey);
        if (rIdx !== -1) {
          rec.options = [...rec.options];
          rec.options[rIdx] = { ...rec.options[rIdx], text };
        } else {
          rec.options = [...rec.options, { key: optKey, text }];
        }
      }

      const next = {
        ...prev,
        options: currentOpts,
        ...(rec ? { reconstruction: rec } : {}),
      };
      setJsonText(JSON.stringify(next, null, 2));
      return next;
    });
  };

  const handleQuestionExplanationChange = (explanation: string) => {
    setEditDraft((prev: any) => {
      if (!prev) return null;
      const rec = prev.reconstruction ? { ...prev.reconstruction, explanation } : undefined;
      const next = {
        ...prev,
        explanation,
        clinicalExplanation: explanation,
        ...(rec ? { reconstruction: rec } : {}),
      };
      setJsonText(JSON.stringify(next, null, 2));
      return next;
    });
  };

  // Veriyi kaydetme
  const saveRow = async () => {
    if (!editDraft || !openRow) return;
    setSavingRow(true);
    try {
      let payload = editDraft;
      if (editTab === 'json') {
        try {
          payload = JSON.parse(jsonText);
        } catch (e: any) {
          toast.error('Geçersiz JSON', e.message || 'Lütfen JSON sözdizimini düzeltin.');
          setSavingRow(false);
          return;
        }
      }

      const id = ds.idOf(openRow);

      if (ds.id === 'questions') {
        await ApiService.adminUpdateQuestion(adminEmail, id, payload as Partial<QuestionItem>);
        await onRefreshData();
      } else if (ds.id === 'past') {
        await ApiService.adminUpdatePastQuestion(adminEmail, id, payload);
        await load();
      } else if (ds.id === 'users') {
        await ApiService.adminUpdateUser(adminEmail, id, payload);
        await load();
      } else if (ds.id === 'summaries') {
        await ApiService.adminUpdateSummary(adminEmail, id, payload);
        await load();
      } else {
        // decks, glossary veya genel veri kümesi
        setRows((prev) => prev.map((r) => (ds.idOf(r) === id ? { ...r, ...payload } : r)));
      }

      toast.success('Kaydedildi', 'Tüm değişiklikler başarıyla uygulandı.');
      setRows((prev) => prev.map((r) => (ds.idOf(r) === id ? { ...r, ...payload } : r)));
      setEditDraft({ ...payload });
      setJsonText(JSON.stringify(payload, null, 2));
    } catch (e: any) {
      toast.error('Kaydedilemedi', e?.message || 'Bilinmeyen bir hata oluştu.');
    } finally {
      setSavingRow(false);
    }
  };

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
            else if (ds.id === 'past') await ApiService.adminDeletePastQuestion(adminEmail, id);
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
      if (ds.id === 'questions') {
        await onRefreshData();
      } else if (ds.id === 'past') {
        try {
          const { pastQuestionsCache } = await import('../../services/pastQuestionsCache');
          await pastQuestionsCache.removeQuestions(ids);
        } catch {}
        await onRefreshData();
        await load();
      } else {
        await load();
      }
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
        onClose={() => {
          setOpenId(null);
          onClearFocus?.();
        }}
        wide
        label="Veri Düzenleme"
        title={
          openRow ? (
            <div className="flex items-center gap-2 min-w-0 pr-2">
              <span className="font-semibold text-ink truncate">
                {String(ds.columns[0]?.value(openRow) || ds.idOf(openRow)).slice(0, 45)}
              </span>
              <span className="text-[11.5px] px-2 py-0.5 rounded-full bg-accent-soft text-accent font-medium shrink-0">
                {ds.label}
              </span>
            </div>
          ) : ''
        }
        head={
          <div className="flex items-center gap-1 bg-surface-2 p-1 rounded-lg border border-line-soft">
            <button
              type="button"
              onClick={() => {
                setEditTab('form');
                if (editDraft) setJsonText(JSON.stringify(editDraft, null, 2));
              }}
              className={`px-3 py-1 text-[12px] font-medium rounded-md transition-all ${
                editTab === 'form' ? 'bg-white shadow-xs text-ink font-semibold' : 'text-ink-3 hover:text-ink'
              }`}
            >
              Form Düzenleyici
            </button>
            {(ds.id === 'questions' || ds.id === 'past') && (
              <button
                type="button"
                onClick={() => setEditTab('history')}
                className={`px-3 py-1 text-[12px] font-medium rounded-md transition-all inline-flex items-center gap-1.5 ${
                  editTab === 'history' ? 'bg-white shadow-xs text-ink font-semibold' : 'text-ink-3 hover:text-ink'
                }`}
              >
                <History className="w-3.5 h-3.5" />
                <span>Geçmiş & Katkılar</span>
                {Boolean((openRow?.revisions?.length || 0) + (openRow?.fragments?.length || 0)) && (
                  <span className="px-1.5 py-0.2 rounded-full bg-accent-soft text-accent text-[10.5px] font-bold">
                    {(openRow?.revisions?.length || 0) + (openRow?.fragments?.length || 0)}
                  </span>
                )}
              </button>
            )}
            <button
              type="button"
              onClick={() => {
                setEditTab('json');
                if (editDraft) setJsonText(JSON.stringify(editDraft, null, 2));
              }}
              className={`px-3 py-1 text-[12px] font-medium rounded-md transition-all ${
                editTab === 'json' ? 'bg-white shadow-xs text-ink font-semibold' : 'text-ink-3 hover:text-ink'
              }`}
            >
              Tüm Alanlar (JSON)
            </button>
          </div>
        }
        foot={
          openRow && editDraft && (
            <div className="flex flex-wrap items-center justify-between gap-2 w-full">
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  disabled={savingRow}
                  onClick={() => void saveRow()}
                  className="ms-btn is-ok inline-flex items-center gap-1.5 font-semibold shadow-xs"
                >
                  <Save className={`w-4 h-4 ${savingRow ? 'animate-spin' : ''}`} />
                  {savingRow ? 'Kaydediliyor…' : 'Kaydet'}
                </button>
                <button
                  type="button"
                  disabled={savingRow}
                  onClick={handleResetDraft}
                  className="ms-btn is-ghost text-ink-3 hover:text-ink"
                  title="İlk haline dön"
                >
                  <RotateCcw className="w-4 h-4" /> Sıfırla
                </button>
              </div>

              <div className="flex items-center gap-1.5">
                {ds.id === 'questions' && (
                  <button
                    type="button"
                    onClick={() => setWizardQuestion(editDraft as QuestionItem)}
                    className="ms-btn is-ghost text-accent hover:bg-accent-soft text-[12.5px]"
                    title="Gelişmiş soru sihirbazında düzenle"
                  >
                    <Sparkles className="w-3.5 h-3.5" /> Sihirbaz
                  </button>
                )}
                <button
                  type="button"
                  onClick={() => {
                    navigator.clipboard?.writeText(jsonText).then(
                      () => toast.success('Kopyalandı', 'JSON panoya kopyalandı'),
                      () => toast.error('Kopyalanamadı'),
                    );
                  }}
                  className="ms-btn is-ghost is-sm"
                  title="JSON Kopyala"
                >
                  <Copy className="w-3.5 h-3.5" />
                </button>
                {ds.canVerify && openRow.status !== 'completed' && (
                  <button
                    type="button"
                    disabled={busy}
                    onClick={() => void runBulk('verify', [ds.idOf(openRow)])}
                    className="ms-btn is-sm is-ghost text-emerald-600 hover:bg-emerald-50"
                  >
                    <CheckCircle2 className="w-3.5 h-3.5" /> Doğrula
                  </button>
                )}
                {ds.canDelete && (
                  <ConfirmButton
                    icon={Trash2}
                    className="ms-btn is-sm is-danger"
                    confirmLabel="Emin misin? Sil"
                    busy={busy}
                    onConfirm={() => runBulk('delete', [ds.idOf(openRow)])}
                  >
                    Sil
                  </ConfirmButton>
                )}
              </div>
            </div>
          )
        }
      >
        {openRow && editDraft && (
          <div className="flex flex-col gap-4">
            {editTab === 'json' ? (
              <div className="flex flex-col gap-2">
                <div className="flex items-center justify-between text-[12px] text-ink-3 bg-surface-2 p-2.5 rounded-lg border border-line-soft">
                  <span>Bu verinin tamamını (alt nesneler, diziler, özel alanlar) doğrudan JSON olarak düzenleyebilirsiniz.</span>
                  <button
                    type="button"
                    onClick={handleFormatJson}
                    className="ms-btn is-sm is-ghost text-accent hover:bg-white inline-flex items-center gap-1 font-medium shrink-0 ml-2"
                  >
                    <FileJson className="w-3.5 h-3.5" /> Biçimlendir
                  </button>
                </div>
                {jsonError && (
                  <div className="flex items-start gap-2 p-2.5 rounded-lg bg-rose-50 border border-rose-200 text-rose-700 text-[12px]">
                    <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5" />
                    <div>
                      <b className="font-semibold">JSON Sözdizimi Hatası:</b> {jsonError}
                    </div>
                  </div>
                )}
                <textarea
                  value={jsonText}
                  onChange={(e) => handleJsonChange(e.target.value)}
                  spellCheck={false}
                  rows={24}
                  className={`w-full font-mono text-[12.5px] leading-relaxed p-3.5 rounded-lg border bg-surface-1 text-ink focus:bg-white focus:outline-none focus:ring-2 focus:ring-accent ${
                    jsonError ? 'border-rose-400 focus:ring-rose-400' : 'border-line'
                  }`}
                />
              </div>
            ) : editTab === 'history' ? (
              <div className="flex flex-col gap-4">
                {/* Yazar & Ekleyen Özeti */}
                <div className="p-3.5 rounded-xl border border-line bg-surface-2 flex flex-col gap-2">
                  <div className="text-[12px] font-bold uppercase tracking-wider text-ink-3">Veri Kaynağı & İlk Ekleyen</div>
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-[13px]">
                    <div>
                      <span className="text-ink-3 block text-[11.5px]">Ekleyen Kullanıcı:</span>
                      <b className="text-ink font-semibold">{editDraft.contributedByName || editDraft.author || '—'}</b>
                    </div>
                    <div>
                      <span className="text-ink-3 block text-[11.5px]">Öğrenci No / UID:</span>
                      <span className="font-mono text-ink-2">{editDraft.contributedByStudentNumber || editDraft.contributedByUid || '—'}</span>
                    </div>
                    <div>
                      <span className="text-ink-3 block text-[11.5px]">Eklenme Tarihi:</span>
                      <span className="text-ink-2">{fmtDate(editDraft.createdAt || editDraft.updatedAt)}</span>
                    </div>
                  </div>
                  {editDraft.sourceFile && (
                    <div className="text-[12px] pt-1 border-t border-line-soft text-ink-3">
                      Kaynak Dosya / OCR: <span className="font-mono text-ink-2">{editDraft.sourceFile}</span>
                    </div>
                  )}
                </div>

                {/* Revizyonlar / Düzenleme Geçmişi */}
                <div className="flex flex-col gap-2">
                  <div className="flex items-center justify-between">
                    <h3 className="text-[13.5px] font-bold text-ink flex items-center gap-2">
                      <History className="w-4 h-4 text-accent" />
                      <span>Düzenleme Geçmişi (Revizyonlar)</span>
                    </h3>
                    <span className="text-[12px] text-ink-3">{(editDraft.revisions || []).length} versiyon</span>
                  </div>

                  {(!editDraft.revisions || editDraft.revisions.length === 0) ? (
                    <div className="p-4 text-center border border-dashed border-line rounded-xl text-ink-3 text-[12.5px]">
                      Bu veri için kaydedilmiş geçmiş düzenleme revizyonu bulunmuyor.
                    </div>
                  ) : (
                    <div className="flex flex-col gap-2.5">
                      {[...editDraft.revisions].reverse().map((rev: any, idx: number) => {
                        const revNum = rev.version || (editDraft.revisions.length - idx);
                        const isLatest = idx === 0;
                        return (
                          <div
                            key={rev.id || idx}
                            className={`p-3.5 rounded-xl border transition-all ${
                              isLatest ? 'bg-accent-soft/30 border-accent/40 shadow-2xs' : 'bg-surface-1 border-line'
                            }`}
                          >
                            <div className="flex items-center justify-between pb-2 border-b border-line-soft">
                              <div className="flex items-center gap-2">
                                <span className={`text-[11px] font-bold px-2 py-0.5 rounded-full ${isLatest ? 'bg-accent text-white' : 'bg-surface-2 text-ink-2'}`}>
                                  v{revNum} {isLatest && '(Son)'}
                                </span>
                                <span className="font-semibold text-[13px] text-ink">
                                  {rev.changeSummary || 'Düzenleme yapıldı'}
                                </span>
                              </div>
                              <span className="text-[11.5px] text-ink-3">{fmtDate(rev.editedAt)}</span>
                            </div>

                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-2 text-[12px] text-ink-2">
                              <div>
                                <span className="text-ink-3">Düzenleyen:</span>{' '}
                                <b className="text-ink font-semibold">{rev.editorName || 'Anonim'}</b>
                                {rev.editorStudentNumber && (
                                  <span className="font-mono text-ink-3 ml-1.5">({rev.editorStudentNumber})</span>
                                )}
                              </div>
                              {rev.claimedAnswer && (
                                <div>
                                  <span className="text-ink-3">Cevap Önerisi:</span>{' '}
                                  <b className="font-bold text-accent">{rev.claimedAnswer}</b>
                                </div>
                              )}
                            </div>

                            {rev.stem && rev.stem !== editDraft.reconstruction?.stem && (
                              <div className="mt-2 p-2 rounded-lg bg-surface-2 text-[12px] text-ink-2 border border-line-soft max-h-24 overflow-y-auto">
                                <div className="text-[11px] font-medium text-ink-3 mb-0.5">Bu versiyondaki soru kökü:</div>
                                {rev.stem}
                              </div>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  )}
                </div>

                {/* Hafıza Parçaları & Katkı Sağlayanlar */}
                <div className="flex flex-col gap-2 pt-2">
                  <div className="flex items-center justify-between">
                    <h3 className="text-[13.5px] font-bold text-ink flex items-center gap-2">
                      <FileText className="w-4 h-4 text-emerald-600" />
                      <span>Kullanıcı Hafıza Parçaları (Fragments)</span>
                    </h3>
                    <span className="text-[12px] text-ink-3">{(editDraft.fragments || []).length} parça</span>
                  </div>

                  {(!editDraft.fragments || editDraft.fragments.length === 0) ? (
                    <div className="p-3 text-center border border-dashed border-line rounded-xl text-ink-3 text-[12.5px]">
                      Kullanıcılar tarafından eklenmiş hafıza parçası yok.
                    </div>
                  ) : (
                    <div className="flex flex-col gap-2">
                      {editDraft.fragments.map((frag: any, fIdx: number) => (
                        <div key={frag.id || fIdx} className="p-3 rounded-xl border border-line-soft bg-surface-1 flex flex-col gap-1.5 text-[12.5px]">
                          <div className="flex items-center justify-between">
                            <span className="font-semibold text-ink flex items-center gap-1.5">
                              <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                              {frag.author || 'İsimsiz Öğrenci'}
                              {frag.authorStudentNumber && (
                                <span className="font-mono text-ink-3 text-[11px]">({frag.authorStudentNumber})</span>
                              )}
                            </span>
                            <span className="text-[11px] text-ink-3">{fmtDate(frag.timestamp)}</span>
                          </div>
                          <p className="m-0 text-ink-2 leading-relaxed bg-surface-2 p-2 rounded-lg border border-line-soft">
                            {frag.text}
                          </p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <div className="flex flex-col gap-4">
                {/* Ekleyen ve Revizyon Hızlı Bilgi Şeridi */}
                {(ds.id === 'questions' || ds.id === 'past') && (
                  <div className="p-2.5 rounded-xl bg-accent-soft/40 border border-accent/20 flex items-center justify-between text-[12.5px]">
                    <div className="flex items-center gap-2 min-w-0">
                      <User className="w-4 h-4 text-accent shrink-0" />
                      <span className="truncate">
                        <span className="text-ink-3">Ekleyen:</span>{' '}
                        <b className="text-ink">{editDraft.contributedByName || editDraft.author || editDraft.fragments?.[0]?.author || 'Bilinmiyor'}</b>
                        {editDraft.contributedByStudentNumber && (
                          <span className="font-mono text-ink-3 ml-1">({editDraft.contributedByStudentNumber})</span>
                        )}
                      </span>
                    </div>
                    <button
                      type="button"
                      onClick={() => setEditTab('history')}
                      className="text-accent hover:underline text-[12px] font-semibold shrink-0 inline-flex items-center gap-1"
                    >
                      <span>Tüm Geçmiş ({editDraft.revisions?.length || 0})</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </button>
                  </div>
                )}
                {(ds.id === 'questions' || ds.id === 'past') && (
                  <>
                    <div className="flex flex-col gap-1.5">
                      <label className="text-[12.5px] font-semibold text-ink flex items-center justify-between">
                        <span>Soru Kökü / Metni</span>
                        <span className="text-[11.5px] text-ink-3 font-normal">Markdown formatı geçerlidir</span>
                      </label>
                      <textarea
                        value={stemOf(editDraft)}
                        onChange={(e) => handleQuestionStemChange(e.target.value)}
                        rows={4}
                        placeholder="Soru metnini girin..."
                        className="w-full text-[13.5px] leading-relaxed p-3 rounded-lg border border-line bg-surface-1 focus:bg-white focus:outline-none focus:ring-2 focus:ring-accent"
                      />
                    </div>

                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
                      <div>
                        <label className="text-[11.5px] font-medium text-ink-3 block mb-1">Soru No</label>
                        <input
                          type="number"
                          value={editDraft.questionNumber ?? ''}
                          onChange={(e) => handleFormChange('questionNumber', e.target.value === '' ? 0 : Number(e.target.value))}
                          className="w-full h-9 px-2.5 text-[13px] rounded-lg border border-line bg-surface-1 focus:bg-white"
                        />
                      </div>
                      <div>
                        <label className="text-[11.5px] font-medium text-ink-3 block mb-1">Ders / Branş</label>
                        <input
                          type="text"
                          value={editDraft.discipline || ''}
                          onChange={(e) => handleFormChange('discipline', e.target.value)}
                          placeholder="Örn: Patoloji"
                          className="w-full h-9 px-2.5 text-[13px] rounded-lg border border-line bg-surface-1 focus:bg-white"
                        />
                      </div>
                      <div>
                        <label className="text-[11.5px] font-medium text-ink-3 block mb-1">Konu Başlığı</label>
                        <input
                          type="text"
                          value={editDraft.topic || ''}
                          onChange={(e) => handleFormChange('topic', e.target.value)}
                          placeholder="Örn: Hücre Zedelenmesi"
                          className="w-full h-9 px-2.5 text-[13px] rounded-lg border border-line bg-surface-1 focus:bg-white"
                        />
                      </div>
                      <div>
                        <label className="text-[11.5px] font-medium text-ink-3 block mb-1">Durum</label>
                        <select
                          value={editDraft.status || 'gathering'}
                          onChange={(e) => handleFormChange('status', e.target.value)}
                          className="w-full h-9 px-2 text-[13px] rounded-lg border border-line bg-surface-1 focus:bg-white"
                        >
                          <option value="completed">Doğrulandı</option>
                          <option value="gathering">Taslak</option>
                          <option value="empty">Boş</option>
                        </select>
                      </div>
                      {ds.id === 'past' && (
                        <>
                          <div>
                            <label className="text-[11.5px] font-medium text-ink-3 block mb-1">Sınav Yılı</label>
                            <input
                              type="text"
                              value={editDraft.examYear || ''}
                              onChange={(e) => handleFormChange('examYear', e.target.value)}
                              placeholder="Örn: 2024-2025"
                              className="w-full h-9 px-2.5 text-[13px] rounded-lg border border-line bg-surface-1 focus:bg-white"
                            />
                          </div>
                          <div>
                            <label className="text-[11.5px] font-medium text-ink-3 block mb-1">Kurul Kodu</label>
                            <input
                              type="text"
                              value={editDraft.committeeId || ''}
                              onChange={(e) => handleFormChange('committeeId', e.target.value)}
                              placeholder="Örn: donem3-kurul1"
                              className="w-full h-9 px-2.5 text-[13px] rounded-lg border border-line bg-surface-1 focus:bg-white"
                            />
                          </div>
                        </>
                      )}
                    </div>

                    <div className="flex flex-col gap-2">
                      <div className="flex items-center justify-between">
                        <label className="text-[12.5px] font-semibold text-ink">Şıklar ve Doğru Cevap</label>
                        <span className="text-[11.5px] text-ink-3">Doğru şık için harfe tıklayın</span>
                      </div>
                      {['A', 'B', 'C', 'D', 'E'].map((letter) => {
                        const currentOpt =
                          (editDraft.reconstruction?.options || editDraft.options || []).find((o: any) => o.key === letter);
                        const currentAnswer =
                          editDraft.reconstruction?.correctAnswer || editDraft.correctAnswer || editDraft.claimedAnswer;
                        const isCorrect = currentAnswer === letter;
                        return (
                          <div
                            key={letter}
                            className={`flex items-start gap-2 p-2 rounded-lg border transition-colors ${
                              isCorrect ? 'bg-emerald-50/70 border-emerald-300' : 'bg-surface-1 border-line-soft'
                            }`}
                          >
                            <button
                              type="button"
                              onClick={() => handleQuestionAnswerChange(letter)}
                              className={`w-7 h-7 rounded-md font-bold text-[12px] flex items-center justify-center shrink-0 transition-colors ${
                                isCorrect ? 'bg-emerald-600 text-white shadow-xs' : 'bg-surface-2 text-ink-3 hover:bg-emerald-100 hover:text-emerald-700'
                              }`}
                              title={isCorrect ? 'Doğru cevap seçili' : 'Doğru cevap olarak işaretle'}
                            >
                              {letter}
                            </button>
                            <input
                              type="text"
                              value={currentOpt?.text || ''}
                              onChange={(e) => handleQuestionOptionChange(letter, e.target.value)}
                              placeholder={`${letter} şıkkı metni...`}
                              className="flex-1 min-w-0 bg-transparent text-[13px] border-none outline-none py-1 text-ink"
                            />
                            {isCorrect && (
                              <span className="text-[11px] font-medium text-emerald-700 px-1.5 py-0.5 bg-emerald-100/80 rounded shrink-0">
                                Doğru
                              </span>
                            )}
                          </div>
                        );
                      })}
                    </div>

                    <div className="flex flex-col gap-1.5">
                      <label className="text-[12.5px] font-semibold text-ink">Çözüm ve Tıbbi Açıklama</label>
                      <textarea
                        value={editDraft.reconstruction?.explanation || editDraft.explanation || editDraft.clinicalExplanation || ''}
                        onChange={(e) => handleQuestionExplanationChange(e.target.value)}
                        rows={4}
                        placeholder="Sorunun ayrıntılı fizyopatolojik gerekçesi ve şık analizleri..."
                        className="w-full text-[13px] leading-relaxed p-3 rounded-lg border border-line bg-surface-1 focus:bg-white focus:outline-none focus:ring-2 focus:ring-accent"
                      />
                    </div>
                  </>
                )}

                {ds.id === 'users' && (
                  <div className="flex flex-col gap-3">
                    <div>
                      <label className="text-[12px] font-medium text-ink-3 block mb-1">Ad Soyad</label>
                      <input
                        type="text"
                        value={editDraft.displayName || ''}
                        onChange={(e) => handleFormChange('displayName', e.target.value)}
                        className="w-full h-9 px-3 text-[13.5px] rounded-lg border border-line bg-surface-1 focus:bg-white"
                      />
                    </div>
                    <div>
                      <label className="text-[12px] font-medium text-ink-3 block mb-1">E-posta</label>
                      <input
                        type="email"
                        value={editDraft.email || ''}
                        onChange={(e) => handleFormChange('email', e.target.value)}
                        className="w-full h-9 px-3 text-[13.5px] rounded-lg border border-line bg-surface-1 focus:bg-white"
                      />
                    </div>
                    <div>
                      <label className="text-[12px] font-medium text-ink-3 block mb-1">Öğrenci Numarası</label>
                      <input
                        type="text"
                        value={editDraft.studentNumber || ''}
                        onChange={(e) => handleFormChange('studentNumber', e.target.value)}
                        className="w-full h-9 px-3 text-[13.5px] rounded-lg border border-line bg-surface-1 focus:bg-white"
                      />
                    </div>
                    <div>
                      <label className="text-[12px] font-medium text-ink-3 block mb-1">Rol</label>
                      <select
                        value={editDraft.role || 'student'}
                        onChange={(e) => handleFormChange('role', e.target.value)}
                        className="w-full h-9 px-3 text-[13.5px] rounded-lg border border-line bg-surface-1 focus:bg-white"
                      >
                        <option value="student">Öğrenci</option>
                        <option value="admin">Yönetici</option>
                      </select>
                    </div>
                  </div>
                )}

                {ds.id === 'glossary' && (
                  <div className="flex flex-col gap-3">
                    <div>
                      <label className="text-[12px] font-medium text-ink-3 block mb-1">Terim</label>
                      <input
                        type="text"
                        value={editDraft.term || ''}
                        onChange={(e) => handleFormChange('term', e.target.value)}
                        className="w-full h-9 px-3 text-[13.5px] rounded-lg border border-line bg-surface-1 focus:bg-white"
                      />
                    </div>
                    <div>
                      <label className="text-[12px] font-medium text-ink-3 block mb-1">Kategori</label>
                      <input
                        type="text"
                        value={editDraft.category || ''}
                        onChange={(e) => handleFormChange('category', e.target.value)}
                        className="w-full h-9 px-3 text-[13.5px] rounded-lg border border-line bg-surface-1 focus:bg-white"
                      />
                    </div>
                    <div>
                      <label className="text-[12px] font-medium text-ink-3 block mb-1">Tanım</label>
                      <textarea
                        rows={4}
                        value={editDraft.definition || ''}
                        onChange={(e) => handleFormChange('definition', e.target.value)}
                        className="w-full p-3 text-[13.5px] rounded-lg border border-line bg-surface-1 focus:bg-white"
                      />
                    </div>
                    <div>
                      <label className="text-[12px] font-medium text-ink-3 block mb-1">Klinik Spot (Pearls)</label>
                      <textarea
                        rows={3}
                        value={editDraft.clinicalPearls || ''}
                        onChange={(e) => handleFormChange('clinicalPearls', e.target.value)}
                        className="w-full p-3 text-[13.5px] rounded-lg border border-line bg-surface-1 focus:bg-white"
                      />
                    </div>
                  </div>
                )}

                {ds.id === 'summaries' && (
                  <div className="flex flex-col gap-3">
                    <div>
                      <label className="text-[12px] font-medium text-ink-3 block mb-1">Başlık</label>
                      <input
                        type="text"
                        value={editDraft.title || ''}
                        onChange={(e) => handleFormChange('title', e.target.value)}
                        className="w-full h-9 px-3 text-[13.5px] rounded-lg border border-line bg-surface-1 focus:bg-white"
                      />
                    </div>
                    <div>
                      <label className="text-[12px] font-medium text-ink-3 block mb-1">Ders / Branş</label>
                      <input
                        type="text"
                        value={editDraft.discipline || ''}
                        onChange={(e) => handleFormChange('discipline', e.target.value)}
                        className="w-full h-9 px-3 text-[13.5px] rounded-lg border border-line bg-surface-1 focus:bg-white"
                      />
                    </div>
                    <div>
                      <label className="text-[12px] font-medium text-ink-3 block mb-1">Kurul</label>
                      <input
                        type="number"
                        value={editDraft.kurul || ''}
                        onChange={(e) => handleFormChange('kurul', Number(e.target.value))}
                        className="w-full h-9 px-3 text-[13.5px] rounded-lg border border-line bg-surface-1 focus:bg-white"
                      />
                    </div>
                    <div>
                      <label className="text-[12px] font-medium text-ink-3 block mb-1">Dosya Adı</label>
                      <input
                        type="text"
                        value={editDraft.fileName || ''}
                        onChange={(e) => handleFormChange('fileName', e.target.value)}
                        className="w-full h-9 px-3 text-[13.5px] rounded-lg border border-line bg-surface-1 focus:bg-white"
                      />
                    </div>
                  </div>
                )}

                {ds.id === 'decks' && (
                  <div className="flex flex-col gap-3">
                    <div>
                      <label className="text-[12px] font-medium text-ink-3 block mb-1">Ders Başlığı</label>
                      <input
                        type="text"
                        value={editDraft.title || ''}
                        onChange={(e) => handleFormChange('title', e.target.value)}
                        className="w-full h-9 px-3 text-[13.5px] rounded-lg border border-line bg-surface-1 focus:bg-white"
                      />
                    </div>
                    <div>
                      <label className="text-[12px] font-medium text-ink-3 block mb-1">Branş</label>
                      <input
                        type="text"
                        value={editDraft.discipline || ''}
                        onChange={(e) => handleFormChange('discipline', e.target.value)}
                        className="w-full h-9 px-3 text-[13.5px] rounded-lg border border-line bg-surface-1 focus:bg-white"
                      />
                    </div>
                    <div>
                      <label className="text-[12px] font-medium text-ink-3 block mb-1">Öğretim Üyesi (Hoca)</label>
                      <input
                        type="text"
                        value={editDraft.instructor || ''}
                        onChange={(e) => handleFormChange('instructor', e.target.value)}
                        className="w-full h-9 px-3 text-[13.5px] rounded-lg border border-line bg-surface-1 focus:bg-white"
                      />
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </Drawer>

      {wizardQuestion && (
        <AdminEditQuestionModal
          isOpen
          question={wizardQuestion}
          adminEmail={adminEmail}
          onClose={() => setWizardQuestion(null)}
          onSaveQuestion={async (updated) => {
            const id = wizardQuestion.id;
            await ApiService.adminUpdateQuestion(adminEmail, id, updated);
            setWizardQuestion(null);
            toast.success('Soru güncellendi');
            await onRefreshData();
            if (openRow && ds.idOf(openRow) === id) {
              setEditDraft((prev) => ({ ...prev, ...updated }));
              setJsonText(JSON.stringify({ ...openRow, ...updated }, null, 2));
            }
          }}
        />
      )}
    </div>
  );
};
