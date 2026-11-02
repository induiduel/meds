import React, { useState } from 'react';
import { SayfaBasligi, VeriTablosu, useAdminSorgu, adminIstek, Rozet, Hata, Yukleniyor, onayIste, gerekceIste, bildir, zamanMetni, IstatistikIzgara, IstatistikKart } from '../kit';
import type { SayfaProps } from '../menu';
import { KisiBag } from './kisiOrtak';

type Talep = {
  id: string; uid: string; email: string; ad: string | null; ogrenci_no: string | null; aciklama: string | null;
  durum: 'bekliyor' | 'onaylandi' | 'reddedildi' | 'iptal'; karar_veren: string | null; karar_notu: string | null; karar_zamani: string | null;
  ip: string | null; cihaz: string | null; olusturma: string; kaynak: string; sifre_var: boolean;
  profil: { ad: string | null; ogrenciNo: string | null; sonGiris: string | null; olusturma: string | null };
  eslesme: { ogrenciNo: boolean | null; ad: boolean | null };
};

/**
 * Kullanıcılar › Şifre talepleri (2026-11-02, H466): giriş yapamayan öğrenci (eski Google/Firebase hesabı ya da unutulan
 * şifre) giriş ekranında e-posta/öğrenci no + ad soyad + öğrenci no + yeni şifre yazar. Burada yazdıkları hesabın kayıtlı
 * profiliyle yan yana görünür; gerçek kişi olduğuna karar verirsen onayla → talepteki şifre hesaba yazılır, öğrencinin
 * cihazı kendiliğinden giriş yapar. uid değişmez, tüm veri yerinde kalır. Uçlar: GET /api/admin/kimlik/sifre-talepleri,
 * POST /api/admin/kimlik/sifre-talepleri/karar. Eşleşme rozetleri yalnız ipucudur; karar yöneticinindir.
 */
export default function SifreTalepleri({ git }: SayfaProps) {
  const [filtre, setFiltre] = useState<'bekliyor' | ''>('bekliyor');
  const d = useAdminSorgu<{ talepler: Talep[]; bekleyen: number }>('/api/admin/kimlik/sifre-talepleri', { sorgu: { durum: filtre }, canliOlay: ['sifre_talebi'], aralikMs: 30_000 });

  const karar = async (t: Talep, k: 'onayla' | 'reddet') => {
    let not: string | null = null;
    if (k === 'onayla') {
      const uyari = t.eslesme.ogrenciNo === false || t.eslesme.ad === false;
      if (!(await onayIste({
        baslik: `${t.ad || t.email} için yeni şifre onaylansın mı?`,
        tehlikeli: uyari,
        onayMetni: 'Onayla',
        aciklama: <>
          Hesap <b>{t.email}</b>. Kayıtlı ad: <b>{t.profil.ad || '—'}</b>, kayıtlı no: <b>{t.profil.ogrenciNo || '—'}</b>.
          Talepte: <b>{t.ad || '—'}</b> / <b>{t.ogrenci_no || '—'}</b>.
          {uyari && <> <b>Bilgiler kayıtla uyuşmuyor</b>; yalnız kişiyi başka yoldan doğruladıysan onayla.</>}
          {' '}Onaylanınca talepteki şifre geçerli olur, öğrenci bu şifreyle e-postası ya da öğrenci numarasıyla girer.
        </>,
      }))) return;
    } else {
      not = await gerekceIste({ baslik: 'Talep reddedilsin mi?', tehlikeli: true, onayMetni: 'Reddet', gerekce: { etiket: 'Öğrenciye görünecek neden', enAz: 3 } });
      if (!not) return;
    }
    try {
      await adminIstek('/api/admin/kimlik/sifre-talepleri/karar', { yontem: 'POST', govde: { id: t.id, karar: k, not } });
      bildir(k === 'onayla' ? 'Onaylandı; öğrenci yeni şifresiyle girebilir.' : 'Reddedildi.', 'iyi');
      d.yenile();
    } catch (e: any) { bildir(e.message, 'kotu'); }
  };

  const esRozet = (v: boolean | null) => (v === null ? <Rozet>kayıt yok</Rozet> : v ? <Rozet ton="iyi">uyuşuyor</Rozet> : <Rozet ton="kotu">uyuşmuyor</Rozet>);
  const durumRozet = (t: Talep) => ({
    bekliyor: <Rozet ton="uyari">bekliyor</Rozet>,
    onaylandi: <Rozet ton="iyi" title={`${t.karar_veren || ''} · ${t.karar_zamani ? zamanMetni(t.karar_zamani) : ''}`}>onaylandı</Rozet>,
    reddedildi: <Rozet ton="kotu" title={t.karar_notu || ''}>reddedildi</Rozet>,
    iptal: <Rozet title={t.karar_notu || ''}>yerine yenisi geldi</Rozet>,
  }[t.durum]);

  if (d.hata && !d.veri) return <Hata hata={d.hata} yenile={d.yenile} />;
  return (
    <>
      <SayfaBasligi
        baslik="Şifre talepleri"
        aciklama="Giriş yapamayan öğrencilerin yeni şifre talepleri. Yazdıklarını kayıtlı profille karşılaştır; gerçek kişiyse onayla."
      />
      <IstatistikIzgara>
        <IstatistikKart etiket="Bekleyen" deger={d.veri?.bekleyen ?? '…'} ton={d.veri?.bekleyen ? 'uyari' : 'iyi'} yukleniyor={d.yukleniyor && !d.veri} />
      </IstatistikIzgara>
      <p style={{ display: 'flex', gap: 6 }}>
        <button type="button" className={`m16-btn${filtre === 'bekliyor' ? ' birincil' : ''}`} onClick={() => setFiltre('bekliyor')}>Bekleyenler</button>
        <button type="button" className={`m16-btn${filtre === '' ? ' birincil' : ''}`} onClick={() => setFiltre('')}>Tümü</button>
      </p>
      {!d.veri ? <Yukleniyor satir={6} /> : (
        <VeriTablosu<Talep>
          kimlik="sifre-talepleri" ogeler={d.veri.talepler} satirKimligi={(x) => x.id} aramaYeri="E-posta, ad, öğrenci no…"
          sutunlar={[
            { anahtar: 'olusturma', baslik: 'Zaman', genislik: '110px', sirala: true, deger: (x) => x.olusturma, hucre: (x) => zamanMetni(x.olusturma) },
            { anahtar: 'email', baslik: 'Hesap', genislik: 'minmax(200px,2fr)', deger: (x) => `${x.email} ${x.profil.ad || ''}`, hucre: (x) => <span className="m16-kisalt"><KisiBag anahtar={`u:${x.uid}`} git={git}><strong>{x.email}</strong></KisiBag> <small style={{ color: 'var(--color-ink-3)' }}>{x.kaynak === 'firebase-gocu' ? 'eski hesap' : 'yeni hesap'}{x.sifre_var ? ' · şifresi var' : ''}</small></span> },
            { anahtar: 'ad', baslik: 'Talepteki ad / kayıtlı', genislik: 'minmax(200px,2fr)', deger: (x) => x.ad || '', hucre: (x) => <span className="m16-kisalt">{x.ad || '—'} <small style={{ color: 'var(--color-ink-3)' }}>/ {x.profil.ad || '—'}</small> {esRozet(x.eslesme.ad)}</span> },
            { anahtar: 'ogrenci_no', baslik: 'Talepteki no / kayıtlı', genislik: 'minmax(190px,1.5fr)', deger: (x) => x.ogrenci_no || '', hucre: (x) => <span className="m16-kisalt">{x.ogrenci_no || '—'} <small style={{ color: 'var(--color-ink-3)' }}>/ {x.profil.ogrenciNo || '—'}</small> {esRozet(x.eslesme.ogrenciNo)}</span> },
            { anahtar: 'aciklama', baslik: 'Not', genislik: 'minmax(140px,1.5fr)', deger: (x) => x.aciklama || '', hucre: (x) => <span className="m16-kisalt" title={x.aciklama || ''}>{x.aciklama || '—'}</span> },
            { anahtar: 'sonGiris', baslik: 'Son giriş', genislik: '110px', deger: (x) => x.profil.sonGiris || '', hucre: (x) => (x.profil.sonGiris ? zamanMetni(x.profil.sonGiris) : '—'), gizli: true },
            { anahtar: 'cihaz', baslik: 'Cihaz', genislik: 'minmax(140px,1fr)', deger: (x) => x.cihaz || '', hucre: (x) => <span className="m16-kisalt" title={x.cihaz || ''}>{x.cihaz || '—'}</span>, gizli: true },
            { anahtar: 'durum', baslik: 'Durum', genislik: '140px', deger: (x) => x.durum, hucre: durumRozet },
            {
              anahtar: 'islem', baslik: '', genislik: '190px', deger: () => '', hucre: (x) => x.durum === 'bekliyor' ? (
                <span style={{ display: 'inline-flex', gap: 6 }}>
                  <button type="button" className="m16-btn birincil" onClick={() => void karar(x, 'onayla')}>Onayla</button>
                  <button type="button" className="m16-btn tehlike" onClick={() => void karar(x, 'reddet')}>Reddet</button>
                </span>
              ) : null,
            },
          ]}
          bosMetin={filtre === 'bekliyor' ? 'Bekleyen şifre talebi yok.' : 'Şifre talebi yok.'}
        />
      )}
    </>
  );
}
