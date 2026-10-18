/**
 * Konu takibi arayüz parçaları: "Bitirdim" / "Tekrar et" düğmeleri ve konuda harcanan süre + çözülen soru etiketi.
 * Sesli ders, Etkileşimli dersler, Soru çözücü, En önemliler ve Bitirdiklerim sayfası ortak kullanır. Veri:
 * services/calismaTakip.ts. Stil: styles/takip.css (.kt-*).
 */
import React from 'react';
import { Check, CircleCheck, RotateCcw, Timer } from 'lucide-react';
import {
  bitir, bitirmeyiGeriAl, bittiMi, sureYaz, tekrarBasla, useKonuKaydi, type TakipModul,
} from '../../services/calismaTakip';
import '../../styles/takip.css';

interface DugmeProps {
  modul: TakipModul;
  konu: string;
  /** konunun adı (ekran okuyucu etiketi) */
  ad: string;
  /** içerikten türetilen tamamlanma */
  turetilen?: boolean;
  /** "Tekrar et" sonrası: konuyu baştan aç (ilerlemeyi sıfırla, sesi başlat …) */
  onTekrar?: () => void;
  /** satır içi küçük sürüm */
  kucuk?: boolean;
  className?: string;
}

/** Bitmemiş konuda "Bitirdim"; bitmiş konuda "Bitti" (dokununca geri alınır) + "Tekrar et". */
export const KonuDugmeleri: React.FC<DugmeProps> = ({ modul, konu, ad, turetilen, onTekrar, kucuk, className }) => {
  const k = useKonuKaydi(modul, konu);
  const bitti = bittiMi(k, turetilen);
  const cls = `kt-dug${kucuk ? ' is-kucuk' : ''}${className ? ` ${className}` : ''}`;
  if (!bitti) {
    return (
      <span className={cls}>
        {k?.durum === 'tekrar' && <span className="kt-tur" title="Tekrar turundasın">{(k.tur || 1) + 1}. tur</span>}
        <button type="button" className="kt-btn is-bitir" onClick={(e) => { e.stopPropagation(); bitir(modul, konu); }}
          aria-label={`Bitirdim: ${ad}`} title="Bu konuyu bitirdim olarak işaretle">
          <CircleCheck aria-hidden /><span>Bitirdim</span>
        </button>
      </span>
    );
  }
  return (
    <span className={cls}>
      <button type="button" className="kt-btn is-bitti" aria-pressed="true" onClick={(e) => { e.stopPropagation(); bitirmeyiGeriAl(modul, konu); }}
        aria-label={`Bitti: ${ad}. İşareti kaldırmak için dokun`} title="Bitti — işareti kaldırmak için dokun">
        <Check aria-hidden /><span>Bitti</span>
      </button>
      <button type="button" className="kt-btn is-tekrar" onClick={(e) => { e.stopPropagation(); tekrarBasla(modul, konu); onTekrar?.(); }}
        aria-label={`Tekrar et: ${ad}`} title="Bu konuyu baştan yeniden çalış">
        <RotateCcw aria-hidden /><span>Tekrar et</span>
      </button>
    </span>
  );
};

/** Yalnız simge: sıkışık satırlar (Sesli ders) için yuvarlak işaret düğmesi. */
export const KonuIsaret: React.FC<Omit<DugmeProps, 'onTekrar' | 'kucuk'>> = ({ modul, konu, ad, turetilen, className }) => {
  const k = useKonuKaydi(modul, konu);
  const bitti = bittiMi(k, turetilen);
  return (
    <button type="button" className={`kt-isaret${bitti ? ' is-bitti' : ''}${className ? ` ${className}` : ''}`} aria-pressed={bitti}
      onClick={(e) => { e.stopPropagation(); bitti ? bitirmeyiGeriAl(modul, konu) : bitir(modul, konu); }}
      aria-label={bitti ? `Bitti: ${ad}. İşareti kaldır` : `Bitirdim: ${ad}`} title={bitti ? 'Bitti — işareti kaldır' : 'Bitirdim olarak işaretle'}>
      {bitti ? <Check aria-hidden /> : <CircleCheck aria-hidden />}
      <span className="kt-isaret-l" aria-hidden>{bitti ? 'Bitti' : 'Bitirdim'}</span>
    </button>
  );
};

/** "⏱ 12 dk · 8 soru" — konuda harcanan etkin süre ve çözülen soru (hiç yoksa çizilmez). */
export const KonuSureEtiketi: React.FC<{ modul: TakipModul; konu: string; ekSoru?: number; className?: string }> = ({ modul, konu, ekSoru = 0, className }) => {
  const k = useKonuKaydi(modul, konu);
  const soru = (k?.soru || 0) + ekSoru;
  if (!k?.sn && !soru) return null;
  return (
    <span className={`kt-sure${className ? ` ${className}` : ''}`} title="Bu konuda geçirdiğin etkin çalışma süresi">
      <Timer aria-hidden />
      <span>{k?.sn ? sureYaz(k.sn) : '0 dk'}</span>
      {soru > 0 && <span className="kt-sure-s">· {soru.toLocaleString('tr-TR')} soru</span>}
      {!!k?.tur && <span className="kt-sure-s">· {k.tur}× tekrar</span>}
    </span>
  );
};
