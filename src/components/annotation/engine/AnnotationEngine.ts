import type {
  AnnotationDocument,
  DrawTool,
  EngineSnapshot,
  Stroke,
  StrokeKind,
  ToolSettings,
  ViewState,
} from '../types';
import { bboxIntersects, cacheStrokeBBox, strokeBBox, strokeHit, type BBox } from './geometry';
import { History } from './history';
import { coalesced, isEraserButton, isHoverBarrel, makeId, readPressure } from './input';
import { drawCommittedStroke, drawEraserCursor, drawPenStroke, drawUniformStroke } from './renderer';

/**
 * AnnotationEngine — framework'süz (vanilla TS) çizim motoru.
 *
 * Katmanlar (alttan üste, hepsi viewport'u kaplar):
 *   1. content         → ders notu (görsel/PDF/HTML); CSS transform ile ölçeklenir.
 *   2. highlightCanvas → fosforlu çizgiler; CSS `mix-blend-mode: multiply` ile notun
 *                         üstüne gerçek fosforlu gibi biner (siyah yazı siyah kalır).
 *   3. inkCanvas       → kalem çizgileri.
 *   4. liveCanvas      → yalnızca o an çizilen çizgi + silgi imleci (hızlı, artımlı).
 *
 * Canvas'lar sayfa boyutunda değil, VIEWPORT boyutunda × devicePixelRatio'dur ve
 * yakınlaştırma ctx.setTransform ile uygulanır. Böylece 8x zoom'da bile çizgiler
 * keskin kalır ve iOS'un canvas bellek sınırına (≈16.7 MP) takılmaz.
 *
 * Girdi politikası:
 *   - pen   → çizer (yan düğme / silgi ucu basılıyken geçici silgi)
 *   - mouse → sol tık çizer, sağ tık geçici silgi, orta tık kaydırır, tekerlek kaydırır,
 *             Ctrl/⌘+tekerlek (ve trackpad pinch) yakınlaştırır
 *   - touch → asla çizmez (avuç içi reddi); 1 parmak kaydırır, 2 parmak yakınlaştırır,
 *             2 parmakla hızlı dokunuş geri alır. Kalem aktifken dokunuşlar yok sayılır.
 */

const MIN_ZOOM = 0.5;
const MAX_ZOOM = 8;
/** Son kalem olayından (hover dahil) bu kadar ms içinde gelen dokunuşlar avuç içi sayılır. */
const PALM_GUARD_MS = 500;
const TWO_FINGER_TAP_MS = 280;
const TAP_SLOP_PX = 12;
/**
 * S-Pen + Android Chrome: yan düğme yalnızca kalem HAVADAYKEN görünür; temas başlayınca
 * bilgi kaybolur. Havada görülen basış bu kadar ms içinde gelen temasa taşınır
 * (Galaxy Tab ölçümü: son "basılı" örnekle temas arası 140–380 ms).
 */
const HOVER_BARREL_LATCH_MS = 600;

const DEFAULT_SETTINGS: ToolSettings = {
  tool: 'pen',
  penColor: '#1e293b',
  penSize: 2.4,
  highlighterColor: '#fde047',
  highlighterSize: 18,
  eraserMode: 'stroke',
  eraserSize: 14,
};

export interface EngineElements {
  viewport: HTMLElement;
  content: HTMLElement;
  highlightCanvas: HTMLCanvasElement;
  inkCanvas: HTMLCanvasElement;
  liveCanvas: HTMLCanvasElement;
}

export interface EngineOptions {
  /** Sayfa genişliği (doküman birimi). content öğesi bu genişlikte (px) yerleşir. */
  docWidth?: number;
  initialDocument?: AnnotationDocument | null;
  settings?: Partial<ToolSettings>;
  onSnapshot?: (snapshot: EngineSnapshot) => void;
  /** Çizgi listesi her değiştiğinde (ekle/sil/geri al). Kaydetme için debounce önerilir. */
  onDocumentChange?: (doc: AnnotationDocument) => void;
}

type ActiveStroke =
  | {
      mode: 'draw';
      pointerId: number;
      pointerType: string;
      tool: DrawTool;
      /** Havada düğme basılıyken başladı: temas boyunca düğme okunamaz, kalem kalkana kadar silgi. */
      stickyEraser: boolean;
      stroke: Stroke;
      /** Canlı katmana artımlı çizimde kalınan segment indeksi. */
      drawnUpTo: number;
    }
  | {
      mode: 'stroke-erase';
      pointerId: number;
      pointerType: string;
      tool: DrawTool;
      stickyEraser: boolean;
      removed: Stroke[];
      last: { x: number; y: number } | null;
    };

type Gesture =
  | { type: 'pan'; startX: number; startY: number; startView: ViewState }
  | {
      type: 'pinch';
      startDist: number;
      startMid: { x: number; y: number };
      startView: ViewState;
      startTime: number;
      moved: boolean;
    }
  | { type: 'mouse-pan'; pointerId: number; startX: number; startY: number; startView: ViewState }
  /** İki parmak dokunuşu tüketildi; kalan parmak kalkana kadar hiçbir şey yapma. */
  | { type: 'idle' };

export class AnnotationEngine {
  private readonly el: EngineElements;
  private readonly opts: EngineOptions;
  private readonly docWidth: number;
  private readonly inkCtx: CanvasRenderingContext2D;
  private readonly hlCtx: CanvasRenderingContext2D;
  private readonly liveCtx: CanvasRenderingContext2D;

  private settings: ToolSettings;
  private strokes: Stroke[] = [];
  private seq = 0;
  private readonly history = new History();

  private view: ViewState = { zoom: 1, panX: 0, panY: 0 };
  private fitScale = 1;
  private vw = 0;
  private vh = 0;
  private dpr = 1;
  private docHeight = 1414;
  private rect: DOMRect | null = null;
  private initialized = false;

  private active: ActiveStroke | null = null;
  private touches = new Map<number, { x: number; y: number }>();
  private gesture: Gesture | null = null;
  private lastPenActivity = -Infinity;
  private penDetected = false;
  private allowTouchDrawing = false;
  private temporaryEraser = false;
  /** Havadaki kalemde yan düğmenin basılı görüldüğü son an (bkz. isHoverBarrel). */
  private hoverBarrelAt = -Infinity;
  private hoverPoint: { x: number; y: number } | null = null;

  private dirtyCommitted = true;
  private dirtyLive = true;
  private pendingCommits: Stroke[] = [];
  private rafId = 0;
  private emittedZoom = 1;
  private readonly cleanups: Array<() => void> = [];

  constructor(elements: EngineElements, options: EngineOptions = {}) {
    this.el = elements;
    this.opts = options;
    this.docWidth = options.docWidth ?? 1000;
    this.settings = { ...DEFAULT_SETTINGS, ...options.settings };
    this.inkCtx = getContext(elements.inkCanvas, true);
    this.hlCtx = getContext(elements.highlightCanvas, false);
    this.liveCtx = getContext(elements.liveCanvas, true);

    if (options.initialDocument) this.loadDocument(options.initialDocument, { silent: true });

    this.bindEvents();
    this.observeLayout();
    this.measure();
    this.emitSnapshot();
  }

  // ───────────────────────────── Genel API ─────────────────────────────

  setTool(tool: DrawTool): void {
    this.updateSettings({ tool });
  }

  updateSettings(patch: Partial<ToolSettings>): void {
    this.settings = { ...this.settings, ...patch };
    this.dirtyLive = true;
    this.requestRender();
    this.emitSnapshot();
  }

  setAllowTouchDrawing(allow: boolean): void {
    this.allowTouchDrawing = allow;
    this.emitSnapshot();
  }

  undo(): void {
    this.finishActiveStroke();
    const next = this.history.undo(this.strokes);
    if (next) this.replaceStrokes(next);
  }

  redo(): void {
    this.finishActiveStroke();
    const next = this.history.redo(this.strokes);
    if (next) this.replaceStrokes(next);
  }

  clear(): void {
    this.finishActiveStroke();
    if (this.strokes.length === 0) return;
    this.history.push({ kind: 'remove', strokes: [...this.strokes] });
    this.replaceStrokes([]);
  }

  zoomBy(factor: number): void {
    this.zoomAt(this.vw / 2, this.vh / 2, this.view.zoom * factor);
  }

  resetView(): void {
    this.view = { zoom: 1, panX: (this.vw - this.docWidth * this.fitScale) / 2, panY: this.margin };
    this.applyView();
  }

  getDocument(): AnnotationDocument {
    return { version: 1, docWidth: this.docWidth, strokes: this.strokes };
  }

  loadDocument(doc: AnnotationDocument, { silent = false } = {}): void {
    // Farklı genişlikte kaydedilmiş belgeyi bu sayfaya ölçekle.
    const k = doc.docWidth && doc.docWidth !== this.docWidth ? this.docWidth / doc.docWidth : 1;
    this.strokes = doc.strokes.map((s) =>
      k === 1 ? s : { ...s, size: s.size * k, points: s.points.map((p) => ({ x: p.x * k, y: p.y * k, p: p.p })) },
    );
    this.strokes.forEach(cacheStrokeBBox);
    this.seq = this.strokes.reduce((max, s) => Math.max(max, s.seq), 0);
    this.history.reset();
    this.dirtyCommitted = true;
    this.requestRender();
    if (!silent) this.emitSnapshot();
  }

  destroy(): void {
    cancelAnimationFrame(this.rafId);
    this.cleanups.forEach((fn) => fn());
    this.cleanups.length = 0;
  }

  // ───────────────────────────── Olay bağlama ─────────────────────────────

  private bindEvents(): void {
    const vp = this.el.viewport;
    const on = <K extends keyof HTMLElementEventMap>(
      type: K,
      handler: (e: HTMLElementEventMap[K]) => void,
      opts?: AddEventListenerOptions,
    ) => {
      vp.addEventListener(type, handler as EventListener, opts);
      this.cleanups.push(() => vp.removeEventListener(type, handler as EventListener, opts));
    };

    on('pointerdown', this.onPointerDown);
    on('pointermove', this.onPointerMove);
    on('pointerup', this.onPointerUp);
    on('pointercancel', this.onPointerUp);
    on('pointerleave', this.onPointerLeave);
    on('wheel', this.onWheel, { passive: false });

    // S-Pen / M-Pen yan düğmesi ve uzun basış, tarayıcının sağ tık menüsünü açar.
    on('contextmenu', (e) => e.preventDefault());
    on('selectstart', (e) => e.preventDefault());
    on('dragstart', (e) => e.preventDefault());

    // iOS Safari: `touch-action: none` tek başına yetmez. touchstart/touchmove'da
    // preventDefault; büyüteç/metin seçimi, Scribble ve sistem kaydırmasının Apple
    // Pencil çizgisini ~yarım saniye sonra pointercancel ile kesmesini önler.
    on('touchstart', (e) => e.preventDefault(), { passive: false });
    on('touchmove', (e) => e.preventDefault(), { passive: false });
    // Safari'nin kendi pinch-zoom (gesture*) olayları — sayfanın yakınlaşmasını engelle.
    for (const type of ['gesturestart', 'gesturechange', 'gestureend']) {
      const prevent = (e: Event) => e.preventDefault();
      vp.addEventListener(type, prevent, { passive: false });
      this.cleanups.push(() => vp.removeEventListener(type, prevent));
    }
  }

  private observeLayout(): void {
    const ro = new ResizeObserver(() => this.measure());
    ro.observe(this.el.viewport);
    // content'in yerleşim yüksekliği (offsetHeight) transform'dan etkilenmez.
    ro.observe(this.el.content);
    this.cleanups.push(() => ro.disconnect());

    const onScroll = () => {
      this.rect = null;
    };
    window.addEventListener('scroll', onScroll, true);
    this.cleanups.push(() => window.removeEventListener('scroll', onScroll, true));

    // devicePixelRatio değişimi (tarayıcı zoom'u, ekranlar arası pencere taşıma).
    let mq: MediaQueryList | null = null;
    const onDprChange = () => {
      this.measure();
      watchDpr();
    };
    const watchDpr = () => {
      mq?.removeEventListener('change', onDprChange);
      mq = window.matchMedia(`(resolution: ${window.devicePixelRatio}dppx)`);
      mq.addEventListener('change', onDprChange);
    };
    watchDpr();
    this.cleanups.push(() => mq?.removeEventListener('change', onDprChange));
  }

  // ───────────────────────────── Pointer olayları ─────────────────────────────

  private onPointerDown = (e: PointerEvent): void => {
    this.rect = null;
    if (e.pointerType === 'touch') {
      this.onTouchDown(e);
      return;
    }

    if (e.pointerType === 'pen') {
      this.markPenActivity();
      // Kalem ekrana değdi: süren parmak hareketini (avuç içi olabilir) iptal et.
      this.cancelTouchInteraction();
    }

    if (e.pointerType === 'mouse' && e.button === 1) {
      e.preventDefault();
      this.capture(e);
      this.gesture = { type: 'mouse-pan', pointerId: e.pointerId, startX: e.clientX, startY: e.clientY, startView: { ...this.view } };
      return;
    }
    if (e.pointerType === 'mouse' && e.button !== 0 && e.button !== 2) return;
    if (this.active) return; // aynı anda tek çizgi

    e.preventDefault();
    this.capture(e);
    const sticky = e.pointerType === 'pen' && this.hoverBarrelLatched();
    if (sticky) this.setTemporaryEraser(true);
    this.beginStroke(e, sticky ? 'eraser' : this.resolveTool(e), sticky);
  };

  private onPointerMove = (e: PointerEvent): void => {
    if (e.pointerType === 'touch') {
      this.onTouchMove(e);
      return;
    }
    if (e.pointerType === 'pen') this.markPenActivity();

    if (this.gesture?.type === 'mouse-pan' && this.gesture.pointerId === e.pointerId) {
      const g = this.gesture;
      this.view = { ...g.startView, panX: g.startView.panX + e.clientX - g.startX, panY: g.startView.panY + e.clientY - g.startY };
      this.applyView();
      return;
    }

    const active = this.active;
    if (!active || active.pointerId !== e.pointerId) {
      // Hover (Apple Pencil hover, S-Pen Air view, fare): silgi imlecini ve
      // "yan düğme basılı" göstergesini güncelle.
      // Havada asla silinmez; düğme basılıysa yalnızca gösterge ve silgi imleci açılır.
      if (e.pointerType === 'pen') {
        if (isHoverBarrel(e)) this.hoverBarrelAt = performance.now();
        this.setTemporaryEraser(isEraserButton(e) || this.hoverBarrelLatched());
      }
      this.hoverPoint = this.effectiveTool() === 'eraser' ? this.toDoc(e.clientX, e.clientY) : null;
      this.dirtyLive = true;
      this.requestRender();
      return;
    }

    // Çizgi ortasında yan düğmeye basıldı/bırakıldı → mevcut çizgiyi bitir,
    // aynı noktadan yeni araçla devam et.
    const tool = active.stickyEraser ? 'eraser' : this.resolveTool(e);
    if (tool !== active.tool) {
      this.endStroke();
      this.beginStroke(e, tool);
      return;
    }

    for (const ev of coalesced(e)) this.addPoint(ev);
    this.requestRender();
  };

  private onPointerUp = (e: PointerEvent): void => {
    if (e.pointerType === 'touch') {
      this.onTouchUp(e);
      return;
    }
    if (this.gesture?.type === 'mouse-pan' && this.gesture.pointerId === e.pointerId) {
      this.gesture = null;
      return;
    }
    if (this.active && this.active.pointerId === e.pointerId) {
      // pointercancel'da da çizgiyi kaybetmek yerine o ana kadarını kaydet.
      this.endStroke();
    }
    if (e.pointerType === 'pen') {
      this.markPenActivity();
      // Düğme hâlâ basılıysa kalem kalkınca gelen hover olayları mandalı yeniden kurar.
      this.hoverBarrelAt = -Infinity;
      this.setTemporaryEraser(isEraserButton(e));
    } else {
      this.setTemporaryEraser(false);
    }
  };

  private onPointerLeave = (e: PointerEvent): void => {
    if (e.pointerType === 'touch' || this.active) return;
    this.hoverPoint = null;
    if (e.pointerType === 'pen') {
      this.hoverBarrelAt = -Infinity;
      this.setTemporaryEraser(false);
    }
    this.dirtyLive = true;
    this.requestRender();
  };

  private onWheel = (e: WheelEvent): void => {
    e.preventDefault();
    const unit = e.deltaMode === 1 ? 16 : e.deltaMode === 2 ? this.vh : 1;
    const r = this.viewportRect();
    if (e.ctrlKey || e.metaKey) {
      // Trackpad pinch, Chrome/Firefox'ta ctrlKey'li wheel olarak gelir.
      this.zoomAt(e.clientX - r.left, e.clientY - r.top, this.view.zoom * Math.exp(-e.deltaY * unit * 0.01));
    } else {
      this.view = { ...this.view, panX: this.view.panX - e.deltaX * unit, panY: this.view.panY - e.deltaY * unit };
      this.applyView();
    }
  };

  // ───────────────────────────── Dokunma: avuç içi reddi + jestler ─────────────────────────────

  private onTouchDown(e: PointerEvent): void {
    // Avuç içi reddi: kalem ekrandayken ya da az önce kullanıldıysa (hover dahil)
    // gelen dokunuşlar tamamen yok sayılır.
    if (this.isPenBusy()) return;

    const pos = this.toLocal(e.clientX, e.clientY);
    this.touches.set(e.pointerId, pos);

    // Yedek mod: kalemini 'touch' olarak bildiren cihazlar için tek parmakla çizim.
    if (this.allowTouchDrawing && this.touches.size === 1 && !this.active) {
      this.capture(e);
      this.beginStroke(e, this.settings.tool);
      return;
    }
    // İkinci parmak geldi: parmakla çizilen yarım çizgiyi at, yakınlaştırmaya geç.
    if (this.active?.pointerType === 'touch') this.abortStroke();
    this.startGesture();
  }

  private onTouchMove(e: PointerEvent): void {
    if (!this.touches.has(e.pointerId)) return;
    this.touches.set(e.pointerId, this.toLocal(e.clientX, e.clientY));

    if (this.active?.pointerType === 'touch' && this.active.pointerId === e.pointerId) {
      for (const ev of coalesced(e)) this.addPoint(ev);
      this.requestRender();
      return;
    }
    this.updateGesture();
  }

  private onTouchUp(e: PointerEvent): void {
    if (!this.touches.delete(e.pointerId)) return;

    if (this.active?.pointerType === 'touch' && this.active.pointerId === e.pointerId) {
      this.endStroke();
      return;
    }

    const g = this.gesture;
    if (g?.type === 'pinch') {
      // İki parmakla kısa, hareketsiz dokunuş → Geri Al (Goodnotes/Notability alışkanlığı).
      if (!g.moved && performance.now() - g.startTime < TWO_FINGER_TAP_MS) {
        this.undo();
        this.gesture = { type: 'idle' };
        return;
      }
    }
    if (this.touches.size === 0) {
      this.gesture = null;
    } else if (g?.type !== 'idle') {
      this.startGesture(); // kalan parmaklarla kesintisiz devam (yeni referans noktası)
    }
  }

  private startGesture(): void {
    const pts = [...this.touches.values()];
    if (pts.length === 1) {
      this.gesture = { type: 'pan', startX: pts[0].x, startY: pts[0].y, startView: { ...this.view } };
    } else if (pts.length >= 2) {
      const [a, b] = pts;
      this.gesture = {
        type: 'pinch',
        startDist: Math.max(1, Math.hypot(b.x - a.x, b.y - a.y)),
        startMid: { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 },
        startView: { ...this.view },
        startTime: performance.now(),
        moved: false,
      };
    }
  }

  private updateGesture(): void {
    const g = this.gesture;
    const pts = [...this.touches.values()];
    if (!g || pts.length === 0) return;

    if (g.type === 'pan') {
      const p = pts[0];
      this.view = { ...g.startView, panX: g.startView.panX + p.x - g.startX, panY: g.startView.panY + p.y - g.startY };
      this.applyView();
    } else if (g.type === 'pinch' && pts.length >= 2) {
      const [a, b] = pts;
      const dist = Math.hypot(b.x - a.x, b.y - a.y);
      const midX = (a.x + b.x) / 2;
      const midY = (a.y + b.y) / 2;
      if (Math.abs(dist - g.startDist) > TAP_SLOP_PX || Math.hypot(midX - g.startMid.x, midY - g.startMid.y) > TAP_SLOP_PX) {
        g.moved = true;
      }
      // Başlangıçta iki parmağın ortasındaki doküman noktası, parmakların yeni ortasına sabitlenir.
      const zoom = clamp(g.startView.zoom * (dist / g.startDist), MIN_ZOOM, MAX_ZOOM);
      const s0 = this.fitScale * g.startView.zoom;
      const s1 = this.fitScale * zoom;
      const docX = (g.startMid.x - g.startView.panX) / s0;
      const docY = (g.startMid.y - g.startView.panY) / s0;
      this.view = { zoom, panX: midX - docX * s1, panY: midY - docY * s1 };
      this.applyView();
    }
  }

  private cancelTouchInteraction(): void {
    if (this.active?.pointerType === 'touch') this.abortStroke();
    this.touches.clear();
    this.gesture = this.gesture?.type === 'mouse-pan' ? this.gesture : null;
  }

  private isPenBusy(): boolean {
    return this.active?.pointerType === 'pen' || performance.now() - this.lastPenActivity < PALM_GUARD_MS;
  }

  private markPenActivity(): void {
    this.lastPenActivity = performance.now();
    if (!this.penDetected) {
      this.penDetected = true;
      this.emitSnapshot();
    }
  }

  // ───────────────────────────── Çizgi yaşam döngüsü ─────────────────────────────

  private effectiveTool(): DrawTool {
    return this.temporaryEraser ? 'eraser' : this.settings.tool;
  }

  /** Olaydaki düğme durumuna göre aracı belirler ve geçici silgi göstergesini günceller. */
  private resolveTool(e: PointerEvent): DrawTool {
    const eraser = isEraserButton(e);
    this.setTemporaryEraser(eraser);
    return eraser ? 'eraser' : this.settings.tool;
  }

  private hoverBarrelLatched(): boolean {
    return performance.now() - this.hoverBarrelAt < HOVER_BARREL_LATCH_MS;
  }

  private setTemporaryEraser(on: boolean): void {
    if (this.temporaryEraser === on) return;
    this.temporaryEraser = on;
    this.emitSnapshot();
  }

  private beginStroke(e: PointerEvent, tool: DrawTool, stickyEraser = false): void {
    const base = { pointerId: e.pointerId, pointerType: e.pointerType, tool, stickyEraser };
    if (tool === 'eraser' && this.settings.eraserMode === 'stroke') {
      this.active = { ...base, mode: 'stroke-erase', removed: [], last: null };
    } else {
      const kind: StrokeKind = tool === 'pen' ? 'pen' : tool === 'highlighter' ? 'highlighter' : 'erase';
      const s = this.settings;
      this.active = {
        ...base,
        mode: 'draw',
        drawnUpTo: 0,
        stroke: {
          id: makeId(),
          seq: ++this.seq,
          kind,
          color: kind === 'pen' ? s.penColor : kind === 'highlighter' ? s.highlighterColor : '#000',
          size: kind === 'pen' ? s.penSize : kind === 'highlighter' ? s.highlighterSize : s.eraserSize,
          points: [],
        },
      };
      // Canlı fosforlu da altındaki nota multiply ile binsin.
      this.el.liveCanvas.style.mixBlendMode = kind === 'highlighter' ? 'multiply' : 'normal';
    }
    this.hoverPoint = null;
    this.addPoint(e);
    this.dirtyLive = true;
    this.requestRender();
  }

  private addPoint(e: PointerEvent): void {
    const a = this.active;
    if (!a) return;
    const { x, y } = this.toDoc(e.clientX, e.clientY);
    const scale = this.scale;

    if (a.mode === 'stroke-erase') {
      const radius = this.settings.eraserSize / 2;
      // Hızlı harekette aradaki noktaları da test et (silgi çizgileri atlamasın).
      const from = a.last ?? { x, y };
      const steps = Math.max(1, Math.ceil(Math.hypot(x - from.x, y - from.y) / (radius * 0.5)));
      for (let i = 1; i <= steps; i++) {
        this.eraseAt(from.x + ((x - from.x) * i) / steps, from.y + ((y - from.y) * i) / steps, radius, a.removed);
      }
      a.last = { x, y };
      this.hoverPoint = { x, y };
      this.dirtyLive = true;
      return;
    }

    const pts = a.stroke.points;
    const last = pts[pts.length - 1];
    // ~0.6 ekran pikselinden yakın noktaları at (gürültü + JSON boyutu).
    if (last && Math.hypot(x - last.x, y - last.y) < 0.6 / scale) return;

    let p = readPressure(e, last?.p);
    if (last) p = last.p * 0.35 + p * 0.65; // basınç titremesini yumuşat
    pts.push({ x: round(x, 2), y: round(y, 2), p: round(p, 3) });

    if (a.stroke.kind === 'erase') {
      // Piksel silgi: kalıcı katmanlar bu izle birlikte yeniden çizilir.
      this.hoverPoint = { x, y };
      this.dirtyCommitted = true;
      this.dirtyLive = true;
    } else if (a.stroke.kind === 'highlighter') {
      this.dirtyLive = true; // tek yol olarak her karede baştan çizilir
    }
    // pen: render() artımlı olarak yalnızca yeni segmentleri çizer.
  }

  private eraseAt(x: number, y: number, radius: number, removed: Stroke[]): void {
    let changed = false;
    this.strokes = this.strokes.filter((s) => {
      if (s.kind === 'erase' || !strokeHit(s, x, y, radius)) return true;
      removed.push(s);
      changed = true;
      return false;
    });
    if (changed) this.dirtyCommitted = true;
  }

  private endStroke(): void {
    const a = this.active;
    if (!a) return;
    this.active = null;

    if (a.mode === 'stroke-erase') {
      if (a.removed.length > 0) {
        this.history.push({ kind: 'remove', strokes: a.removed });
        this.notifyDocumentChange();
      }
    } else if (a.stroke.points.length > 0) {
      cacheStrokeBBox(a.stroke);
      this.strokes.push(a.stroke);
      this.history.push({ kind: 'add', strokes: [a.stroke] });
      if (a.stroke.kind === 'erase') this.dirtyCommitted = true;
      else this.pendingCommits.push(a.stroke); // tam yeniden çizim yerine yalnızca bunu çiz
      this.notifyDocumentChange();
    }
    this.el.liveCanvas.style.mixBlendMode = 'normal';
    this.dirtyLive = true;
    this.requestRender();
    this.emitSnapshot();
  }

  /** Çizgiyi kaydetmeden at (ör. parmakla çizerken ikinci parmak geldi). */
  private abortStroke(): void {
    const a = this.active;
    if (!a) return;
    this.active = null;
    if (a.mode === 'stroke-erase' && a.removed.length > 0) {
      this.strokes = [...this.strokes, ...a.removed].sort((x, y) => x.seq - y.seq);
    }
    this.el.liveCanvas.style.mixBlendMode = 'normal';
    this.dirtyCommitted = true;
    this.dirtyLive = true;
    this.requestRender();
  }

  private finishActiveStroke(): void {
    if (this.active) this.endStroke();
  }

  private replaceStrokes(next: Stroke[]): void {
    this.strokes = next;
    this.dirtyCommitted = true;
    this.requestRender();
    this.notifyDocumentChange();
    this.emitSnapshot();
  }

  // ───────────────────────────── Görünüm (zoom/pan) ─────────────────────────────

  private get scale(): number {
    return this.fitScale * this.view.zoom;
  }

  private get margin(): number {
    return this.vw < 640 ? 8 : 24;
  }

  private zoomAt(sx: number, sy: number, zoom: number): void {
    const z = clamp(zoom, MIN_ZOOM, MAX_ZOOM);
    const s0 = this.scale;
    const s1 = this.fitScale * z;
    const docX = (sx - this.view.panX) / s0;
    const docY = (sy - this.view.panY) / s0;
    this.view = { zoom: z, panX: sx - docX * s1, panY: sy - docY * s1 };
    this.applyView();
  }

  private clampView(): void {
    const s = this.scale;
    const m = this.margin;
    const pageW = this.docWidth * s;
    const pageH = this.docHeight * s;
    const panX =
      pageW <= this.vw - 2 * m ? (this.vw - pageW) / 2 : clamp(this.view.panX, this.vw - pageW - m, m);
    const yA = m;
    const yB = this.vh - pageH - m;
    const panY = clamp(this.view.panY, Math.min(yA, yB), Math.max(yA, yB));
    this.view = { ...this.view, panX, panY };
  }

  private applyView(): void {
    this.clampView();
    const { panX, panY } = this.view;
    this.el.content.style.transform = `translate(${panX}px, ${panY}px) scale(${this.scale})`;
    this.dirtyCommitted = true;
    this.dirtyLive = true;
    this.requestRender();
    // Kaydırma her karede olur; UI'ı yalnızca zoom değişince güncelle.
    if (Math.abs(this.view.zoom - this.emittedZoom) > 0.001) this.emitSnapshot();
  }

  /** Viewport ve DPR'ye göre canvas arka belleklerini yeniden boyutlandırır (bulanıklığı önler). */
  private measure(): void {
    const r = this.el.viewport.getBoundingClientRect();
    this.rect = r;
    const prevVw = this.vw;
    const prevScale = this.scale;
    // Yeniden boyutlandırma öncesi üst-ortadaki doküman noktasını koru.
    const anchorDocX = prevVw ? (prevVw / 2 - this.view.panX) / prevScale : 0;
    const anchorDocY = prevVw ? -this.view.panY / prevScale : 0;

    this.vw = r.width;
    this.vh = r.height;
    this.dpr = window.devicePixelRatio || 1;
    this.docHeight = Math.max(1, this.el.content.offsetHeight);

    for (const c of [this.el.highlightCanvas, this.el.inkCanvas, this.el.liveCanvas]) {
      const w = Math.max(1, Math.round(r.width * this.dpr));
      const h = Math.max(1, Math.round(r.height * this.dpr));
      if (c.width !== w || c.height !== h) {
        c.width = w;
        c.height = h;
      }
      c.style.width = `${r.width}px`;
      c.style.height = `${r.height}px`;
    }

    // Sayfa genişliğe sığar; geniş ekranlarda okunur bir azami genişlikle sınırlanır.
    this.fitScale = Math.max(0.05, Math.min(r.width - this.margin * 2, 1100) / this.docWidth);

    if (!this.initialized && r.width > 0) {
      this.initialized = true;
      this.resetView();
      return;
    }
    if (prevVw) {
      const s = this.scale;
      this.view = { ...this.view, panX: this.vw / 2 - anchorDocX * s, panY: -anchorDocY * s };
    }
    this.applyView();
  }

  // ───────────────────────────── Çizim döngüsü ─────────────────────────────

  private requestRender(): void {
    if (this.rafId) return;
    this.rafId = requestAnimationFrame(() => {
      this.rafId = 0;
      this.render();
    });
  }

  private applyTransform(ctx: CanvasRenderingContext2D): void {
    const s = this.scale * this.dpr;
    ctx.setTransform(s, 0, 0, s, this.view.panX * this.dpr, this.view.panY * this.dpr);
  }

  private visibleDocRect(): BBox {
    const s = this.scale;
    return {
      minX: -this.view.panX / s,
      minY: -this.view.panY / s,
      maxX: (this.vw - this.view.panX) / s,
      maxY: (this.vh - this.view.panY) / s,
    };
  }

  private render(): void {
    if (this.dirtyCommitted) {
      this.dirtyCommitted = false;
      this.pendingCommits = [];
      this.renderCommitted();
    } else if (this.pendingCommits.length > 0) {
      this.applyTransform(this.inkCtx);
      this.applyTransform(this.hlCtx);
      for (const s of this.pendingCommits) drawCommittedStroke(s, this.inkCtx, this.hlCtx);
      this.pendingCommits = [];
    }
    this.renderLive();
  }

  private renderCommitted(): void {
    for (const ctx of [this.inkCtx, this.hlCtx]) {
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
      this.applyTransform(ctx);
    }
    const visible = this.visibleDocRect();
    const a = this.active;
    const list = a?.mode === 'draw' && a.stroke.kind === 'erase' ? [...this.strokes, a.stroke] : this.strokes;
    for (const s of list) {
      if (!bboxIntersects(strokeBBox(s), visible)) continue; // ekran dışını atla
      drawCommittedStroke(s, this.inkCtx, this.hlCtx);
    }
  }

  private renderLive(): void {
    const ctx = this.liveCtx;
    const a = this.active;
    const incrementalPen = a?.mode === 'draw' && a.stroke.kind === 'pen' && !this.dirtyLive;

    if (!incrementalPen) {
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
      if (a?.mode === 'draw') a.drawnUpTo = 0;
    }
    this.dirtyLive = false;
    this.applyTransform(ctx);

    if (a?.mode === 'draw') {
      if (a.stroke.kind === 'pen') {
        a.drawnUpTo = drawPenStroke(ctx, a.stroke, a.drawnUpTo, false);
        if (a.stroke.points.length === 1) {
          // Tek noktalık dokunuşu da hemen göster.
          ctx.beginPath();
          const p = a.stroke.points[0];
          ctx.arc(p.x, p.y, (a.stroke.size * 0.6) / 2, 0, Math.PI * 2);
          ctx.fillStyle = a.stroke.color;
          ctx.fill();
        }
      } else if (a.stroke.kind === 'highlighter') {
        drawUniformStroke(ctx, a.stroke);
      }
    }

    const cursor = this.hoverPoint;
    if (cursor && (a?.tool === 'eraser' || (!a && this.effectiveTool() === 'eraser'))) {
      drawEraserCursor(ctx, cursor.x, cursor.y, this.settings.eraserSize / 2, this.scale);
    }
  }

  // ───────────────────────────── Yardımcılar ─────────────────────────────

  private viewportRect(): DOMRect {
    if (!this.rect) this.rect = this.el.viewport.getBoundingClientRect();
    return this.rect;
  }

  private toLocal(clientX: number, clientY: number): { x: number; y: number } {
    const r = this.viewportRect();
    return { x: clientX - r.left, y: clientY - r.top };
  }

  private toDoc(clientX: number, clientY: number): { x: number; y: number } {
    const { x, y } = this.toLocal(clientX, clientY);
    const s = this.scale;
    return { x: (x - this.view.panX) / s, y: (y - this.view.panY) / s };
  }

  private capture(e: PointerEvent): void {
    try {
      this.el.viewport.setPointerCapture(e.pointerId);
    } catch {
      /* bazı WebView'larda desteklenmiyor; olaylar yine de viewport'a gelir */
    }
  }

  private notifyDocumentChange(): void {
    this.opts.onDocumentChange?.(this.getDocument());
  }

  private emitSnapshot(): void {
    this.emittedZoom = this.view.zoom;
    this.opts.onSnapshot?.({
      settings: this.settings,
      activeTool: this.effectiveTool(),
      temporaryEraser: this.temporaryEraser,
      canUndo: this.history.canUndo,
      canRedo: this.history.canRedo,
      zoom: this.view.zoom,
      penDetected: this.penDetected,
      allowTouchDrawing: this.allowTouchDrawing,
      strokeCount: this.strokes.length,
    });
  }
}

function getContext(canvas: HTMLCanvasElement, lowLatency: boolean): CanvasRenderingContext2D {
  // desynchronized: Chrome/Android'de düşük gecikmeli çizim (kalem ucu ile çizgi arası boşluk azalır).
  // Yalnızca bir ipucudur; mix-blend-mode kullanan fosforlu katmanında kapalı tutulur.
  const ctx = canvas.getContext('2d', { desynchronized: lowLatency }) ?? canvas.getContext('2d');
  if (!ctx) throw new Error('Canvas 2D bağlamı oluşturulamadı');
  return ctx;
}

function clamp(v: number, min: number, max: number): number {
  return Math.min(max, Math.max(min, v));
}

function round(v: number, digits: number): number {
  const k = 10 ** digits;
  return Math.round(v * k) / k;
}
