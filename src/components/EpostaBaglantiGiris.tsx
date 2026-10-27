import React, { useEffect, useState } from 'react';
import { CheckCircle2, Loader2, MailCheck, Send } from 'lucide-react';
import { completeEmailLinkLogin, emailLinkPending, sendEmailLoginLink, storedEmailForLink } from '../services/auth';
import './epostaBaglanti.css';

/**
 * I06 · Şifresiz giriş (Firebase e-posta bağlantısı). Giriş kartının altında:
 *  - "E-postama giriş bağlantısı gönder" → bağlantı gönderildi ekranı (maskeli adres + 60 sn tekrar gönder sayacı)
 *  - Bağlantı başka cihazda açıldıysa (adres giriş bağlantısı, e-posta yerelde yok) e-postayı onaylatıp girişi tamamlar.
 * Oturum açılınca onAuthStateChanged (services/auth.ts initAuth) kullanıcıyı içeri alır; bu bileşen yalnız tetikler.
 */
const maskele = (e: string) => { const [a, d] = e.split('@'); return d ? `${a.slice(0, 1)}***@${d}` : e; };

export function EpostaBaglantiGiris({ email, setEmail, disabled, v12 = false }: { email: string; setEmail: (v: string) => void; disabled?: boolean; v12?: boolean }) {
  const [durum, setDurum] = useState<'bos' | 'gonderiliyor' | 'gonderildi' | 'onay' | 'tamamlaniyor' | 'tamam'>(
    () => (emailLinkPending() && !storedEmailForLink() ? 'onay' : 'bos'));
  const [gonderilen, setGonderilen] = useState('');
  const [sayac, setSayac] = useState(0);
  const [hata, setHata] = useState('');
  useEffect(() => {
    if (sayac <= 0) return;
    const t = window.setTimeout(() => setSayac((s) => s - 1), 1000);
    return () => window.clearTimeout(t);
  }, [sayac]);
  const btn = v12 ? 'e12-btn is-lg is-block' : 'au-google';
  const pri = v12 ? 'e12-btn is-pri is-lg is-block' : 'au-submit';

  const gonder = async () => {
    setHata('');
    if (!email.trim()) { setHata('Bağlantı göndermek için üstteki e-posta alanını doldur.'); return; }
    setDurum('gonderiliyor');
    try { await sendEmailLoginLink(email); setGonderilen(email.trim().toLowerCase()); setDurum('gonderildi'); setSayac(60); }
    catch (e: any) { setHata(e?.message || 'Bağlantı gönderilemedi.'); setDurum('bos'); }
  };
  const tamamla = async (e: React.FormEvent) => {
    e.preventDefault(); setHata(''); setDurum('tamamlaniyor');
    try { if (await completeEmailLinkLogin(email)) setDurum('tamam'); else { setHata('Giriş bağlantısı bulunamadı.'); setDurum('onay'); } }
    catch (er: any) { setHata(er?.message || 'Giriş tamamlanamadı.'); setDurum('onay'); }
  };

  const hataP = hata ? <p role="alert" className="eb-hata">{hata}</p> : null;
  if (durum === 'onay' || durum === 'tamamlaniyor' || durum === 'tamam') {
    return (
      <form className="eb" onSubmit={tamamla}>
        <p className="eb-baslik"><MailCheck aria-hidden />Giriş bağlantısını açtın</p>
        <p className="eb-not">Bağlantı başka bir cihazdan istendi. Güvenlik için bağlantının gönderildiği e-posta adresini yukarıya yazıp girişi tamamla.</p>
        <button type="submit" className={pri} disabled={disabled || durum !== 'onay' || !email.trim()}>
          {durum === 'tamamlaniyor' ? <Loader2 className={v12 ? 'e12-spin' : 'au-spin'} aria-hidden /> : durum === 'tamam' ? <CheckCircle2 aria-hidden /> : null}
          {durum === 'tamam' ? 'Giriş yapıldı' : 'Girişi tamamla'}
        </button>
        {hataP}
      </form>
    );
  }
  if (durum === 'gonderildi') {
    return (
      <div className="eb" role="status">
        <p className="eb-baslik"><MailCheck aria-hidden />E-postanı kontrol et</p>
        <p className="eb-not"><b>{maskele(gonderilen)}</b> adresine tek kullanımlık giriş bağlantısı gönderdik. Bağlantıya bu cihazda dokunduğunda şifresiz giriş yapılır. Gelmezse gereksiz (spam) klasörüne bak.</p>
        <button type="button" className="eb-link" onClick={gonder} disabled={sayac > 0 || disabled}>
          {sayac > 0 ? `Bağlantıyı tekrar gönder · 0:${String(sayac).padStart(2, '0')}` : 'Bağlantıyı tekrar gönder'}
        </button>
        {hataP}
      </div>
    );
  }
  return (
    <div className="eb">
      <button type="button" className={btn} onClick={gonder} disabled={disabled || durum === 'gonderiliyor'}>
        {durum === 'gonderiliyor' ? <Loader2 className={v12 ? 'e12-spin' : 'au-spin'} aria-hidden /> : <Send aria-hidden />}
        Şifresiz giriş: e-postama bağlantı gönder
      </button>
      {hataP}
    </div>
  );
}
