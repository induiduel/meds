import React, { useEffect, useState } from 'react';
import { ArrowUp, BookOpen, FileText, Maximize2, Minimize2, Plus } from 'lucide-react';

interface LearnFabProps {
  children: React.ReactNode;
  onOpenGlossary: () => void;
  onOpenPdf: () => void;
}

/** Öğrenme ekranı kabuğu: mobilde tam ekran modu ve yüzen eylem düğmesi. */
export const LearnFab: React.FC<LearnFabProps> = ({ children, onOpenGlossary, onOpenPdf }) => {
  const [full, setFull] = useState(false);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const onFs = () => { if (!document.fullscreenElement) setFull(false); };
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') { setOpen(false); } };
    document.addEventListener('fullscreenchange', onFs);
    window.addEventListener('keydown', onKey);
    return () => { document.removeEventListener('fullscreenchange', onFs); window.removeEventListener('keydown', onKey); };
  }, []);

  useEffect(() => {
    document.documentElement.classList.toggle('learn-full', full);
    return () => document.documentElement.classList.remove('learn-full');
  }, [full]);

  const toggleFull = async () => {
    const next = !full;
    setFull(next);
    setOpen(false);
    try {
      if (next && !document.fullscreenElement) await document.documentElement.requestFullscreen?.();
      if (!next && document.fullscreenElement) await document.exitFullscreen?.();
    } catch { /* iOS Safari: yalnızca CSS tam ekranı */ }
  };

  const scrollTop = () => {
    setOpen(false);
    const box = document.querySelector('.ms-learn-full');
    (box ?? window).scrollTo({ top: 0, behavior: 'smooth' });
  };

  const run = (fn: () => void) => () => { setOpen(false); fn(); };

  const items = [
    { label: full ? 'Tam ekrandan çık' : 'Tam ekran', icon: full ? Minimize2 : Maximize2, onClick: toggleFull },
    { label: 'Başa dön', icon: ArrowUp, onClick: scrollTop },
    { label: 'Sözlük', icon: BookOpen, onClick: run(onOpenGlossary) },
    { label: 'PDF', icon: FileText, onClick: run(onOpenPdf) },
  ];

  return (
    <div className={full ? 'ms-learn-full' : ''}>
      {children}
      {open && <div className="ms-fab-scrim md:hidden" onClick={() => setOpen(false)} />}
      <div className="ms-fab-wrap md:hidden" style={{ ['--fab-offset' as string]: full ? '0px' : '68px' }}>
        {open && items.slice().reverse().map((it, i) => (
          <button key={it.label} type="button" className="ms-fab-item" style={{ animationDelay: `${i * 35}ms` }} onClick={it.onClick}>
            <it.icon className="w-[18px] h-[18px] text-accent" />
            {it.label}
          </button>
        ))}
        <button
          type="button"
          className={`ms-fab ${open ? 'is-open' : ''}`}
          aria-label={open ? 'Menüyü kapat' : 'Hızlı eylemler'}
          aria-expanded={open}
          onClick={() => setOpen(o => !o)}
        >
          <Plus className="w-6 h-6" strokeWidth={2.2} />
        </button>
      </div>
    </div>
  );
};
