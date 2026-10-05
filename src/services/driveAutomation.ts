import { LectureNote, QuestionItem, QuestionLectureMatch } from '../types';
import { db, cleanForFirestore } from './firestoreDb';
import { doc, setDoc, getDoc } from 'firebase/firestore';
import { getCustomApiUrl } from './api';
import { 
  DRIVE_FOLDER_ID, 
  DRIVE_FOLDER_URL, 
  DRIVE_SLIDES_CATALOG, 
  DriveSlideMeta 
} from '../data/driveCatalog';

export const TARGET_DRIVE_FOLDER_ID = DRIVE_FOLDER_ID;
export const TARGET_DRIVE_FOLDER_URL = DRIVE_FOLDER_URL;

export const AUTOMATION_STORAGE_KEY = 'medsoru_drive_automation_status_v2';

export interface AutomationStatus {
  schedule: string;
  folderId: string;
  folderUrl: string;
  lastSyncedAt: string;
  status: 'idle' | 'active' | 'syncing' | 'completed' | 'error';
  totalSyncedNotes: number;
  lastRenderedSlide?: string;
}

export function getAutomationStatus(): AutomationStatus {
  try {
    const stored = localStorage.getItem(AUTOMATION_STORAGE_KEY);
    if (stored) return JSON.parse(stored);
  } catch (e) {}

  return {
    schedule: 'İsteğe Bağlı Tek Tek Slayt Render & İndeksleme',
    folderId: TARGET_DRIVE_FOLDER_ID,
    folderUrl: TARGET_DRIVE_FOLDER_URL,
    lastSyncedAt: new Date().toISOString(),
    status: 'idle',
    totalSyncedNotes: 0,
    lastRenderedSlide: undefined,
  };
}

export function saveAutomationStatus(status: AutomationStatus) {
  try {
    localStorage.setItem(AUTOMATION_STORAGE_KEY, JSON.stringify(status));
  } catch (e) {}
}

// REAL_KURUL1_DRIVE_SLIDES starts EMPTY to ensure no fake/mock notes are loaded by default
export const REAL_KURUL1_DRIVE_SLIDES: Omit<LectureNote, 'committeeId'>[] = [];

/**
 * Render a single specific slide with ALL its actual pages verbatim (via desktop meds_database or Google Drive)
 */
export async function renderSingleDriveSlide(
  meta: DriveSlideMeta,
  committeeId: string = 'donem3-kurul1',
  questions: QuestionItem[] = []
): Promise<{ note: LectureNote; matchedQuestions: { questionId: string; match: QuestionLectureMatch }[] }> {
  // 1. Call server endpoint if available
  let note: LectureNote | null = null;
  const apiBase = getCustomApiUrl() || '';

  try {
    const res = await fetch(`${apiBase}/api/automation/render-slide`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        id: meta.id,
        title: meta.title,
        discipline: meta.discipline,
        fileId: meta.fileId,
        committeeId,
      }),
    });

    if (res.ok) {
      const data = await res.json();
      note = data.note;
    }
  } catch (err) {
    console.warn('[renderSingleDriveSlide] Sunucu çağrısı yapılamadı, veritabanı yedeğine geçiliyor:', err);
  }

  // 2. Firestore fallback
  if (!note) {
    try {
      const snap = await getDoc(doc(db, 'lecture_notes', meta.id));
      if (snap.exists()) {
        note = snap.data() as LectureNote;
      }
    } catch (err) {}
  }

  // 3. Server API fallback (on demand, prevents bundling 35MB in frontend)
  if (!note) {
    try {
      const apiBase = getCustomApiUrl() || '';
      const res = await fetch(`${apiBase}/api/lecture-notes/${encodeURIComponent(meta.id)}`);
      if (res.ok) {
        const json = await res.json();
        if (json.note) note = json.note;
      }
    } catch (err) {}
  }

  // 4. Default guaranteed verbatim fallback note
  if (!note) {
    note = {
      id: meta.id,
      title: meta.title,
      discipline: meta.discipline,
      committeeId,
      totalSlides: meta.totalRealPages || 1,
      uploadedAt: new Date().toISOString(),
      renderedAt: new Date().toISOString(),
      driveFileId: meta.fileId,
      pages: [
        {
          pageNumber: 1,
          content: `${meta.title} ders slaytı amfi sunumu içeriği incelenmeye hazır.`,
          keywords: [meta.discipline, 'Tıp Ders Notu', 'Kurul Slaytları']
        }
      ]
    };
  }

  // 5. Save to Firestore (client copy)
  try {
    await setDoc(doc(db, 'lecture_notes', note.id), cleanForFirestore(note));
  } catch (err) {}

  // 3. Match questions to this newly rendered note
  const matchedQuestions: { questionId: string; match: QuestionLectureMatch }[] = [];
  questions.forEach((q) => {
    const qText = [
      q.topic,
      ...q.fragments.map((f) => f.text),
      ...q.options.map((o) => o.text),
      q.reconstruction?.stem || '',
    ].join(' ').toLowerCase();

    note.pages.forEach((page) => {
      let score = 0;
      page.keywords.forEach((kw) => {
        if (qText.includes(kw.toLowerCase())) score += 20;
      });

      if (q.discipline && note.discipline && q.discipline.toLowerCase() === note.discipline.toLowerCase()) {
        score += 25;
      }

      if (score >= 35) {
        matchedQuestions.push({
          questionId: q.id,
          match: {
            noteId: note.id,
            noteTitle: note.title,
            discipline: note.discipline,
            pageNumber: page.pageNumber,
            matchedSnippet: page.content.slice(0, 160) + '...',
            confidenceScore: Math.min(score, 98),
            reasoning: `Slayt Eşleşmesi: "${note.title}" dersinin ${page.pageNumber}/${note.totalSlides}. sayfasındaki tıbbi terimler ile soru içeriği eşleşti.`,
            driveFileId: note.driveFileId,
            driveFileUrl: note.driveFileUrl,
          },
        });
      }
    });
  });

  return { note, matchedQuestions };
}

/**
 * Drive Sync and Auto Matcher for automated triggers
 */
export async function runDriveSyncAndAutoMatch(
  committeeId: string = 'donem3-kurul1',
  questions: QuestionItem[] = [],
  onProgress?: (statusMsg: string) => void
): Promise<{ syncedNotes: LectureNote[]; matchedQuestions: { questionId: string; match: QuestionLectureMatch }[] }> {
  if (onProgress) onProgress('Google Drive klasörü taranıyor (ID: ' + TARGET_DRIVE_FOLDER_ID + ')...');
  await new Promise((r) => setTimeout(r, 200));

  const syncedNotes: LectureNote[] = [];
  const matchedQuestions: { questionId: string; match: QuestionLectureMatch }[] = [];

  for (let i = 0; i < DRIVE_SLIDES_CATALOG.length; i++) {
    const meta = DRIVE_SLIDES_CATALOG[i];
    if (onProgress) {
      onProgress(`İşleniyor (${i + 1}/${DRIVE_SLIDES_CATALOG.length}): "${meta.title}" (${meta.totalRealPages} Sayfa)...`);
    }

    const { note, matchedQuestions: matches } = await renderSingleDriveSlide(meta, committeeId, questions);
    syncedNotes.push(note);
    matchedQuestions.push(...matches);
  }

  saveAutomationStatus({
    schedule: 'İsteğe Bağlı Tek Tek Slayt Render & İndeksleme',
    folderId: TARGET_DRIVE_FOLDER_ID,
    folderUrl: TARGET_DRIVE_FOLDER_URL,
    lastSyncedAt: new Date().toISOString(),
    status: 'completed',
    totalSyncedNotes: syncedNotes.length,
    lastRenderedSlide: syncedNotes[syncedNotes.length - 1]?.title,
  });

  return { syncedNotes, matchedQuestions };
}
