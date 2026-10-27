/**
 * Bitirdiklerim (/bitirdiklerim?m=sesli|ogren|cozucu|onem|kamp): beş modülde ders → konu kontrol listesi.
 * Her konu: bitti işareti (dokunarak), harcanan etkin süre, çözülen soru, tekrar turu; "Aç" / "Tekrar et".
 * Her ders ve modül için biten/kalan, toplam süre, soru ve ortalama hıza göre tahmini kalan süre.
 * Veri: services/calismaTakip (süre, soru, durum) + bitirdiklerimVeri (konu listeleri). Stil: styles/takip.css (.bd-*).
 */
import React, { useEffect, useMemo, useState } from 'react';
import { BookOpen, ChevronDown, Tent, Headphones, ListChecks, MessageCircleQuestion, Play, RotateCcw, Search, Star, Target, ChevronRight, X, MoreHorizontal, Undo2 } from 'lucide-react';
import {
  MODUL_AD, bittiMi, sesHizi, grupOzeti, hizHesapla, sureYaz, tekrarBasla, useIzlemeHizi, useTakip, type Hiz, type TakipModul,
} from '../../services/calismaTakip';
import IzlemeHizi from './IzlemeHizi';
import { ELEME_AD, elemeAnahtari, elemeYaz, konuElemesi, useEleme, type ElemeTur } from '../../services/konuEleme';
import { KonuIsaret, KonuSureEtiketi } from './KonuTakip';
import { MODUL_YUKLE, type BdDers, type BdKonu } from './bitirdiklerimVeri';
import { navigateTo, pathFor } from '../../router';
import '../../styles/takip.css';
import '../../styles/v15/bitir.css';
import { useAppearance } from '../../utils/appearance';
import { useV15Baslik } from '../v15/baslik';

const MODULLER: { id: TakipModul; ikon: React.ComponentType<{ 'aria-hidden'?: boolean }> }[] = [
  { id: 'sesli', ikon: Headphones },
  { id: 'ogren', ikon: BookOpen },
  { id: 'cozucu', ikon: MessageCircleQuestion },
  { id: 'onem', ikon: Star },
  { id: 'kamp', ikon: Tent },
];
const MODUL_KISA: Record<TakipModul, string> = { sesli: 'Sesli ders', ogren: 'Etkileşimli', cozucu: 'Soru çözücü', onem: 'En önemliler', kamp: 'Kurul kampı' };
type Suzgec = 'tum' | 'kalan' | 'biten' | 'tekrar' | 'elenen';
const SUZGEC_AD: Record<Suzgec, string> = { tum: 'Tümü', kalan: 'Kalanlar', biten: 'Bitenler', tekrar: 'Tekrarda', elenen: 'Hesap dışı' };

const sayi = (n: number) => n.toLocaleString('tr-TR');
const katla = (s: string) => s.toLocaleLowerCase('tr-TR').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ı/g, 'i');
const urlModul = (): TakipModul => {
  try {
    const m = new URLSearchParams(location.search).get('m');
    return MODULLER.some((x) => x.id === m) ? (m as TakipModul) : 'sesli';
  } catch { return 'sesli'; }
};

type Durum = { yuk: true } | { hata: true } | { veri: BdDers[] };

export default function BitirdiklerimView() {
  const [modul, setModul0] = useState<TakipModul>(urlModul);
  const [durumlar, setDurumlar] = useState<Partial<Record<TakipModul, Durum>>>({});
  const [ara, setAra] = useState('');
  const [suzgec, setSuzgec] = useState<Suzgec>('tum');
  const [acik, setAcik] = useState<Record<string, boolean>>({});
  const takip = useTakip();
  const izHiz = useIzlemeHizi();
  const eleme = useEleme();
  const v15 = !!useAppearance().v15;

  useEffect(() => { document.title = 'Bitirdiklerim · MeDSor'; }, []);
  useEffect(() => {
    let canli = true;
    for (const { id } of MODULLER) {
      setDurumlar((d) => ({ ...d, [id]: { yuk: true } }));
      MODUL_YUKLE[id]().then(
        (veri) => canli && setDurumlar((d) => ({ ...d, [id]: { veri } })),
        () => canli && setDurumlar((d) => ({ ...d, [id]: { hata: true } })),
      );
    }
    return () => { canli = false; };
  }, []);

  const setModul = (m: TakipModul) => {
    setModul0(m);
    setAcik({});
    try {
      const u = new URL(location.href);
      u.searchParams.set('m', m);
      history.replaceState(history.state, '', u.pathname + u.search + u.hash);
    } catch { /* yok */ }
  };

  // Her modülün hızı ve özeti (sekme sayıları dahil)
  const ozetler = useMemo(() => {
    const r: Partial<Record<TakipModul, { hiz: Hiz; dersler: { d: BdDers; o: ReturnType<typeof grupOzeti> }[]; genel: ReturnType<typeof grupOzeti> }>> = {};
    for (const { id } of MODULLER) {
      const dz = durumlar[id];
      if (!dz || !('veri' in dz)) continue;
      // hesaba girenler: çalışmayacağım / sorusuz düşer; başka yerden çalışılan bitmiş sayılır (süresi ölçülmediği için hıza girmez)
      const hesap = (L: BdKonu[]) => L.flatMap((k) => {
        const e = konuElemesi(eleme, id, k);
        return e === 'calisma' || e === 'sorusuz' ? [] : [e === 'baska' ? { ...k, turetilen: true } : k];
      });
      const tum = hesap(dz.veri.flatMap((d) => d.konular));
      const hiz = hizHesapla(id, tum, takip);
      r[id] = { hiz, dersler: dz.veri.map((d) => ({ d, o: grupOzeti(id, hesap(d.konular), hiz, takip) })), genel: grupOzeti(id, tum, hiz, takip) };
    }
    return r;
  }, [durumlar, takip, izHiz, eleme]);

  const dz = durumlar[modul];
  const oz = ozetler[modul];
  const q = katla(ara.trim());

  const konuDurumu = (k: BdKonu) => {
    const kayit = takip.k[`${modul}:${k.id}`];
    const elendi = konuElemesi(eleme, modul, k);
    const disari = elendi === 'calisma' || elendi === 'sorusuz';
    return { kayit, elendi, disari, bitti: !disari && bittiMi(kayit, k.turetilen || elendi === 'baska'), tekrar: kayit?.durum === 'tekrar' };
  };
  const elemeSec = (k: BdKonu, tur: ElemeTur | null) => {
    const once = konuElemesi(eleme, modul, k);
    if (once) elemeYaz(elemeAnahtari(modul, k, once), null);
    if (tur) elemeYaz(elemeAnahtari(modul, k, tur), tur);
  };
  // sıradaki: yarım kalan derste (yoksa ilk derste) bitmemiş ilk konu
  const siradaki = useMemo(() => {
    if (!oz) return null;
    const L = [...oz.dersler.filter(({ o }) => o.biten > 0 && o.biten < o.toplam), ...oz.dersler];
    for (const { d } of L) { const k = d.konular.find((x) => { const z = konuDurumu(x); return !z.bitti && !z.disari; }); if (k) return { d, k }; }
    return null;
  }, [oz, modul, eleme]); // eslint-disable-line react-hooks/exhaustive-deps
  const gorunur = (k: BdKonu) => {
    if (q && !katla(`${k.no ?? ''} ${k.ad} ${k.alt || ''}`).includes(q)) return false;
    if (suzgec === 'tum') return true;
    const s = konuDurumu(k);
    return suzgec === 'elenen' ? !!s.elendi : suzgec === 'biten' ? s.bitti : suzgec === 'kalan' ? !s.bitti && !s.disari : s.tekrar;
  };
  // varsayılan açık ders: yarım kalanlar; hiç yoksa ilki
  const varsayilanAcik = (d: BdDers, o: ReturnType<typeof grupOzeti>, i: number) =>
    (o.biten > 0 && o.biten < o.toplam) || o.tekrarda > 0 || (i === 0 && !(oz?.dersler.some((x) => x.o.biten > 0 && x.o.biten < x.o.toplam)));

  return (
    <div className={`bd${v15 ? ' bd15' : ''}`}>
      {v15 && <V15Bas modul={modul} />}
      {!v15 && <>
      <header className="bd-bas">
        <span className="bd-ic" aria-hidden><ListChecks /></span>
        <div>
          <h1>Bitirdiklerim</h1>
          <p>Hangi konuları bitirdiğini, ne kadar çalıştığını ve geriye ne kaldığını tek yerden takip et.</p>
        </div>
      </header>

      <ol className="sp-nasil-kullan" aria-label="Nasıl kullanılır">
        <li><span>1</span><div><b>Çalışma türünü seç</b><small>Sesli ders, etkileşimli ders, soru çözücü…</small></div></li>
        <li><span>2</span><div><b>Bitirdiğin konuyu işaretle</b><small>Soldaki daireye dokun. Başka yerden çalıştıysan, çalışmayacaksan ya da sınavda sorusu yoksa ⋯ düğmesini kullan.</small></div></li>
        <li><span>3</span><div><b>Sıradakine geç</b><small>"Devam et" bitmemiş ilk konuyu açar.</small></div></li>
      </ol>

      <a className="bd-plan-bag" href={pathFor('sinav_plani')} onClick={(e) => { if (e.button || e.metaKey || e.ctrlKey) return; e.preventDefault(); navigateTo(pathFor('sinav_plani')); }}>
        <Target aria-hidden /> <span>Sınav planı: en az 60 için gün gün yol haritası</span> <ChevronRight aria-hidden />
      </a>

      <h3 className="sp-h"><span className="sp-h-no">1</span> Hangi çalışmana bakıyorsun?</h3>
      </>}
      <div className="bd-modul" role="tablist" aria-label="Modül">
        {MODULLER.map(({ id, ikon: Ikon }) => {
          const g = ozetler[id]?.genel;
          const kalanSayi = g ? g.toplam - g.biten : 0;
          return (
            <button key={id} type="button" role="tab" aria-selected={modul === id} className={modul === id ? 'is-on' : ''} onClick={() => setModul(id)}>
              <Ikon aria-hidden />
              <span className="bd-modul-ad">{MODUL_AD[id]}</span>
              <span className="bd-modul-kisa" aria-hidden>{MODUL_KISA[id]}</span>
              <span className="bd-modul-n">
                {g ? `${g.biten}/${g.toplam} bitti` : "…"}
                {g && kalanSayi > 0 && <em className="bd-modul-s"> · {sureYaz(g.kalanIcerikSn)}</em>}
              </span>
            </button>
          );
        })}
      </div>

      {!dz || 'yuk' in dz ? (
        <div className="bd-bos" role="status"><span className="bd-spin" aria-hidden /> Konular yükleniyor…</div>
      ) : 'hata' in dz ? (
        <div className="bd-bos"><p>{MODUL_AD[modul]} listesi alınamadı. Bağlantını kontrol edip sayfayı yenile.</p></div>
      ) : !oz || !dz.veri.length ? (
        <div className="bd-bos"><p>{MODUL_AD[modul]} için henüz konu yok.</p></div>
      ) : (
        <>
          {!v15 && <h3 className="sp-h"><span className="sp-h-no">2</span> Durumun</h3>}
          {(modul === 'sesli' || modul === 'onem' || modul === 'cozucu') && <IzlemeHizi />}
          <OzetKartlari genel={oz.genel} hiz={oz.hiz} modul={modul} sirada={siradaki} izHiz={izHiz} />

          {!v15 && <h3 className="sp-h"><span className="sp-h-no">3</span> Konu konu liste</h3>}

          <div className="bd-arac">
            <label className="bd-ara">
              <Search aria-hidden />
              <input type="search" value={ara} onChange={(e) => setAra(e.target.value)} placeholder="Konu ara" aria-label="Konu ara" />
              {ara && <button type="button" onClick={() => setAra('')} aria-label="Aramayı temizle"><X aria-hidden /></button>}
            </label>
            <div className="bd-suz" role="group" aria-label="Duruma göre süz">
              {(Object.keys(SUZGEC_AD) as Suzgec[]).map((s) => {
                const n = s === 'tum' ? oz.genel.toplam : s === 'biten' ? oz.genel.biten : s === 'kalan' ? oz.genel.toplam - oz.genel.biten
                  : s === 'elenen' ? (dz.veri.flatMap((d) => d.konular).filter((k) => konuElemesi(eleme, modul, k)).length) : oz.genel.tekrarda;
                if ((s === 'tekrar' || s === 'elenen') && !n) return null;
                return (
                  <button key={s} type="button" aria-pressed={suzgec === s} className={suzgec === s ? 'is-on' : ''} onClick={() => setSuzgec(s)}>
                    {SUZGEC_AD[s]} <span>{sayi(n)}</span>
                  </button>
                );
              })}
            </div>
          </div>

          <div className="bd-dersler">
            {oz.dersler.map(({ d, o }, i) => {
              const konular = d.konular.filter(gorunur);
              if (!konular.length) return null;
              const ac = q || suzgec !== 'tum' ? true : acik[d.id] ?? varsayilanAcik(d, o, i);
              const yuzde = o.toplam ? Math.round((o.biten / o.toplam) * 100) : 0;
              return (
                <section key={d.id} className={`bd-ders${ac ? ' is-acik' : ''}${o.biten === o.toplam ? ' is-tamam' : ''}`} aria-label={d.ad}>
                  <button type="button" className="bd-ders-bas" aria-expanded={ac} onClick={() => setAcik((a) => ({ ...a, [d.id]: !ac }))}>
                    <span className="bd-ders-ust">
                      <b>{d.ad}</b>
                      <span className="bd-ders-n"><b>{o.biten}</b>/{o.toplam} bitti · %{yuzde}</span>
                      <ChevronDown aria-hidden className="bd-ok" />
                    </span>
                    <span className="bd-cubuk" aria-hidden><i style={{ width: `${yuzde}%` }} /></span>
                    <span className="bd-ders-meta">
                      {o.biten < o.toplam
                        ? <span className="is-kalan">{o.toplam - o.biten} konu kaldı · bitirmesi ~{sureYaz(o.kalanSn)}</span>
                        : <span className="is-tamam">Tamamlandı</span>}
                      {o.sn > 0 && <span>{sureYaz(o.sn)} çalıştın</span>}
                      {o.soru > 0 && <span>{sayi(o.soru)} soru çözdün</span>}
                    </span>
                  </button>
                  {ac && (
                    <ul className="bd-konular">
                      {konular.map((k) => <KonuSatiri key={k.id} modul={modul} k={k} {...konuDurumu(k)} onEleme={(t) => elemeSec(k, t)} />)}
                    </ul>
                  )}
                </section>
              );
            })}
            {!oz.dersler.some(({ d }) => d.konular.some(gorunur)) && (
              <div className="bd-bos"><p>{q ? `“${ara}” ile eşleşen konu yok.` : `${SUZGEC_AD[suzgec]} listesinde konu yok.`}</p></div>
            )}
          </div>
        </>
      )}
    </div>
  );
}

/** v15: başlık üst barda; Sınav planı bağlantısı ve kısa kullanım ipucu tek satırda */
function V15Bas({ modul }: { modul: TakipModul }) {
  useV15Baslik({ baslik: 'Bitirdiklerim', alt: MODUL_AD[modul] });
  return (
    <>
      <h1 className="sr-only">Bitirdiklerim</h1>
      <a className="bd15-plan v15-card" href={pathFor('sinav_plani')} onClick={(e) => { if (e.button || e.metaKey || e.ctrlKey) return; e.preventDefault(); navigateTo(pathFor('sinav_plani')); }}>
        <span className="v15-tile is-a" aria-hidden><Target /></span>
        <span className="bd15-plan-t"><b>Sınav planı</b><span className="v15-cap">En az 60 için gün gün yol haritası</span></span>
        <ChevronRight className="v15-chev" aria-hidden />
      </a>
    </>
  );
}

function OzetKartlari({ genel, hiz, modul, sirada, izHiz }: { genel: ReturnType<typeof grupOzeti>; hiz: Hiz; modul: TakipModul; sirada: { d: BdDers; k: BdKonu } | null; izHiz: number | null }) {
  const yuzde = genel.toplam ? Math.round((genel.biten / genel.toplam) * 100) : 0;
  const kalan = genel.toplam - genel.biten;
  // "Kalan" kutusu ölçülen hızdan bağımsız: kalan ders süresi ÷ seçilen izleme hızı (sesli modüller)
  const x = modul === 'sesli' || modul === 'onem' || modul === 'cozucu' ? (izHiz ?? 1) : 1;
  const xYaz = `${x.toLocaleString('tr-TR', { maximumFractionDigits: 2 })}×`;
  const kalanDers = genel.kalanIcerikSn / x;
  const cumle = !kalan
    ? `${MODUL_AD[modul]} bölümündeki konuların hepsini bitirdin. İstersen tekrar turuna başlayabilirsin.`
    : genel.biten === 0
      ? `${MODUL_AD[modul]} bölümünde henüz bitirdiğin konu yok. Aşağıdaki "Devam et" ile ilk konudan başla.`
      : `${sayi(genel.toplam)} konunun ${sayi(genel.biten)} tanesini bitirdin. Kalan ${sayi(kalan)} konu senin hızınla yaklaşık ${sureYaz(genel.kalanSn)} sürer.`;
  return (
    <section className="bd-ozet2" aria-label="Özet">
      <p className={`sp-hukum ${!kalan ? 'is-iyi' : 'is-orta'}`}>{cumle}</p>
      <div className="sp-iki">
        <div><small>Bitirdiğin</small><b>{sayi(genel.biten)}<span className="bd-ozet-b"> / {sayi(genel.toplam)}</span></b><span className="bd-cubuk" aria-hidden><i style={{ width: `${yuzde}%` }} /></span></div>
        <div className="is-plan"><small>Kalan ders süresi</small><b>{kalan ? sureYaz(kalanDers) : '—'}</b><span>{kalan ? `${sayi(kalan)} konu · ${xYaz} izlersen` : 'Hepsi bitti'}</span></div>
        <div><small>Şimdiye kadar</small><b>{sureYaz(genel.sn)}</b><span>{genel.soru ? `${sayi(genel.soru)} soru çözdün` : 'çalıştın'}</span></div>
      </div>
      {sirada && (
        <div className="bd-sirada">
          <div><small>Sıradaki konu</small><b>{sirada.k.ad}</b><span>{sirada.d.ad}{sirada.k.beklenen > 0 ? ` · ~${sureYaz(sirada.k.beklenen)}` : ''}</span></div>
          <button type="button" className="kt-btn" onClick={sirada.k.ac}><Play aria-hidden /><span>Devam et</span></button>
        </div>
      )}
      <details className="bd-nasil">
        <summary>Bu süreler nasıl hesaplanıyor?</summary>
        <ul>
          <li><b>Çalıştığın süre:</b> yalnız sekme açık ve sen etkileşimdeyken sayılır.{hiz.gunluk ? ` Son 14 günde günde ortalama ${sureYaz(hiz.gunluk)} çalışmışsın (çalıştığın ${hiz.aktifGun} günde ${sureYaz(hiz.aktifGunluk)}).` : ''}</li>
          <li><b>Kalan süre:</b> {hiz.kaynak === 'senin'
            ? `bitirdiğin ${hiz.ornek} konudaki gerçek hızına göre (içerik süresinin %${Math.round(hiz.oran * 100)} kadarı).`
            : `${modul === 'sesli' || modul === 'onem' || modul === 'cozucu' ? `${sesHizi(modul).toLocaleString('tr-TR')}× ses hızına göre; ` : ''}konu bitirdikçe senin hızına uyar.`}
            {kalan ? ` Kalan içeriğin 1× süresi ${sureYaz(genel.kalanIcerikSn)} (tamamı ${sureYaz(genel.toplamIcerikSn)}).` : ''}</li>
          <li><b>Bitti işareti:</b> bazı konular içerik bitince kendiliğinden işaretlenir; sen de dairesine dokunarak işaretleyip kaldırabilirsin.</li>
        </ul>
      </details>
    </section>
  );
}

function KonuSatiri({ modul, k, bitti, tekrar, elendi, disari, onEleme }: { modul: TakipModul; k: BdKonu; bitti: boolean; tekrar: boolean; elendi?: ElemeTur; disari: boolean; onEleme: (t: ElemeTur | null) => void }) {
  const [menu, setMenu] = useState(false);
  const [yukari, setYukari] = useState(false);
  const [genis, setGenis] = useState(300);
  // menü ekranda en çok boş alan olan tarafa açılır (alttaki konular, telefonun alt çubuğu)
  const menuAc = (e: React.MouseEvent<HTMLButtonElement>) => {
    if (menu) { setMenu(false); return; }
    const r = e.currentTarget.getBoundingClientRect();
    const alt = window.innerHeight - r.bottom - 96;
    setYukari(alt < 280 && r.top > alt);
    setGenis(Math.max(200, Math.min(300, r.right - 12))); // sağdan hizalı: sol kenardan taşmasın
    setMenu(true);
  };
  useEffect(() => {
    if (!menu) return;
    const kapat = () => setMenu(false);
    const t = setTimeout(() => document.addEventListener('click', kapat, { once: true }));
    return () => { clearTimeout(t); document.removeEventListener('click', kapat); };
  }, [menu]);
  if (disari) {
    return (
      <li className="bd-konu is-disari">
        <span className="bd-konu-ad is-pasif">
          {k.no != null && k.no !== '' && <span className="bd-no">{k.no}</span>}
          <span className="bd-konu-t"><b>{k.ad}</b><small><span className={`bd-eleme is-${elendi}`}>{ELEME_AD[elendi!]}</span><span>hesaba katılmıyor</span></small></span>
        </span>
        <button type="button" className="kt-btn" onClick={() => onEleme(null)} aria-label={`Hesaba geri kat: ${k.ad}`}><Undo2 aria-hidden /><span>Geri al</span></button>
      </li>
    );
  }
  return (
    <li className={`bd-konu${bitti ? ' is-bitti' : ''}${tekrar ? ' is-tekrar' : ''}${menu ? ' is-menu' : ''}`}>
      <KonuIsaret modul={modul} konu={k.id} ad={k.ad} turetilen={k.turetilen} />
      <button type="button" className="bd-konu-ad" onClick={k.ac} title="Konuyu aç">
        {k.no != null && k.no !== '' && <span className="bd-no">{k.no}</span>}
        <span className="bd-konu-t">
          <b>{k.ad}</b>
          <small>
            {k.alt && <span>{k.alt}</span>}
            {k.beklenen > 0 && <span>Süresi ~{sureYaz(k.beklenen)}</span>}
            {tekrar && <span className="bd-etiket">Tekrarda</span>}
            {elendi === 'baska' && <span className="bd-eleme is-baska">Başka yerden çalıştın</span>}
          </small>
          <KonuSureEtiketi modul={modul} konu={k.id} ekSoru={k.ekSoru} uzun />
        </span>
      </button>
      <span className="bd-menu-kap">
        <button type="button" className="kt-btn bd-menu-btn" aria-haspopup="menu" aria-expanded={menu} onClick={menuAc} aria-label={`Seçenekler: ${k.ad}`} title="Başka yerden çalıştım · Çalışmayacağım · Sınavda sorusu yok">
          <MoreHorizontal aria-hidden />
        </button>
        {menu && (
          <span className={`bd-menu${yukari ? ' is-yukari' : ''}`} role="menu" style={{ width: genis }}>
            {elendi === 'baska'
              ? <button type="button" role="menuitem" onClick={() => onEleme(null)}><b>İşareti kaldır</b><small>Başka yerden çalıştım işaretini geri al</small></button>
              : <button type="button" role="menuitem" onClick={() => onEleme('baska')}><b>Başka yerden çalıştım</b><small>Bitti sayılır, kalan süreden düşer; çalışma hızını etkilemez</small></button>}
            <button type="button" role="menuitem" onClick={() => onEleme('calisma')}><b>Çalışmayacağım</b><small>Sınavda soru gelir ama bu dersi çalışmayacaksın; kalan süreden ve plandan çıkar</small></button>
            <button type="button" role="menuitem" onClick={() => onEleme('sorusuz')}><b>Sınavda sorusu yok</b><small>Bu dersten soru gelmeyecek; süreden ve sınav hesabından tamamen çıkar</small></button>
          </span>
        )}
      </span>
      {bitti ? (
        <button type="button" className="kt-btn is-tekrar" onClick={() => { tekrarBasla(modul, k.id); k.tekrar(); }} aria-label={`Tekrar et: ${k.ad}`}>
          <RotateCcw aria-hidden /><span>Tekrar et</span>
        </button>
      ) : (
        <button type="button" className="kt-btn" onClick={k.ac} aria-label={`Aç: ${k.ad}`}>
          <Play aria-hidden /><span>Aç</span>
        </button>
      )}
    </li>
  );
}
