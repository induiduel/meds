/**
 * İstemci tarafı metin arama: Türkçe büyük/küçük harf ve karakter katlama (ç→c, ğ→g, ı/İ→i …),
 * tırnaklı ifade, "-kelime" ile hariç tutma ve alan ağırlıklı puanlama.
 * Katlama karakter başına 1:1 yapılır; böylece bulunan konum özgün metinde de aynı konumdur (vurgulama için).
 */

const FOLD: Record<string, string> = {
  ç: 'c', Ç: 'c', ğ: 'g', Ğ: 'g', ı: 'i', I: 'i', İ: 'i', ö: 'o', Ö: 'o', ş: 's', Ş: 's', ü: 'u', Ü: 'u',
  â: 'a', Â: 'a', î: 'i', Î: 'i', û: 'u', Û: 'u', é: 'e', É: 'e', ä: 'a', ë: 'e',
};

export function foldText(s: string): string {
  let out = '';
  for (const ch of s) {
    const f = FOLD[ch];
    if (f) { out += f; continue; }
    const lower = ch.toLowerCase();
    out += lower.length === ch.length ? lower : ch;
  }
  return out;
}

export interface ParsedQuery {
  /** Hepsi geçmeli (katlanmış) */
  terms: string[];
  /** Hiçbiri geçmemeli */
  excluded: string[];
  /** "#123": soru numarası */
  number: number | null;
  raw: string;
}

export function parseQuery(raw: string): ParsedQuery {
  const terms: string[] = [];
  const excluded: string[] = [];
  let number: number | null = null;
  const re = /(-?)"([^"]+)"|(\S+)/g;
  let m: RegExpExecArray | null;
  while ((m = re.exec(raw))) {
    const neg = m[1] === '-' || (m[3] || '').startsWith('-');
    let t = m[2] ?? m[3] ?? '';
    if (!m[2] && t.startsWith('-')) t = t.slice(1);
    const f = foldText(t).trim();
    if (!f) continue;
    if (!neg && /^#\d{1,3}$/.test(f) && number === null) {
      number = parseInt(f.replace('#', ''), 10);
      continue;
    }
    // Tek harf ya da noktalama tek başına aramayı bozmasın
    if (f.length < 2 && !m[2]) continue;
    (neg ? excluded : terms).push(f);
  }
  return { terms, excluded, number, raw };
}

export interface SearchField {
  text: string;
  weight: number;
}

/**
 * Alanlarda puanla. Her terim en az bir alanda geçmezse 0 döner.
 * Kelime başında eşleşme ve tam kelime eşleşmesi ek puan alır.
 */
export function scoreFields(foldedFields: SearchField[], q: ParsedQuery): number {
  if (!q.terms.length && !q.excluded.length) return 1;
  for (const ex of q.excluded) if (foldedFields.some((f) => f.text.includes(ex))) return 0;
  let score = 0;
  for (const t of q.terms) {
    let best = 0;
    for (const f of foldedFields) {
      const i = f.text.indexOf(t);
      if (i < 0) continue;
      const startsWord = i === 0 || /[^a-z0-9]/.test(f.text[i - 1]);
      const endsWord = i + t.length >= f.text.length || /[^a-z0-9]/.test(f.text[i + t.length]);
      const s = f.weight * (1 + (startsWord ? 0.6 : 0) + (startsWord && endsWord ? 0.4 : 0));
      if (s > best) best = s;
    }
    if (best === 0) return 0;
    score += best;
  }
  return score;
}

/** Metni arama terimlerine göre parçalar: vurgulanacak parçalar `hit: true`. */
export function splitHighlights(text: string, terms: string[]): { t: string; hit: boolean }[] {
  if (!text || !terms.length) return [{ t: text, hit: false }];
  const folded = foldText(text);
  const marks = new Uint8Array(text.length);
  let any = false;
  for (const term of terms) {
    if (!term) continue;
    let from = 0;
    while (from <= folded.length) {
      const i = folded.indexOf(term, from);
      if (i < 0) break;
      marks.fill(1, i, i + term.length);
      any = true;
      from = i + Math.max(1, term.length);
    }
  }
  if (!any) return [{ t: text, hit: false }];
  const out: { t: string; hit: boolean }[] = [];
  let start = 0;
  for (let i = 1; i <= text.length; i++) {
    if (i === text.length || marks[i] !== marks[start]) {
      out.push({ t: text.slice(start, i), hit: marks[start] === 1 });
      start = i;
    }
  }
  return out;
}
