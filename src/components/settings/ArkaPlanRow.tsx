import React, { useEffect, useState } from 'react';
import { BellRing } from 'lucide-react';
import { pushAc, pushDurum, pushKapat, type PushDurum } from '../../services/arkaPlanPush';
import { toast } from '../ui/Toast';

const ALT: Record<PushDurum, string> = {
  acik: 'Açık — yorum yanıtları ve rapor sonuçları site kapalıyken de bu cihaza gelir',
  kapali: 'Site kapalıyken yanıt ve sonuç bildirimlerini bu cihaza gönder',
  engelli: 'Tarayıcı bildirim iznini engellemiş; site ayarlarından izin verin',
  desteklenmiyor: 'Bu tarayıcı arka plan bildirimini desteklemiyor (iPhone’da önce “Ana Ekrana Ekle”)',
};

/** Ayarlar · arka plan bildirimleri (Web Push) aç/kapa. */
export const ArkaPlanRow: React.FC = () => {
  const [d, setD] = useState<PushDurum | null>(null);
  const [mesgul, setMesgul] = useState(false);
  useEffect(() => { void pushDurum().then(setD); }, []);

  const degistir = async () => {
    setMesgul(true);
    try {
      const yeni = d === 'acik' ? await pushKapat() : await pushAc();
      setD(yeni);
      if (yeni === 'acik') toast.success('Arka plan bildirimleri açık', 'Site kapalıyken de bildirim alacaksınız.');
      else if (yeni === 'engelli') toast.info('İzin verilmedi', 'Tarayıcının site ayarlarından bildirime izin verebilirsiniz.');
    } catch (e: any) {
      toast.error('Bildirim ayarlanamadı', e?.message || 'Bir hata oluştu.');
    } finally {
      setMesgul(false);
    }
  };

  if (!d) return null;
  const acik = d === 'acik';
  return (
    <div className="ui-row has-icon">
      <span className="ui-ico" style={{ '--ico-bg': 'var(--color-accent)', '--ico-fg': 'var(--color-on-solid)' } as React.CSSProperties}>
        <BellRing strokeWidth={2.1} />
      </span>
      <span className="ui-row-main">
        <b>Arka plan bildirimleri</b>
        <span>{ALT[d]}</span>
      </span>
      {d !== 'desteklenmiyor' && d !== 'engelli' && (
        <button
          type="button"
          role="switch"
          aria-checked={acik}
          className={`ui-btn is-sm ${acik ? 'is-tonal' : 'is-primary'} ${mesgul ? 'is-loading' : ''}`}
          onClick={degistir}
          disabled={mesgul}
        >
          {acik ? 'Kapat' : 'Aç'}
        </button>
      )}
    </div>
  );
};
