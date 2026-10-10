import type { Stroke, StrokePoint } from '../types';
import { widthForPressure } from './geometry';

/**
 * Çizgi çizim yardımcıları. Hepsi doküman koordinatlarında çalışır; görünüm
 * dönüşümü (yakınlaştırma/kaydırma × devicePixelRatio) önceden ctx.setTransform
 * ile kurulmuş olmalıdır.
 *
 * Yumuşatma: noktalar düz çizgiyle değil, ardışık orta noktalar arasında
 * quadraticCurveTo ile bağlanır (orta nokta yumuşatması).
 */

const mid = (a: StrokePoint, b: StrokePoint) => ({ x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 });

/**
 * Basınçlı kalem: her segment kendi kalınlığıyla ayrı çizilir. Opak renkte
 * üst üste binen yuvarlak uçlar görünmez, bu yüzden değişken kalınlık kesintisiz görünür.
 *
 * Artımlı çizim için `from` indeksinden itibaren yalnızca yeni segmentleri çizer
 * ve bir sonraki çağrıda kullanılacak indeksi döner. `finish` false iken son yarım
 * segment (kuyruk) çizilmez; o, çizgi tamamlanınca kalıcı katmana çizilir.
 */
export function drawPenStroke(ctx: CanvasRenderingContext2D, stroke: Stroke, from = 0, finish = true): number {
  const pts = stroke.points;
  const n = pts.length;
  if (n === 0) return 0;
  ctx.strokeStyle = stroke.color;
  ctx.fillStyle = stroke.color;
  ctx.lineCap = 'round';
  ctx.lineJoin = 'round';

  const w = (pt: StrokePoint) => widthForPressure('pen', stroke.size, pt.p);

  if (n === 1) {
    if (finish) {
      ctx.beginPath();
      ctx.arc(pts[0].x, pts[0].y, w(pts[0]) / 2, 0, Math.PI * 2);
      ctx.fill();
    }
    return 0;
  }

  // Segment 0: ilk noktadan ilk orta noktaya düz çizgi.
  if (from === 0) {
    const m = mid(pts[0], pts[1]);
    ctx.beginPath();
    ctx.lineWidth = w(pts[0]);
    ctx.moveTo(pts[0].x, pts[0].y);
    ctx.lineTo(m.x, m.y);
    ctx.stroke();
    from = 1;
  }

  // Segment i (1..n-2): orta(i-1,i) → orta(i,i+1), kontrol noktası pts[i].
  let i = from;
  for (; i <= n - 2; i++) {
    const a = mid(pts[i - 1], pts[i]);
    const b = mid(pts[i], pts[i + 1]);
    ctx.beginPath();
    ctx.lineWidth = w(pts[i]);
    ctx.moveTo(a.x, a.y);
    ctx.quadraticCurveTo(pts[i].x, pts[i].y, b.x, b.y);
    ctx.stroke();
  }

  if (finish) {
    const a = mid(pts[n - 2], pts[n - 1]);
    ctx.beginPath();
    ctx.lineWidth = w(pts[n - 1]);
    ctx.moveTo(a.x, a.y);
    ctx.lineTo(pts[n - 1].x, pts[n - 1].y);
    ctx.stroke();
  }
  return i;
}

/**
 * Sabit kalınlıklı tek yol (fosforlu kalem ve piksel silgi).
 * Tek bir stroke() çağrısı olduğu için yol kendi üstüne binse de koyulaşmaz —
 * multiply modunda fosforlunun "lekelenmemesi" için bu şart.
 */
export function drawUniformStroke(ctx: CanvasRenderingContext2D, stroke: Stroke): void {
  const pts = stroke.points;
  if (pts.length === 0) return;
  ctx.strokeStyle = stroke.color;
  ctx.fillStyle = stroke.color;
  ctx.lineWidth = stroke.size;
  ctx.lineCap = 'round';
  ctx.lineJoin = 'round';
  ctx.beginPath();
  if (pts.length === 1) {
    ctx.arc(pts[0].x, pts[0].y, stroke.size / 2, 0, Math.PI * 2);
    ctx.fill();
    return;
  }
  ctx.moveTo(pts[0].x, pts[0].y);
  for (let i = 1; i < pts.length - 1; i++) {
    const m = mid(pts[i], pts[i + 1]);
    ctx.quadraticCurveTo(pts[i].x, pts[i].y, m.x, m.y);
  }
  const last = pts[pts.length - 1];
  ctx.lineTo(last.x, last.y);
  ctx.stroke();
}

/** Kalıcı katmanlarda bir çizgiyi türüne uygun karışım moduyla çizer. */
export function drawCommittedStroke(
  stroke: Stroke,
  ink: CanvasRenderingContext2D,
  highlight: CanvasRenderingContext2D,
): void {
  switch (stroke.kind) {
    case 'pen':
      ink.globalCompositeOperation = 'source-over';
      drawPenStroke(ink, stroke);
      break;
    case 'highlighter':
      // Katman içi multiply: üst üste fosforlular gerçek kalem gibi koyulaşır.
      // Altındaki nota karşı multiply ise canvas'ın CSS mix-blend-mode'u ile sağlanır.
      highlight.globalCompositeOperation = 'multiply';
      drawUniformStroke(highlight, stroke);
      break;
    case 'erase':
      // Piksel silgi her iki katmandan da siler; sıra korunduğu için yalnızca
      // kendinden önceki çizgileri etkiler.
      ink.globalCompositeOperation = 'destination-out';
      highlight.globalCompositeOperation = 'destination-out';
      drawUniformStroke(ink, { ...stroke, color: '#000' });
      drawUniformStroke(highlight, { ...stroke, color: '#000' });
      break;
  }
  ink.globalCompositeOperation = 'source-over';
  highlight.globalCompositeOperation = 'source-over';
}

/** Silgi imleci (canlı katmanda). */
export function drawEraserCursor(ctx: CanvasRenderingContext2D, x: number, y: number, radius: number, scale: number): void {
  ctx.beginPath();
  ctx.arc(x, y, radius, 0, Math.PI * 2);
  ctx.lineWidth = 1.5 / scale;
  ctx.strokeStyle = 'rgba(15, 23, 42, 0.55)';
  ctx.fillStyle = 'rgba(255, 255, 255, 0.35)';
  ctx.fill();
  ctx.stroke();
}
