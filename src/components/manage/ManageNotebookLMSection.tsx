import React, { useState, useEffect, useMemo } from 'react';
import {
  Brain,
  Sparkles,
  Upload,
  CheckCircle2,
  Clock,
  Trash2,
  Edit3,
  GitCompare,
  ArrowRight,
  Database,
  Layers,
  FileText,
  Search,
  RefreshCw,
  AlertCircle,
  Copy,
  ExternalLink,
  ChevronRight,
  X,
  Plus
} from 'lucide-react';
import { toast } from '../ui/Toast';

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
  past_question_correction: { label: 'Çıkmış Soru Düzeltmesi', color: 'bg-amber-500/10 text-amber-500 border-amber-500/20', icon: CheckCircle2 },
  interactive_deck: { label: 'İnteraktif Öğrenme Destesi', color: 'bg-purple-500/10 text-purple-500 border-purple-500/20', icon: Layers },
  spot_pearls: { label: 'Spot Bilgiler & Özet', color: 'bg-blue-500/10 text-blue-500 border-blue-500/20', icon: Sparkles },
  practice_questions: { label: 'Örnek Sorular', color: 'bg-emerald-500/10 text-emerald-500 border-emerald-500/20', icon: FileText },
  glossary_terms: { label: 'Tıbbi Terimler Sözlüğü', color: 'bg-cyan-500/10 text-cyan-500 border-cyan-500/20', icon: Database },
  flashcards: { label: 'Akıl Kartları (Flashcards)', color: 'bg-rose-500/10 text-rose-500 border-rose-500/20', icon: Brain },
  raw_json: { label: 'Genel JSON Paketi', color: 'bg-slate-500/10 text-slate-500 border-slate-500/20', icon: FileText },
};

export const ManageNotebookLMSection: React.FC = () => {
  const [items, setItems] = useState<NotebookLMItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'all' | 'active' | 'alternative' | 'questions' | 'decks' | 'summaries'>('all');
  const [searchQuery, setSearchQuery] = useState('');

  // Upload & Editor state
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [inputTitle, setInputTitle] = useState('');
  const [inputText, setInputText] = useState('');
  const [inputNotes, setInputNotes] = useState('');
  const [submitting, setSubmitting] = useState(false);

  // Compare & Edit modal state
  const [selectedItemForDiff, setSelectedItemForDiff] = useState<NotebookLMItem | null>(null);
  const [editingItem, setEditingItem] = useState<NotebookLMItem | null>(null);
  const [editJsonText, setEditJsonText] = useState('');

  const fetchItems = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/notebooklm/manage/contributions');
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
      const type = parsed.type || (Array.isArray(parsed) && parsed[0]?.stem ? 'past_question_correction' : 'raw_json');
      return {
        type,
        valid: true,
        count: Array.isArray(parsed) ? parsed.length : Array.isArray(parsed.questions) ? parsed.questions.length : 1
      };
    } catch {
      return { valid: false, count: 0 };
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
      const res = await fetch('/api/notebooklm/manage/stage', {
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
      const res = await fetch(`/api/notebooklm/manage/activate/${item.id}`, { method: 'POST' });
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
      const res = await fetch(`/api/notebooklm/manage/deactivate/${item.id}`, { method: 'POST' });
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
    if (!window.confirm(`"${item.title}" kaydını silmek istediğinize emin misiniz?`)) return;
    try {
      const res = await fetch(`/api/notebooklm/manage/contribution/${item.id}`, { method: 'DELETE' });
      const data = await res.json();
      if (data.success) {
        toast.success(data.message);
        await fetchItems();
      } else {
        toast.error(data.message);
      }
    } catch (err: any) {
      toast.error('Silinemedi: ' + err.message);
    }
  };

  // Save edited contribution
  const handleSaveEdit = async () => {
    if (!editingItem) return;
    try {
      const parsed = JSON.parse(editJsonText);
      const res = await fetch(`/api/notebooklm/manage/contribution/${editingItem.id}`, {
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

  return (
    <div className="flex flex-col gap-5 min-w-0">
      {/* Top Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 p-5 bg-card border border-border rounded-xl">
        <div>
          <div className="flex items-center gap-2 text-primary font-semibold text-xs tracking-wider uppercase mb-1">
            <Brain className="w-4 h-4" />
            <span>NotebookLM &amp; Yapay Zeka Entegrasyonu</span>
          </div>
          <h2 className="text-xl font-bold text-ink">NotebookLM Stüdyosu &amp; Alternatif Seçim Masası</h2>
          <p className="text-xs text-ink-3 mt-1">
            NotebookLM çıktılarını mevcut verileri ezmeden güvenle yükleyin; orijinal ile yan yana karşılaştırıp tercihinizi yapın.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={fetchItems}
            className="ms-btn is-sm is-ghost flex items-center gap-1.5"
            title="Listeyi yenile"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            Yenile
          </button>
          <button
            type="button"
            onClick={() => setShowUploadModal(true)}
            className="ms-btn is-primary flex items-center gap-2 text-sm shadow-sm"
          >
            <Plus className="w-4 h-4" />
            Yeni JSON / Dosya Yükle
          </button>
        </div>
      </div>

      {/* Peace of Mind Callout */}
      <div className="flex items-start gap-3 p-4 bg-emerald-500/5 border border-emerald-500/20 rounded-xl text-xs text-emerald-800 dark:text-emerald-300">
        <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
        <div>
          <strong className="font-semibold">Sıfır Çakışma ve Güvenli Alternatif Garantisi:</strong> Yüklediğiniz hiçbir dosya veya JSON mevcut veritabanınızın üzerine doğrudan yazılmaz. İlk aşamada <em>"Alternatif"</em> olarak depolanır; siz yan yana inceleyip <em>"Tercih Et"</em> butonuna basana kadar ana sistem korunur. Dilediğiniz an tek tıkla orijinal veriye geri dönebilirsiniz.
        </div>
      </div>

      {/* Stats Bar */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <div className="p-3.5 bg-card border border-border rounded-xl flex flex-col gap-0.5">
          <span className="text-xs text-ink-3">Toplam Yüklenen</span>
          <span className="text-xl font-bold text-ink">{stats.total}</span>
        </div>
        <div className="p-3.5 bg-card border border-border rounded-xl flex flex-col gap-0.5">
          <span className="text-xs text-emerald-600 font-medium">Tercih Edilen (Aktif)</span>
          <span className="text-xl font-bold text-emerald-600">{stats.active}</span>
        </div>
        <div className="p-3.5 bg-card border border-border rounded-xl flex flex-col gap-0.5">
          <span className="text-xs text-amber-600 font-medium">Bekleyen Alternatif</span>
          <span className="text-xl font-bold text-amber-600">{stats.alternative}</span>
        </div>
        <div className="p-3.5 bg-card border border-border rounded-xl flex flex-col gap-0.5">
          <span className="text-xs text-blue-600 font-medium">RAG'e Entegre</span>
          <span className="text-xl font-bold text-blue-600">{stats.rag}</span>
        </div>
      </div>

      {/* Filter Tabs & Search */}
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex flex-wrap items-center gap-1.5 p-1 bg-surface-2 border border-border rounded-lg text-xs">
          <button
            type="button"
            onClick={() => setActiveTab('all')}
            className={`px-3 py-1.5 rounded-md font-medium transition ${activeTab === 'all' ? 'bg-card text-ink shadow-xs' : 'text-ink-3 hover:text-ink'}`}
          >
            Tümü ({items.length})
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('active')}
            className={`px-3 py-1.5 rounded-md font-medium transition ${activeTab === 'active' ? 'bg-card text-emerald-600 shadow-xs' : 'text-ink-3 hover:text-ink'}`}
          >
            🟢 Aktifler ({stats.active})
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('alternative')}
            className={`px-3 py-1.5 rounded-md font-medium transition ${activeTab === 'alternative' ? 'bg-card text-amber-600 shadow-xs' : 'text-ink-3 hover:text-ink'}`}
          >
            🟡 Alternatifler ({stats.alternative})
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('questions')}
            className={`px-3 py-1.5 rounded-md font-medium transition ${activeTab === 'questions' ? 'bg-card text-ink shadow-xs' : 'text-ink-3 hover:text-ink'}`}
          >
            Sorular
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('decks')}
            className={`px-3 py-1.5 rounded-md font-medium transition ${activeTab === 'decks' ? 'bg-card text-ink shadow-xs' : 'text-ink-3 hover:text-ink'}`}
          >
            Desteler
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('summaries')}
            className={`px-3 py-1.5 rounded-md font-medium transition ${activeTab === 'summaries' ? 'bg-card text-ink shadow-xs' : 'text-ink-3 hover:text-ink'}`}
          >
            Özetler
          </button>
        </div>

        <div className="relative min-w-[220px]">
          <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-ink-3" />
          <input
            type="text"
            placeholder="Başlık, ID veya tip ara..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="ms-input !pl-8 text-xs !py-1.5 w-full"
          />
        </div>
      </div>

      {/* Contributions List */}
      <div className="flex flex-col gap-3">
        {filteredItems.length === 0 ? (
          <div className="p-12 text-center bg-card border border-border rounded-xl">
            <Brain className="w-10 h-10 mx-auto text-ink-3 mb-3 opacity-40" />
            <h4 className="text-sm font-semibold text-ink">Henüz kayıtlı bir NotebookLM alternatifi yok</h4>
            <p className="text-xs text-ink-3 max-w-md mx-auto mt-1 mb-4">
              NotebookLM'den aldığınız çıktıları yüklemek için "Yeni JSON / Dosya Yükle" butonunu kullanabilirsiniz.
            </p>
            <button
              type="button"
              onClick={() => setShowUploadModal(true)}
              className="ms-btn is-primary is-sm"
            >
              İlk JSON'ı Yükle
            </button>
          </div>
        ) : (
          filteredItems.map((item) => {
            const typeConfig = TYPE_LABELS[item.type] || TYPE_LABELS.raw_json;
            const Icon = typeConfig.icon;
            const isActive = item.status === 'active';

            return (
              <div
                key={item.id}
                className={`p-4 bg-card border rounded-xl transition flex flex-col gap-3 ${
                  isActive ? 'border-emerald-500/40 shadow-xs' : 'border-border'
                }`}
              >
                <div className="flex flex-wrap items-start justify-between gap-3">
                  <div className="flex items-start gap-3">
                    <div className="p-2.5 bg-surface-2 rounded-lg text-ink shrink-0 mt-0.5">
                      <Icon className="w-4 h-4 text-primary" />
                    </div>
                    <div>
                      <div className="flex flex-wrap items-center gap-2">
                        <h4 className="text-sm font-bold text-ink">{item.title}</h4>
                        <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[11px] font-medium border ${typeConfig.color}`}>
                          {typeConfig.label}
                        </span>
                        {isActive ? (
                          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[11px] font-semibold bg-emerald-500/10 text-emerald-600 border border-emerald-500/30">
                            🟢 Tercih Edilen (Aktif)
                          </span>
                        ) : (
                          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[11px] font-semibold bg-amber-500/10 text-amber-600 border border-amber-500/30">
                            🟡 Alternatif (Beklemede)
                          </span>
                        )}
                        {item.ragOptimized && (
                          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[11px] font-semibold bg-blue-500/10 text-blue-600 border border-blue-500/30">
                            RAG Aktif
                          </span>
                        )}
                      </div>

                      <div className="flex flex-wrap items-center gap-3 text-[12px] text-ink-3 mt-1.5">
                        {item.targetId && (
                          <span>Hedef ID: <code className="bg-surface-2 px-1 rounded">{item.targetId}</code></span>
                        )}
                        <span>{item.itemCount} Öge</span>
                        <span>•</span>
                        <span>{new Date(item.createdAt).toLocaleString('tr-TR')}</span>
                        {item.notes && <span>• {item.notes}</span>}
                      </div>
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="flex items-center gap-2">
                    {item.originalSnapshot && (
                      <button
                        type="button"
                        onClick={() => setSelectedItemForDiff(item)}
                        className="ms-btn is-sm is-ghost text-xs flex items-center gap-1"
                      >
                        <GitCompare className="w-3.5 h-3.5 text-blue-500" />
                        Karşılaştır
                      </button>
                    )}

                    <button
                      type="button"
                      onClick={() => {
                        setEditingItem(item);
                        setEditJsonText(JSON.stringify(item.proposedData, null, 2));
                      }}
                      className="ms-btn is-sm is-ghost text-xs flex items-center gap-1"
                      title="JSON'ı düzenle"
                    >
                      <Edit3 className="w-3.5 h-3.5" />
                      Düzenle
                    </button>

                    {isActive ? (
                      <button
                        type="button"
                        onClick={() => handleDeactivate(item)}
                        className="ms-btn is-sm is-outline text-xs text-amber-600 border-amber-500/30 hover:bg-amber-500/10"
                        title="Orijinal veriye geri dön"
                      >
                        Orijinal Veriye Dön
                      </button>
                    ) : (
                      <button
                        type="button"
                        onClick={() => handleActivate(item)}
                        className="ms-btn is-sm is-primary text-xs bg-emerald-600 hover:bg-emerald-700"
                        title="Bu alternatifi sisteme uygula"
                      >
                        Tercih Et (Uygula)
                      </button>
                    )}

                    <button
                      type="button"
                      onClick={() => handleDelete(item)}
                      className="ms-btn is-sm is-ghost text-xs text-red-500 hover:bg-red-500/10"
                      title="Kaydı sil"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>

      {/* Upload & Staging Modal */}
      {showUploadModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs">
          <div className="bg-card border border-border rounded-2xl w-full max-w-2xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-150">
            <div className="flex items-center justify-between p-4 border-b border-border bg-surface-1">
              <div className="flex items-center gap-2">
                <Brain className="w-5 h-5 text-primary" />
                <h3 className="text-base font-bold text-ink">NotebookLM JSON / Çıktı Yükleme</h3>
              </div>
              <button
                type="button"
                onClick={() => setShowUploadModal(false)}
                className="p-1 rounded-lg text-ink-3 hover:text-ink hover:bg-surface-2"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-5 flex flex-col gap-4 overflow-y-auto">
              <div className="p-3 bg-primary/5 border border-primary/20 rounded-xl text-xs text-primary flex items-start gap-2">
                <Sparkles className="w-4 h-4 shrink-0 mt-0.5" />
                <div>
                  NotebookLM'den kopyaladığınız JSON veya Markdown kod bloğunu aşağıya yapıştırın ya da dosya yükleyin. Sistem veriyi otomatik tanıyacak ve güvenli bir <strong>alternatif</strong> olarak kaydedecektir.
                </div>
              </div>

              <div>
                <label className="text-xs font-semibold text-ink block mb-1">Başlık (İsteğe Bağlı)</label>
                <input
                  type="text"
                  placeholder="Örn: Kurul 1 Patoloji Soru Düzeltmeleri"
                  value={inputTitle}
                  onChange={(e) => setInputTitle(e.target.value)}
                  className="ms-input text-xs w-full"
                />
              </div>

              <div>
                <div className="flex items-center justify-between mb-1">
                  <label className="text-xs font-semibold text-ink">JSON veya Markdown Metni</label>
                  {detectedFormat && (
                    <span className={`text-[11px] px-2 py-0.5 rounded font-medium ${detectedFormat.valid ? 'bg-emerald-500/10 text-emerald-600' : 'bg-rose-500/10 text-rose-600'}`}>
                      {detectedFormat.valid ? `✓ Algılandı: ${detectedFormat.type} (${detectedFormat.count} öge)` : 'JSON hatası'}
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
            </div>

            <div className="flex items-center justify-end gap-2 p-4 border-t border-border bg-surface-1">
              <button
                type="button"
                onClick={() => setShowUploadModal(false)}
                className="ms-btn is-sm is-ghost text-xs"
              >
                İptal
              </button>
              <button
                type="button"
                onClick={handleStageSubmit}
                disabled={submitting}
                className="ms-btn is-sm is-primary text-xs flex items-center gap-1.5"
              >
                <Upload className="w-3.5 h-3.5" />
                {submitting ? 'Kaydediliyor...' : 'Alternatif Olarak Güvenle Kaydet'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Side-by-Side Diff Modal */}
      {selectedItemForDiff && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs">
          <div className="bg-card border border-border rounded-2xl w-full max-w-4xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden">
            <div className="flex items-center justify-between p-4 border-b border-border bg-surface-1">
              <div className="flex items-center gap-2">
                <GitCompare className="w-5 h-5 text-blue-500" />
                <h3 className="text-base font-bold text-ink">Yan Yana Karşılaştırma: {selectedItemForDiff.title}</h3>
              </div>
              <button
                type="button"
                onClick={() => setSelectedItemForDiff(null)}
                className="p-1 rounded-lg text-ink-3 hover:text-ink"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-4 grid grid-cols-1 md:grid-cols-2 gap-4 overflow-y-auto max-h-[70vh]">
              {/* Left: Original snapshot */}
              <div className="flex flex-col gap-2">
                <div className="flex items-center justify-between text-xs font-bold text-ink-2 pb-1 border-b border-border">
                  <span>Mevcut Sistem Verisi (Orijinal)</span>
                  <span className="text-[10px] px-2 py-0.5 rounded bg-surface-2">Mevcut DB</span>
                </div>
                <pre className="p-3 bg-surface-2 rounded-lg text-[11.5px] font-mono overflow-x-auto text-ink-2 max-h-[500px]">
                  {JSON.stringify(selectedItemForDiff.originalSnapshot, null, 2)}
                </pre>
              </div>

              {/* Right: Proposed alternative */}
              <div className="flex flex-col gap-2">
                <div className="flex items-center justify-between text-xs font-bold text-primary pb-1 border-b border-primary/20">
                  <span>NotebookLM Önerisi (Alternatif)</span>
                  <span className="text-[10px] px-2 py-0.5 rounded bg-primary/10 text-primary">NotebookLM</span>
                </div>
                <pre className="p-3 bg-primary/5 border border-primary/20 rounded-lg text-[11.5px] font-mono overflow-x-auto text-ink max-h-[500px]">
                  {JSON.stringify(selectedItemForDiff.proposedData, null, 2)}
                </pre>
              </div>
            </div>

            <div className="flex items-center justify-between p-4 border-t border-border bg-surface-1">
              <span className="text-xs text-ink-3">
                {selectedItemForDiff.status === 'active' ? '🟢 Bu alternatif şu anda sistemde aktiftir.' : '🟡 Bu alternatif henüz aktif edilmemiştir.'}
              </span>
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => setSelectedItemForDiff(null)}
                  className="ms-btn is-sm is-ghost text-xs"
                >
                  Kapat
                </button>
                {selectedItemForDiff.status === 'active' ? (
                  <button
                    type="button"
                    onClick={() => {
                      handleDeactivate(selectedItemForDiff);
                      setSelectedItemForDiff(null);
                    }}
                    className="ms-btn is-sm is-outline text-xs text-amber-600"
                  >
                    Orijinal Veriye Geri Dön
                  </button>
                ) : (
                  <button
                    type="button"
                    onClick={() => {
                      handleActivate(selectedItemForDiff);
                      setSelectedItemForDiff(null);
                    }}
                    className="ms-btn is-sm is-primary text-xs bg-emerald-600 hover:bg-emerald-700"
                  >
                    Bu Alternatifi Tercih Et (Sisteme Uygula)
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Edit Modal */}
      {editingItem && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs">
          <div className="bg-card border border-border rounded-2xl w-full max-w-2xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden">
            <div className="flex items-center justify-between p-4 border-b border-border bg-surface-1">
              <div className="flex items-center gap-2">
                <Edit3 className="w-5 h-5 text-primary" />
                <h3 className="text-base font-bold text-ink">JSON Düzenle: {editingItem.title}</h3>
              </div>
              <button
                type="button"
                onClick={() => setEditingItem(null)}
                className="p-1 rounded-lg text-ink-3 hover:text-ink"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-4 flex flex-col gap-3">
              <textarea
                rows={16}
                value={editJsonText}
                onChange={(e) => setEditJsonText(e.target.value)}
                className="ms-input font-mono text-xs w-full leading-relaxed"
              />
            </div>

            <div className="flex items-center justify-end gap-2 p-4 border-t border-border bg-surface-1">
              <button
                type="button"
                onClick={() => setEditingItem(null)}
                className="ms-btn is-sm is-ghost text-xs"
              >
                İptal
              </button>
              <button
                type="button"
                onClick={handleSaveEdit}
                className="ms-btn is-sm is-primary text-xs"
              >
                Değişiklikleri Kaydet
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
