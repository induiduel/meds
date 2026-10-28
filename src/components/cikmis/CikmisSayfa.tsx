/**
 * Çıkmış sorular sayfa gezgini (H242): üstte konum ("41–60 / 502 · sayfa 3/26"), altta Önceki · sayfa seçimi · Sonraki.
 * Liste ve Panel yerleşiminde hem Kart hem Kompakt görünüm bu sayfalarla çizilir (eskiden Kart sonsuz kaydırmaydı).
 */
import React from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import '../../styles/v15/cikmis-sayfa.css';

export const CikmisSayfa: React.FC<{ sayfa: number; toplamSayfa: number; boy: number; toplam: number; git: (n: number) => void; ust?: boolean }> = ({ sayfa, toplamSayfa, boy, toplam, git, ust }) => {
  const bas = (sayfa - 1) * boy + 1;
  const son = Math.min(toplam, sayfa * boy);
  const konum = `${bas.toLocaleString('tr-TR')}–${son.toLocaleString('tr-TR')} / ${toplam.toLocaleString('tr-TR')} soru`;
  if (ust) return <p className="cs15-sayfa is-ust" aria-live="polite">{konum} · sayfa {sayfa}/{toplamSayfa}</p>;
  return (
    <nav className="cs15-sayfa" aria-label="Sayfalar">
      <button type="button" className="cs15-btn" onClick={() => git(sayfa - 1)} disabled={sayfa <= 1}><ChevronLeft aria-hidden /><span>Önceki</span></button>
      <label className="cs15-sec">
        <span className="sr-only">Sayfa seç</span>
        <select value={sayfa} onChange={(e) => git(Number(e.target.value))}>
          {Array.from({ length: toplamSayfa }, (_, i) => (
            <option key={i} value={i + 1}>Sayfa {i + 1} / {toplamSayfa}</option>
          ))}
        </select>
      </label>
      <button type="button" className="cs15-btn" onClick={() => git(sayfa + 1)} disabled={sayfa >= toplamSayfa}><span>Sonraki</span><ChevronRight aria-hidden /></button>
      <span className="cs15-konum">{konum}</span>
    </nav>
  );
};
