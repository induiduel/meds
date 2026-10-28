import React, { useState } from 'react';
import { adminIstek } from './api';
import { Rozet, type Ton } from './Rozet';
import { bildir, yazimHedefi } from './Bildirim';
import { onayIste } from './Onay';

export type GorunurlukDegeri = 'acik' | 'gizli' | 'yalniz-yonetici';
const ETIKET: Record<GorunurlukDegeri, string> = { acik: 'Açık', gizli: 'Gizli', 'yalniz-yonetici': 'Yalnız yönetici' };
const TON: Record<GorunurlukDegeri, Ton> = { acik: 'iyi', gizli: 'kotu', 'yalniz-yonetici': 'uyari' };

export const GorunurlukRozeti: React.FC<{ deger?: string }> = ({ deger = 'acik' }) => (
  <Rozet ton={TON[deger as GorunurlukDegeri] || 'notr'}>{ETIKET[deger as GorunurlukDegeri] || deger}</Rozet>
);

/**
 * Site ayarı görünürlük haritasında tek anahtarı değiştirir (PUT /api/admin/site-ayar, denetime fark olarak düşer).
 * Anahtar biçimi `<tür>:<kimlik>` — ders:k2-07, deste:<id>, sesli:<key>, paket:<key>, onem:<dizin>/<kod>, kurul:2.
 * "Açık" seçilince anahtar silinir (derleme varsayılanı).
 */
export const GorunurlukSecici: React.FC<{ anahtar: string; deger?: string; degisti?: (v: GorunurlukDegeri) => void }> = ({ anahtar, deger = 'acik', degisti }) => {
  const [v, setV] = useState(deger);
  const [mesgul, setMesgul] = useState(false);
  React.useEffect(() => setV(deger), [deger]);
  // H141: gizleme onay ister (hedef sunucu yazılı), her değişiklik 8 sn geri alınabilir
  const yazDeger = async (y: GorunurlukDegeri) => {
    await adminIstek('/api/admin/site-ayar', { yontem: 'PUT', govde: { gorunurluk: { [anahtar]: y === 'acik' ? null : y } } });
    setV(y);
    degisti?.(y);
  };
  const sec = async (y: GorunurlukDegeri) => {
    if (y === v) return;
    if (y !== 'acik' && !(await onayIste({ baslik: `${ETIKET[y]} yapılsın mı?`, aciklama: `${anahtar} öğrencilerden ${yazimHedefi()} üzerinde hemen gizlenir. 8 saniye içinde geri alabilirsin.`, onayMetni: 'Uygula' }))) return;
    const once = v as GorunurlukDegeri;
    setMesgul(true);
    try {
      await yazDeger(y);
      bildir(`Görünürlük: ${ETIKET[y]}`, 'iyi', { etiket: 'Geri al', yap: () => { yazDeger(once).then(() => bildir('Geri alındı', 'iyi'), (e) => bildir(e?.message || 'Geri alınamadı', 'kotu')); } });
    } catch (e: any) {
      bildir(e?.message || 'Kaydedilemedi', 'kotu');
    } finally {
      setMesgul(false);
    }
  };
  return (
    <span className="m16-cip-grup" role="radiogroup" aria-label={`Görünürlük: ${anahtar}`}>
      {(Object.keys(ETIKET) as GorunurlukDegeri[]).map((k) => (
        <button key={k} type="button" role="radio" aria-checked={v === k} disabled={mesgul} className={`m16-cip ${v === k ? 'on' : ''}`} onClick={() => void sec(k)}>
          {ETIKET[k]}
        </button>
      ))}
    </span>
  );
};
