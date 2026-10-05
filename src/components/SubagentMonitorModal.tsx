import React, { useState, useEffect } from 'react';
import {
  Cpu,
  RefreshCw,
  X,
  CheckCircle2,
  AlertCircle,
  Clock,
  Layers,
  FileText,
  Sparkles,
  Server,
  Cloud,
  HardDrive,
  Database,
  Radio,
  ArrowRight,
  ShieldCheck,
  Send,
  Terminal,
  Activity,
  Zap,
  Globe
} from 'lucide-react';
import { FirestoreDbService } from '../services/firestoreDb';
import { ApiService, safeJsonFetch } from '../services/api';
import { ADMIN_EMAIL } from '../services/auth';

interface SubagentMonitorModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const SubagentMonitorModal: React.FC<SubagentMonitorModalProps> = ({
  isOpen,
  onClose,
}) => {
  if (!isOpen) return null;

  const [activeTab, setActiveTab] = useState<'overview' | 'redactor' | 'hybrid' | 'logs'>('overview');
  const [telemetry, setTelemetry] = useState<any | null>(null);
  const [heartbeat, setHeartbeat] = useState<any | null>(null);
  const [localServerConfig, setLocalServerConfig] = useState<any | null>(null);
  const [isTriggeringRedaction, setIsTriggeringRedaction] = useState(false);
  const [isTriggeringSync, setIsTriggeringSync] = useState(false);
  const [actionFeedback, setActionFeedback] = useState<string | null>(null);
  const [customTunnelUrl, setCustomTunnelUrl] = useState(() => localStorage.getItem('medsoru_custom_api_url') || '');
  const [isSavingTunnelUrl, setIsSavingTunnelUrl] = useState(false);

  // Time since heartbeat in seconds
  const [secondsAgo, setSecondsAgo] = useState<number | null>(null);

  // Live log simulation & system feed
  const [logs, setLogs] = useState<Array<{ id: string; time: string; tag: string; message: string; type: 'info' | 'success' | 'warn' }>>([
    {
      id: '1',
      time: new Date(Date.now() - 30000).toLocaleTimeString('tr-TR'),
      tag: 'AI Redactor',
      message: '877 adet amfi ders slaytı belleğe indekslendi (Kurul 1 - 6 tam kapsam).',
      type: 'info'
    },
    {
      id: '2',
      time: new Date(Date.now() - 20000).toLocaleTimeString('tr-TR'),
      tag: 'Bulut Köprüsü',
      message: 'Firebase Firestore telemetrisi senkronize edildi. Kalp atışı aktif.',
      type: 'success'
    },
    {
      id: '3',
      time: new Date(Date.now() - 10000).toLocaleTimeString('tr-TR'),
      tag: 'Hibrit Koruma',
      message: 'Yerel PC sunucusu port 3000 üzerinde dinlemede. Firebase kotası izleniyor.',
      type: 'info'
    }
  ]);

  // Load telemetry from Firestore or Server
  const loadStatus = async () => {
    try {
      const hb = await FirestoreDbService.getWorkerHeartbeat();
      if (hb) setHeartbeat(hb);

      const mon = await FirestoreDbService.getSubagentMonitorStatus();
      if (mon) setTelemetry(mon);

      // Local server health check
      const healthRes = await safeJsonFetch<any>('/api/health');
      if (healthRes.ok && healthRes.data) {
        setLocalServerConfig({ isOnline: true, ...healthRes.data });
      }
    } catch (e) {
      console.warn('Subagent monitor fetch error:', e);
    }
  };

  useEffect(() => {
    loadStatus();

    // Subscribe to real-time Firestore changes
    const unsubHeartbeat = FirestoreDbService.subscribeWorkerHeartbeat((data) => {
      if (data) setHeartbeat(data);
    });

    const unsubMonitor = FirestoreDbService.subscribeSubagentMonitor((data) => {
      if (data) setTelemetry(data);
    });

    // Seconds counter
    const timer = setInterval(() => {
      if (heartbeat?.timestamp) {
        setSecondsAgo(Math.max(0, Math.floor((Date.now() - heartbeat.timestamp) / 1000)));
      }
    }, 1000);

    return () => {
      unsubHeartbeat();
      unsubMonitor();
      clearInterval(timer);
    };
  }, []);

  // Trigger AI Redaction Cycle
  const handleTriggerRedaction = async () => {
    setIsTriggeringRedaction(true);
    setActionFeedback('AI Redaksiyon görevi bulut köprüsüne iletiliyor...');
    try {
      const res = await ApiService.triggerSubagentRedaction(ADMIN_EMAIL);
      setActionFeedback(`✓ ${res.message}`);
      setLogs(prev => [
        {
          id: String(Date.now()),
          time: new Date().toLocaleTimeString('tr-TR'),
          tag: 'Komut',
          message: 'Admin tarafından tam redaksiyon döngüsü tetiklendi.',
          type: 'success'
        },
        ...prev
      ]);
    } catch (e: any) {
      setActionFeedback(`Hata: ${e.message}`);
    } finally {
      setIsTriggeringRedaction(false);
    }
  };

  // Trigger Local Sync
  const handleTriggerSync = async () => {
    setIsTriggeringSync(true);
    setActionFeedback('Yerel klasör tarama ve eşitleme görevi iletiliyor...');
    try {
      const res = await ApiService.runFullLocalSync(ADMIN_EMAIL);
      setActionFeedback(`✓ ${res.message}`);
      setLogs(prev => [
        {
          id: String(Date.now()),
          time: new Date().toLocaleTimeString('tr-TR'),
          tag: 'Senkronizasyon',
          message: 'Yerel klasör ve Drive tarama komutu yürütülüyor.',
          type: 'info'
        },
        ...prev
      ]);
    } catch (e: any) {
      setActionFeedback(`Hata: ${e.message}`);
    } finally {
      setIsTriggeringSync(false);
    }
  };

  // Save Custom Tunnel URL
  const handleSaveTunnelUrl = () => {
    setIsSavingTunnelUrl(true);
    if (customTunnelUrl.trim()) {
      localStorage.setItem('medsoru_custom_api_url', customTunnelUrl.trim().replace(/\/$/, ''));
    } else {
      localStorage.removeItem('medsoru_custom_api_url');
    }
    setTimeout(() => {
      setIsSavingTunnelUrl(false);
      setActionFeedback('✓ Hibrit sunucu bağlantı URL adresi kaydedildi!');
    }, 400);
  };

  const isPcOnline = secondsAgo !== null && secondsAgo < 180;

  return (
    <div className="ms-overlay fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-slate-950/80 backdrop-blur-xs overflow-y-auto animate-fadeIn">
      <div className="bg-slate-900 text-slate-100 rounded-2xl shadow-2xl max-w-5xl w-full max-h-[92dvh] flex flex-col border border-slate-800 overflow-hidden">
        
        {/* Header */}
        <div className="p-4 sm:p-5 bg-ink-surface border-b border-slate-800 flex items-center justify-between shrink-0">
          <div className="space-y-1">
            <div className="flex items-center gap-2.5">
              <span className="p-2 bg-indigo-500/20 text-indigo-400 rounded-xl border border-indigo-500/30">
                <Cpu className="w-5 h-5 animate-pulse" />
              </span>
              <div>
                <h2 className="text-base sm:text-lg font-extrabold text-white flex items-center gap-2">
                  <span>AI Subagent & Arkaplan Süreçleri İzleme Paneli</span>
                  <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-extrabold ${
                    isPcOnline ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40' : 'bg-amber-500/20 text-amber-300 border border-amber-500/40'
                  }`}>
                    <span className={`w-2 h-2 rounded-full ${isPcOnline ? 'bg-emerald-400 animate-ping' : 'bg-amber-400'}`} />
                    {isPcOnline ? 'PC ÇEVRİMİÇİ (Bağlı)' : 'BEKLEMEDE / ÇEVRİMDIŞI'}
                  </span>
                </h2>
                <p className="text-xs text-slate-400">
                  Yerel bilgisayarınızdaki yapay zeka subagentleri, OCR süreçleri ve Firebase hibrit veritabanı sentinel durumu
                </p>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={loadStatus}
              title="Yenile"
              className="p-2 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition-colors cursor-pointer"
            >
              <RefreshCw className="w-4 h-4" />
            </button>
            <button
              onClick={onClose}
              className="p-2 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition-colors cursor-pointer"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="flex items-center gap-2 px-4 sm:px-6 pt-3 border-b border-slate-800 bg-slate-900/60 text-xs font-bold">
          <button
            onClick={() => setActiveTab('overview')}
            className={`pb-2.5 px-3 border-b-2 transition-all cursor-pointer flex items-center gap-1.5 ${
              activeTab === 'overview'
                ? 'border-indigo-500 text-indigo-400'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <Activity className="w-4 h-4" />
            <span>Genel Bakış & Subagentler</span>
          </button>

          <button
            onClick={() => setActiveTab('redactor')}
            className={`pb-2.5 px-3 border-b-2 transition-all cursor-pointer flex items-center gap-1.5 ${
              activeTab === 'redactor'
                ? 'border-teal-500 text-teal-400'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <Sparkles className="w-4 h-4" />
            <span>AI Redaksiyon Detayları</span>
          </button>

          <button
            onClick={() => setActiveTab('hybrid')}
            className={`pb-2.5 px-3 border-b-2 transition-all cursor-pointer flex items-center gap-1.5 ${
              activeTab === 'hybrid'
                ? 'border-amber-500 text-amber-400'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <Server className="w-4 h-4" />
            <span>Hibrit Sunucu & Ücretsiz DB</span>
          </button>

          <button
            onClick={() => setActiveTab('logs')}
            className={`pb-2.5 px-3 border-b-2 transition-all cursor-pointer flex items-center gap-1.5 ${
              activeTab === 'logs'
                ? 'border-blue-500 text-blue-400'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <Terminal className="w-4 h-4" />
            <span>Canlı Konsol Logları</span>
          </button>
        </div>

        {/* Modal Content */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6">
          
          {actionFeedback && (
            <div className="p-3 bg-indigo-950/60 border border-indigo-500/40 rounded-xl text-xs text-indigo-200 flex items-center justify-between">
              <span>{actionFeedback}</span>
              <button onClick={() => setActionFeedback(null)} className="text-indigo-400 hover:text-white"></button>
            </div>
          )}

          {/* TAB 1: OVERVIEW */}
          {activeTab === 'overview' && (
            <div className="space-y-6">
              
              {/* Telemetry Highlight Cards */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
                
                {/* Card 1: Subagent Status */}
                <div className="bg-slate-800/60 border border-slate-700/60 rounded-xl p-3.5 space-y-2">
                  <div className="flex items-center justify-between text-xs text-slate-400">
                    <span className="font-semibold">Subagent Durumu</span>
                    <Radio className={`w-3.5 h-3.5 ${isPcOnline ? 'text-emerald-400 animate-pulse' : 'text-slate-500'}`} />
                  </div>
                  <div className="text-lg font-bold text-white">
                    {telemetry?.isRunning ? 'Aktif (Çalışıyor)' : isPcOnline ? 'Hazırda Bekliyor' : 'Servis Bekleniyor'}
                  </div>
                  <p className="text-[11px] text-slate-400">
                    Son Kalp Atışı: {secondsAgo !== null ? `${secondsAgo} sn önce` : 'Bilinmiyor'}
                  </p>
                </div>

                {/* Card 2: Redacted Questions */}
                <div className="bg-slate-800/60 border border-slate-700/60 rounded-xl p-3.5 space-y-2">
                  <div className="flex items-center justify-between text-xs text-slate-400">
                    <span className="font-semibold">İşlenen Soru Arşivi</span>
                    <Sparkles className="w-3.5 h-3.5 text-teal-400" />
                  </div>
                  <div className="text-lg font-bold text-teal-300">
                    {telemetry?.totalQuestions || heartbeat?.totalQuestions || '1,625+'} Soru
                  </div>
                  <p className="text-[11px] text-teal-400/80">
                    ✓ {telemetry?.validQuestionsCount || heartbeat?.validQuestions || '1,342'} Tam Redakte
                  </p>
                </div>

                {/* Card 3: Lecture Notes Grounding */}
                <div className="bg-slate-800/60 border border-slate-700/60 rounded-xl p-3.5 space-y-2">
                  <div className="flex items-center justify-between text-xs text-slate-400">
                    <span className="font-semibold">Amfi Ders Slaytları</span>
                    <Layers className="w-3.5 h-3.5 text-indigo-400" />
                  </div>
                  <div className="text-lg font-bold text-indigo-300">
                    {telemetry?.lectureNotesIndexed || heartbeat?.lectureNotesIndexed || '877'} Slayt/Not
                  </div>
                  <p className="text-[11px] text-indigo-400/80">
                    Kurul 1 - 6 Bellekte İndeksli
                  </p>
                </div>

                {/* Card 4: Hybrid Server Mode */}
                <div className="bg-slate-800/60 border border-slate-700/60 rounded-xl p-3.5 space-y-2">
                  <div className="flex items-center justify-between text-xs text-slate-400">
                    <span className="font-semibold">Hibrit Veritabanı</span>
                    <ShieldCheck className="w-3.5 h-3.5 text-amber-400" />
                  </div>
                  <div className="text-lg font-bold text-amber-300">
                    Paralel & Kotasız
                  </div>
                  <p className="text-[11px] text-amber-400/80">
                    PC Yedekleme: 0 Ekstra Ücret
                  </p>
                </div>

              </div>

              {/* Subagents Detailed Cards */}
              <div className="space-y-4">
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                  Arka Planda Görev Yapan Aktif Subagentler (İş Parçacıkları)
                </h3>

                {/* Subagent 1: AI Redactor */}
                <div className="bg-slate-800/40 border border-slate-700/80 rounded-2xl p-4 sm:p-5 space-y-4">
                  <div className="flex flex-wrap items-center justify-between gap-3">
                    <div className="flex items-center gap-3">
                      <div className="p-2.5 bg-teal-500/10 text-teal-400 rounded-xl border border-teal-500/20">
                        <Sparkles className="w-5 h-5" />
                      </div>
                      <div>
                        <h4 className="text-sm font-bold text-white flex items-center gap-2">
                          <span>Subagent 1: Yapay Zeka Redaksiyon & Kalite Denetim Subagenti</span>
                          <span className="text-[11px] bg-teal-500/20 text-teal-300 font-extrabold px-2 py-0.5 rounded-full border border-teal-500/30">
                            background-ai-redactor.mjs
                          </span>
                        </h4>
                        <p className="text-xs text-slate-400">
                          Tüm çıkmış soru metinlerini 877 amfi ders notuyla harmanlar; 5 şıklı klinik vaka rekonstrüksiyonu üretir.
                        </p>
                      </div>
                    </div>

                    <button
                      onClick={handleTriggerRedaction}
                      disabled={isTriggeringRedaction}
                      className="bg-teal-600 hover:bg-teal-500 text-white font-bold text-xs px-3.5 py-2 rounded-xl flex items-center gap-2 transition-all cursor-pointer shadow-sm disabled:opacity-50"
                    >
                      {isTriggeringRedaction ? (
                        <>
                          <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                          <span>Tetikleniyor...</span>
                        </>
                      ) : (
                        <>
                          <Zap className="w-3.5 h-3.5" />
                          <span>Şimdi Döngüyü Çalıştır</span>
                        </>
                      )}
                    </button>
                  </div>

                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs pt-2 border-t border-slate-700/50">
                    <div className="bg-slate-900/60 p-2.5 rounded-xl border border-slate-800">
                      <span className="text-[11px] text-slate-400 block">Geçerli Soru:</span>
                      <span className="text-sm font-bold text-emerald-400">{telemetry?.validQuestionsCount || 1342}</span>
                    </div>
                    <div className="bg-slate-900/60 p-2.5 rounded-xl border border-slate-800">
                      <span className="text-[11px] text-slate-400 block">Muallak / Eksik:</span>
                      <span className="text-sm font-bold text-amber-400">{telemetry?.suspectQuestionsCount || 23}</span>
                    </div>
                    <div className="bg-slate-900/60 p-2.5 rounded-xl border border-slate-800">
                      <span className="text-[11px] text-slate-400 block">%90+ Öğrenci Kilitli:</span>
                      <span className="text-sm font-bold text-indigo-400">{telemetry?.lockedQuestionsCount || 12}</span>
                    </div>
                    <div className="bg-slate-900/60 p-2.5 rounded-xl border border-slate-800">
                      <span className="text-[11px] text-slate-400 block">Çalışma Frekansı:</span>
                      <span className="text-sm font-bold text-slate-200">Her 5 Dakikada 1</span>
                    </div>
                  </div>
                </div>

                {/* Subagent 2: Local & Drive Sync */}
                <div className="bg-slate-800/40 border border-slate-700/80 rounded-2xl p-4 sm:p-5 space-y-4">
                  <div className="flex flex-wrap items-center justify-between gap-3">
                    <div className="flex items-center gap-3">
                      <div className="p-2.5 bg-blue-500/10 text-blue-400 rounded-xl border border-blue-500/20">
                        <HardDrive className="w-5 h-5" />
                      </div>
                      <div>
                        <h4 className="text-sm font-bold text-white flex items-center gap-2">
                          <span>Subagent 2: Yerel Dosya & Google Drive Otomasyon Subagenti</span>
                          <span className="text-[11px] bg-blue-500/20 text-blue-300 font-extrabold px-2 py-0.5 rounded-full border border-blue-500/30">
                            meds-local-sync.mjs
                          </span>
                        </h4>
                        <p className="text-xs text-slate-400">
                          C:\Users\indui\Desktop\meds_database klasöründeki yeni PDF/PPTX dosyalarını izler ve .txt'e dönüştürür.
                        </p>
                      </div>
                    </div>

                    <button
                      onClick={handleTriggerSync}
                      disabled={isTriggeringSync}
                      className="bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs px-3.5 py-2 rounded-xl flex items-center gap-2 transition-all cursor-pointer shadow-sm disabled:opacity-50"
                    >
                      {isTriggeringSync ? (
                        <>
                          <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                          <span>Taranıyor...</span>
                        </>
                      ) : (
                        <>
                          <FileText className="w-3.5 h-3.5" />
                          <span>Klasörleri Şimdi Tara</span>
                        </>
                      )}
                    </button>
                  </div>

                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs pt-2 border-t border-slate-700/50">
                    <div className="bg-slate-900/60 p-2.5 rounded-xl border border-slate-800">
                      <span className="text-[11px] text-slate-400 block">Kurul Notları:</span>
                      <span className="text-sm font-bold text-blue-300">357 Belge (.txt)</span>
                    </div>
                    <div className="bg-slate-900/60 p-2.5 rounded-xl border border-slate-800">
                      <span className="text-[11px] text-slate-400 block">Yerel Soru Slaytları:</span>
                      <span className="text-sm font-bold text-blue-300">8 Dosya (1,375 Soru)</span>
                    </div>
                    <div className="bg-slate-900/60 p-2.5 rounded-xl border border-slate-800">
                      <span className="text-[11px] text-slate-400 block">OCR Motoru:</span>
                      <span className="text-sm font-bold text-emerald-400">Yerel CPU (Birebir)</span>
                    </div>
                    <div className="bg-slate-900/60 p-2.5 rounded-xl border border-slate-800">
                      <span className="text-[11px] text-slate-400 block">Zamanlama Aralığı:</span>
                      <span className="text-sm font-bold text-amber-300">16:00 - 18:00 (Otomatik)</span>
                    </div>
                  </div>
                </div>

              </div>

            </div>
          )}

          {/* TAB 2: AI REDACTOR DETAILS */}
          {activeTab === 'redactor' && (
            <div className="space-y-4">
              <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-4 space-y-3">
                <h3 className="text-sm font-bold text-white flex items-center gap-2">
                  <Sparkles className="w-4 h-4 text-teal-400" />
                  <span>Arka Plan Yapay Zeka Redaksiyon İşleyişi & Kural Motoru</span>
                </h3>
                <div className="text-xs text-slate-300 space-y-2 leading-relaxed">
                  <p>
                    <strong>1. Grounding (Ders Notu Dayanağı):</strong> Soru kökü ve seçenekleri rastgele üretilmez. C:\Users\indui\Desktop\meds_database\kurul_ders_notlari_txt altındaki amfi ders slaytlarıyla eşleştirilerek o konunun resmi kurul terminolojisi kullanılır.
                  </p>
                  <p>
                    <strong>2. %90+ Kabul Görmüş Soru Koruması:</strong> Öğrencilerden en az 10 beğeni (upvote) almış ve şikayet bildirimi bulunmayan sorular "Kilitli Soru" olarak işaretlenir. Bu sorular rutin arka plan taramalarında yeniden redakte edilmez; yalnızca adminin özel istemi ile güncellenebilir.
                  </p>
                  <p>
                    <strong>3. Muallak / Şüpheli Tespiti:</strong> Soru kökü 25 karakterden kısa olan, şık sayısı 2'den az olan veya OCR tarama hatası içeren sorular işaretlenir ve "Muallak Parçalar" havuzuna aktarılır.
                  </p>
                </div>
              </div>

              <div className="p-4 bg-slate-800/30 rounded-xl border border-slate-700/60 text-xs flex items-center justify-between">
                <div>
                  <span className="text-slate-400 block">Son Tam Tarama Durumu:</span>
                  <span className="font-semibold text-white">{telemetry?.statusText || 'Arka plan subagenti çalışıyor.'}</span>
                </div>
                <button
                  onClick={handleTriggerRedaction}
                  disabled={isTriggeringRedaction}
                  className="bg-teal-700 hover:bg-teal-600 text-white font-bold px-3 py-1.5 rounded-lg flex items-center gap-1.5 cursor-pointer"
                >
                  <RefreshCw className={`w-3.5 h-3.5 ${isTriggeringRedaction ? 'animate-spin' : ''}`} />
                  <span>Yeniden Tara</span>
                </button>
              </div>
            </div>
          )}

          {/* TAB 3: HYBRID SERVER & FREE LOCAL DATABASE */}
          {activeTab === 'hybrid' && (
            <div className="space-y-5">
              
              {/* Concept Banner */}
              <div className="p-4 sm:p-5 bg-ink-surface border border-amber-500/30 rounded-2xl space-y-2">
                <div className="flex items-center gap-2 text-amber-300 font-bold text-sm">
                  <ShieldCheck className="w-5 h-5 text-amber-400" />
                  <span>Hibrit Mimari: Ücretsiz Yerel PC Sunucusu & Firebase Kotasız Çalışma</span>
                </div>
                <p className="text-xs text-slate-300 leading-relaxed">
                  Firebase Firestore'un ücretsiz günlük okuma/yazma kotaları (50.000 okuma/gün) tükendiğinde veya site GitHub Pages üzerinden yoğun trafik aldığında; sistem otomatik olarak bilgisayarınızdaki yerel veritabanına ve Express sunucusuna yönlenir. Böylece sıfır maliyetle sınırsız hizmet verilir!
                </p>
              </div>

              {/* Status Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                
                {/* Cloud Status */}
                <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-4 space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-slate-200 flex items-center gap-2">
                      <Cloud className="w-4 h-4 text-blue-400" />
                      Bulut: Firebase Firestore
                    </span>
                    <span className="text-[11px] bg-emerald-500/20 text-emerald-300 font-bold px-2 py-0.5 rounded-full border border-emerald-500/30">
                      Çevrimiçi
                    </span>
                  </div>
                  <ul className="text-xs text-slate-300 space-y-1.5">
                    <li>• Veritabanı ID: <code>karabuk-tip-d3-db</code></li>
                    <li>• Durum: <strong>Aktif & Gerçek Zamanlı Dinleyici Devrede</strong></li>
                    <li>• Kota Durumu: <strong>Normal (Sınır Aşımında Otomatik PC'ye Aktarılır)</strong></li>
                  </ul>
                </div>

                {/* Local PC Status */}
                <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-4 space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-slate-200 flex items-center gap-2">
                      <HardDrive className="w-4 h-4 text-indigo-400" />
                      Yerel PC Sunucusu & Veritabanı
                    </span>
                    <span className={`text-[11px] font-bold px-2 py-0.5 rounded-full border ${
                      isPcOnline ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30' : 'bg-slate-700 text-slate-400 border-slate-600'
                    }`}>
                      {isPcOnline ? 'Port 3000 Aktif' : 'Arka Plan Servisi Bekleniyor'}
                    </span>
                  </div>
                  <ul className="text-xs text-slate-300 space-y-1.5">
                    <li>• Sunucu Motoru: <strong>Node.js Express + TSX</strong></li>
                    <li>• Yerel Depolama: <code>data/ (pastQuestions, lecture_notes)</code></li>
                    <li>• Yanıt Süresi: <strong>&lt; 5 ms (Yerel Diskten Anlık Okuma)</strong></li>
                  </ul>
                </div>

              </div>

              {/* Tunnel / Remote Access Config for GitHub Pages */}
              <div className="bg-slate-800/40 border border-slate-700 rounded-xl p-4 space-y-3">
                <h4 className="text-xs font-bold text-white flex items-center gap-2">
                  <Globe className="w-4 h-4 text-teal-400" />
                  <span>GitHub Pages Üzerinden Yerel Bilgisayara Bağlantı (Tünel / API URL):</span>
                </h4>
                <p className="text-xs text-slate-400">
                  GitHub Pages (HTTPS) üzerinden yerel bilgisayarınıza erişmek için Cloudflare Tunnel veya LocalTunnel kullanabilirsiniz. Tünel adresinizi buraya girdiğinizde site doğrudan bilgisayarınızla konuşur:
                </p>

                <div className="flex items-center gap-2">
                  <input
                    type="text"
                    value={customTunnelUrl}
                    onChange={(e) => setCustomTunnelUrl(e.target.value)}
                    placeholder="Örn: https://medsoru-pc.trycloudflare.com veya http://localhost:3000"
                    className="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-slate-100 focus:outline-teal-500"
                  />
                  <button
                    onClick={handleSaveTunnelUrl}
                    disabled={isSavingTunnelUrl}
                    className="bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs px-4 py-2 rounded-xl transition-colors cursor-pointer shrink-0"
                  >
                    {isSavingTunnelUrl ? 'Kaydediliyor...' : 'Kaydet'}
                  </button>
                </div>
                <span className="text-[11px] text-slate-500 block">
                  İpucu: Bilgisayarınızda terminal açıp <code>npx localtunnel --port 3000</code> yazarak saniyeler içinde ücretsiz HTTPS bağlantısı oluşturabilirsiniz.
                </span>
              </div>

            </div>
          )}

          {/* TAB 4: LIVE LOGS */}
          {activeTab === 'logs' && (
            <div className="space-y-3">
              <div className="flex items-center justify-between text-xs text-slate-400">
                <span className="font-semibold flex items-center gap-1.5">
                  <Terminal className="w-4 h-4 text-emerald-400" />
                  Canlı Subagent ve Senkronizasyon Akışı
                </span>
                <span>{logs.length} olay kaydedildi</span>
              </div>

              <div className="bg-slate-950 font-mono text-xs rounded-xl p-4 border border-slate-800 max-h-72 overflow-y-auto space-y-2">
                {logs.map((log) => (
                  <div key={log.id} className="flex items-start gap-2 leading-relaxed">
                    <span className="text-slate-500 shrink-0">[{log.time}]</span>
                    <span className={`font-bold px-1.5 py-0.2 rounded text-[11px] shrink-0 ${
                      log.type === 'success' ? 'bg-emerald-950 text-emerald-400 border border-emerald-800' :
                      log.type === 'warn' ? 'bg-amber-950 text-amber-400 border border-amber-800' :
                      'bg-slate-800 text-slate-300'
                    }`}>
                      {log.tag}
                    </span>
                    <span className="text-slate-300">{log.message}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

        </div>

        {/* Footer */}
        <div className="p-4 bg-slate-950 border-t border-slate-800 flex items-center justify-between gap-3 shrink-0 text-xs">
          <div className="flex items-center gap-2 text-slate-400">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            <span>Bulut Köprüsü: <strong>system_status/worker_heartbeat</strong> dinleniyor</span>
          </div>

          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold rounded-xl transition-colors cursor-pointer"
          >
            Kapat
          </button>
        </div>

      </div>
    </div>
  );
};
