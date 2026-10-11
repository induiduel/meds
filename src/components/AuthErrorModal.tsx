import React, { useState } from 'react';
import {
  X,
  ShieldAlert,
  ExternalLink,
  Copy,
  KeyRound,
  Globe,
  ShieldCheck,
} from 'lucide-react';
import {
  ADMIN_EMAIL,
  FIREBASE_PROJECT_ID,
  FIREBASE_CONSOLE_URL,
  setLocalAdminSession,
  AppUser,
} from '../services/auth';

interface AuthErrorModalProps {
  isOpen: boolean;
  onClose: () => void;
  onLoginSuccess: (user: AppUser, token: string | null) => void;
}

export const AuthErrorModal: React.FC<AuthErrorModalProps> = ({
  isOpen,
  onClose,
  onLoginSuccess,
}) => {
  const [copied, setCopied] = useState(false);
  const [tokenInput, setTokenInput] = useState('');
  const [showTokenInput, setShowTokenInput] = useState(false);

  if (!isOpen) return null;

  const currentHostname = typeof window !== 'undefined' ? window.location.hostname : 'nofrostlife.com.tr';
  const domainToAuthorize = currentHostname || 'nofrostlife.com.tr';

  const handleBypassAdminLogin = () => {
    const user = setLocalAdminSession(ADMIN_EMAIL, tokenInput ? tokenInput.trim() : undefined);
    onLoginSuccess(user, tokenInput ? tokenInput.trim() : null);
    onClose();
  };

  return (
    <div className="ms-overlay fixed inset-0 z-50 bg-[var(--color-scrim)] flex items-center justify-center p-4 overflow-y-auto">
      <div className="ms-modal-panel bg-white rounded-2xl max-w-xl w-full shadow-2xl border border-line overflow-hidden my-6 flex flex-col max-h-[90dvh]">
        {/* Header */}
        <div className="bg-warn text-white p-5 flex items-center justify-between shrink-0">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-white/20 text-white flex items-center justify-center">
              <ShieldAlert className="w-6 h-6" />
            </div>
            <div>
              <h3 className="font-bold text-base">Firebase Yetkili Alan Adı (Authorized Domain) Uyarısı</h3>
              <p className="text-xs text-warn-soft">
                Hata Kodu: <code className="bg-black/20 px-1 py-0.5 rounded font-mono">auth/unauthorized-domain</code>
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-warn-soft hover:text-white hover:bg-black/10 cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-5 overflow-y-auto text-xs text-ink-2 leading-relaxed">
          <p className="text-ink-2">
            Firebase Authentication güvenlik politikası gereği, uygulamanın çalıştığı alan adını 
            (<strong className="text-ink font-mono">{domainToAuthorize}</strong>) Firebase konsoluna kaydetmeniz gerekir.
          </p>

          {/* Quick Solution 1: Add domain to Firebase Console */}
          <div className="bg-warn-soft/70 border border-warn/30 rounded-xl p-4 space-y-3">
            <h4 className="font-bold text-warn flex items-center gap-1.5 text-xs">
              <Globe className="w-4 h-4 text-warn" />
              1. Kalıcı Çözüm: Alan Adını Firebase'e Ekleyin (1 Dakika)
            </h4>

            <ol className="space-y-2 text-2xs text-warn list-decimal list-inside">
              <li>
                Aşağıdaki butona basarak Firebase Authentication ayarlarını açın:
                <div className="mt-1.5">
                  <a
                    href={FIREBASE_CONSOLE_URL}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1.5 bg-warn hover:bg-warn text-white font-bold px-3 py-1.5 rounded-lg text-xs shadow-xs"
                  >
                    <span>Firebase Konsolunu Aç</span>
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                </div>
              </li>
              <li>
                Açılan sayfada <strong>"Yetkili alan adları" (Authorized domains)</strong> başlığı altındaki <strong>"Alan adı ekle" (Add domain)</strong> butonuna tıklayın.
              </li>
              <li>
                Aşağıdaki alan adlarını tek tek yapıştırıp kaydedin:
                <div className="mt-2 space-y-1.5">
                  {[
                    domainToAuthorize,
                    'nofrostlife.com.tr',
                    'www.nofrostlife.com.tr',
                    'localhost',
                    '127.0.0.1'
                  ]
                    .filter((d, i, arr) => d && arr.indexOf(d) === i)
                    .map((dom) => (
                      <div key={dom} className="flex items-center gap-2 bg-white border border-warn/30 rounded p-1.5 font-mono text-ink text-2xs">
                        <span className="flex-1 font-bold">{dom}</span>
                        <button
                          type="button"
                          onClick={() => {
                            navigator.clipboard.writeText(dom);
                            setCopied(true);
                            setTimeout(() => setCopied(false), 2000);
                          }}
                          className="px-2 py-0.5 rounded bg-warn-soft hover:bg-warn/20 text-warn font-sans text-2xs font-semibold flex items-center gap-1 cursor-pointer"
                        >
                          <Copy className="w-3 h-3" />
                          <span>Kopyala</span>
                        </button>
                      </div>
                    ))}
                </div>
              </li>
            </ol>
          </div>

          {/* Quick Solution 2: Instant Admin Login Bypass */}
          <div className="bg-ok-soft border border-ok/30 rounded-xl p-4 space-y-3">
            <div className="flex items-center justify-between">
              <h4 className="font-bold text-ok flex items-center gap-1.5 text-xs">
                <ShieldCheck className="w-4 h-4 text-ok" />
                2. Beklemeden Devam Et: Yönetici Girişi Yap
              </h4>
              <span className="bg-ok/60 text-ok text-2xs font-bold px-2 py-0.5 rounded-full">
                Hemen Kullan
              </span>
            </div>

            <p className="text-2xs text-ok">
              Firebase ayarlarını yapmadan önce de sisteminizi test etmek ve tüm soruları yönetmek için doğrudan 
              <strong> {ADMIN_EMAIL}</strong> yetkili oturumuyla devam edebilirsiniz.
            </p>

            <button
              onClick={handleBypassAdminLogin}
              className="w-full bg-ok hover:bg-ok text-white font-bold py-2 px-4 rounded-lg flex items-center justify-center gap-2 text-xs shadow-sm cursor-pointer"
            >
              <KeyRound className="w-4 h-4 text-ok" />
              <span>Yönetici Olarak Hemen Giriş Yap ({ADMIN_EMAIL})</span>
            </button>

            {/* Optional Drive access token input */}
            <div className="pt-2 border-t border-ok/60">
              <button
                type="button"
                onClick={() => setShowTokenInput(!showTokenInput)}
                className="text-2xs text-ok hover:text-ok underline cursor-pointer"
              >
                {showTokenInput ? 'Belirteç kutusunu gizle' : 'Google Drive Access Token girmek ister misiniz? (İsteğe bağlı)'}
              </button>
              {showTokenInput && (
                <div className="mt-2 space-y-1">
                  <input
                    type="password"
                    placeholder="ya29.a0AfH6SM..."
                    value={tokenInput}
                    onChange={(e) => setTokenInput(e.target.value)}
                    className="w-full bg-white border border-ok/30 rounded p-1.5 font-mono text-2xs"
                  />
                  <p className="text-2xs text-ok">
                    Google OAuth token girerseniz Drive yüklemelerini doğrudan yapabilirsiniz.
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 bg-field border-t border-line flex items-center justify-between shrink-0">
          <span className="text-2xs text-ink-3">
            Proje ID: <strong className="font-mono">{FIREBASE_PROJECT_ID}</strong>
          </span>
          <button
            onClick={onClose}
            className="bg-ink hover:bg-ink text-white font-bold px-4 py-1.5 rounded-lg text-xs cursor-pointer"
          >
            Kapat
          </button>
        </div>
      </div>
    </div>
  );
};
