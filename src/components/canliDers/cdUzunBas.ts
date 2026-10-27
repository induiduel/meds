/**
 * H06 · Sesli derste cümleye uzun basma (≥450 ms, dokunmatik + fare): basılan cümle seçilir; seçim araç çubuğu
 * (utils/selectionShare + CanliDersDers.useCdSecimCubugu: Nota ekle · Spot yap · Kart · Açıkla · Kopyala) selectionchange
 * ile kendiliğinden açılır. Uzun basmanın ardından gelen tıklama (cümleye atlama) yutulur; kısa dokunuş eskisi gibi çalışır.
 * Yalnız metin bölmesindeki `.cd-p` paragraflarında çalışır; çizim katmanına (kural 18) dokunmaz.
 */
import { useEffect, type RefObject } from 'react';

const SURE = 450;
const KAYMA = 8;

function noktadakiKonum(x: number, y: number): { node: Node; offset: number } | null {
  const d = document as Document & { caretPositionFromPoint?: (x: number, y: number) => { offsetNode: Node; offset: number } | null; caretRangeFromPoint?: (x: number, y: number) => Range | null };
  if (d.caretPositionFromPoint) { const p = d.caretPositionFromPoint(x, y); return p ? { node: p.offsetNode, offset: p.offset } : null; }
  if (d.caretRangeFromPoint) { const r = d.caretRangeFromPoint(x, y); return r ? { node: r.startContainer, offset: r.startOffset } : null; }
  return null;
}

/** Paragraf içinde (metin düğümleri boyunca) karakter konumundan Range kurar */
function aralik(p: HTMLElement, bas: number, son: number): Range | null {
  const w = document.createTreeWalker(p, NodeFilter.SHOW_TEXT);
  let n = 0; let r: Range | null = null;
  for (let t = w.nextNode() as Text | null; t; t = w.nextNode() as Text | null) {
    const L = t.data.length;
    if (!r && bas <= n + L) { r = document.createRange(); r.setStart(t, Math.max(0, bas - n)); }
    if (r && son <= n + L) { r.setEnd(t, Math.max(0, son - n)); return r; }
    n += L;
  }
  return r;
}

/** Basılan noktanın cümlesini seçer; başarılıysa true */
export function cumleSec(p: HTMLElement, x: number, y: number): boolean {
  const k = noktadakiKonum(x, y);
  if (!k || !p.contains(k.node)) return false;
  const pre = document.createRange();
  pre.setStart(p, 0);
  pre.setEnd(k.node, k.offset);
  const konum = pre.toString().length;
  const metin = p.textContent || '';
  // Cümle sınırı: . ! ? … ve ardından boşluk (kısaltmalardaki noktayı da bölebilir; seçim tutamaçla genişletilebilir)
  let bas = 0;
  for (let i = Math.min(konum, metin.length) - 1; i > 0; i--) { if (/[.!?…]/.test(metin[i - 1]) && /\s/.test(metin[i])) { bas = i + 1; break; } }
  let son = metin.length;
  const m = /[.!?…](?=\s|$)/g; m.lastIndex = Math.max(konum, bas);
  const e = m.exec(metin); if (e) son = e.index + 1;
  while (bas < son && /\s/.test(metin[bas])) bas++;
  if (son - bas < 2) return false;
  const r = aralik(p, bas, son);
  if (!r) return false;
  const s = window.getSelection();
  if (!s) return false;
  s.removeAllRanges();
  s.addRange(r);
  return true;
}

export function useUzunBasSecim(paneRef: RefObject<HTMLElement | null>) {
  useEffect(() => {
    const pane = paneRef.current;
    if (!pane) return;
    let zaman = 0; let x0 = 0; let y0 = 0; let hedef: HTMLElement | null = null; let yut = 0;
    const iptal = () => { window.clearTimeout(zaman); zaman = 0; hedef = null; };
    const down = (e: PointerEvent) => {
      if (e.button !== 0 || e.isPrimary === false) return;
      const p = (e.target as Element | null)?.closest?.<HTMLElement>('.cd-p');
      if (!p || !pane.contains(p)) return;
      iptal();
      hedef = p; x0 = e.clientX; y0 = e.clientY;
      zaman = window.setTimeout(() => {
        const h = hedef; zaman = 0;
        if (h && cumleSec(h, x0, y0)) {
          yut = Date.now() + 900;
          try { navigator.vibrate?.(12); } catch { /* yok */ }
        }
      }, SURE);
    };
    const move = (e: PointerEvent) => { if (zaman && Math.hypot(e.clientX - x0, e.clientY - y0) > KAYMA) iptal(); };
    const up = () => { if (zaman) iptal(); };
    const click = (e: MouseEvent) => { if (Date.now() < yut) { e.preventDefault(); e.stopPropagation(); yut = 0; } };
    const menu = (e: Event) => { if (Date.now() < yut || zaman) e.preventDefault(); };
    pane.addEventListener('pointerdown', down);
    pane.addEventListener('pointermove', move, { passive: true });
    pane.addEventListener('pointerup', up);
    pane.addEventListener('pointercancel', iptal);
    pane.addEventListener('click', click, true);
    pane.addEventListener('contextmenu', menu);
    return () => {
      iptal();
      pane.removeEventListener('pointerdown', down);
      pane.removeEventListener('pointermove', move);
      pane.removeEventListener('pointerup', up);
      pane.removeEventListener('pointercancel', iptal);
      pane.removeEventListener('click', click, true);
      pane.removeEventListener('contextmenu', menu);
    };
  }, [paneRef]);
}
