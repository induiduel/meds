/**
 * Ders metnini dosyaya aktarma motoru: .txt, .md, .docx, .pdf (Sesli ders ve Etkileşimli dersler ortak kullanır).
 * Girdi: başlık + bölümler; her bölümün gövdesi sınırlı bir Markdown alt kümesidir:
 *   "### alt başlık", "- madde", "1. madde", "> [!NOTE|IMPORTANT|TIP|WARNING]" kutusu, "| tablo |", düz paragraf;
 *   satır içi **kalın**, ==önemli== (kırmızı + kalın + marker), *eğik*.
 * Metin birebir korunur; yalnız biçim işaretleri hedef dosyanın kendi biçimine çevrilir.
 * DOCX bağımlılıksız (sıkıştırmasız ZIP + WordprocessingML), PDF jsPDF + Türkçe Liberation fontuyla üretilir.
 */
import { setupPdfFonts } from './drive';

export type AktarBicim = 'txt' | 'md' | 'docx' | 'pdf';
export interface AktarBolum { baslik: string; alt?: string; md: string }
export interface AktarBelge {
  baslik: string; alt: string; bolumler: AktarBolum[];
  /** Sesli ders: PDF'de alt başlık + maddeleri ve ana madde + alt maddeleri tek sayfada tutulur (sayfaya sığdıkça); "1)" maddesi "1 -" yazılır */
  dersDuzeni?: boolean;
}

/* ---------------- ayrıştırma ---------------- */

interface Run { t: string; b?: boolean; m?: boolean; i?: boolean }
type Blok =
  | { tur: 'p' | 'h'; r: Run[] }
  | { tur: 'li'; r: Run[]; isaret: string; dz: number }
  | { tur: 'not'; etiket: string; satirlar: Run[][] }
  | { tur: 'tablo'; satirlar: Run[][][] };

const NOT_AD: Record<string, string> = { NOTE: 'Not', IMPORTANT: 'Önemli', TIP: 'İpucu', WARNING: 'Dikkat', CAUTION: 'Dikkat' };

export function satirIci(s: string): Run[] {
  const out: Run[] = [];
  const st = { b: false, m: false, i: false };
  for (const p of s.split(/(\*\*|==|(?<![*\w])\*(?=\S)|(?<=\S)\*(?![*\w]))/)) {
    if (p === '**') st.b = !st.b;
    else if (p === '==') st.m = !st.m;
    else if (p === '*') st.i = !st.i;
    else if (p) out.push({ t: p, ...(st.b && { b: true }), ...(st.m && { m: true }), ...(st.i && { i: true }) });
  }
  return out;
}
const duz = (r: Run[]) => r.map((x) => x.t).join('');

function bloklar(md: string): Blok[] {
  const out: Blok[] = [];
  const sat = md.replace(/\r/g, '').split('\n');
  const girinti: number[] = [];
  for (let k = 0; k < sat.length; k++) {
    const l = sat[k];
    if (!l.trim()) continue;
    const not = l.match(/^\s*>\s*\[!(\w+)\]\s*(.*)$/);
    if (not || /^\s*>/.test(l)) {
      const etiket = not ? NOT_AD[not[1].toUpperCase()] || 'Not' : '';
      const satirlar: Run[][] = [];
      if (not && not[2].trim()) satirlar.push(satirIci(not[2].trim()));
      if (!not) satirlar.push(satirIci(l.replace(/^\s*>\s?/, '')));
      while (k + 1 < sat.length && /^\s*>/.test(sat[k + 1]) && !/^\s*>\s*\[!/.test(sat[k + 1])) {
        const t = sat[++k].replace(/^\s*>\s?/, '').trim();
        if (t) satirlar.push(satirIci(t));
      }
      out.push({ tur: 'not', etiket, satirlar });
      continue;
    }
    if (/^\s*\|/.test(l)) {
      const satirlar: Run[][][] = [];
      for (; k < sat.length && /^\s*\|/.test(sat[k]); k++) {
        const h = sat[k].trim().replace(/^\||\|$/g, '').split('|').map((c) => c.trim());
        if (h.every((c) => /^:?-{2,}:?$/.test(c))) continue;
        satirlar.push(h.map(satirIci));
      }
      k--;
      out.push({ tur: 'tablo', satirlar });
      continue;
    }
    const h = l.match(/^\s*#{1,6}\s+(.*)$/);
    if (h) { girinti.length = 0; out.push({ tur: 'h', r: satirIci(h[1]) }); continue; }
    const li = l.match(/^(\s*)([-*•]|\d+[.)])\s+(.*)$/);
    if (li) {
      // iç içe düzey göreli girintiyle bulunur (2 ya da 4 boşluk fark etmez), en çok 3 düzey
      const g = li[1].replace(/\t/g, '    ').length;
      while (girinti.length && girinti[girinti.length - 1] > g) girinti.pop();
      if (!girinti.length || girinti[girinti.length - 1] < g) girinti.push(g);
      out.push({ tur: 'li', r: satirIci(li[3]), isaret: /\d/.test(li[2]) ? li[2] : '•', dz: Math.min(2, girinti.length - 1) });
      continue;
    }
    girinti.length = 0;
    out.push({ tur: 'p', r: satirIci(l.trim()) });
  }
  return out;
}

/* ---------------- TXT / MD ---------------- */

function txt(b: AktarBelge): string {
  const s: string[] = [b.baslik, '='.repeat(Math.min(80, b.baslik.length)), b.alt];
  for (const bo of b.bolumler) {
    s.push('');
    if (bo.baslik) s.push('', bo.baslik.toLocaleUpperCase('tr'), '-'.repeat(Math.min(80, bo.baslik.length)));
    if (bo.alt) s.push(bo.alt);
    for (const x of bloklar(bo.md)) {
      if (x.tur === 'h') s.push('', duz(x.r));
      else if (x.tur === 'p') s.push(duz(x.r));
      else if (x.tur === 'li') s.push(`${'    '.repeat(x.dz)}${x.isaret} ${duz(x.r)}`);
      else if (x.tur === 'not') s.push(...x.satirlar.map((r, i) => `${i === 0 && x.etiket ? `[${x.etiket}] ` : '    '}${duz(r)}`));
      else if (x.tur === 'tablo') s.push(...x.satirlar.map((r) => r.map(duz).join(' | ')));
    }
  }
  return s.join('\r\n') + '\r\n';
}

function md(b: AktarBelge): string {
  const s: string[] = [`# ${b.baslik}`, '', `_${b.alt}_`];
  for (const bo of b.bolumler) {
    s.push('');
    if (bo.baslik) s.push(`## ${bo.baslik}`, '');
    if (bo.alt) s.push(`_${bo.alt}_`, '');
    s.push(bo.md.trim());
  }
  return s.join('\n') + '\n';
}

/* ---------------- DOCX ---------------- */

const xe = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/g, '');
const runX = (r: Run) => `<w:r>${r.b || r.m || r.i ? `<w:rPr>${r.b || r.m ? '<w:b/>' : ''}${r.i ? '<w:i/>' : ''}${r.m ? '<w:color w:val="C8262D"/><w:highlight w:val="yellow"/>' : ''}</w:rPr>` : ''}<w:t xml:space="preserve">${xe(r.t)}</w:t></w:r>`;
const runsX = (r: Run[]) => r.map(runX).join('');
const par = (stil: string, ic: string, ek = '') => `<w:p><w:pPr><w:pStyle w:val="${stil}"/>${ek}</w:pPr>${ic}</w:p>`;

function docxXml(b: AktarBelge): Record<string, string> {
  const g: string[] = [par('Title', runX({ t: b.baslik })), par('Subtitle', runX({ t: b.alt }))];
  for (const bo of b.bolumler) {
    if (bo.baslik) g.push(par('Heading1', runX({ t: bo.baslik })));
    if (bo.alt) g.push(par('Subtitle2', runX({ t: bo.alt })));
    for (const x of bloklar(bo.md)) {
      if (x.tur === 'h') g.push(par('Heading2', runsX(x.r)));
      else if (x.tur === 'p') g.push(par('Normal', runsX(x.r)));
      else if (x.tur === 'li') {
        g.push(x.isaret === '•'
          ? par('ListParagraph', runsX(x.r), `<w:numPr><w:ilvl w:val="${x.dz}"/><w:numId w:val="1"/></w:numPr>`)
          : par('ListParagraph', runX({ t: `${x.isaret}\t` }) + runsX(x.r), x.dz ? `<w:ind w:left="${360 * (x.dz + 1)}" w:hanging="360"/>` : ''));
      } else if (x.tur === 'not') {
        x.satirlar.forEach((r, i) => g.push(par('Callout', (i === 0 && x.etiket ? runX({ t: `${x.etiket}: `, b: true }) : '') + runsX(r))));
      } else if (x.tur === 'tablo') {
        const sut = Math.max(...x.satirlar.map((r) => r.length));
        const gen = Math.floor(9638 / sut);
        g.push(`<w:tbl><w:tblPr><w:tblW w:w="5000" w:type="pct"/><w:tblBorders>${['top', 'left', 'bottom', 'right', 'insideH', 'insideV'].map((k) => `<w:${k} w:val="single" w:sz="4" w:color="D6DCE3"/>`).join('')}</w:tblBorders><w:tblCellMar><w:left w:w="80" w:type="dxa"/><w:right w:w="80" w:type="dxa"/></w:tblCellMar></w:tblPr><w:tblGrid>${'<w:gridCol w:w="' + gen + '"/>'.repeat(sut)}</w:tblGrid>`
          + x.satirlar.map((r, ri) => `<w:tr>${Array.from({ length: sut }, (_, ci) => `<w:tc><w:tcPr><w:tcW w:w="${gen}" w:type="dxa"/>${ri === 0 ? '<w:shd w:val="clear" w:color="auto" w:fill="EEF3F7"/>' : ''}</w:tcPr>${par('Tablo', (r[ci] || []).map((x2) => runX(ri === 0 ? { ...x2, b: true } : x2)).join(''))}</w:tc>`).join('')}</w:tr>`).join('')
          + '</w:tbl>' + par('Normal', ''));
      }
    }
  }
  const W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"';
  const font = '<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri" w:eastAsia="Calibri"/>';
  const stil = (id: string, ad: string, pPr: string, rPr: string, ek = '') => `<w:style w:type="paragraph" w:styleId="${id}"><w:name w:val="${ad}"/><w:basedOn w:val="Normal"/>${ek}<w:pPr>${pPr}</w:pPr><w:rPr>${rPr}</w:rPr></w:style>`;
  return {
    '[Content_Types].xml': `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/></Types>`,
    '_rels/.rels': `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>`,
    'word/_rels/document.xml.rels': `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/></Relationships>`,
    'word/styles.xml': `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles ${W}>`
      + `<w:docDefaults><w:rPrDefault><w:rPr>${font}<w:sz w:val="22"/><w:lang w:val="tr-TR"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="80" w:line="288" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>`
      + `<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>`
      + stil('Title', 'Title', '<w:spacing w:after="40"/>', '<w:b/><w:color w:val="0E1A26"/><w:sz w:val="40"/>')
      + stil('Subtitle', 'Subtitle', '<w:pBdr><w:bottom w:val="single" w:sz="6" w:space="6" w:color="D6DCE3"/></w:pBdr><w:spacing w:after="240"/>', '<w:color w:val="76828F"/><w:sz w:val="20"/>')
      + stil('Heading1', 'heading 1', '<w:keepNext/><w:spacing w:before="320" w:after="80"/><w:outlineLvl w:val="0"/>', '<w:b/><w:color w:val="0D6E96"/><w:sz w:val="28"/>', '<w:next w:val="Normal"/>')
      + stil('Subtitle2', 'Bölüm alt başlığı', '<w:spacing w:after="120"/>', '<w:i/><w:color w:val="566472"/><w:sz w:val="20"/>')
      + stil('Heading2', 'heading 2', '<w:keepNext/><w:spacing w:before="200" w:after="60"/><w:outlineLvl w:val="1"/>', '<w:b/><w:color w:val="0E1A26"/><w:sz w:val="23"/>', '<w:next w:val="Normal"/>')
      + stil('ListParagraph', 'List Paragraph', '<w:ind w:left="360" w:hanging="360"/>', '')
      + stil('Callout', 'Not kutusu', '<w:pBdr><w:left w:val="single" w:sz="18" w:space="8" w:color="0D6E96"/></w:pBdr><w:shd w:val="clear" w:color="auto" w:fill="EEF5F9"/><w:ind w:left="200"/><w:spacing w:after="0"/>', '')
      + stil('Tablo', 'Tablo metni', '<w:spacing w:after="0" w:line="252" w:lineRule="auto"/>', '<w:sz w:val="19"/>')
      + `</w:styles>`,
    'word/numbering.xml': `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:numbering ${W}><w:abstractNum w:abstractNumId="0"><w:multiLevelType w:val="hybridMultilevel"/>`
      + [0, 1, 2].map((l) => `<w:lvl w:ilvl="${l}"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="${['•', '◦', '▪'][l]}"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="${360 * (l + 1)}" w:hanging="360"/></w:pPr><w:rPr><w:color w:val="0D6E96"/></w:rPr></w:lvl>`).join('')
      + `</w:abstractNum><w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num></w:numbering>`,
    'word/document.xml': `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document ${W}><w:body>${g.join('')}<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" w:header="567" w:footer="567" w:gutter="0"/></w:sectPr></w:body></w:document>`,
  };
}

const CRC = (() => { const t = new Uint32Array(256); for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; } return t; })();
const crc32 = (d: Uint8Array) => { let c = 0xffffffff; for (let i = 0; i < d.length; i++) c = CRC[(c ^ d[i]) & 0xff] ^ (c >>> 8); return (c ^ 0xffffffff) >>> 0; };

/** Sıkıştırmasız (stored) ZIP */
function zip(dosyalar: Record<string, string>): Blob {
  const enc = new TextEncoder();
  const parca: Uint8Array[] = [], merkez: Uint8Array[] = [];
  let ofs = 0;
  for (const [ad, icerik] of Object.entries(dosyalar)) {
    const a = enc.encode(ad), d = enc.encode(icerik), crc = crc32(d);
    const yerel = new DataView(new ArrayBuffer(30));
    yerel.setUint32(0, 0x04034b50, true); yerel.setUint16(4, 20, true); yerel.setUint16(6, 0x0800, true);
    yerel.setUint32(14, crc, true); yerel.setUint32(18, d.length, true); yerel.setUint32(22, d.length, true); yerel.setUint16(26, a.length, true);
    const m = new DataView(new ArrayBuffer(46));
    m.setUint32(0, 0x02014b50, true); m.setUint16(4, 20, true); m.setUint16(6, 20, true); m.setUint16(8, 0x0800, true);
    m.setUint32(16, crc, true); m.setUint32(20, d.length, true); m.setUint32(24, d.length, true); m.setUint16(28, a.length, true); m.setUint32(42, ofs, true);
    parca.push(new Uint8Array(yerel.buffer), a, d);
    merkez.push(new Uint8Array(m.buffer), a);
    ofs += 30 + a.length + d.length;
  }
  const mBoy = merkez.reduce((s, x) => s + x.length, 0);
  const son = new DataView(new ArrayBuffer(22));
  const n = Object.keys(dosyalar).length;
  son.setUint32(0, 0x06054b50, true); son.setUint16(8, n, true); son.setUint16(10, n, true); son.setUint32(12, mBoy, true); son.setUint32(16, ofs, true);
  return new Blob([...parca, ...merkez, new Uint8Array(son.buffer)] as BlobPart[], { type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' });
}

/* ---------------- PDF ---------------- */

type RGB = readonly [number, number, number];
const INK: RGB = [14, 26, 38], SOL: RGB = [118, 130, 143], VURGU: RGB = [13, 110, 150], KIRMIZI: RGB = [200, 38, 45], MARKER: RGB = [255, 233, 128], CIZGI: RGB = [214, 220, 227];

async function pdf(b: AktarBelge): Promise<Blob> {
  const { jsPDF } = await import('jspdf');
  const doc = new jsPDF({ unit: 'mm', format: 'a4', compress: true });
  const { font: F, T } = await setupPdfFonts(doc);
  const W = doc.internal.pageSize.getWidth(), H = doc.internal.pageSize.getHeight();
  const M = 18, CW = W - 2 * M, ALT = H - 16;
  let y = M;
  const lh = (pt: number) => pt * 0.3528 * 1.4;
  const yer = (h: number) => { if (y + h > ALT) { doc.addPage(); y = M; return true; } return false; };
  const stil = (r: Run) => (r.b || r.m ? (r.i ? 'bolditalic' : 'bold') : r.i ? 'italic' : 'normal');
  const fontAyar = (r: Run, pt: number) => {
    const s = stil(r);
    doc.setFont(F, s === 'bolditalic' ? 'bold' : s); doc.setFontSize(pt);
  };

  type Kelime = { t: string; r: Run; w: number; bosluk: boolean };
  /** satır içi biçimli metni genişliğe göre satırlara böler */
  const satirla = (runs: Run[], gen: number, pt: number): Kelime[][] => {
    const kel: Kelime[] = [];
    for (const r of runs) {
      fontAyar(r, pt);
      const parcalar = T(r.t).split(/(\s+)/);
      for (const p of parcalar) {
        if (!p) continue;
        if (/^\s+$/.test(p)) { if (kel.length) kel[kel.length - 1].bosluk = true; continue; }
        kel.push({ t: p, r, w: doc.getTextWidth(p), bosluk: false });
      }
    }
    doc.setFont(F, 'normal'); doc.setFontSize(pt);
    const sp = doc.getTextWidth(' ');
    const satirlar: Kelime[][] = [];
    let cur: Kelime[] = [], w = 0;
    for (const k of kel) {
      const ara = cur.length && cur[cur.length - 1].bosluk ? sp : 0;
      if (cur.length && w + ara + k.w > gen) { satirlar.push(cur); cur = []; w = 0; }
      w += (cur.length && cur[cur.length - 1].bosluk ? sp : 0) + k.w; cur.push(k);
    }
    if (cur.length) satirlar.push(cur);
    return satirlar;
  };
  const satirCiz = (s: Kelime[], x: number, yy: number, pt: number, renk: RGB) => {
    doc.setFont(F, 'normal'); doc.setFontSize(pt);
    const sp = doc.getTextWidth(' ');
    let cx = x;
    s.forEach((k, i) => {
      const sonraki = i < s.length - 1 && k.bosluk ? sp : 0;
      if (k.r.m) {
        const devam = i < s.length - 1 && s[i + 1].r.m ? sonraki : 0;
        doc.setFillColor(...MARKER); doc.rect(cx - 0.3, yy - pt * 0.3528 * 0.8, k.w + devam + 0.6, pt * 0.3528 * 1.05, 'F');
      }
      fontAyar(k.r, pt);
      doc.setTextColor(...(k.r.m ? KIRMIZI : renk));
      doc.text(k.t, cx, yy);
      cx += k.w + sonraki;
    });
  };
  const hesaplaBlokH = (x: Blok): number => {
    if (x.tur === 'h') {
      return satirla(x.r.map((r) => ({ ...r, b: true })), CW, 11.2).length * lh(11.2) + 2.3;
    }
    if (x.tur === 'p') {
      return satirla(x.r, CW, 10.5).length * lh(10.5) + 1.8;
    }
    if (x.tur === 'li') {
      const ic = x.isaret === '•' ? 5 : b.dersDuzeni ? 8 : 6.5;
      const gen = CW - ic - x.dz * 5;
      return satirla(x.r, gen, 10.5).length * lh(10.5) + (x.dz ? 1 : 1.8);
    }
    if (x.tur === 'not') {
      const pt = 10, gen = CW - 9;
      const satirlar = x.satirlar.map((r, i) =>
        satirla(i === 0 && x.etiket ? [{ t: `${x.etiket}: `, b: true }, ...r] : r, gen, pt)
      );
      return satirlar.flat().length * lh(pt) + 6.5;
    }
    if (x.tur === 'tablo') {
      const sut = Math.max(...x.satirlar.map((r) => r.length), 1);
      const cw = CW / sut, pt = 9, pad = 1.6;
      let th = 4;
      for (let ri = 0; ri < x.satirlar.length; ri++) {
        const r = x.satirlar[ri];
        let maxSatir = 1;
        for (let ci = 0; ci < sut; ci++) {
          const l = satirla((r[ci] || []).map((z) => (ri === 0 ? { ...z, b: true } : z)), cw - 2 * pad, pt).length;
          if (l > maxSatir) maxSatir = l;
        }
        th += maxSatir * lh(pt) + 2 * pad;
      }
      return th;
    }
    return 10;
  };

  /** dersDuzeni: i'de başlayan küme (alt başlık → sonraki alt başlığa dek; ana madde → alt maddeleri) yüksekliği */
  const kumeBitis = (dz: Blok[], i: number): number => {
    const x = dz[i];
    let j = i + 1;
    if (x.tur === 'h') while (j < dz.length && dz[j].tur !== 'h') j++;
    else if (x.tur === 'li') while (j < dz.length && dz[j].tur === 'li' && (dz[j] as { dz: number }).dz > x.dz) j++;
    return j;
  };
  const kumeH = (dz: Blok[], i: number, j: number) => {
    let h = 0;
    for (let k = i; k < j; k++) h += hesaplaBlokH(dz[k]) + (dz[k].tur === 'h' ? 1.5 : 0);
    return h + 2;
  };
  /** Küme sayfaya sığıyor ama kalan yere sığmıyorsa yeni sayfa; alt başlık kümesi sığmıyorsa içindeki madde kümelerine bakılır */
  const kumeyiTut = (dz: Blok[], i: number) => {
    if (!b.dersDuzeni || y <= M) return;
    const x = dz[i];
    if (x.tur !== 'h' && !(x.tur === 'li' && x.dz === 0)) return;
    const h = kumeH(dz, i, kumeBitis(dz, i));
    if (h <= ALT - M) { if (y + h > ALT) { doc.addPage(); y = M; } return; }
    // Alt başlık kümesi tek sayfayı aşıyor: başlık ilk madde kümesiyle birlikte
    if (x.tur === 'h' && i + 1 < dz.length) {
      const ilk = kumeH(dz, i, kumeBitis(dz, i + 1));
      if (ilk <= ALT - M && y + ilk > ALT) { doc.addPage(); y = M; }
    }
  };

  /** metni akıtır: paragraf / madde bütünlüğünü korur, sayfa sonuna sığmıyorsa yeni sayfaya taşır */
  const akit = (
    runs: Run[],
    x: number,
    gen: number,
    pt: number,
    renk: RGB = INK,
    once?: () => void,
    ekstraAltBosluk = 0
  ) => {
    const sat = satirla(runs, gen, pt);
    if (!sat.length) return;
    const blokH = sat.length * lh(pt) + ekstraAltBosluk;

    // Paragraf veya madde tek bir sayfaya sığıyorsa ve mevcut sayfada kalan yere sığmıyorsa:
    // Cümleyi/paragrafı yarıda kesme, doğrudan yeni sayfada başlat!
    if (blokH <= ALT - M && y + blokH > ALT) {
      doc.addPage();
      y = M;
    }

    once?.();
    for (const s of sat) {
      if (y + lh(pt) > ALT) {
        doc.addPage();
        y = M;
      }
      satirCiz(s, x, y + pt * 0.3528, pt, renk);
      y += lh(pt);
    }
    y += ekstraAltBosluk;
  };

  akit([{ t: b.baslik, b: true }], M, CW, 19, INK, undefined, 0);
  doc.setFont(F, 'normal'); doc.setFontSize(9.5); doc.setTextColor(...SOL);
  doc.text(T(b.alt), M, y + 3); y += 5.5;
  doc.setDrawColor(...CIZGI); doc.setLineWidth(0.3); doc.line(M, y, W - M, y); y += 5;

  for (const bo of b.bolumler) {
    const blokDizisi = bloklar(bo.md);
    if (bo.baslik) {
      // dersDuzeni: bölüm başlığı slayt alt başlıklarından belirgin büyük
      const BP = b.dersDuzeni ? 15.5 : 13;
      doc.setFont(F, 'bold'); doc.setFontSize(BP);
      const s = doc.splitTextToSize(T(bo.baslik), CW - 4) as string[];
      const hBaslik = s.length * lh(BP) + 4.5;
      const hAlt = bo.alt ? satirla([{ t: bo.alt, i: true }], CW - 3.5, 9.5).length * lh(9.5) + 1 : 0;
      const hIlk = !blokDizisi.length ? 20
        : b.dersDuzeni && (blokDizisi[0].tur === 'h' || blokDizisi[0].tur === 'li') && kumeH(blokDizisi, 0, kumeBitis(blokDizisi, 0)) <= ALT - M - 30
          ? kumeH(blokDizisi, 0, kumeBitis(blokDizisi, 0))
          : hesaplaBlokH(blokDizisi[0]);

      // Konu başlığı + alt başlığı + ilk bloğu bu sayfaya sığmıyorsa
      // veya sayfada 45 mm'den az alan kalmışsa konuyu ve başlığı yeni sayfada başlat
      // (+1: başlıktan sonraki boşluk, +2: yuvarlama payı — başlık sayfa sonunda yalnız kalmasın)
      // dersDuzeni: bölümün tamamı bir sayfaya sığıyorsa bölünmez (sayfa sayısı artabilir)
      const hTum = b.dersDuzeni && blokDizisi.length ? hBaslik + hAlt + 1 + kumeH(blokDizisi, 0, blokDizisi.length) : Infinity;
      if (y > M && hTum <= ALT - M && y + hTum > ALT) { doc.addPage(); y = M; }
      if (y > M && (y + hBaslik + hAlt + 1 + hIlk + 2 > ALT || ALT - y < 45)) {
        doc.addPage();
        y = M;
      }

      y += 3;
      doc.setFillColor(...VURGU); doc.rect(M, y - 0.2, 1.2, s.length * lh(BP) - 0.6, 'F');
      doc.setFont(F, 'bold'); doc.setFontSize(BP); // ölçüm (satirla) yazı tipini normale çevirmişti
      doc.setTextColor(...VURGU);
      s.forEach((t, i) => doc.text(t, M + 3.5, y + (b.dersDuzeni ? 5 : 4.2) + i * lh(BP)));
      y += s.length * lh(BP) + 1.5;
      if (b.dersDuzeni) { doc.setDrawColor(...CIZGI); doc.setLineWidth(0.3); doc.line(M, y + 0.5, W - M, y + 0.5); y += 2.5; }
    }
    if (bo.alt) {
      akit([{ t: bo.alt, i: true }], M + 3.5, CW - 3.5, 9.5, SOL, undefined, 1);
    }
    y += 1;

    for (let bIdx = 0; bIdx < blokDizisi.length; bIdx++) {
      const x = blokDizisi[bIdx];
      kumeyiTut(blokDizisi, bIdx);
      if (x.tur === 'h') {
        const sonrakiBlok = blokDizisi[bIdx + 1];
        const sonrakiH = sonrakiBlok ? hesaplaBlokH(sonrakiBlok) : 15;
        const baslikSatirlar = satirla(x.r.map((r) => ({ ...r, b: true })), CW, 11.2);
        const baslikH = baslikSatirlar.length * lh(11.2) + 2.3;

        // Alt başlık + sonraki blok mevcut sayfaya sığmıyorsa yeni sayfada başlat
        // Sonraki blok tek sayfaya sığıyorsa bütün taşınır; o yüzden başlık onun tamamıyla birlikte ölçülür
        if (y > M && y + 1.5 + baslikH + (sonrakiH <= ALT - M ? sonrakiH : 35) + 2 > ALT) {
          doc.addPage();
          y = M;
        }
        y += 1.5;
        akit(x.r.map((r) => ({ ...r, b: true })), M, CW, 11.2, INK, undefined, 0.8);
      } else if (x.tur === 'p') {
        akit(x.r, M, CW, 10.5, INK, undefined, 1.8);
      } else if (x.tur === 'li') {
        const gx = M + x.dz * 5, ic = x.isaret === '•' ? 5 : b.dersDuzeni ? 8 : 6.5;
        akit(
          x.r,
          gx + ic,
          CW - ic - x.dz * 5,
          10.5,
          INK,
          () => {
            if (x.isaret === '•') {
              doc.setFillColor(...VURGU);
              doc.setDrawColor(...VURGU);
              doc.setLineWidth(0.25);
              // 0: dolu yuvarlak, 1: boş halka, 2: küçük kare
              if (x.dz === 2) doc.rect(gx + 0.85, y + 2.15, 0.9, 0.9, 'F');
              else doc.circle(gx + 1.3, y + 2.6, x.dz ? 0.6 : 0.75, x.dz ? 'S' : 'F');
            } else {
              doc.setFont(F, 'bold');
              doc.setFontSize(10.5);
              doc.setTextColor(...VURGU);
              doc.text(b.dersDuzeni ? x.isaret.replace(/^(\d+)[.)]$/, '$1 -') : x.isaret, gx, y + 3.7);
            }
          },
          x.dz ? 1 : 1.8
        );
      } else if (x.tur === 'not') {
        const pt = 10, gen = CW - 9;
        const satirlar = x.satirlar.map((r, i) =>
          satirla(i === 0 && x.etiket ? [{ t: `${x.etiket}: `, b: true }, ...r] : r, gen, pt)
        );
        const tumu = satirlar.flat();
        const kutuH = tumu.length * lh(pt) + 3;

        // Not kutusu tek sayfaya sığıyor ama şu anki sayfaya sığmıyorsa yeni sayfada başlat
        if (kutuH <= ALT - M && y + kutuH + 2.5 > ALT) {
          doc.addPage();
          y = M;
        }
        y += 1;
        let k = 0;
        while (k < tumu.length) {
          if (y + lh(pt) + 3 > ALT) {
            doc.addPage();
            y = M;
          }
          const sigan = Math.max(1, Math.min(tumu.length - k, Math.floor((ALT - y - 3) / lh(pt))));
          const h = sigan * lh(pt) + 3;
          doc.setFillColor(238, 245, 249);
          doc.rect(M, y, CW, h, 'F');
          doc.setFillColor(...VURGU);
          doc.rect(M, y, 1.1, h, 'F');
          for (let j = 0; j < sigan; j++) satirCiz(tumu[k + j], M + 5, y + 1.5 + j * lh(pt) + pt * 0.3528, pt, INK);
          y += h;
          k += sigan;
        }
        y += 2.5;
      } else if (x.tur === 'tablo') {
        const sut = Math.max(...x.satirlar.map((r) => r.length), 1);
        const cw = CW / sut, pt = 9, pad = 1.6;
        const satirVerileri = x.satirlar.map((r, ri) => {
          const hucre = Array.from({ length: sut }, (_, ci) =>
            satirla((r[ci] || []).map((z) => (ri === 0 ? { ...z, b: true } : z)), cw - 2 * pad, pt)
          );
          const h = Math.max(...hucre.map((c) => c.length), 1) * lh(pt) + 2 * pad;
          return { hucre, h, ri };
        });
        const toplamTabloH = satirVerileri.reduce((acc, row) => acc + row.h, 0);

        // Tablo tek sayfaya sığıyor ama mevcut alana sığmıyorsa yeni sayfada başlat
        if (toplamTabloH <= ALT - M && y + toplamTabloH + 3 > ALT) {
          doc.addPage();
          y = M;
        }
        y += 1;
        satirVerileri.forEach(({ hucre, h, ri }) => {
          if (y + h > ALT) {
            doc.addPage();
            y = M;
          }
          if (ri === 0) {
            doc.setFillColor(238, 243, 247);
            doc.rect(M, y, CW, h, 'F');
          }
          doc.setDrawColor(...CIZGI);
          doc.setLineWidth(0.25);
          hucre.forEach((c, ci) => {
            doc.rect(M + ci * cw, y, cw, h, 'S');
            c.forEach((s, si) => satirCiz(s, M + ci * cw + pad, y + pad + si * lh(pt) + pt * 0.3528, pt, INK));
          });
          y += h;
        });
        y += 3;
      }
    }
  }
  const n = doc.getNumberOfPages();
  for (let i = 1; i <= n; i++) {
    doc.setPage(i); doc.setFont(F, 'normal'); doc.setFontSize(8.5); doc.setTextColor(...SOL);
    doc.text(T(b.baslik.length > 90 ? b.baslik.slice(0, 89) + '…' : b.baslik), M, H - 9);
    doc.text(`${i} / ${n}`, W - M, H - 9, { align: 'right' });
  }
  return doc.output('blob');
}

/* ---------------- indirme ---------------- */

export async function metinDosyasi(b: AktarBelge, bicim: AktarBicim): Promise<Blob> {
  return bicim === 'txt' ? new Blob(['﻿' + txt(b)], { type: 'text/plain;charset=utf-8' })
    : bicim === 'md' ? new Blob([md(b)], { type: 'text/markdown;charset=utf-8' })
    : bicim === 'docx' ? zip(docxXml(b))
    : pdf(b);
}

export async function metniIndir(b: AktarBelge, bicim: AktarBicim, dosyaAdi: string): Promise<void> {
  const blob = await metinDosyasi(b, bicim);
  const ad = dosyaAdi.replace(/[\\/:*?"<>|\u0000-\u001f]/g, '-').replace(/\s+/g, ' ').trim().slice(0, 120);
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = `${ad}.${bicim}`;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 4000);
}
