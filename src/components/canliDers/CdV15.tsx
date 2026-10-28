/**
 * v15 sesli ders denetimleri (tasarım sistemi v15 › S2 · Sesli ders v2). Eski ekranda başlıkta, PDF çubuğunda ve ⋯
 * menüsünde dağınık duran düğmeler her birinin tek evi olacak biçimde toplanır:
 *  - Üst bar: geri, başlık, görünüm, ⓘ Terimler, Görünüm, ⋯ Ders seçenekleri
 *  - Görünüm çekmecesi: Düzen · PDF katmanları · Okuma
 *  - Ders seçenekleri: Çalışma · Dışa aktar ve çevrimdışı · Ders hakkında · Tercihler (düğmeler CanliDersDers'ten gelir)
 *  - Kalem kutusu: çizim açıkken PDF'in sağında yüzen dikey araçlar
 * Davranışlar değişmez; yalnız yerleşim ve gruplama v15'e göredir. Stiller styles/v15/sesli.css.
 */
import React, { useState } from 'react';
import { ArrowLeftRight, Eraser, Highlighter, Info, Maximize2, Minimize2, MoreHorizontal, PenTool, SlidersHorizontal, Star, BookOpen, Undo2, X } from 'lucide-react';
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
      {p.hizli && (
        <span className="cd15-hizli">
          <span className="cd15-yazi" role="group" aria-label="Yazı boyutu">
            <button type="button" className="v15-ib" onClick={() => p.hizli!.setYazi(p.hizli!.yazi - 2)} disabled={p.hizli.yazi <= p.hizli.yaziEnaz} aria-label="Yazıyı küçült" title="Yazıyı küçült">A−</button>
            <button type="button" className="v15-ib" onClick={() => p.hizli!.setYazi(p.hizli!.yazi + 2)} disabled={p.hizli.yazi >= p.hizli.yaziEncok} aria-label="Yazıyı büyüt" title="Yazıyı büyüt">A+</button>
          </span>
          <button type="button" className="v15-ib" onClick={p.hizli.onYildiz} aria-label={`Yıldızlı paragraflar (${p.hizli.yildiz})`} title={`Yıldızlı paragraflar (${p.hizli.yildiz})`}>
            <Star aria-hidden />{p.hizli.yildiz > 0 && <i className="cd15-rozet">{p.hizli.yildiz}</i>}
          </button>
        </span>
      )}
      {p.terimVar && (
        <button type="button" className={`v15-ib${terim ? ' is-on' : ''}`} aria-pressed={terim} onClick={() => terimYardimciAyarla(!terim)}
          aria-label="Terim yardımcısı" title={terim ? 'Terim yardımcısı açık (kapat)' : 'Terimler: slayttaki terimlerin anlamını göster'}>
          <Info aria-hidden />
        </button>
      )}
      {p.onTamEkran && (
        <button type="button" className="v15-ib cd15-tam" onClick={p.onTamEkran} aria-label="Tam ekran" title="Tam ekran (Esc ile çıkılır)">
          <Maximize2 aria-hidden />
        </button>
      )}
      <button type="button" className="v15-ib" onClick={p.onGorunum} aria-haspopup="dialog" aria-label="Görünüm ayarları" title="Görünüm: düzen, PDF katmanları, okuma">
        <SlidersHorizontal aria-hidden />
      </button>
      <button type="button" className="v15-ib" onClick={p.onMenu} aria-haspopup="dialog" aria-label="Ders seçenekleri" title="Ders seçenekleri">
        <MoreHorizontal aria-hidden />
      </button>
    </header>
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
