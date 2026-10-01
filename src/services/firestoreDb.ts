import { 
  getFirestore, 
  collection, 
  doc, 
  getDocs, 
  getDoc,
  setDoc, 
  addDoc,
  deleteDoc, 
  query, 
  where, 
  writeBatch,
  onSnapshot
} from 'firebase/firestore';
import { auth } from './auth';
import { Committee, QuestionItem, AdminNotification, LectureNote } from '../types';
import firebaseConfig from '../../firebase-applet-config.json';

// Initialize Firestore using the configured database ID
const firestoreDatabaseId = firebaseConfig.firestoreDatabaseId || undefined;
export const db = firestoreDatabaseId
  ? getFirestore(auth.app, firestoreDatabaseId)
  : getFirestore(auth.app);

export const COMMITTEES_COLLECTION = 'committees';
export const QUESTIONS_COLLECTION = 'questions';
export const PAST_QUESTIONS_COLLECTION = 'past_questions';
export const LECTURE_NOTES_COLLECTION = 'lecture_notes';
export const NOTIFICATIONS_COLLECTION = 'admin_notifications';

// Helper to prevent any Firebase network hang from blocking the UI
export function withTimeout<T>(promise: Promise<T>, timeoutMs = 4500): Promise<T> {
  return Promise.race([
    promise,
    new Promise<T>((_, reject) =>
      setTimeout(() => reject(new Error(`Veritabanı yanıt süresi aşıldı (${timeoutMs}ms)`)), timeoutMs)
    ),
  ]);
}

/**
 * Strips all undefined fields recursively so Firestore setDoc does not throw
 * "Unsupported field value: undefined" error.
 */
export function cleanForFirestore<T>(data: T): any {
  if (data === null || data === undefined) {
    return null;
  }
  if (Array.isArray(data)) {
    return data.map((item) => cleanForFirestore(item));
  }
  if (typeof data === 'object') {
    const cleaned: Record<string, any> = {};
    for (const [key, value] of Object.entries(data as Record<string, any>)) {
      if (value !== undefined) {
        cleaned[key] = cleanForFirestore(value);
      }
    }
    return cleaned;
  }
  return data;
}

export const COMMITTEE_SORT_ORDER: Record<string, number> = {
  'donem3-kurul1': 1,
  'donem3-kurul2': 2,
  'donem3-kurul3': 3,
  'donem3-kurul4': 4,
  'donem3-kurul5': 5,
  'donem3-kurul6': 6,
  'donem3-final': 7,
  'donem3-butunleme': 8,
};

/**
 * Automatically calculates which committee exam is currently upcoming or active
 * based on the official medical school calendar.
 */
export function getDefaultActiveCommitteeId(): string {
  const now = new Date();
  const schedule = [
    { id: 'donem3-kurul1', examDate: new Date('2026-10-23T23:59:59') },
    { id: 'donem3-kurul2', examDate: new Date('2026-12-04T23:59:59') },
    { id: 'donem3-kurul3', examDate: new Date('2027-01-22T23:59:59') },
    { id: 'donem3-kurul4', examDate: new Date('2027-03-05T23:59:59') },
    { id: 'donem3-kurul5', examDate: new Date('2027-04-22T23:59:59') },
    { id: 'donem3-kurul6', examDate: new Date('2027-06-11T23:59:59') },
    { id: 'donem3-final', examDate: new Date('2027-06-28T23:59:59') },
    { id: 'donem3-butunleme', examDate: new Date('2027-07-16T23:59:59') },
  ];

  for (const item of schedule) {
    if (now <= item.examDate) {
      return item.id;
    }
  }
  return 'donem3-final';
}

// Official curriculum committees from syllabus document
export const INITIAL_COMMITTEES: Committee[] = [
  {
    id: 'donem3-kurul1',
    name: 'Dönem 3 - Kurul 1: TIP 310 - Ürogenital ve Obstetrik Kurulu',
    year: 3,
    term: '2026-2027 Güz',
    targetCount: 100,
    code: 'TIP 310',
    examDate: '23 Ekim 2026',
    description: 'Tıbbi Patoloji (33 saat), Enfeksiyon Hastalıkları (22 saat), Üroloji (13 saat), Tıbbi Genetik (12 saat), Halk Sağlığı (10 saat), Kadın Hastalıkları ve Doğum (4 saat), Tıbbi Farmakoloji (2 saat). Toplam 96 saat.',
    disciplines: [
      'Tıbbi Patoloji',
      'Tıbbi Biyoloji ve Genetik',
      'Tıbbi Biyokimya',
      'Enfeksiyon Hastalıkları',
      'Üroloji',
      'Tıbbi Genetik',
      'Halk Sağlığı',
      'Kadın Hastalıkları ve Doğum',
      'Tıbbi Farmakoloji'
    ]
  },
  {
    id: 'donem3-kurul2',
    name: 'Dönem 3 - Kurul 2: TIP 320 - Nöropsikiyatri Kurulu',
    year: 3,
    term: '2026-2027 Güz',
    targetCount: 100,
    code: 'TIP 320',
    examDate: '04 Aralık 2026',
    description: 'Tıbbi Farmakoloji (28 saat), Psikiyatri (24 saat), Nöroloji (18 saat), Tıbbi Genetik (10 saat), Aile Hekimliği (8 saat), Beyin ve Sinir Cerrahisi (6 saat), Tıbbi Patoloji (5 saat), FTR (4 saat), Anesteziyoloji (2 saat). Toplam 105 saat.',
    disciplines: [
      'Tıbbi Farmakoloji',
      'Psikiyatri',
      'Nöroloji',
      'Tıbbi Genetik',
      'Aile Hekimliği',
      'Beyin ve Sinir Cerrahisi',
      'Tıbbi Patoloji',
      'FTR',
      'Anesteziyoloji ve Reanimasyon'
    ]
  },
  {
    id: 'donem3-kurul3',
    name: 'Dönem 3 - Kurul 3: TIP 330 - Gastrointestinal Sistem Kurulu',
    year: 3,
    term: '2026-2027 Güz',
    targetCount: 100,
    code: 'TIP 330',
    examDate: '22 Ocak 2027',
    description: 'Tıbbi Farmakoloji (31 saat), İç Hastalıkları (26 saat), Tıbbi Patoloji (19 saat), Çocuk Sağlığı ve Hastalıkları (6 saat), Tıbbi Genetik (4 saat), Enfeksiyon Hastalıkları (4 saat). Toplam 90 saat.',
    disciplines: [
      'Tıbbi Farmakoloji',
      'İç Hastalıkları',
      'Tıbbi Patoloji',
      'Çocuk Sağlığı ve Hastalıkları',
      'Tıbbi Genetik',
      'Enfeksiyon Hastalıkları'
    ]
  },
  {
    id: 'donem3-kurul4',
    name: 'Dönem 3 - Kurul 4: TIP 340 - Dolaşım, Solunum ve Tümör Kurulu',
    year: 3,
    term: '2026-2027 Bahar',
    targetCount: 100,
    code: 'TIP 340',
    examDate: '05 Mart 2027',
    description: 'Kardiyoloji (20 saat), Tıbbi Patoloji (18 saat), Tıbbi Farmakoloji (16 saat), Çocuk Sağlığı ve Hastalıkları (9 saat), Tıbbi Genetik (8 saat), Göğüs Hastalıkları (6 saat), Kalp ve Damar Cerrahisi (4 saat), Enfeksiyon Hastalıkları (4 saat), İç Hastalıkları (2 saat), Halk Sağlığı (2 saat), Anestezi (1 saat). Toplam 90 saat.',
    disciplines: [
      'Kardiyoloji',
      'Tıbbi Patoloji',
      'Tıbbi Farmakoloji',
      'Çocuk Sağlığı ve Hastalıkları',
      'Tıbbi Genetik',
      'Göğüs Hastalıkları',
      'Kalp ve Damar Cerrahisi',
      'Enfeksiyon Hastalıkları',
      'İç Hastalıkları',
      'Halk Sağlığı',
      'Anestezi ve Reanimasyon'
    ]
  },
  {
    id: 'donem3-kurul5',
    name: 'Dönem 3 - Kurul 5: TIP 350 - Ortopedi, Travmatoloji ve Hematopoetik Sistem Kurulu',
    year: 3,
    term: '2026-2027 Bahar',
    targetCount: 100,
    code: 'TIP 350',
    examDate: '22 Nisan 2027',
    description: 'Acil Tıp (18 saat), Tıbbi Patoloji (16 saat), Ortopedi ve Travmatoloji (13 saat), Halk Sağlığı (13 saat), FTR (12 saat), İç Hastalıkları (8 saat), Tıbbi Genetik (6 saat), Tıbbi Farmakoloji (6 saat), Çocuk Sağlığı (4 saat), Beyin Cerrahisi (3 saat), Göğüs Cerrahisi (3 saat), Enfeksiyon (2 saat). Toplam 104 saat.',
    disciplines: [
      'Acil Tıp',
      'Tıbbi Patoloji',
      'Ortopedi ve Travmatoloji',
      'Halk Sağlığı',
      'FTR',
      'İç Hastalıkları',
      'Tıbbi Genetik',
      'Tıbbi Farmakoloji',
      'Çocuk Sağlığı ve Hastalıkları',
      'Beyin ve Sinir Cerrahisi',
      'Göğüs Cerrahisi',
      'Enfeksiyon Hastalıkları'
    ]
  },
  {
    id: 'donem3-kurul6',
    name: 'Dönem 3 - Kurul 6: TIP 360 - Endokrin, Metabolizma ve Yaşlanma Kurulu',
    year: 3,
    term: '2026-2027 Bahar',
    targetCount: 100,
    code: 'TIP 360',
    examDate: '11 Haziran 2027',
    description: 'İç Hastalıkları (30 saat), Halk Sağlığı (17 saat), Tıbbi Farmakoloji (14 saat), Tıbbi Genetik (8 saat), Tıbbi Biyokimya (8 saat), Tıbbi Patoloji (4 saat), Çocuk Sağlığı (3 saat), Psikiyatri (3 saat), FTR (2 saat), Aile Hekimliği (2 saat). Toplam 91 saat.',
    disciplines: [
      'İç Hastalıkları',
      'Halk Sağlığı',
      'Tıbbi Farmakoloji',
      'Tıbbi Genetik',
      'Tıbbi Biyokimya',
      'Tıbbi Patoloji',
      'Çocuk Sağlığı ve Hastalıkları',
      'Psikiyatri',
      'FTR',
      'Aile Hekimliği'
    ]
  },
  {
    id: 'donem3-final',
    name: 'Dönem 3 - TIP 300: Yıl Sonu Genel Final Sınavı',
    year: 3,
    term: '2026-2027 Yıl Sonu',
    targetCount: 150,
    code: 'TIP 300',
    examDate: '28 Haziran 2027',
    description: 'Tüm Kurul 1-6 komitelerini kapsayan 150 soruluk genel yıl sonu final sınavı. Sorumlu: Prof. Dr. Hikmet Keleş.',
    disciplines: [
      'Tıbbi Patoloji',
      'Tıbbi Farmakoloji',
      'İç Hastalıkları',
      'Enfeksiyon Hastalıkları',
      'Kardiyoloji & Göğüs Hastalıkları',
      'Pediatri',
      'Acil Tıp & Ortopedi',
      'Nöroloji & Psikiyatri',
      'Tıbbi Genetik & Biyokimya',
      'Halk Sağlığı'
    ]
  },
  {
    id: 'donem3-butunleme',
    name: 'Dönem 3 - TIP 300: Bütünleme Sınavı',
    year: 3,
    term: '2026-2027 Bütünleme',
    targetCount: 150,
    code: 'TIP 300',
    examDate: '16 Temmuz 2027',
    description: 'Tüm Kurul 1-6 komitelerini kapsayan 150 soruluk genel yıl sonu bütünleme sınavı.',
    disciplines: [
      'Tıbbi Patoloji',
      'Tıbbi Farmakoloji',
      'İç Hastalıkları',
      'Enfeksiyon Hastalıkları',
      'Kardiyoloji & Göğüs Hastalıkları',
      'Pediatri',
      'Acil Tıp & Ortopedi',
      'Nöroloji & Psikiyatri',
      'Tıbbi Genetik & Biyokimya',
      'Halk Sağlığı'
    ]
  }
];

// 2026-2027 dönemine ait kurullarda henüz sınava girilmediği için aktif soru havuzu boştur.
export const INITIAL_QUESTIONS: QuestionItem[] = [];

export class FirestoreDbService {
  /**
   * Fetches committees from Firestore. If Firestore is empty, seeds initial committees.
   */
  static async getCommittees(): Promise<Committee[]> {
    try {
      const snap = await withTimeout(getDocs(collection(db, COMMITTEES_COLLECTION)));
      if (!snap.empty) {
        const list: Committee[] = [];
        snap.forEach((d) => {
          list.push(d.data() as Committee);
        });
        return list.sort((a, b) => (COMMITTEE_SORT_ORDER[a.id] || 99) - (COMMITTEE_SORT_ORDER[b.id] || 99) || a.name.localeCompare(b.name));
      }

      // Seed initial committees
      console.log('Seeding initial committees into Firestore...');
      for (const c of INITIAL_COMMITTEES) {
        await withTimeout(setDoc(doc(db, COMMITTEES_COLLECTION, c.id), c), 3000).catch((e) => {
          console.warn('Initial committee seed single err:', e);
        });
      }
      return INITIAL_COMMITTEES;
    } catch (err) {
      console.warn('Firestore getCommittees failed or timed out, falling back to local:', err);
      throw err;
    }
  }

  /**
   * Creates or updates a committee in Firestore
   */
  static async createCommittee(committee: Committee): Promise<Committee> {
    const cleaned = cleanForFirestore(committee);
    await withTimeout(setDoc(doc(db, COMMITTEES_COLLECTION, committee.id), cleaned), 4000);
    return committee;
  }

  /**
   * Fetches questions for a committee from Firestore. If empty for the first committee, seeds default questions.
   */
  static async getQuestions(committeeId: string): Promise<QuestionItem[]> {
    try {
      const qRef = collection(db, QUESTIONS_COLLECTION);
      const qQuery = query(qRef, where('committeeId', '==', committeeId));
      const snap = await withTimeout(getDocs(qQuery));

      if (!snap.empty) {
        const list: QuestionItem[] = [];
        snap.forEach((d) => {
          const item = d.data() as QuestionItem;
          // Sadece sınavı tamamlanmış güncel 2026-2027 sorularını dahil et, çıkmış soruları hariç tut
          if (!item.isPastExam && item.examYear === '2026-2027') {
            list.push(item);
          }
        });
        return list.sort((a, b) => a.questionNumber - b.questionNumber);
      }

      return [];
    } catch (err) {
      console.warn('Firestore getQuestions failed or timed out, falling back:', err);
      throw err;
    }
  }

  /**
   * Saves or updates a single question in Firestore
   */
  static async saveQuestion(question: QuestionItem): Promise<QuestionItem> {
    const updated = {
      ...question,
      updatedAt: new Date().toISOString(),
    };
    const cleaned = cleanForFirestore(updated);
    await withTimeout(setDoc(doc(db, QUESTIONS_COLLECTION, question.id), cleaned), 4000);
    return updated;
  }

  /**
   * Batch creates or updates multiple questions in Firebase Firestore.
   * Splits into safe chunks of up to 100 questions, applies cleanForFirestore,
   * ensures zero initial likes, and provides resilient timeouts.
   */
  static async batchSaveQuestions(questions: QuestionItem[]): Promise<{ success: boolean; count: number }> {
    if (!questions || questions.length === 0) return { success: true, count: 0 };

    const chunkSize = 100;
    let savedTotal = 0;

    for (let i = 0; i < questions.length; i += chunkSize) {
      const chunk = questions.slice(i, i + chunkSize);
      const batch = writeBatch(db);

      for (const q of chunk) {
        const ref = doc(db, QUESTIONS_COLLECTION, q.id);
        const formatted: QuestionItem = {
          ...q,
          upvotes: typeof q.upvotes === 'number' ? q.upvotes : 0,
          likedBy: Array.isArray(q.likedBy) ? q.likedBy : [],
          options: (q.options || []).map((opt) => ({
            ...opt,
            upvotes: typeof opt.upvotes === 'number' ? opt.upvotes : 0,
            likedBy: Array.isArray(opt.likedBy) ? opt.likedBy : [],
          })),
          fragments: (q.fragments || []).map((frag) => ({
            ...frag,
            upvotes: typeof frag.upvotes === 'number' ? frag.upvotes : 0,
            likedBy: Array.isArray(frag.likedBy) ? frag.likedBy : [],
          })),
          updatedAt: new Date().toISOString(),
        };

        const cleaned = cleanForFirestore(formatted);
        batch.set(ref, cleaned, { merge: true });
      }

      // Allow 25 seconds per chunk of 100 questions
      await withTimeout(batch.commit(), 25000);
      savedTotal += chunk.length;
    }

    return { success: true, count: savedTotal };
  }

  /**
   * Deletes a question from Firestore
   */
  static async deleteQuestion(questionId: string): Promise<void> {
    await withTimeout(deleteDoc(doc(db, QUESTIONS_COLLECTION, questionId)), 4000);
  }

  /**
   * Logs an admin notification into Firestore
   */
  static async logAdminNotification(notif: AdminNotification): Promise<void> {
    try {
      const ref = doc(db, NOTIFICATIONS_COLLECTION, notif.id);
      await withTimeout(setDoc(ref, cleanForFirestore(notif)), 3000);
    } catch (e) {
      console.warn('logAdminNotification fallback:', e);
    }
  }

  /**
   * Fetches latest admin notifications
   */
  static async getAdminNotifications(): Promise<AdminNotification[]> {
    try {
      const snap = await withTimeout(getDocs(collection(db, NOTIFICATIONS_COLLECTION)), 4000);
      const list: AdminNotification[] = [];
      snap.forEach((d) => list.push(d.data() as AdminNotification));
      return list.sort(
        (a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
      );
    } catch (e) {
      console.warn('getAdminNotifications fallback:', e);
      return [];
    }
  }

  /**
   * Fetches all registered users from Firestore users collection.
   */
  static async getRegisteredUsers(): Promise<any[]> {
    try {
      const snap = await withTimeout(getDocs(collection(db, 'users')), 4000);
      const list: any[] = [];
      snap.forEach((d) => list.push(d.data()));
      return list;
    } catch (e) {
      console.warn('Firestore getRegisteredUsers fallback:', e);
      return [];
    }
  }

  /**
   * Fetches all lecture notes from Firestore 'lecture_notes' collection
   */
  static async getLectureNotes(): Promise<LectureNote[]> {
    try {
      const snap = await withTimeout(getDocs(collection(db, LECTURE_NOTES_COLLECTION)), 8000);
      const list: LectureNote[] = [];
      snap.forEach((d) => list.push(d.data() as LectureNote));
      return list;
    } catch (e) {
      console.warn('Firestore getLectureNotes fallback:', e);
      return [];
    }
  }

  /**
   * Fetches all past exam questions from Firestore
   */
  static async getAllPastQuestions(): Promise<QuestionItem[]> {
    try {
      // 1. Önce doğrudan past_questions koleksiyonunu kontrol et
      try {
        const pastSnap = await withTimeout(getDocs(collection(db, PAST_QUESTIONS_COLLECTION)), 8000);
        if (!pastSnap.empty) {
          const list: QuestionItem[] = [];
          pastSnap.forEach((d) => {
            const data = d.data() as QuestionItem;
            if (data.id?.startsWith('civan-')) return;
            if (data.tags?.some((t: string) => /civan/i.test(t))) return;
            list.push(data);
          });
          if (list.length > 0) return list;
        }
      } catch (_) {}

      // 2. Fallback olarak questions koleksiyonundan çıkmış soruları filtrele
      const snap = await withTimeout(getDocs(collection(db, QUESTIONS_COLLECTION)), 15000);
      const list: QuestionItem[] = [];
      snap.forEach((d) => {
        const data = d.data() as QuestionItem;
        // Strictly exclude Civan notes
        if (data.id?.startsWith('civan-')) return;
        if (data.tags?.some((t: string) => /civan/i.test(t))) return;
        if (data.author && /civan/i.test(data.author)) return;

        if (data.isPastExam || data.id?.startsWith('past-') || data.id?.startsWith('q-') || data.examYear) {
          // Normalize year
          let year = data.examYear;
          if (!year || year.includes('2026')) {
            const detected = (data.tags || []).find((t: string) => /(?:19\d{2}|20[0-2][0-5])/.test(t));
            year = detected ? detected.match(/(?:19\d{2}|20[0-2][0-5])/)?.[0] || 'Kategorisiz' : 'Kategorisiz';
          }
          data.examYear = year;

          // Ambiguity check
          const stem = (data.reconstruction?.stem || data.fragments?.[0]?.text || data.rawStem || data.topic || '').trim();
          const opts = data.reconstruction?.options || data.options || [];
          const validOpts = opts.filter((o: any) => o && o.text && o.text.trim().length > 0);
          data.isAmbiguous = stem.length < 25 || validOpts.length < 2;

          if (!data.sourceFile) {
            data.sourceFile = (data.tags || []).find((t: string) => t.toLowerCase().endsWith('.pdf')) || 'Çıkmış Sınav Arşivi';
          }

          list.push(data);
        }
      });
      return list;
    } catch (e) {
      console.warn('Firestore getAllPastQuestions fallback:', e);
      return [];
    }
  }

  /**
   * Update or create a past exam question in Firestore 'past_questions' collection
   */
  static async updatePastQuestion(question: QuestionItem): Promise<boolean> {
    try {
      if (!question.id) return false;
      const docRef = doc(db, 'past_questions', question.id);
      await setDoc(docRef, cleanForFirestore(question), { merge: true });
      return true;
    } catch (err: any) {
      console.warn('Firestore updatePastQuestion error:', err.message);
      return false;
    }
  }

  /**
   * Fetches latest local PC background worker heartbeat from Firestore
   */
  static async getWorkerHeartbeat(): Promise<any | null> {
    try {
      const snap = await withTimeout(getDoc(doc(db, 'system_status', 'worker_heartbeat')), 3500);
      return snap.exists() ? snap.data() : null;
    } catch (e) {
      return null;
    }
  }

  /**
   * Realtime subscription to local PC background worker heartbeat
   */
  static subscribeWorkerHeartbeat(callback: (data: any | null) => void): () => void {
    try {
      const unsub = onSnapshot(doc(db, 'system_status', 'worker_heartbeat'), (snap) => {
        callback(snap.exists() ? snap.data() : null);
      }, (err) => {
        console.warn('Worker heartbeat subscription error:', err.message);
      });
      return unsub;
    } catch (e) {
      return () => {};
    }
  }

  /**
   * Fetches latest AI Subagent monitor telemetry from Firestore
   */
  static async getSubagentMonitorStatus(): Promise<any | null> {
    try {
      const snap = await withTimeout(getDoc(doc(db, 'system_status', 'ai_subagent_monitor')), 3500);
      return snap.exists() ? snap.data() : null;
    } catch (e) {
      return null;
    }
  }

  /**
   * Realtime subscription to AI Subagent monitor telemetry
   */
  static subscribeSubagentMonitor(callback: (data: any | null) => void): () => void {
    try {
      const unsub = onSnapshot(doc(db, 'system_status', 'ai_subagent_monitor'), (snap) => {
        callback(snap.exists() ? snap.data() : null);
      }, (err) => {
        console.warn('Subagent monitor subscription error:', err.message);
      });
      return unsub;
    } catch (e) {
      return () => {};
    }
  }

  /**
   * Sends an admin command to the background daemon via Firestore queue
   * (e.g. 'run_full_local_sync', 'run_redactor_cycle', 'install_service', 'stop_service')
   */
  static async sendAdminCommand(command: string, payload: any = {}, requestedBy: string = 'nofrostlife@gmail.com'): Promise<{ success: boolean; commandId?: string; message: string }> {
    try {
      const ref = await addDoc(collection(db, 'admin_commands'), {
        command,
        payload,
        requestedBy,
        status: 'pending',
        createdAt: new Date().toISOString(),
        timestamp: Date.now()
      });
      return {
        success: true,
        commandId: ref.id,
        message: 'Komut bulut kuyruğuna iletildi. Yerel bilgisayarınızdaki servis işleme alıyor...'
      };
    } catch (err: any) {
      console.warn('sendAdminCommand error:', err.message);
      return {
        success: false,
        message: 'Komut iletilemedi: ' + err.message
      };
    }
  }
}
