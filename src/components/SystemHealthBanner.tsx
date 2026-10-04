import React, { useState, useEffect } from 'react';
import { 
  AlertTriangle, 
  AlertOctagon, 
  Sparkles, 
  RefreshCw, 
  ExternalLink, 
  ChevronRight, 
  X, 
  Database,
  Cpu,
  CheckCircle2
} from 'lucide-react';
import { systemHealthMonitor, SystemOverallHealth } from '../services/systemHealthMonitor';

interface SystemHealthBannerProps {
  onOpenDiagnostics: () => void;
  onOpenAiQuotaModal?: () => void;
}

export const SystemHealthBanner: React.FC<SystemHealthBannerProps> = ({
  onOpenDiagnostics,
  onOpenAiQuotaModal,
}) => {
  const [health, setHealth] = useState<SystemOverallHealth>(systemHealthMonitor.getHealth());
  const [dismissed, setDismissed] = useState(false);
  const [lastAlertKey, setLastAlertKey] = useState<string>('');

  useEffect(() => {
    // Abone ol
    const unsubscribe = systemHealthMonitor.subscribe((newHealth) => {
      setHealth(newHealth);

      // Yeni bir kritik hata oluştuğunda bildirimi yeniden aç
      const currentKey = `${newHealth.databaseFailureLevel}-${newHealth.hasAiQuotaAlert}-${newHealth.firebase.status}`;
      if (currentKey !== lastAlertKey) {
        setLastAlertKey(currentKey);
        setDismissed(false);
      }
    });

    // İlk açılışta sağlık kontrolü yap
    systemHealthMonitor.runFullDiagnostic(false);

    return () => unsubscribe();
  }, [lastAlertKey]);

  if (dismissed) return null;

  // 1. KRİTİK VERİTABANI HATASI: Hem Firebase hem Supabase çalışmıyorsa
  if (health.hasCriticalDatabaseError) {
    return (
      <div 
        role="alert" 
        className="w-full bg-rose-50 border-b border-rose-300 text-rose-800 px-4 py-2.5 sm:px-6 sm:py-3 transition-all animate-in fade-in duration-300"
      >
        <div className="max-w-[1280px] mx-auto flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-[13px] sm:text-[14px]">
          <div className="flex items-start sm:items-center gap-2.5">
            <span className="p-1 rounded-md bg-rose-500 text-white shrink-0 mt-0.5 sm:mt-0 animate-pulse">
              <AlertOctagon className="w-4 h-4" />
            </span>
            <div>
              <span className="font-bold text-rose-800 mr-1.5">🚨 Kritik Veritabanı Hatası:</span>
              <span>Online sitede Firebase ve Supabase bulut veritabanlarına ulaşılamıyor. Soru havuzu ve senkronizasyon çalışmayabilir!</span>
            </div>
          </div>
          <div className="flex items-center gap-2 shrink-0 self-end sm:self-auto">
            <button
              type="button"
              onClick={onOpenDiagnostics}
              className="h-8 px-3 rounded-lg bg-rose-600 hover:bg-rose-700 text-white font-semibold text-[13px] inline-flex items-center gap-1.5 shadow-sm transition-colors cursor-pointer"
            >
              <Database className="w-3.5 h-3.5" />
              Tanı & Çözüm Ekranı
              <ChevronRight className="w-3.5 h-3.5" />
            </button>
            <button
              type="button"
              onClick={() => setDismissed(true)}
              aria-label="Kapat"
              className="p-1.5 rounded-lg text-rose-800 hover:bg-rose-100 transition-colors cursor-pointer"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    );
  }


  // 3. YAPAY ZEKA LİMİT UYARISI: AI kotaları dolduysa
  if (health.hasAiQuotaAlert || health.ai.status === 'all_exhausted') {
    return (
      <div 
        role="alert" 
        className="w-full bg-violet-50 border-b border-violet-200 text-violet-700 px-4 py-2 sm:px-6 sm:py-2.5 transition-all"
      >
        <div className="max-w-[1280px] mx-auto flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 text-[12px] sm:text-[13px]">
          <div className="flex items-center gap-2">
            <span className="p-1 rounded-md bg-violet-400 text-white shrink-0 animate-pulse">
              <Sparkles className="w-3.5 h-3.5" />
            </span>
            <div>
              <span className="font-bold mr-1">Yapay Zeka Limit Uyarısı:</span>
              <span>Gemini ücretsiz istek kotaları aşıldı (HTTP 429). Soru düzenleme için kendi anahtarınızı tanımlayın veya Groq'a geçin.</span>
            </div>
          </div>
          <div className="flex items-center gap-2 shrink-0 self-end sm:self-auto">
            <button
              type="button"
              onClick={onOpenAiQuotaModal || onOpenDiagnostics}
              className="h-7 px-2.5 rounded-md bg-violet-500 hover:bg-violet-600 text-white font-semibold text-[12px] inline-flex items-center gap-1 shadow-sm transition-colors cursor-pointer"
            >
              <Cpu className="w-3 h-3" />
              Limiti Çöz & Anahtar Gir
              <ChevronRight className="w-3 h-3" />
            </button>
            <button
              type="button"
              onClick={() => setDismissed(true)}
              aria-label="Kapat"
              className="p-1 rounded text-violet-700 hover:bg-violet-100 transition-colors cursor-pointer"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>
    );
  }

  return null;
};
