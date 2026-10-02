/**
 * generate_kurul6_amfi_ozetleri.mjs
 * 
 * C:\Users\indui\Desktop\meds_database\kurul_ders_notlari_txt\Kurul 6 altındaki
 * 53 adet amfi ders notunu okur; her bir ders notunun klinik, farmakolojik ve patolojik
 * özetini çıkararak C:\Users\indui\Desktop\meds_database\kurul_ders_notlari_ozet\Kurul 6
 * klasörüne Markdown (.md) olarak kaydeder ve master katalog indeksini
 * (kurul6_amfi_notlari_ozet_indeksi.json) oluşturur.
 */

import fs from 'fs';
import path from 'path';

const SRC_DIR = 'C:\\Users\\indui\\Desktop\\meds_database\\kurul_ders_notlari_txt\\Kurul 6';
const OUT_DIR = 'C:\\Users\\indui\\Desktop\\meds_database\\kurul_ders_notlari_ozet\\Kurul 6';

if (!fs.existsSync(OUT_DIR)) {
  fs.mkdirSync(OUT_DIR, { recursive: true });
}

function detectDepartment(filename, content) {
  const f = filename.toLowerCase();
  const c = content.toLowerCase();

  if (f.includes('ilaç') || f.includes('ilac') || f.includes('farm') || f.includes('antidiyabetik') || f.includes('antitiroid') || f.includes('adrenokortikosteroid') || f.includes('gonadal') || f.includes('ergot')) {
    return 'Tıbbi Farmakoloji';
  }
  if (f.includes('pat') || f.includes('tümör') || f.includes('neopl') || f.includes('tiroid_neopl') || f.includes('tiroiditis') || f.includes('adrenal_korteks') || f.includes('adrenokor') || f.includes('hipofiz_hast') || f.includes('hiper_hipo')) {
    return 'Tıbbi Patoloji';
  }
  if (f.includes('genetik') || f.includes('genetig') || f.includes('kalitsal metabolik') || f.includes('dismorfik')) {
    return 'Tıbbi Biyoloji ve Genetik';
  }
  if (f.includes('biyokimya') || f.includes('laboratuvar') || f.includes('paket test') || f.includes('hata kaynak')) {
    return 'Tıbbi Biyokimya';
  }
  if (f.includes('epidemiyoloji') || f.includes('bağışıklama') || f.includes('bagisiklama') || f.includes('çevre') || f.includes('cevre') || f.includes('mobing') || f.includes('sağlık göster')) {
    return 'Halk Sağlığı';
  }
  if (f.includes('cushing') || f.includes('hipoglisemi') || f.includes('diyabet') || f.includes('kalsiyum') || f.includes('paratiroid') || f.includes('endokrin') || f.includes('hipotalamo')) {
    return 'İç Hastalıkları (Endokrinoloji)';
  }
  if (f.includes('geriatri') || f.includes('yaşlılık') || f.includes('yaslilik') || f.includes('hareket sistemi')) {
    return 'İç Hastalıkları (Geriatri)';
  }
  if (f.includes('psikiyatri')) {
    return 'Ruh Sağlığı ve Hastalıkları';
  }

  return 'Endokrin, Metabolizma ve Yaşlanma';
}

function extractKeyPoints(text) {
  const lines = text.split('\n')
    .map(l => l.trim())
    .filter(l => l.length > 25 && !l.startsWith('http') && !l.includes('www.') && !/^[0-9\s\.\-_]+$/.test(l));

  const points = [];
  const visited = new Set();

  for (const line of lines) {
    if (points.length >= 8) break;
    const lower = line.toLowerCase();
    if (
      lower.includes('tanı') || lower.includes('tedavi') || lower.includes('en sık') ||
      lower.includes('klinik') || lower.includes('belirti') || lower.includes('bulgu') ||
      lower.includes('etiyoloji') || lower.includes('etken') || lower.includes('prognoz') ||
      lower.includes('mutasyon') || lower.includes('evre') || lower.includes('komplikasyon') ||
      lower.includes('kriter') || lower.includes('patoloji') || lower.includes('mekanizma') ||
      lower.includes('özellik') || lower.includes('risk') || lower.includes('ilaç') ||
      lower.includes('hormon') || lower.includes('tümör') || lower.includes('sendrom')
    ) {
      const clean = line.replace(/[•\-\*\t\r]/g, ' ').replace(/\s+/g, ' ').trim();
      if (!visited.has(clean) && clean.length > 20 && clean.length < 350) {
        visited.add(clean);
        points.push(clean);
      }
    }
  }

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
  console.log('⚡ Kurul 6 Amfi Notları Taranıyor...');
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
    md += `**Dönem/Kurul:** Dönem 3 · Kurul 6 (Endokrin, Metabolizma ve Yaşlanma)\n`;
    md += `**Ders/Branş:** ${dept}\n`;
    md += `**Orijinal Belge:** ${file}\n\n`;
    md += `## Temel Klinik ve Sınav Odaklı Özet Bilgiler\n\n`;

    keyPoints.forEach((pt, pIdx) => {
      md += `${pIdx + 1}. ${pt}\n\n`;
    });

    fs.writeFileSync(outFilePath, md, 'utf8');

    indexList.push({
      id: `k6-note-${String(i + 1).padStart(3, '0')}`,
      originalFile: file,
      title: title,
      department: dept,
      kurul: 'Dönem 3 Kurul 6',
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
    kurul: 'Dönem 3 Kurul 6 (TIP 360 - Endokrin, Metabolizma ve Yaşlanma)',
    generatedAt: new Date().toISOString(),
    toplamDersNotu: indexList.length,
    dersler: indexList
  };

  fs.writeFileSync(
    path.join(OUT_DIR, 'kurul6_amfi_notlari_ozet_indeksi.json'),
    JSON.stringify(indexList, null, 2),
    'utf8'
  );

  console.log(`\n🎉 Tüm ${files.length} Kurul 6 amfi ders notu özetlendi ve indeks dosyası kaydedildi: ${OUT_DIR}`);
}

run().catch(err => {
  console.error('Hata:', err);
  process.exit(1);
});
