import React, { useState } from 'react';
import { 
  X, 
  Cloud, 
  Download, 
  CheckCircle2, 
  AlertCircle, 
  ExternalLink, 
  FileText, 
  Sparkles,
  Loader2,
  FolderOpen,
  Key,
  ShieldAlert
} from 'lucide-react';
import { Committee, QuestionItem } from '../types';
import { 
  uploadBookletPdfToDrive, 
  downloadBookletPdfLocally, 
  evaluateAutoBackupThreshold, 
  FOLDER_NAME,
  ThresholdStatus 
} from '../services/drive';
import { AppUser, setCustomAccessToken } from '../services/auth';

interface DriveSaveModalProps {
  isOpen: boolean;
  onClose: () => void;
  committee: Committee | undefined;
  questions: QuestionItem[];
  currentUser: AppUser | null;
  accessToken: string | null;
  onGoogleSignIn: () => Promise<void>;
  onUploadSuccess: (link: string, fileName: string) => void;
}

export const DriveSaveModal: React.FC<DriveSaveModalProps> = ({
  isOpen,
  onClose,
  committee,
  questions,
  currentUser,
  accessToken,
  onGoogleSignIn,
  onUploadSuccess,
}) => {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [uploadSuccessResult, setUploadSuccessResult] = useState<{
    fileName: string;
    webViewLink?: string;
  } | null>(null);
  const [tokenInput, setTokenInput] = useState('');
  const [showTokenInput, setShowTokenInput] = useState(false);

  if (!isOpen) return null;

  const threshold: ThresholdStatus = evaluateAutoBackupThreshold(
    questions,
    committee?.targetCount || 100
  );

  const handleDownloadLocally = () => {
    downloadBookletPdfLocally(committee, questions);
  };

  const handleUploadDrive = async () => {
    setUploadError(null);

    let activeToken = accessToken;

    // If user provided a manual token in the input
    if (tokenInput.trim()) {
      activeToken = tokenInput.trim();
      setCustomAccessToken(activeToken);
    }

    if (!activeToken) {
      try {
        await onGoogleSignIn();
        return;
      } catch (e: any) {
        setUploadError(
          'Google oturumu açılamadı. Canlı alan adı için Firebase Console yetkili alan adlarına nofrostlife.com.tr eklenmelidir.'
        );
        return;
      }
    }

    setIsUploading(true);
    try {
      const result = await uploadBookletPdfToDrive({
        committee,
        questions,
        accessToken: activeToken,
      });

      setUploadSuccessResult({
        fileName: result.fileName,
        webViewLink: result.webViewLink,
      });

      onUploadSuccess(result.webViewLink || '', result.fileName);
    } catch (err: any) {
      console.error('Drive upload failed:', err);
      setUploadError(err.message || 'Google Drive yükleme işlemi sırasında hata oluştu.');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="ms-overlay fixed inset-0 z-50 bg-[var(--color-scrim)] flex items-center justify-center p-4 overflow-y-auto">
      <div className="ms-modal-panel bg-white rounded-2xl max-w-lg w-full shadow-2xl border border-line overflow-hidden my-6 flex flex-col max-h-[90dvh]">
        {/* Header */}
        <div className="bg-white text-ink p-5 flex items-center justify-between shrink-0">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-white/10 text-ink border border-white/20 flex items-center justify-center">
              <Cloud className="w-6 h-6 text-ok" />
            </div>
            <div>
              <h3 className="font-bold text-base">Soru Kitapçığını PDF Olarak Kaydet</h3>
              <p className="text-xs text-ok-soft">
                {committee?.name || 'Kurul Sınavı'} ({questions.length} Soru)
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-ok-soft hover:text-ink hover:bg-white/10 cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-5 overflow-y-auto text-xs text-ink-2 leading-relaxed">
          {/* Threshold status badge */}
          <div className="bg-field border border-line rounded-xl p-3.5 space-y-2">
            <div className="flex items-center justify-between text-xs">
              <span className="font-semibold text-ink-2 flex items-center gap-1.5">
                <Sparkles className="w-4 h-4 text-warn" />
                Otomatik Drive Eşiği Durumu
              </span>
              <span className={`font-bold px-2 py-0.5 rounded text-2xs ${
                threshold.isThresholdMet 
                  ? 'bg-ok-soft text-ok' 
                  : 'bg-warn-soft text-warn'
              }`}>
                {threshold.isThresholdMet ? 'EŞİK KARŞILANDI' : `%${threshold.percentageMet} TAMAMLANDI`}
              </span>
            </div>
            <p className="text-2xs text-ink-2">
              {threshold.summary}
            </p>
            <div className="w-full bg-line rounded-full h-1.5 overflow-hidden">
              <div
                className={`h-full transition-all duration-500 ${
                  threshold.isThresholdMet ? 'bg-ok' : 'bg-warn'
                }`}
                style={{ width: `${threshold.percentageMet}%` }}
              />
            </div>
          </div>

          {/* Success state */}
          {uploadSuccessResult && (
            <div className="bg-ok-soft border border-ok/30 rounded-xl p-4 space-y-2.5">
              <div className="flex items-center gap-2 text-ok font-bold text-xs">
                <CheckCircle2 className="w-5 h-5 text-ok" />
                <span>PDF Başarıyla Google Drive'a Yüklendi!</span>
              </div>
              <p className="text-2xs text-ok">
                Dosya Google Drive hesabınızdaki <strong>"{FOLDER_NAME}"</strong> klasörüne kaydedildi.
              </p>
              {uploadSuccessResult.webViewLink && (
                <a
                  href={uploadSuccessResult.webViewLink}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1.5 bg-ok hover:bg-ok text-white font-bold px-3 py-1.5 rounded-lg text-xs"
                >
                  <FolderOpen className="w-3.5 h-3.5" />
                  <span>Google Drive'da Görüntüle</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              )}
            </div>
          )}

          {/* Error message */}
          {uploadError && (
            <div className="bg-bad-soft border border-bad/30 rounded-xl p-3.5 space-y-1.5">
              <div className="flex items-center gap-2 text-bad-text font-bold text-xs">
                <AlertCircle className="w-4 h-4 text-bad-text" />
                <span>Drive Yükleme Bildirimi</span>
              </div>
              <p className="text-2xs text-bad-text leading-normal">
                {uploadError}
              </p>
            </div>
          )}

          {/* Option 1: Direct Local PDF Download (Instant & Always Works) */}
          <div className="border border-line rounded-xl p-4 space-y-2.5 bg-white shadow-2xs hover:border-ok transition-colors">
            <div className="flex items-center justify-between">
              <h4 className="font-bold text-ink flex items-center gap-1.5 text-xs">
                <Download className="w-4 h-4 text-ok" />
                1. Seçenek: Cihazınıza PDF İndir (Anında & İnternetsiz)
              </h4>
              <span className="bg-ok-soft text-ok text-2xs font-bold px-2 py-0.5 rounded-full border border-ok/30">
                1 Tıkla Hazır
              </span>
            </div>
            <p className="text-2xs text-ink-2">
              Tüm soruları, rekonstrüksiyonları, şıkları ve cevap anahtarını içeren A4 baskıya hazır PDF kitapçığını bilgisayarınıza veya telefonunuza anında kaydeder. Google girişi gerektirmez.
            </p>
            <button
              onClick={handleDownloadLocally}
              className="w-full bg-ok hover:bg-ok text-white font-bold py-2 px-4 rounded-lg flex items-center justify-center gap-2 text-xs shadow-xs cursor-pointer active:scale-98 transition-transform"
            >
              <FileText className="w-4 h-4" />
              <span>PDF Kitapçığını Hemen Bilgisayara / Telefona İndir</span>
            </button>
          </div>

          {/* Google Drive'a yükleme 2026-11-02'de kaldırıldı (Google girişi yok, H466): PDF indirilip istenen yere kaydedilir */}
          <p className="text-2xs text-ink-2 bg-field p-2.5 rounded-lg border border-line">
            Google Drive'a doğrudan yükleme kaldırıldı. PDF'i indirip istediğin klasöre (Drive dahil) kendin kaydedebilirsin.
          </p>
        </div>

        {/* Footer */}
        <div className="p-4 bg-field border-t border-line flex items-center justify-between shrink-0">
          <button
            onClick={handleDownloadLocally}
            className="text-xs font-semibold text-ok hover:underline flex items-center gap-1 cursor-pointer"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Direkt PDF İndir</span>
          </button>
          <button
            onClick={onClose}
            className="bg-white hover:bg-field text-ink font-bold px-4 py-1.5 rounded-lg text-xs cursor-pointer"
          >
            Kapat
          </button>
        </div>
      </div>
    </div>
  );
};
