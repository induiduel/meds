import React, { useState, useRef, useEffect } from 'react';
import { Info, X } from 'lucide-react';

interface InfoPopoverProps {
  title: string;
  children: React.ReactNode;
  buttonLabel?: string;
  badgeText?: string;
  className?: string;
  buttonClassName?: string;
  iconClassName?: string;
  align?: 'left' | 'right' | 'center';
}

export const InfoPopover: React.FC<InfoPopoverProps> = ({
  title,
  children,
  buttonLabel,
  badgeText,
  className = '',
  buttonClassName = '',
  iconClassName = 'w-4 h-4',
  align = 'left',
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const popoverRef = useRef<HTMLDivElement>(null);
  const buttonRef = useRef<HTMLButtonElement>(null);

  // Close on outside click
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (
        popoverRef.current &&
        !popoverRef.current.contains(event.target as Node) &&
        buttonRef.current &&
        !buttonRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
      }
    }

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  const alignmentClasses = {
    left: 'left-0 sm:left-0 origin-top-left',
    right: 'right-0 sm:right-0 origin-top-right',
    center: 'left-1/2 -translate-x-1/2 origin-top',
  };

  return (
    <div className={`relative inline-flex items-center ${className}`}>
      <button
        ref={buttonRef}
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        aria-label={title}
        title={title}
        className={`inline-flex items-center gap-1.5 p-1 rounded-full text-slate-400 hover:text-teal-700 hover:bg-teal-50 transition-colors cursor-pointer focus:outline-hidden focus:ring-2 focus:ring-teal-500/20 active:scale-95 ${buttonClassName}`}
      >
        <Info className={iconClassName} />
        {buttonLabel && <span className="text-xs font-semibold">{buttonLabel}</span>}
        {badgeText && (
          <span className="text-[10px] font-bold bg-teal-100 text-teal-800 px-1.5 py-0.2 rounded-full">
            {badgeText}
          </span>
        )}
      </button>

      {/* Popover Bubble */}
      {isOpen && (
        <div
          ref={popoverRef}
          role="dialog"
          aria-modal="true"
          className={`absolute top-full mt-2 z-50 w-72 sm:w-84 max-w-[90vw] p-4 bg-white/95 backdrop-blur-md rounded-2xl shadow-xl border border-teal-100 text-slate-700 text-xs animate-fadeIn ${alignmentClasses[align]}`}
        >
          {/* Header */}
          <div className="flex items-center justify-between gap-2 pb-2 mb-2 border-b border-slate-100">
            <div className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-teal-500"></span>
              <h4 className="font-bold text-slate-900 text-xs tracking-tight">{title}</h4>
            </div>
            <button
              type="button"
              onClick={() => setIsOpen(false)}
              className="text-slate-400 hover:text-slate-700 p-0.5 rounded-md hover:bg-slate-100 cursor-pointer"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          </div>

          {/* Body Content */}
          <div className="text-slate-600 space-y-2 leading-relaxed text-[11px] sm:text-xs">
            {children}
          </div>
        </div>
      )}
    </div>
  );
};
