import React, { useEffect, useMemo, useRef, useState } from 'react';
import { BookA, Check, ChevronDown, ChevronRight, CircleHelp, ClipboardList, Download, Headphones, Layers, Lightbulb, Play, RotateCcw, MessageCircle, Stethoscope, Table2, ListOrdered, HelpCircle, WalletCards } from 'lucide-react';
import { linkClick, navigateTo, parseLocation, pathFor } from '../../router';
import { useAppearance } from '../../utils/appearance';
import { cdDetayGetir, cdKayitliKonum, cdSesUrl, cdTercihVaryant, fmtMb, type CdDetay } from '../canliDers/canliDersStore';
import { cdBransKisa } from '../canliDers/canliDersKategori';
import { bittiMi, sesliKonuId, useTakip } from '../../services/calismaTakip';
import { useV15Baslik } from './baslik';
import { bransYolu, dersBransi, dersKurulu, hocaYaz, merkezYolu, saatYaz, sureDk, useDersListesi } from './dersVeri';
import { Halka } from './Halka';
import { dersCozucu } from '../canliDers/dersCozucu';
import DersIcerikV15 from './DersIcerikV15';
import DersIstatV15 from './DersIstatV15';
import DersPdfEkranV15 from './DersPdfEkranV15';
import { DI_BOLUMLER, dersIcerikGetir, type DiBolum, type DiPaket } from './dersIcerik';
import IcerikKapaliV15 from './IcerikKapaliV15';
import { icerikGizli, useSiteAyar } from '../../services/siteAyar';
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

const GRUP_KEY = 'medsoru_dd15_grup_v2'; // v2: varsayılan kapalı (eski açık tercihleri sayılmaz)
const ICERIK_GRUP: { id: string; ad: string; idler: string[]; varsayilan: boolean }[] = [
  { id: 'calis', ad: 'Dinle ve çalış', idler: ['sesli', 'deste', 'pdf'], varsayilan: false },
  { id: 'soru', ad: 'Soru çöz', idler: ['cikmis', 'cozucu', 'sorular', 'quiz'], varsayilan: false },
  { id: 'bilgi', ad: 'Bilgi kartları', idler: ['terimler', 'hastaliklar', 'bilgiler', 'listeler', 'tablolar', 'kartlar'], varsayilan: false },
];

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
  useSiteAyar();
  const { dersler, hepsi } = useDersListesi();
  const ozet = useMemo(() => (hepsi || dersler)?.find((d) => d.key === key) || null, [dersler, hepsi, key]);
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
    alt: bolumAd ? (bolumAd === 'pdf' ? 'Ders PDF\'i' : DI_BOLUMLER.find((b) => b.id === bolumAd)?.ad || '') : [brans && cdBransKisa(brans), no != null ? `Ders ${no}` : '', hoca].filter(Boolean).join(' · '),
    geri: bolumAd ? `${pathFor('ders_detay', key)}` : brans ? bransYolu(kurul, brans) : merkezYolu(kurul),
  });

  const [grupAcik, setGrupAcik] = useState<Record<string, boolean>>(() => { try { return JSON.parse(localStorage.getItem(GRUP_KEY) || '{}'); } catch { return {}; } });
  const grupYaz = (id: string, ac: boolean) => setGrupAcik((g) => { if (g[id] === ac) return g; const n = { ...g, [id]: ac }; try { localStorage.setItem(GRUP_KEY, JSON.stringify(n)); } catch { /* yok */ } return n; });
  if (!key) return <p className="dd15-bos v15-card">Ders bulunamadı.</p>;
  if (icerikGizli('sesli', key)) return <IcerikKapaliV15 ne="Bu ders" geri={{ yol: '/dersler', etiket: 'Derslere dön' }} />;
  if (bolumAd === 'pdf') return <DersPdfEkranV15 dersKey={key} />;
  const altSayfa = DI_BOLUMLER.find((b) => b.id === bolumAd);
  if (altSayfa && icerikGizli('paket', key.replace(/-v\d+$/, ''))) return <IcerikKapaliV15 ne="Bu içerik bölümü" geri={{ yol: pathFor('ders_detay', key), etiket: 'Derse dön' }} />;
  if (altSayfa) return <DersIcerikV15 dersKey={key} bolum={altSayfa.id} />;
  const dinle = pathFor('canli_ders', key);
  const cikmis = detay?.cikmisKonum || [];
  const yillar = [...new Set(cikmis.map((c) => Number(c.yil)).filter((y) => y > 1990))].sort();
  const pdfVar = !!(detay?.pdf || ozet?.pdf);

  const icerik: { id: string; tone: string; icon: React.ElementType; t: string; s: string; url: string; k?: string }[] = [
    { id: 'sesli', tone: '', icon: Headphones, t: 'Sesli ders', s: [sureDk(sure), pdfVar ? 'PDF + akan metin' : 'akan metin'].filter(Boolean).join(' · '), url: dinle, k: sureDk(sure) || 'akan metin' },
  ];
  if (desteId)
    icerik.push({ id: 'deste', tone: 'is-c', icon: Layers, t: 'Öğren destesi', s: desteSlayt ? `${desteSlayt} slayt · adım adım, mini sorularla` : 'Adım adım, mini sorularla', url: `/dersler/interaktif/${encodeURIComponent(desteId)}`, k: desteSlayt ? `${desteSlayt} slayt` : 'adım adım' });
  if (cikmis.length)
    icerik.push({
      id: 'cikmis', tone: 'is-ok', icon: CircleHelp, t: 'Çıkmış sorular',
      s: `${cikmis.length} soru${yillar.length ? ` · ${yillar[0]}${yillar.length > 1 ? `–${yillar[yillar.length - 1]}` : ''}` : ''} · derste geçtiği yerde işaretli`,
      url: `${dinle}?p=${cikmis[0].p}`, k: `${cikmis.length} soru`,
    });

  const coz = dersCozucu(paket?.baslik) || dersCozucu(baslik);
  if (coz)
    icerik.push({ id: 'cozucu', tone: 'is-ok', icon: HelpCircle, t: 'Sesli soru çözücü', s: `${coz.soru ? coz.soru + ' soru · ' : ''}kaynak gösteren sesli çözüm · derse girmeden önce de, sonra da`, url: coz.url, k: coz.soru ? `${coz.soru} soru` : 'sesli çözüm' });
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
      icerik.push({ id: b.id, tone, icon: ic, t: b.ad, s: n > 0 ? `${n} ${a}` : a, url: `${pathFor('ders_detay', key)}?b=${b.id}`, k: n > 0 ? `${n} ${a.split(' · ')[0].split(' ve ')[0]}` : 'örnek soru' });
    }
    if (paket.spotlar.some((x) => x.adim)) icerik.push({ id: 'pdf', tone: 'is-c', icon: Download, t: 'Ders PDF\'i', s: 'slayt sırasıyla anlatım + her adımın özeti · slayt boyutunda', url: `${pathFor('ders_detay', key)}?b=pdf`, k: 'anlatım + özet' });
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

          <DersIstatV15 dersKey={key} desteId={desteId} cozucuUrl={coz?.url} cikmisN={cikmis.length} miniN={paket?.quiz.length || 0}
            acik={grupAcik.istat ?? false} onToggle={(a) => grupYaz('istat', a)} />

          <section aria-labelledby="dd15-ic-h">
            <h2 id="dd15-ic-h" className="v15-h2 dd15-h">Bu dersin içerikleri</h2>
            {/* Gruplu, açılır-kapanır ızgara: Dinle ve çalış · Soru çöz · Bilgi kartları (açık/kapalı tercihi cihazda) */}
            {ICERIK_GRUP.map((g) => {
              const L = g.idler.map((id) => icerik.find((x) => x.id === id)).filter(Boolean) as typeof icerik;
              if (!L.length) return null;
              const acik = grupAcik[g.id] ?? g.varsayilan;
              return (
                <details key={g.id} className="dd15-grup v15-card" open={acik} onToggle={(e) => grupYaz(g.id, (e.currentTarget as HTMLDetailsElement).open)}>
                  <summary>
                    <b>{g.ad}</b>
                    <span className="dd15-grup-on" aria-hidden>{L.map((x) => <span key={x.id} className={`v15-tile ${x.tone}`} title={x.t}><x.icon /></span>)}</span>
                    <span className="v15-cap">{L.length} içerik</span>
                    <ChevronDown className="dd15-grup-ok" aria-hidden />
                  </summary>
                  <ul className="dd15-izgara" role="list">
                    {L.map((x) => (
                      <li key={x.id}>
                        <a className="dd15-kutu" href={x.url} title={x.s} onClick={linkClick(() => navigateTo(x.url))}>
                          <span className={`v15-tile ${x.tone}`}><x.icon aria-hidden /></span>
                          <span className="dd15-kutu-t"><b>{x.t}</b><span>{x.k || x.s}</span></span>
                        </a>
                      </li>
                    ))}
                  </ul>
                </details>
              );
            })}
            {/* Topluluk: bu dersin yorum kanalı (V2 ayrı ders sayılmaz) */}
            <a className="dd15-yorum v15-card" href={`/topluluk?yorum=ders:${key.replace(/-v\d+$/, '')}`} onClick={linkClick(() => navigateTo(`/topluluk?yorum=ders:${key.replace(/-v\d+$/, '')}`))}>
              <MessageCircle aria-hidden /><span><b>Yorumlar</b> · bu ders hakkında arkadaşlarınla yazış</span><ChevronRight className="v15-chev" aria-hidden />
            </a>
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
