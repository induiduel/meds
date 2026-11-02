import React, { useEffect, useState } from 'react';
import { CheckCircle2, KeyRound, Loader2, MailCheck, Send } from 'lucide-react';
import { sendAuthCode, verifyAuthCode, bekleyenSifreTalebi, AppUser } from '../services/auth';
import { SifreTalebi } from './SifreTalebi';
import './epostaBaglanti.css';

/**
 * Şifre belirleme / şifresiz giriş akışları (2026-11-02; Firebase e-posta bağlantısının yerine). Giriş kartının altında:
 *  - amac 'talep' (asıl yol, e-posta gerekmez): yönetici onaylı yeni şifre — SifreTalebi.tsx.
 *  - amac 'sifre': "Şifremi unuttum / Şifre belirle" → e-postaya 6 haneli kod → kod + yeni şifre → oturum açılır.
 *    Eski giriş sisteminden taşınan hesaplar da şifresini böyle belirler (uid ve tüm veri aynı kalır).
 *  - amac 'giris': şifresiz giriş → kod → oturum açılır.
 * Kod 15 dk geçerli, 5 hatalı denemede düşer; tekrar gönderme 60 sn sonra. Sunucu: src/services/yerelKimlik.ts.
 */
const maskele = (e: string) => { const [a, d] = e.split('@'); return d ? `${a.slice(0, 1)}***@${d}` : e; };

export type KodAmaci = 'sifre' | 'giris' | 'talep';

export function EpostaBaglantiGiris({
  email, setEmail, disabled, v12 = false, acik, setAcik, onGiris, sabitEposta, uyari,
}: {
  email: string;
  setEmail: (v: string) => void;
  disabled?: boolean;
  v12?: boolean;
  /** Açık akış (null: yalnız giriş düğmeleri) */
  acik: KodAmaci | null;
  setAcik: (a: KodAmaci | null) => void;
  onGiris: (u: AppUser, mesaj: string) => void;
  /** Yönetici girişinde e-posta sabittir */
  sabitEposta?: string;
  /** Akışın üstünde gösterilecek açıklama (ör. "giriş sistemimiz yenilendi") */
  uyari?: string | null;
}) {
  const [durum, setDurum] = useState<'bos' | 'gonderiliyor' | 'gonderildi' | 'dogrulaniyor' | 'tamam'>('bos');
  const [gonderilen, setGonderilen] = useState('');
  const [kod, setKod] = useState('');
  const [yeniSifre, setYeniSifre] = useState('');
  const [sayac, setSayac] = useState(0);
  const [hata, setHata] = useState('');
  const [bilgi, setBilgi] = useState('');
  useEffect(() => {
    if (sayac <= 0) return;
    const t = window.setTimeout(() => setSayac((s) => s - 1), 1000);
    return () => window.clearTimeout(t);
  }, [sayac]);
  useEffect(() => { setDurum('bos'); setKod(''); setYeniSifre(''); setHata(''); setBilgi(''); }, [acik]);
  // Bu cihazda bekleyen şifre talebi varsa durum kartı kendiliğinden açılır
  useEffect(() => { if (!acik && bekleyenSifreTalebi()) setAcik('talep'); }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const btn = v12 ? 'e12-btn is-lg is-block' : 'au-google';
  const pri = v12 ? 'e12-btn is-pri is-lg is-block' : 'au-submit';
  const spin = <Loader2 className={v12 ? 'e12-spin' : 'au-spin'} aria-hidden />;
  const adres = (sabitEposta || email).trim().toLowerCase();

  const gonder = async (amac: 'sifre' | 'giris') => {
    setHata(''); setBilgi('');
    if (!adres || !adres.includes('@')) { setAcik(amac); setHata('Kod göndermek için üstteki e-posta alanını doldur.'); return; }
    setAcik(amac);
    setDurum('gonderiliyor');
    try {
      const m = await sendAuthCode(adres, amac);
      setGonderilen(adres); setDurum('gonderildi'); setSayac(60); setBilgi(m);
    } catch (e: any) {
      setHata(e?.message || 'Kod gönderilemedi.'); setDurum('bos');
    }
  };
  const dogrula = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!acik || acik === 'talep') return;
    setHata('');
    if (kod.replace(/\D/g, '').length !== 6) { setHata('E-postana gelen 6 haneli kodu yaz.'); return; }
    if (acik === 'sifre' && yeniSifre.trim().length < 6) { setHata('Yeni şifre en az 6 karakter olmalı.'); return; }
    setDurum('dogrulaniyor');
    try {
      const u = await verifyAuthCode(gonderilen || adres, kod, acik, acik === 'sifre' ? yeniSifre.trim() : undefined);
      setDurum('tamam');
      onGiris(u, acik === 'sifre' ? 'Şifren kaydedildi, giriş yapıldı' : 'Kodla giriş yapıldı');
    } catch (er: any) {
      setHata(er?.message || 'Kod doğrulanamadı.'); setDurum('gonderildi');
    }
  };

  const hataP = hata ? <p role="alert" className="eb-hata">{hata}</p> : null;

  if (acik === 'talep') {
    return <SifreTalebi kimlik={adres} v12={v12} disabled={disabled} onGiris={onGiris} onVazgec={() => setAcik(null)} uyari={uyari} />;
  }

  if (acik && (durum === 'gonderildi' || durum === 'dogrulaniyor' || durum === 'tamam')) {
    return (
      <form className="eb" onSubmit={dogrula} noValidate>
        <p className="eb-baslik"><MailCheck aria-hidden />E-postanı kontrol et</p>
        <p className="eb-not">
          <b>{maskele(gonderilen)}</b> adresine 6 haneli kod gönderdik{acik === 'sifre' ? '; kodu ve yeni şifreni yaz' : ''}. Gelmezse gereksiz (spam) klasörüne bak.
          {bilgi && !bilgi.startsWith('Bu e-postayla') ? ` ${bilgi}` : ''}
        </p>
        <div className="eb-alanlar">
          <input
            className="eb-kod is-hane"
            value={kod}
            onChange={(e) => setKod(e.target.value.replace(/\D/g, '').slice(0, 6))}
            inputMode="numeric"
            autoComplete="one-time-code"
            placeholder="6 haneli kod"
            aria-label="E-posta kodu"
            disabled={disabled || durum !== 'gonderildi'}
          />
          {acik === 'sifre' && (
            <input
              className="eb-kod"
              type="password"
              value={yeniSifre}
              onChange={(e) => setYeniSifre(e.target.value)}
              autoComplete="new-password"
              placeholder="Yeni şifre (en az 6 karakter)"
              aria-label="Yeni şifre"
              disabled={disabled || durum !== 'gonderildi'}
            />
          )}
        </div>
        <button type="submit" className={pri} disabled={disabled || durum !== 'gonderildi'}>
          {durum === 'dogrulaniyor' ? spin : durum === 'tamam' ? <CheckCircle2 aria-hidden /> : null}
          {durum === 'tamam' ? 'Giriş yapıldı' : acik === 'sifre' ? 'Şifreyi kaydet ve gir' : 'Kodla giriş yap'}
        </button>
        <div className="eb-satir">
          <button type="button" className="eb-link" onClick={() => gonder(acik === 'giris' ? 'giris' : 'sifre')} disabled={sayac > 0 || disabled}>
            {sayac > 0 ? `Kodu tekrar gönder · 0:${String(sayac).padStart(2, '0')}` : 'Kodu tekrar gönder'}
          </button>
          <button type="button" className="eb-link" onClick={() => setAcik(null)}>Vazgeç</button>
        </div>
        {hataP}
      </form>
    );
  }

  return (
    <div className="eb">
      {uyari && <p className="eb-not" role="status">{uyari}</p>}
      <button type="button" className={btn} onClick={() => { setHata(''); setAcik('talep'); }} disabled={disabled}>
        <KeyRound aria-hidden />
        Şifremi unuttum / Şifre belirle
      </button>
      <div className="eb-satir">
        <button type="button" className="eb-link" onClick={() => gonder('sifre')} disabled={disabled || durum === 'gonderiliyor'}>
          {durum === 'gonderiliyor' && acik === 'sifre' ? spin : null}E-postayla kod al
        </button>
        {!sabitEposta && (
          <button type="button" className="eb-link" onClick={() => gonder('giris')} disabled={disabled || durum === 'gonderiliyor'}>
            {durum === 'gonderiliyor' && acik === 'giris' ? spin : <Send aria-hidden />}Şifresiz kodla giriş
          </button>
        )}
      </div>
      {hataP}
    </div>
  );
}
