import fs from 'fs';

const FOLDER_IDS = [
  { name: 'Folder 1', id: '18U1LZVvV0VROcWVQTDBeJYwdBWiEIVwS' },
  { name: 'Folder 2', id: '1VJwhDITJWZFaaBTvMajnLUzII31r1GTp' },
  { name: 'Folder 3', id: '1AZaRbCpIUKtv0t6sg3VaZHC42NmbrnB4' },
  { name: 'Folder 4', id: '16ianUX4Nnl-dU9SZOSOgvDDuEaM1x6vZ' },
  { name: 'Folder 5', id: '1FAqqW0iAeg3NNjkPBeY3zG9X4FXaJuVM' },
  { name: 'Folder 6', id: '1QKbD3800KBa3AUWP8apMSiKCMV0jiA21' },
];

async function inspectFolder(folder) {
  const url = `https://drive.google.com/drive/folders/${folder.id}`;
  try {
    const res = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
      }
    });
    console.log(`[${folder.name}] Status: ${res.status}`);
    const html = await res.text();
    
    // Check if page contains file names or IDs
    // Drive embed data in window['_DRIVE_ivd'] or similar JSON array
    const fileMatches = [];
    const re = /\["([a-zA-Z0-9_-]{25,})",\["([^"]+?\.(?:pdf|docx?|txt|jpg|png))"/gi;
    let m;
    while ((m = re.exec(html)) !== null) {
      fileMatches.push({ id: m[1], name: m[2] });
    }

    // Secondary regex for titles and IDs in Drive JSON
    if (fileMatches.length === 0) {
      const titleRegex = /"([a-zA-Z0-9_-]{28,35})",null,"([^"]+?)"/g;
      while ((m = titleRegex.exec(html)) !== null) {
        if (m[2].includes('.') || m[2].length > 3) {
          fileMatches.push({ id: m[1], name: m[2] });
        }
      }
    }

    console.log(`[${folder.name}] Found ${fileMatches.length} files:`);
    fileMatches.slice(0, 10).forEach(f => console.log(`   - ${f.name} (ID: ${f.id})`));
    return { folder, fileMatches };
  } catch (err) {
    console.error(`[${folder.name}] Error:`, err.message);
    return { folder, fileMatches: [] };
  }
}

async function run() {
  for (const f of FOLDER_IDS) {
    await inspectFolder(f);
  }
}

run();
