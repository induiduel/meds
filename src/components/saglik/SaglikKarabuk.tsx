import React, { useMemo, useState } from 'react';
import {
  Ambulance, ArrowLeft, ArrowRight, Baby, Building2, CalendarClock, ChevronDown, ExternalLink, Factory, GitFork, GraduationCap, HardHat, HeartPulse,
  History, Hospital, Landmark, LineChart, MapPin, MapPinned, Search, Skull, Stethoscope, UserRound, Users, Wind,
} from 'lucide-react';
import { Atif, Blok, EkAtif, MaddeAgaci, MiniMetin, OkunurTablo, Rozet, tarihTR } from './SaglikOrtak';
import { ZamanCizgisi } from './SaglikAraclar';
import { seriMaddeleri, useGecmis, type MaddeOge } from './saglikBaglam';
import { kaynaklariTopla, kucukHarf, sayi, type BolumId, type KarabukVeri, type SeriNokta } from './saglikVeri';

/**
 * Karabük bölümü alt sayfalara bölünür (/saglik/karabuk?sayfa=<id>): her sayfa tek konuya odaklanır ve bilgiyi
 * "ad · değer" satırları hâlinde verir (dokununca ayrıntı ya da geçmiş yıllar açılır). Madde görünümünde her blok
 * aynı satırları madde madde yazar. Kaynakça yalnız açık sayfanın kaynaklarını numaralar (karabukSayfaKaynaklari).
 */

export type KarabukSayfaId = 'ozet' | 'kurumlar' | 'ilceler' | 'nufus' | 'gostergeler' | 'cevre' | 'programlar';

export const KARABUK_SAYFALAR: { id: KarabukSayfaId; ad: string; kisa: string; aciklama: string; icon: React.ElementType }[] = [
  { id: 'ozet', ad: 'Kısaca Karabük', kisa: 'Özet', aciklama: 'En önemli sayılar tek bakışta', icon: MapPin },
  { id: 'kurumlar', ad: 'Sağlık kurumları', kisa: 'Kurumlar', aciklama: 'Müdürlükler, TSM, ASM, hastaneler, 112 ve kim kime bağlı', icon: Landmark },
  { id: 'ilceler', ad: 'İlçe ilçe', kisa: 'İlçeler', aciklama: 'Her ilçenin nüfusu ve sağlık kurumları ayrı ayrı', icon: MapPinned },
  { id: 'nufus', ad: 'Nüfus yapısı', kisa: 'Nüfus', aciklama: 'Yaş, cinsiyet, kent–kır ve yıllara göre nüfus', icon: Users },
  { id: 'gostergeler', ad: 'Sağlık göstergeleri', kisa: 'Göstergeler', aciklama: 'Doğum, ölüm ve hizmet göstergeleri; Türkiye ile yan yana', icon: LineChart },
  { id: 'cevre', ad: 'Çevre ve iş sağlığı', kisa: 'Çevre', aciklama: 'Hava kalitesi ölçümleri ve iş kazaları', icon: Factory },
  { id: 'programlar', ad: 'Programlar ve tarihçe', kisa: 'Programlar', aciklama: 'İl sağlık müdürlüğü çalışmaları, kurumların tarihi, tıp fakültesi', icon: CalendarClock },
];

export const karabukSayfa = (id?: string): KarabukSayfaId => (KARABUK_SAYFALAR.some((s) => s.id === id) ? (id as KarabukSayfaId) : 'ozet');

/** Açık alt sayfanın kaynakça kökleri (numaralama bu sırayla) */
export function karabukSayfaKaynaklari(alt: string | undefined, kb: KarabukVeri): string[] {
  const e = kb.envanter;
  const sim = (kb.kurum_sayilari || []).filter((k) => /hava kalitesi/i.test(k.tur));
  switch (karabukSayfa(alt)) {
    case 'ozet': return kaynaklariTopla(
      { kaynak: kb.nufus?.kaynak }, kb.nufus?.yas_65_ustu_orani && { kaynak: kb.nufus.yas_65_ustu_orani.kaynak },
      (kb.kurum_sayilari || []).map((k) => ({ kaynak: k.kaynak })), (e?.ozet || []).map((k) => ({ kaynak: k.kaynak })),
      (kb.gostergeler || []).map((g) => ({ kaynak: g.kaynak })), (kb.cevre || []).slice(0, 1).map((c) => ({ kaynak: c.kaynak })),
    );
    case 'kurumlar': return kaynaklariTopla(e?.kurumlar, (kb.kurum_sayilari || []).filter((k) => !/hava kalitesi/i.test(k.tur)), e?.ozet, kb.hastaneler, kb.birimler);
    case 'ilceler': return kaynaklariTopla({ kaynak: kb.nufus?.kaynak }, kb.nufus?.ilceler, kb.ilceler, e?.ilce_ozeti, e?.kurumlar);
    case 'nufus': return kaynaklariTopla(kb.nufus);
    case 'gostergeler': return kaynaklariTopla(kb.gostergeler);
    case 'cevre': return kaynaklariTopla(kb.cevre, sim, kb.is_sagligi);
    case 'programlar': return kaynaklariTopla(kb.programlar, e?.tarihce, kb.universite);
    default: return [];
  }
}

/* ===============================================================================================================
 * Bilgi satırı: solda ad (+ küçük açıklama), sağda değer (+ Türkiye karşılığı). Ayrıntı ve geçmiş yıllar dokununca.
 * =============================================================================================================== */

export interface SatirOge {
  ad: string;
  /** undefined: değer sütunu yok · null: resmî kaynakta teyit edilemedi */
  deger?: number | string | null;
  birim?: string;
  alt?: string;
  kaynak?: string; konum?: string; ek?: string[];
  seri?: SeriNokta[];
  tr?: { deger?: number | string | null; seri?: SeriNokta[] };
  tanim?: string;
  detay?: MaddeOge[];
  adlar?: string[];
}

const temiz = <T,>(xs: (T | null | undefined | false | '' | 0)[]): T[] => xs.filter(Boolean) as T[];
const sayiSay = (s?: SeriNokta[]) => (s || []).filter((p) => typeof p.deger === 'number').length;
const degerYaz = (v: number | string | null | undefined, birim?: string): string | null => {
  if (v == null || v === '') return null;
  if (typeof v !== 'number') return String(v);
  return birim === '%' ? `%${sayi(v)}` : sayi(v);
};
const benzersiz = (xs: (string | undefined)[]) => [...new Set(xs.filter(Boolean) as string[])];

/** Satır → madde (madde görünümü ve kopyalama) */
export function satirMaddesi(s: SatirOge): MaddeOge {
  const d = degerYaz(s.deger, s.birim);
  const birim = d != null && typeof s.deger === 'number' && s.birim && s.birim !== '%' ? ` ${s.birim}` : '';
  const trD = s.tr ? degerYaz(s.tr.deger, s.birim) : null;
  const deger = s.deger === undefined ? '' : `: ${d ?? 'resmî kaynakta teyit edilemedi'}${birim}`;
  return {
    metin: `**${s.ad}**${deger}${s.alt ? ` (${s.alt})` : ''}${trD ? ` — Türkiye ${trD}${birim}` : ''}`,
    kaynak: s.kaynak, konum: s.konum, ek: s.ek,
    alt: temiz<MaddeOge>([
      s.tanim && `Tanım: ${s.tanim}`,
      ...(s.detay || []),
      s.adlar?.length ? s.adlar.join(', ') : null,
      sayiSay(s.seri) > 1 && { metin: s.tr ? 'Karabük yıllara göre' : 'Yıllara göre', alt: seriMaddeleri(s.seri!, s.birim) },
      s.tr && sayiSay(s.tr.seri) > 1 && { metin: 'Türkiye yıllara göre', alt: seriMaddeleri(s.tr.seri!, s.birim) },
    ]),
  };
}

const Satir: React.FC<{ s: SatirOge }> = ({ s }) => {
  const [acik, setAcik] = useState(false);
  const ac = useGecmis();
  const yilSay = sayiSay(s.seri);
  const d = degerYaz(s.deger, s.birim);
  // Uzun metin değerler (ör. "Metalurji: 1 tesis, 13 baca…") sağ sütuna sığmaz: adın altına yazılır
  const uzun = d != null && typeof s.deger === 'string' && d.length > 18;
  const trD = s.tr ? degerYaz(s.tr.deger, s.birim) : null;
  const yon = typeof s.deger === 'number' && typeof s.tr?.deger === 'number'
    ? (s.deger > s.tr.deger ? 'Türkiye’den yüksek' : s.deger < s.tr.deger ? 'Türkiye’den düşük' : 'Türkiye ile aynı') : null;
  const acilir = !!(s.detay?.length || s.adlar?.length || s.tanim);
  const birimGoster = d != null && typeof s.deger === 'number' && !!s.birim && s.birim !== '%';
  const uzunBirim = birimGoster && s.birim!.length > 6;
  // Dar ekranda değer, Türkiye karşılığı ya da uzun birim varsa adın altına iner (ad sıkışıp satır uzamasın)
  const yigin = uzunBirim || !!trD;
  const gecmisAc = () => ac({
    baslik: s.tr ? `${s.ad} · Karabük ve Türkiye` : s.ad, birim: s.birim,
    seriler: [{ ad: s.tr ? 'Karabük' : s.ad, seri: s.seri! }, ...(s.tr?.seri && sayiSay(s.tr.seri) ? [{ ad: 'Türkiye', seri: s.tr.seri }] : [])],
    kaynak: s.kaynak, konum: s.konum, ek: s.ek, tanim: s.tanim,
  });
  return (
    <li className={`sbk-satir ${acik ? 'is-acik' : ''} ${yigin ? 'is-yigin' : ''}`} data-ders-ad={s.ad}>
      <div className="sbk-satir-ust">
        <div className="sbk-satir-ad">
          {acilir ? (
            <button type="button" className="sbk-satir-ac" onClick={() => setAcik((x) => !x)} aria-expanded={acik}>
              <span>{s.ad}</span><ChevronDown aria-hidden />
            </button>
          ) : <span className="sbk-satir-baslik">{s.ad}</span>}
          {s.alt && <small>{s.alt}</small>}
          {uzun && <span className="sbk-satir-metin">{d}<Atif id={s.kaynak} konum={s.konum} />{s.ek?.length ? <EkAtif ids={s.ek} /> : null}</span>}
        </div>
        {!uzun && s.deger !== undefined && (
          <div className="sbk-satir-d">
            <span>
              {d != null ? <b data-num>{d}</b> : <span className="sbk-satir-yok">teyit edilemedi</span>}
              {birimGoster && !uzunBirim && <small> {s.birim}</small>}
              <Atif id={s.kaynak} konum={s.konum} />{s.ek?.length ? <EkAtif ids={s.ek} /> : null}
            </span>
            {uzunBirim && <small className="sbk-satir-birim">{s.birim}</small>}
            {trD && <small className="sbk-satir-tr">Türkiye <b data-num>{trD}</b>{yon ? ` · ${yon}` : ''}</small>}
          </div>
        )}
        {s.deger === undefined && !uzun && <span className="sbk-satir-d"><span><Atif id={s.kaynak} konum={s.konum} />{s.ek?.length ? <EkAtif ids={s.ek} /> : null}</span></span>}
        {yilSay >= 2 ? (
          <button type="button" className="sbk-satir-gecmis" onClick={gecmisAc} aria-label={`${s.ad}: ${yilSay} yılın değerleri`} title="Geçmiş yıllar">
            <History aria-hidden /><span>{yilSay} yıl</span>
          </button>
        ) : <span className="sbk-satir-bosluk" aria-hidden />}
      </div>
      {acik && (
        <div className="sbk-satir-detay">
          {s.tanim && <p><b>Tanım:</b> {s.tanim}</p>}
          {s.detay?.length ? <MaddeAgaci ogeler={s.detay} sik /> : null}
          {s.adlar?.length ? <div className="sbk-etiketler">{s.adlar.map((a) => <Rozet key={a}>{a}</Rozet>)}</div> : null}
        </div>
      )}
    </li>
  );
};

export const Satirlar: React.FC<{ ogeler: SatirOge[] }> = ({ ogeler }) => (
  <ul className="sbk-satirlar">{ogeler.map((s, i) => <Satir key={`${s.ad}-${i}`} s={s} />)}</ul>
);

/** Başlıklı satır bloğu; madde görünümü aynı satırlardan üretilir */
const SatirBlok: React.FC<{ baslik: string; ikon?: React.ElementType; alt?: string; ogeler: SatirOge[]; arac?: React.ReactNode; children?: React.ReactNode }> = ({ baslik, ikon, alt, ogeler, arac, children }) => {
  if (!ogeler.length) return null;
  return (
    <Blok baslik={baslik} ikon={ikon} alt={alt} arac={arac} maddeler={() => ogeler.map(satirMaddesi)} className="is-satir">
      <Satirlar ogeler={ogeler} />
      {children}
    </Blok>
  );
};

/* ===============================================================================================================
 * Kurum sayıları: il sağlık müdürlüğü listeleri (kurum_sayilari) + envanter özeti tek listede, yinelenenler birleşir
 * =============================================================================================================== */

type SayiKaydi = NonNullable<KarabukVeri['kurum_sayilari']>[number];

function kurumSayilari(kb: KarabukVeri): SayiKaydi[] {
  return [...(kb.kurum_sayilari || []), ...((kb.envanter?.ozet || []) as SayiKaydi[])];
}

/** Desene uyan ilk kaydı (geçmiş yılı olan öncelikli) verir; aynı kurumun öbür kopyası `kullanilan`a işlenir */
function kurumSec(liste: SayiKaydi[], re: RegExp, kullanilan?: Set<SayiKaydi>): SayiKaydi | undefined {
  const es = liste.filter((k) => re.test(k.tur) && !kullanilan?.has(k));
  if (!es.length) return undefined;
  es.forEach((k) => kullanilan?.add(k));
  const sec = es.find((k) => sayiSay(k.seri) > 1) || es[0];
  const adlar = sec.adlar?.length ? sec.adlar : es.find((k) => k.adlar?.length)?.adlar;
  return { ...sec, adlar };
}

const sayildi = (k: SayiKaydi) => (k.yontem && /sayıldı|sayım|listesinden/i.test(k.yontem) ? 'resmî listeden sayıldı' : undefined);

const kurumSatiri = (k: SayiKaydi, ek?: Partial<SatirOge>): SatirOge => ({
  ad: k.tur, deger: k.sayi, alt: temiz<string>([k.yil != null && String(k.yil), sayildi(k)]).join(' · ') || undefined,
  kaynak: k.kaynak, konum: k.konum, seri: k.seri, adlar: k.adlar,
  detay: temiz<MaddeOge>([k.yontem && `Nasıl sayıldı: ${k.yontem}`, k.not]),
  ...ek,
});

const KURUM_GRUPLARI: { id: string; baslik: string; ikon: React.ElementType; alt: string; desenler: RegExp[] }[] = [
  { id: 'yonetim', baslik: 'Yönetim', ikon: Landmark, alt: 'İl ve ilçe sağlık müdürlükleri', desenler: [/^[iİ]l sağlık müdürlüğü/i, /^[iİ]lçe sağlık müdürlüğü/i] },
  {
    id: 'birinci', baslik: 'Birinci basamak ve halk sağlığı', ikon: Stethoscope, alt: 'Aile hekimliği, toplum sağlığı ve tarama birimleri',
    desenler: [/^toplum sağlığı merkezi \(TSM\)/i, /^aile sağlığı merkezi/i, /^aile hekimliği birimi/i, /^aile hekimi/i, /sağlıklı hayat/i, /^KETEM/i, /verem/i, /laboratuvar/i, /ruh sağlığı/i, /kuduz/i, /yabancı uyruklu|göçmen/i],
  },
  {
    id: 'hastane', baslik: 'Hastane ve acil sağlık', ikon: Hospital, alt: 'Yataklı kurumlar, 112 ve evde sağlık',
    desenler: [/^hastane \(sağlık bakanlığı\)/i, /^hastane \(tüm/i, /yatağı/i, /ağız ve diş/i, /ambulans servisi/i, /112.*istasyon/i, /112.*ambulans/i, /evde sağlık/i],
  },
  { id: 'insan', baslik: 'Sağlık insan gücü', ikon: UserRound, alt: 'Tüm sektörlerde çalışan sağlık personeli', desenler: [/^toplam hekim/i, /^diş hekimi/i, /^eczacı/i, /^hemşire/i, /^ebe/i, /personel/i] },
];

function kurumGruplari(kb: KarabukVeri) {
  const liste = kurumSayilari(kb).filter((k) => !/hava kalitesi/i.test(k.tur));
  const kullanilan = new Set<SayiKaydi>();
  const arsiv = liste.find((k) => /toplum sağlığı merkezi \(2017/i.test(k.tur));
  if (arsiv) kullanilan.add(arsiv);
  const gruplar = KURUM_GRUPLARI.map((g) => ({
    ...g,
    satirlar: temiz<SatirOge>(g.desenler.map((re) => {
      const k = kurumSec(liste, re, kullanilan);
      if (!k) return null;
      if (arsiv && /^toplum sağlığı merkezi \(TSM\)/i.test(k.tur)) {
        return kurumSatiri(k, { detay: temiz<MaddeOge>([k.yontem && `Nasıl sayıldı: ${k.yontem}`, k.not, { metin: `2017 arşiv listesinde ${arsiv.sayi} TSM vardı: ${(arsiv.adlar || []).join(', ')}`, kaynak: arsiv.kaynak, konum: arsiv.konum }]) });
      }
      return kurumSatiri(k);
    })),
  }));
  const kalan = liste.filter((k) => !kullanilan.has(k));
  if (kalan.length) gruplar.push({ id: 'diger', baslik: 'Diğer', ikon: Building2, alt: '', desenler: [], satirlar: kalan.map((k) => kurumSatiri(k)) });
  return gruplar.filter((g) => g.satirlar.length);
}

/* ===============================================================================================================
 * Alt sayfa gezintisi
 * =============================================================================================================== */

const AltNav: React.FC<{ sec: KarabukSayfaId; git: (id: KarabukSayfaId) => void }> = ({ sec, git }) => (
  <nav className="sbk-altnav" aria-label="Karabük sayfaları">
    {KARABUK_SAYFALAR.map((s) => {
      const Ic = s.icon;
      return (
        <button key={s.id} type="button" aria-current={s.id === sec ? 'page' : undefined} onClick={() => git(s.id)}>
          <Ic aria-hidden /><span>{s.kisa}</span>
        </button>
      );
    })}
  </nav>
);

const AltGecis: React.FC<{ sec: KarabukSayfaId; git: (id: KarabukSayfaId) => void }> = ({ sec, git }) => {
  const i = KARABUK_SAYFALAR.findIndex((s) => s.id === sec);
  const onceki = KARABUK_SAYFALAR[i - 1];
  const sonraki = KARABUK_SAYFALAR[i + 1];
  return (
    <nav className="sbk-altgecis" aria-label="Önceki ve sonraki sayfa">
      {onceki ? (
        <button type="button" onClick={() => git(onceki.id)}><ArrowLeft aria-hidden /><span><small>Önceki</small>{onceki.ad}</span></button>
      ) : <span />}
      {sonraki ? (
        <button type="button" className="is-sonraki" onClick={() => git(sonraki.id)}><span><small>Sonraki</small>{sonraki.ad}</span><ArrowRight aria-hidden /></button>
      ) : <span />}
    </nav>
  );
};

/* ===============================================================================================================
 * Sayfalar
 * =============================================================================================================== */

/** "Kısaca" cümlesi: "Başlık: **34** ASM, **90** AHB (2026)." — yıl hepsinde aynıysa sonda bir kez */
function cumle(bas: string, kalemler: { k?: SayiKaydi; ad: string }[]): MaddeOge | null {
  const v = kalemler.filter((x): x is { k: SayiKaydi; ad: string } => !!x.k);
  if (!v.length) return null;
  const yillar = benzersiz(v.map((x) => (x.k.yil != null ? String(x.k.yil) : undefined)));
  const tekYil = yillar.length === 1;
  const metin = `${bas}: ${v.map((x) => `**${sayi(x.k.sayi)}** ${x.ad}${!tekYil && x.k.yil != null ? ` (${x.k.yil})` : ''}`).join(', ')}${tekYil ? ` (${yillar[0]})` : ''}.`;
  const kaynaklar = benzersiz(v.map((x) => x.k.kaynak));
  return { metin, kaynak: kaynaklar[0], ek: kaynaklar.slice(1) };
}

const OzetSayfa: React.FC<{ kb: KarabukVeri; git: (id: KarabukSayfaId) => void }> = ({ kb, git }) => {
  const n = kb.nufus;
  const liste = useMemo(() => kurumSayilari(kb), [kb]);
  const k = (re: RegExp) => kurumSec(liste, re);
  const g = (re: RegExp) => kb.gostergeler?.find((x) => re.test(x.ad));
  const ilceler = [...(n?.ilceler || [])].sort((a, b) => b.nufus - a.nufus).map((x) => x.ad);
  const ilceSmYeri = (kb.envanter?.ilce_ozeti || []).filter((x) => Number(x.ilce_sm) > 0).map((x) => x.ilce);
  const y65 = n?.yas_65_ustu_orani;
  const gos = (re: RegExp, ad: string): MaddeOge | null => {
    const x = g(re);
    if (!x || x.deger == null) return null;
    const b = x.birim && x.birim !== '%' ? ` ${x.birim}` : '';
    const v = (d: number | string) => (x.birim === '%' ? `%${typeof d === 'number' ? sayi(d) : d}` : typeof d === 'number' ? sayi(d) : d);
    return { metin: `${ad}: **${v(x.deger)}**${b}${x.turkiye != null ? `; Türkiye ${v(x.turkiye)}` : ''} (${x.yil}).`, kaynak: x.kaynak, konum: x.konum };
  };
  const pm = (kb.cevre || []).find((c) => /PM10/i.test(c.baslik) && typeof c.deger === 'number');
  const maddeler = temiz<MaddeOge>([
    n?.toplam != null && { metin: `**${sayi(n.toplam)}** kişi yaşıyor (${n.yil})${ilceler.length ? `; **${ilceler.length}** ilçe: ${ilceler.join(', ')}` : ''}.`, kaynak: n.kaynak, konum: n.konum },
    y65 && { metin: `65 yaş ve üstü nüfusun oranı **%${sayi(y65.deger)}**${y65.turkiye != null ? ` (Türkiye %${sayi(y65.turkiye)})` : ''}, ${y65.yil}.`, kaynak: y65.kaynak, konum: y65.konum },
    cumle('Yönetim', [
      { k: k(/^[iİ]l sağlık müdürlüğü/i), ad: 'il sağlık müdürlüğü' },
      { k: k(/^[iİ]lçe sağlık müdürlüğü/i), ad: `ilçe sağlık müdürlüğü${ilceSmYeri.length ? ` (${ilceSmYeri.join(', ')})` : ''}` },
    ]),
    cumle('Birinci basamak', [
      { k: k(/^aile sağlığı merkezi/i), ad: 'aile sağlığı merkezi' },
      { k: k(/^aile hekimliği birimi/i), ad: 'aile hekimliği birimi' },
      { k: k(/^toplum sağlığı merkezi \(TSM\)/i), ad: 'toplum sağlığı merkezi' },
    ]),
    cumle('Hastane ve acil', [
      { k: k(/^hastane \(tüm/i) || k(/^hastane/i), ad: 'hastane' },
      { k: k(/yatağı/i), ad: 'yatak' },
      { k: k(/112.*istasyon/i), ad: '112 istasyonu' },
      { k: k(/112.*ambulans/i), ad: 'ambulans' },
    ]),
    cumle('Sağlık insan gücü', [
      { k: k(/^toplam hekim/i), ad: 'hekim' },
      { k: k(/^hemşire/i), ad: 'hemşire' },
      { k: k(/^ebe/i), ad: 'ebe' },
      { k: k(/^diş hekimi/i), ad: 'diş hekimi' },
      { k: k(/^eczacı/i), ad: 'eczacı' },
    ]),
    gos(/^bebek ölüm/i, 'Bebek ölüm hızı'),
    gos(/^doğuşta beklenen yaşam/i, 'Doğuşta beklenen yaşam süresi'),
    gos(/^toplam doğurganlık/i, 'Toplam doğurganlık hızı'),
    pm && { metin: `Hava: ${pm.istasyon ? `${pm.istasyon.replace(/\s*\(.*\)$/, '')} istasyonunda ` : ''}PM10 yıllık ortalaması **${sayi(pm.deger as number)}** ${pm.birim || ''}, ${pm.yil}.`, kaynak: pm.kaynak, konum: pm.konum },
  ]);
  return (
    <>
      <Blok baslik="Kısaca Karabük" ikon={MapPin} alt="Resmî kaynaklardaki en güncel değerler; ayrıntılar alt sayfalarda" maddeler={maddeler} genis>
        <div className="sbk-kisaca"><MaddeAgaci ogeler={maddeler} /></div>
      </Blok>
      <div className="sbk-kart-g sbk-altkartlar">
        {KARABUK_SAYFALAR.filter((s) => s.id !== 'ozet').map((s) => {
          const Ic = s.icon;
          return (
            <button key={s.id} type="button" className="sbk-bolum-kart" onClick={() => git(s.id)}>
              <span className="sbk-bolum-kart-ic"><Ic aria-hidden /></span>
              <span className="sbk-bolum-kart-t">{s.ad}</span>
              <span className="sbk-bolum-kart-a">{s.aciklama}</span>
              <ArrowRight aria-hidden className="sbk-bolum-kart-ok" />
            </button>
          );
        })}
      </div>
    </>
  );
};

/* ── Kurumlar ───────────────────────────────────────────────────────────────────────────────────────────────── */

type KurumT = NonNullable<NonNullable<KarabukVeri['envanter']>['kurumlar']>[number];

/** Veride "Diğer" diye girilmiş kurumların türü addan çıkarılır (TSM, ambulans başhekimliği) */
const turAdi = (k: KurumT) => {
  if (/toplum sağlığı merkezi|t\.s\.m/i.test(k.ad)) return 'Toplum sağlığı merkezi';
  if (/ambulans servisi/i.test(k.ad)) return 'İl ambulans servisi başhekimliği';
  if (/gezici/i.test(k.ad)) return 'Gezici sağlık hizmeti';
  if (/sağlık evi/i.test(k.ad)) return 'Sağlık evi';
  if (/yabancı uyruklu|göçmen/i.test(k.ad)) return 'Göçmen polikliniği';
  return k.tur === 'Diğer' ? k.ad : k.tur;
};

type Dugum = { k: KurumT; cocuk: Dugum[] };

/** bagli alanından ağaç: üst kurum adı bağlılık metninin başıyla eşleşir */
function bagliAgac(kurumlar: KurumT[]) {
  const ust = (k: KurumT): KurumT | undefined => {
    const b = (k.bagli || '').trim();
    if (!b) return undefined;
    return kurumlar.find((p) => p !== k && turAdi(p) !== 'Kuduz aşı merkezi' && (b.startsWith(p.ad) || p.ad.startsWith(b)));
  };
  const dugum = new Map<KurumT, Dugum>(kurumlar.map((k) => [k, { k, cocuk: [] }]));
  const kok: Dugum[] = [];
  const baskaBagli: KurumT[] = [];
  for (const k of kurumlar) {
    const u = ust(k);
    if (u) dugum.get(u)!.cocuk.push(dugum.get(k)!);
    else if (/bakanlığı/i.test(k.bagli || '')) kok.push(dugum.get(k)!);
    else baskaBagli.push(k);
  }
  return { kok, baskaBagli };
}

const grupla = (d: Dugum[]) => {
  const m = new Map<string, Dugum[]>();
  for (const x of d) { const t = turAdi(x.k); m.set(t, [...(m.get(t) || []), x]); }
  return [...m.entries()];
};

const AgacDugum: React.FC<{ d: Dugum; acikBas?: boolean }> = ({ d, acikBas }) => {
  const [acik, setAcik] = useState(!!acikBas);
  const n = d.cocuk.length;
  return (
    <li>
      <div className="sbk-hiy-s">
        {n ? (
          <button type="button" onClick={() => setAcik((x) => !x)} aria-expanded={acik}>
            <ChevronDown aria-hidden className="sbk-hiy-ok" /><b>{d.k.ad}</b>
          </button>
        ) : <span className="sbk-hiy-ad"><b>{d.k.ad}</b></span>}
        <small>{[turAdi(d.k) !== d.k.ad ? turAdi(d.k) : '', d.k.ilce].filter(Boolean).join(' · ')}{n ? ` · ${n} bağlı birim` : ''}<Atif id={d.k.kaynak} konum={d.k.konum} /></small>
      </div>
      {n > 0 && acik && <AgacListe dugumler={d.cocuk} />}
    </li>
  );
};

const AgacGrup: React.FC<{ tur: string; liste: Dugum[] }> = ({ tur, liste }) => {
  const [acik, setAcik] = useState(false);
  return (
    <li>
      <div className="sbk-hiy-s">
        <button type="button" onClick={() => setAcik((x) => !x)} aria-expanded={acik}>
          <ChevronDown aria-hidden className="sbk-hiy-ok" /><b>{tur}</b><Rozet>{liste.length}</Rozet>
        </button>
        <small>{benzersiz(liste.map((x) => x.k.ilce)).join(', ')}</small>
      </div>
      {acik && (
        <ul className="sbk-hiy-l">
          {liste.map((x) => <AgacDugum key={`${x.k.ad}-${x.k.ilce}`} d={x} />)}
        </ul>
      )}
    </li>
  );
};

const AgacListe: React.FC<{ dugumler: Dugum[]; acikBas?: boolean }> = ({ dugumler, acikBas }) => (
  <ul className="sbk-hiy-l">
    {grupla(dugumler).map(([tur, liste]) => (liste.length === 1
      ? <AgacDugum key={tur} d={liste[0]} acikBas={acikBas} />
      : <AgacGrup key={tur} tur={tur} liste={liste} />))}
  </ul>
);

const agacMaddeleri = (d: Dugum[]): MaddeOge[] => grupla(d).map(([tur, liste]) => (liste.length === 1
  ? { metin: `**${liste[0].k.ad}**${turAdi(liste[0].k) !== liste[0].k.ad ? ` (${turAdi(liste[0].k)})` : ''}`, kaynak: liste[0].k.kaynak, alt: agacMaddeleri(liste[0].cocuk) }
  : { metin: `**${tur}** (${liste.length})`, alt: liste.map((x) => ({ metin: `${x.k.ad}${x.k.ilce ? ` — ${x.k.ilce}` : ''}`, kaynak: x.k.kaynak, alt: agacMaddeleri(x.cocuk) })) }));

const KimKimeBagli: React.FC<{ kurumlar: KurumT[] }> = ({ kurumlar }) => {
  const { kok, baskaBagli } = useMemo(() => bagliAgac(kurumlar), [kurumlar]);
  if (!kok.length) return null;
  return (
    <Blok
      baslik="Kim kime bağlı?" ikon={GitFork} alt="Bakanlıktan sahadaki birime örgüt şeması · başlığa dokun: bağlı birimler"
      maddeler={() => [{ metin: '**T.C. Sağlık Bakanlığı**', alt: agacMaddeleri(kok) }, ...(baskaBagli.length ? [{ metin: '**Başka bir birimin içinde çalışanlar**', alt: baskaBagli.map((k) => ({ metin: `${k.ad} → ${k.bagli}`, kaynak: k.kaynak })) }] : [])]}
    >
      <div className="sbk-hiy">
        <div className="sbk-hiy-kok"><Landmark aria-hidden /><b>T.C. Sağlık Bakanlığı</b></div>
        <AgacListe dugumler={kok} acikBas />
      </div>
      {baskaBagli.length > 0 && (
        <div className="sbk-hiy-ek">
          <h4>Başka bir birimin içinde çalışanlar</h4>
          <ul className="sbk-madde">
            {grupla(baskaBagli.map((k) => ({ k, cocuk: [] }))).map(([tur, l]) => (
              <li key={tur}>
                <b>{l.length > 1 ? `${tur} (${l.length})` : l[0].k.ad}</b> <span className="sbk-muted">→ {benzersiz(l.map((x) => x.k.bagli)).join('; ')}</span>
                <Atif id={l[0].k.kaynak} konum={l[0].k.konum} />
              </li>
            ))}
          </ul>
        </div>
      )}
    </Blok>
  );
};

const KurumKarti: React.FC<{ k: KurumT }> = ({ k }) => {
  const [acik, setAcik] = useState(false);
  const ayrinti = (k.gorev?.length || 0) > 0 || !!k.adres || !!k.not || !!k.bagli;
  return (
    <li className={`sbk-kk ${acik ? 'is-acik' : ''}`}>
      <button type="button" onClick={() => setAcik((x) => !x)} aria-expanded={acik} disabled={!ayrinti}>
        <span className="sbk-gezgin-ic">{/müdürlü/i.test(k.tur) ? <Landmark aria-hidden /> : /hastane/i.test(k.tur) ? <Hospital aria-hidden /> : /112/.test(k.tur) ? <Ambulance aria-hidden /> : <Building2 aria-hidden />}</span>
        <span className="sbk-gezgin-t"><b>{k.ad}</b><small>{[turAdi(k) !== k.ad ? turAdi(k) : '', k.ilce].filter(Boolean).join(' · ')}</small></span>
        <Atif id={k.kaynak} konum={k.konum} />
        {ayrinti && <ChevronDown aria-hidden className="sbk-gezgin-ok" />}
      </button>
      {acik && (
        <div className="sbk-kk-d">
          <dl className="sbk-duzey-dl">
            {k.bagli && <div><dt>Bağlı olduğu</dt><dd>{k.bagli}</dd></div>}
            {k.adres && <div><dt>Adres</dt><dd>{k.adres}</dd></div>}
            {k.not && <div><dt>Not</dt><dd>{k.not}</dd></div>}
          </dl>
          {(k.gorev?.length || 0) > 0 && <ul className="sbk-madde">{k.gorev!.map((x, i) => <li key={i}>{x}</li>)}</ul>}
          {k.url && /^https:\/\/[^/]+\.(gov|edu|bel)\.tr/.test(k.url) && <a className="sbk-bag" href={k.url} target="_blank" rel="noopener noreferrer">Resmî sayfası <ExternalLink aria-hidden /></a>}
        </div>
      )}
    </li>
  );
};

const kurumMaddesi = (k: KurumT): MaddeOge => ({
  metin: `**${k.ad}** (${[turAdi(k) !== k.ad ? turAdi(k) : '', k.ilce].filter(Boolean).join(', ')})`, kaynak: k.kaynak,
  alt: temiz<string>([k.bagli && `Bağlı: ${k.bagli}`, k.adres && `Adres: ${k.adres}`, ...(k.gorev || []), k.not]),
});

const KurumRehberi: React.FC<{ kurumlar: KurumT[]; ilceSabit?: string; baslik?: string }> = ({ kurumlar, ilceSabit, baslik = 'Tüm kurumlar' }) => {
  const [tur, setTur] = useState('');
  const [ilce, setIlce] = useState('');
  const [q, setQ] = useState('');
  const [hepsi, setHepsi] = useState(false);
  const turler = useMemo(() => {
    const m = new Map<string, number>();
    for (const k of kurumlar) m.set(turAdi(k), (m.get(turAdi(k)) || 0) + 1);
    return [...m.entries()].filter(([, n]) => n > 1).sort((a, b) => b[1] - a[1]);
  }, [kurumlar]);
  const ilceler = useMemo(() => benzersiz(kurumlar.map((k) => k.ilce)), [kurumlar]);
  const kq = kucukHarf(q.trim());
  const liste = kurumlar.filter((k) => (!tur || turAdi(k) === tur) && (!ilce || k.ilce === ilce) && (!kq || kucukHarf(`${k.ad} ${k.tur} ${k.ilce} ${k.adres || ''}`).includes(kq)));
  if (!kurumlar.length) return null;
  const SINIR = 8;
  const suzgec = !!(tur || ilce || kq);
  const gorunen = hepsi || suzgec ? liste : liste.slice(0, SINIR);
  return (
    <Blok
      baslik={`${baslik} (${kurumlar.length})`} ikon={Building2} alt="Adres, bağlılık ve görevler · kuruma dokun" maddeler={() => liste.map(kurumMaddesi)}
    >
      {kurumlar.length > SINIR && (
        <div className="sbk-bildirim-arac">
          <label className="sbk-ara"><Search aria-hidden /><input type="search" value={q} onChange={(ev) => setQ(ev.target.value)} placeholder="Kurum ara (ör. Safranbolu, KETEM)" aria-label="Kurumlarda ara" /></label>
          {turler.length > 1 && (
            <select className="sbk-sec" value={tur} onChange={(ev) => setTur(ev.target.value)} aria-label="Kurum türü">
              <option value="">Tüm türler</option>
              {turler.map(([t, n]) => <option key={t} value={t}>{t} ({n})</option>)}
            </select>
          )}
          {!ilceSabit && ilceler.length > 1 && (
            <select className="sbk-sec" value={ilce} onChange={(ev) => setIlce(ev.target.value)} aria-label="İlçe">
              <option value="">Tüm ilçeler</option>
              {ilceler.map((x) => <option key={x} value={x}>{x}</option>)}
            </select>
          )}
        </div>
      )}
      <ul className="sbk-kk-l">{gorunen.map((k, i) => <KurumKarti key={`${k.tur}-${k.ad}-${k.ilce || ''}-${i}`} k={k} />)}</ul>
      {!liste.length && <p className="sbk-bos">Eşleşen kurum yok.</p>}
      {!suzgec && liste.length > SINIR && (
        <button type="button" className="sbk-btn sbk-hepsi" onClick={() => setHepsi((x) => !x)} aria-expanded={hepsi}>
          {hepsi ? 'Daha az göster' : `Tümünü göster (${liste.length})`} <ChevronDown aria-hidden />
        </button>
      )}
    </Blok>
  );
};

const KurumlarSayfa: React.FC<{ kb: KarabukVeri }> = ({ kb }) => {
  const gruplar = useMemo(() => kurumGruplari(kb), [kb]);
  const kurumlar = kb.envanter?.kurumlar || [];
  return (
    <>
      <KimKimeBagli kurumlar={kurumlar} />
      {gruplar.map((g) => <SatirBlok key={g.id} baslik={g.baslik} ikon={g.ikon} alt={`${g.alt ? `${g.alt} · ` : ''}satıra dokun: adlar ve ayrıntı`} ogeler={g.satirlar} />)}
      <SatirBlok
        baslik="Hastaneler tek tek" ikon={Hospital}
        ogeler={(kb.hastaneler || []).map((h) => ({ ad: h.ad, alt: h.ilce, kaynak: h.kaynak, deger: undefined, detay: temiz<MaddeOge>([h.tur, h.not]) }))}
      />
      <SatirBlok
        baslik="Halk sağlığı birimleri" ikon={Stethoscope} alt="İl sağlık müdürlüğüne bağlı birimler ne iş yapar?"
        ogeler={(kb.birimler || []).map((b) => ({ ad: b.ad, alt: b.adres_ilce?.split(/\s+[–-]\s+/)[0], kaynak: b.kaynak, detay: temiz<MaddeOge>([b.aciklama, b.adres_ilce && `Adres: ${b.adres_ilce}`]) }))}
      />
      <KurumRehberi kurumlar={kurumlar} />
    </>
  );
};

/* ── İlçeler ────────────────────────────────────────────────────────────────────────────────────────────────── */

const ILCE_ALANLARI: { anahtar: string; ad: string }[] = [
  { anahtar: 'il_sm', ad: 'İl sağlık müdürlüğü' }, { anahtar: 'ilce_sm', ad: 'İlçe sağlık müdürlüğü' }, { anahtar: 'tsm', ad: 'Toplum sağlığı merkezi' },
  { anahtar: 'asm', ad: 'Aile sağlığı merkezi' }, { anahtar: 'ahb', ad: 'Aile hekimliği birimi' }, { anahtar: 'hastane', ad: 'Hastane' },
  { anahtar: 'istasyon_112', ad: '112 istasyonu' }, { anahtar: 'kuduz', ad: 'Kuduz aşı merkezi' }, { anahtar: 'evde_saglik', ad: 'Evde sağlık birimi' },
];
const TABLO_SUTUN: { anahtar: string; ad: string }[] = [
  { anahtar: 'il_sm', ad: 'İl SM' }, { anahtar: 'ilce_sm', ad: 'İlçe SM' }, { anahtar: 'tsm', ad: 'TSM' }, { anahtar: 'asm', ad: 'ASM' },
  { anahtar: 'ahb', ad: 'Aile hek. birimi' }, { anahtar: 'hastane', ad: 'Hastane' }, { anahtar: 'istasyon_112', ad: '112' },
  { anahtar: 'kuduz', ad: 'Kuduz' }, { anahtar: 'evde_saglik', ad: 'Evde sağlık' },
];
const hucre = (v: unknown): string => (v == null || v === '' ? '?' : typeof v === 'number' ? sayi(v) : String(v));

const IlcelerSayfa: React.FC<{ kb: KarabukVeri }> = ({ kb }) => {
  const n = kb.nufus;
  const ozet = kb.envanter?.ilce_ozeti || [];
  const adlar = useMemo(() => {
    const s = benzersiz([...(n?.ilceler || []).map((x) => x.ad), ...(kb.ilceler || []).map((x) => x.ad), ...ozet.map((x) => x.ilce)]);
    const nf = (a: string) => n?.ilceler?.find((x) => x.ad === a)?.nufus || 0;
    return s.sort((a, b) => nf(b) - nf(a));
  }, [n, kb.ilceler, ozet]);
  const [sec, setSec] = useState(adlar[0] || '');
  if (!adlar.length) return <p className="sbk-bos">İlçe verisi bulunamadı.</p>;
  const ilce = adlar.includes(sec) ? sec : adlar[0];
  const nu = n?.ilceler?.find((x) => x.ad === ilce);
  const il = kb.ilceler?.find((x) => x.ad === ilce);
  const oz = ozet.find((x) => x.ilce === ilce);
  const pay = nu && n?.toplam ? (nu.nufus / n.toplam) * 100 : null;
  const nufusSatir = temiz<SatirOge>([
    nu && { ad: 'Nüfus', deger: nu.nufus, alt: temiz<string>([n?.yil != null && String(n.yil), pay != null && `ilin %${sayi(+pay.toFixed(1))}'i (hesaplandı)`]).join(' · '), kaynak: n?.kaynak, konum: n?.konum, seri: nu.seri },
    nu?.ilce_merkezi != null && { ad: 'İlçe merkezinde yaşayan', deger: nu.ilce_merkezi, kaynak: n?.kaynak },
    nu?.belde_koy != null && { ad: 'Belde ve köylerde yaşayan', deger: nu.belde_koy, kaynak: n?.kaynak },
    nu?.yillik_artis_hizi_binde != null && { ad: 'Yıllık nüfus artış hızı', deger: nu.yillik_artis_hizi_binde, birim: 'binde', alt: nu.yillik_artis_hizi_binde < 0 ? 'eksi: nüfus azalıyor' : undefined, kaynak: n?.kaynak },
  ]);
  const kurumSatir = temiz<SatirOge>([
    ...ILCE_ALANLARI.map((a) => {
      if (!oz || !(a.anahtar in oz)) return null;
      const v = oz[a.anahtar];
      const ek: Partial<SatirOge> = {};
      if (a.anahtar === 'asm' && il?.asm_adlari?.length) ek.adlar = il.asm_adlari;
      if (a.anahtar === 'hastane' && il?.hastane) ek.alt = il.hastane;
      return { ad: a.ad, deger: v === 0 ? 'Yok' : (v as number | null), kaynak: oz.kaynak, ...ek } as SatirOge;
    }),
    il?.ahb_basina_nufus != null && { ad: 'Aile hekimliği birimi başına nüfus', deger: il.ahb_basina_nufus, alt: 'ilçe nüfusu ÷ birim sayısı (hesaplandı)', kaynak: il.kaynak },
    oz?.diger?.length && { ad: 'Diğer birimler', deger: oz.diger.length, adlar: oz.diger, kaynak: oz.kaynak },
  ]);
  const kurumlar = (kb.envanter?.kurumlar || []).filter((k) => k.ilce === ilce);
  const notMetni = typeof oz?.not === 'string' ? oz.not : '';
  return (
    <>
      <div className="sbk-cip-l sbk-ilce-cip" role="tablist" aria-label="İlçe seç">
        {adlar.map((a) => {
          const nf = n?.ilceler?.find((x) => x.ad === a)?.nufus;
          return (
            <button key={a} type="button" role="tab" aria-selected={a === ilce} className={`sbk-cip ${a === ilce ? 'is-sec' : ''}`} onClick={() => setSec(a)}>
              {a}{nf ? <small> · {sayi(nf)}</small> : null}
            </button>
          );
        })}
      </div>
      <SatirBlok baslik={`${ilce}: nüfus`} ikon={Users} ogeler={nufusSatir} />
      <SatirBlok
        baslik={`${ilce}: sağlık kurumları`} ikon={Landmark} alt="Yok = ilçede bulunmuyor · teyit edilemedi = resmî kaynakta bulunamadı"
        ogeler={kurumSatir}
      >
        {notMetni && <p className="sbk-not"><b>Not:</b> {notMetni}<EkAtif ids={(oz?.ek_kaynaklar as string[] | undefined) || []} /></p>}
      </SatirBlok>
      <KurumRehberi kurumlar={kurumlar} ilceSabit={ilce} baslik={`${ilce}'deki kurumlar`} />
      {ozet.length > 0 && (
        <Blok
          baslik="Tüm ilçeler yan yana" ikon={MapPinned} alt="SM = sağlık müdürlüğü · TSM = toplum sağlığı merkezi · ? = teyit edilemedi"
          maddeler={() => ozet.map((x) => ({ metin: `**${x.ilce}**`, kaynak: x.kaynak, alt: TABLO_SUTUN.filter((s) => x[s.anahtar] != null).map((s) => `${s.ad}: ${hucre(x[s.anahtar])}`) }))}
        >
          <details className="sbk-katla">
            <summary>Karşılaştırma tablosunu aç <ChevronDown aria-hidden /></summary>
            <OkunurTablo
              baslik="İlçelere göre sağlık kurumları"
              sutunlar={[{ anahtar: 'ilce', ad: 'İlçe' }, ...TABLO_SUTUN]}
              satirlar={ozet.map((x) => ({ ilce: <b>{x.ilce}<Atif id={x.kaynak} /></b>, ...Object.fromEntries(TABLO_SUTUN.map((s) => [s.anahtar, hucre(x[s.anahtar])])) }))}
            />
          </details>
        </Blok>
      )}
    </>
  );
};

/* ── Nüfus ──────────────────────────────────────────────────────────────────────────────────────────────────── */

const NufusSayfa: React.FC<{ kb: KarabukVeri }> = ({ kb }) => {
  const n = kb.nufus;
  if (!n) return <p className="sbk-bos">Nüfus verisi bulunamadı.</p>;
  const o = (x: typeof n.yas_65_ustu_orani, ad: string, alt?: string): SatirOge | null => (x ? {
    ad, deger: x.deger, birim: '%', alt: temiz<string>([x.yil != null && String(x.yil), x.sayi != null && `${sayi(x.sayi)} kişi`, alt]).join(' · '),
    kaynak: x.kaynak, konum: x.konum, seri: x.seri, tr: x.turkiye != null ? { deger: x.turkiye } : undefined,
  } : null);
  const genel = temiz<SatirOge>([
    n.toplam != null && { ad: 'Toplam nüfus', deger: n.toplam, alt: `${n.yil} · 31 Aralık`, kaynak: n.kaynak, konum: n.konum, seri: n.seri },
    n.onceki_yil && { ad: `Bir önceki yıl (${n.onceki_yil.yil})`, deger: n.onceki_yil.toplam, kaynak: n.onceki_yil.kaynak, konum: n.onceki_yil.konum },
    n.yillik_artis_hizi_binde != null && { ad: 'Yıllık nüfus artış hızı', deger: n.yillik_artis_hizi_binde, birim: 'binde', alt: n.yillik_artis_hizi_binde < 0 ? 'eksi: nüfus azalıyor' : undefined, kaynak: n.kaynak },
    n.erkek != null && { ad: 'Erkek', deger: n.erkek, kaynak: n.kaynak },
    n.kadin != null && { ad: 'Kadın', deger: n.kadin, kaynak: n.kaynak },
    n.il_ilce_merkezi != null && { ad: 'İl ve ilçe merkezlerinde', deger: n.il_ilce_merkezi, kaynak: n.kaynak },
    n.belde_koy != null && { ad: 'Belde ve köylerde', deger: n.belde_koy, kaynak: n.kaynak },
  ]);
  const yas = temiz<SatirOge>([
    o(n.yas_0_14_orani, '0–14 yaş (çocuk) oranı'),
    o(n.yas_65_ustu_orani, '65 yaş ve üstü (yaşlı) oranı'),
    o(n.yasli_bagimlilik_orani, 'Yaşlı bağımlılık oranı', '65+ ÷ 15–64 yaş × 100'),
    o(n.toplam_bagimlilik_orani, 'Toplam bağımlılık oranı', '(0–14 + 65+) ÷ 15–64 yaş × 100'),
  ]);
  const kk = n.kent_kir_2024;
  const kentKir = kk ? temiz<SatirOge>([
    kk.yogun_kent_yuzde != null && { ad: 'Yoğun kent', deger: kk.yogun_kent_yuzde, birim: '%', kaynak: kk.kaynak, konum: kk.konum },
    kk.orta_yogun_kent_yuzde != null && { ad: 'Orta yoğun kent', deger: kk.orta_yogun_kent_yuzde, birim: '%', kaynak: kk.kaynak, konum: kk.konum },
    kk.kir_yuzde != null && { ad: 'Kır', deger: kk.kir_yuzde, birim: '%', kaynak: kk.kaynak, konum: kk.konum },
  ]) : [];
  const ilceler = [...(n.ilceler || [])].sort((a, b) => b.nufus - a.nufus).map<SatirOge>((x) => ({
    ad: x.ad, deger: x.nufus, alt: n.toplam ? `ilin %${sayi(+((x.nufus / n.toplam) * 100).toFixed(1))}'i (hesaplandı)` : undefined, kaynak: n.kaynak, seri: x.seri,
  }));
  return (
    <>
      <SatirBlok baslik="Kaç kişi, nerede yaşıyor?" ikon={Users} alt="TÜİK Adrese Dayalı Nüfus Kayıt Sistemi · saat simgesi: geçmiş yıllar" ogeler={genel} />
      <SatirBlok baslik="Yaş yapısı" ikon={Baby} alt="Karabük, Türkiye'ye göre daha yaşlı bir il mi? Sağdaki küçük satır Türkiye değeri" ogeler={yas} />
      <SatirBlok baslik={`Kent ve kır${kk?.yil ? ` (${kk.yil})` : ''}`} ikon={MapPin} alt="Nüfusun yerleşim yoğunluğuna göre dağılımı" ogeler={kentKir} />
      <SatirBlok baslik="İlçelerin nüfusu" ikon={MapPinned} alt="Büyükten küçüğe" ogeler={ilceler} />
    </>
  );
};

/* ── Göstergeler ────────────────────────────────────────────────────────────────────────────────────────────── */

/** `once`: eşleşmesi öbür gruplardan önce yapılır (ör. "hekime müracaat" kapasite değil kullanım) */
const GOSTERGE_GRUPLARI: { baslik: string; ikon: React.ElementType; alt: string; re: RegExp; once?: boolean }[] = [
  { baslik: 'Doğum ve doğurganlık', ikon: Baby, alt: 'Kaç bebek doğuyor?', re: /doğum hızı|doğurganlık/i },
  { baslik: 'Ölüm ve yaşam süresi', ikon: Skull, alt: 'Bebek, çocuk ve genel ölüm; beklenen yaşam', re: /ölüm hızı|yaşam süresi|intihar/i },
  { baslik: 'Ölüm nedenleri', ikon: HeartPulse, alt: 'Ölümlerin hangi hastalık gruplarından olduğu', re: /^ölümlerde/i },
  { baslik: 'Hizmet kapasitesi', ikon: Hospital, alt: 'Yatak, personel ve birim başına düşen nüfus', re: /yata[kğ]|hekim|hemşire|başına düşen nüfus/i },
  { baslik: 'Hizmet kullanımı', ikon: Stethoscope, alt: 'Başvuru, yatış ve 112 kullanımı', re: /müracaat|doluluk|kalış|ihbar/i, once: true },
];

const GostergelerSayfa: React.FC<{ kb: KarabukVeri }> = ({ kb }) => {
  const gruplar = useMemo(() => {
    const kalan = [...(kb.gostergeler || [])];
    const ata = new Map<string, typeof kalan>();
    for (const g of [...GOSTERGE_GRUPLARI].sort((a, b) => (a.once ? -1 : 0) - (b.once ? -1 : 0))) {
      const al = kalan.filter((x) => g.re.test(x.ad));
      al.forEach((x) => kalan.splice(kalan.indexOf(x), 1));
      ata.set(g.baslik, al);
    }
    const out = GOSTERGE_GRUPLARI.map((g) => ({ ...g, liste: ata.get(g.baslik) || [] }));
    if (kalan.length) out.push({ baslik: 'Diğer göstergeler', ikon: LineChart, alt: '', re: /./, liste: kalan });
    return out.filter((g) => g.liste.length);
  }, [kb.gostergeler]);
  return (
    <>
      <p className="sbk-yonerge">Her satırda büyük sayı <b>Karabük</b>, altındaki küçük sayı <b>Türkiye</b>. Saat simgesi iki serinin yıllara göre değerlerini açar; başlığa dokununca tanım ve not görünür.</p>
      {gruplar.map((g) => (
        <SatirBlok
          key={g.baslik} baslik={g.baslik} ikon={g.ikon} alt={g.alt}
          ogeler={g.liste.map((x) => ({
            ad: x.ad, deger: x.deger ?? null, birim: x.birim, alt: x.yil != null ? String(x.yil) : undefined, kaynak: x.kaynak, konum: x.konum, ek: x.ek_kaynaklar,
            seri: x.seri, tr: x.turkiye != null ? { deger: x.turkiye, seri: x.turkiye_seri } : undefined, tanim: x.tanim,
            detay: temiz<MaddeOge>([x.formul?.pay && `Formül: (${x.formul.pay}) / (${x.formul.payda})${x.formul.katsayi ? ` × ${sayi(x.formul.katsayi)}` : ''}`, x.not]),
          }))}
        />
      ))}
    </>
  );
};

/* ── Çevre ──────────────────────────────────────────────────────────────────────────────────────────────────── */

const CevreSayfa: React.FC<{ kb: KarabukVeri; bolumGit: (b: BolumId) => void }> = ({ kb, bolumGit }) => {
  const sim = (kb.kurum_sayilari || []).find((k) => /hava kalitesi/i.test(k.tur));
  const hava = temiz<SatirOge>([
    sim && kurumSatiri(sim),
    ...(kb.cevre || []).map<SatirOge>((c) => ({
      ad: c.baslik, deger: c.deger ?? undefined, birim: c.birim,
      alt: temiz<string>([c.istasyon && c.istasyon !== '–' && c.istasyon, c.yil != null && String(c.yil)]).join(' · ') || undefined,
      kaynak: c.kaynak, konum: c.konum, seri: c.seri, detay: temiz<MaddeOge>([c.aciklama]),
    })),
  ]);
  const is = (kb.is_sagligi || []).map<SatirOge>((c) => ({
    ad: c.ad, deger: c.deger, alt: c.yil != null ? String(c.yil) : undefined, kaynak: c.kaynak, konum: c.konum, seri: c.seri, detay: temiz<MaddeOge>([c.aciklama]),
  }));
  return (
    <>
      <SatirBlok
        baslik="Hava kalitesi" ikon={Wind} alt="Demir-çelik sanayisi kenti · PM10 yıllık sınır değeri 40 µg/m³ · satıra dokun: açıklama"
        ogeler={hava}
        arac={<button type="button" className="sbk-btn" onClick={() => bolumGit('cevre')}>Çevre ve sağlık <ArrowRight aria-hidden /></button>}
      />
      <SatirBlok baslik="İş sağlığı" ikon={HardHat} alt="SGK istatistikleri · satıra dokun: açıklama" ogeler={is} />
      {!hava.length && !is.length && <p className="sbk-bos">Bu sayfa için resmî kaynakta doğrulanmış veri bulunamadı.</p>}
    </>
  );
};

/* ── Programlar ve tarihçe ──────────────────────────────────────────────────────────────────────────────────── */

const ProgramlarSayfa: React.FC<{ kb: KarabukVeri }> = ({ kb }) => {
  const programlar = [...(kb.programlar || [])].sort((a, b) => String(b.tarih || '').localeCompare(String(a.tarih || '')));
  const tarihce = [...(kb.envanter?.tarihce || [])].sort((a, b) => String(a.yil).localeCompare(String(b.yil)));
  return (
    <>
      <SatirBlok
        baslik="İl sağlık müdürlüğü çalışmaları" ikon={CalendarClock} alt="Yeniden eskiye · başlığa dokun: ne yapıldı?"
        ogeler={programlar.map((p) => ({ ad: p.ad, alt: p.tarih ? (/^\d{4}-\d{2}-\d{2}$/.test(p.tarih) ? tarihTR(p.tarih) : p.tarih) : undefined, kaynak: p.kaynak, detay: p.aciklama.split(/(?<=\.)\s+(?=[A-ZÇĞİÖŞÜ])/).filter(Boolean) }))}
      />
      {tarihce.length > 0 && (
        <Blok baslik="Karabük sağlık örgütlenmesinin tarihçesi" ikon={History} maddeler={() => tarihce.map((x) => ({ metin: `**${x.yil}**: ${x.olay}`, kaynak: x.kaynak }))}>
          <ZamanCizgisi ogeler={tarihce.map((x) => ({ anahtar: `${x.yil}-${x.olay}`, zaman: x.yil, baslik: x.olay, kaynak: x.kaynak }))} />
        </Blok>
      )}
      {kb.universite?.aciklama && (
        <Blok
          baslik="Karabük Üniversitesi Tıp Fakültesi" ikon={GraduationCap}
          maddeler={() => kb.universite!.aciklama.split(/(?<=\.)\s+/).filter(Boolean).map((c, i) => (i === 0 ? { metin: c, kaynak: kb.universite!.kaynak, ek: kb.universite!.ek_kaynaklar } : c))}
        >
          <MiniMetin metin={kb.universite.aciklama.split(/(?<=\.)\s+(?=[A-ZÇĞİÖŞÜ])/).map((c) => `- ${c}`).join('\n')} />
          <p className="sbk-grafik-k">Kaynak <Atif id={kb.universite.kaynak} />{kb.universite.ek_kaynaklar?.map((x) => <Atif key={x} id={x} />)}</p>
        </Blok>
      )}
    </>
  );
};

/* ===============================================================================================================
 * Bölüm
 * =============================================================================================================== */

export const KarabukBolum: React.FC<{ v: { karabuk: KarabukVeri }; git: (b: BolumId) => void; alt?: string; altGit?: (id: string) => void }> = ({ v, git, alt, altGit }) => {
  const kb = v.karabuk;
  const [yerel, setYerel] = useState<KarabukSayfaId>(karabukSayfa(alt));
  const sec = altGit ? karabukSayfa(alt) : yerel;
  const sayfaGit = (id: KarabukSayfaId) => (altGit ? altGit(id) : setYerel(id));
  const tanim = KARABUK_SAYFALAR.find((s) => s.id === sec)!;
  if (!kb.nufus && !kb.kurum_sayilari?.length) return <p className="sbk-bos">Bu bölüm için resmî kaynakta doğrulanmış veri bulunamadı; sayı yazılmadı.</p>;
  return (
    <>
      <AltNav sec={sec} git={sayfaGit} />
      {sec !== 'ozet' && (
        <header className="sbk-alt-h">
          <h3>{tanim.ad}</h3>
          <p>{tanim.aciklama}</p>
        </header>
      )}
      {sec === 'ozet' && <OzetSayfa kb={kb} git={sayfaGit} />}
      {sec === 'kurumlar' && <KurumlarSayfa kb={kb} />}
      {sec === 'ilceler' && <IlcelerSayfa kb={kb} />}
      {sec === 'nufus' && <NufusSayfa kb={kb} />}
      {sec === 'gostergeler' && <GostergelerSayfa kb={kb} />}
      {sec === 'cevre' && <CevreSayfa kb={kb} bolumGit={git} />}
      {sec === 'programlar' && <ProgramlarSayfa kb={kb} />}
      <AltGecis sec={sec} git={sayfaGit} />
    </>
  );
};
