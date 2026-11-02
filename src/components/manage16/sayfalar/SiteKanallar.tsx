import React, { useState } from 'react';
import { SayfaBasligi, Form, Rozet, Yukleniyor, Hata, useAdminSorgu, adminIstek, bildir, onayIste, zamanMetni, IstatistikIzgara, IstatistikKart } from '../kit';
import type { SayfaProps } from '../menu';

/**
 * Site › Kanallar — öğrenciye/yöneticiye ulaşan kanallar: SMTP e-posta (kimlik kodları, Faz 14 sonuç postası, karşılama) ve
 * yönetici web push. Uçlar: GET/POST /api/admin/smtp-config, POST /api/admin/smtp-test ({yalnizBaglanti} = göndermeden sına),
 * GET /api/admin/push/status, POST /api/admin/push/test. Şifre istemciye hiç gelmez; alan boş bırakılırsa sunucudaki şifre korunur.
 * Sağlayıcıyı sunucu adı belirler (gmail içeriyorsa Gmail, değilse özel SMTP); port 465 doğrudan TLS, 587 STARTTLS.
 * Kimlik kodları (şifre belirle / kodla giriş) "Gönderim açık" kapalıyken de bu bilgilerle gider (2026-11-02, H466).
 */
type Smtp = { enabled: boolean; service: string; host?: string; port?: number; secure?: boolean; user?: string; from?: string; hasPassword: boolean; isConfigured: boolean; google?: boolean };

/** Google dışı yaygın SMTP sağlayıcıları (ücretsiz katmanı olanlar). Kullanıcı adı/anahtar sağlayıcı panelinden alınır. */
const SAGLAYICILAR: { ad: string; host: string; port: number; not: string }[] = [
  { ad: 'Brevo', host: 'smtp-relay.brevo.com', port: 587, not: 'Günde 300 e-posta ücretsiz. Kullanıcı: SMTP girişi, şifre: SMTP anahtarı.' },
  { ad: 'Resend', host: 'smtp.resend.com', port: 465, not: 'Ayda 3.000 ücretsiz. Kullanıcı: resend, şifre: API anahtarı; alan adı doğrulaması gerekir.' },
  { ad: 'Mailjet', host: 'in-v3.mailjet.com', port: 587, not: 'Günde 200 ücretsiz. Kullanıcı: API anahtarı, şifre: gizli anahtar.' },
  { ad: 'Zoho Mail', host: 'smtp.zoho.eu', port: 465, not: 'Zoho posta hesabı; kullanıcı: tam adres, şifre: uygulama şifresi.' },
];
type Push = { deviceCount: number; devices: { endpoint: string; userAgent?: string; createdAt?: string }[]; recentNotifications: any[]; emailEnabled: boolean };

export default function SiteKanallar(_p: SayfaProps) {
  const smtp = useAdminSorgu<Smtp>('/api/admin/smtp-config');
  const push = useAdminSorgu<Push>('/api/admin/push/status');
  const [mesgul, setMesgul] = useState(false);
  const calis = async (f: () => Promise<any>, ok: string) => {
    setMesgul(true);
    try { const r = await f(); bildir(r?.message || ok, 'iyi'); } catch (e: any) { bildir(e?.message || 'Olmadı', 'kotu'); } finally { setMesgul(false); }
  };
  const s = smtp.veri;
  const [hazir, setHazir] = useState<{ host: string; port: number } | null>(null);
  return (
    <>
      <SayfaBasligi baslik="Kanallar" aciklama="E-posta (SMTP) ve yönetici anlık bildirimleri." />
      <IstatistikIzgara>
        <IstatistikKart etiket="E-posta" deger={s ? (s.enabled && s.isConfigured ? 'Açık' : s.isConfigured ? 'Kapalı' : 'Ayarsız') : '…'} ton={s?.enabled && s?.isConfigured ? 'iyi' : 'uyari'} yukleniyor={smtp.yukleniyor && !s} />
        <IstatistikKart etiket="Push cihazı" deger={push.veri?.deviceCount ?? '…'} yukleniyor={push.yukleniyor && !push.veri} />
      </IstatistikIzgara>
      <div className="m16-izgara-2">
        <div className="m16-kart">
          <h2>SMTP e-posta</h2>
          {s?.google && (
            <p><Rozet ton="uyari">Google</Rozet> Kimlik kodları şu an Gmail üzerinden gidiyor. Google hesabı askıya alınırsa öğrenciler şifre belirleme kodu alamaz;
              aşağıdan Google dışı bir sağlayıcı seç, bilgileri gir, <b>Bağlantıyı sına</b> ile doğrula.</p>
          )}
          <p className="m16-satir" style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
            {SAGLAYICILAR.map((x) => (
              <button key={x.ad} type="button" className="m16-btn" title={x.not} onClick={() => { setHazir({ host: x.host, port: x.port }); bildir(`${x.ad}: ${x.not}`, 'iyi'); }}>{x.ad}</button>
            ))}
          </p>
          {smtp.hata ? <Hata hata={smtp.hata} yenile={smtp.yenile} /> : !s ? <Yukleniyor satir={5} /> : (
            <Form
              key={hazir ? `${hazir.host}:${hazir.port}` : 'kayitli'}
              alanlar={[
                { ad: 'enabled', etiket: 'Genel gönderim açık', tur: 'anahtar', ipucu: 'Karşılama ve bildirim e-postaları. Kimlik kodları kapalıyken de gider.' },
                { ad: 'host', etiket: 'Sunucu', yerTutucu: 'smtp-relay.brevo.com' },
                { ad: 'port', etiket: 'Port', tur: 'sayi', enAz: 1, enFazla: 65535, ipucu: '465 = TLS, 587 = STARTTLS' },
                { ad: 'user', etiket: 'Kullanıcı' },
                { ad: 'from', etiket: 'Gönderen', ipucu: 'Sağlayıcıda doğrulanmış adres, ör. MeDSor <bildirim@alanadin>' },
                { ad: 'pass', etiket: 'Şifre / SMTP anahtarı', ipucu: s.hasPassword ? 'Kayıtlı. Değiştirmek için yazın; boş bırakılırsa korunur.' : 'Kayıtlı şifre yok.' },
              ]}
              deger={{ enabled: s.enabled, host: hazir?.host ?? (s.host || ''), port: hazir?.port ?? (s.port || 465), user: s.user || '', from: s.from || '', pass: '' }}
              kaydet={async (yeni) => {
                const govde: Record<string, unknown> = { ...yeni, port: Number(yeni.port) };
                if (!govde.pass) delete govde.pass;
                await adminIstek('/api/admin/smtp-config', { yontem: 'POST', govde });
                bildir('SMTP ayarı kaydedildi', 'iyi');
                setHazir(null);
                smtp.yenile();
              }}
            />
          )}
          <p><button type="button" className="m16-btn" disabled={mesgul || !s?.isConfigured} onClick={() =>
            void calis(() => adminIstek('/api/admin/smtp-test', { yontem: 'POST', govde: { yalnizBaglanti: true } }), 'Bağlantı başarılı')}>Bağlantıyı sına</button>{' '}
          <button type="button" className="m16-btn" disabled={mesgul || !s?.isConfigured} onClick={async () => {
            if (await onayIste({ baslik: 'Deneme e-postası gönderilsin mi?', aciklama: 'Yönetici adresine tek bir deneme iletisi gider.', onayMetni: 'Gönder' }))
              void calis(() => adminIstek('/api/admin/smtp-test', { yontem: 'POST', govde: {} }), 'Deneme e-postası gönderildi');
          }}>Deneme e-postası</button></p>
        </div>
        <div className="m16-kart">
          <h2>Yönetici web push</h2>
          {push.hata ? <Hata hata={push.hata} yenile={push.yenile} /> : !push.veri ? <Yukleniyor satir={4} /> : (
            <>
              <ul className="m16-liste">
                {push.veri.devices.map((d, i) => <li key={i}><code>{d.endpoint}</code> {d.createdAt && <small>· {zamanMetni(d.createdAt)}</small>}</li>)}
                {!push.veri.devices.length && <li>Kayıtlı cihaz yok.</li>}
              </ul>
              <p><button type="button" className="m16-btn" disabled={mesgul || !push.veri.deviceCount} onClick={() => calis(() => adminIstek('/api/admin/push/test', { yontem: 'POST' }), 'Deneme bildirimi gönderildi')}>Deneme bildirimi</button></p>
              <h2>Son bildirimler</h2>
              <ul className="m16-liste">
                {(push.veri.recentNotifications || []).slice(0, 10).map((n: any, i: number) => <li key={i}>{n.title || n.baslik} {n.createdAt && <Rozet>{zamanMetni(n.createdAt)}</Rozet>}</li>)}
              </ul>
            </>
          )}
        </div>
      </div>
    </>
  );
}
