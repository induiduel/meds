import React, { useEffect, useRef } from 'react';
import { AnnotationEngine } from './engine/AnnotationEngine';
import type { AnnotationDocument, EngineSnapshot, ToolSettings } from './types';

interface AnnotationSurfaceProps {
  /** Zemin katmanı: ders notu görseli, PDF sayfaları ya da HTML. `docWidth` px genişlikte yerleşir. */
  background: React.ReactNode;
  docWidth?: number;
  initialDocument?: AnnotationDocument | null;
  initialSettings?: Partial<ToolSettings>;
  onEngine?: (engine: AnnotationEngine | null) => void;
  onSnapshot?: (snapshot: EngineSnapshot) => void;
  onDocumentChange?: (doc: AnnotationDocument) => void;
  className?: string;
}

const layerStyle: React.CSSProperties = {
  position: 'absolute',
  left: 0,
  top: 0,
  pointerEvents: 'none', // tüm pointer olayları viewport'a düşer
};

/**
 * Katmanlı çizim yüzeyi. Motor yalnızca bir kez (mount'ta) oluşturulur;
 * geri çağırmalar ref üzerinden okunduğu için prop değişimi motoru yeniden kurmaz.
 */
export function AnnotationSurface({
  background,
  docWidth = 1000,
  initialDocument,
  initialSettings,
  onEngine,
  onSnapshot,
  onDocumentChange,
  className,
}: AnnotationSurfaceProps) {
  const viewportRef = useRef<HTMLDivElement>(null);
  const contentRef = useRef<HTMLDivElement>(null);
  const hlRef = useRef<HTMLCanvasElement>(null);
  const inkRef = useRef<HTMLCanvasElement>(null);
  const liveRef = useRef<HTMLCanvasElement>(null);

  const callbacks = useRef({ onEngine, onSnapshot, onDocumentChange });
  callbacks.current = { onEngine, onSnapshot, onDocumentChange };

  useEffect(() => {
    const engine = new AnnotationEngine(
      {
        viewport: viewportRef.current!,
        content: contentRef.current!,
        highlightCanvas: hlRef.current!,
        inkCanvas: inkRef.current!,
        liveCanvas: liveRef.current!,
      },
      {
        docWidth,
        initialDocument,
        settings: initialSettings,
        onSnapshot: (s) => callbacks.current.onSnapshot?.(s),
        onDocumentChange: (d) => callbacks.current.onDocumentChange?.(d),
      },
    );
    callbacks.current.onEngine?.(engine);
    return () => {
      engine.destroy();
      callbacks.current.onEngine?.(null);
    };
    // Motor bilinçli olarak yalnızca docWidth değişince yeniden kurulur.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [docWidth]);

  return (
    <div
      ref={viewportRef}
      className={className}
      style={{
        position: 'relative',
        overflow: 'hidden',
        // Tarayıcının kaydırma/yakınlaştırma/çift dokunma davranışını kapatır;
        // jestleri motor kendisi yönetir. Palm rejection için şart.
        touchAction: 'none',
        // mix-blend-mode yalnızca bu kutunun içindekilerle karışsın.
        isolation: 'isolate',
        userSelect: 'none',
        WebkitUserSelect: 'none',
        WebkitTouchCallout: 'none', // iOS uzun basış menüsü / büyüteç
        overscrollBehavior: 'none',
      }}
    >
      <div
        ref={contentRef}
        style={{ ...layerStyle, width: docWidth, transformOrigin: '0 0' }}
        className="bg-white shadow-[0_1px_3px_rgba(15,23,42,0.12),0_8px_24px_rgba(15,23,42,0.08)]"
      >
        {background}
      </div>
      <canvas ref={hlRef} style={{ ...layerStyle, mixBlendMode: 'multiply' }} />
      <canvas ref={inkRef} style={layerStyle} />
      <canvas ref={liveRef} style={layerStyle} />
    </div>
  );
}

/** Görsel tabanlı ders notu için hazır zemin. */
export function ImageBackground({ src, alt = '' }: { src: string; alt?: string }) {
  return <img src={src} alt={alt} draggable={false} style={{ display: 'block', width: '100%', height: 'auto' }} />;
}
