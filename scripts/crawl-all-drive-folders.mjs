import fs from 'fs';
import https from 'https';

const TARGET_FOLDERS = [
  { name: '1) Çıkmışlar (Kurul 1-6 & Final)', id: '18U1LZVvV0VROcWVQTDBeJYwdBWiEIVwS' },
  { name: '2) 25-26 Dönem 3 Çıkmışları', id: '1VJwhDITJWZFaaBTvMajnLUzII31r1GTp' },
  { name: '3) 3. Dönem', id: '1AZaRbCpIUKtv0t6sg3VaZHC42NmbrnB4' },
  { name: '4) Çıkmış Sorular', id: '16ianUX4Nnl-dU9SZOSOgvDDuEaM1x6vZ' },
  { name: '5) 3. Sınıf', id: '1FAqqW0iAeg3NNjkPBeY3zG9X4FXaJuVM' },
  { name: '6) Dönem 3 Çıkmış Toplama', id: '1QKbD3800KBa3AUWP8apMSiKCMV0jiA21' },
];

// Helper to crawl a folder by its Google Drive folder ID
async function crawlFolder(folderId, pathPrefix = '', visited = new Set()) {
  if (visited.has(folderId)) return [];
  visited.add(folderId);

  const url = `https://drive.google.com/drive/folders/${folderId}`;
  try {
    const res = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
      }
    });

    if (!res.ok) {
      console.warn(`[Crawl] HTTP ${res.status} for folder ${folderId}`);
      return [];
    }

    const html = await res.text();
    const match = html.match(/window\['_DRIVE_ivd'\]\s*=\s*'([^']+)'/);
    if (!match) {
      console.warn(`[Crawl] No _DRIVE_ivd found in folder ${folderId}`);
      return [];
    }

    const unescaped = match[1]
      .replace(/\\\\x([0-9a-fA-F]{2})/g, (_, hex) => String.fromCharCode(parseInt(hex, 16)))
      .replace(/\\x([0-9a-fA-F]{2})/g, (_, hex) => String.fromCharCode(parseInt(hex, 16)));

    const parsed = JSON.parse(unescaped);
    const discovered = [];

    function recurse(val) {
      if (!val) return;
      if (Array.isArray(val)) {
        if (typeof val[0] === 'string' && val[0].length >= 25 && typeof val[2] === 'string' && typeof val[3] === 'string') {
          const id = val[0];
          const name = val[2];
          const mime = val[3];
          const isFolder = mime.includes('folder');
          discovered.push({ id, name, mime, isFolder, parentFolderId: folderId, fullPath: pathPrefix ? `${pathPrefix} / ${name}` : name });
        }
        val.forEach(recurse);
      }
    }

    recurse(parsed);

    // Dedup by ID
    const unique = [];
    const seen = new Set();
    for (const item of discovered) {
      if (!seen.has(item.id)) {
        seen.add(item.id);
        unique.push(item);
      }
    }

    // Now for each subfolder, crawl recursively
    let allFiles = [];
    for (const item of unique) {
      if (item.isFolder) {
        console.log(`[Crawl Subfolder] 📁 ${item.fullPath} (ID: ${item.id})`);
        const subItems = await crawlFolder(item.id, item.fullPath, visited);
        allFiles = allFiles.concat(subItems);
      } else {
        allFiles.push(item);
      }
    }

    return allFiles;
  } catch (err) {
    console.error(`[Crawl Error] ${folderId}:`, err.message);
    return [];
  }
}

async function run() {
  console.log('='.repeat(70));
  console.log('  🔍 TÜM GOOGLE DRIVE ÇIKMIŞ SORU KLASÖRLERİNİ TARAMA & LİSTELEME');
  console.log('='.repeat(70));

  const allFoundFiles = [];
  for (const root of TARGET_FOLDERS) {
    console.log(`\n📂 [KÖK KLASÖR] "${root.name}" (ID: ${root.id})...`);
    const files = await crawlFolder(root.id, root.name);
    console.log(`   ✓ Bu klasör ağacında bulunan dosya sayısı: ${files.length}`);
    allFoundFiles.push(...files);
  }

  console.log('\n' + '='.repeat(70));
  console.log(`TOPLAM BULUNAN DOSYA SAYISI: ${allFoundFiles.length}`);
  console.log('='.repeat(70));

  fs.writeFileSync('data/drive_crawler_results.json', JSON.stringify(allFoundFiles, null, 2), 'utf-8');
  console.log('Sonuçlar data/drive_crawler_results.json dosyasına kaydedildi.');
}

run();
