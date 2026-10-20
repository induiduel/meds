import React, { useState, useEffect, useMemo, useRef } from 'react';
import { confirmText } from '../ui/ConfirmDialog';
import {
  Brain,
  Sparkles,
  Upload,
  CheckCircle2,
  Clock,
  Trash2,
  Edit3,
  GitCompare,
  Database,
  Layers,
  FileText,
  Search,
  RefreshCw,
  ChevronRight,
  ChevronLeft,
  Eye,
  Code,
  AlertTriangle,
  FolderOpen,
  X,
  Plus,
  Table,
  GraduationCap,
} from 'lucide-react';
import { toast } from '../ui/Toast';
import { FlatfileDataOnboarding } from './FlatfileDataOnboarding';
import { getCustomApiUrl } from '../../services/api';
import { Drawer } from './consoleUi';
import { DataTable, DetailNav, PageActions, Pill, SearchField, StatRow, Tabs14, Toolbar } from '../v14/pageKit';
import { BulkBar, useSelection } from '../v14/manageKit';
import { ADMIN_EMAIL } from '../../services/auth';
/** NotebookLM uçları: Ayarlar'daki/canlı API tabanını kullanır ve yönetici başlığını ekler (ham fetch ikisini de atlıyordu). */
const nlmFetch = (url: string, init: RequestInit = {}) => {
  const base = (getCustomApiUrl() || '').replace(/\/$/, '');
  const headers = new Headers(init.headers);
  headers.set('x-admin-email', ADMIN_EMAIL);
  return fetch(`${base}${url}`, { ...init, headers });
};


export interface NotebookLMItem {
  id: string;
  title: string;
  type: string;
  status: 'alternative' | 'active' | 'archived';
  targetId?: string;
  originalSnapshot?: any;
  proposedData: any;
  notes?: string;
  ragOptimized: boolean;
  itemCount: number;
  createdAt: string;
  updatedAt: string;
}

const TYPE_LABELS: Record<string, { label: string; color: string; icon: React.ElementType }> = {
  past_question_correction: { label: 'Çıkmış Soru Düzeltmesi', color: 'bg-warn/10 text-warn border-warn/20', icon: CheckCircle2 },
  interactive_deck: { label: 'İnteraktif Öğrenme Destesi', color: 'bg-ai/10 text-ai border-ai/20', icon: Layers },
  spot_pearls: { label: 'Spot Bilgiler & Özet', color: 'bg-accent/10 text-accent border-accent/20', icon: Sparkles },
  practice_questions: { label: 'Örnek Sorular', color: 'bg-ok/10 text-ok border-ok/20', icon: FileText },
  glossary_terms: { label: 'Tıbbi Terimler Sözlüğü', color: 'bg-accent/10 text-accent border-accent/20', icon: Database },
  flashcards: { label: 'Akıl Kartları (Flashcards)', color: 'bg-bad/10 text-bad-text border-bad/20', icon: Brain },
  raw_json: { label: 'Genel JSON Paketi', color: 'bg-ink-3/10 text-ink-3 border-line-2/20', icon: FileText },
};

function cleanQid(id: any): string {
  if (!id) return '';
  return String(id).replace(/^q:/i, '').trim();
}

function extractQuestionsList(proposedData: any): any[] {
  if (!proposedData) return [];
  if (Array.isArray(proposedData)) return proposedData;
  if (Array.isArray(proposedData.questions)) return proposedData.questions;
  if (proposedData.stem || proposedData.question) return [proposedData];
  return [];
}

function resolveOriginalQuestion(originalSnapshot: any, proposedQ: any, _index: number): any {
  if (!originalSnapshot || !proposedQ) return null;

  // Single question snapshot
  if (originalSnapshot.stem && !originalSnapshot.questions) {
    const rawId = proposedQ.id ? String(proposedQ.id).trim() : '';
    const cId = cleanQid(rawId);
    if (cId && originalSnapshot.id && cleanQid(originalSnapshot.id) !== cId) {
      return null;
    }
    return originalSnapshot;
  }

  const rawId = proposedQ.id ? String(proposedQ.id).trim() : '';
  const cId = cleanQid(rawId);

  // If dictionary of questions
  if (typeof originalSnapshot === 'object' && !Array.isArray(originalSnapshot)) {
    if (cId && originalSnapshot[cId]) return originalSnapshot[cId];
    if (rawId && originalSnapshot[rawId]) return originalSnapshot[rawId];

    const vals = Object.values(originalSnapshot) as any[];
    if (cId) {
      const match = vals.find((q) => q && cleanQid(q.id) === cId);
      if (match) return match;
      // If question has an ID that was not found, it is a brand new question!
      return null;
    }

    if (proposedQ.questionNumber && proposedQ.kurul) {
      const match = vals.find(
        (q) => q && String(q.kurul) === String(proposedQ.kurul) && Number(q.questionNumber) === Number(proposedQ.questionNumber)
      );
      if (match) return match;
    }
  }

  // If array of questions
  if (Array.isArray(originalSnapshot)) {
    if (cId) {
      const match = originalSnapshot.find((q) => q && cleanQid(q.id) === cId);
      if (match) return match;
      // If question has an ID that was not found, it is a brand new question!
      return null;
    }

    if (proposedQ.questionNumber && proposedQ.kurul) {
      const match = originalSnapshot.find(
        (q) => q && String(q.kurul) === String(proposedQ.kurul) && Number(q.questionNumber) === Number(proposedQ.questionNumber)
      );
      if (match) return match;
    }
  }

  return null;
}

function normalizeOptionsList(options: any, correctAnswer?: string): Array<{ key: string; text: string; isCorrect: boolean }> {
  if (!options) return [];
  const targetAns = (correctAnswer || '').trim().toUpperCase();
  const keys = ['A', 'B', 'C', 'D', 'E'];

  if (Array.isArray(options)) {
    return options.map((opt, idx) => {
      const fallbackKey = keys[idx] || String(idx + 1);
      if (typeof opt === 'string') {
        const match = opt.match(/^\s*([A-Ea-e])[\).\s:-]+(.*)$/);
        const key = match ? match[1].toUpperCase() : fallbackKey;
        const text = match ? match[2].trim() : opt.trim();
        return { key, text, isCorrect: key === targetAns };
      }
      const key = String(opt.key || opt.label || fallbackKey).toUpperCase();
      const text = String(opt.text || opt.content || '');
      const isCorrect = opt.isCorrect !== undefined ? Boolean(opt.isCorrect) : key === targetAns;
      return { key, text, isCorrect };
    });
  }

  if (typeof options === 'object') {
    return keys
      .filter((k) => options[k] !== undefined || options[k.toLowerCase()] !== undefined)
      .map((k) => {
        const text = String(options[k] ?? options[k.toLowerCase()] ?? '');
        return { key: k, text, isCorrect: k === targetAns };
      });
  }

  return [];
}

export const ManageNotebookLMSection: React.FC = () => {
  const [items, setItems] = useState<NotebookLMItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'all' | 'active' | 'alternative' | 'questions' | 'decks' | 'summaries'>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const picked = useSelection<string>();
  const [bulkBusy, setBulkBusy] = useState(false);

  // Upload & Editor state
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [showOnboardingModal, setShowOnboardingModal] = useState(false);
  const [inputTitle, setInputTitle] = useState('');
  const [inputText, setInputText] = useState('');
  const [inputNotes, setInputNotes] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [uploadedFileName, setUploadedFileName] = useState<string>('');
  const [uploadedFileSize, setUploadedFileSize] = useState<string>('');
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleOnboardingComplete = async (
    questions: any[],
    meta: { title: string; count: number; validCount: number }
  ) => {
    try {
      const res = await nlmFetch('/api/notebooklm/manage/stage', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          payload: {
            type: 'past_question_correction',
            questions
          },
          title: meta.title,
          notes: `Flatfile Data Onboarding ile yüklendi (${meta.validCount} geçerli soru)`
        })
      });
      const data = await res.json();
      if (data.success) {
        toast.success(data.message || `${questions.length} soru Flatfile ile başarıyla aktarıldı.`);
        setShowOnboardingModal(false);
        await fetchItems();
      } else {
        toast.error(data.message || 'Onboarding aktarımı başarısız.');
      }
    } catch (err: any) {
      toast.error('Bağlantı hatası: ' + err.message);
    }
  };

  // Compare & Edit modal state
  const [selectedItemForDiff, setSelectedItemForDiff] = useState<NotebookLMItem | null>(null);
  const [diffIndex, setDiffIndex] = useState(0);
  const [diffMode, setDiffMode] = useState<'ui' | 'json'>('ui');
  const [editingItem, setEditingItem] = useState<NotebookLMItem | null>(null);
  const [editJsonText, setEditJsonText] = useState('');

  const handleFileProcess = (file: File) => {
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
      const content = (e.target?.result as string) || '';
      setInputText(content);
      setUploadedFileName(file.name);
      const sizeKB = (file.size / 1024).toFixed(1);
      setUploadedFileSize(`${sizeKB} KB`);

      if (!inputTitle.trim()) {
        const cleanName = file.name
          .replace(/\.[^/.]+$/, '')
          .replace(/[_-]/g, ' ')
          .replace(/\b\w/g, (c) => c.toUpperCase());
        setInputTitle(cleanName);
      }
      toast.success(`"${file.name}" yüklendi (${sizeKB} KB).`);
    };
    reader.onerror = () => {
      toast.error('Dosya okunamadı!');
    };
    reader.readAsText(file, 'UTF-8');
  };

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFileProcess(file);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    const file = e.dataTransfer.files?.[0];
    if (file) {
      handleFileProcess(file);
    }
  };

  const handleClearFile = () => {
    setUploadedFileName('');
    setUploadedFileSize('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const openDiff = (item: NotebookLMItem) => {
    setSelectedItemForDiff(item);
    setDiffIndex(0);
    setDiffMode('ui');
  };

  const fetchItems = async () => {
    setLoading(true);
    try {
      const res = await nlmFetch('/api/notebooklm/manage/contributions');
      const data = await res.json();
      setItems(data.contributions || []);
    } catch (err: any) {
      toast.error('Veriler alınamadı: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchItems();
  }, []);

  // Format detector for live paste preview
  const detectedFormat = useMemo(() => {
    if (!inputText.trim()) return null;
    try {
      let raw = inputText.trim();
      const codeMatch = raw.match(/```(?:json)?\s*([\s\S]*?)\s*```/);
      if (codeMatch) raw = codeMatch[1];
      const parsed = JSON.parse(raw);

      let type = parsed.type;
      if (!type) {
        if (Array.isArray(parsed)) {
          if (parsed.length > 0 && (parsed[0].stem || parsed[0].question || parsed[0].options || parsed[0].reconstruction)) {
            type = 'past_question_correction';
          } else if (parsed.length > 0 && parsed[0].front && parsed[0].back) {
            type = 'flashcards';
          } else if (parsed.length > 0 && parsed[0].term && parsed[0].definition) {
            type = 'glossary_terms';
          }
        } else if (typeof parsed === 'object' && parsed !== null) {
          if (parsed.questions || parsed.corrections || parsed.stem || parsed.reconstruction || (parsed.options && Array.isArray(parsed.options))) {
            type = 'past_question_correction';
          } else if (parsed.slides || parsed.deckId || parsed.deck) {
            type = 'interactive_deck';
          } else if (parsed.keyPoints || parsed.highYieldPearls) {
            type = 'spot_pearls';
          } else if (parsed.terms || parsed.thesaurus) {
            type = 'glossary_terms';
          } else if (parsed.cards) {
            type = 'flashcards';
          }
        }
      }
      type = type || 'raw_json';

      let count = 1;
      if (Array.isArray(parsed)) count = parsed.length;
      else if (Array.isArray(parsed.questions)) count = parsed.questions.length;
      else if (Array.isArray(parsed.slides)) count = parsed.slides.length;
      else if (parsed.deck && Array.isArray(parsed.deck.slides)) count = parsed.deck.slides.length;
      else if (Array.isArray(parsed.terms)) count = parsed.terms.length;
      else if (Array.isArray(parsed.cards)) count = parsed.cards.length;
      else if (Array.isArray(parsed.keyPoints)) count = parsed.keyPoints.length;

      return {
        type,
        valid: true,
        count
      };
    } catch {
      return { valid: false, count: 0, type: 'error' };
    }
  }, [inputText]);

  // Stage upload
  const handleStageSubmit = async () => {
    if (!inputText.trim()) {
      toast.info('Lütfen JSON veya Markdown metni girin.');
      return;
    }
    setSubmitting(true);
    try {
      const res = await nlmFetch('/api/notebooklm/manage/stage', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          payload: inputText,
          title: inputTitle.trim() || undefined,
          notes: inputNotes.trim() || undefined
        })
      });
      const data = await res.json();
      if (data.success) {
        toast.success(data.message);
        setShowUploadModal(false);
        setInputText('');
        setInputTitle('');
        setInputNotes('');
        setUploadedFileName('');
        setUploadedFileSize('');
        if (fileInputRef.current) fileInputRef.current.value = '';
        await fetchItems();
      } else {
        toast.error(data.message || 'Yükleme başarısız.');
      }
    } catch (err: any) {
      toast.error('Bağlantı hatası: ' + err.message);
    } finally {
      setSubmitting(false);
    }
  };

  // Activate / Choose alternative
  const handleActivate = async (item: NotebookLMItem) => {
    try {
      const res = await nlmFetch(`/api/notebooklm/manage/activate/${item.id}`, { method: 'POST' });
      const data = await res.json();
      if (data.success) {
        toast.success(data.message);
        await fetchItems();
      } else {
        toast.error(data.message);
      }
    } catch (err: any) {
      toast.error('Hata: ' + err.message);
    }
  };

  // Deactivate / Rollback to original
  const handleDeactivate = async (item: NotebookLMItem) => {
    try {
      const res = await nlmFetch(`/api/notebooklm/manage/deactivate/${item.id}`, { method: 'POST' });
      const data = await res.json();
      if (data.success) {
        toast.success(data.message);
        await fetchItems();
      } else {
        toast.error(data.message);
      }
    } catch (err: any) {
      toast.error('Hata: ' + err.message);
    }
  };

  // Delete contribution
  const handleDelete = async (item: NotebookLMItem) => {
    if (!(await confirmText(`"${item.title}" kaydını silmek istediğinize emin misiniz?`))) return false;
    try {
      const res = await nlmFetch(`/api/notebooklm/manage/contribution/${item.id}`, { method: 'DELETE' });
      const data = await res.json();
      if (data.success) {
        toast.success(data.message);
        await fetchItems();
        return true;
      }
      toast.error(data.message);
    } catch (err: any) {
      toast.error('Silinemedi: ' + err.message);
    }
    return false;
  };

  // Save edited contribution
  const handleSaveEdit = async () => {
    if (!editingItem) return;
    try {
      const parsed = JSON.parse(editJsonText);
      const res = await nlmFetch(`/api/notebooklm/manage/contribution/${editingItem.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ proposedData: parsed })
      });
      const data = await res.json();
      if (data.success) {
        toast.success('Güncelleme kaydedildi.');
        setEditingItem(null);
        await fetchItems();
      } else {
        toast.error(data.message);
      }
    } catch (err: any) {
      toast.error('Geçersiz JSON formatı: ' + err.message);
    }
  };

  const filteredItems = useMemo(() => {
    return items.filter((item) => {
      // Tab filter
      if (activeTab === 'active' && item.status !== 'active') return false;
      if (activeTab === 'alternative' && item.status !== 'alternative') return false;
      if (activeTab === 'questions' && item.type !== 'past_question_correction') return false;
      if (activeTab === 'decks' && item.type !== 'interactive_deck') return false;
      if (activeTab === 'summaries' && item.type !== 'spot_pearls') return false;

      // Search filter
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const matchTitle = item.title.toLowerCase().includes(q);
        const matchTarget = item.targetId?.toLowerCase().includes(q);
        const matchType = item.type.toLowerCase().includes(q);
        return matchTitle || matchTarget || matchType;
      }
      return true;
    });
  }, [items, activeTab, searchQuery]);

  const stats = useMemo(() => {
    return {
      total: items.length,
      active: items.filter((i) => i.status === 'active').length,
      alternative: items.filter((i) => i.status === 'alternative').length,
      rag: items.filter((i) => i.ragOptimized).length,
    };
  }, [items]);

  const isLabel = (s: NotebookLMItem['status']) => (s === 'active' ? 'Etkin' : s === 'archived' ? 'Pasif' : 'Bekliyor');
  const bulkRun = async (fn: (it: NotebookLMItem) => Promise<boolean>) => {
    const hedef = items.filter((it) => picked.has(it.id));
    setBulkBusy(true);
    let ok = 0;
    let bad = 0;
    for (const it of hedef) {
      if (await fn(it).catch(() => false)) ok++;
      else bad++;
    }
    setBulkBusy(false);
    (bad ? toast.error : toast.success)(`${ok} başarılı, ${bad} hata`);
    if (ok) picked.clear();
    await fetchItems();
  };
  const callOk = async (url: string, init?: RequestInit) => {
    const res = await nlmFetch(url, init);
    const data = await res.json().catch(() => ({}));
    return !!data.success;
  };

  return (
    <div className="flex flex-col gap-3 min-w-0">
      <PageActions note="Yüklenen içerik mevcut verinin üzerine yazılmaz; önce alternatif olarak saklanır, siz etkinleştirene kadar ana sistem korunur ve tek tıkla geri dönülebilir.">
        <button type="button" onClick={fetchItems} className="m14-btn ghost" title="Listeyi yenile">
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} /> Yenile
        </button>
        <button type="button" onClick={() => setShowOnboardingModal(true)} className="m14-btn" title="Kolon eşleme ve tablosal doğrulama ile içe aktar">
          <Table className="w-3.5 h-3.5" /> Tablo ile içe aktar
        </button>
        <button type="button" onClick={() => setShowUploadModal(true)} className="m14-btn primary">
          <Upload className="w-4 h-4" /> JSON / MD yükle
        </button>
      </PageActions>

      <StatRow
        stats={[
          { label: 'Katkı', value: stats.total },
          { label: 'Etkin', value: stats.active, tone: 'ok', onClick: () => setActiveTab('active') },
          { label: 'Karşılaştırma bekleyen', value: stats.alternative, tone: stats.alternative ? 'warn' : undefined, onClick: () => setActiveTab('alternative') },
          { label: 'RAG’e entegre', value: stats.rag, tone: 'acc' },
        ]}
      />

      <Toolbar>
        <Tabs14
          label="Katkı süzgeci"
          value={activeTab}
          onChange={setActiveTab}
          options={[
            { id: 'all', label: 'Tümü', n: items.length },
            { id: 'alternative', label: 'Bekleyen', n: stats.alternative },
            { id: 'active', label: 'Etkin', n: stats.active },
            { id: 'questions', label: 'Sorular' },
            { id: 'decks', label: 'Desteler' },
            { id: 'summaries', label: 'Özetler' },
          ]}
        />
        <SearchField value={searchQuery} onChange={setSearchQuery} placeholder="Katkı, kimlik ya da tür ara" label="Katkı ara" />
      </Toolbar>

      <BulkBar
        count={picked.count}
        noun="katkı"
        busy={bulkBusy}
        onClear={picked.clear}
        actions={[
          { label: 'Etkinleştir', kind: 'main', run: () => bulkRun((it) => (it.status === 'active' ? Promise.resolve(true) : callOk(`/api/notebooklm/manage/activate/${it.id}`, { method: 'POST' }))) },
          { label: 'Pasifleştir', run: () => bulkRun((it) => (it.status !== 'active' ? Promise.resolve(true) : callOk(`/api/notebooklm/manage/deactivate/${it.id}`, { method: 'POST' }))) },
          { label: 'Sil', kind: 'danger', confirm: `${picked.count} katkıyı silmeyi onayla`, run: () => bulkRun((it) => callOk(`/api/notebooklm/manage/contribution/${it.id}`, { method: 'DELETE' })) },
        ]}
      />

      <DataTable<NotebookLMItem>
        rows={filteredItems}
        rowKey={(it) => it.id}
        selection={picked}
        onOpen={openDiff}
        activeKey={selectedItemForDiff?.id || null}
        busy={loading}
        minWidth={860}
        empty={
          <div className="flex flex-col items-center gap-2 py-6">
            <span>Henüz kayıtlı bir NotebookLM alternatifi yok.</span>
            <button type="button" onClick={() => setShowUploadModal(true)} className="m14-btn primary">İlk JSON’ı yükle</button>
          </div>
        }
        cols={[
          { key: 'title', label: 'Katkı', main: true, render: (it) => <span title={it.notes || it.title}>{it.title}</span> },
          { key: 'status', label: 'Durum', width: 110, render: (it) => <Pill tone={it.status === 'active' ? 'ok' : it.status === 'archived' ? '' : 'warn'}>{isLabel(it.status)}</Pill> },
          { key: 'type', label: 'Tür', render: (it) => (TYPE_LABELS[it.type] || TYPE_LABELS.raw_json).label },
          { key: 'target', label: 'Hedef', mono: true, render: (it) => <span className="block truncate max-w-[12rem]">{it.targetId || '—'}</span> },
          { key: 'n', label: 'Öge', right: true, render: (it) => it.itemCount },
          { key: 'rag', label: 'RAG', render: (it) => (it.ragOptimized ? <Pill tone="acc">Etkin</Pill> : '—') },
          { key: 'at', label: 'Yüklenme', muted: true, render: (it) => new Date(it.createdAt).toLocaleString('tr-TR') },
        ]}
      />


      {/* Yükleme çalışma alanı */}
      <Drawer
        open={showUploadModal}
        onClose={() => setShowUploadModal(false)}
        title="NotebookLM JSON / çıktı yükleme"
        foot={
          <>
            <button type="button" onClick={() => setShowUploadModal(false)} className="m14-btn ghost">İptal</button>
            <button type="button" onClick={handleStageSubmit} disabled={submitting} className="m14-btn primary">
              <Upload className="w-3.5 h-3.5" />
              {submitting ? 'Kaydediliyor…' : 'Alternatif olarak kaydet'}
            </button>
          </>
        }
      >
            <div className="p-5 flex flex-col gap-4 overflow-y-auto">
              <div className="p-3 bg-primary/5 border border-primary/20 rounded-xl text-xs text-primary flex items-start gap-2">
                <Sparkles className="w-4 h-4 shrink-0 mt-0.5" />
                <div>
                  NotebookLM'den aldığınız <strong>.json</strong>, <strong>.md</strong> veya <strong>.txt</strong> dosyasını doğrudan seçebilir veya içeriğini kopyalayıp yapıştırabilirsiniz. Sistem veriyi otomatik tanıyacak ve güvenli bir <strong>alternatif</strong> olarak kaydedecektir.
                </div>
              </div>

              {/* Hidden file input */}
              <input
                ref={fileInputRef}
                type="file"
                accept=".json,.md,.txt,.jsonl,application/json,text/plain,text/markdown"
                onChange={handleFileInputChange}
                className="hidden"
              />

              {/* File Upload Dropzone / Loaded File Banner */}
              {uploadedFileName ? (
                <div className="flex items-center justify-between p-3.5 bg-ok/10 border border-ok/25 rounded-xl transition-all">
                  <div className="flex items-center gap-3 min-w-0">
                    <div className="p-2.5 rounded-lg bg-ok/20 text-ok shrink-0">
                      <FileText className="w-5 h-5" />
                    </div>
                    <div className="min-w-0">
                      <div className="text-xs font-semibold text-ok truncate flex items-center gap-1.5">
                        <span>{uploadedFileName}</span>
                        <span className="text-2xs px-1.5 py-0.5 rounded bg-ok/20 text-ok font-mono">
                          {uploadedFileSize}
                        </span>
                      </div>
                      <div className="text-2xs text-ok mt-0.5">
                        Dosya içeriği başarıyla okundu ve aşağıdaki metin alanına aktarıldı.
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-2 shrink-0">
                    <button
                      type="button"
                      onClick={() => fileInputRef.current?.click()}
                      className="ms-btn is-xs is-secondary text-xs flex items-center gap-1"
                    >
                      <FolderOpen className="w-3.5 h-3.5" />
                      Farklı Dosya Seç
                    </button>
                    <button
                      type="button"
                      onClick={handleClearFile}
                      className="p-1.5 rounded-md text-ink-3 hover:text-bad-text hover:bg-bad/10 transition-colors"
                      title="Dosya seçimini temizle"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ) : (
                <div
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                  onClick={() => fileInputRef.current?.click()}
                  className={`border-2 border-dashed rounded-xl p-5 text-center cursor-pointer transition-all flex flex-col items-center justify-center gap-2 group ${
                    isDragging
                      ? 'border-primary bg-primary/10 scale-[0.99]'
                      : 'border-border hover:border-primary/60 hover:bg-surface-2/60 bg-surface-1/40'
                  }`}
                >
                  <div className="p-3 rounded-full bg-primary/10 text-primary group-hover:scale-110 transition-transform">
                    <FolderOpen className="w-6 h-6" />
                  </div>
                  <div className="flex flex-col items-center gap-1">
                    <div className="text-xs font-semibold text-ink group-hover:text-primary transition-colors flex items-center gap-1.5">
                      <span>Bilgisayarınızdan Dosya Seçin</span>
                      <span className="text-ink-3 font-normal">veya buraya sürükleyip bırakın</span>
                    </div>
                    <div className="text-2xs text-ink-3">
                      Desteklenen: <strong className="text-ink font-medium">.json</strong>, <strong className="text-ink font-medium">.md</strong>, <strong className="text-ink font-medium">.txt</strong>, <strong className="text-ink font-medium">.jsonl</strong> (Maks: 50MB)
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      fileInputRef.current?.click();
                    }}
                    className="ms-btn is-xs is-secondary text-xs mt-1 pointer-events-none"
                  >
                    <Upload className="w-3 h-3" />
                    Dosya Seç
                  </button>
                </div>
              )}

              <div>
                <label className="text-xs font-semibold text-ink block mb-1">Başlık (İsteğe Bağlı)</label>
                <input
                  type="text"
                  placeholder="Örn: Kurul 1 Patoloji Soru Düzeltmeleri (Boş bırakılırsa dosya adı kullanılır)"
                  value={inputTitle}
                  onChange={(e) => setInputTitle(e.target.value)}
                  className="ms-input text-xs w-full"
                />
              </div>

              <div>
                <div className="flex items-center justify-between mb-1">
                  <label className="text-xs font-semibold text-ink">JSON veya Markdown Metni</label>
                  {detectedFormat && (
                    <span className={`text-2xs px-2 py-0.5 rounded font-medium ${detectedFormat.valid ? 'bg-ok/10 text-ok' : 'bg-bad/10 text-bad-text'}`}>
                      {detectedFormat.valid ? `✓ Algılandı: ${TYPE_LABELS[detectedFormat.type]?.label || detectedFormat.type} (${detectedFormat.count} öge)` : 'Geçersiz JSON formatı'}
                    </span>
                  )}
                </div>
                <textarea
                  rows={10}
                  placeholder={`{\n  "type": "past_question_correction",\n  "questions": [...]\n}`}
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  className="ms-input font-mono text-xs w-full leading-relaxed"
                />
              </div>

              <div>
                <label className="text-xs font-semibold text-ink block mb-1">Notlar / Açıklama</label>
                <input
                  type="text"
                  placeholder="Örn: Robbins 10. baskı sayfa 450 baz alınarak düzeltildi."
                  value={inputNotes}
                  onChange={(e) => setInputNotes(e.target.value)}
                  className="ms-input text-xs w-full"
                />
              </div>

              {/* Shortcut to Flatfile Data Onboarding */}
              <div className="flex items-center justify-between p-3 bg-surface-2/80 rounded-xl border border-border text-xs">
                <span className="text-ink-3">Kolon eşleme ve tablosal doğrulama mı istiyorsunuz?</span>
                <button
                  type="button"
                  onClick={() => {
                    setShowUploadModal(false);
                    setShowOnboardingModal(true);
                  }}
                  className="text-primary hover:underline font-bold flex items-center gap-1.5 cursor-pointer"
                >
                  <Table className="w-3.5 h-3.5" />
                  Flatfile Onboarding Sihirbazını Aç
                </button>
              </div>
            </div>
      </Drawer>

      {/* Tablo ile içe aktarma */}
      <Drawer open={showOnboardingModal} onClose={() => setShowOnboardingModal(false)} wide title="Tablo ile içe aktar">
        <div className="flex flex-col min-h-[70vh]">
          <FlatfileDataOnboarding
            targetMode="notebooklm_alternative"
            onComplete={handleOnboardingComplete}
            onCancel={() => setShowOnboardingModal(false)}
          />
        </div>
      </Drawer>

      {/* Side-by-Side Visual UI Diff Modal */}
      {selectedItemForDiff && (() => {
        const isQuestionType =
          selectedItemForDiff.type === 'past_question_correction' ||
          Boolean(selectedItemForDiff.proposedData?.questions || selectedItemForDiff.proposedData?.stem);

        const qList = extractQuestionsList(selectedItemForDiff.proposedData);
        const safeIndex = Math.min(Math.max(0, diffIndex), Math.max(0, qList.length - 1));
        const propQ = qList[safeIndex] || qList[0];
        const origQ = resolveOriginalQuestion(selectedItemForDiff.originalSnapshot, propQ, safeIndex);

        const propOpts = normalizeOptionsList(propQ?.options, propQ?.correctAnswer);
        const origOpts = normalizeOptionsList(
          origQ?.options || origQ?.reconstruction?.options,
          origQ?.correctAnswer || origQ?.reconstruction?.correctAnswer
        );

        const answerChanged =
          origQ &&
          propQ &&
          origQ.correctAnswer &&
          propQ.correctAnswer &&
          String(origQ.correctAnswer).toUpperCase() !== String(propQ.correctAnswer).toUpperCase();

        return (
          <Drawer
            open
            onClose={() => setSelectedItemForDiff(null)}
            wide
            label="Özgün içerikle karşılaştırma"
            title={selectedItemForDiff.title}
            head={
              <>
                <DetailNav<NotebookLMItem> list={filteredItems} current={selectedItemForDiff} same={(a, b) => a.id === b.id} onGo={openDiff} />
                <button type="button" aria-pressed={diffMode === 'ui'} onClick={() => setDiffMode('ui')} className={`m14-btn ${diffMode === 'ui' ? 'primary' : 'ghost'}`}>
                  <Eye className="w-3.5 h-3.5" /> Görsel
                </button>
                <button type="button" aria-pressed={diffMode === 'json'} onClick={() => setDiffMode('json')} className={`m14-btn ${diffMode === 'json' ? 'primary' : 'ghost'}`}>
                  <Code className="w-3.5 h-3.5" /> Ham JSON
                </button>
              </>
            }
            foot={
              <>
                <span className="text-xs text-ink-3 mr-auto">
                  {selectedItemForDiff.status === 'active' ? 'Bu katkı şu anda canlı veride etkin.' : 'Alternatif havuzunda bekliyor; etkinleştirildiğinde sisteme uygulanır.'}
                </span>
                <button
                  type="button"
                  className="m14-btn ghost"
                  onClick={() => {
                    setEditingItem(selectedItemForDiff);
                    setEditJsonText(JSON.stringify(selectedItemForDiff.proposedData, null, 2));
                  }}
                >
                  <Edit3 className="w-3.5 h-3.5" /> JSON düzenle
                </button>
                <button type="button" className="m14-btn danger" aria-label="Katkıyı sil" onClick={async () => { if (await handleDelete(selectedItemForDiff)) setSelectedItemForDiff(null); }}>
                  <Trash2 className="w-3.5 h-3.5" /> Sil
                </button>
                {selectedItemForDiff.status === 'active' ? (
                  <button type="button" onClick={() => { handleDeactivate(selectedItemForDiff); setSelectedItemForDiff(null); }} className="m14-btn">
                    Orijinal veriye dön
                  </button>
                ) : (
                  <>
                    <button type="button" onClick={() => { handleActivate(selectedItemForDiff); setSelectedItemForDiff(null); }} className="m14-btn">
                      Etkinleştir
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        const it = selectedItemForDiff;
                        const i = filteredItems.findIndex((x) => x.id === it.id);
                        const n = filteredItems.filter((x) => x.id !== it.id)[Math.max(0, i)];
                        handleActivate(it);
                        if (n) openDiff(n);
                        else setSelectedItemForDiff(null);
                      }}
                      className="m14-btn primary"
                    >
                      Etkinleştir ve sonraki
                    </button>
                  </>
                )}
              </>
            }
          >
            <p className="m-0 text-xs text-ink-3 flex flex-wrap items-center gap-1.5">
              {isQuestionType ? `Toplam ${qList.length} soru önerisi · birebir karşılıklı inceleme` : 'Veri paketi görsel incelemesi'}
              {selectedItemForDiff.proposedData?.batch !== undefined && <Pill tone="acc">Batch {selectedItemForDiff.proposedData.batch}</Pill>}
              {selectedItemForDiff.proposedData?.questionRange && <Pill>Sorular: {selectedItemForDiff.proposedData.questionRange}</Pill>}
            </p>

              {/* Multi-Question Navigator Bar (when more than 1 question) */}
              {isQuestionType && qList.length > 1 && diffMode === 'ui' && (
                <div className="flex flex-wrap items-center justify-between px-4 py-2 border-b border-border bg-surface-2/60 gap-2">
                  <div className="flex items-center gap-2">
                    <button
                      type="button"
                      disabled={safeIndex <= 0}
                      onClick={() => setDiffIndex((prev) => Math.max(0, prev - 1))}
                      className="ms-btn is-sm is-ghost text-xs disabled:opacity-30 flex items-center gap-1"
                    >
                      <ChevronLeft className="w-4 h-4" /> Önceki Soru
                    </button>

                    <span className="text-xs font-bold text-ink px-2 py-0.5 bg-card border rounded-md">
                      Soru {safeIndex + 1} / {qList.length}
                    </span>

                    <button
                      type="button"
                      disabled={safeIndex >= qList.length - 1}
                      onClick={() => setDiffIndex((prev) => Math.min(qList.length - 1, prev + 1))}
                      className="ms-btn is-sm is-ghost text-xs disabled:opacity-30 flex items-center gap-1"
                    >
                      Sonraki Soru <ChevronRight className="w-4 h-4" />
                    </button>
                  </div>

                  {/* Quick Jump Pills */}
                  <div className="flex items-center gap-1 overflow-x-auto max-w-full py-1">
                    {qList.map((q, idx) => {
                      const oq = resolveOriginalQuestion(selectedItemForDiff.originalSnapshot, q, idx);
                      const isChg =
                        oq &&
                        q &&
                        oq.correctAnswer &&
                        q.correctAnswer &&
                        String(oq.correctAnswer).toUpperCase() !== String(q.correctAnswer).toUpperCase();
                      const isNew = !oq;
                      const isCur = idx === safeIndex;
                      return (
                        <button
                          key={idx}
                          type="button"
                          onClick={() => setDiffIndex(idx)}
                          className={`px-2 py-0.5 text-2xs rounded-md font-mono font-medium transition shrink-0 relative ${
                            isCur
                              ? 'bg-primary text-white font-bold'
                              : isNew
                                ? 'bg-ok/10 border border-ok/30 text-ok '
                                : 'bg-card border border-border text-ink hover:border-primary/40'
                          }`}
                          title={`Soru ${idx + 1} (${isNew ? 'Yeni Eklenecek Soru' : q.id || 'Mevcut'})`}
                        >
                          #{idx + 1}
                          {isChg && (
                            <span
                              className="absolute -top-0.5 -right-0.5 w-1.5 h-1.5 rounded-full bg-warn"
                              title="Cevap değişikliği var"
                            />
                          )}
                          {isNew && !isCur && (
                            <span
                              className="absolute -top-0.5 -right-0.5 w-1.5 h-1.5 rounded-full bg-ok"
                              title="Yeni soru kaydı"
                            />
                          )}
                        </button>
                      );
                    })}
                  </div>
                </div>
              )}

              {/* Modal Body */}
              <div className="p-3.5 sm:p-4 overflow-y-auto max-h-[72vh] flex-1">
                {diffMode === 'json' ? (
                  /* Raw JSON Diff Mode */
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="flex flex-col gap-2">
                      <div className="flex items-center justify-between text-xs font-bold text-ink-2 pb-1 border-b border-border">
                        <span>Mevcut Sistem Verisi (Orijinal)</span>
                        <span className="text-2xs px-2 py-0.5 rounded bg-surface-2">Mevcut DB</span>
                      </div>
                      <pre className="p-3 bg-surface-2 rounded-lg text-2xs font-mono overflow-x-auto text-ink-2 max-h-[500px]">
                        {JSON.stringify(selectedItemForDiff.originalSnapshot, null, 2) || 'Kayıt bulunamadı'}
                      </pre>
                    </div>

                    <div className="flex flex-col gap-2">
                      <div className="flex items-center justify-between text-xs font-bold text-primary pb-1 border-b border-primary/20">
                        <span>NotebookLM Önerisi (Alternatif)</span>
                        <span className="text-2xs px-2 py-0.5 rounded bg-primary/10 text-primary">NotebookLM</span>
                      </div>
                      <pre className="p-3 bg-primary/5 border border-primary/20 rounded-lg text-2xs font-mono overflow-x-auto text-ink max-h-[500px]">
                        {JSON.stringify(selectedItemForDiff.proposedData, null, 2)}
                      </pre>
                    </div>
                  </div>
                ) : isQuestionType && propQ ? (
                  /* Visual UI Question Comparison Mode */
                  <div className="flex flex-col gap-3">
                    {/* Change alert banner */}
                    {answerChanged && (
                      <div className="flex items-center gap-2 p-3 bg-warn/10 border border-warn/30 rounded-xl text-warn text-xs font-medium">
                        <AlertTriangle className="w-4 h-4 shrink-0 text-warn" />
                        <span>
                          <strong>Cevap Anahtarı Değişikliği:</strong> Orijinal soru cevabı{' '}
                          <strong>{origQ?.correctAnswer}</strong> iken, NotebookLM önerisi bu sorunun doğru cevabını{' '}
                          <strong>{propQ?.correctAnswer}</strong> olarak belirlemiştir.
                        </span>
                      </div>
                    )}

                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 items-start">
                      {/* Left: Original Question UI */}
                      <div className="p-4 bg-surface-1 border border-border rounded-xl flex flex-col gap-3">
                        <div className="flex flex-wrap items-center justify-between gap-2 pb-2 border-b border-border">
                          <div className="flex items-center gap-1.5">
                            <span className="px-2 py-0.5 rounded text-2xs font-bold bg-surface-2 text-ink">
                              Orijinal Soru (Mevcut DB)
                            </span>
                            {origQ?.kurul && (
                              <span className="px-1.5 py-0.5 rounded text-2xs font-medium bg-surface-2 text-ink-3">
                                Kurul {origQ.kurul}
                              </span>
                            )}
                          </div>
                          {origQ?.id && (
                            <code className="text-2xs text-ink-3 bg-surface-2 px-1 py-0.5 rounded">
                              ID: {origQ.id}
                            </code>
                          )}
                        </div>

                        {origQ ? (
                          <>
                            {/* Stem */}
                            <div>
                              <div className="text-2xs font-semibold text-ink-3 uppercase tracking-wider mb-1">
                                Soru Metni
                              </div>
                              <p className="text-xs sm:text-sm text-ink font-medium leading-relaxed bg-card p-3 rounded-lg border border-border">
                                {origQ.stem || origQ.reconstruction?.stem || origQ.question || 'Soru kökü kaydı yok.'}
                              </p>
                            </div>

                            {/* Onculler if any */}
                            {(origQ.oncul_maddeleri || origQ.reconstruction?.oncul_maddeleri) && (
                              <div className="flex flex-col gap-1">
                                <div className="text-2xs font-semibold text-ink-3 uppercase tracking-wider">
                                  Öncül Maddeleri
                                </div>
                                <div className="flex flex-col gap-1 bg-card p-2.5 rounded-lg border border-border">
                                  {(origQ.oncul_maddeleri || origQ.reconstruction?.oncul_maddeleri).map(
                                    (m: string, i: number) => (
                                      <div key={i} className="text-xs text-ink">
                                        {m}
                                      </div>
                                    )
                                  )}
                                </div>
                              </div>
                            )}

                            {/* Options */}
                            <div>
                              <div className="text-2xs font-semibold text-ink-3 uppercase tracking-wider mb-1.5">
                                Seçenekler
                              </div>
                              <div className="flex flex-col gap-1.5">
                                {origOpts.length > 0 ? (
                                  origOpts.map((opt) => {
                                    const isCor =
                                      opt.key ===
                                      String(origQ.correctAnswer || origQ.reconstruction?.correctAnswer).toUpperCase();
                                    return (
                                      <div
                                        key={opt.key}
                                        className={`flex items-start gap-2 p-2 rounded-lg text-xs transition border ${
                                          isCor
                                            ? 'bg-ok/10 border-ok/40 text-ok font-semibold'
                                            : 'bg-card border-border text-ink'
                                        }`}
                                      >
                                        <span
                                          className={`w-5 h-5 rounded flex items-center justify-center shrink-0 text-2xs font-bold ${
                                            isCor ? 'bg-ok text-white' : 'bg-surface-2 text-ink-2'
                                          }`}
                                        >
                                          {opt.key}
                                        </span>
                                        <span className="flex-1 leading-snug pt-0.5">{opt.text}</span>
                                        {isCor && (
                                          <span className="text-2xs px-1.5 py-0.5 rounded bg-ok/20 text-ok shrink-0 font-bold">
                                            ✓ Doğru
                                          </span>
                                        )}
                                      </div>
                                    );
                                  })
                                ) : (
                                  <div className="text-xs text-ink-3 p-2 bg-card rounded border">
                                    Seçenek kaydı bulunmuyor.
                                  </div>
                                )}
                              </div>
                            </div>

                            {/* Explanation */}
                            <div>
                              <div className="text-2xs font-semibold text-ink-3 uppercase tracking-wider mb-1">
                                Açıklama & Fizyopatoloji
                              </div>
                              <div className="text-xs text-ink leading-relaxed bg-card p-3 rounded-lg border border-border whitespace-pre-wrap">
                                {origQ.explanation ||
                                  origQ.tibbi_aciklama ||
                                  origQ.reconstruction?.explanation ||
                                  'Açıklama bulunmuyor.'}
                              </div>
                            </div>

                            {/* Sik Analizi */}
                            {(origQ.sik_analizi || origQ.denetleyiciSurumu?.sik_analizi) && (
                              <div>
                                <div className="text-2xs font-semibold text-ink-3 uppercase tracking-wider mb-1">
                                  Şık Analizi
                                </div>
                                <div className="text-xs text-ink leading-relaxed bg-card p-2.5 rounded-lg border border-border flex flex-col gap-1">
                                  {typeof (origQ.sik_analizi || origQ.denetleyiciSurumu?.sik_analizi) === 'object' ? (
                                    Object.entries(origQ.sik_analizi || origQ.denetleyiciSurumu?.sik_analizi).map(
                                      ([k, val]) => (
                                        <div key={k} className="text-xs border-b border-border/50 pb-1 last:border-none">
                                          <strong className="text-primary">{k})</strong> {String(val)}
                                        </div>
                                      )
                                    )
                                  ) : (
                                    <div className="whitespace-pre-wrap text-xs">
                                      {String(origQ.sik_analizi || origQ.denetleyiciSurumu?.sik_analizi)}
                                    </div>
                                  )}
                                </div>
                              </div>
                            )}
                          </>
                        ) : (
                          <div className="p-8 text-center text-xs text-ink-3 flex flex-col items-center justify-center gap-2.5 bg-card/60 rounded-xl border border-dashed border-border/80 my-auto py-12">
                            <div className="p-2.5 rounded-full bg-ok/10 text-ok ">
                              <Plus className="w-5 h-5" />
                            </div>
                            <div className="font-bold text-ink text-sm">Bu soru veritabanında henüz mevcut değildir.</div>
                            <p className="text-xs text-ink-3 max-w-sm leading-relaxed">
                              Bu kayıt sistemde sıfırdan oluşturulacak <strong>yeni bir çıkmış soru</strong> olarak eklenecektir. Bu alternatifi tercih ettiğinizde otomatik olarak veritabanı kütüğüne işlenecektir.
                            </p>
                            <span className="text-2xs px-2 py-0.5 rounded-full bg-ok/10 text-ok font-semibold border border-ok/20">
                              + Yeni Soru Ekleme Akışı
                            </span>
                          </div>
                        )}
                      </div>

                      {/* Right: NotebookLM Proposed UI */}
                      <div className="p-4 bg-primary/5 border border-primary/20 rounded-xl flex flex-col gap-3">
                        <div className="flex flex-wrap items-center justify-between gap-2 pb-2 border-b border-primary/20">
                          <div className="flex items-center gap-1.5">
                            <span className={`px-2 py-0.5 rounded text-2xs font-bold ${!origQ ? 'bg-ok text-white' : 'bg-primary text-white'}`}>
                              {!origQ ? '+ Yeni Soru Kaydı (Veritabanına Eklenecek)' : 'NotebookLM Önerisi (Alternatif)'}
                            </span>
                            {propQ.kurul && (
                              <span className="px-1.5 py-0.5 rounded text-2xs font-medium bg-primary/10 text-primary">
                                Kurul {propQ.kurul}
                              </span>
                            )}
                          </div>
                          {propQ.id && (
                            <code className="text-2xs text-primary bg-primary/10 px-1 py-0.5 rounded">
                              ID: {propQ.id}
                            </code>
                          )}
                        </div>

                        {/* NotebookLM / Fakülte Müfredat Kazanımı */}
                        {propQ.notebooklm_verisi && (
                          <div className="p-3 bg-ai/10 border border-ai/20 rounded-lg flex flex-col gap-1.5">
                            <div className="text-2xs font-bold text-ai uppercase tracking-wider flex items-center gap-1.5">
                              <GraduationCap className="w-3.5 h-3.5" />
                              Fakülte Müfredat Kazanımı & Künye
                            </div>
                            {propQ.notebooklm_verisi.kazanim && (
                              <p className="text-xs text-ink font-medium leading-relaxed bg-card p-2 rounded border border-ai/20">
                                {propQ.notebooklm_verisi.kazanim}
                              </p>
                            )}
                            <div className="flex flex-wrap items-center gap-1.5 text-2xs">
                              {propQ.notebooklm_verisi.mufredat && (
                                <span className="px-2 py-0.5 rounded bg-card border border-border text-ink-2">
                                  <strong>Müfredat:</strong> {propQ.notebooklm_verisi.mufredat}
                                </span>
                              )}
                              {propQ.notebooklm_verisi.kurul && (
                                <span className="px-2 py-0.5 rounded bg-card border border-border text-ink-2">
                                  <strong>Kurul:</strong> {propQ.notebooklm_verisi.kurul}
                                </span>
                              )}
                              {propQ.notebooklm_verisi.ders && (
                                <span className="px-2 py-0.5 rounded bg-card border border-border text-ink-2">
                                  <strong>Ders:</strong> {propQ.notebooklm_verisi.ders}
                                </span>
                              )}
                              {propQ.notebooklm_verisi.konu && (
                                <span className="px-2 py-0.5 rounded bg-card border border-border text-ink-2">
                                  <strong>Konu:</strong> {propQ.notebooklm_verisi.konu}
                                </span>
                              )}
                            </div>
                          </div>
                        )}

                        {/* Stem */}
                        <div>
                          <div className="text-2xs font-semibold text-primary uppercase tracking-wider mb-1">
                            Önerilen Soru Metni
                          </div>
                          <p className="text-xs sm:text-sm text-ink font-medium leading-relaxed bg-card p-3 rounded-lg border border-primary/20 shadow-2xs">
                            {propQ.stem || propQ.question || 'Soru kökü yok.'}
                          </p>
                        </div>

                        {/* Onculler if any */}
                        {propQ.oncul_maddeleri && propQ.oncul_maddeleri.length > 0 && (
                          <div className="flex flex-col gap-1">
                            <div className="text-2xs font-semibold text-primary uppercase tracking-wider">
                              Öncül Maddeleri
                            </div>
                            <div className="flex flex-col gap-1 bg-card p-2.5 rounded-lg border border-primary/20">
                              {propQ.oncul_maddeleri.map((m: string, i: number) => (
                                <div key={i} className="text-xs text-ink">
                                  {m}
                                </div>
                              ))}
                            </div>
                          </div>
                        )}

                        {/* Options */}
                        <div>
                          <div className="text-2xs font-semibold text-primary uppercase tracking-wider mb-1.5">
                            Seçenekler
                          </div>
                          <div className="flex flex-col gap-1.5">
                            {propOpts.length > 0 ? (
                              propOpts.map((opt) => {
                                const isCor = opt.key === String(propQ.correctAnswer).toUpperCase();
                                return (
                                  <div
                                    key={opt.key}
                                    className={`flex items-start gap-2 p-2 rounded-lg text-xs transition border ${
                                      isCor
                                        ? 'bg-ok/10 border-ok text-ok font-semibold shadow-2xs'
                                        : 'bg-card border-border text-ink'
                                    }`}
                                  >
                                    <span
                                      className={`w-5 h-5 rounded flex items-center justify-center shrink-0 text-2xs font-bold ${
                                        isCor ? 'bg-ok text-white' : 'bg-surface-2 text-ink-2'
                                      }`}
                                    >
                                      {opt.key}
                                    </span>
                                    <span className="flex-1 leading-snug pt-0.5">{opt.text}</span>
                                    {isCor && (
                                      <span className="text-2xs px-1.5 py-0.5 rounded bg-ok/20 text-ok shrink-0 font-bold">
                                        ✓ Doğru Seçenek ({opt.key})
                                      </span>
                                    )}
                                  </div>
                                );
                              })
                            ) : (
                              <div className="text-xs text-ink-3 p-2 bg-card rounded border">Seçenek yok.</div>
                            )}
                          </div>
                        </div>

                        {/* Explanation */}
                        <div>
                          <div className="text-2xs font-semibold text-primary uppercase tracking-wider mb-1">
                            Önerilen Açıklama & Fizyopatoloji
                          </div>
                          <div className="text-xs text-ink leading-relaxed bg-card p-3 rounded-lg border border-primary/20 whitespace-pre-wrap">
                            {propQ.explanation || propQ.tibbi_aciklama || 'Açıklama belirtilmemiş.'}
                          </div>
                        </div>

                        {/* Sik Analizi */}
                        {propQ.sik_analizi && (
                          <div>
                            <div className="text-2xs font-semibold text-primary uppercase tracking-wider mb-1">
                              Şık Analizi & Çürütme
                            </div>
                            <div className="text-xs text-ink leading-relaxed bg-card p-2.5 rounded-lg border border-primary/20 flex flex-col gap-1">
                              {typeof propQ.sik_analizi === 'object' ? (
                                Object.entries(propQ.sik_analizi).map(([k, val]) => (
                                  <div key={k} className="text-xs border-b border-border/50 pb-1 last:border-none">
                                    <strong className="text-ok ">{k})</strong> {String(val)}
                                  </div>
                                ))
                              ) : (
                                <div className="whitespace-pre-wrap text-xs">{String(propQ.sik_analizi)}</div>
                              )}
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                ) : (
                  /* Other types UI view */
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="p-4 bg-surface-1 border rounded-xl flex flex-col gap-2">
                      <div className="text-xs font-bold text-ink-2 pb-1 border-b border-border">Mevcut Veri</div>
                      <pre className="p-3 bg-card rounded-lg text-xs font-mono overflow-auto max-h-[450px]">
                        {JSON.stringify(selectedItemForDiff.originalSnapshot, null, 2) || 'Kayıt bulunamadı'}
                      </pre>
                    </div>
                    <div className="p-4 bg-primary/5 border border-primary/20 rounded-xl flex flex-col gap-2">
                      <div className="text-xs font-bold text-primary pb-1 border-b border-primary/20">
                        NotebookLM Önerisi
                      </div>
                      <pre className="p-3 bg-card rounded-lg text-xs font-mono overflow-auto max-h-[450px]">
                        {JSON.stringify(selectedItemForDiff.proposedData, null, 2)}
                      </pre>
                    </div>
                  </div>
                )}
              </div>
          </Drawer>
        );
      })()}

      {/* JSON düzenleme */}
      <Drawer
        open={!!editingItem}
        onClose={() => setEditingItem(null)}
        title={editingItem ? `JSON düzenle: ${editingItem.title}` : ''}
        foot={
          <>
            <button type="button" onClick={() => setEditingItem(null)} className="m14-btn ghost">İptal</button>
            <button type="button" onClick={handleSaveEdit} className="m14-btn primary">Değişiklikleri kaydet</button>
          </>
        }
      >
        <textarea
          rows={20}
          value={editJsonText}
          onChange={(e) => setEditJsonText(e.target.value)}
          aria-label="Katkı JSON'u"
          className="ms-input font-mono text-xs w-full leading-relaxed"
        />
      </Drawer>
    </div>
  );
};
