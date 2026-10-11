import React, { useEffect, useState, useMemo } from 'react';
import { confirmText } from '../ui/ConfirmDialog';
import {
  Clock,
  Sparkles,
  CheckCircle2,
  AlertTriangle,
  RotateCcw,
  Play,
  Pause,
  RefreshCw,
  Search,
  Filter,
  Trash2,
  ChevronDown,
  ChevronUp,
  FileText,
  BookOpen,
  HelpCircle,
  ShieldCheck,
  ExternalLink,
  Layers,
  MapPin,
} from 'lucide-react';
import {
  AutoRepairItemClient,
  AutoRepairStats,
  loadAutoRepairItems,
  loadAutoRepairStats,
  runNextAutoRepair,
  runAllAutoRepair,
  rollbackAutoRepair,
  retryAutoRepair,
  toggleAutoRepairWorker,
  deleteAutoRepairItem,
  clearProcessedAutoRepair,
  bulkDeleteAutoRepair,
} from '../../services/manageConsoleService';
import { toast } from '../ui/Toast';
import {
  buildUniversalReportUrl,
  getUniversalLocationBreadcrumb,
} from '../../services/universalRedirectService';
import { guardedInterval } from '../../services/net';

export const ManagePendingOperationsSection: React.FC = () => {
  const [items, setItems] = useState<AutoRepairItemClient[]>([]);
  const [stats, setStats] = useState<AutoRepairStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [actionBusy, setActionBusy] = useState(false);
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [selectedIds, setSelectedIds] = useState<string[]>([]);

  // Filtreler
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [filterSource, setFilterSource] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState('');

  const loadData = async () => {
    try {
      const [itemList, statData] = await Promise.all([
        loadAutoRepairItems(),
        loadAutoRepairStats(),
      ]);
      setItems(itemList);
      setStats(statData);
    } catch (e: any) {
      toast.error('Veriler yüklenemedi', e?.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    // Önceki yükleme bitmeden yenisi başlamaz; sekme gizliyken durur
    return guardedInterval(loadData, 10000);
  }, []);

  const handleRunNext = async () => {
    setActionBusy(true);
    try {
      const res = await runNextAutoRepair();
      if (res.success) {
        toast.success('İşlem çalıştırıldı', res.message || 'Sıradaki işlem incelendi.');
        await loadData();
      } else {
        toast.error('Çalıştırılamadı', res.error);
      }
    } catch (e: any) {
      toast.error('Hata', e?.message);
    } finally {
      setActionBusy(false);
    }
  };

  const handleRunAll = async () => {
    setActionBusy(true);
    try {
      const res = await runAllAutoRepair();
      if (res.success) {
        toast.success('Toplu inceleme başlatıldı', res.message);
        await loadData();
      } else {
        toast.error('Başlatılamadı', res.error);
      }
    } catch (e: any) {
      toast.error('Hata', e?.message);
    } finally {
      setActionBusy(false);
    }
  };

  const handleRollback = async (id: string) => {
    if (!(await confirmText('Bu otomatik düzeltmeyi geri alıp orijinal haline döndürmek istediğine emin misin?'))) return;
    setActionBusy(true);
    try {
      const res = await rollbackAutoRepair(id);
      if (res.success) {
        toast.success('Geri Alındı', res.message);
        await loadData();
      } else {
        toast.error('Geri alınamadı', res.error);
      }
    } catch (e: any) {
      toast.error('Geri alma hatası', e?.message);
    } finally {
      setActionBusy(false);
    }
  };

  const handleRetry = async (id: string) => {
    setActionBusy(true);
    try {
      const res = await retryAutoRepair(id);
      if (res.success) {
        toast.success('Yeniden incelendi', 'İşlem Gemini tarafından tekrar işlendi.');
        await loadData();
      } else {
        toast.error('İşlenemedi', res.error);
      }
    } catch (e: any) {
      toast.error('Hata', e?.message);
    } finally {
      setActionBusy(false);
    }
  };

  const handleToggleWorker = async () => {
    if (!stats) return;
    setActionBusy(true);
    try {
      const nextPaused = stats.isWorkerActive; // aktifse duraklat
      await toggleAutoRepairWorker(nextPaused);
      toast.info(nextPaused ? 'Otomasyon Duraklatıldı' : 'Otomasyon Devam Ediyor', nextPaused ? 'Arka plan kuyruk işleyicisi beklemeye alındı.' : 'Kuyruk 20 saniyelik aralıklarla otomatik işlenecek.');
      await loadData();
    } catch (e: any) {
      toast.error('Ayar değiştirilemedi', e?.message);
    } finally {
      setActionBusy(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!(await confirmText("Bu kaydı kuyruktan kalıcı olarak silmek ve ID'sini banlamak istiyor musunuz?\n\nBu ID kalıcı olarak banlanacağı için bir daha asla kuyruğa geri dönemez."))) return;
    try {
      const ok = await deleteAutoRepairItem(id);
      if (ok) {
        toast.success('Silindi & Banlandı', "Hata bildirimi silindi ve ID'si kalıcı olarak banlandı. Tekrar geri gelmeyecek.");
        setItems((prev) => prev.filter((x) => x.id !== id));
        setSelectedIds((prev) => prev.filter((x) => x !== id));
        await loadData();
      }
    } catch (e: any) {
      toast.error('Silinemedi', e?.message);
    }
  };

  const handleClearProcessed = async () => {
    const processedCount = items.filter(
      (x) => x.status === 'applied' || x.status === 'no_change' || x.status === 'rolled_back'
    ).length;
    if (processedCount === 0) {
      toast.info('İşlem Yapılmış Kayıt Yok', 'Kuyrukta temizlenecek tamamlanmış işlem bulunamadı.');
      return;
    }
    if (!(await confirmText(`İşlem yapılmış ${processedCount} adet hata bildirimini kuyruktan topluca temizlemek ve ID'lerini kalıcı olarak banlamak istiyor musunuz?\n\nBu sayede bu bildirimler bir daha asla kuyruğa geri dönemez.`))) return;

    setActionBusy(true);
    try {
      const res = await clearProcessedAutoRepair();
      if (res.success) {
        toast.success('Temizlendi & Banlandı', res.message || `${res.clearedCount} adet işlem yapılan kayıt temizlendi.`);
        await loadData();
      } else {
        toast.error('Temizleme başarısız', res.message);
      }
    } catch (e: any) {
      toast.error('Hata', e?.message);
    } finally {
      setActionBusy(false);
    }
  };

  const handleBulkDelete = async () => {
    if (selectedIds.length === 0) return;
    if (!(await confirmText(`Seçilen ${selectedIds.length} adet hata bildirimini kuyruktan kalıcı olarak silmek ve ID'lerini banlamak istiyor musunuz?\n\nBu bildirimlerin ID'leri banlanacak ve tekrar kuyruğa giremeyecektir.`))) return;

    setActionBusy(true);
    try {
      const res = await bulkDeleteAutoRepair(selectedIds);
      if (res.success) {
        toast.success('Toplu Silindi', res.message || `${selectedIds.length} kayıt silindi ve banlandı.`);
        setSelectedIds([]);
        await loadData();
      } else {
        toast.error('Toplu silme başarısız', res.message);
      }
    } catch (e: any) {
      toast.error('Hata', e?.message);
    } finally {
      setActionBusy(false);
    }
  };

  // Filtreleme
  const filteredItems = useMemo(() => {
    return items.filter((item) => {
      if (filterStatus !== 'all' && item.status !== filterStatus) return false;
      if (filterSource !== 'all' && item.source !== filterSource) return false;
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const text = [
          item.targetId,
          item.userReport.reason,
          item.userReport.details,
          item.userReport.reportedBy,
          item.aiAnalysis?.changesSummary,
          item.aiAnalysis?.medicalReasoning,
          item.subTarget?.label,
          item.subTarget?.location,
        ].filter(Boolean).join(' ').toLowerCase();
        if (!text.includes(q)) return false;
      }
      return true;
    });
  }, [items, filterStatus, filterSource, searchQuery]);

  const getSourceBadge = (source: string, subTarget?: any) => {
    switch (source) {
      case 'past_question':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-medium bg-accent-soft text-accent border border-accent/30">
            <HelpCircle className="w-3 h-3" /> Çıkmış Soru
          </span>
        );
      case 'practice_question':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-medium bg-accent-soft text-accent border border-accent/30">
            <FileText className="w-3 h-3" /> Örnek / Çalışma Sorusu
          </span>
        );
      case 'interactive_deck':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-medium bg-ok-soft text-ok border border-ok/30">
            <BookOpen className="w-3 h-3" /> Öğrenme Destesi {subTarget?.slideNumber ? `· Slayt ${subTarget.slideNumber}` : ''}
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-medium bg-field text-ink-2 border border-line">
            <Layers className="w-3 h-3" /> Ders Notu / Özet
          </span>
        );
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'pending':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-semibold bg-warn-soft text-warn border border-warn/30">
            <Clock className="w-3 h-3 animate-spin" /> Kuyrukta Bekliyor
          </span>
        );
      case 'processing':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-semibold bg-accent-soft text-accent border border-accent/30">
            <Sparkles className="w-3 h-3 animate-pulse" /> Gemini İnceliyor…
          </span>
        );
      case 'applied':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-semibold bg-ok-soft text-ok border border-ok/30">
            <CheckCircle2 className="w-3 h-3" /> Otomatik Düzeltildi & Yayında
          </span>
        );
      case 'no_change':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-semibold bg-field text-ink-2 border border-line">
            <ShieldCheck className="w-3 h-3" /> Doğrulandı · Değişiklik Gerekmedi
          </span>
        );
      case 'rolled_back':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-semibold bg-ai-soft text-ai border border-ai/30">
            <RotateCcw className="w-3 h-3" /> Geri Alındı (Rollback)
          </span>
        );
      case 'error':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-semibold bg-bad-soft text-bad-text border border-bad/30">
            <AlertTriangle className="w-3 h-3" /> İnceleme Hatası
          </span>
        );
      default:
        return null;
    }
  };

  const getTargetNavigation = (item: AutoRepairItemClient) => {
    const breadcrumb = getUniversalLocationBreadcrumb({
      type: item.source as any,
      targetId: item.targetId,
      subTarget: item.subTarget,
      highlightText: item.subTarget?.label || undefined,
    });

    const url = buildUniversalReportUrl({
      type: item.source as any,
      targetId: item.targetId,
      subTarget: item.subTarget,
      highlightText: item.subTarget?.label || undefined,
    });

    let label = 'Konuma Git';
    if (item.source === 'interactive_deck') {
      label = item.subTarget?.slideNumber ? `Slayt #${item.subTarget.slideNumber}'e Git` : 'Derse Git';
    } else if (item.source === 'past_question') {
      label = 'Çıkmış Soruya Git';
    } else if (item.source === 'practice_question') {
      label = 'Soru Havuzuna Git';
    }

    return {
      url,
      label,
      badgeLabel: breadcrumb.badge,
      description: breadcrumb.fullLocation,
      category: breadcrumb.category,
    };
  };

  return (
    <div className="space-y-6">
      {/* Üst Bilgi Başlığı ve Kontrol Çubuğu */}
      <div className="bg-white rounded-xl border border-line shadow-sm p-5 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="p-2 rounded-lg bg-accent-soft text-accent">
                <Sparkles className="w-5 h-5" />
              </span>
              <div>
                <h2 className="text-lg font-bold text-ink">Bekleyen İşlemler & Hata Onarım Otomasyonu</h2>
                <p className="text-xs text-ink-3">
                  ÜCRETSİZ Google Gemini API ve Çok Katmanlı Fall-back Sistemi (<code className="px-1 py-0.5 rounded bg-field text-ink-2 font-mono">Gemini 2.5/2.0 Flash → Groq Cloud Llama/GPT-OSS → OpenRouter → Yerel GPU</code>) ile kullanıcı bildirimleri kuyruğa alınır, bağlam derinlemesine taranır ve eksiksiz düzeltmeler siteye işlenir.
                </p>
              </div>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <button
              type="button"
              onClick={handleToggleWorker}
              disabled={actionBusy}
              className={`ms-btn text-xs ${stats?.isWorkerActive ? 'is-ghost' : 'is-primary'}`}
              title={stats?.isWorkerActive ? 'Arka plan kuyruk işleyicisini duraklat' : 'Arka plan kuyruk işleyicisini başlat'}
            >
              {stats?.isWorkerActive ? (
                <>
                  <Pause className="w-3.5 h-3.5 text-warn" /> Otomasyonu Duraklat
                </>
              ) : (
                <>
                  <Play className="w-3.5 h-3.5" /> Otomasyonu Başlat
                </>
              )}
            </button>

            <button
              type="button"
              onClick={handleRunNext}
              disabled={actionBusy || (stats?.pending || 0) === 0}
              className="ms-btn is-primary text-xs"
              title="Kuyruktaki ilk işlemi şimdi derhal yapay zekaya incelet"
            >
              <Play className="w-3.5 h-3.5" /> Sıradakini Çalıştır
            </button>

            <button
              type="button"
              onClick={handleRunAll}
              disabled={actionBusy || (stats?.pending || 0) === 0}
              className="ms-btn is-ghost text-xs"
              title="Tüm bekleyen bildirimleri sırayla arka planda incelet"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${actionBusy ? 'animate-spin' : ''}`} /> Tümünü İncelet ({stats?.pending || 0})
            </button>

            <button
              type="button"
              onClick={handleClearProcessed}
              disabled={actionBusy}
              className="ms-btn is-ghost text-xs text-bad-text hover:bg-bad-soft border-bad/30"
              title="İşlem yapılmış (uygulandı, doğru bulundu, geri alındı) tüm bildirimleri kalıcı olarak siler ve ID'lerini banlar (bir daha asla geri dönemez)"
            >
              <Trash2 className="w-3.5 h-3.5 text-bad-text" /> İşlem Yapılanları Temizle
            </button>
          </div>
        </div>

        {/* İstatistik Sayaç Kartları */}
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 pt-2 border-t border-line">
          <div className="bg-warn-soft/60 border border-warn/60 rounded-lg p-3">
            <div className="text-xs text-warn font-medium">Kuyrukta Bekleyen</div>
            <div className="text-2xl font-bold text-warn mt-1">{stats?.pending ?? 0}</div>
          </div>
          <div className="bg-ok-soft/60 border border-ok/60 rounded-lg p-3">
            <div className="text-xs text-ok font-medium">Otomatik Düzeltilen</div>
            <div className="text-2xl font-bold text-ok mt-1">{stats?.applied ?? 0}</div>
          </div>
          <div className="bg-field border border-line rounded-lg p-3">
            <div className="text-xs text-ink-2 font-medium">Doğrulanan (Değişiklik Yok)</div>
            <div className="text-2xl font-bold text-ink mt-1">{stats?.noChange ?? 0}</div>
          </div>
          <div className="bg-ai-soft/60 border border-ai/60 rounded-lg p-3">
            <div className="text-xs text-ai font-medium">Geri Alınan (Rollback)</div>
            <div className="text-2xl font-bold text-ai mt-1">{stats?.rolledBack ?? 0}</div>
          </div>
          <div className="bg-field border border-line rounded-lg p-3">
            <div className="text-xs text-ink-2 font-medium">İnceleme Modeli</div>
            <div className="text-sm font-bold text-ink mt-1.5 flex items-center gap-1">
              <span className="w-2 h-2 rounded-full bg-ok animate-pulse"></span>
              Gemini 2.5 Flash
            </div>
            <div className="text-2xs text-ok font-medium mt-0.5">ÜCRETSİZ PLAN</div>
          </div>
        </div>
      </div>

      {/* Arama ve Filtre Çubuğu */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 bg-white p-3 rounded-lg border border-line">
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-ink-3 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Soru no, ders deste adı, kullanıcı notu veya AI gerekçesinde ara…"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 text-xs bg-field border border-line rounded-md focus:bg-white focus:outline-none focus:ring-1 focus:ring-accent"
          />
        </div>

        <div className="flex flex-wrap items-center gap-2 min-w-0">
          <div className="flex items-center gap-1.5 text-xs text-ink-3 min-w-0">
            <Filter className="w-3.5 h-3.5" />
            <span>Durum:</span>
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="text-xs bg-field border border-line rounded px-2 py-1 focus:outline-none min-w-0 max-w-full"
            >
              <option value="all">Tümü</option>
              <option value="pending">Kuyrukta Bekleyenler</option>
              <option value="applied">Otomatik Düzeltilenler</option>
              <option value="no_change">Doğrulananlar (Değişiklik Yok)</option>
              <option value="rolled_back">Geri Alınanlar</option>
              <option value="error">Hatalılar</option>
            </select>
          </div>

          <div className="flex flex-wrap items-center gap-1.5 text-xs text-ink-3 min-w-0">
            <span>Kaynak:</span>
            <select
              value={filterSource}
              onChange={(e) => setFilterSource(e.target.value)}
              className="text-xs bg-field border border-line rounded px-2 py-1 focus:outline-none min-w-0 max-w-full"
            >
              <option value="all">Tüm Kaynaklar</option>
              <option value="past_question">Çıkmış Sorular</option>
              <option value="practice_question">Örnek Sorular</option>
              <option value="interactive_deck">Öğrenme Desteleri & Slaytlar</option>
            </select>
          </div>

          <button
            type="button"
            onClick={loadData}
            className="p-1.5 rounded text-ink-3 hover:text-ink hover:bg-field transition-colors"
            title="Yenile"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>

        {/* Toplu İşlem / Seçim Çubuğu */}
        {filteredItems.length > 0 && (
          <div className="flex items-center justify-between px-3 py-2 bg-field/90 rounded-lg text-xs text-ink-2 border border-line">
            <label className="flex items-center gap-2 cursor-pointer font-medium select-none">
              <input
                type="checkbox"
                checked={selectedIds.length > 0 && selectedIds.length === filteredItems.length}
                onChange={(e) => {
                  if (e.target.checked) {
                    setSelectedIds(filteredItems.map((x) => x.id));
                  } else {
                    setSelectedIds([]);
                  }
                }}
                className="rounded text-accent focus:ring-accent cursor-pointer"
              />
              <span>
                {selectedIds.length > 0
                  ? `${selectedIds.length} / ${filteredItems.length} işlem seçildi`
                  : 'Tümünü Seç'}
              </span>
            </label>

            {selectedIds.length > 0 && (
              <button
                type="button"
                onClick={handleBulkDelete}
                disabled={actionBusy}
                className="ms-btn is-ghost text-xs text-bad-text hover:bg-bad-soft py-1 px-2.5 rounded border border-bad/30 font-semibold inline-flex items-center gap-1.5 cursor-pointer"
              >
                <Trash2 className="w-3.5 h-3.5" /> Seçilenleri Sil & Banla ({selectedIds.length})
              </button>
            )}
          </div>
        )}
      </div>

      {/* İşlem Listesi */}
      {loading ? (
        <div className="py-16 text-center text-ink-3">
          <RefreshCw className="w-6 h-6 animate-spin mx-auto mb-2 text-accent" />
          <p className="text-xs">Bekleyen işlemler ve hata kütüğü yükleniyor…</p>
        </div>
      ) : filteredItems.length === 0 ? (
        <div className="bg-white rounded-xl border border-line p-12 text-center text-ink-3">
          <ShieldCheck className="w-10 h-10 text-ok mx-auto mb-3" />
          <h3 className="text-sm font-semibold text-ink">Kuyruk Temiz & Güncel</h3>
          <p className="text-xs text-ink-3 mt-1 max-w-md mx-auto">
            {searchQuery || filterStatus !== 'all' || filterSource !== 'all'
              ? 'Seçili filtrelere uygun işlem bulunamadı.'
              : 'Şu anda incelenmeyi bekleyen bildirim bulunmuyor. Kullanıcılar hata bildirdikçe otomatik olarak bu kuyruğa eklenecek ve Gemini tarafından sırayla işlenecektir.'}
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {filteredItems.map((item) => {
            const isExpanded = expandedId === item.id;
            const targetNav = getTargetNavigation(item);
            return (
              <div
                key={item.id}
                className="bg-white rounded-xl border border-line shadow-sm hover:border-line-2 transition-all overflow-hidden"
              >
                {/* Kart Başlığı */}
                <div
                  className="p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3 cursor-pointer select-none bg-field/50"
                  onClick={() => setExpandedId(isExpanded ? null : item.id)}
                >
                  <div className="flex items-start gap-3 flex-1 min-w-0">
                    <input
                      type="checkbox"
                      checked={selectedIds.includes(item.id)}
                      onClick={(e) => e.stopPropagation()}
                      onChange={(e) => {
                        e.stopPropagation();
                        if (e.target.checked) {
                          setSelectedIds((prev) => [...prev, item.id]);
                        } else {
                          setSelectedIds((prev) => prev.filter((x) => x !== item.id));
                        }
                      }}
                      className="mt-1 rounded text-accent focus:ring-accent cursor-pointer"
                    />
                    <div className="space-y-1.5 flex-1 min-w-0">
                      <div className="flex flex-wrap items-center gap-2">
                      {getSourceBadge(item.source, item.subTarget)}
                      <span className="font-mono text-xs font-semibold text-ink">
                        #{item.targetId}
                      </span>
                      {getStatusBadge(item.status)}
                      {item.aiAnalysis?.releaseQuarantine && (
                        <span className="px-2 py-0.5 rounded text-2xs font-semibold bg-ok-soft text-ok border border-ok/30">
                          ✓ Karantinadan Kurtarıldı
                        </span>
                      )}
                      {!item.aiAnalysis?.releaseQuarantine && item.crossData?.isQuarantined && (
                        <span className="px-2 py-0.5 rounded text-2xs font-semibold bg-bad-soft text-bad-text border border-bad/30">
                          ⚠️ Karantina Kaydı
                        </span>
                      )}
                      {item.aiAnalysis?.referencedRedactedId && (
                        <span className="px-2 py-0.5 rounded text-2xs font-semibold bg-accent-soft text-accent border border-accent/30">
                          🔗 Redakte Soru #{item.aiAnalysis.referencedRedactedId}
                        </span>
                      )}
                      {!item.aiAnalysis?.referencedRedactedId && item.crossData?.bestRedactedReference && (
                        <span className="px-2 py-0.5 rounded text-2xs font-semibold bg-accent-soft text-accent border border-accent/30">
                          Kardeş Redaksiyon Mevcut
                        </span>
                      )}
                      <span className="text-2xs text-ink-3">
                        {new Date(item.userReport.reportedAt).toLocaleDateString('tr-TR', {
                          day: 'numeric',
                          month: 'short',
                          hour: '2-digit',
                          minute: '2-digit',
                        })}
                      </span>
                    </div>

                    <div className="text-xs text-ink font-medium flex items-baseline gap-2">
                      <span className="text-accent font-semibold">{item.userReport.reason}</span>
                      {item.userReport.details ? (
                        <span className="text-ink-2 truncate max-w-xl">“{item.userReport.details}”</span>
                      ) : (
                        <span className="text-warn text-2xs italic font-normal">
                          (Kullanıcı açıklama girmedi — AI derin denetimi yaptı)
                        </span>
                      )}
                    </div>
                  </div>
                </div>

                  {/* Sağ Aksiyonlar & Yönlendirici */}
                  <div className="flex flex-wrap items-center gap-2 self-end sm:self-center" onClick={(e) => e.stopPropagation()}>
                    {/* Doğrudan Konuma Git (Yönlendirici) */}
                    <a
                      href={targetNav.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="ms-btn text-xs text-accent bg-accent-soft/90 hover:bg-accent-soft hover:text-accent border border-accent/90 shadow-xs flex items-center gap-1.5 font-semibold transition-all px-2.5 py-1"
                      title={targetNav.description}
                    >
                      <ExternalLink className="w-3.5 h-3.5 text-accent shrink-0" />
                      <span>{targetNav.label}</span>
                    </a>

                    {item.status === 'applied' && (
                      <button
                        type="button"
                        onClick={() => handleRollback(item.id)}
                        disabled={actionBusy}
                        className="ms-btn text-xs text-ai bg-ai-soft hover:bg-ai-soft border border-ai/30"
                        title="Bu değişikliği geri al ve eski orijinal veriyi yerine koy"
                      >
                        <RotateCcw className="w-3.5 h-3.5" /> Geri Al (Rollback)
                      </button>
                    )}

                    {item.status === 'pending' && (
                      <button
                        type="button"
                        onClick={async () => {
                          setActionBusy(true);
                          try {
                            const res = await retryAutoRepair(item.id);
                            if (res.success) toast.success('İşlendi', 'Yapay zeka incelemesi tamamlandı.');
                            await loadData();
                          } finally {
                            setActionBusy(false);
                          }
                        }}
                        disabled={actionBusy}
                        className="ms-btn is-primary text-xs"
                      >
                        <Sparkles className="w-3.5 h-3.5" /> Şimdi İncele
                      </button>
                    )}

                    {(item.status === 'error' || item.status === 'rolled_back' || item.status === 'no_change') && (
                      <button
                        type="button"
                        onClick={() => handleRetry(item.id)}
                        disabled={actionBusy}
                        className="ms-btn is-ghost text-xs"
                        title="Yeniden incelemeye gönder"
                      >
                        <RefreshCw className="w-3.5 h-3.5" /> Tekrar İncelet
                      </button>
                    )}

                    <button
                      type="button"
                      onClick={() => handleDelete(item.id)}
                      className="p-1.5 text-ink-3 hover:text-bad-text hover:bg-bad-soft rounded transition-colors"
                      title="Kuyruktan sil"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>

                    <button
                      type="button"
                      onClick={() => setExpandedId(isExpanded ? null : item.id)}
                      className="p-1.5 text-ink-3 hover:text-ink-2 rounded"
                    >
                      {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                    </button>
                  </div>
                </div>

                {/* Genişletilmiş Detay Paneli */}
                {isExpanded && (
                  <div className="p-4 border-t border-line space-y-4 bg-white text-xs">
                    {/* Doğrudan Konum ve Değişiklik Yönlendirici Banner'ı */}
                    <div className="bg-accent-soft/80 border border-accent/80 rounded-xl p-3.5 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs shadow-xs">
                      <div className="flex items-start sm:items-center gap-2.5">
                        <div className="p-2 bg-accent-soft text-accent rounded-lg shrink-0">
                          <MapPin className="w-4 h-4" />
                        </div>
                        <div>
                          <div className="font-semibold text-ink flex flex-wrap items-center gap-2">
                            <span>Değişiklik Yapılan Konum:</span>
                            <code className="bg-white px-2 py-0.5 rounded border border-accent/30 text-accent font-mono text-2xs font-bold">
                              {targetNav.badgeLabel}
                            </code>
                          </div>
                          <p className="text-2xs text-ink-2 mt-0.5">{targetNav.description}</p>
                        </div>
                      </div>

                      <a
                        href={targetNav.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="ms-btn is-primary text-xs flex items-center justify-center gap-1.5 shrink-0 px-3.5 py-1.5 font-semibold shadow-xs hover:shadow-sm"
                      >
                        <span>Konumu Sitede Aç & İncele</span>
                        <ExternalLink className="w-3.5 h-3.5" />
                      </a>
                    </div>
                    {/* Kullanıcı Bildirim Ayrıntıları */}
                    <div className="bg-field p-3 rounded-lg border border-line space-y-1">
                      <div className="text-2xs font-semibold text-ink-3 uppercase tracking-wider">
                        Kullanıcı Şikayet & Bildirim Kaydı
                      </div>
                      <div className="flex flex-wrap gap-x-4 gap-y-1 text-ink-2">
                        <div><b>Bildiren:</b> {item.userReport.reportedBy || 'Anonim Öğrenci'}</div>
                        {item.userReport.email && <div><b>E-Posta:</b> {item.userReport.email}</div>}
                        <div><b>Tarih:</b> {new Date(item.userReport.reportedAt).toLocaleString('tr-TR')}</div>
                        {item.userReport.suggestedAnswer && <div><b>Önerilen Cevap:</b> {item.userReport.suggestedAnswer}</div>}
                      </div>
                      {item.userReport.details && (
                        <div className="mt-2 text-ink bg-white p-2 rounded border border-line font-sans">
                          {item.userReport.details}
                        </div>
                      )}
                    </div>

                    {/* Çapraz Veri & Redaksiyon Denetim Bilgisi */}
                    {item.crossData && (
                      <div className="bg-field p-3 rounded-lg border border-line space-y-1.5 text-xs">
                        <div className="flex items-center gap-1.5 font-bold text-ink">
                          <ShieldCheck className="w-4 h-4 text-accent" />
                          <span>Çapraz Veri & Redaksiyon Denetim Dosyası</span>
                        </div>
                        <div className="text-2xs text-ink-2 space-y-1">
                          <div className="flex items-center gap-2">
                            <b>Karantina Kaydı:</b>{' '}
                            {item.crossData.isQuarantined ? (
                              <span className="text-bad-text font-semibold">
                                Karantinada ({item.crossData.quarantineReasons.join(', ') || 'Neden belirtilmemiş'})
                              </span>
                            ) : (
                              <span className="text-ok font-medium">Standart (Karantinada Değil)</span>
                            )}
                          </div>
                          {item.crossData.mergeGroup && (
                            <div>
                              <b>Birleştirme Grubu:</b> <code className="bg-line px-1 py-0.5 rounded text-2xs">{item.crossData.mergeGroup.groupId}</code>{' '}
                              (Asıl: #{item.crossData.mergeGroup.asilId}, {item.crossData.mergeGroup.otherMembers.length} kardeş soru)
                            </div>
                          )}
                          {item.crossData.bestRedactedReference && (
                            <div className="bg-white p-2 rounded border border-line mt-1">
                              <div className="text-accent font-semibold flex items-center gap-1">
                                <span>⭐ Sistemdeki En Temiz Redaksiyon: Soru #{item.crossData.bestRedactedReference.id}</span>
                                <span className="text-2xs px-1 py-0.2 bg-accent-soft rounded text-accent">
                                  {item.crossData.bestRedactedReference.sourceType}
                                </span>
                              </div>
                              <div className="text-2xs text-ink-2 italic truncate mt-0.5">
                                “{item.crossData.bestRedactedReference.stem}”
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    )}

                    {/* AI Değerlendirmesi ve Raporu */}
                    {item.aiAnalysis && (
                      <div className="bg-accent-soft/50 p-3.5 rounded-lg border border-accent/30 space-y-2.5">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-1.5 text-accent font-bold">
                            <Sparkles className="w-4 h-4 text-accent" />
                            <span>Yapay Zekâ Tıbbi İnceleme Raporu ({item.aiAnalysis.modelUsed})</span>
                          </div>
                          <span className="text-2xs text-ink-3">
                            {new Date(item.aiAnalysis.processedAt).toLocaleString('tr-TR')}
                          </span>
                        </div>

                        {item.aiAnalysis.changesSummary && (
                          <div>
                            <div className="text-2xs font-semibold text-accent">Değişiklik Özeti:</div>
                            <div className="text-ink font-medium mt-0.5">{item.aiAnalysis.changesSummary}</div>
                          </div>
                        )}

                        {item.aiAnalysis.detectedIssues && item.aiAnalysis.detectedIssues.length > 0 && (
                          <div>
                            <div className="text-2xs font-semibold text-bad-text">Tespit Edilen Tıbbi Hatalar:</div>
                            <ul className="list-disc list-inside mt-0.5 text-bad-text space-y-0.5">
                              {item.aiAnalysis.detectedIssues.map((issue, idx) => (
                                <li key={idx}>{issue}</li>
                              ))}
                            </ul>
                          </div>
                        )}

                        {item.aiAnalysis.medicalReasoning && (
                          <div>
                            <div className="text-2xs font-semibold text-ink-2">Fizyopatolojik / Tıbbi Gerekçe (Robbins, Guyton & Müfredat):</div>
                            <div className="text-ink-2 leading-relaxed mt-0.5 whitespace-pre-wrap bg-white/80 p-2.5 rounded border border-accent/30">
                              {item.aiAnalysis.medicalReasoning}
                            </div>
                          </div>
                        )}
                      </div>
                    )}

                    {/* Hata Mesajı Varsa */}
                    {item.errorDetails && (
                      <div className="bg-bad-soft p-3 rounded-lg border border-bad/30 text-bad-text">
                        <b>İnceleme Sırasında Hata:</b> {item.errorDetails}
                      </div>
                    )}

                    {/* Öncesi ve Sonrası (Diff Görünümü) */}
                    {item.beforeSnapshot && item.afterSnapshot && (
                      <div className="space-y-2">
                        <div className="text-2xs font-bold text-ink-2 uppercase tracking-wider flex items-center gap-1.5">
                          <span>Öncesi ve Sonrası Karşılaştırması (Yapılan Değişiklik)</span>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                          {/* Öncesi */}
                          <div className="bg-bad-soft/40 p-3 rounded-lg border border-bad/30 space-y-2">
                            <div className="flex items-center justify-between text-bad-text font-bold border-b border-bad/30 pb-1">
                              <span>Orijinal Hali (Öncesi)</span>
                              <span className="text-2xs font-normal">Veritabanı Snapshot</span>
                            </div>
                            <div className="space-y-1 text-ink font-mono text-2xs max-h-60 overflow-y-auto whitespace-pre-wrap">
                              {item.source === 'interactive_deck' ? (
                                <>
                                  <div className="font-bold text-ink">{item.beforeSnapshot.title}</div>
                                  <div className="text-ink-2 text-xs font-sans mt-1">{item.beforeSnapshot.synthesisNarrative}</div>
                                </>
                              ) : (
                                <>
                                  <div className="font-bold text-ink">{item.beforeSnapshot.stem || item.beforeSnapshot.questionText}</div>
                                  <div className="text-bad-text font-bold mt-1">Cevap: {item.beforeSnapshot.correctAnswer || item.beforeSnapshot.answer}</div>
                                  <div className="text-ink-2 text-xs font-sans mt-1">{item.beforeSnapshot.explanation}</div>
                                </>
                              )}
                            </div>
                          </div>

                          {/* Sonrası */}
                          <div className="bg-ok-soft/40 p-3 rounded-lg border border-ok/30 space-y-2">
                            <div className="flex items-center justify-between text-ok font-bold border-b border-ok/30 pb-1">
                              <span>Düzeltilmiş Hali (Sonrası)</span>
                              <span className="text-2xs font-normal text-ok">Yapay Zekâ Onarımı</span>
                            </div>
                            <div className="space-y-1 text-ink font-mono text-2xs max-h-60 overflow-y-auto whitespace-pre-wrap">
                              {item.source === 'interactive_deck' ? (
                                <>
                                  <div className="font-bold text-ink">{item.afterSnapshot.title}</div>
                                  <div className="text-ink-2 text-xs font-sans mt-1">{item.afterSnapshot.synthesisNarrative}</div>
                                </>
                              ) : (
                                <>
                                  <div className="font-bold text-ink">{item.afterSnapshot.stem || item.afterSnapshot.questionText}</div>
                                  <div className="text-ok font-bold mt-1">Cevap: {item.afterSnapshot.correctAnswer || item.afterSnapshot.answer}</div>
                                  <div className="text-ink-2 text-xs font-sans mt-1">{item.afterSnapshot.explanation}</div>
                                </>
                              )}
                            </div>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
