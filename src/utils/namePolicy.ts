import { OFFICIAL_CURRICULUM_COMMITTEES } from '../data/curriculumData';

/**
 * Normalizes text for comparison:
 * - lowercase Turkish (i -> i, I -> ı)
 * - removes diacritics / accents
 * - removes punctuation and extra whitespace
 */
export function normalizeText(text: string): string {
  if (!text) return '';
  return text
    .toLocaleLowerCase('tr-TR')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

/**
 * Strict regex list for Dr. House and all character/show variations specified:
 * 1. Dr House
 * 2. Dr.house
 * 3. Dr. House
 * 4. Doctor House
 * 5. Dr. H.
 * 6. Dr H
 * 7. House MD
 * 8. House, M.D.
 * 9. House M.D.
 * 10. Dr. Gregory House
 * 11. Doctor Gregory House
 * 12. Dr Gregory House
 * 13. Gregory House
 * 14. Gregory House, M.D.
 * 15. Dr. G. House
 * 16. Dr G House
 * 17. Dr. Greg House
 * 18. Greg House
 * 19. Doctor Greg House
 * 20. Dr. House, M.D.
 * 21. DR. HOUSE
 * 22. DR HOUSE
 * 23. HOUSE MD
 * 24. dr house
 * 25. dr. house
 * 26. dr.house
 * 27. house m.d.
 * 28. Dr. House MD
 * 29. Dr House M.D.
 * 30. Doktor House
 * 31. Dk. House
 * 32. Dr. House (M.D.)
 * 33. House (MD)
 * 34. Dr. G. H.
 * 35. Dr. H
 * 36. Doc House
 * 37. House, Gregory
 * 38. House, Gregory, M.D.
 * 39. G. House, M.D.
 * 40. Dr. Gregory "Greg" House
 */
const FORBIDDEN_CHARACTER_PATTERNS: RegExp[] = [
  /\b(?:dr|dr\.|doktor|dk\.|doc|doctor)\.?\s*house\b/i,
  /\bhouse\s*,?\s*(?:m\.?\s*d\.?|md)\b/i,
  /\bgreg(?:ory)?\s*house\b/i,
  /\bhouse\s*,?\s*greg(?:ory)?\b/i,
  /\b(?:dr|dr\.|doktor|doctor)\.?\s*g(?:reg)?\.?\s*house\b/i,
  /\bg\.?\s*house\b/i,
  /\bdr\.?\s*g\.?\s*h\.?\b/i,
  /\bdr\.?\s*h\.?\b/i,
  /\bhouse\s*\(\s*m\.?\s*d\.?\s*\)/i,
  /\bhouse\b/i // Catch generic standalone "house" when used as medical/fictional alias
];

/**
 * Build dynamic list of instructor names (first + last name pairs) from the official curriculum.
 */
function extractCurriculumInstructors(): Array<{ fullName: string; firstName: string; lastName: string }> {
  const rawList = new Set<string>();

  OFFICIAL_CURRICULUM_COMMITTEES.forEach((comm) => {
    if (comm.president) rawList.add(comm.president);
    comm.disciplines.forEach((d) => {
      d.instructors.forEach((inst) => rawList.add(inst));
    });
  });

  const parsed: Array<{ fullName: string; firstName: string; lastName: string }> = [];

  rawList.forEach((raw) => {
    // Strip academic titles: Prof., Doç., Dr., Öğr., Üyesi, Uzm., Uz.
    const clean = raw
      .replace(/\b(?:prof|doc|doç|dr|ogr|öğr|uyesi|üyesi|uzm|uz)\.?\b/gi, '')
      .replace(/\s+/g, ' ')
      .trim();

    const parts = clean.split(' ').filter(Boolean);
    if (parts.length >= 2) {
      const lastName = parts[parts.length - 1];
      const firstName = parts.slice(0, parts.length - 1).join(' ');
      parsed.push({
        fullName: clean,
        firstName,
        lastName,
      });
    }
  });

  return parsed;
}

export const CURRICULUM_INSTRUCTORS = extractCurriculumInstructors();

export interface NameValidationResult {
  isValid: boolean;
  errorMessage?: string;
  matchedType?: 'fictional_character' | 'instructor_name';
  matchedDetails?: string;
}

/**
 * Validates a user name or contributor name against forbidden fictional names (Dr. House)
 * and real curriculum instructor names (first name + last name together).
 */
export function validateNamePolicy(rawName: string | null | undefined): NameValidationResult {
  if (!rawName || !rawName.trim()) {
    return {
      isValid: false,
      errorMessage: 'Lütfen adınızı ve soyadınızı eksiksiz giriniz.',
    };
  }

  const trimmed = rawName.trim();
  const normalized = normalizeText(trimmed);

  // 1. Check Dr House & character variations
  for (const pattern of FORBIDDEN_CHARACTER_PATTERNS) {
    if (pattern.test(trimmed) || pattern.test(normalized)) {
      return {
        isValid: false,
        errorMessage: 'Güvenlik ve resmiyet gereği "Dr. House" veya dizi/karakter takma adları kullanıcı/kişi adı olarak kullanılamaz. Lütfen kendi gerçek adınızı ve soyadınızı giriniz.',
        matchedType: 'fictional_character',
        matchedDetails: 'Dr. House / Fictional Name',
      };
    }
  }

  // Also check compact text (e.g. "drhouse", "doctorhouse", "drh")
  const compact = normalized.replace(/\s+/g, '');
  if (
    compact === 'drhouse' ||
    compact === 'drh' ||
    compact === 'drgregoryhouse' ||
    compact === 'gregoryhouse' ||
    compact === 'housemd' ||
    compact === 'doktorhouse' ||
    compact === 'dochouse'
  ) {
    return {
      isValid: false,
      errorMessage: 'Güvenlik ve resmiyet gereği "Dr. House" veya dizi/karakter takma adları kullanıcı/kişi adı olarak kullanılamaz. Lütfen kendi gerçek adınızı ve soyadınızı giriniz.',
      matchedType: 'fictional_character',
      matchedDetails: 'Dr. House / Fictional Name',
    };
  }

  // 2. Check Curriculum Instructor Names (Both first name and last name must be present)
  for (const inst of CURRICULUM_INSTRUCTORS) {
    const normFirst = normalizeText(inst.firstName);
    const normLast = normalizeText(inst.lastName);

    if (!normFirst || !normLast || normLast.length < 2) continue;

    // Check if both the first name tokens (or part of it) and last name are in the user name
    const normFirstParts = normFirst.split(' ').filter((p) => p.length >= 2);
    const normLastPart = normLast;

    const hasLastName = new RegExp(`\\b${normLastPart}\\b`, 'i').test(normalized);
    const hasFirstName = normFirstParts.some((p) => new RegExp(`\\b${p}\\b`, 'i').test(normalized));

    if (hasLastName && hasFirstName) {
      return {
        isValid: false,
        errorMessage: `Fakülte öğretim üyemizin adı (${inst.fullName}) kullanıcı adı veya kişi adı olarak kullanılamaz! Lütfen kendi adınızı, soyadınızı ve öğrenci numaranızı kullanınız.`,
        matchedType: 'instructor_name',
        matchedDetails: inst.fullName,
      };
    }
  }

  return { isValid: true };
}
