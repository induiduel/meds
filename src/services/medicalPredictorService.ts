/**
 * ==============================================================================
 * MedSoru Akıllı Tıbbi Tahminci & Hibrit Eşleme Motoru (medicalPredictorService.ts)
 * ==============================================================================
 * Kullanıcının soru ekleme alanında yazdığı metinden (kök, şıklar, ipuçları) yola çıkarak:
 * 1. En olası KURUL (Dönem 3 Kurul 1-6) ve DERS (Patoloji, Farmakoloji vb.) tahmin eder.
 * 2. 5,000+ Tıbbi Kavram Bankası, Müfredat Verisi ve Çıkmış Sorular indeksini kullanarak
 *    ilişkili konuları tespit eder.
 * 3. Kullanıcı yanlış kuruldayken yazıyorsa çapraz kurul uyarısı ve tek tıkla geçiş sağlar.
 * 4. Mevcut taslaklar, çıkmış sorular ve amfi ders slaytlarını birleşik bir asistan
 *    özeti olarak istemciye sunar.
 * ==============================================================================
 */

import { Committee, QuestionItem } from '../types';
import { OFFICIAL_CURRICULUM_COMMITTEES, CurriculumCommittee } from '../data/curriculumData';
import { detectMedicalConcepts, MedicalConceptBank } from './draftClusteringService';
import { foldTurkish, damerauLevenshtein, areWordsFuzzyEqual } from '../utils/fuzzyMatching';

export interface CommitteePrediction {
  committeeId: string;
  committeeName: string;
  confidence: number; // 0 - 100
  matchedDisciplines: string[];
  matchedKeywords: string[];
  reason: string;
}

export interface DisciplinePrediction {
  discipline: string;
  confidence: number; // 0 - 100
  sampleKeywords: string[];
}

export interface TopicSuggestion {
  topic: string;
  conceptName?: string;
  discipline?: string;
  confidence: number;
}

export interface SmartQuestionAssistantResult {
  detectedConcepts: MedicalConceptBank[];
  predictedCommittee?: CommitteePrediction;
  isDifferentFromSelectedCommittee: boolean;
  predictedDiscipline?: DisciplinePrediction;
  suggestedTopics: TopicSuggestion[];
  crossCommitteeWarning?: string;
}

// ==========================================
// TIBBİ SİSTEM & KURUL KELİME DAĞARCIĞI
// ==========================================
interface CommitteeKeywordRule {
  committeeId: string;
  primaryDisciplines: string[];
  keywords: string[];
  weight: number;
}

const COMMITTEE_RULES: CommitteeKeywordRule[] = [
  {
    committeeId: 'donem3-kurul1',
    primaryDisciplines: ['Tıbbi Patoloji', 'Enfeksiyon Hastalıkları', 'Üroloji', 'Tıbbi Genetik', 'Kadın Hastalıkları ve Doğum'],
    keywords: [
      'bobrek', 'glomerul', 'glomerulonefrit', 'nefrotik', 'nefritik', 'ureter', 'mesane',
      'prostat', 'testis', 'over', 'uterus', 'serviks', 'endometrium', 'gebelik', 'obstetrik',
      'preeklampsi', 'plasenta', 'uroloji', 'sistit', 'pyelonefrit', 'hidronefroz', 'karsinomu',
      'seminom', 'psa', 'kreatinin', 'gfr', 'proteinuri', 'hematuri', 'clearance', 'klirens'
    ],
    weight: 1.2
  },
  {
    committeeId: 'donem3-kurul2',
    primaryDisciplines: ['Tıbbi Farmakoloji', 'Psikiyatri', 'Nöroloji', 'Tıbbi Genetik', 'Beyin ve Sinir Cerrahisi'],
    keywords: [
      'beyin', 'korteks', 'serebellum', 'menenjit', 'ensefalit', 'epilepsi', 'nobet', 'parkinson',
      'alzheimer', 'dopamin', 'serotonin', 'gaba', 'noradrenalin', 'depresyon', 'sizofreni',
      'bipolar', 'psikoz', 'antipsikotik', 'antidepresan', 'ssri', 'snri', 'sedatif', 'hipnotik',
      'inme', 'stroke', 'iskemi', 'kanama', 'anevrizma', 'subaraknoid', 'kibas', 'hidrosefali',
      'multipl skleroz', 'ms', 'bos', 'lomber ponksiyon', 'miastenia gravis'
    ],
    weight: 1.2
  },
  {
    committeeId: 'donem3-kurul3',
    primaryDisciplines: ['Tıbbi Farmakoloji', 'İç Hastalıkları', 'Tıbbi Patoloji', 'Çocuk Sağlığı ve Hastalıkları', 'Enfeksiyon Hastalıkları'],
    keywords: [
      'mide', 'ozofagus', 'bagirsak', 'kolon', 'rektum', 'karaciger', 'hepatit', 'siroz',
      'safra', 'kolesistit', 'pankreas', 'pankreatit', 'peptik ulser', 'gastrit', 'h pylori',
      'helicobacter', 'crohn', 'ulseratif kolit', 'ibd', 'colitis', 'malabsorpsiyon', 'colyak',
      'sarilik', 'bilirubin', 'ast', 'alt', 'laksatif', 'antiasit', 'ppi', 'proton pompa',
      'ishal', 'kabizlik', 'kusma', 'gastroenterit', 'apandisit'
    ],
    weight: 1.2
  },
  {
    committeeId: 'donem3-kurul4',
    primaryDisciplines: ['Kardiyoloji', 'Tıbbi Patoloji', 'Tıbbi Farmakoloji', 'Göğüs Hastalıkları', 'Çocuk Sağlığı ve Hastalıkları'],
    keywords: [
      'kalp', 'akciger', 'pnömoni', 'pnomoni', 'astim', 'koah', 'bronsektazi', 'solunum yetmezligi',
      'koroner', 'miyokard', 'infarktus', 'infarktusu', 'ekg', 'st elevasyonu', 'troponin', 'iskemi',
      'anjina', 'angina', 'hipertansiyon', 'kapak', 'mitral', 'aort', 'stenoz', 'yetmezlik',
      'aritmi', 'fibrilasyon', 'ventrikul', 'atrium', 'kalp yetmezligi', 'dijital', 'digoksin',
      'beta blokor', 'ace inhibitoru', 'arb', 'statin', 'tbc', 'tuberkuloz', 'emboli', 'pulmoner'
    ],
    weight: 1.2
  },
  {
    committeeId: 'donem3-kurul5',
    primaryDisciplines: ['Acil Tıp', 'Tıbbi Patoloji', 'Ortopedi ve Travmatoloji', 'Halk Sağlığı', 'FTR', 'İç Hastalıkları'],
    keywords: [
      'kemik', 'eklem', 'fraktur', 'kirik', 'cikis', 'artrit', 'osteoartrit', 'romatoid',
      'osteoporoz', 'osteomiyelit', 'sarkom', 'osteosarkom', 'lovkemi', 'losemi', 'lenfoma',
      'hodgkin', 'non-hodgkin', 'anemi', 'demir eksikligi', 'megaloblastik', 'b12', 'folat',
      'trombosit', 'koagulasyon', 'pt', 'aptt', 'kanama', 'hemofili', 'hemostaz', 'polisitemi',
      'eritropoietin', 'dalak', 'splenomegali', 'kemik iligi', 'travma', 'resusitasyon', 'sok'
    ],
    weight: 1.2
  },
  {
    committeeId: 'donem3-kurul6',
    primaryDisciplines: ['İç Hastalıkları', 'Halk Sağlığı', 'Tıbbi Farmakoloji', 'Tıbbi Biyokimya', 'Tıbbi Genetik'],
    keywords: [
      'tiroid', 'guatr', 'hipotiroidi', 'hipertiroidi', 'graves', 'hashimoto', 'tsh', 't3', 't4',
      'diyabet', 'diabetes', 'mellitus', 'insulin', 'glukoz', 'hba1c', 'hipoglisemi', 'ketoasidoz',
      'surrenal', 'adrenal', 'cushing', 'addison', 'kortizol', 'acth', 'aldosteron', 'feokromasitoma',
      'hipofiz', 'prolaktin', 'akromegali', 'paratiroid', 'pth', 'kalsiyum', 'hiperkalsemi',
      'lipit', 'kolesterol', 'trigliserit', 'dislipidemi', 'metabolik sendrom', 'obezite', 'yaslanma'
    ],
    weight: 1.2
  }
];

const DISCIPLINE_RULES: { discipline: string; keywords: string[]; weight: number }[] = [
  {
    discipline: 'Tıbbi Genetik',
    keywords: [
      'down sendromu', 'down sendrom', 'trizomi 21', 'trizomi 18', 'trizomi 13', 'edwards', 'patau',
      'turner', 'klinefelter', 'karyotip', 'translokasyon', 'robertsonian', 'delesyon', 'duplikasyon',
      'mikrodelesyon', 'genetik', 'kalitim', 'otozomal', 'x e bagli', 'mitokondriyal', 'mendel',
      'fragil x', 'prader willi', 'angelman', 'imprinting', 'dismorfoloji', 'genom', 'kromozom'
    ],
    weight: 2.0
  },
  {
    discipline: 'Tıbbi Patoloji',
    keywords: [
      'patoloji', 'biyopsi', 'histopatoloji', 'nekroz', 'apoptoz', 'karsinom', 'adenokarsinom',
      'sarkom', 'displazi', 'metaplazi', 'anaplazisi', 'granulom', 'enflamasyon', 'malign', 'benign'
    ],
    weight: 1.5
  },
  {
    discipline: 'Tıbbi Farmakoloji',
    keywords: [
      'farmakoloji', 'ilac', 'reseptor', 'agonist', 'antagonist', 'toksisite', 'yan etki',
      'kontrendikasyon', 'yari omur', 'klerens', 'biyoyararlanim', 'etki mekanizmasi', 'antidot'
    ],
    weight: 1.5
  },
  {
    discipline: 'Tıbbi Biyokimya',
    keywords: [
      'biyokimya', 'enzim', 'koenzim', 'glikoliz', 'krebs', 'lipid', 'kolesterol', 'protein',
      'aminoasit', 'ure', 'kreatinin', 'glukoz', 'metabolizma', 'elektroforez'
    ],
    weight: 1.5
  },
  {
    discipline: 'Halk Sağlığı',
    keywords: [
      'halk sagligi', 'epidemiyoloji', 'insidans', 'prevalans', 'surveyans', 'mortalite',
      'morbidite', 'bagisiklama', 'asi', 'taramasi', 'saglik yonetimi'
    ],
    weight: 1.5
  }
];

// ==========================================
// YAZILAN METİNDEN KURUL & DERS TAHMİNİ
// ==========================================
export function predictCommitteeAndDiscipline(
  text: string,
  currentCommitteeId?: string
): {
  predictedCommittee?: CommitteePrediction;
  isDifferentFromSelectedCommittee: boolean;
  predictedDiscipline?: DisciplinePrediction;
  crossCommitteeWarning?: string;
} {
  const norm = foldTurkish(text).trim();
  if (norm.length < 8) {
    return { isDifferentFromSelectedCommittee: false };
  }

  const words = norm
    .replace(/[^a-z0-9\s]/gi, ' ')
    .split(/\s+/)
    .filter((w) => w.length >= 3);

  if (words.length === 0 || (words.length < 2 && words[0].length < 5)) {
    return { isDifferentFromSelectedCommittee: false };
  }

  // 1. Kurul Skorlama (Committee Scoring)
  const committeeScores: Record<string, { score: number; matchedWords: string[]; matchedDisciplines: string[] }> = {};
  for (const c of OFFICIAL_CURRICULUM_COMMITTEES) {
    committeeScores[c.id] = { score: 0, matchedWords: [], matchedDisciplines: [] };
  }

  for (const rule of COMMITTEE_RULES) {
    const entry = committeeScores[rule.committeeId];
    if (!entry) continue;

    for (const kw of rule.keywords) {
      const foldedKw = foldTurkish(kw);
      if (norm.includes(foldedKw)) {
        entry.score += 8 * rule.weight;
        if (!entry.matchedWords.includes(kw)) entry.matchedWords.push(kw);
      } else {
        // Kelime kelime bulanık kontrol
        for (const w of words) {
          if (w.length >= 4 && Math.abs(w.length - foldedKw.length) <= 2 && areWordsFuzzyEqual(w, foldedKw)) {
            entry.score += 5 * rule.weight;
            if (!entry.matchedWords.includes(kw)) entry.matchedWords.push(kw);
            break;
          }
        }
      }
    }
  }

  // 2. Doğrudan Anabilim Dalı Kuralları ile Ders Puanlama
  const disciplineFreq: Record<string, number> = {};
  for (const rule of DISCIPLINE_RULES) {
    for (const kw of rule.keywords) {
      const foldedKw = foldTurkish(kw);
      if (norm.includes(foldedKw)) {
        disciplineFreq[rule.discipline] = (disciplineFreq[rule.discipline] || 0) + 25 * rule.weight;
      }
    }
  }

  // 3. Tıbbi Kavram Bankası ile Kurul/Ders Zenginleştirme
  const detectedConcepts = detectMedicalConcepts(text);

  for (const concept of detectedConcepts.slice(0, 5)) {
    if (concept.disciplines && concept.disciplines.length > 0) {
      for (const disc of concept.disciplines) {
        disciplineFreq[disc] = (disciplineFreq[disc] || 0) + 12;

        // Bu ders hangi kurulda daha baskın?
        for (const comm of OFFICIAL_CURRICULUM_COMMITTEES) {
          const discInfo = comm.disciplines.find(
            (d) => d.name.toLowerCase() === disc.toLowerCase() || disc.toLowerCase().includes(d.name.toLowerCase())
          );
          if (discInfo && committeeScores[comm.id]) {
            committeeScores[comm.id].score += (discInfo.hours || 10) * 0.4;
            if (!committeeScores[comm.id].matchedDisciplines.includes(discInfo.name)) {
              committeeScores[comm.id].matchedDisciplines.push(discInfo.name);
            }
          }
        }
      }
    }
  }

  // En yüksek puanlı kurulu seç
  let bestCommId = '';
  let bestCommScore = 0;
  for (const [cId, item] of Object.entries(committeeScores)) {
    if (item.score > bestCommScore) {
      bestCommScore = item.score;
      bestCommId = cId;
    }
  }

  let predictedComm: CommitteePrediction | undefined;
  if (bestCommId && bestCommScore >= 16) {
    const commObj = OFFICIAL_CURRICULUM_COMMITTEES.find((c) => c.id === bestCommId);
    const entry = committeeScores[bestCommId];
    const confidence = Math.min(98, Math.round(30 + bestCommScore * 1.5));

    predictedComm = {
      committeeId: bestCommId,
      committeeName: commObj?.name || bestCommId,
      confidence,
      matchedDisciplines: entry.matchedDisciplines,
      matchedKeywords: entry.matchedWords.slice(0, 5),
      reason: entry.matchedWords.length > 0
        ? `İçerikte geçen "${entry.matchedWords.slice(0, 3).join(', ')}" anahtar terimleri ${commObj?.name} müfredatı ile örtüşüyor.`
        : `${commObj?.name} ders içeriğiyle uyumlu.`
    };
  }

  // En yüksek puanlı dersi seç
  let bestDiscipline = '';
  let bestDiscScore = 0;
  for (const [disc, score] of Object.entries(disciplineFreq)) {
    if (score > bestDiscScore) {
      bestDiscScore = score;
      bestDiscipline = disc;
    }
  }

  let predictedDiscipline: DisciplinePrediction | undefined;
  if (bestDiscipline && bestDiscScore >= 10) {
    predictedDiscipline = {
      discipline: bestDiscipline,
      confidence: Math.min(95, Math.round(40 + bestDiscScore * 1.2)),
      sampleKeywords: detectedConcepts.slice(0, 3).map((c) => c.name)
    };
  }

  const isDifferent = Boolean(
    predictedComm &&
    currentCommitteeId &&
    predictedComm.committeeId !== currentCommitteeId &&
    predictedComm.confidence >= 60
  );

  let crossCommitteeWarning: string | undefined;
  if (isDifferent && predictedComm) {
    const currentName = OFFICIAL_CURRICULUM_COMMITTEES.find((c) => c.id === currentCommitteeId)?.name || 'Mevcut Kurul';
    crossCommitteeWarning = `Bu soru ${predictedComm.committeeName} (${predictedComm.matchedDisciplines.join(', ') || 'İlgili Dersler'}) ile %${predictedComm.confidence} uyumlu görünüyor. Şu an ${currentName} seçili.`;
  }

  return {
    predictedCommittee: predictedComm,
    isDifferentFromSelectedCommittee: isDifferent,
    predictedDiscipline,
    crossCommitteeWarning
  };
}

// ==========================================
// TIBBİ KONU & BAŞLIK ÖNERİCİSİ
// ==========================================
export function suggestTopicsForInput(
  text: string,
  discipline?: string
): TopicSuggestion[] {
  const concepts = detectMedicalConcepts(text, discipline);
  if (!concepts || concepts.length === 0) return [];

  const suggestions: TopicSuggestion[] = [];
  const seen = new Set<string>();

  for (const concept of concepts.slice(0, 4)) {
    if (seen.has(concept.name.toLowerCase())) continue;
    seen.add(concept.name.toLowerCase());

    suggestions.push({
      topic: concept.name,
      conceptName: concept.name,
      discipline: concept.disciplines?.[0] || discipline,
      confidence: 85
    });
  }

  return suggestions;
}

// ==========================================
// BİRLEŞİK ASİSTAN HİZMETİ (COMPREHENSIVE)
// ==========================================
export function getSmartQuestionAssistant(
  text: string,
  options?: Array<{ key: string; text: string }>,
  currentCommitteeId?: string
): SmartQuestionAssistantResult {
  const fullText = [
    text || '',
    ...(options || []).map((o) => o.text || '')
  ].join(' ').trim();

  const detectedConcepts = detectMedicalConcepts(fullText);
  const { predictedCommittee, isDifferentFromSelectedCommittee, predictedDiscipline, crossCommitteeWarning } =
    predictCommitteeAndDiscipline(fullText, currentCommitteeId);

  const suggestedTopics = suggestTopicsForInput(fullText, predictedDiscipline?.discipline);

  return {
    detectedConcepts,
    predictedCommittee,
    isDifferentFromSelectedCommittee,
    predictedDiscipline,
    suggestedTopics,
    crossCommitteeWarning
  };
}
