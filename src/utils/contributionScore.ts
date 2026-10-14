import type { QuestionItem } from '../types';
import type { AppUser } from '../services/auth';
import { getCleanRumuz } from '../services/profanityFilter';

/**
 * Katkı puanları ve sıralama — Sıralama sayfası ve İstatistiklerim aynı hesabı kullanır.
 * Puan: soru +10, parça/şık +5, düzeltme +5, aldığı her beğeni +2. Yapay zekâ ve sistem hesapları hariç.
 */
export interface ContributorStats {
  id: string;
  name: string;
  studentNumber?: string;
  questionsCount: number;
  optionsCount: number;
  upvotesCount: number;
  revisionsCount: number;
  totalPoints: number;
  isCurrentUser: boolean;
}

export function computeContributorStats(
  relevantQuestions: QuestionItem[],
  currentUser: AppUser | null,
  opts: { includeSamplePassive?: boolean } = {},
): ContributorStats[] {
  const statsMap: Record<string, ContributorStats> = {};

  // Yapay zeka botları ve sistem hesaplarını sıralamadan hariç tut
  const isBotOrSystem = (name?: string, key?: string) => {
    const s = `${name || ''} ${key || ''}`.toLocaleLowerCase('tr-TR');
    return (
      s.includes('yapay zeka') ||
      s.includes('ai (') ||
      s.includes(' ai') ||
      s.startsWith('ai') ||
      s.includes('bot') ||
      s.includes('gemini') ||
      s.includes('gpt') ||
      s.includes('deepseek') ||
      s.includes('claude') ||
      s.includes('asistan') ||
      s.includes('reconstruct') ||
      s.includes('otomasyon') ||
      s.includes('sistem') ||
      s.includes('system') ||
      s.includes('ocr') ||
      s.includes('taranmış') ||
      s.includes('arşivi') ||
      s.includes('arşiv') ||
      s.includes('taslak ayırma')
    );
  };

  // Hangi satır kimlikle (uid), hangisi yalnız adla açıldı — sondaki birleştirme için
  const uidKeys = new Set<string>();
  const nameOnlyKeys = new Set<string>();
  const looksLikeUid = (k: string) => /^[A-Za-z0-9_-]{20,}$/.test(k) && !/\s/.test(k);

  // Helper to get or create stats entry
  const getEntry = (key: string, name: string, studentNumber?: string): ContributorStats | null => {
    if (isBotOrSystem(name, key)) return null;
    const rawKey = key.trim().toLowerCase();
    const isCurrent = !!(
      (currentUser?.uid && key === currentUser.uid) ||
      (currentUser?.displayName && rawKey === currentUser.displayName.trim().toLowerCase())
    );
    // Oturumdaki kişinin uid'le ve yalnız adla yazılmış katkıları tek satırda toplanır (çift "Sen" satırı olmasın)
    const cleanKey = isCurrent ? (currentUser!.uid || currentUser!.displayName || rawKey).trim().toLowerCase() : rawKey;
    if (isCurrent || looksLikeUid(key)) uidKeys.add(cleanKey); else nameOnlyKeys.add(cleanKey);
    if (!statsMap[cleanKey]) {

      statsMap[cleanKey] = {
        id: cleanKey,
        name: getCleanRumuz(name || 'Anonim Tıbbiyeli'),
        studentNumber: studentNumber || (isCurrent ? currentUser?.studentNumber || undefined : undefined),
        questionsCount: 0,
        optionsCount: 0,
        upvotesCount: 0,
        revisionsCount: 0,
        totalPoints: 0,
        isCurrentUser: isCurrent,
      };
    }
    return statsMap[cleanKey];
  };

  // Calculate points from questions
  relevantQuestions.forEach((q) => {
    // 1. Question creators
    if (q.contributedByName || q.contributedByUid) {
      const key = q.contributedByUid || q.contributedByName!;
      const entry = getEntry(key, q.contributedByName || 'Öğrenci', q.contributedByStudentNumber);
      if (entry) {
        entry.questionsCount += 1;
        entry.totalPoints += 10; // +10 points for introducing a question
      }
    }

    // 2. Memory fragments (stem, clue, text)
    q.fragments.forEach((f) => {
      if (f.author && f.author !== 'Anonim' && f.author !== 'Hafıza Parçası') {
        const key = f.authorUid || f.author;
        const entry = getEntry(key, f.author, f.authorStudentNumber);
        if (entry) {
          if (f.type === 'stem') {
            entry.questionsCount += 1;
            entry.totalPoints += 10;
          } else {
            entry.totalPoints += 5;
          }
          entry.upvotesCount += (f.upvotes || 0);
          entry.totalPoints += (f.upvotes || 0) * 2; // +2 points per upvote
        }
      }
    });

    // 3. Options
    q.options.forEach((opt) => {
      if (opt.suggestedBy && opt.suggestedBy !== 'Anonim' && !opt.isAiGenerated) {
        const key = opt.suggestedByUid || opt.suggestedBy;
        const entry = getEntry(key, opt.suggestedBy);
        if (entry) {
          entry.optionsCount += 1;
          entry.totalPoints += 5; // +5 points for providing an option
          entry.upvotesCount += (opt.upvotes || 0);
          entry.totalPoints += (opt.upvotes || 0) * 2; // +2 points per upvote
        }
      }
    });

    // 4. Revisions
    if (q.revisions) {
      q.revisions.forEach((rev) => {
        if (rev.editorName && rev.editorName !== 'Anonim') {
          const key = rev.editorUid || rev.editorName;
          const entry = getEntry(key, rev.editorName, rev.editorStudentNumber);
          if (entry) {
            entry.revisionsCount += 1;
            entry.totalPoints += 5; // +5 points for refining and editing
          }
        }
      });
    }
  });

  // Ensure current logged-in user is listed even if 0 contributions
  if (currentUser) {
    const userKey = currentUser.uid || currentUser.displayName || currentUser.email || 'me';
    const cleanUserKey = userKey.trim().toLowerCase();
    if (!statsMap[cleanUserKey]) {
      statsMap[cleanUserKey] = {
        id: cleanUserKey,
        name: getCleanRumuz(currentUser.displayName || currentUser.email?.split('@')[0] || 'Ben'),
        studentNumber: currentUser.studentNumber || undefined,
        questionsCount: 0,
        optionsCount: 0,
        upvotesCount: 0,
        revisionsCount: 0,
        totalPoints: 0,
        isCurrentUser: true,
      };
    } else {
      statsMap[cleanUserKey].isCurrentUser = true;
    }
  }

  // Add sample registered classmates who haven't contributed yet so they appear in list as requested
  const samplePassiveUsers = [
    { key: 'ogrenci_ali', name: 'Alperen_Tıp3', studentNumber: '2101030012' },
    { key: 'ogrenci_selin', name: 'DrSelin', studentNumber: '2101030045' },
    { key: 'ogrenci_burak', name: 'BurakC_Med', studentNumber: '2101030089' },
  ];
  samplePassiveUsers.forEach((su) => {
    if (!statsMap[su.key]) {
      statsMap[su.key] = {
        id: su.key,
        name: getCleanRumuz(su.name),
        studentNumber: su.studentNumber,
        questionsCount: 0,
        optionsCount: 0,
        upvotesCount: 0,
        revisionsCount: 0,
        totalPoints: 0,
        isCurrentUser: false,
      };
    }
  });

  // Yalnız adla (uid'siz) yazılmış katkılar, aynı rumuzu taşıyan TEK kimlikli kişiye bağlanır (aynı kişi iki satır olmasın).
  // Aynı adı taşıyan birden çok kimlik varsa kimin olduğu bilinemez; satır ayrı kalır.
  for (const nameKey of nameOnlyKeys) {
    const e = statsMap[nameKey];
    if (!e || uidKeys.has(nameKey)) continue;
    const owners = Object.values(statsMap).filter((o) => o !== e && uidKeys.has(o.id) && o.name.toLocaleLowerCase('tr-TR') === e.name.toLocaleLowerCase('tr-TR'));
    if (owners.length !== 1) continue;
    const o = owners[0];
    o.questionsCount += e.questionsCount; o.optionsCount += e.optionsCount; o.upvotesCount += e.upvotesCount;
    o.revisionsCount += e.revisionsCount; o.totalPoints += e.totalPoints;
    o.isCurrentUser = o.isCurrentUser || e.isCurrentUser;
    o.studentNumber = o.studentNumber || e.studentNumber;
    delete statsMap[nameKey];
  }

  // Sort descending by totalPoints
  const sorted = Object.values(statsMap).sort((a, b) => {
    if (b.totalPoints !== a.totalPoints) return b.totalPoints - a.totalPoints;
    if (b.questionsCount !== a.questionsCount) return b.questionsCount - a.questionsCount;
    return b.upvotesCount - a.upvotesCount;
  });

  return sorted;
}
