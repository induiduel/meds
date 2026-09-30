// Comprehensive multilingual profanity filter (Turkish, English, etc.)
// Replaces forbidden terms and profanity with asterisks preserving string length or masking.

const PROFANITY_LIST = [
  // Turkish profanity & slurs
  'amk', 'aq', 'sik', 'sikiş', 'siktir', 'orospu', 'pic', 'piç', 'yarak', 'yarrak',
  'got', 'göt', 'amına', 'amina', 'amcık', 'amcik', 'ibne', 'puşt', 'pust',
  'kahpe', 'sürtük', 'surtuk', 'yarram', 'taşak', 'tasak', 'döl', 'dol',
  'sikik', 'sokayım', 'sokayim', 'sokam', 'oç', 'oc', 'orospuçocuğu',
  'götveren', 'gotveren', 'pezevenk', 'pezevenk', 'amguard', 'yavşak', 'yavsak',
  'ebenin', 'ananı', 'anani', 'ananın', 'ananin', 'gavat', 'kavat', 'fahişe', 'fahise',
  
  // English profanity & slurs
  'fuck', 'fucking', 'fucker', 'shit', 'bitch', 'asshole', 'cunt', 'dick',
  'pussy', 'bastard', 'cock', 'whore', 'slut', 'nigger', 'nigga', 'faggot',
  'retard', 'twat', 'wanker', 'motherfucker', 'bullshit', 'dipshit', 'jackass'
];

/**
 * Normalizes text to handle leetspeak and special character obfuscation
 * e.g., s!k, s1k, @mk, etc.
 */
function normalizeText(text: string): string {
  return text
    .toLowerCase()
    .replace(/[0o]/g, 'o')
    .replace(/[1li!|]/g, 'i')
    .replace(/[@a]/g, 'a')
    .replace(/[3e]/g, 'e')
    .replace(/[$sş]/g, 's')
    .replace(/[çc]/g, 'c')
    .replace(/[ğg]/g, 'g')
    .replace(/[üu]/g, 'u')
    .replace(/[öo]/g, 'o')
    .replace(/[\s\-_.]+/g, '');
}

/**
 * Checks if a nickname or text contains any profanity in any language
 */
export function hasProfanity(text: string): boolean {
  if (!text || text.trim() === '') return false;
  
  const lower = text.toLowerCase();
  const normalized = normalizeText(text);

  // Check whole words and substrings
  for (const badWord of PROFANITY_LIST) {
    const normBad = normalizeText(badWord);
    
    // Check regex word boundary or exact occurrence
    const regex = new RegExp(`\\b${badWord}\\b`, 'i');
    if (regex.test(lower) || normalized.includes(normBad)) {
      return true;
    }
  }

  return false;
}

/**
 * Censors profanity by replacing offending words with asterisks (***)
 */
export function censorProfanity(text: string): string {
  if (!text) return '';
  let result = text;

  for (const badWord of PROFANITY_LIST) {
    const regex = new RegExp(`(${badWord})`, 'gi');
    result = result.replace(regex, (match) => '*'.repeat(match.length));
  }

  // Also catch concatenated / normalized variants if needed
  const normalized = normalizeText(text);
  for (const badWord of PROFANITY_LIST) {
    const normBad = normalizeText(badWord);
    if (normBad.length >= 3 && normalized.includes(normBad)) {
      // If still visible, do a safe character mask
      const regex = new RegExp(badWord.split('').join('[^a-zA-Z0-9]*'), 'gi');
      result = result.replace(regex, '***');
    }
  }

  return result;
}

/**
 * Formats student rumuz/nickname safely
 */
export function getCleanRumuz(rumuz?: string | null, fallback = 'Dönem 3 Öğrencisi'): string {
  if (!rumuz || rumuz.trim() === '') return fallback;
  return censorProfanity(rumuz.trim());
}
