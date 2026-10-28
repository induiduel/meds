import React from 'react';
import { Lock } from 'lucide-react';
import { linkClick, navigateTo, pathFor } from '../../router';
import '../../styles/v15/ek15.css';

/**
 * Yönetici tarafından kapatılmış içerik (site ayarı görünürlük: ders/kurul/deste/sesli/paket/önem…) adresle açılınca.
 * Karar: services/siteAyar.ts::icerikGizli; sunucu da 403 { icerikKapali: true } döner.
 */
export default function IcerikKapaliV15({ ne = 'Bu içerik', geri }: { ne?: string; geri?: { yol: string; etiket: string } }) {
  const hedef = geri || { yol: pathFor('today'), etiket: "Bugün'e dön" };
  return (
    <div className="nf15 v15-card" role="main" aria-labelledby="ik15-b">
      <Lock className="nf15-ik" aria-hidden />
      <h1 id="ik15-b">{ne} şu an kapalı</h1>
      <p className="v15-cap">Bu içerik geçici olarak yayından kaldırıldı. Hazır olduğunda yeniden açılacak; başka bir ders ya da konuyla devam edebilirsin.</p>
      <a className="v15-btn nf15-don" href={hedef.yol} onClick={linkClick(() => navigateTo(hedef.yol))}>{hedef.etiket}</a>
    </div>
  );
}
