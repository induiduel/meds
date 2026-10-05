import fs from 'fs';
import path from 'path';

const driveRoot = path.join('G:', "Drive'ım", 'Tıp Genel', 'Ses Kayıtları Dönem 3 (26-27)');
console.log('Target Drive Root:', driveRoot);
console.log('Exists:', fs.existsSync(driveRoot));

const manifestPath = `${process.env.MEDS_DATABASE_DIR || '/home/indu/Masaüstü/MedSoru Project/meds_database'}/transcriptions/transcription_manifest.json`;
const manifest = fs.existsSync(manifestPath) ? JSON.parse(fs.readFileSync(manifestPath, 'utf8')) : {};

function scanDir(dir) {
  let results = [];
  if (!fs.existsSync(dir)) return results;
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      results = results.concat(scanDir(fullPath));
    } else if (/\.(m4a|mp3|wav|aac|ogg|flac)$/i.test(entry.name)) {
      results.push({ fullPath, relativePath: path.relative(driveRoot, fullPath), name: entry.name, size: fs.statSync(fullPath).size });
    }
  }
  return results;
}

const allAudio = scanDir(driveRoot);
console.log('Total Drive Audio files found:', allAudio.length);

const doneList = [];
const newList = [];

for (const f of allAudio) {
  const stem = path.basename(f.name, path.extname(f.name));
  const isDone = manifest[stem]?.status === 'completed' || Object.values(manifest).some(v => v.audioFileName === f.name || v.filename === f.name);
  if (isDone) {
    doneList.push(f);
  } else {
    newList.push(f);
  }
}

console.log('\n--- ALREADY TRANSCRIBED (' + doneList.length + ') ---');
doneList.forEach(f => console.log(' ✅', f.name, '(' + (f.size / (1024*1024)).toFixed(1) + ' MB)'));

console.log('\n--- NEW / WAITING TO TRANSCRIBE (' + newList.length + ') ---');
newList.forEach(f => console.log(' ⏳', f.name, '(' + (f.size / (1024*1024)).toFixed(1) + ' MB) ->', f.relativePath));
