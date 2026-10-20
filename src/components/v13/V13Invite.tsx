import React, { useEffect, useState } from 'react';
import { Check } from 'lucide-react';
import { Sheet } from '../ui/Sheet';
import { useAppearance } from '../../utils/appearance';
import '../../styles/v13/invite.css';

/**
 * Açılışta bir kez sorulan v13 daveti. Cevap görünüm kaydına yazılır (v13Asked) ve profil eşitlemesiyle diğer
 * cihazlara gider; bu yüzden her cihazda yeniden sorulmaz. Başka bir pencere açıkken (giriş uyarısı, tur, kayıt)
 * beklenir. Seçim sonradan Ayarlar › Tasarım'dan ya da telefonda Menü › Görünüm'den değişir.
 */
const V13Invite: React.FC = () => {
  const look = useAppearance();
  const [open, setOpen] = useState(false);
  const asked = look.v13Asked;

  useEffect(() => {
    if (asked) return;
    let tries = 0;
    let t = 0;
    const check = () => {
      // Başka bir iletişim kutusu açıksa onun kapanmasını bekle (en çok ~1 dk)
      if (document.querySelector('[role="dialog"], [aria-modal="true"]') && tries++ < 30) {
        t = window.setTimeout(check, 2000);
        return;
      }
      setOpen(true);
    };
    t = window.setTimeout(check, 1400);
    return () => window.clearTimeout(t);
  }, [asked]);

  if (asked && !open) return null;

  const answer = (use: boolean) => {
    setOpen(false);
    if (use) look.set({ choice: 'v13' });
    else look.set({ v13Asked: true });
  };

  return (
    <Sheet
      open={open}
      onClose={() => answer(false)}
      title="Yeni tasarım: Ada (v13)"
      subtitle="İstersen şimdi geç; istediğin an Ayarlar › Tasarım'dan geri dönersin."
      width={520}
      footer={
        <div className="a13i-foot">
          <button type="button" className="a13i-btn" onClick={() => answer(false)}>
            Şimdilik kalsın
          </button>
          <button type="button" className="a13i-btn is-primary" onClick={() => answer(true)} autoFocus>
            Ada'yı kullan
          </button>
        </div>
      }
    >
      <div className="a13i">
        <svg className="a13i-art" viewBox="0 0 320 150" role="img" aria-label="Ada tasarımının taslağı: solda yüzen menü adası, üstte başlık kapsülü, ortada içerik kartları">
          <rect x="1" y="1" width="318" height="148" rx="14" className="a13i-bg" />
          <rect x="10" y="10" width="30" height="130" rx="9" className="a13i-is" />
          <rect x="44" y="10" width="72" height="130" rx="9" className="a13i-is" />
          <rect x="17" y="18" width="16" height="16" rx="5" className="a13i-ac" />
          {[48, 66, 84, 102].map((y) => (
            <rect key={y} x="18" y={y} width="14" height="10" rx="3" className="a13i-ln" />
          ))}
          {[22, 36, 50, 64, 78].map((y, i) => (
            <rect key={y} x="50" y={y} width={i === 1 ? 60 : 50} height="9" rx="3" className={i === 1 ? 'a13i-acs' : 'a13i-ln'} />
          ))}
          <rect x="124" y="10" width="186" height="22" rx="8" className="a13i-is" />
          <rect x="132" y="17" width="54" height="8" rx="3" className="a13i-ink" />
          <rect x="124" y="40" width="186" height="46" rx="10" className="a13i-is" />
          <rect x="124" y="92" width="90" height="48" rx="10" className="a13i-is" />
          <rect x="220" y="92" width="90" height="48" rx="10" className="a13i-is" />
          <rect x="134" y="50" width="120" height="7" rx="3" className="a13i-ink" />
          <rect x="134" y="63" width="160" height="6" rx="3" className="a13i-ln" />
          <rect x="134" y="74" width="96" height="6" rx="3" className="a13i-ln" />
        </svg>
        <ul className="a13i-list">
          <li><Check aria-hidden="true" /><span><b>Daha sade ve kompakt.</b> Kenardan kenara şerit yok; menü, başlık ve alt çubuk yüzen “ada”lar.</span></li>
          <li><Check aria-hidden="true" /><span><b>Her sayfa en çok iki dokunuşta.</b> Menü niyetine göre: Ders çalış · Sınava hazırlan · Soru çöz · Başvuru · Sen.</span></li>
          <li><Check aria-hidden="true" /><span><b>Telefon ve tablete göre kuruldu.</b> Hiçbir şey ekran dışına taşmaz, yazılar her temada okunur.</span></li>
          <li><Check aria-hidden="true" /><span><b>İçerik ve işlevler aynı.</b> Yalnız iskelet değişir; Net (v12) tasarımı silinmez.</span></li>
        </ul>
      </div>
    </Sheet>
  );
};

export default V13Invite;
