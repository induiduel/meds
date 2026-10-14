/**
 * İlerlemeyi sıfırlama: öğrenci çözdüğü soruları, Öğren ilerlemesini, kart kutusunu ve spot/özet işaretlerini
 * silebilir; istatistikler (çalışma süresi, etkinlik günlüğü, çözüm/deneme geçmişi) korunur.
 *
 * - Silmeden önce soru çözümleri ve deneme sonuçları `medsoru_stats_archive_v1`'e (profil kv) eklenir;
 *   İstatistiklerim sayfası arşiv + güncel çözümleri birlikte okur (`getStatsAttempts`, `getStatsTests`).
 * - Paket alanlarıyla (birleşimle) eşitlenen veriler için `medsoru_progress_reset_v1` kapsam başına sıfırlama
 *   zamanı tutar; paketle sunucuya gider ve birleştirme (sunucu `mergeUserBundle`, istemci `applyBundleInner`)
 *   bu zamandan eski kayıtları geri getirmez. kv anahtarları zaten son yazan kazanır ile silinir.
 */
import type { AttemptRecord, SelfTestResult } from './studyStore';
import { getProgress, getTestHistory } from './studyStore';

export type ResetScope = 'soru' | 'ogren' | 'kart' | 'spot';
/** Paket alanlarında taşınan kapsamların sıfırlama zamanları (ISO). */
export type ProgressResetStamps = Partial<Record<'soru' | 'kart', string>>;

export const RESET_KEY = 'medsoru_progress_reset_v1';
export const ARCHIVE_KEY = 'medsoru_stats_archive_v1';
const ARCHIVE_MAX_ATTEMPTS = 20000;
const ARCHIVE_MAX_TESTS = 500;

/** Arşivdeki çözüm: soru kimliği, doğru mu, zaman. */
type ArchivedAttempt = { id: string; c: boolean; at: string };
interface StatsArchive {
  attempts: ArchivedAttempt[];
  tests: SelfTestResult[];
}

export const RESET_SCOPES: { id: ResetScope; title: string; desc: string; keys: string[] }[] = [
  {
    id: 'soru',
    title: 'Çözdüğüm sorular',
    desc: 'Çıkmış ve örnek sorulardaki cevapların, yanlışlar listesi ve deneme sınavı geçmişi.',
    keys: ['medsoru_study_progress_v1', 'medsoru_study_review_v1', 'medsoru_selftest_history_v1', 'cikmis_quiz', 'medsoru_ornek_k1_cevap'],
  },
  {
    id: 'ogren',
    title: 'Öğren ilerlemesi',
    desc: 'Destelerde kaldığın adım, bitirilen dersler, etkileşim cevapları ve tekrar listesi.',
    keys: ['medsoru_learn_progress_v1', 'medsoru_learn_done_v1', 'medsoru_learn_review_v1', 'medsoru_learn_sessions_v1'],
  },
  {
    id: 'kart',
    title: 'Kart tekrarları',
    desc: 'Bilgi kartlarının aralıklı tekrar durumu (kartlar ve favoriler kalır).',
    keys: ['medsoru_flashcards_v1'],
  },
  {
    id: 'spot',
    title: 'Spot ve özet işaretleri',
    desc: '"Öğrendim" işaretli sınav spotları ve ders özetlerinde okuma ilerlemesi.',
    keys: ['medsoru_spot_ogrendim', 'medsoru_summary_progress'],
  },
];

const readJson = <T,>(key: string, fallback: T): T => {
  try {
    const raw = localStorage.getItem(key);
    return raw ? (JSON.parse(raw) as T) : fallback;
  } catch {
    return fallback;
  }
};
const writeJson = (key: string, v: unknown) => {
  try { localStorage.setItem(key, JSON.stringify(v)); } catch { /* yoksay */ }
};

export const getResetStamps = (): ProgressResetStamps => readJson<ProgressResetStamps>(RESET_KEY, {});
export const setResetStamps = (s: ProgressResetStamps) => writeJson(RESET_KEY, s);

const readArchive = (): StatsArchive => {
  const a = readJson<Partial<StatsArchive>>(ARCHIVE_KEY, {});
  return { attempts: Array.isArray(a.attempts) ? a.attempts : [], tests: Array.isArray(a.tests) ? a.tests : [] };
};

/** Seçilen kapsamlar için kaç kayıt silineceği (onay penceresinde gösterilir). */
export function countScope(scope: ResetScope): number {
  const size = (key: string) => {
    const v = readJson<unknown>(key, null);
    if (Array.isArray(v)) return v.length;
    if (v && typeof v === 'object') return Object.keys(v).length;
    return 0;
  };
  if (scope === 'soru') return Object.keys(getProgress()).length + getTestHistory().length + size('cikmis_quiz') + size('medsoru_ornek_k1_cevap');
  const def = RESET_SCOPES.find((s) => s.id === scope)!;
  return def.keys.reduce((n, k) => n + size(k), 0);
}

/** İstatistik için tüm çözümler: arşivdekiler + güncel ilerleme. */
export function getStatsAttempts(): [string, AttemptRecord][] {
  const archived = readArchive().attempts.map((a): [string, AttemptRecord] => [a.id, { picked: 'A', correct: a.c, at: a.at }]);
  return [...archived, ...Object.entries(getProgress())];
}

/** İstatistik için tüm denemeler: arşivdekiler + güncel geçmiş. */
export function getStatsTests(): SelfTestResult[] {
  const seen = new Set<string>();
  return [...readArchive().tests, ...getTestHistory()].filter((t) => t && !seen.has(t.id) && seen.add(t.id));
}

/**
 * Seçilen kapsamları siler. Soru kapsamında önce çözümler ve denemeler istatistik arşivine eklenir.
 * Çağıran taraf sonra sayfayı yeniden yüklemelidir (açık ekranlar eski durumu bellekte tutar).
 */
export function resetProgress(scopes: ResetScope[]): void {
  const now = new Date().toISOString();
  if (scopes.includes('soru')) {
    const arc = readArchive();
    for (const [id, a] of Object.entries(getProgress())) if (a?.at) arc.attempts.push({ id, c: Boolean(a.correct), at: a.at });
    const known = new Set(arc.tests.map((t) => t.id));
    for (const t of getTestHistory()) if (t && !known.has(t.id)) arc.tests.push({ ...t, answers: {} });
    writeJson(ARCHIVE_KEY, {
      attempts: arc.attempts.slice(-ARCHIVE_MAX_ATTEMPTS),
      tests: arc.tests.sort((x, y) => String(x.at).localeCompare(String(y.at))).slice(-ARCHIVE_MAX_TESTS),
    });
  }
  const stamps = getResetStamps();
  for (const scope of scopes) {
    if (scope === 'soru' || scope === 'kart') stamps[scope] = now;
    for (const key of RESET_SCOPES.find((s) => s.id === scope)!.keys) {
      try { localStorage.removeItem(key); } catch { /* yoksay */ }
    }
  }
  setResetStamps(stamps);
}
