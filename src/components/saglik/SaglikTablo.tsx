import React, { useCallback, useEffect, useLayoutEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { Maximize2, Minus, Pin, PinOff, Plus, ScanLine, X } from 'lucide-react';
import { lockScroll, unlockScroll } from '../../utils/scrollLock';

/**
 * Tablo kabı: tablonun üstünde "Tam ekran" düğmesi. Tam ekranda tablo yakınlaştırılıp küçültülür (düğmeler, iki parmak,
 * Ctrl + tekerlek, + / − tuşları), "Sığdır" tabloyu ekran genişliğine oturtur, ilk sütun isteğe bağlı sabitlenir.
 * Sayfadaki tabloda ilk sütun kaydırmayla birlikte kayar (telefonda ekranın yarısını kaplamasın).
 */

const ENAZ = 0.3;
const ENCOK = 3;
const sinirla = (z: number) => Math.min(ENCOK, Math.max(ENAZ, Math.round(z * 100) / 100));

const TamEkran: React.FC<{ baslik: string; onClose: () => void; children: React.ReactNode }> = ({ baslik, onClose, children }) => {
  const [z, setZ] = useState(1);
  const [sabit, setSabit] = useState(false);
  const alan = useRef<HTMLDivElement>(null);
  const ic = useRef<HTMLDivElement>(null);
  const zRef = useRef(z);
  zRef.current = z;

  const sigdir = useCallback(() => {
    const a = alan.current, i = ic.current;
    if (!a || !i) return;
    const dogal = i.scrollWidth / (zRef.current || 1);
    if (dogal > 0) setZ(sinirla((a.clientWidth - 24) / dogal));
  }, []);

  useEffect(() => {
    lockScroll();
    // Alt sekme çubuğu (telefon) tam ekranın altından taşmasın
    document.documentElement.classList.add('sbk-tam-acik');
    const tus = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
      else if (e.key === '+' || e.key === '=') setZ((x) => sinirla(x + 0.1));
      else if (e.key === '-') setZ((x) => sinirla(x - 0.1));
      else if (e.key === '0') setZ(1);
    };
    document.addEventListener('keydown', tus);
    return () => { document.removeEventListener('keydown', tus); document.documentElement.classList.remove('sbk-tam-acik'); unlockScroll(); };
  }, [onClose]);

  // Açılışta tablo ekrandan genişse sığdır (telefonda tüm tablo bir bakışta; sonra büyütülür)
  useLayoutEffect(() => {
    const a = alan.current, i = ic.current;
    if (a && i && i.scrollWidth > a.clientWidth) sigdir();
  }, [sigdir]);

  // İki parmakla yakınlaştırma ve Ctrl + tekerlek (tarayıcının sayfa yakınlaştırması yerine tabloyu ölçekler)
  useEffect(() => {
    const a = alan.current;
    if (!a) return;
    let bas: { d: number; z: number } | null = null;
    const mesafe = (t: TouchList) => Math.hypot(t[0].clientX - t[1].clientX, t[0].clientY - t[1].clientY);
    const basla = (e: TouchEvent) => { if (e.touches.length === 2) bas = { d: mesafe(e.touches), z: zRef.current }; };
    const hareket = (e: TouchEvent) => {
      if (e.touches.length !== 2 || !bas) return;
      e.preventDefault();
      setZ(sinirla(bas.z * (mesafe(e.touches) / bas.d)));
    };
    const bitir = (e: TouchEvent) => { if (e.touches.length < 2) bas = null; };
    const teker = (e: WheelEvent) => {
      if (!e.ctrlKey && !e.metaKey) return;
      e.preventDefault();
      setZ((x) => sinirla(x * (e.deltaY < 0 ? 1.1 : 1 / 1.1)));
    };
    a.addEventListener('touchstart', basla, { passive: true });
    a.addEventListener('touchmove', hareket, { passive: false });
    a.addEventListener('touchend', bitir);
    a.addEventListener('wheel', teker, { passive: false });
    return () => {
      a.removeEventListener('touchstart', basla);
      a.removeEventListener('touchmove', hareket);
      a.removeEventListener('touchend', bitir);
      a.removeEventListener('wheel', teker);
    };
  }, []);

  return createPortal(
    <div className="sbk-tam" role="dialog" aria-modal="true" aria-label={`${baslik} — tam ekran`}>
      <header className="sbk-tam-u">
        <b className="sbk-tam-t">{baslik}</b>
        <div className="sbk-tam-arac" role="group" aria-label="Yakınlaştırma">
          <button type="button" onClick={() => setZ((x) => sinirla(x - 0.1))} disabled={z <= ENAZ} aria-label="Küçült" title="Küçült (−)"><Minus aria-hidden /></button>
          <button type="button" className="sbk-tam-yuzde" onClick={() => setZ(1)} title="Gerçek boyut (0)" aria-label={`Yakınlaştırma %${Math.round(z * 100)}, gerçek boyuta dön`}>%{Math.round(z * 100)}</button>
          <button type="button" onClick={() => setZ((x) => sinirla(x + 0.1))} disabled={z >= ENCOK} aria-label="Büyüt" title="Büyüt (+)"><Plus aria-hidden /></button>
          <button type="button" onClick={sigdir} title="Ekran genişliğine sığdır"><ScanLine aria-hidden /><span>Sığdır</span></button>
          <button type="button" onClick={() => setSabit((x) => !x)} aria-pressed={sabit} title="İlk sütunu sabitle">
            {sabit ? <PinOff aria-hidden /> : <Pin aria-hidden />}<span>İlk sütun</span>
          </button>
        </div>
        <button type="button" className="sbk-tam-kapat" onClick={onClose} aria-label="Tam ekranı kapat" title="Kapat (Esc)"><X aria-hidden /></button>
      </header>
      <div ref={alan} className={`sbk-tam-g ${sabit ? 'is-sabit' : ''}`}>
        <div ref={ic} className="sbk-tam-ic" style={{ zoom: z } as React.CSSProperties}>{children}</div>
      </div>
      <p className="sbk-tam-ipucu">İki parmakla ya da Ctrl + tekerlekle yakınlaştır · Esc ile kapat</p>
    </div>,
    document.body,
  );
};

export const TabloKabi: React.FC<{
  baslik?: string;
  /** Sayfada görünen içerik (verilmezse yalnız "Tam ekran" düğmesi görünür) */
  children?: React.ReactNode;
  /** Tam ekranda gösterilecek tablo (verilmezse children) */
  tamEkran?: React.ReactNode;
  dugmeMetni?: string;
}> = ({ baslik = 'Tablo', children, tamEkran, dugmeMetni = 'Tam ekran' }) => {
  const [acik, setAcik] = useState(false);
  const kapat = useCallback(() => setAcik(false), []);
  return (
    <div className="sbk-tk">
      <div className="sbk-tk-u">
        <button type="button" className="sbk-tk-b" onClick={() => setAcik(true)} title="Tabloyu tam ekranda aç; yakınlaştırıp küçültebilirsin">
          <Maximize2 aria-hidden /> {dugmeMetni}
        </button>
      </div>
      {children}
      {acik && <TamEkran baslik={baslik} onClose={kapat}>{tamEkran ?? children}</TamEkran>}
    </div>
  );
};
