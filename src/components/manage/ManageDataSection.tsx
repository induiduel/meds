import React, { useEffect, useMemo, useState } from 'react';
import { Search, ArrowUp, ArrowDown, Columns3, Download, X, Trash2, CheckCircle2, Copy, RefreshCw, ChevronDown, Save, RotateCcw, Sparkles, AlertTriangle, FileJson, User, History, FileText, ArrowRight } from 'lucide-react';
import { Committee, QuestionItem } from '../../types';
import { ApiService, safeJsonFetch } from '../../services/api';
import { toast } from '../ui/Toast';
import { Drawer, ConfirmButton } from './consoleUi';
import { PageActions, Tabs14, SearchField, Toolbar, DataTable, DetailNav, type Col } from '../v14/pageKit';
import { BulkBar, useSelection, JsonView } from '../v14/manageKit';
import { AdminEditQuestionModal } from '../AdminEditQuestionModal';

/**
 * v3 "Tüm veriler": one sortable table for every dataset the site keeps.
 * Pick a dataset, search, sort by any column, hide columns, select rows for bulk actions,
 * open a row for its details, export CSV. Destructive actions ask once, inline.
 */
type DatasetId = 'questions' | 'past' | 'users' | 'decks' | 'glossary' | 'summaries' | 'ornek' | 'cards' | 'interactions' | 'comments' | 'reports';
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

/* Yeniden kurulum (2026-10-11): platformdaki her veri tipi aynı masada. Ağır kaynaklar yalnız seçilince yüklenir. */
const ornekLoaders = import.meta.glob('../../data/ornek_sorular/k[1-6]/k[1-6]-*.json', { import: 'default' }) as Record<string, () => Promise<any>>;
const IX_LABEL: Record<string, string> = {
  micro_quiz: 'Mini soru', cloze_masking: 'Boşluk doldurma', interactive_table: 'Gizli tablo', before_after_slider: 'Karşılaştırma',
  branching_logic: 'Klinik karar', causal_chain: 'Mekanizma zinciri', active_recall: 'Aktif hatırlama', spot_the_lie: 'Tuzak avı',
  swipe_matching: 'Hızlı eşleme', feature_bidding: 'Özellik eşleme', venn_grid: 'Çapraz tablo',
};
const ixSummary = (e: any): string =>
  String(e?.question || e?.prompt || e?.stem || e?.title || e?.sentence || e?.scenario || e?.statement || e?.front || e?.instruction || '').replace(/\s+/g, ' ').trim();
const collectIx = (slide: any): any[] => {
  const out: any[] = [];
  const push = (v: any) => { if (Array.isArray(v)) v.forEach(push); else if (v && typeof v === 'object' && typeof (v.type || v.kind) === 'string') out.push(v); };
  ['interactiveElements', 'elements', 'interaction', 'interactiveElement', 'microQuiz'].forEach((k) => push(slide?.[k]));
  return out;
};
/* Eski ton sınıflarını v14 hap tonuna çevirir */
const Pill: React.FC<{ cls: string; children: React.ReactNode }> = ({ cls, children }) => (
  <span className={`m14-pill ${cls === 'is-ok' ? 'ok' : cls === 'is-warn' ? 'warn' : cls === 'is-accent' ? 'acc' : cls === 'is-bad' ? 'bad' : ''}`}>{children}</span>
);

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
          const { DECK_CATALOG, loadDeckCatalog } = await import('../../data/deckStore');
          await loadDeckCatalog();
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
      {
        id: 'ornek',
        label: 'Örnek sorular',
        load: async () => {
          const files = await Promise.all(Object.values(ornekLoaders).map((l) => l().catch(() => null)));
          const rows: Row[] = [];
          files.forEach((d: any) => (d?.kazanimlar || []).forEach((k: any) => (k.sorular || []).forEach((q: any) =>
            rows.push({ ...q, ders: d.ders, dersId: d.id, kazanimMetin: k.metin }))));
          return rows;
        },
        idOf: (r) => String(r.id),
        defaultSort: { key: 'ders', dir: 1 },
        columns: [
          { key: 'id', label: 'Kimlik', width: '120px', mono: true, value: (r) => r.id || '' },
          { key: 'soru', label: 'Soru', width: 'minmax(0,1fr)', value: (r) => r.soru || '' },
          { key: 'ders', label: 'Ders', width: '170px', value: (r) => r.ders || '' },
          { key: 'kazanim', label: 'Kazanım', width: '80px', mono: true, value: (r) => r.kazanim || 0 },
          { key: 'zorluk', label: 'Zorluk', width: '80px', value: (r) => r.zorluk || '', render: (r) => <Pill cls={r.zorluk === 'zor' ? 'is-warn' : r.zorluk === 'kolay' ? 'is-ok' : 'is-accent'}>{r.zorluk || '—'}</Pill> },
          { key: 'dogru', label: 'Cevap', width: '60px', mono: true, value: (r) => r.dogru || '' },
        ],
      },
      {
        id: 'cards',
        label: 'Kartlar',
        load: async () => {
          const { loadAllDecks } = await import('../../data/deckStore');
          const decks: any[] = await loadAllDecks();
          const rows: Row[] = [];
          decks.forEach((d) => (d.slides || []).forEach((s: any) => (s.flashcards || []).forEach((c: any, i: number) =>
            rows.push({ id: `${d.id}:${s.slideNumber}:${c.id || i}`, front: c.front || c.question || '', back: c.back || c.answer || '', deck: d.shortTitle || d.title, slide: s.slideNumber, category: c.category || '' }))));
          return rows;
        },
        idOf: (r) => r.id,
        defaultSort: { key: 'deck', dir: 1 },
        columns: [
          { key: 'front', label: 'Ön yüz', width: 'minmax(0,1fr)', value: (r) => r.front },
          { key: 'back', label: 'Arka yüz', width: 'minmax(0,1fr)', value: (r) => r.back },
          { key: 'deck', label: 'Deste', width: '180px', value: (r) => r.deck || '' },
          { key: 'slide', label: 'Slayt', width: '60px', mono: true, value: (r) => r.slide || 0 },
          { key: 'category', label: 'Tür', width: '110px', value: (r) => r.category || '' },
        ],
      },
      {
        id: 'interactions',
        label: 'Öğren etkileşimleri',
        load: async () => {
          const { loadAllDecks } = await import('../../data/deckStore');
          const decks: any[] = await loadAllDecks();
          const rows: Row[] = [];
          decks.forEach((d) => (d.slides || []).forEach((s: any) => collectIx(s).forEach((e: any, i: number) => {
            const kind = String(e.type || e.kind);
            rows.push({ id: `${d.id}:${s.slideNumber}:${i}`, kind, kindLabel: IX_LABEL[kind] || kind, summary: ixSummary(e), deck: d.shortTitle || d.title, slide: s.slideNumber });
          })));
          return rows;
        },
        idOf: (r) => r.id,
        defaultSort: { key: 'deck', dir: 1 },
        columns: [
          { key: 'kind', label: 'Tür', width: '150px', value: (r) => r.kindLabel, render: (r) => <Pill cls="is-accent">{r.kindLabel}</Pill> },
          { key: 'summary', label: 'İçerik', width: 'minmax(0,1fr)', value: (r) => r.summary || '' },
          { key: 'deck', label: 'Deste', width: '180px', value: (r) => r.deck || '' },
          { key: 'slide', label: 'Slayt', width: '60px', mono: true, value: (r) => r.slide || 0 },
        ],
      },
      {
        id: 'comments',
        label: 'Yorumlar',
        load: async () => {
          const past: any[] = (await ApiService.getPastQuestions({ includeAmbiguous: true })) || [];
          const rows: Row[] = [];
          [...past, ...(questions as any[])].forEach((q) => (q.comments || []).forEach((c: any, i: number) =>
            rows.push({ id: `${q.id}:${c.id || i}`, text: c.text || '', author: c.author || '', at: c.createdAt || c.timestamp || '', question: stemOf(q), qid: q.id, parent: c.parentId ? 'Yanıt' : 'Yorum' })));
          return rows;
        },
        idOf: (r) => r.id,
        defaultSort: { key: 'at', dir: -1 },
        columns: [
          { key: 'text', label: 'Yorum', width: 'minmax(0,1fr)', value: (r) => r.text },
          { key: 'author', label: 'Yazan', width: '140px', value: (r) => r.author },
          { key: 'parent', label: 'Tür', width: '80px', value: (r) => r.parent, render: (r) => <Pill cls={r.parent === 'Yanıt' ? '' : 'is-accent'}>{r.parent}</Pill> },
          { key: 'question', label: 'Soru', width: '260px', value: (r) => r.question },
          { key: 'at', label: 'Tarih', width: '84px', value: (r) => r.at, render: (r) => fmtDate(r.at) },
        ],
      },
      {
        id: 'reports',
        label: 'Hata bildirimleri',
        load: async () => {
          const past: any[] = (await ApiService.getPastQuestions({ includeAmbiguous: true })) || [];
          const rows: Row[] = [];
          const add = (src: string) => (q: any) => (q.reports || []).forEach((r: any, i: number) =>
            rows.push({ id: r.id || `${q.id}:${i}`, reason: r.reason || '', details: r.details || '', status: r.status || 'pending', by: r.reportedBy || '', at: r.reportedAt || '', question: stemOf(q), qid: q.id, src }));
          past.forEach(add('Çıkmış'));
          (questions as any[]).forEach(add('Havuz'));
          return rows;
        },
        idOf: (r) => String(r.id),
        defaultSort: { key: 'at', dir: -1 },
        columns: [
          { key: 'reason', label: 'Sebep', width: '170px', value: (r) => r.reason },
          { key: 'details', label: 'Ayrıntı', width: 'minmax(0,1fr)', value: (r) => r.details },
          { key: 'status', label: 'Durum', width: '110px', value: (r) => r.status, render: (r) => <Pill cls={r.status === 'pending' ? 'is-warn' : r.status === 'rejected' ? '' : 'is-ok'}>{r.status === 'pending' ? 'Bekliyor' : r.status === 'rejected' ? 'Reddedildi' : 'Çözüldü'}</Pill> },
          { key: 'src', label: 'Kaynak', width: '80px', value: (r) => r.src },
          { key: 'question', label: 'Soru', width: '240px', value: (r) => r.question },
          { key: 'at', label: 'Tarih', width: '84px', value: (r) => r.at, render: (r) => fmtDate(r.at) },
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
  const selection = useSelection<string>();
  const selected = Array.from(selection.sel);
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
  const [editTab, setEditTab] = useState<'form' | 'visual' | 'json' | 'history'>('form');
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
    selection.clear();
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
  const tableCols: Col<Row>[] = cols.map((c) => ({
    key: c.key,
    mono: c.mono,
    right: c.mono && c.key !== 'id',
    main: c.width === 'minmax(0,1fr)',
    width: c.width && c.width !== 'minmax(0,1fr)' ? c.width : undefined,
    label: (
      <button type="button" onClick={() => toggleSort(c.key)} className="inline-flex items-center gap-1 cursor-pointer hover:text-ink" style={{ font: 'inherit', letterSpacing: 'inherit', textTransform: 'inherit', color: sort.key === c.key ? 'var(--color-ink)' : undefined }} aria-sort={sort.key === c.key ? (sort.dir === 1 ? 'ascending' : 'descending') : undefined} aria-label={`${c.label} sütununa göre sırala`}>
        {c.label}
        {sort.key === c.key && (sort.dir === 1 ? <ArrowUp aria-hidden className="w-3 h-3" /> : <ArrowDown aria-hidden className="w-3 h-3" />)}
      </button>
    ),
    render: (r: Row) => (
      <span title={String(c.value(r))}>{c.render ? c.render(r) : c.value(r) || '—'}</span>
    ),
  }));

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
  const saveRow = async (): Promise<boolean> => {
    if (!editDraft || !openRow) return false;
    setSavingRow(true);
    try {
      let payload = editDraft;
      if (editTab === 'json') {
        try {
          payload = JSON.parse(jsonText);
        } catch (e: any) {
          toast.error('Geçersiz JSON', e.message || 'Lütfen JSON sözdizimini düzeltin.');
          setSavingRow(false);
          return false;
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
      } else if (ds.id === 'decks' || ds.id === 'glossary') {
        // Gerçek kayıt: veri kataloğu ucu (izinli alanlar, yedekli atomik yazma). Eskiden yalnız ekrandaki
        // satır değişiyor ama "Kaydedildi" deniyordu — veri hiç yazılmıyordu.
        const entity = ds.id;
        // Sözlük anahtarı kaynakta küçük harfli terimdir; büyük "İ/I" iki biçimde de küçültülmüş olabilir
        // (tr: "i"/"ı", en: "i̇"), bu yüzden adaylar sırayla denenir (eskiden ~115 terim "Terim bulunamadı" veriyordu).
        const raw = String(openRow._key || id);
        const keys = entity === 'glossary'
          ? Array.from(new Set([raw, raw.toLocaleLowerCase('tr'), raw.toLowerCase()]))
          : [id];
        let r: Awaited<ReturnType<typeof safeJsonFetch>> | null = null;
        for (const k of keys) {
          r = await safeJsonFetch(`/api/admin/catalog/${entity}/${encodeURIComponent(k)}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json', 'x-admin-email': adminEmail },
            body: JSON.stringify({ patch: payload }),
          });
          if (r.ok || !/bulunamad/i.test(String((r.data as any)?.error || r.error || ''))) break;
        }
        if (!r?.ok) throw new Error((r?.data as any)?.error || r?.error || 'Sunucu kaydı reddetti');
      } else if (ds.id === 'cards') {
        // Bu tablo destelerin slayt kartlarıdır (deste dosyasının içinde); tek tek düzenleme ucu yok.
        // Eskiden ezber kartları (question_cards) ucuna yanlış kimlikle gidip "Kart bulunamadı" alıyordu.
        throw new Error('Deste kartları buradan düzenlenemez: Öğren destesini düzenleyin ya da Veri kataloğu → Ezber kartları kullanın.');
      } else {
        throw new Error('Bu veri kümesi buradan düzenlenemez. Değerlendirme ve etiket için Veri kataloğunu kullanın.');
      }

      toast.success('Kaydedildi', 'Tüm değişiklikler başarıyla uygulandı.');
      setRows((prev) => prev.map((r) => (ds.idOf(r) === id ? { ...r, ...payload } : r)));
      setEditDraft({ ...payload });
      setJsonText(JSON.stringify(payload, null, 2));
      return true;
    } catch (e: any) {
      toast.error('Kaydedilemedi', e?.message || 'Bilinmeyen bir hata oluştu.');
      return false;
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
      selection.clear();
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
      <PageActions note={`${ds.label}: ${visible.length.toLocaleString('tr-TR')} kayıt`}>
        <button type="button" onClick={() => setColMenu(true)} className="m14-btn">
          <Columns3 aria-hidden /> Sütunları seç
        </button>
        <button type="button" onClick={() => void load()} className="m14-btn" disabled={loading}>
          <RefreshCw aria-hidden className={loading ? 'animate-spin' : ''} /> Yenile
        </button>
        <button type="button" onClick={() => exportCsv(false)} className="m14-btn primary">
          <Download aria-hidden /> CSV indir
        </button>
      </PageActions>

      <Toolbar>
        <Tabs14<DatasetId> label="Veri kümesi" value={dsId} onChange={setDsId} options={DATASETS.map((d) => ({ id: d.id, label: d.label, n: d.id === dsId && !loading ? rows.length : undefined }))} />
      </Toolbar>
      <Toolbar>
        <SearchField value={query} onChange={setQuery} placeholder={`${ds.label} içinde ara`} label={`${ds.label} içinde ara`} />
      </Toolbar>

      <BulkBar
        count={selected.length}
        noun="kayıt"
        busy={busy}
        onClear={selection.clear}
        actions={[
          { label: 'Seçilenleri CSV indir', run: () => exportCsv(true) },
          ...(ds.canVerify ? [{ label: 'Doğrula', kind: 'main' as const, run: () => runBulk('verify', selected) }] : []),
          ...(ds.canDelete ? [{ label: 'Sil', kind: 'danger' as const, confirm: `Emin misin? ${selected.length} kaydı sil`, run: () => runBulk('delete', selected) }] : []),
        ]}
      />

      {loading && rows.length === 0 ? (
        <div className="p-3 flex flex-col gap-2" role="status" aria-label="Yükleniyor">
          {[0, 1, 2, 3, 4].map((i) => <div key={i} className="h-8 rounded-lg ms-shimmer" />)}
        </div>
      ) : (
        <DataTable<Row>
          rows={shown}
          cols={tableCols}
          rowKey={ds.idOf}
          onOpen={(r) => setOpenId(ds.idOf(r))}
          selection={selection}
          activeKey={openId}
          busy={loading}
          minWidth={760}
          empty={query ? 'Aramaya uyan kayıt yok' : 'Bu kümede kayıt yok'}
        />
      )}
      {visible.length > limit && (
        <button type="button" onClick={() => setLimit((n) => n + 200)} className="m14-btn ghost self-center">
          <ChevronDown aria-hidden className="w-4 h-4" />
          {(visible.length - limit).toLocaleString('tr-TR')} kayıt daha
        </button>
      )}

      <Drawer open={colMenu} onClose={() => setColMenu(false)} title="Sütunları seç" foot={<button type="button" className="m14-btn primary" onClick={() => setColMenu(false)}>Bitti</button>}>
        <div className="flex flex-col gap-2">
          {ds.columns.map((c) => (
            <label key={c.key} className="ms-menu-item">
              <input type="checkbox" checked={!hidden[c.key]} onChange={() => setHidden((h) => ({ ...h, [c.key]: !h[c.key] }))} />
              {c.label}
            </label>
          ))}
        </div>
      </Drawer>

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
              <span className="text-xs px-2 py-0.5 rounded-full bg-accent-soft text-accent font-medium shrink-0">
                {ds.label}
              </span>
            </div>
          ) : ''
        }
        head={
          <>
            <DetailNav list={visible} current={openRow || null} same={(x, y) => ds.idOf(x) === ds.idOf(y)} onGo={(r) => setOpenId(ds.idOf(r))} />
            <Tabs14<'form' | 'visual' | 'history' | 'json'>
              label="Kayıt görünümü"
              value={editTab}
              onChange={(v) => {
                if ((v === 'form' || v === 'json') && editDraft) setJsonText(JSON.stringify(editDraft, null, 2));
                setEditTab(v);
              }}
              options={[
                { id: 'form', label: 'Form' },
                { id: 'visual', label: 'Görsel' },
                ...(ds.id === 'questions' || ds.id === 'past'
                  ? [{ id: 'history' as const, label: 'Geçmiş ve katkılar', n: (openRow?.revisions?.length || 0) + (openRow?.fragments?.length || 0) || undefined }]
                  : []),
                { id: 'json', label: 'Ham JSON' },
              ]}
            />
          </>
        }
        foot={
          openRow && editDraft && (
            <div className="flex flex-wrap items-center justify-between gap-2 w-full">
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  disabled={savingRow}
                  onClick={() => void saveRow()}
                  className="m14-btn"
                >
                  <Save aria-hidden className={`w-4 h-4 ${savingRow ? 'animate-spin' : ''}`} />
                  {savingRow ? 'Kaydediliyor…' : 'Kaydet'}
                </button>
                {visible.length > 1 && (
                  <button
                    type="button"
                    disabled={savingRow}
                    onClick={async () => {
                      const i = visible.findIndex((r) => ds.idOf(r) === ds.idOf(openRow));
                      if (!(await saveRow())) return;
                      const next = visible[(i + 1) % visible.length];
                      if (next) setOpenId(ds.idOf(next));
                    }}
                    className="m14-btn primary"
                  >
                    Kaydet ve sonraki
                  </button>
                )}
                <button
                  type="button"
                  disabled={savingRow}
                  onClick={handleResetDraft}
                  className="m14-btn ghost"
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
                    className="ms-btn is-ghost text-accent hover:bg-accent-soft text-sm"
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
                  className="m14-btn ghost"
                  title="JSON kopyala"
                  aria-label="JSON kopyala"
                >
                  <Copy className="w-3.5 h-3.5" />
                </button>
                {ds.canVerify && openRow.status !== 'completed' && (
                  <button
                    type="button"
                    disabled={busy}
                    onClick={() => void runBulk('verify', [ds.idOf(openRow)])}
                    className="ms-btn is-sm is-ghost text-ok hover:bg-ok-soft"
                  >
                    <CheckCircle2 className="w-3.5 h-3.5" /> Doğrula
                  </button>
                )}
                {ds.canDelete && (
                  <ConfirmButton
                    icon={Trash2}
                    className="m14-btn danger"
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
            {editTab === 'visual' ? (
              <JsonView value={editDraft} />
            ) : editTab === 'json' ? (
              <div className="flex flex-col gap-2">
                <div className="flex items-center justify-between text-xs text-ink-3 bg-surface-2 p-2.5 rounded-lg border border-line-soft">
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
                  <div className="flex items-start gap-2 p-2.5 rounded-lg bg-bad-soft border border-bad/30 text-bad-text text-xs">
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
                  className={`w-full font-mono text-sm leading-relaxed p-3.5 rounded-lg border bg-surface-1 text-ink focus:bg-white focus:outline-none focus:ring-2 focus:ring-accent ${
                    jsonError ? 'border-bad focus:ring-bad' : 'border-line'
                  }`}
                />
              </div>
            ) : editTab === 'history' ? (
              <div className="flex flex-col gap-4">
                {/* Yazar & Ekleyen Özeti */}
                <div className="p-3.5 rounded-xl border border-line bg-surface-2 flex flex-col gap-2">
                  <div className="text-xs font-bold uppercase tracking-wider text-ink-3">Veri Kaynağı & İlk Ekleyen</div>
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-sm">
                    <div>
                      <span className="text-ink-3 block text-xs">Ekleyen Kullanıcı:</span>
                      <b className="text-ink font-semibold">{editDraft.contributedByName || editDraft.author || '—'}</b>
                    </div>
                    <div>
                      <span className="text-ink-3 block text-xs">Öğrenci No / UID:</span>
                      <span className="font-mono text-ink-2">{editDraft.contributedByStudentNumber || editDraft.contributedByUid || '—'}</span>
                    </div>
                    <div>
                      <span className="text-ink-3 block text-xs">Eklenme Tarihi:</span>
                      <span className="text-ink-2">{fmtDate(editDraft.createdAt || editDraft.updatedAt)}</span>
                    </div>
                  </div>
                  {editDraft.sourceFile && (
                    <div className="text-xs pt-1 border-t border-line-soft text-ink-3">
                      Kaynak Dosya / OCR: <span className="font-mono text-ink-2">{editDraft.sourceFile}</span>
                    </div>
                  )}
                </div>

                {/* Revizyonlar / Düzenleme Geçmişi */}
                <div className="flex flex-col gap-2">
                  <div className="flex items-center justify-between">
                    <h3 className="text-base font-bold text-ink flex items-center gap-2">
                      <History className="w-4 h-4 text-accent" />
                      <span>Düzenleme Geçmişi (Revizyonlar)</span>
                    </h3>
                    <span className="text-xs text-ink-3">{(editDraft.revisions || []).length} versiyon</span>
                  </div>

                  {(!editDraft.revisions || editDraft.revisions.length === 0) ? (
                    <div className="p-4 text-center border border-dashed border-line rounded-xl text-ink-3 text-sm">
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
                                <span className={`text-2xs font-bold px-2 py-0.5 rounded-full ${isLatest ? 'bg-accent text-white' : 'bg-surface-2 text-ink-2'}`}>
                                  v{revNum} {isLatest && '(Son)'}
                                </span>
                                <span className="font-semibold text-sm text-ink">
                                  {rev.changeSummary || 'Düzenleme yapıldı'}
                                </span>
                              </div>
                              <span className="text-xs text-ink-3">{fmtDate(rev.editedAt)}</span>
                            </div>

                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-2 text-xs text-ink-2">
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
                              <div className="mt-2 p-2 rounded-lg bg-surface-2 text-xs text-ink-2 border border-line-soft max-h-24 overflow-y-auto">
                                <div className="text-2xs font-medium text-ink-3 mb-0.5">Bu versiyondaki soru kökü:</div>
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
                    <h3 className="text-base font-bold text-ink flex items-center gap-2">
                      <FileText className="w-4 h-4 text-ok" />
                      <span>Kullanıcı Hafıza Parçaları (Fragments)</span>
                    </h3>
                    <span className="text-xs text-ink-3">{(editDraft.fragments || []).length} parça</span>
                  </div>

                  {(!editDraft.fragments || editDraft.fragments.length === 0) ? (
                    <div className="p-3 text-center border border-dashed border-line rounded-xl text-ink-3 text-sm">
                      Kullanıcılar tarafından eklenmiş hafıza parçası yok.
                    </div>
                  ) : (
                    <div className="flex flex-col gap-2">
                      {editDraft.fragments.map((frag: any, fIdx: number) => (
                        <div key={frag.id || fIdx} className="p-3 rounded-xl border border-line-soft bg-surface-1 flex flex-col gap-1.5 text-sm">
                          <div className="flex items-center justify-between">
                            <span className="font-semibold text-ink flex items-center gap-1.5">
                              <span className="w-2 h-2 rounded-full bg-ok"></span>
                              {frag.author || 'İsimsiz Öğrenci'}
                              {frag.authorStudentNumber && (
                                <span className="font-mono text-ink-3 text-2xs">({frag.authorStudentNumber})</span>
                              )}
                            </span>
                            <span className="text-2xs text-ink-3">{fmtDate(frag.timestamp)}</span>
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
                  <div className="p-2.5 rounded-xl bg-accent-soft/40 border border-accent/20 flex items-center justify-between text-sm">
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
                      className="text-accent hover:underline text-xs font-semibold shrink-0 inline-flex items-center gap-1"
                    >
                      <span>Tüm Geçmiş ({editDraft.revisions?.length || 0})</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </button>
                  </div>
                )}
                {(ds.id === 'questions' || ds.id === 'past') && (
                  <>
                    <div className="flex flex-col gap-1.5">
                      <label className="text-sm font-semibold text-ink flex items-center justify-between">
                        <span>Soru Kökü / Metni</span>
                        <span className="text-xs text-ink-3 font-normal">Markdown formatı geçerlidir</span>
                      </label>
                      <textarea
                        value={stemOf(editDraft)}
                        onChange={(e) => handleQuestionStemChange(e.target.value)}
                        rows={4}
                        placeholder="Soru metnini girin..."
                        className="w-full text-base leading-relaxed p-3 rounded-lg border border-line bg-surface-1 focus:bg-white focus:outline-none focus:ring-2 focus:ring-accent"
                      />
                    </div>

                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
                      <div>
                        <label className="text-xs font-medium text-ink-3 block mb-1">Soru No</label>
                        <input
                          type="number"
                          value={editDraft.questionNumber ?? ''}
                          onChange={(e) => handleFormChange('questionNumber', e.target.value === '' ? 0 : Number(e.target.value))}
                          className="w-full h-9 px-2.5 text-sm rounded-lg border border-line bg-surface-1 focus:bg-white"
                        />
                      </div>
                      <div>
                        <label className="text-xs font-medium text-ink-3 block mb-1">Ders / Branş</label>
                        <input
                          type="text"
                          value={editDraft.discipline || ''}
                          onChange={(e) => handleFormChange('discipline', e.target.value)}
                          placeholder="Örn: Patoloji"
                          className="w-full h-9 px-2.5 text-sm rounded-lg border border-line bg-surface-1 focus:bg-white"
                        />
                      </div>
                      <div>
                        <label className="text-xs font-medium text-ink-3 block mb-1">Konu Başlığı</label>
                        <input
                          type="text"
                          value={editDraft.topic || ''}
                          onChange={(e) => handleFormChange('topic', e.target.value)}
                          placeholder="Örn: Hücre Zedelenmesi"
                          className="w-full h-9 px-2.5 text-sm rounded-lg border border-line bg-surface-1 focus:bg-white"
                        />
                      </div>
                      <div>
                        <label className="text-xs font-medium text-ink-3 block mb-1">Durum</label>
                        <select
                          value={editDraft.status || 'gathering'}
                          onChange={(e) => handleFormChange('status', e.target.value)}
                          className="w-full h-9 px-2 text-sm rounded-lg border border-line bg-surface-1 focus:bg-white"
                        >
                          <option value="completed">Doğrulandı</option>
                          <option value="gathering">Taslak</option>
                          <option value="empty">Boş</option>
                        </select>
                      </div>
                      {ds.id === 'past' && (
                        <>
                          <div>
                            <label className="text-xs font-medium text-ink-3 block mb-1">Sınav Yılı</label>
                            <input
                              type="text"
                              value={editDraft.examYear || ''}
                              onChange={(e) => handleFormChange('examYear', e.target.value)}
                              placeholder="Örn: 2024-2025"
                              className="w-full h-9 px-2.5 text-sm rounded-lg border border-line bg-surface-1 focus:bg-white"
                            />
                          </div>
                          <div>
                            <label className="text-xs font-medium text-ink-3 block mb-1">Kurul Kodu</label>
                            <input
                              type="text"
                              value={editDraft.committeeId || ''}
                              onChange={(e) => handleFormChange('committeeId', e.target.value)}
                              placeholder="Örn: donem3-kurul1"
                              className="w-full h-9 px-2.5 text-sm rounded-lg border border-line bg-surface-1 focus:bg-white"
                            />
                          </div>
                        </>
                      )}
                    </div>

                    <div className="flex flex-col gap-2">
                      <div className="flex items-center justify-between">
                        <label className="text-sm font-semibold text-ink">Şıklar ve Doğru Cevap</label>
                        <span className="text-xs text-ink-3">Doğru şık için harfe tıklayın</span>
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
                              isCorrect ? 'bg-ok-soft/70 border-ok/30' : 'bg-surface-1 border-line-soft'
                            }`}
                          >
                            <button
                              type="button"
                              onClick={() => handleQuestionAnswerChange(letter)}
                              className={`w-7 h-7 rounded-md font-bold text-xs flex items-center justify-center shrink-0 transition-colors ${
                                isCorrect ? 'bg-ok text-white shadow-xs' : 'bg-surface-2 text-ink-3 hover:bg-ok-soft hover:text-ok'
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
                              className="flex-1 min-w-0 bg-transparent text-sm border-none outline-none py-1 text-ink"
                            />
                            {isCorrect && (
                              <span className="text-2xs font-medium text-ok px-1.5 py-0.5 bg-ok-soft/80 rounded shrink-0">
                                Doğru
                              </span>
                            )}
                          </div>
                        );
                      })}
                    </div>

                    <div className="flex flex-col gap-1.5">
                      <label className="text-sm font-semibold text-ink">Çözüm ve Tıbbi Açıklama</label>
                      <textarea
                        value={editDraft.reconstruction?.explanation || editDraft.explanation || editDraft.clinicalExplanation || ''}
                        onChange={(e) => handleQuestionExplanationChange(e.target.value)}
                        rows={4}
                        placeholder="Sorunun ayrıntılı fizyopatolojik gerekçesi ve şık analizleri..."
                        className="w-full text-sm leading-relaxed p-3 rounded-lg border border-line bg-surface-1 focus:bg-white focus:outline-none focus:ring-2 focus:ring-accent"
                      />
                    </div>
                  </>
                )}

                {ds.id === 'users' && (
                  <div className="flex flex-col gap-3">
                    <div>
                      <label className="text-xs font-medium text-ink-3 block mb-1">Ad Soyad</label>
                      <input
                        type="text"
                        value={editDraft.displayName || ''}
                        onChange={(e) => handleFormChange('displayName', e.target.value)}
                        className="w-full h-9 px-3 text-base rounded-lg border border-line bg-surface-1 focus:bg-white"
                      />
                    </div>
                    <div>
                      <label className="text-xs font-medium text-ink-3 block mb-1">E-posta</label>
                      <input
                        type="email"
                        value={editDraft.email || ''}
                        onChange={(e) => handleFormChange('email', e.target.value)}
                        className="w-full h-9 px-3 text-base rounded-lg border border-line bg-surface-1 focus:bg-white"
                      />
                    </div>
                    <div>
                      <label className="text-xs font-medium text-ink-3 block mb-1">Öğrenci Numarası</label>
                      <input
                        type="text"
                        value={editDraft.studentNumber || ''}
                        onChange={(e) => handleFormChange('studentNumber', e.target.value)}
                        className="w-full h-9 px-3 text-base rounded-lg border border-line bg-surface-1 focus:bg-white"
                      />
                    </div>
                    <div>
                      <label className="text-xs font-medium text-ink-3 block mb-1">Rol</label>
                      <select
                        value={editDraft.role || 'student'}
                        onChange={(e) => handleFormChange('role', e.target.value)}
                        className="w-full h-9 px-3 text-base rounded-lg border border-line bg-surface-1 focus:bg-white"
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
                      <label className="text-xs font-medium text-ink-3 block mb-1">Terim</label>
                      <input
                        type="text"
                        value={editDraft.term || ''}
                        onChange={(e) => handleFormChange('term', e.target.value)}
                        className="w-full h-9 px-3 text-base rounded-lg border border-line bg-surface-1 focus:bg-white"
                      />
                    </div>
                    <div>
                      <label className="text-xs font-medium text-ink-3 block mb-1">Kategori</label>
                      <input
                        type="text"
                        value={editDraft.category || ''}
                        onChange={(e) => handleFormChange('category', e.target.value)}
                        className="w-full h-9 px-3 text-base rounded-lg border border-line bg-surface-1 focus:bg-white"
                      />
                    </div>
                    <div>
                      <label className="text-xs font-medium text-ink-3 block mb-1">Tanım</label>
                      <textarea
                        rows={4}
                        value={editDraft.definition || ''}
                        onChange={(e) => handleFormChange('definition', e.target.value)}
                        className="w-full p-3 text-base rounded-lg border border-line bg-surface-1 focus:bg-white"
                      />
                    </div>
                    <div>
                      <label className="text-xs font-medium text-ink-3 block mb-1">Klinik Spot (Pearls)</label>
                      <textarea
                        rows={3}
                        value={editDraft.clinicalPearls || ''}
                        onChange={(e) => handleFormChange('clinicalPearls', e.target.value)}
                        className="w-full p-3 text-base rounded-lg border border-line bg-surface-1 focus:bg-white"
                      />
                    </div>
                  </div>
                )}

                {ds.id === 'summaries' && (
                  <div className="flex flex-col gap-3">
                    <div>
                      <label className="text-xs font-medium text-ink-3 block mb-1">Başlık</label>
                      <input
                        type="text"
                        value={editDraft.title || ''}
                        onChange={(e) => handleFormChange('title', e.target.value)}
                        className="w-full h-9 px-3 text-base rounded-lg border border-line bg-surface-1 focus:bg-white"
                      />
                    </div>
                    <div>
                      <label className="text-xs font-medium text-ink-3 block mb-1">Ders / Branş</label>
                      <input
                        type="text"
                        value={editDraft.discipline || ''}
                        onChange={(e) => handleFormChange('discipline', e.target.value)}
                        className="w-full h-9 px-3 text-base rounded-lg border border-line bg-surface-1 focus:bg-white"
                      />
                    </div>
                    <div>
                      <label className="text-xs font-medium text-ink-3 block mb-1">Kurul</label>
                      <input
                        type="number"
                        value={editDraft.kurul || ''}
                        onChange={(e) => handleFormChange('kurul', Number(e.target.value))}
                        className="w-full h-9 px-3 text-base rounded-lg border border-line bg-surface-1 focus:bg-white"
                      />
                    </div>
                    <div>
                      <label className="text-xs font-medium text-ink-3 block mb-1">Dosya Adı</label>
                      <input
                        type="text"
                        value={editDraft.fileName || ''}
                        onChange={(e) => handleFormChange('fileName', e.target.value)}
                        className="w-full h-9 px-3 text-base rounded-lg border border-line bg-surface-1 focus:bg-white"
                      />
                    </div>
                  </div>
                )}

                {ds.id === 'decks' && (
                  <div className="flex flex-col gap-3">
                    <div>
                      <label className="text-xs font-medium text-ink-3 block mb-1">Ders Başlığı</label>
                      <input
                        type="text"
                        value={editDraft.title || ''}
                        onChange={(e) => handleFormChange('title', e.target.value)}
                        className="w-full h-9 px-3 text-base rounded-lg border border-line bg-surface-1 focus:bg-white"
                      />
                    </div>
                    <div>
                      <label className="text-xs font-medium text-ink-3 block mb-1">Branş</label>
                      <input
                        type="text"
                        value={editDraft.discipline || ''}
                        onChange={(e) => handleFormChange('discipline', e.target.value)}
                        className="w-full h-9 px-3 text-base rounded-lg border border-line bg-surface-1 focus:bg-white"
                      />
                    </div>
                    <div>
                      <label className="text-xs font-medium text-ink-3 block mb-1">Öğretim Üyesi (Hoca)</label>
                      <input
                        type="text"
                        value={editDraft.instructor || ''}
                        onChange={(e) => handleFormChange('instructor', e.target.value)}
                        className="w-full h-9 px-3 text-base rounded-lg border border-line bg-surface-1 focus:bg-white"
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
