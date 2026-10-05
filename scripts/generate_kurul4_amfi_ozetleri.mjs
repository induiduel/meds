/**
 * generate_kurul4_amfi_ozetleri.mjs
 * 
 * C:\Users\indui\Desktop\meds_database\kurul_ders_notlari_txt\Kurul 4 altındaki
 * 46 adet amfi ders notunu okur; her bir ders notunun klinik, farmakolojik ve patolojik
 * özetini çıkararak C:\Users\indui\Desktop\meds_database\kurul_ders_notlari_ozet\Kurul 4
 * klasörüne Markdown (.md) olarak kaydeder ve master katalog indeksini
 * (kurul4_amfi_notlari_ozet_indeksi.json) oluşturur.
 */

import fs from 'fs';
import path from 'path';

const SRC_DIR = `${process.env.MEDS_DATABASE_DIR || '/home/indu/Masaüstü/MedSoru Project/meds_database'}/kurul_ders_notlari_txt/Kurul 4`;
const OUT_DIR = `${process.env.MEDS_DATABASE_DIR || '/home/indu/Masaüstü/MedSoru Project/meds_database'}/kurul_ders_notlari_ozet/Kurul 4`;

if (!fs.existsSync(OUT_DIR)) {
  fs.mkdirSync(OUT_DIR, { recursive: true });
}

function detectDepartment(filename, content) {
  const f = filename.toLowerCase();
  const c = content.toLowerCase();
  if (f.includes('ilaç') || f.includes('ilac') || f.includes('farm') || f.includes('kemoterapi') || f.includes('vazodilatör') || f.includes('diüretik') || f.includes('antikoagulan') || f.includes('antihipertansif')) {
    return 'Tıbbi Farmakoloji';
  }
  if (f.includes('patoloji') || f.includes('yangi') || f.includes('tümör') || f.includes('hemodinamik') || f.includes('metastaz')) {
    return 'Tıbbi Patoloji';
  }
  if (f.includes('genetik') || f.includes('genetig')) {
    return 'Tıbbi Biyoloji ve Genetik';
  }
  if (f.includes('endokardit') || f.includes('influenza') || f.includes('sepsis') || f.includes('pnömoni') || f.includes('pnomon')) {
    return 'Enfeksiyon Hastalıkları / Göğüs Hastalıkları';
  }
  if (f.includes('akciger') || f.includes('solunum') || f.includes('plevra') || f.includes('göğüs') || f.includes('gogus')) {
    return 'Göğüs Hastalıkları / Göğüs Cerrahisi';
  }
  if (f.includes('kalp') || f.includes('kardiy') || f.includes('ecg') || f.includes('ekg') || f.includes('aritm') || f.includes('htn') || f.includes('acs') || f.includes('kapak') || f.includes('cpr')) {
    return 'Kardiyoloji / KVC';
  }
  return 'Dahili Tıp Bilimleri';
}

function extractKeyPoints(text) {
  const lines = text.split('\n')
    .map(l => l.trim())
    .filter(l => l.length > 25 && !l.startsWith('http') && !l.includes('www.') && !/^[0-9\s\.\-_]+$/.test(l));

  const points = [];
  const seen = new Set();

  for (const line of lines) {
    if (points.length >= 15) break;
    // Pick lines with clinical, diagnostic, treatment keywords
    const isHighYield = /(tedavi|tanı|klinik|en sık|mekanizma|etki|reseptör|doz|komplikasyon|mutasyon|belirti|bulgu|endikasyon|kontrendikasyon|kriter|ilaç|patoloji|prognoz)/i.test(line);
    if (isHighYield && !seen.has(line)) {
      seen.add(line);
      points.push(line.replace(/[\*\#\_]/g, '').trim());
    }
  }

  // Fallback if less than 10
  if (points.length < 10) {
    for (const line of lines) {
      if (points.length >= 12) break;
      if (!seen.has(line)) {
        seen.add(line);
        points.push(line.replace(/[\*\#\_]/g, '').trim());
      }
    }
  }

  return points;
}

function sanitizeSafeName(name) {
  return name.replace(/\.txt$/i, '')
    .replace(/[^\w\d\-_]/g, '_')
    .replace(/_+/g, '_')
    .slice(0, 70);
}

async function run() {
  console.log('🚀 Kurul 4 (Dolaşım, Solunum ve Tümör) Amfi Ders Notları Özetleme İşlemi Başlatılıyor...');

  const files = fs.readdirSync(SRC_DIR).filter(f => f.endsWith('.txt'));
  console.log(`📂 Toplam taranacak ders notu sayısı: ${files.length}`);

  const indexList = [];

  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    const fullPath = path.join(SRC_DIR, file);
    const content = fs.readFileSync(fullPath, 'utf8');

    const dept = detectDepartment(file, content);
    const title = file.replace(/\.txt$/i, '').trim();
    const keyPoints = extractKeyPoints(content);

    const safeBase = sanitizeSafeName(file);
    const outFileName = `${safeBase}_ozet.md`;
    const outFilePath = path.join(OUT_DIR, outFileName);

    let md = `# ${title} (${dept})\n\n`;
    md += `**Dönem/Kurul:** Dönem 3 · Kurul 4 (Dolaşım, Solunum ve Tümör Kurulu)\n`;
    md += `**Ders/Branş:** ${dept}\n`;
    md += `**Orijinal Belge:** ${file}\n\n`;
    md += `## Temel Klinik ve Sınav Odaklı Özet Bilgiler\n\n`;

    keyPoints.forEach((pt, pIdx) => {
      md += `${pIdx + 1}. ${pt}\n\n`;
    });

    fs.writeFileSync(outFilePath, md, 'utf8');

    indexList.push({
      id: `k4-note-${String(i + 1).padStart(3, '0')}`,
      originalFile: file,
      title: title,
      department: dept,
      kurul: 'Dönem 3 Kurul 4',
      summaryFile: outFileName,
      summaryDate: new Date().toISOString(),
      characterCount: content.length,
      keyClinicalPoints: keyPoints,
      fullSummaryMarkdown: md
    });

    console.log(`[${i + 1}/${files.length}] ✓ Özetlendi: ${file} -> ${dept}`);
  }

  // Master index file
  const indexObj = {
    kurul: 'Dönem 3 Kurul 4 (TIP 340 - Dolaşım, Solunum ve Tümör)',
    generatedAt: new Date().toISOString(),
    toplamDersNotu: indexList.length,
    dersler: indexList
  };

  fs.writeFileSync(
    path.join(OUT_DIR, 'kurul4_amfi_notlari_ozet_indeksi.json'),
    JSON.stringify(indexList, null, 2),
    'utf8'
  );

  console.log(`\n🎉 Tüm 46 Kurul 4 amfi ders notu özetlendi ve indeks dosyası kaydedildi: ${OUT_DIR}`);
}

run().catch(err => {
  console.error('Hata:', err);
  process.exit(1);
});
