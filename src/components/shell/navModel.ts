import {
  Bell,
  Stethoscope,
  Medal,
  Gauge,
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
  CalendarDays,
  CalendarClock,
  Gamepad2,
  RotateCcw,
  Network,
  MessagesSquare,
  UserPlus,
  FileDown,
  Grid3x3,
  ArrowDownUp,
  Languages,
  ListTodo,
  LifeBuoy,
} from 'lucide-react';
import type React from 'react';
import type { AppRoute } from '../../router';
import { menudeGorunur, siteAyarAbone } from '../../services/siteAyar';

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
  kmb_asistan: { id: 'kmb_asistan', label: 'KMB sesli dersler', short: 'KMB', tile: 'KMB dersleri', hint: 'Klinik mesleki beceri: sesli ve videolu öğren, hedeflerle çalış, OSCE ve vaka sınavı', icon: Stethoscope, tint: '#0E7490' },
  son_prova: { id: 'son_prova', label: 'Son Prova', short: 'Prova', tile: 'Son Prova', hint: 'Kurulun tüm dersleri sesli özetle, aşama soruları, check-up ve 100 soruluk 3 deneme', icon: Flag, tint: '#E11D48' },
  genetik_checkup: { id: 'genetik_checkup', label: 'TBG Check Up', short: 'TBG', tile: 'TBG Check Up', hint: 'TBG Sınav Kampı v1: sesli ders, soru çözerek tekrar, kalıp kartları, deneme — her biri ayrı sayfa', icon: Dna, tint: '#10B981' },
  cikmis_cozucu: { id: 'cikmis_cozucu', label: 'Çıkmış çözücü', short: 'Çıkmış', tile: 'Çıkmış çözücü', hint: 'Sınav soru sayısı kadar çıkmış paketleri, sesli asistanla birlikte çöz', icon: History, tint: '#7C3AED' },
  kamp: { id: 'kamp', label: 'Kurul kampı', short: 'Kamp', tile: 'Kurul kampı', hint: 'Hocanın derste verdiği ipuçlarından hızlı tekrar: sesli anlatım, kalıp kartları, deneme', icon: Tent, tint: '#EA580C' },
  spots: { id: 'spots', label: 'Sınav spotları', short: 'Spotlar', hint: 'En sık, ayırıcı bulgular, tuzaklar', icon: Crosshair, tint: '#FF3B30' },
  // Soru çöz
  past_exams: { id: 'past_exams', label: 'Çıkmış sorular', short: 'Çıkmış', hint: 'Kurullara göre çıkmışlar', icon: Archive, tint: '#007AFF' },
  questions: { id: 'questions', label: 'Soru havuzu', short: 'Havuz', hint: 'Öğrencilerin birlikte kurduğu kurul soruları', icon: Library, tint: '#5856D6' },
  ornek_sorular: { id: 'ornek_sorular', label: 'Örnek sorular', short: 'Örnek', hint: 'Kazanım temelli sorular', icon: Target, tint: '#FF9500' },
  yanlislarim: { id: 'yanlislarim', label: 'Yanlışlarım', short: 'Yanlışlar', tile: 'Yanlışlarım', hint: 'Yanlış yaptığın sorular 48 saat sonra yeniden', icon: RotateCcw, tint: '#FF3B30' },
  oyunlar: { id: 'oyunlar', label: 'Oyunlar', short: 'Oyun', tile: 'Oyunlar', hint: 'Canlı soru yarışması: oda kur, kodu paylaş', icon: Gamepad2, tint: '#AF52DE' },
  soru_haritasi: { id: 'soru_haritasi', label: 'Soru haritası', short: 'Harita', tile: 'Soru haritası', hint: 'Ders × yıl: hangi dersten kaç çıkmış soru', icon: Grid3x3, tint: '#5E5CE6' },
  olasi_sorular: { id: 'olasi_sorular', label: 'Olası sorular', short: 'Olası', hint: 'Sınavdan sonra hatıralardan kurulan sorular; çöz, doğrula', icon: Sparkles, tint: '#AF52DE' },
  practice: { id: 'practice', label: 'Deneme sınavı', short: 'Deneme', hint: 'Süreli deneme sınavı', icon: Timer, tint: '#0A84FF' },
  // Başvuru
  glossary: { id: 'glossary', label: 'Sözlük', hint: 'Hastalık ve ilaç ansiklopedisi', icon: BookOpenText, tint: '#A2845E' },
  diseases: { id: 'diseases', label: 'Hastalıklar', short: 'Atlas', hint: 'Tıbbi hastalık ve klinik atlası', icon: Activity, tint: '#06B6D4' },
  health_ministry: { id: 'health_ministry', label: 'Sağlık Bakanlığı', short: 'Bakanlık', hint: 'Resmî veriler: aşı, yenidoğan, anne, tarama, salgın, Karabük', icon: Landmark, tint: '#C8102E' },
  gecmis_kurullar: { id: 'gecmis_kurullar', label: 'Geçmiş kurullar', short: 'Geçmiş', tile: 'Geçmiş kurullar', hint: 'Sınavı biten kurulların dersleri, spotları ve soruları', icon: History, tint: '#8E8E93' },
  guncellemeler: { id: 'guncellemeler', label: 'Güncelleme günlüğü', short: 'Sürümler', tile: 'Güncellemeler', hint: 'Her sürümde eklenen, değişen ve kaldırılanlar', icon: ScrollText, tint: '#5E5CE6' },
  oncelikli_dersler: { id: 'oncelikli_dersler', label: 'Öncelikli dersler', short: 'Öncelikli', tile: 'Öncelikli dersler', hint: 'Az ezberli, mantıkla çözülen, kolay puan getiren sesli dersler önce', icon: Gauge, tint: '#34C759' },
  kazanimlar: { id: 'kazanimlar', label: 'Kazanımlar', hint: 'Müfredat ve kazanım haritası', icon: Compass, tint: '#00A79D' },
  // Topluluk
  matrix: { id: 'matrix', label: 'Havuz doluluğu', short: 'Doluluk', hint: 'Havuzda 1–100 soru doluluğu', icon: LayoutGrid, tint: '#64748B' },
  leaderboard: { id: 'leaderboard', label: 'Sıralama', hint: 'Dönemindeki haftalık ve kurul sıralaması', icon: Trophy, tint: '#FFB340' },
  // Kişisel
  study: { id: 'study', label: 'Listelerim ve notlar', short: 'Listelerim', tile: 'Listelerim', hint: 'Kaydettiğin sorular, notların, kendi testin (günün akışı Bugün sayfasında)', icon: ListChecks, tint: '#34C759' },
  cevrimdisi: { id: 'cevrimdisi', label: 'Çevrimdışı ve indirmeler', short: 'Çevrimdışı', tile: 'Çevrimdışı ve indirmeler', hint: 'İndirme kuyruğu, arka plan işleri, indirilenler ve eşitleme' /* H306 */, icon: CloudDownload, tint: '#0A84FF' },
  basarimlar: { id: 'basarimlar', label: 'Başarımlar', short: 'Başarım', tile: 'Başarımlar', hint: 'Günlük, haftalık, kurul hedefleri; başarımlar, puan ve ATP', icon: Medal, tint: '#FF9F0A' },
  zihin_haritasi: { id: 'zihin_haritasi', label: 'Zihin haritası', short: 'Harita', tile: 'Zihin haritası', hint: 'Dersin bölümleri ve anahtar terimleri tek bakışta', icon: Network, tint: '#FF2D55' },
  ders_programi: { id: 'ders_programi', label: 'Ders programı', short: 'Program', tile: 'Ders programı', hint: 'Kurulun günlük ve haftalık ders saatleri', icon: CalendarClock, tint: '#30B0C7' },
  sinav_takvimi: { id: 'sinav_takvimi', label: 'Sınav takvimi', short: 'Takvim', tile: 'Sınav takvimi', hint: 'Kurul sınavları, final ve bütünleme; kalan gün', icon: CalendarDays, tint: '#FF9F0A' },
  sinav_plani: { id: 'sinav_plani', label: 'Sınav planı', short: 'Plan', tile: 'Sınav planı', hint: 'En az 60 için kişiye özel, gün gün yol haritası', icon: Target, tint: '#FF9F0A' },
  hucrem: { id: 'hucrem', label: 'Hücrem', short: 'Hücrem', tile: 'Hücrem', hint: 'ATP ile hücreni 28 evrim basamağında büyüt', icon: Dna, tint: '#34C759' },
  arkadaslar: { id: 'arkadaslar', label: 'Arkadaşlar', short: 'Arkadaş', tile: 'Arkadaşlar', hint: 'Arkadaş ekle, mesajlaş, soru çözmeye davet et', icon: UserPlus, tint: '#34C759' },
  topluluk: { id: 'topluluk', label: 'Topluluk', short: 'Topluluk', tile: 'Topluluk', hint: 'Sohbet kanalları ve ders yorumları', icon: MessagesSquare, tint: '#32ADE6' },
  pdf_olustur: { id: 'pdf_olustur', label: 'PDF oluştur', short: 'PDF', tile: 'PDF oluştur', hint: 'Ders metinlerini tek ya da ayrı PDF olarak indir', icon: FileDown, tint: '#FF3B30' },
  bildirimler: { id: 'bildirimler', label: 'Bildirimler', short: 'Bildirim', tile: 'Bildirimler', hint: 'Yeni ders, sınav hatırlatması, tekrar zamanı, yorum ve düzeltmeler', icon: Bell, tint: '#FF3B30' },
  notlarim: { id: 'notlarim', label: 'Notlarım', short: 'Notlar', tile: 'Notlarım', hint: 'Yaz, kalemle çiz, fosforluyla işaretle; hesabına kaydedilir', icon: NotebookPen, tint: '#FF9F0A' },
  bitirdiklerim: { id: 'bitirdiklerim', label: 'Bitirdiklerim', short: 'Bitenler', tile: 'Bitirdiklerim', hint: 'Konu konu bitenler, harcanan süre, kalanların tahmini', icon: CircleCheckBig, tint: '#30D158' },
  stats: { id: 'stats', label: 'İstatistiklerim', short: 'İstatistik', tile: 'İstatistik', hint: 'İlerleme, puan ve etkinlik', icon: BarChart3, tint: '#5E5CE6' },
  music: { id: 'music', label: 'Müzik', hint: 'Çalışırken dinle', icon: Music, tint: '#FF375F' },
  arka_plan: { id: 'arka_plan', label: 'Arka plan işleri', short: 'Arka plan', tile: 'Arka plan işleri', hint: 'Süren indirmeler, video dışa aktarımı ve eşitleme', icon: ArrowDownUp, tint: '#0A84FF' },
  ilk_adimlar: { id: 'ilk_adimlar', label: 'İlk adımlar', short: 'İlk adımlar', tile: 'İlk adımlar', hint: 'Başlangıç görevleri: profil, ilk ders, ilk sorular', icon: ListTodo, tint: '#30D158' },
  dil_bolge: { id: 'dil_bolge', label: 'Dil ve bölge', short: 'Dil, bölge', tile: 'Dil ve bölge', hint: 'Tarih ve saat biçimi, haftanın ilk günü', icon: Languages, tint: '#8E8E93' },
  yardim: { id: 'yardim', label: 'Yardım', short: 'Yardım', tile: 'Yardım', hint: 'Sık sorulanlar, klavye kısayolları, iletişim', icon: LifeBuoy, tint: '#5E5CE6' },
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
export const NAV_TREE_HAM: NavGroup[] = [
  { label: null, items: [I.today] },
  { label: 'Ders çalış', items: [I.canli_ders, I.kmb_asistan, I.learn, I.summaries, I.flashcards, I.ders_programi, I.oncelikli_dersler, I.gecmis_kurullar] },
  { label: 'Soru çöz', items: [I.soru_cozucu, I.past_exams, I.practice, I.questions, I.ornek_sorular, I.olasi_sorular, I.yanlislarim, I.oyunlar, I.soru_haritasi] },
  { label: 'Sınava hazırlan', items: [I.sinav_takvimi, I.sinav_plani, I.son_prova, I.cikmis_cozucu, I.kamp, I.en_onemliler, I.spots] },
  { label: 'Check Up', items: [I.genetik_checkup, I.patoloji_checkup] },
  { label: 'Başvuru', items: [I.glossary, I.diseases, I.health_ministry, I.kazanimlar] },
  { label: 'Topluluk', items: [I.topluluk, I.arkadaslar, I.hucrem, I.leaderboard, I.matrix] },
  { label: 'Kişisel', items: [I.bitirdiklerim, I.basarimlar, I.guncellemeler, I.cevrimdisi, I.study, I.stats, I.music, I.ilk_adimlar, I.dil_bolge /* H306: arka_plan çıktı, cevrimdisi tek giriş */, I.yardim] },
];

/** Çalışma anında süzülür (services/siteAyar menudeGorunur; panel › Site › Görünürlük). Dizi yerinde güncellenir. */
export const NAV_TREE: NavGroup[] = [];

/** Telefonda alt gezinmede doğrudan duran sayfalar (v10 sıra: Ekle · Öğren · Havuz · Çıkmış); gerisi "Daha" sayfasında */
export const TAB_ITEMS: NavItem[] = [I.quick_add, I.learn, I.questions, I.past_exams];

/** "Daha" sayfası: alt gezinmede olmayanlar, aynı gruplar ve sırayla */
export const MORE_TREE: NavGroup[] = [];

/**
 * v12 "Net" gezinmesi (components/v12/ShellV12). Kenar menüsü NAV_TREE gruplarını aynı adlarla gösterir; her grupta
 * en sık sayfalar (V12_RAIL_IDS) doğrudan görünür, gerisi "Daha fazla" açılırında yine kendi grup adıyla.
 * Telefonda alt çubuk: Bugün · Öğren · [+ Soru ekle] · Çıkmış · Daha.
 */
const V12_RAIL_IDS = new Set<AppRoute>([
  'today',
  'canli_ders', 'kmb_asistan', 'learn', 'summaries', 'flashcards', 'ders_programi',
  'soru_cozucu', 'past_exams', 'practice', 'questions', 'olasi_sorular',
  'sinav_takvimi', 'sinav_plani', 'son_prova', 'cikmis_cozucu', 'kamp', 'en_onemliler', 'spots',
  'genetik_checkup', 'patoloji_checkup',
  'glossary', 'diseases',
  'bitirdiklerim', 'cevrimdisi', 'basarimlar',
]);
const grupSuz = (keep: (it: NavItem) => boolean): NavGroup[] =>
  NAV_TREE.map((g) => ({ ...g, items: g.items.filter(keep) })).filter((g) => g.items.length > 0);
export const V12_RAIL: NavGroup[] = [];
export const V12_RAIL_MORE: NavGroup[] = [];
export const V12_TABS: NavItem[] = [I.today, I.learn, I.quick_add, I.past_exams];
/** Telefonda alt çubuğa konabilen / ızgarada duran her sayfa (Soru ekle ve Ayarlar hariç) */
export const V12_PHONE_PAGES: NavItem[] = [];

const yerine = <T,>(a: T[], b: T[]) => { a.splice(0, a.length, ...b); };
function menuSuz() {
  yerine(NAV_TREE, NAV_TREE_HAM.map((g) => ({ ...g, items: g.items.filter((it) => menudeGorunur(it.id)) })).filter((g) => g.items.length > 0));
  yerine(MORE_TREE, NAV_TREE.map((g) => ({ ...g, items: g.items.filter((it) => !TAB_ITEMS.includes(it)) })).filter((g) => g.items.length > 0));
  yerine(V12_RAIL, grupSuz((it) => V12_RAIL_IDS.has(it.id)));
  yerine(V12_RAIL_MORE, grupSuz((it) => !V12_RAIL_IDS.has(it.id)));
  yerine(V12_PHONE_PAGES, NAV_TREE.flatMap((g) => g.items));
}
menuSuz();
siteAyarAbone(menuSuz);
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
