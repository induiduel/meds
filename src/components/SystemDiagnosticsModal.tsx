import React, { useState, useEffect } from 'react';
import {
  Activity,
  AlertTriangle,
  AlertOctagon,
  CheckCircle2,
  RefreshCw,
  X,
  Database,
  Cpu,
  Key,
  Check,
  ExternalLink,
  Zap,
  Sparkles,
} from 'lucide-react';
import { systemHealthMonitor, SystemOverallHealth } from '../services/systemHealthMonitor';
import { multiDbManager, DatabaseMode } from '../services/multiDbManager';

interface SystemDiagnosticsModalProps {
  isOpen: boolean;
  onClose: () => void;
  onRefreshParentData?: () => void;
}

export const SystemDiagnosticsModal: React.FC<SystemDiagnosticsModalProps> = ({
  isOpen,
  onClose,
  onRefreshParentData,
}) => {
  const [health, setHealth] = useState<SystemOverallHealth>(systemHealthMonitor.getHealth());
  const [isRunningTest, setIsRunningTest] = useState(false);
  const [activeTab, setActiveTab] = useState<'overview' | 'ai' | 'database' | 'settings'>('overview');
  
  // Custom API Keys State
  const [customGeminiKey, setCustomGeminiKey] = useState<string>(() => {
    return (typeof localStorage !== 'undefined' ? localStorage.getItem('medsoru_gemini_api_key') : '') || '';
  });
  const [customGroqKey, setCustomGroqKey] = useState<string>(() => {
    return (typeof localStorage !== 'undefined' ? localStorage.getItem('medsoru_groq_api_key') : '') || '';
  });
  const [customGroqKey2, setCustomGroqKey2] = useState<string>(() => {
    return (typeof localStorage !== 'undefined' ? localStorage.getItem('medsoru_groq_api_key_2') : '') || '';
  });
  const [customMuseSparkKey, setCustomMuseSparkKey] = useState<string>(() => {
    return (typeof localStorage !== 'undefined' ? localStorage.getItem('medsoru_muse_spark_api_key') : '') || '';
  });
  const [dbMode, setDbMode] = useState<DatabaseMode>(() => multiDbManager.getActiveMode());
  
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [realtimeTest, setRealtimeTest] = useState<{
    running: boolean;
    result?: {
      success: boolean;
      latencyMs: number;
      message: string;
      broadcastActive?: boolean;
      postgresActive?: boolean;
      broadcastLatencyMs?: number;
      postgresLatencyMs?: number;
    };
  }>({ running: false });

  const handleTestRealtime = async () => {
    setRealtimeTest({ running: true });
    try {
      const res = await multiDbManager.testRealtimeRoundtrip(4500);
      setRealtimeTest({ running: false, result: res });
    } catch (e: any) {
      setRealtimeTest({
        running: false,
        result: {
          success: false,
          latencyMs: 0,
          broadcastActive: false,
          postgresActive: false,
          message: e.message || 'Bilinmeyen test hatası.',
        },
      });
    }
  };

  useEffect(() => {
    const unsubscribe = systemHealthMonitor.subscribe((newHealth) => {
      setHealth(newHealth);
    });
    return () => unsubscribe();
  }, []);

  if (!isOpen) return null;

  const handleRunTest = async () => {
    setIsRunningTest(true);
    try {
      await systemHealthMonitor.runFullDiagnostic(true);
      if (onRefreshParentData) onRefreshParentData();
    } finally {
      setIsRunningTest(false);
    }
  };

  const handleSaveSettings = () => {
    if (typeof localStorage !== 'undefined') {
      if (customGeminiKey.trim()) {
        localStorage.setItem('medsoru_gemini_api_key', customGeminiKey.trim());
      } else {
        localStorage.removeItem('medsoru_gemini_api_key');
      }

      if (customGroqKey.trim()) {
        localStorage.setItem('medsoru_groq_api_key', customGroqKey.trim());
      } else {
        localStorage.removeItem('medsoru_groq_api_key');
      }

      if (customGroqKey2.trim()) {
        localStorage.setItem('medsoru_groq_api_key_2', customGroqKey2.trim());
      } else {
        localStorage.removeItem('medsoru_groq_api_key_2');
      }

      if (customMuseSparkKey.trim()) {
        localStorage.setItem('medsoru_muse_spark_api_key', customMuseSparkKey.trim());
      } else {
        localStorage.removeItem('medsoru_muse_spark_api_key');
      }
    }

    multiDbManager.setActiveMode(dbMode);

    setSaveSuccess(true);
    setTimeout(() => setSaveSuccess(false), 2500);

    // Ayarlar değiştiğinde tekrar test yap
    handleRunTest();
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'online':
      case 'ok':
      case 'ready':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-ok-soft text-ok border border-ok/30">
            <CheckCircle2 className="w-3.5 h-3.5 text-ok" />
            Çevrimiçi / Hazır
          </span>
        );
      case 'quota_exceeded':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-warn-soft text-warn border border-warn">
            <AlertTriangle className="w-3.5 h-3.5 text-warn" />
            Kota Aşıldı (429)
          </span>
        );
      case 'high_demand':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-warn-soft text-warn border border-warn">
            <AlertTriangle className="w-3.5 h-3.5 text-warn" />
            Aşırı Yoğun (503)
          </span>
        );
      case 'spending_cap_exceeded':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-bad-soft text-bad-text border border-bad/30">
            <AlertOctagon className="w-3.5 h-3.5 text-bad-text" />
            Harcama Limiti Aşıldı
          </span>
        );
      case 'missing_tables':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-warn/20 text-warn border border-warn">
            <AlertTriangle className="w-3.5 h-3.5 text-warn" />
            Tablolar Eksik
          </span>
        );
      case 'offline':
      case 'error':
      case 'auth_error':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-bad-soft text-bad-text border border-bad/30">
            <AlertOctagon className="w-3.5 h-3.5 text-bad-text" />
            Hata / Çevrimdışı
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-field text-ink-2">
            {status}
          </span>
        );
    }
  };

  return (
    <div className="ms-overlay fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-5 bg-[var(--color-scrim)] animate-in fade-in duration-200">
      <div 
        role="dialog"
        aria-labelledby="diagnostics-modal-title"
        className="ms-modal-panel w-full max-w-4xl bg-white rounded-2xl shadow-2xl border border-line flex flex-col max-h-[92dvh] overflow-hidden"
      >
        {/* Header */}
        <div className="px-5 sm:px-6 py-4 border-b border-line bg-canvas flex items-center justify-between shrink-0">
          <div className="flex items-center gap-3">
            <span className="w-10 h-10 rounded-xl bg-accent text-white flex items-center justify-center shrink-0 shadow-sm">
              <Activity className="w-5 h-5" />
            </span>
            <div>
              <h2 id="diagnostics-modal-title" className="font-display font-bold text-lg sm:text-xl text-ink m-0 flex items-center gap-2">
                Veritabanı & Limit Takip Paneli
                {health.hasCriticalDatabaseError && (
                  <span className="px-2 py-0.5 rounded-md text-2xs bg-bad text-white font-bold">
                    KRİTİK HATA
                  </span>
                )}
                {health.hasAiQuotaAlert && (
                  <span className="px-2 py-0.5 rounded-md text-2xs bg-ai text-white font-bold">
                    AI KOTA LİMİTİ
                  </span>
                )}
              </h2>
              <p className="text-sm text-ink-3 m-0">
                Online Firebase, sunucu veritabanı (meds-pg) ve Yapay Zeka servislerinin canlı durum ve limit takibi
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={handleRunTest}
              disabled={isRunningTest}
              className="h-9 px-3 rounded-lg border border-line bg-white hover:bg-canvas text-ink font-semibold text-sm inline-flex items-center gap-2 transition-colors cursor-pointer disabled:opacity-50"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isRunningTest ? 'animate-spin' : ''}`} />
              {isRunningTest ? 'Test Ediliyor…' : 'Yeniden Test Et'}
            </button>
            <button
              type="button"
              onClick={onClose}
              aria-label="Kapat"
              className="w-9 h-9 rounded-lg hover:bg-canvas text-ink-2 flex items-center justify-center transition-colors cursor-pointer"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="px-6 border-b border-line flex items-center gap-4 bg-white shrink-0 overflow-x-auto">
          <button
            type="button"
            onClick={() => setActiveTab('overview')}
            className={`py-3 text-base font-semibold border-b-2 transition-colors cursor-pointer whitespace-nowrap ${
              activeTab === 'overview'
                ? 'border-accent text-accent'
                : 'border-transparent text-ink-2 hover:text-ink'
            }`}
          >
            Genel Bakış
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('database')}
            className={`py-3 text-base font-semibold border-b-2 transition-colors cursor-pointer whitespace-nowrap flex items-center gap-1.5 ${
              activeTab === 'database'
                ? 'border-accent text-accent'
                : 'border-transparent text-ink-2 hover:text-ink'
            }`}
          >
            <Database className="w-4 h-4" />
            Veritabanları (Firebase & meds-pg)
            {health.firebase.status === 'quota_exceeded' && (
              <span className="w-2 h-2 rounded-full bg-warn" />
            )}
            {health.hasCriticalDatabaseError && (
              <span className="w-2 h-2 rounded-full bg-bad" />
            )}
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('ai')}
            className={`py-3 text-base font-semibold border-b-2 transition-colors cursor-pointer whitespace-nowrap flex items-center gap-1.5 ${
              activeTab === 'ai'
                ? 'border-accent text-accent'
                : 'border-transparent text-ink-2 hover:text-ink'
            }`}
          >
            <Cpu className="w-4 h-4" />
            Yapay Zeka Limitleri (Gemini & Groq)
            {health.hasAiQuotaAlert && (
              <span className="w-2 h-2 rounded-full bg-ai" />
            )}
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('settings')}
            className={`py-3 text-base font-semibold border-b-2 transition-colors cursor-pointer whitespace-nowrap flex items-center gap-1.5 ${
              activeTab === 'settings'
                ? 'border-accent text-accent'
                : 'border-transparent text-ink-2 hover:text-ink'
            }`}
          >
            <Key className="w-4 h-4" />
            API & Veritabanı Ayarları
          </button>
        </div>

        {/* Content Body */}
        <div className="flex-1 overflow-y-auto p-5 sm:p-6 space-y-6">

          {/* TAB 1: OVERVIEW */}
          {activeTab === 'overview' && (
            <div className="space-y-6">
              {/* Alert Callouts */}
              {health.hasCriticalDatabaseError && (
                <div className="p-4 rounded-xl bg-bad-soft border border-bad/30 text-bad-text">
                  <div className="flex items-start gap-3">
                    <AlertOctagon className="w-5 h-5 text-bad-text shrink-0 mt-0.5" />
                    <div>
                      <h4 className="font-bold text-md m-0">Online Veritabanı Kesintisi Tespit Edildi!</h4>
                      <p className="text-sm mt-1 m-0 text-bad-text">
                        Online sitede hem Firebase Spark kotası dolmuş hem de sunucu veritabanına (meds-pg) ulaşılamıyor.
                        Öğrenciler soru ekleyemez veya soruları yükleyemez. Lütfen sunucunun ve meds-pg konteynerinin çalıştığını, sunucu loglarını kontrol edin.
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {health.firebase.status === 'quota_exceeded' && health.supabase.status === 'online' && (
                <div className="p-4 rounded-xl bg-warn-soft border border-warn text-warn">
                  <div className="flex items-start gap-3">
                    <CheckCircle2 className="w-5 h-5 text-ok shrink-0 mt-0.5" />
                    <div>
                      <h4 className="font-bold text-md m-0">✓ Otomatik Veritabanı Devri Başarılı</h4>
                      <p className="text-sm mt-1 m-0 text-warn">
                        Firebase Spark günlük ücretsiz 50.000 okuma kotası doldu. MeDSor otomatik failover sistemi sayesinde tüm veri trafiği kesintisiz olarak <strong>sunucu veritabanına (meds-pg PostgreSQL)</strong> aktarıldı.
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {/* Service Cards Grid */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {/* Firebase Card */}
                <div className="p-4 rounded-xl border border-line bg-canvas/40 flex flex-col justify-between">
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-bold text-md text-ink flex items-center gap-2">
                        <Database className="w-4 h-4 text-warn" />
                        Firebase Firestore
                      </span>
                      {getStatusBadge(health.firebase.status)}
                    </div>
                    <div className="text-xs text-ink-3 space-y-1">
                      <div>Plan: Spark (Ücretsiz)</div>
                      <div>Günlük Limit: 50.000 Okuma / 20.000 Yazma</div>
                      {health.firebase.details && (
                        <div className="text-ink-2 font-medium mt-1 text-2xs p-1.5 rounded bg-white border border-line/60">
                          {health.firebase.details}
                        </div>
                      )}
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={() => setActiveTab('database')}
                    className="mt-3 text-xs font-semibold text-accent hover:underline inline-flex items-center gap-1 cursor-pointer"
                  >
                    Detayları Görüntüle →
                  </button>
                </div>

                {/* Sunucu veritabanı (meds-pg) kartı */}
                <div className="p-4 rounded-xl border border-line bg-canvas/40 flex flex-col justify-between">
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-bold text-md text-ink flex items-center gap-2">
                        <Database className="w-4 h-4 text-ok" />
                        Veritabanı (meds-pg PostgreSQL)
                      </span>
                      {getStatusBadge(health.supabase.status)}
                    </div>
                    <div className="text-xs text-ink-3 space-y-1">
                      <div>Bağlantı: Sunucu üzerinden (meds-pg)</div>
                      <div>Çıkmış Soru Sayısı: {health.supabase.rowCounts.past_questions || 0}</div>
                      <div>Ders Notu Sayısı: {health.supabase.rowCounts.lecture_notes || 0}</div>
                      {health.supabase.details && (
                        <div className="text-ink-2 font-medium mt-1 text-2xs p-1.5 rounded bg-white border border-line/60">
                          {health.supabase.details}
                        </div>
                      )}
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={() => setActiveTab('database')}
                    className="mt-3 text-xs font-semibold text-accent hover:underline inline-flex items-center gap-1 cursor-pointer"
                  >
                    Detayları Görüntüle →
                  </button>
                </div>

                {/* AI Pool Card */}
                <div className="p-4 rounded-xl border border-line bg-canvas/40 flex flex-col justify-between">
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-bold text-md text-ink flex items-center gap-2">
                        <Cpu className="w-4 h-4 text-ai" />
                        Yapay Zeka (AI)
                      </span>
                      {getStatusBadge(health.ai.status)}
                    </div>
                    <div className="text-xs text-ink-3 space-y-1">
                      <div>Model: Gemini 3.8 Flash</div>
                      <div>Yedek: Groq Cloud (Llama 3.3 70B)</div>
                      <div>Kota Durumu: {health.hasAiQuotaAlert ? 'Limit Aşıldı (429)' : 'Kullanılabilir'}</div>
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={() => setActiveTab('ai')}
                    className="mt-3 text-xs font-semibold text-accent hover:underline inline-flex items-center gap-1 cursor-pointer"
                  >
                    Kotaları & Modelleri İncele →
                  </button>
                </div>
              </div>

              {/* Quick Action Bar */}
              <div className="p-4 rounded-xl border border-line bg-white flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div>
                  <h4 className="font-bold text-base text-ink m-0">Otomatik Teşhis Scripti</h4>
                  <p className="text-xs text-ink-3 m-0">
                    Terminal üzerinden kontrol etmek için: <code className="px-1.5 py-0.5 rounded bg-canvas font-mono text-2xs">npm run check:status</code>
                  </p>
                </div>
                <div className="flex items-center gap-2 shrink-0">
                  <button
                    type="button"
                    onClick={handleRunTest}
                    disabled={isRunningTest}
                    className="h-8 px-3 rounded-lg bg-accent text-white font-semibold text-sm inline-flex items-center gap-1.5 shadow-sm cursor-pointer disabled:opacity-50"
                  >
                    <RefreshCw className={`w-3.5 h-3.5 ${isRunningTest ? 'animate-spin' : ''}`} />
                    Tüm Servisleri Canlı Test Et
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* TAB 2: DATABASE */}
          {activeTab === 'database' && (
            <div className="space-y-6">
              {/* Firebase Deep Dive */}
              <div className="p-5 rounded-xl border border-line bg-white space-y-3">
                <div className="flex items-center justify-between">
                  <h3 className="font-bold text-md text-ink flex items-center gap-2 m-0">
                    <Database className="w-5 h-5 text-warn" />
                    Google Firebase Firestore (Spark Plan)
                  </h3>
                  {getStatusBadge(health.firebase.status)}
                </div>
                <p className="text-sm text-ink-2 m-0">
                  Firebase Spark planı günde en fazla 50.000 okuma ve 20.000 yazma sunar. Bu sınır aşıldığında Firestore <code className="font-mono text-bad-text">resource-exhausted</code> hatası verir.
                </p>
                <div className="p-3 rounded-lg bg-canvas text-xs font-mono space-y-1">
                  <div>• Proje ID: gen-lang-client-0056595657</div>
                  <div>• Veritabanı ID: ai-studio-medsorutpkurulso-8352a999-14d5-45ab-bdf1-62102aece060</div>
                  <div>• Son Durum: {health.firebase.details || health.firebase.status}</div>
                </div>
              </div>

              {/* meds-pg Deep Dive */}
              <div className="p-5 rounded-xl border border-line bg-white space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="font-bold text-md text-ink flex items-center gap-2 m-0">
                    <Database className="w-5 h-5 text-ok" />
                    Veritabanı (meds-pg PostgreSQL 17 + pgvector)
                  </h3>
                  {getStatusBadge(health.supabase.status)}
                </div>
                <p className="text-sm text-ink-2 m-0">
                  meds-pg, soru havuzunu, çıkmış soruları ve amfi ders notlarını tutan ilişkisel veritabanıdır. Tarayıcı veritabanına doğrudan bağlanmaz; tüm sorgular sunucu üzerinden (<code className="font-mono">/api/db/query</code>) geçer.
                </p>

                {/* Table Row Counts */}
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  <div className="p-3 rounded-lg bg-canvas border border-line/50 text-center">
                    <div className="text-2xs font-semibold text-ink-3 uppercase">Kurullar</div>
                    <div className="font-bold text-lg text-ink mt-0.5">{health.supabase.rowCounts.committees || 0}</div>
                  </div>
                  <div className="p-3 rounded-lg bg-canvas border border-line/50 text-center">
                    <div className="text-2xs font-semibold text-ink-3 uppercase">Güncel Sorular</div>
                    <div className="font-bold text-lg text-ink mt-0.5">{health.supabase.rowCounts.questions || 0}</div>
                  </div>
                  <div className="p-3 rounded-lg bg-canvas border border-line/50 text-center">
                    <div className="text-2xs font-semibold text-ink-3 uppercase">Çıkmış Sorular</div>
                    <div className="font-bold text-lg text-ink mt-0.5">{health.supabase.rowCounts.past_questions || 0}</div>
                  </div>
                  <div className="p-3 rounded-lg bg-canvas border border-line/50 text-center">
                    <div className="text-2xs font-semibold text-ink-3 uppercase">Ders Notları</div>
                    <div className="font-bold text-lg text-ink mt-0.5">{health.supabase.rowCounts.lecture_notes || 0}</div>
                  </div>
                </div>

                {/* Realtime Live Test Card */}
                <div className="p-4 rounded-xl border border-line bg-canvas/40 space-y-3">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                    <div>
                      <div className="font-bold text-base text-ink flex items-center gap-1.5">
                        <Zap className="w-4 h-4 text-warn" />
                        Canlı Yayın (Postgres NOTIFY → Sunucu → SSE)
                      </div>
                      <div className="text-xs text-ink-3">
                        Veritabanındaki değişiklikler tüm ziyaretçilere sunucu üzerinden anlık iletilir.
                      </div>
                    </div>
                    <button
                      type="button"
                      onClick={handleTestRealtime}
                      disabled={realtimeTest.running}
                      className="h-8 px-3 rounded-lg bg-accent hover:bg-accent text-white font-semibold text-xs inline-flex items-center gap-1.5 shadow-xs cursor-pointer disabled:opacity-50 shrink-0"
                    >
                      <RefreshCw className={`w-3.5 h-3.5 ${realtimeTest.running ? 'animate-spin' : ''}`} />
                      {realtimeTest.running ? 'Test Ediliyor…' : 'Canlı Yayını Test Et'}
                    </button>
                  </div>

                  {realtimeTest.result && (
                    <div
                      className={`p-3 rounded-xl text-sm font-medium border flex items-start gap-2.5 ${
                        realtimeTest.result.postgresActive
                          ? 'bg-ok-soft text-ok border-ok/30'
                          : realtimeTest.result.broadcastActive
                          ? 'bg-warn-soft text-warn border-warn/30'
                          : 'bg-bad-soft text-bad-text border-bad/30'
                      }`}
                    >
                      {realtimeTest.result.postgresActive ? (
                        <CheckCircle2 className="w-5 h-5 text-ok shrink-0 mt-0.5" />
                      ) : (
                        <AlertTriangle className="w-5 h-5 text-warn shrink-0 mt-0.5" />
                      )}
                      <div className="space-y-1">
                        <div className="font-bold">
                          {realtimeTest.result.postgresActive
                            ? 'Canlı yayın çalışıyor (NOTIFY → SSE gidiş-dönüş başarılı)'
                            : realtimeTest.result.broadcastActive
                            ? 'SSE akışı açık — Postgres bildirimi geri gelmedi'
                            : 'Canlı akışa (SSE) bağlanılamadı'}
                        </div>
                        <div className="text-xs leading-relaxed">
                          {realtimeTest.result.message}
                        </div>
                      </div>
                    </div>
                  )}

                  <div className="p-3 rounded-lg bg-white border border-line/60 text-xs text-ink-2 space-y-1.5">
                    <div>
                      Canlı yayın, Postgres tetikleyicileri (<code className="font-mono">NOTIFY</code>) → sunucu (<code className="font-mono">LISTEN</code>) → SSE (<code className="font-mono">/api/realtime/events</code>) zinciriyle çalışır; tarayıcıda ek bir ayar gerekmez.
                    </div>
                    <div>
                      Sorun varsa sunucu loglarına ve <code className="font-mono">/api/realtime/status</code> uç noktasına bakın.
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* TAB 3: AI POOL & QUOTAS */}
          {activeTab === 'ai' && (
            <div className="space-y-6">
              <div className="p-4 rounded-xl bg-ai-soft border border-ai/30 text-ai text-sm">
                <div className="flex items-start gap-2.5">
                  <Sparkles className="w-5 h-5 text-ai shrink-0 mt-0.5" />
                  <div>
                    <span className="font-bold">4 Kademeli Kesintisiz Yapay Zeka Havuzu:</span>
                    <p className="mt-1 m-0 text-ai">
                      Soru düzenleme ve yeniden yapılandırma fonksiyonlarında sistem önce Ücretsiz Gemini planlarını dener. Kotaya takılırsa (HTTP 429) anında <strong>Groq Cloud (Llama 3.3 70B & DeepSeek R1)</strong> veya Faturalı plana geçer.
                    </p>
                  </div>
                </div>
              </div>

              {/* Key Status List */}
              <div className="space-y-3">
                <h4 className="font-bold text-base text-ink m-0">Tanımlı Yapay Zeka Planları & Canlı Durumları</h4>
                
                {health.ai.keys.length > 0 ? (
                  health.ai.keys.map((k, i) => (
                    <div key={i} className="p-3.5 rounded-xl border border-line bg-white flex items-center justify-between gap-3">
                      <div>
                        <div className="font-bold text-base text-ink">{k.label}</div>
                        <div className="text-xs text-ink-3">{k.details || 'Model: Gemini 3.8 Flash'}</div>
                      </div>
                      {getStatusBadge(k.status)}
                    </div>
                  ))
                ) : (
                  <div className="p-4 rounded-xl border border-line bg-canvas text-center text-sm text-ink-2">
                    Yapay zeka anahtarlarının durumunu görmek için "Yeniden Test Et" butonuna tıklayın.
                  </div>
                )}
              </div>

              {/* Free Groq Cloud Recommendation */}
              <div className="p-5 rounded-xl border border-ai/30 bg-ai-soft space-y-3">
                <h4 className="font-bold text-md text-ai m-0 flex items-center gap-2">
                  <Zap className="w-4 h-4 text-ai" />
                  Öneri: Ücretsiz & Sınırsız Groq Cloud API'sini Ekleyin
                </h4>
                <p className="text-sm text-ai m-0">
                  Groq Cloud, Llama 3.3 70B ve DeepSeek R1 modellerini saniyede 300+ token hızında tamamen ücretsiz sunar. Gemini kotası dolduğunda sorularınızı anında ve kesintisiz düzenleyebilirsiniz.
                </p>
                <div className="flex flex-wrap items-center gap-3 pt-1">
                  <button
                    type="button"
                    onClick={() => setActiveTab('settings')}
                    className="h-8 px-3 rounded-lg bg-ai hover:bg-ai text-white font-semibold text-sm cursor-pointer"
                  >
                    Groq API Anahtarını Tanımla →
                  </button>
                  <a
                    href="https://console.groq.com/keys"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="h-8 px-3 rounded-lg border border-ai/30 bg-white text-ai font-semibold text-sm inline-flex items-center gap-1.5 cursor-pointer"
                  >
                    Ücretsiz Anahtar Al (Groq)
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                </div>
              </div>
            </div>
          )}

          {/* TAB 4: SETTINGS */}
          {activeTab === 'settings' && (
            <div className="space-y-6">
              {saveSuccess && (
                <div className="p-3 rounded-xl bg-ok-soft border border-ok/30 text-ok text-sm flex items-center gap-2">
                  <Check className="w-4 h-4 text-ok" />
                  Ayarlar başarıyla kaydedildi ve tüm bağlantılar güncellendi!
                </div>
              )}

              {/* Database Mode Switcher */}
              <div className="p-4 rounded-xl border border-line bg-white space-y-3">
                <h4 className="font-bold text-base text-ink m-0">Aktif Veritabanı Modu</h4>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
                  <label className={`p-3 rounded-lg border flex flex-col gap-1 cursor-pointer transition-colors ${
                    dbMode === 'auto' ? 'border-accent bg-accent-soft' : 'border-line hover:bg-canvas'
                  }`}>
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-sm text-ink">Otomatik (Önerilen)</span>
                      <input 
                        type="radio" 
                        name="db_mode" 
                        checked={dbMode === 'auto'} 
                        onChange={() => setDbMode('auto')} 
                      />
                    </div>
                    <span className="text-2xs text-ink-3">Firebase Spark kotası dolarsa otomatik olarak sunucu veritabanı (meds-pg) devralır.</span>
                  </label>

                  <label className={`p-3 rounded-lg border flex flex-col gap-1 cursor-pointer transition-colors ${
                    dbMode === 'supabase' ? 'border-accent bg-accent-soft' : 'border-line hover:bg-canvas'
                  }`}>
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-sm text-ink">Yalnızca sunucu veritabanı (meds-pg)</span>
                      <input 
                        type="radio" 
                        name="db_mode" 
                        checked={dbMode === 'supabase'} 
                        onChange={() => setDbMode('supabase')} 
                      />
                    </div>
                    <span className="text-2xs text-ink-3">Firebase kotalarını atlar, doğrudan sunucu üzerinden meds-pg PostgreSQL kullanır.</span>
                  </label>

                  <label className={`p-3 rounded-lg border flex flex-col gap-1 cursor-pointer transition-colors ${
                    dbMode === 'firebase' ? 'border-accent bg-accent-soft' : 'border-line hover:bg-canvas'
                  }`}>
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-sm text-ink">Yalnızca Firebase</span>
                      <input 
                        type="radio" 
                        name="db_mode" 
                        checked={dbMode === 'firebase'} 
                        onChange={() => setDbMode('firebase')} 
                      />
                    </div>
                    <span className="text-2xs text-ink-3">Yalnızca Google Firestore veritabanını kullanır.</span>
                  </label>
                </div>
              </div>

              {/* API Keys Configuration */}
              <div className="p-4 rounded-xl border border-line bg-white space-y-4">
                <h4 className="font-bold text-base text-ink m-0">Kişisel Yapay Zeka API Anahtarları</h4>
                
                <div>
                  <label className="block text-sm font-semibold text-ink mb-1">
                    Google Gemini API Anahtarı (AI Studio)
                  </label>
                  <input
                    type="password"
                    value={customGeminiKey}
                    onChange={(e) => setCustomGeminiKey(e.target.value)}
                    placeholder="AIzaSy... veya AQ.Ab8..."
                    className="w-full h-10 px-3 rounded-lg border border-line bg-field text-sm text-ink font-mono focus:border-accent outline-0"
                  />
                  <span className="text-2xs text-ink-3 mt-1 block">
                    Kendi ücretsiz anahtarınızı girerek genel kota sınırından bağımsız çalışabilirsiniz.
                  </span>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-ink mb-1">
                    Groq Cloud API Anahtarları (3. Sıra: Hızlı & Ücretsiz AI)
                  </label>
                  <input
                    type="password"
                    value={customGroqKey}
                    onChange={(e) => setCustomGroqKey(e.target.value)}
                    placeholder="1. Groq Anahtarı (gsk_...)"
                    className="w-full h-10 px-3 rounded-lg border border-line bg-field text-sm text-ink font-mono focus:border-accent outline-0"
                  />
                  <input
                    type="password"
                    value={customGroqKey2}
                    onChange={(e) => setCustomGroqKey2(e.target.value)}
                    placeholder="2. Yedek Groq Anahtarı (gsk_...)"
                    className="w-full h-10 px-3 mt-2 rounded-lg border border-line bg-field text-sm text-ink font-mono focus:border-accent outline-0"
                  />
                  <span className="text-2xs text-ink-3 mt-1 block">
                    Groq Cloud (OpenAI GPT-OSS 120B / Llama 3.3 / Qwen) kotasız ve ücretsizdir. Biri dolarsa diğeri otomatik devreye girer.
                  </span>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-ink mb-1">
                    Muse Spark 1.3 Free (Son Çare / Tüm Limitler Dolunca Otomatik Kurtarma)
                  </label>
                  <input
                    type="password"
                    value={customMuseSparkKey}
                    onChange={(e) => setCustomMuseSparkKey(e.target.value)}
                    placeholder="Muse Spark / OpenCode / OpenRouter Anahtarı (İsteğe Bağlı)"
                    className="w-full h-10 px-3 rounded-lg border border-line bg-field text-sm text-ink font-mono focus:border-accent outline-0"
                  />
                  <span className="text-2xs text-ink-3 mt-1 block">
                    Gemini ve Groq limitleri dolduğunda otomatik devreye girer. Boş bırakıldığında yerleşik ücretsiz havuz kullanılır.
                  </span>
                </div>
              </div>

              {/* Veritabanı bağlantısı (salt okunur bilgi) */}
              <div className="p-4 rounded-xl border border-line bg-white space-y-2">
                <h4 className="font-bold text-base text-ink m-0">Veritabanı Bağlantısı</h4>
                <p className="text-sm text-ink-2 m-0">
                  Veritabanı (meds-pg PostgreSQL) yalnızca sunucu üzerinden erişilir; tarayıcıda bağlantı adresi veya anahtar girilmez.
                  Tüm sorgular <code className="font-mono">/api/db/query</code> uç noktasından geçer, bağlantı ayarları sunucunun <code className="font-mono">.env</code> dosyasındadır.
                </p>
              </div>

              {/* Save Button */}
              <div className="flex items-center justify-end gap-3 pt-2">
                <button
                  type="button"
                  onClick={handleSaveSettings}
                  className="h-10 px-5 rounded-lg bg-accent hover:bg-accent/90 text-white font-semibold text-base shadow-sm cursor-pointer transition-colors"
                >
                  Ayarları Kaydet ve Test Et
                </button>
              </div>
            </div>
          )}

        </div>

        {/* Footer */}
        <div className="px-6 py-3.5 border-t border-line bg-canvas flex items-center justify-between text-xs text-ink-3 shrink-0">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-ok" />
            <span>MeDSor Dayanıklılık & Kota İzleme Sistemi Aktif</span>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="h-8 px-4 rounded-lg bg-white border border-line hover:bg-canvas text-ink font-semibold text-sm cursor-pointer"
          >
            Kapat
          </button>
        </div>
      </div>
    </div>
  );
};
