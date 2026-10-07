import fs from 'fs';
import https from 'https';
import path from 'path';
import { PDFParse } from 'pdf-parse';

function downloadFile(fileId, destPath) {
  return new Promise((resolve, reject) => {
    const initialUrl = 'https://drive.usercontent.google.com/download?id=' + fileId + '&export=download&authuser=0&confirm=t';
    function makeReq(url) {
      https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0' } }, (res) => {
        if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
          return makeReq(res.headers.location);
        }
        if (res.statusCode !== 200) return reject(new Error('Status ' + res.statusCode));
        const fileStream = fs.createWriteStream(destPath);
        res.pipe(fileStream);
        fileStream.on('finish', () => { fileStream.close(); resolve(fs.statSync(destPath).size); });
        fileStream.on('error', reject);
      }).on('error', reject);
    }
    makeReq(initialUrl);
  });
}

function sanitizeFileName(name) {
  return name.replace(/[\\/:*?"<>|]/g, '_').trim();
}

async function testMultiple() {
  const crawlerData = JSON.parse(fs.readFileSync('data/drive_crawler_results.json', 'utf8'));
  const pdfs = crawlerData.filter(f => f.name.toLowerCase().endsWith('.pdf') && !f.name.includes('19 final'));

  const samples = [
    pdfs.find(p => p.fullPath.toLowerCase().includes('kurul 1')),
    pdfs.find(p => p.fullPath.toLowerCase().includes('kurul 2')),
    pdfs.find(p => p.name.includes('2024')),
    pdfs.find(p => p.name.toLowerCase().includes('d3k1')),
    pdfs.find(p => p.name.includes('22-23')),
  ].filter(Boolean);

  for (const item of samples) {
    const safeName = sanitizeFileName(item.name);
    const destPath = path.join(`${process.env.MEDS_DATABASE_DIR || '/home/indu/medsor/meds_database'}/meds_sorular`, safeName);
    console.log('\nİndiriliyor:', safeName);
    console.log('Kaynak Yol:', item.fullPath);
    await downloadFile(item.id, destPath);
    const parser = new PDFParse({ data: fs.readFileSync(destPath) });
    const textRes = await parser.getText();
    let totalTextLen = 0;
    let textPages = 0;
    textRes.pages.forEach(p => {
      const len = (p.text || '').trim().length;
      if (len > 30) textPages++;
      totalTextLen += len;
    });
    console.log(`✓ Sonuç: ${textRes.pages.length} sayfa, ${textPages} metinli sayfa, toplam metin: ${totalTextLen} karakter`);
    const snippetPage = textRes.pages.find(p => (p.text || '').trim().length > 100);
    if (snippetPage) {
      console.log('Metin örneği:', snippetPage.text.trim().substring(0, 200).replace(/\n/g, ' '));
    }
  }
}

testMultiple().catch(console.error);
