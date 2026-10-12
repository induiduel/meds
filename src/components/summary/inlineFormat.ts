/**
 * Özet satırı → güvenli HTML. Sıra: kaçış → markdown (==vurgu==, **kalın**, *eğik*, `kod`) → arama eşleşmesi
 * → tıbbi işaretler. İşaretler yalnız etiket dışındaki metne uygulanır; böylece sınıf adları ya da
 * daha önce sarılmış parçalar bozulmaz. Renkler styles/summary.css'teki .sr-m-* sınıflarından (token) gelir.
 */

const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

/** Yalnız etiket dışındaki metin parçalarına uygular */
const mapText = (html: string, fn: (t: string) => string) =>
  html
    .split(/(<[^>]+>)/)
    .map((part) => (part.startsWith('<') ? part : fn(part)))
    .join('');

// Türkçe harfler \b ile çalışmaz: öncesinde harf/rakam olmaması yeterli (ek alabilir: "kontrendikedir")
const W = '(?<![\\p{L}\\p{N}])';
const MARKERS: [RegExp, string][] = [
  [new RegExp(`${W}(en sık|altın standart|ilk tercih|en önemli|en duyarlı|en özgül|patognomonik|tanı koydurucu)`, 'giu'), 'key'],
  [new RegExp(`${W}(kontrendike|toksisite|yan etki|ölümcül|teratojenik|nefrotoksi|hepatotoksi|mortalite)`, 'giu'), 'risk'],
  [/(%\s?\d+(?:[.,]\d+)?(?:\s?[-–]\s?%?\d+(?:[.,]\d+)?)?|(?<![\p{L}\p{N}.,])\d+(?:[.,]\d+)?(?:\s?[-–]\s?\d+(?:[.,]\d+)?)?\s?(?:μm|µm|mm|cm|metre|mg\/dl|mg\/dL|g\/dl|g\/dL|mEq\/L|mmHg|mcg|mg|ml|mL|kg|saat|gün|hafta|ay|yıl|yaş|kez|dakika|dk|°C)(?![\p{L}]))/gu, 'num'],
];

const markMedical = (t: string) => {
  let out = t;
  for (const [re, cls] of MARKERS) {
    out = mapText(out, (s) => s.replace(re, `<span class="sr-m sr-m-${cls}">$1</span>`));
  }
  return mapText(out, (s) => s.replace(/↑+/g, '<span class="sr-m-up">$&</span>').replace(/↓+/g, '<span class="sr-m-down">$&</span>'));
};

export interface InlineOpts {
  markers: boolean;
  /** Belge içi arama (en az 2 harf) */
  query?: string;
}

export function formatInline(src: string, { markers, query }: InlineOpts): string {
  if (!src) return '';
  let html = esc(src)
    .replace(/==([^=\n]+?)==/g, '<mark class="sr-em">$1</mark>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/(^|[^*\w])\*(?!\s)([^*\n]+?)\*(?!\w)/g, '$1<em>$2</em>')
    .replace(/`([^`]+)`/g, '<code>$1</code>');
  const q = (query || '').trim();
  if (q.length >= 2) {
    const re = new RegExp(esc(q).replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'giu');
    html = mapText(html, (s) => s.replace(re, '<mark class="sr-hit">$&</mark>'));
  }
  if (markers) html = markMedical(html);
  return html;
}
