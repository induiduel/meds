import React, { useEffect, useMemo, useState } from 'react';
import { ChevronDown, ChevronRight, Headphones, Video } from 'lucide-react';
import { linkClick, navigateTo, pathFor, type AppRoute } from '../../router';
import { NAV_ITEMS } from '../shell/navModel';
import { KURUL_NOLAR, kurulKaydet, useSeciliKurul } from '../kurul/KurulSecici';
import { MERKEZ_ARACLARI } from '../merkez/merkezModel';
import { menudeGorunur } from '../../services/siteAyar';
import { Sheet } from '../ui/Sheet';
import { useV15Baslik } from './baslik';
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
const TON: Partial<Record<AppRoute, string>> = { canli_ders: '', learn: 'is-c', summaries: 'is-w', flashcards: 'is-ai', kmb_asistan: 'is-ok' };

/** Kurula bağlı araç kurulun altında açılır */
const aracYolu = (id: AppRoute, kurul: number) =>
  id === 'canli_ders' ? `/dersler/canliders/kurul${kurul}` : id === 'learn' ? `${pathFor('learn')}?kurul=${kurul}` : pathFor(id);

const git = (url: string) => linkClick(() => navigateTo(url));

export default function DerslerMerkezV15() {
  const kurul = useSeciliKurul();
  const { dersler, hata } = useDersListesi();
  const ilerleme = useIlerleme();
  useSiteAyar();
  const [diger, setDiger] = useState(false);
  // O01 giriş: yalnız sunucuda hazır ders videosu varken görünür
  const videolar = useHazirVideolar();
  const [desteN, setDesteN] = useState<number | null>(null);

  useEffect(() => {
    let canli = true;
    import('../../data/deckStore')
      .then((m) => m.loadDeckCatalog())
      .then((c) => canli && setDesteN(c.filter((d) => !icerikGizli('deste', d.id) && new RegExp(`Kurul ${kurul}\\b`).test(String(d.committee || ''))).length))
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

      <nav className="d15-tools" aria-label="Ders çalış araçları">
        {ANA.filter((id) => menudeGorunur(id)).map((id) => {
          const it = NAV_ITEMS[id];
          const a = MERKEZ_ARACLARI.dersler.find((x) => x.id === id);
          return (
            <a key={id} className="d15-tool v15-card" href={aracYolu(id, kurul)} onClick={git(aracYolu(id, kurul))} title={a?.ne}>
              <span className={`v15-tile ${TON[id] || ''}`}><it.icon aria-hidden /></span>
              <b>{it.label}</b>
              <span className="d15-tool-s">{sayi[id] || it.hint}</span>
            </a>
          );
        })}
      </nav>

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

      {digerAraclar.length > 0 && (
        <button type="button" className="d15-diger" onClick={() => setDiger(true)} aria-haspopup="dialog">
          <span className="d15-diger-ic" aria-hidden>
            {digerAraclar.slice(0, 3).map((a) => {
              const I = NAV_ITEMS[a.id].icon;
              return <span key={a.id} className={`v15-tile ${TON[a.id] || ''}`}><I /></span>;
            })}
          </span>
          <span className="d15-diger-t">
            <b>Diğer araçlar</b>
            <span>
              {digerAraclar.slice(0, 3).map((a) => NAV_ITEMS[a.id].label).join(' · ')}
              {digerAraclar.length > 3 ? ` +${digerAraclar.length - 3}` : ''}
            </span>
          </span>
          <ChevronRight className="v15-chev" aria-hidden />
        </button>
      )}

      {!!videolar?.length && (
        <a className="d15-diger" href="/video-ders" onClick={git('/video-ders')}>
          <span className="d15-diger-ic" aria-hidden><span className="v15-tile"><Video /></span></span>
          <span className="d15-diger-t">
            <b>Video dersler</b>
            <span>{videolar.length} hazır video · tam ekran, resim içinde resim</span>
          </span>
          <ChevronRight className="v15-chev" aria-hidden />
        </a>
      )}

      <Sheet open={diger} onClose={() => setDiger(false)} title="Diğer araçlar">
        <ul className="d15-sheet" role="list">
          {digerAraclar.map((a) => {
            const it = NAV_ITEMS[a.id];
            return (
              <li key={a.id}>
                <a
                  href={aracYolu(a.id, kurul)}
                  onClick={linkClick(() => {
                    setDiger(false);
                    navigateTo(aracYolu(a.id, kurul));
                  })}
                  className="d15-sheet-a"
                >
                  <span className={`v15-tile ${TON[a.id] || ''}`}><it.icon aria-hidden /></span>
                  <span className="d15-sheet-t">
                    <b>{it.label}</b>
                    <span>{a.ne}</span>
                  </span>
                  <ChevronRight className="v15-chev" aria-hidden />
                </a>
              </li>
            );
          })}
        </ul>
      </Sheet>
    </div>
  );
}
