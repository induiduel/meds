/**
 * v15 sesli ders denetimleri (tasarım sistemi v15 › S2 · Sesli ders v2). Eski ekranda başlıkta, PDF çubuğunda ve ⋯
 * menüsünde dağınık duran düğmeler her birinin tek evi olacak biçimde toplanır:
 *  - Üst bar: geri, başlık, görünüm, ⓘ Terimler, Görünüm, ⋯ Ders seçenekleri
 *  - Görünüm çekmecesi: Düzen · PDF katmanları · Okuma
 *  - Ders seçenekleri: Çalışma · Dışa aktar ve çevrimdışı · Ders hakkında · Tercihler (düğmeler CanliDersDers'ten gelir)
 *  - Kalem kutusu: çizim açıkken PDF'in sağında yüzen dikey araçlar
 * Davranışlar değişmez; yalnız yerleşim ve gruplama v15'e göredir. Stiller styles/v15/sesli.css.
 */
import React, { useEffect, useRef, useState } from 'react';
import { ArrowLeftRight, Check, Eraser, Highlighter, Info, Maximize2, Minimize2, MoreHorizontal, PenTool, SlidersHorizontal, Star, BookOpen, Undo2, X } from 'lucide-react';
import { Sheet } from '../ui/Sheet';
import { penPalette, setDrawingGlobalState, undoLastDrawing, useCanUndoDrawing, useDrawingGlobalState } from '../learn/SlideDrawingCanvas';
import { useAppearance } from '../../utils/appearance';
import { useAppFullscreen } from '../../utils/fullscreen';
import '../../styles/v15/sesli.css';
import { PDF_GORUNUM, pdfGorunumAyarla, terimYardimciAyarla, usePdfGorunum, useTerimYardimci, type PdfGorunumId } from './CdTerimKatman';

export type CdGorunum = 'metin' | 'ikisi' | 'pdf' | 'altyazi';
export type CdBolmeYon = 'oto' | 'yan-yana' | 'ust-alt';
const GOR_AD: Record<CdGorunum, string> = { metin: 'Metin', ikisi: 'İkisi', pdf: 'Slayt', altyazi: 'Altyazı' };

/** v15'te katman adları: ne yaptığını söyleyen kısa ad (anahtar ve kayıt aynı) */
const KATMAN_AD: Record<PdfGorunumId, [string, string]> = {
  metin: ['Okunan satırı takip et', 'Satır ve kelime PDF üstünde işaretlenir'],
  resim: ['Şekil ve resim işaretçisi', 'Anlatılan parça çevrelenir, gerekirse yakınlaşır'],
  tablo: ['Tablo işaretçisi', 'Okunan tablo satırı boyanır'],
  iliski: ['İlişki okları ve şemalar', 'Kavramlar arası oklar ve paneller çizilir'],
  not: ['Öğrenci ve hoca işaretleri', 'Notlarda önemli işaretli yerler gösterilir'],
  cikmis: ['Çıkmış soru işaretleri', 'Slaytta çip; dokununca soru açılır'],
};
const KATMAN_SIRA: PdfGorunumId[] = ['metin', 'resim', 'tablo', 'iliski', 'not', 'cikmis'];

/* =============================================================================
 * Üst bar
 * ============================================================================= */
export function CdV15Bas(p: {
  geri: React.ReactNode;
  ust: React.ReactNode;
  baslik: string;
  title?: string;
  pdfVar: boolean;
  terimVar: boolean;
  mod: CdGorunum;
  setGorunum: (g: CdGorunum) => void;
  onGorunum: () => void;
  onMenu: () => void;
  onTamEkran?: () => void;
  ek?: React.ReactNode;
  hizli?: {
    yildiz: number; onYildiz: () => void;
    onOgren?: () => void;
    vurguVar: boolean; vurgu: boolean; setVurgu: (v: boolean) => void;
    yazi: number; setYazi: (n: number) => void; yaziEnaz: number; yaziEncok: number;
  };
}) {
  const terim = useTerimYardimci();
  const sirali: CdGorunum[] = ['metin', 'ikisi', 'pdf', 'altyazi'];
  const sonraki = sirali[(sirali.indexOf(p.mod) + 1) % sirali.length];
  return (
    <header className="cd-ders-bas cd15-bas">
      <span className="cd15-geri">{p.geri}</span>
      <div className="cd15-baslik">
        <h1 className="cd15-ad" title={p.title}>{p.baslik}</h1>
        <small className="cd15-ust">{p.ust}</small>
      </div>
      {p.pdfVar && (
        <div className="v15-seg cd15-gor" role="radiogroup" aria-label="Görünüm">
          {sirali.map((g) => (
            <button key={g} type="button" role="radio" aria-checked={p.mod === g} aria-current={p.mod === g ? 'page' : undefined} onClick={() => p.setGorunum(g)}>
              {GOR_AD[g]}
            </button>
          ))}
        </div>
      )}
      {p.pdfVar && (
        <button type="button" className="v15-ib cd15-dongu" onClick={() => p.setGorunum(sonraki)}
          aria-label={`Görünüm: ${GOR_AD[p.mod]}. ${GOR_AD[sonraki]} görünümüne geç`} title={`Görünüm: ${GOR_AD[p.mod]}`}>
          <ArrowLeftRight aria-hidden />
        </button>
      )}
      {p.ek}
      {/* H331: üst barda yalnız sık kullanılanlar (görünüm, tam ekran) + ⋯; yazı boyutu, yıldızlılar, terim yardımcısı, Görünüm
          çekmecesi ve Ders seçenekleri menüde. Terim yardımcısı açıksa barda "etkin" göstergesi kalır (dokununca kapanır). */}
      {p.terimVar && terim && (
        <button type="button" className="v15-ib is-on cd15-etkin" aria-pressed onClick={() => terimYardimciAyarla(false)}
          aria-label="Terim yardımcısı açık, kapat" title="Terim yardımcısı açık (kapat)">
          <Info aria-hidden />
        </button>
      )}
      {p.onTamEkran && (
        <button type="button" className="v15-ib cd15-tam" onClick={p.onTamEkran} aria-label="Tam ekran" title="Tam ekran (Esc ile çıkılır)">
          <Maximize2 aria-hidden />
        </button>
      )}
      <CdTasmaMenu etiket="Daha fazla" className="cd15-ust-tm" ogeler={[
        ...(p.hizli ? [
          { ad: 'Yazıyı büyüt', ikon: <b>A+</b>, ipucu: `${p.hizli.yazi}px`, kalAcik: true, disabled: p.hizli.yazi >= p.hizli.yaziEncok, onSec: () => p.hizli!.setYazi(p.hizli!.yazi + 2) },
          { ad: 'Yazıyı küçült', ikon: <b>A−</b>, kalAcik: true, disabled: p.hizli.yazi <= p.hizli.yaziEnaz, onSec: () => p.hizli!.setYazi(p.hizli!.yazi - 2) },
        ] : []),
        ...(p.terimVar ? [{ ad: 'Terim yardımcısı', ikon: <Info />, secili: terim, onSec: () => terimYardimciAyarla(!terim), ayrac: true }] : []),
        ...(p.hizli ? [{ ad: `Yıldızlı paragraflar (${p.hizli.yildiz})`, ikon: <Star />, onSec: p.hizli.onYildiz, ayrac: !p.terimVar }] : []),
        ...(p.onTamEkran ? [{ ad: 'Tam ekran', ikon: <Maximize2 />, ipucu: 'Esc çıkar', onSec: p.onTamEkran }] : []),
        { ad: 'Görünüm ayarları…', ikon: <SlidersHorizontal />, onSec: p.onGorunum, ayrac: true },
        { ad: 'Tüm ders seçenekleri…', ikon: <MoreHorizontal />, onSec: p.onMenu },
      ]} />
    </header>
  );
}


/* =============================================================================
 * H330: Taşma menüsü (⋯) — seyrek düğmeler tek açılır menüde. Erişilebilir: aria-haspopup="menu", Esc ve dışarı tıklama
 * kapatır, ↑/↓/Home/End öğeler arasında gezer, açılınca ilk öğe odaklanır, kapanınca odak düğmeye döner.
 * Durum taşıyan öğe menuitemcheckbox + ✓ ile gösterilir; kalAcik öğesi (yazı boyutu, yakınlaştırma) menüyü kapatmaz.
 * ============================================================================= */
export interface CdTasmaOge {
  ad: string;
  ikon?: React.ReactNode;
  onSec: () => void;
  ipucu?: string;
  secili?: boolean;
  disabled?: boolean;
  kalAcik?: boolean;
  ayrac?: boolean;
}
export function CdTasmaMenu({ ogeler, etiket, className, ikon }: { ogeler: CdTasmaOge[]; etiket: string; className?: string; ikon?: React.ReactNode }) {
  const [acik, setAcik] = useState(false);
  const kok = useRef<HTMLSpanElement>(null);
  const btn = useRef<HTMLButtonElement>(null);
  const liste = useRef<HTMLDivElement>(null);
  const ogeEl = () => Array.from(liste.current?.querySelectorAll<HTMLButtonElement>('[role^="menuitem"]:not([disabled])') || []);
  const kapat = (odak = true) => { setAcik(false); if (odak) btn.current?.focus(); };
  useEffect(() => {
    if (!acik) return;
    ogeEl()[0]?.focus();
    const dis = (e: PointerEvent) => { if (!kok.current?.contains(e.target as Node)) setAcik(false); };
    // H335: TV kumandasının Geri tuşu (GoBack/BrowserBack, 461, 10009) da menüyü kapatır
    const esc = (e: KeyboardEvent) => { if (e.key === 'Escape' || e.key === 'GoBack' || e.key === 'BrowserBack' || e.keyCode === 461 || e.keyCode === 10009) { e.stopPropagation(); e.preventDefault(); kapat(); } };
    document.addEventListener('pointerdown', dis, true);
    document.addEventListener('keydown', esc, true);
    return () => { document.removeEventListener('pointerdown', dis, true); document.removeEventListener('keydown', esc, true); };
  }, [acik]);
  const tus = (e: React.KeyboardEvent) => {
    const el = ogeEl(); if (!el.length) return;
    const i = el.indexOf(document.activeElement as HTMLButtonElement);
    let j = -1;
    if (e.key === 'ArrowDown') j = (i + 1) % el.length;
    else if (e.key === 'ArrowUp') j = (i - 1 + el.length) % el.length;
    else if (e.key === 'Home') j = 0;
    else if (e.key === 'End') j = el.length - 1;
    else if (e.key === 'Tab') { setAcik(false); return; }
    if (j >= 0) { e.preventDefault(); el[j].focus(); }
  };
  return (
    <span className={`cd15-tm${className ? ` ${className}` : ''}`} ref={kok}>
      <button type="button" ref={btn} className="v15-ib cd15-tm-btn" aria-haspopup="menu" aria-expanded={acik} aria-label={etiket} title={etiket}
        onClick={() => setAcik((a) => !a)}
        onKeyDown={(e) => { if (e.key === 'ArrowDown' && !acik) { e.preventDefault(); setAcik(true); } }}>
        {ikon || <MoreHorizontal aria-hidden />}
      </button>
      {acik && (
        <div className="cd15-tm-liste" role="menu" aria-label={etiket} ref={liste} onKeyDown={tus}>
          {ogeler.map((o, i) => (
            <React.Fragment key={i}>
              {o.ayrac && i > 0 && <div className="cd15-tm-ayrac" role="separator" />}
              <button type="button" role={o.secili === undefined ? 'menuitem' : 'menuitemcheckbox'} aria-checked={o.secili === undefined ? undefined : o.secili}
                className="cd15-tm-oge" disabled={o.disabled}
                onClick={() => { o.onSec(); if (!o.kalAcik) kapat(); }}>
                <span className="cd15-tm-ik" aria-hidden>{o.ikon}</span>
                <span className="cd15-tm-ad">{o.ad}</span>
                {o.ipucu && <kbd className="cd15-tm-kbd">{o.ipucu}</kbd>}
                {o.secili !== undefined && <span className={`cd15-tm-ok${o.secili ? ' is-on' : ''}`} aria-hidden>{o.secili ? <Check /> : null}</span>}
              </button>
            </React.Fragment>
          ))}
        </div>
      )}
    </span>
  );
}

/* =============================================================================
 * Görünüm çekmecesi
 * ============================================================================= */
type Sekme = 'duzen' | 'pdf' | 'okuma';

/* Okuma tercihleri (tasarım S08): satır aralığı, yazı tipi, zemin, etkin cümleyi ortala. Cihazda saklanır, kök öğeye
   data-cd-* olarak yazılır (styles/v15/sesli.css); ortalama CanliDersDers kaydırmasında okunur (data-cd-ortala). */
export interface CdOkuma { satir: 'siki' | 'normal' | 'genis'; font: 'okuma' | 'sade' | 'kolay'; zemin: 'varsayilan' | 'krem' | 'gri' | 'gece'; ortala: boolean }
const OKUMA_KEY = 'medsoru_cd_okuma_v1';
const OKUMA_VARS: CdOkuma = { satir: 'normal', font: 'okuma', zemin: 'varsayilan', ortala: false };
const okumaOku = (): CdOkuma => { try { return { ...OKUMA_VARS, ...JSON.parse(localStorage.getItem(OKUMA_KEY) || '{}') }; } catch { return OKUMA_VARS; } };
function okumaUygula(o: CdOkuma) {
  const d = document.documentElement.dataset;
  d.cdSatir = o.satir; d.cdFont = o.font; d.cdZemin = o.zemin;
  if (o.ortala) d.cdOrtala = 'on'; else delete d.cdOrtala;
  if (o.font === 'kolay' && !document.getElementById('cd15-font-kolay')) {
    const l = document.createElement('link');
    l.id = 'cd15-font-kolay'; l.rel = 'stylesheet';
    l.href = 'https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&display=swap';
    document.head.appendChild(l);
  }
}
if (typeof document !== 'undefined') okumaUygula(okumaOku());
export function useOkuma(): [CdOkuma, (y: Partial<CdOkuma>) => void] {
  const [o, setO] = useState(okumaOku);
  return [o, (y) => setO((x) => { const n = { ...x, ...y }; try { localStorage.setItem(OKUMA_KEY, JSON.stringify(n)); } catch { /* yok */ } okumaUygula(n); return n; })];
}
function Anahtar({ ad, acik, deger, set }: { ad: string; acik?: string; deger: boolean; set: (v: boolean) => void }) {
  return (
    <label className="cd15-sat">
      <span className="cd15-sat-t"><b>{ad}</b>{acik && <small>{acik}</small>}</span>
      <input type="checkbox" role="switch" className="cd15-sw" checked={deger} onChange={(e) => set(e.target.checked)} />
    </label>
  );
}
function Secici<T extends string>({ ad, secenek, deger, set }: { ad: string; secenek: [T, string][]; deger: T; set: (v: T) => void }) {
  return (
    <div className="cd15-sat">
      <span className="cd15-sat-t"><b>{ad}</b></span>
      <div className="v15-seg" role="radiogroup" aria-label={ad}>
        {secenek.map(([v, t]) => (
          <button key={v} type="button" role="radio" aria-checked={deger === v} aria-current={deger === v ? 'page' : undefined} onClick={() => set(v)}>{t}</button>
        ))}
      </div>
    </div>
  );
}

export function CdV15Gorunum(p: {
  acik: boolean;
  onKapat: () => void;
  pdfVar: boolean;
  terimVar: boolean;
  mod: CdGorunum;
  setGorunum: (g: CdGorunum) => void;
  yon: CdBolmeYon;
  setYon: (y: CdBolmeYon) => void;
  oran: number;
  setOran: (n: number) => void;
  ters: boolean;
  setTers: (f: (t: boolean) => boolean) => void;
  onTamEkran: () => void;
  vurguVar: boolean;
  vurgu: boolean;
  setVurgu: (v: boolean) => void;
  yazi: number;
  setYazi: (n: number) => void;
  yaziEnaz: number;
  yaziEncok: number;
}) {
  const [sekme, setSekme] = useState<Sekme>(p.pdfVar ? 'pdf' : 'okuma');
  const [okuma, setOkuma] = useOkuma();
  const g = usePdfGorunum();
  const terim = useTerimYardimci();
  const [appFs, toggleAppFs] = useAppFullscreen();
  const katmanlar = KATMAN_SIRA.filter((id) => PDF_GORUNUM.some((x) => x.id === id));
  const acikN = katmanlar.filter((id) => g[id]).length + (p.terimVar && terim ? 1 : 0);
  const topN = katmanlar.length + (p.terimVar ? 1 : 0);
  const sekmeler: [Sekme, string][] = p.pdfVar ? [['duzen', 'Düzen'], ['pdf', 'PDF katmanları'], ['okuma', 'Okuma']] : [['okuma', 'Okuma']];
  return (
    <Sheet open={p.acik} onClose={p.onKapat} title="Görünüm" width={420} className="cd15-sheet">
      <div className="cd15-cek">
        {sekmeler.length > 1 && (
          <div className="v15-seg" role="tablist" aria-label="Görünüm bölümleri">
            {sekmeler.map(([id, t]) => (
              <button key={id} type="button" role="tab" aria-selected={sekme === id} aria-current={sekme === id ? 'page' : undefined} onClick={() => setSekme(id)}>{t}</button>
            ))}
          </div>
        )}

        {sekme === 'duzen' && (
          <div className="cd15-grup">
            <Secici ad="Görünüm" deger={p.mod} set={p.setGorunum} secenek={[['metin', 'Metin'], ['ikisi', 'İkisi'], ['pdf', 'Slayt']]} />
            {p.mod === 'ikisi' && (
              <>
                <Secici ad="Bölme yönü" deger={p.yon} set={p.setYon} secenek={[['oto', 'Oto'], ['yan-yana', 'Yan yana'], ['ust-alt', 'Üst-alt']]} />
                <Secici
                  ad="Oran"
                  deger={p.oran <= 42 ? '35' : p.oran >= 58 ? '65' : '50'}
                  set={(v) => p.setOran(Number(v))}
                  secenek={[['35', 'Metin+'], ['50', '50:50'], ['65', 'PDF+']]}
                />
                <button type="button" className="cd15-sat is-btn" onClick={() => p.setTers((t) => !t)}>
                  <span className="cd15-sat-t"><b>Bölmelerin yeri</b><small>{p.ters ? 'Şu an metin önce, PDF sonra' : 'Şu an PDF önce, metin sonra'}</small></span>
                  <ArrowLeftRight aria-hidden />
                </button>
              </>
            )}
            <button type="button" className="cd15-sat is-btn" onClick={() => { p.onKapat(); p.onTamEkran(); }}>
              <span className="cd15-sat-t"><b>Tam ekran</b><small>Menüler gizlenir; Esc ile çıkılır</small></span>
              <Maximize2 aria-hidden />
            </button>
          </div>
        )}

        {sekme === 'pdf' && (
          <div className="cd15-grup">
            {katmanlar.map((id) => (
              <Anahtar key={id} ad={KATMAN_AD[id][0]} acik={KATMAN_AD[id][1]} deger={g[id]} set={(v) => pdfGorunumAyarla(id, v)} />
            ))}
            {p.terimVar && <Anahtar ad="Terim ve kısaltmalar" acik="Dokununca 1–2 cümlelik anlam açılır" deger={terim} set={terimYardimciAyarla} />}
            <div className="cd15-alt">
              <span>{topN} katmandan {acikN}’{acikN === topN ? 'i' : 'si'} açık</span>
              <button type="button" className="v15-btn is-ghost cd15-kucuk" onClick={() => katmanlar.forEach((id) => pdfGorunumAyarla(id, true))}>Varsayılana dön</button>
            </div>
          </div>
        )}

        {sekme === 'okuma' && (
          <div className="cd15-grup">
            <div className="cd15-sat">
              <span className="cd15-sat-t"><b>Yazı boyutu</b><small>{p.yazi - 2} px</small></span>
              <span className="cd15-adim" role="group" aria-label="Yazı boyutu">
                <button type="button" onClick={() => p.setYazi(p.yazi - 2)} disabled={p.yazi <= p.yaziEnaz} aria-label="Yazıyı küçült">A−</button>
                <button type="button" onClick={() => p.setYazi(20)} aria-label="Varsayılan boyut">Varsayılan</button>
                <button type="button" onClick={() => p.setYazi(p.yazi + 2)} disabled={p.yazi >= p.yaziEncok} aria-label="Yazıyı büyüt">A+</button>
              </span>
            </div>
            <Secici ad="Satır aralığı" deger={okuma.satir} set={(v) => setOkuma({ satir: v })} secenek={[['siki', 'Sıkı'], ['normal', 'Normal'], ['genis', 'Geniş']]} />
            <Secici ad="Yazı tipi" deger={okuma.font} set={(v) => setOkuma({ font: v })} secenek={[['okuma', 'Okuma'], ['sade', 'Sade'], ['kolay', 'Kolay okunur']]} />
            <Secici ad="Zemin" deger={okuma.zemin} set={(v) => setOkuma({ zemin: v })} secenek={[['varsayilan', 'Tema'], ['krem', 'Krem'], ['gri', 'Gri'], ['gece', 'Gece']]} />
            <Anahtar ad="Okunan cümleyi ortada tut" acik="Metin her cümlede ekranın ortasına kayar" deger={okuma.ortala} set={(v) => setOkuma({ ortala: v })} />
            {p.vurguVar && (
              <Anahtar ad="Önemli yerleri vurgula" acik="Çıkmışta, örnek sorularda ve spotlarda geçen cümleler işaretlenir" deger={p.vurgu} set={p.setVurgu} />
            )}
          </div>
        )}
      </div>
    </Sheet>
  );
}

/* =============================================================================
 * Ders seçenekleri (gruplu)
 * ============================================================================= */
export function CdV15Menu({ acik, onKapat, gruplar }: { acik: boolean; onKapat: () => void; gruplar: { ad: string; ogeler: React.ReactNode }[] }) {
  return (
    <Sheet open={acik} onClose={onKapat} title="Ders seçenekleri" width={420} className="cd15-sheet">
      <div className="cd15-menu">
        {gruplar.map((g) => (
          <section key={g.ad} className="cd15-mgrup" aria-label={g.ad}>
            <h3>{g.ad}</h3>
            <div className="cd15-mliste">{g.ogeler}</div>
          </section>
        ))}
      </div>
    </Sheet>
  );
}

/* =============================================================================
 * Kalem: PDF çubuğunda tek düğme; açıkken PDF'in sağında yüzen dikey araç kutusu
 * ============================================================================= */
export function CdV15KalemDugme() {
  const st = useDrawingGlobalState();
  const acik = st.activeMode !== 'none';
  return (
    <button type="button" className={`cd15-pb${acik ? ' is-on' : ''}`} aria-pressed={acik} onClick={() => setDrawingGlobalState({ activeMode: acik ? 'none' : 'pen' })}
      title={acik ? 'Kalemi kapat' : "PDF'e yaz ve çiz"}>
      <PenTool aria-hidden /> <span className="cd15-pb-l">Kalem</span>
    </button>
  );
}

export function CdV15KalemKutusu() {
  const st = useDrawingGlobalState();
  const { mode } = useAppearance();
  const geri = useCanUndoDrawing();
  const [renkAcik, setRenkAcik] = useState(false);
  if (st.activeMode === 'none') return null;
  const palet = penPalette(mode);
  const arac = (m: 'pen' | 'highlighter' | 'eraser', I: React.ElementType, ad: string) => (
    <button type="button" className={`cd15-kk-b${st.activeMode === m ? ' is-on' : ''}`} aria-pressed={st.activeMode === m} aria-label={ad} title={ad}
      onClick={() => setDrawingGlobalState({ activeMode: m })}>
      <I aria-hidden />
    </button>
  );
  return (
    <div className="cd15-kk" role="toolbar" aria-label="Çizim araçları" onPointerDown={(e) => e.stopPropagation()}>
      {arac('pen', PenTool, 'Kalem')}
      {arac('highlighter', Highlighter, 'Fosforlu kalem')}
      {arac('eraser', Eraser, 'Silgi')}
      <span className="cd15-kk-ayr" />
      <button type="button" className="cd15-kk-b" onClick={undoLastDrawing} disabled={!geri} aria-label="Son çizimi geri al" title="Son çizimi geri al"><Undo2 aria-hidden /></button>
      <button type="button" className="cd15-kk-renk" style={{ background: st.color }} aria-expanded={renkAcik} aria-label="Renk seç" title="Renk" onClick={() => setRenkAcik((x) => !x)} />
      <button type="button" className="cd15-kk-b" onClick={() => setDrawingGlobalState({ activeMode: 'none' })} aria-label="Kalemi kapat" title="Kapat"><X aria-hidden /></button>
      {renkAcik && (
        <div className="cd15-kk-palet" role="radiogroup" aria-label="Renk">
          {palet.map((c) => {
            // Etiket "Kırmızı (Önemli)" biçiminde: renk adı + anlamı ayrı satırda
            const m = /^(.*?)\s*\((.*)\)$/.exec(c.label);
            return (
              <button key={c.id} type="button" role="radio" aria-checked={st.color === c.hex} className={st.color === c.hex ? 'is-on' : ''}
                onClick={() => { setDrawingGlobalState({ color: c.hex, activeMode: st.activeMode === 'eraser' ? 'pen' : st.activeMode }); setRenkAcik(false); }}>
                <i style={{ background: c.hex }} />
                <span>{m ? m[1] : c.label}{m && <small>{m[2]}</small>}</span>
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
}
