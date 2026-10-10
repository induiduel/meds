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
        className="w-full bg-bad-soft border-b border-bad/30 text-bad-text px-4 py-2.5 sm:px-6 sm:py-3 transition-all animate-in fade-in duration-300"
      >
        <div className="max-w-[1280px] mx-auto flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-sm sm:text-base">
          <div className="flex items-start sm:items-center gap-2.5">
            <span className="p-1 rounded-md bg-bad text-white shrink-0 mt-0.5 sm:mt-0 animate-pulse">
              <AlertOctagon className="w-4 h-4" />
            </span>
            <div>
              <span className="font-bold text-bad-text mr-1.5">Kritik Veritabanı Hatası:</span>
              <span>Online sitede Firebase ve Supabase bulut veritabanlarına ulaşılamıyor. Soru havuzu ve senkronizasyon çalışmayabilir!</span>
            </div>
          </div>
          <div className="flex items-center gap-2 shrink-0 self-end sm:self-auto">
            <button
              type="button"
              onClick={onOpenDiagnostics}
              className="h-8 px-3 rounded-lg bg-bad hover:bg-bad text-white font-semibold text-sm inline-flex items-center gap-1.5 shadow-sm transition-colors cursor-pointer"
            >
              <Database className="w-3.5 h-3.5" />
              Tanı & Çözüm Ekranı
              <ChevronRight className="w-3.5 h-3.5" />
            </button>
            <button
              type="button"
              onClick={() => setDismissed(true)}
              aria-label="Kapat"
              className="p-1.5 rounded-lg text-bad-text hover:bg-bad-soft transition-colors cursor-pointer"
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
        className="w-full bg-ai-soft border-b border-ai/30 text-ai px-4 py-2 sm:px-6 sm:py-2.5 transition-all"
      >
        <div className="max-w-[1280px] mx-auto flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 text-xs sm:text-sm">
          <div className="flex items-center gap-2">
            <span className="p-1 rounded-md bg-ai text-white shrink-0 animate-pulse">
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
              className="h-7 px-2.5 rounded-md bg-ai hover:bg-ai text-white font-semibold text-xs inline-flex items-center gap-1 shadow-sm transition-colors cursor-pointer"
            >
              <Cpu className="w-3 h-3" />
              Limiti Çöz & Anahtar Gir
              <ChevronRight className="w-3 h-3" />
            </button>
            <button
              type="button"
              onClick={() => setDismissed(true)}
              aria-label="Kapat"
              className="p-1 rounded text-ai hover:bg-ai-soft transition-colors cursor-pointer"
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
