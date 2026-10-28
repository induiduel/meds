import React, { useState } from 'react';
import { SayfaBasligi, VeriTablosu, AyrintiCekmecesi, Hata, Yukleniyor, GorunurlukRozeti, GorunurlukSecici, JsonGoruntuleyici, useAdminSorgu } from '../kit';
import { manageAdres, type SayfaProps } from '../menu';

type Satir = { key: string; baslik: string; kurul: string; sayilar: Record<string, number>; gorunurluk: string };

/** Öğrenme › İçerik paketleri: src/data/ders_icerik (terim, kısaltma, spot, tablo, kart, quiz, çıkmış). Salt okunur + görünürlük paket:<key>. */
export default function IcerikPaketleri({ git }: SayfaProps) {
  const [acik, setAcik] = useState<string | null>(() => new URLSearchParams(location.search).get('ac'));
  const a = useAdminSorgu<any>(acik ? `/api/admin/ders-icerik/${encodeURIComponent(acik)}` : null);
  const dersId = acik?.match(/^k\d-\d+/)?.[0];
  return (
    <>
      <SayfaBasligi baslik="İçerik paketleri" aciklama={<>Ders sayfalarındaki içerik paketleri (terimler, kartlar, tablolar…). Burada sayılar, örnek ögeler ve görünürlük yönetilir.{/* H172 */}<span className="m16-kaynak"><code>ders_icerik</code></span></>} />
      <VeriTablosu<Satir>
        kimlik="ogrenme-paket" kaynak="/api/admin/ders-icerik" canliOlay={['site_ayar_changed']} satirKimligi={(x) => x.key} etkin={acik} satirTikla={(x) => setAcik(x.key)}
        suzgecler={[{ anahtar: 'kurul', etiket: 'Kurul', secenekler: [1, 2, 3, 4, 5, 6].map((k) => ({ deger: String(k), etiket: String(k) })) }]}
        sutunlar={[
          { anahtar: 'key', baslik: 'Anahtar', sirala: true, genislik: 'minmax(200px,2fr)', hucre: (x) => <code className="m16-kisalt">{x.key}</code> },
          { anahtar: 'baslik', baslik: 'Başlık', genislik: 'minmax(160px,2fr)' },
          { anahtar: 'terimler', baslik: 'Terim', sirala: true, genislik: '64px', hizala: 'sag', hucre: (x) => x.sayilar.terimler ?? 0 },
          { anahtar: 'quiz', baslik: 'Quiz', sirala: true, genislik: '64px', hizala: 'sag', hucre: (x) => x.sayilar.quiz ?? 0 },
          { anahtar: 'kartlar', baslik: 'Kart', genislik: '64px', hizala: 'sag', hucre: (x) => x.sayilar.kartlar ?? 0 },
          { anahtar: 'cikmis', baslik: 'Çıkmış', genislik: '64px', hizala: 'sag', hucre: (x) => x.sayilar.cikmis ?? 0 },
          { anahtar: 'gorunurluk', baslik: 'Görünürlük', genislik: '110px', hucre: (x) => <GorunurlukRozeti deger={x.gorunurluk} /> },
        ]}
      />
      <AyrintiCekmecesi acik={!!acik} kapat={() => setAcik(null)} baslik={a.veri?.baslik || acik || ''} altBaslik={<code>{acik}</code>} kayit={a.veri?.ornek} hedef={acik ? `paket:${acik}` : undefined} genis>
        {a.hata ? <Hata hata={a.hata} yenile={a.yenile} /> : !a.veri ? <Yukleniyor satir={4} /> : (
          <>
            <div className="m16-kart"><h2>Görünürlük</h2><GorunurlukSecici anahtar={`paket:${a.veri.key}`} deger={a.veri.gorunurluk} degisti={() => void a.yenile()} /></div>
            {dersId && <p>Ders: <a href={manageAdres(`icerik/dersler/${dersId}`)} onClick={(e) => { e.preventDefault(); git(`icerik/dersler/${dersId}`); }}>{dersId}</a></p>}
            <p>{a.veri.ozet}</p>
            <div className="m16-kart"><h2>Bölümler</h2><dl className="m16-satirlar">{Object.entries(a.veri.sayilar as Record<string, number>).map(([k, n]) => <React.Fragment key={k}><dt>{k}</dt><dd>{n}</dd></React.Fragment>)}</dl></div>
            <div className="m16-kart"><h2>Quiz (ilk 5)</h2><JsonGoruntuleyici veri={a.veri.ornek?.quiz} /></div>
          </>
        )}
      </AyrintiCekmecesi>
    </>
  );
}
