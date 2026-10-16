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
  /** patoloji (morfoloji/mekanizma/tanım…) · prognoz · tedavi (sorulabilir) · klinik bulgu (sorulmaz) */
  kategori?: 'patoloji' | 'prognoz' | 'tedavi' | 'klinik';
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
            {m.klinik && <span className="ol-dis">Klinik bulgu · sorulmaz</span>}
            {m.kategori === 'prognoz' && <span className="ol-kat k-prognoz">Prognoz · sorulabilir</span>}
            {m.kategori === 'tedavi' && <span className="ol-kat k-tedavi">Tedavi · sorulabilir</span>}
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
            {(m.kategori === 'prognoz' || m.kategori === 'tedavi') && <p className="ol-kat-g">{m.kategori === 'prognoz' ? 'Prognoz' : 'Tedavi'} bilgisi sınavda sorulabilir.</p>}
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

/** Önem listesi PDF'i — çoklu seçimli süzgeçler (bant, tür, kategori, kaynak, sınav adayı, çıkmışlı), içerik ve görünüm.
 *  Madde sayısı seçime göre anlık ve kesin (pencere açılınca kapsamdaki dersler yüklenir); dosya tarayıcıda üretilir (services/onemPdf.ts). */
type Kat = 'patoloji' | 'prognoz' | 'tedavi' | 'klinik';
const KAT_AD: Record<Kat, string> = { patoloji: 'Patoloji', prognoz: 'Prognoz', tedavi: 'Tedavi', klinik: 'Klinik bulgu' };
const KAYNAK_AD = { metin: 'Slayt metni', tablo: 'Tablo', sekil: 'Şekil/resim' } as const;
const tglSet = <T,>(s: Set<T>, v: T) => { const n = new Set(s); n.has(v) ? n.delete(v) : n.add(v); return n; };

const Cip: React.FC<{ on: boolean; onClick: () => void; cls?: string; children: React.ReactNode; sayi?: number }> = ({ on, onClick, cls = '', children, sayi }) => (
  <button type="button" className={`ol-bchip ${cls}${on ? ' is-on' : ''}`} onClick={onClick} aria-pressed={on}>{children}{sayi !== undefined && <small>{sayi}</small>}</button>
);

const PdfPenceresi: React.FC<{ dizin: Dizin; secili: string; yukle: (kodlar: string[]) => Promise<Ders[]>; onClose: () => void }> = ({ dizin, secili, yukle, onClose }) => {
  const tekDers = !!secili && secili !== HEPSI && secili !== ADAY;
  const [kapsam, setKapsam] = useState<'secili' | 'hepsi' | 'ozel'>(tekDers ? 'secili' : 'hepsi');
  const [ozel, setOzel] = useState<Set<string>>(() => new Set(tekDers ? [secili] : []));
  const [bant, setBant] = useState<Set<number>>(() => new Set([9, 8, 7]));
  const [turS, setTurS] = useState<Set<Tur>>(() => new Set());
  const [katS, setKatS] = useState<Set<Kat>>(() => new Set(['patoloji', 'prognoz', 'tedavi', 'klinik'] as Kat[]));
  const [kaynakS, setKaynakS] = useState<Set<string>>(() => new Set(['metin', 'tablo', 'sekil']));
  const [yalnizAday, setYalnizAday] = useState(false);
  const [yalnizCikmis, setYalnizCikmis] = useState(false);
  const [ic, setIc] = useState({ ozet: true, adaylarKutusu: true, alt: true, alinti: false, detay: false, ornekSoru: false, cikmis: false });
  const [anahtar, setAnahtar] = useState<'ders' | 'son' | 'yok'>('ders');
  const [gor, setGor] = useState({ format: 'a4' as 'a4' | 'tablet', renk: 'renkli' as 'renkli' | 'gri', buyuk: false, yeniSayfa: true, icindekiler: true, siralama: 'puan' as 'puan' | 'slayt' });
  const [calisiyor, setCalisiyor] = useState(false);
  const [veri, setVeri] = useState<Ders[] | null>(null);

  const kodlar = useMemo(() => (kapsam === 'secili' ? [secili] : kapsam === 'hepsi' ? dizin.dersler.map((d) => d.kod) : dizin.dersler.map((d) => d.kod).filter((k) => ozel.has(k))), [kapsam, secili, dizin, ozel]);
  useEffect(() => { let alive = true; setVeri(null); if (kodlar.length) yukle(kodlar).then((r) => alive && setVeri(r)).catch(() => alive && setVeri([])); else setVeri([]); return () => { alive = false; }; }, [kodlar.join(',')]); // eslint-disable-line react-hooks/exhaustive-deps

  const uyar = (d: Ders, m: Madde) => {
    if (!bant.has(bantOf(m.puan))) return false;
    if (turS.size && !turS.has(m.tur)) return false;
    if (!katS.has((m.kategori || (m.klinik ? 'klinik' : 'patoloji')) as Kat)) return false;
    if (!kaynakS.has(m.kaynak || 'metin')) return false;
    if (yalnizAday && !(d.sinavAdaylari || []).some((a) => a.id === m.id)) return false;
    if (yalnizCikmis && !(m.cikmis || []).length) return false;
    return true;
  };
  const say = useMemo(() => {
    const r = { toplam: 0, bant: {} as Record<number, number>, tur: {} as Record<string, number>, kat: {} as Record<string, number>, kaynak: {} as Record<string, number>, soru: 0, cikmis: 0 };
    for (const d of veri || []) for (const m of d.maddeler) {
      const k = m.kategori || (m.klinik ? 'klinik' : 'patoloji');
      r.bant[bantOf(m.puan)] = (r.bant[bantOf(m.puan)] || 0) + 1; r.tur[m.tur] = (r.tur[m.tur] || 0) + 1;
      r.kat[k] = (r.kat[k] || 0) + 1; r.kaynak[m.kaynak || 'metin'] = (r.kaynak[m.kaynak || 'metin'] || 0) + 1;
      if (uyar(d, m)) { r.toplam++; if (m.ornek_soru) r.soru++; r.cikmis += (m.cikmis || []).length; }
    }
    return r;
  }, [veri, bant, turS, katS, kaynakS, yalnizAday, yalnizCikmis]); // eslint-disable-line react-hooks/exhaustive-deps

  const ozetSatirlari = () => {
    const out: string[] = [];
    out.push(`Puan: ${BANTLAR.filter((B) => bant.has(B.b)).map((B) => B.ad).join(', ')}`);
    if (turS.size) out.push(`Bilgi türü: ${[...turS].map((t) => TUR_AD[t]).join(', ')}`);
    if (katS.size < 4) out.push(`Kategori: ${[...katS].map((k) => KAT_AD[k]).join(', ')}`);
    if (kaynakS.size < 3) out.push(`Kaynak: ${[...kaynakS].map((k) => KAYNAK_AD[k as keyof typeof KAYNAK_AD]).join(', ')}`);
    if (yalnizAday) out.push('Yalnız sınav adayları');
    if (yalnizCikmis) out.push('Yalnız çıkmış sorusu olan maddeler');
    return out;
  };
  const indir = async () => {
    if (!veri?.length || !say.toplam) return;
    setCalisiyor(true);
    try {
      const { onemPdfOlustur } = await import('../../services/onemPdf');
      const ds = veri.map((d) => ({ ...d, maddeler: d.maddeler.filter((m) => uyar(d, m)) })).filter((d) => d.maddeler.length);
      const blob = await onemPdfOlustur(ds as any, { filtreOzeti: ozetSatirlari(), ...ic, anahtar, ...gor }, kapsam === 'secili' ? ds[0]?.baslik : `${ds.length} ders`);
      const ad = kapsam === 'secili' ? `${ds[0].no}_${ds[0].baslik}` : kapsam === 'hepsi' ? 'Tum_patoloji' : `${ds.length}_ders`;
      const url = URL.createObjectURL(blob);
      const el = document.createElement('a');
      el.href = url; el.download = `Patoloji_en_onemliler_${ad.replace(/[^\p{L}\p{N}]+/gu, '_')}.pdf`;
      document.body.appendChild(el); el.click(); el.remove();
      window.setTimeout(() => URL.revokeObjectURL(url), 30_000);
      toast?.success?.('PDF hazırlandı');
      onClose();
    } catch (e) {
      console.warn('Önem listesi PDF hatası:', e);
      toast?.error?.('PDF hazırlanamadı');
    } finally { setCalisiyor(false); }
  };
  const Kutu: React.FC<{ k: keyof typeof ic; ad: string; not?: string }> = ({ k, ad, not }) => (
    <label className="ol-pdf-ck"><input type="checkbox" checked={ic[k]} onChange={(e) => setIc((x) => ({ ...x, [k]: e.target.checked }))} /><span>{ad}{not && <small>{not}</small>}</span></label>
  );
  const hizli = (bs: number[]) => setBant(new Set(bs));
  return (
    <Dialog title="PDF indir" subtitle="Patoloji · Sınav için en önemliler" onClose={onClose} width="max-w-2xl"
      footer={<div className="ol-pdf-f"><span>{veri === null ? 'Sayılıyor…' : `${kodlar.length} ders · ${say.toplam} madde${ic.ornekSoru ? ` · ${say.soru} örnek soru` : ''}${ic.cikmis ? ` · ${say.cikmis} çıkmış` : ''}`}</span><button type="button" className="ol-btn is-dolu" disabled={calisiyor || !say.toplam} onClick={indir}><Download aria-hidden />{calisiyor ? 'Hazırlanıyor…' : 'PDF oluştur ve indir'}</button></div>}>
      <div className="ol-pdf">
        <fieldset>
          <legend>Dersler</legend>
          {tekDers && <label className="ol-pdf-r"><input type="radio" checked={kapsam === 'secili'} onChange={() => setKapsam('secili')} /> Seçili ders</label>}
          <label className="ol-pdf-r"><input type="radio" checked={kapsam === 'hepsi'} onChange={() => setKapsam('hepsi')} /> Tüm patoloji ({dizin.dersler.length} ders)</label>
          <label className="ol-pdf-r"><input type="radio" checked={kapsam === 'ozel'} onChange={() => setKapsam('ozel')} /> Seçeceğim dersler{kapsam === 'ozel' ? ` (${ozel.size})` : ''}</label>
          {kapsam === 'ozel' && (
            <>
              <div className="ol-pdf-mini"><button type="button" onClick={() => setOzel(new Set(dizin.dersler.map((d) => d.kod)))}>Tümünü seç</button><button type="button" onClick={() => setOzel(new Set())}>Temizle</button></div>
              <div className="ol-pdf-dersler">
                {dizin.dersler.map((d) => (
                  <label key={d.kod} className="ol-pdf-ck"><input type="checkbox" checked={ozel.has(d.kod)} onChange={() => setOzel((x) => tglSet(x, d.kod))} /><span>{d.no}) {d.baslik} <small>{d.madde} madde</small></span></label>
                ))}
              </div>
            </>
          )}
        </fieldset>

        <fieldset>
          <legend>Puan partları <em>çoklu seçim</em></legend>
          <div className="ol-pdf-puan">
            {BANTLAR.map((B) => <Cip key={B.b} cls={`b${B.b}`} on={bant.has(B.b)} onClick={() => setBant((s) => tglSet(s, B.b))} sayi={say.bant[B.b] || 0}>{B.ad}</Cip>)}
          </div>
          <div className="ol-pdf-mini"><span>Hızlı:</span><button type="button" onClick={() => hizli([9])}>90+</button><button type="button" onClick={() => hizli([9, 8])}>80+</button><button type="button" onClick={() => hizli([9, 8, 7])}>70+</button><button type="button" onClick={() => hizli([9, 8, 7, 6])}>60+</button><button type="button" onClick={() => hizli([9, 8, 7, 6, 5, 4])}>Hepsi</button></div>
        </fieldset>

        <fieldset>
          <legend>Bilgi türü <em>çoklu seçim · hiçbiri = hepsi</em></legend>
          <div className="ol-pdf-puan">
            {(Object.keys(TUR_AD) as Tur[]).map((t) => <Cip key={t} cls={`ol-turchip t-${t}`} on={turS.has(t)} onClick={() => setTurS((s) => tglSet(s, t))} sayi={say.tur[t] || 0}>{TUR_AD[t]}</Cip>)}
          </div>
        </fieldset>

        <fieldset>
          <legend>Sınav kuralı · kategori ve kaynak <em>çoklu seçim</em></legend>
          <div className="ol-pdf-puan">
            {(Object.keys(KAT_AD) as Kat[]).map((k) => <Cip key={k} cls={`ol-katchip k-${k}`} on={katS.has(k)} onClick={() => setKatS((s) => tglSet(s, k))} sayi={say.kat[k] || 0}>{KAT_AD[k]}{k === 'klinik' ? ' (sorulmaz)' : ''}</Cip>)}
          </div>
          <div className="ol-pdf-puan">
            {(Object.keys(KAYNAK_AD) as (keyof typeof KAYNAK_AD)[]).map((k) => <Cip key={k} on={kaynakS.has(k)} onClick={() => setKaynakS((s) => tglSet(s, k))} sayi={say.kaynak[k] || 0}>{KAYNAK_AD[k]}{k !== 'metin' ? ' (sorulmaz)' : ''}</Cip>)}
          </div>
          <div className="ol-pdf-mini"><span>Hızlı:</span>
            <button type="button" onClick={() => { setKatS(new Set(['patoloji', 'prognoz', 'tedavi'] as Kat[])); setKaynakS(new Set(['metin'])); }}>Yalnız sınava uygun</button>
            <button type="button" onClick={() => { setKatS(new Set(['patoloji', 'prognoz', 'tedavi', 'klinik'] as Kat[])); setKaynakS(new Set(['metin', 'tablo', 'sekil'])); }}>Hepsi</button>
          </div>
          <label className="ol-pdf-ck"><input type="checkbox" checked={yalnizAday} onChange={(e) => setYalnizAday(e.target.checked)} /><span>Yalnız sınav adayları<small>Her dersin sıralı adayları (her slayttan 1, Genetik'ten 2 soru)</small></span></label>
          <label className="ol-pdf-ck"><input type="checkbox" checked={yalnizCikmis} onChange={(e) => setYalnizCikmis(e.target.checked)} /><span>Yalnız çıkmış sorusu olan maddeler</span></label>
        </fieldset>

        <fieldset>
          <legend>İçerik</legend>
          <Kutu k="ozet" ad="Ders özeti ve “Neden önemli”" />
          <Kutu k="adaylarKutusu" ad="“Sınavda çıkabilecek” kutusu" not="Sıralı adaylar, en olası soru vurgulu" />
          <Kutu k="alt" ad="Alt maddeler" />
          <Kutu k="alinti" ad="PDF alıntısı (sayfa no ile)" />
          <Kutu k="detay" ad="Ayrıntılı açıklama" not="Dosya uzar" />
          <Kutu k="ornekSoru" ad="Örnek sorular" />
          <Kutu k="cikmis" ad="Çıkmış sorular" />
          {(ic.ornekSoru || ic.cikmis) && (
            <div className="ol-pdf-seg" role="radiogroup" aria-label="Cevap anahtarı">
              <span>Cevap anahtarı:</span>
              {([['ders', 'Ders sonunda'], ['son', 'Dosya sonunda'], ['yok', 'Yok']] as const).map(([v, ad]) => <Cip key={v} on={anahtar === v} onClick={() => setAnahtar(v)}>{ad}</Cip>)}
            </div>
          )}
        </fieldset>

        <fieldset>
          <legend>Görünüm</legend>
          <div className="ol-pdf-seg"><span>Sayfa:</span><Cip on={gor.format === 'a4'} onClick={() => setGor((g) => ({ ...g, format: 'a4' }))}>A4</Cip><Cip on={gor.format === 'tablet'} onClick={() => setGor((g) => ({ ...g, format: 'tablet' }))}>Tablet (3:4)</Cip></div>
          <div className="ol-pdf-seg"><span>Renk:</span><Cip on={gor.renk === 'renkli'} onClick={() => setGor((g) => ({ ...g, renk: 'renkli' }))}>Renkli</Cip><Cip on={gor.renk === 'gri'} onClick={() => setGor((g) => ({ ...g, renk: 'gri' }))}>Yazıcı dostu (gri)</Cip></div>
          <div className="ol-pdf-seg"><span>Dizim:</span><Cip on={gor.siralama === 'puan'} onClick={() => setGor((g) => ({ ...g, siralama: 'puan' }))}>Puan partları</Cip><Cip on={gor.siralama === 'slayt'} onClick={() => setGor((g) => ({ ...g, siralama: 'slayt' }))}>Slayt sırası</Cip></div>
          <label className="ol-pdf-ck"><input type="checkbox" checked={gor.buyuk} onChange={(e) => setGor((g) => ({ ...g, buyuk: e.target.checked }))} /><span>Büyük yazı</span></label>
          <label className="ol-pdf-ck"><input type="checkbox" checked={gor.yeniSayfa} onChange={(e) => setGor((g) => ({ ...g, yeniSayfa: e.target.checked }))} /><span>Her ders yeni sayfada</span></label>
          <label className="ol-pdf-ck"><input type="checkbox" checked={gor.icindekiler} onChange={(e) => setGor((g) => ({ ...g, icindekiler: e.target.checked }))} /><span>Kapakta içindekiler</span></label>
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
  const [katS, setKatS] = useState<'' | 'prognoz' | 'tedavi'>('');
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
      if (katS && m.kategori !== katS) continue;
      if (kod === HEPSI && !bantlar.size && !t.length && m.puan < 90) continue; // tüm patoloji: yalnız 90–100 (süzgeçsiz)
      if (t.length) {
        const h = kucuk(`${m.baslik} ${m.bilgi} ${(m.alt || []).join(' ')} ${m.detay}`);
        if (!t.every((x) => h.includes(x))) continue;
      }
      out.push({ m, d });
    }
    return out.sort((a, b) => b.m.puan - a.m.puan);
  }, [kaynak, kod, dq, bantlar, yalnizSinav, katS]);
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
        <b>Sınav kuralı:</b> resim ve tablolardan soru yok · klinik bulgu sorulmuyor (prognoz ve tedavi sorulabilir) · her ders slaytından <b>1 soru</b> (Genetik, Pediatrik ve Çevresel Patoloji'den <b>2 soru</b>).
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
            Yalnız sınava uygun<small>tablo/şekil/klinik bulgu hariç</small>
          </button>
          <button type="button" className={`ol-bchip ol-katchip k-prognoz${katS === 'prognoz' ? ' is-on' : ''}`} onClick={() => setKatS((v) => (v === 'prognoz' ? '' : 'prognoz'))} aria-pressed={katS === 'prognoz'}>Prognoz</button>
          <button type="button" className={`ol-bchip ol-katchip k-tedavi${katS === 'tedavi' ? ' is-on' : ''}`} onClick={() => setKatS((v) => (v === 'tedavi' ? '' : 'tedavi'))} aria-pressed={katS === 'tedavi'}>Tedavi</button>
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
