import fs from 'fs';
import path from 'path';

const ROOT_FOLDER_ID = '1ozu5KiLZjFd4YKNMZ0bSRvLVV6b7lv0W';

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
          discovered.push({
            id,
            name,
            mime,
            isFolder,
            parentFolderId: folderId,
            fullPath: pathPrefix ? `${pathPrefix} / ${name}` : name
          });
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

    let allItems = [];
    for (const item of unique) {
      allItems.push(item);
      if (item.isFolder) {
        console.log(`[Klasör] 📁 ${item.fullPath}`);
        const subItems = await crawlFolder(item.id, item.fullPath, visited);
        allItems = allItems.concat(subItems);
      }
    }

    return allItems;
  } catch (err) {
    console.error(`[Crawl Error] ${folderId}:`, err.message);
    return [];
  }
}

async function run() {
  console.log('='.repeat(70));
  console.log('  🔍 USER DRIVE KLASÖRÜNÜ ÖZYİNELEMELİ TARAMA');
  console.log(`  Kök Klasör: ${ROOT_FOLDER_ID}`);
  console.log('='.repeat(70));

  const items = await crawlFolder(ROOT_FOLDER_ID, 'Meds_Drive_Root');
  const files = items.filter(i => !i.isFolder);
  const pdfs = files.filter(f => f.name.toLowerCase().endsWith('.pdf'));

  console.log('\n' + '='.repeat(70));
  console.log(`Toplam Öğe: ${items.length}`);
  console.log(`Toplam Dosya: ${files.length}`);
  console.log(`Toplam PDF: ${pdfs.length}`);
  console.log('='.repeat(70));

  const catalog = {
    updatedAt: new Date().toISOString(),
    rootFolderId: ROOT_FOLDER_ID,
    totalItems: items.length,
    totalFiles: files.length,
    totalPdfs: pdfs.length,
    items,
    files,
    pdfs
  };

  fs.mkdirSync('data', { recursive: true });
  fs.writeFileSync('data/user_drive_catalog.json', JSON.stringify(catalog, null, 2), 'utf-8');
  console.log('Katalog data/user_drive_catalog.json dosyasına yazıldı.');

  // Print PDFs summary
  console.log('\nBulunan PDF Dosyaları:');
  pdfs.forEach((p, idx) => {
    console.log(`${idx + 1}. [${p.id}] ${p.fullPath}`);
  });
}

run();
