import React, { useMemo, useState } from 'react';
import {
  AlertTriangle, ArrowRight, Baby, BookOpenCheck, Building2, CalendarClock, ClipboardList, Droplets, Factory, FlaskConical, GraduationCap,
  HardHat, HeartPulse, History, Hospital, LineChart, ListOrdered, MapPin, Microscope, Pill, Radar, ScanSearch, ShieldCheck, Snowflake,
  Stethoscope, Syringe, Users, Wind,
} from 'lucide-react';
import {
  Atif, Blok, EkAtif, CizgiGrafik, CubukListe, IcBag, Kpi, MiniMetin, Rozet, desteYolu, kazanimBag,
} from './SaglikOrtak';
import {
  AsiTakvimi, BasamakPiramidi, BildirimListesi, GebeIzlemSeridi, GostergeHesap, KanserTaramaYas, MaddeListesi, TaramaTestiHesap, ZamanCizgisi,
} from './SaglikAraclar';
import {
  BOLUMLER, gostergeBul, kaynaklariTopla, sayi, sonDeger, type BolumBaglanti, type BolumId, type Gosterge, type SaglikVeri, type SeriNokta,
} from './saglikVeri';

export interface BolumProps { v: SaglikVeri; bag?: BolumBaglanti; git: (b: BolumId) => void }

const cp = (bag: BolumBaglanti | undefined, ...ids: string[]) => ids.flatMap((id) => bag?.capalar?.[id] || []).slice(0, 2);

/** Bölümün kaynakçasına girecek veri kökleri (numaralama bu sırayla) */
export function bolumKaynaklari(id: BolumId, v: SaglikVeri): string[] {
  const { asi, anne, karabuk, turkiye } = v;
  switch (id) {
    case 'genel': return kaynaklariTopla(turkiye.gostergeler, anne.gostergeler, asi.oranlar, turkiye.kurumlar, karabuk.nufus, karabuk.kurum_sayilari);
    case 'karabuk': return kaynaklariTopla(karabuk);
    case 'asi': return kaynaklariTopla(asi);
    case 'yenidogan': return kaynaklariTopla(anne.yenidogan_taramalari, anne.bebek_cocuk_izlemleri, anne.destek_programlari, yenidoganGostergeleri(v), anne.ureme_sagligi);
    case 'anne_kadin': return kaynaklariTopla(anne.dob_izlemleri, anne.tehlike_isaretleri, anne.lohusa_izlemleri, anneGostergeleri(v), anne.ureme_sagligi, anne.evlilik_oncesi, anne.programlar);
    case 'tarama': return kaynaklariTopla(anne.ketem, anne.kanser_taramalari, anne.yenidogan_taramalari);
    case 'salgin': return kaynaklariTopla(turkiye.bildirimi_zorunlu, turkiye.surveyans, turkiye.salgin_inceleme_basamaklari, turkiye.bulasici_veriler, asi.hastaliklar);
    case 'cevre': return kaynaklariTopla(karabuk.cevre, turkiye.cevre, turkiye.is_sagligi, karabuk.is_sagligi);
    case 'kurumlar': return kaynaklariTopla(turkiye.kurumlar, turkiye.basamaklar, turkiye.insan_gucu, turkiye.tarihce, karabuk.kurum_sayilari);
    case 'istatistik': return kaynaklariTopla(turkiye.gostergeler, turkiye.olum_nedenleri);
    case 'halk_sagligi': return kaynaklariTopla(turkiye.tarihce, turkiye.basamaklar);
    default: return [];
  }
}

const yenidoganGostergeleri = (v: SaglikVeri): Gosterge[] => {
  const hepsi = [...(v.anne.gostergeler || []), ...(v.turkiye.gostergeler || [])];
  const al = (...d: RegExp[]) => hepsi.find((g) => d.some((x) => x.test(`${g.kod || ''} ${g.ad}`)));
  return [al(/bebek ölüm/i), al(/neonatal|yenidoğan ölüm/i), al(/perinatal/i), al(/5 yaş|beş yaş/i), al(/canlı doğum sayısı/i)].filter(Boolean) as Gosterge[];
};
const anneGostergeleri = (v: SaglikVeri): Gosterge[] => {
  const hepsi = [...(v.anne.gostergeler || [])];
  const yd = new Set(yenidoganGostergeleri(v));
  return hepsi.filter((g) => !yd.has(g) || /anne/i.test(g.ad));
};

/** Uzun metinli değerler (TNSA gibi): ad · değer · yıl satırları */
const DegerListesi: React.FC<{ ogeler: { ad: string; deger: number | string; yil?: number | string; kaynak?: string; konum?: string; ek_kaynaklar?: string[] }[] }> = ({ ogeler }) => (
  <dl className="sbk-deger-l">
    {ogeler.map((u) => (
      <div key={u.ad}>
        <dt>{u.ad}{u.yil ? <small> · {u.yil}</small> : null}</dt>
        <dd><span data-num>{typeof u.deger === 'number' ? sayi(u.deger) : u.deger}</span><Atif id={u.kaynak} konum={u.konum} />{u.ek_kaynaklar?.map((e) => <Atif key={e} id={e} />)}</dd>
      </div>
    ))}
  </dl>
);

const KpiIzgara: React.FC<{ children: React.ReactNode }> = ({ children }) => <div className="sbk-kpi-g">{children}</div>;

const GostergeKpi: React.FC<{ g?: Gosterge; ad?: string }> = ({ g, ad }) => {
  const s = sonDeger(g);
  if (!g || !s) return null;
  return <Kpi ad={ad || g.ad} deger={sayi(s.deger as number)} birim={g.birim} yil={s.yil} kaynak={g.kaynak} ek={g.ek_kaynaklar} konum={g.konum} seri={g.seri} />;
};

const Bos: React.FC<{ children?: React.ReactNode }> = ({ children }) => (
  <p className="sbk-bos">{children || 'Bu blok için resmî kaynakta doğrulanmış veri bulunamadı; sayı yazılmadı.'}</p>
);

/** Seçilebilir seriler (çip) + tek grafik */
const SeriSecici: React.FC<{ seriler: { ad: string; seri: SeriNokta[]; ikinci?: { ad: string; seri: SeriNokta[] }; kaynak?: string; konum?: string; ek?: string[]; not?: string; birim?: string }[]; birim?: string; baslik: (ad: string) => string; sifirdan?: boolean }> = ({ seriler, birim, baslik, sifirdan }) => {
  const [sec, setSec] = useState(0);
  const s = seriler[Math.min(sec, seriler.length - 1)];
  if (!s) return null;
  return (
    <div>
      {seriler.length > 1 && (
        <div className="sbk-cip-l" role="radiogroup" aria-label="Seri seç">
          {seriler.map((x, i) => (
            <button key={x.ad} type="button" role="radio" aria-checked={i === sec} className={`sbk-cip ${i === sec ? 'is-sec' : ''}`} onClick={() => setSec(i)}>{x.ad}</button>
          ))}
        </div>
      )}
      <CizgiGrafik
        baslik={baslik(s.ad)} birim={s.birim ?? birim} sifirdan={sifirdan}
        seriler={[{ ad: s.ad, seri: s.seri }, ...(s.ikinci ? [{ ad: s.ikinci.ad, seri: s.ikinci.seri, ton: 'notr' as const }] : [])]}
      />
      {s.not && <p className="sbk-not">{s.not}</p>}
      <p className="sbk-grafik-k">Kaynak <Atif id={s.kaynak} konum={s.konum} />{s.ek && <EkAtif ids={s.ek} />}</p>
    </div>
  );
};

/** Çok sayıda metin kartı: başlık çipleri + seçili kartın maddeleri (uzun duvar yerine) */
const SekmeliKartlar: React.FC<{ kartlar: { baslik: string; maddeler: string[]; kaynak?: string }[] }> = ({ kartlar }) => {
  const [sec, setSec] = useState(0);
  const k = kartlar[Math.min(sec, kartlar.length - 1)];
  if (!k) return null;
  return (
    <div className="sbk-sekmeli">
      <div className="sbk-cip-l" role="tablist" aria-label="Başlık seç">
        {kartlar.map((x, i) => (
          <button key={x.baslik} type="button" role="tab" aria-selected={i === sec} className={`sbk-cip ${i === sec ? 'is-sec' : ''}`} onClick={() => setSec(i)}>
            {x.baslik.replace(/\s*[—(].*$/, '')}
          </button>
        ))}
      </div>
      <section className="sbk-alt-k" role="tabpanel">
        <h4>{k.baslik} <Atif id={k.kaynak} /></h4>
        <MaddeListesi maddeler={k.maddeler} />
      </section>
    </div>
  );
};

/* =============================================================================================================== */
/* Genel bakış                                                                                                      */
/* =============================================================================================================== */

export const GenelBolum: React.FC<BolumProps> = ({ v, git }) => {
  const t = v.turkiye.gostergeler;
  const a = v.anne.gostergeler;
  const asiSeri = v.asi.oranlar?.seriler?.find((s) => /DaBT|Penta|Beşli/i.test(s.asi)) || v.asi.oranlar?.seriler?.[0];
  const asm = v.turkiye.kurumlar?.find((k) => /aile sağlığı merkezi|ASM/i.test(k.ad));
  const enCok = [...(v.baglantilar.mufredat || [])].sort((x, y) => y.cikmis - x.cikmis).slice(0, 10);
  const kb = v.karabuk;
  const kbKurum = (re: RegExp) => kb.kurum_sayilari?.find((k) => re.test(k.tur));
  return (
    <>
      <Blok baslik="Türkiye'de bugün" ikon={LineChart} alt="Sağlık Bakanlığı ve TÜİK'in son yayımladığı değerler" genis>
        <KpiIzgara>
          <GostergeKpi g={gostergeBul(t, /bebek ölüm/i) || gostergeBul(a, /bebek ölüm/i)} />
          <GostergeKpi g={gostergeBul(a, /anne ölüm/i) || gostergeBul(t, /anne ölüm/i)} />
          <GostergeKpi g={gostergeBul(t, /toplam doğurganlık/i) || gostergeBul(a, /toplam doğurganlık/i)} />
          <GostergeKpi g={gostergeBul(t, /beklenen yaşam/i)} />
          {asiSeri && (() => { const s = sonDeger({ seri: asiSeri.degerler }); return s ? <Kpi ad={`Aşılama hızı · ${asiSeri.kisa || asiSeri.asi}`} deger={`%${sayi(s.deger as number)}`} yil={s.yil} kaynak={v.asi.oranlar?.kaynak} konum={v.asi.oranlar?.konum} seri={asiSeri.degerler} /> : null; })()}
          {asm && (() => { const s = sonDeger(asm); return s ? <Kpi ad="Aile sağlığı merkezi" deger={sayi(s.deger as number)} yil={s.yil} kaynak={asm.kaynak} konum={asm.konum} seri={asm.seri} /> : null; })()}
        </KpiIzgara>
      </Blok>

      <div className="sbk-kart-g">
        {BOLUMLER.filter((b) => b.id !== 'genel').map((b) => {
          const bg = v.baglantilar.bolumler[b.id];
          const Ic = b.icon;
          return (
            <button key={b.id} type="button" className="sbk-bolum-kart" onClick={() => git(b.id)}>
              <span className="sbk-bolum-kart-ic"><Ic aria-hidden /></span>
              <span className="sbk-bolum-kart-t">{b.ad}</span>
              <span className="sbk-bolum-kart-a">{b.aciklama}</span>
              {bg && <span className="sbk-bolum-kart-m">{bg.soru_sayisi} çıkmış soru · {bg.desteler.filter((d) => !d.ek).length || bg.desteler.length} deste</span>}
              <ArrowRight aria-hidden className="sbk-bolum-kart-ok" />
            </button>
          );
        })}
      </div>

      {kb.nufus?.toplam && (
        <Blok baslik="Karabük" ikon={MapPin} alt="İlin nüfusu ve birinci basamak sağlık örgütlenmesi" arac={<button type="button" className="sbk-btn" onClick={() => git('karabuk')}>Karabük sayfası <ArrowRight aria-hidden /></button>}>
          <KpiIzgara>
            <Kpi ad="Nüfus" deger={sayi(kb.nufus.toplam)} yil={kb.nufus.yil} kaynak={kb.nufus.kaynak} />
            {[/aile sağlığı merkezi/i, /aile hekim/i, /hastane/i].map((re) => {
              const k = kbKurum(re);
              return k ? <Kpi key={k.tur} ad={k.tur} deger={sayi(k.sayi)} yil={k.yil} kaynak={k.kaynak} /> : null;
            })}
          </KpiIzgara>
        </Blok>
      )}

      {enCok.length > 0 && (
        <Blok baslik="Sınavda en çok soru çıkan halk sağlığı konuları" ikon={GraduationCap} alt="Dönem 3 çıkmış soru sayısı; konuya dokununca kazanımları açılır" genis>
          <CubukListe
            kalemler={enCok.map((m) => ({
              anahtar: `${m.kurul}-${m.anahtar}`,
              ad: <IcBag to={kazanimBag(m.kurul, m.anahtar)}>{m.konu} <small className="sbk-muted">K{m.kurul}</small></IcBag>,
              deger: m.cikmis,
              ipucu: `${m.konu}: ${m.cikmis} çıkmış soru`,
            }))}
            birim="soru"
          />
        </Blok>
      )}
    </>
  );
};

/* =============================================================================================================== */
/* Karabük                                                                                                          */
/* =============================================================================================================== */

const Karsilastir: React.FC<{ satirlar: { ad: string; il: number; tr: number; birim?: string; yil?: number | string; kaynak?: string; konum?: string }[] }> = ({ satirlar }) => {
  const [hepsi, setHepsi] = useState(false);
  const SINIR = 10;
  return (
  <div className="sbk-karsi">
    <div className="sbk-lejant"><span><i aria-hidden />Karabük</span><span className="is-notr"><i aria-hidden />Türkiye</span></div>
    {(hepsi ? satirlar : satirlar.slice(0, SINIR)).map((s) => {
      const mx = Math.max(s.il, s.tr) || 1;
      return (
        <div key={s.ad} className="sbk-karsi-s" title={`${s.ad} — Karabük ${sayi(s.il)}, Türkiye ${sayi(s.tr)} ${s.birim || ''}`}>
          <span className="sbk-karsi-ad">{s.ad}<small>{s.birim}{s.yil ? ` · ${s.yil}` : ''}</small><Atif id={s.kaynak} konum={s.konum} /></span>
          <span className="sbk-cubuk-izler">
            <span className="sbk-cubuk-iz"><i style={{ width: `${(s.il / mx) * 100}%` }} /><b data-num>{sayi(s.il)}</b></span>
            <span className="sbk-cubuk-iz is-notr"><i style={{ width: `${(s.tr / mx) * 100}%` }} /><b data-num>{sayi(s.tr)}</b></span>
          </span>
        </div>
      );
    })}
    {satirlar.length > SINIR && (
      <button type="button" className="sbk-btn" onClick={() => setHepsi((x) => !x)} aria-expanded={hepsi}>
        {hepsi ? 'Daha az göster' : `Tüm göstergeler (${satirlar.length})`}
      </button>
    )}
  </div>
  );
};

/** Kurum/birim listesi: ad + tür satırı, açıklama dokununca açılır */
const KurumListesi: React.FC<{ ogeler: { ad: string; alt?: string; not?: string; kaynak?: string; ikon: React.ElementType }[] }> = ({ ogeler }) => (
  <ul className="sbk-kurum-l">
    {ogeler.map((o) => {
      const Ic = o.ikon;
      const ic = (
        <>
          <span className="sbk-kurum-ic"><Ic aria-hidden /></span>
          <span><b>{o.ad}</b>{o.alt && <small>{o.alt}</small>}</span>
          <Atif id={o.kaynak} />
        </>
      );
      return (
        <li key={o.ad}>
          {o.not ? (
            <details className="sbk-kurum-d">
              <summary>{ic}</summary>
              <p>{o.not}</p>
            </details>
          ) : <div className="sbk-kurum-s">{ic}</div>}
        </li>
      );
    })}
  </ul>
);

export const KarabukBolum: React.FC<BolumProps> = ({ v, git }) => {
  const kb = v.karabuk;
  const ilceler = useMemo(() => {
    const m = new Map<string, { ad: string; nufus?: number; asm?: number; asmAdlari?: string[]; birim?: number; birimBasina?: number; hastane?: string; kaynak?: string }>();
    for (const x of kb.nufus?.ilceler || []) m.set(x.ad, { ad: x.ad, nufus: x.nufus });
    for (const x of kb.ilceler || []) {
      const o = m.get(x.ad) || { ad: x.ad };
      m.set(x.ad, { ...o, nufus: o.nufus ?? x.nufus, asm: x.asm, asmAdlari: x.asm_adlari, birim: x.aile_hekimi_birimi, birimBasina: x.ahb_basina_nufus, hastane: x.hastane, kaynak: x.kaynak });
    }
    return [...m.values()].sort((a, b) => (b.nufus || 0) - (a.nufus || 0));
  }, [kb]);
  const [acikIlce, setAcikIlce] = useState<string | null>(null);
  const kurumGrup = useMemo(() => {
    const gruplar: { ad: string; re: RegExp }[] = [
      { ad: 'Birinci basamak', re: /aile|ASM|kuduz/i },
      { ad: 'Hastane ve acil', re: /hastane|yatak|112|ambulans/i },
      { ad: 'Sağlık insan gücü', re: /hekim|eczacı|hemşire|ebe|personel/i },
    ];
    const kalan = [...(kb.kurum_sayilari || [])];
    const out = gruplar.map((g) => {
      const al = kalan.filter((k) => g.re.test(k.tur));
      al.forEach((k) => kalan.splice(kalan.indexOf(k), 1));
      return { ad: g.ad, liste: al };
    });
    if (kalan.length) out.push({ ad: 'Diğer', liste: kalan });
    return out.filter((g) => g.liste.length);
  }, [kb.kurum_sayilari]);
  const nMax = Math.max(1, ...ilceler.map((x) => x.nufus || 0));
  const karsi = (kb.gostergeler || []).filter((g) => typeof g.deger === 'number' && typeof g.turkiye === 'number');
  const tekil = (kb.gostergeler || []).filter((g) => !(typeof g.deger === 'number' && typeof g.turkiye === 'number'));
  return (
    <>
      <Blok baslik="Karabük bir bakışta" ikon={MapPin} genis>
        <KpiIzgara>
          {kb.nufus?.toplam != null && <Kpi ad="Nüfus" deger={sayi(kb.nufus.toplam)} yil={kb.nufus.yil} kaynak={kb.nufus.kaynak} not="ADNKS" />}
          {kb.nufus?.yas_65_ustu_orani && <Kpi ad="65 yaş ve üstü" deger={`%${sayi(kb.nufus.yas_65_ustu_orani.deger)}`} yil={kb.nufus.yas_65_ustu_orani.yil} kaynak={kb.nufus.yas_65_ustu_orani.kaynak} />}
          {ilceler.length > 0 && <Kpi ad="İlçe" deger={ilceler.length} not={ilceler.map((x) => x.ad).join(', ')} />}
        </KpiIzgara>
        {kurumGrup.map((g) => (
          <div key={g.ad} className="sbk-kpi-grup">
            <h4>{g.ad}</h4>
            <KpiIzgara>
              {g.liste.map((k) => (
                <Kpi
                  key={k.tur} ad={k.tur} deger={sayi(k.sayi)} yil={k.yil} kaynak={k.kaynak} konum={k.konum}
                  not={k.yontem && /sayıldı/i.test(k.yontem) ? 'resmî listeden sayıldı' : undefined}
                  ipucu={[k.yontem, k.not].filter(Boolean).join(' — ')}
                />
              ))}
            </KpiIzgara>
          </div>
        ))}
      </Blok>

      {ilceler.length > 0 && (
        <Blok baslik="İlçelere göre" ikon={ListOrdered} alt="Nüfus, aile sağlığı merkezi ve aile hekimliği birimi" genis>
          <div className="sbk-tablo-kap">
            <table className="sbk-tablo sbk-ilce">
              <thead><tr><th scope="col">İlçe</th><th scope="col">Nüfus</th><th scope="col">ASM</th><th scope="col">Aile hekimliği birimi</th><th scope="col">Birim başına nüfus</th><th scope="col">Hastane</th></tr></thead>
              <tbody>
                {ilceler.map((x) => (
                  <React.Fragment key={x.ad}>
                    <tr>
                      <th scope="row">
                        {x.asmAdlari?.length ? (
                          <button type="button" className="sbk-ilce-b" onClick={() => setAcikIlce(acikIlce === x.ad ? null : x.ad)} aria-expanded={acikIlce === x.ad} title="ASM adlarını göster">{x.ad}</button>
                        ) : x.ad}
                      </th>
                      <td><span className="sbk-hucre-cubuk"><i style={{ width: `${((x.nufus || 0) / nMax) * 100}%` }} /><b data-num>{x.nufus != null ? sayi(x.nufus) : '—'}</b></span></td>
                      <td data-num>{x.asm ?? '—'}</td>
                      <td data-num>{x.birim ?? '—'}</td>
                      <td data-num>{x.birimBasina != null ? sayi(x.birimBasina) : '—'}</td>
                      <td>{x.hastane || '—'} <Atif id={x.kaynak} /></td>
                    </tr>
                    {acikIlce === x.ad && x.asmAdlari?.length ? (
                      <tr className="sbk-ilce-ac"><td colSpan={6}><div className="sbk-etiketler">{x.asmAdlari.map((n) => <Rozet key={n}>{n}</Rozet>)}</div></td></tr>
                    ) : null}
                  </React.Fragment>
                ))}
              </tbody>
            </table>
          </div>
          <p className="sbk-grafik-k">İlçe adına dokun: ASM adları. Birim başına nüfus = ilçe nüfusu / aile hekimliği birimi (hesaplandı). Nüfus <Atif id={kb.nufus?.kaynak} /></p>
        </Blok>
      )}

      {karsi.length > 0 && (
        <Blok baslik="Karabük ve Türkiye" ikon={LineChart} alt="Aynı yıl, aynı tanımla il ve ülke değeri">
          <Karsilastir satirlar={karsi.map((g) => ({ ad: g.ad, il: g.deger as number, tr: g.turkiye as number, birim: g.birim, yil: g.yil, kaynak: g.kaynak, konum: g.konum }))} />
        </Blok>
      )}
      {tekil.length > 0 && (
        <Blok baslik="İl göstergeleri" ikon={ClipboardList}>
          <KpiIzgara>{tekil.map((g) => <Kpi key={g.ad} ad={g.ad} deger={typeof g.deger === 'number' ? sayi(g.deger) : String(g.deger ?? '—')} birim={g.birim} yil={g.yil} kaynak={g.kaynak} konum={g.konum} />)}</KpiIzgara>
        </Blok>
      )}

      {(kb.hastaneler?.length || 0) > 0 && (
        <Blok baslik="Hastaneler" ikon={Hospital} alt={`${kb.hastaneler!.length} kurum`}>
          <KurumListesi ogeler={kb.hastaneler!.map((h) => ({ ad: h.ad, alt: [h.ilce, h.tur].filter(Boolean).join(' · '), not: h.not, kaynak: h.kaynak, ikon: Hospital }))} />
        </Blok>
      )}

      {(kb.birimler?.length || 0) > 0 && (
        <Blok baslik="Halk sağlığı birimleri" ikon={Stethoscope} alt="İl Sağlık Müdürlüğüne bağlı birimler">
          <KurumListesi ogeler={kb.birimler!.map((b) => ({ ad: b.ad, alt: b.adres_ilce, not: b.aciklama, kaynak: b.kaynak, ikon: Building2 }))} />
        </Blok>
      )}

      {((kb.cevre?.length || 0) > 0 || (kb.is_sagligi?.length || 0) > 0) && (
        <Blok baslik="Çevre ve iş sağlığı" ikon={Factory} alt="Demir-çelik sanayisi kenti: hava kalitesi ve iş kazaları" arac={<button type="button" className="sbk-btn" onClick={() => git('cevre')}>Çevre ve sağlık <ArrowRight aria-hidden /></button>}>
          <KpiIzgara>
            {(kb.cevre || []).filter((c) => c.deger != null).slice(0, 4).map((c) => (
              <Kpi key={`${c.baslik}-${c.istasyon || ''}-${c.yil || ''}`} ad={c.baslik} deger={typeof c.deger === 'number' ? sayi(c.deger) : String(c.deger)} birim={c.birim} yil={c.yil} kaynak={c.kaynak} not={c.istasyon} />
            ))}
            {(kb.is_sagligi || []).slice(0, 4).map((c) => <Kpi key={c.ad} ad={c.ad} deger={typeof c.deger === 'number' ? sayi(c.deger) : String(c.deger)} yil={c.yil} kaynak={c.kaynak} konum={c.konum} ipucu={c.aciklama} />)}
          </KpiIzgara>
        </Blok>
      )}

      {(kb.programlar?.length || 0) > 0 && (
        <Blok baslik="İl sağlık müdürlüğü programları" ikon={CalendarClock}>
          <ul className="sbk-program-l">
            {kb.programlar!.map((p) => (
              <li key={p.ad}><b>{p.ad}</b>{p.tarih && <Rozet>{p.tarih}</Rozet>}<span>{p.aciklama} <Atif id={p.kaynak} /></span></li>
            ))}
          </ul>
        </Blok>
      )}

      {kb.universite?.aciklama && (
        <Blok baslik="Karabük Üniversitesi Tıp Fakültesi" ikon={GraduationCap}>
          <MiniMetin metin={kb.universite.aciklama} />
          <p className="sbk-grafik-k">Kaynak <Atif id={kb.universite.kaynak} />{kb.universite.ek_kaynaklar?.map((e) => <Atif key={e} id={e} />)}</p>
        </Blok>
      )}
      {!kb.nufus && !kb.kurum_sayilari?.length && <Bos />}
    </>
  );
};

/* =============================================================================================================== */
/* Aşı                                                                                                              */
/* =============================================================================================================== */

export const AsiBolum: React.FC<BolumProps> = ({ v, bag }) => {
  const a = v.asi;
  const seriler = a.oranlar?.seriler || [];
  const [hastalik, setHastalik] = useState<string | null>(null);
  return (
    <>
      {seriler.length > 0 && (
        <KpiIzgara>
          {seriler.slice(0, 4).map((s) => {
            const son = sonDeger({ seri: s.degerler });
            return son ? <Kpi key={s.asi} ad={s.kisa || s.asi} deger={`%${sayi(son.deger as number)}`} yil={son.yil} kaynak={a.oranlar?.kaynak} konum={a.oranlar?.konum} seri={s.degerler} not="aşılama hızı" /> : null;
          })}
        </KpiIzgara>
      )}

      <Blok baslik="Çocukluk dönemi aşı takvimi" ikon={Syringe} alt="Genişletilmiş Bağışıklama Programı — ziyaret seç, ya da ezber modunda kendini dene" capalar={cp(bag, 'takvim')} genis>
        {a.takvim?.length ? <AsiTakvimi v={a} /> : <Bos />}
      </Blok>

      {seriler.length > 0 && (
        <Blok baslik="Türkiye aşılama hızları" ikon={LineChart} alt="Hedef nüfusta aşılanan çocuk yüzdesi">
          <SeriSecici seriler={seriler.map((s) => ({ ad: s.kisa || s.asi, seri: s.degerler, kaynak: a.oranlar?.kaynak, konum: a.oranlar?.konum }))} birim="%" baslik={(ad) => `${ad} aşılama hızı`} />
          {a.oranlar?.not && <p className="sbk-not sbk-muted">{a.oranlar.not}</p>}
        </Blok>
      )}

      {(a.gebe_eriskin?.length || 0) > 0 && (
        <Blok baslik="Gebe ve erişkin aşıları" ikon={HeartPulse} capalar={cp(bag, 'gebe_asi')}>
          <SekmeliKartlar kartlar={a.gebe_eriskin!.map((g) => ({ baslik: g.baslik, maddeler: g.maddeler, kaynak: g.kaynak }))} />
        </Blok>
      )}

      {(a.hastaliklar?.length || 0) > 0 && (
        <Blok baslik="Aşı ile önlenebilir hastalıklar" ikon={ShieldCheck} alt="Hastalığa dokun: etken, aşı, Türkiye durumu ve vaka seyri" genis>
          <div className="sbk-hastalik-g">
            {a.hastaliklar!.map((h) => {
              const acik = hastalik === h.ad;
              const vaka = (h.vaka || []).filter((x) => x.yil != null && /^\d{4}$/.test(String(x.yil))).map((x) => ({ yil: x.yil as number, deger: x.sayi }));
              const donemler = (h.vaka || []).filter((x) => x.yil == null && x.donem);
              return (
                <section key={h.ad} className={`sbk-hastalik ${acik ? 'is-acik' : ''}`}>
                  <button type="button" onClick={() => setHastalik(acik ? null : h.ad)} aria-expanded={acik}>
                    <b>{h.ad}</b>
                    {vaka.length > 0 && <Rozet ton="accent">{sayi(sonDeger({ seri: vaka })!.deger as number)} vaka · {sonDeger({ seri: vaka })!.yil}</Rozet>}
                    {h.asi && !acik && <small className="sbk-muted sbk-tek-satir">{h.asi}</small>}
                  </button>
                  {acik && (
                    <div className="sbk-hastalik-ic">
                      <dl>
                        {h.asi && <><dt>Aşı</dt><dd>{h.asi}</dd></>}
                        {h.etken && <><dt>Etken</dt><dd>{h.etken}</dd></>}
                        {h.bulas && <><dt>Bulaş</dt><dd>{h.bulas}</dd></>}
                        {h.turkiye && <><dt>Türkiye</dt><dd>{h.turkiye} <Atif id={h.kaynak} /></dd></>}
                      </dl>
                      {donemler.length > 0 && (
                        <ul className="sbk-donem-l">{donemler.map((x) => <li key={x.donem}><span>{x.donem} yıllık ortalama</span><b data-num>{sayi(x.sayi)}</b><Atif id={x.kaynak} konum={x.konum} /></li>)}</ul>
                      )}
                      {vaka.length > 1 && <CizgiGrafik baslik={`${h.ad} vaka sayısı`} seriler={[{ ad: 'Vaka', seri: vaka }]} yukseklik={160} sifirdan />}
                      {vaka.length > 0 && <p className="sbk-grafik-k">Vaka sayıları <Atif id={h.vaka!.find((x) => x.yil != null)?.kaynak} konum={h.vaka!.find((x) => x.yil != null)?.konum} /></p>}
                    </div>
                  )}
                </section>
              );
            })}
          </div>
        </Blok>
      )}

      {(a.kilometre_taslari?.length || 0) > 0 && (
        <Blok baslik="Türkiye'de bağışıklamanın kilometre taşları" ikon={History} capalar={cp(bag, 'tarihce')}>
          <ZamanCizgisi ogeler={[...a.kilometre_taslari!].sort((x, y) => Number(x.yil) - Number(y.yil)).map((k) => ({ anahtar: `${k.yil}-${k.olay}`, zaman: k.yil, baslik: k.olay, kaynak: k.kaynak }))} />
        </Blok>
      )}

      {((a.soguk_zincir?.length || 0) > 0 || (a.genel_kurallar?.length || 0) > 0) && (
        <div className="sbk-iki-sutun">
          {(a.soguk_zincir?.length || 0) > 0 && <Blok baslik="Soğuk zincir" ikon={Snowflake}><MaddeListesi maddeler={a.soguk_zincir!} /></Blok>}
          {(a.genel_kurallar?.length || 0) > 0 && <Blok baslik="Genel aşılama kuralları" ikon={ClipboardList}><MaddeListesi maddeler={a.genel_kurallar!} /></Blok>}
        </div>
      )}
    </>
  );
};

/* =============================================================================================================== */
/* Yenidoğan                                                                                                        */
/* =============================================================================================================== */

export const YenidoganBolum: React.FC<BolumProps> = ({ v, bag, git }) => {
  const an = v.anne;
  const g = yenidoganGostergeleri(v);
  const boh = g.find((x) => /bebek ölüm/i.test(x.ad));
  const neo = g.find((x) => /neonatal|yenidoğan ölüm/i.test(x.ad));
  const taramaGrup = useMemo(() => {
    const m = new Map<string, NonNullable<typeof an.yenidogan_taramalari>>();
    for (const t of an.yenidogan_taramalari || []) {
      const k = t.grup || 'Diğer';
      m.set(k, [...(m.get(k) || []), t]);
    }
    return [...m.entries()];
  }, [an.yenidogan_taramalari]);
  const emzirme = (an.ureme_sagligi || []).filter((u) => /anne sütü|emzir/i.test(u.ad));
  return (
    <>
      {g.length > 0 && <KpiIzgara>{g.map((x) => <GostergeKpi key={x.ad} g={x} />)}</KpiIzgara>}

      <Blok baslik="Ulusal yenidoğan taramaları" ikon={ScanSearch} alt="Topuk kanı ve diğer taramalar — hangi yıldan beri, ne zaman, nasıl" genis>
        {taramaGrup.length ? (
          <div className="sbk-tarama-g">
            {taramaGrup.map(([grup, liste]) => (
              <section key={grup} className="sbk-tarama-grup">
                <h4>{grup}</h4>
                <ul>
                  {liste.map((t) => (
                    <li key={t.id || t.ad}>
                      <span className="sbk-tarama-y" data-num>{t.baslangic ?? '—'}</span>
                      <span>
                        <b>{t.ad}</b>
                        <small>{[t.zaman, t.yontem].filter(Boolean).join(' · ')}</small>
                        {t.not && <small className="sbk-muted">{t.not}</small>}
                      </span>
                      <span><Atif id={t.kaynak} />{t.ek_kaynaklar?.map((e) => <Atif key={e} id={e} />)}</span>
                    </li>
                  ))}
                </ul>
              </section>
            ))}
          </div>
        ) : <Bos />}
      </Blok>

      {(an.bebek_cocuk_izlemleri?.length || 0) > 0 && (
        <Blok baslik="Bebek ve çocuk izlem takvimi" ikon={CalendarClock} alt="Aile hekimliğinde izlem zamanları — zamana dokun, içerik açılsın" capalar={cp(bag, 'bebek_izlem', 'cocuk_izlem')}>
          <ZamanCizgisi acilir ogeler={an.bebek_cocuk_izlemleri!.map((x, i) => ({ anahtar: `${i}`, zaman: x.zaman, icerik: x.icerik, kaynak: x.kaynak }))} />
        </Blok>
      )}

      {(an.destek_programlari?.length || 0) > 0 && (
        <Blok baslik="Destek programları" ikon={Pill} alt="Demir, D vitamini ve diğer ulusal destekler" capalar={cp(bag, 'destekler', 'k_vitamini')}>
          <div className="sbk-tablo-kap">
            <table className="sbk-tablo">
              <thead><tr><th scope="col">Program</th><th scope="col">Kime</th><th scope="col">Doz</th><th scope="col">Ne zaman</th></tr></thead>
              <tbody>
                {an.destek_programlari!.map((p) => (
                  <tr key={p.ad}><th scope="row">{p.ad} <Atif id={p.kaynak} /></th><td>{p.hedef || '—'}</td><td>{p.doz || '—'}</td><td>{[p.baslangic, p.bitis].filter(Boolean).join(' → ') || '—'}</td></tr>
                ))}
              </tbody>
            </table>
          </div>
        </Blok>
      )}

      {boh?.seri && boh.seri.length > 1 && (
        <Blok baslik="Bebek ölüm hızının seyri" ikon={LineChart} capalar={cp(bag, 'gostergeler')}>
          <CizgiGrafik
            baslik="Bebek ölüm hızı" birim={boh.birim} sifirdan
            seriler={[{ ad: 'Bebek ölüm hızı', seri: boh.seri }, ...(neo?.seri && neo.birim === boh.birim ? [{ ad: neo.ad, seri: neo.seri, ton: 'notr' as const }] : [])]}
          />
          <p className="sbk-grafik-k">Kaynak <Atif id={boh.kaynak} konum={boh.konum} />{neo?.seri ? <> · <Atif id={neo.kaynak} konum={neo.konum} /></> : null}</p>
          {boh.tanim && <MiniMetin metin={boh.tanim} className="sbk-muted" />}
        </Blok>
      )}

      {emzirme.length > 0 && (
        <Blok baslik="Anne sütü ve emzirme" ikon={Baby} capalar={cp(bag, 'anne_sutu')}>
          <DegerListesi ogeler={emzirme} />
        </Blok>
      )}

      <button type="button" className="sbk-bolum-gec" onClick={() => git('anne_kadin')}>
        <HeartPulse aria-hidden /><span><b>Kadın / Anne Sağlığı</b><small>Gebe izlemi, lohusa izlemi, anne ölümü</small></span><ArrowRight aria-hidden />
      </button>
    </>
  );
};

/* =============================================================================================================== */
/* Kadın / Anne sağlığı                                                                                             */
/* =============================================================================================================== */

export const AnneKadinBolum: React.FC<BolumProps> = ({ v, bag }) => {
  const an = v.anne;
  const gl = anneGostergeleri(v);
  const aoo = gl.find((g) => /anne ölüm/i.test(g.ad));
  const tdh = gl.find((g) => /toplam doğurganlık/i.test(g.ad));
  const sez = gl.find((g) => /sezaryen/i.test(g.ad));
  const dob = gl.find((g) => /doğum öncesi|DÖB/i.test(g.ad));
  const digerSeriler = gl.filter((g) => g !== aoo && (g.seri?.length || 0) > 1);
  const ureme = (an.ureme_sagligi || []).filter((u) => !/anne sütü|emzir/i.test(u.ad));
  return (
    <>
      <KpiIzgara>
        {[aoo, tdh, sez, dob].filter(Boolean).map((g) => <GostergeKpi key={g!.ad} g={g} />)}
      </KpiIzgara>

      <Blok baslik="Gebe izlem takvimi" ikon={CalendarClock} alt="Doğum Öncesi Bakım Yönetim Rehberi — en az dört izlem" capalar={cp(bag, 'gebe_izlem', 'kessner')} genis>
        {an.dob_izlemleri?.length ? <GebeIzlemSeridi izlemler={an.dob_izlemleri} /> : <Bos />}
      </Blok>

      <div className="sbk-iki-sutun">
        {(an.tehlike_isaretleri?.maddeler.length || 0) > 0 && (
          <Blok baslik="Gebelikte tehlike işaretleri" ikon={AlertTriangle} capalar={cp(bag, 'tehlike')} className="is-uyari">
            <MaddeListesi maddeler={an.tehlike_isaretleri!.maddeler} kaynak={an.tehlike_isaretleri!.kaynak} />
            {(an.tehlike_isaretleri!.acil_sevk_kriterleri?.length || 0) > 0 && (
              <details className="sbk-acil">
                <summary>Acil sevk ölçütleri ({an.tehlike_isaretleri!.acil_sevk_kriterleri!.length})</summary>
                <MaddeListesi maddeler={an.tehlike_isaretleri!.acil_sevk_kriterleri!} />
              </details>
            )}
          </Blok>
        )}
        {(an.lohusa_izlemleri?.length || 0) > 0 && (
          <Blok baslik="Lohusa izlemi" ikon={HeartPulse} capalar={cp(bag, 'lohusa')}>
            <ZamanCizgisi acilir ogeler={an.lohusa_izlemleri!.map((x) => ({ anahtar: String(x.no), zaman: `${x.no}. izlem`, baslik: x.zaman, icerik: x.icerik, kaynak: x.kaynak }))} />
          </Blok>
        )}
      </div>

      {aoo?.seri && aoo.seri.length > 1 && (
        <Blok baslik="Anne ölüm oranının seyri" ikon={LineChart} capalar={cp(bag, 'anne_olum')}>
          <CizgiGrafik baslik="Anne ölüm oranı" birim={aoo.birim} seriler={[{ ad: 'Anne ölüm oranı', seri: aoo.seri }]} sifirdan />
          <p className="sbk-grafik-k">Kaynak <Atif id={aoo.kaynak} konum={aoo.konum} /></p>
          {aoo.tanim && <MiniMetin metin={aoo.tanim} className="sbk-muted" />}
        </Blok>
      )}

      {digerSeriler.length > 0 && (
        <Blok baslik="Doğum ve doğurganlık göstergeleri" ikon={LineChart} alt="Göstergeyi seç">
          <SeriSecici seriler={digerSeriler.map((g) => ({ ad: g.ad, seri: g.seri!, kaynak: g.kaynak, konum: g.konum }))} baslik={(ad) => ad} birim={undefined} />
        </Blok>
      )}

      {ureme.length > 0 && (
        <Blok baslik="Üreme sağlığı ve aile planlaması" ikon={Users} alt="Türkiye Nüfus ve Sağlık Araştırması" capalar={cp(bag, 'tnsa')}>
          <DegerListesi ogeler={ureme} />
        </Blok>
      )}

      <div className="sbk-iki-sutun">
        {(an.evlilik_oncesi?.maddeler.length || 0) > 0 && (
          <Blok baslik="Evlilik öncesi tarama" ikon={Microscope}>
            <MaddeListesi maddeler={an.evlilik_oncesi!.maddeler} kaynak={an.evlilik_oncesi!.kaynak} />
          </Blok>
        )}
        {(an.programlar?.length || 0) > 0 && (
          <Blok baslik="Anne ve kadın sağlığı programları" ikon={ClipboardList}>
            <ul className="sbk-program-l">
              {an.programlar!.map((p) => <li key={p.ad}><b>{p.ad}</b><span>{p.aciklama} <Atif id={p.kaynak} /></span></li>)}
            </ul>
          </Blok>
        )}
      </div>
    </>
  );
};

/* =============================================================================================================== */
/* Erken teşhis                                                                                                     */
/* =============================================================================================================== */

export const TaramaBolum: React.FC<BolumProps> = ({ v, bag, git }) => {
  const an = v.anne;
  const prenatal = cp(bag, 'prenatal');
  return (
    <>
      <KpiIzgara>
        {an.ketem?.sayi != null && <Kpi ad="KETEM (Kanser Erken Teşhis, Tarama ve Eğitim Merkezi)" deger={sayi(an.ketem.sayi)} yil={an.ketem.yil} kaynak={an.ketem.kaynak} konum={an.ketem.konum} seri={an.ketem.seri} ipucu={[an.ketem.detay, an.ketem.not].filter(Boolean).join(' — ')} />}
        {(an.kanser_taramalari?.length || 0) > 0 && <Kpi ad="Ulusal kanser taraması" deger={an.kanser_taramalari!.length} not={an.kanser_taramalari!.map((k) => k.kanser).join(' · ')} kaynak={an.kanser_taramalari![0].kaynak} />}
        {(an.yenidogan_taramalari?.length || 0) > 0 && <Kpi ad="Yenidoğan taraması" deger={an.yenidogan_taramalari!.length} not="ulusal programda" kaynak={an.yenidogan_taramalari![0].kaynak} />}
      </KpiIzgara>

      {an.ketem?.detay && <p className="sbk-not">{an.ketem.detay} <Atif id={an.ketem.kaynak} konum={an.ketem.konum} /></p>}

      <Blok baslik="Yaşına göre kanser taraması" ikon={ScanSearch} alt="Ulusal Kanser Tarama Standartları — yaşı ve cinsiyeti değiştir" capalar={cp(bag, 'kanser')} genis>
        {an.kanser_taramalari?.length ? <KanserTaramaYas liste={an.kanser_taramalari} /> : <Bos />}
      </Blok>

      {(an.kanser_taramalari?.length || 0) > 0 && (
        <Blok baslik="Tarama standartları tablosu" ikon={ClipboardList}>
          <div className="sbk-tablo-kap">
            <table className="sbk-tablo">
              <thead><tr><th scope="col">Kanser</th><th scope="col">Hedef grup</th><th scope="col">Yöntem</th><th scope="col">Sıklık</th></tr></thead>
              <tbody>{an.kanser_taramalari!.map((k) => <tr key={k.kanser}><th scope="row">{k.kanser} <Atif id={k.kaynak} /></th><td>{k.hedef}</td><td>{k.yontem}</td><td>{k.aralik}</td></tr>)}</tbody>
            </table>
          </div>
        </Blok>
      )}

      <Blok baslik="Bir tarama testi ne kadar iyi?" ikon={FlaskConical} alt="Dört gözlü tablodan duyarlılık, seçicilik ve kestirim değerleri — sınavda sık sorulan hesap" genis>
        <TaramaTestiHesap />
      </Blok>

      <div className="sbk-iki-sutun">
        {prenatal.length > 0 && (
          <Blok baslik="Prenatal tarama" ikon={Microscope} alt="İkili/üçlü test ve ense kalınlığı derste" capalar={prenatal}>
            <p className="sbk-muted">Gebelikte anöploidi taraması Tıbbi Genetik ve Halk Sağlığı derslerinde işlenir. Gebe izlemindeki yeri için Kadın / Anne Sağlığı bölümüne bak.</p>
            <button type="button" className="sbk-btn" onClick={() => git('anne_kadin')}>Gebe izlem takvimi <ArrowRight aria-hidden /></button>
          </Blok>
        )}
        <Blok baslik="Yenidoğan taramaları" ikon={Baby}>
          <p className="sbk-muted">Topuk kanı, işitme, kalça ve kalp taramaları başlangıç yıllarıyla Yenidoğan bölümünde.</p>
          <button type="button" className="sbk-btn" onClick={() => git('yenidogan')}>Yenidoğan taramaları <ArrowRight aria-hidden /></button>
        </Blok>
      </div>
    </>
  );
};

/* =============================================================================================================== */
/* Salgın hastalıklar                                                                                               */
/* =============================================================================================================== */

export const SalginBolum: React.FC<BolumProps> = ({ v, bag }) => {
  const t = v.turkiye;
  const veriler = (t.bulasici_veriler || []).filter((x) => (x.seri?.length || 0) > 0);
  return (
    <>
      {veriler.length > 0 && (
        <KpiIzgara>
          {veriler.slice(0, 4).map((x) => { const s = sonDeger(x); return s ? <Kpi key={x.hastalik} ad={x.hastalik} deger={sayi(s.deger as number)} birim={x.olcu} yil={s.yil} kaynak={x.kaynak} konum={x.konum} seri={x.seri} /> : null; })}
        </KpiIzgara>
      )}

      <Blok baslik="Bildirimi zorunlu bulaşıcı hastalıklar" ikon={ClipboardList} alt="Hastalığı ara: hangi grupta, nasıl bildirilir" capalar={cp(bag, 'bildirim')} genis>
        {t.bildirimi_zorunlu?.gruplar?.length ? <BildirimListesi v={t.bildirimi_zorunlu} /> : <Bos />}
      </Blok>

      <div className="sbk-iki-sutun">
        {(t.surveyans?.length || 0) > 0 && (
          <Blok baslik="Sürveyans türleri" ikon={Radar} capalar={cp(bag, 'surveyans')}>
            <dl className="sbk-tanim-l">{t.surveyans!.map((s) => <React.Fragment key={s.tur}><dt>{s.tur} <Atif id={s.kaynak} /></dt><dd>{s.tanim}</dd></React.Fragment>)}</dl>
          </Blok>
        )}
        {(t.salgin_inceleme_basamaklari?.length || 0) > 0 && (
          <Blok baslik="Salgın incelemesinin basamakları" ikon={ListOrdered} capalar={cp(bag, 'inceleme', 'kontrol')}>
            <ol className="sbk-adim-l">{[...t.salgin_inceleme_basamaklari!].sort((a, b) => a.no - b.no).map((s) => <li key={s.no}><span data-num>{s.no}</span><span>{s.adim} <Atif id={s.kaynak} /></span></li>)}</ol>
          </Blok>
        )}
      </div>

      {veriler.length > 0 && (
        <Blok baslik="Türkiye'de bulaşıcı hastalık verileri" ikon={LineChart} alt="Hastalığı seç" capalar={cp(bag, 'zincir')} genis>
          <SeriSecici
            sifirdan
            seriler={veriler.flatMap((x) => [
              { ad: x.hastalik, seri: x.seri!, ikinci: x.olum?.length ? { ad: 'Ölüm', seri: x.olum } : undefined, kaynak: x.kaynak, konum: x.konum, ek: x.ek_kaynaklar, not: [x.ozet, x.not].filter(Boolean).join(' '), birim: x.olcu },
              ...((x.insidans_100bin?.length || 0) > 1 ? [{ ad: `${x.hastalik.replace(/\s*\(.*\)$/, '')} · insidans`, seri: x.insidans_100bin!, kaynak: x.kaynak, konum: x.konum, ek: x.ek_kaynaklar, birim: "100.000'de" }] : []),
            ]).filter((x) => x.seri.filter((n) => /^\d{4}$/.test(String(n.yil))).length > 1)}
            baslik={(ad) => ad}
          />
        </Blok>
      )}
    </>
  );
};

/* =============================================================================================================== */
/* Çevre ve sağlık                                                                                                  */
/* =============================================================================================================== */

export const CevreBolum: React.FC<BolumProps> = ({ v, bag }) => {
  const kb = v.karabuk;
  const t = v.turkiye;
  const ikon = (b: string) => (/su|klor/i.test(b) ? Droplets : /hava|PM|SO2|NO2/i.test(b) ? Wind : /gürültü/i.test(b) ? Radar : Factory);
  return (
    <>
      {(kb.cevre?.length || 0) > 0 && (
        <Blok baslik="Karabük'te hava kalitesi" ikon={Wind} alt="Ölçüm istasyonu yıllık ortalamaları ve il çevre durum raporu" capalar={cp(bag, 'hava', 'cevre_patoloji')} genis>
          <KpiIzgara>
            {kb.cevre!.filter((c) => c.deger != null).map((c) => (
              <Kpi key={`${c.baslik}-${c.istasyon || ''}-${c.yil || ''}`} ad={c.baslik} deger={typeof c.deger === 'number' ? sayi(c.deger) : String(c.deger)} birim={c.birim} yil={c.yil} kaynak={c.kaynak} not={c.istasyon} />
            ))}
          </KpiIzgara>
          {kb.cevre!.filter((c) => c.aciklama).map((c) => <p key={`a-${c.baslik}-${c.yil || ''}`} className="sbk-not"><b>{c.baslik}:</b> {c.aciklama} <Atif id={c.kaynak} /></p>)}
        </Blok>
      )}

      {(t.cevre?.length || 0) > 0 && (
        <div className="sbk-alt-g">
          {t.cevre!.map((c) => {
            const Ic = ikon(c.baslik);
            return (
              <Blok key={c.baslik} baslik={c.baslik} ikon={Ic} capalar={/su/i.test(c.baslik) ? cp(bag, 'su') : /hava/i.test(c.baslik) ? cp(bag, 'hava') : undefined}>
                <MaddeListesi maddeler={c.maddeler || []} kaynak={c.kaynak} />
              </Blok>
            );
          })}
        </div>
      )}

      {((t.is_sagligi?.length || 0) > 0 || (kb.is_sagligi?.length || 0) > 0) && (
        <Blok baslik="İş kazaları ve meslek hastalıkları" ikon={HardHat} capalar={cp(bag, 'meslek')} genis>
          {(kb.is_sagligi?.length || 0) > 0 && (
            <KpiIzgara>{kb.is_sagligi!.map((c) => <Kpi key={c.ad} ad={`Karabük · ${c.ad}`} deger={typeof c.deger === 'number' ? sayi(c.deger) : String(c.deger)} yil={c.yil} kaynak={c.kaynak} konum={c.konum} ipucu={c.aciklama} />)}</KpiIzgara>
          )}
          {(t.is_sagligi?.filter((x) => (x.seri?.length || 0) > 1).length || 0) > 0 && (
            <SeriSecici seriler={t.is_sagligi!.filter((x) => (x.seri?.length || 0) > 1).map((x) => ({ ad: x.ad, seri: x.seri!, kaynak: x.kaynak, konum: x.konum }))} baslik={(ad) => `Türkiye · ${ad}`} sifirdan />
          )}
        </Blok>
      )}
      {!kb.cevre?.length && !t.cevre?.length && <Bos />}
    </>
  );
};

/* =============================================================================================================== */
/* Sağlık kurumları                                                                                                 */
/* =============================================================================================================== */

export const KurumlarBolum: React.FC<BolumProps> = ({ v, bag, git }) => {
  const t = v.turkiye;
  const kurumlar = t.kurumlar || [];
  const [sec, setSec] = useState(0);
  const k = kurumlar[Math.min(sec, kurumlar.length - 1)];
  return (
    <>
      {kurumlar.length > 0 && (
        <KpiIzgara>
          {kurumlar.slice(0, 6).map((x) => { const s = sonDeger(x); return s ? <Kpi key={x.ad} ad={x.ad} deger={sayi(s.deger as number)} yil={s.yil} kaynak={x.kaynak} konum={x.konum} seri={x.seri} /> : null; })}
        </KpiIzgara>
      )}

      {(t.basamaklar?.length || 0) > 0 && (
        <Blok baslik="Sağlık hizmeti basamakları" ikon={Building2} alt="Basamağa dokun: hangi kurumlar, ne iş yapar" capalar={cp(bag, 'basamak', 'aile_hekimligi')} genis>
          <BasamakPiramidi basamaklar={t.basamaklar!} />
        </Blok>
      )}

      {k && (
        <Blok baslik="Kurum sayıları" ikon={Hospital} alt="Kalemi seç">
          <div className="sbk-cip-l" role="radiogroup" aria-label="Kurum türü">
            {kurumlar.map((x, i) => <button key={x.ad} type="button" role="radio" aria-checked={i === sec} className={`sbk-cip ${i === sec ? 'is-sec' : ''}`} onClick={() => setSec(i)}>{x.ad}</button>)}
          </div>
          {(k.seri?.length || 0) > 1 && <CizgiGrafik baslik={k.ad} seriler={[{ ad: k.ad, seri: k.seri! }]} />}
          {(k.alt?.length || 0) > 0 && <CubukListe kalemler={k.alt!.map((a) => ({ ad: a.ad, deger: a.deger }))} />}
          <p className="sbk-grafik-k">Kaynak <Atif id={k.kaynak} konum={k.konum} /></p>
        </Blok>
      )}

      {(t.insan_gucu?.length || 0) > 0 && (
        <Blok baslik="Sağlık insan gücü" ikon={Stethoscope}>
          <KpiIzgara>{t.insan_gucu!.map((x) => { const s = sonDeger(x); return s ? <Kpi key={x.ad} ad={x.ad} deger={sayi(s.deger as number)} yil={s.yil} kaynak={x.kaynak} konum={x.konum} seri={x.seri} /> : null; })}</KpiIzgara>
        </Blok>
      )}

      {(t.tarihce?.length || 0) > 0 && (
        <Blok baslik="Türkiye'de sağlık örgütlenmesinin tarihçesi" ikon={History} capalar={cp(bag, 'sosyalizasyon', 'tarihce')}>
          <ZamanCizgisi ogeler={[...t.tarihce!].sort((a, b) => Number(a.yil) - Number(b.yil)).map((x) => ({ anahtar: `${x.yil}-${x.olay}`, zaman: x.yil, baslik: x.olay, kaynak: x.kaynak }))} />
        </Blok>
      )}

      {(v.karabuk.kurum_sayilari?.length || 0) > 0 && (
        <button type="button" className="sbk-bolum-gec" onClick={() => git('karabuk')}>
          <MapPin aria-hidden /><span><b>Karabük'te sağlık kurumları</b><small>{v.karabuk.kurum_sayilari!.slice(0, 3).map((x) => `${x.sayi} ${x.tur.toLocaleLowerCase('tr-TR')}`).join(' · ')}</small></span><ArrowRight aria-hidden />
        </button>
      )}
    </>
  );
};

/* =============================================================================================================== */
/* İstatistikler                                                                                                    */
/* =============================================================================================================== */

export const IstatistikBolum: React.FC<BolumProps> = ({ v, bag }) => {
  const gl = useMemo(() => {
    const goruldu = new Set<string>();
    return [...(v.turkiye.gostergeler || []), ...(v.anne.gostergeler || [])].filter((g) => {
      const k = (g.kod || g.ad).toLocaleLowerCase('tr-TR');
      if (goruldu.has(k) || goruldu.has(g.ad.toLocaleLowerCase('tr-TR'))) return false;
      goruldu.add(k); goruldu.add(g.ad.toLocaleLowerCase('tr-TR'));
      return !!sonDeger(g);
    });
  }, [v]);
  const [sec, setSec] = useState<string | null>(null);
  const g = gl.find((x) => (x.kod || x.ad) === sec) || gl[0];
  const on = v.turkiye.olum_nedenleri;
  return (
    <>
      <Blok baslik="Sağlık göstergeleri" ikon={LineChart} alt="Göstergeye dokun: tanımı, formülü ve yıllara göre seyri" capalar={cp(bag, 'gostergeler', 'bebek_olum')} genis>
        {gl.length ? (
          <div className="sbk-gosterge">
            <div className="sbk-gosterge-l" role="listbox" aria-label="Gösterge seç">
              {gl.map((x) => {
                const s = sonDeger(x)!;
                const secili = x === g;
                return (
                  <button key={x.kod || x.ad} type="button" role="option" aria-selected={secili} className={secili ? 'is-sec' : ''} onClick={() => setSec(x.kod || x.ad)}>
                    <span>{x.ad}</span>
                    <b data-num>{sayi(s.deger as number)}<small> {x.birim}</small></b>
                  </button>
                );
              })}
            </div>
            {g && (
              <div className="sbk-gosterge-d">
                <h4>{g.ad} <Atif id={g.kaynak} konum={g.konum} /></h4>
                {g.formul?.pay && (
                  <div className="sbk-formul">
                    <span className="sbk-kesir"><span>{g.formul.pay}</span><span>{g.formul.payda}</span></span>
                    {g.formul.katsayi ? <span>× {sayi(g.formul.katsayi)}</span> : null}
                  </div>
                )}
                {g.tanim && <MiniMetin metin={g.tanim} />}
                {(g.seri?.length || 0) > 1 && <CizgiGrafik baslik={g.ad} birim={g.birim} seriler={[{ ad: g.ad, seri: g.seri! }]} />}
              </div>
            )}
          </div>
        ) : <Bos />}
      </Blok>

      {gl.some((x) => x.formul?.pay) && (
        <Blok baslik="Gösterge hesaplayıcı" ikon={BookOpenCheck} alt="Sınavdaki hız-oran sorularını formülle çöz, Türkiye değeriyle karşılaştır">
          <GostergeHesap gostergeler={gl} />
        </Blok>
      )}

      {(on?.kalemler?.length || 0) > 0 && (
        <Blok baslik={`Ölüm nedenleri · ${on!.yil}`} ikon={ListOrdered} alt="Tüm ölümler içindeki pay (%)">
          <CubukListe
            kalemler={on!.kalemler!.map((k) => ({ ad: k.ad, deger: k.yuzde, ikinci: k.onceki?.yuzde, not: k.alt }))}
            birim="%" ondalik={1}
            birinciAd={String(on!.yil)} ikinciAd={on!.kalemler!.find((k) => k.onceki)?.onceki ? String(on!.kalemler!.find((k) => k.onceki)!.onceki!.yil) : undefined}
          />
          <p className="sbk-grafik-k">Kaynak <Atif id={on!.kaynak} konum={on!.konum} /></p>
        </Blok>
      )}

      {(on?.ilk_uc_seri?.length || 0) > 2 && (
        <Blok baslik="İlk üç ölüm nedeninin seyri" ikon={LineChart} alt="Tüm ölümler içindeki pay (%) — nedeni seç">
          <SeriSecici
            birim="%"
            seriler={([['dolasim', 'Dolaşım sistemi'], ['tumor', 'Tümörler'], ['solunum', 'Solunum sistemi']] as const).map(([k, ad]) => ({
              ad, seri: on!.ilk_uc_seri!.filter((x) => typeof x[k] === 'number').map((x) => ({ yil: x.yil, deger: x[k] as number })),
              kaynak: on!.ilk_uc_seri![on!.ilk_uc_seri!.length - 1].kaynak,
              ek: [...new Set(on!.ilk_uc_seri!.map((x) => x.kaynak).filter(Boolean) as string[])].slice(0, -1),
            }))}
            baslik={(ad) => `${ad} hastalıklarına bağlı ölümlerin payı`}
          />
        </Blok>
      )}
    </>
  );
};

/* =============================================================================================================== */
/* Halk sağlığı (müfredat haritası + temel sağlık hizmetleri)                                                       */
/* =============================================================================================================== */

export const HalkSagligiBolum: React.FC<BolumProps> = ({ v, git }) => {
  const m = v.baglantilar.mufredat || [];
  const kurullar = [...new Set(m.map((x) => x.kurul))].sort();
  const mx = Math.max(1, ...m.map((x) => x.cikmis));
  return (
    <>
      <Blok baslik="Halk sağlığı müfredat haritası" ikon={GraduationCap} alt="Dönem 3'teki tüm Halk Sağlığı ve Aile Hekimliği konuları; çubuk = çıkmış soru sayısı" genis>
        <div className="sbk-mufredat">
          {kurullar.map((k) => (
            <section key={k}>
              <h4>Kurul {k}</h4>
              <ul>
                {m.filter((x) => x.kurul === k).map((x) => (
                  <li key={x.anahtar}>
                    <IcBag to={kazanimBag(x.kurul, x.anahtar)} className="sbk-mufredat-a">
                      <span className="sbk-mufredat-t">{x.konu}<small>{x.ders} · {x.kazanim} kazanım</small></span>
                      <span className="sbk-hucre-cubuk"><i style={{ width: `${(x.cikmis / mx) * 100}%` }} /><b data-num>{x.cikmis}</b></span>
                    </IcBag>
                    {x.deste && <IcBag to={desteYolu(x.deste)} className="sbk-ikon-btn" title="Öğren destesini aç"><GraduationCap aria-hidden /></IcBag>}
                  </li>
                ))}
              </ul>
            </section>
          ))}
        </div>
      </Blok>

      {(v.turkiye.basamaklar?.length || 0) > 0 && (
        <Blok baslik="Temel sağlık hizmetleri" ikon={Building2} arac={<button type="button" className="sbk-btn" onClick={() => git('kurumlar')}>Sağlık kurumları <ArrowRight aria-hidden /></button>}>
          <BasamakPiramidi basamaklar={v.turkiye.basamaklar!} />
        </Blok>
      )}

      {(v.turkiye.tarihce?.length || 0) > 0 && (
        <Blok baslik="Türkiye'de halk sağlığının dönüm noktaları" ikon={History}>
          <ZamanCizgisi ogeler={[...v.turkiye.tarihce!].sort((a, b) => Number(a.yil) - Number(b.yil)).map((x) => ({ anahtar: `${x.yil}-${x.olay}`, zaman: x.yil, baslik: x.olay, kaynak: x.kaynak }))} />
        </Blok>
      )}
    </>
  );
};

export const BOLUM_BILESEN: Record<BolumId, React.FC<BolumProps>> = {
  genel: GenelBolum,
  karabuk: KarabukBolum,
  asi: AsiBolum,
  yenidogan: YenidoganBolum,
  anne_kadin: AnneKadinBolum,
  tarama: TaramaBolum,
  salgin: SalginBolum,
  cevre: CevreBolum,
  kurumlar: KurumlarBolum,
  istatistik: IstatistikBolum,
  halk_sagligi: HalkSagligiBolum,
};
