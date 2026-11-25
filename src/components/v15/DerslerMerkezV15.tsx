import React, { useEffect, useMemo, useState } from 'react';
import { Headphones, Video } from 'lucide-react';
import { linkClick, navigateTo, pathFor, type AppRoute } from '../../router';
import { NAV_ITEMS } from '../shell/navModel';
import { KURUL_NOLAR, kurulKaydet, useSeciliKurul } from '../kurul/KurulSecici';
import { MERKEZ_ARACLARI } from '../merkez/merkezModel';
import { menudeGorunur } from '../../services/siteAyar';
import { useV15Baslik } from './baslik';
import { KlinikDizin } from './klinik/KlinikDizin';
import KurulSecV15 from './KurulSecV15';
import { useHazirVideolar } from './VideoDersV15';
import { icerikGizli, kurulGizli, useSiteAyar } from '../../services/siteAyar';
import IcerikKapaliV15 from './IcerikKapaliV15';
import { bransYolu, dersAdi, dersKurulu, dersSirala, dersYolu, kurulBranslari, merkezYolu, sureDk, useDersListesi, useIlerleme } from './dersVeri';
import { cdBransKisa } from '../canliDers/canliDersKategori';
import '../../styles/v15/dersler.css';

/**
 * v15 · Ders çalış merkezi (tasarım sistemi v15 › B01 dersler, Z02 araç listesi). Tek ekran:
 * kurul + branş çipleri → 4 ana araç kartı → "Devam et" (kaldığın sesli dersler) → "Diğer araçlar" satırı (çekmece).
 * Branş çipi branş ders listesine, devam kartı ders ayrıntısına gider.
 */
const ANA: AppRoute[] = ['canli_ders', 'learn', 'summaries', 'flashcards'];

/** Kurula bağlı araç kurulun altında açılır */
const aracYolu = (id: AppRoute, kurul: number) =>
  id === 'canli_ders' ? `/dersler/canliders/kurul${kurul}` : id === 'learn' ? `${pathFor('learn')}?kurul=${kurul}` : pathFor(id);

const git = (url: string) => linkClick(() => navigateTo(url));

export default function DerslerMerkezV15() {
  const kurul = useSeciliKurul();
  const { dersler, hata } = useDersListesi();
  const ilerleme = useIlerleme();
  useSiteAyar();
  // O01 giriş: yalnız sunucuda hazır ders videosu varken görünür
  const videolar = useHazirVideolar();
  const [desteN, setDesteN] = useState<number | null>(null);

  useEffect(() => {
    let canli = true;
    // H157: merkez yayında olmayan (taslak/eski) desteleri de sayıyordu (7), kitaplık yalnız yayındakileri (5) — aynı
    // yüklem (isPublished + kurulOf) iki yerde kullanılır
    Promise.all([import('../../data/deckStore'), import('../learn/LearnLibrary')])
      .then(([m, L]) => m.loadDeckCatalog().then((c) => ({ c, L })))
      .then(({ c, L }) => canli && setDesteN(c.filter((d) => !icerikGizli('deste', d.id) && L.isPublished(d) && L.kurulOf(d) === `Kurul ${kurul}`).length))
      .catch(() => canli && setDesteN(null));
    return () => {
      canli = false;
    };
  }, [kurul]);

  const kuruldakiler = useMemo(() => (dersler ? dersler.filter((d) => dersKurulu(d) === kurul) : null), [dersler, kurul]);
  const branslar = useMemo(() => (dersler ? kurulBranslari(dersler, kurul) : []), [dersler, kurul]);

  // Devam et: kaldığın yer kaydı olan dersler (en yeni önce); yoksa kurulda bitmemiş ilk ders
  const devam = useMemo(() => {
    if (!kuruldakiler) return [];
    const ip = kuruldakiler.map((d) => ({ d, i: ilerleme(d) }));
    const yarim = ip.filter((x) => x.i.t != null && !x.i.bitti).sort((a, b) => b.i.at - a.i.at);
    if (yarim.length) return yarim.slice(0, 3);
    const ilk = dersSirala(kuruldakiler).find((d) => !ilerleme(d).bitti);
    return ilk ? [{ d: ilk, i: ilerleme(ilk) }] : [];
  }, [kuruldakiler, ilerleme]);

  useV15Baslik({ baslik: 'Ders çalış', alt: kuruldakiler ? `Kurul ${kurul} · ${kuruldakiler.length} sesli ders` : `Kurul ${kurul}` });

  const sayi: Partial<Record<AppRoute, string>> = {
    canli_ders: kuruldakiler ? `${kuruldakiler.length} ders` : '',
    learn: desteN != null ? `${desteN} deste` : '',
  };
  const digerAraclar = MERKEZ_ARACLARI.dersler.filter((a) => !ANA.includes(a.id) && NAV_ITEMS[a.id]);

  if (kurulGizli(kurul)) return <IcerikKapaliV15 ne={`Kurul ${kurul}`} />;
  return (
    <div className="d15">
      <h1 className="sr-only">Ders çalış</h1>
      <div className="d15-chips v15-hscroll" role="navigation" aria-label="Kurul ve branş">
        <KurulSecV15 kurul={kurul} onSec={(k) => navigateTo(merkezYolu(k))} />
        {branslar.map((b) => (
          <a key={b.ad} className="d15-chip" href={bransYolu(kurul, b.ad)} onClick={git(bransYolu(kurul, b.ad))}>
            {b.kisa}
            <span>{b.dersler.length}</span>
          </a>
        ))}
        {dersler && !branslar.length && <span className="d15-chip is-bos">Kurul {kurul} için sesli ders henüz yok</span>}
      </div>

      {/* H676: üç araç kartı yerine klinik dizin; sayaç sağda eş aralıklı */}
      <KlinikDizin
        harf="A"
        baslik="Çalışma araçları"
        ogeler={ANA.filter((id) => menudeGorunur(id)).map((id) => {
          const it = NAV_ITEMS[id];
          const a = MERKEZ_ARACLARI.dersler.find((x) => x.id === id);
          return { id, ad: it.label, ne: a?.ne, url: aracYolu(id, kurul), ikon: it.icon, meta: sayi[id] || undefined };
        })}
      />

      <section className="d15-devam" aria-labelledby="d15-devam-h">
        <div className="d15-sec-h">
          <h2 id="d15-devam-h" className="v15-h2">{devam.some((x) => x.i.t != null) ? 'Devam et' : 'Sıradaki ders'}</h2>
          <a className="d15-more" href={`/dersler/canliders/kurul${kurul}`} onClick={git(`/dersler/canliders/kurul${kurul}`)}>Tüm dersler</a>
        </div>
        {kuruldakiler === null ? (
          <div className="d15-devam-l"><span className="v15-skel d15-skel" /><span className="v15-skel d15-skel" /><span className="v15-skel d15-skel" /></div>
        ) : devam.length ? (
          <div className="d15-devam-l">
            {devam.map(({ d, i }) => (
              <a key={d.key} className="d15-dk v15-card" href={dersYolu(d.key)} onClick={git(dersYolu(d.key))}>
                <span className="v15-label">{cdBransKisa(d.brans || 'Diğer')}</span>
                <b className="d15-dk-t">{dersAdi(d)}</b>
                <span className="v15-bar" role="progressbar" aria-valuemin={0} aria-valuemax={100} aria-valuenow={i.pct} aria-label="İlerleme">
                  <span style={{ width: `${i.pct}%` }} />
                </span>
                <span className="d15-dk-f">
                  <span>{i.t != null ? `%${i.pct}` : sureDk(i.sure) || 'Başla'}</span>
                  <Headphones aria-hidden />
                </span>
              </a>
            ))}
          </div>
        ) : (
          // H148: "bitirdin ya da henüz yok" ikili mesajı yerine durum ayrı söylenir; boşsa geçmiş kurula geçiş verilir
          <div className="d15-bos v15-card">
            {hata ? <p>Ders listesi alınamadı: {hata}</p>
              : kuruldakiler && kuruldakiler.length ? <p>Kurul {kurul} derslerinin hepsini bitirdin. Tekrar için <a href={pathFor('canli_ders')} onClick={git(pathFor('canli_ders'))}>tüm dersler</a>.</p>
              : <p>Kurul {kurul} için sesli ders henüz eklenmedi. {kurul > 1 && <a href={`/dersler/canliders/kurul${kurul - 1}`} onClick={git(`/dersler/canliders/kurul${kurul - 1}`)}>Kurul {kurul - 1} derslerine geç</a>}</p>}
          </div>
        )}
      </section>

      {/* H676: "Diğer araçlar" alt penceresi kaldırıldı: araçlar sayfada doğrudan görünür (bir dokunuş az, bulunabilir) */}
      <KlinikDizin
        harf="B"
        baslik="Diğer araçlar"
        baslangic={ANA.filter((id) => menudeGorunur(id)).length + 1}
        ogeler={[
          ...digerAraclar.map((a) => ({ id: a.id, ad: NAV_ITEMS[a.id].label, ne: a.ne, url: aracYolu(a.id, kurul), ikon: NAV_ITEMS[a.id].icon })),
          ...(videolar?.length ? [{ id: 'video', ad: 'Video dersler', ne: 'Tam ekran, resim içinde resim', url: '/video-ders', ikon: Video, meta: String(videolar.length) }] : []),
        ]}
      />
    </div>
  );
}
