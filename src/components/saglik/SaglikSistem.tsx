import React, { useMemo, useState } from 'react';
import {
  Ambulance, Banknote, Building2, CalendarCheck, ChevronDown, ClipboardCheck, FileText, Gavel, Globe, HeartHandshake, Home, Landmark,
  Layers, MapPin, MessageSquare, Network, Plane, Route, Scale, Search, ShieldCheck, Smartphone, Stethoscope, UserRound, Users,
} from 'lucide-react';
import { Atif, Blok, Rozet, useGenislik } from './SaglikOrtak';
import type { MaddeOge } from './saglikBaglam';
import type { BolumProps } from './SaglikBolumler';
import { kucukHarf, type KMadde, type MevzuatOge } from './saglikVeri';

/**
 * Sağlık sistemi ve işleyişi · Anayasa ve mevzuat · Teşkilat ve denetim (src/data/saglik/mevzuat_teskilat.json).
 * Her madde resmî kaynağa (mevzuat.gov.tr, Resmî Gazete, saglik.gov.tr, SGK…) ve varsa madde numarasına (`konum`) bağlıdır.
 */

const mk = (m: KMadde): MaddeOge => ({ metin: `${m.metin}${m.konum ? ` (${m.konum})` : ''}`, kaynak: m.kaynak });

/** Madde + dayanak çipi ("md. 70/1-2") + atıf */
const DayanakliMadde: React.FC<{ m: KMadde }> = ({ m }) => (
  <>
    {m.metin}
    {m.konum && <span className="sbk-dayanak">{m.konum}</span>}
    <Atif id={m.kaynak} konum={m.konum} />
  </>
);

/** Sol liste + sağ ayrıntı; dar kapta açılır liste */
function Gezgin<T>({ ogeler, anahtar, baslik, ikon, ayrinti, etiket }: {
  ogeler: T[]; anahtar: (x: T) => string; baslik: (x: T) => React.ReactNode; ikon?: (x: T) => React.ElementType;
  ayrinti: (x: T) => React.ReactNode; etiket: string;
}) {
  const [ref, w] = useGenislik<HTMLDivElement>();
  const [sec, setSec] = useState<string | null>(ogeler[0] ? anahtar(ogeler[0]) : null);
  const dar = w > 0 && w < 760;
  const secili = ogeler.find((x) => anahtar(x) === sec);
  return (
    <div ref={ref} className={`sbk-gezgin ${dar ? 'is-dar' : ''}`}>
      <ul className="sbk-gezgin-l" role={dar ? undefined : 'tablist'} aria-label={etiket}>
        {ogeler.map((x) => {
          const k = anahtar(x);
          const Ic = ikon?.(x);
          const acik = k === sec;
          return (
            <li key={k} className={acik ? 'is-sec' : ''}>
              <button type="button" role={dar ? undefined : 'tab'} aria-selected={dar ? undefined : acik} aria-expanded={dar ? acik : undefined} onClick={() => setSec(dar && acik ? null : k)}>
                {Ic && <span className="sbk-gezgin-ic"><Ic aria-hidden /></span>}
                <span className="sbk-gezgin-t">{baslik(x)}</span>
                {dar && <ChevronDown aria-hidden className="sbk-gezgin-ok" />}
              </button>
              {dar && acik && <div className="sbk-gezgin-d">{ayrinti(x)}</div>}
            </li>
          );
        })}
      </ul>
      {!dar && secili && <div className="sbk-gezgin-d" role="tabpanel">{ayrinti(secili)}</div>}
    </div>
  );
}

/* =============================================================================================================== */
/* Sağlık sistemi ve işleyişi                                                                                       */
/* =============================================================================================================== */

const SISTEM_IKON: Record<string, React.ElementType> = {
  basamak: Layers, sevk: Route, aile: UserRound, gss: ShieldCheck, katilim: Banknote, sut: Banknote, mhrs: CalendarCheck, randevu: CalendarCheck,
  nabiz: Smartphone, '112': Ambulance, acil: Ambulance, evde: Home, turizm: Plane, finans: Banknote, rol: Network, kurum: Building2,
  hasta: HeartHandshake, basvuru: MessageSquare,
};
const sistemIkon = (id: string) => Object.entries(SISTEM_IKON).find(([k]) => id.toLowerCase().includes(k))?.[1] || Stethoscope;

export const SistemBolum: React.FC<BolumProps> = ({ v }) => {
  const b = v.mevzuat.sistem?.bolumler || [];
  if (!b.length) return <p className="sbk-bos">Bu sayfanın verisi bulunamadı.</p>;
  return (
    <Blok
      baslik="Türkiye'de sağlık sistemi nasıl işler?" ikon={Network} genis alt={`${b.length} başlık · başlığa dokun: özet ve yasal dayanağıyla maddeler`}
      maddeler={() => b.map((x) => ({ metin: `**${x.baslik}**${x.ozet ? ` — ${x.ozet}` : ''}`, alt: (x.maddeler || []).map(mk) }))}
    >
      <Gezgin
        etiket="Sağlık sistemi başlıkları" ogeler={b} anahtar={(x) => x.id} ikon={(x) => sistemIkon(x.id)}
        baslik={(x) => x.baslik}
        ayrinti={(x) => (
          <>
            <h4>{x.baslik}</h4>
            {x.ozet && <p className="sbk-gezgin-ozet">{x.ozet}</p>}
            <ul className="sbk-madde sbk-madde-genis">{(x.maddeler || []).map((m, i) => <li key={i}><DayanakliMadde m={m} /></li>)}</ul>
          </>
        )}
      />
    </Blok>
  );
};

/* =============================================================================================================== */
/* Anayasa ve mevzuat                                                                                               */
/* =============================================================================================================== */

const durumTon = (d?: string): 'ok' | 'warn' | 'bad' | 'nötr' => (!d ? 'nötr' : /mülga|yürürlükten kalk|iptal/i.test(d) && !/yürürlükte/i.test(d.split(/[;(]/)[0]) ? 'bad' : /değiş|kısmen|mülga/i.test(d) ? 'warn' : /yürürlükte/i.test(d) ? 'ok' : 'nötr');

type MevzuatTur = 'kanunlar' | 'kararnameler' | 'yonetmelikler';
const MEVZUAT_TUR: { id: MevzuatTur; ad: string }[] = [
  { id: 'kanunlar', ad: 'Kanunlar' }, { id: 'kararnameler', ad: 'Kararnameler' }, { id: 'yonetmelikler', ad: 'Yönetmelik ve genelgeler' },
];

const MevzuatKarti: React.FC<{ x: MevzuatOge; acik: boolean; onAc: () => void }> = ({ x, acik, onAc }) => (
  <li className={`sbk-mevzuat-k ${acik ? 'is-acik' : ''}`}>
    <button type="button" onClick={onAc} aria-expanded={acik}>
      {x.no && <span className="sbk-mevzuat-no">{x.no}</span>}
      <span className="sbk-mevzuat-t">
        <b>{x.ad}</b>
        <small>{[x.tarih, x.rg && `RG ${x.rg}`].filter(Boolean).join(' · ')}</small>
      </span>
      {x.durum && <Rozet ton={durumTon(x.durum)}>{x.durum.split(/[;(]/)[0].trim()}</Rozet>}
      <ChevronDown aria-hidden className="sbk-gezgin-ok" />
    </button>
    {acik && (
      <div className="sbk-mevzuat-d">
        {x.durum && x.durum.length > 30 && <p className="sbk-muted">Durum: {x.durum}</p>}
        {x.ozet && <p>{x.ozet}</p>}
        <ul className="sbk-madde sbk-madde-genis">{(x.maddeler || []).map((m, i) => <li key={i}><DayanakliMadde m={m} /></li>)}</ul>
        {x.ders && <p className="sbk-mevzuat-ders"><b>Derste:</b> {x.ders}</p>}
        <p className="sbk-grafik-k">Kaynak <Atif id={x.kaynak} /></p>
      </div>
    )}
  </li>
);

export const MevzuatBolum: React.FC<BolumProps> = ({ v }) => {
  const m = v.mevzuat.mevzuat;
  const [hSec, setHSec] = useState(0);
  const [tur, setTur] = useState<MevzuatTur>('kanunlar');
  const [q, setQ] = useState('');
  const [acik, setAcik] = useState<string | null>(null);
  const [aq, setAq] = useState('');
  const liste = useMemo(() => {
    const l = (m?.[tur] || []) as MevzuatOge[];
    const k = kucukHarf(q.trim());
    return k ? l.filter((x) => kucukHarf([x.no, x.ad, x.ders, ...(x.maddeler || []).map((y) => y.metin)].join(' ')).includes(k)) : l;
  }, [m, tur, q]);
  const anayasa = useMemo(() => {
    const k = kucukHarf(aq.trim());
    return (m?.anayasa || []).filter((x) => !k || kucukHarf(`${x.madde} ${x.baslik} ${x.ozet}`).includes(k));
  }, [m, aq]);
  if (!m) return <p className="sbk-bos">Bu sayfanın verisi bulunamadı.</p>;
  const hiy = m.hiyerarsi || [];
  const hs = hiy[hSec];
  return (
    <>
      {hiy.length > 0 && (
        <Blok baslik="Normlar hiyerarşisi" ikon={Layers} alt="Üstteki normu alttaki değiştiremez · düzeye dokun" genis maddeler={() => hiy.map((x, i) => ({ metin: `**${i + 1}. ${x.duzey}**: ${x.aciklama || ''}`, kaynak: x.kaynak }))}>
          <div className="sbk-piramit">
            <div className="sbk-piramit-g" role="tablist" aria-label="Normlar hiyerarşisi">
              {hiy.map((x, i) => (
                <button key={x.duzey} type="button" role="tab" aria-selected={i === hSec} className={i === hSec ? 'is-sec' : ''} style={{ width: `${Math.min(100, 44 + i * (56 / Math.max(1, hiy.length - 1)))}%` }} onClick={() => setHSec(i)}>
                  {x.duzey}
                </button>
              ))}
            </div>
            {hs && <div className="sbk-piramit-d" role="tabpanel"><h4>{hs.duzey}<Atif id={hs.kaynak} /></h4><p>{hs.aciklama}</p></div>}
          </div>
        </Blok>
      )}

      {(m.anayasa?.length || 0) > 0 && (
        <Blok
          baslik="Anayasa'da sağlık" ikon={Scale} alt={`${m.anayasa!.length} madde · sağlık hakkının anayasal dayanağı`} genis
          maddeler={() => m.anayasa!.map((x) => ({ metin: `**Md. ${x.madde} — ${x.baslik || ''}**: ${x.ozet || ''}`, kaynak: x.kaynak, alt: x.alinti ? [`“${x.alinti}”`] : undefined }))}
        >
          <label className="sbk-ara sbk-ara-blok"><Search aria-hidden /><input type="search" value={aq} onChange={(e) => setAq(e.target.value)} placeholder="Madde ara (ör. 56, sağlık, sosyal güvenlik)" aria-label="Anayasa maddelerinde ara" /></label>
          <div className="sbk-anayasa-g">
            {anayasa.map((x) => (
              <article key={x.madde} className={`sbk-anayasa-k ${/^(56|17|60)$/.test(x.madde) ? 'is-ana' : ''}`}>
                <header><span className="sbk-mevzuat-no">Md. {x.madde}</span><h4>{x.baslik}</h4></header>
                {x.ozet && <p>{x.ozet}</p>}
                {x.alinti && <blockquote>{x.alinti}</blockquote>}
                <p className="sbk-grafik-k"><Atif id={x.kaynak} konum={`md. ${x.madde}`} /></p>
              </article>
            ))}
          </div>
        </Blok>
      )}

      <Blok
        baslik="Kanunlar, kararnameler ve yönetmelikler" ikon={Gavel} genis alt="Türü seç, ara; satıra dokun: ne düzenler, hangi maddede, derste nerede"
        maddeler={() => MEVZUAT_TUR.map((t) => ({ metin: `**${t.ad}**`, alt: ((m[t.id] || []) as MevzuatOge[]).map((x) => ({ metin: `**${x.no ? `${x.no} — ` : ''}${x.ad}** (${[x.tarih, x.durum].filter(Boolean).join('; ')})`, kaynak: x.kaynak, alt: (x.maddeler || []).map(mk) })) }))}
      >
        <div className="sbk-bildirim-arac">
          <div className="sbk-seg" role="radiogroup" aria-label="Mevzuat türü">
            {MEVZUAT_TUR.map((t) => (
              <button key={t.id} type="button" role="radio" aria-checked={tur === t.id} className={tur === t.id ? 'is-sec' : ''} onClick={() => { setTur(t.id); setAcik(null); }}>
                {t.ad} <small>{(m[t.id] || []).length}</small>
              </button>
            ))}
          </div>
          <label className="sbk-ara"><Search aria-hidden /><input type="search" value={q} onChange={(e) => setQ(e.target.value)} placeholder="Ara (ör. 224, aile hekimliği, sevk)" aria-label="Mevzuatta ara" /></label>
        </div>
        <ul className="sbk-mevzuat-l">
          {liste.map((x) => { const k = `${x.no || ''}-${x.ad}`; return <MevzuatKarti key={k} x={x} acik={acik === k} onAc={() => setAcik(acik === k ? null : k)} />; })}
          {!liste.length && <li className="sbk-muted">"{q}" bulunamadı.</li>}
        </ul>
      </Blok>
    </>
  );
};

/* =============================================================================================================== */
/* Teşkilat ve denetim                                                                                              */
/* =============================================================================================================== */

const TUR_TON: Record<string, 'accent' | 'ok' | 'warn' | 'bad' | 'ai' | 'clinic'> = {
  'bakanlık içi': 'accent', idari: 'clinic', mali: 'warn', siyasi: 'ai', yargısal: 'bad', meslek: 'ok',
};

const BirimKartlari: React.FC<{ birimler: { birim: string; gorev?: string[]; alt_birimler?: string[]; aciklama?: string; kaynak?: string }[]; ikon: React.ElementType }> = ({ birimler, ikon: Ic }) => {
  const [acik, setAcik] = useState<string | null>(null);
  return (
    <ul className="sbk-birim-g">
      {birimler.map((b) => {
        const ac = acik === b.birim;
        const icerikVar = (b.gorev?.length || 0) > 0 || (b.alt_birimler?.length || 0) > 0 || !!b.aciklama;
        return (
          <li key={b.birim} className={ac ? 'is-acik' : ''}>
            <button type="button" onClick={() => setAcik(ac ? null : b.birim)} aria-expanded={ac} disabled={!icerikVar}>
              <span className="sbk-gezgin-ic"><Ic aria-hidden /></span>
              <span className="sbk-gezgin-t">{b.birim}</span>
              {icerikVar && <ChevronDown aria-hidden className="sbk-gezgin-ok" />}
            </button>
            {ac && (
              <div className="sbk-birim-d">
                {b.aciklama && <p>{b.aciklama}</p>}
                {(b.gorev?.length || 0) > 0 && <ul className="sbk-madde">{b.gorev!.map((g, i) => <li key={i}>{g}</li>)}</ul>}
                {(b.alt_birimler?.length || 0) > 0 && <><h5>Alt birimler</h5><div className="sbk-etiketler">{b.alt_birimler!.map((a) => <Rozet key={a}>{a}</Rozet>)}</div></>}
                <p className="sbk-grafik-k"><Atif id={b.kaynak} /></p>
              </div>
            )}
          </li>
        );
      })}
    </ul>
  );
};

const mBirim = (b: { birim: string; gorev?: string[]; alt_birimler?: string[]; aciklama?: string; kaynak?: string }): MaddeOge => ({
  metin: `**${b.birim}**${b.aciklama ? `: ${b.aciklama}` : ''}`, kaynak: b.kaynak,
  alt: [...(b.gorev || []), ...(b.alt_birimler?.length ? [`Alt birimler: ${b.alt_birimler.join(', ')}`] : [])],
});

export const TeskilatBolum: React.FC<BolumProps> = ({ v }) => {
  const t = v.mevzuat.teskilat;
  const d = v.mevzuat.denetim || [];
  const [tur, setTur] = useState('');
  const turler = [...new Set(d.map((x) => x.tur || 'diğer'))];
  const dListe = d.filter((x) => !tur || (x.tur || 'diğer') === tur);
  if (!t && !d.length) return <p className="sbk-bos">Bu sayfanın verisi bulunamadı.</p>;
  return (
    <>
      {(t?.merkez?.length || 0) > 0 && (
        <Blok baslik="Sağlık Bakanlığı merkez teşkilatı" ikon={Landmark} alt="1 sayılı Cumhurbaşkanlığı Kararnamesi · birime dokun: görevleri" genis maddeler={() => t!.merkez!.map(mBirim)}>
          <BirimKartlari birimler={t!.merkez!} ikon={Building2} />
        </Blok>
      )}
      <div className="sbk-iki-sutun">
        {(t?.bagli?.length || 0) > 0 && (
          <Blok baslik="Bağlı ve ilgili kuruluşlar" ikon={Network} maddeler={() => t!.bagli!.map(mBirim)}>
            <BirimKartlari birimler={t!.bagli!} ikon={Network} />
          </Blok>
        )}
        {(t?.tasra?.length || 0) > 0 && (
          <Blok baslik="Taşra teşkilatı: il ve ilçe sağlık müdürlükleri" ikon={MapPin} maddeler={() => t!.tasra!.map(mBirim)}>
            <BirimKartlari birimler={t!.tasra!} ikon={MapPin} />
          </Blok>
        )}
      </div>
      {(t?.halk_sagligi_birimleri?.length || 0) > 0 && (
        <Blok baslik="Halk sağlığı birimleri" ikon={Users} alt="ASM, Sağlıklı Hayat Merkezi, KETEM, Verem Savaş Dispanseri, Halk Sağlığı Laboratuvarı…" genis maddeler={() => t!.halk_sagligi_birimleri!.map(mBirim)}>
          <BirimKartlari birimler={t!.halk_sagligi_birimleri!} ikon={Stethoscope} />
        </Blok>
      )}
      {(t?.karabuk?.length || 0) > 0 && (
        <Blok baslik="Karabük İl Sağlık Müdürlüğü teşkilatı" ikon={MapPin} maddeler={() => t!.karabuk!.map(mBirim)}>
          <BirimKartlari birimler={t!.karabuk!} ikon={Building2} />
        </Blok>
      )}
      {d.length > 0 && (
        <Blok
          baslik="Sağlık kuruluşlarını kim denetler?" ikon={ClipboardCheck} genis alt="Denetimin türüne göre süz · karta dokun: neyi, hangi dayanakla, nasıl"
          maddeler={() => d.map((x) => ({ metin: `**${x.kurum}** (${x.tur || 'diğer'})`, kaynak: x.kaynak, alt: [x.neyi && `**Neyi denetler**: ${x.neyi}`, x.dayanak && `**Dayanak**: ${x.dayanak}`, ...(x.nasil || []).map((n) => `**Nasıl**: ${n}`)].filter(Boolean) as string[] }))}
        >
          <div className="sbk-cip-l" role="radiogroup" aria-label="Denetim türü">
            <button type="button" role="radio" aria-checked={!tur} className={`sbk-cip ${!tur ? 'is-sec' : ''}`} onClick={() => setTur('')}>Tümü ({d.length})</button>
            {turler.map((x) => <button key={x} type="button" role="radio" aria-checked={tur === x} className={`sbk-cip ${tur === x ? 'is-sec' : ''}`} onClick={() => setTur(x)}>{x} ({d.filter((y) => (y.tur || 'diğer') === x).length})</button>)}
          </div>
          <div className="sbk-denetim-g">
            {dListe.map((x) => (
              <article key={x.kurum} className="sbk-denetim-k">
                <header><Rozet ton={TUR_TON[x.tur || ''] || 'nötr'}>{x.tur || 'diğer'}</Rozet><h4>{x.kurum}<Atif id={x.kaynak} /></h4></header>
                {x.neyi && <p><b>Neyi denetler?</b> {x.neyi}</p>}
                {x.dayanak && <p className="sbk-muted"><FileText aria-hidden /> {x.dayanak}</p>}
                {(x.nasil?.length || 0) > 0 && <ul className="sbk-madde">{x.nasil!.map((n, i) => <li key={i}>{n}</li>)}</ul>}
              </article>
            ))}
          </div>
        </Blok>
      )}
      <p className="sbk-not sbk-muted"><Globe aria-hidden className="sbk-satir-ikon" /> Mevzuat metinleri mevzuat.gov.tr'deki güncel hâlinden; mülga ya da değişik hükümler ayrıca belirtildi.</p>
    </>
  );
};
