/**
 * MeDSor Quiz ve Aktif Geri Çağırma (Active Recall) Motoru Veri Tipleri
 * 
 * Mimari Özellikleri:
 * 1. Ders-bağımsız (Course-agnostic): Tüm tıp branşlarına genişleyebilir.
 * 2. 2x Çapraz Sorgulama: Her atomik bilgi için en az iki soru (Pozitif/Doğrudan ve Negatif/Ters).
 * 3. Çoklu Mod Desteği: Bireysel (Solo Active Recall) ve Eş Zamanlı Rekabet (Multiplayer) modları.
 * 4. Katı Öncelik Bağımlılığı: audio_lesson_id üzerinden sesli ders tamamlanma durumuna bağlıdır.
 */

export type KnowledgeCategory =
  | 'drug'                    // İlaç etken maddesi
  | 'drug_class'              // İlaç sınıfı / farmakolojik grup
  | 'receptor'                // Reseptör
  | 'enzyme'                  // Enzim
  | 'protein'                 // Taşıyıcı / yapısal protein
  | 'gene'                    // Gen / genetik mutasyon
  | 'disease'                 // Hastalık / klinik sendrom
  | 'symptom'                 // Semptom / klinik bulgu
  | 'pharmacokinetics'        // Emilim, dağılım, metabolizma, atılım (ADME)
  | 'pharmacodynamics'        // Etki mekanizması, doz-yanıt
  | 'side_effect'             // Toksisite, advers etki, kontrendikasyon
  | 'clinical_note'           // Slayt içi özel not, hoca vurgusu, antidot, istisna
  | string;

export interface KnowledgeAtomEvidence {
  page: number;
  quote: string;
  reference?: string;
}

export interface PastExamRelevance {
  has_appeared: boolean;
  question_ids?: string[];
  details?: string;
  frequency?: number;
}

/**
 * Tekil Atomik Bilgi Birimi (Single Knowledge Atom)
 * Kaynak slaytlardan çıkarılan, parçalanamaz en küçük bilgi çekirdeği.
 */
export interface KnowledgeAtom {
  knowledge_atom_id: string;        // Örn: "ka_k2-07_001"
  course_id: string;                // Örn: "pharmacology" (ders-bağımsız kimlik)
  board_id: string;                 // Örn: "2026_2027_kurul_2"
  schedule_ref: string;             // Ders programı referansı
  topic_id: string;                 // Ders konusu kimliği (örn: "k2-07")
  audio_lesson_id: string;          // Bağlı olduğu sesli dersin kimliği (State bağımlılığı)
  learning_objective_id: string;    // İlgili öğrenim kazanımı referansı
  category: KnowledgeCategory;      // Bilgi kategorisi
  title: string;                    // Kısa terim / başlık (örn: "Atropin")
  statement: string;                // Net, doğrulanmış atomik bilgi cümlesi
  subtopic?: string;                // İlgili alt başlık
  page_number: number;              // Kaynaktaki slayt sayfa numarası
  evidence: KnowledgeAtomEvidence;  // Kaynak slayttan birebir alıntı kanıtı
  past_exam_relevance: PastExamRelevance; // Çıkmış sınav ilişkisi
  tags?: string[];
}

/**
 * Soru Arketipleri
 */
export type QuestionArchetype =
  | 'receptor_ligand'                    // Reseptör - Ligand (Agonist/Antagonist) Eşleştirmesi
  | 'drug_class_membership'              // İlaç Sınıfı Aidiyeti (Ait olan/olmayan)
  | 'disease_treatment'                  // Hastalık - Tedavi / Birinci Tercih İlaç Eşleştirmesi
  | 'pathophysiological_target'          // Patofizyolojik Hedef (Enzim / Reseptör / Protein / Gen)
  | 'toxicity_side_effect'               // Toksisite ve Karakteristik Yan Etki Profili
  | 'pharmacokinetics_pharmacodynamics'  // Temel Farmakokinetik (ADME) ve Farmakodinamik Mekanizma
  | 'slide_specific_pearl';              // Slayt İçi Özel Vurgu, İstisna ve Klinik Not

/**
 * Çapraz Sorgulama Yönü (2x Matrix)
 */
export type QuestionDirection =
  | 'positive_direct'   // Doğrudan / Pozitif: İsimden özelliğe / Pozitif aidiyet (Örn: X ilacının etki mekanizması nedir?)
  | 'negative_inverse'; // Ters / Negatif: Özellikten isme / Negatif ayıklama (Örn: Hangisi X sınıfı üyesi değildir?)

/**
 * Quiz Sorusu (Active Recall Odaklı)
 */
export interface QuizQuestion {
  id: string;                       // Tekil soru ID (örn: "qz_k2-07_001_p")
  question_pair_id: string;         // Çapraz eş ID (örn: "qp_k2-07_001")
  knowledge_atom_id: string;        // Kaynak atomik bilgi ID'si
  course_id: string;                // "pharmacology", "pathology" vb.
  board_id: string;                 // "2026_2027_kurul_2"
  schedule_ref: string;
  topic_id: string;
  audio_lesson_id: string;          // Sesli ders tamamlanma önşartı
  learning_objective_id: string;
  direction: QuestionDirection;     // Pozitif/Doğrudan veya Ters/Negatif
  archetype: QuestionArchetype;     // Soru şablonu
  prompt: string;                   // Kısa, net soru metni (paragraflardan arındırılmış)
  options: Record<string, string>;  // A, B, C, D (veya E) şıkları
  correct_option: string;           // "A" | "B" | "C" | "D" | "E"
  option_explanations: Record<string, string>; // Her şık için gerekçeli açıklama
  recall_hint?: string;             // Active recall için kısa ipucu (cevabı sızdırmaz)
  estimated_reading_sec: number;    // Okuma ve yanıtlama süresi (5-15 sn aralığında)
  difficulty: 'easy' | 'medium' | 'hard';
  evidence: KnowledgeAtomEvidence;  // Kaynak slayt kanıtı
}

/**
 * 2x Soru Çifti Eşleşmesi
 */
export interface QuestionPair {
  question_pair_id: string;
  knowledge_atom_id: string;
  positive_question_id: string;     // Pozitif / Doğrudan soru ID
  inverse_question_id: string;      // Ters / Negatif soru ID
}

/**
 * Yapılandırılmış Atomik Bilgi Envanteri (Faz 2 Çıktısı - Single Source of Truth)
 */
export interface AtomicKnowledgeInventory {
  course_id: string;
  board_id: string;
  topic_id: string;
  audio_lesson_id: string;
  generated_at: string;
  total_atoms: number;
  atoms: KnowledgeAtom[];
}

/**
 * Bir Dersin Tam Quiz Havuzu Paketi (Faz 4 Çıktısı)
 */
export interface TopicQuizPool {
  course_id: string;
  board_id: string;
  topic_id: string;
  audio_lesson_id: string;
  audio_lesson_status: 'COMPLETED'; // Sesli ders tamamlanma kilidi doğrulaması
  generated_at: string;
  total_atoms: number;              // N
  total_questions: number;          // En az 2N
  pairs: QuestionPair[];
  questions: QuizQuestion[];
}

/**
 * Bireysel Çalışma Modu (Solo / Active Recall) Oturumu
 */
export interface SoloQuizSession {
  session_id: string;
  user_id: string;
  course_id: string;
  topic_ids: string[];
  filter_categories?: KnowledgeCategory[];
  total_answered: number;
  correct_count: number;
  wrong_atom_ids: string[];         // Pekiştirme için yanlış bilinen atomlar
  incomplete_pair_ids: string[];    // Çiftlerden henüz sorulmamış olanlar
  started_at: string;
  last_activity_at: string;
}

/**
 * Eş Zamanlı Rekabet Modu (Real-Time Multiplayer Quiz) Oturumu
 */
export interface MultiplayerQuizSession {
  room_id: string;
  course_id: string;
  topic_id: string;
  question_ids: string[];           // Hızlı 5-15 sn'lik sorulardan seçilen havuz
  time_per_question_sec: number;    // Varsayılan: 10 saniye (5-15 sn aralığında)
  participants: {
    user_id: string;
    score: number;
    streak: number;
    answers: Record<string, { option: string; is_correct: boolean; response_time_ms: number }>;
  }[];
  status: 'waiting' | 'in_progress' | 'completed';
  created_at: string;
}
