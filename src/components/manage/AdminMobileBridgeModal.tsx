import React, { useState, useEffect, useCallback } from 'react';
import {
  Smartphone,
  Server,
  Key,
  Bell,
  Volume2,
  Vibrate,
  CheckCircle2,
  AlertTriangle,
  RefreshCw,
  Download,
  ShieldCheck,
  Wifi,
  Globe,
  Cpu,
  X,
  Send,
  ExternalLink,
} from 'lucide-react';
import {
  ORACLE_API_URL,
  getLocalServerUrl,
  setLocalServerUrl,
  getStoredPanelSecret,
  setStoredPanelSecret,
  isHybridBridgeEnabled,
  setHybridBridgeEnabled,
  getPanelTarget,
  PANEL_TARGET_KEY,
  isCapacitorNative,
  isAdminAppMode,
  ADMIN_APP_MODE_KEY,
} from '../../config/deployment';
import { ADMIN_EMAIL, setLocalAdminSession } from '../../services/auth';
import { realtimeEventService } from '../../services/realtimeEvents';
import { toast } from '../ui/Toast';

export interface AdminMobilePrefs {
  pushEnabled: boolean;
  soundEnabled: boolean;
  vibrateEnabled: boolean;
  onReport: boolean;
  onQuestion: boolean;
  onSystem: boolean;
}

const PREFS_KEY = 'medsoru_admin_mob_prefs_v1';

const DEFAULT_PREFS: AdminMobilePrefs = {
  pushEnabled: true,
  soundEnabled: true,
  vibrateEnabled: true,
  onReport: true,
  onQuestion: true,
  onSystem: true,
};

export function loadAdminMobilePrefs(): AdminMobilePrefs {
  try {
    const raw = localStorage.getItem(PREFS_KEY);
    if (raw) return { ...DEFAULT_PREFS, ...JSON.parse(raw) };
  } catch { /* */ }
  return DEFAULT_PREFS;
}

export function saveAdminMobilePrefs(prefs: AdminMobilePrefs): void {
  try {
    localStorage.setItem(PREFS_KEY, JSON.stringify(prefs));
  } catch { /* */ }
}

/** WebAudio ile harici ses dosyası gerektirmeyen net bildirim tınısı */
export function playAdminAlertChime(tone: 'info' | 'urgent' = 'info') {
  try {
    const Ctx = window.AudioContext || (window as any).webkitAudioContext;
    if (!Ctx) return;
    const ctx = new Ctx();
    const now = ctx.currentTime;
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(tone === 'urgent' ? 880 : 660, now);
    osc.frequency.exponentialRampToValueAtTime(tone === 'urgent' ? 1174.66 : 880, now + 0.14);
    gain.gain.setValueAtTime(0.001, now);
    gain.gain.exponentialRampToValueAtTime(0.18, now + 0.02);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.28);
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start(now);
    osc.stop(now + 0.3);
    setTimeout(() => { try { void ctx.close(); } catch { /* */ } }, 400);
  } catch { /* */ }
}

export function triggerAdminDeviceAlert(title: string, body: string, urgent = false) {
  const prefs = loadAdminMobilePrefs();
  if (prefs.vibrateEnabled && typeof navigator !== 'undefined' && 'vibrate' in navigator) {
    try {
      navigator.vibrate(urgent ? [160, 80, 220, 80, 160] : [120, 60, 140]);
    } catch { /* */ }
  }
  if (prefs.soundEnabled) {
    playAdminAlertChime(urgent ? 'urgent' : 'info');
  }
  if (prefs.pushEnabled && typeof window !== 'undefined' && 'Notification' in window && Notification.permission === 'granted') {
    try {
      if ('serviceWorker' in navigator) {
        void navigator.serviceWorker.getRegistration().then((reg) => {
          if (reg && 'showNotification' in reg) {
            void reg.showNotification(title, {
              body,
              icon: '/icons/icon-192x192.png',
              badge: '/icons/icon-96x96.png',
              tag: `medsor-admin-${Date.now()}`,
            });
          } else {
            new Notification(title, { body, icon: '/icons/icon-192x192.png' });
          }
        });
      } else {
        new Notification(title, { body, icon: '/icons/icon-192x192.png' });
      }
    } catch { /* */ }
  }
}

/** Yönetim konsolu açıkken gerçek zamanlı SSE olaylarını mobil bildirim/ses/titreşime dönüştürür */
export function useAdminMobileRealtimeAlerts(enabled = true) {
  useEffect(() => {
    if (!enabled) return;
    const unsubNotif = realtimeEventService.onNotification((n) => {
      const prefs = loadAdminMobilePrefs();
      const isReport = n.type === 'report';
      if (isReport && !prefs.onReport) return;
      if (!isReport && !prefs.onQuestion) return;
      triggerAdminDeviceAlert(
        n.title || 'MeDSor Yönetim Bildirimi',
        n.message || 'Yeni yönetici bildirimi geldi.',
        isReport
      );
    });
    const unsubAuto = realtimeEventService.onAutoRepairUpdate((d) => {
      const prefs = loadAdminMobilePrefs();
      if (!prefs.onSystem) return;
      if (d?.status === 'failed' || d?.status === 'completed') {
        triggerAdminDeviceAlert(
          'MeDSor Otomasyon / Hat',
          d?.message || `Otomasyon durumu güncellendi: ${d?.status}`,
          d?.status === 'failed'
        );
      }
    });
    return () => {
      unsubNotif();
      unsubAuto();
    };
  }, [enabled]);
}

interface ProbeState {
  status: 'idle' | 'checking' | 'ok' | 'error';
  ms?: number;
  detail?: string;
}

export const AdminMobileBridgeModal: React.FC<{
  open: boolean;
  onClose: () => void;
  onTargetChanged?: (target: 'oracle' | 'yerel') => void;
}> = ({ open, onClose, onTargetChanged }) => {
  const [target, setTarget] = useState<'oracle' | 'yerel'>(() => getPanelTarget());
  const [localUrl, setLocalUrlState] = useState<string>(() => getLocalServerUrl());
  const [hybrid, setHybridState] = useState<boolean>(() => isHybridBridgeEnabled());
  const [secret, setSecretState] = useState<string>(() => getStoredPanelSecret());
  const [secretMasked, setSecretMasked] = useState(true);
  const [prefs, setPrefs] = useState<AdminMobilePrefs>(() => loadAdminMobilePrefs());
  const [adminAppBoot, setAdminAppBoot] = useState<boolean>(() => isAdminAppMode());

  const [oracleProbe, setOracleProbe] = useState<ProbeState>({ status: 'idle' });
  const [localProbe, setLocalProbe] = useState<ProbeState>({ status: 'idle' });
  const [authVerify, setAuthVerify] = useState<{ status: 'idle' | 'checking' | 'ok' | 'error'; msg?: string }>({ status: 'idle' });

  const probeUrl = useCallback(async (baseUrl: string, setter: React.Dispatch<React.SetStateAction<ProbeState>>) => {
    setter({ status: 'checking' });
    const t0 = performance.now();
    try {
      const ctl = new AbortController();
      const timer = setTimeout(() => ctl.abort(), 5000);
      const res = await fetch(`${baseUrl.replace(/\/$/, '')}/api/health`, {
        cache: 'no-store',
        signal: ctl.signal,
      });
      clearTimeout(timer);
      const ms = Math.round(performance.now() - t0);
      if (res.ok) {
        setter({ status: 'ok', ms, detail: `HTTP 200 · ${ms} ms` });
      } else {
        setter({ status: 'error', ms, detail: `HTTP ${res.status}` });
      }
    } catch (e: any) {
      setter({ status: 'error', detail: e?.name === 'AbortError' ? 'Zaman aşımı (5 sn)' : 'Ulaşılamadı (Ağ/Tünel kontrol edin)' });
    }
  }, []);

  useEffect(() => {
    if (!open) return;
    void probeUrl(ORACLE_API_URL, setOracleProbe);
    void probeUrl(localUrl, setLocalProbe);
  }, [open, localUrl, probeUrl]);

  if (!open) return null;

  const updatePref = (key: keyof AdminMobilePrefs, val: boolean) => {
    const next = { ...prefs, [key]: val };
    setPrefs(next);
    saveAdminMobilePrefs(next);
    if (key === 'pushEnabled' && val && typeof window !== 'undefined' && 'Notification' in window && Notification.permission === 'default') {
      void Notification.requestPermission();
    }
  };

  const handleSaveConnection = async () => {
    setLocalServerUrl(localUrl);
    setHybridBridgeEnabled(hybrid);
    setStoredPanelSecret(secret);
    try {
      if (adminAppBoot) localStorage.setItem(ADMIN_APP_MODE_KEY, '1');
      else localStorage.removeItem(ADMIN_APP_MODE_KEY);
    } catch { /* */ }

    if (secret.trim().length >= 24) {
      setAuthVerify({ status: 'checking', msg: 'Yönetici anahtarı doğrulanıyor…' });
      try {
        const testBase = target === 'yerel' ? localUrl.replace(/\/$/, '') : ORACLE_API_URL.replace(/\/$/, '');
        const res = await fetch(`${testBase}/api/admin/servis/list`, {
          headers: {
            'x-panel-secret': secret.trim(),
            'x-admin-email': ADMIN_EMAIL,
          },
          cache: 'no-store',
        });
        if (res.ok) {
          setLocalAdminSession(ADMIN_EMAIL);
          setAuthVerify({ status: 'ok', msg: 'Yönetici anahtarı doğrulandı ve kalıcı oturum açıldı.' });
          toast.success('Yönetici köprüsü ve kalıcı anahtar kaydedildi.');
        } else {
          setAuthVerify({ status: 'error', msg: `Anahtar sunucu tarafından reddedildi (HTTP ${res.status}).` });
        }
      } catch {
        // Sunucuya o an ulaşılamasa bile anahtarı sakla ve yerel oturumu hazırla
        setLocalAdminSession(ADMIN_EMAIL);
        setAuthVerify({ status: 'ok', msg: 'Anahtar kaydedildi (çevrimdışı/yerel kayıt).' });
      }
    } else {
      toast.success('Sunucu ve bildirim ayarları kaydedildi.');
    }

    if (target !== getPanelTarget()) {
      try { localStorage.setItem(PANEL_TARGET_KEY, target); } catch { /* */ }
      if (onTargetChanged) onTargetChanged(target);
      else window.location.reload();
    }
  };

  return (
    <div
      className="fixed inset-0 z-[120] bg-black/55 backdrop-blur-xs flex items-end sm:items-center justify-center p-0 sm:p-4"
      onMouseDown={(e) => e.target === e.currentTarget && onClose()}
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-label="MeDSor Mobil Yönetim Köprüsü ve APK"
        className="w-full sm:max-w-[620px] max-h-[92dvh] bg-[var(--color-white)] text-[var(--color-ink)] border border-[var(--color-line)] rounded-t-2xl sm:rounded-2xl shadow-2xl flex flex-col overflow-hidden"
      >
        <header className="flex items-center justify-between gap-3 px-4 py-3.5 border-b border-[var(--color-line)] bg-[var(--color-canvas)]">
          <div className="flex items-center gap-2.5 min-w-0">
            <span className="w-9 h-9 rounded-xl bg-[var(--color-accent)] text-white flex items-center justify-center shrink-0">
              <Smartphone className="w-5 h-5" />
            </span>
            <div className="min-w-0">
              <h2 className="m-0 text-base font-bold leading-tight truncate">
                MeDSor Yönetim · Mobil Köprü & APK
              </h2>
              <p className="m-0 text-xs text-[var(--color-ink-3)] truncate">
                {isCapacitorNative() ? 'Android Yerel Uygulama (Capacitor) aktif' : 'Uzaktan sunucu erişimi, kalıcı yetki ve anlık bildirimler'}
              </p>
            </div>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="m14-btn ghost icon"
            aria-label="Kapat"
          >
            <X />
          </button>
        </header>

        <div className="flex-1 overflow-y-auto p-4 space-y-4 text-sm">
          {/* 1. Sunucu Hedefi ve Hibrit Köprü */}
          <section className="p-3.5 rounded-xl border border-[var(--color-line)] bg-[var(--color-canvas)] space-y-3">
            <div className="flex items-center justify-between gap-2">
              <div className="flex items-center gap-2 font-semibold">
                <Server className="w-4 h-4 text-[var(--color-accent)]" />
                <span>Veri & Servis Kaynağı (Canlı ↔ Yerel)</span>
              </div>
              <button
                type="button"
                onClick={() => {
                  void probeUrl(ORACLE_API_URL, setOracleProbe);
                  void probeUrl(localUrl, setLocalProbe);
                }}
                className="m14-btn ghost !h-7 !px-2.5 !text-xs"
              >
                <RefreshCw className={`w-3.5 h-3.5 ${oracleProbe.status === 'checking' || localProbe.status === 'checking' ? 'animate-spin' : ''}`} />
                Ping
              </button>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
              <button
                type="button"
                onClick={() => setTarget('oracle')}
                className={`p-3 rounded-xl border text-left transition flex flex-col gap-1 cursor-pointer ${
                  target === 'oracle'
                    ? 'border-[var(--color-accent)] bg-[var(--color-accent-soft)]'
                    : 'border-[var(--color-line)] bg-[var(--color-white)]'
                }`}
              >
                <div className="flex items-center justify-between gap-2">
                  <span className="font-bold flex items-center gap-1.5">
                    <Globe className="w-4 h-4 text-[var(--color-accent)]" />
                    Canlı (Oracle)
                  </span>
                  <span className={`m14-pill ${oracleProbe.status === 'ok' ? 'ok' : oracleProbe.status === 'error' ? 'bad' : ''}`}>
                    {oracleProbe.status === 'checking' ? 'Ölçülüyor…' : oracleProbe.detail || 'Hazır'}
                  </span>
                </div>
                <span className="text-xs text-[var(--color-ink-3)] truncate">{ORACLE_API_URL}</span>
              </button>

              <button
                type="button"
                onClick={() => setTarget('yerel')}
                className={`p-3 rounded-xl border text-left transition flex flex-col gap-1 cursor-pointer ${
                  target === 'yerel'
                    ? 'border-[var(--color-accent)] bg-[var(--color-accent-soft)]'
                    : 'border-[var(--color-line)] bg-[var(--color-white)]'
                }`}
              >
                <div className="flex items-center justify-between gap-2">
                  <span className="font-bold flex items-center gap-1.5">
                    <Cpu className="w-4 h-4 text-[var(--color-accent)]" />
                    Yerel Cihaz (3000)
                  </span>
                  <span className={`m14-pill ${localProbe.status === 'ok' ? 'ok' : localProbe.status === 'error' ? 'warn' : ''}`}>
                    {localProbe.status === 'checking' ? 'Ölçülüyor…' : localProbe.detail || 'Yerel'}
                  </span>
                </div>
                <span className="text-xs text-[var(--color-ink-3)] truncate">{localUrl}</span>
              </button>
            </div>

            <div className="space-y-1.5 pt-1">
              <label className="block text-xs font-semibold text-[var(--color-ink-2)]">
                Yerel Sunucu Adresi (Wi-Fi LAN IP, Tailscale veya Tünel)
              </label>
              <div className="flex gap-2">
                <input
                  type="url"
                  value={localUrl}
                  onChange={(e) => setLocalUrlState(e.target.value)}
                  placeholder="http://192.168.1.46:3000"
                  className="flex-1 h-9 px-3 rounded-lg border border-[var(--color-line-2)] bg-[var(--color-white)] text-sm font-mono"
                />
                <button
                  type="button"
                  onClick={() => void probeUrl(localUrl, setLocalProbe)}
                  className="m14-btn !h-9"
                >
                  <Wifi className="w-4 h-4" /> Test Et
                </button>
              </div>
            </div>

            <label className="flex items-start gap-2.5 pt-1 cursor-pointer select-none">
              <input
                type="checkbox"
                checked={hybrid}
                onChange={(e) => setHybridState(e.target.checked)}
                className="mt-0.5 w-4 h-4 accent-[var(--color-accent)]"
              />
              <span className="text-xs text-[var(--color-ink-2)] leading-relaxed">
                <b>Hibrit Köprü:</b> Canlı (Oracle) modundayken yalnız yerel makinede çalışan <code>Hat Panosu</code>, <code>Betikler</code>, <code>Otomasyon</code> ve <code>Ders Revize</code> isteklerini otomatik olarak yukarıdaki yerel sunucu adresine yönlendir.
              </span>
            </label>
          </section>

          {/* 2. Kalıcı Yönetici Anahtarı (MEDS_PANEL_SECRET) */}
          <section className="p-3.5 rounded-xl border border-[var(--color-line)] bg-[var(--color-canvas)] space-y-2.5">
            <div className="flex items-center justify-between gap-2">
              <div className="flex items-center gap-2 font-semibold">
                <Key className="w-4 h-4 text-[var(--color-accent)]" />
                <span>Kalıcı Yönetici Anahtarı (MEDS_PANEL_SECRET)</span>
              </div>
              {secret.trim().length >= 24 && (
                <span className="m14-pill ok">Tanımlı ({secret.trim().length} krk)</span>
              )}
            </div>
            <p className="m-0 text-xs text-[var(--color-ink-3)] leading-relaxed">
              Android WebView içinde Google oturumu düşse bile <code>Kişiler</code>, <code>meds-pg Veritabanı Gezgini</code>, <code>Servis Denetimi</code> ve <code>Hat Panosu</code> uçlarına kesintisiz güçlü yönetici (<code>via: secret</code>) yetkisi sağlar.
            </p>
            <div className="flex gap-2">
              <input
                type={secretMasked ? 'password' : 'text'}
                value={secret}
                onChange={(e) => setSecretState(e.target.value)}
                placeholder="Sunucu .env dosyasındaki MEDS_PANEL_SECRET değeri"
                className="flex-1 h-9 px-3 rounded-lg border border-[var(--color-line-2)] bg-[var(--color-white)] text-sm font-mono"
              />
              <button
                type="button"
                onClick={() => setSecretMasked((v) => !v)}
                className="m14-btn !h-9 !px-3"
              >
                {secretMasked ? 'Göster' : 'Gizle'}
              </button>
            </div>
            {authVerify.status !== 'idle' && (
              <div className={`flex items-center gap-2 text-xs p-2 rounded-lg ${
                authVerify.status === 'ok'
                  ? 'bg-[var(--color-ok-soft)] text-[var(--color-ok)]'
                  : authVerify.status === 'error'
                  ? 'bg-[var(--color-bad-soft)] text-[var(--color-bad-text)]'
                  : 'bg-[var(--color-field)] text-[var(--color-ink-2)]'
              }`}>
                {authVerify.status === 'ok' ? <CheckCircle2 className="w-4 h-4 shrink-0" /> : <AlertTriangle className="w-4 h-4 shrink-0" />}
                <span>{authVerify.msg}</span>
              </div>
            )}

            <label className="flex items-center gap-2.5 pt-1 cursor-pointer select-none">
              <input
                type="checkbox"
                checked={adminAppBoot}
                onChange={(e) => setAdminAppBoot(e.target.checked)}
                className="w-4 h-4 accent-[var(--color-accent)]"
              />
              <span className="text-xs text-[var(--color-ink-2)]">
                <b>Yönetim Uygulaması Kipi:</b> Uygulama açıldığında doğrudan gelişmiş yönetim paneline (<code>/manage</code>) gir ve siteye geçildiğinde yüzen yönetim çubuğunu göster.
              </span>
            </label>
          </section>

          {/* 3. Anlık Mobil Bildirimler & Uyarılar */}
          <section className="p-3.5 rounded-xl border border-[var(--color-line)] bg-[var(--color-canvas)] space-y-2.5">
            <div className="flex items-center justify-between gap-2">
              <div className="flex items-center gap-2 font-semibold">
                <Bell className="w-4 h-4 text-[var(--color-accent)]" />
                <span>Mobil Anlık Bildirim & Uyarı Merkezi</span>
              </div>
              <button
                type="button"
                onClick={() => {
                  triggerAdminDeviceAlert(
                    'MeDSor Yönetim · Test Bildirimi',
                    'Anlık bildirim, ses ve titreşim köprüsü sorunsuz çalışıyor.',
                    false
                  );
                  toast.success('Test bildirimi ve sesli uyarı tetiklendi.');
                }}
                className="m14-btn !h-7 !px-2.5 !text-xs"
              >
                <Send className="w-3.5 h-3.5" /> Test Bildirimi
              </button>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
              <label className="flex items-center gap-2 p-2.5 rounded-lg border border-[var(--color-line)] bg-[var(--color-white)] cursor-pointer">
                <input
                  type="checkbox"
                  checked={prefs.pushEnabled}
                  onChange={(e) => updatePref('pushEnabled', e.target.checked)}
                  className="w-4 h-4 accent-[var(--color-accent)]"
                />
                <Bell className="w-4 h-4 text-[var(--color-ink-3)]" />
                <span className="text-xs font-medium">Sistem Bildirimi</span>
              </label>
              <label className="flex items-center gap-2 p-2.5 rounded-lg border border-[var(--color-line)] bg-[var(--color-white)] cursor-pointer">
                <input
                  type="checkbox"
                  checked={prefs.soundEnabled}
                  onChange={(e) => updatePref('soundEnabled', e.target.checked)}
                  className="w-4 h-4 accent-[var(--color-accent)]"
                />
                <Volume2 className="w-4 h-4 text-[var(--color-ink-3)]" />
                <span className="text-xs font-medium">Sesli Uyarı</span>
              </label>
              <label className="flex items-center gap-2 p-2.5 rounded-lg border border-[var(--color-line)] bg-[var(--color-white)] cursor-pointer">
                <input
                  type="checkbox"
                  checked={prefs.vibrateEnabled}
                  onChange={(e) => updatePref('vibrateEnabled', e.target.checked)}
                  className="w-4 h-4 accent-[var(--color-accent)]"
                />
                <Vibrate className="w-4 h-4 text-[var(--color-ink-3)]" />
                <span className="text-xs font-medium">Titreşim</span>
              </label>
            </div>

            <div className="flex flex-wrap gap-3 pt-1">
              <label className="flex items-center gap-1.5 text-xs cursor-pointer">
                <input
                  type="checkbox"
                  checked={prefs.onReport}
                  onChange={(e) => updatePref('onReport', e.target.checked)}
                  className="w-3.5 h-3.5 accent-[var(--color-accent)]"
                />
                <span>Hata & Şikayetler</span>
              </label>
              <label className="flex items-center gap-1.5 text-xs cursor-pointer">
                <input
                  type="checkbox"
                  checked={prefs.onQuestion}
                  onChange={(e) => updatePref('onQuestion', e.target.checked)}
                  className="w-3.5 h-3.5 accent-[var(--color-accent)]"
                />
                <span>Yeni Soru / Taslak / Yorum</span>
              </label>
              <label className="flex items-center gap-1.5 text-xs cursor-pointer">
                <input
                  type="checkbox"
                  checked={prefs.onSystem}
                  onChange={(e) => updatePref('onSystem', e.target.checked)}
                  className="w-3.5 h-3.5 accent-[var(--color-accent)]"
                />
                <span>Hat Panosu & Otomasyon</span>
              </label>
            </div>
          </section>

          {/* 4. Android APK İndirme Kartı */}
          <section className="p-3.5 rounded-xl border border-[var(--color-line)] bg-[var(--color-canvas)] flex flex-wrap items-center justify-between gap-3">
            <div className="space-y-0.5 min-w-0 flex-1">
              <div className="flex items-center gap-2 font-semibold">
                <ShieldCheck className="w-4 h-4 text-[var(--color-ok)]" />
                <span>MeDSor Yönetim · Yerel Android Paketi (.apk)</span>
              </div>
              <p className="m-0 text-xs text-[var(--color-ink-3)]">
                Capacitor ile derlenmiş doğrudan yönetim konsolu + tüm site işlevlerini içeren Android kurulum paketi.
              </p>
            </div>
            <a
              href="/apk/medsor-yonetim.apk"
              download="medsor-yonetim.apk"
              className="m14-btn primary no-underline"
            >
              <Download className="w-4 h-4" />
              APK İndir
            </a>
          </section>
        </div>

        <footer className="flex items-center justify-end gap-2 px-4 py-3 border-t border-[var(--color-line)] bg-[var(--color-canvas)]">
          <button type="button" onClick={onClose} className="m14-btn">
            Vazgeç
          </button>
          <button type="button" onClick={() => void handleSaveConnection()} className="m14-btn primary">
            <CheckCircle2 className="w-4 h-4" />
            Uygula ve Kaydet
          </button>
        </footer>
      </div>
    </div>
  );
};
