// Aşama 1: meds_downloads / meds_temp / meds_database iskeletini kurar (idempotent).
import fs from 'fs'; import path from 'path';
import { DOWNLOADS_DIR, TEMP_DIR, DATABASE_DIR } from './config.mjs';
const dirs = [
  DOWNLOADS_DIR,
  ...['extract','ocr','review','jobs','logs','scratch'].map(d => path.join(TEMP_DIR, d)),
  ...['schema','taxonomy','sources','chunks','questions/raw','questions/clean','questions/student','derived','index','reports']
    .map(d => path.join(DATABASE_DIR, d)),
];
for (const d of dirs) fs.mkdirSync(d, { recursive: true });
console.log('İskelet hazır:', dirs.length, 'klasör');
