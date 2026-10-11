/**
 * MeDSor Tıbbi Hastalıklar Bilgi Tabanı (Disease Knowledge Base Profile)
 * Automated Knowledge Base Construction (AKBC) Şeması
 */

export interface DiseaseProfile {
  id: string; // Benzersiz tanımlayıcı (slug veya id: örn. 'akut-apendisit')
  name: string; // Hastalığın Türkçe standart tıbbi adı
  latinName?: string; // Tıbbi Latince/İngilizce adı
  icd_code?: string; // ICD-10 Kodu (örn. 'K35', 'E05.0')
  category: string; // Gastroenteroloji, Endokrinoloji, Kardiyoloji, Hematoloji vb.
  etiology: string[]; // Etiyoloji, patogenez ve risk faktörleri
  morphology_pathology: string[]; // Makroskopik/mikroskopik patoloji, histopatoloji ve histoloji
  symptoms_clinical: string[]; // Semptomlar, klinik prezentasyon, fizik muayene bulguları
  pathognomonic_features: string[]; // Ayırıcı tanıdaki patognomonik ve karakteristik bulgular
  diagnostic_methods: string[]; // Tanı yöntemleri (laboratuvar, biyobelirteçler, biyopsi)
  imaging_findings: string[]; // Görüntüleme teknikleri (BT, MR, USG, Direkt Grafi bulguları)
  treatment: string[]; // Tedavi protokolü, ilk tercih ilaçlar, cerrahi, acil yaklaşım
  physiology_pathophysiology?: string[]; // Fizyolojisi ve patofizyolojik mekanizma
  epidemiology?: string; // Görülme sıklığı, yaş/cinsiyet dağılımı
  source_notes_summary?: string; // Ders notlarındaki amfi hocalarının vurguladığı sınav püf noktaları
  relatedLectures?: string[]; // İlgili komite ve ders notları (örn. ['Dönem 3 Kurul 2 Patoloji', 'Genel Cerrahi'])
  verifiedSources?: Array<{
    source: 'PubMed' | 'NCBI' | 'Wikipedia' | 'Guyton/Robbins' | 'Amfi Notu' | 'Kullanıcı Katkısı';
    verified: boolean;
    referenceUrl?: string;
    verifiedAt?: string;
  }>;
  isCustom?: boolean; // Kullanıcı / admin tarafından manuel eklenmiş veya düzenlenmiş
  createdBy?: string;
  createdAt: string;
  updatedAt: string;
}

export type DiseaseSectionKey =
  | 'overview'
  | 'symptoms'
  | 'pathognomonic'
  | 'etiology'
  | 'pathology'
  | 'physiology'
  | 'diagnosis'
  | 'imaging'
  | 'treatment'
  | 'notes';
