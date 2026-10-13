/**
 * PDF Stüdyosu belge motoru. İçerik, uygulamanın kendi bileşen sınıflarıyla (cx-*, ls-*, ms-*) çizilir ve
 * çalışan sayfanın derlenmiş CSS'i belgeye gömülür; böylece PDF ekrandaki tasarımın birebir kopyası olur.
 *
 * Çıktı yolları:
 *  1. Sunucu (`/api/pdf/render`): başsız Chrome gerçek PDF dosyası üretir (sayfa numarası, gömülü yazı tipi).
 *  2. Tarayıcı yazdırma: sunucuya ulaşılamazsa aynı belge gizli bir çerçevede "PDF olarak kaydet"e açılır.
 *
 * Sayfa boyutu ve yönü `@page { size: <en>mm <boy>mm }` ile verilir (sunucu `preferCSSPageSize` kullanır).
 * Belge içi bağlantılar düz `<a href="#kimlik">` işaretlemesidir: Chrome iki yolda da bunları PDF'te iç
 * bağlantıya (GoTo hedefi) çevirir; soru ↔ cevap ve içindekiler → bölüm atlamaları böyle çalışır.
 */
import React from 'react';
import { createRoot } from 'react-dom/client';
import { flushSync } from 'react-dom';
import { getCustomApiUrl } from '../../services/api';

export type PaperSize = 'a3' | 'a4' | 'a5' | 'b4' | 'b5' | 'letter' | 'legal' | 'tablet';
export type Orientation = 'portrait' | 'landscape';
export type MarginPreset = 'narrow' | 'normal' | 'wide';
export type FontScale = 'xs' | 'sm' | 'md' | 'lg' | 'xl';
export type TemplateId = 'modern' | 'sade' | 'klasik' | 'kompakt' | 'sinav';
export type InkMode = 'color' | 'mono';
/** Sığdırma: kapalı, içerik sayfa genişliğine (tablo/görsel taşmaz), belirli sayfa sayısına (yazı küçülür) */
export type FitMode = 'off' | 'width' | 'pages';

export interface PageSettings {
  paper: PaperSize;
  orientation: Orientation;
  margins: MarginPreset;
  fontScale: FontScale;
  template: TemplateId;
  ink: InkMode;
  fit: FitMode;
  /** fit = 'pages' iken hedef en çok sayfa */
  fitPages: number;
  /** Sayfa altında "3 / 12" numarası */
  pageNumbers: boolean;
  /** Sayfa üstünde belge adı */
  runningHeader: boolean;
}

export interface DocumentOptions extends PageSettings {
  title: string;
  /** Sayfa üst bilgisi (sol); boşsa başlık kullanılır */
  runningHead?: string;
  /** Sayfaya sığdırma ölçümünün bulduğu yakınlaştırma (yoksa yazı boyutu kullanılır) */
  fitZoom?: number;
}

export const DEFAULT_PAGE: PageSettings = {
  paper: 'a4', orientation: 'portrait', margins: 'normal', fontScale: 'md', template: 'modern', ink: 'color',
  fit: 'off', fitPages: 10, pageNumbers: true, runningHeader: true,
};

/** Kâğıt boyutları (mm, dikey) */
export const PAPER: Record<PaperSize, { label: string; hint: string; w: number; h: number }> = {
  a4: { label: 'A4', hint: '210 × 297 mm · standart', w: 210, h: 297 },
  a5: { label: 'A5', hint: '148 × 210 mm · cep kitabı', w: 148, h: 210 },
  a3: { label: 'A3', hint: '297 × 420 mm · poster, geniş tablo', w: 297, h: 420 },
  b5: { label: 'B5', hint: '176 × 250 mm · defter boyu', w: 176, h: 250 },
  b4: { label: 'B4', hint: '250 × 353 mm', w: 250, h: 353 },
  letter: { label: 'Letter', hint: '8,5 × 11 inç · ABD', w: 215.9, h: 279.4 },
  legal: { label: 'Legal', hint: '8,5 × 14 inç · uzun', w: 215.9, h: 355.6 },
  tablet: { label: 'Tablet', hint: '3:4 ekranı doldurur', w: 210, h: 280 },
};
export const PAPER_ORDER: PaperSize[] = ['a4', 'a5', 'a3', 'b5', 'b4', 'letter', 'legal', 'tablet'];

/** Kenar boşlukları (mm): üst, sağ, alt, sol */
export const MARGINS: Record<MarginPreset, { label: string; mm: [number, number, number, number] }> = {
  narrow: { label: 'Dar', mm: [10, 8, 11, 8] },
  normal: { label: 'Normal', mm: [15, 13, 15, 13] },
  wide: { label: 'Geniş', mm: [22, 20, 22, 20] },
};

export const ZOOM: Record<FontScale, number> = { xs: 0.76, sm: 0.84, md: 0.92, lg: 1.04, xl: 1.16 };

export const TEMPLATES: Record<TemplateId, { label: string; hint: string }> = {
  modern: { label: 'Uygulama', hint: 'Ekrandaki kart tasarımı' },
  sade: { label: 'Sade', hint: 'Çerçevesiz, ince çizgiler' },
  klasik: { label: 'Klasik', hint: 'Tırnaklı yazı, kitap düzeni' },
  kompakt: { label: 'Kompakt', hint: 'Sıkı aralık, çok soru' },
  sinav: { label: 'Sınav kitapçığı', hint: 'Siyah-beyaz, A) B) şıklar' },
};

/** Eski kayıtlı ayarları (format: 'a4-landscape' …) yeni modele çevirir; bozuk değerleri düzeltir. */
export function normalizePage(raw: any): PageSettings {
  const o: any = { ...DEFAULT_PAGE, ...(raw && typeof raw === 'object' ? raw : {}) };
  if (raw?.format && !raw?.paper) {
    o.paper = raw.format === 'tablet' ? 'tablet' : raw.format === 'letter' ? 'letter' : 'a4';
    o.orientation = raw.format === 'a4-landscape' ? 'landscape' : 'portrait';
    if (raw.format === 'tablet') o.margins = 'narrow';
  }
  delete o.format;
  if (!PAPER[o.paper as PaperSize]) o.paper = 'a4';
  if (o.orientation !== 'landscape') o.orientation = 'portrait';
  if (!MARGINS[o.margins as MarginPreset]) o.margins = 'normal';
  if (!ZOOM[o.fontScale as FontScale]) o.fontScale = 'md';
  if (!TEMPLATES[o.template as TemplateId]) o.template = 'modern';
  if (o.ink !== 'mono') o.ink = 'color';
  if (!['off', 'width', 'pages'].includes(o.fit)) o.fit = 'off';
  o.fitPages = Math.max(1, Math.min(500, Math.round(Number(o.fitPages) || 10)));
  return o as PageSettings;
}

/** Yönü uygulanmış sayfa ölçüsü ve kenar boşlukları (mm). */
export function pageGeometry(o: Pick<PageSettings, 'paper' | 'orientation' | 'margins'>) {
  const p = PAPER[o.paper] || PAPER.a4;
  const land = o.orientation === 'landscape';
  const [t, r, b, l] = (MARGINS[o.margins] || MARGINS.normal).mm;
  return { w: land ? p.h : p.w, h: land ? p.w : p.h, m: { t, r, b, l } };
}

export const pageLabel = (o: Pick<PageSettings, 'paper' | 'orientation'>) => `${PAPER[o.paper]?.label || 'A4'} ${o.orientation === 'landscape' ? 'yatay' : 'dikey'}`;

/** React ağacını statik HTML'e çevirir (etkileşim yok; PDF'e girecek işaretleme). */
export function renderMarkup(node: React.ReactNode): string {
  const host = document.createElement('div');
  const root = createRoot(host);
  flushSync(() => root.render(node));
  const html = host.innerHTML;
  root.unmount();
  return html;
}

/* ---------------------------------------------------------------------------
 * Uygulama CSS'i: yazdırma kuralları atılır (uygulamanın @media print'i header/aside/button gizler,
 * PDF'te ekrandaki görünüm istenir). Çapraz kökenli sayfalar (Google Fonts) bağlantı olarak kalır.
 * ------------------------------------------------------------------------- */
let cssCache: { css: string; links: string[] } | null = null;

const ruleText = (rule: CSSRule): string => {
  if (typeof CSSMediaRule !== 'undefined' && rule instanceof CSSMediaRule) {
    const media = rule.media.mediaText.toLowerCase();
    if (/\bprint\b/.test(media) && !/\bscreen\b/.test(media)) return '';
    const inner = Array.from(rule.cssRules).map(ruleText).join('\n');
    return inner ? `@media ${rule.media.mediaText} {\n${inner}\n}` : '';
  }
  return rule.cssText;
};

export function collectAppCss(): { css: string; links: string[] } {
  if (cssCache) return cssCache;
  const parts: string[] = [];
  const links: string[] = [];
  for (const sheet of Array.from(document.styleSheets)) {
    const owner = sheet.ownerNode as HTMLElement | null;
    if (owner?.dataset?.pdfIgnore != null) continue;
    try {
      parts.push(Array.from(sheet.cssRules).map(ruleText).join('\n'));
    } catch {
      if (sheet.href) links.push(sheet.href);
    }
  }
  // Uygulamanın yazı tipleri (index.html) her durumda bağlanır
  document.querySelectorAll<HTMLLinkElement>('link[rel="stylesheet"][href*="fonts.googleapis.com"]').forEach((l) => {
    if (!links.includes(l.href)) links.push(l.href);
  });
  cssCache = { css: parts.join('\n'), links };
  return cssCache;
}

const escAttr = (s: string) => s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c] as string);
const cssString = (s: string) => `"${s.replace(/\\/g, '\\\\').replace(/"/g, '\\"').replace(/\n/g, ' ')}"`;

/** PDF'e özgü düzen: sayfa, kenar bilgileri, animasyonsuz ve kırılmayan kartlar. */
const pdfCss = (o: DocumentOptions) => {
  const g = pageGeometry(o);
  const zoom = o.fitZoom || ZOOM[o.fontScale] || ZOOM.md;
  const head = o.runningHead || o.title;
  const mono = o.ink === 'mono';
  const accent = mono ? '#1F2430' : '#2453E6';
  const mm = (n: number) => `${n}mm`;
  return `
@page {
  size: ${g.w}mm ${g.h}mm;
  margin: ${mm(g.m.t)} ${mm(g.m.r)} ${mm(g.m.b)} ${mm(g.m.l)};
  ${o.pageNumbers ? `@bottom-right { content: counter(page) " / " counter(pages); font: 600 8pt "Geist", system-ui, sans-serif; color: #8A94A6; }` : ''}
  ${o.runningHeader ? `@top-left { content: ${cssString(head)}; font: 600 7.5pt "Geist", system-ui, sans-serif; color: #8A94A6; letter-spacing: .02em; }
  @top-right { content: "MedSoru"; font: 700 7.5pt "Bricolage Grotesque", "Geist", sans-serif; color: ${accent}; }` : ''}
}
@page cover { margin: 0; @bottom-right { content: none; } @top-left { content: none; } @top-right { content: none; } }
*, *::before, *::after { animation: none !important; transition: none !important; }
html, body { margin: 0 !important; padding: 0 !important; background: #fff !important; height: auto !important; overflow: visible !important; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; scroll-behavior: auto !important; }
body { font-family: var(--font-sans, "Geist", system-ui, sans-serif); color: var(--color-ink); --ls-mark: #FFF1B8; --ls-mark-ink: #4A3800; }
.pd-zoom { zoom: ${zoom.toFixed(3)}; }
.pd-cover { min-height: ${Math.floor((g.h - 1) / zoom)}mm; }
${o.fit !== 'off' ? `.pd-zoom img, .pd-zoom svg, .pd-zoom video { max-width: 100% !important; height: auto; }
.pd-zoom table { max-width: 100% !important; table-layout: fixed; }
.pd-zoom td, .pd-zoom th { overflow-wrap: anywhere; word-break: break-word; }
.pd-zoom pre, .pd-zoom code { white-space: pre-wrap; overflow-wrap: anywhere; }
.pd-zoom .ls-table, .pd-zoom .ls-table-wrap, .pd-zoom [class*="scroll"] { overflow: visible !important; max-width: 100% !important; }` : ''}
@media screen {
  html { background: #E9EDF4 !important; }
  body { padding: 24px 0 48px !important; background: #E9EDF4 !important; }
  .pd-doc { width: ${g.w}mm; min-height: ${g.h}mm; margin: 0 auto; background: #fff; padding: ${mm(g.m.t)} ${mm(g.m.r)} ${mm(g.m.b)} ${mm(g.m.l)}; box-sizing: border-box; border-radius: 4px; box-shadow: 0 1px 2px rgb(14 23 38 / .06), 0 8px 28px rgb(14 23 38 / .08); }
  .pd-cover { min-height: ${Math.floor((g.h - g.m.t - g.m.b - 2) / zoom)}mm; margin-bottom: 15mm; }
  .pd-page-break { height: 0; margin: 26px 0; border-top: 2px dashed #D5DBE6; }
}
@media print {
  .pd-page-break { break-after: page; height: 0; }
  .pd-cover { page: cover; break-after: page; }
}
`;
};

export function buildDocument(bodyHtml: string, o: DocumentOptions): string {
  const { css, links } = collectAppCss();
  const rootClass = Array.from(document.documentElement.classList).filter((c) => c !== 'theme-dark' && c !== 'dark').join(' ');
  return `<!DOCTYPE html>
<html lang="tr" class="${escAttr(rootClass)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${escAttr(o.title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
${links.map((h) => `<link rel="stylesheet" href="${escAttr(h)}">`).join('\n')}
<style>${css}</style>
<style>${pdfCss(o)}</style>
</head>
<body class="ps-tpl-${o.template} ps-ink-${o.ink}">
<main class="pd-doc"><div class="pd-zoom">${bodyHtml}</div></main>
</body>
</html>`;
}

/* ---------------------------------------------------------------------------
 * Sayfaya sığdırma: belge gizli bir çerçevede sayfa genişliğinde dizilir, zorunlu sayfa sonlarıyla
 * bölünen parçaların yüksekliğinden sayfa sayısı tahmin edilir; hedefe inene dek yazı küçültülür.
 * ------------------------------------------------------------------------- */
const BREAK_SELECTORS = '.pd-section, .pd-group, .pd-step.is-page, .pd-sec-title, .pd-sum, .pd-qlist.is-page > .cx-q, .pd-sol.is-page, .pd-page-break';
const PX_PER_MM = 96 / 25.4;
/** Kırılmayan blokların sayfa sonunda bıraktığı boşluk payı */
const FILL_RATIO = 0.94;

const loadHiddenFrame = (html: string, widthPx: number): Promise<HTMLIFrameElement> =>
  new Promise((resolve) => {
    const frame = document.createElement('iframe');
    frame.setAttribute('aria-hidden', 'true');
    frame.tabIndex = -1;
    frame.style.cssText = `position:fixed;left:-20000px;top:0;width:${Math.ceil(widthPx)}px;height:800px;border:0;visibility:hidden;pointer-events:none`;
    document.body.appendChild(frame);
    const doc = frame.contentDocument!;
    doc.open();
    doc.write(html);
    doc.close();
    const done = async () => {
      try {
        await (frame.contentDocument as any)?.fonts?.ready;
      } catch {}
      resolve(frame);
    };
    if (doc.readyState === 'complete') setTimeout(done, 120);
    else frame.addEventListener('load', () => setTimeout(done, 120), { once: true });
  });

/** Dizilmiş belgede tahmini sayfa sayısı. */
function countPages(doc: Document, pageContentPx: number): number {
  const host = doc.querySelector<HTMLElement>('.pd-zoom');
  if (!host) return 1;
  const top = host.getBoundingClientRect().top;
  const bottom = host.getBoundingClientRect().bottom;
  const cuts: number[] = [];
  const cover = doc.querySelector<HTMLElement>('.pd-cover');
  let pages = 0;
  let start = top;
  if (cover) {
    pages = 1;
    start = cover.getBoundingClientRect().bottom;
  }
  doc.querySelectorAll<HTMLElement>(BREAK_SELECTORS).forEach((el) => {
    const cs = doc.defaultView!.getComputedStyle(el);
    const y = el.getBoundingClientRect().top;
    if ((cs.breakBefore === 'page' || el.classList.contains('pd-page-break')) && y > start + 4) cuts.push(y);
  });
  cuts.sort((a, b) => a - b);
  const usable = pageContentPx * FILL_RATIO;
  for (const y of [...cuts, bottom]) {
    const h = y - start;
    if (h > 2) pages += Math.max(1, Math.ceil(h / usable));
    start = y;
  }
  return Math.max(1, pages);
}

/**
 * Hedef sayfa sayısına sığacak yakınlaştırmayı bulur. Yazı boyutunun seçtiği değerden büyütmez, en çok
 * %50'ye kadar küçültür. Sonuç tahmindir; gerçek sayfa sayısı ±1 sapabilir.
 */
export async function computeFitZoom(bodyHtml: string, o: DocumentOptions): Promise<{ zoom: number; pages: number; basePages: number }> {
  const g = pageGeometry(o);
  const base = ZOOM[o.fontScale] || ZOOM.md;
  const frame = await loadHiddenFrame(buildDocument(bodyHtml, { ...o, fit: 'width', fitZoom: base }), g.w * PX_PER_MM + 120);
  try {
    const doc = frame.contentDocument!;
    const zoomEl = doc.querySelector<HTMLElement>('.pd-zoom');
    const pageContentPx = (g.h - g.m.t - g.m.b) * PX_PER_MM;
    const at = (z: number) => {
      if (zoomEl) zoomEl.style.zoom = z.toFixed(3);
      const cover = doc.querySelector<HTMLElement>('.pd-cover');
      if (cover) cover.style.minHeight = `${Math.floor((g.h - g.m.t - g.m.b - 2) / z)}mm`;
      return countPages(doc, pageContentPx);
    };
    const basePages = at(base);
    const target = Math.max(1, o.fitPages);
    if (basePages <= target) return { zoom: base, pages: basePages, basePages };
    let lo = Math.max(0.42, base * 0.5);
    let hi = base;
    let best = lo;
    let bestPages = at(lo);
    if (bestPages > target) return { zoom: lo, pages: bestPages, basePages };
    for (let i = 0; i < 7; i++) {
      const mid = (lo + hi) / 2;
      const p = at(mid);
      if (p <= target) {
        best = mid;
        bestPages = p;
        lo = mid;
      } else hi = mid;
    }
    return { zoom: Math.floor(best * 1000) / 1000, pages: bestPages, basePages };
  } finally {
    frame.remove();
  }
}

/** Belgenin tahmini sayfa sayısı (sunucu PDF'i yokken önizleme için). */
export async function estimatePages(bodyHtml: string, o: DocumentOptions): Promise<number> {
  const g = pageGeometry(o);
  const frame = await loadHiddenFrame(buildDocument(bodyHtml, o), g.w * PX_PER_MM + 120);
  try {
    return countPages(frame.contentDocument!, (g.h - g.m.t - g.m.b) * PX_PER_MM);
  } finally {
    frame.remove();
  }
}

/* ---------------------------------------------------------------------------
 * Çıktı
 * ------------------------------------------------------------------------- */
const apiBase = () => getCustomApiUrl() || '';

let statusCache: Promise<boolean> | null = null;
/** Sunucuda Chrome ile PDF basılabiliyor mu (oturum boyunca bir kez sorulur). */
export function serverPdfAvailable(): Promise<boolean> {
  if (!statusCache) {
    statusCache = fetch(`${apiBase()}/api/pdf/status`)
      .then((r) => (r.ok && r.headers.get('content-type')?.includes('json') ? r.json() : { available: false }))
      .then((d) => Boolean(d?.available))
      .catch(() => false);
  }
  return statusCache;
}

export async function renderPdfOnServer(html: string, title: string, fileName: string, signal?: AbortSignal): Promise<Blob> {
  const res = await fetch(`${apiBase()}/api/pdf/render`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ html, title, fileName }),
    signal,
  });
  if (!res.ok || !res.headers.get('content-type')?.includes('pdf')) {
    let msg = 'PDF sunucuda oluşturulamadı.';
    try {
      msg = (await res.json()).error || msg;
    } catch {}
    throw new Error(msg);
  }
  return res.blob();
}

export function downloadBlob(blob: Blob, fileName: string) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = fileName;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 4000);
}

/** Tarayıcının yazdırma penceresini (PDF olarak kaydet) aynı belgeyle açar. */
export function printDocument(html: string): Promise<void> {
  return new Promise((resolve) => {
    const frame = document.createElement('iframe');
    frame.setAttribute('aria-hidden', 'true');
    frame.style.cssText = 'position:fixed;right:0;bottom:0;width:0;height:0;border:0;visibility:hidden';
    document.body.appendChild(frame);
    const doc = frame.contentDocument!;
    doc.open();
    doc.write(html);
    doc.close();
    const go = async () => {
      try {
        await (frame.contentDocument as any)?.fonts?.ready;
      } catch {}
      frame.contentWindow?.focus();
      frame.contentWindow?.print();
      setTimeout(() => {
        frame.remove();
        resolve();
      }, 1500);
    };
    if (doc.readyState === 'complete') setTimeout(go, 400);
    else frame.addEventListener('load', () => setTimeout(go, 400), { once: true });
  });
}

export function downloadHtml(html: string, fileName: string) {
  downloadBlob(new Blob([html], { type: 'text/html;charset=utf-8' }), fileName);
}

export const safeFileName = (s: string) =>
  s
    .replace(/[^\p{L}\d]+/gu, '_')
    .replace(/^_+|_+$/g, '')
    .slice(0, 70) || 'MedSoru';
