import React from 'react';
import { BILDIRIM_TURLERI, sessizSaatte, useBildirimTercih } from '../../services/bildirimTercih';
import { userNotificationService } from '../../services/userNotificationService';
import { useV15Baslik } from './baslik';
import '../../styles/v15/kronometre.css';
import '../../styles/v15/ek15.css';

/**
 * v15 · Bildirim tercihleri (tasarım AB06 bildirimTercih) — /bildirimler?gorunum=tercih.
 * Tür başına anahtar + Sessiz saatler. Tercihler hesabınla eşitlenir (medsoru_bildirim_tercih_v1).
 */
export default function BildirimTercihV15() {
  const [t, yaz] = useBildirimTercih();
  useV15Baslik({ baslik: 'Bildirim tercihleri', alt: 'Bildirimler', geri: '/bildirimler' });
  const gruplar = ['Ders', 'Soru', 'Sistem'] as const;
  const push = userNotificationService.isPushEnabled();
  return (
    <div className="bt15">
      <h1 className="sr-only">Bildirim tercihleri</h1>
      {gruplar.map((g) => (
        <section key={g} className="v15-card kre-kart bt15-k">
          <h2 className="v15-cap">{g}</h2>
          {BILDIRIM_TURLERI.filter((x) => x.grup === g).map((x) => {
            const acik = !t.kapali[x.id];
            return (
              <div key={x.id} className="kre-sat bt15-sat">
                <span className="bt15-t"><b>{x.ad}</b><span>{x.alt}</span></span>
                <button type="button" role="switch" aria-checked={acik} aria-label={x.ad} className={`kre-tgl${acik ? ' is-on' : ''}`}
                  onClick={() => { const k = { ...t.kapali }; if (acik) k[x.id] = 1; else delete k[x.id]; yaz({ ...t, kapali: k }); }}><i /></button>
              </div>
            );
          })}
        </section>
      ))}
      <section className="v15-card kre-kart bt15-k">
        <h2 className="v15-cap">Sessiz saatler</h2>
        <div className="kre-sat bt15-sat">
          <span className="bt15-t"><b>Sessiz saatler</b><span>Bu aralıkta anlık bildirim gösterilmez; bildirimler listede birikir.</span></span>
          <button type="button" role="switch" aria-checked={t.sessiz.acik} aria-label="Sessiz saatler" className={`kre-tgl${t.sessiz.acik ? ' is-on' : ''}`}
            onClick={() => yaz({ ...t, sessiz: { ...t.sessiz, acik: !t.sessiz.acik } })}><i /></button>
        </div>
        {t.sessiz.acik && (
          <div className="bt15-saat">
            <label>Başlangıç<input type="time" value={t.sessiz.bas} onChange={(e) => yaz({ ...t, sessiz: { ...t.sessiz, bas: e.target.value } })} /></label>
            <label>Bitiş<input type="time" value={t.sessiz.bit} onChange={(e) => yaz({ ...t, sessiz: { ...t.sessiz, bit: e.target.value } })} /></label>
          </div>
        )}
        {t.sessiz.acik && sessizSaatte(t) && <p className="kre-not">Şu an sessiz saatlerdesin.</p>}
        {!push && <p className="kre-not">Anlık bildirimler bu cihazda kapalı; bildirimler yalnız bu listede görünür.</p>}
      </section>
      <p className="kre-not">Tercihlerin hesabınla eşitlenir; diğer cihazlarında da geçerli olur.</p>
    </div>
  );
}
