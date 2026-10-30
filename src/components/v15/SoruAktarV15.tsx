import React, { useCallback, useDeferredValue, useEffect, useMemo, useRef, useState } from 'react';
import { useVirtualizer } from '@tanstack/react-virtual';
import {
  Check, CheckSquare, Columns2, Eye, FileDown, FileText, Filter, LayoutGrid, ListChecks, Loader2, Palette, Presentation, Printer,
  RotateCcw, Save, Search, Shuffle, SlidersHorizontal, Trash2, Type,
} from 'lucide-react';
import { useV15Baslik } from './baslik';
import { BOS_SUZGEC, KAYNAKLAR, kaynakYukle, miniDesteler, secenekler, suz, type AQ, type KaynakId, type Suzgec } from './soruAktar/kaynak';
import {
  KAGIT, PALETLER, PX_MM, TASARIMLAR, VARSAYILAN, YAZI, ayarNormal, karistir, sayfaOlcu, tasarimUygula,
  type Ayar, type Bicim, type Duzen, type TasarimId,
} from './soruAktar/ayar';
import { Olcer, belgeHtml, hazirla, kagitAdi, renkHaritasi, sayfala, type HS } from './soruAktar/belge';
import { downloadBlob, printDocument, renderPdfOnServer, safeFileName } from '../pdf/pdfDocument';
import { toast } from '../ui/Toast';
import type { DeckCatalogEntry } from '../../data/deckStore';
import '../../styles/v15/soruaktar.css';

/**
 * v15 · Soru dışa aktarıcı (/sorular/disa-aktar, iç /soru-aktar). Sitedeki her soru türünü (çıkmış, örnek, sesli çözücü,
 * hoca üslubu, hocanın sorabileceği, Öğren çalışma/mini, havuz) seçip süzer; 1-2-4-8 ızgara ya da akış düzeni, 6 tasarım
 * modu, kenar/çerçeve/başlık, metin ve satır, renk anahtarı, çözüm yerleşimiyle PDF · DOCX · PPTX üretir.
 * Önizleme indirilecek belgenin aynısıdır (aynı sayfa modeli; büyük seçimde ilk ONIZ_SORU soru). Ayarlar cihazda saklanır.
 */
const AKEY = 'medsoru_soru_aktar_v1';
const SKEY = 'medsoru_soru_aktar_suzgec_v1';
const TKEY = 'medsoru_soru_aktar_sablon_v1';
const ONIZ_SORU = 60;
const ONIZ_SAYFA = 40;
const oku = <T,>(k: string, v: T): T => { try { const r = localStorage.getItem(k); return r ? JSON.parse(r) : v; } catch { return v; } };
const yaz = (k: string, v: unknown) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* özel pencere */ } };

type Sekme = 'sorular' | 'tasarim' | 'sayfa' | 'metin' | 'renk' | 'cozum';
const SEKMELER: { id: Sekme; ad: string; Ic: React.ElementType }[] = [
  { id: 'sorular', ad: 'Sorular', Ic: ListChecks },
  { id: 'tasarim', ad: 'Tasarım', Ic: LayoutGrid },
  { id: 'sayfa', ad: 'Sayfa', Ic: FileText },
  { id: 'metin', ad: 'Metin', Ic: Type },
  { id: 'renk', ad: 'Renk', Ic: Palette },
  { id: 'cozum', ad: 'Çözüm', Ic: CheckSquare },
];
const BICIMLER: { id: Bicim; ad: string; uz: string; Ic: React.ElementType }[] = [
  { id: 'pdf', ad: 'PDF', uz: 'pdf', Ic: FileDown },
  { id: 'docx', ad: 'Word', uz: 'docx', Ic: FileText },
  { id: 'pptx', ad: 'PowerPoint', uz: 'pptx', Ic: Presentation },
];

/* ---------------------------------------------------------------------------
 * Küçük denetimler
 * ------------------------------------------------------------------------- */
function Bolum({ baslik, alt, sag, children }: { baslik: string; alt?: string; sag?: React.ReactNode; children: React.ReactNode }) {
  return (
    <section className="sx15-b">
      <header><h3>{baslik}</h3>{sag}</header>
      {alt && <p className="v15-cap">{alt}</p>}
      {children}
    </section>
  );
}
function Seg<T extends string | number>({ ad, deger, ogeler, degis, kucuk }: { ad: string; deger: T; ogeler: { v: T; ad: React.ReactNode; title?: string }[]; degis: (v: T) => void; kucuk?: boolean }) {
  return (
    <div className={`sx15-seg${kucuk ? ' is-k' : ''}`} role="radiogroup" aria-label={ad}>
      {ogeler.map((o) => (
        <button key={String(o.v)} type="button" role="radio" aria-checked={deger === o.v} title={o.title} className={deger === o.v ? 'is-on' : ''} onClick={() => degis(o.v)}>{o.ad}</button>
      ))}
    </div>
  );
}
function Anahtar({ ad, alt, acik, degis, kapali }: { ad: string; alt?: string; acik: boolean; degis: (v: boolean) => void; kapali?: boolean }) {
  return (
    <button type="button" role="switch" aria-checked={acik} disabled={kapali} className="sx15-sw" onClick={() => degis(!acik)}>
      <span><b>{ad}</b>{alt && <small>{alt}</small>}</span><i aria-hidden />
    </button>
  );
}
function Kaydir({ ad, deger, min, max, adim = 1, birim, degis }: { ad: string; deger: number; min: number; max: number; adim?: number; birim?: string; degis: (v: number) => void }) {
  const id = `sx15-${ad.replace(/\W+/g, '')}`;
  return (
    <div className="sx15-kay">
      <label htmlFor={id}>{ad}</label>
      <input id={id} type="range" min={min} max={max} step={adim} value={deger} onChange={(e) => degis(Number(e.target.value))} />
      <input type="number" aria-label={`${ad} değeri`} min={min} max={max} step={adim} value={Number(deger.toFixed(2))} onChange={(e) => { const v = Number(e.target.value); if (Number.isFinite(v)) degis(Math.min(max, Math.max(min, v))); }} />
      {birim && <span>{birim}</span>}
    </div>
  );
}
function Renk({ ad, deger, degis }: { ad: string; deger: string; degis: (v: string) => void }) {
  return <label className="sx15-renk"><input type="color" value={deger} onChange={(e) => degis(e.target.value)} /><span>{ad}</span></label>;
}
function Metin({ ad, deger, degis, yer }: { ad: string; deger: string; degis: (v: string) => void; yer?: string }) {
  return <label className="sx15-in"><span>{ad}</span><input type="text" value={deger} placeholder={yer} maxLength={140} onChange={(e) => degis(e.target.value)} /></label>;
}
function CokSecim({ ad, liste, secili, degis, ad2 }: { ad: string; liste: { v: string; n: number }[]; secili: string[]; degis: (v: string[]) => void; ad2?: (v: string) => string }) {
  const [ara, setAra] = useState('');
  const [hepsi, setHepsi] = useState(false);
  if (!liste.length && !secili.length) return null;
  const goster = ad2 || ((v: string) => v);
  const tum = [...liste, ...secili.filter((v) => !liste.some((x) => x.v === v)).map((v) => ({ v, n: 0 }))];
  const sk = ara.trim().toLocaleLowerCase('tr');
  const suz2 = sk ? tum.filter((x) => goster(x.v).toLocaleLowerCase('tr').includes(sk)) : tum;
  const MAX = 16;
  const gorunen = hepsi || sk ? suz2 : suz2.slice(0, MAX);
  const ac = (v: string) => degis(secili.includes(v) ? secili.filter((x) => x !== v) : [...secili, v]);
  return (
    <div className="sx15-coklu">
      <div className="sx15-coklu-b">
        <b>{ad}</b>
        {secili.length > 0 && <button type="button" className="sx15-lnk" onClick={() => degis([])}>Temizle ({secili.length})</button>}
      </div>
      {tum.length > MAX && (
        <label className="sx15-ara"><Search aria-hidden /><input type="search" value={ara} placeholder={`${ad} ara`} onChange={(e) => setAra(e.target.value)} /></label>
      )}
      <div className="sx15-cipler">
        {gorunen.map((x) => (
          <button key={x.v} type="button" aria-pressed={secili.includes(x.v)} className={`sx15-cip${secili.includes(x.v) ? ' is-on' : ''}${x.n === 0 ? ' is-0' : ''}`} onClick={() => ac(x.v)}>
            {secili.includes(x.v) && <Check aria-hidden />}<span>{goster(x.v)}</span><em>{x.n}</em>
          </button>
        ))}
        {!hepsi && !sk && suz2.length > MAX && <button type="button" className="sx15-cip is-dev" onClick={() => setHepsi(true)}>+{suz2.length - MAX} daha</button>}
      </div>
    </div>
  );
}

/** Tasarım kartı küçük resmi: düzenin kaba taslağı */
function TasarimResim({ id }: { id: TasarimId }) {
  return <span className={`sx15-tr sx15-tr-${id}`} aria-hidden><i /><i /><i /><i /></span>;
}
function DuzenResim({ d }: { d: Duzen }) {
  const n = d === 'akis' ? 0 : d;
  return <span className={`sx15-dr sx15-dr-${d}`} aria-hidden>{n ? Array.from({ length: n }, (_, i) => <i key={i} />) : <><b /><b /></>}</span>;
}

/* ---------------------------------------------------------------------------
 * Soru listesi (sanal kaydırma)
 * ------------------------------------------------------------------------- */
function SoruListesi({ liste, cikarilan, ac }: { liste: AQ[]; cikarilan: Set<string>; ac: (k: string) => void }) {
  const kap = useRef<HTMLDivElement>(null);
  const v = useVirtualizer({ count: liste.length, getScrollElement: () => kap.current, estimateSize: () => 74, overscan: 8 });
  if (!liste.length) return <p className="sx15-bos">Süzgeçlere uyan soru yok. Kaynak ekle ya da süzgeçleri gevşet.</p>;
  return (
    <div ref={kap} className="sx15-liste" role="list" aria-label="Sorular">
      <div style={{ height: v.getTotalSize(), position: 'relative' }}>
        {v.getVirtualItems().map((r) => {
          const q = liste[r.index];
          const on = !cikarilan.has(q.key);
          return (
            <div key={q.key} role="listitem" className="sx15-sat" style={{ position: 'absolute', top: 0, left: 0, right: 0, transform: `translateY(${r.start}px)` }} ref={v.measureElement} data-index={r.index}>
              <button type="button" aria-pressed={on} className={`sx15-sat-b${on ? ' is-on' : ''}`} onClick={() => ac(q.key)}>
                <span className="sx15-kutu" aria-hidden>{on && <Check />}</span>
                <span className="sx15-sat-t">
                  <span className="sx15-sat-k">{q.stem}</span>
                  <span className="sx15-sat-m">{[q.tur, q.ders, q.konu, q.year, q.kurul ? `K${q.kurul}` : ''].filter(Boolean).join(' · ')}</span>
                </span>
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
}

/* ---------------------------------------------------------------------------
 * Önizleme
 * ------------------------------------------------------------------------- */
interface Oniz { html: string; sayfa: number; tahmini: boolean; tasan: number; gosterilen: number }

function Onizleme({ oniz, ayar, yukleniyor, zum }: { oniz: Oniz | null; ayar: Ayar; yukleniyor: boolean; zum: 'sigdir' | number }) {
  const dis = useRef<HTMLDivElement>(null);
  const fr = useRef<HTMLIFrameElement>(null);
  const [gen, setGen] = useState(600);
  const [aktif, setAktif] = useState(1);
  const { w, h } = sayfaOlcu(ayar);
  const pw = w * PX_MM + 28;
  useEffect(() => {
    const el = dis.current;
    if (!el) return;
    const ro = new ResizeObserver(() => setGen(el.clientWidth));
    ro.observe(el);
    setGen(el.clientWidth);
    return () => ro.disconnect();
  }, []);
  const olcek = zum === 'sigdir' ? Math.min(1.25, Math.max(0.2, (gen - 8) / pw)) : zum;
  // Belge yüksekliği sayfa sayısından (gövde 14 px üst boşluk + sayfa başına yükseklik + 14 px ara); çerçeve gizliyken
  // yüklenirse DOM ölçüsü 0 döner (telefonda Ayarlar sekmesi açıkken), bu yüzden okunmaz.
  const yuk = 14 + (oniz?.gosterilen || 1) * (h * PX_MM + 14);
  const kaydir = () => {
    const el = dis.current;
    if (!el) return;
    const adim = (h * PX_MM + 14) * olcek;
    setAktif(Math.min(oniz?.gosterilen || 1, Math.max(1, Math.floor((el.scrollTop + adim * 0.4) / adim) + 1)));
  };
  return (
    <div className="sx15-oz">
      <div ref={dis} className="sx15-oz-k" onScroll={kaydir} tabIndex={0} aria-label="Belge önizlemesi">
        {oniz ? (
          <div style={{ width: pw * olcek, height: yuk * olcek, margin: '0 auto', position: 'relative' }}>
            <iframe
              ref={fr}
              title="Belge önizlemesi"
              srcDoc={oniz.html}
              style={{ width: pw, maxWidth: 'none', height: yuk, border: 0, transform: `scale(${olcek})`, transformOrigin: '0 0', position: 'absolute', left: 0, top: 0, background: 'transparent' }}
            />
          </div>
        ) : (
          <div className="sx15-oz-bos">{yukleniyor ? <><Loader2 className="sx15-don" aria-hidden />Önizleme hazırlanıyor…</> : 'Önizleme için soru seç.'}</div>
        )}
        {yukleniyor && oniz && <div className="sx15-oz-yuk"><Loader2 className="sx15-don" aria-hidden /></div>}
      </div>
      {oniz && (
        <div className="sx15-oz-alt" aria-live="polite">
          Sayfa {aktif} / {oniz.tahmini ? '≈' : ''}{oniz.sayfa}
          {oniz.gosterilen < oniz.sayfa && <span> · önizlemede ilk {oniz.gosterilen} sayfa</span>}
        </div>
      )}
    </div>
  );
}

/* ---------------------------------------------------------------------------
 * Sayfa
 * ------------------------------------------------------------------------- */
export default function SoruAktarV15() {
  useV15Baslik({ baslik: 'Soru dışa aktarıcı', alt: 'PDF · Word · PowerPoint' });
  const [ayar, setAyar] = useState<Ayar>(() => ayarNormal(oku(AKEY, null)));
  const [suzgec, setSuzgec] = useState<Suzgec>(() => ({ ...BOS_SUZGEC, ...oku<Partial<Suzgec>>(SKEY, {}), arama: '' }));
  const [sablon, setSablon] = useState<{ ad: string; ayar: Ayar }[]>(() => oku(TKEY, []));
  const [sekme, setSekme] = useState<Sekme>('sorular');
  const [mobil, setMobil] = useState<'ayar' | 'oniz'>('ayar');
  const [veri, setVeri] = useState<Partial<Record<KaynakId, AQ[]>>>({});
  const [durum, setDurum] = useState<Partial<Record<KaynakId, 'y' | 'h'>>>({});
  const [desteler, setDesteler] = useState<DeckCatalogEntry[] | null>(null);
  const [cikarilan, setCikarilan] = useState<Set<string>>(() => new Set());
  const [sinir, setSinir] = useState<{ mod: 'hepsi' | 'ilk' | 'rastgele'; n: number }>({ mod: 'hepsi', n: 40 });
  const [oniz, setOniz] = useState<Oniz | null>(null);
  const [onizYuk, setOnizYuk] = useState(false);
  const [zum, setZum] = useState<'sigdir' | number>('sigdir');
  const [uretim, setUretim] = useState<string | null>(null);
  const [sablonAd, setSablonAd] = useState('');
  const set = useCallback((p: Partial<Ayar>) => setAyar((a) => ({ ...a, ...p })), []);
  const setS = useCallback((p: Partial<Suzgec>) => setSuzgec((s) => ({ ...s, ...p })), []);

  useEffect(() => yaz(AKEY, ayar), [ayar]);
  useEffect(() => yaz(SKEY, { ...suzgec, arama: '' }), [suzgec]);
  useEffect(() => yaz(TKEY, sablon), [sablon]);

  /* ---- veri ---- */
  const miniAnahtar = suzgec.desteler.slice().sort().join(',');
  useEffect(() => {
    for (const k of suzgec.kaynaklar) {
      if (k === 'mini') continue;
      if (veri[k] || durum[k] === 'y') continue;
      setDurum((d) => ({ ...d, [k]: 'y' }));
      kaynakYukle(k).then(
        (l) => { setVeri((v) => ({ ...v, [k]: l })); setDurum((d) => ({ ...d, [k]: undefined })); },
        () => setDurum((d) => ({ ...d, [k]: 'h' })),
      );
    }
  }, [suzgec.kaynaklar, veri, durum]);
  useEffect(() => {
    if (!suzgec.kaynaklar.includes('mini')) return;
    if (!desteler) miniDesteler().then(setDesteler, () => setDesteler([]));
    let canli = true;
    setDurum((d) => ({ ...d, mini: 'y' }));
    kaynakYukle('mini', { desteler: suzgec.desteler }).then(
      (l) => { if (canli) { setVeri((v) => ({ ...v, mini: l })); setDurum((d) => ({ ...d, mini: undefined })); } },
      () => canli && setDurum((d) => ({ ...d, mini: 'h' })),
    );
    return () => { canli = false; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [suzgec.kaynaklar.includes('mini'), miniAnahtar]);

  const tum = useMemo(() => suzgec.kaynaklar.flatMap((k) => veri[k] || []), [suzgec.kaynaklar, veri]);
  const aramaG = useDeferredValue(suzgec.arama);
  const suzA = useMemo(() => ({ ...suzgec, arama: aramaG }), [suzgec, aramaG]);
  const suzulmus = useMemo(() => suz(tum, suzA), [tum, suzA]);
  const sec = useMemo(() => ({
    kurullar: secenekler(tum, suzA, 'kurullar'),
    dersler: secenekler(tum, suzA, 'dersler'),
    konular: secenekler(tum, suzA, 'konular'),
    yillar: secenekler(tum, suzA, 'yillar'),
    turler: secenekler(tum, suzA, 'turler'),
    zorluk: secenekler(tum, suzA, 'zorluk'),
  }), [tum, suzA]);
  const secili = useMemo(() => {
    const l = suzulmus.filter((q) => !cikarilan.has(q.key));
    if (sinir.mod === 'ilk') return l.slice(0, sinir.n);
    if (sinir.mod === 'rastgele') return karistir(l, ayar.tohum + 7).slice(0, sinir.n);
    return l;
  }, [suzulmus, cikarilan, sinir, ayar.tohum]);
  const hs = useMemo<HS[]>(() => hazirla(secili, ayar), [secili, ayar]);
  const lejant = useMemo(() => renkHaritasi(secili, ayar), [secili, ayar]);
  const yukleniyor = suzgec.kaynaklar.some((k) => durum[k] === 'y');

  /* ---- önizleme ---- */
  const sira = useRef(0);
  useEffect(() => {
    const no = ++sira.current;
    setOnizYuk(true);
    const t = setTimeout(async () => {
      if (!hs.length) { if (no === sira.current) { setOniz(null); setOnizYuk(false); } return; }
      const olcer = await new Olcer(ayar).hazir();
      try {
        const parca = hs.slice(0, ONIZ_SORU);
        const b = await sayfala(parca, ayar, { olcer });
        if (no !== sira.current) return;
        const tahmini = hs.length > parca.length;
        const toplam = tahmini ? Math.max(b.sayfalar.length, Math.round((b.sayfalar.length * hs.length) / parca.length)) : b.sayfalar.length;
        setOniz({ html: belgeHtml(b, ayar, { onizleme: true, ilk: ONIZ_SAYFA, tum: hs, toplamSayfa: tahmini ? toplam : undefined }), sayfa: toplam, tahmini, tasan: b.tasan, gosterilen: Math.min(ONIZ_SAYFA, b.sayfalar.length) });
      } catch (e) {
        console.warn('[soru-aktar] önizleme', e);
      } finally {
        olcer.kapat();
        if (no === sira.current) setOnizYuk(false);
      }
    }, 280);
    return () => clearTimeout(t);
  }, [hs, ayar]);

  /* ---- üretim ---- */
  const indir = async (yazdir = false) => {
    if (!hs.length || uretim) return;
    const a = ayar;
    const bicim = BICIMLER.find((b) => b.id === a.bicim)!;
    const ad = `${safeFileName(a.baslik || 'Sorular')}_${hs.length}_soru.${bicim.uz}`;
    try {
      setUretim(`${hs.length} soru sayfalanıyor…`);
      const b = await sayfala(hs, yazdir ? { ...a, bicim: 'pdf' } : a);
      if (yazdir || a.bicim === 'pdf') {
        const html = belgeHtml(b, a, { baslik: a.baslik });
        if (yazdir) { setUretim('Yazdırma penceresi açılıyor…'); await printDocument(html); return; }
        setUretim(`PDF oluşturuluyor (${b.sayfalar.length} sayfa)…`);
        try {
          downloadBlob(await renderPdfOnServer(html, a.baslik || 'Sorular', ad), ad);
        } catch (e: any) {
          toast.info('PDF sunucuda oluşturulamadı', `${e?.message || ''} Yazdırma penceresinde "PDF olarak kaydet"i seç.`.trim());
          await printDocument(html);
          return;
        }
      } else if (a.bicim === 'docx') {
        setUretim('Word belgesi yazılıyor…');
        const { docxUret } = await import('./soruAktar/docx');
        downloadBlob(await docxUret(b, a), ad);
      } else {
        setUretim(`PowerPoint sunusu yazılıyor (${b.sayfalar.length} slayt)…`);
        const { pptxUret } = await import('./soruAktar/pptx');
        downloadBlob(await pptxUret(b, a), ad);
      }
      toast.success('İndirildi', `${ad} · ${hs.length} soru, ${b.sayfalar.length} ${a.bicim === 'pptx' ? 'slayt' : 'sayfa'}`);
    } catch (e: any) {
      console.warn('[soru-aktar] üretim', e);
      toast.error('Belge oluşturulamadı', e?.message || 'Beklenmeyen hata');
    } finally {
      setUretim(null);
    }
  };

  const ac = useCallback((k: string) => setCikarilan((s) => { const n = new Set(s); if (n.has(k)) n.delete(k); else n.add(k); return n; }), []);
  const kaynakAc = (k: KaynakId) => setS({ kaynaklar: suzgec.kaynaklar.includes(k) ? suzgec.kaynaklar.filter((x) => x !== k) : [...suzgec.kaynaklar, k] });
  const suzgecSay = suzgec.kurullar.length + suzgec.dersler.length + suzgec.konular.length + suzgec.yillar.length + suzgec.turler.length + suzgec.zorluk.length + (suzgec.cevapli ? 1 : 0) + (suzgec.aciklamali ? 1 : 0) + (suzgec.arama ? 1 : 0);
  const bicim = BICIMLER.find((b) => b.id === ayar.bicim)!;
  const ozet = `${hs.length} soru · ${oniz ? `${oniz.tahmini ? '≈' : ''}${oniz.sayfa} ${ayar.bicim === 'pptx' ? 'slayt' : 'sayfa'}` : '—'} · ${kagitAdi(ayar)}`;

  /* ---- paneller ---- */
  const panelSorular = (
    <>
      <Bolum baslik="Kaynaklar" alt="Birden çok kaynak seçebilirsin; sorular tek belgede birleşir.">
        <div className="sx15-kaynak">
          {KAYNAKLAR.map((k) => {
            const on = suzgec.kaynaklar.includes(k.id);
            const n = veri[k.id]?.length;
            return (
              <button key={k.id} type="button" aria-pressed={on} className={`sx15-ky${on ? ' is-on' : ''}`} onClick={() => kaynakAc(k.id)}>
                <span className="sx15-kutu" aria-hidden>{on && <Check />}</span>
                <span><b>{k.ad}</b><small>{k.alt}</small></span>
                <em>{durum[k.id] === 'y' ? <Loader2 className="sx15-don" aria-label="yükleniyor" /> : durum[k.id] === 'h' ? 'hata' : n != null ? n : ''}</em>
              </button>
            );
          })}
        </div>
        {suzgec.kaynaklar.includes('mini') && (
          <div className="sx15-deste">
            <b>Mini soru desteleri</b>
            {!desteler ? <p className="v15-cap">Desteler yükleniyor…</p> : (
              <CokSecim ad="Deste" liste={desteler.map((d) => ({ v: d.id, n: d.questionCount || 0 }))} secili={suzgec.desteler} degis={(v) => setS({ desteler: v })} ad2={(id) => { const d = desteler.find((x) => x.id === id); return d ? d.shortTitle || d.title : id; }} />
            )}
          </div>
        )}
      </Bolum>
      <Bolum baslik="Süzgeçler" sag={suzgecSay > 0 ? <button type="button" className="sx15-lnk" onClick={() => setS({ kurullar: [], dersler: [], konular: [], yillar: [], turler: [], zorluk: [], cevapli: false, aciklamali: false, arama: '' })}><RotateCcw aria-hidden />Temizle</button> : undefined}>
        <label className="sx15-ara is-b"><Search aria-hidden /><input type="search" value={suzgec.arama} placeholder="Soru metninde ara (ör. nefrotik, akut başlangıç)" onChange={(e) => setS({ arama: e.target.value })} /></label>
        <CokSecim ad="Kurul" liste={sec.kurullar} secili={suzgec.kurullar.map(String)} degis={(v) => setS({ kurullar: v.map(Number) })} ad2={(v) => `Kurul ${v}`} />
        <CokSecim ad="Ders" liste={sec.dersler} secili={suzgec.dersler} degis={(v) => setS({ dersler: v })} />
        <CokSecim ad="Konu" liste={sec.konular} secili={suzgec.konular} degis={(v) => setS({ konular: v })} />
        <CokSecim ad="Yıl" liste={sec.yillar} secili={suzgec.yillar} degis={(v) => setS({ yillar: v })} ad2={(v) => (v === '—' ? 'Yılsız' : v)} />
        <CokSecim ad="Soru türü" liste={sec.turler} secili={suzgec.turler} degis={(v) => setS({ turler: v })} />
        <CokSecim ad="Zorluk" liste={sec.zorluk} secili={suzgec.zorluk} degis={(v) => setS({ zorluk: v })} ad2={(v) => (v === '—' ? 'Belirtilmemiş' : v[0].toLocaleUpperCase('tr') + v.slice(1))} />
        <div className="sx15-iki">
          <Anahtar ad="Yalnız cevaplı" acik={suzgec.cevapli} degis={(v) => setS({ cevapli: v })} />
          <Anahtar ad="Yalnız açıklamalı" acik={suzgec.aciklamali} degis={(v) => setS({ aciklamali: v })} />
        </div>
      </Bolum>
      <Bolum baslik="Soru sayısı">
        <Seg ad="Soru sayısı" deger={sinir.mod} degis={(mod) => setSinir((s) => ({ ...s, mod }))} ogeler={[{ v: 'hepsi', ad: 'Tümü' }, { v: 'ilk', ad: 'İlk N' }, { v: 'rastgele', ad: 'Rastgele N' }]} />
        {sinir.mod !== 'hepsi' && (
          <div className="sx15-sat2">
            <Kaydir ad="N" deger={sinir.n} min={1} max={Math.max(10, Math.min(500, suzulmus.length))} degis={(n) => setSinir((s) => ({ ...s, n }))} birim="soru" />
            {sinir.mod === 'rastgele' && <button type="button" className="v15-btn is-ghost sx15-kb" onClick={() => set({ tohum: ayar.tohum + 1 })}><Shuffle aria-hidden />Yeniden çek</button>}
          </div>
        )}
      </Bolum>
      <Bolum
        baslik={`Seçim · ${secili.length} / ${suzulmus.length}`}
        alt="Listeden dokunarak tek tek çıkar ya da geri ekle."
        sag={
          <span className="sx15-sag">
            <button type="button" className="sx15-lnk" onClick={() => setCikarilan(new Set())}>Tümü</button>
            <button type="button" className="sx15-lnk" onClick={() => setCikarilan(new Set(suzulmus.map((q) => q.key)))}>Hiçbiri</button>
            <button type="button" className="sx15-lnk" onClick={() => setCikarilan((s) => new Set(suzulmus.filter((q) => !s.has(q.key)).map((q) => q.key)))}>Ters çevir</button>
          </span>
        }
      >
        {yukleniyor && !tum.length ? <p className="sx15-bos"><Loader2 className="sx15-don" aria-hidden /> Sorular yükleniyor…</p> : <SoruListesi liste={suzulmus} cikarilan={cikarilan} ac={ac} />}
      </Bolum>
    </>
  );

  const panelTasarim = (
    <>
      <Bolum baslik="Tasarım modu" alt="Bir mod seçince tüm ayarlar ona göre dolar; sonra her şeyi elle değiştirebilirsin.">
        <div className="sx15-tasarim">
          {TASARIMLAR.map((t) => (
            <button key={t.id} type="button" aria-pressed={ayar.tasarim === t.id} className={`sx15-ts${ayar.tasarim === t.id ? ' is-on' : ''}`} onClick={() => setAyar((a) => tasarimUygula(a, t.id))}>
              <TasarimResim id={t.id} />
              <span><b>{t.ad}</b><small>{t.alt}</small></span>
            </button>
          ))}
        </div>
      </Bolum>
      <Bolum baslik="Sayfa düzeni" alt="Sayfa başına soru sayısı. Izgarada sığmayan soru otomatik küçültülür.">
        <Seg ad="Sayfa düzeni" deger={ayar.duzen} degis={(duzen) => set({ duzen })} ogeler={(['akis', 1, 2, 4, 8] as Duzen[]).map((d) => ({ v: d, ad: <span className="sx15-dz"><DuzenResim d={d} />{d === 'akis' ? 'Akış' : d}</span>, title: d === 'akis' ? 'Sorular sığdığı kadar akar' : `Sayfa başına ${d} soru` }))} />
        {ayar.duzen === 'akis' ? (
          <>
            <Seg ad="Sütun" deger={ayar.sutun} degis={(sutun) => set({ sutun })} ogeler={[{ v: 1, ad: 'Tek sütun' }, { v: 2, ad: <><Columns2 aria-hidden />İki sütun</> }]} />
            {ayar.sutun === 2 && <Anahtar ad="Sütun ayırıcı çizgi" acik={ayar.sutunCizgi} degis={(v) => set({ sutunCizgi: v })} />}
          </>
        ) : (
          <>
            <Anahtar ad="Hücre çerçevesi" alt="Her soru yuvarlak köşeli kutuda" acik={ayar.hucreCerceve} degis={(v) => set({ hucreCerceve: v })} />
            <Kaydir ad="Hücre aralığı" deger={ayar.hucreAralik} min={0} max={20} adim={0.5} birim="mm" degis={(v) => set({ hucreAralik: v })} />
          </>
        )}
      </Bolum>
      <Bolum baslik="Sıralama ve gruplama">
        <label className="sx15-sel"><span>Sırala</span>
          <select value={ayar.sirala} onChange={(e) => set({ sirala: e.target.value as Ayar['sirala'] })}>
            <option value="kaynak">Kaynak sırası</option><option value="ders">Derse göre</option><option value="konu">Konuya göre</option>
            <option value="yil">Yıla göre (yeni önce)</option><option value="zorluk">Zorluğa göre (kolaydan)</option><option value="rastgele">Rastgele</option>
          </select>
        </label>
        {ayar.sirala === 'rastgele' && <button type="button" className="v15-btn is-ghost sx15-kb" onClick={() => set({ tohum: ayar.tohum + 1 })}><Shuffle aria-hidden />Yeniden karıştır</button>}
        <label className="sx15-sel"><span>Grupla</span>
          <select value={ayar.grupla} onChange={(e) => set({ grupla: e.target.value as Ayar['grupla'] })}>
            <option value="yok">Gruplama yok</option><option value="ders">Derse göre</option><option value="konu">Konuya göre</option>
            <option value="yil">Yıla göre</option><option value="kaynak">Kaynağa göre</option><option value="kurul">Kurula göre</option>
          </select>
        </label>
        {ayar.grupla !== 'yok' && (
          <div className="sx15-iki">
            <Anahtar ad="Her grup yeni sayfada" acik={ayar.grupYeniSayfa || ayar.duzen !== 'akis'} kapali={ayar.duzen !== 'akis'} degis={(v) => set({ grupYeniSayfa: v })} />
            <Anahtar ad="Numara grupta yeniden" acik={ayar.grupNumara} degis={(v) => set({ grupNumara: v })} />
          </div>
        )}
        <Anahtar ad="Şıkları karıştır" alt="Cevap anahtarı yeni sıraya göre yazılır" acik={ayar.sikKaristir} degis={(v) => set({ sikKaristir: v })} />
        <Kaydir ad="İlk soru numarası" deger={ayar.numaraBas} min={1} max={500} degis={(v) => set({ numaraBas: Math.round(v) })} />
      </Bolum>
      <Bolum baslik="Şablonlarım" alt="Ayarları adıyla kaydet, sonra tek dokunuşla geri yükle (bu cihazda).">
        <form className="sx15-sablon" onSubmit={(e) => { e.preventDefault(); const ad = sablonAd.trim(); if (!ad) return; setSablon((l) => [{ ad, ayar }, ...l.filter((x) => x.ad !== ad)].slice(0, 20)); setSablonAd(''); toast.success('Şablon kaydedildi', ad); }}>
          <input type="text" value={sablonAd} maxLength={40} placeholder="Şablon adı (ör. Patoloji deneme)" onChange={(e) => setSablonAd(e.target.value)} aria-label="Şablon adı" />
          <button type="submit" className="v15-btn is-soft" disabled={!sablonAd.trim()}><Save aria-hidden />Kaydet</button>
        </form>
        {sablon.length > 0 && (
          <ul className="sx15-sl">
            {sablon.map((x) => (
              <li key={x.ad}>
                <button type="button" className="sx15-sl-a" onClick={() => { setAyar(ayarNormal(x.ayar)); toast.info('Şablon yüklendi', x.ad); }}><b>{x.ad}</b><small>{TASARIMLAR.find((t) => t.id === x.ayar.tasarim)?.ad} · {x.ayar.duzen === 'akis' ? 'akış' : `${x.ayar.duzen}/sayfa`}</small></button>
                <button type="button" className="v15-ib" aria-label={`${x.ad} şablonunu sil`} onClick={() => setSablon((l) => l.filter((y) => y.ad !== x.ad))}><Trash2 aria-hidden /></button>
              </li>
            ))}
          </ul>
        )}
        <button type="button" className="sx15-lnk" onClick={() => setAyar({ ...VARSAYILAN, bicim: ayar.bicim })}><RotateCcw aria-hidden />Tüm ayarları varsayılana döndür</button>
      </Bolum>
    </>
  );

  const kenarSet = (i: number, v: number) => set({ kenar: ayar.kenarKilit ? [v, v, v, v] : (ayar.kenar.map((x, j) => (j === i ? v : x)) as Ayar['kenar']) });
  const panelSayfa = (
    <>
      <Bolum baslik="Kâğıt">
        {ayar.bicim === 'pptx' && <Seg ad="Slayt boyutu" deger={ayar.slayt} degis={(slayt) => set({ slayt })} ogeler={[{ v: 'genis', ad: '16:9' }, { v: 'standart', ad: '4:3' }, { v: 'kagit', ad: 'Kâğıt ölçüsü' }]} />}
        {(ayar.bicim !== 'pptx' || ayar.slayt === 'kagit') && (
          <>
            <Seg ad="Kâğıt boyutu" deger={ayar.kagit} degis={(kagit) => set({ kagit })} ogeler={(Object.keys(KAGIT) as Ayar['kagit'][]).map((k) => ({ v: k, ad: KAGIT[k].ad, title: `${KAGIT[k].w} × ${KAGIT[k].h} mm` }))} />
            <Seg ad="Yön" deger={ayar.yatay ? 'y' : 'd'} degis={(v) => set({ yatay: v === 'y' })} ogeler={[{ v: 'd', ad: 'Dikey' }, { v: 'y', ad: 'Yatay' }]} />
          </>
        )}
      </Bolum>
      <Bolum baslik="Kenar boşlukları" sag={<span className="sx15-sag">{[0, 8, 15, 25].map((v) => <button key={v} type="button" className="sx15-lnk" onClick={() => set({ kenar: [v, v, v, v] })}>{v === 0 ? 'Yok' : v === 8 ? 'Dar' : v === 15 ? 'Normal' : 'Geniş'}</button>)}</span>}>
        <Anahtar ad="Dört kenar eşit" acik={ayar.kenarKilit} degis={(v) => set({ kenarKilit: v, kenar: v ? [ayar.kenar[0], ayar.kenar[0], ayar.kenar[0], ayar.kenar[0]] : ayar.kenar })} />
        {(ayar.kenarKilit ? ['Tüm kenarlar'] : ['Üst', 'Sağ', 'Alt', 'Sol']).map((ad, i) => <Kaydir key={ad} ad={ad} deger={ayar.kenar[i]} min={0} max={40} adim={0.5} birim="mm" degis={(v) => kenarSet(i, v)} />)}
      </Bolum>
      <Bolum baslik="Sayfa kenarlığı">
        <Anahtar ad="Kenarlık çiz" acik={ayar.cerceve} degis={(v) => set({ cerceve: v })} />
        {ayar.cerceve && (
          <>
            <Seg ad="Çizgi" kucuk deger={ayar.cerceveStil} degis={(cerceveStil) => set({ cerceveStil })} ogeler={[{ v: 'solid', ad: 'Düz' }, { v: 'dashed', ad: 'Kesik' }, { v: 'dotted', ad: 'Nokta' }, { v: 'double', ad: 'Çift' }]} />
            <Kaydir ad="Kalınlık" deger={ayar.cerceveKalin} min={0.25} max={4} adim={0.25} birim="pt" degis={(v) => set({ cerceveKalin: v })} />
            <Kaydir ad="Köşe" deger={ayar.cerceveYaricap} min={0} max={10} adim={0.5} birim="mm" degis={(v) => set({ cerceveYaricap: v })} />
            <Kaydir ad="İç boşluk" deger={ayar.cerceveIc} min={0} max={12} adim={0.5} birim="mm" degis={(v) => set({ cerceveIc: v })} />
            <Renk ad="Kenarlık rengi" deger={ayar.cerceveRenk} degis={(v) => set({ cerceveRenk: v })} />
          </>
        )}
      </Bolum>
      <Bolum baslik="Başlık ve alt bilgi">
        <Anahtar ad="Sayfa başlığı" acik={ayar.baslikAcik} degis={(v) => set({ baslikAcik: v })} />
        <Metin ad="Başlık" deger={ayar.baslik} degis={(v) => set({ baslik: v })} yer="Soru kitapçığı" />
        <Metin ad="Alt başlık" deger={ayar.altBaslik} degis={(v) => set({ altBaslik: v })} yer="ör. Kurul 2 · Patoloji tekrar" />
        {ayar.baslikAcik && (
          <div className="sx15-iki">
            <Anahtar ad="Ad Soyad alanı" acik={ayar.adSoyad} degis={(v) => set({ adSoyad: v })} />
            <Anahtar ad="Tarih alanı" acik={ayar.tarih} degis={(v) => set({ tarih: v })} />
            <Anahtar ad="Her sayfada" alt="Kapalıysa yalnız ilk sayfada" acik={ayar.baslikHerSayfa} degis={(v) => set({ baslikHerSayfa: v })} />
          </div>
        )}
        <Anahtar ad="Sayfa numarası" acik={ayar.sayfaNo} degis={(v) => set({ sayfaNo: v })} />
        <Metin ad="Alt bilgi metni" deger={ayar.altMetin} degis={(v) => set({ altMetin: v })} yer="ör. MeDSor · 2026" />
        <Anahtar ad="Kapak sayfası" alt="Başlık, soru/ders sayısı, renk anahtarı, ad alanı" acik={ayar.kapak} degis={(v) => set({ kapak: v })} />
        <Metin ad="Filigran" deger={ayar.filigran} degis={(v) => set({ filigran: v })} yer="ör. TASLAK" />
      </Bolum>
    </>
  );

  const panelMetin = (
    <>
      <Bolum baslik="Yazı">
        <label className="sx15-sel"><span>Yazı tipi</span>
          <select value={ayar.yazi} onChange={(e) => set({ yazi: e.target.value as Ayar['yazi'] })}>
            {(Object.keys(YAZI) as Ayar['yazi'][]).map((k) => <option key={k} value={k}>{YAZI[k].ad}</option>)}
          </select>
        </label>
        <Kaydir ad="Punto" deger={ayar.punto} min={7} max={16} adim={0.5} birim="pt" degis={(v) => set({ punto: v })} />
        <div className="sx15-iki">
          <Anahtar ad="Soru kökü kalın" acik={ayar.kokKalin} degis={(v) => set({ kokKalin: v })} />
          <Anahtar ad="İki yana yasla" acik={ayar.iki} degis={(v) => set({ iki: v })} />
        </div>
        <div className="sx15-iki">
          <Renk ad="Metin rengi" deger={ayar.metinRenk} degis={(v) => set({ metinRenk: v })} />
          <Renk ad="Vurgu rengi" deger={ayar.vurgu} degis={(v) => set({ vurgu: v })} />
        </div>
      </Bolum>
      <Bolum baslik="Satır ve aralık">
        <Kaydir ad="Satır aralığı" deger={ayar.satir} min={1} max={2.2} adim={0.05} birim="×" degis={(v) => set({ satir: v })} />
        <Kaydir ad="Paragraf aralığı" deger={ayar.paragraf} min={0} max={10} adim={0.5} birim="pt" degis={(v) => set({ paragraf: v })} />
        <Kaydir ad="Soru arası" deger={ayar.soruArasi} min={0} max={24} adim={0.5} birim="mm" degis={(v) => set({ soruArasi: v })} />
        <Kaydir ad="Yazma satırı" deger={ayar.yazmaSatiri} min={0} max={10} birim="satır" degis={(v) => set({ yazmaSatiri: Math.round(v) })} />
        <Seg ad="Sorular arası çizgi" kucuk deger={ayar.ayirici} degis={(ayirici) => set({ ayirici })} ogeler={[{ v: 'yok', ad: 'Çizgi yok' }, { v: 'solid', ad: 'Düz' }, { v: 'dashed', ad: 'Kesik' }, { v: 'dotted', ad: 'Nokta' }, { v: 'double', ad: 'Çift' }]} />
      </Bolum>
      <Bolum baslik="Numara ve şıklar">
        <Seg ad="Şık düzeni" deger={ayar.secenekDuzen} degis={(secenekDuzen) => set({ secenekDuzen })} ogeler={[{ v: 'alt', ad: 'Alt alta' }, { v: 'iki', ad: 'İki sütun' }, { v: 'yan', ad: 'Yan yana' }]} />
        <Seg ad="Soru numarası" kucuk deger={ayar.numara} degis={(numara) => set({ numara })} ogeler={[{ v: '1.', ad: '1.' }, { v: '1)', ad: '1)' }, { v: 'S1.', ad: 'S1.' }, { v: 'Soru 1', ad: 'Soru 1' }]} />
        <Seg ad="Şık harfi" kucuk deger={ayar.harf} degis={(harf) => set({ harf })} ogeler={[{ v: 'A)', ad: 'A)' }, { v: 'A.', ad: 'A.' }, { v: '(A)', ad: '(A)' }, { v: 'a)', ad: 'a)' }]} />
      </Bolum>
    </>
  );

  const panelRenk = (
    <>
      <Bolum baslik="Renklendirme" alt="Soruları bir özelliğe göre renklendir: aynı ders/konu/yıl aynı rengi alır.">
        <Seg ad="Renk anahtarı" kucuk deger={ayar.renkAlan} degis={(renkAlan) => set({ renkAlan })} ogeler={[{ v: 'yok', ad: 'Yok' }, { v: 'ders', ad: 'Ders' }, { v: 'konu', ad: 'Konu' }, { v: 'yil', ad: 'Yıl' }, { v: 'kaynak', ad: 'Kaynak' }, { v: 'kurul', ad: 'Kurul' }, { v: 'tur', ad: 'Tür' }]} />
        {ayar.renkAlan !== 'yok' && (
          <>
            <Seg ad="Renk biçimi" deger={ayar.renkStil} degis={(renkStil) => set({ renkStil })} ogeler={[{ v: 'serit', ad: 'Şerit' }, { v: 'etiket', ad: 'Etiket' }, { v: 'zemin', ad: 'Zemin' }, { v: 'numara', ad: 'Numara' }]} />
            <div className="sx15-palet" role="radiogroup" aria-label="Palet">
              {(Object.keys(PALETLER) as Ayar['palet'][]).map((p) => (
                <button key={p} type="button" role="radio" aria-checked={ayar.palet === p} className={ayar.palet === p ? 'is-on' : ''} onClick={() => set({ palet: p })}>
                  <span>{PALETLER[p].renk.slice(0, 6).map((c) => <i key={c} style={{ background: c }} />)}</span>{PALETLER[p].ad}
                </button>
              ))}
            </div>
            {lejant.length > 0 && (
              <div className="sx15-lejant">
                <div className="sx15-coklu-b"><b>Renk anahtarı ({lejant.length})</b>{Object.keys(ayar.renkOzel).some((k) => k.startsWith(`${ayar.renkAlan}:`)) && <button type="button" className="sx15-lnk" onClick={() => set({ renkOzel: Object.fromEntries(Object.entries(ayar.renkOzel).filter(([k]) => !k.startsWith(`${ayar.renkAlan}:`))) })}>Renkleri sıfırla</button>}</div>
                <ul>
                  {lejant.slice(0, 40).map((l) => (
                    <li key={l.v}>
                      <input type="color" aria-label={`${l.v} rengi`} value={l.renk} onChange={(e) => set({ renkOzel: { ...ayar.renkOzel, [`${ayar.renkAlan}:${l.v}`]: e.target.value } })} />
                      <span>{l.v}</span><em>{l.n}</em>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </>
        )}
        {ayar.grupla !== 'yok' && <Anahtar ad="Grup başlıkları renkli" acik={ayar.grupRenkli} degis={(v) => set({ grupRenkli: v })} />}
      </Bolum>
      <Bolum baslik="Etiketler" alt="Her sorunun üstünde ya da altında gösterilecek bilgiler.">
        <div className="sx15-cipler">
          {([['kurul', 'Kurul'], ['ders', 'Ders'], ['konu', 'Konu'], ['yil', 'Yıl'], ['kaynak', 'Kaynak'], ['tur', 'Tür'], ['zorluk', 'Zorluk']] as [keyof Ayar['etiket'], string][]).map(([k, ad]) => (
            <button key={k} type="button" aria-pressed={ayar.etiket[k]} className={`sx15-cip${ayar.etiket[k] ? ' is-on' : ''}`} onClick={() => set({ etiket: { ...ayar.etiket, [k]: !ayar.etiket[k] } })}>{ayar.etiket[k] && <Check aria-hidden />}<span>{ad}</span></button>
          ))}
        </div>
        <Seg ad="Etiket yeri" kucuk deger={ayar.etiketYeri} degis={(etiketYeri) => set({ etiketYeri })} ogeler={[{ v: 'ust', ad: 'Sorunun üstünde' }, { v: 'alt', ad: 'Sorunun altında' }]} />
      </Bolum>
    </>
  );

  const YERLER: { v: Ayar['cozumYeri']; ad: string; alt: string }[] = [
    { v: 'yok', ad: 'Çözüm yok', alt: 'Yalnız sorular (deneme, sınav)' },
    { v: 'altinda', ad: 'Sorunun altında', alt: 'Her sorunun hemen altında kutu içinde' },
    { v: 'sayfaAlti', ad: 'Sayfa altında cevaplar', alt: 'Her sayfanın altında o sayfanın cevap şeridi' },
    { v: 'arkada', ad: 'Her sayfanın ardından', alt: 'Soru sayfası → çözüm sayfası (kart arkası)' },
    { v: 'sonda', ad: 'Belgenin sonunda', alt: 'Tüm çözümler en sonda, sırayla' },
  ];
  const panelCozum = (
    <>
      <Bolum baslik="Doğru cevap">
        <Anahtar ad="Doğru şıkkı işaretle" alt="Soruda doğru seçenek vurgulanır" acik={ayar.dogruIsaret} degis={(v) => set({ dogruIsaret: v })} />
        {ayar.dogruIsaret && <Seg ad="İşaret biçimi" kucuk deger={ayar.isaretStil} degis={(isaretStil) => set({ isaretStil })} ogeler={[{ v: 'kalin', ad: 'Kalın renkli' }, { v: 'zemin', ad: 'Fosforlu' }, { v: 'tik', ad: 'Tik ✓' }, { v: 'daire', ad: 'Daire Ⓐ' }]} />}
      </Bolum>
      <Bolum baslik="Çözümlerin yeri">
        <div className="sx15-yer" role="radiogroup" aria-label="Çözümlerin yeri">
          {YERLER.map((y) => (
            <button key={y.v} type="button" role="radio" aria-checked={ayar.cozumYeri === y.v} className={ayar.cozumYeri === y.v ? 'is-on' : ''} onClick={() => set({ cozumYeri: y.v })}>
              <i aria-hidden /><span><b>{y.ad}</b><small>{y.alt}</small></span>
            </button>
          ))}
        </div>
        {ayar.cozumYeri === 'arkada' && ayar.duzen !== 'akis' && <Anahtar ad="Arka yüzü aynala" alt="Çift yüz baskıda her kartın çözümü arkasına denk gelir" acik={ayar.arkaAyna} degis={(v) => set({ arkaAyna: v })} />}
      </Bolum>
      {ayar.cozumYeri !== 'yok' && ayar.cozumYeri !== 'sayfaAlti' && (
        <Bolum baslik="Çözümde neler olsun">
          <div className="sx15-iki">
            <Anahtar ad="Cevap harfi" acik={ayar.cozumIcerik.harf} degis={(v) => set({ cozumIcerik: { ...ayar.cozumIcerik, harf: v } })} />
            <Anahtar ad="Açıklama" acik={ayar.cozumIcerik.aciklama} degis={(v) => set({ cozumIcerik: { ...ayar.cozumIcerik, aciklama: v } })} />
            <Anahtar ad="Şık şık açıklama" acik={ayar.cozumIcerik.siklar} degis={(v) => set({ cozumIcerik: { ...ayar.cozumIcerik, siklar: v } })} />
            <Anahtar ad="Kaynak ve kazanım" acik={ayar.cozumIcerik.kaynak} degis={(v) => set({ cozumIcerik: { ...ayar.cozumIcerik, kaynak: v } })} />
          </div>
        </Bolum>
      )}
      <Bolum baslik="Ek sayfalar">
        <Anahtar ad="Cevap anahtarı" alt="Sonda numara-harf tablosu (renk anahtarıyla)" acik={ayar.cevapAnahtari} degis={(v) => set({ cevapAnahtari: v })} />
        <Anahtar ad="Cevap kâğıdı (optik)" alt="Sonda işaretlemelik A–E daireleri" acik={ayar.optik} degis={(v) => set({ optik: v })} />
      </Bolum>
    </>
  );

  const PANEL: Record<Sekme, React.ReactNode> = { sorular: panelSorular, tasarim: panelTasarim, sayfa: panelSayfa, metin: panelMetin, renk: panelRenk, cozum: panelCozum };

  const bicimSec = (
    <Seg ad="Biçim" deger={ayar.bicim} degis={(b) => set({ bicim: b })} ogeler={BICIMLER.map((b) => ({ v: b.id, ad: <><b.Ic aria-hidden />{b.ad}</> }))} />
  );
  const indirDugme = (
    <button type="button" className="v15-btn sx15-indir" disabled={!hs.length || !!uretim} onClick={() => void indir()}>
      {uretim ? <Loader2 className="sx15-don" aria-hidden /> : <bicim.Ic aria-hidden />}
      {uretim ? 'Hazırlanıyor…' : `${bicim.ad} indir`}
    </button>
  );

  return (
    <div className={`sx15 is-${mobil}`}>
      <h1 className="sr-only">Soru dışa aktarıcı</h1>
      <div className="sx15-mob sx15-seg" role="tablist" aria-label="Görünüm">
        <button type="button" role="tab" aria-selected={mobil === 'ayar'} className={mobil === 'ayar' ? 'is-on' : ''} onClick={() => setMobil('ayar')}><SlidersHorizontal aria-hidden />Ayarlar</button>
        <button type="button" role="tab" aria-selected={mobil === 'oniz'} className={mobil === 'oniz' ? 'is-on' : ''} onClick={() => setMobil('oniz')}><Eye aria-hidden />Önizleme{oniz ? ` · ${oniz.tahmini ? '≈' : ''}${oniz.sayfa}` : ''}</button>
      </div>

      <div className="sx15-sol">
        <nav className="sx15-tabs" aria-label="Ayar bölümleri">
          {SEKMELER.map(({ id, ad, Ic }) => (
            <button key={id} type="button" aria-current={sekme === id ? 'true' : undefined} className={sekme === id ? 'is-on' : ''} onClick={() => setSekme(id)}>
              <Ic aria-hidden /><span>{ad}</span>{id === 'sorular' && <em>{secili.length}</em>}{id === 'sorular' && suzgecSay > 0 && <Filter aria-label="süzgeç açık" className="sx15-f" />}
            </button>
          ))}
        </nav>
        <div className="sx15-panel v15-card">{PANEL[sekme]}</div>
      </div>

      <div className="sx15-sag-k">
        <div className="sx15-ust v15-card">
          {bicimSec}
          <div className="sx15-ust-s">
            <span className="sx15-ozet">{ozet}</span>
            <Seg ad="Yakınlık" kucuk deger={zum} degis={setZum} ogeler={[{ v: 'sigdir', ad: 'Sığdır' }, { v: 0.75, ad: '%75' }, { v: 1, ad: '%100' }]} />
          </div>
          {oniz && oniz.tasan > 0 && <p className="sx15-uyari">{oniz.tasan} soru hücresine en küçük ölçekte de sığmadı ve kırpıldı; sayfa başına daha az soru seç ya da puntoyu küçült.</p>}
          {ayar.bicim === 'pptx' && <p className="v15-cap">Her sayfa bir slayt olur; cevap kâğıdı slaytta da daireler hâlinde çizilir.</p>}
          {ayar.bicim === 'docx' && ayar.duzen === 'akis' && ayar.cozumYeri !== 'arkada' && ayar.cozumYeri !== 'sayfaAlti' && <p className="v15-cap">Word'de akış düzeni düzenlenebilir metin olarak gelir; sayfa sonları Word'ün yazı tipine göre birkaç satır kayabilir.</p>}
        </div>
        <Onizleme oniz={oniz} ayar={ayar} yukleniyor={onizYuk} zum={zum} />
        <div className="sx15-eylem">
          {indirDugme}
          <button type="button" className="v15-btn is-ghost" disabled={!hs.length || !!uretim} onClick={() => void indir(true)}><Printer aria-hidden />Yazdır</button>
        </div>
      </div>

      <div className="sx15-alt" role="region" aria-label="İndirme">
        <span>{uretim || ozet}</span>
        {indirDugme}
      </div>
      {uretim && <div className="sx15-perde" role="status"><Loader2 className="sx15-don" aria-hidden /><span>{uretim}</span></div>}
    </div>
  );
}
