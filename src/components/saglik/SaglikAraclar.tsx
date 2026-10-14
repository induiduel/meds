import React, { useMemo, useState } from 'react';
import { Check, ChevronDown, Eye, EyeOff, LayoutList, Search, Table2 } from 'lucide-react';
import { Atif, MiniMetin, useGenislik } from './SaglikOrtak';
import { kucukHarf, sayi, sonDeger, type AnneVeri, type AsiVeri, type Gosterge, type TurkiyeVeri } from './saglikVeri';

/* ===============================================================================================================
 * Aşı takvimi matrisi — satır aşı, sütun ziyaret. Sütun seçilince o ziyarette yapılacaklar listelenir.
 * "Ezber" modunda hücreler gizlenir; dokununca açılır (aktif hatırlama).
 * =============================================================================================================== */

const dozKisa = (d: string) => {
  const s = d.trim();
  const n = /^(\d+)\./.exec(s);
  if (n) return n[1];
  if (/rapel|pekiştir|hatırlat/i.test(s)) return 'R';
  if (/tek/i.test(s)) return '1';
  return s.slice(0, 2);
};

export const AsiTakvimi: React.FC<{ v: AsiVeri }> = ({ v }) => {
  const zamanlar = useMemo(() => [...(v.takvim_zamanlari || [])].sort((a, b) => a.ay - b.ay), [v.takvim_zamanlari]);
  const asilar = v.takvim || [];
  const [secili, setSecili] = useState<string>(() => zamanlar.find((z) => z.ay === 2)?.id || zamanlar[0]?.id || '');
  const [ezber, setEzber] = useState(false);
  const [acik, setAcik] = useState<Set<string>>(() => new Set());
  const [kapRef, genislik] = useGenislik<HTMLDivElement>();
  const [secimGorunum, setSecimGorunum] = useState<'tablo' | 'liste' | null>(null);
  // Dar kapta (telefon) tablo ekrana sığmaz → ziyaret listesi; kullanıcı isterse tabloya geçer
  const gorunum = secimGorunum ?? (genislik && genislik < 620 ? 'liste' : 'tablo');
  if (!zamanlar.length || !asilar.length) return null;
  const hucre = (asiId: string, zId: string) => asilar.find((a) => a.id === asiId)?.dozlar.filter((d) => d.zaman === zId) || [];
  const zIndex = Math.max(0, zamanlar.findIndex((z) => z.id === secili));
  const seciliZ = zamanlar[zIndex];
  const buZiyaret = asilar.flatMap((a) => a.dozlar.filter((d) => d.zaman === secili).map((d) => ({ a, d })));
  const ac = (k: string) => setAcik((p) => new Set(p).add(k));
  return (
    <div className="sbk-asi" ref={kapRef}>
      <div className="sbk-asi-arac">
        <label className="sbk-kaydir">
          <span>Ziyaret: <b>{seciliZ?.etiket}</b></span>
          <input
            type="range" min={0} max={zamanlar.length - 1} step={1} value={zIndex}
            onChange={(e) => setSecili(zamanlar[Number(e.target.value)].id)}
            aria-valuetext={seciliZ?.etiket}
          />
        </label>
        <div className="sbk-asi-dugmeler">
          <div className="sbk-seg" role="radiogroup" aria-label="Takvim görünümü">
            <button type="button" role="radio" aria-checked={gorunum === 'liste'} className={gorunum === 'liste' ? 'is-sec' : ''} onClick={() => setSecimGorunum('liste')}><LayoutList aria-hidden /> Ziyaret</button>
            <button type="button" role="radio" aria-checked={gorunum === 'tablo'} className={gorunum === 'tablo' ? 'is-sec' : ''} onClick={() => setSecimGorunum('tablo')}><Table2 aria-hidden /> Tablo</button>
          </div>
          <button type="button" className={`sbk-btn ${ezber ? 'is-dolu' : ''}`} onClick={() => { setEzber((x) => !x); setAcik(new Set()); }} aria-pressed={ezber}>
            {ezber ? <EyeOff aria-hidden /> : <Eye aria-hidden />} {ezber ? 'Ezber açık' : 'Ezber modu'}
          </button>
        </div>
      </div>
      {gorunum === 'liste' ? (
        <ol className="sbk-asi-liste" aria-label="Ziyaretlere göre aşılar">
          {zamanlar.map((z) => {
            const burada = asilar.flatMap((a) => a.dozlar.filter((d) => d.zaman === z.id).map((d) => ({ a, d })));
            return (
              <li key={z.id} className={z.id === secili ? 'is-sec' : ''}>
                <button type="button" className="sbk-asi-liste-z" onClick={() => setSecili(z.id)} aria-pressed={z.id === secili}>
                  <b>{z.etiket}</b><small>{burada.length ? `${burada.length} aşı` : 'rutin aşı yok'}</small>
                </button>
                <div className="sbk-asi-cipler">
                  {burada.map(({ a, d }) => {
                    const k = `${a.id}:${z.id}`;
                    return ezber && !acik.has(k) ? (
                      <button key={a.id} type="button" className="sbk-asi-cip is-gizli" onClick={() => ac(k)} aria-label={`${z.etiket}: gizli aşıyı göster`}>?</button>
                    ) : (
                      <span key={a.id} className="sbk-asi-cip" title={`${a.ad} — ${d.doz}`}><b>{a.kisa}</b><i>{dozKisa(d.doz)}</i></span>
                    );
                  })}
                </div>
              </li>
            );
          })}
        </ol>
      ) : (
      <div className="sbk-asi-kap" role="region" aria-label="Aşı takvimi tablosu" tabIndex={0}>
        <table className="sbk-asi-t">
          <thead>
            <tr>
              <th scope="col" className="sbk-asi-ilk">Aşı</th>
              {zamanlar.map((z) => (
                <th key={z.id} scope="col" className={z.id === secili ? 'is-sec' : ''}>
                  <button type="button" onClick={() => setSecili(z.id)} aria-pressed={z.id === secili}>{z.etiket}</button>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {asilar.map((a) => (
              <tr key={a.id}>
                <th scope="row" className="sbk-asi-ilk" title={`${a.ad}${a.hastaliklar?.length ? ` — ${a.hastaliklar.join(', ')}` : ''}`}>
                  <b>{a.kisa}</b><small>{a.hastaliklar?.join(', ') || a.ad}</small>
                </th>
                {zamanlar.map((z) => {
                  const d = hucre(a.id, z.id);
                  const k = `${a.id}:${z.id}`;
                  const gizli = ezber && d.length > 0 && !acik.has(k);
                  return (
                    <td key={z.id} className={`${z.id === secili ? 'is-sec' : ''} ${d.length ? 'is-dolu' : ''}`}>
                      {d.length > 0 && (gizli ? (
                        <button type="button" className="sbk-asi-gizli" onClick={() => ac(k)} aria-label={`${a.kisa}, ${z.etiket}: göster`}>?</button>
                      ) : (
                        <span className="sbk-asi-doz" title={`${a.ad} — ${z.etiket}: ${d.map((x) => x.doz).join(', ')}`}>{d.map((x) => dozKisa(x.doz)).join('·')}</span>
                      ))}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      )}
      <p className="sbk-muted sbk-asi-lejant">Sayı doz sırasıdır; R = rapel (pekiştirme), Ek = ek doz. Ziyarete dokun: o ziyaretin ayrıntısı aşağıda.</p>
      <div className="sbk-asi-ziyaret" aria-live="polite">
        <h4>
          {seciliZ?.etiket}: {buZiyaret.length ? `${buZiyaret.length} aşı` : 'bu ziyarette rutin aşı yok'}
          {ezber && buZiyaret.length > 0 && <span className="sbk-muted"> · açılan {buZiyaret.filter(({ a }) => acik.has(`${a.id}:${secili}`)).length}</span>}
        </h4>
        {seciliZ?.not && <p className="sbk-muted sbk-asi-znot">{seciliZ.not.replace(/\s*\((?:sb|tuik|rg)-[^)]*\)/g, '')}</p>}
        <ul>
          {buZiyaret.filter(({ a }) => !ezber || acik.has(`${a.id}:${secili}`)).map(({ a, d }) => (
            <li key={a.id}>
              <span className="sbk-asi-ad"><b>{a.kisa}</b> {a.ad}</span>
              <span className="sbk-muted">{d.doz}{a.yol ? ` · ${a.yol}` : ''}</span>
              {a.not && <small>{a.not}</small>}
              <span><Atif id={a.kaynak} />{a.ek_kaynaklar?.map((e) => <Atif key={e} id={e} />)}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

/* ===============================================================================================================
 * Gebelik haftası şeridi — dört gebe izlemi hafta aralıklarıyla. İzleme dokununca içeriği açılır.
 * =============================================================================================================== */

export const GebeIzlemSeridi: React.FC<{ izlemler: NonNullable<AnneVeri['dob_izlemleri']> }> = ({ izlemler }) => {
  const [kapRef, genislik] = useGenislik<HTMLDivElement>();
  return <div ref={kapRef}><GebeIzlemIc izlemler={izlemler} dar={!!genislik && genislik < 560} /></div>;
};

const GebeIzlemIc: React.FC<{ izlemler: NonNullable<AnneVeri['dob_izlemleri']>; dar: boolean }> = ({ izlemler, dar }) => {
  const [sec, setSec] = useState(izlemler[0]?.no ?? 1);
  const s = izlemler.find((x) => x.no === sec) || izlemler[0];
  if (!izlemler.length || !s) return null;
  const MAX = 42;
  // Dar kapta hafta şeridi okunmaz → dikey izlem kartları (her kartta 0–42 hafta içinde konumu gösteren ince çubuk)
  if (dar) {
    return (
      <div className="sbk-gebe is-dar">
        <ol className="sbk-gebe-kartlar" role="tablist" aria-label="Gebe izlemleri">
          {izlemler.map((x) => {
            const bas = x.hafta_bas ?? 0, son = x.hafta_son ?? bas + 2;
            const acik = x.no === sec;
            return (
              <li key={x.no} className={acik ? 'is-sec' : ''}>
                <button type="button" role="tab" aria-selected={acik} onClick={() => setSec(x.no)}>
                  <span className="sbk-gebe-no">{x.no}</span>
                  <span className="sbk-gebe-k">
                    <b>{bas}–{son}. hafta</b>
                    <small>{x.zaman}</small>
                    <span className="sbk-gebe-mini" aria-hidden><i style={{ left: `${(bas / MAX) * 100}%`, width: `${Math.max(3, ((son - bas) / MAX) * 100)}%` }} /></span>
                  </span>
                  <ChevronDown aria-hidden />
                </button>
                {acik && x.icerik?.length ? (
                  <div className="sbk-gebe-detay">
                    <ul>{x.icerik.map((m, i) => <li key={i}><BaslikliMadde metin={m} /></li>)}</ul>
                    <p className="sbk-grafik-k">Kaynak <Atif id={x.kaynak} /></p>
                  </div>
                ) : null}
              </li>
            );
          })}
        </ol>
      </div>
    );
  }
  return (
    <div className="sbk-gebe">
      <div className="sbk-gebe-serit" role="tablist" aria-label="Gebe izlemleri">
        <div className="sbk-gebe-eksen" aria-hidden>
          {[0, 10, 14, 20, 28, 37, 42].map((h) => <span key={h} style={{ left: `${(h / MAX) * 100}%`, transform: h === 0 ? 'none' : h === MAX ? 'translateX(-100%)' : undefined }}>{h}</span>)}
        </div>
        <div className="sbk-gebe-trimester" aria-hidden>
          <span style={{ width: `${(13 / MAX) * 100}%` }}>1. trimester</span>
          <span style={{ width: `${(14 / MAX) * 100}%` }}>2. trimester</span>
          <span style={{ width: `${(15 / MAX) * 100}%` }}>3. trimester</span>
        </div>
        <div className="sbk-gebe-izler">
          {izlemler.map((x) => {
            const bas = x.hafta_bas ?? 0, son = x.hafta_son ?? bas + 2;
            return (
              <button
                key={x.no} type="button" role="tab" aria-selected={x.no === sec}
                className={x.no === sec ? 'is-sec' : ''}
                style={{ left: `${(bas / MAX) * 100}%`, width: `${Math.max(4, ((son - bas) / MAX) * 100)}%` }}
                onClick={() => setSec(x.no)}
                title={`${x.no}. izlem: ${x.zaman}`}
              >
                {x.no}
              </button>
            );
          })}
        </div>
        <p className="sbk-muted">Gebelik haftası</p>
      </div>
      <div className="sbk-gebe-detay" role="tabpanel">
        <h4>{s.no}. izlem · {s.zaman} <Atif id={s.kaynak} /></h4>
        {s.icerik?.length ? <ul>{s.icerik.map((m, i) => <li key={i}><BaslikliMadde metin={m} /></li>)}</ul> : null}
      </div>
    </div>
  );
};

/** "Öykü: …" biçimli maddede baştaki kısa başlık kalın */
const BaslikliMadde: React.FC<{ metin: string }> = ({ metin }) => {
  const m = /^([^:]{2,34}):\s+(.*)$/s.exec(metin);
  return m ? <><b>{m[1]}:</b> {m[2]}</> : <>{metin}</>;
};

/* ===============================================================================================================
 * Dikey zaman çizgisi (lohusa, bebek-çocuk izlemi, tarihçe)
 * =============================================================================================================== */

export const ZamanCizgisi: React.FC<{
  ogeler: { anahtar: string; zaman: React.ReactNode; baslik?: React.ReactNode; icerik?: string[]; kaynak?: string }[];
  acilir?: boolean;
}> = ({ ogeler, acilir }) => {
  const [acik, setAcik] = useState<string | null>(acilir ? null : '');
  return (
    <ol className="sbk-zaman">
      {ogeler.map((o) => {
        const ac = !acilir || acik === o.anahtar;
        return (
          <li key={o.anahtar} className={ac ? 'is-acik' : ''}>
            <span className="sbk-zaman-n" aria-hidden />
            {acilir && o.icerik?.length ? (
              <button type="button" className="sbk-zaman-b" onClick={() => setAcik(acik === o.anahtar ? null : o.anahtar)} aria-expanded={ac}>
                <span className="sbk-zaman-z">{o.zaman}</span>
                {o.baslik && <span>{o.baslik}</span>}
                <ChevronDown aria-hidden />
              </button>
            ) : (
              <div className="sbk-zaman-b">
                <span className="sbk-zaman-z">{o.zaman}</span>
                {o.baslik && <span>{o.baslik} <Atif id={o.kaynak} /></span>}
              </div>
            )}
            {ac && o.icerik?.length ? (
              <ul className="sbk-zaman-ic">{o.icerik.map((m, i) => <li key={i}><BaslikliMadde metin={m} /></li>)}{acilir && o.kaynak && <li className="sbk-zaman-k"><Atif id={o.kaynak} /></li>}</ul>
            ) : null}
          </li>
        );
      })}
    </ol>
  );
};

/* ===============================================================================================================
 * Yaşa göre kanser taraması — yaş ve cinsiyet seç, hangi ulusal taramalar kapsıyor gör
 * =============================================================================================================== */

const yasAraligi = (hedef: string): [number, number] | null => {
  const m = /(\d{2})\s*[–\-—]\s*(\d{2})/.exec(hedef);
  return m ? [Number(m[1]), Number(m[2])] : null;
};
const cinsiyet = (hedef: string): 'k' | 'e' | 'her' => (/kadın/i.test(hedef) && !/erkek/i.test(hedef) ? 'k' : /erkek/i.test(hedef) && !/kadın/i.test(hedef) ? 'e' : 'her');

export const KanserTaramaYas: React.FC<{ liste: NonNullable<AnneVeri['kanser_taramalari']> }> = ({ liste }) => {
  const [yas, setYas] = useState(52);
  const [cins, setCins] = useState<'k' | 'e'>('k');
  const MIN = 20, MAX = 80;
  const satir = liste.map((t) => ({ t, ar: yasAraligi(t.hedef), c: cinsiyet(t.hedef) }));
  const uygun = satir.filter((s) => s.ar && yas >= s.ar[0] && yas <= s.ar[1] && (s.c === 'her' || s.c === cins));
  return (
    <div className="sbk-kanser">
      <div className="sbk-kanser-arac">
        <div className="sbk-seg" role="radiogroup" aria-label="Cinsiyet">
          <button type="button" role="radio" aria-checked={cins === 'k'} className={cins === 'k' ? 'is-sec' : ''} onClick={() => setCins('k')}>Kadın</button>
          <button type="button" role="radio" aria-checked={cins === 'e'} className={cins === 'e' ? 'is-sec' : ''} onClick={() => setCins('e')}>Erkek</button>
        </div>
        <label className="sbk-kaydir">
          <span>Yaş: <b data-num>{yas}</b></span>
          <input type="range" min={MIN} max={MAX} value={yas} onChange={(e) => setYas(Number(e.target.value))} />
        </label>
      </div>
      <div className="sbk-kanser-cizelge" aria-hidden>
        <div className="sbk-kanser-imlec" style={{ ['--oran' as string]: (yas - MIN) / (MAX - MIN) } as React.CSSProperties} />
        {satir.map(({ t, ar, c }) => (
          <div key={t.kanser} className={`sbk-kanser-s ${(c === 'her' || c === cins) ? '' : 'is-soluk'}`}>
            <span className="sbk-kanser-ad">{t.kanser}</span>
            <span className="sbk-kanser-iz">
              {ar && <i style={{ left: `${((ar[0] - MIN) / (MAX - MIN)) * 100}%`, width: `${((ar[1] - ar[0]) / (MAX - MIN)) * 100}%` }}><b>{ar[0]}–{ar[1]}</b></i>}
            </span>
          </div>
        ))}
        <div className="sbk-kanser-eksen">{[20, 30, 40, 50, 60, 70, 80].map((x) => <span key={x} style={{ left: `${((x - MIN) / (MAX - MIN)) * 100}%`, transform: x === MIN ? 'none' : x === MAX ? 'translateX(-100%)' : undefined }}>{x}</span>)}</div>
      </div>
      <div className="sbk-kanser-sonuc" aria-live="polite">
        <h4>{yas} yaşında {cins === 'k' ? 'kadın' : 'erkek'}: {uygun.length ? `${uygun.length} ulusal tarama` : 'ulusal kanser taraması kapsamında değil'}</h4>
        <ul>
          {uygun.map(({ t }) => (
            <li key={t.kanser}><b>{t.kanser}</b> — {t.yontem}, {t.aralik}{t.not ? <small> · {t.not}</small> : null} <Atif id={t.kaynak} /></li>
          ))}
        </ul>
      </div>
    </div>
  );
};

/* ===============================================================================================================
 * Tarama testi geçerliliği — 2×2 tablo → duyarlılık, seçicilik, kestirim değerleri
 * =============================================================================================================== */

export const TaramaTestiHesap: React.FC = () => {
  const [a, setA] = useState(90), [b, setB] = useState(40), [c, setC] = useState(10), [d, setD] = useState(860);
  const yuzde = (x: number, y: number) => (y > 0 ? `%${sayi((x / y) * 100, 1)}` : '—');
  const gir = (deger: number, ayarla: (n: number) => void, etiket: string) => (
    <input type="number" min={0} inputMode="numeric" value={deger} aria-label={etiket} onChange={(e) => ayarla(Math.max(0, Number(e.target.value) || 0))} />
  );
  const sonuc = [
    { ad: 'Duyarlılık (sensitivite)', f: 'a / (a + c)', v: yuzde(a, a + c), not: 'Hastaları doğru yakalama gücü' },
    { ad: 'Seçicilik (spesifite)', f: 'd / (b + d)', v: yuzde(d, b + d), not: 'Sağlamları doğru ayırma gücü' },
    { ad: 'Pozitif kestirim değeri', f: 'a / (a + b)', v: yuzde(a, a + b), not: 'Test pozitifken gerçekten hasta olma olasılığı' },
    { ad: 'Negatif kestirim değeri', f: 'd / (c + d)', v: yuzde(d, c + d), not: 'Test negatifken gerçekten sağlam olma olasılığı' },
    { ad: 'Prevalans (bu toplulukta)', f: '(a + c) / N', v: yuzde(a + c, a + b + c + d), not: 'Kestirim değerleri prevalansla değişir' },
    { ad: 'Doğruluk', f: '(a + d) / N', v: yuzde(a + d, a + b + c + d), not: '' },
  ];
  return (
    <div className="sbk-hesap">
      <table className="sbk-iki">
        <thead><tr><th /><th scope="col">Hasta</th><th scope="col">Sağlam</th></tr></thead>
        <tbody>
          <tr><th scope="row">Test +</th><td><span>a · gerçek pozitif</span>{gir(a, setA, 'a: gerçek pozitif')}</td><td><span>b · yalancı pozitif</span>{gir(b, setB, 'b: yalancı pozitif')}</td></tr>
          <tr><th scope="row">Test −</th><td><span>c · yalancı negatif</span>{gir(c, setC, 'c: yalancı negatif')}</td><td><span>d · gerçek negatif</span>{gir(d, setD, 'd: gerçek negatif')}</td></tr>
        </tbody>
      </table>
      <ul className="sbk-hesap-s" aria-live="polite">
        {sonuc.map((s) => (
          <li key={s.ad}><span>{s.ad}<small>{s.f}{s.not ? ` · ${s.not}` : ''}</small></span><b data-num>{s.v}</b></li>
        ))}
      </ul>
    </div>
  );
};

/* ===============================================================================================================
 * Gösterge hesaplayıcı — formülü olan göstergeyi seç, pay/payda gir, Türkiye son değeriyle karşılaştır
 * =============================================================================================================== */

export const GostergeHesap: React.FC<{ gostergeler: Gosterge[] }> = ({ gostergeler }) => {
  const formullu = gostergeler.filter((g) => g.formul?.pay && g.formul?.payda && g.formul?.katsayi);
  const [kod, setKod] = useState(formullu[0]?.kod || formullu[0]?.ad || '');
  const [pay, setPay] = useState(''), [payda, setPayda] = useState('');
  const g = formullu.find((x) => (x.kod || x.ad) === kod) || formullu[0];
  if (!g?.formul) return null;
  const p = Number(pay.replace(',', '.')), q = Number(payda.replace(',', '.'));
  const sonuc = p >= 0 && q > 0 && pay !== '' && payda !== '' ? (p / q) * (g.formul.katsayi || 1) : null;
  const tr = sonDeger(g);
  return (
    <div className="sbk-hesap">
      <label className="sbk-alan">
        <span>Gösterge</span>
        <select className="sbk-sec" value={kod} onChange={(e) => { setKod(e.target.value); setPay(''); setPayda(''); }}>
          {formullu.map((x) => <option key={x.kod || x.ad} value={x.kod || x.ad}>{x.ad}</option>)}
        </select>
      </label>
      <div className="sbk-formul" aria-label="Formül">
        <span className="sbk-kesir"><span>{g.formul.pay}</span><span>{g.formul.payda}</span></span>
        <span>× {sayi(g.formul.katsayi || 1)}</span>
      </div>
      <div className="sbk-hesap-gir">
        <label className="sbk-alan"><span>Pay</span><input inputMode="decimal" value={pay} onChange={(e) => setPay(e.target.value)} placeholder="ör. 450" /></label>
        <label className="sbk-alan"><span>Payda</span><input inputMode="decimal" value={payda} onChange={(e) => setPayda(e.target.value)} placeholder="ör. 50000" /></label>
      </div>
      <p className="sbk-hesap-sonuc" aria-live="polite">
        <span>Sonuç</span>
        <b data-num>{sonuc == null ? '—' : sayi(sonuc, 2)}</b>
        <small>{g.birim}</small>
        {tr && <span className="sbk-muted">Türkiye {tr.yil}: {sayi(tr.deger)} {g.birim} <Atif id={g.kaynak} konum={g.konum} /></span>}
      </p>
      {g.tanim && <MiniMetin metin={g.tanim} className="sbk-muted" />}
    </div>
  );
};

/* ===============================================================================================================
 * Bildirimi zorunlu hastalıklar — gruplar ve hızlı arama ("kuduz hangi grupta?")
 * =============================================================================================================== */

export const BildirimListesi: React.FC<{ v: NonNullable<TurkiyeVeri['bildirimi_zorunlu']> }> = ({ v }) => {
  const [q, setQ] = useState('');
  const [grup, setGrup] = useState('');
  const gruplar = v.gruplar || [];
  const guncel = v.guncel_liste?.hastaliklar || [];
  const [gorunum, setGorunum] = useState<'guncel' | 'grup'>(guncel.length ? 'guncel' : 'grup');
  const k = kucukHarf(q.trim());
  const sonuc = gruplar
    .filter((g) => !grup || g.grup === grup)
    .map((g) => ({ ...g, hastaliklar: k ? g.hastaliklar.filter((h) => kucukHarf(h).includes(k)) : g.hastaliklar }))
    .filter((g) => !k || g.hastaliklar.length);
  const guncelSonuc = k ? guncel.filter((h) => kucukHarf(h).includes(k)) : guncel;
  // Aranan hastalık 2004 gruplarında hangi gruptaydı (güncel listede ararken de gösterilir)
  const grubuNe = (h: string) => gruplar.find((g) => g.hastaliklar.some((x) => kucukHarf(x) === kucukHarf(h) || kucukHarf(h).startsWith(kucukHarf(x))))?.grup;
  return (
    <div className="sbk-bildirim">
      <div className="sbk-bildirim-arac">
        <label className="sbk-ara">
          <Search aria-hidden />
          <input type="search" value={q} onChange={(e) => setQ(e.target.value)} placeholder="Hastalık ara (ör. kuduz, kızamık, KKKA)" aria-label="Bildirimi zorunlu hastalıklarda ara" />
        </label>
        {guncel.length > 0 && gruplar.length > 0 && (
          <div className="sbk-seg" role="radiogroup" aria-label="Liste">
            <button type="button" role="radio" aria-checked={gorunum === 'guncel'} className={gorunum === 'guncel' ? 'is-sec' : ''} onClick={() => setGorunum('guncel')}>Güncel liste ({v.guncel_liste?.sayi ?? guncel.length})</button>
            <button type="button" role="radio" aria-checked={gorunum === 'grup'} className={gorunum === 'grup' ? 'is-sec' : ''} onClick={() => setGorunum('grup')}>A–D grupları</button>
          </div>
        )}
      </div>
      {gorunum === 'guncel' ? (
        <>
          {v.guncel_liste?.aciklama && <p className="sbk-muted sbk-bildirim-not">{v.guncel_liste.aciklama} <Atif id={v.kaynak} /></p>}
          <ul className="sbk-bildirim-guncel">
            {guncelSonuc.map((h) => { const g = grubuNe(h); return <li key={h}>{h}{g && <span className="sbk-grup-harf is-kucuk" title={`2004 rehberinde ${g} grubu`}>{g}</span>}</li>; })}
          </ul>
          {!guncelSonuc.length && <p className="sbk-muted">"{q}" güncel listede yok.</p>}
        </>
      ) : (
        <>
          <div className="sbk-seg sbk-bildirim-gsec" role="radiogroup" aria-label="Grup">
            <button type="button" role="radio" aria-checked={!grup} className={!grup ? 'is-sec' : ''} onClick={() => setGrup('')}>Tümü</button>
            {gruplar.map((g) => (
              <button key={g.grup} type="button" role="radio" aria-checked={grup === g.grup} className={grup === g.grup ? 'is-sec' : ''} onClick={() => setGrup(g.grup)}>{g.grup}</button>
            ))}
          </div>
          <div className="sbk-bildirim-g">
            {sonuc.map((g) => (
              <section key={g.grup} className="sbk-bildirim-k">
                <h4><span className="sbk-grup-harf">{g.grup}</span> {g.grup} grubu <span className="sbk-muted">· {g.hastaliklar.length}</span></h4>
                {g.kural && <p className="sbk-muted">{g.kural}</p>}
                <ul>{g.hastaliklar.map((h) => <li key={h}>{h}</li>)}</ul>
              </section>
            ))}
            {!sonuc.length && <p className="sbk-muted">"{q}" listede yok.</p>}
          </div>
          {v.not && <p className="sbk-muted sbk-bildirim-not">{v.not} <Atif id={v.gruplar_kaynak} konum={v.gruplar_konum} /></p>}
        </>
      )}
      {(v.genel_kurallar?.length || 0) > 0 && (
        <details className="sbk-acil sbk-bildirim-kural">
          <summary>Bildirim yükümlülüğünün genel kuralları</summary>
          <MaddeListesi maddeler={v.genel_kurallar!} kaynak={v.kaynak} />
        </details>
      )}
      <p className="sbk-muted">{v.yonetmelik} <Atif id={v.kaynak} /></p>
    </div>
  );
};

/* ===============================================================================================================
 * Basamak piramidi — birinci / ikinci / üçüncü basamak; seçilen basamağın kurumları
 * =============================================================================================================== */

export const BasamakPiramidi: React.FC<{ basamaklar: NonNullable<TurkiyeVeri['basamaklar']> }> = ({ basamaklar }) => {
  const [sec, setSec] = useState(0);
  // Piramitte yalnız "… basamak" ögeleri (birinci en altta, en geniş); sevk zinciri / tarihsel model altta ayrı sekme
  const kat = basamaklar.map((b, i) => ({ b, i })).filter(({ b }) => /basamak/i.test(b.basamak));
  const diger = basamaklar.map((b, i) => ({ b, i })).filter(({ b }) => !/basamak/i.test(b.basamak));
  const s = basamaklar[sec];
  if (!s) return null;
  return (
    <div className="sbk-piramit">
      <div>
        <div className="sbk-piramit-g" role="tablist" aria-label="Sağlık hizmeti basamakları">
          {[...kat].reverse().map(({ b, i }) => {
            const sira = kat.findIndex((x) => x.i === i);
            return (
              <button
                key={b.basamak} type="button" role="tab" aria-selected={i === sec}
                className={i === sec ? 'is-sec' : ''}
                style={{ width: `${Math.max(44, 100 - sira * 26)}%` }}
                onClick={() => setSec(i)}
              >
                {b.basamak}
              </button>
            );
          })}
        </div>
        {diger.length > 0 && (
          <div className="sbk-cip-l sbk-piramit-diger" role="tablist" aria-label="İlgili başlıklar">
            {diger.map(({ b, i }) => (
              <button key={b.basamak} type="button" role="tab" aria-selected={i === sec} className={`sbk-cip ${i === sec ? 'is-sec' : ''}`} onClick={() => setSec(i)}>{b.basamak}</button>
            ))}
          </div>
        )}
      </div>
      <div className="sbk-piramit-d" role="tabpanel">
        <h4>{s.basamak} <Atif id={s.kaynak} /></h4>
        {s.aciklama && <p>{s.aciklama}</p>}
        {s.kurumlar?.length ? <ul className="sbk-piramit-k">{s.kurumlar.map((k) => <li key={k}>{k}</li>)}</ul> : null}
      </div>
    </div>
  );
};

/* ===============================================================================================================
 * Küçük yardımcı: madde listesi (kaynaklı)
 * =============================================================================================================== */

export const MaddeListesi: React.FC<{ maddeler: (string | { madde?: string; ad?: string; deger?: number | string; not?: string; kaynak?: string })[]; kaynak?: string; isaret?: 'tik' | 'nokta' }> = ({ maddeler, kaynak, isaret = 'nokta' }) => (
  <ul className={`sbk-madde ${isaret === 'tik' ? 'is-tik' : ''}`}>
    {maddeler.map((m, i) => {
      if (typeof m === 'string') return <li key={i}>{isaret === 'tik' && <Check aria-hidden />}<span><MiniSatirIc metin={m} /></span></li>;
      return (
        <li key={i}>
          {isaret === 'tik' && <Check aria-hidden />}
          <span>
            {m.ad && <b>{m.ad}{m.deger != null ? ': ' : ''}</b>}
            {m.deger != null && <span data-num>{typeof m.deger === 'number' ? sayi(m.deger) : m.deger}</span>}
            {m.madde && <MiniSatirIc metin={m.madde} />}
            {m.not && <small> · {m.not}</small>}
            <Atif id={m.kaynak} />
          </span>
        </li>
      );
    })}
    {kaynak && <li className="sbk-madde-k"><Atif id={kaynak} /></li>}
  </ul>
);

const MiniSatirIc: React.FC<{ metin: string }> = ({ metin }) => (
  <>{metin.split(/(\*\*[^*]+\*\*)/g).map((p, i) => (p.startsWith('**') && p.endsWith('**') ? <strong key={i}>{p.slice(2, -2)}</strong> : <React.Fragment key={i}>{p}</React.Fragment>))}</>
);

