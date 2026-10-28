import React, { useState } from 'react';
import { SayfaBasligi, VeriTablosu, useAdminSorgu, adminIstek, AyrintiCekmecesi, Rozet, Hata, Yukleniyor, JsonGoruntuleyici, onayIste, bildir, zamanMetni, BosDurum } from '../kit';
import type { SayfaProps } from '../menu';
import { KisiBag, tarihMetni } from './kisiOrtak';

type BSatir = { uid: string; ad: string; email: string; donem: number | null; kurul: number | null; birlesti: string | null; puan: number; hafta: number; kurulPuan: number; atp: number; kuyruk: number; kilit: number; basarim: number; sonGiris: string; ozel: any; kidem: string; tavan: number | null };

const SEKME = [['kisiler', 'Kişiler'], ['defter', 'Yönetim defteri'], ['tanim', 'Tanım']] as const;

/** Kullanıcılar › Puan ve ATP: kişi bazında puan/ATP/kilit/unvan düzeltmesi, yönetim defteri, tanım (tanim.json) görünümü. */
export default function KisiBasarim({ altYol, git }: SayfaProps) {
  const sekme = altYol[0] || 'kisiler';
  const d = useAdminSorgu<{ kisiler: BSatir[]; tanim: any }>('/api/admin/basarim/kisiler', { canliOlay: ['basarim_changed'] });
  const [acik, setAcik] = useState<string | null>(null);
  return (
    <>
      <SayfaBasligi baslik="Puan ve ATP" aciklama="Her işlem gerekçeli; kişinin defterine ve yönetim günlüğüne yazılır.">
        <nav className="m16-sekmeler">{SEKME.map(([id, ad]) => <button key={id} className={sekme === id ? 'on' : ''} onClick={() => git(`kisi/basarim${id === 'kisiler' ? '' : `/${id}`}`, { degistir: true })}>{ad}</button>)}</nav>
      </SayfaBasligi>
      {d.hata && !d.veri ? <Hata hata={d.hata} yenile={d.yenile} /> : !d.veri ? <Yukleniyor satir={8} /> : sekme === 'tanim' ? (
        <section className="m16-kart"><h2>tanim.json</h2><p style={{ color: 'var(--color-ink-3)', fontSize: 12.5 }}>Salt görünüm. Düzenleme: <code>PUT /api/admin/basarim/tanim</code> doğrulayıcıdan geçer.</p><JsonGoruntuleyici veri={d.veri.tanim} enYuksek={9999} /></section>
      ) : sekme === 'defter' ? <Defter /> : (
        <>
          <VeriTablosu<BSatir>
            kimlik="kisi-basarim" ogeler={d.veri.kisiler} satirKimligi={(x) => x.uid} aramaYeri="Ad, e-posta, uid…"
            satirTikla={(x) => setAcik(x.uid)} etkin={acik}
            sutunlar={[
              { anahtar: 'ad', baslik: 'Kişi', genislik: 'minmax(180px,2fr)', sirala: true, deger: (x) => `${x.ad} ${x.email} ${x.uid}`, hucre: (x) => <span className="m16-kisalt"><strong>{x.ad || x.uid}</strong> <small style={{ color: 'var(--color-ink-3)' }}>{x.email}</small>{x.birlesti && <Rozet ton="uyari">bağlı</Rozet>}{x.ozel && <Rozet ton="vurgu">{x.ozel.unvan}</Rozet>}</span> },
              { anahtar: 'kurul', baslik: 'D/K', genislik: '60px', deger: (x) => x.kurul ?? -1, hucre: (x) => (x.donem ? `${x.donem}/${x.kurul ?? '—'}` : '—') },
              { anahtar: 'puan', baslik: 'Puan', genislik: '80px', hizala: 'sag', sirala: true, deger: (x) => x.puan },
              { anahtar: 'hafta', baslik: 'Hafta', genislik: '70px', hizala: 'sag', sirala: true, deger: (x) => x.hafta },
              { anahtar: 'kurulPuan', baslik: 'Kurul', genislik: '70px', hizala: 'sag', sirala: true, deger: (x) => x.kurulPuan, gizli: true },
              { anahtar: 'atp', baslik: 'ATP', genislik: '80px', hizala: 'sag', sirala: true, deger: (x) => x.atp, hucre: (x) => `${x.atp}${x.kuyruk ? ` (+${x.kuyruk})` : ''}` },
              { anahtar: 'basarim', baslik: 'Başarım', genislik: '70px', hizala: 'sag', sirala: true, deger: (x) => x.basarim },
              { anahtar: 'kidem', baslik: 'Kıdem', genislik: '90px', deger: (x) => x.kidem, gizli: true },
              { anahtar: 'sonGiris', baslik: 'Son giriş', genislik: '110px', sirala: true, deger: (x) => x.sonGiris, hucre: (x) => (x.sonGiris ? zamanMetni(x.sonGiris) : '—') },
            ]}
          />
          {acik && <KisiCekmece uid={acik} tanim={d.veri.tanim} kapat={() => setAcik(null)} git={git} degisti={d.yenile} />}
        </>
      )}
    </>
  );
}

function Defter() {
  const d = useAdminSorgu<{ gunluk: any[] }>('/api/admin/basarim/gunluk', { sorgu: { limit: 1000 }, canliOlay: ['basarim_changed'] });
  if (d.hata && !d.veri) return <Hata hata={d.hata} yenile={d.yenile} />;
  if (!d.veri) return <Yukleniyor satir={8} />;
  return (
    <VeriTablosu<any>
      kimlik="kisi-basarim-defter" ogeler={d.veri.gunluk} satirKimligi={(x) => `${x.at}-${x.uid}-${x.tur}`} aramaYeri="Gerekçe, kişi, işlem…"
      sutunlar={[
        { anahtar: 'at', baslik: 'Zaman', genislik: '120px', sirala: true, deger: (x) => x.at, hucre: (x) => <time title={tarihMetni(x.at)}>{zamanMetni(x.at)}</time> },
        { anahtar: 'tur', baslik: 'İşlem', genislik: '100px', deger: (x) => x.tur, hucre: (x) => <Rozet>{x.tur}</Rozet> },
        { anahtar: 'uid', baslik: 'Kişi', genislik: 'minmax(120px,1fr)', deger: (x) => `${x.ad || ''} ${x.uid}`, hucre: (x) => x.ad || x.uid },
        { anahtar: 'gerekce', baslik: 'Gerekçe', genislik: 'minmax(200px,2fr)', deger: (x) => x.gerekce || '' },
        { anahtar: 'by', baslik: 'Yapan', genislik: 'minmax(120px,1fr)', deger: (x) => x.by || '' },
      ]}
      bosMetin="Yönetim işlemi yok."
    />
  );
}

// H372: tehlike regex'le (/sil|geri|al$/) seçiliyordu, ozel_kaldir kaçıyordu; açık liste
const TEHLIKELI = new Set(['kuyruk_sil', 'odul_geri', 'kilit_al', 'ozel_kaldir']);

function KisiCekmece({ uid, tanim, kapat, git, degisti }: { uid: string; tanim: any; kapat: () => void; git: SayfaProps['git']; degisti: () => void }) {
  const d = useAdminSorgu<any>(`/api/admin/basarim/kisi/${encodeURIComponent(uid)}`);
  const [tur, setTur] = useState('puan');
  const [miktar, setMiktar] = useState('');
  const [kilitId, setKilitId] = useState('');
  const [unvan, setUnvan] = useState('');
  const [gerekce, setGerekce] = useState('');
  const islem = async (t: string, veri: any, baslik: string) => {
    if (gerekce.trim().length < 3) return bildir('Önce gerekçe yazın.', 'kotu');
    if (!(await onayIste({ baslik, onayMetni: 'Uygula', tehlikeli: TEHLIKELI.has(t) }))) return;
    try {
      const r = await adminIstek(`/api/admin/basarim/kisi/${encodeURIComponent(uid)}/islem`, { yontem: 'POST', govde: { tur: t, veri, gerekce: gerekce.trim() } });
      d.setVeri(r); degisti(); bildir('Uygulandı.');
    } catch (e: any) { bildir(e.message, 'kotu'); }
  };
  const k = d.veri?.kisi;
  const kilitler: any[] = tanim?.kilitler || [];
  return (
    <AyrintiCekmecesi acik kapat={kapat} genis baslik={k?.ad || uid} altBaslik={<KisiBag anahtar={`u:${uid}`} git={git}>360° görünüm</KisiBag>} kayit={d.veri?.ozet}
      ekSekmeler={k ? [{ id: 'defter', etiket: 'Defter', icerik: (
        <ul className="m16-liste">{(k.defter || []).map((x: any) => (
          <li key={x.id}>
            <Rozet ton={x.t === 'yonetici' ? 'vurgu' : 'notr'}>{x.t}</Rozet>
            <span className="m16-kisalt" title={x.ad}>{x.ad}{x.geriAlindi ? ' (geri alındı)' : ''}</span>
            <span>{x.p ? `${x.p}p ` : ''}{x.a ? `${x.a} mol` : ''}</span>
            {!x.geriAlindi && x.t !== 'harcama' && x.t !== 'yonetici' && <button className="m16-btn hayalet" onClick={() => islem('odul_geri', { id: x.id }, `“${x.ad}” geri alınsın mı?`)}>Geri al</button>}
          </li>
        ))}</ul>
      ) }] : undefined}
    >
      {d.hata ? <Hata hata={d.hata} yenile={d.yenile} /> : !k ? <Yukleniyor /> : (
        <div style={{ display: 'grid', gap: 12 }}>
          <dl className="m16-satirlar">
            <dt>ATP</dt><dd>{k.atp.bakiye} mol {k.atp.kuyruk.length ? `(kuyruk ${k.atp.kuyruk.reduce((a: number, q: any) => a + q.a, 0)})` : ''}</dd>
            <dt>Puan</dt><dd>{d.veri.ozet?.puan?.toplam ?? '—'}</dd>
            <dt>Dönem / kurul</dt><dd>{k.donem || '—'} / {k.kurul || '—'}</dd>
            <dt>Gizli unvan</dt><dd>{k.ozel ? `${k.ozel.unvan}${k.ozel.muaf ? ' (muaf)' : ''}` : '—'}</dd>
            <dt>Açık kilit</dt><dd>{Object.keys(k.kilit || {}).join(', ') || '—'}</dd>
          </dl>
          <label className="m16-alan">Gerekçe (her işlem için zorunlu)<input className="m16-girdi" value={gerekce} onChange={(e) => setGerekce(e.target.value)} /></label>
          <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
            <select className="m16-girdi" value={tur} onChange={(e) => setTur(e.target.value)} aria-label="Tür"><option value="puan">Puan</option><option value="atp">ATP</option></select>
            <input className="m16-girdi" type="number" placeholder="miktar (±)" value={miktar} onChange={(e) => setMiktar(e.target.value)} aria-label="Miktar" style={{ width: 130 }} />
            <button className="m16-btn birincil" disabled={!Number(miktar)} onClick={() => islem(tur, { miktar: Number(miktar) }, `${tur === 'puan' ? 'Puan' : 'ATP'} ${miktar} uygulansın mı?`)}>Uygula</button>
            {k.atp.kuyruk.length > 0 && <>
              <button className="m16-btn" onClick={() => islem('kuyruk_aktar', {}, 'Kuyruk hemen hesaba geçsin mi?')}>Kuyruğu aktar</button>
              <button className="m16-btn tehlike" onClick={() => islem('kuyruk_sil', {}, 'Kuyruk silinsin mi?')}>Kuyruğu sil</button>
            </>}
          </div>
          <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
            <select className="m16-girdi" value={kilitId} onChange={(e) => setKilitId(e.target.value)} aria-label="Kilit"><option value="">Kilit seç…</option>{kilitler.map((x) => <option key={x.id} value={x.id}>{x.ad} ({x.tur}{k.kilit?.[x.id] ? ', açık' : ''})</option>)}</select>
            <button className="m16-btn" disabled={!kilitId || !!k.kilit?.[kilitId]} onClick={() => islem('kilit_ver', { id: kilitId }, 'Kilit açılsın mı?')}>Kilidi aç</button>
            <button className="m16-btn tehlike" disabled={!kilitId || !k.kilit?.[kilitId]} onClick={() => islem('kilit_al', { id: kilitId, iade: true }, 'Kilit geri alınsın ve ATP iade edilsin mi?')}>Geri al + iade</button>
          </div>
          <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
            <input className="m16-girdi" placeholder="gizli unvan" value={unvan} onChange={(e) => setUnvan(e.target.value)} aria-label="Gizli unvan" />
            <button className="m16-btn" disabled={!unvan.trim()} onClick={() => islem('ozel', { unvan: unvan.trim(), muaf: true }, `“${unvan}” gizli unvanı (sınırlardan muaf) verilsin mi?`)}>Unvan ver</button>
            {k.ozel && <button className="m16-btn tehlike" onClick={() => islem('ozel_kaldir', {}, 'Gizli unvan kaldırılsın mı?')}>Unvanı kaldır</button>}
          </div>
          {!d.veri.gunluk?.length ? <BosDurum baslik="Yönetim işlemi yok" /> : (
            <ul className="m16-liste">{d.veri.gunluk.slice(0, 20).map((g: any, i: number) => <li key={i}><Rozet>{g.tur}</Rozet><span className="m16-kisalt">{g.gerekce}</span><time>{zamanMetni(g.at)}</time></li>)}</ul>
          )}
        </div>
      )}
    </AyrintiCekmecesi>
  );
}
