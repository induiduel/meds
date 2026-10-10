import type { Stroke, StrokeKind } from '../types';

export interface BBox {
  minX: number;
  minY: number;
  maxX: number;
  maxY: number;
}

// Çizgiler değişmez (immutable) olduğundan sınır kutusu bir kez hesaplanıp önbelleğe alınır.
const bboxCache = new WeakMap<Stroke, BBox>();

export function strokeBBox(stroke: Stroke): BBox {
  const cached = bboxCache.get(stroke);
  if (cached) return cached;
  let minX = Infinity;
  let minY = Infinity;
  let maxX = -Infinity;
  let maxY = -Infinity;
  for (const pt of stroke.points) {
    if (pt.x < minX) minX = pt.x;
    if (pt.y < minY) minY = pt.y;
    if (pt.x > maxX) maxX = pt.x;
    if (pt.y > maxY) maxY = pt.y;
  }
  const pad = stroke.size / 2 + 1;
  return { minX: minX - pad, minY: minY - pad, maxX: maxX + pad, maxY: maxY + pad };
}

/** Tamamlanmış çizgiler için çağrılır; canlı çizgi büyüdüğünden önbelleğe alınmaz. */
export function cacheStrokeBBox(stroke: Stroke): BBox {
  bboxCache.delete(stroke);
  const box = strokeBBox(stroke);
  bboxCache.set(stroke, box);
  return box;
}

export function bboxIntersects(a: BBox, b: BBox): boolean {
  return a.minX <= b.maxX && a.maxX >= b.minX && a.minY <= b.maxY && a.maxY >= b.minY;
}

function distToSegmentSq(px: number, py: number, ax: number, ay: number, bx: number, by: number): number {
  const dx = bx - ax;
  const dy = by - ay;
  const lenSq = dx * dx + dy * dy;
  let t = lenSq === 0 ? 0 : ((px - ax) * dx + (py - ay) * dy) / lenSq;
  t = Math.max(0, Math.min(1, t));
  const cx = ax + t * dx - px;
  const cy = ay + t * dy - py;
  return cx * cx + cy * cy;
}

/** Nesne silgisi için isabet testi: (x, y) merkezli `radius` yarıçaplı daire çizgiye değiyor mu? */
export function strokeHit(stroke: Stroke, x: number, y: number, radius: number): boolean {
  const box = strokeBBox(stroke);
  if (x < box.minX - radius || x > box.maxX + radius || y < box.minY - radius || y > box.maxY + radius) {
    return false;
  }
  const reach = radius + stroke.size / 2;
  const reachSq = reach * reach;
  const pts = stroke.points;
  if (pts.length === 1) {
    const dx = pts[0].x - x;
    const dy = pts[0].y - y;
    return dx * dx + dy * dy <= reachSq;
  }
  for (let i = 1; i < pts.length; i++) {
    if (distToSegmentSq(x, y, pts[i - 1].x, pts[i - 1].y, pts[i].x, pts[i].y) <= reachSq) return true;
  }
  return false;
}

/**
 * Basınç → kalınlık eğrisi.
 * - Kalem: hafif dokunuş ince, bastırınca kalın (gamma eğrisiyle doğal his).
 * - Fosforlu ve silgi: sabit kalınlık (gerçek fosforlu kalem gibi).
 */
export function widthForPressure(kind: StrokeKind, size: number, pressure: number): number {
  if (kind !== 'pen') return size;
  const curved = Math.pow(Math.max(0, Math.min(1, pressure)), 0.75);
  return size * (0.25 + 0.85 * curved);
}
