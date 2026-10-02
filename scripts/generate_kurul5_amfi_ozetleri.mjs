/**
 * generate_kurul5_amfi_ozetleri.mjs
 * 
 * C:\Users\indui\Desktop\meds_database\kurul_ders_notlari_txt\Kurul 5 altındaki
 * 75 adet amfi ders notunu okur; her bir ders notunun klinik, farmakolojik ve patolojik
 * özetini çıkararak C:\Users\indui\Desktop\meds_database\kurul_ders_notlari_ozet\Kurul 5
 * klasörüne Markdown (.md) olarak kaydeder ve master katalog indeksini
 * (kurul5_amfi_notlari_ozet_indeksi.json) oluşturur.
 */

import fs from 'fs';
import path from 'path';

const SRC_DIR = 'C:\\Users\\indui\\Desktop\\meds_database\\kurul_ders_notlari_txt\\Kurul 5';
const OUT_DIR = 'C:\\Users\\indui\\Desktop\\meds_database\\kurul_ders_notlari_ozet\\Kurul 5';

if (!fs.existsSync(OUT_DIR)) {
  fs.mkdirSync(OUT_DIR, { recursive: true });
}

function detectDepartment(filename, content) {
  const f = filename.toLowerCase();
  const c = content.toLowerCase();

  if (f.includes('farmakoloji') || f.includes('ilaç') || f.includes('ilac') || f.includes('homeostazis') || f.includes('mineralizasyon')) {
    return 'Tıbbi Farmakoloji';
  }
  if (f.includes('pat') || f.includes('tümör') || f.includes('tumor') || f.includes('myeloid') || f.includes('lenfoid') || f.includes('eritros') || f.includes('deri_') || f.includes('kemik_kikirdak') || f.includes('osteonekroz') || f.includes('artrit')) {
    return 'Tıbbi Patoloji';
  }
  if (f.includes('genetik') || f.includes('genetig') || f.includes('lenfomalarda genetik') || f.includes('lösemilerde genetik')) {
    return 'Tıbbi Biyoloji ve Genetik';
  }
  if (f.includes('sağlık') || f.includes('saglik') || f.includes('meslek') || f.includes('sosyalleş') || f.includes('egitim')) {
    return 'Halk Sağlığı';
  }
  if (f.includes('anemi') || f.includes('demir') || f.includes('megaloblastik') || f.includes('hemolitik') || f.includes('hemostaz') || f.includes('hemoglobinopat')) {
    return 'İç Hastalıkları (Hematoloji)';
  }
  if (f.includes('kırık') || f.includes('kirik') || f.includes('ortopedi') || f.includes('travma') || f.includes('diskitis') || f.includes('pott') || f.includes('anomali') || f.includes('osteomalazi')) {
    return 'Ortopedi ve Travmatoloji';
  }
  if (f.includes('ftr') || f.includes('ekstremite') || f.includes('muayene') || f.includes('bel ağrı') || f.includes('servikal') || f.includes('non - farmakolojik')) {
    return 'Fiziksel Tıp ve Rehabilitasyon';
  }
  if (f.includes('acil') || f.includes('senkop') || f.includes('ikyd') || f.includes('crush') || f.includes('zehirlenme') || f.includes('ani kardiyak')) {
    return 'Acil Tıp';
  }
  if (f.includes('kırım kongo') || f.includes('enfeksiyon')) {
    return 'Enfeksiyon Hastalıkları';
  }
  if (f.includes('kafa travma') || f.includes('beyin')) {
    return 'Beyin ve Sinir Cerrahisi';
  }
  if (f.includes('çocuk') || f.includes('cocuk')) {
    return 'Çocuk Sağlığı ve Hastalıkları';
  }

  return 'Kas-İskelet ve Hematopoetik Sistem';
}

function extractKeyPoints(text) {
  const lines = text.split('\n')
    .map(l => l.trim())
    .filter(l => l.length > 25 && !l.startsWith('http') && !l.includes('www.') && !/^[0-9\s\.\-_]+$/.test(l));

  const points = [];
  const visited = new Set();

  for (const line of lines) {
    if (points.length >= 8) break;
    // Look for clinical / diagnostic keywords
    const lower = line.toLowerCase();
    if (
      lower.includes('tanı') || lower.includes('tedavi') || lower.includes('en sık') ||
      lower.includes('klinik') || lower.includes('belirti') || lower.includes('bulgu') ||
      lower.includes('etiyoloji') || lower.includes('etken') || lower.includes('prognoz') ||
      lower.includes('mutasyon') || lower.includes('evre') || lower.includes('komplikasyon') ||
      lower.includes('kriter') || lower.includes('patoloji') || lower.includes('mekanizma') ||
      lower.includes('özellik') || lower.includes('risk') || lower.includes('ilaç') ||
      lower.includes('sendrom') || lower.includes('hücre') || lower.includes('morfoloji')
    ) {
      const clean = line.replace(/[•\-\*\t\r]/g, ' ').replace(/\s+/g, ' ').trim();
      if (!visited.has(clean) && clean.length > 20 && clean.length < 350) {
        visited.add(clean);
        points.push(clean);
      }
    }
  }

  // If not enough points, take meaningful long lines
  if (points.length < 4) {
    for (const line of lines) {
      if (points.length >= 6) break;
      const clean = line.replace(/[•\-\*\t\r]/g, ' ').replace(/\s+/g, ' ').trim();
      if (!visited.has(clean) && clean.length > 35 && clean.length < 300) {
        visited.add(clean);
        points.push(clean);
      }
    }
  }

  return points;
}

function sanitizeSafeName(name) {
  return name.replace(/\.txt$/i, '')
    .replace(/[^a-zA-Z0-9_\u00C0-\u017F\-]/g, '_')
    .replace(/_+/g, '_')
    .replace(/^_+|_+$/g, '');
}

async function run() {
  console.log('⚡ Kurul 5 Amfi Notları Taranıyor...');
  const files = fs.readdirSync(SRC_DIR).filter(f => f.toLowerCase().endsWith('.txt'));
  console.log(`Bulunan ders notu sayısı: ${files.length}`);

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
    md += `**Dönem/Kurul:** Dönem 3 · Kurul 5 (Ortopedi, Travmatoloji ve Hematopoetik Sistem)\n`;
    md += `**Ders/Branş:** ${dept}\n`;
    md += `**Orijinal Belge:** ${file}\n\n`;
    md += `## Temel Klinik ve Sınav Odaklı Özet Bilgiler\n\n`;

    keyPoints.forEach((pt, pIdx) => {
      md += `${pIdx + 1}. ${pt}\n\n`;
    });

    fs.writeFileSync(outFilePath, md, 'utf8');

    indexList.push({
      id: `k5-note-${String(i + 1).padStart(3, '0')}`,
      originalFile: file,
      title: title,
      department: dept,
      kurul: 'Dönem 3 Kurul 5',
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
    kurul: 'Dönem 3 Kurul 5 (TIP 350 - Ortopedi, Travmatoloji ve Hematopoetik Sistem)',
    generatedAt: new Date().toISOString(),
    toplamDersNotu: indexList.length,
    dersler: indexList
  };

  fs.writeFileSync(
    path.join(OUT_DIR, 'kurul5_amfi_notlari_ozet_indeksi.json'),
    JSON.stringify(indexList, null, 2),
    'utf8'
  );

  console.log(`\n🎉 Tüm ${files.length} Kurul 5 amfi ders notu özetlendi ve indeks dosyası kaydedildi: ${OUT_DIR}`);
}

run().catch(err => {
  console.error('Hata:', err);
  process.exit(1);
});
