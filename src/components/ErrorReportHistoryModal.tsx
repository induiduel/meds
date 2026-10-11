import React, { useState } from 'react';
import { confirmDialog } from './ui/ConfirmDialog';
import {
  X,
  History,
  CheckCircle2,
  Clock,
  Sparkles,
  ExternalLink,
  ShieldCheck,
  User,
  Calendar,
  BadgeCheck,
  Pencil,
  Trash2,
} from 'lucide-react';
import { QuestionItem } from '../types';
import { AppUser, ADMIN_EMAIL } from '../services/auth';
import { buildUniversalReportUrl } from '../services/universalRedirectService';
import { ApiService } from '../services/api';

interface ErrorReportHistoryModalProps {
  isOpen: boolean;
  onClose: () => void;
  question: QuestionItem | null;
  currentUser?: AppUser | null;
  onQuestionUpdated?: (q: QuestionItem) => void;
}

export const ErrorReportHistoryModal: React.FC<ErrorReportHistoryModalProps> = ({
  isOpen,
  onClose,
  question,
  currentUser,
  onQuestionUpdated,
}) => {
  const [editingReportId, setEditingReportId] = useState<string | null>(null);
  const [editReason, setEditReason] = useState('');
  const [editDetails, setEditDetails] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [busyAction, setBusyAction] = useState<string | null>(null);

  if (!isOpen || !question) return null;

  const isAdmin = currentUser?.email === ADMIN_EMAIL || !!currentUser?.isAdmin;

  const getMyReportIds = (): string[] => {
    try {
      const raw = localStorage.getItem('my_report_ids');
      return raw ? JSON.parse(raw) : [];
    } catch {
      return [];
    }
  };

  const canManageReport = (rep: any): boolean => {
    if (isAdmin) return true;
    if (!rep) return false;
    if (currentUser?.uid && rep.reporterUid === currentUser.uid) return true;
    if (currentUser?.email && rep.reporterEmail && rep.reporterEmail.toLowerCase() === currentUser.email.toLowerCase()) return true;
    if (currentUser?.displayName && rep.reportedBy && rep.reportedBy.trim().toLowerCase() === currentUser.displayName.trim().toLowerCase()) return true;
    if (getMyReportIds().includes(rep.id)) return true;
    return false;
  };

  const handleStartEdit = (rep: any) => {
    setEditingReportId(rep.id);
    setEditReason(rep.reason || '');
    setEditDetails(rep.details || '');
  };

  const handleSaveEdit = async (repId: string) => {
    if (!editReason.trim()) return;
    setIsSubmitting(true);
    try {
      const res = await ApiService.editPastReport(
        String(question.id),
        repId,
        { reason: editReason.trim(), details: editDetails.trim() },
        {
          uid: currentUser?.uid,
          email: currentUser?.email ?? undefined,
          reportedBy: currentUser?.displayName ?? undefined,
          adminEmail: isAdmin ? (currentUser?.email || ADMIN_EMAIL) : undefined,
        }
      );
      if (res.success) {
        const updatedReports = (question.reports || []).map((r) =>
          r.id === repId ? { ...r, reason: editReason.trim(), details: editDetails.trim(), isEdited: true, updatedAt: new Date().toISOString() } : r
        );
        const updatedQuestion = { ...question, reports: updatedReports };
        if (onQuestionUpdated) onQuestionUpdated(updatedQuestion);
        setEditingReportId(null);
      } else {
        alert(res.message || 'Düzenleme kaydedilemedi.');
      }
    } catch (e: any) {
      alert('Hata: ' + (e.message || 'Bağlantı hatası'));
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDeleteReport = async (repId: string) => {
    if (!(await confirmDialog({ title: 'Hata bildirimi silinsin mi?', message: 'Bildirim veritabanından ve işlem kuyruklarından kalıcı olarak silinir.', confirmLabel: 'Kalıcı sil', tone: 'danger' }))) {
      return;
    }
    setBusyAction(`del-${repId}`);
    try {
      const res = await ApiService.deletePastReport(
        String(question.id),
        repId,
        {
          uid: currentUser?.uid,
          email: currentUser?.email ?? undefined,
          reportedBy: currentUser?.displayName ?? undefined,
          adminEmail: isAdmin ? (currentUser?.email || ADMIN_EMAIL) : undefined,
        }
      );
      if (res.success) {
        const updatedReports = (question.reports || []).filter((r) => r.id !== repId);
        const updatedQuestion = { ...question, reports: updatedReports };
        if (onQuestionUpdated) onQuestionUpdated(updatedQuestion);
      } else {
        alert(res.message || 'Bildirim silinemedi.');
      }
    } catch (e: any) {
      alert('Hata: ' + (e.message || 'Bağlantı hatası'));
    } finally {
      setBusyAction(null);
    }
  };

  const reports = question.reports || [];
  const revisions = question.revisions || [];

  const totalReports = reports.length;
  const resolvedReports = reports.filter(
    (r) => r.status === 'resolved' || r.status === 'verified_correct'
  ).length;
  const pendingReports = totalReports - resolvedReports;

  // Doğrudan yönlendirme bağlantısı
  const directUrl = buildUniversalReportUrl({
    type: question.isPastExam ? 'past_question' : 'practice_question',
    targetId: String(question.id),
  });

  return (
    <div
      className="ms-overlay fixed inset-0 z-50 flex items-center justify-center p-4 bg-[var(--color-scrim)] animate-fadeIn"
      onClick={onClose}
    >
      <div
        className="ms-modal-panel bg-white rounded-2xl shadow-2xl border border-line w-full max-w-3xl max-h-[90dvh] flex flex-col overflow-hidden relative"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Modal Başlığı */}
        <div className="bg-ink p-5 text-white flex items-center justify-between shrink-0">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-accent/20 text-accent border border-accent/30">
              <History className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="font-bold text-base leading-tight">
                  Hata Bildirimi & Değişim Geçmişi
                </h3>
                <span className="text-2xs font-mono px-2 py-0.5 rounded bg-white/10 text-ink-3">
                  #{question.id}
                </span>
              </div>
              <p className="text-xs text-ink-3 mt-0.5">
                {question.isUnassignedNumber ? 'Numarasız Soru' : `Soru #${question.questionNumber || '–'}`}
                {question.discipline && ` • ${question.discipline}`}
                {question.examYear && ` • ${question.examYear}`}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <a
              href={directUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="p-1.5 rounded-lg text-ink-3 hover:text-white hover:bg-white/10 transition-colors"
              title="Bu soruyu yeni sekmede aç"
            >
              <ExternalLink className="w-4 h-4" />
            </a>
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-ink-3 hover:text-white hover:bg-white/10 transition-colors"
              title="Kapat"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Durum Özeti Çubuğu */}
        <div className="bg-field border-b border-line px-5 py-3 text-xs text-ink-2 flex flex-wrap items-center justify-between gap-3 shrink-0">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-1.5 font-medium">
              <span className="text-ink-3">Toplam Bildirim:</span>
              <strong className="text-ink">{totalReports}</strong>
            </div>

            <div className="flex items-center gap-1.5 font-semibold text-ok">
              <CheckCircle2 className="w-4 h-4 text-ok" />
              <span>{resolvedReports} Onarıldı & Çözüldü</span>
            </div>

            {pendingReports > 0 && (
              <div className="flex items-center gap-1.5 font-semibold text-warn">
                <Clock className="w-4 h-4 text-warn" />
                <span>{pendingReports} İnceleniyor</span>
              </div>
            )}
          </div>

          <div className="flex items-center gap-1 text-2xs text-ink-3 font-medium">
            <ShieldCheck className="w-3.5 h-3.5 text-accent" />
            <span>Tüm değişimler çift taraflı loglanır</span>
          </div>
        </div>

        {/* Bildirim & Düzenleme Listesi */}
        <div className="p-6 overflow-y-auto space-y-4 flex-1">
          {reports.length === 0 && revisions.length === 0 ? (
            <div className="text-center py-12 text-ink-3 space-y-2">
              <ShieldCheck className="w-10 h-10 mx-auto text-ok/60" />
              <p className="text-sm font-semibold text-ink-2">Bu soruda aktif hata bildirimi bulunmuyor.</p>
              <p className="text-xs text-ink-3">Soru tıbbi olarak incelenmiş ve doğrulanmıştır.</p>
            </div>
          ) : (
            reports.map((report, idx) => {
              const isResolved = report.status === 'resolved' || report.status === 'verified_correct';
              const ticketNum = report.ticketNo || `#${String(reports.length - idx).padStart(6, '0')}`;

              return (
                <div
                  key={report.id || idx}
                  className={`rounded-xl border p-4.5 transition-all space-y-3.5 ${
                    isResolved
                      ? 'bg-white border-line shadow-xs hover:border-line-2'
                      : 'bg-warn-soft/40 border-warn/30 shadow-xs'
                  }`}
                >
                  {/* Bildirim Kartı Başlığı */}
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-2.5 border-b border-line">
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-xs font-bold px-2 py-0.5 rounded bg-field text-ink border border-line">
                        {ticketNum} Nolu Hata Bildirimi
                      </span>
                      {isResolved ? (
                        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-2xs font-semibold bg-ok-soft text-ok border border-ok/30">
                          <CheckCircle2 className="w-3 h-3" /> Onarıldı & Çözüldü
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-2xs font-semibold bg-warn-soft text-warn border border-warn/30">
                          <Clock className="w-3 h-3" /> İnceleniyor
                        </span>
                      )}
                    </div>

                    <div className="flex items-center gap-3 text-2xs text-ink-3">
                      <span className="flex items-center gap-1">
                        <User className="w-3 h-3 text-ink-3" />
                        {report.reportedBy || 'Tıp Öğrencisi'}
                      </span>
                      {report.reportedAt && (
                        <span className="flex items-center gap-1">
                          <Calendar className="w-3 h-3 text-ink-3" />
                          {new Date(report.reportedAt).toLocaleDateString('tr-TR', {
                            day: 'numeric',
                            month: 'short',
                            year: 'numeric',
                            hour: '2-digit',
                            minute: '2-digit',
                          })}
                        </span>
                      )}

                      {/* Bildirimi Yönetme Butonları (Sahibi veya Admin) */}
                      {canManageReport(report) && editingReportId !== report.id && (
                        <div className="flex items-center gap-1 ml-2 border-l border-line pl-2">
                          <button
                            type="button"
                            onClick={() => handleStartEdit(report)}
                            className="p-1 rounded hover:bg-line text-ink-2 hover:text-accent transition-colors"
                            title="Bildirimimi Düzenle"
                          >
                            <Pencil className="w-3.5 h-3.5" />
                          </button>
                          <button
                            type="button"
                            disabled={busyAction === `del-${report.id}`}
                            onClick={() => report.id && handleDeleteReport(report.id)}
                            className="p-1 rounded hover:bg-bad-soft text-ink-3 hover:text-bad-text transition-colors"
                            title="Bildirimimi Veritabanından Kalıcı Olarak Sil"
                          >
                            <Trash2 className="w-3.5 h-3.5" />
                          </button>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Eğer Düzenleme Modundaysa Form Göster */}
                  {editingReportId === report.id ? (
                    <div className="bg-field p-3 rounded-xl border border-accent/30 space-y-2.5 animate-fadeIn">
                      <div>
                        <label className="text-2xs font-semibold text-ink-2 block mb-1">Bildirim Başlığı / Sebep:</label>
                        <input
                          type="text"
                          value={editReason}
                          onChange={(e) => setEditReason(e.target.value)}
                          className="w-full text-xs px-2.5 py-1.5 rounded-lg border border-line-2 focus:border-accent outline-none"
                          placeholder="Bildirim konusu..."
                        />
                      </div>
                      <div>
                        <label className="text-2xs font-semibold text-ink-2 block mb-1">Ayrıntılı Şikayet / Açıklama:</label>
                        <textarea
                          value={editDetails}
                          onChange={(e) => setEditDetails(e.target.value)}
                          rows={3}
                          className="w-full text-xs p-2.5 rounded-lg border border-line-2 focus:border-accent outline-none resize-y"
                          placeholder="Hatanın ayrıntılarını yazın..."
                        />
                      </div>
                      <div className="flex items-center justify-end gap-2 pt-1">
                        <button
                          type="button"
                          onClick={() => setEditingReportId(null)}
                          className="px-2.5 py-1 rounded text-xs text-ink-2 hover:bg-line"
                        >
                          Vazgeç
                        </button>
                        <button
                          type="button"
                          disabled={isSubmitting || !editReason.trim()}
                          onClick={() => report.id && handleSaveEdit(report.id)}
                          className="px-3 py-1 rounded text-xs font-semibold bg-accent hover:bg-accent text-white disabled:opacity-50"
                        >
                          {isSubmitting ? 'Kaydediliyor…' : 'Kaydet'}
                        </button>
                      </div>
                    </div>
                  ) : (
                    /* Kullanıcının Şikayeti */
                    <div className="space-y-1">
                      <div className="text-xs font-semibold text-ink flex items-center gap-2">
                        <span className="text-accent">Bildirim Konusu:</span>
                        <span>{report.reason}</span>
                        {(report as any).isEdited && (
                          <span className="text-2xs text-ink-3 font-normal italic">(düzenlendi)</span>
                        )}
                      </div>
                      {report.details && (
                        <p className="text-xs text-ink-2 bg-field p-2.5 rounded-lg border border-line font-sans italic">
                          “{report.details}”
                        </p>
                      )}
                    </div>
                  )}

                  {/* Çözüm ve Yapılan Değişiklik Raporu (Eğer Onarıldıysa) */}
                  {isResolved && (
                    <div className="bg-ok-soft/50 rounded-xl p-3.5 border border-ok/30 space-y-2 text-xs">
                      <div className="flex items-center justify-between text-ok font-bold">
                        <div className="flex items-center gap-1.5">
                          <Sparkles className="w-4 h-4 text-ok" />
                          <span>Çözüm Raporu ({report.resolvedBy || 'Yapay Zekâ Onarımı'})</span>
                        </div>
                        {report.resolvedAt && (
                          <span className="text-2xs text-ok font-normal">
                            {new Date(report.resolvedAt).toLocaleDateString('tr-TR', {
                              day: 'numeric',
                              month: 'short',
                              year: 'numeric',
                              hour: '2-digit',
                              minute: '2-digit',
                            })}
                          </span>
                        )}
                      </div>

                      {report.resolutionSummary && (
                        <div className="text-ink font-medium bg-white p-2 rounded border border-ok/60">
                          {report.resolutionSummary}
                        </div>
                      )}

                      {report.medicalReasoning && (
                        <div className="text-ink-2 bg-white/70 p-2 rounded border border-ok/40 text-2xs">
                          <strong className="text-ok block mb-0.5">Tıbbi Gerekçe & Kanıt:</strong>
                          {report.medicalReasoning}
                        </div>
                      )}

                      {report.detectedIssues && report.detectedIssues.length > 0 && (
                        <div>
                          <span className="text-2xs font-semibold text-ok">Düzeltilen Hususlar:</span>
                          <ul className="list-disc list-inside mt-0.5 text-ink-2 space-y-0.5 text-2xs">
                            {report.detectedIssues.map((issue, i) => (
                              <li key={i}>{issue}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              );
            })
          )}

          {/* Soru Sürüm Revizyonları (Revisions) */}
          {revisions.length > 0 && (
            <div className="pt-4 border-t border-line space-y-3">
              <h4 className="text-xs font-bold text-ink-2 uppercase tracking-wider flex items-center gap-1.5">
                <BadgeCheck className="w-4 h-4 text-accent" />
                <span>Kayıtlı Versiyon ve Düzenleme Kronolojisi</span>
              </h4>

              <div className="space-y-2">
                {[...revisions].reverse().map((rev, rIdx) => (
                  <div
                    key={rev.id || rIdx}
                    className="p-3 bg-field rounded-lg border border-line text-xs flex flex-col sm:flex-row sm:items-center justify-between gap-2"
                  >
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-semibold text-ink">
                          Versiyon #{rev.version || revisions.length - rIdx}
                        </span>
                        {rev.ticketNo && (
                          <span className="font-mono text-2xs text-accent bg-accent-soft px-1.5 py-0.2 rounded border border-accent/30">
                            {rev.ticketNo}
                          </span>
                        )}
                        <span className="text-ink-3 font-medium">· {rev.changeSummary || 'Düzenleme yapıldı'}</span>
                      </div>
                      <div className="text-2xs text-ink-3 mt-0.5">
                        Düzenleyen: <strong>{rev.editorName}</strong>
                      </div>
                    </div>

                    <div className="text-2xs text-ink-3 self-end sm:self-center font-mono">
                      {new Date(rev.editedAt).toLocaleString('tr-TR', {
                        day: 'numeric',
                        month: 'short',
                        year: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit',
                      })}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Modal Alt Çubuğu */}
        <div className="p-4 bg-field border-t border-line flex items-center justify-between gap-3 shrink-0">
          <a
            href={directUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="ms-btn text-xs text-accent bg-accent-soft hover:bg-accent-soft border border-accent/30 flex items-center gap-1.5 font-medium"
          >
            <span>Bu Soruyu Sitede Aç & Doğrula</span>
            <ExternalLink className="w-3.5 h-3.5 text-accent" />
          </a>

          <button
            type="button"
            onClick={onClose}
            className="ms-btn is-ghost text-xs font-semibold px-4 py-1.5"
          >
            Kapat
          </button>
        </div>
      </div>
    </div>
  );
};
