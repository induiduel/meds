import React, { useState, useEffect } from 'react';
import {
  Sparkles,
  AlertTriangle,
  Clock,
  Key,
  Zap,
  ExternalLink,
  X,
  RefreshCw,
  Cpu,
} from 'lucide-react';

interface AiQuotaAlertModalProps {
  isOpen: boolean;
  onClose: () => void;
  onRetry?: () => void;
  errorDetails?: string;
  sourceFunction?: string;
}

export const AiQuotaAlertModal: React.FC<AiQuotaAlertModalProps> = ({
  isOpen,
  onClose,
  onRetry,
  errorDetails,
  sourceFunction = 'Yapay Zeka ile Soru Düzenleme',
}) => {
  const [countdown, setCountdown] = useState<number>(40);
  const [canRetryNow, setCanRetryNow] = useState<boolean>(false);
  const [customKey, setCustomKey] = useState<string>('');
  const [customGroqKey, setCustomGroqKey] = useState<string>('');
  const [customMuseSparkKey, setCustomMuseSparkKey] = useState<string>(() => {
    return (typeof localStorage !== 'undefined' ? localStorage.getItem('medsoru_muse_spark_api_key') : '') || '';
  });
  const [activeTab, setActiveTab] = useState<'muse-spark' | 'groq' | 'gemini' | 'wait'>('muse-spark');
  const [savedSuccess, setSavedSuccess] = useState(false);

  useEffect(() => {
    if (!isOpen) return;

    setCountdown(40);
    setCanRetryNow(false);
    setSavedSuccess(false);

    const timer = setInterval(() => {
      setCountdown((prev) => {
        if (prev <= 1) {
          clearInterval(timer);
          setCanRetryNow(true);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [isOpen]);

  if (!isOpen) return null;

  const handleSaveMuseSparkKey = () => {
    if (customMuseSparkKey.trim()) {
      localStorage.setItem('medsoru_muse_spark_api_key', customMuseSparkKey.trim());
    } else {
      localStorage.removeItem('medsoru_muse_spark_api_key');
    }
    setSavedSuccess(true);
    setTimeout(() => {
      if (onRetry) onRetry();
      onClose();
    }, 1000);
  };

  const handleSaveGroqKey = () => {
    if (customGroqKey.trim()) {
      localStorage.setItem('medsoru_groq_api_key', customGroqKey.trim());
      setSavedSuccess(true);
      setTimeout(() => {
        if (onRetry) onRetry();
        onClose();
      }, 1000);
    }
  };

  const handleSaveGeminiKey = () => {
    if (customKey.trim()) {
      localStorage.setItem('medsoru_gemini_api_key', customKey.trim());
      setSavedSuccess(true);
      setTimeout(() => {
        if (onRetry) onRetry();
        onClose();
      }, 1000);
    }
  };

  return (
    <div className="ms-overlay fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-5 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
      <div 
        role="dialog"
        aria-labelledby="ai-quota-title"
        className="ms-modal-panel w-full max-w-xl bg-white rounded-2xl shadow-2xl border border-line flex flex-col overflow-hidden"
      >
        {/* Header */}
        <div className="px-5 sm:px-6 py-4 border-b border-line bg-ai-soft flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="w-10 h-10 rounded-xl bg-ai text-white flex items-center justify-center shrink-0 shadow-sm animate-pulse">
              <Sparkles className="w-5 h-5" />
            </span>
            <div>
              <h3 id="ai-quota-title" className="font-display font-bold text-lg sm:text-lg text-ai m-0">
                Yapay Zeka İstek Limiti Aşıldı (Hata 429)
              </h3>
              <p className="text-sm text-ai m-0">
                {sourceFunction} için ücretsiz API kotası geçici olarak doldu
              </p>
            </div>
          </div>
          <button
            type="button"
            onClick={onClose}
            aria-label="Kapat"
            className="w-8 h-8 rounded-lg hover:bg-ai-soft text-ai flex items-center justify-center transition-colors cursor-pointer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Body */}
        <div className="p-5 sm:p-6 space-y-5 text-ink">
          {/* Explanation Alert */}
          <div className="p-3.5 rounded-xl bg-canvas border border-line text-sm space-y-1">
            <div className="font-semibold text-ink flex items-center gap-1.5">
              <AlertTriangle className="w-4 h-4 text-warn" />
              Neden bu uyarıyı aldınız?
            </div>
            <p className="text-ink-2 m-0 leading-relaxed">
              Google Gemini ücretsiz API havuzu dakikada en fazla 15 istek (RPM) veya günlük 1.500 istek kotasına sahiptir. Aynı anda çok sayıda soru düzenlendiğinde veya genel kota dolduğunda Google sunucuları geçici olarak yanıt vermeyi durdurur.
            </p>
            {errorDetails && (
              <div className="text-2xs font-mono text-bad-text mt-2 p-2 rounded bg-white border border-bad/30">
                {errorDetails}
              </div>
            )}
          </div>

          {/* Solutions Tabs */}
          <div className="space-y-3">
            <div className="flex border-b border-line text-sm font-semibold gap-3 overflow-x-auto">
              <button
                type="button"
                onClick={() => setActiveTab('muse-spark')}
                className={`pb-2 border-b-2 transition-colors cursor-pointer flex items-center gap-1.5 whitespace-nowrap ${
                  activeTab === 'muse-spark' ? 'border-accent text-accent font-bold' : 'border-transparent text-ink-3 hover:text-ink'
                }`}
              >
                <Cpu className="w-3.5 h-3.5 text-accent" />
                Muse Spark 1.3 Free (Kurtarıcı)
              </button>
              <button
                type="button"
                onClick={() => setActiveTab('groq')}
                className={`pb-2 border-b-2 transition-colors cursor-pointer flex items-center gap-1.5 whitespace-nowrap ${
                  activeTab === 'groq' ? 'border-ai text-ai' : 'border-transparent text-ink-3 hover:text-ink'
                }`}
              >
                <Zap className="w-3.5 h-3.5 text-ai" />
                Ücretsiz Groq
              </button>
              <button
                type="button"
                onClick={() => setActiveTab('gemini')}
                className={`pb-2 border-b-2 transition-colors cursor-pointer flex items-center gap-1.5 whitespace-nowrap ${
                  activeTab === 'gemini' ? 'border-ai text-ai' : 'border-transparent text-ink-3 hover:text-ink'
                }`}
              >
                <Key className="w-3.5 h-3.5 text-ai" />
                Kendi Gemini Anahtarın
              </button>
              <button
                type="button"
                onClick={() => setActiveTab('wait')}
                className={`pb-2 border-b-2 transition-colors cursor-pointer flex items-center gap-1.5 whitespace-nowrap ${
                  activeTab === 'wait' ? 'border-ai text-ai' : 'border-transparent text-ink-3 hover:text-ink'
                }`}
              >
                <Clock className="w-3.5 h-3.5 text-ai" />
                Bekle & Yeniden Dene
              </button>
            </div>

            {/* TAB: MUSE SPARK 1.3 FREE */}
            {activeTab === 'muse-spark' && (
              <div className="p-4 rounded-xl border border-accent/30 bg-accent-soft/50 space-y-3 text-sm">
                <div className="flex items-center gap-2 text-accent font-bold">
                  <span className="w-2.5 h-2.5 rounded-full bg-accent animate-pulse" />
                  <span>Otomatik Kota Kurtarıcı Aktif</span>
                </div>
                <p className="text-accent m-0 leading-relaxed">
                  <strong>Muse Spark 1.3 Free</strong>, sitede Google Gemini ve Groq Cloud kotalarının tamamı tükendiğinde soru sorma işlemlerinde otomatik devreye giren yüksek performanslı akıl yürütme modelidir.
                </p>
                <div className="p-2.5 rounded-lg bg-white border border-accent/30 text-xs text-accent space-y-1">
                  <div>✓ <strong>Model:</strong> Muse Spark 1.3 Free (Contributor Tier)</div>
                  <div>✓ <strong>Çalışma Prensibi:</strong> Tüm AI limitleri dolduğunda sorularınız kesintisiz olarak Muse Spark üzerinden yanıtlanır.</div>
                </div>
                <div className="space-y-2 pt-1">
                  <label className="block text-xs font-semibold text-accent">
                    Özel Muse Spark / OpenCode / OpenRouter Anahtarı (İsteğe Bağlı):
                  </label>
                  <div className="flex items-center gap-2">
                    <input
                      type="password"
                      value={customMuseSparkKey}
                      onChange={(e) => setCustomMuseSparkKey(e.target.value)}
                      placeholder="OpenCode / Muse Spark API Anahtarı..."
                      className="flex-1 h-9 px-3 rounded-lg border border-accent/30 bg-white font-mono text-xs text-ink outline-0 focus:border-accent"
                    />
                    <button
                      type="button"
                      onClick={handleSaveMuseSparkKey}
                      className="h-9 px-4 rounded-lg bg-accent hover:bg-accent text-white font-semibold text-sm cursor-pointer transition-colors"
                    >
                      {savedSuccess ? 'Kaydedildi ✓' : 'Kaydet'}
                    </button>
                  </div>
                  <p className="text-2xs text-accent m-0">
                    Anahtar girmeseniz dahi yerleşik Muse Spark 1.3 havuzu arka planda otomatik devreye girer.
                  </p>
                </div>
              </div>
            )}

            {/* TAB: GROQ */}
            {activeTab === 'groq' && (
              <div className="p-4 rounded-xl border border-ai/30 bg-ai-soft/50 space-y-3 text-sm">
                <p className="text-ai m-0">
                  <strong>Groq Cloud</strong>, Gemini'den bağımsız olarak Llama 3.3 70B modelini saniyede 300+ token hızında tamamen ücretsiz ve sınırsız çalıştırır.
                </p>
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <input
                      type="password"
                      value={customGroqKey}
                      onChange={(e) => setCustomGroqKey(e.target.value)}
                      placeholder="gsk_..."
                      className="flex-1 h-9 px-3 rounded-lg border border-ai/30 bg-white font-mono text-xs text-ink outline-0 focus:border-ai"
                    />
                    <button
                      type="button"
                      onClick={handleSaveGroqKey}
                      disabled={!customGroqKey.trim()}
                      className="h-9 px-4 rounded-lg bg-ai hover:bg-ai text-white font-semibold text-sm disabled:opacity-50 cursor-pointer transition-colors"
                    >
                      {savedSuccess ? 'Kaydedildi ✓' : 'Kaydet ve Devam Et'}
                    </button>
                  </div>
                  <a
                    href="https://console.groq.com/keys"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1 text-xs text-ai font-semibold hover:underline"
                  >
                    10 saniyede ücretsiz Groq anahtarı al →
                    <ExternalLink className="w-3 h-3" />
                  </a>
                </div>
              </div>
            )}

            {/* TAB: GEMINI KEY */}
            {activeTab === 'gemini' && (
              <div className="p-4 rounded-xl border border-line bg-canvas/40 space-y-3 text-sm">
                <p className="text-ink-2 m-0">
                  Google AI Studio'dan kendi adınıza açacağınız ücretsiz API anahtarını tanımlayarak genel kullanıcıların harcadığı kotadan bağımsız olabilirsiniz.
                </p>
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <input
                      type="password"
                      value={customKey}
                      onChange={(e) => setCustomKey(e.target.value)}
                      placeholder="AIzaSy..."
                      className="flex-1 h-9 px-3 rounded-lg border border-line bg-white font-mono text-xs text-ink outline-0 focus:border-accent"
                    />
                    <button
                      type="button"
                      onClick={handleSaveGeminiKey}
                      disabled={!customKey.trim()}
                      className="h-9 px-4 rounded-lg bg-accent text-white font-semibold text-sm disabled:opacity-50 cursor-pointer"
                    >
                      {savedSuccess ? 'Kaydedildi ✓' : 'Uygula'}
                    </button>
                  </div>
                  <a
                    href="https://aistudio.google.com/apikey"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1 text-xs text-accent font-semibold hover:underline"
                  >
                    Google AI Studio'dan Ücretsiz Anahtar Al →
                    <ExternalLink className="w-3 h-3" />
                  </a>
                </div>
              </div>
            )}

            {/* TAB: WAIT & RETRY */}
            {activeTab === 'wait' && (
              <div className="p-4 rounded-xl border border-line bg-canvas/40 text-center space-y-3">
                <div className="w-12 h-12 rounded-full bg-ai-soft text-ai mx-auto flex items-center justify-center">
                  <Clock className="w-6 h-6 animate-pulse" />
                </div>
                <div>
                  <div className="font-bold text-lg text-ink font-mono">
                    {countdown > 0 ? `${countdown} saniye` : 'Kota Sıfırlandı!'}
                  </div>
                  <p className="text-xs text-ink-3 mt-1 m-0">
                    {countdown > 0 
                      ? 'Dakikalık istek limitinin sıfırlanması bekleniyor...'
                      : 'Dakikalık kota yenilendi, şimdi tekrar deneyebilirsiniz!'}
                  </p>
                </div>
                <button
                  type="button"
                  onClick={() => {
                    if (onRetry) onRetry();
                    onClose();
                  }}
                  disabled={!canRetryNow}
                  className="h-9 px-5 rounded-lg bg-ai hover:bg-ai text-white font-semibold text-sm inline-flex items-center gap-2 cursor-pointer disabled:opacity-50"
                >
                  <RefreshCw className="w-3.5 h-3.5" />
                  Şimdi Tekrar Dene
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="px-6 py-3 border-t border-line bg-canvas flex items-center justify-between text-xs text-ink-3">
          <span>MeDSor Yapay Zeka Hata Kalkanı</span>
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={onClose}
              className="h-8 px-4 rounded-lg bg-white border border-line hover:bg-canvas text-ink font-semibold text-sm cursor-pointer"
            >
              Manuel Düzenlemeye Dön
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
