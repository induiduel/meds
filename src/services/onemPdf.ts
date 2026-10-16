/**
 * Patoloji · Sınav için en önemliler — A4 PDF (tarayıcıda jsPDF, Türkçe karakterli Liberation fontu).
 * Seçenekler: hangi dersler, en düşük puan (part), yalnız sınava uygun maddeler, alt maddeler / PDF alıntısı /
 * ayrıntılı açıklama / örnek soru / çıkmış soru eklensin mi. Örnek ve çıkmış soruların cevapları ders sonundaki anahtarda.
 * Tasarım sitedeki önem listesiyle aynı: bant renkleri (90–100 kırmızı … <50 gri), tür etiketi, "Sınavda çıkabilecek" kutusu.
 */
import { setupPdfFonts } from './drive';

export interface OnemPdfMadde {
  id: string; puan: number; baslik: string; bilgi: string; alt?: string[]; tur: string;
  alinti: { sayfa: number; metin: string }[]; neden: string; detay: string;
  ornek_soru?: { kok: string; secenekler: Record<string, string>; dogru: string; aciklama?: string } | null;
  cikmis?: string[]; kaynak?: 'metin' | 'tablo' | 'sekil'; klinik?: boolean; sinavUygun?: boolean;
}
export interface OnemPdfDers {
  kod: string; no: number; baslik: string; pdf: string; ozet: string; neden_onemli: string; maddeler: OnemPdfMadde[];
  cikmis?: Record<string, { sinav: string; kok: string; secenekler: Record<string, string>; dogru: string }>;
  sinavAdaylari?: { id: string; sira: number; gerekce: string }[]; soruSayisi?: number;
}
export interface OnemPdfSecenek {
  minPuan: number; yalnizSinav: boolean; alt: boolean; alinti: boolean; detay: boolean; ornekSoru: boolean; cikmis: boolean; adaylarKutusu: boolean;
}

type RGB = [number, number, number];
const INK: RGB = [14, 26, 38], INK2: RGB = [74, 88, 104], INK3: RGB = [120, 132, 146], LINE: RGB = [226, 231, 236], FIELD: RGB = [244, 246, 249];
const BANT: Record<number, RGB> = { 9: [200, 38, 45], 8: [214, 112, 10], 7: [30, 79, 216], 6: [124, 58, 237], 5: [13, 138, 128], 4: [120, 132, 146] };
const BANT_AD: Record<number, string> = { 9: '90–100 · Olmazsa olmaz', 8: '80–89 · Çok sık sorulur', 7: '70–79 · Sık sorulur', 6: '60–69 · Bilinmeli', 5: '50–59 · Destekleyici', 4: '0–49 · Ayrıntı' };
const TUR_AD: Record<string, string> = { tanim: 'TANIM', en_sik: 'EN SIK', karakteristik: 'KARAKTERİSTİK', sayi: 'SAYI', eslesme: 'EŞLEŞME', mekanizma: 'MEKANİZMA', siniflama: 'SINIFLAMA', tuzak: 'TUZAK', tani_tedavi: 'TANI' };
const STAR: RGB = [180, 120, 0];
/** önceki sözcüğe boşluksuz yapışan belirteçler (kalın sözcük sonrası noktalama) */
const YAPIS = /^[,.;:!?%)\]’'”]/;
const bantOf = (p: number) => Math.max(4, Math.min(9, Math.floor(p / 10)));
const soft = (c: RGB, k = 0.12): RGB => c.map((v) => Math.round(255 - (255 - v) * k)) as RGB;

export async function onemPdfOlustur(dersler: OnemPdfDers[], o: OnemPdfSecenek, baslikEk = ''): Promise<Blob> {
  const { jsPDF } = await import('jspdf');
  const doc = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4', compress: true });
  const { font: F, T: T0 } = await setupPdfFonts(doc);
  // Liberation'da olmayan üst/alt simgeler düz karşılığa çevrilir (yoksa PDF'te kaybolur)
  const SUP: Record<string, string> = { '⁺': '+', '⁻': '−', '⁰': '0', '⁴': '4', '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9', '₀': '0', '₁': '1', '₂': '2', '₃': '3', '₄': '4', '★': '*' };
  const T = (x: string) => T0(String(x).replace(/[⁺⁻⁰⁴-⁹₀-₄★]/g, (c) => SUP[c] || c));
  const W = doc.internal.pageSize.getWidth(), H = doc.internal.pageSize.getHeight();
  const M = 14, CW = W - 2 * M, BOT = H - 14;
  let y = M;
  let sayfaBaslik = '';

  const font = (b: 'normal' | 'bold' | 'italic', size: number, c: RGB = INK) => { doc.setFont(F, b); doc.setFontSize(size); doc.setTextColor(...c); };
  const altbilgi = () => {
    font('normal', 7.5, INK3);
    doc.text(T('MeDSor · Patoloji · Sınav için en önemliler — kaynak: Kurul 1 Tıbbi Patoloji ders PDF\'leri'), M, H - 7);
    doc.text(T(String(doc.getNumberOfPages())), W - M, H - 7, { align: 'right' });
  };
  const yeniSayfa = () => {
    altbilgi(); doc.addPage(); y = M;
    if (sayfaBaslik) { font('bold', 8, INK3); doc.text(T(sayfaBaslik), M, y + 2); y += 7; }
  };
  const yer = (h: number) => { if (y + h > BOT) yeniSayfa(); };

  /** **kalın** destekli satır kırma: [{t, b}] kelime dizisi → satırlar */
  type Tok = { t: string; b: boolean };
  const toks = (s: string): Tok[] => {
    const out: Tok[] = [];
    String(s || '').split(/(\*\*[^*]+\*\*)/g).forEach((p) => {
      const b = p.startsWith('**') && p.endsWith('**');
      (b ? p.slice(2, -2) : p).split(/(\s+)/).forEach((w) => { if (w && !/^\s+$/.test(w)) out.push({ t: T(w), b }); });
    });
    return out;
  };
  const satirla = (s: string, width: number, size: number) => {
    const lines: Tok[][] = []; let cur: Tok[] = []; let w = 0;
    doc.setFontSize(size);
    const sp = (() => { doc.setFont(F, 'normal'); return doc.getTextWidth(' '); })();
    for (const tk of toks(s)) {
      doc.setFont(F, tk.b ? 'bold' : 'normal');
      const tw = doc.getTextWidth(tk.t);
      const bitisik = cur.length > 0 && YAPIS.test(tk.t);
      if (cur.length && !bitisik && w + sp + tw > width) { lines.push(cur); cur = []; w = 0; }
      w += (cur.length && !bitisik ? sp : 0) + tw; cur.push(tk);
    }
    if (cur.length) lines.push(cur);
    return lines;
  };
  const zengin = (s: string, x: number, width: number, size: number, c: RGB, vurgu?: RGB, lh = size * 0.42) => {
    const lines = satirla(s, width, size);
    doc.setFontSize(size);
    const sp = (() => { doc.setFont(F, 'normal'); return doc.getTextWidth(' '); })();
    for (const ln of lines) {
      yer(lh + 0.5);
      let cx = x;
      ln.forEach((tk, i) => {
        if (i > 0 && YAPIS.test(tk.t)) cx -= sp; // noktalama önceki sözcüğe bitişik
        doc.setFont(F, tk.b ? 'bold' : 'normal'); doc.setTextColor(...(tk.b && vurgu ? vurgu : c));
        doc.text(tk.t, cx, y + lh * 0.8); cx += doc.getTextWidth(tk.t) + sp;
      });
      y += lh;
    }
    return lines.length * lh;
  };
  const yukseklik = (s: string, width: number, size: number, lh = size * 0.42) => satirla(s, width, size).length * lh;
  const madde = (s: string, x: number, width: number, size: number, c: RGB, vurgu?: RGB) => {
    yer(size * 0.45);
    doc.setFillColor(...c); doc.circle(x + 1, y + size * 0.2, 0.55, 'F');
    zengin(s, x + 3.2, width - 3.2, size, c, vurgu);
  };
  const etiket = (s: string, x: number, yy: number, c: RGB, size = 6.5) => {
    font('bold', size, c); const w = doc.getTextWidth(T(s)) + 3;
    doc.setFillColor(...soft(c, 0.14)); doc.roundedRect(x, yy - size * 0.36, w, size * 0.5, 0.8, 0.8, 'F');
    doc.text(T(s), x + 1.5, yy); return w;
  };

  // ---------- kapak
  const toplam = dersler.reduce((n, d) => n + d.maddeler.length, 0);
  doc.setFillColor(...BANT[9]); doc.rect(0, 0, W, 4, 'F');
  font('bold', 22, INK); doc.text(T('Patoloji'), M, 36);
  font('bold', 15, INK2); doc.text(T('Sınav için en önemliler'), M, 45);
  font('normal', 10, INK3);
  doc.text(T(`100 puan üzerinden, 10'ar puanlık partlar${baslikEk ? ' · ' + baslikEk : ''}`), M, 53);
  doc.text(T(`${dersler.length} ders · en düşük puan ${o.minPuan}${o.yalnizSinav ? ' · yalnız sınava uygun maddeler' : ''}`), M, 59);
  y = 70;
  font('bold', 9, INK); doc.text(T('Sınav kuralı (hocanın açıklaması)'), M, y); y += 5;
  for (const s of ['Resimlerden ve tablolardan soru sorulmayacak.', 'Klinik bulgu sorulmayacak.', 'Her ders slaytından 1 soru; yalnız "Genetik, Pediatrik ve Çevresel Patoloji"den 2 soru.'])
    madde(s, M, CW, 9.5, INK2);
  y += 4;
  font('bold', 9, INK); doc.text(T('Renkler'), M, y); y += 5;
  for (const b of [9, 8, 7, 6, 5]) { doc.setFillColor(...BANT[b]); doc.roundedRect(M, y - 3, 4, 4, 0.8, 0.8, 'F'); font('normal', 9, INK2); doc.text(T(BANT_AD[b]), M + 6, y); y += 5.5; }
  doc.setFillColor(...STAR); doc.roundedRect(M, y - 3, 4, 4, 0.8, 0.8, 'F'); font('normal', 9, INK2); doc.text(T('Sınavda çıkabilecek (sıralı aday) · Aday 1 = en olası soru'), M + 6, y); y += 8;
  font('bold', 9, INK); doc.text(T('İçindekiler'), M, y); y += 5;
  for (const d of dersler) { yer(5); font('normal', 9, INK2); doc.text(T(`${d.no}) ${d.baslik}`), M, y); font('normal', 9, INK3); doc.text(T(`${d.maddeler.length} madde`), W - M, y, { align: 'right' }); y += 4.6; }

  // ---------- dersler
  for (const d of dersler) {
    yeniSayfa(); sayfaBaslik = `${d.no}) ${d.baslik}`; y = M;
    doc.setFillColor(...INK); doc.roundedRect(M, y, CW, 13, 2, 2, 'F');
    font('bold', 13, [255, 255, 255]); doc.text(T(`${d.no}) ${d.baslik}`), M + 4, y + 8.5);
    y += 17;
    font('italic', 7.5, INK3); doc.text(T(`Kaynak: ${d.pdf}`), M, y); y += 4;
    zengin(d.ozet, M, CW, 9.5, INK2, INK); y += 1.5;
    yer(8); doc.setFillColor(...FIELD); const nh = yukseklik(`Neden önemli: ${d.neden_onemli}`, CW - 6, 9) + 3;
    doc.roundedRect(M, y, CW, nh, 1.5, 1.5, 'F'); y += 1.5; zengin(`**Neden önemli:** ${d.neden_onemli}`, M + 3, CW - 6, 9, INK2, INK); y += 3;

    const byId = new Map(d.maddeler.map((m) => [m.id, m]));
    const ad = (d.sinavAdaylari || []).filter((a) => byId.has(a.id));
    const adaySira = new Map(ad.map((a) => [a.id, a.sira]));
    const ns = d.soruSayisi || 1;
    if (o.adaylarKutusu && ad.length) {
      const kutuH = 10 + ad.reduce((s, a) => s + yukseklik(byId.get(a.id)!.bilgi, CW - 18, 9.2) + yukseklik(a.gerekce, CW - 18, 7.8) + 2.5, 0);
      yer(Math.min(kutuH, 60));
      const y0 = y;
      doc.setDrawColor(...STAR); doc.setLineWidth(0.5); doc.setFillColor(...soft(STAR, 0.08));
      doc.roundedRect(M, y0, CW, kutuH, 2, 2, 'FD');
      y += 5; font('bold', 10, STAR); doc.text(T(`SINAVDA ÇIKABİLECEK — bu slayttan ${ns} soru`), M + 4, y); y += 3;
      for (const a of ad) {
        const m = byId.get(a.id)!;
        yer(8);
        const en = a.sira <= ns;
        doc.setFillColor(...(en ? STAR : soft(STAR, 0.5))); doc.roundedRect(M + 4, y + 0.6, 8, 4.4, 1, 1, 'F');
        font('bold', 7.5, [255, 255, 255]); doc.text(T(`${a.sira}`), M + 8, y + 3.8, { align: 'center' });
        zengin(m.bilgi, M + 14, CW - 18, 9.2, INK, BANT[9]);
        font('italic', 7.8, INK2); zengin((en ? 'En olası soru. ' : '') + a.gerekce, M + 14, CW - 18, 7.8, INK2); y += 2;
      }
      y = Math.max(y, y0 + kutuH) + 3;
    }

    const anahtar: string[] = [];
    let soruNo = 0;
    const sec = d.maddeler.filter((m) => m.puan >= o.minPuan && (!o.yalnizSinav || m.sinavUygun !== false)).sort((a, b) => b.puan - a.puan);
    let part = 0;
    for (const b of [9, 8, 7, 6, 5, 4]) {
      const ms = sec.filter((m) => bantOf(m.puan) === b);
      if (!ms.length) continue;
      part++;
      yer(14);
      doc.setFillColor(...soft(BANT[b], 0.14)); doc.roundedRect(M, y, CW, 7, 1.5, 1.5, 'F');
      doc.setFillColor(...BANT[b]); doc.rect(M, y, 1.4, 7, 'F');
      font('bold', 8, BANT[b]); doc.text(T(`PART ${part}`), M + 4, y + 4.8);
      font('bold', 9.5, INK); doc.text(T(BANT_AD[b]), M + 19, y + 4.8);
      font('bold', 8, BANT[b]); doc.text(T(`${ms.length} madde`), W - M - 3, y + 4.8, { align: 'right' });
      y += 10;
      for (const m of ms) {
        const c = BANT[b];
        const h0 = yukseklik(m.bilgi, CW - 14, 10) + 6;
        yer(Math.min(h0, 30));
        const y0 = y;
        doc.setFillColor(...soft(c, 0.16)); doc.roundedRect(M, y0, 10, 7, 1.4, 1.4, 'F');
        font('bold', 10, c); doc.text(T(String(m.puan)), M + 5, y0 + 4.9, { align: 'center' });
        let ex = M + 13;
        ex += etiket(TUR_AD[m.tur] || m.tur.toUpperCase(), ex, y0 + 2.3, c) + 1.5;
        const sira = adaySira.get(m.id);
        if (sira) ex += etiket(`SINAV ADAYI ${sira}`, ex, y0 + 2.3, STAR) + 1.5;
        if (m.kaynak === 'tablo') ex += etiket('TABLO · SORULMAZ', ex, y0 + 2.3, INK3) + 1.5;
        if (m.kaynak === 'sekil') ex += etiket('ŞEKİL · SORULMAZ', ex, y0 + 2.3, INK3) + 1.5;
        if (m.klinik) ex += etiket('KLİNİK · SORULMAZ', ex, y0 + 2.3, INK3) + 1.5;
        if ((m.cikmis || []).length) etiket(`${m.cikmis!.length} ÇIKMIŞ`, ex, y0 + 2.3, [21, 122, 62]);
        y = y0 + 3.8;
        const sonuk = m.sinavUygun === false;
        zengin(m.bilgi, M + 13, CW - 14, 10, sonuk ? INK2 : INK, c);
        if (o.alt) for (const a of m.alt || []) madde(a, M + 14, CW - 15, 8.8, INK2, c);
        if (o.alinti) for (const a of m.alinti) { yer(5); zengin(`“${a.metin}” — s. ${a.sayfa}`, M + 14, CW - 15, 8, INK3); }
        if (o.detay) {
          y += 0.8;
          for (const s of String(m.detay || '').split('\n').map((x) => x.trim()).filter(Boolean)) {
            if (/^[-•]\s+/.test(s)) madde(s.replace(/^[-•]\s+/, ''), M + 14, CW - 15, 8.5, INK2, c);
            else zengin(s, M + 14, CW - 15, 8.5, INK2, c);
          }
        }
        if (o.ornekSoru && m.ornek_soru) {
          soruNo++; y += 1;
          zengin(`**Soru ${soruNo}.** ${m.ornek_soru.kok}`, M + 14, CW - 15, 8.8, INK);
          for (const [k, v] of Object.entries(m.ornek_soru.secenekler)) zengin(`${k}) ${v}`, M + 18, CW - 19, 8.5, INK2);
          anahtar.push(`${soruNo}: ${m.ornek_soru.dogru}${m.ornek_soru.aciklama ? ' — ' + m.ornek_soru.aciklama : ''}`);
        }
        if (o.cikmis) for (const id of m.cikmis || []) {
          const q = d.cikmis?.[id]; if (!q) continue;
          soruNo++; y += 1;
          zengin(`**Çıkmış ${soruNo}** (${q.sinav}). ${q.kok}`, M + 14, CW - 15, 8.8, INK);
          for (const [k, v] of Object.entries(q.secenekler)) zengin(`${k}) ${v}`, M + 18, CW - 19, 8.5, INK2);
          anahtar.push(`${soruNo}: ${q.dogru}`);
        }
        doc.setDrawColor(...LINE); doc.setLineWidth(0.2); yer(3); y += 1.5; doc.line(M + 13, y, W - M, y); y += 2.5;
      }
    }
    if (anahtar.length) {
      yer(12); y += 2; font('bold', 10, INK); doc.text(T('Cevap anahtarı'), M, y + 3); y += 6;
      for (const a of anahtar) zengin(a, M, CW, 8.3, INK2);
    }
  }
  altbilgi();
  return doc.output('blob');
}
