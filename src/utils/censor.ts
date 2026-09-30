/**
 * Multi-language profanity / abusive words filter
 * Replaces foul language across Turkish, English, and common variants with asterisks (****).
 */

const BAD_WORDS_PATTERNS = [
  // Turkish profanity / slang roots & variants
  /\b(amk|aq|o\.ç|oc|orospu|orospuçocuğu|piç|yavşak|siktir|sikik|sik|sikiş|göt|gavat|pezevenk|amcık|yarrak|taşak|kahpe|ibne|puşt|kancık)\b/gi,
  /o\s*r\s*o\s*s\s*p\s*u/gi,
  /s\s*i\s*k\s*t\s*i\s*r/gi,
  /y\s*a\s*r\s*r\s*a\s*k/gi,
  /a\s*m\s*c\s*ı\s*k/gi,
  /p\s*i\s*ç/gi,
  /g\s*ö\s*t/gi,
  /a\s*m\s*k/gi,
  /a\s*q/gi,

  // English profanity roots & variants
  /\b(fuck|fucker|fucking|f\*ck|bitch|shit|asshole|bastard|dick|pussy|cunt|motherfucker|whore|slut|bullshit)\b/gi,
  /f\s*u\s*c\s*k/gi,
  /b\s*i\s*t\s*c\s*h/gi,
  /s\s*h\s*i\s*t/gi,
];

/**
 * Replaces abusive words with ****
 */
export function censorText(text: string | null | undefined): string {
  if (!text) return '';
  let cleaned = text;

  for (const pattern of BAD_WORDS_PATTERNS) {
    cleaned = cleaned.replace(pattern, (match) => '*'.repeat(match.length));
  }

  return cleaned;
}

/**
 * Checks if the given text contains profanity
 */
export function containsProfanity(text: string | null | undefined): boolean {
  if (!text) return false;
  return BAD_WORDS_PATTERNS.some((pattern) => pattern.test(text));
}
