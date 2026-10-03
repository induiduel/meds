import fs from 'fs';
import path from 'path';
import https from 'https';
import { PDFParse } from 'pdf-parse';

const fileId = '1eam0LUNQ5GiXc7u5-PzO0BcEIRmicrpd';
const fileName = '2022-2023 DÖNEM 3 KURUL 4 ÇIKMIŞLAR.pdf';
const destDir = 'C:\\Users\\indui\\Desktop\\meds_database\\meds_sorular';
const txtDir = 'C:\\Users\\indui\\Desktop\\meds_database\\meds_sorular_txt';
const destPath = path.join(destDir, fileName);
const destTxt = path.join(txtDir, '2022-2023 DÖNEM 3 KURUL 4 ÇIKMIŞLAR.txt');

function downloadDriveFile(id, targetPath) {
  return new Promise((resolve, reject) => {
    const initialUrl = `https://drive.usercontent.google.com/download?id=${id}&export=download&authuser=0&confirm=t`;

    function makeReq(url, redirectCount = 0) {
      if (redirectCount > 6) return reject(new Error('Çok fazla yönlendirme'));

      https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' } }, (res) => {
        if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
          return makeReq(res.headers.location, redirectCount + 1);
        }
        if (res.statusCode !== 200) {
          return reject(new Error(`HTTP Durumu: ${res.statusCode}`));
        }

        const fileStream = fs.createWriteStream(targetPath);
        res.pipe(fileStream);
        fileStream.on('finish', () => {
          fileStream.close();
          resolve(fs.statSync(targetPath).size);
        });
      }).on('error', reject);
    }

    makeReq(initialUrl);
  });
}

async function run() {
  console.log(`İndiriliyor: ${fileName}...`);
  try {
    const size = await downloadDriveFile(fileId, destPath);
    console.log(`✓ Başarıyla indirildi (${Math.round(size / 1024)} KB) -> ${destPath}`);

    // PDF to TXT
    const dataBuffer = fs.readFileSync(destPath);
    const parser = new PDFParse({ data: dataBuffer });
    const textRes = await parser.getText();
    const pages = (textRes.pages || []).map((p, idx) => `--- [SAYFA ${idx + 1}] ---\n${p.text || ''}`);
    fs.writeFileSync(destTxt, pages.join('\n\n'), 'utf8');
    console.log(`✓ Metin çıkarıldı (${pages.length} sayfa) -> ${destTxt}`);
  } catch (e) {
    console.error(`Hata:`, e.message);
  }
}

run();
