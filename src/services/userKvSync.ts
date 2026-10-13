/**
 * Profil anahtar deposu: öğrencinin sitede yaptığı her şey (Öğren ilerlemesi, vurgular, çizimler, kart notları,
 * sınav spotu "öğrendim", örnek soru cevapları, özel hastalık/sözlük kayıtları, müzik listesi, görünüm ve ekran
 * tercihleri…) profiline yazılır.
 *
 * Nasıl: localStorage.setItem/removeItem bir kez sarılır. İzin listesindeki bir anahtar değişince değişiklik
 * zamanı (`at`) damgalanır, anahtar "kirli" işaretlenir ve dinleyiciye (userDataSyncService → birkaç saniye
 * içinde sunucuya gönderim) haber verilir. Sunucuda anahtar başına son yazan kazanır; diğer cihazlar SSE
 * `user_data_changed` ile anında çeker. Ekranlara tek tek dokunmaya gerek yoktur.
 *
 * İzin listesine girmeyenler: API anahtarları, yönetici oturumu, cihaz kimliği, önbellekler, geçiş bayrakları.
 */

export type KvRecord = { v: string | null; at: string };
export type KvMap = Record<string, KvRecord>;

/** Profilde tutulan anahtarlar (desen). Eşitleme servisinin özel birleştirdiği anahtarlar ayrı listededir. */
const SYNC_PATTERNS: RegExp[] = [
  // Öğren
  /^medsoru_learn_(progress|done|recent|layout|mode|toc|zoom)(_v1)?$/,
  /^medsoru_learn_feedback_local_v1$/,
  /^medsoru_slide_drawings_v2(:.*)?$/,
  /^medsoru_annotations:.+$/,
  /^medsoru_highlights_v1$/,
  // Kartlar, sözlük, hastalıklar
  /^medsoru_card_notes_v1$/,
  /^medsoru_card_note_open$/,
  /^medsoru_custom_encyclopedia_v1$/,
  /^medsor_(custom|favorite)_diseases_v1$/,
  // Sınav spotları, örnek/çıkmış sorular
  /^medsoru_spot_ogrendim$/,
  /^medsoru_ornek_(k1_cevap|k1_ders|k1_social|havuz_social|sekme)$/,
  /^cikmis_quiz$/,
  /^my_(comment|report)_ids$/,
  // Ders özetleri / okuyucu
  /^medsoru_summary_progress$/,
  /^medsoru_reader_prefs$/,
  // Katkı formu, arama, yapay zekâ sohbeti
  /^medsoru_saved_(contributor_name|student_number)$/,
  /^medsoru_contrib_exam_year$/,
  /^medsoru_recent_searches$/,
  /^medsoru_ai_chat_history_.+$/,
  // Müzik
  /^medsoru_music_(custom|volume)_v1$/,
  // Görünüm ve ekran tercihleri
  /^medsoru_appearance$/,
  /^medsoru_auto_reveal$/,
  /^medsoru_(glossary|search|studio)_view$/,
  /^medsoru_solve_drawer$/,
  /^medsoru_study_section$/,
  /^medsoru_rail_collapsed$/,
  /^medsoru_last_(committee_id|discipline|status)$/,
  /^medsoru_pdf_(page|q|l|s)_v2$/,
  /^tc_layout$/,
  /^medsor_love_note_hidden_v1$/,
];

/** userDataSyncService'in kendi alanlarında taşıdığı anahtarlar: değişince yine anında gönderim tetiklenir. */
const BUNDLE_KEYS = new Set([
  'medsoru_selftest_history_v1',
  'medsoru_study_progress_v1',
  'medsoru_study_review_v1',
  'medsoru_flashcards_v1',
  'medsoru_study_favorites_v1',
  'medsoru_flashcard_favorites_v1',
  'medsoru_bookmarked_encyclopedia',
  'medsoru_user_notifications_v1',
  'medsoru_user_notifications_deleted_v1',
  'medsoru_push_notifications_enabled',
  'medsoru_email_notifications_enabled',
  'medsoru_notes_v1',
]);
/** Sık yazılan sayaçlar: profile girer ama anlık gönderim tetiklemez (dönemsel/arka plana geçişte gider). */
const QUIET_KEYS = new Set(['medsoru_study_seconds_v1', 'medsoru_activity_v1']);

const META_KEY = 'medsoru_kv_meta_v1'; // anahtar → son yerel değişiklik zamanı
const DIRTY_KEY = 'medsoru_kv_dirty_v1'; // henüz sunucuya gitmemiş anahtarlar
const MAX_VALUE = 2_000_000; // sunucudaki sınırla aynı

export const isProfileKey = (key: string): boolean => SYNC_PATTERNS.some((re) => re.test(key));

let rawSet: ((k: string, v: string) => void) | null = null;
let rawRemove: ((k: string) => void) | null = null;
let applying = 0;
const changeListeners = new Set<(immediate: boolean) => void>();

const ls = (): Storage | null => {
  try {
    return typeof window !== 'undefined' ? window.localStorage : null;
  } catch {
    return null;
  }
};

const readObj = <T extends object>(key: string): T => {
  try {
    const raw = ls()?.getItem(key);
    const v = raw ? JSON.parse(raw) : {};
    return v && typeof v === 'object' ? v : ({} as T);
  } catch {
    return {} as T;
  }
};
const writeObj = (key: string, val: unknown) => {
  try {
    const s = ls();
    if (!s) return;
    (rawSet ? rawSet.bind(s) : s.setItem.bind(s))(key, JSON.stringify(val));
  } catch {
    /* kota/gizli pencere */
  }
};

function stamp(key: string) {
  const at = new Date().toISOString();
  const meta = readObj<Record<string, string>>(META_KEY);
  meta[key] = at;
  writeObj(META_KEY, meta);
  const dirty = readObj<Record<string, 1>>(DIRTY_KEY);
  dirty[key] = 1;
  writeObj(DIRTY_KEY, dirty);
}

function onWrite(key: string) {
  if (applying) return;
  if (isProfileKey(key)) {
    stamp(key);
    changeListeners.forEach((fn) => fn(true));
  } else if (BUNDLE_KEYS.has(key)) {
    changeListeners.forEach((fn) => fn(true));
  } else if (QUIET_KEYS.has(key)) {
    changeListeners.forEach((fn) => fn(false));
  }
}

/** Uygulama açılışında bir kez: localStorage yazımlarını izlemeye başla. */
export function installProfileKvWatcher(): void {
  const s = ls();
  if (!s || rawSet) return;
  const proto = Object.getPrototypeOf(s) as Storage;
  const origSet = proto.setItem;
  const origRemove = proto.removeItem;
  rawSet = function (this: Storage, k: string, v: string) {
    origSet.call(this, k, v);
  } as any;
  rawRemove = function (this: Storage, k: string) {
    origRemove.call(this, k);
  } as any;
  proto.setItem = function (this: Storage, k: string, v: string) {
    origSet.call(this, k, v);
    if (this === s) {
      try {
        onWrite(String(k));
      } catch {
        /* izleme asla yazmayı bozmaz */
      }
    }
  };
  proto.removeItem = function (this: Storage, k: string) {
    origRemove.call(this, k);
    if (this === s) {
      try {
        onWrite(String(k));
      } catch {
        /* yoksay */
      }
    }
  };
}

/** Profil verisi değişince haber ver (`immediate`: birkaç saniye içinde gönder; değilse dönemsel gönderime bırak). */
export function onProfileDataChange(fn: (immediate: boolean) => void): () => void {
  changeListeners.add(fn);
  return () => changeListeners.delete(fn);
}

export function hasDirtyKv(): boolean {
  return Object.keys(readObj(DIRTY_KEY)).length > 0;
}

/**
 * Gönderilecek kv: `full` ise izin listesindeki tüm anahtarlar (ilk eşitleme / hesap değişimi), değilse yalnız kirli
 * olanlar. Hiç damgası olmayan eski veri '0' zamanlıdır: sunucuda başka cihazdan gelmiş bir kayıt varsa o kazanır.
 */
export function collectKv(full: boolean): { kv: KvMap; sentKeys: string[] } {
  const s = ls();
  const kv: KvMap = {};
  if (!s) return { kv, sentKeys: [] };
  const meta = readObj<Record<string, string>>(META_KEY);
  const keys = new Set<string>(Object.keys(readObj(DIRTY_KEY)));
  if (full) {
    for (let i = 0; i < s.length; i++) {
      const k = s.key(i);
      if (k && isProfileKey(k)) keys.add(k);
    }
    for (const k of Object.keys(meta)) if (isProfileKey(k)) keys.add(k); // silinmiş anahtarlar
  }
  for (const k of keys) {
    if (!isProfileKey(k)) continue;
    const v = s.getItem(k);
    if (v != null && v.length > MAX_VALUE) continue;
    kv[k] = { v, at: meta[k] || '0' };
  }
  return { kv, sentKeys: Object.keys(kv) };
}

/** Gönderim başarılıysa: gönderilen anahtarlardan, o arada yeniden değişmeyenlerin kirliliği kalkar. */
export function markKvSent(sent: KvMap): void {
  const meta = readObj<Record<string, string>>(META_KEY);
  const dirty = readObj<Record<string, 1>>(DIRTY_KEY);
  for (const [k, r] of Object.entries(sent)) if ((meta[k] || '0') === r.at) delete dirty[k];
  writeObj(DIRTY_KEY, dirty);
}

/**
 * Sunucudan gelen kv'yi uygula: yalnız sunucudaki kayıt yereldekinden yeniyse yazılır. Değişen anahtarlar için
 * `storage` olayı yayınlanır (aynı sekmedeki dinleyiciler de güncellensin). Dönüş: değişen anahtarlar.
 */
export function applyKv(remote: KvMap | undefined | null): string[] {
  const s = ls();
  if (!s || !remote || typeof remote !== 'object') return [];
  const meta = readObj<Record<string, string>>(META_KEY);
  const dirty = readObj<Record<string, 1>>(DIRTY_KEY);
  const changed: string[] = [];
  applying++;
  try {
    for (const [k, r] of Object.entries(remote)) {
      if (!isProfileKey(k) || !r || typeof r !== 'object') continue;
      const at = String(r.at || '');
      if (at <= (meta[k] || '')) continue;
      const cur = s.getItem(k);
      if (r.v == null) {
        if (cur != null) (rawRemove || s.removeItem).call(s, k);
      } else if (cur !== r.v) {
        (rawSet || s.setItem).call(s, k, r.v);
      }
      meta[k] = at;
      delete dirty[k];
      if (cur !== r.v) changed.push(k);
    }
    writeObj(META_KEY, meta);
    writeObj(DIRTY_KEY, dirty);
  } finally {
    applying--;
  }
  if (changed.length && typeof window !== 'undefined') {
    for (const k of changed) {
      try {
        window.dispatchEvent(new StorageEvent('storage', { key: k, storageArea: s }));
      } catch {
        /* eski tarayıcı */
      }
    }
    window.dispatchEvent(new CustomEvent('medsoru:profile-kv-applied', { detail: { keys: changed } }));
  }
  return changed;
}

/** Sunucudan veri uygulanırken yapılan yazımlar gönderim tetiklemesin. */
export function withoutTracking<T>(fn: () => T): T {
  applying++;
  try {
    return fn();
  } finally {
    applying--;
  }
}
