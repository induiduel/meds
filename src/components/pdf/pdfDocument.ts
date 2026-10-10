/**
 * PDF Stüdyosu belge motoru. İçerik, uygulamanın kendi bileşen sınıflarıyla (cx-*, ls-*, ms-*) çizilir ve
 * çalışan sayfanın derlenmiş CSS'i belgeye gömülür; böylece PDF ekrandaki tasarımın birebir kopyası olur.
 *
 * Çıktı yolları:
 *  1. Sunucu (`/api/pdf/render`): başsız Chrome gerçek PDF dosyası üretir (sayfa numarası, gömülü yazı tipi).
 *  2. Tarayıcı yazdırma: sunucuya ulaşılamazsa aynı belge gizli bir çerçevede "PDF olarak kaydet"e açılır.
 */
import React from 'react';
import { createRoot } from 'react-dom/client';
import { flushSync } from 'react-dom';
import { getCustomApiUrl } from '../../services/api';

export type PageFormat = 'a4' | 'a4-landscape' | 'tablet' | 'letter';
export type FontScale = 'sm' | 'md' | 'lg';

export interface DocumentOptions {
  title: string;
  /** Sayfa üst bilgisi (sol); boşsa başlık kullanılır */
  runningHead?: string;
  format: PageFormat;
  fontScale: FontScale;
  /** Sayfa altında "3 / 12" numarası */
  pageNumbers: boolean;
  /** Sayfa üstünde belge adı */
  runningHeader: boolean;
}

export const PAGE_SIZE: Record<PageFormat, { css: string; label: string; w: number; h: number }> = {
  a4: { css: 'A4 portrait', label: 'A4 dikey', w: 210, h: 297 },
  'a4-landscape': { css: 'A4 landscape', label: 'A4 yatay', w: 297, h: 210 },
  letter: { css: 'letter portrait', label: 'Letter', w: 216, h: 279 },
  // Tablet: 3:4 ekranı tam doldurur, kenar boşluğu dar
  tablet: { css: '210mm 280mm', label: 'Tablet 3:4', w: 210, h: 280 },
};

const ZOOM: Record<FontScale, number> = { sm: 0.84, md: 0.92, lg: 1.04 };

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
  const size = PAGE_SIZE[o.format];
  const narrowMargins = o.format === 'tablet';
  const head = o.runningHead || o.title;
  return `
@page {
  size: ${size.css};
  margin: ${narrowMargins ? '11mm 9mm 12mm' : '15mm 13mm 15mm'};
  ${o.pageNumbers ? `@bottom-right { content: counter(page) " / " counter(pages); font: 600 8pt "Geist", system-ui, sans-serif; color: #8A94A6; }` : ''}
  ${o.runningHeader ? `@top-left { content: ${cssString(head)}; font: 600 7.5pt "Geist", system-ui, sans-serif; color: #8A94A6; letter-spacing: .02em; }
  @top-right { content: "MedSoru"; font: 700 7.5pt "Bricolage Grotesque", "Geist", sans-serif; color: #2453E6; }` : ''}
}
@page cover { margin: 0; @bottom-right { content: none; } @top-left { content: none; } @top-right { content: none; } }
*, *::before, *::after { animation: none !important; transition: none !important; }
html, body { margin: 0 !important; padding: 0 !important; background: #fff !important; height: auto !important; overflow: visible !important; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: var(--font-sans, "Geist", system-ui, sans-serif); color: var(--color-ink); --ls-mark: #FFF1B8; --ls-mark-ink: #4A3800; }
.pd-zoom { zoom: ${ZOOM[o.fontScale]}; }
.pd-cover { min-height: ${Math.floor((size.h - 1) / ZOOM[o.fontScale])}mm; }
@media screen {
  html { background: #E9EDF4 !important; }
  body { padding: 24px 0 48px !important; background: #E9EDF4 !important; }
  .pd-doc { width: ${size.w}mm; margin: 0 auto; background: #fff; padding: ${narrowMargins ? '11mm 9mm' : '15mm 13mm'}; box-sizing: border-box; border-radius: 4px; box-shadow: 0 1px 2px rgb(14 23 38 / .06), 0 8px 28px rgb(14 23 38 / .08); }
  .pd-cover { min-height: ${Math.floor((size.h - 40) / ZOOM[o.fontScale])}mm; margin-bottom: 15mm; }
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
<body>
<main class="pd-doc"><div class="pd-zoom">${bodyHtml}</div></main>
</body>
</html>`;
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
