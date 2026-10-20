/**
 * QuickAddHero'nun ortak yardımcıları (başarım turu 2026-10-20): soru kartı, havuz, matris vb.
 * bunları ilk pakette kullanır; QuickAddHero bileşeni ise tembel yüklenir.
 */
import React from 'react';
import { Check, CircleDashed } from 'lucide-react';
import { Committee, QuestionItem } from '../types';

// Benzerlik puanı kademesine göre renk ve stil haritası
export const getScoreTier = (score: number) => {
  if (score >= 80) {
    return {
      tierName: 'Çok Yüksek Uyum',
      pillBg: 'bg-ok/15 text-ok border-ok/30',
      barColor: 'bg-ok',
      cardBorder: 'border-ok/30 bg-ok-soft/50 hover:border-ok',
    };
  }
  if (score >= 65) {
    return {
      tierName: 'Yüksek Benzerlik',
      pillBg: 'bg-warn/15 text-warn border-warn/30',
      barColor: 'bg-warn',
      cardBorder: 'border-warn/30 bg-warn-soft/50 hover:border-warn',
    };
  }
  if (score >= 50) {
    return {
      tierName: 'Orta Benzerlik',
      pillBg: 'bg-accent/15 text-accent border-accent/30',
      barColor: 'bg-accent',
      cardBorder: 'border-accent/30 bg-accent-soft/40 hover:border-accent/30',
    };
  }
  return {
    tierName: 'İlişkili Konu',
    pillBg: 'bg-ai/15 text-ai border-ai/30',
    barColor: 'bg-ai',
    cardBorder: 'border-ai/30 bg-ai-soft/30 hover:border-ai/30',
  };
};

/**
 * Rozet (#etiket) ve ortak-terim boyası eşiği: yalnızca %80+ ("Çok Yüksek Uyum")
 * kartlarda gösterilir. Altındaki skorlarda rozet yanıltıcı olabiliyor
 * (örn. muğlak girdide alakasız hastalık etiketi).
 */
export const HIGHLIGHT_MIN_SCORE = 80;

/** Öğretim yılı Eylül'de başlar: 9 Ekim 2026 → "2026-2027" */
export const currentAcademicYear = (d = new Date()) => {
  const y = d.getMonth() >= 8 ? d.getFullYear() : d.getFullYear() - 1;
  return `${y}-${y + 1}`;
};
/** 2016-2017'den bu yıla kadar öğretim yılları, yeniden eskiye */
export const academicYears = () => {
  const last = Number(currentAcademicYear().slice(0, 4));
  return Array.from({ length: last - 2016 + 1 }, (_, i) => `${last - i}-${last - i + 1}`);
};

export const committeeShortLabel = (c: Committee) => {
  const m = c.name.match(/Kurul\s*(\d+)/i);
  if (m) return `Kurul ${m[1]}`;
  // Önce kimliğe bakılır: Final kurulunun adı "bütünleme" sözcüğünü de içerebiliyor
  if (/final/i.test(c.id)) return 'Final';
  if (/b[uü]t[uü]nleme/i.test(c.id)) return 'Bütünleme';
  if (/bütünleme/i.test(c.name)) return 'Bütünleme';
  if (/final/i.test(c.name)) return 'Final';
  return c.code || c.name;
};

export const questionStemText = (q: QuestionItem) =>
  q.reconstruction?.stem || q.rawStem || q.fragments.find((f) => f.type === 'stem')?.text || q.fragments[0]?.text || q.topic;

export const StatusPill: React.FC<{ status: QuestionItem['status']; hasFragments?: boolean }> = ({ status, hasFragments }) => {
  if (status === 'completed') {
    return (
      <span className="inline-flex items-center gap-1.5 h-7 px-2.5 rounded-full bg-ok-soft text-ok text-xs font-semibold whitespace-nowrap">
        <Check className="w-[13px] h-[13px]" strokeWidth={3} />
        Doğrulandı
      </span>
    );
  }
  if (status === 'empty' && !hasFragments) {
    return (
      <span className="inline-flex items-center gap-1.5 h-7 px-2.5 rounded-full bg-canvas text-ink-2 text-xs font-semibold whitespace-nowrap">
        Boş
      </span>
    );
  }
  return (
    <span className="inline-flex items-center gap-1.5 h-7 px-2.5 rounded-full bg-warn-soft text-warn text-xs font-semibold whitespace-nowrap">
      <CircleDashed className="w-[13px] h-[13px]" strokeWidth={2.6} />
      Taslak
    </span>
  );
};

/**
 * Resmi ders programına göre bir kurulun soru girişine açılıp açılmadığını kontrol eder.
 * Kural: Önceki kurulun sınav tarihi tamamlanmadan bir sonraki kurula soru yazılamaz.
 * (Kurul 1 daima açıktır; Kurul 2 için Kurul 1 sınavı bitmiş olmalıdır; vb.)
 */
export const COMMITTEE_EXAM_DATES: Record<string, string> = {
  'donem3-kurul1': '2026-10-23T23:59:59',
  'donem3-kurul2': '2026-12-04T23:59:59',
  'donem3-kurul3': '2027-01-22T23:59:59',
  'donem3-kurul4': '2027-03-05T23:59:59',
  'donem3-kurul5': '2027-04-22T23:59:59',
  'donem3-kurul6': '2027-06-11T23:59:59',
  'donem3-final': '2027-06-28T23:59:59',
  'donem3-butunleme': '2027-07-16T23:59:59',
};

const COMMITTEE_SEQUENCE = [
  'donem3-kurul1',
  'donem3-kurul2',
  'donem3-kurul3',
  'donem3-kurul4',
  'donem3-kurul5',
  'donem3-kurul6',
  'donem3-final',
  'donem3-butunleme',
];

/**
 * Kurul kilidi yalnız bu öğretim yılının soruları içindir (sınav takvimi bu yıla ait). Eski bir sınav yılı
 * seçildiyse o yılın bütün sınavları yapılmıştır: tüm kurullar açıktır. "Bilmiyorum" (boş) bu yıl sayılır.
 */
export const isCommitteeLocked = (committeeId: string, examYear?: string): boolean => {
  if (examYear && examYear !== currentAcademicYear()) return false;
  const idx = COMMITTEE_SEQUENCE.indexOf(committeeId);
  if (idx <= 0) return false; // Kurul 1 her zaman açıktır
  const prevCommitteeId = COMMITTEE_SEQUENCE[idx - 1];
  const prevDateStr = COMMITTEE_EXAM_DATES[prevCommitteeId];
  if (!prevDateStr) return false;
  return new Date() < new Date(prevDateStr);
};
