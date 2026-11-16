/**
 * Öğren desteleri tek deposu (sunucu tarafı) — `scripts/deste_deposu.py`'nin eşi.
 *
 * `interactive_learning_decks.json` yolu yalnız burada tanımlıdır. Okuma canlı içerik katmanından
 * (`resolveContent`) yapılır ve mtime ile önbelleğe alınır; yazım katmana (`writableContent`) atomik
 * yapılır, `markContentChanged('decks', ids)` yayınlanır ve önbellek geçersiz kılınır.
 */
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { fileURLToPath } from 'url';
import { resolveContent, writableContent, markContentChanged } from './contentOverlay.ts';

const __filename = fileURLToPath(import.meta.url);
const ROOT_DIR = path.resolve(path.dirname(__filename), '..', '..'); // meds/

export const INTERACTIVE_DECKS_FILE = path.resolve(ROOT_DIR, 'src', 'data', 'interactive_learning_decks.json');

/*
 * Parçalı OKUMA arka ucu (VERI_MODELI Faz 3 iskelesi; biçim tanımı `scripts/deste_deposu.py`).
 * Yalnız MEDS_DESTE_PARCALI=1 + MEDS_DESTE_PARCA_DIZIN verilmişse ve içerik katmanında deste farkı YOKSA etkin:
 * katman (Oracle canlı farkları) her zaman önceliklidir. Yazım bu aşamada monolitte (katmanda) kalır.
 */
const PARCA_SIRA = '_sira.json';
function parcaDizini(): string | null {
  const dz = process.env.MEDS_DESTE_PARCA_DIZIN;
  return process.env.MEDS_DESTE_PARCALI === '1' && dz ? path.resolve(dz) : null;
}
function parcaliOkumaDizini(): string | null {
  const dz = parcaDizini();
  if (!dz || desteKatmandaMi()) return null; // katman farkı varken parçalı okuma KAPALI
  return fs.existsSync(path.join(dz, PARCA_SIRA)) ? dz : null;
}
/** deste_deposu.py `dosya_adi` ile aynı kural (çakışmasız, geri çevrilebilir). */
function parcaDosyaAdi(id: string): string {
  if (/^[A-Za-z0-9][A-Za-z0-9._-]*$/.test(id) && id.length <= 200) return `${id}.json`;
  return `~${Buffer.from(id, 'utf-8').toString('hex')}.json`;
}
function parcalariBirlestir(dz: string): any[] {
  const sira = JSON.parse(fs.readFileSync(path.join(dz, PARCA_SIRA), 'utf-8'));
  if (sira?.bicim !== 1) throw new Error(`desteler/_sira.json biçimi ${sira?.bicim} desteklenmiyor`);
  return (sira.desteler || []).map((g: any) => JSON.parse(fs.readFileSync(path.join(dz, g.dosya), 'utf-8')));
}

export interface DesteOnbellegi {
  file: string;
  mtime: number;
  data: any[];
  compactJsonStr: string;
  compactEtag: string;
  /** Tam liste JSON'unun ETag'i; ilk `desteTamJson()` çağrısında hesaplanır (dizginin kendisi TUTULMAZ). */
  fullEtag?: string;
}

let decksCache: DesteOnbellegi | null = null;

/*
 * Bellek (2026-11-16): tam liste dizgisi (`fullJsonStr`, ~154 MB UTF-16) artık önbellekte tutulmaz — yalnız süzgeçsiz
 * `/api/decks` (compact olmadan) kullanıyordu ve ön yüzde çağıran yok. İstenince üretilir; bayt ve ETag aynıdır.
 * Boşta bırakma: son erişimden MEDS_DESTE_ONBELLEK_DK (vars. 10) dakika sonra önbellek bırakılır; her erişim süreyi uzatır.
 */
const BOSTA_MS = Math.max(1, Number(process.env.MEDS_DESTE_ONBELLEK_DK) || 10) * 60_000;
let sonErisim = 0;
let bostaZamanlayici: ReturnType<typeof setTimeout> | null = null;
function erisimDamgala(): void {
  sonErisim = Date.now();
  if (bostaZamanlayici) return; // tek zamanlayıcı; süre dolunca son erişime göre yeniden kurulur (döngüsüz)
  const kur = (ms: number) => {
    bostaZamanlayici = setTimeout(() => {
      const kalan = sonErisim + BOSTA_MS - Date.now();
      if (kalan > 0) return kur(kalan);
      bostaZamanlayici = null;
      decksCache = null;
    }, ms);
    bostaZamanlayici.unref?.();
  };
  kur(BOSTA_MS);
}

/** Son önbellek (ETag'li hazır JSON dizgeleri için); `desteleriOku()` çağrısından sonra günceldir. */
export function desteOnbellegi(): DesteOnbellegi | null {
  return decksCache;
}

/** Süzgeçsiz tam liste yanıtı: dizge istek başına üretilir (tutulmaz), ETag önbelleğe yazılır. */
export function desteTamJson(): { json: string; etag: string } {
  const list = desteleriOku();
  const json = JSON.stringify({ total: list.length, decks: list });
  const etag = `"${crypto.createHash('md5').update(json).digest('hex')}"`;
  if (decksCache && decksCache.data === list) decksCache.fullEtag = etag;
  return { json, etag };
}

/** Yalnız ETag (304 yanıtı için dizge üretmeden, hesaplanmışsa). */
export function desteTamEtag(): string | null {
  desteleriOku();
  return decksCache?.fullEtag || null;
}

/**
 * Deste listesini okur (katman öncelikli, mtime önbellekli). Dönen dizi önbellekle paylaşılır — DEĞİŞTİRME.
 * Değiştirip geri yazacaksan `{ kopya: true }` ver: dosyadan taze ayrıştırılmış bağımsız liste döner.
 */
export function desteleriOku(secenek: { kopya?: boolean } = {}): any[] {
  const dz = parcaliOkumaDizini();
  if (secenek.kopya) {
    try {
      if (dz) return parcalariBirlestir(dz);
      const file = resolveContent(INTERACTIVE_DECKS_FILE);
      if (!fs.existsSync(file)) return [];
      const data = JSON.parse(fs.readFileSync(file, 'utf-8'));
      return Array.isArray(data) ? data : [];
    } catch (e) {
      console.error('Error reading interactive_learning_decks.json:', e);
      return [];
    }
  }
  erisimDamgala();
  try {
    // Parçalı kipte önbellek anahtarı _sira.json'dur (her parça yazımında yeniden yazılır); mantık aynı.
    const file = dz ? path.join(dz, PARCA_SIRA) : resolveContent(INTERACTIVE_DECKS_FILE);
    if (fs.existsSync(file)) {
      const mtime = fs.statSync(file).mtimeMs;
      if (decksCache && decksCache.file === file && decksCache.mtime === mtime) return decksCache.data;
      const data = dz ? parcalariBirlestir(dz) : JSON.parse(fs.readFileSync(file, 'utf-8'));
      const list = Array.isArray(data) ? data : [];
      const compactList = list.map((d: any) => ({
        id: d.id,
        title: d.title,
        description: d.description,
        committee: d.committee || d.committeeId,
        discipline: d.discipline,
        slideCount: d.slides?.length || 0,
        flashcardCount: d.flashcards?.length || 0,
        updatedAt: d.updatedAt,
      }));
      const compactJsonStr = JSON.stringify({ total: compactList.length, decks: compactList });
      const compactEtag = `"${crypto.createHash('md5').update(compactJsonStr).digest('hex')}"`;
      decksCache = { file, mtime, data: list, compactJsonStr, compactEtag };
      return list;
    }
  } catch (e) {
    console.error('Error reading interactive_learning_decks.json:', e);
  }
  return decksCache?.data || [];
}

/** Tek deste: tam id, `k1p-<id>` ya da id içeren ilk eşleşme (server.ts /api/decks/:id kuralı). */
export function desteOku(id: string, list?: any[]): any | null {
  if (!list) {
    const dz = parcaliOkumaDizini();
    if (dz) {
      // Tek dosya okunur (monolit/birleşim ayrıştırılmaz); bulunamazsa eski kuralın 'içeren' eşleşmesine düşülür.
      for (const ad of [id, `k1p-${id}`]) {
        const p = path.join(dz, parcaDosyaAdi(ad));
        if (fs.existsSync(p)) return JSON.parse(fs.readFileSync(p, 'utf-8'));
      }
    }
    list = desteleriOku();
  }
  return list.find((d) => d.id === id || d.id === `k1p-${id}` || d.id.includes(id)) || null;
}

/** Katman etkin mi (deste dosyası katmandan mı geliyor)? */
export function desteKatmandaMi(): boolean {
  return resolveContent(INTERACTIVE_DECKS_FILE) !== INTERACTIVE_DECKS_FILE;
}

/** Listeyi katmana atomik yazar (JSON.stringify girinti 2), değişimi yayınlar, önbelleği geçersiz kılar. */
export function desteleriYaz(list: any[], degisenIdler: string[]): void {
  const filePath = writableContent(INTERACTIVE_DECKS_FILE);
  const dir = path.dirname(filePath);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  const tempPath = `${filePath}.tmp_${Date.now()}_${Math.random().toString(36).slice(2, 6)}`;
  fs.writeFileSync(tempPath, JSON.stringify(list, null, 2), 'utf-8');
  fs.renameSync(tempPath, filePath);
  decksCache = null;
  markContentChanged('decks', degisenIdler.map(String));
}
