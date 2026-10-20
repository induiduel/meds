import React, { useEffect, useMemo, useRef, useState } from 'react';
import {
  BookMarked, Check, Columns2, Download, Eye, FileText, Layers, List, ListChecks, Loader2, PenLine, Printer,
  RefreshCw, Scissors, Share2, SlidersHorizontal, Sparkles, X, Zap,
} from 'lucide-react';
import { Sheet } from '../../ui/Sheet';
import { toast } from '../../ui/Toast';
import { bransTanim, type Brans } from '../brans';
import type { OnemPdfMod, OnemPdfSecenek } from '../../../services/onemPdf';
import {
  BANTLAR, KAT_AD, KAYNAK_AD, PDF_KEY, TUR_AD, bantOf, dersAdi, dersYukle, katOf, ogrenilenler, tercihOku, tercihYaz,
  type Ders, type Dizin, type Kat, type Madde, type Tur,
} from './onemVeri';
import '../../../styles/spots.css';

const OnemPdfOnizleme = React.lazy(() => import('./OnemPdfOnizleme'));

/**
 * Önem listesi PDF penceresi. Soldaki ayarlar (şablon · kapsam · düzen modu · süzgeç · içerik · sayfa · görünüm · dosya),
 * sağda canlı önizleme (PDF.js). Telefonda iki sekme (Ayarlar | Önizleme), alt şeritte kesin sayılar + İndir.
 * Ayarlar cihazda ve profilde saklanır (medsoru_onem_pdf_v1); kapsam her açılışta ekrandaki seçimden başlar.
 */

type Ogr = 'hepsi' | 'haric' | 'yalniz';
interface Ayar {
  mod: OnemPdfMod;
  bant: number[]; tur: Tur[]; kat: Kat[]; kaynak: string[]; yalnizAday: boolean; yalnizCikmis: boolean; ogrenilen: Ogr;
  ozet: boolean; adaylarKutusu: boolean; alt: boolean; alinti: boolean; neden: boolean; detay: boolean; ornekSoru: boolean; cikmis: boolean;
  anahtar: 'ders' | 'son' | 'yok';
  sayfa: OnemPdfSecenek['sayfa']; yon: OnemPdfSecenek['yon']; sutun: 1 | 2; yazi: OnemPdfSecenek['yazi']; aralik: OnemPdfSecenek['aralik'];
  kenar: OnemPdfSecenek['kenar']; siralama: 'puan' | 'slayt'; renk: OnemPdfSecenek['renk'];
  kapak: boolean; icindekiler: boolean; yeniSayfa: boolean; numara: boolean; isaretKutusu: boolean; notAlani: boolean; optik: boolean;
}
const TUM_KAT: Kat[] = ['patoloji', 'prognoz', 'tedavi', 'klinik'];
const TUM_KAYNAK = ['metin', 'tablo', 'sekil'];
const VARSAYILAN: Ayar = {
  mod: 'liste', bant: [9, 8, 7], tur: [], kat: TUM_KAT, kaynak: TUM_KAYNAK, yalnizAday: false, yalnizCikmis: false, ogrenilen: 'hepsi',
  ozet: true, adaylarKutusu: true, alt: true, alinti: false, neden: false, detay: false, ornekSoru: false, cikmis: false, anahtar: 'ders',
  sayfa: 'a4', yon: 'dikey', sutun: 1, yazi: 'normal', aralik: 'normal', kenar: 'normal', siralama: 'puan', renk: 'renkli',
  kapak: true, icindekiler: true, yeniSayfa: true, numara: false, isaretKutusu: false, notAlani: false, optik: false,
};
const SINAVA_UYGUN = { kat: ['patoloji', 'prognoz', 'tedavi'] as Kat[], kaynak: ['metin'] };

const SABLONLAR: { id: string; ad: string; not: string; ikon: React.ReactNode; ayar: Partial<Ayar> }[] = [
  { id: 'gece', ad: 'Son gece tekrarı', not: '90+ ve 80+ · sınava uygun · 2 sütun sık', ikon: <Zap aria-hidden />,
    ayar: { mod: 'kompakt', bant: [9, 8], ...SINAVA_UYGUN, sutun: 2, aralik: 'sik', yazi: 'kucuk', alt: true, ozet: false, adaylarKutusu: true, yeniSayfa: false, kapak: false, ornekSoru: false, cikmis: false, alinti: false, detay: false, neden: false } },
  { id: 'aday', ad: 'Sınav adayları', not: 'Her dersin sıralı adayları + sorular', ikon: <Sparkles aria-hidden />,
    ayar: { mod: 'liste', bant: [9, 8, 7, 6, 5, 4], yalnizAday: true, adaylarKutusu: false, alt: true, neden: true, ornekSoru: true, cikmis: true, anahtar: 'ders', sutun: 1, yeniSayfa: false } },
  { id: 'kitap', ad: 'Tam çalışma kitabı', not: 'Tüm partlar · alıntı · açıklama · sorular', ikon: <BookMarked aria-hidden />,
    ayar: { mod: 'liste', bant: [9, 8, 7, 6, 5, 4], kat: TUM_KAT, kaynak: TUM_KAYNAK, yalnizAday: false, ozet: true, adaylarKutusu: true, alt: true, alinti: true, neden: true, detay: true, ornekSoru: true, cikmis: true, anahtar: 'ders', notAlani: true, sutun: 1, yeniSayfa: true, kapak: true, icindekiler: true } },
  { id: 'bosluk', ad: 'Boşluk doldurma', not: '70+ · anahtar terimler boş · cevaplar ders sonunda', ikon: <PenLine aria-hidden />,
    ayar: { mod: 'bosluk', bant: [9, 8, 7], ...SINAVA_UYGUN, alt: true, alinti: false, detay: false, ornekSoru: false, cikmis: false, anahtar: 'ders', aralik: 'rahat', sutun: 1 } },
  { id: 'soru', ad: 'Soru kitapçığı', not: 'Örnek + çıkmış · optik daireler · anahtar sonda', ikon: <ListChecks aria-hidden />,
    ayar: { mod: 'soru', bant: [9, 8, 7, 6, 5, 4], kat: TUM_KAT, kaynak: TUM_KAYNAK, yalnizAday: false, ornekSoru: true, cikmis: true, optik: true, anahtar: 'son', sutun: 1, yeniSayfa: false } },
  { id: 'kart', ad: 'Kesilebilir kartlar', not: '80+ · ön yüz başlık, arka yüz bilgi', ikon: <Scissors aria-hidden />,
    ayar: { mod: 'kart', bant: [9, 8], ...SINAVA_UYGUN, alt: true, ozet: false, renk: 'renkli', yeniSayfa: true } },
];

const MODLAR: { k: OnemPdfMod; ad: string; not: string; ikon: React.ReactNode }[] = [
  { k: 'liste', ad: 'Ayrıntılı liste', not: 'Rozet, etiket, ayrıntı', ikon: <List aria-hidden /> },
  { k: 'kompakt', ad: 'Kompakt özet', not: 'Sık, hap bilgi', ikon: <Columns2 aria-hidden /> },
  { k: 'bosluk', ad: 'Boşluk doldurma', not: 'Kalın terim boş', ikon: <PenLine aria-hidden /> },
  { k: 'soru', ad: 'Soru kitapçığı', not: 'Yalnız sorular', ikon: <ListChecks aria-hidden /> },
  { k: 'kart', ad: 'Kartlar', not: 'Kes, katla, çalış', ikon: <Scissors aria-hidden /> },
];

const tgl = <T,>(l: T[], v: T) => (l.includes(v) ? l.filter((x) => x !== v) : [...l, v]);

const Cip: React.FC<{ on: boolean; onClick: () => void; cls?: string; sayi?: number; children: React.ReactNode; disabled?: boolean }> = ({ on, onClick, cls = '', sayi, children, disabled }) => (
  <button type="button" className={`on-cip ${cls}${on ? ' is-on' : ''}`} onClick={onClick} aria-pressed={on} disabled={disabled}>
    {on && <Check className="on-cip-i" aria-hidden />}{children}{sayi !== undefined && <small>{sayi}</small>}
  </button>
);
function Seg<T extends string | number>({ ad, deger, secenekler, onChange }: { ad: string; deger: T; secenekler: [T, string][]; onChange: (v: T) => void }) {
  return (
    <div className="op-seg">
      <span className="op-seg-ad">{ad}</span>
      <div className="op-seg-g" role="radiogroup" aria-label={ad}>
        {secenekler.map(([v, l]) => (
          <button key={String(v)} type="button" role="radio" aria-checked={deger === v} className={deger === v ? 'is-on' : ''} onClick={() => onChange(v)}>{l}</button>
        ))}
      </div>
    </div>
  );
}
const Anahtar: React.FC<{ on: boolean; onChange: (v: boolean) => void; ad: string; not?: string; disabled?: boolean }> = ({ on, onChange, ad, not, disabled }) => (
  <label className={`op-sw${disabled ? ' is-dis' : ''}`}>
    <span className="op-sw-t"><b>{ad}</b>{not && <small>{not}</small>}</span>
    <input type="checkbox" role="switch" checked={on} disabled={disabled} onChange={(e) => onChange(e.target.checked)} />
    <span className="op-sw-k" aria-hidden />
  </label>
);
const Bolum: React.FC<{ no: number; ad: string; ek?: React.ReactNode; children: React.ReactNode }> = ({ no, ad, ek, children }) => (
  <section className="op-bolum">
    <h3><span className="op-no">{no}</span>{ad}{ek && <em>{ek}</em>}</h3>
    {children}
  </section>
);

export interface EkranKapsami { ad: string; kodlar: string[]; uyar: (d: Ders, m: Madde) => boolean }

export const OnemPdfPenceresi: React.FC<{ brans?: Brans; dizin: Dizin; secili: string | null; ekran: EkranKapsami | null; onClose: () => void }> = ({ brans = 'patoloji', dizin, secili, ekran, onClose }) => {
  const bt = bransTanim(brans);
  const [a, setA0] = useState<Ayar>(() => tercihOku(PDF_KEY, VARSAYILAN));
  const [sablon, setSablon] = useState<string | null>(null);
  const setA = (p: Partial<Ayar>) => { setA0((x) => ({ ...x, ...p })); setSablon(null); };
  useEffect(() => { tercihYaz(PDF_KEY, a); }, [a]);
  const [kapsam, setKapsam] = useState<'secili' | 'ekran' | 'hepsi' | 'ozel'>(secili ? 'secili' : ekran ? 'ekran' : 'hepsi');
  const [ozel, setOzel] = useState<string[]>(() => (secili ? [secili] : []));
  const [sekme, setSekme] = useState<'ayar' | 'onizleme'>('ayar');
  const [veri, setVeri] = useState<Ders[] | null>(null);
  const [uretim, setUretim] = useState<number | null>(null);
  const [onizleme, setOnizleme] = useState<{ blob: Blob; sayfa: number; imza: string } | null>(null);
  const [dosyaAdi, setDosyaAdi] = useState('');
  const iptalRef = useRef(false);

  const kodlar = useMemo(() => {
    if (kapsam === 'secili' && secili) return [secili];
    if (kapsam === 'ekran' && ekran) return ekran.kodlar;
    if (kapsam === 'ozel') return dizin.dersler.map((d) => d.kod).filter((k) => ozel.includes(k));
    return dizin.dersler.map((d) => d.kod);
  }, [kapsam, secili, ekran, ozel, dizin]);
  const kodSig = kodlar.join(',');
  useEffect(() => {
    let canli = true; setVeri(null);
    Promise.all(kodlar.map((k) => dersYukle(k, brans))).then((r) => canli && setVeri(r)).catch(() => canli && setVeri([]));
    return () => { canli = false; };
  }, [kodSig]); // eslint-disable-line react-hooks/exhaustive-deps

  const ogr = ogrenilenler();
  const ekranModu = kapsam === 'ekran' && !!ekran;
  const uyar = (d: Ders, m: Madde) => {
    if (a.ogrenilen === 'haric' && ogr.has(m.id)) return false;
    if (a.ogrenilen === 'yalniz' && !ogr.has(m.id)) return false;
    if (ekranModu) return ekran!.uyar(d, m);
    if (!a.bant.includes(bantOf(m.puan))) return false;
    if (a.tur.length && !a.tur.includes(m.tur)) return false;
    if (bt.sinavKurali && !a.kat.includes(katOf(m))) return false;
    if (bt.sinavKurali && !a.kaynak.includes(m.kaynak || 'metin')) return false;
    if (bt.sinavKurali && a.yalnizAday && !(d.sinavAdaylari || []).some((x) => x.id === m.id)) return false;
    if (a.yalnizCikmis && !(m.cikmis || []).length) return false;
    return true;
  };
  const say = useMemo(() => {
    const r = { toplam: 0, ders: 0, soru: 0, cikmis: 0, bant: {} as Record<number, number>, tur: {} as Record<string, number>, kat: {} as Record<string, number>, kaynak: {} as Record<string, number>, ogr: 0 };
    for (const d of veri || []) {
      let dv = 0; const cg = new Set<string>();
      for (const m of d.maddeler) {
        const b = bantOf(m.puan), k = katOf(m), kn = m.kaynak || 'metin';
        r.bant[b] = (r.bant[b] || 0) + 1; r.tur[m.tur] = (r.tur[m.tur] || 0) + 1; r.kat[k] = (r.kat[k] || 0) + 1; r.kaynak[kn] = (r.kaynak[kn] || 0) + 1;
        if (ogr.has(m.id)) r.ogr++;
        if (!uyar(d, m)) continue;
        r.toplam++; dv++;
        if (m.ornek_soru) r.soru++;
        r.soru += m.ornek26?.length || 0;
        for (const id of m.cikmis || []) if (d.cikmis?.[id]) cg.add(id);
      }
      r.cikmis += cg.size;
      if (dv) r.ders++;
    }
    return r;
  }, [veri, a, ekranModu, ogr]); // eslint-disable-line react-hooks/exhaustive-deps
  const soruSayisi = (a.ornekSoru ? say.soru : 0) + (a.cikmis ? say.cikmis : 0);
  const bos = a.mod === 'soru' ? soruSayisi === 0 : say.toplam === 0;

  const ozetSatirlari = () => {
    const out: string[] = [];
    if (ekranModu) out.push(`Ekrandaki süzgeç: ${ekran!.ad}`);
    else {
      out.push(`Puan: ${BANTLAR.filter((B) => a.bant.includes(B.b)).map((B) => B.ad).join(', ')}`);
      if (a.tur.length) out.push(`Bilgi türü: ${a.tur.map((t) => TUR_AD[t]).join(', ')}`);
      if (bt.sinavKurali && a.kat.length < 4) out.push(`Kategori: ${a.kat.map((k) => KAT_AD[k]).join(', ')}`);
      if (bt.sinavKurali && a.kaynak.length < 3) out.push(`Kaynak: ${a.kaynak.map((k) => KAYNAK_AD[k as keyof typeof KAYNAK_AD]).join(', ')}`);
      if (bt.sinavKurali && a.yalnizAday) out.push('Yalnız sınav adayları');
      if (a.yalnizCikmis) out.push('Yalnız çıkmış sorusu olan maddeler');
    }
    if (a.ogrenilen === 'haric') out.push('Öğrendiklerim çıkarıldı');
    if (a.ogrenilen === 'yalniz') out.push('Yalnız öğrendiklerim');
    return out;
  };
  const dersler = useMemo(() => (veri || []).map((d) => ({ ...d, maddeler: d.maddeler.filter((m) => uyar(d, m)) })).filter((d) => d.maddeler.length), [veri, a, ekranModu]); // eslint-disable-line react-hooks/exhaustive-deps
  const kapsamAdi = kapsam === 'secili' && dersler[0] ? dersAdi(dersler[0]) : kapsam === 'hepsi' ? `${bt.hepsi} · ${dersler.length} ders` : `${dersler.length} ders`;
  const varsayilanAd = `${bt.ad}_${a.mod}_${kapsam === 'secili' && dersler[0] ? `${dersler[0].no}_${dersler[0].baslik}` : kapsam === 'hepsi' ? 'tum_dersler' : `${dersler.length}_ders`}`;
  const secenek = (): OnemPdfSecenek => ({
    mod: a.mod, baslik: kapsamAdi, filtreOzeti: ozetSatirlari(),
    ozet: a.ozet, adaylarKutusu: a.adaylarKutusu, alt: a.alt, alinti: a.alinti, neden: a.neden, detay: a.detay, ornekSoru: a.ornekSoru, cikmis: a.cikmis,
    anahtar: a.anahtar, sayfa: a.sayfa, yon: a.yon, sutun: a.sutun, yazi: a.yazi, aralik: a.aralik, kenar: a.kenar, siralama: a.siralama, renk: a.renk,
    kapak: a.kapak, icindekiler: a.icindekiler, yeniSayfa: a.yeniSayfa, numara: a.numara, isaretKutusu: a.isaretKutusu, notAlani: a.notAlani, optik: a.optik,
    brans: bt.ad, bransDers: bt.tam, sinavKurali: bt.sinavKurali,
  });
  const imza = JSON.stringify([kodSig, a, kapsam, veri ? veri.length : -1]);
  const guncel = !!onizleme && onizleme.imza === imza;

  const uret = async (): Promise<{ blob: Blob; sayfa: number } | null> => {
    if (!veri || bos) return null;
    if (guncel) return onizleme;
    iptalRef.current = false;
    setUretim(0);
    try {
      const { onemPdfOlustur } = await import('../../../services/onemPdf');
      const r = await onemPdfOlustur(dersler, secenek(), { ogrenilen: ogr, ilerleme: (x) => setUretim(x), iptal: () => iptalRef.current });
      setOnizleme({ ...r, imza });
      return r;
    } catch (e) {
      if ((e as Error)?.message !== 'iptal') { console.warn('Önem listesi PDF hatası:', e); toast?.error?.('PDF hazırlanamadı'); }
      return null;
    } finally { setUretim(null); }
  };
  // önizleme sekmesi açıkken (ya da geniş ekranda) ayar değişince kendiliğinden yenile; çok büyük seçimde elle
  const genis = useGenis();
  const otomatik = (genis || sekme === 'onizleme') && !bos && veri !== null && (a.mod === 'soru' ? soruSayisi : say.toplam) <= 450;
  useEffect(() => {
    if (!otomatik || guncel || uretim !== null) return;
    const t = window.setTimeout(() => { void uret(); }, 700);
    return () => window.clearTimeout(t);
  }, [otomatik, imza, guncel, uretim]); // eslint-disable-line react-hooks/exhaustive-deps

  const ad = () => `${(dosyaAdi.trim() || varsayilanAd).replace(/\.pdf$/i, '').replace(/[^\p{L}\p{N}]+/gu, '_').replace(/^_|_$/g, '')}.pdf`;
  const indir = async () => {
    const r = await uret(); if (!r) return;
    const url = URL.createObjectURL(r.blob);
    const el = document.createElement('a');
    el.href = url; el.download = ad();
    document.body.appendChild(el); el.click(); el.remove();
    window.setTimeout(() => URL.revokeObjectURL(url), 30_000);
    toast?.success?.(`PDF indirildi · ${r.sayfa} sayfa`);
  };
  const paylasilir = typeof navigator !== 'undefined' && typeof navigator.canShare === 'function';
  const paylas = async () => {
    const r = await uret(); if (!r) return;
    const f = new File([r.blob], ad(), { type: 'application/pdf' });
    try {
      if (navigator.canShare?.({ files: [f] })) await navigator.share({ files: [f], title: `${bt.ad} · Sınav için en önemliler` });
      else await indir();
    } catch { /* kullanıcı vazgeçti */ }
  };
  const yazdir = async () => {
    const r = await uret(); if (!r) return;
    const url = URL.createObjectURL(r.blob);
    const w = window.open(url, '_blank');
    if (!w) toast?.error?.('Açılır pencere engellendi; PDF\'i indirip yazdırabilirsin');
    window.setTimeout(() => URL.revokeObjectURL(url), 120_000);
  };

  const mod = a.mod;
  const listeli = mod === 'liste' || mod === 'kompakt' || mod === 'bosluk';
  const ozetMetni = veri === null ? 'Sayılıyor…'
    : mod === 'soru' ? `${say.ders} ders · ${soruSayisi} soru`
    : `${say.ders} ders · ${say.toplam} madde${a.ornekSoru || a.cikmis ? ` · ${soruSayisi} soru` : ''}`;

  const altSerit = (
    <div className="op-f">
      <span className="op-f-s" aria-live="polite"><b>{ozetMetni}</b>{guncel && onizleme ? <> · {onizleme.sayfa} sayfa</> : null}</span>
      <div className="op-f-b">
        <button type="button" className="op-btn is-ikincil" disabled={bos || uretim !== null || !veri} onClick={() => void yazdir()} title="Yeni sekmede aç / yazdır"><Printer aria-hidden /><span>Yazdır</span></button>
        {paylasilir && <button type="button" className="op-btn is-ikincil" disabled={bos || uretim !== null || !veri} onClick={() => void paylas()}><Share2 aria-hidden /><span>Paylaş</span></button>}
        <button type="button" className="op-btn" disabled={bos || uretim !== null || !veri} onClick={() => void indir()}><Download aria-hidden /><span>İndir</span></button>
      </div>
    </div>
  );
  return (
    <Sheet open onClose={onClose} width={1120} size="full" bare label="PDF oluştur" className="op-sheet" footer={altSerit}>
      <div className="op">
        <div className="op-ust">
        <header className="op-h">
          <div className="op-h-t">
            <h2>PDF oluştur</h2>
            <p>{bt.ad} · Sınav için en önemliler</p>
          </div>
          <button type="button" className="op-ikon" onClick={onClose} aria-label="Kapat"><X /></button>
        </header>
        <div className="op-tabs" role="tablist" aria-label="PDF penceresi">
          <button type="button" role="tab" aria-selected={sekme === 'ayar'} className={sekme === 'ayar' ? 'is-on' : ''} onClick={() => setSekme('ayar')}><SlidersHorizontal aria-hidden />Ayarlar</button>
          <button type="button" role="tab" aria-selected={sekme === 'onizleme'} className={sekme === 'onizleme' ? 'is-on' : ''} onClick={() => setSekme('onizleme')}>
            <Eye aria-hidden />Önizleme{guncel && onizleme ? <small>{onizleme.sayfa} s.</small> : null}
          </button>
        </div>
        </div>

        <div className={`op-govde is-${sekme}`}>
          <div className="op-ayar">
            <section className="op-sablon" aria-label="Hazır şablonlar">
              <h3>Hazır şablonlar</h3>
              <div className="op-sablon-l">
                {SABLONLAR.map((s) => (
                  <button key={s.id} type="button" className={`op-sablon-k${sablon === s.id ? ' is-on' : ''}`}
                    onClick={() => { setA0((x) => ({ ...x, ...s.ayar })); setSablon(s.id); }} aria-pressed={sablon === s.id}>
                    <span className="op-sablon-i">{s.ikon}</span>
                    <b>{s.ad}</b><small>{s.not}</small>
                  </button>
                ))}
              </div>
            </section>

            <Bolum no={1} ad="Hangi dersler">
              <div className="op-kapsam" role="radiogroup" aria-label="Kapsam">
                {secili && <Cip on={kapsam === 'secili'} onClick={() => setKapsam('secili')}>Bu ders</Cip>}
                {ekran && <Cip on={kapsam === 'ekran'} onClick={() => setKapsam('ekran')}>Ekrandaki liste</Cip>}
                <Cip on={kapsam === 'hepsi'} onClick={() => setKapsam('hepsi')} sayi={dizin.dersler.length}>{bt.hepsi}</Cip>
                <Cip on={kapsam === 'ozel'} onClick={() => setKapsam('ozel')} sayi={kapsam === 'ozel' ? ozel.length : undefined}>Seçeceğim dersler</Cip>
              </div>
              {ekranModu && <p className="op-not">Süzgeçler ekrandan alınır: <b>{ekran!.ad}</b>. Puan/tür süzgeçleri bu kapsamda kullanılmaz.</p>}
              {kapsam === 'ozel' && (
                <div className="op-dersler">
                  <div className="op-mini-s">
                    <button type="button" onClick={() => setOzel(dizin.dersler.map((d) => d.kod))}>Tümünü seç</button>
                    <button type="button" onClick={() => setOzel([])}>Temizle</button>
                  </div>
                  <div className="op-dersler-l">
                    {dizin.dersler.map((d) => (
                      <label key={d.kod} className={`op-ders${ozel.includes(d.kod) ? ' is-on' : ''}`}>
                        <input type="checkbox" checked={ozel.includes(d.kod)} onChange={() => setOzel((x) => tgl(x, d.kod))} />
                        <span className="op-ders-no">{d.no}</span><span className="op-ders-ad">{d.baslik}</span><small>{d.madde}</small>
                      </label>
                    ))}
                  </div>
                </div>
              )}
            </Bolum>

            <Bolum no={2} ad="Düzen">
              <div className="op-mod" role="radiogroup" aria-label="Düzen modu">
                {MODLAR.map((x) => (
                  <button key={x.k} type="button" role="radio" aria-checked={mod === x.k} className={`op-mod-k m-${x.k}${mod === x.k ? ' is-on' : ''}`}
                    onClick={() => setA({ mod: x.k, ...(x.k === 'soru' && !a.ornekSoru && !a.cikmis ? { ornekSoru: true, cikmis: true } : {}) })}>
                    <span className="op-mod-r" aria-hidden><i /><i /><i /><i /></span>
                    <span className="op-mod-t">{x.ikon}<b>{x.ad}</b></span>
                    <small>{x.not}</small>
                  </button>
                ))}
              </div>
            </Bolum>

            <Bolum no={3} ad="Hangi maddeler" ek={ekranModu ? 'ekrandan' : 'çoklu seçim'}>
              {!ekranModu && (
                <>
                  <div className="op-grup">
                    <span className="op-grup-ad">Puan partı</span>
                    <div className="op-cipler">
                      {BANTLAR.map((B) => <Cip key={B.b} cls={`b${B.b} is-bant`} on={a.bant.includes(B.b)} onClick={() => setA({ bant: tgl(a.bant, B.b) })} sayi={say.bant[B.b] || 0}>{B.ad}</Cip>)}
                    </div>
                    <div className="op-mini-s"><span>Hızlı</span>
                      {[[9], [9, 8], [9, 8, 7], [9, 8, 7, 6], [9, 8, 7, 6, 5, 4]].map((bs) => (
                        <button key={bs.length} type="button" className={a.bant.length === bs.length && bs.every((b) => a.bant.includes(b)) ? 'is-on' : ''} onClick={() => setA({ bant: bs })}>{bs.length === 6 ? 'Hepsi' : `${bs[bs.length - 1]}0+`}</button>
                      ))}
                    </div>
                  </div>
                  <div className="op-grup">
                    <span className="op-grup-ad">Bilgi türü <em>hiçbiri = hepsi</em></span>
                    <div className="op-cipler">
                      {(Object.keys(TUR_AD) as Tur[]).map((t) => <Cip key={t} cls={`t-${t} is-tur`} on={a.tur.includes(t)} onClick={() => setA({ tur: tgl(a.tur, t) })} sayi={say.tur[t] || 0}>{TUR_AD[t]}</Cip>)}
                    </div>
                  </div>
                  {bt.sinavKurali && <div className="op-grup">
                    <span className="op-grup-ad">Sınav kuralı</span>
                    <div className="op-cipler">
                      {TUM_KAT.map((k) => <Cip key={k} cls={`k-${k} is-kat`} on={a.kat.includes(k)} onClick={() => setA({ kat: tgl(a.kat, k) })} sayi={say.kat[k] || 0}>{KAT_AD[k]}{k === 'klinik' ? ' · sorulmaz' : ''}</Cip>)}
                      {TUM_KAYNAK.map((k) => <Cip key={k} on={a.kaynak.includes(k)} onClick={() => setA({ kaynak: tgl(a.kaynak, k) })} sayi={say.kaynak[k] || 0}>{KAYNAK_AD[k as keyof typeof KAYNAK_AD]}{k !== 'metin' ? ' · sorulmaz' : ''}</Cip>)}
                    </div>
                    <div className="op-mini-s"><span>Hızlı</span>
                      <button type="button" onClick={() => setA(SINAVA_UYGUN)}>Yalnız sınava uygun</button>
                      <button type="button" onClick={() => setA({ kat: TUM_KAT, kaynak: TUM_KAYNAK })}>Hepsi</button>
                    </div>
                  </div>}
                  {bt.sinavKurali && <Anahtar on={a.yalnizAday} onChange={(v) => setA({ yalnizAday: v })} ad="Yalnız sınav adayları" not="Her dersin sıralı adayları (her slayttan 1, Genetik'ten 2 soru)" />}
                  <Anahtar on={a.yalnizCikmis} onChange={(v) => setA({ yalnizCikmis: v })} ad="Yalnız çıkmış sorusu olanlar" />
                </>
              )}
              <Seg<Ogr> ad="Öğrendiklerim" deger={a.ogrenilen} onChange={(v) => setA({ ogrenilen: v })}
                secenekler={[['hepsi', 'Dahil'], ['haric', `Çıkar${say.ogr ? ` (${say.ogr})` : ''}`], ['yalniz', 'Yalnız onlar']]} />
            </Bolum>

            <Bolum no={4} ad="İçerik">
              {mod !== 'soru' && mod !== 'kart' && <Anahtar on={a.ozet} onChange={(v) => setA({ ozet: v })} ad="Ders özeti ve “Neden önemli”" />}
              {mod === 'kart' && <Anahtar on={a.ozet} onChange={(v) => setA({ ozet: v })} ad="Ders özeti (kartlardan önce)" />}
              {listeli && <Anahtar on={a.adaylarKutusu} onChange={(v) => setA({ adaylarKutusu: v })} ad="“Sınavda çıkabilecek” kutusu" not="Sıralı adaylar, en olası soru vurgulu" />}
              {mod !== 'soru' && <Anahtar on={a.alt} onChange={(v) => setA({ alt: v })} ad="Alt maddeler" />}
              {listeli && (
                <>
                  <Anahtar on={a.neden} onChange={(v) => setA({ neden: v })} ad="Her maddede “Neden önemli”" />
                  <Anahtar on={a.alinti} onChange={(v) => setA({ alinti: v })} ad="PDF alıntısı (sayfa no ile)" not={mod === 'bosluk' ? 'Boşluğun cevabını ele verebilir' : undefined} />
                  <Anahtar on={a.detay} onChange={(v) => setA({ detay: v })} ad="Ayrıntılı açıklama" not={mod === 'bosluk' ? 'Boşluğun cevabını ele verebilir · dosya uzar' : 'Dosya uzar'} />
                </>
              )}
              {mod !== 'kart' && (
                <>
                  <Anahtar on={a.ornekSoru} onChange={(v) => setA({ ornekSoru: v })} ad="Örnek sorular" not={veri ? `${say.soru} soru` : undefined} />
                  <Anahtar on={a.cikmis} onChange={(v) => setA({ cikmis: v })} ad="Çıkmış sorular" not={veri ? `${say.cikmis} soru` : undefined} />
                  {mod === 'soru' && <Anahtar on={a.optik} onChange={(v) => setA({ optik: v })} ad="Optik daireler" not="Her sorunun yanında A–E daireleri" />}
                </>
              )}
              {(mod === 'bosluk' || ((a.ornekSoru || a.cikmis) && mod !== 'kart')) && (
                <Seg ad={mod === 'bosluk' ? 'Cevaplar' : 'Cevap anahtarı'} deger={a.anahtar} onChange={(v) => setA({ anahtar: v })}
                  secenekler={[['ders', 'Ders sonunda'], ['son', 'Dosya sonunda'], ['yok', 'Yok']]} />
              )}
              {mod === 'soru' && !a.ornekSoru && !a.cikmis && <p className="op-uyari">Soru kitapçığı için örnek ya da çıkmış sorulardan en az birini aç.</p>}
            </Bolum>

            <Bolum no={5} ad="Sayfa düzeni">
              <Seg ad="Sayfa" deger={a.sayfa} onChange={(v) => setA({ sayfa: v })} secenekler={[['a4', 'A4'], ['a5', 'A5'], ['tablet', 'Tablet'], ['letter', 'Letter']]} />
              <Seg ad="Yön" deger={a.yon} onChange={(v) => setA({ yon: v })} secenekler={[['dikey', 'Dikey'], ['yatay', 'Yatay']]} />
              {mod !== 'kart' && <Seg ad="Sütun" deger={a.sutun} onChange={(v) => setA({ sutun: v })} secenekler={[[1, 'Tek'], [2, 'İki']]} />}
              <Seg ad="Yazı" deger={a.yazi} onChange={(v) => setA({ yazi: v })} secenekler={[['kucuk', 'Küçük'], ['normal', 'Normal'], ['buyuk', 'Büyük']]} />
              <Seg ad="Satır aralığı" deger={a.aralik} onChange={(v) => setA({ aralik: v })} secenekler={[['sik', 'Sık'], ['normal', 'Normal'], ['rahat', 'Rahat']]} />
              <Seg ad="Kenar boşluğu" deger={a.kenar} onChange={(v) => setA({ kenar: v })} secenekler={[['dar', 'Dar'], ['normal', 'Normal'], ['genis', 'Geniş']]} />
              {mod !== 'soru' && <Seg ad="Sıralama" deger={a.siralama} onChange={(v) => setA({ siralama: v })} secenekler={[['puan', 'Puan partları'], ['slayt', 'Slayt sırası']]} />}
            </Bolum>

            <Bolum no={6} ad="Görünüm ve ekler">
              <Seg ad="Renk" deger={a.renk} onChange={(v) => setA({ renk: v })} secenekler={[['renkli', 'Renkli'], ['gri', 'Gri'], ['murekkep', 'Mürekkep tasarrufu']]} />
              <Anahtar on={a.kapak} onChange={(v) => setA({ kapak: v })} ad="Kapak sayfası" not="Düzen, sayılar, puan dağılımı, sınav kuralı" />
              <Anahtar on={a.icindekiler} onChange={(v) => setA({ icindekiler: v })} ad="İçindekiler" not="Sayfa numaralı, tıklanabilir (birden çok derste)" />
              <Anahtar on={a.yeniSayfa} onChange={(v) => setA({ yeniSayfa: v })} ad="Her ders yeni sayfada" />
              {mod !== 'soru' && mod !== 'kart' && (
                <>
                  <Anahtar on={a.isaretKutusu} onChange={(v) => setA({ isaretKutusu: v })} ad="İşaret kutuları" not="Her maddede ☐; öğrendiklerin işaretli gelir" />
                  <Anahtar on={a.numara} onChange={(v) => setA({ numara: v })} ad="Madde numaraları" />
                </>
              )}
              {mod !== 'kart' && <Anahtar on={a.notAlani} onChange={(v) => setA({ notAlani: v })} ad="Ders sonunda not alanı" not="5 satır" />}
              <button type="button" className="op-sifirla" onClick={() => { setA0(VARSAYILAN); setSablon(null); }}><RefreshCw aria-hidden />Varsayılan ayarlara dön</button>
            </Bolum>

            <Bolum no={7} ad="Dosya adı">
              <label className="op-dosya">
                <FileText aria-hidden />
                <input type="text" value={dosyaAdi} onChange={(e) => setDosyaAdi(e.target.value)} placeholder={varsayilanAd} aria-label="Dosya adı" />
                <span>.pdf</span>
              </label>
            </Bolum>
          </div>

          <aside className="op-onizleme" aria-label="Önizleme">
            <div className="op-on-bas">
              <b>Önizleme</b>
              {guncel && onizleme && <span>{onizleme.sayfa} sayfa · {Math.max(1, Math.round(onizleme.blob.size / 1024))} KB</span>}
              {!guncel && !bos && uretim === null && veri && (
                <button type="button" className="op-mini" onClick={() => void uret()}><RefreshCw aria-hidden />{onizleme ? 'Yenile' : 'Önizle'}</button>
              )}
            </div>
            {uretim !== null && (
              <div className="op-ilerleme" role="status">
                <Loader2 className="op-don" aria-hidden />
                <span>Hazırlanıyor… %{Math.round(uretim * 100)}</span>
                <div className="op-bar"><i style={{ width: `${Math.round(uretim * 100)}%` }} /></div>
                <button type="button" className="op-link" onClick={() => { iptalRef.current = true; }}>Vazgeç</button>
              </div>
            )}
            {bos && veri && <p className="op-bos">Bu seçimle PDF'e girecek {mod === 'soru' ? 'soru' : 'madde'} yok. Süzgeçleri genişlet.</p>}
            {!bos && !onizleme && uretim === null && (
              <p className="op-bos">{otomatik ? 'Önizleme birazdan hazır…' : 'Seçim büyük; önizlemek için “Önizle”ye dokun ya da doğrudan indir.'}</p>
            )}
            {onizleme && (
              <div className={`op-on-kap${guncel ? '' : ' is-eski'}`}>
                {!guncel && <span className="op-eski-not"><Layers aria-hidden />Ayarlar değişti — {otomatik ? 'yenileniyor' : '“Yenile”ye dokun'}</span>}
                <React.Suspense fallback={<p className="op-bos">Önizleme yükleniyor…</p>}>
                  <OnemPdfOnizleme blob={onizleme.blob} sayfa={onizleme.sayfa} />
                </React.Suspense>
              </div>
            )}
          </aside>
        </div>

      </div>
    </Sheet>
  );
};

function useGenis() {
  const q = '(min-width: 900px)';
  const [v, setV] = useState(() => typeof window !== 'undefined' && window.matchMedia(q).matches);
  useEffect(() => {
    const m = window.matchMedia(q);
    const f = () => setV(m.matches);
    m.addEventListener('change', f);
    return () => m.removeEventListener('change', f);
  }, []);
  return v;
}

export default OnemPdfPenceresi;
