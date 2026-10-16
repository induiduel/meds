import React, { useDeferredValue, useEffect, useMemo, useState } from 'react';
import { BookOpen, ChevronDown, Download, FileText, History, HelpCircle, Search, Sparkles, Star, X } from 'lucide-react';
import { Dialog } from '../ui/Dialog';
import { toast } from '../ui/Toast';
import { Zengin, kucuk } from './spotsShared';
import '../../styles/onem-listesi.css';

/**
 * Patoloji · Sınav için en önemliler (100 puan). Veri: src/data/patoloji_onem_k1.json —
 * meds_temp/patoloji_onem/araclar/birlestir.py üretir; her madde Kurul 1 Tıbbi Patoloji ders PDF'inden birebir alıntılıdır
 * (araclar/dogrula.py alıntıyı ilgili PDF sayfasında, maddedeki her sayıyı PDF metninde arar). Sayfa yalnız gösterir.
 * Bantlar 10'ar puan ("part"); en önemliden (90–100) başlar. Madde satırı tek cümle hap bilgi; ayrıntı açılınca
 * PDF alıntısı + sayfa, neden önemli, uzun açıklama, örnek soru ve çıkmış sorular görünür.
 */

type Tur = 'tanim' | 'en_sik' | 'karakteristik' | 'sayi' | 'eslesme' | 'mekanizma' | 'siniflama' | 'tuzak' | 'tani_tedavi';
interface Soru { kok: string; secenekler: Record<string, string>; dogru: string; aciklama?: string }
interface Madde {
  id: string; puan: number; baslik: string; bilgi: string; alt?: string[]; tur: Tur;
  alinti: { sayfa: number; metin: string }[]; neden: string; detay: string; ornek_soru?: Soru | null; cikmis?: string[];
  /** sınav kuralı: tablo/şekilden ve klinik bulgudan soru yok */
  kaynak?: 'metin' | 'tablo' | 'sekil'; klinik?: boolean; sinavUygun?: boolean;
}
interface Aday { id: string; sira: number; gerekce: string }
interface Cikmis { sinav: string; kok: string; secenekler: Record<string, string>; dogru: string }
interface Ders { kod: string; no: number; baslik: string; pdf: string; ozet: string; neden_onemli: string; maddeler: Madde[]; cikmis: Record<string, Cikmis>; sinavAdaylari?: Aday[]; soruSayisi?: number }
interface DizinDers { kod: string; no: number; baslik: string; madde: number; bant?: Record<string, number> }
interface Dizin { surum: string; dersler: DizinDers[] }

/** Ders başına ayrı dosya: görünüm yalnız seçilen dersi indirir (tümü ~1,8 MB). */
const DOSYALAR = import.meta.glob('../../data/patoloji_onem/[0-9]*.json') as Record<string, () => Promise<{ default: Ders }>>;
const yukleyici = (kod: string) => DOSYALAR[`../../data/patoloji_onem/${kod}.json`];

const TUR_AD: Record<Tur, string> = {
  tanim: 'Tanım', en_sik: 'En sık', karakteristik: 'Karakteristik', sayi: 'Sayı', eslesme: 'Eşleşme',
  mekanizma: 'Mekanizma', siniflama: 'Sınıflama', tuzak: 'Tuzak', tani_tedavi: 'Tanı',
};
const BANTLAR = [
  { b: 9, ad: '90–100', not: 'Olmazsa olmaz' },
  { b: 8, ad: '80–89', not: 'Çok sık sorulur' },
  { b: 7, ad: '70–79', not: 'Sık sorulur' },
  { b: 6, ad: '60–69', not: 'Bilinmeli' },
  { b: 5, ad: '50–59', not: 'Destekleyici' },
  { b: 4, ad: '0–49', not: 'Ayrıntı' },
];
const bantOf = (p: number) => Math.max(4, Math.min(9, Math.floor(p / 10)));
const HEPSI = '*';
const ADAY = '#';

/** detay: "- **Başlık:** metin" satırları → madde listesi; diğer satırlar paragraf */
const Detay: React.FC<{ metin: string }> = ({ metin }) => {
  const satirlar = metin.split('\n').map((s) => s.trim()).filter(Boolean);
  const out: React.ReactNode[] = []; let liste: string[] = [];
  const bosalt = () => { if (liste.length) { out.push(<ul key={out.length}>{liste.map((x, i) => <li key={i}><Zengin metin={x} /></li>)}</ul>); liste = []; } };
  for (const s of satirlar) {
    if (/^[-•]\s+/.test(s)) liste.push(s.replace(/^[-•]\s+/, ''));
    else { bosalt(); out.push(<p key={out.length}><Zengin metin={s} /></p>); }
  }
  bosalt();
  return <div className="ol-detay">{out}</div>;
};

const SoruKart: React.FC<{ s: Soru | Cikmis; baslik: string; ust?: string }> = ({ s, baslik, ust }) => {
  const [acik, setAcik] = useState(false);
  return (
    <div className="ol-soru">
      <div className="ol-soru-h"><span>{baslik}</span>{ust && <em>{ust}</em>}</div>
      <p className="ol-soru-k">{s.kok}</p>
      <ol className="ol-soru-s">
        {Object.entries(s.secenekler).map(([k, v]) => (
          <li key={k} className={acik && k === s.dogru ? 'is-dogru' : ''}><b>{k})</b> {v}</li>
        ))}
      </ol>
      {acik ? (
        <p className="ol-soru-c">Cevap: <b>{s.dogru}</b>{'aciklama' in s && s.aciklama ? <> — {s.aciklama}</> : null}</p>
      ) : (
        <button type="button" className="ol-btn" onClick={() => setAcik(true)}>Cevabı göster</button>
      )}
    </div>
  );
};

const MaddeSatir: React.FC<{ m: Madde; d: Ders; gosterDers: boolean }> = ({ m, d, gosterDers }) => {
  const cikmis = d.cikmis || {};
  const aday = (d.sinavAdaylari || []).find((a) => a.id === m.id);
  const enOlasi = !!aday && aday.sira <= (d.soruSayisi || 1);
  const [acik, setAcik] = useState(false);
  const cs = (m.cikmis || []).map((id) => [id, cikmis[id]] as const).filter(([, c]) => c);
  return (
    <li className={`ol-m b${bantOf(m.puan)}${acik ? ' is-open' : ''}${m.sinavUygun === false ? ' is-dis' : ''}${aday ? ' is-aday' : ''}`}>
      <button type="button" className="ol-m-row" onClick={() => setAcik((v) => !v)} aria-expanded={acik}>
        <span className="ol-puan" aria-label={`${m.puan} puan`}>{m.puan}</span>
        <span className="ol-m-t">
          <span className="ol-m-meta">
            <span className={`ol-tur t-${m.tur}`}>{TUR_AD[m.tur] || m.tur}</span>
            {aday && <span className={`ol-aday${enOlasi ? ' is-en' : ''}`}><Star aria-hidden />{enOlasi ? 'En olası soru' : `Sınav adayı ${aday.sira}`}</span>}
            {m.kaynak === 'tablo' && <span className="ol-dis">Tablo · sorulmaz</span>}
            {m.kaynak === 'sekil' && <span className="ol-dis">Şekil · sorulmaz</span>}
            {m.klinik && <span className="ol-dis">Klinik · sorulmaz</span>}
            {cs.length > 0 && <span className="ol-cik"><History aria-hidden />{cs.length} çıkmış</span>}
            {gosterDers && <span className="ol-dersad">{d.baslik}</span>}
          </span>
          <span className="ol-bilgi"><Zengin metin={m.bilgi} /></span>
          {m.alt && m.alt.length > 0 && <ul className="ol-alt">{m.alt.map((x, i) => <li key={i}><Zengin metin={x} /></li>)}</ul>}
        </span>
        <ChevronDown className="ol-chev" aria-hidden />
      </button>
      {acik && (
        <div className="ol-m-body">
          <section>
            <h4><FileText aria-hidden />PDF'ten alıntı</h4>
            {m.alinti.map((a, i) => (
              <blockquote key={i}>“{a.metin}”<cite>{d.pdf} · s. {a.sayfa}</cite></blockquote>
            ))}
          </section>
          <section>
            <h4><Sparkles aria-hidden />Neden önemli</h4>
            <p>{m.neden}</p>
            {aday && <p className="ol-aday-g"><Star aria-hidden /><span><b>{enOlasi ? 'En olası soru' : `Sınav adayı ${aday.sira}`}:</b> {aday.gerekce}</span></p>}
            {m.sinavUygun === false && <p className="ol-dis-g">Hocanın açıklamasına göre {m.kaynak === 'tablo' ? 'tablolardan' : m.kaynak === 'sekil' ? 'resim/şekillerden' : 'klinik bulgulardan'} soru sorulmayacak; bilgi olarak bilinmesi yeterli.</p>}
          </section>
          <section>
            <h4><BookOpen aria-hidden />Ayrıntılı açıklama</h4>
            <Detay metin={m.detay} />
          </section>
          {m.ornek_soru && <section><SoruKart s={m.ornek_soru} baslik="Örnek soru" /></section>}
          {cs.length > 0 && (
            <section>
              <h4><History aria-hidden />Çıkmış soru{cs.length > 1 ? 'lar' : ''}</h4>
              {cs.map(([id, c]) => <SoruKart key={id} s={c} baslik="Çıkmış" ust={c.sinav} />)}
            </section>
          )}
        </div>
      )}
    </li>
  );
};

/** Önem listesi PDF'i — dersler, en düşük puan ve içerik seçimi; dosya tarayıcıda üretilir (services/onemPdf.ts). */
const PdfPenceresi: React.FC<{ dizin: Dizin; secili: string; yukle: (kodlar: string[]) => Promise<Ders[]>; onClose: () => void }> = ({ dizin, secili, yukle, onClose }) => {
  const [kapsam, setKapsam] = useState<'secili' | 'hepsi' | 'ozel'>(secili && secili !== HEPSI && secili !== ADAY ? 'secili' : 'hepsi');
  const [ozel, setOzel] = useState<Set<string>>(() => new Set(secili && secili !== HEPSI && secili !== ADAY ? [secili] : []));
  const [minPuan, setMinPuan] = useState(70);
  const [sec, setSec] = useState({ yalnizSinav: false, adaylarKutusu: true, alt: true, alinti: false, detay: false, ornekSoru: false, cikmis: false });
  const [calisiyor, setCalisiyor] = useState(false);
  const kodlar = kapsam === 'secili' ? [secili] : kapsam === 'hepsi' ? dizin.dersler.map((d) => d.kod) : dizin.dersler.map((d) => d.kod).filter((k) => ozel.has(k));
  const tahmini = dizin.dersler.filter((d) => kodlar.includes(d.kod)).reduce((n, d: any) => n + Object.entries(d.bant || {}).filter(([b]) => Number(b) * 10 >= Math.floor(minPuan / 10) * 10 || (Number(b) === 4 && minPuan === 0)).reduce((x, [, v]) => x + Number(v), 0), 0);
  const indir = async () => {
    if (!kodlar.length) return;
    setCalisiyor(true);
    try {
      const [ds, { onemPdfOlustur }] = await Promise.all([yukle(kodlar), import('../../services/onemPdf')]);
      const blob = await onemPdfOlustur(ds as any, { minPuan, ...sec }, kapsam === 'secili' ? ds[0]?.baslik : `${ds.length} ders`);
      const ad = kapsam === 'secili' ? `${ds[0].no}_${ds[0].baslik}` : kapsam === 'hepsi' ? 'Tum_patoloji' : `${ds.length}_ders`;
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url; a.download = `Patoloji_en_onemliler_${ad.replace(/[^\p{L}\p{N}]+/gu, '_')}_${minPuan}+.pdf`;
      document.body.appendChild(a); a.click(); a.remove();
      window.setTimeout(() => URL.revokeObjectURL(url), 30_000);
      toast?.success?.('PDF hazırlandı');
      onClose();
    } catch (e) {
      console.warn('Önem listesi PDF hatası:', e);
      toast?.error?.('PDF hazırlanamadı');
    } finally { setCalisiyor(false); }
  };
  const Kutu: React.FC<{ k: keyof typeof sec; ad: string; not?: string }> = ({ k, ad, not }) => (
    <label className="ol-pdf-ck"><input type="checkbox" checked={sec[k]} onChange={(e) => setSec((x) => ({ ...x, [k]: e.target.checked }))} /><span>{ad}{not && <small>{not}</small>}</span></label>
  );
  return (
    <Dialog title="PDF indir" subtitle="Patoloji · Sınav için en önemliler" onClose={onClose}
      footer={<div className="ol-pdf-f"><span>{kodlar.length} ders · ~{tahmini} madde</span><button type="button" className="ol-btn is-dolu" disabled={calisiyor || !kodlar.length} onClick={indir}>{calisiyor ? 'Hazırlanıyor…' : 'PDF oluştur ve indir'}</button></div>}>
      <div className="ol-pdf">
        <fieldset>
          <legend>Dersler</legend>
          {secili && secili !== HEPSI && secili !== ADAY && <label className="ol-pdf-r"><input type="radio" checked={kapsam === 'secili'} onChange={() => setKapsam('secili')} /> Seçili ders</label>}
          <label className="ol-pdf-r"><input type="radio" checked={kapsam === 'hepsi'} onChange={() => setKapsam('hepsi')} /> Tüm patoloji ({dizin.dersler.length} ders)</label>
          <label className="ol-pdf-r"><input type="radio" checked={kapsam === 'ozel'} onChange={() => setKapsam('ozel')} /> Seçeceğim dersler</label>
          {kapsam === 'ozel' && (
            <div className="ol-pdf-dersler">
              {dizin.dersler.map((d) => (
                <label key={d.kod} className="ol-pdf-ck"><input type="checkbox" checked={ozel.has(d.kod)} onChange={() => setOzel((x) => { const n = new Set(x); n.has(d.kod) ? n.delete(d.kod) : n.add(d.kod); return n; })} /><span>{d.no}) {d.baslik}</span></label>
              ))}
            </div>
          )}
        </fieldset>
        <fieldset>
          <legend>Hangi değerdeki spotlar</legend>
          <div className="ol-pdf-puan">
            {[90, 80, 70, 60, 50, 0].map((p) => (
              <button key={p} type="button" className={`ol-bchip b${Math.max(4, Math.floor(p / 10) || 4)}${minPuan === p ? ' is-on' : ''}`} onClick={() => setMinPuan(p)}>{p === 0 ? 'Hepsi' : `${p}+`}</button>
            ))}
          </div>
          <Kutu k="yalnizSinav" ad="Yalnız sınava uygun maddeler" not="Tablo, şekil ve klinik bulgu maddeleri çıkarılır" />
          <Kutu k="adaylarKutusu" ad="“Sınavda çıkabilecek” kutusu" not="Her dersin sıralı sınav adayları, en olası soru vurgulu" />
        </fieldset>
        <fieldset>
          <legend>İçerik</legend>
          <Kutu k="alt" ad="Alt maddeler" />
          <Kutu k="alinti" ad="PDF alıntısı (sayfa no ile)" />
          <Kutu k="detay" ad="Ayrıntılı açıklama" not="Dosya uzar" />
          <Kutu k="ornekSoru" ad="Örnek sorular" not="Cevap anahtarı ders sonunda" />
          <Kutu k="cikmis" ad="Çıkmış sorular" not="Cevap anahtarı ders sonunda" />
        </fieldset>
      </div>
    </Dialog>
  );
};

export const OnemListesi: React.FC = () => {
  const [dizin, setDizin] = useState<Dizin | null>(null);
  const [yuklu, setYuklu] = useState<Record<string, Ders>>({});
  const [hata, setHata] = useState(false);
  const [kod, setKod] = useState<string>(() => {
    try { return new URLSearchParams(location.search).get('ders') || localStorage.getItem('medsoru_onem_ders') || ''; } catch { return ''; }
  });
  const [q, setQ] = useState('');
  const dq = useDeferredValue(q);
  const [bantlar, setBantlar] = useState<Set<number>>(() => new Set());
  const [yalnizSinav, setYalnizSinav] = useState(false);
  const [pdfAcik, setPdfAcik] = useState(false);
  const cokDers = kod === HEPSI || kod === ADAY;

  useEffect(() => {
    let alive = true;
    import('../../data/patoloji_onem/index.json')
      .then((m) => { if (alive) setDizin((m as any).default as Dizin); })
      .catch(() => alive && setHata(true));
    return () => { alive = false; };
  }, []);
  useEffect(() => {
    if (!dizin) return;
    if (!kod || (!cokDers && !dizin.dersler.some((d) => d.kod === kod))) setKod(dizin.dersler[0]?.kod || HEPSI);
  }, [dizin, kod, cokDers]);
  useEffect(() => { try { if (kod) localStorage.setItem('medsoru_onem_ders', kod); } catch { /* özel pencere */ } }, [kod]);
  const yukle = React.useCallback(async (kodlar: string[]): Promise<Ders[]> => {
    const r = await Promise.all(kodlar.map((k) => (yuklu[k] ? Promise.resolve(yuklu[k]) : yukleyici(k)().then((m) => m.default))));
    setYuklu((y) => ({ ...y, ...Object.fromEntries(r.map((d) => [d.kod, d])) }));
    return r;
  }, [yuklu]);
  // Seçilen ders(ler)in dosyası; "tüm patoloji" / "sınav adayları" bütün dersleri paralel indirir
  useEffect(() => {
    if (!dizin || !kod) return;
    const gerek = (cokDers ? dizin.dersler.map((d) => d.kod) : [kod]).filter((k) => !yuklu[k] && yukleyici(k));
    if (!gerek.length) return;
    let alive = true;
    Promise.all(gerek.map((k) => yukleyici(k)().then((m) => [k, m.default] as const)))
      .then((r) => { if (alive) setYuklu((y) => ({ ...y, ...Object.fromEntries(r) })); })
      .catch(() => alive && setHata(true));
    return () => { alive = false; };
  }, [dizin, kod, cokDers, yuklu]);

  const ders = !cokDers ? yuklu[kod] || null : null;
  const kaynak = useMemo(
    () => (!dizin ? [] : cokDers ? dizin.dersler.map((d) => yuklu[d.kod]).filter(Boolean) : ders ? [ders] : []) as Ders[],
    [dizin, cokDers, ders, yuklu],
  );
  const hazir = !!dizin && (cokDers ? kaynak.length === dizin.dersler.length : !!ders);
  const liste = useMemo(() => {
    const t = kucuk(dq.trim()).split(/\s+/).filter(Boolean);
    const out: { m: Madde; d: Ders }[] = [];
    for (const d of kaynak) for (const m of d.maddeler) {
      if (bantlar.size && !bantlar.has(bantOf(m.puan))) continue;
      if (yalnizSinav && m.sinavUygun === false) continue;
      if (kod === HEPSI && !bantlar.size && !t.length && m.puan < 90) continue; // tüm patoloji: yalnız 90–100 (süzgeçsiz)
      if (t.length) {
        const h = kucuk(`${m.baslik} ${m.bilgi} ${(m.alt || []).join(' ')} ${m.detay}`);
        if (!t.every((x) => h.includes(x))) continue;
      }
      out.push({ m, d });
    }
    return out.sort((a, b) => b.m.puan - a.m.puan);
  }, [kaynak, kod, dq, bantlar, yalnizSinav]);
  const gruplu = useMemo(() => BANTLAR.map((B) => ({ ...B, items: liste.filter((x) => bantOf(x.m.puan) === B.b) })).filter((g) => g.items.length), [liste]);
  const toplam = useMemo(() => dizin?.dersler.reduce((s, d) => s + d.madde, 0) || 0, [dizin]);
  const adayMadde = (d: Ders) => (d.sinavAdaylari || []).map((a) => ({ a, m: d.maddeler.find((x) => x.id === a.id) })).filter((x) => x.m) as { a: Aday; m: Madde }[];

  if (hata) return <div className="ol-page"><p className="ol-bos">Önem listesi yüklenemedi.</p></div>;
  if (!dizin) return <div className="ol-page"><p className="ol-bos">Yükleniyor…</p></div>;
  const tglBant = (b: number) => setBantlar((s) => { const n = new Set(s); n.has(b) ? n.delete(b) : n.add(b); return n; });

  const AdayKutusu: React.FC<{ d: Ders; baslikli?: boolean }> = ({ d, baslikli }) => {
    const ad = adayMadde(d); const ns = d.soruSayisi || 1;
    if (!ad.length) return null;
    return (
      <section className="ol-adaylar">
        <h3><Star aria-hidden />{baslikli ? `${d.no}) ${d.baslik}` : 'Sınavda çıkabilecek'}<span>bu slayttan {ns} soru</span></h3>
        <ol>
          {ad.map(({ a, m }) => (
            <li key={a.id} className={a.sira <= ns ? 'is-en' : ''}>
              <span className="ol-aday-no">{a.sira}</span>
              <span className="ol-aday-t">
                <span className="ol-bilgi"><Zengin metin={m.bilgi} /></span>
                <small>{a.sira <= ns ? <b>En olası soru · </b> : null}{a.gerekce}</small>
              </span>
              <span className="ol-aday-p">{m.puan}</span>
            </li>
          ))}
        </ol>
      </section>
    );
  };

  return (
    <div className="ol-page">
      <header className="ol-head">
        <div>
          <h2>Patoloji · Sınav için en önemliler</h2>
          <p>100 puan üzerinden, 10'ar puanlık partlar · {dizin.dersler.length} ders · {toplam} madde · Kaynak: Kurul 1 Tıbbi Patoloji ders PDF'leri (her madde PDF alıntılı)</p>
        </div>
        <button type="button" className="ol-btn is-dolu ol-pdf-btn" onClick={() => setPdfAcik(true)}><Download aria-hidden />PDF indir</button>
      </header>

      <div className="ol-kural" role="note">
        <b>Sınav kuralı:</b> resim ve tablolardan soru yok · klinik bulgu sorulmuyor · her ders slaytından <b>1 soru</b> (Genetik, Pediatrik ve Çevresel Patoloji'den <b>2 soru</b>).
        <span><Star aria-hidden /> işaretli maddeler sınavda çıkabilecek adaylar; “En olası soru” en güçlü aday.</span>
      </div>

      <div className="ol-bar">
        <label className="ol-select">
          <span>Ders</span>
          <select value={kod} onChange={(e) => setKod(e.target.value)}>
            <option value={ADAY}>★ Sınav adayları (her dersten)</option>
            <option value={HEPSI}>Tüm patoloji (90–100 çekirdek)</option>
            {dizin.dersler.map((d) => <option key={d.kod} value={d.kod}>{d.no}) {d.baslik} · {d.madde}</option>)}
          </select>
        </label>
        <label className="ol-search">
          <Search aria-hidden />
          <input type="search" value={q} onChange={(e) => setQ(e.target.value)} placeholder="Bu listede ara" aria-label="Önem listesinde ara" />
          {q && <button type="button" onClick={() => setQ('')} aria-label="Aramayı temizle"><X /></button>}
        </label>
      </div>
      {kod !== ADAY && (
        <div className="ol-bantsec" role="group" aria-label="Puan bandı">
          <button type="button" className={`ol-bchip ol-sinavchip${yalnizSinav ? ' is-on' : ''}`} onClick={() => setYalnizSinav((v) => !v)} aria-pressed={yalnizSinav}>
            Yalnız sınava uygun<small>tablo/şekil/klinik hariç</small>
          </button>
          {BANTLAR.map((B) => (
            <button key={B.b} type="button" className={`ol-bchip b${B.b}${bantlar.has(B.b) ? ' is-on' : ''}`} onClick={() => tglBant(B.b)} aria-pressed={bantlar.has(B.b)}>
              {B.ad}<small>{B.not}</small>
            </button>
          ))}
        </div>
      )}

      {!hazir && <p className="ol-bos">Yükleniyor…</p>}

      {hazir && kod === ADAY && kaynak.map((d) => <AdayKutusu key={d.kod} d={d} baslikli />)}

      {ders && !cokDers && (
        <section className="ol-ders">
          <h3>{ders.no}) {ders.baslik}</h3>
          <p><Zengin metin={ders.ozet} /></p>
          <p className="ol-ders-neden"><HelpCircle aria-hidden /><span><b>Neden önemli:</b> <Zengin metin={ders.neden_onemli} /></span></p>
        </section>
      )}
      {ders && !cokDers && <AdayKutusu d={ders} />}

      {hazir && kod !== ADAY && gruplu.length === 0 && <p className="ol-bos">Bu süzgeçle madde yok.</p>}
      {kod !== ADAY && gruplu.map((g, i) => (
        <section key={g.b} className={`ol-part b${g.b}`}>
          <h3 className="ol-part-h">
            <span className="ol-part-no">Part {i + 1}</span>
            <span className="ol-part-ad">{g.ad} puan</span>
            <span className="ol-part-not">{g.not}</span>
            <span className="ol-part-n">{g.items.length}</span>
          </h3>
          <ul className="ol-list">
            {g.items.map(({ m, d }) => <MaddeSatir key={`${d.kod}-${m.id}`} m={m} d={d} gosterDers={cokDers} />)}
          </ul>
        </section>
      ))}
      {pdfAcik && <PdfPenceresi dizin={dizin} secili={kod} yukle={yukle} onClose={() => setPdfAcik(false)} />}
    </div>
  );
};

export default OnemListesi;
