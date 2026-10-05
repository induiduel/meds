/**
 * MedSoru Gelişmiş Türkçe Karakter Katlama, Kök Bulma (Stemming) &
 * Harf Eksikliği / Yer Değiştirme (Transposition) Toleranslı Arama Modülü
 * (src/utils/fuzzyMatching.ts)
 */

export const TR_FOLD: Record<string, string> = {
  ı: 'i',
  İ: 'i',
  ç: 'c',
  Ç: 'c',
  ğ: 'g',
  Ğ: 'g',
  ö: 'o',
  Ö: 'o',
  ş: 's',
  Ş: 's',
  ü: 'u',
  Ü: 'u',
  â: 'a',
  Â: 'a',
  î: 'i',
  Î: 'i',
  û: 'u',
  Û: 'u',
};

/**
 * Türkçe karakterleri katlar ve küçük harfe dönüştürür.
 * "böbrek", "bobrek", "IgE", "ige", "Down" -> "down"
 */
export function foldTurkish(text: string = ''): string {
  if (!text) return '';
  return text
    .toLocaleLowerCase('tr-TR')
    .replace(/[ıçğöşüâîûİÇĞÖŞÜÂÎÛ]/g, (ch) => TR_FOLD[ch] || ch);
}

/**
 * Damerau-Levenshtein Mesafesi:
 * Standart Levenshtein'a ek olarak BİTİŞİK HARF YER DEĞİŞTİRMELERİNİ (Transposition)
 * de tek işlem (maliyet = 1) olarak sayar.
 *
 * Örnekler:
 * - "sendrmu"  vs "sendromu" -> 1 (eksik harf / deletion)
 * - "sendormu" vs "sendromu" -> 1 (harflerin yer değiştirmesi: "or" <-> "ro")
 * - "kayrotip" vs "karyotip" -> 1 (harflerin yer değiştirmesi: "ay" <-> "ya")
 * - "triozmi"  vs "trizomi"  -> 1 (yer değiştirme: "oz" <-> "zo")
 */
export function damerauLevenshtein(a: string, b: string, maxLimit = 2): number {
  if (a === b) return 0;
  const al = a.length;
  const bl = b.length;
  if (Math.abs(al - bl) > maxLimit) return 99;
  if (al === 0) return bl;
  if (bl === 0) return al;

  const d: number[][] = Array.from({ length: al + 1 }, () => new Array(bl + 1).fill(0));

  for (let i = 0; i <= al; i++) d[i][0] = i;
  for (let j = 0; j <= bl; j++) d[0][j] = j;

  for (let i = 1; i <= al; i++) {
    for (let j = 1; j <= bl; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      d[i][j] = Math.min(
        d[i - 1][j] + 1, // silme / harf eksikliği
        d[i][j - 1] + 1, // ekleme
        d[i - 1][j - 1] + cost // değiştirme
      );

      // Bitişik harf yer değiştirmesi (Transposition / harflerin yerlerinin karıştırılması)
      if (i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) {
        d[i][j] = Math.min(d[i][j], d[i - 2][j - 2] + cost);
      }
    }
  }

  return d[al][bl];
}

/**
 * İki kelimenin Türkçe kök, harf eksikliği veya yer değiştirme açısından
 * benzer / eşdeğer olup olmadığını denetler.
 */
export function areWordsFuzzyEqual(w1: string, w2: string, maxDistance?: number): boolean {
  if (!w1 || !w2) return false;
  const f1 = foldTurkish(w1).trim();
  const f2 = foldTurkish(w2).trim();
  if (f1 === f2) return true;

  const minL = Math.min(f1.length, f2.length);
  const maxL = Math.max(f1.length, f2.length);

  // Çok kısa kelimelerde (3 harf altı) bulanık eşleşme gürültü yaratır
  if (minL < 3) return false;

  // 3-4 harfli kelimelerde en fazla 1 fark ve boy farkı <= 1
  if (minL <= 4) {
    if (maxL - minL > 1) return false;
    return damerauLevenshtein(f1, f2, 1) <= 1;
  }

  // Türkçe çekim eki / gövde eşleşmesi (örn: "sendrom" ve "sendromu", "paratiroid" ve "paratiroidi")
  // Yalnızca kelimelerden biri DİĞERİNİN tam bir uzantısı ise ve fark <= 3 harf ise geçerli sayılır.
  if (minL >= 5 && (f1.startsWith(f2) || f2.startsWith(f1)) && (maxL - minL <= 3)) {
    return true;
  }

  // Tolerans hesabı: uzun kelimelerde (>= 8) en fazla 2, orta boyda (5-7) 1 harf farkı/yer değiştirmesi
  const allowed = maxDistance !== undefined ? maxDistance : minL >= 8 ? 2 : 1;
  if (maxL - minL > allowed) return false;

  // Harf yer değiştirmesi veya eksikliği varsa Damerau-Levenshtein hesapla
  // Hızlı ön filtre: İlk 2 harften en az biri örtüşmeli
  if (f1[0] !== f2[0] && f1[1] !== f2[0] && f1[0] !== f2[1]) {
    return false;
  }

  const dist = damerauLevenshtein(f1, f2, allowed);
  return dist <= allowed;
}

/**
 * Hızlı Kelime Haznesi İndeksi (Fast Fuzzy Vocabulary):
 * On binlerce tıbbi terim ve indeks token'ı arasında mikrosaniye hızında
 * harf eksikliği ve yer değiştirmesi arar.
 */
export class FastFuzzyVocab {
  private buckets = new Map<number, string[]>();
  private allTerms = new Set<string>();
  private cache = new Map<string, Array<{ term: string; dist: number }>>();

  public clear(): void {
    this.buckets.clear();
    this.allTerms.clear();
    this.cache.clear();
  }

  public add(rawWord: string): void {
    const w = foldTurkish(rawWord).trim();
    if (w.length < 3 || this.allTerms.has(w)) return;
    this.allTerms.add(w);

    const len = w.length;
    let b = this.buckets.get(len);
    if (!b) {
      b = [];
      this.buckets.set(len, b);
    }
    b.push(w);
  }

  public size(): number {
    return this.allTerms.size;
  }

  /**
   * Sorgulanan kelime için en yakın eşleşmeleri döner (dist <= maxDist).
   */
  public findMatches(query: string, maxDist = 2): Array<{ term: string; dist: number }> {
    const q = foldTurkish(query).trim();
    const ql = q.length;
    if (ql < 3) return [];

    const cached = this.cache.get(q);
    if (cached) return cached;

    const allowed = ql >= 6 ? maxDist : Math.min(1, maxDist);
    const results: Array<{ term: string; dist: number }> = [];
    const q0 = q[0];
    const q1 = q[1];

    for (let l = Math.max(3, ql - allowed); l <= ql + allowed; l++) {
      const list = this.buckets.get(l);
      if (!list) continue;

      for (let i = 0; i < list.length; i++) {
        const w = list[i];
        // Ön filtre: İlk harf eşleşmeli veya ilk iki harf yer değiştirmiş olmalı
        if (w[0] !== q0 && !(w[0] === q1 && w[1] === q0)) continue;

        const dist = damerauLevenshtein(q, w, allowed);
        if (dist <= allowed) {
          results.push({ term: w, dist });
        }
      }
    }

    const sorted = results.sort((a, b) => a.dist - b.dist);
    if (this.cache.size < 5000) {
      this.cache.set(q, sorted);
    }
    return sorted;
  }
}

/**
 * Verilen metin veya soru parçalarından bağlam / konu etiketi (#DownSendromu gibi) üretir.
 */
export function toContextHashtag(conceptOrTopic: string): string {
  if (!conceptOrTopic) return '';
  // Türkçe özel karakterleri koruyarak CamelCase hashtag formatına çevir
  const clean = conceptOrTopic
    .replace(/\(.*?\)/g, '')
    .replace(/[–—\-–]/g, ' ')
    .replace(/[^a-zA-Z0-9ğüşıöçĞÜŞİÖÇ\s]/g, '')
    .trim();

  const words = clean.split(/\s+/).filter(Boolean);
  if (words.length === 0) return '';

  const camel = words
    .map((w) => w.charAt(0).toLocaleUpperCase('tr-TR') + w.slice(1).toLocaleLowerCase('tr-TR'))
    .join('');

  return `#${camel}`;
}
