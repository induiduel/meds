/**
 * Ders özeti markdown'ındaki slayt artıklarını okunur yapıya çevirir.
 * - Tek satıra sıkışmış "1. … 2. …", "✔ … ✔ …", "■ / • / ❑ …" listelerini ayrı maddelere böler.
 * - Art arda aynı konu önekiyle başlayan maddeleri ("Temas İzolasyonu …") tek başlık altında toplar.
 * - "kimlere uygulanır?:" gibi alt maddesi olan satırları etiket (alt başlık) yapar.
 * - "Sefoksitin 4x2 gr + Doksisiklin 2x100 mg → …" gibi tedavi rejimlerini seçenek / ilaç / doz olarak ayırır.
 * Yalnızca biçim değişir; metin içeriği silinmez ya da uydurulmaz.
 */

export type InlineListKind = 'steps' | 'checks' | 'bullets';

export interface RichItem {
  /** Kısa başlık: "Kimlere uygulanır?", "Kuralları" */
  label?: string;
  text: string;
  list?: { kind: InlineListKind; items: string[] };
  /** Tedavi rejimleri: her biri ayrı seçenek */
  regimens?: RegimenBlock;
  children: RichItem[];
}

export interface RegimenDrug {
  name: string;
  /** IV, IM, PO … */
  route?: string;
  /** "veya" ile ayrılmış doz seçenekleri: ["3x400 mg", "2x800 mg, 5 gün"] */
  doses: string[];
}

export interface Regimen {
  /** Rejimin geçerli olduğu durum: "meningoensefalit" */
  condition?: string;
  drugs: RegimenDrug[];
  /** "→" sonrası: "klinik bulguların düzelmesinden 24-48 saat sonra …" */
  then?: string;
  /** Dozlardan sonra gelen açıklama */
  note?: string;
}

export interface RegimenBlock {
  /** İlk ilaçtan önceki metin */
  lead?: string;
  items: Regimen[];
  /** Son rejimden sonra gelen başlık: "Tekrarlayan ataklarda tedavi" */
  after?: string;
}

export interface RichGroup {
  /** Ortak konu öneki ("Temas İzolasyonu"); yoksa başlıksız grup */
  title?: string;
  items: RichItem[];
}

const UPPER_START = /^[A-ZÇĞİÖŞÜ]/;
const CHECK_MARK = /[✔✓]/g;
const BULLET_MARK = /[❑■•⮚►●▪➢◦⚫]/g;

const upperFirst = (s: string) => s.replace(/^\p{Ll}/u, (c) => c.toLocaleUpperCase('tr'));
const fold = (s: string) => s.toLocaleLowerCase('tr').replace(/\s+/g, ' ').trim();

/** Slayt çıkarımından kalan bozuklukları temizler (biçim düzeyinde). */
export const cleanSummaryText = (s: string): string =>
  s
    .replace(/\*\*/g, '')
    // "İ" küçültülünce oluşan "i + birleşen nokta"
    .replace(/i̇/g, 'i')
    .replace(/\s+/g, ' ')
    .replace(/^Slayt\s+\d+\s*[–-]\s*/i, '')
    .replace(/\s*\.\s*:+/g, ':')
    .replace(/\?\s*:+/g, '?')
    .replace(/:{2,}/g, ':')
    .replace(/\s+([:?])/g, '$1')
    .trim();

const stripEdgePunct = (s: string) => s.replace(/^[\s,;:–-]+/, '').replace(/[\s,;:]+$/, '').trim();

/** "1. a 2. b 3. c" zincirini bulur; 1'den başlayan ve en az iki ardışık numara şart. */
const splitNumbered = (text: string): { lead: string; items: string[] } | null => {
  const re = /(^|[\s(])(\d{1,2})[.)]\s+(?=\S)/g;
  const hits: { n: number; start: number; end: number }[] = [];
  let m: RegExpExecArray | null;
  while ((m = re.exec(text))) {
    hits.push({ n: Number(m[2]), start: m.index + m[1].length, end: re.lastIndex });
  }
  const firstIdx = hits.findIndex((h) => h.n === 1);
  if (firstIdx < 0) return null;
  const chain = [hits[firstIdx]];
  for (let i = firstIdx + 1; i < hits.length; i++) {
    if (hits[i].n === chain[chain.length - 1].n + 1) chain.push(hits[i]);
  }
  if (chain.length < 2) return null;
  const items = chain
    .map((h, i) => text.slice(h.end, i + 1 < chain.length ? chain[i + 1].start : undefined))
    .map(stripEdgePunct)
    .filter(Boolean);
  if (items.length < 2) return null;
  return { lead: stripEdgePunct(text.slice(0, chain[0].start)), items };
};

const splitBySymbol = (text: string, mark: RegExp): { lead: string; items: string[] } | null => {
  const parts = text.split(mark);
  if (parts.length < 2) return null;
  const lead = stripEdgePunct(parts[0]);
  const items = parts.slice(1).map(stripEdgePunct).filter(Boolean);
  if (items.length === 0) return null;
  // Tek işaretli ve öncesi boş satır liste değildir; işaret düşürülür (çağıran halleder)
  if (items.length === 1 && !lead) return null;
  return { lead, items };
};

/** Satır içine sıkışmış listeyi ayırır; liste yoksa null. */
export const splitInlineList = (
  text: string
): { lead: string; kind: InlineListKind; items: string[] } | null => {
  const checks = splitBySymbol(text, CHECK_MARK);
  if (checks) return { ...checks, kind: 'checks' };
  const steps = splitNumbered(text);
  if (steps) return { ...steps, kind: 'steps' };
  const bullets = splitBySymbol(text, BULLET_MARK);
  if (bullets) return { ...bullets, kind: 'bullets' };
  return null;
};

// ---------------------------------------------------------------------------
// Tedavi rejimleri
// ---------------------------------------------------------------------------
const DOSE_SRC = String.raw`\d+(?:[.,]\d+)?(?:\s?x\s?\d+(?:[.,]\d+)?)?\s?(?:mg|gr|g|mcg|µg|μg|IU|ünite|MU|milyon ünite)(?:\/kg)?(?![a-zçğıöşü/])`;
const ROUTE_SRC = String.raw`(?:IV|İV|IM|İM|PO|oral|intravenöz|intramüsküler)`;
/** İlaç adı + (yol) + doz; ad, dozdan hemen önce gelmeli */
const DRUG_START = new RegExp(String.raw`([A-Za-zÇĞİÖŞÜçğıöşü][A-Za-zÇĞİÖŞÜçğıöşü/-]{2,})(?:\s+(${ROUTE_SRC}))?\s+(?=${DOSE_SRC})`, 'g');
const NOT_DRUG = new Set(['veya', 'ile', 've', 'toplam', 'günde', 'haftada', 'doz', 'dozu', 'yükleme', 'idame', 'sonra', 'önce', 'maksimum', 'max', 'en', 'az', 'fazla', 'her', 'gün', 'tek', 'ilk', 'olarak', 'kez', 'total']);
/** İlaç adına benzeyen sonlar; "Erkeklerde", "Nedenle", "Düzeyinin" gibi kelimeleri eler */
const DRUG_END = /(?:sin|sın|lin|tin|kson|zol|zon|vir|tam|mid|sid|pam|lam|lon|son|fen|nat|pril|olol|tan|din|zin|rin|cin|in|it|at|ol|il|id|on|ast|im|um|ab|ib|ksim)$/i;
const NOT_DRUG_END = /(?:nin|nın|nun|nün|için|icin)$/i;
const isDrugName = (w: string) => {
  const f = w.toLocaleLowerCase('tr');
  return w.length >= 4 && !NOT_DRUG.has(f) && DRUG_END.test(f) && !NOT_DRUG_END.test(f);
};
/** Rejim metni işareti: "2x100", "+", "→" ya da süre */
const REGIMEN_SIGNAL = /\d\s?x\s?\d|\+|→|\d\s?(?:gün|hafta)|tek doz/i;
const DURATION = /(\d+(?:\s?[-–]\s?\d+)?\s?(?:gün|hafta|ay)|tek doz)/gi;
const MARK_EDGE = /^[\s◦•■❑▪⚫,;.]+|[\s◦•■❑▪⚫,;]+$/g;
/** Dozdan sonra süre (ve parantez) gelir; ardındaki uzun metin dozun değil rejimin notudur */
const DOSE_THEN_NOTE = /^(.*?(?:\d+(?:\s?[-–]\s?\d+)?\s?(?:gün|hafta|ay)|tek doz)(?:\s*\([^)]*\))?)\s+(\p{L}.{8,})$/iu;

/** Metindeki son süre ifadesinin bitiş konumu ("7-10 gün", "tek doz"); yoksa -1 */
const lastDurationEnd = (t: string) => {
  let end = -1;
  for (const m of t.matchAll(DURATION)) end = (m.index ?? 0) + m[0].length;
  return end;
};

const parseDrug = (part: string): RegimenDrug | null => {
  const m = part.match(new RegExp(String.raw`^([A-Za-zÇĞİÖŞÜçğıöşü][A-Za-zÇĞİÖŞÜçğıöşü/-]{2,})(?:\s+(${ROUTE_SRC}))?\s+(.+)$`));
  if (!m || !new RegExp('^' + DOSE_SRC).test(m[3])) return null;
  const doses = m[3].split(/\s+veya\s+(?=\d)/).map((d) => d.replace(MARK_EDGE, '').replace(/\.$/, '').trim()).filter(Boolean);
  return { name: upperFirst(m[1]), route: m[2]?.toLocaleUpperCase('tr'), doses };
};

/** En az iki ilaç-doz kalıbı varsa metni rejimlere böler; yoksa null. */
export const splitRegimens = (text: string): RegimenBlock | null => {
  const starts: number[] = [];
  for (const m of text.matchAll(DRUG_START)) {
    if (!isDrugName(m[1])) continue;
    const at = m.index ?? 0;
    // "+" ile bağlanan ilaç aynı rejimin parçasıdır
    if (/\+\s*$/.test(text.slice(0, at))) continue;
    starts.push(at);
  }
  // Tek ilaçlı satır da rejimdir ("Seftriakson 1x250 mg, tek doz + …"); işaret şart
  if (starts.length === 0 || !REGIMEN_SIGNAL.test(text)) return null;

  const lead = text.slice(0, starts[0]).replace(MARK_EDGE, '').replace(/:$/, '').trim();
  const items: Regimen[] = [];
  let after: string | undefined;
  let carry: string | undefined;

  for (let i = 0; i < starts.length; i++) {
    let seg = text.slice(starts[i], starts[i + 1]).replace(MARK_EDGE, '').trim();
    const condition = carry;
    carry = undefined;
    // "… 7-10 gün meningoensefalit →" : süre sonrası metin bir sonraki rejimin durumu
    if (/→\s*$/.test(seg)) {
      seg = seg.replace(/\s*→\s*$/, '');
      const end = lastDurationEnd(seg);
      if (end > 0 && seg.length - end < 60) {
        carry = seg.slice(end).replace(MARK_EDGE, '').trim() || undefined;
        seg = seg.slice(0, end);
      }
    }
    // Son rejimden sonra gelen "… tedavi:" başlığı
    if (i === starts.length - 1 && /:$/.test(seg)) {
      const end = lastDurationEnd(seg);
      if (end > 0) {
        after = upperFirst(seg.slice(end).replace(MARK_EDGE, '').replace(/:$/, '').trim()) || undefined;
        seg = seg.slice(0, end);
      }
    }
    // Satır içi madde işaretinden sonrası ayrı bir nottur ("… 2x1 ⚫ TMP/SMZ …")
    let note: string | undefined;
    const mark = seg.search(/\s[◦•■❑▪⚫]\s/);
    if (mark > 0) {
      note = seg.slice(mark).replace(MARK_EDGE, '').trim() || undefined;
      seg = seg.slice(0, mark);
    }
    const arrow = seg.search(/\s*→\s*/);
    const main = arrow >= 0 ? seg.slice(0, arrow) : seg;
    const then = arrow >= 0 ? seg.slice(arrow).replace(/^\s*→\s*/, '').replace(/[.\s]+$/, '').trim() : undefined;
    const drugs = main.split(/\s*\+\s*/).map(parseDrug);
    if (drugs.some((d) => !d)) return null;
    for (const d of drugs as RegimenDrug[]) {
      const last = d.doses.length - 1;
      const m = d.doses[last].match(DOSE_THEN_NOTE);
      if (m) {
        d.doses[last] = m[1].trim();
        note = [m[2].replace(/[.\s]+$/, ''), note].filter(Boolean).join(' · ');
      }
    }
    items.push({
      condition: condition ? upperFirst(condition) : undefined,
      drugs: drugs as RegimenDrug[],
      then: then ? upperFirst(then) : undefined,
      note: note ? upperFirst(note.replace(/[.\s]+$/, '')) : undefined,
    });
  }
  return { lead: lead ? upperFirst(lead) : undefined, items, after };
};

const toItem = (raw: string, children: RichItem[] = []): RichItem => {
  let text = cleanSummaryText(raw);
  const regimens = splitRegimens(text);
  if (regimens) {
    return { label: regimens.lead, text: '', regimens: { ...regimens, lead: undefined }, children };
  }
  const split = splitInlineList(text);
  if (split) {
    return { label: split.lead ? upperFirst(split.lead) : undefined, text: '', list: { kind: split.kind, items: split.items.map(upperFirst) }, children };
  }
  text = text.replace(/^[✔✓❑■•⮚►●▪➢]\s*/, '').replace(/:$/, '').trim();
  if (children.length > 0 && text.length <= 120) {
    return { label: upperFirst(text), text: '', children };
  }
  // "Anahtar: açıklama" (anahtar kısa ve en çok beş kelime)
  const kv = text.match(/^([^:]{3,48}):\s+(.+)$/);
  if (kv && kv[1].split(' ').length <= 5 && !/\d$/.test(kv[1])) {
    return { label: kv[1].trim(), text: upperFirst(kv[2].trim()), children };
  }
  return { text: upperFirst(text), children };
};

/** Alt madde, üst maddenin aynı türdeki listesinin devamıysa ("❑a ❑b" iki satıra bölünmüş) birleştirir. */
const mergeContinuedLists = (item: RichItem): RichItem => {
  if (!item.list) return item;
  const rest: RichItem[] = [];
  for (const child of item.children) {
    if (child.list && child.list.kind === item.list.kind && !child.label && !child.text && child.children.length === 0) {
      item.list.items.push(...child.list.items);
    } else if (!child.list && !child.label && child.children.length === 0 && item.list.kind === 'bullets' && /^[❑■•]/.test(child.text)) {
      item.list.items.push(child.text.replace(/^[❑■•]\s*/, ''));
    } else {
      rest.push(child);
    }
  }
  item.children = rest;
  return item;
};

const isBareRegimen = (it: RichItem) => !!it.regimens && !it.label && !it.text && it.children.length === 0;
const STEP_LINE = /^(\d{1,2})[.)]\s+(.+)$/;

/**
 * Kaynaktan satır satır gelen kardeş maddeleri birleştirir:
 * ardışık rejim satırları → tek seçenek listesi; "1. …", "2. …" satırları → numaralı adımlar.
 */
export const mergeSiblings = (items: RichItem[]): RichItem[] => {
  // 1) "◦ …" alt bilgisi bir önceki maddenin altına
  const nested: RichItem[] = [];
  for (const raw of items) {
    const it = raw.children.length ? { ...raw, children: mergeSiblings(raw.children) } : raw;
    const prev = nested[nested.length - 1];
    if (prev && !it.label && !it.list && !it.regimens && /^[◦▪○]/.test(it.text)) {
      prev.children = [...prev.children, { ...it, text: upperFirst(it.text.replace(/^[◦▪○]\s*/, '')) }];
      continue;
    }
    nested.push({ ...it });
  }
  // 2) Ardışık rejimler tek seçenek listesi; alt maddesiz "1. …", "2. …" satırları numaralı adımlar
  const out: RichItem[] = [];
  for (const it of nested) {
    const prev = out[out.length - 1];
    if (prev && prev.regimens && isBareRegimen(it) && !prev.regimens.after) {
      prev.regimens.items.push(...it.regimens!.items);
      prev.regimens.after = it.regimens!.after;
      continue;
    }
    const step = !it.list && !it.regimens && !it.label && it.children.length === 0 ? it.text.match(STEP_LINE) : null;
    if (step) {
      const n = Number(step[1]);
      if (prev && prev.list?.kind === 'steps' && !prev.label && !prev.text && prev.list.items.length === n - 1) {
        prev.list.items.push(upperFirst(step[2]));
        continue;
      }
      if (n === 1) {
        out.push({ text: '', list: { kind: 'steps', items: [upperFirst(step[2])] }, children: [] });
        continue;
      }
    }
    out.push(it.regimens ? { ...it, regimens: { ...it.regimens, items: [...it.regimens.items] } } : it);
  }
  // Tek maddelik "1." adım listesi liste değildir
  return out.map((it) => (it.list?.kind === 'steps' && it.list.items.length === 1 && !it.label && !it.text ? { text: `1. ${it.list.items[0]}`, children: [] } : it));
};

/** Başta büyük harfle başlayan en çok altı kelime: "Temas İzolasyonu", "Standart Önlemler". */
const titlePrefix = (text: string): string[] => {
  const out: string[] = [];
  for (const w of text.split(' ')) {
    if (out.length >= 6 || !UPPER_START.test(w) || w.includes('://')) break;
    const bare = w.replace(/[:.,;?–-]+$/, '');
    // OCR'da harfleri ayrılmış kelimeler ("YA Ş L I") başlık olmaz
    if (bare.length < 2) break;
    out.push(bare);
    if (bare !== w) break;
  }
  return out;
};

const groupKey = (text: string): string | null => {
  const words = titlePrefix(text).slice(0, 2);
  if (words.length === 0) return null;
  if (words.length === 1 && words[0].length < 6) return null;
  return words.join(' ');
};

/** Grup başlığını maddeden atar; "Temas İzolasyonu temas izolasyonu kimlere…" → "Kimlere…" */
const stripTitle = (text: string, title: string): string => {
  let rest = text.slice(title.length).trim();
  if (fold(rest).startsWith(fold(title))) rest = rest.slice(title.length).trim();
  rest = rest.replace(/^[:,;–-]\s*/, '');
  return rest ? upperFirst(rest) : text;
};

interface RawNode {
  text: string;
  children: string[];
}

const parseLines = (md: string): RawNode[] => {
  const nodes: RawNode[] = [];
  for (const line of md.split('\n')) {
    if (!line.trim() || /^\s*#/.test(line)) continue;
    const bullet = line.match(/^(\s*)[-*]\s+(.*)$/);
    if (bullet) {
      const indent = bullet[1].replace(/\t/g, '  ').length;
      if (indent >= 2 && nodes.length > 0) nodes[nodes.length - 1].children.push(bullet[2]);
      else nodes.push({ text: bullet[2], children: [] });
      continue;
    }
    // Sarmalanmış satır: önceki maddeye eklenir
    const last = nodes[nodes.length - 1];
    if (last) {
      if (last.children.length > 0) last.children[last.children.length - 1] += ' ' + line.trim();
      else last.text += ' ' + line.trim();
    } else {
      nodes.push({ text: line.trim(), children: [] });
    }
  }
  return nodes;
};

/** Madde listesi markdown'ını gruplanmış, ayrıştırılmış maddelere çevirir. */
export const structureBulletBlock = (md: string): RichGroup[] => {
  const nodes = parseLines(md);
  const cleaned = nodes.map((n) => cleanSummaryText(n.text));
  const keys = cleaned.map(groupKey);

  const groups: RichGroup[] = [];
  let i = 0;
  while (i < nodes.length) {
    const key = keys[i];
    let j = i + 1;
    if (key) while (j < nodes.length && keys[j] && fold(keys[j]!) === fold(key)) j++;
    const runLen = key ? j - i : 1;

    const build = (k: number, title?: string): RichItem[] => {
      const children = nodes[k].children.map((c) => mergeContinuedLists(toItem(c)));
      // Başlıkla aynı satır ("Standart Önlemler") kart başlığında zaten var: alt maddeleri karta çıkar
      if (title && children.length > 0 && fold(cleaned[k]).replace(/[:.]$/, '') === fold(title)) return children;
      return [mergeContinuedLists(toItem(title ? stripTitle(cleaned[k], title) : cleaned[k], children))];
    };

    if (key && runLen >= 2) {
      // Tüm maddelerde ortak olan en uzun önek: "Sistemik Lupus" → "Sistemik Lupus Eritematozus"
      const prefixes = cleaned.slice(i, j).map(titlePrefix);
      let n = key.split(' ').length;
      while (n < prefixes[0].length && prefixes.every((p) => p.length > n && fold(p[n]) === fold(prefixes[0][n]))) n++;
      const title = prefixes[0].slice(0, n).join(' ');
      groups.push({ title, items: mergeSiblings(nodes.slice(i, j).flatMap((_, off) => build(i + off, title))) });
      i = j;
    } else {
      const built = build(i);
      const last = groups[groups.length - 1];
      if (last && !last.title) last.items.push(...built);
      else groups.push({ items: built });
      i += 1;
    }
  }
  for (const g of groups) if (!g.title) g.items = mergeSiblings(g.items);
  return groups;
};

/** Yapay şablon alt başlıkları (her bölümde aynı, içerikle ilgisiz) */
export const isBoilerplateSubheading = (title: string) =>
  /^[A-Z]\.\s+(Temel Kavramlar ve Patofizyolojik Mekanizmalar|Klinik Özellikler, Tanı ve Yaklaşım İlkeleri|Ayrıntılı Değerlendirme ve Kritik Noktalar)\s*$/.test(
    title.trim()
  );

/** Bölüm başlığıyla madde metnini karşılaştırmak için */
export const foldForCompare = (s: string) =>
  fold(cleanSummaryText(s))
    .replace(/[^\p{L}\p{N} ]/gu, '')
    .replace(/\s+/g, ' ')
    .trim();
