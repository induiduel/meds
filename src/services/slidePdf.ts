import type { InteractiveDeck, SlideItem } from '../components/learn/InteractiveDeckView';
import { setupPdfFonts } from './drive';

export interface SlidePdfOptions {
  /** Akıl kartları (soru → cevap) */
  includeFlashcards?: boolean;
  /** Slayta eşleşen çıkmış sorular, ayrı sayfada */
  includeQuestions?: boolean;
  /** Çıkmış sorularda doğru şıkkı yeşil işaretle */
  highlightCorrect?: boolean;
}

type RGB = [number, number, number];
const C: Record<string, RGB> = {
  ink: [14, 26, 38],
  ink2: [74, 88, 104],
  ink3: [120, 132, 146],
  line: [226, 231, 236],
  canvas: [246, 247, 249],
  accent: [30, 79, 216],
  accentSoft: [235, 241, 254],
  ok: [21, 122, 62],
  okSoft: [236, 248, 241],
  amber: [138, 68, 5],
  amberSoft: [255, 249, 239],
  amberLine: [242, 221, 184],
  amberChip: [252, 233, 198],
  rose: [180, 35, 60],
  roseSoft: [255, 244, 246],
  violet: [109, 40, 217],
  violetSoft: [245, 240, 254],
  white: [255, 255, 255],
};

// Infographic tile tints, cycled
const TINTS: [RGB, RGB][] = [
  [[30, 79, 216], [235, 241, 254]],
  [[109, 40, 217], [245, 240, 254]],
  [[15, 122, 95], [232, 246, 241]],
  [[154, 77, 6], [255, 246, 232]],
  [[180, 35, 60], [255, 242, 245]],
];

const EMPHASIS: Record<string, string> = {
  direct_exam_warning: 'Hoca: sınavda sorulur',
  slide_missing: 'Hoca: slaytta yok, dinleyin',
  pearl: 'Hocanın spot bilgisi',
  clinical_tip: 'Klinik ipucu',
};

/** Emoji and variation selectors have no glyph in the embedded font. */
const clean = (s?: string) =>
  String(s || '')
    .replace(/[\u{1F000}-\u{1FAFF}\u{2600}-\u{27BF}\u{2B00}-\u{2BFF}\u{FE0F}\u{200D}]/gu, '')
    .replace(/^#+\s*/gm, '')
    .replace(/\s+/g, ' ')
    .trim();

type Seg = { t: string; b: boolean };
const parseRich = (s?: string): Seg[] =>
  clean(s)
    .split('**')
    .map((t, i) => ({ t, b: i % 2 === 1 }))
    .filter((x) => x.t);

/**
 * Renders one or more Öğren slides as landscape A4 pages. Each slide is laid out in two
 * columns (content | emphasis, spots, cards) and scaled down step by step until it fits
 * one page; if it still does not fit, it flows onto continuation pages in one column.
 */
export async function generateSlidePdfBlob(deck: InteractiveDeck, slides: SlideItem[], options: SlidePdfOptions = {}): Promise<Blob> {
  const { jsPDF } = await import('jspdf');
  const doc = new jsPDF({ orientation: 'landscape', unit: 'mm', format: 'a4' });
  const { font: FONT, T } = await setupPdfFonts(doc);
  const highlight = options.highlightCorrect ?? true;

  const PW = doc.internal.pageSize.getWidth(); // 297
  const PH = doc.internal.pageSize.getHeight(); // 210
  const M = 12;
  const W = PW - M * 2;
  const BOTTOM = PH - 13;

  // ---- drawing primitives (no-ops while measuring) ----
  let measuring = false;
  let y = 0;
  let flow = false; // continuation-page mode
  let flowTop = 22;

  const style = (w: 'normal' | 'bold' | 'italic', size: number, rgb: RGB) => {
    doc.setFont(FONT, w);
    doc.setFontSize(size);
    doc.setTextColor(rgb[0], rgb[1], rgb[2]);
  };
  const text = (s: string, x: number, yy: number, opts?: any) => {
    if (!measuring) doc.text(s, x, yy, opts);
  };
  const box = (x: number, yy: number, w: number, h: number, fillRgb: RGB, r = 2, strokeRgb?: RGB) => {
    if (measuring) return;
    doc.setFillColor(fillRgb[0], fillRgb[1], fillRgb[2]);
    if (strokeRgb) {
      doc.setDrawColor(strokeRgb[0], strokeRgb[1], strokeRgb[2]);
      doc.setLineWidth(0.25);
      doc.roundedRect(x, yy, w, h, r, r, 'FD');
    } else doc.roundedRect(x, yy, w, h, r, r, 'F');
  };
  const circle = (x: number, yy: number, r: number, fillRgb: RGB) => {
    if (measuring) return;
    doc.setFillColor(fillRgb[0], fillRgb[1], fillRgb[2]);
    doc.circle(x, yy, r, 'F');
  };
  const hline = (x1: number, x2: number, yy: number, rgb: RGB = C.line, w = 0.2) => {
    if (measuring) return;
    doc.setDrawColor(rgb[0], rgb[1], rgb[2]);
    doc.setLineWidth(w);
    doc.line(x1, yy, x2, yy);
  };

  /** Word-wraps rich segments (**bold**) to a width at the current font size. */
  const wrap = (segs: Seg[], width: number, size: number): Seg[][] => {
    const lines: Seg[][] = [[]];
    let lineW = 0;
    doc.setFontSize(size);
    for (const seg of segs) {
      for (const tok of T(seg.t).split(/(\s+)/)) {
        if (!tok) continue;
        doc.setFont(FONT, seg.b ? 'bold' : 'normal');
        const isSpace = /^\s+$/.test(tok);
        const w = doc.getTextWidth(isSpace ? ' ' : tok);
        if (!isSpace && lineW + w > width && lineW > 0) {
          lines.push([]);
          lineW = 0;
        }
        if (isSpace && lineW === 0) continue;
        const cur = lines[lines.length - 1];
        const last = cur[cur.length - 1];
        if (last && last.b === seg.b) last.t += isSpace ? ' ' : tok;
        else cur.push({ t: isSpace ? ' ' : tok, b: seg.b });
        lineW += w;
      }
    }
    return lines.filter((l) => l.length);
  };

  const ensure = (h: number) => {
    if (!flow || measuring) return;
    if (y + h > BOTTOM) {
      doc.addPage();
      pageChrome(true);
      y = flowTop;
    }
  };

  /** Draws wrapped rich text; returns height used. */
  const rich = (s: string | Seg[], x: number, width: number, size: number, lh: number, color: RGB, boldColor: RGB = C.ink) => {
    const segs = typeof s === 'string' ? parseRich(s) : s;
    const lines = wrap(segs, width, size);
    for (const line of lines) {
      ensure(lh);
      let cx = x;
      for (const seg of line) {
        style(seg.b ? 'bold' : 'normal', size, seg.b ? boldColor : color);
        text(seg.t, cx, y);
        cx += doc.getTextWidth(seg.t);
      }
      y += lh;
    }
    return lines.length * lh;
  };

  // ---- page chrome ----
  let current: { slide: SlideItem; index: number } | null = null;
  const pageChrome = (continuation: boolean) => {
    if (measuring || !current) return;
    style('bold', 7, C.accent);
    doc.text(T('MEDSORU · ÖĞREN'), M, 9);
    style('normal', 7, C.ink3);
    doc.text(T(clean(deck.title)), M + 27, 9, { maxWidth: W - 70 });
    doc.text(T(`Slayt ${current.slide.slideNumber} / ${deck.slides.length}${continuation ? ' · devamı' : ''}`), PW - M, 9, { align: 'right' });
    hline(M, PW - M, 11.2);
    // footer
    hline(M, PW - M, PH - 9.5);
    style('normal', 6.5, C.ink3);
    doc.text(T(`${clean(deck.discipline)}${deck.instructor ? ' · ' + clean(deck.instructor) : ''}`), M, PH - 6, { maxWidth: W - 40 });
  };

  // ---- content blocks; each draws at y with a scale factor ----
  type Block = (x: number, w: number, s: number) => void;

  const bulletsBlock = (slide: SlideItem): Block | null => {
    const items = slide.coreContent?.keyBullets || [];
    if (!items.length) return null;
    return (x, w, s) => {
      items.forEach((b, i) => {
        const pad = 2.6 * s;
        const r = 2.6 * s;
        const innerX = x + pad + r * 2 + 2.4 * s;
        const innerW = w - (innerX - x) - pad;
        // measure the card height
        const was = measuring;
        const y0 = y;
        measuring = true;
        y = 0;
        const titleH = b.title ? rich([{ t: b.title, b: true }], 0, innerW, 9.6 * s, 4.1 * s, C.ink) : 0;
        const descH = b.desc ? rich(b.desc, 0, innerW, 8.6 * s, 3.85 * s, C.ink2) : 0;
        measuring = was;
        const h = pad * 2 + titleH + descH + (titleH && descH ? 0.6 * s : 0) - 1.2 * s;
        y = y0;
        ensure(h);
        const top = y;
        box(x, top, w, h, b.isKey ? C.accentSoft : C.canvas, 2.2 * s);
        circle(x + pad + r, top + pad + r - 0.3 * s, r, b.isKey ? C.accent : C.white);
        style('bold', 7.6 * s, b.isKey ? C.white : C.accent);
        text(String(i + 1), x + pad + r, top + pad + r + 0.95 * s, { align: 'center' });
        y = top + pad + 2.9 * s;
        if (b.title) rich([{ t: b.title, b: true }], innerX, innerW, 9.6 * s, 4.1 * s, C.ink);
        if (b.title && b.desc) y += 0.6 * s;
        if (b.desc) rich(b.desc, innerX, innerW, 8.6 * s, 3.85 * s, C.ink2);
        y = top + h + 2.2 * s;
      });
    };
  };

  const formulaBlock = (slide: SlideItem): Block | null => {
    const f = slide.coreContent?.formulaBox;
    if (!f || !(f.formula || f.title)) return null;
    return (x, w, s) => {
      const pad = 3 * s;
      const was = measuring;
      const y0 = y;
      measuring = true;
      y = 0;
      const hh =
        (f.title ? rich([{ t: f.title, b: true }], 0, w - pad * 2, 7.6 * s, 3.4 * s, C.violet) : 0) +
        rich([{ t: f.formula, b: true }], 0, w - pad * 2, 10.5 * s, 4.6 * s, C.ink) +
        (f.explanation ? rich(f.explanation, 0, w - pad * 2, 8.2 * s, 3.6 * s, C.ink2) : 0);
      measuring = was;
      y = y0;
      const h = hh + pad * 2;
      ensure(h);
      const top = y;
      box(x, top, w, h, C.violetSoft, 2.2 * s);
      y = top + pad + 2.6 * s;
      if (f.title) rich([{ t: f.title.toLocaleUpperCase('tr-TR'), b: true }], x + pad, w - pad * 2, 7.6 * s, 3.4 * s, C.violet, C.violet);
      rich([{ t: f.formula, b: true }], x + pad, w - pad * 2, 10.5 * s, 4.6 * s, C.ink);
      if (f.explanation) rich(f.explanation, x + pad, w - pad * 2, 8.2 * s, 3.6 * s, C.ink2);
      y = top + h + 2.2 * s;
    };
  };

  const infographicBlock = (slide: SlideItem): Block | null => {
    const items = slide.coreContent?.infographic?.items || [];
    if (!items.length) return null;
    return (x, w, s) => {
      const per = items.length >= 3 && w > 120 ? 3 : 2;
      const gap = 2.2 * s;
      const tw = (w - gap * (per - 1)) / per;
      for (let i = 0; i < items.length; i += per) {
        const row = items.slice(i, i + per);
        const pad = 2.6 * s;
        // row height = tallest tile
        const was = measuring;
        const y0 = y;
        measuring = true;
        const hs = row.map((it) => {
          y = 0;
          rich([{ t: clean(it.label).toLocaleUpperCase('tr-TR'), b: true }], 0, tw - pad * 2, 6.8 * s, 3 * s, C.ink);
          if (it.value) rich([{ t: it.value, b: true }], 0, tw - pad * 2, 10 * s, 4.3 * s, C.ink);
          if (it.detail) rich(it.detail, 0, tw - pad * 2, 7.8 * s, 3.4 * s, C.ink2);
          return y;
        });
        measuring = was;
        y = y0;
        const h = Math.max(...hs) + pad * 2 - 0.6 * s;
        ensure(h);
        const top = y;
        row.forEach((it, j) => {
          const [fg, bg] = TINTS[(i + j) % TINTS.length];
          const tx = x + j * (tw + gap);
          box(tx, top, tw, h, bg, 2.2 * s);
          y = top + pad + 2.2 * s;
          rich([{ t: clean(it.label).toLocaleUpperCase('tr-TR'), b: true }], tx + pad, tw - pad * 2, 6.8 * s, 3 * s, fg, fg);
          if (it.value) rich([{ t: it.value, b: true }], tx + pad, tw - pad * 2, 10 * s, 4.3 * s, C.ink);
          if (it.detail) rich(it.detail, tx + pad, tw - pad * 2, 7.8 * s, 3.4 * s, C.ink2);
        });
        y = top + h + gap;
      }
    };
  };

  const tableBlock = (slide: SlideItem): Block | null => {
    const t = slide.coreContent?.table;
    if (!t || !t.headers?.length) return null;
    return (x, w, s) => {
      const n = t.headers.length;
      // column widths ~ content length, clamped
      const len = t.headers.map((h, ci) => Math.max(clean(h).length, ...t.rows.map((r) => clean(r[ci]).length)));
      const weights = len.map((l) => Math.min(Math.max(l, 8), 60));
      const sum = weights.reduce((a, b) => a + b, 0);
      const cw = weights.map((wt) => (wt / sum) * w);
      const pad = 2 * s;
      const fsz = (n >= 4 ? 7.8 : 8.4) * s;
      const lh = (n >= 4 ? 3.4 : 3.6) * s;
      if (t.title) {
        ensure(5 * s);
        y += 2.6 * s;
        rich([{ t: t.title, b: true }], x, w, 8.6 * s, 3.8 * s, C.ink);
        y += 0.6 * s;
      }
      const row = (cells: string[], head: boolean, zebra: boolean) => {
        const was = measuring;
        const y0 = y;
        measuring = true;
        const hs = cells.map((c, ci) => {
          y = 0;
          rich(head || ci === 0 ? [{ t: clean(c), b: true }] : c, 0, cw[ci] - pad * 2, fsz, lh, C.ink);
          return y;
        });
        measuring = was;
        y = y0;
        const h = Math.max(lh, ...hs) + pad * 1.6;
        ensure(h);
        const top = y;
        if (head) box(x, top, w, h, C.canvas, 1.2 * s);
        else if (zebra) box(x, top, w, h, [250, 251, 252], 0);
        let cx = x;
        cells.forEach((c, ci) => {
          y = top + pad + lh * 0.72;
          if (head) rich([{ t: clean(c), b: true }], cx + pad, cw[ci] - pad * 2, fsz, lh, C.ink2, C.ink2);
          else rich(ci === 0 ? [{ t: clean(c), b: true }] : c, cx + pad, cw[ci] - pad * 2, fsz, lh, ci === 0 ? C.ink : C.ink2);
          cx += cw[ci];
        });
        if (!head) hline(x, x + w, top + h, C.line, 0.15);
        y = top + h;
      };
      row(t.headers, true, false);
      t.rows.forEach((r, i) => row(r, false, i % 2 === 1));
      y += 2.4 * s;
    };
  };

  const highlightBlock = (slide: SlideItem): Block | null => {
    const h0 = slide.professorAudioHighlight;
    if (!h0 || !(h0.quote || h0.note)) return null;
    return (x, w, s) => {
      const pad = 3 * s;
      const was = measuring;
      const y0 = y;
      measuring = true;
      y = 0;
      rich([{ t: 'x', b: true }], 0, w, 7.2 * s, 3.4 * s, C.rose);
      if (h0.quote) rich(`“${clean(h0.quote)}”`, 0, w - pad * 2, 8.6 * s, 3.85 * s, C.ink);
      if (h0.note) rich(h0.note, 0, w - pad * 2, 7.8 * s, 3.4 * s, C.ink2);
      const hh = y;
      measuring = was;
      y = y0;
      const h = hh + pad * 2;
      ensure(h);
      const top = y;
      box(x, top, w, h, C.roseSoft, 2.2 * s, [243, 201, 209]);
      y = top + pad + 2.4 * s;
      const label = (EMPHASIS[h0.emphasisType] || 'Hoca vurgusu') + (h0.timestamp ? ` · ${h0.timestamp}` : '');
      rich([{ t: label.toLocaleUpperCase('tr-TR'), b: true }], x + pad, w - pad * 2, 7.2 * s, 3.4 * s, C.rose, C.rose);
      if (h0.quote) rich(`“${clean(h0.quote)}”`, x + pad, w - pad * 2, 8.6 * s, 3.85 * s, C.ink);
      if (h0.note) rich(h0.note, x + pad, w - pad * 2, 7.8 * s, 3.4 * s, C.ink2);
      y = top + h + 2.4 * s;
    };
  };

  const spotsBlock = (slide: SlideItem): Block | null => {
    const items = (slide.spotPearls || []).filter((p) => clean(p));
    if (!items.length) return null;
    return (x, w, s) => {
      const pad = 3 * s;
      const r = 2.2 * s;
      const innerX = x + pad + r * 2 + 2 * s;
      const innerW = w - (innerX - x) - pad;
      const was = measuring;
      const y0 = y;
      measuring = true;
      y = 0;
      const hs = items.map((p) => {
        const before = y;
        rich(p, 0, innerW, 8.4 * s, 3.75 * s, C.ink);
        return y - before;
      });
      measuring = was;
      y = y0;
      const head = 6.4 * s;
      const h = pad * 2 + head + hs.reduce((a, b) => a + b + 1.8 * s, 0) - 1.4 * s;
      ensure(Math.min(h, 40));
      const top = y;
      box(x, top, w, h, C.amberSoft, 2.2 * s, C.amberLine);
      y = top + pad + 2.6 * s;
      rich([{ t: 'AKILDA TUT', b: true }], x + pad, w, 7.4 * s, 3.4 * s, C.amber, C.amber);
      y = top + pad + head;
      items.forEach((p, i) => {
        ensure(hs[i]);
        const rowTop = y;
        circle(x + pad + r, rowTop - 1.05 * s, r, C.amberChip);
        style('bold', 6.8 * s, C.amber);
        text(String(i + 1), x + pad + r, rowTop - 0.15 * s, { align: 'center' });
        rich(p, innerX, innerW, 8.4 * s, 3.75 * s, C.ink);
        y += 1.8 * s;
      });
      y = Math.max(y, top + h) + 1 * s;
    };
  };

  const cardsBlock = (slide: SlideItem): Block | null => {
    if (!options.includeFlashcards) return null;
    const cards = (slide.flashcards || [])
      .map((c) => ({ q: clean(c.front || c.question), a: clean(c.back || c.answer) }))
      .filter((c) => c.q && c.a);
    if (!cards.length) return null;
    return (x, w, s) => {
      ensure(6 * s);
      y += 2.4 * s;
      rich([{ t: 'AKIL KARTLARI', b: true }], x, w, 7.4 * s, 3.4 * s, C.ink3, C.ink3);
      y += 0.8 * s;
      cards.forEach((c) => {
        const pad = 2.4 * s;
        const was = measuring;
        const y0 = y;
        measuring = true;
        y = 0;
        rich([{ t: c.q, b: true }], 0, w - pad * 2, 8.2 * s, 3.6 * s, C.ink);
        rich(c.a, 0, w - pad * 2, 8 * s, 3.55 * s, C.ink2);
        const hh = y;
        measuring = was;
        y = y0;
        const h = hh + pad * 2 + 0.6 * s;
        ensure(h);
        const top = y;
        box(x, top, w, h, C.white, 2 * s, C.line);
        y = top + pad + 2.6 * s;
        rich([{ t: c.q, b: true }], x + pad, w - pad * 2, 8.2 * s, 3.6 * s, C.ink);
        y += 0.6 * s;
        rich(c.a, x + pad, w - pad * 2, 8 * s, 3.55 * s, highlight ? C.ok : C.ink2, highlight ? C.ok : C.ink);
        y = top + h + 1.6 * s;
      });
    };
  };

  /** Title area for a slide page; returns its height. */
  const titleBlock = (slide: SlideItem, s: number) => {
    y = 19;
    if (slide.badge) {
      style('bold', 6.8, C.accent);
      const bw = doc.getTextWidth(T(clean(slide.badge).toLocaleUpperCase('tr-TR'))) + 5;
      box(M, y - 3.4, bw, 4.8, C.accentSoft, 2.4);
      style('bold', 6.8, C.accent);
      text(T(clean(slide.badge).toLocaleUpperCase('tr-TR')), M + 2.5, y);
      y += 6.4;
    }
    rich([{ t: slide.title, b: true }], M, W, 17 * Math.max(s, 0.85), 7 * Math.max(s, 0.85), C.ink);
    if (slide.subtitle) {
      y += 0.4;
      rich(slide.subtitle, M, W, 10 * Math.max(s, 0.85), 4.6 * Math.max(s, 0.85), C.ink2);
    }
    y += 3.2;
    return y;
  };

  const runBlocks = (blocks: (Block | null)[], x: number, w: number, s: number) => {
    blocks.filter(Boolean).forEach((b) => (b as Block)(x, w, s));
  };

  // ---- related questions page (two-column flow, compact) ----
  const questionsPages = (slide: SlideItem) => {
    const qs = slide.relatedQuestions || [];
    if (!options.includeQuestions || !qs.length) return;
    doc.addPage();
    pageChrome(true);
    const GUT = 8;
    const CW = (W - GUT) / 2;
    let col = 0;
    y = 19;
    style('bold', 11, C.ink);
    doc.text(T(`Bu slaytın çıkmış soruları · ${qs.length}`), M, y);
    y += 6;
    const top = y;
    const cx = () => M + col * (CW + GUT);
    const fit = (h: number) => {
      if (y + h <= BOTTOM) return;
      if (col === 0) {
        col = 1;
        y = top;
      } else {
        doc.addPage();
        pageChrome(true);
        col = 0;
        y = 19;
      }
    };
    const line = (s0: string | Seg[], dx: number, size: number, lh: number, color: RGB, deco?: (x: number, yy: number) => void) => {
      const segs = typeof s0 === 'string' ? parseRich(s0) : s0;
      for (const ln of wrap(segs, CW - dx, size)) {
        fit(lh);
        deco?.(cx() + dx, y);
        let xx = cx() + dx;
        for (const seg of ln) {
          style(seg.b ? 'bold' : 'normal', size, seg.b && color === C.ink2 ? C.ink : color);
          doc.text(seg.t, xx, y);
          xx += doc.getTextWidth(seg.t);
        }
        y += lh;
      }
    };
    qs.forEach((q, i) => {
      fit(12);
      style('normal', 6, C.ink3);
      doc.text(T([q.discipline, q.examYear].filter(Boolean).map((v) => clean(v)).join(' · ')), cx() + 5, y - 0.6);
      y += 2.6;
      style('bold', 8.2, C.accent);
      doc.text(`${i + 1}.`, cx(), y);
      line(q.stem, 5, 8.2, 3.6, C.ink);
      y += 0.6;
      const ans = q.correctAnswer || q.options.find((o) => o.isCorrect)?.key || '';
      q.options.forEach((o) => {
        const mark = highlight && o.key === ans;
        line([{ t: `${o.key})  ${clean(o.text)}`, b: mark }], 6, 7.8, 3.4, mark ? C.ok : C.ink, mark ? (x, yy) => {
          doc.setFillColor(C.okSoft[0], C.okSoft[1], C.okSoft[2]);
          doc.rect(x - 1, yy - 2.65, CW - 5.2, 3.4, 'F');
        } : undefined);
      });
      if (q.explanation || ans) {
        y += 0.8;
        line([{ t: `Cevap: ${ans || '—'}`, b: true }], 7, 6.8, 3.05, highlight ? C.ok : C.ink);
        if (q.explanation) line(clean(q.explanation.replace(/【([^】]+)】\s*:?\s*/g, ' $1: ')), 7, 6.8, 3.05, C.ink2);
      }
      y += 1.6;
      if (y + 3 < BOTTOM) {
        doc.setDrawColor(C.line[0], C.line[1], C.line[2]);
        doc.setLineWidth(0.15);
        doc.line(cx() + 5, y, cx() + CW, y);
      }
      y += 3.4;
    });
  };

  // ---- render each slide ----
  const SCALES = [1, 0.93, 0.86, 0.8, 0.74, 0.68];
  slides.forEach((slide, si) => {
    if (si > 0) doc.addPage();
    current = { slide, index: si };
    flow = false;

    const main: (Block | null)[] = [bulletsBlock(slide), formulaBlock(slide), infographicBlock(slide)];
    const side: (Block | null)[] = [highlightBlock(slide), spotsBlock(slide)];
    const cards = cardsBlock(slide);
    const table = tableBlock(slide);
    // Balance columns: flashcards go under whichever column is shorter
    if (cards) {
      const leftW = W * 0.6 - 3.5;
      measuring = true;
      y = 0;
      runBlocks(main, M, leftW, 1);
      const mh = y;
      y = 0;
      runBlocks(side, M, W - leftW - 7, 1);
      const sh = y;
      measuring = false;
      if (mh <= sh || !side.some(Boolean)) main.push(cards);
      else side.push(cards);
    }
    const hasSide = side.some(Boolean);
    const hasMain = main.some(Boolean) || !!table;
    const GUT = 7;
    const mainW = hasSide && hasMain ? W * 0.6 - GUT / 2 : W;
    const sideW = hasSide && hasMain ? W - mainW - GUT : W;

    // find the largest scale that fits on one page
    let chosen = -1;
    for (const s of SCALES) {
      measuring = true;
      const top = titleBlock(slide, s);
      y = top;
      runBlocks(main, M, mainW, s);
      const mainH = y;
      let sideH = top;
      if (hasSide) {
        y = hasMain ? top : mainH;
        runBlocks(side, hasMain ? M + mainW + GUT : M, sideW, s);
        sideH = y;
      }
      let endY = Math.max(mainH, sideH);
      if (table) {
        y = endY;
        table(M, W, s);
        endY = y;
      }
      measuring = false;
      if (endY <= BOTTOM) {
        chosen = s;
        break;
      }
    }

    pageChrome(false);
    if (chosen > 0) {
      const top = titleBlock(slide, chosen);
      y = top;
      runBlocks(main, M, mainW, chosen);
      const mainEnd = y;
      if (hasSide) {
        y = hasMain ? top : mainEnd;
        runBlocks(side, hasMain ? M + mainW + GUT : M, sideW, chosen);
      }
      const end = Math.max(mainEnd, y);
      if (table) {
        y = end;
        table(M, W, chosen);
      }
    } else {
      // Too long for one page: one wide column flowing over continuation pages
      const s = 0.86;
      flow = true;
      flowTop = 19;
      titleBlock(slide, s);
      runBlocks([...main, table, ...side], M, W, s);
      flow = false;
    }

    questionsPages(slide);
  });

  // page numbers
  const total = doc.getNumberOfPages();
  for (let p = 1; p <= total; p++) {
    doc.setPage(p);
    style('normal', 6.5, C.ink3);
    doc.text(`${p} / ${total}`, PW - M, PH - 6, { align: 'right' });
  }

  return doc.output('blob');
}

export async function downloadSlidePdf(deck: InteractiveDeck, slides: SlideItem[], options?: SlidePdfOptions) {
  const blob = await generateSlidePdfBlob(deck, slides, options);
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  const safe = clean(deck.shortTitle || deck.title)
    .replace(/[^a-zA-Z0-9_À-ſ-]+/g, '_')
    .slice(0, 50);
  a.download = slides.length === 1 ? `${safe}_Slayt${slides[0].slideNumber}.pdf` : `${safe}_${slides.length}_slayt.pdf`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  setTimeout(() => URL.revokeObjectURL(url), 4000);
}
