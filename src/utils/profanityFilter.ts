/**
 * MeDSor Türkçe Argo, Küfür ve Hakaret Filtresi
 * Yorumları, soru açıklamalarını ve kullanıcı girdilerini temizlemek için kullanılır.
 */

// Kök ve yaygın varyasyonlar
const PROFANITY_PATTERNS: RegExp[] = [
  /\b(o[çc]|o\.ç\.)\b/gi,
  /\b(am[kq]|a\.m\.k|aq)\b/gi,
  /\b(pi[çc]|piç|pic)\b/gi,
  /\b(sik|siki[şs]|sikim|sikti|sik[eé]r|sokayım|sokam|siktim)\w*/gi,
  /\b(amcık|amc[ıi]k|am[ıi]na|amcik|amina|amına|amına koy|amk)\w*/gi,
  /\b(yarrak|yarr[aä]k|yarak|yarra[gğ]ı|yarram)\w*/gi,
  /\b(g[oö]t[üu]|g[oö]tveren|g[oö]to[sş]|göt|got)\b/gi,
  /\b(orospu|orospunun|kahpe|orospucocugu|kaltak|fahise|fahişe)\w*/gi,
  /\b(ibne|ibneler|pu[sş]t)\b/gi,
  /\b(taşşak|taşak|tassak)\w*/gi,
  /\b(daşşak|dassak)\w*/gi,
  /\b(pezevenk|pezevenkler)\w*/gi,
  /\b(sürtük|surtuk)\w*/gi,
  /\b(bok|boktan|bokun|boklu)\b/gi,
  /\b(şerefsiz|serefsiz|haysiyetsiz|namussuz)\w*/gi,
  /\b(mal|salak|gerizekalı|gerizekali|ahmak)\b/gi, // hafif argo/hakaret
];

/**
 * Metinde küfür/argo var mı kontrol eder
 */
export function hasProfanity(text: string): boolean {
  if (!text || typeof text !== 'string') return false;
  return PROFANITY_PATTERNS.some((pattern) => pattern.test(text));
}

/**
 * Metindeki küfür ve argo kelimeleri tespit edip sansürler (örn: s***im, a***k)
 */
export function censorProfanity(text: string): string {
  if (!text || typeof text !== 'string') return text;

  let cleanText = text;

  for (const pattern of PROFANITY_PATTERNS) {
    cleanText = cleanText.replace(pattern, (match) => {
      if (match.length <= 2) {
        return '*'.repeat(match.length);
      }
      // İlk harfi bırak, kalanını yıldızla: s***
      return match[0] + '*'.repeat(match.length - 1);
    });
  }

  return cleanText;
}

/**
 * Girdi güvenliği: Yorum göndermeden önce temizler
 */
export function sanitizeCommentInput(input: string): { cleanText: string; hadProfanity: boolean } {
  const hadProfanity = hasProfanity(input);
  const cleanText = censorProfanity(input);
  return { cleanText, hadProfanity };
}
