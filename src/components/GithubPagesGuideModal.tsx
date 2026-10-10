import React, { useState } from 'react';
import { 
  X, 
  Github, 
  CheckCircle2, 
  AlertCircle, 
  FileCode, 
  Terminal, 
  Globe, 
  Copy, 
  Check,
  ExternalLink,
  Zap,
  Server
} from 'lucide-react';
import { getCustomApiUrl, setCustomApiUrl } from '../services/api';

interface GithubPagesGuideModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const GithubPagesGuideModal: React.FC<GithubPagesGuideModalProps> = ({
  isOpen,
  onClose,
}) => {
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);
  const [customUrl, setCustomUrl] = useState(getCustomApiUrl());
  const [saveSuccess, setSaveSuccess] = useState(false);

  if (!isOpen) return null;

  const copyToClipboard = (text: string, index: number) => {
    navigator.clipboard.writeText(text);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  const handleSaveApiUrl = (e: React.FormEvent) => {
    e.preventDefault();
    setCustomApiUrl(customUrl);
    setSaveSuccess(true);
    setTimeout(() => setSaveSuccess(false), 2500);
  };

  return (
    <div className="ms-overlay fixed inset-0 z-50 bg-ink/60 backdrop-blur-xs flex items-center justify-center p-4 overflow-y-auto">
      <div className="ms-modal-panel bg-white rounded-2xl max-w-2xl w-full shadow-2xl border border-line overflow-hidden my-6 flex flex-col max-h-[90dvh]">
        {/* Header */}
        <div className="bg-ink text-white p-5 flex items-center justify-between shrink-0">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-white/10 text-white border border-white/20 flex items-center justify-center">
              <Github className="w-6 h-6" />
            </div>
            <div>
              <h3 className="font-bold text-base">GitHub Pages Kurulum & Çözüm Rehberi</h3>
              <p className="text-xs text-ink-3">
                "GitHub Pages yaptığımda sayfa açılmıyor / beyaz ekran çıkıyor" Çözümü
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-ink-3 hover:text-white hover:bg-ink cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-5 overflow-y-auto text-xs text-ink-2 leading-relaxed">
          {/* Why it was blank explanation */}
          <div className="bg-bad-soft border border-bad/30 rounded-xl p-4 space-y-2">
            <h4 className="font-bold text-bad-text flex items-center gap-1.5 text-xs">
              <AlertCircle className="w-4 h-4 text-bad-text" />
              Sayfanın Beyaz Kalmasının Kesin Nedeni:
            </h4>
            <p className="text-bad-text text-2xs leading-relaxed">
              GitHub Pages şu anda derlenmiş <code className="bg-bad-soft px-1 py-0.5 rounded font-mono font-bold">dist/</code> klasörü yerine, reponun ana dizinindeki ham kaynak dosyayı (<code className="bg-bad-soft px-1 py-0.5 rounded font-mono">&lt;script src="/src/main.tsx"&gt;</code>) sunuyor.
              Tarayıcılar derlenmemiş ham TypeScript (.tsx) dosyalarını doğrudan çalıştıramadığı için sayfa boş kalmaktadır.
            </p>
          </div>

          {/* Step by step deployment */}
          <div className="space-y-3 pt-1">
            <h4 className="font-bold text-ink text-sm border-b pb-1">
              Bunu Düzeltmenin 2 Yolu (Hangisini İsterseniz):
            </h4>

            {/* Method 1: Change Source to GitHub Actions */}
            <div className="bg-ok-soft/60 border border-ok/30 rounded-xl p-4 space-y-2">
              <span className="bg-ok text-white text-2xs font-bold px-2 py-0.5 rounded-full uppercase tracking-wider">
                Yöntem 1 (Önerilen) • GitHub Ayarından "GitHub Actions"ı Seçmek
              </span>
              <ol className="space-y-1.5 text-2xs text-ok list-decimal list-inside">
                <li>
                  GitHub'da <strong>https://github.com/induiduel/meds</strong> sayfanıza gidin.
                </li>
                <li>
                  Üst sekmelerden <strong>Settings</strong> (Ayarlar) Sol menüden <strong>Pages</strong> seçeneğine tıklayın.
                </li>
                <li>
                  <strong>Build and deployment</strong> bölümündeki <strong>Source</strong> açılır kutusunu bulun:
                  <div className="mt-1 p-2 bg-white rounded border border-ok/30 font-semibold text-ink">
                    Şu anki: "Deploy from a branch"<br />
                    <strong>Bunu Seçin: "GitHub Actions"</strong>
                  </div>
                </li>
                <li>
                  Bunu seçtiğiniz anda GitHub otomatik olarak projeyi derleyip <strong>https://induiduel.github.io/meds/</strong> adresinde sitenizi açacaktır!
                </li>
              </ol>
            </div>

            {/* Method 2: One command npm run deploy */}
            <div className="bg-field border border-line rounded-xl p-4 space-y-2">
              <span className="bg-ink text-white text-2xs font-bold px-2 py-0.5 rounded-full uppercase tracking-wider">
                Yöntem 2 (Terminalden Tek Komutla Canlıya Alma)
              </span>
              <p className="text-2xs text-ink-2">
                Eğer "Deploy from a branch" kullanmaya devam etmek isterseniz, terminalinizde şu komutu çalıştırmanız yeterlidir:
              </p>
              <div className="bg-ink text-ink-3 p-2.5 rounded font-mono text-2xs flex items-center justify-between">
                <span>npm run deploy</span>
                <button
                  onClick={() => copyToClipboard('npm run deploy', 1)}
                  className="text-ink-3 hover:text-white"
                >
                  {copiedIndex === 1 ? <Check className="w-3.5 h-3.5 text-ok" /> : <Copy className="w-3.5 h-3.5" />}
                </button>
              </div>
              <p className="text-2xs text-ink-3">
                Bu komut Vite ile projeyi derler ve derlenmiş dosyaları otomatik olarak GitHub'daki <strong>gh-pages</strong> dalına yükler.
              </p>
            </div>
          </div>

          {/* Optional: Connect to Cloud Run / Backend URL */}
          <div className="bg-accent-soft/70 border border-accent/30 rounded-xl p-4 space-y-2">
            <h4 className="font-bold text-accent flex items-center gap-1.5 text-xs">
              <Server className="w-4 h-4 text-accent" />
              İsteğe Bağlı: Harici Backend / Cloud Run Bağlantısı
            </h4>
            <p className="text-accent text-2xs">
              GitHub Pages statik çalışır. Eğer AI rekonstrüksiyonu için canlı sunucunuzu (Cloud Run veya VPS) bağlamak isterseniz backend URL'nizi buraya girebilirsiniz:
            </p>
            <form onSubmit={handleSaveApiUrl} className="flex items-center gap-2">
              <input
                type="url"
                placeholder="Ör: https://ais-pre-npszzozwuymsemwkvwuime-496312357383.europe-west2.run.app"
                value={customUrl}
                onChange={(e) => setCustomUrl(e.target.value)}
                className="flex-1 bg-white border border-accent/30 rounded px-2.5 py-1 text-xs text-ink"
              />
              <button
                type="submit"
                className="bg-accent hover:bg-accent text-white font-bold px-3 py-1 rounded text-xs cursor-pointer"
              >
                Kaydet
              </button>
            </form>
            {saveSuccess && (
              <span className="text-2xs text-ok font-semibold block">
                ✓ Backend adresi kaydedildi.
              </span>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 bg-field border-t border-line flex items-center justify-end shrink-0">
          <button
            onClick={onClose}
            className="bg-ok hover:bg-ok text-white font-bold px-4 py-1.5 rounded-lg text-xs cursor-pointer"
          >
            Anladım, Kapat
          </button>
        </div>
      </div>
    </div>
  );
};
