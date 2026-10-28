import React from 'react';
import { AlertCircle, Inbox, Loader2, Lock } from 'lucide-react';

/** Boş liste / bulunamadı */
export const BosDurum: React.FC<{ baslik?: string; aciklama?: React.ReactNode; ikon?: React.ReactNode; eylem?: React.ReactNode }> = ({ baslik = 'Kayıt yok', aciklama, ikon, eylem }) => (
  <div className="m16-durum" role="status">
    <span className="m16-durum-ikon">{ikon || <Inbox aria-hidden="true" />}</span>
    <strong>{baslik}</strong>
    {aciklama && <p>{aciklama}</p>}
    {eylem}
  </div>
);

/** Yükleniyor: satir verilirse iskelet satırları, yoksa dönen simge */
export const Yukleniyor: React.FC<{ metin?: string; satir?: number }> = ({ metin = 'Yükleniyor…', satir }) =>
  satir ? (
    <div className="m16-iskelet" aria-busy="true" aria-label={metin}>
      {Array.from({ length: satir }, (_, i) => <span key={i} style={{ width: `${70 + ((i * 37) % 30)}%` }} />)}
    </div>
  ) : (
    <div className="m16-durum" role="status" aria-live="polite"><Loader2 className="m16-don" aria-hidden="true" /><span>{metin}</span></div>
  );

/** Hata: 401/403 ise yetki yok görünümü */
export const Hata: React.FC<{ hata: unknown; yenile?: () => void }> = ({ hata, yenile }) => {
  const durum = (hata as any)?.durum;
  const yetki = durum === 401 || durum === 403;
  return (
    <div className="m16-durum m16-durum-hata" role="alert">
      <span className="m16-durum-ikon">{yetki ? <Lock aria-hidden="true" /> : <AlertCircle aria-hidden="true" />}</span>
      <strong>{yetki ? 'Yetki yok' : 'Bir sorun oluştu'}</strong>
      <p>{yetki ? 'Bu işlem yönetici oturumu ister.' : String((hata as any)?.message || hata)}</p>
      {yenile && <button type="button" className="m16-btn" onClick={yenile}>Yeniden dene</button>}
    </div>
  );
};
