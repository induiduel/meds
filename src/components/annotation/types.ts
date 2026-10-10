/**
 * Not üzerine çizim (annotation) modülünün ortak tipleri.
 *
 * Koordinat sistemi: tüm çizgiler "doküman birimi" ile saklanır. Sayfa genişliği
 * her zaman `docWidth` (varsayılan 1000) birimdir; yükseklik içeriğin gerçek
 * yüksekliğidir. Böylece ekran boyutu, yakınlaştırma ya da cihaz değişse de
 * çizgiler notun aynı yerine oturur.
 */

/** Kullanıcının araç çubuğundan seçebildiği araçlar. */
export type DrawTool = 'pen' | 'highlighter' | 'eraser';

/**
 * stroke: dokunduğu çizgiyi bütünüyle siler (Goodnotes "nesne silgisi").
 * pixel: yalnızca geçtiği yeri siler (destination-out ile).
 */
export type EraserMode = 'stroke' | 'pixel';

/** Saklanan çizgi türü. `erase` = piksel silgi izi (yeniden çizimde sırasıyla uygulanır). */
export type StrokeKind = 'pen' | 'highlighter' | 'erase';

export interface StrokePoint {
  /** Doküman birimi cinsinden x. */
  x: number;
  /** Doküman birimi cinsinden y. */
  y: number;
  /** Normalize basınç (0–1). Fare/basınçsız kalemde 0.5. */
  p: number;
}

export interface Stroke {
  id: string;
  /** Oluşturulma sırası; geri al sonrası doğru katman sırasını korumak için. */
  seq: number;
  kind: StrokeKind;
  color: string;
  /** Doküman birimi cinsinden azami kalınlık. */
  size: number;
  points: StrokePoint[];
}

export interface ToolSettings {
  tool: DrawTool;
  penColor: string;
  penSize: number;
  highlighterColor: string;
  highlighterSize: number;
  eraserMode: EraserMode;
  eraserSize: number;
}

/** Motorun UI'a bildirdiği anlık durum. */
export interface EngineSnapshot {
  settings: ToolSettings;
  /** Şu an fiilen kullanılan araç (kalem düğmesi basılıysa 'eraser'). */
  activeTool: DrawTool;
  /** S-Pen / M-Pen yan düğmesi ya da kalemin silgi ucu ile geçici silgi açık mı? */
  temporaryEraser: boolean;
  canUndo: boolean;
  canRedo: boolean;
  zoom: number;
  /** Bu oturumda en az bir `pointerType === 'pen'` olayı görüldü mü? */
  penDetected: boolean;
  /** Kalemini 'touch' olarak raporlayan cihazlar için parmakla çizim yedeği. */
  allowTouchDrawing: boolean;
  strokeCount: number;
}

/** Kalıcı saklama / sunucuya gönderme biçimi. */
export interface AnnotationDocument {
  version: 1;
  docWidth: number;
  strokes: Stroke[];
}

export interface ViewState {
  zoom: number;
  panX: number;
  panY: number;
}
