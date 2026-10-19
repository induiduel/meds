/**
 * Kurul 1 Tıbbi Biyoloji ve Genetik — Sınav Kalıbı, Aşama Aşama Ders Anlatıcısı ve Check Up PDF Motoru.
 * Sayfadaki tüm içerikleri (Aşama aşama doktor ders anlatımı, 10 karşılaştırma tablosu, 65 tek satırlık spot,
 * 31 soru-cevap ve 45 çıkmış/örnek soru + şık açıklamaları) Türkçe karakter destekli (Liberation Sans) A4 PDF'e çevirir.
 */
import { setupPdfFonts } from '../../services/drive';
import {
  GENETIK_BOLUMLER,
  GENETIK_SORU_CEVAPLAR,
  GENETIK_SORULAR,
  GENETIK_SPOTLAR,
  GENETIK_TABLOLAR,
} from './genetikCheckupVeri';
import g07Data from '../../data/genetik_asistan/g07.json';

export type GenetikPdfMod = 'tam' | 'anlatim' | 'spot' | 'soru';

export const GENETIK_PDF_MODLAR: { id: GenetikPdfMod; baslik: string; aciklama: string }[] = [
  {
    id: 'tam',
    baslik: 'Tam Genetik Check Up Kitapçığı (Tüm İçerik)',
    aciklama: 'Aşama aşama doktor ders anlatımı + 10 karşılaştırma tablosu + 65 tek satırlık spot + 31 soru-cevap + 45 çıkmış/örnek soru ve çözümleri.',
  },
  {
    id: 'anlatim',
    baslik: 'Aşama Aşama Ders Anlatım Notu & Tablolar',
    aciklama: 'Sesli ders anlatıcısının adım adım doktor anlatım metinleri, spot kuralları, 10 ayırıcı tanı tablosu ve 65 tek satırlık spot.',
  },
  {
    id: 'spot',
    baslik: 'Son Gece Hızlı Tekrar Özeti (Tablo + Spot + Soru-Cevap)',
    aciklama: '10 karşılaştırma tablosu + 65 tek satırlık nokta atışı bilgi cümlesi + 31 hızlı soru-cevap kartı.',
  },
  {
    id: 'soru',
    baslik: 'Çıkmış & Örnek Genetik Soru Kitapçığı (45 Soru + Çözümler)',
    aciklama: '19 çıkmış genetik sorusu ve 26 sınav kalıbı örnek sorusu + sonunda ayrıntılı çözümlü cevap anahtarı.',
  },
];

type RGB = [number, number, number];
const INK: RGB = [15, 23, 42];
const INK2: RGB = [51, 65, 85];
const INK3: RGB = [100, 116, 139];
const TEAL: RGB = [13, 148, 136];
const BLUE: RGB = [29, 78, 216];
const AMBER: RGB = [180, 83, 9];
const GREEN: RGB = [21, 128, 61];
const LINE: RGB = [203, 213, 225];
const SOFT_BG: RGB = [241, 245, 249];
const SPOT_BG: RGB = [240, 253, 250];
const WARN_BG: RGB = [254, 243, 199];

const SYM_MAP: Record<string, string> = {
  '↑': '(Artar) ',
  '↓': '(Azalır) ',
  '→': ' -> ',
  '←': ' <- ',
  '⁺': '+',
  '⁻': '-',
  '⁰': '0',
  '¹': '1',
  '²': '2',
  '³': '3',
  '⁴': '4',
  '⁵': '5',
  '⁶': '6',
  '⁷': '7',
  '⁸': '8',
  '⁹': '9',
  '₀': '0',
  '₁': '1',
  '₂': '2',
  '₃': '3',
  '₄': '4',
  '★': '*',
};

const cleanMd = (s: string) =>
  String(s || '')
    .replace(/\*\*([^*]+)\*\*/g, '$1')
    .replace(/[↑↓→←⁺⁻⁰-⁹₀-₄★]/g, (c) => SYM_MAP[c] || c);

export async function genetikCheckupPdfIndir(mod: GenetikPdfMod = 'tam'): Promise<{ sayfa: number; dosyaAdi: string }> {
  const { jsPDF } = await import('jspdf');
  const doc = new jsPDF({ unit: 'mm', format: 'a4', orientation: 'portrait', compress: true });
  const { font: F, T: T0 } = await setupPdfFonts(doc);
  const T = (x: string) => T0(cleanMd(x));

  const W = doc.internal.pageSize.getWidth();
  const H = doc.internal.pageSize.getHeight();
  const M = 13;
  const CW = W - 2 * M;
  const TOP = 16;
  const BOT = H - 14;
  let y = TOP;
  let aktifBolumBaslik = 'Kurul 1 Tıbbi Biyoloji ve Genetik Check Up';

  const yeniSayfa = () => {
    doc.addPage();
    y = TOP;
  };

  const alanKontrol = (gereken: number) => {
    if (y + gereken > BOT) yeniSayfa();
  };

  const paragrafYaz = (
    metin: string,
    opts: {
      size?: number;
      style?: 'normal' | 'bold' | 'italic';
      color?: RGB;
      indent?: number;
      width?: number;
      lineGap?: number;
    } = {},
  ) => {
    const size = opts.size ?? 9.5;
    const style = opts.style ?? 'normal';
    const color = opts.color ?? INK;
    const indent = opts.indent ?? 0;
    const width = opts.width ?? CW - indent;
    const lh = size * (opts.lineGap ?? 0.42);

    doc.setFont(F, style);
    doc.setFontSize(size);
    doc.setTextColor(...color);
    const lines: string[] = doc.splitTextToSize(T(metin), width);
    for (const ln of lines) {
      alanKontrol(lh + 1);
      doc.text(ln, M + indent, y);
      y += lh;
    }
  };

  const bolumBasligi = (no: string, baslik: string, altAciklama?: string, renk: RGB = TEAL) => {
    alanKontrol(18);
    y += 2;
    doc.setFillColor(...renk);
    doc.roundedRect(M, y, CW, 8.5, 1.5, 1.5, 'F');
    doc.setFont(F, 'bold');
    doc.setFontSize(10.5);
    doc.setTextColor(255, 255, 255);
    doc.text(T(`${no}  ${baslik}`), M + 3, y + 5.7);
    y += 11;
    aktifBolumBaslik = baslik;
    if (altAciklama) {
      paragrafYaz(altAciklama, { size: 8.8, style: 'italic', color: INK2 });
      y += 2;
    }
  };

  // --- KAPAK / ÜST BANNER ---
  doc.setFillColor(15, 23, 42);
  doc.roundedRect(M, y, CW, 26, 2.5, 2.5, 'F');
  doc.setFont(F, 'bold');
  doc.setFontSize(8.5);
  doc.setTextColor(94, 234, 212);
  doc.text(T('KURUL 1 · TIBBİ BİYOLOJİ VE GENETİK · SINAV KALIBI & CHECK UP'), M + 4, y + 6.5);

  doc.setFont(F, 'bold');
  doc.setFontSize(14);
  doc.setTextColor(255, 255, 255);
  const modObj = GENETIK_PDF_MODLAR.find((m) => m.id === mod) || GENETIK_PDF_MODLAR[0];
  doc.text(T(modObj.baslik), M + 4, y + 14);

  doc.setFont(F, 'normal');
  doc.setFontSize(8.5);
  doc.setTextColor(203, 213, 225);
  doc.text(
    T('1) Hangi bulgu hangi sendromu düşündürür?   2) Kanser türlerinde hedef ilaçlar   3) Spesifik genetik & biyokimyasal belirteçler'),
    M + 4,
    y + 21,
  );
  y += 31;

  // =========================================================================
  // 1. AŞAMA AŞAMA DOKTOR DERS ANLATIMI (g07)
  // =========================================================================
  if (mod === 'tam' || mod === 'anlatim') {
    bolumBasligi(
      'BÖLÜM A',
      'Aşama Aşama Doktor Ders Anlatımı ve Sınav Vurguları',
      'Sesli ders anlatıcısındaki 5 bölüm ve 11 aşamanın tam metni, spot kuralları ve klinik korelasyonları.',
      TEAL,
    );

    g07Data.bolumler.forEach((b, bi) => {
      alanKontrol(14);
      y += 1.5;
      doc.setFillColor(...SOFT_BG);
      doc.setDrawColor(...LINE);
      doc.roundedRect(M, y, CW, 7, 1, 1, 'FD');
      doc.setFont(F, 'bold');
      doc.setFontSize(9.8);
      doc.setTextColor(...BLUE);
      doc.text(T(`${bi + 1}. Bölüm: ${b.baslik}`), M + 2.5, y + 4.8);
      y += 9;
      paragrafYaz(b.neden, { size: 8.6, style: 'italic', color: INK2, indent: 1 });
      y += 2;

      const bNoktalar = g07Data.noktalar.filter((n) => n.bolum === bi);
      bNoktalar.forEach((n, ni) => {
        alanKontrol(22);
        doc.setFont(F, 'bold');
        doc.setFontSize(9.6);
        doc.setTextColor(...INK);
        doc.text(T(`Aşama ${bi + 1}.${ni + 1} — ${n.baslik}`), M + 1, y);
        y += 4.5;

        // Spot bilgi kutusu
        doc.setFont(F, 'bold');
        doc.setFontSize(8.5);
        const spotLines: string[] = doc.splitTextToSize(T(`SINAV SPOTU: ${n.bilgi}`), CW - 6);
        const boxH = spotLines.length * 3.7 + 3.5;
        alanKontrol(boxH + 3);
        doc.setFillColor(...SPOT_BG);
        doc.setDrawColor(...TEAL);
        doc.roundedRect(M + 1, y - 2.5, CW - 2, boxH, 1, 1, 'FD');
        doc.setTextColor(...TEAL);
        let sy = y + 1;
        for (const sl of spotLines) {
          doc.text(sl, M + 3.5, sy);
          sy += 3.7;
        }
        y += boxH + 1.5;

        // Anlatım cümleleri
        for (const cm of n.cumleler) {
          paragrafYaz(`• ${cm}`, { size: 9, style: 'normal', color: INK, indent: 2.5 });
          y += 0.8;
        }
        y += 2.5;
      });
    });
  }

  // =========================================================================
  // 2. 10 HIZLI KARŞILAŞTIRMA TABLOSU
  // =========================================================================
  if (mod === 'tam' || mod === 'anlatim' || mod === 'spot') {
    bolumBasligi(
      'BÖLÜM B',
      '10 Hızlı Ayırıcı Tanı, Sendrom, Hedef İlaç ve Belirteç Tablosu',
      'Sınavda en sık karşılaştırılan sendromlar, kanser ilaçları ve prenatal tanı belirteçleri.',
      BLUE,
    );

    GENETIK_TABLOLAR.forEach((tb, ti) => {
      alanKontrol(24);
      y += 1.5;
      doc.setFont(F, 'bold');
      doc.setFontSize(9.6);
      doc.setTextColor(...BLUE);
      doc.text(T(`Tablo ${ti + 1}: ${tb.baslik}`), M, y);
      y += 4;
      paragrafYaz(tb.aciklama, { size: 8.3, style: 'italic', color: INK2 });
      y += 1.5;

      const colCount = tb.sutunlar.length;
      const colW = CW / colCount;

      // Tablo başlığı
      alanKontrol(8);
      doc.setFillColor(30, 41, 59);
      doc.rect(M, y, CW, 6.2, 'F');
      doc.setFont(F, 'bold');
      doc.setFontSize(8);
      doc.setTextColor(255, 255, 255);
      tb.sutunlar.forEach((st, ci) => {
        const stLines: string[] = doc.splitTextToSize(T(st), colW - 3);
        doc.text(stLines[0] || '', M + ci * colW + 1.5, y + 4.2);
      });
      y += 6.2;

      // Tablo satırları
      tb.satirlar.forEach((row, ri) => {
        doc.setFont(F, 'normal');
        doc.setFontSize(7.9);
        const cellLines = row.map((cell) => doc.splitTextToSize(T(cell), colW - 3) as string[]);
        const maxLines = Math.max(...cellLines.map((cl) => cl.length), 1);
        const rowH = maxLines * 3.4 + 2.4;

        if (y + rowH > BOT) {
          yeniSayfa();
          doc.setFillColor(30, 41, 59);
          doc.rect(M, y, CW, 6.2, 'F');
          doc.setFont(F, 'bold');
          doc.setFontSize(8);
          doc.setTextColor(255, 255, 255);
          tb.sutunlar.forEach((st, ci) => {
            const stLines: string[] = doc.splitTextToSize(T(st), colW - 3);
            doc.text(stLines[0] || '', M + ci * colW + 1.5, y + 4.2);
          });
          y += 6.2;
        }

        if (ri % 2 === 1) {
          doc.setFillColor(...SOFT_BG);
          doc.rect(M, y, CW, rowH, 'F');
        }
        doc.setDrawColor(...LINE);
        doc.rect(M, y, CW, rowH, 'S');

        cellLines.forEach((cl, ci) => {
          doc.setFont(F, ci === 0 ? 'bold' : 'normal');
          doc.setFontSize(7.9);
          doc.setTextColor(...(ci === 0 ? INK : INK2));
          cl.forEach((ln, li) => {
            doc.text(ln, M + ci * colW + 1.5, y + 3.5 + li * 3.4);
          });
        });
        y += rowH;
      });
      y += 4;
    });
  }

  // =========================================================================
  // 3. 65 TEK SATIRLIK NOKTA ATIŞI SPOT BİLGİ CÜMLESİ
  // =========================================================================
  if (mod === 'tam' || mod === 'anlatim' || mod === 'spot') {
    bolumBasligi(
      'BÖLÜM C',
      `${GENETIK_SPOTLAR.length} Tek Satırlık Nokta Atışı Spot Bilgi Cümlesi`,
      'Hocanın ders slaytlarından ve çıkmış sınav kalıplarından süzülmüş tek cümlelik sınav spotları.',
      AMBER,
    );

    GENETIK_BOLUMLER.forEach((b) => {
      const bSpotlar = GENETIK_SPOTLAR.filter((s) => s.bolum === b.id);
      if (!bSpotlar.length) return;
      alanKontrol(12);
      y += 1.5;
      doc.setFont(F, 'bold');
      doc.setFontSize(9.5);
      doc.setTextColor(...AMBER);
      doc.text(T(`${b.kisa} — ${b.ad} (${bSpotlar.length} Spot)`), M, y);
      y += 4.5;

      bSpotlar.forEach((sp, si) => {
        const prefix = `${si + 1}. [${sp.etiket}${sp.cikmisYil ? ' · ÇIKMIŞ ' + sp.cikmisYil : ''}] `;
        paragrafYaz(`${prefix}${sp.cumle}`, { size: 8.6, style: 'normal', color: INK, indent: 1.5 });
        y += 1.2;
      });
      y += 2;
    });
  }

  // =========================================================================
  // 4. 31 HIZLI SINAV SORU - CEVAP KARTI
  // =========================================================================
  if (mod === 'tam' || mod === 'spot') {
    bolumBasligi(
      'BÖLÜM D',
      `${GENETIK_SORU_CEVAPLAR.length} Nokta Atışı Sınav Soru – Cevap Kartı`,
      'Bulgu -> Sendrom, Kanser -> Hedef İlaç ve Spesifik Belirteç kalıpları için hızlı soru-cevaplar.',
      GREEN,
    );

    GENETIK_SORU_CEVAPLAR.forEach((sc, idx) => {
      alanKontrol(14);
      paragrafYaz(`S${idx + 1} [${sc.odak}]: ${sc.soru}`, { size: 8.8, style: 'bold', color: INK });
      paragrafYaz(`Cevap: ${sc.cevap}`, { size: 8.6, style: 'normal', color: GREEN, indent: 3 });
      if (sc.ipucu) {
        paragrafYaz(`Klinik/Sınav Vurgusu: ${sc.ipucu}`, { size: 8.1, style: 'italic', color: INK2, indent: 3 });
      }
      y += 2;
    });
  }

  // =========================================================================
  // 5. 45 ÇIKMIŞ VE ÖRNEK GENETİK SORUSU + ÇÖZÜMLERİ
  // =========================================================================
  if (mod === 'tam' || mod === 'soru') {
    const cikmisCount = GENETIK_SORULAR.filter((q) => q.tur === 'cikmis').length;
    const ornekCount = GENETIK_SORULAR.filter((q) => q.tur === 'ornek').length;

    bolumBasligi(
      'BÖLÜM E',
      `Çıkmış (${cikmisCount}) ve Örnek (${ornekCount}) Genetik Soruları ve Çözümleri`,
      'Soruların hemen altında doğru yanıt, klinik spot ve tüm şıkların neden doğru/yanlış olduğu açıklanmıştır.',
      BLUE,
    );

    GENETIK_SORULAR.forEach((q, qi) => {
      alanKontrol(32);
      const etiket = q.tur === 'cikmis' ? `ÇIKMIŞ SORU · ${q.yil || 'Kurul 1'}` : 'ÖRNEK SINAV SORUSU';
      doc.setFillColor(...(q.tur === 'cikmis' ? WARN_BG : SOFT_BG));
      doc.roundedRect(M, y - 3, CW, 5.5, 1, 1, 'F');
      doc.setFont(F, 'bold');
      doc.setFontSize(8);
      doc.setTextColor(...(q.tur === 'cikmis' ? AMBER : BLUE));
      doc.text(T(`SORU ${qi + 1}  |  ${etiket}  |  ${q.kalipEtiketi}`), M + 2, y + 0.8);
      y += 5;

      paragrafYaz(q.kok, { size: 9, style: 'bold', color: INK });
      y += 1;

      (['A', 'B', 'C', 'D', 'E'] as const).forEach((h) => {
        const sec = q.secenekler[h];
        if (!sec) return;
        const isDogru = q.dogru === h;
        paragrafYaz(`${h}) ${sec}`, {
          size: 8.6,
          style: isDogru ? 'bold' : 'normal',
          color: isDogru ? GREEN : INK,
          indent: 3,
        });
      });

      y += 1;
      paragrafYaz(`Doğru Cevap: ${q.dogru}  |  Spot: ${q.spotCikarim}`, {
        size: 8.3,
        style: 'bold',
        color: TEAL,
        indent: 2,
      });
      paragrafYaz(`Açıklama: ${q.aciklama}`, {
        size: 8.1,
        style: 'normal',
        color: INK2,
        indent: 2,
      });
      (['A', 'B', 'C', 'D', 'E'] as const).forEach((h) => {
        const sa = q.sikAciklamalari?.[h];
        if (!sa) return;
        paragrafYaz(`• ${h} şıkkı: ${sa}`, {
          size: 7.8,
          style: q.dogru === h ? 'bold' : 'normal',
          color: q.dogru === h ? GREEN : INK3,
          indent: 4,
        });
      });
      y += 3;
    });
  }

  // --- ÜST VE ALT BİLGİ (SAYFA NUMARALARI) ---
  const toplamSayfa = doc.getNumberOfPages();
  for (let p = 1; p <= toplamSayfa; p++) {
    doc.setPage(p);
    doc.setDrawColor(...LINE);
    doc.line(M, 11, W - M, 11);
    doc.setFont(F, 'normal');
    doc.setFontSize(7.5);
    doc.setTextColor(...INK3);
    doc.text(T('MeDSor · Kurul 1 Tıbbi Biyoloji ve Genetik Sınav Kalıbı & Sesli Ders Anlatıcısı'), M, 9.2);
    doc.text(T(modObj.baslik), W - M, 9.2, { align: 'right' });

    doc.line(M, H - 10, W - M, H - 10);
    doc.text(T('Bulgu -> Sendrom · Kanser Hedef İlaçları · Spesifik Belirteçler'), M, H - 6.2);
    doc.setFont(F, 'bold');
    doc.text(T(`Sayfa ${p} / ${toplamSayfa}`), W - M, H - 6.2, { align: 'right' });
  }

  const dosyaAdi = `Kurul1_Genetik_CheckUp_${mod}_${new Date().toISOString().slice(0, 10)}.pdf`;
  doc.save(dosyaAdi);
  return { sayfa: toplamSayfa, dosyaAdi };
}
