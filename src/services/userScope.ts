/**
 * Tarayıcıdaki öğrenci verisinin sahibi.
 *
 * localStorage'daki kişisel anahtarlar (ilerleme, notlar, kartlar, cevaplar, taslaklar, ad/öğrenci no, eşitleme
 * defteri…) hesap adıyla ayrılmaz; bu yüzden aynı tarayıcıda oturum değişince eski öğrencinin verisi yeni öğrencinin
 * ekranına ve — ilk eşitlemede — hesabına geçerdi. Burada:
 *  - `medsoru_owner_v1` verinin sahibini tutar: uid ya da '' (oturumsuz kullanım).
 *  - Oturum açan uid sahip değilse: önceki sahibin verisi `medsoru_stash_v1:<uid>` altına kaldırılır (yeni öğrenci
 *    görmez, sunucuya gitmez), alan temizlenir; bu uid'nin daha önce kaldırılmış verisi varsa geri konur.
 *  - Oturumsuz veri (sahip '') oturum açan kişiye geçer: oturum açmadan önce kendisi kullanmıştır.
 *  - Çıkışta: önce sunucuya gönderilir, sonra kişisel anahtarlar silinir ve oturumsuz cihaz kimliği yenilenir
 *    (aksi halde sonraki oturumsuz kişi eski öğrencinin cihaz yedeğini çekerdi).
 * Genel/cihaz ayarları (tema, önbellekler, API adresi) dokunulmadan kalır.
 */
import { isUserDataKey } from './userKvSync';

const OWNER_KEY = 'medsoru_owner_v1';
const STASH_PREFIX = 'medsoru_stash_v1:';

/** userKvSync'in eşitlediği anahtarlara ek olarak kişisel sayılanlar. */
const EXTRA_PERSONAL: RegExp[] = [
  /^medsoru_learn_(attempts|recent|review|sessions|social|voter_id)(_v1)?$/,
  /^medsoru_notes_(deleted_v1|sync_code|synced_identity|synced_at)$/,
  /^medsoru_kv_(meta|dirty|since)_v1$/,
  /^medsoru_last_user_data_(backup|restore)_at$/,
  /^medsoru_(quickadd_draft_v1|open_learn_review|test_kriter_v1|pdf_sel_v1|saglik_sina_v1)$/,
  /^medsoru_draft_studio_.+$/,
  /^medsoru_ornek_.+$/,
  /^medsoru_lecture_notes(_v\d+.*)?$/,
  /^medsoru_user_profile_cache_.+$/,
  /^medsoru_(drive_token|drive_automation_status_v2)$/,
  /^medsoru_(user_registered|visit_count)$/,
  /^medsoru_device_(token|pub)$/,
];

/** Profilde eşitlense de kişisel bilgi taşımayan görünüm/düzen tercihleri: cihazda kalır. */
const DEVICE_PREFS = /^(medsoru_appearance|medsoru_rail_collapsed|medsoru_learn_(layout|mode|toc|zoom)|medsoru_(glossary|search|studio)_view|medsoru_reader_prefs|tc_layout|medsoru_auto_reveal|medsoru_solve_drawer|medsoru_study_section|medsoru_music_volume_v1|medsoru_card_note_open)$/;

export const isPersonalKey = (k: string) =>
  !k.startsWith(STASH_PREFIX) && k !== OWNER_KEY && !DEVICE_PREFS.test(k) && (isUserDataKey(k) || EXTRA_PERSONAL.some((re) => re.test(k)));

const ls = (): Storage | null => {
  try {
    return typeof window !== 'undefined' ? window.localStorage : null;
  } catch {
    return null;
  }
};

export const getOwner = (): string | null => ls()?.getItem(OWNER_KEY) ?? null;
const setOwner = (uid: string) => ls()?.setItem(OWNER_KEY, uid);

const personalKeys = (s: Storage) => {
  const out: string[] = [];
  for (let i = 0; i < s.length; i++) {
    const k = s.key(i);
    if (k && isPersonalKey(k)) out.push(k);
  }
  return out;
};

/** Kişisel anahtarları siler (stash=uid verilirse önce o uid adına kaldırır). */
function clearPersonal(stashFor?: string) {
  const s = ls();
  if (!s) return;
  const keys = personalKeys(s);
  if (stashFor && keys.length) {
    const data: Record<string, string> = {};
    for (const k of keys) data[k] = s.getItem(k) ?? '';
    try {
      s.setItem(STASH_PREFIX + stashFor, JSON.stringify({ at: new Date().toISOString(), data }));
    } catch {
      // Kota: kaldırılamadı. Sızıntı riski kayıptan büyük; sunucuda son eşitlenen hali duruyor.
      console.warn('[userScope] önceki öğrencinin verisi kaldırılamadı (kota); yalnız temizlendi');
    }
  }
  for (const k of keys) s.removeItem(k);
  try {
    sessionStorage.removeItem('medsoru_scroll_pos');
  } catch {
    /* yok */
  }
}

function restoreStash(uid: string): boolean {
  const s = ls();
  const raw = s?.getItem(STASH_PREFIX + uid);
  if (!s || !raw) return false;
  try {
    const { data } = JSON.parse(raw) as { data: Record<string, string> };
    for (const [k, v] of Object.entries(data || {})) if (isPersonalKey(k)) s.setItem(k, v);
  } catch {
    /* bozuk kayıt */
  }
  s.removeItem(STASH_PREFIX + uid);
  return true;
}

/**
 * Oturum açan kişiyi verinin sahibi yapar. Alan değiştiyse true döner (çağıran sayfayı yeniden yüklemeli:
 * bellekteki React durumu hâlâ önceki öğrenciye ait).
 */
export function claimForUser(uid: string): boolean {
  const s = ls();
  if (!s || !uid) return false;
  const owner = getOwner();
  if (owner === uid) return false;

  if (owner === null) {
    // Bu sürümden önceki cihaz: veri kime ait bilinmiyor. Bu uid daha önce burada oturum açtıysa (profil
    // önbelleği / eşitleme defteri) onundur; değilse kimse adına yüklenmemesi için kaldırılır.
    let since: Record<string, string> = {};
    try {
      since = JSON.parse(s.getItem('medsoru_kv_since_v1') || '{}');
    } catch {
      /* yok */
    }
    const seenHere = !!s.getItem(`medsoru_user_profile_cache_${uid}`) || !!since[uid];
    if (!seenHere && personalKeys(s).length) {
      clearPersonal('eski-cihaz-verisi');
      setOwner(uid);
      return true;
    }
    setOwner(uid);
    return false;
  }

  if (owner === '') {
    // Oturumsuz kullanım bu kişinindi: veri hesaba geçer; varsa eski kaldırılmış verisi de birleşmez, üstüne yazmaz.
    setOwner(uid);
    return false;
  }

  // Başka bir öğrencinin verisi duruyor.
  clearPersonal(owner);
  restoreStash(uid);
  setOwner(uid);
  return true;
}

/** Oturum kapandı/sona erdi. sent=true: veri az önce sunucuya gönderildi, yerelde saklamaya gerek yok. */
export function releaseUser(sent: boolean): boolean {
  const owner = getOwner();
  if (!owner) {
    if (owner === null) setOwner('');
    return false;
  }
  clearPersonal(sent ? undefined : owner);
  setOwner('');
  return true;
}
