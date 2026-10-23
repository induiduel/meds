/**
 * Merkez sayfaları ve bölüm şeridinin modeli (2026-10-21): öğrenci "ne yapmak istiyorum" sorusuyla dört kategoriden
 * birine girer; kategori sayfası araçları "ne zaman kullanılır" cümlesiyle sıralar. Kenar menüsü grupları
 * (shell/navModel NAV_TREE) aynı sırayı izler. Adresler: siteHaritasi.ts; kurallar docs/SITE_HARITASI_KURALLARI.md.
 */
import type { AppRoute } from '../../router';
import type { KategoriId } from '../../siteHaritasi';

export interface MerkezArac {
  id: AppRoute;
  /** Öğrenciye: bu aracı ne zaman açmalıyım */
  ne: string;
  /** Kategorinin önerilen ilk adımı */
  oner?: boolean;
}

export const MERKEZ_ARACLARI: Record<KategoriId, MerkezArac[]> = {
  dersler: [
    { id: 'canli_ders', ne: 'Dersi baştan sona dinlemek istiyorsan: metin ve slayt sesle akar', oner: true },
    { id: 'learn', ne: 'Konuyu adım adım, mini sorularla öğrenmek istiyorsan' },
    { id: 'summaries', ne: 'Kısa sürede konunun özetini okumak istiyorsan' },
    { id: 'flashcards', ne: 'Öğrendiklerini aralıklı tekrarla ezberlemek istiyorsan' },
  ],
  sorular: [
    { id: 'soru_cozucu', ne: 'Konu konu soru çözüp her şıkkın nedenini dinlemek istiyorsan', oner: true },
    { id: 'past_exams', ne: 'Geçmiş yılların sorularını görmek istiyorsan' },
    { id: 'practice', ne: 'Süreli bir sınav provası yapmak istiyorsan' },
    { id: 'questions', ne: 'Bu yılın sınavından hatırlananları birlikte kurmak istiyorsan' },
    { id: 'ornek_sorular', ne: 'Kazanım kazanım örnek soru çözmek istiyorsan' },
    { id: 'olasi_sorular', ne: 'Sınavdan sonra kurulan olası soruları çözmek istiyorsan' },
  ],
  kamplar: [
    { id: 'sinav_plani', ne: 'En az 60 için nereye ne kadar çalışacağını gün gün görmek istiyorsan' },
    { id: 'son_prova', ne: 'Sınavdan önceki son günlerde kurulun tamamını sesli özetle bitirmek istiyorsan', oner: true },
    { id: 'cikmis_cozucu', ne: 'Sınavdaki soru sayısı kadar çıkmış paketini sesli asistanla birlikte çözmek istiyorsan' },
    { id: 'kamp', ne: 'Hocanın derste verdiği ipuçlarından hızlı tekrar yapmak istiyorsan' },
    { id: 'en_onemliler', ne: 'Konu başına en önemli bilgileri puan sırasıyla görmek istiyorsan' },
    { id: 'spots', ne: 'Sık sorulan bulguları ve tuzakları taramak istiyorsan' },
  ],
  kaynaklar: [
    { id: 'oncelikli_dersler', ne: 'Az ezberli, mantıkla çözülen ve kolay puan getiren sesli derslerden başlamak istiyorsan', oner: true },
    { id: 'glossary', ne: 'Bir terimin, ilacın ya da kavramın anlamına bakmak istiyorsan' },
    { id: 'diseases', ne: 'Bir hastalığın kliniğini, tanısını ve tedavisini görmek istiyorsan' },
    { id: 'health_ministry', ne: 'Aşı takvimi, tarama programları gibi resmî verilere bakmak istiyorsan' },
    { id: 'kazanimlar', ne: 'Müfredatta hangi kazanımın olduğunu görmek istiyorsan' },
    { id: 'gecmis_kurullar', ne: 'Sınavı biten kurulların içeriğine dönmek istiyorsan' },
    { id: 'guncellemeler', ne: 'Sitede nelerin değiştiğini görmek istiyorsan' },
  ],
};

/** Check Up sınamaları: kamplar merkezinde ayrı sekme; her biri kendi adresinde */
export interface CheckUpTanim { id: string; ad: string; alt: string; yol: string; kurul: number; surum?: string; route: AppRoute }
export const CHECKUPLAR: CheckUpTanim[] = [
  {
    id: 'tbg', ad: 'TBG Sınav Kampı', surum: 'v1', kurul: 1, route: 'genetik_checkup', yol: '/kamplar/kurul1/checkup/tbg/v1/sesli-ders',
    alt: 'Tıbbi Biyoloji ve Genetik: sesli ders, soru çözerek tekrar, kalıp kartları ve 12 soruluk deneme ayrı sayfalarda',
  },
  {
    id: 'patoloji', ad: 'Patoloji Check Up', kurul: 1, route: 'patoloji_checkup', yol: '/kamplar/kurul1/checkup/patoloji',
    alt: 'Mediyatör, sitokin, hücre ve hastalık karşılaştırma tabloları; kendini sına',
  },
];

/** PDF notlar: kamplar merkezinde (Hepsi + En önemliler) indirilebilir tek dosyalık özetler; dosya public/pdf/ */
export interface PdfNotTanim { id: string; ad: string; alt: string; dosya: string; kurul: number; sayfa: number }
export const PDF_NOTLAR: PdfNotTanim[] = [
  {
    id: 'halk-sagligi-k1', kurul: 1, sayfa: 14, dosya: '/pdf/halk-sagligi-kurul1-sayisal-notlar.pdf',
    ad: 'Halk Sağlığı: sayısal veriler ve önemli notlar',
    alt: '7 dersin tüm slaytlarından; kişiler, buluşlar, sayılar tek satır halinde, çıkmışta sorulanlar işaretli',
  },
];

/** Bir sayfanın kategorisi (bölüm şeridi ve merkez bağlantısı için); kategorisizse null */
export function kategoriOf(route: AppRoute): KategoriId | null {
  if (route === 'genetik_checkup' || route === 'patoloji_checkup') return 'kamplar';
  for (const [k, l] of Object.entries(MERKEZ_ARACLARI) as [KategoriId, MerkezArac[]][]) if (l.some((a) => a.id === route)) return k;
  return null;
}

export const MERKEZ_ROUTE: Record<KategoriId, AppRoute> = {
  dersler: 'hub_dersler', sorular: 'hub_sorular', kamplar: 'hub_kamplar', kaynaklar: 'hub_kaynaklar',
};

/** Öğrenciye kapatılan sayfalar (2026-10-21, kullanıcı kararı): yalnız yönetici adresle açabilir */
export const KAPALI_SAYFALAR = new Set<AppRoute>(['sinav_calisma', 'alternatif_cozucu', 'notes']);
