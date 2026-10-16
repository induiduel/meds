import React from 'react';
import './ders-isci-asama.css';

/**
 * Ders işçisi ilerleme şeridi: bir dersin Drive'dan canlı derse kadar hangi aşamada olduğu.
 * Kaynak → İçerik (k/11 çıktı) → Denetim → Konuşma metni → Onay → Yayın → Emel sesi → EMA sesi.
 * İşçi aşamaları taslak özetindeki `asama` alanından (scripts/ders_isci/api.py::asama), ses aşamaları sesli anlatım
 * durumundan (/api/sesli-anlatim: ders varyantları + kuyruk işleri) türetilir.
 */
export type TaslakAsama = {
  kaynak: boolean;
  cikti: number;
  cikti_toplam: number;
  eksik?: string[];
  denetim: number | null;
  ana_bitti: boolean;
  konusma: { metin: boolean; sayfalar: boolean; durum?: string };
  son_dosya?: { ad: string; zaman: number } | null;
};
/** /api/sesli-anlatim'den bu derse ait özet (bileşen dışında süzülür). */
export type SesDurumu = {
  varyantlar: { saglayici: string; metinGuncel?: boolean }[];
  isler: { saglayici: string; durum: string; ilerleme?: { bitti: number; toplam: number } }[];
} | null;

type Adim = { ad: string; durum: 'tamam' | 'suruyor' | 'bekliyor' | 'hata' | 'atla'; not?: string };

const dk = (t?: number) => (t ? `${Math.max(0, Math.round((Date.now() / 1000 - t) / 60))} dk önce` : '');

function sesAdimi(ad: string, saglayici: string, ses: SesDurumu, yayinda: boolean): Adim {
  if (!yayinda) return { ad, durum: 'bekliyor' };
  const is = ses?.isler.find((x) => x.saglayici === saglayici);
  if (is) {
    const p = is.ilerleme?.toplam ? Math.round((100 * is.ilerleme.bitti) / is.ilerleme.toplam) : 0;
    if (is.durum === 'hata') return { ad, durum: 'hata', not: 'hata' };
    return { ad, durum: 'suruyor', not: is.durum === 'calisiyor' ? `%${p}` : 'sırada' };
  }
  const v = ses?.varyantlar.find((x) => x.saglayici === saglayici);
  if (v) return { ad, durum: v.metinGuncel === false ? 'hata' : 'tamam', not: v.metinGuncel === false ? 'metin değişti' : undefined };
  return { ad, durum: 'bekliyor', not: ses ? 'iş yok' : undefined };
}

export const AsamaSeridi: React.FC<{
  a?: TaslakAsama;
  isleniyor: boolean;
  durum?: string;
  karar?: string;
  yayin?: string;
  ses: SesDurumu;
}> = ({ a, isleniyor, durum, karar, yayin, ses }) => {
  if (!a) return null;
  const yayinda = yayin === 'yayinlandi' || durum === 'yayinlandi';
  const k = a.konusma || { metin: false, sayfalar: false };
  const adimlar: Adim[] = [
    { ad: 'Kaynak', durum: a.kaynak ? 'tamam' : isleniyor ? 'suruyor' : 'bekliyor' },
    {
      ad: 'İçerik',
      durum: a.cikti >= a.cikti_toplam ? 'tamam' : isleniyor && a.kaynak ? 'suruyor' : 'bekliyor',
      not: `${a.cikti}/${a.cikti_toplam}`,
    },
    {
      ad: 'Denetim',
      durum: a.denetim === 0 || a.ana_bitti ? 'tamam' : a.denetim != null ? (isleniyor ? 'suruyor' : 'hata') : 'bekliyor',
      not: a.denetim ? `${a.denetim} hata${isleniyor ? ', düzeltiliyor' : ''}` : undefined,
    },
    {
      ad: 'Konuşma metni',
      durum:
        k.durum === 'tamam' ? 'tamam' : k.durum === 'hata' ? 'hata' : k.durum === 'kapali' ? 'atla' : a.ana_bitti && isleniyor ? 'suruyor' : k.metin ? 'suruyor' : 'bekliyor',
      not: k.durum === 'kapali' ? 'kapalı' : k.durum === 'hata' ? 'denetimde hata' : undefined,
    },
    {
      ad: 'Onay',
      durum: karar === 'onayla' ? 'tamam' : karar === 'reddet' ? 'hata' : durum === 'onay_bekliyor' ? 'suruyor' : 'bekliyor',
      not: durum === 'onay_bekliyor' && !karar ? 'seni bekliyor' : karar === 'duzelt' ? 'düzeltme' : undefined,
    },
    {
      ad: 'Yayın',
      durum: yayinda ? 'tamam' : yayin === 'denetim_hatasi' ? 'hata' : karar === 'onayla' ? 'suruyor' : 'bekliyor',
      not: karar === 'onayla' && !yayinda && yayin !== 'denetim_hatasi' ? '≤10 dk' : undefined,
    },
    sesAdimi('Emel', 'edge-emel', ses, yayinda),
    sesAdimi('EMA', 'ema-yerel', ses, yayinda),
  ];
  const suren = adimlar.find((x) => x.durum === 'suruyor');
  return (
    <div className="di-asama" aria-label={`İlerleme${suren ? `: ${suren.ad} sürüyor` : ''}`}>
      <ol>
        {adimlar.map((x) => (
          <li key={x.ad} className={`is-${x.durum}`} title={x.not ? `${x.ad}: ${x.not}` : x.ad}>
            <i aria-hidden />
            <span>
              {x.ad}
              {x.not && <small> · {x.not}</small>}
            </span>
          </li>
        ))}
      </ol>
      {isleniyor && a.son_dosya && (
        <small className="di-asama-son">
          Son yazılan: {a.son_dosya.ad} ({dk(a.son_dosya.zaman)})
          {a.cikti < a.cikti_toplam && a.eksik?.length ? ` · sırada: ${a.eksik.join(', ')}` : ''}
        </small>
      )}
    </div>
  );
};
