import React from 'react';
import { SayfaBasligi, VeriTablosu, useAdminSorgu, adminIstek, Rozet, Hata, Yukleniyor, onayIste, bildir, zamanMetni } from '../kit';
import type { SayfaProps } from '../menu';
import { RolRozeti, KisiBag, tarihMetni } from './kisiOrtak';

type ESatir = { uid: string; email: string; displayName: string; role: string; isOwner: boolean; suspended: boolean; suspension: any; accessHistory: any[]; sessionsRevokedAt: string | null; lastLoginAt: string | null };

/**
 * Kullanıcılar › Erişim: rol (öğrenci/moderatör/yönetici), askıya alma, oturumları sonlandırma.
 * Gerçek etkiler: askı tüm yazma uçlarını 403'ler; oturum sonlandırma o andan önceki girişin jetonlarını sunucuda reddeder
 * ve öğrencinin uygulaması açılışta çıkış yapar (Firebase yenileme jetonu iptal edilmez).
 */
export default function KisiErisim({ git }: SayfaProps) {
  const d = useAdminSorgu<{ users: ESatir[] }>('/api/admin/people-access', { canliOlay: ['people_changed'] });
  const uygula = async (yol: string, uids: string[], govde: any, baslik: string, tehlikeli = false) => {
    if (!uids.length) return;
    if (!(await onayIste({ baslik, tehlikeli, onayMetni: 'Uygula' }))) return false;
    try {
      const r = await adminIstek<any>(`/api/admin/people-access/${yol}`, { yontem: 'POST', govde: { uids, ...govde } });
      bildir(`${r.changed?.length || 0} hesap güncellendi${r.skipped?.length ? ` · ${r.skipped.length} atlandı (${r.skipped[0].reason})` : ''}.`, r.skipped?.length && !r.changed?.length ? 'kotu' : 'iyi');
      d.yenile();
      return true;
    } catch (e: any) { bildir(e.message, 'kotu'); return false; }
  };
  const askiya = async (uids: string[]) => {
    const gerekce = window.prompt('Askı gerekçesi (en az 3 harf):');
    if (!gerekce || gerekce.trim().length < 3) return false;
    const bitis = window.prompt('Bitiş tarihi (YYYY-AA-GG, boş = süresiz):') || '';
    return uygula('suspend', uids, { reason: gerekce.trim(), until: bitis.trim() || undefined }, `${uids.length} hesap askıya alınsın mı?`, true);
  };
  if (d.hata && !d.veri) return <Hata hata={d.hata} yenile={d.yenile} />;
  return (
    <>
      <SayfaBasligi baslik="Erişim" aciklama="Rol, askı ve oturum sonlandırma. Ana yönetici hesabı değiştirilemez; her işlem erişim geçmişine ve denetim kaydına yazılır." />
      {!d.veri ? <Yukleniyor satir={8} /> : (
        <VeriTablosu<ESatir>
          kimlik="kisi-erisim" ogeler={d.veri.users} satirKimligi={(x) => x.uid} secim aramaYeri="Ad, e-posta, uid…"
          suzgecler={[
            { anahtar: 'rol', etiket: 'Rol', secenekler: [{ deger: 'student', etiket: 'Öğrenci' }, { deger: 'moderator', etiket: 'Moderatör' }, { deger: 'admin', etiket: 'Yönetici' }] },
          ]}
          topluEylemler={(sec, temizle) => (
            <>
              <button className="m16-btn" onClick={async () => { if (await uygula('role', sec, { role: 'student' }, `${sec.length} hesap öğrenci yapılsın mı?`)) temizle(); }}>Öğrenci</button>
              <button className="m16-btn" onClick={async () => { if (await uygula('role', sec, { role: 'moderator' }, `${sec.length} hesap moderatör yapılsın mı?`)) temizle(); }}>Moderatör</button>
              <button className="m16-btn tehlike" onClick={async () => { if (await askiya(sec)) temizle(); }}>Askıya al</button>
              <button className="m16-btn" onClick={async () => { if (await uygula('unsuspend', sec, {}, `${sec.length} hesabın askısı kalksın mı?`)) temizle(); }}>Askıyı kaldır</button>
              <button className="m16-btn tehlike" onClick={async () => { if (await uygula('oturum-sonlandir', sec, {}, `${sec.length} hesabın tüm oturumları sonlandırılsın mı?`, true)) temizle(); }}>Oturumları sonlandır</button>
            </>
          )}
          sutunlar={[
            { anahtar: 'displayName', baslik: 'Hesap', genislik: 'minmax(200px,2fr)', sirala: true, deger: (x) => `${x.displayName} ${x.email} ${x.uid}`, hucre: (x) => <span className="m16-kisalt"><KisiBag anahtar={`u:${x.uid}`} git={git}><strong>{x.displayName || x.email}</strong></KisiBag> <small style={{ color: 'var(--color-ink-3)' }}>{x.email}</small></span> },
            { anahtar: 'role', baslik: 'Rol', genislik: '110px', deger: (x) => x.role, hucre: (x) => <span><RolRozeti rol={x.role} />{x.isOwner && <Rozet ton="vurgu">sahip</Rozet>}</span> },
            { anahtar: 'suspended', baslik: 'Askı', genislik: 'minmax(140px,1fr)', deger: (x) => (x.suspended ? 1 : 0), sirala: true, hucre: (x) => (x.suspended ? <Rozet ton="kotu" title={x.suspension?.reason}>Askıda{x.suspension?.until ? ` · ${tarihMetni(x.suspension.until)}` : ''}</Rozet> : '—') },
            { anahtar: 'sessionsRevokedAt', baslik: 'Oturum kesildi', genislik: '120px', deger: (x) => x.sessionsRevokedAt || '', hucre: (x) => (x.sessionsRevokedAt ? zamanMetni(x.sessionsRevokedAt) : '—'), gizli: true },
            { anahtar: 'lastLoginAt', baslik: 'Son giriş', genislik: '110px', sirala: true, deger: (x) => x.lastLoginAt || '', hucre: (x) => (x.lastLoginAt ? zamanMetni(x.lastLoginAt) : '—') },
            { anahtar: 'gecmis', baslik: 'Son işlem', genislik: 'minmax(140px,1fr)', deger: (x) => x.accessHistory?.slice(-1)[0]?.at || '', hucre: (x) => { const h = x.accessHistory?.slice(-1)[0]; return h ? <span className="m16-kisalt">{h.kind} · {zamanMetni(h.at)}</span> : '—'; } },
          ]}
          bosMetin="Kayıtlı hesap yok."
        />
      )}
    </>
  );
}
