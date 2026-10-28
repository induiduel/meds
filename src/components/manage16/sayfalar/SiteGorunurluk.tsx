import React, { useMemo, useState } from 'react';
import { Filter } from 'lucide-react';
import { RotateCcw } from 'lucide-react';
import { SayfaBasligi, VeriTablosu, Rozet, Hata, Yukleniyor, onayIste, bildir, yazimHedefi, GorunurlukRozeti, GORUNURLUK_ETIKET, type GorunurlukDegeri, type Ton } from '../kit';
import type { SayfaProps } from '../menu';
import { NAV_ITEMS } from '../../shell/navModel';
import { ogrenciGorunumu } from '../../../services/siteAyar';
import { GIZLI_SAYFALAR, KAPALI_SAYFALAR } from '../../merkez/sayfaSabitleri';
import { pathFor, type AppRoute } from '../../../router';
import { Anahtar, siteAyarYaz, useSiteAyarAdmin, type SayfaDurumu } from './ortak/siteAyarOrtak';

/**
 * Site › Görünürlük: her öğrenci sayfası için çalışma anı durumu (site_ayar.sayfalar) ve menüde görünme (site_ayar.menu).
 * Menü yapısı/sırası kodda kalır (kural 16, siteHaritasi.ts); panel yalnız gizler/açar. Öğrenci tarafı services/siteAyar.ts.
 */
const DURUM: { d: SayfaDurumu | 'varsayilan'; etiket: string; ipucu: string }[] = [
  { d: 'varsayilan', etiket: 'Varsayılan', ipucu: 'Kod sabiti (GIZLI_SAYFALAR/KAPALI_SAYFALAR) geçerli' },
  { d: 'acik', etiket: 'Herkese açık', ipucu: 'Menüde ve adresle açılır' },
  { d: 'gizli', etiket: 'Gizli', ipucu: 'Menüden kalkar; adresle girilince Bugün açılır (yöneticiye de menüde görünmez)' },
  { d: 'kapali', etiket: 'Kapalı', ipucu: 'Öğrenci "Bu sayfa kullanımdan kaldırıldı" ekranını görür' },
  { d: 'yalniz-yonetici', etiket: 'Yalnız yönetici', ipucu: 'Öğrenci menüde görmez, adresle girince Bugün açılır; yönetici normal kullanır' },
];
const ERISIM: Record<string, [string, Ton]> = {
  acik: ['Açık', 'iyi'], gizli: ['Gizli', 'kotu'], kapali: ['Kapalı', 'uyari'], 'yalniz-yonetici': ['Yalnız yönetici', 'vurgu'], bayrak: ['Bayrak kapalı', 'uyari'],
};
const ATLA = new Set(['manage', 'settings']);

type Satir = { id: AppRoute; ad: string; adres: string; varsayilan: string };

// H327: Görünürlük tek sayfada — "Sayfalar" (öğrenci sayfaları, eski içerik aynen) ve "İçerik" (tüm site_ayar.gorunurluk kayıtları).
// Diğer panel sayfaları yalnız rozet + buraya bağlantı gösterir (kit/Gorunurluk.tsx GorunurlukBaglantisi).
type Sekme = 'sayfalar' | 'icerik';
const sekmeOku = (): Sekme => (new URLSearchParams(window.location.search).get('sekme') === 'icerik' ? 'icerik' : 'sayfalar');

export default function SiteGorunurluk(p: SayfaProps) {
  const [sekme, setSekme] = useState<Sekme>(sekmeOku);
  React.useEffect(() => { const f = () => setSekme(sekmeOku()); window.addEventListener('popstate', f); return () => window.removeEventListener('popstate', f); }, []);
  const sec = (s2: Sekme) => {
    if (s2 === sekme) return;
    // Sekmeler arası tablo durumu (q, s.*, sayfa) taşınmaz
    p.git(s2 === 'icerik' ? 'site/gorunurluk?sekme=icerik' : 'site/gorunurluk', { degistir: true });
    setSekme(s2);
  };
  const cubuk = (
    <div className="m16-sekmeler" role="tablist" aria-label="Görünürlük bölümü" style={{ marginBottom: 12 }}>
      {([['sayfalar', 'Sayfalar'], ['icerik', 'İçerik']] as [Sekme, string][]).map(([k, e]) => (
        <button key={k} type="button" role="tab" aria-selected={sekme === k} className={sekme === k ? 'on' : ''} onClick={() => sec(k)}>{e}</button>
      ))}
    </div>
  );
  return sekme === 'icerik' ? <IcerikSekmesi cubuk={cubuk} git={p.git} /> : <SayfalarSekmesi cubuk={cubuk} />;
}

function SayfalarSekmesi({ cubuk }: { cubuk: React.ReactNode }) {
  const { veri: a, hata, yukleniyor, yenile, setVeri } = useSiteAyarAdmin();
  const [mesgul, setMesgul] = useState<string | null>(null);
  const satirlar = useMemo<Satir[]>(() => {
    const ids = new Set<string>([...Object.keys(NAV_ITEMS), ...KAPALI_SAYFALAR]);
    return [...ids].filter((r) => !ATLA.has(r)).map((r) => {
      const it = (NAV_ITEMS as any)[r];
      let adres = '';
      try { adres = pathFor(r as AppRoute); } catch { /* */ }
      return { id: r as AppRoute, ad: it?.label || r, adres, varsayilan: GIZLI_SAYFALAR.has(r as AppRoute) ? 'gizli' : KAPALI_SAYFALAR.has(r as AppRoute) ? 'kapali' : 'acik' };
    });
  }, []);

  // H141: yazım artık geri alınabilir (8 sn "Geri al"); öğrenciden sayfa kaldıran değişiklik hedef sunucuyu söyleyerek onay ister
  const yaz = async (anahtar: string, parca: Record<string, unknown>, metin: string, geri?: Record<string, unknown>) => {
    setMesgul(anahtar);
    const r = await siteAyarYaz(parca);
    if (r) {
      setVeri(r as any);
      bildir(metin, 'iyi', geri ? { etiket: 'Geri al', yap: () => { void siteAyarYaz(geri, 'Geri alındı').then((g) => { if (g) setVeri(g as any); }); } } : undefined);
    }
    setMesgul(null);
  };
  const kisitlar = (d: string) => d === 'gizli' || d === 'kapali' || d === 'yalniz-yonetici';
  const onayla = (ad: string, ne: string) =>
    onayIste({ baslik: `${ad}: ${ne}?`, aciklama: `Değişiklik ${yazimHedefi()} üzerinde hemen uygulanır; öğrenciler bu sayfayı menüde görmez ya da açamaz. 8 saniye içinde geri alabilirsin.`, onayMetni: 'Uygula' });

  if (hata && !a) return <><SayfaBasligi baslik="Görünürlük" />{cubuk}<Hata hata={hata} yenile={yenile} /></>;
  if (!a) return <><SayfaBasligi baslik="Görünürlük" />{cubuk}<Yukleniyor satir={8} /></>;
  const panelde = Object.keys(a.sayfalar).length + Object.values(a.menu).filter((v) => v === false).length;

  return (
    <>
      <SayfaBasligi
        baslik="Görünürlük"
        aciklama={`Öğrenci sayfalarının durumu ${yazimHedefi()} üzerinde hemen uygulanır (menü, merkez kartları, adres koruması). ${panelde} panel ayarı · sürüm ${a.surum}${a.guncelleyen ? ` · son: ${a.guncelleyen}` : ''}`}
        eylemler={panelde ? (
          <button type="button" className="m16-btn hayalet" disabled={!!mesgul} onClick={async () => {
            if (!(await onayIste({ baslik: 'Tüm sayfa ayarları sıfırlansın mı?', aciklama: 'Sayfa durumları ve menü gizlemeleri kod varsayılanına döner.', tehlikeli: true, yazilacak: 'SIFIRLA', onayMetni: 'Sıfırla' }))) return;
            const sil = (m: Record<string, unknown>) => Object.fromEntries(Object.keys(m).map((k) => [k, null]));
            void yaz('*', { sayfalar: sil(a.sayfalar), menu: sil(a.menu) }, 'Varsayılana döndü');
          }}><RotateCcw aria-hidden="true" />Varsayılana dön</button>
        ) : undefined}
      />
      {cubuk}
      <VeriTablosu<Satir>
        kimlik="site-gorunurluk"
        ogeler={satirlar}
        satirKimligi={(s) => s.id}
        aramaYeri="Sayfa ya da adres ara…"
        adresteDurum={false}
        boyut={200}
        sutunlar={[
          { anahtar: 'ad', baslik: 'Sayfa', genislik: 'minmax(180px,1.4fr)', deger: (s) => `${s.ad} ${s.id} ${s.adres}`, sirala: true,
            hucre: (s) => <span><b>{s.ad}</b><br /><code style={{ fontSize: 11 }}>{s.adres || s.id}</code></span> },
          { anahtar: 'etkin', baslik: 'Öğrenci görür', genislik: '150px', deger: (s) => ogrenciGorunumu(s.id, a).erisim,
            hucre: (s) => { const g = ogrenciGorunumu(s.id, a); const [e, t] = ERISIM[g.erisim]; return <span><Rozet ton={t}>{e}</Rozet>{g.erisim === 'acik' && !g.menude ? <> <Rozet ton="notr">menüde yok</Rozet></> : null}</span>; } },
          { anahtar: 'durum', baslik: 'Durum', genislik: 'minmax(360px,3fr)', deger: (s) => a.sayfalar[s.id] || 'varsayilan',
            hucre: (s) => {
              const cur = a.sayfalar[s.id] || 'varsayilan';
              return (
                <span className="m16-cip-grup" role="radiogroup" aria-label={`${s.ad} durumu`} onClick={(e) => e.stopPropagation()}>
                  {DURUM.map((o) => (
                    <button key={o.d} type="button" role="radio" aria-checked={cur === o.d} title={o.d === 'varsayilan' ? `${o.ipucu} (şu an: ${ERISIM[s.varsayilan][0]})` : o.ipucu}
                      disabled={mesgul === s.id} className={`m16-cip ${cur === o.d ? 'on' : ''}`}
                      onClick={async () => {
                        if (cur === o.d) return;
                        const yeni = o.d === 'varsayilan' ? s.varsayilan : o.d;
                        if (kisitlar(yeni) && !(await onayla(s.ad, o.etiket))) return;
                        void yaz(s.id, { sayfalar: { [s.id]: o.d === 'varsayilan' ? null : o.d } }, `${s.ad}: ${o.etiket}`, { sayfalar: { [s.id]: (cur as string) === 'varsayilan' ? null : cur } });
                      }}>
                      {o.etiket}
                    </button>
                  ))}
                </span>
              );
            } },
          { anahtar: 'menu', baslik: 'Menüde', genislik: '80px', hizala: 'orta', deger: (s) => (a.menu[s.id] === false ? 0 : 1),
            hucre: (s) => (
              <span onClick={(e) => e.stopPropagation()}>
                <Anahtar acik={a.menu[s.id] !== false} mesgul={mesgul === s.id} etiket={`${s.ad} menüde görünsün`}
                  degistir={async (v) => {
                    if (!v && !(await onayla(s.ad, 'menüden kaldırılsın'))) return;
                    const once = a.menu[s.id] === false ? false : null;
                    void yaz(s.id, { menu: { [s.id]: v ? null : false } }, `${s.ad}: menüde ${v ? 'görünür' : 'gizli'}`, { menu: { [s.id]: once } });
                  }} />
              </span>
            ) },
        ]}
      />
    </>
  );
}

/* ================= İçerik sekmesi (H328) ================= */
type IcerikSatiri = { anahtar: string; tur: string; turAd: string; ad: string; kurul: string; deger: string; ayarli?: boolean; sahipsiz?: boolean; brans?: string };
const TUR_SECENEK: [string, string][] = [['kurul', 'Kurul'], ['ders', 'Ders'], ['sesli', 'Sesli ders'], ['deste', 'Öğren destesi'], ['paket', 'İçerik paketi'], ['onem', 'Önem'], ['asistan', 'Asistan'], ['cozucu', 'Çözücü']];
const DEGERLER = Object.keys(GORUNURLUK_ETIKET) as GorunurlukDegeri[];

// H328: içerik görünürlüğünün TEK yazım yeri. Liste GET /api/admin/gorunurluk/icerik (yonetim16/icerik.ts), yazım
// PUT /api/admin/site-ayar {gorunurluk}. Etkin değer site ayarının kendisinden okunur (yazımdan hemen sonra doğru görünür).
// Gizleyen değişiklik onay ister (hedef yazimHedefi()), her değişiklik 8 sn Geri al; toplu seçimle toplu değiştirme.
function IcerikSekmesi({ cubuk, git }: { cubuk: React.ReactNode; git: SayfaProps['git'] }) {
  const { veri: a, setVeri } = useSiteAyarAdmin();
  const [mesgul, setMesgul] = useState(false);
  const [tabloNo, setTabloNo] = useState(0);
  const g = (a?.gorunurluk || {}) as Record<string, string>;
  const etkin = (x: IcerikSatiri) => (a ? g[x.anahtar] || 'acik' : x.deger);

  const uygula = async (anahtarlar: string[], y: GorunurlukDegeri, ad: string, temizle?: () => void) => {
    if (!anahtarlar.length) return;
    if (y !== 'acik' && !(await onayIste({
      baslik: `${anahtarlar.length > 1 ? `${anahtarlar.length} kayıt` : ad}: ${GORUNURLUK_ETIKET[y]} yapılsın mı?`,
      aciklama: `${anahtarlar.length > 1 ? `${anahtarlar.length} içerik` : anahtarlar[0]} öğrencilerden ${yazimHedefi()} üzerinde hemen ${y === 'gizli' ? 'gizlenir' : 'yalnız yöneticiye açık olur'}. 8 saniye içinde geri alabilirsin.`,
      onayMetni: 'Uygula',
    }))) return;
    const once: Record<string, string | null> = Object.fromEntries(anahtarlar.map((k) => [k, g[k] ?? null]));
    const sonra: Record<string, string | null> = Object.fromEntries(anahtarlar.map((k) => [k, y === 'acik' ? null : y]));
    setMesgul(true);
    const r = await siteAyarYaz({ gorunurluk: sonra });
    setMesgul(false);
    if (!r) return;
    setVeri(r as any);
    temizle?.();
    bildir(`${anahtarlar.length > 1 ? `${anahtarlar.length} kayıt` : ad}: ${GORUNURLUK_ETIKET[y]}`, 'iyi', {
      etiket: 'Geri al',
      yap: () => { void siteAyarYaz({ gorunurluk: once }, 'Geri alındı').then((x) => { if (x) setVeri(x as any); }); },
    });
  };
  const kisitliSuz = () => { git('site/gorunurluk?sekme=icerik&s.deger=kisitli', { degistir: true }); setTabloNo((n) => n + 1); };
  const kisitliSayi = Object.values(g).filter((v) => v && v !== 'acik').length;

  return (
    <>
      <SayfaBasligi baslik="Görünürlük"
        aciklama={`İçerik görünürlüğü yalnız buradan değişir; ${yazimHedefi()} üzerinde hemen uygulanır. Kurul, ders, sesli ders, deste, paket, önem, asistan ve çözücü kayıtları. ${kisitliSayi} kayıt açık değil.`} />
      {cubuk}
      <VeriTablosu<IcerikSatiri>
        key={tabloNo}
        kimlik="site-gorunurluk-icerik"
        kaynak="/api/admin/gorunurluk/icerik"
        canliOlay={['site_ayar_changed', 'content_changed']}
        satirKimligi={(x) => x.anahtar}
        aramaYeri="Ad ya da anahtar ara (ör. ders:k2-07)…"
        bosMetin="İçerik görünürlük kaydı yok"
        secim
        suzgecler={[
          { anahtar: 'tur', etiket: 'Tür', secenekler: TUR_SECENEK.map(([deger, etiket]) => ({ deger, etiket })) },
          { anahtar: 'kurul', etiket: 'Kurul', secenekler: [1, 2, 3, 4, 5, 6].map((n) => ({ deger: String(n), etiket: `Kurul ${n}` })) },
          { anahtar: 'deger', etiket: 'Durum', secenekler: [{ deger: 'kisitli', etiket: 'Açık olmayanlar' }, ...DEGERLER.map((d) => ({ deger: d, etiket: GORUNURLUK_ETIKET[d] }))] },
        ]}
        aracEk={<button type="button" className="m16-btn hayalet" onClick={kisitliSuz} title="Yalnız gizli ya da yalnız yöneticiye açık kayıtlar"><Filter aria-hidden="true" />Yalnız açık olmayanlar</button>}
        topluEylemler={(secili, temizle) => (
          <>
            {DEGERLER.map((d) => (
              <button key={d} type="button" className={`m16-btn ${d === 'gizli' ? 'tehlike' : ''}`} disabled={mesgul} onClick={() => void uygula(secili, d, `${secili.length} kayıt`, temizle)}>{GORUNURLUK_ETIKET[d]}</button>
            ))}
          </>
        )}
        sutunlar={[
          { anahtar: 'tur', baslik: 'Tür', genislik: '120px', sirala: true, hucre: (x) => <Rozet ton={x.sahipsiz ? 'uyari' : 'notr'}>{x.turAd}</Rozet> },
          { anahtar: 'ad', baslik: 'Ad', genislik: 'minmax(200px,2fr)', sirala: true,
            hucre: (x) => <span className="m16-kisalt" title={x.ad}>{x.sahipsiz ? <i>{x.ad}</i> : x.ad}</span> },
          { anahtar: 'anahtar', baslik: 'Anahtar', genislik: 'minmax(160px,1.2fr)', sirala: true, hucre: (x) => <code className="m16-kisalt" style={{ fontSize: 11 }} title={x.anahtar}>{x.anahtar}</code> },
          { anahtar: 'kurul', baslik: 'Kurul', genislik: '64px', sirala: true, hizala: 'orta' },
          { anahtar: 'deger', baslik: 'Etkin', genislik: '120px', sirala: true, hucre: (x) => <GorunurlukRozeti deger={etkin(x)} /> },
          { anahtar: 'degistir', baslik: 'Değiştir', genislik: 'minmax(260px,1.4fr)',
            hucre: (x) => {
              const v = etkin(x);
              return (
                <span className="m16-cip-grup" role="radiogroup" aria-label={`Görünürlük: ${x.anahtar}`} onClick={(e) => e.stopPropagation()}>
                  {DEGERLER.map((d) => (
                    <button key={d} type="button" role="radio" aria-checked={v === d} disabled={mesgul || !a} className={`m16-cip ${v === d ? 'on' : ''}`}
                      onClick={() => { if (v !== d) void uygula([x.anahtar], d, x.ad); }}>{GORUNURLUK_ETIKET[d]}</button>
                  ))}
                </span>
              );
            } },
        ]}
      />
    </>
  );
}
