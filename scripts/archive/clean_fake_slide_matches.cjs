const fs = require('fs');
const path = require('path');

const lectureNotesPath = path.join(__dirname, '..', 'src', 'data', 'lecture_notes.json');
const pastQuestionsPath = path.join(__dirname, '..', 'src', 'data', 'pastQuestions.json');

const fakeIds = new Set([
  'note-afa990def7',
  'note-873b595f77', // İSKENDERUN TİMüdürlüğüne0 (1)_230709_230251
  'note-104f1fcc4c', // Kurul I Cevap Anahtarı
  'note-7e8d872672', // combinepdf (28)
  'note-a51ee43893', // Kurul VI Cevap Anahtarı
  'note-429ac49a5d', // Kurul V Cevap Anahtarı
  'note-5e47efe73d', // 2021-2022 Çıkmış
  'note-06356c22cf', // 22-23D3Butunleme_101817
  'note-862e627ec9', // 22%20final_230619_145249.pdf.pdf
]);

function isFakeTitle(title) {
  if (!title) return false;
  const t = title.toLowerCase();
  return (
    t.includes('iskenderun') ||
    t.includes('combinepdf') ||
    t.includes('cevap anahtarı') ||
    t.includes('22%20final') ||
    t.includes('2021-2022 çıkmış') ||
    t.includes('2021-2022 çıkmış') ||
    t.includes('22-23d3butunleme') ||
    t === '1268092026090839'
  );
}

// 1. Clean lecture_notes.json
console.log('Reading lecture_notes.json...');
const notes = JSON.parse(fs.readFileSync(lectureNotesPath, 'utf8'));
const initialNotesLen = notes.length;
const cleanNotes = notes.filter(n => !fakeIds.has(n.id) && !isFakeTitle(n.title));
console.log(`Cleaned lecture_notes: ${initialNotesLen} -> ${cleanNotes.length} (Removed ${initialNotesLen - cleanNotes.length} fake exam notes)`);

fs.writeFileSync(lectureNotesPath, JSON.stringify(cleanNotes, null, 2), 'utf8');
console.log('lecture_notes.json saved.');

// 2. Clean pastQuestions.json
console.log('Reading pastQuestions.json...');
const questions = JSON.parse(fs.readFileSync(pastQuestionsPath, 'utf8'));
let cleanedQCount = 0;

questions.forEach(q => {
  const nid = q.lectureReference?.noteId;
  const nt = q.matchedNoteTitle;
  if (fakeIds.has(nid) || isFakeTitle(nt) || isFakeTitle(q.lectureReference?.noteTitle)) {
    q.matchedNoteTitle = null;
    q.matchedSlidePage = null;
    delete q.lectureReference;
    q.slideAudit = {
      status: 'unmatched',
      auditedAt: new Date().toISOString(),
      reason: 'Sınav kitapçığı / arşivi ders slaytı olmadığı için hatalı eşleşme kaldırıldı.'
    };
    cleanedQCount++;
  }
});

console.log(`Cleaned ${cleanedQCount} past questions in pastQuestions.json.`);
fs.writeFileSync(pastQuestionsPath, JSON.stringify(questions, null, 2), 'utf8');
console.log('pastQuestions.json saved.');
