import React, { useDeferredValue, useEffect, useMemo, useState } from 'react';
import { BookOpen, ChevronDown, FileText, History, HelpCircle, Search, Sparkles, X } from 'lucide-react';
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
}
interface Cikmis { sinav: string; kok: string; secenekler: Record<string, string>; dogru: string }
interface Ders { kod: string; no: number; baslik: string; pdf: string; ozet: string; neden_onemli: string; maddeler: Madde[]; cikmis: Record<string, Cikmis> }
interface DizinDers { kod: string; no: number; baslik: string; madde: number }
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
  const [acik, setAcik] = useState(false);
  const cs = (m.cikmis || []).map((id) => [id, cikmis[id]] as const).filter(([, c]) => c);
  return (
    <li className={`ol-m b${bantOf(m.puan)}${acik ? ' is-open' : ''}`}>
      <button type="button" className="ol-m-row" onClick={() => setAcik((v) => !v)} aria-expanded={acik}>
        <span className="ol-puan" aria-label={`${m.puan} puan`}>{m.puan}</span>
        <span className="ol-m-t">
          <span className="ol-m-meta">
            <span className={`ol-tur t-${m.tur}`}>{TUR_AD[m.tur] || m.tur}</span>
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

  useEffect(() => {
    let alive = true;
    import('../../data/patoloji_onem/index.json')
      .then((m) => { if (alive) setDizin((m as any).default as Dizin); })
      .catch(() => alive && setHata(true));
    return () => { alive = false; };
  }, []);
  useEffect(() => {
    if (!dizin) return;
    if (!kod || (kod !== HEPSI && !dizin.dersler.some((d) => d.kod === kod))) setKod(dizin.dersler[0]?.kod || HEPSI);
  }, [dizin, kod]);
  useEffect(() => { try { if (kod) localStorage.setItem('medsoru_onem_ders', kod); } catch { /* özel pencere */ } }, [kod]);
  // Seçilen ders(ler)in dosyası; "tüm patoloji" bütün dersleri paralel indirir
  useEffect(() => {
    if (!dizin || !kod) return;
    const gerek = (kod === HEPSI ? dizin.dersler.map((d) => d.kod) : [kod]).filter((k) => !yuklu[k] && yukleyici(k));
    if (!gerek.length) return;
    let alive = true;
    Promise.all(gerek.map((k) => yukleyici(k)().then((m) => [k, m.default] as const)))
      .then((r) => { if (alive) setYuklu((y) => ({ ...y, ...Object.fromEntries(r) })); })
      .catch(() => alive && setHata(true));
    return () => { alive = false; };
  }, [dizin, kod, yuklu]);

  const ders = kod !== HEPSI ? yuklu[kod] || null : null;
  const kaynak = useMemo(
    () => (!dizin ? [] : kod === HEPSI ? dizin.dersler.map((d) => yuklu[d.kod]).filter(Boolean) : ders ? [ders] : []) as Ders[],
    [dizin, kod, ders, yuklu],
  );
  const hazir = !!dizin && (kod === HEPSI ? kaynak.length === dizin.dersler.length : !!ders);
  const liste = useMemo(() => {
    const t = kucuk(dq.trim()).split(/\s+/).filter(Boolean);
    const out: { m: Madde; d: Ders }[] = [];
    for (const d of kaynak) for (const m of d.maddeler) {
      if (bantlar.size && !bantlar.has(bantOf(m.puan))) continue;
      if (kod === HEPSI && !bantlar.size && !t.length && m.puan < 90) continue; // tüm patoloji: yalnız 90–100 (süzgeçsiz)
      if (t.length) {
        const h = kucuk(`${m.baslik} ${m.bilgi} ${(m.alt || []).join(' ')} ${m.detay}`);
        if (!t.every((x) => h.includes(x))) continue;
      }
      out.push({ m, d });
    }
    return out.sort((a, b) => b.m.puan - a.m.puan);
  }, [kaynak, kod, dq, bantlar]);
  const gruplu = useMemo(() => BANTLAR.map((B) => ({ ...B, items: liste.filter((x) => bantOf(x.m.puan) === B.b) })).filter((g) => g.items.length), [liste]);
  const toplam = useMemo(() => dizin?.dersler.reduce((s, d) => s + d.madde, 0) || 0, [dizin]);

  if (hata) return <div className="ol-page"><p className="ol-bos">Önem listesi yüklenemedi.</p></div>;
  if (!dizin) return <div className="ol-page"><p className="ol-bos">Yükleniyor…</p></div>;
  const tglBant = (b: number) => setBantlar((s) => { const n = new Set(s); n.has(b) ? n.delete(b) : n.add(b); return n; });

  return (
    <div className="ol-page">
      <header className="ol-head">
        <div>
          <h2>Patoloji · Sınav için en önemliler</h2>
          <p>100 puan üzerinden, 10'ar puanlık partlar · {dizin.dersler.length} ders · {toplam} madde · Kaynak: Kurul 1 Tıbbi Patoloji ders PDF'leri (her madde PDF alıntılı)</p>
        </div>
      </header>

      <div className="ol-bar">
        <label className="ol-select">
          <span>Ders</span>
          <select value={kod} onChange={(e) => setKod(e.target.value)}>
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
      <div className="ol-bantsec" role="group" aria-label="Puan bandı">
        {BANTLAR.map((B) => (
          <button key={B.b} type="button" className={`ol-bchip b${B.b}${bantlar.has(B.b) ? ' is-on' : ''}`} onClick={() => tglBant(B.b)} aria-pressed={bantlar.has(B.b)}>
            {B.ad}<small>{B.not}</small>
          </button>
        ))}
      </div>

      {ders && kod !== HEPSI && (
        <section className="ol-ders">
          <h3>{ders.no}) {ders.baslik}</h3>
          <p><Zengin metin={ders.ozet} /></p>
          <p className="ol-ders-neden"><HelpCircle aria-hidden /><span><b>Neden önemli:</b> <Zengin metin={ders.neden_onemli} /></span></p>
        </section>
      )}

      {!hazir && <p className="ol-bos">Yükleniyor…</p>}
      {hazir && gruplu.length === 0 && <p className="ol-bos">Bu süzgeçle madde yok.</p>}
      {gruplu.map((g, i) => (
        <section key={g.b} className={`ol-part b${g.b}`}>
          <h3 className="ol-part-h">
            <span className="ol-part-no">Part {i + 1}</span>
            <span className="ol-part-ad">{g.ad} puan</span>
            <span className="ol-part-not">{g.not}</span>
            <span className="ol-part-n">{g.items.length}</span>
          </h3>
          <ul className="ol-list">
            {g.items.map(({ m, d }) => <MaddeSatir key={`${d.kod}-${m.id}`} m={m} d={d} gosterDers={kod === HEPSI} />)}
          </ul>
        </section>
      ))}
    </div>
  );
};

export default OnemListesi;
