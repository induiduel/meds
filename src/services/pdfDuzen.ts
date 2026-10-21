/**
 * PDF sayfa düzeni dönüştürmesi (tek ders "Metni indir" ve Toplu PDF ortak): üretilen A4 PDF'in sayfalarını
 * tek yaprağa 2 / 4 / 8 sayfa olacak biçimde yerleştirir (vektörel; metin seçilebilir kalır, pdf-lib embedPage).
 *  - 2 sayfa: yatay A4, 2×1   - 4 sayfa: dikey A4, 2×2   - 8 sayfa: yatay A4, 4×2
 *  - Yön elle değiştirilebilir; sıra soldan sağa (satır) ya da yukarıdan aşağı (sütun); isteğe bağlı çerçeve.
 * Sayfa aralığı seçilirse önce o sayfalar alınır. Yer imleri birleştirmede korunmaz; 1 sayfa/yaprak + tüm sayfalar seçiliyken dosyaya dokunulmaz.
 * Görünüm seçenekleri (PdfStil: kâğıt, yazı/başlık boyutu, satır aralığı, kenar, renk, kapak, üst/alt bilgi, filigran) PDF üretiminde uygulanır.
 */
export type SayfaSayisi = 1 | 2 | 4 | 8;
/** Metin PDF'inin görünümü (metinDisaAktar.pdf okur) */
export interface PdfStil {
  kagit: 'a4' | 'a5' | 'letter';
  yaziBoyutu: 'kucuk' | 'normal' | 'buyuk' | 'cokbuyuk';
  baslikBoyutu: 'kucuk' | 'normal' | 'buyuk';
  satirAraligi: 'sik' | 'normal' | 'ferah';
  kenar: 'dar' | 'normal' | 'genis';
  renk: 'mavi' | 'yesil' | 'mor' | 'bordo' | 'turuncu' | 'murekkep';
  /** ==önemli== işaretleri: sarı fosfor + kırmızı */
  vurgu: boolean;
  kapak: boolean;
  bolumYeniSayfa: boolean;
  /** her sayfanın üstüne yazılır; boşsa üst bilgi yok */
  ustBilgi: string;
  altBilgi: 'baslik-no' | 'no-orta' | 'no-sag' | 'yok';
  /** sayfa kenarında dikey küçük yazı (ad, grup); boşsa yok */
  filigran: string;
}
export const VARSAYILAN_STIL: PdfStil = {
  kagit: 'a4', yaziBoyutu: 'normal', baslikBoyutu: 'normal', satirAraligi: 'normal', kenar: 'normal', renk: 'mavi',
  vurgu: true, kapak: false, bolumYeniSayfa: false, ustBilgi: '', altBilgi: 'baslik-no', filigran: '',
};
export interface PdfDuzen extends PdfStil {
  nup: SayfaSayisi;
  yon: 'oto' | 'dikey' | 'yatay';
  sira: 'satir' | 'sutun';
  cerceve: boolean;
  bosluk: 'dar' | 'normal';
  /** "1-5, 8" gibi; boşsa tüm sayfalar (yerleştirmeden önce uygulanır) */
  sayfaAraligi: string;
}
export const VARSAYILAN_DUZEN: PdfDuzen = { ...VARSAYILAN_STIL, nup: 1, yon: 'oto', sira: 'satir', cerceve: true, bosluk: 'normal', sayfaAraligi: '' };

/** "1-3, 7, 10-" → 0 tabanlı sayfa dizinleri; geçersiz/boşsa null (tümü) */
export function araligiCoz(s: string, n: number): number[] | null {
  const t = s.replace(/\s/g, '');
  if (!t) return null;
  const out: number[] = [];
  for (const p of t.split(/[,;]/)) {
    const m = p.match(/^(\d*)(?:-(\d*))?$/);
    if (!m || (!m[1] && !m[2])) continue;
    const a = m[1] ? +m[1] : 1;
    const b = p.includes('-') ? (m[2] ? +m[2] : n) : a;
    for (let i = Math.max(1, a); i <= Math.min(n, b); i++) if (!out.includes(i - 1)) out.push(i - 1);
  }
  return out.length ? out : null;
}

const A4 = { w: 595.28, h: 841.89 };
const ANAHTAR = 'medsoru_pdf_duzen';

export function duzenOku(): PdfDuzen {
  try {
    const v = JSON.parse(localStorage.getItem(ANAHTAR) || 'null');
    if (v && [1, 2, 4, 8].includes(v.nup)) return { ...VARSAYILAN_DUZEN, ...v };
  } catch { /* yok */ }
  return { ...VARSAYILAN_DUZEN };
}
export function duzenYaz(d: PdfDuzen) {
  try { localStorage.setItem(ANAHTAR, JSON.stringify(d)); } catch { /* yok */ }
}

/** Izgara: [sütun, satır] ve yaprak yönü */
function izgara(d: PdfDuzen): { kol: number; sat: number; yatay: boolean } {
  const otoYatay = d.nup === 2 || d.nup === 8;
  const yatay = d.yon === 'oto' ? otoYatay : d.yon === 'yatay';
  const [uzun, kisa] = d.nup === 2 ? [2, 1] : d.nup === 4 ? [2, 2] : d.nup === 8 ? [4, 2] : [1, 1];
  // Yatay yaprakta uzun kenar sütunlarda, dikeyde satırlarda
  return yatay ? { kol: uzun, sat: kisa, yatay } : { kol: kisa, sat: uzun, yatay };
}

export function duzenEtiketi(d: PdfDuzen): string {
  const ek = d.sayfaAraligi.trim() ? `, sayfa ${d.sayfaAraligi.trim()}` : '';
  if (d.nup === 1) return ek.slice(2);
  const g = izgara(d);
  return `${d.nup} sayfa/yaprak (${g.kol}×${g.sat}, ${g.yatay ? 'yatay' : 'dikey'})${ek}`;
}

export async function pdfDuzenle(blob: Blob, d: PdfDuzen): Promise<Blob> {
  if (d.nup === 1 && !d.sayfaAraligi?.trim()) return blob;
  const { PDFDocument, rgb } = await import('pdf-lib');
  const kaynak = await PDFDocument.load(await blob.arrayBuffer());
  const hedef = await PDFDocument.create();
  const secim = araligiCoz(d.sayfaAraligi || '', kaynak.getPageCount());
  if (d.nup === 1) {
    if (!secim) return blob;
    (await hedef.copyPages(kaynak, secim)).forEach((p) => hedef.addPage(p));
    hedef.setTitle(kaynak.getTitle() || '');
    return new Blob([(await hedef.save()) as BlobPart], { type: 'application/pdf' });
  }
  const kaynakSayfa = kaynak.getPages();
  const sayfalar = await hedef.embedPages(secim ? secim.map((i) => kaynakSayfa[i]) : kaynakSayfa);
  const n = sayfalar.length;
  const { kol, sat, yatay } = izgara(d);
  const W = yatay ? A4.h : A4.w, H = yatay ? A4.w : A4.h;
  const kenar = d.bosluk === 'dar' ? 8 : 18, ara = d.bosluk === 'dar' ? 4 : 10;
  const hw = (W - 2 * kenar - (kol - 1) * ara) / kol;
  const hh = (H - 2 * kenar - (sat - 1) * ara) / sat;
  for (let i = 0; i < n; i += d.nup) {
    const yaprak = hedef.addPage([W, H]);
    for (let j = 0; j < d.nup && i + j < n; j++) {
      const s = sayfalar[i + j];
      const c = d.sira === 'satir' ? j % kol : Math.floor(j / sat);
      const r = d.sira === 'satir' ? Math.floor(j / kol) : j % sat;
      const olcek = Math.min(hw / s.width, hh / s.height);
      const w = s.width * olcek, h = s.height * olcek;
      const x = kenar + c * (hw + ara) + (hw - w) / 2;
      const y = H - kenar - r * (hh + ara) - hh + (hh - h) / 2;
      yaprak.drawPage(s, { x, y, width: w, height: h });
      if (d.cerceve) yaprak.drawRectangle({ x, y, width: w, height: h, borderColor: rgb(0.72, 0.72, 0.72), borderWidth: 0.6 });
    }
  }
  hedef.setTitle(kaynak.getTitle() || '');
  const bayt = await hedef.save();
  return new Blob([bayt as BlobPart], { type: 'application/pdf' });
}
