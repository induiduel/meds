import React, { useState } from 'react';
import { SayfaBasligi, VeriTablosu, AyrintiCekmecesi, Rozet, Yukleniyor, Hata, adminIstek, bildir, onayIste, useAdminSorgu, zamanMetni } from '../kit';
import type { SayfaProps } from '../menu';
import { MesajTablosu } from './ortak/mesajTablosu';
import './ortak/ts16.css';

type Oda = { id: number; tur: 'dm' | 'grup'; ad: string | null; kod: string | null; olusturan: string; olusturma: string; son: string; kapali: string | null; kapatan: string | null; uye: number; mesaj: number; uye_adlari: string | null };
type Uye = { uid: string; ad: string; katilma: string; mesaj: number; sessiz: boolean };

const odaAdi = (o: Oda) => (o.tur === 'grup' ? o.ad || `Grup #${o.id}` : `Birebir: ${o.uye_adlari || '#' + o.id}`);

/** Topluluk › Sohbet odaları — liste, üyeler, kapat/arşivle, davet kodu sıfırla. /manage/topluluk/sohbet/<id> çekmeceyi açar. */
export default function SohbetOdalari({ id, git }: SayfaProps) {
  const [surum, setSurum] = useState(0);
  const acikId = id ? Number(id) : null;
  const ac = (o: Oda | null) => git(o ? `topluluk/sohbet/${o.id}${window.location.search}` : `topluluk/sohbet${window.location.search}`, { degistir: true });
  return (
    <>
      <SayfaBasligi baslik="Sohbet odaları" aciklama="Grup ve birebir sohbetler. Kapatılan odaya kimse katılamaz ve mesaj yazamaz; eski mesajlar okunur kalır." />
      <VeriTablosu<Oda>
        key={surum}
        kimlik="topluluk-sohbet" kaynak="/api/admin/topluluk/odalar"
        canliOlay={['topluluk_changed', 'topluluk_sohbet']}
        aramaYeri="Oda adı, üye adı ya da kimlik…"
        satirKimligi={(o) => String(o.id)} etkin={acikId ? String(acikId) : null} satirTikla={ac}
        suzgecler={[
          { anahtar: 'tur', etiket: 'Tür', secenekler: [{ deger: 'grup', etiket: 'Grup' }, { deger: 'dm', etiket: 'Birebir' }] },
          { anahtar: 'durum', etiket: 'Durum', secenekler: [{ deger: 'acik', etiket: 'Açık' }, { deger: 'kapali', etiket: 'Kapalı' }] },
        ]}
        sutunlar={[
          { anahtar: 'ad', baslik: 'Oda', sirala: true, genislik: 'minmax(180px,2fr)', hucre: (o) => <span className="m16-kisalt">{odaAdi(o)}</span> },
          { anahtar: 'tur', baslik: 'Tür', genislik: '80px', hucre: (o) => <Rozet ton={o.tur === 'grup' ? 'bilgi' : 'notr'}>{o.tur === 'grup' ? 'Grup' : 'Birebir'}</Rozet> },
          { anahtar: 'uye', baslik: 'Üye', sirala: true, genislik: '64px', hizala: 'sag' },
          { anahtar: 'mesaj', baslik: 'Mesaj', sirala: true, genislik: '72px', hizala: 'sag' },
          { anahtar: 'son', baslik: 'Son etkinlik', sirala: true, genislik: '112px', hucre: (o) => <time dateTime={o.son}>{zamanMetni(o.son)}</time> },
          { anahtar: 'kapali', baslik: 'Durum', genislik: '84px', hucre: (o) => (o.kapali ? <Rozet ton="uyari" title={o.kapatan || ''}>Kapalı</Rozet> : <Rozet ton="iyi">Açık</Rozet>) },
          { anahtar: 'olusturma', baslik: 'Kuruldu', sirala: true, genislik: '104px', gizli: true, hucre: (o) => zamanMetni(o.olusturma) },
        ]}
      />
      <OdaCekmecesi id={acikId} kapat={() => ac(null)} degisti={() => setSurum((x) => x + 1)} git={git} />
    </>
  );
}

function OdaCekmecesi({ id, kapat, degisti, git }: { id: number | null; kapat: () => void; degisti: () => void; git: SayfaProps['git'] }) {
  const s = useAdminSorgu<{ oda: Oda; uyeler: Uye[] }>(id ? `/api/admin/topluluk/odalar/${id}` : null, { canliOlay: ['topluluk_changed'] });
  const o = s.veri?.oda;
  const hata = (e: any) => bildir(e?.message || String(e), 'kotu');
  const sonra = () => { void s.yenile(); degisti(); };
  const kapatAc = async () => {
    if (!o) return;
    const kapali = !o.kapali;
    if (!(await onayIste({ baslik: kapali ? 'Oda kapatılsın mı?' : 'Oda yeniden açılsın mı?', aciklama: kapali ? 'Üyeler eski mesajları görür ama yeni mesaj yazamaz; davet koduyla katılım kapanır.' : 'Üyeler yeniden yazabilir.', onayMetni: kapali ? 'Kapat' : 'Aç', tehlikeli: kapali }))) return;
    try { await adminIstek(`/api/admin/topluluk/odalar/${o.id}/kapat`, { yontem: 'POST', govde: { kapali } }); bildir(kapali ? 'Oda kapatıldı.' : 'Oda açıldı.', 'iyi'); sonra(); } catch (e) { hata(e); }
  };
  const kodSifirla = async () => {
    if (!o || !(await onayIste({ baslik: 'Davet kodu sıfırlansın mı?', aciklama: 'Eski davet bağlantıları çalışmaz olur. Mevcut üyeler etkilenmez.', onayMetni: 'Sıfırla' }))) return;
    try { await adminIstek(`/api/admin/topluluk/odalar/${o.id}/kod-sifirla`, { yontem: 'POST', govde: {} }); bildir('Davet kodu yenilendi.', 'iyi'); sonra(); } catch (e) { hata(e); }
  };
  const uyeCikar = async (u: Uye) => {
    if (!o || !(await onayIste({ baslik: `${u.ad} odadan çıkarılsın mı?`, aciklama: 'Kişi davet koduyla yeniden katılabilir; engellemek için kodu da sıfırlayın.', onayMetni: 'Çıkar', tehlikeli: true }))) return;
    try { await adminIstek(`/api/admin/topluluk/odalar/${o.id}/uyeler/${encodeURIComponent(u.uid)}`, { yontem: 'DELETE' }); bildir('Üye çıkarıldı.', 'iyi'); sonra(); } catch (e) { hata(e); }
  };
  return (
    <AyrintiCekmecesi acik={id != null} kapat={kapat} genis
      baslik={o ? odaAdi({ ...o, uye_adlari: s.veri?.uyeler.map((u) => u.ad).join(', ') || null }) : `Oda #${id ?? ''}`}
      altBaslik={o ? `#${o.id} · kuruldu ${new Date(o.olusturma).toLocaleString('tr-TR')}` : ''}
      kayit={s.veri} hedef={id ? `oda:${id}` : undefined}
      ekSekmeler={id ? [{ id: 'mesajlar', etiket: 'Mesajlar', icerik: <MesajTablosu git={git} kimlik="topluluk-oda-mesaj" kaynak={`/api/admin/topluluk/odalar/${id}/mesajlar`} adresteDurum={false} /> }] : []}
      eylemler={o && (
        <div className="m16-ts-eylem">
          {o.tur === 'grup' && <button type="button" className="m16-btn" onClick={kodSifirla}>Davet kodunu sıfırla</button>}
          <button type="button" className={`m16-btn ${o.kapali ? '' : 'tehlike'}`} onClick={kapatAc}>{o.kapali ? 'Odayı aç' : 'Odayı kapat'}</button>
        </div>
      )}
    >
      {s.hata ? <Hata hata={s.hata} yenile={s.yenile} /> : !o ? <Yukleniyor satir={4} /> : (
        <>
          <dl className="m16-satirlar">
            <dt>Tür</dt><dd>{o.tur === 'grup' ? 'Grup' : 'Birebir'}</dd>
            {o.tur === 'grup' && <><dt>Davet kodu</dt><dd><code>{o.kod || '—'}</code></dd></>}
            <dt>Kuran</dt><dd><code>{o.olusturan}</code></dd>
            <dt>Son etkinlik</dt><dd>{new Date(o.son).toLocaleString('tr-TR')}</dd>
            <dt>Durum</dt><dd>{o.kapali ? `Kapalı (${o.kapatan || '—'}, ${new Date(o.kapali).toLocaleString('tr-TR')})` : 'Açık'}</dd>
          </dl>
          <h3>Üyeler ({s.veri!.uyeler.length})</h3>
          <ul className="m16-liste">
            {s.veri!.uyeler.map((u) => (
              <li key={u.uid}>
                <span className="m16-kisalt" title={u.uid}>{u.ad}</span>
                <small>{u.mesaj} mesaj</small>
                <time>{zamanMetni(u.katilma)}</time>
                <button type="button" className="m16-btn hayalet" onClick={() => git(`kisi/${encodeURIComponent(u.uid)}`)}>Kişi</button>
                <button type="button" className="m16-btn hayalet" onClick={() => uyeCikar(u)}>Çıkar</button>
              </li>
            ))}
          </ul>
        </>
      )}
    </AyrintiCekmecesi>
  );
}
