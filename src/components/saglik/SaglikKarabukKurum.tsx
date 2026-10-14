import React, { useMemo, useState } from 'react';
import { Building2, ChevronDown, ExternalLink, History, Landmark, MapPin, Search } from 'lucide-react';
import { Atif, Blok, Kpi, OkunurTablo, Rozet } from './SaglikOrtak';
import { ZamanCizgisi } from './SaglikAraclar';
import type { MaddeOge } from './saglikBaglam';
import { kucukHarf, sayi, type KarabukVeri } from './saglikVeri';

/**
 * Karabük sağlık kurumları rehberi (karabuk.json › envanter): il ve ilçe sağlık müdürlükleri, birinci basamak
 * birimleri, hastaneler. Üstte tür tür sayılar, ortada ilçe × tür tablosu, altta süzülebilir kurum listesi.
 */

type Envanter = NonNullable<KarabukVeri['envanter']>;
type KurumT = NonNullable<Envanter['kurumlar']>[number];

const ILCE_SUTUN: { anahtar: string; ad: string }[] = [
  { anahtar: 'il_sm', ad: 'İl SM' }, { anahtar: 'ilce_sm', ad: 'İlçe SM' }, { anahtar: 'tsm', ad: 'TSM' }, { anahtar: 'asm', ad: 'ASM' },
  { anahtar: 'ahb', ad: 'Aile hek. birimi' }, { anahtar: 'hastane', ad: 'Hastane' }, { anahtar: 'istasyon_112', ad: '112 istasyonu' },
  { anahtar: 'kuduz', ad: 'Kuduz aşı merk.' }, { anahtar: 'evde_saglik', ad: 'Evde sağlık' },
];

const deger = (v: unknown): React.ReactNode => (v == null || v === '' ? '?' : typeof v === 'number' ? sayi(v) : Array.isArray(v) ? v.join(', ') : String(v));

const KurumKarti: React.FC<{ k: KurumT }> = ({ k }) => {
  const [acik, setAcik] = useState(false);
  const ayrinti = (k.gorev?.length || 0) > 0 || !!k.adres || !!k.not || !!k.bagli;
  return (
    <li className={`sbk-kk ${acik ? 'is-acik' : ''}`}>
      <button type="button" onClick={() => setAcik((x) => !x)} aria-expanded={acik} disabled={!ayrinti}>
        <span className="sbk-gezgin-ic">{/müdürlü/i.test(k.tur) ? <Landmark aria-hidden /> : <Building2 aria-hidden />}</span>
        <span className="sbk-gezgin-t"><b>{k.ad}</b><small>{[k.tur, k.ilce].filter(Boolean).join(' · ')}</small></span>
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
          {(k.gorev?.length || 0) > 0 && <ul className="sbk-madde">{k.gorev!.map((g, i) => <li key={i}>{g}</li>)}</ul>}
          {k.url && /^https:\/\/[^/]+\.(gov|edu|bel)\.tr/.test(k.url) && <a className="sbk-bag" href={k.url} target="_blank" rel="noopener noreferrer">Resmî sayfası <ExternalLink aria-hidden /></a>}
        </div>
      )}
    </li>
  );
};

export const KarabukKurumRehberi: React.FC<{ e?: Envanter }> = ({ e }) => {
  const kurumlar = e?.kurumlar || [];
  const [tur, setTur] = useState('');
  const [ilce, setIlce] = useState('');
  const [q, setQ] = useState('');
  const turler = useMemo(() => {
    const m = new Map<string, number>();
    for (const k of kurumlar) m.set(k.tur, (m.get(k.tur) || 0) + 1);
    return [...m.entries()].sort((a, b) => b[1] - a[1]);
  }, [kurumlar]);
  const ilceler = useMemo(() => [...new Set(kurumlar.map((k) => k.ilce).filter(Boolean) as string[])], [kurumlar]);
  const kq = kucukHarf(q.trim());
  const liste = kurumlar.filter((k) => (!tur || k.tur === tur) && (!ilce || k.ilce === ilce) && (!kq || kucukHarf(`${k.ad} ${k.tur} ${k.ilce} ${k.adres || ''}`).includes(kq)));
  if (!e || (!kurumlar.length && !e.ozet?.length)) return null;
  const mudurluk = (e.ozet || []).filter((x) => /müdürlü/i.test(x.tur));
  const diger = (e.ozet || []).filter((x) => !/müdürlü/i.test(x.tur));
  return (
    <>
      <Blok
        baslik="Karabük'te sağlık kurumları: kaç tane, nerede?" ikon={Landmark} genis
        alt="İl ve ilçe sağlık müdürlükleri ile bağlı birimler · kutuya dokun: adlar"
        maddeler={() => [
          ...(e.ozet || []).map((x) => ({ metin: `**${x.tur}**: ${sayi(x.sayi)}${x.yil ? ` (${x.yil})` : ''}${x.yontem ? ` — ${x.yontem}` : ''}`, kaynak: x.kaynak, konum: x.konum, alt: x.adlar?.length ? [x.adlar.join(', ')] : undefined } as MaddeOge)),
        ]}
      >
        {mudurluk.length > 0 && (
          <div className="sbk-kpi-grup sbk-kpi-grup-ilk">
            <h4>Yönetim kademesi</h4>
            <div className="sbk-kpi-g">{mudurluk.map((x) => <OzetKutu key={x.tur} x={x} />)}</div>
          </div>
        )}
        {diger.length > 0 && (
          <div className="sbk-kpi-grup">
            <h4>Bağlı birimler ve hastaneler</h4>
            <div className="sbk-kpi-g">{diger.map((x) => <OzetKutu key={x.tur} x={x} />)}</div>
          </div>
        )}
      </Blok>

      {(e.ilce_ozeti?.length || 0) > 0 && (
        <Blok
          baslik="İlçe ilçe sağlık örgütlenmesi" ikon={MapPin} genis alt="SM = sağlık müdürlüğü · TSM = toplum sağlığı merkezi · ? = resmî kaynakta teyit edilemedi · telefonda her ilçe bir kart"
          maddeler={() => e.ilce_ozeti!.map((x) => ({ metin: `**${x.ilce}**`, kaynak: x.kaynak, alt: [...ILCE_SUTUN.filter((s) => x[s.anahtar] != null).map((s) => `${s.ad}: ${deger(x[s.anahtar])}`), ...(x.diger?.length ? [`Diğer: ${x.diger.join(', ')}`] : [])] }))}
        >
          <OkunurTablo
            baslik="İlçelere göre sağlık kurumları"
            sutunlar={[{ anahtar: 'ilce', ad: 'İlçe' }, ...ILCE_SUTUN, { anahtar: 'diger', ad: 'Diğer birimler' }]}
            satirlar={e.ilce_ozeti!.map((x) => ({
              ilce: <span><b>{x.ilce}<Atif id={x.kaynak} /></b>{typeof x.not === 'string' && x.not ? <small className="sbk-muted sbk-blok-satir">{x.not}</small> : null}</span>,
              ...Object.fromEntries(ILCE_SUTUN.map((s) => [s.anahtar, deger(x[s.anahtar])])),
              diger: x.diger?.length ? <span className="sbk-etiketler">{x.diger.map((d) => <Rozet key={d}>{d}</Rozet>)}</span> : '—',
            }))}
          />
        </Blok>
      )}

      {kurumlar.length > 0 && (
        <Blok
          baslik="Kurum rehberi" ikon={Building2} genis alt={`${kurumlar.length} kurum · türe ve ilçeye göre süz, ara; kuruma dokun: bağlılık, adres, görevler`}
          maddeler={() => kurumlar.map((k) => ({ metin: `**${k.ad}** (${[k.tur, k.ilce].filter(Boolean).join(', ')})`, kaynak: k.kaynak, alt: [k.bagli && `Bağlı: ${k.bagli}`, k.adres && `Adres: ${k.adres}`, ...(k.gorev || []), k.not].filter(Boolean) as string[] }))}
        >
          <div className="sbk-cip-l" role="radiogroup" aria-label="Kurum türü">
            <button type="button" role="radio" aria-checked={!tur} className={`sbk-cip ${!tur ? 'is-sec' : ''}`} onClick={() => setTur('')}>Tümü ({kurumlar.length})</button>
            {turler.map(([t, n]) => <button key={t} type="button" role="radio" aria-checked={tur === t} className={`sbk-cip ${tur === t ? 'is-sec' : ''}`} onClick={() => setTur(t)}>{t} ({n})</button>)}
          </div>
          <div className="sbk-bildirim-arac">
            <label className="sbk-ara"><Search aria-hidden /><input type="search" value={q} onChange={(ev) => setQ(ev.target.value)} placeholder="Kurum ara (ör. Safranbolu, KETEM)" aria-label="Kurumlarda ara" /></label>
            {ilceler.length > 1 && (
              <select className="sbk-sec" value={ilce} onChange={(ev) => setIlce(ev.target.value)} aria-label="İlçe">
                <option value="">Tüm ilçeler</option>
                {ilceler.map((x) => <option key={x} value={x}>{x}</option>)}
              </select>
            )}
          </div>
          <ul className="sbk-kk-l">{liste.map((k) => <KurumKarti key={`${k.tur}-${k.ad}-${k.ilce || ''}`} k={k} />)}</ul>
          {!liste.length && <p className="sbk-bos">Eşleşen kurum yok.</p>}
        </Blok>
      )}

      {(e.tarihce?.length || 0) > 0 && (
        <Blok baslik="Karabük sağlık örgütlenmesinin tarihçesi" ikon={History} maddeler={() => e.tarihce!.map((x) => ({ metin: `**${x.yil}**: ${x.olay}`, kaynak: x.kaynak }))}>
          <ZamanCizgisi ogeler={[...e.tarihce!].sort((a, b) => String(a.yil).localeCompare(String(b.yil))).map((x) => ({ anahtar: `${x.yil}-${x.olay}`, zaman: x.yil, baslik: x.olay, kaynak: x.kaynak }))} />
        </Blok>
      )}
    </>
  );
};

const OzetKutu: React.FC<{ x: NonNullable<Envanter['ozet']>[number] }> = ({ x }) => {
  const [acik, setAcik] = useState(false);
  return (
    <div className="sbk-ozet-kutu">
      <Kpi ad={x.tur} deger={sayi(x.sayi)} yil={x.yil} kaynak={x.kaynak} konum={x.konum} not={x.yontem && /say/i.test(x.yontem) ? 'resmî listeden sayıldı' : undefined} ipucu={x.yontem} />
      {(x.adlar?.length || 0) > 0 && (
        <>
          <button type="button" className="sbk-link-btn" onClick={() => setAcik((v) => !v)} aria-expanded={acik}>{acik ? 'Adları gizle' : `Adlar (${x.adlar!.length})`}</button>
          {acik && <div className="sbk-etiketler sbk-ozet-adlar">{x.adlar!.map((a) => <Rozet key={a}>{a}</Rozet>)}</div>}
        </>
      )}
    </div>
  );
};
