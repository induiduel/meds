/**
 * Başarımlar (/basarimlar?s=hedef|basarim|atp|gecmis|kural): puan, ATP, seri ve sıralama özeti; günlük/haftalık/kurul
 * hedefleri (seviye basamakları), kalıcı başarımlar, ATP ile kilit açma, ödül geçmişi ve kuralların tam listesi.
 * Kurallar sunucudaki tanımdan gelir (src/data/basarim/tanim.json) — liste burada olduğu gibi gösterilir.
 */
import React, { useEffect, useMemo, useState } from 'react';
import { createPortal } from 'react-dom';
import { Award, CalendarClock, Crown, ShieldCheck, Check, ChevronDown, Flame, History, Lock, ScrollText, Share2, ShoppingBag, Sparkles, Target, Trophy, X } from 'lucide-react';
import { KILIT_TUR_AD, sureYaz, olcuYaz, profilKaydet, satinAl, sayi, sec, useBasarim, yenile, type BasarimT, type HedefT, type KilitT } from '../../services/basarimIstemci';
import { navigateTo, pathFor } from '../../router';
import { AtpIkon, Basamaklar, Ikon, OdulCip } from './ortak';
import { DonemKurulSecici } from './BasarimKatmani';
import '../../styles/basarim.css';
import { useTamKatman } from '../../utils/tamKatman';

type Sekme = 'hedef' | 'basarim' | 'atp' | 'gecmis' | 'kural';
const SEKMELER: { id: Sekme; ad: string; ikon: React.ComponentType<{ 'aria-hidden'?: boolean }> }[] = [
  { id: 'hedef', ad: 'Hedefler', ikon: Target },
  { id: 'basarim', ad: 'Başarımlar', ikon: Award },
  { id: 'atp', ad: 'ATP ve kilitler', ikon: ShoppingBag },
  { id: 'gecmis', ad: 'Geçmiş', ikon: History },
  { id: 'kural', ad: 'Kurallar', ikon: ScrollText },
];
const urlSekme = (): Sekme => { try { const s = new URLSearchParams(location.search).get('s'); return SEKMELER.some((x) => x.id === s) ? (s as Sekme) : 'hedef'; } catch { return 'hedef'; } };

const kalanYaz = (son: string, donem: HedefT['donem']) => {
  if (donem === 'gun') {
    const d = new Date(); const dk = 24 * 60 - (d.getHours() * 60 + d.getMinutes());
    return dk > 60 ? `Gün bitimine ${Math.floor(dk / 60)} sa ${dk % 60} dk` : `Gün bitimine ${dk} dk`;
  }
  const g = Math.round((Date.parse(`${son}T23:59:59`) - Date.now()) / 86400000);
  return g <= 0 ? 'Son gün' : `${g} gün kaldı`;
};
const tarihYaz = (iso: string) => new Date(iso).toLocaleString('tr-TR', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' });

export default function BasarimView() {
  const { durum, tanim, hata, uid } = useBasarim();
  const [sekme, setSekme0] = useState<Sekme>(urlSekme);
  const [profilAc, setProfilAc] = useState(false);
  useEffect(() => { document.title = 'Başarımlar · MeDSor'; void yenile(true); }, []);
  const setSekme = (s: Sekme) => {
    setSekme0(s);
    try { const u = new URL(location.href); u.searchParams.set('s', s); history.replaceState(history.state, '', u); } catch { /* */ }
  };

  if (!uid) return <div className="bs"><p className="bs-bos">Başarımlarını görmek için giriş yap.</p></div>;
  if (!durum) return <div className="bs"><div className="bs-iskelet" aria-busy="true" aria-label="Yükleniyor" />{hata && <p className="bs-bos">{hata}</p>}</div>;

  const atpOran = durum.atp.tavan == null ? 0 : Math.min(1, durum.atp.bugunAlinan / Math.max(1, durum.atp.tavan));
  return (
    <div className="bs">
      <header className="bs-bas">
        <div className="bs-bas-ust">
          <div>
            <h1>Başarımlar</h1>
            <p className="bs-bas-profil">
              {durum.ozel && <span className="bs-ozel-unvan" title={durum.ozel.muaf ? 'Yönetici tarafından verildi; günlük sınırlar ve içerik kilitleri sana uygulanmaz' : 'Yönetici tarafından verildi'}><Crown aria-hidden /> {durum.ozel.unvan}</span>}
              {durum.kidem && <span className="bs-kidem-cip" title={`Günlük ATP sınırı: ${durum.atp.tavan ?? 'sınırsız'}`}>{durum.kidem.no}. kıdem · {durum.kidem.ad}</span>}
              {durum.profil.donem}. Dönem · {durum.profil.kurul}. Kurul
              <button type="button" className="bs-baglanti" onClick={() => setProfilAc((x) => !x)} aria-expanded={profilAc}>Değiştir</button>
            </p>
          </div>
          <button type="button" className="bs-sira-dug" onClick={() => navigateTo(pathFor('leaderboard'))}><Trophy aria-hidden /> Sıralama</button>
        </div>
        {profilAc && (
          <div className="bs-profil-duzen">
            <DonemKurulSecici ilk={durum.profil} kaydetYazi="Kaydet" onKaydet={async (d, k) => { await profilKaydet(d, k); setProfilAc(false); }} />
          </div>
        )}
        <div className="bs-ozet">
          <div className="bs-ozet-k is-puan">
            <span className="bs-ozet-e">Puan</span>
            <b className="bs-ozet-s">{sayi(durum.puan.toplam)}</b>
            <span className="bs-ozet-a">Bugün +{sayi(durum.puan.bugun)}</span>
          </div>
          <div className="bs-ozet-k is-atp">
            <span className="bs-ozet-e"><AtpIkon boyut={13} canli /> ATP</span>
            <b className="bs-ozet-s">{sayi(durum.atp.bakiye)}<small> mol</small></b>
            <span className="bs-ozet-cubuk" title={durum.atp.tavan == null ? 'Günlük sınır yok' : `Bugün ${durum.atp.bugunAlinan}/${durum.atp.tavan} mol`}><i style={{ width: `${atpOran * 100}%` }} /></span>
            <span className="bs-ozet-a">Bugün {durum.atp.bugunAlinan}{durum.atp.tavan == null ? ' · sınırsız' : `/${durum.atp.tavan}`}{durum.atp.kuyrukta > 0 ? ` · kuyrukta ${sayi(durum.atp.kuyrukta)}` : ''}</span>
          </div>
          <div className="bs-ozet-k is-seri">
            <span className="bs-ozet-e"><Flame aria-hidden /> Seri</span>
            <b className="bs-ozet-s">{durum.seri}<small> gün</small></b>
            <span className="bs-ozet-a">{durum.seri ? 'Yarın da gel, zincir kopmasın' : 'Bugün girişle başla'}</span>
          </div>
          <div className="bs-ozet-k is-sira">
            <span className="bs-ozet-e"><Trophy aria-hidden /> Bu hafta</span>
            <b className="bs-ozet-s">{durum.siralama.hafta.sira ? `${durum.siralama.hafta.sira}.` : '—'}</b>
            <span className="bs-ozet-a">{durum.siralama.hafta.kisi} kişi · kurulda {durum.siralama.kurul.sira ? `${durum.siralama.kurul.sira}.` : '—'}</span>
          </div>
        </div>
      </header>

      <nav className="bs-sekme" role="tablist" aria-label="Başarım bölümleri">
        {SEKMELER.map(({ id, ad, ikon: I }) => (
          <button key={id} role="tab" type="button" aria-selected={sekme === id} className={sekme === id ? 'is-secili' : ''} onClick={() => setSekme(id)}>
            <I aria-hidden /> <span>{ad}</span>
          </button>
        ))}
      </nav>

      {sekme === 'hedef' && <Hedefler />}
      {sekme === 'basarim' && <BasarimListesi />}
      {sekme === 'atp' && <AtpMagaza />}
      {sekme === 'gecmis' && <Gecmis />}
      {sekme === 'kural' && <Kurallar />}
      {hata && <p className="bs-hata" role="status">{hata}</p>}
      {!tanim && null}
    </div>
  );
}

function HedefKart({ h }: { h: HedefT }) {
  const { durum } = useBasarim();
  const d = durum!.hedefler.find((x) => x.id === h.id);
  const deger = d?.deger || 0;
  const alinan = Math.max(d?.alinan || 0, h.seviyeler.filter(([e]) => deger >= e).length);
  const bitti = alinan >= h.seviyeler.length;
  return (
    <article className={`bs-hedef${bitti ? ' is-bitti' : ''}`}>
      <header>
        <span className="bs-hedef-ikon" aria-hidden><Ikon ad={h.ikon} /></span>
        <div className="bs-hedef-ad">
          <h3>{h.ad}</h3>
          <p><b>{olcuYaz(h.olcu, deger)}</b> · {alinan}/{h.seviyeler.length} seviye</p>
        </div>
        {bitti && <span className="bs-rozet-tamam"><Check aria-hidden /> Tamam</span>}
      </header>
      <Basamaklar seviyeler={h.seviyeler} deger={deger} alinan={d?.alinan || 0} olcu={h.olcu} />
    </article>
  );
}

function Hedefler() {
  const { tanim, durum } = useBasarim();
  const grup = (donem: HedefT['donem']) => tanim.hedefler.filter((h) => h.donem === donem);
  const pen = (donem: HedefT['donem']) => durum!.hedefler.find((x) => tanim.hedefler.find((h) => h.id === x.id)?.donem === donem)?.pencere;
  const BOLUM: { donem: HedefT['donem']; ad: string }[] = [
    { donem: 'gun', ad: 'Günlük hedefler' },
    { donem: 'hafta', ad: 'Haftalık hedefler' },
    { donem: 'kurul', ad: `Kurul hedefleri · ${durum!.kurulPencere.ad}` },
  ];
  return (
    <div className="bs-bolumler">
      <p className="bs-aciklama">Her hedefin seviyeleri vardır; alt seviyeler puan, üst seviyeler ATP verir. Ders, gerçekten bitirildiğinde (“Bitirdim” + en az 10 dk etkin çalışma) sayılır.</p>
      {durum!.calisma && durum!.calisma.dersler.length > 0 && (
        <section className="bs-bolum">
          <header className="bs-bolum-bas"><h2>Bu hafta en çok çalıştığın dersler</h2><span className="bs-kalan">Bugün {sureYaz(durum!.calisma.bugun)} · bu hafta {sureYaz(durum!.calisma.hafta)}</span></header>
          <ol className="bs-ders-liste">
            {durum!.calisma.dersler.map((x, i) => (
              <li key={x.id}>
                <span className="bs-ders-no">{i + 1}</span>
                <span className="bs-ders-ad"><b>{x.ad}</b><small>{x.modul}</small></span>
                <span className="bs-ders-cubuk" aria-hidden><i style={{ width: `${(x.sn / Math.max(1, durum!.calisma!.dersler[0].sn)) * 100}%` }} /></span>
                <span className="bs-ders-sn">{sureYaz(x.sn)}</span>
              </li>
            ))}
          </ol>
        </section>
      )}
      {BOLUM.map(({ donem, ad }) => {
        const p = pen(donem);
        return (
          <section key={donem} className="bs-bolum">
            <header className="bs-bolum-bas">
              <h2>{ad}</h2>
              {p && <span className="bs-kalan"><CalendarClock aria-hidden /> {kalanYaz(p.son, donem)}</span>}
            </header>
            <div className="bs-izgara">{grup(donem).map((h) => <HedefKart key={h.id} h={h} />)}</div>
          </section>
        );
      })}
    </div>
  );
}

function BasarimKart({ b }: { b: BasarimT }) {
  const { durum } = useBasarim();
  const [acik, setAcik] = useState(false);
  const [rozet, setRozet] = useState(false);
  const d = durum!.basarimlar.find((x) => x.id === b.id);
  const deger = d?.deger || 0;
  const alinan = Math.max(d?.alinan || 0, b.seviyeler.filter(([e]) => deger >= e).length);
  const sonraki = b.seviyeler[alinan];
  const onceki = alinan ? b.seviyeler[alinan - 1][0] : 0;
  const oran = sonraki ? Math.max(0, Math.min(1, (deger - onceki) / Math.max(1, sonraki[0] - onceki))) : 1;
  const tam = alinan >= b.seviyeler.length;
  return (
    <article className={`bs-bsm${alinan ? ' is-acik' : ''}${tam ? ' is-tam' : ''}`} style={{ '--bs-renk': b.renk || 'var(--color-accent)' } as React.CSSProperties}>
      <button type="button" className="bs-bsm-bas" onClick={() => setAcik((x) => !x)} aria-expanded={acik}>
        <span className="bs-madalya" aria-hidden>
          <svg viewBox="0 0 44 44" className="bs-madalya-halka">
            <circle cx="22" cy="22" r="19" className="bs-mh-iz" />
            <circle cx="22" cy="22" r="19" className="bs-mh-dolu" style={{ strokeDasharray: `${(alinan / b.seviyeler.length) * 119.4} 119.4` }} />
          </svg>
          <span className="bs-madalya-yuz">{alinan ? <Ikon ad={b.ikon} /> : <Lock />}</span>
          {alinan > 0 && <span className="bs-madalya-no">{alinan}</span>}
        </span>
        <span className="bs-bsm-govde">
          <span className="bs-bsm-ad">{b.ad}{b.topluluk && <em className="bs-yalniz-puan">yalnız puan</em>}</span>
          <span className="bs-bsm-acik">{b.aciklama} · <b>{olcuYaz(b.olcu, deger)}</b></span>
          {sonraki ? (
            <span className="bs-bsm-ilerleme">
              <span className="bs-sv-cubuk"><i style={{ width: `${oran * 100}%` }} /></span>
              <span className="bs-bsm-sonraki">{alinan + 1}. seviye: {olcuYaz(b.olcu, sonraki[0])} <OdulCip p={sonraki[1]} a={sonraki[2]} kucuk /></span>
            </span>
          ) : <span className="bs-bsm-sonraki is-tam"><Sparkles aria-hidden /> Tüm seviyeler açıldı</span>}
        </span>
        <ChevronDown className="bs-bsm-ok" aria-hidden />
      </button>
      {acik && <Basamaklar seviyeler={b.seviyeler} deger={deger} alinan={d?.alinan || 0} olcu={b.olcu} renk={b.renk} />}
      {acik && alinan > 0 && <button type="button" className="bs-rozet-gor" onClick={() => setRozet(true)}><Award aria-hidden /> Rozeti gör</button>}
      {rozet && <RozetDetay b={b} seviye={alinan} deger={deger} tarih={durum!.defter.find((o) => o.id === `b:${b.id}:${alinan}`)?.at} onKapat={() => setRozet(false)} />}
    </article>
  );
}

/** Rozet ayrıntısı (tasarım M11 rozetDetay): baklava rozet, seviye, ad, açıklama + değer, kazanma tarihi, Paylaş */
function RozetDetay({ b, seviye, deger, tarih, onKapat }: { b: BasarimT; seviye: number; deger: number; tarih?: string; onKapat: () => void }) {
  const [kopya, setKopya] = useState(false);
  useEffect(() => {
    const k = (e: KeyboardEvent) => { if (e.key === 'Escape') onKapat(); };
    window.addEventListener('keydown', k);
    return () => { window.removeEventListener('keydown', k); };
  }, [onKapat]);
  useTamKatman();
  const paylas = async () => {
    const metin = `MeDSor'da "${b.ad}" rozetinin ${seviye}. seviyesini kazandım.`;
    try { if (navigator.share) await navigator.share({ title: b.ad, text: metin }); else { await navigator.clipboard.writeText(metin); setKopya(true); } } catch { /* vazgeçti */ }
  };
  return createPortal(
    <div className="bs-rd" role="dialog" aria-modal="true" aria-label={`${b.ad} rozeti`} style={{ '--bs-renk': b.renk || 'var(--color-warn)' } as React.CSSProperties}>
      <div className="bs-rd-ust"><button type="button" className="bs-rd-x" onClick={onKapat} aria-label="Kapat"><X aria-hidden /></button></div>
      <div className="bs-rd-ic">
        <span className="bs-rd-rozet" aria-hidden><span><Ikon ad={b.ikon} /></span></span>
        <span className="bs-rd-sv">Seviye {seviye}{seviye >= b.seviyeler.length ? ' · en üst' : ` / ${b.seviyeler.length}`}</span>
        <h2>{b.ad}</h2>
        <p>{b.aciklama}{b.aciklama ? ' · ' : ''}Şu an <b>{olcuYaz(b.olcu, deger)}</b>.</p>
        {tarih && <span className="bs-rd-tarih"><CalendarClock aria-hidden /> {new Date(tarih).toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', year: 'numeric' })}</span>}
        <button type="button" className="bs-rd-btn" onClick={paylas}><Share2 aria-hidden /> {kopya ? 'Kopyalandı' : 'Paylaş'}</button>
        <button type="button" className="bs-rd-tum" onClick={onKapat}>TÜM ROZETLER →</button>
      </div>
    </div>,
    document.body,
  );
}

function BasarimListesi() {
  const { tanim, durum } = useBasarim();
  const calisma = tanim.basarimlar.filter((b) => !b.topluluk);
  const topluluk = tanim.basarimlar.filter((b) => b.topluluk);
  const acik = durum!.basarimlar.reduce((a, x) => a + x.alinan, 0);
  const toplam = tanim.basarimlar.reduce((a, b) => a + b.seviyeler.length, 0);
  return (
    <div className="bs-bolumler">
      <p className="bs-aciklama">Başarımlar tüm kurullar boyunca birikir ve sıfırlanmaz. Açılan seviye: <b>{acik}/{toplam}</b>.</p>
      <section className="bs-bolum">
        <header className="bs-bolum-bas"><h2>Çalışma başarımları</h2><span className="bs-kalan">Üst seviyeler ATP verir</span></header>
        <div className="bs-bsm-liste">{calisma.map((b) => <BasarimKart key={b.id} b={b} />)}</div>
      </section>
      <section className="bs-bolum">
        <header className="bs-bolum-bas"><h2>Topluluk başarımları</h2><span className="bs-kalan">Yalnız puan verir</span></header>
        <div className="bs-bsm-liste">{topluluk.map((b) => <BasarimKart key={b.id} b={b} />)}</div>
      </section>
    </div>
  );
}

function AtpMagaza() {
  const { tanim, durum } = useBasarim();
  const [onay, setOnay] = useState<KilitT | null>(null);
  const [bekle, setBekle] = useState(false);
  const [ileti, setIleti] = useState('');
  const d = durum!;
  const kidemNo = d.kidem?.no || 1;
  const kidemler = tanim.kidemler || [];
  const turler = useMemo(
    () => (['cerceve', 'renk', 'efekt', 'esya', 'icerik'] as const).map((t) => ({ t, liste: tanim.kilitler.filter((k) => k.tur === t && (!k.eski || d.kilit[k.id])) })).filter((x) => x.liste.length),
    [tanim, d.kilit],
  );
  const eskiUnvan = tanim.kilitler.filter((k) => k.tur === 'unvan' && k.eski && d.kilit[k.id]);
  const al = async (k: KilitT) => {
    setBekle(true); setIleti('');
    try { await satinAl(k.id); setIleti(k.kidemAcar ? `Tebrikler, artık ${kidemler.find((x) => x.no === k.kidem)?.ad || ''} kıdemindesin.` : k.tur === 'esya' ? `${k.ad} çantana eklendi.` : `${k.ad} açıldı.`); setOnay(null); } catch (e: any) { setIleti(e?.message || 'Açılamadı'); } finally { setBekle(false); }
  };

  const Urun = ({ k }: { k: KilitT }) => {
    const t = k.tur;
    const adet = t === 'esya' ? d.esya?.[k.id] || 0 : 0;
    const sahip = t !== 'esya' && !!d.kilit[k.id];
    const secili = t !== 'icerik' && t !== 'esya' && (d.secili as any)[t] === k.id;
    const yetmez = d.atp.bakiye < k.fiyat;
    const kidemGerek = t === 'unvan' && k.kidem ? (k.kidemAcar ? k.kidem - 1 : k.kidem) : 0;
    const kidemKilit = kidemGerek > kidemNo;
    return (
      <article className={`bs-urun is-${t}${sahip ? ' is-sahip' : ''}${!k.etkin && !sahip ? ' is-yakinda' : ''}${k.kidemAcar ? ' is-kidem' : ''}${kidemKilit ? ' is-kidemkilit' : ''}`} style={k.renk ? ({ '--bs-renk': k.renk } as React.CSSProperties) : undefined}>
        <span className="bs-urun-gorsel" aria-hidden>
          {t === 'cerceve' ? <span className={`bs-cerceve-ornek ${k.id}`} /> : t === 'unvan' ? (k.kidemAcar ? <Crown /> : <Award />) : t === 'efekt' ? <Sparkles /> : t === 'renk' ? <span className={`bs-renk-ornek ${k.id}`}>Aa</span> : t === 'esya' ? <ShieldCheck /> : <Lock />}
        </span>
        <span className="bs-urun-ad">{k.ad.replace(/^(Unvan|Kutlama efekti):\s*/, '')}</span>
        {k.kidemAcar && <span className="bs-urun-not">Kıdemi yükseltir: günde {kidemler.find((x) => x.no === k.kidem)?.tavan} mol</span>}
        {k.aciklama && <span className="bs-urun-not">{k.aciklama}</span>}
        {t === 'esya' && adet > 0 && <span className="bs-urun-not is-adet">Çantanda: {adet}</span>}
        <span className="bs-urun-fiyat"><AtpIkon boyut={11} /> {sayi(k.fiyat)} mol</span>
        {!k.etkin && !sahip ? <span className="bs-urun-dug is-pasif">Yakında</span>
          : sahip ? (t === 'icerik' ? <span className="bs-urun-dug is-pasif"><Check aria-hidden /> Açık</span>
            : <button type="button" className={`bs-urun-dug${secili ? ' is-secili' : ''}`} onClick={() => void sec(t as any, secili ? null : k.id)}>{secili ? <><Check aria-hidden /> Kullanılıyor</> : 'Kullan'}</button>)
          : kidemKilit ? <span className="bs-urun-dug is-pasif"><Lock aria-hidden /> {kidemler.find((x) => x.no === kidemGerek)?.ad} kıdemi gerekli</span>
          : <button type="button" className="bs-urun-dug is-al" disabled={yetmez} onClick={() => setOnay(k)} title={yetmez ? `${k.fiyat - d.atp.bakiye} mol eksik` : undefined}>{yetmez ? `${sayi(k.fiyat - d.atp.bakiye)} mol eksik` : t === 'esya' ? 'Satın al' : k.kidemAcar ? 'Kıdem atla' : 'Kilidi aç'}</button>}
      </article>
    );
  };

  return (
    <div className="bs-bolumler">
      <section className="bs-atp-bilgi">
        <div className="bs-atp-bakiye">
          <AtpIkon boyut={30} canli />
          <div><b>{sayi(d.atp.bakiye)} mol</b><span>harcanabilir ATP</span></div>
        </div>
        <ul className="bs-atp-kural">
          <li><b>Nasıl kazanılır?</b> Hedeflerin ve çalışma başarımlarının üst seviyeleri, haftalık sıralamada ilk 5 ({tanim.atp.haftalikSiralama.join(' / ')} mol), haftanın en çok çalışanı ({(tanim.atp as any).calismaHaftaBirinci || 0} mol) ve kurul sonu ilk 5 ({tanim.atp.kurulSiralama.join(' / ')} mol).</li>
          <li><b>Günlük sınır kıdemine bağlı:</b> {d.atp.tavan == null ? 'Senin için sınır yok.' : `${d.kidem?.ad || 'Çömez'} kıdeminde günde en çok ${d.atp.tavan} mol; fazlası kuyruğa girer, sonraki günlerde hesaba geçer.`} Bugün: {d.atp.bugunAlinan}{d.atp.tavan != null ? `/${d.atp.tavan}` : ''}{d.atp.kuyrukta ? `, kuyrukta ${sayi(d.atp.kuyrukta)} mol` : ''}.</li>
          <li><b>Ne kazandırmaz?</b> Soru ekleme, yorum, beğeni, katkı ve hata bildirimi yalnız puan verir.</li>
        </ul>
      </section>
      {ileti && <p className="bs-ileti" role="status">{ileti}</p>}

      {kidemler.length > 0 && (
        <section className="bs-bolum">
          <header className="bs-bolum-bas"><h2>{KILIT_TUR_AD.unvan}</h2><span className="bs-kalan">Kıdem unvanı bir üst kıdeme geçirir; diğer unvanlar o kıdemde açılır</span></header>
          <ol className="bs-kidem-merdiven">
            {kidemler.map((kd) => {
              const unvanlar = tanim.kilitler.filter((k) => k.tur === 'unvan' && !k.eski && k.kidem === kd.no).sort((a, b) => Number(!!b.kidemAcar) - Number(!!a.kidemAcar));
              const durumu = kd.no < kidemNo ? 'gecti' : kd.no === kidemNo ? 'simdi' : kd.no === kidemNo + 1 ? 'sirada' : 'kilitli';
              return (
                <li key={kd.no} className={`bs-kidem is-${durumu}`}>
                  <header>
                    <span className="bs-kidem-no">{kd.no}</span>
                    <div><h3>{kd.ad}{durumu === 'simdi' && <em>Sen buradasın</em>}</h3><p>{kd.aciklama} · günde en çok <b>{kd.tavan} mol</b> ATP</p></div>
                  </header>
                  {unvanlar.length > 0 && <div className="bs-magaza">{unvanlar.map((k) => <Urun key={k.id} k={k} />)}</div>}
                </li>
              );
            })}
          </ol>
          {eskiUnvan.length > 0 && <div className="bs-magaza">{eskiUnvan.map((k) => <Urun key={k.id} k={k} />)}</div>}
        </section>
      )}

      {turler.map(({ t, liste }) => (
        <section key={t} className="bs-bolum">
          <header className="bs-bolum-bas"><h2>{KILIT_TUR_AD[t]}</h2>{t === 'icerik' && <span className="bs-kalan">Bir kez açılır, kalıcıdır</span>}{t === 'esya' && <span className="bs-kalan">Tükenir, yeniden alınabilir</span>}</header>
          <div className="bs-magaza">{liste.map((k) => <Urun key={k.id} k={k} />)}</div>
        </section>
      ))}
      {onay && (
        <div className="bs-onay" role="dialog" aria-modal="true" aria-labelledby="bs-onay-b">
          <div className="bs-onay-kart">
            <h3 id="bs-onay-b">{onay.ad}</h3>
            <p><b>{sayi(onay.fiyat)} mol ATP</b> harcanacak. Kalan: {sayi(d.atp.bakiye - onay.fiyat)} mol.{onay.kidemAcar ? ` Kıdemin ${kidemler.find((x) => x.no === onay.kidem)?.ad} olur; günlük ATP sınırın ${kidemler.find((x) => x.no === onay.kidem)?.tavan} mole çıkar.` : ''} Bu işlem geri alınamaz.</p>
            <div className="bs-onay-dug">
              <button type="button" onClick={() => setOnay(null)} disabled={bekle}>Vazgeç</button>
              <button type="button" className="is-al" onClick={() => void al(onay)} disabled={bekle}>{bekle ? 'Açılıyor…' : onay.tur === 'esya' ? 'Satın al' : 'Kilidi aç'}</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function Gecmis() {
  const { durum } = useBasarim();
  const liste = durum!.defter;
  if (!liste.length) return <p className="bs-bos">Henüz ödül yok. Bugünün ilk hedefi 1 saat çalışma.</p>;
  return (
    <ol className="bs-defter">
      {liste.map((o) => (
        <li key={o.id} className={`is-${o.t}${o.ust ? ' is-ust' : ''}${o.geriAlindi ? ' is-geri' : ''}`}>
          <span className="bs-defter-ikon" aria-hidden>{o.t === 'siralama' ? <Trophy /> : o.t === 'harcama' ? <ShoppingBag /> : o.t === 'basarim' ? <Award /> : o.t === 'baslangic' ? <Sparkles /> : o.t === 'yonetici' ? <Crown /> : <Target />}</span>
          <span className="bs-defter-ad">{o.ad}<time dateTime={o.at}>{tarihYaz(o.at)}</time></span>
          <OdulCip p={o.p} a={o.a} kucuk />
        </li>
      ))}
    </ol>
  );
}

function Kurallar() {
  const { tanim } = useBasarim();
  const t = tanim.taban;
  return (
    <div className="bs-bolumler bs-kurallar">
      <section className="bs-bolum">
        <h2>Puan · her gün kendiliğinden</h2>
        <table className="bs-tablo">
          <tbody>
            <tr><th scope="row">Çözülen her soru</th><td>{t.soruBasina} puan (günde en çok {sayi(t.soruGunlukTavan)} soru)</td></tr>
            <tr><th scope="row">Her 10 dk etkin çalışma</th><td>{t.onDakikaBasina} puan (günde en çok {Math.round(t.calismaGunlukTavanSn / 3600)} sa)</td></tr>
            <tr><th scope="row">Gerçekten bitirilen ders</th><td>{t.bitirilenBasina} puan (günde en çok {t.bitirilenGunlukTavan}; en az {Math.round(t.bitirmeAsgariSn / 60)} dk çalışılmış olmalı)</td></tr>
          </tbody>
        </table>
      </section>
      <section className="bs-bolum">
        <h2>Puan · topluluk (ATP vermez)</h2>
        <table className="bs-tablo">
          <tbody>{tanim.eylemler.map((e) => <tr key={e.id}><th scope="row">{e.ad}</th><td>{e.p} puan (günde en çok {e.gunlukTavan} kez)</td></tr>)}</tbody>
        </table>
      </section>
      <section className="bs-bolum">
        <h2>Tüm hedefler</h2>
        <table className="bs-tablo is-seviye">
          <thead><tr><th scope="col">Hedef</th>{[1, 2, 3, 4, 5].map((i) => <th key={i} scope="col">{i}. seviye</th>)}</tr></thead>
          <tbody>{tanim.hedefler.map((h) => <SeviyeSatir key={h.id} ad={`${h.ad}`} olcu={h.olcu} sv={h.seviyeler} />)}</tbody>
        </table>
      </section>
      <section className="bs-bolum">
        <h2>Tüm başarımlar</h2>
        <table className="bs-tablo is-seviye">
          <thead><tr><th scope="col">Başarım</th>{[1, 2, 3, 4, 5].map((i) => <th key={i} scope="col">{i}. seviye</th>)}</tr></thead>
          <tbody>{tanim.basarimlar.map((b) => <SeviyeSatir key={b.id} ad={b.ad} olcu={b.olcu} sv={b.seviyeler} />)}</tbody>
        </table>
      </section>
      <section className="bs-bolum">
        <h2>Sıralama ödülleri (dönem içinde)</h2>
        <table className="bs-tablo">
          <tbody>
            <tr><th scope="row">Haftalık ilk 5</th><td>{tanim.atp.haftalikSiralama.map((a, i) => `${i + 1}. ${a} mol`).join(' · ')} (en az {sayi(tanim.atp.siralamaEsikPuan.hafta)} haftalık puan)</td></tr>
            <tr><th scope="row">Kurul sonu ilk 5</th><td>{tanim.atp.kurulSiralama.map((a, i) => `${i + 1}. ${a} mol`).join(' · ')} (en az {sayi(tanim.atp.siralamaEsikPuan.kurul)} kurul puanı)</td></tr>
            <tr><th scope="row">Başlangıç</th><td>Her öğrenciye {tanim.atp.baslangic} mol</td></tr>
            <tr><th scope="row">Günlük ATP sınırı</th><td>{tanim.atp.gunlukTavan} mol; fazlası kuyruğa alınır</td></tr>
          </tbody>
        </table>
      </section>
    </div>
  );
}
function SeviyeSatir({ ad, olcu, sv }: { ad: string; olcu: string; sv: [number, number, number][] }) {
  return (
    <tr>
      <th scope="row">{ad}</th>
      {[0, 1, 2, 3, 4].map((i) => <td key={i}>{sv[i] ? <><span className="bs-tablo-esik">{olcuYaz(olcu, sv[i][0])}</span><OdulCip p={sv[i][1]} a={sv[i][2]} kucuk /></> : '—'}</td>)}
    </tr>
  );
}
