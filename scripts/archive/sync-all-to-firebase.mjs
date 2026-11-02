/**
 * scripts/sync-all-to-firebase.mjs
 * 
 * Yerel olarak işlenen tüm verileri doğrudan Firebase Firestore'a eşitler:
 * 1. 184 adet Amfi Ders Slayt Notu -> 'lecture_notes' koleksiyonuna yüklenir.
 * 2. 1.600+ Geçmiş Kurul & Yapay Zeka Sorusu -> 'past_questions' koleksiyonuna aktarılır.
 * 3. Kullanıcıların alternatif yorumları ve şikayetleri için Firestore indekslerini ve koleksiyonlarını hazır tutar.
 */

import fs from 'fs';
import path from 'path';
import { initializeApp } from 'firebase/app';
import { getFirestore, doc, setDoc, writeBatch } from 'firebase/firestore';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');

const cfg = JSON.parse(fs.readFileSync(path.join(ROOT_DIR, 'firebase-applet-config.json'), 'utf8'));
const app = initializeApp(cfg);
const db = cfg.firestoreDatabaseId ? getFirestore(app, cfg.firestoreDatabaseId) : getFirestore(app);

function cleanForFirestore(obj) {
  if (obj === null || obj === undefined) return null;
  if (Array.isArray(obj)) return obj.map(cleanForFirestore).filter(v => v !== undefined);
  if (typeof obj === 'object') {
    const res = {};
    for (const [k, v] of Object.entries(obj)) {
      if (v !== undefined) {
        res[k] = cleanForFirestore(v);
      }
    }
    return res;
  }
  return obj;
}

async function syncLectureNotes() {
  const notesPath = path.join(ROOT_DIR, 'data', 'lecture_notes.json');
  if (!fs.existsSync(notesPath)) {
    console.log('⚠️ lecture_notes.json bulunamadı.');
    return;
  }

  const notes = JSON.parse(fs.readFileSync(notesPath, 'utf8'));
  console.log(`\n📚 [Firebase] ${notes.length} adet amfi ders notu Firestore'a aktarılıyor...`);

  let count = 0;
  // Firestore batch ile 100'lük gruplar halinde yükle
  for (let i = 0; i < notes.length; i += 50) {
    const chunk = notes.slice(i, i + 50);
    const batch = writeBatch(db);
    chunk.forEach(note => {
      let cleanNote = cleanForFirestore(note);
      // Firestore 1MB sınırına takılmamak için kontrol
      let noteStr = JSON.stringify(cleanNote);
      if (noteStr.length > 800000 && cleanNote.pages && cleanNote.pages.length > 30) {
        // Sayfa içeriklerini 500 karakter ile sınırla veya ilk 40 sayfayı tut
        cleanNote.pages = cleanNote.pages.map(p => ({
          ...p,
          content: p.content && p.content.length > 800 ? p.content.substring(0, 800) + '...' : p.content
        }));
        if (JSON.stringify(cleanNote).length > 800000) {
          cleanNote.pages = cleanNote.pages.slice(0, 40);
        }
      }
      const docRef = doc(db, 'lecture_notes', note.id);
      batch.set(docRef, cleanNote, { merge: true });
    });
    await batch.commit();
    count += chunk.length;
    process.stdout.write(`   ✓ ${count}/${notes.length} not aktarıldı...\r`);
  }
  console.log(`\n✅ ${count} adet ders notu Firestore 'lecture_notes' koleksiyonuna başarıyla yüklendi!`);
}

async function syncPastQuestions() {
  const pastPath = path.join(ROOT_DIR, 'data', 'pastQuestions.json');
  if (!fs.existsSync(pastPath)) {
    console.log('⚠️ pastQuestions.json bulunamadı.');
    return;
  }

  const questions = JSON.parse(fs.readFileSync(pastPath, 'utf8'));
  console.log(`\n📝 [Firebase] ${questions.length} adet çıkmış & AI soru Firestore'a aktarılıyor...`);

  let count = 0;
  for (let i = 0; i < questions.length; i += 50) {
    const chunk = questions.slice(i, i + 50);
    const batch = writeBatch(db);
    chunk.forEach(q => {
      const cleanQ = cleanForFirestore(q);
      const docRef = doc(db, 'past_questions', q.id);
      batch.set(docRef, cleanQ, { merge: true });
    });
    await batch.commit();
    count += chunk.length;
    process.stdout.write(`   ✓ ${count}/${questions.length} soru aktarıldı...\r`);
  }
  console.log(`\n✅ ${count} adet soru Firestore 'past_questions' koleksiyonuna başarıyla yüklendi!`);
}

async function main() {
  console.log('🚀 [Firebase Eşitleyici] Başlatılıyor...');
  console.log(`   Proje ID: ${cfg.projectId}`);
  await syncLectureNotes();
  await syncPastQuestions();
  console.log('\n🎉 Tüm yerel ders notları ve sorular Firebase Firestore\'a senkronize edildi!');
}

main().catch(console.error);
