import type { SearchDocType, SearchHit } from './searchShared';

/**
 * Arama dizinindeki düz metin kayıtlarını (ör. "[DEEPSEEK DOĞRULANMIŞ TIP SORUSU]\nDers / Branş: …\nSoru Kökü: …")
 * öğrencinin okuyacağı yapıya çevirir: üst bilgi haplara, soru kök/şık/cevap/açıklamaya,
 * hastalık ve sözlük kayıtları başlıklı madde listelerine, slayt/özet metni Markdown'a.
 * Dizin metni değişmez; yalnız gösterim için ayrıştırılır.
 */

export interface QuestionPart {
  stem: string;
  options: { key: string; text: string }[];
  answer?: string;
  /** Açıklama (Markdown) */
  explanation: string;
}

export interface FormattedHit {
  title: string;
  /** Başlık altı kısa satır (İngilizce ad, diğer adlar …) */
  subtitle?: string;
  /** Küçük üst bilgi hapları: kurul, yıl, zorluk, ICD … */
  tags: string[];
  /** Ayrı satırda gösterilecek bağlam (kazanım) */
  context?: string;
  /** Kısa vurgu maddeleri (hastalığın karakteristik özellikleri) */
  keyPoints: string[];
  question?: QuestionPart;
  /** Gövde (Markdown — NoteMarkdown ile çizilir) */
  body: string;
  /** Kapalı kartta gösterilecek düz metin önizleme */
  preview: string;
}

const QUESTION_TYPES = new Set<SearchDocType>(['past_question', 'deepseek_contribution', 'active_question', 'ornek_question', 'user_contribution', 'gemini_v3_question']);

/** Gösterilmeyecek iç alanlar (tür, kaynak, kimlik …) */
const DROP_KEYS = new Set([
  'ders / branş', 'ders', 'konu', 'konu / başlık', 'soru no', 'deste', 'kaynak', 'bölüm', 'terim', 'türkçe', 'hastalık',
  'özet metin', 'içerik',
]);

/** Veri tabanında içi boş kalıp cümleler (bilgi taşımaz) */
const BOILERPLATE = [
  /konusunun temel kavramlarını, etiyolojisini ve patofizyolojik mekanizmalarını açıklar/i,
  /için altta yatan tetikleyici genetik ve çevresel faktörler incelenmektedir/i,
  /tablosuna özgü akut veya kronik klinik semptomlar/i,
  /ayırıcı tanısında klinik ve laboratuvar bulguları belirleyicidir/i,
  /mekanizması ve klinik özellikleri ders müfredatı kapsamında ele alınmıştır/i,
  /^standart medikal protokol/i,
  /^laboratuvar incelemeleri ve klinik patolojik değerlendirme$/i,
];
const isBoilerplate = (v: string) => BOILERPLATE.some((re) => re.test(v.trim()));
/** "a,Başka Alan: b" gibi yapışık değerleri ayırır, kalıp parçaları atar */
const keepUseful = (v: string) => v.split(/,(?=[A-ZÇĞİÖŞÜ])/).map((x) => x.trim()).filter((x) => x && !isBoilerplate(x)).join('. ');

const KEY_LINE = /^([A-ZÇĞİÖŞÜ][\p{L}0-9 /&().-]{1,48}?)\s*:\s*(.*)$/u;

export function formatKurul(v: string): string {
  const m = v.match(/donem\s*(\d+)\s*-?\s*kurul\s*(\d+)/i);
  if (m) return `Dönem ${m[1]} · Kurul ${m[2]}`;
  const k = v.match(/kurul[-\s]*(\d+)/i);
  return k ? `Kurul ${k[1]}` : v;
}

const yearTag = (v: string) => (/arşiv/i.test(v) ? 'Arşiv' : v.replace(/\s*\(.*\)\s*$/, '').trim());

/** "> [!IMPORTANT]" kutuları, "📌 [SINAV SPOTU]" satırları, HTML parçaları ve etkileşim artıkları */
function cleanMarkdown(md: string): string {
  const lines = md.replace(/\r/g, '').split('\n');
  const out: string[] = [];
  for (let i = 0; i < lines.length; i++) {
    const t = lines[i].trim();
    const call = t.match(/^>\s*\[!(\w+)\]\s*(.*)$/);
    if (call) {
      const exam = /important|warning|caution|tip/i.test(call[1]);
      const body: string[] = call[2] ? [call[2]] : [];
      while (i + 1 < lines.length && lines[i + 1].trim().startsWith('>')) body.push(lines[++i].trim().replace(/^>\s?/, ''));
      const plain = body.filter(Boolean).map((l) => l.replace(/[📌⚡✅❗️]\s*/gu, ''));
      if (plain.length === 1 && !/^[-*]\s/.test(plain[0])) out.push(`${exam ? 'Sınav' : 'Not'}: ${plain[0]}`);
      else { out.push(`### ${exam ? 'Sınav spotları' : 'Not'}`); out.push(...plain); }
      out.push('');
      continue;
    }
    const spot = t.match(/^📌?\s*\[SINAV SPOTU\]\s*(.*)$/i);
    if (spot) { out.push(`Sınav: ${spot[1]}`); continue; }
    // Öğren destesindeki etkileşim türü listesi ve JSON artıkları
    if (/^[a-z_]+(?:\s*,\s*[a-z_]+)*$/.test(t) && t.includes('_')) continue;
    if (/^\{.*\}$/.test(t)) continue;
    out.push(lines[i].replace(/<\/?(sub|sup|br|b|i|u|span)[^>]*>/gi, '').replace(/[📌⚡]\s*/gu, ''));
  }
  return out.join('\n').replace(/\n{3,}/g, '\n\n').trim();
}

/** Markdown işaretlerinden arındırılmış düz metin (önizleme için) */
export function plainText(md: string): string {
  return md
    .replace(/^#{1,4}\s+/gm, '')
    .replace(/^\s*[-*]\s+/gm, '• ')
    .replace(/^\s*>\s?/gm, '')
    .replace(/^(Sınav|Not):\s*/gm, '')
    .replace(/\*\*|==|__/g, '')
    .replace(/\|/g, ' ')
    .replace(/-{3,}/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
    .replace(/^•\s*/, '');
}

const fold = (s: string) =>
  s.replace(/İ/g, 'i').replace(/I/g, 'ı').toLocaleLowerCase('tr')
    .replace(/[âà]/g, 'a').replace(/[îı]/g, 'i').replace(/[ûü]/g, 'u').replace(/ö/g, 'o').replace(/ç/g, 'c').replace(/ş/g, 's').replace(/ğ/g, 'g');

/** Sorgunun ilk geçtiği yer çevresinde kısa pencere; eşleşme yoksa baştan */
export function windowAround(text: string, query: string, size = 260): string {
  if (text.length <= size) return text;
  const stems = fold(query).split(/[^a-z0-9]+/).filter((w) => w.length >= 3).map((w) => w.slice(0, w.length >= 8 ? 7 : 5));
  const f = fold(text);
  let at = -1;
  for (const st of stems) {
    const re = new RegExp(`(^|[^a-z0-9])${st}`);
    const m = re.exec(f);
    if (m && (at < 0 || m.index < at)) at = m.index + m[1].length;
  }
  if (at < 0 || at < size * 0.5) return text.slice(0, size).replace(/\s+\S*$/, '') + '…';
  let start = Math.max(0, at - 60);
  const sp = text.lastIndexOf(' ', start);
  if (sp > 0 && start - sp < 20) start = sp + 1;
  const end = Math.min(text.length, start + size);
  return (start > 0 ? '…' : '') + text.slice(start, end).replace(/\s+\S*$/, '') + (end < text.length ? '…' : '');
}

const matches = (text: string, query: string) => {
  const f = fold(text);
  return fold(query).split(/[^a-z0-9]+/).filter((w) => w.length >= 3).some((w) => f.includes(w.slice(0, w.length >= 8 ? 7 : 5)));
};

function cleanTitle(hit: SearchHit): string {
  let t = hit.title || '';
  t = t.replace(/^(Hastalık|Sözlük|Örnek Soru)\s*:\s*/i, '');
  t = t.replace(/\s*\((?:Soru\s*\??|Soru\s+\d+)\)\s*$/i, '');
  t = t.replace(/\s*\((?:[^()]*\([^()]*\))*[^()]*(?:Çıkmış|Arşiv|Sınav)[^()]*(?:\([^()]*\))*[^()]*\)\s*$/i, '');
  t = t.replace(/\s*\(Özet\s*#\d+\)\s*$/i, '').replace(/\s*\(Sayfa\s*\d+\)\s*$/i, '');
  // TAMAMI BÜYÜK HARF başlıklar okunaklı yazıma çevrilir (kısaltmalar tek sözcük olduğundan dokunulmaz)
  if (t.split(/\s+/).length >= 3 && t === t.toLocaleUpperCase('tr') && /\p{Lu}{4}/u.test(t)) {
    const low = t.toLocaleLowerCase('tr');
    t = low[0].toLocaleUpperCase('tr') + low.slice(1);
  }
  if (hit.discipline) {
    const d = hit.discipline.trim();
    if (t.toLocaleLowerCase('tr').startsWith(d.toLocaleLowerCase('tr') + ' - ')) t = t.slice(d.length + 3);
  }
  return t.trim() || hit.title;
}

/** Baştaki "[TÜR]" etiketini ve "Anahtar: değer" üst bilgi satırlarını ayırır */
function splitHeader(content: string) {
  const lines = content.replace(/\r/g, '').split('\n');
  let tagRest = '';
  if (lines.length && /^\[[^\]]{3,60}\]/.test(lines[0].trim())) {
    tagRest = lines[0].trim().replace(/^\[[^\]]+\]\s*/, '');
    lines.shift();
  }
  return { lines, tagRest };
}

/** Tek parça uzun açıklamaları ikişer cümlelik paragraflara böler (okunurluk) */
function breakLongParagraphs(md: string): string {
  return md.split('\n').map((line) => {
    const t = line.trim();
    if (t.length < 360 || /^([-*#>|]|\d+[.)])/.test(t)) return line;
    const sentences = t.match(/[^.!?]+(?:[.!?]+(?=\s+[A-ZÇĞİÖŞÜ0-9(%])|[.!?]*$)/g);
    if (!sentences || sentences.length < 3) return line;
    const paras: string[] = [];
    for (let i = 0; i < sentences.length; i += 2) paras.push(sentences.slice(i, i + 2).join('').trim());
    return paras.join('\n\n');
  }).join('\n');
}

function parseQuestion(text: string): QuestionPart | null {
  const stemM = text.match(/(?:^|\n)\s*Soru(?: Kökü)?\s*:\s*\n?([\s\S]*?)(?=\n\s*Seçenekler\s*:|\n\s*Doğru[^\n:]{0,30}:|$)/i);
  if (!stemM) return null;
  const stem = stemM[1].trim();
  const options: QuestionPart['options'] = [];
  const optBlock = text.match(/\n\s*Seçenekler\s*:\s*\n([\s\S]*?)(?=\n\s*Doğru[^\n:]{0,30}:|$)/i);
  if (optBlock) {
    for (const l of optBlock[1].split('\n')) {
      const m = l.trim().match(/^([A-E])\s*[).:-]\s*(.+)$/);
      if (m) options.push({ key: m[1], text: m[2].trim() });
    }
  }
  const ansM = text.match(/\n\s*Doğru(?:\s*\/\s*[^\n:]{0,25})?(?:\s*Cevap)?\s*:\s*([A-E])\b/i);
  let explanation = '';
  if (ansM) {
    const after = text.slice((ansM.index || 0) + ansM[0].length);
    const lines = after.replace(/^[^\n]*/, '').split('\n');
    // İlk başlık satırı ("Akademik Açıklama & …:", "DeepSeek Tıbbi Analizi & Çözümü:") atılır; "Açıklama: metin" satırı metne açılır
    const out: string[] = [];
    let first = true;
    for (const raw of lines) {
      const l = raw.trim();
      if (first && !l) continue;
      if (first) {
        first = false;
        const inline = l.match(/^(?:Açıklama|Çözüm)\s*:\s*(.+)$/i);
        if (inline) { out.push(inline[1]); continue; }
        if (/:\s*$/.test(l) && l.length < 80 && !/^[-*]/.test(l)) continue;
      }
      // Kısa başlık satırları ("Seçenek Analizi ve Çürütme (Adım Adım Mekanizma):") alt başlık olur
      if (/^[A-ZÇĞİÖŞÜ][^:]{3,70}:\s*$/.test(l) && !/^[-*]/.test(l)) { out.push(`### ${l.replace(/\s*\([^)]*\)\s*:?\s*$/, '').replace(/:\s*$/, '')}`); continue; }
      out.push(raw);
    }
    explanation = breakLongParagraphs(cleanMarkdown(out.join('\n')));
  }
  return { stem, options, answer: ansM?.[1], explanation };
}

/** Hastalık/sözlük gibi "Anahtar: değer" ve "- Etiket: metin" düzenindeki kayıtlar → Markdown */
function keyedToMarkdown(lines: string[], used: Set<string>): string {
  const out: string[] = [];
  let section = '';
  for (const raw of lines) {
    const t = raw.trim();
    if (!t) { out.push(''); continue; }
    if (/^[-*•]\s/.test(t)) {
      let item = t.replace(/^[-*•]\s+/, '');
      const lm = item.match(/^([^:]{2,40}):\s*(.*)$/);
      if (lm) {
        let val = lm[2];
        // "Yüz: Yüz: düz profil", "Eşlik eden durumlar: Eşlik eden durumlar:; …" tekrarları
        const dup = new RegExp(`^${lm[1].replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\s*:\\s*;?\\s*`, 'i');
        val = val.replace(dup, '').replace(/^;\s*/, '');
        item = lm[1].trim().toLocaleLowerCase('tr') === section ? val : `**${lm[1]}:** ${val}`;
      }
      if (!isBoilerplate(item)) out.push(`- ${item}`);
      continue;
    }
    const km = t.match(KEY_LINE);
    if (km) {
      const key = km[1].trim();
      const k = key.toLocaleLowerCase('tr');
      if (used.has(k) || DROP_KEYS.has(k)) continue;
      const val = km[2].trim();
      if (!val) { section = k; out.push('', `### ${key}`); continue; }
      if (!keepUseful(val)) continue;
      out.push(`- **${key}:** ${keepUseful(val)}`);
      continue;
    }
    out.push(t);
  }
  return out.join('\n').replace(/\n{3,}/g, '\n\n').trim();
}

const prettyCategory = (v: string) => v.replace(/_/g, ' / ').replace(/\s+/g, ' ').trim();

export function formatHit(hit: SearchHit, query: string): FormattedHit {
  const type = hit.documentType;
  const { lines, tagRest } = splitHeader(hit.content || '');
  const tags: string[] = [];
  const keyPoints: string[] = [];
  let subtitle: string | undefined;
  let context: string | undefined;
  const used = new Set<string>();
  const meta = new Map<string, string>();

  // Baştaki üst bilgi satırları
  let bodyStart = 0;
  for (; bodyStart < lines.length; bodyStart++) {
    const t = lines[bodyStart].trim();
    const km = t.match(KEY_LINE);
    if (!km) break;
    const k = km[1].trim().toLocaleLowerCase('tr');
    if (!km[2].trim()) break;
    if (/^soru( kökü)?$|^seçenekler$|^özet metin$|^içerik$|^tanım$|^anlam$/.test(k) || /^slayt \d+/.test(k)) break;
    meta.set(k, km[2].trim());
  }
  const rest = lines.slice(bodyStart);

  const kurul = meta.get('kurul');
  if (kurul) tags.push(formatKurul(kurul));
  const yil = meta.get('sınav yılı');
  if (yil) tags.push(yearTag(yil));
  const zorluk = meta.get('zorluk');
  if (zorluk) tags.push(`Zorluk: ${zorluk}`);
  const kazanim = meta.get('kazanım');
  if (kazanim && !isBoilerplate(kazanim)) context = kazanim;

  let title = cleanTitle(hit);
  let body = '';
  let question: QuestionPart | undefined;
  let preview = '';

  if (QUESTION_TYPES.has(type)) {
    const q = parseQuestion(rest.join('\n')) || parseQuestion(hit.content || '');
    if (q) {
      question = q;
      const ans = q.answer && q.options.find((o) => o.key === q.answer);
      preview = q.stem.replace(/\s+/g, ' ');
      if (preview.length > 280) preview = preview.slice(0, 280).replace(/\s+\S*$/, '') + '…';
      if (ans) preview += `\n✓ ${ans.key}) ${ans.text}`;
    } else body = cleanMarkdown(rest.join('\n'));
  } else if (type === 'disease') {
    if (tagRest) {
      const en = tagRest.match(/\(([^()]*(?:\([^()]*\))?[^()]*)\)\s*$/);
      if (en && /[a-z]/.test(en[1]) && !/[çğışöü]/i.test(en[1])) subtitle = en[1];
    }
    const extra: string[] = [];
    for (const [k, v] of meta) {
      if (k === 'tür') v.split(/\s*·\s*/).filter((x) => x && !/^hastalık$/i.test(x)).forEach((x) => tags.push(x));
      else if (k === 'kategori') tags.push(v);
      else if (k === 'latince') subtitle = subtitle || v.replace(/^\[|\]$/g, '');
      else if (k === 'diğer adlar' || k === 'eşanlamlı') { /* başlığın yinelenen yazımları */ }
      else if (k === 'karakteristik özellik') v.split(/\s*·\s*/).filter(Boolean).forEach((x) => keyPoints.push(x));
      else if (!DROP_KEYS.has(k) && keepUseful(v)) extra.push(`- **${k[0].toLocaleUpperCase('tr')}${k.slice(1)}:** ${keepUseful(v)}`);
      used.add(k);
    }
    body = [extra.join('\n'), keyedToMarkdown(rest, used)].filter(Boolean).join('\n\n');
  } else if (type === 'glossary_term' || type === 'gemini_v3_term') {
    const all = new Map(meta);
    for (const l of rest) { const km = l.trim().match(KEY_LINE); if (km) all.set(km[1].trim().toLocaleLowerCase('tr'), km[2].trim()); }
    const en = all.get('ingilizce') || all.get('latince');
    if (en) subtitle = en;
    const cat = all.get('kategori');
    if (cat) tags.push(prettyCategory(cat));
    const parts: string[] = [];
    const def = all.get('tanım') || all.get('anlam');
    if (def) parts.push(def);
    const pearl = all.get('klinik inci');
    if (pearl) parts.push('', `Sınav: ${pearl}`);
    const syn = all.get('eşanlamlı');
    if (syn) parts.push('', `- **Eşanlamlı:** ${syn}`);
    for (const [k, v] of all) {
      if (['ingilizce', 'latince', 'kategori', 'tanım', 'anlam', 'klinik inci', 'eşanlamlı'].includes(k) || DROP_KEYS.has(k) || !v) continue;
      parts.push(`- **${k[0].toLocaleUpperCase('tr')}${k.slice(1)}:** ${v}`);
    }
    body = parts.join('\n').trim() || (type === 'gemini_v3_term' ? '' : cleanMarkdown(rest.join('\n')));
  } else if (type === 'lecture_slide') {
    const idx = rest.findIndex((l) => /^\s*İçerik\s*:/i.test(l));
    const raw = (idx >= 0 ? rest.slice(idx + 1) : rest).map((l) => l.trim()).filter((l) => l && !/^[·•o▪■◦\-–*]$/.test(l));
    // Slayt metni kısa satırlardan oluşur: ilk satır başlık, kalanı madde
    const head = raw.length > 1 && raw[0].length < 90 ? raw.shift()! : '';
    // Slaytın kendi başlığı karta başlık olur; dosya adı alt satıra iner
    if (head) { subtitle = /^[\d\s.-]*$/.test(title) ? meta.get('konu') : title; title = head; }
    const short = raw.length > 2 && raw.filter((l) => l.length < 110).length / raw.length > 0.6;
    body = [...raw.map((l) => (short && !/^[-*]\s/.test(l) ? `- ${l.replace(/^[·•▪■◦]\s*/, '')}` : l))].join('\n').trim();
  } else {
    // Öğren slaytı, ders özeti, ses kaydı vb.: Markdown gövde
    const r = rest.filter((l) => !/^\s*Slayt\s+\d+\s*:/i.test(l) && !/^\s*Özet Metin\s*:\s*$/i.test(l));
    body = cleanMarkdown(r.join('\n'));
  }

  if (!preview) {
    const base = [keyPoints.join(' · '), plainText(body)].filter(Boolean).join(' — ') || hit.snippet || '';
    // Başlık zaten eşleşiyorsa önizleme baştan (tanım/öne çıkanlar); değilse eşleşmenin çevresi
    preview = matches(title, query) ? windowAround(base, '', 240) : windowAround(base, query);
  }
  if (/^\p{Ll}/u.test(title)) title = title[0].toLocaleUpperCase('tr') + title.slice(1);
  return { title, subtitle, tags: Array.from(new Set(tags)).slice(0, 4), context, keyPoints, question, body, preview };
}
