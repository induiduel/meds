import React, { useCallback, useEffect, useRef, useState, useSyncExternalStore } from 'react';
import {
  PenTool,
  Highlighter as MarkerIcon,
  Eraser,
  Undo2,
  Trash2,
  X,
  Palette,
  Minus,
  Check,
  ChevronDown,
} from 'lucide-react';
import { toast } from '../ui/Toast';

// ---------------------------------------------------------------------------
// Types & Persistence
// ---------------------------------------------------------------------------
export interface DrawingPoint {
  x: number; // 0 to 1 normalized
  y: number; // 0 to 1 normalized
}

export interface DrawingStroke {
  id: string;
  points: DrawingPoint[];
  color: string;
  size: number; // base stroke width in px
  isHighlighter?: boolean;
}

const STORAGE_PREFIX = 'medsoru_slide_drawings_v2';

const readScopeDrawings = (scope: string): DrawingStroke[] => {
  try {
    const raw = localStorage.getItem(`${STORAGE_PREFIX}:${scope}`);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
};

const saveScopeDrawings = (scope: string, strokes: DrawingStroke[]) => {
  try {
    if (strokes.length > 0) {
      localStorage.setItem(`${STORAGE_PREFIX}:${scope}`, JSON.stringify(strokes));
    } else {
      localStorage.removeItem(`${STORAGE_PREFIX}:${scope}`);
    }
  } catch {
    // Storage quota or private mode fallback
  }
};

// Global drawing tool state store
export type DrawingToolMode = 'none' | 'pen' | 'highlighter' | 'eraser';

interface DrawingGlobalState {
  activeMode: DrawingToolMode;
  color: string;
  penSize: number;
  highlighterSize: number;
}

let globalDrawingState: DrawingGlobalState = {
  activeMode: 'none',
  color: '#EF4444', // Red default for high-yield notes
  penSize: 3,
  highlighterSize: 22,
};

const drawingListeners = new Set<() => void>();
export const setDrawingGlobalState = (patch: Partial<DrawingGlobalState>) => {
  globalDrawingState = { ...globalDrawingState, ...patch };
  drawingListeners.forEach((l) => l());
};

export const useDrawingGlobalState = () =>
  useSyncExternalStore(
    (cb) => {
      drawingListeners.add(cb);
      return () => drawingListeners.delete(cb);
    },
    () => globalDrawingState,
    () => globalDrawingState
  );

export const PALETTE_COLORS = [
  { id: 'red', label: 'Kırmızı (Önemli)', hex: '#EF4444' },
  { id: 'blue', label: 'Mavi (Çıkmış Soru)', hex: '#2563EB' },
  { id: 'yellow', label: 'Fosforlu Sarı', hex: '#FACC15' },
  { id: 'green', label: 'Yeşil (Klinik Not)', hex: '#16A34A' },
  { id: 'purple', label: 'Mor (Genel Not)', hex: '#9333EA' },
  { id: 'black', label: 'Siyah (El Yazısı)', hex: '#1E293B' },
];

// ---------------------------------------------------------------------------
// Slide Drawing Canvas Component
// ---------------------------------------------------------------------------
export const SlideDrawingCanvas: React.FC<{
  scope: string;
  className?: string;
}> = ({ scope, className = '' }) => {
  const { activeMode, color, penSize, highlighterSize } = useDrawingGlobalState();
  const containerRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const [strokes, setStrokes] = useState<DrawingStroke[]>(() => readScopeDrawings(scope));
  const currentStrokeRef = useRef<DrawingStroke | null>(null);
  const isDrawingRef = useRef(false);

  // Sync with scope changes (when changing slides)
  useEffect(() => {
    const loaded = readScopeDrawings(scope);
    setStrokes(loaded);
  }, [scope]);

  // Save on strokes update
  const commitStrokes = useCallback(
    (next: DrawingStroke[]) => {
      setStrokes(next);
      saveScopeDrawings(scope, next);
    },
    [scope]
  );

  // Render all strokes onto the HTML5 Canvas
  const redraw = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const w = canvas.width;
    const h = canvas.height;
    ctx.clearRect(0, 0, w, h);

    if (strokes.length === 0 && !currentStrokeRef.current) return;

    const all = currentStrokeRef.current ? [...strokes, currentStrokeRef.current] : strokes;

    all.forEach((stroke) => {
      if (stroke.points.length < 2) {
        // Draw single dot
        if (stroke.points.length === 1) {
          const p = stroke.points[0];
          ctx.beginPath();
          ctx.arc(p.x * w, p.y * h, (stroke.size || 3) / 2, 0, Math.PI * 2);
          ctx.fillStyle = stroke.isHighlighter
            ? stroke.color.includes('rgba')
              ? stroke.color
              : `${stroke.color}66`
            : stroke.color;
          ctx.fill();
        }
        return;
      }

      ctx.save();
      ctx.beginPath();
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';

      if (stroke.isHighlighter) {
        ctx.strokeStyle = stroke.color.includes('rgba') ? stroke.color : `${stroke.color}66`;
        ctx.lineWidth = stroke.size || 22;
        // Use multiply composite for realistic digital highlighter over text
        ctx.globalCompositeOperation = 'source-over';
      } else {
        ctx.strokeStyle = stroke.color;
        ctx.lineWidth = stroke.size || 3;
        ctx.globalCompositeOperation = 'source-over';
      }

      const p0 = stroke.points[0];
      ctx.moveTo(p0.x * w, p0.y * h);

      for (let i = 1; i < stroke.points.length; i++) {
        const p1 = stroke.points[i];
        // Quadratic curve for smooth handwriting
        if (i < stroke.points.length - 1) {
          const p2 = stroke.points[i + 1];
          const midX = ((p1.x + p2.x) / 2) * w;
          const midY = ((p1.y + p2.y) / 2) * h;
          ctx.quadraticCurveTo(p1.x * w, p1.y * h, midX, midY);
        } else {
          ctx.lineTo(p1.x * w, p1.y * h);
        }
      }

      ctx.stroke();
      ctx.restore();
    });
  }, [strokes]);

  // Handle Resize & Canvas sizing
  useEffect(() => {
    const updateSize = () => {
      const container = containerRef.current;
      const canvas = canvasRef.current;
      if (!container || !canvas) return;

      const rect = container.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;
      const displayWidth = Math.max(300, Math.round(rect.width));
      const displayHeight = Math.max(300, Math.round(rect.height));

      if (canvas.width !== displayWidth * dpr || canvas.height !== displayHeight * dpr) {
        canvas.width = displayWidth * dpr;
        canvas.height = displayHeight * dpr;
        const ctx = canvas.getContext('2d');
        if (ctx) {
          ctx.scale(dpr, dpr);
        }
        redraw();
      }
    };

    updateSize();
    const ro = new ResizeObserver(updateSize);
    if (containerRef.current) ro.observe(containerRef.current);
    window.addEventListener('resize', updateSize);
    return () => {
      ro.disconnect();
      window.removeEventListener('resize', updateSize);
    };
  }, [redraw]);

  // Redraw when strokes change
  useEffect(() => {
    redraw();
  }, [strokes, redraw]);

  // Pointer drawing event handlers (supports stylus, finger touch, mouse)
  const onPointerDown = (e: React.PointerEvent<HTMLCanvasElement>) => {
    if (activeMode === 'none') return;
    const canvas = canvasRef.current;
    if (!canvas) return;

    // Capture pointer to guarantee pointerup/move even outside element
    canvas.setPointerCapture(e.pointerId);
    isDrawingRef.current = true;

    const rect = canvas.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width;
    const y = (e.clientY - rect.top) / rect.height;

    // Eraser Mode: erase touched strokes
    if (activeMode === 'eraser') {
      const threshold = 0.03; // ~3% of canvas
      const filtered = strokes.filter((st) => {
        return !st.points.some((p) => Math.hypot(p.x - x, p.y - y) < threshold);
      });
      if (filtered.length !== strokes.length) {
        commitStrokes(filtered);
      }
      return;
    }

    // Pen or Highlighter Mode
    const isHl = activeMode === 'highlighter';
    const currentSize = isHl ? highlighterSize : penSize;

    currentStrokeRef.current = {
      id: `${Date.now()}-${Math.random().toString(36).slice(2, 6)}`,
      points: [{ x, y }],
      color,
      size: currentSize,
      isHighlighter: isHl,
    };

    redraw();
  };

  const onPointerMove = (e: React.PointerEvent<HTMLCanvasElement>) => {
    if (!isDrawingRef.current) return;
    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const x = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
    const y = Math.max(0, Math.min(1, (e.clientY - rect.top) / rect.height));

    if (activeMode === 'eraser') {
      const threshold = 0.035;
      const filtered = strokes.filter((st) => {
        return !st.points.some((p) => Math.hypot(p.x - x, p.y - y) < threshold);
      });
      if (filtered.length !== strokes.length) {
        commitStrokes(filtered);
      }
      return;
    }

    if (currentStrokeRef.current) {
      currentStrokeRef.current.points.push({ x, y });
      redraw();
    }
  };

  const onPointerUp = (e: React.PointerEvent<HTMLCanvasElement>) => {
    if (!isDrawingRef.current) return;
    isDrawingRef.current = false;
    const canvas = canvasRef.current;
    if (canvas && canvas.hasPointerCapture(e.pointerId)) {
      canvas.releasePointerCapture(e.pointerId);
    }

    if (currentStrokeRef.current && currentStrokeRef.current.points.length > 0) {
      const completed = [...strokes, currentStrokeRef.current];
      currentStrokeRef.current = null;
      commitStrokes(completed);
    } else {
      currentStrokeRef.current = null;
    }
  };

  const undo = () => {
    if (strokes.length === 0) return;
    const next = strokes.slice(0, -1);
    commitStrokes(next);
  };

  const clearAll = () => {
    if (strokes.length === 0) return;
    commitStrokes([]);
    toast.info('Slayt çizimleri temizlendi');
  };

  const isInteractive = activeMode !== 'none';

  return (
    <div
      ref={containerRef}
      className={`absolute inset-0 z-20 pointer-events-none select-none overflow-hidden ${className}`}
    >
      <canvas
        ref={canvasRef}
        onPointerDown={onPointerDown}
        onPointerMove={onPointerMove}
        onPointerUp={onPointerUp}
        onPointerCancel={onPointerUp}
        className={`w-full h-full ${
          isInteractive
            ? 'pointer-events-auto touch-none cursor-crosshair'
            : 'pointer-events-none'
        }`}
      />

      {/* Floating Canvas Action Controls when drawings exist */}
      {isInteractive && (
        <div className="absolute top-2 right-2 flex items-center gap-1.5 z-30 pointer-events-auto bg-white/90 dark:bg-panel/90 backdrop-blur-md p-1 rounded-xl border border-line shadow-md animate-in fade-in duration-150">
          <button
            type="button"
            onClick={undo}
            disabled={strokes.length === 0}
            title="Geri Al"
            className="p-1.5 rounded-lg text-ink-2 hover:text-ink hover:bg-canvas disabled:opacity-30 disabled:pointer-events-none cursor-pointer transition-colors"
          >
            <Undo2 className="w-4 h-4" />
          </button>
          <button
            type="button"
            onClick={clearAll}
            disabled={strokes.length === 0}
            title="Bu Slaytın Çizimlerini Temizle"
            className="p-1.5 rounded-lg text-ink-2 hover:text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-950/40 disabled:opacity-30 disabled:pointer-events-none cursor-pointer transition-colors"
          >
            <Trash2 className="w-4 h-4" />
          </button>
          <div className="w-[1px] h-4 bg-line-soft mx-0.5" />
          <span className="text-[11px] font-mono font-semibold text-ink-3 px-1">
            {strokes.length} çizim (Kayıtlı)
          </span>
        </div>
      )}
    </div>
  );
};

// ---------------------------------------------------------------------------
// Drawing Floating Bar for Top Header / Toolbar
// ---------------------------------------------------------------------------
export const DrawingModeToolbarTrigger: React.FC<{ className?: string }> = ({ className = '' }) => {
  const { activeMode, color, penSize, highlighterSize } = useDrawingGlobalState();
  const [showColorPicker, setShowColorPicker] = useState(false);

  const togglePen = () => {
    if (activeMode === 'pen') {
      setDrawingGlobalState({ activeMode: 'none' });
      toast.info('Kalem modu kapatıldı');
    } else {
      setDrawingGlobalState({ activeMode: 'pen' });
      toast.success('Kalem Modu Açık', 'Slaytın üzerine el yazısıyla not alıp çizebilirsiniz. Yazdıklarınız silinmez ve kaydedilir.');
    }
  };

  const toggleHighlighter = () => {
    if (activeMode === 'highlighter') {
      setDrawingGlobalState({ activeMode: 'none' });
    } else {
      setDrawingGlobalState({ activeMode: 'highlighter' });
      toast.success('Fosforlu Çizim Modu', 'Metin seçmenize gerek kalmadan parmağınızla satırların üstünü doğrudan fosforlayabilirsiniz.');
    }
  };

  const toggleEraser = () => {
    if (activeMode === 'eraser') {
      setDrawingGlobalState({ activeMode: 'pen' });
    } else {
      setDrawingGlobalState({ activeMode: 'eraser' });
      toast.info('Silgi Modu', 'Silmek istediğiniz çizgilere dokunun.');
    }
  };

  return (
    <div className={`flex items-center gap-1 ${className}`}>
      {/* Main Pen Mode Button */}
      <button
        type="button"
        onClick={togglePen}
        aria-pressed={activeMode === 'pen'}
        title={activeMode === 'pen' ? 'Kalemi Kapat' : 'Kalem Modu (Üzerine Yazıp Çiz)'}
        className={`h-9 px-2.5 rounded-[10px] flex items-center gap-1.5 cursor-pointer transition-all ${
          activeMode === 'pen'
            ? 'bg-rose-500 text-white font-semibold shadow-xs ring-2 ring-rose-500/30'
            : activeMode !== 'none'
            ? 'bg-accent-soft text-accent'
            : 'text-ink-2 hover:bg-canvas hover:text-ink border border-line'
        }`}
      >
        <PenTool className="w-4 h-4" />
        <span className="hidden sm:inline text-[12.5px]">Kalem Modu</span>
      </button>

      {/* When active, show tool selector: Pen, Highlighter, Eraser, Color, Size */}
      {activeMode !== 'none' && (
        <div className="flex items-center gap-1 h-9 px-1.5 rounded-[10px] bg-canvas border border-line animate-in fade-in zoom-in-95 duration-150 shadow-2xs">
          {/* Pen Tool Button */}
          <button
            type="button"
            onClick={() => setDrawingGlobalState({ activeMode: 'pen' })}
            aria-pressed={activeMode === 'pen'}
            title="İnce Kalem (Yazı & Not)"
            className={`w-7 h-7 rounded-lg flex items-center justify-center cursor-pointer transition-colors ${
              activeMode === 'pen' ? 'bg-white shadow-2xs text-ink font-bold' : 'text-ink-2 hover:text-ink'
            }`}
          >
            <PenTool className="w-3.5 h-3.5" />
          </button>

          {/* Highlighter Tool Button */}
          <button
            type="button"
            onClick={toggleHighlighter}
            aria-pressed={activeMode === 'highlighter'}
            title="Fosforlu Kalem (Parmağınla Boya)"
            className={`w-7 h-7 rounded-lg flex items-center justify-center cursor-pointer transition-colors ${
              activeMode === 'highlighter' ? 'bg-white shadow-2xs text-amber-600 font-bold' : 'text-ink-2 hover:text-ink'
            }`}
          >
            <MarkerIcon className="w-3.5 h-3.5" />
          </button>

          {/* Eraser Button */}
          <button
            type="button"
            onClick={toggleEraser}
            aria-pressed={activeMode === 'eraser'}
            title="Silgi"
            className={`w-7 h-7 rounded-lg flex items-center justify-center cursor-pointer transition-colors ${
              activeMode === 'eraser' ? 'bg-white shadow-2xs text-ink font-bold' : 'text-ink-2 hover:text-ink'
            }`}
          >
            <Eraser className="w-3.5 h-3.5" />
          </button>

          <div className="w-[1px] h-4 bg-line-soft mx-0.5" />

          {/* Color Swatch Trigger */}
          <div className="relative">
            <button
              type="button"
              onClick={() => setShowColorPicker((v) => !v)}
              title="Renk Seç"
              className="w-7 h-7 rounded-lg flex items-center justify-center cursor-pointer hover:bg-white transition-colors"
            >
              <span
                className="w-4 h-4 rounded-full border border-black/20 shadow-2xs"
                style={{ backgroundColor: color }}
              />
            </button>

            {/* Color Palette Popover */}
            {showColorPicker && (
              <div
                className="absolute top-9 left-0 z-50 p-2 bg-white dark:bg-panel border border-line rounded-xl shadow-xl flex items-center gap-1.5 animate-in fade-in duration-100"
                onClick={(e) => e.stopPropagation()}
              >
                {PALETTE_COLORS.map((c) => (
                  <button
                    key={c.id}
                    type="button"
                    onClick={() => {
                      setDrawingGlobalState({ color: c.hex });
                      setShowColorPicker(false);
                    }}
                    title={c.label}
                    className="w-6 h-6 rounded-full flex items-center justify-center cursor-pointer transition-transform hover:scale-110 shadow-2xs"
                    style={{ backgroundColor: c.hex }}
                  >
                    {color === c.hex && <Check className="w-3.5 h-3.5 text-white drop-shadow-sm" />}
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Close Pen Mode */}
          <button
            type="button"
            onClick={() => setDrawingGlobalState({ activeMode: 'none' })}
            title="Çizim modunu kapat (Slayta dokunma moduna dön)"
            className="w-7 h-7 rounded-lg flex items-center justify-center text-ink-3 hover:text-ink cursor-pointer hover:bg-line transition-colors"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        </div>
      )}
    </div>
  );
};
