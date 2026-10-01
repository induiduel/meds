import React, { useState } from 'react';
import { 
  PlusCircle, 
  BookOpen, 
  Layers, 
  Trophy, 
  BookMarked, 
  MoreHorizontal,
  Brain,
  Printer,
  Cloud,
  ShieldCheck,
  X
} from 'lucide-react';
import { AppUser } from '../services/auth';

interface MobileBottomNavProps {
  activeTab: 'quick_add' | 'questions' | 'matrix' | 'leaderboard' | 'notes' | 'practice' | 'booklet';
  setActiveTab: (tab: 'quick_add' | 'questions' | 'matrix' | 'leaderboard' | 'notes' | 'practice' | 'booklet') => void;
  questionsCount: number;
  isAdmin: boolean;
  onOpenContributeModal: () => void;
  onOpenPdfModal: () => void;
  onOpenAdminPanel: () => void;
  onUploadToDrive: () => void;
}

export const MobileBottomNav: React.FC<MobileBottomNavProps> = ({
  activeTab,
  setActiveTab,
  questionsCount,
  isAdmin,
  onOpenContributeModal,
  onOpenPdfModal,
  onOpenAdminPanel,
  onUploadToDrive,
}) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const mainNavItems = [
    {
      id: 'quick_add' as const,
      label: 'Hızlı Ekle',
      icon: PlusCircle,
      badge: null,
    },
    {
      id: 'questions' as const,
      label: 'Sorular',
      icon: BookOpen,
      badge: questionsCount > 0 ? questionsCount : null,
    },
    {
      id: 'matrix' as const,
      label: 'Matris',
      icon: Layers,
      badge: null,
    },
    {
      id: 'leaderboard' as const,
      label: 'Sıralama',
      icon: Trophy,
      badge: null,
    },
    {
      id: 'notes' as const,
      label: 'Notlar',
      icon: BookMarked,
      badge: null,
    },
  ];

  return (
    <>
      {/* Mobile More Options Sheet */}
      {isMenuOpen && (
        <div 
          className="sm:hidden fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex flex-col justify-end"
          onClick={() => setIsMenuOpen(false)}
        >
          <div 
            className="bg-white rounded-t-2xl p-4 space-y-3 border-t border-slate-200 animate-slideUp shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between pb-2 border-b border-slate-100">
              <h4 className="font-bold text-xs text-slate-800 uppercase tracking-wider">
                Daha Fazla Seçenek
              </h4>
              <button
                onClick={() => setIsMenuOpen(false)}
                className="p-1 rounded-lg text-slate-400 hover:text-slate-700"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="grid grid-cols-2 gap-2 text-xs">
              <button
                onClick={() => {
                  setActiveTab('practice');
                  setIsMenuOpen(false);
                }}
                className={`p-3 rounded-xl border flex flex-col items-center gap-1.5 text-center font-bold transition-all ${
                  activeTab === 'practice'
                    ? 'bg-teal-50 border-teal-300 text-teal-800'
                    : 'bg-slate-50 border-slate-200 text-slate-700'
                }`}
              >
                <Brain className="w-5 h-5 text-teal-600" />
                <span>Test Çöz Modu</span>
              </button>

              <button
                onClick={() => {
                  setActiveTab('booklet');
                  setIsMenuOpen(false);
                }}
                className={`p-3 rounded-xl border flex flex-col items-center gap-1.5 text-center font-bold transition-all ${
                  activeTab === 'booklet'
                    ? 'bg-teal-50 border-teal-300 text-teal-800'
                    : 'bg-slate-50 border-slate-200 text-slate-700'
                }`}
              >
                <Printer className="w-5 h-5 text-teal-600" />
                <span>Kitapçık Görünümü</span>
              </button>

              <button
                onClick={() => {
                  setIsMenuOpen(false);
                  onOpenPdfModal();
                }}
                className="p-3 rounded-xl border border-slate-200 bg-slate-50 flex flex-col items-center gap-1.5 text-center font-bold text-slate-700"
              >
                <Printer className="w-5 h-5 text-emerald-600" />
                <span>A4 PDF İndir</span>
              </button>

              <button
                onClick={() => {
                  setIsMenuOpen(false);
                  onOpenContributeModal();
                }}
                className="p-3 rounded-xl border border-teal-200 bg-teal-50 flex flex-col items-center gap-1.5 text-center font-bold text-teal-900"
              >
                <PlusCircle className="w-5 h-5 text-teal-600" />
                <span>Soru Hatırla & Ekle</span>
              </button>

              <button
                onClick={() => {
                  setIsMenuOpen(false);
                  onOpenAdminPanel();
                }}
                className={`col-span-2 p-3 rounded-xl border flex items-center justify-center gap-2 font-bold text-xs cursor-pointer transition-all active:scale-95 ${
                  isAdmin
                    ? 'border-amber-400 bg-amber-400 text-slate-950 font-black ring-1 ring-amber-500'
                    : 'border-slate-800 bg-slate-900 text-amber-300'
                }`}
              >
                <ShieldCheck className={`w-4 h-4 ${isAdmin ? 'text-slate-950' : 'text-amber-400'}`} />
                <span>{isAdmin ? 'Yönetici & Otomasyon Paneli' : 'Admin Paneli Girişi'}</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Sticky Bottom Navigation Bar */}
      <nav 
        aria-label="Mobil Gezinme Çubuğu"
        className="sm:hidden fixed bottom-0 left-0 right-0 z-40 bg-white/95 backdrop-blur-md border-t border-slate-200/90 py-1 px-1.5 flex items-center justify-around shadow-lg safe-area-pb"
      >
        {mainNavItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => {
                setActiveTab(item.id);
                setIsMenuOpen(false);
              }}
              className={`flex-1 flex flex-col items-center justify-center py-1 px-1 rounded-xl transition-all cursor-pointer relative ${
                isActive
                  ? 'text-teal-700 font-bold'
                  : 'text-slate-500 hover:text-slate-800 font-medium'
              }`}
            >
              <div className="relative">
                <Icon className={`w-5 h-5 transition-transform ${isActive ? 'scale-110 text-teal-600' : ''}`} />
                {item.badge !== null && (
                  <span className="absolute -top-1.5 -right-2 bg-teal-600 text-white text-[9px] font-bold px-1 rounded-full min-w-[15px] h-[15px] flex items-center justify-center">
                    {item.badge}
                  </span>
                )}
              </div>
              <span className={`text-[10px] mt-0.5 tracking-tight ${isActive ? 'font-bold' : ''}`}>
                {item.label}
              </span>
              {isActive && (
                <span className="w-1 h-1 rounded-full bg-teal-600 mt-0.5"></span>
              )}
            </button>
          );
        })}

        {/* More Options Button */}
        <button
          onClick={() => setIsMenuOpen(!isMenuOpen)}
          className={`flex-1 flex flex-col items-center justify-center py-1 px-1 rounded-xl transition-all cursor-pointer ${
            isMenuOpen || activeTab === 'practice' || activeTab === 'booklet'
              ? 'text-teal-700 font-bold'
              : 'text-slate-500 hover:text-slate-800 font-medium'
          }`}
        >
          <MoreHorizontal className="w-5 h-5" />
          <span className="text-[10px] mt-0.5 tracking-tight">Fazlası</span>
        </button>
      </nav>
    </>
  );
};
