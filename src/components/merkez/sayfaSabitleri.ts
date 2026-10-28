/**
 * Sayfa görünürlüğünün derleme varsayılanları (bağımlılıksız; services/siteAyar.ts ile merkezModel arasında döngü olmasın).
 * Panel ayarı (Yönetim › Site › Görünürlük) bunların üstüne çalışma anında yazar.
 */
import type { AppRoute } from '../../router';

/** Gizlenenler (2026-10-27, kullanıcı kararı): menüden/merkezden kalkar, öğrenci adresle girse Bugün'e yönlenir; yönetici açabilir.
 *  Soru ekle (ana ekran) sınav günü açılır; Kurul 1 check-up/kamp, olası sorular, soru havuzu, kurul kampı, son prova, sınav spotları, ders özetleri. */
export const GIZLI_SAYFALAR = new Set<AppRoute>([
  'quick_add', 'genetik_checkup', 'patoloji_checkup', 'olasi_sorular', 'questions', 'matrix',
  'kamp', 'son_prova', 'spots', 'summaries',
]);

/** Öğrenciye kapatılan sayfalar (2026-10-21, kullanıcı kararı): yalnız yönetici adresle açabilir */
export const KAPALI_SAYFALAR = new Set<AppRoute>(['sinav_calisma', 'alternatif_cozucu', 'notes']);
