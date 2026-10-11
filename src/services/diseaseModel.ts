/**
 * Hastalıklar bilgi tabanı — ortak model yardımcıları (tarayıcı + sunucu; Node/DOM bağımlılığı yok).
 *
 * - Bölüm sırası ve türe göre bölüm başlıkları (molekülde "İşlev ve etki mekanizması", ilaçta "Etki mekanizması"…)
 * - Eski düz metin kayıtların (şema 1) şema 2'ye çevrilmesi
 * - Düz metin görünümü (arama dizini, bilgi grafiği, kopyalama) ve varlık dizini ("ateş" → hangi hastalıklarda, hangi bölümde)
 */
import type {
  DiseaseEntity, DiseaseEntityType, DiseaseFact, DiseaseKind, DiseaseProfile, DiseaseSectionId, LegacyDiseaseProfile,
} from '../types/disease';

export const SECTION_ORDER: DiseaseSectionId[] = [
  'definition', 'etiology', 'physiology', 'pathology', 'symptoms', 'pathognomonic', 'diagnosis', 'imaging',
  'treatment', 'complications', 'epidemiology', 'lecture',
];

export const KIND_LABEL: Record<DiseaseKind, string> = {
  hastalik: 'Hastalık',
  bulgu: 'Bulgu',
  patolojik_surec: 'Patolojik süreç',
  mekanizma: 'Mekanizma',
  molekul_hucre: 'Molekül / hücre',
  ilac: 'İlaç',
  kavram: 'Kavram',
  yontem: 'Yöntem',
};

export const DISEASE_CATEGORIES = [
  'Genel Patoloji', 'İmmünoloji ve Romatoloji', 'Tıbbi Genetik ve Dismorfoloji', 'Nefroloji ve Üroloji', 'Kardiyoloji ve Damar',
  'Göğüs Hastalıkları', 'Gastroenteroloji ve Hepatoloji', 'Endokrinoloji ve Metabolizma', 'Hematoloji',
  'Enfeksiyon Hastalıkları ve Mikrobiyoloji', 'Nöroloji ve Nöroşirürji', 'Psikiyatri', 'Kadın Hastalıkları ve Doğum',
  'Çocuk Sağlığı ve Beslenme', 'Kas-İskelet Sistemi', 'Dermatoloji', 'Farmakoloji ve Toksikoloji', 'Halk Sağlığı ve Epidemiyoloji',
] as const;

export const ENTITY_TYPE_LABEL: Record<DiseaseEntityType, string> = {
  belirti: 'Belirti', bulgu: 'Muayene bulgusu', laboratuvar: 'Laboratuvar', goruntuleme: 'Görüntüleme bulgusu',
  histopatoloji: 'Histopatoloji', patojen: 'Patojen', gen_protein: 'Gen / protein', ilac: 'İlaç', tedavi: 'Tedavi',
  test: 'Test / yöntem', hastalik: 'Hastalık', anatomi: 'Anatomi', risk_faktoru: 'Risk faktörü', hucre: 'Hücre',
  mekanizma: 'Mekanizma',
};

type Titles = Partial<Record<DiseaseSectionId, string>>;
const BASE: Record<DiseaseSectionId, string> = {
  definition: 'Tanım', etiology: 'Etiyoloji ve risk faktörleri', physiology: 'Patogenez ve fizyopatoloji',
  pathology: 'Morfoloji ve patoloji', symptoms: 'Klinik belirti ve bulgular', pathognomonic: 'Ayırıcı tanı ve sınav spotları',
  diagnosis: 'Tanı: laboratuvar ve biyopsi', imaging: 'Görüntüleme', treatment: 'Tedavi',
  complications: 'Komplikasyon ve prognoz', epidemiology: 'Epidemiyoloji', lecture: 'Ders notu vurguları',
};
/** Türe göre başlık; listede olmayan bölüm o türde gösterilmez (null) */
const KIND_TITLES: Record<DiseaseKind, Titles | null> = {
  hastalik: null,
  bulgu: {
    definition: 'Tanım', etiology: 'Nedenler ve ilişkili sendromlar', physiology: 'Oluşum mekanizması', pathology: 'Görünüm ve morfoloji',
    symptoms: 'Klinik önemi', pathognomonic: 'Ayırt edici noktalar', diagnosis: 'Değerlendirme', imaging: 'Görüntüleme',
    treatment: 'Yaklaşım', complications: 'Eşlik eden sorunlar', epidemiology: 'Sıklık', lecture: BASE.lecture,
  },
  patolojik_surec: {
    definition: 'Tanım', etiology: 'Nedenler ve tetikleyiciler', physiology: 'Mekanizma', pathology: 'Makroskopi ve mikroskopi',
    symptoms: 'Görüldüğü durumlar ve klinik önemi', pathognomonic: 'Ayırt edici noktalar', diagnosis: 'Tanı ve özel boyalar',
    imaging: 'Görüntüleme', treatment: 'Klinik yaklaşım', complications: 'Sonuç ve seyir', epidemiology: 'Sıklık', lecture: BASE.lecture,
  },
  mekanizma: {
    definition: 'Tanım', etiology: 'Tetikleyiciler', physiology: 'Adım adım mekanizma', pathology: 'Morfolojik karşılığı',
    symptoms: 'Hastalık örnekleri', pathognomonic: 'Sınav spotları ve karşılaştırma', diagnosis: 'Saptama yöntemleri',
    treatment: 'Tedaviyle ilişkisi', complications: 'Bozulduğunda sonuçlar', lecture: BASE.lecture,
  },
  molekul_hucre: {
    definition: 'Tanım', etiology: 'Kaynak ve yapı', physiology: 'İşlev ve etki mekanizması', pathology: 'Doku ve morfolojideki karşılığı',
    symptoms: 'İlişkili hastalıklar ve klinik önem', pathognomonic: 'Sınav spotları', diagnosis: 'Saptama ve laboratuvar kullanımı',
    treatment: 'Tedavi hedefi olarak', complications: 'Fazlalık / eksiklik sonuçları', lecture: BASE.lecture,
  },
  ilac: {
    definition: 'Tanım ve sınıf', etiology: 'Sınıf ve üyeler', physiology: 'Etki mekanizması', pathology: 'Farmakokinetik',
    symptoms: 'Endikasyonlar', pathognomonic: 'Sınav spotları', diagnosis: 'İzlem', treatment: 'Kullanım ilkeleri',
    complications: 'Yan etki, kontrendikasyon ve etkileşimler', lecture: BASE.lecture,
  },
  kavram: {
    definition: 'Tanım', etiology: 'Kapsam ve ilkeler', physiology: 'Nasıl işler', symptoms: 'Uygulama ve örnekler',
    pathognomonic: 'Sınav spotları ve karşılaştırma', diagnosis: 'Ölçüt ve hesaplama', treatment: 'Uygulama önlemleri',
    complications: 'Sınırlılıklar', lecture: BASE.lecture,
  },
  yontem: {
    definition: 'Tanım', etiology: 'İlke', physiology: 'Uygulama adımları', symptoms: 'Kullanım alanları',
    pathognomonic: 'Sınav spotları', diagnosis: 'Yorumlama', complications: 'Sınırlılıklar', lecture: BASE.lecture,
  },
};

export function sectionTitle(kind: DiseaseKind | undefined, sec: DiseaseSectionId): string | null {
  const t = KIND_TITLES[kind || 'hastalik'];
  if (!t) return BASE[sec];
  return t[sec] ?? null;
}

/** ==vurgu== işaretlerini ve fazla boşlukları atar */
export function plainText(s: string): string {
  return String(s || '').replace(/==([^=]+)==/g, '$1').replace(/\s+/g, ' ').trim();
}

/** Madde → tek satır düz metin ("Etken: …") */
export function factPlain(f: DiseaseFact): string {
  const t = [plainText(f.text), ...(f.items || []).map(plainText)].filter(Boolean).join(f.items?.length ? '; ' : '');
  return f.label ? `${f.label}: ${t}` : t;
}

export function sectionFacts(d: DiseaseProfile, sec: DiseaseSectionId): DiseaseFact[] {
  return (d.sections?.[sec] || []).filter((f) => f && String(f.text || '').trim());
}

export function sectionTexts(d: DiseaseProfile, sec: DiseaseSectionId): string[] {
  return sectionFacts(d, sec).map(factPlain);
}

const FIELD_OF: Array<[keyof LegacyDiseaseProfile, DiseaseSectionId]> = [
  ['etiology', 'etiology'], ['physiology_pathophysiology', 'physiology'], ['morphology_pathology', 'pathology'],
  ['symptoms_clinical', 'symptoms'], ['pathognomonic_features', 'pathognomonic'], ['diagnostic_methods', 'diagnosis'],
  ['imaging_findings', 'imaging'], ['treatment', 'treatment'], ['epidemiology', 'epidemiology'], ['source_notes_summary', 'lecture'],
];

/** "Etken: açıklama" satırını madde nesnesine çevirir (etiket ≤40 karakter ve ≤5 sözcükse) */
export function lineToFact(line: string): DiseaseFact {
  const s = String(line || '').trim();
  const m = s.match(/^([^:]{2,40}):\s+(.{3,})$/);
  if (m && m[1].trim().split(/\s+/).length <= 5) return { label: m[1].trim(), text: m[2].trim() };
  return { text: s };
}

/** Şema 1'in tüm kayıtlarda aynı olan şablon/dolgu cümleleri: gösterilmez */
const LEGACY_FILLER = /standart medikal protokol|laboratuvar incelemeleri ve klinik|radyolojik görüntüleme ve|tablosuna özgü akut veya kronik|altta yatan tetikleyici genetik|karakteristik histopatolojik doku|hücresel düzeyde fizyopatolojik|toplumda yaş ve cinsiyet|spesifik ayırıcı tanı belirteçleri|klinik ve histopatolojik ayırıcı tanı$/i;

export function isV2(raw: any): raw is DiseaseProfile {
  return Boolean(raw && raw.schemaVersion === 2 && raw.sections && typeof raw.sections === 'object');
}

/** Her biçimden (şema 1 yerel katkı ya da şema 2) güvenli DiseaseProfile üretir */
export function normalizeDisease(raw: any): DiseaseProfile {
  const now = new Date(0).toISOString();
  if (isV2(raw)) {
    return {
      ...raw,
      kind: raw.kind || 'hastalik',
      category: raw.category || 'Genel Patoloji',
      hallmarks: Array.isArray(raw.hallmarks) ? raw.hallmarks : [],
      sections: raw.sections || {},
      createdAt: raw.createdAt || now,
      updatedAt: raw.updatedAt || raw.createdAt || now,
    };
  }
  const old = (raw || {}) as LegacyDiseaseProfile;
  const sections: Partial<Record<DiseaseSectionId, DiseaseFact[]>> = {};
  for (const [field, sec] of FIELD_OF) {
    const v = old[field] as unknown;
    const lines = (Array.isArray(v) ? v : v ? [v] : []).map((x) => String(x || '').trim()).filter((x) => x && !LEGACY_FILLER.test(x));
    if (lines.length) sections[sec] = lines.map(lineToFact);
  }
  return {
    id: String(old.id || ''),
    name: String(old.name || ''),
    latinName: old.latinName || undefined,
    icd_code: old.icd_code || null,
    kind: 'hastalik',
    category: old.category || 'Genel Patoloji',
    hallmarks: [],
    sections,
    relatedLectures: old.relatedLectures,
    schemaVersion: 2,
    isCustom: old.isCustom,
    createdBy: old.createdBy,
    createdAt: old.createdAt || now,
    updatedAt: old.updatedAt || old.createdAt || now,
  };
}

/** Profilin tüm maddeleri (karakteristik özellikler dahil), bölüm bilgisiyle */
export function allFacts(d: DiseaseProfile): Array<{ sec: DiseaseSectionId | 'hallmarks'; fact: DiseaseFact }> {
  const out: Array<{ sec: DiseaseSectionId | 'hallmarks'; fact: DiseaseFact }> = [];
  for (const f of d.hallmarks || []) out.push({ sec: 'hallmarks', fact: f });
  for (const sec of SECTION_ORDER) for (const f of sectionFacts(d, sec)) out.push({ sec, fact: f });
  return out;
}

/** Varlık anahtarı: tür + Türkçe küçük harf ad */
export function entityKey(e: Pick<DiseaseEntity, 'name' | 'type'>): string {
  return `${e.type}:${String(e.name || '').trim().toLocaleLowerCase('tr-TR')}`;
}

export interface EntityOccurrence {
  diseaseId: string;
  section: DiseaseSectionId | 'hallmarks';
  qualifier?: string;
}

/** Varlık → geçtiği profiller ("belirti:ateş" → [{diseaseId, section:'symptoms'}…]) */
export function buildEntityIndex(list: DiseaseProfile[]): Map<string, { entity: DiseaseEntity; hits: EntityOccurrence[] }> {
  const idx = new Map<string, { entity: DiseaseEntity; hits: EntityOccurrence[] }>();
  for (const d of list) {
    for (const { sec, fact } of allFacts(d)) {
      for (const e of fact.entities || []) {
        if (!e?.name || !e.type) continue;
        const k = entityKey(e);
        let row = idx.get(k);
        if (!row) idx.set(k, (row = { entity: { name: e.name, type: e.type }, hits: [] }));
        if (!row.hits.some((h) => h.diseaseId === d.id && h.section === sec)) {
          row.hits.push({ diseaseId: d.id, section: sec, ...(e.qualifier ? { qualifier: e.qualifier } : {}) });
        }
      }
    }
  }
  return idx;
}

/** Tek satırlık arama metni (ad, takma adlar, karakteristik özellik ve tüm maddeler) */
export function diseaseSearchText(d: DiseaseProfile): string {
  return [d.name, d.latinName || '', d.icd_code || '', ...(d.altNames || []), ...allFacts(d).map(({ fact }) => factPlain(fact))].join(' ');
}

/**
 * Eski düz alan görünümü (bilgi grafiği denetimi ve kanıt eşleyicisi şema 1 alan adlarıyla çalışır).
 * Yalnız okuma içindir; diseases.json'a yazılmaz.
 */
export function toFlatView(raw: any): { name: string } & Record<string, any> {
  const d = normalizeDisease(raw);
  const t = (sec: DiseaseSectionId) => sectionTexts(d, sec);
  return {
    id: d.id, name: d.name, latinName: d.latinName, icd_code: d.icd_code, category: d.category, kind: d.kind,
    altNames: d.altNames || [], relatedLectures: d.relatedLectures || [],
    etiology: t('etiology'), physiology_pathophysiology: t('physiology'), morphology_pathology: t('pathology'),
    symptoms_clinical: t('symptoms'), pathognomonic_features: [...(d.hallmarks || []).map(factPlain), ...t('pathognomonic')],
    diagnostic_methods: t('diagnosis'), imaging_findings: t('imaging'), treatment: t('treatment'),
    epidemiology: t('epidemiology'), complications: t('complications'), definition: t('definition'),
    source_notes_summary: t('lecture').join(' '),
  };
}
