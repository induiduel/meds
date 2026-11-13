import React, { useCallback, useDeferredValue, useEffect, useMemo, useRef, useState } from 'react';
import { useVirtualizer } from '@tanstack/react-virtual';
import {
  Check, CheckSquare, Columns2, Eye, FileDown, FileText, Filter, ImagePlus, LayoutGrid, ListChecks, Loader2, Palette, Plus, Presentation, Printer,
  RotateCcw, Save, Search, Shuffle, SlidersHorizontal, Trash2, Type, X,
} from 'lucide-react';
import { useV15Baslik } from './baslik';
import { BOS_SUZGEC, KAYNAKLAR, kaynakYukle, miniDesteler, secenekler, suz, type AQ, type KaynakId, type Suzgec } from './soruAktar/kaynak';
import {
  AGIRLIKLAR, ALANLAR, EN_COK_GRUP, KAGIT, LOGO_EN_COK, PALETLER, PX_MM, RENK_GRUP_AD, RENK_OGELERI, SIRALAMALAR, TASARIMLAR, TEMALAR, VARSAYILAN, YAZI, YAZI_TUR_AD,
  alanAdi, ayarNormal, karistir, ogeRenk, sayfaAraligi, tasarimUygula, temaUygula, yaprakOlcu, yaziBaglantilari,
  type Alan, type Ayar, type Bicim, type Duzen, type RenkOge, type TasarimId, type YaziId,
} from './soruAktar/ayar';
import { Olcer, belgeHtml, ciktiSuz, hazirla, kagitAdi, renkHaritasi, sayfala, yaprakSayisi, type HS } from './soruAktar/belge';
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
const SABLON_EN_COK = 40;
const oku = <T,>(k: string, v: T): T => { try { const r = localStorage.getItem(k); return r ? JSON.parse(r) : v; } catch { return v; } };
const yaz = (k: string, v: unknown) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* özel pencere */ } };

/** Soru sayısı sınırı (Tümü / İlk N / Rastgele N) */
type Sinir = { mod: 'hepsi' | 'ilk' | 'rastgele'; n: number };
/** Şablon: o anki TÜM ayarlar — belge ayarı, soru süzgeci, soru sayısı ve önizleme yakınlığı */
type Sablon = { ad: string; tarih: number; ayar: Ayar; suzgec?: Omit<Suzgec, 'arama'>; sinir?: Sinir; zum?: 'sigdir' | number };
/** Eski şablonlar (yalnız `ayar`) da okunur; eksik katmanlar yüklenirken atlanır */
function sablonlariOku(): Sablon[] {
  const ham = oku<unknown[]>(TKEY, []);
  if (!Array.isArray(ham)) return [];
  return ham.flatMap((x) => {
    const s = x as Partial<Sablon>;
    if (!s || typeof s.ad !== 'string' || !s.ad.trim() || !s.ayar) return [];
    return [{ ad: s.ad.slice(0, 60), tarih: Number(s.tarih) || 0, ayar: s.ayar, suzgec: s.suzgec, sinir: s.sinir, zum: s.zum }];
  }).slice(0, SABLON_EN_COK);
}
/** İki ayarı/süzgeci anahtar sırasından bağımsız karşılaştırmak için kanonik JSON */
function kanonik(v: unknown): string {
  if (Array.isArray(v)) return `[${v.map(kanonik).join(',')}]`;
  if (v && typeof v === 'object') return `{${Object.keys(v as object).sort().map((k) => `${JSON.stringify(k)}:${kanonik((v as Record<string, unknown>)[k])}`).join(',')}}`;
  return JSON.stringify(v ?? null);
}
const sablonTarih = (t: number) => (t ? new Date(t).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short', year: '2-digit' }) : '');
/** Şablon listesinde tek satır özet: tasarım · düzen · kaynak · soru sayısı · tarih */
function sablonOzet(x: Sablon): string {
  const t = TASARIMLAR.find((y) => y.id === x.ayar.tasarim)?.ad || 'Tasarım';
  const d = x.ayar.duzen === 'akis' ? 'akış' : `${x.ayar.duzen}/sayfa`;
  const k = x.suzgec?.kaynaklar?.length || 0;
  const n = x.sinir && x.sinir.mod !== 'hepsi' ? ` · ${x.sinir.mod === 'ilk' ? 'ilk' : 'rastgele'} ${x.sinir.n} soru` : '';
  return [t, d, k ? `${k} kaynak` : '', n.replace(/^ · /, ''), sablonTarih(x.tarih)].filter(Boolean).join(' · ');
}

type Sekme = 'sorular' | 'tasarim' | 'sayfa' | 'metin' | 'renk' | 'cozum' | 'sablon';
const SEKMELER: { id: Sekme; ad: string; Ic: React.ElementType }[] = [
  { id: 'sorular', ad: 'Sorular', Ic: ListChecks },
  { id: 'tasarim', ad: 'Tasarım', Ic: LayoutGrid },
  { id: 'sayfa', ad: 'Sayfa', Ic: FileText },
  { id: 'metin', ad: 'Metin', Ic: Type },
  { id: 'renk', ad: 'Renk', Ic: Palette },
  { id: 'cozum', ad: 'Çözüm', Ic: CheckSquare },
  { id: 'sablon', ad: 'Şablon', Ic: Save },
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
function Renk({ ad, deger, degis, sifirla }: { ad: string; deger: string; degis: (v: string) => void; sifirla?: () => void }) {
  return (
    <label className="sx15-renk">
      <input type="color" value={hex6(deger)} onChange={(e) => degis(e.target.value)} />
      <span>{ad}</span>
      {sifirla && <button type="button" className="sx15-renk-x" aria-label={`${ad} rengini sıfırla`} title="Varsayılana dön" onClick={(e) => { e.preventDefault(); sifirla(); }}><X aria-hidden /></button>}
    </label>
  );
}
/** #rrggbb(aa) → #rrggbb; saydam ton beyazla karıştırılır; boş değer gri */
function hex6(c: string, zemin = '#ffffff'): string {
  const m = /^#([0-9a-f]{6})([0-9a-f]{2})?$/i.exec(c || '');
  if (!m) return '#9ca3af';
  if (!m[2]) return `#${m[1].toLowerCase()}`;
  return karisHex(`#${m[1]}`, parseInt(m[2], 16) / 255, zemin);
}
function karisHex(c: string, oran: number, zemin: string): string {
  const p = (h: string, i: number) => parseInt(h.slice(i, i + 2), 16);
  const a = c.replace('#', ''), b = (/^#[0-9a-f]{6}/i.test(zemin) ? zemin : '#ffffff').replace('#', '');
  return '#' + [0, 2, 4].map((i) => Math.round(p(a, i) * oran + p(b, i) * (1 - oran)).toString(16).padStart(2, '0')).join('');
}
/** Öge renginin renk kutusunda görünen değeri (türetilmiş/saydam renkler düz tona çevrilir) */
function ogeGoster(a: Ayar, k: RenkOge): string {
  const v = ogeRenk(a, k);
  const zemin = hex6(ogeRenk(a, 'sayfaZemin'));
  if (!v) return karisHex(a.vurgu, 0.07, zemin);
  return hex6(v, zemin);
}
const YAZI_GRUPLARI = (Object.keys(YAZI_TUR_AD) as (keyof typeof YAZI_TUR_AD)[]).map((t) => ({ t, ad: YAZI_TUR_AD[t], ids: (Object.keys(YAZI) as YaziId[]).filter((k) => YAZI[k].tur === t) }));
function YaziSec({ ad, deger, degis, ayni, ornek }: { ad: string; deger: string; degis: (v: string) => void; ayni?: boolean; ornek: string }) {
  const id = deger === 'ayni' ? undefined : (deger as YaziId);
  const t = id ? YAZI[id] : undefined;
  return (
    <div className="sx15-yazi">
      <label className="sx15-sel"><span>{ad}</span>
        <select value={deger} onChange={(e) => degis(e.target.value)}>
          {ayni && <option value="ayni">Gövde yazısıyla aynı</option>}
          {YAZI_GRUPLARI.map((g) => (
            <optgroup key={g.t} label={g.ad}>
              {g.ids.map((k) => <option key={k} value={k}>{YAZI[k].ad}{YAZI[k].alt ? ` — ${YAZI[k].alt}` : ''}{YAZI[k].g ? '' : ' (sistem)'}</option>)}
            </optgroup>
          ))}
        </select>
      </label>
      {t && <p className="sx15-yazi-on" style={{ fontFamily: t.css }}><b>{t.ad}</b> · {ornek}</p>}
    </div>
  );
}
function Metin({ ad, deger, degis, yer, cok, enCok = 140, ipucu }: { ad: string; deger: string; degis: (v: string) => void; yer?: string; cok?: boolean; enCok?: number; ipucu?: string }) {
  return (
    <label className="sx15-in"><span>{ad}</span>
      {cok ? <textarea className="sx15-ta" value={deger} placeholder={yer} maxLength={enCok} rows={4} spellCheck={false} onChange={(e) => degis(e.target.value)} />
        : <input type="text" value={deger} placeholder={yer} maxLength={enCok} onChange={(e) => degis(e.target.value)} />}
      {ipucu && <small className="sx15-ip">{ipucu}</small>}
    </label>
  );
}
/** Logo yükleme: resim küçültülür (en çok 900 × 360 px), PNG → sığmazsa JPEG; veri adresi ayarda saklanır (yalnız PDF/yazdırma) */
function LogoSec({ deger, degis }: { deger: string; degis: (v: string) => void }) {
  const al = (f: File | undefined) => {
    if (!f) return;
    if (!/^image\/(png|jpeg|webp|gif)$/.test(f.type)) { toast.error('Desteklenmeyen dosya', 'PNG, JPEG, WebP ya da GIF seç.'); return; }
    const img = new Image();
    const url = URL.createObjectURL(f);
    img.onload = () => {
      URL.revokeObjectURL(url);
      const k = Math.min(1, 900 / img.naturalWidth, 360 / img.naturalHeight);
      const c = document.createElement('canvas');
      c.width = Math.max(1, Math.round(img.naturalWidth * k));
      c.height = Math.max(1, Math.round(img.naturalHeight * k));
      c.getContext('2d')!.drawImage(img, 0, 0, c.width, c.height);
      let d = c.toDataURL('image/png');
      if (d.length > LOGO_EN_COK) d = c.toDataURL('image/jpeg', 0.85);
      if (d.length > LOGO_EN_COK) { toast.error('Logo çok büyük', 'Daha küçük ya da sade bir görsel seç (en çok ~160 KB).'); return; }
      degis(d);
    };
    img.onerror = () => { URL.revokeObjectURL(url); toast.error('Görsel okunamadı'); };
    img.src = url;
  };
  return (
    <div className="sx15-logo">
      {deger ? <img src={deger} alt="Logo" /> : <span className="sx15-logo-bos"><ImagePlus aria-hidden />Logo yok</span>}
      <div className="sx15-logo-b">
        <label className="v15-btn is-soft sx15-logo-sec"><input type="file" accept="image/png,image/jpeg,image/webp,image/gif" onChange={(e) => { al(e.target.files?.[0]); e.target.value = ''; }} />{deger ? 'Değiştir' : 'Logo yükle'}</label>
        {deger && <button type="button" className="v15-btn is-ghost" onClick={() => degis('')}><Trash2 aria-hidden />Kaldır</button>}
      </div>
    </div>
  );
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

/** İç içe gruplama katmanları: her satır bir katman (1 = en üst grup); alan seçilir, kaldırılır, en çok EN_COK_GRUP katman */
const HAZIR_GRUPLAR: { ad: string; v: Alan[] }[] = [
  { ad: 'Yıl › Kurul › Ders › Konu', v: ['yil', 'kurul', 'ders', 'konu'] },
  { ad: 'Kurul › Ders › Konu', v: ['kurul', 'ders', 'konu'] },
  { ad: 'Ders › Konu', v: ['ders', 'konu'] },
  { ad: 'Ders › Yıl', v: ['ders', 'yil'] },
  { ad: 'Etiket', v: ['etiket'] },
];
function GrupKatmanlari({ gruplar, degis }: { gruplar: Alan[]; degis: (v: Alan[]) => void }) {
  const bos = ALANLAR.filter((x) => !gruplar.includes(x.id));
  return (
    <div className="sx15-katman">
      {gruplar.length > 0 && (
        <ol className="sx15-kt-l">
          {gruplar.map((g, i) => (
            <li key={g} className="sx15-kt" style={{ '--sv': i } as React.CSSProperties}>
              <span className="sx15-kt-no" aria-hidden>{i + 1}</span>
              <label className="sx15-sel">
                <span className="sr-only">{i + 1}. katman</span>
                <select value={g} onChange={(e) => degis(gruplar.map((x, j) => (j === i ? (e.target.value as Alan) : x)))}>
                  {ALANLAR.filter((x) => x.id === g || !gruplar.includes(x.id)).map((x) => <option key={x.id} value={x.id}>{x.ad}</option>)}
                </select>
              </label>
              <small>{ALANLAR.find((x) => x.id === g)?.alt}</small>
              <button type="button" className="v15-ib" aria-label={`${alanAdi(g)} katmanını kaldır`} onClick={() => degis(gruplar.filter((_, j) => j !== i))}><X aria-hidden /></button>
            </li>
          ))}
        </ol>
      )}
      {gruplar.length < EN_COK_GRUP && bos.length > 0 && (
        <div className="sx15-cipler">
          {bos.map((x) => (
            <button key={x.id} type="button" className="sx15-cip is-dev" title={x.alt} onClick={() => degis([...gruplar, x.id])}><Plus aria-hidden /><span>{gruplar.length ? `${x.ad} alt grubu` : `${x.ad} ile grupla`}</span></button>
          ))}
        </div>
      )}
      <div className="sx15-hazir">
        <b>Hazır:</b>
        {HAZIR_GRUPLAR.map((h) => <button key={h.ad} type="button" className="sx15-lnk" onClick={() => degis(h.v)}>{h.ad}</button>)}
        {gruplar.length > 0 && <button type="button" className="sx15-lnk" onClick={() => degis([])}>Gruplama yok</button>}
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
interface Oniz { html: string; sayfa: number; /** yaprak sayısı (2'li / kitapçık) */ yaprak: number; yaprakli: boolean; tahmini: boolean; tasan: number; /** önizlemede gösterilen yaprak/sayfa */ gosterilen: number; /** sayfaya sığdırın seçtiği yazı ölçeği */ olcek: number; not?: string }

function Onizleme({ oniz, ayar, yukleniyor, zum }: { oniz: Oniz | null; ayar: Ayar; yukleniyor: boolean; zum: 'sigdir' | number }) {
  const dis = useRef<HTMLDivElement>(null);
  const fr = useRef<HTMLIFrameElement>(null);
  const [gen, setGen] = useState(600);
  const [aktif, setAktif] = useState(1);
  const { w, h } = yaprakOlcu(ayar);
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
          {oniz.yaprakli ? 'Yaprak' : 'Sayfa'} {aktif} / {oniz.tahmini ? '≈' : ''}{oniz.yaprakli ? oniz.yaprak : oniz.sayfa}
          {oniz.yaprakli && <span> · {oniz.tahmini ? '≈' : ''}{oniz.sayfa} sayfa</span>}
          {oniz.gosterilen < (oniz.yaprakli ? oniz.yaprak : oniz.sayfa) && <span> · önizlemede ilk {oniz.gosterilen} {oniz.yaprakli ? 'yaprak' : 'sayfa'}</span>}
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
  const [sablon, setSablon] = useState<Sablon[]>(sablonlariOku);
  const [sekme, setSekme] = useState<Sekme>('sorular');
  const [mobil, setMobil] = useState<'ayar' | 'oniz'>('ayar');
  const [veri, setVeri] = useState<Partial<Record<KaynakId, AQ[]>>>({});
  const [durum, setDurum] = useState<Partial<Record<KaynakId, 'y' | 'h'>>>({});
  const [desteler, setDesteler] = useState<DeckCatalogEntry[] | null>(null);
  const [cikarilan, setCikarilan] = useState<Set<string>>(() => new Set());
  const [sinir, setSinir] = useState<Sinir>({ mod: 'hepsi', n: 40 });
  const [oniz, setOniz] = useState<Oniz | null>(null);
  const [onizYuk, setOnizYuk] = useState(false);
  const [zum, setZum] = useState<'sigdir' | number>('sigdir');
  const [uretim, setUretim] = useState<string | null>(null);
  const [sablonAd, setSablonAd] = useState('');
  const set = useCallback((p: Partial<Ayar>) => setAyar((a) => ({ ...a, ...p })), []);
  const setS = useCallback((p: Partial<Suzgec>) => setSuzgec((s) => ({ ...s, ...p })), []);

  /* ---- şablon: o anki TÜM ayarlar (belge + süzgeç + soru sayısı + yakınlık) ---- */
  const sablonAnlik = useMemo<Omit<Sablon, 'ad' | 'tarih'>>(() => ({ ayar, suzgec: { ...suzgec, arama: '' }, sinir, zum }), [ayar, suzgec, sinir, zum]);
  const sablonImza = kanonik(sablonAnlik);
  const eslesenSablon = sablon.find((x) => kanonik({ ayar: ayarNormal(x.ayar), suzgec: x.suzgec, sinir: x.sinir, zum: x.zum }) === sablonImza)?.ad;
  const sablonKaydet = useCallback((ad: string) => {
    const temiz = ad.trim().slice(0, 60);
    if (!temiz) return;
    const yeni: Sablon = { ad: temiz, tarih: Date.now(), ...sablonAnlik };
    setSablon((l) => [yeni, ...l.filter((x) => x.ad !== temiz)].slice(0, SABLON_EN_COK));
    toast.success('Şablon kaydedildi', temiz);
  }, [sablonAnlik]);
  const sablonYukle = useCallback((x: Sablon) => {
    setAyar(ayarNormal(x.ayar));
    if (x.suzgec) {
      const k = x.suzgec.kaynaklar?.length ? x.suzgec.kaynaklar : BOS_SUZGEC.kaynaklar;
      setSuzgec({ ...BOS_SUZGEC, ...x.suzgec, kaynaklar: k, arama: '' });
    }
    if (x.sinir && ['hepsi', 'ilk', 'rastgele'].includes(x.sinir.mod)) setSinir({ mod: x.sinir.mod, n: Math.max(1, Math.round(Number(x.sinir.n) || 40)) });
    if (x.zum === 'sigdir' || typeof x.zum === 'number') setZum(x.zum);
    toast.info('Şablon yüklendi', `${x.ad} — belge ve soru süzgeçleri geri geldi`);
  }, []);
  const sablonSil = useCallback((ad: string) => setSablon((l) => l.filter((x) => x.ad !== ad)), []);
  const sablonDisaAktar = (liste: Sablon[], ad = 'medsor-sablonlar') => {
    if (!liste.length) return;
    const veri = { tur: 'medsor-soru-sablon', surum: 2, sablonlar: liste };
    downloadBlob(new Blob([JSON.stringify(veri, null, 2)], { type: 'application/json' }), `${safeFileName(ad)}.json`);
  };
  const sablonIceAktar = async (f: File | undefined) => {
    if (!f) return;
    try {
      const j = JSON.parse(await f.text());
      const ham: unknown[] = Array.isArray(j) ? j : Array.isArray(j?.sablonlar) ? j.sablonlar : [j];
      const gelen = ham.flatMap((x) => {
        const s = x as Partial<Sablon>;
        if (!s || typeof s.ad !== 'string' || !s.ad.trim() || !s.ayar) return [];
        return [{ ad: s.ad.trim().slice(0, 60), tarih: Number(s.tarih) || Date.now(), ayar: s.ayar, suzgec: s.suzgec, sinir: s.sinir, zum: s.zum } as Sablon];
      });
      if (!gelen.length) { toast.error('Şablon dosyası okunamadı', 'Dosyada ad ve ayar taşıyan şablon yok.'); return; }
      setSablon((l) => {
        const yeni = [...gelen];
        for (const x of l) if (!yeni.some((y) => y.ad === x.ad)) yeni.push(x);
        return yeni.slice(0, SABLON_EN_COK);
      });
      toast.success('Şablonlar içe aktarıldı', `${gelen.length} şablon eklendi (aynı ad varsa yenisi geçerli)`);
    } catch {
      toast.error('Dosya okunamadı', 'Geçerli bir şablon JSON dosyası seç.');
    }
  };

  useEffect(() => yaz(AKEY, ayar), [ayar]);
  // seçili Google yazı tiplerini panel önizlemesi için sayfaya da yükle
  useEffect(() => {
    for (const href of yaziBaglantilari(ayar)) {
      if (document.querySelector(`link[href="${href}"]`)) continue;
      const l = document.createElement('link');
      l.rel = 'stylesheet'; l.href = href;
      document.head.appendChild(l);
    }
  }, [ayar.yazi, ayar.yaziBaslik]); // eslint-disable-line react-hooks/exhaustive-deps
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
    etiketler: secenekler(tum, suzA, 'etiketler'),
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
        const b = ciktiSuz(await sayfala(parca, ayar, { olcer }), ayar);
        if (no !== sira.current) return;
        const tahmini = hs.length > parca.length;
        const toplam = tahmini ? Math.max(b.sayfalar.length, Math.round((b.sayfalar.length * hs.length) / parca.length)) : b.sayfalar.length;
        const kapakVar = b.sayfalar[0]?.tur === 'kapak';
        const yaprakli = yaprakOlcu(ayar).sayfa > 1;
        setOniz({
          html: belgeHtml(b, ayar, { onizleme: true, ilk: ONIZ_SAYFA, tum: hs, toplamSayfa: tahmini ? toplam : undefined }),
          sayfa: toplam, yaprak: yaprakSayisi(toplam, ayar, kapakVar), yaprakli, tahmini, tasan: b.tasan,
          gosterilen: Math.min(ONIZ_SAYFA, yaprakSayisi(b.sayfalar.length, ayar, kapakVar)), olcek: b.olcek, not: b.sigdirNot,
        });
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
      const b = ciktiSuz(await sayfala(hs, yazdir ? { ...a, bicim: 'pdf' } : a), a);
      if (!b.sayfalar.length) { toast.info('Seçime uyan sayfa yok', 'Çıktı seçimini ya da sayfa aralığını değiştir.'); return; }
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
  const suzgecSay = suzgec.kurullar.length + suzgec.dersler.length + suzgec.konular.length + suzgec.yillar.length + suzgec.turler.length + suzgec.zorluk.length + suzgec.etiketler.length + (suzgec.cevapli ? 1 : 0) + (suzgec.aciklamali ? 1 : 0) + (suzgec.arama ? 1 : 0);
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
      <Bolum baslik="Süzgeçler" sag={suzgecSay > 0 ? <button type="button" className="sx15-lnk" onClick={() => setS({ kurullar: [], dersler: [], konular: [], yillar: [], turler: [], zorluk: [], etiketler: [], cevapli: false, aciklamali: false, arama: '' })}><RotateCcw aria-hidden />Temizle</button> : undefined}>
        <label className="sx15-ara is-b"><Search aria-hidden /><input type="search" value={suzgec.arama} placeholder="Soru metninde ara (ör. nefrotik, akut başlangıç)" onChange={(e) => setS({ arama: e.target.value })} /></label>
        <CokSecim ad="Kurul" liste={sec.kurullar} secili={suzgec.kurullar.map(String)} degis={(v) => setS({ kurullar: v.map(Number) })} ad2={(v) => `Kurul ${v}`} />
        <CokSecim ad="Ders" liste={sec.dersler} secili={suzgec.dersler} degis={(v) => setS({ dersler: v })} />
        <CokSecim ad="Konu" liste={sec.konular} secili={suzgec.konular} degis={(v) => setS({ konular: v })} />
        <CokSecim ad="Yıl" liste={sec.yillar} secili={suzgec.yillar} degis={(v) => setS({ yillar: v })} ad2={(v) => (v === '—' ? 'Yılsız' : v)} />
        <CokSecim ad="Soru türü" liste={sec.turler} secili={suzgec.turler} degis={(v) => setS({ turler: v })} />
        <CokSecim ad="Zorluk" liste={sec.zorluk} secili={suzgec.zorluk} degis={(v) => setS({ zorluk: v })} ad2={(v) => (v === '—' ? 'Belirtilmemiş' : v[0].toLocaleUpperCase('tr') + v.slice(1))} />
        <CokSecim ad="Etiket" liste={sec.etiketler} secili={suzgec.etiketler} degis={(v) => setS({ etiketler: v })} />
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
            <Anahtar ad="Kesim çizgileri" alt="Hücreler arasında kesik çizgi: kartları makasla kesmek için" acik={ayar.kesimCizgi} degis={(v) => set({ kesimCizgi: v })} />
            <Kaydir ad="Hücre aralığı" deger={ayar.hucreAralik} min={0} max={20} adim={0.5} birim="mm" degis={(v) => set({ hucreAralik: v })} />
          </>
        )}
      </Bolum>
      <Bolum baslik="Sayfaya sığdır" alt="Yazı ölçeğini belgeye göre seçer: seyrek kalan son sayfa kaldırılır, sayfalar dolar. Akış düzeninde tüm belgeye, ızgarada hücrelere uygulanır.">
        <Seg ad="Sayfaya sığdır" deger={ayar.sigdir} degis={(sigdir) => set({ sigdir })} ogeler={[{ v: 'yok', ad: 'Kapalı', title: 'Ayarlanan punto aynen kullanılır' }, { v: 'kucult', ad: 'Yalnız küçült', title: 'Seyrek son sayfayı kaldırmak için yazıyı küçültür' }, { v: 'doldur', ad: 'Doldur', title: 'Sayfalar dolsun diye küçültür ya da büyütür' }]} />
        {ayar.sigdir !== 'yok' && ayar.duzen === 'akis' && (
          <>
            <Kaydir ad="Hedef sayfa" deger={ayar.sigdirHedef} min={0} max={Math.max(2, Math.min(300, oniz?.sayfa || 20))} birim="sayfa" degis={(v) => set({ sigdirHedef: Math.round(v) })} />
            <p className="v15-cap">{ayar.sigdirHedef > 0 ? `Belge ${ayar.sigdirHedef} içerik sayfasına sığdırılır (kapak, cevap anahtarı ve cevap kâğıdı sayılmaz).` : 'Hedef 0 = kendiliğinden: gövdesinin yarısından azı dolu son sayfa varsa bir sayfa aza sığdırılır.'}</p>
          </>
        )}
        {ayar.sigdir !== 'yok' && ayar.duzen !== 'akis' && <p className="v15-cap">Izgarada sayfa sayısı hücre sayısından gelir; "Doldur" her sayfadaki hücrelere sığan ortak en büyük yazı ölçeğini kullanır.</p>}
      </Bolum>
      <Bolum baslik="Sıralama">
        <label className="sx15-sel"><span>Sırala</span>
          <select value={ayar.sirala} onChange={(e) => set({ sirala: e.target.value as Ayar['sirala'] })}>
            {SIRALAMALAR.map((x) => <option key={x.id} value={x.id}>{x.ad}</option>)}
          </select>
        </label>
        {ayar.sirala === 'rastgele' && <button type="button" className="v15-btn is-ghost sx15-kb" onClick={() => set({ tohum: ayar.tohum + 1 })}><Shuffle aria-hidden />Yeniden karıştır</button>}
        <Anahtar ad="Şıkları karıştır" alt="Cevap anahtarı yeni sıraya göre yazılır" acik={ayar.sikKaristir} degis={(v) => set({ sikKaristir: v })} />
        <Kaydir ad="İlk soru numarası" deger={ayar.numaraBas} min={1} max={500} degis={(v) => set({ numaraBas: Math.round(v) })} />
      </Bolum>
      <Bolum baslik="Gruplama" alt="İç içe katmanlar: önce 1. katmana göre kümelenir, her küme kendi içinde 2. katmana göre … (en çok 4). Grup içi sıra yukarıdaki sıralamadır.">
        <GrupKatmanlari gruplar={ayar.gruplar} degis={(gruplar) => set({ gruplar })} />
        {ayar.gruplar.length > 0 && (
          <>
            <Seg ad="Grupların sırası" kucuk deger={ayar.grupSirasi} degis={(grupSirasi) => set({ grupSirasi })} ogeler={[{ v: 'olagan', ad: 'Olağan', title: 'Yıl yeni önce, kurul numarası, zorluk kolaydan, ad A→Z' }, { v: 'sayiAzalan', ad: 'Çok sorudan aza' }, { v: 'sayiArtan', ad: 'Az sorudan çoğa' }]} />
            <Seg ad="Başlık biçimi" kucuk deger={ayar.grupStil} degis={(grupStil) => set({ grupStil })} ogeler={[{ v: 'cizgi', ad: 'Alt çizgi' }, { v: 'bant', ad: 'Bant' }, { v: 'kutu', ad: 'Kutu' }, { v: 'sade', ad: 'Sade' }]} />
            <div className="sx15-iki">
              <Anahtar ad="Başlıkta soru sayısı" acik={ayar.grupSayi} degis={(v) => set({ grupSayi: v })} />
              <Anahtar ad="Başlıklar renkli" alt="Ders başlığı dersin rengini, diğerleri renk anahtarını alır" acik={ayar.grupRenkli} degis={(v) => set({ grupRenkli: v })} />
              <Anahtar ad="Her üst grup yeni sayfada" acik={ayar.grupYeniSayfa || ayar.duzen !== 'akis'} kapali={ayar.duzen !== 'akis'} degis={(v) => set({ grupYeniSayfa: v })} />
              <Anahtar ad="Numara grupta yeniden" acik={ayar.grupNumara} degis={(v) => set({ grupNumara: v })} />
            </div>
          </>
        )}
      </Bolum>
      <Bolum baslik="Şablonlar" alt="Şablonlar artık yalnız tasarımı değil, soru süzgeçleri ve soru sayısı dahil TÜM ayarları saklar.">
        <button type="button" className="v15-btn is-soft sx15-kb" onClick={() => setSekme('sablon')}><Save aria-hidden />Şablonları aç ({sablon.length})</button>
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
        {ayar.bicim === 'pdf' && (
          <>
            <span className="sx15-etk">Yaprak düzeni</span>
            <Seg ad="Yaprak düzeni" kucuk deger={ayar.yaprak} degis={(yaprak) => set({ yaprak })} ogeler={[{ v: 'tek', ad: 'Sayfa başına 1' }, { v: 'iki', ad: 'Yaprakta 2 sayfa', title: 'İki sayfa yan yana, yatay yaprakta yarım ölçekte' }, { v: 'kitapcik', ad: 'Kitapçık', title: 'Katlanınca sıra doğru çıkar: yaprakları çift yüz basıp ortadan katla' }]} />
            {ayar.yaprak !== 'tek' && <p className="v15-cap">{ayar.yaprak === 'kitapcik' ? `Sayfalar ${kagitAdi({ ...ayar, yatay: !ayar.yatay })} yaprağa katlama sırasıyla dizilir; "çift yüz, kısa kenardan çevir" ile bas, ortadan katla.` : `İki sayfa ${kagitAdi({ ...ayar, yatay: !ayar.yatay })} yaprakta yan yana basılır (yarım ölçek, aradan kesilebilir).`} Word ve PowerPoint tek sayfa kalır.</p>}
          </>
        )}
        <Anahtar ad="Çift yüz baskı (cilt payı)" alt="Sol kenar iç kenar olur, çift sayfalarda sağa geçer; kapak varsa ardına boş sayfa gelir" acik={ayar.ciftYuz} degis={(v) => set({ ciftYuz: v })} />
      </Bolum>
      <Bolum baslik="Dışa aktarım" alt="Belgenin hangi sayfaları indirilir. Öğrenci ve öğretmen kopyası için iki kez indir.">
        <Seg ad="Çıktı" kucuk deger={ayar.cikti} degis={(cikti) => set({ cikti })} ogeler={[{ v: 'hepsi', ad: 'Tüm sayfalar' }, { v: 'sorular', ad: 'Yalnız sorular', title: 'Kapak, soru sayfaları ve cevap kâğıdı; çözüm ve cevap anahtarı çıkmaz' }, { v: 'cozumler', ad: 'Yalnız çözümler', title: 'Çözüm sayfaları ve cevap anahtarı' }]} />
        {ayar.cikti === 'cozumler' && ayar.cozumYeri === 'yok' && !ayar.cevapAnahtari && <p className="sx15-uyari">Çözüm yeri "yok" ve cevap anahtarı kapalı: bu seçimde sayfa çıkmaz.</p>}
        <Metin ad="Sayfa aralığı" deger={ayar.sayfaAralik} degis={(v) => set({ sayfaAralik: v.replace(/[^\d,\- ]/g, '') })} yer="ör. 1-4, 7 (boş = tümü)" enCok={60} ipucu={ayar.sayfaAralik && !sayfaAraligi(ayar.sayfaAralik) ? 'Aralık okunamadı; tümü dışa aktarılır.' : 'Kapak sayılmaz; numaralar belgedeki sayfa numarasıdır.'} />
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
      <Bolum baslik="Sayfa başlığı">
        <Anahtar ad="Sayfa başlığı" acik={ayar.baslikAcik} degis={(v) => set({ baslikAcik: v })} />
        <Metin ad="Başlık" deger={ayar.baslik} degis={(v) => set({ baslik: v })} yer="Soru kitapçığı" />
        <Metin ad="Alt başlık" deger={ayar.altBaslik} degis={(v) => set({ altBaslik: v })} yer="ör. Kurul 2 · Patoloji tekrar" />
        {ayar.baslikAcik && (
          <>
            <div className="sx15-iki">
              <Anahtar ad="Ad Soyad alanı" acik={ayar.adSoyad} degis={(v) => set({ adSoyad: v })} />
              <Anahtar ad="Tarih alanı" acik={ayar.tarih} degis={(v) => set({ tarih: v })} />
              <Anahtar ad="Her sayfada" alt="Kapalıysa yalnız ilk sayfada" acik={ayar.baslikHerSayfa} degis={(v) => set({ baslikHerSayfa: v })} />
            </div>
            <span className="sx15-etk">Başlık biçimi</span>
            <Seg ad="Başlık biçimi" kucuk deger={ayar.baslikStil} degis={(baslikStil) => set({ baslikStil })} ogeler={[{ v: 'cizgi', ad: 'Alt çizgi' }, { v: 'bant', ad: 'Renkli bant', title: 'Vurgu renkli tam genişlik bant, açık yazı' }, { v: 'kutu', ad: 'Kutu' }, { v: 'sade', ad: 'Sade' }]} />
            <Seg ad="Başlık hizası" kucuk deger={ayar.baslikHiza} degis={(baslikHiza) => set({ baslikHiza })} ogeler={[{ v: 'sol', ad: 'Sola' }, { v: 'orta', ad: 'Ortaya' }]} />
          </>
        )}
      </Bolum>
      <Bolum baslik="Logo" alt="Başlıkta ve/veya kapakta görsel (okul, dernek, kişisel amblem). PDF ve yazdırmada görünür; Word/PowerPoint'e aktarılmaz.">
        <LogoSec deger={ayar.logo} degis={(v) => set({ logo: v })} />
        {ayar.logo && (
          <>
            <Seg ad="Logo yeri" kucuk deger={ayar.logoYer} degis={(logoYer) => set({ logoYer })} ogeler={[{ v: 'ikisi', ad: 'Başlık + kapak' }, { v: 'baslik', ad: 'Yalnız başlık' }, { v: 'kapak', ad: 'Yalnız kapak' }]} />
            <Kaydir ad="Yükseklik" deger={ayar.logoYuk} min={4} max={24} adim={0.5} birim="mm" degis={(v) => set({ logoYuk: v })} />
          </>
        )}
      </Bolum>
      <Bolum baslik="Alt bilgi" alt="Üç bölge: sol, orta, sağ. Yer tutucular: {sayfa} {toplam} {tarih} {baslik} {altbaslik} {soru}">
        <Metin ad="Sol" deger={ayar.altMetin} degis={(v) => set({ altMetin: v })} yer="ör. MeDSor · {tarih}" />
        <div className="sx15-iki">
          <Metin ad="Orta" deger={ayar.altOrta} degis={(v) => set({ altOrta: v })} yer="ör. {baslik}" />
          <Metin ad="Sağ" deger={ayar.altSag} degis={(v) => set({ altSag: v })} yer="ör. {soru} soru" />
        </div>
        <Anahtar ad="Sayfa numarası" acik={ayar.sayfaNo} degis={(v) => set({ sayfaNo: v })} />
        {ayar.sayfaNo && (
          <>
            <Seg ad="Sayfa numarası yeri" kucuk deger={ayar.sayfaNoYer} degis={(sayfaNoYer) => set({ sayfaNoYer })} ogeler={[{ v: 'sol', ad: 'Solda' }, { v: 'orta', ad: 'Ortada' }, { v: 'sag', ad: 'Sağda' }]} />
            <Seg ad="Sayfa numarası biçimi" kucuk deger={ayar.sayfaNoBicim} degis={(sayfaNoBicim) => set({ sayfaNoBicim })} ogeler={[{ v: 'bolme', ad: '3 / 12' }, { v: 'duz', ad: '3' }, { v: 'sayfa', ad: 'Sayfa 3' }, { v: 'tire', ad: '– 3 –' }]} />
          </>
        )}
        <Anahtar ad="Alt bilgi üstünde çizgi" acik={ayar.altCizgi} degis={(v) => set({ altCizgi: v })} />
        <Kaydir ad="Not alanı" deger={ayar.notAlani} min={0} max={80} adim={2} birim="mm" degis={(v) => set({ notAlani: v })} />
        {ayar.notAlani > 0 && <p className="v15-cap">Her sayfanın altında "Notlar" başlıklı çizgili alan; sorular bu alanın üstünde kalır.</p>}
      </Bolum>
      <Bolum baslik="Kapak ve zemin">
        <Anahtar ad="Kapak sayfası" alt="Başlık, soru/ders sayısı, renk anahtarı, ad alanı" acik={ayar.kapak} degis={(v) => set({ kapak: v })} />
        {ayar.kapak && (
          <>
            <Seg ad="Kapak biçimi" kucuk deger={ayar.kapakStil} degis={(kapakStil) => set({ kapakStil })} ogeler={[{ v: 'sade', ad: 'Sade' }, { v: 'bant', ad: 'Yan bant' }, { v: 'zemin', ad: 'Renkli zemin', title: 'Vurgu renginde tam sayfa, açık yazı' }]} />
            <Metin ad="Kapak notu" cok enCok={200} deger={ayar.kapakNot} degis={(v) => set({ kapakNot: v })} yer="ör. Süre: 60 dakika · Her soru 2,5 puan" ipucu="Yer tutucular: {tarih} {soru} {toplam}" />
          </>
        )}
        <Metin ad="Filigran" deger={ayar.filigran} degis={(v) => set({ filigran: v })} yer="ör. TASLAK" />
        <span className="sx15-etk">Zemin deseni</span>
        <Seg ad="Zemin deseni" kucuk deger={ayar.desen} degis={(desen) => set({ desen })} ogeler={[{ v: 'yok', ad: 'Düz' }, { v: 'cizgili', ad: 'Çizgili' }, { v: 'kareli', ad: 'Kareli' }, { v: 'noktali', ad: 'Noktalı' }]} />
        {ayar.desen !== 'yok' && <p className="v15-cap">Defter kâğıdı görünümü; rengi Renk › Öge renkleri › "Zemin deseni". PDF ve yazdırmada.</p>}
      </Bolum>
      <Bolum baslik="Gelişmiş: özel CSS" alt="Belge CSS'ine eklenen kurallar (önizleme, PDF ve yazdırma). Sınıflar: .pg sayfa, .pg-bas başlık, .sb soru, .kok kök, .sk şıklar, .no numara, .hf şık harfi, .cz çözüm, .gb grup başlığı, .et etiketler, .pg-alt alt bilgi.">
        <Metin ad="Özel CSS" cok enCok={4000} deger={ayar.ozelCss} degis={(v) => set({ ozelCss: v })} yer={'.kok{text-transform:none}\n.sb:nth-child(odd){background:#f8fafc}'} />
      </Bolum>
    </>
  );

  const panelMetin = (
    <>
      <Bolum baslik="Yazı tipi" alt="Gövde ve başlık için ayrı yazı tipi seçebilirsin; Google yazı tipleri önizlemede, PDF'te ve Office belgelerinde (yüklüyse) kullanılır.">
        <YaziSec ad="Gövde yazısı" deger={ayar.yazi} degis={(v) => set({ yazi: v as YaziId })} ornek="Hücre zedelenmesi geri dönüşlü evrede şişme ile başlar. 0123456789" />
        <YaziSec ad="Başlık ve grup yazısı" ayni deger={ayar.yaziBaslik} degis={(v) => set({ yaziBaslik: v as Ayar['yaziBaslik'] })} ornek="Tıbbi Patoloji · Hücre Zedelenmesi" />
        <Kaydir ad="Punto" deger={ayar.punto} min={7} max={16} adim={0.5} birim="pt" degis={(v) => set({ punto: v })} />
        <Kaydir ad="Başlık oranı" deger={ayar.baslikOran} min={1} max={2.2} adim={0.05} birim="× punto" degis={(v) => set({ baslikOran: v })} />
        <Kaydir ad="Harf aralığı" deger={ayar.harfAralik} min={-0.05} max={0.2} adim={0.005} birim="em" degis={(v) => set({ harfAralik: v })} />
      </Bolum>
      <Bolum baslik="Yazı stili" alt="Kalınlık değişken Google yazı tiplerinde tam uygulanır; sistem yazılarında normal/kalın olarak yuvarlanır.">
        <span className="sx15-etk">Gövde kalınlığı</span>
        <Seg ad="Gövde kalınlığı" kucuk deger={ayar.agirlik} degis={(agirlik) => set({ agirlik })} ogeler={AGIRLIKLAR.map((x) => ({ v: x.v, ad: <span style={{ fontWeight: x.v }}>{x.ad}</span> }))} />
        <span className="sx15-etk">Başlık kalınlığı</span>
        <Seg ad="Başlık kalınlığı" kucuk deger={ayar.baslikAgirlik} degis={(baslikAgirlik) => set({ baslikAgirlik })} ogeler={AGIRLIKLAR.map((x) => ({ v: x.v, ad: <span style={{ fontWeight: x.v }}>{x.ad}</span> }))} />
        <span className="sx15-etk">Soru kökü</span>
        <Seg ad="Soru kökü stili" kucuk deger={ayar.kokStil} degis={(kokStil) => set({ kokStil, kokKalin: kokStil === 'kalin' || kokStil === 'kalinItalik' })} ogeler={[{ v: 'normal', ad: 'Normal' }, { v: 'kalin', ad: <b>Kalın</b> }, { v: 'italik', ad: <i>İtalik</i> }, { v: 'kalinItalik', ad: <b><i>Kalın italik</i></b> }]} />
        <span className="sx15-etk">Şık metni</span>
        <Seg ad="Şık metni stili" kucuk deger={ayar.sikStil} degis={(sikStil) => set({ sikStil })} ogeler={[{ v: 'normal', ad: 'Normal' }, { v: 'kalin', ad: <b>Kalın</b> }, { v: 'italik', ad: <i>İtalik</i> }, { v: 'kalinItalik', ad: <b><i>Kalın italik</i></b> }]} />
        <span className="sx15-etk">Sayfa başlığı harfleri</span>
        <Seg ad="Sayfa başlığı harfleri" kucuk deger={ayar.baslikBuyuk} degis={(baslikBuyuk) => set({ baslikBuyuk })} ogeler={[{ v: 'normal', ad: 'Olduğu gibi' }, { v: 'buyuk', ad: 'BÜYÜK HARF' }, { v: 'kucukBuyuk', ad: <span style={{ fontVariantCaps: 'small-caps' }}>Küçük Büyük</span> }]} />
        <span className="sx15-etk">Grup ve bant harfleri</span>
        <Seg ad="Grup başlığı harfleri" kucuk deger={ayar.grupBuyuk} degis={(grupBuyuk) => set({ grupBuyuk })} ogeler={[{ v: 'normal', ad: 'Olduğu gibi' }, { v: 'buyuk', ad: 'BÜYÜK HARF' }, { v: 'kucukBuyuk', ad: <span style={{ fontVariantCaps: 'small-caps' }}>Küçük Büyük</span> }]} />
        <Anahtar ad="İki yana yasla" acik={ayar.iki} degis={(v) => set({ iki: v })} />
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
        <span className="sx15-etk">Numara biçimi</span>
        <Seg ad="Numara biçimi" kucuk deger={ayar.numaraStil} degis={(numaraStil) => set({ numaraStil })} ogeler={[{ v: 'kalin', ad: <b>Kalın</b> }, { v: 'duz', ad: 'Düz' }, { v: 'kutu', ad: <span className="sx15-orn-kutu">1.</span> }, { v: 'daire', ad: <span className="sx15-orn-daire">1</span> }, { v: 'altCizgi', ad: <u>Altı çizili</u> }]} />
        <span className="sx15-etk">Şık harfi biçimi</span>
        <Seg ad="Şık harfi biçimi" kucuk deger={ayar.sikHarfStil} degis={(sikHarfStil) => set({ sikHarfStil })} ogeler={[{ v: 'kalin', ad: <b>Kalın</b> }, { v: 'normal', ad: 'Normal' }, { v: 'daire', ad: <span className="sx15-orn-daire">A</span> }, { v: 'kutu', ad: <span className="sx15-orn-kutu">A</span> }]} />
        <Kaydir ad="Şık girintisi" deger={ayar.sikGirinti} min={0} max={12} adim={0.5} birim="mm" degis={(v) => set({ sikGirinti: v })} />
        <Anahtar ad="Asılı girinti" alt="Numara dışarıda kalır, şıklar soru metninin hizasından başlar" acik={ayar.asiliGirinti} degis={(v) => set({ asiliGirinti: v })} />
        <Kaydir ad="Şıklar arası" deger={ayar.sikAralik} min={0} max={8} adim={0.2} birim="pt" degis={(v) => set({ sikAralik: v })} />
        <Kaydir ad="Şık puntosu" deger={ayar.sikOran} min={0.7} max={1.2} adim={0.02} birim="× punto" degis={(v) => set({ sikOran: v })} />
      </Bolum>
      <Bolum baslik="Soru kutusu" alt="Her soru bloğunun çevresi (akış ve ızgarada). Renkleri Renk › Öge renkleri › Çizgiler ve kenarlar altında.">
        <Seg ad="Soru kutusu" kucuk deger={ayar.soruKutu} degis={(soruKutu) => set({ soruKutu })} ogeler={[{ v: 'yok', ad: 'Yok' }, { v: 'cizgi', ad: 'Çerçeve' }, { v: 'zemin', ad: 'Zemin' }, { v: 'golge', ad: 'Kart (gölge)' }]} />
        {ayar.soruKutu !== 'yok' && <Kaydir ad="İç boşluk" deger={ayar.kutuIc} min={0} max={8} adim={0.5} birim="mm" degis={(v) => set({ kutuIc: v })} />}
        <Kaydir ad="Köşe yarıçapı" deger={ayar.kutuYaricap} min={0} max={6} adim={0.2} birim="mm" degis={(v) => set({ kutuYaricap: v })} />
        <p className="v15-cap">Köşe yarıçapı soru kutusu, çözüm kutusu, hücre çerçevesi ve başlık kutusuna uygulanır. Word/PowerPoint'te soru kutusu yaklaşık (zemin/çerçeve) aktarılmaz.</p>
      </Bolum>
    </>
  );

  const ogeSet = (k: RenkOge, v: string | null) => {
    const r = { ...ayar.renkler };
    if (v) r[k] = v; else delete r[k];
    set({ renkler: r, tema: 'ozel' });
  };
  const ozelRenkSayisi = Object.keys(ayar.renkler).length;
  const panelRenk = (
    <>
      <Bolum baslik="Renk teması" alt="Bir tema seçince metin, vurgu ve tüm öge renkleri dolar; sonra her ögeyi aşağıdan tek tek değiştirebilirsin.">
        <div className="sx15-tema" role="radiogroup" aria-label="Renk teması">
          {TEMALAR.map((t) => (
            <button key={t.id} type="button" role="radio" aria-checked={ayar.tema === t.id} className={ayar.tema === t.id ? 'is-on' : ''} title={t.alt} onClick={() => setAyar((a) => (t.id === 'ozel' ? { ...a, tema: 'ozel' } : temaUygula(a, t.id)))}>
              <span className="sx15-tema-sw" style={{ background: t.renkler.sayfaZemin || '#fff' }}>
                <i style={{ background: t.renkler.kok || t.metin }} /><i style={{ background: t.vurgu }} /><i style={{ background: t.renkler.dogru || t.vurgu }} /><i style={{ background: t.renkler.cozumZemin || karisHex(t.vurgu, 0.12, t.renkler.sayfaZemin || '#ffffff') }} />
              </span>
              <b>{t.ad}</b><small>{t.alt}</small>
            </button>
          ))}
        </div>
        <div className="sx15-iki">
          <Renk ad="Metin rengi" deger={ayar.metinRenk} degis={(v) => set({ metinRenk: v, tema: 'ozel' })} />
          <Renk ad="Vurgu rengi" deger={ayar.vurgu} degis={(v) => set({ vurgu: v, tema: 'ozel' })} />
        </div>
      </Bolum>
      <Bolum baslik="Öge renkleri" alt="Her ögenin rengi ayrı ayrı. Boş bırakılan öge vurgu/metin renginden türetilir; × ile türetilmişe dönersin." sag={ozelRenkSayisi > 0 ? <button type="button" className="sx15-lnk" onClick={() => set({ renkler: {}, tema: 'ozel' })}><RotateCcw aria-hidden />Tümünü türet ({ozelRenkSayisi})</button> : undefined}>
        {(Object.keys(RENK_GRUP_AD) as (keyof typeof RENK_GRUP_AD)[]).map((g) => (
          <details key={g} className="sx15-oge-g" open={g === 'metin'}>
            <summary>{RENK_GRUP_AD[g]}<em>{RENK_OGELERI.filter((o) => o.grup === g && ayar.renkler[o.id]).length || ''}</em></summary>
            <div className="sx15-oge">
              {RENK_OGELERI.filter((o) => o.grup === g).map((o) => (
                <Renk key={o.id} ad={o.ad} deger={ogeGoster(ayar, o.id)} degis={(v) => ogeSet(o.id, v)} sifirla={ayar.renkler[o.id] ? () => ogeSet(o.id, null) : undefined} />
              ))}
            </div>
          </details>
        ))}
      </Bolum>
      <Bolum baslik="Renklendirme" alt="Soruları bir özelliğe göre renklendir: aynı ders/konu/yıl aynı rengi alır. Derste her dersin sitedeki sabit rengi kullanılır.">
        <Seg ad="Renk anahtarı" kucuk deger={ayar.renkAlan} degis={(renkAlan) => set({ renkAlan })} ogeler={[{ v: 'yok' as const, ad: 'Yok' }, ...ALANLAR.map((x) => ({ v: x.id as Ayar['renkAlan'], ad: x.ad, title: x.alt }))]} />
        {ayar.renkAlan !== 'yok' && (
          <>
            <Seg ad="Renk biçimi" deger={ayar.renkStil} degis={(renkStil) => set({ renkStil })} ogeler={[{ v: 'serit', ad: 'Şerit' }, { v: 'etiket', ad: 'Etiket' }, { v: 'zemin', ad: 'Zemin' }, { v: 'numara', ad: 'Numara' }]} />
            {ayar.renkAlan === 'ders' && <Anahtar ad="Her dersin kendi rengi" alt="Patoloji pembe, Farmakoloji mor … (sitedeki ders renkleri); kapalıysa palet sırası" acik={ayar.dersRenkleri} degis={(v) => set({ dersRenkleri: v })} />}
            {!(ayar.renkAlan === 'ders' && ayar.dersRenkleri) && (<>
              <div className="sx15-palet" role="radiogroup" aria-label="Palet">
                {(Object.keys(PALETLER) as Ayar['palet'][]).map((p) => (
                  <button key={p} type="button" role="radio" aria-checked={ayar.palet === p} className={ayar.palet === p ? 'is-on' : ''} onClick={() => set({ palet: p })}>
                    <span>{(p === 'ozel' ? (ayar.paletOzel.length ? ayar.paletOzel : ['#e5e7eb', '#d1d5db', '#9ca3af']) : PALETLER[p].renk).slice(0, 6).map((c, i) => <i key={`${c}${i}`} style={{ background: c }} />)}</span>{PALETLER[p].ad}
                  </button>
                ))}
              </div>
              {ayar.palet === 'ozel' && (
                <div className="sx15-palozel">
                  <div className="sx15-coklu-b"><b>Kendi paletim ({ayar.paletOzel.length})</b>{ayar.paletOzel.length > 0 && <button type="button" className="sx15-lnk" onClick={() => set({ paletOzel: [] })}>Temizle</button>}</div>
                  <div className="sx15-palozel-l">
                    {ayar.paletOzel.map((c, i) => (
                      <span key={i} className="sx15-palozel-r">
                        <input type="color" aria-label={`${i + 1}. palet rengi`} value={c} onChange={(e) => set({ paletOzel: ayar.paletOzel.map((x, j) => (j === i ? e.target.value : x)) })} />
                        <button type="button" aria-label="Rengi kaldır" onClick={() => set({ paletOzel: ayar.paletOzel.filter((_, j) => j !== i) })}><X aria-hidden /></button>
                      </span>
                    ))}
                    {ayar.paletOzel.length < 24 && <button type="button" className="sx15-cip is-dev" onClick={() => set({ paletOzel: [...ayar.paletOzel, PALETLER.canli.renk[ayar.paletOzel.length % PALETLER.canli.renk.length]] })}><Plus aria-hidden /><span>Renk ekle</span></button>}
                  </div>
                  <p className="v15-cap">Boş bırakılırsa Canlı palet kullanılır. Renkler sırayla gruplara dağıtılır.</p>
                </div>
              )}
            </>)}
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
        {ayar.gruplar.length > 0 && <Anahtar ad="Grup başlıkları renkli" alt="Ders başlığı dersin rengini, diğer katmanlar renk anahtarını ya da üst katmanı alır" acik={ayar.grupRenkli} degis={(v) => set({ grupRenkli: v })} />}
      </Bolum>
      <Bolum baslik="Etiketler" alt="Her sorunun üstünde ya da altında gösterilecek bilgiler.">
        <div className="sx15-cipler">
          {([['kurul', 'Kurul'], ['ders', 'Ders'], ['konu', 'Konu'], ['yil', 'Yıl'], ['kaynak', 'Kaynak'], ['tur', 'Tür'], ['zorluk', 'Zorluk'], ['etiket', 'Soru etiketleri']] as [keyof Ayar['etiket'], string][]).map(([k, ad]) => (
            <button key={k} type="button" aria-pressed={ayar.etiket[k]} className={`sx15-cip${ayar.etiket[k] ? ' is-on' : ''}`} onClick={() => set({ etiket: { ...ayar.etiket, [k]: !ayar.etiket[k] } })}>{ayar.etiket[k] && <Check aria-hidden />}<span>{ad}</span></button>
          ))}
        </div>
        <Seg ad="Etiket yeri" kucuk deger={ayar.etiketYeri} degis={(etiketYeri) => set({ etiketYeri })} ogeler={[{ v: 'ust', ad: 'Sorunun üstünde' }, { v: 'alt', ad: 'Sorunun altında' }]} />
      </Bolum>
      <Bolum baslik="Etiket görünümü" alt="Boyut, dizilim, şekil ve renk. Renk anahtarının alanı her kipte kendi rengini taşır.">
        <Kaydir ad="Boyut" deger={ayar.etiketBoyut} min={0.5} max={1.1} adim={0.02} birim="× punto" degis={(v) => set({ etiketBoyut: v })} />
        <Seg ad="Dizilim" kucuk deger={ayar.etiketDizilim} degis={(etiketDizilim) => set({ etiketDizilim })} ogeler={[{ v: 'sol', ad: 'Sola' }, { v: 'orta', ad: 'Ortaya' }, { v: 'sag', ad: 'Sağa' }, { v: 'dikey', ad: 'Alt alta' }]} />
        <Seg ad="Şekil" kucuk deger={ayar.etiketSekil} degis={(etiketSekil) => set({ etiketSekil })} ogeler={[{ v: 'hap', ad: 'Hap' }, { v: 'kutu', ad: 'Yuvarlak kutu' }, { v: 'kose', ad: 'Köşeli' }, { v: 'cizgi', ad: 'Çerçeve' }, { v: 'duz', ad: 'Düz metin' }]} />
        <Seg ad="Etiket rengi" kucuk deger={ayar.etiketRenk} degis={(etiketRenk) => set({ etiketRenk })} ogeler={[{ v: 'gri', ad: 'Gri' }, { v: 'alan', ad: 'Türüne göre', title: 'Kurul, ders, konu, yıl … her türün kendi rengi' }, { v: 'ders', ad: 'Dersin rengi', title: 'Sorunun dersinin rengi' }, { v: 'ozel', ad: 'Özel' }]} />
        {ayar.etiketRenk === 'ozel' && (
          <div className="sx15-iki">
            <Renk ad="Etiket zemini" deger={ayar.etiketZemin} degis={(v) => set({ etiketZemin: v })} />
            <Renk ad="Etiket yazısı" deger={ayar.etiketMetin} degis={(v) => set({ etiketMetin: v })} />
          </div>
        )}
        <Anahtar ad="Kalın yazı" acik={ayar.etiketKalin} degis={(v) => set({ etiketKalin: v })} />
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
      {(ayar.cozumYeri === 'altinda') && (
        <Bolum baslik="Çözüm kutusu">
          <Seg ad="Çözüm kutusu biçimi" kucuk deger={ayar.cozumStil} degis={(cozumStil) => set({ cozumStil })} ogeler={[{ v: 'bant', ad: 'Sol bant' }, { v: 'kutu', ad: 'Çerçeve' }, { v: 'zemin', ad: 'Yalnız zemin' }, { v: 'sade', ad: 'Üst çizgi' }]} />
        </Bolum>
      )}
      {ayar.cozumYeri !== 'yok' && ayar.cozumYeri !== 'sayfaAlti' && (
        <Bolum baslik="Çözümde neler olsun">
          <Anahtar ad="Yalnız doğru şıkkı açıkla" alt="Çeldirici çözümlemesi yazılmaz; doğru seçeneğin gerekçesi (yoksa genel açıklama) verilir" acik={ayar.cozumIcerik.yalnizDogru} degis={(v) => set({ cozumIcerik: { ...ayar.cozumIcerik, yalnizDogru: v } })} />
          <div className="sx15-iki">
            <Anahtar ad="Cevap harfi" acik={ayar.cozumIcerik.harf} degis={(v) => set({ cozumIcerik: { ...ayar.cozumIcerik, harf: v } })} />
            <Anahtar ad="Açıklama" acik={ayar.cozumIcerik.aciklama} degis={(v) => set({ cozumIcerik: { ...ayar.cozumIcerik, aciklama: v } })} />
            {!ayar.cozumIcerik.yalnizDogru && <Anahtar ad="Şık şık açıklama" acik={ayar.cozumIcerik.siklar} degis={(v) => set({ cozumIcerik: { ...ayar.cozumIcerik, siklar: v } })} />}
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

  const panelSablon = (
    <>
      <Bolum
        baslik="Şablon kaydet"
        alt="O anki TÜM ayarlar kaydedilir: tasarım, sayfa düzeni, yazı, renkler (her öge ayrı), çözüm, logo ve soru süzgeçleri (kaynaklar, kurul/ders/konu/yıl/tür/zorluk/etiket, soru sayısı). Aynı adla kaydedersen şablon güncellenir."
      >
        <form className="sx15-sablon" onSubmit={(e) => { e.preventDefault(); sablonKaydet(sablonAd); setSablonAd(''); }}>
          <input type="text" value={sablonAd} maxLength={40} placeholder="Şablon adı (ör. Patoloji 40 soru · renkli)" onChange={(e) => setSablonAd(e.target.value)} aria-label="Şablon adı" list="sx15-sablon-adlar" />
          <button type="submit" className="v15-btn is-soft" disabled={!sablonAd.trim()}><Save aria-hidden />{sablon.some((x) => x.ad === sablonAd.trim()) ? 'Güncelle' : 'Kaydet'}</button>
        </form>
        <datalist id="sx15-sablon-adlar">{sablon.map((x) => <option key={x.ad} value={x.ad} />)}</datalist>
        <p className="v15-cap">{eslesenSablon ? `Şu anki ayarlar "${eslesenSablon}" şablonuyla birebir aynı.` : 'Şu anki ayarlar kayıtlı bir şablonla aynı değil.'}</p>
        <div className="sx15-sablon-h">
          <label className="v15-btn is-ghost sx15-sablon-sec"><input type="file" accept="application/json,.json" onChange={(e) => { void sablonIceAktar(e.target.files?.[0]); e.target.value = ''; }} />İçe aktar (JSON)</label>
          <button type="button" className="v15-btn is-ghost" disabled={!sablon.length} onClick={() => sablonDisaAktar(sablon)}><FileDown aria-hidden />Tümünü dışa aktar</button>
          <button type="button" className="v15-btn is-ghost" onClick={() => setAyar({ ...VARSAYILAN, bicim: ayar.bicim })}><RotateCcw aria-hidden />Varsayılana dön</button>
        </div>
      </Bolum>
      <Bolum baslik={`Şablonlarım (${sablon.length})`} alt="Dokununca belge ayarları ve soru süzgeçleri birlikte geri gelir. Şablonlar bu cihazda saklanır; JSON ile başka cihaza taşınır.">
        {sablon.length === 0
          ? <p className="sx15-bos">Henüz şablon yok. Yukarıda ad verip kaydet.</p>
          : (
            <ul className="sx15-sl">
              {sablon.map((x) => (
                <li key={x.ad} className={eslesenSablon === x.ad ? 'is-on' : ''}>
                  <button type="button" className="sx15-sl-a" onClick={() => sablonYukle(x)}>
                    <b>{x.ad}{eslesenSablon === x.ad && <span className="sx15-sl-rozet">şu an</span>}</b>
                    <small>{sablonOzet(x)}</small>
                  </button>
                  <button type="button" className="v15-ib" title="Şu anki ayarlarla güncelle" aria-label={`${x.ad} şablonunu şu anki ayarlarla güncelle`} onClick={() => { setSablon((l) => l.map((y) => (y.ad === x.ad ? { ...y, tarih: Date.now(), ...sablonAnlik } : y))); toast.success('Şablon güncellendi', x.ad); }}><RotateCcw aria-hidden /></button>
                  <button type="button" className="v15-ib" title="JSON olarak indir" aria-label={`${x.ad} şablonunu indir`} onClick={() => sablonDisaAktar([x], x.ad)}><FileDown aria-hidden /></button>
                  <button type="button" className="v15-ib" aria-label={`${x.ad} şablonunu sil`} onClick={() => sablonSil(x.ad)}><Trash2 aria-hidden /></button>
                </li>
              ))}
            </ul>
          )}
      </Bolum>
    </>
  );

  const PANEL: Record<Sekme, React.ReactNode> = { sorular: panelSorular, tasarim: panelTasarim, sayfa: panelSayfa, metin: panelMetin, renk: panelRenk, cozum: panelCozum, sablon: panelSablon };

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
            <Seg ad="Yakınlık" kucuk deger={zum} degis={setZum} ogeler={[{ v: 'sigdir', ad: 'Sığdır' }, { v: 0.5, ad: '%50' }, { v: 0.75, ad: '%75' }, { v: 1, ad: '%100' }, { v: 1.5, ad: '%150' }]} />
          </div>
          {oniz && oniz.tasan > 0 && <p className="sx15-uyari">{oniz.tasan} soru hücresine en küçük ölçekte de sığmadı ve kırpıldı; sayfa başına daha az soru seç ya da puntoyu küçült.</p>}
          {oniz && ayar.sigdir !== 'yok' && (
            <p className="v15-cap">
              Sayfaya sığdır: yazı ölçeği %{Math.round(oniz.olcek * 100)} ({(ayar.punto * oniz.olcek).toFixed(1)} pt).
              {oniz.tahmini ? ' Önizleme ilk sorulara göre; indirilen belgede tüm sorulara göre yeniden hesaplanır.' : ''}
            </p>
          )}
          {oniz?.not && <p className="sx15-uyari">{oniz.not}</p>}
          {ayar.bicim === 'pptx' && <p className="v15-cap">Her sayfa bir slayt olur; cevap kâğıdı slaytta da daireler hâlinde çizilir.</p>}
          {ayar.cikti !== 'hepsi' && <p className="v15-cap">Çıktı: {ayar.cikti === 'sorular' ? 'yalnız soru sayfaları (öğrenci kopyası)' : 'yalnız çözüm ve cevap anahtarı (öğretmen kopyası)'}.</p>}
          {ayar.bicim === 'docx' && ayar.duzen === 'akis' && ayar.cozumYeri !== 'arkada' && ayar.cozumYeri !== 'sayfaAlti' && <p className="v15-cap">Word'de akış düzeni düzenlenebilir metin olarak gelir; sayfa sonları Word'ün yazı tipine göre birkaç satır kayabilir.</p>}
        </div>
        <Onizleme oniz={oniz} ayar={ayar} yukleniyor={onizYuk} zum={zum} />
        <div className="sx15-eylem">
          {indirDugme}
          <button type="button" className="v15-btn is-ghost" disabled={!hs.length || !!uretim} onClick={() => void indir(true)}><Printer aria-hidden />Yazdır</button>
        </div>
      </div>

      <div className="sx15-alt" role="region" aria-label="İndirme ve yazdırma">
        <span>{uretim || ozet}</span>
        <button type="button" className="v15-btn is-ghost sx15-alt-yazdir" disabled={!hs.length || !!uretim} onClick={() => void indir(true)}><Printer aria-hidden /><span>Yazdır</span></button>
        {indirDugme}
      </div>
      {uretim && <div className="sx15-perde" role="status"><Loader2 className="sx15-don" aria-hidden /><span>{uretim}</span></div>}
    </div>
  );
}
