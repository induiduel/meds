import React, { useMemo, useState } from 'react';
import { RotateCcw } from 'lucide-react';
import { SayfaBasligi, VeriTablosu, Rozet, Hata, Yukleniyor, onayIste, type Ton } from '../kit';
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

export default function SiteGorunurluk(_p: SayfaProps) {
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

  const yaz = async (anahtar: string, parca: Record<string, unknown>, metin: string) => {
    setMesgul(anahtar);
    const r = await siteAyarYaz(parca, metin);
    if (r) setVeri(r as any);
    setMesgul(null);
  };

  if (hata && !a) return <><SayfaBasligi baslik="Görünürlük" /><Hata hata={hata} yenile={yenile} /></>;
  if (!a) return <><SayfaBasligi baslik="Görünürlük" /><Yukleniyor satir={8} /></>;
  const panelde = Object.keys(a.sayfalar).length + Object.values(a.menu).filter((v) => v === false).length;

  return (
    <>
      <SayfaBasligi
        baslik="Görünürlük"
        aciklama={`Öğrenci sayfalarının durumu canlı uygulanır (menü, merkez kartları, adres koruması). ${panelde} panel ayarı · sürüm ${a.surum}${a.guncelleyen ? ` · son: ${a.guncelleyen}` : ''}`}
        eylemler={panelde ? (
          <button type="button" className="m16-btn hayalet" disabled={!!mesgul} onClick={async () => {
            if (!(await onayIste({ baslik: 'Tüm sayfa ayarları sıfırlansın mı?', aciklama: 'Sayfa durumları ve menü gizlemeleri kod varsayılanına döner.', tehlikeli: true, yazilacak: 'SIFIRLA', onayMetni: 'Sıfırla' }))) return;
            const sil = (m: Record<string, unknown>) => Object.fromEntries(Object.keys(m).map((k) => [k, null]));
            void yaz('*', { sayfalar: sil(a.sayfalar), menu: sil(a.menu) }, 'Varsayılana döndü');
          }}><RotateCcw aria-hidden="true" />Varsayılana dön</button>
        ) : undefined}
      />
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
                      onClick={() => cur !== o.d && void yaz(s.id, { sayfalar: { [s.id]: o.d === 'varsayilan' ? null : o.d } }, `${s.ad}: ${o.etiket}`)}>
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
                  degistir={(v) => void yaz(s.id, { menu: { [s.id]: v ? null : false } }, `${s.ad}: menüde ${v ? 'görünür' : 'gizli'}`)} />
              </span>
            ) },
        ]}
      />
    </>
  );
}
