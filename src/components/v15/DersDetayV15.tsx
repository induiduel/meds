import React, { useEffect, useMemo, useRef, useState } from 'react';
import { BookA, Check, ChevronRight, CircleHelp, ClipboardList, Download, Headphones, Layers, Lightbulb, Play, RotateCcw, MessageCircle, Stethoscope, Table2, ListOrdered, HelpCircle, WalletCards } from 'lucide-react';
import { linkClick, navigateTo, parseLocation, pathFor } from '../../router';
import { useAppearance } from '../../utils/appearance';
import { cdDetayGetir, cdKayitliKonum, cdSesUrl, cdTercihVaryant, fmtMb, type CdDetay } from '../canliDers/canliDersStore';
import { cdBransKisa } from '../canliDers/canliDersKategori';
import { bittiMi, sesliKonuId, useTakip } from '../../services/calismaTakip';
import { useV15Baslik } from './baslik';
import { bransYolu, dersBransi, dersKurulu, hocaYaz, merkezYolu, saatYaz, sureDk, useDersListesi } from './dersVeri';
import { Halka } from './Halka';
import DersIcerikV15 from './DersIcerikV15';
import { DI_BOLUMLER, dersIcerikGetir, type DiBolum, type DiPaket } from './dersIcerik';
import '../../styles/v15/dersler.css';

/**
 * v15 · Ders ayrıntısı (tasarım sistemi v15 › B03). Adres /dersler/ders/kurulN/<dersKey> (iç /ders/<key>).
 * Kaldığın yer kartı (halka, bölüm, sürdür / MP3 indir) → "Bu dersin içerikleri" (sesli ders, Öğren destesi, çıkmış
 * sorular) → Bölümler zaman çizelgesi (her bölüm sesli derste o paragrafı açar). PC'de bölümler sağ sütunda.
 * Yalnız gerçek veri: içeriği olmayan satır çizilmez. v15 dışında sesli derse yönlenir.
 */
const anahtarOku = () => {
  const { route, param } = parseLocation();
  return route === 'ders_detay' ? param || '' : '';
};

export default function DersDetayV15() {
  const { v15 } = useAppearance();
  const [key, setKey] = useState(anahtarOku);
  useEffect(() => {
    const f = () => setKey(anahtarOku());
    window.addEventListener('popstate', f);
    return () => window.removeEventListener('popstate', f);
  }, []);
  useEffect(() => {
    if (!v15 && key) navigateTo(pathFor('canli_ders', key));
  }, [v15, key]);

  const [bolumAd, setBolumAd] = useState(() => new URLSearchParams(window.location.search).get('b') || '');
  useEffect(() => {
    const f = () => setBolumAd(new URLSearchParams(window.location.search).get('b') || '');
    window.addEventListener('popstate', f);
    return () => window.removeEventListener('popstate', f);
  }, []);
  const [paket, setPaket] = useState<DiPaket | null>(null);
  useEffect(() => {
    setPaket(null);
    if (key) dersIcerikGetir(key).then(setPaket).catch(() => undefined);
  }, [key]);
  const { dersler } = useDersListesi();
  const ozet = useMemo(() => dersler?.find((d) => d.key === key) || null, [dersler, key]);
  const [detay, setDetay] = useState<CdDetay | null>(null);
  const [hata, setHata] = useState<string | null>(null);
  useEffect(() => {
    if (!key) return;
    let canli = true;
    setDetay(null);
    setHata(null);
    cdDetayGetir(key).then(
      (d) => canli && setDetay(d),
      (e) => canli && setHata(e?.message || 'Ders açılamadı.'),
    );
    return () => {
      canli = false;
    };
  }, [key]);

  const [desteSlayt, setDesteSlayt] = useState<number | null>(null);
  const desteId = detay?.desteId || ozet?.desteId;
  useEffect(() => {
    if (!desteId) return;
    let canli = true;
    import('../../data/deckStore')
      .then((m) => m.loadDeckCatalog())
      .then((c) => canli && setDesteSlayt(c.find((d) => d.id === desteId)?.slideCount ?? null))
      .catch(() => undefined);
    return () => {
      canli = false;
    };
  }, [desteId]);

  const takip = useTakip();
  const bitti = key ? bittiMi(takip.k[`sesli:${sesliKonuId(key)}`]) : false;
  const konum = useMemo(() => (key ? cdKayitliKonum(key) : null), [key]);

  const varyant = useMemo(() => {
    const vs = detay?.varyantlar || ozet?.varyantlar || [];
    return vs.find((v) => v.id === konum?.vid) || cdTercihVaryant(vs) || vs[0];
  }, [detay, ozet, konum]);
  const sure = varyant?.sureSn || ozet?.varsayilan?.sureSn || 0;
  const t = konum?.t ?? null;
  const pct = bitti ? 100 : t != null && sure ? Math.min(99, Math.round((t / sure) * 100)) : 0;

  // Bölümler: başlangıç saniyesi = bölümün ilk paragrafının ses zamanlaması
  const bolumler = useMemo(() => {
    if (!detay) return [];
    const z = varyant?.zamanlama;
    return detay.bolumler
      .map((b) => {
        const p = b.paragraflar[0]?.i;
        const bas = p != null && z?.[p] && Number.isFinite(z[p][0]) ? z[p][0] : null;
        return { baslik: b.baslik || 'Bölüm', p, bas };
      })
      .filter((b) => b.p != null);
  }, [detay, varyant]);
  const simdiki = useMemo(() => {
    if (bitti) return bolumler.length;
    if (t == null) return -1;
    let k = -1;
    bolumler.forEach((b, i) => {
      if (b.bas != null && b.bas <= t) k = i;
    });
    return k;
  }, [bolumler, t, bitti]);

  // Bölüm listesi kaldığın bölüme kayar (yalnız listenin kendi içinde; sayfa kaymaz)
  const tlRef = useRef<HTMLOListElement>(null);
  useEffect(() => {
    const ol = tlRef.current;
    const li = ol?.querySelector<HTMLElement>('li.is-now');
    if (ol && li) ol.scrollTop = Math.max(0, li.offsetTop - ol.clientHeight / 2 + li.offsetHeight / 2);
  }, [simdiki, bolumler.length]);

  const brans = ozet ? dersBransi(ozet) : detay?.brans || '';
  const kurul = ozet ? dersKurulu(ozet) : detay?.kurul || 1;
  const no = ozet?.no ?? detay?.no;
  const baslik = ozet?.baslik || detay?.baslik || 'Ders';
  const hoca = hocaYaz(ozet?.hoca || detay?.hoca);
  useV15Baslik({
    baslik,
    alt: bolumAd ? DI_BOLUMLER.find((b) => b.id === bolumAd)?.ad || '' : [brans && cdBransKisa(brans), no != null ? `Ders ${no}` : '', hoca].filter(Boolean).join(' · '),
    geri: bolumAd ? `${pathFor('ders_detay', key)}` : brans ? bransYolu(kurul, brans) : merkezYolu(kurul),
  });

  if (!key) return <p className="dd15-bos v15-card">Ders bulunamadı.</p>;
  const altSayfa = DI_BOLUMLER.find((b) => b.id === bolumAd);
  if (altSayfa) return <DersIcerikV15 dersKey={key} bolum={altSayfa.id} />;
  const dinle = pathFor('canli_ders', key);
  const cikmis = detay?.cikmisKonum || [];
  const yillar = [...new Set(cikmis.map((c) => Number(c.yil)).filter((y) => y > 1990))].sort();
  const pdfVar = !!(detay?.pdf || ozet?.pdf);

  const icerik: { id: string; tone: string; icon: React.ElementType; t: string; s: string; url: string }[] = [
    { id: 'sesli', tone: '', icon: Headphones, t: 'Sesli ders', s: [sureDk(sure), pdfVar ? 'PDF + akan metin' : 'akan metin'].filter(Boolean).join(' · '), url: dinle },
  ];
  if (desteId)
    icerik.push({ id: 'deste', tone: 'is-c', icon: Layers, t: 'Öğren destesi', s: desteSlayt ? `${desteSlayt} slayt · adım adım, mini sorularla` : 'Adım adım, mini sorularla', url: `/dersler/interaktif/${encodeURIComponent(desteId)}` });
  if (cikmis.length)
    icerik.push({
      id: 'cikmis', tone: 'is-ok', icon: CircleHelp, t: 'Çıkmış sorular',
      s: `${cikmis.length} soru${yillar.length ? ` · ${yillar[0]}${yillar.length > 1 ? `–${yillar[yillar.length - 1]}` : ''}` : ''} · derste geçtiği yerde işaretli`,
      url: `${dinle}?p=${cikmis[0].p}`,
    });

  if (paket) {
    const say: Record<DiBolum, [number, string, React.ElementType, string]> = {
      terimler: [paket.terimler.length + paket.kisaltmalar.length, 'terim ve kısaltma · tanımlarıyla', BookA, 'is-ok'],
      hastaliklar: [paket.hastaliklar.length, 'hastalık ve kavram · başlık başlık', Stethoscope, 'is-c'],
      bilgiler: [paket.onemli.length + paket.spotlar.length + paket.bilgiler.length, 'önemli nokta ve sınav spotu', Lightbulb, ''],
      listeler: [paket.listeler.length, 'sıralama ve liste · sıra türüyle', ListOrdered, 'is-ok'],
      quiz: [paket.quiz.length, 'mini soru · anında geri bildirim', HelpCircle, 'is-c'],
      tablolar: [paket.tablolar.length, 'tablo ve karşılaştırma', Table2, 'is-c'],
      sorular: [-1, 'müfredata sadık örnek soru · anında geri bildirim', ClipboardList, 'is-ok'],
      kartlar: [paket.kartlar.length, 'hatırlatma kartı', WalletCards, ''],
    };
    for (const b of DI_BOLUMLER) {
      const [n, a, ic, tone] = say[b.id];
      if (n === 0) continue;
      icerik.push({ id: b.id, tone, icon: ic, t: b.ad, s: n > 0 ? `${n} ${a}` : a, url: `${pathFor('ders_detay', key)}?b=${b.id}` });
    }
  }

  const durum = bitti ? 'Bu dersi bitirdin' : t != null ? `Kaldığın yer: ${saatYaz(t)}` : 'Henüz başlamadın';
  const durumAlt =
    bolumler.length && simdiki >= 0 && simdiki < bolumler.length
      ? `${bolumler[simdiki].baslik} · ${simdiki + 1}/${bolumler.length} bölüm`
      : bolumler.length
        ? `${bolumler.length} bölüm${sure ? ` · ${sureDk(sure)}` : ''}`
        : sureDk(sure);

  return (
    <div className="dd15">
      <h1 className="sr-only">{baslik}</h1>
      <div className="dd15-in">
        <div className="dd15-main">
          <section className="dd15-resume v15-card" aria-label="Kaldığın yer">
            <div className="dd15-resume-h">
              <Halka pct={pct} boyut={56} etiket={bitti ? 'Bitti' : `%${pct} dinlendi`} />
              <span className="dd15-resume-t">
                <b>{durum}</b>
                <span>{durumAlt}</span>
              </span>
            </div>
            <div className="dd15-resume-a">
              <a className="v15-btn dd15-cta" href={dinle} onClick={linkClick(() => navigateTo(dinle))}>
                {bitti ? <RotateCcw aria-hidden /> : <Play aria-hidden />}
                {bitti ? 'Yeniden dinle' : t != null ? 'Sesli dersi sürdür' : 'Sesli dersi başlat'}
              </a>
              {varyant && (
                <a className="v15-btn is-ghost dd15-dl" href={cdSesUrl(key, varyant.id, true)} download aria-label={`MP3 indir${varyant.bayt ? ` (${fmtMb(varyant.bayt)})` : ''}`} title={`MP3 indir${varyant.bayt ? ` · ${fmtMb(varyant.bayt)}` : ''}`}>
                  <Download aria-hidden />
                </a>
              )}
            </div>
          </section>

          <section aria-labelledby="dd15-ic-h">
            <h2 id="dd15-ic-h" className="v15-h2 dd15-h">Bu dersin içerikleri</h2>
            <ul className="dd15-list v15-card" role="list">
              {icerik.map((x) => (
                <li key={x.id}>
                  <a className="dd15-row" href={x.url} onClick={linkClick(() => navigateTo(x.url))}>
                    <span className={`v15-tile ${x.tone}`}><x.icon aria-hidden /></span>
                    <span className="dd15-row-t">
                      <b>{x.t}</b>
                      <span>{x.s}</span>
                    </span>
                    <ChevronRight className="v15-chev" aria-hidden />
                  </a>
                </li>
              ))}
              {/* Topluluk: bu dersin yorum kanalı (V2 ayrı ders sayılmaz) */}
              <li>
                <a className="dd15-row" href={`/topluluk?kanal=ders:${key.replace(/-v\d+$/, '')}`} onClick={linkClick(() => navigateTo(`/topluluk?kanal=ders:${key.replace(/-v\d+$/, '')}`))}>
                  <span className="v15-tile is-n"><MessageCircle aria-hidden /></span>
                  <span className="dd15-row-t"><b>Yorumlar</b><span>Bu ders hakkında arkadaşlarınla yazış</span></span>
                  <ChevronRight className="v15-chev" aria-hidden />
                </a>
              </li>
            </ul>
          </section>
        </div>

        <section className="dd15-side" aria-labelledby="dd15-b-h">
          <h2 id="dd15-b-h" className="v15-h2 dd15-h">Bölümler</h2>
          {detay ? (
            bolumler.length ? (
              <ol ref={tlRef} className="dd15-tl v15-card" role="list">
                {bolumler.map((b, i) => {
                  const st = i < simdiki ? 'is-ok' : i === simdiki ? 'is-now' : '';
                  const url = `${dinle}?p=${b.p}`;
                  return (
                    <li key={i} className={st}>
                      <a href={url} onClick={linkClick(() => navigateTo(url))} aria-current={i === simdiki ? 'step' : undefined}>
                        <span className="dd15-tl-n" aria-hidden>{i < simdiki ? <Check /> : i + 1}</span>
                        <span className="dd15-tl-t">
                          <b>{b.baslik}</b>
                          {b.bas != null && <span>{saatYaz(b.bas)}</span>}
                        </span>
                      </a>
                    </li>
                  );
                })}
              </ol>
            ) : (
              <p className="dd15-bos v15-card">Bu derste bölüm başlığı yok.</p>
            )
          ) : hata ? (
            <p className="dd15-bos v15-card">{hata}</p>
          ) : (
            <span className="v15-skel dd15-skel" aria-hidden />
          )}
        </section>
      </div>
    </div>
  );
}
