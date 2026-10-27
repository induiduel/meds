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
import { sayacBirlestir } from './basarimSayac';

export type KvRecord = { v: string | null; at: string };
export type KvMap = Record<string, KvRecord>;

/** Profilde tutulan anahtarlar (desen). Eşitleme servisinin özel birleştirdiği anahtarlar ayrı listededir. */
const SYNC_PATTERNS: RegExp[] = [
  // Öğren
  /^medsoru_learn_(progress|done|recent|layout|mode|toc|zoom|social|review|sessions)(_v1)?$/,
  /^medsoru_learn_feedback_local_v1$/,
  /^medsoru_learn_tour_(library|lesson)_v1$/,
  /^medsoru_learn_attempts_v1$/,
  /^medsoru_learn_(sort|view)$/,
  /^medsoru_lesson_day_mode$/,
  // Son Prova: aşama/check-up/deneme ilerlemesi (components/sonProva/spIlerleme.ts)
  /^medsoru_son_prova_v1$/,
  // 60 planı: günlük saat ve sınav senaryosu girdileri/sonuçları (components/takip/SinavPlani, SinavSenaryo)
  /^medsoru_sinav_(plani_saat|senaryo)_v1$/,
  // Canlı ders oynatma listesi ve tekrar tercihi
  /^medsoru_canli_ders_(liste|tekrar|varsayilan_ses|konum|vurgu|tur_ders|tur_liste)_v1$/,
  /^medsoru_canli_ders_(hiz|gorunum|tam_yazi)$/,
  // Etkinlik günlüğü: girilen sayfalar, süre, kalınan yer (etkinlikGunlugu.ts)
  /^medsoru_(etkinlik|son_konum)_v1$/,
  // Yıldızlı paragraflar (tekrar listesi) ve WhatsApp günlük tekrar tercihleri
  /^medsoru_yildizli_paragraflar(_v1)?$/,
  /^medsoru_whatsapp_prefs_v1$/,
  /^medsoru_favoriler_v1$/,
  /^medsoru_slide_drawings_v2(:.*)?$/,
  /^medsoru_annotations:.+$/,
  /^medsoru_highlights_v1$/,
  // Kartlar, sözlük, hastalıklar
  /^medsoru_card_notes_v1$/,
  // Yanlışlarım (v15 C04/C09): soru tekrar defteri (services/yanlislarim.ts)
  /^medsoru_yanlislarim_v1$/,
  // Notlarım (v15): not listesi + not başına çizim katmanı (components/v15/NotlarimV15)
  /^medsoru_notlarim_v1$/,
  // Çalışma kapsülü (v15): odak oturumu geçmişi (components/v15/KapsulV15)
  /^medsoru_v15_kapsul_v1$/,
  /^medsoru_notlarim_cizim:[a-z0-9]+$/,
  /^medsoru_card_note_open$/,
  /^medsoru_custom_encyclopedia_v1$/,
  /^medsor_(custom|favorite)_diseases_v1$/,
  // Sınav spotları, örnek/çıkmış sorular
  /^medsoru_spot_(ogrendim|ilerleme_v1|yildiz_v1)$/,
  // Öğrenci profili (üniversite, sınıf, kurul, günlük hedef)
  /^medsoru_profil_v1$/,
  /^medsoru_(sinavlarim|sinav_hatirlat)_v1$/,
  // Patoloji önem listesi: öğrendim işaretleri, ekran ve PDF tercihleri, son ders
  /^medsoru_onem_(ogrendim|tercih|pdf|asistan|asistan_tercih|son)_v1$/,
  /^medsoru_onem_ders(_[a-z0-9_]+)?$/,
  /^medsoru_cozucu_(ilerleme|tercih|istatistik)_v1$/,
  /^medsoru_alt_cozucu_(v1|tercih_v1)$/,
  // Sınav Çalışması: kazanım başına çözülen sorular
  /^medsoru_sinav_calisma_(v2|son_v1)$/,
  /^medsoru_checkup_v1$/,
  /^medsoru_genetik_checkup_(v1|answers_v1)$/,
  /^medsoru_genetik_anlatici_(adim|soru|tamam)_v1$/,
  /^medsoru_genetik_kamp_v1$/,
  // Kurul kampı: dinlenen anlatım, deneme cevapları, kalıp kartı "bildim" (components/kamp/kampIlerleme.ts)
  /^medsoru_kamp_v1$/,
  // Başarım: gün başına çözülen soru (basarimSayac.ts)
  /^medsoru_basarim_sayac_v1$/,
  /^medsoru_(test_kriter_v1|pdf_sel_v1|saglik_sina_v1|quickadd_draft_v1|nav_recent_v1)$/,
  /^medsoru_(cikmis_gorunum|pool_segment|saglik_gorunum|saglik_yogunluk|r12_reader)$/,
  /^medsoru_calisma_takip_v1$/,
  // Bitirdiklerim / Sınav planı: kalan süre hesabındaki izleme hızı (calismaTakip.izlemeHizi)
  /^medsoru_izleme_hizi_v1$/,
  // Bitirdiklerim: çalışmayacağım / sınavda sorusu yok işaretleri (konuEleme.ts)
  /^medsoru_konu_eleme_v1$/,
  /^medsoru_ornek_(k1_cevap|k1_ders|k1_social|havuz_social|sekme)$/,
  /^cikmis_quiz$/,
  /^my_(comment|report)_ids$/,
  // Ders özetleri / okuyucu
  /^medsoru_summary_progress$/,
  // İlerleme sıfırlamasında korunan istatistik arşivi
  /^medsoru_stats_archive_v1$/,
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
  /^medsoru_cikmis_kayitli_gorunumler$/,
  /^medsoru_solve_drawer$/,
  /^medsoru_study_section$/,
  /^medsoru_rail_collapsed$/,
  /^medsoru_tabbar_v1$/,
  /^medsoru_last_(committee_id|discipline|status)$/,
  /^medsoru_pdf_(page|q|l|s)_v2$/,
  /^tc_layout$/,
  /^medsor_love_note_hidden_v1$/,
  // Hoş geldin turu görüldü mü
  /^medsoru_tour_v1$/,
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
  'medsoru_progress_reset_v1',
]);
/** Sık yazılan sayaçlar: profile girer ama anlık gönderim tetiklemez (dönemsel/arka plana geçişte gider). */
const QUIET_KEYS = new Set(['medsoru_study_seconds_v1', 'medsoru_activity_v1']);
/** Ders okurken her adımda/harekette yazılan profil anahtarları: damgalanır ama dönemsel gönderime kalır. */
const QUIET_PROFILE = /^medsoru_(learn_(progress|done|zoom|review|attempts)(_v1)?|calisma_takip_v1|canli_ders_konum_v1|genetik_anlatici_adim_v1|genetik_kamp_v1|kamp_v1|etkinlik_v1|son_konum_v1|basarim_sayac_v1)$/;

const META_KEY = 'medsoru_kv_meta_v1'; // anahtar → son yerel değişiklik zamanı
const DIRTY_KEY = 'medsoru_kv_dirty_v1'; // henüz sunucuya gitmemiş anahtarlar
const MAX_VALUE = 2_000_000; // sunucudaki sınırla aynı

/**
 * Cihaza özgü görünüm/düzen tercihleri: profile eşitlenmez, her cihaz (telefon, tablet, bilgisayar) kendi
 * ayarını saklar — yoksa telefondaki değişiklik bilgisayarın görünümünü eziyordu. Sunucudaki eski kopyaları da uygulanmaz.
 */
export const DEVICE_PREFS = /^(medsoru_appearance|medsoru_theme|medsoru_rail_collapsed|medsoru_tabbar_v1|medsoru_learn_(layout|mode|toc|zoom)|medsoru_lesson_day_mode|medsoru_(glossary|search|studio)_view|medsoru_reader_prefs|tc_layout|medsoru_auto_reveal|medsoru_solve_drawer|medsoru_study_section|medsoru_music_volume_v1|medsoru_card_note_open|medsoru_canli_ders_(gorunum|tam_yazi)|medsoru_(cikmis_gorunum|cikmis_mod|saglik_gorunum|saglik_yogunluk|r12_reader))$/;
export const isProfileKey = (key: string): boolean => !DEVICE_PREFS.test(key) && SYNC_PATTERNS.some((re) => re.test(key));
/** Öğrenciye ait (profil, paket ya da sayaç) anahtar mı — oturum değişince ayrılır (userScope). */
export const isUserDataKey = (key: string): boolean => isProfileKey(key) || BUNDLE_KEYS.has(key) || QUIET_KEYS.has(key);

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
    const immediate = !QUIET_PROFILE.test(key);
    changeListeners.forEach((fn) => fn(immediate));
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
    // Ekran açılışında aynı değerle yeniden yazılan tercihler değişiklik sayılmaz (gereksiz gönderim + SSE yayını)
    const same = this === s && proto.getItem.call(this, k) === String(v);
    origSet.call(this, k, v);
    if (this === s && !same) {
      try {
        onWrite(String(k));
      } catch {
        /* izleme asla yazmayı bozmaz */
      }
    }
  };
  proto.removeItem = function (this: Storage, k: string) {
    const absent = this === s && proto.getItem.call(this, k) === null;
    origRemove.call(this, k);
    if (this === s && !absent) {
      try {
        onWrite(String(k));
      } catch {
        /* yoksay */
      }
    }
  };
}

/** Henüz sunucuya gitmemiş profil anahtarı sayısı (çevrimdışı merkezi eşitleme kartı) */
export const dirtyKvCount = (): number => Object.keys(readObj(DIRTY_KEY)).length;

/** Profil verisi değişince haber ver (`immediate`: birkaç saniye içinde gönder; değilse dönemsel gönderime bırak). */
export function onProfileDataChange(fn: (immediate: boolean) => void): () => void {
  changeListeners.add(fn);
  return () => changeListeners.delete(fn);
}

export function hasDirtyKv(): boolean {
  return Object.keys(readObj(DIRTY_KEY)).length > 0;
}

/** Asla `v: null` mezar taşıyla silinmemesi gereken birikimli öğrenci ilerleme/içerik anahtarları. */
const PROTECTED_PROGRESS_RE =
  /^(medsoru_(calisma_takip_v1|cozucu_(ilerleme|istatistik|tercih)_v1|alt_cozucu_(v1|tercih_v1)|onem_(asistan|asistan_tercih|ogrendim|tercih|pdf|son)_v1|onem_ders(_[a-z0-9_]+)?|spot_(ilerleme_v1|ogrendim|yildiz_v1)|profil_v1|learn_(progress|done|recent|review|sessions)(_v1)?|sinav_calisma_v2|checkup_v1|yildizli_paragraflar(_v1)?|whatsapp_prefs_v1|canli_ders_liste_v1|ornek_(k1_cevap|k1_ders)|summary_progress|stats_archive_v1|highlights_v1|card_notes_v1|custom_encyclopedia_v1|saved_(contributor_name|student_number)|pdf_(page|q|l|s)_v2)|cikmis_quiz|medsor_(custom|favorite)_diseases_v1)$/;

export const isProtectedProgressKey = (key: string): boolean => PROTECTED_PROGRESS_RE.test(key);

/**
 * İki cihazda da JSON nesnesi/dizisi tutan birikimli ilerleme anahtarlarını veri kaybetmeden birleştirir.
 * `olderRaw` ve `newerRaw` ikisi de dolu dizge olduğunda çağrılır; ayrıştırılamazsa `newerRaw` döner.
 */
export function mergeKvJsonValue(key: string, olderRaw: string, newerRaw: string): string {
  if (!olderRaw || !newerRaw || olderRaw === newerRaw) return newerRaw || olderRaw;
  try {
    if (key === 'medsoru_basarim_sayac_v1') return sayacBirlestir(olderRaw, newerRaw);
    if (key === 'medsoru_calisma_takip_v1') {
      const a = JSON.parse(olderRaw);
      const b = JSON.parse(newerRaw);
      if (!a || typeof a !== 'object' || !b || typeof b !== 'object') return newerRaw;
      const ak = a.k && typeof a.k === 'object' ? a.k : {};
      const bk = b.k && typeof b.k === 'object' ? b.k : {};
      const k: Record<string, any> = { ...ak };
      for (const [id, rec] of Object.entries(bk) as [string, any][]) {
        const cur = k[id];
        if (!cur || typeof cur !== 'object' || !rec || typeof rec !== 'object') {
          k[id] = rec;
          continue;
        }
        const aTime = String(cur.sonAt || cur.bittiAt || cur.ilkAt || '');
        const bTime = String(rec.sonAt || rec.bittiAt || rec.ilkAt || '');
        const [lo, hi] = bTime >= aTime ? [cur, rec] : [rec, cur];
        // Yönetici düzeltmesi (adm): düzeltmeden sonra çalışılmadıysa süre/soru en büyüğe değil düzeltilmiş değere eşitlenir
        const admWins = !!hi.adm && String(hi.adm) >= String(lo.sonAt || lo.bittiAt || lo.ilkAt || '');
        const merged: Record<string, any> = {
          ...lo,
          ...hi,
          sn: admWins ? Number(hi.sn) || 0 : Math.max(Number(cur.sn) || 0, Number(rec.sn) || 0),
          soru: admWins ? Number(hi.soru) || 0 : Math.max(Number(cur.soru) || 0, Number(rec.soru) || 0),
        };
        const tur = admWins ? Number(hi.tur) || 0 : Math.max(Number(cur.tur) || 0, Number(rec.tur) || 0);
        if (tur > 0) merged.tur = tur;
        const ilkAt = cur.ilkAt && rec.ilkAt ? (cur.ilkAt < rec.ilkAt ? cur.ilkAt : rec.ilkAt) : cur.ilkAt || rec.ilkAt;
        if (ilkAt) merged.ilkAt = ilkAt;
        const sonAt = cur.sonAt && rec.sonAt ? (cur.sonAt > rec.sonAt ? cur.sonAt : rec.sonAt) : cur.sonAt || rec.sonAt;
        if (sonAt) merged.sonAt = sonAt;
        if (!admWins && hi.durum === undefined && lo.durum === 'bitti') {
          merged.durum = 'bitti';
          if (lo.bittiAt) merged.bittiAt = lo.bittiAt;
        }
        k[id] = merged;
      }
      const ag = a.g && typeof a.g === 'object' ? a.g : {};
      const bg = b.g && typeof b.g === 'object' ? b.g : {};
      const g: Record<string, Record<string, number>> = {};
      for (const m of new Set([...Object.keys(ag), ...Object.keys(bg)])) {
        const ma = ag[m] && typeof ag[m] === 'object' ? ag[m] : {};
        const mb = bg[m] && typeof bg[m] === 'object' ? bg[m] : {};
        const mg: Record<string, number> = { ...ma };
        for (const [d, s] of Object.entries(mb)) mg[d] = Math.max(Number(mg[d]) || 0, Number(s) || 0);
        g[m] = mg;
      }
      return JSON.stringify({ k, g });
    }

    if (key === 'medsoru_cozucu_ilerleme_v1') {
      const a = JSON.parse(olderRaw);
      const b = JSON.parse(newerRaw);
      if (!a || typeof a !== 'object' || !b || typeof b !== 'object') return newerRaw;
      const out: Record<string, any> = { ...a };
      for (const [kod, rec] of Object.entries(b) as [string, any][]) {
        const cur = out[kod];
        if (!cur || typeof cur !== 'object' || !rec || typeof rec !== 'object') {
          out[kod] = rec;
          continue;
        }
        const [lo, hi] = String(rec.at || '') >= String(cur.at || '') ? [cur, rec] : [rec, cur];
        out[kod] = {
          ...lo,
          ...hi,
          s: { ...(lo.s && typeof lo.s === 'object' ? lo.s : {}), ...(hi.s && typeof hi.s === 'object' ? hi.s : {}) },
        };
      }
      return JSON.stringify(out);
    }

    if (key === 'medsoru_alt_cozucu_v1') {
      const a = JSON.parse(olderRaw);
      const b = JSON.parse(newerRaw);
      if (!a || typeof a !== 'object' || !b || typeof b !== 'object') return newerRaw;
      const out: Record<string, any> = { ...a };
      for (const [kod, rec] of Object.entries(b) as [string, any][]) {
        const cur = out[kod];
        if (!cur || typeof cur !== 'object' || !rec || typeof rec !== 'object') {
          out[kod] = rec;
          continue;
        }
        const [lo, hi] = (Number(rec.son) || 0) >= (Number(cur.son) || 0) ? [cur, rec] : [rec, cur];
        const bitti = Array.from(new Set([...(Array.isArray(lo.bitti) ? lo.bitti : []), ...(Array.isArray(hi.bitti) ? hi.bitti : [])]));
        const ilkDogru = Array.from(new Set([...(Array.isArray(lo.ilkDogru) ? lo.ilkDogru : []), ...(Array.isArray(hi.ilkDogru) ? hi.ilkDogru : [])]));
        const incelenen = Array.from(new Set([...(Array.isArray(lo.incelenen) ? lo.incelenen : []), ...(Array.isArray(hi.incelenen) ? hi.incelenen : [])]));
        out[kod] = {
          ...lo,
          ...hi,
          bitti,
          ilkDogru,
          incelenen,
          secim: { ...(lo.secim && typeof lo.secim === 'object' ? lo.secim : {}), ...(hi.secim && typeof hi.secim === 'object' ? hi.secim : {}) },
        };
      }
      return JSON.stringify(out);
    }

    if (key === 'medsoru_onem_asistan_v1') {
      const a = JSON.parse(olderRaw);
      const b = JSON.parse(newerRaw);
      if (!a || typeof a !== 'object' || !b || typeof b !== 'object') return newerRaw;
      const out: Record<string, any> = { ...a };
      for (const [kod, rec] of Object.entries(b) as [string, any][]) {
        const cur = out[kod];
        if (!cur || typeof cur !== 'object' || !rec || typeof rec !== 'object') {
          out[kod] = rec;
          continue;
        }
        const [lo, hi] = String(rec.at || '') >= String(cur.at || '') ? [cur, rec] : [rec, cur];
        out[kod] = {
          ...lo,
          ...hi,
          sonuc: { ...(lo.sonuc && typeof lo.sonuc === 'object' ? lo.sonuc : {}), ...(hi.sonuc && typeof hi.sonuc === 'object' ? hi.sonuc : {}) },
        };
      }
      return JSON.stringify(out);
    }

    if (key === 'medsoru_cozucu_istatistik_v1' || key === 'medsoru_spot_ilerleme_v1') {
      const a = JSON.parse(olderRaw);
      const b = JSON.parse(newerRaw);
      if (!a || typeof a !== 'object' || !b || typeof b !== 'object') return newerRaw;
      return JSON.stringify({
        ...a,
        ...b,
        sureSn: Math.max(Number(a.sureSn) || 0, Number(b.sureSn) || 0),
      });
    }

    if (key === 'medsoru_learn_progress_v1') {
      const a = JSON.parse(olderRaw);
      const b = JSON.parse(newerRaw);
      if (!a || typeof a !== 'object' || !b || typeof b !== 'object') return newerRaw;
      const out: Record<string, any> = { ...a };
      for (const [id, rec] of Object.entries(b) as [string, any][]) {
        const cur = out[id];
        if (!cur || typeof cur !== 'object' || !rec || typeof rec !== 'object') {
          out[id] = rec;
          continue;
        }
        const seen = Array.from(
          new Set([...(Array.isArray(cur.seen) ? cur.seen : []), ...(Array.isArray(rec.seen) ? rec.seen : [])])
        ).sort((x: number, y: number) => x - y);
        const last = typeof rec.last === 'number' && rec.last > 0 ? rec.last : typeof cur.last === 'number' ? cur.last : 0;
        out[id] = { ...cur, ...rec, last, seen };
      }
      return JSON.stringify(out);
    }

    if (key === 'medsoru_yildizli_paragraflar_v1' || key === 'medsoru_yildizli_paragraflar') {
      const a = JSON.parse(olderRaw);
      const b = JSON.parse(newerRaw);
      if (!Array.isArray(a) || !Array.isArray(b)) return newerRaw;
      if (b.length === 0 && a.length > 0) return olderRaw;
      const byId = new Map<string, any>();
      for (const item of [...a, ...b]) {
        if (!item || typeof item !== 'object' || !item.id) continue;
        // Aynı kimlikte en yeni işlem (ekleme ya da silme mezar taşı) kazanır.
        const cur = byId.get(String(item.id));
        if (!cur || (Number(item.tarih) || 0) >= (Number(cur.tarih) || 0)) byId.set(String(item.id), item);
      }
      return JSON.stringify(Array.from(byId.values()).sort((x, y) => (Number(y?.tarih) || 0) - (Number(x?.tarih) || 0)));
    }

    if (key === 'medsoru_ornek_k1_cevap' || key === 'medsoru_sinav_calisma_v2' || key === 'medsoru_summary_progress' || key === 'medsoru_learn_recent_v1') {
      const a = JSON.parse(olderRaw);
      const b = JSON.parse(newerRaw);
      if (a && typeof a === 'object' && !Array.isArray(a) && b && typeof b === 'object' && !Array.isArray(b)) {
        return JSON.stringify({ ...a, ...b });
      }
    }
  } catch {
    /* JSON değilse doğrudan yeni değer kullanılır */
  }
  return newerRaw;
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
    for (const k of Object.keys(meta)) if (isProfileKey(k) && !isProtectedProgressKey(k)) keys.add(k);
  }
  for (const k of keys) {
    if (!isProfileKey(k)) continue;
    const v = s.getItem(k);
    if (v === null && isProtectedProgressKey(k)) continue;
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
 * Sunucudan gelen kv'yi uygula: yalnız sunucudaki kayıt yereldekinden yeniyse (veya yerelde anahtar boşken sunucuda
 * doluysa) yazılır. Değişen anahtarlar için `storage` olayı yayınlanır (aynı sekmedeki dinleyiciler de güncellensin).
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
      const cur = s.getItem(k);
      if (r.v == null) {
        if (isProtectedProgressKey(k)) continue;
        if (at <= (meta[k] || '')) continue;
        if (cur != null) {
          (rawRemove || s.removeItem).call(s, k);
          changed.push(k);
        }
        meta[k] = at;
        delete dirty[k];
        continue;
      }
      // Sunucuda dolu veri var: yerelde boşsa (ör. çıkış sonrası mezar taşı kalmışsa) zaman damgasına bakmadan geri yükle;
      // yerelde de doluysa zamanı yeni olan kazanır ve birikimli JSON anahtarları birleştirilir.
      const localAt = meta[k] || '';
      if (cur != null && at < localAt) continue;
      const nextVal = cur != null ? mergeKvJsonValue(k, cur, r.v) : r.v;
      if (cur !== nextVal) {
        (rawSet || s.setItem).call(s, k, nextVal);
        changed.push(k);
      }
      if (at >= localAt) meta[k] = at;
      delete dirty[k];
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
