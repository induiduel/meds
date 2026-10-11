import React, { useState, useEffect } from 'react';
import {
  Sparkles,
  Send,
  RefreshCw,
  X,
  Lock,
  ChevronDown,
  ChevronUp,
  BrainCircuit,
  MessageSquare,
  Library,
  ShieldAlert,
} from 'lucide-react';
import { ApiService } from '../../services/api';
import { toast } from '../ui/Toast';
import { AppUser } from '../../services/auth';

export interface QuestionClusterItem {
  id: string;
  clusterTitle: string;
  committeeId: string;
  discipline: string;
  sourceQuestionIds: string[];
  mergedQuestionCount: number;
  mergedStem: string;
  mergedOptions: Array<{ key: string; text: string }>;
  claimedAnswer: string;
  explanation: string;
  status: 'proposal';
  isLockedForDeletion: boolean;
  studentContributions: Array<{
    id: string;
    studentName: string;
    studentUid?: string;
    text: string;
    createdAt: string;
  }>;
  createdAt: string;
  updatedAt: string;
}

interface QuestionClusterAutomationModalProps {
  isOpen: boolean;
  onClose: () => void;
  currentUser?: AppUser | null;
  isAdmin?: boolean;
}

export const QuestionClusterAutomationModal: React.FC<QuestionClusterAutomationModalProps> = ({
  isOpen,
  onClose,
  currentUser,
  isAdmin,
}) => {
  const [clusters, setClusters] = useState<QuestionClusterItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [runningPipeline, setRunningPipeline] = useState(false);
  const [expandedClusterId, setExpandedClusterId] = useState<string | null>(null);

  // Katkı formu state
  const [contributionTexts, setContributionTexts] = useState<Record<string, string>>({});
  const [submittingContribId, setSubmittingContribId] = useState<string | null>(null);

  const fetchClusters = async () => {
    setLoading(true);
    try {
      const data = await ApiService.getPoolQuestionClusters();
      setClusters(data);
      if (data.length > 0 && !expandedClusterId) {
        setExpandedClusterId(data[0].id);
      }
    } catch (e: any) {
      toast.error('Hata', 'Kümeler yüklenemedi: ' + (e.message || ''));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      fetchClusters();
    }
  }, [isOpen]);

  const handleRunPipeline = async () => {
    setRunningPipeline(true);
    try {
      const res = await ApiService.runPoolQuestionClusterPipeline();
      toast.success('Otomasyon Başlatıldı', res.message);
      setTimeout(() => {
        fetchClusters();
      }, 3000);
    } catch (e: any) {
      toast.error('Hata', e.message || 'Otomasyon başlatılamadı.');
    } finally {
      setRunningPipeline(false);
    }
  };

  const handleAddContribution = async (clusterId: string) => {
    const text = (contributionTexts[clusterId] || '').trim();
    if (!text) {
      toast.error('Eksik Bilgi', 'Lütfen eklemek istediğiniz notu veya bilgiyi yazın.');
      return;
    }

    setSubmittingContribId(clusterId);
    try {
      const studentName = currentUser?.displayName || currentUser?.email || 'Tıp Öğrencisi';
      const res = await ApiService.contributeToPoolCluster(
        clusterId,
        studentName,
        text,
        currentUser?.uid
      );
      toast.success('Katkınız Eklendi', 'Öneri soru taslağına eklemeniz kaydedildi.');
      setContributionTexts(prev => ({ ...prev, [clusterId]: '' }));
      // Yerel state güncellemesi
      setClusters(prev =>
        prev.map(c => (c.id === clusterId ? res.cluster || {
          ...c,
          studentContributions: [...(c.studentContributions || []), res.contribution],
        } : c))
      );
    } catch (e: any) {
      toast.error('Hata', e.message || 'Katkı eklenemedi.');
    } finally {
      setSubmittingContribId(null);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-[var(--color-scrim)] overflow-y-auto">
      <div className="relative w-full max-w-4xl bg-canvas border border-line rounded-3xl p-5 sm:p-7 text-ink shadow-2xl my-6 flex flex-col max-h-[90vh]">
        {/* Başlık & Kapat */}
        <div className="flex items-start justify-between gap-4 pb-4 border-b border-line">
          <div>
            <div className="flex items-center gap-2 text-ok text-xs font-semibold uppercase tracking-wider mb-1">
              <BrainCircuit className="w-4 h-4 animate-pulse" />
              <span>Yapay Zeka Soru Eşleme & Kümeleme Otomasyonu</span>
            </div>
            <h2 className="text-xl sm:text-2xl font-black">
              Birleştirilmiş Soru Taslakları & Kolektif Öneri Havuzu
            </h2>
            <p className="text-xs sm:text-sm text-ink-3 mt-1 max-w-2xl leading-relaxed">
              Soru havuzundaki benzer ve parçalı sorular ücretsiz yapay zeka ajanları tarafından analiz edilip
              10'arlı gruplar halinde ideal soru kökü ve şıklarıyla birleştirilmiştir.
            </p>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="p-2 rounded-xl bg-field hover:bg-line-soft text-ink-3 hover:text-ink transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Kural Uyarı Kutusu */}
        <div className="mt-4 p-3.5 rounded-2xl bg-warn/10 border border-warn/20 flex items-start gap-3 text-xs text-warn-soft/90 leading-relaxed">
          <ShieldAlert className="w-5 h-5 text-warn shrink-0 mt-0.5" />
          <div>
            <span className="font-bold text-warn">Öğrenci Kuralı & Kısıtlama: </span>
            Bu sorular kolektif öneri taslağı niteliğindedir. Öğrenciler bu taslaklara yalnızca eklemeler ve
            tamamlayıcı notlar yapabilir; taslakları <strong>asla silemez veya doğrudan kabul/onay yapamaz</strong>.
          </div>
        </div>

        {/* Kontrol Çubuğu */}
        <div className="mt-4 flex items-center justify-between gap-3">
          <div className="text-xs text-ink-3">
            Toplam <span className="font-bold text-ok">{clusters.length}</span> birleştirilmiş öneri kümesi
          </div>
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={fetchClusters}
              disabled={loading}
              className="px-3 py-1.5 rounded-xl bg-canvas hover:bg-line-soft text-ink-3 text-xs font-semibold flex items-center gap-1.5 transition-colors"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
              <span>Yenile</span>
            </button>

            {isAdmin && (
              <button
                type="button"
                onClick={handleRunPipeline}
                disabled={runningPipeline}
                className="px-3.5 py-1.5 rounded-xl bg-ok hover:bg-ok text-white text-xs font-bold flex items-center gap-1.5 shadow-lg transition-all"
              >
                <Sparkles className="w-3.5 h-3.5" />
                <span>{runningPipeline ? 'Otomasyon Çalışıyor...' : 'Otomasyonu Tetikle'}</span>
              </button>
            )}
          </div>
        </div>

        {/* Küme Listesi */}
        <div className="mt-4 flex-1 overflow-y-auto space-y-4 pr-1">
          {loading ? (
            <div className="py-16 text-center text-ink-3 text-sm flex flex-col items-center gap-3">
              <RefreshCw className="w-8 h-8 animate-spin text-ok" />
              <span>Soru kümeleri ve öneri taslakları taranıyor...</span>
            </div>
          ) : clusters.length === 0 ? (
            <div className="py-16 text-center text-ink-3 text-sm bg-field rounded-2xl border border-line">
              <Library className="w-10 h-10 text-ink-3 mx-auto mb-2" />
              <p className="font-semibold text-ink-3">Henüz birleştirilmiş soru kümesi bulunmuyor.</p>
              <p className="text-xs text-ink-3 mt-1">
                Yukarıdaki "Otomasyonu Tetikle" butonu ile arka plan eşleme motorunu başlatabilirsiniz.
              </p>
            </div>
          ) : (
            clusters.map(cluster => {
              const isExpanded = expandedClusterId === cluster.id;
              return (
                <div
                  key={cluster.id}
                  className="rounded-2xl border border-line bg-slate-850 overflow-hidden transition-all shadow-md"
                >
                  {/* Başlık Satırı */}
                  <div
                    onClick={() => setExpandedClusterId(isExpanded ? null : cluster.id)}
                    className="p-4 bg-field hover:bg-field cursor-pointer flex items-center justify-between gap-3 transition-colors"
                  >
                    <div className="flex items-center gap-3 min-w-0">
                      <div className="w-9 h-9 rounded-xl bg-ok/10 border border-ok/20 text-ok flex items-center justify-center font-bold text-xs shrink-0">
                        {cluster.mergedQuestionCount}
                      </div>
                      <div className="min-w-0">
                        <div className="flex items-center gap-2 mb-0.5">
                          <span className="px-2 py-0.5 rounded bg-ok/20 text-ok text-2xs font-semibold uppercase">
                            {cluster.committeeId}
                          </span>
                          <span className="px-2 py-0.5 rounded bg-ink-2 text-ink-3 text-2xs font-medium">
                            {cluster.discipline}
                          </span>
                          <span className="px-2 py-0.5 rounded bg-warn/20 text-warn text-2xs font-semibold flex items-center gap-1">
                            <Lock className="w-2.5 h-2.5" /> Kalıcı Öneri Taslağı
                          </span>
                        </div>
                        <h4 className="text-sm font-bold text-ink truncate">
                          {cluster.clusterTitle}
                        </h4>
                      </div>
                    </div>

                    <div className="flex items-center gap-2 shrink-0">
                      <span className="text-xs text-ink-3 hidden sm:inline">
                        {cluster.studentContributions?.length || 0} Katkı
                      </span>
                      {isExpanded ? <ChevronUp className="w-4 h-4 text-ink-3" /> : <ChevronDown className="w-4 h-4 text-ink-3" />}
                    </div>
                  </div>

                  {/* Genişletilmiş Alan */}
                  {isExpanded && (
                    <div className="p-4 sm:p-5 space-y-4 border-t border-line bg-field text-xs">
                      {/* Önerilen Soru Kökü */}
                      <div className="space-y-1.5">
                        <div className="font-bold text-ink-3 uppercase tracking-wider text-2xs flex items-center gap-1.5">
                          <Sparkles className="w-3.5 h-3.5 text-ok" />
                          <span>Yapay Zeka Tarafından Birleştirilen Öneri Soru Kökü:</span>
                        </div>
                        <div className="p-3.5 rounded-xl bg-field border border-line text-ink-3 leading-relaxed text-sm font-medium">
                          {cluster.mergedStem}
                        </div>
                      </div>

                      {/* Önerilen Şıklar */}
                      <div className="space-y-2">
                        <div className="font-bold text-ink-3 uppercase tracking-wider text-2xs">
                          Önerilen Şıklar:
                        </div>
                        <div className="grid grid-cols-1 gap-2">
                          {cluster.mergedOptions.map(opt => {
                            const isCorrect = opt.key.toUpperCase() === cluster.claimedAnswer.toUpperCase();
                            return (
                              <div
                                key={opt.key}
                                className={`p-2.5 rounded-xl border flex items-start gap-3 transition-colors ${
                                  isCorrect
                                    ? 'bg-ok/20 border-ok/40 text-ok-soft'
                                    : 'bg-field border-line text-ink-3'
                                }`}
                              >
                                <span
                                  className={`w-6 h-6 rounded-lg flex items-center justify-center font-bold text-xs shrink-0 ${
                                    isCorrect ? 'bg-ok text-ink' : 'bg-ink-2 text-ink'
                                  }`}
                                >
                                  {opt.key}
                                </span>
                                <span className="pt-0.5 leading-relaxed">{opt.text}</span>
                              </div>
                            );
                          })}
                        </div>
                      </div>

                      {/* Gerekçeli Açıklama */}
                      {cluster.explanation && (
                        <div className="space-y-1.5">
                          <div className="font-bold text-ink-3 uppercase tracking-wider text-2xs">
                            Fizyopatolojik Gerekçe & Çözüm:
                          </div>
                          <div className="p-3 rounded-xl bg-field border border-line text-ink-3 leading-relaxed">
                            {cluster.explanation}
                          </div>
                        </div>
                      )}

                      {/* Birleştirilen Kaynak Soru Kimlikleri */}
                      <div className="pt-2 border-t border-line text-2xs text-ink-3">
                        <span className="font-semibold text-ink-3">Birleştirilen Soru Parçaları ({cluster.sourceQuestionIds.length}): </span>
                        {cluster.sourceQuestionIds.join(', ')}
                      </div>

                      {/* Öğrenci Katkıları & Eklemeler */}
                      <div className="pt-3 border-t border-line space-y-3">
                        <div className="flex items-center justify-between">
                          <h5 className="font-bold text-ok text-xs flex items-center gap-1.5">
                            <MessageSquare className="w-3.5 h-3.5" />
                            <span>Öğrenci Katkıları & Eklemeler ({cluster.studentContributions?.length || 0})</span>
                          </h5>
                          <span className="text-2xs text-ink-3">Yalnızca ekleme yapılabilir</span>
                        </div>

                        {cluster.studentContributions && cluster.studentContributions.length > 0 ? (
                          <div className="space-y-2">
                            {cluster.studentContributions.map(contrib => (
                              <div
                                key={contrib.id}
                                className="p-3 rounded-xl bg-field border border-line space-y-1"
                              >
                                <div className="flex items-center justify-between text-2xs text-ok font-semibold">
                                  <span>{contrib.studentName}</span>
                                  <span className="text-ink-3 font-normal">
                                    {new Date(contrib.createdAt).toLocaleDateString('tr-TR')}
                                  </span>
                                </div>
                                <p className="text-ink-3 leading-relaxed text-xs">{contrib.text}</p>
                              </div>
                            ))}
                          </div>
                        ) : (
                          <p className="text-ink-3 text-xs italic">
                            Bu taslağa henüz öğrenci eklemesi yapılmamış. İlk eklemeyi siz yapabilirsiniz.
                          </p>
                        )}

                        {/* Katkı Ekleme Alanı */}
                        <div className="flex gap-2 mt-2">
                          <input
                            type="text"
                            value={contributionTexts[cluster.id] || ''}
                            onChange={e =>
                              setContributionTexts(prev => ({ ...prev, [cluster.id]: e.target.value }))
                            }
                            placeholder="Bu taslağa ekleme veya hatırlatma notu ekle..."
                            className="flex-1 px-3.5 py-2 rounded-xl bg-canvas border border-line text-ink text-xs placeholder-ink-3 focus:outline-none focus:border-ok"
                            onKeyDown={e => {
                              if (e.key === 'Enter') handleAddContribution(cluster.id);
                            }}
                          />
                          <button
                            type="button"
                            disabled={submittingContribId === cluster.id || !(contributionTexts[cluster.id] || '').trim()}
                            onClick={() => handleAddContribution(cluster.id)}
                            className="px-4 py-2 bg-ok hover:bg-ok disabled:opacity-50 text-white font-bold rounded-xl text-xs flex items-center gap-1.5 transition-all shrink-0"
                          >
                            <Send className="w-3.5 h-3.5" />
                            <span>Ekle</span>
                          </button>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
};
