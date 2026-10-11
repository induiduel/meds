/**
 * MeDSor Hastalıklar bilgi tabanı — veri modeli (şema 2).
 *
 * Her bilgi düz metin değil, sorgulanabilir bir "madde" (DiseaseFact) nesnesidir: metin + alt başlık + sınav önemi +
 * içindeki tıbbi varlıklar (ateş → belirti, metronidazol → ilaç, VHL → gen). Böylece "ateş yapan hastalıklar",
 * "metronidazolle tedavi edilenler" gibi sınıflandırmalar doğrudan veriden çıkarılır (bkz. services/diseaseModel.ts).
 * Kaynak: src/data/diseases.json. Eski düz alanlı kayıtlar (yerel katkılar) normalizeDisease ile bu şemaya çevrilir.
 */

/** Kaydın türü: bölüm başlıkları türe göre değişir (molekülde "Tedavi" yerine "Tedavi hedefi olarak" gibi). */
export type DiseaseKind =
  | 'hastalik'
  | 'bulgu'
  | 'patolojik_surec'
  | 'mekanizma'
  | 'molekul_hucre'
  | 'ilac'
  | 'kavram'
  | 'yontem';

/** Varlık türleri (meds_database/derived/entities soru varlıklarıyla uyumlu ad alanı) */
export type DiseaseEntityType =
  | 'belirti'
  | 'bulgu'
  | 'laboratuvar'
  | 'goruntuleme'
  | 'histopatoloji'
  | 'patojen'
  | 'gen_protein'
  | 'ilac'
  | 'tedavi'
  | 'test'
  | 'hastalik'
  | 'anatomi'
  | 'risk_faktoru'
  | 'hucre'
  | 'mekanizma';

export interface DiseaseEntity {
  /** Kanonik ad: Türkçe, küçük harf, yalın ("ateş", "proteinüri"); tür adı/gen simgesi özgün yazımla */
  name: string;
  type: DiseaseEntityType;
  /** Niteleyici: "yüksek, titremeli", "masif (>3,5 g/gün)" */
  qualifier?: string;
}

export interface DiseaseFact {
  /** Tek bilgi; ==terim== ile işaretlenen kısım arayüzde fosforlu kalemle vurgulanır */
  text: string;
  /** Kısa alt başlık ("Etken", "İlk seçenek", "Mikroskopi") */
  label?: string;
  /** Sınavda sorulan kritik bilgi */
  key?: boolean;
  entities?: DiseaseEntity[];
  /** Ders notundan alınan maddede kaynak dosya/ders adı */
  source?: string;
  /** Sıralama içeren maddede her öge ayrı satır (virgülle birleştirilmez); `text` o zaman kısa giriş cümlesidir */
  items?: string[];
  /** Maddeyi doğrulayan kaynakların `references` içindeki sıraları (web doğrulaması; en az biri URL'li) */
  refs?: number[];
}

/** Bağımsız madde madde web doğrulamasının özeti */
export interface DiseaseVerification {
  at: string;
  method: 'web';
  checked: number;
  ok: number;
  fixed: number;
  conflict: number;
  removed: number;
}

export type DiseaseSectionId =
  | 'definition'
  | 'etiology'
  | 'physiology'
  | 'pathology'
  | 'symptoms'
  | 'pathognomonic'
  | 'diagnosis'
  | 'imaging'
  | 'treatment'
  | 'complications'
  | 'epidemiology'
  | 'lecture';

export interface DiseaseReference {
  label: string;
  url?: string;
}

export interface DiseaseProfile {
  id: string;
  name: string;
  latinName?: string;
  icd_code?: string | null;
  kind: DiseaseKind;
  /** Uzmanlık / organ sistemi (sabit liste: diseaseModel.DISEASE_CATEGORIES) */
  category: string;
  /** Bu kayda birleştirilmiş eski kimlikler (derin bağlantı ve favoriler bunlarla da çözülür) */
  aliases?: string[];
  /** Arama için ek adlar (birleştirilen kayıtların adları) */
  altNames?: string[];
  /** Karakteristik özellik: "Çilek serviks", "Reed-Sternberg hücresi" */
  hallmarks: DiseaseFact[];
  sections: Partial<Record<DiseaseSectionId, DiseaseFact[]>>;
  references?: DiseaseReference[];
  verification?: DiseaseVerification;
  relatedLectures?: string[];
  schemaVersion: 2;
  /** İçeriğin nasıl üretildiği/denetlendiği */
  curation?: { method: string; at: string; by?: string };
  isCustom?: boolean;
  createdBy?: string;
  createdAt: string;
  updatedAt: string;
}

/** Şema 1 (düz metin alanları): yalnız eski yerel katkıları okumak için */
export interface LegacyDiseaseProfile {
  id: string;
  name: string;
  latinName?: string;
  icd_code?: string | null;
  category?: string;
  etiology?: string[];
  morphology_pathology?: string[];
  symptoms_clinical?: string[];
  pathognomonic_features?: string[];
  diagnostic_methods?: string[];
  imaging_findings?: string[];
  treatment?: string[];
  physiology_pathophysiology?: string[];
  epidemiology?: string | string[];
  source_notes_summary?: string | string[];
  relatedLectures?: string[];
  isCustom?: boolean;
  createdBy?: string;
  createdAt?: string;
  updatedAt?: string;
}
