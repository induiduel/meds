import React, { useState, useEffect, useRef } from 'react';
import {
  Play,
  Pause,
  RotateCcw,
  ChevronLeft,
  ChevronRight,
  Volume2,
  VolumeX,
  Maximize2,
  Minimize2,
  Sparkles,
  AlertCircle,
  ArrowDown,
  ShieldAlert,
  Layers,
  ArrowRight,
} from 'lucide-react';
import type { MechanismPathway, PathwayStep } from '../../../types/pathway';
import { speak, stopSpeaking, onSpeakingChange } from '../../../utils/tts';

interface AnimatedPathwayPlayerProps {
  pathway: MechanismPathway;
  autoPlayInitial?: boolean;
  onFinish?: () => void;
  className?: string;
}

export const AnimatedPathwayPlayer: React.FC<AnimatedPathwayPlayerProps> = ({
  pathway,
  autoPlayInitial = false,
  onFinish,
  className = '',
}) => {
  const [currentStepIndex, setCurrentStepIndex] = useState<number>(0);
  const [isPlaying, setIsPlaying] = useState<boolean>(autoPlayInitial);
  const [isAudioEnabled, setIsAudioEnabled] = useState<boolean>(true);
  const [isSpeaking, setIsSpeaking] = useState<boolean>(false);
  const [isFullscreen, setIsFullscreen] = useState<boolean>(false);
  const [playbackSpeed, setPlaybackSpeed] = useState<number>(1);

  const containerRef = useRef<HTMLDivElement>(null);
  const stepTimerRef = useRef<NodeJS.Timeout | null>(null);

  const currentStep: PathwayStep = pathway.steps[currentStepIndex] || pathway.steps[0];
  const totalSteps = pathway.steps.length;

  // Ses dinleyicisi
  useEffect(() => {
    const unsub = onSpeakingChange((speaking) => {
      setIsSpeaking(speaking);
    });
    return () => {
      unsub();
      stopSpeaking();
    };
  }, []);

  // Adım değiştiğinde seslendirmeyi başlat ve video modunda zamanlayıcı kur
  useEffect(() => {
    if (stepTimerRef.current) {
      clearTimeout(stepTimerRef.current);
      stepTimerRef.current = null;
    }

    if (isAudioEnabled && currentStep?.narration) {
      speak(currentStep.narration);
    }

    if (isPlaying) {
      // Kelime sayısına ve belirlenen durationSeconds'a göre süre
      const wordsCount = currentStep.narration ? currentStep.narration.split(/\s+/).length : 20;
      const calculatedDuration = Math.max(8, Math.ceil(wordsCount * 0.42));
      const baseDuration = currentStep.durationSeconds || calculatedDuration;
      const adjustedDurationMs = (baseDuration * 1000) / playbackSpeed;

      stepTimerRef.current = setTimeout(() => {
        handleNextStep();
      }, adjustedDurationMs);
    }

    return () => {
      if (stepTimerRef.current) clearTimeout(stepTimerRef.current);
    };
  }, [currentStepIndex, isPlaying, isAudioEnabled, playbackSpeed]);

  const handleNextStep = () => {
    if (currentStepIndex < totalSteps - 1) {
      setCurrentStepIndex((prev) => prev + 1);
    } else {
      setIsPlaying(false);
      stopSpeaking();
      onFinish?.();
    }
  };

  const handlePrevStep = () => {
    if (currentStepIndex > 0) {
      setCurrentStepIndex((prev) => prev - 1);
    }
  };

  const togglePlay = () => {
    if (isPlaying) {
      setIsPlaying(false);
      stopSpeaking();
      if (stepTimerRef.current) clearTimeout(stepTimerRef.current);
    } else {
      if (currentStepIndex === totalSteps - 1) {
        setCurrentStepIndex(0);
      }
      setIsPlaying(true);
    }
  };

  const toggleAudio = () => {
    if (isAudioEnabled) {
      stopSpeaking();
      setIsAudioEnabled(false);
    } else {
      setIsAudioEnabled(true);
      if (currentStep?.narration) {
        speak(currentStep.narration);
      }
    }
  };

  const handleReset = () => {
    stopSpeaking();
    if (stepTimerRef.current) clearTimeout(stepTimerRef.current);
    setCurrentStepIndex(0);
    setIsPlaying(false);
  };

  const toggleFullscreen = () => {
    if (!containerRef.current) return;
    if (!document.fullscreenElement) {
      containerRef.current.requestFullscreen().catch(() => {});
      setIsFullscreen(true);
    } else {
      document.exitFullscreen().catch(() => {});
      setIsFullscreen(false);
    }
  };

  const isNodeActive = (nodeId: string) => currentStep.activeNodeIds.includes(nodeId);

  // Şemaya göre özel kaskad renderı (Araşidonik Asit Yolağı)
  const isArachidonic = pathway.id.includes('arasidonik');
  const isApoptosis = pathway.id.includes('apoptoz');
  const isExtravasation = pathway.id.includes('lokosit');

  return (
    <div
      ref={containerRef}
      className={`relative flex flex-col rounded-2xl border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-900 text-slate-800 dark:text-slate-100 shadow-xl overflow-hidden transition-all duration-300 ${
        isFullscreen ? 'fixed inset-0 z-50 rounded-none w-screen h-screen' : ''
      } ${className}`}
    >
      {/* 1. ÜST ÇUBUK: Başlık, Disiplin, Ses ve Tam Ekran */}
      <div className="flex items-center justify-between px-5 py-3.5 border-b border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-900/90 backdrop-blur-sm">
        <div className="flex items-center gap-3">
          <div className="flex items-center justify-center w-9 h-9 rounded-xl bg-teal-500/10 text-teal-600 dark:text-teal-400">
            <Sparkles className="w-5 h-5 animate-spin-slow" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="font-bold text-sm sm:text-base text-slate-900 dark:text-white tracking-tight">
                {pathway.title}
              </h3>
              <span className="text-[11px] px-2 py-0.5 rounded-full font-medium bg-teal-100 dark:bg-teal-900/60 text-teal-800 dark:text-teal-300">
                {pathway.discipline}
              </span>
            </div>
            <p className="text-xs text-slate-500 dark:text-slate-400 line-clamp-1">{pathway.subtitle}</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {/* EMA Ses Butonu */}
          <button
            type="button"
            onClick={toggleAudio}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold transition-all ${
              isAudioEnabled
                ? 'bg-emerald-50 dark:bg-emerald-950/70 text-emerald-700 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800 shadow-sm'
                : 'bg-slate-100 dark:bg-slate-800 text-slate-500 border border-slate-200 dark:border-slate-700'
            }`}
            title={isAudioEnabled ? 'EMA Sesini Kapat' : 'EMA Sesini Aç'}
          >
            {isAudioEnabled ? (
              <>
                <Volume2 className={`w-4 h-4 ${isSpeaking ? 'animate-bounce text-emerald-500' : ''}`} />
                <span>EMA Anlatımı</span>
              </>
            ) : (
              <>
                <VolumeX className="w-4 h-4 text-slate-400" />
                <span>Sessiz</span>
              </>
            )}
          </button>

          {/* Tam Ekran Butonu */}
          <button
            type="button"
            onClick={toggleFullscreen}
            className="p-2 rounded-xl text-slate-500 hover:text-slate-800 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            title={isFullscreen ? 'Tam Ekrandan Çık' : 'Tam Ekran Görünümü'}
          >
            {isFullscreen ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* 2. DİNAMİK VE FERAH GÖRSELLEŞTİRME ALANI (ASLA İÇ İÇE GEÇMEYEN KASKAD AKIŞI) */}
      <div className="p-4 sm:p-6 overflow-x-auto overflow-y-auto max-h-[580px] bg-gradient-to-b from-slate-100/60 via-white to-slate-50 dark:from-slate-950 dark:via-slate-900 dark:to-slate-950">
        <div className="min-w-[700px] flex flex-col gap-6">

          {/* === SENARYO A: ARAŞİDONİK ASİT VE EİKOZANOİD YOLAĞI === */}
          {isArachidonic && (
            <div className="flex flex-col gap-5">
              {/* Seviye 1: Membran Fosfolipidleri */}
              <div className="flex items-center justify-center">
                <div
                  className={`w-full max-w-xl p-3.5 rounded-2xl border-2 text-center transition-all duration-500 ${
                    isNodeActive('membrane_phospholipids')
                      ? 'border-sky-500 bg-sky-50 dark:bg-sky-950/80 shadow-lg ring-4 ring-sky-400/30 scale-102'
                      : 'border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 opacity-50'
                  }`}
                >
                  <span className="text-[10px] font-bold uppercase tracking-wider text-sky-600 dark:text-sky-400">
                    Membran Çift Katmanı
                  </span>
                  <div className="text-sm font-bold text-slate-800 dark:text-white">Membran Fosfolipidleri</div>
                  <div className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                    Hücre hasarı veya mediyatörlerle (Bradikinin, Trombin) uyarılır
                  </div>
                </div>
              </div>

              {/* Ok: Fosfolipaz A2 ve İnhibitörler */}
              <div className="flex items-center justify-center gap-4 my-1">
                <div className="flex flex-col items-center">
                  <ArrowDown className={`w-5 h-5 ${isNodeActive('pla2') ? 'text-teal-600 animate-bounce' : 'text-slate-300'}`} />
                  <div
                    className={`px-4 py-2 rounded-xl border-2 text-xs font-bold transition-all duration-500 ${
                      isNodeActive('pla2')
                        ? 'border-amber-500 bg-amber-50 dark:bg-amber-950/80 text-amber-900 dark:text-amber-100 shadow-md ring-2 ring-amber-400/50'
                        : 'border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 opacity-50'
                    }`}
                  >
                    Fosfolipaz A₂ (PLA₂) [Hız Kısıtlayıcı Enzim]
                  </div>
                </div>

                {/* İnhibitör: Kortikosteroidler */}
                <div
                  className={`px-3 py-2 rounded-xl border-2 text-xs font-semibold transition-all duration-500 flex items-center gap-2 ${
                    isNodeActive('corticosteroids')
                      ? 'border-rose-500 bg-rose-50 dark:bg-rose-950/80 text-rose-900 dark:text-rose-100 shadow-lg ring-4 ring-rose-400/40 animate-pulse'
                      : 'border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 opacity-50'
                  }`}
                >
                  <span className="w-5 h-5 rounded-full bg-rose-500 text-white flex items-center justify-center font-bold text-xs">⊣</span>
                  <div>
                    <div className="font-bold">Kortikosteroidler</div>
                    <div className="text-[10px] text-rose-600 dark:text-rose-400">Lipokortin (Anneksin-1) senteziyle PLA₂'yi bloke eder</div>
                  </div>
                </div>
              </div>

              {/* Seviye 2: Merkezi Kavşak - Serbest Araşidonik Asit */}
              <div className="flex items-center justify-center">
                <div
                  className={`w-full max-w-md p-3.5 rounded-2xl border-2 text-center transition-all duration-500 ${
                    isNodeActive('arachidonic_acid')
                      ? 'border-teal-500 bg-teal-50 dark:bg-teal-950/80 shadow-xl ring-4 ring-teal-400/40 scale-102'
                      : 'border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 opacity-50'
                  }`}
                >
                  <span className="text-[10px] font-bold uppercase tracking-wider text-teal-600 dark:text-teal-400">
                    Merkezi Eikozanoid Öncülü
                  </span>
                  <div className="text-base font-extrabold text-teal-950 dark:text-teal-100">ARAŞİDONİK ASİT (20 Karbonlu)</div>
                  <div className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                    İki ana enzimatik yolağa (5-LOX ve COX) ayrılarak ilerler
                  </div>
                </div>
              </div>

              {/* Seviye 3: Dallanma - Sol Dal (5-LOX) vs Sağ Dal (COX) */}
              <div className="grid grid-cols-2 gap-6 mt-2">
                {/* SOL SÜTUN: 5-LİPOOKSİJENAZ KOLU */}
                <div className="flex flex-col gap-3.5 p-4 rounded-2xl bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800">
                  <div className="flex items-center justify-between pb-2 border-b border-slate-100 dark:border-slate-800">
                    <span className="font-bold text-xs text-indigo-600 dark:text-indigo-400 uppercase tracking-wide">
                      Sol Kol: 5-Lipooksijenaz Yolağı
                    </span>
                    <span className="text-[10px] text-slate-400">Lökosit / Mast Hücresi</span>
                  </div>

                  {/* Enzim ve İnhibitör */}
                  <div className="flex items-center justify-between gap-2">
                    <div
                      className={`flex-1 p-2.5 rounded-xl border-2 text-xs font-bold transition-all duration-500 ${
                        isNodeActive('lox_enzyme')
                          ? 'border-indigo-500 bg-indigo-50 dark:bg-indigo-950 text-indigo-900 dark:text-indigo-100 shadow-md ring-2 ring-indigo-400/50'
                          : 'border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50 opacity-50'
                      }`}
                    >
                      5-Lipooksijenaz (5-LOX)
                    </div>
                    <div
                      className={`p-2 rounded-xl border-2 text-[11px] font-semibold transition-all duration-500 flex items-center gap-1.5 ${
                        isNodeActive('zileuton')
                          ? 'border-rose-500 bg-rose-50 dark:bg-rose-950 text-rose-900 dark:text-rose-100 shadow-md ring-2 ring-rose-400/50 animate-pulse'
                          : 'border-slate-200 dark:border-slate-800 opacity-50'
                      }`}
                    >
                      <span className="text-rose-600 font-bold">⊣</span> Zileuton (5-LOX İnhibitörü)
                    </div>
                  </div>

                  <div className="flex justify-center">
                    <ArrowDown className="w-4 h-4 text-slate-300" />
                  </div>

                  {/* Lökotriyenler ve Reseptör Blokörleri */}
                  <div
                    className={`p-3 rounded-xl border-2 transition-all duration-500 ${
                      isNodeActive('leukotrienes')
                        ? 'border-indigo-500 bg-indigo-50/80 dark:bg-indigo-950/80 shadow-md ring-2 ring-indigo-400/40'
                        : 'border-slate-200 dark:border-slate-800 opacity-50'
                    }`}
                  >
                    <div className="font-bold text-xs text-indigo-950 dark:text-indigo-200">
                      Lökotriyenler (LTB₄, LTC₄, LTD₄, LTE₄)
                    </div>
                    <div className="text-[11px] text-slate-600 dark:text-slate-300 mt-1 space-y-0.5">
                      <div>• <strong>LTB₄:</strong> Güçlü nötrofil kemotaksisi</div>
                      <div>• <strong>LTC₄, LTD₄, LTE₄:</strong> Bronkokonstriksiyon ve damar geçirgenliği</div>
                    </div>
                  </div>

                  <div
                    className={`p-2 rounded-xl border-2 text-[11px] font-semibold transition-all duration-500 flex items-center gap-1.5 ${
                      isNodeActive('leukotriene_antagonists')
                        ? 'border-rose-500 bg-rose-50 dark:bg-rose-950 text-rose-900 dark:text-rose-100 shadow-md ring-2 ring-rose-400/50'
                        : 'border-slate-200 dark:border-slate-800 opacity-50'
                    }`}
                  >
                    <span className="text-rose-600 font-bold">⊣</span> Montelukast / Zafirlukast (CysLT₁ Reseptör Blokajı)
                  </div>
                </div>

                {/* SAĞ SÜTUN: SİKLOOKSİJENAZ KOLU */}
                <div className="flex flex-col gap-3.5 p-4 rounded-2xl bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800">
                  <div className="flex items-center justify-between pb-2 border-b border-slate-100 dark:border-slate-800">
                    <span className="font-bold text-xs text-teal-600 dark:text-teal-400 uppercase tracking-wide">
                      Sağ Kol: Siklooksijenaz Yolağı
                    </span>
                    <span className="text-[10px] text-slate-400">Trombosit / Endotel / Çevre Doku</span>
                  </div>

                  {/* Enzim ve İlaçlar */}
                  <div className="flex flex-col gap-2">
                    <div
                      className={`p-2.5 rounded-xl border-2 text-xs font-bold transition-all duration-500 flex items-center justify-between ${
                        isNodeActive('cox_enzyme')
                          ? 'border-teal-500 bg-teal-50 dark:bg-teal-950 text-teal-900 dark:text-teal-100 shadow-md ring-2 ring-teal-400/50'
                          : 'border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50 opacity-50'
                      }`}
                    >
                      <span>Siklooksijenaz (COX-1 ve COX-2)</span>
                    </div>

                    <div className="grid grid-cols-2 gap-2">
                      <div
                        className={`p-2 rounded-xl border-2 text-[11px] font-semibold transition-all duration-500 flex items-center gap-1 ${
                          isNodeActive('nsaids')
                            ? 'border-rose-500 bg-rose-50 dark:bg-rose-950 text-rose-900 dark:text-rose-100 shadow-md ring-2 ring-rose-400/50 animate-pulse'
                            : 'border-slate-200 dark:border-slate-800 opacity-50'
                        }`}
                      >
                        <span className="text-rose-600 font-bold">⊣</span> Aspirin / Non-selektif NSAİİ
                      </div>
                      <div
                        className={`p-2 rounded-xl border-2 text-[11px] font-semibold transition-all duration-500 flex items-center gap-1 ${
                          isNodeActive('cox2_inhibitors')
                            ? 'border-rose-500 bg-rose-50 dark:bg-rose-950 text-rose-900 dark:text-rose-100 shadow-md ring-2 ring-rose-400/50 animate-pulse'
                            : 'border-slate-200 dark:border-slate-800 opacity-50'
                        }`}
                      >
                        <span className="text-rose-600 font-bold">⊣</span> Selekoksib (Selektif COX-2)
                      </div>
                    </div>
                  </div>

                  <div className="flex justify-center">
                    <ArrowDown className="w-4 h-4 text-slate-300" />
                  </div>

                  {/* Terminal Eikozanoidler (Üçlü Terazi) */}
                  <div className="grid grid-cols-3 gap-2">
                    <div
                      className={`p-2.5 rounded-xl border-2 text-center transition-all duration-500 ${
                        isNodeActive('prostacyclin')
                          ? 'border-emerald-500 bg-emerald-50 dark:bg-emerald-950 text-emerald-900 dark:text-emerald-100 shadow-md ring-2 ring-emerald-400/50'
                          : 'border-slate-200 dark:border-slate-800 opacity-50'
                      }`}
                    >
                      <div className="font-bold text-xs">PGI₂ (Prostasiklin)</div>
                      <div className="text-[10px] text-emerald-700 dark:text-emerald-400 mt-1">
                        Endotel • Vazodilatasyon & Agregasyon İnhibisyonu
                      </div>
                    </div>

                    <div
                      className={`p-2.5 rounded-xl border-2 text-center transition-all duration-500 ${
                        isNodeActive('prostaglandins')
                          ? 'border-teal-500 bg-teal-50 dark:bg-teal-950 text-teal-900 dark:text-teal-100 shadow-md ring-2 ring-teal-400/50'
                          : 'border-slate-200 dark:border-slate-800 opacity-50'
                      }`}
                    >
                      <div className="font-bold text-xs">PGE₂ / PGD₂</div>
                      <div className="text-[10px] text-teal-700 dark:text-teal-400 mt-1">
                        Ateş • Ağrı Duyarlılığı • Vazodilatasyon
                      </div>
                    </div>

                    <div
                      className={`p-2.5 rounded-xl border-2 text-center transition-all duration-500 ${
                        isNodeActive('thromboxane')
                          ? 'border-rose-500 bg-rose-50 dark:bg-rose-950 text-rose-900 dark:text-rose-100 shadow-md ring-2 ring-rose-400/50'
                          : 'border-slate-200 dark:border-slate-800 opacity-50'
                      }`}
                    >
                      <div className="font-bold text-xs">TXA₂ (Tromboksan)</div>
                      <div className="text-[10px] text-rose-700 dark:text-rose-400 mt-1">
                        Trombosit • Vazokonstriksiyon & Agregasyon
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* === SENARYO B: APOPTOZ KASKADI (İntrinsik vs Ekstrinsik) === */}
          {isApoptosis && (
            <div className="flex flex-col gap-5">
              <div className="grid grid-cols-2 gap-6">
                {/* Sol Kol: İntrinsik Mitokondriyal */}
                <div className="flex flex-col gap-3 p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
                  <span className="font-bold text-xs text-sky-600 dark:text-sky-400 uppercase">
                    1. İntrinsik (Mitokondriyal) Yolak
                  </span>
                  <div className={`p-3 rounded-xl border-2 transition-all ${isNodeActive('dna_damage') ? 'border-sky-500 bg-sky-50 dark:bg-sky-950 shadow-md' : 'opacity-50'}`}>
                    <div className="font-bold text-xs">DNA Hasarı & Sitotoksik Stres (p53)</div>
                  </div>
                  <div className="flex justify-center"><ArrowDown className="w-4 h-4 text-slate-300" /></div>
                  <div className={`p-3 rounded-xl border-2 transition-all flex items-center justify-between ${isNodeActive('bax_bak') ? 'border-amber-500 bg-amber-50 dark:bg-amber-950 shadow-md' : 'opacity-50'}`}>
                    <div>
                      <div className="font-bold text-xs">Bax & Bak Porları (Pro-apoptotik)</div>
                      <div className="text-[10px] text-slate-500">Mitokondri dış zar geçirgenliği</div>
                    </div>
                    <span className="text-[11px] font-semibold text-rose-600">⊣ Bcl-2/Bcl-xL</span>
                  </div>
                  <div className="flex justify-center"><ArrowDown className="w-4 h-4 text-slate-300" /></div>
                  <div className={`p-3 rounded-xl border-2 transition-all ${isNodeActive('cytochrome_c') || isNodeActive('apaf1') ? 'border-teal-500 bg-teal-50 dark:bg-teal-950 shadow-md' : 'opacity-50'}`}>
                    <div className="font-bold text-xs">Sitokrom c Salınımı & Apaf-1 (Apoptozom)</div>
                  </div>
                  <div className="flex justify-center"><ArrowDown className="w-4 h-4 text-slate-300" /></div>
                  <div className={`p-3 rounded-xl border-2 text-center transition-all ${isNodeActive('caspase9') ? 'border-indigo-500 bg-indigo-50 dark:bg-indigo-950 shadow-md ring-2 ring-indigo-400' : 'opacity-50'}`}>
                    <div className="font-bold text-xs text-indigo-700 dark:text-indigo-300">Başlatıcı Kaspaz-9 Aktivasyonu</div>
                  </div>
                </div>

                {/* Sağ Kol: Ekstrinsik Ölüm Reseptörü */}
                <div className="flex flex-col gap-3 p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
                  <span className="font-bold text-xs text-rose-600 dark:text-rose-400 uppercase">
                    2. Ekstrinsik (Ölüm Reseptörü) Yolağı
                  </span>
                  <div className={`p-3 rounded-xl border-2 transition-all ${isNodeActive('death_ligands') ? 'border-rose-500 bg-rose-50 dark:bg-rose-950 shadow-md' : 'opacity-50'}`}>
                    <div className="font-bold text-xs">FasL / TNF-alfa Ölüm Ligandları</div>
                  </div>
                  <div className="flex justify-center"><ArrowDown className="w-4 h-4 text-slate-300" /></div>
                  <div className={`p-3 rounded-xl border-2 transition-all ${isNodeActive('fas_receptor') ? 'border-rose-500 bg-rose-50 dark:bg-rose-950 shadow-md' : 'opacity-50'}`}>
                    <div className="font-bold text-xs">Fas (CD95) & FADD Adaptör Kompleksi (DISC)</div>
                  </div>
                  <div className="flex justify-center"><ArrowDown className="w-4 h-4 text-slate-300" /></div>
                  <div className={`p-3 rounded-xl border-2 text-center transition-all ${isNodeActive('caspase8') ? 'border-indigo-500 bg-indigo-50 dark:bg-indigo-950 shadow-md ring-2 ring-indigo-400' : 'opacity-50'}`}>
                    <div className="font-bold text-xs text-indigo-700 dark:text-indigo-300">Başlatıcı Kaspaz-8 Aktivasyonu</div>
                  </div>
                </div>
              </div>

              {/* Ortak Yürütücü Yol */}
              <div className="flex flex-col items-center justify-center gap-2 mt-1">
                <ArrowDown className="w-6 h-6 text-indigo-500 animate-bounce" />
                <div
                  className={`w-full max-w-xl p-4 rounded-2xl border-2 text-center transition-all ${
                    isNodeActive('caspase3') || isNodeActive('apoptotic_bodies')
                      ? 'border-indigo-600 bg-indigo-50 dark:bg-indigo-950 shadow-xl ring-4 ring-indigo-400/40'
                      : 'border-slate-200 dark:border-slate-800 opacity-50'
                  }`}
                >
                  <div className="font-extrabold text-sm text-indigo-950 dark:text-indigo-100">
                    ORTAK YÜRÜTÜCÜ: KASPAZ-3 VE KASPAZ-6 AKTİVASYONU
                  </div>
                  <div className="text-xs text-slate-600 dark:text-slate-300 mt-1">
                    CAD Enzimi Aktivasyonu ➔ DNA Parçalanması ➔ Apopitotik Cisimcikler (İnflamasyonsuz Temizlenme)
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* === SENARYO C: LÖKOSİT EKSTRAVAZASYONU VE ADEZYON === */}
          {isExtravasation && (
            <div className="flex flex-col gap-4">
              <div className="grid grid-cols-5 gap-3">
                {[
                  { id: 'stasis', step: 1, title: '1. Marjinasyon', desc: 'Vazodilatasyon ve kan akımının yavaşlaması' },
                  { id: 'selectins', step: 2, title: '2. Yuvarlanma', desc: 'P & E-Selektin ve Sialyl-Lewis X' },
                  { id: 'integrins', step: 3, title: '3. Sıkı Adezyon', desc: 'LFA-1, Mac-1 ve ICAM-1 kenetlenmesi' },
                  { id: 'pecam1', step: 4, title: '4. Diapedez', desc: 'PECAM-1 (CD31) aracılı dokuya geçiş' },
                  { id: 'chemotaxis', step: 5, title: '5. Kemotaksis', desc: 'C5a, LTB₄, IL-8 ile fagositoz' },
                ].map((item) => (
                  <div
                    key={item.id}
                    className={`p-3 rounded-2xl border-2 flex flex-col justify-between transition-all duration-500 ${
                      isNodeActive(item.id)
                        ? 'border-teal-500 bg-teal-50 dark:bg-teal-950 shadow-lg ring-4 ring-teal-400/40 scale-102'
                        : 'border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 opacity-50'
                    }`}
                  >
                    <div>
                      <span className="text-[10px] font-bold text-teal-600 dark:text-teal-400 uppercase">Adım {item.step}</span>
                      <div className="font-bold text-xs text-slate-900 dark:text-white mt-0.5">{item.title}</div>
                    </div>
                    <div className="text-[11px] text-slate-500 dark:text-slate-400 mt-2">{item.desc}</div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* === GENEL DİNAMİK / DİĞER MEKANİZMALAR (GENEL LİSTE) === */}
          {!isArachidonic && !isApoptosis && !isExtravasation && (
            <div className="flex flex-col gap-3">
              {pathway.nodes.map((node) => (
                <div
                  key={node.id}
                  className={`p-3 rounded-xl border-2 transition-all ${
                    isNodeActive(node.id)
                      ? 'border-teal-500 bg-teal-50 dark:bg-teal-950 shadow-md ring-2 ring-teal-400'
                      : 'border-slate-200 dark:border-slate-800 opacity-50'
                  }`}
                >
                  <div className="font-bold text-xs">{node.label}</div>
                  {node.sublabel && <div className="text-[11px] text-slate-500">{node.sublabel}</div>}
                </div>
              ))}
            </div>
          )}

        </div>
      </div>

      {/* 3. AŞAMA AÇIKLAMASI & SINAV SPOTU (SENKRON ANLATIM PANELI) */}
      <div className="p-4 sm:p-5 border-t border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900">
        <div className="flex items-center justify-between mb-1.5">
          <div className="flex items-center gap-2">
            <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-teal-600 text-white font-bold text-xs">
              {currentStep.stepNumber}
            </span>
            <h4 className="font-bold text-sm sm:text-base text-slate-900 dark:text-white">
              {currentStep.title}
            </h4>
          </div>
          <div className="text-xs font-semibold text-slate-400">
            Aşama {currentStepIndex + 1} / {totalSteps}
          </div>
        </div>

        {currentStep.subtitle && (
          <p className="text-xs font-medium text-teal-600 dark:text-teal-400 mb-2 ml-8">
            {currentStep.subtitle}
          </p>
        )}

        {/* Adım Açıklaması */}
        <div className="text-xs sm:text-sm text-slate-600 dark:text-slate-300 space-y-1 ml-8 leading-relaxed">
          {currentStep.description.split('\n').map((line, idx) => {
            const clean = line.trim();
            if (!clean) return null;
            return (
              <div key={idx} className="flex items-start gap-2">
                <div className="w-1.5 h-1.5 rounded-full bg-teal-500 mt-1.5 shrink-0" />
                <span dangerouslySetInnerHTML={{ __html: clean.replace(/^- \*\*(.*?)\*\*:/, '<strong>$1:</strong>') }} />
              </div>
            );
          })}
        </div>

        {/* Sınav Spotu */}
        {currentStep.spotlight && (
          <div className="mt-3 ml-8 p-3 rounded-xl bg-amber-50/90 dark:bg-amber-950/40 border border-amber-300 dark:border-amber-800/80 text-amber-900 dark:text-amber-200 text-xs flex items-start gap-2">
            <AlertCircle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
            <span className="font-semibold leading-relaxed">{currentStep.spotlight}</span>
          </div>
        )}
      </div>

      {/* 4. VİDEO KONTROL ÇUBUĞU (SCRUBBER, OYNAT, HIZ) */}
      <div className="px-5 py-3 border-t border-slate-200 dark:border-slate-800 bg-slate-100/80 dark:bg-slate-950 flex flex-col gap-2">
        {/* Scrubber Çizgisi */}
        <div className="flex items-center gap-2 w-full">
          {pathway.steps.map((step, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => {
                setCurrentStepIndex(idx);
                setIsPlaying(false);
              }}
              className={`h-2 flex-1 rounded-full transition-all duration-300 ${
                idx === currentStepIndex
                  ? 'bg-teal-500 ring-2 ring-teal-400/60 scale-y-125'
                  : idx < currentStepIndex
                  ? 'bg-teal-300 dark:bg-teal-800'
                  : 'bg-slate-300 dark:bg-slate-800'
              }`}
              title={`Aşama ${idx + 1}: ${step.title}`}
            />
          ))}
        </div>

        {/* Kontrol Butonları */}
        <div className="flex items-center justify-between pt-1">
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={handleReset}
              className="p-2 rounded-xl text-slate-500 hover:text-slate-800 dark:hover:text-slate-200 hover:bg-slate-200 dark:hover:bg-slate-800 transition-colors"
              title="Başa Dön"
            >
              <RotateCcw className="w-4 h-4" />
            </button>

            <button
              type="button"
              onClick={handlePrevStep}
              disabled={currentStepIndex === 0}
              className="p-2 rounded-xl text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-800 disabled:opacity-30 disabled:pointer-events-none transition-colors"
              title="Önceki Aşama"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>

            <button
              type="button"
              onClick={togglePlay}
              className="flex items-center justify-center w-10 h-10 rounded-full bg-teal-600 hover:bg-teal-700 text-white shadow-lg shadow-teal-600/30 hover:scale-105 active:scale-95 transition-all"
              title={isPlaying ? 'Durdur' : 'Oynat (Video Modu)'}
            >
              {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4 ml-0.5" />}
            </button>

            <button
              type="button"
              onClick={handleNextStep}
              disabled={currentStepIndex === totalSteps - 1}
              className="p-2 rounded-xl text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-800 disabled:opacity-30 disabled:pointer-events-none transition-colors"
              title="Sonraki Aşama"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>

          {/* Oynatma Hızı */}
          <div className="flex items-center gap-2 text-xs">
            <button
              type="button"
              onClick={() => {
                const speeds = [0.8, 1, 1.25, 1.5];
                const nextIdx = (speeds.indexOf(playbackSpeed) + 1) % speeds.length;
                setPlaybackSpeed(speeds[nextIdx]);
              }}
              className="px-2.5 py-1 rounded-lg bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-mono font-semibold hover:bg-slate-300 dark:hover:bg-slate-700 transition-colors"
              title="Oynatma Hızı"
            >
              {playbackSpeed}x
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
