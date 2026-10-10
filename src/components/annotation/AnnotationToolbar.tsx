import React from 'react';
import {
  Eraser,
  Hand,
  Highlighter,
  Maximize2,
  Minimize2,
  PenLine,
  Redo2,
  Trash2,
  Undo2,
  X,
  ZoomIn,
  ZoomOut,
} from 'lucide-react';
import type { AnnotationEngine } from './engine/AnnotationEngine';
import type { DrawTool, EngineSnapshot } from './types';

const PEN_COLORS = ['#1e293b', '#2563eb', '#dc2626', '#16a34a', '#9333ea'];
const HIGHLIGHTER_COLORS = ['#fde047', '#86efac', '#7dd3fc', '#f9a8d4', '#fdba74'];
const PEN_SIZES = [1.6, 2.4, 4];
const HIGHLIGHTER_SIZES = [12, 18, 28];
const ERASER_SIZES = [8, 14, 28];

interface AnnotationToolbarProps {
  engine: AnnotationEngine | null;
  snapshot: EngineSnapshot | null;
  title?: string;
  isFullscreen: boolean;
  onToggleFullscreen: () => void;
  onClose?: () => void;
}

export function AnnotationToolbar({ engine, snapshot, title, isFullscreen, onToggleFullscreen, onClose }: AnnotationToolbarProps) {
  if (!snapshot) return null;
  const { settings, activeTool } = snapshot;

  const sizes = settings.tool === 'pen' ? PEN_SIZES : settings.tool === 'highlighter' ? HIGHLIGHTER_SIZES : ERASER_SIZES;
  const currentSize =
    settings.tool === 'pen' ? settings.penSize : settings.tool === 'highlighter' ? settings.highlighterSize : settings.eraserSize;
  const setSize = (v: number) =>
    engine?.updateSettings(
      settings.tool === 'pen' ? { penSize: v } : settings.tool === 'highlighter' ? { highlighterSize: v } : { eraserSize: v },
    );

  return (
    <div className="flex items-center gap-1 overflow-x-auto border-b border-slate-200 bg-white/95 px-2 py-1.5 backdrop-blur [scrollbar-width:none]">
      {onClose && (
        <IconButton label="Kapat" onClick={onClose}>
          <X size={18} />
        </IconButton>
      )}
      {title && <span className="mr-2 hidden max-w-[16rem] truncate text-sm font-semibold text-slate-800 md:inline">{title}</span>}

      <Group>
        <ToolButton tool="pen" label="Kalem" active={activeTool} onSelect={(t) => engine?.setTool(t)}>
          <PenLine size={18} />
        </ToolButton>
        <ToolButton tool="highlighter" label="Fosforlu kalem" active={activeTool} onSelect={(t) => engine?.setTool(t)}>
          <Highlighter size={18} />
        </ToolButton>
        <ToolButton tool="eraser" label="Silgi" active={activeTool} onSelect={(t) => engine?.setTool(t)}>
          <Eraser size={18} />
        </ToolButton>
      </Group>

      {settings.tool !== 'eraser' && (
        <Group>
          {(settings.tool === 'pen' ? PEN_COLORS : HIGHLIGHTER_COLORS).map((c) => {
            const selected = (settings.tool === 'pen' ? settings.penColor : settings.highlighterColor) === c;
            return (
              <button
                key={c}
                type="button"
                aria-label={`Renk ${c}`}
                aria-pressed={selected}
                onClick={() => engine?.updateSettings(settings.tool === 'pen' ? { penColor: c } : { highlighterColor: c })}
                className={`h-7 w-7 shrink-0 rounded-full border-2 transition ${selected ? 'border-slate-900 scale-110' : 'border-white ring-1 ring-slate-200'}`}
                style={{ backgroundColor: c }}
              />
            );
          })}
        </Group>
      )}

      {settings.tool === 'eraser' && (
        <Group>
          {(['stroke', 'pixel'] as const).map((mode) => (
            <button
              key={mode}
              type="button"
              aria-pressed={settings.eraserMode === mode}
              onClick={() => engine?.updateSettings({ eraserMode: mode })}
              className={`h-8 shrink-0 rounded-md px-2.5 text-xs font-medium ${
                settings.eraserMode === mode ? 'bg-slate-900 text-white' : 'text-slate-600 hover:bg-slate-100'
              }`}
            >
              {mode === 'stroke' ? 'Çizgi silgisi' : 'Piksel silgisi'}
            </button>
          ))}
        </Group>
      )}

      <Group>
        {sizes.map((v, i) => (
          <button
            key={v}
            type="button"
            aria-label={`Kalınlık ${i + 1}`}
            aria-pressed={currentSize === v}
            onClick={() => setSize(v)}
            className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-md ${currentSize === v ? 'bg-slate-200' : 'hover:bg-slate-100'}`}
          >
            <span className="rounded-full bg-slate-800" style={{ width: 4 + i * 4, height: 4 + i * 4 }} />
          </button>
        ))}
      </Group>

      <Group>
        <IconButton label="Geri al" disabled={!snapshot.canUndo} onClick={() => engine?.undo()}>
          <Undo2 size={18} />
        </IconButton>
        <IconButton label="İleri al" disabled={!snapshot.canRedo} onClick={() => engine?.redo()}>
          <Redo2 size={18} />
        </IconButton>
        <IconButton
          label="Tümünü temizle"
          disabled={snapshot.strokeCount === 0}
          onClick={() => {
            if (window.confirm('Bu sayfadaki tüm çizimler silinsin mi? (Geri al ile geri getirebilirsiniz)')) engine?.clear();
          }}
        >
          <Trash2 size={18} />
        </IconButton>
      </Group>

      <div className="ml-auto flex shrink-0 items-center gap-1">
        {snapshot.temporaryEraser && (
          <span className="rounded-full bg-amber-100 px-2 py-0.5 text-xs font-medium text-amber-800">Kalem düğmesi: silgi</span>
        )}
        {/* Kalemini 'touch' olarak bildiren cihazlar (bazı Huawei/eski WebView) için yedek. */}
        {!snapshot.penDetected && (
          <IconButton
            label={snapshot.allowTouchDrawing ? 'Parmakla çizim açık' : 'Parmakla çiz'}
            active={snapshot.allowTouchDrawing}
            onClick={() => engine?.setAllowTouchDrawing(!snapshot.allowTouchDrawing)}
          >
            <Hand size={18} />
          </IconButton>
        )}
        <IconButton label="Uzaklaştır" onClick={() => engine?.zoomBy(1 / 1.25)}>
          <ZoomOut size={18} />
        </IconButton>
        <button
          type="button"
          onClick={() => engine?.resetView()}
          className="h-8 min-w-[3.25rem] shrink-0 rounded-md px-1 text-xs font-medium tabular-nums text-slate-600 hover:bg-slate-100"
          aria-label="Sayfaya sığdır"
        >
          %{Math.round(snapshot.zoom * 100)}
        </button>
        <IconButton label="Yakınlaştır" onClick={() => engine?.zoomBy(1.25)}>
          <ZoomIn size={18} />
        </IconButton>
        <IconButton label={isFullscreen ? 'Tam ekrandan çık' : 'Tam ekran'} onClick={onToggleFullscreen}>
          {isFullscreen ? <Minimize2 size={18} /> : <Maximize2 size={18} />}
        </IconButton>
      </div>
    </div>
  );
}

function Group({ children }: { children: React.ReactNode }) {
  return <div className="flex shrink-0 items-center gap-1 border-r border-slate-200 px-1.5 last:border-r-0">{children}</div>;
}

function ToolButton({
  tool,
  label,
  active,
  onSelect,
  children,
}: {
  tool: DrawTool;
  label: string;
  active: DrawTool;
  onSelect: (tool: DrawTool) => void;
  children: React.ReactNode;
}) {
  return (
    <IconButton label={label} active={active === tool} onClick={() => onSelect(tool)}>
      {children}
    </IconButton>
  );
}

function IconButton({
  label,
  active = false,
  disabled = false,
  onClick,
  children,
}: {
  label: string;
  active?: boolean;
  disabled?: boolean;
  onClick: () => void;
  children: React.ReactNode;
}) {
  return (
    <button
      type="button"
      title={label}
      aria-label={label}
      aria-pressed={active}
      disabled={disabled}
      onClick={onClick}
      className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-md transition disabled:opacity-30 ${
        active ? 'bg-slate-900 text-white' : 'text-slate-700 hover:bg-slate-100'
      }`}
    >
      {children}
    </button>
  );
}
