import React, { useState, useEffect } from 'react';
import {
  DownloadCloud,
  CheckCircle2,
  AlertCircle,
  Wifi,
  WifiOff,
  RefreshCw,
  Trash2,
  Smartphone,
  HardDrive,
  Database,
  BookOpen,
  Archive,
  Layers,
  Sparkles,
  X,
  Share2,
  BookOpenText,
  FileQuestion,
} from 'lucide-react';
import { offlineDatabaseService, OfflineState } from '../../services/offlineDatabaseService';
import { pwaService, PwaState } from '../../services/pwaService';

interface OfflineDatabaseModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const OfflineDatabaseModal: React.FC<OfflineDatabaseModalProps> = ({ isOpen, onClose }) => {
  const [offlineState, setOfflineState] = useState<OfflineState>(offlineDatabaseService.getState());
  const [pwaState, setPwaState] = useState<PwaState>(pwaService.getState());
  const [isIos, setIsIos] = useState(false);
  const [showIosGuide, setShowIosGuide] = useState(false);

  useEffect(() => {
    const unsubOffline = offlineDatabaseService.subscribe(setOfflineState);
    const unsubPwa = pwaService.subscribe(setPwaState);

    if (typeof window !== 'undefined') {
      const ua = window.navigator.userAgent.toLowerCase();
      setIsIos(/iphone|ipad|ipod/.test(ua));
    }

    return () => {
      unsubOffline();
      unsubPwa();
    };
  }, []);

  if (!isOpen) return null;

  const handleDownload = async () => {
    try {
      const ok = await offlineDatabaseService.downloadEntireDatabase();
      if (!ok) {
        console.warn('[OfflineModal] Download returned false');
      }
    } catch (e: any) {
      console.error('[OfflineModal] Download error:', e);
    }
  };

  const handleClear = async () => {
    if (confirm('Cihazınızdaki çevrimdışı soru ve deste veritabanını temizlemek istediğinize emin misiniz?')) {
      await offlineDatabaseService.clearDatabase();
    }
  };

  const handleInstallPwa = async () => {
    if (pwaState.canInstall) {
      await pwaService.promptInstall();
    } else if (isIos) {
      setShowIosGuide(true);
    }
  };

  const { stats, isDownloading, progress, isOnline, isDatabaseDownloaded } = offlineState;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-slate-950/70 backdrop-blur-sm animate-in fade-in duration-200">
      <div
        className="w-full max-w-lg bg-surface border border-line rounded-3xl shadow-2xl overflow-hidden flex flex-col max-h-[92vh]"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Modal Başlık */}
        <div className="px-5 py-4 border-b border-line flex items-center justify-between bg-surface-hover/30">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-2xl bg-accent-soft text-accent flex items-center justify-center">
              <Database className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-[17px] font-bold text-ink">Çevrimdışı Veritabanı & PWA</h2>
              <div className="flex items-center gap-2 text-xs">
                {isOnline ? (
                  <span className="flex items-center gap-1 text-emerald-600 font-medium">
                    <Wifi className="w-3.5 h-3.5" /> Çevrimiçi
                  </span>
                ) : (
                  <span className="flex items-center gap-1 text-amber-600 font-medium">
                    <WifiOff className="w-3.5 h-3.5" /> Çevrimdışı Mod
                  </span>
                )}
                <span className="text-ink-3">•</span>
                <span className="text-ink-2">Arka Plan Desteği Aktif</span>
              </div>
            </div>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="w-8 h-8 rounded-full flex items-center justify-center text-ink-3 hover:text-ink hover:bg-canvas transition-colors cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal İçerik */}
        <div className="p-5 overflow-y-auto space-y-5 flex-1">
          {/* Durum Özeti Kartı */}
          <div
            className={`p-4 rounded-2xl border transition-all ${
              isDatabaseDownloaded
                ? 'bg-emerald-500/5 border-emerald-500/20 text-emerald-950 dark:text-emerald-100'
                : 'bg-amber-500/5 border-amber-500/20 text-amber-950 dark:text-amber-100'
            }`}
          >
            <div className="flex items-start gap-3">
              {isDatabaseDownloaded ? (
                <div className="w-8 h-8 rounded-xl bg-emerald-500/10 text-emerald-600 flex items-center justify-center shrink-0 mt-0.5">
                  <CheckCircle2 className="w-5 h-5" />
                </div>
              ) : (
                <div className="w-8 h-8 rounded-xl bg-amber-500/10 text-amber-600 flex items-center justify-center shrink-0 mt-0.5">
                  <AlertCircle className="w-5 h-5" />
                </div>
              )}
              <div className="flex-1 min-w-0">
                <h3 className="font-semibold text-sm">
                  {isDatabaseDownloaded
                    ? 'Veritabanı Cihazınızda Kurulu (Tam Çevrimdışı)'
                    : 'Veritabanı Henüz Cihaza İndirilmedi'}
                </h3>
                <p className="text-xs text-ink-2 mt-1 leading-relaxed">
                  {isDatabaseDownloaded
                    ? `İnternetiniz olmasa bile tüm soruları çözebilir, ders destelerini okuyabilirsiniz. (Son indirme: ${
                        stats.downloadedAt
                          ? new Date(stats.downloadedAt).toLocaleDateString('tr-TR', {
                              day: 'numeric',
                              month: 'long',
                              hour: '2-digit',
                              minute: '2-digit',
                            })
                          : 'Tamamlandı'
                      })`
                    : 'Hastanede, metroda veya internetsiz ortamlarda kesintisiz çalışabilmek için tüm veri havuzunu tek tıkla cihazınıza indirebilirsiniz.'}
                </p>
              </div>
            </div>
          </div>

          {/* İndirme İlerleme Çubuğu */}
          {isDownloading && (
            <div className="p-4 rounded-2xl bg-accent-soft border border-accent/20 space-y-2.5">
              <div className="flex items-center justify-between text-xs font-semibold text-accent">
                <span className="flex items-center gap-1.5">
                  <RefreshCw className="w-3.5 h-3.5 animate-spin" /> {progress.stage}
                </span>
                <span>%{progress.percent}</span>
              </div>
              <div className="w-full h-2 bg-accent/20 rounded-full overflow-hidden">
                <div
                  className="h-full bg-accent transition-all duration-300 rounded-full"
                  style={{ width: `${progress.percent}%` }}
                />
              </div>
            </div>
          )}

          {/* Veritabanı Kapsamı Tablosu */}
          <div className="space-y-2">
            <h4 className="text-xs font-bold uppercase tracking-wider text-ink-3">
              Cihaza İndirilen Veriler
            </h4>
            <div className="grid grid-cols-2 gap-2.5">
              <div className="p-3 rounded-2xl bg-canvas border border-line flex items-center gap-3">
                <div className="w-8 h-8 rounded-xl bg-sky-500/10 text-sky-600 flex items-center justify-center shrink-0">
                  <Archive className="w-4 h-4" />
                </div>
                <div>
                  <div className="text-sm font-bold text-ink">
                    {stats.pastQuestionsCount > 0 ? `${stats.pastQuestionsCount.toLocaleString()} Soru` : '5.695 Soru'}
                  </div>
                  <div className="text-[11px] text-ink-3">Çıkmış Sınavlar</div>
                </div>
              </div>

              <div className="p-3 rounded-2xl bg-canvas border border-line flex items-center gap-3">
                <div className="w-8 h-8 rounded-xl bg-purple-500/10 text-purple-600 flex items-center justify-center shrink-0">
                  <Layers className="w-4 h-4" />
                </div>
                <div>
                  <div className="text-sm font-bold text-ink">
                    {stats.decksCount > 0 ? `${stats.decksCount} Deste` : '114+ Deste'}
                  </div>
                  <div className="text-[11px] text-ink-3">İnteraktif Öğren</div>
                </div>
              </div>

              <div className="p-3 rounded-2xl bg-canvas border border-line flex items-center gap-3">
                <div className="w-8 h-8 rounded-xl bg-emerald-500/10 text-emerald-600 flex items-center justify-center shrink-0">
                  <BookOpen className="w-4 h-4" />
                </div>
                <div>
                  <div className="text-sm font-bold text-ink">66+ Ders</div>
                  <div className="text-[11px] text-ink-3">Amfi Notları & Özet</div>
                </div>
              </div>

              <div className="p-3 rounded-2xl bg-canvas border border-line flex items-center gap-3">
                <div className="w-8 h-8 rounded-xl bg-teal-500/10 text-teal-600 flex items-center justify-center shrink-0">
                  <BookOpenText className="w-4 h-4" />
                </div>
                <div>
                  <div className="text-sm font-bold text-ink">
                    {stats.glossaryCount > 0 ? `${stats.glossaryCount} Terim` : '1.000+ Terim'}
                  </div>
                  <div className="text-[11px] text-ink-3">Tıbbi Sözlük</div>
                </div>
              </div>

              <div className="p-3 rounded-2xl bg-canvas border border-line flex items-center gap-3">
                <div className="w-8 h-8 rounded-xl bg-rose-500/10 text-rose-600 flex items-center justify-center shrink-0">
                  <FileQuestion className="w-4 h-4" />
                </div>
                <div>
                  <div className="text-sm font-bold text-ink">
                    {stats.flashcardsCount > 0 ? `${stats.flashcardsCount} Kart` : '2.500+ Kart'}
                  </div>
                  <div className="text-[11px] text-ink-3">Akıl Kartları</div>
                </div>
              </div>

              <div className="p-3 rounded-2xl bg-canvas border border-line flex items-center gap-3">
                <div className="w-8 h-8 rounded-xl bg-amber-500/10 text-amber-600 flex items-center justify-center shrink-0">
                  <HardDrive className="w-4 h-4" />
                </div>
                <div>
                  <div className="text-sm font-bold text-ink">~{stats.estimatedSizeMb || 25} MB</div>
                  <div className="text-[11px] text-ink-3">Yerel Depolama</div>
                </div>
              </div>
            </div>
          </div>

          {/* İndir & Güncelle Butonları */}
          <div className="space-y-2 pt-1">
            <button
              type="button"
              disabled={isDownloading}
              onClick={handleDownload}
              className={`w-full py-3.5 px-4 rounded-2xl font-bold text-sm flex items-center justify-center gap-2 cursor-pointer shadow-lg transition-all ${
                isDownloading
                  ? 'bg-slate-400 text-white cursor-not-allowed'
                  : 'bg-accent text-white hover:bg-accent-hover active:scale-[0.99]'
              }`}
            >
              {isDownloading ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" /> Veritabanı İndiriliyor...
                </>
              ) : isDatabaseDownloaded ? (
                <>
                  <RefreshCw className="w-4 h-4" /> Veritabanını Yenile / Güncelle
                </>
              ) : (
                <>
                  <DownloadCloud className="w-4 h-4" /> Tüm Veritabanını Cihaza İndir
                </>
              )}
            </button>

            {isDatabaseDownloaded && (
              <button
                type="button"
                disabled={isDownloading}
                onClick={handleClear}
                className="w-full py-2.5 px-4 rounded-xl font-medium text-xs text-rose-500 hover:bg-rose-500/10 flex items-center justify-center gap-1.5 cursor-pointer transition-colors"
              >
                <Trash2 className="w-3.5 h-3.5" /> Cihaz Önbelleğini Temizle
              </button>
            )}
          </div>

          {/* PWA Kurulum Bölümü */}
          <div className="p-4 rounded-2xl bg-canvas border border-line space-y-3">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-xl bg-indigo-500/10 text-indigo-600 flex items-center justify-center shrink-0">
                <Smartphone className="w-4 h-4" />
              </div>
              <div className="flex-1 min-w-0">
                <h4 className="text-sm font-bold text-ink">Cihaza Kur (Uygulama Modu)</h4>
                <p className="text-xs text-ink-3">
                  {pwaState.isInstalled
                    ? '✓ MedSoru cihazınızda bağımsız uygulama olarak çalışıyor.'
                    : 'Tarayıcı çubuğu olmadan tam ekran mobil/masaüstü deneyimi.'}
                </p>
              </div>
            </div>

            {!pwaState.isInstalled && (
              <>
                {pwaState.canInstall ? (
                  <button
                    type="button"
                    onClick={handleInstallPwa}
                    className="w-full py-2.5 px-4 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs flex items-center justify-center gap-2 cursor-pointer transition-colors shadow-sm"
                  >
                    <Smartphone className="w-4 h-4" /> Uygulamayı Cihaza Yükle
                  </button>
                ) : isIos ? (
                  <div className="p-3 rounded-xl bg-surface border border-line text-xs text-ink-2 space-y-1.5">
                    <div className="font-semibold text-ink flex items-center gap-1.5">
                      <Share2 className="w-3.5 h-3.5 text-accent" /> iOS Safari Kurulum Rehberi:
                    </div>
                    <ol className="list-decimal list-inside space-y-1 text-ink-3">
                      <li>Safari altındaki <strong>Paylaş</strong> simgesine dokunun.</li>
                      <li>Açılan menüde aşağı kaydırıp <strong>"Ana Ekrana Ekle"</strong>yi seçin.</li>
                    </ol>
                  </div>
                ) : (
                  <div className="text-xs text-ink-3 italic">
                    Tarayıcınızın adres çubuğundaki "Yükle" simgesine tıklayarak doğrudan kurabilirsiniz.
                  </div>
                )}
              </>
            )}
          </div>

          {/* Bilgi Kutusu */}
          <div className="text-[11px] text-ink-3 leading-relaxed text-center px-2">
            💡 Veriler cihazınızın güvenli yerel depolama alanında (IndexedDB) saklanır.
            Arka plan servis yöneticisi (Service Worker) sayesinde internet kesildiğinde otomatik olarak yerel veritabanına geçilir.
          </div>
        </div>
      </div>
    </div>
  );
};
