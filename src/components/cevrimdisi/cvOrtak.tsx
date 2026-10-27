/**
 * Çevrimdışı sayfası (v15) ortak parçaları: onaylı sil düğmesi, ses/PDF seçim çipi, üyenin açılacak adresi, durum adları.
 */
import { useEffect, useState } from 'react';
import { FileText, Headphones, Trash2, VolumeX } from 'lucide-react';
import { paketSil, secimDegistir, type Paket, type Secim } from '../../services/cevrimdisi/paketMotoru';
import { boyutYaz, type BirimDurum } from '../../services/cevrimdisi/dersBirimleri';

export const DURUM_AD: Record<BirimDurum, string> = {
  tam: 'Cihazda', kismi: 'Kısmen cihazda', yok: 'İndirilmedi', iniyor: 'İniyor', guncelleme: 'Güncelleme var', hata: 'Yarıda kaldı',
};
export const DURUM_TON: Record<BirimDurum, string> = { tam: 'is-ok', kismi: 'is-a', yok: '', iniyor: 'is-a', guncelleme: 'is-w', hata: 'is-b' };

export const sureYaz = (sn: number) => {
  if (!isFinite(sn) || sn <= 0) return '';
  if (sn < 60) return `${Math.ceil(sn)} sn`;
  if (sn < 3600) return `${Math.ceil(sn / 60)} dk`;
  return `${Math.floor(sn / 3600)} sa ${Math.ceil((sn % 3600) / 60)} dk`;
};

/** Üyenin ilgili sayfası: indirildikten sonra internetsiz açılarak kullanılır */
export function uyeAdresi(p: Paket): string | null {
  const [m, a, b] = p.id.split(':');
  if (m === 'sesli') return `/canliders/${a}`;
  if (m === 'ogren') return `/ogren/${a}`;
  if (m === 'cozucu') return `/soru-cozucu?brans=${a}&ders=${b}`;
  if (m === 'onem') return `/en-onemliler?brans=${a}&ders=${b}`;
  if (m === 'alt') return `/alternatif-cozucu?ders=${a}`;
  return null;
}

/** İki dokunuşla silme: ilk dokunuş onay sorar, 3,5 sn içinde ikinci dokunuş siler */
export function OnayliSil({ ids, etiket = 'Sil', soru, ikon = false, ad }: { ids: string[]; etiket?: string; soru?: string; ikon?: boolean; ad?: string }) {
  const [onay, setOnay] = useState(false);
  useEffect(() => {
    if (!onay) return;
    const t = window.setTimeout(() => setOnay(false), 3500);
    return () => window.clearTimeout(t);
  }, [onay]);
  if (!ids.length) return null;
  const metin = onay ? soru || (ids.length > 1 ? `${ids.length} paket silinsin mi?` : 'Silinsin mi?') : etiket;
  return (
    <button type="button" className={`cv15-b is-sil${onay ? ' is-onay' : ''}${ikon && !onay ? ' is-ikon' : ''}`}
      aria-label={ad ? `${ad}: ${onay ? 'silmeyi onayla' : 'cihazdan sil'}` : undefined}
      onClick={() => (onay ? (setOnay(false), void paketSil(ids)) : setOnay(true))}>
      <Trash2 aria-hidden /> {(!ikon || onay) && <span>{metin}</span>}
    </button>
  );
}

/** Ses / PDF parçası aç-kapa: indirilmişse kaldırmak anında yer açar, eklemek eksik dosyaları indirir */
export function EkCip({ p, tur, secim }: { p: Paket; tur: 'ses' | 'pdf'; secim: Secim }) {
  const e = p.ek?.[tur];
  if (!e) return null;
  const acik = secim[tur];
  const ad = tur === 'ses' ? 'Ses' : 'PDF';
  const Ik = tur === 'ses' ? (acik ? Headphones : VolumeX) : FileText;
  return (
    <button type="button" className={`cv15-cip${acik ? ' is-on' : ''}`} aria-pressed={acik}
      title={acik ? `${ad} dahil (${boyutYaz(e.b)}). Kaldırmak için dokun.` : `${ad} dahil değil. Eklemek için dokun (+${boyutYaz(e.b)}).`}
      aria-label={`${p.baslik}: ${ad.toLocaleLowerCase('tr-TR')} ${acik ? 'dahil, kaldır' : 'dahil değil, ekle'} (${boyutYaz(e.b)})`}
      onClick={() => void secimDegistir([p.id], { [tur]: !acik })}>
      <Ik aria-hidden /> {acik ? ad : tur === 'ses' ? 'Sessiz' : 'PDF yok'}
    </button>
  );
}
