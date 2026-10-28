import React, { useMemo, useState } from 'react';
import { adminIstek, useAdminSorgu } from './api';
import { SayfaBasligi } from './SayfaBasligi';
import { VeriTablosu, type Sutun } from './VeriTablosu';
import { AyrintiCekmecesi } from './AyrintiCekmecesi';
import { Form, type AlanTanim } from './Form';
import { Hata, Yukleniyor } from './Durumlar';
import { Rozet } from './Rozet';
import { GorunurlukBaglantisi } from './Gorunurluk'; // H321: satır içi seçici kaldırıldı
import { onayIste } from './Onay';
import { bildir } from './Bildirim';

export type KatalogSatiri = { id: string; baslik: string; alt: string; degerlendirme?: string; gorunurluk?: string };
type Meta = { etiket: string; kaynak: string; toplam: number; suzgecler: { anahtar: string; etiket: string }[]; yuzler: Record<string, { deger: string; n: number }[]>; duzenlenebilir: string[] };
type Ayrinti = { id: string; baslik: string; kayit: Record<string, any>; duzenlenebilir: string[]; gorunurlukAnahtari?: string; gorunurluk?: string };

// H268: form alanları ham alan adı yerine Türkçe etiketle gösterilir (bilinmeyen ad olduğu gibi kalır)
const ALAN_ETIKET: Record<string, string> = {
  term: 'Terim', title: 'Başlık', definition: 'Tanım', description: 'Açıklama', explanation: 'Açıklama', stem: 'Soru kökü', spot: 'Spot', clinicalPearl: 'Klinik inci',
  note: 'Not', front: 'Ön yüz', back: 'Arka yüz', tags: 'Etiketler', aliases: 'Eş anlamlılar', category: 'Kategori', committee: 'Kurul', discipline: 'Branş',
  options: 'Şıklar', correctAnswer: 'Doğru cevap', name: 'Ad', metin: 'Metin', aciklama: 'Açıklama', baslik: 'Başlık', ders: 'Ders', kurul: 'Kurul',
};
const alanEtiketi = (a: string) => ALAN_ETIKET[a] || a;
const UZUN = /definition|description|explanation|stem|spot|clinicalPearl|note|back|front|metin|aciklama/i;
const DIZI = /^(tags|aliases)$/;

/**
 * Veri kataloğu varlığı için hazır liste + ayrıntı sayfası (uç: /api/admin/k16/katalog/:varlik).
 * Süzgeç çipleri sunucunun yüzlerinden gelir; düzenlenebilir alanlar formda, kaydetme denetime düşer.
 * silinebilir: katalog silme (çöp kutusuna taşır, geri yüklenebilir). topluEylemler verilirse onu kullanır.
 */
export function KatalogSayfasi(p: {
  varlik: string;
  kimlik: string;
  baslik: string;
  aciklama?: React.ReactNode;
  silinebilir?: boolean;
  /** Ek sekme/üst alan (ör. sekmeler) */
  ust?: React.ReactNode;
  topluEylemler?: (secili: string[], temizle: () => void) => React.ReactNode;
  ekSekme?: (a: Ayrinti) => { id: string; etiket: string; icerik: React.ReactNode } | null;
}) {
  const meta = useAdminSorgu<Meta>(`/api/admin/k16/katalog/${p.varlik}/meta`);
  const [acikId, setAcikId] = useState<string | null>(() => new URLSearchParams(location.search).get('ac'));
  const [kirli, setKirli] = useState(false);
  const [yenileNo, setYenileNo] = useState(0);
  const ayr = useAdminSorgu<Ayrinti>(acikId ? `/api/admin/k16/katalog/${p.varlik}/${encodeURIComponent(acikId)}` : null);

  const gorunurlukVar = p.varlik === 'decks';
  const suzgecler = useMemo(() => {
    const s = (meta.veri?.suzgecler || []).map((f) => ({ anahtar: f.anahtar, etiket: f.etiket, secenekler: (meta.veri?.yuzler[f.anahtar] || []).slice(0, 12).map((y) => ({ deger: y.deger, etiket: y.deger })) }))
      // H184: tek seçenekli süzgeç gizleniyordu → çöp kutusunda tek tür varken "Tür" hiç görünmüyordu. Çöpte tür/silinme her zaman görünür
      .filter((f) => f.secenekler.length > (p.varlik === 'trash' ? 0 : 1));
    if (p.varlik === 'trash') {
      const SIRA = ['Bugün', 'Son 7 gün', 'Son 30 gün', 'Daha eski'];
      for (const f of s) if (f.anahtar === 'silinme') f.secenekler.sort((x, y) => SIRA.indexOf(x.deger) - SIRA.indexOf(y.deger));
    }
    if (gorunurlukVar) s.push({ anahtar: 'gorunurluk', etiket: 'Görünürlük', secenekler: [{ deger: 'gizli', etiket: 'Gizli' }, { deger: 'yalniz-yonetici', etiket: 'Yalnız yönetici' }] });
    return s;
  }, [meta.veri, gorunurlukVar, p.varlik]);

  const sutunlar: Sutun<KatalogSatiri>[] = [
    { anahtar: 'baslik', baslik: 'Kayıt', sirala: true, genislik: 'minmax(220px,3fr)', hucre: (x) => <span className="m16-kisalt" title={x.baslik}>{x.baslik}</span> },
    { anahtar: 'alt', baslik: 'Ayrıntı', genislik: 'minmax(160px,2fr)', hucre: (x) => <span className="m16-kisalt" title={x.alt}>{x.alt}</span> },
    { anahtar: 'id', baslik: 'Kimlik', genislik: 'minmax(100px,1fr)', gizli: true, hucre: (x) => <code>{x.id}</code> },
    ...(gorunurlukVar ? [{ anahtar: 'gorunurluk', baslik: 'Görünürlük', genislik: '150px', hucre: (x: KatalogSatiri) => <GorunurlukBaglantisi anahtar={`deste:${x.id}`} deger={x.gorunurluk} /> } /* H321 */] : []),
    { anahtar: 'degerlendirme', baslik: 'Değerlendirme', genislik: '110px', gizli: true, hucre: (x) => x.degerlendirme ? <Rozet ton={x.degerlendirme === 'onayli' ? 'iyi' : x.degerlendirme === 'sorunlu' ? 'kotu' : 'uyari'}>{x.degerlendirme}</Rozet> : null },
  ];

  const alanlar: AlanTanim[] = (ayr.veri?.duzenlenebilir || []).map((a) => ({
    ad: a, etiket: alanEtiketi(a), tur: DIZI.test(a) ? 'etiketler' : UZUN.test(a) ? 'uzun' : 'metin',
  }));
  const deger = useMemo(() => Object.fromEntries((ayr.veri?.duzenlenebilir || []).map((a) => [a, ayr.veri?.kayit?.[a] ?? (DIZI.test(a) ? [] : '')])), [ayr.veri]);

  const sil = async (ids: string[], temizle: () => void) => {
    if (!(await onayIste({ baslik: `${ids.length} kayıt çöp kutusuna taşınsın mı?`, aciklama: 'Çöp kutusundan geri yüklenebilir.', onayMetni: 'Taşı', tehlikeli: true }))) return;
    try {
      const r = await adminIstek<{ deleted: number }>(`/api/admin/catalog/${p.varlik}/delete`, { yontem: 'POST', govde: { ids } });
      bildir(`${r.deleted} kayıt çöp kutusuna taşındı`);
      temizle();
      setYenileNo((n) => n + 1);
    } catch (e: any) { bildir(e?.message || 'Silinemedi', 'kotu'); }
  };

  const ac = (id: string | null) => {
    setAcikId(id);
    const u = new URL(location.href);
    if (id) u.searchParams.set('ac', id); else u.searchParams.delete('ac');
    history.replaceState(history.state, '', u);
  };

  const a = ayr.veri;
  const ek = a && p.ekSekme ? p.ekSekme(a) : null;
  return (
    <>
      <SayfaBasligi baslik={p.baslik} aciklama={p.aciklama ?? (meta.veri ? <>{meta.veri.toplam.toLocaleString('tr-TR')} kayıt{/* H172: dosya yolu ikincil */}<span className="m16-kaynak" title="Kaynak dosya"><code>{meta.veri.kaynak}</code></span></> : undefined)}>{p.ust}</SayfaBasligi>
      {meta.hata ? <Hata hata={meta.hata} yenile={meta.yenile} /> : (
        <VeriTablosu<KatalogSatiri>
          key={yenileNo}
          kimlik={p.kimlik}
          kaynak={`/api/admin/k16/katalog/${p.varlik}`}
          canliOlay={['content_changed', 'site_ayar_changed']}
          aramaYeri="Ara…"
          satirKimligi={(x) => x.id}
          etkin={acikId}
          satirTikla={(x) => ac(x.id)}
          suzgecler={suzgecler}
          sutunlar={sutunlar}
          secim={!!(p.silinebilir || p.topluEylemler)}
          topluEylemler={p.topluEylemler || (p.silinebilir ? (ids, t) => <button type="button" className="m16-btn tehlike" onClick={() => void sil(ids, t)}>Çöp kutusuna taşı</button> : undefined)}
        />
      )}
      <AyrintiCekmecesi acik={!!acikId} kapat={() => ac(null)} baslik={a?.baslik || acikId || ''} altBaslik={a ? <code>{a.id}</code> : undefined}
        kayit={a?.kayit} hedef={acikId ? `${p.varlik}:${acikId}` : undefined} kirli={kirli} ekSekmeler={ek ? [ek] : undefined}>
        {ayr.hata ? <Hata hata={ayr.hata} yenile={ayr.yenile} /> : !a ? <Yukleniyor satir={4} /> : (
          <>
            {a.gorunurlukAnahtari && (
              <div className="m16-kart"><h2>Görünürlük</h2><GorunurlukBaglantisi anahtar={a.gorunurlukAnahtari} deger={a.gorunurluk} /></div>
            )}
            {alanlar.length ? (
              <Form alanlar={alanlar} deger={deger} kirliDegisti={setKirli} kaydet={async (_y, degisen) => {
                await adminIstek(`/api/admin/k16/katalog/${p.varlik}/${encodeURIComponent(a.id)}`, { yontem: 'PUT', govde: { yama: degisen } });
                bildir('Kaydedildi');
                await ayr.yenile();
              }} />
            ) : <p className="m16-alan-ipucu">Bu veri türü salt okunur; kayıt JSON sekmesinde.</p>}
          </>
        )}
      </AyrintiCekmecesi>
    </>
  );
}
