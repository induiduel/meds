import React, { useCallback, useEffect, useState } from 'react';
import { CheckCircle2, Clock, Loader2, ShieldCheck, XCircle } from 'lucide-react';
import { AppUser, bekleyenSifreTalebi, sifreTalebiDurumu, sifreTalebiGonder, sifreTalebiniUnut } from '../services/auth';
import './epostaBaglanti.css';

/**
 * Yönetici onaylı şifre belirleme (2026-11-02, e-posta gerekmez). Eski giriş sisteminden taşınan ya da şifresini
 * unutan kişi: e-posta/öğrenci no + ad soyad + öğrenci no + yeni şifre yazar → talep yöneticiye gider. Yönetici
 * kayıtlı profille karşılaştırıp gerçek kişiyse onaylar; bu cihaz 20 sn'de bir durumu sorar ve onay gelince
 * kendiliğinden giriş yapar. Başka cihazdan e-posta ya da öğrenci no + yeni şifreyle girilir. Sunucu: yerelKimlik.ts.
 */
export function SifreTalebi({ kimlik: ilkKimlik, v12, disabled, onGiris, onVazgec, uyari }: {
  kimlik: string;
  v12?: boolean;
  disabled?: boolean;
  onGiris: (u: AppUser, mesaj: string) => void;
  onVazgec: () => void;
  uyari?: string | null;
}) {
  const [bekleyen, setBekleyen] = useState(() => bekleyenSifreTalebi());
  const [kimlik, setKimlik] = useState(ilkKimlik);
  const [ad, setAd] = useState('');
  const [no, setNo] = useState(() => (/^\d{5,12}$/.test(ilkKimlik.trim()) ? ilkKimlik.trim() : ''));
  const [sifre, setSifre] = useState('');
  const [sifre2, setSifre2] = useState('');
  const [aciklama, setAciklama] = useState('');
  const [mesgul, setMesgul] = useState(false);
  const [hata, setHata] = useState('');
  const [sonuc, setSonuc] = useState<{ durum: string; not?: string | null } | null>(null);

  const pri = v12 ? 'e12-btn is-pri is-lg is-block' : 'au-submit';
  const spin = <Loader2 className={v12 ? 'e12-spin' : 'au-spin'} aria-hidden />;

  const sor = useCallback(async (elle = false) => {
    if (!bekleyenSifreTalebi()) return;
    if (elle) setMesgul(true);
    try {
      const r = await sifreTalebiDurumu();
      if (r.durum === 'bekliyor') return;
      setBekleyen(null);
      if (r.durum === 'onaylandi' && r.user) { onGiris(r.user, 'Şifren onaylandı, giriş yapıldı'); return; }
      setSonuc({ durum: r.durum, not: r.not });
    } catch (e: any) {
      if (elle) setHata(e?.message || 'Durum alınamadı.');
    } finally {
      if (elle) setMesgul(false);
    }
  }, [onGiris]);

  // Bekleyen talep varken 20 sn'de bir ve sekmeye dönüldüğünde durum sorulur
  useEffect(() => {
    if (!bekleyen) return;
    void sor();
    const t = window.setInterval(() => { if (document.visibilityState === 'visible') void sor(); }, 20_000);
    const g = () => { if (document.visibilityState === 'visible') void sor(); };
    document.addEventListener('visibilitychange', g);
    return () => { window.clearInterval(t); document.removeEventListener('visibilitychange', g); };
  }, [bekleyen, sor]);

  const gonder = async (e: React.FormEvent) => {
    e.preventDefault();
    setHata('');
    if (!kimlik.trim()) { setHata('E-posta adresini ya da öğrenci numaranı yaz.'); return; }
    if (ad.trim().length < 3) { setHata('Ad soyadını yaz.'); return; }
    if (no.replace(/\D/g, '').length < 5) { setHata('Öğrenci numaranı yaz.'); return; }
    if (sifre.trim().length < 6) { setHata('Yeni şifre en az 6 karakter olmalı.'); return; }
    if (sifre !== sifre2) { setHata('İki şifre aynı değil.'); return; }
    setMesgul(true);
    try {
      await sifreTalebiGonder({ kimlik: kimlik.trim(), yeniSifre: sifre, ad: ad.trim(), ogrenciNo: no, aciklama: aciklama.trim() || undefined });
      setSonuc(null);
      setBekleyen(bekleyenSifreTalebi());
    } catch (er: any) {
      setHata(er?.message || 'Talep gönderilemedi.');
    } finally {
      setMesgul(false);
    }
  };

  const hataP = hata ? <p role="alert" className="eb-hata">{hata}</p> : null;

  if (bekleyen) {
    return (
      <div className="eb" role="status">
        <p className="eb-baslik"><Clock aria-hidden />Şifre talebin yönetici onayında</p>
        <p className="eb-not">
          <b>{bekleyen.email}</b> hesabı için yeni şifren yöneticiye iletildi. Yönetici seni tanıyıp onaylayınca bu cihazda
          kendiliğinden giriş yapılır; sayfayı açık bırakabilir ya da daha sonra dönebilirsin. Başka cihazdan e-postan ya da
          öğrenci numaran ve yeni şifrenle girebilirsin.
        </p>
        <button type="button" className={pri} onClick={() => void sor(true)} disabled={disabled || mesgul}>
          {mesgul ? spin : null} Durumu yenile
        </button>
        <div className="eb-satir">
          <button type="button" className="eb-link" onClick={() => { sifreTalebiniUnut(); setBekleyen(null); }}>Yeni talep oluştur</button>
          <button type="button" className="eb-link" onClick={onVazgec}>Girişe dön</button>
        </div>
        {hataP}
      </div>
    );
  }

  return (
    <form className="eb" onSubmit={gonder} noValidate>
      <p className="eb-baslik"><ShieldCheck aria-hidden />Yönetici onayıyla yeni şifre</p>
      {sonuc && (
        <p className="eb-not" role="status">
          {sonuc.durum === 'reddedildi'
            ? <><XCircle aria-hidden style={{ width: 16, height: 16, verticalAlign: '-3px' }} /> Önceki talebin onaylanmadı{sonuc.not ? `: ${sonuc.not}` : '.'} Bilgilerini kontrol edip yeniden gönderebilirsin.</>
            : <><CheckCircle2 aria-hidden style={{ width: 16, height: 16, verticalAlign: '-3px' }} /> Önceki talebin sonuçlandı; yeni şifrenle giriş yapabilirsin.</>}
        </p>
      )}
      <p className="eb-not">
        {uyari || 'E-posta gerekmez. Bilgilerini yaz; yönetici gerçekten sen olduğunu doğrulayınca yeni şifren geçerli olur. Hesabın ve tüm verilerin yerinde kalır.'}
      </p>
      <div className="eb-alanlar">
        <input className="eb-kod" value={kimlik} onChange={(e) => setKimlik(e.target.value)} placeholder="Hesabının e-postası ya da öğrenci numaran" aria-label="E-posta ya da öğrenci numarası" autoComplete="username" disabled={disabled || mesgul} />
        <input className="eb-kod" value={ad} onChange={(e) => setAd(e.target.value)} placeholder="Ad soyad" aria-label="Ad soyad" autoComplete="name" disabled={disabled || mesgul} />
        <input className="eb-kod" value={no} onChange={(e) => setNo(e.target.value.replace(/\D/g, '').slice(0, 12))} inputMode="numeric" placeholder="Öğrenci numarası" aria-label="Öğrenci numarası" autoComplete="off" disabled={disabled || mesgul} />
        <input className="eb-kod" type="password" value={sifre} onChange={(e) => setSifre(e.target.value)} placeholder="Yeni şifre (en az 6 karakter)" aria-label="Yeni şifre" autoComplete="new-password" disabled={disabled || mesgul} />
        <input className="eb-kod" type="password" value={sifre2} onChange={(e) => setSifre2(e.target.value)} placeholder="Yeni şifre (tekrar)" aria-label="Yeni şifre tekrar" autoComplete="new-password" disabled={disabled || mesgul} />
        <input className="eb-kod" value={aciklama} onChange={(e) => setAciklama(e.target.value.slice(0, 500))} placeholder="Yöneticiye not (isteğe bağlı)" aria-label="Yöneticiye not" disabled={disabled || mesgul} />
      </div>
      <button type="submit" className={pri} disabled={disabled || mesgul}>
        {mesgul ? spin : null} Onaya gönder
      </button>
      <div className="eb-satir">
        <span />
        <button type="button" className="eb-link" onClick={onVazgec}>Vazgeç</button>
      </div>
      {hataP}
    </form>
  );
}
