import React, { Suspense, lazy } from 'react';
import { VeriTablosu, SayfaBasligi, Rozet, Durum, zamanMetni, adminIstek, bildir, onayIste, Yukleniyor, useAdminSorgu, IstatistikIzgara, IstatistikKart } from '../kit';
import type { SayfaProps } from '../menu';
import { RolRozeti, sureMetni, kisiYolu, ETKINLIK_ETIKET } from './kisiOrtak';

const Kisi360 = lazy(() => import('./Kisi360'));

type KisiSatiri = {
  key: string; kind: 'account' | 'guest'; agent: string; uid: string | null; email: string | null; name: string; studentNumber: string | null;
  role: string; lastSeen: string | null; online: boolean; deviceCount: number; deviceNames: string[]; totalSeconds: number; weekSeconds: number;
  accuracy: number | null; testCount: number; counts: Record<string, number>; study: { sn: number; haftaSn: number; konu: number; bitti: number } | null;
  donem: number | null; kurul: number | null; universite: string; gizli: boolean; askida: boolean; etkinlik: string;
};

/** Kullanıcılar › Kişiler — sunucu sayfalı liste; /kisi/<anahtar>[/<sekme>] 360° görünümü açar. */
export default function KisiListe({ id, altYol, git }: SayfaProps) {
  if (id) {
    return (
      <Suspense fallback={<Yukleniyor satir={6} />}>
        <Kisi360 anahtar={id} sekme={altYol[1]} git={git} />
      </Suspense>
    );
  }
  return <Liste git={git} />;
}

function Liste({ git }: { git: SayfaProps['git'] }) {
  // Sayaçlar: tek satırlık istek (toplamlar her yanıtta gelir)
  const ozet = useAdminSorgu<{ toplamlar?: Record<string, number> }>('/api/admin/people', { sorgu: { sayfa: 0, boyut: 1 }, canliOlay: ['people_changed'] });
  const t = ozet.veri?.toplamlar;
  const rolDegistir = async (ids: string[], satirlar: string[], temizle: () => void, rol: string) => {
    if (!ids.length) return bildir('Seçimde giriş hesabı yok (misafir satırlarına rol verilemez).', 'kotu');
    if (!(await onayIste({ baslik: `${ids.length} hesabın rolü “${rol}” yapılsın mı?`, onayMetni: 'Uygula' }))) return;
    try {
      const r = await adminIstek('/api/admin/people-access/role', { yontem: 'POST', govde: { uids: ids, role: rol } });
      bildir(`${r.changed?.length || 0} hesap güncellendi${r.skipped?.length ? `, ${r.skipped.length} atlandı` : ''}.`);
      temizle();
    } catch (e: any) { bildir(e.message, 'kotu'); }
    void satirlar;
  };
  const askiya = async (ids: string[], temizle: () => void) => {
    if (!ids.length) return bildir('Seçimde giriş hesabı yok.', 'kotu');
    const gerekce = window.prompt(`${ids.length} hesap askıya alınacak. Gerekçe:`);
    if (!gerekce || gerekce.trim().length < 3) return;
    try {
      const r = await adminIstek('/api/admin/people-access/suspend', { yontem: 'POST', govde: { uids: ids, reason: gerekce.trim() } });
      bildir(`${r.changed?.length || 0} hesap askıya alındı.`);
      temizle();
    } catch (e: any) { bildir(e.message, 'kotu'); }
  };
  const uidOf = (k: string) => (k.startsWith('u:') ? k.slice(2) : '');

  return (
    <>
      <SayfaBasligi baslik="Kişiler" aciklama="Hesaplar ve misafir cihazlar: son görülme, kullanım, çalışma, kurul ve üniversite. Satıra tıklayınca 360° görünüm açılır." />
      <IstatistikIzgara>
        <IstatistikKart etiket="Kişi" deger={t?.people ?? '—'} yukleniyor={!t && ozet.yukleniyor} />
        <IstatistikKart etiket="Hesap" deger={t?.accounts ?? '—'} />
        <IstatistikKart etiket="Çevrimiçi" deger={t?.online ?? '—'} ton="iyi" />
        <IstatistikKart etiket="Bu hafta" deger={t ? sureMetni(t.weekSeconds) : '—'} alt="toplam etkin süre" />
      </IstatistikIzgara>
      <VeriTablosu<KisiSatiri>
        kimlik="kisi-liste"
        kaynak="/api/admin/people"
        canliOlay={['people_changed']}
        aramaYeri="Ad, e-posta, öğrenci no, üniversite, cihaz…"
        satirKimligi={(s) => s.key}
        satirTikla={(s) => git(kisiYolu(s.key))}
        secim
        topluEylemler={(secili, temizle) => {
          const uids = secili.map(uidOf).filter(Boolean);
          return (
            <>
              <button className="m16-btn" onClick={() => rolDegistir(uids, secili, temizle, 'student')}>Öğrenci yap</button>
              <button className="m16-btn" onClick={() => rolDegistir(uids, secili, temizle, 'moderator')}>Moderatör yap</button>
              <button className="m16-btn tehlike" onClick={() => askiya(uids, temizle)}>Askıya al</button>
            </>
          );
        }}
        suzgecler={[
          { anahtar: 'etkinlik', etiket: 'Etkinlik', secenekler: Object.entries(ETKINLIK_ETIKET).map(([deger, etiket]) => ({ deger, etiket })) },
          { anahtar: 'tur', etiket: 'Tür', secenekler: [{ deger: 'hesap', etiket: 'Hesap' }, { deger: 'misafir', etiket: 'Misafir' }, { deger: 'makine', etiket: 'Bot/boş' }] },
          { anahtar: 'rol', etiket: 'Rol', secenekler: [{ deger: 'student', etiket: 'Öğrenci' }, { deger: 'moderator', etiket: 'Moderatör' }, { deger: 'admin', etiket: 'Yönetici' }] },
          { anahtar: 'kurul', etiket: 'Kurul', secenekler: [1, 2, 3, 4, 5, 6].map((k) => ({ deger: String(k), etiket: `${k}. kurul` })) },
          { anahtar: 'askida', etiket: 'Askı', secenekler: [{ deger: '1', etiket: 'Askıda' }] },
        ]}
        sutunlar={[
          { anahtar: 'name', baslik: 'Kişi', sirala: 'ad', genislik: 'minmax(200px,2fr)', hucre: (s) => (
            <span style={{ display: 'flex', gap: 6, alignItems: 'center', minWidth: 0 }}>
              <Durum ton={s.online ? 'iyi' : 'notr'}>{''}</Durum>
              <span className="m16-kisalt" title={s.email || s.key}><strong>{s.name}</strong>{s.email ? <small style={{ color: 'var(--color-ink-3)' }}> · {s.email}</small> : null}</span>
            </span>
          ) },
          { anahtar: 'role', baslik: 'Rol', genislik: '110px', hucre: (s) => <span style={{ display: 'flex', gap: 4 }}><RolRozeti rol={s.role} />{s.askida && <Rozet ton="kotu">Askıda</Rozet>}</span> },
          { anahtar: 'kurul', baslik: 'Kurul', sirala: true, genislik: '70px', hizala: 'orta', hucre: (s) => (s.kurul ? `${s.donem || 3}/${s.kurul}` : '—') },
          { anahtar: 'universite', baslik: 'Üniversite', genislik: 'minmax(120px,1fr)', gizli: true, hucre: (s) => s.universite || '—' },
          { anahtar: 'lastSeen', baslik: 'Son görülme', sirala: 'son', genislik: '120px', hucre: (s) => (s.online ? <Rozet ton="iyi">şimdi</Rozet> : s.lastSeen ? <time dateTime={s.lastSeen}>{zamanMetni(s.lastSeen)}</time> : '—') },
          { anahtar: 'weekSeconds', baslik: '7 gün', sirala: 'hafta', genislik: '100px', hizala: 'sag', hucre: (s) => sureMetni(s.weekSeconds) },
          { anahtar: 'study', baslik: 'Çalışma', sirala: 'calisma', genislik: '100px', hizala: 'sag', hucre: (s) => (s.study ? sureMetni(s.study.sn) : '—') },
          { anahtar: 'bitti', baslik: 'Bitti/konu', genislik: '84px', hizala: 'sag', gizli: true, hucre: (s) => (s.study ? `${s.study.bitti}/${s.study.konu}` : '—') },
          { anahtar: 'accuracy', baslik: 'Doğruluk', sirala: 'dogruluk', genislik: '80px', hizala: 'sag', gizli: true, hucre: (s) => (s.accuracy == null ? '—' : `%${s.accuracy}`) },
          { anahtar: 'deviceCount', baslik: 'Cihaz', genislik: '60px', hizala: 'sag', hucre: (s) => s.deviceCount },
          { anahtar: 'katki', baslik: 'Olay', sirala: 'katki', genislik: '64px', hizala: 'sag', gizli: true, hucre: (s) => s.counts?.events || 0 },
        ]}
      />
    </>
  );
}
