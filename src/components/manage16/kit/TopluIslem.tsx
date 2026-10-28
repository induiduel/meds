import React from 'react';
import { X } from 'lucide-react';

/** Seçim varken görünen alt çubuk. eylemler: düğmeler (m16-btn) */
export const TopluIslem: React.FC<{ secili: number; temizle: () => void; children: React.ReactNode }> = ({ secili, temizle, children }) =>
  secili > 0 ? (
    <div className="m16-toplu" role="toolbar" aria-label="Toplu işlem">
      <span className="m16-toplu-say"><strong>{secili}</strong> seçili</span>
      <div className="m16-toplu-eylem">{children}</div>
      <button type="button" className="m16-btn hayalet ikon" onClick={temizle} aria-label="Seçimi temizle"><X aria-hidden="true" /></button>
    </div>
  ) : null;
