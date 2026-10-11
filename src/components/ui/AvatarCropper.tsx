import React, { useEffect, useRef, useState } from 'react';
import { RotateCcw, ZoomIn, ZoomOut } from 'lucide-react';
import { Dialog } from './Dialog';

const OUT = 256; // çıktı kenarı (px): profil fotoğrafı ~15–30 KB JPEG olur

/**
 * Profil fotoğrafı kırpıcı: görseli sürükle, kaydırıcı / tekerlek / iki parmakla yakınlaştır.
 * Daire maske önizlemesi; çıktı 256×256 JPEG data URL.
 */
export const AvatarCropper: React.FC<{ file: File; onCancel: () => void; onDone: (dataUrl: string) => void }> = ({ file, onCancel, onDone }) => {
  const [src, setSrc] = useState<string | null>(null);
  const [nat, setNat] = useState<{ w: number; h: number } | null>(null);
  const [zoom, setZoom] = useState(1);
  const [pos, setPos] = useState({ x: 0, y: 0 });
  const [busy, setBusy] = useState(false);
  const boxRef = useRef<HTMLDivElement>(null);
  const imgRef = useRef<HTMLImageElement>(null);
  const drag = useRef<{ id: number; x: number; y: number; px: number; py: number } | null>(null);
  const pointers = useRef(new Map<number, { x: number; y: number }>());
  const pinch = useRef<{ d: number; z: number } | null>(null);

  useEffect(() => {
    const url = URL.createObjectURL(file);
    setSrc(url);
    return () => URL.revokeObjectURL(url);
  }, [file]);

  // Kutuyu dolduran taban ölçek: kısa kenar kutuya oturur
  const box = boxRef.current?.clientWidth || 300;
  const base = nat ? box / Math.min(nat.w, nat.h) : 1;
  const scale = base * zoom;

  const clamp = (p: { x: number; y: number }, z = zoom) => {
    if (!nat) return p;
    const s = base * z;
    const mx = Math.max(0, (nat.w * s - box) / 2);
    const my = Math.max(0, (nat.h * s - box) / 2);
    return { x: Math.min(mx, Math.max(-mx, p.x)), y: Math.min(my, Math.max(-my, p.y)) };
  };
  const setZoomClamped = (z: number) => {
    const nz = Math.min(4, Math.max(1, z));
    setZoom(nz);
    setPos((p) => clamp(p, nz));
  };

  const onDown = (e: React.PointerEvent) => {
    (e.currentTarget as HTMLElement).setPointerCapture(e.pointerId);
    pointers.current.set(e.pointerId, { x: e.clientX, y: e.clientY });
    if (pointers.current.size === 2) {
      const [a, b] = [...pointers.current.values()];
      pinch.current = { d: Math.hypot(a.x - b.x, a.y - b.y), z: zoom };
      drag.current = null;
    } else {
      drag.current = { id: e.pointerId, x: e.clientX, y: e.clientY, px: pos.x, py: pos.y };
    }
  };
  const onMove = (e: React.PointerEvent) => {
    if (!pointers.current.has(e.pointerId)) return;
    pointers.current.set(e.pointerId, { x: e.clientX, y: e.clientY });
    if (pinch.current && pointers.current.size === 2) {
      const [a, b] = [...pointers.current.values()];
      setZoomClamped(pinch.current.z * (Math.hypot(a.x - b.x, a.y - b.y) / pinch.current.d));
      return;
    }
    const d = drag.current;
    if (d && d.id === e.pointerId) setPos(clamp({ x: d.px + e.clientX - d.x, y: d.py + e.clientY - d.y }));
  };
  const onUp = (e: React.PointerEvent) => {
    pointers.current.delete(e.pointerId);
    if (pointers.current.size < 2) pinch.current = null;
    if (drag.current?.id === e.pointerId) drag.current = null;
  };

  const save = () => {
    if (!nat || !imgRef.current) return;
    setBusy(true);
    const c = document.createElement('canvas');
    c.width = c.height = OUT;
    const ctx = c.getContext('2d')!;
    ctx.imageSmoothingQuality = 'high';
    // Kutudaki görünür kare → kaynak koordinatları
    const sw = box / scale;
    const sx = nat.w / 2 - pos.x / scale - sw / 2;
    const sy = nat.h / 2 - pos.y / scale - sw / 2;
    ctx.fillStyle = '#fff';
    ctx.fillRect(0, 0, OUT, OUT);
    ctx.drawImage(imgRef.current, sx, sy, sw, sw, 0, 0, OUT, OUT);
    onDone(c.toDataURL('image/jpeg', 0.86));
  };

  return (
    <Dialog
      title="Fotoğrafı kırp"
      subtitle="Sürükleyerek konumla, kaydırıcıyla yakınlaştır."
      onClose={onCancel}
      width="max-w-sm"
      footer={
        <div className="flex items-center justify-end gap-2 w-full">
          <button type="button" className="ui-btn is-ghost" onClick={onCancel}>Vazgeç</button>
          <button type="button" className={`ui-btn is-primary ${busy ? 'is-loading' : ''}`} disabled={!nat} onClick={save}>Kaydet</button>
        </div>
      }
    >
      <div className="flex flex-col gap-4 py-1">
        <div
          ref={boxRef}
          className="ui-crop"
          onPointerDown={onDown}
          onPointerMove={onMove}
          onPointerUp={onUp}
          onPointerCancel={onUp}
          onWheel={(e) => setZoomClamped(zoom * (e.deltaY < 0 ? 1.08 : 1 / 1.08))}
          role="img"
          aria-label="Kırpma alanı"
        >
          {src && (
            <img
              ref={imgRef}
              src={src}
              alt=""
              draggable={false}
              onLoad={(e) => setNat({ w: e.currentTarget.naturalWidth, h: e.currentTarget.naturalHeight })}
              style={nat ? { width: nat.w, height: nat.h, transform: `translate(-50%, -50%) translate(${pos.x}px, ${pos.y}px) scale(${scale})` } : { opacity: 0 }}
            />
          )}
          {!nat && <div className="ui-skel" style={{ position: 'absolute', inset: 0, borderRadius: 0 }} />}
        </div>
        <div className="flex items-center gap-2">
          <button type="button" className="ui-btn is-ghost is-sm" aria-label="Uzaklaştır" onClick={() => setZoomClamped(zoom / 1.15)}><ZoomOut /></button>
          <input
            type="range"
            className="ui-range"
            min={1}
            max={4}
            step={0.01}
            value={zoom}
            aria-label="Yakınlaştırma"
            onChange={(e) => setZoomClamped(Number(e.target.value))}
          />
          <button type="button" className="ui-btn is-ghost is-sm" aria-label="Yakınlaştır" onClick={() => setZoomClamped(zoom * 1.15)}><ZoomIn /></button>
          <button type="button" className="ui-btn is-ghost is-sm" aria-label="Sıfırla" onClick={() => { setZoom(1); setPos({ x: 0, y: 0 }); }}><RotateCcw /></button>
        </div>
      </div>
    </Dialog>
  );
};
