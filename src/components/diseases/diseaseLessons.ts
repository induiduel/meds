import { useEffect, useState } from 'react';

/**
 * Hastalık → ders programı (Kurul → Ders → Konu) eşlemesi: src/data/disease_lessons.json.
 * Üretim: `python3 scripts/diseases/hastalik_ders_eslesmesi.py [--rapor]` (yalnız CPU; diseases.json, kazanımlar,
 * çıkmış soru konu etiketleri ya da ders özetleri değişince yeniden çalıştır). Eşleşme tahmin değildir: profilin adı /
 * eş adı / Latince adı o konunun metninde sözcük sınırıyla geçmelidir (ayrıntı betiğin başında).
 */
export interface LessonTopic {
  k: number;
  d: string;
  t: string;
  /** Öğren destesi (yalnız kesin bağlı konular) */
  deck?: string;
  /** Konuya bağlı ders özeti sayısı */
  ozet: number;
}

/** [konu dizini, geçiş sayısı, kaynak bayrakları] */
export type LessonHit = [number, number, number];

export interface DiseaseLessonData {
  v: number;
  uretim: string;
  kapsam: { profil: number; eslesen: number; konu: number; konuHastalikli: number; ozetKonuya: number; ozetToplam: number };
  kurullar: Array<{ k: number; ad: string }>;
  konular: LessonTopic[];
  hastaliklar: Record<string, LessonHit[]>;
}

export const LESSON_FLAG = { baslik: 1, ozet: 2, kazanim: 4, cikmis: 8 } as const;

/** Bayraklar → "konu başlığında · ders özetinde · çıkmışta" */
export function lessonFlagText(f: number): string {
  const out: string[] = [];
  if (f & LESSON_FLAG.baslik) out.push('konu başlığında');
  if (f & LESSON_FLAG.ozet) out.push('ders özetinde');
  if (f & LESSON_FLAG.kazanim) out.push('kazanımda');
  if (f & LESSON_FLAG.cikmis) out.push('çıkmış soruda');
  return out.join(' · ');
}

/** Ders programı süzgeci seçimi: kurul → ders → konu (konu = konular dizini) */
export interface LessonSel {
  k?: number;
  d?: string;
  t?: number;
}

export const lessonSelOn = (s: LessonSel) => s.k != null || s.d != null || s.t != null;

export function topicMatches(x: LessonTopic, i: number, s: LessonSel): boolean {
  if (s.t != null) return i === s.t;
  if (s.k != null && x.k !== s.k) return false;
  if (s.d != null && x.d !== s.d) return false;
  return true;
}

let cache: Promise<DiseaseLessonData | null> | null = null;
const load = () => {
  if (!cache) {
    cache = import('../../data/disease_lessons.json')
      .then((m) => ((m as any).default ?? m) as DiseaseLessonData)
      .catch(() => { cache = null; return null; });
  }
  return cache;
};

/** Eşleme verisini tembel yükler (~56 KB, ayrı parça) */
export function useDiseaseLessons(): DiseaseLessonData | null {
  const [data, setData] = useState<DiseaseLessonData | null>(null);
  useEffect(() => {
    let alive = true;
    load().then((d) => { if (alive) setData(d); });
    return () => { alive = false; };
  }, []);
  return data;
}
