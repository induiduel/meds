import React, { useEffect } from 'react';
import { X, Sparkles } from 'lucide-react';
import type { MechanismPathway } from '../../../types/pathway';
import { AnimatedPathwayPlayer } from './AnimatedPathwayPlayer';

interface MechanismVideoModalProps {
  pathway: MechanismPathway | null;
  isOpen: boolean;
  onClose: () => void;
}

export const MechanismVideoModal: React.FC<MechanismVideoModalProps> = ({ pathway, isOpen, onClose }) => {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen || !pathway) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-2 sm:p-4 bg-slate-950/80 backdrop-blur-md animate-fadeIn">
      {/* Modal Kutusu */}
      <div className="relative w-full max-w-5xl max-h-[96vh] flex flex-col bg-white dark:bg-slate-900 rounded-2xl shadow-2xl border border-slate-200 dark:border-slate-800 overflow-hidden">
        {/* Kapat Butonu */}
        <button
          type="button"
          onClick={onClose}
          className="absolute top-3 right-3 z-30 p-2 rounded-xl bg-slate-100/80 hover:bg-slate-200 dark:bg-slate-800/80 dark:hover:bg-slate-700 text-slate-500 hover:text-slate-800 dark:text-slate-400 dark:hover:text-slate-100 transition-colors shadow-sm"
          title="Kapat (ESC)"
        >
          <X className="w-5 h-5" />
        </button>

        {/* İçerik: Animasyonlu Yolak Oynatıcı */}
        <div className="flex-1 overflow-y-auto">
          <AnimatedPathwayPlayer
            pathway={pathway}
            autoPlayInitial={true}
            className="border-none shadow-none rounded-none"
          />
        </div>
      </div>
    </div>
  );
};
