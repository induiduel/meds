import React from 'react';
import { Rozet, type Ton } from './Rozet';

export type GorunurlukDegeri = 'acik' | 'gizli' | 'yalniz-yonetici';
export const GORUNURLUK_ETIKET: Record<GorunurlukDegeri, string> = { acik: 'Açık', gizli: 'Gizli', 'yalniz-yonetici': 'Yalnız yönetici' };
const TON: Record<GorunurlukDegeri, Ton> = { acik: 'iyi', gizli: 'kotu', 'yalniz-yonetici': 'uyari' };

export const GorunurlukRozeti: React.FC<{ deger?: string }> = ({ deger = 'acik' }) => (
  <Rozet ton={TON[deger as GorunurlukDegeri] || 'notr'}>{GORUNURLUK_ETIKET[deger as GorunurlukDegeri] || deger}</Rozet>
);

/**
 * H320: görünürlük TEK yerde düzenlenir: Site › Görünürlük (Sayfalar / İçerik sekmeleri). Eski satır içi `GorunurlukSecici`
 * kaldırıldı; içerik görünürlüğü yazımı yalnız sayfalar/SiteGorunurluk.tsx içindedir (PUT /api/admin/site-ayar {gorunurluk}).
 * Diğer sayfalar yalnız rozet + bu bağlantıyı gösterir. Anahtar biçimi `<tür>:<kimlik>` (ders:k2-07, sesli:<key>, deste:<id>,
 * paket:<key>, onem|asistan|cozucu:<dizin>/<kod>, kurul:2).
 */
export const gorunurlukYolu = (anahtar: string) => `site/gorunurluk?sekme=icerik&q=${encodeURIComponent(anahtar)}`;

/** H320: rozet + "Değiştir" bağlantısı. git verilmezse adres değiştirilip popstate ile panel kabuğu yönlendirilir. */
export const GorunurlukBaglantisi: React.FC<{ anahtar: string; deger?: string; git?: (yol: string) => void }> = ({ anahtar, deger, git }) => {
  const yol = gorunurlukYolu(anahtar);
  return (
    <span className="m16-gor-bag" style={{ display: 'inline-flex', alignItems: 'center', gap: 8, flexWrap: 'wrap' }}>
      <GorunurlukRozeti deger={deger} />
      <a href={`/manage/${yol}`} title={`${anahtar} görünürlüğünü Site › Görünürlük sayfasında değiştir`}
        onClick={(e) => {
          if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
          e.preventDefault();
          e.stopPropagation();
          if (git) git(yol);
          else { window.history.pushState(window.history.state, '', `/manage/${yol}`); window.dispatchEvent(new PopStateEvent('popstate')); }
        }}>Değiştir</a>
    </span>
  );
};
