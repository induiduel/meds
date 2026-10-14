import React, { useState } from 'react';
import {
  Apple, ArrowRight, Baby, BookOpenCheck, ChevronDown, Droplets, Eye, EyeOff, Flag, GraduationCap, HeartPulse, History, Lightbulb, ListChecks,
  Quote, Shield, Sprout, Stethoscope, Syringe, Target, Users,
} from 'lucide-react';
import { Atif, Blok, IcBag, OkunurTablo, Rozet, SlaytBag } from './SaglikOrtak';
import { pathFor } from '../../router';
import type { MaddeOge } from './saglikBaglam';
import type { BolumProps } from './SaglikBolumler';
import type { KMadde } from './saglikVeri';

/**
 * Kavram sayfaları (Halk sağlığı kavramı · Sağlığın geliştirilmesi · Koruyucu yaklaşım). İçerik YALNIZ ders notu /
 * özet / Öğren destesinden (kaynak türü "ders", slayt bağlantılı) ve Türkiye'deki karşılığı resmî kaynaktan gelir
 * (src/data/saglik/kavramlar.json; derleme: docs/SAGLIK_BAKANLIGI_PLANI.md 2. tur).
 */

type Esnek = KMadde | string | { ilke?: string; aciklama?: string; grup?: string; metin?: string; kaynak?: string; slayt?: number | number[] | null; maddeler?: string[]; tur?: string };
const metinOf = (x: Esnek): string => (typeof x === 'string' ? x : (x as { metin?: string }).metin || (x as { ilke?: string }).ilke || '');
const kaynakOf = (x: Esnek) => (typeof x === 'string' ? undefined : (x as { kaynak?: string }).kaynak);
const slaytOf = (x: Esnek): unknown => (typeof x === 'string' ? undefined : (x as { slayt?: unknown }).slayt ?? undefined);

/** Madde (kaynak + slayt bağlantılı) */
const KaynakliMadde: React.FC<{ x: Esnek }> = ({ x }) => (
  <>
    <MiniSatir metin={metinOf(x)} />
    <Atif id={kaynakOf(x)} />
    <SlaytBag kaynak={kaynakOf(x)} slayt={slaytOf(x)} />
  </>
);
const MiniSatir: React.FC<{ metin: string }> = ({ metin }) => (
  <>{metin.split(/(\*\*[^*]+\*\*)/g).map((p, i) => (p.startsWith('**') && p.endsWith('**') ? <strong key={i}>{p.slice(2, -2)}</strong> : <React.Fragment key={i}>{p}</React.Fragment>))}</>
);
const mk = (x: Esnek): MaddeOge => ({ metin: metinOf(x), kaynak: kaynakOf(x) });

/** Ezber modu düğmesi (içeriği gizler; dokununca açılır) */
const EzberDugme: React.FC<{ acik: boolean; onClick: () => void }> = ({ acik, onClick }) => (
  <button type="button" className={`sbk-btn ${acik ? 'is-dolu' : ''}`} onClick={onClick} aria-pressed={acik}>
    {acik ? <EyeOff aria-hidden /> : <Eye aria-hidden />} {acik ? 'Ezber açık' : 'Kendini dene'}
  </button>
);

/* =============================================================================================================== */
/* Halk sağlığı kavramı                                                                                             */
/* =============================================================================================================== */

export const KavramBolum: React.FC<BolumProps> = ({ v, git }) => {
  const k = v.kavramlar.kavram;
  const [ezber, setEzber] = useState(false);
  const [acilan, setAcilan] = useState<Set<number>>(() => new Set());
  const [aaAcik, setAaAcik] = useState<string | null>(null);
  if (!k) return <p className="sbk-bos">Kavram verisi yüklenemedi.</p>;
  const ef = k.etkileyen_faktorler;
  const efx = (ef || {}) as { not?: string; belirleyiciler_k5?: { maddeler?: string[]; kaynak?: string } };
  return (
    <>
      {(k.tanimlar?.length || 0) > 0 && (
        <Blok baslik="Halk sağlığı nedir?" ikon={Quote} alt="Ders notundaki tanımlar" genis maddeler={() => k.tanimlar!.map((t) => ({ metin: `**${t.baslik}**: ${t.metin}`, kaynak: t.kaynak }))}>
          <div className="sbk-tanim-g">
            {k.tanimlar!.map((t) => (
              <figure key={t.baslik} className="sbk-tanim-k">
                <figcaption>{t.baslik}</figcaption>
                <blockquote><MiniSatir metin={t.metin} /></blockquote>
                <p className="sbk-grafik-k"><Atif id={t.kaynak} /><SlaytBag kaynak={t.kaynak} slayt={t.slayt} /></p>
              </figure>
            ))}
          </div>
        </Blok>
      )}

      {(k.ilkeler?.length || 0) > 0 && (
        <Blok
          baslik={`Halk sağlığının ${k.ilkeler!.length} temel ilkesi`} ikon={ListChecks} genis
          alt="Her ilke: ne demek, örnek · Kendini dene: ilke adları gizlenir, numaraya dokunarak aç"
          arac={<EzberDugme acik={ezber} onClick={() => { setEzber((x) => !x); setAcilan(new Set()); }} />}
          maddeler={() => k.ilkeler!.map((i) => ({ metin: `**${i.no}. ${i.ilke}**`, kaynak: i.kaynak, alt: [i.ne_demek, i.ornek && `**Örnek**: ${i.ornek}`].filter(Boolean) as string[] }))}
        >
          <ol className="sbk-ilke-g">
            {k.ilkeler!.map((i) => {
              const gizli = ezber && !acilan.has(i.no);
              return (
                <li key={i.no} className={gizli ? 'is-gizli' : ''}>
                  <span className="sbk-ilke-no">{i.no}</span>
                  {gizli ? (
                    <button type="button" className="sbk-ilke-ac" onClick={() => setAcilan((s) => new Set(s).add(i.no))}>İlkeyi hatırla, sonra dokun</button>
                  ) : (
                    <div>
                      <h4>{i.ilke}<Atif id={i.kaynak} /><SlaytBag kaynak={i.kaynak} slayt={i.slayt} /></h4>
                      {i.ne_demek && <p>{i.ne_demek}</p>}
                      {i.ornek && <p className="sbk-ilke-ornek"><b>Örnek:</b> {i.ornek}</p>}
                    </div>
                  )}
                </li>
              );
            })}
          </ol>
        </Blok>
      )}

      {(k.gunumuz_anlayisi?.length || 0) > 0 && (
        <Blok
          baslik="Günümüzde halk sağlığı anlayışı" ikon={Lightbulb} alt="1978 Alma-Ata Bildirgesi ile tanımlanan ilkeler · ilkeye dokun: açıklaması" genis
          maddeler={() => k.gunumuz_anlayisi!.map((g) => ({ metin: `**${g.ilke}**${g.aciklama ? `: ${g.aciklama}` : ''}`, kaynak: g.kaynak }))}
        >
          <div className="sbk-cip-l sbk-aa-cipler" role="list">
            {k.gunumuz_anlayisi!.map((g) => (
              <button key={g.ilke} type="button" role="listitem" className={`sbk-cip ${aaAcik === g.ilke ? 'is-sec' : ''}`} onClick={() => setAaAcik(aaAcik === g.ilke ? null : g.ilke)} aria-expanded={aaAcik === g.ilke}>
                {g.ilke}
              </button>
            ))}
          </div>
          {aaAcik && (() => { const g = k.gunumuz_anlayisi!.find((x) => x.ilke === aaAcik)!; return (
            <div className="sbk-aa-detay" role="status"><h4>{g.ilke}</h4><p>{g.aciklama || 'Ders notunda yalnız adıyla geçer.'} <Atif id={g.kaynak} /><SlaytBag kaynak={g.kaynak} slayt={g.slayt} /></p></div>
          ); })()}
          {!aaAcik && <p className="sbk-muted sbk-not">Bir ilke seç: açıklaması burada açılır.</p>}
        </Blok>
      )}

      <div className="sbk-iki-sutun">
        {(k.sosyal_hekimlik?.length || 0) > 0 && (
          <Blok baslik="Sosyal hekimlik (Grotjahn)" ikon={Users} maddeler={() => (k.sosyal_hekimlik as Esnek[]).map(mk)}>
            <ul className="sbk-madde">{(k.sosyal_hekimlik as Esnek[]).map((x, i) => <li key={i}><KaynakliMadde x={x} /></li>)}</ul>
          </Blok>
        )}
        {(k.uzmanlik_gorevleri?.length || 0) > 0 && (
          <Blok baslik="Uzmanlık dalı olarak halk sağlığı" ikon={Stethoscope} maddeler={() => (k.uzmanlik_gorevleri as Esnek[]).map((x) => ({ ...(mk(x) as object), metin: `${(x as { grup?: string }).grup ? `**${(x as { grup?: string }).grup}**: ` : ''}${metinOf(x)}` } as MaddeOge))}>
            <ul className="sbk-madde">{(k.uzmanlik_gorevleri as Esnek[]).map((x, i) => <li key={i}>{(x as { grup?: string }).grup && <b>{(x as { grup?: string }).grup}: </b>}<KaynakliMadde x={x} /></li>)}</ul>
          </Blok>
        )}
      </div>

      {ef && (ef.gecmis?.length || ef.gunumuz?.length) ? (
        <Blok
          baslik="Sağlığı etkileyen faktörler: geçmişte ve günümüzde" ikon={History} alt="Sınavda sık karıştırılır: hangi faktör geçmişte, hangisi günümüzde?" genis
          maddeler={() => [
            { metin: '**Geçmişte**', kaynak: ef.kaynak, alt: ef.gecmis || [] }, { metin: '**Günümüzde**', alt: ef.gunumuz || [] },
            ...(efx.not ? [`**Sınav tuzağı**: ${efx.not.replace(/^Sınav tuzağı:\s*/, '')}`] : []),
            ...(efx.belirleyiciler_k5?.maddeler?.length ? [{ metin: '**Sağlığın belirleyicileri (Kurul 5)**', kaynak: efx.belirleyiciler_k5.kaynak, alt: efx.belirleyiciler_k5.maddeler } as MaddeOge] : []),
          ]}
        >
          <div className="sbk-dun-bugun">
            <section><h4>Geçmişte</h4><ul>{(ef.gecmis || []).map((x) => <li key={x}>{x}</li>)}</ul></section>
            <ArrowRight aria-hidden className="sbk-dun-ok" />
            <section className="is-bugun"><h4>Günümüzde</h4><ul>{(ef.gunumuz || []).map((x) => <li key={x}>{x}</li>)}</ul></section>
          </div>
          {efx.not && <p className="sbk-vurgu sbk-vurgu-ince"><Lightbulb aria-hidden /> {efx.not}</p>}
          <p className="sbk-grafik-k">Kaynak <Atif id={ef.kaynak} /><SlaytBag kaynak={ef.kaynak} slayt={ef.slayt} /></p>
          {(efx.belirleyiciler_k5?.maddeler?.length || 0) > 0 && (
            <div className="sbk-ust-bosluk">
              <h4 className="sbk-alt-baslik">Sağlığın belirleyicileri (Kurul 5)</h4>
              <ul className="sbk-madde">{efx.belirleyiciler_k5!.maddeler!.map((m) => <li key={m}><MiniSatir metin={m} /></li>)}</ul>
              <p className="sbk-grafik-k"><Atif id={efx.belirleyiciler_k5!.kaynak} /></p>
            </div>
          )}
        </Blok>
      ) : null}

      {(k.tsh_ilkeleri?.length || 0) > 0 && (
        <Blok
          baslik="Temel sağlık hizmetleri ve sosyalleştirme" ikon={Flag} alt="224 sayılı kanunun ilkeleri ve TSH'nin anlamları" genis
          maddeler={() => (k.tsh_ilkeleri as Esnek[]).map((g) => ({ metin: `**${(g as { grup?: string }).grup || metinOf(g)}**`, kaynak: kaynakOf(g), alt: (g as { maddeler?: string[] }).maddeler || [] }))}
        >
          <AcilirGruplar gruplar={(k.tsh_ilkeleri as Esnek[]).map((g) => ({ baslik: (g as { grup?: string }).grup || metinOf(g), maddeler: (g as { maddeler?: string[] }).maddeler || [], kaynak: kaynakOf(g), slayt: slaytOf(g) }))} />
          <button type="button" className="sbk-btn sbk-ust-bosluk" onClick={() => git('kurumlar')}>Sağlık kurumları ve basamaklar <ArrowRight aria-hidden /></button>
        </Blok>
      )}

      <SinavKutusu v={v} konular={/ilke|faktör|tarihçe|sosyalleştirme|tsh|aile hekim/i} />
    </>
  );
};

/** Açılır başlık grupları (ilk grup açık) */
const AcilirGruplar: React.FC<{ gruplar: { baslik: string; maddeler: string[]; kaynak?: string; slayt?: unknown }[] }> = ({ gruplar }) => {
  const [acik, setAcik] = useState<number | null>(0);
  return (
    <div className="sbk-acilir-g">
      {gruplar.map((g, i) => (
        <section key={g.baslik} className={acik === i ? 'is-acik' : ''}>
          <button type="button" onClick={() => setAcik(acik === i ? null : i)} aria-expanded={acik === i}>
            <span>{g.baslik}</span><small>{g.maddeler.length}</small><ChevronDown aria-hidden />
          </button>
          {acik === i && (
            <div>
              <ul className="sbk-madde">{g.maddeler.map((m, j) => <li key={j}><MiniSatir metin={m} /></li>)}</ul>
              <p className="sbk-grafik-k"><Atif id={g.kaynak} /><SlaytBag kaynak={g.kaynak} slayt={g.slayt} /></p>
            </div>
          )}
        </section>
      ))}
    </div>
  );
};

/** Bu kavramlardan çıkmış sorular (kavramlar.json › sinav) */
const SinavKutusu: React.FC<{ v: BolumProps['v']; konular: RegExp }> = ({ v, konular }) => {
  const liste = (v.kavramlar.sinav || []).filter((s) => konular.test(s.konu));
  if (!liste.length) return null;
  return (
    <Blok baslik="Sınavda bu konulardan sorulanlar" ikon={GraduationCap} alt="Soruya dokun: çıkmış sorularda açılır" maddeler={() => liste.map((s) => `**${s.konu}**: ${s.ozet}`)}>
      <ul className="sbk-sinav-l">
        {liste.map((s) => (
          <li key={s.soru_id}>
            <IcBag to={`${pathFor('past_exams')}/${encodeURIComponent(s.soru_id)}`} className="sbk-sinav-a">
              <Rozet ton="clinic">{s.konu}</Rozet>
              <span>{s.ozet}</span>
              <ArrowRight aria-hidden />
            </IcBag>
          </li>
        ))}
      </ul>
    </Blok>
  );
};

/* =============================================================================================================== */
/* Sağlığın geliştirilmesi                                                                                          */
/* =============================================================================================================== */

const BILESEN_IKON: Record<string, React.ElementType> = {
  'guvenilir-cevre': Droplets,
  'bagisikligin-artirilmasi': Syringe,
  'olumlu-saglik-davranisi': HeartPulse,
  'saglikli-beslenme': Apple,
  'saglikli-dogum': Baby,
  'surekli-saglik-bakimi': Stethoscope,
};
const bilesenIkon = (id: string): React.ElementType => BILESEN_IKON[id] || Object.entries(BILESEN_IKON).find(([k]) => id.includes(k.split('-')[0]))?.[1] || Sprout;

const DUZEY_AD: Record<string, string> = { primordial: 'Primordial', birincil: 'Birincil', ikincil: 'İkincil', ucuncul: 'Üçüncül' };

export const GelistirmeBolum: React.FC<BolumProps> = ({ v, git }) => {
  const g = v.kavramlar.gelistirme as NonNullable<BolumProps['v']['kavramlar']['gelistirme']> & {
    ottawa?: { metin?: string; eylem_alanlari?: string[]; kaynak?: string };
    konferanslar?: { maddeler?: string[]; kaynak?: string };
    ortaya_cikis_faktorleri?: { maddeler?: string[]; kaynak?: string };
    stratejiler?: { maddeler?: string[]; kaynak?: string };
    etkiler?: { kisa_donem?: string[]; orta_donem?: string[]; uzun_donem?: string[]; kaynak?: string };
    bilesenler_baslik?: { metin?: string; kaynak?: string; slayt?: number | number[] };
    tanim?: KMadde & { ottawa_tanimi?: string };
  };
  const bilesenler = g?.bilesenler || [];
  const [sec, setSec] = useState(bilesenler[0]?.id || '');
  const [ezber, setEzber] = useState(false);
  const [gor, setGor] = useState<Set<string>>(() => new Set());
  if (!g) return <p className="sbk-bos">Veri yüklenemedi.</p>;
  const b = bilesenler.find((x) => x.id === sec) || bilesenler[0];
  const bAlt = (b as unknown as { alt_maddeler?: string[] } | undefined)?.alt_maddeler;
  const gizli = !!b && ezber && !gor.has(b.id);
  return (
    <>
      {(g.tanim || (g.vurgu?.length || 0) > 0) && (
        <Blok
          baslik="Sağlığın geliştirilmesi nedir?" ikon={Sprout} genis
          maddeler={() => [
            ...(g.tanim ? [mk(g.tanim)] : []),
            ...(g.tanim?.ottawa_tanimi ? [{ metin: `**Ottawa tanımı**: ${g.tanim.ottawa_tanimi}`, kaynak: g.tanim.kaynak } as MaddeOge] : []),
            ...(g.vurgu || []).map(mk),
          ]}
        >
          <div className="sbk-tanim-g">
            {g.tanim && <figure className="sbk-tanim-k"><figcaption>Tanım</figcaption><blockquote>{g.tanim.metin}</blockquote><p className="sbk-grafik-k"><Atif id={g.tanim.kaynak} /></p></figure>}
            {g.tanim?.ottawa_tanimi && <figure className="sbk-tanim-k"><figcaption>Ottawa Sözleşmesi'ne göre</figcaption><blockquote>{g.tanim.ottawa_tanimi}</blockquote><p className="sbk-grafik-k"><Atif id={g.tanim.kaynak} /></p></figure>}
          </div>
          {(g.vurgu?.length || 0) > 0 && (
            <div className="sbk-vurgu">
              <h4><Lightbulb aria-hidden /> Neden "korumak" değil de "geliştirmek"?</h4>
              <ul className="sbk-madde">{g.vurgu!.map((x, i) => <li key={i}><KaynakliMadde x={x} /></li>)}</ul>
            </div>
          )}
        </Blok>
      )}

      {bilesenler.length > 0 && b && (
        <Blok
          baslik={g.bilesenler_baslik?.metin || 'Sağlığın geliştirilmesinin bileşenleri'} ikon={Target} genis
          alt="Her bileşen beş soruyla: Ne demek? · Neden önemli? · Örnek? · Türkiye'de nasıl? · Hangi korunma düzeyi?"
          arac={<EzberDugme acik={ezber} onClick={() => { setEzber((x) => !x); setGor(new Set()); }} />}
          maddeler={() => bilesenler.map((x) => ({
            metin: `**${(x as unknown as { no?: number }).no ?? ''}. ${x.ad}**`, kaynak: x.kaynak,
            alt: [
              ...((x as unknown as { alt_maddeler?: string[] }).alt_maddeler || []).map((m) => `**Kapsam**: ${m}`),
              x.ne_demek && `**Ne demek**: ${x.ne_demek}`,
              x.neden_onemli && `**Neden önemli**: ${x.neden_onemli}`,
              ...(x.ornekler || []).map((o) => `**Örnek**: ${o}`),
              ...(x.turkiyede || []).map((t) => ({ metin: `**Türkiye'de**: ${t.metin}`, kaynak: t.kaynak } as MaddeOge)),
              x.koruma_duzeyi && `**Korunma düzeyi**: ${DUZEY_AD[x.koruma_duzeyi] || x.koruma_duzeyi}`,
            ].filter(Boolean) as MaddeOge[],
          }))}
        >
          <div className="sbk-bilesen">
            <ol className="sbk-bilesen-l" role="tablist" aria-label="Bileşenler">
              {bilesenler.map((x) => {
                const Ic = bilesenIkon(x.id);
                return (
                  <li key={x.id}>
                    <button type="button" role="tab" aria-selected={x.id === b.id} className={x.id === b.id ? 'is-sec' : ''} onClick={() => setSec(x.id)}>
                      <span className="sbk-bilesen-ic"><Ic aria-hidden /></span>
                      <span><small>{(x as unknown as { no?: number }).no}</small>{x.ad}</span>
                    </button>
                  </li>
                );
              })}
            </ol>
            <div className="sbk-bilesen-d" role="tabpanel">
              <h4>{b.ad}<Atif id={b.kaynak} /><SlaytBag kaynak={b.kaynak} slayt={b.slayt} /></h4>
              {gizli ? (
                <button type="button" className="sbk-ilke-ac sbk-bilesen-gizli" onClick={() => setGor((s) => new Set(s).add(b.id))}>Bu bileşen neyi kapsar, neden önemli, Türkiye'de hangi programla yürür? Düşün, sonra dokun.</button>
              ) : (
                <div className="sbk-bilesen-soru">
                  {bAlt && bAlt.length > 0 && <section><h5>Kapsamı</h5><ul className="sbk-madde">{bAlt.map((m) => <li key={m}>{m}</li>)}</ul></section>}
                  {b.ne_demek && <section><h5>Ne demek?</h5><p>{b.ne_demek}</p></section>}
                  {b.neden_onemli && <section><h5>Neden önemli?</h5><p>{b.neden_onemli}</p></section>}
                  {(b.ornekler?.length || 0) > 0 && <section><h5>Örnekler</h5><ul className="sbk-madde">{b.ornekler!.map((o) => <li key={o}>{o}</li>)}</ul></section>}
                  {(b.turkiyede?.length || 0) > 0 && (
                    <section className="is-turkiye"><h5>Türkiye'de nasıl yürütülüyor?</h5><ul className="sbk-madde">{b.turkiyede!.map((t, i) => <li key={i}>{t.metin}<Atif id={t.kaynak} /></li>)}</ul></section>
                  )}
                  {b.koruma_duzeyi && (
                    <section><h5>Hangi korunma düzeyi?</h5><p><Rozet ton="accent">{DUZEY_AD[b.koruma_duzeyi] || b.koruma_duzeyi} korunma</Rozet> <button type="button" className="sbk-link-btn" onClick={() => git('koruma')}>Korunma düzeyleri <ArrowRight aria-hidden /></button></p></section>
                  )}
                </div>
              )}
            </div>
          </div>
        </Blok>
      )}

      {(g.ottawa?.eylem_alanlari?.length || 0) > 0 && (
        <Blok baslik="Ottawa Sözleşmesi'nin 5 eylem alanı (1986)" ikon={Flag} alt={g.ottawa!.metin} genis maddeler={() => g.ottawa!.eylem_alanlari!.map((x, i) => (i === 0 ? { metin: x, kaynak: g.ottawa!.kaynak } : x))}>
          <ol className="sbk-adimlar">{g.ottawa!.eylem_alanlari!.map((x, i) => <li key={x}><span>{i + 1}</span><p>{x}</p></li>)}</ol>
          <p className="sbk-grafik-k">Kaynak <Atif id={g.ottawa!.kaynak} /></p>
        </Blok>
      )}

      {g.etkiler && (
        <Blok
          baslik="Sağlığı geliştirmenin etkileri: ne zaman ne görülür?" ikon={History} alt="Sınavda sorulan ayrım: kısa, orta ve uzun dönem" genis
          maddeler={() => [{ metin: '**Kısa dönem**', kaynak: g.etkiler!.kaynak, alt: g.etkiler!.kisa_donem || [] }, { metin: '**Orta dönem**', alt: g.etkiler!.orta_donem || [] }, { metin: '**Uzun dönem**', alt: g.etkiler!.uzun_donem || [] }]}
        >
          <div className="sbk-donem">
            {([['Kısa dönem', g.etkiler.kisa_donem], ['Orta dönem', g.etkiler.orta_donem], ['Uzun dönem', g.etkiler.uzun_donem]] as const).map(([ad, l], i) => (
              <section key={ad} className={`is-${i}`}><h4>{ad}</h4><ul>{(l || []).map((x) => <li key={x}>{x}</li>)}</ul></section>
            ))}
          </div>
          <p className="sbk-grafik-k">Kaynak <Atif id={g.etkiler.kaynak} /></p>
        </Blok>
      )}

      <div className="sbk-iki-sutun">
        {(g.stratejiler?.maddeler?.length || 0) > 0 && (
          <Blok baslik="Stratejiler" ikon={Target} maddeler={() => g.stratejiler!.maddeler!.map((x, i) => (i === 0 ? { metin: x, kaynak: g.stratejiler!.kaynak } : x))}>
            <ul className="sbk-madde">{g.stratejiler!.maddeler!.map((x) => <li key={x}>{x}</li>)}</ul>
            <p className="sbk-grafik-k"><Atif id={g.stratejiler!.kaynak} /></p>
          </Blok>
        )}
        {(g.ortaya_cikis_faktorleri?.maddeler?.length || 0) > 0 && (
          <Blok baslik="Neden ortaya çıktı?" ikon={Lightbulb} maddeler={() => g.ortaya_cikis_faktorleri!.maddeler!.map((x, i) => (i === 0 ? { metin: x, kaynak: g.ortaya_cikis_faktorleri!.kaynak } : x))}>
            <ul className="sbk-madde">{g.ortaya_cikis_faktorleri!.maddeler!.map((x) => <li key={x}>{x}</li>)}</ul>
            <p className="sbk-grafik-k"><Atif id={g.ortaya_cikis_faktorleri!.kaynak} /></p>
          </Blok>
        )}
      </div>

      {(g.konferanslar?.maddeler?.length || 0) > 0 && (
        <Blok baslik="Uluslararası sağlığı geliştirme konferansları" ikon={BookOpenCheck} alt="İlk: Ottawa (1986)" maddeler={() => g.konferanslar!.maddeler!.map((x, i) => (i === 0 ? { metin: x, kaynak: g.konferanslar!.kaynak } : x))}>
          <ol className="sbk-konferans">{g.konferanslar!.maddeler!.map((x) => {
            const m = /\((\d{4})\)/.exec(x);
            return <li key={x}><b>{m ? m[1] : ''}</b><span>{x.replace(/^\d+\.\s*/, '').replace(/\s*\(\d{4}\)/, '')}</span></li>;
          })}</ol>
          <p className="sbk-grafik-k">Kaynak <Atif id={g.konferanslar!.kaynak} /></p>
        </Blok>
      )}

      <SinavKutusu v={v} konular={/geliştir|ottawa|eğitim|strateji/i} />
    </>
  );
};

/* =============================================================================================================== */
/* Koruyucu yaklaşım                                                                                                */
/* =============================================================================================================== */

const programBag = (metin: string): { yol: string; ad: string } | null => {
  if (/aşı|bağışıkla/i.test(metin)) return { yol: `${pathFor('health_ministry')}/asi`, ad: 'Aşı' };
  if (/kanser|KETEM|mamograf|HPV|gaitada/i.test(metin)) return { yol: `${pathFor('health_ministry')}/tarama`, ad: 'Erken teşhis' };
  if (/yenidoğan|işitme|görme|topuk/i.test(metin)) return { yol: `${pathFor('health_ministry')}/yenidogan`, ad: 'Yenidoğan' };
  if (/gebe|doğum öncesi/i.test(metin)) return { yol: `${pathFor('health_ministry')}/anne-kadin`, ad: 'Anne sağlığı' };
  return null;
};

export const KorumaBolum: React.FC<BolumProps> = ({ v }) => {
  const k = v.kavramlar.koruma as NonNullable<BolumProps['v']['kavramlar']['koruma']> & { giris?: KMadde };
  const duzeyler = k?.duzeyler || [];
  const [sec, setSec] = useState(duzeyler[1]?.id || duzeyler[0]?.id || '');
  if (!k || !duzeyler.length) return <p className="sbk-bos">Veri yüklenemedi.</p>;
  const d = duzeyler.find((x) => x.id === sec) || duzeyler[0];
  return (
    <>
      <Blok
        baslik="Hastalığın seyri boyunca dört korunma düzeyi" ikon={Shield} genis
        alt={k.giris?.metin || 'Düzeye dokun: amaç, hedef, örnekler ve Türkiye\'deki karşılığı'}
        maddeler={() => duzeyler.map((x) => ({
          metin: `**${x.ad}**`, kaynak: x.kaynak,
          alt: [
            x.evre && `**Ne zaman**: ${x.evre}`, x.amac && `**Amaç**: ${x.amac}`, x.hedef && `**Hedef**: ${x.hedef}`,
            (x.ornekler?.length || 0) > 0 && { metin: 'Örnekler', alt: x.ornekler! },
            (x.basarili_hastaliklar?.length || 0) > 0 && { metin: 'Başarılı olduğu hastalıklar', alt: x.basarili_hastaliklar! },
            ...(x.turkiyede || []).map((t) => ({ metin: `**Türkiye'de**: ${t.metin}`, kaynak: t.kaynak } as MaddeOge)),
          ].filter(Boolean) as MaddeOge[],
        }))}
      >
        <ol className="sbk-seyir" role="tablist" aria-label="Korunma düzeyleri">
          {duzeyler.map((x, i) => (
            <li key={x.id}>
              <button type="button" role="tab" aria-selected={x.id === d.id} className={`${x.id === d.id ? 'is-sec' : ''} t-${i}`} onClick={() => setSec(x.id)}>
                <b>{x.ad}</b>
                <small>{(x.evre || '').split(/[:;]/)[0]}</small>
              </button>
            </li>
          ))}
        </ol>
        <div className="sbk-duzey-d" role="tabpanel">
          <h4>{d.ad}<Atif id={d.kaynak} /><SlaytBag kaynak={d.kaynak} slayt={d.slayt} /></h4>
          <dl className="sbk-duzey-dl">
            {d.evre && <div><dt>Ne zaman?</dt><dd>{d.evre}</dd></div>}
            {d.amac && <div><dt>Amaç</dt><dd>{d.amac}</dd></div>}
            {d.hedef && <div><dt>Hedef</dt><dd>{d.hedef}</dd></div>}
          </dl>
          {(d.ornekler?.length || 0) > 0 && <><h5>Örnekler</h5><div className="sbk-etiketler">{d.ornekler!.map((o) => <Rozet key={o} ton="accent">{o}</Rozet>)}</div></>}
          {(d.basarili_hastaliklar?.length || 0) > 0 && <><h5>Bu düzeyin başarılı olduğu hastalıklar</h5><div className="sbk-etiketler">{d.basarili_hastaliklar!.map((o) => <Rozet key={o}>{o}</Rozet>)}</div></>}
          {(d.turkiyede?.length || 0) > 0 && (
            <>
              <h5>Türkiye'de karşılığı</h5>
              <ul className="sbk-madde">{d.turkiyede!.map((t, i) => { const bag = programBag(t.metin); return <li key={i}>{t.metin}<Atif id={t.kaynak} />{bag && <IcBag to={bag.yol} className="sbk-slayt-bag">{bag.ad} sayfası</IcBag>}</li>; })}</ul>
            </>
          )}
        </div>
      </Blok>

      <Blok baslik="Dört düzey yan yana" ikon={ListChecks} alt="Telefonda kart, geniş ekranda tablo" genis maddeler={() => duzeyler.map((x) => `**${x.ad}** — ${x.amac || ''} Örnek: ${(x.ornekler || []).slice(0, 3).join(', ')}`)}>
        <OkunurTablo
          baslik="Korunma düzeyleri karşılaştırması"
          sutunlar={[{ anahtar: 'ad', ad: 'Düzey' }, { anahtar: 'evre', ad: 'Ne zaman?' }, { anahtar: 'amac', ad: 'Amaç' }, { anahtar: 'ornek', ad: 'Örnekler' }]}
          satirlar={duzeyler.map((x) => ({ ad: <b>{x.ad}</b>, evre: x.evre, amac: x.amac, ornek: (x.ornekler || []).join(' · ') }))}
        />
      </Blok>

      <div className="sbk-iki-sutun">
        {(k.tarama_ilkeleri?.length || 0) > 0 && (
          <Blok baslik="Tarama planlarken" ikon={Target} maddeler={() => k.tarama_ilkeleri!.map(mk)}>
            <ul className="sbk-madde">{k.tarama_ilkeleri!.map((x, i) => <li key={i}><KaynakliMadde x={x} /></li>)}</ul>
          </Blok>
        )}
        {(k.notlar?.length || 0) > 0 && (
          <Blok baslik="Sınav için dikkat" ikon={Lightbulb} className="is-uyari" maddeler={() => (k.notlar as Esnek[]).map(mk)}>
            <ul className="sbk-madde">{(k.notlar as Esnek[]).map((x, i) => <li key={i}><KaynakliMadde x={x} /></li>)}</ul>
          </Blok>
        )}
      </div>

      <SinavKutusu v={v} konular={/korun|koruyucu/i} />
    </>
  );
};

