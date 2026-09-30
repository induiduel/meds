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
import { AppUser, FIREBASE_CONSOLE_URL, setCustomAccessToken } from '../services/auth';

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
          'Google oturumu açılamadı. GitHub Pages için Firebase Console yetkili alan adlarına induiduel.github.io eklenmelidir.'
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
    <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 overflow-y-auto">
      <div className="bg-white rounded-2xl max-w-lg w-full shadow-2xl border border-slate-200 overflow-hidden my-6 flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="bg-gradient-to-r from-teal-800 to-teal-900 text-white p-5 flex items-center justify-between shrink-0">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-white/10 text-white border border-white/20 flex items-center justify-center">
              <Cloud className="w-6 h-6 text-teal-300" />
            </div>
            <div>
              <h3 className="font-bold text-base">Soru Kitapçığını PDF & Drive'a Kaydet</h3>
              <p className="text-xs text-teal-200">
                {committee?.name || 'Kurul Sınavı'} ({questions.length} Soru)
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-teal-200 hover:text-white hover:bg-white/10 cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-5 overflow-y-auto text-xs text-slate-700 leading-relaxed">
          {/* Threshold status badge */}
          <div className="bg-slate-50 border border-slate-200 rounded-xl p-3.5 space-y-2">
            <div className="flex items-center justify-between text-xs">
              <span className="font-semibold text-slate-700 flex items-center gap-1.5">
                <Sparkles className="w-4 h-4 text-amber-500" />
                Otomatik Drive Eşiği Durumu
              </span>
              <span className={`font-bold px-2 py-0.5 rounded text-[10px] ${
                threshold.isThresholdMet 
                  ? 'bg-emerald-100 text-emerald-800' 
                  : 'bg-amber-100 text-amber-800'
              }`}>
                {threshold.isThresholdMet ? 'EŞİK KARŞILANDI' : `%${threshold.percentageMet} TAMAMLANDI`}
              </span>
            </div>
            <p className="text-[11px] text-slate-600">
              {threshold.summary}
            </p>
            <div className="w-full bg-slate-200 rounded-full h-1.5 overflow-hidden">
              <div
                className={`h-full transition-all duration-500 ${
                  threshold.isThresholdMet ? 'bg-emerald-600' : 'bg-amber-500'
                }`}
                style={{ width: `${threshold.percentageMet}%` }}
              />
            </div>
          </div>

          {/* Success state */}
          {uploadSuccessResult && (
            <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-4 space-y-2.5">
              <div className="flex items-center gap-2 text-emerald-800 font-bold text-xs">
                <CheckCircle2 className="w-5 h-5 text-emerald-600" />
                <span>PDF Başarıyla Google Drive'a Yüklendi!</span>
              </div>
              <p className="text-[11px] text-emerald-950">
                Dosya Google Drive hesabınızdaki <strong>"{FOLDER_NAME}"</strong> klasörüne kaydedildi.
              </p>
              {uploadSuccessResult.webViewLink && (
                <a
                  href={uploadSuccessResult.webViewLink}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1.5 bg-emerald-700 hover:bg-emerald-800 text-white font-bold px-3 py-1.5 rounded-lg text-xs"
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
            <div className="bg-rose-50 border border-rose-200 rounded-xl p-3.5 space-y-1.5">
              <div className="flex items-center gap-2 text-rose-800 font-bold text-xs">
                <AlertCircle className="w-4 h-4 text-rose-600" />
                <span>Drive Yükleme Bildirimi</span>
              </div>
              <p className="text-[11px] text-rose-950 leading-normal">
                {uploadError}
              </p>
            </div>
          )}

          {/* Option 1: Direct Local PDF Download (Instant & Always Works) */}
          <div className="border border-slate-200 rounded-xl p-4 space-y-2.5 bg-white shadow-2xs hover:border-teal-400 transition-colors">
            <div className="flex items-center justify-between">
              <h4 className="font-bold text-slate-900 flex items-center gap-1.5 text-xs">
                <Download className="w-4 h-4 text-teal-700" />
                1. Seçenek: Cihazınıza PDF İndir (Anında & İnternetsiz)
              </h4>
              <span className="bg-teal-50 text-teal-700 text-[10px] font-bold px-2 py-0.5 rounded-full border border-teal-200">
                1 Tıkla Hazır
              </span>
            </div>
            <p className="text-[11px] text-slate-600">
              Tüm soruları, rekonstrüksiyonları, şıkları ve cevap anahtarını içeren A4 baskıya hazır PDF kitapçığını bilgisayarınıza veya telefonunuza anında kaydeder. Google girişi gerektirmez.
            </p>
            <button
              onClick={handleDownloadLocally}
              className="w-full bg-teal-700 hover:bg-teal-800 text-white font-bold py-2 px-4 rounded-lg flex items-center justify-center gap-2 text-xs shadow-xs cursor-pointer active:scale-98 transition-transform"
            >
              <FileText className="w-4 h-4" />
              <span>PDF Kitapçığını Hemen Bilgisayara / Telefona İndir</span>
            </button>
          </div>

          {/* Option 2: Upload to Google Drive Folder */}
          <div className="border border-slate-200 rounded-xl p-4 space-y-3 bg-white shadow-2xs hover:border-teal-400 transition-colors">
            <div className="flex items-center justify-between">
              <h4 className="font-bold text-slate-900 flex items-center gap-1.5 text-xs">
                <Cloud className="w-4 h-4 text-teal-700" />
                2. Seçenek: Google Drive Klasörüne Kaydet
              </h4>
              <span className="bg-slate-100 text-slate-700 text-[10px] font-medium px-2 py-0.5 rounded">
                Bulut Arşiv
              </span>
            </div>
            <p className="text-[11px] text-slate-600">
              Google Drive hesabınızda <strong>"{FOLDER_NAME}"</strong> adında bir klasör açar ve PDF'i oraya yedekler.
            </p>

            {accessToken ? (
              <button
                onClick={handleUploadDrive}
                disabled={isUploading}
                className="w-full bg-slate-900 hover:bg-slate-800 text-white font-bold py-2 px-4 rounded-lg flex items-center justify-center gap-2 text-xs shadow-xs cursor-pointer active:scale-98 transition-all disabled:opacity-50"
              >
                {isUploading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin text-teal-300" />
                    <span>Google Drive'a Yükleniyor...</span>
                  </>
                ) : (
                  <>
                    <Cloud className="w-4 h-4 text-teal-300" />
                    <span>Google Drive Klasörüne Yedekle</span>
                  </>
                )}
              </button>
            ) : (
              <div className="space-y-2">
                <button
                  onClick={handleUploadDrive}
                  disabled={isUploading}
                  className="w-full bg-white hover:bg-slate-50 border border-slate-300 text-slate-800 font-semibold py-2 px-4 rounded-lg flex items-center justify-center gap-2 text-xs shadow-xs cursor-pointer"
                >
                  <svg className="w-4 h-4" viewBox="0 0 24 24">
                    <path
                      fill="#4285F4"
                      d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.8-2.4 3.66v3.05h3.88c2.27-2.09 3.66-5.17 3.66-9.15z"
                    />
                    <path
                      fill="#34A853"
                      d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.87-3.05c-1.08.72-2.45 1.16-4.06 1.16-3.13 0-5.78-2.11-6.73-4.96H1.25v3.15C3.26 21.36 7.36 24 12 24z"
                    />
                    <path
                      fill="#FBBC05"
                      d="M5.27 14.24c-.25-.72-.38-1.49-.38-2.24s.13-1.52.38-2.24V6.61H1.25C.45 8.24 0 10.07 0 12s.45 3.76 1.25 5.39l4.02-3.15z"
                    />
                    <path
                      fill="#EA4335"
                      d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.36 0 3.26 2.64 1.25 6.61l4.02 3.15c.95-2.85 3.6-4.96 6.73-4.96z"
                    />
                  </svg>
                  <span>Google ile Oturum Aç & Drive'a Yükle</span>
                </button>

                <p className="text-[10px] text-amber-800 bg-amber-50 p-2 rounded border border-amber-200 flex items-start gap-1.5">
                  <ShieldAlert className="w-3.5 h-3.5 text-amber-600 shrink-0 mt-0.5" />
                  <span>
                    GitHub Pages üzerinden Google Drive'a doğrudan yükleyebilmek için Firebase Console'da <strong>induiduel.github.io</strong> alan adının ekli olması gerekir.
                  </span>
                </p>
              </div>
            )}

            {/* Manual token input option */}
            <div className="pt-1">
              <button
                type="button"
                onClick={() => setShowTokenInput(!showTokenInput)}
                className="text-[10px] text-slate-500 hover:text-slate-800 underline flex items-center gap-1 cursor-pointer"
              >
                <Key className="w-3 h-3" />
                <span>{showTokenInput ? 'Belirteç alanını gizle' : 'Google OAuth Access Token ile yüklemek ister misiniz?'}</span>
              </button>

              {showTokenInput && (
                <div className="mt-2 space-y-1.5 bg-slate-50 p-2.5 rounded-lg border border-slate-200">
                  <input
                    type="password"
                    placeholder="ya29.a0AfH6SM..."
                    value={tokenInput}
                    onChange={(e) => setTokenInput(e.target.value)}
                    className="w-full bg-white border border-slate-300 rounded p-1.5 font-mono text-[10px]"
                  />
                  <div className="flex justify-between items-center text-[10px] text-slate-500">
                    <span>Google Drive scope içeren geçici belirteç</span>
                    <button
                      onClick={handleUploadDrive}
                      disabled={!tokenInput.trim() || isUploading}
                      className="bg-teal-700 hover:bg-teal-800 text-white font-bold px-2 py-1 rounded cursor-pointer disabled:opacity-50"
                    >
                      Token ile Yükle
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 bg-slate-50 border-t border-slate-200 flex items-center justify-between shrink-0">
          <button
            onClick={handleDownloadLocally}
            className="text-xs font-semibold text-teal-800 hover:underline flex items-center gap-1 cursor-pointer"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Direkt PDF İndir</span>
          </button>
          <button
            onClick={onClose}
            className="bg-slate-800 hover:bg-slate-900 text-white font-bold px-4 py-1.5 rounded-lg text-xs cursor-pointer"
          >
            Kapat
          </button>
        </div>
      </div>
    </div>
  );
};
