import React, { useState } from 'react';
import { ArrowLeft, RefreshCw } from 'lucide-react';
import {
  SayfaBasligi, useAdminSorgu, adminIstek, Yukleniyor, Hata, BosDurum, Rozet, Durum, IstatistikIzgara, IstatistikKart, VeriTablosu,
  AyrintiCekmecesi, JsonDuzenleyici, JsonGoruntuleyici, DegisiklikGecmisi, onayIste, bildir, zamanMetni,
} from '../kit';
import type { SayfaProps } from '../menu';
import { RolRozeti, sureMetni, kisiYolu, tarihMetni, olayEtiket, KisiBag } from './kisiOrtak';

type Git = SayfaProps['git'];
const SEKMELER = [
  ['ozet', 'Özet'], ['cihaz', 'Cihazlar'], ['etkinlik', 'Etkinlik'], ['calisma', 'Çalışma'], ['basarim', 'Puan ve ATP'],
  ['sosyal', 'Sosyal ve erişim'], ['katki', 'Katkılar'], ['veri', 'Profil verisi'],
] as const;

/** Kullanıcılar › Kişi 360° (/manage/kisi/<anahtar>/<sekme>) */
export default function Kisi360({ anahtar, sekme = 'ozet', git }: { anahtar: string; sekme?: string; git: Git }) {
  const d = useAdminSorgu<any>(`/api/admin/people/${encodeURIComponent(anahtar)}`, { canliOlay: ['people_changed'] });
  const p = d.veri?.person;
  const uid: string | null = p?.uid || (anahtar.startsWith('u:') ? anahtar.slice(2) : null);
  return (
    <>
      <SayfaBasligi
        baslik={<span style={{ display: 'inline-flex', gap: 8, alignItems: 'center' }}>
          <button className="m16-btn ikon hayalet" aria-label="Kişi listesine dön" onClick={() => git('kisi')}><ArrowLeft className="w-4 h-4" aria-hidden /></button>
          {p?.name || anahtar}
        </span>}
        aciklama={p ? <>{p.email || 'e-postasız'} · {p.kind === 'account' ? 'hesap' : 'misafir'} · <code>{p.key}</code></> : undefined}
        eylemler={<button className="m16-btn hayalet" onClick={() => d.yenile()}><RefreshCw className="w-4 h-4" aria-hidden /> Yenile</button>}
      >
        <nav className="m16-sekmeler" aria-label="Kişi sekmeleri">
          {SEKMELER.map(([id, ad]) => (
            <button key={id} className={sekme === id ? 'on' : ''} aria-current={sekme === id ? 'page' : undefined} onClick={() => git(kisiYolu(anahtar, id === 'ozet' ? '' : id), { degistir: true })}>{ad}</button>
          ))}
        </nav>
      </SayfaBasligi>
      {d.hata && !d.veri ? <Hata hata={d.hata} yenile={d.yenile} /> : !d.veri ? <Yukleniyor satir={6} /> : (
        <>
          {sekme === 'ozet' && <Ozet d={d.veri} />}
          {sekme === 'cihaz' && <Cihazlar d={d.veri} yenile={d.yenile} />}
          {sekme === 'etkinlik' && <Etkinlik anahtar={anahtar} />}
          {sekme === 'calisma' && <Calisma anahtar={anahtar} d={d.veri} yenile={d.yenile} />}
          {sekme === 'basarim' && (uid ? <Basarim uid={uid} /> : <BosDurum baslik="Misafir kaydı" aciklama="Puan ve ATP yalnız giriş hesaplarında tutulur." />)}
          {sekme === 'sosyal' && <Sosyal anahtar={anahtar} git={git} />}
          {sekme === 'katki' && <Katkilar d={d.veri} />}
          {sekme === 'veri' && <ProfilVerisi anahtar={anahtar} />}
        </>
      )}
    </>
  );
}

function Ozet({ d }: { d: any }) {
  const p = d.person, c = d.calisma?.ozet, s = d.score;
  return (
    <>
      <IstatistikIzgara>
        <IstatistikKart etiket="Toplam kullanım" deger={sureMetni(d.usage?.totalSeconds)} alt={`${d.usage?.sessions || 0} oturum`} />
        <IstatistikKart etiket="Çalışma (7 gün)" deger={sureMetni(c?.haftaSn)} alt={`toplam ${sureMetni(c?.sn)}`} />
        <IstatistikKart etiket="Konu" deger={c ? `${c.bitti}/${c.konu}` : '—'} alt="bitti / başlanan" />
        <IstatistikKart etiket="Test doğruluğu" deger={s?.accuracy == null ? '—' : `%${s.accuracy}`} alt={`${s?.testCount || 0} test · net ${s?.net ?? 0}`} />
        <IstatistikKart etiket="Cihaz" deger={d.devices?.length || 0} ton={d.devices?.some((x: any) => x.online) ? 'iyi' : 'notr'} alt={d.devices?.some((x: any) => x.online) ? 'çevrimiçi' : undefined} />
      </IstatistikIzgara>
      <div className="m16-izgara-2">
        <section className="m16-kart">
          <h2>Hesap</h2>
          <dl className="m16-satirlar">
            <dt>Rol</dt><dd><RolRozeti rol={p.kind === 'guest' ? 'guest' : p.role} /></dd>
            <dt>Öğrenci no</dt><dd>{p.studentNumber || '—'}</dd>
            <dt>Telefon</dt><dd>{p.phone || '—'}</dd>
            <dt>Kayıt</dt><dd>{tarihMetni(p.createdAt)}</dd>
            <dt>Son giriş</dt><dd>{tarihMetni(p.lastLoginAt)}</dd>
            <dt>Son profil kaydı</dt><dd>{tarihMetni(p.lastBackupAt)}</dd>
            <dt>Doğrulanmış</dt><dd>{p.verified ? 'evet' : 'hayır'}</dd>
            <dt>Profil anahtarı</dt><dd>{d.study?.kvCount ?? 0}</dd>
          </dl>
        </section>
        <section className="m16-kart">
          <h2>Kullanım (son günler)</h2>
          {(d.usage?.daily || []).length ? (
            <ul className="m16-liste">{d.usage.daily.slice(0, 14).map((u: any) => <li key={u.day}><span className="m16-kisalt">{u.day}</span><span>{sureMetni(u.seconds)}</span></li>)}</ul>
          ) : <BosDurum baslik="Cihaz kullanımı yok" />}
        </section>
      </div>
      <section className="m16-kart">
        <h2>Yönetici geçmişi</h2>
        <DegisiklikGecmisi hedef={`kisi:${p.uid || p.key}`} boyut={15} />
      </section>
    </>
  );
}

function Cihazlar({ d, yenile }: { d: any; yenile: () => void }) {
  const unut = async (id: string) => {
    if (!(await onayIste({ baslik: 'Cihaz unutulsun mu?', aciklama: 'Cihaz satırı ve günlük kullanımı silinir; olay günlüğü kalır.', tehlikeli: true, onayMetni: 'Unut' }))) return;
    try { await adminIstek(`/api/admin/people/devices/${encodeURIComponent(id)}`, { yontem: 'DELETE' }); bildir('Cihaz unutuldu.'); yenile(); } catch (e: any) { bildir(e.message, 'kotu'); }
  };
  return (
    <VeriTablosu<any>
      kimlik="kisi-cihaz" adresteDurum={false} ogeler={d.devices || []} satirKimligi={(x) => x.device_id}
      sutunlar={[
        { anahtar: 'label', baslik: 'Cihaz', genislik: 'minmax(180px,2fr)', deger: (x) => x.label, hucre: (x) => <span><Durum ton={x.online ? 'iyi' : 'notr'}>{x.label || x.device_id}</Durum>{x.agent !== 'insan' && <Rozet ton="uyari">{x.note || x.agent}</Rozet>}</span> },
        { anahtar: 'platform', baslik: 'Platform', genislik: '120px', deger: (x) => `${x.platform} ${x.browser}`, hucre: (x) => `${x.platform || ''} ${x.browser || ''}` },
        { anahtar: 'first_seen', baslik: 'İlk', genislik: '110px', sirala: true, deger: (x) => x.first_seen, hucre: (x) => tarihMetni(x.first_seen) },
        { anahtar: 'last_seen', baslik: 'Son', genislik: '110px', sirala: true, deger: (x) => x.last_seen, hucre: (x) => zamanMetni(x.last_seen) },
        { anahtar: 'active_seconds', baslik: 'Süre', genislik: '100px', hizala: 'sag', sirala: true, deger: (x) => x.active_seconds, hucre: (x) => sureMetni(x.active_seconds) },
        { anahtar: 'sessions', baslik: 'Oturum', genislik: '70px', hizala: 'sag', deger: (x) => x.sessions },
        { anahtar: 'last_path', baslik: 'Son sayfa', genislik: 'minmax(120px,1fr)', gizli: true },
        { anahtar: 'eylem', baslik: '', genislik: '70px', hucre: (x) => <button className="m16-btn hayalet" onClick={(e) => { e.stopPropagation(); void unut(x.device_id); }}>Unut</button> },
      ]}
      bosMetin="Kayıtlı cihaz yok."
    />
  );
}

function Etkinlik({ anahtar }: { anahtar: string }) {
  const [tur, setTur] = useState('');
  const [ek, setEk] = useState<any[]>([]);
  const [imlec, setImlec] = useState<number | null>(null);
  const [yukleniyor, setYukleniyor] = useState(false);
  const yol = `/api/admin/people/${encodeURIComponent(anahtar)}/olaylar`;
  const ilk = useAdminSorgu<any>(yol, { sorgu: { tur: tur || undefined, boyut: 50 }, canliOlay: ['people_changed'] });
  React.useEffect(() => { setEk([]); setImlec(null); }, [tur, ilk.veri]);
  const sonraki = imlec ?? ilk.veri?.sonraki ?? null;
  const daha = async () => {
    if (!sonraki) return;
    setYukleniyor(true);
    try {
      const r = await adminIstek<any>(yol, { sorgu: { tur: tur || undefined, boyut: 50, imlec: sonraki } });
      setEk((x) => [...x, ...r.ogeler]); setImlec(r.sonraki ?? 0);
    } catch (e: any) { bildir(e.message, 'kotu'); } finally { setYukleniyor(false); }
  };
  if (ilk.hata && !ilk.veri) return <Hata hata={ilk.hata} yenile={ilk.yenile} />;
  if (!ilk.veri) return <Yukleniyor satir={8} />;
  if (ilk.veri.veritabani === false) return <BosDurum baslik="Veritabanı kapalı" aciklama="Olay günlüğü meds-pg'den okunur." />;
  const ogeler = [...ilk.veri.ogeler, ...ek];
  return (
    <section className="m16-kart">
      <div className="m16-cip-grup" style={{ marginBottom: 8 }}>
        <button className={`m16-cip${!tur ? ' on' : ''}`} onClick={() => setTur('')}>Tümü</button>
        {(ilk.veri.turler || []).map((t: any) => <button key={t.kind} className={`m16-cip${tur === t.kind ? ' on' : ''}`} onClick={() => setTur(t.kind)}>{olayEtiket(t.kind)} <em>{t.n}</em></button>)}
      </div>
      {!ogeler.length ? <BosDurum baslik="Olay yok" /> : (
        <ul className="m16-liste">
          {ogeler.map((o) => (
            <li key={o.id}>
              <Rozet>{olayEtiket(o.kind)}</Rozet>
              <span className="m16-kisalt" title={o.body || o.label}>{o.label}{o.body ? ` — ${o.body}` : ''}</span>
              <time dateTime={o.at} title={tarihMetni(o.at)}>{zamanMetni(o.at)}</time>
            </li>
          ))}
        </ul>
      )}
      {sonraki ? <button className="m16-btn" style={{ marginTop: 8 }} disabled={yukleniyor} onClick={daha}>{yukleniyor ? 'Yükleniyor…' : 'Daha eski olaylar'}</button> : null}
    </section>
  );
}

function Calisma({ anahtar, d, yenile }: { anahtar: string; d: any; yenile: () => void }) {
  const konular: any[] = d.calisma?.konular || [];
  const islem = async (ops: any[] | null, metin: string, hepsini = false) => {
    if (!(await onayIste({ baslik: metin, tehlikeli: hepsini, yazilacak: hepsini ? 'SIFIRLA' : undefined, onayMetni: 'Uygula' }))) return;
    try {
      const r = await adminIstek<any>(`/api/admin/people/${encodeURIComponent(anahtar)}/calisma`, { yontem: 'PATCH', govde: hepsini ? { hepsiniSifirla: true } : { ops } });
      bildir(`${r.changed} konu güncellendi.`); yenile();
    } catch (e: any) { bildir(e.message, 'kotu'); }
  };
  const ad = d.calisma?.ozet;
  return (
    <>
      <IstatistikIzgara>
        <IstatistikKart etiket="Toplam" deger={sureMetni(ad?.sn)} />
        <IstatistikKart etiket="7 gün" deger={sureMetni(ad?.haftaSn)} />
        <IstatistikKart etiket="Soru" deger={ad?.soru ?? 0} />
        <IstatistikKart etiket="Bitti" deger={`${ad?.bitti ?? 0}/${ad?.konu ?? 0}`} />
      </IstatistikIzgara>
      <VeriTablosu<any>
        kimlik="kisi-calisma" adresteDurum={false} ogeler={konular} satirKimligi={(k) => k.id} secim
        aramaYeri="Konu ara…"
        aracEk={konular.length ? <button className="m16-btn tehlike" onClick={() => islem(null, 'Tüm çalışma kaydı sıfırlansın mı?', true)}>Tümünü sıfırla</button> : null}
        topluEylemler={(sec, temizle) => (
          <>
            <button className="m16-btn" onClick={async () => { await islem(sec.map((id) => ({ id, durum: 'bitti' })), `${sec.length} konu bitti yapılsın mı?`); temizle(); }}>Bitti yap</button>
            <button className="m16-btn" onClick={async () => { await islem(sec.map((id) => ({ id, durum: 'acik' })), `${sec.length} konu açık yapılsın mı?`); temizle(); }}>Açık yap</button>
            <button className="m16-btn tehlike" onClick={async () => { await islem(sec.map((id) => ({ id, sifirla: true })), `${sec.length} konu sıfırlansın mı?`); temizle(); }}>Sıfırla</button>
          </>
        )}
        sutunlar={[
          { anahtar: 'modul', baslik: 'Modül', genislik: '80px', deger: (k) => k.modul, hucre: (k) => <Rozet>{k.modul}</Rozet> },
          { anahtar: 'konu', baslik: 'Konu', genislik: 'minmax(200px,2fr)', deger: (k) => k.konu },
          { anahtar: 'durum', baslik: 'Durum', genislik: '90px', deger: (k) => k.durum || '', hucre: (k) => (k.durum ? <Rozet ton={k.durum === 'bitti' ? 'iyi' : k.durum === 'tekrar' ? 'bilgi' : 'notr'}>{k.durum}{k.adm ? ' ·y' : ''}</Rozet> : '—') },
          { anahtar: 'sn', baslik: 'Süre', genislik: '100px', hizala: 'sag', sirala: true, deger: (k) => k.sn, hucre: (k) => sureMetni(k.sn) },
          { anahtar: 'soru', baslik: 'Soru', genislik: '60px', hizala: 'sag', sirala: true, deger: (k) => k.soru },
          { anahtar: 'sonAt', baslik: 'Son', genislik: '110px', sirala: true, deger: (k) => k.sonAt || '', hucre: (k) => (k.sonAt ? zamanMetni(k.sonAt) : '—') },
        ]}
        bosMetin="Çalışma kaydı yok."
      />
      <p style={{ color: 'var(--color-ink-3)', fontSize: 12 }}>Yönetici düzeltmesi <code>adm</code> damgası taşır (·y); öğrencinin cihazındaki eski değer bunu ezmez.</p>
    </>
  );
}

function Basarim({ uid }: { uid: string }) {
  const d = useAdminSorgu<any>(`/api/admin/basarim/kisi/${encodeURIComponent(uid)}`, { canliOlay: ['basarim_changed'] });
  const [tur, setTur] = useState('puan');
  const [miktar, setMiktar] = useState('');
  const [gerekce, setGerekce] = useState('');
  if (d.hata && !d.veri) return <Hata hata={d.hata} yenile={d.yenile} />;
  if (!d.veri) return <Yukleniyor satir={5} />;
  const k = d.veri.kisi, o = d.veri.ozet || {};
  const uygula = async (e: React.FormEvent) => {
    e.preventDefault();
    if (gerekce.trim().length < 3) return bildir('Gerekçe yazın.', 'kotu');
    if (!(await onayIste({ baslik: `${tur === 'puan' ? 'Puan' : 'ATP'} ${miktar} uygulansın mı?`, onayMetni: 'Uygula' }))) return;
    try {
      const r = await adminIstek(`/api/admin/basarim/kisi/${encodeURIComponent(uid)}/islem`, { yontem: 'POST', govde: { tur, veri: { miktar: Number(miktar) }, gerekce } });
      d.setVeri(r); setMiktar(''); setGerekce(''); bildir('Uygulandı.');
    } catch (e2: any) { bildir(e2.message, 'kotu'); }
  };
  return (
    <>
      <IstatistikIzgara>
        <IstatistikKart etiket="ATP" deger={`${k.atp?.bakiye ?? 0} mol`} alt={k.atp?.kuyruk?.length ? `kuyrukta ${k.atp.kuyruk.reduce((a: number, q: any) => a + q.a, 0)}` : undefined} />
        <IstatistikKart etiket="Puan (toplam)" deger={o.puan?.toplam ?? o.toplamPuan ?? '—'} />
        <IstatistikKart etiket="Dönem/kurul" deger={k.donem ? `${k.donem}/${k.kurul ?? '—'}` : '—'} />
        <IstatistikKart etiket="Açık kilit" deger={Object.keys(k.kilit || {}).length} alt={k.ozel ? `unvan: ${k.ozel.unvan}` : undefined} />
      </IstatistikIzgara>
      <section className="m16-kart">
        <h2>Düzeltme</h2>
        <form onSubmit={uygula} style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
          <select className="m16-girdi" value={tur} onChange={(e) => setTur(e.target.value)} aria-label="İşlem türü">
            <option value="puan">Puan</option><option value="atp">ATP</option>
          </select>
          <input className="m16-girdi" type="number" placeholder="miktar (eksi olabilir)" value={miktar} onChange={(e) => setMiktar(e.target.value)} aria-label="Miktar" style={{ width: 160 }} />
          <input className="m16-girdi" placeholder="gerekçe" value={gerekce} onChange={(e) => setGerekce(e.target.value)} aria-label="Gerekçe" style={{ flex: 1, minWidth: 160 }} />
          <button className="m16-btn birincil" disabled={!Number(miktar)}>Uygula</button>
        </form>
        <p style={{ color: 'var(--color-ink-3)', fontSize: 12 }}>Kilit, unvan ve geri alma işlemleri: Kullanıcılar › Puan ve ATP.</p>
      </section>
      <section className="m16-kart">
        <h2>Defter</h2>
        <ul className="m16-liste">
          {(k.defter || []).slice(0, 100).map((x: any) => (
            <li key={x.id}>
              <Rozet ton={x.t === 'yonetici' ? 'vurgu' : x.geriAlindi ? 'uyari' : 'notr'}>{x.t}</Rozet>
              <span className="m16-kisalt" title={x.ad}>{x.ad}{x.geriAlindi ? ' (geri alındı)' : ''}</span>
              <span>{x.p ? `${x.p > 0 ? '+' : ''}${x.p} p` : ''} {x.a ? `${x.a > 0 ? '+' : ''}${x.a} mol` : ''}</span>
              <time dateTime={x.at}>{zamanMetni(x.at)}</time>
            </li>
          ))}
        </ul>
      </section>
    </>
  );
}

function Sosyal({ anahtar, git }: { anahtar: string; git: Git }) {
  const d = useAdminSorgu<any>(`/api/admin/people/${encodeURIComponent(anahtar)}/sosyal`, { canliOlay: ['arkadas_changed', 'people_changed'] });
  if (d.hata && !d.veri) return <Hata hata={d.hata} yenile={d.yenile} />;
  if (!d.veri) return <Yukleniyor satir={5} />;
  const v = d.veri, e = v.erisim;
  const erisimIslem = async (yol: string, govde: any, baslik: string, tehlikeli = false) => {
    if (!(await onayIste({ baslik, tehlikeli, onayMetni: 'Uygula' }))) return;
    try {
      const r = await adminIstek<any>(`/api/admin/people-access/${yol}`, { yontem: 'POST', govde: { uids: [e.uid], ...govde } });
      if (r.skipped?.length) bildir(r.skipped[0].reason, 'kotu'); else bildir('Uygulandı.');
      d.yenile();
    } catch (x: any) { bildir(x.message, 'kotu'); }
  };
  return (
    <div className="m16-izgara-2">
      <section className="m16-kart">
        <h2>Erişim</h2>
        {!e ? <BosDurum baslik="Giriş hesabı değil" aciklama="Rol ve askı yalnız kayıtlı hesaplarda." /> : (
          <>
            <dl className="m16-satirlar">
              <dt>Rol</dt><dd><RolRozeti rol={e.role} /></dd>
              <dt>Askı</dt><dd>{e.suspension?.active ? <Rozet ton="kotu">Askıda{e.suspension.until ? ` · ${tarihMetni(e.suspension.until)}` : ''}</Rozet> : 'yok'}</dd>
              {e.suspension?.active && <><dt>Gerekçe</dt><dd>{e.suspension.reason}</dd></>}
              <dt>Oturum sonlandırma</dt><dd>{tarihMetni(e.oturumSonlandirAt)}</dd>
            </dl>
            {!e.isOwner && (
              <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginTop: 10 }}>
                <select className="m16-girdi" value={e.role} aria-label="Rol" onChange={(x) => erisimIslem('role', { role: x.target.value }, `Rol “${x.target.value}” yapılsın mı?`)}>
                  <option value="student">Öğrenci</option><option value="moderator">Moderatör</option><option value="admin">Yönetici</option>
                </select>
                {e.suspension?.active
                  ? <button className="m16-btn" onClick={() => erisimIslem('unsuspend', {}, 'Askı kaldırılsın mı?')}>Askıyı kaldır</button>
                  : <button className="m16-btn tehlike" onClick={() => { const r = window.prompt('Askı gerekçesi:'); if (r && r.trim().length >= 3) void erisimIslem('suspend', { reason: r.trim() }, 'Hesap askıya alınsın mı?', true); }}>Askıya al</button>}
                <button className="m16-btn tehlike" onClick={() => erisimIslem('oturum-sonlandir', {}, 'Tüm oturumlar sonlandırılsın mı? Açık cihazlar yeniden giriş ister.', true)}>Oturumları sonlandır</button>
              </div>
            )}
            {e.accessHistory?.length ? (
              <ul className="m16-liste" style={{ marginTop: 10 }}>
                {e.accessHistory.map((h: any, i: number) => <li key={i}><Rozet>{h.kind}</Rozet><span className="m16-kisalt">{h.to || h.reason || ''} · {h.by}</span><time>{zamanMetni(h.at)}</time></li>)}
              </ul>
            ) : null}
          </>
        )}
        {v.bag && <p>Sıralamada bağlı olduğu asıl hesap: <KisiBag anahtar={v.bag.key} git={git}>{v.bag.ad}</KisiBag></p>}
      </section>
      <section className="m16-kart">
        <h2>Gizlilik ve profil</h2>
        <dl className="m16-satirlar">
          <dt>Profil herkese açık</dt><dd>{v.gizlilik.profilGizli ? <Rozet ton="uyari">kapalı</Rozet> : 'açık'}</dd>
          <dt>Son görülme</dt><dd>{v.gizlilik.sonGorulmeGizli ? <Rozet ton="uyari">gizli</Rozet> : 'görünür'}</dd>
          <dt>Sohbette son</dt><dd>{tarihMetni(v.gizlilik.sohbetSon)}</dd>
          <dt>Dönem / kurul</dt><dd>{v.profil?.donem ? `${v.profil.donem} / ${v.profil.kurul ?? '—'}` : '—'}</dd>
          <dt>Üniversite</dt><dd>{v.profil?.universite || '—'}</dd>
        </dl>
      </section>
      <section className="m16-kart">
        <h2>Arkadaşlar ({v.arkadaslar.length})</h2>
        {!v.arkadaslar.length ? <BosDurum baslik="Arkadaş yok" /> : (
          <ul className="m16-liste">{v.arkadaslar.map((a: any) => (
            <li key={a.uid}><span className="m16-kisalt"><KisiBag anahtar={a.key} git={git}>{a.ad}</KisiBag></span><Rozet ton={a.durum === 'kabul' ? 'iyi' : 'notr'}>{a.durum === 'kabul' ? 'arkadaş' : a.yon === 'giden' ? 'istek gönderdi' : 'istek aldı'}</Rozet><time>{zamanMetni(a.at)}</time></li>
          ))}</ul>
        )}
      </section>
      <section className="m16-kart">
        <h2>Sohbet üyelikleri ({v.odalar.length})</h2>
        {!v.odalar.length ? <BosDurum baslik="Sohbet yok" /> : (
          <ul className="m16-liste">{v.odalar.map((o: any) => (
            <li key={o.id}><Rozet>{o.tur === 'dm' ? 'özel' : 'grup'}</Rozet><span className="m16-kisalt">{o.ad || `Oda #${o.id}`} · {o.uye} üye{o.sessiz ? ' · sessiz' : ''}</span><time>{zamanMetni(o.son)}</time></li>
          ))}</ul>
        )}
      </section>
    </div>
  );
}

function Katkilar({ d }: { d: any }) {
  return (
    <VeriTablosu<any>
      kimlik="kisi-katki" adresteDurum={false} ogeler={d.items || []} satirKimligi={(x) => `${x.kind}-${x.id}`} aramaYeri="Katkılarda ara…"
      satirTikla={(x) => x.link && window.open(x.link, '_blank', 'noopener')}
      sutunlar={[
        { anahtar: 'kind', baslik: 'Tür', genislik: '90px', deger: (x) => x.kind, hucre: (x) => <Rozet ton={x.kind === 'report' ? 'uyari' : 'notr'}>{olayEtiket(x.kind)}</Rozet> },
        { anahtar: 'title', baslik: 'Başlık', genislik: 'minmax(200px,2fr)', deger: (x) => `${x.title} ${x.body || ''}`, hucre: (x) => <span className="m16-kisalt" title={x.body}>{x.title}</span> },
        { anahtar: 'source', baslik: 'Kaynak', genislik: '80px', deger: (x) => x.source || '' },
        { anahtar: 'at', baslik: 'Zaman', genislik: '110px', sirala: true, deger: (x) => x.at || '', hucre: (x) => (x.at ? zamanMetni(x.at) : '—') },
      ]}
      bosMetin="Katkı yok."
    />
  );
}

type KvSatir = { anahtar: string; at: string | null; boyut: number; silindi: boolean; korumali: boolean; onizleme: string | null };
function ProfilVerisi({ anahtar }: { anahtar: string }) {
  const kok = `/api/admin/user-data/${encodeURIComponent(anahtar)}`;
  const d = useAdminSorgu<any>(kok, { canliOlay: ['people_changed'] });
  const [acik, setAcik] = useState<string | null>(null);
  if (d.hata && !d.veri) return <Hata hata={d.hata} yenile={d.yenile} />;
  if (!d.veri) return <Yukleniyor satir={6} />;
  return (
    <>
      <p style={{ color: 'var(--color-ink-3)', fontSize: 12.5 }}>
        Öğrenci profilindeki <code>kv</code> anahtarları (data/user_backups). Her açma ve yazma denetim kaydına düşer.
        Yazma son-yazan-kazanır ile cihazlara iner; birikimli ilerleme anahtarları silinemez, cihaz daha büyük değeri geri yazabilir.
      </p>
      <VeriTablosu<KvSatir>
        kimlik="kisi-kv" adresteDurum={false} ogeler={d.veri.ogeler} satirKimligi={(x) => x.anahtar} aramaYeri="Anahtar ara…"
        satirTikla={(x) => setAcik(x.anahtar)} etkin={acik}
        sutunlar={[
          { anahtar: 'anahtar', baslik: 'Anahtar', genislik: 'minmax(200px,2fr)', sirala: true, deger: (x) => x.anahtar, hucre: (x) => <span><code>{x.anahtar}</code> {x.korumali && <Rozet ton="bilgi">birikimli</Rozet>} {x.silindi && <Rozet ton="uyari">silindi</Rozet>}</span> },
          { anahtar: 'onizleme', baslik: 'Değer', genislik: 'minmax(160px,2fr)', deger: (x) => x.onizleme || '', hucre: (x) => <span className="m16-kisalt" style={{ color: 'var(--color-ink-3)' }}>{x.onizleme}</span> },
          { anahtar: 'boyut', baslik: 'Boyut', genislik: '80px', hizala: 'sag', sirala: true, deger: (x) => x.boyut, hucre: (x) => (x.boyut > 1024 ? `${Math.round(x.boyut / 1024)} KB` : `${x.boyut} B`) },
          { anahtar: 'at', baslik: 'Güncelleme', genislik: '110px', sirala: true, deger: (x) => x.at || '', hucre: (x) => (x.at ? zamanMetni(x.at) : '—') },
        ]}
        bosMetin="Profil verisi yok."
      />
      {acik && <KvCekmece kok={kok} anahtar={acik} kapat={() => setAcik(null)} degisti={d.yenile} />}
    </>
  );
}

function KvCekmece({ kok, anahtar, kapat, degisti }: { kok: string; anahtar: string; kapat: () => void; degisti: () => void }) {
  const yol = `${kok}/${encodeURIComponent(anahtar)}`;
  const d = useAdminSorgu<any>(yol);
  const [metin, setMetin] = useState<string | null>(null);
  const kaydet = async (govde: any) => {
    try { await adminIstek(yol, { yontem: 'PUT', govde }); bildir('Kaydedildi.'); d.yenile(); degisti(); setMetin(null); } catch (e: any) { bildir(e.message, 'kotu'); }
  };
  const sil = async () => {
    if (!(await onayIste({ baslik: `“${anahtar}” silinsin mi?`, aciklama: 'Mezar taşı yazılır; öğrencinin cihazlarından da silinir.', tehlikeli: true, yazilacak: 'SIL', onayMetni: 'Sil' }))) return;
    try { await adminIstek(yol, { yontem: 'DELETE' }); bildir('Silindi.'); degisti(); kapat(); } catch (e: any) { bildir(e.message, 'kotu'); }
  };
  const v = d.veri;
  return (
    <AyrintiCekmecesi acik kapat={kapat} baslik={<code>{anahtar}</code>} altBaslik={v ? `güncelleme ${tarihMetni(v.at)}` : ''} genis kirli={metin !== null}
      hedef={undefined}
      eylemler={v && !v.korumali && v.v !== null ? <button className="m16-btn tehlike" onClick={sil}>Sil</button> : undefined}
    >
      {d.hata ? <Hata hata={d.hata} yenile={d.yenile} /> : !v ? <Yukleniyor /> : v.v === null ? <BosDurum baslik="Silinmiş anahtar" /> : v.jsonMu ? (
        <JsonDuzenleyici deger={v.json} kaydet={(yeni) => kaydet({ json: yeni })} />
      ) : (
        <>
          <textarea className="m16-girdi" rows={10} style={{ width: '100%', fontFamily: 'var(--font-mono, monospace)' }} value={metin ?? v.v} onChange={(e) => setMetin(e.target.value)} aria-label="Değer" />
          <div style={{ display: 'flex', gap: 6, marginTop: 8 }}>
            <button className="m16-btn birincil" disabled={metin === null} onClick={() => kaydet({ deger: metin })}>Kaydet</button>
            {metin !== null && <button className="m16-btn hayalet" onClick={() => setMetin(null)}>Vazgeç</button>}
          </div>
        </>
      )}
      {v?.jsonMu === false ? null : v && <details style={{ marginTop: 8 }}><summary>Ham metin</summary><JsonGoruntuleyici veri={v.v} /></details>}
    </AyrintiCekmecesi>
  );
}
