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
    <div className="ms-overlay fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 overflow-y-auto">
      <div className="ms-modal-panel bg-white rounded-2xl max-w-2xl w-full shadow-2xl border border-slate-200 overflow-hidden my-6 flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="bg-slate-900 text-white p-5 flex items-center justify-between shrink-0">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-white/10 text-white border border-white/20 flex items-center justify-center">
              <Github className="w-6 h-6" />
            </div>
            <div>
              <h3 className="font-bold text-base">GitHub Pages Kurulum & Çözüm Rehberi</h3>
              <p className="text-xs text-slate-300">
                "GitHub Pages yaptığımda sayfa açılmıyor / beyaz ekran çıkıyor" Çözümü
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-5 overflow-y-auto text-xs text-slate-700 leading-relaxed">
          {/* Why it was blank explanation */}
          <div className="bg-rose-50 border border-rose-200 rounded-xl p-4 space-y-2">
            <h4 className="font-bold text-rose-900 flex items-center gap-1.5 text-xs">
              <AlertCircle className="w-4 h-4 text-rose-600" />
              Sayfanın Beyaz Kalmasının Kesin Nedeni:
            </h4>
            <p className="text-rose-950 text-[11px] leading-relaxed">
              GitHub Pages şu anda derlenmiş <code className="bg-rose-100 px-1 py-0.5 rounded font-mono font-bold">dist/</code> klasörü yerine, reponun ana dizinindeki ham kaynak dosyayı (<code className="bg-rose-100 px-1 py-0.5 rounded font-mono">&lt;script src="/src/main.tsx"&gt;</code>) sunuyor.
              Tarayıcılar derlenmemiş ham TypeScript (.tsx) dosyalarını doğrudan çalıştıramadığı için sayfa boş kalmaktadır.
            </p>
          </div>

          {/* Step by step deployment */}
          <div className="space-y-3 pt-1">
            <h4 className="font-bold text-slate-900 text-sm border-b pb-1">
              Bunu Düzeltmenin 2 Yolu (Hangisini İsterseniz):
            </h4>

            {/* Method 1: Change Source to GitHub Actions */}
            <div className="bg-teal-50/60 border border-teal-200 rounded-xl p-4 space-y-2">
              <span className="bg-teal-700 text-white text-[10px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider">
                Yöntem 1 (Önerilen) • GitHub Ayarından "GitHub Actions"ı Seçmek
              </span>
              <ol className="space-y-1.5 text-[11px] text-teal-950 list-decimal list-inside">
                <li>
                  GitHub'da <strong>https://github.com/induiduel/meds</strong> sayfanıza gidin.
                </li>
                <li>
                  Üst sekmelerden <strong>Settings</strong> (Ayarlar) ➔ Sol menüden <strong>Pages</strong> seçeneğine tıklayın.
                </li>
                <li>
                  <strong>Build and deployment</strong> bölümündeki <strong>Source</strong> açılır kutusunu bulun:
                  <div className="mt-1 p-2 bg-white rounded border border-teal-200 font-semibold text-slate-800">
                    ❌ Şu anki: "Deploy from a branch"<br />
                    👉 <strong>Bunu Seçin: "GitHub Actions"</strong>
                  </div>
                </li>
                <li>
                  Bunu seçtiğiniz anda GitHub otomatik olarak projeyi derleyip <strong>https://induiduel.github.io/meds/</strong> adresinde sitenizi açacaktır!
                </li>
              </ol>
            </div>

            {/* Method 2: One command npm run deploy */}
            <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 space-y-2">
              <span className="bg-slate-800 text-white text-[10px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider">
                Yöntem 2 (Terminalden Tek Komutla Canlıya Alma)
              </span>
              <p className="text-[11px] text-slate-600">
                Eğer "Deploy from a branch" kullanmaya devam etmek isterseniz, terminalinizde şu komutu çalıştırmanız yeterlidir:
              </p>
              <div className="bg-slate-900 text-slate-100 p-2.5 rounded font-mono text-[11px] flex items-center justify-between">
                <span>npm run deploy</span>
                <button
                  onClick={() => copyToClipboard('npm run deploy', 1)}
                  className="text-slate-400 hover:text-white"
                >
                  {copiedIndex === 1 ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                </button>
              </div>
              <p className="text-[10px] text-slate-500">
                Bu komut Vite ile projeyi derler ve derlenmiş dosyaları otomatik olarak GitHub'daki <strong>gh-pages</strong> dalına yükler.
              </p>
            </div>
          </div>

          {/* Optional: Connect to Cloud Run / Backend URL */}
          <div className="bg-sky-50/70 border border-sky-200 rounded-xl p-4 space-y-2">
            <h4 className="font-bold text-sky-900 flex items-center gap-1.5 text-xs">
              <Server className="w-4 h-4 text-sky-700" />
              İsteğe Bağlı: Harici Backend / Cloud Run Bağlantısı
            </h4>
            <p className="text-sky-950 text-[11px]">
              GitHub Pages statik çalışır. Eğer AI rekonstrüksiyonu için canlı sunucunuzu (Cloud Run veya VPS) bağlamak isterseniz backend URL'nizi buraya girebilirsiniz:
            </p>
            <form onSubmit={handleSaveApiUrl} className="flex items-center gap-2">
              <input
                type="url"
                placeholder="Ör: https://ais-pre-npszzozwuymsemwkvwuime-496312357383.europe-west2.run.app"
                value={customUrl}
                onChange={(e) => setCustomUrl(e.target.value)}
                className="flex-1 bg-white border border-sky-300 rounded px-2.5 py-1 text-xs text-slate-800"
              />
              <button
                type="submit"
                className="bg-sky-700 hover:bg-sky-800 text-white font-bold px-3 py-1 rounded text-xs cursor-pointer"
              >
                Kaydet
              </button>
            </form>
            {saveSuccess && (
              <span className="text-[11px] text-emerald-700 font-semibold block">
                ✓ Backend adresi kaydedildi.
              </span>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 bg-slate-50 border-t border-slate-200 flex items-center justify-end shrink-0">
          <button
            onClick={onClose}
            className="bg-teal-700 hover:bg-teal-800 text-white font-bold px-4 py-1.5 rounded-lg text-xs cursor-pointer"
          >
            Anladım, Kapat
          </button>
        </div>
      </div>
    </div>
  );
};
