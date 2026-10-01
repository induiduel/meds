import { 
  getFirestore, 
  collection, 
  doc, 
  getDocs, 
  setDoc, 
  deleteDoc, 
  query, 
  where, 
  writeBatch
} from 'firebase/firestore';
import { auth } from './auth';
import { Committee, QuestionItem, AdminNotification } from '../types';
import firebaseConfig from '../../firebase-applet-config.json';

// Initialize Firestore using the configured database ID
const firestoreDatabaseId = firebaseConfig.firestoreDatabaseId || undefined;
export const db = firestoreDatabaseId
  ? getFirestore(auth.app, firestoreDatabaseId)
  : getFirestore(auth.app);

export const COMMITTEES_COLLECTION = 'committees';
export const QUESTIONS_COLLECTION = 'questions';
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

export const INITIAL_QUESTIONS: QuestionItem[] = [
  {
    id: 'q-101',
    committeeId: 'donem3-kurul2',
    questionNumber: 14,
    discipline: 'Tıbbi Farmakoloji',
    topic: 'Antihipertansif İlaçlar & Bradikinin Yolağı',
    status: 'completed',
    claimedAnswer: 'D',
    tags: ['ACE İnhibitörü', 'Kuru Öksürük', 'Bradikinin', 'Substans P', 'Kininaz II'],
    createdAt: new Date(Date.now() - 3600000 * 24).toISOString(),
    updatedAt: new Date().toISOString(),
    fragments: [
      {
        id: 'f-1',
        author: 'Dr. Adayı M.',
        text: 'Farmada kaptopril/enalapril kullanan hastada kuru öksürüğün nedeni soruldu.',
        type: 'stem',
        timestamp: new Date(Date.now() - 3600000 * 20).toISOString(),
        upvotes: 12,
      },
      {
        id: 'f-2',
        author: 'Sınavzede_99',
        text: 'Soru kökü tam olarak: "Aşağıdaki mediyatörlerden hangisinin bronşiyal mukozada yıkımının azalması ve birikimi kuru öksürükten primer sorumludur?" gibiydi.',
        type: 'stem',
        timestamp: new Date(Date.now() - 3600000 * 18).toISOString(),
        upvotes: 15,
      },
      {
        id: 'f-3',
        author: 'Klinisyen35',
        text: 'Şıklarda Bradikinin ve Substans P vardı. Cevap Bradikinin (D şıkkıydı). Çeldirici olarak Anjiyotensin II, Renin ve Prostoglandin E2 konmuştu.',
        type: 'option',
        timestamp: new Date(Date.now() - 3600000 * 14).toISOString(),
        upvotes: 18,
      },
    ],
    options: [
      { key: 'A', text: 'Anjiyotensin II sentezinin artması', suggestedBy: 'Klinisyen35', upvotes: 2 },
      { key: 'B', text: 'Renin salgılanmasının aşırı uyarılması', suggestedBy: 'Klinisyen35', upvotes: 1 },
      { key: 'C', text: 'Prostaglandin E2 sentezinin selektif blokajı', suggestedBy: 'Klinisyen35', upvotes: 3 },
      { key: 'D', text: 'Bradikinin ve Substans P yıkımının azalması ve akciğerde birikimi', suggestedBy: 'Klinisyen35', upvotes: 22 },
      { key: 'E', text: 'Bronşiyal beta-2 adrenerjik reseptör desensitizasyonu', suggestedBy: 'AI Reconstructor', upvotes: 5 },
    ],
    reconstruction: {
      stem: '58 yaşında esansiyel hipertansiyon tanısıyla enalapril tedavisi başlanan erkek hastada 3 hafta sonra tedaviye dirençli, balgamsız inatçı kuru öksürük gelişmiştir.\n\nBu klinik tablonun ortaya çıkmasında akciğer dokusunda yıkımı inhibe edilerek biriken ve C-liflerini uyararak öksürük refleksini tetikleyen temel mediyatör aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Anjiyotensin II', isAiFilled: false },
        { key: 'B', text: 'Plazma Renini', isAiFilled: false },
        { key: 'C', text: 'Tromboksan A2', isAiFilled: false },
        { key: 'D', text: 'Bradikinin (ve Substans P)', isAiFilled: false },
        { key: 'E', text: 'Endotelin-1', isAiFilled: true },
      ],
      correctAnswer: 'D',
      explanation: 'ACE inhibitörleri (örneğin kaptopril, enalapril, lisinopril), kininaz II enzimi ile özdeş olan ACE enzimini bloke eder. Kininaz II normalde bradikinin ve substans P\'yi yıkar. Enzim inhibe olunca hava yollarında bradikinin ve substans P birikerek akciğer C-liflerini uyarır ve karakteristik inatçı kuru öksürüğe yol açar.',
      confidenceScore: 98,
      notesAndDiscrepancies: 'Tüm öğrenci hafızaları ve şıkları %100 uyumludur. E şıkkı sınav standardında çeldirici olarak AI tarafından dengelenmiştir.',
      lastUpdated: new Date().toISOString(),
    },
  },
  {
    id: 'q-102',
    committeeId: 'donem3-kurul2',
    questionNumber: 27,
    discipline: 'Patoloji',
    topic: 'Miyokard İnfarktüsü Histopatolojisi',
    status: 'gathering',
    claimedAnswer: 'B',
    tags: ['Koagülasyon Nekrozu', 'Nötrofil İnfiltrasyonu', 'Dalgalı Lifler'],
    createdAt: new Date(Date.now() - 3600000 * 12).toISOString(),
    updatedAt: new Date().toISOString(),
    fragments: [
      {
        id: 'f-4',
        author: 'Cemre T.',
        text: 'Patolojide MI süresi sorusu vardı. 1-3. günlerde mikroskopta ne görülür diye sorulmuştu.',
        type: 'stem',
        timestamp: new Date(Date.now() - 3600000 * 10).toISOString(),
        upvotes: 7,
      },
      {
        id: 'f-5',
        author: 'Ahmet K.',
        text: 'Şıklarda nötrofil infiltrasyonu ve yoğun koagülasyon nekrozu vardı. 4-7. günde makrofajlar geliyordu, o yüzden cevap nötrofillerdi.',
        type: 'option',
        timestamp: new Date(Date.now() - 3600000 * 8).toISOString(),
        upvotes: 6,
      },
      {
        id: 'f-6',
        author: 'Zeynep H.',
        text: 'Hoca slaytta sarı-kahverengi yumuşama ve yoğun nötrofilik infiltrasyon vurgusu yapmıştı.',
        type: 'clue',
        timestamp: new Date(Date.now() - 3600000 * 5).toISOString(),
        upvotes: 5,
      },
    ],
    options: [
      { key: 'A', text: 'Dalgalı lifler (wavy fibers) ve ödem', suggestedBy: 'Cemre', upvotes: 2 },
      { key: 'B', text: 'Yoğun koagülasyon nekrozu ve bol nötrofil infiltrasyonu', suggestedBy: 'Ahmet K.', upvotes: 9 },
      { key: 'C', text: 'Makrofaj fagositozu ve granülasyon dokusu başlangıcı', suggestedBy: 'Zeynep H.', upvotes: 3 },
    ],
  },
  {
    id: 'q-103',
    committeeId: 'donem3-kurul2',
    questionNumber: 42,
    discipline: 'Tıbbi Mikrobiyoloji',
    topic: 'Atipik Pnömoni Etkenleri',
    status: 'gathering',
    tags: ['Legionella', 'Klima', 'Hiponatremi', 'BCYE Agar'],
    createdAt: new Date(Date.now() - 3600000 * 6).toISOString(),
    updatedAt: new Date().toISOString(),
    fragments: [
      {
        id: 'f-7',
        author: 'Ozan B.',
        text: 'Otelde kalan yaşlı adam klimalı ortamdan sonra yüksek ateş, ishal ve bilinç bulanıklığı ile geliyor. Sodyumu 126 mg/dL (hiponatremi). Etken soruldu.',
        type: 'stem',
        timestamp: new Date(Date.now() - 3600000 * 5).toISOString(),
        upvotes: 11,
      },
      {
        id: 'f-8',
        author: 'Deniz S.',
        text: 'İdrarda antijen testiyle tanı konan sorulmuştu. Cevap kesinlikle Legionella pneumophila.',
        type: 'clue',
        timestamp: new Date(Date.now() - 3600000 * 3).toISOString(),
        upvotes: 14,
      },
    ],
    options: [
      { key: 'A', text: 'Mycoplasma pneumoniae', suggestedBy: 'Ozan', upvotes: 1 },
      { key: 'B', text: 'Legionella pneumophila', suggestedBy: 'Deniz S.', upvotes: 16 },
      { key: 'C', text: 'Chlamydophila pneumoniae', suggestedBy: 'Soru Grubu', upvotes: 0 },
      { key: 'D', text: 'Streptococcus pneumoniae', suggestedBy: 'Soru Grubu', upvotes: 2 },
    ],
    claimedAnswer: 'B',
  }
];

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
          list.push(d.data() as QuestionItem);
        });
        return list.sort((a, b) => a.questionNumber - b.questionNumber);
      }

      // If this is donem3-kurul2 and it's empty, seed initial sample questions
      if (committeeId === 'donem3-kurul2') {
        console.log('Seeding initial questions for donem3-kurul2 into Firestore...');
        for (const q of INITIAL_QUESTIONS) {
          const cleaned = cleanForFirestore(q);
          await withTimeout(setDoc(doc(db, QUESTIONS_COLLECTION, q.id), cleaned), 3000).catch(() => {});
        }
        return INITIAL_QUESTIONS;
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
   * Batch creates or updates multiple questions
   */
  static async batchSaveQuestions(questions: QuestionItem[]): Promise<void> {
    const batch = writeBatch(db);
    for (const q of questions) {
      const ref = doc(db, QUESTIONS_COLLECTION, q.id);
      const cleaned = cleanForFirestore({
        ...q,
        updatedAt: new Date().toISOString(),
      });
      batch.set(ref, cleaned);
    }
    await withTimeout(batch.commit(), 5000);
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
}
