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
  
  // 1. data/questions.json
  const questionsPath = path.join(rootDir, 'data', 'questions.json');
  let rawQuestions = [];
  if (fs.existsSync(questionsPath)) {
    try {
      const parsed = JSON.parse(fs.readFileSync(questionsPath, 'utf8'));
      rawQuestions = Array.isArray(parsed) ? parsed : (parsed.questions || []);
    } catch (e) {}
  }

  // 2. data/civanPastQuestions.json
  const civanPath = path.join(rootDir, 'data', 'civanPastQuestions.json');
  let civanList = [];
  if (fs.existsSync(civanPath)) {
    try {
      civanList = JSON.parse(fs.readFileSync(civanPath, 'utf8'));
    } catch (e) {}
  }

  // Deduplicate and combine
  const map = new Map();
  for (const q of rawQuestions) {
    if (q && q.id) {
      map.set(q.id, {
        ...q,
        isPastExam: true,
        examYear: q.examYear || (q.tags?.find(t => /\d{4}/.test(t)) || 'Çıkmış Soru'),
        upvotes: typeof q.upvotes === 'number' ? q.upvotes : 0,
        likedBy: Array.isArray(q.likedBy) ? q.likedBy : [],
      });
    }
  }

  for (const cq of civanList) {
    if (cq && cq.id && !map.has(cq.id)) {
      map.set(cq.id, {
        id: cq.id,
        committeeId: cq.committeeId || 'donem3-kurul1',
        questionNumber: cq.questionNumber || 1,
        discipline: cq.discipline || 'Tıbbi Patoloji',
        topic: cq.topic || 'Genel Tıp Çıkmış Soru',
        status: 'completed',
        isPastExam: true,
        examYear: cq.examYear || 'Civan Arşivi (2020-2026)',
        claimedAnswer: cq.correctAnswer || (cq.options?.[0]?.key || 'A'),
        tags: [cq.discipline, 'Civanın Notları', cq.examYear || 'Çıkmış'].filter(Boolean),
        fragments: [
          {
            id: `f-${cq.id}-1`,
            author: "Civan'ın Soru Notları",
            text: cq.rawStem || cq.stem || cq.topic || 'Çıkmış kurul sorusu',
            type: 'stem',
            timestamp: new Date().toISOString(),
            upvotes: 0,
            likedBy: [],
          },
        ],
        options: (cq.options || []).map(opt => ({
          key: opt.key || 'A',
          text: opt.text || '',
          suggestedBy: "Civan'ın Notları",
          upvotes: 0,
          likedBy: [],
        })),
        reconstruction: {
          stem: cq.stem || cq.rawStem || cq.topic || '',
          options: (cq.options || []).map(opt => ({
            key: opt.key || 'A',
            text: opt.text || '',
            isAiFilled: false,
          })),
          correctAnswer: cq.correctAnswer || (cq.options?.[0]?.key || 'A'),
          explanation: cq.explanation || 'Bu soru Civanın Notları geçmiş tıp kurul sınavları arşivinden aktarılmıştır.',
          confidenceScore: 92,
          notesAndDiscrepancies: 'Çıkmış kurul sorusu',
          lastUpdated: new Date().toISOString(),
        },
        upvotes: 0,
        likedBy: [],
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      });
    }
  }

  const allQuestions = Array.from(map.values());
  console.log(`   📂 Aktarılacak toplam soru sayısı: ${allQuestions.length}`);

  const BATCH_SIZE = 400; // Firestore batch limiti 500
  let uploadedCount = 0;

  for (let i = 0; i < allQuestions.length; i += BATCH_SIZE) {
    const chunk = allQuestions.slice(i, i + BATCH_SIZE);
    const batch = writeBatch(db);

    for (const q of chunk) {
      const docRef = doc(db, 'questions', q.id);
      batch.set(docRef, cleanForFirestore(q), { merge: true });
    }

    await batch.commit();
    uploadedCount += chunk.length;
    process.stdout.write(`   ✓ Aktarılan Soru: ${uploadedCount} / ${allQuestions.length}\r`);
  }

  console.log(`\n   ✓ Toplam ${uploadedCount} soru Firestore 'questions' koleksiyonuna başarıyla aktarıldı!`);
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
