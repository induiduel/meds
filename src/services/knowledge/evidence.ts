/**
 * Kanıt cümlesi çıkarımı (hastalık grafiği + anlık analiz ortak).
 *
 * Bir parça metni cümlelere bölünür; hastalık adı/takma adı geçen cümle bölüm ipuçlarıyla (tedavi, tanı, görüntüleme…)
 * sınıflanır ve kalite puanı alır. Soru kökleri ("…hangisidir?"), OCR kırıntıları ve başlık satırları kanıt sayılmaz.
 */
import { type IntentKey, classifyEvidence, fold } from '../queryIntel/core';
import { cleanContent } from '../queryIntel/build';

export type SectionKey = IntentKey | 'general';

/** Bölüm → DiseaseProfile alanı */
export const SECTION_FIELD: Record<IntentKey, string> = {
  treatment: 'treatment',
  diagnosis: 'diagnostic_methods',
  imaging: 'imaging_findings',
  symptoms: 'symptoms_clinical',
  etiology: 'etiology',
  pathology: 'morphology_pathology',
  physiology: 'physiology_pathophysiology',
  epidemiology: 'epidemiology',
  pathognomonic: 'pathognomonic_features',
};

export const SECTION_LABEL: Record<SectionKey, string> = {
  treatment: 'Tedavi', diagnosis: 'Tanı', imaging: 'Görüntüleme', symptoms: 'Klinik bulgular', etiology: 'Etiyoloji',
  pathology: 'Patoloji', physiology: 'Fizyopatoloji', epidemiology: 'Epidemiyoloji', pathognomonic: 'Patognomonik / ayırıcı tanı',
  general: 'Genel',
};

/** Kanıt kaynağı katmanı: ders materyali > çıkmış soru > türetilmiş (örnek soru / deste) */
export const SOURCE_TIER: Record<string, number> = {
  lecture_slide: 3, summary: 3, transcript: 3, past_question: 2, ornek_question: 1, deck_slide: 1,
};

export interface EvidenceSource {
  type: string;
  title: string;
  chunkId: string;
  committee?: string;
  discipline?: string;
}

export interface Evidence {
  t: string;
  section: SectionKey;
  score: number;
  src: EvidenceSource;
}

const SENT_SPLIT = /(?<=[.!?…])\s+|\n+|\s•\s|;\s+/;

export function splitSentences(text: string): string[] {
  const out: string[] = [];
  for (const raw of cleanContent(text).split(SENT_SPLIT)) {
    const s = raw.replace(/^[\s\-–•*>#\d.)]+/, '').replace(/\s+/g, ' ').trim();
    if (s.length >= 25 && s.length <= 420) out.push(s);
  }
  return out;
}

/** Cümle kanıt olabilir mi + kalite puanı (0 = değil) */
export function sentenceQuality(s: string): number {
  if (/\?\s*$/.test(s) || /aşağıdakilerden|hangisi(dir)?\b|hangileri/i.test(s)) return 0; // soru kökü
  if (/^[A-D]\)|^[A-E]\s*[).:-]\s/.test(s)) return 0; // şık
  const letters = (s.match(/\p{L}/gu) || []).length;
  if (letters / s.length < 0.68) return 0; // OCR / tablo kırıntısı
  const upper = (s.match(/\p{Lu}/gu) || []).length;
  if (upper / Math.max(1, letters) > 0.45) return 0; // başlık satırı
  const words = s.split(/\s+/).length;
  if (words < 5) return 0;
  // 12-40 sözcük ideal
  return words < 12 ? 0.6 + words * 0.03 : words <= 40 ? 1 : Math.max(0.5, 1 - (words - 40) * 0.02);
}

/** Cümleden bölüm(ler): en güçlü ipucu; eşit güçte ilk iki bölüm. İpucu yoksa 'general'. */
export function sectionsOf(sentence: string): Array<[SectionKey, number]> {
  const cls = classifyEvidence(fold(sentence));
  if (!cls.length) return [['general', 1]];
  const top = cls[0][1];
  return cls.filter(([, sc]) => sc >= top * 0.75).slice(0, 2);
}

/** Aynı bilginin farklı dosyalardaki kopyalarını tek saymak için imza */
export function sentenceSig(s: string): string {
  return fold(s).replace(/[^a-z0-9]+/g, '').slice(0, 90);
}

/**
 * Bölüm başına en iyi K kanıtı tutan küçük kova (puan sıralı, imza tekil).
 */
export class EvidenceBucket {
  private by = new Map<SectionKey, Evidence[]>();
  private sigs = new Set<string>();
  constructor(private k = 6) {}

  add(e: Evidence): void {
    const sig = sentenceSig(e.t);
    if (this.sigs.has(`${e.section}|${sig}`)) return;
    let arr = this.by.get(e.section);
    if (!arr) { arr = []; this.by.set(e.section, arr); }
    if (arr.length >= this.k && arr[arr.length - 1].score >= e.score) return;
    this.sigs.add(`${e.section}|${sig}`);
    arr.push(e);
    arr.sort((a, b) => b.score - a.score);
    if (arr.length > this.k) arr.length = this.k;
  }

  toJSON(): Partial<Record<SectionKey, Evidence[]>> {
    const o: Partial<Record<SectionKey, Evidence[]>> = {};
    for (const [k, v] of this.by) o[k] = v;
    return o;
  }

  count(section: SectionKey): number {
    return this.by.get(section)?.length || 0;
  }
}

/** Hastalık profili şablon/dolgu cümleleri: birden çok hastalıkta adı maskelenince birebir aynı olan ifadeler */
export function placeholderSignatures(diseases: Array<{ name: string } & Record<string, any>>, fields: string[], minRepeat = 5): Set<string> {
  const count = new Map<string, number>();
  for (const d of diseases) {
    const seen = new Set<string>();
    for (const f of fields) {
      const v = d[f];
      for (const s of Array.isArray(v) ? v : v ? [v] : []) {
        const sig = maskSig(String(s), d.name);
        if (!sig || seen.has(sig)) continue;
        seen.add(sig);
        count.set(sig, (count.get(sig) || 0) + 1);
      }
    }
  }
  return new Set([...count].filter(([, n]) => n >= minRepeat).map(([k]) => k));
}

export function maskSig(s: string, name: string): string {
  let t = s;
  if (name) t = t.split(name).join('<N>');
  return fold(t).replace(/[^a-z0-9<>]+/g, ' ').trim().slice(0, 120);
}
