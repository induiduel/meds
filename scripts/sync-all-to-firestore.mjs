/**
 * MedSoru Firestore Full Database Sync Script
 * 
 * Bu betik:
 * 1. INITIAL_COMMITTEES listesini Firestore 'committees' koleksiyonuna eşitler.
 * 2. data/lecture_notes.json içindeki tüm ders notlarını Firestore 'lecture_notes' koleksiyonuna eşitler.
 * 3. data/questions.json ve data/civanPastQuestions.json içindeki 2,566 çıkmış soruyu
 *    Firestore 'questions' koleksiyonuna 450'lik batch'ler halinde aktarır.
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { initializeApp } from 'firebase/app';
import { getFirestore, doc, writeBatch, collection, getDocs } from 'firebase/firestore';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, '..');

// Helper to remove undefined fields recursively for Firestore
function cleanForFirestore(obj) {
  if (obj === null || obj === undefined) return null;
  if (Array.isArray(obj)) return obj.map(cleanForFirestore);
  if (typeof obj === 'object') {
    const cleaned = {};
    for (const [key, value] of Object.entries(obj)) {
      if (value !== undefined) {
        cleaned[key] = cleanForFirestore(value);
      }
    }
    return cleaned;
  }
  return obj;
}

const configPath = path.join(rootDir, 'firebase-applet-config.json');
const firebaseConfig = JSON.parse(fs.readFileSync(configPath, 'utf8'));

const app = initializeApp(firebaseConfig);
const db = getFirestore(app, firebaseConfig.firestoreDatabaseId || undefined);

console.log('='.repeat(70));
console.log('  🔥 MEDSORU -> FIREBASE FIRESTORE TAM SENKRONİZASYON');
console.log('='.repeat(70));
console.log(`Veritabanı: ${firebaseConfig.firestoreDatabaseId}`);

async function syncCommittees() {
  console.log('\n1. Kurullar (Committees) Senkronize Ediliyor...');
  const committees = [
    {
      id: 'donem3-kurul1',
      name: 'Dönem 3 - Kurul 1: TIP 310 - Ürogenital ve Obstetrik Kurulu',
      year: 3,
      term: 'Kurul 1',
      targetCount: 100,
      description: 'Ürogenital sistem hastalıkları, obstetrik ve jinekolojik patolojiler, farmakoloji ve mikrobiyoloji konuları.',
      code: 'TIP 310',
      examDate: '23 Ekim 2026',
      disciplines: ['Tıbbi Patoloji', 'Tıbbi Farmakoloji', 'Tıbbi Mikrobiyoloji', 'Kadın Hastalıkları ve Doğum', 'Üroloji'],
    },
    {
      id: 'donem3-kurul2',
      name: 'Dönem 3 - Kurul 2: TIP 302 - Kardiyovasküler ve Solunum Sistemi',
      year: 3,
      term: 'Kurul 2',
      targetCount: 100,
      description: 'Kardiyovasküler sistem patolojileri, solunum yolu enfeksiyonları, pulmoner farmakoloji.',
      code: 'TIP 302',
      examDate: '4 Aralık 2026',
      disciplines: ['Kardiyoloji', 'Göğüs Hastalıkları', 'Tıbbi Patoloji', 'Tıbbi Farmakoloji', 'Tıbbi Mikrobiyoloji'],
    },
    {
      id: 'donem3-kurul3',
      name: 'Dönem 3 - Kurul 3: TIP 303 - Gastrointestinal Sistem ve Metabolizma',
      year: 3,
      term: 'Kurul 3',
      targetCount: 100,
      description: 'Gastrointestinal sistem hastalıkları, karaciğer patolojileri, beslenme ve metabolizma bozuklukları.',
      code: 'TIP 303',
      examDate: '22 Ocak 2027',
      disciplines: ['Gastroenteroloji', 'Genel Cerrahi', 'Tıbbi Patoloji', 'Tıbbi Farmakoloji', 'Biyokimya'],
    },
    {
      id: 'donem3-kurul4',
      name: 'Dönem 3 - Kurul 4: TIP 304 - Nörolojik Bilimler ve Psikiyatri',
      year: 3,
      term: 'Kurul 4',
      targetCount: 100,
      description: 'Merkezi ve periferik sinir sistemi patolojileri, psikiyatrik bozukluklar ve psikofarmakoloji.',
      code: 'TIP 304',
      examDate: '5 Mart 2027',
      disciplines: ['Nöroloji', 'Psikiyatri', 'Beyin Cerrahisi', 'Tıbbi Patoloji', 'Tıbbi Farmakoloji'],
    },
    {
      id: 'donem3-kurul5',
      name: 'Dönem 3 - Kurul 5: TIP 305 - Kas-İskelet Sistemi ve Deri',
      year: 3,
      term: 'Kurul 5',
      targetCount: 100,
      description: 'Romatolojik hastalıklar, ortopedik patolojiler, dermatoloji ve otoimmün hastalıklar.',
      code: 'TIP 305',
      examDate: '22 Nisan 2027',
      disciplines: ['Ortopedi', 'Fizik Tedavi ve Rehabilitasyon', 'Dermatoloji', 'Romatoloji', 'Tıbbi Patoloji'],
    },
    {
      id: 'donem3-kurul6',
      name: 'Dönem 3 - Kurul 6: TIP 306 - Endokrin Sistem ve Hematoloji',
      year: 3,
      term: 'Kurul 6',
      targetCount: 100,
      description: 'Endokrin organ patolojileri, anemi ve lösemiler, koagülasyon bozuklukları.',
      code: 'TIP 306',
      examDate: '11 Haziran 2027',
      disciplines: ['Endokrinoloji', 'Hematoloji', 'Tıbbi Patoloji', 'Tıbbi Farmakoloji', 'Biyokimya'],
    },
    {
      id: 'donem3-final',
      name: 'Dönem 3 - Yıl Sonu Genel Final Sınavı',
      year: 3,
      term: 'Final Sınavı',
      targetCount: 100,
      description: 'Dönem 3 tüm kurul ve tıp bilimlerini kapsayan yıl sonu genel değerlendirme sınavı.',
      code: 'TIP 399',
      examDate: '28 Haziran 2027',
      disciplines: ['Tıbbi Patoloji', 'Tıbbi Farmakoloji', 'Tıbbi Mikrobiyoloji', 'Dahiliye', 'Pediatri', 'Genel Cerrahi'],
    },
    {
      id: 'donem3-butunleme',
      name: 'Dönem 3 - Yıl Sonu Bütünleme Sınavı',
      year: 3,
      term: 'Bütünleme',
      targetCount: 100,
      description: 'Dönem 3 yıl sonu bütünleme telafi sınavı soru arşivi ve çalışma kılavuzu.',
      code: 'TIP 399-B',
      examDate: '16 Temmuz 2027',
      disciplines: ['Tıbbi Patoloji', 'Tıbbi Farmakoloji', 'Tıbbi Mikrobiyoloji', 'Dahili Tıp', 'Cerrahi Tıp'],
    },
  ];

  const batch = writeBatch(db);
  for (const c of committees) {
    const docRef = doc(db, 'committees', c.id);
    batch.set(docRef, cleanForFirestore(c), { merge: true });
  }
  await batch.commit();
  console.log(`   ✓ ${committees.length} kurul Firestore'a başarıyla kaydedildi.`);
}

async function syncLectureNotes() {
  console.log('\n2. Ders Notları (Lecture Notes) Senkronize Ediliyor...');
  const notesPath = path.join(rootDir, 'data', 'lecture_notes.json');
  let notes = [];
  if (fs.existsSync(notesPath)) {
    try {
      notes = JSON.parse(fs.readFileSync(notesPath, 'utf8'));
    } catch (e) {
      console.warn('lecture_notes.json okuma uyarısı:', e.message);
    }
  }

  console.log(`   📂 Yerelde bulunan ders notu sayısı: ${notes.length}`);
  if (notes.length === 0) return;

  const BATCH_SIZE = 50; // Slaytlar sayfalar içerdiği için batch boyutunu makul tutuyoruz
  let savedCount = 0;

  for (let i = 0; i < notes.length; i += BATCH_SIZE) {
    const chunk = notes.slice(i, i + BATCH_SIZE);
    const batch = writeBatch(db);
    for (const note of chunk) {
      const noteId = note.id || `ln-${note.title.replace(/[^a-zA-Z0-9_-]/g, '_').toLowerCase()}`;
      let safeNote = {
        ...note,
        id: noteId,
        updatedAt: new Date().toISOString()
      };

      // Firestore 1MB document size limit check
      let rawJson = JSON.stringify(safeNote);
      if (Buffer.byteLength(rawJson) > 750000 && Array.isArray(safeNote.pages)) {
        const ratio = 700000 / Buffer.byteLength(rawJson);
        const allowedPageCount = Math.max(30, Math.floor(safeNote.pages.length * ratio));
        safeNote.pages = safeNote.pages.slice(0, allowedPageCount);
        safeNote.isPartialInCloud = true;
      }

      const docRef = doc(db, 'lecture_notes', noteId);
      batch.set(docRef, cleanForFirestore(safeNote), { merge: true });
    }
    await batch.commit();
    savedCount += chunk.length;
    process.stdout.write(`   ✓ Ders Notları: ${savedCount}/${notes.length}\r`);
  }
  console.log(`\n   ✓ Toplam ${savedCount} ders notu Firestore 'lecture_notes' koleksiyonuna eşitlendi.`);
}

async function syncQuestions() {
  console.log('\n3. Çıkmış Sorular (Past Questions) Senkronize Ediliyor...');
  
  // data/pastQuestions.json
  const pastQuestionsPath = path.join(rootDir, 'data', 'pastQuestions.json');
  let rawQuestions = [];
  if (fs.existsSync(pastQuestionsPath)) {
    try {
      rawQuestions = JSON.parse(fs.readFileSync(pastQuestionsPath, 'utf8'));
    } catch (e) {}
  }

  // Deduplicate and filter (strictly excluding Civan notes)
  const map = new Map();
  for (const q of rawQuestions) {
    if (!q || !q.id) continue;
    if (q.id.startsWith('civan-')) continue;
    if (q.tags && q.tags.some(t => /civan/i.test(t))) continue;
    if (q.author && /civan/i.test(q.author)) continue;

    let year = q.examYear;
    if (!year || year.includes('2026')) {
      const detected = (q.tags || []).find(t => /(?:19\d{2}|20[0-2][0-5])/.test(t));
      year = detected ? detected.match(/(?:19\d{2}|20[0-2][0-5])/)?.[0] || 'Geçmiş Yıllar Çıkmışı (Arşiv)' : 'Geçmiş Yıllar Çıkmışı (Arşiv)';
    }

    const stem = (q.reconstruction?.stem || q.fragments?.[0]?.text || q.rawStem || q.topic || '').trim();
    const opts = q.reconstruction?.options || q.options || [];
    const validOpts = opts.filter(o => o && o.text && o.text.trim().length > 0);
    const isAmbiguous = stem.length < 25 || validOpts.length < 2;

    map.set(q.id, {
      ...q,
      isPastExam: true,
      examYear: year,
      isAmbiguous: q.isAmbiguous ?? isAmbiguous,
      sourceFile: q.sourceFile || (q.tags || []).find(t => t.toLowerCase().endsWith('.pdf')) || 'Çıkmış Sınav Dosyası',
      upvotes: typeof q.upvotes === 'number' ? q.upvotes : 0,
      likedBy: Array.isArray(q.likedBy) ? q.likedBy : [],
    });
  }

  const allQuestions = Array.from(map.values());
  console.log(`   📂 Aktarılacak toplam çıkmış soru sayısı: ${allQuestions.length}`);

  const BATCH_SIZE = 400; // Firestore batch limiti 500
  let uploadedCount = 0;

  for (let i = 0; i < allQuestions.length; i += BATCH_SIZE) {
    const chunk = allQuestions.slice(i, i + BATCH_SIZE);
    const batch = writeBatch(db);

    for (const q of chunk) {
      // Çıkmış sorular doğrudan past_questions koleksiyonuna kaydedilir
      const docRef = doc(db, 'past_questions', q.id);
      batch.set(docRef, cleanForFirestore(q), { merge: true });
    }

    await batch.commit();
    uploadedCount += chunk.length;
    process.stdout.write(`   ✓ Aktarılan Soru: ${uploadedCount} / ${allQuestions.length}\r`);
  }

  console.log(`\n   ✓ Toplam ${uploadedCount} soru Firestore 'past_questions' koleksiyonuna başarıyla aktarıldı!`);
}

async function main() {
  const startTime = Date.now();
  try {
    await syncCommittees();
    await syncLectureNotes();
    await syncQuestions();
    const duration = ((Date.now() - startTime) / 1000).toFixed(1);
    console.log('\n' + '='.repeat(70));
    console.log(`  🎉 TÜM VERİTABANI BAŞARIYLA FİREBASE'E YÜKLENDİ! (${duration} saniye)`);
    console.log('='.repeat(70));
    process.exit(0);
  } catch (err) {
    console.error('\n❌ Senkronizasyon hatası:', err);
    process.exit(1);
  }
}

main();
