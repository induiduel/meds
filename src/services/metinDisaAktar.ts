/**
 * Ders metnini dosyaya aktarma motoru: .txt, .md, .docx, .pdf (Sesli ders ve Etkileşimli dersler ortak kullanır).
 * Girdi: başlık + bölümler; her bölümün gövdesi sınırlı bir Markdown alt kümesidir:
 *   "### alt başlık", "- madde", "1. madde", "> [!NOTE|IMPORTANT|TIP|WARNING]" kutusu, "| tablo |", düz paragraf;
 *   satır içi **kalın**, ==önemli== (kırmızı + kalın + marker), *eğik*;
 *   tek satırlık resim bloğu `![başlık](yol "alt yazı")` (sesli ders ara resimleri; SVG/PNG, kök göreli yol):
 *   PDF'e 2× PNG olarak, DOCX'e gömülü PNG olarak girer; MD'de mutlak bağlantı, TXT'de "[Resim: …]" satırı. Yüklenemezse metin satırı yazılır.
 * Metin birebir korunur; yalnız biçim işaretleri hedef dosyanın kendi biçimine çevrilir.
 * DOCX bağımlılıksız (sıkıştırmasız ZIP + WordprocessingML), PDF jsPDF + Türkçe Liberation fontuyla üretilir.
 */
import { setupPdfFonts } from './drive';
import { VARSAYILAN_STIL, type PdfStil } from './pdfDuzen';

export type AktarBicim = 'txt' | 'md' | 'docx' | 'pdf';
export interface AktarBolum {
  baslik: string; alt?: string; md: string;
  /** Birleşik belgede (toplu sesli ders PDF'i) yeni dersin ilk bölümü: yeni sayfa + ders başlığı + PDF yer imi */
  ders?: { baslik: string; alt: string };
}
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
  | { tur: 'tablo'; satirlar: Run[][][] }
  | { tur: 'resim'; baslik: string; yol: string; alt: string }
  /** Çıkmış/örnek soru kartı: "?# no | yıl | etiket" satırıyla başlar; sonraki satırlar kök, "?- önerme", "?+ soru cümlesi", "?= cevap"; boş satırda biter */
  | { tur: 'soru'; no: string; yil: string; etiket: string; kok: Run[]; onerme: Run[][]; ek: Run[]; cevap: Run[] };

/** Resim satırı: ![başlık](yol "alt yazı") — başlıkta ] ve alt yazıda " bulunmaz (resimSatiri temizler) */
const RESIM_RE = /^\s*!\[([^\]]*)\]\((\S+?)(?:\s+"([^"]*)")?\)\s*$/;
const SORU_RE = /^\s*\?#\s*(.*)$/;

/** Soru kartı satırları (canliDersDisaAktar gibi üreticiler bunu yazar; motor ayrıştırır). Metinler tek satır olmalı. */
export function soruSatirlari(o: { no: number | string; yil?: string | number | null; etiket?: string; kok: string; onerme?: string[]; ek?: string; cevap?: string }): string {
  const tek = (t: string) => t.replace(/\s*\r?\n+\s*/g, ' ').trim();
  const s = [`?# ${o.no} | ${o.yil ?? ''} | ${o.etiket || ''}`, tek(o.kok)];
  for (const x of o.onerme || []) if (tek(x)) s.push(`?- ${tek(x)}`);
  if (o.ek?.trim()) s.push(`?+ ${tek(o.ek)}`);
  if (o.cevap?.trim()) s.push(`?= ${tek(o.cevap)}`);
  return s.join('\n');
}
const ROMEN = /(?:^|\s)((?:I{1,3}|IV|V|VI{0,3}|IX|X)[.)])\s+(?=\S)/g;
/** Soru kökünü parçalar: "Kurgu Soru:" etiketi, Romen rakamlı önermeler (I. II. III.) ayrı satır, sondaki soru cümlesi ayrı. */
export function soruKokParcala(kokHam: string): { etiket: string; kok: string; onerme: string[]; ek: string } {
  let kok = kokHam.replace(/\s*\r?\n+\s*/g, ' ').trim(), etiket = '';
  const kg = kok.match(/^kurgu soru\s*[:\-–]\s*/i);
  if (kg) { etiket = 'Kurgu soru'; kok = kok.slice(kg[0].length); }
  const isaretler = [...kok.matchAll(ROMEN)];
  if (isaretler.length < 2) return { etiket, kok, onerme: [], ek: '' };
  const bas = isaretler[0].index! + (isaretler[0][0].length - isaretler[0][0].trimStart().length);
  const on = kok.slice(0, bas).trim();
  const parcalar: string[] = [];
  for (let i = 0; i < isaretler.length; i++) {
    const s = isaretler[i].index! + (isaretler[i][0].length - isaretler[i][0].trimStart().length);
    const e = i + 1 < isaretler.length ? isaretler[i + 1].index! : kok.length;
    parcalar.push(kok.slice(s, e).trim());
  }
  // son önermenin kuyruğundaki soru cümlesi ("Bu ifadelerden hangileri doğrudur?") ayrılır
  let ek = '';
  const son = parcalar[parcalar.length - 1];
  const m = son.match(/^(.+?)\s+((?:Bu|Buna|Bunlardan|Bunların|Yukarıdaki|Yukarıdakilerden|Verilen|Verilenlerden|Hangi|Hangisi|Hangileri|Aşağıdaki|Aşağıdakilerden|İfadelerden|Seçeneklerden|Numaralı|Numaralanmış)\b[^?]*\?)\s*$/)
    || son.match(/^(.*?[.!)])\s+([A-ZÇĞİÖŞÜ][^.!?]*\?)\s*$/);
  if (m && m[1].trim()) { parcalar[parcalar.length - 1] = m[1].trim(); ek = m[2].trim(); }
  return { etiket, kok: on, onerme: parcalar, ek };
}

/** Metindeki soru kartı gruplarını (?# … boş satıra dek) düz Markdown'a çevirir; diğer satırlar yerinde kalır */
function soruMdDonustur(md: string): string {
  if (!/^\s*\?#/m.test(md)) return md;
  const sat = md.replace(/\r/g, '').split('\n'), out: string[] = [];
  for (let k = 0; k < sat.length; k++) {
    if (!SORU_RE.test(sat[k])) { out.push(sat[k]); continue; }
    const grup = [sat[k]];
    while (k + 1 < sat.length && sat[k + 1].trim() && !SORU_RE.test(sat[k + 1])) grup.push(sat[++k]);
    for (const x of bloklar(grup.join('\n'))) if (x.tur === 'soru') out.push(...soruMdDuz(x));
  }
  return out.join('\n');
}
/** Soru kartının düz Markdown karşılığı (MD dosyası ve kart desteklemeyen hedefler) */
function soruMdDuz(x: Extract<Blok, { tur: 'soru' }>): string[] {
  const bas = `**${x.no}.** ${x.etiket ? `*${x.etiket}:* ` : ''}${mdYaz(x.kok)}${x.yil ? ` *(${x.yil})*` : ''}`;
  const s = [bas, ...x.onerme.map((r) => `   - ${mdYaz(r)}`)];
  if (x.ek.length) s.push(`   ${mdYaz(x.ek)}`);
  if (x.cevap.length) s.push(`   **Cevap:** ${mdYaz(x.cevap)}`);
  return s;
}
const mdYaz = (r: Run[]) => r.map((x) => `${x.b ? '**' : ''}${x.m ? '==' : ''}${x.i ? '*' : ''}${x.t}${x.i ? '*' : ''}${x.m ? '==' : ''}${x.b ? '**' : ''}`).join('');
/** Belgeye resim satırı yazar (başlık/alt yazıdaki ayraç karakterleri temizlenir) */
export const resimSatiri = (baslik: string, yol: string, alt = '') =>
  `![${baslik.replace(/[[\]\n]/g, ' ').trim()}](${yol.replace(/[\s()]/g, encodeURIComponent)}${alt ? ` "${alt.replace(/["\n]/g, "'").trim()}"` : ''})`;

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
    const rs = l.match(RESIM_RE);
    if (rs) { girinti.length = 0; out.push({ tur: 'resim', baslik: rs[1].trim(), yol: rs[2], alt: (rs[3] || '').trim() }); continue; }
    const sb = l.match(SORU_RE);
    if (sb) {
      girinti.length = 0;
      const [no = '', yil = '', etiket = ''] = sb[1].split('|').map((t) => t.trim());
      const kok: string[] = [], onerme: Run[][] = [], ek: string[] = [], cevap: string[] = [];
      while (k + 1 < sat.length && sat[k + 1].trim() && !SORU_RE.test(sat[k + 1])) {
        const t = sat[++k].trim();
        if (t.startsWith('?-')) onerme.push(satirIci(t.slice(2).trim()));
        else if (t.startsWith('?+')) ek.push(t.slice(2).trim());
        else if (t.startsWith('?=')) cevap.push(t.slice(2).trim());
        else kok.push(t);
      }
      out.push({ tur: 'soru', no, yil, etiket, kok: satirIci(kok.join(' ')), onerme, ek: satirIci(ek.join(' ')), cevap: satirIci(cevap.join(' ')) });
      continue;
    }
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
      else if (x.tur === 'resim') s.push('', `[Resim: ${x.baslik}${x.alt ? ` — ${x.alt}` : ''}]`, '');
      else if (x.tur === 'soru') {
        s.push('', `${x.no}. ${x.etiket ? `[${x.etiket}] ` : ''}${duz(x.kok)}${x.yil ? ` (${x.yil})` : ''}`, ...x.onerme.map((r) => `    ${duz(r)}`));
        if (x.ek.length) s.push(`    ${duz(x.ek)}`);
        if (x.cevap.length) s.push(`    Cevap: ${duz(x.cevap)}`);
      }
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
    // resim satırı: mutlak bağlantı (dosya site dışında açılır) + alt yazı; soru kartı düz maddeye (sıra korunur)
    const govde = soruMdDonustur(bo.md);
    s.push(govde.trim().split('\n').map((l) => {
      const rs = l.match(RESIM_RE);
      if (!rs) return l;
      return `\n![${rs[1].trim()}](${mutlak(rs[2])})${rs[3] ? `\n\n_${rs[3].trim()}_` : ''}\n`;
    }).join('\n'));
  }
  return s.join('\n') + '\n';
}

const mutlak = (yol: string) => { try { return new URL(yol, typeof location !== 'undefined' ? location.origin : 'https://nofrostlife.com.tr').href; } catch { return yol; } };

/* ---------------- resimler (PDF / DOCX için PNG) ---------------- */

interface ResimPng { png: Uint8Array; dataUrl: string; w: number; h: number }
type Resimler = Map<string, ResimPng | null>;

/** SVG (ya da PNG/JPEG) adresini 2× çözünürlüklü PNG'ye çevirir; olmazsa null */
async function resimPng(yol: string): Promise<ResimPng | null> {
  try {
    const r = await fetch(yol);
    if (!r.ok) return null;
    const tip = r.headers.get('content-type') || '';
    let blob: Blob;
    let vw = 0, vh = 0;
    if (/svg/.test(tip) || /\.svg(\?|$)/i.test(yol)) {
      const metin = await r.text();
      const d = new DOMParser().parseFromString(metin, 'image/svg+xml');
      const svg = d.documentElement;
      if (!svg || svg.nodeName.toLowerCase() !== 'svg') return null;
      const vb = (svg.getAttribute('viewBox') || '').trim().split(/[\s,]+/).map(Number);
      vw = vb.length === 4 && vb[2] > 0 ? vb[2] : parseFloat(svg.getAttribute('width') || '') || 800;
      vh = vb.length === 4 && vb[3] > 0 ? vb[3] : parseFloat(svg.getAttribute('height') || '') || 500;
      // ölçü verilmemiş SVG tarayıcıda 300×150 çizilir: viewBox ölçüsü yazılır
      svg.setAttribute('width', String(vw)); svg.setAttribute('height', String(vh));
      blob = new Blob([new XMLSerializer().serializeToString(svg)], { type: 'image/svg+xml' });
    } else blob = await r.blob();
    const url = URL.createObjectURL(blob);
    try {
      const img = new Image();
      img.decoding = 'async';
      await new Promise<void>((coz, red) => { img.onload = () => coz(); img.onerror = () => red(new Error('resim')); img.src = url; });
      const ow = vw || img.naturalWidth, oh = vh || img.naturalHeight;
      if (!ow || !oh) return null;
      const olcek = Math.min(2400 / ow, Math.max(2, 1600 / ow));
      const cw = Math.round(ow * olcek), ch = Math.round(oh * olcek);
      const c = document.createElement('canvas');
      c.width = cw; c.height = ch;
      const g = c.getContext('2d');
      if (!g) return null;
      g.fillStyle = '#fff'; g.fillRect(0, 0, cw, ch);
      g.drawImage(img, 0, 0, cw, ch);
      const dataUrl = c.toDataURL('image/png');
      const ik = atob(dataUrl.slice(dataUrl.indexOf(',') + 1));
      const png = new Uint8Array(ik.length);
      for (let i = 0; i < ik.length; i++) png[i] = ik.charCodeAt(i);
      return { png, dataUrl, w: cw, h: ch };
    } finally { URL.revokeObjectURL(url); }
  } catch { return null; }
}

/** Belgedeki tüm resim bloklarını önceden PNG'ye çevirir (yalnız tarayıcıda) */
async function resimleriHazirla(b: AktarBelge): Promise<Resimler> {
  const m: Resimler = new Map();
  if (typeof document === 'undefined') return m;
  const yollar = new Set<string>();
  for (const bo of b.bolumler) for (const x of bloklar(bo.md)) if (x.tur === 'resim') yollar.add(x.yol);
  await Promise.all([...yollar].map(async (y) => { m.set(y, await resimPng(y)); }));
  return m;
}
const resimYedekMetni = (x: { baslik: string; alt: string }) => `[Resim: ${x.baslik}${x.alt ? ` — ${x.alt}` : ''}]`;

/* ---------------- DOCX ---------------- */

const xe = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/g, '');
const runX = (r: Run) => `<w:r>${r.b || r.m || r.i ? `<w:rPr>${r.b || r.m ? '<w:b/>' : ''}${r.i ? '<w:i/>' : ''}${r.m ? '<w:color w:val="C8262D"/><w:highlight w:val="yellow"/>' : ''}</w:rPr>` : ''}<w:t xml:space="preserve">${xe(r.t)}</w:t></w:r>`;
const runsX = (r: Run[]) => r.map(runX).join('');
const par = (stil: string, ic: string, ek = '') => `<w:p><w:pPr><w:pStyle w:val="${stil}"/>${ek}</w:pPr>${ic}</w:p>`;

function docxXml(b: AktarBelge, resimler: Resimler = new Map()): Record<string, string | Uint8Array> {
  const medya: Record<string, Uint8Array> = {};
  const rels: string[] = [];
  let rn = 0;
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
      } else if (x.tur === 'soru') {
        g.push(par('SoruKok', runX({ t: `${x.no}.\t`, b: true }) + (x.etiket ? runX({ t: `${x.etiket}: `, i: true }) : '') + runsX(x.kok) + (x.yil ? runX({ t: `  (${x.yil})`, i: true }) : ''), '<w:keepNext/><w:keepLines/>'));
        for (const r of x.onerme) g.push(par('SoruOnerme', runsX(r), '<w:keepNext/>'));
        if (x.ek.length) g.push(par('SoruOnerme', runsX(x.ek), '<w:keepNext/>'));
        if (x.cevap.length) g.push(par('SoruCevap', runX({ t: 'Cevap: ', b: true }) + runsX(x.cevap)));
      } else if (x.tur === 'resim') {
        const p = resimler.get(x.yol);
        if (!p) { g.push(par('Normal', runX({ t: resimYedekMetni(x), i: true }))); continue; }
        rn++;
        const ad = `image${rn}.png`, rid = `rIdImg${rn}`;
        medya[`word/media/${ad}`] = p.png;
        rels.push(`<Relationship Id="${rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/${ad}"/>`);
        // metin genişliği 9638 twip = 6.120.130 EMU; yükseklik en çok ~19 cm
        let cx = 6120130, cy = Math.round(cx * p.h / p.w);
        const maxCy = 6840000;
        if (cy > maxCy) { cx = Math.round(cx * maxCy / cy); cy = maxCy; }
        if (x.baslik) g.push(par('Heading2', runX({ t: x.baslik }), '<w:keepNext/>'));
        g.push(`<w:p><w:pPr><w:keepNext/><w:jc w:val="center"/><w:spacing w:before="60" w:after="60"/></w:pPr><w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="${cx}" cy="${cy}"/><wp:docPr id="${rn}" name="Resim ${rn}" descr="${xe(x.alt || x.baslik).replace(/"/g, '&quot;')}"/><a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:nvPicPr><pic:cNvPr id="${rn}" name="${ad}"/><pic:cNvPicPr/></pic:nvPicPr><pic:blipFill><a:blip r:embed="${rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="${cx}" cy="${cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>`);
        if (x.alt) g.push(par('Subtitle2', runX({ t: x.alt, i: true }), '<w:jc w:val="center"/>'));
      }
    }
  }
  const W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"';
  const font = '<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri" w:eastAsia="Calibri"/>';
  const stil = (id: string, ad: string, pPr: string, rPr: string, ek = '') => `<w:style w:type="paragraph" w:styleId="${id}"><w:name w:val="${ad}"/><w:basedOn w:val="Normal"/>${ek}<w:pPr>${pPr}</w:pPr><w:rPr>${rPr}</w:rPr></w:style>`;
  return {
    '[Content_Types].xml': `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/></Types>`,
    '_rels/.rels': `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>`,
    'word/_rels/document.xml.rels': `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>${rels.join('')}</Relationships>`,
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
      + stil('SoruKok', 'Soru kökü', '<w:ind w:left="454" w:hanging="454"/><w:spacing w:before="160" w:after="40"/>', '')
      + stil('SoruOnerme', 'Soru önermesi', '<w:ind w:left="794"/><w:spacing w:after="0"/>', '')
      + stil('SoruCevap', 'Soru cevabı', '<w:pBdr><w:left w:val="single" w:sz="18" w:space="8" w:color="0D6E96"/></w:pBdr><w:shd w:val="clear" w:color="auto" w:fill="EEF5F9"/><w:ind w:left="454"/><w:spacing w:before="60" w:after="160"/>', '')
      + `</w:styles>`,
    'word/numbering.xml': `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:numbering ${W}><w:abstractNum w:abstractNumId="0"><w:multiLevelType w:val="hybridMultilevel"/>`
      + [0, 1, 2].map((l) => `<w:lvl w:ilvl="${l}"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="${['•', '◦', '▪'][l]}"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="${360 * (l + 1)}" w:hanging="360"/></w:pPr><w:rPr><w:color w:val="0D6E96"/></w:rPr></w:lvl>`).join('')
      + `</w:abstractNum><w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num></w:numbering>`,
    ...medya,
    'word/document.xml': `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document ${W} xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"><w:body>${g.join('')}<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" w:header="567" w:footer="567" w:gutter="0"/></w:sectPr></w:body></w:document>`,
  };
}

const CRC = (() => { const t = new Uint32Array(256); for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; } return t; })();
const crc32 = (d: Uint8Array) => { let c = 0xffffffff; for (let i = 0; i < d.length; i++) c = CRC[(c ^ d[i]) & 0xff] ^ (c >>> 8); return (c ^ 0xffffffff) >>> 0; };

/** Sıkıştırmasız (stored) ZIP */
function zip(dosyalar: Record<string, string | Uint8Array>): Blob {
  const enc = new TextEncoder();
  return zipIkili(Object.entries(dosyalar).map(([ad, icerik]) => [ad, typeof icerik === 'string' ? enc.encode(icerik) : icerik]), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document');
}

/** Sıkıştırmasız (stored) ZIP, ikili içerik (toplu PDF indirme) */
export function zipIkili(dosyalar: [string, Uint8Array][], tip = 'application/zip'): Blob {
  const enc = new TextEncoder();
  const parca: Uint8Array[] = [], merkez: Uint8Array[] = [];
  let ofs = 0;
  for (const [ad, d] of dosyalar) {
    const a = enc.encode(ad), crc = crc32(d);
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
  const n = dosyalar.length;
  son.setUint32(0, 0x06054b50, true); son.setUint16(8, n, true); son.setUint16(10, n, true); son.setUint32(12, mBoy, true); son.setUint32(16, ofs, true);
  return new Blob([...parca, ...merkez, new Uint8Array(son.buffer)] as BlobPart[], { type: tip });
}

/* ---------------- PDF ---------------- */

type RGB = readonly [number, number, number];
const TEMA_RENK: Record<string, RGB> = {
  mavi: [13, 110, 150], yesil: [22, 120, 82], mor: [104, 64, 168], bordo: [150, 36, 58], turuncu: [190, 92, 20], murekkep: [40, 40, 40],
};
const INK: RGB = [14, 26, 38], SOL: RGB = [118, 130, 143], KIRMIZI0: RGB = [200, 38, 45], MARKER: RGB = [255, 233, 128], CIZGI: RGB = [214, 220, 227];

async function pdf(b: AktarBelge, gorunum?: PdfStil, resimler: Resimler = new Map()): Promise<Blob> {
  const S = { ...VARSAYILAN_STIL, ...gorunum };
  const k = { kucuk: 0.88, normal: 1, buyuk: 1.12, cokbuyuk: 1.26 }[S.yaziBoyutu];
  const hk = k * { kucuk: 0.9, normal: 1, buyuk: 1.12 }[S.baslikBoyutu];
  const PT = { govde: 10.5 * k, alt: 11.2 * hk, kucuk: 9.5 * k, not: 10 * k, tablo: 9 * k, belge: 19 * hk, ders: 17 * hk, bolum: (b.dersDuzeni ? 15.5 : 13) * hk };
  const hex = /^#[0-9a-f]{6}$/i.test(S.renk) ? S.renk.slice(1) : '';
  const VURGU: RGB = hex ? [parseInt(hex.slice(0, 2), 16), parseInt(hex.slice(2, 4), 16), parseInt(hex.slice(4, 6), 16)] : TEMA_RENK[S.renk] || TEMA_RENK.mavi;
  const KIRMIZI: RGB = S.renk === 'murekkep' ? INK : KIRMIZI0;
  const NOT_ZEMIN: RGB = S.renk === 'murekkep' ? [244, 244, 244] : [Math.round(255 - (255 - VURGU[0]) * 0.08), Math.round(255 - (255 - VURGU[1]) * 0.08), Math.round(255 - (255 - VURGU[2]) * 0.08)];
  const { jsPDF } = await import('jspdf');
  const doc = new jsPDF({ unit: 'mm', format: S.kagit, compress: true });
  const { font: F, T } = await setupPdfFonts(doc);
  const W = doc.internal.pageSize.getWidth(), H = doc.internal.pageSize.getHeight();
  const M = { dar: 11, normal: 18, genis: 25 }[S.kenar], CW = W - 2 * M, ALT = H - (S.altBilgi === 'yok' ? 10 : 16);
  const UST = M + (S.ustBilgi ? 5 : 0);
  let y = UST;
  const lh = (pt: number) => pt * 0.3528 * { sik: 1.25, normal: 1.4, ferah: 1.6 }[S.satirAraligi];
  const yer = (h: number) => { if (y + h > ALT) { doc.addPage(); y = UST; return true; } return false; };
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
      if (k.r.m && S.vurgu) {
        const devam = i < s.length - 1 && s[i + 1].r.m ? sonraki : 0;
        doc.setFillColor(...MARKER); doc.rect(cx - 0.3, yy - pt * 0.3528 * 0.8, k.w + devam + 0.6, pt * 0.3528 * 1.05, 'F');
      }
      fontAyar(k.r, pt);
      doc.setTextColor(...(k.r.m && S.vurgu ? KIRMIZI : renk));
      doc.text(k.t, cx, yy);
      cx += k.w + sonraki;
    });
  };
  /** Resim bloğu ölçüsü: başlık + resim (genişliğe sığar, sayfaya sığacak kadar küçülür) + alt yazı tek sayfada */
  const resimOlc = (x: Extract<Blok, { tur: 'resim' }>) => {
    const p = resimler.get(x.yol);
    const bs = x.baslik ? satirla([{ t: x.baslik, b: true }], CW, PT.alt) : [];
    const as = x.alt ? satirla([{ t: x.alt, i: true }], CW, PT.kucuk) : [];
    const bH = bs.length * lh(PT.alt) + (bs.length ? 1.5 : 0), aH = as.length * lh(PT.kucuk) + (as.length ? 1.5 : 0);
    if (!p) return { p, bs, as, bH, aH, w: 0, h: 0, top: lh(PT.govde) + 2 };
    let w = CW, h = (CW * p.h) / p.w;
    const maxH = ALT - UST - bH - aH - 6;
    if (h > maxH) { w = (w * maxH) / h; h = maxH; }
    return { p, bs, as, bH, aH, w, h, top: bH + h + aH + 6 };
  };
  /** Soru kartı yerleşimi: numara rozeti, yıl etiketi, kök (asılı), önermeler (girintili), soru cümlesi, cevap şeridi */
  const soruOlc = (x: Extract<Blok, { tur: 'soru' }>) => {
    const IC = 9, ON = 6, pt = PT.govde, ptC = PT.not, ptK = PT.kucuk * 0.9;
    doc.setFont(F, 'normal'); doc.setFontSize(ptK);
    const yilW = x.yil ? doc.getTextWidth(T(x.yil)) + 4 : 0;
    const etW = x.etiket ? doc.getTextWidth(T(x.etiket)) + 4 : 0;
    const sagPay = yilW + etW + (yilW && etW ? 1.5 : 0);
    const kokSat = satirla(x.kok, CW - IC - (sagPay ? sagPay + 2 : 0), pt);
    const onSat = x.onerme.map((r) => satirla(romenKalin(r), CW - IC - ON, pt));
    const ekSat = x.ek.length ? satirla(x.ek, CW - IC, pt) : [];
    const cvSat = x.cevap.length ? satirla([{ t: 'Cevap: ', b: true }, ...x.cevap], CW - IC - 5, ptC) : [];
    const h = Math.max(kokSat.length, 1) * lh(pt) + (onSat.length ? 0.8 + onSat.flat().length * lh(pt) : 0) + (ekSat.length ? 0.8 + ekSat.length * lh(pt) : 0)
      + (cvSat.length ? 1.6 + cvSat.length * lh(ptC) + 2.2 : 0) + 3.2;
    return { IC, ON, pt, ptC, ptK, yilW, etW, kokSat, onSat, ekSat, cvSat, h };
  };
  /** "I. …" önermesinde Romen işaretini kalın (==) yaparak vurgu rengiyle çizdirir (satirCiz: m → kırmızı yerine burada vurgu) */
  const romenKalin = (r: Run[]): Run[] => {
    if (!r.length) return r;
    const m = r[0].t.match(/^((?:I{1,3}|IV|V|VI{0,3}|IX|X)[.)])(\s+)/);
    if (!m) return r;
    return [{ t: m[1], b: true, i: true }, { ...r[0], t: r[0].t.slice(m[1].length) }, ...r.slice(1)];
  };
  const soruCiz = (x: Extract<Blok, { tur: 'soru' }>) => {
    const o = soruOlc(x);
    // kart tek sayfaya sığıyor ama kalan yere sığmıyorsa yeni sayfa; sığmıyorsa kök + ilk satırlar birlikte başlar
    if (o.h <= ALT - UST && y + o.h > ALT) { doc.addPage(); y = UST; }
    else if (y + Math.max(o.kokSat.length, 1) * lh(o.pt) + lh(o.pt) > ALT) { doc.addPage(); y = UST; }
    const ust = y;
    // numara rozeti
    const no = T(x.no);
    doc.setFont(F, 'bold'); doc.setFontSize(o.pt * 0.92);
    const nw = Math.max(6.2, doc.getTextWidth(no) + 3);
    doc.setFillColor(...VURGU); doc.roundedRect(M, y + 0.2, nw, lh(o.pt) - 0.2, 1, 1, 'F');
    doc.setTextColor(255, 255, 255); doc.text(no, M + nw / 2, y + o.pt * 0.3528 + 0.1, { align: 'center' });
    // yıl ve etiket (sağ üst)
    let sx = W - M;
    const cip = (metin: string, zemin: RGB, yazi: RGB, w: number) => {
      sx -= w;
      doc.setFillColor(...zemin); doc.roundedRect(sx, y + 0.3, w, lh(o.pt) - 0.6, 0.9, 0.9, 'F');
      doc.setFont(F, 'normal'); doc.setFontSize(o.ptK); doc.setTextColor(...yazi);
      doc.text(T(metin), sx + w / 2, y + o.pt * 0.3528, { align: 'center' });
      sx -= 1.5;
    };
    if (x.yil) cip(x.yil, NOT_ZEMIN, SOL, o.yilW);
    if (x.etiket) cip(x.etiket, [255, 240, 214], [160, 92, 10], o.etW);
    // kök
    for (const s of o.kokSat) { if (y + lh(o.pt) > ALT) { doc.addPage(); y = UST; } satirCiz(s, M + o.IC, y + o.pt * 0.3528, o.pt, INK); y += lh(o.pt); }
    if (!o.kokSat.length) y += lh(o.pt);
    // önermeler
    if (o.onSat.length) {
      y += 0.8;
      for (const sat of o.onSat) for (const s of sat) {
        if (y + lh(o.pt) > ALT) { doc.addPage(); y = UST; }
        satirCiz(s, M + o.IC + o.ON, y + o.pt * 0.3528, o.pt, INK); y += lh(o.pt);
      }
    }
    if (o.ekSat.length) {
      y += 0.8;
      for (const s of o.ekSat) { if (y + lh(o.pt) > ALT) { doc.addPage(); y = UST; } satirCiz(s, M + o.IC, y + o.pt * 0.3528, o.pt, INK); y += lh(o.pt); }
    }
    // cevap şeridi (bölünmez)
    if (o.cvSat.length) {
      const h = o.cvSat.length * lh(o.ptC) + 2.2;
      y += 1.6;
      if (y + h > ALT) { doc.addPage(); y = UST; }
      doc.setFillColor(...NOT_ZEMIN); doc.roundedRect(M + o.IC, y, CW - o.IC, h, 0.8, 0.8, 'F');
      doc.setFillColor(...VURGU); doc.rect(M + o.IC, y, 1.1, h, 'F');
      o.cvSat.forEach((s, j) => satirCiz(s, M + o.IC + 4, y + 1.1 + j * lh(o.ptC) + o.ptC * 0.3528, o.ptC, INK));
      y += h;
    }
    // ayırıcı
    y += 1.6;
    if (y > ust) { doc.setDrawColor(...CIZGI); doc.setLineWidth(0.2); doc.line(M + o.IC, y, W - M, y); }
    y += 1.6;
  };
  const hesaplaBlokH = (x: Blok): number => {
    if (x.tur === 'soru') return soruOlc(x).h;
    if (x.tur === 'resim') return resimOlc(x).top;
    if (x.tur === 'h') {
      return satirla(x.r.map((r) => ({ ...r, b: true })), CW, PT.alt).length * lh(PT.alt) + 2.3;
    }
    if (x.tur === 'p') {
      return satirla(x.r, CW, PT.govde).length * lh(PT.govde) + 1.8;
    }
    if (x.tur === 'li') {
      const ic = x.isaret === '•' ? 5 : b.dersDuzeni ? 8 : 6.5;
      const gen = CW - ic - x.dz * 5;
      return satirla(x.r, gen, PT.govde).length * lh(PT.govde) + (x.dz ? 1 : 1.8);
    }
    if (x.tur === 'not') {
      const pt = PT.not, gen = CW - 9;
      const satirlar = x.satirlar.map((r, i) =>
        satirla(i === 0 && x.etiket ? [{ t: `${x.etiket}: `, b: true }, ...r] : r, gen, pt)
      );
      return satirlar.flat().length * lh(pt) + 6.5;
    }
    if (x.tur === 'tablo') {
      const sut = Math.max(...x.satirlar.map((r) => r.length), 1);
      const cw = CW / sut, pt = PT.tablo, pad = 1.6;
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
    if (!b.dersDuzeni || y <= UST) return;
    const x = dz[i];
    if (x.tur !== 'h' && !(x.tur === 'li' && x.dz === 0)) return;
    const h = kumeH(dz, i, kumeBitis(dz, i));
    if (h <= ALT - UST) { if (y + h > ALT) { doc.addPage(); y = UST; } return; }
    // Alt başlık kümesi tek sayfayı aşıyor: başlık ilk madde kümesiyle birlikte
    if (x.tur === 'h' && i + 1 < dz.length) {
      const ilk = kumeH(dz, i, kumeBitis(dz, i + 1));
      if (ilk <= ALT - UST && y + ilk > ALT) { doc.addPage(); y = UST; }
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
    if (blokH <= ALT - UST && y + blokH > ALT) {
      doc.addPage();
      y = UST;
    }

    once?.();
    for (const s of sat) {
      if (y + lh(pt) > ALT) {
        doc.addPage();
        y = UST;
      }
      satirCiz(s, x, y + pt * 0.3528, pt, renk);
      y += lh(pt);
    }
    y += ekstraAltBosluk;
  };

  y = UST;
  if (S.kapak) {
    // Kapak sayfası: renkli şerit, ortalanmış başlık, alt satır ve tarih
    doc.setFillColor(...VURGU); doc.rect(0, 0, W, 9, 'F');
    doc.setFont(F, 'bold'); doc.setFontSize(PT.belge * 1.35); doc.setTextColor(...INK);
    const ks = doc.splitTextToSize(T(b.baslik), CW) as string[];
    let ky = H * 0.38;
    ks.forEach((t) => { doc.text(t, W / 2, ky, { align: 'center' }); ky += lh(PT.belge * 1.35); });
    doc.setDrawColor(...VURGU); doc.setLineWidth(0.8); doc.line(W / 2 - 20, ky, W / 2 + 20, ky); ky += 9;
    doc.setFont(F, 'normal'); doc.setFontSize(11); doc.setTextColor(...SOL);
    (doc.splitTextToSize(T(b.alt), CW) as string[]).forEach((t) => { doc.text(t, W / 2, ky, { align: 'center' }); ky += 5.5; });
    doc.text(new Date().toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', year: 'numeric' }), W / 2, H - 28, { align: 'center' });
    doc.addPage(); y = UST;
  } else {
    akit([{ t: b.baslik, b: true }], M, CW, PT.belge, INK, undefined, 0);
    doc.setFont(F, 'normal'); doc.setFontSize(PT.kucuk); doc.setTextColor(...SOL);
    doc.text(T(b.alt), M, y + 3); y += 5.5;
    doc.setDrawColor(...CIZGI); doc.setLineWidth(0.3); doc.line(M, y, W - M, y); y += 5;
  }
  let ilkBolum = true;

  for (const bo of b.bolumler) {
    const blokDizisi = bloklar(bo.md);
    if (bo.ders) {
      // Birleşik belge: her ders yeni sayfada, belge başlığı biçiminde; PDF yer imi (içindekiler) eklenir
      if (y > UST + 1) { doc.addPage(); y = UST; }
      akit([{ t: bo.ders.baslik, b: true }], M, CW, PT.ders, INK, undefined, 0);
      doc.setFont(F, 'normal'); doc.setFontSize(PT.kucuk); doc.setTextColor(...SOL);
      doc.text(T(bo.ders.alt), M, y + 3); y += 5.5;
      doc.setDrawColor(...CIZGI); doc.setLineWidth(0.3); doc.line(M, y, W - M, y); y += 5;
      try { (doc as unknown as { outline?: { add: (p: unknown, t: string, o: { pageNumber: number }) => void } }).outline?.add(null, T(bo.ders.baslik), { pageNumber: doc.getNumberOfPages() }); } catch { /* yer imi desteklenmiyor */ }
    }
    if (S.bolumYeniSayfa && !ilkBolum && !bo.ders && y > UST + 1) { doc.addPage(); y = UST; }
    ilkBolum = false;
    if (bo.baslik) {
      // dersDuzeni: bölüm başlığı slayt alt başlıklarından belirgin büyük
      const BP = PT.bolum;
      doc.setFont(F, 'bold'); doc.setFontSize(BP);
      const s = doc.splitTextToSize(T(bo.baslik), CW - 4) as string[];
      const hBaslik = s.length * lh(BP) + 4.5;
      const hAlt = bo.alt ? satirla([{ t: bo.alt, i: true }], CW - 3.5, PT.kucuk).length * lh(PT.kucuk) + 1 : 0;
      const hIlk = !blokDizisi.length ? 20
        : b.dersDuzeni && (blokDizisi[0].tur === 'h' || blokDizisi[0].tur === 'li') && kumeH(blokDizisi, 0, kumeBitis(blokDizisi, 0)) <= ALT - UST - 30
          ? kumeH(blokDizisi, 0, kumeBitis(blokDizisi, 0))
          : hesaplaBlokH(blokDizisi[0]);

      // Konu başlığı + alt başlığı + ilk bloğu bu sayfaya sığmıyorsa
      // veya sayfada 45 mm'den az alan kalmışsa konuyu ve başlığı yeni sayfada başlat
      // (+1: başlıktan sonraki boşluk, +2: yuvarlama payı — başlık sayfa sonunda yalnız kalmasın)
      // dersDuzeni: bölümün tamamı bir sayfaya sığıyorsa bölünmez (sayfa sayısı artabilir)
      const hTum = b.dersDuzeni && blokDizisi.length ? hBaslik + hAlt + 1 + kumeH(blokDizisi, 0, blokDizisi.length) : Infinity;
      if (y > UST && hTum <= ALT - UST && y + hTum > ALT) { doc.addPage(); y = UST; }
      if (y > UST && (y + hBaslik + hAlt + 1 + hIlk + 2 > ALT || ALT - y < 45)) {
        doc.addPage();
        y = UST;
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
      akit([{ t: bo.alt, i: true }], M + 3.5, CW - 3.5, PT.kucuk, SOL, undefined, 1);
    }
    y += 1;

    for (let bIdx = 0; bIdx < blokDizisi.length; bIdx++) {
      const x = blokDizisi[bIdx];
      kumeyiTut(blokDizisi, bIdx);
      if (x.tur === 'h') {
        const sonrakiBlok = blokDizisi[bIdx + 1];
        const sonrakiH = sonrakiBlok ? hesaplaBlokH(sonrakiBlok) : 15;
        const baslikSatirlar = satirla(x.r.map((r) => ({ ...r, b: true })), CW, PT.alt);
        const baslikH = baslikSatirlar.length * lh(PT.alt) + 2.3;

        // Alt başlık + sonraki blok mevcut sayfaya sığmıyorsa yeni sayfada başlat
        // Sonraki blok tek sayfaya sığıyorsa bütün taşınır; o yüzden başlık onun tamamıyla birlikte ölçülür
        if (y > UST && y + 1.5 + baslikH + (sonrakiH <= ALT - UST ? sonrakiH : 35) + 2 > ALT) {
          doc.addPage();
          y = UST;
        }
        y += 1.5;
        akit(x.r.map((r) => ({ ...r, b: true })), M, CW, PT.alt, INK, undefined, 0.8);
      } else if (x.tur === 'p') {
        akit(x.r, M, CW, PT.govde, INK, undefined, 1.8);
      } else if (x.tur === 'li') {
        const gx = M + x.dz * 5, ic = x.isaret === '•' ? 5 : b.dersDuzeni ? 8 : 6.5;
        akit(
          x.r,
          gx + ic,
          CW - ic - x.dz * 5,
          PT.govde,
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
              doc.setFontSize(PT.govde);
              doc.setTextColor(...VURGU);
              doc.text(b.dersDuzeni ? x.isaret.replace(/^(\d+)[.)]$/, '$1 -') : x.isaret, gx, y + PT.govde * 0.3528);
            }
          },
          x.dz ? 1 : 1.8
        );
      } else if (x.tur === 'not') {
        const pt = PT.not, gen = CW - 9;
        const satirlar = x.satirlar.map((r, i) =>
          satirla(i === 0 && x.etiket ? [{ t: `${x.etiket}: `, b: true }, ...r] : r, gen, pt)
        );
        const tumu = satirlar.flat();
        const kutuH = tumu.length * lh(pt) + 3;

        // Not kutusu tek sayfaya sığıyor ama şu anki sayfaya sığmıyorsa yeni sayfada başlat
        if (kutuH <= ALT - UST && y + kutuH + 2.5 > ALT) {
          doc.addPage();
          y = UST;
        }
        y += 1;
        let k = 0;
        while (k < tumu.length) {
          if (y + lh(pt) + 3 > ALT) {
            doc.addPage();
            y = UST;
          }
          const sigan = Math.max(1, Math.min(tumu.length - k, Math.floor((ALT - y - 3) / lh(pt))));
          const h = sigan * lh(pt) + 3;
          doc.setFillColor(...NOT_ZEMIN);
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
        const cw = CW / sut, pt = PT.tablo, pad = 1.6;
        const satirVerileri = x.satirlar.map((r, ri) => {
          const hucre = Array.from({ length: sut }, (_, ci) =>
            satirla((r[ci] || []).map((z) => (ri === 0 ? { ...z, b: true } : z)), cw - 2 * pad, pt)
          );
          const h = Math.max(...hucre.map((c) => c.length), 1) * lh(pt) + 2 * pad;
          return { hucre, h, ri };
        });
        const toplamTabloH = satirVerileri.reduce((acc, row) => acc + row.h, 0);

        // Tablo tek sayfaya sığıyor ama mevcut alana sığmıyorsa yeni sayfada başlat
        if (toplamTabloH <= ALT - UST && y + toplamTabloH + 3 > ALT) {
          doc.addPage();
          y = UST;
        }
        y += 1;
        satirVerileri.forEach(({ hucre, h, ri }) => {
          if (y + h > ALT) {
            doc.addPage();
            y = UST;
          }
          if (ri === 0) {
            doc.setFillColor(...NOT_ZEMIN);
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
      } else if (x.tur === 'soru') {
        soruCiz(x);
      } else if (x.tur === 'resim') {
        const o = resimOlc(x);
        if (!o.p) { akit([{ t: resimYedekMetni(x), i: true }], M, CW, PT.govde, SOL, undefined, 1.8); continue; }
        if (y > UST && y + o.top > ALT) { doc.addPage(); y = UST; }
        y += 2;
        for (const s of o.bs) { satirCiz(s, M, y + PT.alt * 0.3528, PT.alt, INK); y += lh(PT.alt); }
        if (o.bs.length) y += 1.5;
        try { doc.addImage(o.p.dataUrl, 'PNG', M + (CW - o.w) / 2, y, o.w, o.h, undefined, 'FAST'); }
        catch { /* bozuk resim: alan boş kalır, akış sürer */ }
        doc.setDrawColor(...CIZGI); doc.setLineWidth(0.25); doc.rect(M + (CW - o.w) / 2, y, o.w, o.h, 'S');
        y += o.h + 1.5;
        for (const s of o.as) { satirCiz(s, M, y + PT.kucuk * 0.3528, PT.kucuk, SOL); y += lh(PT.kucuk); }
        y += 2.5;
      }
    }
  }
  const n = doc.getNumberOfPages();
  const kisa = T(b.baslik.length > 90 ? b.baslik.slice(0, 89) + '…' : b.baslik);
  for (let i = S.kapak ? 2 : 1; i <= n; i++) {
    doc.setPage(i); doc.setFont(F, 'normal'); doc.setFontSize(8.5); doc.setTextColor(...SOL);
    const no = S.kapak ? `${i - 1} / ${n - 1}` : `${i} / ${n}`;
    if (S.ustBilgi) {
      doc.text(T(S.ustBilgi.slice(0, 120)), M, 9);
      doc.setDrawColor(...CIZGI); doc.setLineWidth(0.2); doc.line(M, 10.8, W - M, 10.8);
    }
    if (S.altBilgi === 'baslik-no') { doc.text(kisa, M, H - 9); doc.text(no, W - M, H - 9, { align: 'right' }); }
    else if (S.altBilgi === 'no-orta') doc.text(no, W / 2, H - 9, { align: 'center' });
    else if (S.altBilgi === 'no-sag') doc.text(no, W - M, H - 9, { align: 'right' });
    if (S.filigran) {
      doc.setFontSize(9); doc.setTextColor(200, 205, 212);
      doc.text(T(S.filigran.slice(0, 60)), W - 4, H / 2, { angle: 90, align: 'center' });
    }
  }
  return doc.output('blob');
}

/* ---------------- indirme ---------------- */

export async function metinDosyasi(b: AktarBelge, bicim: AktarBicim, stil?: PdfStil): Promise<Blob> {
  return bicim === 'txt' ? new Blob(['﻿' + txt(b)], { type: 'text/plain;charset=utf-8' })
    : bicim === 'md' ? new Blob([md(b)], { type: 'text/markdown;charset=utf-8' })
    : bicim === 'docx' ? zip(docxXml(b, await resimleriHazirla(b)))
    : pdf(b, stil, await resimleriHazirla(b));
}

export async function metniIndir(b: AktarBelge, bicim: AktarBicim, dosyaAdi: string, duzen?: import('./pdfDuzen').PdfDuzen): Promise<void> {
  let blob = await metinDosyasi(b, bicim, duzen);
  if (bicim === 'pdf' && duzen) blob = await (await import('./pdfDuzen')).pdfDuzenle(blob, duzen);
  const ad = dosyaAdi.replace(/[\\/:*?"<>|\u0000-\u001f]/g, '-').replace(/\s+/g, ' ').trim().slice(0, 120);
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = `${ad}.${bicim}`;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 4000);
}
