/**
 * ?kurul=N süzgeci (Geçmiş kurullar bağlantıları): parametre yoksa ekran bugünkü gibi tüm içeriği gösterir;
 * varsa yalnız o kurulun içeriği + üstte "Kurul N · tümünü göster" hapı. Stil: styles/kurul-suzgec.css (.kh-*).
 */
import { icKonum, icUrl } from '../../siteHaritasi';
import React, { useEffect, useState } from 'react';
import { X } from 'lucide-react';
import { navigateTo } from '../../router';
import '../../styles/kurul-suzgec.css';

/** URL'deki ?kurul=N (1–6); yoksa null. */
export function kurulParam(search: string = typeof location !== 'undefined' ? icKonum().search : ''): number | null {
  try {
    const n = Number(new URLSearchParams(search).get('kurul'));
    return Number.isInteger(n) && n >= 1 && n <= 6 ? n : null;
  } catch { return null; }
}

/** ?kurul= izleyen kanca: "tümünü göster" ya da geri/ileri ile değişince ekran yeniden süzülür. */
export function useKurulParam(): number | null {
  const [k, setK] = useState(() => kurulParam());
  useEffect(() => {
    const f = () => setK(kurulParam());
    window.addEventListener('popstate', f);
    return () => window.removeEventListener('popstate', f);
  }, []);
  return k;
}

/** Kimlikten kurul: "k2-07…", "k2noroloji" → 2; önek yoksa (eski Kurul 1 adları: patoloji, enfeksiyon…) 1. */
export function kurulKimlikten(id: string | undefined | null): number {
  const m = /^k(\d)(?![\d])/.exec(String(id || '').trim().toLowerCase());
  return m ? Number(m[1]) : 1;
}

/** ?kurul= parametresini URL'den kaldırır (hash ve diğer parametreler korunur) ve ekranı yeniden kurar. */
export function kurulSuzgeciniKaldir() {
  const p = new URLSearchParams(icKonum().search);
  p.delete('kurul');
  const q = p.toString();
  navigateTo(`${icKonum().pathname}${q ? `?${q}` : ''}${location.hash}`);
}

export const KurulHapi: React.FC<{ kurul: number; sayi?: number; className?: string; onTumu?: () => void }> = ({ kurul, sayi, className, onTumu }) => (
  <div className={`kh${className ? ` ${className}` : ''}`} role="status">
    <span className="kh-ad">Kurul {kurul}{typeof sayi === 'number' && <small> · {sayi}</small>}</span>
    <button type="button" className="kh-tumu" onClick={onTumu || kurulSuzgeciniKaldir}>
      tümünü göster <X aria-hidden />
    </button>
  </div>
);

/** Süzgeç açıkken içerik yoksa gösterilen boş durum. */
export const KurulBos: React.FC<{ kurul: number; ne: string; onTumu?: () => void }> = ({ kurul, ne, onTumu }) => (
  <div className="kh-bos">
    <b>Kurul {kurul} için henüz {ne} yok</b>
    <p>Bu kurulun içeriği hazırlandıkça burada görünecek.</p>
    <button type="button" className="kh-tumu" onClick={onTumu || kurulSuzgeciniKaldir}>Tüm kurulları göster</button>
  </div>
);
