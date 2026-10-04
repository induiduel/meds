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
  Layers,
  Copy,
  Check,
  ExternalLink,
  ShieldCheck,
  Server,
  Zap,
  Info,
  Sparkles
} from 'lucide-react';
import { systemHealthMonitor, SystemOverallHealth } from '../services/systemHealthMonitor';
import { multiDbManager, DatabaseMode } from '../services/multiDbManager';
import { getSupabaseConfig, setCustomSupabaseConfig } from '../services/supabaseDb';

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
  const [customSupaUrl, setCustomSupaUrl] = useState<string>(() => getSupabaseConfig().url);
  const [customSupaKey, setCustomSupaKey] = useState<string>(() => getSupabaseConfig().key);
  const [dbMode, setDbMode] = useState<DatabaseMode>(() => multiDbManager.getActiveMode());
  
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [copiedSql, setCopiedSql] = useState(false);
  const [copiedRealtimeSql, setCopiedRealtimeSql] = useState(false);
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

    setCustomSupabaseConfig(customSupaUrl.trim(), customSupaKey.trim());
    multiDbManager.setActiveMode(dbMode);

    setSaveSuccess(true);
    setTimeout(() => setSaveSuccess(false), 2500);

    // Ayarlar değiştiğinde tekrar test yap
    handleRunTest();
  };

  const copySupabaseSql = () => {
    const sql = `-- MedSoru Supabase PostgreSQL Tablo Şeması
CREATE TABLE IF NOT EXISTS committees (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  academic_year TEXT DEFAULT '2026-2027',
  target_questions INTEGER DEFAULT 100,
  color TEXT DEFAULT 'teal',
  data JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS questions (
  id TEXT PRIMARY KEY,
  committee_id TEXT NOT NULL,
  question_number INTEGER,
  discipline TEXT,
  topic TEXT,
  status TEXT DEFAULT 'gathering',
  claimed_answer TEXT,
  upvotes INTEGER DEFAULT 0,
  tags TEXT[] DEFAULT ARRAY[]::TEXT[],
  fragments JSONB DEFAULT '[]'::jsonb,
  options JSONB DEFAULT '[]'::jsonb,
  reconstruction JSONB,
  data JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS past_questions (
  id TEXT PRIMARY KEY,
  committee_id TEXT NOT NULL,
  discipline TEXT,
  topic TEXT,
  exam_year TEXT,
  source_file TEXT,
  claimed_answer TEXT,
  raw_question JSONB,
  reconstruction JSONB,
  upvotes INTEGER DEFAULT 0,
  comments JSONB DEFAULT '[]'::jsonb,
  reports JSONB DEFAULT '[]'::jsonb,
  data JSONB DEFAULT '{}'::jsonb,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS past_question_reports (
  id TEXT PRIMARY KEY,
  question_id TEXT REFERENCES past_questions(id) ON DELETE CASCADE,
  reason TEXT NOT NULL,
  details TEXT,
  reported_by TEXT,
  status TEXT DEFAULT 'pending',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS lecture_notes (
  id TEXT PRIMARY KEY,
  committee_id TEXT NOT NULL,
  discipline TEXT,
  title TEXT NOT NULL,
  pages JSONB DEFAULT '[]'::jsonb,
  page_count INTEGER DEFAULT 0,
  data JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS (Row Level Security) Herkese Açık Okuma/Yazma İzni (Soru havuzunun kesintisiz çalışması için)
ALTER TABLE committees ENABLE ROW LEVEL SECURITY;
ALTER TABLE questions ENABLE ROW LEVEL SECURITY;
ALTER TABLE past_questions ENABLE ROW LEVEL SECURITY;
ALTER TABLE past_question_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE lecture_notes ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public read committees" ON committees FOR SELECT USING (true);
CREATE POLICY "Allow public write committees" ON committees FOR ALL USING (true);

CREATE POLICY "Allow public read questions" ON questions FOR SELECT USING (true);
CREATE POLICY "Allow public write questions" ON questions FOR ALL USING (true);

CREATE POLICY "Allow public read past_questions" ON past_questions FOR SELECT USING (true);
CREATE POLICY "Allow public write past_questions" ON past_questions FOR ALL USING (true);

CREATE POLICY "Allow public read past_question_reports" ON past_question_reports FOR SELECT USING (true);
CREATE POLICY "Allow public write past_question_reports" ON past_question_reports FOR ALL USING (true);

CREATE POLICY "Allow public read lecture_notes" ON lecture_notes FOR SELECT USING (true);
CREATE POLICY "Allow public write lecture_notes" ON lecture_notes FOR ALL USING (true);

-- Realtime yayınlarını ve REPLICA IDENTITY ayarını etkinleştir (Canlı dinleme ve anlık senkronizasyon için)
ALTER PUBLICATION supabase_realtime SET TABLE 
  public.committees, 
  public.questions, 
  public.past_questions, 
  public.past_question_reports,
  public.lecture_notes, 
  public.system_status, 
  public.users;

ALTER TABLE public.committees REPLICA IDENTITY FULL;
ALTER TABLE public.questions REPLICA IDENTITY FULL;
ALTER TABLE public.past_questions REPLICA IDENTITY FULL;
ALTER TABLE public.past_question_reports REPLICA IDENTITY FULL;
ALTER TABLE public.lecture_notes REPLICA IDENTITY FULL;
ALTER TABLE public.system_status REPLICA IDENTITY FULL;
ALTER TABLE public.users REPLICA IDENTITY FULL;
`;
    navigator.clipboard.writeText(sql);
    setCopiedSql(true);
    setTimeout(() => setCopiedSql(false), 2500);
  };

  const copyRealtimeSql = () => {
    const sql = `-- Supabase Realtime Yayınlarını ve REPLICA IDENTITY Ayarını Etkinleştir
ALTER PUBLICATION supabase_realtime SET TABLE 
  public.committees, 
  public.questions, 
  public.past_questions, 
  public.past_question_reports,
  public.lecture_notes, 
  public.system_status, 
  public.users;

ALTER TABLE public.committees REPLICA IDENTITY FULL;
ALTER TABLE public.questions REPLICA IDENTITY FULL;
ALTER TABLE public.past_questions REPLICA IDENTITY FULL;
ALTER TABLE public.past_question_reports REPLICA IDENTITY FULL;
ALTER TABLE public.lecture_notes REPLICA IDENTITY FULL;
ALTER TABLE public.system_status REPLICA IDENTITY FULL;
ALTER TABLE public.users REPLICA IDENTITY FULL;
`;
    navigator.clipboard.writeText(sql);
    setCopiedRealtimeSql(true);
    setTimeout(() => setCopiedRealtimeSql(false), 2500);
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'online':
      case 'ok':
      case 'ready':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[12px] font-semibold bg-emerald-100 text-emerald-900 border border-emerald-300">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-700" />
            Çevrimiçi / Hazır
          </span>
        );
      case 'quota_exceeded':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[12px] font-semibold bg-amber-50 text-amber-800 border border-amber-500">
            <AlertTriangle className="w-3.5 h-3.5 text-amber-600" />
            Kota Aşıldı (429)
          </span>
        );
      case 'high_demand':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[12px] font-semibold bg-amber-50 text-amber-800 border border-amber-400">
            <AlertTriangle className="w-3.5 h-3.5 text-amber-600" />
            Aşırı Yoğun (503)
          </span>
        );
      case 'spending_cap_exceeded':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[12px] font-semibold bg-rose-50 text-rose-800 border border-rose-300">
            <AlertOctagon className="w-3.5 h-3.5 text-rose-500" />
            Harcama Limiti Aşıldı
          </span>
        );
      case 'missing_tables':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[12px] font-semibold bg-amber-200 text-amber-800 border border-amber-500">
            <AlertTriangle className="w-3.5 h-3.5 text-amber-600" />
            Tablolar Eksik
          </span>
        );
      case 'offline':
      case 'error':
      case 'auth_error':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[12px] font-semibold bg-rose-50 text-rose-800 border border-rose-300">
            <AlertOctagon className="w-3.5 h-3.5 text-rose-500" />
            Hata / Çevrimdışı
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[12px] font-semibold bg-gray-100 text-gray-700">
            {status}
          </span>
        );
    }
  };

  return (
    <div className="ms-overlay fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-5 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
      <div 
        role="dialog"
        aria-labelledby="diagnostics-modal-title"
        className="ms-modal-panel w-full max-w-4xl bg-white rounded-2xl shadow-2xl border border-line flex flex-col max-h-[92vh] overflow-hidden"
      >
        {/* Header */}
        <div className="px-5 sm:px-6 py-4 border-b border-line bg-canvas flex items-center justify-between shrink-0">
          <div className="flex items-center gap-3">
            <span className="w-10 h-10 rounded-xl bg-accent text-white flex items-center justify-center shrink-0 shadow-sm">
              <Activity className="w-5 h-5" />
            </span>
            <div>
              <h2 id="diagnostics-modal-title" className="font-display font-bold text-[18px] sm:text-[20px] text-ink m-0 flex items-center gap-2">
                Veritabanı & Limit Takip Paneli
                {health.hasCriticalDatabaseError && (
                  <span className="px-2 py-0.5 rounded-md text-[11px] bg-rose-500 text-white font-bold">
                    KRİTİK HATA
                  </span>
                )}
                {health.hasAiQuotaAlert && (
                  <span className="px-2 py-0.5 rounded-md text-[11px] bg-violet-400 text-white font-bold">
                    AI KOTA LİMİTİ
                  </span>
                )}
              </h2>
              <p className="text-[13px] text-ink-3 m-0">
                Online Firebase, Supabase ve Yapay Zeka servislerinin canlı durum ve limit takibi
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={handleRunTest}
              disabled={isRunningTest}
              className="h-9 px-3 rounded-lg border border-line bg-white hover:bg-canvas text-ink font-semibold text-[13px] inline-flex items-center gap-2 transition-colors cursor-pointer disabled:opacity-50"
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
            className={`py-3 text-[14px] font-semibold border-b-2 transition-colors cursor-pointer whitespace-nowrap ${
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
            className={`py-3 text-[14px] font-semibold border-b-2 transition-colors cursor-pointer whitespace-nowrap flex items-center gap-1.5 ${
              activeTab === 'database'
                ? 'border-accent text-accent'
                : 'border-transparent text-ink-2 hover:text-ink'
            }`}
          >
            <Database className="w-4 h-4" />
            Veritabanları (Firebase & Supabase)
            {health.firebase.status === 'quota_exceeded' && (
              <span className="w-2 h-2 rounded-full bg-amber-600" />
            )}
            {health.hasCriticalDatabaseError && (
              <span className="w-2 h-2 rounded-full bg-rose-500" />
            )}
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('ai')}
            className={`py-3 text-[14px] font-semibold border-b-2 transition-colors cursor-pointer whitespace-nowrap flex items-center gap-1.5 ${
              activeTab === 'ai'
                ? 'border-accent text-accent'
                : 'border-transparent text-ink-2 hover:text-ink'
            }`}
          >
            <Cpu className="w-4 h-4" />
            Yapay Zeka Limitleri (Gemini & Groq)
            {health.hasAiQuotaAlert && (
              <span className="w-2 h-2 rounded-full bg-violet-400" />
            )}
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('settings')}
            className={`py-3 text-[14px] font-semibold border-b-2 transition-colors cursor-pointer whitespace-nowrap flex items-center gap-1.5 ${
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
                <div className="p-4 rounded-xl bg-rose-50 border border-rose-300 text-rose-800">
                  <div className="flex items-start gap-3">
                    <AlertOctagon className="w-5 h-5 text-rose-500 shrink-0 mt-0.5" />
                    <div>
                      <h4 className="font-bold text-[15px] m-0">🚨 Online Veritabanı Kesintisi Tespit Edildi!</h4>
                      <p className="text-[13px] mt-1 m-0 text-rose-800">
                        Online sitede hem Firebase Spark kotası dolmuş hem de Supabase bağlantısı sağlanamıyor.
                        Öğrenciler soru ekleyemez veya soruları yükleyemez. Lütfen <strong>Ayarlar</strong> sekmesinden Supabase bağlantınızı kontrol edin.
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {health.firebase.status === 'quota_exceeded' && health.supabase.status === 'online' && (
                <div className="p-4 rounded-xl bg-amber-50 border border-amber-500 text-amber-800">
                  <div className="flex items-start gap-3">
                    <CheckCircle2 className="w-5 h-5 text-emerald-700 shrink-0 mt-0.5" />
                    <div>
                      <h4 className="font-bold text-[15px] m-0">✓ Otomatik Veritabanı Devri Başarılı</h4>
                      <p className="text-[13px] mt-1 m-0 text-amber-900">
                        Firebase Spark günlük ücretsiz 50.000 okuma kotası doldu. MedSoru otomatik failover sistemi sayesinde tüm veri trafiği kesintisiz olarak <strong>Supabase PostgreSQL</strong> bulut veritabanına aktarıldı.
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
                      <span className="font-bold text-[15px] text-ink flex items-center gap-2">
                        <Database className="w-4 h-4 text-amber-600" />
                        Firebase Firestore
                      </span>
                      {getStatusBadge(health.firebase.status)}
                    </div>
                    <div className="text-[12px] text-ink-3 space-y-1">
                      <div>Plan: Spark (Ücretsiz)</div>
                      <div>Günlük Limit: 50.000 Okuma / 20.000 Yazma</div>
                      {health.firebase.details && (
                        <div className="text-ink-2 font-medium mt-1 text-[11px] p-1.5 rounded bg-white border border-line/60">
                          {health.firebase.details}
                        </div>
                      )}
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={() => setActiveTab('database')}
                    className="mt-3 text-[12px] font-semibold text-accent hover:underline inline-flex items-center gap-1 cursor-pointer"
                  >
                    Detayları Görüntüle →
                  </button>
                </div>

                {/* Supabase Card */}
                <div className="p-4 rounded-xl border border-line bg-canvas/40 flex flex-col justify-between">
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-bold text-[15px] text-ink flex items-center gap-2">
                        <Database className="w-4 h-4 text-emerald-700" />
                        Supabase PostgreSQL
                      </span>
                      {getStatusBadge(health.supabase.status)}
                    </div>
                    <div className="text-[12px] text-ink-3 space-y-1">
                      <div>Veritabanı: kgutsltgmqbnlxcnzrtl</div>
                      <div>Çıkmış Soru Sayısı: {health.supabase.rowCounts.past_questions || 0}</div>
                      <div>Ders Notu Sayısı: {health.supabase.rowCounts.lecture_notes || 0}</div>
                      {health.supabase.details && (
                        <div className="text-ink-2 font-medium mt-1 text-[11px] p-1.5 rounded bg-white border border-line/60">
                          {health.supabase.details}
                        </div>
                      )}
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={() => setActiveTab('database')}
                    className="mt-3 text-[12px] font-semibold text-accent hover:underline inline-flex items-center gap-1 cursor-pointer"
                  >
                    Detayları Görüntüle →
                  </button>
                </div>

                {/* AI Pool Card */}
                <div className="p-4 rounded-xl border border-line bg-canvas/40 flex flex-col justify-between">
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-bold text-[15px] text-ink flex items-center gap-2">
                        <Cpu className="w-4 h-4 text-violet-400" />
                        Yapay Zeka (AI)
                      </span>
                      {getStatusBadge(health.ai.status)}
                    </div>
                    <div className="text-[12px] text-ink-3 space-y-1">
                      <div>Model: Gemini 3.8 Flash</div>
                      <div>Yedek: Groq Cloud (Llama 3.3 70B)</div>
                      <div>Kota Durumu: {health.hasAiQuotaAlert ? 'Limit Aşıldı (429)' : 'Kullanılabilir'}</div>
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={() => setActiveTab('ai')}
                    className="mt-3 text-[12px] font-semibold text-accent hover:underline inline-flex items-center gap-1 cursor-pointer"
                  >
                    Kotaları & Modelleri İncele →
                  </button>
                </div>
              </div>

              {/* Quick Action Bar */}
              <div className="p-4 rounded-xl border border-line bg-white flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div>
                  <h4 className="font-bold text-[14px] text-ink m-0">Otomatik Teşhis Scripti</h4>
                  <p className="text-[12px] text-ink-3 m-0">
                    Terminal üzerinden kontrol etmek için: <code className="px-1.5 py-0.5 rounded bg-canvas font-mono text-[11px]">npm run check:status</code>
                  </p>
                </div>
                <div className="flex items-center gap-2 shrink-0">
                  <button
                    type="button"
                    onClick={handleRunTest}
                    disabled={isRunningTest}
                    className="h-8 px-3 rounded-lg bg-accent text-white font-semibold text-[13px] inline-flex items-center gap-1.5 shadow-sm cursor-pointer disabled:opacity-50"
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
                  <h3 className="font-bold text-[16px] text-ink flex items-center gap-2 m-0">
                    <Database className="w-5 h-5 text-amber-600" />
                    Google Firebase Firestore (Spark Plan)
                  </h3>
                  {getStatusBadge(health.firebase.status)}
                </div>
                <p className="text-[13px] text-ink-2 m-0">
                  Firebase Spark planı günde en fazla 50.000 okuma ve 20.000 yazma sunar. Bu sınır aşıldığında Firestore <code className="font-mono text-red-600">resource-exhausted</code> hatası verir.
                </p>
                <div className="p-3 rounded-lg bg-canvas text-[12px] font-mono space-y-1">
                  <div>• Proje ID: gen-lang-client-0056595657</div>
                  <div>• Veritabanı ID: ai-studio-medsorutpkurulso-8352a999-14d5-45ab-bdf1-62102aece060</div>
                  <div>• Son Durum: {health.firebase.details || health.firebase.status}</div>
                </div>
              </div>

              {/* Supabase Deep Dive */}
              <div className="p-5 rounded-xl border border-line bg-white space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="font-bold text-[16px] text-ink flex items-center gap-2 m-0">
                    <Database className="w-5 h-5 text-emerald-700" />
                    Supabase PostgreSQL Bulut Veritabanı
                  </h3>
                  {getStatusBadge(health.supabase.status)}
                </div>
                <p className="text-[13px] text-ink-2 m-0">
                  Supabase, Firebase kotası dolduğunda veya kapalıyken soru havuzunu, çıkmış soruları ve amfi ders notlarını kesintisiz sunan paralel ilişkisel veritabanıdır.
                </p>

                {/* Table Row Counts */}
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  <div className="p-3 rounded-lg bg-canvas border border-line/50 text-center">
                    <div className="text-[11px] font-semibold text-ink-3 uppercase">Kurullar</div>
                    <div className="font-bold text-[18px] text-ink mt-0.5">{health.supabase.rowCounts.committees || 0}</div>
                  </div>
                  <div className="p-3 rounded-lg bg-canvas border border-line/50 text-center">
                    <div className="text-[11px] font-semibold text-ink-3 uppercase">Güncel Sorular</div>
                    <div className="font-bold text-[18px] text-ink mt-0.5">{health.supabase.rowCounts.questions || 0}</div>
                  </div>
                  <div className="p-3 rounded-lg bg-canvas border border-line/50 text-center">
                    <div className="text-[11px] font-semibold text-ink-3 uppercase">Çıkmış Sorular</div>
                    <div className="font-bold text-[18px] text-ink mt-0.5">{health.supabase.rowCounts.past_questions || 0}</div>
                  </div>
                  <div className="p-3 rounded-lg bg-canvas border border-line/50 text-center">
                    <div className="text-[11px] font-semibold text-ink-3 uppercase">Ders Notları</div>
                    <div className="font-bold text-[18px] text-ink mt-0.5">{health.supabase.rowCounts.lecture_notes || 0}</div>
                  </div>
                </div>

                {/* Realtime Live Test Card */}
                {(() => {
                  const projectRef = (customSupaUrl || '').match(/https:\/\/([^.]+)\.supabase\.co/)?.[1] || 'kgutsltgmqbnlxcnzrtl';
                  return (
                    <div className="p-4 rounded-xl border border-line bg-canvas/40 space-y-3">
                      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                        <div>
                          <div className="font-bold text-[14px] text-ink flex items-center gap-1.5">
                            <Zap className="w-4 h-4 text-amber-600" />
                            Supabase Realtime (Anlık Çift Yönlü İletişim & Canlı Eşitleme)
                          </div>
                          <div className="text-[12px] text-ink-3">
                            WebSocket üzerinden canlı veri dinleme, yayınlama ve cihazlar arası anlık senkronizasyon.
                          </div>
                        </div>
                        <button
                          type="button"
                          onClick={handleTestRealtime}
                          disabled={realtimeTest.running}
                          className="h-8 px-3 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-[12px] inline-flex items-center gap-1.5 shadow-xs cursor-pointer disabled:opacity-50 shrink-0"
                        >
                          <RefreshCw className={`w-3.5 h-3.5 ${realtimeTest.running ? 'animate-spin' : ''}`} />
                          {realtimeTest.running ? 'Test Ediliyor…' : '⚡ Realtime Canlı Test Et'}
                        </button>
                      </div>

                      {realtimeTest.result && (
                        <div className="space-y-3">
                          <div
                            className={`p-3 rounded-xl text-[13px] font-medium border flex items-start gap-2.5 ${
                              realtimeTest.result.postgresActive
                                ? 'bg-emerald-50 text-emerald-900 border-emerald-200'
                                : realtimeTest.result.broadcastActive
                                ? 'bg-amber-50 text-amber-900 border-amber-200'
                                : 'bg-red-50 text-red-900 border-red-200'
                            }`}
                          >
                            {realtimeTest.result.postgresActive ? (
                              <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
                            ) : (
                              <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
                            )}
                            <div className="space-y-1">
                              <div className="font-bold">
                                {realtimeTest.result.postgresActive
                                  ? 'Tam Kapasite: Hem WebSocket Hem PostgreSQL Yayını Aktif!'
                                  : realtimeTest.result.broadcastActive
                                  ? 'WebSocket Canlı Yayını Aktif — PostgreSQL Yayını Açılmalı'
                                  : 'Realtime Bağlantı Hatası'}
                              </div>
                              <div className="text-[12px] leading-relaxed">
                                {realtimeTest.result.message}
                              </div>
                            </div>
                          </div>

                          {/* If PostgreSQL changes not active yet, show 1-click fix buttons and guide */}
                          {!realtimeTest.result.postgresActive && (
                            <div className="p-3.5 bg-white rounded-xl border border-amber-200/90 shadow-xs space-y-2.5">
                              <div className="text-[12px] text-ink font-bold flex items-center gap-1.5">
                                <Sparkles className="w-4 h-4 text-amber-500" />
                                PostgreSQL Realtime Yayınını Açmak İçin (2 Kolay Yol):
                              </div>
                              <div className="text-[12px] text-ink-2 space-y-1.5 pl-1">
                                <div>
                                  <strong>1. Yöntem (Dashboard - 10 saniye):</strong> Supabase panelinizde{' '}
                                  <a
                                    href={`https://supabase.com/dashboard/project/${projectRef}/database/publications`}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="text-indigo-600 font-semibold underline inline-flex items-center gap-0.5"
                                  >
                                    Database &gt; Publications &gt; supabase_realtime
                                    <ExternalLink className="w-3 h-3 inline" />
                                  </a>{' '}
                                  menüsüne tıklayın ve <code>questions</code>, <code>past_questions</code>, <code>lecture_notes</code>, <code>committees</code>, <code>system_status</code> anahtarlarını açın.
                                </div>
                                <div>
                                  <strong>2. Yöntem (1 Tıkla SQL):</strong> Aşağıdaki butona tıklayarak SQL komutunu kopyalayın ve{' '}
                                  <a
                                    href={`https://supabase.com/dashboard/project/${projectRef}/sql/new`}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="text-indigo-600 font-semibold underline inline-flex items-center gap-0.5"
                                  >
                                    Supabase SQL Editöründe
                                    <ExternalLink className="w-3 h-3 inline" />
                                  </a>{' '}
                                  yapıştırıp <strong>Run</strong> butonuna basın.
                                </div>
                              </div>

                              <div className="flex flex-wrap items-center gap-2 pt-1">
                                <button
                                  type="button"
                                  onClick={copyRealtimeSql}
                                  className="h-8 px-3 rounded-lg bg-amber-600 hover:bg-amber-500 text-white font-semibold text-[12px] inline-flex items-center gap-1.5 shadow-xs cursor-pointer"
                                >
                                  {copiedRealtimeSql ? <Check className="w-3.5 h-3.5 text-white" /> : <Copy className="w-3.5 h-3.5" />}
                                  {copiedRealtimeSql ? 'Realtime SQL Kopyalandı!' : '⚡ 1 Tıkla Realtime SQL Kopyala'}
                                </button>

                                <a
                                  href={`https://supabase.com/dashboard/project/${projectRef}/sql/new`}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="h-8 px-3 rounded-lg border border-line bg-white hover:bg-canvas text-ink font-semibold text-[12px] inline-flex items-center gap-1.5 cursor-pointer"
                                >
                                  <ExternalLink className="w-3.5 h-3.5" />
                                  Supabase SQL Editörü Aç
                                </a>

                                <a
                                  href={`https://supabase.com/dashboard/project/${projectRef}/database/publications`}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="h-8 px-3 rounded-lg border border-line bg-white hover:bg-canvas text-ink font-semibold text-[12px] inline-flex items-center gap-1.5 cursor-pointer"
                                >
                                  <ExternalLink className="w-3.5 h-3.5" />
                                  Yayınlar (Publications) Menüsü Aç
                                </a>
                              </div>
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  );
                })()}

                <div className="pt-2 flex flex-wrap items-center gap-3">
                  <button
                    type="button"
                    onClick={copySupabaseSql}
                    className="h-9 px-3 rounded-lg border border-line bg-white hover:bg-canvas text-ink font-semibold text-[13px] inline-flex items-center gap-2 cursor-pointer transition-colors"
                  >
                    {copiedSql ? <Check className="w-4 h-4 text-emerald-700" /> : <Copy className="w-4 h-4" />}
                    {copiedSql ? 'SQL Şeması Kopyalandı!' : 'Supabase SQL Şemasını Kopyala'}
                  </button>
                  <a
                    href="https://supabase.com/dashboard"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="h-9 px-3 rounded-lg border border-line bg-white hover:bg-canvas text-ink font-semibold text-[13px] inline-flex items-center gap-2 cursor-pointer transition-colors"
                  >
                    Supabase Dashboard'a Git
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                </div>
              </div>
            </div>
          )}

          {/* TAB 3: AI POOL & QUOTAS */}
          {activeTab === 'ai' && (
            <div className="space-y-6">
              <div className="p-4 rounded-xl bg-purple-50 border border-purple-200 text-purple-900 text-[13px]">
                <div className="flex items-start gap-2.5">
                  <Sparkles className="w-5 h-5 text-purple-600 shrink-0 mt-0.5" />
                  <div>
                    <span className="font-bold">4 Kademeli Kesintisiz Yapay Zeka Havuzu:</span>
                    <p className="mt-1 m-0 text-purple-800">
                      Soru düzenleme ve yeniden yapılandırma fonksiyonlarında sistem önce Ücretsiz Gemini planlarını dener. Kotaya takılırsa (HTTP 429) anında <strong>Groq Cloud (Llama 3.3 70B & DeepSeek R1)</strong> veya Faturalı plana geçer.
                    </p>
                  </div>
                </div>
              </div>

              {/* Key Status List */}
              <div className="space-y-3">
                <h4 className="font-bold text-[14px] text-ink m-0">Tanımlı Yapay Zeka Planları & Canlı Durumları</h4>
                
                {health.ai.keys.length > 0 ? (
                  health.ai.keys.map((k, i) => (
                    <div key={i} className="p-3.5 rounded-xl border border-line bg-white flex items-center justify-between gap-3">
                      <div>
                        <div className="font-bold text-[14px] text-ink">{k.label}</div>
                        <div className="text-[12px] text-ink-3">{k.details || 'Model: Gemini 3.8 Flash'}</div>
                      </div>
                      {getStatusBadge(k.status)}
                    </div>
                  ))
                ) : (
                  <div className="p-4 rounded-xl border border-line bg-canvas text-center text-[13px] text-ink-2">
                    Yapay zeka anahtarlarının durumunu görmek için "Yeniden Test Et" butonuna tıklayın.
                  </div>
                )}
              </div>

              {/* Free Groq Cloud Recommendation */}
              <div className="p-5 rounded-xl border border-violet-200 bg-violet-50 space-y-3">
                <h4 className="font-bold text-[15px] text-violet-700 m-0 flex items-center gap-2">
                  <Zap className="w-4 h-4 text-violet-500" />
                  Öneri: Ücretsiz & Sınırsız Groq Cloud API'sini Ekleyin
                </h4>
                <p className="text-[13px] text-violet-800 m-0">
                  Groq Cloud, Llama 3.3 70B ve DeepSeek R1 modellerini saniyede 300+ token hızında tamamen ücretsiz sunar. Gemini kotası dolduğunda sorularınızı anında ve kesintisiz düzenleyebilirsiniz.
                </p>
                <div className="flex flex-wrap items-center gap-3 pt-1">
                  <button
                    type="button"
                    onClick={() => setActiveTab('settings')}
                    className="h-8 px-3 rounded-lg bg-violet-500 hover:bg-violet-600 text-white font-semibold text-[13px] cursor-pointer"
                  >
                    Groq API Anahtarını Tanımla →
                  </button>
                  <a
                    href="https://console.groq.com/keys"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="h-8 px-3 rounded-lg border border-violet-200 bg-white text-violet-700 font-semibold text-[13px] inline-flex items-center gap-1.5 cursor-pointer"
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
                <div className="p-3 rounded-xl bg-emerald-100 border border-emerald-300 text-emerald-900 text-[13px] flex items-center gap-2">
                  <Check className="w-4 h-4 text-emerald-700" />
                  Ayarlar başarıyla kaydedildi ve tüm bağlantılar güncellendi!
                </div>
              )}

              {/* Database Mode Switcher */}
              <div className="p-4 rounded-xl border border-line bg-white space-y-3">
                <h4 className="font-bold text-[14px] text-ink m-0">Aktif Veritabanı Modu</h4>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
                  <label className={`p-3 rounded-lg border flex flex-col gap-1 cursor-pointer transition-colors ${
                    dbMode === 'auto' ? 'border-accent bg-accent-soft' : 'border-line hover:bg-canvas'
                  }`}>
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-[13px] text-ink">Otomatik (Önerilen)</span>
                      <input 
                        type="radio" 
                        name="db_mode" 
                        checked={dbMode === 'auto'} 
                        onChange={() => setDbMode('auto')} 
                      />
                    </div>
                    <span className="text-[11px] text-ink-3">Firebase Spark kotası dolarsa otomatik Supabase devralır.</span>
                  </label>

                  <label className={`p-3 rounded-lg border flex flex-col gap-1 cursor-pointer transition-colors ${
                    dbMode === 'supabase' ? 'border-accent bg-accent-soft' : 'border-line hover:bg-canvas'
                  }`}>
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-[13px] text-ink">Yalnızca Supabase</span>
                      <input 
                        type="radio" 
                        name="db_mode" 
                        checked={dbMode === 'supabase'} 
                        onChange={() => setDbMode('supabase')} 
                      />
                    </div>
                    <span className="text-[11px] text-ink-3">Firebase kotalarını atlar, doğrudan Supabase PostgreSQL kullanır.</span>
                  </label>

                  <label className={`p-3 rounded-lg border flex flex-col gap-1 cursor-pointer transition-colors ${
                    dbMode === 'firebase' ? 'border-accent bg-accent-soft' : 'border-line hover:bg-canvas'
                  }`}>
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-[13px] text-ink">Yalnızca Firebase</span>
                      <input 
                        type="radio" 
                        name="db_mode" 
                        checked={dbMode === 'firebase'} 
                        onChange={() => setDbMode('firebase')} 
                      />
                    </div>
                    <span className="text-[11px] text-ink-3">Yalnızca Google Firestore veritabanını kullanır.</span>
                  </label>
                </div>
              </div>

              {/* API Keys Configuration */}
              <div className="p-4 rounded-xl border border-line bg-white space-y-4">
                <h4 className="font-bold text-[14px] text-ink m-0">Kişisel Yapay Zeka API Anahtarları</h4>
                
                <div>
                  <label className="block text-[13px] font-semibold text-ink mb-1">
                    Google Gemini API Anahtarı (AI Studio)
                  </label>
                  <input
                    type="password"
                    value={customGeminiKey}
                    onChange={(e) => setCustomGeminiKey(e.target.value)}
                    placeholder="AIzaSy... veya AQ.Ab8..."
                    className="w-full h-10 px-3 rounded-lg border border-line bg-field text-[13px] text-ink font-mono focus:border-accent outline-0"
                  />
                  <span className="text-[11px] text-ink-3 mt-1 block">
                    Kendi ücretsiz anahtarınızı girerek genel kota sınırından bağımsız çalışabilirsiniz.
                  </span>
                </div>

                <div>
                  <label className="block text-[13px] font-semibold text-ink mb-1">
                    Groq Cloud API Anahtarları (3. Sıra: Hızlı & Ücretsiz AI)
                  </label>
                  <input
                    type="password"
                    value={customGroqKey}
                    onChange={(e) => setCustomGroqKey(e.target.value)}
                    placeholder="1. Groq Anahtarı (gsk_...)"
                    className="w-full h-10 px-3 rounded-lg border border-line bg-field text-[13px] text-ink font-mono focus:border-accent outline-0"
                  />
                  <input
                    type="password"
                    value={customGroqKey2}
                    onChange={(e) => setCustomGroqKey2(e.target.value)}
                    placeholder="2. Yedek Groq Anahtarı (gsk_...)"
                    className="w-full h-10 px-3 mt-2 rounded-lg border border-line bg-field text-[13px] text-ink font-mono focus:border-accent outline-0"
                  />
                  <span className="text-[11px] text-ink-3 mt-1 block">
                    Groq Cloud (OpenAI GPT-OSS 120B / Llama 3.3 / Qwen) kotasız ve ücretsizdir. Biri dolarsa diğeri otomatik devreye girer.
                  </span>
                </div>

                <div>
                  <label className="block text-[13px] font-semibold text-ink mb-1">
                    Muse Spark 1.3 Free (Son Çare / Tüm Limitler Dolunca Otomatik Kurtarma)
                  </label>
                  <input
                    type="password"
                    value={customMuseSparkKey}
                    onChange={(e) => setCustomMuseSparkKey(e.target.value)}
                    placeholder="Muse Spark / OpenCode / OpenRouter Anahtarı (İsteğe Bağlı)"
                    className="w-full h-10 px-3 rounded-lg border border-line bg-field text-[13px] text-ink font-mono focus:border-accent outline-0"
                  />
                  <span className="text-[11px] text-ink-3 mt-1 block">
                    Gemini ve Groq limitleri dolduğunda otomatik devreye girer. Boş bırakıldığında yerleşik ücretsiz havuz kullanılır.
                  </span>
                </div>
              </div>

              {/* Supabase Config */}
              <div className="p-4 rounded-xl border border-line bg-white space-y-4">
                <h4 className="font-bold text-[14px] text-ink m-0">Supabase Bağlantı Bilgileri</h4>
                <div>
                  <label className="block text-[13px] font-semibold text-ink mb-1">Supabase URL</label>
                  <input
                    type="text"
                    value={customSupaUrl}
                    onChange={(e) => setCustomSupaUrl(e.target.value)}
                    className="w-full h-10 px-3 rounded-lg border border-line bg-field text-[13px] text-ink font-mono focus:border-accent outline-0"
                  />
                </div>
                <div>
                  <label className="block text-[13px] font-semibold text-ink mb-1">Supabase Anon / Publishable Key</label>
                  <input
                    type="password"
                    value={customSupaKey}
                    onChange={(e) => setCustomSupaKey(e.target.value)}
                    className="w-full h-10 px-3 rounded-lg border border-line bg-field text-[13px] text-ink font-mono focus:border-accent outline-0"
                  />
                </div>
              </div>

              {/* Save Button */}
              <div className="flex items-center justify-end gap-3 pt-2">
                <button
                  type="button"
                  onClick={handleSaveSettings}
                  className="h-10 px-5 rounded-lg bg-accent hover:bg-accent/90 text-white font-semibold text-[14px] shadow-sm cursor-pointer transition-colors"
                >
                  Ayarları Kaydet ve Test Et
                </button>
              </div>
            </div>
          )}

        </div>

        {/* Footer */}
        <div className="px-6 py-3.5 border-t border-line bg-canvas flex items-center justify-between text-[12px] text-ink-3 shrink-0">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-700" />
            <span>MedSoru Dayanıklılık & Kota İzleme Sistemi Aktif</span>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="h-8 px-4 rounded-lg bg-white border border-line hover:bg-canvas text-ink font-semibold text-[13px] cursor-pointer"
          >
            Kapat
          </button>
        </div>
      </div>
    </div>
  );
};
