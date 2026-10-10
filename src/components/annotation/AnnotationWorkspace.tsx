import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { AnnotationSurface } from './AnnotationSurface';
import { AnnotationToolbar } from './AnnotationToolbar';
import { PenDiagnostics } from './PenDiagnostics';
import type { AnnotationEngine } from './engine/AnnotationEngine';
import type { AnnotationDocument, EngineSnapshot } from './types';

interface AnnotationWorkspaceProps {
  title?: string;
  /** Ders notu zemini (ör. <ImageBackground src=... />). */
  background: React.ReactNode;
  docWidth?: number;
  /**
   * Verilirse çizimler bu anahtarla tarayıcıda (localStorage) saklanır.
   * Hesaplar arası senkron için `onDocumentChange` ile sunucuya da gönderin.
   */
  storageKey?: string;
  initialDocument?: AnnotationDocument | null;
  onDocumentChange?: (doc: AnnotationDocument) => void;
  onClose?: () => void;
  /** Kalem tanılama paneli. Verilmezse adreste `?kalemtani` varsa açılır. */
  showDiagnostics?: boolean;
}

/**
 * Tam ekran not çizim çalışma alanı: araç çubuğu + katmanlı yüzey.
 * Klavye: Ctrl/⌘+Z geri, Ctrl/⌘+Shift+Z veya Ctrl+Y ileri, P kalem, H fosforlu, E silgi.
 */
export function AnnotationWorkspace({
  title,
  background,
  docWidth = 1000,
  storageKey,
  initialDocument,
  onDocumentChange,
  onClose,
  showDiagnostics,
}: AnnotationWorkspaceProps) {
  const rootRef = useRef<HTMLDivElement>(null);
  const [surfaceHost, setSurfaceHost] = useState<HTMLDivElement | null>(null);
  const diagnostics = showDiagnostics ?? new URLSearchParams(window.location.search).has('kalemtani');
  const [engine, setEngine] = useState<AnnotationEngine | null>(null);
  const [snapshot, setSnapshot] = useState<EngineSnapshot | null>(null);
  const [isFullscreen, setIsFullscreen] = useState(false);

  const startDocument = useMemo(
    () => initialDocument ?? (storageKey ? readStored(storageKey) : null),
    // Yalnızca ilk açılışta okunur.
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [],
  );

  // Kaydetmeyi her çizgide değil, kısa bir sessizlikten sonra yap.
  const saveTimer = useRef<number | undefined>(undefined);
  const handleDocumentChange = useCallback(
    (doc: AnnotationDocument) => {
      onDocumentChange?.(doc);
      if (!storageKey) return;
      window.clearTimeout(saveTimer.current);
      saveTimer.current = window.setTimeout(() => writeStored(storageKey, doc), 400);
    },
    [onDocumentChange, storageKey],
  );
  useEffect(() => () => window.clearTimeout(saveTimer.current), []);

  useEffect(() => {
    if (!engine) return;
    const onKey = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement | null;
      if (target && (target.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(target.tagName))) return;
      const mod = e.ctrlKey || e.metaKey;
      const key = e.key.toLowerCase();
      if (mod && key === 'z') {
        e.preventDefault();
        if (e.shiftKey) engine.redo();
        else engine.undo();
      } else if (mod && key === 'y') {
        e.preventDefault();
        engine.redo();
      } else if (!mod && !e.altKey) {
        if (key === 'p') engine.setTool('pen');
        else if (key === 'h') engine.setTool('highlighter');
        else if (key === 'e') engine.setTool('eraser');
        else if (key === 'escape' && !document.fullscreenElement) onClose?.();
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [engine, onClose]);

  // Açıkken arka sayfanın kaymasını engelle (iOS lastik bant kaydırması dahil).
  useEffect(() => {
    const { overflow, overscrollBehavior } = document.body.style;
    document.body.style.overflow = 'hidden';
    document.body.style.overscrollBehavior = 'none';
    return () => {
      document.body.style.overflow = overflow;
      document.body.style.overscrollBehavior = overscrollBehavior;
    };
  }, []);

  useEffect(() => {
    const onChange = () => setIsFullscreen(Boolean(document.fullscreenElement ?? (document as WebkitDocument).webkitFullscreenElement));
    document.addEventListener('fullscreenchange', onChange);
    document.addEventListener('webkitfullscreenchange', onChange);
    return () => {
      document.removeEventListener('fullscreenchange', onChange);
      document.removeEventListener('webkitfullscreenchange', onChange);
    };
  }, []);

  const toggleFullscreen = useCallback(() => {
    const doc = document as WebkitDocument;
    if (document.fullscreenElement ?? doc.webkitFullscreenElement) {
      void (document.exitFullscreen?.() ?? doc.webkitExitFullscreen?.());
      return;
    }
    // iPhone Safari öğe tam ekranını desteklemez; çalışma alanı zaten sabit (fixed) tam pencere.
    const el = rootRef.current as WebkitElement | null;
    void (el?.requestFullscreen?.() ?? el?.webkitRequestFullscreen?.())?.catch?.(() => undefined);
  }, []);

  return (
    <div ref={rootRef} className="fixed inset-0 z-[100] flex h-[100dvh] flex-col bg-slate-200">
      <AnnotationToolbar
        engine={engine}
        snapshot={snapshot}
        title={title}
        isFullscreen={isFullscreen}
        onToggleFullscreen={toggleFullscreen}
        onClose={onClose}
      />
      <div ref={setSurfaceHost} className="relative flex min-h-0 flex-1 flex-col">
        <AnnotationSurface
          className="min-h-0 flex-1"
          background={background}
          docWidth={docWidth}
          initialDocument={startDocument}
          onEngine={setEngine}
          onSnapshot={setSnapshot}
          onDocumentChange={handleDocumentChange}
        />
        {diagnostics && <PenDiagnostics target={surfaceHost} />}
      </div>
    </div>
  );
}

type WebkitDocument = Document & { webkitFullscreenElement?: Element | null; webkitExitFullscreen?: () => Promise<void> | void };
type WebkitElement = HTMLElement & { webkitRequestFullscreen?: () => Promise<void> | void };

const STORAGE_PREFIX = 'medsoru_annotations:';

function readStored(key: string): AnnotationDocument | null {
  try {
    const raw = localStorage.getItem(STORAGE_PREFIX + key);
    if (!raw) return null;
    const doc = JSON.parse(raw) as AnnotationDocument;
    return doc?.version === 1 && Array.isArray(doc.strokes) ? doc : null;
  } catch {
    return null;
  }
}

function writeStored(key: string, doc: AnnotationDocument): void {
  try {
    localStorage.setItem(STORAGE_PREFIX + key, JSON.stringify(doc));
  } catch {
    /* gizli sekme / kota dolu: çizim oturum boyunca bellekte kalır */
  }
}
