import {
  Activity,
  Archive,
  BookOpen,
  BookOpenText,
  Compass,
  Crosshair,
  GraduationCap,
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
  past_exams: { id: 'past_exams', label: 'Çıkmış sorular', short: 'Çıkmış', hint: 'Kurullara göre çıkmışlar', icon: Archive, tint: '#007AFF' },
  ornek_sorular: { id: 'ornek_sorular', label: 'Örnek sorular', short: 'Örnek', hint: 'Kazanım temelli sorular', icon: Target, tint: '#FF9500' },
  questions: { id: 'questions', label: 'Soru havuzu', short: 'Havuz', hint: 'Kurul sorularını birlikte kur', icon: Library, tint: '#5856D6' },
  study: { id: 'study', label: 'Çalış', hint: 'Soru çöz, not al, kendini sına', icon: ListChecks, tint: '#34C759' },
  kazanimlar: { id: 'kazanimlar', label: 'Kazanımlar', hint: 'Müfredat ve kazanım haritası', icon: Compass, tint: '#00A79D' },
  learn: { id: 'learn', label: 'Öğren', hint: 'İnteraktif ders desteleri', icon: GraduationCap, tint: '#AF52DE' },
  summaries: { id: 'summaries', label: 'Ders özetleri', short: 'Özetler', hint: 'Spot bilgiler, uzun okuma', icon: BookOpen, tint: '#FF6B3D' },
  spots: { id: 'spots', label: 'Sınav spotları', short: 'Spotlar', hint: 'En sık, ayırıcı bulgular, tuzaklar', icon: Crosshair, tint: '#FF3B30' },
  flashcards: { id: 'flashcards', label: 'Ezber kartları', short: 'Kartlar', hint: 'Aralıklı tekrar', icon: Layers, tint: '#32ADE6' },
  glossary: { id: 'glossary', label: 'Sözlük', hint: 'Hastalık ve ilaç ansiklopedisi', icon: BookOpenText, tint: '#A2845E' },
  diseases: { id: 'diseases', label: 'Hastalıklar', short: 'Atlas', hint: 'Tıbbi hastalık & klinik atlası', icon: Activity, tint: '#06B6D4' },
  matrix: { id: 'matrix', label: 'Soru haritası', short: 'Harita', hint: '1–100 doluluk', icon: LayoutGrid, tint: '#64748B' },
  leaderboard: { id: 'leaderboard', label: 'Sıralama', hint: 'En çok katkı verenler', icon: Trophy, tint: '#FFB340' },
  music: { id: 'music', label: 'Müzik', hint: 'Çalışırken dinle', icon: Music, tint: '#FF375F' },
  practice: { id: 'practice', label: 'Test çöz', short: 'Test', hint: 'Süreli deneme sınavı', icon: Timer, tint: '#0A84FF' },
  notes: { id: 'notes', label: 'Ders notları', short: 'Notlar', hint: 'Amfi slaytları ve ders notları', icon: NotebookPen, tint: '#FF9F0A' },
  stats: { id: 'stats', label: 'İstatistiklerim', short: 'İstatistik', hint: 'İlerleme, puan ve etkinlik', icon: BarChart3, tint: '#5E5CE6' },
  settings: { id: 'settings', label: 'Profil ve ayarlar', short: 'Ayarlar', hint: 'Tema, palet, yoğunluk, fotoğraf', icon: Settings2, tint: '#8E8E93' },
};

export const NAV_ITEMS = I;

/**
 * Menü grupları (v9, 2026-10-11): öğrencinin akışına göre — önce ÖĞREN, sonra SORU ÇÖZ, gerektiğinde BAŞVUR,
 * en sonda TOPLULUK ve KİŞİSEL. Grup içi sıra kullanım sıklığına göredir. "Soru ekle" menünün tepesinde tek
 * başına duran birincil düğmedir (SideNav); telefonda alt gezinmenin ortasındadır.
 */
export const NAV_TREE: NavGroup[] = [
  { label: 'Öğren', items: [I.today, I.learn, I.spots, I.flashcards, I.summaries] },
  { label: 'Soru çöz', items: [I.past_exams, I.ornek_sorular, I.study, I.practice] },
  { label: 'Başvuru', items: [I.glossary, I.diseases, I.kazanimlar] },
  { label: 'Topluluk', items: [I.questions, I.matrix, I.leaderboard] },
  { label: 'Kişisel', items: [I.stats, I.music] },
];

/** Telefonda alt gezinmede doğrudan duran sayfalar (v10 sıra: Ekle · Öğren · Havuz · Çıkmış; Kartlar "Daha"ya taşındı); gerisi "Daha" sayfasında */
export const TAB_ITEMS: NavItem[] = [I.quick_add, I.learn, I.questions, I.past_exams];

/** "Daha" sayfası: alt gezinmede olmayanlar, aynı gruplar ve sırayla */
export const MORE_TREE: NavGroup[] = NAV_TREE.map((g) => ({ ...g, items: g.items.filter((it) => !TAB_ITEMS.includes(it)) })).filter((g) => g.items.length > 0);

/** Global arama paletini aç (üst çubuk dinler; kenar menüsü ve kısayollar tetikler) */
export const openSearch = () => window.dispatchEvent(new CustomEvent('medsoru:search'));

export const initialsOf = (u: { displayName?: string | null; email?: string | null } | null) => {
  const src = (u?.displayName || u?.email || 'Ö').trim();
  const parts = src.split(/[^\p{L}]+/u).filter(Boolean);
  return ((parts[0]?.[0] || 'Ö') + (parts[1]?.[0] || '')).toLocaleUpperCase('tr-TR');
};
