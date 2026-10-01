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
        className="w-full bg-[#FEF2F2] border-b border-[#FCA5A5] text-[#991B1B] px-4 py-2.5 sm:px-6 sm:py-3 transition-all animate-in fade-in duration-300"
      >
        <div className="max-w-[1280px] mx-auto flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-[13px] sm:text-[14px]">
          <div className="flex items-start sm:items-center gap-2.5">
            <span className="p-1 rounded-md bg-[#EF4444] text-white shrink-0 mt-0.5 sm:mt-0 animate-pulse">
              <AlertOctagon className="w-4 h-4" />
            </span>
            <div>
              <span className="font-bold text-[#7F1D1D] mr-1.5">🚨 Kritik Veritabanı Hatası:</span>
              <span>Online sitede Firebase ve Supabase bulut veritabanlarına ulaşılamıyor. Soru havuzu ve senkronizasyon çalışmayabilir!</span>
            </div>
          </div>
          <div className="flex items-center gap-2 shrink-0 self-end sm:self-auto">
            <button
              type="button"
              onClick={onOpenDiagnostics}
              className="h-8 px-3 rounded-lg bg-[#DC2626] hover:bg-[#B91C1C] text-white font-semibold text-[13px] inline-flex items-center gap-1.5 shadow-sm transition-colors cursor-pointer"
            >
              <Database className="w-3.5 h-3.5" />
              Tanı & Çözüm Ekranı
              <ChevronRight className="w-3.5 h-3.5" />
            </button>
            <button
              type="button"
              onClick={() => setDismissed(true)}
              aria-label="Kapat"
              className="p-1.5 rounded-lg text-[#991B1B] hover:bg-[#FEE2E2] transition-colors cursor-pointer"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    );
  }

  // 2. FİREBASE KOTA BİLDİRİMİ (Supabase yedek olarak devraldı)
  if (health.firebase.status === 'quota_exceeded' && health.supabase.status === 'online') {
    return (
      <div 
        role="status" 
        className="w-full bg-[#FFFBEB] border-b border-[#FCD34D] text-[#92400E] px-4 py-2 sm:px-6 sm:py-2.5 transition-all"
      >
        <div className="max-w-[1280px] mx-auto flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 text-[12px] sm:text-[13px]">
          <div className="flex items-center gap-2">
            <span className="p-1 rounded-md bg-[#F59E0B] text-white shrink-0">
              <AlertTriangle className="w-3.5 h-3.5" />
            </span>
            <div>
              <span className="font-bold mr-1">Firebase Spark Kotası Doldu:</span>
              <span>Günlük 50.000 okuma limiti aşıldı. Supabase PostgreSQL bulut veritabanı kesintisiz olarak aktif devraldı.</span>
            </div>
          </div>
          <div className="flex items-center gap-2 shrink-0 self-end sm:self-auto">
            <button
              type="button"
              onClick={onOpenDiagnostics}
              className="h-7 px-2.5 rounded-md bg-white border border-[#FCD34D] hover:bg-[#FEF3C7] text-[#92400E] font-medium text-[12px] inline-flex items-center gap-1 transition-colors cursor-pointer"
            >
              <Database className="w-3 h-3 text-[#D97706]" />
              Veritabanı Durumu
            </button>
            <button
              type="button"
              onClick={() => setDismissed(true)}
              aria-label="Kapat"
              className="p-1 rounded text-[#92400E] hover:bg-[#FEF3C7] transition-colors cursor-pointer"
            >
              <X className="w-3.5 h-3.5" />
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
        className="w-full bg-[#F5F3FF] border-b border-[#DDD6FE] text-[#5B21B6] px-4 py-2 sm:px-6 sm:py-2.5 transition-all"
      >
        <div className="max-w-[1280px] mx-auto flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 text-[12px] sm:text-[13px]">
          <div className="flex items-center gap-2">
            <span className="p-1 rounded-md bg-[#8B5CF6] text-white shrink-0 animate-pulse">
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
              className="h-7 px-2.5 rounded-md bg-[#7C3AED] hover:bg-[#6D28D9] text-white font-semibold text-[12px] inline-flex items-center gap-1 shadow-sm transition-colors cursor-pointer"
            >
              <Cpu className="w-3 h-3" />
              Limiti Çöz & Anahtar Gir
              <ChevronRight className="w-3 h-3" />
            </button>
            <button
              type="button"
              onClick={() => setDismissed(true)}
              aria-label="Kapat"
              className="p-1 rounded text-[#5B21B6] hover:bg-[#EDE9FE] transition-colors cursor-pointer"
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
