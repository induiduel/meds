import {
  Medal,
  Activity,
  Archive,
  History,
  Tent,
  ScrollText,
  Sparkles,
  AudioLines,
  CircleCheckBig,
  CloudDownload,
  ClipboardCheck,
  Dna,
  Flag,
  Headphones,
  MessageCircleQuestion,
  Star,
  Table2,
  BookOpen,
  BookOpenText,
  Compass,
  Crosshair,
  GraduationCap,
  Landmark,
  LayoutGrid,
  Layers,
  Library,
  ListChecks,
  Music,
  BarChart3,
  NotebookPen,
  Timer,
  Settings2,
  SquarePen,
  Sun,
  Target,
  Trophy,
} from 'lucide-react';
import type React from 'react';
import type { AppRoute } from '../../router';

/**
 * v8 kabuğunun tek gezinme modeli: kenar menüsü, alt gezinme ve "Daha" sayfası buradan beslenir.
 * `tint`: Apple Ayarlar tarzı simge karosu rengi (yalnız "Daha" ve hesap listelerinde).
 */
export interface NavItem {
  id: AppRoute;
  label: string;
  short?: string;
  /** Telefon "Tüm sayfalar" döşemesi (iki satıra kadar); yoksa label */
  tile?: string;
  hint: string;
  icon: React.ElementType;
  tint: string;
}
export interface NavGroup {
  label: string | null;
  items: NavItem[];
}

const I: Record<string, NavItem> = {
  today: { id: 'today', label: 'Bugün', hint: 'Kaldığın yer, günün spotu, haftan', icon: Sun, tint: '#FF9F0A' },
  quick_add: { id: 'quick_add', label: 'Soru ekle', short: 'Ekle', hint: 'Hatırladığın parçayı gir', icon: SquarePen, tint: '#FF2D55' },
  // Ders çalış
  learn: { id: 'learn', label: 'Etkileşimli dersler', short: 'Öğren', tile: 'Etkileşimli ders', hint: 'Adım adım ders desteleri, mini sorular', icon: GraduationCap, tint: '#AF52DE' },
  canli_ders: { id: 'canli_ders', label: 'Sesli ders', short: 'Sesli', hint: 'Dersi dinle; metin ve slayt sesle akar, MP3 indir', icon: AudioLines, tint: '#30B0C7' },
  notes: { id: 'notes', label: 'Ders notları', short: 'Notlar', hint: 'Amfi slaytları ve ders notları', icon: NotebookPen, tint: '#FF9F0A' },
  summaries: { id: 'summaries', label: 'Ders özetleri', short: 'Özetler', hint: 'Konu konu kısa özet, uzun okuma', icon: BookOpen, tint: '#FF6B3D' },
  flashcards: { id: 'flashcards', label: 'Ezber kartları', short: 'Kartlar', hint: 'Aralıklı tekrar', icon: Layers, tint: '#32ADE6' },
  // Sınava hazırlan
  sinav_calisma: { id: 'sinav_calisma', label: 'Sınav çalışması', short: 'Sınav', tile: 'Sınav çalışması', hint: 'Kazanım kazanım özet, örnek ve çıkmış sorular', icon: ClipboardCheck, tint: '#8B5CF6' },
  soru_cozucu: { id: 'soru_cozucu', label: 'Soru çözücü', short: 'Çözücü', hint: 'Sesli asistanla soru çöz, nedenini dinle', icon: MessageCircleQuestion, tint: '#0EA5E9' },
  alternatif_cozucu: { id: 'alternatif_cozucu', label: 'Alternatif çözücü', short: 'Alternatif', hint: 'Her soru baştan sona sesli anlatılır, otomatik geçer', icon: Headphones, tint: '#6366F1' },
  en_onemliler: { id: 'en_onemliler', label: 'En önemliler', short: 'Önemli', hint: 'Konu başına en önemli bilgiler, 100 puan', icon: Star, tint: '#F59E0B' },
  patoloji_checkup: { id: 'patoloji_checkup', label: 'Patoloji Check Up', short: 'Check Up', tile: 'Patoloji Check Up', hint: 'Mediyatör, sitokin, hücre ve hastalık tabloları; kendini sına', icon: Table2, tint: '#14B8A6' },
  son_prova: { id: 'son_prova', label: 'Son Prova', short: 'Prova', tile: 'Son Prova', hint: 'Kurulun tüm dersleri sesli özetle, aşama soruları, check-up ve 100 soruluk 3 deneme', icon: Flag, tint: '#E11D48' },
  genetik_checkup: { id: 'genetik_checkup', label: 'TBG Check Up', short: 'TBG', tile: 'TBG Check Up', hint: 'TBG Sınav Kampı v1: sesli ders, soru çözerek tekrar, kalıp kartları, deneme — her biri ayrı sayfa', icon: Dna, tint: '#10B981' },
  kamp: { id: 'kamp', label: 'Kurul kampı', short: 'Kamp', tile: 'Kurul kampı', hint: 'Hocanın derste verdiği ipuçlarından hızlı tekrar: sesli anlatım, kalıp kartları, deneme', icon: Tent, tint: '#EA580C' },
  spots: { id: 'spots', label: 'Sınav spotları', short: 'Spotlar', hint: 'En sık, ayırıcı bulgular, tuzaklar', icon: Crosshair, tint: '#FF3B30' },
  // Soru çöz
  past_exams: { id: 'past_exams', label: 'Çıkmış sorular', short: 'Çıkmış', hint: 'Kurullara göre çıkmışlar', icon: Archive, tint: '#007AFF' },
  questions: { id: 'questions', label: 'Soru havuzu', short: 'Havuz', hint: 'Öğrencilerin birlikte kurduğu kurul soruları', icon: Library, tint: '#5856D6' },
  ornek_sorular: { id: 'ornek_sorular', label: 'Örnek sorular', short: 'Örnek', hint: 'Kazanım temelli sorular', icon: Target, tint: '#FF9500' },
  olasi_sorular: { id: 'olasi_sorular', label: 'Olası sorular', short: 'Olası', hint: 'Sınavdan sonra hatıralardan kurulan sorular; çöz, doğrula', icon: Sparkles, tint: '#AF52DE' },
  practice: { id: 'practice', label: 'Deneme sınavı', short: 'Deneme', hint: 'Süreli deneme sınavı', icon: Timer, tint: '#0A84FF' },
  // Başvuru
  glossary: { id: 'glossary', label: 'Sözlük', hint: 'Hastalık ve ilaç ansiklopedisi', icon: BookOpenText, tint: '#A2845E' },
  diseases: { id: 'diseases', label: 'Hastalıklar', short: 'Atlas', hint: 'Tıbbi hastalık ve klinik atlası', icon: Activity, tint: '#06B6D4' },
  health_ministry: { id: 'health_ministry', label: 'Sağlık Bakanlığı', short: 'Bakanlık', hint: 'Resmî veriler: aşı, yenidoğan, anne, tarama, salgın, Karabük', icon: Landmark, tint: '#C8102E' },
  gecmis_kurullar: { id: 'gecmis_kurullar', label: 'Geçmiş kurullar', short: 'Geçmiş', tile: 'Geçmiş kurullar', hint: 'Sınavı biten kurulların dersleri, spotları ve soruları', icon: History, tint: '#8E8E93' },
  guncellemeler: { id: 'guncellemeler', label: 'Güncelleme günlüğü', short: 'Sürümler', tile: 'Güncellemeler', hint: 'Her sürümde eklenen, değişen ve kaldırılanlar', icon: ScrollText, tint: '#5E5CE6' },
  kazanimlar: { id: 'kazanimlar', label: 'Kazanımlar', hint: 'Müfredat ve kazanım haritası', icon: Compass, tint: '#00A79D' },
  // Topluluk
  matrix: { id: 'matrix', label: 'Soru haritası', short: 'Harita', hint: 'Havuzda 1–100 soru doluluğu', icon: LayoutGrid, tint: '#64748B' },
  leaderboard: { id: 'leaderboard', label: 'Sıralama', hint: 'Dönemindeki haftalık ve kurul sıralaması', icon: Trophy, tint: '#FFB340' },
  // Kişisel
  study: { id: 'study', label: 'Çalışma masam', short: 'Masam', tile: 'Çalışma masam', hint: 'Kendi listelerin, notların, hızlı test', icon: ListChecks, tint: '#34C759' },
  cevrimdisi: { id: 'cevrimdisi', label: 'Çevrimdışı', short: 'Çevrimdışı', tile: 'Çevrimdışı', hint: 'Dersleri cihaza indir, internetsiz çalış; indirilenleri yönet', icon: CloudDownload, tint: '#0A84FF' },
  basarimlar: { id: 'basarimlar', label: 'Başarımlar', short: 'Başarım', tile: 'Başarımlar', hint: 'Günlük, haftalık, kurul hedefleri; başarımlar, puan ve ATP', icon: Medal, tint: '#FF9F0A' },
  bitirdiklerim: { id: 'bitirdiklerim', label: 'Bitirdiklerim', short: 'Bitenler', tile: 'Bitirdiklerim', hint: 'Konu konu bitenler, harcanan süre, kalanların tahmini', icon: CircleCheckBig, tint: '#30D158' },
  stats: { id: 'stats', label: 'İstatistiklerim', short: 'İstatistik', tile: 'İstatistik', hint: 'İlerleme, puan ve etkinlik', icon: BarChart3, tint: '#5E5CE6' },
  music: { id: 'music', label: 'Müzik', hint: 'Çalışırken dinle', icon: Music, tint: '#FF375F' },
  settings: { id: 'settings', label: 'Profil ve ayarlar', short: 'Ayarlar', hint: 'Tema, palet, yoğunluk, fotoğraf', icon: Settings2, tint: '#8E8E93' },
};

export const NAV_ITEMS = I;

/**
 * Menü grupları (2026-10-21, siteHaritasi.ts ile aynı şema): öğrencinin "ne yapmak istiyorum" sorusuna göre
 *   DERS ÇALIŞ (/dersler) → SORU ÇÖZ (/sorular) → SINAVA HAZIRLAN (/kamplar) → CHECK UP (/kamplar/kurulN/checkup)
 *   → BAŞVURU (/kaynaklar) → TOPLULUK → KİŞİSEL.
 * Grup içi sıra components/merkez/merkezModel.ts MERKEZ_ARACLARI ile aynıdır (önerilen ilk adım başta).
 * Öğrenciye kapatılan sayfalar (Sınav çalışması, Alternatif çözücü, Ders notları) menüde yoktur (merkezModel.KAPALI_SAYFALAR).
 * "Soru ekle" menünün tepesinde tek başına duran birincil düğmedir; telefonda alt gezinmenin ortasındadır.
 */
export const NAV_TREE: NavGroup[] = [
  { label: null, items: [I.today] },
  { label: 'Ders çalış', items: [I.canli_ders, I.learn, I.summaries, I.flashcards] },
  { label: 'Soru çöz', items: [I.soru_cozucu, I.past_exams, I.practice, I.questions, I.ornek_sorular, I.olasi_sorular] },
  { label: 'Sınava hazırlan', items: [I.son_prova, I.kamp, I.en_onemliler, I.spots] },
  { label: 'Check Up', items: [I.genetik_checkup, I.patoloji_checkup] },
  { label: 'Başvuru', items: [I.glossary, I.diseases, I.health_ministry, I.kazanimlar, I.gecmis_kurullar, I.guncellemeler] },
  { label: 'Topluluk', items: [I.basarimlar, I.leaderboard, I.matrix] },
  { label: 'Kişisel', items: [I.bitirdiklerim, I.cevrimdisi, I.study, I.stats, I.music] },
];

/** Telefonda alt gezinmede doğrudan duran sayfalar (v10 sıra: Ekle · Öğren · Havuz · Çıkmış); gerisi "Daha" sayfasında */
export const TAB_ITEMS: NavItem[] = [I.quick_add, I.learn, I.questions, I.past_exams];

/** "Daha" sayfası: alt gezinmede olmayanlar, aynı gruplar ve sırayla */
export const MORE_TREE: NavGroup[] = NAV_TREE.map((g) => ({ ...g, items: g.items.filter((it) => !TAB_ITEMS.includes(it)) })).filter((g) => g.items.length > 0);

/**
 * v12 "Net" gezinmesi (components/v12/ShellV12). Kenar menüsü NAV_TREE gruplarını aynı adlarla gösterir; her grupta
 * en sık sayfalar (V12_RAIL_IDS) doğrudan görünür, gerisi "Daha fazla" açılırında yine kendi grup adıyla.
 * Telefonda alt çubuk: Bugün · Öğren · [+ Soru ekle] · Çıkmış · Daha.
 */
const V12_RAIL_IDS = new Set<AppRoute>([
  'today',
  'canli_ders', 'learn', 'summaries', 'flashcards',
  'soru_cozucu', 'past_exams', 'practice', 'questions', 'olasi_sorular',
  'son_prova', 'kamp', 'en_onemliler', 'spots',
  'genetik_checkup', 'patoloji_checkup',
  'glossary', 'diseases',
  'bitirdiklerim', 'cevrimdisi', 'basarimlar',
]);
const grupSuz = (keep: (it: NavItem) => boolean): NavGroup[] =>
  NAV_TREE.map((g) => ({ ...g, items: g.items.filter(keep) })).filter((g) => g.items.length > 0);
export const V12_RAIL: NavGroup[] = grupSuz((it) => V12_RAIL_IDS.has(it.id));
export const V12_RAIL_MORE: NavGroup[] = grupSuz((it) => !V12_RAIL_IDS.has(it.id));
export const V12_TABS: NavItem[] = [I.today, I.learn, I.quick_add, I.past_exams];
/** Telefonda alt çubuğa konabilen / ızgarada duran her sayfa (Soru ekle ve Ayarlar hariç) */
export const V12_PHONE_PAGES: NavItem[] = NAV_TREE.flatMap((g) => g.items);
/**
 * Telefon "Tüm sayfalar" ızgarası: kenar menüsüyle aynı gruplar. Alt çubuk kişiselleştirilebildiği için (shell/phoneNav)
 * o an alt çubukta duranlar `exclude` ile çıkarılır; grupsuz "Bugün" ilk gruba katılır.
 */
export const v12PhoneTree = (exclude: ReadonlySet<AppRoute>): NavGroup[] => {
  const g = grupSuz((it) => !exclude.has(it.id));
  if (g[0] && g[0].label === null) {
    const [bas, ...kalan] = g;
    if (kalan[0]) return [{ ...kalan[0], items: [...bas.items, ...kalan[0].items] }, ...kalan.slice(1)];
    return [{ label: 'Sayfalar', items: bas.items }];
  }
  return g;
};

/** Global arama paletini aç (üst çubuk dinler; kenar menüsü ve kısayollar tetikler) */
export const openSearch = () => window.dispatchEvent(new CustomEvent('medsoru:search'));

export const initialsOf = (u: { displayName?: string | null; email?: string | null } | null) => {
  const src = (u?.displayName || u?.email || 'Ö').trim();
  const parts = src.split(/[^\p{L}]+/u).filter(Boolean);
  return ((parts[0]?.[0] || 'Ö') + (parts[1]?.[0] || '')).toLocaleUpperCase('tr-TR');
};
