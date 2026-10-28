import React, { useState } from 'react';
import { SayfaBasligi, Form, Rozet, Yukleniyor, Hata, useAdminSorgu, adminIstek, bildir, onayIste, zamanMetni, IstatistikIzgara, IstatistikKart } from '../kit';
import type { SayfaProps } from '../menu';

/**
 * Site › Kanallar — öğrenciye/yöneticiye ulaşan kanallar: SMTP e-posta (Faz 14 sonuç postası, e-posta bağlantısı ile giriş) ve
 * yönetici web push. Uçlar: GET/POST /api/admin/smtp-config, POST /api/admin/smtp-test, GET /api/admin/push/status, POST /api/admin/push/test.
 * Şifre istemciye hiç gelmez; alan boş bırakılırsa sunucudaki şifre korunur.
 */
type Smtp = { enabled: boolean; service: string; host?: string; port?: number; secure?: boolean; user?: string; from?: string; hasPassword: boolean; isConfigured: boolean };
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
          {smtp.hata ? <Hata hata={smtp.hata} yenile={smtp.yenile} /> : !s ? <Yukleniyor satir={5} /> : (
            <Form
              alanlar={[
                { ad: 'enabled', etiket: 'Gönderim açık', tur: 'anahtar' },
                { ad: 'service', etiket: 'Servis', tur: 'secim', secenekler: [{ deger: 'gmail', etiket: 'Gmail' }, { deger: 'custom', etiket: 'Özel sunucu' }] },
                { ad: 'host', etiket: 'Sunucu', yerTutucu: 'smtp.example.com' },
                { ad: 'port', etiket: 'Port', tur: 'sayi', enAz: 1, enFazla: 65535 },
                { ad: 'user', etiket: 'Kullanıcı' },
                { ad: 'from', etiket: 'Gönderen' },
                { ad: 'pass', etiket: 'Uygulama şifresi', ipucu: s.hasPassword ? 'Kayıtlı. Değiştirmek için yazın; boş bırakılırsa korunur.' : 'Kayıtlı şifre yok.' },
              ]}
              deger={{ enabled: s.enabled, service: s.service || 'gmail', host: s.host || '', port: s.port || 465, user: s.user || '', from: s.from || '', pass: '' }}
              kaydet={async (yeni) => {
                const govde: Record<string, unknown> = { ...yeni };
                if (!govde.pass) delete govde.pass;
                await adminIstek('/api/admin/smtp-config', { yontem: 'POST', govde });
                bildir('SMTP ayarı kaydedildi', 'iyi');
                smtp.yenile();
              }}
            />
          )}
          <p><button type="button" className="m16-btn" disabled={mesgul || !s?.isConfigured} onClick={async () => {
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
