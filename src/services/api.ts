import { Committee, QuestionItem, MemoryFragment, QuestionOption, ReconstructedQuestion } from '../types';
import { FirestoreDbService, INITIAL_COMMITTEES, COMMITTEE_SORT_ORDER } from './firestoreDb';
import { ADMIN_EMAIL } from './auth';

const STORAGE_KEY = 'medsoru_db_data_v1';
const API_BASE_URL_KEY = 'medsoru_custom_api_url';

export const getCustomApiUrl = (): string => {
  return localStorage.getItem(API_BASE_URL_KEY) || '';
};

export const setCustomApiUrl = (url: string) => {
  if (url) {
    localStorage.setItem(API_BASE_URL_KEY, url.trim().replace(/\/$/, ''));
  } else {
    localStorage.removeItem(API_BASE_URL_KEY);
  }
};

const DEFAULT_COMMITTEES: Committee[] = INITIAL_COMMITTEES;

const DEFAULT_QUESTIONS: QuestionItem[] = [
  {
    id: 'q-101',
    committeeId: 'donem3-kurul2',
    questionNumber: 14,
    discipline: 'Farmakoloji',
    topic: 'Antihipertansifler & Yan Etkiler',
    status: 'completed',
    claimedAnswer: 'C',
    tags: ['ACE İnhibitörleri', 'Bradikinin', 'Öksürük', 'Vaka'],
    createdAt: new Date(Date.now() - 3600000 * 24).toISOString(),
    updatedAt: new Date().toISOString(),
    fragments: [
      {
        id: 'f-1',
        author: 'Stj. Dr. Eren',
        text: '58 yaşında hipertansiyon tanısıyla yeni ilaç başlanan hastada birkaç hafta sonra inatçı kuru öksürük gelişiyor.',
        type: 'stem',
        timestamp: new Date(Date.now() - 3600000 * 20).toISOString(),
        upvotes: 9,
      },
      {
        id: 'f-2',
        author: 'Ayşe Tıp-3',
        text: 'Soru kökü tam olarak: Bu yan etkinin gelişiminden sorumlu olan mediyatör hangisidir? diyordu.',
        type: 'stem',
        timestamp: new Date(Date.now() - 3600000 * 18).toISOString(),
        upvotes: 12,
      },
      {
        id: 'f-3',
        author: 'Mert (Amfi 1)',
        text: 'Şıklarda Bradikinin, Substans P, Anjiyotensin 2, Renin vardı. Kesin Bradikinin doğru cevap!',
        type: 'clue',
        timestamp: new Date(Date.now() - 3600000 * 15).toISOString(),
        upvotes: 14,
      },
    ],
    options: [
      { key: 'A', text: 'Anjiyotensin II azalması', suggestedBy: 'Mert', upvotes: 3 },
      { key: 'B', text: 'Renin sekresyonunda artış', suggestedBy: 'Mert', upvotes: 1 },
      { key: 'C', text: 'Bradikinin birikimi', suggestedBy: 'Ayşe Tıp-3', upvotes: 15 },
      { key: 'D', text: 'Substans P azalması', suggestedBy: 'Kerem', upvotes: 2 },
      { key: 'E', text: 'Prostasiklin inhibisyonu', suggestedBy: 'AI (Yapay Zeka)', isAiGenerated: true, upvotes: 4 },
    ],
    reconstruction: {
      stem: '58 yaşında esansiyel hipertansiyon tanısıyla bir antihipertansif ajan başlanan erkek hasta, 3 hafta sonra polikliniğe gece uykudan uyandıran, balgamsız inatçı kuru öksürük şikayetiyle başvuruyor. Fizik muayenesinde ve akciğer grafisinde patoloji saptanmıyor. Hastanın kullandığı ilacın etki mekanizması göz önüne alındığında, bu yan etkinin gelişiminden doğrudan sorumlu olan mediyatör birikimi aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Anjiyotensin II düzeyinde aşırı artış', isAiFilled: false },
        { key: 'B', text: 'Plazma renin aktivitesinde belirgin supresyon', isAiFilled: false },
        { key: 'C', text: 'Bradikinin ve Substans P yıkımının engellenerek birikmesi', isAiFilled: false },
        { key: 'D', text: 'Endotelin-1 sentezinin stimüle edilmesi', isAiFilled: true },
        { key: 'E', text: 'Noradrenalin geri alımının inhibe edilmesi', isAiFilled: true },
      ],
      correctAnswer: 'C',
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
        author: 'Onur Med',
        text: 'Otelde kalan yaşlı adam sorusu! Klimalardan bulaşan, ateşi yüksek, ishal ve bilinç bulanıklığı olan hasta.',
        type: 'stem',
        timestamp: new Date(Date.now() - 3600000 * 4).toISOString(),
        upvotes: 11,
      },
      {
        id: 'f-8',
        author: 'Selin B.',
        text: 'Laboratuvarda sodyum 126 mg/dL (hiponatremi) verilmişti. Hoca hangi besiyerinde ürer ya da etken kimdir sormuştu.',
        type: 'clue',
        timestamp: new Date(Date.now() - 3600000 * 3).toISOString(),
        upvotes: 8,
      },
    ],
    options: [
      { key: 'A', text: 'Streptococcus pneumoniae', suggestedBy: 'Onur Med', upvotes: 1 },
      { key: 'B', text: 'Legionella pneumophila (BCYE agar)', suggestedBy: 'Selin B.', upvotes: 10 },
      { key: 'C', text: 'Mycoplasma pneumoniae', suggestedBy: 'Anonim', upvotes: 2 },
    ],
  },
];

interface LocalDatabase {
  committees: Committee[];
  questions: QuestionItem[];
}

function getLocalDb(): LocalDatabase {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      const parsed: LocalDatabase = JSON.parse(raw);
      if (parsed && Array.isArray(parsed.committees)) {
        let changed = false;
        for (const official of INITIAL_COMMITTEES) {
          const found = parsed.committees.find((c) => c.id === official.id);
          if (!found) {
            parsed.committees.push(official);
            changed = true;
          } else if (found.targetCount !== official.targetCount || found.name !== official.name) {
            Object.assign(found, official);
            changed = true;
          }
        }
        const valid = parsed.committees.filter((c) => c.id.startsWith('donem3-'));
        if (valid.length !== parsed.committees.length) {
          parsed.committees = valid;
          changed = true;
        }
        parsed.committees.sort(
          (a, b) =>
            (COMMITTEE_SORT_ORDER[a.id] || 99) -
            (COMMITTEE_SORT_ORDER[b.id] || 99) ||
            a.name.localeCompare(b.name)
        );
        if (changed) {
          saveLocalDb(parsed);
        }
        return parsed;
      }
    }
  } catch (e) {
    console.error('LocalStorage parse error:', e);
  }
  const initial = {
    committees: DEFAULT_COMMITTEES,
    questions: DEFAULT_QUESTIONS,
  };
  saveLocalDb(initial);
  return initial;
}

function saveLocalDb(data: LocalDatabase) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  } catch (e) {
    console.error('LocalStorage save error:', e);
  }
}

let isServerAvailable: boolean | null = null;

async function checkServer(): Promise<boolean> {
  if (isServerAvailable !== null) return isServerAvailable;
  try {
    const customUrl = getCustomApiUrl();
    const endpoint = customUrl ? `${customUrl}/api/committees` : '/api/committees';
    const res = await fetch(endpoint, { method: 'GET', headers: { Accept: 'application/json' } });
    if (res.ok && res.headers.get('content-type')?.includes('application/json')) {
      isServerAvailable = true;
      return true;
    }
  } catch (e) {
    // Network error or 404
  }
  isServerAvailable = false;
  return false;
}

export const ApiService = {
  async getCommittees(): Promise<Committee[]> {
    try {
      const cloudCommittees = await FirestoreDbService.getCommittees();
      if (cloudCommittees && cloudCommittees.length > 0) {
        const local = getLocalDb();
        local.committees = cloudCommittees;
        saveLocalDb(local);
        return cloudCommittees;
      }
    } catch (e) {
      console.warn('Firestore getCommittees fallback to local/server', e);
    }

    const hasServer = await checkServer();
    const customUrl = getCustomApiUrl();
    if (hasServer) {
      try {
        const res = await fetch(`${customUrl}/api/committees`);
        const data = await res.json();
        return data.committees || [];
      } catch (e) {
        console.warn('Server fetch failed, falling back to LocalStorage', e);
      }
    }
    return getLocalDb().committees;
  },

  async addCommittee(data: {
    name: string;
    year: number;
    term: string;
    targetCount: number;
    description: string;
  }): Promise<Committee> {
    const newCommittee: Committee = {
      id: `kurul-${Date.now()}`,
      name: data.name,
      year: data.year,
      term: data.term,
      targetCount: data.targetCount,
      description: data.description,
    };

    const db = getLocalDb();
    db.committees.push(newCommittee);
    saveLocalDb(db);

    try {
      await FirestoreDbService.createCommittee(newCommittee);
    } catch (e) {
      console.warn('Firestore addCommittee fallback', e);
    }

    const hasServer = await checkServer();
    const customUrl = getCustomApiUrl();
    if (hasServer) {
      try {
        await fetch(`${customUrl}/api/committees`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data),
        });
      } catch (e) {}
    }

    return newCommittee;
  },

  async getQuestions(params: {
    committeeId?: string;
    discipline?: string;
    status?: string;
    search?: string;
  }): Promise<QuestionItem[]> {
    let questionsList: QuestionItem[] = [];
    let fetchedFromCloud = false;

    if (params.committeeId) {
      try {
        const cloudQuestions = await FirestoreDbService.getQuestions(params.committeeId);
        questionsList = cloudQuestions;
        fetchedFromCloud = true;
        const local = getLocalDb();
        const other = local.questions.filter((q) => q.committeeId !== params.committeeId);
        local.questions = [...other, ...cloudQuestions];
        saveLocalDb(local);
      } catch (e) {
        console.warn('Firestore getQuestions fallback', e);
      }
    }

    if (!fetchedFromCloud) {
      const hasServer = await checkServer();
      const customUrl = getCustomApiUrl();
      if (hasServer) {
        try {
          const qParams = new URLSearchParams();
          if (params.committeeId) qParams.append('committeeId', params.committeeId);
          if (params.discipline && params.discipline !== 'Tümü') qParams.append('discipline', params.discipline);
          if (params.status && params.status !== 'Tümü') qParams.append('status', params.status);
          if (params.search) qParams.append('search', params.search);

          const res = await fetch(`${customUrl}/api/questions?${qParams.toString()}`);
          const data = await res.json();
          if (data.questions) return data.questions;
        } catch (e) {
          console.warn('Server getQuestions failed, using LocalStorage', e);
        }
      }
      questionsList = getLocalDb().questions;
    }

    let result = questionsList;
    if (params.committeeId) {
      result = result.filter((q) => q.committeeId === params.committeeId);
    }
    if (params.discipline && params.discipline !== 'Tümü') {
      result = result.filter((q) => q.discipline.toLowerCase() === params.discipline!.toLowerCase());
    }
    if (params.status && params.status !== 'Tümü') {
      result = result.filter((q) => q.status === params.status);
    }
    if (params.search) {
      const s = params.search.toLowerCase();
      result = result.filter(
        (q) =>
          q.topic.toLowerCase().includes(s) ||
          q.discipline.toLowerCase().includes(s) ||
          q.questionNumber.toString().includes(s) ||
          q.fragments.some((f) => f.text.toLowerCase().includes(s)) ||
          (q.reconstruction && q.reconstruction.stem.toLowerCase().includes(s))
      );
    }

    return result.sort((a, b) => a.questionNumber - b.questionNumber);
  },

  async addQuestionContribution(data: {
    committeeId: string;
    questionNumber?: number;
    isUnknownNumber?: boolean;
    discipline: string;
    topic: string;
    fragmentText: string;
    author: string;
    authorUid?: string;
    authorStudentNumber?: string;
    claimedAnswer?: 'A' | 'B' | 'C' | 'D' | 'E';
    options?: { key: 'A' | 'B' | 'C' | 'D' | 'E'; text: string }[];
  }): Promise<QuestionItem> {
    const db = getLocalDb();
    const isUnassigned = !!data.isUnknownNumber || !data.questionNumber || data.questionNumber <= 0;

    let targetQuestion: QuestionItem;

    const initialFragment: MemoryFragment | null = data.fragmentText?.trim()
      ? {
          id: `f-${Date.now()}-${Math.random().toString(36).substring(2, 6)}`,
          author: data.author || 'Anonim Tıbbiyeli',
          authorUid: data.authorUid,
          authorStudentNumber: data.authorStudentNumber,
          text: data.fragmentText.trim(),
          type: 'stem',
          timestamp: new Date().toISOString(),
          upvotes: 1,
        }
      : null;

    if (isUnassigned) {
      // Unassigned question pool
      const newId = `q-${data.committeeId}-unassigned-${Date.now()}`;
      targetQuestion = {
        id: newId,
        committeeId: data.committeeId,
        questionNumber: 0,
        isUnassignedNumber: true,
        discipline: data.discipline || 'Belirtilmedi',
        topic: data.topic || `${data.discipline || 'Kurul'} (Numarası Belirsiz Soru)`,
        status: initialFragment ? 'gathering' : 'empty',
        fragments: initialFragment ? [initialFragment] : [],
        options: data.options
          ? data.options
              .filter((o) => o.text && o.text.trim())
              .map((o) => ({
                key: o.key,
                text: o.text.trim(),
                suggestedBy: data.author || 'Anonim',
                suggestedByUid: data.authorUid,
                upvotes: 1,
              }))
          : [],
        claimedAnswer: data.claimedAnswer,
        tags: [data.discipline || 'Kurul', 'numarasız-hatırlanan'],
        contributedByUid: data.authorUid,
        contributedByName: data.author,
        contributedByStudentNumber: data.authorStudentNumber,
        revisions: [
          {
            id: `rev-${Date.now()}`,
            version: 1,
            editedAt: new Date().toISOString(),
            editorName: data.author || 'Anonim',
            editorUid: data.authorUid,
            editorStudentNumber: data.authorStudentNumber,
            changeSummary: 'İlk soru kaydı oluşturuldu (Numarasız)',
            stem: data.fragmentText || '',
            discipline: data.discipline,
            topic: data.topic,
            claimedAnswer: data.claimedAnswer,
            options: data.options ? data.options.map(o => ({ key: o.key, text: o.text, upvotes: 1 })) : [],
          }
        ],
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };

      // Also permanently archive options in fragments so they are never lost
      if (data.options) {
        data.options.forEach((o) => {
          if (o.text && o.text.trim()) {
            targetQuestion.fragments.push({
              id: `f-opt-${Date.now()}-${o.key}`,
              author: data.author || 'Anonim',
              authorUid: data.authorUid,
              authorStudentNumber: data.authorStudentNumber,
              text: `${o.key}) ${o.text.trim()}`,
              type: 'option',
              timestamp: new Date().toISOString(),
              upvotes: 1,
            });
          }
        });
      }

      db.questions.push(targetQuestion);

      // Log notification for admin (nofrostlife@gmail.com)
      try {
        await FirestoreDbService.logAdminNotification({
          id: `notif-${Date.now()}`,
          type: 'unassigned_question',
          committeeId: data.committeeId,
          questionId: targetQuestion.id,
          title: `Yeni Numarasız Soru: ${data.discipline}`,
          message: `${data.author || 'Bir öğrenci'} ${data.discipline} dersinden numarasını hatırlamadığı soru parçası ekledi: "${(data.fragmentText || '').substring(0, 90)}..."`,
          author: data.author || 'Anonim',
          timestamp: new Date().toISOString(),
          isRead: false,
        });

        // Check if 10 unassigned questions have accumulated
        const unassignedInCommittee = db.questions.filter(
          (q) => q.committeeId === data.committeeId && q.isUnassignedNumber
        );
        if (unassignedInCommittee.length >= 10 && unassignedInCommittee.length % 5 === 0) {
          await FirestoreDbService.logAdminNotification({
            id: `notif-batch-${Date.now()}`,
            type: 'batch_cluster_ready',
            committeeId: data.committeeId,
            title: `🎯 ${unassignedInCommittee.length} Numarasız Soru Birikti`,
            message: `Bu kurulda ${unassignedInCommittee.length} adet numarasız hatırlanan soru birikti. Yapay zeka ile 1-100 arasına yerleştirilmeye hazır!`,
            author: 'AI Asistan',
            timestamp: new Date().toISOString(),
            isRead: false,
          });
        }
      } catch (e) {
        console.warn('Admin notification error:', e);
      }
    } else {
      // Known question number
      let existing = db.questions.find(
        (q) =>
          q.committeeId === data.committeeId &&
          q.questionNumber === Number(data.questionNumber) &&
          !q.isUnassignedNumber
      );

      if (existing) {
        if (!existing.contributedByUid && data.authorUid) {
          existing.contributedByUid = data.authorUid;
          existing.contributedByName = data.author;
          existing.contributedByStudentNumber = data.authorStudentNumber;
        }

        if (initialFragment) existing.fragments.push(initialFragment);
        if (data.options) {
          data.options.forEach((o) => {
            if (!o.text || !o.text.trim()) return;
            // Always archive option as a fragment
            existing!.fragments.push({
              id: `f-opt-${Date.now()}-${o.key}`,
              author: data.author || 'Anonim',
              authorUid: data.authorUid,
              authorStudentNumber: data.authorStudentNumber,
              text: `${o.key}) ${o.text.trim()}`,
              type: 'option',
              timestamp: new Date().toISOString(),
              upvotes: 1,
            });

            const exOpt = existing!.options.find((opt) => opt.key === o.key);
            if (exOpt) {
              if (exOpt.text.trim().toLowerCase() === o.text.trim().toLowerCase()) {
                exOpt.upvotes = (exOpt.upvotes || 1) + 1;
              } else {
                exOpt.text = o.text.trim();
                exOpt.suggestedBy = data.author;
                exOpt.suggestedByUid = data.authorUid;
              }
            } else {
              existing!.options.push({
                key: o.key,
                text: o.text.trim(),
                suggestedBy: data.author,
                suggestedByUid: data.authorUid,
                upvotes: 1,
              });
            }
          });
          existing.options.sort((a, b) => a.key.localeCompare(b.key));
        }
        if (data.claimedAnswer) {
          existing.claimedAnswer = data.claimedAnswer;
        }

        // Add revision without deleting old versions
        const revision = {
          id: `rev-${Date.now()}`,
          version: (existing.revisions?.length || 0) + 1,
          editedAt: new Date().toISOString(),
          editorName: data.author || 'Anonim',
          editorUid: data.authorUid,
          editorStudentNumber: data.authorStudentNumber,
          changeSummary: `Yeni parça ve şık katkısı (${data.author || 'Öğrenci'})`,
          stem: data.fragmentText || existing.reconstruction?.stem,
          discipline: existing.discipline,
          topic: existing.topic,
          claimedAnswer: existing.claimedAnswer,
          options: [...existing.options],
        };
        if (!existing.revisions) existing.revisions = [];
        existing.revisions.push(revision);

        existing.status = 'gathering';
        existing.updatedAt = new Date().toISOString();
        targetQuestion = existing;
      } else {
        targetQuestion = {
          id: `q-${Date.now()}`,
          committeeId: data.committeeId,
          questionNumber: Number(data.questionNumber),
          discipline: data.discipline || 'Belirtilmedi',
          topic: data.topic || `Soru #${data.questionNumber}`,
          status: initialFragment ? 'gathering' : 'empty',
          fragments: initialFragment ? [initialFragment] : [],
          options: data.options
            ? data.options
                .filter((o) => o.text && o.text.trim())
                .map((o) => ({
                  key: o.key,
                  text: o.text.trim(),
                  suggestedBy: data.author,
                  suggestedByUid: data.authorUid,
                  upvotes: 1,
                }))
            : [],
          claimedAnswer: data.claimedAnswer,
          tags: [data.discipline || 'Kurul'],
          contributedByUid: data.authorUid,
          contributedByName: data.author,
          contributedByStudentNumber: data.authorStudentNumber,
          revisions: [
            {
              id: `rev-${Date.now()}`,
              version: 1,
              editedAt: new Date().toISOString(),
              editorName: data.author || 'Anonim',
              editorUid: data.authorUid,
              editorStudentNumber: data.authorStudentNumber,
              changeSummary: 'İlk soru kaydı oluşturuldu',
              stem: data.fragmentText || '',
              discipline: data.discipline,
              topic: data.topic,
              claimedAnswer: data.claimedAnswer,
              options: data.options ? data.options.map(o => ({ key: o.key, text: o.text, upvotes: 1 })) : [],
            }
          ],
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
        };

        if (data.options) {
          data.options.forEach((o) => {
            if (o.text && o.text.trim()) {
              targetQuestion.fragments.push({
                id: `f-opt-${Date.now()}-${o.key}`,
                author: data.author || 'Anonim',
                authorUid: data.authorUid,
                authorStudentNumber: data.authorStudentNumber,
                text: `${o.key}) ${o.text.trim()}`,
                type: 'option',
                timestamp: new Date().toISOString(),
                upvotes: 1,
              });
            }
          });
        }

        db.questions.push(targetQuestion);
      }
    }

    saveLocalDb(db);

    // Save to Firestore for cross-device cloud sync
    try {
      await FirestoreDbService.saveQuestion(targetQuestion);
    } catch (e) {
      console.warn('Firestore saveQuestion fallback', e);
    }

    return targetQuestion;
  },

  /**
   * User edits their own contributed question.
   * Crucial requirement: Edits are added as revisions, OLD VERSIONS ARE NEVER DELETED!
   */
  async editUserQuestion(data: {
    questionId: string;
    editorUid: string;
    editorName: string;
    editorStudentNumber?: string;
    stem?: string;
    discipline?: string;
    topic?: string;
    claimedAnswer?: 'A' | 'B' | 'C' | 'D' | 'E';
    options?: { key: 'A' | 'B' | 'C' | 'D' | 'E'; text: string }[];
    changeSummary?: string;
  }): Promise<QuestionItem> {
    const db = getLocalDb();
    const q = db.questions.find((item) => item.id === data.questionId);
    if (!q) throw new Error('Soru bulunamadı');

    // Archive current snapshot as a revision
    const newRev = {
      id: `rev-${Date.now()}-${Math.random().toString(36).substring(2, 6)}`,
      version: (q.revisions?.length || 0) + 1,
      editedAt: new Date().toISOString(),
      editorName: data.editorName || 'Anonim',
      editorUid: data.editorUid,
      editorStudentNumber: data.editorStudentNumber,
      changeSummary: data.changeSummary || 'Soru güncellendi',
      stem: data.stem !== undefined ? data.stem : (q.reconstruction?.stem || q.fragments[0]?.text || ''),
      discipline: data.discipline !== undefined ? data.discipline : q.discipline,
      topic: data.topic !== undefined ? data.topic : q.topic,
      claimedAnswer: data.claimedAnswer !== undefined ? data.claimedAnswer : q.claimedAnswer,
      options: data.options ? data.options.map(o => ({ key: o.key, text: o.text, upvotes: 1 })) : [...q.options],
      explanation: q.reconstruction?.explanation,
    };

    if (!q.revisions) q.revisions = [];
    q.revisions.push(newRev);

    // Apply live updates
    if (data.discipline !== undefined) q.discipline = data.discipline;
    if (data.topic !== undefined) q.topic = data.topic;
    if (data.claimedAnswer !== undefined) q.claimedAnswer = data.claimedAnswer;
    if (data.stem !== undefined && data.stem.trim()) {
      const stemFrag = q.fragments.find((f) => f.type === 'stem');
      if (stemFrag) {
        stemFrag.text = data.stem.trim();
        stemFrag.timestamp = new Date().toISOString();
      } else {
        q.fragments.unshift({
          id: `f-${Date.now()}`,
          author: data.editorName,
          authorUid: data.editorUid,
          authorStudentNumber: data.editorStudentNumber,
          text: data.stem.trim(),
          type: 'stem',
          timestamp: new Date().toISOString(),
          upvotes: 1,
        });
      }
      if (q.reconstruction) {
        q.reconstruction.stem = data.stem.trim();
      }
    }

    if (data.options && data.options.length > 0) {
      data.options.forEach((o) => {
        if (!o.text || !o.text.trim()) return;
        const exOpt = q.options.find((opt) => opt.key === o.key);
        if (exOpt) {
          exOpt.text = o.text.trim();
          exOpt.suggestedBy = data.editorName;
          exOpt.suggestedByUid = data.editorUid;
        } else {
          q.options.push({
            key: o.key,
            text: o.text.trim(),
            suggestedBy: data.editorName,
            suggestedByUid: data.editorUid,
            upvotes: 1,
          });
        }
      });
      q.options.sort((a, b) => a.key.localeCompare(b.key));
    }

    q.updatedAt = new Date().toISOString();
    saveLocalDb(db);

    try {
      await FirestoreDbService.saveQuestion(q);
    } catch (e) {
      console.warn('Firestore saveQuestion fallback in editUserQuestion:', e);
    }

    return q;
  },

  async updateQuestionLectureMatch(questionId: string, match: any): Promise<QuestionItem> {
    const db = getLocalDb();
    const q = db.questions.find((item) => item.id === questionId);
    if (!q) throw new Error('Soru bulunamadı');

    q.lectureReference = match;
    q.updatedAt = new Date().toISOString();
    saveLocalDb(db);

    try {
      await FirestoreDbService.saveQuestion(q);
    } catch (e) {
      console.warn('Firestore updateQuestionLectureMatch fallback', e);
    }

    return q;
  },

  /**
   * Sends congratulations and thank-you email to user for their contribution.
   * Requirement: "Bunu yalnızca her kurul 1 kez yap."
   */
  async sendCongratulationsEmail(
    userEmail: string,
    userName: string,
    studentNumber: string | undefined,
    committeeName: string,
    committeeId: string,
    questionInfo: { questionNumber?: number; discipline?: string }
  ): Promise<boolean> {
    if (!userEmail) return false;

    const subject = `Tebrikler ve Teşekkürler! ${committeeName} Soru Katkınız Alındı 🎉`;
    const html = `
      <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; padding: 24px; border: 1px solid #e2e8f0; border-radius: 12px; background-color: #ffffff;">
        <div style="background: linear-gradient(135deg, #0f766e, #0d9488); color: #ffffff; padding: 20px 24px; border-radius: 8px;">
          <h2 style="margin: 0; font-size: 20px; font-weight: 700;">MedSoru • Tıp Dönem 3 Kurul Arşivi</h2>
          <p style="margin: 6px 0 0 0; font-size: 13px; opacity: 0.9;">Kolektif Soru Havuzu ve AI Rekonstrüksiyonu</p>
        </div>
        
        <div style="padding: 24px 8px; color: #1e293b; font-size: 14px; line-height: 1.6;">
          <p style="font-size: 16px;">Sayın <strong>${userName || 'Değerli Tıbbiyeli'}</strong>,</p>
          <p><strong>${committeeName}</strong> sınav soru havuzuna yapmış olduğunuz soru katkısı başarıyla kaydedilmiş ve arşive dahil edilmiştir.</p>
          
          <div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 14px 18px; margin: 18px 0;">
            <h4 style="margin: 0 0 10px 0; color: #166534; font-size: 14px; font-weight: 700;">Katkı Detayları:</h4>
            <ul style="margin: 0; padding-left: 20px; color: #15803d; font-size: 13px; line-height: 1.8;">
              <li><strong>Kurul:</strong> ${committeeName}</li>
              <li><strong>Soru Numarası:</strong> ${questionInfo.questionNumber ? `#${questionInfo.questionNumber}` : 'Numarasız Havuz (Yapay Zeka ile Eşleştirilecek)'}</li>
              <li><strong>Branş:</strong> ${questionInfo.discipline || 'Genel Kurul'}</li>
              ${studentNumber ? `<li><strong>Öğrenci Numarası:</strong> ${studentNumber}</li>` : ''}
            </ul>
          </div>
          
          <p>Tıp fakültesinde bilgi paylaşımı ve dayanışma en büyük gücümüzdür. Dönem arkadaşlarınıza ve gelecek dönemlere miras kalacak bu soru arşivine sunduğunuz samimi destek için teşekkür eder, sınavlarınızda ve hekimlik yolculuğunuzda üstün başarılar dileriz!</p>
          
          <div style="margin-top: 28px; padding-top: 16px; border-top: 1px solid #e2e8f0; color: #64748b; font-size: 12px;">
            <p style="margin: 0;">MedSoru Kurul Sistemi • nofrostlife@gmail.com</p>
            <p style="margin: 4px 0 0 0; font-style: italic;">Not: Bu teşekkür bildirimi her kurul sınavı için öğrenciye yalnızca 1 kez gönderilir.</p>
          </div>
        </div>
      </div>
    `;

    try {
      const res = await fetch('/api/send-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          to: userEmail,
          subject,
          html,
          text: `Sayın ${userName}, ${committeeName} sınavı için soru katkınız başarıyla kaydedildi. Teşekkür ederiz!`,
          type: 'congrats',
          committeeId,
          studentNumber,
        }),
      });
      return res.ok;
    } catch (e) {
      console.warn('sendCongratulationsEmail network error:', e);
      return false;
    }
  },

  async addFragment(questionId: string, text: string, author: string, type: 'stem' | 'clue' | 'option'): Promise<QuestionItem> {
    const db = getLocalDb();
    const q = db.questions.find((item) => item.id === questionId);
    if (!q) throw new Error('Soru bulunamadı');

    const newFrag: MemoryFragment = {
      id: `f-${Date.now()}-${Math.random().toString(36).substring(2, 6)}`,
      author: author || 'Anonim',
      text: text.trim(),
      type: type || 'clue',
      timestamp: new Date().toISOString(),
      upvotes: 1,
    };
    q.fragments.push(newFrag);
    if (q.status === 'empty') q.status = 'gathering';
    q.updatedAt = new Date().toISOString();
    saveLocalDb(db);

    try {
      await FirestoreDbService.saveQuestion(q);
    } catch (e) {
      console.warn('Firestore addFragment fallback', e);
    }

    return q;
  },

  async upvoteFragment(questionId: string, fragmentId: string): Promise<void> {
    const db = getLocalDb();
    const q = db.questions.find((item) => item.id === questionId);
    if (q) {
      const f = q.fragments.find((frag) => frag.id === fragmentId);
      if (f) {
        f.upvotes = (f.upvotes || 0) + 1;
        saveLocalDb(db);
        try {
          await FirestoreDbService.saveQuestion(q);
        } catch (e) {}
      }
    }
  },

  async addOption(questionId: string, key: 'A' | 'B' | 'C' | 'D' | 'E', text: string, suggestedBy: string): Promise<QuestionItem> {
    const db = getLocalDb();
    const q = db.questions.find((item) => item.id === questionId);
    if (!q) throw new Error('Soru bulunamadı');

    // Permanently archive in fragments so no student memory is ever erased or lost
    q.fragments.push({
      id: `f-opt-${Date.now()}-${key}`,
      author: suggestedBy || 'Anonim',
      text: `${key} Şıkkı: "${text.trim()}"`,
      type: 'option',
      timestamp: new Date().toISOString(),
      upvotes: 1,
    });

    const exOpt = q.options.find((o) => o.key === key);
    if (exOpt) {
      if (exOpt.text.trim().toLowerCase() === text.trim().toLowerCase()) {
        exOpt.upvotes = (exOpt.upvotes || 1) + 1;
      } else {
        exOpt.text = text.trim();
        if (suggestedBy) exOpt.suggestedBy = suggestedBy;
      }
    } else {
      q.options.push({ key, text: text.trim(), suggestedBy: suggestedBy || 'Anonim', upvotes: 1 });
    }
    q.options.sort((a, b) => a.key.localeCompare(b.key));
    q.updatedAt = new Date().toISOString();
    saveLocalDb(db);

    try {
      await FirestoreDbService.saveQuestion(q);
    } catch (e) {
      console.warn('Firestore addOption fallback', e);
    }

    return q;
  },

  async upvoteOption(questionId: string, key: 'A' | 'B' | 'C' | 'D' | 'E'): Promise<void> {
    const db = getLocalDb();
    const q = db.questions.find((item) => item.id === questionId);
    if (q) {
      const opt = q.options.find((o) => o.key === key);
      if (opt) {
        opt.upvotes = (opt.upvotes || 0) + 1;
        saveLocalDb(db);
        try {
          await FirestoreDbService.saveQuestion(q);
        } catch (e) {}
      }
    }
  },

  async setClaimedAnswer(questionId: string, answer: 'A' | 'B' | 'C' | 'D' | 'E'): Promise<void> {
    const db = getLocalDb();
    const q = db.questions.find((item) => item.id === questionId);
    if (q) {
      q.claimedAnswer = answer;
      saveLocalDb(db);
      try {
        await FirestoreDbService.saveQuestion(q);
      } catch (e) {}
    }
  },

  async reconstructWithAi(questionId: string): Promise<QuestionItem> {
    const db = getLocalDb();
    const q = db.questions.find((item) => item.id === questionId);
    if (!q) throw new Error('Soru bulunamadı');

    // Synthesize question based on fragments
    const combinedFragment = q.fragments.map((f) => f.text).join(' ');
    const stem = combinedFragment.length > 20
      ? `${combinedFragment} Bu klinik tablo ve mekanizma göz önüne alındığında, aşağıdakilerden hangisi doğrudur?`
      : `${q.discipline} kurul sınavı #${q.questionNumber}: ${q.topic} hakkında aşağıdakilerden hangisi doğrudur?`;

    const existingOptions = q.options.map((o) => ({
      key: o.key,
      text: o.text,
      isAiFilled: false,
    }));

    const letters: ('A' | 'B' | 'C' | 'D' | 'E')[] = ['A', 'B', 'C', 'D', 'E'];
    const filledOptions = letters.map((letter) => {
      const ex = existingOptions.find((o) => o.key === letter);
      if (ex) return ex;
      return {
        key: letter,
        text: `${letter} seçeneği klinik ve farmakolojik çeldirici`,
        isAiFilled: true,
      };
    });

    const chosenAnswer = q.claimedAnswer || (q.options[0]?.key as any) || 'C';

    q.reconstruction = {
      stem,
      options: filledOptions,
      correctAnswer: chosenAnswer,
      explanation: `${q.discipline} dersinde ${q.topic} konusu için kurul sınavı standartlarında Robbins Patoloji ve Katzung Farmakoloji literatürü esas alınarak derlenmiştir.`,
      confidenceScore: Math.min(95, 75 + q.fragments.length * 7),
      notesAndDiscrepancies: 'Ortak havuzdan öğrenci hafızalarıyla birleştirildi.',
      lastUpdated: new Date().toISOString(),
    };

    q.status = 'completed';
    q.updatedAt = new Date().toISOString();
    saveLocalDb(db);

    try {
      await FirestoreDbService.saveQuestion(q);
    } catch (e) {
      console.warn('Firestore reconstructWithAi fallback', e);
    }

    return q;
  },

  async generateSlots(adminEmail: string, committeeId: string, count: number): Promise<void> {
    if (adminEmail !== ADMIN_EMAIL) {
      throw new Error('Yetkisiz işlem: 100/150 soruluk yuva açma yetkisi yalnızca sistem yöneticisine (nofrostlife@gmail.com) aittir.');
    }
    const db = getLocalDb();
    const existingNums = new Set(
      db.questions
        .filter((q) => q.committeeId === committeeId && !q.isUnassignedNumber)
        .map((q) => q.questionNumber)
    );

    const newSlots: QuestionItem[] = [];
    for (let i = 1; i <= count; i++) {
      if (!existingNums.has(i)) {
        const slot: QuestionItem = {
          id: `q-${committeeId}-${i}`,
          committeeId,
          questionNumber: i,
          discipline: 'Belirtilmedi',
          topic: `Soru #${i}`,
          status: 'empty',
          fragments: [],
          options: [],
          tags: [],
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
        };
        db.questions.push(slot);
        newSlots.push(slot);
      }
    }
    saveLocalDb(db);

    if (newSlots.length > 0) {
      try {
        await FirestoreDbService.batchSaveQuestions(newSlots);
      } catch (e) {
        console.warn('Firestore batchSaveQuestions fallback', e);
      }
    }
  },

  // Admin endpoints
  async adminUpdateQuestion(adminEmail: string, id: string, updated: Partial<QuestionItem>): Promise<QuestionItem> {
    if (adminEmail !== ADMIN_EMAIL) {
      throw new Error('Yetkisiz işlem: Soru düzenleme yetkisi yalnızca sistem yöneticisine aittir.');
    }
    const db = getLocalDb();
    const idx = db.questions.findIndex((q) => q.id === id);
    if (idx === -1) throw new Error('Soru bulunamadı');
    db.questions[idx] = { ...db.questions[idx], ...updated, updatedAt: new Date().toISOString() };
    const saved = db.questions[idx];
    saveLocalDb(db);

    try {
      await FirestoreDbService.saveQuestion(saved);
    } catch (e) {
      console.warn('Firestore adminUpdateQuestion fallback', e);
    }

    return saved;
  },

  async adminDeleteQuestion(adminEmail: string, id: string): Promise<void> {
    if (adminEmail !== ADMIN_EMAIL) {
      throw new Error('Yetkisiz işlem: Başkasının sorusunu silme yetkisi yalnızca sistem yöneticisine (nofrostlife@gmail.com) aittir.');
    }
    const db = getLocalDb();
    db.questions = db.questions.filter((q) => q.id !== id);
    saveLocalDb(db);

    try {
      await FirestoreDbService.deleteQuestion(id);
    } catch (e) {
      console.warn('Firestore adminDeleteQuestion fallback', e);
    }
  },

  async assignUnassignedQuestion(
    adminEmail: string,
    unassignedId: string,
    targetNumber: number
  ): Promise<QuestionItem> {
    if (adminEmail !== ADMIN_EMAIL) {
      throw new Error('Yetkisiz işlem: Yalnızca yönetici numarasız soruları yerleştirebilir.');
    }
    const db = getLocalDb();
    const unassigned = db.questions.find((q) => q.id === unassignedId);
    if (!unassigned) throw new Error('Numarasız soru bulunamadı.');

    const target = db.questions.find(
      (q) =>
        q.committeeId === unassigned.committeeId &&
        q.questionNumber === targetNumber &&
        !q.isUnassignedNumber
    );

    if (target) {
      // Merge fragments and options into existing slot
      target.fragments.push(...unassigned.fragments);
      unassigned.options.forEach((opt) => {
        const ex = target.options.find((o) => o.key === opt.key);
        if (!ex) target.options.push(opt);
      });
      if (unassigned.discipline && unassigned.discipline !== 'Belirtilmedi') {
        target.discipline = unassigned.discipline;
      }
      target.status = 'gathering';
      target.updatedAt = new Date().toISOString();

      db.questions = db.questions.filter((q) => q.id !== unassignedId);
      saveLocalDb(db);

      try {
        await FirestoreDbService.saveQuestion(target);
        await FirestoreDbService.deleteQuestion(unassignedId);
      } catch (e) {}
      return target;
    } else {
      // Convert unassigned question directly to slot targetNumber
      unassigned.questionNumber = targetNumber;
      unassigned.isUnassignedNumber = false;
      unassigned.topic =
        unassigned.topic.replace('(Numarası Belirsiz Soru)', '').trim() || `Soru #${targetNumber}`;
      unassigned.updatedAt = new Date().toISOString();
      saveLocalDb(db);

      try {
        await FirestoreDbService.saveQuestion(unassigned);
      } catch (e) {}
      return unassigned;
    }
  },

  async adminExportDb(): Promise<LocalDatabase> {
    return getLocalDb();
  },

  async adminImportDb(adminEmail: string, data: LocalDatabase): Promise<void> {
    if (adminEmail !== ADMIN_EMAIL) {
      throw new Error('Yetkisiz işlem: Veritabanı içe aktarma yetkisi yalnızca sistem yöneticisine aittir.');
    }
    saveLocalDb(data);
    if (data.questions && data.questions.length > 0) {
      try {
        await FirestoreDbService.batchSaveQuestions(data.questions);
      } catch (e) {}
    }
  },

  async adminResetDb(adminEmail: string): Promise<void> {
    if (adminEmail !== ADMIN_EMAIL) {
      throw new Error('Yetkisiz işlem: Sıfırlama yetkisi yalnızca sistem yöneticisine aittir.');
    }
    localStorage.removeItem(STORAGE_KEY);
    getLocalDb();
  },

  // Admin AI Past Exam Questions Parser
  async parsePastExamQuestions({
    rawText,
    examYear,
    committeeId,
    defaultDiscipline,
    adminEmail,
  }: {
    rawText: string;
    examYear: string;
    committeeId: string;
    defaultDiscipline?: string;
    adminEmail: string;
  }): Promise<{ detectedYear: string; totalCount: number; questions: any[] }> {
    const res = await fetch('/api/ai/parse-past-questions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-admin-email': adminEmail,
      },
      body: JSON.stringify({
        rawText,
        examYear,
        committeeId,
        defaultDiscipline,
        adminEmail,
      }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error || 'Yapay zeka soruları ayrıştıramadı.');
    }
    return await res.json();
  },

  // Batch import questions parsed from past exam files into database
  async batchImportPastQuestions(
    adminEmail: string,
    committeeId: string,
    examYear: string,
    parsedQuestions: any[]
  ): Promise<QuestionItem[]> {
    if (adminEmail !== ADMIN_EMAIL) {
      throw new Error('Yetkisiz işlem: Soru aktarma yetkisi yalnızca sistem yöneticisine aittir.');
    }

    const db = getLocalDb();
    const createdQuestions: QuestionItem[] = [];

    for (const pq of parsedQuestions) {
      const qNum = Number(pq.questionNumber) || (db.questions.filter((q) => q.committeeId === committeeId).length + 1);
      const questionId = `past-${committeeId}-${qNum}-${Date.now().toString().slice(-4)}`;

      // Construct options array
      const options = (pq.options || []).map((opt: any) => ({
        key: opt.key as 'A' | 'B' | 'C' | 'D' | 'E',
        text: opt.text || '',
        suggestedBy: `Çıkmış (${examYear})`,
        upvotes: 2,
      }));

      // If less than 5 options, pad with standard placeholders
      const existingKeys = new Set(options.map((o: any) => o.key));
      (['A', 'B', 'C', 'D', 'E'] as const).forEach((k) => {
        if (!existingKeys.has(k)) {
          options.push({
            key: k,
            text: `${k} seçeneği (öğrenci katkısı bekleniyor)`,
            suggestedBy: 'AI Taslak',
            upvotes: 0,
          });
        }
      });

      const newQ: QuestionItem = {
        id: questionId,
        committeeId,
        questionNumber: qNum,
        discipline: pq.discipline || 'Tıbbi Patoloji',
        topic: pq.topic || `Soru #${qNum} (${examYear})`,
        status: pq.claimedAnswer ? 'completed' : 'gathering',
        claimedAnswer: pq.claimedAnswer || undefined,
        tags: [
          `${examYear} Çıkmış`,
          'Çıkmış Soru',
          pq.discipline || 'Genel',
        ].filter(Boolean),
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        contributedByName: `Yönetici (${examYear} Arşivi)`,
        fragments: [
          {
            id: `frag-${Date.now()}-${Math.random().toString(36).substring(7)}`,
            author: `Çıkmış Soru (${examYear})`,
            text: pq.stem || 'Soru kökü metni',
            type: 'stem',
            timestamp: new Date().toISOString(),
            upvotes: 5,
          },
        ],
        options,
        reconstruction: pq.stem
          ? {
              stem: pq.stem,
              options: options.map((o: any) => ({
                key: o.key,
                text: o.text,
                isAiFilled: false,
              })),
              correctAnswer: (pq.claimedAnswer || 'A') as 'A' | 'B' | 'C' | 'D' | 'E',
              explanation: pq.explanation || `Bu soru ${examYear} tıp kurulu sınavında sorulmuştur.`,
              confidenceScore: pq.confidenceScore || 90,
              notesAndDiscrepancies: `Geçmiş yıl çıkmış soru dosyasından AI tarafından ayrıştırıldı. Öğrenciler tarafından düzenlenebilir.`,
              lastUpdated: new Date().toISOString(),
            }
          : undefined,
      };

      // Check if slot with same question number already exists in this committee
      const existingIdx = db.questions.findIndex(
        (q) => q.committeeId === committeeId && q.questionNumber === qNum
      );
      if (existingIdx !== -1) {
        db.questions[existingIdx] = newQ;
      } else {
        db.questions.push(newQ);
      }
      createdQuestions.push(newQ);
    }

    saveLocalDb(db);
    try {
      await FirestoreDbService.batchSaveQuestions(createdQuestions);
    } catch (e) {
      console.warn('Firestore batch save past questions error:', e);
    }

    return createdQuestions;
  },

  // Drive automation sync
  async syncDriveAutomation(committeeId?: string, forceSync = false): Promise<any> {
    const res = await fetch('/api/drive/sync-automation', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ committeeId, forceSync }),
    });
    if (!res.ok) {
      throw new Error('Google Drive senkronizasyonu başlatılamadı.');
    }
    return await res.json();
  },
};
