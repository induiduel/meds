import React from 'react';
import { VeriTablosu, SayfaBasligi, Rozet, AyrintiCekmecesi, Yukleniyor, Hata, adminIstek, useAdminSorgu, onayIste, bildir, yazimHedefi, zamanMetni } from '../kit';
import { manageAdres, type SayfaProps } from '../menu';

/** Sorular › Birleşenler — kopya çıkmış soru grupları: asıl seç, onayla, ayır, geri al, seçili kopyayı tüm kardeşlere yaz. */
type Satir = { id: string; asil: string; uye: number; durum: string; birebir: boolean; benzerlik: number; olusturma: string; kok: string; ders: string; kurul: string };
const DURUM: Record<string, string> = { otomatik: 'Otomatik', onayli: 'Onaylı', ayrildi: 'Ayrıldı' };

function Ayrinti({ id, kapat, git }: { id: string; kapat: () => void; git: SayfaProps['git'] }) {
  const { veri, hata, yukleniyor, yenile } = useAdminSorgu<any>(`/api/admin/sorular/birlesen/${encodeURIComponent(id)}`);
  // H177: 'Ayır' tüm kopyaları sitede ayrı gösterir → tehlikeli + yazılı onay (AYIR) + Geri al (restore); yazılacak sözcük işleme göre
  const islem = async (govde: Record<string, unknown>, baslik: string, tehlikeli = false, yazilacak = 'YAZ', aciklama?: string, geriAl?: Record<string, unknown>) => {
    if (!(await onayIste({ baslik, tehlikeli, aciklama, ...(tehlikeli ? { yazilacak } : {}) }))) return;
    try {
      await adminIstek(`/api/admin/question-merges/${encodeURIComponent(id)}`, { yontem: 'POST', govde });
      bildir('Uygulandı', 'iyi', geriAl ? { etiket: 'Geri al', yap: async () => { await adminIstek(`/api/admin/question-merges/${encodeURIComponent(id)}`, { yontem: 'POST', govde: geriAl }); void yenile(); } } : undefined);
      void yenile();
    }
    catch (e: any) { bildir(e.message, 'kotu'); }
  };
  const g = veri?.grup;
  return (
    <AyrintiCekmecesi acik genis kapat={kapat} baslik={`Grup ${id}`} altBaslik={g ? `${g.uyeler.length} kopya · ${DURUM[g.durum] || g.durum}${g.gorunen ? ` · sitede ${g.gorunen}` : ''}` : ''} kayit={veri} hedef={`grup:${id}`}
      eylemler={g && (<>
        {g.durum !== 'onayli' && g.durum !== 'ayrildi' && <button type="button" className="m16-btn birincil" onClick={() => islem({ action: 'confirm' }, 'Birleştirme onaylansın mı?')}>Onayla</button>}
        {g.durum !== 'ayrildi' ? <button type="button" className="m16-btn" onClick={() => islem({ action: 'split' }, 'Grup ayrılsın mı?', true, 'AYIR', `${g.uyeler.length} kopyanın tümü sitede ayrı soru olarak görünür. Hedef: ${yazimHedefi()}.`, { action: 'restore' })}>Ayır</button>
          : <button type="button" className="m16-btn" onClick={() => islem({ action: 'restore' }, 'Birleştirme geri yüklensin mi?')}>Geri yükle</button>}
      </>)}>
      {hata ? <Hata hata={hata} yenile={yenile} /> : yukleniyor && !veri ? <Yukleniyor satir={8} /> : veri && (
        <>
          {g.ayrisik && <div className="m16-kart"><Rozet ton="uyari">Ayrışık</Rozet> Gizli bir kopya, sitede görünenden sonra düzeltilmiş; düzeltme sitede görünmüyor. O kopyada “Tüm kopyalara yaz”ı kullanın.</div>}
          {veri.sorular.map((s: any) => (
            <div key={s.id} className="m16-kart">
              {/* H266: kimlik Çıkmış ayrıntısına bağlantı */}<h2><a href={manageAdres(`sorular/cikmis/${encodeURIComponent(s.id)}`)} onClick={(e) => { e.preventDefault(); git(`sorular/cikmis/${encodeURIComponent(s.id)}`); }}>{s.id}</a> {s.id === g.asil && <Rozet ton="vurgu">Asıl</Rozet>} {s.id === g.gorunen && <Rozet ton="iyi">Sitede</Rozet>} {s.ayrisik && <Rozet ton="uyari">Ayrışık</Rozet>} {!s.var && <Rozet ton="kotu">Kayıt yok</Rozet>}</h2>
              <p>{s.stem || '—'}</p>
              <ol className="m16-liste" type="A">{s.options.map((o: string, i: number) => <li key={i}>{o}</li>)}</ol>
              <p>Cevap: <b>{s.correctAnswer || '—'}</b> · {s.discipline} · {s.year} {s.duzenleme && <small>· son düzeltme {zamanMetni(s.duzenleme.at)} ({s.duzenleme.kind})</small>}</p>
              <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
                {s.id !== g.asil && g.durum !== 'ayrildi' && <button type="button" className="m16-btn" onClick={() => islem({ action: 'primary', asil: s.id }, `${s.id} asıl yapılsın mı?`)}>Asıl yap</button>}
                <button type="button" className="m16-btn" onClick={() => islem({ action: 'sync', kaynak: s.id }, `${s.id} içeriği gruptaki tüm kopyalara yazılsın mı? Önceki hâller revizyon olarak saklanır.`, true)}>Tüm kopyalara yaz</button>
              </div>
            </div>
          ))}
        </>
      )}
    </AyrintiCekmecesi>
  );
}

export default function Birlesenler({ id, git }: SayfaProps) {
  return (
    <>
      <SayfaBasligi baslik="Birleşen sorular" aciklama="Aynı çıkmış sorunun farklı dökümlerden gelen kopyaları. Sitede gruptan yalnız biri görünür." />
      <VeriTablosu<Satir>
        kimlik="sorular-birlesen" kaynak="/api/admin/sorular/birlesen" canliOlay={['past_questions_changed']}
        aramaYeri="Grup, soru kimliği ya da kök ara…" satirKimligi={(s) => s.id} etkin={id || null}
        satirTikla={(s) => git(`sorular/birlesen/${encodeURIComponent(s.id)}${window.location.search}`)}
        suzgecler={[
          { anahtar: 'durum', etiket: 'Durum', secenekler: Object.entries(DURUM).map(([deger, etiket]) => ({ deger, etiket })) },
          { anahtar: 'birebir', etiket: 'İçerik', secenekler: [{ deger: 'evet', etiket: 'Birebir aynı' }, { deger: 'hayir', etiket: 'Farklı' }] },
          { anahtar: 'kurul', etiket: 'Kurul', secenekler: ['1', '2', '3', '4', '5', '6', 'final'].map((k) => ({ deger: k, etiket: /\d/.test(k) ? `Kurul ${k}` : 'Final' })) },
        ]}
        sutunlar={[
          { anahtar: 'kok', baslik: 'Asıl soru', genislik: 'minmax(240px,3fr)', hucre: (s) => <span title={s.kok}>{s.kok || s.asil}</span> },
          { anahtar: 'ders', baslik: 'Ders', genislik: 'minmax(100px,1fr)' },
          { anahtar: 'uye', baslik: 'Kopya', sirala: true, genislik: '64px', hizala: 'sag' },
          { anahtar: 'benzerlik', baslik: 'Benzerlik', sirala: true, genislik: '84px', hizala: 'sag', hucre: (s) => (s.benzerlik != null ? `%${Math.round(Number(s.benzerlik) * (Number(s.benzerlik) <= 1 ? 100 : 1))}` : '—') },
          { anahtar: 'durum', baslik: 'Durum', genislik: '120px', hucre: (s) => <>{!s.birebir && <Rozet ton="uyari">Farklı</Rozet>} <Rozet ton={s.durum === 'onayli' ? 'iyi' : s.durum === 'ayrildi' ? 'notr' : 'bilgi'}>{DURUM[s.durum] || s.durum}</Rozet></> },
          { anahtar: 'olusturma', baslik: 'Oluşturma', sirala: true, genislik: '104px', hucre: (s) => (s.olusturma ? zamanMetni(s.olusturma) : '—') },
        ]}
      />
      {id && <Ayrinti id={id} git={git} kapat={() => git(`sorular/birlesen${window.location.search}`)} />}
    </>
  );
}
